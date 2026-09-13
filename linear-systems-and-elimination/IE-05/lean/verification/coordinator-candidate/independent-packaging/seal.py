"""Seal once, or rehash the complete independent packaging-review scope.

No candidate/original/author-package writes. In --verify mode this is entirely
read-only. The sole excluded file is evidence/EVIDENCE-MANIFEST.json itself.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,sys

E=Path(__file__).resolve().parent
ROOTS={
 'evidence':E,
 'author_package':Path('/tmp/nla-lean-formalization/ie05-candidate-package').resolve(),
 'original':Path('/tmp/nla-lean-formalization/next-ie05-statements-draft/lean').resolve(),
}
OUTER=E/'EVIDENCE-MANIFEST.json'
SELF='evidence/EVIDENCE-MANIFEST.json'
P=ROOTS['author_package']/'lean'
sha=lambda b:hashlib.sha256(b).hexdigest()
def unique(pairs):
    r={}
    for k,v in pairs:
        assert k not in r,('duplicate key',k)
        r[k]=v
    return r
def load(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def record(p):
    b=p.read_bytes();return {'sha256':sha(b),'bytes':len(b)}
def save(p,r):p.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
def inventory():
    files={}
    counts={}
    for prefix,root in ROOTS.items():
        count=0
        for p in sorted(root.rglob('*')):
            assert not p.is_symlink(),str(p)
            if not p.is_file():continue
            key=prefix+'/'+str(p.relative_to(root))
            assert str(PurePosixPath(key))==key
            if key==SELF:continue
            files[key]=record(p);count+=1
        counts[prefix]=count
    return files,counts
def assertions():
    latest=load(E/'LATEST.json');assert latest['success'] is True
    audit=load(E/latest['attempt']/'result.json')
    assert record(E/latest['attempt']/'result.json')['sha256']==latest['result_sha256']
    assert audit['success'] is True and len(audit['commands'])==5
    assert all(c['exit_code']==0 for c in audit['commands'])
    assert audit['actual_complete_candidate_inventory_count']==2405
    assert audit['historical_inventory_count']==29
    assert sum(i['entries'] for i in audit['historical_inventories'].values())==14280
    assert audit['candidate_and_original_unchanged'] is True
    for p in ['governance/result.json','runtime-pins/result.json','final-selections/result.json']:
        assert load(E/p)['success'] is True
    assert record(P/'verification/candidate-inputs.json')['sha256']=='b1259a165e924357b5474dcb9620ab316dec218e31a95665138cde4359f285e7'
    assert record(P/'verification/candidate-package/HANDOFF.md')['sha256']=='c0f1b96cabf0b00d065272260d94e143464ec4d6422f4677e308783397025f58'
    assert record(ROOTS['author_package']/'AUTHOR-HANDOFF-MANIFEST.json')['sha256']=='5e809e2ef80cd790ca08736ff705dab2fc5a854ee96b09a719c6bc01282777c8'
    return latest,audit
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args()
    latest,audit=assertions()
    if args.verify:
        m=load(OUTER)
        assert m['exact_self_exclusion']==SELF and m['no_other_exclusions'] is True
        assert m['roots']=={k:str(v) for k,v in ROOTS.items()}
        actual,counts=inventory()
        assert actual==m['files'],'Exact scoped file membership or bytes changed'
        assert counts==m['root_file_counts'] and len(actual)==m['file_count']
        assert SELF not in m['files']
        print(json.dumps({'result':'PASS','scope':'Complete independent packaging review seal; no Lean/Linux run',
            'files':len(actual),'root_counts':counts,'manifest_sha256':record(OUTER)['sha256']},indent=2))
        return
    assert not OUTER.exists(),'A sealed review is immutable; use --verify'
    assert not (E/'HANDOFF.json').exists(),'Do not overwrite prior handoff'
    handoff={'reviewer':'OpenAI Codex /root/mf16_final_referee',
      'role':'Independent candidate-packaging review, separate from prior sealed final mathematical review2',
      'verdict':'APPROVE exact candidate for coordinator installation and subsequent Linux gate',
      'report':{'path':'REPORT.md',**record(E/'REPORT.md')},
      'candidate':str(P),'candidate_manifest':{'path':'verification/candidate-inputs.json',**record(P/'verification/candidate-inputs.json')},
      'candidate_handoff':{'path':'verification/candidate-package/HANDOFF.md',**record(P/'verification/candidate-package/HANDOFF.md')},
      'actual_independent_audit':latest,'fresh_audit_commands':5,
      'candidate_files':2405,'original_draft_files':2338,'historical_inventories':29,
      'historical_member_checks':14280,'original_Git_snapshots':27,
      'current_governance_commit':'1c467f88fbf6f6853afe5562e17b81ab421b95a6',
      'original_mathematical_commit':'5830ed4fb06da0659414a3deb2a40ad327aca052',
      'actual_schema':'PASS 17 declarations','actual_harness_static_validate_project':'PASS',
      'independent_scope':'Read-only concrete package/provenance/metadata integrity review; no candidate authorship or proof changes',
      'new_mathematical_approval':False,'new_Lean_build':False,'actual_Linux_Comparator':'pending',
      'canonical_status':'Solved unchanged','whole_problem_verified_claim':False,
      'commit_push_PR_or_publication':False,'own_outer':'EVIDENCE-MANIFEST.json',
      'verification_command':'python3 seal.py --verify'}
    save(E/'HANDOFF.json',handoff)
    files,counts=inventory()
    assert counts['author_package']==2458 and counts['original']==2338
    m={'reviewer':'OpenAI Codex /root/mf16_final_referee','verdict':'APPROVE exact candidate packaging only',
       'roots':{k:str(v) for k,v in ROOTS.items()},
       'scope':'Complete independent evidence, complete author package (including every candidate input and author raw attempt), and complete accepted original draft',
       'path_convention':'Root-key / exact root-relative POSIX path',
       'exact_self_exclusion':SELF,'no_other_exclusions':True,
       'root_file_counts':counts,'file_count':len(files),'files':files}
    save(OUTER,m)
    # Recheck after sealing without creating any post-seal output artifact.
    actual,again=inventory();assert actual==files and again==counts
    print(json.dumps({'result':'SEALED','report_sha256':record(E/'REPORT.md')['sha256'],
      'handoff_sha256':record(E/'HANDOFF.json')['sha256'],'outer_sha256':record(OUTER)['sha256'],
      'file_count':len(files),'root_counts':counts},indent=2))
if __name__=='__main__':main()
