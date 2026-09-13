#!/usr/bin/env python3
"""Seal only this referee's report/evidence; exact sole self-exclusion."""
import hashlib, json, pathlib, sys

E=pathlib.Path(__file__).resolve().parent
P=E.parent.parent
report=P/'reviews/statement-referee-2.md'
seal=E/'EVIDENCE-SEAL.json'
def digest(p):
    b=p.read_bytes()
    return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def scope_files():
    return {str(p.relative_to(P)):p for p in [report]+sorted(E.rglob('*')) if p.is_file() and p!=seal}
for line in (E/'commands.jsonl').read_text().splitlines():
    rec=json.loads(line)
    for channel in ['stdout','stderr']:
        assert digest(E/'logs'/(rec['label']+'.'+channel))['sha256']==rec[channel+'_sha256']
if '--verify' in sys.argv:
    data=json.loads(seal.read_text())
    assert data['self_exclusion']==[str(seal.relative_to(P))]
    paths=scope_files()
    assert set(data['files'])==set(paths)
    for rel,p in paths.items():
        assert not p.is_symlink() and data['files'][rel]==digest(p),rel
    print(json.dumps({'pass':True,'file_count':len(paths),'report':digest(report),'evidence_seal':digest(seal)},indent=2))
else:
    assert not seal.exists()
    assert json.loads((E/'final-checks.json').read_text())['pass_']
    data={'phase':'independent statement-referee-2 evidence seal; not statement freeze',
          'scope':['reviews/statement-referee-2.md','reviews/statement-referee-2-evidence/**'],
          'self_exclusion':[str(seal.relative_to(P))],
          'other_referee_directories_in_scope':False,
          'files':{rel:digest(p) for rel,p in scope_files().items()}}
    seal.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print('Evidence seal written; verify with python3 -B reviews/statement-referee-2-evidence/seal.py --verify')
