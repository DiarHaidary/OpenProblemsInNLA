"""Numerical diagnostic on already certified roots, not an additional proof.

Read the predecessor's exact rank-three certificate centers, convert their
coordinates numerically, and apply the deliberately strict reduced residual
test. Rejection here does not invalidate their full-coordinate certificates.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import io,zipfile,json
import numpy as np
from fast_reduction import evaluate,refine
BASE=Path(__file__).resolve().parents[1]
with zipfile.ZipFile(BASE/'prior'/'SP03_verified_partial.zip') as archive:
    data=archive.read('SP03_verified_partial/certificates/certificates_m3.npz')
with np.load(io.BytesIO(data),allow_pickle=False) as z:
    roots=z['roots'].copy();u=z['U'].reshape(6,6).copy()
m=3;I=np.eye(m);P=np.block([[I,1j*I],[1j*I,I]])/np.sqrt(2);Pi=np.linalg.inv(P)
U=Pi@u@P
blocks=tuple(np.ascontiguousarray(v) for v in (U[:m,:m],U[:m,m:],U[m:,:m],U[m:,m:]))
rejected=[];norms=[];conds=[];residuals=[]
for i,x in enumerate(roots):
    a=np.ascontiguousarray((Pi@x.reshape(6,6)@P)[:m,:m]).ravel()
    norms.append(float(np.max(abs(a))))
    y,ok=refine(a,*blocks)
    g,H,S,T=evaluate(y,*blocks)
    cond=float(np.linalg.cond(H));res=float(np.max(abs(g)))
    conds.append(cond);residuals.append(res)
    if not ok:rejected.append({'source_root_index':i,'reduced_residual':res,'hessian_condition_number':cond})
report={'source_certified_roots':len(roots),'strict_reduced_refiner_rejections':len(rejected),
        'root_norm_quantiles':dict(zip(['median','90_percent','99_percent','maximum'],map(float,np.quantile(norms,[.5,.9,.99,1])))),
        'maximum_hessian_condition_number':max(conds),'maximum_reduced_residual':max(residuals),
        'rejected_roots':rejected,'diagnostic_only':True,'invalidates_no_full_coordinate_certificate':True}
(BASE/'results'/'conditioning_diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='rejected_roots'},indent=2))
