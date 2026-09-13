#!/usr/bin/env python3
"""Generate and independently verify a strict-CP rational witness.
Verification uses Fraction only; algebraic root centers are not assumed exact.
"""
from fractions import Fraction
from pathlib import Path
import json,time,sys
from candidate import make_candidate,eliminate,constraints
ROOT=Path(__file__).resolve().parents[1]

def bracket(x,digits=70):
    D=10**digits;n=x.numerator*D//x.denominator
    def fmt(v):
        sign='-' if v<0 else '';q,r=divmod(abs(v),D);return f'{sign}{q}.{r:0{digits}d}'
    return fmt(n),fmt(n+1)

def generate():
    center=json.loads((ROOT/'data'/'root_centers.json').read_text())
    A=make_candidate(Fraction(center['g']),Fraction(center['z']));t=1-Fraction(1,10**50);D=10**100
    def rounded(x):
        q,r=divmod(x.numerator,x.denominator);return q+int(2*r>=x.denominator)
    data=dict(denominator=str(D),numerators=[[str(rounded(Fraction(a)*t**(i+j)*D)) for j,a in enumerate(row)] for i,row in enumerate(A)],
        strict_lower_bound='4.13251707863247285422334685327737126995279153779',
        construction='Round D(t) A(center) D(t) to denominator 10^100, D(t)_ii=t^(i-1), t=1-10^-50.')
    (ROOT/'data'/'rational_witness.json').write_text(json.dumps(data,indent=2)+'\n')

def verify():
    if not __debug__:raise RuntimeError('Run without -O')
    start=time.time();data=json.loads((ROOT/'data'/'rational_witness.json').read_text());D=int(data['denominator'])
    A=[[Fraction(int(a),D) for a in row] for row in data['numerators']]
    assert len(A)==5 and all(len(row)==5 for row in A)
    assert A[0][0]==1 and max(abs(a) for row in A for a in row)==1
    stages=eliminate(A);p=[s[0][0] for s in stages];cs=constraints(stages)
    assert len(cs)==100 and all(a>0 for _,a in cs) and all(a>0 for a in p)
    assert p[-1]>Fraction(data['strict_lower_bound']) and p[-1]>max(p[:-1])
    det=Fraction(1)
    for a in p:det*=a
    assert det>0
    out=dict(status='PASS: exact rational strict-CP witness',global_solution=False,arithmetic='fractions.Fraction only',
        inequality_count=100,all_nontrivial_inequalities_strict=True,strict_lower_bound=data['strict_lower_bound'],
        fifth_pivot=str(p[-1]),fifth_pivot_enclosure=bracket(p[-1]),minimum_slack=bracket(min(a for _,a in cs)),
        pivots=[bracket(a) for a in p],seconds=time.time()-start)
    (ROOT/'results'/'rational_certificate.json').write_text(json.dumps(out,indent=2)+'\n');return out
if __name__=='__main__':
    if '--generate' in sys.argv:generate()
    r=verify();print(r['status']);print('fifth pivot >',r['strict_lower_bound'])
