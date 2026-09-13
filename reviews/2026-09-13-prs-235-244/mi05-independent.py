"""New numerical stress tests; not a proof of quantified MI05 claims."""
import itertools, json
import numpy as np
from scipy.linalg import expm
from scipy.optimize import linprog
P=list(itertools.permutations(range(4)))
S=[s for n in range(5) for s in itertools.combinations(range(4),n)]
pairs=[(i,j) for i in S for j in S if len(i)==len(j)]
T=np.array([[sorted(p[k] for k in i)==list(j) for p in P] for i,j in pairs],float)
def feature(U):
 return np.array([abs(np.linalg.det(U[np.ix_(i,j)]))**2 if i else 1 for i,j in pairs])
def tc(v):
 d=dict(zip(pairs,v)); t=sum(d[((i,),(i,))] for i in range(4))
 c=d[((0,1),(0,2))]+d[((0,1),(1,3))]-d[((0,2),(0,1))]-d[((0,2),(2,3))]
 return t,c
def weights(v):
 d=dict(zip(pairs,v));t,c=tc(v);h=-(t+c)/4;w=np.zeros(24)
 def put(s,x):w[P.index(tuple(int(i)-1 for i in s))]=x
 put('1234',-h)
 for s,i in [('1423',0),('3241',1),('4132',2),('2314',3)]:put(s,d[((i,),(i,))]+h)
 for s,i in [('2143',(0,1)),('3412',(0,2)),('4321',(0,3))]:put(s,d[(i,i)]+h)
 for s,i,j in [('3142',(0,1),(0,2)),('2413',(0,1),(1,3)),('4312',(0,2),(0,3)),('3421',(0,2),(1,2)),('2341',(0,3),(0,1)),('4123',(0,3),(2,3))]:put(s,d[(i,j)])
 return w,h
rng=np.random.default_rng(24220260913)
H=np.array([[1,1,1,1],[-1,1,-1,1],[-1,1,1,-1],[-1,-1,1,1]])/2
U0=np.array([[1,4,4,4],[-4,1,-4,4],[-4,4,1,-4],[-4,-4,4,1]])/7
worst=0.; lpcount=0; max_lp_error=0.; ball_count=0; safe_count=0
for trial in range(80):
 M=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));K=M-M.conj().T
 if trial<50:U=expm((.0001+trial*.0005)*K)@U0
 else:U=np.linalg.qr(M)[0]
 v=feature(U);w,h=weights(v);err=np.max(abs(T@w-v));worst=max(worst,err);assert err<1e-12
 branches=[]
 for p in P:
  t,c=tc(feature(U[:,p]));branches.extend([-(t+c)/4,-(t-c)/4])
 assert sum(x>1e-10 for x in branches)<=1
 rho=max(0,max(branches));assert rho<=1/6+1e-12
 if rho>1e-8:
  res=linprog(np.r_[np.zeros(24),np.ones(24)],A_eq=np.c_[T,-T],b_eq=v,bounds=(0,None),method='highs')
  assert res.success;error=abs(res.fun-rho);max_lp_error=max(max_lp_error,error);assert error<1e-7;lpcount+=1
 if h>1e-8:
  f=np.array([sum(tc(T[:,j]))/2 for j in range(24)])
  for k in range(20):
   a=rng.normal(size=4)+1j*rng.normal(size=4);b=rng.normal(size=4)+1j*rng.normal(size=4);eta=np.exp(1j*rng.uniform(0,2*np.pi))
   z=np.array([np.prod(a+b[list(p)]) for p in P]);j=np.argmax((eta*z).real)
   if f[j]>0:
    aug=v+(2*h/f[j])*T[:,j];wa,ha=weights(aug)
    assert abs(ha)<1e-12 and min(wa)>-1e-12
    det=np.linalg.det(np.diag(a)+U@np.diag(b)@U.conj().T)
    assert (eta*det).real<=(eta*z[j]).real+1e-9;safe_count+=1
for trial in range(200):
 M=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));K=M-M.conj().T
 U=expm(.01*K/np.linalg.norm(K,2))@H
 assert np.linalg.norm(U-H,2)<=.010000000001
 v=feature(U);w,h=weights(v)
 assert min(w)>-1e-12 and np.max(abs(T@w-v))<1e-12
 positive_at_H=np.flatnonzero(weights(feature(H))[0]>.1)
 assert len(positive_at_H)==8
 assert min(w[j] for j in positive_at_H)>=.03-1e-12
 ball_count+=1
print(json.dumps(dict(result='PASS',random_unitaries=80,positive_branch_LPs=lpcount,max_LP_error=max_lp_error,feature_max_error=worst,open_ball_checks=ball_count,support_criterion_checks=safe_count,scope='Numerical corroboration; no full MI05 or universal theorem certificate'),indent=2))
