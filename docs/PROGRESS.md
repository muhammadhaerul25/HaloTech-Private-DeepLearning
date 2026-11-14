# PROGRESS.md — Disney Deep Learning Course

## P01 — Understanding Images, Image Processing & EDA

### 1. Status Implementasi
- **Status:** **FINAL & SIAP DIGUNAKAN** untuk **P01** (pertemuan pembuka berdurasi 120 menit).
- **Tanggal:** 14 November 2026.

### 2. Struktur & File Utama
- `docs/PLAN.md`, `docs/PROMPT_MASTER.md`, `docs/PROGRESS.md` — kurikulum, prompt master, dan catatan progres.
- `tools/slide_theme.py` — tema presentasi terinspirasi gaya konferensi Google I/O.
- `tools/make_sample_data.py` — generator dataset sintetis deterministik (`SEED=42`) di `data/sample/` (120 foto + `metadata.csv`).
- `tools/build_slides_P01.py` — generator visualisasi Matplotlib/OpenCV (`slides/assets/P01/`) dan dek PPTX 22 slide.
- `tools/build_html_slides_P01.py` — generator dek presentasi web interaktif 54 slide + PWA (`index.html`, `manifest.webmanifest`, `sw.js`).
- `tools/export_pdf_P01.py` — ekspor PDF vektor & gambar resolusi penuh via Playwright Chromium (`63` halaman: `54` slide + `9` pasang Q&A/kuis yang dipisah antara pertanyaan & jawaban).
- `tools/build_notebooks_P01.py` — generator notebook peserta (`25` sel, 5 `# TODO` + 5 sel `<details>` Hint & Jawaban) dan notebook kunci jawaban (`20` sel).
- `tools/sync_materials.py` — penyinkron paket siap pakai ke `Materials/P01 - Understanding Images, Image Processing & EDA/`.
- `tools/build_all.py` — orkestrator 1 perintah untuk menjalankan seluruh pipeline build P01.

### 3. Hasil Generasi Dataset Sampel (`data/sample/`)
- **Total file:** 120 file JPEG (5 kelas geometris: `lingkaran`, `persegi`, `segitiga`, `bintang`, `heksagon` × 2 kondisi: `polos`, `ramai` × 12 foto per kombinasi, ukuran `256 × 256`) + `metadata.csv`.
- **Kasus khusus terverifikasi:**
  - 1 file rusak (`segitiga/ramai/segitiga_ramai_12.jpg`, gagal `Image.verify()`).
  - 2 file duplikat identik SHA-256 (`lingkaran/polos/lingkaran_polos_01.jpg` dan `lingkaran/polos/lingkaran_polos_02.jpg`).
  - 2 file dengan tag EXIF `Orientation = 6` (`persegi/polos/persegi_polos_01.jpg` dan `bintang/ramai/bintang_ramai_01.jpg`).
- **Statistik terhitung dari 119 foto valid (Contoh data sampel):**
  - `polos` (n=60): rata-rata brightness = `228.11`, rata-rata contrast (std) = `45.21`, rata-rata edge density (Canny) = `0.0121`.
  - `ramai` (n=59): rata-rata brightness = `127.21`, rata-rata contrast (std) = `54.69`, rata-rata edge density (Canny) = `0.0853`.

### 4. Hasil Validasi Terakhir
- **HTML Slides (`slides/P01_image_processing_eda.html`):** 54 slide, 9 gambar valid, total speaker notes 120.0 menit, PWA cache `sw.js` (14 aset, 0 missing).
- **PDF (`slides/P01_image_processing_eda.pdf`):** 63 halaman (`960 × 540 pt`, rasio 16:9, `6.37 MB`), cover & Q&A split diverifikasi secara visual.
- **PPTX (`slides/P01_image_processing_eda.pptx`):** 22 slide, seluruhnya memiliki speaker notes (`22/22`).
- **Notebook Kunci (`notebooks/solutions/P01_image_processing_eda.ipynb`):** dieksekusi penuh dengan `SMOKE_TEST=1` via `nbconvert --execute`, 10/10 sel kode lolos tanpa error.
- **Notebook Peserta (`notebooks/P01_image_processing_eda.ipynb`):** 25 sel, 5 `# TODO` + 5 `<details>` Hint & Jawaban, sel pra-TODO berjalan tanpa error.
- **Paket `Materials/P01 - Understanding Images, Image Processing & EDA/`:** 140 file lengkap (HTML, PDF, PPTX, Notebook Peserta & Solusi, `assets/P01/`, dan `data/sample/`).

### 5. Catatan Font PPTX
- Font PPTX: `Poppins` (judul), `Roboto` (isi), `Roboto Mono` (kode/tag). Pasang ketiga font tersebut di komputer penyaji agar rendering PowerPoint/LibreOffice sesuai desain (tanpa fallback ke `Arial`).
