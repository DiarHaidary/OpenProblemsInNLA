"""The denominator-free SP-03 critical system (ordinary transpose).

Numba accelerates numerical proposals only. Acceptance of certificates is
performed independently by the exact-integer backend, which reconstructs
both the polynomial system and its Jacobian from the stored dyadic inputs.
"""
from __future__ import annotations
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import numpy as np
from numba import njit

@njit(cache=True, nogil=True)
def evaluate(x, u, n):
    """Return F_U(x) and its row-major Jacobian; no complex conjugations."""
    m=n//2; d=n*n
    X=x.reshape((n,n)); U=u.reshape((n,n))
    JX=np.empty_like(X); XJ=np.empty_like(X)
    for a in range(n):
        for b in range(n):
            JX[a,b]=X[a+m,b] if a<m else -X[a-m,b]
            XJ[a,b]=-X[a,b+m] if b<m else X[a,b-m]
    F=np.empty(d,np.complex128); H=np.zeros((d,d),np.complex128)
    row=0
    for i in range(n):
        for j in range(i+1,n):
            value=0j
            for a in range(n):
                value+=X[a,i]*JX[a,j]
                H[row,a*n+i]+=JX[a,j]
                H[row,a*n+j]-=JX[a,i]
            if i<m and j==i+m: value-=1
            F[row]=value; row+=1
    for i in range(n):
        for j in range(i,n):
            value=0j
            bi=i+m if i<m else i-m; bj=j+m if j<m else j-m
            si=-1 if i<m else 1; sj=-1 if j<m else 1
            for a in range(n):
                ai=U[a,i]-X[a,i]; aj=U[a,j]-X[a,j]
                value+=ai*XJ[a,j]+aj*XJ[a,i]
                H[row,a*n+i]-=XJ[a,j]
                H[row,a*n+j]-=XJ[a,i]
                H[row,a*n+bj]+=sj*ai
                H[row,a*n+bi]+=si*aj
            F[row]=value; row+=1
    return F,H

@njit(cache=True, nogil=True)
def refine(x, u, n, iterations=5):
    """Newton proposal; successful return is not an existence certificate."""
    y=x.copy()
    for k in range(iterations):
        F,H=evaluate(y,u,n)
        try: delta=np.linalg.solve(H,F)
        except: return y,False
        y-=delta
        if not np.isfinite(y).all(): return y,False
        if k>=2 and np.max(np.abs(delta))<1e-14*(1+np.max(np.abs(y))): break
    return y,True


def forms(m):
    if not isinstance(m,int) or m<1:
        raise ValueError('The rank must be a positive integer')
    I=np.eye(m,dtype=np.complex128); Z=np.zeros_like(I)
    J=np.block([[Z,I],[-I,Z]])
    Q=np.block([[Z,I],[I,Z]])
    P=np.block([[I,1j*I],[1j*I,I]])/np.sqrt(2.)
    return J,Q,P
