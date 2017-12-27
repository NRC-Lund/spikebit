# SpikeBit
SpikeBit is an architecture and data format for integrating multiple massive parallel recordings of spiketrains using high-speed Ethernet. For more information, see the [Wiki](https://github.com/NRC-Lund/spikebit/wiki)

## Install
1. Hdf5 needs to be installed with support for parallel writing and reading, using mpi, which also need to be installed. It is also recommended to install pip package manager for python3. Options (either of):
   1. Compile from source, see [parallel hdf5 documentation](https://support.hdfgroup.org/HDF5/PHDF5/) 
   2. Install package using apt: `$ sudo apt-get install openmpi-bin libopenmpi-dev libhdf5-openmpi-dev python3-pip build-essential gfortran libatlas-base-dev python3-dev`
2. Install numpy, Cython and mpi4py python packages using pip package manager: `$ sudo pip3 install Cython scipy mpi4py numpy`
3. Clone the h5py library using git: `$ git clone https://github.com/h5py/h5py.git`
4. Change directory to h5py `$cd h5py` and build h5py with support for [parallell hdf5](http://docs.h5py.org/en/latest/mpi.html#building-against-parallel-hdf5)
5. Install h5py `sudo python3 setup.py install`
6. Clone spikebit using git: `$ git clone https://github.com/NRC-Lund/spikebit.git`
7. Change directory to spikebit `$ cd spikebit`. Build using the setup script: `$ python3 setup.py build_ext`
8. Install the python "egg": `$ sudo python3 setup.py install`.

## Usage
For server, run: `$ spikebit-server`
For client, run: `$ spikebit-client`. For testing out multiple clients for testing purposes, it is convenient to use `mpiexec`: `$ mpiexec -n x spikebit-client`, where x is the number of parallell clients to run. 

### Common arguments: 
* --nch - number of neurons (per system, default 1000)
* --bufsz - message window length (20 recommended, default)
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
- Linux/OS - SpikeBit is tested on Ubuntu 16.04 but most distributions would probably do.
- MPI - our solution has run using openmpi 1.10.2, but in general other mpi implementations such as mpich would probably be fine. 
- hdf5 -  We have tested using hdf version 1.8.16 
- Python3 - we have developed and tested SpikeBit using python 3.5.2.
