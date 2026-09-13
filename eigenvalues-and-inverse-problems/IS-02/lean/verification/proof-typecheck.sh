#!/usr/bin/env bash
set -euo pipefail

# Local proof-stage check. Lean is invoked directly; dependency objects are read
# from an existing pinned package tree and all newly written artifacts use one
# fresh private prefix. This is not the authoritative Linux Comparator job.
#
# Required usage:
#   IS02_DEP_ROOT=/path/to/existing/.lake/packages \
#     verification/proof-typecheck.sh
#
# IS02_DEP_ROOT must contain the ten package directories named by
# lake-manifest.json. The script checks every manifest revision and requires
# every tracked dependency worktree to be clean before compiling.
# Optional variables are LEAN_BIN, LEAN_SYSROOT and IS02_TYPECHECK_TMPDIR.

project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
dep_root=${IS02_DEP_ROOT:?Set IS02_DEP_ROOT to an existing .lake/packages directory}
lean_bin=${LEAN_BIN:-lean}
tmp_root=${IS02_TYPECHECK_TMPDIR:-${TMPDIR:-/tmp}}
prefix=$(mktemp -d "${tmp_root%/}/nla-is02-proof-typecheck.XXXXXX")
out="$prefix/out"
mkdir -p "$out/NLA/IS02" "$prefix/logs"

manifest="$project_dir/lake-manifest.json"
command_results="$prefix/command-results.ndjson"
: > "$command_results"

# Each invocation gets a private raw log. command-results.ndjson records the
# command label, exit code and log path; dependency-check.json records the
# inner git commands and their complete stdout/stderr as well.
run_capture() {
  local label=$1
  shift
  local log="$prefix/logs/$label.log"
  {
    printf 'cwd: %s\n' "$PWD"
    printf 'argv:'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  local rc
  if "$@" >> "$log" 2>&1; then
    rc=0
  else
    rc=$?
  fi
  printf '%s\t%s\t%s\n' "$label" "$rc" "$log" >> "$command_results"
  if [ "$rc" -ne 0 ]; then
    cat "$log"
    return "$rc"
  fi
}

cd "$project_dir"

# Check every package in the pinned manifest before constructing LEAN_PATH.
run_capture dependency-pins python3 - "$manifest" "$dep_root" "$prefix/dependency-check.json" <<'PY'
import json
from pathlib import Path
import subprocess
import sys

manifest_path, dep_root, report_path = sys.argv[1:]
manifest = json.loads(Path(manifest_path).read_text())
packages = manifest.get("packages", [])
records = []
all_ok = len(packages) == 10

def command(argv, cwd):
    try:
        proc = subprocess.run(argv, cwd=cwd, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {
            "argv": argv,
            "cwd": str(cwd),
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except Exception as exc:
        return {
            "argv": argv,
            "cwd": str(cwd),
            "exit_code": 127,
            "stdout": "",
            "stderr": repr(exc),
        }

for package in packages:
    name = package["name"]
    expected = package["rev"]
    package_dir = Path(dep_root) / name
    head = command(["git", "rev-parse", "HEAD"], package_dir)
    clean = command(["git", "status", "--porcelain=1", "--untracked-files=no"], package_dir)
    observed = head["stdout"].strip()
    clean_ok = clean["exit_code"] == 0 and clean["stdout"] == "" and clean["stderr"] == ""
    pinned_ok = head["exit_code"] == 0 and observed == expected
    item_ok = pinned_ok and clean_ok
    all_ok = all_ok and item_ok
    records.append({
        "name": name,
        "expected_revision": expected,
        "observed_revision": observed,
        "revision_match": pinned_ok,
        "tracked_sources_clean": clean_ok,
        "ok": item_ok,
        "commands": [head, clean],
    })

report = {
    "manifest": str(Path(manifest_path)),
    "dependency_root": str(Path(dep_root)),
    "expected_package_count": 10,
    "observed_package_count": len(packages),
    "all_ten_clean_and_pinned": all_ok,
    "packages": records,
}
Path(report_path).write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({
    "all_ten_clean_and_pinned": all_ok,
    "package_count": len(packages),
    "report": report_path,
}))
if not all_ok:
    raise SystemExit(1)
PY

lean_path="$out"
for package in Cli batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib leancert; do
  lean_path="$lean_path:$dep_root/$package/.lake/build/lib/lean"
done
lean_path="$lean_path:${LEAN_SYSROOT:-$HOME/.elan/toolchains/leanprover--lean4---v4.33.1/lib/lean}"
export LEAN_PATH="$lean_path"

run_capture lean-version "$lean_bin" --version
grep -F 'Lean (version 4.33.1' "$prefix/logs/lean-version.log" >/dev/null
run_capture definitions "$lean_bin" -R "$project_dir" \
  -o "$out/NLA/IS02/Definitions.olean" \
  "$project_dir/NLA/IS02/Definitions.lean"
run_capture proof "$lean_bin" -R "$project_dir" \
  -o "$out/NLA/IS02/Proof.olean" \
  "$project_dir/NLA/IS02/Proof.lean"
run_capture solution "$lean_bin" -R "$project_dir" \
  -o "$out/Solution.olean" \
  "$project_dir/Solution.lean"

run_capture source-hashes python3 - "$project_dir" "$manifest" "$prefix/source-hashes.sha256" <<'PY'
from pathlib import Path
import hashlib
import sys

project, manifest, output = map(Path, sys.argv[1:])
paths = [
    project / "NLA/IS02/Definitions.lean",
    project / "NLA/IS02/Proof.lean",
    project / "Solution.lean",
    manifest,
]
lines = []
for path in paths:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path}")
Path(output).write_text("\n".join(lines) + "\n")
print(Path(output).read_text(), end="")
PY

version=$(grep -F 'Lean (version' "$prefix/logs/lean-version.log" | head -1)
printf 'proof-stage direct Lean check: PASS\n'
printf 'lean: %s\n' "$version"
printf 'output prefix: %s\n' "$prefix"
printf 'dependency report: %s\n' "$prefix/dependency-check.json"
printf 'raw command records: %s\n' "$command_results"
printf 'source hashes: %s\n' "$prefix/source-hashes.sha256"
printf 'solution exports: 9; #assert_trust kernel and #print axioms completed\n'
