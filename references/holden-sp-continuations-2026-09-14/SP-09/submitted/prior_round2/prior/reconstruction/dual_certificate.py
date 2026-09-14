"""Numerical SOS search. Output must be reconstructed and checked exactly."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from scipy.linalg import null_space
from moments import build

def hvec(H):
    n=len(H);i,j=np.triu_indices(n,1)
    return np.r_[H.diagonal().real,np.sqrt(2)*H[i,j].real,np.sqrt(2)*H[i,j].imag]

def hmat(x):
    n=int(round(np.sqrt(len(x))));H=np.diag(x[:n]).astype(complex);i,j=np.triu_indices(n,1);m=len(i)
    H[i,j]=(x[n:n+m]+1j*x[n+m:])/np.sqrt(2);H[j,i]=H[i,j].conj();return H

def mblocks(v,sizes):
    out=[];off=0
    for n in sizes:
        out.append(v[off:off+n*n].reshape(n,n)+1j*v[off+n*n:off+2*n*n].reshape(n,n));off+=2*n*n
    return out

def flatten(Hs):return np.concatenate([np.r_[H.real.ravel(),H.imag.ravel()] for H in Hs])

def example():
    a=np.array([1,(4+5j*np.sqrt(3))/13,(-1+2j*np.sqrt(3))/13]);v=np.sqrt([5/8,1/4,1/8]);R=np.eye(3)-2*np.outer(v,v)
    Ps=[np.diag([1,0,0]),np.diag([0,1,0])];Ps += [R@P@R for P in Ps]
    return a,Ps

def evaluate(w,Ps):
    X=np.eye(3,dtype=complex)
    for j in w:X=X@Ps[j]
    return X

def setup(degree=4,epsilon=0):
    a,Ps=example();t=np.sqrt(27/13);f,A,sizes,keys,B,L=build(a,-a,t,degree)
    y=np.zeros(len(keys))
    for (w,typ),j in keys.items():
        z=np.trace(evaluate(w,Ps))/3;y[j]=z.real if typ=='r' else z.imag
    Ms=mblocks(f+A@y,sizes);Ns=[]
    for M in Ms:
        d,v=np.linalg.eigh(M);Ns.append(v[:,d<1e-9])
    sizesN=[N.shape[1] for N in Ns]
    D=np.diag(a)+sum((a[i]-a[2])*Ps[i+2] for i in range(2))+a[2]*np.eye(3)
    H=t*t*np.eye(3)-D.conj().T@D
    lw=[(),(0,),(1,),(2,),(3,)]
    Rmap=np.column_stack([(H@evaluate(w,Ps)).ravel() for w in lw]);ker=null_space(Rmap,rcond=1e-10)
    tr=np.array([np.trace(evaluate(w,Ps))/3 for w in lw]);z=ker@(ker.conj().T@tr.conj());z/=tr@z
    Q=sum(z[i]*evaluate(w,Ps) for i,w in enumerate(lw))
    assert abs(np.trace(Q)/3-1)<1e-8 and np.linalg.norm(H@Q)<1e-8
    coeff=np.zeros(len(L),complex)
    for zi,w in zip(z,lw):coeff[L.index(w)]=zi
    Yfixed=[epsilon*(N@N.conj().T) for N in Ns];Yfixed[1]+=np.outer(coeff,coeff.conj())
    fix=flatten(Yfixed);F=np.column_stack([f,A]);rhs=-F.T@fix
    Fs=[mblocks(F[:,j],sizes) for j in range(F.shape[1])]
    C=np.array([np.concatenate([hvec(N.conj().T@M@N) for N,M in zip(Ns,blocks)]) for blocks in Fs])
    return C,rhs,sizesN,(Ns,F,Yfixed,coeff,keys,Ps,sizes)

def projectcone(x,sizes):
    out=np.zeros_like(x);off=0
    for n in sizes:
        X=hmat(x[off:off+n*n]);d,v=np.linalg.eigh(X);X=(v*np.maximum(d,0))@v.conj().T;out[off:off+n*n]=hvec(X);off+=n*n
    return out

def run(degree=4,steps=50000,epsilon=0):
    import time
    st=time.monotonic();C,b,sizes,data=setup(degree,epsilon)
    u,s,vh=np.linalg.svd(C,full_matrices=False);rank=np.sum(s>s[0]*1e-11);u=u[:,:rank];s=s[:rank];V=vh[:rank].T
    b0=V@((u.T@b)/s)
    print('setup',degree,sizes,'rank',rank,'incompatibility',np.linalg.norm(C@b0-b),'seconds',time.monotonic()-st,flush=True)
    z=b0.copy()
    for it in range(steps):
        x=z+V@(V.T@(b0-z));y=projectcone(2*x-z,sizes);z+=y-x
        if it%5000==0 or it==steps-1:
            err=np.linalg.norm(y-x);lin=np.linalg.norm(C@y-b)
            print('iteration',it,'error',err,'linear',lin,'norm',np.linalg.norm(y),'seconds',time.monotonic()-st,flush=True)
            if err<1e-9:break
    Ns,F,Yfixed,coeff,keys,Ps,origsizes=data;Ys=[];off=0
    for N,n,Fx in zip(Ns,sizes,Yfixed):
        Ys.append(N@hmat(y[off:off+n*n])@N.conj().T+Fx);off+=n*n
    out={'Y'+str(i):Y for i,Y in enumerate(Ys)};out['coeff']=coeff;out['residual']=F.T@flatten(Ys)
    np.savez('dual_degree'+str(degree)+'.npz',**out)
    return out

if __name__=='__main__':run()
