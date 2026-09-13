#!/usr/bin/env python3
"""Independently validate retained fresh outputs and bind all nested frozen evidence."""
import hashlib, json, pathlib, re, shutil
from run import P, E, G, O, L, C, digest, write, utc, command

fpath = P / 'verification/proof-freeze.json'
freeze = json.loads(fpath.read_text())
assert digest(fpath) == 'f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f'
for name, sha in freeze['files'].items():
    assert digest(P / name) == sha, name
for name, sha in freeze['source_files'].items():
    assert digest(G / name) == sha, name

nested = []
for name in freeze['files']:
    if name.endswith('EVIDENCE-MANIFEST.json') or name in [
            'reviews/statement-freeze.json', 'reviews/statement-package-manifest.json']:
        path = P / name
        record = json.loads(path.read_text())
        base = P if name in ['reviews/statement-freeze.json',
                             'reviews/statement-package-manifest.json'] else path.parent
        for entry, value in record['files'].items():
            expected = value if isinstance(value, str) else value['sha256']
            target = base / entry
            assert digest(target) == expected, (name, entry)
            if isinstance(value, dict) and 'bytes' in value:
                assert target.stat().st_size == value['bytes'], (name, entry)
        nested.append({'path': name, 'sha256': digest(path), 'entries': len(record['files'])})

results = []
build = []
printed = []
warnings = []
for d in sorted(E.glob('command-*')):
    r = json.loads((d / 'result.json').read_text())
    assert r['exit_code'] == 0, d
    assert digest(d / 'raw.log') == r['output_sha256'], d
    results.append(r)
    if 'source' not in r:
        continue
    build.append(r)
    assert digest(P / r['source']) == r['sha256'] == digest(d / 'source.lean'), d
    raw = (d / 'raw.log').read_text()
    for name, axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", raw):
        actual = [a.strip() for a in axioms.split(',') if a.strip()]
        assert set(actual) <= {'propext', 'Classical.choice', 'Quot.sound'}, (name, actual)
        printed.append({'command': str(d.relative_to(P)), 'name': name, 'axioms': actual})
    warnings.extend({'source': r['source'], 'text': line} for line in raw.splitlines() if 'warning:' in line)
assert len(results) == 50 and len(build) == 13
assert len(printed) == 69
assert len(warnings) == 14
assert sum('Reference.lean' in w['source'] for w in warnings) == 12
assert sum(w['source'] == 'NLA/RA20/Differential.lean' for w in warnings) == 2
inspector = (E / 'command-050/raw.log').read_text()
names = json.loads((P / 'comparator.json').read_text())['theorem_names']
matches = re.findall(r'^EXACT_REFERENCE_TYPE ([^:]+):', inspector, re.M)
assert matches == names
assert 'CLOSURE_COMPLETE declarations=214; material_dependencies=28' in inspector
closure = re.findall(r'^PROJECT_DECL ([^:]+): axioms=\[(.*?)\]; project_dependencies=\[(.*?)\]',
                     inspector, re.M | re.S)
assert len(closure) == 214
parsed_closure = []
for name, axioms, deps in closure:
    axs = [x.strip() for x in axioms.split(',') if x.strip()]
    edges = [x.strip() for x in deps.split(',') if x.strip()]
    assert set(axs) <= {'propext', 'Classical.choice', 'Quot.sound'}, name
    assert not any('Reference' in x or 'Contract' in x for x in edges), name
    parsed_closure.append({'declaration': name, 'axioms': axs, 'project_dependencies': edges})
assert len({r['declaration'] for r in parsed_closure}) == 214
write(E / 'parsed-closure.json', parsed_closure)

sources = [r['source'] for r in build if not r['source'].startswith('reviews/')]
assert len(sources) == 11
assertions = sum(len(re.findall(r'^#assert_trust kernel ', (P / name).read_text(), re.M)) for name in sources)
assert assertions == 61
for name in sources:
    content = (P / name).read_text()
    assert not re.search(r'^\s*(axiom|unsafe|partial|sorry|admit)\b', content, re.M), name
    assert not re.search(r'^import .*Challenge', content, re.M), name
    assert not re.search(r'\bnative_decide\b|ofReduceBool|trustCompiler', content), name

library_sources = {
    'mathlib': ['Mathlib/RingTheory/Nullstellensatz.lean',
        'Mathlib/RingTheory/Smooth/Locus.lean', 'Mathlib/RingTheory/Smooth/Basic.lean',
        'Mathlib/Algebra/MvPolynomial/Funext.lean', 'Mathlib/Algebra/MvPolynomial/PDeriv.lean',
        'Mathlib/SetTheory/Cardinal/Basic.lean', 'Mathlib/LinearAlgebra/Matrix/Rank.lean',
        'Mathlib/Analysis/Calculus/FDeriv/Defs.lean'],
    'leancert': ['LeanCert/Tactic/Verification.lean']}
library = []
for package, entries in library_sources.items():
    for name in entries:
        src = C / package / name
        dst = E / 'library-source-snapshots' / package / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
        library.append({'package': package, 'path': name, 'sha256': digest(src),
                        'snapshot': str(dst.relative_to(P))})
write(E / 'library-inspection.json', {'utc': utc(), 'sources': library,
      'read_scope': 'Targeted actual declaration/API source inspection; not a complete Mathlib or LeanCert review.'})

pins = []
for pin in json.loads((P / 'lake-manifest.json').read_text())['packages']:
    head = command(['git', 'rev-parse', 'HEAD'], C / pin['name']).strip()
    status = command(['git', 'status', '--porcelain', '--untracked-files=no'], C / pin['name'])
    assert head == pin['rev'] and not status.strip(), pin['name']
    pins.append({'name': pin['name'], 'revision': head, 'tracked_status_clean': True})
write(E / 'dependency-pins-after.json', {'utc': utc(), 'packages': pins})

owned = {str(p.relative_to(O)): {'sha256': digest(p), 'bytes': p.stat().st_size}
         for p in sorted(O.rglob('*')) if p.is_file()}
assert owned
assert not any(p.is_symlink() for p in O.rglob('*'))
write(E / 'prefix-object-inventory.json', {'utc': utc(), 'prefix': str(O), 'files': owned,
                                        'file_count': len(owned)})
shutil.rmtree(O)
assert not O.exists()
write(E / 'cleanup.json', {'utc': utc(), 'removed_only': str(O), 'owned_file_count': len(owned),
      'owned_bytes': sum(x['bytes'] for x in owned.values()),
      'source_and_shared_dependency_trees_untouched': True})

write(E / 'validation.json', {'utc': utc(), 'result': 'PASS',
    'proof_freeze_sha256': digest(fpath), 'frozen_files': len(freeze['files']),
    'original_sources': len(freeze['source_files']), 'nested_manifests': nested,
    'source_commands': len(build), 'command_records_before_after_pins': 70,
    'real_source_modules': len(sources), 'source_seconds': sum(r['seconds'] for r in build),
    'exact_type_matches': matches, 'project_closure_declarations': 214,
    'material_dependencies': 28, 'source_kernel_assertions': assertions,
    'own_kernel_assertions': 12, 'printed_axiom_reports': len(printed),
    'axiom_reports': printed, 'warnings': warnings,
    'owned_prefix_removed_after_hashing': True,
    'actual_Linux_Comparator_default_kernel_controls': 'NOT RUN by this reviewer'})
print(json.dumps({'result': 'PASS', 'frozen_files': len(freeze['files']),
                  'nested_manifests': len(nested), 'fresh_commands': len(build),
                  'axiom_reports': len(printed), 'project_declarations': len(closure),
                  'owned_objects_removed': len(owned)}))
