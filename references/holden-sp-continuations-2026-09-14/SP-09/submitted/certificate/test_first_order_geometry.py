"""Reject corrupted witnesses and a changed reference matrix, including under -O."""
from __future__ import annotations
import argparse
from copy import deepcopy
from fractions import Fraction
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import first_order_geometry as geom


def check(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def run() -> dict:
    script=Path(__file__).with_name('first_order_geometry.py')
    expected=geom.calculate()
    stored=json.loads(script.with_name('first_order_witness.json').read_text())
    check(expected==stored,'Unmodified witness failed exact recomputation.')
    rows=[]
    mutations=[
        ('changed_A_coefficient',lambda x:x['A_coefficients'][0].__setitem__(0,'154/364')),
        ('nonzero_third_coefficient',lambda x:x['A_coefficients'][2].__setitem__(0,'1')),
        ('wrong_B_sign',lambda x:x['B_coefficients_before_subtraction'][1].__setitem__(0,'-225/364')),
        ('missing_Schur_correction',lambda x:x.__setitem__('flat_schur_curvature',['19/2080','0'])),
        ('negative_curvature',lambda x:x.__setitem__('flat_schur_curvature',['-1/52','0'])),
        ('rank_one_density',lambda x:x.__setitem__('rho_positive_eigenvalues',['1','0'])),
        ('wrong_gauge_rank',lambda x:x.__setitem__('gauge_rank',6)),
        ('wrong_transverse_basis',lambda x:x.__setitem__('transverse_direction_indices_zero_based',[0,1,2])),
    ]
    with tempfile.TemporaryDirectory(prefix='sp09_first_order_tests_') as temp:
        for name,change in mutations:
            bad=deepcopy(expected);change(bad)
            path=Path(temp)/(name+'.json');path.write_text(json.dumps(bad))
            env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
            proc=subprocess.run([sys.executable,'-O',str(script),'--witness',str(path)],
                                capture_output=True,text=True,env=env)
            check(proc.returncode!=0,f'Corruption accepted: {name}')
            check('stored witness differs' in proc.stderr,f'Unexpected failure for {name}: {proc.stderr}')
            rows.append({'corruption':name,'rejected':True})
    original_model=geom.model
    def bad_model():
        result=original_model()
        result['D'][0][0,0]+=Fraction(1,100)
        return result
    try:
        geom.model=bad_model
        try:
            geom.calculate()
        except ValueError as exc:
            check('spectral identity' in str(exc),'Changed model failed for an unexpected reason.')
            rows.append({'corruption':'changed_reference_residual','rejected':True})
        else:
            raise ValueError('A changed reference residual was accepted.')
    finally:
        geom.model=original_model
    return {'result':'PASS','unmodified_witness':'PASS','negative_tests':rows,
            'scope':'Exact finite-identity and data-integrity regression tests, not formalization of the analytic proof.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path);args=parser.parse_args()
    result=run()
    if args.report:args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
