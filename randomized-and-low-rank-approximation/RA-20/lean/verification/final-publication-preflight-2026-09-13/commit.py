"""One-shot RA-20 publication acceptance and blank-email commit, after review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, subprocess

R = Path('/tmp/nla-lean-ra20-worktree').resolve()
P = R / 'randomized-and-low-rank-approximation/RA-20/lean'
D = P / 'verification/publication-preparation-2026-09-13'
V = P / 'verification/publication-referee-2026-09-13'
F = P / 'verification/final-publication-preflight-2026-09-13'
CANDIDATE = '43603b173beb294c2588d83f936a8a96246fd5f0'
CONFIG = Path('/tmp/nla-lean-formalization/RA-20-reviewed-publication-inputs.json')
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
git = lambda *args: subprocess.check_output(['git', *args], cwd=R, env=env)

assert CONFIG.is_file(), 'Root must first read and accept the sealed independent publication report'
config = json.loads(CONFIG.read_text())
assert config['independent_publication_approval_accepted_by_root'] is True
assert config['root_read_full_report_current_documents_and_verifiers'] is True
assert config['root_viewed_all_three_exact_PDF_pages'] is True
assert not F.exists(), 'Inspect the existing receipt instead of rerunning this one-shot operation'
assert git('rev-parse', 'HEAD').decode().strip() == CANDIDATE
assert not git('diff', '--cached', '--name-only')
for rel, expected in config['reviewed_anchors'].items():
    assert sha(P / rel) == expected, rel
assert sha(D / 'EVIDENCE-MANIFEST.json') == '3a2dbd0aa48277f7b5d87bd3b2f1e4e5a2abec571215de85783b10063bcb629a'
assert sha(P.parent / 'problem.pdf') == '066d45b7f3557796f18cf788ee457ec303ef9a391143e8904fd5a35e1b7ecf07'

# Run original read-only publication verifiers before adding the root phase.
checks = []
for directory in [D, V]:
    command = (['python3', str(D / 'verify_inventory.py')] if directory == D else
               ['python3', str(V / 'verify_publication.py'), '--check-own-seal'])
    result = subprocess.run(command, cwd=R, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, result.stdout.decode() + result.stderr.decode()
    checks.append((directory.name, command, result))

documents = json.loads((D / 'DOCUMENT-CHECKS.json').read_text())
outputs = documents['outputs']
assert len(outputs) == 9
assert set(git('diff', '--name-only').decode().splitlines()) == set(outputs)
for rel, record in outputs.items():
    assert sha(R / rel) == record['sha256'] and (R / rel).stat().st_size == record['bytes'], rel
assert len(json.loads((R / 'problem_ids.json').read_text())) == 217

# These enclosing inventories bind CURRENT bytes, including all exact historical archives.
retained = {}
inventories = {}
for directory in [D, V]:
    outer = directory / 'EVIDENCE-MANIFEST.json'
    manifest = json.loads(outer.read_text())
    internal = set()
    for rel, value in manifest['files'].items():
        path = (directory / rel).resolve()
        assert path.is_relative_to(R) and path.is_file() and not path.is_symlink(), str(path)
        digest = value if isinstance(value, str) else value['sha256']
        assert sha(path) == digest, str(path)
        if isinstance(value, dict) and 'bytes' in value:
            assert path.stat().st_size == value['bytes'], str(path)
        key = str(path.relative_to(R))
        assert key not in retained or retained[key] == digest, key
        retained[key] = digest
        if path.is_relative_to(directory):
            internal.add(path)
    assert internal == {p.resolve() for p in directory.rglob('*') if p.is_file() and p != outer}
    retained[str(outer.relative_to(R))] = sha(outer)
    inventories[str(outer.relative_to(P))] = {'sha256': sha(outer), 'bound_files': len(manifest['files'])}

new_directories = [P / 'verification' / name for name in [
    'linux-run-2026-09-13', 'root-linux-acceptance-2026-09-13',
    'publication-preparation-2026-09-13', 'publication-referee-2026-09-13']]
reports = [P / 'reviews' / name for name in [
    'linux-operational-referee-2026-09-13.md', 'publication-referee-2026-09-13.md']]
stage = [*sorted(outputs), *[str(p.relative_to(R)) for p in new_directories + reports]]
for rel in git('ls-files', '--others', '--exclude-standard').decode().splitlines():
    assert any(rel == item or rel.startswith(item + '/') for item in stage), rel
    assert rel in retained, ('unsealed new file', rel)
subprocess.run(['git', 'add', '--', *stage], cwd=R, check=True)
staged = git('diff', '--cached', '--name-only').decode().splitlines()
assert all(any(rel == item or rel.startswith(item + '/') for item in stage) for rel in staged)

initial = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=R,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert not initial.stderr
exceptions = {}
if initial.returncode:
    for line in initial.stdout.decode().splitlines():
        if line.startswith('+') or not line:
            continue  # Exact content lines, not Git's path:line diagnostic headers.
        match = re.fullmatch(r'(.+):\d+: (?:trailing whitespace\.|new blank line at EOF\.)', line)
        assert match, ('unexpected whitespace diagnostic', line)
        rel = match.group(1)
        assert rel in retained and sha(R / rel) == retained[rel], rel
        exceptions[rel] = {'sha256': retained[rel], 'reason': 'Exact sealed raw evidence; not normalized'}
    assert exceptions

F.mkdir()
raw = F / 'git-diff-check-initial.log'
raw.write_bytes(initial.stdout)
if any(line.endswith((b' ', b'\t')) for line in initial.stdout.splitlines()) or initial.stdout.endswith(b'\n\n'):
    exceptions[str(raw.relative_to(R))] = {'sha256': sha(raw), 'reason': 'Original staged-check output retained verbatim'}
command = ['git', 'diff', '--cached', '--check', '--', '.'] + [
    ':(exclude)' + rel for rel in sorted(exceptions)]
result = subprocess.run(command, cwd=R, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert result.returncode == 0, result.stdout.decode() + result.stderr.decode()
for label, args, result in checks:
    (F / (label + '.stdout')).write_bytes(result.stdout)
    (F / (label + '.stderr')).write_bytes(result.stderr)
    (F / (label + '.json')).write_text(json.dumps({'command': args, 'exit_code': result.returncode}, indent=2) + '\n')
acceptance = {
    'utc': datetime.now(timezone.utc).isoformat(), 'problem': 'RA-20',
    'status': 'Root accepts independent review of concrete publication; normal push and new upstream main PR authorized by user',
    'root_role': 'Mathematical contributor and publication coordinator, not an additional independent mathematical referee',
    'publication_referee': '/root/ie05_statement_referee2, independent of RA20 proof and publication',
    'accepted_config': config,
    'accepted_current_publication_files': outputs,
    'candidate': CANDIDATE, 'actual_Linux_run': 34743832047,
    'exact_tested_candidate_inputs_preserved': 1092,
    'prior_accepted_inventories_checked_with_exact_path_and_hash_archives': 19,
    'rejected_initial_root_diagnostic_retained_without_acceptance': True,
    'all_217_IDs_paths_and_original_target_preserved': True,
    'complete_current_enclosing_inventories': inventories,
    'exact_hash_bound_whitespace_exceptions': exceptions,
    'successful_whitespace_command': command,
    'no_new_proof_or_Linux_execution_claimed': True,
}
(F / 'ROOT-ACCEPTANCE.json').write_text(json.dumps(acceptance, indent=2) + '\n')
(F / 'commit.py').write_bytes(Path(__file__).read_bytes())
outer = F / 'EVIDENCE-MANIFEST.json'
members = {str(p.relative_to(F)): {'sha256': sha(p), 'bytes': p.stat().st_size}
           for p in sorted(F.rglob('*')) if p.is_file()}
outer.write_text(json.dumps({'scope': 'Every file in this root phase; only exact outer self excluded',
                            'files': members}, indent=2) + '\n')
subprocess.run(['git', 'add', '--', str(F.relative_to(R))], cwd=R, check=True)
subprocess.run(command, cwd=R, check=True)

# Check all actual index blobs against the reviewed on-disk bytes in one Git batch.
rows = []
for line in git('diff', '--cached', '--raw', '--no-abbrev').decode().splitlines():
    metadata, rel = line.split('\t', 1)
    fields = metadata.split()
    assert fields[1] in ['100644', '100755'] and fields[-1] in ['A', 'M']
    rows.append((fields[3], rel))
raw_blobs = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=R,
    input=''.join(oid + '\n' for oid, _ in rows).encode())
offset = 0
for oid, rel in rows:
    end = raw_blobs.index(b'\n', offset)
    actual_oid, kind, size = raw_blobs[offset:end].decode().split(); size = int(size)
    contents = raw_blobs[end + 1:end + 1 + size]; offset = end + size + 2
    assert actual_oid == oid and kind == 'blob' and raw_blobs[offset - 1:offset] == b'\n'
    assert contents == (R / rel).read_bytes(), rel
assert offset == len(raw_blobs)
identity = dict(env, GIT_AUTHOR_NAME='George Stepaniants', GIT_COMMITTER_NAME='George Stepaniants',
                GIT_AUTHOR_EMAIL='', GIT_COMMITTER_EMAIL='')
commit = subprocess.run(['git', '-c', 'user.name=George Stepaniants', '-c', 'user.email=',
    '-c', 'commit.gpgsign=false', 'commit', '-m',
    'Publish Linux-verified RA-20 formalization and reviewed evidence'], cwd=R, env=identity,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert commit.returncode == 0, commit.stdout.decode() + commit.stderr.decode()
assert git('show', '-s', '--format=%ae%x00%ce', 'HEAD').rstrip(b'\n') == b'\0'
assert not git('status', '--porcelain')
receipt = {'problem': 'RA-20', 'candidate': CANDIDATE,
           'publication_commit': git('rev-parse', 'HEAD').decode().strip(),
           'root_acceptance_sha256': sha(F / 'ROOT-ACCEPTANCE.json'),
           'root_phase_manifest_sha256': sha(outer), 'staged_files_checked': len(rows),
           'blank_author_and_committer_emails': True, 'worktree_clean': True,
           'exact_whitespace_exceptions': len(exceptions)}
Path('/tmp/nla-lean-formalization/RA-20-final-publication-commit.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
