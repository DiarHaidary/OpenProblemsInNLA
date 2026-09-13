"""Exact bounded helper seal; preserves every nested manifest and failed attempt."""
from pathlib import Path
import datetime,hashlib,json,sys
E=Path(__file__).resolve().parent;P=E.parents[1]
OUTER='verification/nonannihilation-development/EVIDENCE-MANIFEST.json'
SOURCE='NLA/KE04/Nonannihilation.lean'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def inventory():
    role=load(E/'ROLE.json');f=load(P/'reviews/statement-freeze.json')
    assert len(f['files'])==1598
    for n,h in f['files'].items():assert sha((P/n).read_bytes())==h,n
    for n,h in role['stable_inputs'].items():assert sha((P/n).read_bytes())==h,n
    names=set(f['files'])|set(role['stable_inputs'])|{SOURCE}
    for manifest in ['verification/krylov-root-development/EVIDENCE-MANIFEST.json','verification/frames-development/EVIDENCE-MANIFEST.json']:
        m=load(P/manifest)
        for n,h in m['files'].items():
            b=(P/n).read_bytes();assert sha(b)==h['sha256'] and len(b)==h['bytes'],(manifest,n)
        names|=set(m['files'])
    names|={str(q.relative_to(P)) for q in E.rglob('*') if q.is_file()}
    names.discard(OUTER)
    files={}
    for n in sorted(names):
        q=P/n;assert q.is_file() and not q.is_symlink(),n
        b=q.read_bytes();files[n]={'sha256':sha(b),'bytes':len(b)}
    return files
def main():
    files=inventory()
    if '--verify' in sys.argv:
        m=load(P/OUTER);assert m['files']==files and m['exact_self_exclusion']==OUTER
        status='VERIFIED'
    else:
        assert not (P/OUTER).exists()
        m={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Complete owned Nonannihilation helper/development evidence, all1598 unchanged statement inputs, explicitly unchanged stable imported boundaries and every exact input named by the two imported helper seals; concurrent unrelated proof additions are outside this scope.','bound_file_count':len(files),'exact_self_exclusion':OUTER,'inventory_rule':'Retain all actual attempted sources, commands, errors, audit records and nested manifests; exclude only this exact outer file itself.','independent_review':False,'complete_problem_verified':False,'files':files}
        (P/OUTER).write_text(json.dumps(m,indent=2)+'\n')
        assert load(P/OUTER)['files']==inventory();status='SEALED AND VERIFIED'
    print(json.dumps({'status':status,'files':len(files),'source_sha256':sha((P/SOURCE).read_bytes()),'handoff_sha256':sha((E/'HANDOFF.json').read_bytes()),'outer_sha256':sha((P/OUTER).read_bytes())},indent=2))
if __name__=='__main__':main()
