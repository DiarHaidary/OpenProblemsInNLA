#!/usr/bin/env python3
"""Fresh statement elaboration and definition-only axiom inspection.

Reads the ten pinned package directories in place. Never invokes Lake, installs,
copies, or builds packages. Hashes and removes only objects in this script's own
initially empty private prefix. Does not import Challenge into the trust inspector.
"""
import json, os, pathlib, re, shutil, sys, tempfile
from audit import E, ENV, run as record_run, sha, write_json

def run(label, argv, cwd=E.parent.parent, env=ENV):
    return record_run('attempt-2-'+label, argv, cwd, env)

PACKAGES=pathlib.Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
LEAN=pathlib.Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean')
manifest=json.loads((E/'inputs/lake-manifest.json').read_text())
defs=(E/'inputs/NLA/IE05/Definitions.lean').read_text()
challenge=(E/'inputs/Challenge.lean').read_text()
config=json.loads((E/'inputs/comparator.json').read_text())
names=re.findall(r'^(?:def|abbrev)\s+(\w+)\b',defs,re.M)
theorems=re.findall(r'^theorem\s+(\w+)\b',challenge,re.M)
assert len(theorems)==17 and len(set(theorems))==17
assert config['theorem_names']==['NLA.IE05.'+x for x in theorems]
assert config['definition_names']==[]
assert set(config['permitted_axioms'])=={'propext','Classical.choice','Quot.sound'}
assert challenge.count(':= by sorry')==17
assert not re.search(r'\b(sorry|axiom|unsafe|implemented_by|extern)\b', re.sub(r'/\-.*?\-/','',defs,flags=re.S))
assert not re.search(r'^(theorem|lemma|axiom)\b',defs,re.M)

def package_status(phase):
    records=[]
    for p in manifest['packages']:
        root=PACKAGES/p['name']
        head=run(phase+'-'+p['name']+'-head',['git','rev-parse','HEAD'],root).decode().strip()
        assert head==p['rev'],p
        status=run(phase+'-'+p['name']+'-status',['git','status','--porcelain=v1','--untracked-files=no'],root)
        assert status==b'',(p['name'],status)
        obj=root/'.lake/build/lib/lean'
        assert obj.is_dir() or p['name']=='Cli'
        records.append(dict(name=p['name'],revision=head,tracked_status_clean=True,
              source_directory=str(root),object_directory=str(obj) if obj.is_dir() else None,
              role='tooling only, not imported' if p['name']=='Cli' else 'read-only dependency'))
    assert len(records)==10
    return records

before=package_status('pre')
version=run('lean-version',[str(LEAN),'--version']).decode().strip()
assert 'version 4.33.1' in version
run('machine',['uname','-a'])
prefix=pathlib.Path(tempfile.mkdtemp(prefix='private-objects-',dir=E))
assert not list(prefix.iterdir())
inspect='import NLA.IE05.Definitions\nimport LeanCert.Tactic.Verification\n\n'
inspect+='set_option leancert.trust "kernel"\n\n'
for name in names:
    q='NLA.IE05.'+name
    inspect+=f'#print {q}\n#print axioms {q}\n#assert_trust kernel {q}\n\n'
inspect+='#print InnerProductSpace.gramSchmidtNormed\n'
inspect+='#check InnerProductSpace.gramSchmidtNormed_orthonormal\n'
inspect+='#check InnerProductSpace.gramSchmidt_ne_zero\n'
inspect+='#check InnerProductSpace.gramSchmidt_inv_triangular\n'
inspect+='#check PiLp.inner_apply\n'
inspect+='#check Real.sqrt_pos\n#check Real.sq_sqrt\n#check le_csSup\n#check csSup_le\n'
inspector=E/'inputs/Referee2Inspect.lean'
assert inspector.read_text()==inspect
objdirs=[str(PACKAGES/p['name']/'.lake/build/lib/lean') for p in manifest['packages'] if p['name']!='Cli']
env=dict(ENV,LEAN_PATH=os.pathsep.join([str(prefix)]+objdirs))
# Clear inherited custom Lean module search settings; the explicit toolchain and
# recorded LEAN_PATH fully determine this standalone run's lookup.
for key in ['LEAN_SRC_PATH','LEAN_SYSROOT']:
    env.pop(key,None)
result=dict(phase='statement-only independent macOS elaboration',proofs_established=False,
  version=version,lean_binary=str(LEAN),lean_binary_sha256=sha(LEAN.read_bytes()),
  package_preflight=before,private_prefix=str(prefix),prefix_initially_empty=True,
  imported_package_objects_copied=False,package_build_or_download=False,
  explicit_environment={'LEAN_PATH':env['LEAN_PATH'],'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1'},
  statement_count=len(theorems),definition_trust_count=len(names),definition_names=names,
  inspector_sha256=sha(inspector.read_bytes()),comparison_configuration=config)
try:
    (prefix/'NLA/IE05').mkdir(parents=True)
    run('fresh-definitions',[str(LEAN),'-o',str(prefix/'NLA/IE05/Definitions.olean'),'NLA/IE05/Definitions.lean'],E/'inputs',env)
    run('fresh-challenge',[str(LEAN),'-o',str(prefix/'Challenge.olean'),'Challenge.lean'],E/'inputs',env)
    run('fresh-inspector',[str(LEAN),'-o',str(prefix/'Referee2Inspect.olean'),'Referee2Inspect.lean'],E/'inputs',env)
    definition_log=(E/'logs/attempt-2-fresh-definitions.stdout').read_text()+(E/'logs/attempt-2-fresh-definitions.stderr').read_text()
    challenge_log=(E/'logs/attempt-2-fresh-challenge.stdout').read_text()+(E/'logs/attempt-2-fresh-challenge.stderr').read_text()
    inspect_log=(E/'logs/attempt-2-fresh-inspector.stdout').read_text()+(E/'logs/attempt-2-fresh-inspector.stderr').read_text()
    assert definition_log==''
    assert challenge_log.count('warning: declaration uses `sorry`')==17
    assert len(challenge_log.strip().splitlines())==17
    assert 'warning:' not in inspect_log and 'error:' not in inspect_log
    axiom_reports=re.findall(r"'NLA\.IE05\.(\w+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)",inspect_log,re.S)
    assert len(axiom_reports)==len(names),(len(axiom_reports),len(names))
    axiom_map={n:[a.strip() for a in axs.split(',') if a.strip()] for n,axs in axiom_reports}
    assert set(axiom_map)==set(names)
    assert all(set(axs)<={'propext','Classical.choice','Quot.sound'} for axs in axiom_map.values())
    result.update(pass_=True,definitions_warnings=0,inspector_warnings=0,intentional_challenge_warnings=17,axiom_reports=axiom_map)
except BaseException as e:
    result.update(pass_=False,error=repr(e))
    raise
finally:
    result['objects']={str(p.relative_to(prefix)):dict(sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
                       for p in sorted(prefix.rglob('*')) if p.is_file()}
    write_json(E/'elaboration-result-2.json',result)
    for p in sorted(prefix.rglob('*'),key=lambda x:len(x.parts),reverse=True):
        if p.is_file(): p.unlink()
        else: p.rmdir()
    prefix.rmdir()
    result['own_objects_hashed_then_removed']=True
    result['private_prefix_absent_after']=not prefix.exists()
    result['package_postflight']=package_status('post')
    assert result['package_postflight']==before
    write_json(E/'elaboration-result-2.json',result)
print('PASS: fresh Definitions, 17-placeholder Challenge and all '+str(len(names))+' local definition trust checks; own objects hashed then removed.')
