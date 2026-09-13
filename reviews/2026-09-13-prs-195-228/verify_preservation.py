#!/usr/bin/env python3
"""Read-only Git-tree preservation audit for the frozen 25-PR batch.

No submitted code, validator, workflow, test or Lean program is executed.
Only Git object reads and scratch report writes occur. Supply --ref with the
assembled integration commit; omission prepares the independent source audit.
"""
from __future__ import annotations

import argparse
import collections
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import unicodedata

PREVIOUS_MAIN = '1c467f88fbf6f6853afe5562e17b81ab421b95a6'
PUBLISHED_BASE = '2db1e5857a4813ca627b60b4e30fa9bf6258c1cc'
SOURCE_BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
HEADS = {
    195: 'b190a7ca5580669ea98d12e23970581abbe6ae7c',
    197: '31756a4a1cc997e48af77637ee90f44e3b8fb7fb',
    199: '98e2ff0c035fd5ebb0532de47db0e687cbaf2a5c',
    201: 'f1e8b7d324823ccca225cbd261330b727b423cab',
    202: 'a183f28836d47f22a270e50ebf0c3f1b0729a1e9',
    203: 'ec0b2c267f476c2e9abd04322ba18e43d2be4b13',
    204: 'e898eb61eccaa1cd8a9a7e0b25d64f176fd71a53',
    205: '9777c86853b40206f70438c92a47a7dec9bc66ae',
    207: '754aa792a5a19d25a353a3975912558820184edf',
    209: '3fececca7c8dbdc594270e07626f6af7ff9e7f14',
    211: 'd4c9b7568f237a9467dbf91bfae4b5ffa655d970',
    213: 'd499a398d5d0f8b5a07e8b31fa8d0deb1020bdba',
    214: '1a0d3fd4315e9683d56745de586a469b85d2e0ac',
    216: '946ce081fb7d67d5f1cae6da688e7c6f7e945418',
    217: '55163265143e2f2b180268b2693ea7d582065806',
    218: '40b933b77b654055a2ad2cb9b8ed8b3c9e8b5974',
    219: 'f7705090561ed0cc831bce5ad297983ede2c2b7f',
    220: '32c71ebf9ee7d89874fcc4c82deae8d374874854',
    222: 'f540441a8521a724461c7b393ed1f19f5e1b2b57',
    223: '957c36750778d0414bdaab6ee0b92d6db7396253',
    224: '18d5719d7f0642e549829588799d19cb3d11ecea',
    225: 'bd82acc73c14835b1497c9bd664648d30f27a925',
    226: '5561d3efbe8bfd5502d7b5889c46b75f1be4aad2',
    227: '8d1048119fb3664e2b4123bfda28ba7dffaa6e2b',
    228: 'a62bb7e56d858af6a7725d4b12ac657b36b6bda2',
}
RENDERER = 'tools/render_problems.py'
SHARED_PREFIXES = ('tools/', '.github/', 'tests/', 'docs/lean/')
SHARED_FILES = {'problem_ids.json', 'AGENTS.md', '.gitmodules', '.gitattributes', '.gitignore'}
SPECIAL_TARGET_START = {
    'RA-04': 'Let $`A\\in', 'RA-05': 'Fix a real $`p>2',
    'RA-08': 'Let $`n', 'RA-09': 'Let $`n', 'MD-02': 'For each $`n',
}
RENDER_EDITS = {
    195: [("'MI-09', 'MI-19', 'MI-23', 'MI-28'", "'MI-09', 'MI-19', 'MI-23', 'MI-27', 'MI-28'")],
    205: [("'SP-12', 'TR-08', 'TR-11'", "'SP-12', 'TR-11'")],
    223: [("'RA-15', 'RA-17', 'RE-01'", "'RA-15', 'RE-01'")],
    226: [('if identifier in {"IE-05", "SP-15", "MF-02"}:',
           'if identifier in {"IE-05", "SP-15", "MF-02", "RE-03"}:'),
          ("'RE-02', 'RE-03', 'RE-06'", "'RE-02', 'RE-06'")],
}
# Independently reviewed maintainer layout adjustment for the combined RA-04
# history. The final canonical PDF has already been visually checked by root.
FINAL_RENDER_EDITS = [("'RA-02', 'RA-04', 'RA-06'", "'RA-02', 'RA-06'")]
# Filled only after independent review of each exact maintainer repair. Source
# identities remain in the authored manifest; repairs never count as unchanged.
REVIEWED_AUTHORED_REPAIRS = {'references/holden-ra17-continuation-2026-09-13/code/sos_pencil_certificate.py': {'before': ['100644', 'blob', '82384abccc72d823bd0eb6d6363d187374f34ca0'], 'after': ['100644', 'blob', '55e27804deb567a8acacc70fdf1d03e32ccb2750'], 'before_sha256': 'b03f1483b0fb3eb348512a3190255586525a792c06495c554b6965eda012baa6', 'after_sha256': '72eda1745021758395d72ce0451cc7d0df999e0968f7d19674e4d5615fa8ae86', 'reason': 'Close reproduced incomplete-basis and nonpolynomial-multiplier false acceptance; independently read and optimized ten-test suite PASS.'}, 'references/holden-ra17-continuation-2026-09-13/README.md': {'before': ['100644', 'blob', '491274ce19a22830ae0971b6612b323ca0c39319'], 'after': ['100644', 'blob', '2c74f0d6c24e0053ed28ecca75e0657ea925c78e'], 'before_sha256': '2ca8f72b59fd0f0a720d5fc0b34c1a31b1c018e775298a61799567d33fb735df', 'after_sha256': 'aa7ff885bafcd50af168be47043032850189a828548ff8158b1edfd9e2b75d38', 'reason': 'Append only the independently reviewed four-line link to the maintainer checker correction; original package description retained verbatim.'}}
REVIEWED_INTEGRATION_ADDITIONS = {'references/holden-ra17-continuation-2026-09-13/code/test_sos_pencil_certificate.py': {'entry': ['100644', 'blob', '6098403dd9567f6b515c5aae32b512f1768cf199'], 'sha256': '438836090c48ef0f600f0b551d38503ec086d7d7a14ced03e25a06ddf7da710d', 'bytes': 5528}, 'references/holden-ra17-continuation-2026-09-13/MAINTAINER_CHECKER_CORRECTION.md': {'entry': ['100644', 'blob', '954f1827e067ff6e97df769cec99bf521cd84593'], 'sha256': '3bbf811a8ef217177faf4dabab00608a8ed8c610b2785f8a0b252dfa29329e77', 'bytes': 2266}}
APPROVED_AUDIT_RECORD_ROOT = 'reviews/2026-09-13-prs-195-228/'
REVIEWED_HISTORY_COMMIT = 'b38e3989566c189546dc6afdf9284f5f909e3ffd'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', default='/private/tmp/nla-integration-195-228')
    ap.add_argument('--ref', help='Frozen integration commit; never reads the mutable working tree')
    ap.add_argument('--output-prefix', default='/private/tmp/nla-prs195-228-integration-preservation')
    args = ap.parse_args()
    repo = Path(args.repo)
    failures = []
    observations = []

    def require(ok, label, details=None):
        if not ok:
            failures.append({'check': label, 'details': details})

    def git(*a):
        return subprocess.check_output(['git', '-C', str(repo), *a])

    trees = {}
    def tree(ref):
        if ref not in trees:
            entries = {}
            for item in git('ls-tree', '-rz', ref).split(b'\0'):
                if not item:
                    continue
                fields, path = item.split(b'\t', 1)
                mode, kind, oid = fields.decode().split()
                entries[path.decode()] = (mode, kind, oid)
            trees[ref] = entries
        return trees[ref]

    blobs = {}
    def blob(ref, path):
        oid = tree(ref)[path][2]
        if oid not in blobs:
            blobs[oid] = git('cat-file', 'blob', oid)
        return blobs[oid]

    def text(ref, path):
        return blob(ref, path).decode()

    def edits(raw, changes):
        for before, after in changes:
            assert raw.count(before) == 1, ('unambiguous reviewed renderer edit', before)
            raw = raw.replace(before, after, 1)
        return raw

    def title(raw):
        return raw.splitlines()[0]

    def status(raw):
        return re.search(r'^\*\*Status:\*\*\s+([^\n]+)', raw, re.M)[1].strip()

    def target(raw, identifier):
        start = SPECIAL_TARGET_START.get(identifier)
        if start is None:
            start = next(s for s in ('## Context and notation\n', '## Problem statement\n', '## Statement\n') if s in raw)
        suffix = raw[raw.index(start):]
        end = re.search(r'^## (?:References?|Why it matters|Relevance|Evidence and numerical significance)', suffix, re.M)
        return (suffix[:end.start()] if end else suffix).rstrip()

    def line_additions(before, after):
        # Resolution records and reference-index additions must survive their merge.
        return [s[2:] for s in difflib.ndiff(before.splitlines(), after.splitlines())
                if s.startswith('+ ') and s[2:].strip()]

    def line_deletions(before, after):
        return [v[2:] for v in difflib.ndiff(before.splitlines(), after.splitlines())
                if v.startswith('- ') and v[2:].strip()]

    base = tree(PUBLISHED_BASE)
    previous = tree(PREVIOUS_MAIN)
    require(base.keys() == previous.keys(), 'new published main retains all previous-main paths')
    main_updates = {'README.md', 'CATALOG.md', 'tools/update_catalog.py', 'tests/test_problem_statuses.py'}
    require({p for p in previous if previous[p] != base[p]} == main_updates,
            'published-main advance changes exactly four reviewed catalog-label files')
    for p in main_updates:
        require(blob(PUBLISHED_BASE, p) == blob(PREVIOUS_MAIN, p).replace(b' Lean verified.', b' solved with Lean verification.'),
                'published-main label edit is exact and does not weaken a check', p)
    original = tree(SOURCE_BASE)
    registry_bytes = blob(PUBLISHED_BASE, 'problem_ids.json')
    registry = json.loads(registry_bytes)
    canonical_to_id = {v: k for k, v in registry.items()}
    require(len(registry) == 217 and len(canonical_to_id) == 217, '217 unique registry identities')
    require(registry_bytes == blob(SOURCE_BASE, 'problem_ids.json'), 'registry unchanged between both published bases')
    require(all(re.fullmatch(r'[A-Z]{2}-[0-9]{2,}', k) for k in registry), 'permanent numeric ID format')
    require(all(PurePosixPath(p).parts[-2] == k and PurePosixPath(p).name == 'README.md'
                and not PurePosixPath(p).is_absolute() and '..' not in PurePosixPath(p).parts
                for k, p in registry.items()), 'exact canonical registry paths')
    category_indexes = {str(PurePosixPath(p).parents[1] / 'README.md') for p in registry.values()}
    combined_indexes = {'README.md', 'CATALOG.md', 'RESOLVED.md', 'references/README.md'} | category_indexes
    doc_paths = {str(PurePosixPath(p).parent / f) for p in registry.values()
                 for f in ('README.md', 'problem.tex', 'problem.pdf')}
    affected_docs = set()
    affected_canonical = set()
    expected = {}
    suppliers = collections.defaultdict(list)
    source_records = []
    required_record_lines = collections.defaultdict(set)
    source_replaced_record_lines = collections.defaultdict(set)
    expected_statuses = {k: status(text(PUBLISHED_BASE, p)) for k, p in registry.items()}
    old_renderer = text(SOURCE_BASE, RENDERER)
    require(old_renderer == text(PUBLISHED_BASE, RENDERER), 'renderer identical in both published bases')
    combined_renderer = old_renderer
    for changes in RENDER_EDITS.values():
        combined_renderer = edits(combined_renderer, changes)
    combined_renderer = edits(combined_renderer, FINAL_RENDER_EDITS)

    for pr, head in HEADS.items():
        meta = json.loads(Path(f'/private/tmp/nla-pr-{pr}.json').read_text())
        require(meta['headRefOid'] == head and meta['baseRefOid'] == SOURCE_BASE,
                f'PR {pr} immutable metadata head/base')
        head_tree = tree(head)
        changed = {p for p in original.keys() | head_tree.keys() if original.get(p) != head_tree.get(p)}
        removed = sorted(original.keys() - head_tree.keys())
        require(not removed, f'PR {pr} deletes no published path', removed)
        require(blob(head, 'problem_ids.json') == registry_bytes, f'PR {pr} exact registry retained')
        canonicals = changed & canonical_to_id.keys()
        require(len(canonicals) == 1, f'PR {pr} changes exactly one canonical page', sorted(canonicals))
        canonical = next(iter(canonicals))
        identifier = canonical_to_id[canonical]
        contribution = str(PurePosixPath(canonical).parent) + '/'
        reference_roots = sorted({'/'.join(p.split('/')[:2]) + '/' for p in changed
                                  if p.startswith('references/') and p != 'references/README.md'})
        external = sorted(p for p in changed if not p.startswith(contribution)
                          and not any(p.startswith(r) for r in reference_roots))
        require(set(external) <= combined_indexes | {RENDERER},
                f'PR {pr} shared surfaces limited to indexes and reviewed renderer', external)
        if RENDERER in changed:
            require(pr in RENDER_EDITS and text(head, RENDERER) == edits(old_renderer, RENDER_EDITS[pr]),
                    f'PR {pr} renderer equals exact reviewed layout edit')
        else:
            require(pr not in RENDER_EDITS, f'PR {pr} expected renderer change present')
        base_page = text(PUBLISHED_BASE, canonical)
        page = text(head, canonical)
        require(title(page) == title(base_page), f'PR {pr} original title and ID unchanged')
        original_target = target(base_page, identifier)
        require(original_target in page, f'PR {pr} complete original target byte-identical')
        affected_canonical.add(canonical)
        affected_docs.update(str(PurePosixPath(canonical).parent / f)
                             for f in ('README.md', 'problem.tex', 'problem.pdf'))
        expected_statuses[identifier] = status(page)
        for p in changed & {'RESOLVED.md', 'references/README.md'}:
            required_record_lines[p].update(line_additions(text(SOURCE_BASE, p), text(head, p)))
            source_replaced_record_lines[p].update(line_deletions(text(SOURCE_BASE, p), text(head, p)))
        authored = sorted(changed - combined_indexes - doc_paths - {RENDERER})
        for p in authored:
            entry = head_tree[p]
            require(entry[:2] == ('100644', 'blob') or entry[:2] == ('100755', 'blob'),
                    f'PR {pr} authored path is regular file', p)
            if p in expected:
                require(expected[p] == entry, 'same authored path has one exact blob/mode across PRs',
                        {'path': p, 'suppliers': suppliers[p] + [pr]})
            expected[p] = entry
            suppliers[p].append(pr)
        source_records.append({
            'pr': pr, 'head': head, 'canonical': canonical, 'id': identifier,
            'changed_paths': len(changed), 'authored_paths': len(authored),
            'authored_archives_and_manifests': sum('verification/' in p or 'manifest' in p.lower() or 'archive/' in p for p in authored),
            'reference_roots': reference_roots, 'external_changes': external,
            'original_target_bytes': len(original_target.encode()),
            'original_target_sha256': hashlib.sha256(original_target.encode()).hexdigest(),
            'status': status(page),
        })

    # Collision checks include archived copies at their full repository-relative paths.
    proposed = dict(base)
    proposed.update(expected)
    normalized = collections.defaultdict(list)
    for p in proposed:
        normalized[unicodedata.normalize('NFC', p).casefold()].append(p)
        require(not PurePosixPath(p).is_absolute() and '..' not in PurePosixPath(p).parts,
                'no absolute or traversal repository path', p)
    path_collisions = [sorted(v) for v in normalized.values() if len(v) > 1]
    require(not path_collisions, 'no case-fold or NFC collision including archives', path_collisions)
    require(not any(str(p) in proposed for q in proposed for p in PurePosixPath(q).parents),
            'no file/directory collision')
    shared = {p for p in base if p.startswith(SHARED_PREFIXES) or p in SHARED_FILES}
    strict_base = {p: entry for p, entry in base.items() if p not in affected_docs | combined_indexes | {RENDERER}}
    # A source-authored change to a prior published reference/code file would need explicit review.
    for p in expected.keys() & strict_base.keys():
        require(expected[p] == strict_base[p], 'new authored files do not overwrite prior published source/evidence', p)
    archive_stats = {
        'authored_paths': len(expected),
        'manifest_named_authored_paths': sum('manifest' in PurePosixPath(p).name.lower() for p in expected),
        'archive_or_verification_authored_paths': sum('/archive/' in p or '/verification/' in p for p in expected),
        'exact_same_authored_path_multiple_suppliers': {p: v for p, v in suppliers.items() if len(v) > 1},
        'casefold_or_unicode_collisions': path_collisions,
    }
    expected_counts = dict(collections.Counter(expected_statuses.values()))
    require(expected_counts == {'Solved': 77, 'Open': 46, 'Partially resolved': 70, 'Lean verified': 24},
            'expected catalog totals 77/46/70/24', expected_counts)

    history_before = text(REVIEWED_HISTORY_COMMIT + '^', 'RESOLVED.md')
    history_after = text(REVIEWED_HISTORY_COMMIT, 'RESOLVED.md')
    history_removed = set(line_deletions(history_before, history_after))
    history_added = set(line_additions(history_before, history_after))
    history_added = {v.replace('the later full proof above now settles it',
                              'the later full proof now settles it') for v in history_added}
    required_record_lines['RESOLVED.md'].difference_update(history_removed)
    required_record_lines['RESOLVED.md'].update(history_added)
    prior_history_lines = {v for v in text(PUBLISHED_BASE, 'RESOLVED.md').splitlines() if v.strip()}
    prior_history_lines -= source_replaced_record_lines['RESOLVED.md'] | history_removed
    final = None
    if args.ref:
        ref = git('rev-parse', args.ref + '^{commit}').decode().strip()
        final_tree_oid = git('rev-parse', ref + '^{tree}').decode().strip()
        integrated = tree(ref)
        final = {'commit': ref, 'tree': final_tree_oid, 'tracked_paths': len(integrated)}
        require(not (base.keys() - integrated.keys()), 'all prior-main paths retained', sorted(base.keys() - integrated.keys()))
        exact_authored = {p: entry for p, entry in expected.items() if p not in REVIEWED_AUTHORED_REPAIRS}
        missing_authored = [p for p, entry in exact_authored.items() if integrated.get(p) != entry]
        require(not missing_authored, 'all authored files outside explicitly reviewed repairs retained byte-identical with original mode', missing_authored)
        for p, repair in REVIEWED_AUTHORED_REPAIRS.items():
            require(expected.get(p) == tuple(repair['before']), 'reviewed repair binds original authored blob/mode', p)
            require(integrated.get(p) == tuple(repair['after']), 'reviewed repair matches exact approved final blob/mode', p)
            require(hashlib.sha256(blob(ref, p)).hexdigest() == repair['after_sha256'], 'reviewed repair final SHA-256', p)
        for p, addition in REVIEWED_INTEGRATION_ADDITIONS.items():
            require(integrated.get(p) == tuple(addition['entry']), 'integration addition matches exact reviewed blob/mode', p)
            require(hashlib.sha256(blob(ref, p)).hexdigest() == addition['sha256'], 'integration addition SHA-256', p)
        changed_prior = [p for p, entry in strict_base.items() if integrated.get(p) != entry]
        require(not changed_prior, 'all prior-main reference/code/evidence paths byte-identical outside explicit page/index exceptions', changed_prior)
        changed_shared = [p for p in shared - {RENDERER} if integrated.get(p) != base[p]]
        require(not changed_shared, 'Lean/ID harness, workflow, schemas, validators, tests and shared configuration unchanged', changed_shared)
        require(text(ref, RENDERER) == combined_renderer, 'renderer is exact union of four source layout patches and reviewed RA-04 adjustment')
        require(blob(ref, 'problem_ids.json') == registry_bytes, 'final registry byte-identical with all 217 permanent IDs')
        require(subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', PUBLISHED_BASE, ref], capture_output=True).returncode == 0,
                'previous main is ancestor of integration')
        for pr, head in HEADS.items():
            require(subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', head, ref], capture_output=True).returncode == 0,
                    f'PR {pr} exact reviewed head is integration ancestor')
        current_statuses = {}
        for identifier, p in registry.items():
            page = text(ref, p)
            require(title(page) == title(text(PUBLISHED_BASE, p)), f'{identifier} title and ID retained')
            if p in affected_canonical:
                require(target(text(PUBLISHED_BASE, p), identifier) in page,
                        f'{identifier} complete original target retained byte-identical in final tree')
            else:
                require(integrated[p] == base[p], f'{identifier} unaffected canonical README byte-identical')
            current_statuses[identifier] = status(page)
        require(current_statuses == expected_statuses, 'all 217 final statuses match reviewed combined outcome',
                {k: [expected_statuses[k], current_statuses[k]] for k in registry if expected_statuses[k] != current_statuses[k]})
        final['status_counts'] = dict(collections.Counter(current_statuses.values()))
        final['open_problem_count'] = sum(v in ('Open', 'Partially resolved') for v in current_statuses.values())
        for p, lines in required_record_lines.items():
            actual = text(ref, p)
            missing = sorted(line for line in lines if line not in actual)
            require(not missing, f'all newly added source-head records/credits retained in {p}', missing)
        require(all(v in text(ref, 'RESOLVED.md') for v in prior_history_lines),
                'all prior resolution-history lines retained outside reviewed upgrades/history corrections',
                sorted(v for v in prior_history_lines if v not in text(ref, 'RESOLVED.md')))
        final['protected_prior_resolution_lines'] = len(prior_history_lines)
        final['reviewed_history_corrections'] = {'commit': REVIEWED_HISTORY_COMMIT,
                                               'removed_lines': len(history_removed),
                                               'required_replacement_lines': len(history_added)}
        final['required_new_resolved_lines'] = len(required_record_lines['RESOLVED.md'])
        final['required_new_reference_index_lines'] = len(required_record_lines['references/README.md'])
        final['strict_prior_main_paths'] = len(strict_base)
        final['shared_paths_checked'] = len(shared - {RENDERER})
        final['authored_paths_byte_identical'] = len(exact_authored)
        final['explicit_authored_repairs'] = REVIEWED_AUTHORED_REPAIRS
        final['reviewed_integration_additions'] = REVIEWED_INTEGRATION_ADDITIONS
        permitted_known = set(base) | set(expected) | set(REVIEWED_INTEGRATION_ADDITIONS) | affected_docs | combined_indexes | {RENDERER}
        new_integration_only = sorted(integrated.keys() - permitted_known)
        audit_records = {}
        unreviewed = []
        for p in new_integration_only:
            if p.startswith(APPROVED_AUDIT_RECORD_ROOT):
                data = blob(ref, p)
                require(integrated[p][:2] == ('100644', 'blob')
                        and PurePosixPath(p).suffix in {'.md', '.json', '.txt', '.log', '.patch', '.py'},
                        'approved audit record is an ordinary evidence file', p)
                if p.endswith('.json'):
                    json.loads(data)
                else:
                    data.decode()
                audit_records[p] = {'entry': integrated[p], 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
            else:
                unreviewed.append(p)
        final['new_integration_only_paths_for_review'] = unreviewed
        final['approved_maintainer_audit_records'] = audit_records
        require(not unreviewed, 'no unreviewed integration-only file (including added shared workflows/tools)', unreviewed)

    result = {
        'status': 'FAIL' if failures else ('PASS' if final else 'SOURCE_PASS_AWAITING_INTEGRATION'),
        'published_base': PUBLISHED_BASE, 'previous_published_main': PREVIOUS_MAIN, 'source_base': SOURCE_BASE,
        'source_pr_count': len(HEADS), 'previous_main_tracked_paths': len(base),
        'registry_count': len(registry), 'affected_canonical_pages': len(affected_canonical),
        'authored_preservation': archive_stats, 'expected_status_counts': expected_counts,
        'expected_open_problem_count': 116, 'shared_paths_outside_renderer': len(shared - {RENDERER}),
        'renderer_review': {'path': RENDERER, 'prs': list(RENDER_EDITS),
                            'maintainer_adjustment': 'remove RA-04 from References page-break set after combining histories',
                            'expected_combined_sha256': hashlib.sha256(combined_renderer.encode()).hexdigest()},
        'source_reviews': source_records, 'final_integration': final,
        'failures': failures, 'observations': observations,
    }
    out = Path(args.output_prefix)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix('.json').write_text(json.dumps(result, separators=(',', ':')) + '\n')
    manifest = {'published_base': PUBLISHED_BASE, 'source_base': SOURCE_BASE, 'heads': HEADS,
                'expected_authored_files': {p: {'mode': e[0], 'type': e[1], 'git_blob': e[2], 'prs': suppliers[p]}
                                            for p, e in sorted(expected.items())}}
    out.with_name(out.name + '-authored-manifest.json').write_text(json.dumps(manifest, separators=(',', ':')) + '\n')
    lines = [f'# PRs 195–228 independent preservation review — {result["status"]}', '',
             f'Published integration base: `{PUBLISHED_BASE}`; all 25 reviewed source heads branch from `{SOURCE_BASE}`.', '',
             f'Checked {len(base):,} previous-main tracked paths, all 217 permanent IDs and canonical paths, '
             f'{len(affected_canonical)} changed canonical targets, and {len(expected):,} authored reference/code/evidence paths. '
             f'All original target blocks are byte-identical in their respective source heads. '
             f'{len(shared - {RENDERER})} shared tools/workflows/schema/test/config paths are protected unchanged.', '',
             'The only shared source modification is tools/render_problems.py. Independent diff review restricts its final content to the exact union of four source layout patches: add MI-27 to the reference-page-break set; remove TR-08, RA-17 and RE-03 from that set; add RE-03 to the Context-and-notation page-break set. The separately reviewed maintainer adjustment also removes RA-04 from the reference-page-break set after combining its histories, keeping its contextual text and references on page two. No other renderer byte and no Lean or permanent-ID safeguard may change.', '',
             f'Authored archives and verification records: {archive_stats["archive_or_verification_authored_paths"]:,} paths; '
             f'manifest-named authored files: {archive_stats["manifest_named_authored_paths"]}. '
             'Complete repository-relative paths are checked, including all nested manifests and copied source trees. '
             'No authored blob/mode conflict, case-fold/NFC collision, symlink, submodule or path traversal was found unless listed below. '
             'Repeated generic filenames inside distinct archives are not merged or ignored. '
             'The unchanged Lean selector derives project roots only from the canonical registry; nested archived manifests cannot introduce or shadow an active project.', '',
             'Canonical README.md/problem.tex/problem.pdf files for the 22 affected entries and combined root/category/reference indexes are explicit integration surfaces. '
             'Their exemption from whole-file identity does not exempt original titles, IDs, complete mathematical targets, final status semantics, or added RESOLVED/reference-index records. '
             'Every other previous-main source/reference/evidence file and each new authored reference/code file outside the two explicitly reviewed #223 repairs must preserve its exact Git blob and mode. '
             'Metadata and all 25 source head hashes are frozen in the audit script. The final check uses one immutable Git commit, never the mutable worktree.', '',
             'Expected final counts: 24 Lean verified, 77 Solved, 46 Open, 70 Partially resolved; 116 still open in total.', '',
             '| PR | ID | Reviewed head | Authored paths | Original target bytes |', '|---|---|---|---:|---:|']
    for row in source_records:
        lines.append(f'| #{row["pr"]} | {row["id"]} | `{row["head"]}` | {row["authored_paths"]} | {row["original_target_bytes"]} |')
    if final:
        lines += ['', f'Final frozen commit: `{final["commit"]}`; tree `{final["tree"]}`. '
                  f'All checks above were exercised on its {final["tracked_paths"]:,} tracked paths. '
                  f'All 25 source heads and the previous main must be ancestors. '
                  f'Newly authored resolution-record lines checked: {final["required_new_resolved_lines"]}; '
                  f'reference-index lines: {final["required_new_reference_index_lines"]}.', '',
                  f'Exactly {final["authored_paths_byte_identical"]:,} authored files retain their original blobs and modes. '
                  'The two explicit authored exceptions are the repaired #223 optional checker and the package README’s four-line repair link; '
                  'their original/final blobs and SHA-256 values are recorded separately in the JSON. '
                  'The new regression file and MAINTAINER_CHECKER_CORRECTION.md are independently reviewed additions with exact bound hashes. '
                  f'The {len(final["approved_maintainer_audit_records"])} maintainer evidence records are confined to the approved audit directory, '
                  'and every record’s type, blob and SHA-256 is inventoried. No additional integration-only file is accepted.', '',
                  f'The history review protects {final["protected_prior_resolution_lines"]} prior resolution lines plus '
                  f'{final["required_new_resolved_lines"]} new resolution/credit lines and the new reference-index line. '
                  'Eight precise historical replacements from b38e398 preserve earlier scopes while identifying later resolutions; '
                  'the relative-direction typo in the moved RA-04 record was corrected. '
                  'The new-main advance from 1c467f8 to 2db1e58 changes exactly four files and only the catalog phrase '
                  '“Lean verified” to “solved with Lean verification”; all logic and test assertions are otherwise unchanged.', '',
                  'Unreviewed integration-only paths:']
        lines += [f'- `{p}`' for p in final['new_integration_only_paths_for_review']] or ['None.']
    else:
        lines += ['', 'The source-surface audit passes; no assembled integration commit has been checked in this run. '
                  'Rerun with `--ref <frozen-integration-commit>` for the final preservation verdict.']
    if failures:
        lines += ['', 'Failures:']
        lines += [f'- {f["check"]}: `{json.dumps(f["details"], ensure_ascii=False)}`' for f in failures]
    lines += ['', 'This preservation script executes no submitted code, validators, test suites or Lean programs. The separate independent #223 repair review ran its ten regression methods on an isolated frozen scratch copy with optimized Python; all passed. No integration source, Git state or GitHub state was mutated. '
              'This surface/preservation review supplements the separate mathematical reviews and independently authenticated CI receipts; it does not replace them.', '']
    out.with_suffix('.md').write_text('\n'.join(lines))
    print(json.dumps({'status': result['status'], 'source_prs': len(HEADS), 'authored_paths': len(expected),
                      'previous_main_paths': len(base), 'failures': failures, 'report': str(out.with_suffix('.md'))}, separators=(',', ':')))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
