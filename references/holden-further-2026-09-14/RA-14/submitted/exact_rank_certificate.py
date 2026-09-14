"""Create/verify an exact integer rank separation; no floating point ranks."""
from __future__ import annotations
from fractions import Fraction
import argparse, json, random
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def elimination(a):
    m=len(a); n=len(a[0]) if m else 0
    work=[[Fraction(x) for x in row] for row in a]
    row_ids=list(range(m)); cols=[]; r=0
    for c in range(n):
        pivot=next((i for i in range(r,m) if work[i][c]),None)
        if pivot is None: continue
        work[r],work[pivot]=work[pivot],work[r]
        row_ids[r],row_ids[pivot]=row_ids[pivot],row_ids[r]
        pv=work[r][c]
        for i in range(r+1,m):
            if work[i][c]:
                factor=work[i][c]/pv
                for j in range(c,n): work[i][j]-=factor*work[r][j]
        cols.append(c);r+=1
        if r==m: break
    return r,row_ids[:r],cols

def determinant(a):
    n=len(a)
    if any(len(row)!=n for row in a): raise ValueError('Not square')
    w=[[Fraction(x) for x in row] for row in a]; product=Fraction(1)
    for j in range(n):
        pivot=next((i for i in range(j,n) if w[i][j]),None)
        if pivot is None:return 0
        if pivot!=j:w[j],w[pivot]=w[pivot],w[j];product=-product
        pv=w[j][j];product*=pv
        for i in range(j+1,n):
            factor=w[i][j]/pv
            for c in range(j+1,n):w[i][c]-=factor*w[j][c]
            w[i][j]=0
    assert product.denominator==1
    return product.numerator

def minor(a,rows,cols):return [[a[i][j] for j in cols] for i in rows]

def make_features(g,d):
    actual=[row[:3]+[di*x for x in row[:3]]+[row[3]] for row,di in zip(g,d)]
    prefix=[[di**power*x for power in range(4) for x in row] for row,di in zip(g,d)]
    return actual,prefix

def create():
    diagonal=[51,50,50,50,25,25,25,-25,-25,-25,-50,-50]
    for seed in range(100):
        rng=random.Random(seed)
        g=[[rng.randrange(-4,5) for _ in range(4)] for _ in range(12)]
        actual,prefix=make_features(g,diagonal)
        ra,_,_=elimination(actual)
        rt,rows_t,cols_t=elimination(actual[1:])
        rp,rows_p,cols_p=elimination(prefix)
        if (ra,rt,rp)==(7,7,12):break
    else:raise RuntimeError('No rank separation found')
    data=dict(status='EXACT_NONZERO_MINOR_CERTIFICATE',n=12,k=1,q=3,
        epsilon='1/100',spectrum_scale=50,scaled_diagonal=diagonal,
        starting_matrix=g,seed=seed,actual_full_rank=ra,actual_tail_rank=rt,
        prefix_rank=rp,actual_feature_columns=7,prefix_feature_columns=16,
        actual_tail_minor=dict(rows=rows_t,columns=cols_t,
            determinant=str(determinant(minor(actual[1:],rows_t,cols_t)))),
        prefix_minor=dict(rows=rows_p,columns=cols_p,
            determinant=str(determinant(minor(prefix,rows_p,cols_p)))),
        scope='An exact separation between actual-query and full-prefix spaces, not a probabilistic adaptive lower bound.')
    path=ROOT/'results'/'linear_vs_prefix_certificate.json'
    path.write_text(json.dumps(data,indent=2)+'\n')
    return data

def verify(data):
    actual,prefix=make_features(data['starting_matrix'],data['scaled_diagonal'])
    for matrix,key in [(actual[1:],'actual_tail_minor'),(prefix,'prefix_minor')]:
        rec=data[key];got=determinant(minor(matrix,rec['rows'],rec['columns']))
        assert got!=0 and str(got)==rec['determinant']
    assert len(actual[0])==7 and len(actual[1:])==11
    assert len(prefix)==12
    return True

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    data=json.loads((ROOT/'results'/'linear_vs_prefix_certificate.json').read_text()) if args.verify else create()
    verify(data)
    print('Exact rank certificate verified: actual rank/tail rank 7/7, prefix rank 12.')
