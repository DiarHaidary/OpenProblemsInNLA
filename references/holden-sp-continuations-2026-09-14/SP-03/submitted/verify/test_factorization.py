"""Finite exact checks supplement the general proof in the report."""
from pathlib import Path
import sys,json,random,time
import sympy as sp
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'src'))
from pole_factorization import matrices
rng=random.Random(9032026);result=[];start=time.perf_counter()
for m in range(1,6):
    for trial in range(5):
        A=sp.Matrix(m,m,[rng.randrange(-3,4) for _ in range(m*m)])
        B=sp.Matrix(m,m,[rng.randrange(-3,4) for _ in range(m*m)])
        if trial==3 and m>1:A[m-1,:]=A[0,:]
        if trial==4 and m>1:B[m-1,:]=B[0,:]
        L,K=matrices(A,B)
        lhs=L.det();rhs=A.det()*B.det()*K.det()
        assert lhs==rhs,(m,trial,lhs,rhs)
        result.append({'rank':m,'trial':trial,'passed':True,'determinant':str(lhs)})
a=sp.symbols('a:4');b=sp.symbols('b:4')
A=sp.Matrix(2,2,a);B=sp.Matrix(2,2,b)
L,K=matrices(A,B)
assert sp.expand(L.det()-A.det()*B.det()*K.det())==0
result.append({'rank':2,'symbolic_identity_in_eight_indeterminates':True})
# The spectral formula is also checked for non-diagonal, nonnormal matrices.
for m in range(1,6):
    A=sp.eye(m)
    for i in range(m):
        for j in range(i+1,m):A[i,j]=rng.randrange(-3,4)
    R=sp.eye(m)
    for i in range(m):
        for j in range(i+1,m):R[i,j]=rng.randrange(-3,4)
    mu=[sp.Integer(2*i+1) for i in range(m)]
    M=R*sp.diag(*mu)*R.inv();B=A*M
    L,K=matrices(A,B)
    value=A.det()**(m+1)*sp.prod(mu)*sp.prod(mu[i]+mu[j] for i in range(m) for j in range(i+1,m))
    assert L.det()==value
    result.append({'rank':m,'nondiagonal_spectral_identity':True})
report={'all_checks_passed':True,'checks':result,'seconds':time.perf_counter()-start,
        'scope':'Finite exact checks and a rank-two symbolic identity; the all-rank proof is written separately.'}
(BASE/'results'/'factorization_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
