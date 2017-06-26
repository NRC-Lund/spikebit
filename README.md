# SpikeBit compression
SpikeBit is an architecture for integrating multiple massive parallel recordings of spiketrains using high-speed Ethernet.

## Hardware configuration
- CPU(s) with support for as many threads as acquistions systems that are connected to is strongly recommended. 
- Please consider high performance storage device for data files, such as solid stated drive(s). If recording over longer periods of time, please also consider performance capacity. 
- GbE or if possible 10GbE as Ethernet medium, at least for highly recommended.

## Dependencies (in order of suggested installation order)
- Linux/OS - SpikeBit is tested on Ubuntu 16.04 but most distributions would probably do. The following packages need to be installed using apt package manager: `openmpi-bin openmpi-doc libopenmpi-dev` 
- MPI - our solution has run using the openmpi option as noted above, but in general other mpi implementations such as mpich would probably be fine. 
- hdf5 - You may either install package `libhdf5-openmpi-dev` or  be compiled and installed  from source using the following options. Compilation is made with the following option: `$./configure --enable-parallel --enable-shared`
- Python3 - we have developed and tested SpikeBit using python 3.5. The following packages needs to be installed using `pip`: `numpy mpi4py cython python-lzf`. h5py needs to be compiled and installed separately with [mpi support](http://docs.h5py.org/en/latest/mpi.html#building-against-parallel-hdf5)
