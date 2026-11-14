# PROGRESS.md — Disney Deep Learning Course

## P4 — Image Processing & EDA Foto Sendiri

### 1. Status Implementasi
- **Status:** **FINAL & SIAP DIGUNAKAN** untuk P04 — mencakup dek slide interaktif HTML 54 slide + ekspor PDF vektor 54 halaman (`slides/P4_image_processing_eda_final.html` & `slides/P4_image_processing_eda_final.pdf`), notebook peserta & kunci jawaban (`notebooks/P04_image_processing_eda.ipynb` & `notebooks/solutions/P04_image_processing_eda.ipynb`), dataset sampel sintetis, dan validasi end-to-end.
- **Tanggal:** 14 November 2026.

### 2. File yang Dibuat / Dimodifikasi
- `tools/slide_theme.py` — tema presentasi terinspirasi gaya konferensi Google I/O (konstanta warna, tipografi, margin, badge sesi, kartu, tag pil, kluster 4 bentuk, pembatas bagian, slide keynote, tabel, footer, dan speaker notes OOXML).
- `tools/make_sample_data.py` — generator dataset sintetis deterministik (`SEED=42`) di `data/sample/`.
- `tools/build_slides_P04.py` — skrip analisis data sampel, generator visualisasi Matplotlib/OpenCV (`slides/assets/P04/`), dan pembangun 22 slide PPTX.
- `tools/build_html_slides_P04.py` — pembangun dek presentasi web interaktif 54 slide bergaya Google I/O conference (Bahasa Indonesia + istilah teknis Inggris natural, tanpa kode sesi/tugas rumah, simulator komputer membaca gambar 4×4 s/d 64×64, ilustrasi manusia melihat gambar realistis, Q&A dengan visual tersembunyi hingga diklik, persistensi halaman `#slide-N` + `localStorage`, dan `#page-jump`).
- `tools/build_notebooks_P04.py` — generator notebook peserta (`# TODO`) dan notebook kunci jawaban P04.
- `slides/P4_image_processing_eda_final.html` & `slides/P4_image_processing_eda_final.pdf` — salinan final slide P4 (54 slide HTML interaktif & 54 halaman PDF 16:9).
- `notebooks/P04_image_processing_eda.ipynb` — notebook peserta (berjalan hingga sel `# TODO` pertama tanpa error).
- `notebooks/solutions/P04_image_processing_eda.ipynb` — notebook kunci jawaban (lolos semua sel & `assert` dengan `SMOKE_TEST=1`).
- `tools/validate_and_render_P04.py` — skrip validasi struktural PPTX, validasi dataset, dan rendering PNG/PDF alternatif.
- `data/sample/` + `data/sample/metadata.csv` — 120 file gambar sintetis + metadata.
- `slides/assets/P04/` — 10 aset visualisasi PNG (termasuk `07b_brightness_contrast_box.png`) + `sample_stats.json` + folder `rendered/` (22 PNG + `P04_preview.pdf`) + folder `rendered_html/` + `rendered_all/` (audit seluruh 54 halaman).
- `slides/P04_image_processing_eda.html` — dek presentasi interaktif 54 slide (16:9, Google Fonts, widget interaktif: grid piksel 8×8, mixer RGB, kalkulator normalisasi, toggle jawaban kuis, speaker notes drawer `N`, grid overview `G`, fullscreen `F`).
- `slides/P04_image_processing_eda.pdf` — ekspor PDF vektor 54 halaman (16:9, `960 × 540 pt` / `13.333 × 7.5 in`) melalui headless Google Chrome.
- `slides/P04_image_processing_eda.pptx` — dek presentasi PPTX 22 slide.
- `docs/PROGRESS.md` — dokumentasi status dan hasil validasi ini.

### 3. Hasil Generasi Dataset Sampel (`data/sample/`)
- **Total file:** 120 file JPEG (5 kelas geometris: `lingkaran`, `persegi`, `segitiga`, `bintang`, `heksagon` × 2 kondisi: `polos`, `ramai` × 12 foto per kombinasi, ukuran `256 × 256`).
- **Kasus khusus terverifikasi:**
  - 1 file rusak (`segitiga/ramai/segitiga_ramai_12.jpg`, gagal `Image.verify()` dan dikecualikan dari perhitungan statistik).
  - 2 file duplikat identik SHA-256 (`lingkaran/polos/lingkaran_polos_01.jpg` dan `lingkaran/polos/lingkaran_polos_02.jpg`).
  - 2 file dengan tag EXIF `Orientation = 6` (`persegi/polos/persegi_polos_01.jpg` dan `bintang/ramai/bintang_ramai_01.jpg`).
- **Statistik terhitung dari 119 foto valid (Contoh data sampel):**
  - `polos` (n=60): rata-rata brightness = `228.11`, rata-rata contrast (std) = `45.21`, rata-rata edge density (Canny) = `0.0121` (min `0.0083`, max `0.0154`).
  - `ramai` (n=59): rata-rata brightness = `127.21`, rata-rata contrast (std) = `54.69`, rata-rata edge density (Canny) = `0.0853` (min `0.0462`, max `0.1194`).

### 4. Hasil Validasi Programatik
- Eksekusi `python tools/make_sample_data.py`: **Lolos** (exit code 0).
- Eksekusi `python tools/build_slides_P04.py`: **Lolos** (exit code 0, menghasilkan 9 aset visualisasi + `slides/P04_image_processing_eda.pptx`).
- Eksekusi `python tools/build_html_slides_P04.py`: **Lolos** (exit code 0, menghasilkan `slides/P04_image_processing_eda.html` dengan 54 slide).
- Ekspor PDF via headless Google Chrome (`--print-to-pdf`): **Lolos**, terverifikasi via PyMuPDF (`54 halaman`, `Rect(0.0, 0.0, 960.0, 540.0)` = 16:9).

### 5. Jumlah Slide
- **Dek HTML Interaktif & PDF Utama:** **54 slide** (dielaborasi lebih rinci dan terstruktur, tanpa tugas rumah sesuai permintaan pengguna).
- **Dek PPTX Awal:** **22 slide** (sesuai urutan wajib awal Slide 01–22).

### 6. Rasio Aspek
- **16:9** (`13.333 × 7.5` inci / `960 × 540 pt` pada PDF).

### 7. Validasi Speaker Notes
- Seluruh **54 slide** pada dek HTML memiliki speaker notes berbahasa Indonesia (dapat dibuka lewat tombol `N` di browser) dengan total alokasi waktu sesi **120 menit**.
- Seluruh 22 slide pada dek PPTX juga memiliki speaker notes tertanam di `notes_slide.notes_text_frame` dengan total **120 menit**.

### 8. Hasil Rendering
- **Dek HTML Interaktif (54 slide):** Diekspor langsung ke PDF vektor `slides/P04_image_processing_eda.pdf` menggunakan headless Google Chrome, lalu sampel halaman (`page_01`, `page_04`, `page_10`, `page_26`, `page_35`, `page_45`, `page_52`, `page_54`) dirender ke PNG di `slides/assets/P04/rendered_html/` via PyMuPDF untuk inspeksi visual.
- **Dek PPTX (22 slide):** LibreOffice (`soffice`) dan Microsoft PowerPoint tidak terpasang di lingkungan Windows ini, sehingga `tools/validate_and_render_P04.py` merender 22 PNG pratinjau di `slides/assets/P04/rendered/`.

### 9. Hasil Inspeksi Visual
- **Dek HTML & PDF 54 slide:** Sampel halaman yang dirender telah diperiksa secara visual. Dua isu kecil yang ditemukan pada putaran pertama telah diperbaiki:
  - Slide 26: scrollbar horizontal pada blok kode `preprocess_input` dihilangkan dengan `white-space: pre-wrap; word-break: break-word;` pada `pre.code`.
  - Slide 35: `suptitle` bawah pada `08_canny_edge_density.png` yang sedikit terpotong dihapus dan disimpan dengan `bbox_inches="tight", pad_inches=0.15` (penjelasan sudah ada di kartu callout slide).
  - Kedua halaman (`page_26.png` dan `page_35.png`) dirender ulang dan diverifikasi bersih tanpa pemotongan maupun scrollbar.

### 10. Validasi Font
- **Font yang digunakan di PPTX:** `Poppins` (judul), `Roboto` (isi), `Roboto Mono` (kode/tag).
- **Font yang terpasang di sistem saat ini:** `Arial` (`arial.ttf`, `arialbd.ttf`, `arialbi.ttf`, `ariali.ttf`).
- **Font yang belum terpasang di lingkungan ini:** `Poppins`, `Roboto`, dan `Roboto Mono`.
- **Rekomendasi sebelum presentasi:** Pasang font `Poppins` (SemiBold/Bold), `Roboto`, dan `Roboto Mono` di komputer penyaji agar rendering PowerPoint/LibreOffice sesuai desain (tanpa fallback ke Arial).

### 11. Keterbatasan & Dependensi yang Belum Terselesaikan
- LibreOffice tidak tersedia di mesin ini, sehingga rendering dilakukan melalui renderer Python (`python-pptx` + `Pillow`) dan bukan konversi LibreOffice/PowerPoint asli.
- File `PLAN.md` berada di root repositori (`PLAN.md`), bukan `docs/PLAN.md`, sehingga referensi dibaca dari `PLAN.md`.
- File `Prompt B` terpisah tidak ada di repositori; oleh karena itu 6 langkah pratinjau pada Slide 18 diambil langsung dari `PLAN.md` bagian P4 (`Hands-on (menit 45–95)`).

### 12. Keputusan yang Sudah Difinalisasi
1. **Tipografi:** Tetap menggunakan `Poppins`, `Roboto`, dan `Roboto Mono` sesuai `AGENTS.md` (dengan fallback otomatis ke `Arial` bila font belum terpasang; disarankan tetap memasang ketiga font tersebut di komputer penyaji sebelum sesi).
2. **Pratinjau Hands-on (Slide 18):** Menggunakan 6 langkah dari `PLAN.md` bagian P4 (`Hands-on (menit 45–95)`).

