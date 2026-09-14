"""Independent arithmetic comparisons, adversarial tests, and exact Euler sums."""
from pathlib import Path
import os,sys,json,time
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
import sympy as sp
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from polynomial import evaluate
from backend import check
from reference import check_one
from quad_proposal import refine_quad
from separation import check_disjoint
rng=np.random.default_rng(69792);results=[];start=time.perf_counter()
z=np.load(BASE/'verify'/'fixtures'/'pilot_m4.npz');u=z['U']
indices=list(rng.choice(len(z['roots']),12,False))
for i in indices:
    x=z['roots'][i].copy()
    for kind in ['stored','quad_refined','perturbed','zero_inverse']:
        y=refine_quad(x,u,3) if kind=='quad_refined' else x.copy()
        if kind=='perturbed':y[0]+=2
        _,H=evaluate(x,u,8);B=np.linalg.inv(H)
        if kind=='zero_inverse':B*=0
        yes,re,info=check(y,u,B);ok,r,a,b,c=check_one(y,u,B,8)
        assert yes==ok,(i,kind)
        assert float(r)==2.**re
        assert np.allclose(info[:3],[float(a),float(b),float(c)],rtol=1e-14,atol=0)
        if kind in ['stored','quad_refined']:assert yes
        if kind=='zero_inverse':assert not yes
        results.append({'root_index':int(i),'case':kind,'exact_backend_agrees_with_reference':True,'accepted':yes})
# Explicit equality/overlap, first-coordinate separation, and other-coordinate separation.
a=np.asarray([[0j,0j],[1j,0j]],dtype=complex)
assert check_disjoint(a,[-3,-3])['distinct']
assert not check_disjoint(np.asarray([[0j],[0j]]),[-30,-30])['distinct']
assert not check_disjoint(np.asarray([[0j],[.25+0j]]),[-3,-3])['distinct'] # touching closed balls
assert check_disjoint(np.asarray([[0j],[.25000000000000006+0j]]),[-3,-3])['distinct']
# Independent enumeration of the two Stirling-number formulas for chi(Omega_m).
from sympy.functions.combinatorial.numbers import stirling
chi=[]
for m in range(0,13):
    lhs=sum(stirling(m+1,r+1,kind=2)*(-2)**r*sp.factorial(r) for r in range(m+1))
    rhs=(-1)**m*sum(stirling(m,r,kind=2)*sp.factorial(r) for r in range(m+1))
    assert lhs==rhs
    chi.append({'rank':m,'compactly_supported_euler_characteristic':int(lhs)})
report={'all_checks_passed':True,'backend_comparisons':results,'separation_adversarial_tests_passed':True,
        'euler_identity_checks':chi,'seconds':time.perf_counter()-start}
(BASE/'results'/'expanded_exact_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='backend_comparisons'},indent=2))
