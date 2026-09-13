"""Independent exact roots-of-unity and derivative checks; no submitted imports."""
from math import comb, factorial
import json
import sympy as s
coefficient_checks=0
for p in range(1,31):
 for q in range(1,31):
  N=p+q
  for i in range(p+2):
   for k in range(q+2):
    t=i+k
    # The sum over roots a^N=eps^(q-1) is zero unless N divides t.
    c=0 if t%N else N*comb(p+1,i)*comb(q+1,k)*sum(e**(k+1+(q-1)*(t//N)) for e in (-1,1))
    assert c==(2*N*(p+1)*(q+1) if (i,k)==(p,q) else 0)
    coefficient_checks+=1
x,y,u,v=s.symbols('x y u v')
def cat(F,A,B,i,k):
 rows=[(a,A-i-a,b,B-k-b) for a in range(A-i+1) for b in range(B-k+1)]
 cols=[]
 for a in range(i+1):
  for b in range(k+1):
   f=s.Poly(s.diff(F,x,a,y,i-a,u,b,v,k-b),x,y,u,v)
   cols.append([f.coeff_monomial(m) for m in rows])
 return s.Matrix(cols).T
# Repeated-factor, balanced and pure-power edge cases, after independent GL2 changes.
tests=[((x+y)**3*(2*x-y)**2,5,(u-v)**2*(u+3*v),3,3,4,2,3),
 ((x+2*y)**2*(3*x-y)**2,4,(u+v)**2*(u-v)**2,4,3,3,3,3),
 ((x+y)**4,4,(u-v)**3*(2*u+v),4,1,5,2,4)]
for F,A,G,B,r,ss,rp,sp in tests:
 assert cat(s.expand(F*G),A,B,r-1,sp-1).rank()==r*rp
 assert cat(s.expand(F*G),A,B,ss-1,rp-1).rank()==r*rp
print(json.dumps(dict(result='PASS',parameter_pairs=900,exact_coefficient_checks=coefficient_checks,transformed_binary_edge_cases=len(tests),scope='Exact finite corroboration; universal statements rest on the manuscript proofs'),indent=2))
