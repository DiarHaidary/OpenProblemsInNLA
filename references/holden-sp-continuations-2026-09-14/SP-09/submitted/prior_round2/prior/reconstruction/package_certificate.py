"""Assemble an exact-integer certificate and positive-definiteness witnesses."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json,numpy as np,time
from exact_reconstruct import int_congruence
st=time.monotonic()
s=np.load('exact_system.npz');r=json.load(open('rational_coordinates.json'))
nums=[int(x) for x in r['numerators']];den=int(r['denominator']);out={'field':'Q(s), s^2=-3, s=i*sqrt(3)','coordinate_denominator':str(den),'q_denominator':388,'q_real':s['qr'].ravel().tolist(),'q_s':s['qi'].ravel().tolist(),'blocks':[]}
off=0
for j,n in enumerate([52,26,26]):
 vals=nums[off:off+n*n];off+=n*n
 R=np.zeros((n,n),dtype=object);I=R.copy();ii,jj=np.triu_indices(n,1);m=len(ii)
 for i in range(n):R[i,i]=vals[i]
 for k,(i,l) in enumerate(zip(ii,jj)):
  R[i,l]=R[l,i]=vals[n+k];I[i,l]=vals[n+m+k];I[l,i]=-vals[n+m+k]
 H=np.array(R,dtype=float)/den+1j*np.sqrt(3)*np.array(I,dtype=float)/den
 L=np.linalg.cholesky(H);S=np.linalg.inv(L.conj().T);sd=10**10
 SR=np.array([[round(v*sd) for v in row] for row in S.real],dtype=object)
 SI=np.array([[round(v*sd/np.sqrt(3)) for v in row] for row in S.imag],dtype=object)
 GR,GI=int_congruence(SR,SI,R,I)
 assert np.array_equal(GR,GR.T) and np.array_equal(GI,-GI.T)
 margins=[]
 for i in range(n):
  margin=GR[i,i]-sum(abs(GR[i,k])+2*abs(GI[i,k]) for k in range(n) if k!=i)
  assert margin>0
  margins.append(int(margin))
 print('block',j,'minimum normalized diagonal-dominance margin',min(margins)/(den*sd*sd),'time',time.monotonic()-st,flush=True)
 def arr(A,strings=False):return [[str(int(z)) if strings else int(z) for z in row] for row in A]
 out['blocks'].append({'size':n,'kernel_real':arr(s[f'KR{j}']),'kernel_s':arr(s[f'KI{j}']),'matrix_real':arr(R,True),'matrix_s':arr(I,True),'preconditioner_real':arr(SR),'preconditioner_s':arr(SI),'preconditioner_scale':sd,'min_integer_margin':str(min(margins))})
with open('krause_certificate.json','w') as f:json.dump(out,f,separators=(',',':'))
print('saved certificate',time.monotonic()-st,flush=True)
