"""
Created on Tue Jun 27 00:27:35 2017

@author: bengt
"""

import spikebit.sbcomm
import numpy as np
import time


class spikeclient(object):
    """
    A client Mediator superclass for forwarding acquisition system data to 
    Spikebit Server. 
    
    """
    
    def __init__(self,  acqhost,  spikebithost):
        self.acqhost = acqhost
        self.acqisconnected = False
        self.spikebithost = spikebithost
        self.nch=128
        self.bufSz=20

    def acqconnect(self):
        """
        Connect to the specific acquisition system using its API to define 
        callback
        """
        self.acqisconnected = True
        
    def acqreceive(self, D):
        """
        Should implement the callback method from the acquisition system
        alternatively polling from main thread 
        """
        
        pass
    
    def spikebitconnect(self):
        self.sbc=sbcomm.Client(self.nCh,self.bufSz)
        self.sbc.connect(self.sbikebithost,port)

   # cpdef main(self, **kwargs):
    #    self.acqconnect()
     #   pass


class simclient(spikeclient):
    """
    Client which does not have a real aquisition system
    """
    def __init__(self, acqhost,  spikebithost):
        super.__init__(acqhost, spikebithost)


    def acqconnect(self):
        
        super.acqconnect()
    
    def acqreceive(self, D):
        pass
        

    

    def main(self, nCh, simSz, bufSz, fs, port):
        simrun.runsim(nCh, simSz, bufSz, fs, port)