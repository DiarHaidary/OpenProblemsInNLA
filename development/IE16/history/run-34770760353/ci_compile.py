#!/usr/bin/env python3
"""Bounded remote draft feedback only; never authoritative verification."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
WORKFLOW = REPO / ".github/workflows/lean-ie16-development.yml"
RECORDS: list[dict] = []


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*") if p.is_file()
                  and ".lake" not in p.relative_to(ROOT).parts
                  and "__pycache__" not in p.relative_to(ROOT).parts) + [WORKFLOW]


def inventory() -> dict[str, str]:
    return {str(p.relative_to(REPO)): sha(p) for p in files()}


def record_inputs(logs: Path) -> None:
    copied = json.loads((ROOT / "SOURCE_INPUTS.json").read_text())
    for rel, expected in copied["files"].items():
        if sha(ROOT / rel) != expected:
            raise RuntimeError(f"Copied draft source differs from snapshot: {rel}")
    recorded = inventory()
    dump(logs / "source-hashes.json", {
        "purpose": "Development compiler feedback only; not formal verification",
        "repository": os.environ.get("GITHUB_REPOSITORY"),
        "commit": os.environ.get("GITHUB_SHA"),
        "ref": os.environ.get("GITHUB_REF"),
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "files": recorded,
    })
    for rel in recorded:
        target = logs / "inputs" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / rel, target)


def run(logs: Path, label: str, args: list[str], seconds: int) -> int:
    command = ["timeout", "--signal=TERM", "--kill-after=10s", f"{seconds}s", *args]
    start = time.monotonic()
    with (logs / f"{label}.stdout").open("wb") as out, \
            (logs / f"{label}.stderr").open("wb") as err:
        try:
            status = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err,
                                    check=False).returncode
        except OSError as exc:
            err.write((str(exc) + "\n").encode())
            status = 127
    RECORDS.append({"label": label, "command": command,
                    "cwd": "development/IE16", "returncode": status,
                    "elapsed_seconds": round(time.monotonic() - start, 3)})
    dump(logs / "commands.json", RECORDS)
    print(f"{label}: exit {status}", flush=True)
    return status


def check_pins(logs: Path) -> None:
    manifest = json.loads((ROOT / "lake-manifest.json").read_text())
    records = []
    for item in manifest["packages"]:
        path = ROOT / manifest["packagesDir"] / item["name"]
        label = f"pin-{item['name']}"
        status = run(logs, label, ["git", "-C", str(path), "rev-parse", "HEAD"], 30)
        actual = (logs / f"{label}.stdout").read_text().strip()
        records.append({"name": item["name"], "expected": item["rev"],
                        "actual": actual, "returncode": status})
    dump(logs / "dependency-pins.json", records)
    if any(r["returncode"] or r["actual"] != r["expected"] for r in records):
        raise RuntimeError("Dependency revision differs from pinned manifest")


def compile_drafts(logs: Path) -> int:
    status = 1
    reason = None
    try:
        if run(logs, "lake-env", ["lake", "env", "true"], 600):
            raise RuntimeError("Pinned dependency setup failed")
        check_pins(logs)
        if run(logs, "mathlib-cache", ["lake", "exe", "cache", "get"], 900):
            raise RuntimeError("Mathlib development cache fetch failed")

        cert = ROOT / ".lake/packages/leancert"
        cert_source = cert / "LeanCert/Tactic/Verification.lean"
        # This pinned module depends only on Lean's toolchain modules. Avoid a
        # full package build or a second, nested dependency checkout.
        imports = [line.split()[1] for line in cert_source.read_text().splitlines()
                   if line.startswith("import ")]
        if any(mod != "Lean" and not mod.startswith("Lean.") for mod in imports):
            raise RuntimeError("LeanCert direct-module dependency scope changed")
        dump(logs / "leancert-module.json", {"imports": imports, "sha256": sha(cert_source)})
        cert_output = cert / ".lake/build/lib/lean/LeanCert/Tactic/Verification.olean"
        cert_output.parent.mkdir(parents=True, exist_ok=True)
        cert_args = ["lake", "env", "lean", "-M4096", "-j1", "-R", str(cert),
                     "-o", str(cert_output), str(cert_source)]
        previous = run(logs, "compile-leancert-verification", cert_args, 120)
        for name in ["Definitions", "Numeric", "Minimax"]:
            label = f"compile-{name}"
            if previous:
                RECORDS.append({"label": label, "skipped": "Dependency compilation failed"})
                dump(logs / "commands.json", RECORDS)
                continue
            source = Path("NLA/IE16") / f"{name}.lean"
            output = Path(".lake/build/lib/lean/NLA/IE16") / f"{name}.olean"
            (ROOT / output).parent.mkdir(parents=True, exist_ok=True)
            previous = run(logs, label,
                           ["lake", "env", "lean", "-M4096", "-j1",
                            "-o", str(output), str(source)], 120)
        status = 0 if previous == 0 else 1
    except Exception as exc:
        reason = f"{type(exc).__name__}: {exc}"
        (logs / "setup-or-driver-error.txt").write_text(reason + "\n")
        print(reason, file=sys.stderr, flush=True)
    finally:
        before = json.loads((logs / "source-hashes.json").read_text())["files"]
        after = inventory()
        dump(logs / "source-hashes-after.json", after)
        unchanged = before == after
        if not unchanged:
            status = 1
        dump(logs / "result.json", {
            "purpose": "Draft compiler feedback only",
            "authoritative_verification": False,
            "canonical_problem_verified": False,
            "comparator_executed": False,
            "source_inputs_unchanged": unchanged,
            "returncode": status,
            "driver_error": reason,
            "commands": RECORDS,
        })
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record-inputs", action="store_true")
    mode.add_argument("--compile", action="store_true")
    args = parser.parse_args()
    if os.environ.get("GITHUB_ACTIONS") != "true" or sys.platform != "linux":
        raise SystemExit("This development compiler runs only on Linux GitHub Actions.")
    if os.environ.get("GITHUB_REF") != "refs/heads/codex/lean-ie16-development":
        raise SystemExit("This development compiler is restricted to its dedicated branch.")
    logs = Path(os.environ["IE16_LOG_DIR"])
    logs.mkdir(parents=True, exist_ok=True)
    if args.record_inputs:
        record_inputs(logs)
        return 0
    return compile_drafts(logs)


if __name__ == "__main__":
    raise SystemExit(main())
