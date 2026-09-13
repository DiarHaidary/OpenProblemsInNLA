"""Read-only audit of the fresh final helper and all retained attempts."""
from pathlib import Path
import datetime,hashlib,json,re
E=Path(__file__).resolve().parent;P=E.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def main():
    attempts=[]
    for a in sorted(E.glob('attempt-*')):
        r=load(a/'result.json')
        for n,h in r['inputs'].items():
            b=(a/'source'/n).read_bytes();assert sha(b)==h['sha256'] and len(b)==h['bytes'],(a,n)
        for c in r['commands']:
            for ext in ['stdout','stderr']:assert sha((a/c[ext]).read_bytes())==c[ext+'_sha256']
        assert not Path(r['private_prefix']).exists() and r['own_prefix_removed']
        attempts.append({'path':str(a.relative_to(P)),'result_sha256':sha((a/'result.json').read_bytes()),'success':r['success'],'Lean_commands':[{'source':c['command'][-1],'exit_code':c['exit_code']} for c in r['commands'] if '-o' in c['command']],'hashed_removed_objects':len(r['objects'])})
    successful=[a for a in attempts if a['success']];assert len(successful)==1 and len(attempts)==3
    a=P/successful[0]['path'];r=load(a/'result.json');assert r['final_inspection_counts']==['1','32','17']
    assert len(successful[0]['Lean_commands'])==5
    full=[];trusts=[];warnings={}
    for c in r['commands']:
        if '-o' not in c['command']:continue
        module=c['command'][-1];s=(a/'source'/module).read_text();log=(a/c['stdout']).read_text()
        assert c['exit_code']==0 and not (a/c['stderr']).read_bytes()
        assert not re.search(r'^.*?\.lean:\d+:\d+: error:',log,re.M)
        reports=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log)
        assertions=re.findall(r'^#assert_trust kernel (\S+)',s,re.M)
        assert len(reports)==len(assertions)
        for n,axs in reports:
            values=[x.strip() for x in axs.split(',') if x.strip()]
            assert set(values)<={'propext','Classical.choice','Quot.sound'}
            full.append({'source':module,'declaration':n,'actual_axioms':values})
        trusts.extend({'source':module,'assertion':n} for n in assertions)
        warnings[module]=re.findall(r'^.*?\.lean:\d+:\d+: warning:.*$',log,re.M)
    assert len(full)==len(trusts)==31
    assert not warnings['NLA/KE04/Nonannihilation.lean']
    log=(a/'Inspect.stdout').read_text()
    entries=re.findall(r'^ACTUAL_PROJECT (\S+): axioms=\[([^\]]*)\]; dependencies=\[([^\]]*)\]',log,re.M)
    assert len(entries)==32 and len({x[0] for x in entries})==32
    required=re.findall(r'^MATERIAL_DEPENDENCY (\S+)',log,re.M);assert len(required)==17
    actual=[{'name':n,'axioms':[x.strip() for x in axs.split(',') if x.strip()],'actual_type_and_body_constants':[x.strip() for x in ds.split(',') if x.strip()]} for n,axs,ds in entries]
    assert all(not x['name'].startswith('KE04NonannihilationExpected') for x in actual)
    source=P/'NLA/KE04/Nonannihilation.lean'
    assert source.read_bytes()==(a/'source/NLA/KE04/Nonannihilation.lean').read_bytes()
    stable=load(E/'ROLE.json')['stable_inputs']
    for n,h in stable.items():assert sha((P/n).read_bytes())==h,n
    frozen=load(P/'reviews/statement-freeze.json')['files'];assert len(frozen)==1598
    for n,h in frozen.items():assert sha((P/n).read_bytes())==h,n
    nested={}
    for name in ['verification/krylov-root-development/EVIDENCE-MANIFEST.json','verification/frames-development/EVIDENCE-MANIFEST.json']:
        m=load(P/name)
        for n,h in m['files'].items():
            b=(P/n).read_bytes();assert sha(b)==h['sha256'] and len(b)==h['bytes'],(name,n)
        nested[name]={'manifest_sha256':sha((P/name).read_bytes()),'exact_checked_membership':len(m['files'])}
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS complete bounded helper source/type/term/axiom validation','source_sha256':sha(source.read_bytes()),'attempts':attempts,'final_attempt':str(a.relative_to(P)),'successful_source_commands':5,'exact_contracts':1,'actual_project_closure':actual,'required_material_dependencies':required,'kernel_assertions':trusts,'actual_axiom_reports':full,'warnings':warnings,'stable_inputs':stable,'all1598frozen_inputs_unchanged':True,'imported_nested_manifests_checked':nested,'independent_review':False,'Linux_Comparator':False,'complete_KE04_proof':False}
    (E/'AUDIT-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'attempts':len(attempts),'source_sha256':result['source_sha256'],'fresh_commands':5,'actual_closure':len(actual),'required_dependencies':len(required),'kernel_axiom_records':len(full)},indent=2))
if __name__=='__main__':main()
