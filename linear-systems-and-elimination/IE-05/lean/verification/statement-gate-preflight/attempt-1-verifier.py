#!/usr/bin/env python3
"""Portable, read-only IE05 coordinator-helper preflight. JSON is written to stdout.

No existing driver is executed. No Lean compile, write, Git mutation, package
build, cache copy, download, proof, freeze, or gate authorization is performed.
Pass --project, --source-repo, --packages and --lean to relocate the inputs.
The caller may retain stdout/stderr in a NEW directory of its own choosing.
"""
import argparse, ast, collections, hashlib, json, os, pathlib, re, subprocess, sys, time, traceback
from fractions import Fraction as F

BASE='5830ed4fb06da0659414a3deb2a40ad327aca052'
HANDOFF='f2a38aa918a4f00a7b8f1986e80e87548827d44592ea055930051513f1aab5e0'
INVENTORY='85265ec4d16e1c69570f5a7aab4bf068336fb84aa9e67dd3c5121a9c4eaa9568'
R1='reviews/statement-referee-1-evidence'
R2='reviews/statement-referee-2-evidence'
REPORTS={
 'reviews/statement-referee-1.md':'13aa3e9b73c1fde94d2b45c4ec327a44b0e4470c685fa58478526a122cb25c10',
 'reviews/statement-referee-2.md':'d5b204c4bcc727e52c52c60855e5a393debdba5bc5a2d5567c1c715e5de18730'}
SEALS=[(R1,'outer-manifest.json','26f09fc4bff996802f57dea898de457d4105d0454e1700288da96f578222561b','excluded_paths',123),
       (R2,'EVIDENCE-SEAL.json','f21212db9edcfba43dccbf92bb1eb75fea56b63fc464fa636abb756aa81c7a52','self_exclusion',490)]
ALLOW={'propext','Classical.choice','Quot.sound'}
OUT={'phase':'coordinator-helper mechanical preflight, not third mathematical review',
     'proof_authorized':False,'is_statement_freeze':False,'new_Lean_compile':False,
     'new_mathematical_approval':False,'stage':'initializing','actual_commands':[],
     'internal_checks':[],'limitations':[
       'Successful historical Lean exits and source/log bindings are audited; no new Lean compile or Comparator run occurs.',
       'Removed private objects cannot be rehashed now. Their historical hashes, matching shared object identities, cleanup receipts, and current absence are checked.',
       'Original source-lock remote harness artifacts and structural Schiffer/Forsythe example identities are source-bound historical metadata, not an assertion of a current harness or external-example run.']}

def require(ok,msg):
    if not ok:raise AssertionError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        require(k not in d,'duplicate JSON key '+k);d[k]=v
    return d
def read(p):
    require(p.is_file() and not p.is_symlink(),'missing/symlink file '+str(p));return p.read_bytes()
def ident(p):
    b=read(p);return {'sha256':sha(b),'bytes':len(b)}
def load(p):return json.loads(read(p),object_pairs_hook=unique)
def join(base,rel):
    r=pathlib.PurePosixPath(rel)
    require(not r.is_absolute() and '..' not in r.parts,'unsafe relative path '+rel)
    p=base.joinpath(*r.parts)
    for q in [p,*p.parents]:
        if q==base.parent:break
        require(not q.is_symlink(),'symlink component '+str(q))
    return p
def match(p,meta):
    got=ident(p)
    require(all(got[k]==meta[k] for k in ['sha256','bytes']),'identity mismatch '+str(p))
    return got
def full_tree(root):
    out={}
    for q in sorted(root.rglob('*')):
        require(not q.is_symlink(),'symlink in scope '+str(q))
        if q.is_file():out[q.relative_to(root).as_posix()]=q
    return out
def filemap(base,m):
    for rel,meta in m.items():match(join(base,rel),meta)
def check(name,**data):OUT['internal_checks'].append({'check':name,'pass':True,**data})
def command(argv,cwd):
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
    t=time.monotonic();r=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    OUT['actual_commands'].append({'argv':list(map(str,argv)),'cwd':str(cwd),'exit_code':r.returncode,
        'elapsed_seconds':time.monotonic()-t,'stdout':r.stdout.decode('utf-8'),
        'stderr':r.stderr.decode('utf-8'),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)})
    require(r.returncode==0,'actual read-only command failed '+str(argv));return r.stdout
def git(root,*args):return command(['git','-c','core.fsmonitor=false',*args],root)
def axioms(txt):
    found=re.findall(r"^'NLA\.IE05\.(\w+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)",txt,re.M|re.S)
    require(len(found)==len({n for n,a in found}),'duplicate axiom report')
    return {n:[v.strip() for v in a.split(',') if v.strip()] for n,a in found}
def cleanlog(txt):require('warning:' not in txt and 'error:' not in txt and 'error(' not in txt,'unclean inspector log')
def pin_records(rows,pins):
    require(len(rows)==10 and len({r['name'] for r in rows})==10,'pin count')
    for row in rows:
        require(row.get('revision',row.get('rev'))==pins[row['name']],'pin revision')
        require(row.get('tracked_status','')=='' and row.get('tracked_status_clean',True) and row.get('tracked_clean',True),'dirty historical pin')
def metadata_hash(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':')).encode())

def main(args):
    P=args.project.resolve();G=args.source_repo.resolve();PK=args.packages.resolve()
    OUT['project']=str(P);OUT['source_repo']=str(G);OUT['source_base']=BASE
    OUT['verifier_identity']=ident(pathlib.Path(__file__).resolve())
    OUT['stage']='sealed referee closures'
    sealed={}
    for rel,expected in REPORTS.items():require(ident(P/rel)['sha256']==expected,'report hash '+rel)
    for root,name,h,exclusion,count in SEALS:
        sealpath=root+'/'+name
        require(ident(P/sealpath)['sha256']==h,'seal hash '+sealpath)
        data=load(P/sealpath)
        require(data[exclusion]==[sealpath],'outer self-exclusion '+sealpath)
        actual={root+'/'+rel:ident(p) for rel,p in full_tree(P/root).items() if root+'/'+rel!=sealpath}
        report='reviews/statement-referee-'+('1' if root==R1 else '2')+'.md'
        actual[report]=ident(P/report)
        require(data['files']==actual and len(actual)==count,'complete outer membership '+root)
        sealed.update(actual);sealed[sealpath]=ident(P/sealpath)
        check('complete outer seal',path=sealpath,members=count,exact_sole_self_exclusion=True)

    OUT['stage']='103 inputs and exact complete tree'
    inv=load(P/'DRAFT-INVENTORY.json')
    require(ident(P/'DRAFT-INVENTORY.json')['sha256']==INVENTORY,'inventory anchor')
    require(ident(P/'STATEMENT-HANDOFF.md')['sha256']==HANDOFF,'handoff anchor')
    require(len(inv['files'])==102 and inv['source_base']==BASE and not inv['proof_authorized'] and not inv['is_statement_freeze'],'draft metadata')
    inputs=dict(inv['files']);inputs['DRAFT-INVENTORY.json']=ident(P/'DRAFT-INVENTORY.json')
    filemap(P,inputs)
    snap1=P/R1/'input-snapshot';snap2=P/R2/'inputs'
    b1=load(P/R1/'inputs.json');b2=load(P/R2/'input-binding.json')
    require(b1['files']==b2['files']==inputs,'referee complete input maps')
    for snap,extras in [(snap1,{'RefereeDefinitions.lean','RefereeContracts.lean'}),(snap2,{'Referee2Inspect.lean'})]:
        filemap(snap,inputs)
        require(set(full_tree(snap))==set(inputs)|extras,'snapshot exact membership '+str(snap))
    allinputs={**inputs,**sealed}
    actual={rel:ident(p) for rel,p in full_tree(P).items() if not rel.startswith('verification/statement-gate-preflight/')}
    require(actual==allinputs and len(actual)==718,'unexpected original project inputs outside preflight')
    require(not any((P/x).exists() for x in ['Solution.lean','NLA/IE05/Proof.lean','formalization.yaml','.lake']),'unexpected implementation artifact')
    OUT['proposed_input_binding']={'purpose':'PROPOSED complete reviewed input binding for coordinator; NOT a freeze',
       'source_base':BASE,'proof_authorized':False,'is_statement_freeze':False,
       'draft_inputs':103,'referee_1_closure_including_outer':124,'referee_2_closure_including_outer':491,
       'files':allinputs,'preflight_outputs_are_separate_evidence':True}
    check('all draft and review inputs unchanged',draft_count=103,full_reviewed_input_count=718)

    OUT['stage']='27 original Git bindings'
    src=load(P/'verification/original-source-inventory.json')
    require(src['base']==BASE and len(src['files'])==27,'source inventory')
    require(git(G,'rev-parse',BASE+'^{commit}').decode().strip()==BASE,'source base commit')
    originals={}
    records1={x['path']:x for x in b1['source_bindings']}
    records2=load(P/R2/'git-source-binding.json')
    require(len(records1)==27 and records2['base']==BASE,'reviewer Git binding maps')
    for rel,meta in src['files'].items():
        oid=git(G,'rev-parse',BASE+':'+rel).decode().strip()
        raw=git(G,'cat-file','blob',oid)
        require(meta=={'git_blob':oid,'sha256':sha(raw),'bytes':len(raw)},'Git blob identity '+rel)
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid,'independent Git blob SHA1 '+rel)
        for root in [P,snap1,snap2]:require(read(root/'verification/original-sources'/rel)==raw,'original snapshot '+rel)
        require(records1[rel]['exit_codes']==[0,0] and records1[rel]['snapshot_equals_git_blob'],'referee1 Git commands '+rel)
        for row in [records1[rel],records2['files'][rel]]:
            require(all(row[k]==meta[k] for k in meta),'reviewer source identity '+rel)
        originals[rel]=meta
    require(load(P/'verification/original-sources/problem_ids.json')['IE-05']=='linear-systems-and-elimination/IE-05/README.md','permanent registry')
    check('original sources independently rebound to Git',count=27)

    OUT['stage']='definitions, signatures and actual inspectors'
    definitions=read(P/'NLA/IE05/Definitions.lean').decode();challenge=read(P/'Challenge.lean').decode()
    names=re.findall(r'^(?:def|abbrev)\s+(\w+)\b',definitions,re.M)
    thms=re.findall(r'^theorem\s+(\w+)\b',challenge,re.M)
    require(len(names)==len(set(names))==41 and len(thms)==len(set(thms))==17,'41/17 declaration lists')
    config=load(P/'comparator.json')
    require(config['theorem_names']==['NLA.IE05.'+n for n in thms] and config['definition_names']==[] and set(config['permitted_axioms'])==ALLOW,'comparator exact configuration')
    require(challenge.count(':= by sorry')==17,'reference holes')
    no_comments=re.sub(r'/\-.*?\-/','',definitions,flags=re.S)
    require(not re.search(r'\b(sorry|admit|axiom|unsafe|extern|implemented_by|native_decide)\b',no_comments),'definition trust escape')
    i1=read(snap1/'RefereeDefinitions.lean').decode();i2=read(snap2/'Referee2Inspect.lean').decode()
    ci=read(snap1/'RefereeContracts.lean').decode()
    for txt in [i1,i2]:
        require(re.findall(r'^import (.*)$',txt,re.M)==['NLA.IE05.Definitions','LeanCert.Tactic.Verification'],'definition-only imports')
        require('set_option leancert.trust "kernel"' in txt,'explicit kernel trust')
        for prefix in ['#assert_trust kernel ','#print axioms ','#print ']:
            require(re.findall(r'^'+re.escape(prefix)+r'NLA\.IE05\.(\w+)$',txt,re.M)==names,'exact inspector coverage '+prefix)
        require(not re.search(r'^(theorem|lemma|def|axiom)\b',txt,re.M),'inspector added declaration')
    expected_ci='import Challenge\nset_option pp.universes true\n'+'\n'.join('#check NLA.IE05.'+n+'\n#print axioms NLA.IE05.'+n for n in thms)+'\n'
    require(ci==expected_ci,'exact contract inspector')
    inspector_meta=load(P/R1/'inspector-inputs.json');filemap(snap1,inspector_meta['files'])
    require(inspector_meta['definition_names']==names and inspector_meta['contract_names']==thms,'inspector manifest coverage')
    logs=[read(P/R1/'RefereeDefinitions.log').decode(),read(P/R2/'logs/fresh-inspector.stdout').decode(),read(P/R2/'logs/attempt-2-fresh-inspector.stdout').decode()]
    ax=[]
    for txt in logs:
        cleanlog(txt);a=axioms(txt);require(set(a)==set(names),'actual axiom count')
        require(all(set(v)<=ALLOW for v in a.values()),'forbidden actual definition axiom');ax.append(a)
    require(ax[0]==ax[1]==ax[2],'independent axiom maps differ')
    counts=collections.Counter('none' if not v else 'propext' if v==['propext'] else 'standard_three' for v in ax[0].values())
    require(dict(counts)=={'none':5,'propext':4,'standard_three':32},'axiom distributions')
    type_log=read(P/R1/'RefereeContracts.log').decode();cleanlog(type_log)
    type_blocks=re.findall(r"^(NLA\.IE05\.(\w+)\b.*?)\n'NLA\.IE05\.\2' depends on axioms: \[([^]]*)\]",type_log,re.M|re.S)
    require([n for txt,n,a in type_blocks]==thms and all('sorryAx' in a for txt,n,a in type_blocks),'all 17 actual elaborated types')
    source_statements=re.findall(r'^theorem\s+(\w+)\b(.*?)\s*:= by sorry',challenge,re.M|re.S)
    require([n for n,t in source_statements]==thms,'all 17 source types')
    OUT['configured_types']={n:{'source_signature':('theorem '+n+t).strip(),
       'source_signature_sha256':sha(('theorem '+n+t).strip().encode()),
       'actual_elaborated_type':type_blocks[i][0],
       'actual_elaborated_type_sha256':sha(type_blocks[i][0].encode())} for i,(n,t) in enumerate(source_statements)}
    OUT['actual_definition_axioms']=ax[0]
    check('exact statements, inspector sources and actual logs',definitions=41,contracts=17,axiom_counts=dict(counts),types_from_retained_fresh_compile=True)

    OUT['stage']='actual historical commands, pins and failures'
    deps=load(P/'lake-manifest.json');pins={x['name']:x['rev'] for x in deps['packages']};require(len(pins)==10,'ten manifest pins')
    r1=load(P/R1/'lean-result.json');a1=load(P/R1/'audit-result.json');f1=load(P/R1/'initial-driver-status.json')
    require(len(r1['commands'])==4 and 'pass' not in r1 and f1['commands'][1]['exit_code']==1,'referee1 failure must remain failure')
    require(f1['runner_sha256']==ident(P/R1/'runner.py')['sha256'],'referee1 failed driver snapshot')
    require(f1['commands'][0]['inputs_json_sha256']==ident(P/R1/'inputs.json')['sha256'],'referee1 initial bind receipt')
    require(f1['commands'][1]['retained_lean_result_sha256']==ident(P/R1/'lean-result.json')['sha256'],'referee1 failure result binding')
    runner1=read(P/R1/'runner.py').decode();auditor1=read(P/R1/'audit-results.py').decode()
    require("reports=re.findall(r\"'NLA\\.IE05\\.([^']+)' depends on axioms:" in runner1,'referee1 failed parser inspected')
    require('does not depend on any axioms' in auditor1 and a1['driver_exit_code']==1 and a1['pass'],'referee1 replayed audit distinction')
    match(P/R1/'audit-results.py',a1['auditor_source']);match(P/R1/'lean-result.json',a1['retained_run_result'])
    require(a1['actual_definition_axiom_reports']==ax[0],'referee1 corrected audit maps')
    for c in r1['commands']:
        require(c['exit_code']==0 and c['elapsed_seconds']>0,'referee1 historical Lean exit')
        match(P/R1/c['log'],c['log_identity']);match(snap1/c['argv'][-1],c['source_identity'])
        require(c['cwd'].endswith('/'+R1+'/input-snapshot'),'referee1 source working directory')
        require(c['argv'][2].startswith(r1['private_prefix']+'/'),'referee1 own output prefix')
    for c in load(P/R1/'audit-and-exact-commands.json'):
        require(c['exit_code']==0 and ident(P/R1/c['log'])['sha256']==c['log_sha256'],'referee1 post-check receipt')
    require(r1['pins_before']==r1['pins_after'],'referee1 stable pins');pin_records(r1['pins_before'],pins)
    require(r1['private_prefix_removed'] and not pathlib.Path(r1['private_prefix']).exists(),'referee1 own prefix remains')
    require(len(r1['generated_objects_before_removal'])==8 and sum(x['bytes'] for x in r1['generated_objects_before_removal'].values())==1030698,'referee1 object receipt')
    require(not r1['linux_comparator_run'] and not r1['mathematics_proved'],'referee1 scope')
    r2s=[load(P/R2/'elaboration-result.json'),load(P/R2/'elaboration-result-2.json')]
    commands2=[json.loads(line,object_pairs_hook=unique) for line in read(P/R2/'commands.jsonl').decode().splitlines()]
    require(len({c['label'] for c in commands2})==len(commands2),'referee2 duplicate command label')
    c2map={c['label']:c for c in commands2}
    for c in commands2:
        require(c['exit_code']==0,'referee2 actual subprocess failure')
        for channel in ['stdout','stderr']:
            require(ident(P/R2/'logs'/(c['label']+'.'+channel))['sha256']==c[channel+'_sha256'],'referee2 raw log '+c['label'])
    require(not r2s[0]['pass_'] and r2s[1]['pass_'],'referee2 original failure and successful fresh rerun')
    require(r2s[0]['private_prefix']!=r2s[1]['private_prefix'],'referee2 separate new prefix')
    for index,r in enumerate(r2s):
        require(r['prefix_initially_empty'] and r['own_objects_hashed_then_removed'] and r['private_prefix_absent_after'] and not pathlib.Path(r['private_prefix']).exists(),'referee2 own objects cleanup')
        require(r['inspector_sha256']==ident(snap2/'Referee2Inspect.lean')['sha256'],'referee2 inspector source')
        require(r['package_preflight']==r['package_postflight'],'referee2 stable pins');pin_records(r['package_preflight'],pins)
        require(len(r['objects'])==3 and sum(x['bytes'] for x in r['objects'].values())==986352,'referee2 object receipts')
        require(r['comparison_configuration']==config and not r['proofs_established'] and not r['package_build_or_download'] and not r['imported_package_objects_copied'],'referee2 scope')
        prefix='' if index==0 else 'attempt-2-'
        for label,source in [('fresh-definitions','NLA/IE05/Definitions.lean'),('fresh-challenge','Challenge.lean'),('fresh-inspector','Referee2Inspect.lean')]:
            c=c2map[prefix+label]
            require(c['argv'][-1]==source and c['cwd'].endswith('/'+R2+'/inputs') and c['argv'][2].startswith(r['private_prefix']+'/'),'referee2 actual fresh command/source')
            require(c['exit_code']==0 and c['elapsed_seconds']>0,'referee2 Lean exit')
        require(r['explicit_environment']['LEAN_PATH'].split(os.pathsep)[0]==r['private_prefix'],'referee2 private module lookup')
    require(r2s[1]['axiom_reports']==ax[0],'referee2 fresh map')
    require("warning: declaration uses 'sorry'" in read(P/R2/'attempt-1-elaborate.py').decode() and 'warning: declaration uses `sorry`' in read(P/R2/'elaborate.py').decode(),'referee2 failed and corrected driver sources')
    require(read(P/R2/'attempt-1-terminal.log').decode().endswith('AssertionError\n'),'referee2 failure transcript')
    warnings_expected=['Challenge.lean:'+str(i)+':8: warning: declaration uses `sorry`' for i,line in enumerate(challenge.splitlines(),1) if line.startswith('theorem ')]
    for q in [P/R1/'Challenge.log',P/R2/'logs/fresh-challenge.stdout',P/R2/'logs/attempt-2-fresh-challenge.stdout']:
        require(read(q).decode().splitlines()==warnings_expected,'exact warning source locations '+str(q))
    for q in [P/R1/'Definitions.log',P/R2/'logs/fresh-definitions.stdout',P/R2/'logs/attempt-2-fresh-definitions.stdout']:
        require(read(q)==b'','fresh Definitions warning')
    for r,objs in [(r2s[0],r2s[0]['objects']),(r2s[1],r2s[1]['objects'])]:
        for key in ['NLA/IE05/Definitions.olean','Challenge.olean']:
            require(objs[key]==r1['generated_objects_before_removal'][key],'fresh shared module object receipts differ')
    OUT['historical_execution_scope']={'referee1':{'fresh_Lean_exits':[0]*4,'outer_driver_exit':1,'resolution':'separate retained-log audit, no additional Lean execution'},
       'referee2':{'first_fresh_Lean_exits':[0]*3,'first_outer_postcheck_exit':1,'second_fresh_Lean_exits':[0]*3,'second_outer_driver_exit':0,'resolution':'new empty-prefix Lean rerun after own parser correction'},
       'new_preflight_Lean_compiles':0,'historical_referee2_commands_checked':len(commands2)}
    check('fresh execution receipts and failure distinctions',referee1_Lean_commands=4,referee2_Lean_commands=6,referee1_replayed_audit=True)

    OUT['stage']='current read-only pins and imported API records'
    currentpins={}
    for name,rev in pins.items():
        root=PK/name
        require(git(root,'rev-parse','HEAD').decode().strip()==rev,'current package pin '+name)
        require(git(root,'status','--porcelain=v1','--untracked-files=no')==b'','current package dirty '+name)
        objects=(root/'.lake/build/lib/lean').is_dir()
        require(objects==(name!='Cli'),'Cli/current imported objects distinction')
        currentpins[name]={'revision':rev,'source_clean':True,'object_directory_present':objects}
    leanid=ident(args.lean)
    require(leanid==r1['lean_binary'] and leanid['sha256']==r2s[1]['lean_binary_sha256'],'actual Lean binary identity')
    version=command([str(args.lean),'--version'],P).decode().strip()
    require(version==r1['lean_version']==r2s[1]['version'],'exact Lean version')
    for path in [r1['lean_path'],*(r['explicit_environment']['LEAN_PATH'] for r in r2s)]:
        require('/packages/Cli/' not in path,'Cli erroneously imported by independent reviewer')
        imported=re.findall(r'/packages/([^/]+)/\.lake/build/lib/lean',path)
        require(set(imported)==set(pins)-{'Cli'} and len(imported)==9,'independent LEAN_PATH nine packages')
    apis=load(P/'verification/statement-development/api-and-example-identities.json')
    apiids={}
    for pkg in ['mathlib','leancert']:
        require(apis[pkg]['revision']==pins[pkg],'API pin')
        for rel,meta in apis[pkg]['files'].items():
            p=PK/pkg/rel;match(p,meta)
            require(git(PK/pkg,'rev-parse',pins[pkg]+':'+rel).decode().strip()==meta['git_blob'],'API Git identity '+rel)
            require(hashlib.sha1(b'blob '+str(p.stat().st_size).encode()+b'\0'+read(p)).hexdigest()==meta['git_blob'],'API blob bytes '+rel)
            apiids[pkg+'/'+rel]=meta
    imported_objects={}
    for rel,meta in a1['inspected_pinned_apis'].items():
        pkg,source=rel.split('/',1);match(PK/pkg/source,meta)
        require(meta['source_equals_pinned_git'] and meta['revision']==pins[pkg],'referee1 API record')
        expected={}
        for obj,oid in meta['read_only_existing_objects'].items():match(PK/pkg/obj,oid);expected[obj]=oid
        stem=PK/pkg/'.lake/build/lib/lean'/pathlib.Path(source).with_suffix('.olean')
        actual_obj={q.relative_to(PK/pkg).as_posix():ident(q) for q in stem.parent.glob(stem.name+'*') if q.is_file()}
        require(actual_obj==expected,'complete imported object identity set '+rel)
        imported_objects[rel]=expected
    for rel,meta in load(P/R2/'api-source-binding.json')['files'].items():
        pkg,source=rel.split('/',1);match(PK/pkg/source,meta)
        require(meta['git_blob']==apiids[rel]['git_blob'],'referee2 API record')
    match(PK/'mathlib/Mathlib/Data/Finset/Lattice/Fold.lean',load(P/R2/'finite-max-source-binding.json'))
    OUT['current_dependencies']=currentpins;OUT['current_imported_object_identities']=imported_objects
    check('current exact read-only dependency and API identities',packages=10,source_API_files=len(apiids),imported_object_files=sum(map(len,imported_objects.values())))

    OUT['stage']='all nested manifests and historical author attempts'
    manifests=[]
    for root in [P,snap1,snap2]:
        # Each nested original inventory and Lake manifest is checked at its own
        # location, including historical source snapshots. Their hypotheses and
        # older mathematical versions are not silently changed to current ones.
        nested_inv=load(root/'DRAFT-INVENTORY.json');filemap(root,nested_inv['files'])
        sinv=load(root/'verification/original-source-inventory.json')
        for rel,meta in sinv['files'].items():match(root/'verification/original-sources'/rel,meta)
        dev=root/'verification/statement-development'
        latest=load(dev/'latest.json');validation=load(dev/'validation.json')
        require(ident(dev/latest['attempt']/'result.json')['sha256']==latest['result_sha256']==validation['latest_result_sha256'],'nested latest pointer')
        require(validation['statement_approvals']==0 and not validation['proof_implementation_started'] and not validation['linux_comparator_ran'],'historical author scope')
        attempts=[]
        for attempt in sorted(dev.glob('attempt-*')):
            if (attempt/'result.json').exists():
                r=load(attempt/'result.json');filemap(attempt/'source',r['inputs'])
                require(set(full_tree(attempt/'source'))==set(r['inputs']),'historical attempt source completeness')
                require(r['pins_before']==r['pins_after'],'author pin preservation');pin_records(r['pins_before'],pins)
                require(r['source_unchanged'] and r['own_prefix_removed'] and not pathlib.Path(r['prefix']).exists(),'author object cleanup')
                require(not r['mathematics_proved'] and not r['authoritative_linux_comparator'],'author scope')
                for c in r['commands']:
                    require(ident(attempt/c['log'])['sha256']==c['log_sha256'],'author command raw log')
                    require(c['argv'][-1]==c['source'] and c['argv'][2].startswith(r['prefix']+'/'),'author command source/output')
                require(r['pass']==all(c['exit_code']==0 for c in r['commands']),'author pass/exit consistency')
                attempts.append({'attempt':attempt.name,'pass':r['pass'],'exits':[c['exit_code'] for c in r['commands']]})
            else:
                failure=load(attempt/'preflight-failure.json')
                require(not failure['mathematical_compile_started'],'preflight failure scope')
                require(ident(attempt/'source/verification/statement-development/check_statements.py')['sha256']==failure['script_sha256'],'failed preflight driver binding')
                require(all(not pathlib.Path(x['path']).exists() for x in failure['cleanup']),'failed preflight cleanup')
                attempts.append({'attempt':attempt.name,'pass':False,'exits':[]})
        require(len(attempts)==5 and sum(x['pass'] for x in attempts)==1,'five retained author attempts')
        for rel in ['reconstruction.json','reconstruction-before-namespace-correction.json']:
            r=load(dev/rel)
            require(r['script_sha256']==ident(dev/'reconstruct.py')['sha256'],'author reconstruction script')
            require(any(meta['sha256']==r['source_sha256'] for path,meta in inputs.items() if path.endswith('Definitions.lean')),'retained author arithmetic source version')
        require(ident(dev/'reconstruction.json')['sha256']==validation['reconstruction_sha256'],'author reconstruction pointer')
        for p in root.rglob('lake-manifest.json'):
            if root==P and p.parts[:len((P/'reviews').parts)]==(P/'reviews').parts:continue
            if root==P and 'statement-gate-preflight' in p.parts:continue
            require(load(p)==deps,'every nested Lake manifest agrees')
        manifests.append({'snapshot_root':str(root.relative_to(P)) or '.', 'draft_members':102,'original_sources':27,'historical_attempts':attempts})
    # Exhaustive JSON enumeration is part of the seal, including manifests whose
    # remote payloads are policy/example metadata rather than local proof inputs.
    OUT['nested_json_documents']={}
    for rel,meta in allinputs.items():
        if not rel.endswith('.json'):continue
        data=load(P/rel)
        OUT['nested_json_documents'][rel]={'identity':meta,'top_level_type':type(data).__name__,
            'top_level_keys':list(data) if isinstance(data,dict) else None,
            'covered_by_complete_seal_or_103_input_inventory':True}
    lock=load(P/'verification/original-sources/tools/lean/source-lock.json')
    require(lock['commit']=='8d1b0c0545a77b40245e84705aa7d273e6c81e62' and len(lock['files'])==58,'original remote source lock')
    require(len({x['destination'] for x in lock['files']})==58,'duplicate remote source-lock destination')
    for x in lock['files']:
        require(re.fullmatch('[0-9a-f]{64}',x['sha256']) and x['bytes']>0,'source-lock digest shape')
        join(P,x['source']);join(P,x['destination'])
    OUT['nested_manifest_checks']=manifests
    check('all nested input/source/attempt manifests and JSON parse',nested_JSON_documents=len(OUT['nested_json_documents']),snapshot_roots=3,remote_policy_source_lock_entries=58)

    OUT['stage']='numerical receipt agreement and unchanged closure'
    e1=load(P/R1/'exact-result.json');e2=load(P/R2/'numerical-result.json')
    match(snap1/'NLA/IE05/Definitions.lean',e1['source']);match(P/R1/'exact-referee-check.py',e1['script'])
    match(snap1/'verification/original-sources/linear-systems-and-elimination/IE-05/solution.md',e1['canonical_source'])
    require(e1['pass'] and e1['no_Lean_proof_or_certificate'] and e2['pass_'] and e2['not_a_Lean_theorem'],'numerical diagnostics scope')
    require(e1['exact_positive_squared_gap']==e2['exact_gap']=='117335164/1147041','exact gap receipts')
    require(e2['actual_Lean_arrays_sha256']==ident(P/'NLA/IE05/Definitions.lean')['sha256'],'referee2 numeric source binding')
    for rel,meta in e2['source_array_bindings'].items():match(P/'verification/original-sources'/rel,meta)
    for name1,name2,keys,count in [('witness_64_input_bounds','witness_input_certificates',['i','j','lhs','rhs'],64),
                                 ('candidate_204_active_bounds','candidate_active_certificates',['k','i','j','lhs','rhs'],204)]:
        a=e1[name1];b=e2[name2]
        require(len(a)==len(b)==count,'numerical receipt count')
        require([{k:r[k] for k in keys} for r in a]==[{k:r[k] for k in keys} for r in b],'independent numerical receipt agreement')
        require(all(r['lhs']<=r['rhs'] for r in a),'stored one-sided bound')
    for label,boolean in [('candidate','false'),('witness','true')]:
        case=e1['matrix_cases'][label]
        require(case['D']==e2['cases'][boolean]['positive_D'],'stored D vectors')
        require([case['T'][i][i] for i in range(8)]==e2['cases'][boolean]['positive_T_diagonal'],'stored positive T diagonals')
        require(case['direct_schur_vs_tail_identity_count']==204,'stored actual active entry count')
    require(e1['matrix_cases']['witness']['L'][7][1]==0 and e1['matrix_cases']['witness']['L'][6][1]==-1,'canonical 8,2 certificate orientation')
    require(F(5272,63)**2-F(17948132,2601)==F(e2['exact_gap'])>0,'rational gap receipt consistency')
    check('independent numerical receipts agree',witness_bounds=64,candidate_bounds=204,canonical_modification=[8,2],new_Lean_theorem=False)
    for rel,meta in allinputs.items():match(P/rel,meta)
    for rel,p in full_tree(P).items():
        if rel.startswith('verification/statement-gate-preflight/'):continue
        require(rel in allinputs,'new unexpected project file '+rel)
    OUT['stage']='complete'
    OUT['pass']=True
    OUT['coordinator_acceptance_required']=True
    OUT['checked_reviewed_input_count']=len(allinputs)
    OUT['proposed_binding_canonical_JSON_sha256']=metadata_hash(OUT['proposed_input_binding'])
    OUT['portable_reproduction']=['python3','-B','verification/statement-gate-preflight/verify_preflight.py',
      '--project','<IE05_LEAN_PROJECT>','--source-repo','<GIT_REPO_WITH_SOURCE_BASE>',
      '--packages','<TEN_READ_ONLY_PINNED_PACKAGE_DIRS>','--lean','<LEAN_4.33.1_BIN>']

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parents[2])
    parser.add_argument('--source-repo',type=pathlib.Path,default=pathlib.Path('/tmp/nla-lean-ra20-worktree'))
    parser.add_argument('--packages',type=pathlib.Path,default=pathlib.Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages'))
    parser.add_argument('--lean',type=pathlib.Path,default=pathlib.Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean'))
    args=parser.parse_args();code=0
    try:main(args)
    except BaseException as exc:
        OUT['pass']=False;OUT['error']=repr(exc);OUT['traceback']=traceback.format_exc();code=1
    print(json.dumps(OUT,indent=2,sort_keys=True))
    sys.exit(code)
