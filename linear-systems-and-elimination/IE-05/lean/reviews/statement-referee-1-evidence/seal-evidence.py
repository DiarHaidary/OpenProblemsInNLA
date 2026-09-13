#!/usr/bin/env python3
"""Seal or verify every referee-owned artifact, excluding this one outer manifest only."""
import hashlib,json,pathlib,sys
E=pathlib.Path(__file__).resolve().parent
P=E.parents[1]
REPORT=P/'reviews/statement-referee-1.md'
OUTER=E/'outer-manifest.json'
def identity(p):
    assert p.is_file() and not p.is_symlink(),str(p)
    raw=p.read_bytes();return {'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def own_files():
    result={REPORT.relative_to(P).as_posix():identity(REPORT)}
    for q in sorted(E.rglob('*')):
        assert not q.is_symlink(),str(q)
        if q.is_file() and q!=OUTER:result[q.relative_to(P).as_posix()]=identity(q)
    return result
def verify():
    data=json.loads(OUTER.read_text())
    assert data['excluded_paths']==[OUTER.relative_to(P).as_posix()]
    assert data['files']==own_files()
    inputs=json.loads((E/'inputs.json').read_text())['files']
    inventory=json.loads((E/'input-snapshot/DRAFT-INVENTORY.json').read_text())['files']
    assert set(inputs)==set(inventory)|{'DRAFT-INVENTORY.json'} and len(inputs)==103
    for rel,meta in inputs.items():assert identity(P/rel)==meta and identity(E/'input-snapshot'/rel)==meta
    actual={q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_file() and q.relative_to(P).parts[0]!='reviews'}
    assert actual==set(inputs)
    for path in ['inputs.json','inspector-inputs.json','audit-result.json','exact-result.json',
                 'input-snapshot/DRAFT-INVENTORY.json','input-snapshot/verification/original-source-inventory.json']:
        assert (E/path).relative_to(P).as_posix() in data['files']
    r=json.loads((E/'lean-result.json').read_text())
    assert len(r['commands'])==4 and all(c['exit_code']==0 for c in r['commands'])
    assert r['private_prefix_removed'] and not pathlib.Path(r['private_prefix']).exists()
    assert json.loads((E/'audit-result.json').read_text())['pass']
    assert json.loads((E/'exact-result.json').read_text())['pass']
    assert len(json.loads((E/'audit-and-exact-commands.json').read_text()))==2
    for c in json.loads((E/'audit-and-exact-commands.json').read_text()):
        assert c['exit_code']==0 and identity(E/c['log'])['sha256']==c['log_sha256']
    assert not list(E.rglob('*.olean')) and not list(E.rglob('*.ilean'))
    print(json.dumps({'pass':True,'verdict':'APPROVE statement boundary only','outer':identity(OUTER),
        'report':identity(REPORT),'bound_files_excluding_outer':len(data['files']),
        'strict_outer_self_exclusion':True,'unchanged_draft_inputs':103,'Linux_or_theorem_claim':False},sort_keys=True))
def main():
    assert len(sys.argv)==2 and sys.argv[1] in ['create','verify']
    if sys.argv[1]=='create':
        assert not OUTER.exists()
        data={'phase':'independent statement referee 1 approval evidence','reviewer':'/root/ie05_statement_referee1',
            'source_base':'5830ed4fb06da0659414a3deb2a40ad327aca052',
            'scope':'This report and every file under statement-referee-1-evidence, including every nested manifest and source snapshot.',
            'excluded_paths':[OUTER.relative_to(P).as_posix()],
            'exclusion_rule':'Strict exact outer self-exclusion; no basename or recursive manifest exclusions.',
            'files':own_files()}
        OUTER.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    verify()
if __name__=='__main__':main()
