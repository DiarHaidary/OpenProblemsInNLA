#!/usr/bin/env python3
"""Independent exact-integer interval verifier for IE-28 local certificates.

No third-party dependencies. Every arithmetic operation encloses the exact
real result; floating-point values are used only for optional display.
A passing certificate proves a unique positive diagonal in the listed box
for EVERY node vector in the listed node box. It is NOT an all-stage proof.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import json

BITS = 256
SCALE = 1 << BITS

def ceildiv(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError('positive denominator required')
    return -((-a) // b)

@dataclass(frozen=True)
class Ball:
    lo: int
    hi: int
    def __post_init__(self):
        if self.lo > self.hi: raise ValueError('reversed interval')
    @classmethod
    def scalar(cls, x=0):
        if isinstance(x, cls): return x
        f = Fraction(x)
        return cls((f.numerator*SCALE)//f.denominator,
                   ceildiv(f.numerator*SCALE, f.denominator))
    @classmethod
    def bounds(cls, lo, hi):
        a,b=Fraction(lo),Fraction(hi)
        if a>b: raise ValueError('reversed bounds')
        return cls(cls.scalar(a).lo, cls.scalar(b).hi)
    def __add__(self, other):
        b=Ball.scalar(other);return Ball(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):return Ball(-self.hi,-self.lo)
    def __sub__(self,other):return self+-Ball.scalar(other)
    def __rsub__(self,other):return Ball.scalar(other)+-self
    def __mul__(self,other):
        b=Ball.scalar(other)
        p=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return Ball(min(p)//SCALE,ceildiv(max(p),SCALE))
    __rmul__=__mul__
    def reciprocal(self):
        if self.lo <= 0 <= self.hi: raise ZeroDivisionError('interval contains zero')
        if self.hi < 0: return -(-self).reciprocal()
        return Ball(SCALE*SCALE//self.hi,ceildiv(SCALE*SCALE,self.lo))
    def __truediv__(self, other):return self*Ball.scalar(other).reciprocal()
    def __rtruediv__(self,other):return Ball.scalar(other)*self.reciprocal()
    def magnitude(self):return max(abs(self.lo),abs(self.hi))

ZERO=Ball.scalar(0)
ONE=Ball.scalar(1)

def det_interval(A):
    """Division-free determinant via subset dynamic programming."""
    n=len(A); dp={0:ONE}
    for mask in range(1,1<<n):
        k=mask.bit_count(); row=k-1; val=ZERO
        for col in range(n):
            if mask&(1<<col):
                # Laplace expansion in the last row of this minor.
                pos=(mask & ((1<<col)-1)).bit_count()
                term=dp[mask^(1<<col)]*A[row][col]
                val=val+term if (row+pos)%2==0 else val-term
        dp[mask]=val
    return dp[(1<<n)-1]

def coefficients(C):
    n=len(C)
    M=[[ZERO for _ in C] for _ in C]
    for i in range(n):
        for j in range(n):
            if i!=j:M[i][j]=ONE/(C[i]-C[j])
        M[i][i]=ONE/C[i]+sum((M[i][j] for j in range(n) if j!=i),ZERO)
    out=[]
    for k in range(1,n+1):
        for ii in combinations(range(n),k):
            out.append((ii,det_interval([[M[i][j] for j in ii] for i in ii])))
    return out

def product(xx):
    p=ONE
    for x in xx:p=p*x
    return p

def evaluate(center,X,cs):
    n=len(center);F=[-Ball.scalar(comb(n,k)) for k in range(1,n+1)]
    J=[[ZERO for _ in range(n)] for _ in range(n)]
    for ii,a in cs:
        k=len(ii)-1
        F[k]=F[k]+a*product(center[i] for i in ii)
        for j in ii:J[k][j]=J[k][j]+a*product(X[i] for i in ii if i!=j)
    return F,J

def verify(data,verbose=False):
    global BITS,SCALE,ZERO,ONE
    bits=data.get('precision_bits',256)
    if not isinstance(bits,int) or bits<128 or bits>4096:raise ValueError('invalid precision')
    BITS=bits;SCALE=1<<bits;ZERO=Ball.scalar(0);ONE=Ball.scalar(1)
    cb=data['node_box'];n=len(cb)
    if not 2<=n<=20:raise ValueError('unsupported dimension')
    if len(data['center'])!=n or len(data['preconditioner'])!=n:raise ValueError('shape')
    C=[Ball.bounds(a,b) for a,b in cb]
    if C[0].lo<=0 or any(C[i].hi>=C[i+1].lo for i in range(n-1)) or C[-1].hi>SCALE:
        raise ValueError('node box must be strictly positive, separated, and <=1')
    centers=[Fraction(s) for s in data['center']]
    r=Fraction(data['radius'])
    if r<=0:raise ValueError('positive radius required')
    if any(x-r<=0 for x in centers):raise ValueError('diagonal box is not positive')
    point=[Ball.scalar(s) for s in centers]
    X=[Ball.bounds(s-r,s+r) for s in centers]
    R=[[Ball.scalar(s) for s in row] for row in data['preconditioner']]
    if any(len(row)!=n for row in R):raise ValueError('matrix shape')
    F,J=evaluate(point,X,coefficients(C))
    RF=[sum((R[i][k]*F[k] for k in range(n)),ZERO) for i in range(n)]
    E=[[(ONE if i==j else ZERO)-sum((R[i][k]*J[k][j] for k in range(n)),ZERO)
        for j in range(n)] for i in range(n)]
    eta=max(z.magnitude() for z in RF)
    q=max(sum(z.magnitude() for z in row) for row in E)
    # Integer form of eta/SCALE + (q/SCALE)*r < r.
    strict=(eta*r.denominator+q*r.numerator < SCALE*r.numerator)
    passed=(q<SCALE and strict)
    ordered=all(centers[i]+r<centers[i+1]-r for i in range(n-1))
    ans={'label':data.get('label','unnamed'),'stages':n,'passed':passed,
         'q_upper_exact':str(Fraction(q,SCALE)),
         'eta_upper_exact':str(Fraction(eta,SCALE)),
         'radius_exact':str(r),'strict_contraction':q<SCALE,
         'strict_self_mapping':strict,'positive':True,'ordered':ordered,
         'scope':'for every node vector in the specified node box; unique root only within the diagonal box'}
    if verbose:
        print(f"{ans['label']}: {'PASS' if passed else 'FAIL'}; n={n}; "
              f"q <= {float(Fraction(q,SCALE)):.4g}; eta <= {float(Fraction(eta,SCALE)):.4g}; r={float(r):.4g}")
    return ans

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('certificates',nargs='+',type=Path)
    ap.add_argument('--report',type=Path)
    args=ap.parse_args();out=[]
    for fn in args.certificates:
        obj=json.loads(fn.read_text())
        for item in (obj if isinstance(obj,list) else [obj]):out.append(verify(item,True))
    if args.report:args.report.write_text(json.dumps(out,indent=2)+'\n')
    if not all(x['passed'] for x in out):raise SystemExit(1)

if __name__=='__main__':main()
