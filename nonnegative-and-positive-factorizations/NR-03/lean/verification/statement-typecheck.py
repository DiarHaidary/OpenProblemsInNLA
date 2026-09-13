"""Elaborate the NR-03 statement boundary using existing pinned objects.

This script deliberately does not invoke Lake, download dependencies, build a
shared cache, or implement any theorem.  It creates all Lean output and raw
logs in a fresh temporary directory and records the exact dependency heads.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

project = Path(__file__).resolve().parents[1]
deps = Path(os.environ["NR03_DEP_ROOT"])
sysroot = Path(os.environ.get(
    "LEAN_SYSROOT",
    str(Path.home() / ".elan/toolchains/leanprover--lean4---v4.33.1"),
))
lean = sysroot / "bin/lean"
prefix = Path(tempfile.mkdtemp(prefix="nla-nr03-statement-typecheck-"))
out = prefix / "objects"
(out / "NLA/NR03").mkdir(parents=True)
record: dict[str, object] = {
    "phase": "statements only",
    "project": str(project),
    "commands": [],
    "dependencies": {},
}


def run(args: list[object], *, cwd: Path = project, log: str | None = None) -> str:
    result = subprocess.run(
        [str(a) for a in args],
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout.decode()
    command = {
        "argv": [str(a) for a in args],
        "cwd": str(cwd),
        "exit_code": result.returncode,
        "output": output,
    }
    record["commands"].append(command)  # type: ignore[union-attr]
    if log is not None:
        (prefix / log).write_bytes(result.stdout)
    if result.returncode:
        (prefix / "EVIDENCE.json").write_text(json.dumps(record, indent=2) + "\n")
        raise SystemExit(f"Lean statement check failed; evidence: {prefix}")
    return output


env = os.environ.copy()
version = run([lean, "--version"])
if "Lean (version 4.33.1" not in version:
    raise SystemExit(f"unexpected Lean version: {version}")

manifest = json.loads((project / "lake-manifest.json").read_text())
for package in manifest["packages"]:
    name = package["name"]
    package_root = deps / name
    head = run(["git", "rev-parse", "HEAD"], cwd=package_root).strip()
    status = run(
        ["git", "status", "--porcelain=1", "--untracked-files=no"],
        cwd=package_root,
    )
    if head != package["rev"] or status:
        raise SystemExit(f"dependency is not the pinned clean checkout: {name}")
    record["dependencies"][name] = {  # type: ignore[index]
        "revision": head,
        "tracked_sources_clean": True,
    }

lib_paths = [
    str(deps / package["name"] / ".lake/build/lib/lean")
    for package in manifest["packages"]
]
env["LEAN_PATH"] = os.pathsep.join([str(out), *lib_paths, str(sysroot / "lib/lean")])
record["lean_path"] = env["LEAN_PATH"]
record["source_hashes"] = {
    path: hashlib.sha256((project / path).read_bytes()).hexdigest()
    for path in ["NLA/NR03/Definitions.lean", "Challenge.lean"]
}

run(
    [
        lean,
        "-R",
        project,
        "-o",
        out / "NLA/NR03/Definitions.olean",
        project / "NLA/NR03/Definitions.lean",
    ],
    log="Definitions.log",
)
run(
    [
        lean,
        "-R",
        project,
        "-o",
        out / "Challenge.olean",
        project / "Challenge.lean",
    ],
    log="Challenge.log",
)

record["result"] = (
    "PASS: definitions and ten intentional statement placeholders elaborated "
    "with pinned dependencies"
)
(prefix / "EVIDENCE.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"result": record["result"], "evidence": str(prefix)}))
