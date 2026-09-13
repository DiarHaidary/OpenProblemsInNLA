#!/usr/bin/env python3
"""Numerical implementation checks; these are not additional existence proofs."""
from pathlib import Path
import sys
from math import comb
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]
for folder in ['cluster','numerics','prior_work/src']:
    sys.path.insert(0,str(ROOT/folder))
from confluent import seed,fcoeff,pencil
from continue_cluster import pencil_matrices,FJ,values,continuation
from ie28 import collocation_matrix

def main():
    mp.mp.dps=100
    for n in range(2,21):
        a=seed(n)
        assert max(abs(fcoeff(a,k)-(-1)**k*comb(n,k)) for k in range(1,n+1))<mp.mpf('1e-75')
    print('PASS: high-precision seed residuals through n=20')
    for n in range(2,8):
        c=[mp.mpf(i*i+1)/(n*n+1) for i in range(1,n+1)]
        a=[-mp.mpf(j+1)/(j+2) for j in range(n)]
        A=collocation_matrix(c);G=mp.diag(values(c,a))
        B0,B1=pencil(c,a);Bs=pencil_matrices(c)
        K=sum((a[j]*Bs[j] for j in range(n)),mp.zeros(n))
        for lam in [mp.mpf('.1'),mp.mpf('.5'),mp.mpf('1.2')]:
            exact=mp.det(mp.eye(n)-lam*A*G)
            assert abs(mp.det(B0-lam*B1)/mp.factorial(n)-exact)<mp.mpf('1e-80')
            assert abs(mp.det(mp.eye(n)-lam*K)-exact)<mp.mpf('1e-80')
        F,J=FJ(a,Bs)
        for k in range(n):
            for j in range(n):
                def fun(x):
                    b=a.copy();b[j]=x
                    return FJ(b,Bs,False)[0][k]
                assert abs(mp.diff(fun,a[j])-J[k,j])<mp.mpf('1e-75')
    print('PASS: both pencils and analytic Jacobian versus independent evaluations, n=2,...,7')
    mp.mp.dps=60
    out=continuation([mp.mpf(i)/8 for i in range(1,9)])
    assert out['pass'] and all(mp.mpf(d)>0 for d in out['d'])
    print('PASS: eight-stage numerical continuation smoke test (not a certificate)')
    print('ALL NUMERICAL IMPLEMENTATION CHECKS PASSED')
if __name__=='__main__':main()
