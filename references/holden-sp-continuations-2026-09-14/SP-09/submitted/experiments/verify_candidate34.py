"""Audit stored feasible witnesses. This does not certify a base lower bound."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np


def check(ok: bool, message: str) -> None:
    if not ok:raise ValueError(message)


def run() -> dict:
    root=Path(__file__).with_name('candidate34')
    desc=json.loads((root/'initial.json').read_text())
    with np.load(root/'base.npz',allow_pickle=False) as z:
        a,b,U=(z[x] for x in ['a','b','U'])
    with np.load(root/'amplified.npz',allow_pickle=False) as z:
        aa,bb,V=(z[x] for x in ['a','b','U'])
    n=len(a);check(n==7 and b.shape==a.shape,'Incorrect base spectra.')
    check(np.array_equal(a,aa) and np.array_equal(b,bb),'Saved spectra disagree.')
    check(U.shape==(n,n) and V.shape==(2*n,2*n),'Incorrect unitary dimensions.')
    check(np.all(np.isfinite(a)) and np.all(np.isfinite(b)),'Nonfinite spectra.')
    defect_u=float(np.linalg.norm(U.conj().T@U-np.eye(n),2))
    defect_v=float(np.linalg.norm(V.conj().T@V-np.eye(2*n),2))
    check(defect_u<1e-10 and defect_v<1e-10,'Unitarity tolerance failed.')
    base=float(np.linalg.norm((a[:,None]-b[None,:])*U,2))
    ampl=float(np.linalg.norm((np.repeat(a,2)[:,None]-np.repeat(b,2)[None,:])*V,2))
    check(abs(base-desc['base_upper'])<1e-10,'Base objective mismatch.')
    check(abs(ampl-desc['amplified_upper'])<1e-10,'Amplified objective mismatch.')
    check(abs((base-ampl)-desc['candidate_gap'])<1e-10,'Gap mismatch.')
    tensor_defect=float(np.linalg.norm(V-np.kron(U,np.eye(2)),2))
    return {'result':'PASS: numerical feasibility audit','n':n,'k':2,
            'base_feasible_norm':base,'amplified_feasible_norm':ampl,
            'base_unitarity_defect':defect_u,'amplified_unitarity_defect':defect_v,
            'distance_from_repeated_base_witness':tensor_defect,
            'scope':'Both objective values are feasible upper bounds. No lower bound or counterexample is certified.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path);args=p.parse_args()
    result=run()
    if args.report:args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
