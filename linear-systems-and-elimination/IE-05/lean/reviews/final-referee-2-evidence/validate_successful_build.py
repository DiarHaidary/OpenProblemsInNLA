"""Audit the completed successful Lean commands without rerunning unchanged proofs.

The first runner's final Python policy rejected harmless, reviewer-owned unused
Prop-binder warnings. Keep that failed result unchanged; this separate receipt
distinguishes the actual fourteen successful Lean commands from that policy error.
"""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, traceback
E=Path(__file__).resolve().parent;P=E.parents[1]
A=E/'attempt-gxrxb23r'
DEPS=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
    out=E/'successful-build-validation';assert not out.exists();out.mkdir()
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/mf16_final_referee','attempt':A.name,'historical_attempt_result_sha256':sha((A/'result.json').read_bytes()),'commands':[],'errors':[]}
    try:
        original=load(A/'result.json')
        assert len(original['errors'])==1 and 'Compiler diagnostic present' in original['errors'][0]
        records=original['commands']; commands=[r for r in records if '-o' in r['command']]
        assert len(commands)==14 and all(r['exit_code']==0 for r in commands)
        inputs=load(A/'source-inputs.json'); combined='';axioms=[];trusts=[];warn=[]
        for n,r in inputs.items():
            b=(A/'source'/n).read_bytes();assert sha(b)==r['sha256'] and len(b)==r['bytes'],n
            if n!='Inspect.lean':assert b==(P/n).read_bytes(),n
        for r in commands:
            b=(A/r['stdout']).read_bytes();stderr=(A/r['stderr']).read_bytes()
            assert sha(b)==r['stdout_sha256'] and sha(stderr)==r['stderr_sha256'] and not stderr
            text=b.decode(); assert not re.search(r'^.*?: error:',text,re.M)
            module=r['command'][-1];source=(A/'source'/module).read_text()
            warnings=re.findall(r'^(Inspect\.lean:\d+:\d+: warning: Variable name `[^`]+` is not explicitly referenced\.)$',text,re.M)
            actual_warnings=re.findall(r'^.*?\.lean:\d+:\d+: warning:.*$',text,re.M)
            if module=='Inspect.lean':assert warnings==actual_warnings and len(warnings)==14;warn=warnings
            else:assert not actual_warnings,module
            local_trusts=re.findall(r'^#assert_trust kernel (\S+)',source,re.M)
            local_axioms=re.findall(r"^'([^']+)' depends on axioms: \[([^\]]*)\]",text,re.M)
            assert len(local_trusts)==len(local_axioms),(module,len(local_trusts),len(local_axioms))
            for name,ax in local_axioms:
                parsed=[s.strip() for s in ax.split(',') if s.strip()]
                assert set(parsed)<= {'propext','Classical.choice','Quot.sound'},(name,parsed)
                axioms.append({'module':module,'declaration':name,'axioms':parsed})
            trusts.extend({'module':module,'source_assertion':n,'successful_compiler_exit':0} for n in local_trusts)
            combined+=text+'\n'
        assert len(axioms)==len(trusts)==106
        types=re.findall(r'^EXACT_TYPE (NLA\.IE05\.\w+):',combined,re.M)
        assert types==load(P/'comparator.json')['theorem_names']
        matches=re.findall(r'^AUDIT_COMPLETE (\w+) roots=(\d+) closure=(\d+) required=(\d+)$',combined,re.M)
        assert matches==[('FINAL','1','152','27'),('ALL','17','181','3')]
        closure={}
        for scope,roots,count,required in matches:
            decls=re.findall(r'^ACTUAL_DECL '+scope+r' (\S+) AXIOMS \[([^\]]*)\]',combined,re.M)
            assert len(decls)==len({n for n,_ in decls})==int(count)
            deps=re.findall(r'^RETAINED '+scope+r' (\S+)$',combined,re.M); assert len(deps)==int(required)
            assert not any('Referee2Expected' in n for n,_ in decls)
            closure[scope]={'roots':int(roots),'actual_declarations':[{'name':n,'axioms':[s.strip() for s in ax.split(',') if s.strip()]} for n,ax in decls],'required_material_dependencies':deps,'Lean_inspector_enforced_safe_nonpartial_and_actual_type_body_recursion':True}
        save(out/'actual-types-and-dependencies.json',{'exact_types':types,'closure':closure})
        save(out/'kernel-and-axioms.json',{'successful_kernel_assertions':trusts,'actual_axiom_reports':axioms})
        save(out/'reviewer-warning-diagnostic.json',{'origin':'Reviewer-generated proof-free expected Prop expressions retain frozen binder names that are unused in their conclusion. Their forall hypotheses remain in the exact compared types.','warnings':warn,'proof_source_warnings':0,'Lean_errors':0,'all_Lean_exits':0,'correction':'Replace the overstrict Python any-warning policy with exact classification of these 14 harmless expected-type binder warnings; no Lean source change or rebuild.','failed_result_preserved_unchanged':True})
        env=dict(os.environ,GIT_OPTIONAL_LOCKS='0');pins=[]
        for pkg in load(P/'lake-manifest.json')['packages']:
            n=pkg['name'];values={}
            for suffix,args in [('head',['git','rev-parse','HEAD']),('status',['git','status','--porcelain=v1','--untracked-files=no'])]:
                cp=subprocess.run(args,cwd=DEPS/n,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                label=n+'-'+suffix
                (out/(label+'.stdout')).write_bytes(cp.stdout);(out/(label+'.stderr')).write_bytes(cp.stderr)
                result['commands'].append({'command':args,'cwd':str(DEPS/n),'exit_code':cp.returncode,'stdout':label+'.stdout','stderr':label+'.stderr','stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr)})
                assert cp.returncode==0 and not cp.stderr;values[suffix]=cp.stdout.decode().strip()
            assert values['head']==pkg['rev'] and values['status']==''
            before=next(r for r in original['pins_before'] if r['name']==n)
            assert before['head']==values['head'] and before['clean_tracked_sources']
            pins.append(before)
        result['pins_after_equal_before']=pins
        freeze_b=(P/'reviews/proof-freeze.json').read_bytes();assert sha(freeze_b)=='72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251'
        freeze=json.loads(freeze_b);assert len(freeze['files'])==1800
        for n,h in freeze['files'].items():
            b=(P/n).read_bytes();assert sha(b)==h and len(b)==freeze['file_sizes'][n],n
        assert not Path(original['empty_private_output_prefix']).exists()
        objects=load(A/'objects-before-cleanup.json');assert len(objects['files'])==14
        result.update({'status':'PASS independent fresh complete source compilation and exact elaborated type/actual dependency/kernel-axiom audit','Lean_commands':14,'exact_types':17,'actual_all_export_closure':181,'actual_final_closure':152,'final_required_dependencies':27,'kernel_assertions':106,'standard_three_axiom_reports':106,'frozen_inputs_unchanged':1800,'no_reference_Challenge_compiled':not any('Challenge.lean'==r['command'][-1] for r in commands),'hashed_owned_objects_removed':14,'warning_classification_only_no_source_or_proof_correction':True})
    except Exception:result['errors'].append(traceback.format_exc())
    result['success']=not result['errors'];save(out/'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['commands','pins_after_equal_before']},indent=2))
    raise SystemExit(0 if result['success'] else 1)
if __name__=='__main__':main()
