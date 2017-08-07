#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 22:28:28 2017

@author: bengt
"""
def mpi_hdf_test():
    """
    TODO: Must spawn child process
    """
    from mpi4py import MPI
    import h5py
    
    rank = MPI.COMM_WORLD.rank  # The process ID (integer 0-3 for 4-process run)
    
    f = h5py.File('parallel_test.hdf5', 'w', driver='mpio', comm=MPI.COMM_WORLD)
    dset = f.create_dataset('test', (4,), dtype='i')
    dset[rank] = rank
    f.close()