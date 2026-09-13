"""One read-only Git batch pins current packaging governance and canonical ID."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, traceback

E=Path(__file__).resolve().parent
R=Path('/tmp/nla-lean-ra20-worktree')
CURRENT='1c467f88fbf6f6853afe5562e17b81ab421b95a6'
ORIGINAL='5830ed4fb06da0659414a3deb2a40ad327aca052'
paths=['AGENTS.md','docs/lean/REVIEW.md','docs/lean/schema/README.md',
       'docs/lean/schema/v0.4.schema.json','tools/lean/HARNESS.md',
       'tools/lean/validate_manifest.py','tools/lean/harness.py','tools/lean/projects.py',
       'tools/lean/verify.sh','tools/lean/bootstrap.sh','.github/workflows/lean-verification.yml',
       'problem_ids.json','linear-systems-and-elimination/IE-05/README.md']
G=E/'governance'
G.mkdir(exist_ok=False)
(G/'executed.py').write_bytes(Path(__file__).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
result={'reviewer':'/root/mf16_final_referee','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'current_upstream_main':CURRENT,'original_mathematical_base':ORIGINAL,
        'scope':'Read-only current upstream Git blobs and comparison to local governing tool bytes. No network claim or Git mutation.',
        'files':{},'success':False}
try:
    cmd=['git','-C',str(R),'cat-file','--batch']
    query=''.join(CURRENT+':'+p+'\n' for p in paths).encode()
    c=subprocess.run(cmd,input=query,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                     env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    (G/'git-batch.stdin').write_bytes(query)
    (G/'git-batch.stdout').write_bytes(c.stdout)
    (G/'git-batch.stderr').write_bytes(c.stderr)
    result['command']={'argv':cmd,'exit_code':c.returncode,'stdin_sha256':sha(query),
                       'stdout_sha256':sha(c.stdout),'stderr_sha256':sha(c.stderr)}
    assert c.returncode==0
    raw=c.stdout;pos=0
    for p in paths:
        end=raw.index(b'\n',pos);header=raw[pos:end].decode().split()
        assert len(header)==3 and header[1]=='blob',(p,header)
        blob,kind,size=header;n=int(size);start=end+1;b=raw[start:start+n];pos=start+n+1
        assert raw[pos-1:pos]==b'\n'
        dest=G/'current-upstream'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
        live=(R/p).read_bytes()
        result['files'][p]={'git_blob':blob,'sha256':sha(b),'bytes':n,
                            'working_file_sha256':sha(live),'working_bytes_equal':b==live}
        if p not in ['problem_ids.json']:
            assert b==live,('current governance differs from working copy',p)
    assert pos==len(raw)
    canonical='linear-systems-and-elimination/IE-05/README.md'
    assert result['files'][canonical]['git_blob']=='8224c5ba49ce68198e18124245e3e736ed9ca569'
    content=(G/'current-upstream'/canonical).read_text()
    assert '**Status:** Solved' in content
    ids=json.loads((G/'current-upstream/problem_ids.json').read_text())
    assert ids['IE-05']==canonical
    result['permanent_ID_and_original_target_unchanged']=True
    result['current_canonical_status']='Solved (unchanged); packaging is no status promotion'
    result['success']=True
except Exception:
    result['error']=traceback.format_exc()
(G/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'success':result['success'],'files':len(result['files']),
                  'error':result.get('error')},indent=2))
sys.exit(0 if result['success'] else 1)
