#!/usr/bin/env python3
"""Portable read-only evidence verification; no Lean/Git/build/cleanup execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re

P = Path(__file__).resolve().parents[2]
E = P / 'verification/completion-development'
OUTER = 'verification/completion-development/EVIDENCE-MANIFEST.json'
SOURCE = '4014011a7c6435c362ce4cf304aed8d7a8ad2e32ffb03448fbf43223c59a3f97'
INSPECT = '317c5228a570227cfe4afe5b5a27240fd817a91a167c7a8bd75d94ea8cc9d3ed'
FREEZE = '85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e'
GATE = '5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624'
PRIOR = {
    'verification/spectral-window-development/EVIDENCE-MANIFEST.json': '2fecf0e58267ebab396ccc9a4691fb1e41a751fe6e23e98c89a2842af01a269c',
    'verification/transport-intersection-handoff/EVIDENCE-MANIFEST.json': 'b3232d8adb072dc44447a2a1f6f806f709bc55b4201b85d680d557645d9d72e8',
    'verification/nonannihilation-development/EVIDENCE-MANIFEST.json': 'd57bb205a29e51eefa1e1d67f662f052875a58961c750f6930028408251def68'}
BUILD_SEALS = {'verification/spectral-window-development/EVIDENCE-MANIFEST.json':
    '2fecf0e58267ebab396ccc9a4691fb1e41a751fe6e23e98c89a2842af01a269c'}
TARGETS = ['strictIntervalOccupancy', 'blockLanczosConjecture']
ROOTS = TARGETS + ['psd_form_nonneg']
ATTEMPTS = [('attempt-c7o2c3cd', True, 9), ('attempt-700n3s8e', True, 10)]
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text())

def hashes(files):
    for r, value in files.items():
        rel = Path(r)
        assert not rel.is_absolute() and '..' not in rel.parts
        path = P / rel
        assert path.is_file() and not path.is_symlink(), r
        expected = value if isinstance(value, str) else value['sha256']
        assert sha(path) == expected, r
        if isinstance(value, dict):
            assert path.stat().st_size == value['bytes'], r

def header(text, name):
    m = re.search(r'\btheorem\s+' + re.escape(name) + r'\b(.*?):=', text, re.S)
    assert m, name
    return ' '.join(m[1].split())

def records(text, marker):
    found = {}
    for m in re.finditer(r'^' + re.escape(marker) + r' (\S+): \[([^\]]*)\]', text, re.M):
        assert m[1] not in found
        found[m[1]] = [x.strip() for x in m[2].split(',') if x.strip()]
    return found

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pre-seal', action='store_true')
    args = ap.parse_args()
    prior = {}
    for r, expected in PRIOR.items():
        assert sha(P / r) == expected
        d = read(P / r)
        assert d['exact_self_exclusion'] == r
        hashes(d['files'])
        prior[r] = expected
        for path, v in d['files'].items():
            if path in prior:
                assert prior[path] == v['sha256']
            prior[path] = v['sha256']
    assert len(prior) == 3047
    assert sha(P / 'reviews/statement-freeze.json') == FREEZE
    assert sha(P / 'verification/proof-start.json') == GATE
    freeze = read(P / 'reviews/statement-freeze.json')
    assert len(freeze['files']) == 1598
    hashes(freeze['files'])
    assert sha(P / 'NLA/KE04/Completion.lean') == SOURCE
    assert sha(E / 'Inspect.lean') == INSPECT
    source = (P / 'NLA/KE04/Completion.lean').read_text()
    challenge = (P / 'Challenge.lean').read_text()
    for name in TARGETS:
        assert header(source, name) == header(challenge, name)
    assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', source)
    assert 'import Challenge' not in source
    assert source.count('#assert_trust kernel ') == 3
    package_pins = {d['name']: d['rev'] for d in read(P / 'lake-manifest.json')['packages']}
    assert {a.name for a in E.glob('attempt-*') if a.is_dir()} == {a[0] for a in ATTEMPTS}
    total_commands, total_objects = 0, 0
    for name, passes, count in ATTEMPTS:
        a = E / name
        result = read(a / 'result.json')
        commands = read(a / 'commands.json')
        total_commands += len(commands)
        assert len(commands) == 41 + count
        assert result['all_requested_compiles_pass'] is passes
        assert result['Linux_Comparator_execution'] is False
        assert result['unchanged_sources'] is True
        compiles = [c for c in commands if c['stdout'].startswith('compile-')]
        assert len(compiles) == count
        exits = [0] * count if passes else [0] * (count-1) + [1]
        assert [c['exit'] for c in compiles] == exits
        assert [c['exit'] for c in result['compile_commands']] == exits
        for c in commands:
            assert (a / c['stdout']).is_file() and (a / c['stderr']).is_file()
        before = read(a / 'source-before.json')
        assert before == read(a / 'source-after.json')
        for r, expected in before.items():
            assert sha(a / 'inputs' / r) == expected, (name, r)
            if r in prior:
                assert prior[r] == expected, (name, r)
        assert before['NLA/KE04/Frames.lean'] == 'bfea6b02091db4e999c2c870b4b1f238cb546ad84df010c7d5431fe82904db0b'
        assert before['NLA/KE04/Spectral.lean'] == '64e8255697387e32e65cf591a0cb7dbf7986f471c82b4f1715c9a88a7650e20e'
        for phase in ['before', 'after']:
            assert read(a / ('frozen-' + phase + '.json')) == {
                'all_match': True, 'checked': 1598, 'freeze_sha256': FREEZE}
            assert read(a / ('imported-' + phase + '.json')) == {
                'seals': BUILD_SEALS, 'all_match': True, 'bound_files': 2764}
            pins = read(a / ('pins-' + phase + '.json'))
            assert {d['name']: d['revision'] for d in pins} == package_pins and len(pins) == 10
            assert sum(d['build_objects_present'] for d in pins) == 9
            for d in pins:
                assert d['clean'] is True
                h = next(c for c in commands if c['stdout'] == phase + '-' + d['name'] + '-head.stdout')
                s = next(c for c in commands if c['stdout'] == phase + '-' + d['name'] + '-status.stdout')
                assert h['exit'] == s['exit'] == 0
                assert (a / h['stdout']).read_text().strip() == package_pins[d['name']]
                assert not (a / s['stdout']).read_bytes()
                assert not (a / h['stderr']).read_bytes() and not (a / s['stderr']).read_bytes()
        tc = read(a / 'toolchain.json')
        prefix = read(a / 'prefix.json')
        assert tc['sha256'] == '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554'
        assert '4.33.1' in tc['version'] and 'arm64-apple-darwin' in tc['version']
        assert prefix['initial_output_files'] == [] and len(tc['LEAN_PATH']) == 11
        assert tc['LEAN_PATH'][0] == prefix['path'] + '/lib'
        for c, m in zip(compiles, result['compile_commands']):
            assert c['LEAN_PATH'].split(':') == tc['LEAN_PATH']
            assert c['cwd'] == prefix['path'] + '/src'
            assert c['argv'][1] == '--root=' + prefix['path'] + '/src'
            assert c['argv'][-1] == prefix['path'] + '/src/' + m['module'] + '.lean'
        objects, cleanup = read(a / 'objects.json'), read(a / 'cleanup.json')
        assert objects['prefix'] == cleanup['prefix'] == prefix['path']
        assert cleanup['all_own_object_hashes_matched'] is True and cleanup['removed'] is True
        assert cleanup['objects'] == len(objects['files']) == 2 * (count if passes else count-1)
        total_objects += cleanup['objects']
        for r, d in objects['files'].items():
            assert r.startswith('lib/') and re.fullmatch('[0-9a-f]{64}', d['sha256']) and d['bytes'] > 0
        text = (a / 'compile-NLA-KE04-Completion.stdout').read_text()
        if passes:
            assert before['NLA/KE04/Completion.lean'] == SOURCE
            assert 'warning:' not in text and 'error:' not in text and 'sorryAx' not in text
            for root in ROOTS:
                assert f"'NLA.KE04._proved.{root}' depends on axioms: [propext, Classical.choice, Quot.sound]" in text
        else:
            assert 'error' in text
    a = E / ATTEMPTS[-1][0]
    assert read(a / 'source-before.json')['verification/completion-development/Inspect.lean'] == INSPECT
    text = (a / 'compile-Inspect.stdout').read_text()
    assert not any(x in text for x in ['warning:', 'error:', 'sorryAx'])
    assert re.findall(r'^EXACT_FROZEN_TYPE (\S+):', text, re.M) == ['NLA.KE04._proved.' + n for n in TARGETS]
    axes, edges, deps = [records(text, label) for label in ['ACTUAL_AXIOMS', 'PROJECT_EDGE', 'ALL_DIRECT_DEPENDENCIES']]
    assert len(axes) == len(edges) == len(deps) == 104 and set(axes) == set(edges) == set(deps)
    assert all(set(v) <= ALLOWED for v in axes.values())
    assert sum(set(v) == ALLOWED for v in axes.values()) == 89
    pending, seen = ['NLA.KE04._proved.' + n for n in ROOTS], set()
    while pending:
        n = pending.pop()
        if n not in seen:
            seen.add(n)
            assert n in edges and not n.startswith('NLA.KE04.CompletionExpected.')
            pending.extend(edges[n])
            assert set(edges[n]) == {d for d in deps[n]
                if d.startswith('NLA.KE04.') or d.startswith('_private.NLA.KE04.')}
    assert seen == set(edges)
    used = {d for ds in deps.values() for d in ds}
    required = re.findall(r'^RETAINED_DEPENDENCY (\S+)', text, re.M)
    assert len(required) == len(set(required)) == 22 and set(required) <= used
    assert {'sorryAx', 'Lean.ofReduceBool', 'Lean.trustCompiler'}.isdisjoint(used)
    assert 'PROJECT_COUNTS declarations=104, required=22' in text
    capture = E / 'imported-helper-checks'
    assert read(capture / 'before.json') == read(capture / 'after.json')
    binding = read(capture / 'before.json')
    assert binding['seals'] == PRIOR and binding['files'] == prior
    assert binding['file_count'] == 3047
    commands = read(capture / 'commands.json')
    assert len(commands) == 3
    for i, c in enumerate(commands):
        assert c['exit'] == 0 and c['read_only_branch'] is True
        assert not (capture / c['stderr']).read_bytes()
        assert sha(capture / ('executed-verifier-' + str(i) + '.py')) == c['executed_verifier_sha256']
        original = Path(c['argv'][1])
        relative = str(original).split('/next-ke04-statements-draft/lean/', 1)[1]
        assert sha(P / relative) == c['executed_verifier_sha256']
    assert read(capture / '0.stdout')['status'] == 'SEALED_KE04_SPECTRAL_WINDOW_PASS'
    assert read(capture / '1.stdout')['pass'] is True
    assert read(capture / '2.stdout')['status'] == 'VERIFIED'
    assert commands[2]['argv'][-1] == '--verify'
    final_warnings = []
    reports = 0
    for log in a.glob('compile-*.stdout'):
        content = log.read_text()
        assert 'error:' not in content and 'sorryAx' not in content
        reports += len(re.findall(r"^'[^']+' depends on axioms:", content, re.M))
        final_warnings.extend((log.name, line) for line in content.splitlines() if 'warning:' in line)
    assert len(final_warnings) == 1
    assert final_warnings[0][0] == 'compile-NLA-KE04-Krylov.stdout'
    assert 'Krylov.lean:107:25: warning: This simp argument is unused:' in final_warnings[0][1]
    assert reports == 56
    bound = None
    if not args.pre_seal:
        outer = read(P / OUTER)
        assert outer['exact_self_exclusion'] == OUTER
        expected = set(prior) | {'NLA/KE04/Completion.lean'}
        expected |= {str(f.relative_to(P)) for f in E.rglob('*') if f.is_file()}
        expected.remove(OUTER)
        assert set(outer['files']) == expected
        hashes(outer['files'])
        bound = len(expected)
        assert outer['file_count'] == bound
    print(json.dumps({'status': 'KE04_COMPLETION_PREFLIGHT_PASS' if args.pre_seal else 'SEALED_KE04_COMPLETION_PASS',
        'scope': 'complete target proof author assembly; final verification gates remain' , 'exact_frozen_types': 2,
        'final_fresh_Lean_commands': 10, 'new_source_and_inspector_warnings': 0,
        'inherited_Krylov_warnings': 1, 'actual_project_closure': 104,
        'required_material_dependencies': 22, 'new_material_kernel_assertions': 6,
        'fresh_attempts': 2, 'historical_failed_new_module_compiles': 0,
        'actual_build_driver_commands': total_commands, 'own_hashed_removed_objects': total_objects,
        'preserved_frozen_inputs': 1598, 'preserved_imported_seal_files': 3047,
        'actual_imported_read_only_checks': 3, 'final_actual_axiom_reports': 56, 'outer_files': bound,
        'independent_final_mathematical_approval': False, 'Linux_Comparator_execution': False}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
