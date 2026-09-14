"""Finite-instance utilities for TR-03; not global optimization certificates."""
from __future__ import annotations
from itertools import combinations
from typing import Sequence
import numpy as np
from numpy.typing import NDArray
Array = NDArray[np.float64]

def elementary(values: Sequence, degree: int):
    """Elementary symmetric polynomial, retaining Fraction arithmetic."""
    if degree < 0 or degree > len(values): return 0
    c = [1] + [0]*degree
    for v in values:
        for j in range(degree,0,-1): c[j] += v*c[j-1]
    return c[degree]

def clipping_threshold(sigma: Sequence, q: int):
    if not 0 <= q < len(sigma): raise ValueError('Invalid q')
    if any(x<=0 for x in sigma): raise ValueError('Positive spectrum required')
    if any(sigma[i]<sigma[i+1] for i in range(len(sigma)-1)):
        raise ValueError('Decreasing order required')
    h=sum(1/v for v in sigma[:q]); ans=None
    for s,v in enumerate(sigma[q:],1):
        h += 1/v; candidate=s/h
        ans=candidate if ans is None else max(ans,candidate)
    return ans

def inverse_trace(matrix: Array) -> float:
    e=np.linalg.eigvalsh((matrix+matrix.T)/2)
    if e[0] <= 2e-12*max(1.,float(np.max(abs(e)))): return float('inf')
    return float(np.sum(1/e))

def nystrom_error(matrix: Array, selected: Sequence[int], *, auxiliary_psd=False) -> float:
    """Pseudoinverse is allowed only for explicitly auxiliary PSD covariances.
    Singular limiting precision blocks must instead have infinite cost.
    """
    s=np.asarray(selected,dtype=int); b=matrix[np.ix_(s,s)]; c=matrix[:,s]
    pred=c@np.linalg.pinv(b,rcond=1e-12)@c.T if auxiliary_psd else c@np.linalg.solve(b,c.T)
    return float(np.trace(matrix-pred))

def orthogonal(n: int, rng: np.random.Generator) -> Array:
    q,r=np.linalg.qr(rng.normal(size=(n,n)))
    signs=np.sign(np.diag(r));signs[signs==0]=1
    return q*signs

def equal_diagonal(values: Sequence[float]) -> tuple[Array,Array]:
    """Real plane rotations make the diagonal equal to the spectral mean."""
    v=np.asarray(values,dtype=float); n=len(v); mean=float(v.mean())
    b=np.diag(v-mean); u=np.eye(n); tol=5e-13*max(1.,float(np.max(abs(v))))
    for i in range(n-1):
        diagonal=b.diagonal()
        z=next((j for j in range(i,n) if abs(diagonal[j])<=tol),None)
        if z is not None: p=z
        else:
            pos=[j for j in range(i,n) if diagonal[j]>0]
            neg=[j for j in range(i,n) if diagonal[j]<0]
            if not pos or not neg: raise ArithmeticError('Trace-zero rotation failed numerically')
            p,z=pos[0],neg[0]; ap,az=diagonal[p],diagonal[z]
            c=np.sqrt(-az/(ap-az)); s=np.sqrt(ap/(ap-az))
            r=np.eye(n);r[p,p]=r[z,z]=c;r[p,z]=-s;r[z,p]=s
            b=r.T@b@r;u=u@r
        if p!=i:
            order=np.arange(n);order[i],order[p]=order[p],order[i]
            b=b[np.ix_(order,order)];u=u[:,order]
    return b+mean*np.eye(n),u

def contrast_group(alpha: Sequence[float]) -> tuple[Array,Array]:
    v=np.asarray(alpha,dtype=float)
    if not len(v): return np.zeros((1,1)),np.ones(1)
    if np.any(v<=0): raise ValueError('Positive contrast eigenvalues required')
    c=float(v.sum()); h,o=equal_diagonal(np.r_[v,-c]);u=o[-1,:]
    b=h+c*np.outer(u,u)
    return (b+b.T)/2,u

def grouped_covariance(sigma: Sequence[float], k: int, q: int,
                       rng: np.random.Generator, level=100.) -> dict:
    sigma=np.sort(np.asarray(sigma,dtype=float))[::-1]
    j=k-q;n=j+len(sigma);N=2*k
    if n<4*k: raise ValueError('Require n >= 4k')
    head=sigma[:k+q];tail=sigma[k+q:]
    alpha=[tail[g::N] for g in range(N)]
    T=np.zeros((n,N));B=np.zeros((n,n));groups=[];labels=np.empty(n,dtype=int);off=0
    for g,v in enumerate(alpha):
        block,u=contrast_group(v);ix=np.arange(off,off+len(u));off+=len(u)
        T[ix,g]=u;B[np.ix_(ix,ix)]=block;labels[ix]=g;groups.append(ix)
    G=rng.normal(size=(N,j));H=G.T@G
    ev,o=np.linalg.eigh(H);ih=(o/np.sqrt(ev))@o.T
    U0=G@ih;V0=np.linalg.qr(U0,mode='complete')[0][:,j:];U=T@U0
    tail_cov=T@V0@np.diag(head)@V0.T@T.T+B
    return dict(full=level*(U@U.T)+tail_cov,reduced=level*(U@U.T)+B,
                U=U,U0=U0,V0=V0,G=G,H=H,T=T,contrast=B,groups=groups,
                labels=labels,c=np.array([v.sum() for v in alpha]),sigma=sigma,
                level=level,j=j,k=k,q=q)

def granted_posterior(data: dict, selected: Sequence[int]):
    selected=np.asarray(selected,dtype=int)
    lab,ct=np.unique(data['labels'][selected],return_counts=True)
    heavy=lab[ct>=2];single=lab[ct==1];aug=set(selected.tolist());j=data['j']
    for g in heavy: aug.update(data['groups'][g].tolist())
    if len(heavy):
        _,_,vt=np.linalg.svd(data['G'][heavy],full_matrices=True);Z=vt[len(heavy):].T
    else: Z=np.eye(j)
    W=data['G'][single]@Z;HZ=Z.T@data['H']@Z
    precision=HZ/data['level']
    if len(single): precision+=W.T@(W/data['c'][single,None])
    value=float(np.trace(HZ@np.linalg.inv(precision)))
    return value,np.array(sorted(aug),dtype=int),Z,W,heavy,single
