from pathlib import Path
import hashlib, json, subprocess
root=Path('/tmp/nla-lean-ke04-worktree')
project=root/'eigenvalues-and-inverse-problems/KE-04/lean'
freeze=json.loads((project/'reviews/proof-freeze.json').read_text())

def blob(commit,path):
    p=subprocess.run(['git','-C',str(root),'show',f'{commit}:{path}'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout,p.stderr.decode()
def sha(x): return hashlib.sha256(x).hexdigest()
rows=[]
for sealed, rec in freeze['source_records'].items():
    retained=project/sealed
    raw=retained.read_bytes()
    rc,src,err=blob(rec['commit'],rec['upstream_path'])
    own={'sealed':sealed,'commit':rec['commit'],'upstream_path':rec['upstream_path'],'retained_sha256':sha(raw),'retained_bytes':len(raw),'record_sha256':rec['sha256'],'record_bytes':rec['bytes'],'record_match':sha(raw)==rec['sha256'] and len(raw)==rec['bytes'],'git_source_available':rc==0,'git_source_match':rc==0 and sha(src)==rec['sha256'] and len(src)==rec['bytes'],'git_blob_match':rc==0 and subprocess.run(['git','-C',str(root),'rev-parse',f'{rec["commit"]}:{rec["upstream_path"]}'],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).stdout.decode().strip()==rec['git_blob']}
    base_rc,base_src,base_err=blob('50838e3',rec['upstream_path'])
    own['base_50838e3_available']=base_rc==0
    own['base_50838e3_sha256']=sha(base_src) if base_rc==0 else None
    own['base_50838e3_equal_retained']=base_rc==0 and base_src==raw
    own['base_50838e3_equal_source_commit']=base_rc==0 and base_src==src if rc==0 else False
    rows.append(own)
print(json.dumps({'source_record_count':len(rows),'records':rows},indent=2))
