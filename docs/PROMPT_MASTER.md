# Prompt untuk Antigravity (tempel di Agent chat)

> Cara pakai: (1) Buat folder project kosong `disney-dl-course/`, salin `AGENTS.md` ke root dan `PLAN.md` ke `docs/`. (2) Buka folder itu di Antigravity. (3) Pilih mode **Planning** dan review policy yang meminta persetujuan Anda. (4) Tempel **Prompt Utama** di bawah. (5) Setelah tiap pertemuan selesai dan Anda setujui, tempel **Prompt Per Pertemuan** untuk sesi berikutnya.

## Prompt Utama (jalankan sekali, mulai dari P4)

```
Baca AGENTS.md dan docs/PLAN.md sampai selesai. Keduanya adalah sumber kebenaran.

Tugas: buat materi ajar untuk 10 pertemuan deep learning (P4–P13) dengan project klasifikasi karakter Disney (MobileNetV2). Untuk setiap pertemuan hasilkan: (1) slide .pptx, (2) notebook .ipynb versi peserta, (3) notebook .ipynb versi kunci jawaban, sesuai durasi 120 menit dan template di PLAN.md.

Mulai dengan menyusun implementation plan, lalu kerjakan HANYA P4 sampai selesai:
1. Buat struktur folder sesuai PLAN.md bagian 3 dan docs/PROGRESS.md.
2. Buat tools/make_sample_data.py yang menghasilkan data sampel sintetis kecil di data/sample/ (5 kelas × 2 kondisi, gambar sederhana yang dibuat kode, bukan gambar Disney) lengkap dengan metadata.csv, agar notebook bisa divalidasi tanpa foto asli peserta.
3. Buat tools/slide_theme.py (tema visual gaya konferensi Google I/O sesuai bagian "Tema visual" di AGENTS.md: palet, font, cover bergaya badge sesi, kartu, pil, kluster bentuk, pembatas bagian). Lalu buat slides/P04_image_processing_eda.pptx dengan python-pptx memakai tema itu (18–25 slide, speaker notes). Jangan memakai logo atau aset resmi Google.
4. Buat notebooks/P04_image_processing_eda.ipynb (peserta, ada TODO) dan notebooks/solutions/P04_image_processing_eda.ipynb (kunci).
5. Validasi sesuai "Definition of Done" di AGENTS.md: eksekusi kedua notebook dengan SMOKE_TEST=True, render slide ke gambar dan periksa tata letak.
6. Tulis hasil validasi, asumsi, dan pertanyaan terbuka di docs/PROGRESS.md.

Setelah selesai, BERHENTI dan beri ringkasan: file yang dibuat, hasil validasi, dan hal yang perlu keputusan saya. Jangan lanjut ke P5 sebelum saya menyetujui.

Aturan penting: jangan mengarang statistik, kutipan, atau URL; hal yang belum diputuskan (daftar kelas, jumlah foto) dibuat sebagai variabel konfigurasi; semua teks untuk peserta dalam bahasa Indonesia.
```

## Prompt Per Pertemuan (ganti P05 sesuai urutan)

```
P04 sudah saya setujui. Kerjakan P05 mengikuti AGENTS.md dan bagian P5 di docs/PLAN.md.
Hasilkan slides/P05_*.pptx, notebooks/P05_*.ipynb, dan notebooks/solutions/P05_*.ipynb.
Jaga kontinuitas dengan P04: impor tools/slide_theme.py (tema Google I/O-style yang sama), running example Mickey, dan variabel konfigurasi yang sama.
Validasi sesuai Definition of Done, perbarui docs/PROGRESS.md, lalu berhenti dan ringkas.
Jangan lanjut ke P06 sebelum saya menyetujui.
```

## Prompt Revisi (opsional)

```
Revisi P0X berdasarkan catatan berikut: [tulis catatan]. Ubah hanya file P0X, jalankan ulang validasi, catat perubahan di docs/PROGRESS.md.
```

## Prompt untuk menambah referensi/info baru (saat Anda sudah punya)

```
Saya punya tambahan informasi/referensi: [tempel di sini]. Perbarui docs/PLAN.md bagian yang relevan (asumsi, sumber, atau detail pertemuan) dan catat perubahan di docs/PROGRESS.md. Beri tahu pertemuan mana yang materinya perlu dibuat ulang.
```

## Catatan
- Antigravity membaca `AGENTS.md` di root workspace secara otomatis; file rules punya batas ±12.000 karakter, dan `AGENTS.md` ini dibuat di bawah batas itu.
- Pertemuan dikerjakan satu per satu agar Anda bisa meninjau kualitas dan gaya sebelum diteruskan ke sesi berikutnya.
- Isi `data/raw/` dengan foto Anda sendiri nanti; notebook memakai `DATA_DIR` dan `CLASS_NAMES` sehingga tinggal diganti.
