from pathlib import Path
import hashlib,json,re,subprocess,itertools,datetime,os,tempfile
R=Path('/tmp/nla-lean-nr03-publication-worktree')
P=R/'nonnegative-and-positive-factorizations/NR-03/lean'
O=Path('/tmp/nla-nr03-canonical-root-final-referee')
H='523c5aeaddd8bf7c2dc01afb053bb0dea8811335'
def sha(x):return hashlib.sha256(x).hexdigest()
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(R),*a])
def save(n,d):
 fd,t=tempfile.mkstemp(prefix=n+'.',dir=O)
 with os.fdopen(fd,'w') as f:json.dump(d,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(t,O/n)
assert git('rev-parse','HEAD').decode().strip()==H
prefix=str(P.relative_to(R))+'/'
paths=git('ls-tree','-r','--name-only',H,'--',prefix).decode().splitlines()
inputs={}
for rp in paths:
 rel=rp[len(prefix):];actual=(P/rel).read_bytes();assert actual==git('show',H+':'+rp),rel
 inputs[rel]=sha(actual)
assert len(inputs)==102
m=json.loads((P/'ACTIVE-MODULE-MANIFEST.json').read_text())
active={x['path']:x for x in m['active_modules']}
assert len(active)==58
for n,e in active.items():
 assert inputs[n]==e['sha256'],n
 assert (P/n).read_bytes()==git('show',m['source_commit']+':'+e['source_path']),n
inventory=json.loads((P/'reviews/proof-candidate-hashes.json').read_text())['files_excluding_this_manifest']
assert inventory=={k:v for k,v in inputs.items() if k!='reviews/proof-candidate-hashes.json'}
for n,h in m['frozen_boundary'].items():
 assert inputs['NLA/NR03/Definitions.lean' if n=='Definitions.lean' else n]==h,n
# Nested block comments and line comments are stripped for source-level token checks only.
def code(s):
 out=[];i=0;depth=0
 while i<len(s):
  if s[i:i+2]=='/-':depth+=1;i+=2
  elif depth and s[i:i+2]=='-/':depth-=1;i+=2
  elif depth:i+=1
  elif s[i:i+2]=='--':
   j=s.find('\n',i);i=len(s) if j<0 else j
  else:out.append(s[i]);i+=1
 assert depth==0
 return ''.join(out)
texts={n:code((P/n).read_text()) for n in active}
for n,s in texts.items():
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|sorryAx|ofReduceBool)\b',s),n
mods={n[:-5].replace('/','.'):n for n in active}
graph={n:[] for n in active}
for n,s in texts.items():
 for imp in re.findall(r'^import\s+(\S+)',s,re.M):
  if imp.startswith('NLA.NR03.') or imp=='Solution':
   assert imp in mods,(n,imp);graph[n].append(mods[imp])
  assert imp not in ['Challenge','NLA.NR03.CertificateData']
seen=set();visiting=set()
def visit(n):
 assert n not in visiting,n
 if n in seen:return
 visiting.add(n)
 for x in graph[n]:visit(x)
 visiting.remove(n);seen.add(n)
visit('Solution.lean');assert seen==set(active)
fi=texts['NLA/NR03/FamilyIdentities.lean']
coverage={}
for family in ['Singleton','Pair','Four']:
 prefixf='NLA/NR03/RowCertificate/'+family+'/'
 rows=[]
 for n,s in texts.items():
  if n.startswith(prefixf):
   hits=re.findall(r'theorem row(\d+) : ∀ b : Mask7,\s*'+family.lower()+r'Sum \((\d+) : Mask7\) b = '+family.lower()+r'Closed \((\d+) : Mask7\) b := by\s*decide \+kernel',s)
   assert len(hits)==8,(n,hits)
   for a,b,c in hits:assert a==b==c;rows.append(int(a))
 assert sorted(rows)==list(range(128)),family
 used=[int(x) for x in re.findall(r'exact RowCertificate\.'+family+r'\.row(\d+)',fi)]
 assert used==list(range(128)),family
 coverage[family]={'rows':128,'columns_per_row':128,'blocks':16,'kernel_decisions':128,'assembly_covers_each_row_once':True}
fd=texts['NLA/NR03/FamilyDefs.lean']
for name,k in [('pairMasks',2),('fourMasks',4)]:
 nums=list(map(int,re.findall(r'\d+',re.search(r'def '+name+r' : Array Nat :=\s*#\[(.*?)\]',fd,re.S).group(1))))
 assert sorted(nums)==sorted(sum(1<<i for i in x) for x in itertools.combinations(range(7),k))
challenge=code((P/'Challenge.lean').read_text())
pat=r'theorem\s+(\w+)\s*(.*?)\s*:=\s*by'
targets={n:re.sub(r'\s+',' ',t).strip() for n,t in re.findall(pat,challenge,re.S)}
proofs={n:re.sub(r'\s+',' ',t).strip() for n,t in re.findall(pat,texts['NLA/NR03/Rank.lean'],re.S)}
cfg=json.loads((P/'comparator.json').read_text());names=cfg['theorem_names']
assert len(names)==10
for full in names:
 short=full.split('.')[-1];assert targets[short]==proofs[short],short
 assert '#assert_trust kernel '+full in texts['Solution.lean']
 assert '#print axioms '+full in texts['Solution.lean']
assert cfg['permitted_axioms']==['propext','Classical.choice','Quot.sound']
checks={'scope':'Independent second full mathematical SOURCE review; actual canonical mechanical acceptance pending','commit':H,'reviewer':'/root, integrator/metadata author, no NR03 Lean proof-body authorship','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'committed_project_files_matching':len(inputs),'active_modules_matching_reviewed_development_source':len(active),'acyclic_solution_closure_equals_active_set':True,'source_literal_trust_scan':'PASS; source scan alone is not transitive axiom verification','frozen_contracts_unchanged':True,'ten_raw_source_signatures_identical':True,'finite_families':coverage,'complete_pair_and_four_enumerations':True,'no_local_Lean_Lake_run':True,'actual_run_pending':34783909558,'whole_problem_verified':False}
save('INPUT-HASHES.json',inputs);save('CHECKS.json',checks)
print(json.dumps(checks,indent=2))
