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
| `P02` | `/p2` | Fondasi | `#EA4335` | `neural_network_ann` | P5: Teori Neural Network (ANN) |
| `P03` | `/p3` | Fondasi | `#FBBC04` | `cnn_fundamentals_cv` | P6: CNN Fundamentals & Tugas CV |
| `P04` | `/p4` | Fondasi | `#34A853` | `cnn_architectures_transfer_learning` | P7: Arsitektur CNN & Transfer Learning |
| `P05` | `/p5` | Eksperimen | `#4285F4` | `data_methodology_splitting` | P8: Metodologi Data, Splitting & Desain |
| `P06` | `/p6` | Eksperimen | `#EA4335` | `data_pipeline_augmentation_baseline` | P9: Data Pipeline, Augmentation & Baseline |
| `P07` | `/p7` | Eksperimen | `#FBBC04` | `training_finetuning` | P10: Training Lengkap & Fine-Tuning |
| `P08` | `/p8` | Analisis & Pelaporan | `#34A853` | `evaluation_error_analysis_gradcam` | P11 + P12 (+ penutup / atau perluasan P09 opsional) |

---

## 3. Standar Desain & Pedagogi HTML5 (`tools/core/html_shell.py`)

### A. Tema Visual (Gaya Konferensi Google I/O — Tanpa Aset Resmi Google)
- **Palet Warna Baku:**
  - Primer: `--blue: #4285F4` (`--blue-text: #1A73E8` di latar putih), `--red: #EA4335`, `--yellow: #FBBC04`, `--green: #34A853`.
  - Netral: `--dark: #202124`, `--muted: #5F6368`, `--border: #DADCE0`, `--surface: #F8F9FA`, `--white: #FFFFFF`.
  - Tint Kartu: `--tint-blue: #E8F0FE`, `--tint-red: #FCE8E6`, `--tint-yellow: #FEF7E0`, `--tint-green: #E6F4EA`.
- **Tipografi:** `Poppins` (judul, kicker, pill), `Roboto` (isi), `Roboto Mono` (kode, angka metrik, badge teknis).
- **Aturan Kontras:** Teks di atas kuning/hijau menggunakan `#202124`; jangan menaruh teks kuning di atas latar putih.

### B. Alur Pedagogi 5 Bab (~45–60 Slide · Tepat `120.0 Menit`)
Setiap sesi mengikuti template 120 menit yang ramah pemula non-IT:
1. **Slide Pembuka (5 slide · ~5–6 menit):**
   - **Slide 01 (Cover):** Latar terang bergradien halus + ornamen SVG geometris + badge `DEEP LEARNING TRACK · Fase ... · 120 Menit` + `Presented by Muhammad Haerul` + pill topik & tools (tanpa tanggal/jam).
   - **Slide 02 (Peta Perjalanan Belajar):** 5 Bab menggunakan `.step-list`.
   - **Slide 03 (Alur Sesi 120 Menit):** 6 kartu blok waktu (`00–10`, `10–40`, `40–45`, `45–95`, `95–110`, `110–120`).
   - **Slide 04 (Tujuan Belajar):** 3 kartu kompetensi inti + `.callout` hasil.
   - **Slide 05 (Pemanasan / Recap):** Jembatan dari sesi sebelumnya ke masalah sesi hari ini.
2. **Bab 1 s.d. Bab 4 (Teori Visual & Simulator · ~30–34 menit):**
   - Setiap bab dimulai oleh slide pembatas penuh 1 warna bergantian (`bg-blue`, `bg-red`, `bg-green`, `bg-yellow`).
   - Pola penjelasan tiap konsep: **Analogi → Visual/Simulator Interaktif → Intuisi/Rumus minimal → Contoh Disney/sampel → Dampak ke AI**.
   - Minimal **3–5 simulator interaktif HTML5/Canvas/SVG** yang bisa diklik/digeser langsung di kelas.
   - Minimal **3–5 slide Tanya-Jawab (`qa-box`)** di tengah teori dengan `.vis-q` (pertanyaan) / `.vis-a` (jawaban) & `toggleQA(...)`.
3. **Bab 5 (Praktik, Diskusi, Glosarium, Kuis & Penutup · ~80 menit):**
   - Pembatas Bab 5 (`Alokasi waktu: 5 menit` — jeda istirahat).
   - Ringkasan 5–6 Langkah Praktik Hands-On (`40–50 menit`) + 1–2 slide "Di Balik Layar" kode penting.
   - *Mini-Challenge / Diskusi Kasus* (`10–15 menit`).
   - *Kamus Istilah Santai* (1–2 slide glosarium).
   - *Kuis Interaktif 5 Soal* (3 slide: Soal 1–2, Soal 3–4, Soal 5, memakai `.quiz-item` & `.quiz-ans`).
   - *3 Poin Utama Hari Ini* (slide `dark`).
   - *Closing, Key Quote & Preview Sesi Berikutnya*.
   - *Referensi Belajar Mandiri* (2 slide ber-alokasi `0 menit`, kartu `.ref-item`, URL hanya dari `docs/PLAN.md` atau berlabel `[CEK LINK]`).

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
- Memecah semua slide yang memiliki `.qa-answer` atau `.quiz-ans` menjadi 2 halaman berurutan (**Pertanyaan → Jawaban**).
- Menyalin seluruh isi `<canvas>` secara akurat saat mengkloning slide.

---

## 4. Standar Ekspor PDF, PPTX & Presenter Script (`tools/core/exporter.py`)

1. **Slide PDF (`16:9`):** Dicetak via Chrome/Edge Headless (`--headless=new --no-pdf-header-footer --print-to-pdf`), ukuran `@page { size: 13.333in 7.5in; margin: 0; }`.
2. **Slide PPTX (`16:9` HD):** Dirender via Chrome DevTools Protocol (CDP) pada viewport `1120×630` dengan `deviceScaleFactor: 2` (`2240×1260` Retina HD), disusun dengan `python-pptx` berukuran `13.333 × 7.5 in`, serta diisi **Speaker Notes** lengkap di setiap slide (gabungan `data-notes` HTML + `SLIDE_EXPLANATIONS[origNum]`).
3. **Presenter Script PDF (`A4 Portrait`):** 1 slide HTML dasar = 1 halaman A4 berisi Header (`Slide N — Judul` + kicker), bingkai preview live 16:9 (`592×333px`), dan kotak *Penjelasan Detail Materi* dari `presenter_notes.py`.

---

## 5. Standar Notebook Hands-On (`tools/core/notebook_builder.py`)

- **Cell-by-Cell Ultra Awam-Friendly:** 5–15 baris per sel kode, 1 sel = 1 tugas, tanpa nested loop/comprehension rumit, komentar Bahasa Indonesia (`# ...`) di tiap baris penting.
- **Markdown Sebelum Kode:** Setiap sel kode wajib didahului sel Markdown pengantar yang menautkan nomor slide HTML (`Sesuai Slide XX–YY`).
- **Setup 3 Tahap Baku:**
  1. `Setup 1/3`: Import library & cetak versi (`numpy`, `pandas`, `tensorflow`, dll.).
  2. `Setup 2/3`: Deteksi Colab/Lokal (`try: import google.colab`) + kunci `SEED = 42`.
  3. `Setup 3/3`: Konfigurasi tidak di-hardcode (`IMG_SIZE = 224`, `CLASS_NAMES`, `SMOKE_TEST`, auto-detect `BASE_DIR`, `DATA_DIR`, `RESULTS_DIR`).
- **Latihan `# TODO` & Hint Terbuka:**
  - Versi peserta: 6–10 sel `# TODO` singkat dengan `assert` otomatis + sel Markdown `<details><summary><b>💡 Hint & Jawaban ...</b></summary>` tepat setelahnya.
  - Versi kunci (`solutions/`): seluruh `# TODO` terisi, tanpa sel `<details>`, seluruh sel & `assert` wajib lolos dengan `SMOKE_TEST=1`.
- **Kebijakan Metodologi:** Augmentation & statistik normalisasi hanya pada `train`; test set dievaluasi sekali; hasil pada `data/sample/` diberi label *"contoh data sampel"*.

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
