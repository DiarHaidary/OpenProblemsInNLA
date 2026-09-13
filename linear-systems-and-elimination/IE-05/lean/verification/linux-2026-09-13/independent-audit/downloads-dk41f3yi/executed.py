"""Download exact completed IE05/control artifacts and raw run logs read-only."""
from pathlib import Path,PurePosixPath
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,os,stat,subprocess,tempfile,zipfile
E=Path(__file__).resolve().parent;GH='/tmp/nla-submission-tools/gh_2.100.0_macOS_arm64/bin/gh';REPO='repos/sgstepaniants/OpenProblemsInNLA'
sha=lambda b:hashlib.sha256(b).hexdigest()
A=Path(tempfile.mkdtemp(prefix='downloads-',dir=E));(A/'executed.py').write_bytes(Path(__file__).read_bytes())
api=E/'api-jlvyv9bw';metadata=json.loads((api/'artifacts.json').read_text());selected={x['name']:x for x in metadata['artifacts'] if x['name'] in ['lean-IE-05','lean-checker-controls']};assert len(selected)==2
requests=[('ie05-job.log',f'{REPO}/actions/jobs/103708463461/logs',True),('controls-job.log',f'{REPO}/actions/jobs/103708463293/logs',True),('runlogs.zip',f'{REPO}/actions/runs/34751393873/logs',False),('ids-jobs.json',f'{REPO}/actions/runs/34751393871/jobs?per_page=100',False)]
requests += [(name+'.zip',f'{REPO}/actions/artifacts/{r["id"]}/zip',False) for name,r in selected.items()]
def one(row):
    name,url,raw=row;cmd=[GH,'api',url]+(['--allow-escape-sequences'] if raw else []);start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    cp=subprocess.run(cmd,capture_output=True,env=dict(os.environ,GH_PROMPT_DISABLED='1'))
    (A/name).write_bytes(cp.stdout);(A/(name+'.stderr')).write_bytes(cp.stderr)
    return name,{'argv':cmd,'utc_start':start,'exit_code':cp.returncode,'bytes':len(cp.stdout),'sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr)}
with ThreadPoolExecutor(max_workers=4) as pool:cmds=dict(pool.map(one,requests))
(A/'commands.json').write_text(json.dumps(cmds,indent=2)+'\n');assert all(x['exit_code']==0 for x in cmds.values()),cmds
archives={}
for name in ['lean-IE-05.zip','lean-checker-controls.zip','runlogs.zip']:
    q=A/name;out=A/name[:-4];out.mkdir();members={}
    with zipfile.ZipFile(q) as z:
        assert z.testzip() is None
        for i in z.infolist():
            r=PurePosixPath(i.filename);assert not r.is_absolute() and '..' not in r.parts
            assert stat.S_IFMT(i.external_attr>>16)!=stat.S_IFLNK
            if i.is_dir():continue
            assert str(r) not in members
            b=z.read(i);f=out/str(r);f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
            members[str(r)]={'sha256':sha(b),'bytes':len(b),'CRC':i.CRC}
    rec={'sha256':sha(q.read_bytes()),'members':members,'member_count':len(members)}
    if name[:-4] in selected:
        md=selected[name[:-4]];assert 'sha256:'+rec['sha256']==md['digest'] and q.stat().st_size==md['size_in_bytes']
        rec['artifact_metadata']=md
    archives[name]=rec
original=Path('/tmp/nla-lean-formalization/ie05-linux-run-34751393873/ie05-artifact')
got=A/'lean-IE-05';names={str(x.relative_to(got)) for x in got.rglob('*') if x.is_file()}
assert names=={str(x.relative_to(original)) for x in original.rglob('*') if x.is_file()}
for n in names:assert (got/n).read_bytes()==(original/n).read_bytes(),n
result={'success':True,'commands':cmds,'archives':archives,'earlier_parent_IE05_extraction_matches_all_files':True,'metadata_api_snapshot':'api-jlvyv9bw','raw_log_note':'Earlier gh API calls refused ANSI bytes. Documented --allow-escape-sequences is used only to capture original bytes to files; no raw terminal rendering.'}
(A/'result.json').write_text(json.dumps(result,indent=2)+'\n');(E/'DOWNLOADS.json').write_text(json.dumps({'directory':A.name,'result_sha256':sha((A/'result.json').read_bytes())},indent=2)+'\n')
print(json.dumps({'directory':str(A),'success':True,'archives':{n:{k:v for k,v in r.items() if k not in ['members','artifact_metadata']} for n,r in archives.items()}},indent=2))
