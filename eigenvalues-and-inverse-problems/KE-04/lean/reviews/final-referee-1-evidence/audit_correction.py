"""Independently bind the corrected source provenance without repeating math builds."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,traceback
P=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
EXPECTED='394db25967661b12b107062fb00976dc847817c03942dca44c4725492d4003c4'
out=E/'corrected-freeze-acceptance.json';assert not out.exists()
R={'reviewer':'/root/ra09_final_referee1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'commands':[],'approval':False,'scope':'Corrected immutable provenance only; no new Lean execution'}
try:
    f=P/'reviews/proof-freeze.json';assert sha(f)==EXPECTED
    d=json.loads(f.read_text());assert len(d['files'])==3503
    initial=json.loads((E/'original-compilation-proof-freeze.json').read_text())
    assert sha(E/'original-compilation-proof-freeze.json')=='d45703f80e35612826060bc53d7a46da7c341234f2edd8cd6269e1ed72c53c16'
    assert (P/'verification/proof-freeze-source-correction/original-proof-freeze.json').read_bytes()==(E/'original-compilation-proof-freeze.json').read_bytes()
    for rel,h in initial['files'].items():assert sha(P/rel)==h==d['files'][rel],rel
    for rel,h in d['files'].items():assert sha(P/rel)==h and (P/rel).stat().st_size==d['file_sizes'][rel],rel
    inv=json.loads((P/'verification/original-source-inventory.json').read_text())
    stmt=json.loads((P/'reviews/statement-freeze.json').read_text())
    assert set(d['source_files'])==set(d['source_git_blobs'])==set(d['source_records'])==set(inv['files'])==set(stmt['source_files'])
    assert len(d['source_records'])==17 and d['source_snapshot_directory']=='.'
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    for i,(rel,r) in enumerate(d['source_records'].items()):
        original=inv['files'][rel]
        assert all(r[k]==original[k] for k in ['commit','upstream_path','git_blob','sha256','bytes'])
        assert r['sha256']==d['source_files'][rel]==stmt['source_files'][rel]
        assert r['git_blob']==d['source_git_blobs'][rel]==stmt['source_git_blobs'][rel]
        argv=['git','show',r['commit']+':'+r['upstream_path']]
        cp=subprocess.run(argv,cwd='/tmp/nla-lean-ra20-worktree',env=env,capture_output=True)
        stdout=E/f'corrected-source-{i:02d}.stdout';stderr=E/f'corrected-source-{i:02d}.stderr'
        assert not stdout.exists() and not stderr.exists()
        stdout.write_bytes(cp.stdout);stderr.write_bytes(cp.stderr)
        R['commands'].append({'argv':argv,'cwd':'/tmp/nla-lean-ra20-worktree','exit_code':cp.returncode,
            'stdout':stdout.name,'stdout_sha256':sha(stdout),'stderr':stderr.name,'stderr_sha256':sha(stderr)})
        assert cp.returncode==0 and not cp.stderr
        assert cp.stdout==(P/rel).read_bytes() and blob(cp.stdout)==r['git_blob']
        assert len(cp.stdout)==r['bytes'] and sha(P/rel)==r['sha256']
    seal=P/'verification/proof-freeze-source-correction/EVIDENCE-MANIFEST.json'
    assert sha(seal)=='68e5e08a987f1d97a4afbe33173271be3fc6fd678529af471f2385e5c1e0c870'
    seal_data=json.loads(seal.read_text())
    for rel,r in seal_data['files'].items():assert sha(P/rel)==r['sha256'] and (P/rel).stat().st_size==r['bytes']
    current={str(p.relative_to(P)) for p in seal.parent.rglob('*') if p.is_file() and p!=seal}
    assert current==set(seal_data['files'])
    R.update(success=True,approval=True,corrected_proof_freeze_sha256=EXPECTED,
       original_proof_freeze_sha256=sha(E/'original-compilation-proof-freeze.json'),
       corrected_frozen_input_count=3503,unchanged_prior_inputs=3493,exact_source_records=17,
       source_metadata_finding='Resolved: correct distinct snapshot keys and actual per-record commits/paths/blobs; original defective metadata preserved',
       mathematical_source_changes=0,new_Lean_compilations=0,
       correction_seal_sha256=sha(seal),auditor_sha256=sha(__file__))
except BaseException:
    R.update(success=False,error=traceback.format_exc())
    out.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');raise
out.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:R[k] for k in ['success','corrected_proof_freeze_sha256','corrected_frozen_input_count','unchanged_prior_inputs','exact_source_records','source_metadata_finding']},indent=2))
