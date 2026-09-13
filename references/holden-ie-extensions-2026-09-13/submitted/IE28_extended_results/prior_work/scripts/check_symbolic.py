#!/usr/bin/env python3
"""Exact algebra checks supporting the derivations in writeup.pdf."""
from pathlib import Path
import sys
import sympy as S


def zero(expr, name):
    value = S.cancel(expr)
    if value != 0:
        raise AssertionError(f"{name}: nonzero residual {value}")
    print("PASS", name)


def main():
    a, b, c, r = S.symbols("a b c r", positive=True)
    cs = [a, b, c]
    s1, s2, s3 = a + b + c, a*b + a*c + b*c, a*b*c
    h = [1/t + sum(1/(t-u) for u in cs if u != t) for t in cs]
    for m in (2, 3):
        ds = [t*(t+r)/(m*t+r) for t in cs]
        tr = sum(q*d for q, d in zip(h, ds)) - 3
        den = S.prod(m*t+r for t in cs)
        if m == 2:
            expected = r*(2*s2 + 3*s1*r + 3*r*r)/den
            zero(tr-expected, "three-stage positive endpoint trace identity")
        else:
            F = 6*S.prod(t+r for t in cs)-den
            zero(tr*den-(F-2*(r**3+3*s3)), "three-stage negative endpoint identity")
            zero(F-(5*r**3+3*s1*r**2-3*s2*r-21*s3), "repeated-root determinant expansion")

    x, y, A, B, C = S.symbols("x y A B C")
    f = lambda t: t*(A*t*t+B*t+C)/(3*A*t*t+2*B*t+C)
    H = (3*A*A*x*x*y*y+2*A*B*x*y*(x+y)+A*C*(x*x+y*y)
         +2*(B*B-A*C)*x*y+B*C*(x+y)+C*C)
    zero((f(x)-f(y))/(x-y)-H/((3*A*x*x+2*B*x+C)*(3*A*y*y+2*B*y+C)),
         "cancellation-free divided difference")

    # n=2 determinant equation has the unique positive root r=sqrt(2ab).
    d1, d2 = a*(a+r)/(2*a+r), b*(b+r)/(2*b+r)
    num = S.cancel(2*d1*d2/(a*b)-1).as_numer_denom()[0]
    zero(S.rem(num, r*r-2*a*b, r), "two-stage determinant polynomial reduction")
    t = S.symbols("t")
    ell = [(t-b)/(a-b), (t-a)/(b-a)]
    A2 = S.Matrix([[S.integrate(q, (t, 0, v)) for q in ell] for v in [a, b]])
    L2 = A2.inv()*S.diag(d1, d2)
    numtr = S.cancel(S.trace(L2)-2).as_numer_denom()[0]
    zero(S.rem(numtr, r*r-2*a*b, r), "two-stage trace polynomial reduction")

    for n in range(2, 7):
        vals = [S.Rational(k*k+1, n*n+1) for k in range(1, n+1)]
        V = S.Matrix([[v**k for k in range(n)] for v in vals])
        Ac = S.diag(*vals)*V*S.diag(*[S.Rational(1,k) for k in range(1,n+1)])*V.inv()
        w = [1/S.prod(vals[i]-vals[j] for j in range(n) if j!=i) for i in range(n)]
        T = S.diag(*[vals[i]/w[i] for i in range(n)])
        M = S.Matrix(n,n,lambda i,j: 1/(vals[i]-vals[j]) if i!=j else
                     1/vals[i]+sum(1/(vals[i]-vals[k]) for k in range(n) if k!=i))
        assert T.inv()*Ac.inv()*T == M
        print(f"PASS exact inverse similarity, rational example n={n}")
        zero(Ac.det()-S.prod(vals)/S.factorial(n), f"exact determinant, rational example n={n}")
        alphas = [S.Rational(k, n+2) for k in range(1,n)]
        p = t*S.prod(t+v for v in alphas)
        q = S.diff(p,t)
        d = [S.cancel(p.subs(t,v)/q.subs(t,v)) for v in vals]
        eigvec = S.Matrix([q.subs(t,v) for v in vals])
        assert Ac.inv()*S.diag(*d)*eigvec == eigvec
        print(f"PASS exact ansatz eigenvalue one, rational example n={n}")
        if n <= 4:
            L = [S.prod((t-vals[k])/(vals[j]-vals[k]) for k in range(n) if k!=j) for j in range(n)]
            Aint = S.Matrix([[S.integrate(q,(t,0,v)) for q in L] for v in vals])
            assert Aint == Ac
            print(f"PASS direct integral comparison, rational example n={n}")

    e2, z = S.symbols("e2 z")
    p3 = z**3-3*z**2+e2*z-1
    zero(p3.subs(z,1)-(e2-3), "cubic spectral completion")
    B4 = S.diag(1,2,S.Matrix([[S.Rational(1,2),-S.Rational(1,2)],
                              [S.Rational(1,2),S.Rational(1,2)]]))
    assert S.trace(B4) == 4 and B4.det() == 1 and (B4-S.eye(4)).det() == 0
    assert B4.charpoly(z).as_expr() != (z-1)**4
    print("PASS four-stage invariant insufficiency example (not a collocation counterexample)")
    print("ALL SYMBOLIC CHECKS PASSED")


if __name__ == "__main__":
    main()
