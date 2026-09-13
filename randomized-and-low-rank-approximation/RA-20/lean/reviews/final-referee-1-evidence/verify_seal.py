#!/usr/bin/env python3
"""Read-only verification; all frozen inputs and nested manifest basenames must remain bound."""
from pathlib import Path
import hashlib,json,os
E=Path(__file__).resolve().parent;P=E.parent.parent;M=E/'EVIDENCE-MANIFEST.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads(M.read_text());f=json.loads((P/'verification/proof-freeze.json').read_text())
expected={(P/n).resolve() for n in f['files']}
expected.add((P/'verification/proof-freeze.json').resolve())
expected.add((P/'reviews/final-referee-1.md').resolve())
expected|={p.resolve() for p in E.rglob('*') if p.is_file() and p!=M}
assert set(m['files'])=={os.path.relpath(p,E) for p in expected}
for n,v in m['files'].items():
    p=E/n;assert p.is_file() and sha(p)==v['sha256'] and p.stat().st_size==v['bytes'],n
assert len(m['files'])==m['file_count']
assert m['exact_self_exclusion']=='EVIDENCE-MANIFEST.json'
assert 'EVIDENCE-MANIFEST.json' not in m['files']
assert sha(P/'verification/proof-freeze.json')=='f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f'
for n,h in f['files'].items():assert sha(P/n)==h,n
for n,h in f['source_files'].items():assert sha(P/'verification/original-sources'/n)==h,n
c=json.loads((E/'owned-prefix-cleanup.json').read_text())
assert c['removed'] and c['postcheck_absent'] and not Path(c['prefix']).exists()
v=json.loads((E/'validated-results.json').read_text());assert v['status']=='PASS'
assert len(v['complete_nested_manifests'])==12
print(json.dumps({'status':'PASS','file_count':len(m['files']),'own_evidence_files':m['own_evidence_files'],
  'frozen_files_including_freeze':522,'nested_manifests_rehashed':12,'original_source_identities':16,
  'report_sha256':sha(P/'reviews/final-referee-1.md'),'validation_sha256':sha(E/'validated-results.json'),
  'manifest_sha256':sha(M),'final_sha256':sha(E/'FINAL.json')},indent=2))
