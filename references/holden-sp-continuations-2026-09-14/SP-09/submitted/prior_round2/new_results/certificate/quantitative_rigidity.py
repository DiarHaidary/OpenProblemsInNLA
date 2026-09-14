"""Exact constants for normalized Hilbert--Schmidt stability of Krause minimizers."""
from __future__ import annotations
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json,argparse
import numpy as np
from local_geometry import PRIOR
from verify_certificate import require,words,poly_product,load_matrix,mm,star

def plus(*polys):
 d={}
 for p in polys:
  for w,c in p.items():d[w]=d.get(w,F(0))+c
 return {w:c for w,c in d.items() if c}
def scale(p,c):return {w:c*v for w,v in p.items() if c*v}
def prod(p,q):
 r=poly_product({w:(v,F(0)) for w,v in p.items()},{w:(v,F(0)) for w,v in q.items()})
 require(all(z[1]==0 for z in r.values()))
 return {w:z[0] for w,z in r.items()}
def ceil_sqrt(q):
 require(q>=0);n=isqrt(q.numerator//q.denominator)
 return n if F(n*n)>=q else n+1

def verify():
 c=json.loads((PRIOR/'krause_certificate.json').read_text());N=int(c['coordinate_denominator']);delta=388**2*N;blocks=c['blocks'];trace_local=F(0)
 for j in (1,2):
  b=blocks[j];K=(load_matrix(b['kernel_real']),load_matrix(b['kernel_s']));Z=(load_matrix(b['matrix_real']),load_matrix(b['matrix_s']));Y=mm(mm(K,Z),star(K))
  require(sum(Y[1].diagonal())==0);trace_local+=F(int(sum(Y[0].diagonal())),delta)
 qr=[int(x) for x in c['q_real']];qi=[int(x) for x in c['q_s']];trace_local+=F(sum(x*x+3*y*y for x,y in zip(qr,qi)),388**2)
 B=29*trace_local
 b=blocks[0];K=load_matrix(b['kernel_real']);require(np.all(load_matrix(b['kernel_s'])==0));Z=(load_matrix(b['matrix_real']),load_matrix(b['matrix_s']));S=(load_matrix(b['preconditioner_real']),load_matrix(b['preconditioner_s']));G=mm(mm(star(S),Z),S)
 margins=[int(G[0][i,i])-sum(abs(int(G[0][i,j]))+2*abs(int(G[1][i,j])) for j in range(52) if j!=i) for i in range(52)];m=min(margins);require(m>0)
 I={():F(1)};Ps=[{(0,):F(1)},{(1,):F(1)},{():F(1),(0,):F(-1),(1,):F(-1)}];Q1={(2,):F(1)};Q2={(3,):F(1)};weights=[F(1,16),F(10,16),F(5,16)]
 rs=[plus(prod(prod(P,Q1),P),scale(P,-p)) for P,p in zip(Ps,weights)]
 C=plus(Ps[0],scale(Ps[1],F(-1,5)),scale(Ps[2],F(1,5)));rs.append(plus(Q2,scale(prod(prod(C,Q1),C),-10)))
 basis=words(4);bounds=[]
 for r in rs:
  v=np.array([r.get(w,F(0)) for w in basis],dtype=object);coef=v[9:]/768
  require(np.array_equal(K@coef,v),'A required rigidity relation is not in the verified degree-four kernel.')
  tr=S[0].T@coef;ti=-S[1].T@coef;normsq=sum(x*x+3*y*y for x,y in zip(tr,ti));bounds.append(F(delta,m)*B*normsq)
 Sbound=sum(g/p for g,p in zip(bounds[:3],weights));Cinteger=44*ceil_sqrt(Sbound)+2*ceil_sqrt(bounds[3])
 require(Cinteger>0)
 out={'result':'PASS','norm':'normalized Hilbert--Schmidt norm, tau=Tr/(3k)','squared_cost_excess':'epsilon = ||A_k + U A_k U*||^2 - 27/13','integer_stability_constant':str(Cinteger),'statement':'inf_{V,W block diagonal} ||U - V(R tensor I_k)W||_2,tau <= C sqrt(epsilon)','local_trace_upper_bound':str(B),'kernel_congruence_minimum_margin':str(m),'relation_squared_constants':[str(v) for v in bounds],'polar_sum_squared_constant':str(Sbound)}
 print('PASS: all four rigidity relations have exact kernel coordinates.')
 print('PASS: the explicit dimension-independent stability constant is C =',Cinteger)
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--json-report',type=Path);a=p.parse_args();r=verify()
 if a.json_report:a.json_report.write_text(json.dumps(r,indent=2)+'\n')
