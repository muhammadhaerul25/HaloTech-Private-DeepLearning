# STANDAR_MATERI.md — Standar Baku Penyusunan Materi (P01–P08)

Dokumen ini adalah **Standard Operating Procedure (SOP)** resmi untuk penyusunan seluruh materi **HaloTech Private Deep Learning (P01–P08)**, diturunkan dari arsitektur final **P01** yang telah tervalidasi.

---

## 1. Prinsip Arsitektur: HTML5 sebagai Single Source of Truth (SSOT)

Seluruh artefak dalam satu pertemuan tinggal di dalam **satu folder `materials/P{NN}/`** dan diturunkan dari **satu sumber kebenaran utama (`HTML5 Interaktif`)**:

```text
materials/P{NN}/
├── P{NN}_{slug}.html                  # [1] MAIN SOURCE (SSOT) — Slide Interaktif HTML5 & PWA
├── P{NN}_{slug}.pdf                   # [2] Ekspor PDF Vektor 16:9 (Chrome Headless + Ekspansi State & Q&A)
├── P{NN}_{slug}.pptx                  # [3] Ekspor PPTX 16:9 HD 2x (Chrome CDP 2240x1260 + Speaker Notes Detail)
├── P{NN}_presenter_script.pdf         # [4] Naskah Pengajar A4 (1 Slide = 1 Halaman: Visual 16:9 + Penjelasan Detail)
├── P{NN}_{slug}.ipynb                 # [5a] Notebook Peserta (Cell-by-cell, # TODO + <details> Hint & Jawaban)
├── solutions/
│   └── P{NN}_{slug}.ipynb             # [5b] Notebook Kunci Jawaban (100% terisi + assert lolos SMOKE_TEST=1)
└── assets/
    └── P{NN}/                         # Grafik Matplotlib/OpenCV deterministik, JSON statistik/sampel, ikon PWA
```

### Aturan Sinkronisasi Wajib
Setiap kali isi atau urutan slide di HTML (`build_html.py`) diubah, **wajib menjalankan orkestrator tunggal**:
```bash
python tools/build_session.py P{NN} --validate
```
Orkestrator ini otomatis menjalankan urutan:
1. `build_assets.py` → menghasilkan gambar & JSON statistik ke `materials/P{NN}/assets/P{NN}/`
2. `build_html.py` → menghasilkan HTML5 SSOT memakai `tools/core/html_shell.py`
3. `exporter.py (PDF)` → mengekspor PDF 16:9 dari HTML dengan ekspansi state simulator & Q&A
4. `exporter.py (PPTX)` → mengekspor PPTX 16:9 Retina HD (`2240×1260`) identik PDF/HTML + Speaker Notes detail dari `presenter_notes.py`
5. `exporter.py (Presenter Script)` → mengekspor `P{NN}_presenter_script.pdf` (A4 Portrait)
6. `build_notebooks.py` → menghasilkan Notebook Peserta & Kunci Jawaban selaras nomor slide HTML
7. `validator.py` → menjalankan seluruh gerbang validasi (*Definition of Done*) termasuk eksekusi `SMOKE_TEST=1`

---

## 2. Peta Resmi Sesi & Konvensi Penamaan (P01–P08)

Penomoran kurikulum aktif mengikuti [sessions.json](../sessions.json) (**timeless — tanpa tanggal, hari, atau jam**):

| ID | URL Cepat | Fase | Warna Aksen | Slug File | Rujukan `docs/PLAN.md` |
|---|---|---|---|---|---|
| `P01` | `/p1` | Fondasi | `#4285F4` | `understanding_images_processing_eda` | P4: Image Processing & EDA |
| `P02` | `/p2` | Fondasi | `#EA4335` | `teori_neural_network` | Teori Neural Network (AI/ML/DL, CV Tasks & Backprop) |
| `P03` | `/p3` | Fondasi | `#FBBC04` | `arsitektur_neural_network` | Arsitektur Neural Network |
| `P04` | `/p4` | Fondasi | `#34A853` | `cnn_architectures_transfer_learning` | Arsitektur CNN & Transfer Learning |
| `P05` | `/p5` | Eksperimen | `#4285F4` | `data_methodology_splitting` | Metodologi Data, Splitting & Desain |
| `P06` | `/p6` | Eksperimen | `#EA4335` | `data_pipeline_augmentation_baseline` | Data Pipeline, Augmentation & Baseline |
| `P07` | `/p7` | Eksperimen | `#FBBC04` | `training_finetuning` | Training Lengkap & Fine-Tuning |
| `P08` | `/p8` | Analisis & Pelaporan | `#34A853` | `evaluation_error_analysis_gradcam` | Evaluasi, Error Analysis & Grad-CAM |

---

## 3. Standar Desain & Pedagogi HTML5 (Acuan Resmi **P02 Standard** · `tools/core/html_shell.py`)

### A. Tema Visual & Disiplin Layout (`1152×648`, Gaya Google I/O Cerah)
- **Palet Warna Baku:**
  - Primer: `--blue: #4285F4` (`--blue-text: #1A73E8` di latar putih), `--red: #EA4335`, `--yellow: #FBBC04`, `--green: #34A853`.
  - Netral: `--dark: #202124`, `--muted: #5F6368`, `--border: #DADCE0`, `--surface: #F8F9FA`, `--white: #FFFFFF`.
  - Tint Kartu: `--tint-blue: #E8F0FE`, `--tint-red: #FCE8E6`, `--tint-yellow: #FEF7E0`, `--tint-green: #E6F4EA`.
- **Tipografi:** `Poppins` (judul, kicker, pill), `Roboto` (isi), `Roboto Mono` (kode, angka metrik, badge teknis).
- **Aturan Kontras & Kepadatan:**
  - Teks di atas kuning/hijau memakai `#202124`; jangan menaruh teks kuning di atas latar putih (`--yellow` untuk bentuk/border/tint `#FEF7E0`).
  - Wajib `0` scrollbar / overflow pada stage baku (`scrollHeight == 648`, `scrollWidth == 1152`, jarak konten ke `.slide-footer` $\ge 13\text{px}$).

### B. Alur Pedagogi & Arsitektur Dek (~50–55 Slide · Tepat `120.0 Menit`)
Mengikuti pola teruji **P02** agar ritme kelas 1-on-1 cepat masuk ke praktik dan bebas jargon prematur:
1. **Pembuka Ringkas (`4` Slide · `~6.0 menit`):**
   - **Slide 01 (Cover):** Latar putih radial gradien lembut + ornamen SVG sudut + badge `DEEP LEARNING TRACK · Fase ... · 120 Menit` + judul gradien + garis pembagi 4 warna (`4px`) + badge `[MH] Presented by Muhammad Haerul` + kartu kanan **1+4 Bento Showcase** foto nyata 5 karakter Frozen (`data/frozen_v1/`).
   - **Slide 02 (Agenda + 3 Learning Goals Gabungan):** Layout `.split-60-40` — kiri `.step-list` blok bab beserta badge menit; kanan 3 kartu `.mini-box` berwarna (*Yang Akan Kamu Kuasai*) + `.callout` ritme `120 Menit`.
   - **Slide 03 (Pemanasan / Recap Sesi Sebelumnya):** Jembatan konkret dari konsep & angka sesi sebelumnya ke masalah sesi hari ini.
   - **Slide 04 (Tanya-Jawab #1):** Pemantik konsep awal memakai `make_qa_slide(...)`.
2. **Bab Inti Teori (`~3`–`4` Bab · `~45–50 menit`):**
   - Pembatas bab satu warna penuh bergantian (`bg-blue`, `bg-red`, `bg-green`, `bg-yellow`) via `make_divider_slide(...)`.
   - Pola pedagogi **Micro-Ladder** (*tanpa lompatan konsep / istilah yang belum diajarkan*):
     **Analogi Nyata $\rightarrow$ Visual / Animasi / Simulator $\rightarrow$ Rumus / Mekanisme Minimal $\rightarrow$ Contoh Piksel/Foto Frozen $\rightarrow$ Tanya-Jawab Checkpoint (`QA #2, #3, ...`)**.
   - **Standar Animasi Kontinu (`@media print` Safe):** Untuk diagram pembanding (mis. Slide 06, 07, 12–16 P02), gunakan `@keyframes` CSS/SVG **loop otomatis tanpa tombol Play**, dilengkapi aturan `@media print { animation: none !important; opacity: 1 !important; transform: none !important; }` agar PDF & PPTX tetap tajam membeku pada kondisi terbaca.
   - **Standar Simulator & Kartu Sinkron (`.sync-card` + `.ds-chip`):**
     - **Resting State Penuh:** Saat slide dibuka atau di-reset, seluruh kartu penjelasan kiri tampil **terang 100%** (tidak redup); hanya menyorot `● AKTIF` saat tombol *Play/Step/Tab* sedang aktif.
     - Tombol `▶ Play`, `⏭ +1 Langkah`, `↺ Reset`, chip 5 karakter Frozen (`.ds-chip`), dan slider bekerja sinkron tanpa menggeser layout (*zero layout shift*).
3. **Evaluasi, Kamus & Referensi (`~7.5 menit`):**
   - **Cover Evaluasi (`bg-yellow` · `0.5m`):** Menggunakan `.cover-roadmap` 3 chip.
   - **Kuis 5 Soal Terpisah (`5` Slide · `5.0m`):** 1 soal per slide via `make_qa_slide(..., quiz_progress_idx=1..5)` — opsi A/B/C bisa diklik langsung (`pickQAChoice`) + stepper progres kanan atas + panel visual kanan yang berubah dari `.vis-q` (pertanyaan) menjadi `.vis-a` (ilustrasi jawaban).
   - **Kamus Istilah Santai (`1` Slide · `2.0m`):** Menggunakan `make_glossary_slide(...)` — 2 kolom terkelompok per Bab (`.dict-grid`), dilengkapi input pencarian live (`.gloss-search`), filter tombol Bab (`.gloss-fbtn`), dan tombol lompat slide **`SXX ↗`**.
   - **Referensi Materi (`2` Slide · `0.0m`):** Menggunakan `make_references_slide(...)` — grid **`2×3` kartu penuh** (`.ref-grid-full`, `.ref-card-rich` dengan badge konteks `Bab X (SXX)`) + strip bawah **3-Langkah Rute Belajar Mandiri** (`.ref-route-bar`). URL hanya berasal dari `docs/PLAN.md` (atau bertanda `[CEK LINK]`).
4. **Hands-On Visual-First (`~55 menit`):**
   - **Cover Hands-On (`bg-blue` · `1.0m`):** Memakai `.cover-roadmap-3x2` (6 chip peta mikro-task) + `.cover-env-strip` (nama `.ipynb`, folder dataset dinamis, aturan `1 Sel = 1 Visual Nyata`).
   - **5–6 Slide Langkah Hands-On (`make_handson_step_slide`):** Header ber-stepper progres 6 tahap (`.ho-stepper`), kartu kiri (`.ho-sub-list` dengan badge warna tahap selaras `# TODO`, chip rujukan teori `🔗`, kotak `🎯 CEK BERHASIL`, & `.callout` Momen Aha), kolom kanan berisi kartu kode gelap `3–8 baris` ber-syntax highlight (`highlight_python` + tombol `Salin`) tepat di atas pratinjau **`.ho-vis-card` hasil plot nyata** dari dataset Frozen!
5. **Penutup Simetris Putih Google I/O (`3.0 menit`):**
   - **3 Poin Utama (`2.0m` · `make_summary_3pillars_slide`):** Tema **putih bersih Google I/O** (`#FFFFFF`, latar radial halus, 3 kartu `.finale-card` bernomor `01–03` lengkap dengan strip visual/pipeline, pill capaian nyata, dan banner footer menuju Kamus, Referensi, & file output di `results/`).
   - **Closing & Key Quote (`1.0m` · `make_closing_slide`):** Slide penutup **putih lapang Google I/O** (header `CLOSING · P{NN}` + badge `✓ Fondasi/Sesi Selesai`, 4 titik Google kanan atas, ornamen sudut halus, 1 pesan inti penutup berbahasa lugas bebas jargon berlebihan, garis pembagi 4 warna, dan kalimat sambutan menuju `P{NN+1}`).

### C. Kontrak Ekspansi Interaktif untuk PDF & PPTX (`window.SLIDE_PDF_EXPANDERS`)
Agar mesin `tools/core/exporter.py` tetap 100% generik untuk semua sesi, setiap simulator/tab di HTML yang ingin dipecah menjadi beberapa halaman di PDF & PPTX **wajib** mendaftarkan expander melalui kontrak baku berikut:

```javascript
window.SLIDE_PDF_EXPANDERS = window.SLIDE_PDF_EXPANDERS || [];
window.SLIDE_PDF_EXPANDERS.push(({ cloneSlideWithCanvases }) => {
  const host = document.getElementById('my-sim-tabs');
  if (!host || typeof setMySimMode !== 'function') return;
  const slide = host.closest('section.slide');
  if (!slide) return;
  const modes = ['mode1', 'mode2', 'mode3'];
  const clones = modes.map((m) => {
    setMySimMode(m);
    return cloneSlideWithCanvases(slide, 'mysim-' + m);
  });
  clones.forEach((c) => slide.parentNode.insertBefore(c, slide));
  slide.remove();
});
```
Selain expander kustom tersebut, `exporter.py` secara otomatis:
- Menandai `data-orig-num="1..N"` sebelum ekspansi.
- Memecah semua slide yang memiliki `.qa-answer` atau `.quiz-ans` menjadi 2 halaman berurutan (**Pertanyaan $\rightarrow$ Jawaban**).
- Menyalin seluruh isi `<canvas>` secara akurat saat mengkloning slide.

---

## 4. Standar Ekspor Atomik PDF, PPTX & Presenter Script (`tools/core/exporter.py`)

Semua penulisan PDF, PPTX, dan notebook wajib memakai **temp file `_tmp_*` (di-ignore Git)** yang lalu dipindahkan secara **atomik** lewat `.replace(...)` agar tidak terjadi race condition *truncation* `mmap` pada Git Windows saat IDE memantau perubahan.
1. **Slide PDF (`16:9`):** Dicetak via Chrome/Edge Headless (`--headless=new --no-pdf-header-footer --print-to-pdf`), ukuran `@page { size: 13.333in 7.5in; margin: 0; }`.
2. **Slide PPTX (`16:9` HD):** Dirender via Chrome DevTools Protocol (CDP) pada viewport `1120×630` dengan `deviceScaleFactor: 2` (`2240×1260` Retina HD), disusun dengan `python-pptx` berukuran `13.333 × 7.5 in`, serta diisi **Speaker Notes** lengkap di setiap slide (gabungan `data-notes` HTML + `SLIDE_EXPLANATIONS[origNum]`).
3. **Presenter Script PDF (`A4 Portrait`):** 1 slide HTML dasar = 1 halaman A4 berisi Header (`Slide N — Judul` + kicker), bingkai preview live 16:9 (`592×333px`), dan kotak *Penjelasan Detail Materi* dari `presenter_notes.py`.

---

## 5. Standar Notebook Hands-On *Visual-First* (`tools/core/notebook_builder.py`)

- **Pemisahan `Alat Visualisasi Siap Pakai` (Tahap 0.2):** Kode plotting `matplotlib` dan helper loader dinamis (mis. `muat_dataset_frozen`) dikumpulkan pada satu sel siap pakai di Tahap 0.2 agar setiap sel kerja peserta sangat pendek (**2–14 baris**), 1 sel = 1 tugas sederhana, tanpa nested loop/comprehension rumit, dan selalu menghasilkan output gambar/angka nyata.
- **Markdown Sebelum Kode:** Setiap sel kode wajib didahului sel Markdown pengantar yang menautkan nomor slide HTML (`Sesuai Slide XX–YY`) dan diakhiri ringkasan *"Apa yang perlu diperhatikan?"* di akhir tiap tahap.
- **Setup 3 Tahap Baku (`setup_cells_standard`):**
  1. `Setup 1/3`: Import library & cetak versi (`numpy`, `pandas`, `tensorflow`, dll.).
  2. `Setup 2/3`: Deteksi Colab/Lokal (`try: import google.colab`) + kunci `SEED = 42`.
  3. `Setup 3/3`: Konfigurasi tidak di-hardcode (`IMG_SIZE = 224`, `CLASS_NAMES`, `SMOKE_TEST`, auto-detect `BASE_DIR`, `DATA_DIR`, `RESULTS_DIR`).
- **Latihan `# TODO` & Output Referensi Tersimpan:**
  - Versi peserta: 6–10 sel `# TODO` singkat (1–2 baris isian) dengan `assert` diagnostik Bahasa Indonesia + sel Markdown `<details><summary><b>💡 Hint & Jawaban ...</b></summary>` tepat setelahnya. Seluruh sel kode di notebook peserta juga boleh diisi pratinjau *saved outputs* hasil eksekusi nyata notebook solusi agar peserta langsung melihat target outputnya.
  - Versi kunci (`solutions/`): seluruh `# TODO` terisi, tanpa sel `<details>`, seluruh sel dieksekusi penuh (`SMOKE_TEST=0`) dengan output tersimpan (`0` error) serta wajib lolos validasi `SMOKE_TEST=1`.
- **Kebijakan Metodologi:** Augmentation & statistik normalisasi hanya pada `train`; test set dievaluasi sekali; grafik kunci disimpan ke `results/`; hasil pada `data/sample/` diberi label *"contoh data sampel"*.

---

## 6. Standar Validasi (*Definition of Done*) & Rilis Portal/PWA

Setiap sesi wajib lolos `python tools/build_session.py P{NN} --validate`:
1. **HTML:** Jumlah slide sinkron dengan counter & footer; 0 asset hilang; 0 kode sesi lama (`P4`–`P13`); 0 string tanggal/hari/jam; semua `data-notes` hadir dan total waktu tepat `120.0 menit`.
2. **PDF & PPTX:** Jumlah halaman PDF === jumlah slide PPTX; rasio `16:9`; 100% slide PPTX punya Speaker Notes non-kosong; 0 string tanggal/jam.
3. **Presenter Script:** Seluruh slide `1..N` terdefinisi di `SLIDE_EXPLANATIONS`; PDF terbentuk dengan halaman ≥ `N`.
4. **Notebooks:** Versi kunci dieksekusi penuh (`SMOKE_TEST=1`) dengan 0 error; versi peserta berjalan bersih hingga sebelum sel `# TODO` pertama; jumlah `# TODO` === jumlah sel `<details>` Hint.
5. **Registrasi Web & Dokumentasi (setelah disetujui):**
   - Update `sessions.json`: ubah `status: "available"` dan lengkapi `links` (`slidesHtml`, `slidesPdf`, `slidesPptx`, `notebook`, `solution`).
   - Update `vercel.json`: arahkan rewrite `/p{N}` & `/p0{N}` ke `/materials/P{NN}/P{NN}_{slug}.html`.
   - Update `sw.js`: naikkan versi `CACHE_NAME` (mis. `v6`) dan tambahkan HTML + aset penting `P{NN}` ke `PRECACHE_ASSETS`.
   - Update `docs/PROGRESS.md` dengan ringkasan artefak, asumsi, dan hasil validasi.


---

## 7. Standar Dataset Proyek Utama (Mulai P02–P08): `data/frozen_v1/`

Mulai sesi **P02 dan seterusnya**, seluruh contoh visual slide, simulator interaktif, dan notebook hands-on menggunakan dataset proyek akhir **Disney Frozen Figurine Dataset** yang disiapkan dari `data/dataset _frozen_v1.zip` melalui `python tools/prepare_frozen_dataset.py`:

- **Struktur Folder Siap Pakai (GitHub- & Colab-friendly):**
  ```text
  data/frozen_v1/
  ├── anna/{polos,ramai}/anna_<kondisi>_<NN>.jpg
  ├── elsa/{polos,ramai}/elsa_<kondisi>_<NN>.jpg
  ├── kristoff/{polos,ramai}/kristoff_<kondisi>_<NN>.jpg
  ├── olaf/{polos,ramai}/olaf_<kondisi>_<NN>.jpg
  ├── sven/{polos,ramai}/sven_<kondisi>_<NN>.jpg
  ├── metadata.csv           # file, orig_file, kelas, kondisi, sub_kondisi, sesi_foto, EDA metrics, sha256
  └── dataset_summary.json   # ringkasan statistik dinamis untuk diimpor ke slide P02–P08
  ```
- **Kelas Baku:** `CLASS_NAMES = ["anna", "elsa", "kristoff", "olaf", "sven"]` (5 kelas karakter Disney Frozen).
- **Kondisi Baku:** `polos` vs `ramai` (dengan metadata `sub_kondisi`: `polos_terang`, `polos_redup`, `ramai_rak_terang`, `ramai_rak_redup`, serta `sesi_foto` untuk Group Split anti-leakage di P05).
- **Aturan Dinamis:** Karena foto dapat terus ditambah di versi berikutnya (`v2` dst.), kode notebook dan skrip slide **dilarang meng-hardcode jumlah foto** — selalu baca secara dinamis dari `DATA_DIR` dan `metadata.csv`.
- **Kebijakan Git:** Arsip `.zip` mentah (`data/*.zip`, 166 MB) di-ignore di `.gitignore` agar aman dari batas 100 MB GitHub, sedangkan folder `data/frozen_v1/` (JPEG ringan ~576×768) aman di-commit ke repo dan dipakai langsung pada slide HTML/PDF/PPTX serta notebook.
