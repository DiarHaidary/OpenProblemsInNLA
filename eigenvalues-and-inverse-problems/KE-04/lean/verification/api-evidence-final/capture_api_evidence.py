#!/usr/bin/env python3
"""Capture selected text evidence, never package caches or build artifacts."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import traceback

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "verification/api-evidence-final"
PKG = Path("/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages")
SPECS = {
    "mathlib": (PKG / "mathlib", "0df444a360eaa60ab8c11dca51a86af692955474", [
        "Mathlib/Analysis/Matrix/Spectrum.lean", "Mathlib/Analysis/InnerProductSpace/Spectrum.lean",
        "Mathlib/Analysis/InnerProductSpace/PiL2.lean", "Mathlib/Analysis/InnerProductSpace/Positive.lean",
        "Mathlib/LinearAlgebra/Matrix/Hermitian.lean", "Mathlib/LinearAlgebra/Matrix/PosDef.lean",
        "Mathlib/Analysis/Matrix/Order.lean", "Mathlib/Analysis/Matrix/PosDef.lean",
        "Mathlib/LinearAlgebra/Dimension/Constructions.lean",
        "Mathlib/LinearAlgebra/FiniteDimensional/Lemmas.lean",
        "Mathlib/LinearAlgebra/Finsupp/LinearCombination.lean",
        "Mathlib/LinearAlgebra/LinearIndependent/Defs.lean", "Mathlib/Data/Fin/Rev.lean"]),
    "leancert": (PKG / "leancert", "621a43d7cf21f87872392a01e874f2f1dbddc926", [
        "LeanCert/Tactic/Verification.lean"]),
    "forsythe": (Path("/Users/georgestepaniants/Research/Forsythe"),
        "8d1b0c0545a77b40245e84705aa7d273e6c81e62", [
            "lean-proof/Challenge.lean", "lean-proof/ProofProject/CheckedMultivariateBound.lean",
            "lean-proof/NUMERICAL_TARGETS.md", "lean-proof/comparator.json", "lean-proof/LICENSE"]),
    "schiffer": (Path("/tmp/nla-lean-formalization/leancert-examples/Schiffer"),
        "2938e277969c329caf154e48a3d8823f3635c7f1", ["Schiffer/Challenge.lean"]),
    "tauceti": (Path("/tmp/nla-lean-formalization/standards/sources/TauCetiProject/TauCetiReview"),
        "afb424eda89e8ac96d9eb69f6a88972055a4cd1b", [
            "README.md", "rubrics/README.md", "rubrics/_common.md", "rubrics/scope.md", "rubrics/correctness.md",
            "rubrics/reuse.md", "rubrics/attribution.md", "rubrics/api-design.md",
            "rubrics/generality.md", "rubrics/placement.md", "rubrics/naming.md",
            "rubrics/documentation.md", "rubrics/proof-quality.md"]),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(argv, cwd):
    cp = subprocess.run(argv, cwd=cwd, env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    return cp, {"argv": argv, "cwd": str(cwd), "exit_code": cp.returncode,
                "stdout_sha256": sha(cp.stdout), "stdout_bytes": len(cp.stdout),
                "stderr": cp.stderr.decode(errors="replace")}


def main():
    assert not OUT.exists(), "Do not overwrite a captured evidence set"
    OUT.mkdir()
    (OUT / "capture_api_evidence.py").write_bytes(Path(__file__).read_bytes())
    record = {"phase": "statement API/reuse inspection", "files": {}, "searches": [],
              "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "scope": "Selected text snapshots and actual read-only searches; no package/build copy."}
    try:
        standards = Path("/tmp/nla-lean-formalization/standards")
        archives = ["MANIFEST.json", "TauCetiProject_TauCetiReview-tree.json", "TauCetiProject_TauCetiReview-commit.json"]
        record["tauceti_archive_bindings"] = {}
        for filename in archives:
            target = OUT / "tauceti-archive" / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((standards / filename).read_bytes())
            record["tauceti_archive_bindings"][str(target.relative_to(ROOT))] = {
                "source": str(standards / filename), "sha256": sha(target.read_bytes()), "bytes": target.stat().st_size}
        tree = json.loads((standards / archives[1]).read_text())
        commit_record = json.loads((standards / archives[2]).read_text())
        archive_manifest = json.loads((standards / "MANIFEST.json").read_text())
        assert tree["sha"] == SPECS["tauceti"][1] and not tree["truncated"]
        assert commit_record["sha"] == SPECS["tauceti"][1]
        entries = {x["path"]: x for x in tree["tree"]}
        tree_hashes = {}
        for directory in [""] + [x["path"] for x in tree["tree"] if x["type"] == "tree"]:
            children = [x for x in tree["tree"] if str(Path(x["path"]).parent).replace(".", "", 1) == directory]
            children.sort(key=lambda x: (Path(x["path"]).name + ("/" if x["type"] == "tree" else "")).encode())
            body = b"".join((x["mode"].lstrip("0") + " " + Path(x["path"]).name).encode() + b"\0" + bytes.fromhex(x["sha"]) for x in children)
            digest = hashlib.sha1(b"tree " + str(len(body)).encode() + b"\0" + body).hexdigest()
            expected = commit_record["commit"]["tree"]["sha"] if directory == "" else entries[directory]["sha"]
            assert digest == expected, (directory, digest, expected)
            tree_hashes[directory] = digest
        record["tauceti_reconstructed_git_trees"] = tree_hashes
        for name, (repo, commit, files) in SPECS.items():
            for relative in files:
                if name == "tauceti":
                    content = (repo / relative).read_bytes()
                    blob_id = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
                    assert blob_id == entries[relative]["sha"]
                    assert sha(content) == archive_manifest["sources/TauCetiProject/TauCetiReview/" + relative]["sha256"]
                    command = {"operation": "read pinned source archive and independently hash Git blob",
                               "source": str(repo / relative), "git_tree_binding_checked": True}
                else:
                    cp, command = run(["git", "show", commit + ":" + relative], repo)
                    assert cp.returncode == 0, command
                    content = cp.stdout
                    blob, blob_command = run(["git", "rev-parse", commit + ":" + relative], repo)
                    assert blob.returncode == 0, blob_command
                    blob_id = blob.stdout.decode().strip()
                target = OUT / name / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                target.chmod(0o444)
                record["files"][str(target.relative_to(ROOT))] = {
                    "repo": str(repo), "commit": commit, "upstream_path": relative,
                    "git_blob": blob_id, "sha256": sha(content),
                    "bytes": len(content), "capture_command": command,
                    "working_source_equal": (repo / relative).read_bytes() == content}
        searches = [
            ("spectral", "mathlib", ["rg", "-n",
             "eigenvalues_antitone|roots_charpoly_eq_eigenvalues|eigenvalues_eq_eigenvalues_iff|apply_eigenvectorBasis|isSymmetric_toEuclideanLin_iff",
             "Mathlib/Analysis/Matrix/Spectrum.lean", "Mathlib/Analysis/InnerProductSpace/Spectrum.lean"]),
            ("subspace", "mathlib", ["rg", "-n",
             "finrank_span_eq_card|finrank_sup_add_finrank_inf_eq|linearIndependent_iff_injective_fintypeLinearCombination|range_linearCombination|exists_orthonormalBasis|stdOrthonormalBasis",
             "Mathlib/LinearAlgebra/Dimension/Constructions.lean", "Mathlib/LinearAlgebra/FiniteDimensional/Lemmas.lean",
             "Mathlib/LinearAlgebra/LinearIndependent/Defs.lean", "Mathlib/LinearAlgebra/Finsupp/LinearCombination.lean",
             "Mathlib/Analysis/InnerProductSpace/PiL2.lean"]),
            ("positive", "mathlib", ["rg", "-n",
             "dotProduct_mulVec_zero_iff|posSemidef_iff_eigenvalues_nonneg|isPositive_toEuclideanLin_iff|isHermitian_conjTranspose_mul_mul|conjTranspose_mul_mul_same|mul_mul_conjTranspose_same",
             "Mathlib/Analysis/Matrix/Order.lean", "Mathlib/Analysis/Matrix/PosDef.lean",
             "Mathlib/Analysis/InnerProductSpace/Positive.lean", "Mathlib/LinearAlgebra/Matrix/Hermitian.lean",
             "Mathlib/LinearAlgebra/Matrix/PosDef.lean"]),
            ("krylov_reuse", "mathlib", ["rg", "-n", "Krylov|Lanczos|krylov|lanczos", "Mathlib"]),
            ("trust", "leancert", ["rg", "-n", "assert_trust|collectAxioms|foundational|nativeCompiler|sorryAx|mode : VerificationMode", "LeanCert/Tactic/Verification.lean"]),
        ]
        for label, name, argv in searches:
            cp, command = run(argv, SPECS[name][0])
            log = OUT / (label + ".log")
            log.write_bytes(cp.stdout + cp.stderr)
            command.update(log=str(log.relative_to(ROOT)), log_sha256=sha(log.read_bytes()))
            record["searches"].append(command)
            assert cp.returncode in (0, 1), command
        record["all_working_sources_equal_pins"] = all(x["working_source_equal"] for x in record["files"].values())
        assert record["all_working_sources_equal_pins"]
        record["success"] = True
    except Exception:
        record["success"] = False
        record["error"] = traceback.format_exc()
        raise
    finally:
        (OUT / "manifest.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"files": len(record["files"]), "searches": len(record["searches"]), "success": record["success"]}))


if __name__ == "__main__":
    main()
