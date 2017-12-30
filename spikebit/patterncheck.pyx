"""
@author: Bengt Ljungquist
"""
import numpy as np
cimport numpy as np
# import gmpy2
# from gmpy2 import mpz

def check_pattern(np.ndarray data, np.ndarray a_pattern):
    """ Checks bitwise if bits of the required pattern aPattern are set
    in columns of array D. Returns an array of booleans for each bin of
    window
    """
    # check if equal with np.equal()
    win_sz = data.shape[1]    
    pattern_mat = np.transpose(np.tile(a_pattern,(win_sz,1)))
    return np.all(np.equal(data,pattern_mat), axis=0)