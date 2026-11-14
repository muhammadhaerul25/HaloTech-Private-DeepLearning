"""Generator notebook peserta dan kunci jawaban untuk Hands-on P4: Image Processing & EDA."""

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

    # Judul + Tujuan + Estimasi Waktu
    cells.append(
        md(
            """
# Hands-on: Image Processing & Exploratory Data Analysis (EDA)

**Durasi Hands-on:** ±50 menit (6 langkah terpandu + 1 bagian Opsional)  
**Tujuan Pembelajaran:**
1. Memahami gambar digital sebagai *pixel matrix* `(tinggi, lebar, channel)` dan melakukan *normalization* (`uint8` → `float32`).
2. Memperbaiki *EXIF orientation* agar foto kamera HP tidak miring (*rotated*).
3. Menyaring *corrupted files* dan *duplicate images* menggunakan *file hash* (`SHA-256`).
4. Menghitung *Brightness*, *Contrast*, dan *Edge Density* untuk membandingkan kondisi **polos vs ramai**, lalu menyimpan laporan EDA.

> **Cara Kerja:** Jalankan sel dari atas ke bawah. Pada notebook peserta, lengkapi bagian bertanda `# TODO` sebelum menjalankan sel `assert` di bawahnya.
"""
        )
    )

    # Setup
    cells.append(
        md(
            """
## Setup & Konfigurasi Lingkungan (Colab / Lokal)

Sel ini otomatis mendeteksi apakah notebook dijalankan di Google Colab atau lokal, mengunci `SEED = 42` agar hasil *reproducible*, serta mengatur path dataset (`data/raw/` jika tersedia, atau `data/sample/` saat `SMOKE_TEST=1` / belum ada data pribadi).
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
    DATA_LABEL = "data/raw"
else:
    DATA_DIR = BASE_DIR / "data" / "sample"
    CLASS_NAMES = ["lingkaran", "persegi", "segitiga", "bintang", "heksagon"]
    DATA_LABEL = "contoh data sampel"

RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"IN_COLAB   : {IN_COLAB}")
print(f"SMOKE_TEST : {SMOKE_TEST}")
print(f"DATA_DIR   : {DATA_DIR.resolve()} ({DATA_LABEL})")
print(f"CLASS_NAMES: {CLASS_NAMES}")
print(f"Versi      : numpy={np.__version__}, cv2={cv2.__version__}, pandas={pd.__version__}")
"""
        )
    )

    # Langkah 1 (8 menit): Siapkan Folder & Uji Buka 1 Foto (RGB, Normalization, EXIF)
    cells.append(
        md(
            """
---
## Langkah 1 (8 menit): Uji Buka 1 Foto, *Normalization* & Koreksi *EXIF Orientation*

Komputer membaca gambar sebagai *pixel matrix* bertipe `uint8` (`0–255`). Sebelum masuk ke model AI:
1. Pastikan foto terbaca dalam format `RGB` dan ukuran seragam `IMG_SIZE × IMG_SIZE` (`224 × 224`).
2. Ubah tipe data ke `float32` lalu lakukan **normalization** (`÷ 255.0`) agar rentangnya `0.0–1.0`.
3. Terapkan `ImageOps.exif_transpose()` agar foto dari kamera HP tidak terbaca miring (*rotated*).
"""
        )
    )

    cells.append(
        code(
            """
all_jpgs = sorted(DATA_DIR.rglob("*.jpg"))
assert len(all_jpgs) > 0, f"Tidak ditemukan file .jpg di {DATA_DIR}"
sample_img_path = all_jpgs[0]

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
# 1A. Konversi uint8 -> float32 dan normalization ke [0.0, 1.0]
arr_norm = arr_u8.astype(np.float32) / 255.0

# 1B. Fungsi aman membuka gambar dengan koreksi EXIF orientation
def load_image_exif_safe(path: Path) -> Image.Image:
    \"\"\"Membuka gambar dan menerapkan koreksi orientasi EXIF secara otomatis.\"\"\"
    with Image.open(path) as im:
        im_fixed = ImageOps.exif_transpose(im)
        return im_fixed.convert("RGB")

test_fixed = load_image_exif_safe(sample_img_path)

assert arr_norm.shape == (IMG_SIZE, IMG_SIZE, 3), "Shape harus (224, 224, 3)"
assert arr_norm.dtype == np.float32, "Dtype harus float32"
assert 0.0 <= arr_norm.min() and arr_norm.max() <= 1.0, "Nilai harus berada di [0.0, 1.0]"
assert test_fixed.mode == "RGB"
print("Normalisasi min/max:", round(float(arr_norm.min()), 4), "/", round(float(arr_norm.max()), 4))
print("Cek Langkah 1 lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
# TODO 1A: Ubah arr_u8 ke tipe float32 lalu bagi dengan 255.0 agar rentangnya [0.0, 1.0]
# Petunjuk: arr_u8.astype(np.float32) / 255.0
arr_norm = None  # TODO: ganti None

# TODO 1B: Lengkapi fungsi koreksi EXIF orientation
def load_image_exif_safe(path: Path) -> Image.Image:
    \"\"\"Membuka gambar dan menerapkan koreksi orientasi EXIF secara otomatis.\"\"\"
    with Image.open(path) as im:
        im_fixed = None  # TODO: isi dengan ImageOps.exif_transpose(im)
        return im_fixed.convert("RGB")

test_fixed = load_image_exif_safe(sample_img_path)

assert arr_norm is not None, "arr_norm belum diisi!"
assert arr_norm.shape == (IMG_SIZE, IMG_SIZE, 3), "Shape harus (224, 224, 3)"
assert arr_norm.dtype == np.float32, "Dtype harus float32"
assert 0.0 <= arr_norm.min() and arr_norm.max() <= 1.0, "Nilai harus berada di [0.0, 1.0]"
assert test_fixed.mode == "RGB"
print("Cek Langkah 1 lolos!")
"""
            )
        )

    # Langkah 2 (8 menit): Saring Corrupted File & Hitung Class Balance
    cells.append(
        md(
            """
---
## Langkah 2 (8 menit): Saring *Corrupted Files* & Cek *Class Balance*

Sebelum menghitung statistik, kita periksa seluruh file `.jpg` di folder dataset:
- File yang gagal melewati `Image.verify()` ditandai sebagai **corrupted file** dan disisihkan.
- Untuk setiap **valid image**, kita catat kelas, kondisi (`polos`/`ramai`), resolusi, ukuran file, dan tag EXIF `Orientation`.
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
valid_records = []
corrupted_files = []
exif_rotated_count = 0

for p in all_jpgs:
    try:
        with Image.open(p) as im:
            im.verify()
    except Exception:
        corrupted_files.append(str(p))
        continue

    with Image.open(p) as im_raw:
        orient = im_raw.getexif().get(274, 1)  # 274 = Orientation
        if orient != 1:
            exif_rotated_count += 1

    with load_image_exif_safe(p) as im_ok:
        w, h = im_ok.size

    parts = p.relative_to(DATA_DIR).parts
    cls_name = parts[0] if len(parts) >= 2 else "unknown"
    cond_name = parts[1] if len(parts) >= 3 else "unknown"

    valid_records.append({
        "path": str(p),
        "filename": p.name,
        "class": cls_name,
        "condition": cond_name,
        "width": w,
        "height": h,
        "exif_orientation": orient,
        "size_kb": round(p.stat().st_size / 1024, 2),
    })

df_valid = pd.DataFrame(valid_records)
balance_tbl = pd.crosstab(df_valid["class"], df_valid["condition"])

print(f"Total file dicek     : {len(all_jpgs)}")
print(f"Corrupted files      : {len(corrupted_files)}")
print(f"Valid images         : {len(df_valid)}")
print(f"EXIF Orientation != 1: {exif_rotated_count}")
print("\\nTabel Class Balance (kelas x kondisi):")
print(balance_tbl)

assert len(df_valid) > 0, "Tidak ada valid images!"
print("Cek Langkah 2 lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
valid_records = []
corrupted_files = []
exif_rotated_count = 0

for p in all_jpgs:
    # TODO: cek integritas file dengan Image.open(p) dan im.verify() di dalam blok try/except
    # Jika gagal (rusak), tambahkan str(p) ke corrupted_files dan continue
    try:
        with Image.open(p) as im:
            pass  # TODO: ganti pass dengan im.verify()
    except Exception:
        corrupted_files.append(str(p))
        continue

    with Image.open(p) as im_raw:
        orient = im_raw.getexif().get(274, 1)
        if orient != 1:
            exif_rotated_count += 1

    with load_image_exif_safe(p) as im_ok:
        w, h = im_ok.size

    parts = p.relative_to(DATA_DIR).parts
    cls_name = parts[0] if len(parts) >= 2 else "unknown"
    cond_name = parts[1] if len(parts) >= 3 else "unknown"

    valid_records.append({
        "path": str(p),
        "filename": p.name,
        "class": cls_name,
        "condition": cond_name,
        "width": w,
        "height": h,
        "exif_orientation": orient,
        "size_kb": round(p.stat().st_size / 1024, 2),
    })

df_valid = pd.DataFrame(valid_records)
print(f"Valid images: {len(df_valid)} | Corrupted: {len(corrupted_files)}")
assert len(df_valid) < len(all_jpgs) or len(corrupted_files) == 0
print("Cek Langkah 2 lolos!")
"""
            )
        )

    # Langkah 3 (9 menit): Deteksi Duplicate Images dengan SHA-256
    cells.append(
        md(
            """
---
## Langkah 3 (9 menit): Deteksi *Duplicate Images* dengan *File Hash* (`SHA-256`)

Meskipun dua file memiliki nama berbeda, isi byte-nya bisa 100% identik (*duplicate images*). Jika tidak dibersihkan sebelum *split*, satu bisa masuk ke **Train Set** dan kembarannya masuk ke **Test Set** → menyebabkan **data leakage** & **inflated accuracy**!
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
def get_file_hash(path: Path, chunk_size: int = 8192) -> str:
    \"\"\"Menghitung file hash SHA-256 dari sebuah file gambar.\"\"\"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

df_valid["sha256"] = [get_file_hash(Path(p)) for p in df_valid["path"]]
dup_mask = df_valid.duplicated(subset=["sha256"], keep="first")
df_dups = df_valid[dup_mask]
df_clean = df_valid[~dup_mask].reset_index(drop=True)

print(f"Duplicate images ditemukan : {len(df_dups)}")
if len(df_dups) > 0:
    print("Contoh duplikat:", df_dups[["filename", "sha256"]].head().to_dict("records"))
print(f"Valid & unique images      : {len(df_clean)}")

assert df_clean["sha256"].is_unique, "Masih ada hash duplikat pada df_clean!"
print("Cek Langkah 3 lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
def get_file_hash(path: Path, chunk_size: int = 8192) -> str:
    \"\"\"Menghitung file hash SHA-256 dari sebuah file gambar.\"\"\"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            # TODO: perbarui hash dengan memanggil h.update(chunk)
            pass
    return h.hexdigest()

df_valid["sha256"] = [get_file_hash(Path(p)) for p in df_valid["path"]]
dup_mask = df_valid.duplicated(subset=["sha256"], keep="first")
df_dups = df_valid[dup_mask]
df_clean = df_valid[~dup_mask].reset_index(drop=True)

print(f"Duplicate images: {len(df_dups)} | Valid & unique: {len(df_clean)}")
assert df_clean["sha256"].is_unique, "Hash harus unik! Cek kembali get_file_hash."
print("Cek Langkah 3 lolos!")
"""
            )
        )

    # Langkah 4 (10 menit): Ukur Brightness, Contrast & Edge Density
    cells.append(
        md(
            """
---
## Langkah 4 (10 menit): Ukur *Brightness*, *Contrast* & *Edge Density*

Pada setiap gambar bersih (`df_clean`), kita ubah ke *grayscale* berukuran `IMG_SIZE × IMG_SIZE` lalu hitung:
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
    \"\"\"Menghitung Brightness, Contrast, dan Canny Edge Density pada foto.\"\"\"
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
df_eda = pd.concat([df_clean, metrics_df], axis=1)

assert {"brightness", "contrast", "edge_density"}.issubset(df_eda.columns)
assert df_eda["edge_density"].between(0.0, 1.0).all()
print(df_eda[["class", "condition", "brightness", "contrast", "edge_density"]].head())
print("Cek Langkah 4 lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
def compute_image_metrics(path: Path) -> dict:
    \"\"\"Menghitung Brightness, Contrast, dan Canny Edge Density pada foto.\"\"\"
    im = load_image_exif_safe(path).resize((IMG_SIZE, IMG_SIZE))
    gray = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    # TODO: hitung brightness (np.mean), contrast (np.std), dan edge_density (Canny)
    brightness = None    # TODO: float(np.mean(gray))
    contrast = None      # TODO: float(np.std(gray))
    edges = cv2.Canny(gray, 100, 200)
    edge_density = None  # TODO: float(np.mean(edges > 0))
    return {
        "brightness": brightness,
        "contrast": contrast,
        "edge_density": edge_density,
    }

metrics_df = pd.DataFrame([compute_image_metrics(Path(p)) for p in df_clean["path"]])
df_eda = pd.concat([df_clean, metrics_df], axis=1)

assert df_eda["brightness"].notna().all(), "brightness belum dihitung!"
assert df_eda["contrast"].notna().all(), "contrast belum dihitung!"
assert df_eda["edge_density"].between(0.0, 1.0).all(), "edge_density harus di antara 0 dan 1!"
print("Cek Langkah 4 lolos!")
"""
            )
        )

    # Langkah 5 (8 menit): Bandingkan Kondisi Polos vs Ramai
    cells.append(
        md(
            """
---
## Langkah 5 (8 menit): Bandingkan Kondisi *Polos vs Ramai* (Tabel & Boxplot)

Sekarang kita bandingkan distribusi *Brightness*, *Contrast*, dan *Edge Density* antara kondisi `polos` dan `ramai` secara kuantitatif dan visual.
"""
        )
    )

    cells.append(
        code(
            """
summary = (
    df_eda.groupby("condition")[["brightness", "contrast", "edge_density"]]
    .agg(["count", "mean", "std", "min", "max"])
    .round(4)
)
print(f"Ringkasan Statistik ({DATA_LABEL}):")
print(summary)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
df_eda.boxplot(column="brightness", by="condition", ax=axes[0])
axes[0].set_title(f"Brightness ({DATA_LABEL})")
axes[0].set_ylabel("Mean Intensity (0-255)")

df_eda.boxplot(column="contrast", by="condition", ax=axes[1])
axes[1].set_title(f"Contrast ({DATA_LABEL})")
axes[1].set_ylabel("Std Intensity")

df_eda.boxplot(column="edge_density", by="condition", ax=axes[2])
axes[2].set_title(f"Edge Density ({DATA_LABEL})")
axes[2].set_ylabel("Proporsi Piksel Tepi (0-1)")

plt.suptitle("")
plt.tight_layout()
out_plot = RESULTS_DIR / "p04_eda_polos_vs_ramai.png"
plt.savefig(out_plot, dpi=150)
plt.show()
print("Grafik perbandingan disimpan ke:", out_plot)
"""
        )
    )

    # Langkah 6 (7 menit): Simpan Ringkasan Audit Data
    cells.append(
        md(
            """
---
## Langkah 6 (7 menit): Simpan Ringkasan Audit Data & *Mini-Challenge*

Kita simpan tabel audit per foto (`p04_audit_metadata.csv`) dan tabel ringkasan statistik (`p04_eda_summary.csv`) ke folder `results/` sebagai pegangan sebelum tahap *dataset splitting*.
"""
        )
    )

    cells.append(
        code(
            """
audit_csv = RESULTS_DIR / "p04_audit_metadata.csv"
summary_csv = RESULTS_DIR / "p04_eda_summary.csv"

df_eda.to_csv(audit_csv, index=False)
summary.to_csv(summary_csv)

assert audit_csv.exists() and summary_csv.exists()
print("File audit tersimpan   :", audit_csv)
print("File ringkasan tersimpan:", summary_csv)
"""
        )
    )

    # Opsional
    cells.append(
        md(
            """
---
## Bagian Opsional: Menjaga *Aspect Ratio* dengan *Letterbox Padding*

Jika foto asli berbentuk persegi panjang (`16:9`), *resize* paksa ke `224 × 224` akan membuat objek *distorted* (gepeng). Salah satu solusinya adalah `ImageOps.pad()` agar proporsi objek tetap terjaga.
"""
        )
    )

    cells.append(
        code(
            """
def resize_with_pad(im: Image.Image, target_size: int = 224) -> Image.Image:
    \"\"\"Me-resize gambar secara proporsional lalu menambahkan padding hingga persegi.\"\"\"
    return ImageOps.pad(im, (target_size, target_size), color=(248, 249, 250))

padded = resize_with_pad(load_image_exif_safe(sample_img_path), IMG_SIZE)
assert padded.size == (IMG_SIZE, IMG_SIZE)
print("Ukuran hasil padding:", padded.size)
"""
        )
    )

    # Ringkasan & Mini-challenge
    cells.append(
        md(
            """
---
## Mini-Challenge & 3 Temuan Utama

Berdasarkan hasil tabel dan boxplot di atas, tuliskan **3 temuan utama** Anda:
1. Kondisi mana yang memiliki *Edge Density* jauh lebih tinggi? Mengapa kondisi tersebut lebih menantang bagi model AI?
2. Bagaimana perbedaan *Brightness* dan *Contrast* antara kondisi `polos` dan `ramai`?
3. Berapa banyak *corrupted files*, *duplicate images*, dan foto dengan `EXIF orientation != 1` yang berhasil Anda temukan?

*(Catatan: EDA pada sesi ini bersifat deskriptif; pembagian `Train / Val / Test` dan pencegahan data leakage secara penuh dilakukan pada sesi splitting dataset).*
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
