import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from fast_general import evaluate
from fast_reduction import evaluate as ev
rng=np.random.default_rng(75312)
for m in range(1,5):
 def rc(shape):return rng.normal(size=shape)+1j*rng.normal(size=shape)
 A=np.eye(m)+rc((m,m))/4;U=rc((2*m,2*m));dU=rc(U.shape);h=1e-6
 g,H,gp,S,T=evaluate(A.ravel(),U,dU)
 go,Ho,So,To=ev(A.ravel(),U[:m,:m].copy(),U[:m,m:].copy(),U[m:,:m].copy(),U[m:,m:].copy())
 assert np.allclose(g,go) and np.allclose(H,Ho) and np.allclose(S,So) and np.allclose(T,To)
 gd=(evaluate(A.ravel(),U+h*dU,dU)[0]-evaluate(A.ravel(),U-h*dU,dU)[0])/(2*h)
 print(m, np.max(abs(gd-gp))/(1+np.max(abs(gp))),flush=True)
 assert np.allclose(gd,gp,rtol=2e-6,atol=2e-6)
print('all passed',flush=True)
