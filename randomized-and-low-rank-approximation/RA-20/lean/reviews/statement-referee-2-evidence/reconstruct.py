"""Independent exact symbolic and rational RA20 statement reconstruction.
No CAS, floating point, imported author checker, or claimed generic geometric proof.
Polynomial identities have rational coefficients and are valid over complex scalars.
"""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import json
E=Path(__file__).resolve().parent
N=12;zero=(0,)*N
class P:
 def __init__(self,d=0):self.d={k:Q(v) for k,v in d.items() if v} if isinstance(d,dict) else ({zero:Q(d)} if d else {})
 def __add__(self,b):
  b=b if isinstance(b,P) else P(b);d=self.d.copy()
  for k,v in b.d.items():d[k]=d.get(k,0)+v
  return P(d)
 __radd__=__add__
 def __neg__(self):return P({k:-v for k,v in self.d.items()})
 def __sub__(self,b):return self+-1*b
 def __rsub__(self,b):return -self+b
 def __mul__(self,b):
  b=b if isinstance(b,P) else P(b);d={}
  for k,v in self.d.items():
   for l,w in b.d.items():
    t=tuple(x+y for x,y in zip(k,l));d[t]=d.get(t,0)+v*w
  return P(d)
 __rmul__=__mul__
 def __pow__(self,n):
  o=P(1)
  for _ in range(n):o=o*self
  return o
 def diff(self,i):
  d={}
  for k,v in self.d.items():
   if k[i]:l=list(k);l[i]-=1;d[tuple(l)]=v*k[i]
  return P(d)
 def sub(self,mapping):
  o=P(0)
  for k,v in self.d.items():
   t=P(v)
   for i,e in enumerate(k):
    if e:t=t*mapping.get(i,V[i])**e
   o=o+t
  return o
 def at(self,values):
  out=Q(0)
  for k,v in self.d.items():
   for i,e in enumerate(k):v*=Q(values[i])**e
   out+=v
  return out
 def __eq__(self,b):return self.d==(b.d if isinstance(b,P) else P(b).d)
 def serialize(self):return [{'powers':list(k),'coefficient':str(v)} for k,v in sorted(self.d.items())]
V=[]
for i in range(N):k=[0]*N;k[i]=1;V.append(P({tuple(k):1}))
a,b,c=V[:3];X=[[P(0),a,b],[a,P(0),c],[b,c,P(0)]]
U=[[V[3+3*i+j] for j in range(3)] for i in range(3)]
def determinant(M):
 out=P(0)
 for perm in permutations(range(3)):
  t=P((-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3)))
  for i in range(3):t=t*M[i][perm[i]]
  out=out+t
 return out
det=determinant(X);assert det==2*a*b*c
F=sum((X[i][j]-U[i][j])**2 for i in range(3) for j in range(3))
assert all(F.diff(i).diff(j)==(4 if i==j else 0) for i in range(3) for j in range(3))
sym={6:V[4],9:V[5],10:V[8]};Fs=F.sub(sym)
expected=sum(U[i][i]**2 for i in range(3))+2*((a-V[4])**2+(b-V[5])**2+(c-V[8])**2)
assert Fs==expected
alpha,beta,gamma=V[4],V[5],V[8]
points=[(P(0),beta,gamma),(alpha,P(0),gamma),(alpha,beta,P(0))]
records=[]
for excluded,point in enumerate(points):
 sub={i:p for i,p in enumerate(point)};free=[i for i in range(3) if i!=excluded]
 assert det.sub(sub)==0 and all(Fs.diff(i).sub(sub)==0 for i in free)
 constraint=[det.diff(i).sub(sub) for i in range(3)]
 assert constraint[excluded]!=P(0) and all(constraint[i]==0 for i in free)
 assert all(F.diff(i).diff(j)==(4 if i==j else 0) for i in free for j in free)
 u=[[Q(v) for v in row] for row in [[1,1,2],[1,2,3],[2,3,3]]]
 numbers=[0,0,0]+[v for row in u for v in row]
 coords=[z.at(numbers) for z in point];values=coords+numbers[3:]
 distance=F.at(values);assert distance==[16,22,32][excluded]
 matrix=[[Q(0),coords[0],coords[1]],[coords[0],Q(0),coords[2]],[coords[1],coords[2],Q(0)]]
 assert any(-matrix[i][j]**2!=0 for i in range(3) for j in range(i+1,3))
 records.append({'zero_coordinate':excluded,'coordinates':list(map(str,coords)),
  'full_Frobenius_distance':str(distance),'determinant_gradient':list(map(str,[g.at(numbers) for g in constraint])),
  'generic_free_gradient_exact_zero':True,'actual_unrestricted_U_Hessian_4I':True})
assert len({tuple(r['coordinates']) for r in records})==3
assert 27*(3-3)+4==4
r={'verdict':'PASS independent exact reconstruction','coefficient_field':'Q; polynomial identities valid over C',
 'variables':['a','b','c','U00','U01','U02','U10','U11','U12','U20','U21','U22'],
 'determinant':det.serialize(),'symmetric_distance':Fs.serialize(),
 'full_unsymmetric_U_Hessian_in_abc':'4 I3; hence every plane chart has 4 I2',
 'points':records,'plane_hessian_determinant':'16','generic_count_predicted_by_components':3,
 'original_formula_at_3_3':4,
 'limitations':'Diagnostic algebra only. No proof of smoothLocus equivalence, reduced quotient isomorphism, arbitrary-polynomial genericity intersection or Cardinal count is supplied here; those remain exact Challenge obligations.'}
(E/'reconstruction.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
