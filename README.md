# SpikeBit compression

## Dependencies
- Python3 - we have developed and tested SpikeBit . The following packages needs to be installed using `pip`: `numpy mpi4py cython python-lzf`
- Linux/OS - SpikeBit is tested on Ubuntu 16.04 but most distributions would probably do. The following packages need to be installed using apt package manager: `openmpi-bin openmpi-doc libopenmpi-dev` 
- MPI - our solution has run using the openmpi option as noted above, but in general other mpi implementations such as mpich would probably be fine. 
- hdf5 - must be compiled and installed  from source using the following options. Compilation is made with the following option: `$./configure --enable-parallel --enable-shared`
```

```

- 
