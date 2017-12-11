#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: bengtl
"""
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy

extensions = [Extension("spikebit.encoder", ["spikebit/encoder.pyx"],
                        include_dirs=[numpy.get_include()]),
              Extension("spikebit.patterncheck",
                        ["spikebit/patterncheck.pyx"],
                        include_dirs=[numpy.get_include()]),
              Extension("spikebit.simrun",
                        ["spikebit/simrun.pyx"],
                        include_dirs=[numpy.get_include()])]

setup(name='spikebit',
      description='Electrophysiology data integration',
      version='0.21',
      install_requires=['mpi4py>=3.0', 'Cython>=0.27', 'numpy>=1.13',
                        'h5py>=2.7'],
      author='Bengt Ljungquist',
      author_email='bengt@ljungquist.info',
      py_modules=['spikebit'],
      platforms='linux',
      packages=find_packages(exclude=['test']),
      license='MIT',
      ext_modules=cythonize(extensions),
      include_dirs=[numpy.get_include()],
      entry_points={
        'console_scripts':
            ['spikebit-server=spikebit.command_line:server',
             'spikebit-singleserver=spikebit.serverwrapper:main',
             'spikebit-client=spikebit.command_line:client'],
            })
