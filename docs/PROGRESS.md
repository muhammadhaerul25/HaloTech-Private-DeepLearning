# PROGRESS.md — Disney Deep Learning Course

## P01 — Understanding Images, Image Processing & EDA

### 1. Status Implementasi
- **Status:** **FINAL & SIAP DIGUNAKAN** untuk **P01** (pertemuan pembuka berdurasi 120 menit).
- **Aturan Sinkronisasi Utama (Single Source of Truth):** Ke-4 komponen utama per pertemuan berada dalam satu folder `materials/P01/`. File **HTML (`materials/P01/P01_understanding_images_processing_eda.html`) adalah sumber utama (main source)**. Setiap perubahan pada HTML wajib diikuti dengan pembaruan **PDF (`materials/P01/P01_understanding_images_processing_eda.pdf`)**, **Notebook (`materials/P01/P01_understanding_images_processing_eda.ipynb` & `solutions/`)**, dan **PPTX (`materials/P01/P01_understanding_images_processing_eda.pptx`)**.
- **Kebijakan Tampilan Waktu:** Seluruh materi (cover slide, PPTX, HTML interaktif, PDF, notebook, dan halaman web portal) bersifat *timeless* — **tidak mencantumkan tanggal, hari, maupun jam sesi (`datetime`)**.

### 2. Struktur & File Utama
- `docs/PLAN.md`, `docs/PROMPT_MASTER.md`, `docs/PROGRESS.md`, `docs/references/` — kurikulum, prompt master, catatan progres, dan referensi slide.
- `tools/slide_theme.py` — tema presentasi terinspirasi gaya konferensi Google I/O.
- `tools/make_sample_data.py` — generator dataset sintetis deterministik (`SEED=42`) di `data/sample/` (120 foto + `metadata.csv`) serta dataset asli **MNIST** di `data/mnist/` (`mnist.npz` penuh, 100 file `.png` asli `28×28` untuk kelas `0` s.d. `9`, 4 file `.png` variasi gaya tulisan tangan di `data/mnist/variants/`, `mnist_samples.json`, dan `metadata.csv`).
- `tools/build_slides_P01.py` — generator visualisasi Matplotlib/OpenCV (`materials/P01/assets/P01/`, termasuk `11_rgb_screen_display.png`, `12_color_channels_overview.png` & `mnist_grid_demo.png`) dan dek PPTX 29 slide (termasuk studi kasus asli MNIST `28×28`, visualisasi sub-pixel layar HP, pengantar visual Color Channels `1/3/4/5+`, 3 slide AI Fundamental, & 2 slide Referensi Belajar Mandiri).
- `tools/build_html_slides_P01.py` — generator dek presentasi web interaktif 59 slide (termasuk simulator Slide 08 default `Apel Merah + 1. Mata Manusia`, simulator interaktif 3 tahap layar HP Slide 09, Persistent Session Timer kanan atas slide, simulator interaktif MNIST `28×28` asli, 3 slide interaktif AI Fundamental di Bab 2 dengan pembanding variasi MNIST `'7'`, simulator interaktif Histogram Gelap/Silau Slide 33, simulator interaktif Brightness vs Contrast Slide 34, & 2 slide Referensi Video/Sumber Belajar) + PWA (`index.html`, `manifest.webmanifest`, `sw.js`).
- `tools/export_pdf_P01.py` — ekspor PDF vektor & gambar resolusi penuh via Chrome Headless (`80` halaman: `59` slide + ekspansi seluruh tab/kondisi interaktif AI Fundamental Slide 20–22 termasuk MNIST `'7'` + ekspansi 3 kondisi Histogram Slide 33 `Normal/Gelap/Silau` + ekspansi 4 kondisi Brightness/Contrast Slide 34 `Normal/Kontras Rendah/Kontras Tinggi/Gelap` + `9` pasang Q&A/kuis yang dipisah antara pertanyaan & jawaban).
- `tools/build_presenter_script_P01.py` — generator PDF Naskah & Poin Penjelasan Presentasi per Slide (`materials/P01/P01_presenter_script.pdf`), memecah seluruh `59` slide satu per satu lengkap dengan fokus utama, poin-poin penjelasan, panduan klik aksi interaktif/demo, kunci jawaban Q&A/kuis, serta kalimat transisi.
- `tools/build_notebooks_P01.py` — generator notebook peserta (`66` sel ramah pemula / *cell-by-cell breakdown* dengan komentar baris demi baris, 9 latihan `# TODO` terpisah + 9 sel `<details>` Hint & Jawaban + pengait Slide 08–13 + eksplorasi MNIST `28×28` + pembuktian kode AI Fundamental + daftar referensi belajar selaras Slide 50 & 58–59) dan notebook kunci jawaban (`57` sel).
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
- **HTML Slides (`materials/P01/P01_understanding_images_processing_eda.html`):** 59 slide (termasuk simulator Slide 08 default `Apel Merah + 1. Mata Manusia`, simulator interaktif 3 tahap layar HP Slide 09, simulator interaktif kerapatan pixel `4×4` s.d. `64×64` Slide 10, pengantar jenis Color Channels `1/3/4/5+` dengan ilustrasi contoh tiap channel di Slide 11, simulator interaktif MNIST `28×28` di Slide 13 dengan default angka `0` + mode `1. Gambar Tulisan`, fokus RGB di Slide 14–18, simulator AI Fundamental 1/3 Slide 20 default `1. Program Biasa` dengan pembeda visual tegas **Manusia vs Mesin (ML vs DL)**, AI Fundamental 2/3 Slide 21 default `1. Tengah` beserta MNIST `'7'`, AI Fundamental 3/3 Slide 22 berpanah ringkas, penomoran terarah **Issue #1–#3** pada Bab 3 EDA Slide 30–39 termasuk **simulator interaktif Histogram Gelap/Silau di Slide 33** dan **simulator interaktif Brightness vs Contrast + Boxplot 119 foto di Slide 34**, Persistent Session Timer di kanan atas slide, QA #3 di Slide 26, & 2 slide Referensi Belajar Mandiri), total speaker notes 120.0 menit, PWA cache `sw.js` (`dl-course-pwa-v5`).
- **PDF (`materials/P01/P01_understanding_images_processing_eda.pdf`):** 80 halaman (`16:9`), mencakup seluruh 59 slide + ekspansi seluruh state interaktif AI Fundamental (termasuk tab MNIST `'7'`), 3 state simulator Histogram Slide 33, 4 state simulator Brightness & Contrast Slide 34, + 9 pasang halaman Q&A/kuis terpisah.
- **PPTX (`materials/P01/P01_understanding_images_processing_eda.pptx`):** 80 slide (`16:9`, `2240×1260` 2× Retina HD, `16.11 MB`), diekspor langsung dari HTML sehingga **100% identik secara visual dan urutan halaman dengan HTML & PDF** (mencakup seluruh 59 slide + ekspansi tab AI Fundamental Slide 20–22, 3 state simulator Histogram Slide 33, 4 state simulator Brightness & Contrast Slide 34, serta 9 pasang halaman Q&A/Kuis), lengkap dengan *Speaker Notes* detail di seluruh 80 slide (`80/80`).
- **Notebook Kunci (`materials/P01/solutions/P01_understanding_images_processing_eda.ipynb`):** 59 sel (*cell-by-cell* ultra ramah awam, 5–15 baris per sel tanpa nested loop / merge rumit), seluruh 28 sel kode & `assert` lolos dieksekusi dengan `SMOKE_TEST=1` (termasuk Setup 3 tahap, Langkah 1 selaras Slide 08–13, eksplorasi dataset asli MNIST `28×28` selaras Slide 13, pemisahan RGB & Grayscale terpisah di Langkah 2, demo kode AI Fundamental & Letterbox `ImageOps.pad` + Normalization di Langkah 3 selaras Slide 20–29, 3 fungsi penyaring kamera HP terpisah di Langkah 4, EDA di Langkah 5, ekspor CSV/Boxplot & Mini-Challenge Slide 50 di Langkah 6, serta Referensi Slide 58–59).
- **Notebook Peserta (`materials/P01/P01_understanding_images_processing_eda.ipynb`):** 68 sel (*cell-by-cell* ultra ramah awam), 9 sel latihan `# TODO` terfokus (`1`, `2A`, `2B`, `3A`, `3B`, `4A`, `4B`, `4C`, `5`) + 9 `<details>` Hint & Jawaban, berjalan bersih 7 sel kode awal hingga sebelum sel `# TODO` pertama (`SMOKE_TEST=1`), selaras penuh dengan slide HTML/PDF/PPTX (`Slide 08–13`, `Slide 20–29`, `Slide 50`, `Slide 58–59`).

### 5. Catatan Font PPTX
- Font PPTX: `Poppins` (judul), `Roboto` (isi), `Roboto Mono` (kode/tag). Pasang ketiga font tersebut di komputer penyaji agar rendering PowerPoint/LibreOffice sesuai desain (tanpa fallback ke `Arial`).


---

## Standarisasi Arsitektur & Pipeline Materi (P01 → P02–P08)

### 1. Dokumen Standar & Penyelarasan Aturan
- **`docs/STANDAR_MATERI.md`** — SOP resmi penyusunan materi (HTML SSOT → PDF 16:9 + PPTX 16:9 HD 2× + Presenter Script PDF A4 + Notebook cell-by-cell + 6 Gerbang Validasi DoD + Registrasi Portal/PWA).
- **`AGENTS.md`** — Diselaraskan penuh dengan standar final P01 (penomoran aktif `P01–P08`, kebijakan *timeless*, HTML SSOT, `tools/core/`, `tools/build_session.py P{NN} --validate`).

### 2. Shared Engine Reusable (`tools/core/`) & CLI
- `tools/core/registry.py` — Registri metadata resmi sesi `P01–P08` (slug URL, slug file, fase, warna aksen, path output baku).
- `tools/core/html_shell.py` — Shell HTML5 standar (tema Google I/O, Slide Player Engine, keyboard shortcuts, Persistent Session Timer ber-namespace per sesi, Q&A/Quiz reveal, `@media print`, auto-numbering dinamis, serta helper pembatas bab & agenda).
- `tools/core/exporter.py` — Mesin ekspor generik berbasis Chrome Headless & Chrome CDP:
  - `export_pdf()` — PDF vektor `16:9` dengan dukungan kontrak deklaratif `window.SLIDE_PDF_EXPANDERS` + pemisahan otomatis Q&A/Kuis (Pertanyaan → Jawaban).
  - `export_pptx()` — PPTX `16:9` Retina HD (`2240×1260`) 100% identik PDF/HTML + Speaker Notes detail (`data-notes` + `SLIDE_EXPLANATIONS`).
  - `export_presenter_script()` — Naskah Pengajar A4 Portrait (1 slide dasar HTML = 1 halaman).
- `tools/core/notebook_builder.py` — Helper standar notebook *cell-by-cell* (Setup 3 tahap, Colab/Lokal, `SEED=42`, `SMOKE_TEST`, pasangan `# TODO` + `<details>` Hint & Jawaban).
- `tools/core/validator.py` — Validator 6 Gerbang DoD (HTML, Paritas PDF/PPTX, Presenter Script, Eksekusi Notebook Solusi & Peserta `SMOKE_TEST=1`, dan sinkronisasi Portal/PWA).
- `tools/build_session.py` — Orkestrator CLI tunggal (`python tools/build_session.py P{NN} --validate`).
- `tools/init_session.py` — Scaffolder otomatis kerangka sesi baru (`tools/sessions/P{NN}/` & `materials/P{NN}/`).

### 3. Uji Regresi P01 & Scaffold P02
- Perbaikan minor P01: angka counter `#page-jump` & judul HTML (`build_html_slides_P01.py`) kini otomatis sinkron dinamis (`59` slide, menggantikan sisa teks `60`).
- **Hasil Validasi 6 Gerbang P01 (`.venv\Scripts\python.exe tools/build_session.py P01 --validate-only`):** **PASSED 100%**
  - HTML: `59` slide, `28` aset lokal valid, `120.0` menit total `data-notes`, `timeless_ok = true`.
  - PDF & PPTX: `80` halaman PDF === `80` slide PPTX (`16:9`), Speaker Notes `80/80`.
  - Presenter Script: `59` halaman, `SLIDE_EXPLANATIONS` mencakup `59/59`.
  - Notebooks (`SMOKE_TEST=1`): Solusi (`59` sel) dieksekusi penuh **0 error**, Peserta (`68` sel, `9` `# TODO` === `9` `<details>` Hint) berjalan bersih hingga sebelum `# TODO` pertama.
  - Portal & PWA: `sessions.json`, `vercel.json`, dan `sw.js` terverifikasi sinkron.
- **Scaffold P02:** Kerangka `tools/sessions/P02/` (`build_assets.py`, `build_html.py`, `build_notebooks.py`, `presenter_notes.py`) dan folder `materials/P02/` telah dibuat dan siap diisi konten penuh P02 (*Teori Neural Network / ANN*).

### 4. Catatan Keputusan Arsitektur
- Kurikulum portal aktif tetap **P01–P08** (ekstensibel di `tools/core/registry.py` bila kelak ingin menambah slot P09 untuk Demo & Laporan).
- **PPTX HD Mirror dari HTML via Chrome CDP** ditetapkan sebagai standar permanen P02 dst.
- Skrip P01 eksisting dipertahankan agar tampilan final P01 tidak berubah, sambil terhubung penuh ke `tools/build_session.py` dan `tools/core/validator.py`.


---

## Dataset Proyek Utama (`data/frozen_v1/`) — Siap untuk P02–P08

- **Sumber Mentah (di-ignore Git via `data/*.zip`):** `data/dataset _frozen_v1.zip` (`166.63 MB`, 143 file `.HEIC` dari Apple iPhone 15 Pro Max di 1 folder datar `Frozen 1/`).
- **Skrip Konversi Deterministik:** `tools/prepare_frozen_dataset.py` (membutuhkan `pillow-heif`, sudah ditambahkan ke `requirements.txt`).
- **Hasil Konversi Siap Repo & Colab (`data/frozen_v1/`):**
  - **Total file:** `143` JPEG valid (`0` rusak, `0` duplikat SHA-256), ukuran total hanya **`9.66 MB`** (~17× lebih ringan dari arsip HEIC mentah), resolusi proporsional **`576 × 768`** (`3:4` portrait, EXIF terkoreksi).
  - **5 Kelas (`CLASS_NAMES`):** `anna` (`28`), `elsa` (`29`), `kristoff` (`28`), `olaf` (`28`), `sven` (`30`).
  - **2 Kondisi (`polos` vs `ramai`, 4 `sub_kondisi`, 7 `sesi_foto`):**
    - `polos` (`n = 102`, 71.3%): `mean_brightness = 143.44 ± 26.95`, `mean_contrast = 36.06`, `mean_edge_density = 0.0434` (`576×768`).
    - `ramai` (`n = 41`, 28.7%): `mean_brightness = 116.81 ± 27.04`, `mean_contrast = 45.92`, `mean_edge_density = 0.0535` (`576×768`).
  - **Artefak Metadata:** `data/frozen_v1/metadata.csv` & `data/frozen_v1/dataset_summary.json` (dibaca dinamis oleh seluruh slide & notebook mulai P02 dst. agar tetap aman saat foto ditambah di versi berikutnya).
- **Kebijakan Penggunaan Visual:** Disetujui peserta untuk di-commit ke repo dan dipakai langsung sebagai contoh gambar nyata di slide HTML/PDF/PPTX dan notebook P02–P08.


---

## P02 — Teori Neural Network (ANN)

### 1. Status Implementasi
- **Status:** **FINAL & SIAP DIGUNAKAN** untuk **P02** (dibangun 100% memakai arsitektur standar `tools/core/` + dataset proyek nyata `data/frozen_v1/`).
- **Transisi P01 → P02 → P03:** Dimulai dari titik akhir P01 (matriks piksel `0.0–1.0`) + perkenalan langsung galeri 5 karakter **Disney Frozen** (`anna, elsa, kristoff, olaf, sven`, `polos` vs `ramai`), naik bertahap dari 1 neuron → MLP `28×28` → eksperimen *Flatten* foto Frozen (`>19,2 juta` bobot di 1 layer) sebagai jembatan alami menuju **P03 (CNN Fundamentals)**.

### 2. Struktur File & Artefak P02
- **Kode Sumber Modular (`tools/sessions/P02/`):**
  - `build_assets.py` — menghasilkan 8 thumbnail foto Frozen nyata (`thumb_*.jpg`), 5 grafik Matplotlib (`01_frozen_gallery_5classes.png` s.d. `05_flatten_frozen_visual.png`), serta `p02_data.json` dinamis dari `data/frozen_v1/`.
  - `build_html.py` — dek HTML5 interaktif 59 slide memakai `tools/core/html_shell.py`, dengan **6 simulator interaktif** terdaftar di `window.SLIDE_PDF_EXPANDERS` (Kalkulator 1 Neuron Frozen dengan kondisi AKTIF Elsa & TIDAK AKTIF Anna, Lab Aktivasi `ReLU/Sigmoid/Tanh`, Simulator `Softmax` 5 Karakter Frozen, Simulasi `Gradient Descent` & `Learning Rate`, Evaluasi Kurva `Loss` Train vs Val, dan Kalkulator Ledakan Bobot `Flatten`).
  - `presenter_notes.py` — `SLIDE_EXPLANATIONS` lengkap & mendalam (4–5 poin terstruktur per slide: Tujuan, Naskah/Panduan Demo, Interaksi/Sorotan Visual, Transisi) untuk seluruh `59` slide.
  - `build_notebooks.py` — notebook peserta & kunci jawaban *cell-by-cell* memakai `tools/core/notebook_builder.py`.
- **Keluaran Tervalidasi (`materials/P02/`, Final — Istilah Asli + Penjelasan Sederhana + Audit 80 Halaman):**
  - `materials/P02/P02_neural_network_ann.html` — **59 slide** (`120.0` menit exact `data-notes`, `timeless_ok = true`, `29` aset lokal valid, istilah teknis asli dengan penjelasan sederhana, serta **Slide 58–59 Referensi Belajar Mandiri berisi 16 kartu video YouTube/dokumentasi klik-langsung terverifikasi + Rute Maraton ±2 Jam** setara P01).
  - `materials/P02/P02_neural_network_ann.pdf` — **80 halaman** (`16:9`, `9.54 MB`), ekspansi penuh 6 simulator + pemisahan Pertanyaan → Jawaban pada seluruh Q&A, Mini-Challenge, & Kuis; 0 tumpang-tindih teks/SVG/kanvas.
  - `materials/P02/P02_neural_network_ann.pptx` — **80 slide** (`16:9` Retina HD `2240×1260`, `13.74 MB`), 100% identik HTML/PDF + Speaker Notes detail di seluruh `80/80` slide.
  - `materials/P02/P02_presenter_script.pdf` — **59 halaman** A4 Portrait (`8.28 MB`), 1 slide = 1 halaman (`59/59` naskah pengajar detail tercakup).
  - `materials/P02/P02_neural_network_ann.ipynb` — Notebook peserta (`52` sel, `8` `# TODO` === `8` `<details>` Hint & Jawaban, seluruh rujukan nomor slide tersinkron penuh ke 59 slide termasuk Sel 50 → Slide 49).
  - `materials/P02/solutions/P02_neural_network_ann.ipynb` — Notebook kunci (`44` sel), lolos eksekusi nyata TensorFlow 2.21 / Keras 3.15 dengan `SMOKE_TEST=1` (termasuk training MLP pada `data/frozen_v1/` & ekspor `results/p02_lr_activation_compare.png` dan `results/p02_mlp_parameter_comparison.csv`).

### 3. Hasil Validasi 6 Gerbang DoD & Integrasi Portal/PWA
- **Perintah:** `.venv\Scripts\python.exe tools/build_session.py P02 --validate` → **PASSED 100%** (termasuk verifikasi visual lembar kontak seluruh slide terdampak & Presenter Script A4).
- **Aturan Gaya Baru (dicatat di `AGENTS.md` untuk P02–P08):** Selalu pakai istilah teknis asli (*Neuron, Layer, ReLU, Softmax, Conv2D, Feature Map*, dll.) tanpa julukan rekaan, lalu sederhanakan penjelasannya dengan bahasa Indonesia sehari-hari.
- **Portal & PWA:** `sessions.json` (`P02` berstatus `available` + 5 tautan lengkap), `vercel.json` (rewrite `/p2` & `/p02`), `sw.js` (`dl-course-pwa-v6` + precache HTML P02), dan `requirements.txt` (`tensorflow>=2.16.0`) telah diperbarui.
