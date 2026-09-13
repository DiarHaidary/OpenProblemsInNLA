#!/usr/bin/env python3
"""Fresh scoped source elaboration. Never invokes Lake or writes shared dependencies."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

P = Path(__file__).resolve().parents[2]
E = Path(__file__).resolve().parent
TOOL = Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
PACKAGES = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
ORDER = ['Cli', 'batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph',
    'LeanSearchClient', 'plausible', 'mathlib', 'leancert']


def record(p):
    return {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}


def frozen():
    p = P / 'reviews/statement-freeze.json'
    assert record(p)['sha256'] == '85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e'
    f = json.loads(p.read_text())
    assert len(f['files']) == 1598
    for rel, h in f['files'].items():
        assert record(P / rel)['sha256'] == h, rel
    return len(f['files'])


def pins():
    result = []
    for p in json.loads((P / 'lake-manifest.json').read_text())['packages']:
        q = PACKAGES / p['name']
        rev = subprocess.check_output(['git', '-C', str(q), 'rev-parse', 'HEAD'], text=True).strip()
        dirty = subprocess.check_output(['git', '-C', str(q), 'status', '--porcelain', '--untracked-files=no'], text=True)
        assert rev == p['rev'] and not dirty, p['name']
        result.append({'name': p['name'], 'rev': rev, 'tracked_clean': True,
            'object_directory_present': (q / '.lake/build/lib/lean').is_dir()})
    assert len(result) == 10 and sum(p['object_directory_present'] for p in result) == 9
    return result


def main():
    inspect = '--inspect' in sys.argv
    modules = ['NLA/KE04/Definitions.lean', 'NLA/KE04/Frames.lean']
    if inspect:
        modules.append('verification/frames-development/Inspect.lean')
    extra = ['lean-toolchain', 'lakefile.toml', 'lake-manifest.json', 'comparator.json',
        'verification/proof-start.json', 'verification/frames-development/compile.py']
    assert record(P / 'verification/proof-start.json')['sha256'] == '5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624'
    before = frozen()
    before_pins = pins()
    attempt = Path(tempfile.mkdtemp(prefix='attempt-', dir=E))
    prefix = Path(tempfile.mkdtemp(prefix='nla-ke04-frames-', dir='/tmp'))
    inputs = {}
    for rel in modules + extra:
        target = attempt / 'source' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(P / rel, target)
        inputs[rel] = record(target)
    env = os.environ.copy()
    env['LEAN_PATH'] = ':'.join([str(prefix)] +
        [str(PACKAGES / n / '.lake/build/lib/lean') for n in ORDER] + [str(TOOL / 'lib/lean')])
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'phase': 'KE04 Frames scoped author source validation',
        'platform': subprocess.check_output(['uname', '-srm'], text=True).strip(),
        'toolchain': subprocess.check_output([str(TOOL / 'bin/lean'), '--version'], text=True).strip(),
        'fresh': True, 'inspect': inspect, 'prefix': str(prefix), 'inputs': inputs,
        'commands': [], 'lean_path': env['LEAN_PATH'], 'frozen_inputs_before': before,
        'pins_before': before_pins, 'independent_review': False, 'actual_linux_comparator': False}
    passed = True
    try:
        for rel in modules:
            target = prefix / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            argv = [str(TOOL / 'bin/lean'), '-o', str(target.with_suffix('.olean')),
                '-i', str(target.with_suffix('.ilean')), rel]
            start = time.monotonic()
            c = subprocess.run(argv, cwd=attempt / 'source', env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log = attempt / (Path(rel).stem + '.log')
            log.write_bytes(c.stdout)
            entry = {'source': rel, 'argv': argv, 'exit_code': c.returncode,
                'seconds': time.monotonic() - start, 'log': log.name, 'log_sha256': record(log)['sha256']}
            result['commands'].append(entry)
            print(json.dumps({'attempt': attempt.name, **entry}), flush=True)
            if c.returncode:
                print(c.stdout.decode(errors='replace'), flush=True)
                passed = False
                break
        result['pins_after'] = pins()
        result['frozen_inputs_after'] = frozen()
        result['source_unchanged'] = all(record(P / rel) == rec for rel, rec in inputs.items())
        result['pass'] = passed and result['source_unchanged']
    except BaseException as exc:
        result['pass'] = False
        result['runner_exception'] = repr(exc)
        raise
    finally:
        objects = {str(q.relative_to(prefix)): record(q) for q in prefix.rglob('*') if q.is_file()}
        assert all(n.endswith(('.olean', '.ilean')) for n in objects)
        result['own_object_cleanup'] = {'prefix': str(prefix), 'objects': objects}
        shutil.rmtree(prefix)
        result['own_object_cleanup']['removed'] = not prefix.exists()
        out = attempt / 'result.json'
        out.write_text(json.dumps(result, indent=2) + '\n')
        (E / 'latest.json').write_text(json.dumps({'attempt': attempt.name,
            'result_sha256': record(out)['sha256']}, indent=2) + '\n')
    print(json.dumps({'attempt': attempt.name, 'pass': result['pass']}))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
