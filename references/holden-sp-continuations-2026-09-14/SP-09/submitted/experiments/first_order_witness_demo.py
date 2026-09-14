"""Construct first-order upper-bound witnesses for the six-dimensional example.

The exact theorem is in the manuscript. This floating-point demonstration
checks the construction and its Taylor behavior; it does not prove a lower
bound or a counterexample to SP-09.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import block_diag,expm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'prior_round2'/'new_results'/'certificate'))
from local_geometry import model,directions


def check(ok: bool, message: str) -> None:
    if not ok:raise ValueError(message)


def run() -> dict:
    m=model();S=np.diag(np.sqrt([float(w) for w in m['w']]))
    def physical(pair):
        x=np.asarray(pair[0],float)+1j*np.sqrt(3)*np.asarray(pair[1],float)
        return S@x@np.linalg.inv(S)
    R=physical((m['R'],np.zeros((3,3))));D=physical(m['D']);E=physical(m['E'])
    C=physical(m['C']);Pv=(np.eye(3)-R)/2;rho=(5*Pv+23*(E-Pv))/28
    basis=[physical(x) for x in directions(m)]
    face=[]
    for j in [3,4,6]:
        dD=basis[j]@C-C@basis[j]
        face.append(E@(D.conj().T@dD+dD.conj().T@D)@E)
    gram=np.array([[np.trace(x@y).real for y in face] for x in face])
    dual=[sum((np.linalg.inv(gram)[j,h]*face[h] for h in range(3)),np.zeros((3,3),complex)) for j in range(3)]
    H=[np.diag([1.,-1.]),np.diag([0.,2.]),np.diag([-1.,1.])]
    K=[np.diag([-2.,1.]),np.diag([1.,-1.]),np.diag([0.,3.])]
    c=[(153-45j*np.sqrt(3))/364,(225-135j*np.sqrt(3))/364,0]
    Z=[2*c[0].real*H[0],2*c[1].real*H[1],-2*c[0].real*K[0],-2*c[1].real*K[1]]
    means=np.array([np.trace(z).real/2 for z in Z]);lengths=np.array([(np.linalg.eigvalsh(z)[-1]-np.linalg.eigvalsh(z)[0])/2 for z in Z])
    exact_slope=F(603,364)
    check(abs(means.sum()-float(exact_slope))<1e-12,'Incorrect example slope.')
    check(2*max(lengths)<sum(lengths),'The example does not admit a closed quadrilateral.')
    low=max(abs(lengths[0]-lengths[1]),abs(lengths[2]-lengths[3]))
    high=min(lengths[0]+lengths[1],lengths[2]+lengths[3]);d=(low+high)/2
    vectors=[]
    for j,sign in [(0,1),(2,-1)]:
        l1,l2=lengths[j:j+2]
        z1=(d*d+l1*l1-l2*l2)/(2*d*l1)
        z2=(d*d+l2*l2-l1*l1)/(2*d*l2)
        x1=np.sqrt(max(0.,1-z1*z1));x2=-l1*x1/l2
        vectors.extend([np.array([x1,sign*z1]),np.array([x2,sign*z2])])
    check(np.linalg.norm(sum((l*v for l,v in zip(lengths,vectors)),np.zeros(2)))<1e-12,'Polygon does not close.')
    us=[]
    for z,mean,vector in zip(Z,means,vectors):
        sign=1 if z[0,0].real>mean else -1
        theta=np.arctan2(sign*vector[0],sign*vector[1]);ct=np.cos(theta/2);st=np.sin(theta/2)
        us.append(np.array([[ct,-st],[st,ct]],complex))
    V=block_diag(us[0].conj().T,us[1].conj().T,np.eye(2));W=block_diag(us[2],us[3],np.eye(2))
    RR=np.kron(R,np.eye(2));DD=np.kron(D,np.eye(2));EE=np.kron(E,np.eye(2))
    dh=V.conj().T@block_diag(*H)@V-RR@W@block_diag(*K)@W.conj().T@RR
    G=EE@(DD.conj().T@dh+dh.conj().T@DD)@EE
    target=np.kron(E,float(exact_slope)*np.eye(2))-G
    def partial(f,x):
        return np.einsum('ji,iajb->ab',f,x.reshape(3,2,3,2))
    check(np.linalg.norm(partial(rho,target),2)<1e-12,'First-order residual is not in the face-map range.')
    coeff=[partial(f,target) for f in dual]
    S0=sum((np.kron(basis[j],t) for j,t in zip([3,4,6],coeff)),np.zeros((6,6),complex))
    check(np.linalg.norm(S0+S0.conj().T,2)<1e-11,'Correction is not skew-Hermitian.')
    check(np.linalg.norm(sum((np.kron(f,t) for f,t in zip(face,coeff)),np.zeros((6,6),complex))-target,2)<1e-11,'Face correction failed.')
    a0=np.array([1,(4+5j*np.sqrt(3))/13,(-1+2j*np.sqrt(3))/13]);rows=[]
    for t in [.03,.01,.003,.001,.0003,.0001]:
        A=block_diag(*(a*np.eye(2)+t*h for a,h in zip(a0,H)))
        B=block_diag(*(-a*np.eye(2)+t*k for a,k in zip(a0,K)))
        U=V@expm(t*S0)@RR@W
        defect=float(np.linalg.norm(U.conj().T@U-np.eye(6),2))
        val=float(np.linalg.norm(A-U@B@U.conj().T,2)**2)
        check(defect<1e-11,'Constructed witness is not numerically unitary.')
        rows.append({'t':t,'feasible_squared_norm':val,'observed_first_order_slope':(val-27/13)/t,
                     'second_order_remainder_ratio':(val-27/13-t*float(exact_slope))/t**2,
                     'unitarity_defect':defect})
    check(abs(rows[-1]['observed_first_order_slope']-float(exact_slope))<.01,'Taylor slope did not converge in the demonstration.')
    return {'result':'PASS: floating-point construction checks','base_dimension':6,
            'exact_first_order_coefficient':'603/364','rows':rows,
            'scope':'Constructive feasible upper bounds only; not numerical lower-bound certification.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path);args=p.parse_args()
    result=run()
    if args.report:args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
