"""Sinkronkan materi siap pakai per pertemuan ke folder Materials/.

Struktur keluaran:
Materials/
  P01 - Understanding Images & Image Processing/
    P01_image_processing_eda.html
    P01_image_processing_eda.pdf
    P01_image_processing_eda.pptx
    P01_image_processing_eda.ipynb
    solutions/
      P01_image_processing_eda.ipynb
    assets/
      P01/
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATERIALS_DIR = ROOT / "Materials"

SESSIONS = [
    {
        "code": "P01",
        "folder": "P01 - Understanding Images, Image Processing & EDA",
        "slug": "P01_image_processing_eda",
    },
]


def sync_session(session: dict[str, str]) -> Path:
    code = session["code"]
    slug = session["slug"]
    title = session["folder"]
    target_dir = MATERIALS_DIR / title
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Slides (.html, .pdf, .pptx) dengan nama sesuai judul pertemuan
    for ext in ("html", "pdf", "pptx"):
        src = ROOT / "slides" / f"{slug}.{ext}"
        if src.exists():
            shutil.copy2(src, target_dir / f"{title}.{ext}")

    # 2. Slide assets agar file .html bisa dibuka langsung dari Materials/
    assets_src = ROOT / "slides" / "assets" / code
    if assets_src.exists():
        assets_dst = target_dir / "assets" / code
        if assets_dst.exists():
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)

    # 3. Notebook peserta & solusi (.ipynb)
    nb_src = ROOT / "notebooks" / f"{slug}.ipynb"
    if nb_src.exists():
        shutil.copy2(nb_src, target_dir / f"{title}.ipynb")

    sol_src = ROOT / "notebooks" / "solutions" / f"{slug}.ipynb"
    if sol_src.exists():
        sol_dir = target_dir / "solutions"
        sol_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sol_src, sol_dir / f"{title}.ipynb")

    # 4. Data sampel agar notebook di Materials/ bisa langsung dijalankan standalone
    data_src = ROOT / "data" / "sample"
    if data_src.exists():
        data_dst = target_dir / "data" / "sample"
        if data_dst.exists():
            shutil.rmtree(data_dst)
        shutil.copytree(data_src, data_dst)

    return target_dir


def main() -> None:
    MATERIALS_DIR.mkdir(parents=True, exist_ok=True)
    for session in SESSIONS:
        out_dir = sync_session(session)
        files = sorted(
            str(p.relative_to(out_dir))
            for p in out_dir.rglob("*")
            if p.is_file()
        )
        print(f"Synced {out_dir.relative_to(ROOT)} ({len(files)} files)")


if __name__ == "__main__":
    main()

