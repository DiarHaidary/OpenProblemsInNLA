#!/usr/bin/env python3
"""Prepare bounded helper input snapshots and admission-free expected types."""
from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent; P=E.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):
 p=E/n;assert not p.exists(),n;p.write_text(json.dumps(v,indent=2)+'\n')
pins={
 'reviews/statement-freeze.json':'bd329885eb323bd4f3fd40879649b56c201918d8c2bd6f63fbd0e86f48ca770c',
 'verification/proof-start.json':'2a8e4b4029a6ba005856c9ec56178cc7fefc8b8b16e945df27599ce471c95726',
 'NLA/IE05/ExactCertificates.lean':'5ee8f9bc7bc79b4e0e80b85c81952ae32689661dac405edd1559f92d6eb643af',
 'NLA/IE05/IntegerQR.lean':'fc87524d6aceddf208722daa33c855384e772425d54fd654f5f531250c67cc44',
 'verification/exactcert-diagnostic-referee/EVIDENCE-MANIFEST.json':'74d46f48c5d0a3b70da7925065b3a7c34fd7306d7a46120aee8a750bc8442420',
 'verification/gepp-development/EVIDENCE-MANIFEST.json':'f3854e99028561510756f6c58d024841d2e8cab4ce8d9315d45ac4b25eebd0d1',
 'verification/lu-development/EVIDENCE-MANIFEST.json':'9333e7615283fa9067b571a60f22488c884c435444d0f7a9221d8090ec5412a2',
 'verification/qr-scaling-handoff/EVIDENCE-MANIFEST.json':'b328744f06c3af7d3ae119ba28dc6d5a078ed79675d3e89fe888b6000c2f58c6'}
for n,h in pins.items():assert sha(P/n)==h,n
freeze=json.loads((P/'reviews/statement-freeze.json').read_text());assert len(freeze['files'])==733
assert json.loads((P/'verification/proof-start.json').read_text())['proof_authorized']
files=set(pins)|set(freeze['files'])|{'verification/certificates-qr-handoff/ROOT-NOTE.json'}
for n,h in freeze['files'].items():assert sha(P/n)==h,n
manifests=[]
for n in pins:
 if not n.endswith('EVIDENCE-MANIFEST.json'):continue
 p=P/n; m=json.loads(p.read_text());base=p.parent if 'qr-scaling-handoff' in n else P
 for k,v in m['files'].items():
  q=(base/k).resolve();assert q.is_relative_to(P.resolve()) and sha(q)==v['sha256'],(n,k)
  assert q.stat().st_size==v['bytes'];files.add(str(q.relative_to(P.resolve())))
 manifests.append({'path':n,'sha256':sha(p),'entries':len(m['files']),'base':str(base.relative_to(P))})
for directory in ['verification/exactcertificates-development','verification/integerqr-development','verification/certdiagnostic-development']:
 files|={str(q.relative_to(P)) for q in (P/directory).rglob('*') if q.is_file()}
files|={'NLA/IE05/'+n+'.lean' for n in ['Definitions','Scaling','QR','IntegerQR','ExactCertificates']}
files|={'Challenge.lean','lean-toolchain','lake-manifest.json','lakefile.toml','comparator.json'}
assert not any('Witness' in n or 'witness-development' in n for n in files)
write('INPUTS.json',{'scope':'Frozen733 plus exact stable helper sources/prior handoffs/root attempts; concurrent Witness is outside scope',
 'pins':pins,'prior_manifests':manifests,'file_count':len(files),
 'files':{n:{'sha256':sha(P/n),'bytes':(P/n).stat().st_size} for n in sorted(files)}})
names=['integer_factor_certificates','integer_entry_certificates','numerical_gap_positive']
challenge=(P/'Challenge.lean').read_text(); actual=(P/'NLA/IE05/ExactCertificates.lean').read_text()
defs=[]; headers={}
for n in names:
 pattern=r'theorem '+re.escape(n)+r'\s*:\s*([\s\S]*?)\s*:= by'
 c=re.search(pattern,challenge).group(1);a=re.search(pattern,actual).group(1)
 assert ''.join(c.split())==''.join(a.split()),n
 defs.append('def '+n+' : Prop :=\n'+c+'\n')
 headers[n]={'Challenge_header':c,'actual_header':a,'equal_modulo_whitespace':True}
write('expected-type-extraction.json',{'Challenge_sha256':sha(P/'Challenge.lean'),'ExactCertificates_sha256':sha(P/'NLA/IE05/ExactCertificates.lean'),'headers':headers})
prefix='''/- Admission-free helper inspection. No Challenge/reference module is imported.
Completion inspection only; no whole-proof independent approval or Linux run. -/
import NLA.IE05.IntegerQR
import NLA.IE05.ExactCertificates
import Lean.Util.FoldConsts
set_option maxHeartbeats 4000000
set_option leancert.trust "kernel"
noncomputable section
namespace NLA.IE05.CertificatesQRExpected
'''
generic='''def normalizedQRQ_of_gram_lu : Prop :=
  ∀ {n : ℕ} (L H T : Mat n) (d : Fin n → ℝ),
    (∀ j, 0 < d j) → H.transpose * H = Matrix.diagonal d →
    H = L * T → UpperTriangular T → (∀ i, 0 < T i i) →
    normalizedQRQ L = scaledColumns H d
end NLA.IE05.CertificatesQRExpected
'''
body=(E/'inspector-body.txt').read_text()
p=E/'Inspect.lean';assert not p.exists();p.write_text(prefix+'\n'.join(defs)+generic+body)
write('navigation-diagnostics.json',{'missing_file_read':{
 'command':'cat NLA/IE05/Scaling.lean NLA/IE05/QR.lean verification/qr-scaling-handoff/Inspect.lean',
 'exit_code':1,'stdout':'The two actual mathematical modules were printed fully; their exact bytes are bound in INPUTS.json.',
 'stderr':'cat: verification/qr-scaling-handoff/Inspect.lean: No such file or directory',
 'interpretation':'Navigation-only missing historical inspector path; no source/compiler failure. The present fresh admission-free inspector is new.'}})
print(json.dumps({'prepared':True,'stable_bound_files':len(files),'frozen_inputs':733,'expected_contracts':3,'generic_type':1}))
