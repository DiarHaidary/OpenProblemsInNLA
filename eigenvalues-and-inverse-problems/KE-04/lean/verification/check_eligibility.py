#!/usr/bin/env python3
"""Read-only bounded upstream eligibility check, before KE-04 statement drafting."""
import datetime,hashlib,json,os,pathlib,subprocess,tempfile,urllib.parse,urllib.request
P=pathlib.Path(__file__).resolve().parents[1]
E=P/'verification'
G=pathlib.Path('/tmp/nla-lean-ra20-worktree')
REPO='ajt60gaibb/OpenProblemsInNLA'
def save(name,obj):(E/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def main():
    global E
    E=pathlib.Path(tempfile.mkdtemp(prefix='eligibility-attempt-',dir=E))
    r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'bounded pre-draft eligibility','commands':[],
       'source_note_is_not_approval':True,'scope':'Current upstream main and all-state upstream PR title/body searches for KE-04, KE04, and block Lanczos; not private, deleted, or unidentifiably named work.'}
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    argv=['git','ls-remote','https://github.com/'+REPO+'.git','refs/heads/main']
    cp=subprocess.run(argv,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    r['commands'].append({'argv':argv,'exit_code':cp.returncode,'output':cp.stdout})
    save('preflight.json',r)
    print(json.dumps(r['commands'][-1]),flush=True)
    assert cp.returncode==0
    base=cp.stdout.split()[0];r['upstream_main']=base
    def show(path):
        argv=['git','-C',str(G),'show',base+':'+path]
        data=subprocess.check_output(argv,env=env)
        r['commands'].append({'argv':argv,'exit_code':0,'output_sha256':hashlib.sha256(data).hexdigest(),'output_bytes':len(data)})
        return data
    registry=json.loads(show('problem_ids.json'))
    path=registry['KE-04'];r['canonical_path']=path
    assert path=='eigenvalues-and-inverse-problems/KE-04/README.md'
    canonical=show(path).decode();assert '**Status:** Solved' in canonical
    r['canonical_status']='Solved'
    argv=['git','-C',str(G),'ls-tree','-r','--name-only',base,path.rsplit('/',1)[0]]
    output=subprocess.check_output(argv,env=env,text=True)
    r['commands'].append({'argv':argv,'exit_code':0,'output':output})
    r['canonical_files']=output.splitlines()
    r['canonical_lean_files']=[x for x in output.splitlines() if '/lean/' in x or x.endswith('.lean')]
    assert not r['canonical_lean_files']
    r['queries']=[]
    try:
        for term in ['"KE-04"','KE04','"block Lanczos"']:
            query='repo:'+REPO+' is:pr in:title,body '+term
            url='https://api.github.com/search/issues?'+urllib.parse.urlencode({'q':query,'per_page':100})
            req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'Codex-KE04-statement-source-audit'})
            with urllib.request.urlopen(req,timeout=30) as response:raw=response.read()
            data=json.loads(raw);assert not data['incomplete_results'] and data['total_count']<=100
            r['queries'].append({'url':url,'query':query,'all_states':True,'response_sha256':hashlib.sha256(raw).hexdigest(),
                'total_count':data['total_count'],'incomplete_results':data['incomplete_results'],
                'items':[{k:item.get(k) for k in ['number','title','state','html_url','body','created_at','updated_at','closed_at','pull_request']} for item in data['items']]})
        r['pass']=True
    except Exception as ex:
        r['pass']=False;r['network_failure']=repr(ex)
        raise
    finally:save('eligibility-query.json',r)
    print(json.dumps({'pass':True,'base':base,'canonical_status':r['canonical_status'],'canonical_lean_files':[],
        'queries':[{'query':q['query'],'count':q['total_count'],'numbers':[i['number'] for i in q['items']]} for q in r['queries']]}))
if __name__=='__main__':main()
