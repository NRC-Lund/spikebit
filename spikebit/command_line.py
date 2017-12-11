#!/usr/bin/env python

import argparse

from mpi4py import MPI
import spikebit.dbcom as sbd
import spikebit.spikeclient
import socket


def parsecommon(parser):
    """
    Parse common arguments
    """
    parser.add_argument("--simsz", help="size of simulation",
                        type=int,  default=0)
    parser.add_argument("--bufsz", help="size of buffer",
                        type=int,  default=20)
    parser.add_argument("--nch", help="Number of channels",
                        type=int, default=1000)
    parser.add_argument("--fs", help="sampling frequency",
                        type=int, default=1000)
    parser.add_argument("--port", help="port to connect to",
                        type=int, default=29170)
    return parser


def server():
    """
    server() - spawns servers as specified
    """
    parser = argparse.ArgumentParser()
    parser = parsecommon(parser)
    parser.add_argument("--nsys", help="number of systems",
                        type=int, default=1)

    parser.add_argument("--filename", help="file name to use for hdf file",
                        default='spikebit.hdf5')
    args = parser.parse_args()
    sbnm = sbd.SBHdf(args.filename, args.fs, args.nch, args.bufsz,
                     args.nsys)
    sbnm.close()
    # for isys in range(1, args.nsys+1):
    #    print("Spawning server no: {}".format(isys))
    comm = MPI.COMM_SELF.Spawn(
        'spikebit-singleserver',
        args=['--fs={}'.format(args.fs),
              '--nch={}'.format(args.nch),
              '--bufsz={}'.format(args.bufsz),
              '--filename={}'.format(args.filename),
              '--simsz={}'.format(args.simsz),
              '--port={}'.format(args.port)],
        maxprocs=args.nsys)
    comm.Disconnect()


def client():
    """
    client() - connects to a server and checks for eventual mpi comm world
    """
    parser = argparse.ArgumentParser()
    parser = parsecommon(parser)
    parser.add_argument("--host", help="host to connect to",
                        type=str, default='localhost')

    mpicomm = MPI.COMM_WORLD
    args = parser.parse_args()
    # Parallell sessions run on consecutive ports
    port = args.port + mpicomm.Get_rank()
    hostname = args.host
    params = {"fs": args.fs, "nch": args.nch, "bufsz": args.bufsz,
              "simsz": args.simsz, "port": port}
    try:
        # Currently,  only simclient is implemented
        sps = spikebit.spikeclient.Simclient('localhost', hostname, params)
        sps.main()
    except socket.error:
        print("Error: Server closed connection")
