"""One-shot preservation, cleanup and complete proof freeze before refereeing."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,re,shutil,subprocess,sys,tempfile
P=Path('/tmp/nla-lean-formalization/next-ie05-statements-draft/lean').resolve()
O=P/'verification/assembly-handoff';F=P/'reviews/proof-freeze.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ident=lambda p:{'sha256':sha(p),'bytes':p.stat().st_size}
load=lambda p:json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
assert not O.exists() and not F.exists()
anchors={
 'NLA/IE05/Definitions.lean':'aa9a18994bb8d1889af8b30290cb71846af5424436d720afaf15a54184164dfa',
 'Challenge.lean':'0ccd5424f990587b1bb7170c674cba4645d9427286c916e2e19387234ccf250e',
 'verification/proof-start.json':'2a8e4b4029a6ba005856c9ec56178cc7fefc8b8b16e945df27599ce471c95726',
 'NLA/IE05/GrowthBounds.lean':'3aa83977f50095643fdc93469a95661c55c15a10bd9f8ba04e59dc71988a6160',
 'NLA/IE05/Growth.lean':'82f12e85d35fac9b60eea228f68abaeacf21538ec2a029faa6427709b0b323b6',
 'NLA/IE05/Proof.lean':'f8ef9d1901845439e7c09f4e9d004eb49d87ed28d8a6d567d48ac4d16199a950',
 'Solution.lean':'3e12274c074f9d221230bd3939a76d433532b067c7123a12effe2b9e6f6a5c9a',
 'verification/certificates-qr-handoff/EVIDENCE-MANIFEST.json':'b3a780ff4ed077050224c305aba71af2c27efca4ec03c1b9ecc6f21d11c7d6c1',
 'verification/witness-development/EVIDENCE-MANIFEST.json':'1c9b9c923b38e0224581a3a1f45d0959f24604d9e18edd284948e4df269f7c2a'}
for n,h in anchors.items():assert sha(P/n)==h,n
initial={str(p.relative_to(P)):ident(p) for p in sorted(P.rglob('*')) if p.is_file()}
oldfreeze=load(P/'reviews/statement-freeze.json');assert len(oldfreeze['files'])==733
for n,h in oldfreeze['files'].items():assert sha(P/n)==h,n
R=Path(tempfile.mkdtemp(prefix='ie05-root-proof-freeze-',dir='/tmp/nla-lean-formalization')).resolve()
(R/'executed-freeze.py').write_bytes(Path(__file__).read_bytes())
cmds=[]
def run(label,argv,inp=None):
 c=subprocess.run(argv,cwd=P,input=inp,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for s in ['stdout','stderr']:(R/(label+'.'+s)).write_bytes(getattr(c,s))
 row={'label':label,'argv':argv,'cwd':str(P),'exit_code':c.returncode,'stdout_sha256':sha(R/(label+'.stdout')),'stderr_sha256':sha(R/(label+'.stderr'))}
 if inp is not None:(R/(label+'.stdin')).write_bytes(inp);row['stdin_sha256']=sha(R/(label+'.stdin'))
 cmds.append(row);save(R/'commands.json',cmds)
 assert c.returncode==0,(label,str(R))
 return c.stdout
cert=json.loads(run('certificate-qr-seal',[sys.executable,'-B',str(P/'verification/certificates-qr-handoff/verify_handoff.py')]))
wit=json.loads(run('witness-seal',[sys.executable,'-B',str(P/'verification/witness-development/verify_seal.py')]))
assert cert['sealed_files']==1353 and wit['pass'] and wit['bound_files']==148
original=load(P/'verification/original-source-inventory.json');rows=list(original['files'].items());assert len(rows)==27
query=''.join(original['base']+':'+n+'\n' for n,_ in rows).encode()
raw=run('original-27-git-blobs',['git','-C','/tmp/nla-lean-ra20-worktree','cat-file','--batch'],query);pos=0
for n,r in rows:
 end=raw.index(b'\n',pos);obj,kind,ns=raw[pos:end].decode().split();size=int(ns);b=raw[end+1:end+1+size];pos=end+2+size
 assert raw[pos-1:pos]==b'\n' and kind=='blob' and obj==r['git_blob']
 q=P/'verification/original-sources'/n
 assert b==q.read_bytes() and ident(q)=={'sha256':r['sha256'],'bytes':r['bytes']},n
assert pos==len(raw)
A=P/'verification/assembly-development/attempt-wv3puyku';result=load(A/'result.json')
assert result['pass'] and result['source_commands']==14 and len(result['exact_types'])==17
assert result['actual_project_closure']==181 and result['actual_material_dependencies']==30
assert result['actual_printed_axiom_reports']==result['actual_kernel_assertions']==106 and result['warnings']==0
assert len(result['commands'])==55 and result['before_dependencies']==result['after_dependencies']
for c in result['commands']:
 assert c['exit_code']==0
 for s in ['stdout','stderr']:assert sha(A/(c['label']+'.'+s))==c[s+'_sha256']
for live,r in result['sources'].items():
 assert ident(P/live)==ident(A/'source'/r['snapshot'])=={k:v for k,v in r.items() if k!='snapshot'},live
for a in load(A/'axioms.json'):assert set(a['axioms'])<={'propext','Classical.choice','Quot.sound'}
log=(A/'Inspect.stdout').read_text()
assert re.findall(r'EXACT_FROZEN_TYPE (\S+):',log)==load(P/'comparator.json')['theorem_names']
assert 'COMPLETE_ASSEMBLY roots=17, closure=181, required=30' in log
cleanup=[]
attempts=[
 ('verification/growthbounds-development/attempt-beg_jm6e','old'),
 ('verification/growth-development/attempt-d7ty79mn','old'),
 ('verification/proof-development/attempt-l1c1v_rz','old'),
 ('verification/assembly-development/attempt-_fcoxern','new'),
 ('verification/assembly-development/attempt-wv3puyku','new')]
for rel,kind in attempts:
 a=P/rel
 if kind=='old':
  inp=load(a/'inputs.json');prefix=Path(inp['prefix']).resolve()
  for r in inp['sources']:assert ident(a/'source'/r['path'])=={'sha256':r['sha256'],'bytes':r['bytes']}
  expected={r['path']:{'sha256':r['sha256'],'bytes':r['bytes']} for r in load(a/'objects.json')}
 else:
  r=load(a/'result.json');prefix=Path(r['fresh_private_prefix']).resolve();expected=load(a/'objects.json')
  for info in r['sources'].values():assert ident(a/'source'/info['snapshot'])=={k:v for k,v in info.items() if k!='snapshot'}
 assert prefix.parent==Path('/tmp/nla-lean-formalization/independent-prefixes').resolve() and prefix.name.startswith('ie05-root-')
 assert prefix.is_dir() and not prefix.is_symlink()
 assert not any(q.is_symlink() for q in prefix.rglob('*'))
 actual={str(q.relative_to(prefix)):ident(q) for q in sorted(prefix.rglob('*')) if q.is_file()}
 assert actual==expected,(rel,sorted(actual),sorted(expected))
 cleanup.append({'attempt':rel,'prefix':str(prefix),'objects':actual,'objects_record_sha256':sha(a/'objects.json'),'exact_match_before_removal':True})
 shutil.rmtree(prefix);assert not prefix.exists()
save(R/'root-object-cleanup.json',cleanup)
assert {str(p.relative_to(P)):ident(p) for p in sorted(P.rglob('*')) if p.is_file()}==initial
O.mkdir()
for q in R.iterdir():assert q.is_file() and not q.is_symlink();(O/q.name).write_bytes(q.read_bytes())
utc=datetime.now(timezone.utc).isoformat()
accept={
 'utc':utc,'phase':'Complete author proof assembly accepted for independent final review',
 'root_role':'Proof contributor and coordinator, not independent mathematical referee',
 'root_read_full_helper_sources_and_reports_and_actual_inspectors':True,
 'root_read_only_helper_seals_passed':{'certificates_QR':1353,'Witness':148},
 'fresh_original_Git_sources_checked':27,'frozen_statement_inputs_unchanged':733,
 'final_fresh_attempt':str(A.relative_to(P)),'final_attempt_sha256':sha(A/'result.json'),
 'fresh_source_commands':14,'fresh_total_command_receipts':55,'exact_types':17,'project_closure':181,
 'material_dependencies':30,'source_kernel_assertions':89,'inspector_kernel_assertions':17,
 'actual_axiom_reports':106,'warnings':0,'private_root_prefixes_removed':5,
 'private_root_objects_removed':sum(len(r['objects']) for r in cleanup),
 'historical_diagnostics':'The first complete assembly source run compiled all14 commands and matched all17 types; its driver rejected14 expected-Prop unused-binder warnings. Only expected binder names were alpha-renamed. A final fresh14-command run passed without warnings. Earlier module failures and object records remain unchanged.',
 'comments_only_update':'Proof.lean rational-gap documentation was clarified after the preliminary12-module proof build; the final14-command run compiled the exact final source.',
 'reviewed_anchors':anchors,'fully_verified':False,'independent_final_approvals':0,'actual_Linux_Comparator':False}
save(O/'ROOT-ASSEMBLY-ACCEPTANCE.json',accept)
outer=O/'EVIDENCE-MANIFEST.json'
owned={str(q.relative_to(P)):ident(q) for q in O.rglob('*') if q.is_file()}
for n in ['PROOF-MAP.md',*anchors]:owned[n]=ident(P/n)
save(outer,{'scope':'Every own root assembly-handoff artifact and explicit mathematical/boundary inputs. Only this exact own outer is excluded. Full historical inputs are covered separately by the subsequent whole-project proof freeze.',
 'exact_self_exclusion':str(outer.relative_to(P)),'files':owned})
before={str(q.relative_to(P)):ident(q) for q in sorted(P.rglob('*')) if q.is_file()}
freeze={'utc':utc,'phase':'Complete IE05 proof before independent final mathematical review','base':original['base'],
 'files':{n:r['sha256'] for n,r in before.items()},'file_sizes':{n:r['bytes'] for n,r in before.items()},
 'source_files':{n:r['sha256'] for n,r in original['files'].items()},'source_git_blobs':{n:r['git_blob'] for n,r in original['files'].items()},
 'source_snapshot_directory':'verification/original-sources','frozen_statement_sha256':sha(P/'reviews/statement-freeze.json'),
 'proof_start_sha256':sha(P/'verification/proof-start.json'),'root_assembly_acceptance_sha256':sha(O/'ROOT-ASSEMBLY-ACCEPTANCE.json'),
 'root_assembly_evidence_sha256':sha(outer),'final_author_source_attempt_sha256':sha(A/'result.json'),
 'configured_contracts':load(P/'comparator.json')['theorem_names'],'exact_self_exclusion':str(F.relative_to(P)),
 'inventory_rule':'Every project file existing before independent final review, including all earlier manifests and diagnostics; no basename exemptions. Later reviews and publication phases are separate additions.',
 'status':'Ready for two independent final mathematical reviews; not Lean verified',
 'known_metadata_phase':'The frozen statement-phase Lake defaultTargets remains Challenge. Each proof check explicitly compiles Solution. Candidate packaging must select Solution by default with exact archival bindings before publication.'}
save(F,freeze)
receipt={'problem':'IE-05','complete_author_proof':True,'fully_verified':False,'frozen_project_inputs':len(before),'original_Git_sources':27,
 'proof_freeze_sha256':sha(F),'root_assembly_acceptance_sha256':sha(O/'ROOT-ASSEMBLY-ACCEPTANCE.json'),'root_assembly_evidence_sha256':sha(outer),
 'final_author_attempt_sha256':sha(A/'result.json'),'exact_exports':17,'actual_project_closure':181,'actual_axiom_reports':106,
 'root_objects_removed':accept['private_root_objects_removed'],'source_modules':{str(q.relative_to(P)):sha(q) for q in sorted((P/'NLA/IE05').glob('*.lean'))},
 'Solution_sha256':sha(P/'Solution.lean'),'PROOF_MAP_sha256':sha(P/'PROOF-MAP.md')}
save(Path('/tmp/nla-lean-formalization/IE-05-final-proof-freeze.json'),receipt)
print(json.dumps(receipt,indent=2))
