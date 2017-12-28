"""
Created on Tue Jun 27 00:27:35 2017

@author: bengt
"""

import spikebit.sbcomm
import spikebit.simrun


class Spikeclient(object):
    """
    A client Mediator superclass for forwarding acquisition system data to
    Spikebit Server.
    """

    def __init__(self,  acqhost,  spikebithost, params):
        """ Constructor method
        """
        self.acqhost = acqhost
        self.acqisconnected = False
        self.spikebithost = spikebithost
        self.nch = params["nch"]
        self.bufsz = params["bufsz"]
        self.port = params["port"]
        self.simsz = params["simsz"]
        self.fs = params["fs"]

    def acqconnect(self):
        """ Connect to the specific acquisition system using its API to define
        callback
        """
        self.acqisconnected = True

    def acqreceive(self, data):
        """
        Should implement the callback method from the acquisition system
        alternatively polling from main thread
        """
        pass

    def spikebitconnect(self):
        self.sbc = spikebit.sbcomm.Client(self.nCh, self.bufsz)
        self.sbc.connect(self.sbikebithost, self.port)


class Simclient(Spikeclient):
    """
    Client which does not have a real aquisition system
    """
    def __init__(self, acqhost,  spikebithost, params):
        super().__init__(acqhost, spikebithost, params)

    def acqconnect(self):
        super.acqconnect()

    def acqreceive(self, data):
        pass

    def main(self):
        spikebit.simrun.runsim(self.nch, self.simsz, self.bufsz, self.fs,
                               self.spikebithost, self.port)
