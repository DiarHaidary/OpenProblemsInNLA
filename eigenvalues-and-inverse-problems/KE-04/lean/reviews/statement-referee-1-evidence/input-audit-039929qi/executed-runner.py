#!/usr/bin/env python3
"""Read-only source/provenance and retained evidence audit; reviewer-owned output only."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, re, shutil, subprocess, tempfile, traceback

E = Path(__file__).resolve().parent
K = E.parent.parent
OUT = Path(tempfile.mkdtemp(prefix='input-audit-', dir=E))
shutil.copyfile(__file__, OUT / 'executed-runner.py')
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
commands = []

def sha(b): return hashlib.sha256(b).hexdigest()
def identity(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha(b)}
def write(p, v): p.write_text(json.dumps(v, indent=2, ensure_ascii=False) + '\n')
def run(argv, cwd, label, allowed=(0,)):
    stem = f'command-{len(commands):03d}-{label}'
    r = subprocess.run(list(map(str, argv)), cwd=cwd, env=ENV, capture_output=True)
    (OUT / (stem + '.stdout')).write_bytes(r.stdout)
    (OUT / (stem + '.stderr')).write_bytes(r.stderr)
    c = {'argv': list(map(str, argv)), 'cwd': str(cwd), 'exit_code': r.returncode,
         'stdout': stem + '.stdout', 'stderr': stem + '.stderr', 'stdout_identity': identity(OUT / (stem + '.stdout')),
         'stderr_identity': identity(OUT / (stem + '.stderr'))}
    commands.append(c)
    write(OUT / (stem + '.json'), c)
    assert r.returncode in allowed, c
    return r.stdout

result = {'phase': 'independent statement provenance and retained evidence inspection', 'proof': False}
try:
    baseline = json.loads((E / 'baseline.json').read_text())['files']
    assert len(baseline) == 168
    for path, expected in baseline.items(): assert identity(K / path) == expected, path
    result['all_original_168_unchanged_before'] = True
    api = json.loads((K / 'verification/api-evidence-complete/manifest.json').read_text())
    assert len(api['files']) == 33
    result['api_files'] = []
    for i, (path, expected) in enumerate(api['files'].items()):
        actual = identity(K / path)
        assert actual == {k: expected[k] for k in ['bytes', 'sha256']}, path
        live = Path(expected['repo']) / expected['upstream_path']
        b = live.read_bytes()
        assert b == (K / path).read_bytes(), path
        blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        assert blob == expected['git_blob'], path
        if '/tauceti/' not in path:
            spec = expected['commit'] + ':' + expected['upstream_path']
            got = run(['git', 'rev-parse', spec], expected['repo'], f'api-{i:02d}-git-blob').decode().strip()
            raw = run(['git', 'show', spec], expected['repo'], f'api-{i:02d}-git-text')
            assert got == blob and raw == b, path
        result['api_files'].append({'path': path, 'live_path': str(live), 'commit': expected['commit'], 'git_blob': blob, **actual})
    # Independent Git tree reconstruction from the retained recursive API tree.
    archive = K / 'verification/api-evidence-complete/tauceti-archive'
    tree = json.loads((archive / 'TauCetiProject_TauCetiReview-tree.json').read_text())
    commit = json.loads((archive / 'TauCetiProject_TauCetiReview-commit.json').read_text())
    assert not tree['truncated']
    assert commit['sha'] == 'afb424eda89e8ac96d9eb69f6a88972055a4cd1b'
    expected_root = commit['commit']['tree']['sha']
    # This archived API response echoes the requested commit in its outer sha.
    # The actual Git tree identity is independently reconstructed below and
    # must equal the distinct root tree recorded in the commit object.
    assert tree['sha'] == commit['sha']
    rows = {r['path']: r for r in tree['tree']}
    dirs = [''] + [r['path'] for r in rows.values() if r['type'] == 'tree']
    calculated = {}
    for directory in sorted(dirs, key=lambda s: s.count('/') + bool(s), reverse=True):
        # PurePosixPath top-level parent is '.', but '.github' itself must not be stripped.
        children = [r for path, r in rows.items() if ('' if str(PurePosixPath(path).parent) == '.' else str(PurePosixPath(path).parent)) == directory]
        payload = b''
        for child in sorted(children, key=lambda r: (PurePosixPath(r['path']).name + ('/' if r['type'] == 'tree' else '')).encode()):
            name = PurePosixPath(child['path']).name
            child_sha = calculated[child['path']] if child['type'] == 'tree' else child['sha']
            mode = child['mode'].lstrip('0')
            payload += mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(child_sha)
        digest = hashlib.sha1(b'tree ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()
        expected = expected_root if directory == '' else rows[directory]['sha']
        assert digest == expected, (directory, digest, expected)
        calculated[directory] = digest
    assert calculated == api['tauceti_reconstructed_git_trees']
    for row in result['api_files']:
        if '/tauceti/' in row['path']:
            upstream = api['files'][row['path']]['upstream_path']
            assert rows[upstream]['sha'] == row['git_blob']
    result['tauceti_7_git_trees'] = calculated
    for path, expected in api['tauceti_archive_bindings'].items():
        assert identity(K / path) == {key: expected[key] for key in ['bytes', 'sha256']}
        assert (K / path).read_bytes() == Path(expected['source']).read_bytes()
    # Author searches are checked against their raw logs, then rerun independently.
    for i, c in enumerate(api['searches']):
        assert sha((K / c['log']).read_bytes()) == c['log_sha256']
        raw = run(c['argv'], c['cwd'], f'api-search-{i}', allowed=(0, 1))
        # rg may interleave whole-file result groups in different orders.
        # Compare the complete line multiset, preserving duplicate counts;
        # both complete raw outputs remain retained with exact byte hashes.
        assert sorted(raw.splitlines()) == sorted((K / c['log']).read_bytes().splitlines()), c['log']
        assert commands[-1]['exit_code'] == c['exit_code']
    result['independent_source_searches'] = 5
    # Inspect complete original policy, target/proof, examples, and all rubric text.
    reads = [
      ['NUMERICAL_TARGETS.md', 'SourceCorrespondence.md', 'README.md', 'comparator.json', 'lakefile.toml', 'lake-manifest.json', 'lean-toolchain'],
      ['NLA/KE04/Definitions.lean', 'Challenge.lean'],
      ['verification/original-sources/AGENTS.md', 'verification/original-sources/CONTRIBUTING.md', 'verification/original-sources/docs/lean/REVIEW.md', 'verification/original-sources/docs/lean/README.md'],
      ['verification/original-sources/eigenvalues-and-inverse-problems/KE-04/README.md', 'verification/original-sources/eigenvalues-and-inverse-problems/KE-04/solution.md', 'verification/original-sources/eigenvalues-and-inverse-problems/KE-04/solution.tex', 'verification/original-target/README.md', 'verification/original-submission/solution.md', 'verification/original-sources/references/colbrook-2026-09-11/verification/reviews/KE-04-review.md'],
      ['verification/api-evidence-complete/schiffer/Schiffer/Challenge.lean', 'verification/api-evidence-complete/forsythe/lean-proof/Challenge.lean', 'verification/api-evidence-complete/forsythe/lean-proof/NUMERICAL_TARGETS.md', 'verification/api-evidence-complete/forsythe/lean-proof/comparator.json', 'verification/api-evidence-complete/forsythe/lean-proof/ProofProject/CheckedMultivariateBound.lean'],
      ['verification/api-evidence-complete/tauceti/README.md', 'verification/api-evidence-complete/tauceti/rubrics/README.md'] + sorted(str(p.relative_to(K)) for p in (K / 'verification/api-evidence-complete/tauceti/rubrics').glob('*.md') if p.name != 'README.md'),
      ['verification/EVIDENCE-RECOVERY.md', 'verification/statement-development/check_statements.py', 'verification/validation-attempt-v4kpdcg6/validate_draft.py', 'verification/validation-attempt-nxgen1so/validate_draft.py']
    ]
    for i, paths in enumerate(reads): run(['cat'] + paths, K, f'full-source-read-{i}')
    current = (K / 'verification/original-sources/eigenvalues-and-inverse-problems/KE-04/solution.md').read_text()
    original = (K / 'verification/original-submission/solution.md').read_text()
    block = lambda text: text[text.index('## Theorem '):text.index('## Scope and review notes')].strip().encode()
    assert block(current) == block(original)
    assert len(block(current)) == 2622 and sha(block(current)) == '3ba1bd9a62a00aaf787758af6312e4787ca8d6db02b4487e8b956ce0553977a7'
    result['original_complete_proof_block'] = {'bytes': len(block(current)), 'sha256': sha(block(current))}
    author_dir = K / 'verification/statement-development/attempt-r5fn2nl_'
    author = json.loads((author_dir / 'result.json').read_text())
    assert author['success'] and len(author['commands']) == 5
    for item in author['inputs']:
        path = author_dir / 'source' / item['path']
        assert identity(path) == {key: item[key] for key in ['bytes', 'sha256']}
        if (K / item['path']).is_file(): assert path.read_bytes() == (K / item['path']).read_bytes()
    for c in author['commands']:
        assert c['exit_code'] == 0
        if 'log' in c: assert sha((author_dir / c['log']).read_bytes()) == c['log_sha256']
    assert len(author['definition_axioms']) == 27 and len(author['objects']) == 4
    manifest_pins = {p['name']: p['rev'] for p in json.loads((K / 'lake-manifest.json').read_text())['packages']}
    for stage in ['dependency_preflight', 'dependency_postflight']:
        rows_by_name = {r['name']: r for r in author[stage]}
        assert set(rows_by_name) == set(manifest_pins)
        for name, pinned in manifest_pins.items():
            r = rows_by_name[name]
            assert r['head']['exit_code'] == r['status']['exit_code'] == 0
            assert r['head']['output'].strip() == pinned and r['status']['output'] == ''
            assert r['head']['argv'] == ['git', 'rev-parse', 'HEAD']
            assert r['status']['argv'] == ['git', 'status', '--porcelain', '--untracked-files=all']
            assert Path(r['head']['cwd']).resolve() == Path(r['status']['cwd']).resolve()
            assert Path(r['head']['cwd']).name == name
            if stage == 'dependency_preflight':
                assert r['expected_rev'] == pinned
                assert r['used_in_lean_path'] == (name != 'Cli')
                assert r['build_dir_exists'] == (name != 'Cli')
    assert author['private_prefix_removed'] and not Path(author['private_prefix']).exists()
    for path in ['Definitions.log', 'Challenge.log', 'InspectDefinitions.log', 'InspectTypes.log']:
        run(['cat', str(author_dir / path)], K, 'author-log-' + path.replace('.', '-'))
    old = json.loads((K / 'verification/statement-development/attempt-xrn2jug1/result.json').read_text())
    assert old['phase'] == 'author statement integrity only' and 'objects' not in old
    result['author_evidence'] = {'accepted_attempt': str(author_dir.relative_to(K)), 'result': identity(author_dir / 'result.json'),
        'old_overwritten_json': identity(K / 'verification/statement-development/attempt-xrn2jug1/result.json'),
        'old_elaboration_final_json_lost': True, 'no_reconstructed_object_or_postflight_claim_for_old_attempt': True,
        'fresh_four_modules_and_27_definition_audits_bound': True}
    assert not (K / 'Solution.lean').exists() and not (K / 'formalization.yaml').exists()
    assert len(re.findall(r'^theorem ', (K / 'Challenge.lean').read_text(), re.M)) == 24
    assert len(re.findall(r':= by sorry', (K / 'Challenge.lean').read_text())) == 24
    assert 'sorry' not in (K / 'NLA/KE04/Definitions.lean').read_text()
    for path, expected in baseline.items(): assert identity(K / path) == expected, path
    result['all_original_168_unchanged_after'] = True
    result['success'] = True
except BaseException as exc:
    result['success'] = False
    result['error'] = repr(exc)
    (OUT / 'failure.txt').write_text(traceback.format_exc())
finally:
    result['commands'] = commands
    result['utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(OUT / 'result.json', result)
    print(json.dumps({'success': result['success'], 'error': result.get('error'), 'commands': len(commands)}, indent=2))
if not result['success']: raise SystemExit(1)
