#!/usr/bin/env python3
"""Run every rigorous certificate. No exploratory solver is required."""
from pathlib import Path
import subprocess,sys,json,platform
ROOT=Path(__file__).resolve().parents[1]
if not __debug__:raise RuntimeError('Run without -O')
records=[]
for name in ['derive_algebra.py','check_intervals.py','verify_local.py','rational_witness.py','global_model.py','verify_layer_hull.py']:
    r=subprocess.run([sys.executable,str(ROOT/'src'/name)],capture_output=True,text=True,check=True)
    print(r.stdout,end='');records.append(dict(script=name,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
(ROOT/'results'/'run_all.json').write_text(json.dumps(dict(python=platform.python_version(),status='PASS',global_solution=False,checks=records),indent=2)+'\n')
print('All rigorous checks pass. This package does not establish the global upper bound.')
