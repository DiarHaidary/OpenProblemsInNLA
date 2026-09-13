from pathlib import Path
import datetime, hashlib, json, subprocess, shutil

P=Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean')
PREP=Path('/tmp/nla-lean-formalization/ke04-final-referee2-prep')
E=P/'reviews/final-referee-2-evidence'
EXPECTED='d45703f80e35612826060bc53d7a46da7c341234f2edd8cd6269e1ed72c53c16'
def sha(b): return hashlib.sha256(b).hexdigest()
def write(p,d): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
f=P/'reviews/proof-freeze.json'
assert sha(f.read_bytes())==EXPECTED
d=json.loads(f.read_text()); assert len(d['files'])==3493
errors=[]
for r,h in d['files'].items():
    q=P/r
    if not q.is_file() or sha(q.read_bytes())!=h or q.stat().st_size!=d['file_sizes'][r]: errors.append(r)
assert not errors,errors
assert not E.exists(), 'New reviewer evidence must start absent'
E.mkdir(parents=True)
for q in PREP.rglob('*'):
    if q.is_file():
        z=E/'pre-gate-prep'/q.relative_to(PREP);z.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,z)
write(E/'freeze-before.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'freeze_sha256':EXPECTED,'all_frozen_files':d['files'],'file_count':len(d['files']),'exact_freeze_self':str(f.relative_to(P)),'independence':'No KE04 statement, route, definition, or proof contribution. Independent final mathematical referee 2; unrelated campaign work only.','gate_message':'Root explicitly supplied exact complete freeze and allowed review/build after source-first read.','errors':errors})
commands=[]
def run(argv,cwd,label):
    r=subprocess.run(argv,cwd=cwd,capture_output=True)
    x=E/'provenance'/label;x.parent.mkdir(parents=True,exist_ok=True)
    x.with_suffix('.stdout').write_bytes(r.stdout);x.with_suffix('.stderr').write_bytes(r.stderr)
    c={'argv':argv,'cwd':str(cwd),'exit_code':r.returncode,'stdout':str(x.with_suffix('.stdout').relative_to(E)),'stderr':str(x.with_suffix('.stderr').relative_to(E)),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)};commands.append(c);write(E/'provenance/commands.json',commands)
    assert r.returncode==0,c
    return r.stdout
original=json.loads((P/'verification/original-source-inventory.json').read_text())
gitrepo=Path('/Users/georgestepaniants/Research/OpenProblemsInNLA')
out={}
for i,(rel,rec) in enumerate(original['files'].items()):
    spec=rec['commit']+':'+rec['upstream_path']
    blob=run(['git','rev-parse',spec],gitrepo,f'original-{i:02d}-blob').decode().strip()
    b=run(['git','show',spec],gitrepo,f'original-{i:02d}-bytes')
    assert blob==rec['git_blob'] and sha(b)==rec['sha256'] and b==(P/rel).read_bytes(),rel
    dest=E/'immutable-inputs'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
    out[rel]={'sha256':sha(b),'git_blob':blob,'commit':rec['commit'],'upstream_path':rec['upstream_path'],'bytes':len(b)}
assert len(out)==17
write(E/'originals.json',out)
selected=[str(q.relative_to(P)) for q in (P/'NLA/KE04').glob('*.lean')]+['Solution.lean','Challenge.lean','NUMERICAL_TARGETS.md','SourceCorrespondence.md','README.md','PROOF-MAP.md','comparator.json','lakefile.toml','lake-manifest.json','lean-toolchain','reviews/statement-referee-1.md','reviews/statement-referee-2.md','reviews/statement-freeze.json','reviews/proof-freeze.json','verification/proof-start.json','verification/original-source-inventory.json']
for rel in selected:
    q=P/rel;z=E/'immutable-inputs'/rel;z.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,z)
write(E/'immutable-selected.json',{r:sha((P/r).read_bytes()) for r in sorted(set(selected))})
write(E/'preflight-result.json',{'all_frozen_files_pass':True,'file_count':len(d['files']),'original_git_files':len(out),'proof_freeze':EXPECTED,'selected_input_count':len(set(selected)),'source_review_first':True})
print(json.dumps({'preflight':'PASS','frozen':len(d['files']),'originals':len(out),'evidence':str(E)}))
