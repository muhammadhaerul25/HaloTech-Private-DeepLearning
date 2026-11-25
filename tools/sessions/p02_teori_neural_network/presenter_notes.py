"""Naskah Penjelasan Detail per Slide untuk P02: Teori Neural Network (Slide 1 s.d. 59).

Standar penulisan:
- Memakai istilah asli Deep Learning & Computer Vision (AI, ML, DL, Image Classification,
  Object Detection, Instance Segmentation, Object Tracking, Neuron, Input/Hidden/Output Layer,
  Weight, Bias, ReLU, Softmax, Forward Pass, Loss, Gradient Descent, Backpropagation, Epoch,
  MLP, CNN, ResNet, MobileNetV2) dengan penjelasan bahasa Indonesia sehari-hari.
- Dipakai oleh `tools/core/exporter.py` untuk Speaker Notes PPTX (100% slide) dan
  `materials/P02/p02_teori_neural_network_presenter_script.pdf` (A4 Portrait, 1 slide = 1 halaman).
"""

from __future__ import annotations

_ALL_SLIDE_EXPLANATIONS: dict[int, list[str]] = {
    1: [
        "**Tujuan Slide (1 menit):** Menyambut peserta di **P02 — Teori Neural Network** berdurasi 120 menit dan membangun rasa percaya diri bahwa topik besar dari AI sampai Neural Network akan dibedah perlahan.",
        "• **Naskah Pengajar:** \"Di P01 kita sudah berhasil mengubah foto menjadi angka piksel. Hari ini kita melihat peta besarnya dulu — apa beda AI, ML, DL, apa saja tugas Computer Vision, lalu membongkar Neural Network mulai dari 1 neuron terkecil sampai arsitektur modern.\"",
        "• **Sorotan Visual:** Tunjukkan alur di SVG kanan: Foto (Piksel) → Neural Network → Output 5 karakter Frozen.",
    ],
    2: [
        "**Tujuan Slide (2 menit):** Memberikan gambaran utuh sesi 120 menit dalam 1 halaman ringkas — menggabungkan Agenda 5 Bab beserta durasinya (kiri) dan 3 *Learning Goals* konkret (kanan) tanpa pengulangan.",
        "• **Naskah Pengajar:** Bacakan singkat alur 5 bab beserta durasinya (~58 menit pembuka & teori interaktif, 5 menit istirahat, 57 menit praktik notebook, mini-challenge, & kuis), lalu tunjuk 3 target penguasaan di kanan.",
    ],
    3: [
        "**Tujuan Slide (2 menit):** Menyambung akhir P01 langsung ke dataset proyek nyata peserta (`data/frozen_v1/`).",
        "• **Naskah Pengajar:** Tunjukkan galeri 5 karakter Frozen (Anna, Elsa, Kristoff, Olaf, Sven) dalam kondisi Polos dan Ramai. Tekankan bahwa komputer melihat foto bukan sebagai boneka, melainkan matriks angka `(224, 224, 3)` berskala `0.0–1.0`.",
        "• **Catatan Dinamis:** Jumlah foto (`143` di `v1`) dibaca otomatis dari folder dataset agar aman bila foto ditambah nanti.",
    ],
    4: [
        "**Tujuan Slide (1 menit):** Memancing rasa ingin tahu lewat Q&A #1 sebelum masuk Bab 1.",
        "• **Aktivitas Kelas:** Tunjukkan foto Elsa berlatar rak ramai. Minta peserta menebak A, B, atau C sebelum klik jawaban. Kunci: **B** (belajar dari contoh foto berlabel lewat Neural Network).",
    ],
    5: [
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 1: AI vs Machine Learning vs Deep Learning**.",
        "• **Naskah Pengajar:** \"Sebelum menyentuh istilah teknis visi komputer, mari kita luruskan dulu tiga istilah yang paling sering tertukar di media: AI, ML, dan DL.\"",
    ],
    6: [
        "**Tujuan Slide (1.5 menit):** Menyampaikan definisi **Artificial Intelligence (AI)** yang akurat — sistem yang mampu mengamati lingkungan (*perceive*), menalar/memutuskan (*reason*), dan bertindak (*act*) untuk mencapai tujuan — lewat 3 kartu perbandingan jernih.",
        "• **Naskah Pengajar:** Bandingkan kiri ke kanan: **Bukan AI** (automasi statis: kalkulator, *vending machine*, menu tombol `1-2-3`), **AI Klasik** (tanpa ML: AI catur *Deep Blue / Minimax*, navigasi rute *A**, dan *Expert System* dengan *inference engine*), lalu **AI Modern** (belajar pola dari data: *Face Unlock*, rekomendasi konten, asisten LLM, dan proyek Frozen kita).",
    ],
    7: [
        "**Tujuan Slide (2 menit):** Membandingkan **Pemrograman Tradisional** vs **Machine Learning (ML)** lengkap dengan 2 tahap (*Training → Prediksi*) lewat Simulator #1.",
        "• **Panduan Demo Simulator #1:** Klik tab 1 (`Pemrograman Tradisional`: Data + Aturan Manual → Jawaban) lalu tab 2 (`Machine Learning`: Tahap 1 Training `Data + Label → Algoritma ML → Model`, lalu Tahap 2 Prediksi `Foto Baru → Model → Elsa!`). Jelaskan singkat *Supervised Learning* = belajar dengan kunci jawaban.",
    ],
    8: [
        "**Tujuan Slide (1.5 menit):** Menjelaskan posisi **Deep Learning (DL)** sebagai cabang ML yang memakai Neural Network berlapis banyak lewat Simulator #2.",
        "• **Panduan Demo Simulator #2:** Gunakan tab `Recap AI` & `Recap ML` singkat (20 detik) lalu fokus ke tab `Deep Learning`: fitur tidak perlu diekstrak manual oleh manusia karena jaringan saraf mempelajarinya otomatis dari piksel.",
    ],
    9: [
        "**Tujuan Slide (2 menit):** Membedakan secara tajam **Machine Learning (ML klasik)** vs **Deep Learning (DL)** dari sisi algoritma inti dan cara mendapatkan fitur gambar.",
        "• **Naskah Pengajar:** Tunjuk alur atas (ML Klasik): memakai algoritma matematika/statistik (*Random Forest, SVM, Regression*) yang butuh fitur jelas — sehingga untuk foto, **manusia harus mengekstrak fitur secara manual** (warna, tepi, tekstur). Bandingkan dengan alur bawah (DL): memakai **Neural Network** berlapis banyak di mana **AI mempelajari fiturnya sendiri otomatis** dari piksel mentah!",
    ],
    10: [
        "**Tujuan Slide (1.5 menit):** Mengunci pemahaman Bab 1 lewat Q&A #2.",
        "• **Aktivitas Kelas:** Minta peserta menempatkan proyek klasifikasi 5 karakter Frozen (memakai Neural Network berlapis banyak) di peta `AI ⊃ ML ⊃ DL`. Kunci: **C** (Deep Learning, sekaligus bagian dari ML dan AI).",
    ],
    11: [
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 2: Task Computer Vision**.",
        "• **Naskah Pengajar:** \"Di dalam Deep Learning, cabang yang khusus mengolah gambar dan video disebut **Computer Vision**. Mari lihat 4 tugas paling populernya.\"",
    ],
    12: [
        "**Tujuan Slide (2 menit):** Memperlihatkan perbandingan keempat tugas utama CV secara berdampingan pada **satu foto Elsa yang sama** sebelum membedah tiap tugas di Slide 13–16.",
        "• **Naskah Pengajar:** Arahkan mata dari kiri ke kanan pada gambar 4-panel (Classification → Detection → Semantic & Instance Segmentation dengan mask siluet presisi → Object Tracking). Tegaskan bahwa overlay adalah **ilustrasi buatan kode** di atas foto asli peserta.",
    ],
    13: [
        "**Tujuan Slide (1 menit):** Membedah **Image Classification** sebagai tugas proyek akhir kita.",
        "• **Naskah Pengajar:** Input = 1 gambar utuh; Output = 1 label kategori + probabilitas tiap kelas. Beri jembatan ke Bab 3: karena ada 5 kelas Frozen, *Output Layer*-nya punya tepat 5 neuron.",
    ],
    14: [
        "**Tujuan Slide (1 menit):** Membedah **Object Detection** (banyak objek sekaligus + kotak koordinat *bounding box*).",
        "• **Naskah Pengajar:** Jelaskan output ganda: selain label kelas, model juga menebak 4 angka koordinat kotak `(x, y, w, h)` untuk setiap objek di dalam foto.",
    ],
    15: [
        "**Tujuan Slide (1.5 menit):** Membedah **Semantic and Instance Segmentation** serta perbedaannya secara visual.",
        "• **Naskah Pengajar:** Tunjuk diagram kanan: pada *Semantic Segmentation*, dua Olaf digabung dalam 1 warna kelas; pada **Instance Segmentation**, Olaf #1 dan Olaf #2 dipisahkan sebagai dua individu berbeda dengan *mask* piksel presisi.",
    ],
    16: [
        "**Tujuan Slide (1 menit):** Membedah **Object Tracking** pada video (*detection* + *ID tracking* antar-frame).",
        "• **Naskah Pengajar:** Tunjuk panah dari `Frame t=1 → t=2 → t=3` dengan `ID #1` yang konsisten. Catat bahwa ini wawasan lengkap karena proyek Frozen kita memakai foto tunggal.",
    ],
    17: [
        "**Tujuan Slide (1.5 menit):** Latihan interaktif Simulator #4 — mencocokkan 4 kasus nyata dengan task CV yang tepat.",
        "• **Aktivitas Kelas:** Bacakan 4 skenario satu per satu (penyakit daun → Classification; kasir nampan → Detection; potong rambut → Segmentation; CCTV jalan tol → Tracking), minta peserta memilih, lalu klik tombolnya.",
    ],
    18: [
        "**Tujuan Slide (1.5 menit):** Q&A #3 untuk mengunci pilihan task proyek Frozen.",
        "• **Aktivitas Kelas:** Minta peserta memilih A, B, atau C lalu jelaskan alasannya. Kunci: **A** (*Image Classification* multi-kelas 5 kelas). Latar ramai tidak mengharuskan kita ganti ke segmentation.",
    ],
    19: [
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 3: Bedah Total Neural Network (Terkecil → Terbesar)**.",
        "• **Naskah Pengajar:** \"Sekarang kita masuk ke jantung sesi ini. Kita bongkar Neural Network mulai dari unit paling kecil (1 Neuron) sampai terbentuk jaringan utuh.\"",
    ],
    20: [
        "**Tujuan Slide (1.5 menit):** Memulai Bab 3 dari unit paling konkret — **1 Neuron** sebagai wadah pemegang **1 nilai angka**, khususnya 1 angka piksel biru gaun Elsa (`0.42`).",
        "• **Panduan Demo Interaktif:** Klik **`▶ Play`** agar peserta melihat foto Elsa di-*zoom* menjadi grid `8×8`, 1 kotak piksel biru gaun Elsa (`Baris 5, Kol 3 · 0.42`) terangkat menjadi kartu nilai piksel lalu berubah bentuk (*morph*) menjadi lingkaran biru **1 Neuron**. Klik **`⏭ Piksel Lain`** atau klik langsung kotak mana saja di grid `8×8` (rambut, dinding, tangan) untuk menunjukkan setiap piksel punya nilai & neuronnya sendiri.",
    ],
    21: [
        "**Tujuan Slide (1.5 menit):** Memperlihatkan **animasi langsung proses `Flatten`** — tiap piksel foto Elsa (`4×4` = 16 piksel nyata) dipindai dari **kiri ke kanan, atas ke bawah**, lalu terbang dan ditumpuk vertikal menjadi **1 kolom `Input Layer`**.",
        "• **Panduan Demo Animasi Interaktif:** Klik **`▶ Play`** (atau klik **`⏭ +1 Piksel`** satu per satu sambil menjelaskan) agar peserta melihat Baris 1 biru (`x₁..x₄`) → Baris 2 merah (`x₅..x₈`) → Baris 3 kuning (`x₉..x₁₂`) → Baris 4 hijau (`x₁₃..x₁₆`) mendarat berurutan dari atas ke bawah menjadi **Input Layer**.",
    ],
    22: [
        "**Tujuan Slide (2 menit):** Memperlihatkan secara besar, detail, & **beranimasi per-piksel** transformasi 3 tahap foto menuju **Input Layer**: (1) Foto Original Elsa (`H`, `W`, `C`); (2) Hasil *Flatten* 1D dengan kurung kurawal `}` perkalian `H × W × C = Total Neuron`; dan (3) Kolom **Input Layer** berisi lingkaran neuron angka nyata `0.0–1.0`.",
        "• **Panduan Demo Interaktif Per-Piksel:** Klik **`▶ Play`** (atau **`⏭ +1 Piksel`** / klik langsung kotak piksel mana saja pada **Foto Elsa**) agar peserta melihat kotak piksel nyata terbang ke Pita 1D lalu pecah di udara menjadi 3 bola `R, G, B` yang mendarat ke lingkaran `x₁, x₂, x₃`! Klik lingkaran neuron mana saja di kanan untuk menampilkan garis jejak balik ke asalnya, lalu bandingkan `64×64×1 (Gray)` vs `64×64×3 (RGB)` vs `224×224×3 (RGB)`.",
    ],
    23: [
        "**Tujuan Slide (2 menit):** Menyambungkan **Input Layer** langsung ke **Output Layer** dalam 4 tahap bernomor yang sinkron antara ilustrasi atas dan 4 kartu penjelasan di bawahnya: `1. Foto Original` → `2. Input Layer` → `3. Output Layer` → `4. Hasil Klasifikasi`.",
        "• **Panduan Demo Interaktif (`▶ Play` / `⏭ +1 Langkah`):** Jalankan animasi agar peserta melihat alur penuh dari piksel ke neuron (`x₁..x₆` hingga `x150.528`), lalu kalkulasi probabilitas kelas lewat koneksi neuron demi neuron ke seluruh 5 output (`y₁..y₅`), hingga bola `89%` meluncur ke hasil klasifikasi `ELSA`. Klik langsung piksel foto, salah satu neuron Input, atau salah satu kelas Output untuk menyorot koneksinya!",
        "• **Aturan Kunci yang Akurat secara Ilmiah:** Tekankan kotak catatan bawah: (1) **Ukuran piksel × channel gambar (`H × W × C`)** menentukan jumlah neuron di **Input Layer** pada MLP (grayscale `C=1` → tepat `H×W`; RGB `C=3` → `3×` lebih banyak karena tiap piksel punya 3 nilai R, G, B); (2) **Jumlah kelas gambar** menentukan jumlah neuron di **Output Layer** untuk klasifikasi multi-kelas (5 kelas Frozen → 5 neuron + Softmax; pengecualian: untuk klasifikasi biner 2 kelas sering cukup 1 neuron Sigmoid, dan untuk task seperti *Regression* atau *Detection* jumlah output mengikuti target tugasnya).",
        "• **Transisi ke Slide 24:** \"Pertanyaannya sekarang: bagaimana jaringan bisa tahu secara matematis bahwa input ini gambar Elsa? Mari kita lihat simulasi training langsung di slide berikutnya!\"",
    ],
    24: [
        "**Tujuan Slide (3.5 menit — Tahap 4):** Menjawab secara konkret & matematis bagaimana Neural Network bisa tahu foto ini adalah **Elsa** (atau karakter lain) lewat **Simulasi Training** pada 5 foto nyata Frozen berlabel (`Anna, Elsa, Kristoff, Olaf, Sven`), memakai **jumlah neuron Input Layer asli `150.528` (`224×224×3`)** persis seperti Slide 22–23, dengan menyorot 2 tahap hitungan: **Tahap 4.1 Weight + Bias (`z = Σ(x·w) + b`)** dan **Tahap 4.2 Activation Function (`Softmax`)**.",
        "• **Panduan Demo Interaktif:** Tunjukkan bahwa `Input Layer` memakai **jumlah neuron asli `150.528`** (`x₁, x₂, x₃`, elipsis **`⋮ +150.522 neuron piksel`**, `x₁₅₀.₅₂₆, x₁₅₀.₅₂₇, x₁₅₀.₅₂₈`) ditambah node **`+1 · Bias`**. Klik **`Sebelum Training (Acak)`** dulu agar peserta melihat bobot acak menghasilkan tebakan salah (`Elsa 14.4%`, kalah dari Kristoff `45.8%`). Lalu klik **`▶ Play`** (atau **`⏭ +1 Tahap Hitung`** / **`↺ Reset`**): sorot bagaimana piksel pojok latar bobotnya mengecil mendekati `w ≈ 0` (diabaikan), sementara `150.522` piksel objek membawa sumbangan utama (`Σ = +3.17`), ditambah `Bias (-1.04)` → `z₂ = +2.13` → Softmax `e^(+2.13) / 10.82 = 77.7% ✅` (5/5 kelas tepat!).",
        "• **Transisi ke Tahap 4.1 (Slide 25):** \"Di kotak kuning dan kotak hijau tadi ada mesin inti yang bekerja: **Weight + Bias**, **Activation Function**, dan **Output Akhir**. Mari kita bedah masing-masing secara khusus di tiga slide berikutnya!\"",
    ],
    25: [
        "**Tujuan Slide (3 menit — Tahap 4.1):** Membedah khusus **Tahap 4.1 (`Weight & Bias`)** secara runtut (Apa itu, Kenapa perlu, Cara kerja) dengan **diagram Zoom-In kabel nyata `150.528` neuron dari Tahap 4** yang persis sama angkanya per setiap karakter (`Anna, Elsa, Kristoff, Olaf, Sven`).",
        "• **Panduan Demo Interaktif (Kontinuitas Tahap 4 → 4.1):** Tunjuk strip peta atas (`📍 Posisi di Tahap 4: Input 150.528 → 🔍 Tahap 4.1: Weight + Bias → z → Tahap 4.2`). Tunjukkan bahwa angka Elsa di sini (`Σ 150.522 piksel = +3.17`, piksel sudut `w ≈ 0`, `b₂ = -1.04`, `z₂ = +2.13 → Softmax 77.7%`) adalah **zoom-in persis dari Tahap 4**! Klik **`▶ Play`** atau klik chip 5 karakter, lalu uji **`Coba Bias = 0`** (coba juga pada Olaf/Sven agar terlihat peluang turun drastis tanpa *Bias*), **`Coba Balik Weight`** (kabel 150.522 piksel berbalik merah → Elsa jatuh ke `0.5% ❌`), geser 2 slider bawah, dan klik **`↺ Reset`** untuk kembali!",
        "• **Transisi ke Tahap 4.2 (Slide 26):** \"Lihat kotak hijau di bawah neuron tadi: setelah Tahap 4.1 menghasilkan skor mentah `z₂ = +2.13`, angkanya langsung masuk ke **Tahap 4.2: Activation Function** — mari kita zoom-in di slide berikutnya!\"",
    ],
    26: [
        "**Tujuan Slide (3 menit — Tahap 4.2):** Membedah khusus **Tahap 4.2 (`Activation Function`)** secara runtut (Apa itu, Kenapa wajib ada *Non-Linearity*, Cara kerja `ReLU / Sigmoid / Softmax`) lewat **diagram SVG Zoom-In langsung dari skor mentah `z` hasil Tahap 4.1**!",
        "• **Panduan Demo Interaktif (Kontinuitas Tahap 4.1 → 4.2):** Tunjuk strip peta atas (`📍 Posisi di Tahap 4: Tahap 4.1 → 🔍 Tahap 4.2: Activation Function → Tahap 4.3`). Klik **`▶ Play`** atau pilih foto Anna/Elsa/Kristoff/Olaf/Sven, lalu berpindah tab **`1. ReLU`** (tunjukkan seluruh 4 skor negatif Elsa langsung dipotong jadi `0.00 ✕` sedangkan `z₂=+2.13` lolos!), **`2. Sigmoid`** (peras `z₂=+2.13` di kurva-S jadi `89.4% Elsa`), dan **`3. Softmax`** (tunjukkan kotak `e^z / Σe^z = 8.41 / 10.82 = 77.7%` **persis sama dengan Tahap 4**!). Geser slider `Geser z` ke minus untuk melihat output langsung berubah, lalu klik **`↺ Reset`** di bar atas untuk kembali ke nilai asli!",
        "• **Transisi ke Tahap 4.3 (Slide 27):** \"Setelah Softmax menghasilkan 5 angka probabilitas di atas, bagaimana model memutuskan 1 jawaban akhir, menilai apakah ia yakin atau ragu, lalu menghitung Error? Mari kita zoom-in **Tahap 4.3: Output Akhir** di slide berikutnya!\"",
    ],
    27: [
        "**Tujuan Slide (2.5 menit — Tahap 4.3):** Melengkapi trilogi Zoom-In dari Tahap 4 (**Tahap 4.1 → 4.2 → 4.3 Output Akhir**): menunjukkan bagaimana 5 probabilitas Softmax diubah menjadi 1 keputusan lewat **`Argmax`**, dicek keyakinannya (*Confidence* vs *Threshold*), lalu dibandingkan dengan **Label Asli** untuk menghitung **Error & Cross-Entropy Loss**.",
        "• **Panduan Demo Interaktif (`▶ Play` / `■ Stop` / `↺ Reset`):** Tunjuk strip peta atas (`📍 Posisi di Tahap 4: Tahap 4.1 → Tahap 4.2 → 🔍 Tahap 4.3: Output Akhir & Error → Tahap 5`). Di mode **`1. Terlatih`**, tunjukkan seluruh 5 karakter Frozen lolos yakin (`Elsa 77.7%`, `Anna 83.0%`, `Olaf 79.2%`). Lalu klik **`2. Ragu (Tipis)`** (`Elsa 41.9% ⚠ Ragu` di bawah ambang `60%`) dan geser slider **`Ambang Yakin (Threshold)`** dari `40%` ke `80%`. Terakhir klik **`3. Acak (Belum Latih)`** pada foto **Olaf** (`P=11.3%`, salah menebak `Kristoff 46.0%`, `Error = 88.7%`, `Loss = 2.18`) — tekankan bahwa angka *Error/Loss* besar inilah yang dikirim balik untuk mengoreksi bobot saat *Training*!",
        "• **Transisi ke Tahap 5 (Slide 28):** \"Tadi kita lihat foto Olaf yang belum dilatih punya **Error 88.7% (Loss 2.18)**. Bagaimana caranya angka Loss besar ini mengubah *Weight* & *Bias* sampai Olaf dikenali 79.2%? Mari lihat **Tahap 5: Siklus Belajar Utuh**!\"",
    ],
    28: [
        "**Tujuan Slide (1.5 menit):** Membedah koneksi *Fully Connected / Dense* — menelusuri tepat **1 neuron input** ke seluruh **5 neuron output**.",
        "• **Panduan Demo Simulator:** Klik tombol `x₁`, `x₂`, `x₃`, `x₄` bergantian. Tekankan satu hal: 1 neuron input saja sudah punya **5 garis weight** (`w₁,₁` sampai `w₁,₅`).",
    ],
    29: [
        "**Tujuan Slide (1 menit):** Menghitung jumlah weight & bias **tanpa hidden layer** untuk foto `224×224×3` ke 5 kelas.",
        "• **Naskah Pengajar:** Tunjukkan hitungan persis: `150.528 × 5 = 752.640` weight + `5` bias = `752.645` parameter. Lalu jelaskan mengapa 1 lapisan lurus saja belum mampu memahami bentuk kompleks.",
    ],
    30: [
        "**Tujuan Slide (1 menit):** Menjelaskan mengapa kita menambahkan **Hidden Layer** di antara Input dan Output.",
        "• **Naskah Pengajar:** Telusuri 4 kartu dari kiri ke kanan: piksel mentah → tepi & warna dasar → bagian bentuk objek → keputusan 5 karakter. Sampaikan bahwa tumpukan banyak *Hidden Layer* inilah asal kata **Deep Learning**.",
    ],
    31: [
        "**Tujuan Slide (1 menit):** Menampilkan diagram utuh **Multi-Layer Perceptron (MLP)**: `Input Layer → Hidden Layer (+ ReLU) → Output Layer (+ Softmax)`.",
        "• **Naskah Pengajar:** Tunjukkan simbol `W₁, b₁` dan `W₂, b₂`. Aliran perhitungan maju dari kiri ke kanan disebut **Forward Pass**.",
    ],
    32: [
        "**Tujuan Slide (1.5 menit):** Momen \"Aha!\" — menghitung lonjakan parameter ketika menambahkan **Hidden Layer**.",
        "• **Panduan Demo Simulator:** Tunjukkan posisi standar `224×224×3` dengan `128` neuron hidden = **`19.268.357` parameter** (`19,27` juta!). Bandingkan dengan tombol `64×64×3` (`1,57` juta). Tunjukkan bahwa 99,99% parameter menumpuk di Layer 1.",
    ],
    33: [
        "**Tujuan Slide (2.5 menit):** Menunjukkan **Forward Pass** langkah demi langkah memakai **4 piksel nyata** dari foto Elsa (`x = [0.76, 0.74, 0.65, 0.65]`).",
        "• **Panduan Demo Simulator:** Klik tombol 1 → 2 → 3 → 4 perlahan. Tunjukkan bahwa tidak ada sihir: hanya perkalian, penjumlahan bias, ReLU, dan Softmax hingga keluar probabilitas `87.47%` Elsa.",
    ],
    34: [
        "**Tujuan Slide (1 menit):** Q&A #4 mengecek kemampuan peserta menghitung parameter 1 layer secara manual.",
        "• **Aktivitas Kelas:** Minta peserta menghitung `4 input → 2 hidden` dengan rumus `(4 × 2) + 2 = 10` (Kunci: **C**). Ingatkan untuk tidak melupakan angka bias.",
    ],
    35: [
        "**Tujuan Slide (1.5 menit):** Masuk ke bagian intuitif *bagaimana network belajar*: memperkenalkan **Loss Function** (Cross-Entropy).",
        "• **Naskah Pengajar:** Tunjuk panel kiri grafik (`05_loss_gradient_descent_overview.png`): jika foto Elsa diberi probabilitas rendah (`10%`), hukumannya besar (`Loss = 2.30`); jika diberi `90%`, `Loss = 0.11`. Makin kecil Loss = makin bagus!",
    ],
    36: [
        "**Tujuan Slide (1.5 menit):** Menjelaskan **Gradient Descent** sebagai \"turun bukit mencari error terkecil\" serta efek **Learning Rate**.",
        "• **Panduan Demo Simulator:** Klik `LR Kecil` (lambat), `LR Ideal` (mulus ke dasar `Loss = 0.002`), lalu `LR Besar` (memantul liar/divergen). Tanpa rumus turunan berat, cukup intuisi arah turun dan lebar langkah.",
    ],
    37: [
        "**Tujuan Slide (1.5 menit):** Mengenalkan **Backpropagation** sekilas secara intuitif.",
        "• **Naskah Pengajar:** Tunjuk panah biru (maju: *Forward Pass*) dan panah merah putus-putus (mundur: *Backpropagation*) serta 3 kartu langkah di bawahnya. Tenangkan peserta: seluruh perhitungan arah koreksi dikerjakan otomatis oleh Keras saat `model.fit()` dipanggil.",
    ],
    38: [
        "**Tujuan Slide (1 menit):** Merangkum satu siklus penuh training (**Tebak → Ukur Loss → Koreksi → Ulangi**) dan arti **Epoch**.",
        "• **Naskah Pengajar:** Jelaskan 1 *Epoch* = 1 putaran penuh membaca seluruh data latih. Beri preview bahwa detail diagnosis kurva *Train vs Val Loss* & *Overfitting* akan diperdalam di P03.",
    ],
    39: [
        "**Tujuan Slide (1 menit):** Mengunci seluruh Bab 3 lewat tangga hierarki dari unit terkecil (**1 Neuron**) hingga sistem belajar (**Training Loop**).",
        "• **Naskah Pengajar:** Baca cepat nomor 1 sampai 5 dan tanyakan apakah ada satu tangga yang masih terasa mengganjal sebelum pindah ke Bab 4.",
    ],
    40: [
        "**Tujuan Slide (1 menit):** Q&A #5 menutup Bab 3 — memastikan peserta paham arah baca nilai Loss yang menurun.",
        "• **Aktivitas Kelas:** Kunci: **B** (Loss turun dari `1.65` ke `0.35` berarti bobot berhasil diperbaiki oleh Gradient Descent sehingga kesalahan mengecil).",
    ],
    41: [
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 4: Peta Arsitektur Neural Network untuk Computer Vision (Teaser)**.",
        "• **Naskah Pengajar:** \"Di Bab 4 yang singkat ini, kita sambungkan temuan 19,27 juta parameter tadi ke peta arsitektur CV modern — cukup secara konseptual dulu sebagai jembatan ke P03 dan P04.\"",
    ],
    42: [
        "**Tujuan Slide (1.5 menit):** Menunjukkan 2 kelemahan utama **MLP** pada foto (`06_mlp_vs_cnn_preview.png`): boros parameter dan peka pergeseran objek akibat *Flatten*.",
        "• **Naskah Pengajar:** Bandingkan kiri (MLP mengiris foto 1D) vs kanan (CNN menggeser filter kecil `3×3` di foto 2D utuh — jauh lebih hemat bobot & tahan geser).",
    ],
    43: [
        "**Tujuan Slide (2 menit):** Menelusuri peta evolusi arsitektur CV (`MLP → CNN → ResNet → MobileNetV2`).",
        "• **Panduan Demo Simulator:** Klik keempat tombol secara berurutan. Tekankan bahwa di P02 cukup kenal ide besar dan alasannya; detail konvolusi dibedah di P03 dan *Transfer Learning* di P04.",
    ],
    44: [
        "**Tujuan Slide (1 menit):** Menghubungkan Task CV (Bab 2) dengan contoh keluarga arsitektur populernya dan menjelaskan alasan pemilihan **MobileNetV2** untuk proyek Frozen.",
        "• **Naskah Pengajar:** Tunjuk 3 kartu (Classification: ResNet/MobileNetV2; Detection: YOLO/Faster R-CNN; Segmentation: U-Net/Mask R-CNN) lalu bacakan 3 alasan memilih MobileNetV2.",
    ],
    45: [
        "**Tujuan Slide (1 menit):** Q&A #6 menutup sesi teori — mengunci alasan pindah dari MLP ke CNN.",
        "• **Aktivitas Kelas:** Kunci: **B** (MLP merusak struktur 2D lewat Flatten dan meledakkan parameter hingga jutaan).",
    ],
    46: [
        "**Tujuan Slide (5 menit):** Jeda istirahat wajib 5 menit sebelum masuk ke sesi praktik **Hands-On Notebook**.",
        "• **Catatan Instruktur:** Ajak peserta minum air & istirahatkan mata. Pastikan file `materials/P02/p02_teori_neural_network.ipynb` dan folder `data/frozen_v1/` siap dibuka.",
    ],
    47: [
        "**Tujuan Slide (6 menit — Hands-On Langkah 1):** Mendampingi peserta menjalankan Setup 3 tahap dan membaca `metadata.csv` foto Frozen secara dinamis.",
        "• **Panduan Praktik:** Pastikan `SEED = 42` terkunci, `DATA_DIR` mengarah ke `data/frozen_v1`, dan 5 foto karakter Frozen tampil dengan benar.",
    ],
    48: [
        "**Tujuan Slide (6 menit — Hands-On Langkah 2):** Mendampingi peserta melakukan `.flatten()` foto Elsa dan mengerjakan `# TODO 1` serta `# TODO 2`.",
        "• **Panduan Praktik:** Minta peserta membuktikan sendiri panjang vektor `64×64×3 = 12.288` dan `224×224×3 = 150.528` sesuai Slide 21–22.",
    ],
    49: [
        "**Tujuan Slide (6 menit — Hands-On Langkah 3):** Mendampingi peserta mengerjakan `# TODO 3` (1 Neuron + ReLU) dan `# TODO 4` (Softmax manual) serta memverifikasi Forward Pass 4 piksel nyata Elsa di NumPy.",
        "• **Tips Mengajar:** Biarkan peserta mencoba mengetik sendiri dulu sebelum membuka kotak `<details>` Hint.",
    ],
    50: [
        "**Tujuan Slide (6 menit — Hands-On Langkah 4):** Mendampingi peserta memuat foto Frozen ukuran `64×64×3` dan mengerjakan `# TODO 5` membangun MLP kecil di Keras.",
        "• **Catatan Penting:** Tegaskan kembali bahwa MLP ini hanya demo konsep untuk memahami layer dan parameter, bukan model akhir proyek.",
    ],
    51: [
        "**Tujuan Slide (7 menit — Hands-On Langkah 5):** Mendampingi peserta mengerjakan `# TODO 6` melatih MLP singkat dan memplot kurva *Training Loss*.",
        "• **Panduan Diskusi:** Amati apakah kurva Loss turun tiap epoch, dan ingatkan bahwa pembagian data resmi anti-leakage (Group Split) akan dipelajari di P05.",
    ],
    52: [
        "**Tujuan Slide (7 menit — Hands-On Langkah 6):** Mendampingi peserta membaca `mlp.summary()` dan mengerjakan `# TODO 7` mencocokkan hitungan tangan parameter dengan `mlp.count_params()`.",
        "• **Momen Aha:** Pastikan peserta merasakan kepuasan saat `assert hitung_manual == mlp.count_params()` lolos 100%!",
    ],
    53: [
        "**Tujuan Slide (5 menit — Mini-Challenge):** Meminta peserta menebak dampak mengubah jumlah neuron hidden (`32` vs `64` vs `128`) sebelum menjalankan `# TODO 8` di notebook.",
        "• **Poin Diskusi:** Parameter naik proporsional `2×` saat hidden naik `2×`, namun lebih banyak parameter pada dataset kecil juga memperbesar risiko menghafal data latih (*overfitting*).",
    ],
    54: [
        "**Tujuan Slide (2 menit):** Mengulas singkat 12 istilah asli Teori Neural Network di Kamus Istilah.",
        "• **Interaksi:** Tanyakan ke peserta apakah ada 1–2 istilah yang masih ingin diperjelas ulang sebelum kuis.",
    ],
    55: [
        "**Tujuan Slide (4 menit):** Kuis interaktif 5 soal mencakup Bab 1 sampai Bab 4.",
        "• **Aktivitas Kelas:** Minta peserta menjawab kelima soal secara lisan dulu, lalu klik tombol `Lihat Jawaban` satu per satu untuk konfirmasi bersama.",
    ],
    56: [
        "**Tujuan Slide (2 menit):** Mengunci sesi hari ini dengan 3 Poin Utama di slide gelap.",
        "• **Naskah Pengajar:** Bacakan 3 pilar: (01) Peta AI/ML/DL & Image Classification; (02) Struktur Neuron → Layer → Forward Pass → Training; (03) Batasan MLP menjadi jembatan kuat menuju CNN di P03.",
    ],
    57: [
        "**Tujuan Slide (2 menit):** Menutup kelas dengan apresiasi, tugas ringan mandiri opsional, dan preview menarik untuk **P03 (Training Neural Network & Konvolusi CNN)**.",
        "• **Catatan Referensi:** Arahkan peserta ke Slide 58–59 untuk tautan video 3Blue1Brown & sumber resmi belajar mandiri.",
    ],
    58: [
        "**Tujuan Slide (0 menit — Referensi Mandiri 1/2):** 6 tautan rujukan utama Neural Network & ML dasar sesuai `docs/PLAN.md` (sumber belum diverifikasi ulang diberi label `[CEK LINK]`).",
        "• **Catatan Penggunaan:** Tidak perlu dibahas panjang di kelas; rekomendasikan video 3Blue1Brown #1 sebagai tontonan opsional terbaik di rumah.",
    ],
    59: [
        "**Tujuan Slide (0 menit — Referensi Mandiri 2/2):** 6 tautan rujukan Computer Vision, CNN Explainer, ResNet, dan MobileNetV2 sesuai `docs/PLAN.md` sebagai jembatan menuju P03 dan P04.",
    ],
}

# Sinkron otomatis dengan flag HIDE_SLIDES_28_40 & HIDE_BAB4_ARCH di build_html.py:
# seluruh 59 naskah tetap tersimpan di _ALL_SLIDE_EXPLANATIONS agar bisa dimunculkan kembali kapan saja.
try:
    from sessions.p02_teori_neural_network.build_html import HIDE_BAB4_ARCH, HIDE_SLIDES_28_40  # type: ignore
except Exception:
    try:
        from build_html import HIDE_BAB4_ARCH, HIDE_SLIDES_28_40  # type: ignore
    except Exception:
        HIDE_SLIDES_28_40 = True
        HIDE_BAB4_ARCH = True

if HIDE_SLIDES_28_40:
    SLIDE_EXPLANATIONS: dict[int, list[str]] = {}
    _new_idx = 1
    _post_bab3_order = (
        [55, 54, 58, 59, 46, 47, 48, 49, 50, 51, 52, 56]
        if HIDE_BAB4_ARCH
        else list(range(41, 60))
    )
    _orig_sequence = list(range(1, 28)) + _post_bab3_order
    for _orig_idx in _orig_sequence:
        _notes = list(_ALL_SLIDE_EXPLANATIONS[_orig_idx])
        if _orig_idx == 1 and HIDE_BAB4_ARCH:
            _notes[0] = (
                "**Tujuan Slide (1 menit):** Menyambut peserta di **P02 — Teori Neural Network** berdurasi 120 menit dan membangun rasa percaya diri bahwa topik besar dari AI sampai Neural Network akan dibedah perlahan dalam 3 bab terstruktur."
            )
            _notes[1] = (
                "• **Naskah Pengajar:** \"Di P01 kita sudah berhasil mengubah foto menjadi angka piksel. Hari ini kita melihat peta besarnya dulu — apa beda AI, ML, DL, apa saja tugas Computer Vision, lalu membongkar Neural Network dari 1 piksel sampai Backpropagation, ditutup kuis dan praktik langsung.\""
            )
        elif _orig_idx == 2 and HIDE_BAB4_ARCH:
            _notes[0] = (
                "**Tujuan Slide (2 menit):** Memberikan gambaran utuh sesi 120 menit dalam 1 halaman ringkas — menyatukan 3 Bab teori (`AI/ML/DL`, `4 Tugas CV`, `Bedah Total Neural Network`), Kuis, Kamus & Referensi, serta Hands-On Notebook & Rangkuman Penutup beserta 3 *Learning Goals* di kanan."
            )
            _notes[1] = (
                "• **Naskah Pengajar:** Bacakan singkat ritme 120 menit (~58 menit pembuka, Bab 1–3, kuis & kamus, lalu 62 menit sesi hands-on praktik model 1-layer & rangkuman penutup), lalu tunjuk 3 target penguasaan di kanan."
            )
        elif _orig_idx == 27:
            _notes[-1] = (
                "• **Transisi ke Tahap 5 (Slide 28 — Siklus Belajar Utuh):** \"Tadi kita lihat foto Olaf yang belum dilatih punya **Error 88.7% (Loss 2.18)**. "
                "Nah, bagaimana caranya angka Loss besar ini benar-benar mengubah *Weight* & *Bias* sampai Olaf dikenali 79.2%? Mari lihat **Tahap 5: Siklus Belajar Utuh** di Slide 28!\""
            )
        elif _orig_idx == 42:
            _notes.insert(
                1,
                "• **Pengantar Singkat MLP & Hidden Layer (20–30 detik):** Jelaskan singkat bahwa jaringan standar di Bab 3 yang semua neuronnya disambung penuh (plus 1 lapisan tengah bernama *Hidden Layer*, mis. `Dense(128)`) disebut **MLP (*Multi-Layer Perceptron*)** — dan untuk foto `224×224×3` (`150.528` input), sambungan penuhnya langsung menghasilkan `150.528 × 128 + 128 = 19,27 juta parameter`!",
            )
        elif _orig_idx == 45:
            _notes[0] = _notes[0].replace("Q&A #6", "Q&A #4")
        elif _orig_idx == 46 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (1 menit — Cover Hands-On):** Pembuka sesi praktik langsung **Hands-On: Praktik Neural Network** pada dataset foto Disney Frozen (`143` foto).",
                "• **Catatan Instruktur:** Ajak peserta membuka `materials/P02/p02_teori_neural_network.ipynb` di Google Colab atau Jupyter lokal dan arahkan sekilas ke 6 langkah di strip bawah.",
            ]
        elif _orig_idx == 47 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (9.5 menit — Hands-On Langkah 1):** Mendampingi peserta menjalankan Setup 3 tahap dan membaca `metadata.csv` foto Frozen secara dinamis (`143` foto: polos vs ramai).",
                "• **Panduan Praktik:** Pastikan `SEED = 42` terkunci, `DATA_DIR` mengarah ke `data/frozen_v1`, dan output tabel crosstab cocok dengan panel **Expected Output** kanan.",
            ]
        elif _orig_idx == 48 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (9.5 menit — Hands-On Langkah 2):** Mendampingi peserta melakukan `.flatten()` foto Elsa dan mengerjakan `# TODO 1` (`12.288` neuron) serta `# TODO 2` (`150.528` neuron → `752.645` parameter `W + b`).",
                "• **Panduan Praktik:** Cocokkan angka `752.645` langsung dengan diagram Slide 29 agar teori dan kode terasa 100% menyatu!",
            ]
        elif _orig_idx == 49 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (10 menit — Hands-On Langkah 3):** Mendampingi peserta mengerjakan `# TODO 3` (1 Neuron `W·x + b` + ReLU) dan `# TODO 4` (`softmax_manual`, `Argmax`, & `Loss`) pada 4 piksel nyata Elsa (`ELSA 85.5% | Loss = 0.16`).",
                "• **Tips Mengajar:** Biarkan peserta mencoba mengetik sendiri dulu 2 menit sebelum membuka kotak `<details>` Hint.",
            ]
        elif _orig_idx == 50 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (10 menit — Hands-On Langkah 4):** Mendampingi peserta memuat `143` foto Frozen ukuran `64×64×3` dan mengerjakan `# TODO 5` membangun **Neural Network 1-Layer** (`Input → Flatten → Dense(5, softmax)`).",
                "• **Catatan Penting:** Tegaskan bahwa model 1-layer ini sama persis dengan diagram Slide 29 — dan menjadi fondasi sebelum naik ke arsitektur berlapis & CNN di P03!",
            ]
        elif _orig_idx == 51 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (10 menit — Hands-On Langkah 5):** Mendampingi peserta mengerjakan `# TODO 6` menjalankan `model_nn.fit()` (8 epoch: `Loss 3.39 → 1.44`, `Acc 20.3% → 44.8%`) dan menyimpan `results/p02_nn_loss_curve.png`.",
                "• **Panduan Diskusi:** Amati kurva Loss yang turun stabil, lalu diskusikan dengan jujur mengapa model 1-layer mulai kesulitan pada latar ramai — pembagian split anti-leakage akan dibahas di P05.",
            ]
        elif _orig_idx == 52 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (9 menit — Hands-On Langkah 6):** Mendampingi peserta membaca `model_nn.summary()` (`61.445` parameter), membuktikannya di `# TODO 7` (`12.288 × 5 + 5`), lalu menguji `# TODO 8` (eksperimen opsional 3 nilai *Learning Rate*).",
                "• **Momen Aha:** Pastikan peserta melihat `assert n_weight + n_bias == model_nn.count_params()` lolos 100% dan menyambungkannya dengan angka `752.645` pada resolusi `224×224×3`.",
            ]
        elif _orig_idx == 54 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (2 menit — Kamus Istilah):** Mengulas 12 istilah asli Bab 1–3 yang kini dikelompokkan berdasarkan warna bab (`Bab 1` Biru, `Bab 2` Merah, `Bab 3` Hijau/Kuning).",
                "• **Panduan Interaktif:** Gunakan tombol filter **`Semua` / `Bab 1` / `Bab 2` / `Bab 3`** di pojok kanan atas untuk menyorot kelompok konsep tertentu jika ada pertanyaan dari peserta.",
            ]
        elif _orig_idx == 55 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (5 menit — Kuis Interaktif 5 Soal):** Menguji pemahaman Bab 1–3 secara aktif sebelum masuk praktik notebook.",
                "• **Panduan Interaktif:** Minta peserta mengklik langsung salah satu chip pilihan di setiap kartu soal hingga panel **`Skor: 0 / 5`** bertambah hijau/merah, lalu klik **`Lihat Penjelasan`** atau **`Buka Semua`** untuk membahas alasan setiap jawaban.",
            ]
        elif _orig_idx == 56 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (3 menit — Grand Finale 3 Poin Utama):** Mengunci seluruh sesi **P02 — Teori Neural Network** dalam 3 pilar rapi di slide gelap beserta jembatan menuju **P03 (Arsitektur Neural Network & Konvolusi CNN)**.",
                "• **Naskah Pengajar:** Bacakan 3 pilar: (01) Peta AI/ML/DL & Image Classification; (02) 5 Tahap runtut 1 Piksel → Flatten → Weight+Bias → Softmax → Backprop; (03) Neural Network 1-Layer terbukti di Keras (`61.445` / `752.645` param) sebagai jembatan alami menuju **P03 (Arsitektur & CNN)**. Ingatkan pula Slide 33–34 untuk belajar mandiri.",
            ]
        elif _orig_idx == 57:
            _notes[0] = (
                "**Tujuan Slide (2 menit):** Menutup kelas dengan apresiasi, tugas ringan mandiri opsional, dan preview menarik untuk **P03 (Arsitektur Neural Network & Konvolusi CNN)**."
                if HIDE_BAB4_ARCH
                else _notes[0]
            )
            _notes[-1] = _notes[-1].replace("Slide 58–59", "Slide 33–34" if HIDE_BAB4_ARCH else "Slide 47–48")
        SLIDE_EXPLANATIONS[_new_idx] = _notes
        _new_idx += 1
        if _orig_idx == 27:
            # Sisipkan Slide 28: Siklus Belajar Utuh (menyambung langsung dari Error/Loss Slide 27!)
            SLIDE_EXPLANATIONS[_new_idx] = [
                "**Tujuan Slide (2.5 menit — Tahap 5):** Mengikat seluruh Bab 3 (`Slide 24–27`) menjadi **1 siklus belajar utuh**: `Forward Pass → Hitung Loss → Backpropagation & Gradient Descent → Ulangi tiap Epoch`, memakai angka nyata foto **Olaf** dari model `150.528` piksel Slide 27 (`Loss 2.18 → 0.23`, `P(Olaf) 11.3% → 79.2%`).",
                "• **Panduan Demo Interaktif (`▶ Play` / `■ Stop` / `⏭ +1 Tahap` / `↺ Reset`):** Klik **`▶ Play`** atau jalankan 4 tahap satu per satu: (1) **Forward Pass** = alur maju Tahap 4.1–4.3 (`Epoch 1: P(Olaf)=11.3%`, salah tebak Kristoff); (2) **Hitung Loss** = ukur kesalahan (`Loss=2.18`); (3) **Backpropagation & Gradient Descent** = lacak mundur bobot salah lalu geser sebesar *Learning Rate*; (4) **Epoch** = ulangi ke seluruh foto Frozen hingga kurva *Loss* di bawah turun mulus dari `2.18` ke `0.23` (`Olaf 79.2% ✅`).",
                "• **Transisi ke Ultimate Slide 29 (Simulasi Full Neural Network):** \"Sekarang kelima tahap sudah kita kuasai satu per satu! Mari kita lihat **seluruh 5 tahap bekerja bersama dari ujung ke ujung** dalam 1 simulasi Neural Network nyata dari piksel sampai Backpropagation di Slide 29!\"",
            ]
            _new_idx += 1
            # Sisipkan Slide 29 (Ultimate Bab 3): Simulasi Full Neural Network End-to-End (Tahap 1–5)!
            SLIDE_EXPLANATIONS[_new_idx] = [
                f"**Tujuan Slide ({'4' if HIDE_BAB4_ARCH else '3'} menit — Ultimate Bab 3):** Merangkum **seluruh Bab 3 (Tahap 1 → 5)** dalam **1 simulasi end-to-end Neural Network nyata 1-layer** (`150.528 Input → 5 Output Softmax = 752.645 parameter`, tanpa memperkenalkan konsep *Hidden Layer* dulu!) yang dilatih langsung 8 *epoch* melewati kelima foto figurin Frozen.",
                "• **Panduan Demo Interaktif (`▶ Full 8 Epoch` / `▶ 1 Foto` / `⏭ +1 Tahap` / Slider `Epoch 1–8` / 5 Foto / 5 Kartu Tahap):** Klik **`▶ Full 8 Epoch`** agar peserta menyaksikan proses training utuh melewati **Anna → Elsa → Kristoff → Olaf → Sven secara bergantian** dari **Epoch 1 (`0/5`, Mean Loss `1.70`)** → `E2 (1/5)` → `E3 (3/5)` → `E4 (4/5)` → `E5 (5/5)` → **Epoch 8 (`5/5 Yakin ≥ 74%`, Mean Loss `0.21 ✅`)** lengkap dengan kilatan merah **Backpropagation**, kurva Mean Loss yang turun real-time, dan 5 lencana karakter `A E K O S` yang berubah hijau satu per satu! Lalu gunakan **`▶ 1 Foto`** atau klik kartu tahap bawah bila ingin membedah pelan 1 karakter.",
                (
                    "• **Transisi ke Slide 30 (Cover Kuis, Kamus & Referensi):** \"Lihat bagaimana seluruh 5 tahap dari piksel, `Flatten`, `Weight + Bias`, `Softmax`, hingga `Backpropagation` bekerja bersama melatih 5 karakter Frozen! Mari kita masuk ke sesi evaluasi singkat: **Kuis, Kamus Istilah & Referensi**!\""
                    if HIDE_BAB4_ARCH
                    else "• **Jembatan Emas ke Bab 4 (Slide 30):** Tunjuk jumlah parameter `752.645` (dan melompat ke `19,27 juta` bila ditambah 1 lapisan tengah) sebagai jembatan menuju **Bab 4**!"
                ),
            ]
            _new_idx += 1
            if HIDE_BAB4_ARCH:
                # Sisipkan Slide 30: Cover Kuis, Kamus Istilah & Referensi
                SLIDE_EXPLANATIONS[_new_idx] = [
                    "**Tujuan Slide (0.5 menit — Cover Evaluasi & Sumber Belajar):** Pembatas visual yang rapi setelah Bab 3 sebelum masuk ke **Kuis 5 Soal**, **Kamus Istilah**, dan **Referensi Belajar Mandiri**.",
                    "• **Naskah Pengajar:** \"Tiga bab teori inti sudah tuntas! Sebelum langsung praktik di notebook, mari kita uji cepat pemahaman lewat 5 soal kuis, merangkum 12 istilah kunci, dan melihat tautan belajar mandiri.\"",
                ]
                _new_idx += 1
else:
    SLIDE_EXPLANATIONS = dict(_ALL_SLIDE_EXPLANATIONS)
