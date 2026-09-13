"""Verify the delivered SHA-256 manifest using only the standard library."""
from pathlib import Path
import hashlib,json,sys

def check(root: Path):
    root=root.resolve(); lines=(root/'SHA256SUMS').read_text().splitlines();count=0
    for line in lines:
        if not line.strip():continue
        digest,name=line.split('  ',1);path=(root/name).resolve()
        if root not in path.parents:raise ValueError('Manifest path escapes archive root')
        if not path.is_file():raise FileNotFoundError(path)
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=digest:raise ValueError('Hash mismatch: '+name)
        count+=1
    return {'passed':True,'files_checked':count}
if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
    print(json.dumps(check(root),indent=2))
