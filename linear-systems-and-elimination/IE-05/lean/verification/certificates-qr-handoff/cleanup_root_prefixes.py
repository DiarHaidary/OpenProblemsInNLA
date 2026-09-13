#!/usr/bin/env python3
"""Remove only explicitly delegated root prefixes whose full object records match."""
from pathlib import Path
import datetime,hashlib,json,shutil
E=Path(__file__).resolve().parent;P=E.parents[1]
B=Path('/tmp/nla-lean-formalization/independent-prefixes').resolve()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (E/'root-prefix-cleanup.json').exists()
records=[]
for target in ['exactcertificates','integerqr','certdiagnostic']:
 for a in sorted((P/f'verification/{target}-development').glob('attempt-*')):
  inputs=json.loads((a/'inputs.json').read_text());expected=json.loads((a/'objects.json').read_text())
  prefix=Path(inputs['prefix']);q=prefix.resolve()
  assert q.parent==B and q.name.startswith('ie05-root-'+target+'-') and not prefix.is_symlink()
  for item in inputs['sources']:
   src=a/'source'/item['path'];assert sha(src)==item['sha256'] and src.stat().st_size==item['bytes']
  rec={'attempt':str(a.relative_to(P)),'inputs_sha256':sha(a/'inputs.json'),
       'objects_sha256':sha(a/'objects.json'),'recorded_prefix':str(prefix),
       'original_object_count':len(expected),'already_absent':not q.exists()}
  if q.exists():
   actual={str(f.relative_to(q)):{'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(q.rglob('*')) if f.is_file()}
   assert all(not f.is_symlink() for f in q.rglob('*'))
   wanted={r['path']:{'sha256':r['sha256'],'bytes':r['bytes']} for r in expected}
   assert actual==wanted,(q,'object mismatch; nothing deleted')
   rec['actual_objects_before_removal']=actual
   shutil.rmtree(q);rec['removed_after_exact_match']=not q.exists()
  records.append(rec)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Only root-delegated ExactCertificates/IntegerQR/CertDiagnostic prefixes matched to original immutable attempt inputs and exact complete objects.json',
 'records':records,'attempts':len(records),
 'removed_prefixes':sum(r.get('removed_after_exact_match',False) for r in records),
 'removed_objects':sum(len(r.get('actual_objects_before_removal',{})) for r in records),
 'already_absent':sum(r['already_absent'] for r in records)}
(E/'root-prefix-cleanup.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='records'}))
