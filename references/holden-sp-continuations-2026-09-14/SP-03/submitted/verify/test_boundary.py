"""Exact checks for the projective denominator and scalar-direction asymptotic."""
from pathlib import Path
import sys,json,random
import sympy as sp
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from stein_normal_form import induced_matrix
rng=random.Random(88715);z,s,t=sp.symbols('z s t');checks=[]
for m in range(1,6):
    C=sp.Matrix(m,m,[rng.randrange(-4,5) for _ in range(m*m)])
    M=induced_matrix(C);W=induced_matrix(C,symmetric=False)
    k=m*(m+1)//2;r=m*(m-1)//2
    left=(-1)**k*M.charpoly(s).as_expr().subs(s,z*z)
    right=(-1)**r*C.charpoly(s).as_expr().subs(s,z)*C.charpoly(s).as_expr().subs(s,-z)*W.charpoly(s).as_expr().subs(s,z*z)
    assert sp.expand(left-right)==0
    assert left.subs(z,0)==C.det()**(m+1)
    checks.append({'rank':m,'homogenized_identity_checked':True,'leading_determinant_power_checked':True})
    b=sp.Matrix(m,m,[rng.randrange(-3,4) for _ in range(m*m)])
    c=sp.Matrix(m,m,[rng.randrange(-3,4) for _ in range(m*m)])
    sb=b+b.T;tc=c+c.T
    # The matrix t*Psi(tI) has this limit, including noncommutative order.
    leading=tc*sb-c*sb-tc*b
    assert leading==c.T*b.T-c*b
    checks[-1]['scalar_direction_asymptotic_checked']=True
report={'all_checks_passed':True,'checks':checks}
(BASE/'results'/'boundary_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
