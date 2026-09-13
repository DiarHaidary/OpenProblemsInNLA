"""Commit the reviewed unchanged proof candidate for actual Linux verification."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, subprocess, sys
W=Path('/tmp/nla-lean-ie05-worktree').resolve()
prefix='linear-systems-and-elimination/IE-05/lean/'
P=W/prefix
O=P/'verification/coordinator-candidate'
E=Path('/tmp/nla-lean-formalization/ie05-root-candidate-install')
PY='/tmp/nla-lean-formalization/venv/bin/python'
BASE='1c467f88fbf6f6853afe5562e17b81ab421b95a6'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ident=lambda p:{'sha256':sha(p),'bytes':p.stat().st_size}
load=lambda p:json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=W)
assert not (O/'ROOT-CHECKS.json').exists()
assert git('rev-parse','HEAD').decode().strip()==BASE
assert git('branch','--show-current').decode().strip()=='codex/lean-ie05-orthogonal-extremizer'
assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
assert git('rev-parse','origin/main').decode().strip()==BASE
assert git('hash-object','linear-systems-and-elimination/IE-05/README.md').decode().strip()=='8224c5ba49ce68198e18124245e3e736ed9ca569'
assert '**Status:** Solved' in (P.parent/'README.md').read_text()
registry=load(W/'problem_ids.json');assert len(registry)==217
assert all((W/path).is_file() for path in registry.values())
for n,r in load(P/'verification/candidate-inputs.json')['files'].items():assert ident(P/n)==r,n
assert sha(P/'verification/candidate-inputs.json')=='b1259a165e924357b5474dcb9620ab316dec218e31a95665138cde4359f285e7'
assert sha(P/'verification/final-review-acceptance.json')=='6e1de72e81a0603066544133f7bb52a7217b31bd6f05372a8c1abe109ff03d61'
before={str(q.relative_to(P)):ident(q) for q in sorted(P.rglob('*')) if q.is_file()}
commands=[]
def run(label,argv,cwd=W):
    c=subprocess.run(argv,cwd=cwd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for s in ['stdout','stderr']:(E/(label+'.'+s)).write_bytes(getattr(c,s))
    row={'label':label,'argv':argv,'cwd':str(cwd),'returncode':c.returncode,
        'stdout':ident(E/(label+'.stdout')),'stderr':ident(E/(label+'.stderr'))}
    commands.append(row);save(E/'precommit-commands.json',commands)
    assert c.returncode==0,(label,c.stderr.decode(),c.stdout.decode()[:1000])
    return c.stdout
run('installed-independent-seal',[sys.executable,'-B',str(O/'verify_installed_packaging.py')])
run('candidate-fixed-archives',[sys.executable,'-B',str(P/'verification/candidate-package/verify_inventory.py'),'--candidate-members-only'])
run('candidate-metadata',[PY,'-B',str(P/'verification/candidate-package/audit_metadata.py')])
run('current-v04-schema',[PY,'-B','tools/lean/validate_manifest.py',str(P)])
run('permanent-IDs',[sys.executable,'-B','tools/validate_problem_ids.py','--base-ref','origin/main'])
run('permanent-ID-tests',[sys.executable,'-B','-m','unittest','discover','-s','tests','-p','test_problem_ids.py','-v'])
assert {str(q.relative_to(P)):ident(q) for q in P.rglob('*') if q.is_file()}==before
new_live=['README.md','SourceCorrespondence.md','formalization.yaml','NOTICE.md']
email=re.compile(rb'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
for n in new_live:assert not email.search((P/n).read_bytes()),n
for n in before:
    assert not re.search(rb'(?i)\b(?:[\w.+-]*stepaniants[\w.+-]*|george[\w.+-]*)@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',(P/n).read_bytes()),n
subprocess.run(['git','add','-f','--',prefix],cwd=W,check=True)
staged=git('diff','--cached','--name-only','-z').decode().split('\0')[:-1]
assert set(staged)=={prefix+n for n in before}
check=subprocess.run(['git','diff','--cached','--check'],cwd=W,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
assert not check.stderr
bound=set(load(P/'verification/candidate-inputs.json')['files'])|{'verification/candidate-inputs.json'}|set(load(O/'installed-external-inputs.json'))
exceptions={}
if check.returncode:
    for line in check.stdout.decode().splitlines():
        if line.startswith('+'):continue
        m=re.fullmatch(r'(.+):\d+: (?:trailing whitespace\.|new blank line at EOF\.)',line)
        if m:
            n=m.group(1);assert n.startswith(prefix) and n[len(prefix):] in bound,n
            exceptions[n]={'sha256':sha(W/n),'reason':'Exact previously sealed proof, source snapshot or raw evidence; no normalization.'}
        elif re.match(r'.+:\d+: ',line):raise AssertionError(line)
    assert exceptions
else:assert check.returncode==0
(E/'staged-whitespace.stdout').write_bytes(check.stdout)
(E/'staged-whitespace.stderr').write_bytes(check.stderr)
save(E/'staged-whitespace-command.json',{'argv':['git','diff','--cached','--check'],'returncode':check.returncode,'exceptions':exceptions})
receipts=O/'root-preflight';receipts.mkdir()
for q in sorted(E.iterdir()):
    assert q.is_file() and not q.is_symlink();(receipts/q.name).write_bytes(q.read_bytes())
(O/'commit_candidate.py').write_bytes(Path(__file__).read_bytes())
raw=receipts/'staged-whitespace.stdout'
exceptions[str(raw.relative_to(W))]={'sha256':sha(raw),'reason':'Exact diagnostic output containing original whitespace.'}
record={'utc':datetime.now(timezone.utc).isoformat(),
    'status':'Root accepts the independent concrete packaging review; candidate ready for actual Ubuntu verification',
    'root_role':'Proof contributor/coordinator; not an independent mathematical, candidate-author, or operational referee',
    'source_gate_sha256':sha(P/'verification/final-review-acceptance.json'),
    'independent_packaging_report_sha256':sha(O/'independent-packaging/REPORT.md'),
    'independent_packaging_seal_sha256':sha(O/'independent-packaging/EVIDENCE-MANIFEST.json'),
    'root_read_full_live_README_SourceCorrespondence_YAML_report_and_verification_scripts':True,
    'candidate_fixed_selection_sha256':sha(P/'verification/candidate-inputs.json'),
    'original_accepted_files':2338,'candidate_fixed_files':2405,'independent_evidence_members':4854,
    'portable_external_evidence_files_installed':112,
    'proof_sources_changed':False,'all_217_IDs_paths_and_targets_preserved':True,
    'canonical_status':'Solved unchanged','fully_verified':False,'actual_Linux_Comparator':'pending',
    'no_new_Lean_compilation':True,'privacy':'George and full Caltech department public; no George email in candidate; empty commit emails required',
    'exact_hash_bound_whitespace_exceptions':exceptions,
    'sparse_checkout_note':'All 217 canonical READMEs retained. CI checks a full Git checkout; project selection is evaluated from Git trees after commit, rather than treating sparse absence as project deletion.',
    'phase_note':'The immutable author candidate metadata records its then-pending packaging review; this separate receipt and retained independent report establish the later approval without rewriting sealed metadata.'}
save(O/'ROOT-CHECKS.json',record)
outer=O/'EVIDENCE-MANIFEST.json'
save(outer,{'scope':'Every coordinator installation and retained external-review file, exact outer self-exclusion only',
    'exact_self_exclusion':'EVIDENCE-MANIFEST.json',
    'files':{str(q.relative_to(O)):ident(q) for q in sorted(O.rglob('*')) if q.is_file()}})
subprocess.run(['git','add','-f','--',prefix],cwd=W,check=True)
cmd=['git','diff','--cached','--check','--','.']+[':(exclude)'+n for n in sorted(exceptions)]
subprocess.run(cmd,cwd=W,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
live={prefix+str(q.relative_to(P)):ident(q) for q in sorted(P.rglob('*')) if q.is_file()}
raw=git('diff','--cached','--raw','--no-abbrev','-z').split(b'\0')
entries=[]
for i in range(0,len(raw)-1,2):
    fields=raw[i].decode().split();name=raw[i+1].decode()
    assert fields[0]==':000000' and fields[1] in ['100644','100755'] and fields[-1]=='A',name
    entries.append((fields[3],name))
assert {n for _,n in entries}==set(live)
data=subprocess.check_output(['git','cat-file','--batch'],cwd=W,input=''.join(oid+'\n' for oid,_ in entries).encode())
pos=0
for oid,name in entries:
    end=data.index(b'\n',pos);actual,kind,size=data[pos:end].decode().split();size=int(size)
    b=data[end+1:end+1+size];pos=end+2+size
    assert actual==oid and kind=='blob' and b==(W/name).read_bytes(),name
assert pos==len(data)
env=dict(os.environ,GIT_AUTHOR_NAME='George Stepaniants',GIT_COMMITTER_NAME='George Stepaniants',GIT_AUTHOR_EMAIL='',GIT_COMMITTER_EMAIL='')
c=subprocess.run(['git','-c','user.name=George Stepaniants','-c','user.email=','-c','commit.gpgsign=false','commit','-m',
    'Add reviewed IE-05 Lean candidate for authoritative Linux verification'],cwd=W,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
assert c.returncode==0,c.stderr.decode()
assert git('show','-s','--format=%ae%x00%ce','HEAD').rstrip(b'\n')==b'\0'
assert not git('status','--porcelain=v1','--untracked-files=all')
receipt={'problem':'IE-05','candidate':git('rev-parse','HEAD').decode().strip(),
    'base':BASE,'branch':'codex/lean-ie05-orthogonal-extremizer','candidate_inputs':len(live),
    'root_candidate_sha256':sha(O/'ROOT-CHECKS.json'),'root_evidence_sha256':sha(outer),
    'candidate_math_manifest_sha256':sha(P/'verification/candidate-inputs.json'),
    'blank_author_and_committer_emails':True,'worktree_clean':True,'canonical_status':'Solved unchanged',
    'actual_Linux':'pending','fully_verified':False}
save(Path('/tmp/nla-lean-formalization/IE-05-candidate-commit.json'),receipt)
print(json.dumps(receipt,indent=2))
