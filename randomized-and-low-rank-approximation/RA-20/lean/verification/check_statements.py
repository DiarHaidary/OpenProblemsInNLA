"""Direct statement-only elaboration against immutable read-only dependency objects.

No Lake invocation, download, cached project object or proof implementation.
All attempts and their exact source/log bytes are retained. One private prefix
is reused after hashing and removing only this script's own generated objects.
"""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, tempfile, time

P = Path(__file__).resolve().parents[1]
E = P / 'verification' / 'statement-checks'
E.mkdir(exist_ok=True)
C = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
L = Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
state = E / 'prefix.json'
if state.exists():
    prefix = Path(json.loads(state.read_text())['prefix'])
else:
    prefix = Path(tempfile.mkdtemp(prefix='ra20-statements-', dir='/tmp/nla-lean-formalization/independent-prefixes'))
    state.write_text(json.dumps({'prefix': str(prefix)}, indent=2) + '\n')
assert prefix.parent == Path('/tmp/nla-lean-formalization/independent-prefixes')
assert prefix.name.startswith('ra20-statements-')
removed = []
for f in sorted(prefix.rglob('*')):
    if f.is_file():
        assert f.suffix in {'.olean', '.ilean'}
        removed.append({'path': str(f.relative_to(prefix)), 'sha256': sha(f), 'bytes': f.stat().st_size})
        f.unlink()
pins = []
for d in json.loads((P / 'lake-manifest.json').read_text())['packages']:
    dep = C / d['name']
    rev = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=dep).decode().strip()
    assert rev == d['rev']
    assert not subprocess.check_output(['git', 'status', '--porcelain=v1'], cwd=dep)
    pins.append({'name': d['name'], 'rev': rev, 'git_clean': True})
order = ['Cli', 'batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph', 'LeanSearchClient', 'plausible', 'mathlib', 'leancert']
env = os.environ.copy()
env['LEAN_PATH'] = ':'.join(map(str, [prefix, *[C / n / '.lake/build/lib/lean' for n in order], L / 'lib/lean']))
attempt = Path(tempfile.mkdtemp(prefix='attempt-', dir=E))
record = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'scope': 'macOS author statement elaboration only; no implementation or Linux Comparator',
          'prefix': str(prefix), 'LEAN_PATH': env['LEAN_PATH'], 'pins': pins,
          'removed_prior_owned_object_hashes': removed, 'commands': [], 'result': 'RUNNING'}
inputs = ['NLA/RA20/Definitions.lean', 'Challenge.lean', 'verification/InspectStatements.lean']
source_hashes = {name: sha(P / name) for name in inputs}
(attempt / 'check_statements.py.txt').write_bytes(Path(__file__).read_bytes())
try:
    for name in inputs:
        source = P / name
        out = prefix / Path(name).with_suffix('.olean')
        out.parent.mkdir(parents=True, exist_ok=True)
        (attempt / (name.replace('/', '-') + '.txt')).write_bytes(source.read_bytes())
        cmd = [str(L / 'bin/lean'), '-o', str(out), '-i', str(out.with_suffix('.ilean')), str(source)]
        start = time.monotonic()
        run = subprocess.run(cmd, cwd=P, env=env, capture_output=True)
        log = attempt / name.replace('/', '-').replace('.lean', '.log')
        log.write_bytes(run.stdout + run.stderr)
        row = {'source': name, 'source_sha256': sha(source), 'command': cmd,
               'exit_code': run.returncode, 'seconds': time.monotonic() - start,
               'log': log.name, 'log_sha256': sha(log)}
        record['commands'].append(row)
        (attempt / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
        print(name, run.returncode, round(row['seconds'], 2), flush=True)
        if run.returncode:
            print(log.read_text()[-20000:], flush=True)
        assert run.returncode == 0, log
        text = log.read_text()
        if name == 'Challenge.lean':
            assert text.count('warning: declaration uses `sorry`') == 12
            assert text.count('warning:') == 12
        else:
            assert 'warning:' not in text and 'error:' not in text
        reports = re.findall(r"'([^']+)' depends on axioms:\s*\[(.*?)\]", text, re.S)
        for decl, axioms in reports:
            assert {a.strip() for a in axioms.split(',')} - {''} <= {'propext', 'Classical.choice', 'Quot.sound'}, (decl, axioms)
        row['definition_kernel_axiom_reports'] = len(reports)
    assert not (P / 'Solution.lean').exists()
    assert not list((P / 'NLA').rglob('Proof.lean'))
    assert source_hashes == {name: sha(P / name) for name in inputs}
    for d in pins:
        dep = C / d['name']
        assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=dep).decode().strip() == d['rev']
        assert not subprocess.check_output(['git', 'status', '--porcelain=v1'], cwd=dep)
    record['inputs_unchanged_throughout_run'] = source_hashes
    record['ten_pins_rechecked_after_run'] = True
    record['result'] = 'PASS'
finally:
    record['objects'] = [{'path': str(f.relative_to(prefix)), 'sha256': sha(f), 'bytes': f.stat().st_size}
                         for f in sorted(prefix.rglob('*')) if f.is_file()]
    (attempt / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    (E / 'latest.json').write_text(json.dumps({'attempt': str(attempt), 'result_sha256': sha(attempt / 'result.json')}, indent=2) + '\n')
print(attempt, record['result'], flush=True)
