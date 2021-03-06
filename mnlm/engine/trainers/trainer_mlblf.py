# Trainer module for MLBLF model

import numpy as np
import gnumpy as gpu
import copy
from lm import mlblf
from utils import lm_tools
from numpy.random import RandomState


def trainer(z, split=3500, pre_train=True):
    """
    Trainer function for a MLBLF model
    """
    # Unpack some stuff
    ngrams = z['ngrams']
    labels = z['labels']
    instances = z['instances']
    word_dict = z['word_dict']
    index_dict = z['index_dict']
    context = z['context']
    vocabsize = len(z['word_dict'])
    im = z['IM']
    index = z['index']

    # Load word embeddings
    if pre_train:
        embed_map = lm_tools.load_embeddings()
    else:
        embed_map = None

    # Initialize the network
    net = mlblf.MLBLF(name='mlblf',
                      loc='models/mlblf.pkl',         # where to store the model file
                      seed=1234,                              # used to initializing the model parameters
                      criteria='validation_pp',        # the stopping criteria
                      k=5,                                           # the window size used for validation
                      V=vocabsize,                           # the size of the vocabulary
                      K=50,                                        # the dim of the word representations
                      D=im.shape[1],                       # the dim of the images features
                      h=256,                                      # dim of an intermediate layer on the image channel
                      factors=50,                              # number of factors
                      context=context,
                      batchsize=20,
                      maxepoch=100,
                      eta_t=0.02,
                      gamma_r=1e-4,
                      gamma_c=1e-5,
                      f=0.998,
                      p_i=0.5,
                      p_f=0.9,
                      T=20.0,
                      verbose=1)

    # Break up the data for training and validation
    inds = np.arange(len(ngrams))
    prng = RandomState(net.seed)
    prng.shuffle(inds)

    ngramsV = [ngrams[i] for i in inds[-split:]]
    flat_ngramsV = [item for sublist in ngramsV for item in sublist]
    instance_split = len(flat_ngramsV)

    inds = np.arange(len(instances))
    prng = RandomState(net.seed)
    prng.shuffle(inds)

    X = instances[inds[:-instance_split]]
    V = instances[inds[-instance_split:]]
    Y = labels[inds[:-instance_split]]
    VY = labels[inds[-instance_split:]]
    indX = index[inds[:-instance_split]]
    indV = index[inds[-instance_split:]]

    # Train the network
    net.train(X, indX, Y, V, indV, VY, im, index_dict, word_dict, embed_map)

