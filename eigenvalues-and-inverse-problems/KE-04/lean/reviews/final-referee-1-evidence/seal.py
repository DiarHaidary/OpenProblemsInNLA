"""Seal frozen author inputs plus this reviewer; exclude only this exact seal."""
from pathlib import Path
import datetime,hashlib,json
P=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
outer=E/'EVIDENCE-MANIFEST.json'
assert not outer.exists()
execution=json.loads((E/'execution.json').read_text())
assert execution['status']=='PASS_LOCAL_SOURCE_AND_INSPECTION'
assert execution['only_recorded_owned_generated_objects_removed']
assert json.loads((E/'source-and-output-audit.json').read_text())['success']
proof=P/'reviews/proof-freeze.json'
correction=json.loads((E/'corrected-freeze-acceptance.json').read_text())
assert correction['success'] and correction['approval']
assert correction['original_proof_freeze_sha256']==execution['proof_freeze_sha256']
assert sha(proof)==correction['corrected_proof_freeze_sha256']
freeze=json.loads(proof.read_text())
names=set(freeze['files'])|{'reviews/proof-freeze.json','reviews/final-referee-1.md'}
for rel,h in freeze['files'].items():assert sha(P/rel)==h,rel
for f in E.rglob('*'):
    assert not f.is_symlink(),str(f)
    if f.is_file() and f!=outer:names.add(str(f.relative_to(P)))
files={rel:{'sha256':sha(P/rel),'bytes':(P/rel).stat().st_size} for rel in sorted(names)}
for rel in files:assert not (P/rel).is_symlink(),rel
manifest={'reviewer':'/root/ra09_final_referee1','role':'Independent KE-04 final mathematical referee 1',
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'proof_freeze_sha256':sha(proof),'frozen_author_input_count':len(freeze['files']),
    'original_compilation_proof_freeze_sha256':execution['proof_freeze_sha256'],
    'correction_acceptance_sha256':sha(E/'corrected-freeze-acceptance.json'),
    'scope':'All frozen author files, the author proof freeze itself, this independent report and every file in its evidence directory. All nested inventories are included. Concurrent other-reviewer additions and future packaging are outside this review boundary.',
    'exact_self_exclusion':str(outer.relative_to(P)),'files':files}
outer.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
for rel,r in files.items():assert sha(P/rel)==r['sha256'] and (P/rel).stat().st_size==r['bytes']
assert sha(proof)==correction['corrected_proof_freeze_sha256']
print(json.dumps({'sealed_files':len(files),'frozen_author_inputs':len(freeze['files']),
    'report_sha256':sha(P/'reviews/final-referee-1.md'),'manifest_sha256':sha(outer),
    'all_bound_bytes_verified_after_seal':True},indent=2))
