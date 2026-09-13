#!/usr/bin/env python3
"""Verify integration against both the published base and the older source PR base."""
import argparse,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',default='/private/tmp/nla-integration-251');p.add_argument('--ref',default='HEAD');p.add_argument('--out',default='/private/tmp/nla-pr251-preservation.json');a=p.parse_args()
BASE='54f7e76383aea76c96da40281ddbb35f0b729c7b';SOURCE_BASE='752218e5417998b7f4d2aee9c447ca5d256fe530';SOURCE='589ec79798ee42adc7a7160a376c67252280a121'
def git(*s):return subprocess.check_output(['git',*s],cwd=a.repo)
def tree(ref):
 out={}
 for row in git('ls-tree','-rz','--full-tree',ref).split(b'\0'):
  if row:
   meta,name=row.split(b'\t',1);out[name.decode()]=meta.decode()
 return out
def read(ref,n):return git('show',ref+':'+n).decode()
head=git('rev-parse',a.ref).decode().strip();bt,st,ft=tree(BASE),tree(SOURCE),tree(head);d=git('diff','--name-status','--no-renames','-z',SOURCE_BASE,SOURCE).split(b'\0');changes=[(d[i].decode(),d[i+1].decode()) for i in range(0,len(d)-1,2)];assert all(s in ['A','M'] for s,n in changes);added={n for s,n in changes if s=='A'};modified={n for s,n in changes if s=='M'}
central={'README.md','CATALOG.md','RESOLVED.md','nonnegative-and-positive-factorizations/README.md'};issues=[]
for n in added|modified-central:
 if ft.get(n)!=st[n]:issues.append('Audited source blob changed/missing: '+n)
for n,v in bt.items():
 if n not in modified and ft.get(n)!=v:issues.append('Previously published blob changed/missing: '+n)
assert not set(bt)-set(ft)
assert ft['problem_ids.json']==bt['problem_ids.json'];reg=json.loads(read(head,'problem_ids.json'));assert len(reg)==217
for prefix in ['tools/','.github/','tests/','docs/lean/']:
 for n,v in bt.items():
  if n.startswith(prefix):assert ft.get(n)==v,n
n=reg['NR-03'];b=read(BASE,n);f=read(head,n);marker='## Context and notation';assert b[b.index(marker):]==f[f.index(marker):]
def sections(s):
 ms=list(re.finditer(r'^### .+$',s,re.M));return {m.group():s[m.start():(ms[i+1].start() if i+1<len(ms) else len(s))].strip() for i,m in enumerate(ms)}
sb=sections(read(SOURCE_BASE,'RESOLVED.md'));sc=sections(read(SOURCE,'RESOLVED.md'));bc=sections(read(BASE,'RESOLVED.md'));final=read(head,'RESOLVED.md');changed={h:v for h,v in sc.items() if sb.get(h)!=v}
for h,v in changed.items():assert v in final,h
removed=set(sb)-set(sc);assert removed=={'### ✅ NR-03 — quadratic correlation counterexample — Sidney Holden'}
for h,v in bc.items():
 if h not in changed and h not in removed:assert v in final,h
for ref in [BASE,SOURCE]:subprocess.run(['git','merge-base','--is-ancestor',ref,head],cwd=a.repo,check=True)
counts={}
for n in reg.values():
 m=re.search(r'^\*\*Status:\*\*\s*(.*?)\s*$',read(head,n),re.M);assert m;counts[m[1]]=counts.get(m[1],0)+1
assert counts=={'Open':43,'Partially resolved':73,'Solved':71,'Lean verified':30},counts
out={'passed':not issues,'published_base':BASE,'source_base':SOURCE_BASE,'audited_source_head':SOURCE,'integration_head':head,'integration_tree':git('rev-parse',head+'^{tree}').decode().strip(),'added_source_files_preserved_exactly':len(added),'modified_source_files':sorted(modified),'published_base_paths_retained':len(bt),'registry_entries':len(reg),'original_target_and_context_verbatim':True,'shared_infrastructure_unchanged':True,'previous_reference_files_unchanged':sum(n.startswith('references/') for n in bt),'renamed_source_resolved_heading':list(removed),'updated_resolved_blocks_retained':list(changed),'unchanged_resolved_blocks_retained':len(bc)-len(set(bc)&(set(changed)|removed)),'status_counts':counts,'issues':issues};Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert not issues
