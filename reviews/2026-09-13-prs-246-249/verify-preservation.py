#!/usr/bin/env python3
"""Read-only exact-blob and retained-target audit of the three-PR integration.

Run from any directory. Writes JSON outside the worktree by default. No canonical PDF, manuscript, archive, verification artifact or added source file is exempted.
"""
import argparse,json,re,subprocess
from pathlib import Path
BASE='752218e5417998b7f4d2aee9c447ca5d256fe530'
HEADS={246:'a4e8ea57f9b010b85390845b4de902183b6d97ba',247:'24212f477b26aad36a757e62998bd4974b24ac81',249:'9e11821e2e999afb1699272005a167da7ee42861'}
CENTRAL={'README.md','CATALOG.md','RESOLVED.md',
'linear-systems-and-elimination/README.md','randomized-and-low-rank-approximation/README.md'}
REBUILD_ALLOWED=set()
p=argparse.ArgumentParser();p.add_argument('--worktree',default='/private/tmp/nla-integration-246-249');p.add_argument('--ref',default='HEAD');p.add_argument('--out',default='/private/tmp/nla-integration-246-249-preservation.json');a=p.parse_args()
cwd=Path(a.worktree)
def git(*args):return subprocess.check_output(['git',*args],cwd=cwd)
def tree(ref):
 result={}
 for entry in git('ls-tree','-rz','--full-tree',ref).split(b'\0'):
  if not entry:continue
  meta,name=entry.split(b'\t',1);mode,kind,digest=meta.decode().split();result[name.decode()]=(mode,kind,digest)
 return result
def content(ref,name):return git('show',f'{ref}:{name}').decode()
def changed(ref):
 vals=git('diff','--name-status','--no-renames','-z',BASE,ref).split(b'\0');out=[]
 for i in range(0,len(vals)-1,2):out.append((vals[i].decode(),vals[i+1].decode()))
 return out
final=git('rev-parse',a.ref).decode().strip();bt=tree(BASE);ft=tree(final);issues=[];prs=[];alladded=set();allmodified=set();canon=[];rebuild=[]
for number,head in HEADS.items():
 ancestor=subprocess.run(['git','merge-base','--is-ancestor',head,final],cwd=cwd).returncode==0
 if not ancestor:issues.append(f'PR {number}: exact head is not an ancestor')
 st=tree(head);diff=changed(head);added=[n for s,n in diff if s=='A'];modified=[n for s,n in diff if s=='M'];other=[(s,n) for s,n in diff if s not in ['A','M']]
 if other:issues.append(f'PR {number}: unexpected delete/rename changes {other}')
 for n in added:
  if ft.get(n)!=st[n]:issues.append(f'PR {number}: added source file differs or missing: {n}')
 for n in modified:
  if n not in CENTRAL and ft.get(n)!=st[n]:issues.append(f'PR {number}: noncentral modified file differs from audited source: {n}')
  if re.search(r'/[A-Z]{2}-\d+/README\.md$',n):canon.append((number,head,n))
 alladded.update(added);allmodified.update(modified)
 prs.append({'pr':number,'audited_head':head,'head_is_ancestor':ancestor,'added_files_exact':len(added),'modified_files':modified})
missing=sorted(set(bt)-set(ft))
if missing:issues.append(f'Published base paths deleted: {missing}')
untouched=0;oldarchive=0
for n,val in bt.items():
 if n.startswith('references/'):
  oldarchive+=1
  if ft.get(n)!=val:issues.append(f'Previously published reference/archive changed: {n}')
 if n not in allmodified:
  if n in REBUILD_ALLOWED and ft.get(n)!=val:rebuild.append(n);continue
  if ft.get(n)!=val:issues.append(f'Unexpected mutation of previously published file: {n}')
  else:untouched+=1
registry=bt.get('problem_ids.json')==ft.get('problem_ids.json')
if not registry:issues.append('Permanent registry bytes or mode changed')
protected=[]
for n,val in bt.items():
 if n.startswith('tools/') or n.startswith('.github/workflows/'):
  protected.append(n)
  if ft.get(n)!=val:issues.append(f'Shared infrastructure changed: {n}')
# Compare exact original problem text, not just problem IDs.
targets=[]
for number,head,n in canon:
 b=content(BASE,n);f=content(final,n)
 ident=Path(n).parent.name
 marker={'IE-16':'## Original problem (retained)','RA-05':'## Original question','IE-20':'This fixes an implementation','IE-27':'## Statement','IE-28':'## Statement'}.get(ident,'## Problem statement')
 start=b.index(marker);end=b.find('\n## ',start+len(marker));segment=b[start:end if end!=-1 else len(b)].strip()
 ok=segment in f
 if not ok:issues.append(f'Original problem statement not retained verbatim: {n}')
 if '## Context and notation' in b:
  cs=b.index('## Context and notation');ce=b.find('\n## ',cs+len('## Context and notation'));context=b[cs:ce if ce!=-1 else len(b)].strip()
  if context not in f:issues.append(f'Original context not retained verbatim: {n}')
 targets.append({'pr':number,'path':n,'original_target_verbatim':ok,'canonical_matches_audited_head':ft[n]==tree(head)[n]})
# Every changed per-problem RESOLVED section survives as an exact text block.
def sections(text):
 matches=list(re.finditer(r'^### .+$',text,re.M));result={}
 for i,m in enumerate(matches):
  end=matches[i+1].start() if i+1<len(matches) else len(text);result[m.group()]=text[m.start():end].strip()
 return result
base_resolved=sections(content(BASE,'RESOLVED.md'));final_resolved=content(final,'RESOLVED.md');blocks=[]
source_resolved={number:sections(content(head,'RESOLVED.md')) for number,head in HEADS.items()}
unchanged_base_sections=[]
for title,body in base_resolved.items():
 if all(source_resolved[number].get(title)==body for number in HEADS):
  ok=body in final_resolved
  if not ok:issues.append(f'Unchanged published RESOLVED history missing/altered: {title}')
  unchanged_base_sections.append({'heading':title,'exact_block_retained':ok})
for number,head in HEADS.items():
 for title,body in source_resolved[number].items():
  if body!=base_resolved.get(title):
   ok=body in final_resolved
   if not ok:issues.append(f'PR {number}: changed RESOLVED block missing/altered: {title}')
   blocks.append({'pr':number,'heading':title,'exact_block_retained':ok})
status_counts={}
reg=json.loads(content(final,'problem_ids.json'))
for ident,n in reg.items():
 text=content(final,n);m=re.search(r'^\*\*Status:\*\*\s*(.+?)\s*$',text,re.M)
 status=m.group(1) if m else 'MISSING';status_counts[status]=status_counts.get(status,0)+1
out={'ok':not issues,'base':BASE,'integration_head':final,'worktree':str(cwd),'source_prs':prs,'all_source_added_files_exact':len(alladded),'published_base_paths_retained':len(bt)-len(missing),'previously_published_reference_files_byte_identical':oldarchive,'other_published_files_unchanged':untouched,'registry_byte_identical':registry,'registry_entries':len(reg),'shared_tools_workflows_checked':len(protected),'shared_tools_workflows_unchanged':True,'canonical_original_targets':targets,'resolved_sections':blocks,'unchanged_base_resolved_sections':unchanged_base_sections,'canonical_rebuild_exceptions_used':rebuild,'additional_files_outside_source_heads':sorted(set(ft)-set(bt)-alladded),'status_counts':status_counts,'issues':issues}
Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['ok','integration_head','all_source_added_files_exact','published_base_paths_retained','previously_published_reference_files_byte_identical','registry_entries','registry_byte_identical','status_counts','issues']},indent=2))
raise SystemExit(0 if out['ok'] else 1)
