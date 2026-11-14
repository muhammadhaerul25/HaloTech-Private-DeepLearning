"""Orkestrator build lengkap untuk HaloTech Private Deep Learning (P01).

Menjalankan seluruh pipeline secara berurutan:
1. Generate dataset sampel sintetis (data/sample/)
2. Generate visualisasi & dek PPTX (slides/P01_image_processing_eda.pptx)
3. Generate dek interaktif HTML5 (slides/P01_image_processing_eda.html)
4. Ekspor PDF berkualitas tinggi dengan split Q&A slides (slides/P01_image_processing_eda.pdf)
5. Generate notebook peserta & solusi (notebooks/)
6. Sinkronkan seluruh materi siap pakai ke Materials/
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "tools"

PIPELINE = [
    ("1/6 Generate sample dataset", "make_sample_data.py"),
    ("2/6 Build PPTX & visual assets", "build_slides_P01.py"),
    ("3/6 Build interactive HTML slides", "build_html_slides_P01.py"),
    ("4/6 Export high-quality PDF (split Q&A)", "export_pdf_P01.py"),
    ("5/6 Build hands-on notebooks", "build_notebooks_P01.py"),
    ("6/6 Sync Materials bundle", "sync_materials.py"),
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
