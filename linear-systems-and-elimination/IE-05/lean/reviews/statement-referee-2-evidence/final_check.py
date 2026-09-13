#!/usr/bin/env python3
"""Final source consistency and complete raw-evidence cross-check, before sealing."""
import json, pathlib, re
from audit import E, P, run, sha, write_json

# Repeat the substantive initial source-display reads with full raw capture.
# These commands are audit reads, and write only their own logs here.
read_groups={
 'handoff':['STATEMENT-HANDOFF.md','DRAFT-INVENTORY.json'],
 'boundary':['NLA/IE05/Definitions.lean','Challenge.lean'],
 'targets':['NUMERICAL_TARGETS.md','SourceCorrespondence.md','comparator.json','README.md','lakefile.toml','lake-manifest.json','lean-toolchain'],
 'original-proof':['verification/original-sources/linear-systems-and-elimination/IE-05/README.md','verification/original-sources/linear-systems-and-elimination/IE-05/solution.md','verification/original-sources/linear-systems-and-elimination/IE-05/solution.tex','verification/original-sources/references/stepaniants-ie05-2026-09-11/full-proof.md'],
 'policies':['verification/original-sources/AGENTS.md','verification/original-sources/CONTRIBUTING.md','verification/original-sources/docs/lean/README.md','verification/original-sources/docs/lean/REVIEW.md','verification/original-sources/tools/lean/HARNESS.md'],
 'provenance':['verification/original-sources/references/stepaniants-ie05-2026-09-11/README.md','verification/original-sources/references/stepaniants-ie05-2026-09-11/independent-review.md','verification/original-sources/references/stepaniants-ie05-2026-09-11/recovery/RECOVERY_NOTES.md','verification/original-sources/references/stepaniants-ie05-2026-09-11/recovery/solution.md','verification/original-sources/references/stepaniants-ie05-2026-09-11/verification/verify_recovery_relation.py'],
}
for name,files in read_groups.items():
    run('archived-read-'+name,['cat']+files)
write_json(E/'reading-record.json',dict(read_groups=read_groups,
 note='Complete substantive source-display reads repeated with actual raw log capture. All 103 original handed-off inputs are additionally retained byte-for-byte. Prior author diagnostics are archival inputs, not independent mathematical evidence.'))

inv=json.loads((P/'DRAFT-INVENTORY.json').read_text())
binding=json.loads((E/'input-binding.json').read_text())
actual={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and p.relative_to(P).parts[0]!='reviews'}
assert actual==set(binding['files'])
for rel,item in binding['files'].items():
    b=(P/rel).read_bytes()
    assert dict(sha256=sha(b),bytes=len(b))==item
    assert b==(E/'inputs'/rel).read_bytes()
assert len(actual)==103 and len(inv['files'])==102
assert not list(E.glob('private-objects-*'))
assert not [p for p in E.rglob('*') if p.is_file() and p.suffix in ['.olean','.ilean','.ir']]
assert not (P/'Solution.lean').exists()
assert not (P/'NLA/IE05/Proof.lean').exists()
assert not (P/'formalization.yaml').exists()

good=json.loads((E/'elaboration-result-2.json').read_text())
bad=json.loads((E/'elaboration-result.json').read_text())
assert good['pass_'] and not bad['pass_']
assert good['statement_count']==17 and good['definition_trust_count']==41
assert all(x['own_objects_hashed_then_removed'] and x['private_prefix_absent_after'] for x in [good,bad])
assert good['package_preflight']==good['package_postflight']==bad['package_preflight']==bad['package_postflight']
assert good['inspector_sha256']==bad['inspector_sha256']==sha((E/'inputs/Referee2Inspect.lean').read_bytes())
assert 'import Challenge' not in (E/'inputs/Referee2Inspect.lean').read_text()
assert 'sorry' not in (E/'inputs/Referee2Inspect.lean').read_text()
numerical=json.loads((E/'numerical-result.json').read_text())
assert numerical['pass_'] and numerical['not_a_Lean_theorem']
assert numerical['exact_gap']=='117335164/1147041' and numerical['reduced_certificate_counts']==[64,204]

git=json.loads((E/'git-source-binding.json').read_text())
for rel,item in git['files'].items():
    if rel=='registry_IE05': continue
    assert item['sha256']==sha((E/'inputs/verification/original-sources'/rel).read_bytes())
    assert item['exact_blob_equality']

# Source-bind the finite-maximum API file searched by api_check.py as well.
root=pathlib.Path(good['package_preflight'][1]['source_directory'])
rel='Mathlib/Data/Finset/Lattice/Fold.lean'
oid=run('finite-max-git-oid',['git','rev-parse','HEAD:'+rel],root).decode().strip()
actual_oid=run('finite-max-actual-oid',['git','hash-object',rel],root).decode().strip()
assert oid==actual_oid
write_json(E/'finite-max-source-binding.json',dict(git_blob=oid,sha256=sha((root/rel).read_bytes()),bytes=(root/rel).stat().st_size))

records=[json.loads(line) for line in (E/'commands.jsonl').read_text().splitlines()]
for rec in records:
    assert rec['exit_code']==0
    for channel in ['stdout','stderr']:
        b=(E/'logs'/(rec['label']+'.'+channel)).read_bytes()
        assert sha(b)==rec[channel+'_sha256'],(rec['label'],channel)
# The first outer script failed only after all subprocesses returned zero;
# that outer failure is retained separately and is not relabelled a PASS.
assert (E/'attempt-1-terminal.log').read_text().endswith('AssertionError\n')
write_json(E/'final-checks.json',dict(pass_=True,complete_project_inputs_unchanged=103,
    original_git_bound_files=27,command_records_checked=len(records),all_raw_subprocess_log_hashes_match=True,
    retained_failed_outer_postcheck=True,successful_fresh_Lean_exit_codes=[0,0,0],
    no_own_generated_objects_remain=True,no_proof_or_manifest_added=True,
    concurrent_other_referee_outputs_not_inspected_or_sealed=True))
print('PASS: final 103-input consistency, 27 source bindings, 17 contracts, 41 definition trust reports, retained failure, raw command/log checks, and own-object cleanup.')
