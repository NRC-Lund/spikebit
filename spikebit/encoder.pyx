"""
Created on Sun Jul  2 19:02:44 2017

@author: bengt
"""
import numpy as np
import scipy.sparse as scs


def bitEncode(np.ndarray spikeTimes, np.ndarray neuronIds, int firstTime,
           int nNeurons, int winSize):              
    """
    Takes arrays of spikeTimes (1xn must be from onset of window in ms)  and 
    neuronIDs (1xn)  as input and creates 
    bitencoded grid of size (n/32)
    """
    nSpikes = len(spikeTimes)
    
    # Create a vector of spikes of same 
    # size as spiketimes vector
    spikes = np.ones((1, arrSize), np.uint8).flatten()
    intSpTimes = spikeTimes.astype(np.uint8)
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
    bitArrSize = spikeMat.shape[0] // 32
    # TODO is this doing the right thing?
    atest=np.reshape(spikeMat,(bitArrSize,20,32))
    # Calculated number of 32-bit integers nneded
    nIntegers = spikeMat.shape[0] // 32
    if toPad > 0:
    #Increase number of integers with 1
    nIntegers += 1
      
    # Reshape matrix to nIntegers x 
    # winSize x 32
    spikeMat=np.reshape(spikeMat,(nIntegers,winSize,32))
    # create bitvector (1,2,4, ... ,2**31)
    bit32 = 2**np.arange(32)
    # multiply matrices (spikeMat X bit32) to get bit encoding 
    bitEncodedData = spikeMat.dot(np.transpose(bit32))
    return bitEncodedData
    
    
    # Create a vector of spikes of same 
    # size as spiketimes vector
    spikes = np.ones((1, spikeTimes.size), np.uint8)
    # Use vectors to create sparse matrix
    spikeMat = scs.csc_matrix((spikes, (neuronIds, intSpTimes)),
    shape=(self.nNeurons, 20)).toarray()
    # Pad with zeros to get a number of rows
    # divisable by 32
    toPad = self.nNeurons % 32 
    spikeMat = np.lib.pad(spikeMat,((0,toPad),(0,0)),
    "constant", constant_values=0)
  # Calculated number of 32-bit integers  
  nIntegers = spikeMat.shape[0] // 32
  if toPad > 0:
    #Increase number of integers with 1
    nIntegers += 1
  # Use window size of 20
  winSize=20
  # Reshape matrix to nIntegers x 
  # winSize x 32
  spikeMat=np.reshape(spikeMat,(nIntegers,
    winSize,32))

  
  
    arrSize = spikeTimes.size
    spikes = np.ones((1, arrSize), np.uint8).flatten()
    intSpTimes = (spikeTimes - firstTime).astype(np.uint8)
    spikeMat = scs.csc_matrix((spikes, (neuronIds, intSpTimes)),
                              shape=(nNeurons, winSize), dtype=np.int8).toarray()
    return spikeMat
    