"""One-shot metadata correction retaining the exact original proof freeze.

Mathematical bytes, statement gate and actual completed source builds are unchanged.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess

P=Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean').resolve()
F=P/'reviews/proof-freeze.json'
O=P/'verification/proof-freeze-source-correction'
receipt=Path('/tmp/nla-lean-formalization/KE-04-final-proof-freeze.json')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ident=lambda p:{'sha256':sha(p),'bytes':p.stat().st_size}
load=lambda p:json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
oldhash='d45703f80e35612826060bc53d7a46da7c341234f2edd8cd6269e1ed72c53c16'
assert sha(F)==oldhash and not O.exists()
old=load(F);assert len(old['files'])==3493 and len(old['source_files'])==15
for n,h in old['files'].items():
    assert sha(P/n)==h and (P/n).stat().st_size==old['file_sizes'][n],n
original=load(P/'verification/original-source-inventory.json')
statement=load(P/'reviews/statement-freeze.json')
records={n:{k:r[k] for k in ['commit','upstream_path','git_blob','sha256','bytes']}
    for n,r in original['files'].items()}
assert len(records)==17 and len({(r['commit'],r['upstream_path']) for r in records.values()})==17
assert {n:r['sha256'] for n,r in records.items()}==statement['source_files']
assert {n:r['git_blob'] for n,r in records.items()}==statement['source_git_blobs']
query=''.join(r['commit']+':'+r['upstream_path']+'\n' for r in records.values()).encode()
cmd=['git','-C','/tmp/nla-lean-ra20-worktree','cat-file','--batch']
c=subprocess.run(cmd,input=query,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
assert c.returncode==0 and not c.stderr
pos=0
for n,r in records.items():
    end=c.stdout.index(b'\n',pos);oid,kind,size=c.stdout[pos:end].decode().split();size=int(size)
    data=c.stdout[end+1:end+1+size];pos=end+2+size
    assert kind=='blob' and oid==r['git_blob'] and c.stdout[pos-1:pos]==b'\n'
    assert data==(P/n).read_bytes() and ident(P/n)=={k:r[k] for k in ['sha256','bytes']},n
assert pos==len(c.stdout)
O.mkdir()
(O/'original-proof-freeze.json').write_bytes(F.read_bytes())
(O/'original-coordinator-freeze-receipt.json').write_bytes(receipt.read_bytes())
(O/'executed-correction.py').write_bytes(Path(__file__).read_bytes())
(O/'original-Git.stdout').write_bytes(c.stdout)
(O/'original-Git.stderr').write_bytes(c.stderr)
(O/'original-Git.stdin').write_bytes(query)
save(O/'original-Git-command.json',{'argv':cmd,'returncode':0,'snapshot_count':17,
    'stdout':ident(O/'original-Git.stdout'),'stderr':ident(O/'original-Git.stderr'),'stdin':ident(O/'original-Git.stdin')})
save(O/'source-records.json',records)
save(O/'CORRECTION.json',{
    'utc':datetime.now(timezone.utc).isoformat(),
    'reported_by':'Independent final mathematical referee /root/ra09_final_referee1',
    'defect':'The initial complete proof freeze keyed source convenience maps only by upstream path, collapsing two historical/current version pairs into 15 entries. Its complete 3493-file inventory, the accepted statement freeze and all actual 17-record Git checks were correct.',
    'correction':'All 17 source maps are now keyed by their distinct project-relative snapshot paths, exactly as in the immutable statement freeze. Explicit per-snapshot source commit/path/blob/size/hash records are included.',
    'original_freeze_sha256':oldhash,'original_archive':'verification/proof-freeze-source-correction/original-proof-freeze.json',
    'source_files_changed':False,'numerical_statements_changed':False,'new_Lean_compilation':False,
    'reviewer_checks':'Referee 1 completed source and postflight checks on the original hash before replacement. Referee 2 preserved its original preflight and has not compiled yet. Both must independently rebind the corrected freeze before final approval.',
    'fully_verified':False,'actual_Linux_Comparator':False})
outer=O/'EVIDENCE-MANIFEST.json'
members={str(q.relative_to(P)):ident(q) for q in sorted(O.iterdir()) if q.is_file()}
save(outer,{'scope':'Every file in the metadata-correction directory except the exact outer itself',
    'exact_self_exclusion':str(outer.relative_to(P)),'files':members})
new=dict(old)
new['utc']=datetime.now(timezone.utc).isoformat()
new['source_files']={n:r['sha256'] for n,r in records.items()}
new['source_git_blobs']={n:r['git_blob'] for n,r in records.items()}
new['source_records']=records
new['source_snapshot_directory']='.'
new['source_key_convention']='Exact project-relative snapshot path, not upstream path; each source_records item gives its actual source commit and upstream path. Distinct historical versions are never collapsed.'
new['base_scope']='Canonical/governance base; original-target and original-submission snapshots retain their separately specified historical commits in source_records.'
new['supersedes']={'sha256':oldhash,'archive':'verification/proof-freeze-source-correction/original-proof-freeze.json',
    'reason':'Correct source identity metadata only; no mathematical or numerical statement change.'}
for q in sorted(O.iterdir()):
    if q.is_file():
        n=str(q.relative_to(P));new['files'][n]=sha(q);new['file_sizes'][n]=q.stat().st_size
new['inventory_rule']='Every original pre-final-review file plus the exact metadata-correction evidence. The previous freeze is preserved as a named archive. The only prospective additions omitted are the exact independent final referee report/evidence scopes, which seal themselves separately; no basename exception.'
new['independent_final_review_addition_scopes']=['reviews/final-referee-1.md','reviews/final-referee-1-evidence/','reviews/final-referee-2.md','reviews/final-referee-2-evidence/']
assert 'reviews/proof-freeze.json' not in new['files']
for q in P.rglob('*'):
    assert not q.is_symlink()
    if q.is_file():
        n=str(q.relative_to(P))
        assert n in new['files'] or n=='reviews/proof-freeze.json' or any(n==r or r.endswith('/') and n.startswith(r) for r in new['independent_final_review_addition_scopes']),n
save(F,new)
for n,h in new['files'].items():assert sha(P/n)==h,n
d=load(receipt);d.update({'frozen_project_inputs':len(new['files']),'proof_freeze_sha256':sha(F),
    'previous_proof_freeze_sha256':oldhash,'source_identity_metadata_corrected':True,
    'source_identity_count':17,'source_correction_evidence_sha256':sha(outer)})
save(receipt,d)
print(json.dumps({'proof_freeze_sha256':sha(F),'frozen_project_inputs':len(new['files']),
    'distinct_source_identities':17,'correction_evidence_sha256':sha(outer),
    'mathematical_source_changes':False,'fully_verified':False},indent=2))
