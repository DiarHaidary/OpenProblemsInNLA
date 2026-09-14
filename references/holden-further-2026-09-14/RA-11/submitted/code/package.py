"""Preserve available prior files and build a checksummed, integrity-tested ZIP."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import html
import json
import shutil
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
prior_candidates=[
 ('round1_archive','/mnt/data/RA11_research_package.zip'),
 ('round1_manuscript','/mnt/data/RA11_research_package/manuscript/ra11_partial_results.pdf'),
 ('round2_archive','/mnt/data/RA11_round2_research_package.zip'),
 ('round2_manuscript','/mnt/data/RA11_round2/manuscript/ra11_linear_accuracy.pdf'),
 ('round3_archive','/mnt/data/RA11_round3_research_package.zip'),
 ('round3_manuscript','/mnt/data/RA11_round3/manuscript/ra11_superset_controls.pdf'),
]
records=[]
for label,raw in prior_candidates:
    src=Path(raw)
    if not src.is_file():
        # Automatically mounted conversation files can be nested in a mount directory.
        matches=[p for p in Path('/mnt/data').rglob(src.name)
                 if p.is_file() and ROOT not in p.parents]
        if matches: src=matches[0]
    record={'label':label,'requested_path':raw,'available':src.is_file()}
    if src.is_file():
        dest=ROOT/'prior_work'/src.name
        shutil.copy2(src,dest)
        digest=hashlib.sha256(src.read_bytes()).hexdigest()
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==digest
        record.update({'copied_from':str(src),'archive_path':str(dest.relative_to(ROOT)),
                       'sha256':digest,'bytes':dest.stat().st_size})
    records.append(record)
(ROOT/'prior_work'/'CONTENTS.json').write_text(json.dumps(records,indent=2)+'\n')

url='https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/randomized-and-low-rank-approximation/RA-11/README.md'
meta={'url':url,'attempted_at_utc':datetime.now(timezone.utc).isoformat()}
try:
    request=urllib.request.Request(url,headers={'User-Agent':'RA11-research-source-snapshot'})
    with urllib.request.urlopen(request,timeout=10) as response:
        data=response.read()
    (ROOT/'sources'/'RA-11_README_snapshot.md').write_bytes(data)
    meta.update({'status':'retrieved','sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
except Exception as exc:
    meta.update({'status':'retrieval_failed','error':repr(exc),
                 'fallback':'Problem model is quoted and cited from the preceding supplied manuscript.'})
(ROOT/'sources'/'retrieval_metadata.json').write_text(json.dumps(meta,indent=2)+'\n')

# Standalone HTML reading copy; no external fonts, scripts, or network dependencies.
text=(ROOT/'manuscript'/'ra11_probability_diagonal.md').read_text()
try:
    import markdown
    body=markdown.markdown(text,extensions=['extra','toc'])
except ImportError:
    pieces=[]; para=[]; code=[]
    def flush_para():
        if para:
            pieces.append('<p>'+html.escape(' '.join(para))+'</p>'); para.clear()
    def flush_code():
        if code:
            pieces.append('<pre>'+html.escape('\n'.join(code))+'</pre>'); code.clear()
    for line in text.splitlines():
        if line.startswith('    '):
            flush_para(); code.append(line[4:]); continue
        flush_code()
        if not line.strip(): flush_para(); continue
        if line.startswith('#'):
            flush_para(); level=min(6,len(line)-len(line.lstrip('#')))
            pieces.append(f'<h{level}>'+html.escape(line[level:].strip())+f'</h{level}>')
        else: para.append(line)
    flush_para(); flush_code(); body='\n'.join(pieces)
css='''body{font-family:Georgia,serif;line-height:1.62;color:#20262c;background:#f3f5f7;margin:0}
main{max-width:960px;margin:32px auto;padding:48px 60px;background:white;border:1px solid #d7dfe4}
h1,h2,h3{font-family:Arial,sans-serif;color:#16394d;line-height:1.2}h1{font-size:32px}
h2{margin-top:2em;padding-top:.5em;border-top:1px solid #c6d5dc}h3{font-size:20px}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f6;border-left:3px solid #527b91;padding:16px;font-size:13px;line-height:1.55}
a{color:#1d577a}.scope{background:#fff3df;border-left:4px solid #af782c;padding:15px;margin-bottom:25px;font-family:Arial,sans-serif}
@media print{body{background:white}main{border:0;padding:0;margin:0;max-width:none}h2,h3{break-after:avoid}pre{break-inside:avoid}a{color:inherit}}'''
page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>RA-11 Round 4 — Partial results</title><style>'+css+'</style></head><body><main><div class="scope"><strong>PARTIAL RESULT.</strong> This is not a completed unrestricted minimax solution. See Sections 5 and 8 for the distinction between estimator-specific and oracle lower bounds.</div>'+body+'</main></body></html>'
(ROOT/'manuscript'/'ra11_probability_diagonal.html').write_text(page)

files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
       and p.name not in {'SHA256SUMS.txt','package_integrity.json'}]
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT))+'\n'
                 for p in sorted(files))
(ROOT/'SHA256SUMS.txt').write_text(manifest)
archive=Path('/mnt/data/RA11_round4_research_package.zip')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.name!='package_integrity.json':
            z.write(p,arcname='RA11_round4/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for line in manifest.splitlines():
        digest,relative=line.split('  ',1)
        assert hashlib.sha256(z.read('RA11_round4/'+relative)).hexdigest()==digest
    entries=len(z.namelist())
status={'zip':str(archive),'exists':archive.is_file(),'bytes':archive.stat().st_size,
        'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
        'entries':entries,'zip_crc_check':'passed','manifest_check':'passed',
        'prior_files_available':sum(r['available'] for r in records)}
(ROOT/'results'/'package_integrity.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps(status,indent=2))
