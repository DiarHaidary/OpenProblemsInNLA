#!/usr/bin/env python3
"""Exact rational check: the global layerwise convexification has optimum 81/16.
This is a statement about a RELAXATION, not about g5. Standard library only.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations
import json
ROOT=Path(__file__).resolve().parents[1]

def model():
    vertices=[];P=[[] for _ in range(5)]
    for k in range(5):
        m=4-k
        for l in product([-1,1],repeat=m):
            for r in product([-1,1],repeat=m):
                V=[[0]*5 for _ in range(5)];lv=(1,)+l;rv=(1,)+r
                for i in range(k,5):
                    for j in range(k,5):V[i][j]=lv[i-k]*rv[j-k]
                vertices.append((k,V))
                for t in range(5):P[t].append(Q(int(t==k)))
    A=[]
    for k in range(4):
        for i in range(k,5):
            for j in range(k,5):
                if i==j==k:continue
                for s in [-1,1]:
                    A.append([Q(s*V[i][j] if t>=k else 0)-P[k][v] for v,(t,V) in enumerate(vertices)])
    # Exact known growth bounds applied to consecutive pivot subsequences.
    bounds={1:Q(1),2:Q(2),3:Q(9,4),4:Q(4)}
    for k in range(4):
        for j in range(k+1,5):
            if j-k+1<=4:A.append([P[j][v]-bounds[j-k+1]*P[k][v] for v in range(len(vertices))])
    return vertices,P,A

def run():
    if not __debug__:raise RuntimeError('Run without -O')
    data=json.loads((ROOT/'data'/'layer_hull_witness.json').read_text());V,P,A=model();w=[Q(0)]*len(V)
    for rec in data['support']:
        i=rec['vertex'];assert 0<=i<len(V) and w[i]==0;w[i]=Q(rec['weight'])
    assert all(t>=0 for t in w)
    dot=lambda a:sum(x*y for x,y in zip(a,w))
    assert dot(P[0])==1 and all(dot(a)<=0 for a in A)
    pivots=[dot(p) for p in P]
    assert pivots[4]==Q(81,16)
    # Matching universal upper bound: p5 <= (9/4)p3 <= (9/4)^2*p1.
    assert pivots[4]<=Q(9,4)*pivots[2] and pivots[2]<=Q(9,4)*pivots[0]
    # Verify directly that this witness has a non-rank-one layer.
    layers=[[[Q(0) for _ in range(5)] for _ in range(5)] for _ in range(5)]
    for weight,(k,M) in zip(w,V):
        for i in range(k,5):
            for j in range(k,5):layers[k][i][j]+=weight*M[i][j]
    failure=None
    for k,M in enumerate(layers):
        for i1,i2 in combinations(range(k,5),2):
            for j1,j2 in combinations(range(k,5),2):
                minor=M[i1][j1]*M[i2][j2]-M[i1][j2]*M[i2][j1]
                if minor:failure=dict(layer=k+1,rows=[i1+1,i2+1],columns=[j1+1,j2+1],minor=str(minor));break
            if failure:break
        if failure:break
    assert failure is not None
    out=dict(status='PASS: exact RELAXATION optimum is 81/16',global_solution=False,
        not_a_counterexample=True,corner_count=len(V),inequality_count=len(A),
        positive_weights=sum(t>0 for t in w),relaxed_pivots=[str(t) for t in pivots],
        non_rank_one_minor=failure,relaxation_value='81/16')
    (ROOT/'results'/'layer_hull_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    return out
if __name__=='__main__':
    r=run();print(r['status']);print('This value is NOT g5 and the mixture is NOT a counterexample.')
