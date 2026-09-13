from pathlib import Path
import hashlib, importlib.util, json, re

OWN=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review',OWN/'review.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
out=OWN/'primary-001';out.mkdir(exist_ok=False)
(out/'executed-primary-sources.py').write_bytes(Path(__file__).read_bytes())
records={}
def record(p,origin):
    p=Path(p); records[str(p)]={'sha256':r.sha(p),'bytes':p.stat().st_size,'origin':origin}
    return p.read_text()
standards=Path('/tmp/nla-lean-formalization/standards')
tree=json.loads((standards/'TauCetiProject_TauCetiReview-tree.json').read_text())
assert tree['sha']=='afb424eda89e8ac96d9eb69f6a88972055a4cd1b' and not tree['truncated']
byname={x['path']:x for x in tree['tree']}
rubrics=['_common','correctness','scope','proof-quality','reuse','generality','api-design','naming','placement','documentation','attribution']
for name in rubrics:
    p=standards/'sources/TauCetiProject/TauCetiReview/rubrics'/(name+'.md')
    content=p.read_bytes(); blob=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
    assert blob==byname['rubrics/'+name+'.md']['sha']
    record(p,'TauCetiReview '+tree['sha']+' blob '+blob)
record(r.ROOT/'verification/original-sources/docs/lean/REVIEW.md','NLA original base '+json.loads((r.ROOT/'verification/original-source-inventory.json').read_text())['base'])

examples=[
  ('schiffer',Path('/tmp/nla-lean-formalization/leancert-examples/Schiffer'),'2938e277969c329caf154e48a3d8823f3635c7f1', ['Schiffer/Challenge.lean']),
  ('forsythe',Path('/Users/georgestepaniants/Research/Forsythe'),'8d1b0c0545a77b40245e84705aa7d273e6c81e62',['lean-proof/Challenge.lean','lean-proof/ProofProject/CheckedMultivariateBound.lean'])]
for label,repo,base,paths in examples:
    raw=r.run(out,label+'-git-blobs',['git','-C',repo,'cat-file','--batch'],stdin=''.join(base+':'+p+'\n' for p in paths).encode())
    offset=0
    for rel in paths:
        end=raw.index(b'\n',offset); head=raw[offset:end].decode().split();offset=end+1
        assert len(head)==3 and head[1]=='blob',head
        size=int(head[2]); content=raw[offset:offset+size];offset+=size+1
        snapshot=out/'examples'/label/rel;snapshot.parent.mkdir(parents=True,exist_ok=True);snapshot.write_bytes(content)
        record(snapshot,label+' Git '+base+':'+rel+' blob '+head[0])
        if label=='schiffer': assert (repo/rel).read_bytes()==content
        else:
            old=Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean/verification/api-evidence-complete/forsythe')/rel
            assert old.read_bytes()==content

math=r.PACKAGES/'mathlib'
queries={
 'Mathlib/Analysis/InnerProductSpace/GramSchmidtOrtho.lean':r'gramSchmidtNormed|gramSchmidt_ne_zero|gramSchmidt_inv_triangular|gramSchmidt_def',
 'Mathlib/Analysis/InnerProductSpace/PiL2.lean':r'inner_apply|EuclideanSpace',
 'Mathlib/LinearAlgebra/Matrix/NonsingularInverse.lean':r'mulVec_injective_iff_isUnit|mul_nonsing_inv|isUnit_iff_isUnit_det|invertibleOfIsUnitDet|linearIndependent_cols_of_det_ne_zero',
 'Mathlib/LinearAlgebra/Matrix/Block.lean':r'blockTriangular_inv_of_blockTriangular|det_of_isUpperTriangular|det_of_isLowerTriangular',
 'Mathlib/LinearAlgebra/Matrix/Determinant/Basic.lean':r'det_mul|det_transpose|linearIndependent_cols_of_det_ne_zero',
 'Mathlib/Data/List/MinMax.lean':r'def argmax|def argAux|index_of_argmax|le_of_mem_argmax',
 'Mathlib/Data/List/FinRange.lean':r'idxOf_finRange|mem_finRange',
 'Mathlib/Data/Finset/Max.lean':r'exists_max_image',
 'Mathlib/Order/ConditionallyCompleteLattice/Basic.lean':r'theorem le_csSup|theorem csSup_le ',
 'Mathlib/Analysis/Real/Sqrt.lean':r'lemma sqrt_pos|theorem sqrt_pos|lemma sq_sqrt|theorem sq_sqrt',
}
for i,(rel,query) in enumerate(queries.items()):
    p=math/rel; record(p,'Mathlib 0df444a360eaa60ab8c11dca51a86af692955474')
    # Context surrounds each actual primary API declaration; output is retained.
    r.run(out,f'api-{i:02d}',['rg','-n','-A','8','-B','2',query,p])
for rel in ['Lean/Declaration.lean','Lean/Util/CollectAxioms.lean','Lean/Util/FoldConsts.lean','Lean/Elab/Tactic/Decide.lean']:
    record(r.LEANROOT/'src/lean'/rel,'Lean v4.33.1')
record(r.PACKAGES/'leancert/LeanCert/Tactic/Verification.lean','LeanCert 621a43d7cf21f87872392a01e874f2f1dbddc926')
# These searches record where existing API supports the specific new bridges.
r.run(out,'reuse-search',['rg','-n','gramSchmidtNormed|starProjection_singleton|mulVec_injective_iff_isUnit|blockTriangular_inv_of_blockTriangular|exists_max_image|index_of_argmax',math/'Mathlib/Analysis/InnerProductSpace',math/'Mathlib/LinearAlgebra/Matrix',math/'Mathlib/Data/Finset',math/'Mathlib/Data/List'])
r.save(out/'source-records.json',records)
print('Primary sources recorded: common + 10 actual pinned rubrics, original NLA review policy, 3 Git-pinned example files, and relevant current pinned Mathlib/Lean/LeanCert APIs')
