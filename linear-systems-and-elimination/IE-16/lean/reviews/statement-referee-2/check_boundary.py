from pathlib import Path
import hashlib, json, re, subprocess
from fractions import Fraction as Q
import yaml, jsonschema

HERE = Path(__file__).resolve().parent
P = Path('/tmp/nla-lean-ie16-project/linear-systems-and-elimination/IE-16/lean')
REPO = Path('/tmp/nla-lean-sp06-worktree')
REV = 'b73cd1804e40e0d101294eedb156984f0d62b4a6'
sha = lambda b: hashlib.sha256(b).hexdigest()
checks = {}
inventory = json.loads((P/'verification/STATEMENT_HASHES.json').read_text())
checks['statement_hashes'] = {}
for name, digest in inventory['files'].items():
    actual = sha((P/name).read_bytes())
    assert actual == digest, name
    checks['statement_hashes'][name] = actual
source_paths = {
 'canonical-README.md': 'linear-systems-and-elimination/IE-16/README.md',
 'canonical-problem.tex': 'linear-systems-and-elimination/IE-16/problem.tex',
 'holden-solution.tex': 'references/holden-ie16-2026-09-12/submitted/source/solution.tex',
 'holden-submission.md': 'references/holden-ie16-2026-09-12/submitted/README.md',
 'verify.py': 'references/holden-ie16-2026-09-12/submitted/code/verify.py',
 'all_subset_certificate.json': 'references/holden-ie16-2026-09-12/submitted/certificates/all_subset_certificate.json',
}
checks['upstream_source_identity'] = {}
for name, path in source_paths.items():
    blob = subprocess.check_output(['git','show',f'{REV}:{path}'], cwd=REPO)
    assert blob == (P/'verification/source-snapshot'/name).read_bytes(), name
    checks['upstream_source_identity'][path] = sha(blob)
defs = (P/'NLA/IE16/Definitions.lean').read_text()
challenge = (P/'Challenge.lean').read_text()
aggregate = (P/'verification/bounded-recheck-input/All.lean').read_text()
assert aggregate == defs + '\n' + challenge.replace('import NLA.IE16.Definitions\n\n', '', 1)
assert aggregate == Path('/tmp/nla-lean-ie16-project/recheck/All.lean').read_text()
record = json.loads((P/'verification/bounded-statement-recheck-result.json').read_text())
assert record['exit_code'] == 0 and record['lean_memory_limit_mb'] == 2048
assert record['threads'] == 1 and record['wall_time_limit_seconds'] == 90
assert record['command'][1:5] == ['-M','2048','-j','1']
original_log = Path(record['log'])
assert original_log.read_bytes() == (P/'verification/bounded-statement-recheck-lean.log').read_bytes()
assert original_log.with_name('result.json').read_bytes() == (P/'verification/bounded-statement-recheck-result.json').read_bytes()
assert original_log.read_text().count('declaration uses `sorry`') == 15
assert 'error:' not in original_log.read_text()
checks['bounded_aggregate'] = {'sha256':sha(aggregate.encode()), 'result':record,
 'original_raw_log_sha256':sha(original_log.read_bytes()),
 'independent_compiler_run':False}
names = ['NLA.IE16.'+n for n in re.findall(r'^theorem (\w+)', challenge, re.M)]
metadata = yaml.safe_load((P/'formalization.yaml').read_text())
config = json.loads((P/'comparator.json').read_text())
assert len(names) == 15 and names == config['theorem_names']
assert names == [v['declaration'] for v in metadata['status']['main_results']]
assert re.findall(r'\bsorry\b', re.sub(r'/\-.*?\-/','',defs,flags=re.S)) == []
schema_path = Path('/tmp/nla-lean-formalization/standards/sources/mathlib-initiative/formalization.yaml/schema/v0.4.schema.json')
schema = json.loads(schema_path.read_text())
jsonschema.validate(metadata, schema)
checks['coverage'] = names
checks['schema'] = {'status':'PASS','sha256':sha(schema_path.read_bytes())}
e = Q(1,1000)
D = 1+e+3*e**2+e**3+e**4
m = 3*e*(1+e+e**2)/D
lower = Q(299,100000)
upper = Q(23,10000)
assert m == Q(3003003000,1001003001001) and m > lower
coarse_upper = e*(9+36*e+36*e**2+16*e**3)/(4*(1-e)**4)
assert coarse_upper < upper
assert lower/upper == Q(13,10)
assert Q(4)/Q(31,10) < Q(13,10)
checks['exact_scalar_checks'] = {k:str(v) for k,v in dict(epsilon=e,denominator=D,
 full_value=m,full_lower=lower,coarse_subset_upper=coarse_upper,
 subset_upper=upper,ratio_lower=lower/upper).items()}
checks['limits'] = 'Source and statement review only; no independent Lean run, proof, Comparator, or Linux result.'
(HERE/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
print('PASS: 36 hashes; six exact upstream blobs; unchanged aggregate; bounded raw records; 15 contracts; schema; exact scalar checks.')
