#!/usr/bin/env python3
"""Fetch only the existing NR03 canonical run; never launch a workflow or compiler."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, os, stat, subprocess, tempfile, zipfile
ROOT = Path(__file__).resolve().parent
GH = '/tmp/nla-submission-tools/gh_2.100.0_macOS_arm64/bin/gh'
REPO = 'repos/sgstepaniants/OpenProblemsInNLA'
RUN = 34785341662
COMMIT = 'f664d07e82aaa60bc9c78dd1946e763168c5c530'
WORKTREE = Path('/tmp/nla-lean-nr03-publication-worktree')
PREFIX = 'nonnegative-and-positive-factorizations/NR-03/lean/'
def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f'Refuse to replace retained evidence: {path}')
        return
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)
def api(endpoint):
    data = subprocess.run([GH, 'api', endpoint], check=True, stdout=subprocess.PIPE, timeout=60).stdout
    if len(data) > 6_000_000:
        raise ValueError('Unexpectedly large GitHub response')
    return data
def sha(data): return hashlib.sha256(data).hexdigest()
def raw_json(name, endpoint):
    data = api(endpoint); value = json.loads(data)
    atomic(ROOT / name, data)
    return value
run_data = api(f'{REPO}/actions/runs/{RUN}')
run = json.loads(run_data)
assert run['head_sha'] == COMMIT and run['name'] == 'Lean verification'
if run['status'] != 'completed':
    if not (ROOT / 'run-initial.json').exists(): atomic(ROOT / 'run-initial.json', run_data)
    jobs_data = api(f'{REPO}/actions/runs/{RUN}/jobs?per_page=100')
    jobs_now = json.loads(jobs_data)['jobs']
    selected = [j for j in jobs_now if j['name'].startswith('verify (')]
    assert len(selected) == 1 and selected[0]['id'] == 103799711659
    assert selected[0]['name'] == 'verify (NR-03, nonnegative-and-positive-factorizations/NR-03/lean)'
    if not (ROOT / 'jobs-initial.json').exists(): atomic(ROOT / 'jobs-initial.json', jobs_data)
    print(json.dumps({'selected_job': selected[0]['id'], 'active_steps': [s['name'] for s in selected[0]['steps'] if s['status'] == 'in_progress']}))
    print(json.dumps({'run_id': RUN, 'status': run['status'], 'conclusion': run['conclusion']}))
    raise SystemExit(0)
atomic(ROOT / 'run-final.json', run_data)
jobs = raw_json('jobs-final.json', f'{REPO}/actions/runs/{RUN}/jobs?per_page=100')
verify_jobs = [j for j in jobs['jobs'] if j['name'].startswith('verify (')]
assert len(verify_jobs) == 1
job = verify_jobs[0]
assert job['id'] == 103799711659 and job['name'] == 'verify (NR-03, nonnegative-and-positive-factorizations/NR-03/lean)'
artifacts = raw_json('artifacts-final.json', f'{REPO}/actions/runs/{RUN}/artifacts?per_page=100')['artifacts']
assert len(artifacts) == 1, 'Inspect absent or unexpected artifact list before proceeding'
a = artifacts[0]
assert a['name'] == 'lean-NR-03' and not a['expired'] and a['size_in_bytes'] < 5_000_000
assert os.statvfs(ROOT).f_bavail * os.statvfs(ROOT).f_frsize > 100_000_000
archive = api(f"{REPO}/actions/artifacts/{a['id']}/zip")
assert len(archive) < 5_000_000
if a.get('digest'): assert a['digest'] == 'sha256:' + sha(archive)
atomic(ROOT / 'artifact.zip', archive)
extracted = {}
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    assert sum(f.file_size for f in z.infolist()) < 20_000_000
    for info in z.infolist():
        rel = PurePosixPath(info.filename)
        assert not rel.is_absolute() and '..' not in rel.parts
        assert not stat.S_ISLNK(info.external_attr >> 16)
        if info.is_dir(): continue
        data = z.read(info)
        atomic(ROOT / 'extracted' / rel, data)
        extracted[str(rel)] = sha(data)
results = sorted((ROOT / 'extracted').rglob('result.json'))
accepted = [f for f in results if json.loads(f.read_text()).get('result') == 'comparator-accepted']
checks = {'run': RUN, 'job': job['id'], 'commit': COMMIT,
          'run_conclusion': run['conclusion'], 'job_conclusion': job['conclusion'],
          'artifact_id': a['id'], 'artifact_size_bytes': len(archive),
          'artifact_sha256': sha(archive), 'extracted_sha256': extracted,
          'local_compiler_executed': False, 'workflow_launched_by_fetcher': False,
          'independent_mathematical_acceptance': 'not performed by this fetcher'}
if accepted:
    assert len(accepted) == 1 and run['conclusion'] == job['conclusion'] == 'success'
    result = json.loads(accepted[0].read_text())
    assert result['repository_commit'] == COMMIT and result['project'] == PREFIX[:-1]
    for rel, digest in result['input_sha256'].items():
        data = subprocess.check_output(['git', 'show', COMMIT + ':' + PREFIX + rel], cwd=WORKTREE)
        assert sha(data) == digest, rel
    checks['comparator_result'] = str(accepted[0].relative_to(ROOT))
    checks['inputs_matched_to_commit'] = len(result['input_sha256'])
    checks['all_configured_contracts'] = result['config']['theorem_names']
    checks['result'] = 'comparator-accepted; operational and semantic review still separate'
else:
    checks['result'] = 'No accepted Comparator record; inspect retained failure logs'
atomic(ROOT / 'FETCH-CHECKS.json', (json.dumps(checks, indent=2) + '\n').encode())
print(json.dumps({k: v for k, v in checks.items() if k != 'extracted_sha256'}, indent=2))
