#!/usr/bin/env python3
"""Recover a global layerwise convex-hull relaxation and an exact gap witness.

The relaxation optimum is 81/16, not the true CP growth factor. Generation uses
SciPy and SymPy; verify_layer_hull.py checks the resulting rational witness
using only the standard library. A convex mixture is not a rank-one layer.
"""
from pathlib import Path
from fractions import Fraction as Q
import sys,json
import numpy as np
import sympy as sp
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from verify_layer_hull import model

def run():
    vertices,P,A=model();N=len(vertices)
    result=linprog([-float(v) for v in P[4]],A_ub=np.array(A,dtype=float),b_ub=np.zeros(len(A)),
        A_eq=np.array(P[:1],dtype=float),b_eq=[1.],bounds=(0,None),method='highs')
    if not result.success:raise RuntimeError(result.message)
    support=[i for i,x in enumerate(result.x) if x>1e-9]
    active=[i for i,x in enumerate(np.array(A,dtype=float)@result.x) if abs(x)<1e-8]
    rows=[[sp.Rational(P[0][j]) for j in support]]+[[sp.Rational(A[i][j]) for j in support] for i in active]
    rhs=[sp.Integer(1)]+[sp.Integer(0)]*len(active)
    M=sp.Matrix(rows);independent=M.T.rref()[1]
    assert len(independent)==len(support)
    M0=M[list(independent),:];b=sp.Matrix([rhs[i] for i in independent]);x=M0.inv()*b
    assert all(a>=0 for a in x)
    data=dict(description='Exact feasible point of the layerwise convex-hull RELAXATION; not a CP matrix.',
        support=[dict(vertex=i,weight=str(a)) for i,a in zip(support,x)],
        objective='81/16',generation='SciPy linprog support, followed by exact rational linear algebra',
        global_solution=False)
    (ROOT/'data'/'layer_hull_witness.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Generated exact relaxation witness with',len(support),'nonzero corner weights.')
if __name__=='__main__':run()
