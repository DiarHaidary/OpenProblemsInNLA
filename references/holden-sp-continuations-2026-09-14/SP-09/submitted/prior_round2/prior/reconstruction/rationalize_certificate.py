"""Replace the numerical certificate by rational matrices satisfying all identities exactly."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from scipy.linalg import qr
from sympy import ZZ, Matrix
from sympy.polys.matrices import DomainMatrix
import time,json
st=time.monotonic()
s=np.load('exact_system.npz');C=s['C'];rhs=s['rhs'];x=np.load('exact_x_initial.npy')
Cf=C.astype(float);scale=np.maximum(np.linalg.norm(Cf,axis=1),1);Cscaled=Cf/scale[:,None]
_,r,rowp=qr(Cscaled.T,mode='economic',pivoting=True)
rank=np.sum(abs(np.diag(r))>abs(r[0,0])*1e-10);rows=rowp[:rank]
_,r,colp=qr(Cscaled[rows],mode='economic',pivoting=True);cols=colp[:rank]
Cp=C[np.ix_(rows,cols)]
print('rank',rank,'condition',np.linalg.cond(Cscaled[np.ix_(rows,cols)]),'seconds',time.monotonic()-st,flush=True)
den0=10**14
xn=np.array([round(float(v)*den0) for v in x],dtype=object)
res=np.array([int(v)*den0 for v in rhs],dtype=object)-C.astype(object)@xn
print('integer residual max',max(abs(int(z)) for z in res),'seconds',time.monotonic()-st,flush=True)
DM=DomainMatrix.from_Matrix(Matrix(Cp.tolist())).convert_to(ZZ)
b=DomainMatrix.from_Matrix(Matrix([int(res[i]) for i in rows])).convert_to(ZZ)
sol,den=DM.solve_den(b,method='rref')
sol=[int(v) for v in sol.to_Matrix()];den=int(den)
print('solved exact correction','den digits',len(str(abs(den))),'seconds',time.monotonic()-st,flush=True)
# x = xn/den0 + sol/(den*den0), only pivot coordinates corrected.
outn=[int(v)*den for v in xn]
for j,d in zip(cols,sol):outn[int(j)]+=d
outden=den*den0
if outden<0:outn=[-v for v in outn];outden=-outden
from math import gcd
G=outden
for z in outn:G=gcd(G,z)
outn=[z//G for z in outn];outden//=G
check=C.astype(object)@np.array(outn,dtype=object)-np.array([int(z)*outden for z in rhs],dtype=object)
assert all(z==0 for z in check), 'Full exact trace identity failed'
xf=np.array([z/outden for z in outn]);print('max correction',np.max(abs(xf-x)),'full exact residual ZERO','seconds',time.monotonic()-st,flush=True)
obj={'denominator':str(outden),'numerators':[str(z) for z in outn],'rows':[int(v) for v in rows],'columns':[int(v) for v in cols]}
with open('rational_coordinates.json','w') as f:json.dump(obj,f,separators=(',',':'))
print('saved','denominator digits',len(str(outden)),'seconds',time.monotonic()-st,flush=True)
