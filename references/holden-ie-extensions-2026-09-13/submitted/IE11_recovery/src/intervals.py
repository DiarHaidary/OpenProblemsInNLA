"""Outward-rounded 512-bit dyadic intervals, using integer endpoints only."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
BITS=512
SCALE=1<<BITS

def ceil_div(a,b):
    if b==0:raise ZeroDivisionError
    return -((-a)//b)

@dataclass(frozen=True)
class I:
    lo:int
    hi:int
    def __post_init__(self):
        if self.lo>self.hi:raise ValueError('Reversed interval')
    @staticmethod
    def point(x):
        q=Fraction(x);return I(q.numerator*SCALE//q.denominator,ceil_div(q.numerator*SCALE,q.denominator))
    @staticmethod
    def bounds(lo,hi):
        a,b=Fraction(lo),Fraction(hi)
        if a>b:raise ValueError('Reversed endpoints')
        return I(a.numerator*SCALE//a.denominator,ceil_div(b.numerator*SCALE,b.denominator))
    @staticmethod
    def coerce(x):return x if isinstance(x,I) else I.point(x)
    def __add__(self,o):
        y=I.coerce(o);return I(self.lo+y.lo,self.hi+y.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,o):return self+-I.coerce(o)
    def __rsub__(self,o):return I.coerce(o)+-self
    def __mul__(self,o):
        y=I.coerce(o);p=[self.lo*y.lo,self.lo*y.hi,self.hi*y.lo,self.hi*y.hi]
        return I(min(p)//SCALE,ceil_div(max(p),SCALE))
    __rmul__=__mul__
    def __truediv__(self,o):
        y=I.coerce(o)
        if y.lo<=0<=y.hi:raise ZeroDivisionError('Interval denominator contains zero')
        pairs=[(a*SCALE,b) for a in [self.lo,self.hi] for b in [y.lo,y.hi]]
        return I(min(a//b for a,b in pairs),max(ceil_div(a,b) for a,b in pairs))
    def __rtruediv__(self,o):return I.coerce(o)/self
    def __pow__(self,n):
        if not isinstance(n,int):raise TypeError('Integer exponent required')
        if n<0:return 1/(self**(-n))
        if n==0:return I.point(1)
        if n%2:return self*(self**(n-1))
        lo=0 if self.lo<=0<=self.hi else min(self.lo**2,self.hi**2)
        square=I(lo//SCALE,ceil_div(max(self.lo**2,self.hi**2),SCALE))
        return square**(n//2)
    def contains_zero(self):return self.lo<=0<=self.hi
    def abs_upper(self):return Fraction(max(abs(self.lo),abs(self.hi)),SCALE)
    def midpoint(self):return Fraction(self.lo+self.hi,2*SCALE)
    def lower(self):return Fraction(self.lo,SCALE)
    def upper(self):return Fraction(self.hi,SCALE)
    def strict_inside(self,o):return o.lo<self.lo<=self.hi<o.hi
    def decimal_bounds(self,places=30):
        power=10**places;a=self.lo*power//SCALE;b=ceil_div(self.hi*power,SCALE)
        def fmt(n):
            sign='-' if n<0 else '';n=abs(n)
            return sign+str(n) if places==0 else f'{sign}{n//power}.{n%power:0{places}d}'
        return fmt(a),fmt(b)

def solve_interval(A,b):
    n=len(A)
    if len(b)!=n or any(len(row)!=n for row in A):raise ValueError('Square system required')
    M=[list(row)+[b[i]] for i,row in enumerate(A)];pivots=[]
    for k in range(n):
        row=max(range(k,n),key=lambda i:abs(M[i][k].lo+M[i][k].hi))
        M[k],M[row]=M[row],M[k];p=M[k][k]
        if p.contains_zero():raise ArithmeticError(f'Cannot certify pivot {k}')
        pivots.append(p)
        for i in range(k+1,n):
            f=M[i][k]/p
            for j in range(k+1,n+1):M[i][j]-=f*M[k][j]
            M[i][k]=I.point(0)
    x=[I.point(0)]*n
    for i in range(n-1,-1,-1):x[i]=(M[i][n]-sum((M[i][j]*x[j] for j in range(i+1,n)),I.point(0)))/M[i][i]
    return x,pivots
