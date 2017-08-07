"""
Created on Sun Jul  2 16:10:17 2017

@author: bengt
"""

import numpy as np
def randspikes(int nCh,int winSz,int method):
    """Create Random spikes or if method ==1, random noise"""
    D=np.random.randint(0,2**32-1,[nCh,winSz],dtype=np.dtype('uint32'))
    if method==1:
        D[:,0]=2**32-1 # all neurons are spiking
    return D