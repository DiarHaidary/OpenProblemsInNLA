"""Independent read-only IE05 attempt-one audit. Writes only its own evidence.

No Lean, network, Git mutations, CI dispatch, or candidate modifications.
"""
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,re,subprocess,sys,tempfile,traceback,zipfile
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent
R=Path('/tmp/nla-lean-ie05-worktree'); REL='linear-systems-and-elimination/IE-05/lean'; P=R/REL
SHA='71cf72f9db2af0f01b5cfa7f18a69e28310eb52f'
API=E/'api-jlvyv9bw'; D=E/'downloads-dk41f3yi'; S=E/'supplement-ave_okm4'
A=Path(tempfile.mkdtemp(prefix='audit-',dir=E)); (A/'executed.py').write_bytes(Path(__file__).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def rec(p):
    b=p.read_bytes();return {'sha256':sha(b),'bytes':len(b)}
def unique(pairs):
    d={}
    for k,v in pairs:assert k not in d,k;d[k]=v
    return d
def load(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def save(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'success':False,'candidate':SHA,'attempt':1,'commands':[]}
def command(args,label,cwd=R):
    c=subprocess.run(args,cwd=cwd,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1'),capture_output=True)
    (A/(label+'.stdout')).write_bytes(c.stdout);(A/(label+'.stderr')).write_bytes(c.stderr)
    out['commands'].append({'argv':args,'cwd':str(cwd),'exit_code':c.returncode,'stdout_sha256':sha(c.stdout),'stderr_sha256':sha(c.stderr)})
    assert c.returncode==0,(label,c.stderr.decode(errors='replace'));return c.stdout
def exact(p,want):
    d=rec(p); want={'sha256':want} if isinstance(want,str) else want
    assert d['sha256']==want['sha256'],str(p)
    if 'bytes' in want:assert d['bytes']==want['bytes'],str(p)
    return d
def copy(p,rel):
    q=A/'consulted'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes());return rec(q)
try:
    assert command(['git','rev-parse','HEAD'],'head-before').decode().strip()==SHA
    assert command(['git','status','--porcelain=v1','--untracked-files=all'],'status-before')==b''
    commit=command(['git','cat-file','commit',SHA],'commit-object').decode()
    assert re.search(r'^author George Stepaniants <> \d+ [+-]\d+$',commit,re.M)
    assert re.search(r'^committer George Stepaniants <> \d+ [+-]\d+$',commit,re.M)
    api_commit=load(API/'commit.json');assert api_commit['sha']==SHA
    assert api_commit['commit']['author']['email']==api_commit['commit']['committer']['email']==''
    assert re.search(r'^tree (\w+)$',commit,re.M).group(1)==api_commit['commit']['tree']['sha']
    binding=load(E/'candidate-binding/git-inputs.json')['files'];assert len(binding)==2543
    for rel,w in binding.items():exact(P/rel,w)
    runtime=load(D/'lean-IE-05/verify-20260913T101713Z-4149/result.json')
    assert runtime['repository_commit']==SHA and runtime['project']==REL
    assert runtime['input_sha256']=={k:v['sha256'] for k,v in binding.items()}
    assert runtime['result']=='comparator-accepted' and runtime['semantic_review']=='not-performed-by-this-command'
    assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}==set(binding)
    out['all_committed_and_runtime_inputs_match']=len(binding)
    archive=load(P/'verification/candidate-package/ARCHIVE-MAP.json');wrappers=archive['wrapper_archives']
    assert set(wrappers)=={'README.md','SourceCorrespondence.md','lakefile.toml'}
    historical_count=0;redirects=0
    def member(root,key,w,sizes=None):
        nonlocal_dummy=None
        global redirects
        logical=(P/root/key).resolve();assert logical.is_relative_to(P.resolve()),key
        name=str(logical.relative_to(P.resolve()));w={'sha256':w} if isinstance(w,str) else dict(w)
        if sizes is not None:w['bytes']=sizes[key]
        if name in wrappers and w['sha256']==wrappers[name]['expected']['sha256']:
            logical=P/wrappers[name]['archive'];redirects+=1
        exact(logical,w)
        if 'git_blob' in w:
            b=logical.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==w['git_blob']
    before=load(P/'verification/candidate-package/PRE-PACKAGE-INPUTS.json')
    assert len(before['files'])==2338
    for n,w in before['files'].items():member('.',n,w)
    registry=archive['historical_inventory_roots'];assert len(registry)==29
    discovered=[]
    for n in before['files']:
        if n.endswith('.json'):
            try:t=load(P/n)
            except (ValueError,UnicodeError):continue
            if isinstance(t,dict) and isinstance(t.get('files'),dict) and t['files'] and all(isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) or isinstance(v,dict) and re.fullmatch('[0-9a-f]{64}',v.get('sha256','')) for v in t['files'].values()):discovered.append(n)
    assert set(discovered)==set(registry)
    counts={}
    for n,w in registry.items():
        exact(P/n,w['inventory']);t=load(P/n);assert len(t['files'])==w['member_count'];sizes=t.get('file_sizes',t.get('sizes'))
        for k,v in t['files'].items():member(w['root'],k,v,sizes)
        counts[n]=len(t['files'])
    assert counts['reviews/proof-freeze.json']==1800 and counts['reviews/statement-freeze.json']==733
    orig=load(P/'verification/original-source-inventory.json');assert len(orig['files'])==27
    original_rows={}
    for n,w in orig['files'].items():
        b=command(['git','cat-file','blob',w['git_blob']],f'original-{len(original_rows):02d}')
        assert sha(b)==w['sha256'] and (P/'verification/original-sources'/n).read_bytes()==b
        actual=command(['git','rev-parse',orig['base']+':'+n],f'original-path-{len(original_rows):02d}').decode().strip();assert actual==w['git_blob']
        original_rows[n]=w
    # Validate the later independently sealed packaging evidence after portable installation.
    coord=P/'verification/coordinator-candidate';ind=coord/'independent-packaging'
    for n,w in load(coord/'EVIDENCE-MANIFEST.json')['files'].items():exact(coord/n,w)
    independent=load(ind/'EVIDENCE-MANIFEST.json');assert len(independent['files'])==4854
    for n,w in independent['files'].items():
        kind,k=n.split('/',1)
        if kind=='original':member('.',k,w)
        elif kind=='evidence':exact(ind/k,w)
        elif kind=='author_package':
            if k.startswith('lean/'):exact(P/k[5:],w)
            else:exact(coord/'author-external'/k,w)
        else:raise AssertionError(n)
    for n in ['reviews/proof-freeze.json','reviews/statement-freeze.json','verification/final-review-acceptance.json','reviews/final-referee-1.md','reviews/final-referee-2.md','verification/candidate-package/ARCHIVE-MAP.json','verification/candidate-package/verify_inventory.py','verification/coordinator-candidate/ROOT-CHECKS.json','verification/coordinator-candidate/independent-packaging/REPORT.md']:
        copy(P/n,n)
    out['historical_preservation']={'original_accepted':2338,'proof':1800,'statements':733,'original_Git_sources':27,'historical_inventories':counts,'archive_redirects_checked':redirects,'independent_packaging_inventory_members':4854,'nested_EVIDENCE_MANIFEST_files':sum(Path(n).name=='EVIDENCE-MANIFEST.json' for n in binding)}
    run=load(API/'run.json');jobs=load(API/'jobs.json')['jobs'];assert run['head_sha']==SHA and run['run_attempt']==1 and run['status']=='completed' and run['conclusion']=='failure'
    assert len(jobs)==20 and {j['id'] for j in jobs if j['conclusion']=='failure'}=={103708463532,103708463566}
    for name,num in [('ie05-job.json',103708463461),('controls-job.json',103708463293)]:
        j=load(API/name);assert j['id']==num and j['conclusion']=='success' and j['labels']==['ubuntu-24.04']
        assert all(x['conclusion']=='success' for x in j['steps'])
    for n in ['MI06-attempt1.log','RA07-attempt1.log']:
        t=(S/n).read_text();assert 'curl: (22) The requested URL returned error: 500' in t and 'elan: command failed: curl' in t
        assert 'Lean default kernel accepts the solution' not in t
    ids=load(API/'ids-run.json');assert ids['head_sha']==SHA and ids['conclusion']=='success'
    idlog=(S/'permanent-IDs.log').read_text();assert 'Validated 217 permanent problem IDs' in idlog and 'Ran 17 tests' in idlog
    registry_ids=load(R/'problem_ids.json');assert registry_ids['IE-05']=='linear-systems-and-elimination/IE-05/README.md'
    assert (R/registry_ids['IE-05']).read_bytes()==(P/'verification/original-sources'/registry_ids['IE-05']).read_bytes()
    cfg=load(P/'comparator.json');assert cfg==runtime['config'];names=cfg['theorem_names'];assert len(names)==17 and len(set(names))==17 and cfg.get('definition_names',[])==[]
    assert set(cfg['permitted_axioms'])=={'propext','Classical.choice','Quot.sound'}
    logroot=D/'lean-IE-05/verify-20260913T101713Z-4149';cl=(logroot/'comparator.log').read_text()
    for n in names:assert len(re.findall(r'(?<![A-Za-z_])'+re.escape(n)+r'(?=[,\]])',cl))>=2,n
    assert 'Running Lean default kernel on solution.' in cl and 'Lean default kernel accepts the solution' in cl and 'Your solution is okay!' in cl and cl.endswith('EXIT_STATUS=0\n')
    ax=re.findall(r'depends on axioms: \[([^]]*)\]',cl);assert len(ax)==89 and set(ax)=={'propext, Classical.choice, Quot.sound'}
    assert 'Build completed successfully (2380 jobs).' in cl and 'Build completed successfully (3089 jobs).' in cl
    assert len(re.findall(r'warning: Challenge.lean:\d+:\d+: declaration uses `sorry`',cl))==17
    assert 'warning: Solution.lean:' not in cl
    out['actual_Linux']={'attempt':1,'job':103708463461,'runner':'Ubuntu 24.04.5 / x86_64 / UID 1001','exports':names,'standard_three_source_axiom_reports':89,'Challenge_build_jobs':2380,'Solution_build_jobs':3089,'Challenge_intended_holes':17,'result':'default-kernel and Comparator accepted','overall_workflow':'failure; exactly two unrelated elan installer HTTP 500 failures'}
    controlsroot=D/'lean-checker-controls/selftest-20260913T101712Z-4114'
    selftest=load(controlsroot/'result.json');assert selftest['result']=='checker-selftest-passed' and selftest['tool_receipt']==runtime['tool_receipt']
    for lr in [logroot,controlsroot]:
        k=(lr/'kernel-controls.log').read_text();assert 'PASS: all three actual Comparator.runBuiltinKernel cases behaved as required' in k and k.endswith('EXIT_STATUS=0\n')
        for s in ['honest_with_inductives_and_quotients','invalid_raw_proof','quotient_postcheck_mismatch']:assert s in k
        c=(lr/'comparator-controls.log').read_text();assert 'PASS: all five Comparator regressions' in c and c.endswith('EXIT_STATUS=0\n')
        for s in ['simple_match','simple_mismatch','simple_axiom_issue','simple_kind_mismatch','type_mismatch']:assert s in c
        for n,marker in [('native',"Illegal axiom detected: 'checked._native.native_decide.ax_1_1'"),('sorry',"Illegal axiom detected: 'sorryAx'")]:
            t=(lr/('negative-'+n+'.log')).read_text();assert marker in t and t.endswith('EXIT_STATUS=1\n')
        t=(lr/'sandbox.log').read_text();assert t.count('Sandbox UID: 1001')==2 and t.count('bwrap: setting up uid map: Permission denied')==2
        for m in ['outside .lake write-open: denied','host parent: absent','host loopback listener: unreachable','AF_UNIX socket creation: denied','effective capabilities: none','no_new_privs: set','nested namespace write attempt: rejected','Outer and export fixture contents unchanged']:
            assert m in t,m
        assert t.endswith('EXIT_STATUS=0\n') and (lr/'user-service.log').read_text().endswith('EXIT_STATUS=0\n')
    deps=(logroot/'dependencies.log').read_text();manifest=load(P/'lake-manifest.json');packages=manifest['packages'];assert len(packages)==10
    for pk in packages:assert f"info: {pk['name']}: checking out revision '{pk['rev']}'" in deps
    assert deps.count(': cloning ')==10
    cache=(logroot/'mathlib-cache.log').read_text();assert 'Decompressed 8690 file(s)' in cache and cache.endswith('EXIT_STATUS=0\n')
    lock=load(R/'tools/lean/source-lock.json');assert len(lock['files'])==58
    assert rec(R/'tools/lean/source-lock.json')['sha256']==runtime['source_lock_sha256']==runtime['tool_receipt']['source_lock_sha256']
    toolrows={}; F=Path('/Users/georgestepaniants/Research/Forsythe')
    for i,w in enumerate(lock['files']):
        b=command(['git','show',lock['commit']+':'+w['source']],f'tool-{i:02d}',F)
        assert sha(b)==w['sha256'] and len(b)==w['bytes']
        q=A/'tool-sources'/w['destination'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);toolrows[w['destination']]=w
    spec=importlib.util.spec_from_file_location('inspected_ie05_harness',R/'tools/lean/harness.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
    probe=h.ci_probe_source(A/'tool-sources');assert sha(probe.encode())==runtime['tool_receipt']['ci_sandbox_probe_sha256'];(A/'tool-sources/reproduction/checks/sandbox_probe_ci.py').write_text(probe)
    assert h.validate_project(P)==cfg
    command(['python3','tools/lean/validate_manifest.py',str(P)],'schema-and-coverage')
    out['dependencies']={'packages':packages,'fresh_public_checkout_count':10,'matching_Mathlib_cached_files':8690,'tool_source_files':58,'source_lock_sha256':runtime['source_lock_sha256'],'tool_receipt':runtime['tool_receipt'],'CI_probe_exact_derived_hash_matches':True}
    # Bind actual artifact receipt, ZIP digest, upload-job digest, and every extracted byte.
    artifactmetadata=load(API/'artifacts.json')['artifacts'];download=load(D/'result.json')
    for n,jlog in [('lean-IE-05','ie05-job.log'),('lean-checker-controls','controls-job.log')]:
        md=next(x for x in artifactmetadata if x['name']==n);z=D/(n+'.zip');assert 'sha256:'+sha(z.read_bytes())==md['digest'] and z.stat().st_size==md['size_in_bytes']
        assert md['workflow_run']['id']==34751393873 and md['workflow_run']['head_sha']==SHA
        t=(D/jlog).read_text();assert '24.04.5' in t and SHA in t and md['digest'].split(':')[1] in t and str(md['id']) in t
        with zipfile.ZipFile(z) as zz:
            assert zz.testzip() is None
            actual={i.filename for i in zz.infolist() if not i.is_dir()};assert actual=={str(p.relative_to(D/n)) for p in (D/n).rglob('*') if p.is_file()}
            for k in actual:assert zz.read(k)==(D/n/k).read_bytes()
    assert download['archives']['runlogs.zip']['member_count']==0
    out['artifact_identity']={n:{'sha256':sha((D/(n+'.zip')).read_bytes()),'files':download['archives'][n+'.zip']['member_count']} for n in ['lean-IE-05','lean-checker-controls']}
    out['run_log_archive_limitation']='GitHub full-run ZIP endpoint returned a valid empty archive. No full-run ZIP coverage claimed. Original individual IE05/checker/select/ID/MI06/RA07 logs are retained.'
    for n in ['README.md','formalization.yaml']:
        t=(P/n).read_text();assert 'George Stepaniants' in t and 'California Institute of Technology' in t and 'Computing and Mathematical Sciences' in t
        assert not re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',t)
    command(['git','diff','--exit-code','HEAD','--'],'diff-after')
    assert command(['git','status','--porcelain=v1','--untracked-files=all'],'status-after')==b''
    out['success']=True
except Exception:out['error']=traceback.format_exc()
save(A/'result.json',out)
save(E/'AUDIT-LATEST.json',{'directory':A.name,'result':rec(A/'result.json')})
print(json.dumps({k:v for k,v in out.items() if k not in ['commands','historical_preservation','dependencies']},indent=2))
raise SystemExit(0 if out['success'] else 1)
