# HaloTech Private Deep Learning (P01–P08)

Materi pembelajaran **1-on-1 Deep Learning (120 menit/sesi)** oleh **Muhammad Haerul**, menggunakan proyek utama klasifikasi karakter **Disney Frozen Figurine** (*Computer Vision → Neural Network → CNN → Transfer Learning MobileNetV2*). Setiap pertemuan menghasilkan paket lengkap: **Dek HTML5 Interaktif (SSOT)**, **PDF 16:9 Vektor**, **PPTX 16:9 Retina HD (+ Speaker Notes)**, **Presenter Script PDF A4**, serta **Notebook Peserta & Kunci Jawaban**.

## Live Slides (PWA)
- **GitHub Pages:** https://muhammadhaerul25.github.io/HaloTech-Private-DeepLearning/
- Dapat di-install sebagai **PWA** (offline-ready) langsung dari Chrome/Edge/mobile saat dibuka melalui HTTPS.

## Struktur Folder
```text
├── index.html                                  # Portal Kurikulum Web (P01–P08) + PWA entry
├── sessions.json                               # Konfigurasi & status sesi untuk portal web
├── manifest.webmanifest / sw.js / vercel.json  # Konfigurasi PWA & routing deploy statis
├── requirements.txt                            # Dependensi Python (slide, PDF/PPTX & notebook)
├── AGENTS.md                                   # Aturan pengembangan materi per sesi (P01–P08)
├── docs/
│   ├── PLAN.md                                 # Kurikulum utama P01–P08
│   ├── STANDAR_MATERI.md                       # SOP arsitektur SSOT, tema & validasi
│   ├── PROMPT_MASTER.md                        # Prompt master perancangan sesi
│   ├── PROGRESS.md                             # Status implementasi & log validasi P01–P08
│   └── references/                             # PDF referensi desain internal (di-ignore saat deploy web)
├── materials/                                  # Paket materi siap pakai per pertemuan
│   ├── P01/                                    # P01: Understanding Images, Image Processing & EDA
│   └── P02/                                    # P02: Teori Neural Network (51 slide + 30-epoch notebooks)
├── data/
│   ├── sample/                                 # Dataset sintetis & data/mnist/ untuk P01
│   └── frozen_v1/                              # Dataset proyek Frozen v1 (5 kelas, polos vs ramai)
├── results/                                    # Output CSV & grafik eksekusi notebook aktif
└── tools/                                      # Orkestrator build & validator (6 gerbang DoD)
    ├── build_session.py                        # CLI utama build & validasi P01–P08
    ├── init_session.py                         # Scaffolder sesi baru (tools/sessions/ + materials/)
    ├── prepare_frozen_dataset.py               # Konverter dataset Frozen (.HEIC -> .jpg + metadata)
    ├── core/                                   # Mesin standar (shell HTML, exporter, notebook, validator)
    ├── sessions/                               # Kode modular aktif per pertemuan (P02+)
    │   └── p02_teori_neural_network/
    └── legacy_p01/                             # Skrip build P01 yang dipertahankan
```

## Cara Menjalankan / Rebuild Lokal
```bash
pip install -r requirements.txt
python tools/build_session.py P02 --validate
python tools/build_session.py P01 --validate-only
```
