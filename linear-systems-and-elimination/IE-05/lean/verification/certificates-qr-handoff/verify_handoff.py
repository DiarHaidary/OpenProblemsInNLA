#!/usr/bin/env python3
"""Read-only bounded helper evidence verifier. No builds, writes or cache access.

Run normally after sealing; --preseal checks preserved inputs and actual results
before the outer seal exists. The mathematical result is the recorded helper
completion, not a new final proof approval or Linux/Comparator execution.
"""
from pathlib import Path
import argparse,hashlib,json,re
E=Path(__file__).resolve().parent;P=E.parents[1]
M=E/'EVIDENCE-MANIFEST.json';REPORT=P/'reviews/certificates-qr-completion.md'
def unique(pairs):
 d={}
 for k,v in pairs:
  assert k not in d,('duplicate JSON key',k)
  d[k]=v
 return d
def load(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def sha(p):
 assert p.is_file() and not p.is_symlink(),str(p)
 return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,v):
 h=v if isinstance(v,str) else v['sha256']
 assert sha(p)==h,('hash',str(p))
 if isinstance(v,dict) and 'bytes' in v:assert p.stat().st_size==v['bytes'],('size',str(p))

def verify(preseal=False):
 b=load(E/'INPUTS.json');assert b['file_count']==len(b['files'])==1210
 assert not any('Witness' in n or 'witness-development' in n for n in b['files'])
 for n,v in b['files'].items():check(P/n,v)
 for n,h in b['pins'].items():check(P/n,h)
 freeze=load(P/'reviews/statement-freeze.json');assert len(freeze['files'])==733
 for n,h in freeze['files'].items():check(P/n,h);assert (P/n).stat().st_size==freeze['file_sizes'][n]
 gate=load(P/'verification/proof-start.json');assert gate['proof_authorized'] and not gate['fully_verified']
 prior=[]
 for item in b['prior_manifests']:
  m=P/item['path'];check(m,item['sha256']);base=P/item['base'];data=load(m)
  assert len(data['files'])==item['entries']
  assert (base/data['exact_self_exclusion']).resolve()==m.resolve()
  bound={(base/n).resolve() for n in data['files']}
  assert len(bound)==len(data['files']) and m.resolve() not in bound
  for n,v in data['files'].items():
   q=(base/n).resolve();assert q.is_relative_to(P) and str(q.relative_to(P)) in b['files'];check(q,v)
  own={q.resolve() for q in m.parent.rglob('*') if q.is_file() and q.resolve()!=m.resolve()}
  assert {q for q in bound if q.is_relative_to(m.parent)}==own
  prior.append({'path':item['path'],'sha256':sha(m),'files':len(bound),'own_files':len(own)})
 assert len(prior)==4
 note=load(E/'ROOT-NOTE.json');assert sha(E/'ROOT-NOTE.json')=='253a215374601297c216bf1d5afa529771c1d78a6d6bf137ff9e468406545003'
 check(P/note['exact_retained_snapshot'],note['diagnostic_sha256'])
 assert not (P/note['diagnostic_removed_from_mathematical_module_directory']).exists()
 for n,h in note['source_imports_held_fixed'].items():check(P/n,h)
 fix=P/'verification/exactcert-diagnostic-referee/PatchedCertificates.lean'
 assert fix.read_bytes()==(P/'NLA/IE05/ExactCertificates.lean').read_bytes()
 final=load(E/'latest.json');A=E/final['attempt'];check(A/'result.json',final['result_sha256'])
 result=load(A/'result.json');audit=load(E/'AUDIT-RESULT.json')
 assert final['pass'] and result['pass'] and result['prefix_initial_files']==[]
 assert result['sources_unchanged_after'] and result['boundary_before']==result['boundary_after']
 assert result['boundary_before']['all_match'] and result['boundary_before']['file_count']==1210
 assert result['pins_before']==result['pins_after'] and len(result['pins_before'])==10
 assert sum(p['build_directory_present'] for p in result['pins_before'])==9
 assert {p['name']:p['rev'] for p in result['pins_before']}=={p['name']:p['rev'] for p in load(P/'lake-manifest.json')['packages']}
 assert all(p['tracked_clean'] for p in result['pins_before'])
 assert len(result['LEAN_PATH'].split(':'))==11 and result['LEAN_PATH'].split(':')[0]==result['prefix']
 assert result['Lean_binary_sha256']=='1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554'
 assert '4.33.1' in result['Lean_version'] and 'arm64-apple-darwin' in result['Lean_version']
 for n,v in result['source_snapshots'].items():check(P/n,v);check(A/'source'/n,v)
 sources=[]
 for c in result['commands']:
  assert c['exit_code']==0
  for s in ['stdout','stderr']:check(A/(c['label']+'.'+s),c[s+'_sha256'])
  if c['label'] in ['Definitions','Scaling','QR','IntegerQR','ExactCertificates','Inspect']:
   sources.append(c['label'])
   assert not (A/(c['label']+'.stderr')).read_bytes()
   assert not re.search(r'\b(?:error|warning):',(A/(c['label']+'.stdout')).read_text())
   rel=result['modules'][len(sources)-1]
   assert c['argv'][-1]==rel and Path(c['cwd']).resolve()==(A/'source').resolve()
   assert Path(c['argv'][2]).resolve()==(Path(result['prefix'])/Path(rel).with_suffix('.olean')).resolve()
 assert sources==['Definitions','Scaling','QR','IntegerQR','ExactCertificates','Inspect']
 assert len(result['commands'])==47
 check(A/'objects-before-removal.json',result['objects_sha256'])
 assert len(load(A/'objects-before-removal.json'))==result['object_count']==12
 assert result['own_prefix_removed'] and not Path(result['prefix']).exists()
 closure=load(E/'ACTUAL-DECLARATION-CLOSURE.json');assert closure['total']==len(closure['declarations'])==36
 log=(A/'Inspect.stdout').read_text()
 declarations={m.group(1):{'kind':m.group(2),'axioms':[a.strip() for a in m.group(3).split(',') if a.strip()]}
   for m in re.finditer(r'ACTUAL_DECL (\S+) KIND (\S+) AXIOMS \[([^]]*)\]',log)}
 edges={m.group(1):[n.strip() for n in m.group(2).split(',') if n.strip()]
   for m in re.finditer(r'ACTUAL_EDGE (\S+): \[([^]]*)\]',log)}
 assert declarations==closure['declarations'] and edges==closure['edges']
 seen=set();pending=closure['actual_roots'][:]
 while pending:
  n=pending.pop()
  if n in seen:continue
  seen.add(n);pending+=edges[n]
 assert seen==set(declarations) and all('CertificatesQRExpected' not in n for n in seen)
 assert len(closure['actual_roots'])==4 and len(closure['decide_kernel_auxiliaries'])==3
 for n in closure['decide_kernel_auxiliaries']:assert declarations[n]['kind']=='theorem'
 assert set(closure['module_local_instance_constants'])=={'NLA.IE05._proved.integerLowerZeroDecidable','NLA.IE05._proved.integerTZeroDecidable'}
 assert edges['Int.instDecidableEq']==['Int.decEq'] and declarations['Int.decEq']['axioms']==[]
 assert re.findall(r'^EXACT_EXPECTED_TYPE (\S+):',log,re.M)==closure['actual_roots']
 assert re.findall(r'^REQUIRED_ACTUAL_DEPENDENCY (\S+)$',log,re.M)==closure['required_actual_dependencies']
 assert len(closure['required_actual_dependencies'])==19
 ax=load(E/'AXIOM-RECORDS.json');assert len(ax['records'])==28
 allowed={'propext','Classical.choice','Quot.sound'}
 assert all(set(x['axioms'])<=allowed for x in ax['records'])
 assert sum(set(x['axioms'])==allowed for x in ax['records'])==24
 assert sum(x['axioms']==['propext'] for x in ax['records'])==2 and sum(not x['axioms'] for x in ax['records'])==2
 assert len(re.findall(r'^#assert_trust kernel ',(E/'Inspect.lean').read_text(),re.M))==8
 assert sum(len(re.findall(r'^#assert_trust kernel ',(P/n).read_text(),re.M)) for n in result['modules'][:5])==20
 expected=load(E/'expected-type-extraction.json')
 check(P/'Challenge.lean',expected['Challenge_sha256']);check(P/'NLA/IE05/ExactCertificates.lean',expected['ExactCertificates_sha256'])
 assert len(expected['headers'])==3 and all(h['equal_modulo_whitespace'] for h in expected['headers'].values())
 hist=load(E/'ROOT-ATTEMPT-AUDIT.json');assert hist['total']==len(hist['attempts'])==13
 assert hist['passed']==3 and hist['failed']==10
 for h in hist['attempts']:
  a=P/h['attempt'];check(a/'runner.py.txt',h['original_runner_sha256']);check(a/'inputs.json',h['inputs_sha256']);check(a/'objects.json',h['objects_sha256'])
  assert load(a/'results.json')==h['commands'] and h['pass']==all(c['exit_code']==0 for c in h['commands'])
  for c in h['commands']:check(a/(c['module']+'.log'),c['log_sha256'])
 cleanup=load(E/'root-prefix-cleanup.json');assert cleanup['attempts']==cleanup['removed_prefixes']==13 and cleanup['removed_objects']==20
 for c in cleanup['records']:
  a=P/c['attempt'];check(a/'inputs.json',c['inputs_sha256']);check(a/'objects.json',c['objects_sha256'])
  original=load(a/'inputs.json');assert original['prefix']==c['recorded_prefix']
  assert c['actual_objects_before_removal']=={x['path']:{'sha256':x['sha256'],'bytes':x['bytes']} for x in load(a/'objects.json')}
  assert c['removed_after_exact_match'] and not Path(c['recorded_prefix']).exists()
 for r in load(E/'PRIMARY-SOURCES.json')['sources'].values():check(E/r['snapshot'],r)
 assert audit['status']=='HELPER_COMPLETION_INSPECTION_PASS' and not audit['independent_final_proof_approval'] and not audit['actual_Linux_Comparator']
 for d in (E/'commands').iterdir():
  r=d/'result.json'
  if not r.exists():
   assert preseal,'incomplete postseal command receipt'
   continue
  rec=load(r)
  for s in ['stdout','stderr']:check(d/s,rec[s+'_sha256'])
  for src in rec['actual_script_sources']:check(d/src['snapshot'],src['sha256'])
  assert rec['exit_code']==0
 count=None
 if preseal:assert not M.exists()
 else:
  seal=load(M);assert seal['exact_self_exclusion']==str(M.relative_to(P))
  own={str(q.relative_to(P)) for q in E.rglob('*') if q.is_file() and q!=M}
  expected_paths=set(b['files'])|own|{str(REPORT.relative_to(P))}
  assert set(seal['files'])==expected_paths and len(seal['files'])==seal['file_count']
  assert str(M.relative_to(P)) not in seal['files']
  for n,v in seal['files'].items():check(P/n,v)
  count=len(seal['files'])
 return {'status':'IE05_CERTIFICATES_QR_HELPER_HANDOFF_PASS','scope':'bounded helper completion inspection',
  'source_commands':6,'all_fresh_command_receipts':47,'frozen_inputs':733,'stable_scoped_inputs':1210,
  'prior_complete_seals':prior,'certificate_type_equalities':3,'generic_QR_LU_type_equality':1,
  'actual_closure':36,'decide_kernel_auxiliaries':3,'local_instances':2,'material_dependencies':19,
  'source_kernel_assertions':20,'inspector_kernel_assertions':8,'printed_allowed_axiom_records':28,
  'warnings':0,'root_attempts_retained':13,'root_prefixes_exactly_matched_and_removed':13,
  'root_objects_removed':20,'fresh_own_objects_hashed_and_removed':12,'whole_problem_approval':False,
  'Linux_or_Comparator':False,'mathematical_source_edits':False,'sealed_files':count,
  'ExactCertificates_sha256':sha(P/'NLA/IE05/ExactCertificates.lean'),
  'IntegerQR_sha256':sha(P/'NLA/IE05/IntegerQR.lean')}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--preseal',action='store_true')
 print(json.dumps(verify(parser.parse_args().preseal),indent=2))
