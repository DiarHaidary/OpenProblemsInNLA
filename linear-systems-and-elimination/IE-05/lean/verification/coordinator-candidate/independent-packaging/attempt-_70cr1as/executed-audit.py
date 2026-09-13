"""Independent read-only audit of the immutable concrete IE-05 package.

No proof compilation and no candidate/original/dependency writes. All command
receipts and diagnostic attempts are created only under this external directory.
"""
from pathlib import Path, PurePosixPath
import argparse,datetime,hashlib,importlib.util,json,os,posixpath,re,subprocess,sys,tempfile,time,traceback
import yaml

E=Path(__file__).resolve().parent
P=Path('/tmp/nla-lean-formalization/ie05-candidate-package/lean')
D=Path('/tmp/nla-lean-formalization/next-ie05-statements-draft/lean')
R=Path('/tmp/nla-lean-ra20-worktree')
PY=Path('/tmp/nla-lean-formalization/venv/bin/python')
CP='verification/candidate-package'
sha=lambda b:hashlib.sha256(b).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        assert k not in d,('duplicate JSON key',k)
        d[k]=v
    return d
def load(p):return json.loads(Path(p).read_text(),object_pairs_hook=unique)
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def member_record(value):
    if isinstance(value,str):return {'sha256':value}
    assert isinstance(value,dict) and 'sha256' in value,value
    return value
def inventory(root):
    d={}
    for q in sorted(root.rglob('*')):
        assert not q.is_symlink(),q
        if q.is_file():
            n=str(q.relative_to(root));b=q.read_bytes()
            assert '.lake' not in q.relative_to(root).parts and q.suffix not in ['.olean','.ilean','.o','.so','.a'],n
            d[n]={'sha256':sha(b),'bytes':len(b)}
    return d
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--handoff',required=True);ap.add_argument('--handoff-sha',required=True);ap.add_argument('--manifest',required=True);ap.add_argument('--manifest-sha',required=True);args=ap.parse_args()
    a=Path(tempfile.mkdtemp(prefix='attempt-',dir=E))
    (a/'executed-audit.py').write_bytes(Path(__file__).read_bytes())
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/mf16_final_referee','phase':'Independent candidate-packaging audit, not a new mathematical approval','candidate':str(P),'commands':[],'errors':[]}
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
    def run(cmd,label,cwd=R,input=None):
        start=time.monotonic();c=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (a/(label+'.stdout')).write_bytes(c.stdout);(a/(label+'.stderr')).write_bytes(c.stderr)
        if input is not None:(a/(label+'.stdin')).write_bytes(input)
        r={'command':list(map(str,cmd)),'cwd':str(cwd),'exit_code':c.returncode,'seconds':time.monotonic()-start,'stdout':label+'.stdout','stderr':label+'.stderr','stdout_sha256':sha(c.stdout),'stderr_sha256':sha(c.stderr),'stdin':label+'.stdin' if input else None}
        result['commands'].append(r);assert c.returncode==0,r
        return c.stdout
    try:
        assert sha((P/args.handoff).read_bytes())==args.handoff_sha
        assert sha((P/args.manifest).read_bytes())==args.manifest_sha
        before=inventory(P);save(a/'candidate-inputs-before.json',before)
        original=inventory(D);save(a/'original-inputs-before.json',original)
        baseline=load(P/CP/'PRE-PACKAGE-INPUTS.json');assert baseline['file_count']==2338
        assert baseline['files']==original,'original draft changed from exact packaging baseline'
        result['handoff']={'path':args.handoff,'sha256':args.handoff_sha,'manifest':args.manifest,'manifest_sha256':args.manifest_sha}
        amap=load(P/CP/'ARCHIVE-MAP.json');wrappers=amap['wrapper_archives']
        assert set(wrappers)=={'README.md','SourceCorrespondence.md','lakefile.toml'}
        def relative(root,name):
            n=posixpath.normpath(posixpath.join(root,name))
            assert n!='..' and not n.startswith('../') and not PurePosixPath(n).is_absolute(),n
            return n
        def checked(name,value):
            r=member_record(value);q=P/name;mapped=None
            if name in wrappers:
                w=wrappers[name]
                if r['sha256']==w['expected']['sha256']:
                    assert ('bytes' not in r or r['bytes']==w['expected']['bytes'])
                    q=P/w['archive'];mapped=w['archive']
            assert q.is_file() and not q.is_symlink(),str(q)
            b=q.read_bytes();assert sha(b)==r['sha256'],(name,str(q),'SHA mismatch')
            if 'bytes' in r:assert len(b)==r['bytes'],(name,'byte mismatch')
            if 'git_blob' in r:
                assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],name
            return mapped
        changes=[];mapped_records={}
        for name,r in original.items():
            mapped=checked(name,r)
            if before[name]!=r:changes.append(name)
            if mapped:mapped_records[name]={'archive':mapped,'original':r,'live':before[name]}
        assert set(changes)==set(wrappers)
        assert len(mapped_records)==3
        result['unchanged_originals']=len(original)-3;result['exact_wrapper_changes']=mapped_records
        for name,w in wrappers.items():
            assert w['expected']==original[name]
            assert (P/w['archive']).read_bytes()==(D/name).read_bytes()
        # Independently discover every historical top-level files inventory.
        filemaps={}
        for name in original:
            if not name.endswith('.json'):continue
            try:obj=load(D/name)
            except (json.JSONDecodeError,UnicodeDecodeError):continue
            files=obj.get('files') if isinstance(obj,dict) else None
            if isinstance(files,dict) and files and all(isinstance(k,str) and (isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) or isinstance(v,dict) and isinstance(v.get('sha256'),str) and re.fullmatch('[0-9a-f]{64}',v['sha256'])) for k,v in files.items()):filemaps[name]=files
        roots=amap['historical_inventory_roots'];assert set(roots)==set(filemaps),(set(filemaps)-set(roots),set(roots)-set(filemaps))
        nested={}
        for name,files in filemaps.items():
            root=roots[name];assert root['inventory']==original[name] and root['member_count']==len(files)
            original_map=load(D/name)
            sizes=original_map.get('file_sizes',original_map.get('sizes'))
            if sizes is not None:assert set(sizes)==set(files)
            mapped=[]
            for member,r in files.items():
                target=relative(root['root'],member)
                expected=dict(member_record(r))
                if sizes is not None:
                    assert 'bytes' not in expected or expected['bytes']==sizes[member]
                    expected['bytes']=sizes[member]
                resolved=checked(target,expected)
                if resolved:mapped.append({'original_path':target,'archive':resolved,'expected':member_record(r)})
            nested[name]={'root':root['root'],'entries':len(files),'exact_wrapper_lookups':mapped,'sha256':original[name]['sha256']}
        result['historical_inventories']=nested
        result['historical_inventory_count']=len(nested)
        archives=amap['primary_source_archives']
        for name,r in archives.items():
            checked(r['archive'],r['expected'])
            source=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')/r['source_package']/r['source_path_within_package']
            assert source.read_bytes()==(P/r['archive']).read_bytes(),name
        result['small_primary_source_archives']=len(archives)
        freeze=load(P/'reviews/proof-freeze.json');assert len(freeze['files'])==1800
        statement=load(P/'reviews/statement-freeze.json');assert len(statement['files'])==733
        for f in [freeze,statement]:
            for name,h in f['files'].items():checked(name,h)
        sourceinv=load(P/'verification/original-source-inventory.json')
        assert len(sourceinv['files'])==27
        query=''.join(freeze['base']+':'+n+'\n' for n in sourceinv['files']).encode()
        raw=run(['git','cat-file','--batch'],'original-Git-snapshots',input=query);pos=0;source_records={}
        for name,r in sourceinv['files'].items():
            end=raw.index(b'\n',pos);blob,kind,size=raw[pos:end].decode().split();start=end+1;b=raw[start:start+int(size)];pos=start+int(size)+1
            assert kind=='blob' and blob==r['git_blob'] and sha(b)==r['sha256'] and len(b)==r['bytes']
            assert b==(P/'verification/original-sources'/name).read_bytes()
            assert freeze['source_files'][name]==r['sha256'] and freeze['source_git_blobs'][name]==blob
            source_records[name]=r
        assert pos==len(raw)
        result['original_source_git_identities']=source_records
        mathfiles=['Challenge.lean','comparator.json','NUMERICAL_TARGETS.md','PROOF-MAP.md','lean-toolchain','lake-manifest.json','Solution.lean']+[str(q.relative_to(D)) for q in (D/'NLA/IE05').glob('*.lean')]
        assert len([n for n in mathfiles if n.startswith('NLA/')])==12
        for n in mathfiles:assert (P/n).read_bytes()==(D/n).read_bytes(),n
        result['unchanged_mathematical_and_trust_inputs']={n:before[n] for n in mathfiles}
        run([PY,R/'tools/lean/validate_manifest.py',P],'actual-v04-schema')
        helper='''import importlib.util,json,sys\nfrom pathlib import Path\nspec=importlib.util.spec_from_file_location("ie05_harness",sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)\nc=m.validate_project(Path(sys.argv[2]));print(json.dumps(c,indent=2))\n'''
        (a/'validate_actual_harness.py').write_text(helper)
        run([PY,a/'validate_actual_harness.py',R/'tools/lean/harness.py',P],'actual-harness-project-inputs')
        # This host's pinned schema interpreter is Python 3.10, without tomllib.
        # The exact single-line source change is stronger than parsing an unrelated
        # permissive TOML subset; the actual shared harness separately checks inputs.
        old_lake=(D/'lakefile.toml').read_text();lake=(P/'lakefile.toml').read_text()
        assert old_lake.count('defaultTargets = ["Challenge"]')==1
        assert lake==old_lake.replace('defaultTargets = ["Challenge"]','defaultTargets = ["Solution"]')
        assert re.findall(r'^defaultTargets\s*=\s*(.*)$',lake,re.M)==['["Solution"]']
        config=load(P/'comparator.json');names=config['theorem_names'];assert len(names)==17
        assert config==load(D/'comparator.json')
        assert config['definition_names']==[] and set(config['permitted_axioms'])=={'propext','Classical.choice','Quot.sound'}
        metadata=yaml.safe_load((P/'formalization.yaml').read_text())
        assert metadata['version']=='v0.4'
        assert [x['declaration'] for x in metadata['status']['main_results']]==names
        for r in metadata['status']['main_results']:
            assert r['file']=='NLA/IE05/Proof.lean' and r['sorry_count']==0 and r['comparator_config']=='comparator.json'
            assert not r.get('literature_dependencies',[])
        assert metadata['status']['sorry_count']==metadata['status']['sorry_in_definitions']==0
        assert set(metadata['status']['axioms'])=={'propext','Classical.choice','Quot.sound'}
        assert metadata['status']['whole_problem_verified'] is False
        assert metadata['status']['canonical_status']=='Solved'
        assert metadata['status']['actual_linux_comparator']==metadata['status']['independent_packaging_approval']=='pending'
        assert metadata['reproduction']['authoritative_Linux']['status']=='pending'
        assert [x['declaration'] for x in metadata['alignment']]==names
        pins={d['name']:d['rev'] for d in load(P/'lake-manifest.json')['packages']}
        assert len(pins)==10 and metadata['toolchain']['dependencies']==pins
        assert metadata['toolchain']['lean']==(P/'lean-toolchain').read_text().strip()
        for name,r in load(P/CP/'schema/SOURCE-RECORDS.json').items():
            archived=(P/CP/name).read_bytes();actual=(R/r['source_repository_path']).read_bytes()
            assert archived==actual and sha(archived)==r['sha256'] and len(archived)==r['bytes']
        run([PY,P/CP/'verify_inventory.py'],'candidate-author-readonly-archive-checker',cwd=P)
        run([PY,P/CP/'audit_metadata.py'],'candidate-author-readonly-metadata-checker',cwd=P)
        result['schema_and_static_harness']={'actual_schema_checked':True,'actual_harness_validate_project_checked':True,'Solution_default':True,'all17metadata_results_and_comparator_equal':True,'no_definition_holes':True,'standard_three_only':True,'no_Linux_or_Git_snapshot_run':True}
        live=(P/'README.md').read_text()+'\n'+(P/'SourceCorrespondence.md').read_text()+'\n'+(P/'formalization.yaml').read_text()
        for term in ['George Stepaniants','Computing and Mathematical Sciences','California Institute of Technology','John Peca-Medlin']:assert term in live,term
        privacy=[]
        for n in before:
            b=(P/n).read_bytes();t=b.decode(errors='ignore')
            if re.search(r'(?i)\b(?:[\w.+-]*stepaniants[\w.+-]*|george[\w.+-]*)@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',t):privacy.append(n)
        assert not privacy,privacy
        result['George_email_scan']='No matching George/Stepaniants email in any candidate file'
        new=set(before)-set(original)
        assert all(n in {'formalization.yaml','LICENSE','NOTICE.md',args.manifest} or n.startswith(CP+'/') for n in new),new
        result['new_files']=sorted(new)
        candmanifest=load(P/args.manifest)
        cfiles=candmanifest['files'];assert set(cfiles)==set(before)-{args.manifest},'candidate manifest must include every other candidate file'
        for n,r in cfiles.items():
            rec=member_record(r);assert before[n]['sha256']==rec['sha256']
            if 'bytes' in rec:assert before[n]['bytes']==rec['bytes']
        result['actual_complete_candidate_inventory_count']=len(before)
        result['candidate_manifest_exact_self_only']=True
        assert inventory(P)==before and inventory(D)==original
        save(a/'candidate-inputs-after.json',before)
        result['candidate_and_original_unchanged']=True
        result['status']='PASS static complete candidate, archives and metadata; human-readable package semantics still reviewed separately'
    except Exception:result['errors'].append(traceback.format_exc())
    result['success']=not result['errors'];save(a/'result.json',result)
    save(E/'LATEST.json',{'attempt':a.name,'result_sha256':sha((a/'result.json').read_bytes()),'success':result['success']})
    print(json.dumps({'attempt':a.name,'success':result['success'],'candidate_files':result.get('actual_complete_candidate_inventory_count'),'historical_inventory_count':result.get('historical_inventory_count'),'errors':result['errors']},indent=2))
    raise SystemExit(0 if result['success'] else 1)
if __name__=='__main__':main()
