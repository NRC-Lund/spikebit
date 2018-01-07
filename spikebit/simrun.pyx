"""
@author: Bengt Ljungquist
"""
import spikebit.sbcomm
cimport numpy as np
import numpy as np
import spikebit.encoder as spenc
import time

cpdef randspikes(int n_ch, int win_sz, int method):
    """Create Random spikes or all neurons spiking
    
    args:
        n_ch: number of channels (32 neurons in bits) as rows
        win_sz: the window size as the columns
        method: the method to use; 2 use bit encoding, 1 all is spiking, 0 random
    returns:
        the generated numpy array according to the method       
    """
    if method==2:
        n_neurons = n_ch * 32
        train_length = n_neurons * win_sz // 16 # spike every 16th bin in mean
        spike_times = np.random.randint(0, win_sz, size=(1,train_length), dtype=np.uint32)
        neuron_ids = np.random.randint(0, n_neurons, size=(1,train_length), dtype=np.uint32)
        the_data=spenc.bit_encode(spike_times, neuron_ids, n_neurons, win_sz)

    else:
        the_data=np.random.randint(0,2**32-1,[n_ch,win_sz],dtype=np.dtype('uint32'))
        if method==1:
            the_data[:,0]=2**32-1 # all neurons are spiking
    return the_data

cpdef runsim(int n_ch, int sim_sz, int win_sz, int fs, str host, int port, bint encode):
    """ runs a simulation client according to parameters
    
    args:
        n_ch: number of channels (32 neurons in bits) as rows
        sim_sz: the number of channels 
        win_sz: the window size as the columns
        fs: the sampling frequency
        host: the Spikebit server to connect to
        port: the port at the server to connect to
    """
    sbc=spikebit.sbcomm.Client(n_ch, win_sz)
    sbc.connect(host, port)
    
    alt_data=randspikes(n_ch, win_sz, 1)
    the_data=randspikes(n_ch, win_sz, 0)
    cdef double comp_time = win_sz/fs
    t_times=[] 

    for i in range(0,sim_sz):
        t1=time.time()
        if i % 40==21:
            sbc.send_data(alt_data)
        else:
            if encode:
                sbc.send_data(randspikes(n_ch, win_sz, 2))
            else:    
                sbc.send_data(the_data)
        t2=time.time()
        time_pass=t2-t1
        t_times=np.append(t_times,time_pass)
        timeRem=comp_time-time_pass
    sbc.disconnect()
