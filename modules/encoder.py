import torch
from torch.autograd import Variable
import torch.nn as nn
from torch.nn import init

hasCuda = torch.cuda.is_available()

class Encoder(nn.Module):
    """
    Applies a bi-direcitonl RNN
    on the input character vectors.
    It then uses a hidden/dense layer to
    build the final hidden vectors of each step.
    """
    def __init__(self, cfg):
        super(Encoder, self).__init__()

        self.cfg = cfg

        #Size of input character vectors
        in_size = cfg.src_em_size
        self.src_rnn = nn.LSTM(
                            input_size=in_size,
                            hidden_size=cfg.h_units,
                            num_layers=1,
                            bias=True,
                            batch_first=True,
                            dropout=0.0,
                            bidirectional=True
                            )

        self.dense = nn.Linear(
                            2 * cfg.h_units,
                            cfg.h_units,
                            bias=True
                            )

        self.drop = nn.Dropout(cfg.dropout)

        self.param_init()
        self.embeddings()
        return

    def param_init(self):
        for name, param in self.named_parameters():
            if 'bias' in name:
                init.constant(param, 0.0)
            if 'weight' in name:
                init.xavier_uniform(param)
        return


    def embeddings(self):
        """Add embedding layer that maps from ids to vectors."""
        cfg = self.cfg

        src_lt = torch.FloatTensor(cfg.data['src_vec']) #source lookup table
        self.src_em = nn.Embedding(cfg.src_alphabet_size, cfg.src_em_size)
        self.src_em.weight.data.copy_(src_lt)
        self.src_em.weight.data[cfg.src_pad_id].fill_(0.0)
        self.src_em.weight.requires_grad = True
        return

    def forward(self):

        cfg = self.cfg

        #zero the pad id vectors
        self.src_em.weight.data[cfg.src_pad_id].fill_(0.0)

        x_mask = Variable(cfg.B['x_mask'].cuda()) if hasCuda else Variable(cfg.B['x_mask'])

        #Tensor to Input Variables
        x = Variable(cfg.B['x'].cuda()) if hasCuda else Variable(cfg.B['x'])

        #Create a variable for initial hidden vector of RNNs.
        zeros = torch.zeros(2, cfg.d_batch_size, cfg.h_units)
        h0 = Variable(zeros.cuda()) if hasCuda else Variable(zeros)

        x_ems = self.src_em(x)

        #Bi-directional RNN
        outputs, _ = self.src_rnn(x_ems, (h0, h0))

        outputs_dr = self.drop(outputs)

        HH = self.dense(outputs_dr)

        #tanh non-linear layer.
        H = nn.functional.tanh(HH)

        #H is the final matrix having final hidden vectors of steps.
        return H * x_mask.view(-1, cfg.max_length, 1).expand(-1, cfg.max_length, cfg.h_units)
