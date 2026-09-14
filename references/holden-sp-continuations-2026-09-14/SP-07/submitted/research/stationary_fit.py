#!/usr/bin/env python3
"""Numerical exploration of the stationary two-line model and an inherited bulk.

The formal selected-gap quotient is not the infinite matching ratio and is not a
finite SP-07 bound. Local optimization does not prove a global parameter optimum.
The rational chosen-parameter enclosure is provided separately by verify_model.py.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
from fractions import Fraction
import argparse,json,time,hashlib
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1]


def integral(b,c):
    if b<0 or c<0 or b+c>=1:raise ValueError('Outside the parameter simplex')
    q=lambda t:(1+t*t-2*c*t)**2-b*b*(1+t*t)**2
    return quad(lambda t:2/np.sqrt(q(t)),0,1,epsabs=2e-12,epsrel=2e-12,limit=200)[0]


def formal(b,c):
    I=integral(b,c)
    return np.sqrt((b+c)**2+(np.pi/(2*I))**2)


def evaluate(b,c):
    I=integral(b,c);T=I/np.pi;B=b*T;C=c*T
    ys=(B+C)/2;yc=(B-C)/2
    rhs=lambda t,y:np.sqrt(np.maximum(0,(T-C*np.sin(y))**2-B*B))
    sol=solve_ivp(rhs,(0,np.pi),[0.],method='DOP853',rtol=2e-12,atol=1e-13,
                  dense_output=True,max_step=np.pi/200)
    if not sol.success:raise RuntimeError(sol.message)
    end=float(sol.y[0,-1]);endpoint_error=abs(end-np.pi/2)
    phi=lambda t:float(sol.sol(t)[0])
    h=[];g=[]
    for k in range(10):
        h.append(quad(lambda t:np.sin(phi(t))*np.sin((k+.5)*t)/np.pi,0,np.pi,epsabs=2e-12)[0])
        g.append(quad(lambda t:np.cos(phi(t))*np.cos((k+.5)*t)/np.pi,0,np.pi,epsabs=2e-12)[0])
    return dict(b=b,c=c,I=I,T=T,B=B,C=C,y_selected=ys,y_complement=yc,
                formal_ratio=formal(b,c),actual_infinite_ratio=np.sqrt(.25+B*B)/T,
                endpoint_error=endpoint_error,h_coefficients=h,g_coefficients=g)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--optimize',action='store_true')
    parser.add_argument('--output',type=Path,default=ROOT/'results/stationary_fit.json')
    parser.add_argument('--finite-source',type=Path,default=ROOT/'research/inputs/n193_prior_search_candidate.npz')
    a=parser.parse_args();begin=time.perf_counter()
    spec=json.loads((ROOT/'certificates/model_parameters.json').read_text())
    b=float(Fraction(spec['b']));c=float(Fraction(spec['c']));out=evaluate(b,c)
    records=[]
    if a.optimize:
        def objective(x):
            if x[0]<0 or x[1]<0 or sum(x)>=1:return 10+sum(np.abs(x))
            return -formal(*x)
        for seed in [[.59,.37],[.4,.5],[.75,.18]]:
            opt=minimize(objective,seed,method='Nelder-Mead',
                         options=dict(maxiter=1500,xatol=1e-11,fatol=2e-14))
            records.append(dict(start=seed,parameters=opt.x.tolist(),formal_ratio=-float(opt.fun),
                                success=bool(opt.success),iterations=int(opt.nit),
                                scope='Local numerical optimum only'))
    z=np.load(a.finite_source);alpha=z['alpha'];U=z['U'];p=(len(alpha)+1)//2
    step=1/(.25+1j*out['y_selected'])
    ms=np.array([((j+1)//2)*(1 if j%2==0 else -1) for j in range(p)])
    predicted=1+ms*step
    cs=(.25+1j*out['y_complement'])*step
    mc=np.array([((j+1)//2)*(1 if j%2==0 else -1) for j in range(len(alpha)-p)])
    predicted_c=cs+mc*step
    coeffs=[]
    for k in range(10):
        coeffs.append(dict(k=k,model_h=out['h_coefficients'][k],finite_h=float(U[0,2*k].real),
                          model_g=out['g_coefficients'][k],finite_g=float(U[0,p+2*k].real)))
    H=(alpha[:,None]+alpha[None,:])*U
    fit=dict(source=str(a.finite_source.relative_to(ROOT)),
             source_sha256=hashlib.sha256(a.finite_source.read_bytes()).hexdigest(),n=len(alpha),
             selected_first_21_max_error=float(np.max(np.abs(alpha[:21]-predicted[:21]))),
             complement_first_21_max_error=float(np.max(np.abs(alpha[p:p+21]-predicted_c[:21]))),
             selected_all_max_error=float(np.max(np.abs(alpha[:p]-predicted))),
             complement_all_max_error=float(np.max(np.abs(alpha[p:]-predicted_c))),
             prior_candidate_float_norm=float(np.linalg.norm(H,2)),
             model_rescaled_norm=2/out['formal_ratio'],coefficients=coeffs,
             scope='Fit to the inherited floating-point search candidate, not a convergence proof')
    out.update(local_optimizations=records,finite_bulk_fit=fit,seconds=time.perf_counter()-begin,
               scope='Stationary model diagnostics only. No new finite lower or unrestricted upper bound.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
