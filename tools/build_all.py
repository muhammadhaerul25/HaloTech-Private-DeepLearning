"""Orkestrator build lengkap untuk HaloTech Private Deep Learning (P01).

HTML (slides/P01_image_processing_eda.html) adalah Sumber Utama (Main Source).
Menjalankan seluruh pipeline secara berurutan agar semua format selalu sinkron:
1. Generate dataset sampel sintetis (data/sample/)
2. Generate dek interaktif HTML5 — Main Source (slides/P01_image_processing_eda.html)
3. Ekspor PDF berkualitas tinggi dari HTML (slides/P01_image_processing_eda.pdf)
4. Generate notebook peserta & solusi selaras HTML (notebooks/)
5. Generate visualisasi & dek PPTX selaras HTML (slides/P01_image_processing_eda.pptx)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "tools"

PIPELINE = [
    ("1/5 Generate sample dataset", "make_sample_data.py"),
    ("2/5 Build interactive HTML slides (Main Source)", "build_html_slides_P01.py"),
    ("3/5 Export high-quality PDF from HTML", "export_pdf_P01.py"),
    ("4/5 Build hands-on notebooks synced with HTML", "build_notebooks_P01.py"),
    ("5/5 Build PPTX & visual assets synced with HTML", "build_slides_P01.py"),
]


def main() -> None:
    for label, script in PIPELINE:
        print(f"\n=== {label} ({script}) ===")
        result = subprocess.run([sys.executable, str(TOOLS_DIR / script)], cwd=str(ROOT))
        if result.returncode != 0:
            raise SystemExit(f"Gagal pada {script} (exit code {result.returncode})")
    print("\nSeluruh pipeline build P01 selesai dengan sukses!")


if __name__ == "__main__":
    main()
