"""Express the numerical dual in the exact sparse kernel bases."""
import numpy as np
s=np.load('exact_system.npz');y=np.load('dual_degree4.npz')
q=(s['qr']+1j*np.sqrt(3)*s['qi'])/388
xs=[]
for j in range(3):
    Y=y[f'Y{j}'].copy()
    if j==1:Y-=q@q.conj().T
    free=s[f'free{j}'];d=int(s[f'den{j}'])
    T=Y[np.ix_(free,free)]*388**2/d**2
    n=len(T);i,k=np.triu_indices(n,1)
    xs.append(np.r_[T.diagonal().real,T[i,k].real,T[i,k].imag/np.sqrt(3)])
np.save('exact_x_initial.npy',np.concatenate(xs))
