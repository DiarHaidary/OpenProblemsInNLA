"""Read-only historical membership verifier; --strict rejects later additions.

--seal is one-time reviewer packaging and must never overwrite an existing seal.
No mutating author/other-review verifier is invoked.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, re
E=Path(__file__).resolve().parent;P=E.parents[1]
M=E/'EVIDENCE-MANIFEST.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')

def entries(m):
    d=load(m)
    for name,r in d['files'].items():
        b=(P/name).read_bytes()
        assert sha(b)==r['sha256'] and len(b)==r['bytes'],name
    return set(d['files'])

def raw_commands(parent,rows):
    for r in rows:
        for key in ['stdout','stderr']:
            b=(parent/r[key]).read_bytes()
            assert sha(b)==r[key+'_sha256'],str(parent/r[key])
        assert r['exit_code']==0,r['command']
    return len(rows)

def evidence_checks(check_live_phase=False):
    assert sha((P/'DRAFT-INVENTORY.json').read_bytes())=='e82c391cc2d8d3ad1ee12e4f19266e2495e469e4b39272d31697a2e4a873a9fa'
    draft=entries(P/'DRAFT-INVENTORY.json')
    assert len(draft)==167
    ref1=P/'reviews/statement-referee-1-evidence/EVIDENCE-MANIFEST.json'
    assert sha(ref1.read_bytes())=='f3bbf77a6dcc4abf108ceb068393f6e90fdde9abff5e306f1b05dcd4c4064dd6'
    one=entries(ref1)
    assert len(one)==1467 and draft|{'DRAFT-INVENTORY.json'}<=one
    before=entries(E/'prior-boundary.json')
    assert before==one|{str(ref1.relative_to(P))} and len(before)==1468
    assert sha((P/'reviews/statement-referee-1.md').read_bytes())=='a685c8098738d02f66adf58816ad7b979f21f85c91c7881c1e90c7a1b732dcb7'
    for n,h in {'NLA/KE04/Definitions.lean':'ae1baccc0cb622f83103eff8bb4a5efe4cd9a3bae4822ccca38da29554ae9ca4','Challenge.lean':'a27de227d483072e395b6658a97cbf31296503c7fab36e5f9dbf248b2efa299e','STATEMENT-HANDOFF.md':'f46ec1cb54a9eed22dd7fc2cf640531be64b2ec86d48251d09075a64e94fa8a9'}.items():
        assert sha((P/n).read_bytes())==h,n
    actual={str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()}
    added=actual-before
    if check_live_phase:
        assert all(n=='reviews/statement-referee-2.md' or n.startswith('reviews/statement-referee-2-evidence/') for n in added)
    a=E/'attempt-o6p9csbt';r=load(a/'result.json')
    assert r['success'] and not r['errors'] and r['no_prior_private_objects'] and r['own_private_prefix_removed']
    assert not Path(r['private_prefix']).exists()
    count=raw_commands(a,r['commands'])
    assert count==45 and r['actual_successful_Lean_commands']==4 and r['kernel_assertions']==27 and r['definition_closure']==33 and r['exact_types']==24
    assert len(r['objects'])==4
    assert r['before_dependencies']==r['after_dependencies'] and len(r['before_dependencies'])==10
    assert sum(x['compiled_path_used'] is not None for x in r['before_dependencies'])==9
    for name,ident in r['inputs'].items():
        b=(a/'source'/name).read_bytes();assert sha(b)==ident['sha256'] and len(b)==ident['bytes']
        if (P/name).exists():assert b==(P/name).read_bytes()
    dl=(a/'InspectDefinitions.stdout').read_text();tl=(a/'InspectTypes.stdout').read_text()
    assert 'DEFINITION_COUNTS roots=27, closure=33' in dl
    assert tl.count('EXACT_REVIEWED_TYPE ')==24 and tl.count('TYPE_ONLY_SAFE ')==24
    assert (a/'source/InspectDefinitions.lean').read_text().count('#assert_trust kernel ')==27
    assert 'import Challenge' not in (a/'source/InspectDefinitions.lean').read_text()
    assert ':= by sorry' not in (a/'source/InspectTypes.lean').read_text()
    deps=set()
    for row in re.findall(r'dependencies=\[([^\]]*)\]',dl.split('DEFINITION_COUNTS')[0],re.S):
        deps.update(x.strip() for x in row.split(',') if x.strip())
    needed=['EuclideanSpace','Matrix.toEuclideanLin','Submodule.span','LinearIndependent','Fintype.linearCombination','Module.finrank','Matrix.transpose','Matrix.conjTranspose','Matrix.isSymmetric_toEuclideanLin_iff','LinearMap.IsSymmetric.eigenvalues','LinearMap.IsSymmetric.eigenvectorBasis','Fin.rev','Fin.revPerm','OrthonormalBasis.reindex','Matrix.isHermitian_conjTranspose_mul_mul','Polynomial.X','Polynomial.C','finrank_euclideanSpace_fin','WithLp.toLp']
    assert set(needed)<=deps,sorted(set(needed)-deps)
    source=load(E/'source-audit/result.json')
    assert source['success'] and not source['errors'] and len(source['files'])==50
    assert raw_commands(E/'source-audit',source['commands'])==10
    assert len(source['tauceti_trees_reconstructed'])==7
    for name,ident in source['files'].items():
        b=(P/name).read_bytes();assert sha(b)==ident['sha256'] and len(b)==ident['bytes']
    if check_live_phase:
        assert not (P/'Solution.lean').exists() and not (P/'formalization.yaml').exists()
    return {'success':True,'phase':'second independent statement approval only','author_files_preserved_including_manifest':168,'entire_prior_referee_boundary_preserved':1468,'own_successful_Lean_commands':4,'own_Lean_version_command':1,'dependency_identity_status_commands_before_after':40,'source_identity_search_commands':10,'raw_command_receipts':55,'actual_kernel_assertions':27,'actual_safe_definition_closure':33,'actual_exact_target_types':24,'actual_selected_definition_dependencies':needed,'original_Git_files':17,'selected_source_references':33,'TauCeti_reconstructed_trees':7,'own_objects_hash_recorded_removed':4,'own_execution_failures':0,'no_proof_or_Comparator_or_Linux_claim':True,'review_sha256':sha((P/'reviews/statement-referee-2.md').read_bytes()),'fresh_result_sha256':sha((a/'result.json').read_bytes()),'source_audit_result_sha256':sha((E/'source-audit/result.json').read_bytes())}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seal',action='store_true');ap.add_argument('--strict',action='store_true');a=ap.parse_args()
    r=evidence_checks(a.seal or a.strict)
    if a.seal:
        assert not M.exists(),'Never overwrite a seal'
        r['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        save(E/'RESULT.json',r)
        files={str(f.relative_to(P)):{'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size} for f in sorted(P.rglob('*')) if f.is_file() and f!=M}
        save(M,{'schema_version':1,'phase':'second independent KE04 statement review','scope':'Complete project as sealed, including all exact author and first-referee manifests and all reviewer evidence','reviewer':'/root/mf16_final_referee','utc':r['utc'],'excluded_paths':[str(M.relative_to(P))],'input_count':len(files),'files':files})
    d=load(M);assert d['excluded_paths']==[str(M.relative_to(P))]
    sealed=entries(M);assert len(sealed)==d['input_count']
    if a.strict:
        actual={str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()}
        assert actual==sealed|{str(M.relative_to(P))},{'extra':sorted(actual-sealed-{str(M.relative_to(P))}),'missing':sorted(sealed-actual)}
    print(json.dumps({'status':'PASS','strict_current_membership':a.strict,'sealed_files':len(sealed),'manifest_sha256':sha(M.read_bytes()),'review_sha256':r['review_sha256'],'fresh_result_sha256':r['fresh_result_sha256'],'source_result_sha256':r['source_audit_result_sha256'],'raw_command_receipts':r['raw_command_receipts']},indent=2))

if __name__=='__main__':main()
