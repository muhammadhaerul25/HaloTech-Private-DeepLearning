# PROGRESS.md — Disney Deep Learning Course

## P01 — Understanding Images, Image Processing & EDA

### 1. Status Implementasi
- **Status:** **FINAL & SIAP DIGUNAKAN** untuk **P01** (pertemuan pembuka berdurasi 120 menit).
- **Aturan Sinkronisasi Utama (Single Source of Truth):** Ke-4 komponen utama per pertemuan berada dalam satu folder `materials/P01/`. File **HTML (`materials/P01/P01_image_processing_eda.html`) adalah sumber utama (main source)**. Setiap perubahan pada HTML wajib diikuti dengan pembaruan **PDF (`materials/P01/P01_image_processing_eda.pdf`)**, **Notebook (`materials/P01/P01_image_processing_eda.ipynb` & `solutions/`)**, dan **PPTX (`materials/P01/P01_image_processing_eda.pptx`)**.
- **Kebijakan Tampilan Waktu:** Seluruh materi (cover slide, PPTX, HTML interaktif, PDF, notebook, dan halaman web portal) bersifat *timeless* — **tidak mencantumkan tanggal, hari, maupun jam sesi (`datetime`)**.

### 2. Struktur & File Utama
- `docs/PLAN.md`, `docs/PROMPT_MASTER.md`, `docs/PROGRESS.md`, `docs/references/` — kurikulum, prompt master, catatan progres, dan referensi slide.
- `tools/slide_theme.py` — tema presentasi terinspirasi gaya konferensi Google I/O.
- `tools/make_sample_data.py` — generator dataset sintetis deterministik (`SEED=42`) di `data/sample/` (120 foto + `metadata.csv`).
- `tools/build_slides_P01.py` — generator visualisasi Matplotlib/OpenCV (`materials/P01/assets/P01/`) dan dek PPTX 28 slide (termasuk studi kasus asli MNIST `28×28`, 3 slide AI Fundamental, & 2 slide Referensi Belajar Mandiri).
- `tools/build_html_slides_P01.py` — generator dek presentasi web interaktif 60 slide (termasuk simulator interaktif MNIST `28×28` asli, 3 slide interaktif AI Fundamental di Bab 2 dengan pembanding variasi MNIST `'7'`, & 2 slide Referensi Video/Sumber Belajar) + PWA (`index.html`, `manifest.webmanifest`, `sw.js`).
- `tools/export_pdf_P01.py` — ekspor PDF vektor & gambar resolusi penuh via Chrome Headless (`76` halaman: `60` slide + ekspansi seluruh tab/kondisi interaktif AI Fundamental Slide 20–22 termasuk MNIST `'7'` + `9` pasang Q&A/kuis yang dipisah antara pertanyaan & jawaban).
- `tools/build_notebooks_P01.py` — generator notebook peserta (`29` sel, 5 `# TODO` + 5 sel `<details>` Hint & Jawaban + eksplorasi MNIST `28×28` + pembuktian kode AI Fundamental + daftar referensi belajar) dan notebook kunci jawaban (`24` sel).
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
- **HTML Slides (`materials/P01/P01_image_processing_eda.html`):** 60 slide (termasuk simulator interaktif MNIST `28×28` di Slide 12, pembanding variasi tulisan tangan MNIST `'7'` di Slide 21 AI Fundamental 2/3, & 2 slide Referensi Belajar Mandiri), 44 elemen gambar valid, total speaker notes 120.0 menit, PWA cache `sw.js`.
- **PDF (`materials/P01/P01_image_processing_eda.pdf`):** 76 halaman (`16:9`, `12.69 MB`), mencakup seluruh 60 slide + ekspansi seluruh state interaktif AI Fundamental (termasuk tab MNIST `'7'`) + 9 pasang halaman Q&A/kuis terpisah.
- **PPTX (`materials/P01/P01_image_processing_eda.pptx`):** 28 slide (termasuk Slide 07 studi kasus MNIST `28×28`, 3 slide AI Fundamental, 6 langkah Hands-on selaras notebook, & 2 slide Referensi Belajar bertautan aktif), seluruhnya memiliki speaker notes (`28/28`, total `120.0 menit`).
- **Notebook Kunci (`materials/P01/solutions/P01_image_processing_eda.ipynb`):** 24 sel (termasuk eksplorasi dataset asli MNIST `28×28`, demo kode AI Fundamental di Langkah 3, serta daftar referensi video/modul berurutan).
- **Notebook Peserta (`materials/P01/P01_image_processing_eda.ipynb`):** 29 sel, 5 `# TODO` + 5 `<details>` Hint & Jawaban, selaras penuh dengan slide HTML/PDF/PPTX.

### 5. Catatan Font PPTX
- Font PPTX: `Poppins` (judul), `Roboto` (isi), `Roboto Mono` (kode/tag). Pasang ketiga font tersebut di komputer penyaji agar rendering PowerPoint/LibreOffice sesuai desain (tanpa fallback ke `Arial`).
