#!/usr/bin/env python3
"""Run one pinned local Lean process with bounded memory and wall time.

Local development only. Authoritative Linux verification uses the repository
harness on GitHub. Every local agent must use this wrapper instead of Lean/Lake.
"""
from pathlib import Path
import fcntl
import json
import os
import subprocess
import sys
import tempfile
import time

binary = '/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean'
args = sys.argv[1:]
if any(a.startswith(('-M', '--memory', '-j', '--threads')) for a in args):
    raise SystemExit('Local memory/thread limits are fixed by the shared wrapper.')
lock = open('/tmp/nla-lean-formalization/local-compiler.lock', 'a+')
try:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    raise SystemExit('Another local compiler is running; do not start a second one.')
prefix = Path(tempfile.mkdtemp(prefix='nla-bounded-lean-'))
log = prefix / 'lean.log'
command = [binary, '-M', '2048', '-j', '1', *args]
record = {'command': command, 'cwd': os.getcwd(), 'lean_memory_limit_mb': 2048,
          'wall_time_limit_seconds': 90, 'threads': 1, 'log': str(log)}
started = time.monotonic()
with log.open('w') as output:
    process = subprocess.Popen(command, stdout=output, stderr=subprocess.STDOUT)
    record['pid'] = process.pid
    try:
        code = process.wait(timeout=90)
    except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
        record['interrupted_reason'] = type(error).__name__
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        code = 124 if isinstance(error, subprocess.TimeoutExpired) else 130
record.update(exit_code=code, elapsed_seconds=time.monotonic() - started)
(prefix / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
print(log.read_text()[-12000:], end='')
print(f'Bounded local Lean exit={code}; evidence: {prefix}')
raise SystemExit(code if code >= 0 else 128 - code)
