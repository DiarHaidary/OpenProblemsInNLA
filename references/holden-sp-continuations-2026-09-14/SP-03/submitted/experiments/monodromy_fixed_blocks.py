"""Exploratory monodromy of the m^2-variable SP-03 reduction.

Outputs are numerical candidates, never a completeness certificate. The source
checkpoint must specify ordinary-Frobenius data and full critical matrices.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import argparse,json,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from fast_reduction import evaluate,triangle,refine,lift

def main():
 p=argparse.ArgumentParser();p.add_argument('--rank',type=int,default=4);p.add_argument('--seconds',type=float,default=600);p.add_argument('--workers',type=int,default=4);p.add_argument('--seed',type=int,default=953071);p.add_argument('--max-roots',type=int,default=100000);p.add_argument('--source',type=Path);p.add_argument('--output',type=Path,default=Path(__file__).parent/'fixed_m4.npz');args=p.parse_args()
 m=args.rank;n=2*m;out=args.output;rng=np.random.default_rng(args.seed)
 I=np.eye(m);P=np.block([[I,1j*I],[1j*I,I]])/np.sqrt(2);Pi=np.linalg.inv(P)
 if out.exists():
  z=np.load(out);U=z['U'];roots0=z['roots'];loops=int(z['loops'])
 else:
  source=args.source or Path(__file__).resolve().parents[1]/'certificates'/f'rank{m}.npz'
  z=np.load(source);U=Pi@z['U'].reshape(n,n)@P
  roots0=np.array([(Pi@x.reshape(n,n)@P)[:m,:m].ravel() for x in z['roots']]);loops=0
 ua=U[:m,:m].copy();ub=U[:m,m:].copy();uc=U[m:,:m].copy();ud=U[m:,m:].copy()
 roots=[];bucket={};proj=(rng.normal(size=m*m)+1j*rng.normal(size=m*m));width=.001
 def add(y):
  if not np.isfinite(y).all() or np.max(abs(y))>1e5:return False
  z=np.dot(proj,y);a=int(np.floor(z.real/width));b=int(np.floor(z.imag/width))
  for i in range(a-1,a+2):
   for j in range(b-1,b+2):
    for ix in bucket.get((i,j),[]):
     if np.max(abs(roots[ix]-y))<1e-6*(1+np.max(abs(y))):return False
  bucket.setdefault((a,b),[]).append(len(roots));roots.append(y.copy());return True
 for a in roots0:
  b,ok=refine(a,ua,ub,uc,ud)
  if ok:add(b)
 if not roots:raise RuntimeError('No valid starting root')
 triangle(roots[0],ua,ub,uc,ud,ud,ud)
 print(json.dumps(dict(event='start',rank=m,roots=len(roots),prior_loops=loops)),flush=True)
 start=time.monotonic();last=start;paths=failures=steps=0;no_gain=0
 logfile=out.with_suffix('.jsonl')
 def save():
  np.savez_compressed(out,roots=np.array(roots),U=U,loops=loops,seed=args.seed)
  info=dict(rank=m,loops=loops,roots=len(roots),elapsed_seconds=time.monotonic()-start,triangles=paths,failed_triangles=failures,steps=steps,completeness_proved=False)
  print(json.dumps(info),flush=True)
  with logfile.open('a') as f:f.write(json.dumps(info)+'\n')
 with ThreadPoolExecutor(max_workers=args.workers) as pool:
  while time.monotonic()-start<args.seconds and len(roots)<args.max_roots and no_gain<8:
   old=len(roots);loops+=1
   scale=[.5,1.,2.,3.,5.,8.,12.][(loops-1)%7]/np.sqrt(m)
   v=ud+scale*(rng.normal(size=(m,m))+1j*rng.normal(size=(m,m)))
   w=ud+scale*(rng.normal(size=(m,m))+1j*rng.normal(size=(m,m)))
   order=list(rng.permutation(len(roots)));index=0
   while index<len(order) and time.monotonic()-start<args.seconds and len(roots)<args.max_roots:
    batch=order[index:index+64];index+=len(batch)
    fut=[pool.submit(triangle,roots[ix],ua,ub,uc,ud,v,w) for ix in batch]
    for ff in fut:
     y,ok,st=ff.result();paths+=1;steps+=st
     if not ok:failures+=1
     elif add(y):order.append(len(roots)-1)
    if time.monotonic()-last>15:
     save();last=time.monotonic()
   no_gain=no_gain+1 if old==len(roots) else 0
   save();last=time.monotonic()
 save()
if __name__=='__main__':main()
