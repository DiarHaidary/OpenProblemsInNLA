#!/usr/bin/env python3
"""Read-only exact bounded seal check. Never rerun or rewrite evidence."""
from pathlib import Path
import hashlib,json
E=Path(__file__).resolve().parent
P=E.parents[1]
M=E/'EVIDENCE-MANIFEST.json'
D=json.loads(M.read_text())
assert D['exact_self_exclusion']==str(M.relative_to(P))
for rel,r in D['files'].items():
 p=P/rel
 assert p.is_file() and not p.is_symlink(),rel
 assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],rel
 assert p.stat().st_size==r['bytes'],rel
for scope in D['complete_evidence_directories']:
 actual={str(p.relative_to(P)) for p in (P/scope).rglob('*') if p.is_file() and p!=M}
 expected={rel for rel in D['files'] if rel.startswith(scope+'/')}
 assert actual==expected,(scope,actual-expected,expected-actual)
F=json.loads((P/'reviews/statement-freeze.json').read_text())
for rel,h in F['files'].items():
 assert hashlib.sha256((P/rel).read_bytes()).hexdigest()==h,rel
print(json.dumps({'pass':True,'bound_files':len(D['files']),
 'preserved_statement_inputs':len(F['files']),
 'independent_review':False,'actual_linux_comparator':False}))
