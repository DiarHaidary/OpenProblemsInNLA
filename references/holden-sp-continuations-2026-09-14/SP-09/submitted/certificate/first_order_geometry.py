"""Exact finite algebra for the first-order splitting theorem.

All proof-critical arithmetic uses Fraction and integer arrays over Q(s),
s^2=-3. NumPy is only an array container. This verifies finite identities,
not the analytic perturbation argument or the cited Horn theorem.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'prior_round2'/'new_results'/'certificate'))
from local_geometry import (model,directions,real,sub,comm,weighted_star,
                            mm,add_pair,scale_pair,trace_pair,zero,exact_rank)

def check(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def eq(A,B) -> bool:
    return np.array_equal(A[0],B[0]) and np.array_equal(A[1],B[1])

def vec(A):
    return np.r_[A[0].ravel(),A[1].ravel()]

def fr(z):
    return [str(F(z[0])),str(F(z[1]))]

def calculate() -> dict:
    m=model(); I=real(m['I']); Z=real(zero(3)); E=m['E']; D=m['D']; C=m['C']
    star=lambda A:weighted_star(A,m['W'],m['Wi'])
    Ds=star(D); H=mm(Ds,D); Fp=sub(I,E)
    gamma=F(27,13); ell=F(4,13); gap=gamma-ell
    check(eq(mm(H,E),scale_pair(E,(gamma,0))),'Top spectral identity failed.')
    check(eq(mm(H,Fp),scale_pair(Fp,(ell,0))),'Lower spectral identity failed.')
    Pv=real((m['I']-m['R'])/2)
    rho=add_pair(scale_pair(Pv,(F(5,28),0)),scale_pair(sub(E,Pv),(F(23,28),0)))
    check(eq(star(rho),rho) and trace_pair(rho)==(1,0),'Density normalization failed.')
    for P in (E,Pv,sub(E,Pv)):
        check(eq(mm(P,P),P) and eq(star(P),P),'An active spectral projection failed.')
    check(eq(mm(Pv,sub(E,Pv)),Z),'Density eigenspaces are not orthogonal.')
    check(trace_pair(Pv)==(1,0) and trace_pair(sub(E,Pv))==(1,0),'Density ranks failed.')
    Xlist=directions(m)
    faces=[]
    for X in Xlist:
        dD=comm(X,C)
        H1=add_pair(mm(Ds,dD),mm(star(dD),D))
        L=mm(mm(E,H1),E)
        check(trace_pair(mm(rho,L))==(0,0),'Stationarity failed.')
        faces.append(vec(L))
    face_matrix=np.column_stack(faces)
    face_rank=exact_rank(face_matrix)
    check(face_rank==3,'Active-face rank is not three.')
    gauge=[]
    for j in range(3):
        P=zero(3);P[j,j]=F(1)
        gauge.extend([(zero(3),P),(zero(3),m['R']@P@m['R'])])
    gauge_matrix=np.column_stack([vec(X) for X in gauge])
    gauge_rank=exact_rank(gauge_matrix)
    check(gauge_rank==5,'Gauge tangent rank is not five.')
    for X in gauge:
        dD=comm(X,C); H1=add_pair(mm(Ds,dD),mm(star(dD),D))
        check(eq(mm(mm(E,H1),E),Z),'A gauge tangent changes the active face.')
    X=add_pair(add_pair(scale_pair(Xlist[3],(F(-3,5),0)),
                        scale_pair(Xlist[4],(F(2,5),0))),Xlist[5])
    check(eq(add_pair(X,star(X)),Z),'Flat tangent is not anti-adjoint.')
    check(exact_rank(np.column_stack([gauge_matrix,vec(X)]))==6,'Flat tangent is gauge.')
    D1=comm(X,C); D2=scale_pair(comm(X,D1),(F(1,2),0))
    H1=add_pair(mm(Ds,D1),mm(star(D1),D))
    H2=add_pair(add_pair(mm(star(D1),D1),mm(Ds,D2)),mm(star(D2),D))
    check(eq(mm(mm(E,H1),E),Z),'Flat tangent has a nonzero first-order face.')
    Q=add_pair(mm(mm(E,H2),E),scale_pair(mm(mm(mm(mm(E,H1),Fp),H1),E),(1/gap,0)))
    q=trace_pair(mm(rho,Q))
    check(q==(F(1,52),0),'Flat Schur-complement curvature is not 1/52.')
    selected=[]; current=0
    for j,col in enumerate(faces):
        trial=np.column_stack([faces[i] for i in selected+[j]])
        rank=exact_rank(trial)
        if rank>current:
            selected.append(j);current=rank
        if current==3:break
    basis=np.column_stack([gauge_matrix,vec(X)]+[vec(Xlist[j]) for j in selected])
    check(exact_rank(basis)==9,'Gauge, flat, and transverse directions do not span.')
    cs=[]; ds=[]
    for i in range(3):
        P=zero(3);P[i,i]=F(1)
        cs.append(fr(trace_pair(mm(mm(rho,Ds),real(P)))))
        ds.append(fr(trace_pair(mm(mm(rho,Ds),real(m['R']@P@m['R'])))))
    check(cs==ds,'Left and right first-order coefficients differ.')
    check(cs==[['153/364','-45/364'],['225/364','-135/364'],['0','0']],
          'Incorrect first-order coefficients.')
    return {
        'field':'Q(s), s^2=-3; a pair [x,y] denotes x+y*s',
        'gamma':str(gamma),'lower_squared_singular_value':str(ell),'spectral_gap':str(gap),
        'rho_positive_eigenvalues':['5/28','23/28'],
        'A_coefficients':cs,'B_coefficients_before_subtraction':ds,
        'face_rank':face_rank,'gauge_rank':gauge_rank,'gauge_plus_flat_rank':6,
        'full_tangent_rank':9,'transverse_direction_indices_zero_based':selected,
        'flat_direction_coefficients':['0','0','0','-3/5','2/5','1','0','0','0'],
        'flat_schur_curvature':fr(q),
        'flat_unreduced_H2_density_trace':fr(trace_pair(mm(rho,H2))),
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--witness',type=Path,default=Path(__file__).with_name('first_order_witness.json'))
    p.add_argument('--write-witness',action='store_true')
    p.add_argument('--report',type=Path)
    args=p.parse_args(); result=calculate()
    if args.write_witness:
        args.witness.write_text(json.dumps(result,indent=2)+'\n')
    else:
        expected=json.loads(args.witness.read_text())
        check(result==expected,'The stored witness differs from the exact recomputation.')
    report={'result':'PASS','finite_algebra':result,
            'scope':'Finite identities only. The analytic proof and Horn input are in the manuscript.'}
    if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
