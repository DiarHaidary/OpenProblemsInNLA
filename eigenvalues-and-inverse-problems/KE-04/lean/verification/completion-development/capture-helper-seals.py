#!/usr/bin/env python3
"""Bind completed imported helper seals and retain their actual read-only checks."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

P = Path(__file__).resolve().parents[2]
E = P / 'verification/completion-development/imported-helper-checks'
assert not E.exists()
E.mkdir()
seals = {
    'verification/spectral-window-development/EVIDENCE-MANIFEST.json': '2fecf0e58267ebab396ccc9a4691fb1e41a751fe6e23e98c89a2842af01a269c',
    'verification/transport-intersection-handoff/EVIDENCE-MANIFEST.json': 'b3232d8adb072dc44447a2a1f6f806f709bc55b4201b85d680d557645d9d72e8',
    'verification/nonannihilation-development/EVIDENCE-MANIFEST.json': 'd57bb205a29e51eefa1e1d67f662f052875a58961c750f6930028408251def68'}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(name, value):
    (E / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def binding():
    files = {}
    memberships = {}
    for seal, expected in seals.items():
        assert sha(P / seal) == expected
        d = json.loads((P / seal).read_text())
        assert d['exact_self_exclusion'] == seal
        files[seal] = expected
        memberships[seal] = len(d['files'])
        for r, v in d['files'].items():
            assert sha(P / r) == v['sha256'] and (P / r).stat().st_size == v['bytes'], r
            if r in files:
                assert files[r] == v['sha256'], r
            files[r] = v['sha256']
    return {'seals': seals, 'memberships': memberships, 'files': files, 'file_count': len(files)}

before = binding()
write('before.json', before)
entries = [
    ('verification/spectral-window-development/verify_seal.py', []),
    ('verification/transport-intersection-handoff/verify_seal.py', []),
    ('verification/nonannihilation-development/seal.py', ['--verify'])]
commands = []
for i, (r, args) in enumerate(entries):
    verifier = P / r
    (E / ('executed-verifier-' + str(i) + '.py')).write_bytes(verifier.read_bytes())
    argv = [sys.executable, str(verifier), *args]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(argv, cwd=P, capture_output=True)
    (E / (str(i) + '.stdout')).write_bytes(result.stdout)
    (E / (str(i) + '.stderr')).write_bytes(result.stderr)
    commands.append({'argv': argv, 'cwd': str(P), 'started_utc': start,
        'exit': result.returncode, 'stdout': str(i) + '.stdout', 'stderr': str(i) + '.stderr',
        'executed_verifier_sha256': sha(verifier), 'read_only_branch': True})
    write('commands.json', commands)
    assert result.returncode == 0 and not result.stderr
after = binding()
write('after.json', after)
assert before == after
summary = {'all_three_actual_read_only_checks_pass': True, 'source_or_prior_evidence_writes': False,
    'preserved_imported_union': before['file_count'], 'complete_memberships': before['memberships']}
write('result.json', summary)
print(json.dumps(summary, indent=2))
