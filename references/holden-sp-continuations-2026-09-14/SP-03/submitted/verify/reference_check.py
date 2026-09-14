"""Independently recheck a sample (or all centers) with Python integers.

This does not import or call the C++ backend. Jacobian inverses are untrusted
floating-point proposals. Every contraction inequality uses the separate
Fraction/int implementation in reference.py. A sampled run is not a full-file
check. Optional worker processes change only execution order, not proof tests.
"""
from __future__ import annotations
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import argparse,sys,time,json,hashlib,multiprocessing
from concurrent.futures import ProcessPoolExecutor
import numpy as np
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from polynomial import evaluate
from reference import check_one,disjoint
from separation import check_disjoint,pow2

_U=None
_N=None

def _initialize(u,n):
    global _U,_N
    _U=u
    _N=n

def _check_indexed(item):
    i,x=item
    _,H=evaluate(x,_U,_N)
    B=np.linalg.inv(H)
    ok,r,eta,z0,z2=check_one(x,_U,B,_N)
    if not ok:
        raise AssertionError(f'Exact Python certificate failed at input index {i}')
    # The reference check chooses an exact power-of-two radius.
    re=r.numerator.bit_length()-r.denominator.bit_length()
    if r!=pow2(re):raise AssertionError('The reference radius is not a power of two')
    return int(i),int(re)

def main(args):
    with np.load(args.path,allow_pickle=False) as z:
        roots=z['roots'].copy();u=z['U'].ravel().copy()
    if roots.dtype!=np.dtype('complex128') or u.dtype!=np.dtype('complex128'):
        raise ValueError('Exact complex binary64 data required')
    if roots.ndim!=2 or not len(roots):raise ValueError('Nonempty center matrix required')
    n=int(round(roots.shape[1]**.5))
    if n<2 or n%2 or n*n!=roots.shape[1] or u.size!=n*n:
        raise ValueError('Invalid matrix shapes')
    if not np.isfinite(roots).all() or not np.isfinite(u).all():
        raise ValueError('All data and centers must be finite')
    if args.sample<1 or args.workers<1:raise ValueError('sample and workers must be positive')
    indices=np.arange(len(roots)) if args.all else np.sort(np.random.default_rng(args.seed).choice(len(roots),min(args.sample,len(roots)),replace=False))
    started=time.perf_counter();exponents=[]
    items=((int(i),roots[i]) for i in indices)
    if args.workers==1:
        _initialize(u,n)
        results=map(_check_indexed,items)
        for count,(i,re) in enumerate(results,1):
            exponents.append(re)
            if count%1000==0:
                print(json.dumps({'checked':count,'seconds':time.perf_counter()-started}),flush=True)
    else:
        context=multiprocessing.get_context('spawn')
        with ProcessPoolExecutor(max_workers=args.workers,mp_context=context,
                                 initializer=_initialize,initargs=(u,n)) as pool:
            for count,(i,re) in enumerate(pool.map(_check_indexed,items,chunksize=16),1):
                exponents.append(re)
                if count%1000==0:
                    print(json.dumps({'checked':count,'seconds':time.perf_counter()-started}),flush=True)
    subset=roots[indices]
    sep=check_disjoint(subset,exponents)
    if not sep['distinct']:raise AssertionError('Exact separation failed')
    if len(indices)<=512:
        independent,gap=disjoint(subset,[pow2(e) for e in exponents])
        if not independent:raise AssertionError('Independent pairwise separation failed')
    report={'rank':n//2,'input_roots':len(roots),'checked_roots':len(indices),
            'all_roots_checked':len(indices)==len(roots),
            'indices':list(map(int,indices)),
            'all_selected_checks_passed':True,
            'arithmetic':'Python integers and fractions; no C++ backend import or call',
            'separation':sep,'worker_processes':args.workers,
            'completeness_proved':False,
            'certificate_sha256':hashlib.sha256(args.path.read_bytes()).hexdigest(),
            'seconds':time.perf_counter()-started}
    text=json.dumps(report,indent=2)+'\n'
    print(json.dumps({k:v for k,v in report.items() if k!='indices'},indent=2))
    if args.output:args.output.write_text(text)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path',type=Path)
    p.add_argument('--sample',type=int,default=32)
    p.add_argument('--seed',type=int,default=624897)
    p.add_argument('--all',action='store_true')
    p.add_argument('--workers',type=int,default=1)
    p.add_argument('--output',type=Path)
    main(p.parse_args())
