"""Generate deterministic synthetic sample dataset in data/sample/ and MNIST dataset in data/mnist/.

Dataset specification:
1. data/sample/:
   - 5 geometric classes: lingkaran, persegi, segitiga, bintang, heksagon
   - 2 conditions per class: polos, ramai
   - 12 images per (kelas, kondisi) = 120 image files total (256x256)
   - Special cases embedded in the 120 files:
     * 2 exact duplicate images (same SHA-256 bytes)
     * 1 corrupted image file (invalid JPEG bytes)
     * 2 images with EXIF Orientation tag = 6
   - Metadata saved to data/sample/metadata.csv
2. data/mnist/:
   - Full archive data/mnist/mnist.npz (when available) + data/mnist/mnist_samples.json
   - 10 digit folders (data/mnist/0/ .. data/mnist/9/) with real 28x28 grayscale PNG images
   - data/mnist/variants/ with pairs of different handwriting styles (7_a, 7_b, 5_a, 5_b)
   - Metadata saved to data/mnist/metadata.csv
"""

from __future__ import annotations

import ast
import csv
import json
import math
import shutil
import struct
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SEED = 42
IMG_SIZE = 256
CLASSES = ["lingkaran", "persegi", "segitiga", "bintang", "heksagon"]
CONDITIONS = ["polos", "ramai"]
IMAGES_PER_COMBO = 12

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SAMPLE_DIR = ROOT_DIR / "data" / "sample"
MNIST_DIR = ROOT_DIR / "data" / "mnist"
ASSETS_MNIST_JSON = ROOT_DIR / "materials" / "P01" / "assets" / "P01" / "mnist_samples.json"

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


def _read_npy_slice(raw_file, max_items: int):
    magic = raw_file.read(6)
    assert magic[:6] == b"\x93NUMPY"
    major, _ = struct.unpack("<BB", raw_file.read(2))
    hlen = struct.unpack("<H" if major == 1 else "<I", raw_file.read(2 if major == 1 else 4))[0]
    meta = ast.literal_eval(raw_file.read(hlen).decode("latin1"))
    shape = meta["shape"]
    if len(shape) == 1:
        return list(raw_file.read(max_items))
    h, w = shape[1], shape[2]
    data = raw_file.read(max_items * h * w)
    imgs = []
    for idx in range(max_items):
        start = idx * h * w
        imgs.append(np.frombuffer(data[start : start + h * w], dtype=np.uint8).reshape(h, w))
    return imgs


def build_mnist_dataset() -> dict:
    """Create data/mnist/ with organized 28x28 PNG images (0-9), variants, mnist_samples.json, and metadata.csv."""
    MNIST_DIR.mkdir(parents=True, exist_ok=True)
    npz_path = MNIST_DIR / "mnist.npz"

    # Copy mnist_samples.json to data/mnist/ if available in assets
    if ASSETS_MNIST_JSON.exists():
        shutil.copyfile(ASSETS_MNIST_JSON, MNIST_DIR / "mnist_samples.json")

    rows: list[dict[str, str | int]] = []
    per_digit_target = 10

    if npz_path.exists():
        with zipfile.ZipFile(npz_path, "r") as zf:
            with zf.open("y_train.npy") as fy:
                y_sub = _read_npy_slice(fy, 500)
            with zf.open("x_train.npy") as fx:
                x_sub = _read_npy_slice(fx, 500)

        counts = {d: 0 for d in range(10)}
        # Ensure index 1 of each digit (the iconic sample in mnist_samples.json) is saved as _01.png
        by_digit: dict[int, list[tuple[int, np.ndarray]]] = {d: [] for d in range(10)}
        for idx, (lbl, arr) in enumerate(zip(y_sub, x_sub)):
            by_digit[int(lbl)].append((idx, arr))

        for d in range(10):
            d_dir = MNIST_DIR / str(d)
            d_dir.mkdir(parents=True, exist_ok=True)
            candidates = by_digit[d]
            # Put the 2nd sample first so mnist_{d}_01.png matches the iconic digit in mnist_samples.json
            if len(candidates) > 1:
                ordered = [candidates[1], candidates[0]] + candidates[2:]
            else:
                ordered = candidates
            for rank, (orig_idx, arr) in enumerate(ordered[:per_digit_target], start=1):
                fname = f"mnist_{d}_{rank:02d}.png"
                fpath = d_dir / fname
                Image.fromarray(arr, mode="L").save(fpath)
                counts[d] += 1
                rows.append({
                    "file": f"{d}/{fname}",
                    "digit": d,
                    "kategori": "standar",
                    "mnist_train_index": orig_idx,
                })

    # Also save the iconic digits and handwriting variants from mnist_samples.json
    sample_json_path = MNIST_DIR / "mnist_samples.json"
    if sample_json_path.exists():
        mdata = json.loads(sample_json_path.read_text(encoding="utf-8"))
        # If mnist.npz wasn't present, at least save 1 PNG per digit from mnist_samples.json
        if not rows:
            for d_str, mat in mdata["digits"].items():
                d_dir = MNIST_DIR / d_str
                d_dir.mkdir(parents=True, exist_ok=True)
                fname = f"mnist_{d_str}_01.png"
                arr = np.array(mat, dtype=np.uint8)
                Image.fromarray(arr, mode="L").save(d_dir / fname)
                rows.append({
                    "file": f"{d_str}/{fname}",
                    "digit": int(d_str),
                    "kategori": "standar",
                    "mnist_train_index": mdata.get("digit_indices", {}).get(d_str, -1),
                })

        var_dir = MNIST_DIR / "variants"
        var_dir.mkdir(parents=True, exist_ok=True)
        var_map = {
            "7_a": ("mnist_7_penulis_a.png", 7),
            "7_b": ("mnist_7_penulis_b.png", 7),
            "5_a": ("mnist_5_penulis_a.png", 5),
            "5_b": ("mnist_5_penulis_b.png", 5),
        }
        for key, (vname, d_num) in var_map.items():
            if key in mdata.get("variants", {}):
                vinfo = mdata["variants"][key]
                arr = np.array(vinfo["pixels"], dtype=np.uint8)
                Image.fromarray(arr, mode="L").save(var_dir / vname)
                rows.append({
                    "file": f"variants/{vname}",
                    "digit": d_num,
                    "kategori": f"variasi_{key}",
                    "mnist_train_index": vinfo.get("index", -1),
                })

    meta_csv = MNIST_DIR / "metadata.csv"
    with meta_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "digit", "kategori", "mnist_train_index"])
        writer.writeheader()
        writer.writerows(rows)

    return {
        "mnist_dir": str(MNIST_DIR),
        "total_png_files": len(rows),
        "has_full_npz": npz_path.exists(),
        "metadata_path": str(meta_csv),
    }


if __name__ == "__main__":
    summary = build_sample_dataset()
    print(f"Dataset sintetis selesai dibuat: {summary}")
    mnist_summary = build_mnist_dataset()
    print(f"Dataset MNIST selesai dibuat   : {mnist_summary}")

