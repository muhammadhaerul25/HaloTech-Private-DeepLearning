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

from core.html_shell import make_agenda_slide, make_divider_slide, write_deck_html  # noqa: E402
from core.registry import get_session  # noqa: E402

SESSION = get_session("{s.id}")
FOOTER = SESSION.short_title


def build_slides_html() -> str:
    # TODO: Lengkapi seluruh 5 Bab (~45–60 slide, total Alokasi waktu tepat 120.0 menit)
    # mengikuti docs/PLAN.md ({s.plan_ref}) & docs/STANDAR_MATERI.md.
    slides = [
        f"""
    <!-- 01: COVER -->
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

      <div style="position:relative; z-index:1; margin:auto 0;">
        <h1 style="font-family:var(--font-title); font-size:clamp(28px,3.4vw,44px); font-weight:700; line-height:1.12; color:#202124;">
          {s.id} - {s.title}
        </h1>
        <div style="height:4px; width:100%; max-width:580px; border-radius:999px; margin:10px 0 12px; background:linear-gradient(90deg, #4285F4 0%, #EA4335 35%, #FBBC04 70%, #34A853 100%);"></div>
        <div style="margin-top:10px; display:inline-flex; align-items:center; gap:8px; background:#FFFFFF; border:1.5px solid #E0E3E7; border-radius:999px; padding:5px 14px 5px 7px;">
          <span style="width:24px; height:24px; border-radius:50%; background:linear-gradient(135deg, #4285F4, #34A853); color:#FFFFFF; font-family:var(--font-title); font-size:11px; font-weight:700; display:inline-flex; align-items:center; justify-content:center;">MH</span>
          <span style="font-size:13.5px; color:#5F6368;">Presented by <strong style="color:#202124; font-weight:700;">Muhammad Haerul</strong></span>
        </div>
      </div>
      <div style="display:flex; gap:6px; flex-wrap:wrap;">
        <span class="pill blue">{s.id}</span>
        <span class="pill solid-blue">Python</span>
      </div>
    </section>
""",
        make_agenda_slide(
            footer_label=FOOTER,
            notes="Alokasi waktu: 1 menit. Agenda 120 menit sesi hari ini.",
            blocks=[
                ("blue", "00–10 · Pemanasan", "Recap sesi sebelumnya dan pertanyaan pemantik."),
                ("red", "10–40 · Teori & Simulator", "Konsep inti visual dengan simulator interaktif."),
                ("yellow", "40–45 · Istirahat Singkat", "Jeda 5 menit sebelum sesi praktik kode."),
                ("green", "45–95 · Praktik Terpandu", "Hands-on notebook langkah demi langkah."),
                ("blue", "95–110 · Mini-Challenge", "Latihan singkat dan diskusi intuisi."),
                ("red", "110–120 · Kuis & Penutup", "Kuis interaktif 5 soal, rangkuman, dan tugas."),
            ],
        ),
        make_divider_slide(
            bg_class="bg-blue",
            kicker="BAB 1 · KONSEP INTI",
            title="Bab 1: Mulai dari Intuisi",
            description="Lengkapi konten Bab 1 s.d. Bab 5 sesuai docs/PLAN.md.",
            footer_label=FOOTER,
            data_title="Bab 1 — Pembuka",
            notes="Alokasi waktu: 118 menit. [TEMPLATE SCAFFOLD — ganti alokasi saat isi slide lengkap]",
        ),
    ]
    return "\n".join(slides)


def main() -> None:
    out_path, total = write_deck_html(
        SESSION,
        build_slides_html(),
        extra_css="",
        extra_js="",
    )
    print(f"HTML scaffold {s.id} dibuat: {{out_path}} ({{total}} slide)")


if __name__ == "__main__":
    main()
'''


def _notebooks_template(s: SessionConfig) -> str:
    return f'''"""Generator notebook peserta & kunci jawaban untuk Hands-on {s.id}: {s.title}.

Mengikuti standar ultra awam-friendly (cell-by-cell, 5–15 baris/sel, Setup 3 tahap,
# TODO + <details> Hint & Jawaban, lolos SMOKE_TEST=1).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from core.notebook_builder import build_notebook_pair, code, md, setup_cells_standard, todo_block  # noqa: E402
from core.registry import get_session  # noqa: E402

SESSION = get_session("{s.id}")


def build_cells(is_solution: bool) -> list:
    cells = []

    cells.append(
        md(
            """
# Hands-on {s.id}: {s.title}

**Durasi Hands-on:** ±50 menit  
**Gaya Kode:** Ramah pemula — setiap sel kode dibuat **pendek (5–15 baris)**, satu sel hanya melakukan **satu tugas sederhana**, dan setiap baris dilengkapi komentar (`# ...`).

> **Cara Menjalankan:** Tekan `Shift + Enter` pada setiap sel dari atas ke bawah. Pada versi peserta, isi bagian bertanda `# TODO`.
"""
        )
    )

    cells.extend(setup_cells_standard(use_tensorflow=True))

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 1 (`# TODO 1`): Contoh Kerangka Latihan",
        instruction_md="Ganti placeholder ini dengan latihan nyata sesuai `docs/PLAN.md` ({s.plan_ref}).",
        student_code="""
# TODO 1: Lengkapi nilai variabel contoh
hasil = None  # TODO

assert hasil == 42
print("✅ Cek Latihan 1 lolos!")
""",
        solution_code="""
# Contoh solusi awal (ganti saat menyusun konten {s.id})
hasil = 42

assert hasil == 42
print("✅ Cek Latihan 1 lolos!")
""",
        hint_code="hasil = 42",
        hint_label="Latihan 1",
    )

    return cells


def main() -> None:
    build_notebook_pair(SESSION, build_cells)


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
        "• Lengkapi poin penjelasan detail per slide 1..N sesuai isi HTML final.",
    ],
    2: [
        "**Alokasi Waktu 120 Menit:** Mengikuti template standar 6 blok waktu.",
    ],
    3: [
        "**Pengantar Bab 1:** Scaffold awal — lengkapi saat produksi konten {s.id}.",
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
