#!/usr/bin/env python

import argparse

import sys
from mpi4py import MPI
import spikebit.dbcom as sbd
import socket
import time
import spikebit.spikeclient as sps


def parsecommon(parser):
    """
    Parse common arguments
    """
    parser.add_argument("--simsz", help="size of simulation",
                        type=int, required=True)
    parser.add_argument("--bufsz", help="size of buffer",
                        type=int, required=True)
    parser.add_argument("--nch", help="Number of channels",
                        type=int, required=True)
    parser.add_argument("--fs", help="sampling frequency",
                        type=int, required=True)
    parser.add_argument("--ntrials", help="Number of trials",
                        type=int, required=True)
    return parser


def server():
    """
    Server method
    """
    parser = argparse.ArgumentParser()
    parser = parsecommon(parser)
    parser.add_argument("--nsys", help="number of systems",
                        type=int, required=True)
    args = parser.parse_args()

    for isys in range(1, args.nsys+1):
        ich = args.nch
        for itrial in range(1, args.ntrials+1):
            filename = "{}_{}_{}_{}.hdf5".format(args.fs, ich, isys, itrial)
            sbnm = sbd.NMHdf(filename, args.fs, ich, args.bufsz, args.nsys)
            sbnm.close()
            print("Spawning server no %d, trial %d", isys, itrial)
            comm = MPI.COMM_SELF.Spawn(sys.executable,
                                       args=['serverwrapper.py',
                                             '--fs={}'.format(args.fs),
                                             '--nch={}'.format(ich),
                                             '--bufsz={}'.format(args.bufsz),
                                             '--filename={}'.format(filename),
                                             '--simsz={}'.format(args.simsz)],
                                       maxprocs=isys)
            comm.Disconnect()


def client():
    """
    Client method
    """
    parser = argparse.ArgumentParser()
    parser = parsecommon(parser)
    parser.add_argument("--host", help="host to connect to",
                        type=str, required=True)
    parser.add_argument("--port", help="port to connect to",
                        type=int, required=True)

    mpicomm = MPI.COMM_WORLD
    args = parser.parse_args()
    port = args.port + mpicomm.Get_rank()
    hostname = args.host
    nCh, simSz, bufSz, fs, nTrials = args.nch, args.simsz, args.bufsz, args.fs, args.ntrials
    for itrial in range(1, nTrials+1):
        try:
            sps.main(nCh, simSz, bufSz, fs, hostname, port)
        except socket.error:
            "Server closed connection"
        time.sleep(2)
