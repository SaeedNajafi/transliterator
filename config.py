class Configuration(object):
    """Model hyperparams and data information"""
    h_units = 256
    src_em_size = 128
    trg_em_size = 128
    dropout = 0.5
    learning_rate = 0.0005
    actor_step_size = 0.5
    max_gradient_norm = 5.
    max_epochs = 256
    max_length = 64
    early_stopping = 10
    batch_size = 64
    seed = 125

    """path to different files"""
    src_alphabet = './data/' + 'src.alphabet'
    trg_alphabet = './data/' + 'trg.alphabet'

    train_raw = './data/' + 'train.raw'
    train_ref = './data/' + 'train.ref'
    dev_raw = './data/' + 'dev.raw'
    dev_ref = './data/' + 'dev.ref'


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

    #For inference in decoder RNNs, we have greedy search or beam search.
    #Specify the beam size.
    search = 'greedy'
    #search = 'beam'
    #beamsize = 10
