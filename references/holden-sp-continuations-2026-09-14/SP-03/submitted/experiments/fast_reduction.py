"""Numerical kernels for the regular SP-03 chart; NOT certified continuation.

The first three Q-coordinate data blocks are fixed. Only U_d varies. Every
transpose is ordinary (complex bilinear). Final root certification is separate.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
from numba import njit

@njit(cache=True, nogil=True)
def norm_inf(x):
    return np.max(np.abs(x))

@njit(cache=True, nogil=True)
def evaluate(a, ua, ub, uc, ud):
    m=ua.shape[0];d=m*m;k=m*(m+1)//2
    A=a.reshape((m,m));Y=np.linalg.inv(A).T.copy()
    pp=np.empty(k,np.int64);qq=np.empty(k,np.int64);r=0
    for i in range(m):
        for j in range(i,m):pp[r]=i;qq[r]=j;r+=1
    V2=2*A-ua
    L=np.empty((k,k),np.complex128);b=np.zeros(k,np.complex128);c=np.zeros(k,np.complex128)
    for r in range(k):
        s=pp[r];t=qq[r]
        for i in range(m):
            b[r]+=A[i,s]*uc[i,t]
            c[r]+=A[t,i]*ub[s,i]
            if s!=t:
                b[r]+=A[i,t]*uc[i,s]
                c[r]+=A[s,i]*ub[t,i]
        for z in range(k):
            p=pp[z];q=qq[z]
            v=A[p,s]*V2[q,t]
            if s!=t:v+=A[p,t]*V2[q,s]
            if p!=q:
                v+=A[q,s]*V2[p,t]
                if s!=t:v+=A[q,t]*V2[p,s]
            L[r,z]=v
    Li=np.linalg.inv(L)
    tv=Li@b;sv=Li.T@c
    S=np.zeros((m,m),np.complex128);T=np.zeros_like(S)
    for r in range(k):
        i=pp[r];j=qq[r];S[i,j]=S[j,i]=sv[r];T[i,j]=T[j,i]=tv[r]
    V=4*A-ua;W=Y@ua.T@Y
    AA=T@V-uc;BB=V@S-ub
    g=AA@S-T@ub-ud+W
    HS=np.zeros((d,k),np.complex128);HT=np.zeros((d,k),np.complex128)
    for r in range(k):
        s=pp[r];t=qq[r]
        for i in range(m):
            HS[i*m+t,r]+=AA[i,s]
            HT[s*m+i,r]+=BB[t,i]
            if s!=t:
                HS[i*m+s,r]+=AA[i,t]
                HT[t*m+i,r]+=BB[s,i]
    R=(HT@Li)@HS.T
    H=np.empty((d,d),np.complex128)
    for a0 in range(m):
        for b0 in range(m):
            p=a0*m+b0
            for i in range(m):
                for j in range(m):
                    q=i*m+j
                    H[p,q]=4*T[a0,i]*S[j,b0]-Y[a0,j]*W[i,b0]-W[a0,j]*Y[i,b0]-R[p,q]-R[q,p]
    return g.ravel(),H,S,T

@njit(cache=True, nogil=True)
def refine(a,ua,ub,uc,ud):
    a=a.copy()
    for _ in range(8):
        try:
            g,H,S,T=evaluate(a,ua,ub,uc,ud)
            delta=np.linalg.solve(H,g)
        except:return a,False
        a-=delta
        if not np.isfinite(a).all():return a,False
        if norm_inf(delta)<2e-13*(1+norm_inf(a)):break
    try:g,H,S,T=evaluate(a,ua,ub,uc,ud)
    except:return a,False
    return a,norm_inf(g)<1e-7

@njit(cache=True, nogil=True)
def track(a0, ua,ub,uc, u0,u1):
    a=a0.copy();du=u1-u0;t=0.;h=.015;steps=0
    while t<1.:
        steps+=1
        if steps>2000:return a,False,steps
        try:
            g,H,S,T=evaluate(a,ua,ub,uc,u0+t*du)
            v=np.linalg.solve(H,du.ravel())
        except:return a,False,steps
        h=min(h,1.-t);pred=a+h*v;y=pred.copy();ok=False;olderr=1e300
        for it in range(7):
            try:
                g,H,S,T=evaluate(y,ua,ub,uc,u0+(t+h)*du)
                delta=np.linalg.solve(H,g)
            except:break
            err=norm_inf(delta)
            if not np.isfinite(err):break
            y-=delta
            if err<1e-6*(1+norm_inf(y)):ok=True;break
            if it>=2 and err>olderr*.85:break
            olderr=err
        if ok:
            corr=norm_inf(y-pred)/(1+norm_inf(y))
            if corr>.055:h*=.5
            else:
                a=y;t+=h
                if corr<.001:h*=1.7
                elif corr<.009:h*=1.3
                elif corr>.035:h*=.75
                h=min(h,.18)
        else:h*=.5
        if h<1e-10 or norm_inf(a)>1e8:return a,False,steps
    a,ok=refine(a,ua,ub,uc,u1)
    return a,ok,steps

@njit(cache=True,nogil=True)
def triangle(a,ua,ub,uc,u,v,w):
    y,ok,s1=track(a,ua,ub,uc,u,v)
    if not ok:return y,False,s1
    y,ok,s2=track(y,ua,ub,uc,v,w)
    if not ok:return y,False,s1+s2
    y,ok,s3=track(y,ua,ub,uc,w,u)
    return y,ok,s1+s2+s3


def lift(a,ua,ub,uc,ud):
    m=ua.shape[0]
    g,H,S,T=evaluate(a,ua,ub,uc,ud)
    A=a.reshape(m,m)
    X=np.block([[A,A@S],[T@A,T@A@S+np.linalg.inv(A).T]])
    return X,g,H
