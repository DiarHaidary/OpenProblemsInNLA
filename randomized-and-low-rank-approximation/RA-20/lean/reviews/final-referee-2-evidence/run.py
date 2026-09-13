#!/usr/bin/env python3
"""Independent referee 2: source rebuild and diagnostic inspection, not Comparator."""
import datetime, hashlib, json, os, pathlib, subprocess, time, sys

P = pathlib.Path(__file__).resolve().parents[2]
E = pathlib.Path(__file__).resolve().parent
G = P.parents[2]
O = pathlib.Path('/tmp/nla-lean-formalization/independent-prefixes/ra20-final-referee2')
L = pathlib.Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
C = pathlib.Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
ORDER = ['Cli', 'batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph',
         'LeanSearchClient', 'plausible', 'mathlib', 'leancert']

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def command(args, cwd, env=None, source=None):
    d = E / ('command-%03d' % (1 + len(list(E.glob('command-*')))))
    d.mkdir()
    r = {'utc': utc(), 'command': args, 'cwd': str(cwd)}
    if env is not None:
        r['LEAN_PATH'] = env['LEAN_PATH']
    if source is not None:
        r.update(source=str(source.relative_to(P)), sha256=digest(source))
        (d / 'source.lean').write_bytes(source.read_bytes())
    write(d / 'command.json', r)
    start = time.monotonic()
    with (d / 'raw.log').open('wb') as output:
        proc = subprocess.run(args, cwd=cwd, env=env, stdout=output, stderr=subprocess.STDOUT)
    r.update(exit_code=proc.returncode, seconds=time.monotonic() - start,
             output_sha256=digest(d / 'raw.log'))
    write(d / 'result.json', r)
    print(json.dumps({'path': str(d.relative_to(P)), 'command': args, 'exit_code': proc.returncode}), flush=True)
    if proc.returncode:
        raise RuntimeError((d / 'raw.log').read_text())
    return (d / 'raw.log').read_text()

def verify_inputs():
    fpath = P / 'verification/proof-freeze.json'
    assert digest(fpath) == 'f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f'
    f = json.loads(fpath.read_text())
    assert len(f['files']) == 521 and len(f['source_files']) == 16
    for name, sha in f['files'].items():
        assert digest(P / name) == sha, name
    for name, sha in f['source_files'].items():
        assert digest(G / name) == sha, name
        blob = command(['git', 'rev-parse', f['base'] + ':' + name], G).strip()
        assert blob == f['source_git_blobs'][name], name
    record = {'utc': utc(), 'frozen_files': len(f['files']),
              'original_sources': len(f['source_files']), 'proof_freeze_sha256': digest(fpath),
              'base': f['base'], 'original_git_blobs': f['source_git_blobs']}
    write(E / 'input-validation.json', record)

def check_pins():
    pins = json.loads((P / 'lake-manifest.json').read_text())['packages']
    assert len(pins) == 10
    data = []
    for pin in pins:
        name = pin['name']
        head = command(['git', 'rev-parse', 'HEAD'], C / name).strip()
        assert head == pin['rev'], name
        status = command(['git', 'status', '--porcelain', '--untracked-files=no'], C / name)
        assert not status.strip(), name
        data.append({'name': name, 'revision': head, 'tracked_status_clean': True})
    version = command([str(L / 'bin/lean'), '--version'], P)
    write(E / 'dependency-pins.json', {'utc': utc(), 'packages': data,
          'lean_version': version, 'objects_policy': 'Read-only existing pinned dependency objects; no dependency source rebuild claimed.'})

def make_diagnostics():
    original = (P / 'Challenge.lean').read_text()
    assert original.count('namespace NLA.RA20\n') == 1
    assert original.count('end NLA.RA20\n') == 1
    ref = original.replace('namespace NLA.RA20\n', 'namespace NLA.RA20.RefereeTwoContract\n').replace(
        'end NLA.RA20\n', 'end NLA.RA20.RefereeTwoContract\n')
    assert ref.replace('namespace NLA.RA20.RefereeTwoContract\n', 'namespace NLA.RA20\n').replace(
        'end NLA.RA20.RefereeTwoContract\n', 'end NLA.RA20\n') == original
    (E / 'Reference.lean').write_text(ref)
    names = json.loads((P / 'comparator.json').read_text())['theorem_names']
    assert len(names) == 12
    pairs = ',\n    '.join('(``%s, ``NLA.RA20.RefereeTwoContract.%s)' % (name, name.split('.')[-1]) for name in names)
    body = (E / 'Inspect.template').read_text().replace('PAIRS_HERE', pairs)
    body += '\n' + '\n'.join('#assert_trust kernel ' + n + '\n#print axioms ' + n for n in names) + '\n'
    (E / 'Inspect.lean').write_text(body)
    write(E / 'diagnostic-source.json', {'utc': utc(), 'challenge_sha256': digest(P / 'Challenge.lean'),
        'reference_sha256': digest(E / 'Reference.lean'), 'namespace_only_reversible': True,
        'inspection_sha256': digest(E / 'Inspect.lean'), 'exports': names,
        'Comparator': 'Not run here; in-environment namespace-reference type diagnostic only.'})

def compile_all():
    assert not O.exists(), 'Owned prefix must be genuinely new and empty'
    O.mkdir(parents=True)
    write(E / 'prefix-created.json', {'utc': utc(), 'prefix': str(O), 'initial_files': [],
          'no_target_or_dependency_objects_copied': True})
    env = os.environ.copy()
    env['LEAN_PATH'] = ':'.join(map(str, [O, *[C / n / '.lake/build/lib/lean' for n in ORDER], L / 'lib/lean']))
    sources = ['NLA/RA20/' + n + '.lean' for n in
               ['Definitions', 'Algebra', 'SmoothTransport', 'Smooth', 'Tangent',
                'Differential', 'Generic', 'Critical', 'Count', 'Proof']]
    sources += ['Solution.lean', str((E / 'Reference.lean').relative_to(P)),
                str((E / 'Inspect.lean').relative_to(P))]
    for name in sources:
        source = P / name
        out = O / pathlib.Path(name).with_suffix('')
        out.parent.mkdir(parents=True, exist_ok=True)
        args = [str(L / 'bin/lean'), '-o', str(out.with_suffix('.olean')),
                '-i', str(out.with_suffix('.ilean')), name]
        command(args, P, env, source)
    write(E / 'build-complete.json', {'utc': utc(), 'source_modules': sources,
          'count': len(sources), 'result': 'PASS'})

if __name__ == '__main__':
    verify_inputs()
    check_pins()
    make_diagnostics()
    compile_all()
