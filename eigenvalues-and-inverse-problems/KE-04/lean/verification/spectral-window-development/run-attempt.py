#!/usr/bin/env python3
"""Fresh local source builds only; all pinned package objects remain read-only.

Executed development driver, not a portable retrospective verifier. Every
invocation creates and later removes only its own fresh private prefix.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

P = Path(__file__).resolve().parents[2]
E = P / 'verification/spectral-window-development'
T = Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
C = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
FREEZE = '85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e'
GATE = '5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n')

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inspect', action='store_true')
    args = ap.parse_args()
    prefix = Path(tempfile.mkdtemp(prefix='ke04-spectral-window-'))
    attempt = E / ('attempt-' + prefix.name.removeprefix('ke04-spectral-window-'))
    attempt.mkdir()
    (prefix / 'lib').mkdir()
    assert not list((prefix / 'lib').rglob('*'))
    commands = []
    env = os.environ.copy()
    env['GIT_OPTIONAL_LOCKS'] = '0'
    def run(argv, label, cwd=P, cmd_env=env):
        start = utc()
        result = subprocess.run([str(v) for v in argv], cwd=cwd, env=cmd_env,
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (attempt / (label + '.stdout')).write_text(result.stdout)
        (attempt / (label + '.stderr')).write_text(result.stderr)
        commands.append({'argv': [str(v) for v in argv], 'cwd': str(cwd),
                         'started_utc': start, 'finished_utc': utc(), 'exit': result.returncode,
                         'stdout': label + '.stdout', 'stderr': label + '.stderr',
                         'LEAN_PATH': cmd_env.get('LEAN_PATH'),
                         'GIT_OPTIONAL_LOCKS': cmd_env.get('GIT_OPTIONAL_LOCKS')})
        write(attempt / 'commands.json', commands)
        return result
    frozen = json.loads((P / 'reviews/statement-freeze.json').read_text())
    assert sha(P / 'reviews/statement-freeze.json') == FREEZE
    assert sha(P / 'verification/proof-start.json') == GATE
    assert len(frozen['files']) == 1598
    assert json.loads((P / 'verification/proof-start.json').read_text())['proof_authorized'] is True

    imported_seals = {
        'verification/frames-development/EVIDENCE-MANIFEST.json': '73770debb7678e443032c5f30e77ef82365cd32b81d24bba161990e2ac7f8db8',
        'verification/spectral-development/EVIDENCE-MANIFEST.json': '27a8328c569a17db1e6cf671a0a79034e3ce9eb2dc85c4640d13be7624191ca2'}
    def imported(phase):
        union = {}
        for seal, expected in imported_seals.items():
            assert sha(P / seal) == expected, seal
            union[seal] = expected
            d = json.loads((P / seal).read_text())
            for r, v in d['files'].items():
                assert sha(P / r) == v['sha256'], r
                if r in union:
                    assert union[r] == v['sha256'], r
                union[r] = v['sha256']
        write(attempt / ('imported-' + phase + '.json'),
              {'seals': imported_seals, 'all_match': True, 'bound_files': len(union)})
    imported('before')
    sources = ['NLA/KE04/Definitions.lean', 'NLA/KE04/Frames.lean', 'NLA/KE04/Spectral.lean', 'NLA/KE04/SpectralWindow.lean',
               'Challenge.lean', 'NUMERICAL_TARGETS.md', 'SourceCorrespondence.md',
               'lake-manifest.json', 'lakefile.toml', 'lean-toolchain',
               'reviews/statement-freeze.json', 'verification/proof-start.json']
    if args.inspect:
        sources.append('verification/spectral-window-development/Inspect.lean')
    sources.append('verification/spectral-window-development/run-attempt.py')
    before = {r: sha(P / r) for r in sources}
    for r in sources:
        dst = attempt / 'inputs' / r
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(P / r, dst)
    for r, h in frozen['files'].items():
        assert sha(P / r) == h, r
    write(attempt / 'frozen-before.json', {'checked': 1598, 'freeze_sha256': FREEZE,
                                          'all_match': True})
    write(attempt / 'source-before.json', before)
    write(attempt / 'prefix.json', {'path': str(prefix), 'initial_output_files': [],
                                   'source_copies_only': True, 'utc': utc()})
    packages = json.loads((P / 'lake-manifest.json').read_text())['packages']
    def pins(phase):
        info = []
        for pkg in packages:
            d = C / pkg['name']
            head = run(['git', '-c', 'core.fsmonitor=false', 'rev-parse', 'HEAD'],
                       phase + '-' + pkg['name'] + '-head', d)
            status = run(['git', '-c', 'core.fsmonitor=false', 'status', '--porcelain',
                          '--untracked-files=all'], phase + '-' + pkg['name'] + '-status', d)
            assert head.returncode == 0 and head.stdout.strip() == pkg['rev'], pkg['name']
            assert status.returncode == 0 and not status.stdout, pkg['name']
            info.append({'name': pkg['name'], 'directory': str(d), 'revision': pkg['rev'],
                         'clean': True, 'build_objects_present': (d / '.lake/build/lib/lean').is_dir()})
        write(attempt / ('pins-' + phase + '.json'), info)
        return info
    info = pins('before')
    paths = [prefix / 'lib'] + [C / d['name'] / '.lake/build/lib/lean'
                               for d in info if d['build_objects_present']] + [T / 'lib/lean']
    assert len(paths) == 11 and len(info) == 10
    assert next(d for d in info if d['name'] == 'Cli')['build_objects_present'] is False
    env['LEAN_PATH'] = ':'.join(map(str, paths))
    version = run([T / 'bin/lean', '--version'], 'lean-version')
    assert version.returncode == 0
    write(attempt / 'toolchain.json', {'lean': str(T / 'bin/lean'), 'sha256': sha(T / 'bin/lean'),
                                      'version': version.stdout.strip(), 'LEAN_PATH': list(map(str, paths))})
    modules = [('NLA/KE04/Definitions.lean', 'NLA/KE04/Definitions'),
               ('NLA/KE04/Frames.lean', 'NLA/KE04/Frames'),
               ('NLA/KE04/Spectral.lean', 'NLA/KE04/Spectral'),
               ('NLA/KE04/SpectralWindow.lean', 'NLA/KE04/SpectralWindow')]
    if args.inspect:
        modules.append(('verification/spectral-window-development/Inspect.lean', 'Inspect'))
    compile_records = []
    for r, mod in modules:
        source = prefix / 'src' / (mod + '.lean')
        source.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(attempt / 'inputs' / r, source)
        output = prefix / 'lib' / (mod + '.olean')
        output.parent.mkdir(parents=True, exist_ok=True)
        result = run([T / 'bin/lean', '--root=' + str(prefix / 'src'),
                      '-o', output, '-i', output.with_suffix('.ilean'), source],
                     'compile-' + mod.replace('/', '-'), prefix / 'src')
        compile_records.append({'source': r, 'module': mod, 'exit': result.returncode})
        if result.returncode:
            break
    pins('after')
    imported('after')
    after = {r: sha(P / r) for r in sources}
    write(attempt / 'source-after.json', after)
    assert before == after
    for r, h in frozen['files'].items():
        assert sha(P / r) == h, r
    write(attempt / 'frozen-after.json', {'checked': 1598, 'freeze_sha256': FREEZE,
                                         'all_match': True})
    objects = {str(f.relative_to(prefix)): {'sha256': sha(f), 'bytes': f.stat().st_size}
               for f in sorted((prefix / 'lib').rglob('*')) if f.is_file()}
    write(attempt / 'objects.json', {'prefix': str(prefix), 'files': objects})
    for r, d in objects.items():
        assert sha(prefix / r) == d['sha256']
    shutil.rmtree(prefix)
    write(attempt / 'cleanup.json', {'prefix': str(prefix), 'all_own_object_hashes_matched': True,
                                    'objects': len(objects), 'removed': not prefix.exists(), 'utc': utc()})
    outcome = {'attempt': attempt.name, 'compile_commands': compile_records,
               'all_requested_compiles_pass': len(compile_records) == len(modules)
                 and all(d['exit'] == 0 for d in compile_records),
               'fresh_prefix': str(prefix), 'preserved_frozen_inputs': 1598,
               'unchanged_sources': True, 'local_execution_only': True,
               'Linux_Comparator_execution': False}
    write(attempt / 'result.json', outcome)
    print(json.dumps(outcome, indent=2))
    raise SystemExit(0 if outcome['all_requested_compiles_pass'] else 1)

if __name__ == '__main__':
    main()
