"""Optional GCC binary128 Newton proposals, followed by independent checking."""
import ctypes
from pathlib import Path
import numpy as np
_DLL=None

def refine_quad(x,u,iterations=4):
    global _DLL
    if _DLL is None:
        path=Path(__file__).with_name('quad_proposal_kernel.so')
        if not path.exists():raise RuntimeError('Build quad_proposal.so first')
        _DLL=ctypes.CDLL(str(path));p=ctypes.POINTER(ctypes.c_double)
        _DLL.sp03_refine_quad.argtypes=[ctypes.c_int,p,p,p,ctypes.c_int]
        _DLL.sp03_refine_quad.restype=ctypes.c_int
    x=np.ascontiguousarray(x,dtype=np.complex128).ravel()
    u=np.ascontiguousarray(u,dtype=np.complex128).ravel()
    n=int(round(np.sqrt(x.size)))
    if n<2 or n%2 or n*n!=x.size or u.shape!=x.shape:raise ValueError('Invalid shapes')
    out=np.empty_like(x);p=ctypes.POINTER(ctypes.c_double)
    code=_DLL.sp03_refine_quad(n,x.ctypes.data_as(p),u.ctypes.data_as(p),out.ctypes.data_as(p),iterations)
    if code:raise ArithmeticError(f'High-precision Newton proposal failed ({code})')
    return out
