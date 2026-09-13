#!/usr/bin/env python3
"""Remove only this referee's previously empty generated object prefix, after hashing it."""
from pathlib import Path
import datetime,hashlib,json,shutil
E=Path(__file__).resolve().parent
P=Path('/tmp/nla-lean-formalization/independent-prefixes/ra20-final-referee1')
assert json.loads((E/'validated-results.json').read_text())['status']=='PASS'
assert P.is_dir() and not P.is_symlink()
files=[]
for f in sorted(P.rglob('*')):
    assert not f.is_symlink()
    if f.is_file():
        assert f.suffix in ['.olean','.ilean'],f
        files.append({'path':str(f.relative_to(P)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size})
assert len(files)==26
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prefix':str(P),'initially_empty':True,
        'files':files,'total_files':len(files),'total_bytes':sum(f['bytes'] for f in files),
        'source_evidence_retained':True,'shared_cache_untouched':True}
(E/'owned-prefix-before-cleanup.json').write_text(json.dumps(record,indent=2)+'\n')
shutil.rmtree(P)
record.update(removed=True,postcheck_absent=not P.exists())
assert record['postcheck_absent']
(E/'owned-prefix-cleanup.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS','removed_own_files':len(files),'bytes':record['total_bytes']}))
