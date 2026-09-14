"""Exploratory numerical fit; all values are feasible upper bounds."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,time,json,sys
from pathlib import Path
from scipy.linalg import expm
from search_orbits import optimize,haar,bottleneck,value
out=Path(__file__).parent/'candidate34_rerun';out.mkdir(exist_ok=True)
rng=np.random.default_rng(60914034);n=7;k=2
x=np.array([1,(4+5j*np.sqrt(3))/13,(-1+2j*np.sqrt(3))/13]);a=np.repeat(x,[2,2,3]);b=-a
a=a+.01*(rng.normal(size=n)+1j*rng.normal(size=n));b=b+.01*(rng.normal(size=n)+1j*rng.normal(size=n));scale=max(max(abs(a)),max(abs(b)),1);a/=scale;b/=scale
R=np.eye(3)-2*np.outer(np.sqrt([5/8,1/4,1/8]),np.sqrt([5/8,1/4,1/8]))
taus=(.008,.001,.0001,.00001,.000001,.0000001,.00000001);base=bottleneck(a,b)
for j in range(12):
 seed=haar(n,rng)
 if j==0:seed=np.eye(n,dtype=complex);seed[:3,:3]=R
 z=optimize(a,b,seed,taus=taus,maxiter=450)
 if z[0]<base[0]:base=z
 print('base',j,base[0],flush=True)
 np.savez_compressed(out/'base.npz',a=a,b=b,U=base[1])
aa=np.repeat(a,k);bb=np.repeat(b,k);ampl=base[0],np.kron(base[1],np.eye(k))
for j in range(10):
 seed=haar(n*k,rng)
 if j==0:
  h=rng.normal(size=(n*k,n*k))+1j*rng.normal(size=(n*k,n*k));seed=np.kron(base[1],np.eye(k))@expm(.03j*(h+h.conj().T))
 z=optimize(aa,bb,seed,taus=taus,maxiter=600)
 if z[0]<ampl[0]:ampl=z
 print('ampl',j,ampl[0],base[0]-ampl[0],flush=True)
 np.savez_compressed(out/'amplified.npz',a=a,b=b,U=ampl[1])
(out/'initial.json').write_text(json.dumps({'base_upper':base[0],'amplified_upper':ampl[0],'candidate_gap':base[0]-ampl[0],'scope':'Numerical upper bounds only'},indent=2))
