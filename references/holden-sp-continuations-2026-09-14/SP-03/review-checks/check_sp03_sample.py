import sys,json,time,hashlib
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]/'submitted'
sys.path.insert(0,str(p/'verify'))
from reference import exact_system,check_one,disjoint
out=[]
for m in range(1,5):
 path=p/f'certificates/rank{m}.npz'
 z=np.load(path,allow_pickle=False); roots=z['roots']; u=z['U'].ravel(); n=2*m
 ids=np.arange(len(roots)) if m<=3 else np.unique(np.linspace(0,len(roots)-1,32,dtype=int))
 radii=[];t=time.time()
 for i in ids:
  x=roots[i];fr,fi,ar,ai,e=exact_system(x,u,n)
  h=np.asarray(ar,dtype=float)*2.**(-e)+1j*np.asarray(ai,dtype=float)*2.**(-e)
  ok,r,*_=check_one(x,u,np.linalg.inv(h),n)
  assert ok,(m,int(i));radii.append(r)
 assert disjoint(roots[ids],radii)[0]
 row={'rank':m,'input_roots':len(roots),'checked_indices':[int(i) for i in ids],'all_roots_checked':len(ids)==len(roots),'exact_contraction_passed':True,'sample_pairwise_separation_passed':True,'seconds':time.time()-t,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 out.append(row);print(json.dumps(row),flush=True)
Path('SP03-sample-results.json').write_text(json.dumps(out,indent=2)+'\n')
