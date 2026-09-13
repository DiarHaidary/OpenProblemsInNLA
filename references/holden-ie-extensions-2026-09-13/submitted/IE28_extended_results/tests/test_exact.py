#!/usr/bin/env python3
"""Independent rational and symbolic regression checks (requires SymPy only)."""
from __future__ import annotations
import copy,json,random,sys
from pathlib import Path
from fractions import Fraction as Q
from math import factorial,comb
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'certification'))
import verify as iv
import sympy as sp


def enclosed(x,b):
    assert Q(b.lo,iv.SCALE)<=x<=Q(b.hi,iv.SCALE),(x,b)


def ratdet(A):
    n=len(A)
    if not n:return Q(1)
    return sum(((-1)**j)*A[0][j]*ratdet([r[:j]+r[j+1:] for r in A[1:]]) for j in range(n))


def interval_arithmetic():
    rng=random.Random(2811)
    for _ in range(1500):
        a,b,c,d=[Q(rng.randrange(-1000,1001),rng.randrange(1,1001)) for _ in range(4)]
        a,b=sorted((a,b));c,d=sorted((c,d))
        A=iv.Ball.bounds(a,b);B=iv.Ball.bounds(c,d)
        for x in (a,(a+b)/2,b):
            for y in (c,(c+d)/2,d):
                enclosed(x+y,A+B);enclosed(x-y,A-B);enclosed(x*y,A*B)
                if not c<=0<=d:enclosed(x/y,A/B)
    for n in range(1,6):
        for _ in range(10):
            A=[[Q(rng.randrange(-20,21),rng.randrange(1,20)) for _ in range(n)] for _ in range(n)]
            B=[[iv.Ball.scalar(x) for x in row] for row in A]
            enclosed(ratdet(A),iv.det_interval(B))
    print('PASS: 1500 rational interval trials and 50 exact determinant trials')


def symbolic_confluent():
    z,lam,t=sp.symbols('z lambda t')
    for n in range(2,7):
        a=sp.symbols(f'a1:{n+1}');H=sum(a[j-1]*z**j for j in range(1,n+1))
        f=[]
        for k in range(1,n+1):
            P=sp.Poly(sp.expand(H**k),z)
            f.append(sp.expand(sum(P.nth(j) for j in range(n+1))/factorial(k)))
        J=sp.Matrix(f[::-1]).jacobian(a)
        for i in range(n):
            for j in range(i+1,n):assert J[i,j]==0
            assert sp.simplify(J[i,i]-a[0]**(n-i-1)/factorial(n-i-1))==0
        print(f'PASS: formal triangular seed Jacobian, n={n}')
    # Independent Taylor-jet determinant versus the exponential expression.
    for n in range(2,6):
        a=[sp.Rational((-1)**j*(j+2),j+1) for j in range(n)]
        g=-sum((j+1)*a[j]*(1-t)**j for j in range(n))
        T=sp.Matrix(n,n,lambda k,j:sp.diff((j+1)*t**j-lam*g*t**(j+1),t,k).subs(t,1)/factorial(k))
        H=sum(a[j-1]*z**j for j in range(1,n+1))
        expected=1
        for k in range(1,n+1):
            P=sp.Poly(sp.expand(H**k),z)
            expected+=sum(P.nth(j) for j in range(n+1))*lam**k/factorial(k)
        assert sp.expand(T.det(method='domain-ge')/factorial(n)-expected)==0
        print(f'PASS: exact confluent determinant identity, n={n}')


def collocation_identities():
    t,z,lam=sp.symbols('t z lambda')
    for n in range(2,8):
        c=[sp.Rational(k*k+1,n*n+1) for k in range(1,n+1)]
        V=sp.Matrix([[v**j for j in range(n)] for v in c])
        A=sp.diag(*c)*V*sp.diag(*[sp.Rational(1,j) for j in range(1,n+1)])*V.inv()
        pi=sp.prod(t-v for v in c)
        expected=sum(sp.diff(pi,t,j).subs(t,0)*z**j for j in range(n+1))/factorial(n)
        assert sp.expand(A.charpoly(z).as_expr()-expected)==0
        if n<=5:
            C=[iv.Ball.scalar(str(v)) for v in c]
            for ii,b in iv.coefficients(C):
                exact=A.inv().extract(ii,ii).det()
                enclosed(Q(str(exact)),b)
            # Divided differences computed directly from evaluations.
            ac=[sp.Rational(j+1,j+2) for j in range(n)]
            g=-sum((j+1)*ac[j]*(1-t)**j for j in range(n))
            funcs=[(j+1)*t**j-lam*g*t**(j+1) for j in range(n)]
            rows=[]
            for k in range(n):
                rows.append([sum(f.subs(t,c[i])/sp.prod(c[i]-c[l] for l in range(k+1) if l!=i)
                                   for i in range(k+1)) for f in funcs])
            R=sp.Matrix(rows)
            assert sp.expand(R.det(method='domain-ge')/factorial(n)-
                             (sp.eye(n)-lam*A*sp.diag(*[g.subs(t,v) for v in c])).det(method='domain-ge'))==0
        print(f'PASS: exact collocation characteristic polynomial, n={n}')
    delta=sp.symbols('delta',positive=True)
    for n in range(1,16):
        L=sum((-1)**j*comb(n,j)*(t/delta)**j/factorial(j) for j in range(n+1))
        pi=(-delta)**n*factorial(n)*L
        expected=sum(sp.diff(pi,t,j).subs(t,0)*z**j for j in range(n+1))/factorial(n)
        assert sp.expand(expected-(z-delta)**n)==0
    print('PASS: exact Laguerre scalar family identities, n=1,...,15')


def certificate_tests():
    certs=[]
    for fn in ['point_certificates.json','neighborhood_certificates.json']:
        certs.extend(json.loads((ROOT/'certification'/fn).read_text()))
    assert len(certs)==12
    for c in certs:assert iv.verify(c)['passed']
    c=copy.deepcopy(certs[0]);n=len(c['center'])
    c['preconditioner']=[['0']*n for _ in range(n)]
    assert not iv.verify(c)['passed']
    c=copy.deepcopy(certs[0]);c['preconditioner']=[[str(-Q(x)) for x in row] for row in c['preconditioner']]
    assert not iv.verify(c)['passed']
    c=copy.deepcopy(certs[0]);c['node_box'][0]=['0','0']
    try:iv.verify(c)
    except ValueError:pass
    else:raise AssertionError('zero node accepted')
    print('PASS: all 12 certificates and three deliberate-corruption checks')


def main():
    interval_arithmetic();symbolic_confluent();collocation_identities();certificate_tests()
    print('ALL EXACT REGRESSION CHECKS PASSED')
if __name__=='__main__':main()
