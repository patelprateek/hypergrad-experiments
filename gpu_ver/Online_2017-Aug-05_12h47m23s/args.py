import argparse
import numpy as np


def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        type=bool, default=True)
    parser.add_argument('-m', '--model',
                        type=str, choices=['mlp', 'convnet'], default='convnet')
    parser.add_argument('-d', '--dataset',
                        choices=['mnist', 'cifar10'], default='cifar10')
    parser.add_argument('-r', '--ratioValid', help='the ratio of valid set to train set',
                        type=float, default=0.2) #unused arg
    parser.add_argument('--bn', help='use BatchNorm or not',
                        type=bool, default=True) #batch normalization is definitely used
    parser.add_argument('--predata', help='to load from preprocess data or not',
                        type=bool, default=False)
    parser.add_argument('--regL1', help='tune L1 reg or not',
                        type=bool, default=False)
    parser.add_argument('--regL2', help='tune L2 reg or not',
                        type=bool, default=True)
    parser.add_argument('--initScale', help='tune initial scale or not',
                        type=bool, default=False) #not being used; ScaleLayers on log scale should be fast enough?
    parser.add_argument('--ratioHyper', help='ratio of Hyper Set',
                        type=int, default=0.2) #unused arg
    parser.add_argument('--validHyper', help='ratio of Valid Set',
                        type=int, default=0.0) #unused arg
    parser.add_argument('--meta_bw', help='use meta backward or not',
                        type=bool, default=True) #unused arg
    parser.add_argument('--maxEpochInit',
                        type=int, default=300) #100 previously; 10 if you don't have confidence in your initial guess
                        #don't start too small, since otherwise hypergradients may systematically lead to less regularization
    parser.add_argument('--maxEpochMult',
                        type=float, default=1.4) #1.4 previously; 2 to go with maxEpochInit=10
    parser.add_argument('--maxMaxEpoch',
                        type=int, default=300) #TODO: 300 from DenseNet on CIFAR10
    #first do maxEpochInit epochs, then 1.2*maxEpochInit epochs, then 1.2^2 * maxEpochInit, and so on
    #until maxMaxEpoch is reached, after which the number of epochs is constant at that value
    parser.add_argument('--batchSizeEle',
                        type=int, default=64) #use power of 2
    parser.add_argument('--batchSizeHyper',
                        type=int, default=64) #use power of 2
    parser.add_argument('--metaEpoch',
                        type=int, default=80) #meta-iter
    parser.add_argument('--lrHyper',
                        type=float, default=0.01) 
                        # TODO: 0.3333 for DrMAD, 0.0005 for online 5-5, 0.01 for online 120-5
                        #fixed hyper learning rate
                        # base-10 log-scale hypers can increase or decrease by at most a factor of 10^0.333~2.154 this way
                        # and a full order of magnitude in three steps (0.3333~1/3)
                        # when the partial derivative *consistently* points in the same direction
                        # but momentum will slow it down otherwise
    parser.add_argument('--lrEle',
                        type=float, default=0.1) # from DenseNet; 
                        #in DenseNet, decrease by factor of 10 after 30 epochs and again after 60 epochs
                        #only the initial value for online/adaptive version
    parser.add_argument('--momHyper',
                        type=float, default=0.7) #TODO: 0.7 for DrMAD, 0.95 for online
    parser.add_argument('--momEle',
                        type=float, default=0.9) #TODO: 0.9 from DenseNet, for DrMAD
    parser.add_argument('--lrLlr',
                        type=float, default=0.2) #learning rate for (natural) log learning rate
                        #TODO: 0.001 for online with 5-5, 0.1 for online 120-5
                        #Maybe try 0.5 for online 120-5? If large enough, it could be like cyclical learning rates
                        # 1. lead to nan on a small NN; some llrs decreased to ~e^-8
    parser.add_argument('--momLlr',
                        type=float, default=0.) #momentum for log learning rate
                        #TODO: 0.7 for 5-5 per update
    parser.add_argument('--eleAlg',
                        type=str, choices=['SGDm', 'SGDNesterov'], default='SGDm') #TODO: Nesterov in DenseNet
                        #Only SGDm for the online version currently
    parser.add_argument('--nBackwardMult',
                        type=float, default=1.) #TODO: multiplies number of reverse iterations
    parser.add_argument('--onlineItersPerUpdate',
                        type=int, default=100) #TODO:
    parser.add_argument('--nReversedIters',
                        type=int, default=5) #TODO: only compute hypergradient based on the last 5
                        
    
    #TODO: DenseNet
    parser.add_argument('--classes',
                        type=int, default=10)
    parser.add_argument('--depth',
                        type=int, default=40) #TODO: 40 "depth must be num_blocks * n + 1 for some n"
    parser.add_argument('--first_output',
                        type=int, default=16) #TODO: 16
    parser.add_argument('--growth_rate',
                        type=int, default=12)
    parser.add_argument('--num_blocks',
                        type=int, default=3)
    parser.add_argument('--dropout',
                        type=float, default=0.2) #TODO: 
    
    args = parser.parse_args()

    #TODO: these are ignored
    args.processedDataName = args.dataset + '_processed.npz'
    args.preProcess = 'None' #'global_contrast_norm'
    args.preContrast = 'None'
    
    args.seed = 1235 #TODO:
    args.evaluateTestInterval = 1 #unused
    args.MLPlayer = [300, 300, 300, 10] #unused

    args.regInit = { #regularization on logarithmic scale
        #'L1': 0,
        #'L2': 0.02,
        'L1': np.log10(0.001), 
        'L2': -4., #-4. from Lasagne Densenet implementation #TODO: try -3. and -6.
    }
    return args
