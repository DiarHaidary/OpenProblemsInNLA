#!/usr/bin/env python3
"""Capture reused pinned library text by actual read-only Git commands."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

P = Path(__file__).resolve().parents[2]
E = P / 'verification/spectral-window-development/api-sources'
R = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages/mathlib')
PIN = '0df444a360eaa60ab8c11dca51a86af692955474'
paths = ['Mathlib/Analysis/InnerProductSpace/Orthonormal.lean',
    'Mathlib/LinearAlgebra/Dimension/Constructions.lean',
    'Mathlib/LinearAlgebra/Finsupp/LinearCombination.lean',
    'Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean',
    'Mathlib/Data/Matrix/Mul.lean', 'Mathlib/Analysis/InnerProductSpace/Spectrum.lean']
assert not E.exists()
E.mkdir()
env = os.environ.copy()
env['GIT_OPTIONAL_LOCKS'] = '0'
records, commands = [], []
for i, path in enumerate(paths):
    values = []
    for op in ['rev-parse', 'show']:
        argv = ['git', '-c', 'core.fsmonitor=false', op, PIN + ':' + path]
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        result = subprocess.run(argv, cwd=R, env=env, capture_output=True)
        prefix = str(i) + '-' + op
        (E / (prefix + '.stdout')).write_bytes(result.stdout)
        (E / (prefix + '.stderr')).write_bytes(result.stderr)
        commands.append({'argv': argv, 'cwd': str(R), 'GIT_OPTIONAL_LOCKS': '0',
            'started_utc': start, 'exit': result.returncode,
            'stdout': prefix + '.stdout', 'stderr': prefix + '.stderr'})
        (E / 'commands.json').write_text(json.dumps(commands, indent=2, sort_keys=True) + '\n')
        assert result.returncode == 0
        values.append(result.stdout)
    blob, data = values[0].decode().strip(), values[1]
    assert data == (R / path).read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == blob
    records.append({'commit': PIN, 'path': path, 'git_blob': blob,
        'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'snapshot': str(i) + '-show.stdout'})
    (E / 'records.json').write_text(json.dumps(records, indent=2, sort_keys=True) + '\n')
print(json.dumps({'actual_Git_commands': len(commands), 'exact_API_sources': len(records),
    'all_snapshots_equal_clean_pinned_working_sources': True}, indent=2))
