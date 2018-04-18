import torch
import numpy as np
import torch.nn as nn
from torch.nn import init
from torch.autograd import Variable

hasCuda = torch.cuda.is_available()

class MLDecoder(nn.Module):
    """
    This module is for prediction of the tags using a decoder RNN.
    It has 3 variants for ML training:
        1-TF: Teachor Forcing
        2-SS: Scheduled Sampling
        3-DS: Differential Scheduled Sampling

    The decoder rnn can have general attention or not.
    """

    def __init__(self, cfg):
        super(MLDecoder, self).__init__()

        self.cfg = cfg

        #Size of input feature vectors
        in_size = cfg.h_units + cfg.trg_em_size
        self.dec_rnn = nn.LSTMCell(
                            input_size=in_size,
                            hidden_size=cfg.h_units,
                            bias=True
                            )

        self.drop = nn.Dropout(cfg.dropout)

        if cfg.atten=='soft-general':
            self.atten_W = nn.Parameter(torch.Tensor(cfg.h_units, cfg.h_units), requires_grad=True)

            self.atten_affine = nn.Linear(
                                2 * cfg.h_units,
                                cfg.h_units,
                                bias=True
                                )

            self.affine = nn.Linear(
                                cfg.h_units,
                                cfg.trg_alphabet_size,
                                bias=True
                                )

        elif cfg.atten=='hard-monotonic':
            self.affine = nn.Linear(
                                2 * cfg.h_units,
                                cfg.trg_alphabet_size,
                                bias=True
                                )

        self.param_init()
        self.embeddings()

        return

    def param_init(self):
        for name, param in self.named_parameters():
            if 'bias' in name:
                init.constant(param, 0.0)
            if 'weight' in name:
                init.xavier_uniform(param)

        if self.cfg.atten=='soft-general':
            init.xavier_uniform(self.atten_W)

        return

    def embeddings(self):
        cfg = self.cfg

        trg_lt = torch.FloatTensor(cfg.data['trg_vec']) #target lookup table
        self.trg_em = nn.Embedding(cfg.trg_alphabet_size, cfg.trg_em_size)
        self.trg_em.weight.data.copy_(trg_lt)
        self.trg_em.weight.data[cfg.trg_pad_id].fill_(0.0)
        self.trg_em.weight.requires_grad = True
        return

    def forward(self, H):
        cfg = self.cfg
        """
            Type can have three values:
            'TF': teacher force
            'SS': scheduled sampling
            'DS': differential scheduled sampling
        """
        type = cfg.mldecoder_type
        if type=='TF':
            return self.TF_forward(H)
        elif type=='SS':
            return self.SS_forward(H)
        elif type=='DS':
            return self.DS_forward(H)
        else:
            print "INFO: MLDecoder Error!"
            exit()

    def TF_forward(self, H):
        cfg = self.cfg

        #zero the pad vector
        self.trg_em.weight.data[cfg.trg_pad_id].fill_(0.0)

        Y = Variable(cfg.B['y'].cuda()) if hasCuda else Variable(cfg.B['y'])


        Y_ems = self.trg_em(Y)

        #Create a variable for initial hidden vector of RNN.
        zeros = torch.zeros(cfg.d_batch_size, cfg.h_units)
        h0 = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        #Create a variable for the initial previous tag.
        zeros = torch.zeros(cfg.d_batch_size, cfg.trg_em_size)
        Go_symbol = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        if cfg.atten=='soft-general':
            #global general attention as https://nlp.stanford.edu/pubs/emnlp15_attn.pdf
            states_mapped = torch.mm(H.view(-1, cfg.h_units), self.atten_W).view(-1, cfg.max_length, cfg.h_units)

        Scores = []
        for i in range(cfg.max_length):
            Hi = H[:,i,:]
            if i==0:
                prev_output = Go_symbol
                h = h0
                c = h0
                context = h0

            input = torch.cat((prev_output, context), dim=1)

            output, c = self.dec_rnn(input, (h, c))

            output_dr = self.drop(output)

            if cfg.atten=='hard-monotonic':
                context = Hi
                output_dr_context = torch.cat((output_dr, context), dim=1)
                score = self.affine(output_dr_context)

            elif cfg.atten=='soft-general':
                atten_scores = torch.sum(states_mapped * output_dr.view(-1, 1, cfg.h_units).expand(-1, cfg.max_length, cfg.h_units), dim=2)
                atten = nn.functional.softmax(atten_scores, dim=1)
                context = torch.sum(atten.view(-1, cfg.max_length, 1).expand(-1, cfg.max_length, cfg.h_units) * H, dim=1)
                score = self.affine(nn.functional.tanh(self.atten_affine(torch.cat((output_dr, context), dim=1))))

            Scores.append(score)

            #For the next step
            h = output

            #Teachor Force the previous gold tag.
            prev_output = Y_ems[:,i,:]


        #Return log_probs
        return nn.functional.log_softmax(torch.stack(Scores, dim=1), dim=2)

    def SS_forward(self, H):
        cfg = self.cfg

        #Sampling probability to use generated previous tag or the gold previous tag.
        sp = cfg.sampling_p

        flip_coin = torch.rand(cfg.d_batch_size, cfg.max_length)

        #If equal to or greater than the sampling probabiliy,
        #we will use the generated previous tag.
        switch = torch.ge(flip_coin, sp).float()

        sw = Variable(switch.cuda(), requires_grad=False) if hasCuda else Variable(switch, requires_grad=False)
        sw_expanded = sw.view(-1, cfg.max_length, 1).expand(-1, cfg.max_length, cfg.trg_em_size)

        #zero the pad vector
        self.trg_em.weight.data[cfg.trg_pad_id].fill_(0.0)

        Y = Variable(cfg.B['y'].cuda()) if hasCuda else Variable(cfg.B['y'])


        Y_ems = self.trg_em(Y)

        #Create a variable for initial hidden vector of RNN.
        zeros = torch.zeros(cfg.d_batch_size, cfg.h_units)
        h0 = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        #Create a variable for the initial previous tag.
        zeros = torch.zeros(cfg.d_batch_size, cfg.trg_em_size)
        Go_symbol = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        if cfg.atten=='soft-general':
            #global general attention as https://nlp.stanford.edu/pubs/emnlp15_attn.pdf
            states_mapped = torch.mm(H.view(-1, cfg.h_units), self.atten_W).view(-1, cfg.max_length, cfg.h_units)

        Scores = []
        for i in range(cfg.max_length):
            Hi = H[:,i,:]
            if i==0:
                prev_output = Go_symbol
                h = h0
                c = h0
                context = h0

            input = torch.cat((prev_output, context), dim=1)

            output, c = self.dec_rnn(input, (h, c))

            output_dr = self.drop(output)

            if cfg.atten=='hard-monotonic':
                context = Hi
                output_dr_context = torch.cat((output_dr, context), dim=1)
                score = self.affine(output_dr_context)

            elif cfg.atten=='soft-general':
                atten_scores = torch.sum(states_mapped * output_dr.view(-1, 1, cfg.h_units).expand(-1, cfg.max_length, cfg.h_units), dim=2)
                atten = nn.functional.softmax(atten_scores, dim=1)
                context = torch.sum(atten.view(-1, cfg.max_length, 1).expand(-1, cfg.max_length, cfg.h_units) * H, dim=1)
                score = self.affine(nn.functional.tanh(self.atten_affine(torch.cat((output_dr, context), dim=1))))

            Scores.append(score)

            #For the next step
            h = output

            #Greedily generated previous tag or the gold previous one?
            gold_prev_output = Y_ems[:,i,:]
            _, gen_idx = nn.functional.softmax(score, dim=1).max(dim=1)
            generated_prev_output = self.trg_em(gen_idx)
            sw_expanded_i = sw_expanded[:,i,:]
            prev_output = sw_expanded_i * generated_prev_output + (1.0-sw_expanded_i) * gold_prev_output

        #Return log_probs
        return nn.functional.log_softmax(torch.stack(Scores, dim=1), dim=2)

    def DS_forward(self, H):
        cfg = self.cfg

        #Sampling probability to use generated previous tag or the gold previous tag.
        sp = cfg.sampling_p

        #We feed the probability-weighted average of all tag embeddings biased strongly
        #towards the greedily generated tag.
        bias_tensor = torch.FloatTensor(1,).fill_(cfg.greedy_bias)
        bias = Variable(bias_tensor.cuda()) if hasCuda else Variable(bias_tensor)

        flip_coin = torch.rand(cfg.d_batch_size, cfg.max_length)

        #If equal to or greater than the sampling probabiliy,
        #we will use the generated previous tag.
        switch = torch.ge(flip_coin, sp).float()

        sw = Variable(switch.cuda(), requires_grad=False) if hasCuda else Variable(switch, requires_grad=False)
        sw_expanded = sw.view(-1, cfg.max_length, 1).expand(-1, cfg.max_length, cfg.trg_em_size)

        #zero the pad vector
        self.trg_em.weight.data[cfg.trg_pad_id].fill_(0.0)

        Y = Variable(cfg.B['y'].cuda()) if hasCuda else Variable(cfg.B['y'])

        Y_ems = self.trg_em(Y)

        #Create a variable for initial hidden vector of RNN.
        zeros = torch.zeros(cfg.d_batch_size, cfg.h_units)
        h0 = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        #Create a variable for the initial previous tag.
        zeros = torch.zeros(cfg.d_batch_size, cfg.trg_em_size)
        Go_symbol = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        if cfg.atten=='soft-general':
            #global general attention as https://nlp.stanford.edu/pubs/emnlp15_attn.pdf
            states_mapped = torch.mm(H.view(-1, cfg.h_units), self.atten_W).view(-1, cfg.max_length, cfg.h_units)

        Scores = []
        for i in range(cfg.max_length):
            Hi = H[:,i,:]
            if i==0:
                prev_output = Go_symbol
                h = h0
                c = h0
                context = h0

            input = torch.cat((prev_output, context), dim=1)

            output, c = self.dec_rnn(input, (h, c))

            output_dr = self.drop(output)

            if cfg.atten=='hard-monotonic':
                context = Hi
                output_dr_context = torch.cat((output_dr, context), dim=1)
                score = self.affine(output_dr_context)

            elif cfg.atten=='soft-general':
                atten_scores = torch.sum(states_mapped * output_dr.view(-1, 1, cfg.h_units).expand(-1, cfg.max_length, cfg.h_units), dim=2)
                atten = nn.functional.softmax(atten_scores, dim=1)
                context = torch.sum(atten.view(-1, cfg.max_length, 1).expand(-1, cfg.max_length, cfg.h_units) * H, dim=1)
                score = self.affine(nn.functional.tanh(self.atten_affine(torch.cat((output_dr, context), dim=1))))

            Scores.append(score)

            #For the next step
            h = output


            #Greedily generated previous tag or the gold previous one?
            gold_prev_output = Y_ems[:,i,:]


            averaging_weights = nn.functional.softmax(bias * score, dim=1)
            #Weighted average of all tag embeddings biased strongly towards the greedy best tag.
            generated_prev_output = torch.mm(averaging_weights, self.trg_em.weight)
            sw_expanded_i = sw_expanded[:,i,:]
            prev_output = sw_expanded_i * generated_prev_output + (1.0-sw_expanded_i) * gold_prev_output

        #Return log_probs
        return nn.functional.log_softmax(torch.stack(Scores, dim=1), dim=2)

    def loss(self, log_probs):
        #ML loss
        cfg = self.cfg
        y_mask = Variable(cfg.B['y_mask'].cuda()) if hasCuda else Variable(cfg.B['y_mask'])
        y_one_hot = Variable(cfg.B['y_one_hot'].cuda()) if hasCuda else Variable(cfg.B['y_one_hot'])

        objective = torch.sum(y_one_hot * log_probs, dim=2) * y_mask
        loss = -1 * torch.mean(torch.mean(objective, dim=1), dim=0)
        return loss

    def beam(self, H):
        cfg = self.cfg
        beamsize = cfg.nbest

        #zero the pad vector
        self.trg_em.weight.data[cfg.trg_pad_id].fill_(0.0)

        #Create a variable for initial hidden vector of RNN.
        zeros = torch.zeros(cfg.d_batch_size, cfg.h_units)
        h0 = Variable(zeros.cuda()) if hasCuda else Variable(zeros)
        c0 = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        #Create a variable for the initial previous tag.
        zeros = torch.zeros(cfg.d_batch_size, cfg.trg_em_size)
        Go_symbol = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        very_negative = torch.zeros(cfg.d_batch_size)
        V_Neg = Variable(very_negative.cuda()) if hasCuda else Variable(very_negative)
        V_Neg.data.fill_(-10**10)

        pads = torch.zeros(cfg.d_batch_size)
        Pads = Variable(pads.cuda()) if hasCuda else Variable(pads)
        Pads.data.fill_(cfg.trg_pad_id)

        lprob_candidates = torch.zeros(cfg.d_batch_size, beamsize*beamsize)
        lprob_c = Variable(lprob_candidates.cuda()) if hasCuda else Variable(lprob_candidates)

        isEnd_candidates = torch.zeros(cfg.d_batch_size, beamsize*beamsize)
        isEnd_c = Variable(isEnd_candidates.cuda()) if hasCuda else Variable(isEnd_candidates)

        y_candidates = torch.zeros(cfg.d_batch_size, beamsize*beamsize).long()
        y_c = Variable(y_candidates.cuda()) if hasCuda else Variable(y_candidates)

        h_candidates = torch.zeros(cfg.d_batch_size, beamsize, cfg.h_units)
        h_c = Variable(h_candidates.cuda()) if hasCuda else Variable(h_candidates)

        c_candidates = torch.zeros(cfg.d_batch_size, beamsize, cfg.h_units)
        c_c = Variable(c_candidates.cuda()) if hasCuda else Variable(c_candidates)

        context_candidates = torch.zeros(cfg.d_batch_size, beamsize, cfg.h_units)
        context_c = Variable(context_candidates.cuda()) if hasCuda else Variable(context_candidates)

        if cfg.atten=='soft-general':
            #global general attention as https://nlp.stanford.edu/pubs/emnlp15_attn.pdf
            states_mapped = torch.mm(H.view(-1, cfg.h_units), self.atten_W).view(-1, cfg.max_length, cfg.h_units)

        beam = []
        for i in range(cfg.max_length):
            Hi = H[:,i,:]
            if i==0:
                context = h0
                input = torch.cat((Go_symbol, context), dim=1)
                output, temp_c = self.dec_rnn(input, (h0, c0))

                if cfg.atten=='hard-monotonic':
                    temp_context = Hi
                    output_context = torch.cat((output, temp_context), dim=1)
                    score = self.affine(output_context)

                elif cfg.atten=='soft-general':
                    atten_scores = torch.sum(states_mapped * output.view(-1, 1, cfg.h_units).expand(-1, cfg.max_length, cfg.h_units), dim=2)
                    atten = nn.functional.softmax(atten_scores, dim=1)
                    temp_context = torch.sum(atten.view(-1, cfg.max_length, 1).expand(-1, cfg.max_length, cfg.h_units) * H, dim=1)
                    score = self.affine(nn.functional.tanh(self.atten_affine(torch.cat((output, temp_context), dim=1))))

                log_prob = nn.functional.log_softmax(score, dim=1)
                log_prob.data[:, cfg.trg_pad_id] = V_Neg.data #never select pad
                kprob, kidx = torch.topk(log_prob, beamsize, dim=1, largest=True, sorted=True)

                #For the time step > 1
                h = torch.stack([output] * beamsize, dim=1)
                c = torch.stack([temp_c] * beamsize, dim=1)
                context = torch.stack([temp_context] * beamsize, dim=1)
                prev_y = kidx
                prev_lprob = kprob

            else:
                isEnd = torch.eq(prev_y, cfg.trg_end_id).long()
                isEnd_f = isEnd.float()
                isPad = torch.eq(prev_y, cfg.trg_pad_id).long()
                isPad_f = isPad.float()
                prev_output = self.trg_em(prev_y)
                for b in range(beamsize):
                    input = torch.cat((prev_output[:,b,:], context[:,b,:]), dim=1)
                    output, temp_c = self.dec_rnn(input, (h[:,b,:], c[:,b,:]))

                    if cfg.atten=='hard-monotonic':
                        temp_context = Hi
                        output_context = torch.cat((output, temp_context), dim=1)
                        score = self.affine(output_context)

                    elif cfg.atten=='soft-general':
                        atten_scores = torch.sum(states_mapped * output.view(-1, 1, cfg.h_units).expand(-1, cfg.max_length, cfg.h_units), dim=2)
                        atten = nn.functional.softmax(atten_scores, dim=1)
                        temp_context = torch.sum(atten.view(-1, cfg.max_length, 1).expand(-1, cfg.max_length, cfg.h_units) * H, dim=1)
                        score = self.affine(nn.functional.tanh(self.atten_affine(torch.cat((output, temp_context), dim=1))))

                    log_prob = nn.functional.log_softmax(score, dim=1)
                    log_prob.data[:, cfg.trg_pad_id] = V_Neg.data #never select pad
                    kprob, kidx = torch.topk(log_prob, beamsize, dim=1, largest=True, sorted=True)
                    h_c[:,b,:] = output
                    c_c[:,b,:] = temp_c
                    context_c[:,b,:] = temp_context

                    for bb in range(beamsize):
                        isEnd_c[:,beamsize*b + bb] = isEnd_f[:,b] + isPad_f[:,b]
                        new_lprob = prev_lprob[:,b] + (1.0 - isEnd_c[:,beamsize*b + bb]) * kprob[:,bb]
                        normalized_new_lprob = torch.div(new_lprob, i+1)
                        final_new_lprob = isEnd_f[:,b] * normalized_new_lprob + (1.0 - isEnd_f[:,b]) * new_lprob
                        lprob_c[:,beamsize*b + bb] = final_new_lprob
                        y_c[:,beamsize*b + bb] = (1.0 - isEnd_c[:,beamsize*b + bb]) * kidx[:,bb] + isEnd_c[:,beamsize*b + bb] * Pads

                    for bb in range(1, beamsize):
                        lprob_c[:,beamsize*b + bb] = lprob_c[:,beamsize*b + bb] + isEnd_c[:,beamsize*b + bb] * V_Neg

                formalized_lprob_c = torch.div(lprob_c, i+1)
                _, maxidx = torch.topk(isEnd_c * lprob_c + (1.0-isEnd_c) * formalized_lprob_c, beamsize, dim=1, largest=True, sorted=True)

                y = torch.gather(y_c, 1, maxidx)
                which_parent_ids = torch.div(maxidx, beamsize)
                parent_y = torch.gather(prev_y, 1, which_parent_ids)
                beam.append(parent_y)

                #For next step
                prev_y = y
                prev_lprob = torch.gather(lprob_c, 1, maxidx)
                h = torch.gather(h_c, 1, which_parent_ids.view(-1, beamsize, 1).expand(-1, beamsize, cfg.h_units))
                c = torch.gather(c_c, 1, which_parent_ids.view(-1, beamsize, 1).expand(-1, beamsize, cfg.h_units))
                context = torch.gather(context_c, 1, which_parent_ids.view(-1, beamsize, 1).expand(-1, beamsize, cfg.h_units))

        beam.append(prev_y)
        preds = torch.stack(beam, dim=2)
        #!!Returning individual log probs for each time step is not implemented.!!
        #instead we return the prev_lprob which has the overall score for each output of the beam.
        confidence = prev_lprob
        #confidence is of size (batch size, beam size)
        #preds is of size (batch size, beam size, max length)
        return preds, confidence
