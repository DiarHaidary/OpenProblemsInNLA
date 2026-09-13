#!/usr/bin/env python3
"""Record actual read-only Git identities for preserved originals and reused APIs."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

P = Path(__file__).resolve().parents[2]
E = P / 'verification/spectral-development/source-bindings'
C = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
R = Path('/tmp/nla-lean-ra20-worktree')
assert not E.exists(), 'This source capture is immutable; do not overwrite it.'
E.mkdir()
env = os.environ.copy()
env['GIT_OPTIONAL_LOCKS'] = '0'
commands = []
records = []

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write(name, data):
    (E / name).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')

def run(repo, args, name):
    argv = ['git', '-c', 'core.fsmonitor=false', *args]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(argv, cwd=repo, env=env, capture_output=True)
    (E / (name + '.stdout')).write_bytes(r.stdout)
    (E / (name + '.stderr')).write_bytes(r.stderr)
    commands.append({'argv': argv, 'cwd': str(repo), 'GIT_OPTIONAL_LOCKS': '0',
                     'started_utc': start, 'exit': r.returncode,
                     'stdout': name + '.stdout', 'stderr': name + '.stderr'})
    write('commands.json', commands)
    assert r.returncode == 0, name
    return r.stdout

def bind(repo, commit, upstream, expected, kind, local):
    n = str(len(records)).zfill(2)
    ref = commit + ':' + upstream
    blob = run(repo, ['rev-parse', ref], n + '-blob').decode().strip()
    data = run(repo, ['show', ref], n + '-source')
    actual_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert blob == actual_blob
    assert sha(data) == expected
    assert local.read_bytes() == data
    records.append({'kind': kind, 'repo': str(repo), 'commit': commit,
                    'upstream_path': upstream, 'git_blob': blob, 'sha256': expected,
                    'bytes': len(data), 'local_file': str(local),
                    'snapshot': n + '-source.stdout'})
    write('records.json', records)

originals = json.loads((P / 'verification/original-source-inventory.json').read_text())
assert originals['source_count'] == len(originals['files']) == 17
for local, d in originals['files'].items():
    bind(R, d['commit'], d['upstream_path'], d['sha256'], 'original', P / local)

api = {
    'mathlib': [
        'Mathlib/Analysis/InnerProductSpace/Spectrum.lean',
        'Mathlib/Analysis/InnerProductSpace/Positive.lean',
        'Mathlib/Analysis/InnerProductSpace/PiL2.lean',
        'Mathlib/Analysis/Matrix/Spectrum.lean',
        'Mathlib/Analysis/Matrix/Order.lean',
        'Mathlib/Analysis/Normed/Lp/Matrix.lean',
        'Mathlib/LinearAlgebra/Charpoly/ToMatrix.lean',
        'Mathlib/LinearAlgebra/Matrix/PosDef.lean',
        'Mathlib/Algebra/Polynomial/Degree/Domain.lean',
        'Mathlib/Algebra/Polynomial/AlgebraMap.lean',
        'Mathlib/Data/Fintype/Basic.lean',
        'Mathlib/Tactic/Module.lean'],
    'leancert': ['LeanCert/Tactic/Verification.lean']}
pins = {d['name']: d['rev'] for d in json.loads((P / 'lake-manifest.json').read_text())['packages']}
for package, paths in api.items():
    for path in paths:
        local = C / package / path
        bind(C / package, pins[package], path, sha(local.read_bytes()), 'reused API', local)

current = (P / 'verification/original-sources/eigenvalues-and-inverse-problems/KE-04/solution.md').read_text()
original = (P / 'verification/original-submission/solution.md').read_text()
def block(s):
    return s[s.index('## Theorem '):s.index('## Scope and review notes')].strip().encode()
assert block(current) == block(original)
assert sha(block(current)) == '3ba1bd9a62a00aaf787758af6312e4787ca8d6db02b4487e8b956ce0553977a7'
result = {'originals': 17, 'reused_API_sources': 13, 'actual_Git_commands': len(commands),
          'all_snapshots_match_local_source_and_exact_Git_blob': True,
          'original_full_proof_block_unchanged': True, 'proof_block_bytes': len(block(current)),
          'proof_block_sha256': sha(block(current))}
write('result.json', result)
print(json.dumps(result, indent=2))
