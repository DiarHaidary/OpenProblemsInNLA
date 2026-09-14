"""Exact checks for the Stein identities, potential, and normalization."""
from pathlib import Path
import sys,json
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
import sympy as sp
import random
from pole_factorization import matrices,symmetric_basis
from stein_normal_form import induced_matrix,stein_solutions,evaluate,euler_characteristic
rng=random.Random(51937)
def mat(m):return sp.Matrix(m,m,[rng.randrange(-3,4) for _ in range(m*m)])
checks=[]
for m in range(1,6):
 E=symmetric_basis(m);k=len(E);I=sp.eye(m)
 for trial in range(3):
  A=mat(m);Ua=mat(m);B=2*A-Ua;C=4*A-Ua
  L,_=matrices(A,B)
  gram=sp.Matrix([[sp.trace((C*e*C.T-Ua*e*Ua.T)*f) for f in E] for e in E])
  assert gram==8*L
  checks.append({'rank':m,'trial':trial,'identity':'general Stein bilinear form','passed':True})
 C=mat(m);A=(C+I)/4;L,_=matrices(A,2*A-I)
 M=induced_matrix(C)-sp.eye(k)
 W=induced_matrix(C,symmetric=False)-sp.eye(m*(m-1)//2)
 assert L.det()==sp.Rational(1,2**(m*(m+2)))*M.det()
 assert M.det()==(C-I).det()*(C+I).det()*W.det()
 checks.append({'rank':m,'identity':'both normalized determinant factorizations','passed':True})
 # A separate invertible-Ua normalization check, without arbitrary choices of square roots.
 while True:
  Ua=mat(m)
  if Ua.det():break
 A=mat(m);L,_=matrices(A,2*A-Ua)
 Cn=4*Ua.inv()*A-I
 delta=(induced_matrix(Cn)-sp.eye(k)).det()
 assert L.det()==sp.Rational(1,2**(m*(m+2)))*Ua.det()**(m+1)*delta
 checks.append({'rank':m,'identity':'general invertible-Ua determinant formula','passed':True})
 if m<=3:
  while True:
   C=mat(m)
   if (induced_matrix(C)-sp.eye(k)).det():break
  b,c,d=mat(m),mat(m),mat(m)
  phi,g,S,T=evaluate(C,b,c,d);A=(C+I)/4
  L,_=matrices(A,2*A-I)
  bv=sp.Matrix([sp.trace(A*e*c.T) for e in E])
  cv=sp.Matrix([sp.trace(e*A*b.T) for e in E])
  tv=L.inv()*bv;sv=L.T.inv()*cv
  So=sum((sv[i]*E[i] for i in range(k)),sp.zeros(m))
  To=sum((tv[i]*E[i] for i in range(k)),sp.zeros(m))
  assert (S,T)==(So,To)
  assert C*S*C.T-S==(C+I)*b.T+b*(C+I).T
  assert C.T*T*C-T==c.T*(C+I)+(C+I).T*c
  oldphi=-sp.trace(A*d.T)-sp.trace(A.inv())-(cv.T*tv)[0]
  assert sp.simplify(phi-oldphi)==0
  Y=A.inv().T
  assert g==T*(4*A-I)*S-c*S-T*b-d+Y*Y
  # Exact directional differentiation of the scalar potential, using the
  # inverse-matrix derivative and the differentiated Stein equation.
  V=mat(m);C1=C+I;Vinv=C1.inv()
  rhs=c.T*V+V.T*c-V.T*T*C-C.T*T*V
  MT=induced_matrix(C.T)-sp.eye(k)
  pairs=[(i,j) for i in range(m) for j in range(i,m)]
  dtv=MT.inv()*sp.Matrix([rhs[i,j] for i,j in pairs])
  dT=sum((dtv[i]*E[i] for i in range(k)),sp.zeros(m))
  deriv=-sp.trace(V*d.T)/4+4*sp.trace(Vinv*V*Vinv)-sp.trace(dT*C1*b.T+T*V*b.T)/4
  assert sp.simplify(deriv-sp.trace(g.T*V)/4)==0
  checks.append({'rank':m,'identity':'Stein solutions, potential, gradient directional derivative','passed':True})
  # Q-isometric left normalization of arbitrary data and points.
  U=mat(2*m);X=mat(2*m);Ua=U[:m,:m]
  if Ua.det():
   zero=sp.zeros(m);Q=zero.row_join(I).col_join(I.row_join(zero))
   G=Ua.inv().row_join(zero).col_join(zero.row_join(Ua.T))
   assert G.T*Q*G==Q
   assert (G*U)[:m,:m]==I
   assert sp.trace(Q*(G*(X-U)).T*Q*(G*(X-U)))==sp.trace(Q*(X-U).T*Q*(X-U))
   checks.append({'rank':m,'identity':'Q-isometric data normalization','passed':True})
x,b,c,d=sp.symbols('x b c d')
p,g,_,_=evaluate(sp.Matrix([[x]]),sp.Matrix([[b]]),sp.Matrix([[c]]),sp.Matrix([[d]]))
assert sp.simplify(4*sp.diff(p,x)-g[0])==0
assert sp.simplify(g[0]-(4*b*c/(x-1)**2+16/(x+1)**2-d))==0
checks.append({'rank':1,'identity':'fully symbolic scalar derivative','passed':True})
report={'all_checks_passed':True,'checks':checks,'euler_characteristics':[int(euler_characteristic(m)) for m in range(13)]}
text=json.dumps(report,indent=2)+'\n'
(BASE/'results'/'stein_checks.json').write_text(text)
print(text)
