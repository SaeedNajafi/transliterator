import torch
import numpy as np
import torch.nn as nn
from torch.nn import init
from torch.autograd import Variable

hasCuda = torch.cuda.is_available()

class RLTrain(nn.Module):
    """
    This module applies RL training to the decoder RNN.
    It has 2 variants:
        1- 'BR': Reinforce with baseline
        2- 'AC': Actor-critic
    """

    def __init__(self, cfg):
        super(RLTrain, self).__init__()

        self.cfg = cfg

        #Critic:
        self.cr_size = 2 * cfg.h_units

        self.layer1 = nn.Linear(
                            self.cr_size,
                            self.cr_size,
                            bias=True
                            )

        self.layer2 = nn.Linear(
                            self.cr_size,
                            self.cr_size,
                            bias=True
                            )

        self.layer3 = nn.Linear(
                            self.cr_size,
                            1,
                            bias=True
                            )
        self.param_init()

        return

    def param_init(self):
        for name, param in self.named_parameters():
            if 'bias' in name:
                init.constant(param, 0.0)
            if 'weight' in name:
                init.xavier_uniform(param)
        return

    #Critic approximates the state-value function of a state.
    def V(self, S):
        #Do not back propagate through S!
        in_S = Variable(S.data.cuda(), requires_grad=False) if hasCuda else Variable(S.data, requires_grad=False)

        cfg = self.cfg
        l = cfg.gamma
        if l>=1 or l<0:
            print "INFO: 0 <= discount factor < 1 !"
            exit()

        #We do not apply any dropout layer as this is a regression model
        #and the optimizer will apply L2 regularization on the weights.
        H1 = nn.functional.leaky_relu(self.layer1(in_S))
        H2 = nn.functional.leaky_relu(self.layer2(H1))
        H3 = nn.functional.sigmoid(self.layer3(H2))
        #H3 is now scaler between 0 and 1

        v = torch.div(H3, 1.0-l)
        #v is now scaler between 0 and 1.0-l which are the boundries for returns w.r.t. l and 0/1 rewards.

        return v.view(cfg.d_batch_size, cfg.max_length)

    #least square loss for V.
    #L2 regularization will be done by optimizer.
    def V_loss(self, Returns, prev_V):
        """
            Returns are the temporal difference or monte carlo returns calculated for
            each step. They are the target regression values for the Critic V.
            prev_V is the previous estimates of the Critic V for the returns.
            We want to minimize the Mean Squared Error between Returns and prev_V.
        """
        cfg = self.cfg
        #Do not back propagate through Returns!
        in_Returns = Variable(Returns.data.cuda(), requires_grad=False) if hasCuda else Variable(Returns.data, requires_grad=False)

        #mask pad
        y_mask = Variable(cfg.B['y_mask'].cuda()) if hasCuda else Variable(cfg.B['y_mask'])

        #No negative, this is MSE loss
        MSEloss = torch.mean(torch.mean(torch.pow(prev_V-in_Returns, 2.0) * y_mask, dim=1), dim=0)

        #MSEloss will be plugged in a separate optimizer.
        return MSEloss

    def forward(self, H, mldecoder):
        cfg = self.cfg
        dec_rnn = mldecoder.dec_rnn
        affine = mldecoder.affine
        trg_em = mldecoder.trg_em
        if cfg.atten=='soft-general':
            atten_W = mldecoder.atten_W
            atten_affine = mldecoder.atten_affine

        #zero the pad vector
        trg_em.weight.data[cfg.trg_pad_id].fill_(0.0)

        #Create a variable for initial hidden vector of RNN.
        zeros = torch.zeros(cfg.d_batch_size, cfg.h_units)
        h0 = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        #Create a variable for the initial previous tag.
        zeros = torch.zeros(cfg.d_batch_size, cfg.trg_em_size)
        Go_symbol = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        if cfg.atten=='soft-general':
            #global general attention as https://nlp.stanford.edu/pubs/emnlp15_attn.pdf
            states_mapped = torch.mm(H.view(-1, cfg.h_units), atten_W).view(-1, cfg.max_length, cfg.h_units)

        #critic V estimates
        states = []
        taken_actions = []
        action_log_policies = []
        for i in range(cfg.max_length):
            H_i = H[:,i,:]
            if i==0:
                prev_output = Go_symbol
                h = h0
                c = h0
                context = h0

            input = torch.cat((prev_output, context), dim=1)

            output, c = dec_rnn(input, (h, c))

            if cfg.atten=='hard-monotonic':
                context = Hi
                output_context = torch.cat((output, context), dim=1)
                score = affine(output_context)
                states.append(output_context)

            elif cfg.atten=='soft-general':
                atten_scores = torch.sum(states_mapped * output.view(-1, 1, cfg.h_units).expand(-1, cfg.max_length, cfg.h_units), dim=2)
                atten = nn.functional.softmax(atten_scores, dim=1)
                context = torch.sum(atten.view(-1, cfg.max_length, 1).expand(-1, cfg.max_length, cfg.h_units) * H, dim=1)
                score = affine(nn.functional.tanh(atten_affine(torch.cat((output, context), dim=1))))
                states.append(torch.cat((output, context), dim=1))

            #For the next step
            h = output

            log_p, gen_idx = nn.functional.log_softmax(score, dim=1).max(dim=1)
            prev_output = trg_em(gen_idx)
            taken_actions.append(gen_idx)
            action_log_policies.append(log_p)

        S = torch.stack(states, dim=1)
        V_es = self.V(S)
        taken_actions = torch.stack(taken_actions, dim=1)
        action_log_policies = torch.stack(action_log_policies, dim=1)

        type = cfg.rltrain_type

        if type=='BR':
            return self.REINFORCE(V_es, taken_actions, action_log_policies)
        elif type=='AC':
            return self.Actor_Critic(V_es, taken_actions, action_log_policies)

        else:
            print "INFO: RLTrain type error!"
            exit()

        return None, None

    def REINFORCE(self, V_es, taken_actions, action_log_policies):
        cfg = self.cfg
        l = cfg.gamma

        #Building gamma matrix to calculate return for each step.
        powers = np.arange(cfg.max_length)
        bases = np.full((1,cfg.max_length), l)
        rows = np.power(bases, powers)
        inverse_rows = 1.0/rows
        inverse_cols = inverse_rows.reshape((cfg.max_length, 1))
        gammaM = np.triu(np.multiply(inverse_cols, rows))
        gM_tensor = torch.from_numpy(gammaM.T).float()
        if hasCuda:
            gM = Variable(gM_tensor.cuda(), requires_grad=False)
        else:
            gM = Variable(gM_tensor, requires_grad=False)

        Y = Variable(cfg.B['y'].cuda()) if hasCuda else Variable(cfg.B['y'])
        y_mask = Variable(cfg.B['y_mask'].cuda()) if hasCuda else Variable(cfg.B['y_mask'])

        is_true_y = torch.eq(taken_actions, Y)
        #0/1 reward (hamming loss) for each prediction.
        rewards = is_true_y.float() * y_mask
        V_es = V_es * y_mask
        Returns = torch.matmul(rewards, gM)
        advantages = Returns - V_es
        pos_neq = torch.ge(advantages, 0.0).float()
        signs = torch.eq(pos_neq, rewards).float()

        #Do not back propagate through Returns and V_es!
        #biased advantage in favor of true tags, against wrong tags.
        #if the advantage was negative for a true tag, or
        #the advantage was positive for a wrong tag, make the advantages zero!
        biased_advantages = signs * advantages
        if hasCuda:
            deltas = Variable(biased_advantages.data.cuda(), requires_grad=False)
        else:
            deltas = Variable(biased_advantages.data, requires_grad=False)

        rlloss = -torch.mean(torch.mean(action_log_policies * deltas * y_mask, dim=1), dim=0)
        vloss = self.V_loss(Returns, V_es)
        return rlloss, vloss

    def Actor_Critic(self, V_es, taken_actions, action_log_policies):
        cfg = self.cfg
        l = cfg.gamma
        n = cfg.n_step
        if n<0:
            print "INFO: 1 <= n step !"
            exit()

        #Building gamma matrix to calculate return for each step.
        powers = np.arange(cfg.max_length)
        bases = np.full((1,cfg.max_length), l)
        rows = np.power(bases, powers)
        inverse_rows = 1.0/rows
        inverse_cols = inverse_rows.reshape((cfg.max_length,1))
        gammaM = np.tril(np.triu(np.multiply(inverse_cols, rows)), k=n-1)
        gM_tensor = torch.from_numpy(gammaM.T).float()

        """
            for n = 3, gamma=0.9
            gM_tensor:

            array(
                    [[1.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0. ],
                    [0.9 , 1.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  ],
                    [0.81, 0.9 , 1.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  ],
                    [0.  , 0.81, 0.9 , 1.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  ],
                    [0.  , 0.  , 0.81, 0.9 , 1.  , 0.  , 0.  , 0.  , 0.  , 0.  ],
                    [0.  , 0.  , 0.  , 0.81, 0.9 , 1.  , 0.  , 0.  , 0.  , 0.  ],
                    [0.  , 0.  , 0.  , 0.  , 0.81, 0.9 , 1.  , 0.  , 0.  , 0.  ],
                    [0.  , 0.  , 0.  , 0.  , 0.  , 0.81, 0.9 , 1.  , 0.  , 0.  ],
                    [0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.81, 0.9 , 1.  , 0.  ],
                    [0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.81, 0.9 , 1.  ]
                    ])
        """

        if hasCuda:
            gM = Variable(gM_tensor.cuda(), requires_grad=False)
        else:
            gM = Variable(gM_tensor, requires_grad=False)

        Y = Variable(cfg.B['y'].cuda()) if hasCuda else Variable(cfg.B['y'])
        y_mask = Variable(cfg.B['y_mask'].cuda()) if hasCuda else Variable(cfg.B['y_mask'])

        is_true_y = torch.eq(taken_actions, Y)
        #0/1 reward (hamming loss) for each prediction.
        rewards = is_true_y.float() * y_mask
        V_es = V_es * y_mask
        Returns = torch.matmul(rewards, gM)
        for i in range(cfg.max_length-n):
            Returns[:,i].data = Returns[:,i].data + (l ** n) * V_es[:, i + n].data

        advantages = Returns - V_es
        pos_neq = torch.ge(advantages, 0.0).float()
        signs = torch.eq(pos_neq, rewards).float()

        #Do not back propagate through Returns and V_es!
        biased_advantages = signs * advantages
        if hasCuda:
            deltas = Variable(biased_advantages.data.cuda(), requires_grad=False)
        else:
            deltas = Variable(biased_advantages.data, requires_grad=False)

        rlloss = -torch.mean(torch.mean(action_log_policies * deltas * y_mask, dim=1), dim=0)
        vloss = self.V_loss(Returns, V_es)
        return rlloss, vloss
