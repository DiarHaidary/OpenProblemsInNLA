import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json
from pathlib import Path
import numpy as np
from fractions import Fraction
ROOT=Path('/private/tmp/nla-review-253-256/pr255'); sys.path.insert(0,str(ROOT/'scratch/sp03/verify'))
from reference import exact_system,check_one
from separation import check_disjoint
rows=[]
for m in range(1,5):
 z=np.load(ROOT/f'scratch/sp03/certificates/rank{m}.npz',allow_pickle=False);u=z['U'].ravel()
 for i in np.unique(np.linspace(0,len(z['roots'])-1,min(16,len(z['roots'])),dtype=int)):
  x=z['roots'][i];_,_,ar,ai,e=exact_system(x,u,2*m);h=(np.asarray(ar,dtype=float)+1j*np.asarray(ai,dtype=float))*2.**-e;b=np.linalg.inv(h)
  if not check_one(x,u,b,2*m)[0]:raise RuntimeError('Valid failed')
  bad=x.copy();bad[0]+=16*(1+max(abs(x)))
  if check_one(bad,u,b,2*m)[0]:raise RuntimeError('Perturbed center accepted')
  if check_one(x,u,b*0,2*m)[0]:raise RuntimeError('Zero inverse accepted')
  if check_one(x,u,-b,2*m)[0]:raise RuntimeError('Negated inverse accepted')
  rows.append({'rank':m,'center':int(i),'valid':True,'large_center_corruption_rejected':True,'zero_inverse_rejected':True,'negative_inverse_rejected':True})
cases=[('duplicate',[[0j],[0j]],[-30,-30],False),('touching',[[0j],[.25+0j]],[-3,-3],False),('above_touching',[[0j],[np.nextafter(.25,1)+0j]],[-3,-3],True),('imaginary',[[0j],[1j]],[-3,-3],True)]
for label,arr,re,expected in cases:
 if check_disjoint(np.array(arr,dtype=complex),re)['distinct']!=expected:raise RuntimeError(label)
# Verify that the full set has disjoint first-coordinate intervals independently of the sweep implementation.
separations=[]
for m in range(1,5):
 z=np.load(ROOT/f'scratch/sp03/certificates/rank{m}.npz',allow_pickle=False);report=json.loads((ROOT/f'sp03-rank{m}-full.json').read_text())
 spans=[]
 for x,re in zip(z['roots'],report['radius_exponents']):
  c=Fraction(float(x[0].real));r=Fraction(2)**re;spans.append((c-r,c+r))
 spans.sort()
 if any(spans[i][1]>=spans[i+1][0] for i in range(len(spans)-1)):raise RuntimeError('Independent separation failed')
 separations.append({'rank':m,'balls':len(spans),'adjacent_exact_interval_checks':len(spans)-1,'distinct':True})
result={'result':'PASS','centers':rows,'corruption_checks':len(rows)*3,'separation_boundary_cases':4,'independent_full_first_coordinate_separation':separations}
(ROOT/'sp03-controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='centers'},indent=2))
