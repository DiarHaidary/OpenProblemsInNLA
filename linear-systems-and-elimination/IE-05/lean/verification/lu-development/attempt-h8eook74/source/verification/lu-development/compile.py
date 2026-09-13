#!/usr/bin/env python3
"""Fresh authorized LU trajectory helper source check. No Lake, network, or shared-cache writes.
Derived from the retained IE05 statement runner; raw source attempts are independent
and no Challenge/reference module is imported into proof checks. Not Linux Comparator.
"""
from __future__ import annotations
import datetime, hashlib, json, os, pathlib, platform, shutil, subprocess, tempfile, time, sys

PROJECT = pathlib.Path(__file__).resolve().parents[2]
EVIDENCE = PROJECT / 'verification/lu-development'
PACKAGES = pathlib.Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
TOOLCHAIN = pathlib.Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
ORDER = ['Cli', 'batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph',
         'LeanSearchClient', 'plausible', 'mathlib', 'leancert']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def pins():
    result = []
    manifest = json.loads((PROJECT/'lake-manifest.json').read_text())
    assert len(manifest['packages']) == 10
    for package in manifest['packages']:
        path = PACKAGES / package['name']
        head = subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'], text=True).strip()
        dirty = subprocess.check_output(['git','-C',str(path),'status','--porcelain','--untracked-files=no'], text=True)
        assert head == package['rev'] and not dirty, (package['name'], head, dirty)
        built = (path/'.lake/build/lib/lean').is_dir()
        # Cli is a Lake/tooling dependency and is not imported by these modules.
        # Do not pretend it has cached objects; no build is launched for it.
        assert built or package['name']=='Cli'
        result.append({'name':package['name'],'rev':head,'tracked_clean':True,
                       'compiled_artifact_directory_present':built})
    return result

def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    attempt = pathlib.Path(tempfile.mkdtemp(prefix='attempt-', dir=EVIDENCE))
    prefix = pathlib.Path(tempfile.mkdtemp(prefix='nla-ie05-lu-',dir='/tmp'))
    snapshot = attempt/'source'; snapshot.mkdir()
    modules=['NLA/IE05/Definitions.lean','NLA/IE05/Pivot.lean','NLA/IE05/LUTrajectory.lean']
    if len(sys.argv)>1 and sys.argv[1]=='Inspect':
        modules.append('verification/lu-development/Inspect.lean')
    sources=modules+['lean-toolchain','lakefile.toml','lake-manifest.json','comparator.json',
                     'verification/proof-start.json','verification/lu-development/compile.py']
    inputs = {}
    for rel in sources:
        src=PROJECT/rel; dst=snapshot/rel
        dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        inputs[rel]={'sha256':sha(src),'bytes':src.stat().st_size}
    result={'phase':'authorized LU trajectory helper author check','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'platform':platform.platform(),'project':str(PROJECT),'prefix':str(prefix),
            'inputs':inputs,'commands':[],
            'authoritative_linux_comparator':False,'independent_review':False}
    env=os.environ.copy()
    env['LEAN_PATH']=os.pathsep.join([str(prefix)]+[str(PACKAGES/x/'.lake/build/lib/lean') for x in ORDER]+[str(TOOLCHAIN/'lib/lean')])
    env['PATH']=str(TOOLCHAIN/'bin')+os.pathsep+env.get('PATH','')
    result['lean_path']=env['LEAN_PATH']
    result['toolchain_version']=subprocess.check_output([str(TOOLCHAIN/'bin/lean'),'--version'],text=True).strip()
    try:
        freeze=json.loads((PROJECT/'reviews/statement-freeze.json').read_text())
        assert len(freeze['files'])==733
        for rel,h in freeze['files'].items():assert sha(PROJECT/rel)==h,rel
        result['frozen_inputs_before']=len(freeze['files'])
        result['pins_before']=pins()
        handoffs=[]
        for mrel, base, expected in [
            ('verification/gepp-development/EVIDENCE-MANIFEST.json', PROJECT, 150),
            ('verification/qr-scaling-handoff/EVIDENCE-MANIFEST.json', PROJECT/'verification/qr-scaling-handoff', 847)]:
            manifest=json.loads((PROJECT/mrel).read_text()); assert len(manifest['files'])==expected
            for r,d in manifest['files'].items():assert sha(base/r)==d['sha256'],r
            handoffs.append({'manifest':mrel,'sha256':sha(PROJECT/mrel),'verified_files':expected})
        result['imported_handoffs']=handoffs
        for rel in modules:
            out=prefix/pathlib.Path(rel).with_suffix('.olean'); out.parent.mkdir(parents=True,exist_ok=True)
            cmd=[str(TOOLCHAIN/'bin/lean'),'-o',str(out),'-i',str(out.with_suffix('.ilean')),rel]
            start=time.monotonic()
            cp=subprocess.run(cmd,cwd=snapshot,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=240)
            log=attempt/(pathlib.Path(rel).stem+'.log');log.write_text(cp.stdout)
            result['commands'].append({'source':rel,'argv':cmd,'exit_code':cp.returncode,
                                       'elapsed_seconds':time.monotonic()-start,'log':log.name,'log_sha256':sha(log)})
            print(json.dumps(result['commands'][-1]),flush=True)
            if cp.returncode:
                break
        result['pins_after']=pins()
        for rel,h in freeze['files'].items():assert sha(PROJECT/rel)==h,rel
        result['frozen_inputs_after']=len(freeze['files'])
        result['source_unchanged']=all(sha(PROJECT/r)==v['sha256'] for r,v in inputs.items())
        result['pass']=len(result['commands'])==len(modules) and all(c['exit_code']==0 for c in result['commands']) and result['source_unchanged']
    finally:
        generated={str(p.relative_to(prefix)):{'sha256':sha(p),'bytes':p.stat().st_size}
                   for p in prefix.rglob('*') if p.is_file()}
        result['removed_own_objects']=generated
        assert prefix.parent==pathlib.Path('/tmp') and prefix.name.startswith('nla-ie05-lu-')
        shutil.rmtree(prefix)
        result['own_prefix_removed']=not prefix.exists()
        (attempt/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        (EVIDENCE/'latest.json').write_text(json.dumps({'attempt':attempt.name,'result_sha256':sha(attempt/'result.json')},indent=2)+'\n')
    print(json.dumps({'attempt':str(attempt),'pass':result.get('pass',False)}),flush=True)
    raise SystemExit(0 if result.get('pass') else 1)

if __name__=='__main__':main()
