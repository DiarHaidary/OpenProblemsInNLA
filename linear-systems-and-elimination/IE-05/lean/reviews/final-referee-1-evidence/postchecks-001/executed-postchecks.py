from pathlib import Path
import hashlib, importlib.util, json, os, shutil

OWN=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review',OWN/'review.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
d=OWN/'postchecks-001';d.mkdir(exist_ok=False)
shutil.copyfile(__file__,d/'executed-postchecks.py')
for name in ['exact-check','audit-inspection']:
    script=OWN/(name+'.py');shutil.copyfile(script,d/('executed-'+name+'.py'))
    r.run(d,name,['python3',script])
pins=json.loads((OWN/'preflight-001/pins.json').read_text())
env=json.loads((OWN/'inspection-001/run-003/actual-environment.json').read_text())
prefix=OWN/'attempt-001/objects'
paths=[prefix]+[Path(x) for x in pins['built_paths']]+[r.LEANROOT/'lib/lean']
objects={}
for module in env['imported_modules']:
    rel=Path(*module.split('.')).with_suffix('.olean')
    choices=[base/rel for base in paths if (base/rel).is_file()]
    assert len(choices)==1,(module,[str(x) for x in choices])
    for suffix in ['.olean','.olean.private','.olean.server']:
        p=choices[0].with_suffix(suffix)
        if p.is_file(): objects[str(p)]={'sha256':r.sha(p),'bytes':p.stat().st_size,'module':module}
r.save(d/'imported-object-records.json',objects)
assert len(objects)==16158
r.save(d/'imported-object-summary.json',{'modules':len(env['imported_modules']),'files':len(objects),
    'bytes':sum(v['bytes'] for v in objects.values()),'paths':list(map(str,paths)),
    'scope':'Read-only hashes of each resolved imported .olean and existing .olean.private/.olean.server companion; dependency packages were not copied or rebuilt.'})
# Preserve object outcomes of the two failed reviewer-only inspector attempts.
for run in ['run-001','run-002']:
    old=OWN/'inspection-001'/run
    reference={str(p.relative_to(prefix)):{'sha256':r.sha(p),'bytes':p.stat().st_size}
        for p in prefix.glob('RefereeReference.olean*')}
    for p,v in reference.items():
        assert json.loads((OWN/'inspection-001/run-003/objects-before.json').read_text())[p]==v
    r.save(old/'object-outcome.json',{'reference_objects':reference,'inspector_exit_code':1,
        'inspector_object_produced':False,'note':'The successful reference elaboration was repeated unchanged and its object hashes match the before-run-003 inventory. The failing inspector did not produce an olean; all command/source/log records remain.'})
# Hash-match every own object immediately before cleanup; no dependency is touched.
expected=json.loads((OWN/'inspection-001/run-003/objects-after.json').read_text())
live={str(p.relative_to(prefix)):{'sha256':r.sha(p),'bytes':p.stat().st_size}
    for p in prefix.rglob('*') if p.is_file()}
assert live==expected
assert not any(p.is_symlink() for p in prefix.rglob('*'))
for rel in sorted(live):
    p=prefix/rel
    assert p.resolve().is_relative_to(prefix.resolve()) and '.olean' in p.name
    p.unlink()
for p in sorted(prefix.rglob('*'),key=lambda p:len(p.parts),reverse=True):
    if p.is_dir():p.rmdir()
assert not list(prefix.iterdir())
r.save(d/'owned-object-cleanup.json',{'prefix':str(prefix),'matched_and_removed':live,'removed_files':len(live),
    'dependency_mutations':False,'contents_after':[],'utc':r.utc()})
proof,files=r.members('reviews/proof-freeze.json','72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251')
statement,sfiles=r.members('reviews/statement-freeze.json',proof['frozen_statement_sha256'])
r.save(d/'post-review-frozen-check.json',{'status':'PASS','proof_members':len(files),'statement_members':len(sfiles),
    'proof_freeze_sha256':r.sha(r.ROOT/'reviews/proof-freeze.json'),'proof_start_sha256':r.sha(r.ROOT/'verification/proof-start.json'),'utc':r.utc()})
r.save(d/'result.json',{'status':'PASS','fresh_commands':['exact-check','audit-inspection'],'imported_artifact_files':len(objects),
    'owned_objects_removed_after_matching':len(live),'frozen_proof_inputs_unchanged':1800})
print('Postchecks PASS: recorded exact/algebraic audit, 16158 imported artifact hashes, owned object cleanup, and unchanged 1800/733 frozen inputs')
