from pathlib import Path
import subprocess, json, hashlib, re

r = Path('/tmp/nla-lean-is02-worktree')
p = r/'eigenvalues-and-inverse-problems/IS-02'
out = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
checks = {}
old = subprocess.check_output(['git','show','HEAD:eigenvalues-and-inverse-problems/IS-02/README.md'],cwd=r,text=True)
new = (p/'README.md').read_text()
section = lambda s:s.split('## Problem statement\n',1)[1].split('## References',1)[0]
assert section(old) == section(new)
checks['original_mathematical_target_byte_identical'] = True
checks['unchanged_manuscripts'] = {}
for name in ['solution.md','solution.tex','solution.pdf']:
    original = subprocess.check_output(['git','show','HEAD:eigenvalues-and-inverse-problems/IS-02/'+name],cwd=r)
    assert original == (p/name).read_bytes()
    checks['unchanged_manuscripts'][name] = sha(original)
assert (r/'problem_ids.json').read_bytes() == subprocess.check_output(['git','show','HEAD:problem_ids.json'],cwd=r)
for path in ['tools','docs/lean/ci-toolchain','.github/workflows']:
    assert not subprocess.check_output(['git','diff','--name-only','--',path],cwd=r)
checks['shared_tools_registry_unchanged'] = True
res = subprocess.run(['/tmp/nla-lean-formalization/venv/bin/python',str(p/'lean/verification/verify_publication.py')],cwd=r,text=True,capture_output=True)
(out/'offline-check.log').write_text(res.stdout+res.stderr)
assert res.returncode == 0
checks['offline_checker'] = {'exit_code':res.returncode,'log_sha256':sha((res.stdout+res.stderr).encode())}
checks['publication_inputs'] = {}
for name in ['README.md','problem.tex','problem.pdf','lean/README.md','lean/formalization.yaml','lean/verification/verify_publication.py','lean/verification/package-inputs.json']:
    checks['publication_inputs'][name] = sha((p/name).read_bytes())
for name in ['README.md','lean/README.md','lean/formalization.yaml']:
    text = (p/name).read_text()
    normalized = ' '.join(text.split())
    assert 'George Stepaniants' in normalized and 'Department of Computing and Mathematical Sciences' in normalized and 'California Institute' in normalized
    assert not any('stepaniants' in e.lower() or 'george' in e.lower() for e in re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',text))
checks['attribution_privacy'] = True
tex = (p/'problem.tex').read_text()
assert '\\newpage\n\\subsection{Problem statement}' in tex
assert '\\newpage\n\\subsection{References}' not in tex
checks['visual_inspection'] = 'Root independently viewed both final PNG pages: full original statement together; no clipping/overlap/glyph loss.'
checks['prior_checks'] = {}
q = Path('/tmp/nla-is02-publication-review')
for name in ['REPORT.md','PUBLICATION-CHECKS.json','problem-id-tests.log','catalog.log','render.log','xelatex-layout-1.log','xelatex-layout-2.log']:
    checks['prior_checks'][name] = sha((q/name).read_bytes())
(out/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
print('IS02 independent publication checks PASS')
