#!/usr/bin/env python3
"""Read-only GitHub authentication of the IE-16 Lean proofs.

Usage: python3 -B SCRIPT --pr NUMBER --head SHA --base SHA [--run-id ID]
All network operations are explicit GitHub GET requests through gh. No checkout,
fetch, push, rerun, comment, or other GitHub/branch mutation is performed.
Writes raw evidence and a final receipt beneath --output (default /private/tmp).
An incomplete/failed/mismatched workflow raises an error, never a partial PASS.
"""
from pathlib import Path, PurePosixPath
import argparse
import ast
import base64
import copy
import hashlib
import json
import re
import stat
import subprocess
import sys
import zipfile

GITHUB = 'ajt60gaibb/OpenProblemsInNLA'
REPOSITORY_ID = 1360959635
WORKFLOW = '.github/workflows/lean-verification.yml'
TRUSTED_BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
PROJECTS = {'IE-16': 'linear-systems-and-elimination/IE-16/lean'}
EXPECTED_EXPORT_COUNTS = {'IE-16': 15}

STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}
CHECKER_PATHS = ('tools/lean', '.github/workflows', 'docs/lean/ci-toolchain',
                 'docs/lean/ci-toolchain.md')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')


def git_command(repo):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args], timeout=60)
    return git


def api(endpoint, path=None, binary=False):
    assert endpoint.startswith(('repos/' + GITHUB + '/', 'repos/sgstepaniants/Forsythe/'))
    raw = subprocess.check_output(['gh', 'api', '--method', 'GET', endpoint], timeout=60)
    value = raw if binary else json.loads(raw)
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    return value


def paged(endpoint, key, path):
    values = []
    pages = []
    for page in range(1, 101):
        query = '&' if '?' in endpoint else '?'
        data = api(endpoint + query + f'per_page=100&page={page}')
        pages.append(data)
        values.extend(data[key])
        if len(data[key]) < 100:
            break
    else:
        raise AssertionError('pagination exceeded 100 pages')
    save_json(path, {key: values, 'pages': pages})
    return values


def checked_commit(mc, base, head, tree):
    assert re.fullmatch('[a-f0-9]{40}', mc['sha']), 'invalid checked commit'
    assert [p['sha'] for p in mc['parents']] == [base, head], 'checked merge parents mismatch'
    assert mc['tree']['sha'] == tree, 'checked merge tree differs from reviewed head'
    return mc['sha']


def tool_context(repo, head, base, probe_json):
    git = git_command(repo)
    for before in (base, TRUSTED_BASE):
        assert git('diff', '--name-only', before, head, '--', *CHECKER_PATHS) == b'', \
            'shared checker/workflows/toolchain changed; separate review required'
    raw = git('show', head + ':tools/lean/source-lock.json')
    lock = json.loads(raw)
    assert lock['repository'] == 'https://github.com/sgstepaniants/Forsythe'
    assert lock['commit'] == '8d1b0c0545a77b40245e84705aa7d273e6c81e62'
    assert lock['lean_toolchain'] == 'leanprover/lean4:v4.33.1'
    entry = next(x for x in lock['files'] if x['source'].endswith('/sandbox_probe.py'))
    pinned = base64.b64decode(json.loads(probe_json.read_text())['content'])
    assert sha(pinned) == entry['sha256'] and len(pinned) == entry['bytes']
    function = next(x for x in ast.parse(git('show', head + ':tools/lean/harness.py')).body
                    if isinstance(x, ast.FunctionDef) and x.name == 'ci_probe_source')
    replacements = ast.literal_eval(next(x.value for x in function.body
        if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'replacements'
                                             for t in x.targets)))
    source = pinned.decode()
    for before, after, count in replacements:
        assert source.count(before) == count
        source = source.replace(before, after)
    return {'lock': lock, 'lock_sha': sha(raw), 'probe_sha': sha(source.encode())}


def archive_members(path, artifact):
    raw = path.read_bytes()
    assert artifact['digest'] == 'sha256:' + sha(raw), 'artifact ZIP digest mismatch'
    assert artifact['size_in_bytes'] == len(raw), 'artifact ZIP size mismatch'
    with zipfile.ZipFile(path) as z:
        assert len(z.namelist()) == len(set(z.namelist())), 'duplicate ZIP entries'
        assert sum(x.file_size for x in z.infolist()) <= 100_000_000, 'unexpected artifact size'
        files = {}
        for info in z.infolist():
            name = PurePosixPath(info.filename)
            assert not name.is_absolute() and '..' not in name.parts and '\\' not in str(name)
            assert not stat.S_ISLNK(info.external_attr >> 16), 'symlink in artifact'
            if not info.is_dir():
                assert str(name) == info.filename, 'noncanonical ZIP path'
                files[str(name)] = z.read(info)
        return files


def materialize(files, directory):
    directory.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        path = directory / name
        assert not path.is_symlink(), 'symlink in evidence directory'
        if path.exists():
            assert path.read_bytes() == data, 'existing evidence differs'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    local = {p.relative_to(directory).as_posix(): p.read_bytes()
             for p in directory.rglob('*') if p.is_file()}
    assert local == files, 'extracted evidence set differs from ZIP'


def authenticate_project(repo, head, commit, project_id, files, directory, context):
    REPO, HEAD = str(repo), head
    git = git_command(repo)
    name = 'lean-' + project_id
    project = PROJECTS[project_id]
    standard = STANDARD
    paths = [p for p in files if PurePosixPath(p).name == 'result.json']
    assert len(paths) == 1, 'expected exactly one result manifest per artifact'
    resultpath = directory / paths[0]
    d = json.loads(files[paths[0]])
    assert d['project'] == project
    assert d['repository_commit'] == commit and d['result'] == 'comparator-accepted'
    lock, locksha, probe = context['lock'], context['lock_sha'], context['probe_sha']
    tr = d['tool_receipt']
    assert d['source_lock_sha256'] == locksha == tr['source_lock_sha256']
    assert tr['forsythe_commit'] == lock['commit']
    assert tr['lean_toolchain'] == lock['lean_toolchain']
    assert tr['ci_sandbox_probe_sha256'] == probe
    assert tr['lean_version'] == ('Lean (version 4.33.1, x86_64-unknown-linux-gnu, '
        'commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)')
    assert tr['platform'].startswith('Linux-')
    assert tr['go_version'] == 'go version go1.27.1 linux/amd64'
    assert set(tr['executables']) == {'.tools/comparator/.lake/build/bin/comparator',
        '.tools/lean4export/.lake/build/bin/lean4export', '.tools/bin/landrun'}
    assert all(re.fullmatch('[a-f0-9]{64}', x) for x in tr['executables'].values())
    assert re.fullmatch('[a-f0-9]{64}', tr['env_sha256'])
    # The source-manifest and actual-log checks below are adapted from the
    # already exercised PR194 and five-upstream-artifact authenticators.
    cfg=json.loads(git('show',HEAD+':'+project+'/comparator.json'));assert len(cfg['theorem_names']) == EXPECTED_EXPORT_COUNTS[project_id];assert d['config']==cfg and set(cfg['permitted_axioms'])==standard and cfg['definition_names']==[]
    entries=[]
    for item in git('ls-tree','-r','-z',HEAD,'--',project).split(b'\0'):
     if not item:continue
     header,path=item.split(b'\t');mode,typ,obj=header.decode().split();path=path.decode();assert typ=='blob' and mode in ['100644','100755'];entries.append((path[len(project)+1:],obj))
    assert set(p for p,o in entries)==set(d['input_sha256'])
    objects=list(dict.fromkeys(o for p,o in entries))
    out=subprocess.check_output(['git','-C',REPO,'cat-file','--batch'],input=('\n'.join(objects)+'\n').encode());pos=0;byobj={}
    for obj in objects:
     e=out.index(b'\n',pos);header=out[pos:e].decode().split();assert header[0]==obj and header[1]=='blob';length=int(header[2]);content=out[e+1:e+1+length];assert out[e+1+length:e+2+length]==b'\n';pos=e+2+length;byobj[obj]=content
    assert pos==len(out)
    for p,o in entries:assert sha(byobj[o])==d['input_sha256'][p],(name,p)
    contents={p:byobj[o] for p,o in entries}
    assert contents['lean-toolchain'].decode().strip()==lock['lean_toolchain']
    logs={p.name:p.read_text() for p in resultpath.parent.glob('*.log')}
    def contains(log,*markers):
     for marker in markers:assert marker in logs[log],(name,log,marker)
    contains('comparator.log','Building Challenge','Building Solution','Running Lean default kernel on solution.','Lean default kernel accepts the solution','Your solution is okay!','EXIT_STATUS=0','nla-fresh-proof-','RestrictAddressFamilies=~AF_UNIX','strict_landrun.py')
    cl=logs['comparator.log'];assert 'Illegal axiom detected' not in cl and 'Lean default kernel rejects' not in cl
    for mod in ['Challenge','Solution']:
     exports=re.findall(r'Exporting #\[(.*?)\] from '+mod+r'\n',cl);assert len(exports)==1
     own=[s.strip() for s in exports[0].split(',') if s.strip().startswith('NLA.')];assert own==cfg['theorem_names']
    ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",cl)
    reports=re.findall(r"info: ([^:\n]+):([0-9]+):[0-9]+: '([^']+)' depends on axioms: \[([^\]]*)\]",cl)
    assert len(reports)==len(ax)
    for filename,lineno,full_name,axioms in reports:
     line=contents[filename].decode().splitlines()[int(lineno)-1].strip()
     assert line.startswith('#print axioms ')
     printed=line.split()[-1]
     assert full_name==printed or full_name.endswith('.'+printed)
    for n,axs in ax:assert set(v.strip() for v in axs.split(',') if v.strip())<=standard,(name,n,axs)
    assert set(cfg['theorem_names'])<=set(n for n,a in ax)
    contains('kernel-controls.log','RETURN honest_with_inductives_and_quotients: accepted','RETURN invalid_raw_proof: rejected:','(kernel) declaration type mismatch','RETURN quotient_postcheck_mismatch: rejected: Quotient constant mismatch on: Quot.lift','PASS: all three actual Comparator.runBuiltinKernel cases behaved as required','EXIT_STATUS=0')
    contains('comparator-controls.log','PASS simple_match: exit 0, expected 0','PASS simple_mismatch: exit 1, expected 1','PASS simple_axiom_issue: exit 1, expected 1','PASS simple_kind_mismatch: exit 1, expected 1','PASS type_mismatch: exit 1, expected 1','PASS: all five Comparator regressions','EXIT_STATUS=0')
    # Bind each control to its actual transcript, not merely a PASS summary.
    regression_phases = {
        'simple_match': ('Running Lean default kernel on solution.', 'Lean default kernel accepts the solution', 'Your solution is okay!'),
        'simple_mismatch': ("uncaught exception: Challenge and solution constant kind don't match: 'comm'",),
        'simple_axiom_issue': ("uncaught exception: Illegal axiom detected: 'helper'",),
        'simple_kind_mismatch': ("uncaught exception: Illegal axiom detected: 'helper'",),
        'type_mismatch': ("uncaught exception: Challenge and solution theorem statement do not match: 'checked'",),
    }
    for case, phases in regression_phases.items():
        sections = logs['comparator-controls.log'].split('CASE ' + case + '\n')
        assert len(sections) == 2, (name, 'duplicate/missing control', case)
        actual = sections[1].split('PASS ' + case + ':', 1)[0]
        assert actual.count('Building Challenge') == actual.count('Building Solution') == 1
        for phase in phases:
            assert phase in actual, (name, 'missing actual control phase', case, phase)
    for case, phase in {
        'honest_with_inductives_and_quotients': 'Lean default kernel accepts the solution',
        'invalid_raw_proof': 'Lean default kernel rejects the solution',
        'quotient_postcheck_mismatch': 'Quotient post-check rejects the solution',
    }.items():
        sections = logs['kernel-controls.log'].split('BEGIN ' + case + '\n')
        assert len(sections) == 2, (name, 'duplicate/missing replay control', case)
        actual = sections[1].split('RETURN ' + case + ':', 1)[0]
        assert 'Running Lean default kernel on solution.' in actual and phase in actual
    for log,axiom in [('negative-sorry.log','sorryAx'),('negative-native.log','checked._native.native_decide.ax_1_1')]:contains(log,'Building Challenge','Building Solution',"Illegal axiom detected: '"+axiom+"'",'EXIT_STATUS=1','RestrictAddressFamilies=~AF_UNIX','strict_landrun.py')
    contains('user-service.log','RestrictAddressFamilies=~AF_UNIX','/usr/bin/true','EXIT_STATUS=0')
    sl=logs['sandbox.log']
    common=['outside .lake write-open: denied','outside .lake truncate: denied','outside .lake read-only truncate-open: denied','symlink from .lake to outside write: denied','outside .lake creation: denied','user namespace: private','pid namespace: private','mnt namespace: private','net namespace: private','ipc namespace: private','uts namespace: private','host parent: absent from private /proc','host parent signal lookup: denied','host loopback listener: unreachable','AF_UNIX socket creation: denied','effective capabilities: none','no_new_privs: set','nested namespace write attempt: rejected exit=1']
    for marker in common:assert sl.count('PASS '+marker)==2,(name,marker)
    contains('sandbox.log','MODE build: exit=0','MODE export: exit=0','PASS build .lake write: allowed','PASS export .lake write-open: denied','PASS export .lake truncate: denied','NEGATIVE unknown option: exit=2','NEGATIVE unexpected --rw: exit=2','NEGATIVE unexpected --rwx: exit=2','NEGATIVE relative --rwx: exit=2','Outer and export fixture contents unchanged; only designated build fixture written.','EXIT_STATUS=0')
    assert re.findall(r'Sandbox UID: (\d+)',sl)==['1001','1001']
    return {'name': name, 'project': project, 'repository_commit': commit,
        'complete_git_tracked_set': True, 'all_input_hashes_match': True,
        'input_hashes': len(entries), 'input_manifest_sha256': sha(json.dumps(
            d['input_sha256'], sort_keys=True, separators=(',', ':')).encode()),
        'theorem_exports': cfg['theorem_names'], 'standard_axiom_reports': len(ax),
        'axiom_report_names': [n for n, _ in ax], 'default_kernel': 'accepted',
        'source_lock_sha256': locksha, 'tool_receipt': tr,
        'kernel_actual_cases': 3, 'comparator_actual_regressions': 5,
        'admitted_proof_rejection': True, 'native_decision_rejection': True,
        'sandbox_actual_modes': 2, 'sandbox_rejected_options': 4,
        'archive_bytes_match': True, 'config_matches': True,
        'logs_sha256': {k: sha(v.encode()) for k, v in logs.items()}, 'result': 'PASS'}


def main(args):
    assert __debug__, 'do not run authentication with Python -O'
    for value in (args.head, args.base):
        assert re.fullmatch('[a-f0-9]{40}', value), 'head/base must be full lowercase SHAs'
    projects = {key: PROJECTS[key] for key in (args.project or PROJECTS)}
    assert len(projects) == len(args.project or PROJECTS), 'duplicate project selection'
    root = Path(args.output or f'/private/tmp/nla-pr{args.pr}-final-ci')
    root.mkdir(parents=True, exist_ok=True)
    git = git_command(args.repo)
    tree = git('rev-parse', args.head + '^{tree}').decode().strip()
    subprocess.run(['git', '-C', args.repo, 'merge-base', '--is-ancestor', args.base, args.head],
                   check=True, timeout=60)
    pr = api(f'repos/{GITHUB}/pulls/{args.pr}', root / 'pr.json')
    assert pr['number'] == args.pr and pr['base']['repo']['id'] == REPOSITORY_ID
    assert pr['head']['sha'] == args.head and pr['base']['sha'] == args.base
    assert pr['base']['repo']['full_name'] == GITHUB
    assert pr['merge_commit_sha'], 'PR synthetic merge commit not ready'
    if args.run_id:
        run = api(f'repos/{GITHUB}/actions/runs/{args.run_id}', root / 'run.json')
    else:
        runs = paged(f'repos/{GITHUB}/actions/workflows/lean-verification.yml/runs?'
                     f'event=pull_request&head_sha={args.head}', 'workflow_runs', root / 'runs.json')
        assert runs, 'no pull_request Lean workflow for supplied head'
        latest = max(runs, key=lambda x: x['id'])
        run = api(f'repos/{GITHUB}/actions/runs/{latest["id"]}', root / 'run.json')
    assert run['status'] == 'completed' and run['conclusion'] == 'success', \
        'exact workflow has not completed successfully'
    assert run['event'] == 'pull_request' and run['head_sha'] == args.head
    assert run['path'] == WORKFLOW and run['repository']['full_name'] == GITHUB
    assert run['repository']['id'] == REPOSITORY_ID
    run_id = run['id']
    jobs = paged(f'repos/{GITHUB}/actions/runs/{run_id}/jobs?filter=all', 'jobs', root / 'jobs.json')
    artifacts = paged(f'repos/{GITHUB}/actions/runs/{run_id}/artifacts', 'artifacts',
                      root / 'artifacts.json')
    assert len(artifacts) == len(projects) and {a['name'] for a in artifacts} == \
        {'lean-' + p for p in projects}, 'artifacts differ from explicit expected project set'
    mc = api(f'repos/{GITHUB}/git/commits/{pr["merge_commit_sha"]}', root / 'checked-commit.json')
    commit = checked_commit(mc, args.base, args.head, tree)
    probe_json = root / 'pinned-sandbox-probe.json'
    lock = json.loads(git('show', args.head + ':tools/lean/source-lock.json'))
    entry = next(x for x in lock['files'] if x['source'].endswith('/sandbox_probe.py'))
    api('repos/sgstepaniants/Forsythe/contents/' + entry['source'] + '?ref=' + lock['commit'], probe_json)
    context = tool_context(args.repo, args.head, args.base, probe_json)
    results = []
    for project_id, project in projects.items():
        a = next(a for a in artifacts if a['name'] == 'lean-' + project_id)
        arun = a['workflow_run']
        assert not a['expired'] and arun['id'] == run_id and arun['head_sha'] == args.head
        assert arun['repository_id'] == REPOSITORY_ID
        assert arun['head_repository_id'] == pr['head']['repo']['id']
        candidates = [j for j in jobs if j['name'] == f'verify ({project_id}, {project})'
            and j['status'] == 'completed' and j['conclusion'] == 'success'
            and j['head_sha'] == args.head and j['started_at'] <= a['created_at'] <= j['completed_at']]
        assert len(candidates) == 1, 'artifact does not bind to one successful verification job'
        job = candidates[0]
        for title in ('Validate formalization manifest',
                      'Fresh sandboxed statement, axiom and kernel verification',
                      'Retain verification logs'):
            steps = [s for s in job['steps'] if s['name'] == title]
            assert len(steps) == 1 and steps[0]['conclusion'] == 'success', title
        zpath = root / f'{a["name"]}-{a["id"]}.zip'
        if not zpath.exists():
            api(f'repos/{GITHUB}/actions/artifacts/{a["id"]}/zip', zpath, binary=True)
        files = archive_members(zpath, a)
        directory = root / f'{a["name"]}-{a["id"]}'
        materialize(files, directory)
        result = authenticate_project(args.repo, args.head, commit, project_id, files, directory, context)
        result.update({'artifact_id': a['id'], 'artifact_digest': a['digest'],
            'run_id': run_id, 'job_id': job['id'], 'job_run_attempt': job['run_attempt']})
        results.append(result)
        print(json.dumps({k: result[k] for k in ('name', 'input_hashes', 'standard_axiom_reports', 'result')}),
              flush=True)
    # Detect PR or run changes during downloads before issuing an overall PASS.
    last_pr = api(f'repos/{GITHUB}/pulls/{args.pr}', root / 'pr-final-snapshot.json')
    last_run = api(f'repos/{GITHUB}/actions/runs/{run_id}', root / 'run-final-snapshot.json')
    assert last_pr['head']['sha'] == args.head and last_pr['base']['sha'] == args.base
    assert last_pr['merge_commit_sha'] == commit
    assert last_run['run_attempt'] == run['run_attempt']
    assert last_run['status'] == 'completed' and last_run['conclusion'] == 'success'
    evidence = {'result': 'PASS', 'pr': args.pr, 'head': args.head, 'base': args.base,
        'tree': tree, 'pr_checked_commit': commit, 'checked_commit_parents': [args.base, args.head],
        'run_id': run_id, 'run_attempt': run['run_attempt'], 'workflow_event': run['event'],
        'shared_checker_unchanged_from_base_and_reviewed_anchor': True,
        'authenticator_sha256': sha(Path(__file__).read_bytes()), 'artifacts': results}
    save_json(root / 'artifact-authentication.json', evidence)
    print(str(root / 'artifact-authentication.json'), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pr', type=int, required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--base', required=True)
    parser.add_argument('--repo', default='/private/tmp/nla-integration-246-249')
    parser.add_argument('--run-id', type=int)
    parser.add_argument('--project', action='append', choices=sorted(PROJECTS))
    parser.add_argument('--output')
    parsed = parser.parse_args()
    try:
        main(parsed)
    except (AssertionError, KeyError, ValueError, subprocess.SubprocessError) as exc:
        print(f'AUTHENTICATION FAILED: {type(exc).__name__}: {exc}', file=sys.stderr)
        raise SystemExit(1)
