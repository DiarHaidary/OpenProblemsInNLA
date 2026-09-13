"""Seal independent statement review, every original attempt, and exact source package.
Manifest paths are relative to this directory. Only this exact outer file excludes itself.
"""
from pathlib import Path
import datetime,hashlib,json,os
E=Path(__file__).resolve().parent;P=E.parents[1];out=E/'EVIDENCE-MANIFEST.json'
assert not out.exists();sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
f=json.loads((P/'reviews/statement-freeze.json').read_text())
for n,h in f['files'].items():assert sha(P/n)==h,n
original=json.loads((P/'reviews/statement-package-manifest.json').read_text())
for n,r in original['files'].items():assert sha(P/n)==r['sha256'],n
paths={x.resolve() for x in E.rglob('*') if x.is_file() and x!=out}
paths|={(P/n).resolve() for n in original['files']}
paths|={(P/'reviews/statement-package-manifest.json').resolve(),(P/'reviews/statement-referee-2.md').resolve()}
rows={os.path.relpath(x,E.resolve()):{'sha256':sha(x),'bytes':x.stat().st_size} for x in sorted(paths)}
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'APPROVE exact RA20 frozen statements only',
 'reviewer':'/root/leancert_examples, independent AI statement referee2',
 'report_sha256':sha(P/'reviews/statement-referee-2.md'),
 'inventory_rule':'Every own evidence file, report, and every file in the original author package plus its manifest. Exact outer self exclusion only; all nested manifests and all original and referee attempts are ordinary bound inputs.',
 'file_count':len(rows),'own_internal_files':sum(not n.startswith('../') for n in rows),
 'original_author_package_files_including_outer':len(original['files'])+1,
 'files':rows}
out.write_text(json.dumps(r,indent=2)+'\n')
for n,row in rows.items():assert sha(E/n)==row['sha256'],n
actual={os.path.relpath(x,E) for x in E.rglob('*') if x.is_file() and x!=out}
assert actual=={n for n in rows if not n.startswith('../')}
print('APPROVE report',r['report_sha256']);print('Evidence',sha(out),'bound',len(rows),'internal',r['own_internal_files'])
