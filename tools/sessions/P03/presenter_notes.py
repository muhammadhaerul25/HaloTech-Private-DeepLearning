"""Naskah Penjelasan Detail per Slide (1..52) untuk P03: Arsitektur Neural Network.

Dipakai oleh:
1. `tools/core/exporter.py` -> Speaker Notes PPTX (100% slide)
2. `tools/core/exporter.py` -> `materials/P03/P03_presenter_script.pdf` (A4 1 slide/halaman)

Mengikuti standar P02 (dinamis dari `p03_data.json` dengan struktur 3 bagian per slide):
- Tujuan Slide + Alokasi Waktu
- Panduan Demo Interaktif / Naskah Pengajar (kata-kata lisan non-IT + aksi tombol spesifik)
- Transisi ke Slide Berikutnya
"""

from __future__ import annotations

import json
from pathlib import Path

_ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
_P03_DATA_PATH = _ROOT_DIR / "materials" / "P03" / "assets" / "P03" / "p03_data.json"


def _load_p03_stats() -> dict:
    fallback = {
        "total_images": 143,
        "polos": 102,
        "ramai": 41,
        "p02_params": 752_645,
        "mlp_params": 9_636_101,
        "mlp_mb": 36.76,
        "mlp_ms": 62.3,
        "cnn_params": 101_829,
        "cnn_mb": 0.39,
        "cnn_ms": 244.8,
        "res_params": 23_597_957,
        "res_mb": 90.02,
        "res_ms": 1615.8,
        "res_layers": 175,
        "res_skip": 16,
        "mob_params": 2_264_389,
        "mob_mb": 8.64,
        "mob_ms": 773.5,
        "mob_layers": 154,
        "mob_dw": 17,
        "eff_params": 4_055_976,
        "eff_mb": 15.47,
        "eff_ms": 2238.9,
        "eff_layers": 237,
        "eff_se": 16,
        "mlp_val": 11.4,
        "cnn_val": 34.3,
        "cnn_shift": 34.3,
    }
    if not _P03_DATA_PATH.exists():
        return fallback
    try:
        d = json.loads(_P03_DATA_PATH.read_text(encoding="utf-8"))
        bm = {r["architecture"]: r for r in d.get("benchmarks", [])}
        m_mlp = bm.get("1. MLP (2 Hidden)", {})
        m_cnn = bm.get("2. CNN Klasik", {})
        m_res = bm.get("3. ResNet50", {})
        m_mob = bm.get("4. MobileNetV2", {})
        m_eff = bm.get("5. EfficientNetB0", {})
        sh = d.get("shift_test_64", {})
        cond = d.get("condition_counts", {})
        return {
            "total_images": int(d.get("total_images", fallback["total_images"])),
            "polos": int(cond.get("polos", fallback["polos"])),
            "ramai": int(cond.get("ramai", fallback["ramai"])),
            "p02_params": int(d.get("p02_1layer_params", fallback["p02_params"])),
            "mlp_params": int(m_mlp.get("total_params", fallback["mlp_params"])),
            "mlp_mb": float(m_mlp.get("est_size_mb", fallback["mlp_mb"])),
            "mlp_ms": float(m_mlp.get("latency_ms_8imgs", fallback["mlp_ms"])),
            "cnn_params": int(m_cnn.get("total_params", fallback["cnn_params"])),
            "cnn_mb": float(m_cnn.get("est_size_mb", fallback["cnn_mb"])),
            "cnn_ms": float(m_cnn.get("latency_ms_8imgs", fallback["cnn_ms"])),
            "res_params": int(m_res.get("total_params", fallback["res_params"])),
            "res_mb": float(m_res.get("est_size_mb", fallback["res_mb"])),
            "res_ms": float(m_res.get("latency_ms_8imgs", fallback["res_ms"])),
            "res_layers": int(m_res.get("layers_backbone", fallback["res_layers"])),
            "res_skip": int(m_res.get("skip_add_layers", fallback["res_skip"])),
            "mob_params": int(m_mob.get("total_params", fallback["mob_params"])),
            "mob_mb": float(m_mob.get("est_size_mb", fallback["mob_mb"])),
            "mob_ms": float(m_mob.get("latency_ms_8imgs", fallback["mob_ms"])),
            "mob_layers": int(m_mob.get("layers_backbone", fallback["mob_layers"])),
            "mob_dw": int(m_mob.get("depthwise_layers", fallback["mob_dw"])),
            "eff_params": int(m_eff.get("total_params", fallback["eff_params"])),
            "eff_mb": float(m_eff.get("est_size_mb", fallback["eff_mb"])),
            "eff_ms": float(m_eff.get("latency_ms_8imgs", fallback["eff_ms"])),
            "eff_layers": int(m_eff.get("layers_backbone", fallback["eff_layers"])),
            "eff_se": int(m_eff.get("se_multiply_layers", fallback["eff_se"])),
            "mlp_val": float(sh.get("mlp_val_acc", fallback["mlp_val"])),
            "cnn_val": float(sh.get("cnn_val_acc", fallback["cnn_val"])),
            "cnn_shift": float(sh.get("cnn_shift6px_acc", fallback["cnn_shift"])),
        }
    except Exception:
        return fallback


_S = _load_p03_stats()

SLIDE_EXPLANATIONS: dict[int, list[str]] = {
    1: [
        f"**Tujuan Slide (1 menit — Cover P03):** Membuka sesi **P03 — Arsitektur Neural Network** dan langsung menempatkan **{_S['total_images']} foto Disney Frozen** di kartu bento kanan sebagai tolok ukur tetap lintas 5 generasi arsitektur.",
        "**Naskah Pengajar:** *\"Di P02 kita sudah melihat satu piksel menjadi 150.528 angka dan dilatih dengan model 1-layer. Hari ini di P03, kita membedah cetak biru arsitekturnya: dari MLP hingga MobileNetV2 dan EfficientNet.\"*",
        "**Transisi ke Slide 2:** Mari lihat jadwal 120 menit dan 3 target belajar yang akan kita capai.",
    ],
    2: [
        "**Tujuan Slide (1 menit — Agenda & Target Belajar):** Memberi peserta peta waktu 120 menit dan pola bedah yang selalu konsisten (`In General -> Fitur Khusus -> Simulasi Full -> Use Case`).",
        "**Panduan Demo / Penjelasan:** Tekankan bahwa paruh pertama (~52 menit) membahas evolusi 5 arsitektur dengan **5 simulator interaktif**, lalu istirahat 5 menit, dan paruh kedua (~48 menit) praktik langsung di notebook Keras yang ringan (*offline-safe* `weights=None`).",
        "**Transisi ke Slide 3:** Sebelum masuk arsitektur baru, mari ingat kembali batas nyata model 1-layer dari akhir sesi P02.",
    ],
    3: [
        f"**Tujuan Slide (2 menit — Pemanasan Sederhana dari P02):** Menjelaskan dengan contoh foto langsung mengapa model 1-layer dari P02 (`{_S['p02_params']:,}` kabel bobot) masih belum cukup untuk menebak `{_S['total_images']}` foto Frozen secara tangguh.",
        f"**Naskah Pengajar:** *\"Ingat model 1 lapis di P02 kemarin? Cara kerjanya meluruskan semua piksel menjadi 1 baris panjang. Akibatnya ada 3 kendala sederhana: (1) begitu posisi Elsa digeser sedikit saja di foto kiri, kabel bobotnya bingung; (2) ada `{_S['ramai']}` foto berlatar rak ramai di kanan yang warnanya bisa mengecoh; dan (3) kalau kita langsung menambah lapisan biasa, jumlah kabelnya meledak jadi ~9,6 juta!\"*",
        "**Transisi ke Slide 4:** Lalu, arsitektur AI apa saja yang diciptakan manusia langkah demi langkah untuk memecahkan tiga masalah itu? Ini dia petanya.",
    ],
    4: [
        "**Tujuan Slide (2 menit — Peta Evolusi 5 Arsitektur):** Menanamkan mental model bahwa setiap arsitektur baru lahir karena **cacat konkret** pada pendahulunya (`Obat -> Cacat Baru`), bukan muncul mendadak.",
        "**Naskah Pengajar:** Arahkan perhatian dari kiri ke kanan: `1. MLP` menambal model 1-layer P02 tapi meledak ke `9.64M` param → `2. CNN Klasik` membawa filter geser `3×3` tapi macet saat dalam → `3. ResNet` membawa `Skip +x` dan `GAP` tapi `90 MB` → `4. MobileNetV2` (`8.64 MB`, ★ Proyek Frozen) → `5. EfficientNet` menambah `Compound Scaling` + `SE Attention`.",
        "**Transisi ke Slide 5:** Mari kita buka bab pertama dengan menguji generasi paling awal: **MLP**.",
    ],
    5: [
        "**Tujuan Slide (1 menit — Pembuka Bab 1: MLP):** Mengajak peserta fokus membedah arsitektur klasik **Multi-Layer Perceptron** secara utuh dalam 4 slide ke depan.",
        "**Naskah Pengajar:** *\"Kita sudah tahu 1-layer P02 terlalu polos. Langkah pertama manusia waktu itu sederhana: bagaimana kalau di tengah-tengahnya kita tambah 1 atau 2 lapisan tersembunyi (*Hidden Layer*)?\"*",
        "**Transisi ke Slide 6:** Seperti ini bentuk lengkap aliran angka di dalam arsitektur MLP.",
    ],
    6: [
        "**Tujuan Slide (1.5 menit — #1.1 Aliran Rinci Neuron-per-Neuron MLP):** Memastikan peserta benar-benar paham cara tiap **1 neuron** (`Input x₁..xₙ` → `Hidden h₁..h₆₄` → `Hidden k₁..k₃₂` → `Output Anna..Sven`) terhubung penuh (*Dense*) dan meneruskan angka ke seluruh neuron di depannya.",
        "**Panduan Demo Interaktif:** Klik salah satu neuron langsung di diagram (misal **`x₁`** atau **`h₁`**) untuk menyorot kabel milik neuron tersebut saja, atau klik **`⏭ +1 Neuron`** & **`▶ Play Neuron`** untuk menyaksikan bola sinyal `60fps` meluncur neuron demi neuron dari `x₁` → `h₁..h₆₄` → `k₁..k₃₂` → `Elsa 82% ✓`! Gunakan tombol **`0 Hidden (P02)`** untuk membandingkan model lama.",
        "**Transisi ke Slide 7:** Setelah melihat betapa rapatnya kabel antar-neuron ini, mari lihat kekuatan sekaligus kelemahan fatal MLP pada gambar.",
    ],
    7: [
        "**Tujuan Slide (1.5 menit — #1.2 MLP Fitur Khusus & Kelemahan Foto):** Menyebutkan 2 kekuatan MLP (*Non-linear Hidden Representation*, kombinasi fitur global) sekaligus 2 cacat fatalnya di gambar: **Spatial Blindness** dan **Parameter Explosion (`9.636.101` bobot)**.",
        f"**Naskah Pengajar:** Jelaskan analogi *\"menghafal nomor kursi\"*: pada foto `{_S['polos']}` polos dan `{_S['ramai']}` ramai, menggeser figurin Elsa sedikit saja ke kanan memindahkan gaun biru ke nomor piksel baru sehingga kabel bobot lama langsung kebingungan.",
        "**Transisi ke Slide 8:** Jangan hanya dibayangkan — mari kita geser foto Elsa langsung di Simulator #1!",
    ],
    8: [
        "**Tujuan Slide (2 menit — #1.3 Simulator Full MLP Bergaya P02):** Menguji langsung efek mengubah **jumlah neuron Hidden Layer (`4 → 128`)** terhadap ledakan bobot dan dampak menggeser foto Frozen **`0 → 4 piksel`** di koordinat tetap.",
        "**Panduan Demo Interaktif:** Pilih foto nyata (**Anna / Elsa / Olaf**) di bar atas, gerakkan slider **`Hidden: 4 ↔ 128`** sambil menunjuk persamaan bobot di bawah panggung, lalu tekan **`▶ Play`** untuk menyaksikan sinyal mengalir `60fps` melewati 4 tahap hingga foto Elsa bergeser `+2px` dan prediksinya langsung meleset (`29%` kalah dari `Olaf 36%`)!",
        "**Transisi ke Slide 9:** Setelah melihat kelemahan nyata MLP pada foto, kapan sebenarnya MLP tetap menjadi pilihan terbaik?",
    ],
    9: [
        "**Tujuan Slide (1 menit — #1.4 Use Case & Verdict MLP):** Menegaskan bahwa MLP bukan arsitektur gagal — ia juara mutlak untuk **data tabel (CSV)** dan tetap dipakai di ujung CNN sebagai *Classification Head*.",
        "**Naskah Pengajar:** Tunjuk kotak verdict merah di bawah: MLP kita simpan sebagai **kontrol negatif** pembuktian di notebook, bukan sebagai *backbone* pemroses foto Frozen.",
        "**Transisi ke Slide 10:** Saatnya melangkah ke inovasi yang mengubah sejarah Computer Vision: **CNN Klasik**!",
    ],
    10: [
        "**Tujuan Slide (1 menit — Pembuka Bab 2: CNN Klasik):** Memperkenalkan ide besar *Convolutional Neural Network*: berhenti meratakan foto di awal; biarkan filter **menggeser di atas grid 2D**!",
        "**Naskah Pengajar:** *\"Alih-alih menarik 150 ribu kabel ke satu piksel tetap, CNN memakai satu kaca pembesar kecil `3×3` yang berjalan menyisir seluruh sudut foto Elsa.\"*",
        "**Transisi ke Slide 11:** Mari kita lihat cetak biru arsitektur CNN Klasik 3-blok secara utuh.",
    ],
    11: [
        "**Tujuan Slide (1.5 menit — #2.1 Alur Interaktif CNN Klasik 4 Tahap):** Menunjukkan perjalanan visual `Foto 2D Utuh -> Conv2D 3×3 + ReLU -> MaxPooling 2×2 -> Conv Dalam + GAP` dengan alasan jelas kenapa CNN 95× lebih hemat (`101.829` param) dari MLP.",
        "**Panduan Demo Interaktif:** Klik **`▶ Play 4 Tahap`** (atau klik satu per satu kartu kiri/kanan) untuk mengarahkan fokus peserta secara berurutan: `Tahap 1` menjaga piksel 2D tetap bertetangga → `Tahap 2` filter `3×3` menyalakan tepi biru di *Feature Map* → `Tahap 3` *MaxPool* meringkas peta & membuatnya tahan geser → `Tahap 4` *GAP + Softmax* menebak Elsa!",
        "**Transisi ke Slide 12:** Mari bedah lebih rinci 4 senjata mekanis di balik blok konvolusi (`Kernel`, `Stride`, `Padding`, dan `Pooling`).",
    ],
    12: [
        "**Tujuan Slide (2 menit — #2.2 Animasi Sliding Window 3×3 & Perpindahan Piksel pada Foto Frozen):** Memperlihatkan secara langsung menggunakan foto asli **Elsa, Anna, dan Olaf** bagaimana *sliding window `3×3`* menggeser & memindahkan nilai piksel ke *Feature Map*, efek `Stride S=1 vs S=2` + `Padding P=1`, *MaxPooling `2×2`*, serta perluasan *Receptive Field*.",
        "**Naskah Pengajar:** Arahkan perhatian peserta ke foto asli Frozen yang bergerak di keempat kartu: (1) jendela `3×3` di atas Elsa menembakkan titik piksel merah menyala ke `Feature Map` biru; (2) bingkai `Pad P=1` pada foto Anna + gerak rapat `S=1` vs lompat `S=2`; (3) kotak kuning `2×2` pada Olaf memindahkan nilai maksimum `8, 4, 7, 6`; dan (4) sorotan `3×3` meluas menjadi `Elsa Utuh ✓`.",
        "**Transisi ke Slide 13:** Sekarang mari kita coba kendalikan sendiri Filter, Stride, dan Padding pada piksel nyata foto Elsa di Simulator #2!",
    ],
    13: [
        "**Tujuan Slide (2.5 menit — #2.3 Simulator #2: Sliding Window 3×3 pada Piksel Elsa):** Memperlihatkan secara nyata bagaimana operasi konvolusi bekerja lewat **jendela geser (*sliding window*) `3×3`** di atas matriks `16×16` foto Elsa.",
        "**Panduan Demo Interaktif:** Kotak kuning `3×3` di panel kiri otomatis menyala sejak awal (dan bisa digeser manual dengan **klik langsung piksel mana pun**!). Tekan **`▶ Play 3×3`** agar jendela kuning meluncur baris demi baris sambil melukis *Feature Map* biru, lalu ubah **`Stride: 2`** dan **`Padding: Same (1)`** — bingkai padding biru muda di tepi `18×18` langsung muncul menjelaskan kenapa tepi pinggir bisa terpindai!",
        "**Transisi ke Slide 14:** Hebat ya, bobotnya turun ~95×! Tapi kenapa CNN polos masih belum cukup kalau ditumpuk sangat dalam atau dilatih dari nol pada data kecil?",
    ],
    14: [
        f"**Tujuan Slide (1.5 menit — #2.4 Use Case & Batas CNN Klasik):** Menempatkan CNN Klasik secara jujur: andal untuk OCR/inspeksi seragam, tetapi pada `{_S['total_images']}` foto Frozen (~85–100 train) belajar dari nol hanya mencapai `val_acc {_S['cnn_val']}%` (uji `48×48`).",
        "**Naskah Pengajar:** Tekankan peran resminya: **CNN Klasik adalah Baseline #1 (*from scratch*)** proyek Frozen — membuktikan kita butuh dua hal: (1) jaringan yang lebih dalam tapi tetap lancar dilatih (**ResNet**), dan (2) bobot siap pakai (*Pretrained CNN* di P04).",
        "**Transisi ke Slide 15:** Sebelum lanjut ke ResNet, mari cek pemahaman hitung dimensi *Feature Map* lewat Q&A #1!",
    ],
    15: [
        "**Tujuan Slide (2 menit — Q&A #1: Hitung Output CNN):** Menguji pemahaman rumus ukuran konvolusi `28×28` dengan `Kernel 3×3, Stride 1, Padding Valid` + `MaxPool 2×2`.",
        "**Panduan Demo / Naskah Pengajar:** Beri peserta ~30 detik menghitung di kepala `(28 - 3 + 0)/1 + 1 = 26`, lalu dibagi 2 menjadi `13×13`. Minta mereka memilih A/B/C sebelum mengklik tombol **`Klik untuk Lihat Jawaban & Pembahasan`**.",
        "**Transisi ke Slide 16:** Sekarang kita masuk Bab 3 untuk memecahkan misteri kenapa CNN yang terlalu dalam justru susah dilatih.",
    ],
    16: [
        "**Tujuan Slide (1 menit — Pembuka Bab 3: ResNet):** Mengenalkan terobosan besar Kaiming He dkk. (`2015`): **Residual Network (ResNet)** dengan ide jalan pintas yang sederhana namun revolusioner.",
        "**Naskah Pengajar:** *\"Bayangkan pesan berantai di kelas sepanjang 50 baris: makin panjang barisnya, suara di ujung depan hampir hilang (*Vanishing Gradient*). Solusinya? Buat kabel mikrofon langsung ke depan!\"*",
        "**Transisi ke Slide 17:** Mari lihat bukti paradoks jaringan polos dalam vs ResNet langsung di dataset Frozen.",
    ],
    17: [
        "**Tujuan Slide (1.5 menit — #3.1 ResNet In General):** Menjelaskan *Degradation Problem* pada *Plain Deep Net* dan membuktikannya lewat grafik `03_resnet_skip_gap.png` pada foto Frozen (`Plain` vs `Mini-ResNet` dengan parameter identik `24.373`).",
        "**Naskah Pengajar:** Tunjuk kurva training di slide: meski jumlah parameternya sama persis, `Mini-ResNet` mampu menurunkan error lebih dalam (`loss 0.762` vs `0.963`) dan menggandakan akurasi validasi (`22.9%` vs `11.4%`) berkat jalan pintas!",
        "**Transisi ke Slide 18:** Apa saja 3 inovasi spesifik di dalam blok ResNet50?",
    ],
    18: [
        "**Tujuan Slide (1.5 menit — #3.2 ResNet Fitur Khusus):** Membedah **Skip Connection (`y = F(x) + x`)**, **Batch Normalization** (penjaga skala angka antar layer), dan **Global Average Pooling (`GAP`)** yang menghancurkan kepala *Flatten* (`51.38M -> 10.245` param).",
        "**Naskah Pengajar:** Jelaskan makna `F(x) + x`: alih-alih belajar memetakan gambar dari nol berulang-ulang, tiap blok cukup belajar *koreksi/selisih kecilnya* saja.",
        "**Transisi ke Slide 19:** Mari lihat perjalanan sinyal *Backpropagation* mundur dari Layer 20 ke Layer 1 di Simulator #3!",
    ],
    19: [
        "**Tujuan Slide (2 menit — #3.3 Simulator #3: ResNet Signal Flow):** Memvisualisasikan perbedaan drastis antara hilangnya sinyal di *Plain Deep Net* (`7%` di Layer 1) vs bertahannya sinyal di *ResNet* (`86%`).",
        "**Panduan Demo Interaktif:** Tekan **`▶ Play Backprop`**! Amati bulatan kuning bergerak mundur dari `Layer 20 -> L15 -> L10 -> L5 -> L1` saat mode `Plain Deep Net` (batang merah hampir padam), lalu otomatis beralih ke `ResNet (+Skip & GAP)` di mana sinyal melewati **Jalur Tol `+x`** dan tetap kuat `86%`!",
        "**Transisi ke Slide 20:** Kalau ResNet sekuat itu, kenapa kita tidak langsung menjadikannya model utama proyek Frozen?",
    ],
    20: [
        f"**Tujuan Slide (1.5 menit — #3.4 Use Case & Verdict ResNet):** Menjelaskan posisi **ResNet50** (`{_S['res_params']:,}` param / `{_S['res_mb']} MB` / `{_S['res_ms']:.0f} ms`) secara objektif — sangat perkasa di server GPU & radiologi medis, tetapi terlalu berat/berisiko *overfit* pada `{_S['total_images']}` foto Frozen.",
        "**Naskah Pengajar:** Tekankan peran ResNet50 di proyek: sebagai **pembanding berat (*heavy benchmark*)** melawan model ringan di P06/P07.",
        "**Transisi ke Slide 21:** Mari uji pemahaman konsep `Skip Connection + GAP` melalui Q&A #2.",
    ],
    21: [
        "**Tujuan Slide (2 menit — Q&A #2: Rahasia ResNet & GAP):** Memastikan peserta benar-benar paham dua fungsi berbeda: `Skip +x` menjaga gradien `L20 -> L1`, sementara `GAP` meringkas `7×7×2048` menjadi `2.048` angka rata-rata.",
        "**Panduan Demo / Naskah Pengajar:** Ajak peserta menebak dulu opsi yang benar sebelum mengklik tombol reveal jawaban.",
        "**Transisi ke Slide 22:** Sekarang kita masuk bab puncak evolusi arsitektur: era model ringan modern (`MobileNetV2` & `EfficientNet`).",
    ],
    22: [
        "**Tujuan Slide (1 menit — Pembuka Bab 4: MobileNetV2 & EfficientNet):** Menyiapkan panggung dua bintang utama efisiensi modern yang justru menurunkan bobot dari `90 MB` ke `~8–15 MB` tanpa membuang kecerdasan konvolusi.",
        "**Naskah Pengajar:** *\"Kalau ResNet ibarat truk tangki tangguh 90 MB, bagaimana cara mengecilkannya menjadi motor sport lincah di bawah 9 MB yang tetap cerdas melihat figurin Frozen di HP?\"*",
        "**Transisi ke Slide 23:** Kenalkan generasi ke-4: **MobileNetV2** — kandidat jagoan utama proyek kita!",
    ],
    23: [
        f"**Tujuan Slide (1.5 menit — #4.1 MobileNetV2 In General):** Memperkenalkan **MobileNetV2** sebagai **100% keluarga CNN modern** yang memangkas bobot lebih dari 10× dibanding ResNet50 (`{_S['mob_params']:,}` param / `{_S['mob_mb']} MB`).",
        "**Naskah Pengajar:** Garisbawahi kekhawatiran umum pemula: *\"Memilih MobileNetV2 bukan berarti meninggalkan CNN — MobileNetV2 adalah CNN itu sendiri, dengan blok konvolusi yang dipecah agar super efisien!\"*",
        "**Transisi ke Slide 24:** Rahasia penghematan `8.4×` itu ada di 3 teknik berikut ini.",
    ],
    24: [
        "**Tujuan Slide (2 menit — #4.2 MobileNetV2 Fitur Khusus):** Membedah 3 pilar Sandler dkk.: (1) **Depthwise Separable Convolution** (memisahkan kerja *spasial per kanal `3×3`* dan *pengaduk antar kanal `1×1`*), (2) **Inverted Residual** (`sempit → lebar 6× → sempit`), dan (3) **Linear Bottleneck** (melepas ReLU di proyeksi sempit agar informasi tidak terpotong).",
        "**Naskah Pengajar:** Pakai analogi *\"pelukis + peracik cat\"* saat menunjuk diagram `04_mobilenetv2_depthwise.png`: pisahkan tugas menggambar garis per kanal dari tugas mencampur warna antar kanal!",
        "**Transisi ke Slide 25:** Mari buktikan langsung penghematan `231.2 juta` vs `27.5 juta` perkalian di Simulator #4!",
    ],
    25: [
        "**Tujuan Slide (2 menit — #4.3 Simulator #4: MobileNetV2 Bottleneck Flow):** Membandingkan langsung *Conv2D Standar* vs *Inverted Residual MobileNetV2* langkah demi langkah.",
        "**Panduan Demo Interaktif:** Mulai dari mode `1. Conv2D Biasa` (`231.2 Juta ops`), lalu tekan **`▶ Play Aliran Blok`**! Simulator akan otomatis berpindah ke `MobileNetV2` dan menyorot bertahap `Langkah 1 (Expand 1×1: 32→192)` -> `Langkah 2 (Depthwise 3×3: 27.5M ops)` -> `Langkah 3 (Linear Project 1×1 + Skip)`!",
        "**Transisi ke Slide 26:** Dengan efisiensi 8.4× lebih hemat, mari lihat alasan ilmiah mengapa MobileNetV2 dipilih menjadi *backbone* utama Frozen!",
    ],
    26: [
        f"**Tujuan Slide (1.5 menit — #4.4 Use Case & Pemilihan MobileNetV2):** Merangkum keunggulan MobileNetV2 di HP (`TFLite`) dan di proyek `{_S['total_images']}` foto Frozen (`{_S['mob_mb']} MB`, `{_S['mob_dw']}` *DepthwiseConv2D*, head latih hanya **`6.405` parameter** saat *base* beku di P04!).",
        "**Naskah Pengajar:** Tekankan rencana resmi **Transfer Learning 2 Tahap** (P04–P08): Tahap 1 latih head `6.405` param (`preprocess_input` `[-1,+1]`), Tahap 2 *fine-tuning* ujung backbone dengan `training=False`, lalu audit **Grad-CAM (`7×7×1280`)** di P08.",
        "**Transisi ke Slide 27:** Sebelum memutuskan final, ada satu lagi evolusi setelah MobileNetV2 yang wajib kita bedah: **EfficientNet**!",
    ],
    27: [
        "**Tujuan Slide (1 menit — #5.1 EfficientNet In General):** Menjelaskan motivasi lahirnya **EfficientNet** (Tan & Le): menggantikan cara memperbesar jaringan yang asal menebak dengan formula scaling sistematis berbasiskan blok `MBConv`.",
        "**Naskah Pengajar:** *\"Kalau di ResNet orang menaikkan kedalaman secara manual (`18 -> 50 -> 101`), EfficientNet menemukan cara menaikkan tinggi gedung, lebar lantai, dan ketajaman kamera secara bersamaan dan seimbang.\"*",
        "**Transisi ke Slide 28:** Mari bedah 3 senjata khas EfficientNet beserta visual nyata di foto `elsa_ramai.jpg`!",
    ],
    28: [
        f"**Tujuan Slide (1.5 menit — #5.2 EfficientNet Fitur Khusus):** Menjelaskan **Compound Scaling (φ)**, **MBConv** (`{_S['eff_se']}` blok berbasis MobileNet), dan **Squeeze-and-Excitation (SE) Attention** (`05_efficientnet_compound_se.png`) untuk memusatkan bobot pada gaun/wajah Elsa di latar `ramai`.",
        "**Naskah Pengajar:** Perhatikan istilah teknis *Squeeze* (memeras peta menjadi 1 ringkasan skor per kanal) lalu *Excite* (memberi volume `0..1` agar kanal pengganggu diredam).",
        "**Transisi ke Slide 29:** Mari uji langsung efek menaikkan skala `B0 -> B1 -> B2` dan tombol **SE Gate** pada foto `elsa_ramai.jpg` di Simulator #5!",
    ],
    29: [
        "**Tujuan Slide (2 menit — #5.3 Simulator #5: EfficientNet Scaling & SE Gate):** Membuktikan cara kerja **SE Attention** meredam kanal latar ramai (`Cangkir 0.16`, `Dinding 0.10`) sambil mengangkat ciri Elsa (`0.95`, `0.88`).",
        "**Panduan Demo Interaktif:** Klik **`▶ Play SE Gate`**! Peserta akan melihat skala naik ke `B1`, lalu tahap `Squeeze` merangkum 4 kanal (bobot rata `0.55`), hingga akhirnya `SE ON` mengangkat batang biru/hijau Elsa & menekan batang latar ramai ke dasar!",
        "**Transisi ke Slide 30:** Lalu, jika punya SE Attention, mengapa EfficientNetB0 di proyek kita menjadi **Runner-Up** dan bukan menggantikan MobileNetV2 sepenuhnya?",
    ],
    30: [
        f"**Tujuan Slide (1.5 menit — #5.4 Use Case & Verdict EfficientNet):** Membandingkan jujur `EfficientNetB0` (`{_S['eff_params']/1e6:.2f}M` param, `{_S['eff_mb']} MB`, `{_S['eff_layers']}` layer, `{_S['eff_ms']:.1f} ms` CPU) vs `MobileNetV2` (`{_S['mob_ms']:.1f} ms` CPU): di CPU tanpa GPU, cabang SE membuat B0 ~`{_S['eff_ms']/_S['mob_ms']:.1f}×` lebih lambat!",
        "**Naskah Pengajar:** Tegaskan peran resmi di silabus: **MobileNetV2** = *Model Utama*, sedangkan **EfficientNetB0** = **Runner-Up / pembanding** terutama untuk menguji apakah *SE Attention* unggul di kondisi latar `ramai` (`{_S['ramai']}` foto).",
        "**Transisi ke Slide 31:** Kini saatnya menyandingkan kelima arsitektur dalam satu matriks angka nyata Keras + melihat posisi model era terbaru seperti ViT dan YOLO.",
    ],
    31: [
        "**Tujuan Slide (2 menit — Matriks Rangkuman 5 Arsitektur + Konteks ViT/YOLO):** Mengkonsolidasi seluruh data benchmark Keras (`224×224×3`) bersama grafik kuadran `06_5arch_comparison_chart.png`.",
        "**Naskah Pengajar:** Tunjuk baris hijau **MobileNetV2 ★** pada tabel & posisi kiri-bawah di grafik kuadran. Jelaskan singkat callout biru: **Vision Transformer (ViT)** butuh jutaan foto (*overfit* di 143 foto), sedangkan **YOLO** dirancang untuk *Object Detection* (bukan klasifikasi tunggal seperti proyek kita).",
        "**Transisi ke Slide 32:** Sekarang giliran kamu bertindak sebagai konsultan arsitektur di Q&A #3!",
    ],
    32: [
        "**Tujuan Slide (2 menit — Q&A #3: Konsultan Pemilihan Arsitektur):** Mengunci pemahaman strategis sebelum jeda istirahat — memastikan peserta bisa berargumen **mengapa MobileNetV2 terpilih** menggunakan angka nyata, bukan sekadar hafalan.",
        "**Panduan Demo:** Arahkan ke 3 syarat kotak kiri (`143 foto`, `Colab Gratis / HP`, `Tahan Overfit`), minta peserta memilih A/B/C lalu klik **`Klik untuk Lihat Jawaban & Pembahasan`**.",
        "**Transisi ke Slide 33:** Semua angka di matriks tadi akan kita bangun dan ukur sendiri dengan tangan kita setelah istirahat!",
    ],
    33: [
        "**Tujuan Slide (1 menit — Transisi ke Praktik Kode):** Memberi pratinjau jelas mengenai 3 bukti nyata yang akan dihasilkan di notebook `P03_arsitektur_neural_network.ipynb`.",
        "**Naskah Pengajar:** Tekankan dua kenyamanan bagi pemula: (1) gaya **Visual-First** (sel latihan cuma 3–10 baris dengan `Alat Visualisasi Siap Pakai`), dan (2) **Mode Aman Offline (`weights=None`)** supaya proses perakitan & benchmark berjalan cepat tanpa download ratusan MB.",
        "**Transisi ke Slide 34:** Sebelum masuk ke kode, mari istirahat sejenak selama 5 menit.",
    ],
    34: [
        "**Tujuan Slide (5 menit — Istirahat 5 Menit):** Mengistirahatkan mata dan fokus peserta setelah 52 menit teori & simulasi intensif, sambil menyiapkan Colab / Jupyter Notebook.",
        "**Naskah Pengajar:** *\"Kita jeda 5 menit ya. Silakan minum air atau peregangan ringan. Setelah ini kita jalankan notebook `P03_arsitektur_neural_network.ipynb`.\"*",
        "**Transisi ke Slide 35:** Waktu istirahat selesai — mari buka peta 6 langkah praktik kode kita.",
    ],
    35: [
        "**Tujuan Slide (2 menit — Cover Peta Hands-On 6 Langkah):** Menjelaskan tata cara kerja di notebook: jalankan Setup 3 tahap + sel helper sekali dengan `Shift + Enter`, lalu selesaikan 6 langkah (`# TODO 1` s.d. `# TODO 8`).",
        "**Naskah Pengajar:** Ingatkan bahwa peserta bisa membuka `<details> Hint & Jawaban` kapan saja bila lupa sintaks Keras, namun usahakan menebak 1–2 menit terlebih dahulu.",
        "**Transisi ke Slide 36:** Ayo mulai Langkah 1 membangun MLP Keras!",
    ],
    36: [
        f"**Tujuan Slide (6 menit — Hands-On Langkah 1: MLP `# TODO 1`):** Membimbing peserta menyusun `Dense(64, 'relu') -> Dense(32, 'relu')` di bawah `Flatten()` dan menyaksikan sendiri grafik lonjakan ke `{_S['mlp_params']:,}` parameter.",
        "**Panduan Praktik:** Pastikan peserta menjalankan `Setup 1–3` dan sel `Alat Visualisasi Siap Pakai` dulu sebelum `# TODO 1`, lalu perhatikan panel output nyata di sisi kanan slide sebagai pembanding bahwa kode mereka sukses (`assert` hijau).",
        "**Transisi ke Slide 37:** Sesudah membuktikan ledakan MLP, mari uji langsung filter konvolusi `3×3` di Langkah 2.",
    ],
    37: [
        "**Tujuan Slide (6 menit — Hands-On Langkah 2: Conv2D + MaxPool `# TODO 2`):** Membimbing peserta mengisi `Conv2D(1, kernel_size=3, use_bias=False)` dan `MaxPooling2D(pool_size=(2, 2))` lalu melihat foto Elsa `32×32` berubah menjadi *Feature Map* tepi!",
        "**Panduan Praktik:** Ajak peserta membaca kotak `> 💡 Apa yang perlu diperhatikan` di notebook: amati tepi gaun & rambut Elsa menyala kuning, serta ukurannya menyusut `(32,32) -> (30,30) -> (15,15)`.",
        "**Transisi ke Slide 38:** Sekarang mari gabungkan 3 blok konvolusi dan GAP menjadi **CNN Klasik** utuh di Langkah 3!",
    ],
    38: [
        f"**Tujuan Slide (6 menit — Hands-On Langkah 3: CNN Klasik & Kurva Latih `# TODO 3`):** Memastikan peserta mengisi `MaxPooling2D(2)` dan `GlobalAveragePooling2D()`, melihat parameter jatuh 95× ke `{_S['cnn_params']:,}`, dan menjalankan kurva latih MLP vs CNN pada data `48×48`.",
        "**Panduan Praktik:** Tunjukkan betapa cepatnya `bandingkan_training_mlp_vs_cnn()` berjalan secara offline dan tunjuk bagaimana garis biru CNN naik jauh lebih stabil dari garis putus-putus merah MLP.",
        "**Transisi ke Slide 39:** Setelah 3 blok berurutan, bagaimana menulis blok bercabang **Skip Connection** di Keras? Mari ke Langkah 4!",
    ],
    39: [
        f"**Tujuan Slide (7 menit — Hands-On Langkah 4: Functional API `Add()` & ResNet50 `# TODO 4`):** Mengenalkan perbedaan `Sequential` vs **Keras Functional API** dengan contoh minimal `Add()([fx, shortcut])` dan memeriksa struktur `ResNet50(weights=None)`.",
        "**Panduan Praktik:** Minta peserta mengecek angka `assert`: jumlah layer `Add()` di `ResNet50` tepat **`{_S['res_skip']}` buah** dari total `{_S['res_layers']}` layer!",
        "**Transisi ke Slide 40:** Kini di Langkah 5 kita bedah isi dalam **MobileNetV2** dan **EfficientNetB0** langsung lewat kode!",
    ],
    40: [
        f"**Tujuan Slide (8 menit — Hands-On Langkah 5: Audit MobileNetV2 & EfficientNetB0 `# TODO 5–6`):** Membuktikan secara empiris perbedaan arsitektural dua model efisien modern di Keras.",
        f"**Panduan Praktik:** Peserta mengisi `# TODO 5` (`MobileNetV2`) & `# TODO 6` (`EfficientNetB0`), lalu membaca bukti langsung dari layer model: `MobileNetV2` memiliki **`{_S['mob_dw']}` layer `DepthwiseConv2D`**, sedangkan `EfficientNetB0` memiliki **`{_S['eff_se']}` gerbang SE `Multiply`**!",
        "**Transisi ke Slide 41:** Saatnya menggabungkan kelima model ke dalam satu lomba benchmark kecepatan & ukuran di Langkah 6!",
    ],
    41: [
        "**Tujuan Slide (7 menit — Hands-On Langkah 6: Benchmark 5 Arsitektur & Ekspor `results/` `# TODO 7–8`):** Menjalankan pengukuran nyata waktu inferensi 8 foto Frozen `224×224×3` dan menyimpan hasilnya ke `results/p03_5_architectures_benchmark.csv` & `.png`.",
        "**Panduan Praktik:** Ingatkan peserta untuk mengecek fungsi `pasang_head_5kelas` dengan `base_model(inp, training=False)` — pola resmi ini akan kita pakai terus di P04–P08. Jika ada waktu lebih, ajak mencoba sel *Bonus Eksperimen Bebas `FILTER_PILIHAN`* di bawahnya!",
        "**Transisi ke Slide 42:** Sebelum mengakhiri materi, mari uji naluri arsitekturmu lewat Mini-Challenge!",
    ],
    42: [
        f"**Tujuan Slide (6 menit — Mini-Challenge: Konsultan Arsitektur):** Melatih peserta memetakan **Kasus A (CSV Harga Rumah)**, **Kasus B (Radiologi Server GPU)**, dan **Kasus C (Kamera Frozen {_S['total_images']} foto)** ke arsitektur tepat, serta menyusun 3 kalimat argumen memilih **MobileNetV2**.",
        "**Panduan Demo:** Biarkan peserta menuliskan draf singkatnya terlebih dahulu menggunakan angka dari `df_bench` (`2.26M`, `8.64 MB`), lalu klik **`Klik untuk Lihat Jawaban & Pembahasan`** untuk membandingkan hasilnya.",
        "**Transisi ke Slide 43:** Mari rapikan kosa kata teknis yang sudah kita pelajari hari ini lewat Kamus 18 Istilah.",
    ],
    43: [
        "**Tujuan Slide (2 menit — Kamus Istilah P03):** Menyegarkan kembali 18 istilah teknis asli bahasa Inggris beserta arti awamnya tanpa julukan buatan, lengkap dengan fitur cari dan lompat slide.",
        "**Panduan Demo:** Gunakan filter per bab atau ketik salah satu kata kunci seperti `Bottleneck`, `Skip`, atau `GAP` untuk memperagakan cara me-review materi.",
        "**Transisi ke Slide 44:** Saatnya evaluasi seru 5 soal kuis interaktif — soal pertama tentang MLP!",
    ],
    44: [
        "**Tujuan Slide (2 menit — Kuis 1/5: Kelemahan MLP pada Gambar):** Menguji pemahaman mengapa MLP `Dense` melambung ke `9.64M` parameter dan gagal mempertahankan tebakan saat figurin bergeser.",
        "**Panduan Demo:** Minta peserta klik opsi `A`, `B`, atau `C` dulu di kartu kiri, kemudian buka **`Lihat Jawaban & Penjelasan`** untuk memverifikasi alasannya.",
        "**Transisi ke Slide 45:** Soal kedua menguji hitung cepat dimensi *Feature Map* dan *MaxPool* CNN.",
    ],
    45: [
        "**Tujuan Slide (2 menit — Kuis 2/5: Hitung Output Conv2D + MaxPool):** Menguji perhitungan `(10 - 3 + 0) / 1 + 1 = 8×8`, lalu `MaxPool 2×2` mengecilkannya menjadi `4×4`.",
        "**Panduan Demo:** Ingatkan peserta untuk membayangkan langkah kotak `3×3` di atas papan `10×10` — jangan cuma menebak rumus!",
        "**Transisi ke Slide 46:** Soal ketiga masuk ke peran *Skip Connection* pada ResNet.",
    ],
    46: [
        "**Tujuan Slide (2 menit — Kuis 3/5: Fungsi Skip Connection `+x`):** Mengkonfirmasi peserta memahami jalan pintas mencegah *Vanishing Gradient* mundur ke layer awal.",
        "**Panduan Demo:** Minta peserta menjelaskan dengan bahasanya sendiri mengapa `F(x) + x` membantu layer pertama tetap belajar tepi gambar.",
        "**Transisi ke Slide 47:** Soal keempat menguji inovasi efisiensi inti di balik MobileNetV2.",
    ],
    47: [
        "**Tujuan Slide (2 menit — Kuis 4/5: Rahasia Hemat MobileNetV2):** Mengecek pemahaman peserta bahwa MobileNetV2 memecah kerja konvolusi berat menjadi *Depthwise (`3×3` per kanal)* + *Pointwise (`1×1` pengaduk)* + *Linear Bottleneck*.",
        "**Panduan Demo:** Kaitkan jawaban dengan bukti nyata yang baru saja dilihat di `# TODO 5` (`17` layer `DepthwiseConv2D`).",
        "**Transisi ke Slide 48:** Satu soal kuis terakhir tentang EfficientNet dan *SE Attention*!",
    ],
    48: [
        "**Tujuan Slide (2 menit — Kuis 5/5: Compound Scaling & SE Gate):** Menguji pemahaman bahwa EfficientNet menyeimbangkan *Depth × Width × Resolusi* secara bersamaan serta memakai *SE Attention* untuk meredam latar belakang `ramai`.",
        "**Panduan Demo:** Setelah membuka penjelasan, berikan apresiasi atas ketuntasan peserta menjawab seluruh 5 soal kuis P03.",
        "**Transisi ke Slide 49:** Mari ringkas seluruh perjalanan 120 menit hari ini dalam 3 Poin Utama!",
    ],
    49: [
        "**Tujuan Slide (2 menit — Rangkuman 3 Poin Utama):** Menegaskan tiga pesan inti yang harus dibawa pulang: (1) Setiap arsitektur lahir dari cacat nyata, (2) Senjata khas tiap generasi (`Conv2D -> Skip+GAP -> Depthwise+Linear -> Compound+SE`), dan (3) **MobileNetV2 (*Pretrained CNN*)** resmi terpilih sebagai arsitektur inti proyek Frozen menuju P04.",
        "**Naskah Pengajar:** Bacakan kutipan penutup kartu bawah bersama peserta sebagai pegangan mindset insinyur AI.",
        "**Transisi ke Slide 50:** Terakhir, mari lihat pratinjau seru apa yang akan kita kerjakan di **P04**!",
    ],
    50: [
        "**Tujuan Slide (1 menit — Closing & Jembatan ke P04):** Memberi apresiasi hangat atas keberhasilan peserta merakit & membenchmark 5 arsitektur di Python/Keras, serta membangun antusiasme ke **P04 — Arsitektur CNN & Transfer Learning**.",
        "**Naskah Pengajar:** *\"Hari ini semua arsitektur kita uji dalam keadaan polos (`weights=None`). Di P04 nanti, kita akan memasang otak terlatih (`ImageNet`) ke dalam MobileNetV2 agar akurasi dataset Frozen melesat tinggi!\"*",
        "**Transisi ke Slide 51–52:** Sebagai bahan bacaan tambahan opsional sesudah kelas, dua slide berikut merangkum referensi resmi sesuai silabus.",
    ],
    51: [
        "**Tujuan Slide (0 menit — Referensi Bagian 1):** Daftar tautan opsional untuk mendalami MLP, *CNN Explainer*, *Convolution Arithmetic*, dan paper ResNet (`arXiv 1512.03385`).",
        "**Naskah Pengajar:** Tidak perlu dibahas rinci saat kelas berakhir; sampaikan bahwa tautan bisa diklik kapan saja langsung dari PDF atau dek HTML.",
        "**Transisi ke Slide 52:** Slide terakhir berisi tautan lanjutan untuk MobileNetV2 & Transfer Learning persiapan P04.",
    ],
    52: [
        "**Tujuan Slide (0 menit — Referensi Bagian 2):** Daftar tautan resmi MobileNetV2 (`arXiv 1801.04381`), panduan TensorFlow Transfer Learning (ID), Roboflow, serta Keras Functional API.",
        "**Penutup Sesi:** Selesai! Pastikan folder `results/` peserta sudah menyimpan `p03_5_architectures_benchmark.csv` & `.png` sebelum menutup Colab/Jupyter.",
    ],
}
