#!/usr/bin/env python3
"""Retain one actual invocation of the read-only content preflight."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

E = Path(__file__).resolve().parent
P = E.parents[1]
D = Path(tempfile.mkdtemp(prefix='validation-', dir=E))
verifier = E / 'verify_seal.py'
shutil.copyfile(verifier, D / 'executed-verifier.py')
shutil.copyfile(__file__, D / 'executed-driver.py')
argv = [sys.executable, str(verifier), '--pre-seal']
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
r = subprocess.run(argv, cwd=P, capture_output=True)
(D / 'stdout.log').write_bytes(r.stdout)
(D / 'stderr.log').write_bytes(r.stderr)
(D / 'command.json').write_text(json.dumps({'argv': argv, 'cwd': str(P),
    'started_utc': start, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'exit': r.returncode, 'stdout': 'stdout.log', 'stderr': 'stderr.log',
    'verifier_sha256': hashlib.sha256(verifier.read_bytes()).hexdigest()}, indent=2, sort_keys=True) + '\n')
print(D.name)
print(r.stdout.decode(), end='')
print(r.stderr.decode(), end='', file=sys.stderr)
raise SystemExit(r.returncode)
