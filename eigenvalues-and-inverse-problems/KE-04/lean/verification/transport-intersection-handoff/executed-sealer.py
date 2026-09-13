from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re

P = Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean').resolve()
E = P / 'verification/transport-intersection-handoff'
assert not E.exists()
E.mkdir()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, d):
    p.write_text(json.dumps(d, indent=2) + '\n')
files = set()
for scope, digest in [
    ('krylov-root-development', 'd0077d6e4f751a13404ebee91f60a2c9965ad22e5030983e66412746acb69407'),
    ('frames-development', '73770debb7678e443032c5f30e77ef82365cd32b81d24bba161990e2ac7f8db8'),
    ('spectral-development', '27a8328c569a17db1e6cf671a0a79034e3ce9eb2dc85c4640d13be7624191ca2')]:
    outer = P / 'verification' / scope / 'EVIDENCE-MANIFEST.json'
    assert sha(outer) == digest
    m = json.loads(outer.read_text())
    files.add(outer)
    for rel, r in m['files'].items():
        q = P / rel
        assert q.is_file() and not q.is_symlink() and sha(q) == r['sha256'], rel
        assert q.stat().st_size == r['bytes']
        files.add(q)
f = json.loads((P / 'reviews/statement-freeze.json').read_text())
assert len(f['files']) == 1598
for rel, h in f['files'].items():
    assert sha(P / rel) == h

results = []
scopes = ['verification/transport-development', 'verification/intersection-development', str(E.relative_to(P))]
for module, dirname, final, counts, compiles, own_assertions in [
    ('Transport', 'transport-development', 'attempt-1zv5sy8b', [4, 63, 14], 6, 11),
    ('Intersection', 'intersection-development', 'attempt-thbyznuc', [1, 11, 6], 4, 1)]:
    d = P / 'verification' / dirname
    a = d / final
    r = json.loads((a / 'result.json').read_text())
    assert r['success'] and not r['errors']
    assert list(map(int, r['final_inspection_counts'])) == counts
    assert len(r['commands']) == compiles + 1
    assert r['module_kernel_assertions'] == own_assertions
    for rel, v in r['inputs'].items():
        q = a / 'source' / rel if rel == 'Inspect.lean' else P / rel
        assert sha(q) == v['sha256'] and q.stat().st_size == v['bytes']
    reports = []
    warnings = []
    for c in r['commands']:
        assert c['exit_code'] == 0
        for stream in ['stdout', 'stderr']:
            assert sha(a / c[stream]) == c[stream + '_sha256']
        log = (a / c['stdout']).read_text()
        reports += re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", log)
        warnings += [line for line in log.splitlines() if ': warning:' in line]
    assert all({s.strip() for s in ax.split(',') if s.strip()} <=
               {'propext', 'Classical.choice', 'Quot.sound'} for _, ax in reports)
    for phase in ['before_dependencies', 'after_dependencies']:
        assert len(r[phase]) == 10
        for pkg in r[phase]:
            assert pkg['checks'][0]['stdout'].strip() == pkg['expected_revision']
            assert pkg['checks'][1]['stdout'] == ''
            assert all(c['exit_code'] == 0 and not c['stderr'] for c in pkg['checks'])
    assert r['own_prefix_removed'] and not Path(r['private_prefix']).exists()
    logs = (a / 'Inspect.stdout').read_text()
    assert len(re.findall(r'^EXACT_CONTRACT ', logs, re.M)) == counts[0]
    assert len(re.findall(r'^ACTUAL_PROJECT ', logs, re.M)) == counts[1]
    assert len(re.findall(r'^MATERIAL_DEPENDENCY ', logs, re.M)) == counts[2]
    assert ': warning:' not in (a / ('NLA-KE04-' + module + '.stdout')).read_text()
    results.append({'module': module, 'source_sha256': sha(P / 'NLA/KE04' / (module + '.lean')),
        'final_attempt': str(a.relative_to(P)), 'result_sha256': sha(a / 'result.json'),
        'fresh_source_commands': compiles, 'exact_types': counts[0],
        'actual_project_closure': counts[1], 'required_dependencies': counts[2],
        'own_kernel_assertions': own_assertions, 'additional_inspector_assertions': counts[0],
        'all_fresh_compile_axiom_reports_including_imports': len(reports),
        'own_mathematical_source_warnings': 0, 'all_retained_warnings': warnings,
        'historical_attempts': [{'path': str(t.relative_to(P)),
            'success': json.loads((t / 'result.json').read_text())['success'],
            'result_sha256': sha(t / 'result.json')} for t in sorted(d.glob('attempt-*'))]})
    files |= {q for q in d.rglob('*') if q.is_file()}
    files.add(P / 'NLA/KE04' / (module + '.lean'))

(E / 'HANDOFF.md').write_text('''# KE-04 transport and intersection author completion

The exact frozen contracts 12, 16, 19, 20 and 23 are implemented, freshly compiled
and compared to their full approved types. These are bounded author checks,
not complete KE-04 verification, independent final review or actual Linux/Comparator.

Transport proves that an orthonormal frame is isometric and gives the coordinates
of the actual compression action. Its quadratic-form expansion needs only x and
Ax in the frame span; symmetry moves the first A to the other inner-product slot.
Both earlier and later frames therefore give the same form on K_(k-1). Equality
of vector actions is used only for the later frame, which also contains A^2x.
The proof never equates the earlier squared compression with A^2. Exact natural
index arithmetic handles k=1 and p=0 by their empty allowed index sets, and the
full-prefix assertion implies the canonical largest-full-iteration assertion.

Intersection uses the exact finite-dimensional sum/intersection identity. A
(p+1)-dimensional subspace inside K_k cannot have zero intersection with the
(k-1)p-dimensional previous prefix, since the sum has dimension at most kp.
Positive actual finrank supplies an actual nonzero vector of the intersection.
No existence or nonannihilation conclusion is assumed in the definitions.

Transport passed its first source build and a separate final inspection. The first
Intersection attempt failed because an infimum was coerced into Type too early;
the only correction was the explicit subtype coercion in its finrank expression.
The second fresh source/inspector run passed. Both failures and successes retain
all exact source snapshots, executed drivers, commands and raw diagnostics. The
new mathematical modules have no warnings. The unchanged imported Krylov module
has its previously disclosed unused simp-argument warning, and expected proposition
binders have harmless warnings preserved verbatim in HANDOFF.json.

All 1598 frozen statement inputs and the exact imported Krylov, Frames and Spectral
seals were checked. Ten clean source pins before and after each run identify the
nine existing read-only dependency object paths. Every build used an empty own
prefix and retained generated object hashes before removing that prefix. No
dependency cache was copied, downloaded, rebuilt or changed. Numerical interval
computation is unnecessary for these symbolic statements.

Original argument: Matthew J. Colbrook. AI-assisted formalization: George
Stepaniants, Department of Computing and Mathematical Sciences, California
Institute of Technology, Pasadena, California, USA. The coordinator is a proof
contributor and is ineligible as an independent final KE-04 mathematical referee.
Canonical status, permanent IDs, original targets and Git state are unchanged.
''')
save(E / 'HANDOFF.json', {'utc': datetime.now(timezone.utc).isoformat(),
    'status': 'COMPLETE_SCOPED_AUTHOR_VALIDATION', 'results': results,
    'preserved_statement_inputs': 1598, 'independent_final_review': False,
    'actual_linux_comparator': False, 'whole_problem_verified': False})
(E / 'executed-sealer.py').write_bytes(Path(__file__).read_bytes())
(E / 'verify_seal.py').write_text('''from pathlib import Path
import hashlib,json
E=Path(__file__).resolve().parent;P=E.parents[1];M=E/'EVIDENCE-MANIFEST.json'
D=json.loads(M.read_text());assert D['exact_self_exclusion']==str(M.relative_to(P))
for rel,r in D['files'].items():
 p=P/rel;assert p.is_file() and not p.is_symlink(),rel
 assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],rel
 assert p.stat().st_size==r['bytes'],rel
for scope in D['complete_owned_scopes']:
 actual={str(p.relative_to(P)) for p in (P/scope).rglob('*') if p.is_file() and p!=M}
 expected={r for r in D['files'] if r.startswith(scope+'/')}
 assert actual==expected,(scope,actual-expected,expected-actual)
F=json.loads((P/'reviews/statement-freeze.json').read_text())
for rel,h in F['files'].items():assert hashlib.sha256((P/rel).read_bytes()).hexdigest()==h,rel
print(json.dumps({'pass':True,'bound_files':len(D['files']),'frozen_inputs':len(F['files']),
 'independent_final_review':False,'actual_linux_comparator':False}))
''')
files |= {q for q in E.rglob('*') if q.is_file()}
outer = E / 'EVIDENCE-MANIFEST.json'
save(outer, {'scope': 'Complete own transport/intersection evidence and explicit immutable imported seal union',
    'complete_owned_scopes': scopes, 'exact_self_exclusion': str(outer.relative_to(P)),
    'files': {str(q.relative_to(P)): {'sha256': sha(q), 'bytes': q.stat().st_size}
              for q in sorted(files)}})
print(json.dumps({'handoff_sha256': sha(E / 'HANDOFF.json'),
    'outer_sha256': sha(outer), 'bound_files': len(files), 'results': results}))
