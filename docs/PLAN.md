# PLAN.md — Learning Plan Deep Learning P4–P13
**Project:** Klasifikasi Karakter Disney dengan CNN (MobileNetV2, transfer learning)
**Peserta:** Wur · Online 1-on-1 · 10 sesi × 120 menit · 15 Nov – 16 Des 2026 (Minggu 13:00–15:00 WIB, Rabu 19:30–21:30 WIB)
**Audiens:** pemula deep learning. Teoritis tapi praktis, mudah dipahami.

## 1. Asumsi (belum dikonfirmasi; tandai `[ASUMSI]` di materi bila relevan)
1. P1–P3 sudah mencakup Python dasar, NumPy, konsep ML dasar.
2. Project memakai foto karakter Disney buatan sendiri (mis. figurine/plush/merchandise). **Polos vs ramai** = kondisi latar belakang foto.
3. Stack: Python, TensorFlow/Keras 3 (format `.keras`), Google Colab (GPU gratis).
4. Bahasa materi: Indonesia; istilah teknis tetap Inggris.
5. Dataset awal: 5 kelas × 2 kondisi × 60–100 foto. Kelas contoh: Mickey, Minnie, Donald, Goofy, Stitch. Daftar kelas final **belum ditentukan**: simpan sebagai variabel konfigurasi, jangan di-hardcode.

## 2. Template 120 menit (semua sesi)
| Menit | Blok |
|---|---|
| 0–10 | Recap + pertanyaan pemantik |
| 10–40 | Teori inti (slide) |
| 40–45 | Istirahat |
| 45–95 | Hands-on notebook |
| 95–110 | Mini-challenge / diskusi |
| 110–120 | Rangkuman, quiz 5 soal, tugas |

## 3. Struktur folder project
```
disney-dl-course/
├── AGENTS.md
├── docs/PLAN.md, docs/PROGRESS.md
├── slides/P04_...pptx ... P13_...pptx
├── notebooks/P04_...ipynb (peserta) + notebooks/solutions/P04_...ipynb (kunci)
├── data/raw/ (foto + metadata.csv)        # dikelola peserta
├── data/sample/ (data sintetis kecil)     # dibuat agent untuk smoke test
├── split/train|val|test/<kelas>/ + split_log.csv
├── models/ baseline.keras, model_final.keras
└── results/ history.csv, metrik, confusion matrix, Grad-CAM
```

## 4. Alur eksperimen yang harus konsisten antar sesi
- Skenario S1: latih dengan campuran polos+ramai, uji terpisah pada polos dan ramai.
- Skenario S2: latih pada polos, uji pada ramai (generalisasi).
- EDA (P4) hanya deskriptif. Split (P8) stratified + group per sesi foto; cek duplikat via hash. Normalisasi/augmentation hanya dari/pada train.
- Baseline (P9): pembanding majority class + MobileNetV2 beku + GAP + Dropout + Dense softmax.
- Fine-tuning (P10): dua tahap, LR kecil (~1e-5), base dipanggil `training=False`, EarlyStopping/ReduceLROnPlateau/ModelCheckpoint.
- Evaluasi (P11): test set dipakai sekali; metrik keseluruhan, per kelas, per kondisi; bootstrap CI.
- Grad-CAM (P12): layer konv terakhir MobileNetV2 (umumnya `out_relu`, verifikasi lewat `model.summary()`).

## 5. Detail per pertemuan

### P4 · Minggu, 15 November 2026 · 13:00–15:00 WIB · Image Processing & EDA Foto Sendiri  (fase: Fondasi)

**Tujuan:**
- Memahami gambar sebagai array angka (tinggi × lebar × channel).
- Memuat, me-resize, dan menormalisasi foto dengan Pillow/OpenCV/NumPy.
- Menghitung dan membandingkan statistik dataset kondisi polos vs ramai.

**Teori (menit 10–40):** Piksel, channel RGB vs grayscale, tipe data uint8 vs float32, normalisasi. Resolusi, aspect ratio, dan resize (mengapa model butuh ukuran seragam). Histogram, brightness, kontras. Apa itu EDA dan mengapa dilakukan sebelum modeling. Proxy kompleksitas background: edge density dan entropy. Konsep awal class imbalance.

**Hands-on (menit 45–95):** Load foto dan baca nilai arraynya; koreksi orientasi EXIF (foto HP sering terputar); inventaris dataset (jumlah per kelas × kondisi, resolusi, ukuran file); deteksi file rusak dan duplikat dengan hash; hitung brightness, kontras, dan edge density (Canny) per foto; boxplot polos vs ramai.

**Mini-challenge (menit 95–110):** Hanya dari statistik, tebak kondisi mana yang lebih sulit bagi model dan mengapa. Jawaban dicatat sebagai hipotesis awal untuk laporan.

**Konsep kunci:** Image = array, Channel, Normalisasi, EDA, Edge density, Class imbalance

**Sumber:**
- Dokumentasi Pillow dan OpenCV (tutorial dasar image processing)
- 3Blue1Brown, *But what is a neural network?* — bagian awal menunjukkan gambar sebagai grid piksel: https://www.youtube.com/watch?v=aircAruvnKk
- Coursera CNN (DeepLearning.AI) Week 1, topik edge detection: https://www.coursera.org/learn/convolutional-neural-networks

**Output & tugas:** Tabel statistik dataset polos vs ramai + 3 temuan utama. EDA bersifat deskriptif; belum ada keputusan yang memakai data test (lihat P8).

**Kriteria berhasil:**
- Bisa menjelaskan arti shape (224, 224, 3).
- Tabel statistik per kelas × kondisi tersedia dan bisa dibaca.
- Tidak ada foto rusak/duplikat yang lolos ke tahap berikut.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Apa beda uint8 dan float32 pada gambar?
- Mengapa foto HP perlu dicek EXIF-nya?
- Apa yang diukur edge density terhadap background?

### P5 · Rabu, 18 November 2026 · 19:30–21:30 WIB · Teori Neural Network (ANN)  (fase: Fondasi)

**Tujuan:**
- Menjelaskan neuron: input × weight + bias → fungsi aktivasi.
- Memahami peran aktivasi (ReLU, sigmoid, tanh) dan softmax.
- Memahami secara intuitif bagaimana jaringan belajar (loss, gradient descent).

**Teori (menit 10–40):** Neuron sebagai kalkulator sederhana; layer dan hidden layer; mengapa perlu non-linearitas; sigmoid, tanh, ReLU; softmax mengubah skor menjadi probabilitas; cross-entropy sebagai ukuran 'seberapa salah'; gradient descent dan learning rate; backpropagation secara intuitif tanpa turunan formal; epoch, batch, pengenalan overfitting.

**Hands-on (menit 45–95):** Satu neuron dan forward pass dari nol dengan NumPy; hitung softmax manual lalu cocokkan dengan Keras; MLP Keras pada Fashion-MNIST; ubah learning rate dan aktivasi lalu amati kurva loss; eksperimen flatten foto Disney ke MLP untuk melihat hilangnya struktur spasial (jembatan ke CNN).

**Mini-challenge (menit 95–110):** Tebak output softmax dari tiga skor tanpa kalkulator, lalu jelaskan mengapa jumlahnya selalu 1.

**Konsep kunci:** Neuron, Weight & bias, ReLU, Softmax, Loss, Gradient descent, Learning rate

**Sumber:**
- 3Blue1Brown Neural Networks, bab 1–4 (playlist): https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi
- Versi tulis 3Blue1Brown: https://3blue1brown.com/lessons/neural-networks
- TensorFlow Playground (eksperimen visual jaringan kecil)
- Stanford CS231n, catatan Neural Networks (opsional)
- Coursera Deep Learning Specialization Course 1 (opsional)

**Output & tugas:** Ringkasan satu halaman 'cara kerja neuron sampai softmax' dengan bahasa sendiri.

**Kriteria berhasil:**
- Bisa menghitung satu neuron dengan tangan.
- Bisa menjelaskan mengapa ReLU dipakai di hidden layer dan softmax di output.
- Bisa membaca kurva loss turun/naik.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Apa fungsi bias?
- Apa yang terjadi jika learning rate terlalu besar?
- Mengapa softmax dipakai untuk klasifikasi multi-kelas?

### P6 · Minggu, 22 November 2026 · 13:00–15:00 WIB · CNN Fundamentals & Jenis Tugas Computer Vision  (fase: Fondasi)

**Tujuan:**
- Menjelaskan konvolusi, kernel/filter, stride, padding, pooling, dan feature map.
- Membedakan classification, localization, detection, dan segmentation.
- Menempatkan project ini sebagai image classification multi-kelas.

**Teori (menit 10–40):** Kernel sebagai pencari pola (tepi → bentuk → bagian → objek); stride dan padding; parameter sharing (mengapa jauh lebih hemat daripada Dense); pooling; receptive field; flatten/Global Average Pooling dan softmax di ujung; peta tugas computer vision.

**Hands-on (menit 45–95):** Konvolusi manual dengan kernel Sobel pada foto Disney; Conv2D kecil di Keras; visualisasi feature map tiap layer; bandingkan jumlah parameter CNN vs MLP pada input yang sama.

**Mini-challenge (menit 95–110):** Hitung manual ukuran output untuk beberapa kombinasi input/kernel/stride/padding; tentukan tugas CV yang tepat untuk 4 skenario berbeda.

**Konsep kunci:** Kernel, Stride, Padding, Pooling, Feature map, Receptive field, GAP

**Sumber:**
- Coursera CNN (DeepLearning.AI), Week 1 Foundations of CNN: https://www.coursera.org/learn/convolutional-neural-networks
- CNN Explainer (poloclub.github.io/cnn-explainer) — visual interaktif
- Dumoulin & Visin, *A guide to convolution arithmetic for deep learning* (arXiv 1603.07285)
- Stanford CS231n, catatan Convolutional Networks (opsional)

**Output & tugas:** Diagram buatan sendiri tentang alur satu foto melewati conv → pooling → softmax.

**Kriteria berhasil:**
- Bisa menghitung ukuran output konvolusi.
- Bisa menjelaskan mengapa CNN lebih cocok daripada MLP untuk gambar.
- Bisa menyebut tugas CV yang sesuai untuk project ini.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Apa yang dilakukan stride 2?
- Mengapa pooling dipakai?
- Apa beda classification dan detection?

### P7 · Rabu, 25 November 2026 · 19:30–21:30 WIB · Arsitektur CNN & Transfer Learning  (fase: Fondasi)

**Tujuan:**
- Memahami evolusi arsitektur CNN dan inti ide tiap generasi.
- Memahami transfer learning (feature extraction vs fine-tuning).
- Menyusun alasan ilmiah memilih MobileNetV2.

**Teori (menit 10–40):** Garis waktu LeNet → AlexNet → VGG → Inception → ResNet → MobileNet → EfficientNet. Masalah network dalam dan ide residual connection. Depthwise separable convolution. Inverted residual dan linear bottleneck (MobileNetV2). ImageNet dan pretrained weights. Feature extraction vs fine-tuning. Kapan transfer learning efektif pada dataset kecil.

**Hands-on (menit 45–95):** Muat MobileNetV2 berbobot ImageNet, prediksi foto Disney dan amati label ImageNet yang 'meleset' (motivasi transfer learning); model.summary(), hitung layer dan parameter; bandingkan MobileNetV2 dengan ResNet50 dan EfficientNetB0 (parameter, ukuran, kecepatan inferensi); bangun base beku + head baru; cek preprocess_input yang benar (skala −1 s.d. 1).

**Mini-challenge (menit 95–110):** Isi tabel kriteria pemilihan model: akurasi, ukuran, kecepatan, ketersediaan di Keras, kecocokan dataset kecil, batas Colab.

**Konsep kunci:** Residual, Depthwise separable conv, Inverted residual, Pretrained, Feature extraction, Fine-tuning

**Sumber:**
- Sandler dkk., *MobileNetV2: Inverted Residuals and Linear Bottlenecks* (CVPR 2018): https://arxiv.org/abs/1801.04381
- Tutorial TensorFlow Transfer Learning & Fine-tuning (ada versi Indonesia): https://www.tensorflow.org/tutorials/images/transfer_learning?hl=id
- Roboflow, *How to train MobileNetV2 on a custom dataset*: https://roboflow.com/blog/how-to-train-mobilenetv2-on-a-custom-dataset
- Yosinski dkk., *How transferable are features in deep neural networks?* (arXiv 1411.1792)
- He dkk., *Deep Residual Learning* (arXiv 1512.03385)

**Output & tugas:** Paragraf 'Alasan Pemilihan MobileNetV2' (kandidat bab Metode) lengkap dengan tabel perbandingan model.

**Kriteria berhasil:**
- Bisa menjelaskan mengapa transfer learning cocok untuk dataset kecil.
- Tabel perbandingan model terisi dengan angka dari notebook.
- Bisa menjelaskan arti 'base beku' dan 'head baru'.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Apa masalah yang dipecahkan residual connection?
- Apa beda feature extraction dan fine-tuning?
- Mengapa MobileNetV2 ringan?

### P8 · Minggu, 29 November 2026 · 13:00–15:00 WIB · Metodologi Data: Collection, Splitting & Desain Eksperimen  (fase: Eksperimen)

**Tujuan:**
- Menyusun protokol pengumpulan data yang konsisten.
- Membuat split train/val/test yang bebas data leakage.
- Merancang eksperimen yang bisa direproduksi.

**Teori (menit 10–40):** Kualitas vs kuantitas data; protokol pengambilan foto dan penamaan file; fungsi train/validation/test (70/15/15 atau 80/10/10); stratified split; data leakage (foto burst, duplikat, normalisasi dari seluruh data); group split per sesi foto; seed dan reproducibility; variabel eksperimen (kondisi latar) dan skenario S1/S2.

**Hands-on (menit 45–95):** Skrip split stratified + group (scikit-learn); verifikasi tidak ada foto kembar antar-split dengan hash; plot distribusi kelas × kondisi per split; tulis split_log.csv (file, kelas, kondisi, id_sesi, split, seed); bentuk folder split/train|val|test/kelas.

**Mini-challenge (menit 95–110):** Temukan 3 sumber leakage tersembunyi pada contoh dataset yang sengaja 'dirusak'.

**Konsep kunci:** Train/Val/Test, Stratified, Group split, Data leakage, Seed, Reproducibility

**Sumber:**
- Dokumentasi scikit-learn model_selection (train_test_split, StratifiedGroupKFold)
- Google Machine Learning Crash Course — data splits
- Kapoor & Narayanan, *Leakage and the reproducibility crisis in machine-learning-based science* (Patterns, 2023)

**Output & tugas:** Folder split/ final + split_log.csv + paragraf desain eksperimen (kandidat bab Metode).

**Kriteria berhasil:**
- Tidak ada file yang sama/hampir sama di dua split.
- Proporsi kelas dan kondisi seimbang antar-split.
- split_log.csv bisa mereproduksi split yang sama.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Mengapa foto burst bisa menyebabkan leakage?
- Apa fungsi validation set?
- Mengapa seed perlu dicatat?

### P9 · Rabu, 2 Desember 2026 · 19:30–21:30 WIB · Data Pipeline, Augmentation & Model Baseline  (fase: Eksperimen)

**Tujuan:**
- Membangun pipeline data yang efisien.
- Memahami dan menerapkan augmentation dengan benar.
- Menghasilkan model baseline yang dapat dibandingkan.

**Teori (menit 10–40):** Alur tf.data (load → resize → batch → cache → prefetch); preprocessing vs augmentation; jenis augmentation (flip, rotate, zoom, brightness, contrast) dan batasnya (hanya pada train; jangan merusak identitas karakter); definisi baseline dan alasan wajib punya baseline; membaca kurva awal.

**Hands-on (menit 45–95):** image_dataset_from_directory pada folder split/; visualisasi hasil augmentation; baseline pembanding (majority class); baseline model = MobileNetV2 beku + GlobalAveragePooling + Dropout + Dense softmax selama 5–10 epoch; ModelCheckpoint; simpan models/baseline.keras.

**Mini-challenge (menit 95–110):** Diagnosis dari kurva: underfitting, overfitting, atau normal.

**Konsep kunci:** tf.data, Prefetch, Augmentation, Baseline, Dropout, Checkpoint

**Sumber:**
- Tutorial TensorFlow: Data augmentation & Load and preprocess images
- Keras guide: Working with preprocessing layers
- Roboflow MobileNetV2 tutorial: https://roboflow.com/blog/how-to-train-mobilenetv2-on-a-custom-dataset

**Output & tugas:** models/baseline.keras + grafik kurva training + perbandingan akurasi validasi vs baseline majority.

**Kriteria berhasil:**
- Augmentation tidak ikut ke val/test.
- Baseline mengalahkan tebakan majority class.
- File baseline.keras bisa dimuat ulang dan dipakai prediksi.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Mengapa augmentation tidak dipakai pada test set?
- Apa fungsi prefetch?
- Mengapa perlu baseline?

### P10 · Minggu, 6 Desember 2026 · 13:00–15:00 WIB · Training Lengkap & Fine-tuning  (fase: Eksperimen)

**Tujuan:**
- Menjalankan training dua tahap (head lalu fine-tuning).
- Menggunakan callback untuk training yang stabil.
- Mendokumentasikan riwayat training secara rapi.

**Teori (menit 10–40):** Tahap 1 melatih head, tahap 2 membuka sebagian layer atas; mengapa learning rate fine-tuning kecil (±1e-5); perilaku BatchNorm saat fine-tuning (base dipanggil dengan training=False); EarlyStopping, ReduceLROnPlateau, ModelCheckpoint; class weight; hyperparameter utama (learning rate, batch size, dropout); optimizer Adam.

**Hands-on (menit 45–95):** Training tahap 1 → unfreeze N layer teratas → training tahap 2; simpan history ke CSV dan grafik; bandingkan baseline vs model final pada validation; simpan models/model_final.keras; tips Colab (batas sesi, simpan ke Drive, seed).

**Mini-challenge (menit 95–110):** Ubah satu hyperparameter dan prediksikan dampaknya sebelum menjalankan, lalu cocokkan dengan hasil.

**Konsep kunci:** Unfreeze, Learning rate kecil, BatchNorm, EarlyStopping, Class weight, Adam

**Sumber:**
- Tutorial TensorFlow Transfer Learning & Fine-tuning: https://www.tensorflow.org/tutorials/images/transfer_learning?hl=id
- Keras guide: Transfer learning & fine-tuning
- Kingma & Ba, *Adam* (arXiv 1412.6980)
- Srivastava dkk., *Dropout* (JMLR, 2014)

**Output & tugas:** models/model_final.keras + riwayat training (CSV + plot) + catatan hyperparameter.

**Kriteria berhasil:**
- Kurva val tidak menunjukkan overfitting parah.
- Model final lebih baik daripada baseline pada validation.
- Riwayat training tersimpan dan terbaca.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Mengapa learning rate dikecilkan saat fine-tuning?
- Apa fungsi EarlyStopping?
- Apa risiko membuka semua layer sekaligus?

### P11 · Rabu, 9 Desember 2026 · 19:30–21:30 WIB · Evaluasi & Metrics: Polos vs Ramai  (fase: Analisis & Pelaporan)

**Tujuan:**
- Mengevaluasi model secara jujur pada test set.
- Menjelaskan dan menghitung accuracy, precision, recall, F1, confusion matrix.
- Membandingkan performa kondisi polos vs ramai.

**Teori (menit 10–40):** Test set dipakai sekali; accuracy dan mengapa tidak cukup; confusion matrix, precision, recall, F1 (macro vs weighted); analisis per kelas dan per kondisi; kalibrasi confidence (softmax); ketidakpastian dengan bootstrap confidence interval pada dataset kecil.

**Hands-on (menit 45–95):** Prediksi test set; classification_report; heatmap confusion matrix; metrik terpisah polos vs ramai; selisih performa (gap) dan bootstrap CI; histogram confidence benar vs salah; ekspor tabel CSV dan grafik resolusi tinggi dengan gaya konsisten.

**Mini-challenge (menit 95–110):** Tulis interpretasi satu paragraf dari tabel hasil (apa yang terlihat, bukan hanya angka).

**Konsep kunci:** Confusion matrix, Precision, Recall, F1, Macro vs weighted, Bootstrap CI

**Sumber:**
- Dokumentasi scikit-learn Metrics (classification_report, confusion_matrix)
- Google Machine Learning Crash Course — classification metrics
- StatQuest — Confusion Matrix, Sensitivity & Specificity

**Output & tugas:** Tabel dan grafik untuk bab Hasil: metrik keseluruhan, per kelas, dan per kondisi.

**Kriteria berhasil:**
- Test set hanya dievaluasi sekali untuk laporan.
- Ada metrik per kondisi dan selisihnya dengan CI.
- Setiap grafik/tabel punya interpretasi tertulis.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Kapan accuracy menyesatkan?
- Apa beda macro dan weighted F1?
- Apa arti baris dan kolom confusion matrix?

### P12 · Minggu, 13 Desember 2026 · 13:00–15:00 WIB · Analisis Error & Grad-CAM  (fase: Analisis & Pelaporan)

**Tujuan:**
- Memahami mengapa model membuat kesalahan.
- Menerapkan Grad-CAM pada MobileNetV2.
- Memeriksa apakah model melihat karakter atau malah background.

**Teori (menit 10–40):** Error analysis sistematis: galeri salah prediksi, pasangan kelas yang sering tertukar, kategori penyebab (background, oklusi, cahaya, sudut, blur). Ide Grad-CAM: gradien skor kelas terhadap feature map konvolusi terakhir → bobot → heatmap. Batasan Grad-CAM (penjelasan kasar, bukan bukti kausal). Shortcut learning dan bias dataset.

**Hands-on (menit 45–95):** Galeri salah prediksi dan kategorisasi manual; implementasi Grad-CAM di Keras (layer konvolusi terakhir MobileNetV2, umumnya out_relu — cek lewat model.summary()); heatmap untuk prediksi benar vs salah, polos vs ramai; hitung proporsi kasus ketika perhatian model jatuh ke background.

**Mini-challenge (menit 95–110):** Tulis 3 hipotesis penyebab error beserta cara mengujinya.

**Konsep kunci:** Error analysis, Grad-CAM, Heatmap, Shortcut learning, Dataset bias

**Sumber:**
- Keras example: Grad-CAM class activation visualization: https://keras.io/examples/vision/grad_cam
- Selvaraju dkk., *Grad-CAM* (ICCV 2017 / IJCV 2019): https://arxiv.org/abs/1610.02391
- PyImageSearch, Grad-CAM dengan Keras dan TensorFlow: https://pyimagesearch.com/2020/03/09/grad-cam-visualize-class-activation-maps-with-keras-tensorflow-and-deep-learning/
- Geirhos dkk., *Shortcut Learning in Deep Neural Networks* (arXiv 2004.07780)

**Output & tugas:** Draf bab Diskusi + figur Grad-CAM (benar/salah × polos/ramai).

**Kriteria berhasil:**
- Minimal 3 kategori penyebab error terdokumentasi dengan contoh gambar.
- Figur Grad-CAM disertai interpretasi dan catatan keterbatasan.
- Hipotesis dirumuskan, bukan diklaim sebagai fakta.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Apa yang ditunjukkan area merah pada heatmap?
- Mengapa Grad-CAM tidak membuktikan sebab-akibat?
- Apa itu shortcut learning?

### P13 · Rabu, 16 Desember 2026 · 19:30–21:30 WIB · Rangkuman, Demo & Persiapan Laporan  (fase: Analisis & Pelaporan)

**Tujuan:**
- Merangkai seluruh pipeline menjadi cerita utuh.
- Mendemokan model pada foto baru.
- Siap mempertahankan pekerjaan dalam mock defense.

**Teori (menit 10–40):** Recap end-to-end (data → model → evaluasi → penjelasan); struktur laporan (Pendahuluan, Tinjauan Pustaka, Metode, Hasil, Diskusi, Kesimpulan, Keterbatasan, Saran); menulis keterbatasan dengan jujur (dataset kecil, satu kamera, dll.); sitasi dan daftar pustaka.

**Hands-on (menit 45–95):** Notebook inferensi (foto baru → top-3 prediksi + confidence + Grad-CAM); opsional demo sederhana dengan Gradio; kerangka laporan dan pemetaan artefak P4–P12 ke bab laporan.

**Mini-challenge (menit 95–110):** Mock defense: latihan tanya-jawab (mengapa MobileNetV2? mengapa split begitu? apa itu overfitting? apa arti F1? apa kelemahan dataset? bagaimana jika ditambah karakter baru?).

**Konsep kunci:** End-to-end, Inferensi, Struktur laporan, Keterbatasan, Sitasi

**Sumber:**
- Jurnal Indonesia berbasis MobileNetV2 sebagai contoh penulisan (lihat Bagian 6)
- Dokumentasi Keras/TensorFlow untuk rujukan teknis

**Output & tugas:** Draft laporan + catatan perbaikan hasil mock defense.

**Kriteria berhasil:**
- Setiap artefak P4–P12 sudah terpetakan ke bab laporan.
- Demo inferensi berjalan pada foto yang belum pernah dilihat model.
- Peserta bisa menjawab ≥80% pertanyaan mock defense dengan penjelasan sendiri.

**Contoh soal quiz (bank awal, tambah sampai 5):**
- Apa urutan pipeline dari foto sampai prediksi?
- Apa saja keterbatasan penelitian ini?
- Bagaimana cara memperbaiki dataset di iterasi berikutnya?

## 6. Sumber
**Terverifikasi ada (saat penyusunan; cek ulang akses/harga):** Coursera CNN DeepLearning.AI (https://www.coursera.org/learn/convolutional-neural-networks); 3Blue1Brown (https://www.youtube.com/watch?v=aircAruvnKk, playlist PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi); TensorFlow Transfer Learning ID (https://www.tensorflow.org/tutorials/images/transfer_learning?hl=id); Keras Grad-CAM (https://keras.io/examples/vision/grad_cam); Roboflow MobileNetV2 (https://roboflow.com/blog/how-to-train-mobilenetv2-on-a-custom-dataset); PyImageSearch Grad-CAM (https://pyimagesearch.com/2020/03/09/grad-cam-visualize-class-activation-maps-with-keras-tensorflow-and-deep-learning/); MobileNetV2 (arXiv 1801.04381); Grad-CAM (arXiv 1610.02391); Udemy opsional: complete-deep-learning-computer-vision-with-projects, master-deep-learning-for-computer-vision-with-tensorflow-2, python-for-deep-learning-and-artificial-intelligence, hands-on-transfer-learning-with-tensorflow-20.
**Jurnal Indonesia MobileNetV2 (contoh tinjauan pustaka):** jurnal.polinema.ac.id (ras ayam), journal.nurulfikri.ac.id (SIBI), ojs-teknik.usni.ac.id (BISINDO), ejournal.uksw.edu (sarang walet), eprints.walisongo.ac.id (batik).
**Belum diverifikasi ulang (tandai `[CEK LINK]` jika dipakai):** CS231n, CNN Explainer, TensorFlow Playground, StatQuest, Google ML Crash Course, Keras guides, d2l.ai, Chollet *Deep Learning with Python*, paper ResNet (1512.03385), Adam (1412.6980), Dropout (JMLR 2014), Yosinski (1411.1792), Dumoulin & Visin (1603.07285), Geirhos (2004.07780), Kapoor & Narayanan (Patterns 2023).
**Referensi tambahan dari peserta:** belum ada. Bagian ini akan diperbarui.

## 7. Rubrik capaian (ringkas)
Konsep (bisa menjelaskan dengan bahasa sendiri) · Data & split (bebas leakage, terdokumentasi) · Training (dua tahap + callback + riwayat) · Evaluasi (per kelas & kondisi + CI) · Analisis error (kategori penyebab + Grad-CAM + keterbatasan jujur).
