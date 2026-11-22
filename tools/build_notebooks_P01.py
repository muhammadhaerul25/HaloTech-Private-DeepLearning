"""Generator notebook peserta dan kunci jawaban untuk Hands-on P1:
Understanding Images & Image Processing (step-by-step sesuai slide P01).

Dirancang ramah pemula (awam-friendly):
- Dipecah cell-by-cell (satu sel = satu aksi sederhana).
- Tanpa sintaks Python tingkat lanjut yang membingungkan pemula.
- Setiap baris/blok kode dilengkapi komentar penjelasan bahasa Indonesia.
"""

from pathlib import Path
import json

try:
    import nbformat as nbf
except ImportError:
    nbf = None


ROOT = Path(__file__).resolve().parent.parent
NB_STUDENT = ROOT / "materials" / "P01" / "P01_understanding_images_processing_eda.ipynb"
NB_SOLUTION = ROOT / "materials" / "P01" / "solutions" / "P01_understanding_images_processing_eda.ipynb"


def _to_source_lines(text: str) -> list[str]:
    lines = text.strip().splitlines(keepends=True)
    return lines


def md(text: str):
    if nbf is not None:
        return nbf.v4.new_markdown_cell(text.strip())
    return {
        "cell_type": "markdown",
        "id": f"md-{abs(hash(text)) % 10**8:08d}",
        "metadata": {},
        "source": _to_source_lines(text),
    }


def code(text: str):
    if nbf is not None:
        return nbf.v4.new_code_cell(text.strip())
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": f"code-{abs(hash(text)) % 10**8:08d}",
        "metadata": {},
        "outputs": [],
        "source": _to_source_lines(text),
    }


def build_cells(is_solution: bool) -> list:
    cells = []

    # =========================================================================
    # JUDUL + TUJUAN + PETA HANDS-ON
    # =========================================================================
    cells.append(
        md(
            """
# Hands-on P01: Understanding Images, Image Processing & EDA

**Durasi Hands-on:** ±50 menit (6 langkah terpandu mengikuti alur slide presentasi Bab 1–4)  
**Gaya Belajar:** *Step-by-step* ramah pemula — kode dipecah satu per satu (*cell-by-cell*) lengkap dengan penjelasan komentar (`# ...`) di setiap barisnya.

**Tujuan Pembelajaran:**
1. Membaca gambar digital sebagai *pixel matrix* `(tinggi, lebar, channel)`, mengintip nilai intensitas `0–255` pada foto RGB (`224×224×3`) maupun **dataset asli MNIST (`28×28`)** (**Bab 1**).
2. Memisahkan **RGB channels** dan mengubah gambar ke **Grayscale** (**Bab 1**).
3. Memahami **AI Fundamental** (mengapa aturan manual `if-else` gagal saat objek bergeser/latar ramai) dan menerapkan **Image Processing** inti: *resize* dengan **Letterbox Padding** (`224×224`) serta **Normalization** (`uint8` → `float32` `0.0–1.0`) (**Bab 2**).
4. Mendeteksi **3 Jebakan Kamera HP**: *EXIF orientation*, *corrupted files*, dan *duplicate images* (`SHA-256`) (**Bab 4**).
5. Melakukan **Exploratory Data Analysis (EDA)** dataset: *Class Balance*, *Brightness*, *Contrast*, *Histogram*, dan *Edge Density* (**Polos vs Ramai**), lalu menyimpan laporan audit (**Bab 3 & 5**).

> **Cara Kerja:** Jalankan sel secara berurutan dari atas ke bawah (`Shift + Enter`). Pada notebook peserta, lengkapi bagian pendek bertanda `# TODO` sebelum menjalankan pengecekan (`assert`).
"""
        )
    )

    # =========================================================================
    # SETUP 1/3: IMPORT PUSTAKA (LIBRARIES)
    # =========================================================================
    cells.append(
        md(
            """
## Setup 1/3: Mengimpor Pustaka (*Libraries*) Python

Sebelum bekerja dengan gambar, kita memanggil "kotak perkakas" (*library*) yang sudah disediakan Python. Perhatikan komentar `#` di sebelah kanan untuk mengetahui fungsi masing-masing alat.
"""
        )
    )

    cells.append(
        code(
            """
# --- Pustaka bawaan Python ---
import os                   # Untuk membaca pengaturan sistem/environment komputer
import json                 # Untuk membaca file data berformat JSON (seperti sampel MNIST)
import random               # Untuk mengatur pengacakan angka
import hashlib              # Untuk membuat kode sidik jari file (SHA-256) pendeteksi foto kembar
from pathlib import Path    # Untuk mengelola alamat folder dan lokasi file dengan rapi

# --- Pustaka pengolahan gambar, tabel, dan grafik ---
import cv2                          # OpenCV: alat pengolahan citra (ubah warna, deteksi garis tepi Canny)
import numpy as np                  # NumPy: alat pengolah tabel/matriks angka pixel
import pandas as pd                 # Pandas: alat pembuat tabel data (mirip Excel) untuk audit & EDA
import matplotlib.pyplot as plt     # Matplotlib: alat untuk menampilkan foto dan menggambar grafik
from PIL import Image, ImageOps     # Pillow (PIL): alat untuk membuka file foto & memutar orientasi EXIF

print("Semua library berhasil dimuat!")
print(f"Versi library -> NumPy: {np.__version__} | OpenCV: {cv2.__version__} | Pandas: {pd.__version__}")
"""
        )
    )

    # =========================================================================
    # SETUP 2/3: DETEKSI COLAB & KUNCI SEED
    # =========================================================================
    cells.append(
        md(
            """
## Setup 2/3: Deteksi Lingkungan (Colab / Lokal) & Mengunci `SEED = 42`

Mengapa kita perlu mengunci `SEED = 42`? Agar setiap kali kode ini dijalankan ulang (baik hari ini maupun besok), urutan acaknya tetap konsisten (*reproducible*).
"""
        )
    )

    cells.append(
        code(
            """
# Cek otomatis apakah notebook ini sedang dibuka di Google Colab atau di komputer lokal
try:
    import google.colab  # noqa: F401
    from google.colab import drive
    drive.mount('/content/drive')   # Hubungkan Google Drive jika berada di Colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False                # Jika bukan di Colab, berarti berjalan di komputer lokal

# Kunci angka acak (SEED = 42) agar hasil eksperimen selalu konsisten
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

print(f"Berjalan di Google Colab : {IN_COLAB}")
print(f"Angka acak dikunci pada  : SEED = {SEED}")
"""
        )
    )

    # =========================================================================
    # SETUP 3/3: KONFIGURASI FOLDER DATASET
    # =========================================================================
    cells.append(
        md(
            """
## Setup 3/3: Menentukan Lokasi Folder Foto (`DATA_DIR`)

Sel ini mencari lokasi folder `data/` secara otomatis:
- Jika folder `data/raw/` sudah berisi foto Anda sendiri, notebook akan menggunakannya.
- Jika belum ada (atau saat mode uji cepat `SMOKE_TEST=1`), notebook otomatis memakai **`data/sample/`** yang berisi 120 foto latihan (5 bentuk × kondisi `polos` & `ramai`).
"""
        )
    )

    cells.append(
        code(
            """
# Ukuran standar tinggi & lebar gambar yang akan disiapkan untuk AI (224 x 224 pixel)
IMG_SIZE = 224

# Mode uji cepat (SMOKE_TEST): bernilai True jika variabel environment SMOKE_TEST="1"
SMOKE_TEST = os.environ.get("SMOKE_TEST", "0") == "1"

# Cari lokasi folder utama proyek yang memiliki subfolder "data"
BASE_DIR = Path(".")
for kandidat_folder in [Path("."), Path(".."), Path("../.."), Path("../../..")]:
    if (kandidat_folder / "data").exists():
        BASE_DIR = kandidat_folder
        break

# Pilih folder dataset: gunakan data/raw jika sudah ada isinya, jika belum gunakan data/sample
folder_raw = BASE_DIR / "data" / "raw"
if (not SMOKE_TEST) and folder_raw.exists() and any(folder_raw.iterdir()):
    DATA_DIR = folder_raw
    CLASS_NAMES = sorted([p.name for p in DATA_DIR.iterdir() if p.is_dir()])
    DATA_LABEL = "data/raw"
else:
    DATA_DIR = BASE_DIR / "data" / "sample"
    CLASS_NAMES = ["lingkaran", "persegi", "segitiga", "bintang", "heksagon"]
    DATA_LABEL = "contoh data sampel"

# Lokasi folder dataset klasik MNIST (28x28 pixel Grayscale) di dalam folder data/mnist
MNIST_DIR = BASE_DIR / "data" / "mnist"

# Siapkan folder "results/" untuk menyimpan grafik dan tabel CSV hasil audit nanti
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Mode SMOKE_TEST : {SMOKE_TEST}")
print(f"Lokasi Dataset  : {DATA_DIR.resolve()} ({DATA_LABEL})")
print(f"Lokasi MNIST    : {MNIST_DIR.resolve()}")
print(f"Daftar Kelas    : {CLASS_NAMES}")
print(f"Folder Hasil    : {RESULTS_DIR.resolve()}")
"""
        )
    )

    # =========================================================================
    # LANGKAH 1: MEMBACA GAMBAR & MENGINTIP MATRIKS PIXEL
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 1 (6 menit): Membaca Gambar & Mengintip Matriks Pixel (Sesuai Slide 08–13)

Mata manusia langsung mengenali bentuk benda (seperti **Apel Merah** pada **Slide 08**), tetapi **komputer hanya melihat deretan angka** di dalam kotak-kotak kecil (*pixel*, **Slide 10**). Saat menampilkan gambar ke layar (**Slide 09**), komputer menyalakan 3 lampu mikro **Red, Green, Blue** sesuai angka tersebut:
- Menurut **Color Channel** (**Slide 11**), gambar bisa memiliki **1 channel** (*Grayscale* `0–255` seperti **MNIST**), **3 channels** (**RGB**), **4 channels** (*RGBA*/*CMYK*), hingga **5+ channels** (satelit).
- Foto warna kita memakai format **RGB** berdimensi `(Tinggi, Lebar, 3)` dengan angka bulat `0` (gelap/mati) sampai `255` (terang penuh).

### Langkah 1.1: Mencari dan Membuka 1 File Foto Contoh
Mari kita ambil 1 file foto `.jpg` pertama dari folder dataset, lalu membukanya menggunakan `Image.open()`.
"""
        )
    )

    cells.append(
        code(
            """
# Cari semua file berakhiran .jpg di dalam folder DATA_DIR (termasuk di dalam sub-foldernya)
all_jpgs = sorted(DATA_DIR.rglob("*.jpg"))

# Pastikan minimal ada 1 file foto yang ditemukan
assert len(all_jpgs) > 0, f"Tidak ditemukan file .jpg di {DATA_DIR}"

# Ambil file foto urutan pertama (indeks ke-0) sebagai contoh
sample_img_path = all_jpgs[0]

# Buka file foto tersebut dengan Pillow, lalu pastikan format warnanya RGB (3 channel)
img_raw = Image.open(sample_img_path).convert("RGB")

print("Berhasil membuka foto contoh!")
print("Nama file         :", sample_img_path.name)
print("Ukuran (Lebar, Tinggi) di Pillow :", img_raw.size)
"""
        )
    )

    cells.append(
        md(
            """
### Langkah 1.2: Mengubah Foto Menjadi Tabel Angka (`NumPy Array`)
Agar komputer bisa menghitung isi foto, kita mengubah gambar `img_raw` menjadi matriks/tabel angka menggunakan `np.array()`.
> **Perhatian:** Di Pillow (`img_raw.size`), urutan ukurannya adalah `(Lebar, Tinggi)`. Namun setelah diubah ke tabel angka NumPy (`arr_raw.shape`), urutannya menjadi **`(Tinggi/Baris, Lebar/Kolom, Channel)`**.
"""
        )
    )

    cells.append(
        code(
            """
# Ubah gambar Pillow menjadi matriks angka 3 dimensi (NumPy array)
arr_raw = np.array(img_raw)

# Tampilkan informasi struktur matriks angka tersebut
print("Bentuk matriks (.shape) :", arr_raw.shape, "-> artinya (Tinggi, Lebar, Jumlah Channel)")
print("Tipe angka (.dtype)     :", arr_raw.dtype, "-> uint8 artinya angka bulat 0 sampai 255")
print("Angka paling gelap (min):", int(arr_raw.min()))
print("Angka paling terang(max):", int(arr_raw.max()))
"""
        )
    )

    cells.append(
        md(
            """
### Langkah 1.3: Menampilkan Foto Asli & Mengintip Angka di Area Kecil `8×8` Pixel
Supaya kita benar-benar yakin bahwa foto terdiri dari angka `0–255`, kita akan memotong kotak kecil berukuran `8×8` pixel tepat di tengah foto, lalu menuliskan angka terangnya di setiap kotak pixel!
"""
        )
    )

    cells.append(
        code(
            """
# Ambil nilai tinggi (h) dan lebar (w) dari bentuk matriks arr_raw
h, w, _ = arr_raw.shape

# Cari titik koordinat tengah gambar (dibagi 2 dengan pembulatan ke bawah //)
cy = h // 2   # Baris tengah (vertikal)
cx = w // 2   # Kolom tengah (horizontal)

# Potong (crop) area 8x8 pixel di sekitar titik tengah (4 pixel ke kiri/kanan dan atas/bawah)
patch_8x8 = arr_raw[cy - 4 : cy + 4, cx - 4 : cx + 4]

# Ubah potongan 8x8 tersebut menjadi 1 angka terang-gelap (Grayscale) agar mudah ditulis di layar
patch_gray = cv2.cvtColor(patch_8x8, cv2.COLOR_RGB2GRAY)

# Buat kanvas gambar dengan 2 kolom (kiri: foto asli, kanan: zoom-in 8x8 pixel)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# --- Panel Kiri: Foto Asli ---
axes[0].imshow(arr_raw)
axes[0].set_title(f"Foto Asli ({w}×{h} px)")
axes[0].axis("off")  # Sembunyikan garis sumbu koordinat

# --- Panel Kanan: Zoom-in 8x8 Pixel beserta angkanya ---
axes[1].imshow(patch_gray, cmap="gray", vmin=0, vmax=255)

# Tulis nilai angka (0-255) di tengah setiap kotak pixel (baris 0..7, kolom 0..7)
for baris in range(8):
    for kolom in range(8):
        nilai_pixel = int(patch_gray[baris, kolom])
        # Gunakan teks putih jika kotaknya gelap (<128), atau teks hitam jika kotaknya terang
        warna_teks = "white" if nilai_pixel < 128 else "black"
        axes[1].text(kolom, baris, str(nilai_pixel), ha="center", va="center", color=warna_teks, fontsize=8)

axes[1].set_title("Zoom-in 8×8 Pixel Tengah (Angka 0–255)")
axes[1].set_xticks(range(8))
axes[1].set_yticks(range(8))

plt.tight_layout()
plt.show()
"""
        )
    )

    cells.append(
        md(
            """
### Latihan 1 (`# TODO 1`): Membaca Dimensi & Nilai RGB Satu Titik Pixel
Sekarang giliran Anda!
1. Ambil ukuran `(img_h, img_w, img_c)` dari atribut `arr_raw.shape`.
2. Ambil 3 angka warna `[R, G, B]` tepat di titik pixel tengah gambar, yaitu pada baris `img_h // 2` dan kolom `img_w // 2`.
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
# 1. Ambil tinggi (img_h), lebar (img_w), dan jumlah channel (img_c) dari arr_raw.shape
img_h, img_w, img_c = arr_raw.shape

# 2. Ambil nilai [Red, Green, Blue] pada pixel di baris tengah (img_h // 2) dan kolom tengah (img_w // 2)
center_rgb = arr_raw[img_h // 2, img_w // 2]

# Pengecekan otomatis (assert) untuk memastikan jawaban benar
assert img_c == 3, "Gambar RGB harus memiliki 3 channel"
assert len(center_rgb) == 3, "Nilai 1 pixel RGB harus berisi 3 angka [R, G, B]"

print(f"Tinggi: {img_h} px | Lebar: {img_w} px | Channel: {img_c}")
print(f"Nilai [R, G, B] di pixel tengah: {center_rgb.tolist()}")
print("✅ Cek Langkah 1 lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
# TODO 1A: Isi dengan arr_raw.shape untuk mengambil (tinggi, lebar, channel)
img_h, img_w, img_c = None, None, None  # TODO: ganti None, None, None dengan arr_raw.shape

# TODO 1B: Ambil nilai RGB di titik tengah dengan mengakses arr_raw[img_h // 2, img_w // 2]
center_rgb = None                       # TODO: ganti None dengan arr_raw[img_h // 2, img_w // 2]

# Pengecekan otomatis (jangan diubah)
assert img_c == 3, "Gambar RGB harus memiliki 3 channel"
assert len(center_rgb) == 3, "Nilai 1 pixel RGB harus berisi 3 angka [R, G, B]"

print(f"Tinggi: {img_h} px | Lebar: {img_w} px | Channel: {img_c}")
print(f"Nilai [R, G, B] di pixel tengah: {center_rgb.tolist()}")
print("✅ Cek Langkah 1 lolos!")
"""
            )
        )
        cells.append(
            md(
                """
<details>
<summary><b>💡 Hint & Jawaban Langkah 1</b> (klik untuk membuka jika butuh bantuan)</summary>

**Penjelasan:**
- `arr_raw.shape` berisi 3 angka berurutan: `(tinggi, lebar, channel)`.
- Untuk membaca 1 titik pixel pada matriks gambar, tulis `nama_array[nomor_baris, nomor_kolom]`.

**Jawaban:**
```python
img_h, img_w, img_c = arr_raw.shape
center_rgb = arr_raw[img_h // 2, img_w // 2]
```
</details>
"""
            )
        )

    # =========================================================================
    # LANGKAH 1.4 & 1.5 (PEMANASAN KLASIK): DATASET ASLI MNIST (28x28 GRAYSCALE)
    # =========================================================================
    cells.append(
        md(
            """
### Langkah 1.4 (Pemanasan Klasik · Sesuai Slide 13): Membuka Dataset Asli MNIST (`28×28` Grayscale) dari `data/mnist/`

Di video klasik **3Blue1Brown**, pengenalan gambar dimulai dari dataset tulisan tangan angka **MNIST** yang sudah kita sediakan di folder **`data/mnist/`** (`0/` s.d. `9/`, `variants/`, serta arsip `mnist.npz`).
- Berbeda dengan foto warna (`224 × 224 × 3 = 150.528` angka), satu gambar MNIST hanyalah kotak hitam-putih kecil berukuran **`28 × 28 = 784` angka** (*1 channel Grayscale*).
- Mari kita buka file gambar angka **`'7'`** langsung dari folder `data/mnist/` menggunakan `Image.open()` dan `np.array()`!
"""
        )
    )

    cells.append(
        code(
            """
# Tentukan lokasi file gambar angka '7' dan dua variasi gaya tulisan tangan di folder data/mnist/
path_7_utama = MNIST_DIR / "7" / "mnist_7_01.png"
path_7_penulis_a = MNIST_DIR / "variants" / "mnist_7_penulis_a.png"
path_7_penulis_b = MNIST_DIR / "variants" / "mnist_7_penulis_b.png"

if path_7_utama.exists():
    # Buka file PNG langsung dari data/mnist/ dalam mode "L" (Grayscale 1 channel) lalu ubah ke array NumPy
    digit_7 = np.array(Image.open(path_7_utama).convert("L"))
    var_7a = np.array(Image.open(path_7_penulis_a).convert("L"))
    var_7b = np.array(Image.open(path_7_penulis_b).convert("L"))
else:
    # Cadangan (fallback) jika dijalankan terpisah di Google Colab tanpa folder data/mnist/
    from tensorflow.keras.datasets import mnist as tf_mnist
    (x_train, y_train), _ = tf_mnist.load_data()
    idx7 = np.where(y_train == 7)[0]
    digit_7, var_7a, var_7b = x_train[idx7[1]], x_train[idx7[0]], x_train[idx7[2]]

# Hitung total file gambar PNG yang tersedia di folder data/mnist/
total_png_mnist = len(list(MNIST_DIR.rglob("*.png"))) if MNIST_DIR.exists() else 0

print(f"Folder MNIST                   : {MNIST_DIR} ({total_png_mnist} file PNG siap pakai)")
print("Ukuran 1 gambar MNIST (.shape) :", digit_7.shape, "-> hanya (Tinggi, Lebar) karena 1 channel Grayscale")
print("Total pixel dalam 1 gambar     :", digit_7.size, "angka (28 x 28)")
print("Rentang nilai pixel            :", int(digit_7.min()), "sampai", int(digit_7.max()))
print(f"Nilai pixel di titik tengah (14,14) pada 2 tulisan '7' berbeda: Penulis A = {var_7a[14, 14]} vs Penulis B = {var_7b[14, 14]}")
"""
        )
    )

    cells.append(
        md(
            """
### Langkah 1.5: Visualisasi Angka Pixel MNIST `'7'` & Perbedaan Gaya Tulisan Tangan
Mari kita tampilkan gambar angka `'7'` tersebut beserta nilai angka di bagian tengahnya (`14×14`), lalu bandingkan tulisan tangan angka `'7'` dari **Penulis A** vs **Penulis B**.
"""
        )
    )

    cells.append(
        code(
            """
# Siapkan kanvas dengan 3 panel gambar berjajar
fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))

# --- Panel 1: Gambar MNIST '7' ukuran penuh 28x28 ---
axes[0].imshow(digit_7, cmap="gray", vmin=0, vmax=255)
axes[0].set_title("MNIST Asli '7' (28×28 px)")
axes[0].axis("off")

# --- Panel 2: Potongan tengah 14x14 beserta angka 0-255 ---
crop_7 = digit_7[7:21, 7:21]  # Ambil baris 7..20 dan kolom 7..20
axes[1].imshow(crop_7, cmap="gray", vmin=0, vmax=255)

for baris in range(14):
    for kolom in range(14):
        nilai = int(crop_7[baris, kolom])
        warna_teks = "white" if nilai < 128 else "black"
        axes[1].text(kolom, baris, str(nilai), ha="center", va="center", color=warna_teks, fontsize=6)

axes[1].set_title("Zoom-in Area Tengah 14×14 (0–255)")
axes[1].set_xticks([])
axes[1].set_yticks([])

# --- Panel 3: Dua gaya tulisan '7' berbeda digabung bersebelahan ---
garis_pemisah = np.full((28, 4), 180, dtype=np.uint8)  # Garis abu-abu selebar 4 pixel sebagai pembatas
dua_tulisan_7 = np.hstack([var_7a, garis_pemisah, var_7b])

axes[2].imshow(dua_tulisan_7, cmap="gray", vmin=0, vmax=255)
axes[2].set_title(f"Dua Penulis '7': pixel[14,14] = {var_7a[14,14]} vs {var_7b[14,14]}")
axes[2].axis("off")

plt.tight_layout()
plt.show()
"""
        )
    )

    # =========================================================================
    # LANGKAH 2: MEMISAHKAN RGB CHANNELS & KONVERSI GRAYSCALE
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 2 (6 menit): Memisahkan *RGB Channels* & Mengubah ke *Grayscale* (Sesuai Slide 14–18)

Foto berwarna **RGB** sebenarnya adalah **3 lembar matriks angka yang ditumpuk menjadi satu**:
- Lapisan ke-`0` (`arr_raw[:, :, 0]`) mengatur tingkat warna **Merah (*Red*)**.
- Lapisan ke-`1` (`arr_raw[:, :, 1]`) mengatur tingkat warna **Hijau (*Green*)**.
- Lapisan ke-`2` (`arr_raw[:, :, 2]`) mengatur tingkat warna **Biru (*Blue*)**.

> **Arti tanda titik dua `[:, :, 0]`:** Tanda `:` pertama artinya "ambil semua baris (tinggi)", tanda `:` kedua artinya "ambil semua kolom (lebar)", dan angka `0` artinya "ambil channel ke-0 saja".

### Latihan 2A (`# TODO 2A`): Memisahkan Channel Red, Green, dan Blue
Pisahkan ketiga lapisan warna dari `arr_raw` ke dalam variabel `r_ch`, `g_ch`, dan `b_ch`.
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
# Ambil semua baris (:), semua kolom (:), untuk masing-masing channel 0 (Red), 1 (Green), dan 2 (Blue)
r_ch = arr_raw[:, :, 0]   # Lapisan Merah (Red)
g_ch = arr_raw[:, :, 1]   # Lapisan Hijau (Green)
b_ch = arr_raw[:, :, 2]   # Lapisan Biru (Blue)

# Pastikan ukuran tiap lapisan adalah 2 dimensi (Tinggi, Lebar)
assert r_ch.shape == (img_h, img_w), "Ukuran channel Red harus (Tinggi, Lebar)"
assert g_ch.shape == (img_h, img_w), "Ukuran channel Green harus (Tinggi, Lebar)"
assert b_ch.shape == (img_h, img_w), "Ukuran channel Blue harus (Tinggi, Lebar)"

print("Ukuran masing-masing channel:", r_ch.shape, "-> 2 dimensi (Tinggi, Lebar)")
print("✅ Cek Latihan 2A lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
# TODO 2A: Pisahkan channel Red (indeks 0), Green (indeks 1), dan Blue (indeks 2) dari arr_raw
r_ch = None  # TODO: isi dengan arr_raw[:, :, 0]
g_ch = None  # TODO: isi dengan arr_raw[:, :, 1]
b_ch = None  # TODO: isi dengan arr_raw[:, :, 2]

# Pengecekan otomatis (jangan diubah)
assert r_ch is not None and r_ch.shape == (img_h, img_w), "Ukuran channel Red harus (Tinggi, Lebar)"
assert g_ch is not None and g_ch.shape == (img_h, img_w), "Ukuran channel Green harus (Tinggi, Lebar)"
assert b_ch is not None and b_ch.shape == (img_h, img_w), "Ukuran channel Blue harus (Tinggi, Lebar)"

print("Ukuran masing-masing channel:", r_ch.shape, "-> 2 dimensi (Tinggi, Lebar)")
print("✅ Cek Latihan 2A lolos!")
"""
            )
        )
        cells.append(
            md(
                """
<details>
<summary><b>💡 Hint & Jawaban Latihan 2A</b> (klik untuk membuka)</summary>

**Penjelasan:** Gunakan tanda kurung siku `[:, :, nomor_channel]` dengan nomor `0` untuk Red, `1` untuk Green, dan `2` untuk Blue.

**Jawaban:**
```python
r_ch = arr_raw[:, :, 0]
g_ch = arr_raw[:, :, 1]
b_ch = arr_raw[:, :, 2]
```
</details>
"""
            )
        )

    cells.append(
        md(
            """
### Latihan 2B (`# TODO 2B`): Mengubah Foto Berwarna (RGB) Menjadi Hitam-Putih (*Grayscale*)
Saat kita hanya ingin mengukur tingkat terang-gelap atau mencari garis tepi bentuk objek, 3 channel warna diringkas menjadi **1 channel *Grayscale*** menggunakan fungsi OpenCV: `cv2.cvtColor(arr_raw, cv2.COLOR_RGB2GRAY)`.
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
# Ubah gambar 3 channel (RGB) menjadi 1 channel (Grayscale / hitam-putih)
gray_arr = cv2.cvtColor(arr_raw, cv2.COLOR_RGB2GRAY)

# Pastikan hasilnya adalah matriks 2 dimensi (Tinggi, Lebar) tanpa dimensi channel ke-3
assert gray_arr.ndim == 2 and gray_arr.shape == (img_h, img_w), "Grayscale harus 2D (Tinggi, Lebar)"

print("Shape sebelum (RGB)      :", arr_raw.shape)
print("Shape sesudah (Grayscale):", gray_arr.shape)
print("✅ Cek Latihan 2B lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
# TODO 2B: Ubah arr_raw menjadi Grayscale menggunakan cv2.cvtColor(arr_raw, cv2.COLOR_RGB2GRAY)
gray_arr = None  # TODO: ganti None dengan cv2.cvtColor(arr_raw, cv2.COLOR_RGB2GRAY)

# Pengecekan otomatis (jangan diubah)
assert gray_arr is not None and gray_arr.ndim == 2 and gray_arr.shape == (img_h, img_w), "Grayscale harus 2D (Tinggi, Lebar)"

print("Shape sebelum (RGB)      :", arr_raw.shape)
print("Shape sesudah (Grayscale):", gray_arr.shape)
print("✅ Cek Latihan 2B lolos!")
"""
            )
        )
        cells.append(
            md(
                """
<details>
<summary><b>💡 Hint & Jawaban Latihan 2B</b> (klik untuk membuka)</summary>

**Jawaban:**
```python
gray_arr = cv2.cvtColor(arr_raw, cv2.COLOR_RGB2GRAY)
```
</details>
"""
            )
        )

    cells.append(
        md(
            """
### Langkah 2.3: Menampilkan Perbandingan Visual RGB vs Tiap Channel vs Grayscale
Sekarang kita tampilkan kelima hasil di atas secara berjajar agar terlihat jelas peran masing-masing channel.
"""
        )
    )

    cells.append(
        code(
            """
# Buat kanvas gambar dengan 5 kolom berjajar
fig, axes = plt.subplots(1, 5, figsize=(15, 3.2))

# Kolom 0: Foto Asli (RGB)
axes[0].imshow(arr_raw)
axes[0].set_title("1. Original (RGB)")
axes[0].axis("off")

# Kolom 1: Lapisan Merah (Red Channel)
axes[1].imshow(r_ch, cmap="Reds")
axes[1].set_title("2. Red Channel")
axes[1].axis("off")

# Kolom 2: Lapisan Hijau (Green Channel)
axes[2].imshow(g_ch, cmap="Greens")
axes[2].set_title("3. Green Channel")
axes[2].axis("off")

# Kolom 3: Lapisan Biru (Blue Channel)
axes[3].imshow(b_ch, cmap="Blues")
axes[3].set_title("4. Blue Channel")
axes[3].axis("off")

# Kolom 4: Hasil Grayscale (1 Channel)
axes[4].imshow(gray_arr, cmap="gray")
axes[4].set_title("5. Grayscale (1 Ch)")
axes[4].axis("off")

plt.tight_layout()
plt.show()
"""
        )
    )

    # =========================================================================
    # LANGKAH 3: AI FUNDAMENTAL & IMAGE PROCESSING (RESIZE, LETTERBOX & NORMALIZATION)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 3 (8 menit): Jembatan *AI Fundamental* & *Image Processing* (Sesuai Slide 20–27)

Sebelum melatih AI, ingat 3 konsep kunci pada **Bab 2 (Slide 20–22)**:
1. **Beda *Machine Learning* vs *Deep Learning* (Slide 20):** Pada *Machine Learning* klasik, manusia masih harus merumuskan ciri gambar secara manual. Pada **Deep Learning**, foto mentah langsung masuk dan jaringan saraf tiruan otomatis mempelajari ciri dari *garis tepi → bentuk → objek*.
2. **Kenapa Aturan Manual `If-Else` Gagal pada Foto (Slide 21)?** Mari kita buktikan di sel berikut: jika kita membuat aturan `if-else` yang mengecek warna di titik tengah foto, aturan itu langsung hancur begitu objek di foto bergeser sedikit saja!
"""
        )
    )

    cells.append(
        code(
            """
# Simulasikan objek di dalam foto bergeser 55 pixel ke kanan menggunakan np.roll
arr_shifted = np.roll(arr_raw, shift=55, axis=1)

# Baca nilai RGB tepat di titik tengah sebelum dan sesudah objek bergeser
rgb_tengah_awal = arr_raw[img_h // 2, img_w // 2].tolist()
rgb_tengah_geser = arr_shifted[img_h // 2, img_w // 2].tolist()

print("RGB titik tengah (saat objek di tengah) :", rgb_tengah_awal)
print("RGB titik tengah (saat objek bergeser)  :", rgb_tengah_geser)
print("-> Angkanya berubah drastis! Inilah alasan aturan if-else kaku gagal dan kita butuh Deep Learning.")
"""
        )
    )

    cells.append(
        md(
            """
### Latihan 3A (`# TODO 3A`): Menyamakan Ukuran Foto Tanpa Gepeng (*Letterbox Padding* `224×224`)
Model AI membutuhkan semua foto berukuran seragam (misalnya `224 × 224` pixel).
- Jika kita asal menarik paksa (*Stretch Resize*) foto persegi panjang menjadi kotak, bentuk objek akan **gepeng/penyok**.
- Solusinya adalah **Letterbox Padding**: kecilkan foto secara proporsional mengikuti sisi terpanjangnya (`target_size / max(lebar, tinggi)`), lalu tempelkan di tengah bingkai persegi berwarna abu-abu netral `(128, 128, 128)`.
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
def resize_letterbox(gambar_pil, target_size=IMG_SIZE):
    \"\"\"Mengubah ukuran gambar ke target_size x target_size tanpa membuat objek gepeng.\"\"\"
    # 1. Ambil lebar (w) dan tinggi (h) foto asli
    w, h = gambar_pil.size

    # 2. Hitung faktor skala proporsional berdasarkan sisi yang paling panjang
    sisi_terpanjang = max(w, h)
    scale = target_size / sisi_terpanjang

    # 3. Hitung lebar dan tinggi baru setelah dikalikan faktor skala
    new_w = int(round(w * scale))
    new_h = int(round(h * scale))

    # 4. Ubah ukuran gambar secara proporsional
    gambar_kecil = gambar_pil.resize((new_w, new_h), Image.Resampling.BILINEAR)

    # 5. Buat kanvas persegi baru berukuran target_size x target_size berwarna abu-abu (128, 128, 128)
    kanvas_persegi = Image.new("RGB", (target_size, target_size), (128, 128, 128))

    # 6. Hitung posisi tengah, lalu tempelkan gambar_kecil tepat di tengah kanvas_persegi
    posisi_x = (target_size - new_w) // 2
    posisi_y = (target_size - new_h) // 2
    kanvas_persegi.paste(gambar_kecil, (posisi_x, posisi_y))

    return kanvas_persegi


# Bandingkan hasil Stretch Resize biasa vs Letterbox Padding pada foto contoh
img_stretch = img_raw.resize((IMG_SIZE, IMG_SIZE))
img_letterbox = resize_letterbox(img_raw, IMG_SIZE)

assert img_letterbox.size == (IMG_SIZE, IMG_SIZE), "Ukuran hasil letterbox harus (224, 224)"
print("Ukuran foto setelah Letterbox Padding:", img_letterbox.size)
print("✅ Cek Latihan 3A lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
def resize_letterbox(gambar_pil, target_size=IMG_SIZE):
    \"\"\"Mengubah ukuran gambar ke target_size x target_size tanpa membuat objek gepeng.\"\"\"
    # 1. Ambil lebar (w) dan tinggi (h) foto asli
    w, h = gambar_pil.size

    # 2. TODO 3A: Hitung faktor skala proporsional: bagi target_size dengan sisi terpanjang max(w, h)
    scale = None  # TODO: ganti None dengan target_size / max(w, h)

    # 3. Hitung lebar dan tinggi baru setelah dikalikan faktor skala
    new_w = int(round(w * scale))
    new_h = int(round(h * scale))

    # 4. Ubah ukuran gambar secara proporsional
    gambar_kecil = gambar_pil.resize((new_w, new_h), Image.Resampling.BILINEAR)

    # 5. Buat kanvas persegi baru berukuran target_size x target_size berwarna abu-abu (128, 128, 128)
    kanvas_persegi = Image.new("RGB", (target_size, target_size), (128, 128, 128))

    # 6. Hitung posisi tengah, lalu tempelkan gambar_kecil tepat di tengah kanvas_persegi
    posisi_x = (target_size - new_w) // 2
    posisi_y = (target_size - new_h) // 2
    kanvas_persegi.paste(gambar_kecil, (posisi_x, posisi_y))

    return kanvas_persegi


# Jalankan fungsi pada foto contoh
img_stretch = img_raw.resize((IMG_SIZE, IMG_SIZE))
img_letterbox = resize_letterbox(img_raw, IMG_SIZE)

# Pengecekan otomatis (jangan diubah)
assert img_letterbox.size == (IMG_SIZE, IMG_SIZE), "Ukuran hasil letterbox harus (224, 224)"
print("Ukuran foto setelah Letterbox Padding:", img_letterbox.size)
print("✅ Cek Latihan 3A lolos!")
"""
            )
        )
        cells.append(
            md(
                """
<details>
<summary><b>💡 Hint & Jawaban Latihan 3A</b> (klik untuk membuka)</summary>

**Penjelasan:** Agar sisi foto yang paling panjang (`max(w, h)`) pas masuk ke dalam ukuran `target_size`, rumus skalanya adalah `target_size / max(w, h)`.

**Jawaban:**
```python
scale = target_size / max(w, h)
```
</details>
"""
            )
        )

    cells.append(
        md(
            """
### Langkah 3.3: Menampilkan Perbandingan *Foto Asli* vs *Stretch Resize* vs *Letterbox Padding*
Mari kita lihat hasil gambar yang sudah diubah ukurannya ke `224 × 224` pixel.
"""
        )
    )

    cells.append(
        code(
            """
# Tampilkan 3 panel gambar untuk membandingkan hasil resize
fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))

axes[0].imshow(img_raw)
axes[0].set_title(f"1. Foto Asli ({img_raw.size[0]}×{img_raw.size[1]})")
axes[0].axis("off")

axes[1].imshow(img_stretch)
axes[1].set_title(f"2. Stretch Resize ({IMG_SIZE}×{IMG_SIZE})")
axes[1].axis("off")

axes[2].imshow(img_letterbox)
axes[2].set_title(f"3. Letterbox Padding ({IMG_SIZE}×{IMG_SIZE})")
axes[2].axis("off")

plt.tight_layout()
plt.show()
"""
        )
    )

    cells.append(
        md(
            """
### Latihan 3B (`# TODO 3B`): *Normalization* — Mengubah Skala Angka `0–255` Menjadi `0.0–1.0`
Jaringan saraf tiruan (*Deep Learning*) jauh lebih stabil dan cepat belajar jika diberi angka desimal kecil (`0.0` sampai `1.0`) dibandingkan angka bulat besar (`0` sampai `255`).
Caranya hanya 2 tahap:
1. Ubah tipe data array dari `uint8` (angka bulat) menjadi `np.float32` (angka desimal).
2. Bagi seluruh angka dengan `255.0`.
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
# Ubah gambar hasil letterbox menjadi matriks angka uint8 (0 s.d. 255)
arr_u8 = np.array(img_letterbox)

# Tahap 1: Ubah tipe angka dari uint8 menjadi angka desimal float32
arr_float = arr_u8.astype(np.float32)

# Tahap 2: Bagi semua angka dengan 255.0 agar nilainya berada di rentang 0.0 sampai 1.0
arr_norm = arr_float / 255.0

# Pengecekan otomatis
assert arr_norm.shape == (IMG_SIZE, IMG_SIZE, 3), "Shape harus (224, 224, 3)"
assert arr_norm.dtype == np.float32, "Tipe data harus float32"
assert 0.0 <= arr_norm.min() and arr_norm.max() <= 1.0, "Nilai harus di antara 0.0 dan 1.0"

print(f"Sebelum normalisasi -> tipe: {arr_u8.dtype}   | min: {arr_u8.min()}      | max: {arr_u8.max()}")
print(f"Sesudah normalisasi -> tipe: {arr_norm.dtype} | min: {arr_norm.min():.4f} | max: {arr_norm.max():.4f}")
print("✅ Cek Latihan 3B lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
# Ubah gambar hasil letterbox menjadi matriks angka uint8 (0 s.d. 255)
arr_u8 = np.array(img_letterbox)

# TODO 3B: Ubah arr_u8 ke tipe np.float32 lalu bagi dengan 255.0
arr_norm = None  # TODO: ganti None dengan arr_u8.astype(np.float32) / 255.0

# Pengecekan otomatis (jangan diubah)
assert arr_norm is not None and arr_norm.shape == (IMG_SIZE, IMG_SIZE, 3), "Shape harus (224, 224, 3)"
assert arr_norm.dtype == np.float32, "Tipe data harus float32"
assert 0.0 <= arr_norm.min() and arr_norm.max() <= 1.0, "Nilai harus di antara 0.0 dan 1.0"

print(f"Sebelum normalisasi -> tipe: {arr_u8.dtype}   | min: {arr_u8.min()}      | max: {arr_u8.max()}")
print(f"Sesudah normalisasi -> tipe: {arr_norm.dtype} | min: {arr_norm.min():.4f} | max: {arr_norm.max():.4f}")
print("✅ Cek Latihan 3B lolos!")
"""
            )
        )
        cells.append(
            md(
                """
<details>
<summary><b>💡 Hint & Jawaban Latihan 3B</b> (klik untuk membuka)</summary>

**Penjelasan:** Gunakan `.astype(np.float32)` untuk mengubah tipe angka menjadi desimal, lalu bagi dengan `255.0`.

**Jawaban:**
```python
arr_norm = arr_u8.astype(np.float32) / 255.0
```
</details>
"""
            )
        )

    # =========================================================================
    # LANGKAH 4: TIGA JEBAKAN KAMERA HP (EXIF, CORRUPTED, DUPLICATE HASH)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 4 (10 menit): Mengatasi 3 Jebakan Tersembunyi Kamera HP (Sesuai Slide 40–45)

Sebelum menganalisis ratusan foto di dataset, kita harus menyiapkan **3 alat penyaring** untuk mengatasi jebakan klasik kamera HP:
1. **Jebakan #1 — *EXIF Orientation*:** Foto terlihat tegak di galeri HP, tapi tersimpan miring di file.
2. **Jebakan #2 — *Corrupted Files*:** File foto rusak/kosong yang bisa membuat program berhenti mendadak (*crash*).
3. **Jebakan #3 — *Duplicate Images*:** Foto kembar identik yang bisa memicu *Data Leakage* (kebocoran data ujian AI).

Kita akan membuat dan menguji ketiga fungsi penyaring tersebut **satu per satu**!

### Latihan 4A (`# TODO 4A`): Membuat Fungsi Pembuka Foto Anti-Miring (*EXIF Orientation*)
Gunakan `ImageOps.exif_transpose(im)` di dalam fungsi berikut agar setiap foto otomatis diputar tegak sesuai catatan kamera HP.
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
def load_image_exif_safe(lokasi_foto):
    \"\"\"Membuka foto dan memutarnya otomatis jika ada catatan rotasi EXIF dari kamera HP.\"\"\"
    with Image.open(lokasi_foto) as im:
        # Putar foto menjadi tegak sesuai tag EXIF
        im_fixed = ImageOps.exif_transpose(im)
        # Kembalikan gambar dalam format warna RGB standar
        return im_fixed.convert("RGB")


# Uji fungsi kita pada 1 foto contoh
contoh_tegak = load_image_exif_safe(sample_img_path)
assert contoh_tegak.size == img_raw.size
print("Berhasil menguji fungsi EXIF pada:", sample_img_path.name, "| Ukuran:", contoh_tegak.size)
print("✅ Cek Latihan 4A lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
def load_image_exif_safe(lokasi_foto):
    \"\"\"Membuka foto dan memutarnya otomatis jika ada catatan rotasi EXIF dari kamera HP.\"\"\"
    with Image.open(lokasi_foto) as im:
        # TODO 4A: Gunakan ImageOps.exif_transpose(im) agar foto miring otomatis ditegakkan
        im_fixed = None  # TODO: ganti None dengan ImageOps.exif_transpose(im)
        return im_fixed.convert("RGB")


# Uji fungsi kita pada 1 foto contoh
contoh_tegak = load_image_exif_safe(sample_img_path)
assert contoh_tegak.size == img_raw.size
print("Berhasil menguji fungsi EXIF pada:", sample_img_path.name, "| Ukuran:", contoh_tegak.size)
print("✅ Cek Latihan 4A lolos!")
"""
            )
        )
        cells.append(
            md(
                """
<details>
<summary><b>💡 Hint & Jawaban Latihan 4A</b> (klik untuk membuka)</summary>

**Jawaban:**
```python
im_fixed = ImageOps.exif_transpose(im)
```
</details>
"""
            )
        )

    cells.append(
        md(
            """
### Latihan 4B (`# TODO 4B`): Membuat Fungsi Pemeriksa File Rusak (*Corrupted File*)
Bagaimana komputer mengecek apakah sebuah file `.jpg` utuh atau rusak tanpa membuat program macet?
- Kita gunakan blok `try ... except` dan perintah `im.verify()` dari Pillow.
- Jika file foto sehat, fungsi mengembalikan status `True`. Jika file rusak, bagian `except` akan menangkap error-nya dan mengembalikan status `False` dengan aman!
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
def check_image_integrity(lokasi_foto):
    \"\"\"Mengecek apakah file foto utuh (valid) atau rusak (corrupted).\"\"\"
    try:
        # Tahap 1: Buka file dan jalankan verify() untuk memeriksa keutuhan data gambar
        with Image.open(lokasi_foto) as im:
            im.verify()

        # Tahap 2: Jika tidak rusak, buka kembali untuk membaca ukuran lebar (w) dan tinggi (h)
        with Image.open(lokasi_foto) as im2:
            im2 = ImageOps.exif_transpose(im2)
            w, h = im2.size

        # Kembalikan: (status_sehat=True, lebar, tinggi, pesan_error_kosong)
        return True, int(w), int(h), ""

    except Exception as pesan_error:
        # Jika terjadi error saat dibuka/diverifikasi, tandai file sebagai rusak (False)
        return False, 0, 0, str(pesan_error)


# Uji fungsi pada 1 foto contoh
status_sehat, lebar_uji, tinggi_uji, info_err = check_image_integrity(sample_img_path)
assert status_sehat is True, "Foto contoh seharusnya valid!"
print(f"Hasil cek '{sample_img_path.name}' -> Sehat: {status_sehat} | Ukuran: {lebar_uji}x{tinggi_uji}")
print("✅ Cek Latihan 4B lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
def check_image_integrity(lokasi_foto):
    \"\"\"Mengecek apakah file foto utuh (valid) atau rusak (corrupted).\"\"\"
    try:
        # Tahap 1: Buka file dan jalankan im.verify() untuk memeriksa keutuhan gambar
        with Image.open(lokasi_foto) as im:
            pass  # TODO 4B: ganti kata pass dengan im.verify()

        # Tahap 2: Jika tidak rusak, buka kembali untuk membaca ukuran lebar (w) dan tinggi (h)
        with Image.open(lokasi_foto) as im2:
            im2 = ImageOps.exif_transpose(im2)
            w, h = im2.size

        return True, int(w), int(h), ""

    except Exception as pesan_error:
        # Jika file rusak, tangkap error-nya agar program tidak berhenti macet
        return False, 0, 0, str(pesan_error)


# Uji fungsi pada 1 foto contoh
status_sehat, lebar_uji, tinggi_uji, info_err = check_image_integrity(sample_img_path)
assert status_sehat is True, "Foto contoh seharusnya valid!"
print(f"Hasil cek '{sample_img_path.name}' -> Sehat: {status_sehat} | Ukuran: {lebar_uji}x{tinggi_uji}")
print("✅ Cek Latihan 4B lolos!")
"""
            )
        )
        cells.append(
            md(
                """
<details>
<summary><b>💡 Hint & Jawaban Latihan 4B</b> (klik untuk membuka)</summary>

**Penjelasan:** Panggil `im.verify()` di dalam blok `with Image.open(lokasi_foto) as im:` agar Pillow menguji apakah isi file foto rusak atau tidak.

**Jawaban:**
```python
im.verify()
```
</details>
"""
            )
        )

    cells.append(
        md(
            """
### Latihan 4C (`# TODO 4C`): Membuat Fungsi Sidik Jari File (`SHA-256`) Pendeteksi Foto Kembar
Dua file foto yang isinya 100% kembar akan menghasilkan kode *hash* **SHA-256** (64 karakter huruf & angka) yang persis sama, walaupun nama file-nya berbeda (`foto_01.jpg` vs `foto_02.jpg`).
Cara kerjanya sangat sederhana (sesuai **Slide 46**):
1. Buat objek penghitung hash `h = hashlib.sha256()`.
2. Baca seluruh isi byte file (`isi_file = f.read()`), lalu masukkan ke dalam penghitung hash dengan `h.update(isi_file)`.
3. Ambil hasil teks sidik jarinya menggunakan `h.hexdigest()`.
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
def compute_sha256(lokasi_foto):
    \"\"\"Menghasilkan kode unik SHA-256 (64 karakter) sebagai sidik jari isi file.\"\"\"
    # 1. Siapkan mesin penghitung hash SHA-256
    h = hashlib.sha256()

    # 2. Buka file dalam mode biner ("rb" = read binary) dan baca seluruh isinya
    with open(lokasi_foto, "rb") as f:
        isi_file = f.read()
        # Masukkan isi file ke mesin penghitung hash
        h.update(isi_file)

    # 3. Kembalikan hasil kode hash dalam bentuk teks heksadesimal (64 karakter)
    return h.hexdigest()


# Uji fungsi sidik jari pada foto contoh
contoh_hash = compute_sha256(sample_img_path)
assert len(contoh_hash) == 64, "Kode SHA-256 harus sepanjang 64 karakter"
print(f"File       : {sample_img_path.name}")
print(f"SHA-256    : {contoh_hash}")
print("✅ Cek Latihan 4C lolos!")
"""
            )
        )
    else:
        cells.append(
            code(
                """
def compute_sha256(lokasi_foto):
    \"\"\"Menghasilkan kode unik SHA-256 (64 karakter) sebagai sidik jari isi file.\"\"\"
    # 1. Siapkan mesin penghitung hash SHA-256
    h = hashlib.sha256()

    # 2. Buka file dalam mode biner ("rb" = read binary) dan baca seluruh isinya
    with open(lokasi_foto, "rb") as f:
        isi_file = f.read()
        # TODO 4C: Masukkan isi_file ke dalam objek hash h menggunakan h.update(isi_file)
        pass  # TODO: ganti kata pass dengan h.update(isi_file)

    # 3. Kembalikan hasil kode hash dalam bentuk teks (64 karakter)
    return h.hexdigest()


# Uji fungsi sidik jari pada foto contoh
contoh_hash = compute_sha256(sample_img_path)
assert len(contoh_hash) == 64, "Kode SHA-256 harus sepanjang 64 karakter"
print(f"File       : {sample_img_path.name}")
print(f"SHA-256    : {contoh_hash}")
print("✅ Cek Latihan 4C lolos!")
"""
            )
        )
        cells.append(
            md(
                """
<details>
<summary><b>💡 Hint & Jawaban Latihan 4C</b> (klik untuk membuka)</summary>

**Penjelasan:** Setelah `isi_file = f.read()`, panggil `h.update(isi_file)` untuk menghitung sidik jari digital dari byte file tersebut.

**Jawaban:**
```python
h.update(isi_file)
```
</details>
"""
            )
        )

    cells.append(
        md(
            """
### Langkah 4.4: Memindai Seluruh Foto di Folder Dataset
Setelah ketiga fungsi penyaring kita siap, mari kita gunakan perulangan `for` untuk memeriksa seluruh file foto di `DATA_DIR` satu per satu dan mencatat hasilnya ke dalam tabel `df_audit`.
"""
        )
    )

    cells.append(
        code(
            """
# Daftar akhiran (ekstensi) file gambar yang ingin kita periksa
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# Kumpulkan semua file gambar di dalam folder DATA_DIR
image_files = []
for p in sorted(DATA_DIR.rglob("*")):
    if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
        image_files.append(p)

# Siapkan list kosong untuk menampung catatan hasil pemeriksaan setiap foto
records = []

# Periksa foto satu per satu
for p in image_files:
    # Ambil alamat relatif terhadap DATA_DIR (contoh: "lingkaran/polos/lingkaran_polos_01.jpg")
    rel = p.relative_to(DATA_DIR)
    cls_name = rel.parts[0] if len(rel.parts) >= 2 else "unknown"   # Nama kelas (misal: lingkaran)
    cond = rel.parts[1] if len(rel.parts) >= 3 else "unknown"       # Kondisi latar (polos / ramai)

    # Jalankan fungsi pemeriksa keutuhan file (Latihan 4B)
    is_valid, w, h, err = check_image_integrity(p)

    # Jika fotonya sehat (is_valid), hitung sidik jari SHA-256 (Latihan 4C)
    sha = compute_sha256(p) if is_valid else ""

    # Simpan informasi foto ini ke dalam daftar records
    records.append({
        "rel_path": str(rel).replace("\\\\", "/"),
        "class": cls_name,
        "condition": cond,
        "width": w,
        "height": h,
        "is_valid": is_valid,
        "error": err,
        "sha256": sha,
        "abs_path": str(p),
    })

# Ubah daftar records menjadi tabel Pandas DataFrame
df_audit = pd.DataFrame(records)
print(f"Selesai memindai {len(df_audit)} file! Berikut 5 baris pertama tabel audit:")
print(df_audit[["rel_path", "class", "condition", "width", "height", "is_valid"]].head().to_string(index=False))
"""
        )
    )

    cells.append(
        md(
            """
### Langkah 4.5: Menandai Foto Kembar (*Duplicate*) & Mencetak Ringkasan Audit
Sekarang kita saring foto yang sehat (`df_valid`), tandai jika ada yang memiliki kode `sha256` kembar dengan `.duplicated(subset=["sha256"])`, lalu tampilkan laporan temuannya!
"""
        )
    )

    cells.append(
        code(
            """
# Tandai foto yang valid dan memiliki kode SHA-256 yang sama persis dengan foto sebelumnya
df_audit["is_duplicate"] = df_audit["is_valid"] & df_audit.duplicated(subset=["sha256"], keep="first")

# Buat tabel khusus berisi foto-foto yang sehat (valid) untuk dianalisis pada Langkah 5
df_valid = df_audit[df_audit["is_valid"]].copy()

# Hitung jumlah file yang rusak dan yang duplikat
n_corrupted = int((~df_audit["is_valid"]).sum())
n_dupes = int(df_audit["is_duplicate"].sum())

assert len(df_audit) > 0, "Tabel audit tidak boleh kosong!"

print("=== RINGKASAN AUDIT KEBERSIHAN DATASET ===")
print(f"Total file dipindai      : {len(df_audit)}")
print(f"Foto sehat (Valid)       : {len(df_valid)}")
print(f"Foto rusak (Corrupted)   : {n_corrupted}")
print(f"Foto kembar (Duplicate)  : {n_dupes}")

# Tampilkan nama file yang rusak atau duplikat jika ditemukan
if n_corrupted > 0:
    print("\\nDaftar file rusak (disisihkan otomatis):")
    print(df_audit[~df_audit["is_valid"]][["rel_path", "error"]].to_string(index=False))

if n_dupes > 0:
    print("\\nDaftar file duplikat (memiliki SHA-256 kembar):")
    print(df_audit[df_audit["is_duplicate"]][["rel_path", "sha256"]].to_string(index=False))

print("\\n✅ Cek Langkah 4 selesai dengan sempurna!")
"""
        )
    )

    # =========================================================================
    # LANGKAH 5: EDA KESEHATAN DATASET (CLASS BALANCE, BRIGHTNESS, CONTRAST, EDGE DENSITY)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 5 (12 menit): EDA Kesehatan Dataset (*Class Balance*, *Brightness*, *Contrast* & *Edge Density*)

Setelah file yang rusak disisihkan, sekarang kita memeriksa **kesehatan foto yang valid (`df_valid`)** sesuai **Bab 3 EDA (Slide 31–39)**:
- **Issue #1 — *Class Imbalance*:** Apakah jumlah foto di setiap kelas dan kondisi (`polos` vs `ramai`) sudah seimbang?
- **Issue #2 — Pencahayaan (*Brightness* & *Contrast*):** Rata-rata terang (`np.mean`) dan tingkat kontras (`np.std`).
- **Issue #3 — Keramaian Latar Belakang (*Edge Density*):** Persentase piksel garis tepi hasil deteksi **Canny** (`cv2.Canny`).

### Langkah 5.1: Memeriksa Keseimbangan Jumlah Foto (*Class Balance* · Issue #1)
Kita gunakan `pd.crosstab()` untuk menghitung jumlah foto per kelas dan kondisi latar, lalu menggambar grafik batangnya.
"""
        )
    )

    cells.append(
        code(
            """
# Hitung tabel silang jumlah foto untuk setiap Kelas (baris) dan Kondisi Latar (kolom)
ct = pd.crosstab(df_valid["class"], df_valid["condition"])

print("Tabel Distribusi Jumlah Foto per Kelas & Kondisi:")
print(ct)

# Gambar grafik batang (bar chart) dari tabel di atas
ax = ct.plot(kind="bar", figsize=(8, 3.6), color=["#4285F4", "#EA4335"])
ax.set_title(f"Class Balance per Kelas & Kondisi ({DATA_LABEL})")
ax.set_xlabel("Nama Kelas")
ax.set_ylabel("Jumlah Foto Valid")
plt.xticks(rotation=0)  # Buat tulisan nama kelas di sumbu X tetap mendatar (tidak miring)
plt.tight_layout()
plt.show()
"""
        )
    )

    cells.append(
        md(
            """
### Latihan 5 (`# TODO 5`): Menghitung *Brightness*, *Contrast*, dan *Edge Density* (Issue #2 & #3)
Pada fungsi `compute_image_metrics(lokasi_foto)` di bawah ini, gambar diubah menjadi hitam-putih (`gray`), lalu kita hitung 3 angka kesehatannya:
1. **`brightness`**: Nilai rata-rata seluruh pixel (`float(np.mean(gray))`). Makin tinggi mendekati 255, foto makin terang.
2. **`contrast`**: Nilai simpangan baku pixel (`float(np.std(gray))`). Makin tinggi, perbedaan antara area terang dan gelap makin tajam.
3. **`edge_density`**: Proporsi pixel yang merupakan garis tepi (`float(np.mean(edges > 0))`). Makin tinggi, latar belakang foto makin ramai/penuh corak!
"""
        )
    )

    if is_solution:
        cells.append(
            code(
                """
def compute_image_metrics(lokasi_foto):
    \"\"\"Menghitung nilai (brightness, contrast, edge_density) dari sebuah foto.\"\"\"
    # 1. Buka foto dengan koreksi EXIF, lalu ubah ke mode "L" (Luminance / Grayscale 1 channel)
    im = load_image_exif_safe(lokasi_foto)
    gray = np.array(im.convert("L"))

    # 2. Hitung rata-rata terang (Brightness) menggunakan np.mean
    brightness = float(np.mean(gray))

    # 3. Hitung ketajaman perbedaan terang-gelap (Contrast) menggunakan np.std
    contrast = float(np.std(gray))

    # 4. Deteksi garis tepi dengan algoritma Canny (ambang bawah 100, ambang atas 200)
    edges = cv2.Canny(gray, 100, 200)

    # 5. Hitung proporsi pixel yang merupakan garis tepi (nilainya > 0)
    edge_density = float(np.mean(edges > 0))

    return brightness, contrast, edge_density


# Hitung ketiga metrik di atas untuk seluruh foto yang valid
daftar_metrik = []
for alamat_file in df_valid["abs_path"]:
    b, c, ed = compute_image_metrics(Path(alamat_file))
    daftar_metrik.append({"brightness": b, "contrast": c, "edge_density": ed})

# Gabungkan hasil hitungan ke dalam tabel df_valid
df_metrik = pd.DataFrame(daftar_metrik, index=df_valid.index)
df_valid[["brightness", "contrast", "edge_density"]] = df_metrik

# Pengecekan otomatis
assert df_valid["brightness"].between(0, 255).all(), "Brightness harus di antara 0 dan 255"
assert (df_valid["contrast"] >= 0).all(), "Contrast tidak boleh negatif"
assert df_valid["edge_density"].between(0, 1).all(), "Edge density harus berupa proporsi 0.0 s.d. 1.0"

print("✅ Cek Langkah 5 lolos! Contoh hasil metrik pada 5 foto pertama:")
print(df_valid[["rel_path", "condition", "brightness", "contrast", "edge_density"]].head().to_string(index=False))
"""
            )
        )
    else:
        cells.append(
            code(
                """
def compute_image_metrics(lokasi_foto):
    \"\"\"Menghitung nilai (brightness, contrast, edge_density) dari sebuah foto.\"\"\"
    # 1. Buka foto dengan koreksi EXIF, lalu ubah ke mode "L" (Luminance / Grayscale 1 channel)
    im = load_image_exif_safe(lokasi_foto)
    gray = np.array(im.convert("L"))

    # 2. TODO 5A: Hitung rata-rata terang (Brightness) dengan float(np.mean(gray))
    brightness = None    # TODO: ganti None dengan float(np.mean(gray))

    # 3. TODO 5B: Hitung simpangan baku (Contrast) dengan float(np.std(gray))
    contrast = None      # TODO: ganti None dengan float(np.std(gray))

    # 4. Deteksi garis tepi dengan algoritma Canny
    edges = cv2.Canny(gray, 100, 200)

    # 5. TODO 5C: Hitung proporsi pixel garis tepi dengan float(np.mean(edges > 0))
    edge_density = None  # TODO: ganti None dengan float(np.mean(edges > 0))

    return brightness, contrast, edge_density


# Hitung ketiga metrik di atas untuk seluruh foto yang valid
daftar_metrik = []
for alamat_file in df_valid["abs_path"]:
    b, c, ed = compute_image_metrics(Path(alamat_file))
    daftar_metrik.append({"brightness": b, "contrast": c, "edge_density": ed})

# Gabungkan hasil hitungan ke dalam tabel df_valid
df_metrik = pd.DataFrame(daftar_metrik, index=df_valid.index)
df_valid[["brightness", "contrast", "edge_density"]] = df_metrik

# Pengecekan otomatis (jangan diubah)
assert df_valid["brightness"].between(0, 255).all(), "Brightness harus di antara 0 dan 255"
assert (df_valid["contrast"] >= 0).all(), "Contrast tidak boleh negatif"
assert df_valid["edge_density"].between(0, 1).all(), "Edge density harus berupa proporsi 0.0 s.d. 1.0"

print("✅ Cek Langkah 5 lolos! Contoh hasil metrik pada 5 foto pertama:")
print(df_valid[["rel_path", "condition", "brightness", "contrast", "edge_density"]].head().to_string(index=False))
"""
            )
        )
        cells.append(
            md(
                """
<details>
<summary><b>💡 Hint & Jawaban Langkah 5</b> (klik untuk membuka)</summary>

**Penjelasan:**
- `np.mean(gray)` menghitung nilai rata-rata dari semua pixel (`brightness`).
- `np.std(gray)` menghitung simpangan baku dari semua pixel (`contrast`).
- `np.mean(edges > 0)` menghitung berapa bagian (proporsi `0.0–1.0`) pixel yang merupakan garis tepi putih (`> 0`).

**Jawaban:**
```python
brightness = float(np.mean(gray))
contrast = float(np.std(gray))
edges = cv2.Canny(gray, 100, 200)
edge_density = float(np.mean(edges > 0))
```
</details>
"""
            )
        )

    cells.append(
        md(
            """
### Langkah 5.3: Melihat Langsung Bedanya Foto *Latar Polos* vs *Latar Ramai* (Histogram, 3 Zona Cahaya & Canny Edges · Sesuai Slide 33–36)
Mengapa foto berlatar **Ramai** lebih menantang bagi AI? Mari kita ambil 1 contoh foto **Polos** dan 1 contoh foto **Ramai**, lalu bandingkan:
1. **Grafik Histogram (`65.536` piksel)** beserta sebaran **3 Zona Cahaya**: `Gelap (0–84)`, `Sedang (85–170)`, dan `Terang (171–255)`.
2. **Peta Garis Tepi (*Canny Edges*)** untuk melihat kepadatan garis latar belakang.
"""
        )
    )

    cells.append(
        code(
            """
# Ambil 1 baris contoh foto berlatar "polos" dan 1 baris contoh foto berlatar "ramai"
if (df_valid["condition"] == "polos").any():
    sample_polos = df_valid[df_valid["condition"] == "polos"].iloc[0]
else:
    sample_polos = df_valid.iloc[0]

if (df_valid["condition"] == "ramai").any():
    sample_ramai = df_valid[df_valid["condition"] == "ramai"].iloc[0]
else:
    sample_ramai = df_valid.iloc[-1]

# Buat kanvas gambar 2 baris x 3 kolom (Baris atas: Polos, Baris bawah: Ramai)
fig, axes = plt.subplots(2, 3, figsize=(13, 6.5))
pasangan_contoh = [("Latar Polos", sample_polos), ("Latar Ramai", sample_ramai)]

for nomor_baris, (judul_kondisi, data_foto) in enumerate(pasangan_contoh):
    # Buka foto, ubah ke grayscale, dan cari garis tepi Canny
    im_contoh = load_image_exif_safe(Path(data_foto["abs_path"]))
    gray_contoh = np.array(im_contoh.convert("L"))
    edges_contoh = cv2.Canny(gray_contoh, 100, 200)

    # Hitung persentase 3 Zona Cahaya (sesuai simulator Slide 33: Gelap 0-84, Sedang 85-170, Terang 171-255)
    pct_gelap = float(np.mean(gray_contoh <= 84) * 100)
    pct_sedang = float(np.mean((gray_contoh >= 85) & (gray_contoh <= 170)) * 100)
    pct_terang = float(np.mean(gray_contoh >= 171) * 100)
    print(f"{judul_kondisi:11s} ({Path(data_foto['rel_path']).name}) -> Gelap: {pct_gelap:4.1f}% | Sedang: {pct_sedang:4.1f}% | Terang: {pct_terang:4.1f}%")

    # Kolom 0: Tampilkan Foto Asli
    axes[nomor_baris, 0].imshow(im_contoh)
    axes[nomor_baris, 0].set_title(f"{judul_kondisi}: {Path(data_foto['rel_path']).name}")
    axes[nomor_baris, 0].axis("off")

    # Kolom 1: Tampilkan Grafik Histogram Sebaran Angka Pixel (0 s.d. 255)
    warna_grafik = "#4285F4" if nomor_baris == 0 else "#EA4335"
    axes[nomor_baris, 1].hist(gray_contoh.ravel(), bins=32, range=(0, 256), color=warna_grafik, alpha=0.85)
    axes[nomor_baris, 1].axvline(gray_contoh.mean(), color="#202124", linestyle="--", linewidth=1.8, label=f"Mean={gray_contoh.mean():.1f}")
    axes[nomor_baris, 1].set_title(f"Histogram (Mean={data_foto['brightness']:.1f}, Std={data_foto['contrast']:.1f})")
    axes[nomor_baris, 1].set_xlim(0, 255)
    axes[nomor_baris, 1].set_xlabel("Nilai Intensitas Pixel (0=Gelap s.d. 255=Terang)")
    axes[nomor_baris, 1].legend(loc="upper left")

    # Kolom 2: Tampilkan Peta Garis Tepi Canny
    axes[nomor_baris, 2].imshow(edges_contoh, cmap="gray")
    axes[nomor_baris, 2].set_title(f"Canny Edges (Edge Density = {data_foto['edge_density']*100:.2f}%)")
    axes[nomor_baris, 2].axis("off")

plt.tight_layout()
plt.show()
"""
        )
    )

    # =========================================================================
    # LANGKAH 6: ANALISIS POLOS VS RAMAI, SIMPAN AUDIT & MINI-CHALLENGE
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 6 (8 menit): Bandingkan *Polos vs Ramai* & Simpan Laporan Audit (Sesuai Slide 39 & 50)

Sebagai penutup sesi praktik, kita akan:
1. Merangkum rata-rata statistik seluruh foto **Polos vs Ramai** dalam sebuah tabel ringkasan.
2. Menggambar grafik **Boxplot** untuk membandingkan sebaran *Brightness*, *Contrast*, dan *Edge Density*.
3. Menyimpan tabel laporan audit (`CSV`) dan gambar grafik (`PNG`) ke dalam folder `results/`.

### Langkah 6.1: Membuat Tabel Ringkasan Statistik (*Polos vs Ramai*)
"""
        )
    )

    cells.append(
        code(
            """
# Kelompokkan foto berdasarkan kondisi latar ("polos" vs "ramai"),
# lalu hitung jumlah foto (count), nilai rata-rata (mean), dan simpangan baku (std)
summary = (
    df_valid.groupby("condition")[["brightness", "contrast", "edge_density"]]
    .agg(["count", "mean", "std"])
    .round(4)
)

print(f"=== TABEL RINGKASAN EDA: POLOS VS RAMAI ({DATA_LABEL}) ===")
print(summary)
"""
        )
    )

    cells.append(
        md(
            """
### Langkah 6.2: Menggambar Grafik *Boxplot* Perbandingan *Polos vs Ramai*
Grafik **Boxplot** membantu kita melihat perbedaan rentang nilai antara kumpulan foto berlatar **Polos** dan **Ramai** secara visual.
"""
        )
    )

    cells.append(
        code(
            """
# Siapkan kanvas dengan 3 grafik berjajar (Brightness, Contrast, Edge Density)
fig, axes = plt.subplots(1, 3, figsize=(13, 4))

daftar_kolom = [
    ("brightness", "1. Brightness (Rata-rata Terang 0–255)"),
    ("contrast", "2. Contrast (Simpangan Baku)"),
    ("edge_density", "3. Edge Density (Kepadatan Tepi Canny)"),
]

# Gambar masing-masing Boxplot satu per satu
for idx, (nama_kolom, judul_grafik) in enumerate(daftar_kolom):
    ax = axes[idx]

    # Pisahkan angka untuk kelompok latar 'polos' dan 'ramai'
    kelompok_angka = []
    nama_label = []
    for nama_kondisi, tabel_kelompok in df_valid.groupby("condition"):
        kelompok_angka.append(tabel_kelompok[nama_kolom].values)
        nama_label.append(nama_kondisi)

    # Gambar boxplot pada panel ke-idx
    ax.boxplot(kelompok_angka, tick_labels=nama_label)
    ax.set_title(judul_grafik)
    ax.set_xlabel("Kondisi Latar")
    ax.grid(axis="y", alpha=0.3)

fig.suptitle(f"Perbandingan Latar Polos vs Ramai ({DATA_LABEL})", fontsize=12, fontweight="bold")
plt.tight_layout()

# Simpan grafik ke dalam folder results/
plot_path = RESULTS_DIR / "p01_eda_polos_vs_ramai.png"
fig.savefig(plot_path, dpi=150)
plt.show()

print(f"Grafik berhasil disimpan ke: {plot_path}")
"""
        )
    )

    cells.append(
        md(
            """
### Langkah 6.3: Menyimpan Tabel Laporan Audit ke File CSV
Terakhir, kita simpan tabel hasil pemeriksaan seluruh foto (`p01_audit_metadata.csv`) dan tabel ringkasan statistik (`p01_eda_summary.csv`) ke folder `results/` agar siap digunakan pada sesi berikutnya.
"""
        )
    )

    cells.append(
        code(
            """
# Pilih kolom-kolom utama dari tabel audit
audit_cols = ["rel_path", "class", "condition", "width", "height", "is_valid", "is_duplicate", "sha256"]

# Gabungkan (merge) tabel audit dengan hasil hitungan brightness, contrast, dan edge_density
df_audit_out = df_audit[audit_cols].merge(
    df_valid[["rel_path", "brightness", "contrast", "edge_density"]],
    on="rel_path",
    how="left",
)

# Tentukan nama file CSV tujuan di dalam folder results/
audit_csv = RESULTS_DIR / "p01_audit_metadata.csv"
summary_csv = RESULTS_DIR / "p01_eda_summary.csv"

# Simpan kedua tabel ke file CSV
df_audit_out.to_csv(audit_csv, index=False)
summary.to_csv(summary_csv)

# Pastikan ketiga file hasil (2 CSV dan 1 PNG) benar-benar sudah tersimpan
assert audit_csv.exists() and summary_csv.exists() and plot_path.exists()

print("=== LAPORAN AUDIT BERHASIL DISIMPAN ===")
print(f"1. Tabel Audit Lengkap : {audit_csv}")
print(f"2. Tabel Ringkasan EDA : {summary_csv}")
print(f"3. Grafik Boxplot PNG  : {plot_path}")
print("✅ Seluruh langkah Hands-on P01 telah selesai!")
"""
        )
    )

    cells.append(
        md(
            """
### Mini-Challenge: Diskusi Kasus Polos vs Ramai (Sesuai Slide 50)
Diskusikan dan jawab 3 pertanyaan berikut berdasarkan hasil nyata EDA di atas:
1. Menurut Anda, kondisi mana yang akan lebih sulit ditebak oleh AI nantinya: **Polos** atau **Ramai**? Mengapa (kaitkan dengan angka *brightness* dan *edge density* di atas)?
2. Jika AI hanya kita latih dengan foto **Polos**, kira-kira apa yang terjadi saat ia diuji melihat foto **Ramai**?
3. Apa saran strategi penyiapan dataset agar AI bisa pintar mengenali objek di kedua kondisi sekaligus, serta bebas dari jebakan *corrupted files*, *EXIF orientation*, dan *duplicate data leakage*?

*(Catatan metodologi: EDA pada sesi ini bersifat deskriptif untuk memahami kesehatan koleksi foto sebelum digunakan melatih model AI).*
"""
        )
    )

    cells.append(
        md(
            """
## Referensi Belajar Mandiri (Video YouTube & Modul Berurutan · Slide 58–59)

Gunakan daftar referensi berikut secara berurutan untuk memperdalam konsep P01:

### Tahap 1 — Piksel, Array & NumPy
1. [3Blue1Brown — *But what is a neural network? (Ch. 1)*](https://www.youtube.com/watch?v=aircAruvnKk) *(menit 00:00–05:30: gambar sebagai grid angka piksel)*
2. [Keith Galli — *Complete Python NumPy Tutorial*](https://www.youtube.com/watch?v=GB9ByFAIAH4) *(indexing, `.shape`, `dtype`, `float32`)*

### Tahap 2 — AI Fundamental
3. [IBM Technology — *AI, Machine Learning, Deep Learning & GenAI Explained*](https://www.youtube.com/watch?v=qYNweeDHiyU)
4. [Simplilearn — *Deep Learning In 5 Minutes*](https://www.youtube.com/watch?v=6M5VXKLf4D4)
5. [Simplilearn — *What is Artificial Intelligence? (5 Minutes)*](https://www.youtube.com/watch?v=ad79nYk2keg) *(opsional)*

### Tahap 3 — Image Processing Praktis (`Pillow` & `OpenCV`)
6. [Corey Schafer — *Python Tutorial: Image Manipulation with Pillow*](https://www.youtube.com/watch?v=6Qs3w1uYujo)
7. [freeCodeCamp.org — *OpenCV Course - Full Tutorial with Python*](https://www.youtube.com/watch?v=oXlwWbU8l2o) · [Kode GitHub](https://github.com/jasmcaus/opencv-course)
8. [Murtaza's Workshop — *Learn OpenCV in 3 Hours with Python*](https://www.youtube.com/watch?v=WQeoO7MI0Bs)

### Tahap 4 — EDA Citra, Filter & Deteksi Tepi (`Canny`)
9. [Computerphile — *How Blurs & Filters Work*](https://www.youtube.com/watch?v=C_zFhWdM4ic)
10. [Computerphile — *Finding the Edges (Sobel Operator)*](https://www.youtube.com/watch?v=uihBwtPIBxM)
11. [Computerphile — *Canny Edge Detector*](https://www.youtube.com/watch?v=sRF9t8LqXW4) *(algoritma di balik `edge_density` polos vs ramai)*
12. [DigitalSreeni — *Python for Microscopists* (GitHub)](https://github.com/bnsreenu/python_for_microscopists)

### Tahap 5 — Kualitas Data, Class Imbalance & Anti-Data Leakage
13. [Coursera (DeepLearning.AI) — *Convolutional Neural Networks (Week 1)*](https://www.coursera.org/learn/convolutional-neural-networks)
14. [Kaggle Learn — *Data Leakage (Tutorial Interaktif)*](https://www.kaggle.com/code/alexisbcook/data-leakage)
15. [IBM — *What is Data Leakage in Machine Learning?*](https://www.ibm.com/topics/data-leakage)
"""
        )
    )

    return cells


def write_notebook(path: Path, is_solution: bool) -> None:
    cells = build_cells(is_solution=is_solution)
    path.parent.mkdir(parents=True, exist_ok=True)
    if nbf is not None:
        nb = nbf.v4.new_notebook()
        nb.metadata["kernelspec"] = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }
        nb.metadata["language_info"] = {"name": "python", "version": "3.11"}
        nb.cells = cells
        with open(path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
    else:
        nb_dict = {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python", "version": "3.11"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        path.write_text(json.dumps(nb_dict, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Written: {path} ({len(cells)} cells)")


def main() -> None:
    write_notebook(NB_STUDENT, is_solution=False)
    write_notebook(NB_SOLUTION, is_solution=True)


if __name__ == "__main__":
    main()
