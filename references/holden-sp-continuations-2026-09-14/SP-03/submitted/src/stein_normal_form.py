"""Exact Stein normal form of the regular SP-03 critical-point reduction.

All matrices are over a characteristic-zero field, with ordinary transpose.
The data are in Q-metric coordinates. These symbolic constructions are intended
for small-rank checking; the accompanying proof applies in every rank.
"""
from __future__ import annotations
import sympy as sp
from pole_factorization import symmetric_basis, skew_basis


def induced_matrix(C, *, symmetric=True):
    """Coordinate matrix of Z -> C Z C.T, on Sym or skew matrices."""
    C=sp.Matrix(C)
    if C.rows != C.cols or not C.rows:
        raise ValueError('C must be a nonempty square matrix')
    m=C.rows
    basis=symmetric_basis(m) if symmetric else skew_basis(m)
    pairs=[(i,j) for i in range(m) for j in range(i if symmetric else i+1,m)]
    result=sp.zeros(len(basis))
    for j,E in enumerate(basis):
        image=C*E*C.T
        for i,(a,b) in enumerate(pairs):result[i,j]=image[a,b]
    return result


def stein_solutions(C,b,c):
    """Solve the two symmetric Stein equations exactly; fail at a pole."""
    C,b,c=map(sp.Matrix,(C,b,c));m=C.rows
    if C.shape!=(m,m) or b.shape!=C.shape or c.shape!=C.shape:
        raise ValueError('Equal square shapes required')
    I=sp.eye(m);E=symmetric_basis(m)
    pairs=[(i,j) for i in range(m) for j in range(i,m)]
    rs=(C+I)*b.T+b*(C+I).T
    rt=c.T*(C+I)+(C+I).T*c
    ms=induced_matrix(C)-sp.eye(len(E))
    mt=induced_matrix(C.T)-sp.eye(len(E))
    sv=ms.inv()*sp.Matrix([rs[i,j] for i,j in pairs])
    tv=mt.inv()*sp.Matrix([rt[i,j] for i,j in pairs])
    S=sum((sv[i]*E[i] for i in range(len(E))),sp.zeros(m))
    T=sum((tv[i]*E[i] for i in range(len(E))),sp.zeros(m))
    return S,T


def evaluate(C,b,c,d):
    """Return (potential, 4*gradient_C, S, T), all exact SymPy matrices."""
    C,b,c,d=map(sp.Matrix,(C,b,c,d));m=C.rows;I=sp.eye(m)
    if any(M.shape!=(m,m) for M in (C,b,c,d)):
        raise ValueError('Equal square shapes required')
    S,T=stein_solutions(C,b,c)
    V=(C+I).inv();Y=V.T
    phi=-sp.trace((C+I)*d.T)/4-4*sp.trace(V)-sp.trace(T*(C+I)*b.T)/4
    gradient4=T*C*S-c*S-T*b-d+16*Y*Y
    return phi,gradient4,S,T


def euler_characteristic(m:int):
    """Compactly supported Euler characteristic of the universal domain."""
    if not isinstance(m,int) or m<0:raise ValueError('m must be a nonnegative integer')
    from sympy.functions.combinatorial.numbers import stirling
    return sum(stirling(m+1,r+1,kind=2)*(-2)**r*sp.factorial(r) for r in range(m+1))
