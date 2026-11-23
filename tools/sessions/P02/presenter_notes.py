"""Naskah Penjelasan Detail per Slide untuk P02: Teori Neural Network (ANN) (Slide 1 s.d. 59).

Standar penulisan:
- Menggunakan istilah asli Deep Learning (Neuron, Layer, Weight, Bias, ReLU, Softmax,
  Loss, Gradient Descent, Learning Rate, Backpropagation, Batch, Epoch, Overfitting, Flatten)
  dengan penjelasan bahasa Indonesia sehari-hari yang sederhana dan ramah pemula non-IT.
- Dipakai oleh:
  1. `tools/core/exporter.py` -> Speaker Notes PPTX (100% slide)
  2. `tools/core/exporter.py` -> `materials/P02/P02_presenter_script.pdf` (A4 Portrait, 1 slide/halaman)
"""

from __future__ import annotations

SLIDE_EXPLANATIONS: dict[int, list[str]] = {
    1: [
        "**Tujuan Slide (1 menit):** Menyambut peserta masuk ke P02 (*Teori Neural Network / ANN*) berdurasi **120 menit** dan membangun rasa percaya diri bahwa cara kerja AI bisa dipahami langkah demi langkah tanpa rumus rumit.",
        "• **Naskah Pengajar:** \"Di P01 kita sudah berhasil mengubah foto menjadi matriks angka `0.0–1.0`. Hari ini kita membongkar bagaimana **Neural Network** memproses angka-angka tersebut sampai bisa menebak 5 karakter **Disney Frozen** milikmu sendiri.\"",
        "• **Sorotan Visual:** Tunjukkan diagram 3 lapisan (*Input → Hidden → Softmax*) di sebelah kanan serta 7 topik inti di bagian bawah.",
        "• **Transisi:** \"Mari kita lihat dulu peta 5 bab perjalanan belajar kita hari ini.\"",
    ],
    2: [
        "**Tujuan Slide (1 menit):** Memberi gambaran besar 5 bab agar peserta tahu arah belajarnya dan tidak merasa tersesat saat istilah baru muncul.",
        "• **Naskah Pengajar:** Bacakan singkat alur 5 bab: Bab 1 mengenal **Neuron & Layer**, Bab 2 mengenal **ReLU & Softmax**, Bab 3 memahami cara model belajar lewat **Loss, Gradient Descent, & Backpropagation**, Bab 4 melihat batas **MLP** pada foto Frozen, dan Bab 5 praktik langsung di notebook.",
        "• **Poin Penenang Pemula:** Tekankan bahwa kita tetap memakai istilah asli Deep Learning (*Neuron, Weight, Bias, Softmax, Loss*) supaya peserta familier dengan literatur dan kode Keras, tetapi semuanya dijelaskan dengan bahasa sehari-hari.",
        "• **Transisi:** \"Sekarang kita cek pembagian waktu 120 menit supaya sesi berjalan santai.\"",
    ],
    3: [
        "**Tujuan Slide (1 menit):** Menyepakati ritme kelas 120 menit agar peserta tahu kapan teori, kapan istirahat, dan kapan praktik kode.",
        "• **Naskah Pengajar:** Jelaskan proporsi sesi: 10 menit pembuka & kenalan dataset Frozen, 30 menit teori + 6 simulator interaktif, 5 menit istirahat wajib, 50 menit praktik notebook sel pendek, 15 menit *Mini-Challenge*, dan 10 menit kuis/penutup.",
        "• **Interaksi Singkat:** Tanyakan ke peserta apakah sudah siap membuka *Google Colab* nanti di menit ke-45 (belum perlu dibuka sekarang supaya fokus dulu ke konsep).",
        "• **Transisi:** \"Sebelum mulai, ini 3 kemampuan praktis yang akan langsung kamu kuasai di akhir sesi.\"",
    ],
    4: [
        "**Tujuan Slide (1 menit):** Menetapkan 3 target belajar konkret dan terukur sesuai `docs/PLAN.md`.",
        "• **Naskah Pengajar:** Bacakan 3 target: (1) Bisa menghitung output 1 **Neuron** (`input × weight + bias`) dengan tangan; (2) Paham alasan memakai **ReLU** di *hidden layer* dan **Softmax** di *output layer*; (3) Bisa membaca grafik *Train vs Validation Loss* untuk mendeteksi **Overfitting**.",
        "• **Sorotan Visual:** Tunjuk kotak *Contoh Target* di setiap kartu agar peserta merasakan bahwa hasilnya konkret, bukan sekadar teori abstrak.",
        "• **Transisi:** \"Sekarang mari kita sambungkan materi P01 dengan dataset proyek akhir kita.\"",
    ],
    5: [
        "**Tujuan Slide (1.5 menit):** Menghubungkan akhir P01 (matriks piksel `0.0–1.0`) langsung ke dataset proyek akhir nyata peserta (`data/frozen_v1/`).",
        "• **Naskah Pengajar:** Tunjukkan galeri 5 kelas asli (**Anna, Elsa, Kristoff, Olaf, Sven**) dalam 2 kondisi: baris atas **Polos** (`102` foto) vs baris bawah **Ramai** (`41` foto) lintas **7 sesi foto**. Ingatkan lagi kenapa aturan `if-else` manual gagal ketika objek bergeser atau latarnya ramai.",
        "• **Catatan Penting:** Tegaskan bahwa jumlah foto `143` di `v1` bersifat dinamis — kalau peserta menambah foto di versi berikutnya, seluruh kode kita membacanya otomatis dari folder `DATA_DIR`.",
        "• **Transisi:** \"Dengan data ini di depan mata, mari kita masuk ke Bab 1 untuk melihat bagaimana 1 Neuron bekerja!\"",
    ],
    6: [
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 1: Anatomi Neuron & Layer**.",
        "• **Naskah Pengajar:** \"Di Bab 1 ini kita tidak langsung masuk rumus. Kita mulai dari cara matamu sendiri mengenali foto Elsa, lalu kita terjemahkan pelan-pelan menjadi **Neuron** dan **Layer**.\"",
        "• **Transisi:** \"Coba lihat foto Elsa di slide berikutnya.\"",
    ],
    7: [
        "**Tujuan Slide (1 menit):** Membangun intuisi *zero-math* tentang bagaimana evaluasi ciri-ciri visual bekerja sebelum memperkenalkan simbol `x, w, b`.",
        "• **Pertanyaan Pancingan:** Tanyakan langsung ke peserta: *\"Saat melihat foto di kiri, ciri apa yang paling cepat membuatmu yakin ini Elsa?\"* Dengarkan jawabannya (gaun biru, rambut pirang, tidak bertanduk).",
        "• **Naskah Pengajar:** Tunjukkan 3 kotak poin di kanan: warna biru muda memberi bobot positif besar (`+3`), rambut pirang mendukung (`+2`), sedangkan tanduk rusa menolak keras (`-5`). Jika total skornya melewati batas minimum, kita menyimpulkan \"Ini Elsa!\".",
        "• **Transisi:** \"Nah, 4 hal yang baru saja kita lakukan di kepala punya nama resmi di Neural Network. Mari kita pasangkan satu per satu.\"",
    ],
    8: [
        "**Tujuan Slide (1 menit):** Memetakan penjelasan sederhana di Slide 7 ke 4 istilah asli **Neuron**: `Input (x)`, `Weight (w)`, `Bias (b)`, dan `Activation Function`.",
        "• **Naskah Pengajar:** Bacakan pasangan kiri–kanan secara perlahan: Ciri pada foto = **Input (`x`)**; Seberapa besar pengaruh tiap ciri = **Weight / Bobot (`w`)**; Batas ambang minimal = **Bias (`b`)**; Aturan keluaran akhir = **Activation Function**.",
        "• **Penegasan Penting:** Tekankan kotak biru bawah: 1 **Neuron** hanyalah unit hitung sederhana (`input × weight + bias` lalu masuk aktivasi), bukan sesuatu yang misterius.",
        "• **Transisi:** \"Supaya benar-benar nempel, yuk kita hitung pakai angka bulat pada foto Elsa vs foto Sven!\"",
    ],
    9: [
        "**Tujuan Slide (1 menit):** Melatih hitungan tangan pertama dengan angka bulat sederhana sehingga peserta merasakan sendiri perbedaan output **AKTIF** vs **TIDAK AKTIF**.",
        "• **Aktivitas Interaktif:** Ajak peserta ikut menghitung lisan baris demi baris: pada **Kasus A (Foto Elsa)**, `1×3 + 1×2 + 0×(-5) − 3 = +2` (positif → Neuron **AKTIF**!). Lalu pindah ke **Kasus B (Foto Sven)**: `0×3 + 0×2 + 1×(-5) − 3 = -8` (negatif → Neuron **TIDAK AKTIF**!).",
        "• **Poin Kunci:** Perhatikan bahwa *Weight* (`+3, +2, -5`) dan *Bias* (`-3`) di kedua sisi **persis sama** — yang berubah hanya angka *Input* dari fotonya.",
        "• **Transisi:** \"Karena hitungan angka bulat tadi sudah lancar, sekarang diagram resmi 1 Neuron akan terlihat sangat mudah dibaca.\"",
    ],
    10: [
        "**Tujuan Slide (1 menit):** Memperkenalkan diagram arsitektur resmi 1 Neuron lengkap dengan simbol `x₁, x₂, x₃`, `w₁, w₂, w₃`, `+ b`, `Σ + b`, dan `f(z)`.",
        "• **Naskah Pengajar:** Tunjuk alur dari kiri ke kanan pada SVG: nilai warna RGB (`0.0–1.0`) dikalikan dengan masing-masing *Weight*, dijumlahkan bersama *Bias* menghasilkan skor mentah `z`, lalu masuk ke fungsi aktivasi `f(z)`.",
        "• **Hal Wajib Ditekankan:** Baca kotak putih di kanan — manusia **tidak** mengetik angka `w` dan `b` satu per satu; komputerlah yang mencarinya otomatis saat proses *training* (akan kita lihat di Bab 3).",
        "• **Transisi:** \"Sekarang giliranmu mencoba langsung menggeser *Weight* dan *Bias* pada Simulator #1!\"",
    ],
    11: [
        "**Tujuan Slide (1.5 menit):** Memberi pengalaman langsung melihat perubahan `z`, `ReLU`, dan `Sigmoid` secara *real-time* memakai nilai RGB nyata dari `data/frozen_v1/`.",
        "• **Panduan Demo Simulator #1:** Klik bergantian tombol **Elsa**, **Anna**, dan **Olaf**. Tunjukkan bahwa dengan bobot bawaan (`w = [-1.5, +1.5, +2.5], b = -1.3`), **Elsa** menghasilkan `z = +0.36` (**AKTIF**, `ReLU = 0.36`), sedangkan **Anna** menghasilkan `z = -0.09` (**TIDAK AKTIF**, `ReLU = 0.00`)!",
        "• **Sorotan Visual:** Arahkan perhatian ke **4 batang kontribusi** di kanan (`x₁·w₁`, `x₂·w₂`, `x₃·w₃`, `Bias`): batang hijau mendorong ke kanan (+), batang merah menarik ke kiri (−). Coba geser slider `Bias` ke kanan/kiri untuk melihat dampaknya.",
        "• **Transisi:** \"Baru saja kita menggeser slider Bias. Memangnya kenapa kita wajib punya angka Bias? Mari kita lihat grafiknya.\"",
    ],
    12: [
        "**Tujuan Slide (1 menit):** Menjelaskan fungsi matematis **Bias (`b`)** secara visual tanpa rumus rumit.",
        "• **Naskah Pengajar:** Bandingkan grafik kiri (**Tanpa Bias**: garis merah terkunci di `(0, 0)`, hanya bisa diputar kemiringannya) dengan grafik kanan (**Dengan Bias**: garis hijau bisa naik-turun bebas sebesar `+b`, sama seperti konstanta `c` pada rumus garis `y = mx + c`).",
        "• **Kaitan ke Foto Proyek:** Foto polos yang terang dan foto di ruangan agak redup punya kecerahan dasar berbeda; **Bias** membantu neuron menyesuaikan ambang batas aktifnya.",
        "• **Transisi:** \"Itu baru 1 Neuron. Tentu 1 neuron tidak cukup untuk membedakan 5 karakter Frozen. Mari kita susun banyak neuron menjadi berlapis-lapis!\"",
    ],
    13: [
        "**Tujuan Slide (1 menit):** Memperkenalkan arsitektur **Multi-Layer Perceptron (MLP)**: `Input Layer`, `Hidden Layer`, dan `Output Layer`.",
        "• **Naskah Pengajar:** Tunjuk 4 kotak warna pada SVG: **Input Layer** (biru) menerima angka piksel, **Hidden Layer 1 & 2** (kuning & merah) terdiri dari puluhan neuron yang bekerja paralel mendeteksi warna/pola lalu menggabungkannya, dan **Output Layer** (hijau) memiliki tepat **5 neuron** untuk `Anna, Elsa, Kristoff, Olaf, Sven`.",
        "• **Poin Kunci:** Tunjuk callout hijau bawah — istilah **Deep Learning** berasal dari kata *deep* (dalam), yaitu memiliki banyak *Hidden Layer* yang bertumpuk.",
        "• **Transisi:** \"Mari kita ikuti perjalanan lengkap 1 foto Elsa dari ujung kiri sampai ujung kanan!\"",
    ],
    14: [
        "**Tujuan Slide (1.5 menit):** Merangkum seluruh Bab 1 dalam satu alur konkret bernama **Forward Pass** (4 tahap dari foto hingga prediksi `87.8%`).",
        "• **Naskah Pengajar:** Telusuri 4 kartu dari kiri ke kanan: **Tahap 1** angka piksel `0.0–1.0` masuk; **Tahap 2** 128 neuron *Hidden Layer* menghitung `w·x + b` + `ReLU`; **Tahap 3** keluar 5 skor mentah (**logits**) di *Output Layer*; **Tahap 4** `Softmax` mengubah 5 skor mentah menjadi probabilitas `87.8% Elsa`.",
        "• **Pengait ke Bab Berikutnya:** Tunjukkan bahwa di Tahap 2 ada `ReLU` dan di Tahap 4 ada `Softmax` — keduanya akan kita bedah tuntas di Bab 2.",
        "• **Transisi:** \"Sebelum pindah ke Bab 2, mari cek pemahaman Bab 1 lewat 2 pertanyaan cepat!\"",
    ],
    15: [
        "**Tujuan Slide (1 menit):** Melatih peserta menghitung sendiri `z = (x₁·w₁) + (x₂·w₂) + b` dengan desimal ringan (`0.8` dan `0.2`).",
        "• **Aktivitas Kelas:** Minta peserta menjawab lisan dulu sebelum mengklik tombol *Lihat Jawaban*: `0.8 × 2.0 = 1.6`, `0.2 × (-1.0) = -0.2`, ditambah `b = +0.5` → total `z = 1.9` (**Jawaban B**).",
        "• **Umpan Balik:** Setelah tombol diklik, tunjukkan panel kanan yang berubah dari petunjuk menjadi rincian hitungan lengkap. Beri apresiasi jika peserta benar!",
        "• **Transisi:** \"Satu pertanyaan singkat lagi tentang fungsi Bias.\"",
    ],
    16: [
        "**Tujuan Slide (1 menit):** Mengunci pemahaman tentang fungsi **Bias (`b`)** sebelum menutup Bab 1.",
        "• **Aktivitas Kelas:** Minta peserta memilih A, B, atau C lalu menjelaskan alasannya dengan 1 kalimat sendiri. Kunci: **Jawaban B** (menggeser ambang aktif neuron agar tidak terkunci di `(0, 0)`).",
        "• **Sorotan Visual:** Ingatkan persamaan garis sederhana `y = m·x + c` di panel kanan supaya konsep Bias selalu mudah diingat.",
        "• **Transisi:** \"Bab 1 selesai! Sekarang kita masuk Bab 2 untuk membongkar `ReLU` dan `Softmax`.\"",
    ],
    17: [
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 2: Fungsi Aktivasi (`ReLU`) & Probabilitas `Softmax`**.",
        "• **Naskah Pengajar:** \"Di Bab 1 kita sudah menyebut nama `ReLU` dan `Softmax`. Di Bab 2 ini kita bahas kenapa keduanya wajib ada di Neural Network dengan cara yang sangat sederhana.\"",
        "• **Transisi:** \"Kita mulai dari fungsi aktivasi paling populer di dunia: `ReLU`.\"",
    ],
    18: [
        "**Tujuan Slide (1 menit):** Menjelaskan fungsi aktivasi **ReLU** (`max(0, z)`) secara super sederhana beserta alasan matematis kenapa butuh *patahan di nol* (non-linearitas).",
        "• **Naskah Pengajar:** Bacakan aturan 1 kalimatnya: *\"Kalau negatif ubah jadi 0; kalau positif biarkan tetap.\"* Tunjukkan 3 contoh di tabel (`-8.0 → 0.0`, `-0.5 → 0.0`, `+2.0 → +2.0`).",
        "• **Penjelasan Non-Linearitas:** Jelaskan kartu kanan — tanpa `ReLU`, menumpuk 10 layer perkalian lurus tetap hanya menghasilkan 1 garis lurus. Patahan di titik `0` membuat gabungan neuron bisa membentuk batas melengkung.",
        "• **Transisi:** \"Supaya langsung kelihatan bedanya, mari kita lihat gambarnya di Slide 19.\"",
    ],
    19: [
        "**Tujuan Slide (1.5 menit):** Memberi bukti visual mengapa **non-linearitas** sangat krusial pada klasifikasi gambar.",
        "• **Naskah Pengajar:** Arahkan mata ke grafik kiri (1 garis lurus mustahil memisahkan titik biru Elsa di tengah yang dikelilingi titik lain) vs grafik kanan (dengan aktivasi `ReLU`, batas keputusan melengkung melingkari kelompok Elsa dengan bersih).",
        "• **Kaitan ke Foto Frozen:** Bacakan perbandingan aturan lurus vs non-linear di kanan — pada foto berlatar ramai, aturan sederhana \"makin banyak warna biru = Elsa\" akan gagal jika ada benda biru lain di rak.",
        "• **Transisi:** \"Selain `ReLU`, ada dua fungsi aktivasi klasik lain yang sering kamu temui. Mari kita bandingkan ketiganya.\"",
    ],
    20: [
        "**Tujuan Slide (1 menit):** Mengenalkan 3 fungsi aktivasi utama (**ReLU**, **Sigmoid**, **Tanh**) melalui bentuk kurva dan kegunaan praktisnya.",
        "• **Naskah Pengajar:** Tunjuk ketiga grafik di atas lalu tabel ringkasnya: `ReLU` (`0` s.d. `+∞`) adalah standar di *hidden layer*; `Sigmoid` (`0.0` s.d. `1.0`) dipakai untuk output 2 pilihan; `Tanh` (`-1` s.d. `+1`) simetris di nol.",
        "• **Poin Penenang Pemula:** Tekankan callout bawah — tidak perlu menghafal rumus eksponensial `e⁻ᶻ`, cukup ingat `ReLU` di tengah dan `Sigmoid/Softmax` di output.",
        "• **Transisi:** \"Mari kita coba menggeser sendiri skor `z` pada ketiga kurva ini di Simulator #2!\"",
    ],
    21: [
        "**Tujuan Slide (1.5 menit):** Mengamati perilaku `ReLU`, `Sigmoid`, dan `Tanh` secara interaktif pada berbagai nilai skor `z`.",
        "• **Panduan Demo Simulator #2:** Klik tab `1. ReLU`, geser slider `z` ke `-3.0` (hasil tepat `0.000`) lalu ke `+3.0` (hasil `3.000`). Pindah ke `2. Sigmoid` dan tunjukkan kurva huruf S yang selalu terjepit antara `0` dan `1`. Pindah ke `3. Tanh` dan tunjukkan skala `-1` sampai `+1` yang simetris di nol.",
        "• **Pertanyaan Pancingan:** *\"Lihat ujung kiri dan kanan kurva Sigmoid — datar atau curam?\"* (Datar! Itu jadi alasan mengapa ReLU dipilih di slide berikutnya.)",
        "• **Transisi:** \"Nah, apa saja 3 alasan utama kenapa `ReLU` hampir selalu dipilih di *Hidden Layer*?\"",
    ],
    22: [
        "**Tujuan Slide (1 menit):** Merangkum 3 keunggulan praktis `ReLU` dibanding `Sigmoid` di *hidden layer*.",
        "• **Naskah Pengajar:** Jelaskan 3 kolom singkat: (01) **Super Cepat** karena tanpa pangkat eksponensial; (02) **Sinyal Belajar Tidak Macet** (menghindari *vanishing gradient* yang terjadi di ujung datar Sigmoid); (03) **Neuron Fokus & Hemat** karena nilai negatif otomatis `0`.",
        "• **Jembatan ke Model Proyek:** Sebutkan bahwa **MobileNetV2** yang akan kita pakai di P04–P08 juga memakai varian ReLU bernama `ReLU6`.",
        "• **Transisi:** \"Itu untuk *Hidden Layer*. Sekarang bagaimana di ujung *Output Layer* agar keluar persentase 0–100%? Jawabannya: `Softmax`!\"",
    ],
    23: [
        "**Tujuan Slide (1 menit):** Menjelaskan fungsi **Softmax** sebagai pengubah skor mentah (*logits*) menjadi distribusi probabilitas `0–100%` yang totalnya tepat `100%`.",
        "• **Naskah Pengajar:** Urai 3 langkah di kiri tanpa intimidasi: (1) Ubah semua skor — termasuk yang negatif — jadi positif lewat `eᶻ`; (2) Jumlahkan seluruh nilai positifnya; (3) Bagi masing-masing dengan totalnya sehingga kelima kelas selalu berjumlah `1.0` (`100%`).",
        "• **Kaitan ke Kode Keras:** Tunjuk kotak hijau kanan bawah: cukup tulis `Dense(5, activation=\"softmax\")` di baris paling akhir model.",
        "• **Transisi:** \"Mari kita buktikan sendiri di Simulator #3 memakai 5 karakter Frozen kita!\"",
    ],
    24: [
        "**Tujuan Slide (1.5 menit):** Mendemonstrasikan cara kerja **Softmax** secara *live* termasuk pembuktian kolom `eᶻ` saat seluruh skor mentah bernilai negatif.",
        "• **Panduan Demo Simulator #3:** Klik 3 preset secara berurutan: `1. Yakin Elsa` (`84.9%`), `2. Ragu Elsa vs Anna` (`51.3%` vs `42.0%`), lalu **`3. Semua Skor Negatif`** (`Elsa = -0.8` tetap menjadi yang tertinggi `64.4%`!).",
        "• **Sorotan Visual:** Tunjuk kolom `eᶻ` dan badge `Total = 100.0%` di pojok kanan atas — meski semua *logits* negatif, `eᶻ` selalu positif sehingga probabilitas tidak pernah minus dan totalnya selalu tepat `100.0%`.",
        "• **Transisi:** \"Sekarang kapan kita pakai `Sigmoid` dan kapan pakai `Softmax` di *Output Layer*?\"",
    ],
    25: [
        "**Tujuan Slide (1 menit):** Memberikan aturan praktis kapan memakai `Sigmoid` (klasifikasi biner / 2 kelas) vs `Softmax` (multi-kelas / 3+ kelas).",
        "• **Naskah Pengajar:** Gunakan dua contoh langsung dari dataset peserta: menebak **Polos vs Ramai** (2 pilihan) cukup `Dense(1, \"sigmoid\")` + `binary_crossentropy`; sedangkan menebak **5 karakter Frozen** butuh `Dense(5, \"softmax\")` + `sparse_categorical_crossentropy`.",
        "• **Sorotan Visual:** Tunjuk baris kode Keras di bagian bawah kedua kartu — pasangan aktivasi dan *loss function* ini akan kita pakai terus sampai P08.",
        "• **Transisi:** \"Yuk cek pemahaman Bab 2 dengan 1 pertanyaan cepat!\"",
    ],
    26: [
        "**Tujuan Slide (1.5 menit):** Memastikan peserta paham perbedaan fungsi `ReLU` (*hidden layer*) vs `Softmax` (*output layer*).",
        "• **Aktivitas Kelas:** Minta peserta mengamati kotak kanan (`ReLU: Total 4.2` vs `Softmax: Total ???`) lalu memilih A, B, atau C. Kunci: **Jawaban B**.",
        "• **Penguatan:** Tegaskan bahwa `ReLU` mengeluarkan angka tak terbatas sehingga bukan probabilitas, sedangkan `Softmax` menormalkan 5 skor menjadi peluang `0–100%` berjumlah tepat `100%`.",
        "• **Transisi:** \"Hebat! Sekarang kita sudah tahu struktur jaringannya. Di Bab 3, kita bongkar pertanyaan terbesar: bagaimana bobot `w` dan `b` bisa belajar sendiri?\"",
    ],
    27: [
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 3: Proses Training Model**.",
        "• **Naskah Pengajar:** \"Di Bab 3 ini kita ikuti cerita 1 foto Elsa dari saat bobot model masih acak, lalu bagaimana **Loss**, **Gradient Descent**, dan **Backpropagation** memperbaikinya sedikit demi sedikit.\"",
        "• **Transisi:** \"Mari kita lihat apa yang terjadi pada detik pertama sebuah model baru dibuat.\"",
    ],
    28: [
        "**Tujuan Slide (1 menit):** Menjawab pertanyaan klasik pemula tentang dari mana nilai awal `weight` berasal (inisialisasi acak).",
        "• **Naskah Pengajar:** Tunjukkan 3 kolom dari kiri ke kanan: (1) Foto asli **Elsa** masuk; (2) Bobot `w₁, w₂, w₃` masih diisi angka acak oleh komputer; (3) Akibatnya prediksi awal keliru total (`Anna 45%, Elsa cuma 10%`).",
        "• **Pertanyaan Pancingan:** *\"Kalau model salah menebak seperti ini, hal pertama apa yang harus kita hitung dulu?\"* (Seberapa besar salahnya → **Loss**!)",
        "• **Transisi:** \"Mari kita ukur besar kesalahannya di Slide 29.\"",
    ],
    29: [
        "**Tujuan Slide (1.5 menit):** Memperkenalkan **Cross-Entropy Loss** sebagai ukuran seberapa salah prediksi model.",
        "• **Naskah Pengajar:** Baca grafik merah dari kanan ke kiri: kalau model yakin & benar (`92%` untuk Elsa), `Loss = 0.08` (sangat kecil); kalau ragu (`50%`), `Loss = 0.69`; kalau salah dengan percaya diri tinggi (memberi Elsa cuma `8%`), penalti `Loss` melonjak tajam ke `2.53`!",
        "• **Aturan Wajib Ingat:** **Makin kecil nilai Loss = makin akurat model.** Target ideal selama training adalah mendekati `0.0`.",
        "• **Transisi:** \"Setelah tahu nilai *Loss*-nya besar, bagaimana cara model mengubah bobot supaya *Loss* mengecil? Jawabannya: **Gradient Descent**.\"",
    ],
    30: [
        "**Tujuan Slide (1 menit):** Menjelaskan intuisi **Gradient Descent** tanpa kalkulus berat.",
        "• **Naskah Pengajar:** Tunjuk kurva U di kiri (dari titik merah *Loss tinggi* menuju titik hijau *Titik Minimum Loss ≈ 0*). Gunakan penjelasan sederhana seperti menyetel keran air hangat/dingin sedikit demi sedikit sampai pas.",
        "• **Bedah 1 Rumus di Kanan:** Jelaskan arti 3 bagian pada `w_baru = w_lama − (Learning Rate × Gradien)`: **Gradien** = arah kemiringan kurva, tanda **minus (`−`)** = melangkah ke arah turun, dan **Learning Rate** = besar langkahnya. Di Keras kita memakai optimizer **`Adam`**.",
        "• **Transisi:** \"Seberapa besar sebaiknya kita memasang **Learning Rate**? Mari kita bandingkan 3 skenario di Slide 31.\"",
    ],
    31: [
        "**Tujuan Slide (1 menit):** Menunjukkan efek **Learning Rate** yang terlalu kecil, ideal, dan terlalu besar lewat 3 ilustrasi mini kurva Loss.",
        "• **Naskah Pengajar:** Bandingkan kiri ke kanan: **Kekecilan (`0.00001`)** membuat training sangat lambat; **Ideal (`0.001`)** turun mulus ke dasar; **Kebesaran (`0.5–1.0`)** membuat bobot melompat melewati dasar hingga *Loss* malah naik atau menjadi `NaN`.",
        "• **Patokan Proyek:** Catat patokan emas untuk notebook nanti: mulai dari `Adam(learning_rate=0.001)`, lalu kecilkan jadi `1e-5` saat *fine-tuning* MobileNetV2 di P07.",
        "• **Transisi:** \"Yuk kita lihat langsung pergerakan titik bobotnya pada Simulator #4!\"",
    ],
    32: [
        "**Tujuan Slide (1.5 menit):** Mendemonstrasikan efek `Learning Rate` secara langsung dari titik awal yang sama (`w = -2.8`, `Loss = 7.84`).",
        "• **Panduan Demo Simulator #4:** Klik `1. LR Kecil (0.03)` → setelah 8 langkah baru sampai `w = -1.71` (`Loss = 2.913`, lambat!). Klik `2. LR Ideal (0.20)` → meluncur mulus ke `w = -0.05` (`Loss = 0.002`!). Klik `3. LR Besar (1.06)` → memantul bolak-balik makin jauh ke `w = -6.93` (`Loss = 48.062`, divergen!).",
        "• **Sorotan Visual:** Tunjuk label `Mulai (t=0)` dan `Akhir (t=8)` di kanvas agar peserta melihat perbandingan 8 langkah yang adil.",
        "• **Transisi:** \"Tadi itu baru 1 bobot `w`. Kalau ada ribuan bobot di banyak layer, bagaimana cara tahu bobot mana yang paling banyak salah? Itulah tugas **Backpropagation**.\"",
    ],
    33: [
        "**Tujuan Slide (1.5 menit):** Menjelaskan konsep **Backpropagation** secara visual lewat diagram 2 arah (Maju Biru → Mundur Merah) tanpa rumus turunan.",
        "• **Naskah Pengajar:** Ikuti panah biru di atas: foto **Olaf** masuk → lewat `w₁` dan `w₂` → salah ditebak `70% Elsa` → **Loss tinggi!** Lalu ikuti panah merah putus-putus di bawah: dari nilai *Loss*, sistem menghitung mundur seberapa besar kontribusi kesalahan `w₂` dan `w₁` agar bobot yang paling berkontribusi dikoreksi paling besar.",
        "• **Poin Penenang Pemula:** Tunjuk kotak hijau bawah — kamu tidak pernah perlu menghitung turunan manual; 1 baris `model.fit()` di TensorFlow/Keras menghitungnya otomatis.",
        "• **Transisi:** \"Sekarang mari kita gabungkan keempat langkah tadi menjadi 1 siklus utuh `model.fit()`.\"",
    ],
    34: [
        "**Tujuan Slide (1 menit):** Merangkum keseluruhan siklus training (4 langkah) dan memperlihatkan progres nyata prediksi foto Elsa lintas epoch.",
        "• **Naskah Pengajar:** Bacakan 4 kartu atas: `01 Forward Pass → 02 Hitung Loss → 03 Backpropagation → 04 Update Bobot (Adam)`. Lalu tunjukkan 3 progress bar di bawah: dari **Epoch 1** (`12% Elsa, Loss 2.12`), naik di **Epoch 5** (`68%, Loss 0.39`), hingga mantap di **Epoch 15** (`93%, Loss 0.07`).",
        "• **Poin Kunci:** Seluruh siklus ini berulang otomatis ratusan kali saat kita memanggil `model.fit()`.",
        "• **Transisi:** \"Tadi saya menyebut kata *Epoch*. Apa bedanya **Batch Size** dan **Epoch**? Mari kita lihat Slide 35.\"",
    ],
    35: [
        "**Tujuan Slide (1 menit):** Membedakan dua parameter wajib di `model.fit()`: **Batch Size** dan **Epoch**.",
        "• **Naskah Pengajar:** Jelaskan dengan sederhana: **Batch Size** (mis. `16` foto) adalah jumlah foto yang diproses dalam 1 paket sebelum bobot di-update 1 kali (agar memori GPU tidak penuh). **Epoch** adalah 1 putaran penuh ketika model sudah melihat seluruh data latih.",
        "• **Contoh Hitung Cepat:** Tunjuk kotak bawah kiri — jika ada `128` foto latih dengan `batch_size=16`, berarti ada `8` kali pembaruan bobot dalam `1` epoch.",
        "• **Transisi:** \"Hati-hati: mengulang terlalu banyak epoch tanpa rem bisa memicu masalah klasik bernama **Overfitting**.\"",
    ],
    36: [
        "**Tujuan Slide (1 menit):** Mengenalkan 3 kondisi hasil training: **Underfitting**, **Good Fit**, dan **Overfitting**.",
        "• **Naskah Pengajar:** Tunjukkan 3 mini-grafik kurva biru (*Train Loss*) vs merah (*Validation Loss*): pada **Underfitting** keduanya tinggi; pada **Good Fit** keduanya turun rapat bersama; pada **Overfitting** garis biru turun ke 0 tetapi garis merah justru naik lagi karena model menghafal latar/foto latih.",
        "• **Kaitan ke Dataset Frozen:** Karena dataset `v1` kita berisi `143` foto, memantau grafik *Train vs Val Loss* sangat wajib di setiap eksperimen.",
        "• **Transisi:** \"Mari kita latih mata membaca 3 pola kurva tersebut pada Simulator #5!\"",
    ],
    37: [
        "**Tujuan Slide (1 menit):** Melatih peserta mendiagnosis kurva *Train Loss vs Val Loss* secara cepat menggunakan 3 angka KPI (*Train Loss, Val Loss, Gap*).",
        "• **Panduan Demo Simulator #5:** Klik `1. Underfitting` (keduanya tinggi > `1.37`), `2. Good Fit` (turun rapat `0.19` vs `0.28`, gap tipis `+0.09`), dan `3. Overfitting` (mulai Epoch 5 garis berpisah tajam, gap melonjak `+1.50`!).",
        "• **Jembatan ke P06–P07:** Sebutkan singkat solusi overfitting yang akan kita praktikkan nanti: *Data Augmentation, Dropout, EarlyStopping,* dan *Transfer Learning*.",
        "• **Transisi:** \"Sebelum lanjut ke Bab 4, mari cek pemahaman Bab 3 lewat 1 pertanyaan cepat.\"",
    ],
    38: [
        "**Tujuan Slide (1 menit):** Mengecek pemahaman peserta tentang efek **Learning Rate** terlalu besar (`0.5`).",
        "• **Aktivitas Kelas:** Minta peserta menjawab lisan dulu sebelum mengklik *Lihat Jawaban*. Kunci: **Jawaban B** (bobot melompat melewati titik minimum sehingga Loss naik-turun liar atau meningkat).",
        "• **Penguatan:** Ingatkan solusi tercepat di kode Keras jika grafik Loss berantakan: kecilkan `learning_rate` (mis. ke `0.001`).",
        "• **Transisi:** \"Sekarang kita masuk ke Bab 4 — bagian penting yang menjawab mengapa foto Frozen butuh CNN di P03!\"",
    ],
    39: [
        "**Tujuan Slide (0.5 menit):** Pembatas masuk ke **Bab 4: Batasan MLP pada Foto & Jembatan Menuju CNN (P03)**.",
        "• **Naskah Pengajar:** \"Kalau ANN/MLP sudah bisa belajar sendiri, kenapa kita masih perlu mempelajari CNN di pertemuan berikutnya? Bab 4 akan menjawabnya dengan bukti nyata pada foto Elsa kita.\"",
        "• **Transisi:** \"Mari kita lihat apa yang dilakukan operasi `Flatten` pada foto Elsa.\"",
    ],
    40: [
        "**Tujuan Slide (1.5 menit):** Menunjukkan dampak nyata operasi **Flatten** pada foto 2D Elsa (`224×224×3`).",
        "• **Naskah Pengajar:** Arahkan perhatian ke 3 panel gambar: (1) Foto Elsa 2D utuh dipecah baris demi baris; (2) Disambung memanjang menjadi 1 vektor 1D (`150.528` angka) sehingga piksel tetangga atas-bawah terputus; (3) Jumlah bobot di Layer 1 saja meledak ke `19,27 juta`!",
        "• **Poin Kunci:** Layer `Dense` biasa tidak mengerti bahwa piksel di baris atas dan baris bawah saling berdekatan membentuk wajah atau gaun Elsa.",
        "• **Transisi:** \"Mari kita hitung sendiri ledakan bobotnya pada Simulator #6!\"",
    ],
    41: [
        "**Tujuan Slide (1.5 menit):** Membandingkan secara interaktif jumlah parameter Layer 1 MLP antara MNIST (`28×28`), Frozen kecil (`64×64×3`), dan Frozen standar (`224×224×3`).",
        "• **Panduan Demo Simulator #6:** Klik `MNIST 28×28` (`100.352` bobot), lalu `Frozen 64×64×3` (`1,57 juta` bobot — `16×` MNIST), lalu `Frozen 224×224×3` (`19,27 juta` bobot — **`192×` MNIST**!). Coba geser slider jumlah neuron hidden untuk menunjukkan skalanya.",
        "• **Pertanyaan Pancingan:** *\"Kita baru punya 143 foto Frozen, tapi 1 layer MLP saja sudah punya 19,2 juta bobot. Kira-kira model akan belajar pola atau menghafal foto?\"* (Menghafal / Overfitting!)",
        "• **Transisi:** \"Mari lihat bukti nyatanya pada foto Elsa Polos vs Ramai di Slide 42.\"",
    ],
    42: [
        "**Tujuan Slide (1 menit):** Menghubungkan kelemahan teknis MLP (*Flatten* & ledakan parameter) langsung ke tantangan dataset proyek peserta (**Polos vs Ramai**).",
        "• **Naskah Pengajar:** Tunjuk 2 foto Elsa di kiri: di foto **Ramai**, posisi Elsa bergeser sedikit dan dikelilingi benda di rak. Karena MLP menghafal nomor indeks piksel tertentu, pergeseran kecil langsung mengacaukan prediksinya. Sementara di kanan, rasio `19,2 juta bobot vs 143 foto` memicu overfitting ke latar belakang.",
        "• **Jembatan ke P03:** Tegaskan bahwa solusi di P03 (**CNN**) membaca gambar tetap dalam bentuk 2D utuh dengan filter kecil `3×3` yang jauh lebih hemat parameter.",
        "• **Transisi:** \"Cek pemahaman cepat sebelum melihat gambar besar arsitektur model akhir kita.\"",
    ],
    43: [
        "**Tujuan Slide (1 menit):** Memastikan peserta bisa menyebutkan 2 alasan utama mengapa MLP tidak cukup untuk klasifikasi foto beresolusi besar.",
        "• **Aktivitas Kelas:** Minta peserta menjawab lisan lalu klik *Lihat Jawaban*. Kunci: **Jawaban B** (struktur 2D gambar rusak akibat `Flatten` dan jumlah bobot meledak jutaan sehingga rawan *overfitting*).",
        "• **Transisi:** \"Apakah artinya materi ANN hari ini tidak terpakai saat nanti pakai CNN? Justru sebaliknya! Lihat Slide 44.\"",
    ],
    44: [
        "**Tujuan Slide (1 menit):** Menunjukkan posisi materi P01, P02, dan P03–P04 dalam arsitektur akhir proyek **Disney Frozen**.",
        "• **Naskah Pengajar:** Tunjukkan diagram alur bawah: **Input Foto (P01)** → **CNN Backbone / MobileNetV2 (P03–P04)** untuk mengekstrak ciri 2D → **Classification Head ANN (P02: `Dense + Softmax(5) + Loss + Adam`)** untuk mengambil keputusan 5 karakter Frozen!",
        "• **Penguatan Motivasi:** Beri tahu peserta bahwa dengan menguasai P01 dan P02, dua dari tiga blok utama model final sudah ada di tangannya.",
        "• **Transisi:** \"Teori selesai! Sekarang waktunya istirahat 5 menit sebelum kita praktik santai di notebook.\"",
    ],
    45: [
        "**Tujuan Slide (5 menit):** Memberi jeda istirahat penuh 5 menit sebelum masuk ke sesi praktik kode.",
        "• **Naskah Pengajar:** Persilakan peserta minum air, meregangkan mata/tangan, dan menyiapkan browser untuk membuka `P02_neural_network_ann.ipynb` di Google Colab (atau Jupyter lokal) setelah 5 menit.",
        "• **Catatan Instruktur:** Gunakan 1 menit terakhir jeda untuk memastikan file `P02_neural_network_ann.ipynb` dan folder `data/frozen_v1/` sudah siap diakses peserta.",
    ],
    46: [
        "**Tujuan Slide (44 menit — Panduan Praktik):** Menjadi peta utama selama peserta mengerjakan 6 langkah hands-on di `P02_neural_network_ann.ipynb`.",
        "• **Alur Pendampingan:** Pandu sel demi sel (setiap sel hanya 5–15 baris): **Setup 3 tahap** → **Langkah 1** (1 Neuron + ReLU/Sigmoid di NumPy pada RGB foto Elsa & Olaf) → **Langkah 2** (`softmax_manual` vs `tf.nn.softmax`) → **Langkah 3** (MLP pertama di Keras pada data 28×28) → **Langkah 4** (uji `LR=0.001` vs `0.1` & `ReLU` vs `Sigmoid`, simpan grafik) → **Langkah 5** (muat `143` foto `data/frozen_v1/`, cek ledakan parameter `64×64` vs `224×224`) → **Langkah 6** (verifikasi Mini-Challenge).",
        "• **Tips Mengajar Pemula:** Jangan langsung memberi jawaban `# TODO`; minta peserta baca komentar Bahasa Indonesia dulu, lalu boleh buka dropdown `<details>` Hint jika mentok > 2 menit.",
        "• **Transisi:** \"Setelah kode jalan, mari kita bedah singkat 2 bagian kode terpenting di Slide 47–48.\"",
    ],
    47: [
        "**Tujuan Slide (1 menit):** Mereview kode NumPy paling inti dari Langkah 1 & 2 agar peserta melihat betapa ringkasnya implementasi 1 Neuron dan Softmax.",
        "• **Naskah Pengajar:** Tunjuk blok kiri (`np.dot(x_elsa, w) + b` dan `np.maximum(0.0, z)`) — cukup 2 baris Python! Tunjuk blok kanan (`softmax_manual`) dan jelaskan alasan praktis mengurangi `np.max(logits)` agar angka eksponensial tidak *overflow*.",
        "• **Sorotan Visual:** Tunjukkan output verifikasi bahwa selisih hitungan manual kita dan `tf.nn.softmax` adalah `0.000000`.",
        "• **Transisi:** \"Sekarang mari kita lihat 4 baris arsitektur MLP di Keras.\"",
    ],
    48: [
        "**Tujuan Slide (1 menit):** Menghubungkan setiap baris kode `tf.keras.Sequential` dan `model.compile` langsung ke teori Bab 1–4.",
        "• **Naskah Pengajar:** Baca daftar kanan baris demi baris: `Flatten()` = Bab 4; `Dense(128, \"relu\")` = Bab 1 & 2; `Dense(5, \"softmax\")` = Bab 2; `sparse_categorical_crossentropy` = Bab 3 (Loss); `Adam(0.001)` = Bab 3 (Gradient Descent).",
        "• **Pengait P03:** Tunjuk kotak hijau kanan bawah — di P03 kita hanya mengganti `Flatten()` di depan dengan `Conv2D + MaxPooling2D`!",
        "• **Transisi:** \"Sekarang waktunya Mini-Challenge 12 menit tanpa kalkulator!\"",
    ],
    49: [
        "**Tujuan Slide (12 menit):** Menjalankan *Mini-Challenge Softmax* sesuai `docs/PLAN.md` untuk mengasah intuisi probabilitas tanpa kalkulator.",
        "• **Aktivitas Diskusi (8 menit):** Tunjukkan skor `[Elsa = 2.0, Anna = 1.0, Olaf = 0.0]`. Minta peserta memperkirakan: (1) Siapa terbesar dan apakah > 50%?; (2) Kenapa total selalu `1.0`?; (3) Apa jadinya jika semua skor ditambah `+10` jadi `[12, 11, 10]`?",
        "• **Pembahasan & Verifikasi (4 menit):** Klik *Lihat Kunci Diskusi* (`Elsa 66.5%, Anna 24.5%, Olaf 9.0%`, dan ditambah `+10` **tidak berubah** karena Softmax hanya bergantung pada selisih antar-skor!), lalu cocokkan bersama hasil Langkah 6 di Notebook.",
        "• **Transisi:** \"Sebelum kuis akhir, mari kita ulang cepat 12 istilah asli yang sudah kamu kuasai hari ini.\"",
    ],
    50: [
        "**Tujuan Slide (1 menit):** Mengulas 6 istilah inti Bab 1 & Bab 2 dalam 1 tabel referensi cepat.",
        "• **Naskah Pengajar:** Pindai cepat 6 baris (*Neuron, Weight & Bias, Dense/Hidden Layer, Forward Pass, Activation Function, ReLU & Sigmoid*). Tanyakan apakah ada 1 istilah yang masih terasa samar agar bisa langsung diklarifikasi.",
        "• **Transisi:** \"Lanjut ke 6 istilah Bagian 2 (Bab 3 & Bab 4).\"",
    ],
    51: [
        "**Tujuan Slide (1 menit):** Mengulas 6 istilah inti Bab 3 & Bab 4 (*Logits & Softmax, Loss, Gradient Descent & LR, Backpropagation, Batch & Epoch, Overfitting & Flatten*).",
        "• **Naskah Pengajar:** Tunjuk strip ringkasan merah di bawah (`Forward Pass → Hitung Loss → Backpropagation → Update Bobot (Adam)`) — satu baris ini adalah jantung seluruh proses *training* Deep Learning.",
        "• **Transisi:** \"Siap untuk kuis santai 5 soal?\"",
    ],
    52: [
        "**Tujuan Slide (1.5 menit):** Kuis interaktif Soal 1 (`Bias`) dan Soal 2 (`Learning Rate` terlalu besar).",
        "• **Aktivitas Kelas:** Minta peserta menjawab dengan bahasanya sendiri dulu sebelum mengklik tombol *Lihat Jawaban* satu per satu.",
        "• **Kunci Singkat:** (1) Menggeser ambang aktif neuron agar tidak terkunci di `(0, 0)`; (2) Bobot melompat melewati titik minimum sehingga Loss naik-turun liar / tidak konvergen / `NaN`.",
        "• **Transisi:** \"Lanjut ke Soal 3 dan 4!\"",
    ],
    53: [
        "**Tujuan Slide (1.5 menit):** Kuis interaktif Soal 3 (`ReLU` vs `Softmax`) dan Soal 4 (gejala `Overfitting`).",
        "• **Aktivitas Kelas:** Biarkan peserta menjawab lisan terlebih dulu. Kunci: (3) `ReLU` cepat & non-linear di *hidden layer*, `Softmax` menghasilkan probabilitas `0–100%` berjumlah `100%` di *output layer*; (4) **Overfitting** (menghafal data latih/latar).",
        "• **Transisi:** \"Satu soal terakhir sekaligus cek kesiapan masuk ke P03!\"",
    ],
    54: [
        "**Tujuan Slide (1 menit):** Kuis Soal 5 (alasan MLP tidak cukup untuk foto `224×224×3`) + *Self-Check* 3 kriteria berhasil sesuai `docs/PLAN.md`.",
        "• **Aktivitas Kelas:** Minta peserta menjawab Soal 5 (dua alasan: `Flatten` merusak struktur 2D & bobot meledak >19 juta), lalu centang bersama 3 poin checklist hijau di sisi kanan.",
        "• **Transisi:** \"Mari kita kunci sesi hari ini dengan 3 poin utama.\"",
    ],
    55: [
        "**Tujuan Slide (1 menit):** Merangkum keseluruhan P02 menjadi 3 pilar padat yang mudah diingat setelah kelas usai.",
        "• **Naskah Pengajar:** Bacakan tegas 3 kartu: (01) **Neuron, ReLU, & Softmax** adalah fondasi arsitektur; (02) **Training** adalah siklus memperbaiki bobot lewat *Loss, Backpropagation,* dan *Gradient Descent*; (03) **Batasan MLP** menjadi jembatan logis menuju **CNN (P03)**.",
        "• **Transisi:** \"Berikut tugas ringan mandiri dan bocoran seru pertemuan berikutnya.\"",
    ],
    56: [
        "**Tujuan Slide (1 menit):** Menyampaikan tugas mandiri ringan (maks. 1 halaman ringkasan dengan bahasa sendiri + 1 grafik perbandingan Learning Rate dari Notebook) serta preview **P03 (CNN Fundamentals)**.",
        "• **Naskah Pengajar:** Tekankan bahwa tugas bukan hafalan definisi, melainkan latihan merangkum alur *Neuron → Softmax → Training* dengan bahasa sendiri. Berikan antusiasme untuk P03 di mana kita langsung melihat *Feature Map* dari foto Frozen milik peserta.",
        "• **Transisi:** \"Terima kasih atas kerja kerasnya hari ini — satu kalimat penutup untukmu.\"",
    ],
    57: [
        "**Tujuan Slide (1 menit):** Menutup kelas dengan apresiasi hangat dan kutipan penutup P02.",
        "• **Naskah Pengajar:** Bacakan kutipan penutup dengan tenang, beri apresiasi spesifik atas pencapaian peserta selama praktik notebook & mini-challenge, lalu tanyakan jika ada pertanyaan penutup.",
        "• **Catatan Referensi:** Informasikan bahwa 2 slide terakhir (Slide 58–59) berisi tautan video 3Blue1Brown & TensorFlow Playground untuk belajar mandiri di rumah.",
    ],
    58: [
        "**Tujuan Slide (0 menit — Referensi Mandiri 1/2, Langkah 1–8):** Menyediakan 8 tautan video YouTube & sandbox interaktif klik-langsung setara standar P01, dibagi dalam 3 tahap: **Tahap 1** (*3Blue1Brown Ch. 1, StatQuest NN Pt. 1, & Versi Tulis*), **Tahap 2** (*StatQuest ReLU in Action & TensorFlow Playground*), dan **Tahap 3** (*StatQuest SoftMax, Cross-Entropy, & 3Blue1Brown Gradient Descent Ch. 2*).",
        "• **Catatan Penggunaan:** Tidak perlu dibahas panjang di kelas; arahkan peserta mengklik kartu berlabel *Wajib* terlebih dulu pada versi HTML/PDF untuk memperdalam intuisi visual di rumah.",
    ],
    59: [
        "**Tujuan Slide (0 menit — Referensi Mandiri 2/2, Langkah 9–16):** Menyediakan 8 tautan lanjutan klik-langsung untuk **Tahap 4** (*StatQuest Gradient Descent, 3Blue1Brown Backprop Ch. 3–4, & StatQuest Backprop Details*) dan **Tahap 5** (*TensorFlow Fashion-MNIST Official Tutorial, Keras Sequential Guide, Stanford CS231n, & Coursera DL Course 1*), lengkap dengan **Rute Maraton ±2 Jam** yang langsung menuju preview **P03 (CNN Week 1)**.",
        "• **Catatan Penggunaan:** Tekankan bahwa item berlabel *Opsional* tidak wajib sebelum P03 — cukup ikuti 5 langkah cepat di *Rute Maraton* bawah.",
    ],
}
