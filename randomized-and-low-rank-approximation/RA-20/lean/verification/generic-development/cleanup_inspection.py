"""Delete only this helper inspector's completed, hash-recorded disposable prefix."""
from pathlib import Path
import datetime,hashlib,json,shutil
E=Path(__file__).resolve().parent
state=json.loads((E/'inspection-state.json').read_text());p=Path(state['prefix']).resolve()
assert p.parent==Path('/tmp/nla-lean-formalization/independent-prefixes').resolve()
assert p.name.startswith('ra20-generic-inspection-') and state['owner']=='/root/mf16_final_referee'
assert json.loads((E/'validation.json').read_text())['status'].startswith('PASS ')
files={str(f.relative_to(p)):{'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in p.rglob('*') if f.is_file()}
assert len(files)==8 and all(Path(n).suffix in ('.olean','.ilean') for n in files)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':state['owner'],'prefix':str(p),'files':files,'file_count':len(files),'bytes':sum(v['bytes'] for v in files.values()),'scope':'Only own completed disposable target objects. Shared dependency caches, source snapshots, logs and other agents prefixes untouched.','removed':False}
f=E/'owned-prefix-cleanup.json';f.write_text(json.dumps(r,indent=2)+'\n')
shutil.rmtree(p);assert not p.exists();r['removed']=True;f.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
