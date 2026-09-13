"""Independent exact checks, written for the 2026-09-13 informal audit."""
import itertools, json, random
import sympy as s
P=list(itertools.permutations(range(4)))
subs=[i for k in range(5) for i in itertools.combinations(range(4),k)]
pairs=[(i,j) for i in subs for j in subs if len(i)==len(j)]
def Q(U,I,J):
 d=U.extract(I,J).det() if I else s.Integer(1)
 return s.expand_complex(d*s.conjugate(d)).simplify()
def tc(U):
 return sum(abs(U[i,i])**2 for i in range(4)),Q(U,[0,1],[0,2])+Q(U,[0,1],[1,3])-Q(U,[0,2],[0,1])-Q(U,[0,2],[2,3])
def weights(U):
 t,c=tc(U);h=-(t+c)/4
 w={p:s.Integer(0) for p in P}
 def put(st,v):w[tuple(int(i)-1 for i in st)]=v
 put('1234',-h)
 for st,i in [('1423',0),('3241',1),('4132',2),('2314',3)]:put(st,abs(U[i,i])**2+h)
 for st,I in [('2143',[0,1]),('3412',[0,2]),('4321',[0,3])]:put(st,Q(U,I,I)+h)
 for st,I,J in [('3142',[0,1],[0,2]),('2413',[0,1],[1,3]),('4312',[0,2],[0,3]),('3421',[0,2],[1,2]),('2341',[0,3],[0,1]),('4123',[0,3],[2,3])]:put(st,Q(U,I,J))
 return w
rng=random.Random(20260913)
checks=0
for trial in range(5):
 M=s.Matrix(4,4,lambda i,j:rng.randint(-2,2)+s.I*rng.randint(-2,2))
 K=M-M.conjugate().T
 U=(s.eye(4)-K).inv()*(s.eye(4)+K)
 U=U.applyfunc(s.simplify)
 assert U.conjugate().T*U==s.eye(4) or (U.conjugate().T*U-s.eye(4)).applyfunc(s.simplify)==s.zeros(4)
 w=weights(U)
 for I,J in pairs:
  assert s.simplify(sum(w[p] for p in P if sorted(p[i] for i in I)==list(J))-Q(U,I,J))==0
  checks+=1
 t,c=tc(U);tt,cc=tc(U.T)
 assert s.simplify(t-tt)==0 and s.simplify(c+cc)==0
 hs=[]
 for p in P:
  a,b=tc(U[:,list(p)])
  hs.extend([-(a+b)/4,-(a-b)/4])
 assert sum(bool(h>0) for h in hs)<=1
 assert max(hs)<=s.Rational(1,6)
 # Direct determinant expansion tests the orientation of the spectral labels.
 a=[1+s.I,2-s.I,-3,4*s.I];b=[-2,3+2*s.I,1-4*s.I,5]
 lhs=(s.diag(*a)+U*s.diag(*b)*U.conjugate().T).det()
 rhs=sum(w[p]*s.prod(a[i]+b[p[i]] for i in range(4)) for p in P)
 assert s.simplify(lhs-rhs)==0
print(json.dumps({'status':'PASS','seed':20260913,'rational_complex_unitaries':5,'exact_minor_equations':checks,'direct_determinant_checks':5,'all_branch_checks':240,'transpose_sign_checks':5},indent=2))
