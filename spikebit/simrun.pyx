# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:47:59 2017

@author: bengt
"""
import spikebit.sbcomm
cimport numpy as np
import numpy as np
import time

cpdef randspikes(int nCh,int winSz,int method):
    """randspikes(nCh, winSz, method) - Create Random spikes or if method ==1,
    random noise"""
    D=np.random.randint(0,2**32-1,[nCh,winSz],dtype=np.dtype('uint32'))
    if method==1:
        D[:,0]=2**32-1 # all neurons are spiking
    return D 

cpdef runsim(int nCh,int simSz,int bufSz,int fs,str host,int port):
    """runsim(nCh, simSz, bufSz, fs, host, port) - runs a simulation
    """
    sbc=spikebit.sbcomm.Client(nCh,bufSz)
    sbc.connect(host,port)
    
    altData=randspikes(nCh,bufSz,1)
    theData=randspikes(nCh,bufSz,0)
    cdef double compTime=bufSz/fs
    tTimes=[] 

    for i in range(0,simSz):
        t1=time.time()
        if i%40==21:
            sbc.sendData(altData)

        else:
            sbc.sendData(theData)
        t2=time.time()
        timePass=t2-t1
        tTimes=np.append(tTimes,timePass)
        timeRem=compTime-timePass
    sbc.disconnect()
