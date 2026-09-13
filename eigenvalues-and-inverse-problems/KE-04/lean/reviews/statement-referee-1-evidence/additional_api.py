#!/usr/bin/env python3
"""Independent source binding for the precise symmetry/finite-dimension bridges."""
from pathlib import Path
import hashlib, json, os, subprocess
E=Path(__file__).resolve().parent
M=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages/mathlib')
P='0df444a360eaa60ab8c11dca51a86af692955474'
OUT=E/'additional-api'
OUT.mkdir(exist_ok=False)
rows=[]
for i,path in enumerate(['Mathlib/Analysis/Matrix/Hermitian.lean','Mathlib/LinearAlgebra/FiniteDimensional/Defs.lean','Mathlib/LinearAlgebra/Dimension/Finrank.lean']):
    argv=['git','show',P+':'+path]
    r=subprocess.run(argv,cwd=M,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),capture_output=True)
    (OUT/f'{i}.stdout').write_bytes(r.stdout)
    (OUT/f'{i}.stderr').write_bytes(r.stderr)
    assert r.returncode==0 and r.stdout==(M/path).read_bytes()
    b=r.stdout
    rows.append({'argv':argv,'cwd':str(M),'exit_code':r.returncode,'source':path,'commit':P,'stdout':f'{i}.stdout','stderr':f'{i}.stderr','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
(OUT/'result.json').write_text(json.dumps({'success':True,'files':rows},indent=2)+'\n')
print('ADDITIONAL_API_PASS',len(rows))
