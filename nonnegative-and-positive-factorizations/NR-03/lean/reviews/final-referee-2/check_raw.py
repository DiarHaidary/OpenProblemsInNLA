from pathlib import Path
import json, hashlib, subprocess, re, zipfile, os, tempfile
E=Path('/tmp/nla-nr03-canonical-linux-repaired')
R=Path('/tmp/nla-lean-nr03-publication-worktree')
O=Path(__file__).resolve().parent
H='f664d07e82aaa60bc9c78dd1946e763168c5c530'
P='nonnegative-and-positive-factorizations/NR-03/lean'
raw=E/'extracted/verify-20260913T215907Z-4140'
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *a:subprocess.check_output(['git','-c','gc.auto=0','-C',str(R),*a])
write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
r=json.loads((raw/'result.json').read_text()); api=json.loads((E/'artifacts-final.json').read_text())['artifacts'][0]
run=json.loads((E/'run-final.json').read_text()); jobs=json.loads((E/'jobs-final.json').read_text())['jobs']; job=next(j for j in jobs if j['id']==103799711659)
assert run['id']==34785341662 and run['head_sha']==H and run['conclusion']=='success'
assert job['conclusion']=='success' and job['run_id']==34785341662
z=E/'artifact.zip'; assert z.stat().st_size==21628 and sha(z.read_bytes())==api['digest'].removeprefix('sha256:')=='91f80abcbbb0f10fbf614ab259fbf5121a8dabd5c600969a260e3b8b2c8e267c'
assert api['id']==10326896988 and api['workflow_run']['head_sha']==H and api['workflow_run']['id']==34785341662
with zipfile.ZipFile(z) as f:
 names=[n for n in f.namelist() if not n.endswith('/')]; assert len(names)==13
 for n in names: assert f.read(n)==(E/'extracted'/n).read_bytes()
assert r['repository_commit']==H and r['project']==P and r['result']=='comparator-accepted'
inputs=r['input_sha256']; files=git('ls-tree','-r','--name-only',H,'--',P).decode().splitlines(); assert len(inputs)==len(files)==113
assert {x.removeprefix(P+'/') for x in files}==set(inputs)
for p,h in inputs.items(): assert sha(git('show',H+':'+P+'/'+p))==h
cfg=json.loads(git('show',H+':'+P+'/comparator.json')); assert cfg==r['config'] and len(cfg['theorem_names'])==10
std={'propext','Classical.choice','Quot.sound'};assert set(cfg['permitted_axioms'])==std
pins=json.loads(git('show',H+':'+P+'/lake-manifest.json'))['packages']
actual=dict(re.findall(r"info: ([^:]+): checking out revision '([0-9a-f]+)'",(raw/'dependencies.log').read_text()))
assert actual=={x['name']:x['rev'] for x in pins} and len(actual)==10
assert r['tool_receipt']['lean_toolchain']=='leanprover/lean4:v4.33.1'
assert 'x86_64-unknown-linux-gnu' in r['tool_receipt']['lean_version']
assert r['source_lock_sha256']==r['tool_receipt']['source_lock_sha256']==sha(git('show',H+':tools/lean/source-lock.json'))
assert r['tool_receipt']['forsythe_commit']=='8d1b0c0545a77b40245e84705aa7d273e6c81e62'
log=(raw/'comparator.log').read_text(); assert log.rstrip().endswith('EXIT_STATUS=0')
for s in ['Built NLA.NR03.Rank','Built Solution','Running Lean default kernel on solution.','Lean default kernel accepts the solution','Your solution is okay!']:assert s in log
axioms={n:sorted(x.strip() for x in a.split(',')) for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",log)}
assert len(axioms)==403 and all(set(a)==std for a in axioms.values())
assert all(n in axioms for n in cfg['theorem_names'])
rows={n for n in axioms if '.RowCertificate.' in n};assert len(rows)==384
assert rows=={f'NLA.NR03.RowCertificate.{f}.row{i}' for f in ['Singleton','Pair','Four'] for i in range(128)}
mods=set(re.findall(r'Built (NLA\.NR03\.[A-Za-z0-9_.]+|Solution)\b',log));assert len(mods)==58
sol=git('show',H+':'+P+'/Solution.lean').decode(); assertions=re.findall(r'^#assert_trust kernel (\S+)',sol,re.M)
assert assertions==cfg['theorem_names'] and 'LeanCert.Tactic.Verification' in sol
kr=(raw/'kernel-controls.log').read_text(); cr=(raw/'comparator-controls.log').read_text(); sa=(raw/'sandbox.log').read_text()
assert 'PASS: all three actual Comparator.runBuiltinKernel cases behaved as required' in kr and kr.rstrip().endswith('EXIT_STATUS=0')
assert 'PASS: all five Comparator regressions' in cr and cr.rstrip().endswith('EXIT_STATUS=0')
assert sa.count('Sandbox UID: 1001')==2 and 'PASS AF_UNIX socket creation: denied' in sa and 'Outer and export fixture contents unchanged' in sa and sa.rstrip().endswith('EXIT_STATUS=0')
for f,m in [('negative-sorry.log',"Illegal axiom detected: 'sorryAx'"),('negative-native.log','Illegal axiom detected: \'checked._native.native_decide.ax_1_1\'')]:
 t=(raw/f).read_text(); assert m in t and t.rstrip().endswith('EXIT_STATUS=1')
# Bind the original complete mathematical review and the only subsequent Lean delta.
prior=Path('/tmp/nla-nr03-canonical-root-final-referee/REVIEW.md');delta=Path('/tmp/nla-nr03-rank-cast-root-review/REVIEW.md')
assert sha(prior.read_bytes())=='c55ea0a61a23519df2389b6aa5735fa9a8830b9f69e2aae27b18c0f4857cc58b'
assert sha(delta.read_bytes())=='48d192162cc5c97fbc974d9ce6f12e0d9210217b6f40b8b2cd7c74b956d248cc'
old='523c5aeaddd8bf7c2dc01afb053bb0dea8811335';leanfiles=[p for p in inputs if p.endswith('.lean')]
for p in leanfiles:
 b=git('show',H+':'+P+'/'+p);a=git('show',old+':'+P+'/'+p)
 if p=='NLA/NR03/Rank.lean':assert b.replace(b'    change (0 : \xe2\x84\x9d) \xe2\x89\xa4 (W i k : \xe2\x84\x9d)\n',b'',1)==a
 else:assert a==b
out={'verdict':'accepted','reviewer':'/root','role':'independent Lean mathematical reviewer; integration and metadata author, not a Lean proof-body author','commit':H,'run':34785341662,'job':103799711659,'artifact':10326896988,'artifact_sha256':sha(z.read_bytes()),'raw_result_sha256':sha((raw/'result.json').read_bytes()),'raw_comparator_sha256':sha((raw/'comparator.log').read_bytes()),'package_inputs':len(inputs),'active_modules_built':len(mods),'public_exports':cfg['theorem_names'],'actual_public_axioms':{n:axioms[n] for n in cfg['theorem_names']},'all_403_printed_axiom_closures_standard_only':True,'all_384_rows_present':True,'default_kernel':True,'comparator':True,'leancert_kernel_assertions':True,'sandbox':True,'negative_controls':True,'pins':actual,'source_delta_only_rank_change':True,'prior_full_math_review_sha256':sha(prior.read_bytes()),'rank_delta_review_sha256':sha(delta.read_bytes()),'raw_extracted_hashes':{n:sha((E/'extracted'/n).read_bytes()) for n in names},'no_local_lean_or_lake':True}
write(O/'CHECKS.json',out)
write(O/'BINDINGS.json',{'checked_git_inputs':inputs,'prior_review':str(prior),'rank_review':str(delta),'actual_run_json_sha256':sha((E/'run-final.json').read_bytes()),'actual_jobs_json_sha256':sha((E/'jobs-final.json').read_bytes()),'artifacts_json_sha256':sha((E/'artifacts-final.json').read_bytes())})
print(json.dumps({k:v for k,v in out.items() if k not in ['raw_extracted_hashes','pins','actual_public_axioms']},indent=2))
