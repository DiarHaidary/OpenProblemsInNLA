#!/usr/bin/env python3
"""Read-only complete publication preservation check with exact version mappings.

No network, Lean build, writes or edits to historical seals are performed.
The preauthoring original operational audit was run before wrapper changes;
this checker verifies continuity to those accepted immutable candidate bytes.
"""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess
E=Path(__file__).resolve().parent;P=E.parents[1];R=P.parents[2]
SELF=E/'EVIDENCE-MANIFEST.json'
OLD='7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
CANDIDATE='43603b173beb294c2588d83f936a8a96246fd5f0'
BASE='5830ed4fb06da0659414a3deb2a40ad327aca052'
ROOT_OUTER=P/'verification/root-linux-acceptance-2026-09-13/EVIDENCE-MANIFEST.json'
DIAGNOSTIC='verification/root-linux-acceptance-2026-09-13/initial-scope-diagnostic/EVIDENCE-MANIFEST.json'

def sha(p):
 assert p.is_file() and not p.is_symlink(),('missing or symlink',str(p))
 return hashlib.sha256(p.read_bytes()).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:
  assert k not in d,('duplicate JSON key',k)
  d[k]=v
 return d
def load(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def resolved(p,h):
 p=p.resolve()
 if p==(P/'README.md').resolve() and h==OLD:return P/'verification/pre-candidate-README.md'
 for a in load(E/'ARCHIVES.json')['archives']:
  if p==(R/a['original_repository_path']).resolve() and h==a['expected_sha256']:
   return P/a['archive_project_path']
 return p
def check(p,v,historical=False):
 h=v if isinstance(v,str) else v['sha256']
 q=resolved(p,h) if historical else p
 assert sha(q)==h,('wrong hash',str(p))
 if isinstance(v,dict) and 'bytes' in v:assert q.stat().st_size==v['bytes'],('wrong size',str(p))

def sealed_scope():
 scope={q.resolve() for q in P.rglob('*') if q.is_file() and q.resolve()!=SELF.resolve()}
 scope|={(ROOT_OUTER.parent/n).resolve() for n in load(ROOT_OUTER)['files']}
 scope|={(R/n).resolve() for n in load(E/'PREFLIGHT.json')['other_publication_inputs']}
 scope|={R/n for n in ['tools/render_problems.py','tools/update_catalog.py','tools/format_math.py','tools/problem-template.tex','tools/github_math.lua','tests/test_problem_ids.py']}
 assert SELF.resolve() not in scope
 return scope

def verify(preseal=False):
 assert sha(E/'PREFLIGHT.json')=='ca08a0e2f2525dd009ee41e7fe99fd0e8d55d54f26884508334c3702bf555b16'
 b=load(E/'PREFLIGHT.json');d=load(E/'DOCUMENT-CHECKS.json')
 assert b['project_baseline_count']==len(b['project_baseline'])==1580
 assert len(b['other_publication_inputs'])==17
 assert d['status']=='FINAL_AUTHOR_DOCUMENT_CHECKS_PASS'
 changed=[]
 for n,v in b['project_baseline'].items():
  check(P/n,v,True)
  if sha(P/n)!=v['sha256']:changed.append(str((P/n).relative_to(R)))
 for n,v in b['other_publication_inputs'].items():
  check(R/n,v,True)
  if sha(R/n)!=v['sha256']:changed.append(n)
 assert sorted(changed)==d['changed_existing_paths'] and len(changed)==9
 assert sorted(n for n in b['project_baseline'] if sha(P/n)!=b['project_baseline'][n]['sha256'])==['README.md','formalization.yaml']
 for n,v in d['outputs'].items():check(R/n,v)
 assert sha(R/'problem_ids.json')==b['registry_sha256'] and len(load(R/'problem_ids.json'))==217
 archives=load(E/'ARCHIVES.json')['archives'];assert len(archives)==19
 for a in archives:check(P/a['archive_project_path'],a['expected_sha256'])
 for n,h in b['anchors'].items():check(P/n,h,True)
 gate=load(P/'verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json')
 assert gate['fully_verified'] and gate['verdict']=='ACCEPT complete-target Lean verification'
 assert gate['actual_Ubuntu_run']==34743832047 and gate['candidate']==CANDIDATE
 assert load(E/'operational-recheck-result.json')['exit_code']==0
 before=load(E/'operational-recheck.stdout')
 assert before['status']=='INDEPENDENT_RA20_OPERATIONAL_SEAL_PASS' and before['read_only_runtime_recheck']=='PASS'
 assert before['file_count']==1589 and before['candidate_Git_inputs']==1092

 nested=[]
 for n in b['project_baseline']:
  if n.endswith('EVIDENCE-MANIFEST.json') or n=='reviews/statement-package-manifest.json':
   path=P/n;m=load(path)
   if n==DIAGNOSTIC:
    # The accepted root seal binds this deliberately rejected attempt byte-for-byte.
    why=load(path.parent/'observed-failure.json')
    assert why['observed_tool_exit_code']==1 and 'incomplete and is not counted' in why['reason']
    assert len(m['files'])==1596
    continue
   parent=P if n=='reviews/statement-package-manifest.json' else path.parent
   for k,v in m['files'].items():check(parent/k,v,True)
   nested.append({'file':n,'sha256':sha(path),'entries':len(m['files'])})
 assert len(nested)==19
 proof=load(P/'verification/proof-freeze.json');statement=load(P/'reviews/statement-freeze.json')
 for frozen,count in [(proof,521),(statement,68)]:
  assert len(frozen['files'])==count
  for n,h in frozen['files'].items():check(P/n,h,True)
 assert proof['source_files']==statement['source_files'] and len(proof['source_files'])==16
 env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
 for n,h in proof['source_files'].items():
  check(R/n,h,True);check(P/'verification/original-sources'/n,h)
  raw=subprocess.check_output(['git','show',BASE+':'+n],cwd=R,env=env)
  assert hashlib.sha256(raw).hexdigest()==h
  assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==proof['source_git_blobs'][n]
 binding=load(P/'verification/linux-run-2026-09-13/source-binding.json')
 assert binding['candidate']==CANDIDATE and len(binding['candidate_inputs'])==1092
 rel=str(P.relative_to(R))+'/'
 names=subprocess.check_output(['git','ls-tree','-r','--name-only',CANDIDATE,'--',rel],cwd=R,env=env,text=True).splitlines()
 assert {n[len(rel):] for n in names}==set(binding['candidate_inputs'])
 raw=subprocess.check_output(['git','cat-file','--batch'],cwd=R,env=env,input=''.join(CANDIDATE+':'+n+'\n' for n in names).encode())
 offset=0
 for n in names:
  end=raw.index(b'\n',offset);oid,kind,size=raw[offset:end].decode().split();size=int(size)
  data=raw[end+1:end+1+size];offset=end+2+size
  v=binding['candidate_inputs'][n[len(rel):]]
  assert oid==v['git_blob'] and kind=='blob' and size==v['bytes']
  assert hashlib.sha256(data).hexdigest()==v['sha256'] and raw[offset-1:offset]==b'\n'
  assert data==resolved(R/n,v['sha256']).read_bytes(),n
 assert offset==len(raw)
 runtime=load(P/'verification/linux-run-2026-09-13/runtime-verification.json')
 assert runtime['candidate']==CANDIDATE and runtime['run']==34743832047 and runtime['run_attempt']==1
 assert runtime['all17_jobs_and_steps_successful'] is True
 assert runtime['source_kernel_assertions']==61 and runtime['actual_printed_standard_three_axiom_occurrences']==57
 assert runtime['distinct_printed_names']==45 and runtime['official_matching_Mathlib_cache_files']==8690
 ax=load(P/'verification/linux-run-2026-09-13/axiom-verification.json')
 assert len(ax['records'])==57
 config=load(P/'comparator.json');assert len(config['theorem_names'])==12 and config['definition_names']==[]
 assert set(config['permitted_axioms'])=={'propext','Classical.choice','Quot.sound'}
 assert runtime['actual_exports']==config['theorem_names']
 canonical=(P.parent/'README.md').read_text();old=(E/'archive/repository/randomized-and-low-rank-approximation/RA-20/README.md').read_text()
 assert canonical[canonical.index('## Statement\n'):]==old[old.index('## Statement\n'):]
 assert '**Status:** Lean verified' in canonical and 'lake build Solution' in canonical
 for n in config['theorem_names']:assert '`'+n.rsplit('.',1)[1]+'`' in canonical
 for item in d['relative_paths_and_links']:
  target=R/item['target']
  if preseal and target.resolve()==SELF.resolve():continue
  assert target.is_file(),item['target']
  if 'sha256' in item:check(target,item['sha256'])
 for c in load(E/'CHECKS.json')['commands']+d['new_checks']:
  assert c['exit_code']==0
 visual=load(E/'VISUAL-QA.json');assert visual['verdict']=='AUTHOR_VISUAL_QA_PASS' and visual['page_count']==3
 check(P.parent/'problem.pdf',visual['PDF_sha256'])
 for page in visual['all_pages']:check(E/page['file'],page['sha256']);assert page['visually_inspected']
 assert (E/'pdf-build/xelatex-2/problem.pdf').read_bytes()==(P.parent/'problem.pdf').read_bytes()
 assert (E/'pdf-build/xelatex-2/problem.tex').read_bytes()==(P.parent/'problem.tex').read_bytes()
 assert load(E/'artifact-operation-result.json')['exit_code']==0
 assert load(E/'artifact-operation-result.json')['before_first_publication_authoring']
 email=re.compile(rb'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
 material={R/n for n in changed}|{q for q in E.rglob('*') if q.is_file()}
 assert not [str(q.relative_to(R)) for q in material if email.search(q.read_bytes())],'email-like publication material'
 own={q.resolve() for q in E.rglob('*') if q.is_file() and q.resolve()!=SELF.resolve()}
 if preseal:
  assert not SELF.exists()
  assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()==CANDIDATE
  new=[str(q.relative_to(P)) for q in P.rglob('*') if q.is_file() and str(q.relative_to(P)) not in b['project_baseline']]
  assert all(n.startswith(str(E.relative_to(P))+'/') for n in new)
  count=None
 else:
  m=load(SELF)
  assert m['exact_self_exclusion']=='EVIDENCE-MANIFEST.json' and m['file_count']==len(m['files'])
  bound={(E/n).resolve() for n in m['files']}
  assert SELF.resolve() not in bound
  assert {q for q in bound if q.is_relative_to(E)}==own
  prior_project={(P/n).resolve() for n in b['project_baseline']}
  assert {q for q in bound if q.is_relative_to(P)}==prior_project|own
  expected_external={q for q in sealed_scope() if not q.is_relative_to(P)}
  assert {q for q in bound if not q.is_relative_to(P)}==expected_external
  for n,v in m['files'].items():check((E/n).resolve(),v)
  assert m['accepted_prior_inventories']==nested
  assert m['root_gate_sha256']==b['anchors']['verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json']
  assert load(E/'VALIDATION.json')['status']=='PUBLICATION_PRESEAL_PASS'
  count=len(bound)
 return {'status':'PUBLICATION_PRESEAL_PASS' if preseal else 'SEALED_RA20_PUBLICATION_PASS',
  'role':'Publication author consistency check; independent publication review pending',
  'candidate':CANDIDATE,'actual_accepted_Ubuntu_run':34743832047,
  'project_baseline':1580,'other_prepublication_inputs':17,'changed_existing_paths':sorted(changed),
  'archives':19,'accepted_prior_inventories':nested,'rejected_diagnostic_manifest_retained':DIAGNOSTIC,
  'proof_inputs':521,'statement_inputs':68,'original_source_Git_identities':16,'exact_candidate_Git_inputs':1092,
  'exports':12,'source_LeanCert_assertions':61,'actual_source_prints':57,'actual_distinct_printed_names':45,
  'official_matching_cache_files':8690,'permanent_IDs':217,'PDF_pages_visually_checked':3,
  'email_like_matches':0,'own_evidence_files_excluding_outer':len(own),'complete_bound_files':count,
  'README_sha256':sha(P/'README.md'),'YAML_sha256':sha(P/'formalization.yaml'),'canonical_README_sha256':sha(P.parent/'README.md'),
  'canonical_TeX_sha256':sha(P.parent/'problem.tex'),'canonical_PDF_sha256':sha(P.parent/'problem.pdf'),
  'outer_sha256':None if preseal else sha(SELF),'publication_commit_push_PR':'not performed by this task',
  'independent_publication_review':'pending'}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--preseal',action='store_true')
 print(json.dumps(verify(parser.parse_args().preseal),indent=2))
