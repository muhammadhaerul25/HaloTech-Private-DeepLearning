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

import json
from pathlib import Path

_P02_DATA_PATH = Path(__file__).resolve().parents[3] / "materials" / "P02" / "assets" / "P02" / "p02_data.json"
_DRESS_GRAY = "0.42"
_HO_B_VAL = "0.60"
_HO_EPOCHS = 30
_HO_TOTAL = 143
_HO_STEPS = 9
_HO_S0 = 2
_HO_SEND = 5
_HO_E0_LOSS = "1.71"
_HO_E1_LOSS = "3.03"
_HO_END_LOSS = "0.89"
_HO_END_ACC = "76.9"
_HO_POLOS_ACC = "77.5"
_HO_RAMAI_ACC = "95.1"
if _P02_DATA_PATH.exists():
    try:
        _d = json.loads(_P02_DATA_PATH.read_text(encoding="utf-8"))
        _ends = _d.get("elsa_rgb_ends", {})
        _g = _ends.get("grid", [])
        _di = int(_ends.get("dress_idx", 34))
        if 0 <= _di < len(_g):
            _DRESS_GRAY = f"{float(_g[_di]['gray']):.2f}"
        _HO_TOTAL = int(_d.get("total_images", 143))
        _HO_STEPS = (_HO_TOTAL + 15) // 16
        _hm = _d.get("handson_metrics", {})
        if _hm:
            _rgb = _hm.get("elsa_px_rgb", [0.52, 0.53, 0.60])
            _HO_B_VAL = f"{float(_rgb[2]):.2f}"
            _HO_EPOCHS = int(_hm.get("epochs", 30))
            _HO_S0 = int(_hm.get("sample_e0_correct", 2))
            _HO_SEND = int(_hm.get("sample_end_correct", 5))
            _HO_E0_LOSS = f"{float(_hm.get('epoch0_loss', 1.71)):.2f}"
            _HO_E1_LOSS = f"{float(_hm.get('epoch1_loss', 3.03)):.2f}"
            _HO_END_LOSS = f"{float(_hm.get('epoch_end_loss', 0.89)):.2f}"
            _HO_END_ACC = f"{float(_hm.get('epoch_end_acc_pct', 76.9)):.1f}"
            _HO_POLOS_ACC = f"{float(_hm.get('all_polos_acc_pct', 77.5)):.1f}"
            _HO_RAMAI_ACC = f"{float(_hm.get('all_ramai_acc_pct', 95.1)):.1f}"
    except Exception:
        pass

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
        f"**Tujuan Slide (1.5 menit):** Memulai Bab 3 dari unit paling konkret — **1 Neuron** sebagai wadah pemegang **1 nilai angka**, khususnya 1 angka piksel biru gaun Elsa (`{_DRESS_GRAY}`).",
        f"• **Panduan Demo Interaktif:** Klik **`▶ Play`** agar peserta melihat foto Elsa di-*zoom* menjadi grid `8×8`, 1 kotak piksel biru gaun Elsa (`Baris 5, Kol 3 · {_DRESS_GRAY}`) terangkat menjadi kartu nilai piksel lalu berubah bentuk (*morph*) menjadi lingkaran biru **1 Neuron**. Klik **`⏭ Piksel Lain`** atau klik langsung kotak mana saja di grid `8×8` (rambut, dinding, tangan) untuk menunjukkan setiap piksel punya nilai & neuronnya sendiri.",
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
        "**Tujuan Slide (1.5 menit):** Menyambungkan **Input Layer** langsung ke **Output Layer** dalam 4 tahap bernomor yang sinkron antara ilustrasi atas dan 4 kartu penjelasan di bawahnya: `1. Foto Original` → `2. Input Layer` → `3. Output Layer` → `4. Hasil Klasifikasi`.",
        "• **Panduan Demo Interaktif (`▶ Play` / `⏭ +1 Langkah`):** Jalankan animasi agar peserta melihat alur penuh dari piksel ke neuron (`x₁..x₆` hingga `x150.528`), lalu kalkulasi probabilitas kelas lewat koneksi neuron demi neuron ke seluruh 5 output (`y₁..y₅`), hingga bola `89%` meluncur ke hasil klasifikasi `ELSA`. Klik langsung piksel foto, salah satu neuron Input, atau salah satu kelas Output untuk menyorot koneksinya!",
        "• **Aturan Kunci yang Akurat secara Ilmiah:** Tekankan kotak catatan bawah: (1) **Ukuran piksel × channel gambar (`H × W × C`)** menentukan jumlah neuron di **Input Layer** pada Neural Network gambar (grayscale `C=1` → tepat `H×W`; RGB `C=3` → `3×` lebih banyak karena tiap piksel punya 3 nilai R, G, B); (2) **Jumlah kelas gambar** menentukan jumlah neuron di **Output Layer** untuk klasifikasi multi-kelas (5 kelas Frozen → 5 neuron + Softmax; pengecualian: untuk klasifikasi biner 2 kelas cukup 1 neuron Sigmoid).",
        "• **Transisi ke Slide 24:** \"Sekarang kita lihat bagaimana setiap kabel penghubung dari Input Layer ke Output Layer bekerja dalam lapisan **`Dense` (*Fully Connected*)** sekaligus cara menghitung jumlah parameternya!\"",
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
        "**Tujuan Slide (0 menit — Referensi Materi 1/2 · Bab 1 & Bab 2):** 6 tautan rujukan resmi dari `docs/PLAN.md` khusus memperdalam **Bab 1 (AI Klasik vs Modern, Supervised Learning & ML vs DL — Slide 6–9)** dan **Bab 2 (4 Tugas Computer Vision & Pengolahan Piksel — Slide 12–16, Recap S03)** (`[CEK LINK]` untuk tautan belum diverifikasi ulang).",
        "• **Catatan Penggunaan:** Tidak perlu dibahas panjang di kelas; peserta bisa membuka tautan sesuai bab yang ingin diulang di rumah.",
    ],
    59: [
        "**Tujuan Slide (0 menit — Referensi Materi 2/2 · Bab 3 & Hands-On):** 6 tautan rujukan resmi dari `docs/PLAN.md` khusus **Bab 3 (Neuron, Flatten, Dense+Parameter, Weight+Bias, ReLU/Sigmoid/Tanh/Softmax, Loss, Backprop, Gradient Descent, LR/Adam & Overfitting — Slide 20–33)** serta praktik **Keras Sequential (`S47–S49`)**.",
        "• **Rekomendasi Utama:** Video 3Blue1Brown #7 (`S20–S29`), TensorFlow Playground #10 (`S28, S31–S32`), dan Keras Sequential Guide #11 (`S24, S47–S49`).",
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
        [55, 54, 58, 59, 46, 47, 48, 49, 50, 51, 52, 56, 57]
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
                "**Tujuan Slide (2 menit):** Memberikan gambaran utuh sesi 120 menit dalam 1 halaman ringkas — menyatukan 3 Bab teori (`AI/ML/DL` 9m, `4 Tugas CV` 9.5m, `Bedah Total Neural Network` 29.5m), Kuis 5 Soal, Kamus 16 Istilah & Referensi Materi (7.5m), serta Hands-On 5 Tahap Mikro-Task & Rangkuman Penutup (58.5m) beserta 3 *Learning Goals* di kanan."
            )
            _notes[1] = (
                "• **Naskah Pengajar:** Bacakan singkat ritme 120 menit (`61,5 menit` pembuka, Bab 1–3, kuis & kamus, lalu `58,5 menit` sesi hands-on praktik model 1-layer & rangkuman penutup), lalu tunjuk 3 target penguasaan di kanan."
            )
        elif _orig_idx == 23:
            # Slide 23 tetap Input & Output Layer, lalu sisipkan Slide 24 (Dense & Parameter) + Slide 25 (Q&A #4)!
            pass
        elif _orig_idx == 24:
            _notes = [
                "**Tujuan Slide (3 menit — Tahap 4 · Simulasi Training Alur Utuh):** Menjawab secara konkret & matematis bagaimana Neural Network bisa tahu foto ini adalah **Elsa** (atau karakter lain) lewat **Simulasi Training** pada 5 foto nyata Frozen berlabel (`Anna, Elsa, Kristoff, Olaf, Sven`), memakai **jumlah neuron Input Layer asli `150.528` (`224×224×3`)** dengan menyorot 2 tahap hitungan: **Tahap 4.1 Weight + Bias (`z = Σ(x·w) + b`)** dan **Tahap 4.2 Activation Function (`Softmax`)**.",
                "• **Panduan Demo Interaktif:** Klik **`Sebelum Training (Acak)`** dulu agar peserta melihat bobot acak menghasilkan tebakan salah (`Elsa 14.4%`, kalah dari Kristoff `45.8%`). Lalu klik **`▶ Play`** (atau **`⏭ +1 Tahap Hitung`** / **`↺ Reset`**): sorot bagaimana piksel pojok latar bobotnya `w ≈ 0` (diabaikan), `150.522` piksel objek membawa sumbangan utama (`Σ = +3.17`), ditambah `Bias (-1.04)` → `z₂ = +2.13` → Softmax `e^(+2.13) / 10.82 = 77.7% ✅`!",
                "• **Transisi ke Tahap 4.1 (Slide 27):** \"Di kotak kuning dan kotak hijau tadi ada mesin inti yang bekerja: **Weight + Bias**, **Activation Function**, dan **Output Akhir**. Mari kita bedah masing-masing di tiga slide berikutnya!\"",
            ]
        elif _orig_idx == 25:
            _notes = [
                "**Tujuan Slide (2.5 menit — Tahap 4.1 · Weight & Bias):** Membedah khusus **Tahap 4.1 (`Weight & Bias`)** secara runtut (Apa itu, Kenapa perlu, Cara kerja) dengan **diagram Zoom-In kabel nyata `150.528` neuron dari Slide 26** yang persis sama angkanya per setiap karakter.",
                "• **Panduan Demo Interaktif:** Tunjuk strip peta atas (`📍 Posisi di Tahap 4: Input 150.528 → 🔍 Tahap 4.1: Weight + Bias → z → Tahap 4.2`). Klik **`▶ Play`** atau pilih chip 5 karakter, lalu uji **`Coba Bias = 0`** dan **`Coba Balik Weight`** (kabel 150.522 piksel berbalik merah → Elsa jatuh ke `0.5% ❌`), geser 2 slider bawah, dan klik **`↺ Reset`** untuk kembali!",
                "• **Transisi ke Tahap 4.2 (Slide 28):** \"Setelah Tahap 4.1 menghasilkan skor mentah `z₂ = +2.13`, angkanya langsung masuk ke **Tahap 4.2: Activation Function** — mari kita zoom-in di slide berikutnya!\"",
            ]
        elif _orig_idx == 26:
            _notes = [
                "**Tujuan Slide (2.5 menit — Tahap 4.2 · Activation Function):** Membedah fungsi aktivasi (**`ReLU`**, **`Sigmoid`**, **`Tanh`**, & **`Softmax`**) — mengapa *non-linearity* wajib ada agar tumpukan neuron mampu mengenali bentuk kompleks.",
                "• **Panduan Demo Interaktif:** Jalankan tab **`1. ReLU`** (`max(0, z)` memotong skor negatif jadi `0`), **`2. Sigmoid`** (`0–100%`), **`3. Tanh`** (`−1 s/d +1` terpusat nol), dan **`4. Softmax`** (5 skor kelas → total tepat `100%`, persis Slide 26!). Geser slider `Geser z` untuk melihat perubahan langsung.",
                "• **Transisi ke Tahap 4.3 (Slide 29):** \"Setelah Softmax menghasilkan 5 probabilitas di atas, bagaimana model memutuskan 1 jawaban akhir dan menghitung Error? Mari lanjut ke **Tahap 4.3: Output Akhir**!\"",
            ]
        elif _orig_idx == 27:
            _notes = [
                "**Tujuan Slide (2.5 menit — Tahap 4.3 · Output Akhir & Error):** Melengkapi trilogi Zoom-In dari Slide 26 (**Tahap 4.1 Slide 27 → 4.2 Slide 28 → 4.3 Output Akhir Slide 29**): menunjukkan bagaimana 5 probabilitas Softmax diubah menjadi 1 keputusan lewat **`Argmax`**, dicek keyakinannya (*Confidence* vs *Threshold*), lalu dibandingkan dengan **Label Asli** untuk menghitung **Error & Cross-Entropy Loss**.",
                "• **Panduan Demo Interaktif (`▶ Play` / `■ Stop` / `↺ Reset`):** Di mode **`1. Terlatih`**, tunjukkan 5 karakter Frozen lolos yakin (`Elsa 77.7%`). Klik **`2. Ragu (Tipis)`** (`Elsa 41.9% ⚠`) dan geser **`Ambang Yakin (Threshold)`**. Terakhir klik **`3. Acak (Belum Latih)`** pada **Olaf** (`P=11.3%`, salah tebak `Kristoff`, `Error = 88.7%`, `Loss = 2.18`).",
                "• **Transisi ke Tahap 5 (Slide 30 — Siklus Belajar Utuh):** \"Tadi kita lihat foto Olaf yang belum dilatih punya **Error 88.7% (Loss 2.18)**. Nah, bagaimana caranya angka Loss besar ini mengubah *Weight* & *Bias* sampai Olaf dikenali 79.2%? Mari lihat **Tahap 5: Siklus Belajar Utuh** di Slide 30!\"",
            ]
        elif _orig_idx == 42:
            _notes.insert(
                1,
                "• **Pengantar Singkat MLP & Hidden Layer (20–30 detik):** Jelaskan singkat bahwa jaringan standar di Bab 3 yang semua neuronnya disambung penuh (plus 1 lapisan tengah bernama *Hidden Layer*, mis. `Dense(128)`) disebut **MLP (*Multi-Layer Perceptron*)** — dan untuk foto `224×224×3` (`150.528` input), sambungan penuhnya langsung menghasilkan `150.528 × 128 + 128 = 19,27 juta parameter`!",
            )
        elif _orig_idx == 45:
            _notes[0] = _notes[0].replace("Q&A #6", "Q&A #4")
        elif _orig_idx == 46 and HIDE_BAB4_ARCH:
            _notes = [
                f"**Tujuan Slide (1 menit — Cover Hands-On Visual-First):** Pembuka sesi praktik langsung **Hands-On: Praktik Neural Network** pada dataset foto Disney Frozen (`{_HO_TOTAL}` foto), dipecah menjadi mikro-task **Tahap 1 → Tahap 5.4** selaras Bab 3.",
                "• **Catatan Instruktur:** Ajak peserta membuka `materials/P02/p02_teori_neural_network.ipynb` di Google Colab atau Jupyter lokal. Jelaskan bahwa kode grafik sudah dirapikan ke *Alat Visualisasi Siap Pakai* sehingga setiap sel kerja cuma 3–6 baris dan langsung menampilkan gambar output nyata!",
            ]
        elif _orig_idx == 47 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (9 menit — Hands-On Tahap 0 & Tahap 1):** Menjalankan Setup + Alat Visualisasi + Galeri Frozen (Tahap 0), lalu membimbing peserta mengerjakan **Tahap 1.1 (`# TODO 1`: `/ 255.0`)** dan **Tahap 1.2 (`# TODO 2`: `foto_mini[4, 2]`)**.",
                f"• **Panduan Praktik:** Sorot visual 3 panel yang muncul: foto asli Elsa → grid `8×8` kotak angka `0.0–1.0` → zoom piksel gaun biru `[4, 2]` dengan kanal Biru (`B = {_HO_B_VAL}`) paling tinggi!",
            ]
        elif _orig_idx == 48 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (9 menit — Hands-On Tahap 2):** Membimbing peserta mengerjakan **Tahap 2.1 (`# TODO 3`: `.flatten()`)** dan **Tahap 2.2 (`# TODO 4`: `150.528` neuron → `752.645` parameter, persis Slide 21–24 & 33)**.",
                "• **Momen Klik:** Tunjuk gambar **Pita 1D 64 Piksel Warna (`B1..B8`)**: warna biru gaun Elsa di baris `B4–B5` benar-benar terlihat pindah menjadi garis lurus di tengah pita 1D!",
            ]
        elif _orig_idx == 49 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (9 menit — Hands-On Tahap 3):** Membimbing **Tahap 3.1 (`# TODO 5`: rumus kali-tambah biasa `r*w_r + g*w_g + b*w_b + bias`)**, **Tahap 3.2 (`# TODO 6`: `ReLU` + perbandingan singkat `Tanh` Slide 28)**, dan **Tahap 3.3 (eksperimen bebas `Softmax` & `Loss`)**.",
                "• **Tips Mengajar:** Tidak ada rumus `np.dot` atau `exp` rumit — biarkan peserta bermain mengubah angka `skor_olaf` di Tahap 3.3 untuk melihat foto, bar pemenang `Argmax`, & nilai `Loss` berpindah seketika!",
            ]
        elif _orig_idx == 50 and HIDE_BAB4_ARCH:
            _notes = [
                f"**Tujuan Slide (9.5 menit — Hands-On Tahap 4):** Memuat `{_HO_TOTAL}` foto Frozen `64×64×3` (Tahap 4.1), merakit 2 layer Keras di **Tahap 4.2 (`# TODO 7`: `Flatten()` + `Dense(5, softmax)`)** & mencocokkan `61.445` di `summary()`, lalu menjalankan **Tahap 4.3 (Model Bayi Epoch 0 — Weight Init acak Slide 31)**.",
                f"• **Catatan Penting:** Melihat *Model Bayi* menebak ngawur (`{_HO_S0}/5`, `Loss {_HO_E0_LOSS}`, bar ~20% rata) di Epoch 0 adalah momen penting agar peserta langsung paham mengapa proses training (`model.fit`) dibutuhkan!",
            ]
        elif _orig_idx == 51 and HIDE_BAB4_ARCH:
            _notes = [
                f"**Tujuan Slide (9.5 menit — Hands-On Tahap 5.1 & 5.2):** Membimbing **Tahap 5.1 (`# TODO 8`: `model_nn.fit` {_HO_EPOCHS} epoch, `batch_size=16 → {_HO_STEPS} Step/Epoch` persis Slide 32)** dan **Tahap 5.2 (plot kurva Loss turun & Akurasi naik)** yang tersimpan ke `results/p02_nn_loss_curve.png`.",
                f"• **Panduan Diskusi:** Tunjuk angka `{_HO_STEPS}/{_HO_STEPS}` di sebelah tiap Epoch (`{_HO_TOTAL} ÷ 16`), sorot Loss turun di bawah `1.0` (`{_HO_E1_LOSS} → {_HO_END_LOSS}`) & Akurasi naik ke `{_HO_END_ACC}%`, lalu ingatkan bahwa Group Split bebas *leakage* dipelajari khusus di **P05**.",
            ]
        elif _orig_idx == 52 and HIDE_BAB4_ARCH:
            _notes = [
                f"**Tujuan Slide (8.5 menit — Hands-On Tahap 5.3, 5.4 & Bonus):** Menjalankan **Tahap 5.3 (Before vs After `{_HO_S0}/5 → {_HO_SEND}/5` + uji visual 5 foto `X_5ramai` & cek Polos `{_HO_POLOS_ACC}%` vs Ramai `{_HO_RAMAI_ACC}%`)**, **Tahap 5.4 (Intip Peta Fokus Bobot `ΔW`)**, serta bonus mengubah `LEARNING_RATE_COBA` (Slide 31).",
                "• **Momen Aha & Jembatan P03:** Jelaskan mengapa skor foto `ramai` pada data latih tampak tinggi (`shortcut learning` / menghafal warna latar — *Overfitting* Slide 32) serta area terang `ΔW` di tengah — inilah jembatan sempurna menuju **CNN di P03** & **Group Split di P05**!",
            ]
        elif _orig_idx == 54 and HIDE_BAB4_ARCH:
            _notes = [
                "**Tujuan Slide (2 menit — Kamus Istilah):** Mengulas 16 istilah asli Bab 1–3 (`4` Bab 1 + `4` Bab 2 + `8` Bab 3) dalam format **2-Column Grouped Dictionary List** (Kiri: Bab 1 & Bab 2 · Kanan: Bab 3).",
                "• **Panduan Interaktif:** Gunakan kotak **`Cari istilah...`**, tombol filter **`Semua (16)` / `Bab 1 (4)` / `Bab 2 (4)` / `Bab 3 (8)`**, atau klik kode slide (`S06 ↗`–`S32 ↗`) untuk langsung melompat ke visual konsepnya.",
            ]
        elif _orig_idx == 55 and HIDE_BAB4_ARCH:
            # 5 Slide Kuis Terpisah (Slide 35–39, masing-masing 1 menit = 5 menit total!)
            _quiz_notes_5 = [
                [
                    "**Tujuan Slide (1 menit — Kuis 1/5 · Bab 1):** Menguji pemahaman hierarki **AI ⊃ ML ⊃ DL** sekaligus menyambungkan **AI Klasik (Minimax/A*) vs AI Modern**, **Supervised Learning**, & **Feature Learning otomatis** (`Slide 6–9`).",
                    "• **Panduan Interaktif:** Minta peserta mengklik pilihan A/B/C terlebih dahulu (hijau/merah langsung muncul), lalu klik **Lihat Jawaban & Penjelasan** agar diagram Venn AI → ML → DL dengan contoh Frozen tampil di kanan.",
                ],
                [
                    "**Tujuan Slide (1 menit — Kuis 2/5 · Bab 2):** Menguji perbedaan **Multi-Class Image Classification (5 kelas Frozen, Slide 13)** vs **Object Detection (`[x, y, w, h] + label + yakin`, contoh YOLO, Slide 14)**, serta pembeda singkat dari Segmentation & Tracking (`Slide 15–16`).",
                    "• **Panduan Interaktif:** Setelah peserta memilih opsi, buka jawaban untuk menunjukkan ilustrasi foto Frozen nyata berdampingan antara Multi-Class Classification (`ELSA 94%`) dan Object Detection (`[x, y, w, h] + Label`).",
                ],
                [
                    "**Tujuan Slide (1 menit — Kuis 3/5 · Bab 3 Tahap 2):** Menguji rumus jumlah neuron **Input Layer** pada foto RGB (`100 × 100 × 3 = 30.000`) dan mengaitkannya ke `Dense(5)` (`752.645` parameter, `Slide 21–24`).",
                    "• **Panduan Interaktif:** Ingatkan jebakan umum pemula (lupa mengalikan 3 channel RGB sehingga menjawab 10.000). Sambungkan hasilnya ke skala penuh Frozen (`224×224×3 = 150.528` neuron → `752.645` param).",
                ],
                [
                    "**Tujuan Slide (1 menit — Kuis 4/5 · Bab 3 Tahap 4.2–4.3):** Menguji peran **Softmax** di *Output Layer* 5 karakter Frozen dibanding aktivasi lain di Slide 28 (**`ReLU`**, **`Sigmoid`**, & **`Tanh`**).",
                    "• **Panduan Interaktif:** Setelah membuka jawaban, tunjuk 5 bar probabilitas berikon karakter Frozen di kanan (`Elsa 68.3% ★`, total tepat `100.0%`) dan tegaskan kapan memakai `ReLU/Sigmoid/Tanh` vs `Softmax`.",
                ],
                [
                    "**Tujuan Slide (1 menit — Kuis 5/5 · Bab 3 Tahap 5):** Menguji pasangan proses koreksi bobot **Backpropagation + Gradient Descent** (berjalan per **Batch**, diatur **Learning Rate** & optimizer **Adam**, `Slide 30–33`) yang menurunkan *Mean Loss* `1.70 → 0.21`.",
                    "• **Panduan Interaktif:** Setelah membuka jawaban, tunjuk ilustrasi *Loss & Gradient Descent* di kanan lalu beri transisi semangat menuju **Kamus 16 Istilah (Slide 40)** dan **Hands-On**!",
                ],
            ]
            for _qn in _quiz_notes_5:
                SLIDE_EXPLANATIONS[_new_idx] = _qn
                _new_idx += 1
            continue
        elif _orig_idx == 56 and HIDE_BAB4_ARCH:
            _notes = [
                f"**Tujuan Slide (2 menit — Rangkuman Inti 3 Poin Utama):** Mengunci seluruh sesi **P02 — Teori Neural Network** dalam 3 pilar terstruktur beserta visual proyek Frozen, alur 5 tahap Bab 3, capaian nyata Hands-On {_HO_EPOCHS} Epoch, dan jembatan ke **P03 — Arsitektur Neural Network**.",
                f"• **Naskah Pengajar:** Bacakan 3 pilar: (01) AI Klasik vs Modern, peta `AI ⊃ ML ⊃ DL`, & *Multi-Class Image Classification* 5 karakter Frozen; (02) 5 Tahap runtut (`Piksel → Flatten → Dense(5) 752.645 → ReLU/Sigmoid/Tanh/Softmax → Backprop, Adam, LR, Batch & Overfitting`); (03) Hands-On 1-Layer nyata (`Loss {_HO_E1_LOSS} → {_HO_END_LOSS}`, `{_HO_S0}/5 → {_HO_SEND}/5 ✓`, `Polos {_HO_POLOS_ACC}% vs Ramai {_HO_RAMAI_ACC}%`) menjadi alasan kuat lanjut ke **P03 (Arsitektur Neural Network)** & **P05 (Group Split)**. Ingatkan Kamus Slide 40, Referensi Slide 41–42, dan menyimpan `results/p02_nn_loss_curve.png` sebelum berpindah ke Slide Penutup.",
            ]
        elif _orig_idx == 57:
            _notes = (
                [
                    "**Tujuan Slide (1 menit — Closing & Key Quote):** Menutup sesi P02 dengan kutipan penutup yang tenang, apresiasi hangat atas kerja keras peserta menuntaskan teori & Hands-On 30 Epoch, serta undangan antusias ke **P03 — Arsitektur Neural Network**.",
                    "• **Naskah Pengajar:** Bacakan kutipan penutup dengan santai, beri apresiasi spesifik atas momen terbaik peserta selama kuis dan praktik notebook hari ini, tanyakan apakah ada pertanyaan terakhir, lalu tutup dengan pesan pembuka menuju P03!",
                ]
                if HIDE_BAB4_ARCH
                else [
                    _notes[0],
                    _notes[-1].replace("Slide 58–59", "Slide 47–48"),
                ]
            )
        SLIDE_EXPLANATIONS[_new_idx] = _notes
        _new_idx += 1
        if _orig_idx == 23:
            # Sisipkan Slide 24: Dense (Fully Connected) & Menghitung Parameter (W + b)
            SLIDE_EXPLANATIONS[_new_idx] = [
                "**Tujuan Slide (1.5 menit — Tahap 3.2 · Dense & Parameter Interaktif):** Menjelaskan arti lapisan **`Dense` (*Fully Connected*)** dan rumus praktis **`Total Parameter = (Input × Output) + Bias`** lewat simulator perakitan kabel interaktif.",
                "• **Panduan Demo Interaktif (`▶ Play` / `⏭ +1 Langkah` / Klik Neuron `x₁..xₙ` & `y₁..y₅`):** Tekan **`▶ Play`** untuk memperlihatkan `x₁ → x₂ → x₃ → semua` menyambungkan 5 kabel bobot ke semua output (`n × 5 W`) lalu `+ 5 Bias`, dan klik tombol skala (**Mini `8×8` → `965`**, **Hands-On `64×64` → `61.445`**, **Penuh `224×224` → `752.645`**) agar peserta melihat kecocokan 100% dengan `model.summary()` Keras!",
            ]
            _new_idx += 1
            # Sisipkan NEW Slide 25: Tanya-Jawab #4 (Cek Pemahaman Parameter Dense)
            SLIDE_EXPLANATIONS[_new_idx] = [
                "**Tujuan Slide (1 menit — Bab 3 · Tanya-Jawab #4):** Mengunci rumus parameter `Dense` (`(Input × Output) + Bias`) di tengah Bab 3 sebelum masuk ke Tahap 4 (Simulasi Training).",
                "• **Aktivitas Kelas:** Minta peserta menghitung `100` neuron input ke `5` neuron output Frozen (`100 × 5 = 500 Weight`, ditambah `5 Bias` = **`505` parameter**, Kunci: **C**). Ingatkan agar tidak melupakan *Bias* (pengecoh B).",
            ]
            _new_idx += 1
        if _orig_idx == 27:
            # Sisipkan Slide 30: Siklus Belajar Utuh (menyambung langsung dari Error/Loss Slide 29!)
            SLIDE_EXPLANATIONS[_new_idx] = [
                "**Tujuan Slide (2 menit — Tahap 5.1):** Mengikat seluruh Bab 3 menjadi **1 siklus belajar utuh**: `Forward Pass → Hitung Loss → Backpropagation & Gradient Descent → Ulangi tiap Epoch`, memakai angka nyata foto **Olaf** (`Loss 2.18 → 0.23`, `P(Olaf) 11.3% → 79.2%`).",
                "• **Panduan Demo Interaktif (`▶ Play` / `■ Stop` / `⏭ +1 Tahap` / `↺ Reset`):** Jalankan 4 tahap satu per satu (Forward → Loss → Backprop+GD → Epoch) lalu ajak peserta melihat efek *Learning Rate* & *Optimizer* di slide berikutnya!",
            ]
            _new_idx += 1
            # Sisipkan Slide 31: Weight Initialization, Learning Rate & Optimizer (SGD vs Adam)
            SLIDE_EXPLANATIONS[_new_idx] = [
                "**Tujuan Slide (2 menit — Tahap 5.2 · Simulator Interaktif Weight Init, Learning Rate & Optimizer):** Mendemonstrasikan langsung **Weight Initialization** (bobot acak Epoch 0), efek **Learning Rate** terlalu kecil vs ideal vs terlalu besar, dan keunggulan adaptif **Optimizer `Adam ★` vs `SGD`**.",
                "• **Panduan Demo Interaktif (`▶ Play` / `⏭ +1 Langkah` / `🎲 Acak Bobot` / Slider `LR` / `Duel SGD vs Adam`):** Klik **`🎲 Acak Bobot`** (atau klik langsung kurva parabola) untuk melihat posisi awal acak, jalankan **`▶ Play`** di preset **`1. LR Kecil`**, **`2. LR Ideal`**, dan **`3. LR Besar`** (memantul liar!), lalu klik **`Duel SGD vs Adam`** agar peserta melihat **`Adam ★`** stabil menuju dasar lembah!",
            ]
            _new_idx += 1
            # Sisipkan Slide 32: Batch Size vs Step vs Epoch & Pengenalan Overfitting
            SLIDE_EXPLANATIONS[_new_idx] = [
                "**Tujuan Slide (2 menit — Tahap 5.3 · Dua Simulator Interaktif Batch Size & Overfitting):** Mendemonstrasikan langsung kaitan **`Batch Size` → `Step` → `Epoch`** pada `143` foto Frozen (Kiri) dan transisi **`Underfitting` → `Good Fit (Generalization)` → `Overfitting`** (Kanan).",
                "• **Panduan Demo Interaktif:** Di Kiri, tunjuk alur 3 tahap (**Tumpukan 143 Foto → Mesin NN + Meteran Beban RAM → Counter Koreksi Bobot `W & b`**); tekan **`▶ Play 1 Epoch`** atau bandingkan **`16 ★`** (*RAM 36% Pas, 9× update*) vs **`143`** (*RAM 98% PENUH, cuma 1× update*). Di Kanan, tiap kondisi (**`Underfit`**, **`Good Fit ✓`**, **`Overfit`**) bisa di-**`▶ Play`** sendiri-sendiri (`Epoch 1→30`) PLUS tab **`Semua`** (`Epoch 1→50`)!",
            ]
            _new_idx += 1
            # Sisipkan Slide 33 (Ultimate Bab 3): Simulasi Full Neural Network End-to-End (Tahap 1–5)!
            SLIDE_EXPLANATIONS[_new_idx] = [
                f"**Tujuan Slide ({'3.5' if HIDE_BAB4_ARCH else '3'} menit — Ultimate Bab 3):** Merangkum **seluruh Bab 3 (Tahap 1 → 5)** dalam **1 simulasi end-to-end Neural Network nyata 1-layer** (`150.528 Input → 5 Output Softmax = 752.645 parameter`) yang dilatih langsung 8 *epoch* melewati kelima foto figurin Frozen.",
                "• **Panduan Demo Interaktif (`▶ Full 8 Epoch` / `▶ 1 Foto` / `⏭ +1 Tahap` / Slider `Epoch 1–8`):** Klik **`▶ Full 8 Epoch`** (~18 detik) agar peserta menyaksikan proses training utuh melewati **Anna → Elsa → Kristoff → Olaf → Sven** dari **Epoch 1 (`0/5`, Mean Loss `1.70`)** hingga **Epoch 8 (`5/5 Yakin ≥ 74%`, Mean Loss `0.21 ✅`)**!",
                (
                    "• **Transisi ke Slide 34 (Cover Kuis, Kamus & Referensi Materi):** \"Seluruh teori Neural Network Bab 1–3 sudah tuntas! Mari kita uji cepat lewat 5 slide kuis berilustrasi, kamus 16 istilah, dan referensi materi sebelum masuk Hands-On!\""
                    if HIDE_BAB4_ARCH
                    else "• **Jembatan Emas ke Bab 4:** Tunjuk jumlah parameter `752.645` sebagai jembatan menuju **Bab 4**!"
                ),
            ]
            _new_idx += 1
            if HIDE_BAB4_ARCH:
                # Sisipkan Slide 34: Cover Kuis, Kamus Istilah & Referensi Materi
                SLIDE_EXPLANATIONS[_new_idx] = [
                    "**Tujuan Slide (0.5 menit — Cover Evaluasi & Referensi Materi):** Pembatas visual rapi setelah Bab 3 sebelum masuk ke **5 Slide Kuis Berilustrasi**, **Kamus 16 Istilah**, dan **Referensi Materi Bab 1–3**.",
                    "• **Naskah Pengajar:** \"Tiga bab teori inti sudah tuntas! Mari kita uji cepat pemahaman lewat 5 kuis interaktif, rangkum 16 istilah kunci, dan lihat referensi materi Bab 1–3.\"",
                ]
                _new_idx += 1
else:
    SLIDE_EXPLANATIONS = dict(_ALL_SLIDE_EXPLANATIONS)
