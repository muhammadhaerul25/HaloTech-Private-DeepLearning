"""Naskah Penjelasan Detail per Slide untuk P02: Computer Vision 101 (Slide 1 s.d. 58).

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
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 2: 4 Task Utama Computer Vision**.",
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
        "**Tujuan Slide (1.5 menit):** Memulai Bab 3 dari unit paling konkret — **1 Neuron** sebagai wadah pemegang **1 nilai angka**, khususnya 1 angka piksel (`0.76`) dari foto Elsa.",
        "• **Naskah Pengajar:** Arahkan mata ke kanan: 1 kotak piksel foto Elsa (`0.76`) masuk ke 1 lingkaran biru (**1 Neuron**). Jelaskan akurat: di lapisan paling depan neuron hanya memegang angka piksel; nanti di lapisan berikutnya barulah neuron menghitung angkanya sendiri. Singgung singkat ilustrasi sel saraf otak kiri sebagai asal-usul nama *Neuron*.",
    ],
    21: [
        "**Tujuan Slide (1.5 menit):** Memperlihatkan **animasi langsung proses `Flatten`** — tiap piksel foto Elsa (`3×3` = 9 piksel nyata) dipindai dari **kiri ke kanan, atas ke bawah**, lalu terbang dan ditumpuk vertikal menjadi **1 kolom `Input Layer`**.",
        "• **Panduan Demo Animasi Interaktif:** Klik **`▶ Putar Animasi`** (atau klik **`⏭ +1 Piksel`** satu per satu sambil menjelaskan) agar peserta melihat Baris 1 biru (`x₁..x₃`) → Baris 2 merah (`x₄..x₆`) → Baris 3 hijau (`x₇..x₉`) mendarat berurutan dari atas ke bawah menjadi **Input Layer**.",
    ],
    22: [
        "**Tujuan Slide (2 menit):** Memperluas konsep `Input Layer` dari contoh mini `2×2` hitam-putih ke **foto berwarna (RGB)** — setiap 1 titik piksel warna punya 3 nilai (`R, G, B`) sehingga butuh 3 neuron input (`Tinggi × Lebar × Channel`).",
        "• **Panduan Demo Simulator #3:** Tunjuk pemetaan 1 foto RGB → `x₁, x₂, x₃, ...` bertumpuk ke bawah, lalu klik `MNIST 28×28×1` (`784`), `Frozen 64×64×3` (`12.288`), dan `Frozen 224×224×3` (`150.528` neuron!).",
    ],
    23: [
        "**Tujuan Slide (1 menit):** Menampilkan wujud **skala nyata** proses *Flatten* pada foto asli Elsa `224×224×3` (`03_flatten_frozen_visual.png`).",
        "• **Naskah Pengajar:** Tunjukkan foto 2D Elsa diiris baris demi baris lalu ditumpuk vertikal menjadi strip `x₁` sampai `x₁₅₀₅₂₈`, serta bandingkan panjang kolom Input Layer antara `784`, `12.288`, dan `150.528` neuron.",
    ],
    24: [
        "**Tujuan Slide (1 menit):** Menjelaskan **Output Layer** yang jumlah neuronnya sama dengan jumlah kelas (5 kelas Frozen).",
        "• **Naskah Pengajar:** Tekankan catatan akurasi di kartu kanan: aturan `output = jumlah kelas` ini khusus untuk **Image Classification** (sesuai Bab 2, untuk *detection/segmentation* outputnya berbeda).",
    ],
    25: [
        "**Tujuan Slide (2 menit):** Mendemonstrasikan fungsi **Softmax** mengubah 5 skor mentah (*logits*) menjadi probabilitas 0–100% lewat Simulator #4.",
        "• **Panduan Demo Simulator #4:** Klik `1. Yakin Elsa`, `2. Ragu Elsa vs Anna`, lalu `3. Semua Skor Negatif` (tunjukkan kolom `eᶻ` yang mengubah semua nilai menjadi positif sehingga total selalu tepat `100.0%`).",
    ],
    26: [
        "**Tujuan Slide (1.5 menit):** Membedah koneksi *Fully Connected / Dense* — menelusuri tepat **1 neuron input** ke seluruh **5 neuron output** lewat Simulator #5.",
        "• **Panduan Demo Simulator #5:** Klik tombol `x₁`, `x₂`, `x₃`, `x₄` bergantian. Tekankan satu hal: 1 neuron input saja sudah punya **5 garis weight** (`w₁,₁` sampai `w₁,₅`).",
    ],
    27: [
        "**Tujuan Slide (1 menit):** Menghitung jumlah weight & bias **tanpa hidden layer** untuk foto `224×224×3` ke 5 kelas.",
        "• **Naskah Pengajar:** Tunjukkan hitungan persis: `150.528 × 5 = 752.640` weight + `5` bias = `752.645` parameter. Lalu jelaskan mengapa 1 lapisan lurus saja belum mampu memahami bentuk kompleks.",
    ],
    28: [
        "**Tujuan Slide (1 menit):** Menjelaskan mengapa kita menambahkan **Hidden Layer** di antara Input dan Output.",
        "• **Naskah Pengajar:** Telusuri 4 kartu dari kiri ke kanan: piksel mentah → tepi & warna dasar → bagian bentuk objek → keputusan 5 karakter. Sampaikan bahwa tumpukan banyak *Hidden Layer* inilah asal kata **Deep Learning**.",
    ],
    29: [
        "**Tujuan Slide (1 menit):** Menampilkan diagram utuh **Multi-Layer Perceptron (MLP)**: `Input Layer → Hidden Layer (+ ReLU) → Output Layer (+ Softmax)`.",
        "• **Naskah Pengajar:** Tunjukkan simbol `W₁, b₁` dan `W₂, b₂`. Aliran perhitungan maju dari kiri ke kanan disebut **Forward Pass**.",
    ],
    30: [
        "**Tujuan Slide (1.5 menit):** Momen \"Aha!\" — menghitung lonjakan parameter ketika menambahkan **Hidden Layer** lewat Simulator #6.",
        "• **Panduan Demo Simulator #6:** Tunjukkan posisi standar `224×224×3` dengan `128` neuron hidden = **`19.268.357` parameter** (`19,27` juta!). Bandingkan dengan tombol `64×64×3` (`1,57` juta). Tunjukkan bahwa 99,99% parameter menumpuk di Layer 1.",
    ],
    31: [
        "**Tujuan Slide (2.5 menit):** Menunjukkan **Forward Pass** langkah demi langkah memakai **4 piksel nyata** dari foto Elsa (`x = [0.76, 0.74, 0.65, 0.65]`) lewat Simulator #7.",
        "• **Panduan Demo Simulator #7:** Klik tombol 1 → 2 → 3 → 4 perlahan. Tunjukkan bahwa tidak ada sihir: hanya perkalian, penjumlahan bias, ReLU, dan Softmax hingga keluar probabilitas `87.47%` Elsa.",
    ],
    32: [
        "**Tujuan Slide (1 menit):** Q&A #4 mengecek kemampuan peserta menghitung parameter 1 layer secara manual.",
        "• **Aktivitas Kelas:** Minta peserta menghitung `4 input → 2 hidden` dengan rumus `(4 × 2) + 2 = 10` (Kunci: **C**). Ingatkan untuk tidak melupakan angka bias.",
    ],
    33: [
        "**Tujuan Slide (1.5 menit):** Masuk ke bagian intuitif *bagaimana network belajar*: memperkenalkan **Loss Function** (Cross-Entropy).",
        "• **Naskah Pengajar:** Tunjuk panel kiri grafik (`05_loss_gradient_descent_overview.png`): jika foto Elsa diberi probabilitas rendah (`10%`), hukumannya besar (`Loss = 2.30`); jika diberi `90%`, `Loss = 0.11`. Makin kecil Loss = makin bagus!",
    ],
    34: [
        "**Tujuan Slide (2 menit):** Menjelaskan **Gradient Descent** sebagai \"turun bukit mencari error terkecil\" serta efek **Learning Rate** lewat Simulator #8.",
        "• **Panduan Demo Simulator #8:** Klik `LR Kecil` (lambat), `LR Ideal` (mulus ke dasar `Loss = 0.002`), lalu `LR Besar` (memantul liar/divergen). Tanpa rumus turunan berat, cukup intuisi arah turun dan lebar langkah.",
    ],
    35: [
        "**Tujuan Slide (1.5 menit):** Mengenalkan **Backpropagation** sekilas secara intuitif.",
        "• **Naskah Pengajar:** Tunjuk panah biru (maju: *Forward Pass*) dan panah merah putus-putus (mundur: *Backpropagation*) serta 3 kartu langkah di bawahnya. Tenangkan peserta: seluruh perhitungan arah koreksi dikerjakan otomatis oleh Keras saat `model.fit()` dipanggil.",
    ],
    36: [
        "**Tujuan Slide (1 menit):** Merangkum satu siklus penuh training (**Tebak → Ukur Loss → Koreksi → Ulangi**) dan arti **Epoch**.",
        "• **Naskah Pengajar:** Jelaskan 1 *Epoch* = 1 putaran penuh membaca seluruh data latih. Beri preview bahwa detail diagnosis kurva *Train vs Val Loss* & *Overfitting* akan diperdalam di P03.",
    ],
    37: [
        "**Tujuan Slide (1 menit):** Mengunci seluruh Bab 3 lewat tangga hierarki dari unit terkecil (**1 Neuron**) hingga sistem belajar (**Training Loop**).",
        "• **Naskah Pengajar:** Baca cepat nomor 1 sampai 5 dan tanyakan apakah ada satu tangga yang masih terasa mengganjal sebelum pindah ke Bab 4.",
    ],
    38: [
        "**Tujuan Slide (1 menit):** Q&A #5 menutup Bab 3 — memastikan peserta paham arah baca nilai Loss yang menurun.",
        "• **Aktivitas Kelas:** Kunci: **B** (Loss turun dari `1.65` ke `0.35` berarti bobot berhasil diperbaiki oleh Gradient Descent sehingga kesalahan mengecil).",
    ],
    39: [
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 4: Peta Arsitektur Neural Network untuk Computer Vision (Teaser)**.",
        "• **Naskah Pengajar:** \"Di Bab 4 yang singkat ini, kita sambungkan temuan 19,27 juta parameter tadi ke peta arsitektur CV modern — cukup secara konseptual dulu sebagai jembatan ke P03 dan P04.\"",
    ],
    40: [
        "**Tujuan Slide (1.5 menit):** Menunjukkan 2 kelemahan utama **MLP** pada foto (`06_mlp_vs_cnn_preview.png`): boros parameter dan peka pergeseran objek akibat *Flatten*.",
        "• **Naskah Pengajar:** Bandingkan kiri (MLP mengiris foto 1D) vs kanan (CNN menggeser filter kecil `3×3` di foto 2D utuh — jauh lebih hemat bobot & tahan geser).",
    ],
    41: [
        "**Tujuan Slide (2 menit):** Menelusuri peta evolusi arsitektur CV (`MLP → CNN → ResNet → MobileNetV2`) lewat Simulator #9.",
        "• **Panduan Demo Simulator #9:** Klik keempat tombol secara berurutan. Tekankan bahwa di P02 cukup kenal ide besar dan alasannya; detail konvolusi dibedah di P03 dan *Transfer Learning* di P04.",
    ],
    42: [
        "**Tujuan Slide (1 menit):** Menghubungkan 4 Task CV (Bab 2) dengan contoh keluarga arsitektur populernya dan menjelaskan alasan pemilihan **MobileNetV2** untuk proyek Frozen.",
        "• **Naskah Pengajar:** Tunjuk 3 kartu (Classification: ResNet/MobileNetV2; Detection: YOLO/Faster R-CNN; Segmentation: U-Net/Mask R-CNN) lalu bacakan 3 alasan memilih MobileNetV2.",
    ],
    43: [
        "**Tujuan Slide (1 menit):** Q&A #6 menutup sesi teori — mengunci alasan pindah dari MLP ke CNN.",
        "• **Aktivitas Kelas:** Kunci: **B** (MLP merusak struktur 2D lewat Flatten dan meledakkan parameter hingga jutaan).",
    ],
    44: [
        "**Tujuan Slide (5 menit):** Jeda istirahat wajib 5 menit sebelum masuk ke sesi praktik **Hands-On Notebook**.",
        "• **Catatan Instruktur:** Ajak peserta minum air & istirahatkan mata. Pastikan file `materials/P02/P02_computer_vision_101.ipynb` dan folder `data/frozen_v1/` siap dibuka.",
    ],
    45: [
        "**Tujuan Slide (7 menit — Hands-On Langkah 1):** Mendampingi peserta menjalankan Setup 3 tahap dan membaca `metadata.csv` foto Frozen secara dinamis.",
        "• **Panduan Praktik:** Pastikan `SEED = 42` terkunci, `DATA_DIR` mengarah ke `data/frozen_v1`, dan 5 foto karakter Frozen tampil dengan benar.",
    ],
    46: [
        "**Tujuan Slide (7 menit — Hands-On Langkah 2):** Mendampingi peserta melakukan `.flatten()` foto Elsa dan mengerjakan `# TODO 1` serta `# TODO 2`.",
        "• **Panduan Praktik:** Minta peserta membuktikan sendiri panjang vektor `64×64×3 = 12.288` dan `224×224×3 = 150.528` sesuai Slide 22–23.",
    ],
    47: [
        "**Tujuan Slide (7 menit — Hands-On Langkah 3):** Mendampingi peserta mengerjakan `# TODO 3` (1 Neuron + ReLU) dan `# TODO 4` (Softmax manual) serta memverifikasi Forward Pass 4 piksel nyata Elsa di NumPy.",
        "• **Tips Mengajar:** Biarkan peserta mencoba mengetik sendiri dulu sebelum membuka kotak `<details>` Hint.",
    ],
    48: [
        "**Tujuan Slide (7 menit — Hands-On Langkah 4):** Mendampingi peserta memuat foto Frozen ukuran `64×64×3` dan mengerjakan `# TODO 5` membangun MLP kecil di Keras.",
        "• **Catatan Penting:** Tegaskan kembali bahwa MLP ini hanya demo konsep untuk memahami layer dan parameter, bukan model akhir proyek.",
    ],
    49: [
        "**Tujuan Slide (7 menit — Hands-On Langkah 5):** Mendampingi peserta mengerjakan `# TODO 6` melatih MLP singkat dan memplot kurva *Training Loss*.",
        "• **Panduan Diskusi:** Amati apakah kurva Loss turun tiap epoch, dan ingatkan bahwa pembagian data resmi anti-leakage (Group Split) akan dipelajari di P05.",
    ],
    50: [
        "**Tujuan Slide (7 menit — Hands-On Langkah 6):** Mendampingi peserta membaca `mlp.summary()` dan mengerjakan `# TODO 7` mencocokkan hitungan tangan parameter dengan `mlp.count_params()`.",
        "• **Momen Aha:** Pastikan peserta merasakan kepuasan saat `assert hitung_manual == mlp.count_params()` lolos 100%!",
    ],
    51: [
        "**Tujuan Slide (5 menit — Mini-Challenge):** Meminta peserta menebak dampak mengubah jumlah neuron hidden (`32` vs `64` vs `128`) sebelum menjalankan `# TODO 8` di notebook.",
        "• **Poin Diskusi:** Parameter naik proporsional `2×` saat hidden naik `2×`, namun lebih banyak parameter pada dataset kecil juga memperbesar risiko menghafal data latih (*overfitting*).",
    ],
    52: [
        "**Tujuan Slide (2 menit):** Mengulas singkat 12 istilah asli Computer Vision 101 di Kamus Istilah.",
        "• **Interaksi:** Tanyakan ke peserta apakah ada 1–2 istilah yang masih ingin diperjelas ulang sebelum kuis.",
    ],
    53: [
        "**Tujuan Slide (4 menit):** Kuis interaktif 5 soal mencakup Bab 1 sampai Bab 4.",
        "• **Aktivitas Kelas:** Minta peserta menjawab kelima soal secara lisan dulu, lalu klik tombol `Lihat Jawaban` satu per satu untuk konfirmasi bersama.",
    ],
    54: [
        "**Tujuan Slide (2 menit):** Mengunci sesi hari ini dengan 3 Poin Utama di slide gelap.",
        "• **Naskah Pengajar:** Bacakan 3 pilar: (01) Peta AI/ML/DL & Image Classification; (02) Struktur Neuron → Layer → Forward Pass → Training; (03) Batasan MLP menjadi jembatan kuat menuju CNN di P03.",
    ],
    55: [
        "**Tujuan Slide (2 menit):** Menutup kelas dengan apresiasi, tugas ringan mandiri opsional, dan preview menarik untuk **P03 (Training Neural Network & Konvolusi CNN)**.",
        "• **Catatan Referensi:** Arahkan peserta ke Slide 56–57 untuk tautan video 3Blue1Brown & sumber resmi belajar mandiri.",
    ],
    56: [
        "**Tujuan Slide (0 menit — Referensi Mandiri 1/2):** 6 tautan rujukan utama Neural Network & ML dasar sesuai `docs/PLAN.md` (sumber belum diverifikasi ulang diberi label `[CEK LINK]`).",
        "• **Catatan Penggunaan:** Tidak perlu dibahas panjang di kelas; rekomendasikan video 3Blue1Brown #1 sebagai tontonan opsional terbaik di rumah.",
    ],
    57: [
        "**Tujuan Slide (0 menit — Referensi Mandiri 2/2):** 6 tautan rujukan Computer Vision, CNN Explainer, ResNet, dan MobileNetV2 sesuai `docs/PLAN.md` sebagai jembatan menuju P03 dan P04.",
    ],
}
