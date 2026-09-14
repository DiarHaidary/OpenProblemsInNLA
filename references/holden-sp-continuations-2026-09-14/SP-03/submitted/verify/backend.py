"""ctypes interface to the supplied exact-integer certificate backend."""
from pathlib import Path
import ctypes
import numpy as np
_DLL=None

def load():
    global _DLL
    if _DLL is None:
        path=Path(__file__).with_name('exact_backend.so')
        if not path.exists():
            raise RuntimeError('Build exact_backend.so using the command in README.md')
        _DLL=ctypes.CDLL(str(path))
        ptr=ctypes.POINTER(ctypes.c_double)
        _DLL.sp03_verify.argtypes=[ctypes.c_int,ptr,ptr,ptr,ctypes.POINTER(ctypes.c_int),ptr]
        _DLL.sp03_verify.restype=ctypes.c_int
    return _DLL

def check(x,u,B):
    x=np.ascontiguousarray(x,dtype=np.complex128).ravel()
    u=np.ascontiguousarray(u,dtype=np.complex128).ravel()
    n=int(round(np.sqrt(x.size)));d=n*n
    B=np.ascontiguousarray(B,dtype=np.complex128)
    if n<2 or n%2 or x.size!=d or u.size!=d or B.shape!=(d,d):
        raise ValueError('Incompatible even-square matrix and preconditioner shapes')
    if not all(np.isfinite(z).all() for z in (x,u,B)):
        raise ValueError('Inputs must be finite')
    ptr=ctypes.POINTER(ctypes.c_double)
    bounds=np.zeros(4,dtype=np.float64);re=ctypes.c_int()
    code=load().sp03_verify(n,x.ctypes.data_as(ptr),u.ctypes.data_as(ptr),B.ctypes.data_as(ptr),ctypes.byref(re),bounds.ctypes.data_as(ptr))
    if code<0:raise RuntimeError('Exact verifier rejected malformed input')
    return code==0,re.value,bounds
