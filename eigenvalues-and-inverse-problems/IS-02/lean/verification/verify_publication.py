"""Offline source, receipt and archive checks for the IS-02 publication.

Checks retained evidence and source correspondence; does not run Lean or
replace the independent mathematical reviews. Use a full repository checkout
with tools/lean/requirements.txt installed.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
project = Path(__file__).resolve().parents[1]
repository = project.parents[2]
subprocess.run([sys.executable, str(project / 'verification/verify_package.py')], check=True)
audit = project / 'verification/linux-2026-09-13/independent-audit'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = json.loads((audit / 'EVIDENCE-MANIFEST.json').read_text())
for name, expected in manifest['files'].items():
    path = Path(name)
    assert not path.is_absolute() and '..' not in path.parts, name
    assert digest(audit / path) == expected, name
assert digest(audit / 'OPERATIONAL-REVIEW.md') == 'a8671227d0d033713789831218f73e4002c288d64903fcb703bd8853ee74fe14'
assert digest(audit / 'check_evidence.py') == '495d30f09b0984358d9731c0fd1b0783d5427fae7063d412b0063d4f92ef847d'
subprocess.run([sys.executable, str(audit / 'check_evidence.py')], check=True)

result = json.loads((audit / 'extracted/verify-20260913T153914Z-4215/result.json').read_text())
commit = '522f091b9f0d39d4846f5939bcafc1549ba16a55'
assert result['repository_commit'] == commit and result['result'] == 'comparator-accepted'
config = json.loads((project / 'comparator.json').read_text())
assert config == result['config']
assert len(config['theorem_names']) == 9 and config['definition_names'] == []
assert set(config['permitted_axioms']) == {'propext', 'Classical.choice', 'Quot.sound'}
mapping = json.loads((project / 'verification/candidate-metadata-map.json').read_text())
assert mapping['verified_commit'] == commit
assert set(mapping['mapping']) == {'README.md', 'formalization.yaml', 'verification/package-inputs.json'}
assert len(result['input_sha256']) == 119
for name, expected in result['input_sha256'].items():
    relative = Path(mapping['mapping'].get(name, name))
    assert not relative.is_absolute() and '..' not in relative.parts, name
    assert digest(project / relative) == expected, name
assert digest(repository / 'tools/lean/source-lock.json') == result['source_lock_sha256']
print('IS-02 publication integrity: PASS; 119 original inputs, 9 exports, original ZIP and successful Linux receipts')
