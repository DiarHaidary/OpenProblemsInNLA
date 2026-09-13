"""Finite tensor calculations for the even-power continuation.

This is a proof-diagnostic library, not an implementation of Rothvoss's
partial-coloring oracle or of the asymptotic coreset construction.
"""
from __future__ import annotations
from functools import lru_cache
from itertools import product
from math import factorial, sqrt
from typing import Dict, Tuple
import numpy as np

@lru_cache(None)
def multiindices(dim: int, degree: int) -> tuple[tuple[int, ...], ...]:
    if dim < 1 or degree < 0:
        raise ValueError('Invalid tensor dimension or degree')
    if dim == 1:
        return ((degree,),)
    return tuple((a,)+b for a in range(degree+1)
                 for b in multiindices(dim-1, degree-a))

def multinomial(alpha: tuple[int, ...]) -> int:
    value = factorial(sum(alpha))
    for a in alpha:
        value //= factorial(a)
    return value

def sympower(x: np.ndarray, degree: int) -> np.ndarray:
    """Coordinates of x^{tensor degree} in the orthonormal symmetric basis."""
    x = np.asarray(x, dtype=float)
    return np.array([sqrt(multinomial(a))*np.prod(x**np.array(a))
                     for a in multiindices(len(x), degree)])

def root_on_range(M: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return range square root R and left whitener W: R R.T=M, W M W.T=I."""
    vals, U = np.linalg.eigh((M+M.T)/2)
    threshold = 2e-10*max(float(vals[-1]), 1e-20)
    keep = vals > threshold
    if not np.any(keep):
        return np.zeros((len(M),0)), np.zeros((0,len(M)))
    R=U[:,keep]*np.sqrt(vals[keep])
    W=(U[:,keep]/np.sqrt(vals[keep])).T
    return R,W

class Features:
    def __init__(self, B: np.ndarray, C: np.ndarray, omega: np.ndarray, s: int):
        if s < 2 or B.ndim != 2 or C.ndim != 2 or len(B) != len(C):
            raise ValueError('Inconsistent even-power feature input')
        if np.any(omega<=0) or not np.isclose(sum(omega),1):
            raise ValueError('omega must be a positive probability vector')
        self.B,self.C,self.omega,self.s=B,C,omega,s
        self.n,self.k=B.shape; self.q=C.shape[1]
        self.r=np.linalg.norm(C,axis=1)
        self.E={}; self.F={}; self.Mroot={}; self.Nroot={}
        self.M={}; self.N={}; self.h={}
        self.Bp={j:np.array([sympower(b,j) for b in B]) for j in range(s+1)}
        self.Cp={t:np.array([sympower(c,t) for c in C]) for t in range(2*s+1)}
        for l in range(1,s+1):
            raw=self.Bp[l]; M=raw.T@(omega[:,None]*raw)
            R,W=root_on_range(M)
            self.M[l]=M; self.Mroot[l]=R
            self.E[l]=(raw@W.T)*np.sqrt(omega[:,None])
        for j in range(s):
            for t in range(1,2*s+1):
                raw=self.Bp[j]
                N=raw.T@((omega*self.r**(2*t))[:,None]*raw)
                R,W=root_on_range(N)
                self.N[j,t]=N; self.Nroot[j,t]=R; self.h[j,t]=R.shape[1]
                head=raw@W.T
                self.F[j,t]=np.array([sqrt(omega[i])*np.kron(head[i],self.Cp[t][i])
                                      for i in range(self.n)])
        probs=[omega]
        for E in self.E.values():
            if E.shape[1]: probs.append(np.sum(E*E,axis=1)/E.shape[1])
        for key,F in self.F.items():
            if self.h[key]: probs.append(np.sum(F*F,axis=1)/self.h[key])
        self.num_probabilities=len(probs)
        self.pi=np.mean(probs,axis=0)

# Sparse multivariate polynomials, used only to construct finite query maps.
Poly=Dict[Tuple[int,...],float]
def add(P: Poly,Q: Poly) -> Poly:
    R=P.copy()
    for a,v in Q.items(): R[a]=R.get(a,0.0)+v
    return {a:v for a,v in R.items() if abs(v)>1e-16}
def scale(P: Poly,c: float) -> Poly:
    return {a:v*c for a,v in P.items()}
def mul(P: Poly,Q: Poly) -> Poly:
    R={}
    for a,v in P.items():
        for b,w in Q.items():
            ab=tuple(x+y for x,y in zip(a,b)); R[ab]=R.get(ab,0.0)+v*w
    return {a:v for a,v in R.items() if abs(v)>1e-16}
def power(P: Poly,n: int,dim: int) -> Poly:
    if n<0: raise ValueError('Negative polynomial exponent')
    R={(0,)*dim:1.0}
    for _ in range(n): R=mul(R,P)
    return R

def query_polynomials(V: np.ndarray,W: np.ndarray,Ptail: np.ndarray):
    k=V.shape[1]; q=W.shape[1]; dim=k+q
    def linear(coeff):
        ret={}
        for i,c in enumerate(coeff):
            a=[0]*dim; a[i]=1
            if c: ret[tuple(a)]=float(c)
        return ret
    VB=[linear(np.r_[row,np.zeros(q)]) for row in V]
    WC=[linear(np.r_[np.zeros(k),row]) for row in W]
    A={}; X={}; R={}
    for vb,wc in zip(VB,WC):
        A=add(A,mul(vb,vb)); X=add(X,mul(vb,wc))
    for i in range(q):
        for j in range(q):
            a=[0]*dim;a[k+i]+=1;a[k+j]+=1
            R[tuple(a)]=R.get(tuple(a),0.)+float(Ptail[i,j])
    return A,X,R,VB

def coefficient_map(polys: list[Poly],k: int,q: int,j: int,t: int) -> np.ndarray:
    heads=multiindices(k,j); tails=multiindices(q,t)
    ret=np.zeros((len(polys),len(heads)*len(tails)))
    for row,P in enumerate(polys):
        for i,a in enumerate(heads):
            for h,b in enumerate(tails):
                ret[row,i*len(tails)+h]=P.get(a+b,0.)/sqrt(multinomial(a)*multinomial(b))
    return ret

def monomials(s: int):
    for a in range(s+1):
        for b in range(s-a+1):
            for c in range(s-a-b+1):
                yield a,b,c,s-a-b-c

def protected_indices(s: int,a: int,b: int,c: int,d: int):
    if a<1 or b+c<1 or a+b+c+d!=s:
        raise ValueError('Not a protected-family monomial')
    l=min(2*a,s); nu=l%2; h=l//2; e=a-(l+1)//2
    j=2*a+b-l;t=b+2*c
    return l,nu,h,e,j,t

def protected_maps(feat: Features,V,W,Ptail,a,b,c,d):
    s,k,q=feat.s,feat.k,feat.q; dim=k+q
    A,X,R,VB=query_polynomials(V,W,Ptail)
    l,nu,h,e,j,t=protected_indices(s,a,b,c,d)
    Lbase=power(A,h,dim)
    Rbase=mul(mul(power(A,e,dim),power(X,b,dim)),power(R,c,dim))
    Lpolys=[Lbase] if not nu else [mul(Lbase,v) for v in VB]
    Rpolys=[Rbase] if not nu else [mul(Rbase,v) for v in VB]
    L=coefficient_map(Lpolys,k,q,l,0)@feat.Mroot[l]
    RR=coefficient_map(Rpolys,k,q,j,t)
    RR=RR@np.kron(feat.Nroot[j,t],np.eye(len(multiindices(q,t))))
    return L,RR,(l,nu,h,e,j,t)
