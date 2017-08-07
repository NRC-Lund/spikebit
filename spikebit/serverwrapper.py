#!/usr/bin/env python
import argparse
from mpi4py import MPI
import sbcomm

parser = argparse.ArgumentParser()
parser.add_argument("--fs", help="sampling frequency",
                    type=int, required=True)
parser.add_argument("--nch", help="number of channels",
                    type=int, required=True)
parser.add_argument("--bufsz", help="buffer size",
                    type=int, required=True)
parser.add_argument("--simsz", help="simulation size",
                    type=int, required=True)
parser.add_argument("--filename", help="simulation size",
                    type=str, required=True)


args = parser.parse_args()

print("Started!")

mpicomm = MPI.Comm.Get_parent()
rank = mpicomm.Get_rank()
print("Rank".format(rank))

HOST, PORT = "", 29170 + rank
params = {"fs": args.fs, "nCh": args.nch, "bufSz": args.bufsz,
          "simsz": args.simsz, "filename": args.filename}

# Create the server, binding to localhost on port 9999
sbs = sbcomm.MyTCPServer((HOST, PORT), sbcomm.MyTCPHandler, params)
print("Server listening on port: {}".format(PORT))
try:
    sbs.serve_forever()
except KeyboardInterrupt:
    print("^C detected;")
finally:
    print("Shutting down")
    sbs.usershutdown()
    sbs.server_close()
    print("bye")
print("Server killed on port: {}".format(PORT))
mpicomm.Disconnect()
