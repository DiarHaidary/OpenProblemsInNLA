#!/usr/bin/env python3
"""Retain and correct stale candidate-phase prose found in the author review."""
from pathlib import Path
import json,shutil
E=Path(__file__).resolve().parent;P=E.parents[1]
d=E/'initial-text';d.mkdir()
for n in ['README.md','formalization.yaml']:shutil.copyfile(P/n,d/n)
f=P/'formalization.yaml';s=f.read_text()
a='before this candidate-document installation. No actual RA20 Linux success is asserted. Actual Ubuntu run'
b='before the historical candidate-document installation. The later actual Ubuntu run'
assert a in s;s=s.replace(a,b)
a='''    historical_inventory_mapping: Only the exact README.md path when expecting SHA256 7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50
      maps to verification/pre-candidate-README.md. Every other prior path/hash remains unchanged, including
      both full final referee inventories.'''
b='''    historical_inventory_mapping: At the candidate stage, only the exact README.md path expecting SHA256
      7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50 mapped to verification/pre-candidate-README.md.
      That mapping remains valid. The later publication archives listed below preserve the exact checked
      candidate README and metadata and canonical-page inputs for every full historical inventory.'''
assert a in s;f.write_text(s.replace(a,b))
f=P/'README.md';s=f.read_text()
a='''preceded the committed candidate. `/root/ra20_final_referee1` subsequently
authored the candidate and publication documents; that author role adds no'''
b='''preceded the committed candidate. After its independent mathematical review,
`/root/ra20_final_referee1` authored the candidate documents and later these
publication documents; that author role adds no'''
assert a in s;s=s.replace(a,b)
s=s.replace('their actual method; this candidate-document task ran no new Lean build.','their actual method; candidate-document and publication preparation ran no new Lean build.')
f.write_text(s)
(E/'phase-wording-correction.json').write_text(json.dumps({'reason':'Author review found one stale no-Linux-success candidate sentence and clarified the historical mapping and role chronology','initial_wrappers_retained':'initial-text/','canonical_PDF_affected':False,'independent_review':'not claimed'},indent=2)+'\n')
print('Current-phase wording corrected; prior draft bytes retained; canonical PDF unchanged.')
