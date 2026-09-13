#!/usr/bin/env python3
"""Independent IE-05 statement-referee evidence. No proof implementation or shared writes."""
from __future__ import annotations
import argparse, ast, datetime, hashlib, json, os, pathlib, platform, re, shutil, subprocess, tempfile, time
from fractions import Fraction

P = pathlib.Path('/tmp/nla-lean-formalization/next-ie05-statements-draft/lean').resolve()
E = P / 'reviews/statement-referee-1-evidence'
S = E / 'input-snapshot'
G = pathlib.Path('/tmp/nla-lean-ra09-worktree')
D = pathlib.Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
T = pathlib.Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
ORDER = ['batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
EXPECTED = {'STATEMENT-HANDOFF.md':'f2a38aa918a4f00a7b8f1986e80e87548827d44592ea055930051513f1aab5e0',
            'DRAFT-INVENTORY.json':'85265ec4d16e1c69570f5a7aab4bf068336fb84aa9e67dd3c5121a9c4eaa9568',
            'NLA/IE05/Definitions.lean':'aa9a18994bb8d1889af8b30290cb71846af5424436d720afaf15a54184164dfa',
            'Challenge.lean':'0ccd5424f990587b1bb7170c674cba4645d9427286c916e2e19387234ccf250e'}

def digest(data): return hashlib.sha256(data).hexdigest()
def ident(p):
    assert p.is_file() and not p.is_symlink(), str(p)
    data = p.read_bytes()
    return {'sha256':digest(data),'bytes':len(data)}
def save(name, data): (E/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(argv):
    env = os.environ.copy(); env['GIT_OPTIONAL_LOCKS']='0'
    cp = subprocess.run(['git',*argv],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    return cp.stdout
def source_set():
    return {p.relative_to(P).as_posix() for p in P.rglob('*')
            if p.is_file() and p.relative_to(P).parts[0]!='reviews'}
def no_duplicate(pairs):
    out={}
    for k,v in pairs:
        assert k not in out,k
        out[k]=v
    return out

def bind():
    E.mkdir(parents=True,exist_ok=False)
    shutil.copyfile(__file__,E/'runner.py')
    inv=json.loads((P/'DRAFT-INVENTORY.json').read_text(),object_pairs_hook=no_duplicate)
    assert len(inv['files'])==102 and inv['source_base']==BASE
    assert inv['proof_authorized'] is False and inv['is_statement_freeze'] is False
    assert source_set()==set(inv['files'])|{'DRAFT-INVENTORY.json'}
    inputs={}
    for rel in sorted(set(inv['files'])|{'DRAFT-INVENTORY.json'}):
        assert not pathlib.PurePosixPath(rel).is_absolute() and '..' not in pathlib.PurePosixPath(rel).parts
        meta=ident(P/rel)
        if rel in inv['files']: assert meta==inv['files'][rel],rel
        if rel in EXPECTED: assert meta['sha256']==EXPECTED[rel],rel
        dst=S/rel; dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(P/rel,dst);dst.chmod(0o444)
        assert ident(dst)==meta
        inputs[rel]=meta
    srcinv=json.loads((S/'verification/original-source-inventory.json').read_text(),object_pairs_hook=no_duplicate)
    assert srcinv['base']==BASE and len(srcinv['files'])==27
    bindings=[]
    for rel,meta in srcinv['files'].items():
        raw=git(['-C',str(G),'show',BASE+':'+rel])
        blob=git(['-C',str(G),'rev-parse',BASE+':'+rel]).decode().strip()
        snap=S/'verification/original-sources'/rel
        assert raw==snap.read_bytes()
        calcblob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        assert meta=={'sha256':digest(raw),'bytes':len(raw),'git_blob':blob}
        assert blob==calcblob
        bindings.append({'path':rel,**meta,'actual_commands':[
            ['git','-C',str(G),'show',BASE+':'+rel],
            ['git','-C',str(G),'rev-parse',BASE+':'+rel]],'exit_codes':[0,0],'snapshot_equals_git_blob':True})
    save('inputs.json',{'utc':utc(),'source_base':BASE,'files':inputs,
        'inventory_members':102,'including_inventory':103,'source_bindings':bindings,
        'outside_inventory_exclusion':'Only concurrent reviews/ subtree; all other files must be in draft inventory.',
        'all_snapshot_files_mode':'0444','pass':True})
    print(json.dumps({'mode':'bind','pass':True,'draft_files':103,'git_blob_bindings':27,'inputs':ident(E/'inputs.json')}))

def pin_state():
    result=[]
    for pkg in json.loads((S/'lake-manifest.json').read_text())['packages']:
        root=D/pkg['name']
        head=git(['-C',str(root),'rev-parse','HEAD']).decode().strip()
        status=git(['-c','core.fsmonitor=false','-C',str(root),'status','--porcelain','--untracked-files=no']).decode()
        assert head==pkg['rev'] and status=='',pkg['name']
        built=(root/'.lake/build/lib/lean').is_dir()
        assert built or pkg['name']=='Cli'
        result.append({'name':pkg['name'],'revision':head,'tracked_status':status,'build_objects_present':built,
            'actual_commands':[['git','-C',str(root),'rev-parse','HEAD'],
              ['git','-c','core.fsmonitor=false','-C',str(root),'status','--porcelain','--untracked-files=no']]})
    assert len(result)==10
    return result

def lean():
    definitions=(S/'NLA/IE05/Definitions.lean').read_text()
    names=re.findall(r'^(?:def|abbrev) (\w+)',definitions,re.M)
    contracts=re.findall(r'^theorem (\w+)',(S/'Challenge.lean').read_text(),re.M)
    config=json.loads((S/'comparator.json').read_text())
    assert config['theorem_names']==['NLA.IE05.'+x for x in contracts] and len(contracts)==17
    assert config['definition_names']==[] and set(config['permitted_axioms'])=={'propext','Classical.choice','Quot.sound'}
    assert not re.search(r'\b(sorry|admit|native_decide|ofReduceBool)\b',definitions)
    assert not re.search(r'^\s*(axiom|opaque|unsafe|theorem|lemma)\b',definitions,re.M)
    inspectors={
      'RefereeDefinitions.lean':'import NLA.IE05.Definitions\nimport LeanCert.Tactic.Verification\nset_option leancert.trust "kernel"\n'+
        '\n'.join(f'#print NLA.IE05.{n}\n#assert_trust kernel NLA.IE05.{n}\n#print axioms NLA.IE05.{n}' for n in names)+'\n',
      'RefereeContracts.lean':'import Challenge\nset_option pp.universes true\n'+
        '\n'.join(f'#check NLA.IE05.{n}\n#print axioms NLA.IE05.{n}' for n in contracts)+'\n'}
    for rel,content in inspectors.items():
        q=S/rel;assert not q.exists();q.write_text(content);q.chmod(0o444)
    save('inspector-inputs.json',{'files':{rel:ident(S/rel) for rel in inspectors},
        'definition_count':len(names),'definition_names':names,'contract_count':len(contracts),'contract_names':contracts})
    prefix=pathlib.Path(tempfile.mkdtemp(prefix='nla-ie05-referee1-objects-',dir='/tmp'))
    env=os.environ.copy(); env['GIT_OPTIONAL_LOCKS']='0'
    env['LEAN_PATH']=os.pathsep.join([str(prefix),*[str(D/x/'.lake/build/lib/lean') for x in ORDER],str(T/'lib/lean')])
    env['PATH']=str(T/'bin')+os.pathsep+env.get('PATH','')
    result={'phase':'independent statement referee 1 source elaboration','utc':utc(),'platform':platform.platform(),
        'lean_binary':ident(T/'bin/lean'),'lean_version':subprocess.check_output([str(T/'bin/lean'),'--version'],text=True).strip(),
        'private_prefix':str(prefix),'lean_path':env['LEAN_PATH'],'commands':[],
        'mathematics_proved':False,'linux_comparator_run':False,'Cli_note':'Tooling only; no build objects, excluded from LEAN_PATH.'}
    try:
        result['pins_before']=pin_state()
        for rel in ['NLA/IE05/Definitions.lean','Challenge.lean',*inspectors]:
            out=prefix/pathlib.Path(rel).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
            argv=[str(T/'bin/lean'),'-o',str(out),'-i',str(out.with_suffix('.ilean')),rel]
            start=time.monotonic()
            cp=subprocess.run(argv,cwd=S,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=60)
            log=pathlib.Path(rel).stem+'.log';(E/log).write_text(cp.stdout)
            result['commands'].append({'argv':argv,'cwd':str(S),'elapsed_seconds':time.monotonic()-start,
                'exit_code':cp.returncode,'log':log,'log_identity':ident(E/log),'source_identity':ident(S/rel)})
            print(json.dumps(result['commands'][-1]),flush=True)
            assert cp.returncode==0,rel
        result['pins_after']=pin_state()
        assert result['pins_before']==result['pins_after']
        assert (E/'Definitions.log').read_text()==''
        assert (E/'Challenge.log').read_text().count('declaration uses `sorry`')==17
        trust=(E/'RefereeDefinitions.log').read_text()
        reports=re.findall(r"'NLA\.IE05\.([^']+)' depends on axioms: \[([^]]*)\]",trust)
        allowed={'propext','Classical.choice','Quot.sound'}
        assert len(reports)==len(names),(len(reports),len(names))
        assert {n for n,_ in reports}==set(names)
        assert all({x.strip() for x in a.split(',') if x.strip()}<=allowed for n,a in reports)
        assert 'warning:' not in trust and 'error:' not in trust
        typelog=(E/'RefereeContracts.log').read_text()
        assert typelog.count('sorryAx')==17 and 'error:' not in typelog and 'warning:' not in typelog
        result['definition_axiom_reports']={n:[x.strip() for x in a.split(',') if x.strip()] for n,a in reports}
        result['definition_kernel_assertions']=len(names)
        result['challenge_reference_placeholders']=17
        result['all_input_sources_unchanged']=all(ident(P/r)==meta and ident(S/r)==meta for r,meta in json.loads((E/'inputs.json').read_text())['files'].items())
        assert result['all_input_sources_unchanged']
        result['pass']=True
    finally:
        result['generated_objects_before_removal']={str(p.relative_to(prefix)):ident(p) for p in prefix.rglob('*') if p.is_file()}
        assert prefix.parent==pathlib.Path('/tmp') and prefix.name.startswith('nla-ie05-referee1-objects-')
        shutil.rmtree(prefix);result['private_prefix_removed']=not prefix.exists()
        save('lean-result.json',result)
    print(json.dumps({'mode':'lean','pass':result.get('pass',False),'definitions':len(names),'contracts':len(contracts),'result':ident(E/'lean-result.json')}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['bind','lean'])
    args=parser.parse_args();globals()[args.mode]()
