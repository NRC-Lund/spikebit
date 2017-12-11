#!/usr/bin/env python
import argparse
from mpi4py import MPI
import spikebit.sbcomm as spiksbc
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fs", help="sampling frequency",
                        type=int)
    parser.add_argument("--nch", help="number of channels",
                        type=int)
    parser.add_argument("--bufsz", help="buffer size",
                        type=int, default=20)
    parser.add_argument("--simsz", help="simulation size",
                        type=int, default=10)
    parser.add_argument("--filename", help="filename",
                        type=str, default='spikebit.hdf5')
    parser.add_argument("--port", help="port to connect to",
                        type=int, default=29170)
    args = parser.parse_args()
    mpicomm = MPI.Comm.Get_parent()
    rank = mpicomm.Get_rank()
    host, port = "localhost", args.port + rank
    params = {"fs": args.fs, "nch": args.nch, "bufsz": args.bufsz,
              "simsz": args.simsz, "filename": args.filename}
    # Create the server
    print("Starting the server")
    sbs = spiksbc.SpikebitServer((host, port),
                                 spiksbc.SpikebitTCPHandler, params)
    try:
        sbs.serve_forever()
    except KeyboardInterrupt:
        print("^C detected;")
    except:
        print("Unexpected error: {}".format(sys.exc_info()[0]))
        raise
    finally:
        print("Shutting down")
        sbs.server_close()
        print("bye")
        mpicomm.Disconnect()
        print("Server killed on port: {}".format(port))
