#!/usr/bin/env python3
"""One-shot installation of reviewed-math RA20 candidate wrappers; no proof or Git edit."""
from pathlib import Path
import datetime,hashlib,json,shutil
D=Path(__file__).resolve().parent
P=Path('/tmp/nla-lean-ra20-worktree/randomized-and-low-rank-approximation/RA-20/lean')
E=P/'verification/linux-candidate-2026-09-13'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((D/'preflight.json').read_text())
actual={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}
assert actual==set(b['baseline']),'Project inventory changed after preauthoring gate'
for n,h in b['baseline'].items():assert sha(P/n)==h['sha256'],n
assert sha(P/'verification/final-review-acceptance.json')==b['root_gate_sha256']
assert not E.exists() and not (P/'formalization.yaml').exists()
E.mkdir()
for n in ['preflight.py','preflight.json','preflight-read-diagnostic.json','write_metadata.py','install.py']:
    shutil.copyfile(D/n,E/n)
(E/'draft').mkdir()
for n in ['README.md','formalization.yaml']:shutil.copyfile(D/n,E/'draft'/n)
archive=P/'verification/pre-candidate-README.md'
assert not archive.exists()
archive.write_bytes((P/'README.md').read_bytes())
assert sha(archive)=='7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
(P/'README.md').write_bytes((D/'README.md').read_bytes())
(P/'formalization.yaml').write_bytes((D/'formalization.yaml').read_bytes())
changed=[]
for n,h in b['baseline'].items():
    if sha(P/n)!=h['sha256']:changed.append(n)
assert changed==['README.md']
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'INSTALLED; author checks and independent packaging review pending',
  'author':'/root/ra20_final_referee1','role':'Prior independent final mathematical referee 1; now document author, no additional review approval',
  'root_gate_sha256':b['root_gate_sha256'],'baseline_count':len(b['baseline']),'changed_existing_files':changed,
  'README_sha256':sha(P/'README.md'),'YAML_sha256':sha(P/'formalization.yaml'),
  'historical_archive':{'path':'verification/pre-candidate-README.md','sha256':sha(archive),'original_path':'README.md'},
  'historical_mapping_rule':'Only the exact project README.md path when its expected hash is 7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50 is checked against verification/pre-candidate-README.md. All other path/hash checks remain exact.',
  'new_files_scope':['formalization.yaml','verification/pre-candidate-README.md','verification/linux-candidate-2026-09-13/'],
  'canonical_status':'Solved, unchanged','proofs_pins_and_prior_evidence':'Unchanged; complete old README bytes archived',
  'actual_Linux_Comparator_default_kernel_controls':'Pending','independent_operational_review':'Pending','publication':'Pending'}
(E/'installation.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'INSTALLED','baseline':len(b['baseline']),'changed_existing':changed,
                  'README_sha256':record['README_sha256'],'YAML_sha256':record['YAML_sha256']}))
