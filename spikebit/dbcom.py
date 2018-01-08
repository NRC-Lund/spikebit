#!/usr/bin/env python3

import h5py
from mpi4py import MPI
import spikebit.observer as sbo
import os.path


class SBHdf(sbo.Observable):
    def __init__(self, file_name, fs, nCh, bufsz, nsys=1):
        self.file_length = 1 * 10 * fs  # 60 s to start with
        self.file_i = 0
        self.speed_i = 0
        self.time_i = 0
        self.last_data = None
        self.bufsz = bufsz
        if not os.path.isfile(file_name):
            self.file_obj = h5py.File(file_name, 'a', driver='mpio',
                               comm=MPI.COMM_WORLD)
            for i_sys in range(0, nsys):
                a_group = self.file_obj.create_group("session{}".format(i_sys))
                a_group.create_dataset("speedData", (1, 10000))
                a_group.create_dataset("timeData", (1, 10000))
                a_group.create_dataset("ePhysData", (nCh, self.file_length),
                                 dtype='uint32')
        else:
            self.file_obj = h5py.File(file_name, 'a', driver='mpio',
                               comm=MPI.COMM_WORLD)
        mpicomm = MPI.COMM_WORLD
        self.comm_sz = mpicomm.Get_size()
        self.rank = mpicomm.Get_rank()
        super(SBHdf, self).__init__()

    def write_data(self, data):
        a_group = self.file_obj["session{}".format(self.rank)]
        data_set = a_group["ePhysData"]
        step_size = data.shape[1]
        data_set[:, self.file_i:(self.file_i+step_size)] = data
        self.file_i += step_size
        self.last_data = data
        self.notify_observers(sbo.DATA_RECEIVED)

    def write_speed(self, speed):
        a_group = self.file_obj["session{}".format(self.rank)]
        data_set = a_group["speedData"]
        data_set[0, self.speed_i] = speed
        self.speed_i += 1

    def write_time(self, the_time):
        a_group = self.file_obj["session{}".format(self.rank)]
        data_set = a_group["timeData"]
        data_set[0, self.time_i] = the_time
        self.time_i += 1

    # def write_analysis_time(self, atime):
    #     a_group = self.file_obj["session{}".format(self.rank)]
    #     data_set = a_group["Data"]
    #     data_set[0, self.speed_i] = atime
    #     self.speed_i += 1

    def read_last_data(self):
        return self.last_data

    def close(self):
        self.file_obj.flush()
        self.file_obj.close()
