import json,sys,math,itertools
import numpy as np
import scipy.linalg as la
from scipy.integrate import quad
from scipy.stats import chi2
rng=np.random.default_rng(991372)
summary={}
# RA18: build lift independently and enumerate every square subset, including
# parents with zero rows, g=1 and n=r, which are absent from generic random draws.
w=np.exp(2j*np.pi/3)
parents=[np.eye(1),np.eye(2),np.array([[1.],[0.],[0.]]),np.array([[1.,0.],[0.,1.],[0.,0.],[0.,0.]])]
for n,r in [(3,1),(3,2),(4,1),(4,2)]:
    parents.append(np.linalg.qr(rng.normal(size=(n,r))+1j*rng.normal(size=(n,r)))[0])
checks=0; legal=0; worst=0.; min_slack=float('inf')
for U in parents:
    n,r=U.shape
    T=np.array([np.r_[U[i],w**j*np.eye(n)[i]]/np.sqrt(3) for i in range(n) for j in range(3)])
    assert np.linalg.norm(T.conj().T@T-np.eye(n+r))<1e-12
    for ids in itertools.combinations(range(3*n),n+r):
        counts=np.bincount(np.array(ids)//3,minlength=n)
        I=np.where(counts==2)[0]
        valid=(np.all((counts==1)|(counts==2)) and len(I)==r and np.linalg.matrix_rank(U[I])==r)
        singular=np.linalg.svd(T[list(ids)],compute_uv=False)
        assert valid==(singular[-1]>1e-10)
        checks+=1
        if valid:
            legal+=1
            g=np.linalg.svd(U[I],compute_uv=False)[-1]**2
            slack=1/singular[-1]**2-4/g+1.5
            min_slack=min(min_slack,slack)
            assert slack>=-1e-8
            if n==2*r:
                ev=np.linalg.eigvalsh(U[I].conj().T@U[I])
                blocks=[np.array([[1+x,np.sqrt(x),np.sqrt(max(0,1-x))],[np.sqrt(x),2,0],[np.sqrt(max(0,1-x)),0,1]])/3 for x in ev]
                predicted=np.sort(np.concatenate([np.linalg.eigvalsh(b) for b in blocks]))
                err=np.max(abs(np.sort(singular**2)-predicted));worst=max(worst,err)
                assert err<2e-12
summary['RA18_independent_boundary_lifts']={'parents':len(parents),'all_square_subsets':checks,'nonsingular':legal,'minimum_amplification_slack':min_slack,'maximum_spectral_error':worst}
# RA18 weighted duality: fresh complex/real matrices and thresholds almost at
# their strict admissible boundary; compare the two Loewner conditions directly.
dual=0; close=0
for field in [False,True]:
  for q,r in [(3,1),(3,2),(4,2),(5,3)]:
    A=rng.normal(size=(q,r))
    if field:A=A+1j*rng.normal(size=(q,r))
    V=np.linalg.qr(A)[0];W=la.null_space(V.conj().T)
    m=np.arange(1,q+1)**2
    for factor in [1e-5,.1,.9,1-1e-7]:
      eta=factor/max(m); weights=eta*m/(1-eta*m)
      aa=W.conj().T@(weights[:,None]*W)
      ev,Q=np.linalg.eigh(aa);isq=(Q/np.sqrt(ev))@Q.conj().T
      Z=(np.sqrt(weights)[:,None]*W)@isq
      assert np.linalg.norm(Z.conj().T@Z-np.eye(q-r))<2e-8
      for I in itertools.combinations(range(q),r):
        J=[i for i in range(q) if i not in I]
        l=np.linalg.eigvalsh(V[list(I)].conj().T@(V[list(I)]/m[list(I),None]))[0]-eta
        rr=np.linalg.eigvalsh(Z[J].conj().T@(Z[J]/m[J,None]))[0]-eta
        if min(abs(l),abs(rr))<1e-8:close+=1
        else:assert (l>=0)==(rr>=0)
        dual+=1
summary['RA18_independent_weighted_duality']={'comparisons':dual,'within_1e8_of_threshold':close}
# RA14: independent arbitrary-block Schur/pseudodeterminant identities with
# unequal dimensions, noncommuting factors and a near-wall compression.
geom=0; max_pdet=0.;max_kernel=0.;max_short=0.
for t,d,k in [(0,3,1),(1,2,1),(1,4,3),(2,5,2),(3,4,1)]:
  for gap in [1e-4,.2,3.]:
    h=.4
    V=np.linalg.qr(rng.normal(size=(t,t)))[0] if t else np.zeros((0,0))
    J=V@np.diag(h+gap+np.arange(t))@V.T
    B=rng.normal(size=(d,t));Q=np.linalg.qr(rng.normal(size=(d,k)))[0];C=la.null_space(Q.T)
    K=B@np.linalg.solve(J,np.linalg.solve(J,B.T)) if t else np.zeros((d,d))
    R=np.eye(d)+(B@np.linalg.solve(J,np.linalg.solve(J-h*np.eye(t),B.T)) if t else 0)
    short=C.T@R@C-C.T@R@Q@np.linalg.solve(Q.T@R@Q,Q.T@R@C)
    # Reciprocal-compression representation is independently equivalent.
    short2=np.linalg.inv(C.T@np.linalg.solve(R,C))
    err=np.linalg.norm(short-short2)/max(1,np.linalg.norm(short2));max_short=max(max_short,err)
    assert err<2e-9
    Y=rng.normal(size=(d-k,d-k+1));Sp=h*short+Y@Y.T;S=C@Sp@C.T
    H=np.block([[J,B.T],[B,B@np.linalg.solve(J,B.T)+S]])
    HH=np.vstack([-np.linalg.solve(J,B.T)@Q,Q])
    ker=np.linalg.norm(H@HH)/max(1,np.linalg.norm(H)*np.linalg.norm(HH));max_kernel=max(max_kernel,ker)
    assert ker<1e-12
    evals=np.linalg.eigvalsh(H)
    assert evals[k]>=h-1e-8
    lhs=np.sum(np.log(evals[k:]));rhs=np.linalg.slogdet(J)[1]+np.linalg.slogdet(Sp)[1]+np.linalg.slogdet(np.eye(k)+Q.T@K@Q)[1]
    er=abs(lhs-rhs);max_pdet=max(max_pdet,er);assert er<1e-7
    geom+=1
summary['RA14_independent_posterior_geometry']={'cases':geom,'max_relative_shorting_error':max_short,'max_normalized_kernel_residual':max_kernel,'max_log_pseudodeterminant_error':max_pdet}
# RA14: direct rejection disintegration in residual dimension 2, k=1.
# Prior angular law uniform; positive Gram block is chi-square_2.
h=.4;j=2.;b=np.array([1.2,-.8]);R=np.eye(2)+np.outer(b,b)/(j*(j-h))
def wall(theta):
 q=np.array([np.cos(theta),np.sin(theta)])
 return h*np.linalg.det(R)/(q@R@q)
z=quad(lambda a:np.exp(-wall(a)/2),0,2*np.pi,epsabs=1e-12)[0]
expected=quad(lambda a:np.cos(a)**2*np.exp(-wall(a)/2),0,2*np.pi,epsabs=1e-12)[0]/z
N=250000;theta=rng.uniform(0,2*np.pi,N);qs=np.stack([np.cos(theta),np.sin(theta)],axis=1)
walls=h*np.linalg.det(R)/np.einsum('ij,jk,ik->i',qs,R,qs)
gram=rng.chisquare(2,N);accepted=gram>walls
obs=qs[accepted,0]**2; mean=float(obs.mean());se=float(obs.std(ddof=1)/np.sqrt(len(obs)))
assert abs(mean-expected)<6*se
fresh=gram[accepted]-walls[accepted]
assert abs(fresh.mean()-2)<6*fresh.std(ddof=1)/np.sqrt(len(fresh))
summary['RA14_independent_angular_disintegration']={'proposals':N,'accepted':int(accepted.sum()),'quadrature_expected_Q11':expected,'sample_mean_Q11':mean,'sample_standard_error':se,'translated_gram_mean_expected2':float(fresh.mean())}
# First exit conditional law, with m=1 and direction almost parallel to kernel.
Q=np.array([.6,.8]);C=np.array([-.8,.6]);eta=lambda v:(v@R@Q)**2/(Q@R@Q)
rows=[]
for tilt in [.05,.4,1.4]:
 v=np.cos(tilt)*Q+np.sin(tilt)*C;gamma=(v@C)**2
 law=rng.chisquare(2,100000)*gamma-h*eta(v)
 expected=float(chi2.cdf(h*eta(v)/gamma,2));observed=float((law<=0).mean())
 assert abs(observed-expected)<6*np.sqrt(max(expected*(1-expected),1e-5)/len(law))+1e-5
 rows.append({'tilt':tilt,'exact_exit_probability':expected,'empirical_exit_probability':observed})
summary['RA14_independent_exit_law']=rows
print(json.dumps(summary,indent=2))
open('/private/tmp/nla-independent-239-243-results.json','w').write(json.dumps(summary,indent=2)+'\n')
