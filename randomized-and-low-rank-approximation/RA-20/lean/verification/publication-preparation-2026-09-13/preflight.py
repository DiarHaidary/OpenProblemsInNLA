#!/usr/bin/env python3
"""Read-only author gate before RA20 publication editing; no new review approval."""
from pathlib import Path
import hashlib,json,os,subprocess,datetime,time
D=Path(__file__).resolve().parent
R=Path('/tmp/nla-lean-ra20-worktree').resolve()
P=R/'randomized-and-low-rank-approximation/RA-20/lean'
E=P/'verification/publication-preparation-2026-09-13'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
anchors={
 'verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json':'a2c3a74eb858edb859d34d8bd2985dc54710e31816412d285c32a547e080e57e',
 'verification/root-linux-acceptance-2026-09-13/EVIDENCE-MANIFEST.json':'40d68224c966fc5114995418bf47ee2fc38f3ebbacc50536cae3b1c9d98ca0b8',
 'reviews/linux-operational-referee-2026-09-13.md':'7f7532bbc01533d0c35fe0ac3aece0ff66cb43c1444e41275db0784cee6b8ae7',
 'verification/linux-run-2026-09-13/EVIDENCE-MANIFEST.json':'89b3cd2aa8c47835be4531cca85561a70aee7f20be6e9f3bcdaaa48d23812dcd',
 'README.md':'83e19faf1bf25a9748de40da3193cfd68690100923a50379553e288c45b5e8bc',
 'formalization.yaml':'bec9d851e204464fa2d3e29033d5958034665d51c3554d2043f1470bfafd4197'}
for n,h in anchors.items():assert sha(P/n)==h,n
gate=load(P/'verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json')
assert gate['fully_verified'] is True and gate['verdict']=='ACCEPT complete-target Lean verification'
assert gate['candidate']=='43603b173beb294c2588d83f936a8a96246fd5f0'
assert gate['actual_Ubuntu_run']==34743832047
root_outer=P/'verification/root-linux-acceptance-2026-09-13/EVIDENCE-MANIFEST.json'
m=load(root_outer);assert len(m['files'])==1604
for n,v in m['files'].items():
 p=(root_outer.parent/n).resolve();assert sha(p)==v['sha256'] and p.stat().st_size==v['bytes'],n
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
cmd=['python3','-B',str(P/'verification/linux-run-2026-09-13/verify_inventory.py')]
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':str(R),'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'}}
(D/'operational-recheck-command.json').write_text(json.dumps(record,indent=2)+'\n')
t=time.monotonic();s=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(D/'operational-recheck.stdout').write_bytes(s.stdout);(D/'operational-recheck.stderr').write_bytes(s.stderr)
record.update(exit_code=s.returncode,seconds=time.monotonic()-t,stdout_sha256=sha(D/'operational-recheck.stdout'),stderr_sha256=sha(D/'operational-recheck.stderr'))
(D/'operational-recheck-result.json').write_text(json.dumps(record,indent=2)+'\n');assert s.returncode==0,s.stderr.decode()
result=json.loads(s.stdout);assert result['status']=='INDEPENDENT_RA20_OPERATIONAL_SEAL_PASS' and result['file_count']==1589
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()==gate['candidate']
assert not E.exists()
baseline={str(q.relative_to(P)):{'sha256':sha(q),'bytes':q.stat().st_size} for q in sorted(P.rglob('*')) if q.is_file()}
assert len(baseline)==1580
categories=[p for p in R.iterdir() if p.is_dir() and (p/'README.md').is_file() and any(p.glob('[A-Z][A-Z]-*/README.md'))]
possible=[R/'README.md',R/'CATALOG.md',R/'RESOLVED.md']+[p/'README.md' for p in sorted(categories)]+[P.parent/'README.md',P.parent/'problem.tex',P.parent/'problem.pdf']
other={str(q.relative_to(R)):{'sha256':sha(q),'bytes':q.stat().st_size} for q in possible}
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PUBLICATION_PREAUTHOR_GATE_PASS','author':'/root/ra20_final_referee1','role':'Candidate-document and publication author; no independent approval of own publication',
 'candidate':gate['candidate'],'actual_Linux_run':gate['actual_Ubuntu_run'],'anchors':anchors,'root_outer_entries':1604,'operational_recheck':result,
 'project_baseline_count':len(baseline),'project_baseline':baseline,'other_publication_inputs':other,'registry_sha256':sha(R/'problem_ids.json'),'permanent_ID_count':len(load(R/'problem_ids.json')),
 'original_source_base':'5830ed4fb06da0659414a3deb2a40ad327aca052','new_scope':'Current project wrappers, their exact candidate archives, canonical RA20 README/TeX/PDF, generated indexes and RESOLVED, and own publication evidence only'}
(D/'PREFLIGHT.json').write_text(json.dumps(out,indent=2)+'\n')
(D/'navigation-diagnostics.json').write_text(json.dumps({'failed_read':'No root-linux-acceptance verify_inventory.py exists; actual coordinator source and the independent operational verifier read instead','bounded_filename_search':'A broad temporary filename search reported two inaccessible tmp-mount directories; no files from them were read or copied','pandoc':'Not on PATH; existing /tmp/nla-submission-tools/pandoc-3.11-arm64/bin/pandoc located through prior published reproduction record'},indent=2)+'\n')
print(json.dumps({'status':out['status'],'project_baseline':len(baseline),'other_inputs':len(other),'root_bound':1604,'operational_bound':1589,'IDs':217,'preflight_sha256':sha(D/'PREFLIGHT.json')}))
