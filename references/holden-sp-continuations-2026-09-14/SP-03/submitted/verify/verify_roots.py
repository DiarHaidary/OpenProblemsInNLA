"""Verify all stored roots by exact contraction inequalities and separation.

Build exact_backend.so first. NumPy/Numba only propose Jacobian inverses.
No approximate residual or computed inverse is trusted without independent
exact reconstruction and verification of the contraction inequalities.
"""
from __future__ import annotations
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import argparse,sys,json,time,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from polynomial import evaluate
from backend import check,load
from separation import check_disjoint


def verify(path,workers=1):
    if workers<1: raise ValueError('workers must be a positive integer')
    with np.load(path,allow_pickle=False) as z:
        roots=z['roots'].copy(); u=z['U'].ravel().copy()
    if roots.dtype!=np.dtype('complex128') or u.dtype!=np.dtype('complex128'):
        raise ValueError('Certificates must store complex binary64 arrays')
    if roots.ndim!=2 or not len(roots): raise ValueError('A nonempty root matrix is required')
    n=int(round(np.sqrt(roots.shape[1])))
    if n<2 or n%2 or n*n!=roots.shape[1] or u.shape!=(n*n,):
        raise ValueError('Incompatible data and root shapes')
    evaluate(roots[0],u,n);load()
    start=time.perf_counter()
    def one(x):
        F,H=evaluate(x,u,n)
        B=np.linalg.inv(H)
        return check(x,u,B)
    if workers==1: results=list(map(one,roots))
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool: results=list(pool.map(one,roots))
    failed=[i for i,v in enumerate(results) if not v[0]]
    if failed: raise AssertionError(f'Failed exact contraction certificates: {failed[:20]} ({len(failed)} total)')
    radii=np.asarray([v[1] for v in results],dtype=np.int64)
    separated=check_disjoint(roots,radii)
    if not separated['distinct']: raise AssertionError(f'Unseparated certified balls: {separated}')
    bounds=np.asarray([v[2] for v in results])
    return {'rank':n//2,'certified_distinct_simple_roots':len(roots),
            'certificate_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'completeness_proved':False,'certificate_arithmetic':'exact multiprecision integers',
            'separation':separated,'maximum_radius_exponent':int(max(radii)),
            'maximum_eta':float(max(bounds[:,0])),'maximum_z0':float(max(bounds[:,1])),
            'maximum_z2':float(max(bounds[:,2])),
            'verification_seconds':time.perf_counter()-start}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path',type=Path)
    p.add_argument('--workers',type=int,default=1);p.add_argument('--output',type=Path)
    args=p.parse_args();report=verify(args.path,args.workers)
    text=json.dumps(report,indent=2)+'\n';print(text)
    if args.output: args.output.write_text(text)
