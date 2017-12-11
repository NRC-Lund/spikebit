#!/usr/bin/env python

import numpy as np
import time
from mpi4py import MPI
import socket
import numpy
import spikebit.dbcom
import spikebit.observer
import socketserver
import _thread


DETECT_NONE = 1  # Nothing detected
DETECT_THRESHOLD = 2  # Detected a threshold


class Client(object):
    def __init__(self, nch, bfsz):
        """ Constructor method
        """
        self.isConnected = False
        self.sock = []
        self.nch = nch
        self.bfsz = bfsz

    def connect(self, hostname, port):
        """ connect (hostname,port)  - connect to server port at host hostname
        """
        print("Connecting to server...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, port))
        self.sock.setblocking(True)
        self.isConnected = True
        print("Connection successful")

    def disconnect(self):
        """ disconnect () - disconnects from server
        """
        if self.isConnected:
            self.sock.close()
            self.sock = []
            self.isConnected = False

    def sendData(self, sD):
        """sendData(sD) -- writes samples that must be given as a numpy array,
        windowsize x channels.
        """
        if not(isinstance(sD, numpy.ndarray)) or len(sD.shape) != 2:
            raise ValueError('Data should numpy array: winsize x channels)')
        if not(self.isConnected):
            raise IOError('Not connected to SpikeBit server')
        self.sock.sendall(sD.data)  # send numpy internal memory buffer


class SpikebitTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print('Handling')
        t1 = time.clock()
        data = b''  # Init data to empty binary string
        expectLen = self.server.nch*self.server.bufsz*4
        # while True:
        breakNext = False
        while True:
            try:
                while len(data) < expectLen:
                    thisData = self.request.recv(expectLen-len(data))
                    if not thisData:
                        break  # No more data received - breaking
                    else:
                        data += thisData
                if (len(data) == 0) & breakNext:
                    break
                elif len(data) == 0:
                    breakNext = True
                    continue
                else:
                    breakNext = False
                D = np.ndarray(shape=(self.server.bufsz, self.server.nch),
                               dtype=np.uint32, buffer=data)
                self.server.dbc.writeData(D)
                data = b''
                t2 = time.clock()
                tDelta = t2 - t1
                tRate = D.size * 32 / (tDelta)  # Writing 32 bits
                self.server.dbc.writeSpeed(tRate)
                self.server.dbc.writeTime(t2)
                t1 = time.clock()
            except Exception as e:
                print(e)
                raise e

        def kill_me_please(server):
            server.shutdown()
        _thread.start_new_thread(kill_me_please, (self.server,))


class SpikebitServer(socketserver.TCPServer, spikebit.observer.Observer):

    def __init__(self, server_address, Clienthandler, params):
        """ Constructor method - initates attributes and starts server
        """
        print(server_address)
        socketserver.TCPServer.__init__(self, server_address, Clienthandler)
        self.fs = fs = params["fs"]
        self.nch = nch = params["nch"]
        self.bufsz = bufsz = params["bufsz"]
        self.simsz = params["simsz"]
        self.filename = filename = params["filename"]
        mpicomm = MPI.Comm.Get_parent()
        self.rank = mpicomm.Get_rank()
        self.dbc = spikebit.dbcom.SBHdf(filename, fs, nch, bufsz)
        self.detectedEvent = DETECT_NONE
        self.start_observing(self.dbc)
        self.doEval = True  # Do evaluation

    def handleerror(request, client_address):
        print("Client {} disconnected".format(client_address))
        super(request, client_address)

    def usershutdown(self):
        self.dbc.f.close()

    def notify(self, subject, msg):
        """ notify(subject, msg) - called by observed subject with message msg
        """
        D = self.dbc.readlastData()
        if self.doEval:
            Dmean = np.mean(D, 1)
            # change to select which events to listen for
            if Dmean[0] > self.nch:
                self.detectedEvent = DETECT_THRESHOLD
            else:
                self.detectedEvent = DETECT_NONE

