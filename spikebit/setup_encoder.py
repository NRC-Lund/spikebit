# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 00:29:08 2017

@author: bengt
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
  name='encoder test',
  ext_modules=cythonize("encoder.pyx"),
)
