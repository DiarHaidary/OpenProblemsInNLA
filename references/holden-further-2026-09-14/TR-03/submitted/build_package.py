"""Rebuild supporting records and archive; does not certify mathematical claims."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess, zipfile, datetime
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'TR03_all_spectra_bound.zip'
assert (ROOT/'TR03_all_spectra_bound.tex').is_file()
assert (ROOT/'README.md').is_file()
results=ROOT/'results';results.mkdir(exist_ok=True)
provenance=[]
for name in ['TR03_analysis.zip','TR03_continuation.zip','TR03_reduction_addendum.zip']:
    original=ROOT.parent/name;dest=ROOT/'prior'/name
    assert original.is_file(),f'Missing supplied archive: {name}'
    dest.parent.mkdir(exist_ok=True);shutil.copyfile(original,dest)
    a=hashlib.sha256(original.read_bytes()).hexdigest();b=hashlib.sha256(dest.read_bytes()).hexdigest();assert a==b
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        assert not any(Path(p).suffix.lower() in {'.ttf','.otf','.woff','.woff2'} for p in z.namelist())
    provenance.append({'file':name,'sha256':a,'byte_for_byte_preserved':True,'bytes':dest.stat().st_size})
(results/'prior_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')

# Recompile and retain the actual outcome.
engine=shutil.which('pdflatex');compilation={'engine':engine,'attempted':bool(engine),'success':False}
if engine:
    outcomes=[]
    for i in (1,2):
        try:
            p=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','TR03_all_spectra_bound.tex'],cwd=ROOT,capture_output=True,text=True,timeout=90)
            (results/f'latex_pass{i}.log').write_text(p.stdout+'\n'+p.stderr)
            outcomes.append(p.returncode)
            if p.returncode:break
        except Exception as ex:
            compilation['error']=repr(ex);break
    compilation['returncodes']=outcomes
    compilation['success']=outcomes==[0,0] and (ROOT/'TR03_all_spectra_bound.pdf').is_file()
(results/'compilation.json').write_text(json.dumps(compilation,indent=2)+'\n')

layout={'attempted':False,'limitations':'Automated checks do not replace visual inspection.'}
pdf=ROOT/'TR03_all_spectra_bound.pdf'
if pdf.is_file():
    try:
        import fitz
        doc=fitz.open(pdf);layout.update(attempted=True,pages=len(doc),page_text_lengths=[],out_of_page_blocks=[])
        previews=ROOT.parent/'TR03_all_spectra_preview';previews.mkdir(exist_ok=True)
        for i,page in enumerate(doc):
            text=page.get_text();layout['page_text_lengths'].append(len(text))
            for block in page.get_text('blocks'):
                x0,y0,x1,y1=block[:4]
                if x0<0 or y0<0 or x1>page.rect.width+1 or y1>page.rect.height+1:
                    layout['out_of_page_blocks'].append({'page':i+1,'bbox':[x0,y0,x1,y1]})
            # Render every page, not only the title page.
            page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(previews/f'page-{i+1:02}.png')
        layout['nonempty_pages']=all(n>20 for n in layout['page_text_lengths'])
        layout['no_out_of_page_blocks']=not layout['out_of_page_blocks']
        log=(ROOT/'TR03_all_spectra_bound.log').read_text(errors='replace') if (ROOT/'TR03_all_spectra_bound.log').exists() else ''
        layout['overfull_box_messages']=re.findall(r'Overfull[^\n]*',log)
        layout['undefined_reference_warning']='There were undefined references' in log
        try:
            from PIL import Image,ImageOps,ImageDraw
            thumbs=[]
            for p in sorted(previews.glob('page-*.png')):
                im=Image.open(p).convert('RGB');im.thumbnail((260,370))
                tile=Image.new('RGB',(280,400),'white');tile.paste(im,((280-im.width)//2,5));ImageDraw.Draw(tile).text((10,380),p.stem,fill='black');thumbs.append(tile)
            columns=4;rows=(len(thumbs)+columns-1)//columns
            sheet=Image.new('RGB',(columns*280,rows*400),(220,220,220))
            for i,tile in enumerate(thumbs):sheet.paste(tile,((i%columns)*280,(i//columns)*400))
            sheet.save(previews/'contact-sheet.png')
        except Exception as ex:layout['contact_sheet_error']=repr(ex)
        doc.close()
    except Exception as ex:layout['error']=repr(ex)
(results/'layout_audit.json').write_text(json.dumps(layout,indent=2)+'\n')

# A readable status distinguishes the process result from completion of TR-03.
execution_path=results/'execution.json'
execution=json.loads(execution_path.read_text()) if execution_path.exists() else {'status':'not_recorded'}
verification_path=results/'verification.json'
verification=json.loads(verification_path.read_text()) if verification_path.exists() else None
summary={'mathematical_completion':'partial','full_solution':False,'verification_execution':execution,
         'recorded_check_groups':verification.get('check_groups') if verification else None,
         'recorded_all_checks_passed':verification.get('all_checks_passed') if verification else None,
         'pdf_compilation':compilation,'pdf_page_count':layout.get('pages'),
         'formal_certification':False,'independent_peer_review':False}
(results/'package_status.json').write_text(json.dumps(summary,indent=2)+'\n')

# Remove intermediate compiler files and bytecode from the deliverable.
for suffix in ('.aux','.log','.out','.toc'):
    f=ROOT/('TR03_all_spectra_bound'+suffix)
    if f.exists():f.unlink()
for d in ROOT.rglob('__pycache__'):shutil.rmtree(d)
manifest=ROOT/'SHA256SUMS'
entries=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p!=manifest:
        assert p.suffix.lower() not in {'.ttf','.otf','.woff','.woff2'}
        entries.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT)))
manifest.write_text('\n'.join(entries)+'\n')
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(ROOT.parent))
with zipfile.ZipFile(OUT) as z:assert z.testzip() is None
print(json.dumps(summary,indent=2))
print('Archive:',OUT,'bytes:',OUT.stat().st_size)
