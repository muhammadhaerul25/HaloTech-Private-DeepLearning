"""Prepare structured, web- & Colab-ready JPEG dataset from `data/dataset _frozen_v1.zip`.

Non-destructive: reads `data/dataset _frozen_v1.zip` in read-only mode and writes:
- `data/frozen_v1/<kelas>/<kondisi>/<kelas>_<kondisi>_<NN>.jpg` (RGB, EXIF-corrected, max side 768px)
- `data/frozen_v1/metadata.csv` (complete inventory with kelas, kondisi, sub_kondisi, sesi_foto, EDA metrics)
- `data/frozen_v1/dataset_summary.json` (real descriptive stats for P02–P08 slides & notebooks)

This makes the Frozen dataset natively readable by Pillow, OpenCV, TensorFlow/Keras,
and web browsers without requiring `pillow-heif` at training/serving time, while keeping
total size GitHub-friendly (~5–10 MB instead of 166 MB HEIC archive).
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

ROOT_DIR = Path(__file__).resolve().parent.parent
ZIP_PATH = ROOT_DIR / "data" / "dataset _frozen_v1.zip"
OUT_DIR = ROOT_DIR / "data" / "frozen_v1"
MAX_SIDE = 768
JPEG_QUALITY = 88

CLASS_NAMES = ["anna", "elsa", "kristoff", "olaf", "sven"]
CONDITIONS = ["polos", "ramai"]


def classify_frozen_v1(img_num: int) -> tuple[str, str, str, str]:
    """Verified visual mapping of `Frozen 1/IMG_<num>.HEIC` -> (kelas, kondisi, sub_kondisi, sesi_foto)."""
    # Sesi 1: Polos terang (dipegang tangan, dinding terang)
    if 6594 <= img_num <= 6598: return ("sven", "polos", "polos_terang", "S01_polos_terang")
    if 6599 <= img_num <= 6602: return ("elsa", "polos", "polos_terang", "S01_polos_terang")
    if 6603 <= img_num <= 6606: return ("anna", "polos", "polos_terang", "S01_polos_terang")
    if 6611 <= img_num <= 6614: return ("kristoff", "polos", "polos_terang", "S01_polos_terang")
    if 6619 <= img_num <= 6622: return ("olaf", "polos", "polos_terang", "S01_polos_terang")

    # Sesi 2: Ramai rak terang (rak pajangan Disney)
    if 6665 <= img_num <= 6669: return ("sven", "ramai", "ramai_rak_terang", "S02_ramai_terang")
    if 6678 <= img_num <= 6682: return ("anna", "ramai", "ramai_rak_terang", "S02_ramai_terang")
    if 6691 <= img_num <= 6694: return ("elsa", "ramai", "ramai_rak_terang", "S02_ramai_terang")
    if 6695 <= img_num <= 6700: return ("olaf", "ramai", "ramai_rak_terang", "S02_ramai_terang")
    if 6701 <= img_num <= 6704: return ("kristoff", "ramai", "ramai_rak_terang", "S02_ramai_terang")

    # Sesi 3: Polos terang (batch 2)
    if 6799 <= img_num <= 6802: return ("elsa", "polos", "polos_terang", "S03_polos_terang")
    if 6803 <= img_num <= 6806: return ("anna", "polos", "polos_terang", "S03_polos_terang")
    if 6807 <= img_num <= 6810: return ("kristoff", "polos", "polos_terang", "S03_polos_terang")
    if 6811 <= img_num <= 6814: return ("sven", "polos", "polos_terang", "S03_polos_terang")
    if 6815 <= img_num <= 6818: return ("olaf", "polos", "polos_terang", "S03_polos_terang")

    # Sesi 4: Polos redup / lampu hangat
    if 6819 <= img_num <= 6824: return ("elsa", "polos", "polos_redup", "S04_polos_redup")
    if 6825 <= img_num <= 6828: return ("kristoff", "polos", "polos_redup", "S04_polos_redup")
    if 6829 <= img_num <= 6832: return ("sven", "polos", "polos_redup", "S04_polos_redup")
    if 6833 <= img_num <= 6836: return ("anna", "polos", "polos_redup", "S04_polos_redup")
    if 6837 <= img_num <= 6840: return ("olaf", "polos", "polos_redup", "S04_polos_redup")

    # Sesi 5: Ramai rak redup / variasi sudut
    if 6841 <= img_num <= 6844: return ("anna", "ramai", "ramai_rak_redup", "S05_ramai_redup")
    if 6845 <= img_num <= 6848: return ("elsa", "ramai", "ramai_rak_redup", "S05_ramai_redup")
    if 6849 <= img_num <= 6852: return ("kristoff", "ramai", "ramai_rak_redup", "S05_ramai_redup")
    if 6853 <= img_num <= 6856: return ("olaf", "ramai", "ramai_rak_redup", "S05_ramai_redup")
    if 6857 <= img_num <= 6860: return ("sven", "ramai", "ramai_rak_redup", "S05_ramai_redup")

    # Sesi 6: Polos terang (batch 3)
    if 6861 <= img_num <= 6864: return ("anna", "polos", "polos_terang", "S06_polos_terang")
    if 6865 <= img_num <= 6868: return ("elsa", "polos", "polos_terang", "S06_polos_terang")
    if 6869 <= img_num <= 6872: return ("kristoff", "polos", "polos_terang", "S06_polos_terang")
    if 6873 <= img_num <= 6876: return ("sven", "polos", "polos_terang", "S06_polos_terang")
    if 6877 <= img_num <= 6880: return ("olaf", "polos", "polos_terang", "S06_polos_terang")

    # Sesi 7: Polos redup / lampu hangat (batch 2)
    if 6881 <= img_num <= 6884: return ("olaf", "polos", "polos_redup", "S07_polos_redup")
    if 6885 <= img_num <= 6888: return ("sven", "polos", "polos_redup", "S07_polos_redup")
    if 6889 <= img_num <= 6893: return ("elsa", "polos", "polos_redup", "S07_polos_redup")
    if 6894 <= img_num <= 6897: return ("kristoff", "polos", "polos_redup", "S07_polos_redup")
    if 6898 <= img_num <= 6901: return ("anna", "polos", "polos_redup", "S07_polos_redup")

    raise ValueError(f"Nomor file belum terpetakan: IMG_{img_num}.HEIC")


def main() -> None:
    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"Arsip dataset tidak ditemukan: {ZIP_PATH}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    counters: dict[tuple[str, str], int] = defaultdict(int)
    records = []
    total_bytes = 0

    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        infos = sorted(
            [i for i in zf.infolist() if not i.is_dir() and i.filename.lower().endswith(".heic")],
            key=lambda x: x.filename,
        )

        for info in infos:
            orig_name = Path(info.filename).name
            m = re.search(r"(\d+)", orig_name)
            if not m:
                raise ValueError(f"Tidak dapat membaca nomor gambar dari {orig_name}")
            img_num = int(m.group(1))
            kelas, kondisi, sub_kondisi, sesi_foto = classify_frozen_v1(img_num)

            counters[(kelas, kondisi)] += 1
            idx = counters[(kelas, kondisi)]
            rel_path = Path(kelas) / kondisi / f"{kelas}_{kondisi}_{idx:02d}.jpg"
            out_path = OUT_DIR / rel_path
            out_path.parent.mkdir(parents=True, exist_ok=True)

            raw = zf.read(info.filename)
            with Image.open(io.BytesIO(raw)) as im:
                exif = im.getexif()
                dt_str = ""
                try:
                    dt_str = str(exif.get_ifd(0x8769).get(36867, "")).strip()
                except Exception:
                    pass
                if not dt_str and exif:
                    dt_str = str(exif.get(306, "")).strip()

                im_fixed = ImageOps.exif_transpose(im).convert("RGB")
                orig_w, orig_h = im_fixed.size

                # Resize proportionally so max side <= MAX_SIDE (preserving exact 3:4 aspect ratio)
                im_resized = im_fixed.copy()
                im_resized.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
                w, h = im_resized.size
                im_resized.save(out_path, format="JPEG", quality=JPEG_QUALITY, optimize=True)

            jpg_bytes = out_path.read_bytes()
            total_bytes += len(jpg_bytes)
            sha256 = hashlib.sha256(jpg_bytes).hexdigest()

            # Compute EDA metrics directly on the saved JPEG (same as notebook will read)
            arr = np.array(Image.open(out_path).convert("RGB"))
            gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            edge_density = float(np.count_nonzero(edges)) / float(edges.size)

            # Relative capture sequence index (no calendar dates exposed in summaries)
            ts_iso = ""
            if dt_str:
                try:
                    ts_iso = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S").isoformat()
                except Exception:
                    ts_iso = dt_str

            records.append(
                {
                    "file": rel_path.as_posix(),
                    "orig_file": orig_name,
                    "kelas": kelas,
                    "kondisi": kondisi,
                    "sub_kondisi": sub_kondisi,
                    "sesi_foto": sesi_foto,
                    "capture_ts": ts_iso,
                    "orig_w": orig_w,
                    "orig_h": orig_h,
                    "w": w,
                    "h": h,
                    "file_kb": round(len(jpg_bytes) / 1024.0, 2),
                    "brightness": round(float(gray.mean()), 2),
                    "contrast": round(float(gray.std()), 2),
                    "edge_density": round(edge_density, 4),
                    "sha256": sha256,
                }
            )

    df = pd.DataFrame(records)
    meta_csv = OUT_DIR / "metadata.csv"
    df.to_csv(meta_csv, index=False)

    # Build real summary JSON for slides/notebooks
    by_class = {k: int(v) for k, v in df["kelas"].value_counts().sort_index().items()}
    by_cond = {}
    for cond, grp in df.groupby("kondisi"):
        by_cond[cond] = {
            "count": int(len(grp)),
            "mean_brightness": round(float(grp["brightness"].mean()), 2),
            "std_brightness": round(float(grp["brightness"].std()), 2),
            "mean_contrast": round(float(grp["contrast"].mean()), 2),
            "mean_edge_density": round(float(grp["edge_density"].mean()), 4),
        }

    ct = pd.crosstab(df["kelas"], df["kondisi"])
    class_x_cond = {
        kls: {c: int(ct.loc[kls, c]) for c in CONDITIONS}
        for kls in CLASS_NAMES
    }

    summary = {
        "dataset_name": "Disney Frozen Figurine Dataset (v1)",
        "total_images": int(len(df)),
        "classes": CLASS_NAMES,
        "conditions": CONDITIONS,
        "sessions_count": int(df["sesi_foto"].nunique()),
        "image_size_jpeg": f"{int(df['w'].median())}x{int(df['h'].median())}",
        "total_size_mb": round(total_bytes / (1024 * 1024), 2),
        "by_class": by_class,
        "by_condition": by_cond,
        "class_x_condition": class_x_cond,
    }
    summary_json = OUT_DIR / "dataset_summary.json"
    summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # Quick integrity check on all generated JPEGs with standard Pillow + OpenCV
    for rel in df["file"]:
        fp = OUT_DIR / rel
        with Image.open(fp) as im:
            im.verify()

    print(f"✅ Dataset Frozen v1 siap di: {OUT_DIR}")
    print(f"   Total foto valid : {len(df)} JPEG ({summary['total_size_mb']:.2f} MB)")
    print(f"   Resolusi JPEG    : {summary['image_size_jpeg']} (portrait 3:4)")
    print(f"   Per kelas        : {by_class}")
    print(f"   Polos vs Ramai   : {by_cond}")


if __name__ == "__main__":
    main()
