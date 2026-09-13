"""Rebuild the manuscript with three pdflatex passes in a temporary folder.

Requires a local LaTeX installation and the packages listed in the TeX
preamble. No third-party Python dependency is required. Only the final
PDF is copied into the package root; compilation logs are shown on error.
"""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    source = root / "IE20_extended_results.tex"
    destination = root / "IE20_extended_results.pdf"
    executable = shutil.which("pdflatex")
    if executable is None:
        raise SystemExit("pdflatex is required but was not found on PATH")
    if not source.is_file():
        raise SystemExit(f"Missing source: {source}")
    with tempfile.TemporaryDirectory(prefix="ie20-pdf-") as directory:
        command = [executable, "-interaction=nonstopmode", "-halt-on-error",
                   f"-output-directory={directory}", str(source)]
        for pass_number in range(1, 4):
            try:
                result = subprocess.run(command, cwd=root, text=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        check=False, timeout=120)
            except subprocess.TimeoutExpired as exc:
                raise SystemExit(f"LaTeX pass {pass_number} timed out") from exc
            if result.returncode:
                print(result.stdout)
                raise SystemExit(f"LaTeX pass {pass_number} failed")
        compiled = Path(directory) / source.with_suffix(".pdf").name
        if not compiled.is_file():
            raise SystemExit("LaTeX returned successfully but produced no PDF")
        shutil.copy2(compiled, destination)
    print(f"Rebuilt {destination}")
    print("Rebuilding changes PDF metadata and may invalidate its manifest hash.")


if __name__ == "__main__":
    main()
