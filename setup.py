#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:30:36 2017

@author: bengtl
"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

setup(name='spikebit',
      description='Electrophysiology data integration',
      version='0.2',
      author='Bengt Ljungquist',
      authour_email='bengt@ljungquist.info',
      py_modules=['spikebit'],
      install_requires=['Cython>=0.25.2',
                    'h5py>=2.7',
                    'mpi4py>=2.0',
                    'numpy>=1.13.0'
                    ],
      platforms='linux',
      license='MIT',
      cmdclass = {'build_ext': build_ext},
      ext_modules = [Extension("mandelcy", ["mandelcy.pyx"], )],
      include_dirs = [numpy.get_include(),],
      entry_points = {
        'console_scripts': 
            ['spikebit-server=spikebit.command_line:server_main',
            'spikebit-client=spikebit.command_line:client_main'],
            })
