import pathlib,subprocess,json,hashlib,re
repo=pathlib.Path('/private/tmp/nla-audit-246')
prefix='linear-systems-and-elimination/IE-16/lean/'
p=repo/prefix
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
assert head=='a4e8ea57f9b010b85390845b4de902183b6d97ba'
def show(rev,path): return subprocess.check_output(['git','show',rev+':'+path],cwd=repo)
def sha(b): return hashlib.sha256(b).hexdigest()
seen=set()
def walk(mod):
    path=mod.replace('.','/')+'.lean'
    if path in seen:return
    src=(p/path).read_text();seen.add(path)
    for imported in re.findall(r'^import (\S+)',src,re.M):
        if (p/(imported.replace('.','/')+'.lean')).exists():walk(imported)
walk('Solution')
assert len(seen)==10 and 'Challenge.lean' not in seen
bad=[]
for name in sorted(seen):
    raw=(p/name).read_bytes()
    assert raw==show('697a2a1d88337a6747aa5c82fb6e554d3ff1b356',prefix+name)
    text=raw.decode()
    # Source inspection also read every live file; remove explanatory comments before lexical scan.
    text=re.sub(r'/-.*?-/', '',text, flags=re.S)
    text=re.sub(r'--[^\n]*','',text)
    for tok in ['sorry','admit','axiom','native_decide','implemented_by','unsafe','run_tac']:
        if re.search(r'\b'+tok+r'\b',text):bad.append((name,tok))
assert not bad,bad
spec=json.loads((p/'comparator.json').read_text())
expected=[s.rsplit('.',1)[-1] for s in spec['theorem_names']]
assert len(set(expected))==15
challenge=(p/'Challenge.lean').read_text()
assert re.findall(r'^theorem (\w+)',challenge,re.M)==expected
for name in expected:
    assert sum(len(re.findall(r'^(?:theorem|lemma) '+name+r'\b',(p/file).read_text(),re.M)) for file in seen)==1
bound=json.loads((p/'verification/STATEMENT_HASHES.json').read_text())['files']
for name in ['Challenge.lean','NLA/IE16/Definitions.lean','comparator.json','lake-manifest.json','lean-toolchain']:
    assert sha((p/name).read_bytes())==bound[name]
source=p/'verification/source-snapshot'
manifest=json.loads((source/'SOURCE_HASHES.json').read_text())
map_original={
 'canonical-README.md':'linear-systems-and-elimination/IE-16/README.md',
 'canonical-problem.tex':'linear-systems-and-elimination/IE-16/problem.tex',
 'holden-solution.tex':'references/holden-ie16-2026-09-12/submitted/source/solution.tex',
 'holden-submission.md':'references/holden-ie16-2026-09-12/submitted/README.md',
 'verify.py':'references/holden-ie16-2026-09-12/submitted/code/verify.py',
 'all_subset_certificate.json':'references/holden-ie16-2026-09-12/submitted/certificates/all_subset_certificate.json'}
for f,h in manifest['files'].items():
    assert sha((source/f).read_bytes())==h
    assert (source/f).read_bytes()==show(manifest['upstream_commit'],map_original[f]),f
base='752218e5417998b7f4d2aee9c447ca5d256fe530'
assert (repo/'problem_ids.json').read_bytes()==show(base,'problem_ids.json')
assert len(json.loads((repo/'problem_ids.json').read_text()))==217
base_read=show(base,'linear-systems-and-elimination/IE-16/README.md').decode()
current_read=(repo/'linear-systems-and-elimination/IE-16/README.md').read_text()
assert base_read.split('## Original problem (retained)',1)[1]==current_read.split('## Original problem (retained)',1)[1]
summary={'head':head,'local_import_closure':sorted(seen),'local_module_count':len(seen),'forbidden_tokens':bad,'each_public_export_declared_once':15,'closure_byte_identical_to_verified_revision':'697a2a1d88337a6747aa5c82fb6e554d3ff1b356','approved_boundary_and_dependency_pin_hashes':True,'source_snapshot_hashes_and_upstream_git_bytes':True,'registry_entries_unchanged':217,'original_target_tail_byte_unchanged':True,'limitation':'Read-only source/hash audit; kernel closure authentication and current CI handled by coordinator; no Lean invocation.'}
pathlib.Path('/private/tmp/nla-246-source-scan.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
