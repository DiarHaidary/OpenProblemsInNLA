"""Reviewer checks against direct Lagrange integration, not the M formula."""
import importlib.util,json
from pathlib import Path
from fractions import Fraction
from itertools import combinations
from math import comb
import sympy as s

ROOT=Path('/private/tmp/nla-audit-249/references/holden-ie-extensions-2026-09-13/submitted')
spec=importlib.util.spec_from_file_location('iv28',ROOT/'IE28_extended_results/certification/verify.py')
import sys
iv=importlib.util.module_from_spec(spec);sys.modules[spec.name]=iv;spec.loader.exec_module(iv)
t,z=s.symbols('t z')
def inside(a,b):
    a=Fraction(str(a));assert Fraction(b.lo,iv.SCALE)<=a<=Fraction(b.hi,iv.SCALE)

certs=json.loads((ROOT/'IE28_extended_results/certification/point_certificates.json').read_text())
for cert in certs:
    # Every supplied point, including stages six and seven absent from the
    # submission's direct-principal-minor regression checks.
    c=[s.Rational(a) for a,b in cert['node_box']]
    assert all(a==b for a,b in cert['node_box'])
    n=len(c)
    cardinal=[s.prod((t-c[k])/(c[j]-c[k]) for k in range(n) if k!=j) for j in range(n)]
    A=s.Matrix([[s.integrate(p,(t,0,x)) for p in cardinal] for x in c])
    inv=A.inv()
    d=[s.Rational(v) for v in cert['center']]
    iv.verify(cert)
    coeff=iv.coefficients([iv.Ball.scalar(str(x)) for x in c])
    F,J=iv.evaluate([iv.Ball.scalar(str(x)) for x in d],
                    [iv.Ball.scalar(str(x)) for x in d],coeff)
    directF=[-s.Integer(comb(n,k)) for k in range(1,n+1)]
    directJ=s.zeros(n)
    for ii,bound in coeff:
        minor=inv.extract(ii,ii).det()
        inside(minor,bound)
        k=len(ii)-1
        directF[k]+=minor*s.prod(d[i] for i in ii)
        for j in ii:directJ[k,j]+=minor*s.prod(d[i] for i in ii if i!=j)
    char=(inv*s.diag(*d)).charpoly(z).all_coeffs()
    for k in range(n):
        inside(directF[k],F[k])
        assert s.simplify(directF[k]-((-1)**(k+1)*char[k+1]-comb(n,k+1)))==0
        for j in range(n):inside(directJ[k,j],J[k][j])
    print('PASS direct Lagrange integral, all principal minors, characteristic system and Jacobian:',cert['label'],flush=True)

for q in range(2,25):
    J=sum((-1)**(q-1-k)*comb(q-1,k)*comb(q+k,k)*t**k for k in range(q))
    assert s.expand(s.legendre(q,2*t-1)-s.legendre(q-1,2*t-1)-2*(t-1)*J)==0
    assert s.expand(t*(1-t)*s.diff(J,t,2)+(1-3*t)*s.diff(J,t)+(q*q-1)*J)==0
print('PASS IE-27 independent Legendre/Jacobi coefficient and ODE checks q=2..24')

# Check the no-pivot-factor identity against directly integrated two/three
# stage matrices using exact algebraic arithmetic, rather than a D formula.
for c in [[s.Rational(1,3),s.Integer(1)],[(4-s.sqrt(6))/10,(4+s.sqrt(6))/10,s.Integer(1)]]:
    n=len(c)
    ell=[s.prod((t-c[k])/(c[j]-c[k]) for k in range(n) if k!=j) for j in range(n)]
    A=s.Matrix([[s.simplify(s.integrate(p,(t,0,x))) for p in ell] for x in c])
    inv=A.inv().applyfunc(s.simplify)
    v=[x*s.prod(x-y for j,y in enumerate(c) if j!=i) for i,x in enumerate(c)]
    D=s.Matrix(n,n,lambda i,j:v[i]/(v[j]*(c[i]-c[j])) if i!=j else 1/(2*c[i]) if i<n-1 else s.Rational(n*n+1,2))
    assert (D-inv).applyfunc(s.simplify)==s.zeros(n)
    print('PASS IE-27 inverse differentiation formula against exact direct integration q=',n)
