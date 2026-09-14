"""Numerical implementations of the proved polygon completion formulas.

These functions are diagnostic, not exact real-arithmetic certificates.
"""
import numpy as np


def _lambdas(values):
    x=np.asarray(values,dtype=float)
    if x.ndim!=1 or len(x)<3 or len(x)%2==0:
        raise ValueError('An odd list of at least three eigenvalues is required')
    if not np.isfinite(x).all() or abs(x[0]-1)>1e-10 or np.max(np.abs(x))>1+1e-10:
        raise ValueError('Require lambda_0=1 and all eigenvalues in [-1,1]')
    return np.clip(x,-1,1)


def formula(values,R=1.0):
    lam=_lambdas(values)
    if not np.isfinite(R) or R<=0:raise ValueError('R must be positive')
    th=np.arccos(lam[1:])/2
    M=max(np.cos(th[0]),np.cos(th[-1]),np.max(np.abs(np.cos(th[:-1]+th[1:]))))
    return float(2*R*M)


def canonical(values,C=None,R=1.0):
    lam=_lambdas(values);p=len(lam);n=2*p-1
    if C is None:
        C=np.zeros((p-1,p-1),complex)
        for j in range(p-2):C[j+1,j]=-R
    C=np.asarray(C,complex)
    if C.shape!=(p-1,p-1) or not np.isfinite(C).all():raise ValueError('Invalid complementary matrix')
    D=np.zeros((n,n),complex);U=np.zeros((n,n),complex)
    for j in range(p):D[(j+1)%p,j]=R
    D[p:,p:]=C
    U[np.arange(p),np.arange(p)]=lam
    for j in range(1,p):
        k=p+j-1;s=np.sqrt(max(0,1-lam[j]**2))
        U[k,k]=-lam[j];U[j,k]=U[k,j]=s
    return D,U


def optimal_angles(p):
    if not isinstance(p,int) or p<3 or p%2==0:raise ValueError('p must be odd and >=3')
    gamma=np.pi/(2*p)
    return np.array([0]+[(np.pi/2-j*gamma if j%2 else j*gamma) for j in range(1,p)])


def compressed_optimal(p):
    if not isinstance(p,int) or p<3 or p%2==0:raise ValueError('p must be odd and >=3')
    j=np.arange(p)
    return (-1.0)**j*(1-2*j/p)


def twirl_overlap(X,v):
    X=np.asarray(X,complex);v=np.asarray(v,complex);p=len(v)
    if X.shape!=(p,p):raise ValueError('Dimension mismatch')
    if np.linalg.norm(X-X.conj().T)>1e-9 or np.linalg.norm(X@v-v)>1e-9:
        raise ValueError('Require Hermitian X and Xv=v')
    if abs(np.vdot(v,v)-1)>1e-9:raise ValueError('v must be unit')
    out=np.zeros_like(X)
    for g in range(p):
        w=np.roll(v,g);Y=np.roll(np.roll(X,g,axis=0),g,axis=1)
        out+=w.conj()[:,None]*Y*w[None,:]
    return out


def fourier(p):
    j=np.arange(p)
    return np.exp(2j*np.pi*np.outer(j,j)/p)/np.sqrt(p)


def norm(M):return float(np.linalg.norm(M,2))
