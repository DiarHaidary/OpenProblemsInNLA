# Exact read-only Python bodies from the initial tool inspection probes.
# Historical transcript only. Do not execute sequentially: the first and third
# probes intentionally show the exceptions observed before the corrected reads.

# Probe 1: executed before any reviewer file existed.
from pathlib import Path
import json,hashlib
K=Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean')
a=json.loads((K/'DRAFT-INVENTORY.json').read_text())
print(json.dumps({k:v for k,v in a.items() if k!='files'},indent=2))
print(json.dumps(a['files'][:3],indent=2))
print('Actual files',sum(p.is_file() for p in K.rglob('*')))
print('Free bytes',__import__('shutil').disk_usage(K).free)

# Probe 2: corrected shape inspection, also before any reviewer write.
from pathlib import Path
import json,hashlib,shutil
K=Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean')
a=json.loads((K/'DRAFT-INVENTORY.json').read_text())
print(type(a['files']).__name__)
print(json.dumps(list(a['files'].items())[:3],indent=2))
print('Actual files',sum(p.is_file() for p in K.rglob('*')))
print('Free bytes',shutil.disk_usage(K).free)

# Probe 3: later read incorrectly assumed a nonempty failed historical manifest.
from pathlib import Path
import json
K=Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean')
for name in ['verification/api-evidence-final/manifest.json','verification/statement-development/attempt-r5fn2nl_/result.json','verification/statement-development/attempt-xrn2jug1/result.json']:
 a=json.loads((K/name).read_text()); print(name, json.dumps({k:(f'{len(v)} entries' if isinstance(v,(list,dict)) else v) for k,v in a.items()},indent=2));
 if 'files' in a: print('firstfile',json.dumps(next(iter(a['files'].items())) if isinstance(a['files'],dict) else a['files'][0],indent=2))
