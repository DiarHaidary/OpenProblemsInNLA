"""Seeded numerical diagnostics; these are not proofs of the probability bounds."""
from __future__ import annotations
import json
import math
from pathlib import Path
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from ra11 import (DenseProductOracle, ParallelProductAccess, complex_product_via_real,
                  complex_second_moment, kron_vectors, product_trace_exact,
                  proved_bound_functions, product_trace_hutchpp)


def interpolation_checks(rng):
    rows=[]
    for n,q in [(2,2),(2,4),(2,6),(3,3)]:
        N=n**q
        b=rng.normal(size=(N,max(2,N//3)))
        M=b@b.T
        factors=[rng.normal(size=n)+1j*rng.normal(size=n) for _ in range(q)]
        oracle=DenseProductOracle(M,n,q)
        computed=complex_product_via_real(oracle,factors)
        expected=M@kron_vectors(factors)
        error=np.linalg.norm(computed-expected)/np.linalg.norm(expected)
        assert error<1e-10 and oracle.calls==q+1
        rows.append({"n":n,"q":q,"relative_error":float(error),"real_calls":oracle.calls})
    return rows


def product_checks(rng):
    rows=[]
    for n,q in [(2,4),(3,3),(5,2)]:
        factors=[]
        for _ in range(q):
            g=rng.normal(size=(n,n)); factors.append(g@g.T+np.eye(n))
        M=factors[0]
        for a in factors[1:]: M=np.kron(M,a)
        oracle=DenseProductOracle(M,n,q)
        access=ParallelProductAccess(oracle,n,q,rng)
        estimate=product_trace_exact(access)
        error=abs(estimate-np.trace(M))/np.trace(M)
        assert error<1e-9 and oracle.calls==n
        rows.append({"n":n,"q":q,"trace_relative_error":float(error),"real_calls":oracle.calls})
    # Exercise the low-rank/variance-reduced branch using a product oracle which
    # does not form the n**q by n**q matrix, but returns the full vector response.
    n,q,r=20,2,2
    factors=[]
    for _ in range(q):
        u,_=np.linalg.qr(rng.normal(size=(n,n)))
        factors.append((u*np.geomspace(1,0.001,n))@u.T)
    calls=0
    def oracle(vectors):
        nonlocal calls
        calls+=1
        assert all(not np.iscomplexobj(v) for v in vectors)
        return kron_vectors([a@v for a,v in zip(factors,vectors)])
    access=ParallelProductAccess(oracle,n,q,rng)
    streams=[np.random.default_rng(511+i) for i in range(q)]
    estimate=product_trace_hutchpp(access,r,streams)
    true=math.prod(float(np.trace(a)) for a in factors)
    assert np.isfinite(estimate) and calls<=5*r+5
    rows.append({"n":n,"q":q,"r":r,"branch":"parallel Hutch++ demonstration; r is not an accuracy certificate",
                 "estimate":estimate,"truth":true,"relative_error":abs(estimate-true)/true,"real_calls":calls})
    return rows


def moment_checks(rng):
    rows=[]
    samples=60000
    for n,q,kind in [(2,3,'general PSD'),(3,2,'general PSD'),(2,4,'product rank one')]:
        N=n**q
        if kind=='product rank one':
            v=kron_vectors([rng.normal(size=n) for _ in range(q)]);v/=np.linalg.norm(v)
            M=np.outer(v,v)
        else:
            g=rng.normal(size=(N,N));M=g@g.T;M/=np.trace(M)
        X=np.ones((samples,1),dtype=complex)
        for _ in range(q):
            z=rng.normal(size=(samples,n))+1j*rng.normal(size=(samples,n))
            z*=np.sqrt(n/np.sum(abs(z)**2,axis=1))[:,None]
            X=(X[:,:,None]*z[:,None,:]).reshape(samples,-1)
        values=np.einsum('bi,ij,bj->b',X.conj(),M,X,optimize=True).real
        theoretical=complex_second_moment(M,n,q)
        empirical=float(np.mean(values**2))
        assert abs(empirical/theoretical-1)<0.05
        if kind=='product rank one':
            assert abs(theoretical-(2*n/(n+1))**q)<1e-10
        rows.append({"n":n,"q":q,"matrix_kind":kind,"samples":samples,
                     "mean":float(values.mean()),"theoretical_second_moment":theoretical,
                     "empirical_second_moment":empirical,
                     "relative_second_moment_error":abs(empirical/theoretical-1)})
    return rows


def adaptive_wishart_diagnostic(rng):
    d,t,samples=10,3,7000
    residuals=[]; known=[]
    for _ in range(samples):
        G=rng.normal(size=(d,d));W=G.T@G
        u=np.zeros(d);u[0]=1
        U=[]
        for j in range(t):
            U.append(u)
            if j<t-1:
                v=W@u
                for a in U: v-=a*np.dot(a,v)
                # second orthogonalization for floating-point reliability
                for a in U: v-=a*np.dot(a,v)
                u=v/np.linalg.norm(v)
        U=np.column_stack(U);Y=W@U;C=U.T@Y
        a=float(np.trace(np.linalg.solve(C,Y.T@Y)))
        known.append(a);residuals.append(float(np.trace(W))-a)
    k=(d-t)**2
    residuals=np.asarray(residuals)
    mean=float(residuals.mean());variance=float(residuals.var())
    assert abs(mean/k-1)<0.025 and abs(variance/(2*k)-1)<0.07
    return {"d":d,"adaptive_rounds":t,"samples":samples,"predicted_chi_square_df":k,
            "residual_mean":mean,"predicted_mean":k,"residual_variance":variance,
            "predicted_variance":2*k,
            "empirical_correlation_with_known_trace":float(np.corrcoef(residuals,known)[0,1]),
            "limitation":"Moment/correlation diagnostics do not establish conditional independence."}



def zero_and_real_oracle_checks():
    rng=np.random.default_rng(90909)
    n,q=3,2
    oracle=DenseProductOracle(np.zeros((n**q,n**q)),n,q)
    access=ParallelProductAccess(oracle,n,q,rng)
    assert access.zero and product_trace_exact(access)==0.0 and oracle.calls==1
    try:
        oracle([np.ones(n,dtype=complex),np.ones(n)])
    except ValueError:
        pass
    else:
        raise AssertionError("The actual oracle accepted a complex input.")
    assert oracle.calls==1
    return {"zero_matrix_output":0.0,"real_calls":1,"complex_input_rejected":True}



def conditioning_spectrum_checks():
    rows=[]
    for q in (2,3,4,8,12,20):
        length=q+1
        theta=np.pi*np.arange(length)/length
        gram=np.cos(theta[:,None]-theta[None,:])**q
        observed=np.linalg.eigvalsh(gram)
        expected=np.sort([length*2.0**(-q)*math.comb(q,j) for j in range(length)])
        relative_error=float(np.max(abs(observed-expected)/expected))
        assert relative_error<1e-8
        rows.append({"q":q,"predicted_squared_condition_number":math.comb(q,q//2),
                     "maximum_relative_eigenvalue_error":relative_error})
    return rows


def main():
    start=time.perf_counter();rng=np.random.default_rng(20260913)
    result={"seed":20260913,"interpolation":interpolation_checks(rng),
            "product_access":product_checks(rng),"complex_moments":moment_checks(rng),
            "adaptive_Wishart":adaptive_wishart_diagnostic(rng),
            "edge_cases":zero_and_real_oracle_checks(),
            "conditioning_spectrum":conditioning_spectrum_checks(),
            "bounds":[dict(n=n,q=q,epsilon=e,**proved_bound_functions(n,q,e))
                      for n,q,e in [(2,8,.1),(2,20,.1),(4,8,.01),(2,6,1/64),(100,4,.01)]]}
    result['all_diagnostic_assertions_passed']=True
    result['elapsed_seconds']=round(time.perf_counter()-start,3)
    (ROOT/'results'/'numerical_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
