import time
import sbcomm
import randspikes as rsp
import random
import numpy as np
import socket

#TODO 
# - change names from neuromining
# - change packet names

def busy_wait(dt):
	curr_time=time.time
	while (time.time()<curr_time+dt):
		pass

def runsim(int nCh,int simSz,int bufSz,int fs,str host,int port):
	sbc=sbcomm.Client(nCh,bufSz)
	sbc.connect(host,port)
	
	altData=rsp.randspikes(nCh,bufSz,1)
	theData=rsp.randspikes(nCh,bufSz,0)
	cdef double compTime=bufSz/fs
	tTimes=[] 

	for i in range(0,simSz):
		t1=time.time()
		if i%40==21:
			#print altData
			sbc.sendData(altData)
			# HOST = ''                
			# PORT = 50007              
			# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# s.bind((HOST, PORT))
			# s.listen(1)
			# print "listening on {}".format(PORT)
			# conn, addr = s.accept()
			# while 1:
			# 	data = conn.recv(1024)
			# 	if not data: break
			# conn.close()
			# print "Recieved confirmation"
		else:
			#print theData.dtype
			sbc.sendData(theData)
		t2=time.time()
		timePass=t2-t1
		tTimes=np.append(tTimes,timePass)
		timeRem=compTime-timePass
		#print "compTime: {}, timePass: {}".format(compTime,timePass)
		#if timeRem<0:
		#	print "Warning{}".format(timeRem)
#		else:
#			busy_wait(timeRem)
	sbc.disconnect()
	theMean=np.mean(tTimes)
	print theMean