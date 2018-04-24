class Configuration(object):
    """Model hyperparams and data information"""
    h_units = 256
    src_em_size = 128
    trg_em_size = 128
    dropout = 0.5
    learning_rate = 0.0005
    actor_step_size = 0.5
    max_gradient_norm = 15.
    max_epochs = 256
    max_length = 64
    early_stopping = 10
    batch_size = 64
    seed = 125

    """path to different files"""
    src_alphabet = './data/news2015/news2015/' + 'SplitsNEWS15/EnJa/src.alphabet'
    trg_alphabet = './data/news2015/news2015/' + 'SplitsNEWS15/EnJa/trg.alphabet'

    train_raw = './data/news2015/news2015/' + 'SplitsNEWS15/EnJa/enja.0-7.tst.src'
    train_ref = 'data/news2015/news2015/' + 'SplitsNEWS15/EnJa/enja.0-7.tst.trg'
    dev_raw = 'data/news2015/news2015/' + 'SplitsNEWS15/EnJa/enja.tune.src'
    dev_ref_xml = 'data/news2015/news2015/' + 'SplitsNEWS15/EnJa/enja.tune.xml'

    """ Model Type """
    #Conditional Random Field
    #model_type = 'CRF'

    #Decoder RNN trained only with teacher forcing
    model_type = 'TF-RNN'

    #Decoder RNN trained with scheduled sampling.
    #model_type = 'SS-RNN'

    #Decoder RNN trained with differential scheduled sampling.
    #model_type = 'DS-RNN'

    #Also specify k for decaying the sampling probability in inverse sigmoid schedule.
    #Only for 'SS-RNN' and 'DS-RNN'
    #k=25

    #Decoder RNN trained using REINFORCE with baseline.
    #model_type = 'BR-RNN'

    #Decoder RNN trained with Actor-Critic.
    #model_type = 'AC-RNN'

    #For RL, you need to specify gamma and n-step.
    #gamma = 0.9
    #n_step = 4

    #Attention type for decoder RNNs
    #atten = 'hard-monotonic'
    atten = 'soft-general'

    #nbest results
    nbest = 10
