"""Exact conservative ball-selection tests; no claim about roots."""
from pathlib import Path
import json
import numpy as np
from separation import select_disjoint,check_disjoint
BASE=Path(__file__).resolve().parents[1]
# The tentative nonmandatory ball is processed first, then must be revoked.
x=np.array([[1+0j],[0j]],dtype=complex);r=np.array([-2,1])
keep,rejected=select_disjoint(x,r,mandatory_count=1)
assert keep==[0] and rejected==[[1,0]]
# Overlap in the first real coordinate does not preclude exact separation.
x=np.array([[0j],[1j]],dtype=complex);r=np.array([-3,-3])
keep,_=select_disjoint(x,r);assert keep==[0,1]
# Touching closed balls are conservatively rejected.
x=np.array([[0j],[.25+0j]],dtype=complex);r=np.array([-3,-3])
keep,_=select_disjoint(x,r);assert len(keep)==1
# Random trials with an exactly disjoint mandatory prefix and duplicate copies.
rng=np.random.default_rng(991204)
for trial in range(100):
    prior=(rng.normal(size=(12,5))+1j*rng.normal(size=(12,5))).astype(complex)
    more=np.concatenate([prior+2**-45,(rng.normal(size=(25,5))+1j*rng.normal(size=(25,5)))])
    x=np.concatenate([prior,more]);r=np.full(len(x),-20,dtype=np.int64)
    assert check_disjoint(prior,r[:12])['distinct']
    keep,rejected=select_disjoint(x,r,mandatory_count=12)
    assert set(range(12)).issubset(keep)
    assert check_disjoint(x[keep],r[keep])['distinct']
report={'all_checks_passed':True,'random_trials':100,'mandatory_prefix_preserved':True,
        'late_mandatory_revocation_test_passed':True,'closed_ball_touching_test_passed':True}
(BASE/'results'/'selection_checks.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
