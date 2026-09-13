#!/usr/bin/env python3
"""Independent IE05 statement-referee-2 input binding and evidence recorder."""
import datetime, hashlib, json, os, pathlib, subprocess, sys, time

E = pathlib.Path(__file__).resolve().parent
P = E.parent.parent
SOURCE_REPO = pathlib.Path('/Users/georgestepaniants/Research/OpenProblemsInNLA')
BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')

def run(label, argv, cwd=P, env=ENV):
    t = time.monotonic()
    r = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logs = E / 'logs'
    logs.mkdir(exist_ok=True)
    (logs / (label + '.stdout')).write_bytes(r.stdout)
    (logs / (label + '.stderr')).write_bytes(r.stderr)
    rec = dict(label=label, argv=list(map(str,argv)), cwd=str(cwd), exit_code=r.returncode,
               elapsed_seconds=time.monotonic()-t,
               utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               stdout_sha256=sha(r.stdout), stderr_sha256=sha(r.stderr))
    with (E / 'commands.jsonl').open('a') as f:
        f.write(json.dumps(rec, sort_keys=True)+'\n')
    if r.returncode:
        raise RuntimeError(f'{label}: exit {r.returncode}; see recorded logs')
    return r.stdout

def bind_inputs():
    invbytes=(P/'DRAFT-INVENTORY.json').read_bytes()
    assert sha(invbytes)=='85265ec4d16e1c69570f5a7aab4bf068336fb84aa9e67dd3c5121a9c4eaa9568'
    inv=json.loads(invbytes)
    assert len(inv['files'])==102
    assert inv['source_base']==BASE and inv['proof_authorized'] is False and inv['is_statement_freeze'] is False
    actual={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and not p.relative_to(P).parts[0]=='reviews'}
    expected=set(inv['files']) | {'DRAFT-INVENTORY.json'}
    assert actual==expected, dict(extra=sorted(actual-expected), missing=sorted(expected-actual))
    verified={}
    for rel in sorted(expected):
        src=P/rel
        assert not src.is_symlink()
        b=src.read_bytes()
        item=dict(sha256=sha(b), bytes=len(b))
        if rel in inv['files']:
            assert item==inv['files'][rel], rel
        dest=E/'inputs'/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():
            assert dest.read_bytes()==b
        else:
            dest.write_bytes(b)
        verified[rel]=item
    assert verified['STATEMENT-HANDOFF.md']['sha256']=='f2a38aa918a4f00a7b8f1986e80e87548827d44592ea055930051513f1aab5e0'
    write_json(E/'input-binding.json', dict(pass_=True, reviewed_base=BASE, files=verified,
       complete_input_count=103, excluded_from_completeness=['reviews/**'],
       exclusion_reason='Concurrent and own referee artifacts are outputs, not handed-off draft inputs.'))
    return inv

def bind_git():
    inventory=json.loads((E/'inputs/verification/original-source-inventory.json').read_text())
    assert inventory['base']==BASE and len(inventory['files'])==27
    assert run('source-commit',['git','rev-parse',BASE+'^{commit}'],SOURCE_REPO).decode().strip()==BASE
    run('source-commit-metadata',['git','show','--no-patch','--format=fuller',BASE],SOURCE_REPO)
    run('source-status',['git','status','--porcelain=v1','--untracked-files=no'],SOURCE_REPO)
    run('source-remote',['git','remote','get-url','origin'],SOURCE_REPO)
    results={}
    for i,(rel,item) in enumerate(sorted(inventory['files'].items())):
        blob=run(f'source-{i:02d}-oid',['git','rev-parse',BASE+':'+rel],SOURCE_REPO).decode().strip()
        b=run(f'source-{i:02d}-blob',['git','cat-file','blob',blob],SOURCE_REPO)
        snapshot=(E/'inputs/verification/original-sources'/rel).read_bytes()
        assert dict(sha256=sha(b),bytes=len(b),git_blob=blob)==item,rel
        assert snapshot==b,rel
        results[rel]=dict(**item, exact_blob_equality=True)
    registered=json.loads((E/'inputs/verification/original-sources/problem_ids.json').read_text())
    results['registry_IE05']=registered.get('IE-05')
    assert registered['IE-05']=='linear-systems-and-elimination/IE-05/README.md'
    write_json(E/'git-source-binding.json',dict(pass_=True,source_repo=str(SOURCE_REPO),base=BASE,files=results))

if __name__=='__main__':
    bind_inputs()
    bind_git()
    print('PASS: 103 complete draft inputs and 27 immutable original Git/source bindings verified and snapshotted.')
