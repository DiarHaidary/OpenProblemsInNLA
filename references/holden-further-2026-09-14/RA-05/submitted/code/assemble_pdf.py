#!/usr/bin/env python3
"""Assemble the new proof and the unchanged even-power proof into one PDF."""
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import json
ROOT=Path(__file__).resolve().parents[1]
parts=[('Part I: full theorem and non-even proof','part_i_non_even.pdf'),
       ('Part II: provenance and scope','part_ii_cover.pdf'),
       ('Part II: complete even-power proof (unchanged)','part_ii_even.pdf')]
writer=PdfWriter(); records=[]
for title,name in parts:
    path=ROOT/'manuscript'/name
    if not path.is_file(): raise FileNotFoundError(path)
    start=len(writer.pages); reader=PdfReader(str(path))
    writer.append(reader,outline_item=title,import_outline=True)
    records.append({'title':title,'file':'manuscript/'+name,'start_pdf_page':start+1,'pages':len(reader.pages)})
writer.add_metadata({'/Title':'RA-05: Strong row coresets and the even/non-even dichotomy',
                     '/Author':'Prepared for Sidney Holden with ChatGPT',
                     '/Subject':'Complete resolution claim for all fixed real p>2, pending independent review',
                     '/Keywords':'RA-05, coresets, non-even powers, Walsh spectrum, tensor amplification, restricted invertibility'})
out=ROOT/'RA05_full_resolution.pdf'
with out.open('wb') as f: writer.write(f)
result={'path':out.name,'pages':len(writer.pages),'parts':records,'status':'complete resolution claimed; not independently verified'}
(ROOT/'results/pdf_assembly.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
