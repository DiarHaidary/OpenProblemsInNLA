"""Optional real/complex diagnostics, not exact certificates or universal proofs."""
from __future__ import annotations
import json, math, time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


def make_matrix(r:int,n:int,kind:str,complex_input:bool,seed:int):
    rng=np.random.default_rng(seed)
    G=rng.normal(size=(n,n))
    if complex_input:G=G+1j*rng.normal(size=(n,n))
    U,_=np.linalg.qr(G)
    head=np.geomspace(1000.,2.,r)
    tail=(2.**(-np.arange(n-r)) if kind=='geometric'
          else 1./np.arange(1,n-r+1,dtype=float)**2)
    spectrum=np.r_[head,tail]
    A=(U*spectrum)@U.conj().T
    return (A+A.conj().T)/2,spectrum


def pivot(R,j):
    d=float(R[j,j].real)
    if d<=0:raise ArithmeticError('Nonpositive pivot in a positive-definite test.')
    v=R[:,j].copy()
    B=R-np.outer(v,v.conj())/d
    B=(B+B.conj().T)/2
    B[j,:]=0;B[:,j]=0
    return B


def exhaustive(A):
    n=len(A);states={0:A};probs={0:1.};means=[];maxdiff=0.;maxnorm=0.;transitions=0
    for k in range(n+1):
        if abs(sum(probs.values())-1)>2e-10:raise AssertionError('Probability normalization')
        means.append(float(sum(p*np.trace(states[s]).real for s,p in probs.items())))
        if k==n:break
        nxt={}
        for S,p in probs.items():
            R=states[S];T=float(np.trace(R).real)
            for j in range(n):
                if S&(1<<j):continue
                d=float(R[j,j].real)
                B=pivot(R,j);Sn=S|(1<<j);transitions+=1
                if Sn in states:
                    diff=float(np.max(np.abs(B-states[Sn])))
                    maxdiff=max(maxdiff,diff)
                    if diff>5e-8:raise AssertionError('Residual paths disagree beyond tolerance')
                else:states[Sn]=B
                nxt[Sn]=nxt.get(Sn,0)+p*d/T
        probs=nxt
    return {'expected_traces':means,'positive_transitions':transitions,
            'max_absolute_alternate_path_difference':maxdiff}


def monte_carlo(A,r,kind,trials,seed):
    rng=np.random.default_rng(seed);n=len(A);C=3 if kind=='geometric' else 4
    k0=3*r+1;k=min(n,math.ceil(C*r/.99));ks=sorted(set([k0,k]));samples={s:[] for s in ks}
    min_diag=0.
    for it in range(trials):
        R=A.copy();available=np.ones(n,dtype=bool)
        for step in range(1,max(ks)+1):
            ds=R.diagonal().real.copy();min_diag=min(min_diag,float(ds.min()))
            if ds.min() < -1e-9:raise AssertionError('Substantial negative residual diagonal')
            ds[~available]=0;ds=np.maximum(ds,0)
            j=rng.choice(n,p=ds/ds.sum());R=pivot(R,j);available[j]=False
            if step in samples:samples[step].append(float(np.trace(R).real))
    return {'trials':trials,'seed':seed,'epsilon':.99,'C':C,
            'smallest_numerical_diagonal':min_diag,
            'counts':{str(k):{'mean':float(np.mean(x)),
                             'standard_error':float(np.std(x,ddof=1)/np.sqrt(trials)),
                             'minimum':float(min(x)),'maximum':float(max(x))} for k,x in samples.items()}}


def main():
    start=time.perf_counter();records=[]
    for cplx in [False,True]:
        seed=20260913+int(cplx)
        A,spectrum=make_matrix(3,11,'geometric',cplx,seed)
        res=exhaustive(A);tau=float(sum(spectrum[3:]))
        if res['expected_traces'][10]>1.6*tau+1e-8:raise AssertionError('Warm start diagnostic')
        records.append({'mode':'floating exhaustive subsets','complex':cplx,'dimension':11,
                        'target_rank':3,'construction_seed':seed,'tail':'geometric',
                        'eigenvalues':spectrum.tolist(),'tau':tau,**res})
        print(f'PASS floating exhaustive n=11 complex={cplx}',flush=True)
    for i,(r,kind,cplx) in enumerate([(3,'geometric',False),(5,'geometric',True),(8,'geometric',True),
                                    (3,'square',True),(5,'square',False),(8,'square',True)]):
        n=(3*r+4 if kind=='geometric' else 4*r+5);seed=20261000+i
        A,spectrum=make_matrix(r,n,kind,cplx,seed);tau=float(sum(spectrum[r:]))
        res=monte_carlo(A,r,kind,200,seed+1000)
        warm=res['counts'][str(3*r+1)]['mean'];B=1.6 if kind=='geometric' else 2.
        if warm>B*tau+1e-8:raise AssertionError('Monte Carlo diagnostic mean exceeds proposed bound')
        records.append({'mode':'Monte Carlo diagnostic','complex':cplx,'dimension':n,
                        'target_rank':r,'tail':kind,'construction_seed':seed,
                        'eigenvalues':spectrum.tolist(),'tau':tau,**res})
        print(f'PASS Monte Carlo n={n} r={r} {kind} complex={cplx}',flush=True)
    out={'status':'PASS','arithmetic':'NumPy float64/complex128','records':records,
         'seconds':round(time.perf_counter()-start,3),
         'scope':'Floating-point exhaustive enumeration and Monte Carlo diagnostics only. Not exact certificates, independent review, or formal verification.'}
    (ROOT/'verification'/'floating_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(f"PASS 2 exhaustive cases and 1200 Monte Carlo trajectories; {out['seconds']} seconds")

if __name__=='__main__':main()
