from fractions import Fraction as F
from random import Random
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'submitted/IE-27_research_update/prior_results/code'))
from verify import I,SCALE,jacobi_coefficients
rng=Random(270913)
checks=0
def encl(i,values):
 global checks
 assert F(i.lo,SCALE)<=min(values)<=max(values)<=F(i.hi,SCALE)
 checks+=1
for k in range(1500):
 a,b=sorted([F(rng.randrange(-10000,10001),rng.randrange(1,1000)) for _ in range(2)])
 c,d=sorted([F(rng.randrange(-10000,10001),rng.randrange(1,1000)) for _ in range(2)])
 x=I(I.rational(a.numerator,a.denominator).lo,I.rational(b.numerator,b.denominator).hi)
 y=I(I.rational(c.numerator,c.denominator).lo,I.rational(d.numerator,d.denominator).hi)
 encl(x+y,[a+c,b+d]);encl(x-y,[a-d,b-c]);encl(x*y,[a*c,a*d,b*c,b*d])
 encl(x.square(),[a*a,b*b]+([F(0)] if a<=0<=b else []))
 if not c<=0<=d:encl(x/y,[a/c,a/d,b/c,b/d])
# Independent Legendre recurrence, converted to variable t with x=2t-1.
def plus(a,b):
 return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]
def scale(a,c):return [v*c for v in a]
def xmul(a):return plus(scale(a,-1),[0]+scale(a,2))
p0,p1=[F(1)],[F(-1),F(2)]
for q in range(2,129):
 p=scale(plus(scale(xmul(p1),2*q-1),scale(p0,-(q-1))),F(1,q))
 j=jacobi_coefficients(q)
 rhs=plus(scale(j,-2),[0]+scale(j,2))
 assert plus(p,scale(p1,-1))==rhs
 # Check Jacobi ODE from coefficients, separately from report.
 for k in range(q):
  v=(k+1)**2*(j[k+1] if k+1<q else 0)+(q*q-1-k*(k+2))*j[k]
  assert v==0
 p0,p1=p1,p
print(json.dumps({'status':'PASS','interval_fraction_enclosure_checks':checks,'legendre_jacobi_identity_stages':'2..128','jacobi_ODE_stages':'2..128'}))
