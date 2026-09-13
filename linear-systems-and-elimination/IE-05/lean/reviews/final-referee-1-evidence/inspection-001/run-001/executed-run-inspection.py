from pathlib import Path
import importlib.util, os, sys, shutil
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review',HERE/'review.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
src=HERE/'inspection-001'
attempt=src/sys.argv[1]; attempt.mkdir(exist_ok=False)
shutil.copyfile(__file__,attempt/'executed-run-inspection.py')
prefix=HERE/'attempt-001/objects'
pins=r.json.loads((HERE/'preflight-001/pins.json').read_text())
env={'LEAN_PATH':os.pathsep.join([str(prefix)]+pins['built_paths'])}
before={str(p.relative_to(prefix)):{'sha256':r.sha(p),'bytes':p.stat().st_size} for p in prefix.rglob('*') if p.is_file()}
r.save(attempt/'objects-before.json',before)
for i,name in enumerate(['RefereeReference','RefereeInspect'],1):
    f=src/(name+'.lean'); snap=attempt/(name+'.lean'); shutil.copyfile(f,snap)
    r.save(attempt/(name+'-source.json'),{'path':str(f),'sha256':r.sha(f),'bytes':f.stat().st_size})
    print('Compiling inspector source',name,flush=True)
    r.run(attempt,f'{i:02d}-'+name,[r.LEAN,'-R',src,'-o',prefix/(name+'.olean'),f],env)
after={str(p.relative_to(prefix)):{'sha256':r.sha(p),'bytes':p.stat().st_size} for p in prefix.rglob('*') if p.is_file()}
r.save(attempt/'objects-after.json',after)
for p,v in before.items():
    if not p.startswith('Referee'):
        assert after[p]==v,(p,'final proof object changed')
shutil.copyfile(src/'actual-environment.json',attempt/'actual-environment.json')
r.save(attempt/'result.json',{'status':'PASS','utc':r.utc(),'actual_environment_sha256':r.sha(attempt/'actual-environment.json')})
print('Inspector completed',flush=True)
