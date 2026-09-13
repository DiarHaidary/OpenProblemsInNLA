#!/usr/bin/env python3
"""Read-only hash and run-record verifier for REVIEW-ADDENDUM.md."""
import hashlib, json, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/tmp/nla-ie16-development-evidence/run-34773404263/extracted')
project = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('/tmp/nla-ie16-development-worktree')
commit = '281fc3790412b7ab2b05c202c0351b4d259a6382'
source = json.loads((root/'source-hashes.json').read_text())['files']
assert json.loads((root/'source-hashes-after.json').read_text()).keys() == source.keys()
for rel, expected in source.items():
    p = root/'inputs'/rel
    assert p.is_file(), rel
    assert hashlib.sha256(p.read_bytes()).hexdigest() == expected, rel
    got = subprocess.run(['git','show',f'{commit}:{rel}'], cwd=project, capture_output=True, check=True).stdout
    assert hashlib.sha256(got).hexdigest() == expected, rel
mods = json.loads((root/'module-results.json').read_text())
assert all(v == 0 for v in mods.values())
cmds = json.loads((root/'commands.json').read_text())
assert all(c['returncode'] == 0 for c in cmds)
pins = json.loads((root/'dependency-pins.json').read_text())
assert all(p['returncode'] == 0 and p['expected'] == p['actual'] for p in pins)
print(f'PASS: {len(source)} source hashes, {len(mods)} modules, {len(cmds)} commands, {len(pins)} pins')
