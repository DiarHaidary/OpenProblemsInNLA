"""Offline IE-16 publication integrity: no Lean/Lake or network execution.

Requires a full repository checkout and the shared metadata requirements.
This checker binds records to the accepted canonical revision; it does not
replace the independent mathematical/semantic referee decisions.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[2]
COMMIT = '697a2a1d88337a6747aa5c82fb6e554d3ff1b356'
RAW = PROJECT / 'verification/linux-2026-09-13/operational-record'
LOGS = RAW / 'extracted/verify-20260913T182805Z-4150'
AXIOMS = ['propext', 'Classical.choice', 'Quot.sound']

def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out: raise ValueError(f'Duplicate JSON key: {key}')
        out[key] = value
    return out

def read(path): return json.loads(path.read_text(), object_pairs_hook=unique)
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def local(root, name):
    rel = PurePosixPath(name)
    assert not rel.is_absolute() and '..' not in rel.parts and str(rel) == name
    path = root.joinpath(*rel.parts)
    assert not path.is_symlink() and path.is_file()
    return path

inventory = read(PROJECT / 'verification/package-inputs.json')
assert inventory['verified_commit'] == COMMIT
for name, expected in inventory['sha256'].items():
    assert digest(local(PROJECT, name)) == expected, name
present = {str(p.relative_to(PROJECT)) for p in PROJECT.rglob('*')
           if p.is_file() and '.lake' not in p.relative_to(PROJECT).parts
           and '__pycache__' not in p.relative_to(PROJECT).parts
           and str(p.relative_to(PROJECT)) != 'verification/package-inputs.json'}
assert present == set(inventory['sha256']), 'Incomplete publication inventory'

result = read(LOGS / 'result.json')
assert result['repository_commit'] == COMMIT
assert result['project'] == 'linear-systems-and-elimination/IE-16/lean'
assert result['result'] == 'comparator-accepted'
assert digest(LOGS / 'result.json') == '3fa4b80021abb07a0df3921d33e1bd3c16d07df732578453bf312250f06fc9dd'
assert len(result['input_sha256']) == 281
config = read(PROJECT / 'comparator.json')
assert config == result['config'] and config['definition_names'] == []
assert config['permitted_axioms'] == AXIOMS and len(config['theorem_names']) == 15
mapping = read(PROJECT / 'verification/candidate-metadata-map.json')
assert mapping == {'verified_commit': COMMIT, 'mapping': {
    'README.md': 'verification/candidate-metadata/README.md',
    'formalization.yaml': 'verification/candidate-metadata/formalization.yaml'}}
for name, expected in result['input_sha256'].items():
    assert digest(local(PROJECT, mapping['mapping'].get(name, name))) == expected, name
assert digest(REPO / 'tools/lean/source-lock.json') == result['source_lock_sha256']

run = read(RAW / 'run-final.json')
assert run['id'] == 34774629327 and run['head_sha'] == COMMIT
assert run['status'] == 'completed' and run['conclusion'] == 'success'
verify_jobs = [j for j in read(RAW / 'jobs-final.json')['jobs'] if j['name'].startswith('verify (')]
assert len(verify_jobs) == 1
assert verify_jobs[0]['id'] == 103770408910 and verify_jobs[0]['conclusion'] == 'success'
artifacts = read(RAW / 'artifacts-final.json')['artifacts']
assert len(artifacts) == 1 and artifacts[0]['id'] == 10322764134
assert artifacts[0]['name'] == 'lean-IE-16'
zip_digest = digest(RAW / 'artifact.zip')
assert zip_digest == '1e1662ad25d3ea724277a840f9c4579c034cae08c9f6fce76bc08cd48795eefd'
assert artifacts[0]['digest'] == 'sha256:' + zip_digest
with zipfile.ZipFile(RAW / 'artifact.zip') as archive:
    for member in archive.infolist():
        if member.is_dir(): continue
        assert local(RAW / 'extracted', member.filename).read_bytes() == archive.read(member)

log = (LOGS / 'comparator.log').read_text()
assert digest(LOGS / 'comparator.log') == 'f226bbdaf0c47e4dff3127d1711b00819ccf0e7d275b320521191e2fc0087d9f'
closures = re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", log)
assert [name for name, _ in closures] == config['theorem_names']
assert all(items.split(', ') == AXIOMS for _, items in closures)
assert 'Lean default kernel accepts the solution\nYour solution is okay!' in log
assert log.endswith('EXIT_STATUS=0\n')

acceptance = read(PROJECT / 'reviews/FINAL-ACCEPTANCE.json')
assert acceptance['verified_commit'] == COMMIT
assert acceptance['final_canonical_ci_accepted'] is True
for name, expected in acceptance['boundary_files'].items():
    assert digest(local(PROJECT, name)) == expected, name
assert len(acceptance['reports']) >= 2
for name, expected in acceptance['reports'].items():
    assert digest(local(PROJECT / 'reviews', name)) == expected, name

subprocess.run([sys.executable, str(REPO / 'tools/lean/validate_manifest.py'),
                str(PROJECT)], check=True)
print('IE-16 publication integrity PASS: 281 original inputs, 15 exports, '
      'immutable ZIP/raw receipts, standard axioms and final review hashes')
