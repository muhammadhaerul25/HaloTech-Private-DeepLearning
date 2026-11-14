"""Generator notebook peserta dan kunci jawaban untuk Pertemuan P04: Image Processing & EDA."""

from pathlib import Path
import nbformat as nbf


ROOT = Path(__file__).resolve().parent.parent
NB_STUDENT = ROOT / "notebooks" / "P04_image_processing_eda.ipynb"
NB_SOLUTION = ROOT / "notebooks" / "solutions" / "P04_image_processing_eda.ipynb"


def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text: str):
    return nbf.v4.new_code_cell(text.strip())


def build_cells(is_solution: bool) -> list:
    cells = []

    # 1. Judul + Tujuan + Estimasi Waktu
    cells.append(
        md(
            """
# Image Processing & Exploratory Data Analysis (EDA) Foto Sendiri

**Durasi Hands-on:** ±50 menit (6 bagian terpandu + 1 bagian Opsional)  
**Tujuan Pembelajaran:**
1. Memahami gambar digital sebagai array angka `(tinggi, lebar, channel)`.
2. Melakukan *preprocessing* dasar: cek tipe data `uint8` → `float32`, normalisasi, dan koreksi *EXIF orientation*.
3. Melakukan audit kebersihan dataset: mendeteksi *corrupted file* dan *duplicate images* dengan `SHA-256`.
4. Menghitung dan membandingkan statistik **polos vs ramai** (`Brightness`, `Contrast`, dan `Edge Density`).

> **Catatan:** Jalankan setiap sel berurutan dari atas ke bawah. Pada versi peserta, lengkapi bagian bertanda `# TODO` sebelum menjalankan sel `assert` di bawahnya.
"""
        )
    )

    # 2. Setup
    cells.append(
        md(
            """
## Setup & Konfigurasi Lingkungan (Colab / Lokal)

Sel di bawah otomatis mendeteksi apakah notebook dijalankan di Google Colab atau lokal, mengunci `SEED = 42` agar hasil *reproducible*, serta menyiapkan variabel konfigurasi dataset.
"""
        )
    )

    cells.append(
        code(
            """
import os
import random
import hashlib
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

try:
    import google.colab  # noqa: F401
    from google.colab import drive
    drive.mount('/content/drive')
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# Variabel konfigurasi (ubah sesuai dataset Anda nanti)
IMG_SIZE = 224
SMOKE_TEST = os.environ.get("SMOKE_TEST", "0") == "1"

BASE_DIR = next((p for p in (Path("."), Path(".."), Path("../..")) if (p / "data").exists()), Path("."))
if not SMOKE_TEST and (BASE_DIR / "data" / "raw").exists() and any((BASE_DIR / "data" / "raw").iterdir()):
    DATA_DIR = BASE_DIR / "data" / "raw"
    CLASS_NAMES = sorted([p.name for p in DATA_DIR.iterdir() if p.is_dir()])
else:
    DATA_DIR = BASE_DIR / "data" / "sample"
    CLASS_NAMES = ["lingkaran", "persegi", "segitiga", "bintang", "heksagon"]

RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"IN_COLAB   : {IN_COLAB}")
print(f"SMOKE_TEST : {SMOKE_TEST}")
print(f"DATA_DIR   : {DATA_DIR.resolve()}")
print(f"CLASS_NAMES: {CLASS_NAMES}")
print(f"Versi      : numpy={np.__version__}, cv2={cv2.__version__}, pandas={pd.__version__}")
"""
        )
    )

    # Bagian 1: Load foto, shape, uint8 -> float32, normalisasi (8 menit)
    cells.append(
        md(
            """
---
## Bagian 1 (8 menit): Membaca Gambar sebagai Array Angka & Normalisasi

Komputer membaca gambar sebagai matriks angka bertipe `uint8` (`0–255`). Sebelum masuk ke model AI, kita perlu:
1. Memastikan gambar berada pada format warna `RGB` dan ukuran seragam `IMG_SIZE × IMG_SIZE`.
2. Mengubah tipe data menjadi `float32` lalu melakukan **normalisasi** ke skala `0.0–1.0` (dibagi `255.0`).
"""
        )
    )

    cells.append(
        code(
            """
sample_img_path = sorted(DATA_DIR.rglob("*.jpg"))[0]
img_pil = Image.open(sample_img_path).convert("RGB")
img_resized = img_pil.resize((IMG_SIZE, IMG_SIZE))
arr_u8 = np.array(img_resized)

print("File contoh :", sample_img_path.name)
print("Shape       :", arr_u8.shape)
print("Dtype awal  :", arr_u8.dtype)
print("Min / Max   :", arr_u8.min(), "/", arr_u8.max())
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
# Konversi uint8 -> float32 dan normalisasi ke rentang [0.0, 1.0]
arr_norm = arr_u8.astype(np.float32) / 255.0

print("Dtype baru  :", arr_norm.dtype)
print("Min / Max   :", round(float(arr_norm.min()), 4), "/", round(float(arr_norm.max()), 4))

assert arr_norm.shape == (IMG_SIZE, IMG_SIZE, 3), "Shape harus (224, 224, 3)"
assert arr_norm.dtype == np.float32, "Dtype harus float32"
assert 0.0 <= arr_norm.min() and arr_norm.max() <= 1.0, "Nilai harus berada di [0.0, 1.0]"
print("Cek Bagian 1 lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
# TODO: Ubah arr_u8 ke tipe float32 lalu bagi dengan 255.0 agar rentangnya [0.0, 1.0]
# Petunjuk: gunakan .astype(np.float32) / 255.0
arr_norm = None  # TODO: ganti None dengan ekspresi yang benar

assert arr_norm is not None, "arr_norm belum diisi!"
assert arr_norm.shape == (IMG_SIZE, IMG_SIZE, 3), "Shape harus (224, 224, 3)"
assert arr_norm.dtype == np.float32, "Dtype harus float32"
assert 0.0 <= arr_norm.min() and arr_norm.max() <= 1.0, "Nilai harus berada di [0.0, 1.0]"
print("Cek Bagian 1 lolos!")
"""
            )
        )

    # Bagian 2: Koreksi EXIF orientation (7 menit)
    cells.append(
        md(
            """
---
## Bagian 2 (7 menit): Memperbaiki Rotasi Tersembunyi (*EXIF Orientation*)

Kamera HP sering menyimpan foto dalam posisi miring/tertidur dan hanya menempelkan catatan rotasi di metadata **EXIF**. Jika program langsung membaca pikselnya tanpa `ImageOps.exif_transpose()`, foto bisa terputar!
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
def load_image_exif_safe(path: Path) -> Image.Image:
    \"\"\"Membuka gambar dan menerapkan koreksi orientasi EXIF secara otomatis.\"\"\"
    with Image.open(path) as im:
        im_fixed = ImageOps.exif_transpose(im)
        return im_fixed.convert("RGB")

exif_count = 0
for p in sorted(DATA_DIR.rglob("*.jpg")):
    try:
        with Image.open(p) as im:
            orient = im.getexif().get(274, 1)  # 274 = tag Orientation
            if orient != 1:
                exif_count += 1
                fixed = load_image_exif_safe(p)
                assert fixed.mode == "RGB"
    except Exception:
        pass

print(f"Jumlah file dengan EXIF Orientation != 1: {exif_count}")
assert exif_count >= 0
print("Cek Bagian 2 lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
def load_image_exif_safe(path: Path) -> Image.Image:
    \"\"\"Membuka gambar dan menerapkan koreksi orientasi EXIF secara otomatis.\"\"\"
    with Image.open(path) as im:
        # TODO: perbaiki orientasi EXIF menggunakan ImageOps.exif_transpose(im)
        im_fixed = None  # TODO: isi dengan ImageOps.exif_transpose(im)
        return im_fixed.convert("RGB")

# Uji fungsi pada 1 foto contoh
test_fixed = load_image_exif_safe(sample_img_path)
assert test_fixed.mode == "RGB"
print("Cek Bagian 2 lolos!")
"""
            )
        )

    # Bagian 3 & 4: Inventaris, deteksi file rusak & duplikat SHA-256 (18 menit)
    cells.append(
        md(
            """
---
## Bagian 3 & 4 (18 menit): Inventaris Dataset, Cek *Corrupted File*, dan *Duplicate Images*

Sebelum menghitung statistik atau melatih model, kita wajib menyaring:
1. **Corrupted File:** File yang gagal dibuka atau gagal melewati `Image.verify()`.
2. **Duplicate Images:** File identik yang memiliki *file hash* (`SHA-256`) sama persis (berisiko menyebabkan *data leakage* jika tersebar ke *train* dan *test*).
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
def get_file_hash(path: Path, chunk_size: int = 8192) -> str:
    \"\"\"Menghitung hash SHA-256 dari sebuah file gambar.\"\"\"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

all_files = sorted(DATA_DIR.rglob("*.jpg"))
seen_hashes = {}
records = []
corrupted_files = []
duplicate_files = []

for p in all_files:
    # 1. Cek integritas file
    try:
        with Image.open(p) as im:
            im.verify()
    except Exception:
        corrupted_files.append(str(p))
        continue

    # 2. Cek duplikat dengan SHA-256
    fhash = get_file_hash(p)
    if fhash in seen_hashes:
        duplicate_files.append((str(p), seen_hashes[fhash]))
        continue
    seen_hashes[fhash] = str(p)

    # 3. Catat metadata kelas & kondisi (polos / ramai)
    parts = p.relative_to(DATA_DIR).parts
    cls_name = parts[0] if len(parts) >= 2 else "unknown"
    cond_name = parts[1] if len(parts) >= 3 else "unknown"
    with load_image_exif_safe(p) as im:
        w, h = im.size
    records.append({
        "path": str(p),
        "class": cls_name,
        "condition": cond_name,
        "width": w,
        "height": h,
        "size_kb": round(p.stat().st_size / 1024, 2),
        "sha256": fhash,
    })

df_clean = pd.DataFrame(records)
print(f"Total file ditemukan : {len(all_files)}")
print(f"File rusak (dibuang) : {len(corrupted_files)}")
print(f"File duplikat        : {len(duplicate_files)}")
print(f"File valid & unik    : {len(df_clean)}")

assert len(df_clean) > 0, "Tidak ada file valid!"
assert df_clean["sha256"].is_unique, "Masih ada hash duplikat!"
print("Cek Bagian 3 & 4 lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
def get_file_hash(path: Path, chunk_size: int = 8192) -> str:
    \"\"\"Menghitung hash SHA-256 dari sebuah file gambar.\"\"\"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            # TODO: perbarui objek hash h dengan chunk menggunakan h.update(chunk)
            pass
    return h.hexdigest()

all_files = sorted(DATA_DIR.rglob("*.jpg"))
seen_hashes = {}
records = []
corrupted_files = []
duplicate_files = []

for p in all_files:
    try:
        with Image.open(p) as im:
            im.verify()
    except Exception:
        corrupted_files.append(str(p))
        continue

    fhash = get_file_hash(p)
    if fhash in seen_hashes:
        duplicate_files.append((str(p), seen_hashes[fhash]))
        continue
    seen_hashes[fhash] = str(p)

    parts = p.relative_to(DATA_DIR).parts
    cls_name = parts[0] if len(parts) >= 2 else "unknown"
    cond_name = parts[1] if len(parts) >= 3 else "unknown"
    with load_image_exif_safe(p) as im:
        w, h = im.size
    records.append({
        "path": str(p),
        "class": cls_name,
        "condition": cond_name,
        "width": w,
        "height": h,
        "size_kb": round(p.stat().st_size / 1024, 2),
        "sha256": fhash,
    })

df_clean = pd.DataFrame(records)
print(f"File valid & unik: {len(df_clean)} | Rusak: {len(corrupted_files)} | Duplikat: {len(duplicate_files)}")
assert df_clean["sha256"].is_unique, "Hash harus unik! Cek kembali fungsi get_file_hash."
print("Cek Bagian 3 & 4 lolos!")
"""
            )
        )

    # Bagian 5: Brightness, Contrast, Edge Density (10 menit)
    cells.append(
        md(
            """
---
## Bagian 5 (10 menit): Menghitung *Brightness*, *Contrast*, dan *Edge Density*

Untuk mengukur perbedaan kondisi foto **polos** vs **ramai** secara objektif, kita hitung tiga metrik pada versi *grayscale*:
- **Brightness:** Rata-rata nilai intensitas (`0–255`).
- **Contrast:** Simpangan baku (*standard deviation*) intensitas.
- **Edge Density:** Proporsi piksel tepi hasil deteksi **Canny** (`cv2.Canny(gray, 100, 200)`).
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
def compute_image_metrics(path: Path) -> dict:
    \"\"\"Menghitung brightness, contrast, dan Canny edge density pada foto.\"\"\"
    im = load_image_exif_safe(path).resize((IMG_SIZE, IMG_SIZE))
    gray = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    brightness = float(np.mean(gray))
    contrast = float(np.std(gray))
    edges = cv2.Canny(gray, 100, 200)
    edge_density = float(np.mean(edges > 0))
    return {
        "brightness": brightness,
        "contrast": contrast,
        "edge_density": edge_density,
    }

metrics_df = pd.DataFrame([compute_image_metrics(Path(p)) for p in df_clean["path"]])
df_eda = pd.concat([df_clean.reset_index(drop=True), metrics_df], axis=1)

assert {"brightness", "contrast", "edge_density"}.issubset(df_eda.columns)
assert df_eda["edge_density"].between(0.0, 1.0).all()
display_cols = ["class", "condition", "brightness", "contrast", "edge_density"]
print(df_eda[display_cols].head())
print("Cek Bagian 5 lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
def compute_image_metrics(path: Path) -> dict:
    \"\"\"Menghitung brightness, contrast, dan Canny edge density pada foto.\"\"\"
    im = load_image_exif_safe(path).resize((IMG_SIZE, IMG_SIZE))
    gray = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    # TODO: hitung brightness (np.mean), contrast (np.std), dan edge_density (Canny)
    brightness = None  # TODO: float(np.mean(gray))
    contrast = None    # TODO: float(np.std(gray))
    edges = cv2.Canny(gray, 100, 200)
    edge_density = None  # TODO: float(np.mean(edges > 0))
    return {
        "brightness": brightness,
        "contrast": contrast,
        "edge_density": edge_density,
    }

metrics_df = pd.DataFrame([compute_image_metrics(Path(p)) for p in df_clean["path"]])
df_eda = pd.concat([df_clean.reset_index(drop=True), metrics_df], axis=1)

assert df_eda["brightness"].notna().all(), "brightness belum dihitung!"
assert df_eda["edge_density"].between(0.0, 1.0).all(), "edge_density harus di antara 0 dan 1!"
print("Cek Bagian 5 lolos!")
"""
            )
        )

    # Bagian 6: Tabel perbandingan polos vs ramai & Boxplot (7 menit)
    cells.append(
        md(
            """
---
## Bagian 6 (7 menit): Ringkasan Statistik *Polos vs Ramai* & Visualisasi Boxplot

Mari kita bandingkan rata-rata statistik antara foto kondisi `polos` dan `ramai`, lalu simpan grafik perbandingannya ke folder `results/`.
"""
        )
    )

    cells.append(
        code(
            """
summary = (
    df_eda.groupby("condition")[["brightness", "contrast", "edge_density"]]
    .agg(["count", "mean", "std"])
    .round(4)
)
print(summary)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
df_eda.boxplot(column="brightness", by="condition", ax=axes[0])
axes[0].set_title("Brightness: Polos vs Ramai (Contoh data sampel)")
axes[0].set_ylabel("Mean Intensity (0-255)")

df_eda.boxplot(column="edge_density", by="condition", ax=axes[1])
axes[1].set_title("Edge Density: Polos vs Ramai (Contoh data sampel)")
axes[1].set_ylabel("Proporsi Piksel Tepi (0-1)")

plt.suptitle("")
plt.tight_layout()
out_plot = RESULTS_DIR / "p04_eda_polos_vs_ramai.png"
plt.savefig(out_plot, dpi=150)
plt.show()
print("Grafik disimpan ke:", out_plot)
"""
        )
    )

    # Opsional
    cells.append(
        md(
            """
---
## Bagian Opsional: Menjaga *Aspect Ratio* dengan *Letterbox Padding*

Jika foto asli berbentuk persegi panjang (`16:9`), *resize* langsung ke `224 × 224` akan membuat objek terdistorsi (*gepeng*). Salah satu cara menjaga proporsi adalah menambahkan *padding* sebelum *resize*.
"""
        )
    )

    cells.append(
        code(
            """
def resize_with_pad(im: Image.Image, target_size: int = 224) -> Image.Image:
    \"\"\"Me-resize gambar secara proporsional lalu menambahkan padding hingga persegi.\"\"\"
    return ImageOps.pad(im, (target_size, target_size), color=(248, 249, 250))

padded = resize_with_pad(Image.open(sample_img_path).convert("RGB"), IMG_SIZE)
assert padded.size == (IMG_SIZE, IMG_SIZE)
print("Ukuran hasil pad:", padded.size)
"""
        )
    )

    # Ringkasan & Mini-challenge
    cells.append(
        md(
            """
---
## Ringkasan & Mini-Challenge

Tuliskan **3 temuan utama** Anda berdasarkan tabel dan boxplot di atas:
1. Kondisi mana yang memiliki *edge density* lebih tinggi? Mengapa hal ini bisa membuat model AI lebih mudah terkecoh?
2. Bagaimana perbedaan *brightness* antara kondisi `polos` dan `ramai`?
3. Apakah ada file rusak atau duplikat yang berhasil tersaring?

*(Catatan: EDA pada pertemuan ini bersifat deskriptif; pembagian `Train / Val / Test` dan pencegahan data leakage secara penuh akan dibahas pada tahap split dataset).*
"""
        )
    )

    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    return nb


def main():
    NB_STUDENT.parent.mkdir(parents=True, exist_ok=True)
    NB_SOLUTION.parent.mkdir(parents=True, exist_ok=True)

    nbf.write(build_cells(is_solution=False), NB_STUDENT)
    nbf.write(build_cells(is_solution=True), NB_SOLUTION)
    print(f"Notebook peserta : {NB_STUDENT}")
    print(f"Notebook solusi  : {NB_SOLUTION}")


if __name__ == "__main__":
    main()
