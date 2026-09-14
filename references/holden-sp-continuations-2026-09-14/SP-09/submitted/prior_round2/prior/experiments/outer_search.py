"""Joint spectrum/unitary search for repeated-spectrum counterexample candidates.
SLSQP output is heuristic and cannot establish a lower bound on base distance.
"""
from search_orbits import *
from scipy.optimize._numdiff import approx_derivative
import json,time

def spec_unpack(x,n):
 a=x[:n].astype(complex);off=n;a[1:]+=1j*x[off:off+n-1];off+=n-1
 b=np.zeros(n,complex);b[:-1]=x[off:off+n-1];off+=n-1;b[:-1]+=1j*x[off:off+n-1]
 return a,b

def spec_pack(a,b):return np.r_[a.real,a[1:].imag,b[:-1].real,b[:-1].imag]
def spec_grad(ga,gb):return np.r_[ga.real,ga[1:].imag,gb[:-1].real,gb[:-1].imag]

def joint(x,Ubase,n,k,tau):
 d=n*k;xx=x[:d*d];a,b=spec_unpack(x[d*d:],n);ak=np.repeat(a,k);bk=np.repeat(b,k)
 f,gh,GW,U=cost_gradient(xx,ak[:,None]-bk[None,:],Ubase,tau,extras=True)
 H=GW*U.conj();ga=H.sum(axis=1).reshape(n,k).sum(axis=1);gb=-H.sum(axis=0).reshape(n,k).sum(axis=1)
 return f,np.r_[gh,spec_grad(ga,gb)]

def cons(x,n,k,p,q):
 a,b=spec_unpack(x[(n*k)**2:],n);return (abs(a[:p,None]-b[None,:q])**2-1).ravel()

def consjac(x,n,k,p,q):
 a,b=spec_unpack(x[(n*k)**2:],n);rows=[]
 for i in range(p):
  for j in range(q):
   ga=np.zeros(n,complex);gb=ga.copy();ga[i]=2*(a[i]-b[j]);gb[j]=-ga[i]
   rows.append(np.r_[np.zeros((n*k)**2),spec_grad(ga,gb)])
 return np.array(rows)

def outer(a,b,U,k,p,q):
 n=len(a);c=b[-1];a=a-c;b=b-c;rot=np.exp(-1j*np.angle(a[0]));a*=rot;b*=rot
 scale=np.min(abs(a[:p,None]-b[None,:q]));a/=scale;b/=scale
 for tau in [.01,.002,.0004,.00008,.000016]:
  x0=np.r_[np.zeros((n*k)**2),spec_pack(a,b)]
  r=minimize(joint,x0,args=(U,n,k,tau),jac=True,method='SLSQP',constraints=[{'type':'ineq','fun':lambda x:cons(x,n,k,p,q),'jac':lambda x:consjac(x,n,k,p,q)}],options={'maxiter':500,'ftol':1e-11,'disp':False})
  l,v=eigh(unpack(r.x[:(n*k)**2]));U=U@(v*np.exp(1j*l))@v.conj().T;a,b=spec_unpack(r.x[(n*k)**2:],n)
 scale=np.min(abs(a[:p,None]-b[None,:q]));a/=scale;b/=scale
 return a,b,U,value(np.repeat(a,k),np.repeat(b,k),U)

if __name__=='__main__':
 rng=np.random.default_rng(2026091309);t0=time.monotonic();a0=np.array([1,(4+5j*np.sqrt(3))/13,(-1+2j*np.sqrt(3))/13]);v=np.sqrt([5/8,1/4,1/8]);R=np.eye(3)-2*np.outer(v,v)
 log=open('outer_log.jsonl','w',buffering=1)
 for case in range(60):
  n=4;k=2;p=2;q=3
  c=-a0[case%2]+.1*(rng.normal()+1j*rng.normal())
  a=np.r_[a0,c];b=np.r_[-a0[:2],c,-a0[2]]
  baseU=np.eye(4,dtype=complex);baseU[:3,:3]=R;baseU=baseU[:,[0,1,3,2]]
  U=np.kron(baseU,np.eye(k))
  if case%3==1:
   H=unpack(.25*rng.normal(size=(n*k)**2));l,v=eigh(H);U=U@(v*np.exp(1j*l))@v.conj().T
  elif case%3==2:U=haar(n*k,rng)
  a,b,U,amp=outer(a,b,U,k,p,q)
  best=bottleneck(a,b)
  for trial in range(24):
   vv,UU=optimize(a,b,baseU if trial==0 else haar(n,rng),taus=(.01,.002,.0004,.00008,.000016,.0000032),maxiter=500)
   if vv<best[0]:best=vv,UU
  lift=optimize(np.repeat(a,k),np.repeat(b,k),U,taus=(.00008,.000016,.0000032),maxiter=600)
  if lift[0]<amp:amp,U=lift
  item={'case':case,'a':[[z.real,z.imag] for z in a],'b':[[z.real,z.imag] for z in b],'base_upper':best[0],'amplified_upper':amp,'candidate_gap':best[0]-amp,'matching':bottleneck(a,b)[0],'seconds':time.monotonic()-t0}
  log.write(json.dumps(item)+'\n')
  np.savez('outer_case'+str(case)+'.npz',a=a,b=b,baseU=best[1],ampU=U)
  print(case,'base',best[0],'amp',amp,'gap',best[0]-amp,'match',item['matching'],'time',item['seconds'],flush=True)
