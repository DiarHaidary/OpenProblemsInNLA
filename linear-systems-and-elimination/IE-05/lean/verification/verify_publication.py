#!/usr/bin/env python3
"""Read-only integrity/metadata checks for the published IE-05 phase.

Historical inventories remain immutable. This verifier explicitly separates
the two refreshed publication metadata files and later evidence additions from
the old candidate phase. It does not execute Lean or independently certify math.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parents[1]
OUTER = 'verification/publication-inputs.json'
OLD = 'verification/candidate-inputs.json'
OLD_SHA = 'b1259a165e924357b5474dcb9620ab316dec218e31a95665138cde4359f285e7'
REFRESHED_METADATA = {'README.md', 'formalization.yaml'}
# This one Python bytecode file is part of the original immutable referee
# evidence. It is checked as inert bytes, never imported or executed.
HISTORICAL_PYC = 'reviews/final-referee-1-evidence/__pycache__/review.cpython-313.pyc'

def require(ok, detail):
    if not ok:
        raise ValueError(detail)

def record(p):
    b = p.read_bytes()
    return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'Duplicate key: {key}')
        result[key] = value
    return result

def load(p):
    return json.loads(p.read_text(), object_pairs_hook=unique)

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

def verify():
    historical = module('ie05_historical_inventory', P / 'verification/candidate-package/verify_inventory.py')
    preserved = historical.verify(preseal=True)
    require(record(P / OLD)['sha256'] == OLD_SHA, 'Historical candidate inventory changed')
    old = load(P / OLD)
    require(old['file_count'] == len(old['files']) == 2404, 'Historical candidate membership')
    selection = json.dumps(old['files'], sort_keys=True, separators=(',', ':')).encode()
    require(hashlib.sha256(selection).hexdigest() == old['selection_sha256'], 'Historical selection digest')
    for rel, expected in old['files'].items():
        if rel not in REFRESHED_METADATA:
            require(record(P / rel) == expected, f'Historical candidate member changed: {rel}')

    current = {}
    for p in sorted(P.rglob('*')):
        rel = p.relative_to(P).as_posix()
        require(not p.is_symlink(), f'Symlink: {rel}')
        require(not ({'.git', '.lake'} & set(p.relative_to(P).parts)), f'Cache/store path: {rel}')
        if '__pycache__' in p.relative_to(P).parts:
            require(rel in {HISTORICAL_PYC, str(Path(HISTORICAL_PYC).parent)}, f'New Python cache: {rel}')
        if p.is_file():
            require(p.suffix not in {'.olean', '.ilean', '.o', '.so', '.a'}, f'Generated proof object: {rel}')
            if p.suffix == '.pyc':
                require(rel == HISTORICAL_PYC and record(p) == old['files'][rel], f'Unsealed Python bytecode: {rel}')
            current[rel] = record(p)
    outer = load(P / OUTER)
    require(outer['phase'] == 'publication' and outer['root'] == '.', 'Publication phase/root')
    require(outer['exact_self_exclusion'] == OUTER and OUTER not in outer['files'], 'Publication self exclusion')
    require(outer['refreshed_historical_metadata'] == sorted(REFRESHED_METADATA), 'Metadata redirect scope')
    require(outer['historical_candidate_sha256'] == OLD_SHA, 'Historical boundary binding')
    require(len(outer['files']) == outer['file_count'], 'Publication file count')
    require(set(current) == set(outer['files']) | {OUTER}, 'Publication whole-tree membership changed')
    for rel, expected in outer['files'].items():
        require(not Path(rel).is_absolute() and (P / rel).resolve().is_relative_to(P), f'Escaping path: {rel}')
        require(current.get(rel) == expected, f'Publication member changed: {rel}')
    selected = json.dumps(outer['files'], sort_keys=True, separators=(',', ':')).encode()
    require(hashlib.sha256(selected).hexdigest() == outer['selection_sha256'], 'Publication selection digest')

    schema_dir = P / 'verification/candidate-package/schema'
    validator = module('ie05_preserved_manifest_validator', schema_dir / 'validate_manifest.py')
    validator.validate(P, load(schema_dir / 'v0.4.schema.json'))
    metadata = validator.yaml.load((P / 'formalization.yaml').read_text(), Loader=validator.UniqueSafeLoader)
    config = load(P / 'comparator.json')
    require(len(config['theorem_names']) == 17, 'Export count')
    require(metadata['toolchain']['dependencies'] == {a['name']: a['rev'] for a in load(P / 'lake-manifest.json')['packages']}, 'Dependency pins')
    status = metadata['status']
    require(status['actual_linux_comparator'] == status['independent_packaging_approval'] == 'accepted', 'Publication acceptance metadata')
    require(status['whole_problem_verified'] is True and status['canonical_status'] == 'Lean verified', 'Publication status')
    require(metadata['reproduction']['authoritative_Linux']['status'] == 'accepted', 'Linux reproduction status')
    require(metadata['review']['publication_inventory'] == OUTER, 'Live inventory metadata link')
    require(metadata['review']['candidate_inventory'] == OLD, 'Historical inventory metadata link')
    require(metadata['project']['authors'] == ['George Stepaniants'], 'Formalization author')
    require(metadata['project']['affiliations']['George Stepaniants'] == 'Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA', 'Formalization affiliation')
    import re
    for rel in ['README.md', 'SourceCorrespondence.md', 'formalization.yaml', 'NOTICE.md']:
        require(re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', (P / rel).read_text()) is None, f'Unexpected email: {rel}')

    operational = subprocess.run([sys.executable, str(P / 'verification/linux-2026-09-13/independent-audit/verify.py')], cwd=P, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    require(operational.returncode == 0, 'Operational evidence seal failed: ' + operational.stdout)
    operational_result = json.loads(operational.stdout)
    require(operational_result['verdict'] == 'PASS', 'Operational evidence verdict')
    print(json.dumps({'result': 'PASS', 'scope': 'publication byte integrity and metadata only; no Lean execution or new mathematical approval', 'publication_members': len(outer['files']), 'unchanged_historical_candidate_members': 2404 - len(REFRESHED_METADATA), 'refreshed_metadata': sorted(REFRESHED_METADATA), 'preserved_historical_inventories': preserved['historical_inventory_count'], 'original_source_identities': preserved['original_source_git_blob_identities'], 'operational_evidence_files': operational_result['bound_files'], 'exports': 17}, indent=2))

if __name__ == '__main__':
    verify()
