"""Independent local final review commands; no candidate edits or dependency builds."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
PROJECT = Path('/tmp/nla-lean-is02-project/eigenvalues-and-inverse-problems/IS-02/lean')
DEPS = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
SYSROOT = Path.home()/'.elan/toolchains/leanprover--lean4---v4.33.1'
REPO = Path('/tmp/nla-lean-ke04-worktree')
BASE = '50838e37dd793830e2cecd1055cfc7e0349490f1'
record = {'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'phase':'independent final proof review on macOS', 'commands':[]}

def run(args, *, cwd=ROOT, env=None, log=None):
    args = [str(a) for a in args]
    r = subprocess.run(args,cwd=cwd,env=env,capture_output=True)
    item = {'argv':args,'cwd':str(cwd),'exit_code':r.returncode,
            'stdout':r.stdout.decode(),'stderr':r.stderr.decode()}
    record['commands'].append(item)
    if log: (ROOT/log).write_bytes(r.stdout+r.stderr)
    (ROOT/'command-results.json').write_text(json.dumps(record,indent=2)+'\n')
    if r.returncode: raise RuntimeError(item)
    return r.stdout

snapshot = {}
for f in sorted(PROJECT.rglob('*')):
    if f.is_file():
        rel = f.relative_to(PROJECT)
        raw = f.read_bytes()
        dest = ROOT/'candidate'/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(raw)
        snapshot[str(rel)] = hashlib.sha256(raw).hexdigest()
(ROOT/'candidate-hashes.json').write_text(json.dumps(snapshot,indent=2)+'\n')
assert snapshot['NLA/IS02/Proof.lean'] == 'f108eb9d89a524514bd24b6cc379bc500b03d00143b49b14938aa75cbe72bde8'
assert snapshot['Solution.lean'] == '8cf1db571f72a181107bd5cbea8910bc2fd4ff6266bbea2218783ea88cdba545'
freeze = json.loads((PROJECT/'reviews/statement-freeze.json').read_text())
for f, sha in freeze['frozen_statement_files'].items(): assert snapshot[f] == sha
for review in freeze['reviewers']: assert snapshot[review['report']] == review['report_sha256']
source_hashes={}
for rel in ['eigenvalues-and-inverse-problems/IS-02/README.md',
            'eigenvalues-and-inverse-problems/IS-02/problem.tex',
            'eigenvalues-and-inverse-problems/IS-02/solution.md',
            'eigenvalues-and-inverse-problems/IS-02/solution.tex',
            'docs/lean/REVIEW.md','docs/lean/schema/v0.4.schema.json']:
    raw = run(['git','-C',REPO,'show',BASE+':'+rel])
    dest = ROOT/'source'/rel
    dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(raw)
    source_hashes[rel] = hashlib.sha256(raw).hexdigest()
(ROOT/'source-hashes.json').write_text(json.dumps(source_hashes,indent=2)+'\n')

manifest = json.loads((PROJECT/'lake-manifest.json').read_text())
deps={}
for pkg in manifest['packages']:
    name = pkg['name']; directory = DEPS/name
    head = run(['git','rev-parse','HEAD'],cwd=directory).decode().strip()
    status = run(['git','status','--porcelain=1','--untracked-files=no'],cwd=directory)
    assert head == pkg['rev'] and status == b'', name
    deps[name] = {'revision':head,'tracked_sources_clean':True}
record['dependencies'] = deps
assert len(deps)==10
env=os.environ.copy()
env['IS02_DEP_ROOT']=str(DEPS)
env['LEAN_BIN']=str(SYSROOT/'bin/lean')
env['LEAN_SYSROOT']=str(SYSROOT/'lib/lean')
private=Path(tempfile.mkdtemp(prefix='nla-is02-final-referee1-objects-'))
env['IS02_TYPECHECK_TMPDIR']=str(private)
record['proof_run_environment']={k:env[k] for k in ['IS02_DEP_ROOT','LEAN_BIN','LEAN_SYSROOT','IS02_TYPECHECK_TMPDIR']}
run(['bash','-x',PROJECT/'verification/proof-typecheck.sh'],cwd=PROJECT,env=env,log='proof-typecheck.log')
prefixes=list(private.glob('nla-is02-proof-typecheck.*'))
assert len(prefixes)==1
record['private_output_prefix']=str(prefixes[0])
record['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
record['result']='PASS: local direct proof build and nine LeanCert kernel trust assertions'
(ROOT/'command-results.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'result':record['result'],'private_output_prefix':str(prefixes[0])}))
