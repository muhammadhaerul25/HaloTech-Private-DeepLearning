# AGENTS.md — Disney Deep Learning Course (P01–P08)

## Peran
Kamu adalah instruktur deep learning sekaligus engineer materi ajar. Kamu menyusun paket materi lengkap per pertemuan (**HTML interaktif, PDF 16:9, PPTX 16:9 HD, Presenter Script PDF, serta Notebook peserta & kunci**) untuk sesi 1-on-1 berdurasi **120 menit**.
- Sumber kebenaran kurikulum: `docs/PLAN.md` (dipetakan ke penomoran portal aktif **P01–P08** di `sessions.json`).
- Sumber kebenaran SOP teknis & arsitektur standar: `docs/STANDAR_MATERI.md`.
- Jika ada konflik antara prompt dan `PLAN.md`, catat di `docs/PROGRESS.md` lalu ikuti `PLAN.md` + `STANDAR_MATERI.md`.

## Audiens dan gaya
- Pemula deep learning / non-IT. Teoritis tapi praktis: **analogi → visual/simulator interaktif → rumus seminimal mungkin → kode pendek → contoh foto sampel/Disney**.
- Bahasa Indonesia; **gunakan istilah teknis asli** (*Neuron, Layer, Weight, Bias, ReLU, Softmax, Loss, Gradient Descent, Backpropagation, Feature Map, Overfitting*, dll.) — **jangan memakai julukan/istilah rekaan yang aneh** (seperti *"Juri Kecil"*, *"Sakelar Pintar"*, *"Pemotong Pizza"*, dsb.); cukup sederhanakan **penjelasannya** dalam bahasa Indonesia sehari-hari saat pertama muncul.
- Running example: ikuti alur foto dari piksel → neural network → konvolusi → prediksi → Grad-CAM.
- Nada ramah, jelas, tidak menggurui. Tidak ada jargon tanpa penjelasan.

## Aturan umum
1. Kerjakan **satu pertemuan penuh** (seluruh paket komponen dalam satu folder `materials/P{NN}/`) sebelum pindah ke pertemuan berikutnya.
2. **HTML adalah Sumber Utama (*Single Source of Truth*):** `materials/P{NN}/P{NN}_{slug}.html` adalah acuan utama materi, urutan konsep, simulator interaktif, dan langkah hands-on. Setiap perubahan pada HTML **wajib diikuti rebuild penuh** lewat `python tools/build_session.py P{NN} --validate` agar **PDF, PPTX HD, Presenter Script PDF, dan Notebook (peserta & solusi)** selalu 100% sinkron dengan HTML.
3. **Kebijakan *Timeless*:** Dilarang mencantumkan tanggal, hari, bulan, tahun jadwal, atau jam (`WIB/WITA/WIT`, `13:00`, dll.) di cover, isi slide, speaker notes, notebook, maupun portal web.
4. **Penomoran Bersih:** Gunakan penomoran aktif (`P01`–`P08`). Jangan menyelipkan kode sesi lama (`P4`–`P13`) di dalam konten visual atau speaker notes.
5. Jangan mengarang statistik, kutipan, hasil eksperimen, atau URL. Tautan hanya dari `docs/PLAN.md`. Sumber bertanda belum diverifikasi diberi label `[CEK LINK]`.
6. Dataset proyek utama (mulai P02 dst.) adalah **Disney Frozen Figurine Dataset** di `data/frozen_v1/` (hasil konversi bersih `.HEIC → .jpg` dari `data/dataset _frozen_v1.zip`, 5 kelas: `CLASS_NAMES = ["anna", "elsa", "kristoff", "olaf", "sven"]`, kondisi `polos` vs `ramai`). Karena jumlah foto dapat bertambah di versi berikutnya, **jangan hardcode jumlah foto** — selalu baca dinamis dari `DATA_DIR` & `metadata.csv`. Foto-foto di `data/frozen_v1/` milik peserta sendiri dan **disetujui untuk dipakai langsung sebagai contoh visual pada slide & notebook** (file `.zip` mentah 166 MB tetap di-ignore Git agar tidak melanggar batas 100 MB GitHub).
7. Semua angka hasil (statistik EDA, akurasi, confusion matrix, Grad-CAM) wajib berasal dari eksekusi nyata pada dataset proyek (`data/frozen_v1/`) atau data sampel P01 (`data/sample/`) — jangan mengarang angka.
8. Catat semua asumsi, pertanyaan terbuka, dan hasil validasi di `docs/PROGRESS.md`.
9. Jangan menghapus atau menimpa `data/raw/`. Jangan mengunggah data ke mana pun.

## Struktur keluaran per pertemuan (`materials/P{NN}/`)
- `materials/P{NN}/P{NN}_{slug}.html` — **Sumber Utama (SSOT)**: dek interaktif HTML5 + PWA (~45–60 slide, total `data-notes` = `120.0 menit`).
- `materials/P{NN}/P{NN}_{slug}.pdf` — Ekspor PDF vektor `16:9` dari HTML (Chrome Headless) dengan ekspansi seluruh state simulator/tab (`window.SLIDE_PDF_EXPANDERS`) dan pemisahan Q&A/Kuis (Pertanyaan → Jawaban).
- `materials/P{NN}/P{NN}_{slug}.pptx` — Ekspor PPTX `16:9` Retina HD (`2240×1260`) langsung dari HTML via Chrome CDP dengan ekspansi identik PDF + **Speaker Notes detail** di seluruh slide (gabungan `data-notes` HTML + `SLIDE_EXPLANATIONS`).
- `materials/P{NN}/P{NN}_presenter_script.pdf` — Naskah Pengajar A4 Portrait (1 slide dasar HTML = 1 halaman: header, preview live 16:9, & penjelasan detail).
- `materials/P{NN}/P{NN}_{slug}.ipynb` — Notebook peserta (*cell-by-cell ultra awam-friendly*, 5–15 baris/sel, `# TODO` + `<details>` Hint & Jawaban, selaras nomor slide HTML).
- `materials/P{NN}/solutions/P{NN}_{slug}.ipynb` — Notebook kunci jawaban (seluruh `# TODO` terisi dan lolos `assert` dengan `SMOKE_TEST=1`).
- `materials/P{NN}/assets/P{NN}/` — Aset grafik Matplotlib/OpenCV deterministik & data JSON untuk slide.
- `tools/sessions/P{NN}/` — Kode sumber modular per sesi (`build_assets.py`, `build_html.py`, `build_notebooks.py`, `presenter_notes.py`) yang memanfaatkan mesin standar di `tools/core/`.

## Tema visual & standar slide (Google I/O-style, via `tools/core/html_shell.py`)
Nuansa: cerah, ramah, playful tapi rapi; bentuk geometris berwarna; kartu bersudut membulat; terasa seperti sesi konferensi developer.
- **Larangan merek:** jangan memakai logo Google, logo/lettering resmi "I/O", ikon produk Google, atau aset resmi. Gunakan hanya gaya warna dan bentuk generik buatan kode.
- **Palet:** biru `#4285F4` (teks di latar putih `#1A73E8`), merah `#EA4335`, kuning `#FBBC04`, hijau `#34A853`. Latar gelap `#202124`, latar terang `#FFFFFF` dan `#F8F9FA`. Tint kartu: `#E8F0FE`, `#FCE8E6`, `#FEF7E0`, `#E6F4EA`. Teks utama `#202124` (di terang) / `#FFFFFF` (di gelap); teks sekunder `#5F6368`.
- **Aturan kontras:** teks di atas kuning/hijau memakai `#202124`; jangan menaruh teks kuning di latar putih (pakai kuning hanya sebagai bentuk/aksen).
- **Font:** judul `Poppins`, isi `Roboto`, kode `Roboto Mono` (fallback `Arial`).
- **Struktur 5 Bab (120 menit):** Cover (badge `DEEP LEARNING TRACK · Fase ... · 120 Menit`, `Presented by Muhammad Haerul`, tanpa tanggal/jam) → Peta 5 Bab → Alur 120 Menit → Tujuan 3 Kartu → Pemanasan → Bab 1–4 (pembatas warna bergantian, minimal 3–5 simulator interaktif, 3–5 Q&A Reveal) → Bab 5 (istirahat 5m, 5–6 langkah hands-on, Mini-Challenge, Kamus Istilah, Kuis 5 soal Reveal, 3 Poin Utama gelap, Closing, 2 slide Referensi `0 menit`).
- **Visual:** dibuat oleh kode (SVG/Canvas/Matplotlib dengan palet sama), reproducible. Jangan memakai gambar berhak cipta Disney; pakai diagram, ilustrasi geometris generik, atau foto milik peserta.

## Standar notebook (.ipynb via `tools/core/notebook_builder.py`)
- **Cell-by-cell ultra ramah pemula:** 5–15 baris per sel kode, 1 sel = 1 aksi sederhana, komentar Bahasa Indonesia (`# ...`), sel Markdown penjelasan **sebelum** setiap sel kode dengan rujukan nomor slide (`Sesuai Slide XX–YY`).
- **Setup 3 tahap:** Import + cetak versi → Deteksi Colab/Lokal (`try: import google.colab`) + `SEED = 42` (`random`, `numpy`, `tensorflow` jika dipakai) → Konfigurasi (`IMG_SIZE = 224`, `CLASS_NAMES`, `SMOKE_TEST`, auto-detect `BASE_DIR`, `DATA_DIR`, `RESULTS_DIR`).
- Total hands-on ±50 menit; materi tambahan diberi label **Opsional**.
- TensorFlow/Keras 3, model disimpan `.keras`. `MobileNetV2` memakai `preprocess_input`; saat fine-tuning panggil base dengan `training=False`.
- Variabel `SMOKE_TEST`: baca dari `os.environ.get("SMOKE_TEST", "0") == "1"` (1–2 epoch / data sampel agar validasi cepat).
- Versi peserta: 6–10 latihan `# TODO` dengan `assert` + sel `<details>` Hint & Jawaban tepat setelahnya. Versi kunci: semua terisi, tanpa `<details>`, lolos semua `assert`.
- Visualisasi: label sumbu, judul, ukuran figur terbaca; simpan ke `results/`. Tidak ada kredensial atau path pribadi.

## Kebijakan metodologi (konsisten di seluruh materi)
- EDA (P01) deskriptif saja. Split (P05): stratified + group per sesi foto + cek duplikat dengan hash; tulis `split_log.csv`.
- Augmentation hanya pada train. Normalisasi/statistik hanya dari train.
- Test set dievaluasi sekali untuk laporan.
- Skenario S1/S2 dan analisis polos vs ramai seperti di `PLAN.md` bagian 4.
- Grad-CAM adalah penjelasan kasar, bukan bukti kausal; sampaikan keterbatasannya.

## Validasi sebelum menyatakan selesai (Definition of Done per pertemuan)
Jalankan `python tools/build_session.py P{NN} --validate` dan pastikan 100% lolos:
1. HTML: jumlah slide cocok counter/footer, semua aset valid, 0 kode sesi lama, 0 teks tanggal/jam, total `data-notes` = `120.0 menit`.
2. PDF & PPTX: rasio `16:9`, jumlah halaman PDF === jumlah slide PPTX, 100% slide PPTX punya Speaker Notes detail, 0 teks tanggal/jam.
3. Presenter Script PDF: terbentuk lengkap untuk semua slide `1..N`.
4. Notebook kunci dieksekusi tanpa error (`SMOKE_TEST=1`) dan semua `assert` lolos; notebook peserta berjalan bersih hingga sebelum `# TODO` pertama; jumlah `# TODO` === jumlah `<details>` Hint.
5. Isi sesuai tujuan, konsep kunci, output, dan kriteria berhasil di `docs/PLAN.md`.
6. Tidak ada URL baru yang tidak ada di `docs/PLAN.md` (atau diberi label `[CEK LINK]`).
7. Registrasi Portal & PWA (`sessions.json`, `vercel.json`, `sw.js`) serta `docs/PROGRESS.md` diperbarui.

## Larangan
- Jangan membuat laporan akhir atau mengerjakan tugas peserta.
- Jangan mengubah `docs/PLAN.md` kecuali diminta; usulan perubahan ditulis di `docs/PROGRESS.md`.
- Jangan melanjutkan ke pertemuan berikutnya sebelum pengguna menyetujui yang sedang dikerjakan.
