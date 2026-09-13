from pathlib import Path
import datetime,hashlib,json,sys

OWN=Path(__file__).resolve().parent; ROOT=OWN.parents[1]
OUTER=OWN/'EVIDENCE-MANIFEST.json'; REPORT=ROOT/'reviews/final-referee-1.md'
FROZEN=ROOT/'reviews/proof-freeze.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
assert not OUTER.exists()
assert sha(FROZEN)=='72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251'
freeze=json.loads(FROZEN.read_text());assert len(freeze['files'])==1800
for rel,h in freeze['files'].items():
    p=ROOT/rel;assert p.is_file() and not p.is_symlink() and sha(p)==h
    assert p.stat().st_size==freeze['file_sizes'][rel]
assert not list((OWN/'attempt-001/objects').iterdir())
dump(OWN/'seal-execution.json',{'argv':['python3',str(Path(__file__).relative_to(ROOT))],'cwd':str(ROOT),
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sealer_sha256':sha(Path(__file__)),
    'report_sha256':sha(REPORT),'proof_freeze_sha256':sha(FROZEN),'checked_frozen_members':1800,
    'verdict':'APPROVE','scope':'Complete independent final mathematical review; macOS source validation, not Linux Comparator'})
own_files=sorted(p for p in OWN.rglob('*') if p.is_file() and p!=OUTER)
assert all(not p.is_symlink() for p in own_files)
files={rel:{'sha256':h,'bytes':freeze['file_sizes'][rel]} for rel,h in freeze['files'].items()}
for p in own_files+[REPORT,FROZEN]:
    rel=str(p.relative_to(ROOT));assert rel not in files
    files[rel]={'sha256':sha(p),'bytes':p.stat().st_size}
assert not any(p.startswith('reviews/final-referee-2') for p in files)
dump(OUTER,{'reviewer':'Codex AI agent /root/ie05_final_math_referee1','verdict':'APPROVE',
    'exact_self_exclusion':str(OUTER.relative_to(ROOT)),'files':files,'file_count':len(files),
    'frozen_input_count':1800,'own_evidence_file_count':len(own_files),
    'report':str(REPORT.relative_to(ROOT)),'proof_freeze':str(FROZEN.relative_to(ROOT)),
    'membership_rule':'Exact 1800 proof-freeze members plus the proof-freeze itself, this report, and every file in this reviewer-owned evidence directory; exclude only this exact outer path. Concurrent final referee 2 files are not selected.'})
print('SEALED',len(files),'files; report',sha(REPORT),'outer',sha(OUTER))
