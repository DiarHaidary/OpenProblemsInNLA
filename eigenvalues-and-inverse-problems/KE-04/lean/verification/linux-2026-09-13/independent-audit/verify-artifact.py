from pathlib import Path
import hashlib,json,subprocess
root=Path('/tmp/nla-lean-ke04-worktree'); project='eigenvalues-and-inverse-problems/KE-04/lean'; project_path=root/project; commit='40b0bf52e73e776e7769f0f12dbbda7cd9fff183'
art=Path('/tmp/nla-ke04-operational-review/linux-artifact')
result=json.loads(next((art/'verify-20260913T132545Z-4211').glob('result.json')).read_text())
candidate_config=json.loads((project_path/'comparator.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
# list tree blobs for exact project
out=subprocess.check_output(['git','-C',str(root),'ls-tree','-r','-z',commit,'--',project])
entries=[]
for e in out.split(b'\0'):
 if not e: continue
 meta,name=e.split(b'\t',1); mode,kind,obj=meta.decode().split(); rel=name.decode()[len(project)+1:]
 entries.append((rel,obj))
proc=subprocess.Popen(['git','-C',str(root),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
requests=''.join(obj+'\n' for _,obj in entries).encode(); outb,_=proc.communicate(requests)
expected={}; pos=0
for rel,obj in entries:
 header_end=outb.index(b'\n',pos); header=outb[pos:header_end].decode(); pos=header_end+1
 size=int(header.split()[2]); data=outb[pos:pos+size]; pos+=size+1
 expected[rel]=sha(data)
actual=result['input_sha256']
missing=sorted(set(expected)-set(actual)); extra=sorted(set(actual)-set(expected)); mismatch=sorted(k for k in expected if actual.get(k)!=expected[k])
print(json.dumps({'repository_commit':result.get('repository_commit'),'project':result.get('project'),'commit_match':result.get('repository_commit')==commit,'project_match':result.get('project')==project,'tree_file_count':len(expected),'artifact_file_count':len(actual),'missing':missing[:20],'extra':extra[:20],'mismatch':mismatch[:20],'all_input_hashes_match':not missing and not extra and not mismatch,'config_match':result.get('config')==candidate_config,'artifact_theorem_count':len(result.get('config',{}).get('theorem_names',[])),'source_lock_result':result.get('source_lock_sha256'),'tool_source_lock':result.get('tool_receipt',{}).get('source_lock_sha256'),'source_lock_match':result.get('source_lock_sha256')==result.get('tool_receipt',{}).get('source_lock_sha256'),'result':result.get('result')},indent=2))
