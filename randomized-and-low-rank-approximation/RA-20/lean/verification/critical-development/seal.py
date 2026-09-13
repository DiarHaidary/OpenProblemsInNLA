"""Seal the completed Critical helper and all its own raw author evidence.

Uses the same exact-path self-exclusion as the sealed Smooth helper. This is
packaging of author checks, not independent mathematical or Linux validation.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os

E = Path(__file__).resolve().parent
P = E.parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def row(path):
    return {"sha256": sha(path), "bytes": Path(path).stat().st_size}


start = json.loads((E / "START.json").read_text())
for name, digest in start["frozen_files"].items():
    assert sha(P / name) == digest, name
for name, digest in start["imports"].items():
    assert sha(P / name) == digest, name
tangent = json.loads((E / "TANGENT-IMPORT.json").read_text())
assert sha(P / tangent["source"]) == tangent["source_sha256"]
final = json.loads((E / "FINAL.json").read_text())
result_path = Path(final["attempt"]) / "result.json"
assert sha(result_path) == final["result_sha256"]
result = json.loads(result_path.read_text())
assert final["verdict"] == result["verdict"] == "PASS"
assert len(result["commands"]) == 9
assert result["explicit_kernel_assertions"] == 30
assert result["standard_three_reports"] == 26
assert result["actual_project_declarations"] == 174
assert len(result["required_material_dependencies"]) == 39
source = P / "NLA/RA20/Critical.lean"
assert sha(source) == "e8b2e3646d4b1f5e41e35ae4e23ba55d758cb6e48d125643d02eb1d51cab2040"
assert not Path(start["prefix"]).exists()
assert not Path(result["prefix"]).exists()

imports = [
    "smooth-development", "algebra-development", "differential-development",
    "tangent-development", "smooth-transport-development",
]
for name in imports:
    outer = P / "verification" / name / "EVIDENCE-MANIFEST.json"
    for relative, identity in json.loads(outer.read_text())["files"].items():
        assert row((outer.parent / relative).resolve()) == identity, relative

handoff = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "verdict": "AUTHOR_VALIDATION_PASS",
    "role": "implementation author, not independent final referee or Linux verifier",
    "source": str(source.relative_to(P)),
    "source_identity": row(source),
    "export": "NLA.RA20.generic_critical_locus_proved",
    "exact_frozen_contract": 7,
    "handoff_sha256": sha(E / "HANDOFF.md"),
    "fresh_result": str(result_path.relative_to(E)),
    "fresh_result_sha256": sha(result_path),
    "commands_passed": len(result["commands"]),
    "explicit_kernel_assertions": result["explicit_kernel_assertions"],
    "standard_three_reports": result["standard_three_reports"],
    "actual_project_declarations": result["actual_project_declarations"],
    "required_material_dependencies": len(result["required_material_dependencies"]),
    "frozen_statement_files_unchanged": len(start["frozen_files"]),
    "original_Git_source_files_unchanged": len(start["source_files"]),
    "imported_sources_unchanged": 6,
    "imported_manifests_fully_rechecked": 5,
    "clean_read_only_dependency_pins": len(result["pins"]),
    "only_owned_generated_prefixes_removed": True,
    "independent_final_reviews_and_actual_Ubuntu_pending": True,
}
(E / "HANDOFF.json").write_text(json.dumps(handoff, indent=2) + "\n")

outer = E / "EVIDENCE-MANIFEST.json"
files = {q.resolve() for q in E.rglob("*") if q.is_file() and q.resolve() != outer.resolve()}
files.update((P / name).resolve() for name in start["imports"])
files.update([
    source.resolve(), (P / tangent["source"]).resolve(),
    (P / "Challenge.lean").resolve(),
    (P / "reviews/statement-freeze.json").resolve(),
    (P / "verification/proof-start.json").resolve(),
    (P / "verification/implementation-roles.json").resolve(),
])
for name in imports:
    files.add((P / "verification" / name / "EVIDENCE-MANIFEST.json").resolve())
manifest = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "format": "sha256-size-manifest-v1",
    "root": ".",
    "excludes_only": "EVIDENCE-MANIFEST.json",
    "scope": "All Critical author raw attempts, final checks and handoff; actual source, sealed imports, original frozen boundary and gate. Nested manifests are included.",
    "files": {os.path.relpath(q, E): row(q) for q in sorted(files)},
}
outer.write_text(json.dumps(manifest, indent=2) + "\n")
for relative, identity in manifest["files"].items():
    assert row((E / relative).resolve()) == identity
print(json.dumps({
    "source_sha256": sha(source),
    "handoff_md_sha256": sha(E / "HANDOFF.md"),
    "handoff_json_sha256": sha(E / "HANDOFF.json"),
    "outer_sha256": sha(outer),
    "bound_files": len(manifest["files"]),
    "all_evidence_identity_checks": "PASS",
}, indent=2))
