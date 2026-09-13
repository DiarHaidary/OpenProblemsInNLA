"""Seal scoped assembly evidence and every complete immutable helper input closure."""
from pathlib import Path
import datetime, hashlib, json, os
E=Path(__file__).resolve().parent; P=E.parents[1]; M=E/'EVIDENCE-MANIFEST.json'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
dirs=['algebra-development','tangent-development','differential-development',
      'smooth-transport-development','smooth-development','generic-development','critical-development']
files={f.resolve() for f in E.rglob('*') if f.is_file() and f!=M}
files|={(P/n).resolve() for n in ['NLA/RA20/Count.lean','NLA/RA20/Proof.lean','Solution.lean']}
prior=[]
for d in dirs:
    base=P/'verification'/d; manifest=base/'EVIDENCE-MANIFEST.json'; previous=json.loads(manifest.read_text())
    files.add(manifest.resolve())
    for n,v in previous['files'].items():
        f=(base/n).resolve(); expected=v if isinstance(v,str) else v['sha256']
        assert f.is_relative_to(P) and sha(f)==expected,(d,n)
        files.add(f)
    prior.append({'manifest':str(manifest.relative_to(P)),'sha256':sha(manifest),'bound_files':len(previous['files'])})
assert M.resolve() not in files
rows={os.path.relpath(f,E):{'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(files)}
inside=sum(f.is_relative_to(E) for f in files)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'scope':'RA20 scoped complete author assembly, Count/Proof/Solution; not the whole-project proof freeze',
   'owner':'/root/formal_review_standards',
   'inventory_rule':'Every own evidence file, three newly owned sources, and all seven complete helper seals/input closures, including nested manifests. Exclude only this exact outer manifest from its own inventory.',
   'file_count':len(rows),'own_evidence_files':inside,'bound_input_files':len(rows)-inside,'prior_manifests':prior,'files':rows}
M.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'manifest_sha256':sha(M),'bound_files':len(rows),'own_files':inside,'input_files':len(rows)-inside,'handoff_sha256':sha(E/'HANDOFF.md'),'validation_sha256':sha(E/'validation.json')}))
