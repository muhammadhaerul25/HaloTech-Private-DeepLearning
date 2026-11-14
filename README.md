# HaloTech Private Deep Learning — P1: Understanding Images & Image Processing

Materi pembelajaran **1-on-1 Deep Learning (120 menit)** oleh **Muhammad Haerul**, mencakup slide interaktif berbasis web (PWA), ekspor PDF, dataset sampel sintetis, dan notebook hands-on beserta kunci jawabannya.

## Live Slides (PWA)
- **GitHub Pages:** https://muhammadhaerul25.github.io/HaloTech-Private-DeepLearning/
- Dapat di-install sebagai **PWA** (offline-ready) langsung dari Chrome/Edge/mobile saat dibuka melalui HTTPS.

## Struktur Folder
```text
├── index.html                          # Entry redirect ke slide P1 + PWA manifest
├── manifest.webmanifest                # Konfigurasi Web App Manifest (PWA)
├── sw.js                               # Service Worker untuk caching offline (14 aset)
├── requirements.txt                    # Dependensi Python untuk slide & notebook
├── PLAN.md                             # Kurikulum utama
├── docs/
│   └── PROGRESS.md                     # Status implementasi & hasil validasi
├── Materials/                          # Paket materi siap pakai per pertemuan
│   └── P01 - Understanding Images, Image Processing & EDA/
│       ├── P01_image_processing_eda.html
│       ├── P01_image_processing_eda.pdf
│       ├── P01_image_processing_eda.pptx
│       ├── P01_image_processing_eda.ipynb
│       ├── solutions/P01_image_processing_eda.ipynb
│       ├── data/sample/
│       └── assets/P01/
├── slides/
│   ├── P01_image_processing_eda.html   # Dek interaktif 54 slide (HTML5)
│   ├── P01_image_processing_eda.pdf    # Ekspor PDF vektor 54 halaman (16:9)
│   ├── P01_image_processing_eda.pptx   # Dek PPTX awal (22 slide)
│   └── assets/P01/                     # Aset gambar, grafik EDA, ikon PWA & statistik
├── notebooks/
│   ├── P01_image_processing_eda.ipynb  # Notebook hands-on peserta (# TODO)
│   └── solutions/
│       └── P01_image_processing_eda.ipynb  # Notebook kunci jawaban (tervalidasi)
├── data/
│   └── sample/                         # 120 foto sintetis (5 kelas × polos/ramai)
├── results/                            # Output CSV & grafik boxplot EDA
└── tools/                              # Skrip generator & validator reproducible
    ├── build_html_slides_P01.py
    ├── build_notebooks_P01.py
    ├── build_slides_P01.py
    ├── export_pdf_P01.py
    ├── make_sample_data.py
    ├── slide_theme.py
    ├── sync_materials.py
    └── validate_and_render_P01.py
```

## Cara Menjalankan / Rebuild Lokal
```bash
pip install -r requirements.txt
python tools/make_sample_data.py
python tools/build_html_slides_P01.py
python tools/export_pdf_P01.py
python tools/build_notebooks_P01.py
python tools/sync_materials.py
```
