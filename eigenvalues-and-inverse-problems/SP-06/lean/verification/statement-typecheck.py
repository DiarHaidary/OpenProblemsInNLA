"""Typecheck statements into a fresh private prefix using existing pinned objects.

No Lake invocation, dependency download, shared cache build or write is used.
This local statement check is not a mathematical proof or Linux Comparator run.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

project = Path(__file__).resolve().parents[1]
deps = Path(os.environ['SP06_DEP_ROOT'])
sysroot = Path(os.environ.get('LEAN_SYSROOT', str(Path.home() / '.elan/toolchains/leanprover--lean4---v4.33.1')))
lean = sysroot / 'bin/lean'
prefix = Path(tempfile.mkdtemp(prefix='nla-sp06-statement-typecheck-'))
out = prefix / 'objects'
(out / 'NLA/SP06').mkdir(parents=True)
record = {'phase': 'statements only', 'project': str(project), 'commands': [], 'dependencies': {}}

def run(args, *, cwd=project, env=None, log=None):
    result = subprocess.run([str(a) for a in args], cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    record['commands'].append({'argv': [str(a) for a in args], 'cwd': str(cwd), 'exit_code': result.returncode, 'output': result.stdout.decode()})
    if log:
        (prefix / log).write_bytes(result.stdout)
    if result.returncode:
        (prefix / 'EVIDENCE.json').write_text(json.dumps(record, indent=2) + '\n')
        print(result.stdout.decode())
        raise SystemExit(f'FAILED; evidence {prefix}')
    return result.stdout.decode()

assert 'Lean (version 4.33.1' in run([lean, '--version'])
manifest = json.loads((project / 'lake-manifest.json').read_text())
for package in manifest['packages']:
    name = package['name']
    head = run(['git', 'rev-parse', 'HEAD'], cwd=deps / name).strip()
    status = run(['git', 'status', '--porcelain=1', '--untracked-files=no'], cwd=deps / name)
    assert head == package['rev'] and not status, name
    record['dependencies'][name] = {'revision': head, 'tracked_sources_clean': True}

env = os.environ.copy()
env['LEAN_PATH'] = ':'.join([str(out)] + [str(deps / p['name'] / '.lake/build/lib/lean') for p in manifest['packages']] + [str(sysroot / 'lib/lean')])
record['lean_path'] = env['LEAN_PATH']
record['source_hashes'] = {p: hashlib.sha256((project / p).read_bytes()).hexdigest() for p in ['NLA/SP06/Definitions.lean', 'Challenge.lean']}
run([lean, '-R', project, '-o', out / 'NLA/SP06/Definitions.olean', project / 'NLA/SP06/Definitions.lean'], env=env, log='Definitions.log')
run([lean, '-R', project, '-o', out / 'Challenge.olean', project / 'Challenge.lean'], env=env, log='Challenge.log')
record['result'] = 'PASS: local elaboration of definitions and intentional statement placeholders only'
(prefix / 'EVIDENCE.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'result': record['result'], 'evidence': str(prefix)}))
