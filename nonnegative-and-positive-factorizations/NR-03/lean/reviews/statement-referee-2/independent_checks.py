"""Statement-referee audit, not a Lean mathematical proof certificate.

Run with the campaign Python that supplies PyYAML and jsonschema.  The script
does not import the submission's certificate generator or verifier.  It reads
the immutable source snapshots stored beside it, checks every scaled entry,
and compares the four stated atom families to the retained certificate.
"""
from pathlib import Path
import hashlib
import itertools
import json
import re

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent
candidate = ROOT / "candidate"
source = ROOT / "source"
cert_path = source / "references/holden-nr03-2026-09-13/data/factors_n7.json"
cert = json.loads(cert_path.read_text())
assert hashlib.sha256(cert_path.read_bytes()).hexdigest() == (
    "fa515775f9c77e5dfe85109125d3f730c4b36684894730096247cd67fcc60bb9"
)
assert cert["n"] == 7 and cert["r"] == 127
W, V, d = cert["W"], cert["H_scaled"], cert["denominators"]
assert len(W) == 128 and all(len(row) == 127 for row in W)
assert len(V) == 127 and all(len(row) == 128 for row in V)
assert len(d) == 128 and all(type(v) is int and v > 0 for v in d)
assert all(type(v) is int and v >= 0 for row in W + V for v in row)

# A direct mask/Boolean correspondence check, independent of all data labels.
vectors = list(itertools.product((False, True), repeat=7))
to_mask = lambda a: sum((1 << i) for i in range(7) if a[i])
assert len(vectors) == len({to_mask(a) for a in vectors}) == 128
assert {to_mask(a) for a in vectors} == set(range(128))
for a, b in itertools.product(vectors, repeat=2):
    dot = sum(int(x) * int(y) for x, y in zip(a, b))
    assert dot == (to_mask(a) & to_mask(b)).bit_count()

zeros = 0
for a in range(128):
    for b in range(128):
        target = (1 - (a & b).bit_count()) ** 2
        actual = sum(W[a][k] * V[k][b] for k in range(127))
        assert actual == d[b] * target, (a, b, actual, target)
        zeros += target == 0

# Compare every W and V entry to the four formula families, independently of
# the certificate's atom labels and source scripts.
subsets = lambda k: [sum(1 << i for i in t) for t in itertools.combinations(range(7), k)]
atoms = [("core", s) for s in range(64)]
atoms += [("single", 1 << i) for i in range(7)]
atoms += [("pair", s) for s in subsets(2)]
atoms += [("four", s) for s in subsets(4)]
assert len(atoms) == 127
for k, (family, s) in enumerate(atoms):
    for a in range(128):
        w = {
            "core": int(a == s or a == (s ^ 127)),
            "single": int(a & s == 0),
            "pair": int(a & s == s),
            "four": max((a & s).bit_count() - 2, 0),
        }[family]
        assert W[a][k] == w, ("W", a, k)
    for b in range(128):
        p = b.bit_count()
        v = {
            "core": (1 - (s & b).bit_count()) ** 2 * (1 - ((s ^ 127) & b).bit_count()) ** 2,
            "single": int(b == s),
            "pair": 4 * (p - 2) * int(s & b == s),
            "four": 12 * int(s & b == s),
        }[family]
        assert V[k][b] == v, ("V", k, b)
for b in range(128):
    assert d[b] == max(1, (b.bit_count() - 1) ** 2)

metadata = yaml.safe_load((candidate / "formalization.yaml").read_text())
schema = json.loads((source / "docs/lean/schema/v0.4.schema.json").read_text())
schema_errors = [
    {"path": list(error.absolute_path), "message": error.message}
    for error in jsonschema.Draft202012Validator(schema).iter_errors(metadata)
]
comparator = json.loads((candidate / "comparator.json").read_text())
challenge = (candidate / "Challenge.lean").read_text()
definition_text = (candidate / "NLA/NR03/Definitions.lean").read_text()
names = ["NLA.NR03." + n for n in re.findall(r"^theorem\s+(\w+)", challenge, re.M)]
assert names == comparator["theorem_names"]
assert names == [r["declaration"] for r in metadata["status"]["main_results"]]
assert len(names) == len(set(names)) == 10
assert len(re.findall(r"^\s+sorry\s*$", challenge, re.M)) == 10
assert not re.search(r"\bsorry\b|^axiom\b|^opaque\b", definition_text, re.M)
assert metadata["status"]["sorry_count"] == 10
assert metadata["status"]["sorry_in_definitions"] == 0
assert metadata["status"]["whole_problem_verified"] is False
assert "sorryAx" in metadata["status"]["axioms"]
assert all(r["sorry_count"] == 1 and r["file"] == "Challenge.lean" for r in metadata["status"]["main_results"])
assert comparator["definition_names"] == []
assert comparator["permitted_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
manifest = json.loads((candidate / "lake-manifest.json").read_text())
assert len(manifest["packages"]) == 10
pins = {p["name"]: p["rev"] for p in manifest["packages"]}
assert pins == metadata["toolchain"]["dependencies"]
source_map = (candidate / "SOURCE_MAP.md").read_text()
for path, blob, sha in re.findall(r"\|[^|]+\| `([^`]+)` \| `([0-9a-f]+)` \| `([0-9a-f]+)` \|", source_map):
    raw = (source / path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == sha
    assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == blob

results = {
    "phase": "independent statement review, not mathematical verification",
    "result": "CHANGES REQUESTED: metadata schema" if schema_errors else "PASS",
    "source_commit": "50838e37dd793830e2cecd1055cfc7e0349490f1",
    "certificate_dimensions": [128, 127, 128],
    "entries_checked_exactly": 16384,
    "zero_target_entries": zeros,
    "positive_target_entries": 16384 - zeros,
    "boolean_mask_bijection_checked": 128,
    "boolean_dot_vs_mask_intersection_pairs_checked": 16384,
    "atom_family_formula_entries_checked": 2 * 128 * 127,
    "denominators": sorted(set(d)),
    "W_nonzeros": sum(v != 0 for row in W for v in row),
    "W_max": max(v for row in W for v in row),
    "V_max": max(v for row in V for v in row),
    "metadata_schema": "FAIL v0.4" if schema_errors else "PASS v0.4",
    "metadata_schema_errors": schema_errors,
    "declaration_coverage": names,
    "source_map_hashes_and_git_blob_ids": "PASS",
    "toolchain_dependency_pins": pins,
    "limitations": [
        "Python checks are not a Lean proof or trusted oracle.",
        "Challenge contains ten intentional placeholders.",
        "No Linux Comparator or full proof audit was performed.",
        "Pre-existing dependency objects were reused, not rebuilt or independently authenticated by a kernel replay."
    ]
}
(ROOT / "independent_checks.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
