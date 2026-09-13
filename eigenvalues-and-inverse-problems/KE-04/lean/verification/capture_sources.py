#!/usr/bin/env python3
"""Retain immutable original source bytes; read-only Git, no repository mutations."""
import datetime,hashlib,json,os,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parents[1]
G=pathlib.Path('/tmp/nla-lean-ra20-worktree')
BASE='5830ed4fb06da0659414a3deb2a40ad327aca052'
PATHS=['AGENTS.md','CONTRIBUTING.md','problem_ids.json','docs/lean/README.md','docs/lean/REVIEW.md',
       'docs/lean/schema/README.md','docs/lean/schema/v0.4.schema.json','tools/lean/HARNESS.md','tools/lean/source-lock.json',
       'eigenvalues-and-inverse-problems/KE-04/README.md','eigenvalues-and-inverse-problems/KE-04/solution.md',
       'eigenvalues-and-inverse-problems/KE-04/solution.tex','references/colbrook-2026-09-11/README.md',
       'references/colbrook-2026-09-11/verification/README.md',
       'references/colbrook-2026-09-11/verification/reviews/KE-04-review.md']
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0';records={}
    items=[(BASE,rel,'verification/original-sources/'+rel) for rel in PATHS]
    items += [('fe025e14d2639cbae59f98cacf4023d83addcb89','eigenvalues-and-inverse-problems/KE-04/solution.md','verification/original-submission/solution.md'),
              ('b4123194697bdf6f8f82518c1dd7d6c40a30c2e0','eigenvalues-and-inverse-problems/KE-04/README.md','verification/original-target/README.md')]
    for rev,rel,dest in items:
        cmd=['git','-C',str(G),'show',rev+':'+rel];data=subprocess.check_output(cmd,env=env)
        blob=subprocess.check_output(['git','-C',str(G),'rev-parse',rev+':'+rel],env=env,text=True).strip()
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
        dst=P/dest;dst.parent.mkdir(parents=True,exist_ok=True);assert not dst.exists();dst.write_bytes(data)
        records[dest]={'commit':rev,'upstream_path':rel,'git_blob':blob,'sha256':sha(data),'bytes':len(data),
            'actual_command':cmd,'exit_code':0}
    def proofblock(p):
        t=p.read_text().replace('\r\n','\n').replace('\r','\n')
        return t[t.index('## Theorem '):t.index('## Scope and review notes')].strip().encode()
    current=proofblock(P/'verification/original-sources/eigenvalues-and-inverse-problems/KE-04/solution.md')
    initial=proofblock(P/'verification/original-submission/solution.md')
    assert current==initial and len(current)==2622 and sha(current)=='3ba1bd9a62a00aaf787758af6312e4787ca8d6db02b4487e8b956ce0553977a7'
    note=pathlib.Path('/tmp/nla-lean-formalization/NEXT-PROBLEM-KE-04.md').read_bytes()
    (P/'verification/coordinator-source-note.md').write_bytes(note)
    campaign=pathlib.Path('/tmp/nla-lean-formalization/CAMPAIGN.json').read_bytes()
    snapshot=json.loads(campaign)
    relevant=[]
    def walk(obj):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k=='KE-04':relevant.append(v)
                walk(v)
        elif isinstance(obj,list):
            for v in obj:walk(v)
    walk(snapshot)
    assert len(relevant)==1 and relevant[0]['agent']=='/root/ie05_statement_referee1'
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':BASE,'files':records,
        'source_count':len(records),'proof_block':{'sha256':sha(current),'bytes':len(current),'unchanged_from_initial_submission':True},
        'coordinator_note':{'sha256':sha(note),'bytes':len(note),'approval':False},
        'campaign_snapshot':{'whole_source_sha256':sha(campaign),'KE04_records':relevant,'claim':'The only current KE-04 record is the coordinator assignment for this statement-only task.'}}
    out=P/'verification/original-source-inventory.json';out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'pass':True,'sources':len(records),'proof_block_unchanged':True,'inventory_sha256':sha(out.read_bytes())}))
if __name__=='__main__':main()
