"""Apply two IS-02-only page-break changes after tools/render_problems.py.

No mathematical wording or shared renderer changes. Compile the standalone TeX
with XeLaTeX twice, retain the final warning record, and replace only problem.pdf.
"""
from pathlib import Path
import json
import re
import shutil
import subprocess
import tempfile

source = Path('/tmp/nla-lean-is02-worktree/eigenvalues-and-inverse-problems/IS-02/problem.tex')
review = Path('/tmp/nla-is02-publication-review')
tex = source.read_text()
assert tex.count(r'\subsection{Problem statement}') == 1
assert tex.count('\\newpage\n\\subsection{References}') == 1
tex = tex.replace(r'\subsection{Problem statement}', '\\newpage\n\\subsection{Problem statement}', 1)
tex = tex.replace('\\newpage\n\\subsection{References}', r'\subsection{References}', 1)
source.write_text(tex)
records = []
with tempfile.TemporaryDirectory(prefix='nla-is02-final-pdf-') as temp:
    temp = Path(temp)
    (temp / 'problem.tex').write_text(tex)
    for i in range(2):
        command = ['/Library/TeX/texbin/xelatex', '-interaction=nonstopmode', '-halt-on-error', 'problem.tex']
        result = subprocess.run(command, cwd=temp, capture_output=True, text=True)
        (review / f'xelatex-layout-{i+1}.log').write_text(result.stdout + result.stderr)
        records.append({'command':command, 'cwd':str(temp), 'exit_code':result.returncode})
        if result.returncode:
            (review / 'render-layout-commands.json').write_text(json.dumps(records, indent=2) + '\n')
            raise SystemExit(result.returncode)
    log = (temp / 'problem.log').read_text()
    warnings = re.findall(r'(?:Overfull[^\n]+|Missing character[^\n]+)', log)
    assert not warnings, warnings
    shutil.copyfile(temp / 'problem.pdf', source.with_suffix('.pdf'))
(review / 'render-layout-commands.json').write_text(json.dumps({'commands':records,'warnings':warnings}, indent=2) + '\n')
print('IS-02 canonical PDF rebuilt; complete original statement starts on page2; no overfull or missing-character warnings.')
