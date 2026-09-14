import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import sys, json, time, hashlib, multiprocessing
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
BASE=Path('/private/tmp/nla-review-253-256/pr255/scratch/sp03')
sys.path.insert(0,str(BASE/'verify'))
from reference import exact_system, check_one
from separation import check_disjoint

def init(u,n):
 global U,N
 U,N=u,n

def one(pair):
 i,x=pair
 _,_,ar,ai,e=exact_system(x,U,N)
 H=np.asarray(ar,dtype=float)*2.**(-e)+1j*np.asarray(ai,dtype=float)*2.**(-e)
 ok,r,eta,z0,z2=check_one(x,U,np.linalg.inv(H),N)
 if not ok: raise RuntimeError(f'Exact contraction failed at {i}')
 re=r.numerator.bit_length()-r.denominator.bit_length()
 return i,re,float(eta),float(z0),float(z2)

if __name__=='__main__':
 for m in map(int,sys.argv[1:] or [1,2,3,4]):
  p=BASE/f'certificates/rank{m}.npz'
  z=np.load(p,allow_pickle=False); roots=z['roots'];u=z['U'].ravel(); t=time.time();rows=[]
  with ProcessPoolExecutor(max_workers=4,mp_context=multiprocessing.get_context('spawn'),initializer=init,initargs=(u,2*m)) as pool:
   for row in pool.map(one,enumerate(roots),chunksize=16):
    rows.append(row)
    if len(rows)%1000==0: print(json.dumps({'rank':m,'checked':len(rows),'seconds':time.time()-t}),flush=True)
  sep=check_disjoint(roots,[r[1] for r in rows])
  if not sep['distinct']:raise RuntimeError(str(sep))
  report={'rank':m,'checked_roots':len(rows),'input_roots':len(roots),'all_roots_checked':True,'arithmetic':'Exact Python integers and fractions with floating inverse proposals from exact Jacobian','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'separation':sep,'maximum_eta':max(x[2] for x in rows),'maximum_z0':max(x[3] for x in rows),'maximum_z2':max(x[4] for x in rows),'seconds':time.time()-t,'completeness_proved':False,'radius_exponents':[x[1] for x in rows]}
  (BASE.parents[1]/f'sp03-rank{m}-full.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps({k:v for k,v in report.items() if k!='radius_exponents'}),flush=True)
