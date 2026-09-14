"""Numerical kernels for the regular SP-03 chart; NOT certified continuation.

All four Q-coordinate data blocks may vary. Every
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
def evaluate(a, U, du):
    m=U.shape[0]//2
    ua=U[:m,:m].copy();ub=U[:m,m:].copy();uc=U[m:,:m].copy();ud=U[m:,m:].copy()
    da=du[:m,:m].copy();db=du[:m,m:].copy();dc=du[m:,:m].copy();dd=du[m:,m:].copy()
    m=ua.shape[0];d=m*m;k=m*(m+1)//2
    A=a.reshape((m,m));Y=np.linalg.inv(A).T.copy()
    pp=np.empty(k,np.int64);qq=np.empty(k,np.int64);r=0
    for i in range(m):
        for j in range(i,m):pp[r]=i;qq[r]=j;r+=1
    V2=2*A-ua
    L=np.empty((k,k),np.complex128);Lp=np.empty_like(L);b=np.zeros(k,np.complex128);c=np.zeros(k,np.complex128);bp=np.zeros_like(b);cp=np.zeros_like(c)
    for r in range(k):
        s=pp[r];t=qq[r]
        for i in range(m):
            b[r]+=A[i,s]*uc[i,t]
            c[r]+=A[t,i]*ub[s,i]
            bp[r]+=A[i,s]*dc[i,t];cp[r]+=A[t,i]*db[s,i]
            if s!=t:
                b[r]+=A[i,t]*uc[i,s]
                c[r]+=A[s,i]*ub[t,i]
                bp[r]+=A[i,t]*dc[i,s];cp[r]+=A[s,i]*db[t,i]
        for z in range(k):
            p=pp[z];q=qq[z]
            v=A[p,s]*V2[q,t];vp=-A[p,s]*da[q,t]
            if s!=t:
                v+=A[p,t]*V2[q,s];vp-=A[p,t]*da[q,s]
            if p!=q:
                v+=A[q,s]*V2[p,t];vp-=A[q,s]*da[p,t]
                if s!=t:
                    v+=A[q,t]*V2[p,s];vp-=A[q,t]*da[p,s]
            L[r,z]=v;Lp[r,z]=vp
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
    tp=Li@(bp-Lp@tv);sp=Li.T@(cp-Lp.T@sv)
    gp=HS@sp+HT@tp+(-T@da@S-dc@S-T@db-dd+Y@da.T@Y).ravel()
    return g.ravel(),H,gp,S,T


@njit(cache=True,nogil=True)
def refine(a,U):
    a=a.copy();best=a.copy();quality=1e300;last=1e300;zero=np.zeros_like(U)
    m=U.shape[0]//2
    for _ in range(7):
        try:
            g,H,gp,S,T=evaluate(a,U,zero);delta=np.linalg.solve(H,g)
        except:return best,quality<1e-4
        q=norm_inf(delta)/(1+norm_inf(a))
        if not np.isfinite(q):break
        if q<quality:quality=q;best=a.copy()
        if q<3e-12:break
        if q>last*1.8 and quality<1e-5:break
        a-=delta;last=q
        if not np.isfinite(a).all():break
    try:
        g,H,gp,S,T=evaluate(best,U,zero)
        A=best.reshape(m,m);Y=np.linalg.inv(A).T
        ua=U[:m,:m];ub=U[:m,m:];uc=U[m:,:m];ud=U[m:,m:]
        scale=(1+m*m*norm_inf(T)*norm_inf(4*A-ua)*norm_inf(S)
               +m*norm_inf(uc)*norm_inf(S)+m*norm_inf(T)*norm_inf(ub)
               +norm_inf(ud)+m*m*norm_inf(Y)**2*norm_inf(ua))
    except:return best,False
    return best,quality<1e-4 and norm_inf(g)/scale<1e-8

@njit(cache=True,nogil=True)
def track(a0,u0,u1):
    a=a0.copy();du=u1-u0;t=0.;h=.015;steps=0
    while t<1.:
        steps+=1
        if steps>1800:return a,False,steps
        try:
            g,H,gp,S,T=evaluate(a,u0+t*du,du);v=np.linalg.solve(H,-gp)
        except:return a,False,steps
        h=min(h,1.-t);pred=a+h*v;y=pred.copy();ok=False;olderr=1e300
        for it in range(7):
            try:
                g,H,gp,S,T=evaluate(y,u0+(t+h)*du,du);delta=np.linalg.solve(H,g)
            except:break
            err=norm_inf(delta)
            if not np.isfinite(err):break
            y-=delta
            if err<1e-5*(1+norm_inf(y)):ok=True;break
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
    a,ok=refine(a,u1)
    return a,ok,steps

@njit(cache=True,nogil=True)
def triangle(a,u,v,w):
    y,ok,s1=track(a,u,v)
    if not ok:return y,False,s1
    y,ok,s2=track(y,v,w)
    if not ok:return y,False,s1+s2
    y,ok,s3=track(y,w,u)
    return y,ok,s1+s2+s3

def lift(a,U):
    m=U.shape[0]//2;g,H,gp,S,T=evaluate(a,U,np.zeros_like(U));A=a.reshape(m,m)
    return np.block([[A,A@S],[T@A,T@A@S+np.linalg.inv(A).T]]),g,H
