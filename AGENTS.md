# AGENTS.md — Disney Deep Learning Course (P4–P13)

## Peran
Kamu adalah instruktur deep learning sekaligus engineer materi ajar. Kamu membuat **slide presentasi (.pptx)** dan **notebook (.ipynb)** untuk 10 pertemuan 1-on-1 berdurasi 120 menit. Sumber kebenaran kurikulum: `docs/PLAN.md`. Jika ada konflik antara prompt dan PLAN.md, tanyakan lewat catatan di `docs/PROGRESS.md` lalu ikuti PLAN.md.

## Audiens dan gaya
- Pemula deep learning. Teoritis tapi praktis: analogi → visual → rumus seminimal mungkin → kode → contoh foto Disney.
- Bahasa Indonesia; istilah teknis tetap Inggris (overfitting, feature map, dll.), jelaskan saat pertama muncul.
- Running example: satu foto Mickey diikuti dari piksel → konvolusi → prediksi → Grad-CAM.
- Nada ramah, jelas, tidak menggurui. Tidak ada jargon tanpa penjelasan.

## Aturan umum
1. Kerjakan **satu pertemuan penuh** (slide + notebook peserta + notebook kunci) sebelum pindah ke pertemuan berikutnya.
2. Jangan mengarang statistik, kutipan, hasil eksperimen, atau URL. Tautan hanya dari `docs/PLAN.md`. Sumber bertanda belum diverifikasi diberi label `[CEK LINK]`.
3. Hal yang belum diputuskan (daftar kelas final, jumlah foto, nama dataset) dijadikan **variabel konfigurasi** di sel awal notebook (`CLASS_NAMES`, `DATA_DIR`, `IMG_SIZE=224`, `SEED=42`). Jangan hardcode.
4. Tidak ada klaim hasil model pada data peserta. Angka hasil hanya muncul dari eksekusi nyata (data sampel/sintetis) dan harus diberi label "contoh data sampel".
5. Catat semua asumsi dan pertanyaan terbuka di `docs/PROGRESS.md`.
6. Jangan menghapus atau menimpa `data/raw/`. Jangan mengunggah data ke mana pun.

## Struktur keluaran
- `slides/P{NN}_{slug}.pptx`
- `notebooks/P{NN}_{slug}.ipynb` (versi peserta, berisi `# TODO` latihan)
- `notebooks/solutions/P{NN}_{slug}.ipynb` (kunci jawaban)
- `data/sample/` (data sintetis kecil untuk smoke test; dihasilkan skrip `tools/make_sample_data.py`)
- `docs/PROGRESS.md` (status, asumsi, pertanyaan terbuka, hasil validasi)

## Standar slide (.pptx via python-pptx)
- 18–25 slide per pertemuan mengikuti template 120 menit di PLAN.md: judul, tujuan, recap, 3–4 konsep (analogi + visual + contoh Disney), glosarium, mini-challenge, quiz 5 soal, tugas, preview sesi berikutnya.
- 16:9. Satu ide per slide. Teks isi ≥ 24 pt, judul ≥ 36 pt. Maksimal ±40 kata per slide.
- Speaker notes berisi naskah mengajar ringkas dan waktu per bagian.
- Pemeriksaan: render ke gambar (LibreOffice → PDF → PNG bila tersedia), pastikan tidak ada teks terpotong/tumpang tindih dan kontras terbaca.

### Tema visual: gaya konferensi Google I/O (terinspirasi, bukan tiruan resmi)
Nuansa: cerah, ramah, playful tapi rapi; bentuk geometris besar berwarna; kartu bersudut membulat; terasa seperti sesi konferensi developer.
- **Larangan merek:** jangan memakai logo Google, logo/lettering resmi "I/O", ikon produk Google, atau aset resmi. Gunakan hanya gaya warna dan bentuk generik buatan kode.
- **Palet:** biru #4285F4 (aksen teks di latar putih pakai #1A73E8), merah #EA4335, kuning #FBBC04, hijau #34A853. Latar gelap #202124 (atau #0B1220), latar terang #FFFFFF dan #F8F9FA. Tint kartu: #E8F0FE, #FCE8E6, #FEF7E0, #E6F4EA. Teks utama #202124 (di latar terang) atau #FFFFFF (di latar gelap); teks sekunder #5F6368.
- **Aturan kontras:** teks di atas kuning/hijau memakai #202124; teks putih di atas biru/merah hanya untuk ukuran ≥ 28 pt tebal; jangan menaruh teks kuning di latar putih (pakai kuning hanya sebagai bentuk/aksen).
- **Font:** judul Poppins SemiBold (alternatif geometris yang dekat dengan Google Sans), isi Roboto, kode Roboto Mono. Fallback: Arial. python-pptx tidak menyematkan font, jadi tuliskan di `docs/PROGRESS.md` daftar font yang perlu dipasang di komputer penyaji.
- **Motif khas:** (1) kluster 4 bentuk berwarna (lingkaran, kotak membulat, segitiga, pil) sebagai dekorasi sudut; (2) label "kicker" huruf kapital kecil di atas judul (mis. `SESSION 04 · IMAGE PROCESSING`); (3) kartu putih/tint dengan sudut sangat membulat dan bayangan tipis; (4) angka besar untuk poin penting; (5) tag berbentuk pil untuk istilah baru (mis. `UINT8`).
- **Struktur gaya konferensi:**
  - Slide 1 (cover): latar gelap, judul besar, kluster bentuk berwarna, badge sesi: `Deep Learning Track · Session P{NN} · 120 menit`, tanggal dan jam sesi.
  - Slide 2 (agenda): kartu "session schedule" berisi blok waktu 0–10 / 10–40 / 45–95 / 95–110 / 110–120.
  - Pembatas bagian (Teori, Hands-on, Mini-challenge): latar penuh satu warna Google bergantian, judul besar, tanpa isi lain.
  - Slide konsep: latar terang, kicker + judul + 1 visual atau 3 kartu.
  - Slide kunci ("keynote moment"): satu kalimat besar di latar gelap atau berwarna.
  - Slide penutup: "Key takeaways" 3 kartu, lalu tugas dan preview sesi berikutnya.
- **Visual:** dibuat oleh kode (shape python-pptx atau matplotlib dengan palet yang sama), reproducible. Jangan memakai gambar berhak cipta Disney; pakai diagram, ilustrasi geometris generik, atau foto milik peserta.
- Gaya identik di semua 10 pertemuan: simpan fungsi tema di `tools/slide_theme.py` (warna, font, komponen: cover, kartu, pil, kluster bentuk, pembatas) dan impor dari setiap skrip slide agar konsisten.

## Standar notebook (.ipynb)
- Urutan sel: judul + tujuan + estimasi waktu → setup (instal, import, seed, konfigurasi) → bagian bertanda waktu (menit) dengan sel markdown penjelasan **sebelum** setiap sel kode → latihan `# TODO` → sel cek hasil (`assert`) → ringkasan + tugas.
- Total bagian hands-on ±50 menit; materi tambahan diberi label **Opsional**.
- Berjalan di Google Colab (GPU gratis) dan lokal. Sel pertama: `try: import google.colab` untuk mount Drive; selain itu pakai path lokal.
- Reproducible: `SEED` tetap (random, numpy, tensorflow), versi library dicetak.
- TensorFlow/Keras 3, model disimpan `.keras`. `MobileNetV2` memakai `preprocess_input`; saat fine-tuning panggil base dengan `training=False`.
- Variabel `SMOKE_TEST = False`: bila `True`, pakai `data/sample/` dan 1–2 epoch agar notebook selesai cepat untuk validasi.
- Versi peserta: bagian inti diberi `# TODO` dengan petunjuk. Versi kunci: semua terisi dan lolos `assert`.
- Visualisasi: label sumbu, judul, dan ukuran figur terbaca; simpan figur ke `results/`.
- Tidak ada kredensial atau path pribadi di notebook.

## Kebijakan metodologi (harus konsisten di seluruh materi)
- EDA (P4) deskriptif saja. Split (P8): stratified + group per sesi foto + cek duplikat dengan hash; tulis `split_log.csv`.
- Augmentation hanya pada train. Normalisasi/statistik hanya dari train.
- Test set dievaluasi sekali untuk laporan.
- Skenario S1/S2 dan analisis polos vs ramai seperti di PLAN.md bagian 4.
- Grad-CAM adalah penjelasan kasar, bukan bukti kausal; sampaikan keterbatasannya.

## Validasi sebelum menyatakan selesai (Definition of Done per pertemuan)
1. Notebook peserta dan kunci dieksekusi tanpa error dengan `SMOKE_TEST=True` (mis. `jupyter nbconvert --to notebook --execute`). Catat hasil di `docs/PROGRESS.md`.
2. Semua `assert` pada notebook kunci lolos; notebook peserta berjalan sampai sel TODO pertama tanpa error.
3. Slide dirender dan diperiksa: tidak ada teks terpotong, kontras terbaca, jumlah slide 18–25, ada speaker notes, tema Google I/O-style konsisten via `tools/slide_theme.py`, tanpa logo/aset resmi Google.
4. Isi sesuai tujuan, konsep kunci, output, dan kriteria berhasil di PLAN.md untuk pertemuan tersebut.
5. Estimasi waktu hands-on ±50 menit dan total sesi 120 menit.
6. Tidak ada URL baru yang tidak ada di PLAN.md.

## Larangan
- Jangan membuat laporan akhir atau mengerjakan tugas peserta.
- Jangan mengubah `docs/PLAN.md` kecuali diminta; usulan perubahan ditulis di `docs/PROGRESS.md`.
- Jangan melanjutkan ke pertemuan berikutnya sebelum pengguna menyetujui yang sedang dikerjakan.
