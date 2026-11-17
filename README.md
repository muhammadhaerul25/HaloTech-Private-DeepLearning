# HaloTech Private Deep Learning — P1: Understanding Images & Image Processing

Materi pembelajaran **1-on-1 Deep Learning (120 menit)** oleh **Muhammad Haerul**, mencakup slide interaktif berbasis web (PWA), ekspor PDF, dataset sampel sintetis, dan notebook hands-on beserta kunci jawabannya.

## Live Slides (PWA)
- **GitHub Pages:** https://muhammadhaerul25.github.io/HaloTech-Private-DeepLearning/
- Dapat di-install sebagai **PWA** (offline-ready) langsung dari Chrome/Edge/mobile saat dibuka melalui HTTPS.

## Struktur Folder
```text
├── index.html                          # Portal Kurikulum Web (P01–P08) + PWA entry
├── sessions.json                       # Konfigurasi sesi & tautan materi portal web
├── manifest.webmanifest                # Konfigurasi Web App Manifest (PWA)
├── sw.js                               # Service Worker untuk caching offline
├── vercel.json                         # Konfigurasi routing & header untuk Vercel
├── requirements.txt                    # Dependensi Python untuk slide, PDF & notebook
├── AGENTS.md                           # Panduan & aturan standar pengembangan materi
├── docs/                               # Dokumentasi kurikulum & referensi
│   ├── PLAN.md                         # Kurikulum utama (10/8 pertemuan)
│   ├── PROMPT_MASTER.md                # Prompt master perancangan materi
│   ├── PROGRESS.md                     # Status implementasi & hasil validasi
│   └── references/                     # Kumpulan PDF referensi desain slide
├── slides/                             # Materi presentasi per pertemuan (HTML, PDF, PPTX)
│   ├── P01_image_processing_eda.html   # Dek interaktif 57 slide (HTML5)
│   ├── P01_image_processing_eda.pdf    # Ekspor PDF vektor 72 halaman (16:9)
│   ├── P01_image_processing_eda.pptx   # Dek PowerPoint (25 slide, 120 menit)
│   └── assets/
│       └── P01/                        # Aset visualisasi, grafik EDA, ikon PWA & statistik
├── notebooks/                          # Notebook hands-on Google Colab / Jupyter
│   ├── P01_image_processing_eda.ipynb  # Notebook peserta (26 sel, 5 latihan # TODO)
│   └── solutions/
│       └── P01_image_processing_eda.ipynb  # Notebook kunci jawaban (21 sel tervalidasi)
├── data/
│   └── sample/                         # Dataset sampel sintetis (120 foto + metadata.csv)
├── results/                            # Output CSV & grafik hasil eksekusi notebook
└── tools/                              # Skrip generator, ekspor & validator otomatis
    ├── build_all.py                    # Orkestrator 1 perintah untuk seluruh pipeline
    ├── build_html_slides_P01.py        # Generator slide HTML interaktif & PWA
    ├── build_notebooks_P01.py          # Generator notebook peserta & kunci jawaban
    ├── build_slides_P01.py             # Generator visualisasi & dek PPTX
    ├── export_pdf_P01.py               # Ekspor HTML ke PDF via Chrome Headless
    ├── make_sample_data.py             # Generator dataset sintetis deterministik
    ├── slide_theme.py                  # Komponen & palet tema Google I/O-style
    └── validate_and_render_P01.py      # Validator kualitas slide & dataset
```

## Cara Menjalankan / Rebuild Lokal
```bash
pip install -r requirements.txt
python tools/build_all.py
```
