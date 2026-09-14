"""Tracial moment construction for two normal three-point spectra.
Exploratory use only: floating-point feasibility is not an exact certificate.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from itertools import product
from scipy.linalg import qr

def reduce(w,cyclic=False):
    w=list(w)
    while True:
        changed=False
        for i in range(len(w)-1):
            if w[i]//2==w[i+1]//2:
                if w[i]!=w[i+1]:return None
                del w[i+1];changed=True;break
        if changed:continue
        if cyclic and len(w)>1 and w[0]//2==w[-1]//2:
            if w[0]!=w[-1]:return None
            del w[-1];continue
        break
    if cyclic and w:w=min(tuple(w[i:]+w[:i]) for i in range(len(w)))
    return tuple(w)

def canon(w):
    w=reduce(w,True)
    if w is None:return None,0
    wr=reduce(w[::-1],True)
    return (w,1) if w<=wr else (wr,-1)

def basis(degree):
    return [()] + [w for l in range(1,degree+1) for w in product(range(4),repeat=l) if reduce(w)==w]

def addpoly(d,w,c):
    w=reduce(w)
    if w is not None:d[w]=d.get(w,0)+c

def mul(p,q):
    d={}
    for u,a in p.items():
        for v,b in q.items():addpoly(d,u+v,a*b)
    return d

def adj(p):return {w[::-1]:np.conj(c) for w,c in p.items()}

def build(a,b,t,degree=2,tracep=(1/3,1/3),traceq=(1/3,1/3)):
    B=basis(degree);L=basis(degree-1)
    pa={():a[2],(0,):a[0]-a[2],(1,):a[1]-a[2]}
    pb={():b[2],(2,):b[0]-b[2],(3,):b[1]-b[2]}
    d=pa.copy()
    for w,c in pb.items():d[w]=d.get(w,0)-c
    h1=mul(adj(d),d);h2=mul(d,adj(d))
    mats=[(B,{():1}),(L,{w:-c for w,c in h1.items()}),(L,{w:-c for w,c in h2.items()})]
    for _,poly in mats[1:]:poly[()]=poly.get((),0)+t*t
    fixed={():1,(0,):tracep[0],(1,):tracep[1],(2,):traceq[0],(3,):traceq[1]}
    keys={}
    for bs,p in mats:
        for u in bs:
            for v in bs:
                for w in p:
                    c,sgn=canon(u[::-1]+w+v)
                    if c is not None and c not in fixed:
                        keys[(c,'r')]=0
                        if reduce(c[::-1],True)!=c:keys[(c,'i')]=0
    keys={key:j for j,key in enumerate(sorted(keys))};nv=len(keys);tensors=[]
    for bs,p in mats:
        T=np.zeros((len(bs),len(bs),nv+1),complex)
        for i,u in enumerate(bs):
            for j,v in enumerate(bs):
                for w,c in p.items():
                    z,sgn=canon(u[::-1]+w+v)
                    if z is None:continue
                    if z in fixed:T[i,j,0]+=c*fixed[z]
                    else:
                        T[i,j,1+keys[(z,'r')]]+=c
                        if (z,'i') in keys:T[i,j,1+keys[(z,'i')]]+=c*sgn*1j
        assert np.max(abs(T-T.swapaxes(0,1).conj()))<1e-12
        tensors.append(T)
    F=np.concatenate([np.concatenate([T.real.reshape(-1,nv+1),T.imag.reshape(-1,nv+1)]) for T in tensors])
    return F[:,0],F[:,1:],[len(bs) for bs,p in mats],keys,B,L
