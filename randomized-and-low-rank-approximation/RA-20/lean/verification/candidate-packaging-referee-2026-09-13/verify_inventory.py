#!/usr/bin/env python3
"""Read-only independent RA20 packaging seal verification; no Lean/Linux/Git execution."""
from pathlib import Path
import hashlib
import json
import re

E = Path(__file__).resolve().parent
P = E.parents[1]
G = P.parents[2]
A = P / 'verification/linux-candidate-2026-09-13'
SELF = E / 'EVIDENCE-MANIFEST.json'
REPORT = P / 'reviews/candidate-packaging-referee-2026-09-13.md'
OLD = '7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
AUTHOR = '60f056cd293d2b093786a34e55b670975dd6b27e7e927acdbf8513438c28b381'


def sha(p):
    assert p.is_file() and not p.is_symlink(), str(p)
    return hashlib.sha256(p.read_bytes()).hexdigest()


def unique(pairs):
    d = {}
    for k, v in pairs:
        assert k not in d, ('duplicate JSON key', k)
        d[k] = v
    return d


def load(p):
    return json.loads(p.read_text(), object_pairs_hook=unique)


def check(path, expected, historical=False):
    path = path.resolve()
    h = expected if isinstance(expected, str) else expected['sha256']
    if historical and path == P / 'README.md' and h == OLD:
        path = P / 'verification/pre-candidate-README.md'
    assert sha(path) == h, str(path)
    if isinstance(expected, dict) and 'bytes' in expected:
        assert path.stat().st_size == expected['bytes'], str(path)


def verify(m=None):
    m = load(SELF) if m is None else m
    assert m['verdict'] == 'APPROVE: candidate packaging only'
    assert m['exact_self_exclusion'] == 'EVIDENCE-MANIFEST.json'
    assert m['file_count'] == len(m['files'])
    bound = {(E / n).resolve() for n in m['files']}
    assert len(bound) == len(m['files']) and SELF not in bound
    for name, expected in m['files'].items():
        check(E / name, expected)
    own = {p.resolve() for p in E.rglob('*') if p.is_file() and p.resolve() != SELF}
    assert {p for p in bound if p.is_relative_to(E)} == own
    assert len(own) == m['own_evidence_files_excluding_outer']
    assert REPORT in bound

    check(A / 'EVIDENCE-MANIFEST.json', AUTHOR)
    author = load(A / 'EVIDENCE-MANIFEST.json')
    assert len(author['files']) == author['file_count'] == 1010
    author_bound = {(A / n).resolve() for n in author['files']}
    assert author_bound | {A / 'EVIDENCE-MANIFEST.json'} <= bound
    author_own = {p.resolve() for p in A.rglob('*')
                  if p.is_file() and p.resolve() != A / 'EVIDENCE-MANIFEST.json'}
    assert len(author_own) == 32
    assert {p for p in author_bound if p.is_relative_to(A)} == author_own
    for name, expected in author['files'].items():
        check(A / name, expected)

    baseline = load(A / 'preflight.json')['baseline']
    assert len(baseline) == 958
    differences = []
    for name, expected in baseline.items():
        check(P / name, expected, historical=True)
        if sha(P / name) != expected['sha256']:
            differences.append(name)
    assert differences == ['README.md']
    author_project = {(P / n).resolve() for n in baseline}
    author_project |= {P / 'formalization.yaml', P / 'verification/pre-candidate-README.md'} | author_own
    assert {p for p in author_bound if p.is_relative_to(P)} == author_project
    assert len(author_project) == 992

    inventories = []
    for name in baseline:
        if name.endswith('EVIDENCE-MANIFEST.json') or name == 'reviews/statement-package-manifest.json':
            path = P / name
            nested = load(path)
            parent = P if name == 'reviews/statement-package-manifest.json' else path.parent
            for n, expected in nested['files'].items():
                check(parent / n, expected, historical=True)
            inventories.append((name, len(nested['files'])))
            assert path in bound
    assert len(inventories) == 14
    assert dict(inventories)['reviews/final-referee-1-evidence/EVIDENCE-MANIFEST.json'] == 699
    assert dict(inventories)['reviews/final-referee-2-evidence/EVIDENCE-MANIFEST.json'] == 793

    proof = load(P / 'verification/proof-freeze.json')
    statement = load(P / 'reviews/statement-freeze.json')
    assert len(proof['files']) == 521 and len(statement['files']) == 68
    assert proof['source_files'] == statement['source_files']
    assert proof['source_git_blobs'] == statement['source_git_blobs']
    for frozen in (proof, statement):
        for name, expected in frozen['files'].items():
            check(P / name, expected, historical=True)
    for i, (name, h) in enumerate(proof['source_files'].items(), 1):
        check(G / name, h)
        check(P / 'verification/original-sources' / name, h)
        command = load(E / ('command-%02d' % i) / 'result.json')
        assert command['command'] == ['git', 'show', proof['base'] + ':' + name]
        raw = (E / ('command-%02d' % i) / 'raw.log').read_bytes()
        assert hashlib.sha256(raw).hexdigest() == h
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == proof['source_git_blobs'][name]
    assert len(proof['source_files']) == 16

    snapshots = load(E / 'snapshots.json')
    for name, expected in snapshots.items():
        check(G / name, expected['sha256'])
        check(P / expected['snapshot'], expected['sha256'])
        assert (G / name).resolve() in bound
    expected_scope = author_bound | {A / 'EVIDENCE-MANIFEST.json', REPORT} | own
    expected_scope |= {(G / name).resolve() for name in snapshots}
    assert bound == expected_scope

    commands = sorted(E.glob('command-*'))
    assert len(commands) == 21
    for d in commands:
        cmd = load(d / 'command.json')
        result = load(d / 'result.json')
        assert result['exit_code'] == 0
        assert result['command'] == cmd['command'] and result['cwd'] == cmd['cwd']
        check(d / 'raw.log', result['log_sha256'])
    assert 'PASS (12 declarations)' in (E / 'command-17/raw.log').read_text()
    assert '217 permanent problem IDs against origin/main' in (E / 'command-18/raw.log').read_text()
    assert '217 permanent problem IDs against nla-upstream/main' in (E / 'command-19/raw.log').read_text()
    assert load(E / 'command-20/raw.log')['status'] == 'SEALED_INSTALLATION_PASS'
    assert (E / 'command-21/raw.log').read_bytes() == b''
    result = load(E / 'RESULT.json')
    assert result['status'] == 'INDEPENDENT_FIXED_CANDIDATE_CHECKS_PASS'
    assert len(result['relative_links']) == 29 and len(result['metadata_file_paths']) == 40
    assert result['all_twelve_exact_metadata_alignment_exports'] == load(P / 'comparator.json')['theorem_names']
    assert len(result['pinned_packages']) == 10
    assert result['new_Lean_builds'] == 0
    for record in result['relative_links']:
        check(G / record['target'], record['sha256'])
    for record in result['metadata_file_paths']:
        check(P / record['path'], record['sha256'])
    for field, name in [('README_sha256','README.md'), ('YAML_sha256','formalization.yaml'),
                        ('coordinator_gate_sha256','verification/final-review-acceptance.json')]:
        check(P / name, result[field])
    assert 'APPROVE' in REPORT.read_text()
    assert load(E / 'FINAL.json')['verdict'] == 'APPROVE: candidate packaging only'
    assert sha(REPORT) == load(E / 'FINAL.json')['report_sha256']

    email = re.compile(rb'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
    assert not any(email.search(p.read_bytes()) for p in own | {REPORT, P/'README.md', P/'formalization.yaml'}), 'Email-like text in new review material; do not display'
    return {
        'status': 'INDEPENDENT_PACKAGING_SEAL_PASS',
        'verdict': 'APPROVE: candidate packaging only',
        'file_count': len(bound),
        'own_evidence_files_excluding_outer': len(own),
        'installer_bound_inputs': 1010,
        'installer_outer_itself_bound': True,
        'baseline_preserved': 958,
        'proof_inputs': 521,
        'statement_inputs': 68,
        'original_live_snapshot_and_recorded_Git_identities': 16,
        'historical_nested_inventories': 14,
        'complete_final_review_inventories': [699,793],
        'successful_command_receipts': 21,
        'metadata_exports': 12,
        'pins': 10,
        'relative_links': 29,
        'metadata_paths': 40,
        'new_Lean_builds': 0,
        'actual_Linux_Comparator_default_kernel_controls': 'pending; not executed',
        'new_mathematical_approval': False,
        'canonical_status': 'Solved, unchanged',
        'operational_acceptance_and_publication': 'pending',
        'email_like_matches_in_new_review_material': 0,
        'inventory_scope': 'All fixed installer inputs and its outer manifest, all actual additional snapshotted tool inputs, own complete evidence and report; only exact own outer self excluded. Later acceptance/publication additions outside this evidence directory are outside this seal.'
    }


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
