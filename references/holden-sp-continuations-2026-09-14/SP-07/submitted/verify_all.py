#!/usr/bin/env python3
"""Run delivered checks; standard-library checks are the default.

--numerical adds NumPy/SciPy/SymPy diagnostics, which are not proof certificates.
--prior reruns the retained rank-one certificate and the inherited n=193 pair;
this is slower and uses temporary extraction without modifying the old archive.
"""
from pathlib import Path
import argparse,json,os,subprocess,sys,tempfile,time,zipfile
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True

def safe_extract(path,destination):
    destination=Path(destination).resolve()
    with zipfile.ZipFile(path) as z:
        for item in z.infolist():
            target=(destination/item.filename).resolve()
            if destination!=target and destination not in target.parents:
                raise ValueError('Unsafe archive member')
        bad=z.testzip()
        if bad:raise ValueError('Corrupt archive member: '+bad)
        z.extractall(destination)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--numerical',action='store_true');p.add_argument('--prior',action='store_true')
    p.add_argument('--output',type=Path);a=p.parse_args();begin=time.perf_counter();rows=[]
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    def run(label,cmd,cwd=ROOT):
        print('\n=== '+label+' ===',flush=True);t=time.perf_counter()
        result=subprocess.run(cmd,cwd=cwd,env=env)
        rows.append({'name':label,'command':cmd,'returncode':result.returncode,'seconds':time.perf_counter()-t})
        if result.returncode:raise RuntimeError(label+' failed')
    py=sys.executable
    run('Exact all-odd-order polygon formulas',[py,'-S','verify_polygon.py'])
    run('Rational stationary-model enclosure',[py,'-S','verify_model.py'])
    run('Exact and corrupted-input rejection tests',[py,'-S','-m','unittest','discover','-s','tests','-p','test_exact.py','-v'])
    run('Rejection tests with Python optimization enabled',[py,'-S','-O','-m','unittest','discover','-s','tests','-p','test_exact.py','-v'])
    if a.numerical:
        run('Numerical regression diagnostics',[py,'-m','unittest','discover','-s','tests','-p','test_numerical.py','-v'])
        run('Separate symbolic reconstruction',[py,'src/symbolic_audit.py'])
        with tempfile.TemporaryDirectory(prefix='sp07-model-') as tmp:
            run('Stationary-model numerical exploration',[py,'research/stationary_fit.py','--optimize','--output',str(Path(tmp)/'fit.json')])
    if a.prior:
        with tempfile.TemporaryDirectory(prefix='sp07-prior-') as tmp:
            tmp=Path(tmp);safe_extract(ROOT/'prior/SP-07_round4_sharp_subclass.zip',tmp/'r4')
            r4=tmp/'r4/SP-07_round4_release'
            run('Inherited rank-one exact certificate',[py,'-S','verify_rank_one.py'],r4)
            run('Inherited rank-one exact rejection tests',[py,'-S','-m','unittest','discover','-s','tests','-p','test_exact.py','-v'],r4)
            safe_extract(r4/'prior/SP-07_round3_certified_progress.zip',tmp/'r3')
            r3=tmp/'r3/SP-07_round3_bundle'
            run('Inherited n=193 certificate by both exact positivity methods',
                [py,'-S','verify_all.py','--only','n193','--ldl'],r3)
    out={'status':'PASS','all_passed':True,'steps':rows,'seconds':time.perf_counter()-begin,
         'numerical_enabled':a.numerical,'inherited_checks_enabled':a.prior}
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
    print('\nPASS all requested checks.',flush=True)
if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError,zipfile.BadZipFile) as exc:
        print('VERIFICATION FAILED: '+str(exc),file=sys.stderr);raise SystemExit(1)
