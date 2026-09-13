#!/usr/bin/env python3
"""Exact outward-rounded integer proof of a confluent eigenpolynomial sign.

The printed decimal is informational; the sign is decided with integers only.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from math import comb,factorial
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'certification'))
import verify as iv


def floor_root(a:int,n:int)->int:
    if a<0 or n<1:raise ValueError('invalid integer root')
    if a<2:return a
    lo=0;hi=1<<((a.bit_length()+n-1)//n)
    while hi-lo>1:
        m=(lo+hi)//2
        if m**n<=a:lo=m
        else:hi=m
    assert lo**n<=a<(lo+1)**n
    return lo


def convolution(a,b,n):
    out=[iv.ZERO]*(n+1)
    for i in range(min(n+1,len(a))):
        for j in range(min(n-i+1,len(b))):out[i+j]=out[i+j]+a[i]*b[j]
    return out


def coefficients(a,k):
    n=len(a);H=[iv.ZERO]+a;v=[iv.ONE]+[iv.ZERO]*n
    for _ in range(k):v=convolution(v,H,n)
    return sum(v,iv.ZERO)/factorial(k)


def certify(n=11,bits=512,root_digits=100):
    if n < 2: raise ValueError('stages must be at least two')
    iv.BITS=bits;iv.SCALE=1<<bits;iv.ZERO=iv.Ball.scalar(0);iv.ONE=iv.Ball.scalar(1)
    denom=10**root_digits;num=floor_root(factorial(n)*denom**n,n)
    rlo=Fraction(num,denom);rhi=Fraction(num+1,denom)
    assert rlo**n<factorial(n)<rhi**n
    a=[iv.ZERO]*n;a[0]=-iv.Ball.bounds(rlo,rhi)
    for j in range(2,n+1):
        k=n-j+1;den=iv.ONE
        for _ in range(k-1):den=den*a[0]
        a[j-1]=(((-1)**k)*comb(n,k)-coefficients(a,k))*factorial(k-1)/den
    z=[iv.ONE]+[iv.ZERO]*n;power=z.copy()
    for k in range(1,n+1):
        power=convolution(power,[iv.ZERO]+a,n)
        z=[v+p/factorial(k) for v,p in zip(z,power)]
    lead=z[n]*((-1)**n)
    if n == 11:
        assert Fraction(-1664575,10**16) < Fraction(lead.lo,iv.SCALE)
        assert Fraction(lead.hi,iv.SCALE) < Fraction(-1664574,10**16)
    return {'stages':n,'precision_bits':bits,'root_digits':root_digits,
        'root_lower':str(rlo),'root_upper':str(rhi),'root_bracket_verified':True,
        'leading_coefficient_lower':str(Fraction(lead.lo,iv.SCALE)),
        'leading_coefficient_upper':str(Fraction(lead.hi,iv.SCALE)),
        'strictly_negative':lead.hi<0,
        'meaning':'The normalized degree-at-most-n confluent eigenpolynomial has a negative coefficient of t^n. This does not disprove IE-28.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--stages',type=int,default=11)
    ap.add_argument('--report',type=Path);args=ap.parse_args();out=certify(args.stages)
    if args.report:args.report.write_text(json.dumps(out,indent=2)+'\n')
    print('n =',args.stages,'strict negative coefficient:',out['strictly_negative'])
    print('coefficient upper bound (approx):',float(Fraction(out['leading_coefficient_upper'])))
    if args.stages==11 and not out['strictly_negative']:raise SystemExit(1)
if __name__=='__main__':main()
