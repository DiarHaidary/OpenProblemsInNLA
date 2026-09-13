"""Read-only exact Git/blob source binding with no bulk source/cache copy."""
from pathlib import Path
import hashlib,json,os,subprocess,traceback
E=Path(__file__).resolve().parent
R=Path('/tmp/nla-lean-ie05-worktree')
COMMIT='71cf72f9db2af0f01b5cfa7f18a69e28310eb52f'
PROJECT='linear-systems-and-elimination/IE-05/lean'
P=R/PROJECT
B=E/'candidate-binding';B.mkdir(exist_ok=False)
(B/'executed.py').write_bytes(Path(__file__).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def record(b):return {'sha256':sha(b),'bytes':len(b)}
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
r={'candidate_commit':COMMIT,'project':PROJECT,'success':False,'commands':[]}
def run(argv,label,data=None,retain=True):
 c=subprocess.run(argv,cwd=R,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                  env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
 (B/(label+'.stderr')).write_bytes(c.stderr)
 if data is not None:(B/(label+'.stdin')).write_bytes(data)
 if retain:(B/(label+'.stdout')).write_bytes(c.stdout)
 r['commands'].append({'argv':argv,'cwd':str(R),'exit_code':c.returncode,
     'stdout':record(c.stdout),'stderr':record(c.stderr),'raw_stdout_retained':retain,
     'note':None if retain else 'Bulk blob stream hashed while inspected, not duplicated on disk; every immutable Git blob identity and current byte hash retained below.'})
 assert c.returncode==0
 return c.stdout
try:
 assert run(['git','rev-parse','HEAD'],'head').decode().strip()==COMMIT
 run(['git','diff','--exit-code','HEAD','--',PROJECT],'candidate-worktree-diff')
 paths=['AGENTS.md','docs/lean/REVIEW.md','docs/lean/HARNESS.md']
 # The actual harness guide is tools/lean/HARNESS.md; no guessed absent file is queried.
 paths=['AGENTS.md','docs/lean/REVIEW.md','docs/lean/schema/README.md','docs/lean/schema/v0.4.schema.json',
   'tools/lean/HARNESS.md','tools/lean/harness.py','tools/lean/source-lock.json','tools/lean/validate_manifest.py',
   'tools/lean/projects.py','tools/lean/requirements.txt','tools/lean/bootstrap.sh','tools/lean/verify.sh',
   'tools/lean/selftest.sh','.github/workflows/lean-verification.yml','problem_ids.json',
   'linear-systems-and-elimination/IE-05/README.md']
 rawtree=run(['git','ls-tree','-r','-z',COMMIT,'--',PROJECT,*paths],'git-tree')
 entries=[]
 for entry in rawtree.split(b'\0'):
  if not entry:continue
  meta,name=entry.split(b'\t',1);mode,kind,blob=meta.decode().split();name=name.decode()
  assert kind=='blob' and mode in {'100644','100755'}
  entries.append((name,mode,blob))
 unique=list(dict.fromkeys(blob for _,_,blob in entries))
 raw=run(['git','cat-file','--batch'],'unique-git-blobs', ''.join(x+'\n' for x in unique).encode(),False)
 blobs={};pos=0
 for expected in unique:
  end=raw.index(b'\n',pos);blob,kind,size=raw[pos:end].decode().split();start=end+1;n=int(size);b=raw[start:start+n];pos=start+n+1
  assert blob==expected and kind=='blob' and len(b)==n
  assert hashlib.sha1(b'blob '+str(n).encode()+b'\0'+b).hexdigest()==blob
  blobs[blob]=b
 assert pos==len(raw)
 material={str(p.relative_to(P)) for p in (P/'NLA/IE05').glob('*.lean')}|{'Challenge.lean','Solution.lean','comparator.json','lakefile.toml','lake-manifest.json','lean-toolchain','formalization.yaml','README.md','SourceCorrespondence.md'}
 inputs={};governance={}
 for name,mode,blob in entries:
  b=blobs[blob];current=(R/name);assert not current.is_symlink() and current.read_bytes()==b,name
  info={'git_blob':blob,'mode':mode,**record(b)}
  if name.startswith(PROJECT+'/'):
   rel=name[len(PROJECT)+1:];assert '.lake' not in Path(rel).parts and Path(rel).suffix not in {'.olean','.ilean','.o','.so','.a'}
   inputs[rel]=info
   if rel in material:
    target=B/'material-sources'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
  else:
   governance[name]=info;target=B/'governing-sources'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
 assert len(inputs)==2543
 assert inputs['verification/candidate-inputs.json']['sha256']=='b1259a165e924357b5474dcb9620ab316dec218e31a95665138cde4359f285e7'
 assert inputs['verification/coordinator-candidate/ROOT-CHECKS.json']['sha256']=='07bc78ceb06e62f347162ff68d34a4b78d42a328b578f23b9d8a270d448805ca'
 live={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}
 assert live==set(inputs),'Untracked or missing candidate input'
 original_manifest=json.loads((P/'verification/candidate-inputs.json').read_text())
 for name,x in original_manifest['files'].items():assert {k:inputs[name][k] for k in ['sha256','bytes']}==x
 assert original_manifest['file_count']==2404
 assert governance['linear-systems-and-elimination/IE-05/README.md']['git_blob']=='8224c5ba49ce68198e18124245e3e736ed9ca569'
 save(B/'git-inputs.json',{'candidate_commit':COMMIT,'project':PROJECT,'file_count':2543,'files':inputs})
 save(B/'governing-inputs.json',{'candidate_commit':COMMIT,'files':governance})
 r.update({'success':True,'candidate_inputs':2543,'governing_inputs':len(governance),'unique_blobs':len(unique),
   'project_worktree_equals_committed_bytes':True,'frozen_2405_candidate_selection_unchanged':True,
   'original_target_and_Solved_status_unchanged':True,'material_source_copies':len(material),
   'no_dependency_or_bulk_project_copy':True})
except Exception:r['error']=traceback.format_exc()
save(B/'result.json',r)
print(json.dumps({k:v for k,v in r.items() if k!='commands'},indent=2))
raise SystemExit(0 if r['success'] else 1)
