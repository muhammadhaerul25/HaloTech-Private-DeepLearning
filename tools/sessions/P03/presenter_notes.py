"""Naskah Penjelasan Detail per Slide (1..52) untuk P03: Arsitektur Neural Network.

Dipakai oleh:
1. `tools/core/exporter.py` -> Speaker Notes PPTX (100% slide)
2. `tools/core/exporter.py` -> `materials/P03/P03_presenter_script.pdf` (A4 1 slide/halaman)
"""

from __future__ import annotations

SLIDE_EXPLANATIONS: dict[int, list[str]] = {
    1: [
        "**Judul & Ruang Lingkup P03:** *Arsitektur Neural Network* — membedah evolusi 5 arsitektur paling relevan untuk proyek klasifikasi karakter Disney Frozen (`120` menit).",
        "**Bento Preview:** Sorot foto nyata `data/frozen_v1/` (*Anna, Elsa, Kristoff, Olaf, Sven*) di sisi kanan sebagai objek uji tetap lintas semua generasi arsitektur.",
        "**Transisi:** Dari P02 kita sudah paham 1 neuron hingga training 1-layer; hari ini kita naik level membandingkan *cetak biru arsitektur*-nya.",
    ],
    2: [
        "**Agenda & 3 Target Belajar:** Jelaskan alur 5 blok waktu (Pemanasan, Bedah Evolusi 5 Arsitektur, Istirahat 5m, Hands-On Keras 6 Langkah, Evaluasi Kuis 5 Soal).",
        "**Target Utama:** Peserta mampu menjelaskan **mengapa** arsitektur berevolusi, membedah ciri khas tiap generasi, dan membuktikan angkanya langsung di notebook.",
    ],
    3: [
        "**Pemanasan — Titik Mentok Model P02:** Tampilkan grafik nyata `01_p02_handoff_limit.png` yang memperlihatkan lonjakan parameter saat foto `224×224×3` hanya diberi Dense layer (`752.645` -> `9,64 juta` param).",
        "**Temuan Geser Piksel:** Jelaskan bar sebelah kanan — saat foto Frozen digeser 8 piksel saja, model `Flatten` stagnan di ~22% sementara `CNN (Conv2D)` mampu bertahan jauh lebih baik (~40%).",
    ],
    4: [
        "**Peta Besar Evolusi 5 Arsitektur:** Gunakan analogi evolusi kamera/desain bangunan: setiap arsitektur baru lahir untuk **menambal cacat fatal** generasi sebelumnya.",
        "**Urutan Sesi:** `1. MLP` → `2. CNN Klasik` → `3. ResNet` → `4. MobileNetV2` → `5. EfficientNet` (+ konteks singkat posisi *Vision Transformer / YOLO* di ujung Bab 4).",
    ],
    5: [
        "**Pembuka Bab 1 — Arsitektur #1: MLP (*Multi-Layer Perceptron*):** Bab ini menjawab apa yang terjadi bila model 1-layer P02 kita beri *Hidden Layer* bertingkat.",
    ],
    6: [
        "**MLP In General:** Jelaskan anatomi lengkap `Input Flatten → Dense(64, ReLU) → Dense(32, ReLU) → Output Softmax(5)`. Ini adalah arsitektur neural network klasik pertama.",
        "**Peran Hidden Layer:** Di P02 output langsung menebak karakter dari piksel mentah; dengan *Hidden Layer*, neuron tengah bisa menggabungkan ciri awal (*warna biru + terang salju*) sebelum memutuskan kelas.",
    ],
    7: [
        "**Fitur Khusus MLP & Keterbatasannya:** Sorot dua sisi: (1) *Hidden Representation* & aktivasi non-linear berantai memungkinkan pola kompleks dipelajari, (2) *Fully-Connected* menyebabkan **Spatial Blindness** dan **Parameter Explosion (`9.636.101` parameter pada `224×224×3`)**.",
        "**Jembatan ke Simulasi:** Mari uji langsung apa yang terjadi ketika foto Elsa digeser sedikit di MLP.",
    ],
    8: [
        "**Simulator #1 — Full Arsitektur MLP & Uji Geser 2 Piksel:** Klik tombol `4 Hidden`, `64 Hidden`, lalu aktifkan `Geser Foto Elsa 2px`.",
        "**Sorotan:** Amati kartu `.sync-card` dan angka total parameter di `224×224×3` (`9,64 juta`), serta bagaimana pergeseran 2 piksel membuat koneksi bobot menabrak piksel tetangga yang salah.",
    ],
    9: [
        "**Use Case MLP & Verdict Proyek Frozen:** Tegaskan bahwa MLP **bukan arsitektur buruk** — ia juara untuk **data tabular** (tabel harga, sensor CSV, nilai ujian) dan dipakai sebagai **head klasifikasi** di ujung CNN.",
        "**Verdict Frozen:** Tidak cocok sebagai pemroses piksel mentah foto `polos`/`ramai`.",
    ],
    10: [
        "**Pembuka Bab 2 — Arsitektur #2: CNN Klasik (*Conv2D + Pooling*):** Sekarang kita mengajarkan komputer melihat pola **kotak 2D** persis seperti kaca pembesar yang menggeser di atas gambar.",
    ],
    11: [
        "**CNN Klasik In General:** Telusuri alur utuh `Foto 2D → Stacked Conv2D + ReLU → MaxPooling2D → Head → Softmax(5)` bersama gambar `02_cnn_conv_pool_elsa.png`.",
        "**Hierarki Fitur:** Layer awal mendeteksi tepi garis, layer tengah menyusun bentuk mahkota/baju, layer dalam mengenali objek karakter Frozen secara utuh.",
    ],
    12: [
        "**Fitur Khusus CNN Klasik:** Bedah 4 mekanisme kunci: (1) **Kernel/Filter `3×3`** & **Parameter Sharing** (1 filter dipakai ulang ke seluruh area gambar!), (2) **Stride**, (3) **Padding** (`valid` vs `same`), dan (4) **MaxPooling `2×2`**.",
        "**Rumus Sederhana:** Tunjukkan contoh cepat `(16 - 3 + 2×0)/1 + 1 = 14` agar peserta paham perubahan ukuran *Feature Map*.",
    ],
    13: [
        "**Simulator #2 — Full Arsitektur CNN Klasik (Data Elsa Nyata):** Ubah jenis Filter (*Sobel Vertikal / Horizontal / Tajamkan*), lalu ubah **Stride (`1` vs `2`)** dan **Padding (`Valid` vs `Same`)**.",
        "**Poin Demo:** Perhatikan kanvas *Feature Map* dan hasil *MaxPool 2×2* berubah langsung menghitung matriks asli `16×16` dari foto Elsa `data/frozen_v1/`, serta lihat betapa hematnya parameter (`101.829` di model 3-blok vs `9,64 juta` di MLP).",
    ],
    14: [
        "**Use Case CNN Klasik & Munculnya Masalah Baru:** Efektif untuk OCR, klasifikasi ikon, dan deteksi cacat industri sederhana.",
        "**Cacat Generasi Ini:** Saat ditumpuk dalam agar tahan latar `ramai` (misal era VGG16 ~138 juta param), sinyal gradien melemah (*Vanishing Gradient*) dan kepala `Flatten → Dense` tetap menyedot puluhan juta bobot.",
    ],
    15: [
        "**Q&A #1 — Cek Pemahaman CNN Klasik:** Minta peserta memilih opsi `A/B/C` untuk menghitung ukuran output `28×28` dengan `Kernel 3×3, Stride 1, Padding Valid`, baru klik *Lihat Jawaban*.",
    ],
    16: [
        "**Pembuka Bab 3 — Arsitektur #3: ResNet (*Residual Network*):** Bagaimana membuat CNN yang sangat dalam (`50+` layer) tetap bisa dilatih tanpa kehilangan informasi tepi awal?",
    ],
    17: [
        "**ResNet In General:** Jelaskan paradoks *Degradation Problem* — menambah layer di CNN biasa justru kadang membuat training error memburuk, lalu kenalkan peta jalan pintas ResNet (`03_resnet_skip_gap.png`).",
        "**Hasil Nyata Frozen:** Pada kompleksitas parameter identik (`24.373`), `Mini-ResNet` menurunkan loss lebih dalam (`0.762`) dan akurasi validasi 2× lipat dibanding `Plain Deep Net`.",
    ],
    18: [
        "**Fitur Khusus ResNet:** Tiga pahlawan utama: (1) **Skip / Shortcut Connection (`F(x) + x`)** sehingga blok cukup belajar *perubahan/residu kecil*, (2) **Batch Normalization** untuk menstabilkan distribusi angka, dan (3) **Global Average Pooling (GAP)** yang memangkas bobot kepala `51,38 juta → 10.245` parameter!",
    ],
    19: [
        "**Simulator #3 — Full ResNet Signal Flow:** Klik toggle antara `Plain Deep Net` dan `ResNet (+ Skip Connection)`, lalu pantau kekuatan sinyal gradien dari Layer 20 mundur ke Layer 1.",
        "**Sorotan GAP:** Klik pula panel perbandingan kepala `Flatten` vs `GAP` agar peserta langsung melihat mengapa ResNet membuang lapisan *Flatten* raksasa.",
    ],
    20: [
        "**Use Case ResNet & Posisi di Proyek Frozen:** Dipakai luas di riset akademis, citra medis (X-Ray/MRI), dan sistem ber-GPU besar (`ResNet50`: `23.597.957` param, `90.02 MB`, `16` blok `Add()`).",
        "**Verdict Frozen:** Sangat bagus sebagai **pembanding akurasi**, namun terlalu berat bila targetnya ringan di Colab gratis dan aplikasi HP.",
    ],
    21: [
        "**Q&A #2 — Skip Connection & GAP:** Uji pemahaman mengapa penjumlahan `F(x) + x` menjaga kelancaran backpropagation dan mengapa *Global Average Pooling* mencegah ledakan bobot di ekor arsitektur.",
    ],
    22: [
        "**Pembuka Bab 4 — Era Efisien (*MobileNetV2 & EfficientNet*):** Bagaimana membawa kecerdasan ResNet ke bodi super ramping yang muat di HP dan cocok untuk dataset kecil seperti Frozen?",
    ],
    23: [
        "**MobileNetV2 In General:** Perkenalkan arsitektur yang memang didesain dari nol untuk perangkat seluler (`2.264.389` parameter total, `~8.64 MB`) — lebih dari **10× lebih kecil** dibanding ResNet50.",
    ],
    24: [
        "**Fitur Khusus MobileNetV2:** Bedah 3 inovasi brilian Sandler dkk.: (1) **Depthwise Separable Convolution** (pisah filter per kanal `3×3` + aduk antar kanal `1×1`, hemat hitungan **`8.4×`** di `04_mobilenetv2_depthwise.png`), (2) **Inverted Residual** (sempit → mengembang `6×` → sempit lagi), dan (3) **Linear Bottleneck** (tidak memakai `ReLU` saat menyempit supaya informasi tidak terpotong).",
    ],
    25: [
        "**Simulator #4 — MobileNetV2 Conv Biasa vs Bottleneck:** Bandingkan langsung operasi `Conv2D 3×3` biasa (`231.2M` perkalian) dengan `Depthwise + Pointwise` (`27.5M` perkalian), serta telusuri langkah `Expand → Depthwise → Project + Skip`.",
    ],
    26: [
        "**Use Case MobileNetV2 & Kandidat Utama Proyek Frozen:** Jelaskan mengapa **MobileNetV2 dipilih sebagai arsitektur inti proyek kita (`P04–P08`)**: hemat RAM Colab, cepat inferensi (`773.5 ms` per 8 foto di CPU, jauh lebih cepat di GPU), minim *overfitting* di `143+` foto, dan punya bobot ImageNet siap Transfer Learning di P04.",
    ],
    27: [
        "**EfficientNet In General:** Setelah MobileNetV2 membuktikan arsitektur ramping itu mungkin, pertanyaan berikutnya muncul: bagaimana menaikkan kapasitas model secara sistematis (`B0 → B1 → B2 → B7`) tanpa tebak-tebakan?",
    ],
    28: [
        "**Fitur Khusus EfficientNet:** Sorot 3 inti: (1) **Compound Scaling (φ)** menaikkan *Depth*, *Width*, dan *Resolution* secara seimbang, (2) blok **MBConv** (keturunan langsung Inverted Residual MobileNetV2!), dan (3) **Squeeze-and-Excitation (SE) Attention** — perlihatkan `05_efficientnet_compound_se.png` di mana gaun biru Elsa menyala fokus di tengah latar `ramai`!",
    ],
    29: [
        "**Simulator #5 — Compound Scaling & SE Channel Attention:** Geser pilihan scaling `B0 / B1 / B2` dan toggle **SE Attention OFF vs ON** pada foto Elsa berlatar ramai.",
        "**Poin Kunci:** Amati bagaimana SE Attention menekan skor kanal latar cangkir/dinding dan mengangkat bobot kanal karakter Elsa.",
    ],
    30: [
        "**Use Case EfficientNet & Perbandingannya dengan MobileNetV2:** Sangat kuat di layanan *cloud* yang mengejar rasio akurasi per FLOPs (`EfficientNetB0: 4.06M param, 15.47 MB, 16 SE blocks`), namun memiliki operasi per-blok lebih banyak (`237` layer, `2238.9 ms` di CPU) sehingga **MobileNetV2** lebih praktis & stabil sebagai baseline utama peserta.",
    ],
    31: [
        "**Matriks Rangkuman 5 Arsitektur (+ Konteks Modern ViT/YOLO):** Tampilkan grafik `06_5arch_comparison_chart.png` hasil benchmark Keras nyata pada mesin ini + kartu kecil menjelaskan di mana posisi **Vision Transformer (ViT)** dan **YOLO** agar wawasan peserta utuh.",
    ],
    32: [
        "**Q&A #3 — Konsultan Keputusan Arsitektur:** Latih peserta memilih arsitektur paling rasional untuk kasus dataset kecil `143` foto `polos vs ramai` dengan keterbatasan komputasi Colab gratis.",
    ],
    33: [
        "**Transisi ke Praktik:** Ringkas apa yang baru saja dibahas di teori ke daftar eksperimen konkret yang sebentar lagi dibuktikan sendiri di `P03_arsitektur_neural_network.ipynb`.",
    ],
    34: [
        "**Istirahat 5 Menit:** Beri jeda sejenak sebelum sesi praktik coding 42 menit. Pastikan browser Google Colab / Jupyter Notebook sudah terbuka.",
    ],
    35: [
        "**Peta Hands-On Visual-First (6 Langkah):** Jelaskan alur kerja notebook: Jalankan Setup 3 tahap & sel `Alat Visualisasi Siap Pakai`, lalu kerjakan 6 langkah ringkas (`# TODO 1` s.d. `# TODO 8`).",
    ],
    36: [
        "**Hands-On Langkah 1 — MLP & Bukti Ledakan Parameter:** Peserta melengkapi `# TODO 1` menyusun MLP Keras `Flatten → Dense(64) → Dense(32) → Dense(5)` dan melihat grafik `9.64M` parameter muncul (`ho_step1_mlp_explosion.png`).",
    ],
    37: [
        "**Hands-On Langkah 2 — Konvolusi 2D & MaxPooling Nyata:** Peserta melengkapi `# TODO 2` menerapkan `Conv2D(1, 3)` / filter Sobel & `MaxPooling2D(2)` pada foto Elsa untuk memunculkan `Feature Map` (`ho_step2_conv_pool_map.png`).",
    ],
    38: [
        "**Hands-On Langkah 3 — Merakit CNN Klasik & Membandingkan vs MLP:** Peserta melengkapi `# TODO 3` merangkai blok `Conv2D + MaxPooling2D + GAP` serta membandingkan akurasi & hematnya parameter (`ho_step3_cnn_vs_mlp.png`).",
    ],
    39: [
        "**Hands-On Langkah 4 — Mini-ResNet Block (`Add()`) & Inspeksi `ResNet50`:** Peserta mengerjakan `# TODO 4` menyambungkan *Skip Connection* `layers.Add()([jalur_conv, shortcut])` dan memeriksa jumlah blok `Add()` pada `ResNet50(weights=None)`.",
    ],
    40: [
        "**Hands-On Langkah 5 — Membedah `MobileNetV2` & `EfficientNetB0`:** Peserta melengkapi `# TODO 5` & `# TODO 6` memuat kedua arsitektur (`weights=None`), lalu menghitung langsung jumlah layer `DepthwiseConv2D` (17 di MobileNetV2) dan `Multiply` SE Attention (16 di EfficientNetB0).",
    ],
    41: [
        "**Hands-On Langkah 6 — Benchmark 5 Arsitektur & Ekspor `results/`:** Peserta melengkapi `# TODO 7` & `# TODO 8` mengumpulkan tabel parameter, estimasi MB, dan waktu inferensi ke `results/p03_5_architectures_benchmark.csv` + grafik kuadran.",
    ],
    42: [
        "**Mini-Challenge (6 Menit):** Berikan 3 skenario industri singkat (HP offline, cloud medis, data harga tiket CSV) dan minta peserta menebak arsitektur terbaik + menulis draf 3 kalimat *'Alasan Memilih MobileNetV2'* untuk laporan proyek.",
    ],
    43: [
        "**Kamus Istilah P03 (18 Istilah Teknis Asli):** Gunakan filter Bab 1–4 atau fitur cari jika peserta lupa arti istilah seperti *Linear Bottleneck*, *Inverted Residual*, atau *Squeeze-and-Excitation*.",
    ],
    44: [
        "**Kuis 1/5 — Kelemahan MLP pada Gambar:** Cek mengapa MLP `Dense` kehilangan struktur ruang 2D & mudah keliru saat posisi objek bergeser.",
    ],
    45: [
        "**Kuis 2/5 — Hitung Dimensi Feature Map CNN:** Cek pemahaman peserta menghitung `(10 - 3 + 0) / 1 + 1 = 8×8`, lalu dibagi dua oleh `MaxPooling 2×2` menjadi `4×4` tanpa menebak.",
    ],
    46: [
        "**Kuis 3/5 — Fungsi Skip Connection pada ResNet:** Pastikan peserta paham jalur pintas `+x` mengedarkan sinyal gradien agar jaringan dalam tidak mengalami degradasi.",
    ],
    47: [
        "**Kuis 4/5 — Rahasia Hemat Komputasi MobileNetV2:** Uji pemahaman kombinasi *Depthwise (`3×3` per channel)* + *Pointwise (`1×1` pengaduk)*.",
    ],
    48: [
        "**Kuis 5/5 — Compound Scaling & SE Attention pada EfficientNet:** Uji pemahaman keseimbangan Depth × Width × Resolution serta peran perhatian kanal (*SE*) meredam latar `ramai`.",
    ],
    49: [
        "**Rangkuman 3 Poin Utama:** Tegaskan tiga pilar P03: (1) Arsitektur berevolusi dari cacat nyata, (2) Setiap generasi punya senjata khas, dan (3) Bukti angka di notebook menempatkan **MobileNetV2** sebagai kandidat terbaik proyek Frozen.",
    ],
    50: [
        "**Closing & Jembatan ke P04:** Apresiasi peserta karena sudah memahami peta arsitektur dari MLP hingga EfficientNet. Di **P04 — Arsitektur CNN & Transfer Learning**, kita akan mengaktifkan bobot *pretrained ImageNet* pada MobileNetV2!",
    ],
    51: [
        "**Referensi Bagian 1 (0 Menit):** Tautan bacaan & video visual untuk MLP, CNN Klasik (*CNN Explainer*, CS231n, *Convolution Arithmetic*), dan ResNet (`arXiv 1512.03385`).",
    ],
    52: [
        "**Referensi Bagian 2 (0 Menit):** Tautan paper MobileNetV2 (`arXiv 1801.04381`), panduan Transfer Learning Keras/TensorFlow, serta peta bacaan mandiri.",
    ],
}
