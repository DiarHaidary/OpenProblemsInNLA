from __future__ import annotations
import csv, io, json, math, platform, sys, time, unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from capacity import chebyshev_data, nodal_capacity, first_moment_bound, simulate_coordinate_policy

def main():
    (ROOT/'results').mkdir(exist_ok=True)
    stream=io.StringIO()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    log=stream.getvalue()
    (ROOT/'results'/'unit_tests.txt').write_text(log)
    print(log)
    rng=np.random.default_rng(20260913)
    rows=[]
    # Deliberately mixed easy/hard diagnostic cases, not theorem-constant tests.
    for degree in (1,3,6):
      for width in (2,4):
       for epsilon in (.01,.08):
        k=2; _,e,ell,_=chebyshev_data(degree,epsilon)
        mult=np.full(degree+1,width+5,dtype=int)
        bound=first_moment_bound(width,mult,e,ell,2*epsilon+3*epsilon**2)
        for trial in range(30):
            g0=rng.standard_normal((k,width))
            blocks=[rng.standard_normal((int(m),width)) for m in mult]
            h=nodal_capacity(g0,blocks,e,ell)
            minimum=float(np.linalg.eigvalsh(h).min())
            rows.append(dict(degree=degree,width=width,k=k,epsilon=epsilon,
                trial=trial,lambda_min=minimum,delta=2*epsilon+3*epsilon**2,
                contains_success=int(minimum>=2*epsilon+3*epsilon**2),
                first_moment_upper_bound=bound))
    with (ROOT/'results'/'capacity_trials.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    rotation=[]
    for trial in range(24):
        q,_=np.linalg.qr(rng.normal(size=(24,24)))
        a=q@np.diag(np.linspace(-1,1.2,24))@q.T
        rotation.append(dict(trial=trial,**simulate_coordinate_policy(a,6,trial+170)))
    with (ROOT/'results'/'rotation_checks.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rotation[0]));writer.writeheader();writer.writerows(rotation)
    summary=dict(status='PASS' if result.wasSuccessful() else 'FAIL',
        tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),
        skipped=len(result.skipped),capacity_trials=len(rows),
        contains_success=sum(row['contains_success'] for row in rows),
        does_not_contain_success=sum(1-row['contains_success'] for row in rows),
        rotation_checks=len(rotation),max_transcript_error=max(r['transcript_error'] for r in rotation),
        max_span_error=max(r['span_error'] for r in rotation),
        python=platform.python_version(),numpy=np.__version__,
        prior_suites_rerun=False,
        limitation='Component and floating-point diagnostics only; no universal probability or adaptive lower-bound proof is certified by these tests.')
    (ROOT/'results'/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__': raise SystemExit(main())
