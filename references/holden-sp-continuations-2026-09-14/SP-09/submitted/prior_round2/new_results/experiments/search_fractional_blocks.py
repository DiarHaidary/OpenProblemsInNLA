"""Exploration: fractional direct-sum constructions versus base feasible bounds.
No base objective is a certified lower bound. A positive gap is only a candidate.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import sys,json,time,itertools
from concurrent.futures import ProcessPoolExecutor,as_completed
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'prior'/'experiments'))
from search_orbits import optimize,haar,bottleneck,value

ROOT=Path(__file__).resolve().parent

def frac_lp(a,b,models):
 n=len(a);M=[];cost=[];descr=[]
 for I,J,U,v in models:
  c=np.zeros(2*n)
  for i in I:c[i]+=1
  for j in J:c[n+j]+=1
  M.append(c);cost.append(v);descr.append((I,J,U))
 for i in range(n):
  for j in range(n):
   c=np.zeros(2*n);c[i]=1;c[n+j]=1;M.append(c);cost.append(abs(a[i]-b[j]));descr.append(((i,),(j,),np.ones((1,1))))
 M=np.column_stack(M);cost=np.array(cost);levels=np.unique(cost);lo=0;hi=len(levels)-1
 def solve(t):
  ids=np.flatnonzero(cost<=t+1e-13);r=linprog(np.zeros(len(ids)),A_eq=M[:,ids],b_eq=np.ones(2*n),bounds=(0,None),method='highs');return r,ids
 while lo<hi:
  mid=(lo+hi)//2;r,ids=solve(levels[mid])
  if r.success:hi=mid
  else:lo=mid+1
 r,ids=solve(levels[lo]);sol=[(int(ids[j]),float(x)) for j,x in enumerate(r.x) if x>1e-8]
 return float(levels[lo]),sol,descr,M,cost

def run(case):
 rng=np.random.default_rng(202609133000+case);n=6 if case%4<3 else 4;a0=np.array([1,(4+5j*np.sqrt(3))/13,(-1+2j*np.sqrt(3))/13]);v=np.sqrt([5/8,1/4,1/8]);R=np.eye(3)-2*np.outer(v,v);amp=[.002,.008,.02,.06,.12,.25,.4,.8][case//4%8];t0=time.monotonic()
 if n==6:
  a=np.repeat(a0,2)+amp*(rng.normal(size=6)+1j*rng.normal(size=6));b=-np.repeat(a0,2)+amp*(rng.normal(size=6)+1j*rng.normal(size=6));Is=list(itertools.product(range(2),range(2,4),range(4,6)));Js=Is;anchor=np.kron(R,np.eye(2))
  if case%3==0:b=-a
 else:
  z=-a0[case%2]+.3*(rng.normal()+1j*rng.normal());a=np.r_[a0,z]+amp*(rng.normal(size=4)+1j*rng.normal(size=4));b=np.r_[-a0,z]+amp*(rng.normal(size=4)+1j*rng.normal(size=4));Is=list(itertools.combinations(range(4),3));Js=Is;anchor=np.eye(4,dtype=complex);anchor[:3,:3]=R
 scale=max(abs(a).max(),abs(b).max());a/=scale;b/=scale;models=[]
 taus=(.004,.0004,.00004,.000004,.0000004,.00000004)
 for I in Is:
  for J in Js:
   aa=a[list(I)];bb=b[list(J)];best=bottleneck(aa,bb)
   for U in [R,haar(3,rng)]:
    z=optimize(aa,bb,U,taus=taus,maxiter=400)
    if z[0]<best[0]:best=z
   models.append((I,J,best[1],best[0]))
 upper,sol,descr,M,cost=frac_lp(a,b,models);base=bottleneck(a,b)
 for j in range(12):
  z=optimize(a,b,anchor if j==0 else haar(n,rng),taus=taus,maxiter=700)
  if z[0]<base[0]:base=z
 gap=base[0]-upper
 if gap>1e-7:
  for j in range(60):
   z=optimize(a,b,haar(n,rng),taus=taus+(4e-9,),maxiter=1000)
   if z[0]<base[0]:base=z
 item={'case':case,'n':n,'amplitude':amp,'base_upper':base[0],'fractional_amplified_upper':upper,'candidate_gap':base[0]-upper,'matching':bottleneck(a,b)[0],'models':len(models),'fractional_support':[(list(descr[i][0]),list(descr[i][1]),x,float(cost[i])) for i,x in sol],'seconds':time.monotonic()-t0}
 arrays=dict(a=a,b=b,baseU=base[1],M=M,cost=cost,weights=np.array(sol));
 for i,x in sol:arrays['block_'+str(i)]=descr[i][2]
 return item,arrays

if __name__=='__main__':
 out=ROOT/'rerun_results';out.mkdir(exist_ok=True)
 with ProcessPoolExecutor(max_workers=2) as ex,open(out/'results.jsonl','w',buffering=1) as log:
  for f in as_completed([ex.submit(run,c) for c in range(32)]):
   d,arrays=f.result();np.savez_compressed(out/f"case_{d['case']:03d}.npz",**arrays);log.write(json.dumps(d)+'\n');print(json.dumps(d),flush=True)
