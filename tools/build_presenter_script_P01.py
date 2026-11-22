"""Generator PDF Script Penjelasan Materi P01 per Slide (Slide 1 s.d. Slide 59) — Versi Detail & Mendalam.

Format setiap halaman:
- Slide {N} — Judul Slide
- Gambar Slide (visual asli slide 16:9 dari P01_understanding_images_processing_eda.html)
- Penjelasan Detail Slide (poin-poin penjelasan materi yang sangat lengkap, membedah konsep,
  cara kerja teknis, setiap bagian visual/diagram di slide, rumus/angka, serta dampaknya ke AI)
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLIDES_HTML_PATH = ROOT / "materials" / "P01" / "P01_understanding_images_processing_eda.html"
OUT_PDF_PATH = ROOT / "materials" / "P01" / "P01_presenter_script.pdf"
TMP_HTML_PATH = ROOT / "materials" / "P01" / "_tmp_presenter_script_P01.html"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


# Penjelasan materi per slide yang detail, mendalam, dan membedah seluruh isi slide (1 s.d. 59)
SLIDE_EXPLANATIONS: dict[int, list[str]] = {
    1: [
        "**Judul & Ruang Lingkup Sesi P01:** *Memahami Gambar di Komputer, Image Processing & Exploratory Data Analysis (EDA)* merupakan fondasi paling awal dalam kurikulum *Deep Learning untuk Computer Vision* (total durasi sesi: 120 menit).",
        "**Masalah Utama yang Dijawab di Sesi Ini:** Sebelum sebuah model kecerdasan buatan (*Neural Network / CNN*) dapat dilatih untuk mengenali gambar (seperti karakter atau objek), kita harus memahami bagaimana gambar fisik diterjemahkan menjadi struktur angka di dalam memori komputer.",
        "**Tiga Pilar Materi P01:**",
        "• **1. Representasi Gambar Digital (*Understanding Images*):** Membedah anatomi gambar dari tingkat titik terkecil (*pixel*), saluran warna (*color channels*: *Grayscale* 1 channel vs *RGB* 3 channels), hingga struktur *array/tensor* 3 dimensi `(Height, Width, Channels)`.",
        "• **2. Pemrosesan Citra Dasar (*Image Processing*):** Teknik menyiapkan gambar mentah agar memenuhi syarat matematis model AI, meliputi penyeragaman ukuran (*Resize `224×224`*) tanpa merusak proporsi bentuk (*Letterbox Padding*) serta penyetaraan skala nilai pixel (*Normalization `0.0–1.0`* dalam tipe data `float32`).",
        "• **3. Audit Kualitas Dataset (*Exploratory Data Analysis / EDA*):** Memeriksa kesehatan koleksi foto secara statistik dan visual — mendeteksi ketimpangan jumlah kelas (*Class Imbalance*), masalah pencahayaan (*Histogram, Brightness, Contrast*), kerumitan latar belakang (*Canny Edge Density: Polos vs Ramai*), serta 3 jebakan file kamera HP (*EXIF Orientation, Duplicate Hash SHA-256, Corrupted Files*).",
    ],
    2: [
        "**Struktur 5 Bab Berurutan (Dari Konsep Dasar ke Praktik Kode):**",
        "• **Bab 1 — Cara Kita & Komputer Melihat Gambar (Slide 06–18):** Membandingkan sistem penglihatan manusia (cahaya → retina → otak) dengan sistem kamera digital (lensa → sensor grid pixel → matriks angka `0–255`), cara layar HP menyalakan 3 lampu sub-pixel RGB, konsep *Color Channels* (`1, 3, 4, 5+`), studi kasus dataset klasik **MNIST (`28×28`)**, hingga pemisahan 3 channel warna **RGB**.",
        "• **Bab 2 — Peran AI & Mengapa Perlu Image Processing (Slide 19–29):** Menjelaskan perbedaan mendasar antara *Program Biasa (`if-else`)*, *Machine Learning Klasik*, dan *Deep Learning (CNN)*, alasan mengapa aturan koordinat manual selalu gagal pada foto dunia nyata, serta 2 tahapan wajib *preprocessing* gambar (*Uniform Resolution `224×224`* dan *Normalization*).",
        "• **Bab 3 — Exploratory Data Analysis / EDA (Slide 30–39):** Metodologi pemeriksaan kesehatan dataset foto yang dikelompokkan ke dalam 3 isu utama: **Issue #1** (*Class Imbalance*), **Issue #2** (*Histogram, Brightness & Contrast*), dan **Issue #3** (*Edge Detection Canny & Strategi Latar Polos vs Ramai*).",
        "• **Bab 4 — Tiga Jebakan Tersembunyi Kamera HP (Slide 40–45):** Membedah 3 sumber bug paling sering pada dataset foto buatan sendiri: foto terputar akibat metadata **EXIF (`Orientation = 6`)**, foto kembar/beruntun (**Duplicate & Burst Photos**), file rusak (**Corrupted Files**), serta bahaya kebocoran data ujian (**Data Leakage**).",
        "• **Bab 5 — Praktik Hands-on, Diskusi & Uji Pemahaman (Slide 46–59):** Mengimplementasikan seluruh konsep di atas ke dalam kode Python (*Notebook* 6 langkah), mendiskusikan hasil nyata pada 119 foto valid, mengulas glosarium istilah teknis, dan mengevaluasi pemahaman lewat 5 soal kuis.",
    ],
    3: [
        "**Pembagian Alokasi Waktu 120 Menit (Manajemen Ritme Belajar):**",
        "• **00–10 Menit (10 Menit — Pembuka & Pemanasan):** Orientasi peta materi, sasaran belajar, dan jembatan logika mengapa foto harus diubah menjadi angka.",
        "• **10–40 Menit (30 Menit — Teori & Konsep Visual):** Penjelasan konsep Bab 1 s.d. Bab 4 yang dilengkapi 12 simulator interaktif (simulator kamera, sub-pixel layar, kerapatan pixel, MNIST `28×28`, pencampur RGB, AI Fundamental, kalkulator normalisasi, serta simulator Histogram & Boxplot Brightness/Contrast).",
        "• **40–45 Menit (5 Menit — Istirahat Singkat):** Jeda penyegaran sebelum beralih dari pemahaman konsep visual ke penulisan kode di *Jupyter Notebook / Google Colab*.",
        "• **45–95 Menit (50 Menit — Praktik Hands-on Terpandu):** Mengerjakan 6 langkah terstruktur di Notebook yang sudah dipecah *cell-by-cell* (satu sel = satu aksi sederhana) beserta latihan `# TODO` dan pengecekan otomatis (`assert`).",
        "• **95–110 Menit (15 Menit — Mini-Challenge):** Menganalisis tabel statistik dan grafik *Boxplot Polos vs Ramai* hasil eksekusi Notebook untuk merumuskan hipotesis kesulitan model.",
        "• **110–120 Menit (10 Menit — Kuis & Penutup):** Evaluasi 5 soal pilihan ganda, rangkuman 3 poin kunci (*Key Takeaways*), dan pengantar menuju sesi P02.",
    ],
    4: [
        "**Tiga Kompetensi Inti (*Learning Outcomes*) Sesi P01:**",
        "• **1. Memahami Gambar di Komputer (*Image as a Numerical Matrix*):**",
        "  – Memahami bahwa file foto bukanlah 'gambar utuh' di mata komputer, melainkan kumpulan titik (*pixel*) yang tersusun dalam baris dan kolom.",
        "  – Mampu membaca dimensi matriks gambar (`.shape`): `(Tinggi, Lebar)` untuk gambar 1 channel (*Grayscale*) dan `(Tinggi, Lebar, 3)` untuk gambar berwarna (*RGB*) dengan rentang nilai `0` (gelap total) hingga `255` (terang maksimal).",
        "• **2. Menyiapkan Foto Siap Latih (*Image Preprocessing Pipeline*):**",
        "  – Mampu mengubah ukuran (*resize*) foto yang beragam menjadi ukuran standar model AI (`224 × 224` pixel) menggunakan teknik *Letterbox Padding* agar bentuk objek tidak gepeng/terdistorsi.",
        "  – Mampu mengonversi tipe data bilangan bulat `uint8 (0–255)` menjadi bilangan desimal `float32` dan menormalisasi skalanya ke `0.0–1.0` agar perhitungan matematis *Neural Network* berjalan stabil.",
        "• **3. Memeriksa Kesehatan Koleksi Foto (*Dataset Audit & EDA*):**",
        "  – Mampu menghitung dan membaca metrik statistik dataset: keseimbangan jumlah foto per kelas (*Class Balance*), tingkat terang rata-rata (*Brightness / Mean*), ketajaman kontras (*Contrast / Std*), serta kepadatan garis tepi (*Canny Edge Density*).",
        "  – Mampu menyaring 3 masalah file foto sebelum pelatihan: memutar otomatis foto miring (*EXIF transpose*), memisahkan file rusak (`verify()`), dan mendeteksi foto kembar dengan sidik jari digital (`SHA-256`).",
    ],
    5: [
        "**Perbedaan Input Angka Biasa vs Input Gambar pada Komputer:**",
        "• **Kartu Kiri (Data Angka Biasa):** Ketika kita memasukkan data numerik seperti harga barang, suhu udara, atau nilai ujian (`[80, 95, 70]`) ke dalam program komputer, bentuk datanya sudah berupa angka sehingga prosesor (CPU/GPU) dapat langsung melakukan operasi matematika (penjumlahan, rata-rata, perbandingan).",
        "• **Kartu Tengah (Data Foto Kamera):** Ketika kita memotret objek dunia nyata (seperti apel, wajah, atau mainan karakter) menggunakan kamera HP, hasil yang kita lihat di layar adalah bentuk visual yang kaya warna, bayangan, dan tekstur.",
        "• **Kartu Kanan (Tantangan Komputer):** Komputer secara fisik hanya terdiri dari rangkaian sirkuit elektronik yang memproses angka biner/numerik — komputer **tidak memiliki mata biologis maupun pemahaman konsep bentuk**.",
        "• **Jembatan Solusi:** Agar komputer (dan nantinya model AI) dapat mengenali objek di dalam foto, langkah pertama yang mutlak dilakukan adalah **menerjemahkan setiap titik cahaya pada foto menjadi tabel/matriks angka yang terukur**.",
    ],
    6: [
        "**Pengantar Bab 1 — Cara Kita & Komputer Melihat Gambar:**",
        "• Bab ini membangun intuisi paling mendasar dalam *Computer Vision*: mengapa manusia bisa mengenali sebuah objek dalam sepersekian detik, sedangkan komputer hanya melihat deretan ratusan ribu angka?",
        "• Alur pembahasan Bab 1 bergerak secara kronologis: (1) Cara mata manusia melihat objek → (2) Cara kamera menangkap cahaya menjadi matriks angka di memori → (3) Cara layar HP menampilkan matriks angka kembali menjadi gambar → (4) Anatomi *Pixel* & *Color Channels* (`1, 3, 4, 5+`) → (5) Studi kasus 1 Channel (*MNIST*) vs 3 Channels (*RGB*).",
    ],
    7: [
        "**Mekanisme Penglihatan Manusia (Alur 4 Tahap Biologis di Slide):**",
        "• **Tahap 1 — Cahaya & Objek Nyata:** Penglihatan dimulai dari adanya cahaya (matahari atau lampu) yang menyinari objek fisik (contoh: buah apel merah). Permukaan apel menyerap sebagian spektrum cahaya dan memantulkan spektrum warna merah ke segala arah.",
        "• **Tahap 2 — Mata & Retina:** Lensa mata manusia memfokuskan berkas cahaya pantulan tersebut agar jatuh tepat di lapisan **retina** di bagian belakang bola mata. Retina memiliki jutaan sel reseptor cahaya (*sel batang/rod* untuk gelap-terang dan *sel kerucut/cone* yang peka terhadap gelombang Merah, Hijau, dan Biru).",
        "• **Tahap 3 — Sinyal Saraf Visual:** Sel-sel di retina mengubah energi cahaya menjadi impuls listrik yang dikirim melalui saraf optik menuju korteks visual di otak.",
        "• **Tahap 4 — Otak Mengenali Makna (*High-Level Understanding*):** Otak manusia memproses tepian, lengkungan, gradasi warna, dan membandingkannya dengan ingatan masa lalu, sehingga kita langsung menyimpulkan makna objek tersebut: ***'Ini adalah Apel Merah yang segar'***.",
        "• **Poin Kunci Perbandingan:** Manusia langsung melompat ke **makna objek**, sedangkan komputer tidak memiliki "
        "tahap ke-4 ini secara bawaan — komputer baru berhenti di tahap pencatatan angka intensitas cahaya (yang nantinya harus dipelajari oleh *Deep Learning*).",
    ],
    8: [
        "**Mekanisme Kamera Digital & Komputer Membaca Gambar (Alur 4 Tahap pada Simulator):**",
        "• **Tahap 1 — Objek di Dunia Nyata (*1. Mata Manusia*):** Objek asli (Apel Merah, Bintang Kuning, atau Rumah) memantulkan cahaya warna-warni ke arah lensa kamera.",
        "• **Tahap 2 — Bukaan Rana Kamera (*2. Katup Kamera / Shutter*):** Saat tombol potret ditekan, katup mekanis/elektronik (*shutter*) kamera terbuka selama sepersekian detik (misal `1/100` detik) untuk mengizinkan cahaya masuk mengenai sensor.",
        "• **Tahap 3 — Perekaman di Sensor (*3. Sensor Cahaya / Pixel Grid*):**",
        "  – Sensor kamera digital (CMOS/CCD) berbentuk papan berpetak yang terdiri dari jutaan kotak sensor mikroskopis (*photodiode / pixel*).",
        "  – Setiap kotak pixel dilengkapi filter warna mikro (*Bayer filter*: Red, Green, Blue) yang mengukur **seberapa kuat intensitas cahaya Merah, Hijau, dan Biru** yang menabrak kotak tersebut.",
        "• **Tahap 4 — Penyimpanan sebagai Matriks Angka (*4. Matriks Angka RGB*):**",
        "  – Besarnya energi cahaya di setiap kotak diubah menjadi angka digital bulat dari **`0` (tidak ada cahaya / gelap total)** hingga **`255` (cahaya penuh / sangat terang)**.",
        "  – Contoh pembacaan 1 titik pixel pada daging apel merah: koordinat `Pixel(x, y)` menyimpan paket 3 angka **`[R: 234, G: 67, B: 53]`** (komponen Merah sangat tinggi `234`, sedangkan Hijau `67` dan Biru `53` rendah).",
        "  – **Kesimpulan Inti:** Di dalam file `.jpg` atau `.png`, sama sekali tidak tersimpan bentuk lingkaran atau konsep 'apel', melainkan murni **tabel raksasa berisi paket 3 angka `[R, G, B]` untuk setiap titik koordinat**.",
    ],
    9: [
        "**Bagaimana Komputer Menampilkan Kembali Angka RGB ke Layar HP/Monitor (Alur 3 Tahap):**",
        "• **Tahap 1 — Nyalakan 3 Lampu Mikro di Dalam 1 Pixel (*Zoom 1000×*):**",
        "  – Jika layar HP atau monitor diperbesar `1000×` dengan mikroskop, setiap **1 kotak pixel layar** ternyata berisi **3 lampu LED super kecil (*sub-pixel*)** yang berjajar rapat: lampu **Merah (R)**, **Hijau (G)**, dan **Biru (B)**.",
        "  – Komputer membaca paket 3 angka dari memori lalu mengatur persentase terangnya ketiga lampu tersebut dengan rumus $\\text{Persentase} = (\\text{Nilai} / 255) \\times 100\\%$.",
        "  – Contoh pada **Apel Merah `[234, 67, 53]`**: Lampu R menyala sangat terang (**`92%`**), Lampu G menyala redup (**`26%`**), dan Lampu B menyala redup (**`21%`**). Karena ketiga lampu mikro ini berhimpitan dalam 1 titik, cahaya ketiganya bercampur di mata kita menjadi **1 titik cahaya berwarna merah**.",
        "  – Contoh pada **Bintang Kuning `[251, 188, 4]`**: Lampu R (`98%`) dan Lampu G (`74%`) sama-sama menyala terang sedangkan B mati (`2%`) → campuran cahaya Merah + Hijau menghasilkan **titik warna kuning**!",
        "• **Tahap 2 — Susun 3 Lapis RGB (*3 Channel Stack*):**",
        "  – Di dalam memori (RAM), angka `234`, `67`, dan `53` tadi tidak disimpan berantakan, melainkan tersusun rapi sebagai **3 lembar matriks 2D yang ditumpuk sejajar (*Lapis R, Lapis G, Lapis B*)**.",
        "  – Untuk menyalakan 1 titik pixel pada koordinat `(112, 88)`, komputer mengambil nilai dari koordinat `(112, 88)` di Lapis R (`234`), Lapis G (`67`), dan Lapis B (`53`).",
        "• **Tahap 3 — Tampil Menjadi Gambar Utuh (*Layar HP*):**",
        "  – Layar modern memiliki jutaan kotak pixel yang bekerja serentak. Ketika dilihat dari jarak baca normal, jutaan titik lampu mikro itu menyatu membentuk **gambar apel, daun, bintang, dan langit yang utuh serta halus**.",
    ],
    10: [
        "**Konsep Dasar Pixel & Resolusi Gambar:**",
        "• **Asal Kata *Pixel*:** Singkatan dari ***Pic**ture **El**ement* (elemen gambar), yaitu unit kotak terkecil dalam citra digital. Satu kotak pixel hanya boleh memiliki **1 warna tunggal yang rata** (tidak bisa setengah merah setengah biru di dalam 1 pixel yang sama).",
        "• **Analogi Kertas Berpetak / Mosaik Keramik:** Membentuk gambar digital di komputer sama seperti menyusun ubin keramik berwarna di atas kertas berpetak. Setiap petak diisi oleh satu ubin warna.",
        "• **Definisi Resolusi (*Spatial Resolution*):** Menyatakan jumlah kolom pixel (lebar / *width*) dikalikan jumlah baris pixel (tinggi / *height*):",
        "  – **`4 × 4` (`16 pixel`):** Hanya ada 16 kotak warna besar. Bentuk apel sama sekali belum dikenali, hanya tampak seperti 4 kotak merah di tengah.",
        "  – **`8 × 8` (`64 pixel`) & `16 × 16` (`256 pixel`):** Siluet bulat apel dan daun mulai terlihat, namun pinggirannya masih tampak bergerigi seperti tangga (*jagged / pixelated*).",
        "  – **`32 × 32` (`1.024 pixel`) & `64 × 64` (`4.096 pixel`):** Ukuran tiap kotak pixel menjadi semakin kecil dan rapat, sehingga lengkungan apel tampak halus.",
        "• **Hubungan dengan Deep Learning:** Semakin tinggi resolusi foto, semakin detail informasi tepi objeknya, namun jumlah angka yang harus dihitung komputer meningkat secara kuadratik. Oleh karena itu, di AI kita memilih titik tengah yang optimal (seperti `224 × 224 = 50.176` pixel).",
    ],
    11: [
        "**Klasifikasi Gambar Berdasarkan Jumlah *Color Channel* (Isi Angka di Tiap Pixel):**",
        "• **1. Satu Channel (`1 Channel` · *Grayscale / Hitam-Putih*):**",
        "  – Setiap kotak pixel hanya menyimpan **1 angka (`0–255`)** yang mengatur intensitas gelap-terang.",
        "  – Sangat ringan dan efisien. Dipakai ketika warna tidak relevan untuk mengenali objek, seperti pada **dataset angka tulisan tangan MNIST**, citra medis Rontgen/CT-Scan/USG, pemindaian teks dokumen (OCR), dan hasil deteksi garis tepi (*Canny edge map*).",
        "• **2. Tiga Channels (`3 Channels` · *RGB — Fokus Utama Project Kita*):**",
        "  – Setiap kotak pixel menyimpan **3 angka (`[R, G, B]`)**. Mampu merepresentasikan $256^3 = 16.777.216$ variasi warna.",
        "  – Merupakan standar universal untuk kamera HP, layar monitor, halaman web, dan **model Deep Learning pengenalan objek (seperti MobileNetV2 & ResNet)**.",
        "  – *Catatan Teknis:* Selain RGB, terdapat palet 3-channel lain untuk keperluan khusus, seperti **HSV** (*Hue, Saturation, Value* — memisahkan warna murni dari terangnya cahaya) serta **LAB / YCbCr**.",
        "• **3. Empat Channels (`4 Channels` · *RGBA & CMYK*):**",
        "  – Menyimpan **4 angka per pixel**. Pada desain grafis/web digunakan format **RGBA** (`Red, Green, Blue, Alpha`), di mana channel ke-4 (*Alpha*) mengatur transparansi (`0` = tembus pandang total seperti latar stiker `.png`, `255` = padat/tidak tembus pandang).",
        "  – Pada mesin cetak/percetakan digunakan format **CMYK** (*Cyan, Magenta, Yellow, Key/Black* — 4 warna tinta fisik printer).",
        "• **4. Lima Channel atau Lebih (`5+ Channels` · *Multispectral & Hyperspectral*):**",
        "  – Menyimpan **5 hingga ratusan angka per pixel**. Menggabungkan 3 channel cahaya tampak (RGB) dengan channel sensor tak kasatmata seperti **NIR (*Near-Infrared* / Inframerah Dekat)** untuk mendeteksi kesehatan klorofil hutan/tanaman, serta **Thermal Infrared** untuk memetakan suhu permukaan bumi atau titik api kebakaran hutan.",
    ],
    12: [
        "**Bedah Matriks 1 Channel (*Grayscale*) pada Grid `8 × 8` Pixel:**",
        "• **Struktur Matriks 2 Dimensi:** Karena hanya memiliki 1 channel, sebuah gambar *grayscale* berukuran `8 × 8` disimpan di Python (NumPy) sebagai tabel 2 dimensi dengan `.shape = (8, 8)` (8 baris ke bawah × 8 kolom ke samping = 64 angka).",
        "• **Aturan Skala Kecerahan (`0` s.d. `255`):**",
        "  – **Nilai `0` = Hitam Pekat:** Tidak ada cahaya sama sekali.",
        "  – **Nilai `255` = Putih Terang:** Cahaya putih maksimal.",
        "  – **Nilai Antara (`1` s.d. `254`) = Derajat Keabuan:** Angka kecil (`30–70`) menghasilkan abu-abu tua/gelap; angka menengah (`110–160`) menghasilkan abu-abu sedang; angka tinggi (`200–245`) menghasilkan abu-abu muda/putih.",
        "• **Bagaimana Bentuk Muncul dari Angka:** Pada contoh grid `8×8` di slide, kotak-kotak di bagian pinggir memiliki angka tinggi **`245`** (tampak sebagai latar putih), sedangkan kotak-kotak yang membentuk pola objek di tengah memiliki angka rendah **`35` s.d. `90`** (tampak sebagai bentuk gelap). Kontras perbedaan angka antara `35` dan `245` inilah yang membentuk siluet gambar.",
    ],
    13: [
        "**Studi Kasus Nyata 1 Channel: Dataset Klasik MNIST (`28 × 28` Grayscale):**",
        "• **Apa itu MNIST?** Singkatan dari *Modified National Institute of Standards and Technology* — dataset berisi 70.000 gambar angka tulisan tangan (`0` sampai `9`) yang dijuluki sebagai *'Hello World'*-nya Deep Learning (digunakan dalam video pembelajaran *3Blue1Brown* dan sudah tersedia lengkap di folder `data/mnist/` kita).",
        "• **Mengapa MNIST Hanya Menggunakan 1 Channel (`28 × 28`)?**",
        "  – Untuk mengenali apakah sebuah tulisan tangan adalah angka `'0'`, `'7'`, atau `'9'`, informasi warna tinta (biru, hitam, atau merah) sama sekali tidak mengubah makna angkanya.",
        "  – Dengan 1 channel *Grayscale* berukuran `28 × 28`, satu gambar hanya membutuhkan **`28 × 28 × 1 = 784` angka**, sehingga sangat ringan untuk dipelajari.",
        "• ** Tiga Mode Pembacaan pada Simulator MNIST di Slide:**",
        "  – **1. Gambar Tulisan Visual:** Tampilan goresan putih/abu-abu di atas latar hitam (`0`).",
        "  – **2. Angka Asli `0–255` (`uint8`):** Menunjukkan bahwa latar hitam bernilai `0`, tengah goresan tebal bernilai `252–255`, dan **pinggiran goresan bernilai abu-abu transisi (`37`, `114`, `190`)** akibat efek *anti-aliasing* saat pemindaian tulisan.",
        "  – **3. Skala Normalisasi `0.0–1.0` (`float32`):** Nilai `0–255` dibagi `255.0` (misal `253` menjadi `0.99`, `128` menjadi `0.50`) — format angka desimal inilah yang masuk ke lapisan input *Neural Network*.",
    ],
    14: [
        "**Fokus Utama ke Format 3 Channels (*RGB*) & Prinsip Pencampuran 3 Cahaya:**",
        "• **Perbandingan Visual Kiri (*Grayscale vs RGB*):**",
        "  – Gambar *Grayscale* (`Shape: (256, 256)`) hanya menyimpan bentuk geometri bintang tetapi kehilangan identitas warna hijaunya.",
        "  – Gambar *RGB* (`Shape: (256, 256, 3)`) menyimpan 3 lapis angka sekaligus sehingga warna hijau bintang, latar, dan bayangannya terekam lengkap.",
        "• **Prinsip Pencampuran Cahaya Aditif (*Additive Color Mixing* — Diagram Kanan):**",
        "  – Layar digital memulai semuanya dari layar mati/gelap (`[0, 0, 0]` = **Hitam**), lalu menambahkan 3 sinar warna primer: **Red (Merah)**, **Green (Hijau)**, dan **Blue (Biru)**.",
        "  – **Merah + Hijau = Kuning** (contoh: `[255, 255, 0]`).",
        "  – **Hijau + Biru = Cyan / Biru Muda** (contoh: `[0, 255, 255]`).",
        "  – **Merah + Biru = Magenta / Ungu Kemerahan** (contoh: `[255, 0, 255]`).",
        "  – **Merah + Hijau + Biru menyala penuh = Putih** (`[255, 255, 255]`).",
    ],
    15: [
        "**Mekanisme Pembentukan Warna pada Simulator Pencampur RGB (`0–255`):**",
        "• Setiap saluran warna (`R`, `G`, `B`) memiliki `256` kemungkinan tingkat kecerahan (`0` sampai `255`).",
        "• Karena ketiganya dapat diatur secara independen, total kombinasi warna yang bisa dibentuk adalah $256 \\times 256 \\times 256 = 16.777.216$ warna.",
        "• **Pola Penting untuk Membaca Angka RGB dengan Cepat:**",
        "  – **Dominasi Satu Channel:** Jika salah satu angka jauh lebih tinggi dari dua lainnya, warnanya mengikuti channel tertinggi tersebut (misal `[234, 67, 53]` → Merah; `[52, 168, 83]` → Hijau; `[66, 133, 244]` → Biru).",
        "  – **Nilai Ketiga Channel Sama Persis (`R = G = B`):** Selalu menghasilkan warna netral tanpa rona warna (Hitam `[0, 0, 0]`, Abu-abu gelap `[60, 60, 60]`, Abu-abu terang `[190, 190, 190]`, hingga Putih `[255, 255, 255]`).",
        "  – **Tingkat Kecerahan Keseluruhan:** Semakin tinggi rata-rata ketiga angka, warna semakin terang/muda (mendekati pastel/putih); semakin rendah ketiga angka, warna semakin tua/gelap (mendekati hitam).",
    ],
    16: [
        "**Analisis Pemisahan (*Channel Splitting*) 1 Foto RGB Menjadi 3 Matriks Tunggal:**",
        "• Pada slide ini ditunjukkan sebuah foto sampel asli: **Persegi Merah** di atas **Latar Belakang Putih** (`persegi_polos_03.jpg`), lalu dipecah menjadi `img[:, :, 0]` (Channel R), `img[:, :, 1]` (Channel G), dan `img[:, :, 2]` (Channel B).",
        "• **Mengapa Masing-Masing Channel Ditampilkan dalam Hitam-Putih (*Grayscale*)?**",
        "  – Ketika satu channel (misal Channel R saja) diambil tersendiri, ia hanya berisi 1 angka per pixel (`0–255`). Dalam visualisasi analisis citra, nilai tinggi (`~255`) digambar sebagai **putih terang**, sedangkan nilai rendah (`~0`) digambar sebagai **hitam gelap**.",
        "• **Cara Membaca Keempat Panel Gambar di Slide:**",
        "  – **Panel 1 (Asli RGB):** Persegi tampak merah menyala, latar belakang putih.",
        "  – **Panel 2 (Channel R / Merah):** Bagian dalam persegi tampak **putih terang** (karena warna merah memiliki nilai `R` sangat tinggi `~230`), dan latar putih juga tampak putih terang (`R ~ 245`).",
        "  – **Panel 3 (Channel G / Hijau):** Bagian dalam persegi tampak **hitam gelap** (karena persegi merah hampir tidak mengandung warna hijau, `G ~ 40`), sedangkan latar belakang putih tetap putih terang (`G ~ 245`).",
        "  – **Panel 4 (Channel B / Biru):** Bagian dalam persegi juga tampak **hitam gelap** (`B ~ 35`), sedangkan latar belakang putih tetap putih terang (`B ~ 245`).",
        "• **Relevansi dengan CNN:** Filter pada *Convolutional Neural Network* membaca ketiga lembar channel ini sekaligus untuk membedakan objek berdasarkan kontras warnanya terhadap latar.",
    ],
    17: [
        "**Pembahasan Tanya-Jawab #1 — Menghitung Total Angka dalam 1 Foto RGB:**",
        "• **Soal:** Sebuah foto berwarna (*RGB*) telah diseragamkan ukurannya menjadi `224 × 224` pixel. Berapa banyak angka yang harus dibaca oleh komputer dari 1 foto ini saja?",
        "• **Pilihan:** A. `224` angka | B. `50.176` angka | **C. `150.528` angka (Jawaban Benar)**.",
        "• **Penjabaran Rumus Dimensi Tensor `(H, W, C)`:**",
        "  – $\\text{Tinggi } (H) = 224$ baris pixel.",
        "  – $\\text{Lebar } (W) = 224$ kolom pixel.",
        "  – Jumlah total titik pixel di permukaan foto = $224 \\times 224 = 50.176$ pixel (ini adalah jawaban pengecoh B, yang hanya benar jika gambarnya 1 channel *Grayscale*).",
        "  – Karena foto berformat **RGB (`C = 3` channels)**, setiap 1 kotak pixel menyimpan 3 nilai (`R, G, B`).",
        "  – Maka total angka di dalam matriks `.shape = (224, 224, 3)` adalah $50.176 \\times 3 = \\mathbf{150.528\\text{ angka}}$.",
        "• **Makna Penting:** Membayangkan `150.528` angka untuk 1 foto membantu kita memahami mengapa manusia mustahil menulis aturan `if-else` manual dan mengapa ukuran foto tidak boleh dibiarkan terlalu besar (misal foto kamera 12 Megapixel = $12.000.000 \\times 3 = 36\\text{ juta}$ angka per foto!).",
    ],
    18: [
        "**Pembahasan Tanya-Jawab #2 — Kapan Informasi Warna (RGB) Menjadi Penentu Utama?**",
        "• **Soal:** Jika mengubah foto menjadi hitam-putih (*Grayscale*) bisa menghemat jumlah angka hingga 3 kali lipat (dari `150.528` menjadi `50.176` angka), mengapa untuk foto objek sehari-hari kita tetap menggunakan **3 Channels (RGB)**?",
        "• **Pilihan:** A. Agar file foto menjadi lebih berat | **B. Karena pada banyak objek, warna adalah ciri pembeda utama (Jawaban Benar)** | C. Karena komputer tidak bisa membaca gambar hitam-putih.",
        "• **Penjelasan Mendalam:**",
        "  – Saat sebuah foto RGB dikonversi ke *Grayscale* (menggunakan rumus luminansi $Y = 0.299R + 0.587G + 0.114B$), tiga angka warna diringkas menjadi satu nilai kecerahan saja.",
        "  – Dua warna yang sangat berbeda di mata manusia — misalnya **Apel Merah** dan **Apel Hijau**, atau kostum karakter berwarna merah vs biru dengan tingkat kecerahan setara — dapat menghasilkan **nilai abu-abu (*grayscale*) yang hampir sama persis (misal sama-sama `~130`)**.",
        "  – Akibatnya, jika bentuk objeknya serupa, model AI yang hanya diberi gambar *Grayscale* akan kehilangan fitur pembeda terpentingnya. Oleh sebab itu, standar input model *Computer Vision* modern tetap mempertahankan **3 Channels (RGB)**.",
    ],
    19: [
        "**Pengantar Bab 2 — Peran AI & Mengapa Perlu Image Processing:**",
        "• Setelah di Bab 1 kita memahami bahwa 1 foto berukuran `224×224` adalah kumpulan `150.528` angka, Bab 2 menjawab dua pertanyaan fundamental:",
        "  – **Bagian A (Slide 20–22 — AI Fundamental):** Bagaimana algoritma AI menemukan pola objek di balik `150.528` angka tersebut, dan apa bedanya *Program Biasa*, *Machine Learning*, serta *Deep Learning*?",
        "  – **Bagian B (Slide 23–29 — Image Processing):** Mengapa foto mentah wajib diseragamkan ukurannya (*Resize Letterbox `224×224`*) dan disetarakan skalanya (*Normalization `float32`*) sebelum diberikan ke AI?",
    ],
    20: [
        "**AI Fundamental (1/3) — Perbandingan 3 Paradigma: Program Biasa vs Machine Learning vs Deep Learning:**",
        "• **1. Program Biasa (*Rule-Based Programming / `if-else`*):**",
        "  – **Cara Kerja:** Programmer manusia merumuskan semua aturan logika secara manual (contoh: `if pixel_tengah == merah and bentuk == bulat: return 'Apel'`).",
        "  – **Kelemahan pada Gambar:** Hanya bekerja pada masalah matematis yang kaku. Pada foto, sedikit perubahan cahaya, sudut kamera, atau posisi objek langsung mengubah ribuan angka pixel sehingga aturan `if-else` runtuh.",
        "• **2. Machine Learning Klasik (*Classical ML* — misal SVM, Random Forest):**",
        "  – **Cara Kerja:** Komputer sudah bisa belajar mencari batas keputusan dari data, **NAMUN manusia masih harus melakukan *Feature Extraction* (ekstraksi ciri) secara manual terlebih dahulu**.",
        "  – **Peran Manusia di ML Klasik:** Engineer manusia harus menulis kode pengukur ciri-ciri gambar (misal: menghitung jumlah sudut lancip, rata-rata nilai R-G-B, rasio panjang-lebar), lalu tabel angka ciri tersebut disuapkan ke algoritma ML. Jika ciri yang dipilih manusia kurang tepat, model ML gagal.",
        "• **3. Deep Learning (*DL / Convolutional Neural Network* — Pendekatan Project Ini):**",
        "  – **Cara Kerja (*End-to-End Learning*):** Manusia **tidak perlu lagi memilih atau merumuskan ciri gambar secara manual**. Manusia cukup menyiapkan **contoh foto yang rapi + label namanya**.",
        "  – **Keunggulan Jaringan Berlapis:** Lapisan-lapisan (*layers*) di dalam *Deep Learning* otomatis belajar mengekstrak ciri secara bertingkat: **Layer Awal** mengenali garis tepi miring/tegak (*edges*) → **Layer Tengah** menggabungkan garis menjadi lengkungan, sudut, dan tekstur → **Layer Akhir** menggabungkan bagian-bagian tersebut untuk mengenali objek utuh!",
    ],
    21: [
        "**AI Fundamental (2/3) — Pembuktian Mengapa Aturan Manual (`if-else`) Gagal pada 5 Kondisi Nyata:**",
        "• Slide ini menguji aturan manual sederhana (`if pixel_tengah(128, 128) == hijau_bintang: tebak 'Bintang'`) melawan model *Deep Learning* pada 5 skenario:",
        "• **Kondisi 1 — Objek Tepat di Tengah & Latar Polos:** Titik tengah `(128, 128)` kebetulan jatuh di badan bintang hijau (`RGB: [38, 176, 65]`). Baik aturan `if-else` maupun AI berhasil menebak *Bintang*.",
        "• **Kondisi 2 — Objek Bergeser (*Translation*):** Bintang masih utuh di dalam foto tetapi posisinya bergeser sedikit ke samping. Kini titik tengah `(128, 128)` mengenai latar belakang putih (`RGB: [238, 244, 240]`). **Aturan `if-else` langsung GAGAL**, sedangkan **AI tetap BERHASIL** karena filter konvolusi memindai seluruh area gambar (*translation invariance*).",
        "• **Kondisi 3 — Objek Miring / Berubah Ukuran (*Rotation & Scale*):** Koordinat ujung-ujung bintang berpindah seluruhnya → aturan posisi koordinat manual gagal, sedangkan AI tetap mengenali pola 5 sudut bintang.",
        "• **Kondisi 4 — Latar Belakang Ramai (*Cluttered Background*):** Banyak bercak warna hijau/biru/merah di latar belakang yang mengecoh aturan pengecekan warna sederhana.",
        "• **Kondisi 5 — Bukti Nyata pada Dataset MNIST Angka `'7'`:**",
        "  – Ditampilkan 2 gambar asli angka `'7'` dari penulis yang berbeda (`data/mnist/variants/`).",
        "  – Pada **Tulisan A**, goresan diagonal angka `'7'` melewati titik pusat `(14, 14)` sehingga nilainya **`253` (putih terang)**.",
        "  – Pada **Tulisan B**, penulis membuat angka `'7'` sedikit lebih lebar sehingga titik pusat `(14, 14)` jatuh di ruang kosong dan bernilai **`0` (hitam pekat)**!",
        "  – Ini membuktikan secara nyata bahwa kita **tidak pernah bisa mendefinisikan gambar objek lewat koordinat pixel tetap**, melainkan harus melalui pembelajaran pola (*Deep Learning*).",
    ],
    22: [
        "**AI Fundamental (3/3) — Posisi P01 dalam Alur Kerja Project (*Pipeline 3 Tahap*):**",
        "• **Tahap 1 — Siapkan & Audit Foto (Fokus Sesi P01 Hari Ini):**",
        "  – Bahan mentah berupa ratusan foto dari kamera HP harus melewati penyaringan kualitas (*EDA & Bab 4*: bebas file rusak, bebas miring EXIF, bebas duplikat bocor) serta *Image Processing* (*Letterbox Resize `224×224`* dan *Normalization `0.0–1.0`*). Outputnya adalah tensor bersih siap latih.",
        "• **Tahap 2 — AI (CNN / MobileNetV2) Belajar Pola (Sesi Berikutnya):**",
        "  – Model *Deep Learning* membaca ratusan contoh foto dari *Train Set* yang sudah seragam, lalu menyesuaikan bobot jaringan sarafnya untuk membedakan ciri tiap kelas.",
        "• **Tahap 3 — AI Menebak Foto Baru (*Inference & Evaluasi Test Set*):**",
        "  – Model yang sudah terlatih diuji dengan foto baru untuk menghasilkan prediksi kelas beserta tingkat keyakinannya (*confidence score*).",
        "• **Perbandingan Skenario A vs Skenario B (*Garbage In, Garbage Out*):**",
        "  – **Skenario A (Dengan P01):** Input seragam `224×224`, proporsi utuh, skala `0.0–1.0` stabil, dan bebas *data leakage* → AI belajar ciri bentuk objek yang sebenarnya.",
        "  – **Skenario B (Tanpa P01):** Foto masuk dalam keadaan miring 90°, gepeng karena ditarik paksa, skala `0–255` mentah, atau bocor duplikat → proses *training* error/tidak stabil dan prediksi model di dunia nyata gagal.",
    ],
    23: [
        "**Tiga Alasan Teknis Mengapa Foto Mentah Wajib Melewati *Preprocessing*:**",
        "• **1. Dimensi Resolusi yang Berbeda-beda (*Non-Uniform Resolution*):**",
        "  – Foto yang dikumpulkan dari berbagai sumber memiliki ukuran berbeda (misal `4000×3000` dari HP A, `1280×720` dari HP B, `500×500` dari unduhan). Arsitektur *Neural Network* memiliki struktur matriks bobot berdimensi tetap sehingga **menolak input yang ukurannya berubah-ubah**.",
        "• **2. Perbedaan Proporsi Lebar-Tinggi (*Aspect RatioMismatch*):**",
        "  – Mengubah foto persegi panjang menjadi bujur sangkar `224×224` secara paksa akan merusak geometri objek (objek bulat menjadi lonjong), sehingga diperlukan teknik *resize* yang mempertahankan proporsi.",
        "• **3. Skala Nilai Pixel Mentah Terlalu Besar (`0–255` dalam `uint8`):**",
        "  – Memasukkan angka ratusan secara langsung ke ribuan perkalian berantai di *Neural Network* dapat menyebabkan nilai aktivasi dan gradien meledak (*exploding gradients*) atau pembelajaran menjadi sangat lambat.",
    ],
    24: [
        "**Alasan 1 Image Processing: *Resize* & *Uniform Resolution (`224 × 224`)*:**",
        "• **Kebutuhan Pemrosesan *Batch* pada GPU:** Saat melatih model *Deep Learning*, komputer tidak memproses foto satu per satu, melainkan menggabungkan puluhan foto sekaligus (misal 32 foto) ke dalam satu blok tensor 4 dimensi berukuran `(32, 224, 224, 3)`. Penggabungan matriks ini secara matematis hanya bisa dilakukan jika setiap foto memiliki tinggi dan lebar yang **identik (`224 × 224`)**.",
        "• **Mengapa Angka `224 × 224`?**",
        "  – Merupakan ukuran standar arsitektur *Transfer Learning* modern (seperti **MobileNetV2**, *ResNet50*, *VGG16*) yang dilatih pada dataset *ImageNet*.",
        "  – Ukuran `224 × 224` dapat dibagi dua secara bulat berkali-kali oleh lapisan *pooling/stride* di dalam CNN ($224 \\rightarrow 112 \\rightarrow 56 \\rightarrow 28 \\rightarrow 14 \\rightarrow 7$).",
        "• **Efisiensi Memori & Kecepatan:** Mengecilkan foto kamera `3000 × 2000` (`6.000.000` pixel) menjadi `224 × 224` (`50.176` pixel) memangkas beban hitungan hingga **~120 kali lebih ringan** sambil tetap mempertahankan bentuk visual objek secara jelas.",
    ],
    25: [
        "**Teknik *Resize* Tanpa Merusak Proporsi (*Aspect Ratio*):**",
        "• **Pengertian *Aspect Ratio*:** Perbandingan antara lebar dan tinggi gambar (contoh: foto `340 × 180` memiliki rasio lebar:tinggi sekitar `16:9`, sedangkan target model AI adalah `224 × 224` atau rasio `1:1`).",
        "• **Perbandingan 3 Metode *Resize* pada Slide:**",
        "  – **1. Gambar Asli (`340 × 180`):** Menampilkan objek **lingkaran biru sempurna** di tengah bidang persegi panjang.",
        "  – **2. Cara Salah — *Stretch / Direct Resize (`224 × 224`)*:** Sisi lebar `340` ditekan paksa ke `224` (menyusut `34%`), sedangkan sisi tinggi `180` ditarik ke `224` (melebar `24%`). Akibatnya, lingkaran sempurna **rusak menjadi elips/lonjong vertikal**!",
        "  – **3. Cara Benar — *Letterbox Padding (`224 × 224`)*:**",
        "    a) Hitung faktor skala terkecil: $r = \\min(224 / W, 224 / H)$ agar sisi terpanjang pas menyentuh `224` (dalam contoh ini menjadi `224 × 118`).",
        "    b) Tempelkan gambar yang sudah dikecilkan secara proporsional tersebut tepat di tengah kanvas bujur sangkar `224 × 224` berwarna netral (abu-abu/hitam), sehingga sisa ruang atas-bawah menjadi bingkai (*letterbox padding*).",
        "    c) **Hasil Akhir:** Ukuran gambar tepat **`224 × 224`** DAN bentuk lingkaran tetap **100% bulat sempurna tanpa terpotong**.",
    ],
    26: [
        "**Pembahasan Tanya-Jawab #3 — Dampak Distorsi *Aspect Ratio* pada AI:**",
        "• **Soal:** Apa yang terjadi pada objek di dalam foto jika foto persegi panjang (*landscape/portrait*) langsung ditarik paksa (*stretch*) menjadi ukuran kotak `224 × 224`?",
        "• **Pilihan:** A. Foto otomatis menjadi lebih tajam | **B. Proporsi bentuk asli objek berubah menjadi gepeng atau lonjong (Jawaban Benar)** | C. Warna foto berubah menjadi hitam-putih.",
        "• **Penjelasan Implikasi ke Model CNN:**",
        "  – Filter konvolusi pada CNN bekerja dengan mengenali geometri lokal (seperti kelengkungan lingkaran, sudut segitiga, atau proporsi wajah karakter).",
        "  – Apabila sebagian foto dipotret *landscape* (lalu gepeng ke samping saat di-*stretch*) dan sebagian lain dipotret *portrait* (lalu gepeng memanjang ke atas saat di-*stretch*), objek yang sama akan tampak memiliki dua bentuk geometri yang berbeda di mata AI, sehingga menurunkan akurasi model secara signifikan.",
    ],
    27: [
        "**Alasan 2 Image Processing: Menyetarakan Skala Angka (*Normalization*):**",
        "• **Mengapa Angka `0–255` Perlu Dinormalisasi?**",
        "  – Di dalam *Neural Network*, setiap nilai pixel akan dikalikan dengan bobot (*weight* $w$) dan dijumlahkan lintas ribuan neuron ($z = \\sum w_i x_i + b$).",
        "  – Jika input $x_i$ bernilai besar (`0` s.d. `255`), hasil penjumlahan $z$ menjadi sangat besar dan tidak seragam, membuat langkah pembaruan bobot (*Gradient Descent*) berosilasi liar dan sulit mencapai titik optimal.",
        "• **Dua Rumus Normalisasi Standar:**",
        "  – **1. Skala `[0.0, 1.0]` (*Min-Max Scaling*):** $\\text{ nilai\\_baru} = \\frac{\\text{pixel}}{255.0}$. Memetakan `0` $\\rightarrow$ `0.0`, `128` $\\rightarrow$ `0.502`, dan `255` $\\rightarrow$ `1.0`. Paling umum dipakai pada model CNN yang dilatih dari awal (*from scratch*).",
        "  – **2. Skala `[−1.0, +1.0]` (*Zero-Centered Scaling*):** $\\text{nilai\\_baru} = \\frac{\\text{pixel}}{127.5} - 1.0$. Memetakan `0` $\\rightarrow$ `−1.0`, `127.5` $\\rightarrow$ `0.0`, dan `255` $\\rightarrow$ `+1.0`. Merupakan skala wajib untuk **MobileNetV2** (melalui fungsi `tf.keras.applications.mobilenet_v2.preprocess_input`).",
    ],
    28: [
        "**Cara Kerja Kalkulator Penyetara Skala & Aturan Emas *Preprocessing*:**",
        "• **Demonstrasi Konversi Angka pada Slide:**",
        "  – Ketika nilai intensitas pixel asli adalah **`0` (Hitam)** $\\rightarrow$ Skala `[0, 1]` = **`0.00`** | Skala `[−1, 1]` = **`−1.00`**.",
        "  – Ketika nilai intensitas pixel asli adalah **`128` (Abu-abu Sedang)** $\\rightarrow$ Skala `[0, 1]` = **`0.50`** ($128/255$) | Skala `[−1, 1]` = **`+0.004`** ($128/127.5 - 1$).",
        "  – Ketika nilai intensitas pixel asli adalah **`255` (Putih Terang)** $\\rightarrow$ Skala `[0, 1]` = **`1.00`** ($255/255$) | Skala `[−1, 1]` = **`+1.00`** ($255/127.5 - 1$).",
        "• **Aturan Emas *Preprocessing* (*Consistency Rule*):**",
        "  – *Preprocessing* yang diterapkan pada foto baru saat **prediksi/ujian (*inference*)** WAJIB **100% identik** dengan *preprocessing* yang diterapkan saat **pelatihan (*training*)**.",
        "  – *Contoh Bug Klasik:* Jika saat *training* foto dibagi `255.0` (model terbiasa membaca angka `0.0–1.0`), lalu saat aplikasi dijalankan kita lupa membagi `255.0` (model tiba-tiba diberi angka `0–255`), maka seluruh perhitungan bobot model akan jenuh (*saturated*) dan menghasilkan tebakan yang salah semua.",
    ],
    29: [
        "**Perbedaan Tipe Data Gambar: `uint8` (Penyimpanan) vs `float32` (Komputasi AI):**",
        "• **1. Tipe Data `uint8` (*Unsigned Integer 8-bit* — Kartu Kiri):**",
        "  – *Unsigned* berarti tidak memiliki tanda negatif; *Integer 8-bit* berarti bilangan bulat yang disimpan menggunakan 8 digit biner ($2^8 = 256$ kemungkinan nilai, yaitu **`0` sampai `255`**).",
        "  – Tidak dapat menyimpan angka koma/desimal (jika `128` dibagi `255` tetap dalam tipe integer, hasilnya terpotong menjadi `0`).",
        "  – Sangat hemat ruang penyimpanan (`1 byte` per angka), sehingga dipakai oleh format file gambar `.jpg` dan `.png`.",
        "• **2. Tipe Data `float32` (*32-bit Floating Point* — Kartu Kanan):**",
        "  – Menyimpan angka pecahan/desimal hingga ~7 digit di belakang koma (misal `0.5019608`).",
        "  – Membutuhkan `4 byte` per angka di RAM/VRAM GPU. Seluruh operasi matriks, fungsi aktivasi (*ReLU, Softmax*), dan perhitungan turunan (*backpropagation*) di TensorFlow/Keras dan PyTorch bekerja menggunakan `float32`.",
        "• **Urutan Kode yang Benar:** Ubah tipe matriks ke `float32` terlebih dahulu dengan `.astype(np.float32)`, baru dibagi dengan `255.0`: `arr_norm = arr_u8.astype(np.float32) / 255.0`.",
    ],
    30: [
        "**Pengantar Bab 3 — Exploratory Data Analysis (EDA) pada Dataset Citra:**",
        "• Jika Bab 1 dan Bab 2 membahas cara membaca dan merapikan **satu buah foto**, maka Bab 3 membahas cara memeriksa kualitas **ratusan foto sekaligus di dalam sebuah dataset** sebelum digunakan untuk melatih model AI.",
        "• Pembahasan EDA di Bab 3 disusun secara sistematis ke dalam **3 *Issue* (masalah utama dataset)** yang paling sering menurunkan performa model *Computer Vision*.",
    ],
    31: [
        "**Konsep & Peta 3 *Issue* Utama dalam *Exploratory Data Analysis (EDA)*:**",
        "• **Apa itu EDA?** Tahap investigasi awal terhadap dataset menggunakan ringkasan statistik dan grafik visual untuk memahami sifat data, menemukan anomali, dan mencegah bias model. Dalam metodologi ilmiah, **EDA bersifat deskriptif** (hanya memotret kondisi data tanpa mengintip kunci ujian *Test Set*).",
        "• **Tiga *Issue* Utama yang Diaudit pada Bab 3:**",
        "  – **Issue #1 — *Class Imbalance* (Keseimbangan Jumlah Foto Antar-Kelas):** Memeriksa tabel distribusi jumlah foto per kelas dan kondisi latar agar model tidak pilih kasih (*bias*) ke kelas mayoritas.",
        "  – **Issue #2 — Pencahayaan & Kontras (*Histogram, Brightness & Contrast*):** Memeriksa sebaran kecerahan piksel untuk mendeteksi foto yang terlalu gelap, terlalu silau, atau terlalu pucat, serta melihat apakah ada perbedaan pencahayaan yang ekstrem antar-kelompok foto.",
        "  – **Issue #3 — Keramaian Latar Belakang (*Edge Density: Latar Polos vs Ramai*):** Mengukur kepadatan garis tepi menggunakan algoritma *Canny Edge Detection* untuk mendeteksi risiko AI mengecoh/menghafal latar belakang (*shortcut learning*).",
    ],
    32: [
        "**Issue #1 EDA — Keseimbangan Jumlah Foto (*Class Imbalance*):**",
        "• **Definisi *Class Imbalance*:** Ketimpangan jumlah foto yang mencolok antar-kategori/kelas di dalam dataset (contoh pada kartu kiri: Kelas A memiliki `90 foto`, sedangkan Kelas B hanya memiliki `10 foto`).",
        "• **Mengapa *Class Imbalance* Berbahaya bagi AI?**",
        "  – Model AI belajar dengan cara meminimalkan jumlah total tebakan yang salah (*loss function*) di seluruh dataset.",
        "  – Jika `90%` isi dataset adalah Kelas A, model yang malas dan **selalu menebak 'Kelas A' untuk semua foto** akan langsung mendapatkan akurasi `90%`, padahal kemampuannya mengenali Kelas B adalah **`0%` (gagal total)**!",
        "• **Hasil Audit pada Dataset Sampel Kita (`119 Foto Valid` — Grafik Kanan):**",
        "  – Dataset kita terdiri dari 5 kelas (`bintang, heksagon, lingkaran, persegi, segitiga`) × 2 kondisi latar (`polos` dan `ramai`).",
        "  – Setiap kombinasi memiliki tepat **`12 foto`** (`12 polos + 12 ramai = 24 foto per kelas`), kecuali `segitiga ramai` yang berjumlah **`11 foto`** karena 1 file rusak disisihkan. Artinya, dataset sampel kita berada dalam kondisi **Seimbang (*Balanced*)**.",
    ],
    33: [
        "**Issue #2 EDA (Bagian 1/2) — Membaca Sebaran Cahaya dengan Grafik Histogram (`65.536` Piksel):**",
        "• **Anatomi Grafik Histogram Citra:**",
        "  – **Sumbu X (`0` s.d. `255`):** Menunjukkan tingkat intensitas/kecerahan piksel dari hitam pekat (`0` di ujung kiri), abu-abu sedang (`85–170` di tengah), hingga putih terang (`255` di ujung kanan). Pada grafik ini, rentang `0–255` dibagi menjadi `32 batang (*bins*)` (setiap batang mewakili rentang 8 angka intensitas).",
        "  – **Sumbu Y (`Jumlah Piksel`):** Menunjukkan berapa banyak titik piksel di dalam foto yang memiliki tingkat kecerahan tersebut. Karena ukuran foto sampel adalah `256 × 256`, maka **jumlah total seluruh batang di dalam 1 grafik selalu berjumlah tepat `256 × 256 = 65.536` piksel**.",
        "  – **Garis Putus-Putus Vertikal (*Mean*):** Menunjukkan titik rata-rata kecerahan (*Brightness*) dari seluruh `65.536` piksel tersebut.",
        "• **Bedah Perbandingan Grafik Kiri (*Contoh Gambar Polos*) vs Grafik Kanan (*Contoh Gambar Ramai*) pada Kondisi Normal (`Offset 0`):**",
        "  – **Gambar Polos (`bintang_polos` · `Mean = 232.2 | Std = 40.1`):** Memiliki satu tiang raksasa setinggi casi `~60.000` piksel di ujung kanan (`235–245`). Hal ini terjadi karena **`93%` area foto adalah latar belakang putih bersih** (Zona Terang `171–255`), sedangkan objek bintang hijau di tengah hanya menyumbang **`5%` Zona Sedang** dan **`2%` Zona Gelap** (garis tepi bintang).",
        "  – **Gambar Ramai (`bintang_ramai` · `Mean = 122.9 | Std = 50.2`):** Bentuk histogramnya seperti bukit lebar di tengah (**`58%` Zona Sedang `85–170`, `25%` Zona Gelap `0–84`, dan `17%` Zona Terang `171–255`**) karena seluruh latar belakangnya dipenuhi bentuk dan corak warna-warni.",
        "• **Analisis Simulasi *Gelap (−90)* vs *Silau (+75)*:**",
        "  – **Mode Gelap (`Offset −90`):** Nilai setiap piksel dikurangi `90` (dibatasi minimum `0`). Seluruh batang histogram bergeser ke dinding kiri (`0`), rata-rata *Mean* turun drastis (Polos ke `142.2`, Ramai ke `37.1`), dan proporsi **Zona Gelap** melonjak tajam.",
        "  – **Mode Silau (`Offset +75`):** Nilai setiap piksel ditambah `75` (mentok maksimum di `255`). Batang histogram menumpuk di dinding kanan `255` (*highlight clipping*) — informasi gradasi warna hilang luntur menjadi putih silau dan simpangan baku (*Std*) menyempit.",
    ],
    34: [
        "**Issue #2 EDA (Bagian 2/2) — Mengukur *Brightness* vs *Contrast* & Membaca Grafik *Boxplot* (`119 Foto Valid`):**",
        "• **1. *Brightness* (Tingkat Terang Keseluruhan · Rumus Python: `np.mean(gray)`):**",
        "  – Menghitung nilai rata-rata dari seluruh piksel (`0–255`) pada satu foto.",
        "  – **Grafik Boxplot Kiri (`Tingkat Terang / Brightness`):** Membandingkan sebaran nilai *Brightness* dari **`60` foto Latar Polos** vs **`59` foto Latar Ramai**.",
        "  – **Temuan Statistik Nyata:** Kelompok **Latar Polos memiliki rata-rata `228.11`** (kotak biru berada tinggi di atas, rentang `~216–240`), sedangkan **Latar Ramai memiliki rata-rata `127.21`** (kotak merah berada di tengah-bawah, rentang `~102–152`).",
        "  – **Efek Geser Slider *Brightness* (`pixel + ΔB`):** Menambah/mengurangi angka konstan ke semua piksel $\\rightarrow$ seluruh kotak pada **Boxplot Kiri** bergeser naik atau turun secara vertikal.",
        "• **2. *Contrast* (Ketajaman Perbedaan Gelap–Terang · Rumus Python: `np.std(gray)`):**",
        "  – Menghitung **Simpangan Baku (*Standard Deviation*)** nilai piksel — seberapa jauh piksel-piksel di dalam foto menyebar dari nilai rata-ratanya.",
        "  – **Grafik Boxplot Kanan (`Ketajaman Beda / Contrast`):** Kelompok **Latar Polos memiliki rata-rata `45.21`**, sedangkan **Latar Ramai memiliki rata-rata `54.69`** (karena latar ramai memuat campuran warna gelap dan warna terang sekaligus).",
        "  – **Efek Geser Slider *Contrast* (`(pixel − mean) × C + mean`):**",
        "    a) Saat **Kontras Rendah (`0.35×`)**: Jarak antara piksel gelap dan terang dipersempit mendekati rata-rata. Perhatikan bahwa **Boxplot Kiri (*Brightness*) hampir tidak berubah**, tetapi **Boxplot Kanan (*Contrast*) anjlok ke `~15–19`** dan foto tampak **pucat berkabut**!",
        "    b) Saat **Kontras Tinggi (`1.60×`)**: Piksel gelap didorong makin hitam dan piksel terang didorong makin putih $\\rightarrow$ **Boxplot Kanan (*Contrast*) naik tinggi** dan batas warna tampak sangat tajam.",
        "• **Peringatan Penting untuk AI:** Karena *Brightness* foto Polos (`228.11`) dan Ramai (`127.21`) berbeda sangat jauh, kita wajib memastikan setiap kelas karakter memiliki foto polos dan ramai yang seimbang agar AI tidak menebak kelas hanya dari terang/gelapnya foto!",
    ],
    35: [
        "**Issue #3 EDA (Bagian 1/4) — Mengukur Keramaian Latar Belakang dengan *Edge Detection*:**",
        "• **Apa itu *Edge* (Garis Tepi) dalam Pengolahan Citra?**",
        "  – *Edge* adalah lokasi piksel di mana terjadi **perubahan intensitas cahaya atau warna secara mendadak/tajam** antara dua piksel yang bertetangga — yang biasanya menandai batas pinggiran suatu objek.",
        "• **Cara Kerja *Sliding Window Kernel `3×3`* (Diagram Animasi Kiri):**",
        "  – Komputer menggeser sebuah matriks pengali kecil berukuran `3 × 3` (contoh: *Sobel Kernel* dengan nilai kolom kiri `[-1, -2, -1]`, tengah `[0, 0, 0]`, dan kanan `[+1, +2, +1]`) melintasi gambar input petak demi petak.",
        "  – Jika area `3×3` yang sedang dipindai warnanya rata/seragam (misal sama-sama latar putih `245`), maka selisih kiri dan kanan adalah **`0` (Bukan Tepi $\\rightarrow$ diberi warna Hitam)**.",
        "  – Jika sisi kiri jendela mengenai latar putih (`245`) dan sisi kanan mengenai objek gelap (`40`), maka hasil perkaliannya menghasilkan selisih besar (**Tepi Terdeteksi! $\\rightarrow$ diberi warna Putih** pada Peta Edge).",
        "• **Metrik *Edge Density* (Kartu Kanan):**",
        "  – Menggunakan algoritma standar **Canny Edge Detector** (`cv2.Canny(gray, 100, 200)`), kita menghitung rasio/proporsi piksel garis putih terhadap seluruh piksel foto:",
        "    $$\\text{Edge Density} = \\frac{\\text{Jumlah Piksel Tepi (Putih)}}{\\text{Total Piksel Gambar (256 \\times 256)}}$$",
        "  – **Latar Polos:** Hanya garis siluet luar objek utama yang terdeteksi $\\rightarrow$ nilai *edge density* sangat rendah.",
        "  – **Latar Ramai:** Garis objek utama bercampur dengan ratusan garis dari corak/benda di latar belakang $\\rightarrow$ nilai *edge density* melonjak tinggi.",
    ],
    36: [
        "**Issue #3 EDA (Bagian 2/4) — Bukti Nyata *Canny Edge Density* pada `119 Foto Valid`:**",
        "• **Perbandingan Visual Langsung (Kiri & Tengah):**",
        "  – **Foto Asli & Canny Latar Polos (`heksagon_polos`):** Pada peta *Canny* berlatar hitam, hanya terlihat 6 garis luar segi enam yang sangat bersih. Nilai **`Edge density = 0.0110`** (hanya `1,10%` dari total piksel yang merupakan garis tepi).",
        "  – **Foto Asli & Canny Latar Ramai (`heksagon_ramai`):** Pada peta *Canny*, garis segi enam di tengah dikepung oleh puluhan garis lingkaran, persegi, dan goresan dari latar belakang. Nilai **`Edge density = 0.0885`** (`8,85%` piksel merupakan garis tepi — **8 kali lipat lebih banyak garis!**).",
        "• **Perbandingan Statistik Seluruh Dataset (`119 Foto Valid` — Grafik Boxplot Kanan):**",
        "  – **Kelompok Latar Polos (`n = 60` foto):** Rata-rata *Edge Density* = **`0.0121`** (`1,21%`), dengan sebaran kotak yang sangat sempit dan konsisten rendah.",
        "  – **Kelompok Latar Ramai (`n = 59` foto):** Rata-rata *Edge Density* = **`0.0853`** (`8,53%`), atau **~7 kali lipat lebih padat** dibanding foto berlatar polos.",
        "• **Makna bagi Model CNN:** Karena lapisan awal CNN berfungsi sebagai pendeteksi garis tepi (*edge detector*), foto berlatar ramai memberikan **7 kali lipat lebih banyak sinyal garis pengecoh (*background noise*)** yang harus disaring oleh model.",
    ],
    37: [
        "**Pembahasan Tanya-Jawab #4 — Mengapa Latar Belakang Ramai Bisa Mengecoh AI (*Shortcut Learning*)?**",
        "• **Skenario Kasus:** Misalkan saat mengumpulkan dataset, seluruh foto **Objek A (Bintang Biru)** diambil di atas **meja kayu yang berantakan**, sedangkan seluruh foto **Objek B (Kotak Hijau)** diambil di depan **tembok putih polos**. Apa risiko terbesarnya saat AI dilatih?",
        "• **Pilihan:** A. AI mengenali bentuk A dan B dengan sempurna | **B. AI 'curang': ia menghafal meja kayu = A, tembok putih = B! (Jawaban Benar)** | C. Foto tidak bisa disimpan.",
        "• **Penjelasan Fenomena *Shortcut Learning / Background Bias*:**",
        "  – Model *Deep Learning* tidak mengetahui mana 'objek utama' dan mana 'latar belakang' kecuali diajarkan melalui variasi data.",
        "  – Karena area latar belakang (meja kayu vs tembok putih) mencakup `>80%` piksel gambar dan perbedaannya sangat mencolok (*edge density* tinggi vs rendah, *brightness* gelap vs terang), jalan pintas matematis termudah bagi AI untuk menebak benar 100% selama latihan adalah dengan **melihat latar belakangnya saja, bukan bentuk objek di tengahnya**.",
        "  – **Bukti Kegagalan Saat Ujian (Diagram Kanan Bawah):** Ketika pada saat ujian **Objek A (Bintang Biru) diletakkan di depan Tembok Putih**, AI yang sudah telanjur menghafal *'Tembok Putih = B'* akan langsung salah menebak gambar tersebut sebagai **'Objek B!'**.",
    ],
    38: [
        "**Issue #3 EDA (Bagian 3/4) — Strategi Desain Dataset & Evaluasi *Polos vs Ramai*:**",
        "• Untuk mencegah jebakan *Shortcut Learning* dan menguji kecerdasan model secara jujur, kita menerapkan 3 strategi metodologis sejak P01:",
        "• **1. Penandaan Kondisi Latar di Metadata (`kondisi: polos / ramai`):**",
        "  – Setiap foto di dalam dataset tidak hanya dicatat label kelasnya (`lingkaran, persegi, segitiga, bintang, heksagon`), tetapi juga label kondisi latarnya (`polos` atau `ramai`).",
        "• **2. Penyeimbangan Silang (*Cross-Condition Balance*):**",
        "  – Setiap kelas wajib memiliki foto berlatar **polos** dan foto berlatar **ramai** dalam proporsi yang seimbang (pada sampel kita: 12 polos + 12 ramai di setiap kelas). Dengan demikian, latar putih maupun latar ramai muncul sama seringnya di semua kelas sehingga AI **dipaksa fokus mencari bentuk objek utamanya**.",
        "• **3. Evaluasi Rapor Terpisah (*Skenario Uji S1 & S2 di Sesi Lanjutan*):**",
        "  – Saat mengevaluasi model pada *Test Set* nanti, kita tidak hanya melihat 1 angka akurasi gabungan, tetapi memisahkan **Akurasi pada Test Polos** vs **Akurasi pada Test Ramai** untuk mengukur seberapa tahan model kita terhadap gangguan latar belakang.",
    ],
    39: [
        "**Issue #3 EDA (Bagian 4/4) — Catatan Metodologis: *Edge Density* adalah Indikator (*Proxy*), Bukan Vonis Mutlak:**",
        "• **Memahami Istilah *Proxy* (Ukuran Pendekatan):**",
        "  – Algoritma *Canny Edge Detection* menghitung **seluruh garis tepi di dalam foto** (baik garis yang berasal dari latar belakang maupun garis yang berada di dalam tubuh objek utama).",
        "• **Dua Penyebab Nilai *Edge Density* Tinggi:**",
        "  – **Kasus 1 (Latar Memang Ramai):** Objeknya sederhana, tetapi pemandangan di belakangnya penuh corak/benda lain.",
        "  – **Kasus 2 (Objek Utamanya Sendiri Bertekstur Detail):** Latarnya putih polos, tetapi objek utamanya memiliki banyak detail garis internal (misalnya karakter dengan pakaian bermotif batik/garis-garis, rambut keriting detail, atau roda gigi).",
        "• **Prinsip Kerja Data Scientist / AI Engineer:**",
        "  – Jangan pernah membuang foto secara membabi buta hanya karena nilai *edge density* atau *brightness*-nya berada di ujung grafik.",
        "  – Gunakan angka statistik dan grafik *Boxplot* sebagai **radar pendeteksi cepat**, kemudian selalu **buka dan lihat sampel fotonya dengan mata manusia** sebelum mengambil keputusan.",
    ],
    40: [
        "**Pengantar Bab 4 — Tiga Jebakan Tersembunyi Kamera HP:**",
        "• Setelah memahami cara mengukur kualitas visual foto di Bab 3, Bab 4 membahas **3 masalah teknis tingkat file** yang selalu muncul saat mengumpulkan dataset foto menggunakan kamera smartphone atau mengunduh dari internet.",
        "• Ketiga jebakan ini (**EXIF Orientation**, **Duplicate / Burst Photos**, dan **Corrupted Files**) wajib dibersihkan pada tahap paling awal sebelum menghitung statistik EDA maupun membagi dataset menjadi *Train/Test Set*.",
    ],
    41: [
        "**Jebakan #1 — *EXIF Orientation*: Mengapa Foto Tegak di Galeri HP Menjadi Miring 90° di Python?**",
        "• **Akar Masalah Teknis (*Hardware Sensor vs Metadata EXIF*):**",
        "  – Sensor kamera fisik di dalam smartphone dipasang dalam satu posisi tetap (umumnya mendatar / *landscape*). Saat pengguna memutar HP menjadi tegak (*portrait*) lalu memotret, kamera sering kali **tidak memutar susunan jutaan pikselnya di memori** agar penyimpanan berlangsung cepat.",
        "  – Sebagai gantinya, sensor gyroscope HP mencatat posisi kemiringan HP ke dalam header metadata file `.jpg` yang disebut **Tag EXIF (*Exchangeable Image File Format*)**, misalnya **`Orientation = 6` (*Rotate 90° Clockwise*)**.",
        "• **Mengapa Terlihat Berbeda di Galeri HP vs Kode Python?**",
        "  – Aplikasi Galeri HP dan File Explorer membaca tag `EXIF Orientation = 6` lalu memutar tampilan foto secara otomatis di layar sehingga tampak **tegak normal**.",
        "  – Sebaliknya, pustaka pemrograman (`Image.open()` tanpa transpose atau `cv2.imread()`) membaca baris-demi-baris matriks piksel mentah langsung dari file dan mengabaikan tag EXIF $\\rightarrow$ **foto masuk ke model AI dalam posisi tertidur miring 90°!**",
        "• **Solusi Permanen di Kode:** Gunakan fungsi **`ImageOps.exif_transpose(img)`** dari pustaka `Pillow` setiap kali memuat gambar. Fungsi ini membaca tag EXIF, memutar matriks piksel secara fisik ke arah yang benar, lalu menghapus tag rotasinya. Pada dataset sampel kita, terdapat **2 file ber-EXIF=6** (`persegi_polos_01.jpg` dan `bintang_ramai_01.jpg`).",
    ],
    42: [
        "**Jebakan #2 — *Duplicate Images* (Foto Kembar Identik) & *Burst Photos* (Jepretan Beruntun):**",
        "• **1. *Exact Duplicate Images* (Kembar Identik 100%):**",
        "  – Terjadi ketika file yang sama tersalin dua kali dengan nama berbeda (misal `lingkaran_polos_01.jpg` dan `lingkaran_polos_02.jpg`, atau hasil pengunduhan berulang).",
        "  – **Cara Deteksi:** Jangan mengecek dari nama file, melainkan hitung sidik jari isi byte file menggunakan algoritma **Cryptographic Hash `SHA-256`**. Jika dua file menghasilkan kode `SHA-256` yang sama, salah satunya wajib disisihkan.",
        "• **2. *Burst Photos / Near-Duplicates* (Foto Beruntun dari Sesi yang Sama):**",
        "  – Terjadi ketika pengguna menekan tombol kamera berkali-kali dalam waktu singkat pada objek dan latar yang sama. Nilai pikselnya bergeser sedikit (sehingga kode `SHA-256`-nya berbeda), namun secara visual gambarnya `98%` kembar.",
        "  – **Cara Penanganan:** Catat identitas sesi pemotretan (**`id_sesi`**) pada `metadata.csv`. Saat membagi dataset menjadi *Train Set* dan *Test Set* nanti (di sesi *Data Splitting*), gunakan **Group Split berdasarkan `id_sesi`** agar foto-foto dari sesi pemotretan yang sama tidak pernah terpecah antara latihan dan ujian.",
    ],
    43: [
        "**Jebakan #3 — *Corrupted Files* (Satu File Rusak Menghentikan Seluruh Proses Training):**",
        "• **Apa itu *Corrupted Image File*?**",
        "  – File berekstensi `.jpg` atau `.png` yang struktur datanya tidak lengkap atau rusak — misalnya akibat proses unduh/salin yang terputus di tengah jalan (*Truncated File Read*), file kosong (`0 KB`), atau file dokumen/halaman HTML error yang salah disimpan dengan akhiran `.jpg`.",
        "• **Mengapa Sangat Berbahaya?**",
        "  – Proses pelatihan (*training*) model Deep Learning dapat berjalan selama puluhan menit hingga berjam-jam membaca ribuan foto secara berurutan.",
        "  – Jika di tengah antrean terdapat **1 saja *corrupted file*** yang belum disaring, pustaka pembaca gambar akan melempar *fatal error (`OSError / UnidentifiedImageError`)* dan **menghentikan paksa seluruh proses training yang sedang berjalan!**",
        "• **Alur Pencegahan Otomatis (Diagram Kanan):**",
        "  – Sebelum menghitung statistik EDA maupun melatih AI, jalankan fungsi verifikasi (`img.verify()`) pada seluruh file di folder dataset.",
        "  – Pada dataset sampel kita (`120 file`), pemindaian otomatis menemukan **1 file rusak (`segitiga/ramai/segitiga_ramai_12.jpg`)** dan langsung menyisihkannya sehingga hanya **`119 foto valid`** yang diteruskan ke tahap analisis.",
    ],
    44: [
        "**Pembahasan Tanya-Jawab #5 — Bahaya *Data Leakage* (Kebocoran Data Ujian AI):**",
        "• **Soal:** Kita memiliki 2 *duplicate images* (foto kembar). Satu foto masuk ke **Train Set** (bahan latihan AI), dan kembarannya masuk ke **Test Set** (soal ujian AI). Mengapa hal ini sangat berbahaya?",
        "• **Pilihan:** A. Komputer akan hang | **B. Nilai ujian AI terlihat 100% pintar, padahal ia cuma menghafal! (Jawaban Benar)** | C. Tidak berpengaruh apa-apa.",
        "• **Penjelasan Mendalam tentang *Data Leakage*:**",
        "  – Tujuan utama dari **Test Set** adalah mengukur kemampuan **generalisasi** model AI — yakni seberapa pintar model menebak foto baru yang **belum pernah ia lihat sama sekali** selama latihan.",
        "  – Jika foto di *Test Set* ternyata adalah kembaran identik (`Hash: a94f...`) atau foto *burst* dari foto yang sudah ada di *Train Set*, itu sama saja seperti **membocorkan soal ujian persis sama dengan soal latihan di kelas**.",
        "  – **Akibatnya (*Inflated Accuracy*):** Saat dievaluasi di laboratorium, rapor akurasi *Test Set* tampak sempurna (`~99–100%`). Namun ketika model tersebut dirilis ke pengguna nyata dan bertemu foto baru yang sesungguhnya, akurasinya langsung anjlok drastis.",
    ],
    45: [
        "**Empat Aturan Emas (*Golden Rules*) Menjaga Kejujuran & Kualitas Data:**",
        "• **1. Hapus *Duplicate* Sebelum *Split* (*Deduplicate First*):**",
        "  – Pemeriksaan hash `SHA-256` dan pembuangan foto kembar wajib dilakukan pada tahap inventarisasi awal **sebelum** dataset dibagi menjadi *Train Set*, *Validation Set*, dan *Test Set*.",
        "• **2. Jaga *Group* Sesi Foto (*Group-Aware Splitting*):**",
        "  – Semua foto yang diambil dari satu momen/sesi pemotretan yang sama (`id_sesi`) harus dikunci dalam satu paket: semuanya masuk ke *Train Set* ATAU semuanya masuk ke *Test Set* (tidak boleh menyeberang).",
        "• **3. *Test Set* Disimpan Rapat (*Hold-out Test Set Discipline*):**",
        "  – Seluruh keputusan pembersihan data, normalisasi, dan penentuan parameter harus didasarkan pada *EDA* dan *Train/Validation Set*. *Test Set* hanya dibuka satu kali di akhir untuk penilaian rapor final.",
        "• **4. Catat Semua Pembersihan (*Transparent Audit Trail*):**",
        "  – Jangan menghapus file mentah secara diam-diam tanpa catatan. Simpan tabel audit lengkap (`p01_audit_metadata.csv`) yang mencatat status setiap file (`is_valid`, `is_duplicate`, `sha256`, `error`) agar eksperimen ilmiah dapat dipertanggungjawabkan.",
    ],
    46: [
        "**Pengantar Bab 5 — Praktik Hands-on Notebook, Diskusi Kasus & Uji Pemahaman:**",
        "• Bab 5 menerjemahkan seluruh konsep visual dari Bab 1–4 ke dalam **praktik pemrograman Python yang ramah pemula (*awam-friendly*)**.",
        "• Di dalam file `P01_understanding_images_processing_eda.ipynb`, kode telah dipecah menjadi sel-sel pendek (*cell-by-cell*, satu sel fokus pada satu langkah) lengkap dengan komentar penjelasan Bahasa Indonesia (`# ...`) di setiap barisnya.",
    ],
    47: [
        "**Peta Detail 6 Langkah Praktik di Notebook (`50 Menit` — Sinkron 1-ke-1 dengan Bab 1–4):**",
        "• **Langkah 01 — Baca Gambar & Intip Matriks Pixel (Bab 1 · `8 menit`):**",
        "  – Membuka 1 foto sampel (`bintang_polos_01.jpg`), mencetak ukuran `(Lebar, Tinggi)` di Pillow vs `.shape = (256, 256, 3)` dan `.dtype = uint8` di NumPy (`# TODO 1`).",
        "  – Memotong area kecil `8×8` pixel di tengah foto untuk menampilkan nilai angka `0–255` di atas setiap kotak pixel, serta memuat **dataset asli MNIST (`28×28 = 784` angka)** dari folder `data/mnist/`.",
        "• **Langkah 02 — Pisahkan RGB Channels & Grayscale (Bab 1 · `7 menit`):**",
        "  – Memisahkan 3 lapisan warna `R = arr[:, :, 0]`, `G = arr[:, :, 1]`, `B = arr[:, :, 2]` (`# TODO 2A`) dan mengubah foto berwarna ke 1 channel *Grayscale* dengan `img.convert('L')` (`# TODO 2B`).",
        "• **Langkah 03 — Bukti AI Fundamental, Resize Letterbox & Normalization (Bab 2 · `8 menit`):**",
        "  – Membuktikan lewat kode bahwa nilai RGB titik tengah `(128, 128)` berubah drastis dari `[38, 176, 65]` menjadi `[238, 244, 240]` saat foto bintang digeser 45 pixel (alasan `if-else` gagal).",
        "  – Membuat fungsi `resize_with_letterbox()` ke `224×224` (`# TODO 3A`) dan menormalisasi array ke `float32` skala `0.0–1.0` (`# TODO 3B`).",
        "• **Langkah 04 — Saring 3 Jebakan Kamera HP (Bab 4 · `10 menit`):**",
        "  – Membuat 3 fungsi penyaring: `load_image_exif_safe()` (`# TODO 4A`), `check_image_integrity()` dengan `verify()` (`# TODO 4B`), dan `compute_sha256()` (`# TODO 4C`), lalu memindai seluruh `120 file` untuk menghasilkan tabel `df_audit` (`119 valid`, `1 corrupted`, `1 duplicate`).",
        "• **Langkah 05 — EDA Kesehatan Dataset: Polos vs Ramai (Bab 3 · `12 menit`):**",
        "  – Memeriksa *Class Balance* dengan `pd.crosstab()`, menghitung *Brightness* (`np.mean`), *Contrast* (`np.std`), *3 Zona Cahaya*, dan *Edge Density* (`cv2.Canny`) untuk seluruh 119 foto valid (`# TODO 5`).",
        "• **Langkah 06 — Simpan Ringkasan Audit & Grafik Boxplot (`5 menit`):**",
        "  – Merangkum tabel statistik `groupby('condition')`, menggambar 3 panel *Boxplot (Brightness, Contrast, Edge Density)*, dan menyimpan file CSV serta PNG ke folder `results/`.",
    ],
    48: [
        "**Bedah Kode Python di Balik Layar (1/2) — Cek *Corrupted File* & Koreksi *EXIF* dengan `Pillow`:**",
        "• **Mengapa `Image.open()` Dipanggil Dua Kali di Dalam Kode?**",
        "  – **Panggilan Pertama (`with Image.open(lokasi_foto) as img: img.verify()`):**",
        "    Fungsi `img.verify()` membaca dan memeriksa struktur internal file JPEG/PNG untuk memastikan file tidak rusak/terpotong. Karena cara kerja internal `Pillow`, setelah `verify()` dijalankan, pointer file ditutup sehingga objek `img` tersebut tidak bisa langsung dipakai mengambil gambar.",
        "  – **Panggilan Kedua (`with Image.open(lokasi_foto) as img: img = ImageOps.exif_transpose(img).convert('RGB')`):**",
        "    Setelah file terbukti utuh (tidak melempar *error*), file dibuka kembali untuk: (1) Diputar otomatis matriks pikselnya sesuai tag orientasi kamera HP (`exif_transpose`), dan (2) Dikonversi ke mode warna standar 3 channel (`convert('RGB')`) untuk mengantisipasi jika ada file `.png` 4 channel (RGBA) atau 1 channel (L) yang terselip.",
    ],
    49: [
        "**Bedah Kode Python di Balik Layar (2/2) — Mendeteksi *Duplicate Images* dengan `hashlib.sha256`:**",
        "• **Baris demi Baris Fungsi `get_file_hash(lokasi_foto)`:**",
        "  – **`open(lokasi_foto, 'rb').read()`:** Membuka file foto dalam mode **`'rb'` (*Read Binary*)** — membaca deretan byte mentah file dari awal hingga akhir tanpa mengubahnya.",
        "  – **`hashlib.sha256(isi).hexdigest()`:** Memasukkan seluruh byte file ke dalam algoritma kriptografi **SHA-256 (*Secure Hash Algorithm 256-bit*)** dan mengeluarkan hasilnya dalam bentuk teks heksadesimal sepanjang **64 karakter** (contoh: `a3f9c2...`).",
        "• **Keunggulan Pendeteksian dengan SHA-256:**",
        "  – **Sensitivitas Tinggi (*Avalanche Effect*):** Jika ada 1 byte saja yang berbeda di dalam file, kode 64 karakter yang dihasilkan akan berubah total.",
        "  – **Kebal terhadap Perubahan Nama File:** Walaupun `foto_a.jpg` disalin dan diganti namanya menjadi `copy_b.jpg` di folder lain, selama isinya kembar identik, keduanya pasti menghasilkan kode `SHA-256` yang sama persis (`a3f9c2...`).",
    ],
    50: [
        "**Pembahasan Mendalam *Mini-Challenge*: Diskusi Detektif Data (*Polos vs Ramai*):**",
        "• **Fakta Statistik Hasil Eksekusi 119 Foto Valid (Kartu Kiri):**",
        "  – **Latar Polos (`60 foto`):** Rata-rata *Brightness* = **`228.11`** (sangat terang/putih), *Contrast* = **`45.21`**, *Edge Density* = **`0.0121`** (`1,21%` piksel tepi).",
        "  – **Latar Ramai (`59 foto`):** Rata-rata *Brightness* = **`127.21`** (sedang), *Contrast* = **`54.69`**, *Edge Density* = **`0.0853`** (`8,53%` piksel tepi — **~7 kali lipat lebih tinggi!**).",
        "• **Analisis Jawaban untuk 3 Pertanyaan Diskusi (Kartu Kanan):**",
        "  – **1. Kondisi mana yang lebih sulit ditebak oleh AI dan mengapa?**",
        "    Kondisi **Latar Ramai** jauh lebih sulit. Dengan *edge density* ~7× lebih tinggi (`0.0853` vs `0.0121`), terdapat ribuan garis tepi dari corak latar belakang yang menempel langsung dengan garis tepi objek utama, sehingga model AI lebih sulit memisahkan batas objek dari latarnya.",
        "  – **2. Apa yang terjadi jika AI hanya dilatih menggunakan foto Latar Polos?**",
        "    Model AI akan terbiasa bahwa *'latar belakang selalu bernilai ~240 (putih bersih) dan setiap garis tepi yang muncul pasti milik objek utama'*. Begitu diuji dengan foto **Latar Ramai**, model akan kebingungan oleh ribuan garis latar belakang dan akurasinya akan anjlok drastis (*poor generalization*).",
        "  – **3. Apa strategi agar AI pintar di kedua kondisi sekaligus?**",
        "    a) Latih model menggunakan **campuran foto Polos dan Ramai yang seimbang** di dalam *Train Set* (skenario eksperimen lengkap).",
        "    b) Terapkan **Data Augmentation** (variasi rotasi, kecerahan, kontras) hanya pada *Train Set* di sesi pelatihan berikutnya.",
        "    c) Evaluasi performa model pada *Test Set Polos* dan *Test Set Ramai* secara terpisah untuk memverifikasi ketangguhan model.",
    ],
    51: [
        "**Penjelasan Detail Glosarium Bagian 1/2 (5 Istilah Dasar Gambar & AI):**",
        "• **1. Pixel (*Picture Element*):** Elemen kotak terkecil penyusun citra digital. Setiap pixel menyimpan nilai numerik intensitas cahaya (`0` = gelap total s.d. `255` = terang penuh).",
        "• **2. RGB & Grayscale:** Dua format *color channel* paling utama. **RGB** menggunakan 3 channel warna primer cahaya (*Red, Green, Blue* $\\rightarrow$ 3 angka per pixel) untuk foto berwarna; **Grayscale** menggunakan 1 channel gelap-terang (1 angka per pixel) seperti pada dataset MNIST.",
        "• **3. Deep Learning (AI):** Sub-bidang *Machine Learning* yang menggunakan jaringan saraf tiruan berlapis banyak (*deep neural networks*, seperti CNN) untuk mengekstrak hierarki fitur visual (garis tepi $\\rightarrow$ bentuk $\\rightarrow$ objek) secara otomatis langsung dari data piksel.",
        "• **4. Resolution (Resolusi Spasial):** Dimensi jumlah kolom (lebar) × baris (tinggi) pixel yang menyusun sebuah gambar. Sebelum masuk ke model CNN seperti MobileNetV2, resolusi seluruh foto diseragamkan ke `224 × 224` pixel.",
        "• **5. Aspect Ratio (Rasio Aspek):** Perbandingan proporsional antara lebar dan tinggi gambar ($W : H$). Wajib dijaga menggunakan teknik *Letterbox Padding* saat proses *resize* agar bentuk geometri objek tidak mengalami distorsi (gepeng atau lonjong).",
    ],
    52: [
        "**Penjelasan Detail Glosarium Bagian 2/2 (5 Istilah *Image Processing & EDA*):**",
        "• **6. Normalization (Normalisasi Skala Pixel):** Proses mengubah skala nilai pixel dari bilangan bulat `0–255` (`uint8`) menjadi bilangan desimal kecil seperti `0.0–1.0` ($\text{pixel}/255.0$) atau `−1.0 s.d. +1.0` (`float32`) agar komputasi gradien pada pelatihan AI berjalan stabil.",
        "• **7. EDA (*Exploratory Data Analysis*):** Tahap pemeriksaan dan pemetaan kualitas dataset secara deskriptif (meliputi audit distribusi kelas, ukuran, pencahayaan, kontras, dan kompleksitas latar) sebelum melakukan pelatihan model.",
        "• **8. Histogram (Histogram Intensitas Citra):** Grafik distribusi frekuensi yang menampilkan jumlah piksel untuk setiap tingkat kecerahan dari `0` (sisi kiri / gelap) hingga `255` (sisi kanan / terang).",
        "• **9. Edge Density (Kepadatan Garis Tepi):** Proporsi jumlah piksel yang terdeteksi sebagai garis tepi (menggunakan algoritma seperti *Canny Edge Detector*) dibandingkan terhadap total seluruh piksel gambar; digunakan sebagai indikator (*proxy*) tingkat keramaian visual/latar.",
        "• **10. EXIF & Hash (`SHA-256`):** **EXIF** adalah metadata yang disematkan kamera HP (termasuk tag orientasi rotasi `Orientation = 6`); sedangkan **Hash (`SHA-256`)** adalah kode sidik jari digital 64 karakter yang dihitung dari isi byte file untuk mendeteksi file kembar (*exact duplicates*).",
    ],
    53: [
        "**Pembahasan Detail Kuis Evaluasi — Soal 1 & Soal 2:**",
        "• **SOAL 1 (Cara Komputer Melihat Gambar):**",
        "  – *Pertanyaan:* Apa yang sebenarnya dilihat komputer saat membaca sebuah foto?",
        "  – *Opsi:* A. Bentuk benda secara langsung seperti mata manusia | **B. Matriks pixel berisi nilai intensitas `0–255` (Jawaban Benar)** | C. Rekaman suara kamera.",
        "  – *Penjelasan Konsep:* Komputer tidak memiliki persepsi visual bawaan; file gambar di memori selalu direpresentasikan sebagai array/tensor angka intensitas `0–255` berukuran `(H, W, C)`.",
        "• **SOAL 2 (Pencampuran Warna Cahaya RGB):**",
        "  – *Pertanyaan:* Jika sebuah titik pixel memiliki nilai `RGB = (255, 255, 255)`, warna apa yang tampil di layar?",
        "  – *Opsi:* A. Hitam pekat | B. Grayscale gelap | **C. Putih terang (Jawaban Benar)**.",
        "  – *Penjelasan Konsep:* Layar menggunakan sistem warna aditif (*additive color*). Nilai `(0, 0, 0)` berarti ketiga lampu sub-pixel mati (Hitam), sedangkan `(255, 255, 255)` berarti ketiga lampu Merah, Hijau, dan Biru menyala dengan intensitas maksimum secara bersamaan sehingga menghasilkan cahaya **Putih terang**.",
    ],
    54: [
        "**Pembahasan Detail Kuis Evaluasi — Soal 3 & Soal 4:**",
        "• **SOAL 3 (Tujuan *Resize Proporsional & Normalization*):**",
        "  – *Pertanyaan:* Mengapa kita perlu mengecilkan foto secara proporsional & menyamakan skalanya ke `0–1`?",
        "  – *Opsi:* **A. Agar *aspect ratio* tidak terdistorsi dan *training* AI lebih stabil (Jawaban Benar)** | B. Agar foto berubah menjadi *grayscale* | C. Agar ukuran file menjadi lebih berat.",
        "  – *Penjelasan Konsep:* Menjaga proporsi (*Letterbox Padding*) memastikan bentuk geometri objek tidak gepeng/lonjong, sedangkan normalisasi ke `0.0–1.0` (`float32`) mencegah ledakan nilai pada perkalian bobot jaringan saraf.",
        "• **SOAL 4 (Jebakan Kamera HP — *EXIF Orientation*):**",
        "  – *Pertanyaan:* Mengapa foto yang terlihat tegak di galeri HP kadang tampak miring / tertidur (*rotated*) saat dibaca langsung oleh program komputer?",
        "  – *Opsi:* A. Karena ukuran fotonya terlalu kecil | **B. Karena komputer mengabaikan metadata *EXIF orientation* dari kamera HP (Jawaban Benar)** | C. Karena fotonya berlatar belakang polos.",
        "  – *Penjelasan Konsep:* Kamera HP menyimpan matriks piksel dalam orientasi sensor fisik (mendatar) dan hanya menulis instruksi rotasi di tag EXIF. Tanpa memanggil `ImageOps.exif_transpose()`, Python membaca matriks mentah tersebut dalam keadaan miring 90°.",
    ],
    55: [
        "**Pembahasan Detail Kuis Evaluasi — Soal 5 (Penentu Kejujuran Data):**",
        "• **SOAL 5 (Bahaya *Duplicate Images* & *Data Leakage*):**",
        "  – *Pertanyaan:* Apa bahayanya jika foto *duplicate* (kembar) dibiarkan masuk ke *Train Set* dan *Test Set* sekaligus?",
        "  – *Opsi:* A. AI akan menolak membuka gambar tersebut | **B. Nilai ujian AI mengalami *inflated accuracy* akibat *data leakage* (Jawaban Benar)** | C. Gambar akan otomatis terhapus oleh komputer.",
        "  – *Penjelasan Konsep & Diagram Kanan:*",
        "    a) Ketika file yang sama (`foto1.jpg` di *Train Set* dan salinan kembarnya di *Test Set*) lolos tanpa disaring dengan hash `SHA-256`, terjadi kebocoran data ujian (**Data Leakage**).",
        "    b) Akibatnya, skor evaluasi pada *Test Set* mengalami **Inflated Accuracy** (akurasi melambung tinggi secara palsu hingga `~100%`) karena model diuji menggunakan soal yang sudah pernah dihafalnya.",
        "    c) Namun saat model tersebut berhadapan dengan **Foto Baru Asli** di dunia nyata, performanya langsung anjlok/gagal.",
    ],
    56: [
        "**Rangkuman 3 Poin Utama (*Keynote Takeaways*) Sesi P01:**",
        "• **01 · Image = Pixel Matrix (Bab 1):**",
        "  – Mata manusia melihat bentuk dan makna objek, sedangkan komputer membaca tensor angka intensitas `0–255`.",
        "  – Gambar 1 channel (*Grayscale*, seperti MNIST `28×28 = 784` angka) menyimpan 1 nilai gelap-terang per pixel; gambar 3 channels (*RGB*, `224×224×3 = 150.528` angka) menyimpan 3 lapisan warna `[R, G, B]` yang menyalakan 3 lampu sub-pixel di layar.",
        "• **02 · AI Butuh Bahan yang Rapi — *Image Processing* (Bab 2):**",
        "  – Aturan manual `if-else` gagal menangani pergeseran posisi, rotasi, dan variasi latar pada foto, sehingga kita membutuhkan **Deep Learning** yang mempelajari pola dari contoh gambar.",
        "  – Sebelum masuk ke AI, setiap foto wajib diseragamkan ukurannya ke **`224 × 224`** tanpa gepeng (**Letterbox Padding**) dan dikonversi dari `uint8 (0–255)` ke **`float32` skala `0.0–1.0`** (**Normalization**).",
        "• **03 · Exploratory Data Analysis / EDA & Kebersihan Data (Bab 3 & Bab 4):**",
        "  – Selalu audit 3 isu utama dataset: **Issue #1** (*Class Imbalance*), **Issue #2** (*Histogram, Brightness `np.mean`, Contrast `np.std`*), dan **Issue #3** (*Canny Edge Density: Latar Polos vs Ramai*).",
        "  – Saring 3 jebakan kamera HP sejak awal: putar orientasi **EXIF** (`exif_transpose`), sisihkan **Corrupted Files** (`verify()`), dan bersihkan **Duplicate Images** (`SHA-256`) untuk mencegah **Data Leakage**.",
    ],
    57: [
        "**Makna Kutipan Penutup (*Closing Quote*) & Jembatan Menuju Sesi P02:**",
        "• **Inti Kutipan:** *'Data yang bersih melahirkan model yang cerdas, sedangkan Image Processing & EDA memastikan AI belajar dari pola yang benar.'*",
        "  – Dalam proyek *Deep Learning* dunia nyata, kualitas dan kejujuran data menyumbang porsi keberhasilan yang jauh lebih besar daripada sekadar mengganti-ganti arsitektur model.",
        "• **Keterkaitan Langsung dengan Sesi Berikutnya (P02 — Teori Neural Network / ANN):**",
        "  – Pada akhir sesi P01 hari ini, kita telah berhasil mengubah 1 foto mentah menjadi deretan **`150.528` angka desimal (`0.0–1.0`)** yang bersih, tegak, proporsional, dan bebas bocor.",
        "  – Pertanyaan selanjutnya yang akan dijawab di **Sesi P02**: *Bagaimana sebuah Jaringan Saraf Tiruan (Artificial Neural Network) menerima `150.528` angka desimal tersebut, mengalikan dengan bobot (weights) dan bias, melewati fungsi aktivasi (ReLU & Softmax), menghitung kesalahan (Loss Function), hingga bisa menebak nama objeknya dengan tepat?*",
    ],
    58: [
        "**Penjelasan Panduan Referensi Belajar Mandiri Bagian 1/2 (Urutan 1 s.d. 8):**",
        "• **Tahap 1 — Piksel & NumPy (Pendalaman Bab 1):**",
        "  – **1. *3Blue1Brown — But what is a neural network? (Ch. 1)*:** Wajib ditonton pada menit `00:00–05:30` karena memperlihatkan animasi visual bagaimana gambar angka tulisan tangan **MNIST (`28 × 28 = 784` pixel)** dengan nilai `0.0–1.0` masuk ke lapisan neuron pertama.",
        "  – **2. *Keith Galli — Complete Python NumPy Tutorial*:** Panduan memanipulasi array/matriks di Python (`.shape`, *slicing* `arr[y, x]`, dan konversi tipe `.astype('float32')`).",
        "• **Tahap 2 — AI Fundamental (Pendalaman Bab 2):**",
        "  – **3. *IBM Technology — AI, ML, DL & GenAI Explained*:** Menjelaskan hierarki perbedaan antara *Artificial Intelligence*, *Machine Learning* klasik (ekstraksi ciri manual), dan *Deep Learning* (jaringan saraf berlapis).",
        "  – **4 & 5. *Simplilearn — Deep Learning & What is AI in 5 Minutes*:** Ringkasan konsep dasar bagi pemula.",
        "• **Tahap 3 — Pustaka Pillow & OpenCV (Pendalaman Praktik Notebook):**",
        "  – **6. *Corey Schafer — Python Pillow Tutorial*:** Cara membuka, memutar, mengubah ukuran (*resize*), dan menyimpan file gambar menggunakan `PIL / Pillow`.",
        "  – **7 & 8. *freeCodeCamp & Murtaza's Workshop — OpenCV Python Course*:** Cara membaca matriks gambar, memisahkan channel warna, menggambar histogram, dan menjalankan deteksi tepi *Canny* dengan `cv2`.",
    ],
    59: [
        "**Penjelasan Panduan Referensi Belajar Mandiri Bagian 2/2 (Urutan 9 s.d. 15):**",
        "• **Tahap 4 — Filter, Kernel `3×3` & Deteksi Tepi Canny (Pendalaman Bab 3 EDA):**",
        "  – Tiga video demonstrasi visual dari **Computerphile (bersama Dr. Mike Pound)** yang sangat direkomendasikan karena menjadi jembatan langsung menuju konsep konvolusi CNN di sesi berikutnya:",
        "  – **9. *How Blurs & Filters Work*:** Menjelaskan cara kerja jendela geser (*sliding window kernel 3×3*) di atas matriks piksel.",
        "  – **10. *Finding the Edges (Sobel Operator)*:** Menjelaskan bagaimana kernel `[-1, 0, +1]` menghitung selisih kecerahan kiri-kanan dan atas-bawah untuk menemukan garis batas objek.",
        "  – **11. *Canny Edge Detector*:** Menjelaskan algoritma lengkap di balik fungsi `cv2.Canny(gray, 100, 200)` yang kita gunakan untuk menghitung `edge_density` pada foto *Polos vs Ramai*.",
        "  – **12. *DigitalSreeni — Python for Microscopists (GitHub)*:** Kumpulan skrip Python untuk analisis citra ilmiah.",
        "• **Tahap 5 — Kualitas Data, *Class Imbalance* & *Anti-Data Leakage* (Pendalaman Bab 3 & Bab 4):**",
        "  – **13. *Coursera DeepLearning.AI — Convolutional Neural Networks (Week 1)*:** Pengantar akademis standar industri oleh Prof. Andrew Ng.",
        "  – **14 & 15. *Kaggle Learn & IBM — Data Leakage in Machine Learning*:** Studi kasus nyata mengapa kebocoran data antara *Train Set* dan *Test Set* adalah kesalahan paling berbahaya dalam proyek AI dan cara sistematis mencegahnya.",
    ],
}


def md_inline_to_html(text: str) -> str:
    """Convert **bold**, *italic*, `code`, and math tokens to clean HTML."""
    s = (
        text.replace("$$", "")
        .replace("\\times", "×")
        .replace("\\approx", "≈")
        .replace("\\rightarrow", "→")
        .replace("\\sum", "Σ")
        .replace("\\min", "min")
        .replace("\\mathbf{", "**")
        .replace("\\text{", "")
        .replace("\\frac{", "(")
        .replace("}{", ") / (")
        .replace("}", "")
        .replace("$", "")
    )
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def build_presenter_script_pdf() -> None:
    if not SLIDES_HTML_PATH.exists():
        raise FileNotFoundError(f"Slide HTML tidak ditemukan: {SLIDES_HTML_PATH}")

    raw_html = SLIDES_HTML_PATH.read_text(encoding="utf-8")

    explanations_html_map: dict[str, list[str]] = {}
    for k, bullets in SLIDE_EXPLANATIONS.items():
        explanations_html_map[str(k)] = [md_inline_to_html(b) for b in bullets]

    explanations_json = json.dumps(explanations_html_map, ensure_ascii=False)

    PRESENTER_OVERRIDE_CSS = """
    @media print {
      @page {
        size: A4 portrait;
        margin: 8mm 10mm 8mm 10mm;
      }
      html, body {
        background: #FFFFFF !important;
        width: 100% !important;
        height: auto !important;
        overflow: visible !important;
        display: block !important;
        padding: 0 !important;
        margin: 0 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      #progress-bar, #controls, #notes-drawer, #grid-modal, #session-timer, #edge-modal {
        display: none !important;
      }
      #stage-wrap {
        width: 100% !important;
        max-width: none !important;
        height: auto !important;
        aspect-ratio: auto !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        background: transparent !important;
        overflow: visible !important;
        display: block !important;
      }
      .presenter-page {
        width: 100%;
        page-break-after: always;
        break-after: page;
        page-break-inside: avoid;
        break-inside: avoid;
        display: flex;
        flex-direction: column;
        gap: 7px;
        padding: 0;
        margin: 0;
      }
      .presenter-page:last-child {
        page-break-after: auto;
        break-after: auto;
      }
      .p-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        border-bottom: 2px solid #1A73E8;
        padding-bottom: 4px;
      }
      .p-header-title {
        font-family: 'Poppins', sans-serif;
        font-size: 12.2pt;
        font-weight: 700;
        color: #202124;
        line-height: 1.22;
      }
      .p-header-title .p-slide-num {
        display: inline-block;
        background: #1A73E8;
        color: #FFFFFF;
        font-family: 'Roboto Mono', monospace;
        font-size: 9.5pt;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 5px;
        margin-right: 7px;
        vertical-align: middle;
      }
      .p-header-kicker {
        font-family: 'Roboto Mono', monospace;
        font-size: 7.8pt;
        font-weight: 700;
        color: #5F6368;
        background: #F1F3F4;
        padding: 2.5px 8px;
        border-radius: 999px;
        white-space: nowrap;
      }

      /* Container Gambar Slide (16:9 scaled from 1120x630 to 592x333 so detailed explanation fits on 1 page) */
      .p-slide-frame {
        width: 592px;
        height: 333px;
        margin: 0 auto;
        border: 1.5px solid #DADCE0;
        border-radius: 10px;
        overflow: hidden;
        position: relative;
        background: #FFFFFF;
        box-shadow: 0 2px 6px rgba(32,33,36,0.05);
        flex-shrink: 0;
      }
      .p-slide-frame > section.slide {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 1120px !important;
        height: 630px !important;
        transform: scale(0.5285714) !important;
        transform-origin: top left !important;
        display: flex !important;
        opacity: 1 !important;
        animation: none !important;
        page-break-after: avoid !important;
        break-after: avoid !important;
        border-radius: 0 !important;
        box-shadow: none !important;
      }

      .p-slide-frame .btn-ui {
        display: inline-flex !important;
      }
      .p-slide-frame .qa-answer, .p-slide-frame .quiz-ans {
        display: block !important;
        opacity: 1 !important;
        animation: none !important;
      }

      /* Box Penjelasan Detail Slide */
      .p-exp-box {
        background: #F8F9FA;
        border: 1px solid #DADCE0;
        border-left: 4.5px solid #1A73E8;
        border-radius: 0 9px 9px 0;
        padding: 9px 13px;
        display: flex;
        flex-direction: column;
        gap: 5px;
      }
      .p-exp-label {
        font-family: 'Poppins', sans-serif;
        font-size: 10pt;
        font-weight: 700;
        color: #1A73E8;
        letter-spacing: 0.2px;
        border-bottom: 1px solid #E8EAED;
        padding-bottom: 3px;
      }
      .p-exp-list {
        padding-left: 16px;
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin: 0;
      }
      .p-exp-list li {
        font-family: 'Roboto', Arial, sans-serif;
        font-size: 8.95pt;
        line-height: 1.38;
        color: #202124;
      }
      .p-exp-list li.sub-point {
        list-style-type: none;
        margin-left: -6px;
        padding-left: 8px;
        border-left: 2px solid #C6DAFC;
        color: #3C4043;
      }
      .p-exp-list li code {
        font-family: 'Roboto Mono', monospace;
        font-size: 8.2pt;
        background: #FFFFFF;
        border: 1px solid #E8EAED;
        color: #C5221F;
        padding: 0.5px 4px;
        border-radius: 3px;
      }
    }
    """

    TRANSFORM_DOM_JS = f"""
    const EXPLANATIONS = {explanations_json};
    window.addEventListener('load', () => {{
      setTimeout(() => {{
        const stage = document.getElementById('stage-wrap');
        const slides = Array.from(stage.querySelectorAll('section.slide'));
        slides.forEach((slide, idx) => {{
          const num = idx + 1;
          const title = slide.getAttribute('data-title') || ('Slide ' + num);
          const kickerEl = slide.querySelector('.kicker');
          const kicker = kickerEl ? kickerEl.textContent.trim() : 'SESSION P01';

          const page = document.createElement('div');
          page.className = 'presenter-page';

          // 1. Header: Slide N + Judul
          const hdr = document.createElement('div');
          hdr.className = 'p-header';
          hdr.innerHTML = `
            <div class="p-header-title">
              <span class="p-slide-num">Slide ${{num}}</span>${{title}}
            </div>
            <span class="p-header-kicker">${{kicker}}</span>
          `;

          // 2. Gambar Slide (live rendered slide inside 16:9 frame)
          const frame = document.createElement('div');
          frame.className = 'p-slide-frame';

          // 3. Penjelasan Detail Slide
          const exp = document.createElement('div');
          exp.className = 'p-exp-box';
          const bullets = EXPLANATIONS[String(num)] || [];
          const liHtml = bullets.map((b) => {{
            const trimmed = b.trim();
            if (trimmed.startsWith('•') || trimmed.startsWith('–')) {{
              return `<li class="sub-point">${{trimmed}}</li>`;
            }}
            return `<li>${{trimmed}}</li>`;
          }}).join('');
          exp.innerHTML = `
            <div class="p-exp-label">Penjelasan Detail Materi — Slide ${{num}}:</div>
            <ul class="p-exp-list">${{liHtml}}</ul>
          `;

          slide.parentNode.insertBefore(page, slide);
          frame.appendChild(slide);
          page.appendChild(hdr);
          page.appendChild(frame);
          page.appendChild(exp);
        }});
      }}, 350);
    }});
    """

    inject_block = (
        f"<style>{PRESENTER_OVERRIDE_CSS}</style>\n"
        f"<script>{TRANSFORM_DOM_JS}</script>\n"
        "</body>"
    )
    print_html = raw_html.replace("</body>", inject_block, 1)
    TMP_HTML_PATH.write_text(print_html, encoding="utf-8")

    browser_bin = next((c for c in CHROME_CANDIDATES if Path(c).exists()), None)
    if browser_bin is None:
        TMP_HTML_PATH.unlink(missing_ok=True)
        raise RuntimeError("Tidak ditemukan Chrome atau Edge untuk ekspor PDF script presentasi.")

    try:
        file_url = TMP_HTML_PATH.resolve().as_uri()
        cmd = [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=4500",
            f"--print-to-pdf={OUT_PDF_PATH.resolve()}",
            file_url,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finally:
        TMP_HTML_PATH.unlink(missing_ok=True)

    raw_pdf = OUT_PDF_PATH.read_bytes()
    page_count = len(re.findall(rb"/Type\s*/Page\b", raw_pdf))
    size_mb = OUT_PDF_PATH.stat().st_size / (1024 * 1024)

    print(
        f"PDF Script Penjelasan Detail Slide P01 berhasil dibuat: {OUT_PDF_PATH}\n"
        f"  Total Slide: 59 | Total Halaman PDF: {page_count} | Ukuran: {size_mb:.2f} MB"
    )


if __name__ == "__main__":
    build_presenter_script_pdf()
