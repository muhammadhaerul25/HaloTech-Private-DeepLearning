"""Scaffold a new standardized session workspace under tools/sessions/P{NN}/ and materials/P{NN}/.

Usage:
    python tools/init_session.py P02
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT_DIR / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from core.registry import SessionConfig, get_session  # noqa: E402


def _assets_template(s: SessionConfig) -> str:
    return f'''"""Generate deterministic visual assets & JSON data for {s.id}: {s.title}.

Outputs saved to `materials/{s.id}/assets/{s.id}/`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from core.registry import get_session  # noqa: E402

SEED = 42
SESSION = get_session("{s.id}")


def main() -> None:
    SESSION.assets_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    meta = {{
        "session": SESSION.id,
        "title": SESSION.title,
        "seed": SEED,
        "sample_check": round(float(rng.random()), 4),
    }}
    out_json = SESSION.assets_dir / "session_data.json"
    out_json.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Aset awal {s.id} siap di: {{SESSION.assets_dir}}")


if __name__ == "__main__":
    main()
'''


def _html_template(s: SessionConfig) -> str:
    return f'''"""Generate interactive HTML5 presentation (SSOT) for {s.id}: {s.title}.

Menggunakan shell standar `tools/core/html_shell.py` (tema Google I/O, timer persisten,
auto-numbering, Q&A reveal, dan kontrak `window.SLIDE_PDF_EXPANDERS`).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from core.html_shell import (  # noqa: E402
    make_agenda_goals_slide,
    make_closing_slide,
    make_cover_roadmap_slide,
    make_divider_slide,
    make_glossary_slide,
    make_handson_step_slide,
    make_qa_slide,
    make_references_slide,
    make_summary_3pillars_slide,
    write_deck_html,
)
from core.registry import get_session  # noqa: E402

SESSION = get_session("{s.id}")
FOOTER = SESSION.short_title


def build_slides_html() -> str:
    # Template Standar P02: ~45–60 slide, total Alokasi waktu tepat 120.0 menit
    # mengikuti docs/PLAN.md ({s.plan_ref}) & docs/STANDAR_MATERI.md.
    slides = [
        f"""
    <!-- 01: COVER (WHITE GOOGLE I/O + 1+4 BENTO SHOWCASE) -->
    <section class="slide active" data-title="Cover — {s.title}" data-notes="Alokasi waktu: 1 menit. Pembukaan sesi {s.id}: {s.title}." style="background: radial-gradient(circle at 82% 46%, rgba(251,188,4,0.14) 0%, rgba(66,133,244,0.10) 32%, rgba(234,67,53,0.05) 56%, #FFFFFF 100%); justify-content: space-between;">
      <div style="position:relative; z-index:1;">
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="display:inline-flex; gap:5px; align-items:center; background:#FFFFFF; border:1px solid #E0E3E7; padding:5px 12px; border-radius:999px; box-shadow:0 2px 6px rgba(0,0,0,0.04);">
            <span style="width:9px; height:9px; border-radius:50%; background:#4285F4;"></span>
            <span style="width:9px; height:9px; border-radius:50%; background:#EA4335;"></span>
            <span style="width:9px; height:9px; border-radius:50%; background:#FBBC04;"></span>
            <span style="width:9px; height:9px; border-radius:50%; background:#34A853;"></span>
            <span style="font-size:11.5px; font-weight:700; letter-spacing:1px; color:#202124; margin-left:4px;">DEEP LEARNING TRACK</span>
          </span>
          <span style="font-size:13.5px; font-weight:600; color:#5F6368;">Fase {s.phase} &nbsp;·&nbsp; 120 Menit</span>
        </div>
      </div>

      <div style="position:relative; z-index:1; margin:auto 0; display:grid; grid-template-columns:1.18fr 0.82fr; gap:24px; align-items:center;">
        <div>
          <h1 style="font-family:var(--font-title); font-size:clamp(28px,3.3vw,42px); font-weight:700; line-height:1.12; color:#202124;">
            {s.id} - {s.title}
          </h1>
          <div style="height:4px; width:100%; max-width:540px; border-radius:999px; margin:12px 0; background:linear-gradient(90deg, #4285F4 0%, #EA4335 35%, #FBBC04 70%, #34A853 100%);"></div>
          <p style="font-size:14.5px; color:#3C4043; line-height:1.48; max-width:540px; margin-bottom:12px;">
            Ringkasan 1 kalimat tujuan utama sesi ini untuk pemula dengan contoh dataset Frozen.
          </p>
          <div style="display:inline-flex; align-items:center; gap:8px; background:#FFFFFF; border:1.5px solid #E0E3E7; border-radius:999px; padding:5px 14px 5px 7px;">
            <span style="width:24px; height:24px; border-radius:50%; background:linear-gradient(135deg, #4285F4, #34A853); color:#FFFFFF; font-family:var(--font-title); font-size:11px; font-weight:700; display:inline-flex; align-items:center; justify-content:center;">MH</span>
            <span style="font-size:13.5px; color:#5F6368;">Presented by <strong style="color:#202124; font-weight:700;">Muhammad Haerul</strong></span>
          </div>
        </div>
        <div class="card" style="padding:14px; border-radius:16px; background:#FFFFFF; box-shadow:0 6px 20px rgba(32,33,36,0.08);">
          <div style="font-family:var(--font-title); font-size:11px; font-weight:700; color:#1A73E8; letter-spacing:0.6px; margin-bottom:8px;">PREVIEW DATASET &amp; TARGET SESI</div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
            <div style="background:#E8F0FE; border-radius:10px; padding:10px; font-size:11.5px; color:#174EA6; font-weight:700;">1. Konsep Inti</div>
            <div style="background:#FCE8E6; border-radius:10px; padding:10px; font-size:11.5px; color:#C5221F; font-weight:700;">2. Simulator</div>
            <div style="background:#FEF7E0; border-radius:10px; padding:10px; font-size:11.5px; color:#B06000; font-weight:700;">3. Dataset Frozen</div>
            <div style="background:#E6F4EA; border-radius:10px; padding:10px; font-size:11.5px; color:#137333; font-weight:700;">4. Praktik Keras</div>
          </div>
        </div>
      </div>
      <div style="display:flex; gap:6px; flex-wrap:wrap;">
        <span class="pill blue">{s.id}</span>
        <span class="pill solid-blue">Deep Learning</span>
        <span class="pill green">Dataset Frozen (5 Kelas)</span>
      </div>
    </section>
""",
        make_agenda_goals_slide(
            footer_label=FOOTER,
            notes="Alokasi waktu: 1 menit. Agenda 120 menit & 3 target belajar utama sesi ini.",
            steps=[
                ("01", "blue", "Pemanasan & Recap", "~10 menit", "Menghubungkan sesi sebelumnya dengan materi hari ini."),
                ("02", "red", "Teori & Simulator Visual", "~45 menit", "Micro-ladder konsep inti dengan simulator interaktif."),
                ("03", "yellow", "Istirahat Singkat", "5 menit", "Jeda 5 menit sebelum masuk ke praktik kode."),
                ("04", "green", "Praktik Terpandu (Visual-First)", "~50 menit", "Hands-on notebook langkah demi langkah pada data Frozen."),
                ("05", "blue", "Evaluasi, Kuis & Penutup", "~10 menit", "Kamus istilah, kuis 5 soal, dan 3 poin utama."),
            ],
            goals=[
                ("Intuisi Konsep", "Memahami konsep inti sesi ini secara intuitif melalui analogi dan simulator interaktif."),
                ("Eksperimen Nyata", "Mengamati langsung perubahan metrik atau representasi visual pada foto dataset Frozen."),
                ("Praktik Mandiri", "Menjalankan notebook hands-on dan menyelesaikan seluruh latihan # TODO dengan mandiri."),
            ],
            rhythm_callout="<strong>Ritme 120 Menit:</strong> Setiap konsep dijelaskan dari contoh konkret terlebih dahulu sebelum menyentuh istilah teknis dan kode.",
        ),
        make_divider_slide(
            bg_class="bg-blue",
            kicker="BAB 1 · KONSEP INTI",
            title="Bab 1: Mulai dari Intuisi",
            description="Lengkapi konten Bab 1 s.d. Bab 4 (~30–40 slide micro-ladder + simulator) sesuai docs/PLAN.md.",
            footer_label=FOOTER,
            data_title="Bab 1 — Pembuka",
            notes="Alokasi waktu: 100 menit. [TEMPLATE SCAFFOLD — pecah alokasi waktu saat melengkapi seluruh slide Bab 1–4]",
        ),
        make_qa_slide(
            qa_id="qa-contoh-1",
            qa_num=1,
            kicker="CEK PEMAHAMAN · CONTOH Q&A STANDAR P02",
            title_html='Pertanyaan Pemantik <span class="hl-blue">Konsep Utama</span>',
            question_html="Contoh pertanyaan Q&amp;A / Kuis dengan pilihan A/B/C yang bisa diklik langsung dan visual yang berubah saat jawaban dibuka.",
            choices=[
                "A. Pilihan pertama (contoh jawaban tepat)",
                "B. Pilihan kedua (miskonsepsi umum)",
                "C. Pilihan ketiga (distraktor)",
            ],
            answer_html="<strong>Jawaban: Pilihan A.</strong><br>Penjelasan ringkas dan ramah pemula mengapa A benar dan B/C kurang tepat.",
            vis_q_html='<div style="text-align:center; padding:18px; color:#5F6368; font-size:13px;">❓ Visual Sebelum Jawaban Dibuka (ganti dengan diagram SVG / kartu data)</div>',
            vis_a_html='<div style="text-align:center; padding:18px; color:#137333; font-size:13px; font-weight:600;">✅ Visual Jawaban Terungkap (highlight bagian kunci)</div>',
            footer_label=FOOTER,
            notes="Alokasi waktu: 2 menit. Diskusikan pilihan A/B/C bersama peserta sebelum membuka penjelasan.",
            bar_color="blue",
            correct_choice="A",
            data_title="Q&A Contoh — Pemahaman Inti",
        ),
        make_cover_roadmap_slide(
            bg_class="bg-green",
            kicker="BAB 5 · PRAKTIK KODE TERPANDU",
            title="Hands-On Notebook",
            description="Mengubah intuisi visual menjadi kode Python pendek pada dataset Frozen (5 kelas).",
            chips=[
                ("Langkah 1", "Muat Foto & Metadata", "Baca foto Frozen dinamis dari DATA_DIR & metadata.csv"),
                ("Langkah 2", "Eksperimen Inti", "Bangun & amati perilaku model dengan output visual"),
                ("Langkah 3", "Evaluasi & Kesimpulan", "Cek akurasi / grafik loss dan jawab Mini-Challenge"),
            ],
            footer_label=FOOTER,
            data_title="Hands-On — Peta Langkah Praktik",
            notes="Alokasi waktu: 2 menit. Perkenalkan peta langkah hands-on sebelum membuka notebook.",
            grid_3x2=False,
            env_strip="<strong>Alat Visualisasi Siap Pakai:</strong> Fungsi plotting tersedia di awal notebook agar sel latihan peserta tetap ringkas (3–12 baris).",
        ),
        make_handson_step_slide(
            step_num=1,
            step_labels=["Muat Data", "Bangun Model", "Latih", "Visualisasi", "Evaluasi"],
            stage_badge="TAHAP 1 · DATA FROZEN",
            title="Membaca Dataset Frozen Secara Dinamis",
            kicker="HANDS-ON LANGKAH 1 · SESUAI SEL LATIHAN 1",
            notebook_name="{s.stem}.ipynb",
            goal_html="Membaca daftar foto dari <code>DATA_DIR</code> dan <code>metadata.csv</code> tanpa hardcode jumlah file.",
            bullets_html="<li>Gunakan <code>CLASS_NAMES = ['anna', 'elsa', 'kristoff', 'olaf', 'sven']</code>.</li><li>Pastikan jumlah baris terbaca dinamis dari folder aktif.</li>",
            code_snippet="# Contoh snippet 3-8 baris (selaras Sel Latihan 1)\\nimport pandas as pd\\nmeta = pd.read_csv(DATA_DIR / 'metadata.csv')\\nprint('Total foto:', len(meta))\\nprint(meta['kelas'].value_counts())",
            callout_html="<strong>Kenapa dinamis?</strong> Jumlah foto dataset Frozen bisa bertambah di versi berikutnya tanpa perlu mengubah kode.",
            color="blue",
            footer_label=FOOTER,
            notes="Alokasi waktu: 8 menit. Arahkan peserta menjalankan setup 3 tahap dan mengisi # TODO 1 di notebook.",
            theory_ref="Bab 1 · Peta Konsep",
        ),
        make_glossary_slide(
            kicker="GLOSARIUM RINGKAS · {s.id}",
            title_html='Kamus Istilah <span class="hl-blue">{s.title}</span>',
            groups=[
                {{
                    "ch": "1",
                    "color": "b1",
                    "label": "Bab 1",
                    "heading": "BAB 1 · ISTILAH INTI",
                    "col": "left",
                    "grow": True,
                    "items": [
                        ("Istilah Teknis 1", "Penjelasan sederhana dalam bahasa Indonesia sehari-hari.", 3, "istilah teknis 1"),
                    ],
                }},
                {{
                    "ch": "5",
                    "color": "b3",
                    "label": "Praktik",
                    "heading": "BAB 5 · PRAKTIK KODE",
                    "col": "right",
                    "grow": True,
                    "items": [
                        ("Dataset Frozen", "Kumpulan foto 5 karakter Frozen (polos & ramai) yang dibaca dinamis.", 6, "dataset frozen"),
                    ],
                }},
            ],
            footer_label=FOOTER,
            notes="Alokasi waktu: 2 menit. Ulas singkat istilah kunci; gunakan filter Bab atau tombol lompat slide (SXX).",
            data_title="Kamus Istilah {s.id}",
        ),
        make_summary_3pillars_slide(
            session_id="{s.id}",
            title_html='3 Poin Utama <span class="hl-blue">{s.title}</span>',
            kicker="RANGKUMAN SESI · {s.id}",
            pillars=[
                {{
                    "bar": "blue",
                    "badge": "INTUISI",
                    "title": "Poin Pilar Pertama",
                    "bullets": ["Ringkas pesan utama pertama untuk peserta pemula."],
                    "foot_cls": "blue",
                    "foot_html": "Kunci: Mulai dari contoh konkret sebelum rumus.",
                }},
                {{
                    "bar": "red",
                    "badge": "MEKANISME",
                    "title": "Poin Pilar Kedua",
                    "bullets": ["Ringkas cara kerja mekanisme inti yang dipelajari hari ini."],
                    "foot_cls": "yellow",
                    "foot_html": "Kunci: Amati visual/simulator per langkah.",
                }},
                {{
                    "bar": "green",
                    "badge": "PRAKTIK",
                    "title": "Poin Pilar Ketiga",
                    "bullets": ["Hubungkan hasil praktik di notebook dengan tujuan proyek Frozen."],
                    "foot_cls": "green",
                    "foot_html": "Kunci: Verifikasi langsung lewat grafik &amp; metrik.",
                }},
            ],
            banner_left_html='<strong style="color:#137333;">Jembatan ke Sesi Berikutnya:</strong> Siapkan pemahaman hari ini sebagai bekal pertemuan berikutnya.',
            banner_quote="Pahami intuisi dari gambar nyata sebelum menulis arsitektur.",
            footer_label=FOOTER,
            notes="Alokasi waktu: 2 menit. Tutup dengan mengulang 3 pilar utama sesi hari ini.",
        ),
        make_closing_slide(
            session_id="{s.id}",
            status_badge="✓ {s.id} Selesai",
            headline_html='<span class="hl-blue">Pesan Penutup Utama</span> untuk Sesi <span class="hl-red">{s.title}</span> dalam Satu Kalimat Jernih.',
            subtext_html='Terima kasih sudah mengikuti sesi <strong style="color:#202124;">{s.id} — {s.title}</strong>!',
            footer_label=FOOTER,
            notes="Alokasi waktu: 2 menit. Apresiasi progres peserta dan beri pratinjau singkat pertemuan berikutnya.",
        ),
        make_references_slide(
            kicker="REFERENSI MATERI · {s.id}",
            title_html='Referensi Bacaan &amp; <span class="hl-blue">Dokumentasi Resmi</span>',
            cards=[
                {{
                    "num": 1,
                    "title": "Sumber Referensi Utama (sesuai docs/PLAN.md) [CEK LINK]",
                    "url": "https://keras.io/guides/",
                    "tag": "Dokumentasi",
                    "tag_cls": "doc",
                    "desc": "Ganti dengan tautan resmi dari docs/PLAN.md untuk {s.id}.",
                    "ctx": "Bab 1–5",
                    "accent": "acc-blue",
                    "featured": True,
                }},
            ],
            route_title="📚 Peta Referensi Mandiri ({s.id})",
            route_steps=[
                ("#1A73E8", "Konsep (#1):", "Rujukan visual tambahan sesuai silabus {s.plan_ref}."),
                ("#C5221F", "Dokumentasi:", "Cek API Keras/TensorFlow yang dipakai di notebook."),
                ("#137333", "Praktik:", "Ulangi eksperimen pada foto polos vs ramai di data/frozen_v1/."),
            ],
            footer_label=FOOTER,
            notes="Alokasi waktu: 0 menit. Referensi opsional sesuai docs/PLAN.md; tandai [CEK LINK] bila belum diverifikasi.",
            data_title="Referensi Materi {s.id}",
        ),
    ]
    return "\\n".join(slides)


def main() -> None:
    out_path, total = write_deck_html(
        SESSION,
        build_slides_html(),
        extra_css="",
        extra_js="",
    )
    print(f"HTML scaffold {s.id} dibuat: {{{{out_path}}}} ({{{{total}}}} slide)")


if __name__ == "__main__":
    main()
'''


def _notebooks_template(s: SessionConfig) -> str:
    return f'''"""Generator notebook peserta & kunci jawaban untuk Hands-on {s.id}: {s.title}.

Mengikuti Standar P02 (Visual-First, cell-by-cell 3–12 baris/sel, Setup 3 tahap,
Alat Visualisasi tersembunyi di sel helper, data Frozen dinamis, # TODO + <details>).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from core.notebook_builder import build_notebook_pair, code, md, setup_cells_standard, todo_block  # noqa: E402
from core.registry import get_session  # noqa: E402

SESSION = get_session("{s.id}")

VIZ_HELPER_CODE = """# Alat bantu visualisasi & pemuat foto siap pakai (cukup jalankan sekali)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

def muat_metadata_frozen(data_dir):
    meta_path = Path(data_dir) / "metadata.csv"
    df = pd.read_csv(meta_path)
    return df

def plot_sebaran_kelas(df, out_path):
    counts = df["kelas"].value_counts().reindex(CLASS_NAMES, fill_value=0)
    fig, ax = plt.subplots(figsize=(6.5, 3.6), dpi=130)
    colors = ["#4285F4", "#EA4335", "#FBBC04", "#34A853", "#8E24AA"]
    ax.bar(counts.index, counts.values, color=colors)
    ax.set_title("Jumlah Foto per Karakter Frozen (Dinamis)")
    ax.set_xlabel("Kelas")
    ax.set_ylabel("Jumlah Foto")
    plt.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.show()
print("✅ Alat visualisasi siap dipakai!")"""


def _execute_notebook_atomic(nb_path: Path) -> None:
    """Opsional: jalankan seluruh sel agar notebook langsung memiliki output nyata (atomic write)."""
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

    with nb_path.open("r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
    ep.preprocess(nb, {{"metadata": {{"path": str(nb_path.parent)}}}})
    tmp_path = nb_path.with_name(f"_tmp_{{nb_path.name}}")
    with tmp_path.open("w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    tmp_path.replace(nb_path)


def build_cells(is_solution: bool) -> list:
    cells = []

    cells.append(
        md(
            """
# Hands-on {s.id}: {s.title}

**Durasi Hands-on:** ±50 menit  
**Gaya Kode (Visual-First):** Sel latihan dibuat **pendek (3–12 baris)** karena fungsi grafik sudah disediakan di bagian **Alat Visualisasi Siap Pakai**.

> **Cara Menjalankan:** Tekan `Shift + Enter` pada setiap sel dari atas ke bawah. Pada versi peserta, isi bagian bertanda `# TODO`.
"""
        )
    )

    cells.extend(setup_cells_standard(use_tensorflow=True))

    cells.append(
        md(
            """
## Alat Visualisasi Siap Pakai
Jalankan sel di bawah ini **satu kali saja** untuk mengaktifkan fungsi bantu grafik agar sel latihan Anda tetap ringkas.
"""
        )
    )
    cells.append(code(VIZ_HELPER_CODE))

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 1 (`# TODO 1`): Membaca Dataset Frozen Secara Dinamis (Slide 06)",
        instruction_md="Lengkapi pemanggilan `muat_metadata_frozen(DATA_DIR)` untuk membaca jumlah foto nyata sesuai `docs/PLAN.md` ({s.plan_ref}).",
        student_code="""
# TODO 1: Muat metadata dataset Frozen secara dinamis dari DATA_DIR
df_meta = None  # TODO

assert df_meta is not None and len(df_meta) > 0, "Metadata kosong!"
print(f"Total foto terbaca: {{len(df_meta)}} | Kelas: {{sorted(df_meta['kelas'].unique())}}")
plot_sebaran_kelas(df_meta, RESULTS_DIR / "{s.id.lower()}_sebaran_kelas.png")
""",
        solution_code="""
# Muat metadata dataset Frozen secara dinamis dari DATA_DIR
df_meta = muat_metadata_frozen(DATA_DIR)

assert df_meta is not None and len(df_meta) > 0, "Metadata kosong!"
print(f"Total foto terbaca: {{len(df_meta)}} | Kelas: {{sorted(df_meta['kelas'].unique())}}")
plot_sebaran_kelas(df_meta, RESULTS_DIR / "{s.id.lower()}_sebaran_kelas.png")
""",
        hint_code="df_meta = muat_metadata_frozen(DATA_DIR)",
        hint_label="Latihan 1",
    )

    return cells


def main() -> None:
    student_nb, solution_nb = build_notebook_pair(SESSION, build_cells)
    if os.environ.get("RUN_OUTPUTS", "0") == "1":
        _execute_notebook_atomic(solution_nb)
        _execute_notebook_atomic(student_nb)


if __name__ == "__main__":
    main()
'''


def _presenter_notes_template(s: SessionConfig) -> str:
    return f'''"""Naskah Penjelasan Detail per Slide untuk {s.id}: {s.title}.

Dipakai oleh:
1. `tools/core/exporter.py` -> Speaker Notes PPTX (100% slide)
2. `tools/core/exporter.py` -> `materials/{s.id}/{s.id}_presenter_script.pdf` (A4 1 slide/halaman)
"""

from __future__ import annotations

SLIDE_EXPLANATIONS: dict[int, list[str]] = {{
    1: [
        "**Judul & Ruang Lingkup Sesi {s.id}:** *{s.title}* (durasi 120 menit).",
        "• Jelaskan benang merah dari sesi sebelumnya ke dataset Frozen 5 kelas.",
    ],
    2: [
        "**Agenda & 3 Target Belajar:** Pandu peserta membaca alur 5 blok waktu + 3 capaian utama.",
    ],
    3: [
        "**Pembuka Bab 1:** Bangun intuisi konkret sebelum menyentuh istilah teknis dan kode.",
    ],
    4: [
        "**Q&A Pemantik:** Minta peserta memilih A/B/C terlebih dahulu sebelum klik 'Lihat Jawaban'.",
    ],
    5: [
        "**Peta Hands-On:** Jelaskan 3 langkah utama yang akan dipraktikkan di notebook.",
    ],
    6: [
        "**Hands-On Langkah 1:** Pastikan peserta menjalankan Setup 3 tahap dan Alat Visualisasi lebih dulu.",
    ],
    7: [
        "**Kamus Istilah:** Gunakan filter Bab atau tombol lompat SXX jika ada istilah yang masih samar.",
    ],
    8: [
        "**3 Poin Utama:** Rangkum Intuisi, Mekanisme, dan Praktik dalam bahasa sederhana.",
    ],
    9: [
        "**Closing:** Beri apresiasi pencapaian peserta dan pratinjau singkat pertemuan berikutnya.",
    ],
    10: [
        "**Referensi (0 menit):** Bahan bacaan opsional sesuai docs/PLAN.md.",
    ],
}}
'''


def scaffold_session(session: SessionConfig, force: bool = False) -> None:
    session.code_dir.mkdir(parents=True, exist_ok=True)
    session.assets_dir.mkdir(parents=True, exist_ok=True)
    session.solutions_dir.mkdir(parents=True, exist_ok=True)

    files = {
        session.code_dir / "__init__.py": f'"""Session {session.id} content builders."""\n',
        session.code_dir / "build_assets.py": _assets_template(session),
        session.code_dir / "build_html.py": _html_template(session),
        session.code_dir / "build_notebooks.py": _notebooks_template(session),
        session.code_dir / "presenter_notes.py": _presenter_notes_template(session),
    }

    for path, content in files.items():
        if path.exists() and not force:
            print(f"Skip (sudah ada): {path.relative_to(ROOT_DIR)}")
            continue
        path.write_text(content, encoding="utf-8")
        print(f"Created: {path.relative_to(ROOT_DIR)}")

    print(
        f"\nScaffold {session.id} siap!\n"
        f"  Folder kode   : {session.code_dir.relative_to(ROOT_DIR)}\n"
        f"  Folder materi : {session.material_dir.relative_to(ROOT_DIR)}\n"
        f"  Perintah build: python tools/build_session.py {session.id} --validate"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Inisialisasi scaffold folder & template sesi baru (P02–P08).")
    parser.add_argument("session", help="ID sesi, mis. P02")
    parser.add_argument("--force", action="store_true", help="Timpa file template yang sudah ada")
    args = parser.parse_args()

    session = get_session(args.session)
    if session.is_legacy_p01:
        raise SystemExit("P01 sudah final dengan skrip eksisting; gunakan init_session.py untuk P02–P08.")
    scaffold_session(session, force=args.force)


if __name__ == "__main__":
    main()
