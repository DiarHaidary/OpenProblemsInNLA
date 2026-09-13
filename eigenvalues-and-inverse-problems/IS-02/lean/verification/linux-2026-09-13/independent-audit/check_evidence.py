"""Offline verification of the retained IS-02 Linux receipts and raw archive."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

root = Path(__file__).resolve().parent
identity = json.loads((root / 'IDENTITY-CHECKS.json').read_text())
logs = root / 'extracted/verify-20260913T153914Z-4215'
result = json.loads((logs / 'result.json').read_text())
commit = '522f091b9f0d39d4846f5939bcafc1549ba16a55'
assert result['repository_commit'] == commit and result['result'] == 'comparator-accepted'
assert len(result['input_sha256']) == 119
assert result['input_sha256'] == identity['input_sha256']
config = result['config']
assert len(config['theorem_names']) == 9 and config['definition_names'] == []
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
assert set(config['permitted_axioms']) == allowed
run = json.loads((root / 'run-api.json').read_text())
job = json.loads((root / 'verify-job-api.json').read_text())
for record in (run, job):
    assert record['head_sha'] == commit and record['status'] == 'completed' and record['conclusion'] == 'success'
assert run['id'] == 34766178560 and job['id'] == 103747466088
artifact = json.loads((root / 'artifacts.json').read_text())['artifacts'][0]
archive = root / 'lean-IS-02-artifact.zip'
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
assert digest == '27171071d0a2087eaa63cfac39d95529f7037e7c007084852b01fae72d2afeca'
assert artifact['id'] == 10320941744 and artifact['name'] == 'lean-IS-02'
assert artifact['digest'] == 'sha256:' + digest and not artifact['expired']
with zipfile.ZipFile(archive) as bundle:
    assert len(bundle.infolist()) == 13
    for entry in bundle.infolist():
        path = Path(entry.filename)
        assert not path.is_absolute() and '..' not in path.parts
        assert bundle.read(entry) == (root / 'extracted' / path).read_bytes()
needed = {
    'comparator.log': ['Building Challenge', 'Building Solution', 'Lean default kernel accepts the solution', 'Your solution is okay!', 'EXIT_STATUS=0'],
    'sandbox.log': ['Sandbox UID: 1001', 'PASS AF_UNIX socket creation', 'PASS effective capabilities: none', 'PASS no_new_privs: set', 'PASS nested namespace write attempt', 'Outer and export fixture contents unchanged', 'EXIT_STATUS=0'],
    'kernel-controls.log': ['PASS: all three actual Comparator.runBuiltinKernel cases behaved as required', 'EXIT_STATUS=0'],
    'comparator-controls.log': ['PASS: all five Comparator regressions', 'EXIT_STATUS=0'],
    'negative-sorry.log': ["Illegal axiom detected: 'sorryAx'", 'EXIT_STATUS=1'],
    'negative-native.log': ["Illegal axiom detected: 'checked._native.native_decide.ax_1_1'", 'EXIT_STATUS=1'],
}
for filename, needles in needed.items():
    text = (logs / filename).read_text()
    for needle in needles:
        assert needle in text, (filename, needle)
raw = (logs / 'comparator.log').read_text()
axioms = dict(re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", raw))
assert set(axioms) == set(config['theorem_names'])
for name, ax in axioms.items():
    assert set(ax.split(', ')) == allowed, name
export = [line for line in raw.splitlines() if line.startswith('Exporting #[') and line.endswith(' from Solution')]
assert len(export) == 1 and all(name in export[0] for name in config['theorem_names'])
manifest = root / 'EVIDENCE-MANIFEST.json'
if manifest.exists():
    for filename, expected in json.loads(manifest.read_text())['files'].items():
        assert hashlib.sha256((root / filename).read_bytes()).hexdigest() == expected, filename
print('PASS: exact IS-02 run/job and ZIP, 119 recorded input hashes, 9 statements and actual standard3 axiom reports, kernel and rejection controls')
