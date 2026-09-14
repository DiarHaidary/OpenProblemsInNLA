"""Independent finite diagnostics for PR253 RA05; not an asymptotic proof."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import json, importlib.util, math, hashlib
import numpy as np
root=Path(__file__).resolve().parent
src=Path('/private/tmp/nla-audit-253/references/holden-further-2026-09-14/RA-05')
rng=np.random.default_rng(1409253)
counts=Counter(); worst=0.
def check(c,category):
 assert bool(c),category
 counts[category]+=1
def close(a,b,category,tol=5e-10):
 global worst
 err=float(np.linalg.norm(np.asarray(a)-np.asarray(b))/(1+np.linalg.norm(np.asarray(b))))
 worst=max(worst,err);check(err<tol,category)
# Direct all-test integer cubic tensor identity; does not call submitted helper.
data=json.loads((src/'submitted/results/cubic_tensor_certificate.json').read_text())
core=np.array(data['core_numerators_denominator_2'],dtype=np.int64)
cube=1-2*((np.arange(256)[:,None]>>np.arange(8))&1)
noise=cube[data['noise_selected_cube_indices']]
A=np.array([np.outer(u,v).ravel() for u in core for v in noise])
Q=np.array([np.outer(z,y).ravel() for z in core for y in cube])
K=np.abs(Q@A.T)**3
G=np.abs(core@core.T)**3
F=np.abs(cube@noise.T)**3
check(np.array_equal(K,np.kron(G,F)),'complete_626688_integer_tensor_grid')
check(Fraction(int(np.sum(np.sum(K,axis=1)**2)),32768**2)==Fraction(34287,2),'independent_squared_cost_sum')
# Actual block projectors; arbitrarily large auxiliary dimension, fixed query rank.
for k in (1,2,4):
 for N in (1,3,17):
  dim=k*(N+1);R=2*np.sqrt(k)
  rows=np.zeros((k*N,dim));y=np.zeros((k,dim))
  for j in range(k):
   vals=rng.uniform(.1,2,size=N);vals/=np.linalg.norm(vals);y[j,k+j*N:k+(j+1)*N]=vals
   for t in range(N): rows[j*N+t,j]=R;rows[j*N+t,k+j*N+t]=1
  for sign in (-1,1):
   basis=(R*np.eye(dim)[:k]+sign*y)/np.sqrt(R*R+1);P=basis.T@basis
   close(P@P,P,'block_projector_idempotence');close(np.trace(P),k,'block_query_rank')
   residual=np.sum((rows-rows@P)**2,axis=1)
   u=np.concatenate([y[j,k+j*N:k+(j+1)*N] for j in range(k)])
   expected=2-1/(R*R+1)-u*u/(R*R+1)-sign*2*R*R/(R*R+1)*u
   close(residual,expected,'block_direct_euclidean_residual')
  dp=2-1/(R*R+1)-u*u/(R*R+1)-2*R*R/(R*R+1)*u
  dm=2-1/(R*R+1)-u*u/(R*R+1)+2*R*R/(R*R+1)*u
  for p in (2.0001,2.5,3,3.9999,4.0001,9.75,16):
   s=p/2
   check(np.all(dp>=-1e-14),'block_nonnegative_with_roundoff')
   delta=dm**s-np.maximum(dp,0)**s  # exact zero at N=1 can round slightly negative
   check(np.all(delta>=s*u-1e-9) and np.all(delta<=s*4**s*u+1e-9),'block_non_even_power_bounds')
# Exact polynomial derivative and rank-regime identities to higher degree than examples.
for s in range(2,17):
 q=2*s; d=[-sum(Fraction(1,j) for j in range(1,q+1))]+[Fraction((-1)**(j+1)*math.comb(q,j),j) for j in range(1,q+1)]
 for t in range(q+1): check(sum(d[j]*j**t for j in range(q+1))==int(t==1),'exact_derivative_extraction')
 for e in [Fraction(j,12) for j in range(1,73)]:
  up=min(s+2*e,max(s+Fraction(1,2)+e,s-1+2*e))
  lower=max(min(s+2*e,s+Fraction(1,2)+e,2*s),s-1+2*e)
  check(up==lower,'complete_even_lower_combination')
# The original mathematics is byte preserved after the dated publication covers.
for no,orig in [(1,'part_i_non_even.tex'),(2,'part_ii_even.tex')]:
 pub=(src/f'part-{no}.tex').read_text();sub=(src/'submitted/manuscript'/orig).read_text()
 check(pub[pub.index('\\section{'):]==sub[sub.index('\\section{'):],'publication_mathematical_body_unchanged')
# Three bad certificates must be rejected independently of their saved PASS result.
spec=importlib.util.spec_from_file_location('certchecker',src/'submitted/code/check_certificate.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
for kind in ['pivot','core','support']:
 bad=json.loads(json.dumps(data))
 if kind=='pivot': bad['gram_minus_32I_ldl_diagonal'][0]='-1'
 if kind=='core': bad['core_numerators_denominator_2'][0][0]=3
 if kind=='support': bad['universal_support_bound']['epsilon_squared_coefficient']='548591'
 path=root/f'negative-{kind}.json';path.write_text(json.dumps(bad))
 try: mod.run(path)
 except AssertionError: check(True,'corrupted_certificate_rejection')
 else: raise AssertionError('Bad certificate accepted: '+kind)
 path.unlink()
result={'passed':True,'assertions':sum(counts.values()),'categories':dict(counts),'largest_scaled_residual':worst,'seed':1409253,'scope':'Finite diagnostics and negative controls; no finite test proves the asymptotic theorem.'}
(root/'adversarial-rerun.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
