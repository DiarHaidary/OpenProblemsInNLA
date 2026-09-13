#!/usr/bin/env python3
"""Rational containment tests for the interval kernel; no floating arithmetic."""
from fractions import Fraction as Q
from pathlib import Path
import random,json
from intervals import I

def run():
    if not __debug__:raise RuntimeError('Run without -O')
    rng=random.Random(11);checks=0
    for _ in range(1000):
        a,b=sorted([Q(rng.randrange(-100,101),rng.randrange(1,101)) for _ in range(2)])
        c,d=sorted([Q(rng.randrange(-100,101),rng.randrange(1,101)) for _ in range(2)])
        A=I.bounds(a,b);B=I.bounds(c,d)
        for C,vals in [(A+B,[a+c,b+d]),(A-B,[a-d,b-c]),(A*B,[a*c,a*d,b*c,b*d])]:
            assert C.lower()<=min(vals)<=max(vals)<=C.upper();checks+=1
        if not B.contains_zero():
            C=A/B;vals=[a/c,a/d,b/c,b/d]
            assert C.lower()<=min(vals)<=max(vals)<=C.upper();checks+=1
        for n in range(5):
            C=A**n;vals=[a**n,b**n]
            if n>0 and n%2==0 and a<=0<=b:vals.append(Q(0))
            assert C.lower()<=min(vals)<=max(vals)<=C.upper();checks+=1
    out=dict(status='PASS',containment_tests=checks,seed=11)
    (Path(__file__).resolve().parents[1]/'results'/'interval_tests.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS:',checks,'rational interval containment tests');return out
if __name__=='__main__':run()
