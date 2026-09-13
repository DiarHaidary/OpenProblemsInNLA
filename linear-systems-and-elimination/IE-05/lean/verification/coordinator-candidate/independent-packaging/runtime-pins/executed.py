"""Read-only supplemental current-Git identities for actual harness pins."""
from pathlib import Path
import hashlib,json,os,subprocess,traceback
E=Path(__file__).resolve().parent
R=Path('/tmp/nla-lean-ra20-worktree')
G=E/'runtime-pins';G.mkdir(exist_ok=False)
(G/'executed.py').write_bytes(Path(__file__).read_bytes())
base='1c467f88fbf6f6853afe5562e17b81ab421b95a6'
paths=['tools/lean/source-lock.json','tools/lean/requirements.txt','tools/lean/selftest.sh',
       'tools/lean/NOTICE.md','docs/lean/schema/LICENSE']
sha=lambda b:hashlib.sha256(b).hexdigest()
r={'current_upstream_main':base,'success':False,'files':{}}
try:
    argv=['git','-C',str(R),'cat-file','--batch']
    query=''.join(base+':'+p+'\n' for p in paths).encode()
    c=subprocess.run(argv,input=query,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                     env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    for n,b in [('stdin',query),('stdout',c.stdout),('stderr',c.stderr)]:
        (G/('git-batch.'+n)).write_bytes(b)
    r['command']={'argv':argv,'exit_code':c.returncode,'stdout_sha256':sha(c.stdout)}
    assert c.returncode==0
    raw=c.stdout;pos=0
    for p in paths:
        end=raw.index(b'\n',pos);blob,kind,size=raw[pos:end].decode().split();n=int(size)
        b=raw[end+1:end+1+n];pos=end+n+2
        assert kind=='blob' and b==(R/p).read_bytes(),p
        out=G/'current-upstream'/p;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
        r['files'][p]={'git_blob':blob,'sha256':sha(b),'bytes':n,'working_bytes_equal':True}
    assert pos==len(raw)
    lock=json.loads((R/'tools/lean/source-lock.json').read_text())
    assert lock['schema_version']==1 and lock['repository']=='https://github.com/sgstepaniants/Forsythe'
    assert lock['lean_toolchain']=='leanprover/lean4:v4.33.1'
    assert len(lock['commit'])==40
    r['actual_shared_harness_pins']={'commit':lock['commit'],'repository':lock['repository'],
       'lean_toolchain':lock['lean_toolchain'],'locked_files':len(lock['files'])}
    r['scope']='Static inspection of actual shared source lock, not execution of the Linux checker.'
    r['success']=True
except Exception:r['error']=traceback.format_exc()
(G/'result.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
raise SystemExit(0 if r['success'] else 1)
