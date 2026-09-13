from pathlib import Path
import json
from fractions import Fraction as Q
from itertools import product
root=Path(__file__).resolve().parents[1]/'submitted'
d=json.loads((root/'IE11_recovery/data/rational_witness.json').read_text())
a=[[Q(int(v),int(d['denominator'])) for v in row] for row in d['numerators']]
assert max(abs(v) for row in a for v in row)==1
pivots=[]; comparisons=0
for k in range(5):
 p=a[0][0]; assert p>0; pivots.append(p)
 for i in range(len(a)):
  for j in range(len(a)):
   if (i,j)!=(0,0):
    assert p>a[i][j] and p>-a[i][j]; comparisons+=2
 a=[[a[i][j]-a[i][0]*a[0][j]/p for j in range(1,len(a))] for i in range(1,len(a))]
assert comparisons==100
assert pivots[-1]>Q(d['strict_lower_bound'])
assert pivots[-1]>max(pivots[:-1])
print('Independent IE11 exact elimination: 100 strict inequalities and lower bound PASS')
for p in range(2,10):
 u=Q(1,2**p); errors=[]
 for signs in product((-1,1),repeat=9):
  factors=[1+s*u for s in signs]; F=Q(1)
  for factor in factors[:5]: F*=factor
  for factor in factors[5:]: F/=factor
  errors.append(abs(1-F)/(1+F))
 worst=((1+u)**4-(1-u)**5)/((1+u)**4+(1-u)**5)
 assert max(errors)==worst
print('Independent IE20 scalar product-ratio check: 4096 corners PASS')
for a in (Q(1),Q(1,2),Q(1,16),Q(1,1024)):
 for t in (a,(a+1)/2,(1+3*a)/(3+a),Q(1)):
  lhs=(1-a)**2/(8*(1+a))-(1-t)*(t-a)/(1+t)**2
  rhs=((a+3)*t-(3*a+1))**2/(8*(1+a)*(1+t)**2)
  assert lhs==rhs and lhs>=0
print('Independent IE20 first-step identity: 16 rational substitutions PASS')
