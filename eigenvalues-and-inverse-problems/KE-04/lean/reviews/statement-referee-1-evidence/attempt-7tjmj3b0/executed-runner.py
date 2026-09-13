#!/usr/bin/env python3
"""Independent KE-04 statement inspection; no theorem proof is constructed.

The diagnostic closure idiom was inspected in my earlier RA-20 referee source;
all KE-04 inputs, commands, objects, dependencies, and results are new here.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import traceback

E = Path(__file__).resolve().parent
K = E.parent.parent
PACKAGES = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages').resolve()
TOOLCHAIN = Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
LEAN = TOOLCHAIN / 'bin/lean'
REPO = Path('/tmp/nla-lean-ra20-worktree').resolve()
ORDER = ['batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph', 'LeanSearchClient', 'plausible', 'mathlib', 'leancert']
PRIMARY = ['NLA/KE04/Definitions.lean', 'Challenge.lean', 'NUMERICAL_TARGETS.md', 'SourceCorrespondence.md', 'README.md', 'comparator.json', 'lakefile.toml', 'lake-manifest.json', 'lean-toolchain']
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
ATTEMPT = Path(tempfile.mkdtemp(prefix='attempt-', dir=E))
SOURCE = ATTEMPT / 'source'
SOURCE.mkdir()
PRIVATE_ROOT = Path('/tmp/nla-lean-formalization/independent-prefixes')
PRIVATE_ROOT.mkdir(exist_ok=True)
OUTPUT = Path(tempfile.mkdtemp(prefix='ke04-statement-referee1-', dir=PRIVATE_ROOT)).resolve()
assert not list(OUTPUT.iterdir())
commands = []

def digest(data):
    return hashlib.sha256(data).hexdigest()

def row(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': digest(b)}

def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def command(argv, label, *, cwd=K, env=ENV):
    num = len(commands)
    stem = f'command-{num:03d}-{label}'
    rec = {'argv': list(map(str, argv)), 'cwd': str(cwd), 'utc_started': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'environment_overrides': {key: env[key] for key in ['GIT_OPTIONAL_LOCKS', 'PYTHONDONTWRITEBYTECODE', 'LEAN_PATH', 'LEAN_SRC_PATH'] if key in env},
           'stdout': stem + '.stdout', 'stderr': stem + '.stderr'}
    commands.append(rec)
    write(ATTEMPT / 'progress.json', {'runner_pid': os.getpid(), 'private_output': str(OUTPUT), 'commands': commands})
    start = time.monotonic()
    with (ATTEMPT / rec['stdout']).open('wb') as out, (ATTEMPT / rec['stderr']).open('wb') as err:
        proc = subprocess.Popen(rec['argv'], cwd=cwd, env=env, stdout=out, stderr=err)
        rec['pid'] = proc.pid
        write(ATTEMPT / (stem + '.json'), rec)
        rec['exit_code'] = proc.wait()
    rec['elapsed_seconds'] = time.monotonic() - start
    rec['utc_finished'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rec['stdout_identity'] = row(ATTEMPT / rec['stdout'])
    rec['stderr_identity'] = row(ATTEMPT / rec['stderr'])
    write(ATTEMPT / (stem + '.json'), rec)
    write(ATTEMPT / 'progress.json', {'runner_pid': os.getpid(), 'private_output': str(OUTPUT), 'commands': commands})
    if rec['exit_code'] != 0:
        raise RuntimeError(f'{stem} exited {rec["exit_code"]}')
    return (ATTEMPT / rec['stdout']).read_bytes()

def baseline_check():
    baseline = json.loads((E / 'baseline.json').read_text())['files']
    for p, expected in baseline.items():
        assert row(K / p) == expected, p
    return len(baseline)

def pin_check(stage):
    manifest = json.loads((K / 'lake-manifest.json').read_text())
    found = []
    assert len(manifest['packages']) == 10
    for pkg in manifest['packages']:
        folder = PACKAGES / pkg['name']
        head = command(['git', '-C', folder, 'rev-parse', 'HEAD'], f'{stage}-{pkg["name"]}-head').decode().strip()
        status = command(['git', '-C', folder, 'status', '--porcelain', '--untracked-files=all'], f'{stage}-{pkg["name"]}-clean').decode()
        assert head == pkg['rev'], (pkg['name'], head)
        assert status == '', (pkg['name'], status)
        found.append({'name': pkg['name'], 'revision': head, 'clean': True})
    return found

result = {'phase': 'independent statement-only elaboration and definition trust', 'reviewer': '/root/ra20_final_referee2',
          'author_independent': True, 'proof_implementation': False, 'linux_comparator_run': False,
          'private_output': str(OUTPUT), 'empty_private_output': True, 'source': str(SOURCE), 'started': datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
    result['baseline_before'] = baseline_check()
    result['toolchain_binary'] = row(LEAN)
    assert result['toolchain_binary']['sha256'] == '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554'
    result['version'] = command([LEAN, '--version'], 'lean-version').decode().strip()
    result['pins_before'] = pin_check('before')
    originals = json.loads((K / 'verification/original-source-inventory.json').read_text())['files']
    result['original_git_sources'] = []
    for i, (path, expected) in enumerate(originals.items()):
        selector = f'{expected["commit"]}:{expected["upstream_path"]}'
        blob = command(['git', '-C', REPO, 'rev-parse', selector], f'original-{i:02d}-blob').decode().strip()
        data = command(['git', '-C', REPO, 'show', selector], f'original-{i:02d}-bytes')
        assert blob == expected['git_blob'], path
        assert data == (K / path).read_bytes(), path
        assert digest(data) == expected['sha256'] and len(data) == expected['bytes'], path
        result['original_git_sources'].append({'path': path, 'commit': expected['commit'], 'git_blob': blob, **row(K / path)})
    assert len(result['original_git_sources']) == 17
    result['source_identities'] = {}
    for path in PRIMARY:
        dst = SOURCE / path
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((K / path).read_bytes())
        dst.chmod(0o444)
        result['source_identities'][path] = row(dst)
    definitions = re.findall(r'^(?:abbrev|def) ([A-Za-z_][A-Za-z0-9_]*)', (SOURCE / 'NLA/KE04/Definitions.lean').read_text(), re.M)
    contracts = re.findall(r'^theorem ([A-Za-z_][A-Za-z0-9_]*)', (SOURCE / 'Challenge.lean').read_text(), re.M)
    names = ['NLA.KE04.' + n for n in contracts]
    conf = json.loads((SOURCE / 'comparator.json').read_text())
    assert len(definitions) == 27 and len(contracts) == 24
    assert conf['theorem_names'] == names
    assert conf['definition_names'] == []
    assert conf['permitted_axioms'] == ['propext', 'Classical.choice', 'Quot.sound']
    def_list = ',\n    '.join('``NLA.KE04.' + n for n in definitions)
    defs_inspector = '''/- Independent diagnostic only. No Challenge import and no theorem proofs. -/
import NLA.KE04.Definitions
import LeanCert
import Lean.Util.FoldConsts
set_option leancert.trust "kernel"
set_option maxHeartbeats 2000000
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let original : List Name := [DEF_LIST]
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." || n.toString.startsWith "_private.NLA.KE04."
  let mut pending := original
  let mut visited : List Name := []
  for _ in [:10000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless visited.contains name do
        visited := name :: visited
        let some ci := env.find? name | throwError "Missing concrete definition {name}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe/partial definition {name}"
        let some value := ci.value? (allowOpaque := true) | throwError "Bodyless definition {name}"
        let axioms ← liftCoreM <| collectAxioms name
        for ax in axioms do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Nonfoundational axiom {name}: {ax}"
        let deps := ci.type.getUsedConstants.toList ++ value.getUsedConstants.toList
        for dep in deps do
          if [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler].contains dep then
            throwError "Forbidden actual dependency {name}: {dep}"
        let projectDeps := deps.filter isProject
        let externalDeps := deps.filter (fun n => !isProject n)
        logInfo m!"DEFINITION_CLOSURE {name}: axioms={axioms.toList}; project={projectDeps}; imported={externalDeps}"
        pending := projectDeps ++ pending
  unless pending.isEmpty do throwError "Incomplete definition closure"
  logInfo m!"DEFINITION_CLOSURE_COMPLETE {visited.length}"
'''.replace('DEF_LIST', def_list)
    for name in definitions:
        full = 'NLA.KE04.' + name
        defs_inspector += f'\n#assert_trust kernel {full}\n#print axioms {full}\nset_option pp.all true in\n#print {full}\n'
    type_list = ',\n    '.join('``' + n for n in names)
    type_inspector = '''/- Intentional Challenge admissions are checked as admissions, never proofs. -/
import Challenge
import Lean.Util.FoldConsts
set_option maxHeartbeats 2000000
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let targets : List Name := [TYPE_LIST]
  let expectedDefs : List Name := [DEF_LIST]
  for name in targets do
    let some ci := env.find? name | throwError "Missing contract {name}"
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Contract is not a theorem declaration {name}"
    let axs ← liftCoreM <| collectAxioms name
    unless axs.contains ``sorryAx do throwError "Expected deliberate admission missing {name}"
    for dep in ci.type.getUsedConstants do
      if dep.toString.startsWith "NLA.KE04." then
        unless expectedDefs.contains dep do throwError "Contract type uses another admitted contract {name}: {dep}"
    logInfo m!"CONTRACT_TYPE_DIRECT {name}: {ci.type.getUsedConstants.toList}"
    logInfo m!"CONTRACT_ADMITTED {name}: {axs.toList}"
  logInfo m!"CONTRACT_INSPECTION_COMPLETE {targets.length}"
'''.replace('TYPE_LIST', type_list).replace('DEF_LIST', def_list)
    for name in names:
        type_inspector += f'\nset_option pp.all true in\n#print {name}\n'
    for filename, data in [('InspectDefinitions.lean', defs_inspector), ('InspectContracts.lean', type_inspector)]:
        (SOURCE / filename).write_text(data)
        (SOURCE / filename).chmod(0o444)
    shutil.copyfile(__file__, ATTEMPT / 'executed-runner.py')
    paths = [OUTPUT] + [PACKAGES / n / '.lake/build/lib/lean' for n in ORDER] + [TOOLCHAIN / 'lib/lean']
    assert all(p.is_dir() for p in paths)
    lean_env = dict(ENV, LEAN_PATH=os.pathsep.join(map(str, paths)), LEAN_SRC_PATH=str(SOURCE))
    result['lean_path'] = list(map(str, paths))
    result['modules'] = []
    for module in ['NLA/KE04/Definitions', 'Challenge', 'InspectDefinitions', 'InspectContracts']:
        target = OUTPUT / (module + '.olean')
        target.parent.mkdir(parents=True, exist_ok=True)
        data = command([LEAN, '-o', target, module + '.lean'], 'compile-' + module.replace('/', '-'), cwd=SOURCE, env=lean_env)
        result['modules'].append({'name': module, 'exit_code': 0, 'stdout_sha256': digest(data)})
    result['pins_after'] = pin_check('after')
    result['baseline_after'] = baseline_check()
    assert result['pins_before'] == result['pins_after']
    result['success'] = True
except BaseException as exc:
    result['success'] = False
    result['error'] = repr(exc)
    (ATTEMPT / 'failure.txt').write_text(traceback.format_exc())
finally:
    result['private_object_identities'] = {str(p.relative_to(OUTPUT)): row(p) for p in sorted(OUTPUT.rglob('*')) if p.is_file()}
    assert OUTPUT.parent == PRIVATE_ROOT.resolve() and OUTPUT.name.startswith('ke04-statement-referee1-')
    shutil.rmtree(OUTPUT)
    result['private_objects_removed'] = not OUTPUT.exists()
    result['commands'] = commands
    result['finished'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(ATTEMPT / 'result.json', result)
    print(json.dumps({'attempt': str(ATTEMPT), 'success': result['success'], 'error': result.get('error'), 'commands': len(commands), 'objects_hashed_and_removed': len(result['private_object_identities'])}, indent=2), flush=True)
if not result['success']:
    raise SystemExit(1)
