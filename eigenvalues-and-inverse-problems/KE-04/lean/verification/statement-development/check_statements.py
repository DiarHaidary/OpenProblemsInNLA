#!/usr/bin/env python3
"""Author development: immutable inputs, fresh private objects, read-only dependencies.

This elaborates statement placeholders. It is not a proof build or Comparator run.
Each invocation retains a new attempt, including failures; own objects are removed.
"""
from pathlib import Path
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
DEV = ROOT / "verification/statement-development"
PACKAGES = Path("/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages")
LEAN = Path("/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean")
ORDER = ["batteries", "Qq", "aesop", "proofwidgets", "importGraph",
         "LeanSearchClient", "plausible", "mathlib", "leancert"]
STANDARD = {"propext", "Classical.choice", "Quot.sound"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def command(argv, cwd, env, timeout=60):
    start = time.time()
    try:
        cp = subprocess.run(argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=timeout)
        return {"argv": list(map(str, argv)), "cwd": str(cwd), "exit_code": cp.returncode,
                "output": cp.stdout, "seconds": time.time() - start}
    except subprocess.TimeoutExpired as e:
        out = e.stdout or ""
        if isinstance(out, bytes):
            out = out.decode(errors="replace")
        return {"argv": list(map(str, argv)), "cwd": str(cwd), "exit_code": None,
                "timed_out_seconds": timeout, "output": out, "seconds": time.time() - start}


def main():
    attempt = Path(tempfile.mkdtemp(prefix="attempt-", dir=DEV))
    source = attempt / "source"
    source.mkdir()
    private = Path(tempfile.mkdtemp(prefix="nla-ke04-statement-objects-"))
    result = {"phase": "author statement-only development", "proof_implemented": False,
              "authoritative_linux_gate": False, "comparator_run": False,
              "platform": platform.platform(), "private_prefix": str(private),
              "utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "runner_argv": sys.argv, "runner_cwd": os.getcwd(),
              "runner_sha256": sha(Path(__file__).resolve()),
              "commands": [], "inputs": [], "dependency_preflight": [],
              "dependency_postflight": [], "objects": [], "errors": []}
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    originals = ["NLA/KE04/Definitions.lean", "Challenge.lean", "lean-toolchain",
                 "lakefile.toml", "lake-manifest.json", "comparator.json",
                 "verification/statement-development/check_statements.py"]
    try:
        for relative in originals:
            origin = ROOT / relative
            target = source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(origin.read_bytes())
            target.chmod(0o444)
            result["inputs"].append({"path": relative, "sha256": sha(target),
                                     "bytes": target.stat().st_size, "mode": "0444"})
        definitions = (source / originals[0]).read_text()
        challenge = (source / "Challenge.lean").read_text()
        names = ["NLA.KE04." + n for n in re.findall(r"^(?:abbrev|def) (\w+)", definitions, re.M)]
        targets = ["NLA.KE04." + n for n in re.findall(r"^theorem (\w+)", challenge, re.M)]
        config = json.loads((source / "comparator.json").read_text())
        assert config["theorem_names"] == targets
        assert config["definition_names"] == []
        assert set(config["permitted_axioms"]) == STANDARD
        assert len(targets) == len(re.findall(r":= by sorry", challenge))
        assert not re.search(r"\b(?:sorry|axiom|unsafe|native_decide)\b", re.sub(r"/\-.*?\-/", "", definitions, flags=re.S))
        inspect = "import NLA.KE04.Definitions\nimport LeanCert.Tactic.Verification\n\nset_option leancert.trust \"kernel\"\n"
        inspect += "\n".join(f"#assert_trust kernel {n}\n#print axioms {n}" for n in names) + "\n"
        types = "import Challenge\n\n" + "\n".join(f"#check {n}" for n in targets) + "\n"
        for relative, text in [("InspectDefinitions.lean", inspect), ("InspectTypes.lean", types)]:
            target = source / relative
            target.write_text(text)
            target.chmod(0o444)
            result["inputs"].append({"path": relative, "sha256": sha(target),
                                     "bytes": target.stat().st_size, "mode": "0444 generated inspector"})
        result.update(definition_names=names, theorem_names=targets, challenge_holes=len(targets))
        manifest = json.loads((source / "lake-manifest.json").read_text())
        assert len(manifest["packages"]) == 10
        for dep in manifest["packages"]:
            path = PACKAGES / dep["name"]
            head = command(["git", "rev-parse", "HEAD"], path, env)
            status = command(["git", "status", "--porcelain", "--untracked-files=all"], path, env)
            item = {"name": dep["name"], "expected_rev": dep["rev"], "head": head, "status": status,
                    "build_dir_exists": (path / ".lake/build/lib/lean").is_dir(),
                    "used_in_lean_path": dep["name"] in ORDER}
            result["dependency_preflight"].append(item)
            assert head["exit_code"] == 0 and head["output"].strip() == dep["rev"], item
            assert status["exit_code"] == 0 and status["output"] == "", item
            if dep["name"] in ORDER:
                assert item["build_dir_exists"], item
        env["LEAN_PATH"] = ":".join([str(private)] + [str(PACKAGES / d / ".lake/build/lib/lean") for d in ORDER])
        env["LEAN_SRC_PATH"] = str(source)
        result["lean_path"] = env["LEAN_PATH"]
        result["lean_src_path"] = env["LEAN_SRC_PATH"]
        result["lean_binary_sha256"] = sha(LEAN)
        version = command([str(LEAN), "--version"], source, env)
        result["commands"].append(version)
        assert version["exit_code"] == 0 and "4.33.1" in version["output"]
        record(attempt / "preflight.json", result)
        modules = [("NLA/KE04/Definitions.lean", "NLA/KE04/Definitions.olean", "Definitions"),
                   ("Challenge.lean", "Challenge.olean", "Challenge"),
                   ("InspectDefinitions.lean", "InspectDefinitions.olean", "InspectDefinitions"),
                   ("InspectTypes.lean", "InspectTypes.olean", "InspectTypes")]
        for relative, obj, label in modules:
            output = private / obj
            output.parent.mkdir(parents=True, exist_ok=True)
            run = command([str(LEAN), "-o", str(output), relative], source, env)
            (attempt / (label + ".log")).write_text(run.pop("output"))
            run["log"] = label + ".log"
            run["log_sha256"] = sha(attempt / run["log"])
            result["commands"].append(run)
            record(attempt / "progress.json", result)
            assert run["exit_code"] == 0, run
        inspect_log = (attempt / "InspectDefinitions.log").read_text()
        reports = {}
        for match in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", inspect_log):
            reports[match[1]] = {x.strip() for x in match[2].split(",") if x.strip()}
        for match in re.finditer(r"'([^']+)' does not depend on any axioms", inspect_log):
            reports[match[1]] = set()
        assert set(reports) == set(names), {"missing": sorted(set(names) - set(reports)), "extra": sorted(set(reports) - set(names))}
        assert all(axioms <= STANDARD for axioms in reports.values()), reports
        # At the pinned release #assert_trust succeeds silently and errors on failure.
        # Its exact generated command count plus the inspector's exit 0 is the evidence.
        assert (source / "InspectDefinitions.lean").read_text().count("#assert_trust kernel ") == len(names)
        result["definition_axioms"] = {k: sorted(v) for k, v in reports.items()}
        result["all_statement_modules_elaborated"] = True
        result["definition_trust_checks_passed"] = len(names)
    except Exception:
        result["errors"].append(traceback.format_exc())
    finally:
        for relative in originals:
            source_file = source / relative
            if source_file.is_file():
                original = ROOT / relative
                result.setdefault("post_source_bindings", []).append({"path": relative,
                    "snapshot_sha256": sha(source_file), "current_sha256": sha(original),
                    "unchanged": sha(source_file) == sha(original)})
        manifest_path = source / "lake-manifest.json"
        if manifest_path.is_file():
            for dep in json.loads(manifest_path.read_text())["packages"]:
                path = PACKAGES / dep["name"]
                result["dependency_postflight"].append({"name": dep["name"],
                    "head": command(["git", "rev-parse", "HEAD"], path, env),
                    "status": command(["git", "status", "--porcelain", "--untracked-files=all"], path, env)})
        for obj in sorted(private.rglob("*")):
            if obj.is_file():
                result["objects"].append({"path": str(obj.relative_to(private)),
                    "sha256": sha(obj), "bytes": obj.stat().st_size})
        shutil.rmtree(private)
        result["private_prefix_removed"] = not private.exists()
        result["utc_end"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        result["success"] = not result["errors"]
        record(attempt / "result.json", result)
    print(json.dumps({"attempt": str(attempt), "success": result["success"], "errors": result["errors"],
                      "objects_removed": len(result["objects"])}))
    raise SystemExit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
