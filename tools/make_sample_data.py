"""Generate deterministic synthetic sample dataset in data/sample/.

Dataset specification:
- 5 geometric classes: lingkaran, persegi, segitiga, bintang, heksagon
- 2 conditions per class: polos, ramai
- 12 images per (kelas, kondisi) = 120 image files total (256x256)
- Special cases embedded in the 120 files:
  * 2 exact duplicate images (same SHA-256 bytes)
  * 1 corrupted image file (invalid JPEG bytes)
  * 2 images with EXIF Orientation tag = 6
- Metadata saved to data/sample/metadata.csv with columns:
  file, kelas, kondisi, id_sesi, catatan
"""

from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SEED = 42
IMG_SIZE = 256
CLASSES = ["lingkaran", "persegi", "segitiga", "bintang", "heksagon"]
CONDITIONS = ["polos", "ramai"]
IMAGES_PER_COMBO = 12

ROOT_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = ROOT_DIR / "data" / "sample"

# Google I/O-inspired vibrant colors for foreground shapes
CLASS_COLORS = {
    "lingkaran": (66, 133, 244),   # Blue
    "persegi": (234, 67, 53),      # Red
    "segitiga": (251, 188, 4),     # Yellow
    "bintang": (52, 168, 83),      # Green
    "heksagon": (142, 68, 173),    # Purple
}

POLOS_BGS = [
    (245, 247, 250),
    (238, 242, 247),
    (250, 248, 242),
    (240, 246, 242),
]


def _regular_polygon_points(cx: float, cy: float, r: float, sides: int, angle_deg: float = -90) -> list[tuple[float, float]]:
    pts = []
    for i in range(sides):
        ang = math.radians(angle_deg + i * (360.0 / sides))
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def _star_points(cx: float, cy: float, r_outer: float, r_inner: float, spikes: int = 5, angle_deg: float = -90) -> list[tuple[float, float]]:
    pts = []
    for i in range(spikes * 2):
        r = r_outer if i % 2 == 0 else r_inner
        ang = math.radians(angle_deg + i * (180.0 / spikes))
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def _draw_main_shape(draw: ImageDraw.ImageDraw, kelas: str, cx: float, cy: float, size: float, color: tuple[int, int, int], angle: float) -> None:
    outline = (32, 33, 36)
    if kelas == "lingkaran":
        draw.ellipse([cx - size, cy - size, cx + size, cy + size], fill=color, outline=outline, width=4)
        # Inner highlight ring so rotation/EXIF is visible
        draw.arc([cx - size * 0.65, cy - size * 0.65, cx + size * 0.65, cy + size * 0.65], start=200, end=330, fill=(255, 255, 255), width=5)
    elif kelas == "persegi":
        pts = _regular_polygon_points(cx, cy, size * 1.15, 4, angle_deg=45 + angle)
        draw.polygon(pts, fill=color, outline=outline, width=4)
        # Small top marker so EXIF rotation is visually obvious
        draw.rectangle([cx - 10, cy - size * 0.5, cx + 10, cy - size * 0.25], fill=(255, 255, 255))
    elif kelas == "segitiga":
        pts = _regular_polygon_points(cx, cy, size * 1.15, 3, angle_deg=-90 + angle)
        draw.polygon(pts, fill=color, outline=outline, width=4)
    elif kelas == "bintang":
        pts = _star_points(cx, cy, size * 1.2, size * 0.52, spikes=5, angle_deg=-90 + angle)
        draw.polygon(pts, fill=color, outline=outline, width=4)
    elif kelas == "heksagon":
        pts = _regular_polygon_points(cx, cy, size * 1.1, 6, angle_deg=0 + angle)
        draw.polygon(pts, fill=color, outline=outline, width=4)


def _generate_image(rng: np.random.Generator, kelas: str, kondisi: str) -> Image.Image:
    if kondisi == "polos":
        bg_base = np.array(POLOS_BGS[int(rng.integers(0, len(POLOS_BGS)))], dtype=np.float32)
        bg = np.clip(bg_base + rng.normal(0, 3.0, (IMG_SIZE, IMG_SIZE, 3)), 0, 255).astype(np.uint8)
        img = Image.fromarray(bg, mode="RGB")
        draw = ImageDraw.Draw(img)
    else:
        # Ramai: textured gradient + noise + distractor lines & shapes
        x = np.linspace(0, 1, IMG_SIZE, dtype=np.float32)
        y = np.linspace(0, 1, IMG_SIZE, dtype=np.float32)
        xx, yy = np.meshgrid(x, y)
        c1 = rng.integers(60, 200, size=3).astype(np.float32)
        c2 = rng.integers(60, 200, size=3).astype(np.float32)
        grad = c1[None, None, :] * (1 - xx[:, :, None]) + c2[None, None, :] * yy[:, :, None]
        noise = rng.normal(0, 22.0, (IMG_SIZE, IMG_SIZE, 3))
        bg = np.clip(grad + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(bg, mode="RGB")
        draw = ImageDraw.Draw(img)

        # Distractor lines
        for _ in range(int(rng.integers(10, 18))):
            p1 = (int(rng.integers(0, IMG_SIZE)), int(rng.integers(0, IMG_SIZE)))
            p2 = (int(rng.integers(0, IMG_SIZE)), int(rng.integers(0, IMG_SIZE)))
            col = tuple(int(v) for v in rng.integers(40, 230, size=3))
            draw.line([p1, p2], fill=col, width=int(rng.integers(2, 5)))

        # Distractor geometric objects
        for _ in range(int(rng.integers(8, 15))):
            dx = int(rng.integers(10, IMG_SIZE - 10))
            dy = int(rng.integers(10, IMG_SIZE - 10))
            dr = int(rng.integers(8, 26))
            col = tuple(int(v) for v in rng.integers(30, 240, size=3))
            kind = int(rng.integers(0, 3))
            if kind == 0:
                draw.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=col, outline=(30, 30, 30), width=1)
            elif kind == 1:
                draw.rectangle([dx - dr, dy - dr, dx + dr, dy + dr], fill=col, outline=(30, 30, 30), width=1)
            else:
                pts = _regular_polygon_points(dx, dy, dr, 3, angle_deg=float(rng.uniform(0, 360)))
                draw.polygon(pts, fill=col, outline=(30, 30, 30), width=1)

    # Foreground target shape
    base_col = np.array(CLASS_COLORS[kelas], dtype=np.int32)
    jitter = rng.integers(-18, 19, size=3)
    fg_col = tuple(int(np.clip(c, 20, 245)) for c in (base_col + jitter))

    cx = IMG_SIZE / 2 + float(rng.uniform(-16, 16))
    cy = IMG_SIZE / 2 + float(rng.uniform(-16, 16))
    size = float(rng.uniform(48, 64))
    angle = float(rng.uniform(-15, 15))
    _draw_main_shape(draw, kelas, cx, cy, size, fg_col, angle)

    if kondisi == "ramai" and rng.random() < 0.35:
        img = img.filter(ImageFilter.GaussianBlur(radius=0.6))

    return img


def build_sample_dataset() -> dict:
    """Create the 120-file synthetic dataset and metadata.csv."""
    if SAMPLE_DIR.exists():
        shutil.rmtree(SAMPLE_DIR)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(SEED)
    rows: list[dict[str, str]] = []

    duplicate_source_path: Path | None = None

    for kelas in CLASSES:
        for kondisi in CONDITIONS:
            target_dir = SAMPLE_DIR / kelas / kondisi
            target_dir.mkdir(parents=True, exist_ok=True)

            for idx in range(1, IMAGES_PER_COMBO + 1):
                fname = f"{kelas}_{kondisi}_{idx:02d}.jpg"
                fpath = target_dir / fname
                rel_path = f"{kelas}/{kondisi}/{fname}"
                id_sesi = f"sesi_{(idx - 1) // 4 + 1:02d}"
                catatan = "normal"

                # Special case 1: exact duplicate pair (lingkaran/polos 01 & 02)
                if kelas == "lingkaran" and kondisi == "polos" and idx == 1:
                    img = _generate_image(rng, kelas, kondisi)
                    img.save(fpath, format="JPEG", quality=92)
                    duplicate_source_path = fpath
                    catatan = "duplikat_sumber"
                elif kelas == "lingkaran" and kondisi == "polos" and idx == 2:
                    assert duplicate_source_path is not None
                    shutil.copyfile(duplicate_source_path, fpath)
                    catatan = "duplikat_identik"

                # Special case 2: 1 corrupted file (segitiga/ramai 12)
                elif kelas == "segitiga" and kondisi == "ramai" and idx == 12:
                    fpath.write_bytes(b"\xff\xd8\xff\xe0CORRUPTED_TRUNCATED_IMAGE_DATA_P04")
                    catatan = "rusak"

                # Special case 3: 2 images with EXIF orientation = 6
                elif (kelas == "persegi" and kondisi == "polos" and idx == 1) or (
                    kelas == "bintang" and kondisi == "ramai" and idx == 1
                ):
                    img = _generate_image(rng, kelas, kondisi)
                    # Rotate 90 deg CCW when saving raw pixels so Orientation=6 restores it
                    rotated_raw = img.rotate(90, expand=True)
                    exif = rotated_raw.getexif()
                    exif[274] = 6  # 274 = Orientation, 6 = Rotate 90 CW
                    rotated_raw.save(fpath, format="JPEG", quality=92, exif=exif.tobytes())
                    catatan = "exif_orientation_6"

                else:
                    img = _generate_image(rng, kelas, kondisi)
                    img.save(fpath, format="JPEG", quality=92)

                rows.append(
                    {
                        "file": rel_path,
                        "kelas": kelas,
                        "kondisi": kondisi,
                        "id_sesi": id_sesi,
                        "catatan": catatan,
                    }
                )

    metadata_path = SAMPLE_DIR / "metadata.csv"
    with metadata_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "kelas", "kondisi", "id_sesi", "catatan"])
        writer.writeheader()
        writer.writerows(rows)

    return {
        "total_files": len(rows),
        "classes": len(CLASSES),
        "conditions": len(CONDITIONS),
        "metadata_path": str(metadata_path),
    }


if __name__ == "__main__":
    summary = build_sample_dataset()
    print(f"Dataset sintetis selesai dibuat: {summary}")

