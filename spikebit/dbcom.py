#!/usr/bin/env python

import h5py
from mpi4py import MPI
import sbcomm
import os.path


class NMHdf(sbcomm.Subject):
    def __init__(self, fileName, fs, nCh, bufSz, nsys=1):
        self.defLength = 1 * 20 * fs  # 15 minutes
        self.fIx = 0
        self.sIx = 0
        self.tIx = 0
        self.lastData = None
        self.bufSz = bufSz
        if not os.path.isfile(fileName):
            self.f = h5py.File(fileName, 'a', driver='mpio',
                               comm=MPI.COMM_WORLD)
            for iSys in range(0, nsys):
                r = self.f.create_group("sess{}".format(iSys))
                r.create_dataset("speedData", (1, 10000))
                r.create_dataset("timeData", (1, 10000))
                r.create_dataset("ePhysData", (self.defLength, nCh))
        else:
            self.f = h5py.File(fileName, 'a', driver='mpio',
                               comm=MPI.COMM_WORLD)
        mpicomm = MPI.COMM_WORLD
        # print(mpicomm)
        commSz = mpicomm.Get_size()
        self.rank = mpicomm.Get_rank()
        super(NMHdf, self).__init__()

    def writeData(self, D):
        fKeys = self.f.keys()
        # print "Fkeys:{}".format(fKeys)
        rg = self.f["sess{}".format(self.rank)]
        # print "writing to sess{}".format(self.rank)
        r = rg["ePhysData"]
        stepL = D.shape[0]
        r[self.fIx:(self.fIx+stepL), :] = D
        self.fIx += stepL
        # print self.fIx
        self.lastData = D
        self.notify_observers(sbc.DATA_RECEIVED)

    def writeSpeed(self, tRate):
        rg = self.f["sess{}".format(self.rank)]
        q = rg["speedData"]
        q[0, self.sIx] = tRate
        self.sIx += 1

    def writeTime(self, theTime):
        rg = self.f["sess{}".format(self.rank)]
        q = rg["timeData"]
        q[0, self.tIx] = theTime
        self.tIx += 1

    def writeAnalysisTime(self, tRate):
        rg = self.f["sess{}".format(self.rank)]
        q = rg["Data"]
        q[0, self.sIx] = tRate
        self.sIx += 1

    def readlastData(self):
        return self.lastData

    def close(self):
        self.f.flush()
        self.f.close()
