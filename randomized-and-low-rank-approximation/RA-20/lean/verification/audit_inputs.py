"""Record immutable original Git sources and actual pinned primary library inputs."""
from pathlib import Path
import datetime, hashlib, json, subprocess

P = Path(__file__).resolve().parents[1]
W = Path('/tmp/nla-lean-ra09-worktree')
BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
C = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
S = P / 'verification' / 'original-sources'
sources = [
    'randomized-and-low-rank-approximation/RA-20/README.md',
    'randomized-and-low-rank-approximation/RA-20/solution.md',
    'randomized-and-low-rank-approximation/RA-20/solution.tex',
    'references/research-expansion-2026-09-11/ra20-resolution/README.md',
    'references/research-expansion-2026-09-11/ra20-resolution/independent-review.md',
    'references/research-expansion-2026-09-11/ra20-resolution/verify_counterexample.py',
    'references/research-expansion-2026-09-11/ra20-resolution/exact-results.json',
    'AGENTS.md', 'CONTRIBUTING.md', 'problem_ids.json',
    'docs/lean/README.md', 'docs/lean/REVIEW.md',
    'docs/lean/schema/README.md', 'docs/lean/schema/v0.4.schema.json',
    'tools/lean/HARNESS.md', 'tools/lean/source-lock.json',
]
sha = lambda b: hashlib.sha256(b).hexdigest()
blob = lambda b: hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
record = {'base': BASE, 'source_repository': 'https://github.com/ajt60gaibb/OpenProblemsInNLA',
          'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'files': {}}
for name in sources:
    raw = subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=W)
    actual = subprocess.check_output(['git', 'rev-parse', BASE + ':' + name], cwd=W).decode().strip()
    assert blob(raw) == actual
    path = S / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    record['files'][name] = {'sha256': sha(raw), 'git_blob': actual, 'bytes': len(raw),
                             'snapshot': str(path.relative_to(P))}
(P / 'verification' / 'original-source-inventory.json').write_text(json.dumps(record, indent=2) + '\n')
libraries = {
    'mathlib': ['Mathlib/RingTheory/Nullstellensatz.lean',
                'Mathlib/RingTheory/Smooth/Locus.lean',
                'Mathlib/RingTheory/Smooth/StandardSmoothOfFree.lean',
                'Mathlib/RingTheory/Smooth/StandardSmooth.lean',
                'Mathlib/RingTheory/RegularLocalRing/Defs.lean',
                'Mathlib/LinearAlgebra/Matrix/Rank.lean',
                'Mathlib/Algebra/MvPolynomial/PDeriv.lean',
                'Mathlib/Analysis/Calculus/FDeriv/Basic.lean',
                'Mathlib/Analysis/Matrix/Normed.lean'],
    'leancert': ['LeanCert/Tactic/Verification.lean'],
}
pins = {d['name']: d['rev'] for d in json.loads((P / 'lake-manifest.json').read_text())['packages']}
lib_record = {'scope': 'Actual primary library sources inspected; ten clean dependency heads also checked by the elaboration runner',
              'files': {}}
for package, names in libraries.items():
    for name in names:
        dep = C / package
        raw = (dep / name).read_bytes()
        assert subprocess.check_output(['git', 'show', pins[package] + ':' + name], cwd=dep) == raw
        git_blob = subprocess.check_output(['git', 'rev-parse', pins[package] + ':' + name], cwd=dep).decode().strip()
        assert git_blob == blob(raw)
        lib_record['files'][package + '/' + name] = {'package_rev': pins[package], 'sha256': sha(raw),
                                                   'git_blob': git_blob, 'bytes': len(raw)}
(P / 'verification' / 'primary-library-inventory.json').write_text(json.dumps(lib_record, indent=2) + '\n')
registry = json.loads(subprocess.check_output(['git', 'show', BASE + ':problem_ids.json'], cwd=W))
assert registry['RA-20'] == 'randomized-and-low-rank-approximation/RA-20/README.md'
assert len(registry) == 217
assert '**Status:** Solved' in (S / registry['RA-20']).read_text()
existing = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE,
                                   'randomized-and-low-rank-approximation/RA-20/lean'], cwd=W)
assert not existing
(P / 'verification' / 'eligibility.json').write_text(json.dumps({
    'base': BASE, 'problem_id': 'RA-20', 'canonical_path': registry['RA-20'],
    'base_status': 'Solved', 'canonical_lean_subtree_present': False,
    'permanent_registry_entries': len(registry), 'registry_unchanged': True,
    'campaign_initial_snapshot_sha256': '3b4f8b6bfe921c6638ef6f092dda70a721c938f476b8770af5761f8d9cd615fc',
    'campaign_initial_target_record': 'absent; root subsequently asked to reserve this draft',
    'scope': 'Immutable base and campaign duplicate check; not a new comprehensive branch/fork search',
    'git_or_canonical_mutation': False,
}, indent=2) + '\n')
print(json.dumps({'original_Git_sources': len(record['files']), 'primary_library_sources': len(lib_record['files']),
                  'registry_entries': len(registry), 'status': 'PASS'}))
