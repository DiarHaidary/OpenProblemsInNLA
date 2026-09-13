"""Seal/verify only the exact proof freeze and this independent referee's scope."""
from pathlib import Path
import datetime, hashlib, json, sys
E=Path(__file__).resolve().parent;P=E.parents[1]
OUTER='reviews/final-referee-2-evidence/EVIDENCE-MANIFEST.json'
REPORT='reviews/final-referee-2.md'
FREEZE='reviews/proof-freeze.json'
FROZEN_SHA='72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def check():
    b=(P/FREEZE).read_bytes();assert sha(b)==FROZEN_SHA
    f=json.loads(b);assert len(f['files'])==1800
    for n,h in f['files'].items():
        q=P/n;assert q.is_file() and not q.is_symlink(),n
        b=q.read_bytes();assert sha(b)==h and len(b)==f['file_sizes'][n],n
    expected=set(f['files'])|{FREEZE,REPORT}
    expected|={str(q.relative_to(P)) for q in E.rglob('*') if q.is_file()}
    expected.discard(OUTER)
    assert not any(n.startswith('reviews/final-referee-1') for n in expected)
    files={}
    for n in sorted(expected):
        q=P/n;assert q.is_file() and not q.is_symlink(),n
        b=q.read_bytes();files[n]={'sha256':sha(b),'bytes':len(b)}
    return files
def main():
    files=check()
    if '--verify' in sys.argv:
        m=load(P/OUTER);assert m['files']==files
        assert m['exact_self_exclusion']==OUTER and m['frozen_boundary_count']==1800
        mode='VERIFIED'
    else:
        assert not (P/OUTER).exists()
        m={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/mf16_final_referee','phase':'Independent final mathematical referee 2, IE-05','verdict':'APPROVE','proof_freeze_sha256':FROZEN_SHA,'frozen_boundary_count':1800,'bound_file_count':len(files),'scope':'Exactly all 1800 frozen proof inputs, the proof-freeze itself, this reviewer report, and every file under reviews/final-referee-2-evidence; preserve all nested manifests, raw failures and source copies. Concurrent final-referee-1 additions are outside this scope.','exact_self_exclusion':OUTER,'files':files}
        (P/OUTER).write_text(json.dumps(m,indent=2)+'\n')
        assert load(P/OUTER)['files']==check();mode='SEALED AND VERIFIED'
    print(json.dumps({'status':mode,'bound_files':len(files),'outer_sha256':sha((P/OUTER).read_bytes()),'report_sha256':sha((P/REPORT).read_bytes())},indent=2))
if __name__=='__main__':main()
