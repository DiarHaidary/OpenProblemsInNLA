"""Exact finite checks for the round-four manuscript. Python standard library only."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math
import time

ROOT = Path(__file__).resolve().parents[1]


def kron(factors):
    out = [1]
    for f in factors:
        out = [a * b for a in out for b in f]
    return out


def matvec(M, x):
    return [sum(a*b for a,b in zip(row,x)) for row in M]


def psd_matrix(N):
    B = [[((i+2)*(j+3) + i*i - 2*j) % 7 - 3 for j in range(3)] for i in range(N)]
    return [[sum(B[i][k]*B[j][k] for k in range(3)) + (i==j) for j in range(N)] for i in range(N)]


def diagonal_identity(n, q):
    N=n**q; M=psd_matrix(N); d=[M[i][i] for i in range(N)]; tau=sum(d)
    counts=[0]*N; error_norm=F(0); correction_mean=F(0); correction_second=F(0)
    cond_variance=F(0); B=(N-1).bit_length(); D=2**B
    weights=[F(D//N + (i<D%N),D) for i in range(N)]
    assert sum(weights)==1 and all(p>=F(1,2*N) for p in weights)
    samples=2**(n*q)
    for signs in product((-1,1),repeat=n*q):
        x=kron([signs[j*n:(j+1)*n] for j in range(q)])
        y=matvec(M,x); a=[x[i]*y[i] for i in range(N)]
        err=[d[i]-a[i] for i in range(N)]
        for i in range(N): counts[i]+=a[i]
        error_norm+=sum(v*v for v in err)
        base=sum(a)
        conditional_mean=F(0); conditional_second=F(0)
        for i,p in enumerate(weights):
            T=F(base)+F(err[i])/p
            conditional_mean+=p*T
            conditional_second+=p*(T-tau)**2
        assert conditional_mean==tau
        rhs=sum(F(err[i]**2)/weights[i] for i in range(N))-sum(err)**2
        assert conditional_second==rhs
        correction_mean+=conditional_mean
        correction_second+=conditional_second
        cond_variance+=rhs
    assert [F(v,samples) for v in counts]==list(map(F,d))
    offdiag=sum(M[i][j]**2 for i in range(N) for j in range(N) if i!=j)
    assert error_norm/samples==offdiag
    assert correction_mean/samples==tau
    assert correction_second==cond_variance
    assert correction_second/samples<=2*N*tau*tau
    return {'n':n,'q':q,'N':N,'enumerated_training_probes':samples,
            'enumerated_training_coordinate_pairs':samples*N,
            'mean_squared_diagonal_error':str(error_norm/samples),
            'single_training_single_correction_variance':str(correction_second/samples),
            'passed':True}

# Gaussian-rational arithmetic as (real Fraction, imaginary Fraction).
def ga(x=0,y=0): return (F(x),F(y))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,s): return (a[0]*s,a[1]*s)

def gkron(factors):
    v=[ga(1)]
    for f in factors: v=[mul(a,b) for a in v for b in f]
    return v


def interpolation(n,q):
    factors=[]
    for j in range(q):
        factors.append([ga((j+2*i)%5-2,(2*j+i)%5-2) for i in range(n)])
    N=n**q
    diag=[(i%5)+1 for i in range(N)]; u=[(i*3)%7-3 for i in range(N)]
    def real_map(v):
        dot=sum(u[i]*v[i] for i in range(N))
        return [diag[i]*v[i]+u[i]*dot for i in range(N)]
    target_input=gkron(factors)
    tr=real_map([v[0] for v in target_input]); ti=real_map([v[1] for v in target_input])
    target=list(zip(tr,ti)); observed=[ga() for _ in range(N)]
    actual_calls=0
    for j in range(q+1):
        raw=[[a[0]+j*a[1] for a in factor] for factor in factors]
        response=real_map(kron(raw)); actual_calls+=1
        weight=ga(1)
        for h in range(q+1):
            if h!=j: weight=mul(weight,ga(F(-h,j-h),F(1,j-h)))
        observed=[add(v,scale(weight,r)) for v,r in zip(observed,response)]
    assert observed==target
    assert actual_calls==q+1
    return {'n':n,'q':q,'N':N,'real_product_calls':actual_calls,'passed':True}


def moment_checks():
    checks=0; max_slack=-float('inf')
    for n in range(2,65):
        D=math.log(n)-math.fsum(1/k for k in range(2,n+1))
        V=math.fsum(1/(k*k) for k in range(2,n+1))
        for i in range(1,101):
            t=i/100
            f=t*math.log(n)-math.fsum(math.log1p(t/k) for k in range(2,n+1))
            slack=f-D*t-V*t*t/2
            assert slack<=2e-14
            max_slack=max(max_slack,slack); checks+=1
        c2=math.exp(math.log(n)-math.fsum(math.log1p(1/k) for k in range(2,n+1)))
        assert abs(c2-2*n/(n+1))<1e-12
    assert 1458<1600  # exact squared comparison in Section 7.3
    return {'inequality_grid_points':checks,'largest_floating_slack':max_slack,
            'note':'Grid inequalities are floating-point diagnostics; interpolation and diagonal checks are exact.',
            'passed':True}


def main():
    start=time.time()
    out={'status':'passed','exact_arithmetic':'fractions.Fraction',
         'diagonal_checks':[diagonal_identity(n,q) for n,q in [(2,1),(2,2),(2,3),(3,1),(3,2)]],
         'interpolation_checks':[interpolation(2,q) for q in range(1,9)] + [interpolation(3,q) for q in range(1,5)],
         'moment_diagnostics':moment_checks()}
    out['elapsed_seconds']=time.time()-start
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/'exact_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
