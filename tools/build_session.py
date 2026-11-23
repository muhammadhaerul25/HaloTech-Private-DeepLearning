"""Unified CLI Orchestrator for HaloTech Private Deep Learning (P01–P08).

Usage:
    python tools/build_session.py P01 --validate
    python tools/build_session.py P02 --validate
    python tools/build_session.py P01 --validate-only
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT_DIR / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from core.exporter import export_pdf, export_pptx, export_presenter_script  # noqa: E402
from core.registry import SessionConfig, get_session  # noqa: E402
from core.validator import load_presenter_explanations, validate_session  # noqa: E402


def _run_py(script_path: Path, label: str) -> None:
    print(f"\n=== {label} ({script_path.relative_to(ROOT_DIR)}) ===")
    res = subprocess.run([sys.executable, str(script_path)], cwd=str(ROOT_DIR))
    if res.returncode != 0:
        raise SystemExit(f"Gagal pada {script_path.name} (exit code {res.returncode})")


def build_legacy_p01(session: SessionConfig, skip_data: bool = False) -> None:
    """Run preserved P01 build pipeline without changing P01 visual design."""
    if not skip_data:
        _run_py(TOOLS_DIR / "make_sample_data.py", "1/6 Generate sample dataset & MNIST")
    _run_py(TOOLS_DIR / "build_slides_P01.py", "2/6 Generate P01 visual assets & sample_stats.json")
    _run_py(TOOLS_DIR / "build_html_slides_P01.py", "3/6 Build P01 interactive HTML slides (Main Source)")
    _run_py(TOOLS_DIR / "export_pdf_P01.py", "4/6 Export P01 PDF (16:9) & PPTX HD (16:9 + Notes)")
    _run_py(TOOLS_DIR / "build_notebooks_P01.py", "5/6 Build P01 hands-on notebooks (Student & Solution)")
    _run_py(TOOLS_DIR / "build_presenter_script_P01.py", "6/6 Build P01 per-slide presenter script PDF")


def build_modular_session(session: SessionConfig) -> None:
    """Run standardized modular pipeline for P02–P08 from tools/sessions/P{NN}/."""
    code_dir = session.code_dir
    if not code_dir.exists():
        raise SystemExit(
            f"Folder kode sesi belum ada: {code_dir}\n"
            f"Jalankan dulu: python tools/init_session.py {session.id}"
        )

    assets_script = code_dir / "build_assets.py"
    html_script = code_dir / "build_html.py"
    nb_script = code_dir / "build_notebooks.py"

    if assets_script.exists():
        _run_py(assets_script, f"1/6 Generate visual assets & data JSON ({session.id})")
    else:
        print(f"\n=== 1/6 Skip build_assets.py (tidak ada untuk {session.id}) ===")

    _run_py(html_script, f"2/6 Build interactive HTML slides — SSOT ({session.id})")

    explanations = load_presenter_explanations(session)

    print(f"\n=== 3/6 Export 16:9 Vector PDF from HTML ({session.id}) ===")
    export_pdf(session)

    print(f"\n=== 4/6 Export 16:9 Retina HD PPTX + Speaker Notes ({session.id}) ===")
    export_pptx(session, explanations=explanations)

    print(f"\n=== 5/6 Export A4 Presenter Script PDF ({session.id}) ===")
    export_presenter_script(session, explanations=explanations)

    _run_py(nb_script, f"6/6 Build hands-on notebooks — Student & Solution ({session.id})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build & validate HaloTech Deep Learning session (P01–P08).")
    parser.add_argument("session", help="ID sesi, mis. P01, P02, ..., P08")
    parser.add_argument("--validate", action="store_true", help="Jalankan 6 gerbang validasi DoD setelah build")
    parser.add_argument("--validate-only", action="store_true", help="Hanya jalankan validasi tanpa rebuild")
    parser.add_argument("--skip-data", action="store_true", help="(P01) Lewati regenerasi data/sample & data/mnist")
    parser.add_argument("--skip-nb-exec", action="store_true", help="Lewati eksekusi jupyter nbconvert saat validasi")
    parser.add_argument("--skip-portal", action="store_true", help="Lewati pemeriksaan sinkronisasi sessions.json/vercel.json/sw.js")
    args = parser.parse_args()

    session = get_session(args.session)

    if not args.validate_only:
        if session.is_legacy_p01:
            build_legacy_p01(session, skip_data=args.skip_data)
        else:
            build_modular_session(session)
        print(f"\nPipeline build {session.id} selesai!")

    if args.validate or args.validate_only:
        print(f"\n=== Validasi 6 Gerbang Definition of Done ({session.id}) ===")
        report = validate_session(
            session,
            execute_notebooks=not args.skip_nb_exec,
            check_portal=not args.skip_portal,
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"\n✅ Seluruh gerbang validasi {session.id} LOLOS!")


if __name__ == "__main__":
    main()
