import pathlib,re,json,hashlib,subprocess,itertools
from fractions import Fraction as F
out={}
for num,tag in [(240,'SP-06'),(241,'IS-02')]:
 repo=pathlib.Path(f'/private/tmp/nla-audit-{num}'); root=repo/'eigenvalues-and-inverse-problems'/tag/'lean'
 item={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()}
 closure=[]
 def walk(p):
  if p in closure:return
  closure.append(p)
  for mod in re.findall(r'^import ([\w.]+)',p.read_text(),re.M):
   q=root/(mod.replace('.','/')+'.lean')
   if q.exists():walk(q)
 walk(root/'Solution.lean')
 item['proof_closure']={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in closure}
 item['forbidden_tokens']={}
 for p in closure:
  txt=re.sub(r'/-.*?-/', '',p.read_text(),flags=re.S);txt=re.sub(r'--[^\n]*','',txt)
  bad=re.findall(r'\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|run_tac|elab|macro)\b',txt)
  if bad:item['forbidden_tokens'][str(p.relative_to(root))]=bad
 item['challenge_in_closure']=root/'Challenge.lean' in closure
 configs=json.loads((root/'comparator.json').read_text());item['export_count']=len(configs['theorem_names'])
 decls={m.group(1):' '.join(m.group(2).split()) for p in closure for m in re.finditer(r'\btheorem\s+(\w+)(.*?):=',p.read_text(),re.S)}
 chall={m.group(1):' '.join(m.group(2).split()) for m in re.finditer(r'\btheorem\s+(\w+)(.*?):=',(root/'Challenge.lean').read_text(),re.S)}
 item['source_type_comparison']={name:decls.get(name.rsplit('.',1)[-1])==chall.get(name.rsplit('.',1)[-1]) for name in configs['theorem_names']}
 item['frozen_boundary_matches']={}
 for f in ['STATEMENT-ACCEPTANCE.json','FINAL-ACCEPTANCE.json']:
  data=json.loads((root/'reviews'/f).read_text());item['frozen_boundary_matches'][f]={p:hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in data['boundary_files'].items()}
 item['original_source_hashes']={}
 for path,blob,h in re.findall(r'`([^`]+)` \| `([a-f0-9]{40})` \| `([a-f0-9]{64})`',(root/'SOURCE_MAP.md').read_text()):
  data=subprocess.check_output(['git','show','50838e37dd793830e2cecd1055cfc7e0349490f1:'+path],cwd=repo)
  gotblob=subprocess.check_output(['git','rev-parse','50838e37dd793830e2cecd1055cfc7e0349490f1:'+path],cwd=repo,text=True).strip()
  item['original_source_hashes'][path]=hashlib.sha256(data).hexdigest()==h and blob==gotblob
 out[tag]=item

def add(p,q):
 r=p.copy()
 for k,v in q.items():r[k]=r.get(k,F(0))+v
 return {k:v for k,v in r.items() if v}
def mul(p,q):
 r={}
 for i,a in p.items():
  for j,b in q.items():r[i+j]=r.get(i+j,F(0))+a*b
 return {k:v for k,v in r.items() if v}
def charpoly(A):
 n=len(A);ans={}
 for p in itertools.permutations(range(n)):
  inv=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n));v={0:F((-1)**inv)}
  for i,j in enumerate(p):v=mul(v,add({0:-F(A[i][j])},{1:F(1)} if i==j else {}))
  ans=add(ans,v)
 return ans
A=[[0,1,0,0],[1,0,0,0],[0,0,F(1,2),F(1,2)],[0,0,F(1,2),F(1,2)]]
a={-1:F(8),1:F(8),2:F(1)}; b={-2:F(-64),-1:F(8),0:F(-128),1:F(-8),2:F(-63),3:F(-16),4:F(-1)}
comp=add(a,{k:-v for k,v in mul(a,a).items()}); cT=charpoly([[-128,8],[-8,-128]]); cA=charpoly(A)
expected=mul(mul({1:F(1)},{1:F(1),0:F(1)}),mul({1:F(1),0:F(-1)},{1:F(1),0:F(-1)}))
out['independent_exact_arithmetic']={'sp06_composition_equal':comp==b,'sp06_charpoly':{k:str(v) for k,v in cT.items()},'sp06_minus128_plus8i_root':cT=={0:F(16448),1:F(256),2:F(1)},'is02_trace':str(sum(A[i][i] for i in range(4))),'is02_charpoly':{k:str(v) for k,v in cA.items()},'is02_charpoly_is_x_times_xplus1_times_xminus1_squared':cA==expected}
p=pathlib.Path('/private/tmp/nla-pr-240-241-independent-checks.json');p.write_text(json.dumps(out,indent=2)+'\n');print(p);print(json.dumps(out,indent=2))
