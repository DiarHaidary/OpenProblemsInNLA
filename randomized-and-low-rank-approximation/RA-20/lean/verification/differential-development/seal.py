"""Bind the complete scoped helper evidence and frozen inputs; only self is excluded."""
from pathlib import Path
import datetime,hashlib,json,os
E=Path(__file__).resolve().parent;P=E.parents[1];M=E/'EVIDENCE-MANIFEST.json'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
load=lambda f:json.loads(f.read_text())
files={f.resolve() for f in E.rglob('*') if f.is_file() and f!=M}
freeze=load(P/'reviews/statement-freeze.json')
files|={P/name for name in freeze['files']}
files|={P/name for name in ['NLA/RA20/Differential.lean','verification/proof-start.json','verification/implementation-roles.json','reviews/statement-freeze.json']}
for name,base in [('reviews/statement-package-manifest.json',P),
 ('reviews/statement-referee-1-evidence/EVIDENCE-MANIFEST.json',P/'reviews/statement-referee-1-evidence'),
 ('reviews/statement-referee-2-evidence/EVIDENCE-MANIFEST.json',P/'reviews/statement-referee-2-evidence')]:
 files.add(P/name)
 for n,v in load(P/name)['files'].items():
  f=(base/n).resolve();assert f.is_relative_to(P)
  assert sha(f)==(v if isinstance(v,str) else v['sha256'])
  files.add(f)
files={f.resolve() for f in files}
assert M.resolve() not in files
rows={os.path.relpath(f,E):{'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(files)}
inside=sum(f.is_relative_to(E) for f in files)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'RA20 differential helper author completion, contracts 5,6,8 only; local macOS',
 'owner':'/root/mf16_final_referee','inventory_rule':'Every file under this evidence directory plus the helper and complete frozen statement/prior-review input closure. Only this exact EVIDENCE-MANIFEST.json is excluded from its own inventory. No wildcard exclusions.',
 'file_count':len(rows),'own_evidence_files':inside,'bound_input_files':len(rows)-inside,'files':rows}
M.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'manifest':str(M),'sha256':sha(M),'files':len(rows),'own':inside,'inputs':len(rows)-inside}))
