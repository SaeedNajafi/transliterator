import itertools
import re
import numpy as np

def load_embeddings(cfg):
    #This is where we will keep embeddings data.
    cfg.data = {}

    #Defining some constants.
    cfg.end = 'ENDENDEND'
    cg.pad = 'PADPADPAD'
    cfg.unk = 'UNKUNKUNK'

    #Creates random vectors for source and target characters.
    f = open(cfg.src_alphabet, 'r')
    src_chars = [line.strip().decode('utf-8') for line in f.readlines()]
    src_chars.append(cfg.unk)
    src_chars.append(cfg.end)
    src_chars.append(cfg.pad)
    cfg.src_alphabet_size = len(src_chars)
    f.close()

    f = open(cfg.trg_alphabet, 'r')
    trg_chars = [line.strip().decode('utf-8') for line in f.readlines()]
    trg_chars.append(cfg.unk)
    trg_chars.append(cfg.end)
    trg_chars.append(cfg.pad)
    cfg.trg_alphabet_size = len(trg_chars)
    f.close()

    src_id_to_char = dict(enumerate(src_chars))
    src_char_to_id = {v:k for k,v in src_id_to_char.iteritems()}

    trg_id_to_char = dict(enumerate(trg_chars))
    trg_char_to_id = {v:k for k,v in trg_id_to_char.iteritems()}

    ep = np.sqrt(np.divide(6.0, cfg.src_em_size))
    src_vectors = np.random.uniform(
                                    low=-ep,
                                    high=ep,
                                    size=(cfg.src_alphabet_size, cfg.src_em_size)
                                    )

    ep = np.sqrt(np.divide(6.0, cfg.trg_em_size))
    trg_vectors = np.random.uniform(
                                    low=-ep,
                                    high=ep,
                                    size=(cfg.trg_alphabet_size, cfg.trg_em_size)
                                    )

    cfg.data['src_vec'] = src_vectors
    cfg.data['trg_vec'] = trg_vectors
    cfg.data['src_id_ch'] = src_id_to_char
    cfg.data['src_ch_id'] = src_char_to_id
    cfg.data['trg_id_ch'] = trg_id_to_char
    cfg.data['trg_ch_id'] = trg_char_to_id

    cfg.src_unk_id = cfg.data['src_ch_id'][cfg.unk]
    cfg.src_pad_id = cfg.data['src_ch_id'][cfg.pad]
    cfg.src_end_id = cfg.data['src_ch_id'][cfg.end]

    cfg.trg_unk_id = cfg.data['trg_ch_id'][cfg.unk]
    cfg.trg_pad_id = cfg.data['trg_ch_id'][cfg.pad]
    cfg.trg_end_id = cfg.data['trg_ch_id'][cfg.end]

    return

def map_chars_to_ids(cfg, word, src_or_trg):
    if src_or_trg='src':
        ch_id = cfg.data['src_ch_id']

    elif src_or_trg='trg':
        ch_id = cfg.data['trg_ch_id']

    lst = []
    for ch in list(word):
        if ch in ch_id:
            lst.append(ch_id[ch])
        else:
            lst.append(ch_id[cfg.unk])
            print "INFO: Could not find the following char and replaced it with the unk char: ", ch

    #add end symbol
    return lst.append(ch_id[cfg.end])

def load_data(cfg):
    """ Loads train, dev or test data. """

    #static batch size
    sb_size = cfg.batch_size

    #local_mode can have three values 'train', 'dev' and 'test'.
    mode = cfg.local_mode

    if mode == 'train':
        f_raw = cfg.train_raw
        f_ref = cfg.train_ref
        hasY = True

    elif mode == 'dev':
        f_raw = cfg.dev_raw
        f_ref = cfg.dev_ref
        hasY = True

    elif mode == 'test':
        f_raw = cfg.test_raw
        f_ref = None
        hasY = False


    batch = []
    fd_raw = open(f_raw, 'r')
    if hasY: fd_ref = open(f_ref, 'r')

    x_line = None
    y_line = None
    for x_line in fd_raw:
        x_line = x_line.strip()
        #we assume ref and raw files have the same number of lines.
        if hasY: y_line = fd_ref.readline().strip()

        if len(x_line)==0: continue

        batch.append((x_line, y_line))
        if len(batch)==sb_size:
            yield process_batch(cfg, batch)
            batch = []

    fd_raw.close()
    if hasY: fd_ref.close()

    #flush running buffer
    if len(batch)!=0:
        yield process_batch(cfg, batch)

def process_batch(cfg, batch):
    mode = cfg.local_mode

    hasY = True
    if mode=='test': hasY = False

    Raw_X = []
    X = []
    X_Len = []
    X_Mask = []

    Raw_Y = []
    Y = []
    Y_Len = []
    Y_Mask = []

    for (in_W, out_W) in batch:

        #in_W is one word.
        Raw_X.append(in_W)
        X_chars = map_chars_to_ids(cfg, in_W, 'src')
        X.append(X_chars)
        X_Len.append(len(X_chars))

        if hasY:
            #out_W is one word.
            Raw_Y.append(out_W)
            Y_chars = map_chars_to_ids(cfg, out_W, 'trg')
            Y.append(Y_chars)
            Y_Len.append(len(Y_chars))

    #Set dynamic batch size
    d_batch_size = len(X_Len)

    #Creating mask for char sequences
    X_Mask = []
    for each in X_Len:
        lst = [1.0] * each
        X_Mask.append(lst)

    if hasY:
        Y_Mask = []
        for each in Y_Len:
            lst = [1.0] * each
            Y_Mask.append(lst)

    #The processed batch is now a dictionary.
    B = {
        'raw_x': Raw_X,
        'x': X,
        'x_len': X_Len,
        'x_mask': X_Mask,
        'd_batch_size': d_batch_size
        }

    if hasY:
        B['raw_y'] = Raw_Y
        B['y'] = Y
        B['y_len'] = Y_Len
        B['y_mask'] = Y_Mask

    else:
        B['raw_y'] = None
        B['y'] = None
        B['y_len'] = None
        B['y_mask'] = None

    pad(cfg, B)

    return B

def pad(cfg, B):
    #Pad x with src_pad_id
    for word in B['x']:
        pad_lst = [cfg.src_pad_id] * (cfg.max_length-len(word))
        word.extend(pad_lst)

    #Pad x_mask with 0.0
    for word in B['x_mask']:
        pad_lst = [0.0] * (cfg.max_length-len(word))
        word.extend(pad_lst)

    if B['y'] is not None:
        #Pad y with trg_pad_id
        for word in B['y']:
            pad_lst = [cfg.trg_pad_id] * (cfg.max_length-len(word))
            word.extend(pad_lst)

        #Pad y_mask with 0.0
        for word in B['y_mask']:
            pad_lst = [0.0] * (cfg.max_length-len(word))
            word.extend(pad_lst)
    return
