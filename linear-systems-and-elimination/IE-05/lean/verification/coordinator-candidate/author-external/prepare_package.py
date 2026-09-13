#!/usr/bin/env python3
"""One-shot candidate authoring copy; never edits the accepted original draft."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
SOURCE = Path('/tmp/nla-lean-formalization/next-ie05-statements-draft/lean')
DEST = HERE / 'lean'
EVIDENCE = DEST / 'verification/candidate-package'
PACKAGES = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
GATE_SHA = '6e1de72e81a0603066544133f7bb52a7217b31bd6f05372a8c1abe109ff03d61'
ROOT_SEAL_SHA = 'b2b7643a19573ce128a531d9e701b4fcc25f0d28b5261fc88e54e1f03f10e678'

def record(p):
    b = p.read_bytes()
    return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def main():
    assert not DEST.exists(), 'One-shot preparation: destination already exists'
    assert record(SOURCE / 'verification/final-review-acceptance.json')['sha256'] == GATE_SHA
    assert record(SOURCE / 'verification/final-review-root-acceptance/EVIDENCE-MANIFEST.json')['sha256'] == ROOT_SEAL_SHA
    gate = json.loads((SOURCE / 'verification/final-review-acceptance.json').read_text())
    assert [r['verdict'] for r in gate['reviews']] == ['APPROVE', 'APPROVE']
    assert gate['actual_linux_comparator'] == 'pending' and gate['whole_problem_verified'] is False
    original = {}
    for p in sorted(SOURCE.rglob('*')):
        rel = p.relative_to(SOURCE).as_posix()
        assert not p.is_symlink(), rel
        assert not ({'.git', '.lake'} & set(p.relative_to(SOURCE).parts)), rel
        if p.is_file():
            assert p.suffix not in {'.olean', '.ilean', '.o', '.so', '.a'}, rel
            original[rel] = record(p)
    # All original files are copied: there is no ignore function or basename exemption.
    for rel, expected in original.items():
        dst = DEST / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / rel, dst)
        assert record(dst) == expected, rel
    archives = {}
    for rel in ['README.md', 'SourceCorrespondence.md', 'lakefile.toml']:
        archive = 'verification/candidate-package/archive/pre-package/' + rel
        dst = DEST / archive
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / rel, dst)
        archives[rel] = {'expected': original[rel], 'archive': archive}
        (DEST / rel).chmod(0o644)
    lakefile = DEST / 'lakefile.toml'
    old = lakefile.read_text()
    assert old.count('defaultTargets = ["Challenge"]') == 1
    lakefile.write_text(old.replace('defaultTargets = ["Challenge"]', 'defaultTargets = ["Solution"]'))

    roots = {
        'DRAFT-INVENTORY.json': '.',
        'reviews/final-referee-1-evidence/EVIDENCE-MANIFEST.json': '.',
        'reviews/final-referee-2-evidence/EVIDENCE-MANIFEST.json': '.',
        'reviews/final-referee-2-evidence/attempt-gxrxb23r/frozen-before.json': '.',
        'reviews/proof-freeze.json': '.',
        'reviews/statement-freeze.json': '.',
        'reviews/statement-referee-1-evidence/input-snapshot/DRAFT-INVENTORY.json': 'reviews/statement-referee-1-evidence/input-snapshot',
        'reviews/statement-referee-1-evidence/input-snapshot/verification/original-source-inventory.json': 'reviews/statement-referee-1-evidence/input-snapshot/verification/original-sources',
        'reviews/statement-referee-1-evidence/inputs.json': 'reviews/statement-referee-1-evidence/input-snapshot',
        'reviews/statement-referee-1-evidence/inspector-inputs.json': 'reviews/statement-referee-1-evidence/input-snapshot',
        'reviews/statement-referee-1-evidence/outer-manifest.json': '.',
        'reviews/statement-referee-2-evidence/EVIDENCE-SEAL.json': '.',
        'reviews/statement-referee-2-evidence/api-source-binding.json': 'verification/candidate-package/primary-source-archives',
        'reviews/statement-referee-2-evidence/input-binding.json': 'reviews/statement-referee-2-evidence/inputs',
        'reviews/statement-referee-2-evidence/inputs/DRAFT-INVENTORY.json': 'reviews/statement-referee-2-evidence/inputs',
        'reviews/statement-referee-2-evidence/inputs/verification/original-source-inventory.json': 'reviews/statement-referee-2-evidence/inputs/verification/original-sources',
        'verification/assembly-handoff/EVIDENCE-MANIFEST.json': '.',
        'verification/certificates-qr-handoff/EVIDENCE-MANIFEST.json': '.',
        'verification/certificates-qr-handoff/INPUTS.json': '.',
        'verification/exactcert-diagnostic-referee/EVIDENCE-MANIFEST.json': '.',
        'verification/final-review-root-acceptance/EVIDENCE-MANIFEST.json': '.',
        'verification/gepp-development/EVIDENCE-MANIFEST.json': '.',
        'verification/lu-development/EVIDENCE-MANIFEST.json': '.',
        'verification/original-source-inventory.json': 'verification/original-sources',
        'verification/qr-scaling-handoff/EVIDENCE-MANIFEST.json': 'verification/qr-scaling-handoff',
        'verification/statement-acceptance/EVIDENCE-MANIFEST.json': 'verification/statement-acceptance',
        'verification/statement-gate-preflight/EVIDENCE-SEAL.json': '.',
        'verification/statement-gate-preflight/proposed-input-binding.json': '.',
        'verification/witness-development/EVIDENCE-MANIFEST.json': '.',
    }
    api_rel = 'reviews/statement-referee-2-evidence/api-source-binding.json'
    api = json.loads((SOURCE / api_rel).read_text())
    primary = {}
    for rel, expected in api['files'].items():
        source = PACKAGES / rel
        assert record(source) == {k: expected[k] for k in ('sha256', 'bytes')}, rel
        blob = source.read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(blob)).encode() + b'\0' + blob).hexdigest() == expected['git_blob']
        archived = 'verification/candidate-package/primary-source-archives/' + rel
        dst = DEST / archived
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dst)
        primary[rel] = {'archive': archived, 'expected': expected,
                        'source_package': rel.split('/')[0],
                        'source_path_within_package': rel.split('/', 1)[1]}
    manifests = {}
    found = set()
    for rel in original:
        if not rel.endswith('.json'):
            continue
        try:
            data = json.loads((SOURCE / rel).read_text())
        except (ValueError, UnicodeDecodeError):
            continue
        if isinstance(data, dict) and isinstance(data.get('files'), dict) and data['files'] and all(
            isinstance(v, str) and len(v) == 64 or isinstance(v, dict) and isinstance(v.get('sha256'), str)
            for v in data['files'].values()
        ):
            found.add(rel)
            assert rel in roots, ('unregistered historical files inventory', rel)
            manifests[rel] = {'root': roots[rel], 'member_count': len(data['files']), 'inventory': original[rel]}
    assert found == set(roots), sorted(found.symmetric_difference(roots))
    write(EVIDENCE / 'PRE-PACKAGE-INPUTS.json', {
        'scope': 'Every regular file in the completed accepted original draft at packaging start',
        'original_directory': str(SOURCE), 'file_count': len(original), 'files': original,
        'no_files_excluded': True, 'required_gate_sha256': GATE_SHA,
        'required_root_seal_sha256': ROOT_SEAL_SHA,
    })
    write(EVIDENCE / 'ARCHIVE-MAP.json', {
        'rule': 'Redirect only an exact original project-relative path together with its exact expected old SHA-256 and byte length. Nested snapshot basenames do not match.',
        'wrapper_archives': archives, 'primary_source_archives': primary,
        'historical_inventory_roots': manifests,
    })
    shutil.copy2(Path(__file__), EVIDENCE / 'prepare_package.py')
    copied = {r: record(DEST / r) for r in original if r != 'lakefile.toml'}
    assert all(copied[r] == original[r] for r in copied)
    assert {p.relative_to(SOURCE).as_posix(): record(p) for p in sorted(SOURCE.rglob('*')) if p.is_file()} == original
    write(EVIDENCE / 'copy-result.json', {
        'author': 'OpenAI Codex /root/ie05_final_math_referee1, subsequent packaging-author role',
        'independent_packaging_review': False, 'original_files_copied': len(original),
        'historical_files_inventories': len(manifests), 'wrapper_archives': len(archives),
        'small_pinned_primary_source_archives': len(primary), 'original_unchanged': True,
        'dependency_caches_copied': False, 'git_objects_copied': False,
        'actual_linux_comparator': 'pending', 'new_lean_compilation': False,
    })
    print(json.dumps({'copied': len(original), 'historical_inventories': len(manifests), 'gate': GATE_SHA}))

if __name__ == '__main__':
    main()
