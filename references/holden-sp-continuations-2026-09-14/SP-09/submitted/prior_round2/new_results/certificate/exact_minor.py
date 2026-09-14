"""Fraction-free integer audit of the same 107-by-107 coefficient minor.

Unlike rank_witness.py, this program does not reduce the coefficient arithmetic
modulo a prime. It clears only the trace denominator 3 and uses exact Bareiss
elimination. The integer determinant is compared with the modular witness.
"""
from __future__ import annotations
from pathlib import Path
import argparse,json,time,hashlib
from functools import lru_cache
import numpy as np
from local_geometry import PRIOR,moment_keys
from verify_certificate import require,words,normal_word,poly_product,adj,add

@lru_cache(maxsize=None)
def cyclic(w):return normal_word(w,True)

def mul(x,y):
 a,b=x;c,d=y
 return a*c-3*b*d,a*d+b*c

class ExactBuilder:
 def __init__(self):
  c=json.loads((PRIOR/'krause_certificate.json').read_text());self.keys=moment_keys();self.ix={v:i for i,v in enumerate(self.keys)};self.k=[];self.meta={}
  for j,bl in enumerate(c['blocks']):
   W=words(4 if j==0 else 3);kr=bl['kernel_real'];ki=bl['kernel_s'];cols=[]
   for z in range(len(kr[0])):
    cols.append([(w,(int(kr[i][z]),int(ki[i][z]))) for i,w in enumerate(W) if int(kr[i][z]) or int(ki[i][z])])
   self.k.append(cols)
  d={():(-2,4),(0,):(14,-2),(1,):(5,3),(2,):(14,-2),(3,):(5,3)};ds={w[::-1]:adj(c) for w,c in d.items()};h1={w:(-a,-b) for w,(a,b) in poly_product(ds,d).items()};h2={w:(-a,-b) for w,(a,b) in poly_product(d,ds).items()}
  for h in (h1,h2):h[()]=add(h.get((),(0,0)),(351,0))
  self.h=[{():(169,0)},h1,h2]
 def wm(self,w):
  if w in self.meta:return self.meta[w]
  if len(w)<=1:v=(0,-1,1,1 if len(w)==1 else 3)
  else:
   wr=cyclic(w[::-1]);key=min(w,wr);v=(self.ix[(key,'r')],self.ix.get((key,'s'),-1),1 if w==key else -1,3)
  self.meta[w]=v;return v
 def column(self,meta):
  j,u,v,typ=meta;re=[0]*109;im=[0]*109
  for a,ca in self.k[j][v]:
   for b,cb in self.k[j][u]:
    c0=mul((ca[0],-ca[1]),cb)
    for w,cw in self.h[j].items():
     word=cyclic(a[::-1]+w+b)
     if word is None:continue
     x,y=mul(c0,cw);ir,ii,sgn,scale=self.wm(word);x*=scale;y*=scale;re[ir]+=x;im[ir]+=y
     if ii>=0:re[ii]-=3*sgn*y;im[ii]+=sgn*x
  if typ=='diag':
   require(u==v and all(x==0 for x in im),'Nonreal diagonal Gram entry.');return re
  if typ=='real':return [2*x for x in re]
  if typ=='s':return [-6*x for x in im]
  raise ValueError('Unknown Gram column type.')

def bareiss(A):
 A=np.array(A,dtype=object).copy();n=len(A);require(A.shape==(n,n));prev=1;sign=1
 for k in range(n-1):
  pivot=next((i for i in range(k,n) if A[i,k]!=0),None)
  require(pivot is not None,'Singular exact minor.')
  if pivot!=k:A[[k,pivot]]=A[[pivot,k]];sign=-sign
  p=A[k,k];num=A[k+1:,k+1:]*p-A[k+1:,k:k+1]*A[k:k+1,k+1:]
  if prev!=1:
   require(all(x%prev==0 for x in num.ravel()),'Bareiss division was not exact.')
   num=num//prev
  A[k+1:,k+1:]=num;A[k+1:,k]=0;prev=p
 return sign*int(A[-1,-1])

def run(write=False,report:Path|None=None):
 start=time.monotonic();root=Path(__file__).resolve().parent;wp=root/'local_rank_witness.json';w=json.loads(wp.read_text());b=ExactBuilder();M=np.array([b.column(c) for c in w['columns']],dtype=object).T[w['rows'],:];det=bareiss(M);require(det!=0)
 require(det%w['prime']==pow(3,107,w['prime'])*w['minor_determinant_mod_prime']%w['prime'],'Integer and modular determinant paths disagree.')
 digest=hashlib.sha256(wp.read_bytes()).hexdigest();ep=root/'exact_minor_witness.json'
 if write:
  factors=[[2,1740],[3,342],[5,14],[7,1],[13,215],[59,1]];product=-1
  for prime,power in factors:product*=prime**power
  require(product==det,'Regenerated determinant has changed factorization.')
  ep.write_text(json.dumps({'rank_witness_sha256':digest,'dimension':107,'clearing_factor':3,'integer_determinant':str(det),'determinant_sign':-1,'prime_power_factorization':factors},indent=2)+'\n')
 else:
  e=json.loads(ep.read_text());require(e['rank_witness_sha256']==digest and e['dimension']==107 and e['clearing_factor']==3);require(det==int(e['integer_determinant']),'Integer determinant does not match the fixed witness.')
  product=int(e['determinant_sign'])
  for prime,power in e['prime_power_factorization']:product*=int(prime)**int(power)
  require(product==det,'The displayed exact determinant factorization is wrong.')
 out={'result':'PASS','dimension':107,'clearing_factor':3,'determinant_decimal_digits':len(str(abs(det))),'determinant_sign':1 if det>0 else -1,'modular_cross_check':True,'elapsed_seconds':time.monotonic()-start}
 print('PASS: exact fraction-free determinant is nonzero ('+str(out['determinant_decimal_digits'])+' decimal digits) and agrees with the modular calculation.')
 if report:report.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write-witness',action='store_true');p.add_argument('--json-report',type=Path);a=p.parse_args();run(a.write_witness,a.json_report)
