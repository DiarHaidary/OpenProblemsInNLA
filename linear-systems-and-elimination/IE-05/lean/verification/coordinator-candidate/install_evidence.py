"""Install sealed external packaging evidence beside the unchanged candidate."""
from pathlib import Path
import hashlib, json, shutil
P=Path('/tmp/nla-lean-ie05-worktree/linear-systems-and-elimination/IE-05/lean')
A=Path('/tmp/nla-lean-formalization/ie05-candidate-package')
E=Path('/tmp/nla-lean-formalization/ie05-candidate-independent-audit')
R=P/'verification/coordinator-candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ident=lambda p:{'sha256':sha(p),'bytes':p.stat().st_size}
assert not R.exists()
assert sha(P/'verification/candidate-inputs.json')=='b1259a165e924357b5474dcb9620ab316dec218e31a95665138cde4359f285e7'
assert sha(E/'REPORT.md')=='c14f6635b8e702fde6217b92bd49cfe25d2b693c191570fcadd0e4bb4dd681a3'
assert sha(E/'EVIDENCE-MANIFEST.json')=='a44510a7778510a7fd2988278fd8cdd0eeab07e92895f247848a4ddabd88312e'
R.mkdir()
copied={}
for root,target,skip in [(A,R/'author-external',True),(E,R/'independent-packaging',False)]:
    for q in sorted(root.rglob('*')):
        if skip and (q==root/'lean' or root/'lean' in q.parents):continue
        assert not q.is_symlink(),str(q)
        if q.is_file():
            to=target/q.relative_to(root);to.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(q,to);assert ident(to)==ident(q)
            copied[str(to.relative_to(P))]=ident(to)
assert len(copied)==112
(R/'installed-external-inputs.json').write_text(json.dumps(copied,indent=2)+'\n')
(R/'install_evidence.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({'exact_external_files_installed':len(copied),'existing_candidate_inputs_changed':False}))
