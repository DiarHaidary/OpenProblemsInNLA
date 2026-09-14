import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,time,json,io,zipfile
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1]
from reference import check_one
from backend import check
rng=np.random.default_rng(1);results=[]
for m in [1,2,3]:
 with zipfile.ZipFile(BASE/'prior'/'SP03_verified_partial.zip') as archive:
  content=archive.read(f'SP03_verified_partial/certificates/certificates_m{m}.npz')
 z=np.load(io.BytesIO(content),allow_pickle=False)
 ix=rng.choice(len(z['roots']),min(8,len(z['roots'])),replace=False)
 for k in ix:
  x=z['roots'][k];u=z['U'];B=z['inverses'][k]
  st=time.perf_counter();yes,re,b=check(x,u,B);duration=time.perf_counter()-st
  ok,r,eta,z0,z2=check_one(x,u,B,2*m)
  assert yes==ok and yes
  assert float(r)==2.**re
  assert np.allclose(b[:3],[float(eta),float(z0),float(z2)],rtol=1e-14,atol=0)
  results.append(dict(rank=m,root_index=int(k),pass_exact_comparison=True,seconds=duration))
 x=z['roots'][0].copy();x[0]+=10
 assert not check(x,z['U'],z['inverses'][0])[0]
 assert not check(z['roots'][0],z['U'],np.zeros_like(z['inverses'][0]))[0]
print(json.dumps(results,indent=2))
(BASE/'results'/'backend_crosschecks.json').write_text(json.dumps(results,indent=2)+'\n')
