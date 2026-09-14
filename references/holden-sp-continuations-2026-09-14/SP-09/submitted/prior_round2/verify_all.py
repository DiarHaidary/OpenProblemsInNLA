"""Run every proof-critical checker from this extracted archive.

Optional reports are written only to the explicitly requested report directory.
The default command prints its results and leaves proof files unchanged.
"""
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,time

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report-dir',type=Path);p.add_argument('--skip-hash-check',action='store_true');a=p.parse_args();root=Path(__file__).resolve().parent;rows=[]
 manifest=root/'SHA256SUMS.txt'
 if manifest.exists() and not a.skip_hash_check:
  checked=0
  for line in manifest.read_text().splitlines():
   if not line.strip():continue
   digest,name=line.split('  ',1);path=(root/name).resolve()
   if not path.is_relative_to(root) or not path.is_file():raise ValueError('Invalid manifest path: '+name)
   if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('SHA-256 mismatch: '+name)
   checked+=1
  print(f'PASS: {checked} file hashes match the manifest.',flush=True)
 checks=[
  'prior/certificate/verify_certificate.py',
  'prior/certificate/verify_witness_and_rigidity.py',
  'prior/certificate/test_verifiers.py',
  'new_results/certificate/local_geometry.py',
  'new_results/certificate/rank_witness.py',
  'new_results/certificate/exact_minor.py',
  'new_results/certificate/quantitative_rigidity.py',
  'new_results/certificate/test_new_certificates.py',
 ]
 if a.report_dir:a.report_dir.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ);env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1'
 for i,script in enumerate(checks):
  start=time.monotonic();r=subprocess.run([sys.executable,'-O',str(root/script)],cwd=root,env=env,text=True,capture_output=True);elapsed=time.monotonic()-start
  print('\n=== '+script+' ===\n'+r.stdout,end='',flush=True)
  if r.stderr:print(r.stderr,file=sys.stderr)
  row={'script':script,'returncode':r.returncode,'elapsed_seconds':elapsed,'result':'PASS' if r.returncode==0 else 'FAIL'};rows.append(row)
  if a.report_dir:(a.report_dir/f'{i+1:02d}_{Path(script).stem}.log').write_text(r.stdout+r.stderr)
  if r.returncode!=0:raise RuntimeError('Verification failed: '+script)
 result={'result':'PASS','python':sys.version,'checks':rows,'scope':'Local amplification invariance and reference quantitative rigidity, not universal SP-09.'}
 if a.report_dir:(a.report_dir/'all_checks.json').write_text(json.dumps(result,indent=2)+'\n')
 print('\nALL EXACT CHECKS PASSED. Universal SP-09 is not claimed solved.',flush=True)
if __name__=='__main__':main()
