# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:47:59 2017

@author: bengt
"""
import sbcomm
cimport numpy as np
import time

cpdef randspikes(int nCh,int winSz,int method):
    """Create Random spikes or if method ==1, random noise"""
    D=np.random.randint(0,2**32-1,[nCh,winSz],dtype=np.dtype('uint32'))
    if method==1:
        D[:,0]=2**32-1 # all neurons are spiking
    return D 

cpdef runsim(int nCh,int simSz,int bufSz,int fs,str host,int port):
    sbc=sbcomm.Client(nCh,bufSz)
    sbc.connect(host,port)
    
    altData=randspikes(nCh,bufSz,1)
    theData=randspikes(nCh,bufSz,0)
    cdef double compTime=bufSz/fs
    tTimes=[] 

    for i in range(0,simSz):
        t1=time.time()
        if i%40==21:
            #print altData
            sbc.sendData(altData)
            # HOST = ''                
            # PORT = 50007              
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.bind((HOST, PORT))
            # s.listen(1)
            # print "listening on {}".format(PORT)
            # conn, addr = s.accept()
            # while 1:
            #     data = conn.recv(1024)
            #     if not data: break
            # conn.close()
            # print "Recieved confirmation"
        else:
            #print theData.dtype
            sbc.sendData(theData)
        t2=time.time()
        timePass=t2-t1
        tTimes=np.append(tTimes,timePass)
        timeRem=compTime-timePass
        #print "compTime: {}, timePass: {}".format(compTime,timePass)
        #if timeRem<0:
        #    print "Warning{}".format(timeRem)
#        else:
#            busy_wait(timeRem)
    sbc.disconnect()
    theMean=np.mean(tTimes)
