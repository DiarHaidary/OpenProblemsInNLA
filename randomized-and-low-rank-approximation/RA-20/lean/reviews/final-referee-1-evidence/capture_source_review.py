#!/usr/bin/env python3
"""Retain exact primary library/rubric source used in the semantic review, not cache objects."""
from pathlib import Path
import datetime,hashlib,json,subprocess
E=Path(__file__).resolve().parent
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
S=Path('/tmp/nla-lean-formalization/standards/sources/TauCetiProject/TauCetiReview')
L=Path('/tmp/nla-lean-formalization/leancert-examples/Schiffer')
files=[(C/'mathlib',x,'mathlib') for x in ['Mathlib/RingTheory/Smooth/Locus.lean','Mathlib/RingTheory/Smooth/Basic.lean',
  'Mathlib/RingTheory/Nullstellensatz.lean','Mathlib/Algebra/MvPolynomial/PDeriv.lean',
  'Mathlib/Algebra/MvPolynomial/Funext.lean','Mathlib/Analysis/Calculus/FDeriv/Defs.lean',
  'Mathlib/SetTheory/Cardinal/Basic.lean','Mathlib/LinearAlgebra/Matrix/Rank.lean']]
files += [(C/'leancert','LeanCert/Tactic/Verification.lean','leancert')]
files += [(S,'rubrics/'+n+'.md','tau-ceti') for n in ['correctness','scope','proof-quality','reuse','api-design','attribution','naming','placement','documentation','generality']]
files += [(L,'Schiffer/Challenge.lean','schiffer')]
inventory=[]
for base,n,label in files:
    f=base/n;b=f.read_bytes();dest=E/'inspected-source'/label/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
    rec={'origin':str(f),'snapshot':str(dest.relative_to(E)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
    if label in ['mathlib','leancert']:
        blob=subprocess.check_output(['git','show','HEAD:'+n],cwd=base)
        assert b==blob
        rec['pinned_HEAD']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=base).decode().strip()
    inventory.append(rec)
queries=[
 ['rg','-n','smoothLocus.*[Ee]quiv|[Ee]quiv.*smoothLocus|FormallySmooth.*retract|formallySmooth.*retract|[Ff]ormallySmooth.*split','Mathlib/RingTheory/Smooth'],
 ['rg','-n','hessian|sum_squares|square.*[Ff][Dd]eriv|[Ff][Dd]eriv.*square','Mathlib/Analysis/Calculus','Mathlib/Analysis/SpecialFunctions'],
 ['rg','-n','eval.*pderiv|pderiv.*eval|pderiv.*aeval|eval.*derivation|derivation.*eval','Mathlib/Algebra/MvPolynomial']]
search=[]
for i,cmd in enumerate(queries,1):
    r=subprocess.run(cmd,cwd=C/'mathlib',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (E/('reuse-search-%d.log'%i)).write_bytes(r.stdout)
    assert r.returncode in [0,1]
    search.append({'command':cmd,'cwd':str(C/'mathlib'),'exit_code':r.returncode,'log':'reuse-search-%d.log'%i,
                   'meaning_of_exit_1':'No textual match, not a failed proof check'})
(E/'source-review.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'files':inventory,'targeted_reuse_searches':search,'scope':'Read actual definitions and relevant proof passages. No complete third-party library proof review or example-project verification claimed.'},indent=2)+'\n')
(E/'primary-paper-check.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'url':'https://arxiv.org/pdf/2010.15636v2','method':'Successful direct web-tool PDF open and theorem/table find; no downloaded PDF hash asserted',
    'locations':['Section 2.2, printed p.4','Section 2.3, printed p.5','Conjecture 5.6 and Table 7, printed p.21'],
    'observations':'The source counts complex smooth critical points generically, uses the bilinear extension and full-entry Frobenius distance, and prints four for n=s=3. Canonical original target is retained.',
    'scope':'Target/convention check only; no later-literature search or full-paper verification.'},indent=2)+'\n')
(E/'example-fetch-diagnostics.json').write_text(json.dumps({'method':'web-tool direct raw GitHub fetch','results':[
    {'url':'https://raw.githubusercontent.com/sgstepaniants/Forsythe/8d1b0c0545a77b40245e84705aa7d273e6c81e62/lean-proof/'+n,
     'result':'Cache miss; contents not retrieved; no read claimed'} for n in ['Challenge.lean','Solution.lean']],
    'available_example_inspected':'Retained local Schiffer/Schiffer/Challenge.lean plus pinned NLA source-lock and verification protocol. No example theorem is a mathematical dependency.'},indent=2)+'\n')
print('PRIMARY_SOURCE_AND_REUSE_RECORDS_WRITTEN',len(inventory))
