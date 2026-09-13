#!/usr/bin/env python3
"""Independent audit of actual RA20 Ubuntu logs and original workflow artifacts.
Raw-control checklist adapted after reading the RA09 operational example; no
RA09 result is reused. This script performs no Lean or Linux execution itself.
"""
from pathlib import Path, PurePosixPath
from collections import Counter
import hashlib, json, re, zipfile

E=Path(__file__).resolve().parent
P=E.parents[1];G=P.parents[2]
HEAD='43603b173beb294c2588d83f936a8a96246fd5f0'
RUN=34743832047
RAJOB=103687982518
CONTROLJOB=103687982272
IDRUN=34743832109
B=json.loads((E/'source-binding.json').read_text())
assert B['candidate']==HEAD and B['candidate_input_count']==1092
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def save(n,d):(E/n).write_text(json.dumps(d,indent=2)+'\n')
def api(n):return load(E/'commands'/n/'stdout')

vs=list((E/'artifacts/lean-RA-20').glob('verify-*'))
ss=list((E/'artifacts/lean-checker-controls').glob('selftest-*'))
assert len(vs)==len(ss)==1
V,S=vs[0],ss[0]
r=load(V/'result.json')
assert r['repository_commit']==HEAD and r['project']==B['project']
assert r['result']=='comparator-accepted' and r['semantic_review']=='not-performed-by-this-command'
assert r['input_sha256']=={n:v['sha256'] for n,v in B['candidate_inputs'].items()}
assert len(r['input_sha256'])==1092
for n,h in r['input_sha256'].items():assert sha((P/n).read_bytes())==h,n
config=r['config'];names=config['theorem_names'];assert config==B['config'] and len(names)==12
tool=r['tool_receipt']
assert r['source_lock_sha256']==tool['source_lock_sha256']==B['source_lock_sha256']
assert tool['forsythe_commit']=='8d1b0c0545a77b40245e84705aa7d273e6c81e62'
assert tool['ci_sandbox_probe_sha256']==B['derived_ci_probe_sha256']
assert len(B['checker_source_files'])==58
assert tool['lean_toolchain']=='leanprover/lean4:v4.33.1'
assert tool['lean_version']=='Lean (version 4.33.1, x86_64-unknown-linux-gnu, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)'
assert tool['go_version']=='go version go1.27.1 linux/amd64'
assert tool['platform']=='Linux-6.17.0-1022-azure-x86_64-with-glibc2.39'
assert set(tool['executables'])=={'.tools/comparator/.lake/build/bin/comparator',
    '.tools/lean4export/.lake/build/bin/lean4export','.tools/bin/landrun'}
standalone=load(S/'result.json')
assert standalone['result']=='checker-selftest-passed'
assert standalone['mathematical_verification']=='none; checker fixtures only'
assert standalone['tool_receipt']==tool

controls={}
for label,d in [('standalone-checker-controls',S),('RA20-preproof-controls',V)]:
    sandbox=(d/'sandbox.log').read_text()
    for mode in ['build','export']:assert f'MODE {mode}: exit=0' in sandbox
    for kind in ['user','pid','mnt','net','ipc','uts']:
        assert sandbox.count(f'PASS {kind} namespace: private')==2
    for marker in ['PASS outside .lake write-open: denied errno=30',
                   'PASS outside .lake truncate: denied errno=30',
                   'PASS outside .lake read-only truncate-open: denied errno=30',
                   'PASS symlink from .lake to outside write: denied errno=30',
                   'PASS outside .lake creation: denied errno=30',
                   'PASS host parent: absent from private /proc',
                   'PASS host parent signal lookup: denied errno=3',
                   'PASS host loopback listener: unreachable errno=13',
                   'PASS AF_UNIX socket creation: denied errno=97',
                   'PASS effective capabilities: none','PASS no_new_privs: set',
                   'PASS nested namespace write attempt: rejected exit=1',
                   'bwrap: setting up uid map: Permission denied']:
        assert sandbox.count(marker)==2,(label,marker)
    assert re.findall(r'Sandbox UID: (\d+)',sandbox)==['1001','1001']
    for marker in ['PASS build .lake write: allowed','PASS export .lake write-open: denied errno=30',
                   'PASS export .lake truncate: denied errno=30',
                   'Outer and export fixture contents unchanged; only designated build fixture written.']:
        assert marker in sandbox
    for case in ['unknown option','unexpected --rw','unexpected --rwx','relative --rwx']:
        assert f'NEGATIVE {case}: exit=2' in sandbox
    kernel=(d/'kernel-controls.log').read_text()
    for marker in ['RETURN honest_with_inductives_and_quotients: accepted',
                   'RETURN invalid_raw_proof: rejected:', '(kernel) declaration type mismatch',
                   '  True','  False','Quotient post-check rejects the solution',
                   'RETURN quotient_postcheck_mismatch: rejected: Quotient constant mismatch on: Quot.lift',
                   'PASS: all three actual Comparator.runBuiltinKernel cases behaved as required']:
        assert marker in kernel
    assert kernel.count('Running Lean default kernel on solution.')==3
    assert kernel.count('Lean default kernel accepts the solution')==2
    comp=(d/'comparator-controls.log').read_text()
    phases={'simple_match':'Your solution is okay!',
            'simple_mismatch':"Challenge and solution constant kind don't match: 'comm'",
            'simple_axiom_issue':"Illegal axiom detected: 'helper'",
            'simple_kind_mismatch':"Illegal axiom detected: 'helper'",
            'type_mismatch':"Challenge and solution theorem statement do not match: 'checked'"}
    for case,phase in phases.items():
        block=comp.split('\nCASE '+case+'\n',1)[1].split('\nCASE ',1)[0]
        code=0 if case=='simple_match' else 1
        assert f'PASS {case}: exit {code}, expected {code}' in block
        assert phase in block and 'required phase: '+phase in block
        assert block.count('Building Challenge')==block.count('Building Solution')==1
        assert block.count('Exporting #[')==2
    assert 'Lean default kernel accepts the solution' in comp
    assert comp.count('Building Challenge')==comp.count('Building Solution')==5
    assert comp.count('Exporting #[')==10
    for f,axiom in [('negative-sorry.log','sorryAx'),('negative-native.log','checked._native.native_decide.ax_1_1')]:
        text=(d/f).read_text()
        assert text.count('Building Challenge')==text.count('Building Solution')==1
        assert text.count('Exporting #[')==2 and f"Illegal axiom detected: '{axiom}'" in text
        assert text.rstrip().endswith('EXIT_STATUS=1')
    for f in ['sandbox.log','kernel-controls.log','comparator-controls.log','user-service.log']:
        assert (d/f).read_text().rstrip().endswith('EXIT_STATUS=0')
    controls[label]={'sandbox_modes':2,'nonroot_UIDs':[1001,1001],'sandbox_option_rejections':4,
        'actual_default_kernel_fixtures':3,'actual_comparator_fixtures':5,'forbidden_axiom_rejections':2,
        'nested_namespace_denial_stage':'bwrap executable ran; UID-map setup was denied before the inner write. No completed nested-write syscall is claimed.'}

def normalized(s):
    s=re.sub(r'\b[0-9a-f]{32}\b','INVOCATION',s)
    s=re.sub(r'\([0-9.]+[m]?s\)','(TIME)',s)
    s=re.sub(r'((?:Service runtime|CPU time consumed|Memory peak|Memory swap peak): ).*',r'\1RESOURCE',s)
    return re.sub(r'nla-axiom-[a-z0-9_]+','nla-axiom-FRESH',s)
control_texts={}
for f in ['sandbox.log','kernel-controls.log','comparator-controls.log','negative-sorry.log','negative-native.log','user-service.log']:
    first,second=(V/f).read_text(),(S/f).read_text()
    assert normalized(first)==normalized(second),f
    control_texts[f]={'RA20_sha256':sha((V/f).read_bytes()),'standalone_sha256':sha((S/f).read_bytes()),
                      'normalized_complete_sha256':sha(normalized(first).encode())}

main=(V/'comparator.log').read_text();main_command=main.splitlines()[0]
assert main_command.startswith('$ systemd-run --user ')
for marker in ['--wait --pipe --collect','RestrictAddressFamilies=~AF_UNIX','/usr/bin/env -i ',
               'COMPARATOR_LANDRUN=','/scripts/strict_landrun.py','COMPARATOR_LEAN4EXPORT=',
               'GIT_CONFIG_GLOBAL=/dev/null',' comparator.json']:
    assert marker in main_command,marker
assert '--skip-kernel' not in main
fresh=re.search(r'--working-directory (\S+)',main_command).group(1)
assert '/.verification-tmp/nla-fresh-proof-' in fresh and fresh.endswith('/project')
assert main.count('Building Challenge')==main.count('Building Solution')==1
assert main.count('Exporting #[')==2
for module in ['Definitions','Algebra','Smooth','SmoothTransport','Tangent','Differential','Critical','Generic','Count','Proof']:
    assert 'Built NLA.RA20.'+module in main
assert 'Built Solution' in main and 'Built LeanCert.Tactic.Verification' in main
assert main.split('Building Solution',1)[0].count('declaration uses `sorry`')==12
assert 'declaration uses `sorry`' not in main.split('Building Solution',1)[1]
warnings=re.findall(r'^warning: (.*)',main.split('Building Solution',1)[1],re.M)
assert len(warnings)==2
assert warnings[0].startswith('NLA/RA20/Differential.lean:103:2: Try this:')
assert warnings[1].startswith('NLA/RA20/Differential.lean:105:2: Try this:')
assert main.count('linter.style.haveILetI')==2
build_jobs=[int(v) for v in re.findall(r'Build completed successfully \((\d+) jobs\)\.',main)]
assert build_jobs==[3202,3494]
exports=re.findall(r'Exporting #\[(.*?)\] from (Challenge|Solution)',main)
assert [module for _,module in exports]==['Challenge','Solution']
for listing,module in exports:
    assert [v.strip() for v in listing.split(',') if v.strip().startswith('NLA.RA20.')]==names
axioms=re.findall(r"^info: ([^:\n]+):(\d+):0: '([^'\n]+)' depends on axioms: \[([^\]]*)\]",main,re.M)
assert len(axioms)==main.count('depends on axioms:')==57
assert all([v.strip() for v in ax.split(',')]==config['permitted_axioms'] for _,_,_,ax in axioms)
expected=[]
for filename,v in B['source_trust_scan'].items():
    text=(P/filename).read_text()
    for match in re.finditer(r'^#print axioms\s+(\S+)',text,re.M):
        name=match.group(1)
        if not name.startswith('NLA.RA20.'):name='NLA.RA20.'+name
        expected.append((filename,text.count('\n',0,match.start())+1,name))
assert Counter(expected)==Counter((f,int(line),name) for f,line,name,_ in axioms)
assert len({name for _,_,name,_ in axioms})==45
assert B['source_kernel_assertions']==61 and len(expected)==57
for marker in ['Running Lean default kernel on solution.','Lean default kernel accepts the solution','Your solution is okay!']:
    assert marker in main
assert main.rstrip().endswith('EXIT_STATUS=0')
save('axiom-verification.json',{'status':'PASS','source_occurrences':57,'distinct_names':45,
    'source_kernel_assertions':61,'four_unprinted_assertions':4,
    'records':[{'file':f,'line':int(line),'declaration':name,'axioms':[v.strip() for v in ax.split(',')]} for f,line,name,ax in axioms],
    'multiplicity_scope':'Several supporting theorem names print in their defining modules and again in Proof; source file/line occurrences, not unique names, are matched exactly. Twelve final-referee diagnostic exports are absent from this official source run.'})

manifest=load(P/'lake-manifest.json');deps=(V/'dependencies.log').read_text()
assert len(manifest['packages'])==10
for dep in manifest['packages']:
    assert f"{dep['name']}: cloning {dep['url']}" in deps
    assert f"{dep['name']}: checking out revision '{dep['rev']}'" in deps
assert deps.rstrip().endswith('EXIT_STATUS=0')
cache=(V/'mathlib-cache.log').read_text()
cache_counts=re.findall(r'^Decompressed (\d+) file\(s\)',cache,re.M)
assert cache_counts==['8690'] and cache.rstrip().endswith('EXIT_STATUS=0')
for label in ['lean-RA-20','lean-checker-controls']:
    d=E/'artifacts'/label/'bootstrap'
    for f in ['elan.log','landrun-build.log','comparator-build.log']:
        assert (d/f).read_text().rstrip().endswith('EXIT_STATUS=0')
    for marker in ['Built comparator:exe','Built lean4export:exe']:
        assert marker in (d/'comparator-build.log').read_text()

run=api('014-final-run');jobsdata=api('013-jobs');jobs=jobsdata['jobs']
assert run['id']==RUN and run['head_sha']==HEAD and run['run_attempt']==1
assert run['event']=='push' and run['status']=='completed' and run['conclusion']=='success'
assert run['path']=='.github/workflows/lean-verification.yml'
assert len(jobs)==jobsdata['total_count']==17 and len({j['id'] for j in jobs})==17
assert all(j['run_id']==RUN and j['head_sha']==HEAD and j['status']=='completed' and j['conclusion']=='success' for j in jobs)
assert all(s['status']=='completed' and s['conclusion']=='success' for j in jobs for s in j['steps'])
rajob=next(j for j in jobs if j['id']==RAJOB);cj=next(j for j in jobs if j['id']==CONTROLJOB)
assert rajob['name']=='verify (RA-20, randomized-and-low-rank-approximation/RA-20/lean)'
assert cj['name']=='checker-controls'
job_raw_paths={103687957360:'010-select-job-log',CONTROLJOB:'009-controls-job-log',RAJOB:'016-ra20-job-log'}
wholepath=E/'commands/018-whole-run-log-zip/stdout'
whole_members={};full_jobs={};job_raw={}
with zipfile.ZipFile(wholepath) as z:
    assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==217
    for item in z.infolist():
        n=PurePosixPath(item.filename)
        assert not n.is_absolute() and '..' not in n.parts and ((item.external_attr>>16)&0o170000)!=0o120000
        assert not item.is_dir()
        data=z.read(item);whole_members[item.filename]={'sha256':sha(data),'bytes':len(data)}
    for j in jobs:
        display=j['name'].replace('/','_')
        top=[n for n in z.namelist() if '/' not in n and re.fullmatch(r'\d+_'+re.escape(display)+r'\.txt',n)]
        assert len(top)==1
        raw=z.read(top[0]);text=raw.decode();job_raw[j['id']]=text
        assert HEAD in text and '##[error]' not in text
        assert 'Ubuntu2404-Readme.md' in text and 'Version: 20260907.300.1' in text
        assert '--skip-kernel' not in text
        if j['id'] in job_raw_paths:
            assert raw==(E/'commands'/job_raw_paths[j['id']]/'stdout').read_bytes()
        for s in j['steps']:
            candidates=[n for n in z.namelist() if n.startswith(display+'/'+str(s['number'])+'_')]
            assert len(candidates)==1,(j['name'],s['number'],s['name'])
        full_jobs[str(j['id'])]={'name':j['name'],'top_level_log':top[0],
            'sha256':sha(raw),'steps':j['steps'],'all_steps_successful':True}
assert len(full_jobs)==17
select=job_raw[103687957360]
assert 'BASE_REF: '+'0'*40 in select and 'EVENT_NAME: push' in select
assert re.findall(r'Ran (\d+) tests',select)==['30','12']
ra20raw=job_raw[RAJOB]
assert 'Manifest schema and comparator coverage: PASS (12 declarations)' in ra20raw
for raw in [ra20raw,job_raw[CONTROLJOB]]:
    for marker in ['sudo apt-get update','bubblewrap','ulimit -n 65536','tools/lean/bootstrap.sh',
                   '$RUNNER_TEMP/nla-lean-tools','Prepare unprivileged Linux isolation']:
        assert marker in raw,marker
assert 'tools/lean/verify.sh' in ra20raw and 'tools/lean/selftest.sh' in job_raw[CONTROLJOB]
save('whole-run-verification.json',{'status':'PASS','run':RUN,'candidate':HEAD,
    'zip_path':str(wholepath.relative_to(E)),'zip_sha256':sha(wholepath.read_bytes()),
    'archive_file_count':217,'complete_members':whole_members,'whole_job_count':17,'jobs':full_jobs,
    'three_selected_job_API_logs_exactly_equal_whole_ZIP_members':True,
    'selection_tests':[30,12],'zero_before_SHA_selected_all_15_projects':True,
    'other_project_semantic_audits_claimed':False})

art=api('015-final-artifacts')
assert len(art['artifacts'])==art['total_count']==16 and len({a['id'] for a in art['artifacts']})==16
artifacts=[]
for a in art['artifacts']:
    assert not a['expired'] and a['workflow_run']['id']==RUN and a['workflow_run']['head_sha']==HEAD
    assert a['workflow_run']['head_branch']=='codex/lean-ra20-hollow-critical-count'
    if a['name']=='lean-RA-20':rawzip=E/'commands/019-ra20-artifact/stdout';j=rajob
    elif a['name']=='lean-checker-controls':rawzip=E/'commands/006-controls-artifact/stdout';j=cj
    else:
        rawzip=E/'commands'/('020-artifact-'+str(a['id']))/'stdout'
        ident=a['name'][len('lean-'):]
        j=next(j for j in jobs if j['name'].startswith('verify ('+ident+','))
    raw=rawzip.read_bytes();assert sha(raw)==a['digest'].removeprefix('sha256:') and len(raw)==a['size_in_bytes']
    upload=job_raw[j['id']]
    assert 'SHA256 digest of uploaded artifact zip is '+sha(raw) in upload
    assert f"Artifact ID {a['id']}" in upload
    members={}
    with zipfile.ZipFile(rawzip) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
        for info in z.infolist():
            n=PurePosixPath(info.filename)
            assert not n.is_absolute() and '..' not in n.parts and ((info.external_attr>>16)&0o170000)!=0o120000
            if info.is_dir():continue
            data=z.read(info);members[info.filename]={'sha256':sha(data),'bytes':len(data)}
            if a['name'] in {'lean-RA-20','lean-checker-controls'}:
                assert data==(E/'artifacts'/a['name']/n).read_bytes()
    if a['name'] in {'lean-RA-20','lean-checker-controls'}:
        d=E/'artifacts'/a['name'];assert set(members)=={str(p.relative_to(d)) for p in d.rglob('*') if p.is_file()}
    artifacts.append({'name':a['name'],'id':a['id'],'job_id':j['id'],'raw_zip':str(rawzip.relative_to(E)),
        'zip_sha256':sha(raw),'zip_bytes':len(raw),'files':members,
        'API_digest_original_ZIP_and_upload_job_agree':True,
        'proof_or_control_semantics_audited':a['name'] in {'lean-RA-20','lean-checker-controls'}})
assert len(artifacts)==16
save('artifact-verification.json',{'status':'PASS','all16_original_artifacts_verified':True,'artifacts':artifacts})

ids=api('011-id-run');idj=api('012-id-jobs')
assert ids['id']==IDRUN and ids['head_sha']==HEAD and ids['status']=='completed' and ids['conclusion']=='success'
assert len(idj['jobs'])==idj['total_count']==1
assert idj['jobs'][0]['id']==103687957731
assert all(s['status']=='completed' and s['conclusion']=='success' for s in idj['jobs'][0]['steps'])
idtext=(E/'commands/017-id-job-log/stdout').read_text()
assert HEAD in idtext and '##[error]' not in idtext
assert 'Validated 217 permanent problem IDs' in idtext
assert re.findall(r'Ran (\d+) tests',idtext)==['17','3','16','11']

save('runtime-verification.json',{
    'status':'APPROVE independent actual Ubuntu operational verification','candidate':HEAD,'run':RUN,'run_attempt':1,
    'RA20_job':RAJOB,'checker_controls_job':CONTROLJOB,'all17_jobs_and_steps_successful':True,
    'candidate_Git_and_actual_Linux_inputs_bound':1092,'actual_exports':names,
    'default_kernel_replay':'accepted','statement_Comparator':'accepted',
    'source_kernel_assertions':61,'actual_printed_standard_three_axiom_occurrences':57,'distinct_printed_names':45,
    'deliberate_Challenge_admission_warnings':12,'existing_Differential_style_warnings':warnings,
    'actual_Challenge_graph_jobs':3202,'actual_Solution_graph_jobs':3494,
    'actual_main_command':main_command,'fresh_project':fresh,'actual_tool_receipt':tool,
    'all58_checker_sources_and_derived_probe_bound':True,'actual_controls':controls,
    'complete_control_text_correspondence':control_texts,
    'control_normalization_scope':'Only invocation IDs, fresh axiom directory names, elapsed times and resource measurements; commands, rejection phases and outcomes preserved.',
    'ten_dependency_revisions':manifest['packages'],'official_matching_Mathlib_cache_files':8690,
    'cache_scope':'Fresh RA20 project proof compilation used official matching dependency objects. This is not a from-source rebuild of every Mathlib dependency; no dependency object was downloaded/copied locally for this audit.',
    'all16_original_artifact_API_upload_ZIP_identities_verified':True,'whole_workflow_original_log_files':217,
    'permanent_ID_run':IDRUN,'permanent_ID_count':217,'ID_workflow_test_groups':[17,3,16,11],
    'operational_reviewer':'/root/ra20_final_referee2','new_mathematical_approval':False,
    'new_local_Lean_or_Linux_execution':False,'other_project_semantic_audits_claimed':False,
    'canonical_status':'Solved, unchanged','root_operational_acceptance_and_publication':'pending'})
print(json.dumps({'status':'RUNTIME_AUDIT_PASS','candidate_inputs':1092,'all_jobs':17,'all_artifacts':16,
                  'exports':12,'source_kernel_assertions':61,'source_axiom_occurrences':57,
                  'default_kernel':'accepted','Comparator':'accepted','actual_control_runs':2}))
