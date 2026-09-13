#!/usr/bin/env python3
"""Check statement-only integrity; this is not an independent semantic approval."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
GIT = Path("/tmp/nla-lean-ra20-worktree")
BASE = "5830ed4fb06da0659414a3deb2a40ad327aca052"
STANDARD = {"propext", "Classical.choice", "Quot.sound"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_bytes(repo, commit, relative):
    argv = ["git", "-C", str(repo), "show", commit + ":" + relative]
    cp = subprocess.run(argv, env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    assert cp.returncode == 0, (argv, cp.returncode, cp.stderr.decode())
    return cp.stdout, {"argv": argv, "exit_code": cp.returncode,
                       "output_sha256": hashlib.sha256(cp.stdout).hexdigest(),
                       "output_bytes": len(cp.stdout), "stderr": cp.stderr.decode()}


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main():
    validation_dir = Path(tempfile.mkdtemp(prefix="validation-attempt-", dir=ROOT / "verification"))
    (validation_dir / "validate_draft.py").write_bytes(Path(__file__).read_bytes())
    report = {"phase": "author statement integrity only", "approval": False,
              "proof_authorized": False, "platform_scope": "macOS source development",
              "argv": sys.argv, "cwd": os.getcwd(), "commands": [], "checks": [],
              "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "inputs": {}}
    def check(name, test):
        assert test, name
        report["checks"].append(name)
    try:
        primary = ["NLA/KE04/Definitions.lean", "Challenge.lean", "NUMERICAL_TARGETS.md",
                   "SourceCorrespondence.md", "README.md", "LICENSE", "lean-toolchain",
                   "lakefile.toml", "lake-manifest.json", "comparator.json",
                   "verification/README.md", "verification/eligibility.json",
                   "verification/original-source-inventory.json", "verification/api-evidence-complete/manifest.json",
                   "verification/statement-development/check_statements.py"]
        for relative in primary:
            p = ROOT / relative
            report["inputs"][relative] = {"sha256": sha(p), "bytes": p.stat().st_size}
        inventory = json.loads((ROOT / "verification/original-source-inventory.json").read_text())
        check("canonical base and exactly 17 original Git-bound sources", inventory["base"] == BASE and len(inventory["files"]) == 17)
        for relative, item in inventory["files"].items():
            p = ROOT / relative
            data, command = git_bytes(GIT, item["commit"], item["upstream_path"])
            report["commands"].append(command)
            check("original Git bytes " + relative, data == p.read_bytes() and git_blob(data) == item["git_blob"] and sha(p) == item["sha256"] and len(data) == item["bytes"])
        registry = json.loads((ROOT / "verification/original-sources/problem_ids.json").read_text())
        # The registry is a direct ID/path map at this pin.
        check("permanent canonical ID/path", registry["KE-04"] == "eigenvalues-and-inverse-problems/KE-04/README.md")
        eligibility = json.loads((ROOT / "verification/eligibility.json").read_text())
        query_path = ROOT / eligibility["evidence"]
        query = json.loads(query_path.read_text())
        check("bounded eligibility evidence hash", sha(query_path) == eligibility["evidence_sha256"])
        check("Solved and no existing canonical Lean project at observed current base", query["upstream_main"] == BASE and query["canonical_status"] == "Solved" and query["canonical_lean_files"] == [])
        check("three complete all-state bounded searches", len(query["queries"]) == 3 and all(q["all_states"] and not q["incomplete_results"] and q["total_count"] == len(q["items"]) for q in query["queries"]))
        check("only classified PRs 6 and 143 returned", {x["number"] for q in query["queries"] for x in q["items"]} == {6, 143})
        current = (ROOT / "verification/original-sources/eigenvalues-and-inverse-problems/KE-04/solution.md").read_text()
        original = (ROOT / "verification/original-submission/solution.md").read_text()
        block = lambda text: text[text.index("## Theorem "):text.index("## Scope and review notes")].strip().encode()
        check("original submitted and current complete theorem/proof block identical", block(current) == block(original) and hashlib.sha256(block(current)).hexdigest() == inventory["proof_block"]["sha256"])
        definitions = (ROOT / "NLA/KE04/Definitions.lean").read_text()
        challenge = (ROOT / "Challenge.lean").read_text()
        clean_defs = re.sub(r"/\-.*?\-/", "", definitions, flags=re.S)
        check("Definitions has no placeholder, axiom, unsafe or native decision declaration", not re.search(r"\b(?:sorry|axiom|unsafe|native_decide)\b", clean_defs))
        defs = ["NLA.KE04." + x for x in re.findall(r"^(?:abbrev|def) (\w+)", definitions, re.M)]
        names = ["NLA.KE04." + x for x in re.findall(r"^theorem (\w+)", challenge, re.M)]
        cfg = json.loads((ROOT / "comparator.json").read_text())
        check("27 concrete definitions and 24 exact reference targets", len(defs) == 27 and len(names) == 24 and cfg["theorem_names"] == names)
        check("all and only Challenge theorem bodies are intentional placeholders", len(re.findall(r":= by sorry", challenge)) == 24)
        check("Comparator configuration has no definition holes and only standard axioms", cfg["definition_names"] == [] and set(cfg["permitted_axioms"]) == STANDARD)
        check("no proof/Solution/publication manifest or private cache in project root", not any((ROOT / p).exists() for p in ["Solution.lean", "NLA/KE04/Proof.lean", "formalization.yaml", ".lake", ".git"]))
        check("no binary build objects or symlinks retained anywhere in project", not any(p.is_symlink() or (p.is_file() and p.suffix in {".olean", ".ilean", ".o", ".so", ".dylib", ".pyc"}) for p in ROOT.rglob("*")))
        success_dir = ROOT / "verification/statement-development/attempt-r5fn2nl_"
        result = json.loads((success_dir / "result.json").read_text())
        check("successful fresh statement-only attempt", result["success"] and result["all_statement_modules_elaborated"] and result["definition_trust_checks_passed"] == 27 and not result["proof_implemented"] and not result["authoritative_linux_gate"] and not result["comparator_run"])
        for item in result["inputs"]:
            p = success_dir / "source" / item["path"]
            check("immutable input snapshot " + item["path"], sha(p) == item["sha256"] and p.stat().st_size == item["bytes"] and p.stat().st_mode & 0o777 == 0o444)
            if item["path"] not in ["InspectDefinitions.lean", "InspectTypes.lean"]:
                check("current source still equals elaborated bytes " + item["path"], (ROOT / item["path"]).read_bytes() == p.read_bytes())
        for cmd in result["commands"]:
            check("actual Lean command exit 0: " + " ".join(cmd["argv"]), cmd["exit_code"] == 0)
            if "log" in cmd:
                check("actual log hash " + cmd["log"], sha(success_dir / cmd["log"]) == cmd["log_sha256"])
        check("four actual Lean modules elaborated", len([x for x in result["commands"] if "log" in x]) == 4)
        for phase in ["dependency_preflight", "dependency_postflight"]:
            check(phase + " has ten unchanged clean pinned sources", len(result[phase]) == 10 and all(x["head"]["exit_code"] == 0 and x["status"]["exit_code"] == 0 and x["status"]["output"] == "" for x in result[phase]))
        pins = {x["name"]: x["rev"] for x in json.loads((ROOT / "lake-manifest.json").read_text())["packages"]}
        check("both actual dependency snapshots equal all ten manifest pins", all(x["head"]["output"].strip() == pins[x["name"]] for phase in ["dependency_preflight", "dependency_postflight"] for x in result[phase]))
        check("Cli is tooling-only and no imported build directory exists", next(x for x in result["dependency_preflight"] if x["name"] == "Cli")["used_in_lean_path"] is False and next(x for x in result["dependency_preflight"] if x["name"] == "Cli")["build_dir_exists"] is False)
        check("all 27 actual transitive definition axiom sets permitted", set(result["definition_axioms"]) == set(defs) and all(set(v) <= STANDARD for v in result["definition_axioms"].values()))
        inspector = (success_dir / "source/InspectDefinitions.lean").read_text()
        check("27 explicit kernel trust checks excluding Challenge", "import Challenge" not in inspector and inspector.count("#assert_trust kernel ") == 27 and 'set_option leancert.trust "kernel"' in inspector)
        check("24 actual placeholder warnings retained", (success_dir / "Challenge.log").read_text().count("warning: declaration uses `sorry`") == 24)
        for attempt in sorted((ROOT / "verification/statement-development").glob("attempt-*")):
            if attempt.name == "attempt-xrn2jug1":
                check("misdirected validator result preserved honestly", json.loads((attempt / "result.json").read_text())["phase"] == "author statement integrity only" and (ROOT / "verification/EVIDENCE-RECOVERY.md").exists())
                continue
            r = json.loads((attempt / "result.json").read_text())
            check("only own private objects hashed and removed " + attempt.name, r["private_prefix_removed"] and not Path(r["private_prefix"]).exists() and len(r["objects"]) == 4 and all(len(o["sha256"]) == 64 for o in r["objects"]))
        ap = ROOT / "verification/api-evidence-complete/manifest.json"
        api = json.loads(ap.read_text())
        check("successful exact selected API/reference source capture", api["success"] and api["all_working_sources_equal_pins"] and len(api["files"]) == 33 and len(api["searches"]) == 5)
        for relative, item in api["files"].items():
            p = ROOT / relative
            check("selected source content and Git blob " + relative, sha(p) == item["sha256"] and p.stat().st_size == item["bytes"] and git_blob(p.read_bytes()) == item["git_blob"])
            if "/tauceti/" not in relative:
                data, cmd = git_bytes(item["repo"], item["commit"], item["upstream_path"])
                report["commands"].append(cmd)
                check("fresh external Git binding " + relative, data == p.read_bytes())
        for item in api["searches"]:
            check("actual search log hash " + item["log"], sha(ROOT / item["log"]) == item["log_sha256"] and item["exit_code"] in [0, 1])
        check("retained initial reporting and both API capture failures", (ROOT / "verification/statement-development/attempt-2n_e6pes/result.json").exists() and (ROOT / "verification/api-evidence/failure.json").exists() and json.loads((ROOT / "verification/api-evidence-final/manifest.json").read_text())["success"] is False)
        report["success"] = True
    except Exception:
        report["success"] = False
        report["error"] = traceback.format_exc()
    (validation_dir / "result.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"attempt": str(validation_dir), "success": report["success"], "checks": len(report["checks"]), "error": report.get("error")}))
    raise SystemExit(0 if report["success"] else 1)


if __name__ == "__main__":
    main()
