#!/usr/bin/env python3
"""Regression and deliberate-corruption tests for the exact verifiers."""
from pathlib import Path
import contextlib,copy,io,json,tempfile
from verify_certificate import verify,require
from verify_witness_and_rigidity import verify as verify_witness

def main():
    source=Path(__file__).with_name('krause_certificate.json')
    with contextlib.redirect_stdout(io.StringIO()):
        verify(source);verify_witness(source)
    original=json.loads(source.read_text());tests=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name in ['trace','positivity','identity']:
            c=copy.deepcopy(original)
            if name=='trace':c['q_real'][0]+=1
            elif name=='positivity':
                n=c['blocks'][0]['size']
                c['blocks'][0]['preconditioner_real']=[[0]*n for _ in range(n)]
                c['blocks'][0]['preconditioner_s']=[[0]*n for _ in range(n)]
            else:
                c['blocks'][0]['matrix_real'][0][0]=str(int(c['blocks'][0]['matrix_real'][0][0])+1)
            p=Path(tmp)/(name+'.json');p.write_text(json.dumps(c))
            rejected=False
            try:
                with contextlib.redirect_stdout(io.StringIO()):verify(p)
            except ValueError:rejected=True
            require(rejected,f'Corruption test {name} was not rejected.')
            tests.append({'corruption':name,'rejected':True})
    print(json.dumps({'valid_certificate':'PASS','valid_witness_and_rigidity':'PASS','corruption_tests':tests},indent=2))
if __name__=='__main__':main()
