#!/usr/bin/env python3
"""Read-only, portable verification of the complete RA20 candidate installation.

Historical manifests keep their original bytes. Only their exact old project
README path plus old expected hash is redirected to the exact retained archive.
No dependency build, network access, or write occurs in this verifier.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import urllib.parse

E = Path(__file__).resolve().parent
P = E.parents[1]
R = P.parents[2]
OUTER = E / 'EVIDENCE-MANIFEST.json'
OLD = '7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
NEW_README = '83e19faf1bf25a9748de40da3193cfd68690100923a50379553e288c45b5e8bc'
NEW_YAML = 'bec9d851e204464fa2d3e29033d5958034665d51c3554d2043f1470bfafd4197'
GATE = 'a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb'
BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
BASELINE = 'a6540a7a937fc0298954cf5b508f0354881fec87e832f80f223773c6f9cd0210'

def digest(p):
    assert p.is_file() and not p.is_symlink(), ('missing or symlink input', str(p))
    return hashlib.sha256(p.read_bytes()).hexdigest()

def unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        assert k not in result, ('duplicate JSON key', k)
        result[k] = v
    return result

def load(p):
    return json.loads(p.read_text(), object_pairs_hook=unique_pairs)

def verify(p, entry, historical=False):
    expected = entry if isinstance(entry, str) else entry['sha256']
    original = p.resolve()
    if historical and original == (P / 'README.md').resolve() and expected == OLD:
        p = P / 'verification/pre-candidate-README.md'
    assert digest(p) == expected, ('wrong hash', str(original))
    if isinstance(entry, dict) and 'bytes' in entry:
        assert p.stat().st_size == entry['bytes'], ('wrong size', str(original))

def run(preseal=False):
    assert digest(E / 'preflight.json') == BASELINE
    b = load(E / 'preflight.json')
    assert b['baseline_count'] == len(b['baseline']) == 958
    for n, v in b['baseline'].items():
        verify(P / n, v, historical=True)
    assert [n for n, v in b['baseline'].items() if digest(P / n) != v['sha256']] == ['README.md']
    assert digest(P / 'README.md') == NEW_README
    assert digest(P / 'formalization.yaml') == NEW_YAML
    assert digest(P / 'verification/pre-candidate-README.md') == OLD
    assert digest(P / 'verification/final-review-acceptance.json') == GATE
    installation = load(E / 'installation.json')
    assert installation['README_sha256'] == NEW_README and installation['YAML_sha256'] == NEW_YAML
    assert installation['changed_existing_files'] == ['README.md']
    assert (E / 'draft/README.md').read_bytes() == (P / 'README.md').read_bytes()
    assert (E / 'draft/formalization.yaml').read_bytes() == (P / 'formalization.yaml').read_bytes()

    proof = load(P / 'verification/proof-freeze.json')
    statement = load(P / 'reviews/statement-freeze.json')
    assert len(proof['files']) == 521 and len(statement['files']) == 68
    assert proof['base'] == BASE
    assert proof['source_files'] == statement['source_files']
    assert len(proof['source_files']) == 16
    for frozen in [proof, statement]:
        for n, v in frozen['files'].items():
            verify(P / n, v, historical=True)
    env = os.environ.copy()
    env['GIT_OPTIONAL_LOCKS'] = '0'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for n, h in proof['source_files'].items():
        verify(R / n, h)
        verify(P / 'verification/original-sources' / n, h)
        raw = subprocess.check_output(['git', 'show', BASE + ':' + n], cwd=R, env=env)
        assert hashlib.sha256(raw).hexdigest() == h, ('original Git bytes', n)
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == proof['source_git_blobs'][n], n

    nested = []
    for n in b['baseline']:
        if n.endswith('EVIDENCE-MANIFEST.json') or n == 'reviews/statement-package-manifest.json':
            path = P / n
            m = load(path)
            relative_base = P if n == 'reviews/statement-package-manifest.json' else path.parent
            for k, v in m['files'].items():
                verify(relative_base / k, v, historical=True)
            nested.append({'file': n, 'sha256': digest(path), 'entries': len(m['files'])})
    assert len(nested) == 14
    gate = load(P / 'verification/final-review-acceptance.json')
    assert len(gate['reports']) == 2
    assert [r['evidence']['bound_files'] for r in gate['reports']] == [699, 793]
    for r in gate['reports']:
        verify(P / r['report'], r['sha256'])
        verify(P / r['evidence']['file'], r['evidence']['sha256'])
        assert len(load(P / r['evidence']['file'])['files']) == r['evidence']['bound_files']

    checks = load(E / 'CHECKS.json')
    assert checks['status'].startswith('AUTHOR_CHECKS_PASS')
    assert checks['all_prior_nested_manifests'] == nested
    assert checks['baseline_count'] == 958 and checks['exact_existing_changes'] == ['README.md']
    assert len(checks['commands']) == 3
    for i, command in enumerate(checks['commands'], 1):
        receipt = load(E / ('check-%d-result.json' % i))
        assert receipt == command and receipt['exit_code'] == 0
        assert (E / ('check-%d.log' % i)).stat().st_size > 0
    config = load(P / 'comparator.json')
    assert config['theorem_names'] == checks['actual_main_results']
    assert len(config['theorem_names']) == 12 and config['definition_names'] == []
    assert set(config['permitted_axioms']) == {'propext', 'Classical.choice', 'Quot.sound'}
    assert '**Status:** Solved' in (P.parent / 'README.md').read_text()
    assert 'lake build Solution' in (P / 'README.md').read_text()

    hygiene = load(E / 'HYGIENE.json')
    assert hygiene['status'] == 'AUTHOR_PUBLICATION_HYGIENE_PASS'
    assert hygiene['email_like_matches'] == 0
    for record in hygiene['relative_links'] + hygiene['metadata_file_paths']:
        target = R / record['target']
        if preseal and target.resolve() in {OUTER.resolve(), (E / 'VALIDATION.json').resolve()}:
            continue
        assert target.is_file(), ('missing published link', record['target'])
        if 'sha256' in record:
            verify(target, record['sha256'])
    for record in hygiene['immutable_original_source_links']:
        assert record['matches_base_and_live'] is True
    email = re.compile(rb'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
    material = [P / 'README.md', P / 'formalization.yaml', P / 'verification/pre-candidate-README.md']
    material += [p for p in sorted(E.rglob('*')) if p.is_file()]
    assert not [str(p.relative_to(P)) for p in material if email.search(p.read_bytes())], 'email-like publication material'

    own = {p.resolve() for p in E.rglob('*') if p.is_file() and p.resolve() != OUTER.resolve()}
    allowed_new = {'formalization.yaml', 'verification/pre-candidate-README.md'}
    if preseal:
        assert not OUTER.exists(), 'preseal must precede the one-shot outer seal'
        additions = [str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and str(p.relative_to(P)) not in b['baseline']]
        assert all(n in allowed_new or n.startswith(str(E.relative_to(P)) + '/') for n in additions)
        count = None
    else:
        m = load(OUTER)
        assert m['exact_self_exclusion'] == 'EVIDENCE-MANIFEST.json'
        assert m['baseline_count'] == 958
        assert m['file_count'] == len(m['files'])
        assert m['README_sha256'] == NEW_README and m['YAML_sha256'] == NEW_YAML
        bound = {(E / n).resolve() for n in m['files']}
        assert OUTER.resolve() not in bound
        assert {q for q in bound if q.is_relative_to(E)} == own, 'complete own evidence coverage'
        required_project = {(P / n).resolve() for n in b['baseline']}
        required_project |= {(P / n).resolve() for n in allowed_new}
        required_project |= own
        assert {q for q in bound if q.is_relative_to(P)} == required_project, 'complete project installation coverage'
        external = {(R / n).resolve() for n in proof['source_files']}
        external |= {R / 'tools/lean/validate_manifest.py', R / 'tools/validate_problem_ids.py'}
        assert bound - required_project == external, 'complete frozen originals and check-tool coverage'
        for n, v in m['files'].items():
            target = (E / n).resolve()
            assert target.is_relative_to(R), ('bound file outside repository', n)
            verify(target, v)
        assert m['nested_historical_inventories'] == nested
        assert m['original_sources'] == proof['source_files']
        assert m['original_source_git_blobs'] == proof['source_git_blobs']
        assert load(E / 'VALIDATION.json')['status'] == 'PRESEAL_INPUTS_PASS'
        count = len(m['files'])
    return {
        'status': 'PRESEAL_INPUTS_PASS' if preseal else 'SEALED_INSTALLATION_PASS',
        'role': 'Candidate-document author consistency check; no independent packaging approval',
        'baseline_count': 958,
        'existing_files_changed': ['README.md'],
        'unchanged_existing_paths': 957,
        'exact_old_README_archive_sha256': OLD,
        'proof_inputs': 521,
        'statement_inputs': 68,
        'original_source_snapshot_and_base_Git_checks': 16,
        'complete_final_review_inventories': [699, 793],
        'nested_historical_inventories': 14,
        'schema_and_ID_commands_passed': 3,
        'Comparator_exports': 12,
        'README_sha256': NEW_README,
        'YAML_sha256': NEW_YAML,
        'root_gate_sha256': GATE,
        'installation_sha256': digest(E / 'installation.json'),
        'complete_bound_files': count,
        'complete_manifest_sha256': None if preseal else digest(OUTER),
        'own_evidence_files_excluding_outer': len(own),
        'publication_email_like_matches': 0,
        'independent_packaging_review': 'pending',
        'actual_RA20_Linux_Comparator_default_kernel_controls': 'pending',
        'independent_operational_acceptance': 'pending',
        'canonical_status': 'Solved, unchanged',
        'publication': 'pending',
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preseal', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(args.preseal), indent=2))
