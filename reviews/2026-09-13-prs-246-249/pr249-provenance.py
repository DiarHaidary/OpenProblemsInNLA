#!/usr/bin/env python3
"""Read-only PR249 archive/attribution audit; output only /private/tmp artifacts."""
from pathlib import Path,PurePosixPath,PureWindowsPath
import ast,difflib,hashlib,io,json,re,stat,subprocess,zipfile
ROOT=Path('/private/tmp/nla-audit-249/references/holden-ie-extensions-2026-09-13')
sha=lambda b:hashlib.sha256(b).hexdigest()
result={'root':str(ROOT),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'archives':[],'archive_hazards':[],'payload_mismatches':[],'nested_archives':[],'static_sensitive_calls':[],'attribution':[],'manifests':[]}
expected=json.loads((ROOT/'original-sha256.json').read_text())
payload={}; code_files=[]
def archive_check(source,label,top=False,depth=0):
 assert depth<6
 with zipfile.ZipFile(source) as z:
  seen=set();folded=set();records=[]
  for entry in z.infolist():
   name=entry.filename;p=PurePosixPath(name);mode=entry.external_attr>>16
   bad=[]
   if p.is_absolute() or '..' in p.parts or '\\' in name or PureWindowsPath(name).drive or '\x00' in name:bad.append('unsafe path')
   if name in seen or name.casefold() in folded:bad.append('duplicate/case-colliding path')
   if stat.S_ISLNK(mode):bad.append('symlink')
   if stat.S_IFMT(mode) not in (0,stat.S_IFREG,stat.S_IFDIR):bad.append('nonregular entry')
   if entry.flag_bits&1:bad.append('encrypted')
   if bad:result['archive_hazards'].append({'archive':label,'entry':name,'hazards':bad})
   seen.add(name);folded.add(name.casefold())
   if entry.is_dir():continue
   assert entry.file_size<100_000_000
   data=z.read(entry) # also checks ZIP CRC
   records.append({'path':name,'bytes':len(data),'sha256':sha(data)})
   if top:
    assert name not in payload
    payload[name]=data
    disk=ROOT/'submitted'/name
    if bad or not disk.is_file() or disk.is_symlink() or disk.read_bytes()!=data:result['payload_mismatches'].append(name)
   if name.endswith('.zip'):
    nested=archive_check(io.BytesIO(data),label+'!/'+name,False,depth+1)
    result['nested_archives'].append(nested)
   if name.endswith('.py'):
    text=data.decode('utf-8');tree=ast.parse(text,filename=label+'!/'+name);code_files.append(label+'!/'+name)
    for node in ast.walk(tree):
     if isinstance(node,ast.Call):
      call=ast.unparse(node.func)
      if call in {'eval','exec','compile','__import__','os.system','os.remove','os.unlink','shutil.rmtree','shutil.move'} or call.startswith(('subprocess.','requests.','urllib.','socket.')) or call.endswith(('.unlink','.rmdir','.rmtree','.extractall')):
       result['static_sensitive_calls'].append({'file':label+'!/'+name,'line':node.lineno,'call':ast.unparse(node)})
   if name.endswith(('.tex','.sh','.bat','.ps1','.js')) and re.search(r'\\write18|\\openout|shell-escape|\brm\s+-rf\b',data.decode('utf-8',errors='replace')):
    result['archive_hazards'].append({'archive':label,'entry':name,'hazards':['potential TeX/shell side effect; inspect']})
  return {'name':label,'files':len(records),'uncompressed_bytes':sum(r['bytes'] for r in records),'max_compression_ratio':max((e.file_size/max(1,e.compress_size) for e in z.infolist()),default=0),'entries':records}
for name,digest in expected.items():
 path=ROOT/'originals'/name;actual=sha(path.read_bytes());assert actual==digest,(name,actual,digest)
 record=archive_check(path,name,True);record.update(sha256=actual,expected_sha256=digest,hash_matches=True);result['archives'].append(record)
assert len(payload)==240
tracked=subprocess.check_output(['git','ls-files','-z','--','submitted'],cwd=ROOT).decode().split('\x00');tracked={p[len('submitted/'):] for p in tracked if p}
result['tracked_payload_count']=len(tracked);result['unmatched_tracked_payloads']=sorted(tracked-set(payload));result['untracked_or_ignored_extras']=sorted(str(p.relative_to(ROOT/'submitted')) for p in (ROOT/'submitted').rglob('*') if p.is_file() and str(p.relative_to(ROOT/'submitted')) not in payload)
assert tracked==set(payload)
# Exact, explicitly enumerated attribution transformations; every other byte stays unchanged.
common=r'Sidney Holden\\[3pt]\small Center for Computational Biology, Flatiron Institute\\\small Simons Foundation\\[3pt]\small Prepared with substantial AI assistance'
mapping={
 'IE-11':('IE11_recovery/report/IE11_report.tex',[(r'pdfauthor={ChatGPT}',r'pdfauthor={Sidney Holden}'),(r'\author{Reconstructed computational and mathematical write-up}',r'\author{'+common+'}')]),
 'IE-20':('IE20_extended/IE20_extended_results.tex',[(r'pdfauthor={ChatGPT}',r'pdfauthor={Sidney Holden}'),('Prepared by ChatGPT\\hfill September 13, 2026','\\textbf{Sidney Holden}\\hfill September 13, 2026\\par\n{\\small Center for Computational Biology, Flatiron Institute, Simons Foundation\\par Prepared with substantial AI assistance\\par}')]),
 'IE-27':('IE-27_research_update/report.tex',[(r'pdfauthor={OpenAI ChatGPT}',r'pdfauthor={Sidney Holden}'),('\\vspace{5pt}\n\\fcolorbox','\\par\\textbf{Sidney Holden}\\par\n{\\small Center for Computational Biology, Flatiron Institute, Simons Foundation\\par Prepared with substantial AI assistance}\\par\\vspace{5pt}\n\\fcolorbox')]),
 'IE-28':('IE28_extended_results/writeup.tex',[(r'pdfauthor={ChatGPT}',r'pdfauthor={Sidney Holden}'),(r'\author{Prepared by ChatGPT}',r'\author{'+common+'}')])}
diffs=[]
for entry,(source,changes) in mapping.items():
 original=(ROOT/'submitted'/source).read_text();new=(ROOT/'manuscripts'/entry/'report.tex').read_text();changed=original
 for old,replacement in changes:assert changed.count(old)==1,(entry,old);changed=changed.replace(old,replacement,1)
 assert changed==new,entry
 result['attribution'].append({'entry':entry,'source':source,'author_only_transform_matches':True,'changes':len(changes),'original_sha256':sha(original.encode()),'attributed_sha256':sha(new.encode())})
 diffs.extend(difflib.unified_diff(original.splitlines(True),new.splitlines(True),fromfile=source,tofile=entry+'/report.tex'))
for sidecar in ['candidate_matrix.tex','multiplier_table.tex']:
 assert (ROOT/'submitted/IE11_recovery/report'/sidecar).read_bytes()==(ROOT/'manuscripts/IE-11'/sidecar).read_bytes()
# Verify embedded manifests against delivered bytes; record rather than suppress missing paths.
for name,data in payload.items():
 if PurePosixPath(name).name not in ['MANIFEST.sha256','SHA256SUMS']:continue
 entries=[]
 for line in data.decode().splitlines():
  if not line.strip():continue
  m=re.match(r'^([0-9a-fA-F]{64})\s+\*?(.+)$',line)
  if not m:entries.append({'line':line,'status':'unparsed'});continue
  digest,rel=m.groups();key=str(PurePosixPath(name).parent/rel)
  entries.append({'path':key,'status':'missing' if key not in payload else 'match' if sha(payload[key])==digest else 'mismatch'})
 result['manifests'].append({'path':name,'entries':len(entries),'failures':[e for e in entries if e['status']!='match']})
result['payload_files_matched']=len(payload)-len(result['payload_mismatches']);result['python_archive_files_parsed']=len(code_files)
result['passed']=not result['archive_hazards'] and not result['payload_mismatches'] and not result['unmatched_tracked_payloads'] and all(x['author_only_transform_matches'] for x in result['attribution'])
Path('/private/tmp/nla-249-provenance.json').write_text(json.dumps(result,indent=2)+'\n')
Path('/private/tmp/nla-249-provenance-attribution.diff').write_text(''.join(diffs))
print(json.dumps({k:v for k,v in result.items() if k not in ['archives','nested_archives']},indent=2))
print('archive counts',[(x['name'],x['files']) for x in result['archives']]);print('nested counts',[(x['name'],x['files']) for x in result['nested_archives']])
