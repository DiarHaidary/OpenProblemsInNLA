#!/usr/bin/env python3
"""Read-only final IE-16 source/evidence audit; no Lean/Lake invocation."""
from __future__ import annotations
import hashlib, json, pathlib, re, subprocess, sys

WORK = pathlib.Path('/tmp/nla-ie16-development-worktree')
PROJECT = WORK / 'linear-systems-and-elimination/IE-16/lean'
RAWROOT = pathlib.Path('/tmp/nla-ie16-canonical-ci-34774629327')
RAW = RAWROOT / 'extracted/verify-20260913T182805Z-4150'
COMMIT = '697a2a1d88337a6747aa5c82fb6e554d3ff1b356'
FIFTH = '281fc3790412b7ab2b05c202c0351b4d259a6382'
PREF = 'linear-systems-and-elimination/IE-16/lean/'

def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha_file(p: pathlib.Path) -> str:
    return sha_bytes(p.read_bytes())

def git_blob(c: str, p: str) -> bytes:
    return subprocess.check_output(['git', '-C', str(WORK), 'show', f'{c}:{p}'])

def norm_body(s: str) -> str:
    # The fifth-to-canonical source transition changed only leading comments;
    # normalize comments and whitespace for a conservative body comparison.
    s = re.sub(r'/\-.*?\-/', '', s, flags=re.S)
    s = re.sub(r'(?m)--[^\n]*', '', s)
    return re.sub(r'\s+', '', s)

result = json.loads((RAW / 'result.json').read_text())
assert result['repository_commit'] == COMMIT
assert result['project'] == 'linear-systems-and-elimination/IE-16/lean'
inputs = result['input_sha256']
assert len(inputs) == 281
missing = []
bad = []
for rel, expected in inputs.items():
    try:
        b = git_blob(COMMIT, PREF + rel)
    except subprocess.CalledProcessError:
        missing.append(rel)
        continue
    if sha_bytes(b) != expected:
        bad.append(rel)
assert not missing and not bad, (missing, bad[:5])
fs_missing = []
fs_bad = []
for rel, expected in inputs.items():
    p = PROJECT / rel
    if not p.is_file():
        fs_missing.append(rel)
    elif sha_file(p) != expected:
        fs_bad.append(rel)
assert not fs_missing and not fs_bad, (fs_missing, fs_bad[:5])

# The pinned harness source lock is exactly the receipt's source lock.
lock = WORK / 'tools/lean/source-lock.json'
assert sha_file(lock) == result['source_lock_sha256']

# Exact proof-bearing transition from the fifth compiled snapshot.
proof_files = [
    'NLA/IE16/Definitions.lean', 'NLA/IE16/FinalContractsDraft.lean',
    'NLA/IE16/FullMinimumDraft.lean', 'NLA/IE16/Minimax.lean',
    'NLA/IE16/Numeric.lean', 'NLA/IE16/SubsetBoundsDraft.lean',
    'NLA/IE16/SubsetGeometryDraft.lean', 'NLA/IE16/WeightedBridgeDraft.lean',
    'NLA/IE16/WeightedDraft.lean', 'Solution.lean', 'Challenge.lean',
    'NUMERICAL_TARGETS.md', 'comparator.json', 'lean-toolchain'
]
body_same = {}
for rel in proof_files:
    old = git_blob(FIFTH, 'development/IE16/' + rel)
    new = git_blob(COMMIT, PREF + rel)
    body_same[rel] = norm_body(old.decode()) == norm_body(new.decode())
assert all(body_same.values())

# The current Solution source has one trust assertion per configured export and
# no source-level forbidden proof shortcuts in active proof modules.
config = json.loads((PROJECT / 'comparator.json').read_text())
names = config['theorem_names']
solution = (PROJECT / 'Solution.lean').read_text()
assert len(names) == 15
assert solution.count('#assert_trust kernel') == 15
assert all(re.search(r'#assert_trust kernel ' + re.escape(n.rsplit('.', 1)[-1]) + r'\b', solution) for n in names)
active = ['NLA/IE16/FinalContractsDraft.lean','NLA/IE16/FullMinimumDraft.lean',
          'NLA/IE16/Minimax.lean','NLA/IE16/Numeric.lean',
          'NLA/IE16/SubsetBoundsDraft.lean','NLA/IE16/SubsetGeometryDraft.lean',
          'NLA/IE16/WeightedBridgeDraft.lean','NLA/IE16/WeightedDraft.lean','Solution.lean']
lexical = {}
for rel in active:
    s = (PROJECT / rel).read_text()
    lexical[rel] = {k: len(re.findall(p, s)) for k,p in {
        'sorry': r'\bsorry\b', 'admit': r'\badmit\b',
        'axiom': r'\baxiom\b', 'native_decide': r'\bnative_decide\b'
    }.items()}
assert all(all(v == 0 for v in x.values()) for x in lexical.values())

# Independent reading of the raw API receipts and retained logs.
run = json.loads((RAWROOT / 'run-final.json').read_text())
jobs = json.loads((RAWROOT / 'jobs-final.json').read_text())
job = next(j for j in jobs['jobs'] if j['id'] == 103770408910)
artifacts = json.loads((RAWROOT / 'artifacts-final.json').read_text())['artifacts']
assert run['status'] == 'completed' and run['conclusion'] == 'success' and run['head_sha'] == COMMIT
assert job['status'] == 'completed' and job['conclusion'] == 'success'
assert job['name'] == 'verify (IE-16, linear-systems-and-elimination/IE-16/lean)'
assert len(artifacts) == 1 and artifacts[0]['id'] == 10322764134
artifact = artifacts[0]
assert not artifact['expired'] and artifact['digest'] == 'sha256:' + sha_file(RAWROOT / 'artifact.zip')

clog = (RAW / 'comparator.log').read_text()
ctrl = (RAW / 'comparator-controls.log').read_text()
klog = (RAW / 'kernel-controls.log').read_text()
slog = (RAW / 'sandbox.log').read_text()
native = (RAW / 'negative-native.log').read_text()
sorry = (RAW / 'negative-sorry.log').read_text()
deps = (RAW / 'dependencies.log').read_text()
assert 'Lean default kernel accepts the solution' in clog
assert 'Your solution is okay!' in clog and 'EXIT_STATUS=0' in clog
assert 'PASS: all five Comparator regressions' in ctrl and 'EXIT_STATUS=0' in ctrl
assert 'PASS: all three actual Comparator.runBuiltinKernel cases behaved as required' in klog
assert 'EXIT_STATUS=0' in klog and 'EXIT_STATUS=0' in slog
assert all(x in slog for x in ['PASS outside .lake write-open: denied', 'PASS user namespace: private',
                                'PASS pid namespace: private', 'PASS net namespace: private',
                                'PASS AF_UNIX socket creation: denied'])
assert 'Illegal axiom detected' in native and 'native_decide.ax_1_1' in native and 'EXIT_STATUS=1' in native
assert 'Illegal axiom detected' in sorry and 'sorryAx' in sorry and 'EXIT_STATUS=1' in sorry
assert 'EXIT_STATUS=0' in deps

raw_hashes = {f.name: sha_file(f) for f in sorted(RAW.iterdir()) if f.is_file()}
api_hashes = {f: sha_file(RAWROOT / f) for f in ['run-final.json','jobs-final.json','artifacts-final.json',
                                                 'FETCH-CHECKS.json','OPERATIONAL-CHECKS.json']}
checks = {
    'reviewer': '/root/lean_iv01_next (OpenAI Codex AI agent)',
    'review_date': '2026-09-13',
    'local_lean_or_lake_run': False,
    'candidate_commit': COMMIT,
    'fifth_compiled_commit': FIFTH,
    'project': result['project'],
    'input_count': len(inputs),
    'git_input_hashes_match': True,
    'filesystem_input_hashes_match': True,
    'source_lock_sha256': result['source_lock_sha256'],
    'source_lock_matches': True,
    'proof_transition_body_comparison': body_same,
    'all_15_assert_trust_commands': True,
    'active_proof_lexical_scan': lexical,
    'run_id': run['id'],
    'job_id': job['id'],
    'run_conclusion': run['conclusion'],
    'job_conclusion': job['conclusion'],
    'artifact_id': artifact['id'],
    'artifact_size_bytes': artifact['size_in_bytes'],
    'artifact_sha256': sha_file(RAWROOT / 'artifact.zip'),
    'configured_export_count': len(names),
    'raw_comparator_acceptance': True,
    'raw_default_kernel_acceptance': True,
    'raw_comparator_controls': True,
    'raw_sandbox_controls': True,
    'raw_negative_sorry_control_rejected': True,
    'raw_negative_native_control_rejected': True,
    'raw_dependency_setup_exit_zero': True,
    'raw_log_sha256': raw_hashes,
    'api_receipt_sha256': api_hashes,
}
(PROJECT / 'comparator.json').read_text()  # ensure source was read as a file
print(json.dumps(checks, indent=2, sort_keys=True))
