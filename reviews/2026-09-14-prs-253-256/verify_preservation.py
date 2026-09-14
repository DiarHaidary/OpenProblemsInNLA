"""Bind integrated source content and immutable prior material to audited git objects."""
import argparse,json,re,subprocess,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',default='.');p.add_argument('--ref',default='HEAD');p.add_argument('--out',required=True);a=p.parse_args()
BASE='deb549fa9ddd6b119e6c59016f268237e645dfa2'
SOURCES={'253':'43183e8254d121aa4b365fdd34643cc4c91d8503','254':'0ea258baa0bde427540dfb64fee7dfff95e6498c','255':'ecc57b82bbcb33aa37dd403530669f74bdf2ec30','256':'b84772b48cd26a2e763ecc52a6243e8f0c34681f'}
def git(*args):return subprocess.check_output(['git',*args],cwd=a.repo)
def tree(ref):
 return {n.decode():m.decode() for r in git('ls-tree','-rz','--full-tree',ref).split(b'\0') if r for m,n in [r.split(b'\t',1)]}
def read(ref,n):return git('show',f'{ref}:{n}').decode()
def sections(s):
 ms=list(re.finditer(r'^##+ .+$',s,re.M));return {m.group():s[m.start():ms[i+1].start() if i+1<len(ms) else len(s)].strip() for i,m in enumerate(ms)}
head=git('rev-parse',a.ref).decode().strip();bt=tree(BASE);ft=tree(head);allowed={'README.md','CATALOG.md','RESOLVED.md','tools/render_problems.py','eigenvalues-and-inverse-problems/README.md','randomized-and-low-rank-approximation/README.md','references/holden-continuations-2026-09-13/MI-20/README.md'}
for prefix in ['eigenvalues-and-inverse-problems/SP-07/','nonnegative-and-positive-factorizations/NM-01/']:
 allowed.update(prefix+n for n in ['README.md','problem.tex','problem.pdf'])
modified=set();source_details={};added_union=set()
for number,ref in SOURCES.items():
 st=tree(ref);added=set(st)-set(bt);changed={n for n in st.keys()&bt.keys() if st[n]!=bt[n]}
 assert not set(bt)-set(st),(number,'deleted source files')
 for n in added|changed:
  if n not in allowed:assert ft.get(n)==st[n],('source change lost',number,n)
 modified|=changed;added_union|=added
 source_details[number]={'head':ref,'added_files':len(added),'modified_files':sorted(changed),'exactly_preserved_added_files':len(added-allowed)}
 subprocess.run(['git','merge-base','--is-ancestor',ref,head],cwd=a.repo,check=True)
assert not set(bt)-set(ft)
for n,v in bt.items():
 if n not in modified|allowed:assert ft[n]==v,('unrelated change',n)
assert ft['problem_ids.json']==bt['problem_ids.json'];reg=json.loads(read(head,'problem_ids.json'));assert len(reg)==217
old_sections=0;canonical_count=0
for ident,n in reg.items():
 b=read(BASE,n);f=read(head,n)
 # Every previously published named body section remains verbatim, including prior credit.
 for title,body in sections(b).items():
  if ident=='NM-01' and title=='## References':continue
  assert body in f,('old canonical section changed',ident,title)
  old_sections+=1
 if bt[n]!=ft[n]:canonical_count+=1
 for label in ['Difficulty','Importance','Rating rationale']:
  pat=r'^\*\*'+label+r':\*\*.*$'
  bm=re.search(pat,b,re.M);fm=re.search(pat,f,re.M)
  assert (bm.group() if bm else None)==(fm.group() if fm else None),(ident,label)
counts={};transitions={}
for ident,n in reg.items():
 b=re.search(r'^\*\*Status:\*\*\s*(.*?)\s*$',read(BASE,n),re.M)[1];f=re.search(r'^\*\*Status:\*\*\s*(.*?)\s*$',read(head,n),re.M)[1]
 counts[f]=counts.get(f,0)+1
 if b!=f:transitions[ident]=[b,f]
assert counts=={'Open':42,'Partially resolved':73,'Solved':72,'Lean verified':30},counts
assert transitions=={'RA-05':['Partially resolved','Solved'],'SP-03':['Open','Partially resolved']},transitions
for title,body in sections(read(BASE,'RESOLVED.md')).items():
 if title.startswith('### '):assert body in read(head,'RESOLVED.md'),title
for ref in [SOURCES['253'],SOURCES['255']]:
 for title,body in sections(read(ref,'RESOLVED.md')).items():
  if title.startswith('### '):assert body in read(head,'RESOLVED.md'),title
for ref in [SOURCES['254'],SOURCES['255']]:
 for title,body in sections(read(ref,'eigenvalues-and-inverse-problems/SP-07/README.md')).items():assert body in read(head,'eigenvalues-and-inverse-problems/SP-07/README.md'),title
oldrefs=[n for n in bt if n.startswith('references/')]
assert all(ft[n]==bt[n] for n in oldrefs)
for n in bt:
 if n.startswith(('.github/','tests/','tools/lean/','docs/lean/')) or '/lean/' in n:assert ft[n]==bt[n],n
rbase=read(BASE,'tools/render_problems.py');rfinal=read(head,'tools/render_problems.py')
# Compare Python tokens while removing exactly the five intended string elements and their commas.
import io,tokenize
removals={'RA-11','RA-14','SP-07','SP-14','NM-01'}
def tokens(s,remove=False):
 seq=list(tokenize.generate_tokens(io.StringIO(s).readline));out=[];skip_comma=False
 for t in seq:
  if remove and t.type==tokenize.STRING and t.string.strip("'\"") in removals:skip_comma=True;continue
  if skip_comma and t.string==',':skip_comma=False;continue
  if t.type not in [tokenize.ENCODING,tokenize.NL,tokenize.NEWLINE,tokenize.INDENT,tokenize.DEDENT,tokenize.ENDMARKER,tokenize.COMMENT]:out.append((t.type,t.string))
 return out
assert tokens(rbase,True)==tokens(rfinal)
out={'status':'PASS','base':BASE,'reviewed_ref':head,'tree':git('rev-parse',head+'^{tree}').decode().strip(),'source_prs':source_details,'base_paths_retained':len(bt),'new_source_files_retained':len(added_union),'exact_source_addition_exception':'Only the MI-20 reference README disclosure is corrected; original ZIP and proof are unchanged.','old_reference_files_unchanged':len(oldrefs),'permanent_ids':len(reg),'prior_canonical_sections_retained_verbatim':old_sections,'changed_canonical_pages':canonical_count,'status_transitions':transitions,'status_counts':counts,'all_prior_and_new_resolved_records_retained':True,'both_sp07_updates_retained':True,'lean_projects_and_harness_unchanged':True,'renderer_only_removes_reference_breaks':sorted(removals)}
Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
