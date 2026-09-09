"""Compile complementary TeX notes to files/<course>/extra/*.pdf."""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from extra_materials_catalog import ITEMS  # noqa: E402

PDFLATEX = pathlib.Path(r"C:\Users\Lenovo\AppData\Roaming\TinyTeX\bin\windows\pdflatex.exe")
TLMGR = PDFLATEX.with_name("tlmgr.bat")
if not TLMGR.exists():
    TLMGR = PDFLATEX.with_name("tlmgr.exe")

AUX = {".aux", ".log", ".out", ".toc", ".bcf", ".run.xml", ".bbl", ".blg", ".nav", ".snm", ".vrb"}


def install_pkg(name: str) -> None:
    cmd = [str(TLMGR), "install", name]
    subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)


def missing_packages(log: str) -> list[str]:
    return re.findall(r"! LaTeX Error: File `([^']+)' not found", log)


def sanitize_tex(text: str) -> str:
    idx = text.find("\\documentclass")
    if idx > 0:
        text = text[idx:]
    text = text.replace("\ufffd", "")
    text = text.replace("\\usepackage{microtype}", "% microtype")
    text = re.sub(
        r"\\usepackage\[style=ieee[^\]]*\]\{biblatex\}",
        r"\\usepackage[style=numeric]{biblatex}",
        text,
    )
    text = text.replace("\\usepackage[latin1]{inputenc}", "\\usepackage[utf8]{inputenc}")
    text = text.replace("\\usepackage[dvips]{epsfig}", "% epsfig")
    return text


def compile_one(src: pathlib.Path, work: pathlib.Path) -> pathlib.Path | None:
    if not src.exists():
        print(f"MISSING {src}")
        return None
    work.mkdir(parents=True, exist_ok=True)
    dest_tex = work / src.name
    raw = src.read_text(encoding="utf-8", errors="replace")
    dest_tex.write_text(sanitize_tex(raw), encoding="utf-8")
    src_dir = src.parent
    for extra in src_dir.iterdir():
        if extra.suffix.lower() in {".bib", ".png", ".jpg", ".jpeg", ".pdf"}:
            target = work / extra.name
            if not target.exists():
                shutil.copy2(extra, target)
    refs = work / "references.bib"
    if refs.exists() and not (work / "refs.bib").exists():
        shutil.copy2(refs, work / "refs.bib")

    for _attempt in range(4):
        proc = subprocess.run(
            [str(PDFLATEX), "-interaction=nonstopmode", dest_tex.name],
            cwd=str(work),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        pdf = work / (dest_tex.stem + ".pdf")
        if pdf.exists() and pdf.stat().st_size > 1000:
            if proc.returncode == 0:
                subprocess.run(
                    [str(PDFLATEX), "-interaction=nonstopmode", dest_tex.name],
                    cwd=str(work),
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
            return pdf
        log = (proc.stdout or "") + (proc.stderr or "")
        pkgs = missing_packages(log)
        sty = [p[:-4] if p.endswith(".sty") else p[:-4] if p.endswith(".cls") else p for p in pkgs]
        sty = [p for p in sty if p]
        if not sty:
            print(f"FAIL {src.name}", flush=True)
            err = [ln for ln in log.splitlines() if ln.startswith("!") or "Error" in ln][:8]
            for ln in err:
                print("  ", ln.encode("ascii", "replace").decode("ascii"), flush=True)
            return None
        for pkg in sty:
            print(f"  install {pkg}")
            install_pkg(pkg)
    print(f"FAIL {src.name} after package installs")
    return None


def main() -> None:
    work = ROOT / "files" / "_extra-compile"
    work.mkdir(parents=True, exist_ok=True)
    only_missing = "--retry-missing" in sys.argv
    ok = 0
    fail = 0
    copied = set()
    for item in ITEMS:
        courses = {c for c, _w in item["assign"]}
        if only_missing and all((ROOT / "files" / c / "extra" / item["pdf"]).exists() for c in courses):
            ok += 1
            continue
        src = ROOT / item["src"]
        try:
            pdf = compile_one(src, work / pathlib.Path(item["pdf"]).stem)
        except Exception as exc:
            print(f"FAIL {src.name}: {exc}", flush=True)
            fail += 1
            continue
        if pdf is None:
            fail += 1
            continue
        ok += 1
        courses = {c for c, _w in item["assign"]}
        for course in courses:
            out_dir = ROOT / "files" / course / "extra"
            out_dir.mkdir(parents=True, exist_ok=True)
            dest = out_dir / item["pdf"]
            shutil.copy2(pdf, dest)
            copied.add(str(dest.relative_to(ROOT)))
            print(f"OK {dest.relative_to(ROOT)}")
    print(f"Compiled {ok}, failed {fail}, wrote {len(copied)} PDFs")


if __name__ == "__main__":
    main()
