"""
@author: Bengt Ljungquist
"""
import numpy as np
cimport numpy as np
import scipy.sparse as scs


cpdef bit_encode(np.ndarray spike_times, np.ndarray neuron_ids,
                 int n_neurons, int win_size):              
    """ Creates bitencoded grid from spike times
        and neuron IDs
    
    Args:    
        spike_times: numpy array 1 x n, must be from onset of window in ms 
        neuron_ids: numpy array 1 x n, ids of neurons of the spike times
        n_neurons:  total number of neurons
        win_size: the window size used for the encoded sample
    
    Returns:
        A numpy array of bitencoded data of size n_neurons/32 x win_size
    """
    spike_times = spike_times.flatten()
    neuron_ids = neuron_ids.flatten()
    n_spikes = spike_times.size
    
    # Create a vector of spikes of same size as spike_times vector
    spikes = np.ones((1, n_spikes), np.uint8).flatten()
    int_sp_times = spike_times.astype(np.uint8).flatten()
    # Use vectors to create sparse matrix
    print("Creating matrix")
    print(spikes) 
    spike_mat = scs.csc_matrix((spikes, (neuron_ids, int_sp_times)),
                               shape=(n_neurons, win_size), 
                               dtype=np.int8).toarray()
    spike_mat=spike_mat.astype(np.bool).astype(np.int)  
    # Pad with zeros to get a number of rows
    # divisable by 32
    print("Starting to pad")
    x_neurons = n_neurons % 32
    if x_neurons != 0:
        to_pad = 32-x_neurons
        spike_mat = np.lib.pad(spike_mat, ((0,to_pad),(0,0)), "constant", 
                               constant_values=0)    
    # Calculated number of 32-bit integers nneded
    n_ints = spike_mat.shape[0] // 32
      
    # Reshape matrix to a "bit shape" to prepare for multiplication
    spike_mat=np.reshape(spike_mat.transpose(), (win_size, n_ints,32))

    # create bitvector (1,2,4, ... ,2**31)
    bit32 = 2 ** np.arange(32)
    
    # multiply matrices (spike_mat X bit32) to get bit encoding 
    bit_encoded_data = spike_mat.dot(np.transpose(bit32)).transpose()
    return bit_encoded_data
    
    