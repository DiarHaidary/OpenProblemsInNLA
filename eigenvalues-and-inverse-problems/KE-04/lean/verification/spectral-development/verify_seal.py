#!/usr/bin/env python3
"""Portable, read-only verification of this bounded author development evidence.

This reads retained execution receipts; it does not run Lean, Git, old drivers,
dependency builds, or cleanup scripts. Historical failed compiles remain failures.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

P = Path(__file__).resolve().parents[2]
E = P / 'verification/spectral-development'
OUTER = 'verification/spectral-development/EVIDENCE-MANIFEST.json'
FREEZE = '85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e'
GATE = '5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624'
SOURCE = '64e8255697387e32e65cf591a0cb7dbf7986f471c82b4f1715c9a88a7650e20e'
INSPECT = '0eba246cae16b7faae8ab69afc3e626f18a7c2c5cf9616469ef83aeb6a362e39'
TARGETS = ['orderedSpectrum_semantics', 'quadratic_semantics',
           'spectral_gap_quadratic_psd', 'psd_zero_form_iff_kernel']
ROOTS = TARGETS + ['quadratic_apply_eigenvector']
ATTEMPTS = [('attempt-qr384kbx', False, 2), ('attempt-wzr6ev6d', False, 2),
            ('attempt-k0z8w9ex', True, 2), ('attempt-k2z1xc0b', True, 3)]
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def check_hashes(files):
    for relative, info in files.items():
        rel = Path(relative)
        assert not rel.is_absolute() and '..' not in rel.parts, relative
        f = P / rel
        assert f.is_file() and not f.is_symlink(), relative
        expected = info if isinstance(info, str) else info['sha256']
        assert sha(f) == expected, relative
        if isinstance(info, dict) and 'bytes' in info:
            assert f.stat().st_size == info['bytes'], relative

def header(text, name):
    match = re.search(r'\btheorem\s+' + re.escape(name) + r'\b(.*?):=\s*by', text, re.S)
    assert match, name
    return ' '.join(match.group(1).split())

def bracket_records(text, marker):
    result = {}
    for m in re.finditer(r'^' + re.escape(marker) + r' (\S+): \[([^\]]*)\]', text, re.M):
        assert m[1] not in result, m[1]
        result[m[1]] = [v.strip() for v in m[2].split(',') if v.strip()]
    return result

def inspect_receipts():
    total_commands = 0
    total_objects = 0
    assert {d.name for d in E.glob('attempt-*') if d.is_dir()} == {a[0] for a in ATTEMPTS}
    package_pins = {d['name']: d['rev'] for d in read(P / 'lake-manifest.json')['packages']}
    for name, passes, count in ATTEMPTS:
        a = E / name
        result = read(a / 'result.json')
        commands = read(a / 'commands.json')
        assert result['all_requested_compiles_pass'] is passes
        assert len(result['compile_commands']) == count
        assert result['Linux_Comparator_execution'] is False
        assert result['preserved_frozen_inputs'] == 1598
        assert result['unchanged_sources'] is True
        total_commands += len(commands)
        assert len(commands) == 41 + count
        for c in commands:
            assert (a / c['stdout']).is_file() and (a / c['stderr']).is_file()
        compiles = [c for c in commands if c['stdout'].startswith('compile-')]
        assert [c['exit'] for c in compiles] == ([0] * count if passes else [0, 1])
        assert [c['exit'] for c in compiles] == [c['exit'] for c in result['compile_commands']]
        before = read(a / 'source-before.json')
        assert before == read(a / 'source-after.json')
        for r, expected in before.items():
            assert sha(a / 'inputs' / r) == expected, (name, r)
        for phase in ['before', 'after']:
            assert read(a / ('frozen-' + phase + '.json')) == {
                'all_match': True, 'checked': 1598, 'freeze_sha256': FREEZE}
            pins = read(a / ('pins-' + phase + '.json'))
            assert len(pins) == 10
            assert {d['name']: d['revision'] for d in pins} == package_pins
            assert sum(d['build_objects_present'] for d in pins) == 9
            for d in pins:
                assert d['clean'] is True
                h = next(c for c in commands if c['stdout'] == phase + '-' + d['name'] + '-head.stdout')
                s = next(c for c in commands if c['stdout'] == phase + '-' + d['name'] + '-status.stdout')
                assert h['exit'] == s['exit'] == 0
                assert (a / h['stdout']).read_text().strip() == package_pins[d['name']]
                assert not (a / s['stdout']).read_bytes()
                assert not (a / h['stderr']).read_bytes() and not (a / s['stderr']).read_bytes()
        toolchain = read(a / 'toolchain.json')
        assert toolchain['sha256'] == '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554'
        assert '4.33.1' in toolchain['version'] and 'arm64-apple-darwin' in toolchain['version']
        assert len(toolchain['LEAN_PATH']) == 11
        prefix = read(a / 'prefix.json')
        assert prefix['initial_output_files'] == []
        assert toolchain['LEAN_PATH'][0] == prefix['path'] + '/lib'
        for c, module in zip(compiles, result['compile_commands']):
            assert c['LEAN_PATH'].split(':') == toolchain['LEAN_PATH']
            assert c['cwd'] == prefix['path'] + '/src'
            assert c['argv'][1] == '--root=' + prefix['path'] + '/src'
            assert c['argv'][-1] == prefix['path'] + '/src/' + module['module'] + '.lean'
            assert c['argv'][2:3] == ['-o'] and c['argv'][4:5] == ['-i']
        objects = read(a / 'objects.json')
        cleanup = read(a / 'cleanup.json')
        assert objects['prefix'] == cleanup['prefix'] == prefix['path']
        assert cleanup['all_own_object_hashes_matched'] is True and cleanup['removed'] is True
        assert cleanup['objects'] == len(objects['files']) == (2 * count if passes else 2)
        assert all(r.startswith('lib/') for r in objects['files'])
        assert all(re.fullmatch('[0-9a-f]{64}', d['sha256']) and d['bytes'] > 0
                   for d in objects['files'].values())
        total_objects += cleanup['objects']
        if passes:
            assert before['NLA/KE04/Spectral.lean'] == SOURCE
            text = (a / 'compile-NLA-KE04-Spectral.stdout').read_text()
            assert 'warning:' not in text and 'error:' not in text and 'sorryAx' not in text
            for root in ROOTS:
                assert f"'NLA.KE04._proved.{root}' depends on axioms: [propext, Classical.choice, Quot.sound]" in text
        else:
            text = (a / 'compile-NLA-KE04-Spectral.stdout').read_text()
            assert 'error' in text and 'sorryAx' in text
    a = E / ATTEMPTS[-1][0]
    assert read(a / 'source-before.json')['verification/spectral-development/Inspect.lean'] == INSPECT
    text = (a / 'compile-Inspect.stdout').read_text()
    assert 'warning:' not in text and 'error:' not in text and 'sorryAx' not in text
    exact = re.findall(r'^EXACT_FROZEN_TYPE (\S+):', text, re.M)
    assert exact == ['NLA.KE04._proved.' + n for n in TARGETS]
    axes = bracket_records(text, 'ACTUAL_AXIOMS')
    edges = bracket_records(text, 'PROJECT_EDGE')
    deps = bracket_records(text, 'ALL_DIRECT_DEPENDENCIES')
    assert len(axes) == len(edges) == len(deps) == 22
    assert set(axes) == set(edges) == set(deps)
    assert all(set(v) <= ALLOWED for v in axes.values())
    assert sum(set(v) == ALLOWED for v in axes.values()) == 21
    pending = ['NLA.KE04._proved.' + n for n in ROOTS]
    seen = set()
    while pending:
        n = pending.pop()
        if n not in seen:
            seen.add(n)
            assert n in edges
            assert not n.startswith('NLA.KE04.SpectralExpected.')
            pending.extend(edges[n])
            assert set(edges[n]) == {d for d in deps[n]
                if d.startswith('NLA.KE04.') or d.startswith('_private.NLA.KE04.')}
    assert seen == set(edges)
    used = {d for values in deps.values() for d in values}
    required = re.findall(r'^RETAINED_DEPENDENCY (\S+)', text, re.M)
    assert len(required) == len(set(required)) == 25 and set(required) <= used
    assert {'sorryAx', 'Lean.ofReduceBool', 'Lean.trustCompiler'}.isdisjoint(used)
    assert 'PROJECT_COUNTS declarations=22, required=25' in text
    return {'actual_build_driver_commands': total_commands, 'fresh_attempts': 4,
            'historical_failed_Spectral_compiles': 2, 'own_removed_objects': total_objects,
            'final_fresh_Lean_commands': 3, 'exact_types': 4,
            'project_declaration_closure': 22, 'required_material_dependencies': 25,
            'material_kernel_assertions_in_final_source_and_inspector': 10,
            'final_source_and_inspector_warnings': 0}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pre-seal', action='store_true', help='Validate content before the outer seal exists')
    args = ap.parse_args()
    assert sha(P / 'reviews/statement-freeze.json') == FREEZE
    assert sha(P / 'verification/proof-start.json') == GATE
    freeze = read(P / 'reviews/statement-freeze.json')
    assert len(freeze['files']) == 1598
    check_hashes(freeze['files'])
    assert read(P / 'verification/proof-start.json')['proof_authorized'] is True
    assert sha(P / 'NLA/KE04/Spectral.lean') == SOURCE
    assert sha(E / 'Inspect.lean') == INSPECT
    source = (P / 'NLA/KE04/Spectral.lean').read_text()
    challenge = (P / 'Challenge.lean').read_text()
    for name in TARGETS:
        assert header(source, name) == header(challenge, name), name
    assert 'import Challenge' not in source and not re.search(r'\b(sorry|admit|axiom|native_decide)\b', source)
    assert source.count('#assert_trust kernel ') == 5
    checkpoint = read(E / 'CHECKPOINT-SEAL.json')
    assert sha(E / 'CHECKPOINT-SEAL.json') == 'ef842aa46a2b84b05be31fcf667bb2b6f60513abe34edbca62e96838845d46b8'
    check_hashes(checkpoint['files'])
    checkpoint_set = {str(f.relative_to(P)) for f in (E / 'attempt-qr384kbx').rglob('*') if f.is_file()}
    checkpoint_set.add('verification/spectral-development/CHECKPOINT.md')
    assert set(checkpoint['files']) == checkpoint_set and len(checkpoint_set) == 110
    assert checkpoint['exact_self_exclusion'] == 'verification/spectral-development/CHECKPOINT-SEAL.json'
    findings = inspect_receipts()
    binding = E / 'source-bindings'
    records = read(binding / 'records.json')
    commands = read(binding / 'commands.json')
    assert len(records) == 30 and len(commands) == 60
    originals = read(P / 'verification/original-source-inventory.json')['files']
    assert sum(d['kind'] == 'original' for d in records) == len(originals) == 17
    for i, d in enumerate(records):
        data = (binding / d['snapshot']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == d['sha256'] and len(data) == d['bytes']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == d['git_blob']
        h, s = commands[2*i:2*i+2]
        assert h['exit'] == s['exit'] == 0
        assert h['argv'][-1] == s['argv'][-1] == d['commit'] + ':' + d['upstream_path']
        assert (binding / h['stdout']).read_text().strip() == d['git_blob']
        assert s['stdout'] == d['snapshot']
        assert not (binding / h['stderr']).read_bytes() and not (binding / s['stderr']).read_bytes()
        if d['kind'] == 'original':
            matches = [(r, v) for r, v in originals.items()
                       if (v['commit'], v['upstream_path']) == (d['commit'], d['upstream_path'])]
            assert len(matches) == 1
            r, v = matches[0]
            assert v['sha256'] == d['sha256'] and v['git_blob'] == d['git_blob']
            assert (P / r).read_bytes() == data
    assert read(binding / 'result.json')['original_full_proof_block_unchanged'] is True
    if args.pre_seal:
        status = 'KE04_SPECTRAL_CONTENT_PREFLIGHT_PASS'
        bound_count = None
    else:
        outer = read(P / OUTER)
        assert outer['exact_self_exclusion'] == OUTER
        expected = set(freeze['files']) | {'reviews/statement-freeze.json',
            'verification/proof-start.json', 'NLA/KE04/Spectral.lean', 'reviews/spectral-development.md'}
        expected |= {str(f.relative_to(P)) for f in E.rglob('*') if f.is_file()}
        expected.remove(OUTER)
        assert set(outer['files']) == expected
        check_hashes(outer['files'])
        bound_count = len(expected)
        assert outer['file_count'] == bound_count
        status = 'SEALED_KE04_SPECTRAL_HELPER_PASS'
    print(json.dumps({'status': status, 'scope': 'bounded author helper completion',
        'independent_final_mathematical_approval': False, 'Linux_Comparator_execution': False,
        'complete_frozen_inputs_preserved': 1598, 'unchanged_checkpoint_files': 110,
        'original_Git_bindings': 17, 'reused_API_Git_bindings': 13,
        'outer_bound_files': bound_count, **findings}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
