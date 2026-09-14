from __future__ import annotations
import datetime,hashlib,json,os,re,shutil,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def build():
    required=['report.tex','README.md','PROOF_AUDIT.md','STATUS.json','claims.json',
              'src/capacity.py','tests/test_capacity.py','results/verification.json',
              'results/linear_vs_prefix_certificate.json']
    for name in required:
        if not (ROOT/name).is_file():raise FileNotFoundError(name)
    exact=subprocess.run([sys.executable,'exact_rank_certificate.py','--verify'],cwd=ROOT,
                         capture_output=True,text=True,timeout=20)
    (ROOT/'results'/'exact_certificate_verification.txt').write_text(exact.stdout+exact.stderr)
    if exact.returncode:raise RuntimeError('Exact certificate verification failed')
    # Compile from the current source; no stale PDF is accepted as a build success.
    engine=shutil.which('pdflatex')
    pdf=ROOT/'report.pdf'
    build_record={'engine':engine,'source_sha256':sha(ROOT/'report.tex'),'passes':[]}
    if engine:
        for i in (1,2):
            proc=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','report.tex'],
                cwd=ROOT,capture_output=True,text=True,timeout=35)
            (ROOT/'results'/f'latex_final_pass{i}.txt').write_text(proc.stdout+proc.stderr)
            build_record['passes'].append(proc.returncode)
            if proc.returncode:break
    success=bool(engine and build_record['passes']==[0,0] and pdf.is_file() and pdf.stat().st_size>1000)
    build_record['full_latex_pdf']=success
    if not success:
        # Always make an honest readable fallback rather than a broken PDF link.
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
        from xml.sax.saxutils import escape
        styles=getSampleStyleSheet();story=[]
        story.append(Paragraph('RA-14: continuation package',styles['Title']))
        story.append(Paragraph('PARTIAL. The full mathematical manuscript is in report.tex. Its LaTeX build did not complete in this environment; build logs are retained. This PDF is an artifact-status summary, not a substitute for the mathematical source.',styles['BodyText']))
        story.append(Spacer(1,14))
        for paragraph in (ROOT/'README.md').read_text().split('\n\n'):
            if paragraph.strip():story.append(Paragraph(escape(paragraph).replace('\n','<br/>'),styles['BodyText']));story.append(Spacer(1,7))
        SimpleDocTemplate(str(pdf),pagesize=letter,rightMargin=54,leftMargin=54,topMargin=54,bottomMargin=54).build(story)
    try:
        import fitz
        document=fitz.open(pdf)
        texts=[page.get_text() for page in document]
        build_record['pages']=len(document)
        build_record['text_characters']=sum(map(len,texts))
        build_record['scope_text_present']=any('not completed' in t.lower() or 'partial' in t.lower() for t in texts)
        assert len(document)>0 and build_record['text_characters']>100
        preview_dir=Path('/mnt/data/RA14_v7_previews');preview_dir.mkdir(exist_ok=True)
        for index in sorted({0,min(3,len(document)-1),len(document)-1}):
            document[index].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(preview_dir/f'page_{index+1:02d}.png')
        rectangles=[]
        for i,page in enumerate(document):
            for word in page.get_text('words'):
                x0,y0,x1,y1=word[:4]
                if x0 < -1 or y0 < -1 or x1>page.rect.width+1 or y1>page.rect.height+1:
                    rectangles.append({'page':i+1,'word':word[4],'box':[x0,y0,x1,y1]})
        build_record['outside_page_words']=rectangles
        document.close()
    except ImportError:
        build_record['rendering']='PyMuPDF unavailable'
    log=(ROOT/'report.log').read_text(errors='replace') if (ROOT/'report.log').exists() else ''
    build_record['overfull_boxes']=re.findall(r'Overfull \\hbox[^\n]*',log)
    build_record['undefined_references']=bool(re.search(r'There were undefined references',log))
    (ROOT/'results'/'pdf_build.json').write_text(json.dumps(build_record,indent=2)+'\n')
    # Exclude transient compilation and Python cache files from the deliverable.
    for pattern in ('*.aux','*.out','*.toc','*.log'):
        for p in ROOT.glob(pattern):p.unlink()
    for p in list(ROOT.rglob('__pycache__')):
        shutil.rmtree(p)
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.name!='MANIFEST.json':
            if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2','.pfb'}:
                raise RuntimeError('Raw font files are not permitted in this artifact')
            files.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'meaning':'File-byte integrity only, not mathematical correctness','files':files}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    verification=subprocess.run([sys.executable,'verify_manifest.py'],cwd=ROOT,capture_output=True,text=True,timeout=20)
    assert verification.returncode==0,verification.stdout+verification.stderr
    out=ROOT.parent/'RA14_adaptive_capacity_v7.zip'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file():z.write(p,arcname=f'{ROOT.name}/{p.relative_to(ROOT).as_posix()}')
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        assert f'{ROOT.name}/report.pdf' in z.namelist()
        assert f'{ROOT.name}/report.tex' in z.namelist()
    standalone=ROOT.parent/'RA14_adaptive_capacity_v7.pdf'
    shutil.copy2(pdf,standalone)
    delivery={'zip':str(out),'zip_bytes':out.stat().st_size,'zip_sha256':sha(out),
              'pdf':str(standalone),'full_latex_pdf':success,
              'new_tests':json.loads((ROOT/'results'/'verification.json').read_text()),
              'exact_rank_certificate':'verified','manifest':verification.stdout.strip(),
              'status':'PARTIAL','unrestricted_gap_closed':False}
    (ROOT.parent/'RA14_v7_delivery.json').write_text(json.dumps(delivery,indent=2)+'\n')
    print(json.dumps(delivery,indent=2))
    return delivery

if __name__=='__main__':build()
