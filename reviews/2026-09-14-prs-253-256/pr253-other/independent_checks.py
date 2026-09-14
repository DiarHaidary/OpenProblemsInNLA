"""Reviewer-written exact and numerical crosschecks, separate from supplied PASS logs."""
import json,sys,math,itertools,importlib.util
from pathlib import Path
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parent
r={'scope':'Finite supplementary evidence; universal conclusions require the written proofs.'}
# Reconstruct the graph polynomial construction independently, from mathematical definition.
rng=np.random.default_rng(253256)
graphs=0
for p,q,d in [(0,4,0),(4,0,0),(1,5,1),(8,11,4),(15,19,5)]:
 for trial in range(12):
  neighbors=[sorted(rng.choice(p,min(d,p,int(rng.integers(d+1))),replace=False).tolist()) if p else [] for _ in range(q)]
  t=s.symbols('t');vecs=[[int((i+1)**h) for h in range(d+1)] for i in range(p)]
  for ns in neighbors:
   poly=s.Poly(t**(d-len(ns))*s.prod(t-(i+1) for i in ns),t)
   vecs.append([poly.nth(h) for h in range(d+1)])
  gram=s.Matrix(vecs)*s.Matrix(vecs).T
  for i in range(p+q):
   for j in range(i+1,p+q):
    edge=(i<p<=j and i in neighbors[j-p])
    assert (gram[i,j]==0)==edge
  graphs+=1
r['SP10_extra_exact_graphs']=graphs
# Independently reconstruct RA14 integer certificate ranks and every published minor.
d=json.loads((ROOT/'RA-14/results/linear_vs_prefix_certificate.json').read_text());G=s.Matrix(d['starting_matrix']);D=s.diag(*d['scaled_diagonal'])
actual=G[:,:3].row_join(D*G[:,:3]).row_join(G[:,3:4]);prefix=G.row_join(D*G).row_join(D**2*G).row_join(D**3*G)
assert (actual.rank(),actual[1:,:].rank(),prefix.rank())==(7,7,12)
for M,key in [(actual[1:,:],'actual_tail_minor'),(prefix,'prefix_minor')]:
 rec=d[key];assert M.extract(rec['rows'],rec['columns']).det()==s.Integer(rec['determinant'])!=0
# Singular energy formula with anisotropic noncommuting leading excess: direct KKT check.
T=s.Matrix([[1,0,1],[0,1,1]]);W=s.Matrix([[0,1,0],[0,0,1]]);Gram=W.T*W
R=s.Matrix([[0],[1]]);CR=R.T*T*Gram.pinv()*T.T*R;P=R*CR.inv()*R.T
N=s.Matrix([[1],[0],[0]]);L0=Gram.pinv()*T.T*P;L=L0+N*(T*N).pinv()*(s.eye(2)-T*L0)
assert T*L==s.eye(2) and L.T*Gram*L==P and Gram*L==T.T*P
for a,b in [(1,2),(3,-2),(-7,1)]:
 J=T.nullspace()[0]*s.Matrix([[a,b]])
 assert (L+J).T*Gram*(L+J)-P==J.T*Gram*J
r['RA14_sympy_reconstruction']={'actual_rank':7,'actual_tail_rank':7,'prefix_rank':12,'singular_energy':'PASS'}
# Extra exact RA11 diagonal/correction cases at different PSD inputs, with all product signs.
tracecases=0
for n,q in [(2,2),(2,3),(3,2)]:
 N=n**q;B=s.Matrix([[int(rng.integers(-3,4)) for _ in range(2)] for i in range(N)]);M=B*B.T
 A=np.array(M.tolist(),dtype=object);diag=np.diag(A);means=np.zeros(N,dtype=object);mse=0
 for signs in itertools.product([-1,1],repeat=n*q):
  x=np.array([math.prod(signs[j*n+ij] for j,ij in enumerate(idx)) for idx in itertools.product(range(n),repeat=q)],dtype=object)
  est=x*(A@x);means+=est;mse+=sum((est-diag)**2)
  residual=diag-est
  # Uniform coordinate correction independently integrates to exact trace.
  assert sum(sum(est)+N*residual[i] for i in range(N))==N*sum(diag)
 count=2**(n*q)
 assert list(means)==list(count*diag)
 assert mse==count*sum(A[i,j]**2 for i in range(N) for j in range(N) if i!=j)
 tracecases+=1
r['RA11_extra_exact_cases']=tracecases
# Check elementary TR03 bounds directly, without calling the submitted utilities.
from fractions import Fraction as F
spectra=0
for n in range(3,10):
 for trial in range(10):
  v=sorted([F(int(rng.integers(1,100)),int(rng.integers(1,20))) for _ in range(n)],reverse=True)
  e=[sum((math.prod(c) for c in itertools.combinations(v,j)),F(0)) for j in range(n+1)]
  for k in range(1,n-1):
   t=e[k+1]/e[k];u=e[k-1]/e[k];tail=sum(v[k:])
   assert sum(t/(z+t) for z in v[:k])<=tail*u<=tail/t
   assert (k+1)*t<=min((k+1)*tail,(n-k)*(k+1)/sum(1/z for z in v[:k+1]))
   spectra+=1
r['TR03_extra_exact_spectral_cases']=spectra
r['status']='PASS'
(ROOT/'independent_checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
