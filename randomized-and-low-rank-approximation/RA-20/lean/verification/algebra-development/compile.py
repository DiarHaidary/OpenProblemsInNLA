#!/usr/bin/env python3
"""Direct source elaboration; dependency objects are read-only and every attempt is retained."""
import datetime, hashlib, json, os, pathlib, subprocess, sys, time
P = pathlib.Path(__file__).resolve().parents[2]
E = pathlib.Path(__file__).resolve().parent
A = json.loads((E / 'gate-acknowledged.json').read_text())
O = pathlib.Path(A['prefix'])
L = pathlib.Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
C = pathlib.Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
order = ['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
env = os.environ.copy()
env['LEAN_PATH'] = ':'.join(map(str, [O, *[C / n / '.lake/build/lib/lean' for n in order], L / 'lib/lean']))
source = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'NLA/RA20/Algebra.lean')
attempt = E / ('attempt-%03d' % (1 + len(list(E.glob('attempt-*')))))
attempt.mkdir()
b = (P / source).read_bytes()
(attempt / source.name).write_bytes(b)
out = O / source.with_suffix('')
out.parent.mkdir(parents=True, exist_ok=True)
cmd = [str(L / 'bin/lean'), '-o', str(out.with_suffix('.olean')), '-i', str(out.with_suffix('.ilean')), str(source)]
record = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source': str(source), 'sha256': hashlib.sha256(b).hexdigest(), 'command': cmd, 'cwd': str(P), 'LEAN_PATH': env['LEAN_PATH']}
(attempt / 'command.json').write_text(json.dumps(record, indent=2) + '\n')
start = time.monotonic()
with (attempt / 'lean.log').open('wb') as f:
    result = subprocess.run(cmd, cwd=P, env=env, stdout=f, stderr=subprocess.STDOUT)
record.update(exit_code=result.returncode, seconds=time.monotonic()-start)
(attempt / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
(E / 'latest.json').write_text(json.dumps({'attempt': str(attempt), **record}, indent=2) + '\n')
print((attempt / 'lean.log').read_text())
print(json.dumps({'attempt': str(attempt), 'exit_code': result.returncode, 'seconds': record['seconds']}))
sys.exit(result.returncode)
