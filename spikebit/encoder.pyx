"""
Created on Sun Jul  2 19:02:44 2017

@author: bengt
"""
import numpy as np
cimport numpy as np
import scipy.sparse as scs


cpdef bit_encode(np.ndarray spike_times, np.ndarray neuron_ids,
           int n_neurons, int win_size):              
    """
    Creates bitencoded grid
    
    Args:    
        spike_times: numpy array 1 x n, must be from onset of window in ms 
        neuron_ids: numpy array 1 x n, ids of neurons of the spike times
        n_neurons:  total number of neurons   
    
    Returns:
        A numpy array of bitencoded data of size win_size x n_neurons/32
    """
    nspikes = len(spike_times)
    
    # Create a vector of spikes of same 
    # size as spike_times vector
    spikes = np.ones((1, nspikes), np.uint8).flatten()
    int_sp_times = (spike_times).astype(np.uint8)
    # Use vectors to create sparse matrix
    spike_mat = scs.csc_matrix((spikes, (neuron_ids, int_sp_times)),
                                  shape=(n_neurons, win_size), 
                                dtype=np.int8).toarray()
    spike_mat=spike_mat.astype(np.bool).astype(np.int)
                                 
    # Pad with zeros to get a number of rows
    # divisable by 32
    to_pad = n_neurons % 32
    if to_pad != 0:
        padding = 32-to_pad
        spike_mat = np.lib.pad(spike_mat, ((0,to_pad),(0,0)), "constant", 
                              constant_values=0)    
    # Calculated number of 32-bit integers nneded
    n_ints = spike_mat.shape[0] // 32
    if to_pad > 0:
    #Increase number of integers with 1
        n_ints += 1
      
    # Reshape matrix to n_ints x win_size x 32
    spike_mat=np.reshape(spike_mat, (n_ints, win_size, 32))
    # create bitvector (1,2,4, ... ,2**31)
    bit32 = 2**np.arange(32)
    # multiply matrices (spike_mat X bit32) to get bit encoding 
    bit_encoded_data = spike_mat.dot(np.transpose(bit32))
    return bit_encoded_data
    
    