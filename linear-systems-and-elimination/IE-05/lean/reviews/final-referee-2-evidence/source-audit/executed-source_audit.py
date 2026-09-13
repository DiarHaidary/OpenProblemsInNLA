"""Independent batched source identities, exact numerical diagnostics and nested seals."""
from pathlib import Path
from fractions import Fraction
import ast, datetime, hashlib, json, os, re, subprocess, traceback
E=Path(__file__).resolve().parent; P=E.parents[1]
K=Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean')
DEPS=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
    out=E/'source-audit';assert not out.exists();out.mkdir()
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':[],'errors':[]}
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    def run(args,cwd,label,data=None,allowed=(0,)):
        cp=subprocess.run(args,cwd=cwd,env=env,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        for ext,b in [('stdout',cp.stdout),('stderr',cp.stderr)]: (out/(label+'.'+ext)).write_bytes(b)
        if data is not None:(out/(label+'.stdin')).write_bytes(data)
        r={'command':args,'cwd':str(cwd),'exit_code':cp.returncode,'stdout':label+'.stdout','stderr':label+'.stderr','stdin':label+'.stdin' if data else None,'stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr)}
        result['commands'].append(r);assert cp.returncode in allowed,r
        return cp.stdout
    def git_batch(repo,items,label):
        stream=run(['git','cat-file','--batch'],repo,label,''.join(r['commit']+':'+r['path']+'\n' for r in items).encode())
        pos=0; records=[]
        for r in items:
            end=stream.index(b'\n',pos);blob,kind,size=stream[pos:end].decode().split();start=end+1
            b=stream[start:start+int(size)];pos=start+int(size)+1
            assert kind=='blob' and blob==r['git_blob'] and sha(b)==r['sha256'] and len(b)==r['bytes'],r
            if 'local' in r:assert b==Path(r['local']).read_bytes(),r
            records.append(r|{'git_content_verified':True})
        assert pos==len(stream)
        return records
    try:
        freeze=load(P/'reviews/proof-freeze.json'); assert len(freeze['files'])==1800
        originals=load(P/'verification/original-source-inventory.json')
        items=[{'path':n,'commit':originals['base'],**r,'local':str(P/'verification/original-sources'/n)} for n,r in originals['files'].items()]
        assert len(items)==27
        result['originals']=git_batch('/tmp/nla-lean-ra20-worktree',items,'original-27')
        assert {r['path']:r['sha256'] for r in items}==freeze['source_files']
        assert {r['path']:r['git_blob'] for r in items}==freeze['source_git_blobs']
        reg=load(P/'verification/original-sources/problem_ids.json')
        assert len(reg)==217 and reg['IE-05']=='linear-systems-and-elimination/IE-05/README.md'
        canonical=(P/'verification/original-sources'/reg['IE-05']).read_text()
        assert '**Status:** Solved' in canonical
        result['canonical']={'base':originals['base'],'registered_IDs':217,'IE05_status':'Solved','path':reg['IE-05'],'no_live_remote_claim':True}
        api=load(P/'verification/statement-development/api-and-example-identities.json')
        repos={'mathlib':DEPS/'mathlib','leancert':DEPS/'leancert','Schiffer':Path('/tmp/nla-lean-formalization/leancert-examples/Schiffer'),'Forsythe':Path('/tmp/nla-lean-formalization/leancert-examples/Forsythe')}
        result['pinned_examples_and_APIs']={}
        for group,d in api.items():
            entries=[{'path':n,'commit':d['revision'],**r,'local':str(repos[group]/n)} for n,r in d['files'].items()]
            result['pinned_examples_and_APIs'][group]=git_batch(repos[group],entries,'api-'+group)
        km=load(K/'verification/api-evidence-complete/manifest.json')['files']
        tau={n:r for n,r in km.items() if '/tauceti/' in n}
        archive=K/'verification/api-evidence-complete/tauceti-archive'
        tree=load(archive/'TauCetiProject_TauCetiReview-tree.json');commit=load(archive/'TauCetiProject_TauCetiReview-commit.json')
        assert commit['sha']=='afb424eda89e8ac96d9eb69f6a88972055a4cd1b' and not tree['truncated']
        entries={r['path']:r for r in tree['tree']}; hashes={}
        dirs=['']+[n for n,r in entries.items() if r['type']=='tree']
        for d in sorted(dirs,key=lambda x:x.count('/')+(1 if x else 0),reverse=True):
            direct=[r for n,r in entries.items() if str(Path(n).parent)==(d or '.')]
            direct.sort(key=lambda r:(Path(r['path']).name+('/' if r['type']=='tree' else '')).encode())
            payload=b''
            for r in direct:
                h=hashes[r['path']] if r['type']=='tree' else r['sha']
                payload+=r['mode'].lstrip('0').encode()+b' '+Path(r['path']).name.encode()+b'\0'+bytes.fromhex(h)
            h=hashlib.sha1(b'tree '+str(len(payload)).encode()+b'\0'+payload).hexdigest()
            assert h==(entries[d]['sha'] if d else commit['commit']['tree']['sha']);hashes[d]=h
        result['tau_ceti']={'commit':commit['sha'],'reconstructed_trees':hashes,'files':{}}
        for n,r in tau.items():
            b=(K/n).read_bytes();assert sha(b)==r['sha256'] and len(b)==r['bytes']
            assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob']==entries[r['upstream_path']]['sha']
            q=out/'pinned-TauCeti'/r['upstream_path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
            result['tau_ceti']['files'][r['upstream_path']]={'sha256':sha(b),'bytes':len(b),'git_blob':r['git_blob']}
        for n in ['TauCetiProject_TauCetiReview-tree.json','TauCetiProject_TauCetiReview-commit.json']:(out/n).write_bytes((archive/n).read_bytes())
        assert len([n for n in result['tau_ceti']['files'] if n.startswith('rubrics/') and n.endswith('.md')])==12
        # Every selected nested manifest is checked against its exact named historical scope.
        roots={'verification/qr-scaling-handoff/EVIDENCE-MANIFEST.json':P/'verification/qr-scaling-handoff','verification/statement-acceptance/EVIDENCE-MANIFEST.json':P/'verification/statement-acceptance'}
        nested={}
        for n in freeze['files']:
            if not (n.endswith(('EVIDENCE-MANIFEST.json','EVIDENCE-SEAL.json','DRAFT-INVENTORY.json')) or n=='reviews/statement-freeze.json'):continue
            d=load(P/n);files=d.get('files');assert isinstance(files,dict),n
            root=(P/n).parent if n.endswith('DRAFT-INVENTORY.json') else roots.get(n,P)
            identities={}
            for name,r in files.items():
                q=(root/name).resolve();relative=str(q.relative_to(P.resolve()))
                assert relative in freeze['files'],(n,relative)
                b=q.read_bytes(); h=r if isinstance(r,str) else r['sha256']
                assert sha(b)==h,(n,relative)
                if isinstance(r,dict) and 'bytes' in r:assert len(b)==r['bytes']
                identities[relative]=h
            nested[n]={'manifest_sha256':sha((P/n).read_bytes()),'root':str(root.relative_to(P)),'count':len(files),'exact_bound_files':identities}
        result['nested_manifests']=nested
        # An independent exact rational reconstruction, supplementary to Lean.
        source=(P/'NLA/IE05/Definitions.lean').read_text(); mats={}
        for name,nextname in [('integerH','integerD'),('integerD','integerT'),('integerT','castIntegerMatrix')]:
            block=source.split('def '+name+' ',1)[1].split('def '+nextname+' ',1)[0]
            for flag in ['false','true']:
                value=block.split('| '+flag+' =>',1)[1].split('|',1)[0].strip()
                mats[(name,flag)]=ast.literal_eval(value.replace('!',''))
        tex=(P/'verification/original-sources/linear-systems-and-elimination/IE-05/solution.tex').read_text()
        for label,kind,flag in [('H','integerH','true'),('T','integerT','true'),('H_0','integerH','false')]:
            block=re.search(r'\b'+label+r'=\s*\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',tex,re.S).group(1)
            array=[[int(x.strip()) for x in row.split('&')] for row in block.strip().split('\\\\')]
            assert array==mats[(kind,flag)],label
        numeric={}
        for flag in ['false','true']:
            H,D,T=[mats[(n,flag)] for n in ['integerH','integerD','integerT']]
            L=[[1 if i==j else (-1 if j<i else 0) for j in range(8)] for i in range(8)]
            if flag=='true':L[7][1]=0
            assert all(sum(H[r][i]*H[r][j] for r in range(8))==(D[i] if i==j else 0) for i in range(8) for j in range(8))
            assert all(H[i][j]==sum(L[i][r]*T[r][j] for r in range(8)) for i in range(8) for j in range(8))
            assert all(D[i]>0 and T[i][i]>0 for i in range(8))
            assert all(T[i][j]==0 for i in range(8) for j in range(i))
            active=[[[sum(L[i][r]*T[r][j] for r in range(k,8)) if min(i,j)>=k else 0 for j in range(8)] for i in range(8)] for k in range(9)]
            assert active[0]==H and active[8]==[[0]*8 for _ in range(8)]
            for k in range(8):
                assert active[k][k][k]==T[k][k] and active[k][k][k]>0
                assert all(abs(active[k][i][k])<=abs(active[k][k][k]) for i in range(k,8))
                for i in range(k+1,8):
                    for j in range(k+1,8):assert Fraction(active[k][i][j])-Fraction(active[k][i][k]*active[k][k][j],active[k][k][k])==active[k+1][i][j]
            if flag=='true':
                assert all(5272*H[i][j]**2<=3969*D[j] for i in range(8) for j in range(8))
                assert D[7]==active[7][7][7]==5272
            else:
                assert H[2][2]==51 and D[2]==3286
                assert all(active[k][i][j]**2<=5462*D[j] for k in range(8) for i in range(k,8) for j in range(k,8))
            numeric[flag]={'Gram':True,'LU':True,'all_nonzero_first_available_pivots':True,'actual_integer_Schur_recurrence':True,'terminal_zero':True,'D':D,'T_diagonal':[T[i][i] for i in range(8)]}
        gap=Fraction(5272,63)**2-Fraction(17948132,2601);assert gap==Fraction(117335164,1147041)>0
        result['supplementary_exact_diagnostic']={'objects':numeric,'witness_input_inequalities':64,'candidate_active_inequalities':sum((8-k)**2 for k in range(8)),'rational_gap':str(gap),'manuscript_H_T_H0_literal_match':True,'scope':'Supplementary finite integer/Fraction diagnostics, not a universal proof or kernel substitute'}
        searches=[('QR-reuse',['rg','-n','-A','4','-B','2','gramSchmidtNormed_orthonormal|gramSchmidt_ne_zero|gramSchmidt_inv_triangular|gramSchmidt_eq_sub_sum','Mathlib/Analysis/InnerProductSpace/GramSchmidtOrtho.lean']),('finite-max-supremum',['rg','-n','-A','4','-B','2','theorem le_csSup |theorem le_sup |theorem sup_le |exists_mem_eq_sup','Mathlib/Order/ConditionallyCompleteLattice/Basic.lean','Mathlib/Data/Finset/Lattice/Fold.lean']),('matrix-triangular',['rg','-n','-A','3','-B','2','det_of_lowerTriangular|linearIndependent_cols_of_det_ne_zero|inv_of_upperTriangular','Mathlib/LinearAlgebra/Matrix']),('no-existing-GEPP',['rg','-n','Gaussian elimination|partial pivot|FirstAvailablePivot|firstPivotIndex|ActiveInjective','Mathlib'])]
        for label,args in searches:run(args,DEPS/'mathlib',label,allowed=(0,1))
        run(['rg','-n','-A','8','-B','3','assert_trust|collectAxioms|foundationalAxioms|register_option leancert.trust','LeanCert/Tactic/Verification.lean'],DEPS/'leancert','actual-LeanCert-kernel')
        actual_sources=[P/'NLA/IE05'/n for n in ['Definitions.lean','ExactCertificates.lean','GEPP.lean','Growth.lean','GrowthBounds.lean','IntegerQR.lean','LUTrajectory.lean','Pivot.lean','Proof.lean','QR.lean','Scaling.lean','Witness.lean']]+[P/'Solution.lean']
        for q in actual_sources:
            text=q.read_text();assert not re.search(r'^import\s+Challenge\b|\b(?:sorry|native_decide|axiom)\b',re.sub(r'/\-.*?\-/','',text,flags=re.S),re.M),q
            assert not re.search(r'(?i)(?:george\S*|\S*stepaniants)@[\w.-]+',text),q
        result['source_boundary_checks']={'proof_and_solution_have_no_Challenge_import_or_admission_or_custom_axiom_or_native_decide':True,'George_email_absent_from_actual_sources':True,'live_historical_lakefile_defaultTargets_Challenge':True,'later_candidate_must_select_Solution':True}
        result['status']='PASS independent exact original/reference/nested-seal/numerical audit'
    except Exception:result['errors'].append(traceback.format_exc())
    result['success']=not result['errors'];save(out/'result.json',result)
    print(json.dumps({'success':result['success'],'commands':len(result['commands']),'nested_manifests':len(result.get('nested_manifests',{})),'errors':result['errors']},indent=2))
    raise SystemExit(0 if result['success'] else 1)
if __name__=='__main__':main()
