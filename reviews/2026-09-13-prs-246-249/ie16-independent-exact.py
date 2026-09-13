from fractions import Fraction as F
from math import isqrt
from itertools import combinations
from collections import Counter
from decimal import Decimal, localcontext
import json

class Qw:
    def __init__(self,a=0,b=0): self.a,self.b=F(a),F(b)
    def __add__(self,z):
        z=z if isinstance(z,Qw) else Qw(z)
        return Qw(self.a+z.a,self.b+z.b)
    __radd__=__add__
    def __neg__(self): return Qw(-self.a,-self.b)
    def __sub__(self,z): return self+-z
    def __mul__(self,z):
        z=z if isinstance(z,Qw) else Qw(z)
        return Qw(self.a*z.a-self.b*z.b,self.a*z.b+self.b*z.a-self.b*z.b)
    __rmul__=__mul__
    def conj(self): return Qw(self.a-self.b,-self.b)
    def norm2(self): return self.a**2-self.a*self.b+self.b**2
    def __truediv__(self,z):
        z=z if isinstance(z,Qw) else Qw(z)
        return self*z.conj()*F(1,z.norm2())
    def __pow__(self,n):
        ans=Qw(1)
        for _ in range(n): ans=ans*self
        return ans
    def __eq__(self,z):
        z=z if isinstance(z,Qw) else Qw(z)
        return (self.a,self.b)==(z.a,z.b)
    def __hash__(self): return hash((self.a,self.b))

w=Qw(0,1)
e=F(1,1000)
D=1+e+3*e**2+e**3+e**4
c=(1+e)/D
m=F(3003003000,1001003001001)
assert w**3==1 and w!=1
labels=[(a,b) for a in range(3) for b in range(3)]
nodes=[w**a+e*w**b for a,b in labels]
assert len(set(nodes))==9 and all(z.norm2()>0 for z in nodes)
residuals=[Qw(1)-c*z**3 for z in nodes]
weights=[F(332333665667 if a==b else 334334667667,3003009003003) for a,b in labels]
H=1-3*e+e**2-3*e**3+e**4
Q=(1+e)**2*(1+e+e**2)
assert weights==[H/(9*D) if a==b else Q/(9*D) for a,b in labels]
assert min(weights)>0 and sum(weights)==1
assert all(r.norm2()==m*m for r in residuals)
assert m==3*e*(1+e+e**2)/D
for ell in range(1,5):
    assert sum((nu*r.conj()*z**ell for nu,r,z in zip(weights,residuals,nodes)),Qw())==0
lower,near,far=F(999,1000),F(13,7500),F(2603,1500)
assert 109*near*far**3<lower**4
assert 146*near**2*far**2<lower**4
for i,z in enumerate(nodes):
    assert z.norm2()>=lower**2
    for j,t in enumerate(nodes):
        assert (z-t).norm2()<=far**2
        if labels[i][0]==labels[j][0]: assert (z-t).norm2()<=near**2

def root_bounds(q):
    scale=10**55
    n=isqrt(q.numerator*scale*scale//q.denominator)
    lo,hi=F(n,scale),F(n+1,scale)
    assert lo*lo<=q<hi*hi
    return lo,hi

records=[]
profiles=Counter()
for inds in combinations(range(9),5):
    profile=tuple(sorted((sum(labels[i][0]==a for i in inds) for a in range(3)),reverse=True))
    profiles[profile]+=1
    companions={i:sum(j!=i and labels[j][0]==labels[i][0] for j in inds) for i in inds}
    assert sum(v>=1 for v in companions.values())>=4 or sum(v>=2 for v in companions.values())>=3
    lows,highs=[],[]
    for i in inds:
        ell=Qw(1)
        for j in inds:
            if j!=i: ell=ell*(-nodes[j])/(nodes[i]-nodes[j])
        q=ell.norm2()
        assert q>0
        if companions[i]>=1: assert q>109**2
        if companions[i]>=2: assert q>146**2
        lo,hi=root_bounds(q)
        lows.append(lo);highs.append(hi)
    Mlo,Mhi=1/sum(highs),1/sum(lows)
    assert 0<Mlo<Mhi<F(23,10000)
    records.append((inds,Mlo,Mhi))
B_lo=max(row[1] for row in records)
B_hi=max(row[2] for row in records)
assert m>F(299,100000)
assert m/B_hi>F(13,10)

def atan_bounds(x,terms=55):
    s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(terms)),F(0))
    t=s+(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(s,t),max(s,t)
a,b=atan_bounds(F(1,5)); c,d=atan_bounds(F(1,239))
pi_lo,pi_hi=16*a-4*d,16*b-4*c
assert F(314,100)<pi_lo and 4/pi_lo<F(13,10)
assert m-4/pi_lo*B_hi>0

def decimal(q):
    with localcontext() as ctx:
        ctx.prec=50
        return str(Decimal(q.numerator)/Decimal(q.denominator))
summary={
    'basis':'Independent standard-library Fraction arithmetic in Q(omega), omega^2+omega+1=0; certified rational square-root intervals at 55 decimal places; no submitted verifier imported.',
    'all_checks_passed':True,
    'points':9,'weights':'9 strictly positive; exact sum one; match source H/(9D),Q/(9D)',
    'norms_squared':'all nine exactly m^2','moments':'four exact complex zero sums',
    'subset_count':len(records),'profiles':{str(k):v for k,v in profiles.items()},
    'full_minimum':str(m),'full_decimal':decimal(m),
    'B_interval':[str(B_lo),str(B_hi)],'B_decimal_interval':[decimal(B_lo),decimal(B_hi)],
    'ratio_decimal_interval':[decimal(m/B_hi),decimal(m/B_lo)],
    'positive_gap_lower':decimal(m-4/pi_lo*B_hi),
    'maximum_subset_labels':[labels[i] for i in max(records,key=lambda row:row[1])[0]],
    'checks':['distinct/nonzero nodes','source and Lean exact weights agree','all point/near/far squared bounds','both rational coefficient margins','all 126 occupancy disjunctions','all 630 exact Lagrange squared norms','every subset minimum interval positive and below 23/10000','actual subset maximum interval and ratio','Machin arctangent alternating bounds imply pi>3.14'],
    'limitation':'Arithmetic independently checks finite constants and all subset Lagrange values. Analytic minimax/attainment justification comes from source review; this script does not run Lean or reprove Machin identity.'
}
with open('/private/tmp/nla-246-independent-exact.json','w') as f:json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
