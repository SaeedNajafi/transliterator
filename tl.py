from config import Configuration
from load import load_embeddings
from load import load_data
from modules.encoder import Encoder
from modules.mldecoder import MLDecoder
from modules.rltrain import RLTrain
from modules.crf import CRF
from random import shuffle
from itertools import ifilter
import torch
import torch.optim as optim
import numpy as np
import random
import re
import os
import sys
import time
import codecs

hasCuda = torch.cuda.is_available()

#Global variables for modules.
encoder = None
crf = None
mldecoder = None
rltrain = None

#Optimizers for modules.
e_opt = None
c_opt = None
m_opt = None
r_opt = None

def batch_to_tensors(cfg, in_B):
    o_B = {}
    o_B['x'] = torch.LongTensor(in_B['x'])
    o_B['x_len'] = torch.LongTensor(in_B['x_len'])
    o_B['x_mask'] = torch.LongTensor(in_B['x_mask'])

    if in_B['y'] is not None:
        o_B['y'] = torch.LongTensor(in_B['y'])
        o_B['y_len'] = torch.LongTensor(in_B['y_len'])
        o_B['y_mask'] = torch.LongTensor(in_B['y_mask'])
    else:
        o_B['y'] = None
        o_B['y_len'] = None
        o_B['y_mask'] = None

    if in_B['y'] is not None:
        y_one_hot = np.zeros((cfg.d_batch_size * cfg.max_length, cfg.trg_alphabet_size))
        y_one_hot[np.arange(cfg.d_batch_size * cfg.max_length), np.reshape(in_B['y'], (-1,))] = 1.0
        y_o_h = np.reshape(y_one_hot, (cfg.d_batch_size, cfg.max_length, cfg.trg_alphabet_size))
        o_B['y_one_hot'] = torch.FloatTensor(y_o_h)
    else:
        o_B['y_one_hot'] = None

    cfg.B = o_B
    return

def save_predictions(cfg, batch, preds, f):
    """Saves predictions to the provided file stream."""
    w_idx = 0
    for pred in preds:
        w = ''.join(batch['raw_x'][w_idx])
        end_idx = pred.index(cfg.trg_end_id)
        target = []
        for id in range(0, end_idx):
            target.append(cfg.data['trg_id_ch'][pred[id]])

        target_w = ''.join(target)
        to_write = w + '\t' + target_w + '\n'
        f.write(to_write.encode('utf-8'))
        w_idx += 1

    return

#Recursive Levenshtein Distance Function in Python
def LD(str1, str2):
    m = np.zeros([len(str2)+1, len(str1)+1])
    for x in xrange(1, len(str2) + 1):
        m[x][0] = m[x-1][0] + 1
    for y in xrange(1, len(str1) + 1):
        m[0][y] = m[0][y-1] + 1
    for x in xrange(1, len(str2) + 1):
        for y in xrange(1, len(str1) + 1):
            if str1[y-1] == str2[x-1]:
                dg = 0
            else:
                dg = 1
            m[x][y] = min(m[x-1][y] + 1, m[x][y-1] + 1, m[x-1][y-1] + dg)
    return int(m[len(str2)][len(str1)])

def avg_edit_distance(ref_file, pred_file):
    ref_lines = open(ref_file, 'r').readlines()
    pred_lines = open(pred_file, 'r').readlines()

    if len(ref_lines)!=len(pred_lines):
        print "INFO: Wrong number of lines in reference and prediction files"
        exit()

    dist = 0.0
    for index in range(len(ref_lines)):
        ref_line = ref_lines[index].strip()
        pred_line = pred_lines[index].strip()
        if len(ref_line)!=0 and len(pred_line)!=0:
            GYs = ref_line.split('\t')
            y = pred_line.split('\t')[1]
            cost = 0.0
            for gy in GYs:
                ref = list(gy.decode('utf8'))
                pred = list(y.decode('utf8'))
                cost += LD(ref, pred)

            dist = dist + cost/float(len(GYs))


        edit_distance = dist/float(index)
    return edit_distance

def accuracy(ref_file, pred_file):
    #Top1 Accuracy
    ref_lines = open(ref_file, 'r').readlines()
    pred_lines = open(pred_file, 'r').readlines()

    if len(ref_lines)!=len(pred_lines):
        print "INFO: Wrong number of lines in reference and prediction files"
        exit()

    total = 0.0
    correct = 0.0
    for index in range(len(ref_lines)):
        ref_line = ref_lines[index].strip()
        pred_line = pred_lines[index].strip()
        if len(ref_line)!=0 and len(pred_line)!=0:
            GYs = ref_line.split('\t')
            y = pred_line.split('\t')[1]
            total += 1
            for gy in GYs:
                if list(gy.decode('utf8'))==list(y.decode('utf8')):
                    correct += 1
                    break

    return float(correct/total) * 100

def evaluate(cfg, ref_file, pred_file):
    error =100 - accuracy(ref_file, pred_file)
    edit_distance = avg_edit_distance(ref_file, pred_file)
    return error/200.0 + edit_distance/0.5

def run_epoch(cfg):
    cfg.local_mode = 'train'

    total_loss = []
    if cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN':
        vtotal_loss = []

    #Turn on training mode which enables dropout.
    encoder.train()
    if cfg.model_type=='CRF': crf.train()
    else:
        mldecoder.train()
        if cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN':
            rltrain.train()

    batches = [batch for batch in load_data(cfg)]
    shuffle(batches)
    for step, batch in enumerate(batches):
        cfg.d_batch_size = batch['d_batch_size']
        e_opt.zero_grad()
        if cfg.model_type=='CRF':
            c_opt.zero_grad()
        elif cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN':
            r_opt.zero_grad()
            m_opt.zero_grad()
        else:
            m_opt.zero_grad()

        batch_to_tensors(cfg, batch)
        H = encoder()
        if cfg.model_type=='CRF':
            log_probs = crf(H)
            loss = crf.loss(log_probs)
        elif cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN':
            loss, vloss = rltrain(H, mldecoder)
        else:
            log_probs = mldecoder(H)
            loss = mldecoder.loss(log_probs)

        loss.backward()
        if cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN': vloss.backward()

        torch.nn.utils.clip_grad_norm(encoder.parameters(), cfg.max_gradient_norm)
        if cfg.model_type=='CRF': torch.nn.utils.clip_grad_norm(crf.parameters(), cfg.max_gradient_norm)
        elif cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN':
            torch.nn.utils.clip_grad_norm(mldecoder.parameters(), cfg.max_gradient_norm)
        else:
            torch.nn.utils.clip_grad_norm(mldecoder.parameters(), cfg.max_gradient_norm)

        e_opt.step()
        if cfg.model_type=='CRF':
            c_opt.step()
        elif cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN':
            r_opt.step()
            m_opt.step()
        else:
            m_opt.step()

        loss_value = loss.cpu().data.numpy()[0]
        total_loss.append(loss_value)
        if cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN':
            vloss_value = vloss.cpu().data.numpy()[0]
            vtotal_loss.append(vloss_value)
            ##
            sys.stdout.write('\rBatch:{} | Loss:{} | Mean Loss:{} | VLoss:{} | Mean VLoss:{}'.format(
                                                step,
                                                loss_value,
                                                np.mean(total_loss),
                                                vloss_value,
                                                np.mean(vtotal_loss)
                                                )
                            )
            sys.stdout.flush()
        else:
            ##
            sys.stdout.write('\rBatch:{} | Loss:{} | Mean Loss:{}'.format(
                                                step,
                                                loss_value,
                                                np.mean(total_loss)
                                                )
                            )
            sys.stdout.flush()
    return

def predict(cfg, o_file):
    if cfg.mode=='train':
        cfg.local_mode = 'dev'

    elif cfg.mode=='test':
        cfg.local_mode = 'test'

    #Turn on evaluation mode which disables dropout.
    encoder.eval()
    if cfg.model_type=='CRF': crf.eval()
    elif cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN':
        rltrain.eval()
        mldecoder.eval()
    else:
        mldecoder.eval()

    #file stream to save predictions
    f = open(o_file, 'w')
    for batch in load_data(cfg):
        cfg.d_batch_size = batch['d_batch_size']

        batch_to_tensors(cfg, batch)
        H = encoder()
        if cfg.model_type=='CRF':
            preds = crf.predict(H)
        else:
            if cfg.search=='greedy':
                preds = mldecoder.greedy(H)[0].cpu().data.numpy()
            elif cfg.search=='beam':
                preds = mldecoder.beam(H)[0][:,0,:].cpu().data.numpy()

        save_predictions(cfg, batch, preds, f)

    f.close()
    return

def run_model(mode, path, in_file, o_file):
    global encoder, crf, mldecoder, rltrain, e_opt, c_opt, m_opt, r_opt


    cfg = Configuration()

    #General mode has two values: 'train' or 'test'
    cfg.mode = mode

    #Set Random Seeds
    random.seed(cfg.seed)
    np.random.seed(cfg.seed)
    torch.manual_seed(cfg.seed)
    if hasCuda:
        torch.cuda.manual_seed_all(cfg.seed)

    #Load Embeddings
    load_embeddings(cfg)

    #Only for testing
    if mode=='test': cfg.test_raw = in_file

    #Construct models
    encoder = Encoder(cfg)
    if cfg.model_type=='AC-RNN' or cfg.model_type=='BR-RNN':
        e_opt = optim.SGD(ifilter(lambda p: p.requires_grad, encoder.parameters()), lr=cfg.actor_step_size)
    else:
        e_opt = optim.Adam(ifilter(lambda p: p.requires_grad, encoder.parameters()), lr=cfg.learning_rate)
    if hasCuda: encoder.cuda()

    if cfg.model_type=='CRF':
        crf = CRF(cfg)
        c_opt = optim.Adam(ifilter(lambda p: p.requires_grad, crf.parameters()), lr=cfg.learning_rate)
        if hasCuda: crf.cuda()

    elif cfg.model_type=='TF-RNN':
        mldecoder = MLDecoder(cfg)
        m_opt = optim.Adam(ifilter(lambda p: p.requires_grad, mldecoder.parameters()), lr=cfg.learning_rate)
        if hasCuda: mldecoder.cuda()
        cfg.mldecoder_type = 'TF'

    elif cfg.model_type=='SS-RNN':
        mldecoder = MLDecoder(cfg)
        m_opt = optim.Adam(ifilter(lambda p: p.requires_grad, mldecoder.parameters()), lr=cfg.learning_rate)
        if hasCuda: mldecoder.cuda()
        cfg.mldecoder_type = 'SS'

    elif cfg.model_type=='DS-RNN':
        mldecoder = MLDecoder(cfg)
        m_opt = optim.Adam(ifilter(lambda p: p.requires_grad, mldecoder.parameters()), lr=cfg.learning_rate)
        if hasCuda: mldecoder.cuda()
        cfg.mldecoder_type = 'DS'

    elif cfg.model_type=='BR-RNN':
        mldecoder = MLDecoder(cfg)
        m_opt = optim.SGD(ifilter(lambda p: p.requires_grad, mldecoder.parameters()), lr=cfg.actor_step_size)
        if hasCuda: mldecoder.cuda()
        cfg.mldecoder_type = 'TF'
        rltrain = RLTrain(cfg)
        r_opt = optim.Adam(ifilter(lambda p: p.requires_grad, rltrain.parameters()), lr=cfg.learning_rate)
        if hasCuda: rltrain.cuda()
        cfg.rltrain_type = 'BR'
        #For RL, the network should be pre-trained with teacher forced ML decoder.
        encoder.load_state_dict(torch.load(path + 'TF-RNN' + '_encoder'))
        mldecoder.load_state_dict(torch.load(path + 'TF-RNN' + '_predictor'))

    elif cfg.model_type=='AC-RNN':
        mldecoder = MLDecoder(cfg)
        m_opt = optim.SGD(ifilter(lambda p: p.requires_grad, mldecoder.parameters()), lr=cfg.actor_step_size)
        if hasCuda: mldecoder.cuda()
        cfg.mldecoder_type = 'TF'
        rltrain = RLTrain(cfg)
        r_opt = optim.Adam(ifilter(lambda p: p.requires_grad, rltrain.parameters()), lr=cfg.learning_rate)
        if hasCuda: rltrain.cuda()
        cfg.rltrain_type = 'AC'
        #For RL, the network should be pre-trained with teacher forced ML decoder.
        encoder.load_state_dict(torch.load(path + 'TF-RNN' + '_encoder'))
        mldecoder.load_state_dict(torch.load(path + 'TF-RNN' + '_predictor'))

    if mode=='train':
        o_file = './temp.predicted'
        best_val_cost = float('inf')
        best_val_epoch = 0
        first_start = time.time()
        epoch=0
        while (epoch < cfg.max_epochs):
            print
            print 'Model:{} | Epoch:{}'.format(cfg.model_type, epoch)

            if cfg.model_type=='SS-RNN' or cfg.model_type=='DS-RNN':
                #Specify the decaying schedule for sampling probability.
                #inverse sigmoid schedule:
                cfg.sampling_p = float(cfg.k)/float(cfg.k + np.exp(float(epoch)/cfg.k))

            if cfg.model_type=='DS-RNN':
                cfg.greedy_bias = np.minimum(10**8, (2)**epoch)

            start = time.time()
            run_epoch(cfg)
            print '\nValidation:'
            predict(cfg, o_file)
            val_cost = evaluate(cfg, cfg.dev_ref, o_file)
            print 'Validation score:{}'.format(1.000000000 - val_cost)
            if val_cost < best_val_cost:
                best_val_cost = val_cost
                best_val_epoch = epoch
                torch.save(encoder.state_dict(), path + cfg.model_type + '_encoder')
                if cfg.model_type=='CRF': torch.save(crf.state_dict(), path + cfg.model_type + '_predictor')
                elif cfg.model_type=='TF-RNN' or cfg.model_type=='SS-RNN' or cfg.model_type=='DS-RNN':
                    torch.save(mldecoder.state_dict(), path + cfg.model_type + '_predictor')
                elif cfg.model_type=='BR-RNN' or cfg.model_type=='AC-RNN':
                    torch.save(mldecoder.state_dict(), path + cfg.model_type + '_predictor')
                    torch.save(rltrain.state_dict(), path + cfg.model_type + '_critic')

            #For early stopping
            if epoch - best_val_epoch > cfg.early_stopping:
                break
                ###

            print 'Epoch training time:{} seconds'.format(time.time() - start)
            epoch += 1

        print 'Total training time:{} seconds'.format(time.time() - first_start)

    elif mode=='test':
        encoder.load_state_dict(torch.load(path + cfg.model_type + '_encoder'))
        if cfg.model_type=='CRF': crf.load_state_dict(torch.load(path + cfg.model_type + '_predictor'))
        elif cfg.model_type=='TF-RNN' or cfg.model_type=='SS-RNN' or cfg.model_type=='DS-RNN':
            mldecoder.load_state_dict(torch.load(path + cfg.model_type + '_predictor'))
        elif cfg.model_type=='BR-RNN' or cfg.model_type=='AC-RNN':
            mldecoder.load_state_dict(torch.load(path + cfg.model_type + '_predictor'))
            rltrain.load_state_dict(torch.load(path + cfg.model_type + '_critic'))

        print
        print 'Model:{} Predicting'.format(cfg.model_type)
        start = time.time()
        predict(cfg, o_file)
        print 'Total prediction time:{} seconds'.format(time.time() - start)
    return

"""
    For training: python tl.py train <path to save model>
    example: python tl.py train ./saved_models/

    For testing: python tl.py test <path to restore model> <input file path> <output file path>
    example: python tl.py test ./saved_models/ ./data/test.raw ./saved_models/test.predicted
    or: python tl.py test ./saved_models/ ./data/dev.raw ./saved_models/dev.predicted
"""
if __name__ == "__main__":
    mode = sys.argv[1]
    path = sys.argv[2]
    in_file = None
    o_file = None
    if mode=='test':
        in_file = sys.argv[3]
        o_file = sys.argv[4]

    run_model(mode, path, in_file, o_file)
