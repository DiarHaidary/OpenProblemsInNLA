"""Reviewer-written finite checks; no supplied module is imported."""
import json
import numpy as np
from scipy.linalg import schur
rng=np.random.default_rng(142026)
checks=[]
for n in range(1,9):
 for trial in range(8):
  C=rng.normal(size=(n+1,n+1))+1j*rng.normal(size=(n+1,n+1))
  C+=4*(n+1)*np.eye(n+1)
  Ci=np.linalg.inv(C); A=C[:-1,1:]; k=Ci[0,-1]
  M=np.linalg.norm(C,2); K=np.linalg.norm(Ci,2); s=np.linalg.svd(A,compute_uv=False)[-1]
  checks.append(bool(abs(k)/(2*K*K)<=s+1e-12 and s<=2*M*M*abs(k)+1e-12))
  checks.append(bool(abs(np.linalg.det(A)-(-1)**n*np.linalg.det(C)*k)<=1e-10*max(1,abs(np.linalg.det(A)))))
  old=np.linalg.inv(C[:-1,:-1])[0]
  pred=k*np.r_[-C[-1,:-1]@np.linalg.inv(C[:-1,:-1]),1]
  checks.append(bool(np.linalg.norm(Ci[0]-np.r_[old,0]-pred)<1e-12))
for n in (2,4,9,15):
 coeff={k:(rng.normal()+1j*rng.normal())/(1+abs(k)) for k in range(-5,6)}
 A=np.array([[coeff.get(i-j,0) for j in range(n)] for i in range(n)])
 S,Q=schur(A,output='complex'); ev=np.diag(S)
 z=np.exp(2j*np.pi*np.arange(512)/512)
 a=sum(v*z**k for k,v in coeff.items())
 polys=(z[:,None]**np.arange(n))@Q
 weights=abs(polys)**2
 checks.append(bool(np.max(abs(np.mean(a[:,None]*weights,axis=0)-ev))<1e-12))
 cost=np.mean(np.sum(abs(a[:,None]-ev)**2*weights,axis=1))/n
 deficit=sum(abs(v)**2 for v in coeff.values())-np.mean(abs(ev)**2)
 checks.append(bool(abs(cost-deficit)<1e-12))
report={'reviewer_generated_checks':len(checks),'passed':sum(checks),'failed':len(checks)-sum(checks),'scope':'Finite general complex bordering/cofactor/singular comparisons and exact-degree quadrature of Schur energy coupling; no asymptotic inference.'}
print(json.dumps(report,indent=2))
assert all(checks)
