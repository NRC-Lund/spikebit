#!/usr/bin/env python

#import neuromining.neurosim as nsim
import argparse
import neurosim as nsim
from socket import error
import time
from  mpi4py import MPI

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="host to connect to",
                    type=str, required=True)
parser.add_argument("--port", help="port to connect to",
                    type=int, required=True)
parser.add_argument("--simsz", help="size of simulation",
                    type=int, required=True)
parser.add_argument("--bufsz", help="size of buffer",
                    type=int, required=True)
parser.add_argument("--nch", help="Number of channels",
                    type=int, required=True)
parser.add_argument("--ntrials", help="Number of trials",
                    type=int, required=True)


mpicomm=MPI.COMM_WORLD
args = parser.parse_args()
port=args.port+mpicomm.Get_rank()
hostname = args.host
#hostname = '192.168.1.3'

nCh,simSz,bufSz,fs,nTrials=args.nch,args.simsz,args.bufsz,1000,args.ntrials
# for iCh in range(1000,10000,1000):
# 
# 
# 	data = {
#         'nSystems': nCh,
# 		'nChannels': iCh,
# 		'sessNo': 1,
# 		'samplingRate': fs,
# 		'port': args.port,
# 		'host': hostname,
# 		'filename': 'test.hdf5'
# 	}
# 
# 	req = urllib2.Request('http://{}/api/setparams'.format(hostname ))
# 	req.add_header('Content-Type', 'application/json')
# 	print 'http://{}/api/setparams'.format(hostname )

	#response = urllib2.urlopen(req, json.dumps(data))
#for ich in range(2000,24000,2000):
ich=10000;
for itrial in range(1,args.ntrials+1):
	try:
		nsim.runsim(ich,simSz,bufSz,fs,hostname,port)
	except error:
		"Server closed connection"
	time.sleep(2)
		
	
	#req2 = urllib2.urlopen('http://{}/api/killthreads'.format(hostname ))
