from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, subprocess

R = Path('/tmp/nla-lean-ra20-worktree')
P = R / 'randomized-and-low-rank-approximation/RA-20/lean'
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
G = P / 'verification/final-review-acceptance.json'
assert not G.exists(), 'One-shot final acceptance'
freeze = P / 'verification/proof-freeze.json'
assert h(freeze) == 'f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f'
f = json.loads(freeze.read_text())
statement = P / 'reviews/statement-freeze.json'
s = json.loads(statement.read_text())
for boundary in [f, s]:
    for rel, digest in boundary['files'].items():
        assert h(P / rel) == digest, rel
assert len(f['files']) == 521 and len(s['files']) == 68
for rel, digest in f['source_files'].items():
    assert h(R / rel) == digest, rel
    blob = subprocess.check_output(['git', 'show', f['base'] + ':' + rel], cwd=R)
    assert hashlib.sha256(blob).hexdigest() == digest, rel
    oid = subprocess.check_output(['git', 'rev-parse', f['base'] + ':' + rel], cwd=R, text=True).strip()
    assert oid == f['source_git_blobs'][rel], rel
assert len(f['source_files']) == 16
names = json.loads((P / 'comparator.json').read_text())['theorem_names']
assert len(names) == 12
allowed = {'propext', 'Classical.choice', 'Quot.sound'}

def inventory(path, expected_sha, count):
    assert h(path) == expected_sha
    members = json.loads(path.read_text())['files']
    assert len(members) == count
    internal, resolved_members = set(), set()
    for rel, value in members.items():
        q = (path.parent / rel).resolve()
        resolved_members.add(str(q))
        assert q.is_relative_to(R.resolve()), str(q)
        digest = value if isinstance(value, str) else value['sha256']
        assert h(q) == digest, (path.name, rel)
        if isinstance(value, dict) and 'bytes' in value:
            assert q.stat().st_size == value['bytes'], rel
        if q.is_relative_to(path.parent.resolve()):
            internal.add(str(q.relative_to(path.parent.resolve())))
    actual = {str(q.relative_to(path.parent)) for q in path.parent.rglob('*') if q.is_file() and q != path}
    assert internal == actual, (actual - internal, internal - actual)
    for rel in f['files']:
        assert str((P / rel).resolve()) in resolved_members, rel
    return {'file': str(path.relative_to(P)), 'sha256': expected_sha, 'bound_files': count}

reviews = []
for number, report_sha, outer_sha, count, validation_name, validation_sha in [
    (1, '2a313084cdc1c06be789181bf05d9874bde020483d501151bc224b5af896e345',
     '360b0d841ebd8cb7219b39997e0b0a2617be32abfef461866d0f022ca134f70d', 699,
     'validated-results.json', '2a73677b8f9daf002858dc0a9e4fcc0af7a4d1709c21fa7e44f2b0d05aeb79a6'),
    (2, 'd7cfa1404c147ae19cec776e2047c85b6bdfd1484192a1cbbb171ed9afa7dbcf',
     '7fc642361790960be2d3a584d2842dc688d13511d93220907abc0d7ab951318c', 793,
     'validation.json', '5118411b069f1efbc9dc499a88adf768daae58331a14b7546354c030fed7eb3b')]:
    E = P / f'reviews/final-referee-{number}-evidence'
    report = P / f'reviews/final-referee-{number}.md'
    assert h(report) == report_sha
    assert h(E / validation_name) == validation_sha
    inv = inventory(E / 'EVIDENCE-MANIFEST.json', outer_sha, count)
    final = json.loads((E / 'FINAL.json').read_text())
    assert final['verdict'] == 'APPROVE' and final['report_sha256'] == report_sha
    dirs = sorted(E.glob('attempt-*' if number == 1 else 'command-*'))
    commands, reports, source_assertions = [], [], 0
    for d in dirs:
        record = json.loads((d / 'result.json').read_text())
        if not record.get('source'):
            continue
        assert record['exit_code'] == 0, (number, d.name)
        source = P / record['source']
        expected = record.get('source_sha256', record.get('sha256'))
        assert h(source) == expected, source
        snapshot = d / (source.name if number == 1 else 'source.lean')
        assert h(snapshot) == expected
        log = d / ('lean.log' if number == 1 else 'raw.log')
        if 'output_sha256' in record:
            assert h(log) == record['output_sha256']
        raw = log.read_text()
        for name, axioms in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", raw):
            ax = {x.strip() for x in axioms.split(',') if x.strip()}
            assert ax <= allowed, (number, name, ax)
            reports.append({'name': name, 'axioms': sorted(ax), 'log': str(log.relative_to(P)), 'log_sha256': h(log)})
        if record['source'].startswith('NLA/') or record['source'] == 'Solution.lean':
            assert expected == f['files'][record['source']]
            source_assertions += len(re.findall(r'^#assert_trust kernel\b', source.read_text(), re.M))
        commands.append({'source': record['source'], 'source_sha256': expected, 'exit_code': 0,
                         'log': str(log.relative_to(P)), 'log_sha256': h(log)})
    assert len(commands) == 13, (number, len(commands))
    assert len(reports) == 69 and source_assertions == 61, (number, len(reports), source_assertions)
    inspector_log = E / ('attempt-13/lean.log' if number == 1 else 'command-050/raw.log')
    raw = inspector_log.read_text()
    prefix = 'EXACT_FROZEN_TYPE ' if number == 1 else 'EXACT_REFERENCE_TYPE '
    actual = re.findall(re.escape(prefix) + r'(NLA\.RA20\.[A-Za-z_]+):', raw)
    assert actual == names, (number, actual)
    closure = re.search(r'PROJECT_COUNTS declarations=(\d+), required=(\d+)' if number == 1
                        else r'CLOSURE_COMPLETE declarations=(\d+); material_dependencies=(\d+)', raw)
    assert closure and tuple(map(int, closure.groups())) == (214, 39 if number == 1 else 28)
    if number == 1:
        assert 'ALL_PROJECT_DECLARATIONS 236' in raw
    namespace = 'Referee1Reference' if number == 1 else 'RefereeTwoContract'
    reference = E / ('ReferenceChallenge.lean' if number == 1 else 'Reference.lean')
    expected_reference = (P / 'Challenge.lean').read_text().replace('namespace NLA.RA20', 'namespace NLA.RA20.' + namespace).replace('end NLA.RA20', 'end NLA.RA20.' + namespace)
    assert reference.read_text() == expected_reference
    reviews.append({'reviewer': f'/root/ra20_final_referee{number}', 'report': str(report.relative_to(P)),
                    'sha256': report_sha, 'evidence': inv, 'validation_sha256': validation_sha,
                    'successful_fresh_source_commands': 13, 'failed_Lean_commands': 0,
                    'exact_export_type_matches': names, 'actual_project_closure': 214,
                    'required_material_dependencies': 39 if number == 1 else 28,
                    'source_kernel_assertions': 61, 'additional_kernel_assertions': 12,
                    'actual_standard_three_reports': 69, 'commands': commands, 'axiom_reports': reports,
                    'mathematical_revision_requested': False})

gate = {'utc': datetime.now(timezone.utc).isoformat(),
        'gate': 'ACCEPT both independent final mathematical approvals; candidate packaging and actual Linux may proceed',
        'coordinator': '/root',
        'coordinator_role': 'Disclosed Generic proof contributor and proof coordinator; not an independent final mathematical referee',
        'reviewed_proof_freeze_sha256': h(freeze), 'statement_freeze_sha256': h(statement),
        'project_inputs_preserved': 521, 'statement_inputs_preserved': 68,
        'original_source_Git_blobs_preserved': 16, 'reports': reviews,
        'root_review': 'Both full final mathematical reports, actual public contracts and definitions, complete proof map, Count and Generic proofs, Proof and Solution assemblies, and both exact-type/dependency inspectors read. Complete frozen files, original Git identities and both full referee inventories rehashed. All actual successful source/log/snapshot identities, twelve namespace-only reference matches and both sets of69 printed axiom reports independently checked. No new source compilation claimed by this acceptance.',
        'scope': 'Full original complex symmetric rank-at-most-two four-formula generic smooth critical-count conjecture negated at n=s=3. Actual reduced coordinate ring, algebraic smooth locus and entire vanishing ideal tangent, complex bilinear full-entry Frobenius derivatives, arbitrary nonempty generic-open intersection and actual cardinality are proved; no real-only or chosen-generic-set restriction.',
        'numerical_scope': 'Exact algebra/calculus/cardinality with LeanCert kernel-trust assertions; no interval certificate or native oracle',
        'nonblocking_findings': ['The abcLocalChart comment says complete local ring; its actual type is ordinary localization, not adic completion. Disclose in candidate prose and preserve frozen source.', 'Hessian nondegeneracy is exported; a separate scheme-theoretic multiplicity theorem is not claimed.', 'Historical statement README, correspondence, proof map and source phase notices retain their earlier wording. Archive exact README before replacement, label historical notices, and explicitly build/check Solution because the Lake default remains Challenge.'],
        'required_next_steps': ['Truthful reviewed candidate README and v0.4 formalization.yaml, with exact historical wrapper archive', 'Independent concrete packaging audit; blank-email commit and fork push', 'Actual non-root Ubuntu Comparator, default-kernel replay and full control suite', 'Independent operational audit, reviewed canonical publication/index/PDF updates and individual upstream main PR'],
        'canonical_status': 'Solved, unchanged', 'actual_Linux_Comparator': 'pending', 'publication': 'pending'}
G.write_text(json.dumps(gate, indent=2) + '\n')
(P / 'verification/accept_final_reviews.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({'gate_sha256': h(G), 'proof_inputs': 521, 'original_sources': 16,
                  'reviewers': [{'reviewer': r['reviewer'], 'report_sha256': r['sha256'],
                                 'bound_evidence_files': r['evidence']['bound_files'],
                                 'fresh_commands': 13, 'axiom_reports': 69} for r in reviews]}, indent=2))
