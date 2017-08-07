import numpy as np
def tilarang(int nCh,int winSz,int method):
    """Create Wavefunction"""
    if method==0:
        wave=np.arange(1,nCh+1,1,dtype=np.int32)
    else:
        wave=np.arange(101,nCh+101,1,dtype=np.int32)
    nump=np.transpose(np.tile(wave,(winSz,1)))
    return nump