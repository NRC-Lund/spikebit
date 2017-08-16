#!/usr/bin/env python

import numpy as np
import time
from mpi4py import MPI
import socket
import struct
import numpy
import socketserver
import dbcom

import thread
import weakref


DETECT_NONE = 1
DETECT_THRESHOLD = 2


class Client(object):
    def __init__(self, nch, bfsz):
        self.isConnected = False
        self.sock = []
        self.nch = nch
        self.bfsz = bfsz

    def connect(self, hostname, port):
        print("Connecting to server...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, port))
        self.sock.setblocking(True)
        self.isConnected = True
        print("Connection successful")

    def disconnect(self):
        if self.isConnected:
            self.sock.close()
            self.sock = []
            self.isConnected = False

    def sendData(self, sD):
        """sendData(sD) -- writes samples that must be given as a NUMPY array,
        samples x channels.
        """
        if not(isinstance(sD, numpy.ndarray)) or len(sD.shape) != 2:
            raise ValueError('Data must be numpy array size winsize x cells)')
        dataBuf = sD.data
        if not(self.isConnected):
            raise IOError('Not connected to SpikeBit server')
        self.sock.sendall(dataBuf)


class SpikebitServer(SocketServer.TCPServer, Observer):
    defLength = 15 * 60  # 15 min recording
    # TODO change to server forever

    def __init__(self, server_address, Clienthandler, params):
        SocketServer.TCPServer.__init__(self, server_address, Clienthandler)
        # filename="test2.hdf5"
        self.fs = fs = params["fs"]
        self.nCh = nCh = params["nCh"]
        self.bufSz = bufSz = params["bufSz"]
        self.simsz = simsz = params["simsz"]
        self.filename = filename = params["filename"]
        mpicomm = MPI.Comm.Get_parent()
        # commSz=mpicomm.Get_size()
        self.rank = mpicomm.Get_rank()
        self.dbc = dbcom.NMHdf(filename, fs, nCh, bufSz)
        self.detectedEvent = DETECT_NONE
        self.start_observing(self.dbc)
        self.doEval = False

    def handleerror(request, client_address):
        print("Client {} disconnected".format(client_address))
        super(request, client_address)

    def usershutdown(self):
        self.dbc.f.close()

    def notify(self, subject, msg):
        D = self.dbc.readlastData()
        if self.doEval:
            Dmean = np.mean(D, 1)
            # change to select which events to listen for
            if Dmean[0] > self.nCh:
                self.detectedEvent = DETECT_THRESHOLD
            else:
                self.detectedEvent = DETECT_NONE


class SpikebitTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for the SpikeBit server.
    It is instantiated once per connection to the server
    """

    def handle(self):
        t1 = time.clock()
        toNextBuff = ""
        dataBuff = []
        nCh = self.server.nCh
        bufSz = self.server.bufSz
        expectLen = nCh * bufSz * 4
        # TODO change to while loop instead and kill from outside (control 
        # server)
        for ix in range(1, self.server.simsz):
            reqlen = min(1024, expectLen)
            data = self.request.recv(reqlen)
            dataBuff = toNextBuff + data
            reclen = len(data)
            while reclen < expectLen:  # recieve local message
                data = self.request.recv(reqlen)
                dataBuff += data
                reclen = len(dataBuff)

            readBuff = buffer(dataBuff, 0, expectLen)
            D = np.ndarray(shape=(bufSz, nCh), dtype=np.int32, buffer=readBuff)
            toNextBuff = buffer(dataBuff, expectLen)
            self.server.dbc.writeData(D)
            t2 = time.clock()
            tDelta = t2 - t1
            tRate = D.size / (tDelta)
            self.server.dbc.writeSpeed(tRate)
            self.server.dbc.writeTime(t2)
            t1 = time.clock()
        print("Exiting handling client")

        def kill_me_please(server):
            server.shutdown()
        thread.start_new_thread(kill_me_please, (self.server,))


class Subject(object):
    def __init__(self):
        self._observers = weakref.WeakSet()

    def register_observer(self, observer):
        self._observers.add(observer)

    def notify_observers(self, msg):
        for observer in self._observers:
            observer.notify(self, msg)


class Observer(object):
    def __init__(self):
        pass

    def start_observing(self, subject):
        subject.register_observer(self)

    def notify(self, subject, msg):
        pass
