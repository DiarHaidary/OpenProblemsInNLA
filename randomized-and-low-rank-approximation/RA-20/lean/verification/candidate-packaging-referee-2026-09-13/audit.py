#!/usr/bin/env python3
"""Independent fixed-byte RA20 candidate metadata/evidence audit; no Lean/Linux execution."""
import datetime, hashlib, importlib.util, json, os, pathlib, re, subprocess, time, urllib.parse
import yaml

E = pathlib.Path(__file__).resolve().parent
P = E.parents[1]
G = P.parents[2]
A = P / 'verification/linux-candidate-2026-09-13'
BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
OLD = '7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
NEW = '83e19faf1bf25a9748de40da3193cfd68690100923a50379553e288c45b5e8bc'
YAML = 'bec9d851e204464fa2d3e29033d5958034665d51c3554d2043f1470bfafd4197'
OUTER = '60f056cd293d2b093786a34e55b670975dd6b27e7e927acdbf8513438c28b381'
HANDOFF = 'b2277179cad1d686c684abe6f676fe9680e5510d26935f7c7a72205ba79db4ae'
GATE = 'a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb'
PY = '/tmp/nla-lean-formalization/venv/bin/python'

def digest(p):
    assert p.is_file() and not p.is_symlink(), p
    return hashlib.sha256(p.read_bytes()).hexdigest()

def unique(pairs):
    result = {}
    for k,v in pairs:
        assert k not in result, ('duplicate JSON key', k)
        result[k] = v
    return result

def load(p): return json.loads(p.read_text(), object_pairs_hook=unique)
def write(p, d): p.write_text(json.dumps(d, indent=2) + '\n')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def check(p, value, historic=False):
    expected = value if isinstance(value, str) else value['sha256']
    p = p.resolve()
    # There is exactly one permitted historical archive mapping, not a basename rule.
    if historic and p == (P / 'README.md').resolve() and expected == OLD:
        p = P / 'verification/pre-candidate-README.md'
    assert digest(p) == expected, p
    if isinstance(value, dict) and 'bytes' in value:
        assert p.stat().st_size == value['bytes'], p

command_number = 0
def command(args, cwd):
    global command_number
    command_number += 1
    d = E / ('command-%02d' % command_number)
    if d.exists():
        # Retain the first attempt's successful immutable-base Git receipts.
        assert command_number <= 16 and args[:2] == ['git', 'show']
        old = load(d/'result.json')
        assert old['command'] == args and old['cwd'] == str(cwd)
        assert old['exit_code'] == 0 and digest(d/'raw.log') == old['log_sha256']
        return (d/'raw.log').read_bytes()
    d.mkdir()
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['GIT_OPTIONAL_LOCKS'] = '0'
    record = {'utc': utc(), 'command': args, 'cwd': str(cwd),
              'environment_overrides': {'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0'}}
    write(d / 'command.json', record)
    start = time.monotonic()
    with (d / 'raw.log').open('wb') as f:
        proc = subprocess.run(args, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT)
    record.update(exit_code=proc.returncode, seconds=time.monotonic()-start,
                  log_sha256=digest(d / 'raw.log'))
    write(d / 'result.json', record)
    assert proc.returncode == 0, (d, (d/'raw.log').read_text())
    return (d/'raw.log').read_bytes()

# The installer explicitly released this exact sealed handoff before this script was written.
check(A/'HANDOFF.md', HANDOFF)
check(A/'EVIDENCE-MANIFEST.json', OUTER)
check(P/'README.md', NEW)
check(P/'formalization.yaml', YAML)
check(P/'verification/final-review-acceptance.json', GATE)
check(A/'preflight.json', 'a6540a7a937fc0298954cf5b508f0354881fec87e832f80f223773c6f9cd0210')
before = load(A/'preflight.json')['baseline']
assert len(before) == 958
for n,v in before.items(): check(P/n,v,historic=True)
assert [n for n,v in before.items() if digest(P/n) != v['sha256']] == ['README.md']
check(P/'verification/pre-candidate-README.md', OLD)

author = load(A/'EVIDENCE-MANIFEST.json')
assert author['file_count'] == len(author['files']) == 1010
assert author['project_files_excluding_outer'] == 992
assert author['live_original_and_check_tool_files'] == 18
assert author['own_evidence_files_excluding_outer'] == 32
for n,v in author['files'].items(): check(A/n,v)
bound = {(A/n).resolve() for n in author['files']}
author_own = {p.resolve() for p in A.rglob('*') if p.is_file() and p.resolve() != (A/'EVIDENCE-MANIFEST.json').resolve()}
assert {p for p in bound if p.is_relative_to(A)} == author_own
assert (A/'EVIDENCE-MANIFEST.json').resolve() not in bound
expected_project = {(P/n).resolve() for n in before}
expected_project |= {P/'formalization.yaml', P/'verification/pre-candidate-README.md'} | author_own
assert {p for p in bound if p.is_relative_to(P)} == expected_project

proof = load(P/'verification/proof-freeze.json')
statement = load(P/'reviews/statement-freeze.json')
assert len(proof['files']) == 521 and len(statement['files']) == 68
assert proof['source_files'] == statement['source_files']
assert proof['source_git_blobs'] == statement['source_git_blobs']
assert len(proof['source_files']) == 16
for f in [proof, statement]:
    for n,v in f['files'].items(): check(P/n,v,historic=True)
for n,h in proof['source_files'].items():
    check(G/n,h)
    check(P/'verification/original-sources'/n,h)
    original = command(['git','show',BASE+':'+n],G)
    assert hashlib.sha256(original).hexdigest() == h, n
    assert hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest() == proof['source_git_blobs'][n]
expected_external = {(G/n).resolve() for n in proof['source_files']}
expected_external |= {G/'tools/lean/validate_manifest.py', G/'tools/validate_problem_ids.py'}
assert bound - expected_project == expected_external

nested = []
for name in before:
    if name.endswith('EVIDENCE-MANIFEST.json') or name == 'reviews/statement-package-manifest.json':
        path = P/name
        m = load(path)
        parent = P if name == 'reviews/statement-package-manifest.json' else path.parent
        for n,v in m['files'].items(): check(parent/n,v,historic=True)
        nested.append({'file':name,'sha256':digest(path),'bound_files':len(m['files'])})
assert len(nested) == 14

gate = load(P/'verification/final-review-acceptance.json')
assert gate['canonical_status'] == 'Solved, unchanged'
assert gate['actual_Linux_Comparator'] == 'pending' and gate['publication'] == 'pending'
assert gate['reviewed_proof_freeze_sha256'] == digest(P/'verification/proof-freeze.json')
assert gate['statement_freeze_sha256'] == digest(P/'reviews/statement-freeze.json')
names = load(P/'comparator.json')['theorem_names']
reports = []
for i,r in enumerate(gate['reports'],1):
    check(P/r['report'],r['sha256'])
    check(P/r['evidence']['file'],r['evidence']['sha256'])
    assert len(load(P/r['evidence']['file'])['files']) == [699,793][i-1]
    assert r['exact_export_type_matches'] == names
    assert r['successful_fresh_source_commands'] == 13 and r['failed_Lean_commands'] == 0
    assert r['source_kernel_assertions'] == 61 and r['additional_kernel_assertions'] == 12
    assert r['actual_standard_three_reports'] == 69
    assert r['actual_project_closure'] == 214
    assert r['required_material_dependencies'] == [39,28][i-1]
    assert len(r['commands']) == 13 and len(r['axiom_reports']) == 69
    for c in r['commands']:
        check(P/c['source'],c['source_sha256'])
        check(P/c['log'],c['log_sha256'])
        assert c['exit_code'] == 0
    for ax in r['axiom_reports']:
        check(P/ax['log'],ax['log_sha256'])
        assert set(ax['axioms']) == {'propext','Classical.choice','Quot.sound'}
        log = (P/ax['log']).read_text()
        matching = re.findall("'"+re.escape(ax['name'])+r"' depends on axioms: \[([^\]]+)\]",log)
        assert matching and all(set(x.strip() for x in v.split(',')) == set(ax['axioms']) for v in matching)
    reports.append({k:r[k] for k in ['reviewer','report','sha256','evidence','successful_fresh_source_commands',
                    'actual_project_closure','required_material_dependencies','source_kernel_assertions',
                    'additional_kernel_assertions','actual_standard_three_reports']})

# Snapshot the concrete reviewed documents and policy/script bytes, only in our own directory.
snapshot = E/'snapshots'
snapshot.mkdir(exist_ok=True)
snapshots = {}
for source, name in [(P/'README.md','candidate-README.md'),(P/'formalization.yaml','candidate-formalization.yaml'),
                     (A/'HANDOFF.md','installer-HANDOFF.md'),
                     (G/'tools/lean/harness.py','harness.py'),(G/'tools/lean/HARNESS.md','HARNESS.md'),
                     (G/'tools/lean/verify.sh','verify.sh'),(G/'tools/lean/bootstrap.sh','bootstrap.sh'),
                     (G/'tools/lean/selftest.sh','selftest.sh'),
                     (G/'tools/lean/validate_manifest.py','validate_manifest.py'),
                     (G/'docs/lean/schema/v0.4.schema.json','v0.4.schema.json')]:
    if (snapshot/name).exists():
        assert (snapshot/name).read_bytes() == source.read_bytes()
    else:
        (snapshot/name).write_bytes(source.read_bytes())
    snapshots[str(source.relative_to(G))] = {'sha256':digest(source),'snapshot':str((snapshot/name).relative_to(P))}
if (E/'snapshots.json').exists():
    assert load(E/'snapshots.json') == snapshots
else:
    write(E/'snapshots.json',snapshots)

spec = importlib.util.spec_from_file_location('ra20_manifest_validator',G/'tools/lean/validate_manifest.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
meta = yaml.load((P/'formalization.yaml').read_text(),Loader=module.UniqueSafeLoader)
config = load(P/'comparator.json')
assert len(names) == 12 and config['definition_names'] == []
assert config['challenge_module'] == 'Challenge' and config['solution_module'] == 'Solution'
standard = {'propext','Classical.choice','Quot.sound'}
assert set(config['permitted_axioms']) == standard
assert meta['version'] == 'v0.4' and meta['repository']['role'] == 'substantive-development'
assert meta['project']['authors'] == ['George Stepaniants']
assert meta['project']['affiliations']['George Stepaniants'] == 'Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA'
assert meta['sources'][1]['authors'] == ['Codex automated maintainer audit']
assert meta['sources'][2]['authors'] == ['Kaie Kubjas','Luca Sodomaco','Elias Tsigaridas']
assert meta['status']['sorry_count'] == meta['status']['sorry_in_definitions'] == 0
assert set(meta['status']['axioms']) == standard
assert [r['declaration'] for r in meta['status']['main_results']] == names
assert [r['declaration'] for r in meta['alignment']] == names
for r in meta['status']['main_results']:
    assert r['file'] == 'Solution.lean' and r['sorry_count'] == 0
    assert set(r['axioms']) == standard and r['comparator_config'] == 'comparator.json'
    assert r['literature_dependencies'] == []
    assert re.search(r'^theorem '+re.escape(r['declaration'].split('.')[-1])+r'\b',(P/'Solution.lean').read_text(),re.M)
assert meta['toolchain']['lean'] == (P/'lean-toolchain').read_text().strip()
assert meta['toolchain']['dependencies'] == {r['name']:r['rev'] for r in load(P/'lake-manifest.json')['packages']}
assert len(meta['toolchain']['dependencies']) == 10
for key in ['statement_freeze','proof_freeze','statement_gate','coordinator_acceptance']:
    check(P/meta['review'][key]['file'],meta['review'][key]['sha256'])
for key in ['statement_reports','proof_reports']:
    for record in meta['review'][key]: check(P/record['file'],record['sha256'])
for name,r in meta['review']['proof_report_evidence'].items():
    check(P/name,r['sha256']); assert len(load(P/name)['files']) == r['bound_files']
assert meta['review']['linux_verification']['status'] == 'pending'
assert meta['reproduction']['authoritative_Linux']['status'] == 'pending'
assert meta['review']['candidate_documents']['independent_packaging_review'] == 'pending'
assert meta['reproduction']['local_development']['command'] == 'lake build Solution'
assert 'defaultTargets = ["Challenge"]' in (P/'lakefile.toml').read_text()
assert meta['reproduction']['authoritative_Linux']['commands'] == [
    'tools/lean/bootstrap.sh /tmp/nla-ra20-check','tools/lean/selftest.sh /tmp/nla-ra20-check',
    'tools/lean/verify.sh randomized-and-low-rank-approximation/RA-20/lean /tmp/nla-ra20-check']
assert meta['review']['candidate_documents']['frozen_readme_archive'] == 'verification/pre-candidate-README.md'
assert meta['review']['candidate_documents']['frozen_readme_sha256'] == OLD
assert meta['review']['coordinator_acceptance']['sha256'] == GATE
assert meta['review']['standards']['schema_sha256'] == digest(G/'docs/lean/schema/v0.4.schema.json')

readme = (P/'README.md').read_text()
for required in ['Canonical status remains Solved','lake build Solution','ordinary localizations',
                 'no adic completion','No separate scheme-theoretic', 'local macOS checks',
                 '68 project inputs','521 proof/evidence files','236 project declarations',
                 '214 in the actual export closure','39 material dependencies','28 separately selected',
                 '57 from the proof sources','61 source and twelve additional']:
    assert required in readme, required
assert '**Status:** Solved' in (P.parent/'README.md').read_text()
links = []
for doc in [P/'README.md', A/'HANDOFF.md']:
    count = 0
    for label,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',doc.read_text()):
        if urllib.parse.urlsplit(url).scheme:
            assert url.startswith('https://')
        else:
            path = (doc.parent/urllib.parse.unquote(url.split('#')[0])).resolve()
            assert path.is_file(),url
            count += 1
            links.append({'document':str(doc.relative_to(P)), 'label':label,
                          'target':str(path.relative_to(G)),'sha256':digest(path)})
    assert count == (22 if doc == P/'README.md' else 7)
assert len(links) == 29
metadata_paths = []
path_keys = {'file','comparator_config','dependency_manifest','frozen_readme_archive',
             'installation_evidence','adaptation','local_schema','prerequisites_document'}
def inspect_paths(value, loc=''):
    if isinstance(value, dict):
        for key,item in value.items():
            names_to_check = ([item] if key in path_keys else [])
            if key.endswith('EVIDENCE-MANIFEST.json'): names_to_check.append(key)
            for name in names_to_check:
                path = (P/name).resolve()
                assert path.is_file() and path.is_relative_to(G), name
                metadata_paths.append({'key':loc+'/'+key,'path':name,'sha256':digest(path)})
            inspect_paths(item,loc+'/'+key)
    elif isinstance(value,list):
        for j,item in enumerate(value): inspect_paths(item,loc+'/'+str(j))
inspect_paths(meta)
assert len(metadata_paths) == 40
source_links = []
for s in meta['sources'][:2]:
    prefix='https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/'+BASE+'/'
    assert s['id'].startswith(prefix)
    path=s['id'][len(prefix):]
    assert digest(G/path) == proof['source_files'][path]
    source_links.append(s['id'])

commands = [
    [PY,str(G/'tools/lean/validate_manifest.py'),str(P)],
    ['python3','tools/validate_problem_ids.py','--base-ref','origin/main'],
    ['python3','tools/validate_problem_ids.py','--base-ref','nla-upstream/main'],
    ['python3',str(A/'verify_inventory.py')],
    ['git','diff','--exit-code','HEAD','--','randomized-and-low-rank-approximation/RA-20/README.md',
     'problem_ids.json','README.md','CATALOG.md','RESOLVED.md']]
for args in commands: command(args,G)

# The installer seal includes every live candidate path. It remains unchanged after all checks.
for n,v in author['files'].items(): check(A/n,v)
check(A/'EVIDENCE-MANIFEST.json',OUTER)
check(A/'HANDOFF.md',HANDOFF)
check(P/'README.md',NEW); check(P/'formalization.yaml',YAML)
email = re.compile(rb'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
material=[P/'README.md',P/'formalization.yaml',A/'HANDOFF.md']
assert not any(email.search(p.read_bytes()) for p in material), 'Email-like material; do not display'
write(E/'RESULT.json',{'utc':utc(),'status':'INDEPENDENT_FIXED_CANDIDATE_CHECKS_PASS',
    'reviewer':'/root/ra20_final_referee2','role':'Independent metadata/reproduction/evidence-preservation reviewer; previously final mathematical referee 2; no new mathematical approval',
    'author_handoff_sha256':HANDOFF,'author_manifest_sha256':OUTER,
    'README_sha256':NEW,'YAML_sha256':YAML,'coordinator_gate_sha256':GATE,
    'author_bound_files':1010,'author_project_files':992,'baseline_preserved':958,
    'changed_prior_paths':['README.md'],'sole_historical_archive_sha256':OLD,
    'proof_inputs':521,'statement_inputs':68,'original_Git_and_live_and_snapshot_sources':16,
    'historical_nested_inventories':nested,'complete_final_reviews':reports,
    'all_twelve_exact_metadata_alignment_exports':names,'pinned_packages':meta['toolchain']['dependencies'],
    'relative_links':links,'original_immutable_links':source_links,
    'metadata_file_paths':metadata_paths,
    'audit_diagnostics':'One reviewer link-count assertion failed before correction; complete source/log preserved. Sixteen original Git receipts reused with exact command, successful exit and raw-log hash checks during resume.',
    'recorded_commands':len(list(E.glob('command-*'))),
    'new_Lean_builds':0,'Linux_Comparator_default_kernel_controls':'pending, not run in this audit',
    'canonical_status':'Solved, unchanged','operational_review':'pending','publication':'pending',
    'candidate_document_email_like_matches':0})
print(json.dumps({'status':'PASS','baseline_preserved':958,'author_bound_files':1010,
    'historical_nested_inventories':14,'full_final_reviews':[699,793],
    'exports':12,'pins':10,'links':len(links),'commands':len(list(E.glob('command-*')))}))
