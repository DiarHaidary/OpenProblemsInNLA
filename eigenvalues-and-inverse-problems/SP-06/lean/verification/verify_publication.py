"""Offline source, receipt and archive checks for the SP-06 publication.

This verifies retained evidence and current correspondence; it does not run
Lean or replace the independent informal mathematical reviews.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
project = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(project / 'verification/verify_package.py')], check=True)
audit = project / 'verification/linux-2026-09-13/independent-audit'
manifest = json.loads((audit / 'EVIDENCE-MANIFEST.json').read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for name, record in manifest['files'].items():
    assert digest(audit / name) == record['sha256'], name
    assert (audit / name).stat().st_size == record['bytes'], name
for line in (audit / 'MANIFEST.sha256').read_text().splitlines():
    expected, name = line.split('  ', 1)
    assert digest(audit / name) == expected, name
assert digest(audit / 'OPERATIONAL-REVIEW.md') == '8be74df4c72817a96377c3b68d89a4fce78aaa298304470f64df88fa1ebf9d5c'
archive = audit / 'lean-SP-06-artifact.zip'
assert digest(archive) == 'fac2ebe5f81ec421a7b478fcbd1a11768887b8678ad5d166adac3a1402aece6c'
with zipfile.ZipFile(archive) as bundle:
    assert len(bundle.infolist()) == 13
    for info in bundle.infolist():
        path = Path(info.filename)
        assert not path.is_absolute() and '..' not in path.parts
        assert bundle.read(info) == (audit / 'extracted' / path).read_bytes(), path

result = json.loads((audit / manifest['result_summary']['path']).read_text())
commit = '3122d69460b0ed6dda3ea00dfaa899f93411ce2f'
assert result['repository_commit'] == commit
assert result['result'] == 'comparator-accepted'
config = json.loads((project / 'comparator.json').read_text())
assert result['config'] == config
assert not config['definition_names'] and len(config['theorem_names']) == 20
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
assert set(config['permitted_axioms']) == allowed
mapping = json.loads((project / 'verification/candidate-metadata-map.json').read_text())
assert mapping['verified_commit'] == commit
assert set(mapping['mapping']) == {'README.md', 'formalization.yaml', 'verification/package-inputs.json'}
assert len(result['input_sha256']) == 61
for name, expected in result['input_sha256'].items():
    actual = project / mapping['mapping'].get(name, name)
    assert digest(actual) == expected, name
assert digest(project.parents[2] / 'tools/lean/source-lock.json') == result['source_lock_sha256']
run = json.loads((audit / 'run-api.json').read_text())
job = json.loads((audit / 'verify-job-api.json').read_text())
for record in (run, job):
    assert record['head_sha'] == commit and record['status'] == 'completed' and record['conclusion'] == 'success'
assert job['id'] == 103745998196 and run['id'] == 34765629739
logs = audit / 'extracted/verify-20260913T152822Z-3952'
required = {
    'comparator.log': ['Building Challenge', 'Building Solution', 'Lean default kernel accepts the solution', 'Your solution is okay!', 'EXIT_STATUS=0'],
    'sandbox.log': ['Sandbox UID: 1001', 'PASS AF_UNIX socket creation', 'PASS nested namespace write attempt', 'Outer and export fixture contents unchanged', 'EXIT_STATUS=0'],
    'kernel-controls.log': ['PASS: all three actual Comparator.runBuiltinKernel cases behaved as required', 'EXIT_STATUS=0'],
    'comparator-controls.log': ['PASS: all five Comparator regressions', 'EXIT_STATUS=0'],
    'negative-sorry.log': ["Illegal axiom detected: 'sorryAx'", 'EXIT_STATUS=1'],
    'negative-native.log': ["Illegal axiom detected: 'checked._native.native_decide.ax_1_1'", 'EXIT_STATUS=1'],
}
for name, needles in required.items():
    raw = (logs / name).read_text()
    for needle in needles:
        assert needle in raw, (name, needle)
exports = [line for line in (logs / 'comparator.log').read_text().splitlines() if line.startswith('Exporting #[') and line.endswith(' from Solution')]
assert len(exports) == 1
for theorem in config['theorem_names']:
    assert theorem in exports[0]
axioms = dict(re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", (project / 'verification/local-2026-09-13/types-axioms.log').read_text()))
for theorem in config['theorem_names']:
    assert theorem in axioms and set(axioms[theorem].split(', ')) <= allowed
print('SP-06 publication integrity: PASS; 61 original inputs, 20 exports, original ZIP and successful Linux receipts')
