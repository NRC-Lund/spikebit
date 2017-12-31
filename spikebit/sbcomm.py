#!/usr/bin/env python3
"""
@author: Bengt Ljungquist
"""
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
        """ connect(hostname,port)  - connect to server port at host hostname
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

    def send_data(self, s_data):
        """sends data to server
        args:
            s_data: windowsize x channels numpy array
        """
        if not(isinstance(s_data, numpy.ndarray)) or len(s_data.shape) != 2:
            raise ValueError('Data should be numpy array: channels x winsize)')
        if not(self.isConnected):
            raise IOError('Not connected to SpikeBit server')
        self.sock.sendall(s_data.data)  # send numpy internal memory buffer


class SpikebitTCPHandler(socketserver.StreamRequestHandler):
    """class defining the request handler used by the SpikebitServer class
    """
    def handle(self):
        """ method called when request received by server
        """
        server = self.server
        n_ch = server.nch
        win_size = server.bufsz
        request = self.request
        t1 = time.clock()
        data = b''  # Init data to empty binary string
        expect_len = n_ch * win_size * 4

        break_next = False
        while True:
            try:
                while len(data) < expect_len:
                    this_data = request.recv(expect_len-len(data))
                    if not this_data:
                        break  # No more data received
                    else:
                        data += this_data
                if (len(data) == 0):
                    if break_next:
                        break
                    else:
                        break_next = True
                        continue
                else:
                    break_next = False
                np_data = np.ndarray(
                    shape=(n_ch, win_size),
                    dtype=np.uint32, buffer=data)
                server.dbc.write_data(np_data)
                data = b''
                t2 = time.clock()
                t_delta = t2 - t1
                speed = np_data.size * 32 / (t_delta)  # Writing 32 bits
                server.dbc.write_speed(speed)
                server.dbc.write_time(t2)
                t1 = time.clock()
            except Exception as e:
                print(e)
                raise e

        def kill_me_please(server):
            """ function called to shutdown the server
            by starting a new thread
            """
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
        self.file_name = file_name = params["file_name"]
        mpicomm = MPI.Comm.Get_parent()
        self.rank = mpicomm.Get_rank()
        self.dbc = spikebit.dbcom.SBHdf(file_name, fs, nch, bufsz)
        self.detected_event = DETECT_NONE
        self.start_observing(self.dbc)
        self.do_eval = True  # Do evaluation

    def handleerror(self, request, client_address):
        """ called when error in connection to client

        args:
            request: the current request
            client_address: the client address for which error is received
        """
        print("Client {} disconnected".format(client_address))
        super(request, client_address)

    def usershutdown(self):
        self.dbc.file_obj.close()

    def notify(self, subject, msg):
        """ called by observed subject with message msg

        args:
            msg: message to send to observers, as defined by constant with
            prefix detect.
        """
        data = self.dbc.read_last_data()
        if self.do_eval:
            Dmean = np.mean(data, 1)
            # change to select which events to listen for
            if Dmean[0] > self.nch:
                self.detected_event = DETECT_THRESHOLD
            else:
                self.detected_event = DETECT_NONE
