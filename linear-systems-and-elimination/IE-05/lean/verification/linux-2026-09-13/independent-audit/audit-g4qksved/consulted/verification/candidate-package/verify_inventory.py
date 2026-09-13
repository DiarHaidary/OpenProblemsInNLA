#!/usr/bin/env python3
"""Read-only exact-path archive and candidate inventory validation; never runs Lean.

The default checks exact current candidate membership. After a later phase adds
files, --candidate-members-only checks the same fixed candidate selection without
pretending that a historical whole-tree boundary includes those later files.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

PROJECT = Path(__file__).resolve().parents[2]
EVIDENCE = 'verification/candidate-package/'
OUTER = 'verification/candidate-inputs.json'
GATE = '6e1de72e81a0603066544133f7bb52a7217b31bd6f05372a8c1abe109ff03d61'
PROOF_FREEZE = '72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251'
STATEMENT_FREEZE = 'bd329885eb323bd4f3fd40879649b56c201918d8c2bd6f63fbd0e86f48ca770c'
WRAPPERS = {'README.md', 'SourceCorrespondence.md', 'lakefile.toml'}

def require(ok, detail):
    if not ok:
        raise ValueError(detail)

def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'Duplicate JSON key: {key!r}')
        result[key] = value
    return result

def load(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_pairs)

def record(path):
    b = path.read_bytes()
    return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def normalized(root, key):
    require(isinstance(key, str) and not Path(key).is_absolute(), f'Absolute/non-string member: {key!r}')
    p = (PROJECT / root / key).resolve()
    require(p.is_relative_to(PROJECT), f'Escaping member: {root}/{key}')
    return p.relative_to(PROJECT).as_posix()

def files_inventory(data):
    return isinstance(data, dict) and isinstance(data.get('files'), dict) and bool(data['files']) and all(
        isinstance(v, str) and re.fullmatch('[0-9a-f]{64}', v) or
        isinstance(v, dict) and isinstance(v.get('sha256'), str) and re.fullmatch('[0-9a-f]{64}', v['sha256'])
        for v in data['files'].values())

def verify(preseal=False, candidate_members_only=False):
    current = {}
    for p in sorted(PROJECT.rglob('*')):
        rel = p.relative_to(PROJECT).as_posix()
        require(not p.is_symlink(), f'Symlink: {rel}')
        require(not ({'.git', '.lake'} & set(p.relative_to(PROJECT).parts)), f'Git/cache path: {rel}')
        if p.is_file():
            require(p.suffix not in {'.olean', '.ilean', '.o', '.so', '.a'}, f'Generated proof artifact: {rel}')
            current[rel] = record(p)
    archives = load(PROJECT / EVIDENCE / 'ARCHIVE-MAP.json')
    before = load(PROJECT / EVIDENCE / 'PRE-PACKAGE-INPUTS.json')
    wrappers = archives['wrapper_archives']
    require(set(wrappers) == WRAPPERS, 'Wrapper archive mapping scope changed')
    require(before['file_count'] == len(before['files']) == 2338, 'Original accepted membership changed')
    require(before['no_files_excluded'] is True, 'Original file exclusions introduced')
    require(before['required_gate_sha256'] == GATE, 'Original gate binding changed')
    for rel, item in wrappers.items():
        require(item['expected'] == before['files'][rel], f'Archive expected version: {rel}')
        require(item['archive'] == EVIDENCE + 'archive/pre-package/' + rel, f'Archive path: {rel}')
        require(current.get(item['archive']) == item['expected'], f'Archive bytes: {rel}')
        require(current.get(rel) != item['expected'], f'Live wrapper not refreshed: {rel}')

    checked_entries = 0
    redirects = 0
    def check(root, key, expected, sizes=None):
        nonlocal checked_entries, redirects
        logical = normalized(root, key)
        wanted = {'sha256': expected} if isinstance(expected, str) else expected
        require(re.fullmatch('[0-9a-f]{64}', wanted['sha256']) is not None, f'Invalid digest: {key}')
        size = wanted.get('bytes')
        if sizes is not None:
            require(key in sizes, f'Missing size binding: {key}')
            require(size is None or size == sizes[key], f'Conflicting size binding: {key}')
            size = sizes[key]
        selected = logical
        item = wrappers.get(logical)
        if item is not None and wanted['sha256'] == item['expected']['sha256']:
            require(size is None or size == item['expected']['bytes'], f'Archive size mismatch: {key}')
            selected = item['archive']
            redirects += 1
        actual = current.get(selected)
        require(actual is not None and actual['sha256'] == wanted['sha256'], f'Hash mismatch: {logical} -> {selected}')
        require(size is None or actual['bytes'] == size, f'Byte length mismatch: {logical}')
        if 'git_blob' in wanted:
            b = (PROJECT / selected).read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
            require(blob == wanted['git_blob'], f'Git blob mismatch: {logical}')
        checked_entries += 1
        return selected

    for rel, expected in before['files'].items():
        check('.', rel, expected)
    registry = archives['historical_inventory_roots']
    require(len(registry) == 29, 'Historical inventory registry count changed')
    discovered = set()
    for rel in before['files']:
        if rel.endswith('.json'):
            try:
                data = load(PROJECT / rel)
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
            if files_inventory(data):
                discovered.add(rel)
    require(discovered == set(registry), 'Historical files inventory omitted or invented')
    historical_counts = {}
    for rel, binding in sorted(registry.items()):
        require(current.get(rel) == binding['inventory'] == before['files'][rel], f'Historical manifest bytes: {rel}')
        data = load(PROJECT / rel)
        require(len(data['files']) == binding['member_count'], f'Historical membership: {rel}')
        sizes = data.get('file_sizes', data.get('sizes'))
        if sizes is not None:
            require(set(sizes) == set(data['files']), f'Historical size membership: {rel}')
        for key, expected in data['files'].items():
            check(binding['root'], key, expected, sizes)
        historical_counts[rel] = len(data['files'])

    api = load(PROJECT / 'reviews/statement-referee-2-evidence/api-source-binding.json')['files']
    require(set(api) == set(archives['primary_source_archives']) and len(api) == 7, 'Primary source archive membership')
    for key, item in archives['primary_source_archives'].items():
        require(item['expected'] == api[key], f'Primary source expected version: {key}')
        require(item['archive'] == EVIDENCE + 'primary-source-archives/' + key, f'Primary source archive path: {key}')
        check('.', item['archive'], item['expected'])

    original = load(PROJECT / 'verification/original-source-inventory.json')
    require(len(original['files']) == 27 and original['base'] == '5830ed4fb06da0659414a3deb2a40ad327aca052', 'Original source base or count')
    for name, digest, count in [('proof-freeze', PROOF_FREEZE, 1800), ('statement-freeze', STATEMENT_FREEZE, 733)]:
        rel = 'reviews/' + name + '.json'
        require(current[rel]['sha256'] == digest, f'Immutable {name} changed')
        freeze = load(PROJECT / rel)
        require(len(freeze['files']) == count, f'Immutable {name} membership')
        require(freeze['base'] == original['base'], f'{name} original base')
        require(set(freeze['source_files']) == set(freeze['source_git_blobs']) == set(original['files']), f'{name} original paths')
        for key, expected in original['files'].items():
            require(freeze['source_files'][key] == expected['sha256'] and freeze['source_git_blobs'][key] == expected['git_blob'], f'{name} original source identity: {key}')
    require(current['verification/final-review-acceptance.json']['sha256'] == GATE, 'Accepted gate changed')
    gate = load(PROJECT / 'verification/final-review-acceptance.json')
    require(gate['actual_linux_comparator'] == 'pending' and gate['whole_problem_verified'] is False, 'Historical acceptance runtime scope changed')
    for review in gate['reviews']:
        number = review['number']
        require(review['verdict'] == 'APPROVE', f'Review verdict: {number}')
        require(current[f'reviews/final-referee-{number}.md']['sha256'] == review['report_sha256'], f'Review report: {number}')
        require(current[f'reviews/final-referee-{number}-evidence/EVIDENCE-MANIFEST.json']['sha256'] == review['evidence_sha256'], f'Review seal: {number}')

    candidate_count = None
    if not preseal:
        candidate = load(PROJECT / OUTER)
        require(candidate['exact_self_exclusion'] == OUTER and OUTER not in candidate['files'], 'Candidate exact self-exclusion')
        require(candidate['file_count'] == len(candidate['files']), 'Candidate selected count')
        selection = json.dumps(candidate['files'], sort_keys=True, separators=(',', ':')).encode()
        require(candidate['selection_sha256'] == hashlib.sha256(selection).hexdigest(), 'Candidate source-selection digest')
        require(candidate['root'] == '.' and candidate['path_convention'] == 'project-relative POSIX paths', 'Candidate path convention')
        require(candidate['actual_linux_comparator'] == 'pending' and candidate['independent_packaging_approval'] == 'pending', 'Candidate phase claim')
        for rel, expected in candidate['files'].items():
            require(normalized('.', rel) == rel, f'Noncanonical candidate member: {rel}')
            require(current.get(rel) == expected, f'Live candidate bytes: {rel}')
        if not candidate_members_only:
            require(set(current) == set(candidate['files']) | {OUTER}, 'Candidate whole-tree membership changed; use a new phase seal for later additions')
        candidate_count = len(candidate['files'])
    return {
        'result': 'PASS', 'check_kind': 'packaging-author read-only byte/inventory check; no Lean execution or independent approval',
        'preseal': preseal, 'candidate_members_only': candidate_members_only,
        'original_accepted_files': len(before['files']), 'historical_inventory_count': len(registry),
        'historical_inventory_member_checks': sum(historical_counts.values()),
        'all_preservation_member_checks': checked_entries, 'exact_wrapper_archive_redirects': redirects,
        'original_source_git_blob_identities': 27, 'candidate_selected_files': candidate_count,
        'current_regular_files': len(current), 'historical_inventories': historical_counts,
        'actual_linux_comparator': 'pending',
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preseal', action='store_true', help='Check preserved scopes during authoring, before a new candidate outer exists')
    parser.add_argument('--candidate-members-only', action='store_true', help='Check fixed candidate members after explicitly separate later-phase additions')
    args = parser.parse_args()
    require(not (args.preseal and args.candidate_members_only), 'Choose one phase mode')
    print(json.dumps(verify(args.preseal, args.candidate_members_only), indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
