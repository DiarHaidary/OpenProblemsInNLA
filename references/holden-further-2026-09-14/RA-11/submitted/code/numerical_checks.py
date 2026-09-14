"""Executed diagnostics; not a substitute for the mathematical proofs."""
from __future__ import annotations
from pathlib import Path
import json
import math
import time
import numpy as np
from estimators import ProductOracle, diagonal_control, log_fractional_bound

ROOT=Path(__file__).resolve().parents[1]


def normalized_psd_families(N,rng):
    def outer_normal(v):
        v=v/np.linalg.norm(v)
        return np.outer(v,v)
    product=np.ones(1)
    for _ in range(int(math.log2(N))):
        f=rng.normal(size=2); f/=np.linalg.norm(f); product=np.kron(product,f)
    u=rng.normal(size=N)
    G=rng.normal(size=(N,12)); W=G@G.T; W/=np.trace(W)
    d=rng.random(N)**4; d/=d.sum()
    return {'identity':np.eye(N)/N,
            'diagonal':np.diag(d),
            'rank_one_product':outer_normal(product),
            'rank_one_unstructured':outer_normal(u),
            'rank_twelve':W,
            'identity_plus_product':0.5*np.eye(N)/N+0.5*outer_normal(product)}


def main():
    start=time.time(); rng=np.random.default_rng(240913)
    n,q,epsilon=2,8,0.45; N=n**q
    families=normalized_psd_families(N,rng)
    trials=[]; hashes={}; seeds=list(range(12))
    for name,M in families.items():
        tau=float(np.trace(M))
        for seed in seeds:
            oracle=ProductOracle(M,n,q,budget=N)
            result=diagonal_control(oracle,epsilon,seed)
            error=abs(result['estimate']-tau)/tau
            assert result['branch']=='diagonal_control'
            assert result['calls']<N
            key=seed
            if key in hashes: assert result['query_hash']==hashes[key]
            else: hashes[key]=result['query_hash']
            trials.append({'family':name,'seed':seed,'relative_error':error,
                           'success':bool(error<=epsilon),'calls':result['calls'],
                           'm':result['m'],'query_hash':result['query_hash']})
    # Zero input uses the same design, and must return exactly zero.
    zero=diagonal_control(ProductOracle(np.zeros((N,N)),n,q,budget=N),epsilon,0)
    assert zero['estimate']==0 and zero['query_hash']==hashes[0]
    # Too-small budget must be rejected before any queries are made.
    insufficient=ProductOracle(np.eye(N),n,q,budget=1)
    try: diagonal_control(insufficient,epsilon,0)
    except RuntimeError: pass
    else: raise AssertionError('Budget guard did not reject.')
    assert insufficient.calls==0
    # General N finite-bit correction is tested by forcing its diagnostic branch.
    nonpower=ProductOracle(np.diag(np.arange(1,10,dtype=float)),3,2,budget=10)
    nonpower_result=diagonal_control(nonpower,0.4,11,force_training_count=5)
    assert abs(nonpower_result['estimate']-45)<1e-12
    # Scalar distribution experiments: no exponentially large matrix is allocated.
    D=math.log(2)-0.5; phase=[]
    for order in [8,16,24,32,40]:
        for rate in [D-0.08,D,D+0.08]:
            count=max(1,math.ceil(math.exp(rate*order))); values=[]
            for repetition in range(40):
                logs=order*math.log(2)-rng.gamma(shape=order,scale=1.0,size=count)
                values.append(float(np.exp(logs).mean()))
            phase.append({'q':order,'exponential_rate':rate,'samples_per_repetition':count,
                          'repetitions':len(values),'median_estimate':float(np.median(values)),
                          'success_fraction_epsilon_quarter':float(np.mean(np.abs(np.array(values)-1)<=0.25)),
                          'interpretation':'Scalar Gamma-law empirical-average diagnostic only.'})
    bounds=[log_fractional_bound(2,order,0.25) for order in [32,64,128,256,512,1024]]
    summary={name:{'trials':len(seeds),
                   'successes':sum(t['success'] for t in trials if t['family']==name),
                   'max_relative_error':max(t['relative_error'] for t in trials if t['family']==name)}
             for name in families}
    out={'status':'passed','parameters':{'n':n,'q':q,'N':N,'epsilon':epsilon},
         'full_vector_trials':len(trials),'summary_by_matrix_family':summary,
         'query_hash_invariance_checked':True,'zero_input_checked':True,
         'prequery_budget_guard_checked':True,
         'nonpower_of_two_diagnostic':nonpower_result,
         'trials':trials,'empirical_average_scalar_experiments':phase,
         'floating_bound_comparisons':bounds,
         'limitations':['No floating-point stability theorem.',
                        'Finite tests do not establish the universal probability guarantee.',
                        'Scalar empirical-mean diagnostics are not unrestricted oracle lower bounds.'],
         'elapsed_seconds':time.time()-start}
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/'numerical_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['trials','empirical_average_scalar_experiments']},indent=2))

if __name__=='__main__': main()
