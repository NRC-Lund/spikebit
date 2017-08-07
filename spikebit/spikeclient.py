#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 00:27:35 2017

@author: bengt
"""


class spikeclient(object):
    """
    A client superclass for forwarding acquisition system data to 
    """
    def __init__(self, acqhost, spikebithost):
        self.acqhost = acqhost
        self.acqisconnected = False
        self.spikebithost = spikebithost

    def acqconnect(self):
        self.acqconnect = True

    def main():
        pass


class simclient(spikeclient):
    def __init__(self, acqhost, spikebithost):
        super.__init__(acqhost, spikebithost)
        #TODO initaite client

    def acqconnect(self):
        super.acqconnect()

    def main():
        
