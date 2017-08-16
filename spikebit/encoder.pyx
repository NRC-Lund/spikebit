"""
Created on Sun Jul  2 19:02:44 2017

@author: bengt
"""
import numpy as np
cimport numpy as np
import scipy.sparse as scs


def bitEncode(np.ndarray spikeTimes, np.ndarray neuronIds, int firstTime,
           int nNeurons, int winSize):              
    """
    Takes arrays of spikeTimes (1xn must be from onset of window in ms) 
    neuronIDs (1xn), number of neurons   as input and creates 
    bitencoded grid of size (n/32)
    """
    nSpikes = len(spikeTimes)
    
    # Create a vector of spikes of same 
    # size as spiketimes vector
    spikes = np.ones((1, nSpikes), np.uint8).flatten()
    intSpTimes = (spikeTimes).astype(np.uint8)
    # Use vectors to create sparse matrix
    spikeMat = scs.csc_matrix((spikes, (neuronIds, intSpTimes)),
                                  shape=(nNeurons, winSize), 
                                dtype=np.int8).toarray()
    spikeMat=spikeMat.astype(np.bool).astype(np.int)
                                 
    # Pad with zeros to get a number of rows
    # divisable by 32
    toPad = nNeurons % 32
    if toPad != 0:
        padding = 32-toPad
        spikeMat = np.lib.pad(spikeMat,((0,toPad),(0,0)), "constant", 
                              constant_values=0)    
    # TODO is this doing the right thing?
    # Calculated number of 32-bit integers nneded
    nIntegers = spikeMat.shape[0] // 32
    if toPad > 0:
    #Increase number of integers with 1
        nIntegers += 1
      
    # Reshape matrix to nIntegers x winSize x 32
    spikeMat=np.reshape(spikeMat,(nIntegers,winSize,32))
    # create bitvector (1,2,4, ... ,2**31)
    bit32 = 2**np.arange(32)
    # multiply matrices (spikeMat X bit32) to get bit encoding 
    bitEncodedData = spikeMat.dot(np.transpose(bit32))
    return bitEncodedData
    
    