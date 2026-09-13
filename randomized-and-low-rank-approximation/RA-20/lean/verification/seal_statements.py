"""Seal exact statement-stage inputs and source identities, with no proof claim."""
from pathlib import Path
import datetime, hashlib, json, re, shutil, subprocess

P = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
sources = json.loads((P / 'verification/original-source-inventory.json').read_text())
latest = json.loads((P / 'verification/statement-checks/latest.json').read_text())
attempt = Path(latest['attempt'])
result = json.loads((attempt / 'result.json').read_text())
assert sha(attempt / 'result.json') == latest['result_sha256']
assert result['result'] == 'PASS'
assert len(result['commands']) == 3 and result['ten_pins_rechecked_after_run']
assert all(row['exit_code'] == 0 for row in result['commands'])
for row in result['commands']:
    assert sha(P / row['source']) == row['source_sha256']
    assert sha(attempt / row['log']) == row['log_sha256']
    assert sha(attempt / (row['source'].replace('/', '-') + '.txt')) == row['source_sha256']
for name, data in sources['files'].items():
    assert sha(P / data['snapshot']) == data['sha256']
    raw = subprocess.check_output(['git', 'show', sources['base'] + ':' + name], cwd='/tmp/nla-lean-ra09-worktree')
    assert hashlib.sha256(raw).hexdigest() == data['sha256']
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == data['git_blob']
defs = (P / 'NLA/RA20/Definitions.lean').read_text()
assert not re.search(r'(?m)^\s*(axiom|opaque|unsafe|theorem|lemma)\b', defs)
assert not re.search(r'\b(sorry|admit|native_decide)\b', defs)
challenge = (P / 'Challenge.lean').read_text()
names = re.findall(r'(?m)^theorem\s+(\w+)', challenge)
config = json.loads((P / 'comparator.json').read_text())
assert len(names) == 12
assert config['theorem_names'] == ['NLA.RA20.' + n for n in names]
assert config['definition_names'] == []
assert config['permitted_axioms'] == ['propext','Classical.choice','Quot.sound']
assert len(re.findall(r'(?m)^\s+sorry\s*$', challenge)) == 12
assert not (P / 'Solution.lean').exists() and not list((P / 'NLA').rglob('Proof.lean'))
diagnostic = json.loads((P / 'verification/reconstruction.json').read_text())
assert diagnostic['status'] == 'PASS' and not diagnostic['actual_geometric_claims_proved']

# Reclaim only this author's recorded generated prefix objects; keep all sources,
# snapshots, raw logs and every read-only dependency object untouched.
prefix = Path(result['prefix'])
assert prefix.parent == Path('/tmp/nla-lean-formalization/independent-prefixes')
assert prefix.name.startswith('ra20-statements-')
objects = {r['path']: r for r in result['objects']}
actual = {str(f.relative_to(prefix)): f for f in prefix.rglob('*') if f.is_file()}
assert set(actual) == set(objects)
for name, f in actual.items():
    assert f.suffix in {'.olean','.ilean'} and sha(f) == objects[name]['sha256']
cleanup = {'scope': 'Only own generated prefix objects; all evidence and dependencies preserved',
           'prefix': str(prefix), 'objects': result['objects'],
           'logical_bytes': sum(x['bytes'] for x in result['objects'])}
shutil.rmtree(prefix)
(P / 'verification/owned-prefix-cleanup.json').write_text(json.dumps(cleanup, indent=2) + '\n')

freeze_path = P / 'reviews/statement-freeze.json'
handoff_path = P / 'reviews/statement-handoff.md'
outer_path = P / 'reviews/statement-package-manifest.json'
excluded = {freeze_path, handoff_path, outer_path}
files = {str(f.relative_to(P)): sha(f) for f in sorted(P.rglob('*'))
         if f.is_file() and f not in excluded}
freeze = {'format': 'statement-stage-sha256-v1', 'problem_id': 'RA-20',
          'base': sources['base'], 'project_root_at_freeze': str(P),
          'files': files,
          'source_files': {n: d['sha256'] for n, d in sources['files'].items()},
          'source_git_blobs': {n: d['git_blob'] for n, d in sources['files'].items()},
          'author_statement_check': {'result': 'PASS', 'commands': 3, 'intentional_reference_holes': 12,
                                     'definition_kernel_axiom_reports': 9,
                                     'result_path': str((attempt / 'result.json').relative_to(P)),
                                     'result_sha256': sha(attempt / 'result.json')},
          'independent_statement_approvals': [], 'proof_gate_open': False,
          'implementation_exists': False,
          'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
freeze_path.write_text(json.dumps(freeze, indent=2) + '\n')
handoff = f'''# RA-20 frozen statement handoff

Ready for **two independent statement reviews**. No proof gate is open, and no
mathematical implementation exists. The statement authoring agent is
`/root/formal_review_standards`; this author handoff is not an independent review.

- Base: `{sources['base']}`; canonical status Solved and no prior RA-20 Lean subtree.
- Freeze: `statement-freeze.json`, SHA-256 `{sha(freeze_path)}`.
- Frozen project inputs: **{len(files)}**; original source/policy Git files: **{len(sources['files'])}**.
- Definitions: `{sha(P / 'NLA/RA20/Definitions.lean')}`.
- Challenge: `{sha(P / 'Challenge.lean')}`; **twelve** complete reference contracts.
- Mathematical targets: `{sha(P / 'NUMERICAL_TARGETS.md')}`.
- Source correspondence: `{sha(P / 'SourceCorrespondence.md')}`.
- Comparator configuration: `{sha(P / 'comparator.json')}`; twelve exports, no definition exceptions.
- Three fresh author-local commands passed; twelve intended Challenge holes,
  nine definition-only kernel/standard-three reports, ten clean read-only pins.
  Exact run result: `{sha(attempt / 'result.json')}`.
- Exact coefficient/rational diagnostic: `{sha(P / 'verification/reconstruction.json')}`;
  this is not a geometric or Lean proof.

Read the complete canonical/source and original review snapshots, then
`Definitions.lean`, `Challenge.lean`, `NUMERICAL_TARGETS.md`, `SourceCorrespondence.md`
and the author check. In particular audit the genuine reduced coordinate-ring
and Mathlib smooth-locus definitions; the entire-ideal tangent equations; the
complex bilinear metric and actual derivatives; arbitrary nonempty generic-open
data sets and their required intersection; cardinal counting; and full negation
of the original four-formula target. The coordinate smoothness equivalence is a
substantive **unproved obligation**, never a premise or a coordinate-case definition.

The draft is outside a Git worktree and no source/status/registry/branch was
changed. It uses no Lake build or copied dependency cache. All failed and passed
author attempts are retained; only the hashed own generated prefix objects were
removed to preserve disk headroom. Final proofs, two independent final referees,
actual Linux Comparator/kernel controls and truthful v0.4 metadata are pending.
Do not start mathematical proof implementation before the root accepts both
new independent statement reports and seals an explicit proof-start gate.
'''
handoff_path.write_text(handoff)
outer = {'scope': 'Full statement package; only this exact outer manifest excludes itself',
         'files': {str(f.relative_to(P)): {'sha256': sha(f), 'bytes': f.stat().st_size}
                   for f in sorted(P.rglob('*')) if f.is_file() and f != outer_path}}
outer_path.write_text(json.dumps(outer, indent=2) + '\n')
for name, data in outer['files'].items():
    assert sha(P / name) == data['sha256']
print(json.dumps({'freeze_sha256': sha(freeze_path), 'handoff_sha256': sha(handoff_path),
                  'outer_manifest_sha256': sha(outer_path), 'frozen_project_files': len(files),
                  'original_Git_sources': len(sources['files']), 'package_bound_files': len(outer['files']),
                  'package_total_files': len(outer['files']) + 1,
                  'owned_generated_bytes_reclaimed': cleanup['logical_bytes']}, indent=2))
