"""
Created on Sun Jul  2 19:02:44 2017

@author: bengt
"""
import numpy as np
cimport numpy as np
import gmpy2
from gmpy2 import mpz

def checkForPattern(np.ndarray D, np.ndarray aPattern):
    """ 
    patterncheck(D,aPattern) 
    Checks bitwise if bits of the required pattern aPattern are set in columns
    of array D. Returns an array of booleans for each bin of window
    """
    # TODO tile aPattern to same size as D 
    # check if equal with np.equal()
    winSz = D.shape[1]    
    patternMat = np.transpose(np.tile(aPattern,(winSz,1)))
    return np.all(np.equal(D,patternMat), axis=0)