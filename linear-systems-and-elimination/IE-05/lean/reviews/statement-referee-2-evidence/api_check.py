#!/usr/bin/env python3
"""Source-bind and inspect the imported semantics and supporting pinned APIs."""
import json, pathlib
from audit import E, run, sha, write_json

packages=pathlib.Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
selected={
 'mathlib':{
  'Mathlib/Analysis/InnerProductSpace/GramSchmidtOrtho.lean':['35,78p','235,272p'],
  'Mathlib/Analysis/InnerProductSpace/PiL2.lean':['65,110p','135,163p'],
  'Mathlib/Analysis/Real/Sqrt.lean':['25,95p'],
  'Mathlib/Order/ConditionallyCompleteLattice/Basic.lean':['1,115p'],
  'Mathlib/LinearAlgebra/Matrix/Determinant/Basic.lean':[],
  'Mathlib/LinearAlgebra/Matrix/SchurComplement.lean':[],
 },
 'leancert':{'LeanCert/Tactic/Verification.lean':['635,725p']}
}
records={}
counter=0
for package,files in selected.items():
    root=packages/package
    for rel,ranges in files.items():
        p=root/rel
        expected=run(f'api-{counter}-git-oid',['git','rev-parse','HEAD:'+rel],root).decode().strip()
        actual=run(f'api-{counter}-actual-oid',['git','hash-object',rel],root).decode().strip()
        assert actual==expected
        records[package+'/'+rel]=dict(git_blob=actual,sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
        for i,span in enumerate(ranges):
            run(f'api-{counter}-excerpt-{i}',['sed','-n',span,str(p)])
        counter+=1
run('api-determinant-search',['rg','-n','linearIndependent_cols_of_det_ne_zero|theorem det_mul|theorem det_transpose|det_fromBlocks₁₁',
 str(packages/'mathlib/Mathlib/LinearAlgebra/Matrix/Determinant/Basic.lean'),
 str(packages/'mathlib/Mathlib/LinearAlgebra/Matrix/SchurComplement.lean')])
run('api-sup-search',['rg','-n','theorem le_csSup|theorem csSup_le|lemma le_csSup|lemma csSup_le',
 str(packages/'mathlib/Mathlib/Order/ConditionallyCompleteLattice/Basic.lean')])
run('api-finite-max-search',['rg','-n','theorem le_sup|theorem sup_le|lemma le_sup|lemma sup_le',
 str(packages/'mathlib/Mathlib/Data/Finset/Lattice/Fold.lean')])
write_json(E/'api-source-binding.json',dict(pass_=True,files=records,
  purpose='Actual imported semantics and supporting APIs; no generic bridge implemented or claimed.'))
print('PASS: seven relevant actual package source files bound to exact pinned Git blobs; excerpts and API searches retained.')
