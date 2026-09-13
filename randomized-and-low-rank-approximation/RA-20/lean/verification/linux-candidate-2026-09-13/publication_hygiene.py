#!/usr/bin/env python3
"""Author checks of candidate links and publication material; no HTTP claims."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import urllib.parse
import yaml

E = Path(__file__).resolve().parent
P = E.parents[1]
R = P.parents[2]
SELF_LATE = {E / 'EVIDENCE-MANIFEST.json', E / 'HYGIENE.json', E / 'VALIDATION.json'}

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def local_link(base, value):
    parsed = urllib.parse.urlparse(value)
    assert not parsed.scheme and not parsed.netloc, value
    target = (base / urllib.parse.unquote(parsed.path)).resolve()
    if target in SELF_LATE and not target.exists():
        return {'link': value, 'target': str(target.relative_to(R)),
                'status': 'scheduled-seal-output; final verifier requires existence'}
    assert target.is_file(), ('missing relative link', value)
    return {'link': value, 'target': str(target.relative_to(R)),
            'status': 'exists', 'sha256': digest(target)}

relative = []
external = set()
for document in [P / 'README.md', E / 'HANDOFF.md']:
    body = document.read_text()
    for match in re.finditer(r'\[[^\]]+\]\(([^\s)]+)\)', body):
        link = match.group(1)
        parsed = urllib.parse.urlparse(link)
        if parsed.scheme:
            assert parsed.scheme == 'https' and parsed.netloc, link
            external.add(link)
        else:
            item = local_link(document.parent, link)
            item['document'] = str(document.relative_to(P))
            relative.append(item)
    assert all(line == line.rstrip() for line in body.splitlines()), document

metadata = yaml.safe_load((P / 'formalization.yaml').read_text())
paths = []
keys = {'file', 'comparator_config', 'dependency_manifest', 'frozen_readme_archive',
        'installation_evidence', 'adaptation', 'local_schema', 'prerequisites_document'}

def walk(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in keys:
                paths.append(local_link(P, item))
            if key.endswith('EVIDENCE-MANIFEST.json'):
                paths.append(local_link(P, key))
            walk(item)
    elif isinstance(value, list):
        for item in value:
            walk(item)
    elif isinstance(value, str) and value.startswith('https://'):
        parsed = urllib.parse.urlparse(value)
        assert parsed.netloc and not parsed.username and not parsed.password, value
        external.add(value)

walk(metadata)
assert all(line == line.rstrip() for line in (P / 'formalization.yaml').read_text().splitlines())
env = os.environ.copy()
env['GIT_OPTIONAL_LOCKS'] = '0'
immutable = []
for link in sorted(external):
    parsed = urllib.parse.urlparse(link)
    parts = parsed.path.strip('/').split('/')
    if parsed.netloc == 'github.com' and parts[:3] == ['ajt60gaibb', 'OpenProblemsInNLA', 'blob']:
        assert parts[3] == '5830ed4fb06da0659414a3deb2a40ad327aca052', link
        rel = '/'.join(parts[4:])
        raw = subprocess.check_output(['git', 'show', parts[3] + ':' + rel], cwd=R, env=env)
        assert raw == (R / rel).read_bytes(), rel
        immutable.append({'url': link, 'sha256': hashlib.sha256(raw).hexdigest(), 'matches_base_and_live': True})

email = re.compile(rb'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
new_material = [P / 'README.md', P / 'formalization.yaml', P / 'verification/pre-candidate-README.md']
new_material += [p for p in sorted(E.rglob('*')) if p.is_file()]
violations = [str(p.relative_to(P)) for p in new_material if email.search(p.read_bytes())]
assert not violations, ('personal-email-like text in files', violations)
out = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'AUTHOR_PUBLICATION_HYGIENE_PASS',
    'relative_links': relative,
    'metadata_file_paths': paths,
    'immutable_original_source_links': immutable,
    'external_urls_syntax_only': sorted(external),
    'external_live_HTTP_probe': 'not performed or claimed by this installation',
    'email_like_matches': 0,
    'new_material_files_scanned': len(new_material),
    'README_YAML_HANDOFF_trailing_whitespace': 0,
    'later_seal_outputs': [str(p.relative_to(P)) for p in sorted(SELF_LATE)],
    'independent_packaging_review': 'pending',
}
(E / 'HYGIENE.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'status': out['status'], 'relative_links': len(relative),
                  'metadata_paths': len(paths), 'immutable_source_links': len(immutable),
                  'email_like_matches': 0}))
