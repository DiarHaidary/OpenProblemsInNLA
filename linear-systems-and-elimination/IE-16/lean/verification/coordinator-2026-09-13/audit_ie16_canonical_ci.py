"""Read-only coordinator audit of the already-completed IE-16 Linux run."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import tempfile

WORK = Path('/tmp/nla-ie16-development-worktree')
EVIDENCE = Path('/tmp/nla-ie16-canonical-ci-34774629327')
RAW = EVIDENCE / 'extracted/verify-20260913T182805Z-4150'
HEAD = '697a2a1d88337a6747aa5c82fb6e554d3ff1b356'
PROJECT = 'linear-systems-and-elimination/IE-16/lean'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_file(path):
    return subprocess.check_output(['git', 'show', HEAD + ':' + path], cwd=WORK)

result = json.loads((RAW / 'result.json').read_text())
assert result['repository_commit'] == HEAD
assert result['project'] == PROJECT
assert result['result'] == 'comparator-accepted'
config = json.loads(git_file(PROJECT + '/comparator.json'))
assert result['config'] == config
names = config['theorem_names']
assert len(names) == len(set(names)) == 15
assert config['definition_names'] == []
assert set(config['permitted_axioms']) == ALLOWED
inputs = result['input_sha256']
assert len(inputs) == 281
for path, digest in inputs.items():
    assert sha(git_file(PROJECT + '/' + path)) == digest, path

logs = {p.name: p.read_text() for p in RAW.glob('*.log')}
main = logs['comparator.log']
assert 'Build completed successfully (3136 jobs).' in main
assert 'Lean default kernel accepts the solution' in main
assert 'Your solution is okay!' in main
assert main.rstrip().endswith('EXIT_STATUS=0')
axioms = dict(re.findall(r"'(NLA\.IE16\.[^']+)' depends on axioms: \[([^\]]*)\]", main))
assert set(axioms) == set(names)
assert all(set(a.strip() for a in axioms[n].split(',')) == ALLOWED for n in names)
source = git_file(PROJECT + '/Solution.lean').decode()
assert source.count('#assert_trust kernel') == 15
assert 'import Challenge' not in source
assert 'Sandbox UID: 1001' in logs['sandbox.log']
assert logs['sandbox.log'].count('PASS effective capabilities: none') == 2
assert logs['sandbox.log'].count('PASS no_new_privs: set') == 2
assert 'PASS: all three actual Comparator.runBuiltinKernel cases behaved as required' in logs['kernel-controls.log']
assert 'PASS: all five Comparator regressions' in logs['comparator-controls.log']
assert "Illegal axiom detected: 'sorryAx'" in logs['negative-sorry.log']
assert "Illegal axiom detected: 'checked._native.native_decide.ax_1_1'" in logs['negative-native.log']
assert logs['negative-sorry.log'].rstrip().endswith('EXIT_STATUS=1')
assert logs['negative-native.log'].rstrip().endswith('EXIT_STATUS=1')
assert result['tool_receipt']['forsythe_commit'] == '8d1b0c0545a77b40245e84705aa7d273e6c81e62'
assert result['tool_receipt']['lean_toolchain'] == 'leanprover/lean4:v4.33.1'
assert result['source_lock_sha256'] == sha(git_file('tools/lean/source-lock.json'))

report = {
    'scope': 'Coordinator source/evidence audit of an existing Linux run; no new compiler execution and no independent mathematical referee claim.',
    'reviewer': 'OpenAI Codex primary agent /root',
    'candidate_commit': HEAD,
    'linux_run': 34774629327,
    'linux_job': 103770408910,
    'project': PROJECT,
    'input_count': len(inputs),
    'all_input_hashes_match_git_candidate': True,
    'target_contract_count': len(names),
    'actual_axioms': {n: sorted(ALLOWED) for n in names},
    'all_replay_comparator_sandbox_and_negative_controls_pass': True,
    'raw_sha256': {p.name: sha(p.read_bytes()) for p in sorted(RAW.iterdir()) if p.is_file()},
    'proof_and_boundary_sha256': {p: d for p, d in inputs.items() if p == 'Solution.lean' or p == 'Challenge.lean' or p.startswith('NLA/') and p.endswith('.lean')},
}
destination = EVIDENCE / 'COORDINATOR-CHECKS.json'
fd, temporary = tempfile.mkstemp(prefix='.coordinator-', dir=destination.parent)
with os.fdopen(fd, 'w') as f:
    f.write(json.dumps(report, indent=2) + '\n')
    f.flush()
    os.fsync(f.fileno())
os.replace(temporary, destination)
print(json.dumps({'result': 'PASS', 'inputs': len(inputs), 'contracts': len(names), 'report': str(destination), 'sha256': sha(destination.read_bytes())}))
