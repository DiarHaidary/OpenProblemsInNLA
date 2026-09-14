import sympy as s,itertools,json,sys
from pathlib import Path
p,y,z,a,w=s.symbols('p y z a w');n=p+y+z;d=1-a
K=s.Matrix([[1,1,a],[1,a,1],[a,1,a]])*s.diag(p,y,z)
f=K.charpoly(w).as_expr();t=p+a*(y+z)
e2=-d*p*(y+z)+d*(1+a)*z*(p-y)
e3=-(1+a)*d*d*p*y*z
assert s.expand(f-(w**3-t*w*w+e2*w-e3))==0
B=s.Matrix([[a*z,n-z],[z,n-z]])
assert s.expand(s.trace(B)**2-4*B.det()-(n*n+d*(2*n*z-(a+3)*z*z)))==0
count=0
for entries in itertools.product([-1,1],repeat=9):
 T=s.Matrix(3,3,entries)
 if T.det():
  assert s.expand((T.T*T).charpoly(w).as_expr()-(w-4)**2*(w-1))==0
  count+=1
# Check the positivity charts actually use nonnegative polynomial exponents in squares.
root=Path(sys.argv[1])/'checks';nsq=0
for kind in ['B','Q']:
 cert=json.loads((root/f'typeA_minus_{kind}_certificate.json').read_text())
 for term in cert['squares']:
  al,be=term['alpha'],term['beta']
  assert all((x-min(x,y))%2==0 and (y-min(x,y))%2==0 for x,y in zip(al,be));nsq+=1
out={'status':'PASS','independent_typeA_characteristic_polynomial':True,'independent_candidate_spread_formula':True,'all_3_by_3_sign_matrices_examined':512,'nonsingular_sign_matrices_with_singular_values_2_2_1':count,'squares_with_integral_half_exponents':nsq}
Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
