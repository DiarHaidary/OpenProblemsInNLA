"""Exploratory monodromy using known symmetries of the critical equations.

Negation, conjugation, inverse/symplectic adjoint, and metric adjoint map a
known fiber to a known fiber. Two numerical continuation edges return to the
original data. All endpoints remain untrusted until exact certification.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from numba import njit
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,time,json
from fast_general import evaluate,track,refine

@njit(cache=True,nogil=True)
def two_edges(a,U,Us,V,mode):
    m=U.shape[0]//2
    if mode==0:y=-a
    elif mode==1:y=np.conj(a)
    else:
        try:
            g,H,gp,S,T=evaluate(a,U,np.zeros_like(U));A=a.reshape((m,m))
            y=(S@A.T@T+np.linalg.inv(A)).ravel()
        except:return a,False,0
    y,ok=refine(y,Us)
    if not ok:return y,False,0
    y,ok,s1=track(y,Us,V)
    if not ok:return y,False,s1
    y,ok,s2=track(y,V,U)
    return y,ok,s1+s2

def main(args):
    z=np.load(args.input,allow_pickle=False);U=z['U'];m=U.shape[0]//2;n=2*m
    roots=list(z['roots']);rng=np.random.default_rng(args.seed)
    p=(rng.normal(size=m*m)+1j*rng.normal(size=m*m))/m;width=2e-3;buckets={}
    def key(a):
        v=np.dot(p,a);return int(np.floor(v.real/width)),int(np.floor(v.imag/width))
    for i,a in enumerate(roots):buckets.setdefault(key(a),[]).append(i)
    def add(a):
        if not np.isfinite(a).all() or np.max(abs(a))>1e7:return False
        x,y=key(a)
        for xx in range(x-2,x+3):
            for yy in range(y-2,y+3):
                for i in buckets.get((xx,yy),[]):
                    if np.max(abs(a-roots[i]))<1e-6*(1+np.max(abs(a))):return False
        buckets.setdefault((x,y),[]).append(len(roots));roots.append(a.copy());return True
    two_edges(roots[0],U,-U,1j*U,0)
    start=time.perf_counter();lastsave=start;paths=failed=steps=0;loops=args.start_mode
    print(json.dumps({'event':'start','rank':m,'roots':len(roots)}),flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        while time.perf_counter()-start<args.seconds and len(roots)<args.max_roots:
            mode=loops%4;loops+=1
            if mode==0:Us=-U
            elif mode==1:Us=U.conj()
            else:
                sign=-1 if mode==2 else 1
                Us=np.block([[U[m:,m:].T,sign*U[:m,m:].T],[sign*U[m:,:m].T,U[:m,:m].T]])
            V=(U+Us)/2+(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))/np.sqrt(n)
            order=list(rng.permutation(len(roots)))[:args.per_mode];ix=0
            while ix<len(order) and time.perf_counter()-start<args.seconds:
                jobs=order[ix:ix+64];ix+=len(jobs)
                futures=[pool.submit(two_edges,roots[j],U,Us,V,mode) for j in jobs]
                for f in futures:
                    y,ok,st=f.result();paths+=1;steps+=st
                    if not ok:failed+=1
                    elif add(y):
                        if len(order)<args.per_mode:order.append(len(roots)-1)
                now=time.perf_counter()
                if now-lastsave>15:
                    report={'rank':m,'mode':mode,'loops':loops,'roots':len(roots),'paths':paths,'failed':failed,'steps':steps,'elapsed_seconds':now-start,'completeness_proved':False}
                    print(json.dumps(report),flush=True)
                    np.savez_compressed(args.output,U=U,roots=np.asarray(roots),loops=loops)
                    with args.output.with_suffix('.jsonl').open('a') as f:f.write(json.dumps(report)+'\n')
                    lastsave=time.perf_counter()
    np.savez_compressed(args.output,U=U,roots=np.asarray(roots),loops=loops)
    print(json.dumps({'event':'finish','roots':len(roots),'paths':paths,'elapsed_seconds':time.perf_counter()-start}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--seconds',type=float,default=600);p.add_argument('--workers',type=int,default=4);p.add_argument('--seed',type=int,default=612947)
    p.add_argument('--max-roots',type=int,default=85000)
    p.add_argument('--per-mode',type=int,default=1024);p.add_argument('--start-mode',type=int,default=1)
    main(p.parse_args())
