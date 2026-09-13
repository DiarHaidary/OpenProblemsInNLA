#!/usr/bin/env python3
"""Independent source provenance only; never invokes Lean or writes to checkout."""
from pathlib import Path,PurePosixPath,PureWindowsPath
import hashlib,json,re,stat,subprocess,zipfile
import yaml,jsonschema
REPO=Path('/private/tmp/nla-audit-251');REL='nonnegative-and-positive-factorizations/NR-03/lean';ROOT=REPO/REL
HEAD='589ec79798ee42adc7a7160a376c67252280a121';PROOF='f664d07e82aaa60bc9c78dd1946e763168c5c530';BASE='752218e5417998b7f4d2aee9c447ca5d256fe530';SOURCE='50838e37dd793830e2cecd1055cfc7e0349490f1';DEV='3b3eb8f3fa384e4b3bf640d48bca87cf40db9565'
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def blob(commit,path):return git('show',commit+':'+path)
def data(path):return json.loads((ROOT/path).read_text())
result={'head':HEAD,'verified_proof':PROOF,'source_base':SOURCE}
assert git('rev-parse','HEAD').decode().strip()==HEAD
# Recompute every raw source binding from the actual Git objects, not local manifest agreement alone.
bindings=data('verification/linux-2026-09-13/GIT-SOURCE-BINDINGS.json');raw=data('verification/linux-2026-09-13/extracted/verify-20260913T215907Z-4140/result.json')
assert bindings['commit']==PROOF and bindings['input_sha256']==raw['input_sha256']
changed=[]
for path,digest in bindings['input_sha256'].items():
 b=blob(PROOF,REL+'/'+path);assert sha(b)==digest,path
 if (ROOT/path).read_bytes()!=b:changed.append(path)
assert len(bindings['input_sha256'])==113
assert set(changed)=={'ACTIVE-MODULE-MANIFEST.json','README.md','SOURCE_MAP.md','formalization.yaml','reviews/proof-candidate-hashes.json'}
result['historical_inputs']={'checked':113,'current_metadata_deltas':changed,'all_hashes_match_git':True}
# Full present inventory, including self-exclusion semantics.
inventory=data('reviews/proof-candidate-hashes.json')['files_excluding_this_manifest']
tracked={x for x in git('ls-tree','-r','--name-only',HEAD,REL).decode().splitlines()}
relative={p[len(REL)+1:] for p in tracked}
assert relative==set(inventory)|{'reviews/proof-candidate-hashes.json'}
for p,h in inventory.items():assert sha((ROOT/p).read_bytes())==h,p
result['present_inventory']={'listed':len(inventory),'self_excluded':1,'total_tracked':len(relative),'complete':True}
active=data('ACTIVE-MODULE-MANIFEST.json');paths=[];development_deltas=[]
dev_available=subprocess.run(['git','cat-file','-e',DEV+'^{commit}'],cwd=REPO,capture_output=True).returncode==0
for item in active['active_modules']:
 p=item['path'];paths.append(p);b=(ROOT/p).read_bytes()
 assert sha(b)==item['sha256'] and len(b)==item['bytes'],p
 assert b==blob(PROOF,REL+'/'+p),p
 if dev_available:
  old=blob(DEV,item['source_path'])
  assert blob('523c5aeaddd8bf7c2dc01afb053bb0dea8811335',REL+'/'+p)==old,p
  if old!=b:development_deltas.append(p)
assert len(paths)==len(set(paths))==58
if dev_available:assert development_deltas==['NLA/NR03/Rank.lean']
for p,h in active['frozen_boundary'].items():
 rp='NLA/NR03/Definitions.lean' if p=='Definitions.lean' else p
 assert sha((ROOT/rp).read_bytes())==h and (ROOT/rp).read_bytes()==blob(PROOF,REL+'/'+rp),rp
# Independently follow project imports from Solution; metadata inventory must describe exact closure.
closure=set();stack=['Solution.lean']
while stack:
 p=stack.pop()
 if p in closure:continue
 closure.add(p)
 for line in (ROOT/p).read_text().splitlines():
  if line.startswith('import '):
   for name in line[7:].split():
    q=name.replace('.','/')+'.lean'
    if (ROOT/q).exists():stack.append(q)
assert closure==set(paths)
assert 'Challenge.lean' not in closure and 'NLA/NR03/CertificateData.lean' not in closure
result['active_graph']={'modules':58,'closure_exact':True,'all_match_verified_commit':True,'development_git_authenticated':dev_available,'prior_523_package_matches_development':dev_available,'development_deltas':development_deltas if dev_available else None,'frozen_boundary_files':len(active['frozen_boundary'])}
repair=data('reviews/rank-cast-repair/HASHES.json');new=(ROOT/'NLA/NR03/Rank.lean').read_bytes();old=blob(repair['base_commit'],repair['canonical_path']);line='    change (0 : ℝ) ≤ (W i k : ℝ)\n'.encode()
assert new.count(line)==1 and new.replace(line,b'',1)==old
assert sha(new)==repair['new_rank_sha256'] and sha(old)==repair['old_rank_sha256']
assert sha((ROOT/'reviews/rank-cast-repair/REPAIR.diff').read_bytes())==repair['repair_diff_sha256']
result['rank_repair_exact']=True
# Exact seven-path historical development overlay, with copied subset hashes.
overlay=active['bridge_overlay'];expected={x['source_path'] for x in overlay['paths']};actual=expected
if dev_available:
 actual=set(git('diff','--name-only',overlay['base_commit'],DEV,'--','development/NR03').decode().splitlines())
 assert actual==expected and len(actual)==7
 receipt=data('certificate-bridge/INTEGRATION-PATHS.json')
 assert receipt['base_commit']==overlay['base_commit'] and set(receipt['paths'])==actual
 for status,key in [('A','added'),('M','changed')]:
  assert set(git('diff','--name-only','--diff-filter='+status,overlay['base_commit'],DEV,'--','development/NR03').decode().splitlines())==set(receipt[key])
else:
 result['historical_development_git_limit']='Development commit unavailable locally; seven listed paths checked against immutable preserved package receipts and five copied files, not authenticated against development Git objects.'
for row in overlay['paths']:
 if dev_available:assert sha(blob(DEV,row['source_path']))==row['source_sha256']
 if row['package_path']:assert sha((ROOT/row['package_path']).read_bytes())==row['package_sha256']
result['historical_overlay_paths']=sorted(actual)
# Seven source-correspondence rows, authenticating both Git blob IDs and SHA256 bytes.
source_rows=re.findall(r'^\|[^|]+\| `([^`]+)` \| `([0-9a-f]{40})` \| `([0-9a-f]{64})` \|$',(ROOT/'SOURCE_MAP.md').read_text(),re.M)
for p,oid,digest in source_rows:
 assert git('rev-parse',SOURCE+':'+p).decode().strip()==oid and sha(blob(SOURCE,p))==digest,p
assert len(source_rows)==7
result['mathematical_source_map_rows_verified']=7
# Preserve canonical mathematical target, historical credit and permanent numbering.
canonical='nonnegative-and-positive-factorizations/NR-03/README.md';before=blob(BASE,canonical).decode();after=(REPO/canonical).read_text()
assert before.split('## Context and notation',1)[1]==after.split('## Context and notation',1)[1]
marker='<!-- colbrook-factorization -->';end='<!-- /colbrook-factorization -->'
assert before.split(marker)[1].split(end)[0]==after.split(marker)[1].split(end)[0]
assert blob(BASE,'problem_ids.json')==(REPO/'problem_ids.json').read_bytes()
registry=json.loads((REPO/'problem_ids.json').read_text())
result['target_and_ids']={'target_suffix_unchanged':True,'colbrook_block_unchanged':True,'registry_unchanged':True,'registered_ids':len(registry)}
# Current metadata against pinned schema and all actual manifest revisions.
meta=yaml.safe_load((ROOT/'formalization.yaml').read_text());schema_bytes=(REPO/'docs/lean/schema/v0.4.schema.json').read_bytes();schema=json.loads(schema_bytes);jsonschema.validate(meta,schema)
assert sha(schema_bytes)=='25ff6b25ca4511635aff4443cf20480c15e59dddf19591c730950b442ea54fce'
pins={p['name']:p['rev'] for p in data('lake-manifest.json')['packages']}
assert pins==meta['toolchain']['dependencies'] and len(pins)==10
assert meta['toolchain']['lean']==(ROOT/'lean-toolchain').read_text().strip()==raw['tool_receipt']['lean_toolchain']
assert raw['config']==data('comparator.json');config=raw['config'];exports=[x['declaration'] for x in meta['status']['main_results']]
assert exports==config['theorem_names'] and len(exports)==10
for x in meta['review']['proof_reports']:assert sha((ROOT/x['file']).read_bytes())==x['sha256']
result['metadata']={'pinned_schema_valid':True,'schema_sha256':sha(schema_bytes),'dependency_pins_match':10,'exports_match':10,'final_review_hashes_match':2}
# Verify copied evidence bytes, but leave external Actions authentication to coordinator.
evidence=ROOT/'verification/linux-2026-09-13';manifest=data('verification/linux-2026-09-13/EVIDENCE-MANIFEST.json')
for p,h in manifest['files'].items():assert sha((evidence/p).read_bytes())==h,p
with zipfile.ZipFile(evidence/'artifact.zip') as z:
 seen=set();count=0
 for info in z.infolist():
  p=PurePosixPath(info.filename);mode=info.external_attr>>16
  assert not p.is_absolute() and '..' not in p.parts and not PureWindowsPath(info.filename).drive and '\\' not in info.filename
  assert not stat.S_ISLNK(mode) and info.filename not in seen
  seen.add(info.filename)
  if not info.is_dir():assert z.read(info)==(evidence/'extracted'/info.filename).read_bytes();count+=1
actual=meta['reproduction']['actual_verification'];assert sha((evidence/'artifact.zip').read_bytes())==actual['artifact_sha256']
assert sha((evidence/'extracted/verify-20260913T215907Z-4140/result.json').read_bytes())==actual['raw_evidence_sha256']
result['evidence_integrity']={'manifest_files':len(manifest['files']),'zip_payload_files':count,'artifact_and_raw_digests_match':True,'external_authentication':'coordinator responsibility'}
publication=data('verification/publication/DOCUMENT-CHECKS.json')
for p,h in publication['final_documents'].items():assert sha((REPO/p).read_bytes())==h,p
for p,h in publication['all_lean_files_and_boundary_review_bindings'].items():assert sha((ROOT/p).read_bytes())==h,p
result['publication_receipt']={'final_document_hashes':3,'source_and_boundary_hashes':84,'all_match':True}
result['passed']=True
Path('/private/tmp/nla-pr-251-provenance.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
