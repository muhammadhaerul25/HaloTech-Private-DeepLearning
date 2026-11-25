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


---

## Redesign P02 → Computer Vision 101 (Aktif)

### 1. Keputusan Redesign & Usulan Perubahan `docs/PLAN.md` (Tanpa Mengedit `PLAN.md`)
- **Alasan:** Menata ulang P02 menjadi **Computer Vision 101** dengan alur besar → kecil → membangun ulang dari bawah (*AI vs ML vs DL → 4 Task Computer Vision → Bedah Neural Network dari 1 Neuron sampai MLP, Forward Pass, & Intuisi Training → Teaser Arsitektur CV*).
- **Pengarsipan Materi Lama:** Kode sumber P02 lama (*Teori Neural Network / ANN*) diarsipkan di `tools/sessions/_archive_P02_ann/` agar detail aktivasi (`ReLU/Sigmoid/Tanh`), `Loss`, `Learning Rate`, dan `Overfitting` dapat dipakai ulang saat menyusun **P03**.
- **Usulan Perubahan Kurikulum (`PLAN.md` tidak diubah langsung):**
  - **P02** menjadi *Computer Vision 101* (`P02_computer_vision_101.*`), mencakup Bab 1 (AI/ML/DL), Bab 2 (Classification, Object Detection, Instance Segmentation + beda singkat Semantic, Object Tracking), Bab 3 (Neuron → Input Layer `H×W×C` → Output Layer → 1 Neuron Input ke 5 Output → Hidden Layer → Forward Pass 4 piksel nyata Elsa → Loss/Gradient Descent/Backprop intuitif), Bab 4 (Teaser MLP → CNN → ResNet → MobileNetV2), Bab 5 (Hands-On MLP kecil + Mini-Challenge + Kamus + Kuis 5 soal).
  - **P03** diusulkan menjadi *Training Neural Network & Konvolusi (CNN)* — fokus pada pendalaman training (aktivasi, loss, learning rate, overfitting) dan konvolusi 2D (kernel, stride, padding, pooling, feature map), tanpa mengulang Task CV yang sudah tuntas di P02. Deskripsi P03 di `sessions.json` dan `tools/core/registry.py` telah diselaraskan.

### 2. Artefak Terbangun (`materials/P02/` & `tools/sessions/P02/`)
- **Aset Visual & Data Nyata (`materials/P02/assets/P02/`):** 8 thumbnail foto Frozen nyata (`thumb_*.jpg`), 11 grafik deterministik (`01_frozen_gallery_5classes.png` s.d. `06_mlp_vs_cnn_preview.png`, termasuk siluet *mask* OpenCV Bab 2, `03a_one_pixel_one_neuron.png` zoom piksel `8×8` Elsa → 1 Neuron, serta `03_flatten_frozen_visual.png` dengan kapsul lingkaran Neuron `x₁..x₁₅₀₅₂₈`), dan `p02_data.json` dinamis dari `data/frozen_v1/` (`143` foto, `102` polos, `41` ramai, 9 piksel `3×3` Elsa untuk animasi Flatten, dan 4 piksel `2×2` Elsa untuk Forward Pass).
- **Dek HTML5 SSOT:** `materials/P02/P02_computer_vision_101.html` — **57 slide** (Cover kolase Bento 1+4 lima karakter asli Frozen, Slide 02 gabungan *Agenda & Learning Goals*, Bab 1 dilengkapi *AI vs Bukan AI* & *ML Klasik vs Deep Learning*, Bab 2 diperbarui menjadi peta 4-panel + *Semantic and Instance Segmentation* + visual nyata Elsa/Olaf + ekspansi Latihan Slide 17, Bab 3 dibuka dengan alur mulus **Slide 20 (1 Piksel → 1 Neuron) → Slide 21 (Animasi Motion 60fps Interaktif `Flatten` 9 piksel nyata Elsa dari kiri→kanan, atas→bawah → `Input Layer`) → Slide 22 (`Input Layer` RGB `H×W×C`) → Slide 23 (Skala Nyata `150.528` Neuron)**), `10` simulator/animasi interaktif (`8` terdaftar di `window.SLIDE_PDF_EXPANDERS`), `6` Q&A Reveal, `1` Kuis 5 Soal Reveal, total `data-notes` = **`120.0` menit**, `timeless_ok = true`, `39` aset lokal terverifikasi, seluruh tautan referensi berasal dari `docs/PLAN.md` (sumber belum diverifikasi berlabel `[CEK LINK]`).
- **Ekspor Sinkron:**
  - `materials/P02/P02_computer_vision_101.pdf` — **79 halaman** (`16:9`, `10.88 MB`, termasuk 2 frame animasi Flatten: *mid-flight* & *9/9 selesai*).
  - `materials/P02/P02_computer_vision_101.pptx` — **79 slide** (`16:9` Retina HD `2240×1260`, `15.53 MB`), Speaker Notes **`79/79`**.
  - `materials/P02/P02_presenter_script.pdf` — **57 halaman** A4 Portrait (`9.19 MB`), `SLIDE_EXPLANATIONS` mencakup **`57/57`**.
- **Notebook Hands-On:**
  - `materials/P02/P02_computer_vision_101.ipynb` — Peserta (`47` sel, `8` `# TODO` === `8` `<details>` Hint & Jawaban, rujukan slide tersinkron ke `57` slide).
  - `materials/P02/solutions/P02_computer_vision_101.ipynb` — Kunci (`39` sel, `0` `# TODO`, seluruh `17` sel kode lolos AST syntax check & sel NumPy/dataset Langkah 1–3 lolos seluruh `assert`).
- **Portal & PWA:** `tools/core/registry.py`, `sessions.json` (`P02` + deskripsi `P03`), `vercel.json` (`/p2` & `/p02`), dan `sw.js` (`dl-course-pwa-v7`) telah diperbarui dan terverifikasi sinkron. `tools/core/validator.py` diperbarui memakai `python -m nbconvert` agar tidak bergantung pada `jupyter-nbconvert.exe` di PATH Windows.

### 3. Status Validasi & Pembaruan Interaktif Bab 3 (56 Slide — Terverifikasi Penuh)
- **Peningkatan Visual & Animasi Interaktif Bab 3:**
  - **Slide 20 (1 Piksel → 1 Neuron):** Sorotan `8×8` dipindahkan ke piksel biru nyata pada gaun Elsa `(4, 2)` (`gray = 0.45`, `RGB [108, 112, 143]`).
  - **Slide 21 (Animasi `Flatten` 4×4):** Ditingkatkan ke `4×4` (`16` piksel warna asli gaun Elsa `thumb_elsa_flatten.jpg`), panah penghubung `Bagi 4×4 →` dari foto ke grid, dan penjajaran judul tanpa nomor.
  - **Slide 22 (`Input Layer: Tinggi × Lebar × Channel`):** Fokus penuh ke dataset Frozen (`64×64×1`, `64×64×3`, `224×224×3` + slider `H=W` & `Ch`), pita `03c_elsa_flatten_strip.png` nyata, serta **animasi 60fps per-piksel *zero-reflow*** (`8×8` grid piksel nyata Elsa, `▶ Putar`, `⏭ +1 Piksel`, `↺ Reset`, plus klik kotak piksel mana saja di Foto Elsa & lacak balik neuron Input Layer).
  - **Slide 23 (`Input Layer & Output Layer`):** Digabung menjadi 1 slide visual proporsi corong (*Input Layer* jauh lebih banyak dari *Output Layer*) + 4 kartu penjelasan bernomor + **animasi 60fps sangat detail** (*pixel-by-pixel → neuron-by-neuron → koneksi neuron-by-neuron `w` → Output Layer → Hasil Klasifikasi*, plus klik langsung piksel foto, neuron Input `x₁..x₁₅₀.₅₂₈`, dan neuron Output `y₁..y₅`).
  - **Proporsi Corong & Kerapian Global:** Proporsi *Input Layer* > *Output Layer* diselaraskan pada Slide 23, 25, & 28; kicker disederhanakan menjadi `BAB NN · <TOPIK>`; `tools/core/exporter.py` diperbaiki agar ekspor PPTX selalu 100% *opaque* (menonaktifkan animasi fade-in CSS saat tangkap CDP).
- **Lolos Penuh 6 Gerbang Validasi (`python tools/build_session.py P02 --validate`, termasuk `SMOKE_TEST=1` TensorFlow/Keras):**
  - HTML (`56` slide, `41` aset lokal, `120.0` menit, `timeless_ok = true`),
  - PDF & PPTX 16:9 (`79/79` halaman/slide cocok, `79/79` Speaker Notes),
  - Presenter Script (`56/56` halaman A4 Portrait),
  - Notebook (`47` sel peserta dengan `8` `# TODO` === `8` Hint, `39` sel solusi, `solution_smoke_executed = true`, `student_prefix_executed = true`),
  - Portal & PWA (`sessions.json`, `vercel.json`, `sw.js` versi `dl-course-pwa-v8`).

### 4. Pembaruan Fullscreen Engine, Animasi Slide 20, & Slide 24 Simulasi Training Matematis (57 Slide — Terverifikasi Penuh)
- **Optimasi Mode Fullscreen (`tools/core/html_shell.py`, `tools/core/exporter.py`, `sw.js` → `dl-course-pwa-v9`):**
  - Seluruh dek kini dirender di atas panggung kanonik `1152×648` (`16:9`) dalam `#stage-scaler` dengan penskalaan GPU `transform: scale(...)` (`fitStage()` pada `load`, `resize`, `fullscreenchange`, tombol `F`, dan `F11`) — mengisi 100% layar `1920×1080` proporsional tanpa distorsi; bar `#controls` terkunci 1 baris rapi di tengah bawah (`width: max-content; white-space: nowrap; opacity: 0.08`, hover `1.0`).
- **Peningkatan Visual & Interaktif P02:**
  - **Kicker Bab 2 & Penutup:** Dirapikan menjadi format seragam `BAB 02 · <TASK>` (`IMAGE CLASSIFICATION`, `OBJECT DETECTION`, `IMAGE SEGMENTATION`, `OBJECT TRACKING`), `BAB 05 · ISTIRAHAT & HANDS-ON`, dan `REFERENSI BELAJAR · BAGIAN 1/2`.
  - **Slide 20 (`Dimulai dari 1 Neuron`):** Diganti dari gambar statis menjadi **animasi interaktif 60fps 3 tahap** (`Zoom Piksel` → grid nyata `8×8` Elsa yang bisa diklik langsung → `Ambil 1 Piksel` → *morph* kotak ke lingkaran biru `3. 1 Neuron`, default piksel biru gaun Elsa `Baris 5, Kol 3 · 0.42`).
  - **Slide 23 (`Input Layer & Output Layer`):** Label pil kuning ditetapkan ke **`Kalkulasi probabilitas kelas`**, dilengkapi kotak **`Aturan Kunci (MLP · Klasifikasi Multi-Kelas)`** yang presisi secara ilmiah (`Ukuran piksel × channel (H×W×C)` → Input Layer; `Jumlah kelas gambar` → Output Layer, dengan catatan biner 1 neuron Sigmoid).
  - **Slide 24 (`Simulasi Training: Bagaimana Neural Network Mengenali Gambar?`):** Dilengkapi training Softmax Regression nyata ber-L2 (`l2 = 0.0005`) pada 5 foto figurin Frozen dengan **6 fitur piksel murni** (`Merah R, Hijau G, Biru B, Piksel Atas, Piksel Bawah, Kontras` > 5 neuron output agar proporsi corong *Input > Output* tetap terjaga, jembatan eksplisit dari `150.528` piksel), node **`+1 · Bias (b)`** terpisah bebas tabrakan, legenda warna hijau/merah *weight*, animasi 4 tahap + **`⏭ +1 Tahap Hitung`**, matematika 100% eksak bisa dicek kalkulator (`W` & `b` bulat 1 desimal + unshifted Softmax `e^z / Σe^z`), dan tampilan **`Target 100% vs Prediksi → Error`** pada Tahap 4!
  - **Trilogi Zoom-In Slide 24 → 25 → 26 → 27 & Penyeragaman Kontrol (`▶ Play` / `■ Stop` / `↺ Reset`):** Dek lengkap **`59` slide** (setara P01) dengan total `data-notes` tetap **`120.0` menit**. Ketiga slide setelah Slide 24 kini terhubung mulus lewat strip **`📍 Posisi di Slide 24`** dengan angka **100% identik Slide 24**: (1) **Slide 25** (*Zoom-In Tahap A: Weight + Bias* — diagram kabel & perkalian `× w = hasil` per karakter + 2 slider fokus *Weight Utama* & *Bias*), (2) **Slide 26** (*Zoom-In Tahap B: Activation Function* — diagram pipa `Hasil Tahap A (z) → Mesin ReLU / Sigmoid / Softmax → Output Akhir` + slider live `Geser z`), dan (3) **Slide 27** (*Zoom-In Output Akhir* — diagram 3 kolom `Hasil Tahap B (5 Probabilitas Softmax) → Argmax & Confidence vs Ambang Yakin → Evaluasi vs Label Asli (Error & Cross-Entropy Loss)` across mode `1. Terlatih`, `2. Ragu (Tipis)`, & `3. Acak (Belum Latih)`). Seluruh 8 simulator interaktif (Slide 20–27) memakai label tombol seragam **`▶ Play` / `■ Stop` / `↺ Reset`** dan terdaftar penuh di `window.SLIDE_PDF_EXPANDERS`.
  - **Ultimate Slide 29 (`Simulasi Full Neural Network End-to-End`), Slide 28 (`Siklus Belajar Utuh`), Hierarki `Tahap 1–5`, Motion `4×4` Slide 21, Sinkronisasi Kartu `.sync-card` (`Slide 20–29`), & Penyeragaman `150.528` Neuron + Triplet RGB Lengkap (`Slide 22–25`):**
    - Seluruh Bab 3 memiliki penomoran bertahap runtut di kicker & strip kontinuitas (**`Tahap 1` S20 → `Tahap 2.1` S21 → `Tahap 2.2` S22 → `Tahap 3` S23 → `Tahap 4` S24 → `Tahap 4.1` S25 → `Tahap 4.2` S26 → `Tahap 4.3` S27 → `Tahap 5` S28 → `Simulasi Full Neural Network End-to-End` S29**).
    - **Slide 20** dirapikan label `1–4` sejajar di atas + perbesaran 1:1 foto & grid `8×8` (`172×172px`); **Slide 21** memiliki foto `218×218px` sejajar 1:1 dengan grid `4×4` + motion 2-fase 60fps; **Slide 22–25** seragam penuh menampilkan triplet RGB lengkap pada piksel awal (`x₁..x₃`) maupun piksel akhir (`x₁₅₀.₅₂₆..x₁₅₀.₅₂₈`, elipsis **`+150.522`** neuron).
    - **Slide 20–29** dilengkapi koreografi kartu penjelasan aktif (`.sync-card`) yang otomatis terangkat, menyala sesuai warna tahap, dan menampilkan lencana `● AKTIF` mengikuti proses animasi.
    - **Ultimate Slide 29 (`Simulasi Full Neural Network: End-to-End Tahap 1–5` — Tanpa *Hidden Layer* + Mode `▶ Full 8 Epoch`):** menjalankan **model 1-layer nyata `150.528 → 5 Softmax` (`752.645` parameter)** terlatih langsung 8 epoch melewati kelima foto Frozen (`data/frozen_v1/` via SGD NumPy nyata), tanpa istilah *Hidden Layer* karena belum diperkenalkan di Bab 3. Dilengkapi tombol **`▶ Full 8 Epoch`** yang mensimulasikan **semua 5 karakter (`Anna → Elsa → Kristoff → Olaf → Sven`) secara bergantian selama 8 Epoch penuh** (`40` langkah training) dengan lencana status live `A E K O S`, kurva *Mean Loss* real-time (`1.70 → 0.21`), perubahan akurasi `0/5 → 1/5 → 3/5 → 4/5 → 5/5 Yakin (≥74%)`, gelombang merah *Backpropagation*, serta tombol **`▶ 1 Foto`**, **`⏭ +1 Tahap`**, dan slider `Epoch 1–8`.
    - **Pemindahan Bab 4 (`Arsitektur Neural Network untuk CV`) ke P03, Cover Evaluasi & Hands-On, Opsi Kuis Klik Hijau/Merah, & Penghapusan Mention Istirahat (`42` Slide):**
      - Sesuai permintaan pengguna, Bab 4 (*Arsitektur Neural Network untuk CV* — 5 slide) disembunyikan secara *reversible* (`HIDE_BAB4_ARCH = True` di `tools/sessions/p02_teori_neural_network/build_html.py`) dan dipindahkan ke **P03** (`Arsitektur Neural Network & Konvolusi (CNN)` di `tools/core/registry.py` & `sessions.json`).
      - Judul resmi, folder, dan seluruh file P02 diperbarui menjadi **`p02_teori_neural_network`** (`materials/p02_teori_neural_network/p02_teori_neural_network.*`, `p02_teori_neural_network_presenter_script.pdf`, dan kode sumber di `tools/sessions/p02_teori_neural_network/`), tersinkron penuh dengan `tools/core/registry.py`, `sessions.json`, `vercel.json` (`/p2`, `/p02`), dan `sw.js` (`dl-course-pwa-v10`).
      - Setelah **Bab 3 (Slide 19–29)** langsung masuk **Slide 30 (Cover kuning: `Kuis, Kamus Istilah & Referensi`)** → **Slide 31 (Kuis 5 Soal — Q5 tentang Backpropagation & Gradient Descent `1.70 → 0.21`)** → **Slide 32 (Kamus Istilah 12 kartu)** → **Slide 33–34 (Referensi Belajar Mandiri 1/2 & 2/2)** → **Slide 35 (Cover biru: `Hands-On: Praktik Neural Network`)** → **Slide 36–41 (Hands-On Langkah 1–6)** → **Slide 42 (3 Poin Utama — Penutup)**. Slide Mini-Challenge & Closing lama dihapus dari dek aktif, dan seluruh penyebutan *istirahat 5 menit* dihapus bersih (`0` kemunculan di HTML & `presenter_notes.py`).
      - Seluruh slide Tanya-Jawab pilihan ganda (**Slide 04, 10, 18**, standar di `tools/core/html_shell.py`) mendukung klik langsung opsi `A/B/C` dengan umpan balik hijau (`✓ Tepat!`) / merah (`✕ Belum tepat`) sebelum tombol *Lihat Jawaban & Penjelasan* diklik.
      - Dek aktif **`42` slide** (`120.0` menit exact), `presenter_notes.py` **`42/42`**, `build_notebooks.py` tersinkron penuh ke `Slide 36–41` (Hands-On) & `Slide 33–34` (Referensi), dan `setArchTab()` diberi guard null-safe (terverifikasi `0` error JS di Chrome).
- **Lolos Penuh 6 Gerbang Validasi (`python tools/build_session.py P02 --validate`):**
  - HTML (`42` slide aktif, `38` aset lokal, `120.0` menit, `timeless_ok = true`),
  - PDF & PPTX 16:9 (`61/61` halaman/slide cocok, `61/61` Speaker Notes),
  - Presenter Script (`42/42` halaman A4 Portrait),
  - Notebook (`47` sel peserta dengan `8` `# TODO` === `8` Hint, `39` sel solusi, `solution_smoke_executed = true`, `student_prefix_executed = true`),
  - Portal & PWA (`sessions.json`, `vercel.json`, `sw.js` versi `dl-course-pwa-v10`).
