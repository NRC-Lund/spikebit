#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: bengtl
"""
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Distutils import build_ext
import numpy

extensions = [Extension("spikebit.encoder", ["spikebit/encoder.pyx"]),
                Extension("spikebit.patterncheck",
                          ["spikebit/patterncheck.pyx"]),
                Extension("spikebit.simrun",
                          ["spikebit/simrun.pyx"])]

setup(name='spikebit',
      description='Electrophysiology data integration',
      version='0.7',
      install_requires=['mpi4py>=3.0','Cython>=0.27','numpy>=1.13',
      'h5py>=2.7'],
      author='Bengt Ljungquist',
      authour_email='bengt@ljungquist.info',
      py_modules=['spikebit'],
      platforms='linux',
      packages= find_packages(exclude=['test']),
      license='MIT',
      cmdclass={'build_ext': build_ext},
      ext_modules=extensions,
      include_dirs=[numpy.get_include()],
      entry_points={
        'console_scripts':
            ['spikebit-server=spikebit.command_line:server',
            'spikebit-client=spikebit.command_line:client'],
            })
