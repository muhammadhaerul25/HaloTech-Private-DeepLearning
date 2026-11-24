"""Naskah Penjelasan Detail per Slide untuk P02: Computer Vision 101 (Slide 1 s.d. 59).

Standar penulisan:
- Memakai istilah asli Deep Learning & Computer Vision (AI, ML, DL, Image Classification,
  Object Detection, Instance Segmentation, Object Tracking, Neuron, Input/Hidden/Output Layer,
  Weight, Bias, ReLU, Softmax, Forward Pass, Loss, Gradient Descent, Backpropagation, Epoch,
  MLP, CNN, ResNet, MobileNetV2) dengan penjelasan bahasa Indonesia sehari-hari.
- Dipakai oleh `tools/core/exporter.py` untuk Speaker Notes PPTX (100% slide) dan
  `materials/P02/P02_presenter_script.pdf` (A4 Portrait, 1 slide = 1 halaman).
"""

from __future__ import annotations

SLIDE_EXPLANATIONS: dict[int, list[str]] = {
    1: [
        "**Tujuan Slide (1 menit):** Menyambut peserta di **P02 — Computer Vision 101** berdurasi 120 menit dan membangun rasa percaya diri bahwa topik besar dari AI sampai Neural Network akan dibedah perlahan.",
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
        "• **Panduan Demo Interaktif:** Klik **`▶ Putar`** agar peserta melihat foto Elsa di-*zoom* menjadi grid `8×8`, 1 kotak piksel biru gaun Elsa (`Baris 5, Kol 3 · 0.42`) terangkat menjadi kartu nilai piksel lalu berubah bentuk (*morph*) menjadi lingkaran biru **1 Neuron**. Klik **`⏭ Piksel Lain`** atau klik langsung kotak mana saja di grid `8×8` (rambut, dinding, tangan) untuk menunjukkan setiap piksel punya nilai & neuronnya sendiri.",
    ],
    21: [
        "**Tujuan Slide (1.5 menit):** Memperlihatkan **animasi langsung proses `Flatten`** — tiap piksel foto Elsa (`4×4` = 16 piksel nyata) dipindai dari **kiri ke kanan, atas ke bawah**, lalu terbang dan ditumpuk vertikal menjadi **1 kolom `Input Layer`**.",
        "• **Panduan Demo Animasi Interaktif:** Klik **`▶ Putar Animasi`** (atau klik **`⏭ +1 Piksel`** satu per satu sambil menjelaskan) agar peserta melihat Baris 1 biru (`x₁..x₄`) → Baris 2 merah (`x₅..x₈`) → Baris 3 kuning (`x₉..x₁₂`) → Baris 4 hijau (`x₁₃..x₁₆`) mendarat berurutan dari atas ke bawah menjadi **Input Layer**.",
    ],
    22: [
        "**Tujuan Slide (2 menit):** Memperlihatkan secara besar, detail, & **beranimasi per-piksel** transformasi 3 tahap foto menuju **Input Layer**: (1) Foto Original Elsa (`H`, `W`, `C`); (2) Hasil *Flatten* 1D dengan kurung kurawal `}` perkalian `H × W × C = Total Neuron`; dan (3) Kolom **Input Layer** berisi lingkaran neuron angka nyata `0.0–1.0`.",
        "• **Panduan Demo Interaktif Per-Piksel:** Klik **`▶ Putar`** (atau **`⏭ +1 Piksel`** / klik langsung kotak piksel mana saja pada **Foto Elsa**) agar peserta melihat kotak piksel nyata terbang ke Pita 1D lalu pecah di udara menjadi 3 bola `R, G, B` yang mendarat ke lingkaran `x₁, x₂, x₃`! Klik lingkaran neuron mana saja di kanan untuk menampilkan garis jejak balik ke asalnya, lalu bandingkan `64×64×1 (Gray)` vs `64×64×3 (RGB)` vs `224×224×3 (RGB)`.",
    ],
    23: [
        "**Tujuan Slide (2 menit):** Menyambungkan **Input Layer** langsung ke **Output Layer** dalam 4 tahap bernomor yang sinkron antara ilustrasi atas dan 4 kartu penjelasan di bawahnya: `1. Foto Original` → `2. Input Layer` → `3. Output Layer` → `4. Hasil Klasifikasi`.",
        "• **Panduan Demo Interaktif (`▶ Putar Semua` / `⏭ +1 Langkah`):** Jalankan animasi agar peserta melihat alur penuh dari piksel ke neuron (`x₁..x₆` hingga `x150.528`), lalu kalkulasi probabilitas kelas lewat koneksi neuron demi neuron ke seluruh 5 output (`y₁..y₅`), hingga bola `89%` meluncur ke hasil klasifikasi `ELSA`. Klik langsung piksel foto, salah satu neuron Input, atau salah satu kelas Output untuk menyorot koneksinya!",
        "• **Aturan Kunci yang Akurat secara Ilmiah:** Tekankan kotak catatan bawah: (1) **Ukuran piksel × channel gambar (`H × W × C`)** menentukan jumlah neuron di **Input Layer** pada MLP (grayscale `C=1` → tepat `H×W`; RGB `C=3` → `3×` lebih banyak karena tiap piksel punya 3 nilai R, G, B); (2) **Jumlah kelas gambar** menentukan jumlah neuron di **Output Layer** untuk klasifikasi multi-kelas (5 kelas Frozen → 5 neuron + Softmax; pengecualian: untuk klasifikasi biner 2 kelas sering cukup 1 neuron Sigmoid, dan untuk task seperti *Regression* atau *Detection* jumlah output mengikuti target tugasnya).",
        "• **Transisi ke Slide 24:** \"Pertanyaannya sekarang: bagaimana jaringan bisa tahu secara matematis bahwa input ini gambar Elsa? Mari kita lihat simulasi training langsung di slide berikutnya!\"",
    ],
    24: [
        "**Tujuan Slide (2 menit):** Menjawab secara konkret & matematis bagaimana Neural Network bisa tahu foto ini adalah **Elsa** (atau karakter lain) lewat **Simulasi Training lambat (*slow-motion*)** pada 5 foto nyata Frozen berlabel (`Anna, Elsa, Kristoff, Olaf, Sven`), dengan menyorot 2 tahap hitungan: **A. Weight + Bias (`z = Σ(x·w) + b`)** dan **B. Activation Function (`Softmax`)**.",
        "• **Panduan Demo Interaktif:** Jelaskan bahwa `Input Layer` di sini adalah **versi mini 6 fitur piksel murni** (`Merah R, Hijau G, Biru B, Piksel Atas, Piksel Bawah, Kontras` — aslinya `150.528` piksel, selalu lebih banyak dari 5 neuron *Output Layer*!) ditambah node **`+1 · Bias`** di bawahnya. Klik **`Sebelum Training (Acak)`** dulu agar peserta melihat bobot acak menghasilkan tebakan salah (~`19%`). Lalu klik **`▶ Simulasi Training`** (atau klik **`⏭ +1 Tahap Hitung`** pada foto mana saja) agar peserta bisa mengecek setiap angka dengan kalkulator: (1) Input `x₁..x₆` masuk → (2) Kotak kuning **Weight + Bias** menyala (hijau = mendukung, merah = menekan) menghitung `z = Σ(x·w) + b` → (3) Kotak hijau **Activation Function (`Softmax`)** menghitung `e^z / Σe^z` secara eksak → (4) Bandingkan **Target 100% vs Prediksi → Error** sehingga *Weight* & *Bias* diperbarui hingga 5/5 kelas tepat (`Elsa 76.1%`)!",
        "• **Transisi ke Slide 25:** \"Di kotak kuning dan kotak hijau tadi ada dua mesin inti yang bekerja: **Weight + Bias** dan **Activation Function**. Mari kita bedah masing-masing secara khusus di dua slide berikutnya!\"",
    ],
    25: [
        "**Tujuan Slide (2 menit):** Membedah khusus **Weight (`w`) & Bias (`b`)** secara runtut: Apa itu, Kenapa keduanya wajib ada, Bagaimana cara kerjanya (`z = Σ(x·w) + b`), serta simulasi langsung pada **5 foto nyata Frozen**.",
        "• **Panduan Demo Interaktif (`1. Bobot Ideal Elsa` → `2. Tanpa Bias` → `3. Weight Biru Dibalik`):** Tunjukkan dulu `Bobot Ideal Elsa` (`w₃ Biru = +12.7` mengangkat Elsa `+2.39`, sementara `Bias = -2.8` menekan kelas lain). Lalu klik **`2. Tanpa Bias (b = 0)`** agar peserta melihat semua 5 karakter ikut jadi positif (`z > 0`) karena garis ambang hilang! Terakhir klik **`3. Weight Biru Dibalik`** atau geser slider manual untuk menunjukkan *weight* menentukan ciri warna apa yang dicari neuron.",
        "• **Transisi ke Slide 26:** \"Skor mentah `z` sudah terbentuk oleh Weight & Bias, tapi nilainya masih bebas dari minus sampai plus. Bagaimana mengubahnya jadi sinyal aktivasi & peluang? Itulah tugas **Activation Function** di Slide 26!\"",
    ],
    26: [
        "**Tujuan Slide (2 menit):** Membedah khusus **Activation Function** secara runtut: Apa itu, Kenapa wajib ada (*Non-Linearity* agar 100 layer tidak runtuh menjadi 1 garis lurus + menstandarkan rentang output), Cara kerja 3 fungsi utama (`ReLU`, `Sigmoid`, `Softmax`), dan simulasi langsung pada **5 foto nyata Frozen**.",
        "• **Panduan Demo Interaktif (`1. ReLU` → `2. Sigmoid` → `3. Softmax`):** Di tab **`ReLU`**, tunjukkan kurva patah di `z=0` dan klik foto Elsa (`z=+2.39 → Aktif`) vs Anna (`z=-0.40 → 0.00 Mati`) atau geser slider `z`. Pindah ke **`Sigmoid`** untuk melihat kurva-S `0–100%` (cocok untuk 2 kelas: *Elsa vs Bukan Elsa*), lalu pindah ke **`Softmax`** untuk melihat 5 skor sekaligus diubah menjadi total tepat `100.0%`!",
        "• **Transisi ke Slide 27:** \"Mari kita eksplorasi lebih bebas cara kerja **Softmax** dengan menggeser ke-5 skor mentah (*logits*) di slide berikutnya!\"",
    ],
    27: [
        "**Tujuan Slide (1.5 menit):** Mendemonstrasikan fungsi **Softmax** mengubah 5 skor mentah (*logits*) menjadi probabilitas 0–100% lewat Simulator Softmax.",
        "• **Panduan Demo Simulator:** Klik `1. Yakin Elsa`, `2. Ragu Elsa vs Anna`, lalu `3. Semua Skor Negatif` (tunjukkan kolom `eᶻ` yang mengubah semua nilai menjadi positif sehingga total selalu tepat `100.0%`).",
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
        "• **Catatan Instruktur:** Ajak peserta minum air & istirahatkan mata. Pastikan file `materials/P02/P02_computer_vision_101.ipynb` dan folder `data/frozen_v1/` siap dibuka.",
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
        "**Tujuan Slide (2 menit):** Mengulas singkat 12 istilah asli Computer Vision 101 di Kamus Istilah.",
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
