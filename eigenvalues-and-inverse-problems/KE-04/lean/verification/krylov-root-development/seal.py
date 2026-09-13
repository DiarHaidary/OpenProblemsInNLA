#!/usr/bin/env python3
"""One-shot author handoff; historical attempt files are never rewritten."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

E = Path(__file__).resolve().parent
P = E.parents[1]
M = E / 'EVIDENCE-MANIFEST.json'
assert not M.exists(), 'Already sealed; use the read-only verifier'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):
    return {'sha256': sha(p), 'bytes': p.stat().st_size}
def write(p, d):
    assert not p.exists(), str(p)
    p.write_text(json.dumps(d, indent=2) + '\n')

F = json.loads((P / 'reviews/statement-freeze.json').read_text())
assert len(F['files']) == 1598
for rel, h in F['files'].items():
    assert sha(P / rel) == h, rel
A = E / 'attempt-xl8o7wdd'
D = json.loads((A / 'result.json').read_text())
assert D['success'] and not D['errors'] and D['final_requested']
assert D['final_inspection_counts'] == ['5', '30', '14']
assert D['module_kernel_assertions'] == 14
assert len(D['module_axiom_reports']) == 14
assert all(v == 'propext, Classical.choice, Quot.sound'
           for v in D['module_axiom_reports'].values())
for rel, r in D['inputs'].items():
    actual = A / 'source' / rel if rel == 'Inspect.lean' else P / rel
    assert rec(actual) == r, rel
for c in D['commands']:
    assert c['exit_code'] == 0
    for stream in ['stdout', 'stderr']:
        assert sha(A / c[stream]) == c[stream + '_sha256']
for phase in ['before_dependencies', 'after_dependencies']:
    assert len(D[phase]) == 10
    for dep in D[phase]:
        checks = dep['checks']
        assert all(c['exit_code'] == 0 and not c['stderr'] for c in checks)
        assert checks[0]['stdout'].strip() == dep['expected_revision']
        assert checks[1]['stdout'] == ''
assert D['own_prefix_removed'] and not Path(D['private_prefix']).exists()
log = (A / 'Inspect.stdout').read_text()
assert len(re.findall(r'^EXACT_CONTRACT ', log, re.M)) == 5
assert len(re.findall(r'^ACTUAL_PROJECT ', log, re.M)) == 30
assert len(re.findall(r'^MATERIAL_DEPENDENCY ', log, re.M)) == 14
assert len(re.findall(r' depends on axioms:', log)) == 5
warnings = [s for s in log.splitlines() if ': warning:' in s]
assert len(warnings) == 3 and all('not explicitly referenced' in s for s in warnings)
source_warnings = [s for s in (A / 'NLA-KE04-Krylov.stdout').read_text().splitlines()
                   if ': warning:' in s]
assert len(source_warnings) == 1 and 'simp argument is unused' in source_warnings[0]
assert ': warning:' not in (A / 'NLA-KE04-Definitions.stdout').read_text()
old = P / 'verification/krylov-development'
C = json.loads((old / 'CHECKPOINT.json').read_text())
assert sha(old / 'attempt-z68t67pr/source/NLA/KE04/Krylov.lean') == C['module_sha256']
assert sha(old / 'check.py') == C['runner_sha256']
assert sha(old / 'attempt-z68t67pr/result.json') == C['attempt_result_sha256']
assert sha(old / 'attempt-z68t67pr/NLA-KE04-Krylov.stdout') == C['raw_Lean_log_sha256']

report = '''# KE-04 Krylov author completion

The five frozen range, shift, independence, full-prefix and largest-iteration
contracts compile with their exact approved types. This is a bounded helper
completion, not independent mathematical review or complete KE-04 verification.

The proof uses the genuine span of indexed matrix-power columns. Its coefficient
map is the finite linear-combination map; independence follows from finite span
dimension and restricts along the injective prefix embedding. At positive block
width, full rank bounds the iteration by the ambient dimension, and the first
full iteration makes the finite set nonempty. `Nat.findGreatest` therefore yields
the actual greatest full iteration. Zero block width is not silently admitted to
that existence contract. No numerical search, interval calculation or native
decision certificate is required.

The mf16_final_referee agent drafted this helper. After its recorded checkpoint,
the coordinator completed five elaboration fixes and removed one unnecessary
`simpa` warning. The first coordinator build passed, then a separate fresh final
Definitions/Krylov/Inspect build passed. Both attempts and the original failed
agent attempt remain byte-for-byte recorded. The historical checkpoint's old
source hash refers to its exact retained attempt source, not today's live module.

The final inspection compared all five actual theorem types to proof-free
propositions extracted from frozen Challenge headers. It traversed the actual
type/body closure of 30 project declarations and retained 14 required material
dependencies. Fourteen source and five inspection LeanCert kernel assertions
passed; their 19 axiom reports contain only propext, Classical.choice, Quot.sound.
Definitions has no warnings. The mathematical proof retains one harmless unused
`hr` simp-argument warning, without changing its successful elaboration. The inspection has three
retained, harmless unused hypothesis-name warnings in expected propositions;
their hypotheses remain universally quantified and no linter was disabled.

All 1598 frozen statement inputs matched. The final run checked all ten pinned
source repositories before and after compilation and used nine existing read-only
dependency object directories. It compiled three project modules into an empty
private prefix, hashed all generated objects and removed only that owned prefix.
This macOS author check is not an actual Ubuntu/default-kernel/Comparator run.

Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA, with
substantial AI assistance. Original mathematical proof: Matthew J. Colbrook.
The coordinator and original helper contributor are proof authors, not independent
final referees of KE-04. Canonical status, IDs, metadata, Git and publication are
unchanged by this helper handoff.
'''
assert not (E / 'HANDOFF.md').exists()
(E / 'HANDOFF.md').write_text(report)
write(E / 'HANDOFF.json', {
    'utc': datetime.now(timezone.utc).isoformat(),
    'status': 'COMPLETE_SCOPED_AUTHOR_VALIDATION',
    'source': {'path': 'NLA/KE04/Krylov.lean', **rec(P / 'NLA/KE04/Krylov.lean')},
    'final_attempt': str(A.relative_to(P)),
    'final_result': rec(A / 'result.json'),
    'frozen_contracts': 5, 'actual_project_closure': 30,
    'required_material_dependencies': 14,
    'fresh_source_commands': 3, 'kernel_assertions_and_axiom_reports': 19,
    'expected_type_binder_warnings': warnings, 'source_warnings': source_warnings,
    'preserved_statement_inputs': 1598,
    'original_source_archive': 'verification/krylov-development/attempt-z68t67pr/source/NLA/KE04/Krylov.lean',
    'original_source_sha256': C['module_sha256'],
    'independent_review': False, 'actual_linux_comparator': False,
    'complete_problem_verified': False,
})
verifier = '''#!/usr/bin/env python3
"""Read-only exact bounded seal check. Never rerun or rewrite evidence."""
from pathlib import Path
import hashlib,json
E=Path(__file__).resolve().parent
P=E.parents[1]
M=E/'EVIDENCE-MANIFEST.json'
D=json.loads(M.read_text())
assert D['exact_self_exclusion']==str(M.relative_to(P))
for rel,r in D['files'].items():
 p=P/rel
 assert p.is_file() and not p.is_symlink(),rel
 assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],rel
 assert p.stat().st_size==r['bytes'],rel
for scope in D['complete_evidence_directories']:
 actual={str(p.relative_to(P)) for p in (P/scope).rglob('*') if p.is_file() and p!=M}
 expected={rel for rel in D['files'] if rel.startswith(scope+'/')}
 assert actual==expected,(scope,actual-expected,expected-actual)
F=json.loads((P/'reviews/statement-freeze.json').read_text())
for rel,h in F['files'].items():
 assert hashlib.sha256((P/rel).read_bytes()).hexdigest()==h,rel
print(json.dumps({'pass':True,'bound_files':len(D['files']),
 'preserved_statement_inputs':len(F['files']),
 'independent_review':False,'actual_linux_comparator':False}))
'''
assert not (E / 'verify_seal.py').exists()
(E / 'verify_seal.py').write_text(verifier)
scopes = ['verification/krylov-development', str(E.relative_to(P))]
paths = {p for scope in scopes for p in (P / scope).rglob('*') if p.is_file() and p != M}
paths |= {P / rel for rel in [
    'NLA/KE04/Krylov.lean', 'NLA/KE04/Definitions.lean', 'Challenge.lean',
    'NUMERICAL_TARGETS.md', 'SourceCorrespondence.md', 'comparator.json',
    'lean-toolchain', 'lakefile.toml', 'lake-manifest.json',
    'reviews/statement-freeze.json', 'verification/proof-start.json']}
assert not any(p.is_symlink() for p in paths)
write(M, {'scope': 'All old checkpoint and new coordinator Krylov evidence, exact current helper and frozen statement anchors; no concurrent helper scope',
          'exact_self_exclusion': str(M.relative_to(P)),
          'complete_evidence_directories': scopes,
          'files': {str(p.relative_to(P)): rec(p) for p in sorted(paths)}})
print(json.dumps({'source': sha(P / 'NLA/KE04/Krylov.lean'),
                  'handoff': sha(E / 'HANDOFF.json'),
                  'outer': sha(M), 'bound_files': len(paths)}))
