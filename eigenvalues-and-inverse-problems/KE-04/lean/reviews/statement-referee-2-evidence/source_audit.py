"""One batched read-only audit of exact original and selected reference sources."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, traceback
E=Path(__file__).resolve().parent;P=E.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
    out=E/'source-audit';assert not out.exists();out.mkdir()
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Fresh read-only Git/blob identities and selected API searches; no new public status or exhaustive literature claim','commands':[],'files':{},'errors':[]}
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    def run(args,cwd,label,data=None,allowed=(0,)):
        cp=subprocess.run(args,cwd=cwd,env=env,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (out/(label+'.stdout')).write_bytes(cp.stdout);(out/(label+'.stderr')).write_bytes(cp.stderr)
        r={'command':args,'cwd':str(cwd),'stdin_utf8':data.decode() if data else None,'exit_code':cp.returncode,'stdout':label+'.stdout','stderr':label+'.stderr','stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr)}
        result['commands'].append(r)
        assert cp.returncode in allowed,r
        return cp.stdout
    try:
        original=load(P/'verification/original-source-inventory.json')['files']
        api=load(P/'verification/api-evidence-complete/manifest.json')['files']
        assert len(original)==17 and len(api)==33
        groups={};tau={}
        for name,r in (original|api).items():
            b=(P/name).read_bytes();assert sha(b)==r['sha256'] and len(b)==r['bytes']
            assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob']
            if 'tauceti/' in name:tau[name]=r;continue
            repo=r.get('repo') or r['actual_command'][2]
            groups.setdefault(repo,[]).append((name,r))
        for i,(repo,items) in enumerate(groups.items()):
            query=''.join(r['commit']+':'+r['upstream_path']+'\n' for name,r in items).encode()
            stream=run(['git','cat-file','--batch'],repo,'git-batch-'+str(i+1),query)
            pos=0
            for name,r in items:
                end=stream.index(b'\n',pos);blob,kind,size=stream[pos:end].decode().split();start=end+1
                b=stream[start:start+int(size)];pos=start+int(size)+1
                assert blob==r['git_blob'] and kind=='blob' and b==(P/name).read_bytes()
                result['files'][name]={'sha256':sha(b),'bytes':len(b),'git_blob':blob,'commit':r['commit'],'source_path':r['upstream_path'],'Git_content_equal':True}
                if name in api:assert b==(Path(repo)/r['upstream_path']).read_bytes()
            assert pos==len(stream)
        archive=P/'verification/api-evidence-complete/tauceti-archive'
        tree=load(archive/'TauCetiProject_TauCetiReview-tree.json');commit=load(archive/'TauCetiProject_TauCetiReview-commit.json')
        assert commit['sha']=='afb424eda89e8ac96d9eb69f6a88972055a4cd1b' and not tree['truncated']
        entries={r['path']:r for r in tree['tree']}
        hashes={}
        dirs=['']+[n for n,r in entries.items() if r['type']=='tree']
        for d in sorted(dirs,key=lambda x:x.count('/')+(1 if x else 0),reverse=True):
            direct=[r for n,r in entries.items() if str(Path(n).parent)==(d or '.')]
            direct.sort(key=lambda r:(Path(r['path']).name+('/' if r['type']=='tree' else '')).encode())
            payload=b''
            for r in direct:
                mode=r['mode'].lstrip('0');name=Path(r['path']).name
                blob=hashes[r['path']] if r['type']=='tree' else r['sha']
                payload+=mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(blob)
            value=hashlib.sha1(b'tree '+str(len(payload)).encode()+b'\0'+payload).hexdigest()
            expected=entries[d]['sha'] if d else commit['commit']['tree']['sha']
            assert value==expected,d
            hashes[d]=value
        for name,r in tau.items():
            b=(P/name).read_bytes();assert entries[r['upstream_path']]['sha']==r['git_blob']
            assert b==(Path(r['repo'])/r['upstream_path']).read_bytes()
            result['files'][name]={'sha256':sha(b),'bytes':len(b),'git_blob':r['git_blob'],'commit':r['commit'],'source_path':r['upstream_path'],'reconstructed_pinned_tree_binding':True}
        result['tauceti_trees_reconstructed']=hashes
        original_text=(P/'verification/original-submission/solution.md').read_text()
        current_text=(P/'verification/original-sources/eigenvalues-and-inverse-problems/KE-04/solution.md').read_text()
        proof=lambda s:s[s.index('## Theorem '):s.index('## Scope and review notes')].strip().encode()
        assert proof(original_text)==proof(current_text)
        result['original_current_proof_block']={'bytes':len(proof(original_text)),'sha256':sha(proof(original_text)),'equal':True}
        reg=load(P/'verification/original-sources/problem_ids.json')
        assert len(reg)==217 and reg['KE-04']=='eigenvalues-and-inverse-problems/KE-04/README.md'
        assert '**Status:** Solved' in (P/'verification/original-sources/eigenvalues-and-inverse-problems/KE-04/README.md').read_text()
        result['canonical_status_at_pinned_base']='Solved; permanent ID/path retained'
        mathlib=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages/mathlib')
        searches=[('spectral',['rg','-n','-A','5','-B','2','irreducible_def eigenvalues|irreducible_def eigenvectorBasis|eigenvalues_antitone|roots_charpoly_eq_eigenvalues|eigenvalues_eq_eigenvalues_iff|theorem apply_eigenvectorBasis','Mathlib/Analysis/InnerProductSpace/Spectrum.lean']),('real-action-and-basis',['rg','-n','-A','4','-B','2','def toEuclideanLin|toLpLin_apply|reindex_apply|def reindex|exists_orthonormalBasis|def orthonormalBasis','Mathlib/Analysis/InnerProductSpace/PiL2.lean']),('subspace-apis',['rg','-n','-A','4','-B','2','range_linearCombination|finrank_span_eq_card|finrank_sup_add_finrank_inf_eq|linearIndependent_iff_injective_fintypeLinearCombination','Mathlib/LinearAlgebra/Finsupp/LinearCombination.lean','Mathlib/LinearAlgebra/Dimension/Constructions.lean','Mathlib/LinearAlgebra/FiniteDimensional/Lemmas.lean','Mathlib/LinearAlgebra/LinearIndependent/Defs.lean']),('PSD-and-reversal',['rg','-n','-A','4','-B','2','dotProduct_mulVec_zero_iff|mul_mul_conjTranspose_same|rev_le_rev|def revPerm|theorem rev_rev','Mathlib/Analysis/Matrix/Order.lean','Mathlib/LinearAlgebra/Matrix/PosDef.lean','Mathlib/Data/Fin/Rev.lean'])]
        for label,args in searches:run(args,mathlib,label)
        run(['rg','-n','-A','8','-B','3','assert_trust|collectAxioms|def foundational|foundationalAxioms|register_option leancert.trust','LeanCert/Tactic/Verification.lean'],mathlib.parent/'leancert','LeanCert-kernel')
        result['source_counts']={'original_Git_files':17,'selected_reference_files':33,'selected_Git_reference_files':len(api)-len(tau),'TauCeti_tree_bound_files':len(tau)}
        result['status']='PASS exact originals and selected source bindings'
    except Exception:result['errors'].append(traceback.format_exc())
    result['success']=not result['errors'];save(out/'result.json',result)
    print(json.dumps({'success':result['success'],'counts':result.get('source_counts'),'commands':len(result['commands']),'errors':result['errors']},indent=2))
    raise SystemExit(0 if result['success'] else 1)
if __name__=='__main__':main()
