"""Standalone integer/rational checker; no third-party dependencies required."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__:
    raise RuntimeError('Run without -O; this checker uses assertions.')

def mm(A,B):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]

def rank(A):
    B=[list(map(F,row)) for row in A]; r=0
    for j in range(len(B[0])):
        pivot=next((i for i in range(r,len(B)) if B[i][j]),None)
        if pivot is None: continue
        B[r],B[pivot]=B[pivot],B[r]
        v=B[r][j];B[r]=[x/v for x in B[r]]
        for i in range(r+1,len(B)):
            v=B[i][j];B[i]=[x-v*y for x,y in zip(B[i],B[r])]
        r+=1
        if r==len(B):break
    return r

def check(path: Path):
    data=json.loads(path.read_text()); A=data['rows']; weights=list(map(F,data['weights']))
    n,d=len(A),len(A[0]); k,N,R=data['k'],data['N'],data['R']
    expected=[]
    for j in range(k):
        for t in range(N):
            for sign in (1,-1):
                row=[0]*d;row[j]=R;row[k+j*N+t]=sign;expected.append(row)
    assert A==expected and n==2*k*N and d==k+k*N
    assert rank(A)==d and all(w>=0 for w in weights)
    covariance=mm(list(map(list,zip(*A))),A)
    expected_diag=[2*N*R*R]*k+[2]*(k*N)
    assert covariance==[[expected_diag[i] if i==j else 0 for j in range(d)] for i in range(d)]
    assert 2*N*R*R>=2
    report=[]
    for case in data['powers']:
        p=case['p'];s=p//2;assert p==2*s and s>=2
        headcost=sum(F(sum(x*x for x in a[k:]))**s for a in A)
        assert headcost==n==F(case['optimal_head_cost'])
        queries=[]
        for item in case['queries']:
            den=item['denominator'];Z=item['projector_numerator']
            assert Z==list(map(list,zip(*Z)))
            assert mm(Z,Z)==[[den*x for x in row] for row in Z]
            assert sum(Z[i][i] for i in range(d))==den*k
            P=[[F(x,den) for x in row] for row in Z]
            costs=[]
            for row in A:
                Pr=[sum(P[i][j]*row[j] for j in range(d)) for i in range(d)]
                costs.append(sum((F(row[i])-Pr[i])**2 for i in range(d))**s)
            original=sum(costs,F(0));weighted=sum((w*c for w,c in zip(weights,costs)),F(0))
            error=abs(original-weighted)/original
            assert original==F(item['original_cost'])
            assert weighted==F(item['weighted_cost'])
            assert error==F(item['relative_error']) and error>F(data['epsilon'])
            queries.append(dict(label=item['label'],original_cost=str(original),weighted_cost=str(weighted),relative_error=str(error)))
        report.append(dict(p=p,queries=queries,optimal_head_cost=str(headcost)))
    return dict(passed=True,rows=n,input_rank=d,query_rank=k,retained_rows=sum(bool(w) for w in weights),
                scope='Exact finite data/projector/cost certificate; optimality follows from the proved covariance/Jensen argument, not from sampled queries.',powers=report)

if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'results'/'exact_even_power_certificate.json'
    print(json.dumps(check(path),indent=2))
