#!/usr/bin/env python3
"""Render attributed copies; keep submitted sources immutable. Requires Pandoc and TeX."""
import concurrent.futures,json,os,re,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AFFILIATION='Center for Computational Biology, Flatiron Institute, Simons Foundation'
SOURCES={'TR-03':['TR03_all_spectra_bound.tex'],'RA-14':['report.tex'], 'RA-11':['manuscript/ra11_probability_diagonal.md'],'SP-10':['report/REPORT.md'],'RA-05':['manuscript/part_i_non_even.tex','manuscript/part_ii_even.tex']}

def render(identifier):
    folder=ROOT/identifier
    status=json.loads((ROOT/'dispositions.json').read_text())[identifier]
    notice=status['notice']
    url='https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/reviews/2026-09-14-further-submissions/'+identifier+'-review.md'
    outputs=[]; warnings=[]
    for idx,rel in enumerate(SOURCES[identifier]):
        source=folder/'submitted'/rel
        text=source.read_text()
        name='manuscript' if len(SOURCES[identifier])==1 else 'part-'+str(idx+1)
        if source.suffix=='.md':
            text=re.sub(r'(?<![<(])https?://[^\s<>)]+' ,lambda m:'<'+m[0]+'>',text)
            title=text.splitlines()[0][2:]
            content='---\ntitle: '+json.dumps(title)+'\nauthor: Sidney Holden\ndate: 14 September 2026\n---\n\n**Affiliation:** '+AFFILIATION+'.\n\n**Submission disposition:** '+notice+'\n\n[Independent informal AI-agent review]('+url+'). ChatGPT assistance is disclosed. No Lean verification, external human peer review or formal verification is claimed. This dated notice supersedes historical statements about pending review; inherited claims are accepted only within the linked review scope.\n\n'+text.split('\n',1)[1]
            (folder/'manuscript.md').write_text(content)
            result=subprocess.run([os.environ.get('PANDOC','pandoc'),'--from=markdown+tex_math_dollars+tex_math_single_backslash+raw_tex','--to=latex','--standalone','-V','geometry:margin=25mm','-V','fontsize:10pt'],input=content,text=True,capture_output=True,check=True)
            result.stdout=re.sub(r'\\texttt\{([^{}]+)\}',lambda m:r'\nolinkurl{'+m[1].replace(r'\_', '_')+'}',result.stdout)
            tex=result.stdout.replace(r'\begin{document}', r'\usepackage{fvextra,xurl}'+'\n'+r'\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaklines=true,fontsize=\small}'+'\n'+r'\begin{document}',1)
        else:
            tex=text
            if identifier=='RA-14':
                tex=tex.replace(r'\tableofcontents',r'\newpage\tableofcontents',1)
                tex=tex.replace(r'\input{results/verification_summary.tex}',(folder/'submitted/results/verification_summary.tex').read_text(),1)
            byline=r'Sidney Holden\\{\small Center for Computational Biology}\\{\small Flatiron Institute, Simons Foundation}'
            if r'\author{}' in tex:
                tex=tex.replace(r'\author{}',r'\author{'+byline+'}',1).replace(r'\date{}',r'\date{14 September 2026}',1)
                tex=tex.replace(r'\vspace{-2em}','',1)
            tex=tex.replace('Prepared for Sidney Holden with ChatGPT',r'\textbf{Sidney Holden}\par Center for Computational Biology\par Flatiron Institute, Simons Foundation\par Prepared with ChatGPT assistance')
            # A dedicated dated cover preserves the source page structure.
            cover='\n\\begin{titlepage}\n\\thispagestyle{empty}\n{\\LARGE\\bfseries '+identifier+' submission}\\par\\bigskip\n{\\Large Sidney Holden}\\par\\medskip\n'+AFFILIATION+'.\\par\\medskip\n14 September 2026\\par\\bigskip\n\\textbf{Submission disposition.} '+notice+'\\par\\bigskip\n\\href{'+url+'}{Independent informal Codex AI-agent review}.\\par\\medskip\nChatGPT assistance is disclosed. No Lean verification, external human peer review or formal verification is claimed. This dated notice supersedes historical statements about pending review. Inherited claims are accepted only within the linked review scope.\\par\\bigskip\nThe mathematical body and its references are retained from the submitted source.\\par\n\\end{titlepage}\n'
            tex=tex.replace(r'\begin{document}',r'\usepackage{xurl}\setlength{\emergencystretch}{3em}'+'\n'+r'\hypersetup{pdfauthor={Sidney Holden}}'+'\n'+r'\begin{document}'+cover,1)
        with tempfile.TemporaryDirectory(prefix='nla-further-pdf-') as tmp:
            tmp=Path(tmp)
            if identifier=='RA-14':shutil.copytree(folder/'submitted/results',tmp/'results')
            (tmp/'report.tex').write_text(tex)
            engine=os.environ.get('XELATEX','xelatex') if source.suffix=='.md' else os.environ.get('PDFLATEX','pdflatex')
            for _ in range(2):
                result=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','report.tex'],cwd=tmp,text=True,errors='replace',capture_output=True)
                if result.returncode:raise RuntimeError(identifier+': '+result.stdout[-5000:])
            log=(tmp/'report.log').read_text(errors='replace')
            warnings.extend(re.findall(r'(?:Overfull[^\n]+|Missing character[^\n]+|[^\n]*undefined[^\n]*)',log))
            (folder/(name+'.tex')).write_text(tex)
            shutil.copyfile(tmp/'report.pdf',folder/(name+'.pdf'))
            outputs.append(folder/(name+'.pdf'))
    if len(outputs)>1:
        from pypdf import PdfWriter
        writer=PdfWriter()
        for output in outputs:writer.append(output)
        writer.add_metadata({'/Author':'Sidney Holden','/Title':'RA-05: Strong row coresets, even/non-even dichotomy'})
        writer.write(folder/'manuscript.pdf')
    return identifier,warnings

if __name__=='__main__':
    import sys
    ids=sys.argv[1:] or list(SOURCES)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for identifier,warnings in pool.map(render,ids):print(identifier+': '+('; '.join(warnings) if warnings else 'OK'),flush=True)
