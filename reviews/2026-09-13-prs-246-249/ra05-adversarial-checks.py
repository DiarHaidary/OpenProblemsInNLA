from pathlib import Path
import sys, json
from collections import Counter
import numpy as np
import sympy as sp
sys.path.insert(0, str(Path(__file__).parent/'code'))
from even_features import Features, monomials, protected_maps
rng=np.random.default_rng(98724471)
counts=Counter()
maxerr=0.
def equal(a,b,label,tol=1e-8):
    global maxerr
    a=np.asarray(a);b=np.asarray(b)
    err=float(np.linalg.norm(a-b))/(1+max(float(np.linalg.norm(a)),float(np.linalg.norm(b))))
    assert err<tol,(label,err)
    maxerr=max(maxerr,err);counts[label]+=1
# Independent geometry for the large-rank lower construction, including N >> k.
for r,N in [(1,1),(2,17),(4,31),(9,3)]:
    dim=r+1+N
    for _ in range(20):
        z=rng.normal(size=r);z/=np.linalg.norm(z)
        u=rng.normal(size=r);u/=np.linalg.norm(u)
        y=rng.normal(size=N);y/=np.linalg.norm(y)
        tail=int(rng.integers(N));tau=r**-.5
        for t in [-13.,-1.,0.,.001,2.,25.]:
            v=np.r_[z/np.sqrt(2),-1/np.sqrt(2),t*y]/np.sqrt(1+t*t)
            P=np.zeros((dim,dim));P[:r,:r]=np.eye(r)-np.outer(z,z);P+=np.outer(v,v)
            equal(P@P,P,'large_lower_projector');equal(np.trace(P),r,'large_lower_query_rank')
            row=np.r_[u,0.,tau*np.eye(N)[tail]]
            a=z@u/np.sqrt(2);beta=y[tail]
            D=a*a+tau*tau*(1-beta*beta)+(tau*beta-t*a)**2/(1+t*t)
            equal(np.linalg.norm(row-P@row)**2,D,'large_lower_residual_identity')
            assert -1e-10<=D<=2*(a*a+tau*tau)+1e-10
            counts['large_lower_cost_bound']+=1
# Symbolic derivative and finite-interpolation polynomial degree, every s=2..12.
a,b,t,tau=sp.symbols('a b t tau',real=True)
D=a*a+tau*tau*(1-b*b)+(tau*b-t*a)**2/(1+t*t)
for s in range(2,13):
    assert sp.simplify(sp.diff(D**s,t).subs(t,0)+2*s*tau*a*b*(a*a+tau*tau)**(s-1))==0
    counts['exact_derivative_identity']+=1
    numerator=sp.cancel((1+t*t)*D)
    assert sp.Poly(numerator,t).degree()==2
    assert sp.Poly(numerator**s,t).degree()==2*s
    counts['exact_interpolation_degree']+=1
# Singular tensor ranges, zero-tail/zero-head rows, pure projections and larger tails.
for s,k,q in [(2,2,5),(3,3,3),(5,2,2)]:
    n=15
    for mode in ['singular','mixed_zeros','all_zero_tail']:
        B=rng.normal(size=(n,k))*.4;C=rng.normal(size=(n,q));C/=np.maximum(np.linalg.norm(C,axis=1),1)[:,None];C*=.8
        if mode=='singular': B[:,1:]=0
        if mode=='mixed_zeros': B[:3]=0;C[3:7]=0
        if mode=='all_zero_tail': C[:]=0
        omega=rng.uniform(.2,2.,n);omega/=omega.sum();feat=Features(B,C,omega,s)
        equal(feat.pi.sum(),1,'edge_density')
        for l,E in feat.E.items(): equal(E.T@E,np.eye(E.shape[1]),'edge_head_range_isotropy')
        for key,F in feat.F.items():
            equal(np.sum(F*F),feat.h[key],'edge_mixed_range_trace')
            assert np.linalg.eigvalsh(F@F.T)[-1]<=1+1e-8
            counts['edge_mixed_covariance']+=1
        dim=k+q
        for rank in [0,1,k]:
            U,_=np.linalg.qr(rng.normal(size=(dim,rank)))
            P=U@U.T;Q=np.eye(dim)-P;V,W=Q[:,:k],Q[:,k:];PC=P[k:,k:]
            VB=B@V.T;WC=C@W.T
            A=np.sum(VB*VB,axis=1);X=np.sum(VB*WC,axis=1);R=np.einsum('ni,ij,nj->n',C,PC,C)
            H=omega@(A**s)
            for a0,b0,c0,d0 in monomials(s):
                if not(a0>=1 and b0+c0>0):continue
                LL,RR,(l,nu,h,e,j,tt)=protected_maps(feat,V,W,PC,a0,b0,c0,d0)
                left=feat.E[l]@LL.T;right=feat.F[j,tt]@RR.T
                val=np.sum(left*right,axis=1)*feat.r**(2*d0)
                expected=omega*(A**a0)*(X**b0)*(R**c0)*feat.r**(2*d0)
                equal(val,expected,'edge_protected_factorization')
                equal(np.sum(LL*LL),omega@(A**l),'edge_left_norm_identity')
                assert np.sum(RR*RR)<=k**c0*H**(j/s)+1e-8
                counts['edge_right_norm_bound']+=1
# Full lower support certificate is not claimed by any finite test above.
result={'passed':True,'seed':98724471,'assertions':sum(counts.values()),'categories':dict(counts),'max_scaled_residual':maxerr,'limits':'Independent finite geometry/symbolic checks plus supplied feature library edge-case diagnostics; no partial-coloring or restricted-invertibility oracle.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
