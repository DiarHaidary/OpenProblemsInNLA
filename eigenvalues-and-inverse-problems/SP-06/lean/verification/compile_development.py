"""Compile the requested SP-06 source prefix into fresh private objects.

Development only. This never imports Challenge, runs Lake, downloads files,
or writes shared dependency objects. Actual Linux/Comparator remains a later
gate. Existing pinned dependency objects are read, not rebuilt here.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

project = Path(__file__).resolve().parents[1]
order = ['NLA.SP06.Definitions', 'NLA.SP06.Numeric', 'NLA.SP06.Curve', 'NLA.SP06.Proof', 'Solution']
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('through', choices=order)
args = parser.parse_args()
modules = order[:order.index(args.through) + 1]
deps = Path(os.environ['SP06_DEP_ROOT'])
sysroot = Path(os.environ.get('LEAN_SYSROOT', str(Path.home() / '.elan/toolchains/leanprover--lean4---v4.33.1')))
lean = sysroot / 'bin/lean'
prefix = Path(tempfile.mkdtemp(prefix='nla-sp06-development-'))
out = prefix / 'objects'
out.mkdir()
evidence = {'phase': 'proof development', 'started_utc': datetime.now(timezone.utc).isoformat(), 'project': str(project), 'commands': [], 'sources': {}, 'dependencies': {}}

def save():
    (prefix / 'EVIDENCE.json').write_text(json.dumps(evidence, indent=2) + '\n')

def run(argv, *, cwd=project, env=None, log=None):
    completed = subprocess.run([str(a) for a in argv], cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    item = {'argv': [str(a) for a in argv], 'cwd': str(cwd), 'exit_code': completed.returncode, 'output': completed.stdout.decode()}
    if log:
        (prefix / log).write_bytes(completed.stdout)
        item['log'] = log
    evidence['commands'].append(item)
    save()
    if completed.returncode:
        print(completed.stdout.decode())
        raise SystemExit(f'FAILED; all command results retained at {prefix}')
    return completed.stdout.decode()

assert 'Lean (version 4.33.1' in run([lean, '--version'])
manifest = json.loads((project / 'lake-manifest.json').read_text())
for package in manifest['packages']:
    name = package['name']
    head = run(['git', 'rev-parse', 'HEAD'], cwd=deps / name).strip()
    clean = not run(['git', 'status', '--porcelain=1', '--untracked-files=no'], cwd=deps / name)
    assert head == package['rev'] and clean, name
    evidence['dependencies'][name] = {'revision': head, 'tracked_sources_clean': clean}

env = os.environ.copy()
env['LEAN_PATH'] = ':'.join([str(out)] + [str(deps / p['name'] / '.lake/build/lib/lean') for p in manifest['packages']] + [str(sysroot / 'lib/lean')])
evidence['lean_path'] = env['LEAN_PATH']
for module in modules:
    rel = module.replace('.', '/') + '.lean'
    source = project / rel
    target = out / (module.replace('.', '/') + '.olean')
    target.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    evidence['sources'][rel] = digest
    run([lean, '-R', project, '-o', target, source], env=env, log=module + '.log')
    assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
evidence['result'] = 'PASS: requested development modules elaborated; not an independent review or Linux result'
evidence['finished_utc'] = datetime.now(timezone.utc).isoformat()
save()
print(json.dumps({'result': evidence['result'], 'modules': modules, 'evidence': str(prefix)}))
