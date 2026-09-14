"""Exploratory full-polynomial Newton basin sampling, never a completeness test.

All inputs/outputs are in ordinary Frobenius coordinates. Stored centers need
independent exact contraction and separation checks before any counting claim.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import argparse,sys,time,json
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from numba import njit
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from polynomial import evaluate

@njit(cache=True,nogil=True)
def newton(x,u,n):
    y=x.copy();quality=1e300;best=y.copy();last=1e300
    for k in range(35):
        F,H=evaluate(y,u,n)
        try:delta=np.linalg.solve(H,F)
        except:return best,False
        size=np.max(np.abs(y));err=np.max(np.abs(delta))/(1+size)
        if not np.isfinite(err):return best,False
        if err<quality:quality=err;best=y.copy()
        if err<3e-12:break
        step=1.
        if err>2.:step=2./err
        y-=step*delta
        if np.max(np.abs(y))>1e7:return best,False
        if k>=15 and err>last*1.5 and quality<1e-7:break
        last=err
    F,H=evaluate(best,u,n)
    size=np.max(np.abs(best));scale=1+size*size+np.max(np.abs(u))*size
    return best,quality<1e-7 and np.max(np.abs(F))/scale<1e-10

@njit(cache=True,nogil=True)
def batch(xs,u,n):
    out=xs.copy();oks=np.empty(len(xs),np.bool_)
    for i in range(len(xs)):out[i],oks[i]=newton(xs[i],u,n)
    return out,oks

def main(args):
    z=np.load(args.input,allow_pickle=False);u=z['U'].ravel();roots=list(z['roots'])
    n=int(np.sqrt(len(u)));rng=np.random.default_rng(args.seed)
    proj=(rng.normal(size=n*n)+1j*rng.normal(size=n*n))/n
    width=2e-3;buckets={}
    def key(x):
        q=np.dot(proj,x);return int(np.floor(q.real/width)),int(np.floor(q.imag/width))
    for i,x in enumerate(roots):buckets.setdefault(key(x),[]).append(i)
    def add(x):
        if not np.isfinite(x).all():return False
        a,b=key(x)
        for aa in range(a-2,a+3):
            for bb in range(b-2,b+3):
                for i in buckets.get((aa,bb),[]):
                    if np.max(abs(x-roots[i]))<1e-6*(1+np.max(abs(x))):return False
        buckets.setdefault((a,b),[]).append(len(roots));roots.append(x.copy());return True
    batch(np.asarray(roots[:1]),u,n)
    start=time.perf_counter();attempts=successful=loops=0;lastsave=start
    print(json.dumps({'event':'start','rank':n//2,'roots':len(roots)}),flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        while time.perf_counter()-start<args.seconds and len(roots)<args.max_roots:
            loops+=1;futures=[]
            scales=[.005,.02,.05,.1,.2,.4,.8,1.5,3.]
            for w in range(args.workers):
                ids=rng.integers(len(roots),size=64)
                xs=np.asarray([roots[i] for i in ids]);sizes=np.max(abs(xs),axis=1)
                scale=scales[(loops+w-1)%len(scales)]
                noise=(rng.normal(size=xs.shape)+1j*rng.normal(size=xs.shape))/n
                # Alternate relative and absolute perturbations.
                if loops%3:noise*=((1+sizes)*scale)[:,None]
                else:noise*=scale
                xs=xs+noise
                futures.append(pool.submit(batch,xs,u,n))
            for f in futures:
                ys,oks=f.result();attempts+=len(ys);successful+=sum(oks)
                for y,ok in zip(ys,oks):
                    if ok:add(y)
            now=time.perf_counter()
            if now-lastsave>15:
                report={'rank':n//2,'roots':len(roots),'attempts':attempts,'numerical_successes':int(successful),'elapsed_seconds':now-start,'completeness_proved':False}
                print(json.dumps(report),flush=True)
                np.savez_compressed(args.output,U=u,roots=np.asarray(roots))
                with args.output.with_suffix('.jsonl').open('a') as f:f.write(json.dumps(report)+'\n')
                lastsave=time.perf_counter()
    np.savez_compressed(args.output,U=u,roots=np.asarray(roots))
    print(json.dumps({'event':'finish','roots':len(roots),'attempts':attempts,'elapsed_seconds':time.perf_counter()-start}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--seconds',type=float,default=120);p.add_argument('--workers',type=int,default=4)
    p.add_argument('--seed',type=int,default=57471);p.add_argument('--max-roots',type=int,default=85000)
    main(p.parse_args())
