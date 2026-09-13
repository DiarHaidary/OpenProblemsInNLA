#!/usr/bin/env python3
"""Read-only complete scoped exact certificate diagnostic handoff integrity check."""
from pathlib import Path
import hashlib,json
E=Path(__file__).resolve().parent;P=E.parents[1]
M=E/'EVIDENCE-MANIFEST.json';data=json.loads(M.read_text())
assert data['exact_self_exclusion']==str(M.relative_to(P))
for rel,record in data['files'].items():
 p=P/rel;assert p.is_file() and not p.is_symlink(),rel
 assert hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'],rel
 assert p.stat().st_size==record['bytes'],rel
actual={str(p.relative_to(P))for p in E.rglob('*')if p.is_file() and p!=M}
expected={r for r in data['files'] if r.startswith(str(E.relative_to(P))+'/')}
assert actual==expected,(actual-expected,expected-actual)
freeze=json.loads((P/'reviews/statement-freeze.json').read_text())
for rel,h in freeze['files'].items():assert hashlib.sha256((P/rel).read_bytes()).hexdigest()==h,rel
print(json.dumps({'pass':True,'bound_files':len(data['files']),'scoped_evidence_files_including_outer':len(actual)+1,'preserved_statement_inputs':len(freeze['files'])}))
