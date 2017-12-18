# SpikeBit
SpikeBit is an architecture and data format for integrating multiple massive parallel recordings of spiketrains using high-speed Ethernet. For more information, see article published in [TBD]

## Install
1. Hdf5 needs to be installed with support for parallel writing and reading, using mpi, which also need to be installed. It is also recommended to install pip package manager for python3. Options:
   1. Compile from source, see [parallel hdf5 documentation](https://support.hdfgroup.org/HDF5/PHDF5/) 
   2. Install package using apt: `$sudo openmpi-bin openmpi-doc libopenmpi-dev libhdf5-openmpi-dev python3-pip`
2. Clone using git: `$ git clone  
3. Run: `$ python3 setup.py build_ext`
4. Run: `$ python3 setup.py install` (will download missing python packages if pip is installed)

## Usage
For server, run: `$ spikebit-server`
For client, run: `$ spikebit-client`. For testing out multiple clients for testing purposes, it is convenient to use `mpiexec`: `$ mpiexec -n x spikebit-client`, where x is the number of parallell clients to run. 

### Common arguments: 
* --nch - number of channels (default 1000)
* --bufsz - message window lenth (20 recommended, default)
* --fs - bin sampling frequency (default 1000)
* --port - port to connect to on server/sport listening on server (default 29170)

### Client arguments:
* --host - server to connect to (default localhost)
* --simsz - size of simulation, number of complete messages to send (default 100)

### Server arguments:
* --nsys - number of clients to connect to (default 1 system)
* --filename - filename to use for hdf5 file (default set to current datetime in format %Y-%m-%d-%H%M%S.hdf5)

## Hardware configuration
- CPU(s) with support for as many threads (that is, total number of cores) as acquisition systems that are connected to is strongly recommended. 
- Please consider high performance storage device for data files, such as solid stated drive(s). If recording over longer periods of time, please also consider performance capacity. 
- GbE or if possible 10GbE as Ethernet medium is highly recommended.

## Dependencies (in order of suggested installation order)
- Linux/OS - SpikeBit is tested on Ubuntu 16.04 but most distributions would probably do. The following packages need to be installed using apt package manager: `openmpi-bin openmpi-doc libopenmpi-dev` 
- MPI - our solution has run using openmpi 1.10.2, but in general other mpi implementations such as mpich would probably be fine. 
- hdf5 -  We have tested using hdf version 1.8.16 You may either install package `libhdf5-openmpi-dev` or  be compiled and installed  from source using the following options. Compilation is made with the following option: `$./configure --enable-parallel --enable-shared`
- Python3 - we have developed and tested SpikeBit using python 3.5.2. The following packages needs to be installed using `pip`: `numpy mpi4py cython python-lzf`. h5py needs to be compiled and installed separately with [mpi support](http://docs.h5py.org/en/latest/mpi.html#building-against-parallel-hdf5)
