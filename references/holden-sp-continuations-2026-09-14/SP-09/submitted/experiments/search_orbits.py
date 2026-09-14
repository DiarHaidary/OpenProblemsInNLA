"""Numerical exploration only; objective values are upper bounds, not proofs."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize,linear_sum_assignment

def unpack(x):
 n=int(round(np.sqrt(len(x))));H=np.diag(x[:n]).astype(complex);i,j=np.triu_indices(n,1);m=len(i)
 H[i,j]=x[n:n+m]+1j*x[n+m:];H[j,i]=H[i,j].conj();return H

def packgrad(H):
 n=len(H);i,j=np.triu_indices(n,1);return np.r_[H.diagonal().real,2*H[i,j].real,2*H[i,j].imag]

def haar(n,rng):return np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))[0]

def value(a,b,U):return float(np.linalg.norm((np.asarray(a)[:,None]-np.asarray(b)[None,:])*U,2))

def bottleneck(a,b):
 C=abs(np.asarray(a)[:,None]-np.asarray(b)[None,:]);cs=np.unique(C);lo=0;hi=len(cs)-1
 while lo<hi:
  mid=(lo+hi)//2;i,j=linear_sum_assignment(C>cs[mid])
  if (C[i,j]<=cs[mid]).all():hi=mid
  else:lo=mid+1
 i,j=linear_sum_assignment(C>cs[lo]);U=np.zeros(C.shape,complex);U[i,j]=1
 return float(cs[lo]),U

def cost_gradient(x,C,Ubase,tau,extras=False):
 H=unpack(x);lam,V=eigh(H,check_finite=False);U=Ubase@(V*np.exp(1j*lam))@V.conj().T
 W=C*U;d,Z=eigh(W.conj().T@W,check_finite=False);p=np.exp((d-d[-1])/tau);p/=p.sum()
 f=d[-1]+tau*np.log(np.exp((d-d[-1])/tau).sum());GW=2*(W@Z*p)@Z.conj().T;GU=C.conj()*GW
 delta=lam[:,None]-lam[None,:];D=1j*np.exp(.5j*(lam[:,None]+lam[None,:]))*np.sinc(delta/(2*np.pi))
 GH=V@(D.conj()*(V.conj().T@Ubase.conj().T@GU@V))@V.conj().T;GH=(GH+GH.conj().T)/2
 if extras:return float(f),packgrad(GH),GW,U
 return float(f),packgrad(GH)

def optimize(a,b,U,taus=(.01,.002,.0004,.00008,.000016),maxiter=300):
 a=np.asarray(a);b=np.asarray(b);C=a[:,None]-b[None,:];scale=max(1.,abs(C).max()**2);best=(value(a,b,U),U.copy())
 for tau in taus:
  r=minimize(cost_gradient,np.zeros(len(a)**2),args=(C,U,tau*scale),jac=True,method='L-BFGS-B',options={'maxiter':maxiter,'ftol':1e-13,'gtol':1e-9,'maxls':40})
  l,v=eigh(unpack(r.x));U=U@(v*np.exp(1j*l))@v.conj().T
  f=value(a,b,U)
  if f<best[0]:best=f,U.copy()
 return best
