"""Independently inspect the final live/new selection and external author seal."""
from pathlib import Path
import hashlib,json,sys,traceback
E=Path(__file__).resolve().parent
P=Path('/tmp/nla-lean-formalization/ie05-candidate-package/lean')
A=P.parent
Q=E/'final-selections';Q.mkdir(exist_ok=False)
(Q/'executed.py').write_bytes(Path(__file__).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def rec(p):
    b=p.read_bytes();return {'sha256':sha(b),'bytes':len(b)}
def selectsha(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':')).encode())
r={'reviewer':'/root/mf16_final_referee','success':False,'no_Lean_execution':True}
try:
    m=P/'verification/candidate-inputs.json';d=load(m)
    assert sha(m.read_bytes())=='b1259a165e924357b5474dcb9620ab316dec218e31a95665138cde4359f285e7'
    assert d['selection_sha256']==selectsha(d['files'])
    assert d['exact_self_exclusion']=='verification/candidate-inputs.json' and d['no_other_exclusions'] is True
    assert d['file_count']==len(d['files'])==2404
    sel=P/'verification/candidate-package/LIVE-SOURCE-SELECTION.json';s=load(sel)
    assert sha(sel.read_bytes())=='cea388df5779e0f0ceb27c753a4355cf1a32c68d4fc66c13512f5dd16cc758df'
    expected={str(p.relative_to(P)) for p in (P/'NLA/IE05').glob('*.lean')}|{
       'Challenge.lean','Solution.lean','lakefile.toml','lake-manifest.json','lean-toolchain','comparator.json'}
    assert set(s['files'])==expected and len(expected)==s['file_count']==18
    assert s['selection_sha256']==selectsha(s['files'])
    for n,v in s['files'].items():assert rec(P/n)==v
    before=load(P/'verification/candidate-package/PRE-PACKAGE-INPUTS.json')
    unchanged=load(P/'verification/candidate-package/ORIGINAL-UNCHANGED.json')
    assert unchanged['original_files']==2338 and unchanged['original_selection_sha256']==selectsha(before['files'])
    outer=A/'AUTHOR-HANDOFF-MANIFEST.json';o=load(outer)
    assert sha(outer.read_bytes())=='5e809e2ef80cd790ca08736ff705dab2fc5a854ee96b09a719c6bc01282777c8'
    assert o['exact_self_exclusion']=='AUTHOR-HANDOFF-MANIFEST.json'
    actual={}
    for p in sorted(A.rglob('*')):
        assert not p.is_symlink(),str(p)
        if p.is_file() and p!=outer:actual[str(p.relative_to(A))]=rec(p)
    assert actual==o['files'] and len(actual)==o['file_count']==2457
    assert rec(A/'HANDOFF.md')['sha256']=='ff176c9814b2b0130407aed9767e68ca98e2d413bfd348228c673870feb5b366'
    final=load(A/'checks/final/FINAL-RESULT.json')
    assert rec(A/'checks/final/FINAL-RESULT.json')['sha256']=='1fa64807d30b5b5ddd70670e375545391f026aefde3d3c381a66d34e1cde2736'
    # These remain author receipts; the independent main audit has its own raw
    # fresh command results, not a verdict copied from this author status.
    r.update({'success':True,'live_source_selection_files':18,
      'candidate_files':2405,'candidate_selection_sha256':d['selection_sha256'],
      'original_selection_sha256':unchanged['original_selection_sha256'],
      'author_root_manifest_selected_files':2457,'author_root_total_files':2458,
      'author_root_manifest_sha256':rec(outer)['sha256'],
      'author_final_receipt':final})
except Exception:r['error']=traceback.format_exc()
(Q/'result.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
sys.exit(0 if r['success'] else 1)
