#!/usr/bin/env python3
"""Read-only preauthoring gate for the RA20 Linux candidate documentation."""
from pathlib import Path
import datetime,hashlib,json,subprocess
D=Path(__file__).resolve().parent
P=Path('/tmp/nla-lean-ra20-worktree/randomized-and-low-rank-approximation/RA-20/lean')
R=P.parents[2]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
gate=P/'verification/final-review-acceptance.json'
assert sha(gate)=='a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb'
g=json.loads(gate.read_text());assert g['gate'].startswith('ACCEPT both independent final mathematical approvals')
assert len(g['reports'])==2
proof=P/'verification/proof-freeze.json';f=json.loads(proof.read_text())
assert sha(proof)=='f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f'
for n,h in f['files'].items():assert sha(P/n)==h,n
s=json.loads((P/'reviews/statement-freeze.json').read_text())
for n,h in s['files'].items():assert sha(P/n)==h,n
for n,h in f['source_files'].items():
    assert sha(R/n)==h and sha(P/'verification/original-sources'/n)==h,n
    b=subprocess.check_output(['git','show',f['base']+':'+n],cwd=R)
    assert hashlib.sha256(b).hexdigest()==h,n
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['source_git_blobs'][n],n
reviews=[]
for r in g['reports']:
    assert sha(P/r['report'])==r['sha256']
    mf=P/r['evidence']['file'];assert sha(mf)==r['evidence']['sha256']
    m=json.loads(mf.read_text());assert len(m['files'])==r['evidence']['bound_files']
    for n,v in m['files'].items():
        q=mf.parent/n;h=v if isinstance(v,str) else v['sha256'];assert sha(q)==h,(str(mf),n)
        if isinstance(v,dict) and 'bytes' in v:assert q.stat().st_size==v['bytes'],n
    reviews.append({'reviewer':r['reviewer'],'report':r['report'],'sha256':r['sha256'],
                    'evidence':r['evidence'],'all_entries_rehashed':True})
assert not (P/'formalization.yaml').exists()
assert not (P/'verification/pre-candidate-README.md').exists()
assert not (P/'verification/linux-candidate-2026-09-13').exists()
assert sha(P/'README.md')=='7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
baseline={str(q.relative_to(P)):{'sha256':sha(q),'bytes':q.stat().st_size} for q in sorted(P.rglob('*')) if q.is_file()}
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','author':'/root/ra20_final_referee1',
     'role':'Previously independent final mathematical referee 1; now candidate-document author, adding no review approval',
     'root_gate_sha256':sha(gate),'proof_freeze_sha256':sha(proof),'proof_inputs':len(f['files']),
     'statement_inputs':len(s['files']),'original_sources_and_Git_blobs':len(f['source_files']),
     'complete_final_reviews':reviews,'baseline_count':len(baseline),'baseline':baseline,
     'permitted_existing_change':'README.md only, with exact frozen bytes archived at verification/pre-candidate-README.md',
     'canonical_status':'Solved, unchanged','actual_Linux_and_packaging_review':'Pending'}
(D/'preflight.json').write_text(json.dumps(out,indent=2)+'\n')
(D/'preflight-read-diagnostic.json').write_text(json.dumps({'attempt':'Read tools/lean/validate.py','result':'File not found; no mutation; actual tools/lean/validate_manifest.py found and read'},indent=2)+'\n')
print(json.dumps({'status':'PASS','baseline_count':len(baseline),'frozen_inputs':len(f['files']),
                  'statement_inputs':len(s['files']),'original_sources':len(f['source_files']),
                  'review_inventories':[r['evidence']['bound_files'] for r in reviews],'preflight_sha256':sha(D/'preflight.json')}))
