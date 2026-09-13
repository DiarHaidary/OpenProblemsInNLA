#!/usr/bin/env python3
"""Verify the two reviewed submissions and original repository in a frozen Git tree."""
from pathlib import Path, PurePosixPath
import argparse,collections,difflib,hashlib,json,subprocess,unicodedata
BASE='50838e37dd793830e2cecd1055cfc7e0349490f1'
SOURCES={232:('5ce3e36cacbebcafda267eb6a9f2a42c461b189b','linear-systems-and-elimination/IE-05'),233:('ecd7d63a22e40db0967a9cb8e785555a0fad6ca8','eigenvalues-and-inverse-problems/KE-04')}
AUDIT='reviews/2026-09-13-prs-232-233/'
CLARIFICATIONS={232:('contains the uploaded artifacts and the independent operational seal.\n','contains the uploaded artifacts and the independent operational seal.\n\nThe [source correspondence](lean/SourceCorrespondence.md) is preserved from the earlier candidate phase; its “Solved” status and pending-Linux wording are historical and superseded by this verification record.\n'),233:('See the [definitions and source correspondence](lean/SourceCorrespondence.md) and [proof map](lean/PROOF-MAP.md).','See the [historical statement-stage correspondence](lean/SourceCorrespondence.md) and [proof map](lean/PROOF-MAP.md). The correspondence is preserved from before proof implementation; its pending-gate descriptions are historical and superseded by the completed verification below.')}
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',default='.');p.add_argument('--ref',default='HEAD');p.add_argument('--output-prefix',default='/tmp/nla-232-233-preservation');a=p.parse_args()
def git(*args):return subprocess.check_output(['git','-C',a.repo,*args])
def tree(ref):
 d={}
 for line in git('ls-tree','-rz',ref).split(b'\0'):
  if line:
   row,path=line.split(b'\t',1);d[path.decode()]=row.decode().split()
 return d
def text(ref,path):return git('show',ref+':'+path).decode()
fail=[]
def require(condition,message):
 if not condition:fail.append(message)
ref=git('rev-parse',a.ref).decode().strip();base=tree(BASE);final=tree(ref)
require(subprocess.run(['git','-C',a.repo,'merge-base','--is-ancestor',BASE,ref],stdout=subprocess.DEVNULL).returncode==0,'Published base must be an ancestor')
registry=json.loads(text(BASE,'problem_ids.json'));require(len(registry)==217,'217 published IDs');require(text(BASE,'problem_ids.json')==text(ref,'problem_ids.json'),'Exact registry preservation')
allowed={'README.md','CATALOG.md','RESOLVED.md'}
source_records=[];all_new={};expected_resolved=text(BASE,'RESOLVED.md')
for n,(head,root) in SOURCES.items():
 st=tree(head);new=set(st)-set(base);changed={f for f in base.keys()&st.keys() if base[f]!=st[f]};category=root.split('/')[0]+'/README.md';surfaces={root+'/'+f for f in ('README.md','problem.tex','problem.pdf')}|{'README.md','CATALOG.md','RESOLVED.md',category};allowed|=surfaces
 require(not(set(base)-set(st)),f'PR{n}: no removed published path');require(changed==surfaces,f'PR{n}: exactly reviewed seven document changes');require(all(f.startswith(root+'/lean/') for f in new),f'PR{n}: additions only in its Lean project');require(all(st[f][0]=='100644' and st[f][1]=='blob' for f in new),f'PR{n}: only regular nonexecutable authored files')
 require(subprocess.run(['git','-C',a.repo,'merge-base','--is-ancestor',head,ref],stdout=subprocess.DEVNULL).returncode==0,f'PR{n}: exact source head ancestor')
 for f in new:
  require(f not in all_new,f'Unexpected cross-project collision: {f}');all_new[f]=st[f];require(final.get(f)==st[f],f'Authored file changed: {f}')
 canon=root+'/README.md';old=text(BASE,canon);submitted=text(head,canon);current=text(ref,canon);anchor='## Negative resolution' if n==232 else '## Resolution'
 require(old[old.index(anchor):]==submitted[submitted.index(anchor):],f'PR{n}: original target and old proof history byte-identical')
 before,after=CLARIFICATIONS[n];require(submitted.count(before)==1,f'PR{n}: unique reviewed clarification');require(current==submitted.replace(before,after,1),f'PR{n}: only reviewed canonical clarification added')
 require('**Status:** Lean verified' in current,f'PR{n}: correct Lean status');require(final.get(category)==st[category],f'PR{n}: source category index retained')
 old_lines=text(BASE,'RESOLVED.md').splitlines(keepends=True);new_lines=text(head,'RESOLVED.md').splitlines(keepends=True)
 for tag,i,j,k,l in reversed(list(difflib.SequenceMatcher(None,old_lines,new_lines,autojunk=False).get_opcodes())):
  if tag=='equal':continue
  require(tag=='insert',f'PR{n}: resolution history only gains text')
  block=''.join(new_lines[k:l]);tail=''.join(old_lines[i:]);require(expected_resolved.count(tail)==1,f'PR{n}: resolution insertion unambiguous');expected_resolved=expected_resolved.replace(tail,block+tail,1)
 source_records.append({'pr':n,'head':head,'canonical':canon,'authored_files':len(new),'all_authored_blobs_and_modes_retained':True})
require(text(ref,'RESOLVED.md')==expected_resolved,'Exact union of source resolution/credit additions')
for f,entry in base.items():
 require(f in final,f'Published path removed: {f}')
 if f not in allowed:require(final.get(f)==entry,f'Unreviewed published change: {f}')
for f in set(final)-set(base)-set(all_new):require(f.startswith(AUDIT) and final[f][0]=='100644',f'Unreviewed integration addition: {f}')
folded={}
for f in final:
 key=unicodedata.normalize('NFC',f).casefold();require(key not in folded or folded[key]==f,f'Case/Unicode collision: {f}');folded[key]=f
 require(not PurePosixPath(f).is_absolute() and '..' not in PurePosixPath(f).parts,f'Unsafe path: {f}')
counts=collections.Counter()
for ident,canon in registry.items():
 raw=text(ref,canon);status=next(line.split('**Status:** ',1)[1].strip() for line in raw.splitlines() if '**Status:** ' in line);counts[status]+=1
 if ident not in {'IE-05','KE-04'}:require(final[canon]==base[canon],f'Unrelated canonical page changed: {ident}')
require(dict(counts)=={'Lean verified':26,'Solved':75,'Open':46,'Partially resolved':70},'Expected final category counts')
summary='**Resolution evidence:** 75 solved (published or independently audited); 26 solved with Lean verification.'
for f in ('README.md','CATALOG.md'):require(summary in text(ref,f),'Correct combined resolution summary in '+f)
result={'result':'FAIL' if fail else 'PASS','base':BASE,'head':ref,'tree':git('rev-parse',ref+'^{tree}').decode().strip(),'published_paths_retained':len(base),'permanent_ids':len(registry),'sources':source_records,'authored_files_retained':len(all_new),'shared_tools_workflows_and_tests_unchanged':True,'counts':dict(counts),'open_targets':counts['Open']+counts['Partially resolved'],'failures':fail}
out=Path(a.output_prefix);out.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');out.with_suffix('.md').write_text('# Independent source-preservation audit\n\n'+json.dumps(result,indent=2)+'\n\nChecked immutable Git blobs and modes, original target/history bytes, exact source ancestry, permanent IDs, shared verification tools, source document additions, canonical clarifications, and combined status counts. No submitted code was executed.\n')
print(json.dumps(result));raise SystemExit(bool(fail))
