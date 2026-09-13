from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, subprocess, os, sys

R = Path('/tmp/nla-lean-ra20-worktree')
prefix = 'randomized-and-low-rank-approximation/RA-20/lean/'
P = R / prefix
D = P / 'verification/linux-candidate-2026-09-13'
V = P / 'verification/candidate-packaging-referee-2026-09-13'
O = P / 'verification/root-candidate-2026-09-13'
config_path = Path('/tmp/nla-lean-formalization/RA-20-reviewed-candidate-inputs.json')
config = json.loads(config_path.read_text())
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
git = lambda *args: subprocess.check_output(['git', *args], cwd=R)
old_readme = '7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
assert not O.exists(), 'One-shot candidate commit; inspect an existing receipt before resuming'
assert config['root_read_complete_report_and_live_wrappers'] is True
assert config['independent_packaging_verdict'] == 'APPROVE'
assert git('rev-parse', 'HEAD').decode().strip() == '5830ed4fb06da0659414a3deb2a40ad327aca052'
assert not git('diff', '--name-only') and not git('diff', '--cached', '--name-only')
report = P / 'reviews/candidate-packaging-referee-2026-09-13.md'
for file, digest in config['reviewed_files'].items():
    assert h(P / file) == digest, file
assert h(P / 'verification/final-review-acceptance.json') == 'a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb'
verifier_command = [sys.executable, str(V / 'verify_inventory.py')]
verifier_result = subprocess.run(verifier_command, cwd=R,
    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert verifier_result.returncode == 0, verifier_result.stdout.decode() + verifier_result.stderr.decode()
verifier_output = json.loads(verifier_result.stdout)
assert verifier_output['status'] == 'INDEPENDENT_PACKAGING_SEAL_PASS'
assert verifier_output['file_count'] == 1102 and verifier_output['successful_command_receipts'] == 21

def resolved_historical(path, expected):
    if path.resolve() == (P / 'README.md').resolve() and expected == old_readme:
        return P / 'verification/pre-candidate-README.md'
    return path

baseline = json.loads((D / 'preflight.json').read_text())['baseline']
assert len(baseline) == 958
retained = {}
for rel, value in baseline.items():
    file = resolved_historical(P / rel, value['sha256'])
    assert h(file) == value['sha256'] and file.stat().st_size == value['bytes'], rel
    retained[str(file.relative_to(R))] = value['sha256']
inventories = {}
for directory in [D, V]:
    outer = directory / 'EVIDENCE-MANIFEST.json'
    members = json.loads(outer.read_text())['files']
    internal = set()
    for rel, value in members.items():
        expected = value if isinstance(value, str) else value['sha256']
        original = (directory / rel).resolve()
        assert original.is_relative_to(R.resolve()), str(original)
        file = resolved_historical(original, expected)
        assert h(file) == expected, (directory, rel)
        if isinstance(value, dict) and 'bytes' in value:
            assert file.stat().st_size == value['bytes'], rel
        retained[str(file.resolve().relative_to(R.resolve()))] = expected
        if original.is_relative_to(directory.resolve()):
            internal.add(str(original.relative_to(directory.resolve())))
    actual = {str(q.relative_to(directory)) for q in directory.rglob('*') if q.is_file() and q != outer}
    assert internal == actual, directory
    retained[str(outer.relative_to(R))] = h(outer)
    inventories[str(outer.relative_to(P))] = {'sha256': h(outer), 'bound_files': len(members)}

F = json.loads((P / 'verification/proof-freeze.json').read_text())
for rel, digest in F['source_files'].items():
    assert h(R / rel) == digest
    assert hashlib.sha256(git('show', F['base'] + ':' + rel)).hexdigest() == digest
for rel, digest in F['files'].items():
    assert h(resolved_historical(P / rel, digest)) == digest, rel
assert len(F['files']) == 521 and len(F['source_files']) == 16
assert '**Status:** Solved' in (P.parent / 'README.md').read_text()
assert len(json.loads((R / 'problem_ids.json').read_text())) == 217
email_pattern = re.compile(rb'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
for file in P.rglob('*'):
    if file.is_file():
        assert not email_pattern.search(file.read_bytes()), 'Inspect address-like token in ' + str(file.relative_to(P))
before = {str(q.relative_to(P)): h(q) for q in sorted(P.rglob('*')) if q.is_file()}
assert set(before) == {rel.removeprefix(prefix) for rel in git('ls-files', '--others', '--exclude-standard', '--', prefix).decode().splitlines()}
subprocess.run(['git', 'add', '--', prefix], cwd=R, check=True)
assert all(rel.startswith(prefix) for rel in git('diff', '--cached', '--name-only').decode().splitlines())
initial = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=R, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert not initial.stderr
exceptions = {}
if initial.returncode:
    for line in initial.stdout.decode().splitlines():
        match = re.match(r'^(.+):\d+: (?:trailing whitespace\.|new blank line at EOF\.)$', line)
        if match:
            rel = match.group(1)
            assert rel in retained and h(R / rel) == retained[rel], rel
            exceptions[rel] = {'sha256': retained[rel], 'reason': 'Exact already sealed source or historical raw evidence; no normalization'}
        elif re.match(r'^.+:\d+: ', line):
            raise AssertionError(line)
    assert exceptions, initial.stdout.decode()
O.mkdir()
(O / 'independent-seal-recheck.log').write_bytes(verifier_result.stdout)
(O / 'independent-seal-recheck-command.json').write_text(json.dumps({
    'argv': verifier_command, 'cwd': str(R), 'PYTHONDONTWRITEBYTECODE': '1',
    'returncode': verifier_result.returncode, 'stderr': verifier_result.stderr.decode(),
    'stdout_sha256': hashlib.sha256(verifier_result.stdout).hexdigest()}, indent=2) + '\n')
raw = O / 'git-diff-check-initial.log'
raw.write_bytes(initial.stdout)
if any(line.endswith((b' ', b'\t')) for line in initial.stdout.splitlines()) or initial.stdout.endswith(b'\n\n'):
    exceptions[str(raw.relative_to(R))] = {'sha256': h(raw), 'reason': 'Exact raw output of the preceding staged check'}
command = ['git', 'diff', '--cached', '--check', '--', '.'] + [':(exclude)' + rel for rel in sorted(exceptions)]
check = subprocess.run(command, cwd=R, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert check.returncode == 0, check.stdout.decode() + check.stderr.decode()
record = {'utc': datetime.now(timezone.utc).isoformat(),
          'status': 'Root accepts independent concrete packaging approval; commit and fork push for actual Linux authorized',
          'root_role': 'Generic proof contributor and coordinator; not an independent final mathematical referee or candidate-wrapper author',
          'independent_packaging_report_sha256': h(report),
          'independent_packaging_evidence_sha256': h(V / 'EVIDENCE-MANIFEST.json'),
          'root_read_complete_live_README_YAML_and_report': True,
          'prior_inputs': before, 'prior_input_count': len(before),
          'complete_package_inventories': inventories,
          'read_only_independent_verifier_reexecuted': verifier_output,
          'final_review_gate_sha256': h(P / 'verification/final-review-acceptance.json'),
          'proof_inputs_preserved': 521, 'original_source_Git_blobs_preserved': 16,
          'historical_archive_mapping': {'exact_path': 'README.md', 'expected_sha256': old_readme, 'archive': 'verification/pre-candidate-README.md'},
          'all_217_IDs_and_original_target_preserved': True,
          'address_like_tokens_in_entire_candidate': 0,
          'exact_hash_bound_whitespace_exceptions': exceptions,
          'successful_whitespace_command': command, 'canonical_status': 'Solved, unchanged',
          'actual_Linux_Comparator_default_kernel_controls': 'Pending; this candidate is prepared for its first authoritative run',
          'new_local_proof_or_dependency_build': False}
(O / 'ROOT-CHECKS.json').write_text(json.dumps(record, indent=2) + '\n')
(O / 'reviewed-inputs.json').write_bytes(config_path.read_bytes())
(O / 'commit_candidate.py').write_bytes(Path(__file__).read_bytes())
outer = O / 'EVIDENCE-MANIFEST.json'
files = {str(q.relative_to(O)): {'sha256': h(q), 'bytes': q.stat().st_size} for q in sorted(O.rglob('*')) if q.is_file()}
outer.write_text(json.dumps({'scope': 'Every file in this directory; exact outer self exclusion only', 'files': files}, indent=2) + '\n')
subprocess.run(['git', 'add', '--', str(O.relative_to(R))], cwd=R, check=True)
subprocess.run(command, cwd=R, check=True)
for row in git('diff', '--cached', '--raw', '--no-abbrev').decode().splitlines():
    metadata, path = row.split('\t', 1)
    fields = metadata.split()
    assert fields[1] in ['100644', '100755']
    assert hashlib.sha256(git('cat-file', 'blob', fields[3])).hexdigest() == h(R / path), path
env = dict(os.environ, GIT_AUTHOR_NAME='George Stepaniants', GIT_COMMITTER_NAME='George Stepaniants',
           GIT_AUTHOR_EMAIL='', GIT_COMMITTER_EMAIL='')
result = subprocess.run(['git', '-c', 'user.name=George Stepaniants', '-c', 'user.email=',
                         '-c', 'commit.gpgsign=false', 'commit', '-m',
                         'Add reviewed RA-20 Lean candidate for authoritative Linux verification'],
                        cwd=R, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert result.returncode == 0, result.stdout.decode() + result.stderr.decode()
assert git('show', '-s', '--format=%ae%x00%ce', 'HEAD').rstrip(b'\n') == b'\0'
assert not git('status', '--porcelain')
receipt = {'problem': 'RA-20', 'candidate': git('rev-parse', 'HEAD').decode().strip(),
           'candidate_inputs': len(before) + len(files) + 1,
           'blank_author_and_committer_emails': True, 'worktree_clean': True,
           'root_candidate_sha256': h(O / 'ROOT-CHECKS.json'), 'root_evidence_sha256': h(outer),
           'exact_whitespace_exceptions': len(exceptions), 'canonical_status': 'Solved, unchanged',
           'actual_Linux': 'pending'}
Path('/tmp/nla-lean-formalization/RA-20-candidate-commit.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
