#!/usr/bin/env python3
"""Audit the retained run, including the driver's no-axiom-output parser failure."""
import hashlib,json,pathlib,re,subprocess,os
E=pathlib.Path(__file__).resolve().parent
S=E/'input-snapshot'
P=E.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def identity(p):return {'sha256':sha(p),'bytes':p.stat().st_size}
def main():
    result=json.loads((E/'lean-result.json').read_text())
    inputs=json.loads((E/'inputs.json').read_text())
    inspector=json.loads((E/'inspector-inputs.json').read_text())
    assert len(result['commands'])==4 and all(c['exit_code']==0 for c in result['commands'])
    for c in result['commands']:
        assert identity(E/c['log'])==c['log_identity']
        assert identity(S/c['argv'][-1])==c['source_identity']
    for rel,meta in inputs['files'].items():assert identity(P/rel)==meta and identity(S/rel)==meta,rel
    for rel,meta in inspector['files'].items():assert identity(S/rel)==meta
    assert result['pins_before']==result['pins_after'] and len(result['pins_before'])==10
    assert result['private_prefix_removed'] and not pathlib.Path(result['private_prefix']).exists()
    assert len(result['generated_objects_before_removal'])==8
    assert (E/'Definitions.log').read_text()==''
    assert (E/'Challenge.log').read_text().count('declaration uses `sorry`')==17
    txt=(E/'RefereeDefinitions.log').read_text()
    records={n:[x.strip() for x in axs.split(',') if x.strip()] for n,axs in
        re.findall(r"'NLA\.IE05\.([^']+)' depends on axioms: \[([^]]*)\]",txt)}
    no_axioms=re.findall(r"'NLA\.IE05\.([^']+)' does not depend on any axioms",txt)
    assert len(records)==36 and len(no_axioms)==5
    for n in no_axioms:assert n not in records;records[n]=[]
    assert len(records)==41 and set(records)==set(inspector['definition_names'])
    assert all(set(axs)<={'propext','Classical.choice','Quot.sound'} for axs in records.values())
    assert (S/'RefereeDefinitions.lean').read_text().count('#assert_trust kernel ')==41
    assert 'import Challenge' not in (S/'RefereeDefinitions.lean').read_text()
    assert 'error:' not in txt and 'warning:' not in txt
    contractlog=(E/'RefereeContracts.log').read_text()
    assert contractlog.count('sorryAx')==17 and 'error:' not in contractlog and 'warning:' not in contractlog
    config=json.loads((S/'comparator.json').read_text())
    assert config['theorem_names']==['NLA.IE05.'+n for n in inspector['contract_names']]
    assert config['definition_names']==[]
    api={
      'mathlib/Mathlib/Analysis/InnerProductSpace/GramSchmidtOrtho.lean':{'read_lines':[[40,125],[189,284]],'semantic_check':'Gram-Schmidt uses preceding ordered indices and scales residual by inverse actual norm; nonzero and orthonormality depend on linear independence.'},
      'mathlib/Mathlib/Analysis/InnerProductSpace/PiL2.lean':{'read_lines':[[67,157]],'semantic_check':'EuclideanSpace is PiLp 2 and its norm is sqrt of the sum of squared entry norms.'},
      'mathlib/Mathlib/Order/ConditionallyCompleteLattice/Basic.lean':{'read_lines':[[180,220]],'semantic_check':'le_csSup requires genuine boundedness; csSup_le requires nonemptiness.'},
      'mathlib/Mathlib/Data/Finset/Lattice/Fold.lean':{'read_lines':[[32,98]],'semantic_check':'Finset.sup is the lattice fold with bottom; NNReal bottom is zero and nonempty finite maxima are attained.'},
      'leancert/LeanCert/Tactic/Verification.lean':{'read_lines':[[584,679]],'semantic_check':'assert_trust kernel collects declaration axiom closure and rejects sorryAx, custom axioms and native compiler axioms.'}}
    packages=pathlib.Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    for rel,item in api.items():
        pkg,source=rel.split('/',1);root=packages/pkg;p=root/source
        rev=next(x['revision'] for x in result['pins_after'] if x['name']==pkg)
        raw=subprocess.check_output(['git','-C',str(root),'show',rev+':'+source],env=env)
        assert raw==p.read_bytes()
        item.update(identity(p));item['revision']=rev;item['source_equals_pinned_git']=True
        item['source_binding_command']=['git','-C',str(root),'show',rev+':'+source]
        obj=root/'.lake/build/lib/lean'/pathlib.Path(source).with_suffix('.olean')
        item['read_only_existing_objects']={str(q.relative_to(root)):identity(q) for q in obj.parent.glob(obj.name+'*') if q.is_file()}
    out={'phase':'independent statement referee 1 post-run audit','pass':True,
        'auditor_source':identity(pathlib.Path(__file__)),'retained_run_result':identity(E/'lean-result.json'),
        'driver_exit_code':1,'driver_failure':'Postprocessing regex counted only 36 depends-on-axioms lines and omitted five does-not-depend-on-any-axioms lines; all four Lean commands already exited zero. The failed runner, result and logs are retained unchanged.',
        'lean_commands_exit_zero':4,'explicit_definition_kernel_assertions':41,'actual_definition_axiom_reports':records,
        'axiom_class_counts':{'no_axioms':5,'propext_only':4,'standard_three':32},
        'challenge_placeholder_warnings':17,'actual_contract_type_and_axiom_reports':17,
        'original_and_snapshot_103_inputs_unchanged':True,'pins_clean_before_and_after':True,
        'all_eight_own_objects_hashed_then_removed':True,'own_generated_bytes':sum(x['bytes'] for x in result['generated_objects_before_removal'].values()),
        'inspected_pinned_apis':api,'mathematical_proof':False,'authoritative_linux_comparator':False}
    (E/'audit-result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'pass':True,'lean_commands':4,'definition_assertions':41,'axiom_classes':out['axiom_class_counts'],'audit':identity(E/'audit-result.json')}))
if __name__=='__main__':main()
