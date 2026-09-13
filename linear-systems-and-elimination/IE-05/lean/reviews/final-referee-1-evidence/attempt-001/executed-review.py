#!/usr/bin/env python3
"""Independent final-referee-1 evidence runner; never mutates reviewed inputs."""
from pathlib import Path
import datetime, hashlib, json, os, platform, re, shutil, subprocess, sys, time

ROOT = Path(__file__).resolve().parents[2]
OWN = ROOT / 'reviews/final-referee-1-evidence'
LEANROOT = Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
LEAN = LEANROOT / 'bin/lean'
PACKAGES = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
GITROOT = Path('/tmp/nla-lean-ra20-worktree')
ORDER = ['Definitions', 'Pivot', 'GEPP', 'Scaling', 'QR', 'IntegerQR',
         'LUTrajectory', 'ExactCertificates', 'Witness', 'GrowthBounds', 'Growth', 'Proof']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,v):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def run(where,label,argv,env_extra=None,stdin=None):
    d=where/'commands'/label; d.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy(); env.update({'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1'})
    env.update(env_extra or {})
    rec={'argv':[str(x) for x in argv], 'cwd':str(ROOT), 'utc_start':utc(),
         'environment_overrides':{k:env[k] for k in ['GIT_OPTIONAL_LOCKS','PYTHONDONTWRITEBYTECODE']+list(env_extra or {})}}
    if stdin is not None: (d/'stdin').write_bytes(stdin); rec['stdin_sha256']=sha(d/'stdin')
    save(d/'command.json',rec)
    start=time.monotonic()
    with (d/'stdout').open('wb') as out, (d/'stderr').open('wb') as err:
        p=subprocess.run(rec['argv'],cwd=ROOT,env=env,input=stdin,stdout=out,stderr=err)
    save(d/'result.json',{'exit_code':p.returncode,'seconds':time.monotonic()-start,
        'utc_end':utc(),'stdout_sha256':sha(d/'stdout'),'stderr_sha256':sha(d/'stderr')})
    if p.returncode: raise RuntimeError(f'{label} failed ({p.returncode}); evidence preserved in {d}')
    return (d/'stdout').read_bytes()

def members(name,expected):
    p=ROOT/name
    assert sha(p)==expected,(name,'outer hash')
    data=json.loads(p.read_text()); got={}
    for rel,want in data['files'].items():
        f=ROOT/rel
        assert f.is_file() and not f.is_symlink(),(name,rel,'missing/symlink')
        assert sha(f)==want,(name,rel,'hash')
        if 'file_sizes' in data: assert f.stat().st_size==data['file_sizes'][rel],(name,rel,'size')
        got[rel]={'sha256':sha(f),'bytes':f.stat().st_size}
    return data,got

def preflight():
    d=OWN/'preflight-001'; d.mkdir(exist_ok=False)
    shutil.copyfile(__file__,d/'executed-review.py')
    proof,files=members('reviews/proof-freeze.json','72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251')
    statement,sfiles=members('reviews/statement-freeze.json',proof['frozen_statement_sha256'])
    assert len(files)==1800 and len(sfiles)==733
    assert sha(ROOT/'verification/proof-start.json')==proof['proof_start_sha256']
    assert sha(ROOT/'NLA/IE05/Proof.lean')=='f8ef9d1901845439e7c09f4e9d004eb49d87ed28d8a6d5'+'67d48ac4d16199a950'
    assert sha(ROOT/'Solution.lean')=='3e12274c074f9d221230bd3939a76d433532b067c7123a12effe2b9e6f6a5c9a'
    save(d/'frozen-members.json',files)
    save(d/'statement-members.json',sfiles)
    inventory=json.loads((ROOT/'verification/original-source-inventory.json').read_text())
    assert inventory['base']==proof['base'] and len(inventory['files'])==27
    batch=''.join(inventory['base']+':'+p+'\n' for p in inventory['files']).encode()
    raw=run(d,'original-git-objects',['git','-C',GITROOT,'cat-file','--batch'],stdin=batch)
    offset=0; originals={}
    for p,v in inventory['files'].items():
        end=raw.index(b'\n',offset); h=raw[offset:end].decode().split(); offset=end+1
        assert len(h)==3 and h[1]=='blob',(p,h)
        size=int(h[2]); content=raw[offset:offset+size]; offset+=size
        assert raw[offset:offset+1]==b'\n'; offset+=1
        f=ROOT/proof['source_snapshot_directory']/p
        assert h[0]==v['git_blob']==proof['source_git_blobs'][p]
        assert size==v['bytes']==len(content)==f.stat().st_size
        digest=hashlib.sha256(content).hexdigest()
        assert digest==v['sha256']==proof['source_files'][p]==sha(f)
        assert content==f.read_bytes()
        originals[p]={'git_blob':h[0],'sha256':digest,'bytes':size,'base':inventory['base']}
    assert offset==len(raw)
    save(d/'originals.json',originals)
    packages=json.loads((ROOT/'lake-manifest.json').read_text())['packages']; pins=[]; built=[]
    for spec in packages:
        p=PACKAGES/spec['name']
        head=run(d,'pin-'+spec['name'],['git','-C',p,'rev-parse','HEAD']).decode().strip()
        assert head==spec['rev'],(spec['name'],head,spec['rev'])
        diff=run(d,'diff-'+spec['name'],['git','-C',p,'diff','--no-ext-diff','--name-only','HEAD','--']).decode()
        assert not diff,(spec['name'],'modified tracked sources',diff)
        lib=p/'.lake/build/lib/lean'
        if lib.is_dir(): built.append(str(lib.resolve()))
        pins.append({'name':spec['name'],'source':str(p.resolve()),'rev':head,
                     'built_path':str(lib.resolve()) if lib.is_dir() else None})
    assert len(pins)==10 and len(built)==9
    version=run(d,'lean-version',[LEAN,'--version']).decode().strip()
    assert '4.33.1' in version
    run(d,'lean-help',[LEAN,'--help'])
    save(d/'pins.json',{'packages':pins,'built_paths':built,'lean_executable':str(LEAN),
        'lean_executable_sha256':sha(LEAN),'lean_version':version,'platform':platform.platform()})
    save(d/'result.json',{'status':'PASS','utc':utc(),'proof_members':1800,'statement_members':733,
        'original_git_paths':27,'source_pins':10,'built_paths':9,'proof_freeze_sha256':sha(ROOT/'reviews/proof-freeze.json')})
    print('Preflight PASS: 1800 proof members, 733 statement members, 27 original Git paths, 10 pins, 9 dependency paths',flush=True)

def build():
    d=OWN/'attempt-001'; d.mkdir(exist_ok=False)
    shutil.copyfile(__file__,d/'executed-review.py')
    prefix=d/'objects'; prefix.mkdir(); assert not list(prefix.iterdir())
    save(d/'initial-prefix.json',{'path':str(prefix),'contents':[],'utc':utc()})
    pins=json.loads((OWN/'preflight-001/pins.json').read_text())
    env={'LEAN_PATH':os.pathsep.join([str(prefix)]+pins['built_paths'])}
    sources=['NLA/IE05/'+m+'.lean' for m in ORDER]+['Solution.lean']; objects={}; snapshots={}
    for i,rel in enumerate(sources,1):
        f=ROOT/rel; dest=d/'source'/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(f,dest)
        assert sha(dest)==sha(f)
        snapshots[rel]={'sha256':sha(dest),'bytes':dest.stat().st_size}
        save(d/'source-manifest.json',snapshots)
        out=prefix/Path(rel).with_suffix('.olean'); out.parent.mkdir(parents=True,exist_ok=True)
        argv=[LEAN,'-R',ROOT,'-o',out,f]
        print('Compiling',rel,flush=True)
        run(d,f'{i:02d}-'+Path(rel).stem,argv,env)
        for obj in sorted(prefix.rglob('*')):
            if obj.is_file(): objects[str(obj.relative_to(prefix))]={'sha256':sha(obj),'bytes':obj.stat().st_size}
        save(d/'objects.json',objects)
        assert sha(f)==snapshots[rel]['sha256'],(rel,'changed during compile')
    save(d/'build-result.json',{'status':'PASS','commands':13,'source_count':13,'source_manifest_sha256':sha(d/'source-manifest.json'),
        'objects_manifest_sha256':sha(d/'objects.json'),'utc':utc(),'environment':env})
    print('All 12 final modules and Solution compiled from direct source',flush=True)

if __name__=='__main__':
    {'preflight':preflight,'build':build}[sys.argv[1]]()
