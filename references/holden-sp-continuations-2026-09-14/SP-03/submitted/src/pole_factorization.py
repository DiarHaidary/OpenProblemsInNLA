"""Exact symbolic constructions for the factored regular-chart denominator."""
from __future__ import annotations
import sympy as sp


def symmetric_basis(m: int):
    result=[]
    for i in range(m):
        for j in range(i,m):
            E=sp.zeros(m);E[i,j]=1;E[j,i]=1;result.append(E)
    return result


def skew_basis(m: int):
    result=[]
    for i in range(m):
        for j in range(i+1,m):
            E=sp.zeros(m);E[i,j]=1;E[j,i]=-1;result.append(E)
    return result


def matrices(A,B):
    """Return L_ij=tr(A E_i B.T E_j) and K(Z)=A Z B.T+B Z A.T.

    L uses the unnormalized symmetric basis, while K uses coordinate
    coefficients in the strict-upper skew basis (not a Frobenius Gram form).
    """
    A=sp.Matrix(A);B=sp.Matrix(B)
    if A.rows!=A.cols or B.shape!=A.shape:raise ValueError('Equal square shapes required')
    m=A.rows;E=symmetric_basis(m);Z=skew_basis(m)
    L=sp.Matrix([[sp.trace(A*e*B.T*f) for f in E] for e in E])
    pairs=[(i,j) for i in range(m) for j in range(i+1,m)]
    K=sp.zeros(len(Z))
    for j,z in enumerate(Z):
        image=A*z*B.T+B*z*A.T
        for i,(a,b) in enumerate(pairs):K[i,j]=image[a,b]
    return L,K
