"""Recompute a nonzero 107-by-107 minor over a prime field.

All entries come from the fixed integer certificate. A nonzero modular minor
proves an exact rank lower bound over Q. No numerical rank tolerance is used.
The trace coordinates are 1, Re tau(w), and Im(tau(w))/sqrt(3).
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from functools import lru_cache
import numpy as np
from local_geometry import PRIOR,moment_keys
from verify_certificate import require,words,normal_word,poly_product,adj,add

P_DEFAULT=1000003
@lru_cache(maxsize=None)
def cyclic(w):return normal_word(w,True)

class Builder:
 def __init__(self,prime:int=P_DEFAULT):
  self.p=prime;self.inv3=pow(3,prime-2,prime);self.keys=moment_keys();self.ix={v:i for i,v in enumerate(self.keys)}
  c=json.loads((PRIOR/'krause_certificate.json').read_text());self.kernels=[]
  for j,bl in enumerate(c['blocks']):
   W=words(4 if j==0 else 3);kr=bl['kernel_real'];ki=bl['kernel_s'];cols=[]
   for z in range(len(kr[0])):
    cols.append([(w,(int(kr[i][z])%prime,int(ki[i][z])%prime)) for i,w in enumerate(W) if int(kr[i][z]) or int(ki[i][z])])
   self.kernels.append(cols)
  d={():(-2,4),(0,):(14,-2),(1,):(5,3),(2,):(14,-2),(3,):(5,3)};ds={w[::-1]:adj(c) for w,c in d.items()}
  h1={w:(-a,-b) for w,(a,b) in poly_product(ds,d).items()};h2={w:(-a,-b) for w,(a,b) in poly_product(d,ds).items()}
  for h in (h1,h2):h[()]=add(h.get((),(0,0)),(351,0))
  self.hs=[{():(169,0)},h1,h2]
  self.meta={}
 def mul(self,x,y):
  a,b=x;c,d=y;p=self.p
  return (a*c-3*b*d)%p,(a*d+b*c)%p
 def word_meta(self,w):
  if w in self.meta:return self.meta[w]
  if len(w)<=1:v=(0,-1,1,self.inv3 if len(w)==1 else 1)
  else:
   wr=cyclic(w[::-1]);key=min(w,wr);sgn=1 if w==key else -1;v=(self.ix[(key,'r')],self.ix.get((key,'s'),-1),sgn,1)
  self.meta[w]=v;return v
 def bilinear(self,j,u,v):
  """Real and s-imaginary coefficient vectors of tau(r_v^* h_j r_u)."""
  p=self.p;re=[0]*109;im=[0]*109
  for a,ca in self.kernels[j][v]:
   for b,cb in self.kernels[j][u]:
    c0=self.mul((ca[0],-ca[1]),cb)
    for w,cw in self.hs[j].items():
     word=cyclic(a[::-1]+w+b)
     if word is None:continue
     x,y=self.mul(c0,cw);ir,ii,sgn,scale=self.word_meta(word);x=x*scale%p;y=y*scale%p
     re[ir]=(re[ir]+x)%p;im[ir]=(im[ir]+y)%p
     if ii>=0:re[ii]=(re[ii]-3*sgn*y)%p;im[ii]=(im[ii]+sgn*x)%p
  return np.array(re,dtype=np.int64),np.array(im,dtype=np.int64)
 def column(self,meta):
  j,u,v,typ=meta;r,i=self.bilinear(j,u,v)
  if typ=='diag':
   require(u==v and np.all(i==0),'A diagonal Gram coefficient is not real.');return r
  if typ=='real':return 2*r%self.p
  if typ=='s':return (-6*i)%self.p
  raise ValueError('Unknown column type.')

def det_mod(A,p):
 A=np.array(A,dtype=np.int64).copy()%p;require(A.ndim==2 and A.shape[0]==A.shape[1]);det=1
 for j in range(len(A)):
  choices=np.flatnonzero(A[j:,j]);require(len(choices)>0,'The claimed square minor is singular.');r=j+int(choices[0])
  if r!=j:A[[j,r]]=A[[r,j]];det=-det
  pivot=int(A[j,j]);det=det*pivot%p
  if j+1<len(A):
   f=A[j+1:,j]*pow(pivot,p-2,p)%p;A[j+1:,j:]=(A[j+1:,j:]-f[:,None]*A[j,j:][None,:])%p
 return det%p

def is_prime(p):
 if p<2:return False
 i=2
 while i*i<=p:
  if p%i==0:return False
  i+=1
 return True

def discover(path:Path):
 b=Builder();p=b.p;basis={};columns=[];metadata=[];rows=[];started=time.monotonic()
 done=False
 for j,ks in enumerate(b.kernels):
  n=len(ks);candidates=[(j,u,u,'diag') for u in range(n)]+[(j,u,v,typ) for u in range(n) for v in range(u+1,n) for typ in ('real','s')]
  for meta in candidates:
   col=b.column(meta);v=col.copy()
   for r,z in basis.items():
    if v[r]:v=(v-int(v[r])*z)%p
   nz=np.flatnonzero(v)
   if len(nz):
    r=int(nz[0]);basis[r]=v*pow(int(v[r]),p-2,p)%p;columns.append(col);metadata.append(meta);rows.append(r)
    if len(columns)==107:done=True;break
  print('block',j,'rank',len(columns),'seconds',time.monotonic()-started,flush=True)
  if done:break
 require(len(columns)==107,'Did not find 107 independent columns.')
 M=np.column_stack(columns)[rows,:];det=det_mod(M,p)
 out={'prime':p,'rank_lower_bound':107,'rows':rows,'columns':metadata,'minor_determinant_mod_prime':int(det),'trace_coordinates':[[list(w),typ] for w,typ in b.keys]}
 path.write_text(json.dumps(out,indent=2)+'\n');print('SAVED',path,'determinant',det,flush=True)

def verify(path:Path):
 started=time.monotonic();w=json.loads(path.read_text());p=int(w['prime']);require(is_prime(p) and p!=3,'Invalid prime.');b=Builder(p)
 require(w['trace_coordinates']==[[list(v),typ] for v,typ in b.keys],'Coordinate inventory changed.')
 require(w['rank_lower_bound']==107 and len(w['rows'])==107 and len(set(w['rows']))==107 and len(w['columns'])==107)
 require(all(0<=r<109 for r in w['rows']));M=np.column_stack([b.column(meta) for meta in w['columns']])[w['rows'],:];det=det_mod(M,p)
 require(det==int(w['minor_determinant_mod_prime']) and det!=0,'Nonzero determinant certificate failed.')
 print(f'PASS: the exact coefficient map has rank at least 107 (minor determinant {det} modulo prime {p}).')
 return {'result':'PASS','rank_lower_bound':107,'prime':p,'minor_determinant_mod_prime':det,'coefficient_space_dimension':109,'elapsed_seconds':time.monotonic()-started}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--discover',action='store_true');p.add_argument('--witness',type=Path,default=Path(__file__).with_name('local_rank_witness.json'));p.add_argument('--json-report',type=Path);a=p.parse_args()
 if a.discover:discover(a.witness)
 else:
  r=verify(a.witness)
  if a.json_report:a.json_report.write_text(json.dumps(r,indent=2)+'\n')
