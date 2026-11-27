"""Interactive HTML Deck Builder for P03: Arsitektur Neural Network (52 Slides · 120.0 Min).

Follows the P02-Standard Architecture (Google I/O White Bento bookends, 5-Architecture
Evolutionary Dissection, Dual Animation Contract, Visual-First Hands-On, and Atomic Export).
"""

from __future__ import annotations

import json
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

SESSION = get_session("P03")
FOOTER = SESSION.short_title
ASSETS_DIR = SESSION.assets_dir

EXTRA_CSS = """
    .arch-flow {
      display: flex; align-items: center; gap: 6px; flex-wrap: nowrap;
      padding: 8px 10px; background: #F8F9FA; border: 1.4px solid #E0E3E7;
      border-radius: 12px; justify-content: space-between;
    }
    .arch-node {
      flex: 1; min-width: 0; border-radius: 10px; padding: 7px 8px;
      text-align: center; border: 1.5px solid #DADCE0; background: #FFFFFF;
    }
    .arch-node.blue { background: #E8F0FE; border-color: #8AB4F8; color: #174EA6; }
    .arch-node.red { background: #FCE8E6; border-color: #F28B82; color: #C5221F; }
    .arch-node.yellow { background: #FEF7E0; border-color: #FDD663; color: #B06000; }
    .arch-node.green { background: #E6F4EA; border-color: #81C995; color: #137333; }
    .arch-node.dark { background: #202124; border-color: #202124; color: #FFFFFF; }
    .arch-node-ttl { font-family: var(--font-title); font-size: 11px; font-weight: 700; line-height: 1.2; }
    .arch-node-sub { font-family: var(--font-code); font-size: 9.5px; opacity: 0.9; margin-top: 2px; }
    .arch-arr { font-weight: 800; color: #5F6368; font-size: 14px; flex-shrink: 0; }

    .evo-track {
      display: grid; grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 9px; flex: 1; min-height: 0; margin-top: 6px;
    }
    .evo-card {
      background: #FFFFFF; border: 1.5px solid #DADCE0; border-radius: 14px;
      padding: 11px 11px 10px; display: flex; flex-direction: column;
      justify-content: space-between; gap: 6px; position: relative; overflow: hidden;
    }
    .evo-gen { font-family: var(--font-code); font-size: 9.5px; font-weight: 700; padding: 2px 7px; border-radius: 999px; width: fit-content; }
    .evo-name { font-family: var(--font-title); font-size: 13.8px; font-weight: 700; color: #202124; line-height: 1.2; }
    .evo-prob { font-size: 11px; line-height: 1.42; color: #C5221F; background: #FCE8E6; border: 1px solid #FAD2CF; border-radius: 9px; padding: 8px 9px; flex: 1; display: grid; place-items: center start; }
    .evo-sol { font-size: 11px; line-height: 1.42; color: #137333; background: #E6F4EA; border: 1px solid #CEEAD6; border-radius: 9px; padding: 8px 9px; flex: 1; display: grid; place-items: center start; }
    .evo-stat { font-family: var(--font-code); font-size: 9.6px; font-weight: 700; color: #3C4043; background: #F1F3F4; border-radius: 7px; padding: 5px 7px; text-align: center; }

    .card-tint { border-radius: 12px; border: 1.4px solid #DADCE0; background: #F8F9FA; }
    .card-tint.blue { background: var(--tint-blue); border-color: #C6DAFC; }
    .card-tint.red { background: var(--tint-red); border-color: #F6AEA9; }
    .card-tint.yellow { background: var(--tint-yellow); border-color: #FDE293; }
    .card-tint.green { background: var(--tint-green); border-color: #A8DAB5; }

    .kpi-row { display: inline-flex; gap: 6px; align-items: center; margin-left: auto; flex-wrap: nowrap; }
    .kpi-chip { background: #F1F3F4; border: 1.2px solid #DADCE0; border-radius: 999px; padding: 3.5px 10px; font-family: var(--font-code); font-size: 10.5px; font-weight: 700; color: #202124; white-space: nowrap; }
    .sim-bar .btn-ui { padding: 5.5px 11px; font-size: 11.4px; border-radius: 9px; }

    .uc-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 11px; }
    .uc-card { background: #FFFFFF; border: 1.4px solid #DADCE0; border-radius: 13px; padding: 11px 13px; display: flex; flex-direction: column; gap: 5px; }
    .verdict-box {
      border-radius: 14px; padding: 11px 15px; display: flex; align-items: center;
      justify-content: space-between; gap: 14px; border: 1.5px solid #DADCE0;
    }
    .verdict-box.avoid { background: #FCE8E6; border-color: #F6AEA9; border-left: 6px solid #EA4335; }
    .verdict-box.foundation { background: #E8F0FE; border-color: #C6DAFC; border-left: 6px solid #4285F4; }
    .verdict-box.bench { background: #FEF7E0; border-color: #FDE293; border-left: 6px solid #FBBC04; }
    .verdict-box.winner { background: #E6F4EA; border-color: #A8DAB5; border-left: 6px solid #34A853; }
    .verdict-box.runner { background: #F3E8FD; border-color: #D7AEFB; border-left: 6px solid #8E24AA; }

    .cmp-table { width: 100%; border-collapse: collapse; font-size: 11.4px; background: #FFFFFF; border-radius: 12px; overflow: hidden; border: 1px solid #DADCE0; }
    .cmp-table th { background: #202124; color: #FFFFFF; font-family: var(--font-title); font-size: 10.6px; text-align: left; padding: 7px 9px; }
    .cmp-table td { padding: 6.5px 9px; border-bottom: 1px solid #EEF0F3; color: #202124; }
    .cmp-table tr:nth-child(even) td { background: #FAFBFD; }
    .cmp-table tr.row-winner td { background: #E6F4EA; font-weight: 600; }

    .cnn-canvas-strip { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; align-items: stretch; }
    .cnn-can-card { background: #F8F9FA; border: 1.4px solid #DADCE0; border-radius: 12px; padding: 8px; display: flex; flex-direction: column; align-items: center; gap: 5px; }
    .cnn-can-card canvas { border-radius: 8px; border: 1px solid #DADCE0; background: #FFFFFF; image-rendering: pixelated; }

    .signal-bar-row { display: grid; grid-template-columns: 74px 1fr 48px; align-items: center; gap: 8px; font-size: 11px; }
    .signal-track { height: 14px; background: #F1F3F4; border-radius: 999px; overflow: hidden; border: 1px solid #E0E3E7; }
    .signal-fill { height: 100%; border-radius: 999px; transition: width 0.28s ease, background 0.28s ease; }

    @keyframes pulseDotLoop {
      0%, 100% { transform: scale(1); opacity: 0.78; }
      50% { transform: scale(1.12); opacity: 1; }
    }
    .ambient-pulse { animation: pulseDotLoop 2.4s ease-in-out infinite; transform-origin: center; }
    @media print {
      .ambient-pulse { animation: none !important; opacity: 1 !important; transform: none !important; }
    }
"""


def _bench_dict(data: dict) -> dict[str, dict]:
    return {row["architecture"]: row for row in data["benchmarks"]}


def _arch_badge_row(gen_label: str, color: str, steps: list[tuple[str, str, str]]) -> str:
    parts = []
    for idx, (col_cls, ttl, sub) in enumerate(steps):
        if idx > 0:
            parts.append('<span class="arch-arr">&#8594;</span>')
        parts.append(
            f'<div class="arch-node {col_cls}">'
            f'<div class="arch-node-ttl">{ttl}</div>'
            f'<div class="arch-node-sub">{sub}</div>'
            f'</div>'
        )
    return f"""
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">
        <span class="pill {color}" style="font-size:10px; padding:2px 9px;">{gen_label}</span>
        <span style="font-family:var(--font-code); font-size:10px; color:#5F6368;">Aliran Tensor Data Frozen (5 Kelas Output)</span>
      </div>
      <div class="arch-flow">{''.join(parts)}</div>
    """


def build_slides_html(data: dict) -> str:
    b = _bench_dict(data)
    r_mlp = b["1. MLP (2 Hidden)"]
    r_cnn = b["2. CNN Klasik"]
    r_res = b["3. ResNet50"]
    r_mob = b["4. MobileNetV2"]
    r_eff = b["5. EfficientNetB0"]

    tot_imgs = data["total_images"]
    n_polos = data["condition_counts"]["polos"]
    n_ramai = data["condition_counts"]["ramai"]
    p02_p = data["p02_1layer_params"]
    sh = data["shift_test_64"]
    tr = data["train_traces_64"]

    ho_steps = ["1. MLP", "2. Conv+Pool", "3. CNN Klasik", "4. Mini-ResNet", "5. MobileNet/Eff", "6. Benchmark"]

    slides: list[str] = []

    # ------------------------------------------------------------------
    # S01: COVER (WHITE GOOGLE I/O + 1+4 FROZEN BENTO)
    # ------------------------------------------------------------------
    slides.append(f"""
    <section class="slide active" data-title="Cover — Arsitektur Neural Network" data-notes="Alokasi waktu: 1 menit. Pembukaan sesi P03: Arsitektur Neural Network — membedah evolusi 5 arsitektur utama pada dataset Disney Frozen." style="background: radial-gradient(circle at 82% 44%, rgba(251,188,4,0.16) 0%, rgba(66,133,244,0.10) 34%, rgba(52,168,83,0.06) 62%, #FFFFFF 100%); justify-content: space-between; overflow:hidden;">
      <svg viewBox="0 0 960 540" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:0;">
        <circle cx="888" cy="78" r="22" fill="none" stroke="#EA4335" stroke-width="2.5" opacity="0.55"/>
        <rect x="615" y="42" width="20" height="20" rx="6" transform="rotate(-14 625 52)" fill="none" stroke="#4285F4" stroke-width="2.2" opacity="0.55"/>
        <polygon points="468,54 484,82 452,82" fill="none" stroke="#34A853" stroke-width="2.4" opacity="0.55"/>
        <circle cx="904" cy="438" r="14" fill="none" stroke="#FBBC04" stroke-width="2.4" opacity="0.65"/>
      </svg>

      <div style="position:relative; z-index:1; display:flex; align-items:center; justify-content:space-between;">
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="display:inline-flex; gap:5px; align-items:center; background:#FFFFFF; border:1px solid #E0E3E7; padding:5px 12px; border-radius:999px; box-shadow:0 2px 6px rgba(0,0,0,0.04);">
            <span style="width:9px; height:9px; border-radius:50%; background:#4285F4;"></span>
            <span style="width:9px; height:9px; border-radius:50%; background:#EA4335;"></span>
            <span style="width:9px; height:9px; border-radius:50%; background:#FBBC04;"></span>
            <span style="width:9px; height:9px; border-radius:50%; background:#34A853;"></span>
            <span style="font-size:11.5px; font-weight:700; letter-spacing:1px; color:#202124; margin-left:4px;">DEEP LEARNING TRACK</span>
          </span>
          <span style="font-size:13.5px; font-weight:600; color:#5F6368;">Fase Fondasi &nbsp;·&nbsp; 120 Menit</span>
        </div>
        <span class="pill yellow" style="font-size:10.5px;">Evolusi 5 Arsitektur CV</span>
      </div>

      <div style="position:relative; z-index:1; margin:auto 0; display:grid; grid-template-columns:1.10fr 0.90fr; gap:24px; align-items:center;">
        <div>
          <h1 style="font-family:var(--font-title); font-size:clamp(31px,3.6vw,46px); font-weight:700; line-height:1.10; color:#202124; letter-spacing:-0.4px;">
            P03 &mdash; Arsitektur<br/><span style="color:#1A73E8;">Neural</span> <span style="color:#EA4335;">Network</span>
          </h1>
          <div style="height:4px; width:100%; max-width:500px; border-radius:999px; margin:12px 0; background:linear-gradient(90deg, #4285F4 0%, #EA4335 35%, #FBBC04 70%, #34A853 100%);"></div>
          <p style="font-size:14.2px; color:#3C4043; line-height:1.48; max-width:500px; margin-bottom:14px;">
            Bedah tuntas evolusi <strong>5 arsitektur</strong> relevan proyek Frozen (<strong>MLP &#8594; CNN Klasik &#8594; ResNet &#8594; MobileNetV2 &#8594; EfficientNet</strong>): anatomi, fitur khusus, simulasi penuh, hingga <em>use case</em> nyata.
          </p>
          <div style="display:inline-flex; align-items:center; gap:8px; background:#FFFFFF; border:1.5px solid #E0E3E7; border-radius:999px; padding:5px 14px 5px 7px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <span style="width:24px; height:24px; border-radius:50%; background:linear-gradient(135deg, #4285F4, #34A853); color:#FFFFFF; font-family:var(--font-title); font-size:11px; font-weight:700; display:inline-flex; align-items:center; justify-content:center;">MH</span>
            <span style="font-size:13.5px; color:#5F6368;">Presented by <strong style="color:#202124; font-weight:700;">Muhammad Haerul</strong></span>
          </div>
        </div>

        <div class="card" style="padding:12px 13px; border-radius:16px; background:#FFFFFF; box-shadow:0 8px 26px rgba(32,33,36,0.09); display:flex; flex-direction:column; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-family:var(--font-title); font-size:10.2px; font-weight:700; color:#1A73E8; letter-spacing:0.4px;">DATASET PROYEK · {tot_imgs} FOTO FROZEN</span>
            <span class="pill blue" style="font-size:9.2px; padding:1.5px 8px;">5 Kelas</span>
          </div>
          <div style="display:grid; grid-template-columns:1.12fr 0.88fr; gap:7px; height:172px;">
            <div style="position:relative; border-radius:10px; overflow:hidden; border:2.2px solid #4285F4;">
              <img src="assets/P03/thumb_elsa_ramai.jpg" alt="Elsa Ramai" style="width:100%; height:100%; object-fit:cover; display:block;"/>
              <span style="position:absolute; bottom:6px; left:6px; background:#1A73E8; color:#FFF; font-family:var(--font-title); font-size:9.2px; font-weight:700; padding:2px 8px; border-radius:999px;">Elsa · Ramai</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; grid-template-rows:1fr 1fr; gap:6px; min-height:0;">
              <div style="position:relative; border-radius:8px; overflow:hidden; border:1.8px solid #EA4335;">
                <img src="assets/P03/thumb_anna.jpg" alt="Anna" style="width:100%; height:100%; object-fit:cover; display:block;"/>
                <span style="position:absolute; bottom:3px; left:3px; background:#EA4335; color:#FFF; font-family:var(--font-title); font-size:8px; font-weight:700; padding:1px 5px; border-radius:999px;">Anna</span>
              </div>
              <div style="position:relative; border-radius:8px; overflow:hidden; border:1.8px solid #34A853;">
                <img src="assets/P03/thumb_olaf.jpg" alt="Olaf" style="width:100%; height:100%; object-fit:cover; display:block;"/>
                <span style="position:absolute; bottom:3px; left:3px; background:#137333; color:#FFF; font-family:var(--font-title); font-size:8px; font-weight:700; padding:1px 5px; border-radius:999px;">Olaf</span>
              </div>
              <div style="position:relative; border-radius:8px; overflow:hidden; border:1.8px solid #FBBC04;">
                <img src="assets/P03/thumb_kristoff.jpg" alt="Kristoff" style="width:100%; height:100%; object-fit:cover; display:block;"/>
                <span style="position:absolute; bottom:3px; left:3px; background:#FBBC04; color:#202124; font-family:var(--font-title); font-size:8px; font-weight:700; padding:1px 5px; border-radius:999px;">Kristoff</span>
              </div>
              <div style="position:relative; border-radius:8px; overflow:hidden; border:1.8px solid #4285F4;">
                <img src="assets/P03/thumb_sven.jpg" alt="Sven" style="width:100%; height:100%; object-fit:cover; display:block;"/>
                <span style="position:absolute; bottom:3px; left:3px; background:#1A73E8; color:#FFF; font-family:var(--font-title); font-size:8px; font-weight:700; padding:1px 5px; border-radius:999px;">Sven</span>
              </div>
            </div>
          </div>
          <div style="display:grid; grid-template-columns:repeat(5, minmax(0, 1fr)); gap:4px; text-align:center; padding-top:4px; border-top:1px dashed #E8EAED;">
            <span style="background:#FCE8E6; color:#C5221F; font-family:var(--font-code); font-size:8.8px; font-weight:700; padding:3.5px 2px; border-radius:6px;">1. MLP</span>
            <span style="background:#E8F0FE; color:#1A73E8; font-family:var(--font-code); font-size:8.8px; font-weight:700; padding:3.5px 2px; border-radius:6px;">2. CNN</span>
            <span style="background:#FEF7E0; color:#B06000; font-family:var(--font-code); font-size:8.8px; font-weight:700; padding:3.5px 2px; border-radius:6px;">3. ResNet</span>
            <span style="background:#E6F4EA; color:#137333; font-family:var(--font-code); font-size:8.8px; font-weight:700; padding:3.5px 2px; border-radius:6px;">4. MobV2</span>
            <span style="background:#F3E8FD; color:#681DA8; font-family:var(--font-code); font-size:8.8px; font-weight:700; padding:3.5px 2px; border-radius:6px;">5. EffNet</span>
          </div>
        </div>
      </div>

      <div style="position:relative; z-index:1; display:flex; gap:6px; flex-wrap:wrap;">
        <span class="pill blue">P03 · Fondasi</span>
        <span class="pill red">MLP &#8594; CNN &#8594; ResNet</span>
        <span class="pill green">MobileNetV2 &amp; EfficientNet</span>
        <span class="pill yellow">5 Simulator Interaktif</span>
        <span class="pill solid-blue">Keras Benchmark</span>
      </div>
    </section>
""")

    # ------------------------------------------------------------------
    # S02: AGENDA + LEARNING GOALS
    # ------------------------------------------------------------------
    slides.append(
        make_agenda_goals_slide(
            footer_label=FOOTER,
            notes="Alokasi waktu: 1 menit. Peta belajar 120 menit P03: pemanasan P02, bedah evolusi 5 arsitektur, praktik Keras 6 langkah, dan evaluasi kuis.",
            title_html='Agenda 120 Menit &amp; <span class="hl-blue">3 Target Belajar</span>',
            steps=[
                ("01", "blue", "Pemanasan & Peta Evolusi", "~6 menit", "Kenapa model 1-layer P02 mentok dan bagaimana 5 generasi berevolusi."),
                ("02", "red", "Bedah 5 Arsitektur + 5 Simulator", "~46 menit", "MLP, CNN Klasik, ResNet, MobileNetV2, EfficientNet (4 sudut + simulator)."),
                ("03", "yellow", "Istirahat Singkat", "5 menit", "Jeda segar 5 menit sebelum masuk ke sesi praktik notebook Keras."),
                ("04", "green", "Hands-On Keras & Mini-Challenge", "~48 menit", "Bangun 6 langkah & benchmark 5 arsitektur pada foto Frozen (weights=None)."),
                ("05", "blue", "Kamus 18 Istilah, Kuis 5 Soal & Penutup", "~15 menit", "Ulas istilah inti, kuis interaktif 5 soal, 3 poin utama, & jembatan P04."),
            ],
            goals=[
                ("Alasan Evolusi", "Menjelaskan <strong>masalah konkret</strong> yang memicu lahirnya tiap generasi baru dari MLP hingga EfficientNet."),
                ("Anatomi & Fitur Khusus", "Membedah cara kerja <em>Kernel</em>, <em>Skip Connection</em>, <em>Depthwise Conv</em>, &amp; <em>SE Attention</em> lewat simulator interaktif."),
                ("Benchmark Nyata Frozen", "Membandingkan parameter, ukuran MB, &amp; latensi di Keras untuk membuktikan keunggulan <strong>MobileNetV2</strong>."),
            ],
            rhythm_callout="<strong>Pola Konsisten 5 Arsitektur:</strong> Tiap model dibedah 4 langkah seragam: <em>In General &#8594; Fitur Khusus &#8594; Simulasi Full &#8594; Use Case Proyek</em>.",
        )
    )

    # ------------------------------------------------------------------
    # S03: PEMANASAN — TITIK MENTOK MODEL 1-LAYER P02
    # ------------------------------------------------------------------
    slides.append(f"""
    <section class="slide" data-title="Pemanasan — Titik Mentok Model P02" data-notes="Alokasi waktu: 2 menit. Recap nyata titik akhir P02: model Dense 1-layer melesat menjadi 9.64M param jika ditambah MLP Dense, dan rentan terhadap pergeseran posisi.">
      <div class="kicker">PEMANASAN · REKAP P02 KE P03</div>
      <h2>Kenapa Model 1-Layer P02 Butuh <span class="hl-red">Arsitektur Lebih Cerdas</span>?</h2>
      <div class="split-60-40" style="grid-template-columns:1.12fr 0.88fr; flex:1; min-height:0; align-items:stretch;">
        <div style="display:flex; flex-direction:column; gap:9px; min-height:0;">
          <div class="card" style="flex:1; padding:11px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:8px; min-height:0;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="font-family:var(--font-title); font-size:12.6px; color:#202124;">Bukti Eksperimen Nyata pada {tot_imgs} Foto Frozen</strong>
              <span class="pill red" style="font-size:9.5px; padding:2px 8px;">Hasil Eksekusi TensorFlow</span>
            </div>
            <div style="flex:1; min-height:0; display:flex; align-items:center; justify-content:center;">
              <img src="assets/P03/01_p02_handoff_limit.png" alt="Batas Parameter dan Pergeseran MLP vs CNN" style="width:100%; height:100%; max-height:245px; border-radius:9px; object-fit:contain;"/>
            </div>
            <div style="background:#FFF8E1; border:1px solid #FDE293; border-radius:8px; padding:6px 10px; font-size:11.2px; color:#3C4043;">
              <strong style="color:#B06000;">Kesimpulan Visual:</strong> CNN 3-blok memotong bobot ~<strong>95×</strong> &amp; mempertahankan akurasi saat posisi bergeser <code>8px</code>!
            </div>
          </div>
          <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:8px;">
            <div class="mini-box" style="text-align:center; padding:7px 5px;"><div style="font-family:var(--font-title); font-size:14.5px; font-weight:800; color:#B06000;">{p02_p:,}</div><div style="font-size:9.8px; color:#5F6368;">1-Layer P02</div></div>
            <div class="mini-box" style="text-align:center; padding:7px 5px;"><div style="font-family:var(--font-title); font-size:14.5px; font-weight:800; color:#C5221F;">{r_mlp['total_params']/1e6:.2f}M</div><div style="font-size:9.8px; color:#5F6368;">MLP 2-Hidden</div></div>
            <div class="mini-box" style="text-align:center; padding:7px 5px;"><div style="font-family:var(--font-title); font-size:14.5px; font-weight:800; color:#137333;">{sh['cnn_val_acc']}% &#8594; {sh['cnn_shift6px_acc']}%</div><div style="font-size:9.8px; color:#5F6368;">CNN Geser 8px</div></div>
            <div class="mini-box" style="text-align:center; padding:7px 5px;"><div style="font-family:var(--font-title); font-size:14.5px; font-weight:800; color:#1A73E8;">{n_polos} / {n_ramai}</div><div style="font-size:9.8px; color:#5F6368;">Polos vs Ramai</div></div>
          </div>
        </div>

        <div class="card surface" style="justify-content:space-between; padding:14px 16px; gap:8px; height:100%;">
          <div class="card-top-bar bar-red"></div>
          <div style="font-family:var(--font-title); font-size:13.5px; font-weight:700; color:#202124;">3 Batas Nyata yang Kita Bawa dari P02</div>
          <div style="display:flex; flex-direction:column; gap:8px; flex:1; justify-content:space-between;">
            <div class="card-tint red" style="padding:10px 12px; flex:1; display:flex; flex-direction:column; justify-content:center;">
              <div class="card-title" style="color:#C5221F; font-size:12.8px;">1. Pita 1D (<code>Flatten</code>) Buta Pola 2D</div>
              <p class="card-text" style="font-size:11.6px; margin-top:3px;">Meluruskan foto menjadi <code>150.528</code> angka memisahkan piksel mata/gaun yang bertetangga; bobot terikat posisi kaku.</p>
            </div>
            <div class="card-tint yellow" style="padding:10px 12px; flex:1; display:flex; flex-direction:column; justify-content:center;">
              <div class="card-title" style="color:#B06000; font-size:12.8px;">2. Ledakan Bobot &amp; Rentan Latar Ramai</div>
              <p class="card-text" style="font-size:11.6px; margin-top:3px;">Menambah Hidden Dense langsung membengkakkan bobot ke <code>{r_mlp['total_params']:,}</code>, tapi akurasi uji <code>48×48</code> mandek di <code>{sh['mlp_val_acc']}%</code>.</p>
            </div>
            <div class="card-tint blue" style="padding:10px 12px; flex:1; display:flex; flex-direction:column; justify-content:center;">
              <div class="card-title" style="color:#1A73E8; font-size:12.8px;">3. Risiko Overfit di Data Kecil ({tot_imgs} Foto)</div>
              <p class="card-text" style="font-size:11.6px; margin-top:3px;">Jutaan bobot bebas cepat menghafal warna latar <em>shortcut</em> ketimbang bentuk figurin Frozen.</p>
            </div>
          </div>
          <div class="callout" style="padding:8px 11px; font-size:11.6px;">
            <strong>Pertanyaan Besar P03:</strong> Bagaimana evolusi arsitektur memecahkan ketiganya sekaligus?
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # ------------------------------------------------------------------
    # S04: PETA BESAR EVOLUSI 5 ARSITEKTUR
    # ------------------------------------------------------------------
    slides.append(f"""
    <section class="slide" data-title="Peta Evolusi 5 Arsitektur" data-notes="Alokasi waktu: 2 menit. Tunjukkan alur evolusi 5 arsitektur dari MLP -> CNN Klasik -> ResNet -> MobileNetV2 -> EfficientNet dengan diagram mini blok dan perbandingan parameter.">
      <div class="kicker">PETA EVOLUSI · MASALAH &#8594; SOLUSI GENERASI BARU</div>
      <h2>5 Arsitektur Relevan: <span class="hl-blue">Evolusi dari MLP hingga EfficientNet</span></h2>
      <div class="evo-track">
        <div class="evo-card">
          <div class="card-top-bar bar-red"></div>
          <div>
            <span class="evo-gen" style="background:#FCE8E6; color:#C5221F;">GEN #1 · ERA DENSE</span>
            <div class="evo-name" style="margin-top:4px;">1. MLP</div>
            <div style="font-size:10.2px; color:#5F6368;">Multi-Layer Perceptron</div>
          </div>
          <svg viewBox="0 0 150 64" style="width:100%; height:64px; background:#FAFBFD; border-radius:8px; border:1px solid #EEF0F3;">
            <g stroke="#DADCE0" stroke-width="1">
              <line x1="28" y1="16" x2="75" y2="20"/><line x1="28" y1="16" x2="75" y2="44"/>
              <line x1="28" y1="32" x2="75" y2="20"/><line x1="28" y1="32" x2="75" y2="44"/>
              <line x1="28" y1="48" x2="75" y2="20"/><line x1="28" y1="48" x2="75" y2="44"/>
              <line x1="75" y1="20" x2="122" y2="22"/><line x1="75" y1="20" x2="122" y2="42"/>
              <line x1="75" y1="44" x2="122" y2="22"/><line x1="75" y1="44" x2="122" y2="42"/>
            </g>
            <g fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.5"><circle cx="28" cy="16" r="5"/><circle cx="28" cy="32" r="5"/><circle cx="28" cy="48" r="5"/></g>
            <g fill="#FCE8E6" stroke="#EA4335" stroke-width="1.5"><circle cx="75" cy="20" r="6"/><circle cx="75" cy="44" r="6"/></g>
            <g fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"><circle cx="122" cy="22" r="5.5"/><circle cx="122" cy="42" r="5.5"/></g>
          </svg>
          <div class="evo-sol"><div><strong>Obat P02:</strong> Tambah <em>Hidden Layer</em> non-linear agar bisa rangkai fitur bertingkat.</div></div>
          <div class="evo-prob"><div><strong>Cacat Baru:</strong> Boros bobot (<code>9.64M</code>) &amp; buta posisi 2D piksel.</div></div>
          <div class="evo-stat">{r_mlp['total_params']:,} param · {r_mlp['est_size_mb']} MB</div>
        </div>

        <div class="evo-card">
          <div class="card-top-bar bar-blue"></div>
          <div>
            <span class="evo-gen" style="background:#E8F0FE; color:#1A73E8;">GEN #2 · CONVNET</span>
            <div class="evo-name" style="margin-top:4px;">2. CNN Klasik</div>
            <div style="font-size:10.2px; color:#5F6368;">Era LeNet &#8594; VGG</div>
          </div>
          <svg viewBox="0 0 150 64" style="width:100%; height:64px; background:#FAFBFD; border-radius:8px; border:1px solid #EEF0F3;">
            <rect x="12" y="10" width="38" height="44" rx="4" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.5"/>
            <rect x="18" y="16" width="14" height="14" rx="2" fill="rgba(234,67,53,0.22)" stroke="#EA4335" stroke-width="1.5"/>
            <path d="M54 32 L68 32" stroke="#5F6368" stroke-width="1.6"/>
            <rect x="72" y="14" width="26" height="36" rx="4" fill="#D2E3FC" stroke="#1A73E8" stroke-width="1.5"/>
            <path d="M102 32 L114 32" stroke="#5F6368" stroke-width="1.6"/>
            <rect x="118" y="21" width="20" height="22" rx="4" fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"/>
            <text x="128" y="35" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" font-weight="700" fill="#137333">Pool</text>
          </svg>
          <div class="evo-sol"><div><strong>Obat #1:</strong> Pakai <code>Conv2D 3×3</code> &amp; <code>Pooling</code>! Filter sama geser ke seluruh foto.</div></div>
          <div class="evo-prob"><div><strong>Cacat Baru:</strong> Jaringan dalam sulit dilatih (<em>Vanishing Gradient</em>).</div></div>
          <div class="evo-stat">{r_cnn['total_params']:,} param (3-blok)</div>
        </div>

        <div class="evo-card">
          <div class="card-top-bar bar-yellow"></div>
          <div>
            <span class="evo-gen" style="background:#FEF7E0; color:#B06000;">GEN #3 · RESIDUAL</span>
            <div class="evo-name" style="margin-top:4px;">3. ResNet</div>
            <div style="font-size:10.2px; color:#5F6368;">Skip Connection + GAP</div>
          </div>
          <svg viewBox="0 0 150 64" style="width:100%; height:64px; background:#FAFBFD; border-radius:8px; border:1px solid #EEF0F3;">
            <path d="M 22 44 Q 75 6 126 36" fill="none" stroke="#FBBC04" stroke-width="2.4" stroke-dasharray="4,2"/>
            <rect x="34" y="28" width="32" height="20" rx="4" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.4"/>
            <text x="50" y="41" text-anchor="middle" font-family="Roboto Mono" font-size="8" font-weight="700" fill="#1A73E8">Conv</text>
            <line x1="66" y1="38" x2="78" y2="38" stroke="#5F6368" stroke-width="1.4"/>
            <rect x="78" y="28" width="32" height="20" rx="4" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.4"/>
            <text x="94" y="41" text-anchor="middle" font-family="Roboto Mono" font-size="8" font-weight="700" fill="#1A73E8">Conv</text>
            <circle cx="126" cy="38" r="9" fill="#FEF7E0" stroke="#B06000" stroke-width="1.6"/>
            <text x="126" y="41.5" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#B06000">+x</text>
          </svg>
          <div class="evo-sol"><div><strong>Obat #2:</strong> Jalan pintas <code>F(x)+x</code> + <code>GAP</code> buang jutaan bobot Flatten.</div></div>
          <div class="evo-prob"><div><strong>Cacat Baru:</strong> Conv <code>3×3</code> standar tetap berat untuk HP (<code>90 MB</code>).</div></div>
          <div class="evo-stat">ResNet50: {r_res['total_params']/1e6:.2f}M · 90 MB</div>
        </div>

        <div class="evo-card" style="border-color:#34A853; background:#F8FDF9;">
          <div class="card-top-bar bar-green"></div>
          <div>
            <span class="evo-gen" style="background:#E6F4EA; color:#137333;">GEN #4 · MOBILE ★</span>
            <div class="evo-name" style="margin-top:4px;">4. MobileNetV2</div>
            <div style="font-size:10.2px; color:#137333; font-weight:700;">Pilihan Utama Frozen!</div>
          </div>
          <svg viewBox="0 0 150 64" style="width:100%; height:64px; background:#FFFFFF; border-radius:8px; border:1px solid #CEEAD6;">
            <path d="M 24 44 Q 75 62 126 44" fill="none" stroke="#34A853" stroke-width="2" stroke-dasharray="3,2"/>
            <rect x="14" y="22" width="22" height="22" rx="4" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.4"/>
            <text x="25" y="36" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" font-weight="700" fill="#1A73E8">32</text>
            <rect x="46" y="10" width="26" height="42" rx="4" fill="#E6F4EA" stroke="#34A853" stroke-width="1.6"/>
            <text x="59" y="34" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" font-weight="700" fill="#137333">192</text>
            <rect x="78" y="10" width="28" height="42" rx="4" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.6"/>
            <text x="92" y="34" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" font-weight="700" fill="#B06000">DW3</text>
            <rect x="114" y="22" width="22" height="22" rx="4" fill="#E8F0FE" stroke="#1A73E8" stroke-width="1.4"/>
            <text x="125" y="36" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" font-weight="700" fill="#1A73E8">Lin</text>
          </svg>
          <div class="evo-sol"><div><strong>Obat #3:</strong> <em>Depthwise Separable</em> + <em>Inverted Residual</em> super ramping!</div></div>
          <div class="evo-prob"><div><strong>Tantangan:</strong> Bagaimana menaikkan kapasitas secara sistematis?</div></div>
          <div class="evo-stat" style="background:#34A853; color:#FFF;">{r_mob['total_params']/1e6:.2f}M param · {r_mob['est_size_mb']} MB</div>
        </div>

        <div class="evo-card">
          <div class="card-top-bar" style="background:#8E24AA;"></div>
          <div>
            <span class="evo-gen" style="background:#F3E8FD; color:#681DA8;">GEN #5 · SCALING</span>
            <div class="evo-name" style="margin-top:4px;">5. EfficientNet</div>
            <div style="font-size:10.2px; color:#5F6368;">MBConv + SE Attention</div>
          </div>
          <svg viewBox="0 0 150 64" style="width:100%; height:64px; background:#FAFBFD; border-radius:8px; border:1px solid #EEF0F3;">
            <rect x="14" y="16" width="38" height="32" rx="5" fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"/>
            <text x="33" y="35" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" font-weight="700" fill="#137333">MBConv</text>
            <path d="M54 32 L68 32" stroke="#681DA8" stroke-width="1.6"/>
            <rect x="70" y="14" width="34" height="36" rx="5" fill="#F3E8FD" stroke="#8E24AA" stroke-width="1.5"/>
            <text x="87" y="35" text-anchor="middle" font-family="Roboto Mono" font-size="8" font-weight="700" fill="#681DA8">SE★</text>
            <path d="M106 32 L116 32" stroke="#681DA8" stroke-width="1.6"/>
            <rect x="118" y="18" width="20" height="28" rx="4" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.4"/>
            <text x="128" y="35" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#C5221F">&phi;</text>
          </svg>
          <div class="evo-sol"><div><strong>Obat #4:</strong> <em>Compound Scaling</em> seimbang + <em>SE Attention</em> fokus objek.</div></div>
          <div class="evo-prob"><div><strong>Trade-off:</strong> Operasi banyak (<code>237</code> layer) &#8594; CPU lebih lambat.</div></div>
          <div class="evo-stat">EffNetB0: {r_eff['total_params']/1e6:.2f}M · 15.5 MB</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # ==================================================================
    # BAB 1 — ARSITEKTUR #1: MLP (S05–S09, 7.0 menit)
    # ==================================================================
    slides.append(
        make_divider_slide(
            bg_class="bg-blue",
            kicker="BAB 1 · ARSITEKTUR #1 (EVOLUSI AWAL)",
            title="MLP: Multi-Layer Perceptron",
            description="Melompat dari 1-Layer P02 dengan menambahkan Hidden Layer bertingkat — mengenal kekuatan non-linearitas dan keterbatasannya pada foto.",
            footer_label=FOOTER,
            data_title="Bab 1 — MLP (Multi-Layer Perceptron)",
            notes="Alokasi waktu: 1 menit. Masuk Bab 1 membahas Arsitektur #1: MLP.",
        )
    )

    # S06: #1.1 MLP In General
    slides.append(f"""
    <section class="slide" data-title="#1.1 MLP — Gambaran Umum" data-notes="Alokasi waktu: 1.5 menit. Penjelasan MLP in general: seluruh piksel diluruskan lalu melewati satu atau lebih Hidden Layer sebelum Softmax 5 kelas.">
      <div class="kicker">ARSITEKTUR #1 · PENJELASAN IN GENERAL</div>
      <h2>MLP: <span class="hl-blue">Menambah Lapisan Tersembunyi (Hidden Layer)</span></h2>
      {_arch_badge_row("1. MLP (FULLY-CONNECTED)", "red", [
          ("dark", "Foto 224×224×3", "Kotak Piksel RGB"),
          ("yellow", "Flatten", "150.528 Angka 1D"),
          ("blue", "Hidden 1 (64) + ReLU", "Gabung Ciri Dasar"),
          ("blue", "Hidden 2 (32) + ReLU", "Gabung Pola Lanjut"),
          ("green", "Output Dense(5)", "Softmax Frozen"),
      ])}
      <div class="grid-2" style="flex:1; min-height:0; margin-top:10px; align-items:stretch;">
        <div class="card" style="display:flex; flex-direction:column; justify-content:space-between; gap:8px; padding:14px 16px;">
          <div class="card-title" style="color:#1A73E8;">Apa Bedanya dengan Model 1-Layer di P02?</div>
          <ul class="clean" style="font-size:12.6px; line-height:1.48;">
            <li><strong>P02 (1-Layer):</strong> Input piksel langsung dikalikan bobot ke 5 kelas — seperti menilai foto hanya dengan 1 lapis rata-rata warna/posisi.</li>
            <li><strong>P03 (MLP):</strong> Menyisipkan <strong>Hidden Layer</strong> di tengah sehingga jaringan bisa membentuk kombinasi ciri berjenjang (misal: <em>biru gaun + putih salju</em> &#8594; ciri Elsa).</li>
            <li>Disebut <em>Fully-Connected</em> (<code>Dense</code>) karena <strong>setiap neuron terhubung ke semua neuron</strong> lapisan sebelumnya.</li>
          </ul>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
            <div class="mini-box" style="background:#FEF7E0; border-color:#FDE293; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.8px; font-weight:700; color:#B06000;">MODEL P02 (0 HIDDEN)</div>
              <div style="font-size:11.4px; color:#202124; margin-top:2px;"><code>150.528 &#8594; 5</code> = <strong>{p02_p:,}</strong></div>
            </div>
            <div class="mini-box" style="background:#FCE8E6; border-color:#F6AEA9; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.8px; font-weight:700; color:#C5221F;">MODEL P03 (2 HIDDEN)</div>
              <div style="font-size:11.4px; color:#202124; margin-top:2px;"><code>.. &#8594; 64 &#8594; 32 &#8594; 5</code> = <strong>{r_mlp['total_params']:,}</strong></div>
            </div>
          </div>
          <div class="callout blue" style="font-size:11.8px; padding:8px 11px;">
            <strong>Analogi Sederhana:</strong> P02 = 1 manajer langsung memeriksa 150.528 piksel sendirian; MLP = 64 asisten merangkum dulu, baru 32 koordinator menyaring ke 5 kelas.
          </div>
        </div>
        <div class="card" style="display:flex; flex-direction:column; justify-content:space-between; align-items:center; gap:6px; padding:14px 16px;">
          <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
            <span style="font-family:var(--font-title); font-size:12.8px; font-weight:700; color:#202124;">Anatomi Koneksi Rapat (Dense Mesh)</span>
            <span class="pill blue" style="font-size:9.5px; padding:2px 8px;">Semua ke Semua</span>
          </div>
          <svg viewBox="0 0 400 220" style="width:100%; flex:1; max-height:230px;">
            <g stroke="#CFD8DC" stroke-width="1.3">
              <line x1="58" y1="32" x2="162" y2="48"/><line x1="58" y1="32" x2="162" y2="96"/><line x1="58" y1="32" x2="162" y2="144"/>
              <line x1="58" y1="74" x2="162" y2="48"/><line x1="58" y1="74" x2="162" y2="96"/><line x1="58" y1="74" x2="162" y2="144"/>
              <line x1="58" y1="116" x2="162" y2="48"/><line x1="58" y1="116" x2="162" y2="96"/><line x1="58" y1="116" x2="162" y2="144"/>
              <line x1="58" y1="158" x2="162" y2="48"/><line x1="58" y1="158" x2="162" y2="96"/><line x1="58" y1="158" x2="162" y2="144"/>
              <line x1="162" y1="48" x2="258" y2="70"/><line x1="162" y1="48" x2="258" y2="126"/>
              <line x1="162" y1="96" x2="258" y2="70"/><line x1="162" y1="96" x2="258" y2="126"/>
              <line x1="162" y1="144" x2="258" y2="70"/><line x1="162" y1="144" x2="258" y2="126"/>
              <line x1="258" y1="70" x2="346" y2="48"/><line x1="258" y1="70" x2="346" y2="96"/><line x1="258" y1="70" x2="346" y2="144"/>
              <line x1="258" y1="126" x2="346" y2="48"/><line x1="258" y1="126" x2="346" y2="96"/><line x1="258" y1="126" x2="346" y2="144"/>
            </g>
            <g fill="#FEF7E0" stroke="#FBBC04" stroke-width="2.2">
              <circle cx="58" cy="32" r="14"/><circle cx="58" cy="74" r="14"/><circle cx="58" cy="116" r="14"/><circle cx="58" cy="158" r="14"/>
            </g>
            <g fill="#E8F0FE" stroke="#4285F4" stroke-width="2.2">
              <circle cx="162" cy="48" r="16"/><circle cx="162" cy="96" r="16"/><circle cx="162" cy="144" r="16"/>
              <circle cx="258" cy="70" r="16"/><circle cx="258" cy="126" r="16"/>
            </g>
            <g fill="#E6F4EA" stroke="#34A853" stroke-width="2.2">
              <circle cx="346" cy="48" r="15"/><circle cx="346" cy="96" r="15"/><circle cx="346" cy="144" r="15"/>
            </g>
            <text x="58" y="36" text-anchor="middle" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#B06000">x₁</text>
            <text x="58" y="162" text-anchor="middle" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#B06000">xₙ</text>
            <text x="162" y="100" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#1A73E8">64</text>
            <text x="258" y="102" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#1A73E8">32</text>
            <text x="346" y="100" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#137333">5</text>
            <text x="58" y="192" text-anchor="middle" font-family="Poppins" font-size="9.8" font-weight="700" fill="#B06000">150.528 Piksel</text>
            <text x="210" y="192" text-anchor="middle" font-family="Poppins" font-size="9.8" font-weight="700" fill="#1A73E8">Hidden Layers (ReLU)</text>
            <text x="346" y="192" text-anchor="middle" font-family="Poppins" font-size="9.8" font-weight="700" fill="#137333">Softmax</text>
          </svg>
          <div class="formula-box" style="width:100%; font-size:10.4px; padding:7px 10px;">
            (150.528×64+64) + (64×32+32) + (32×5+5) = <strong>{r_mlp['total_params']:,} Param</strong>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S07: #1.2 Fitur Khusus MLP
    slides.append(f"""
    <section class="slide" data-title="#1.2 MLP — Fitur Khusus & Kelemahan Foto" data-notes="Alokasi waktu: 1.5 menit. Bedah fitur khusus MLP (Hidden Representation, ReLU berlapis) serta 3 cacatnya pada foto: Ledakan Parameter, Buta Posisi Spasial, dan rentan shortcut latar.">
      <div class="kicker">ARSITEKTUR #1 · FITUR KHUSUS &amp; BATASNYA</div>
      <h2>Fitur Khusus MLP: <span class="hl-blue">Kuat di Pola Non-Linear</span>, <span class="hl-red">Lemah di Gambar</span></h2>
      <div class="grid-2" style="flex:1; min-height:0; align-items:stretch;">
        <div class="card" style="border-top:5px solid #34A853; display:flex; flex-direction:column; justify-content:space-between; gap:9px; padding:13px 15px;">
          <span class="pill green" style="width:fit-content;">FITUR KHUSUS UTAMA</span>
          <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; flex:1; display:flex; flex-direction:column; justify-content:center;">
            <strong style="color:#137333; font-size:12.5px;">1. Representasi Hidden Bertingkat</strong>
            <div style="font-size:11.6px; margin-top:3px; color:#202124;">Kombinasi 2+ <em>Hidden Layer</em> + aktivasi <code>ReLU</code> mampu memisahkan pola berliku (<em>non-linear boundary</em>): <code>h&#8322; = ReLU(W&#8322;·ReLU(W&#8321;x + b&#8321;) + b&#8322;)</code>.</div>
          </div>
          <div class="mini-box" style="background:#E8F0FE; border-color:#C6DAFC; flex:1; display:flex; flex-direction:column; justify-content:center;">
            <strong style="color:#1A73E8; font-size:12.5px;">2. Koneksi Semua-ke-Semua (<em>All-to-All Dense</em>)</strong>
            <div style="font-size:11.6px; margin-top:3px; color:#202124;">Setiap fitur masukan bebas berinteraksi dengan fitur mana pun tanpa asumsi urutan ruang — sangat ideal untuk kolom tabel angka CSV.</div>
          </div>
          <div class="mini-box" style="flex:1; display:flex; flex-direction:column; justify-content:center;">
            <strong style="color:#202124; font-size:12.5px;">3. Menjadi &ldquo;Kepala&rdquo; di Ekor Arsitektur Modern</strong>
            <div style="font-size:11.6px; margin-top:3px; color:#5F6368;">Lapisan akhir <code>Dense + Softmax</code> di CNN, ResNet, maupun MobileNetV2 pada hakikatnya adalah blok MLP mini!</div>
          </div>
        </div>

        <div class="card" style="border-top:5px solid #EA4335; display:flex; flex-direction:column; justify-content:space-between; gap:9px; padding:13px 15px;">
          <span class="pill red" style="width:fit-content;">CACAT FATAL SAAT MEMBACA FOTO</span>
          <div class="mini-box" style="background:#FCE8E6; border-color:#F6AEA9; flex:1; display:flex; flex-direction:column; justify-content:center;">
            <strong style="color:#C5221F; font-size:12.5px;">1. Ledakan Parameter: {r_mlp['total_params']:,} Param!</strong>
            <div style="font-size:11.6px; margin-top:3px; color:#202124;">Hanya dengan <code>64</code> hidden neuron pada <code>224×224×3</code>: layer ke-1 sendiri memakan <code>150.528 × 64 + 64 = 9.633.856</code> bobot!</div>
          </div>
          <div class="mini-box" style="background:#FEF7E0; border-color:#FDE293; flex:1; display:flex; flex-direction:column; justify-content:center;">
            <strong style="color:#B06000; font-size:12.5px;">2. Spatial Blindness (Lupa Tetangga 2D)</strong>
            <div style="font-size:11.6px; margin-top:3px; color:#202124;">Jika karakter Elsa bergeser 2–8 piksel ke kanan atau kiri, seluruh piksel berpindah indeks — bobot terlatih kehilangan jejak!</div>
          </div>
          <div class="callout red" style="font-size:11.6px; padding:10px 12px;">
            <strong>Akibat Nyata di Proyek Frozen:</strong> Pada foto <code>48×48</code>, MLP butuh <code>444.677</code> param tapi akurasi belajarnya macet di <code>{tr['mlp']['acc'][-1]}%</code> (validasi <code>{sh['mlp_val_acc']}%</code>) &#8594; butuh <strong>CNN</strong>!
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S08: #1.3 Simulasi Full MLP (Interactive)
    slides.append(f"""
    <section class="slide" id="sim-mlp-slide" data-title="#1.3 Simulasi Full Arsitektur MLP" data-notes="Alokasi waktu: 2 menit. Simulator #1: uji pengaruh Hidden Neuron MLP dan efek menggeser posisi foto Elsa 2 piksel terhadap ledakan parameter & skor prediksi.">
      <div class="kicker">ARSITEKTUR #1 · SIMULASI FULL MLP</div>
      <h2>Simulasi MLP: <span class="hl-blue">Hidden Layer</span> &amp; <span class="hl-red">Tes Geser 2 Piksel</span></h2>
      <div class="sim-bar pdf-keep-ui" id="sim-mlp-bar">
        <button type="button" class="btn-ui" data-mlp="4_norm" onclick="setMlpSim('4_norm')">1. Normal (Hidden 4)</button>
        <button type="button" class="btn-ui outline" data-mlp="64_norm" onclick="setMlpSim('64_norm')">2. Hidden 64 (224×224)</button>
        <button type="button" class="btn-ui outline" data-mlp="64_shift" onclick="setMlpSim('64_shift')">3. Geser Elsa 2 Piksel!</button>
        <div class="kpi-row">
          <span class="kpi-chip" id="mlp-kpi-param">Param: 9.636.101</span>
          <span class="kpi-chip" id="mlp-kpi-pred">Elsa: 82%</span>
        </div>
      </div>

      <div class="grid-2" style="flex:1; min-height:0; margin-top:8px; align-items:stretch;">
        <div class="canvas-box" style="justify-content:space-between; gap:8px;">
          <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
            <strong style="font-family:var(--font-title); font-size:12px;" id="mlp-vis-ttl">Aliran Input Posisi Normal → Hidden → Output</strong>
            <span class="pill blue" id="mlp-vis-badge" style="font-size:10px;">Posisi Tepat</span>
          </div>
          <svg id="mlp-sim-svg" viewBox="0 0 430 225" style="width:100%; flex:1; max-height:225px;"></svg>
          <div class="formula-box" id="mlp-sim-callout" style="width:100%; font-size:11px; text-align:left;">
            <strong>Ringkas:</strong> Pada posisi normal, bobot terlatih tepat mengenai piksel gaun biru Elsa (<code>x4..x7</code>).
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:9px; justify-content:space-between;">
          <div class="card sync-card" id="mlp-stage-1" style="flex:1; padding:12px 14px; justify-content:center;">
            <div class="card-top-bar bar-yellow"></div>
            <div style="font-family:var(--font-title); font-size:13px; font-weight:700; color:#B06000;">Tahap 1 · Input Flatten (Koordinat Kaku)</div>
            <div style="font-size:11.8px; color:#3C4043; margin-top:3px;" id="mlp-st1-desc">Foto <code>224×224×3</code> diratakan menjadi <code>150.528</code> input tetap berdasarkan nomor koordinat.</div>
          </div>
          <div class="card sync-card" id="mlp-stage-2" style="flex:1; padding:12px 14px; justify-content:center;">
            <div class="card-top-bar bar-blue"></div>
            <div style="font-family:var(--font-title); font-size:13px; font-weight:700; color:#1A73E8;">Tahap 2 · Hidden Dense + ReLU</div>
            <div style="font-size:11.8px; color:#3C4043; margin-top:3px;" id="mlp-st2-desc">Setiap neuron terhubung ke semua <code>150.528</code> piksel — jumlah bobot melambung cepat.</div>
          </div>
          <div class="card sync-card" id="mlp-stage-3" style="flex:1; padding:12px 14px; justify-content:center;">
            <div class="card-top-bar bar-green"></div>
            <div style="font-family:var(--font-title); font-size:13px; font-weight:700; color:#137333;">Tahap 3 · Output Softmax (5 Kelas Frozen)</div>
            <div style="font-size:11.8px; color:#3C4043; margin-top:3px;" id="mlp-st3-desc">Skor keyakinan Elsa vs Anna/Olaf — langsung anjlok saat piksel objek bergeser ke kanan!</div>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S09: #1.4 Use Case MLP
    slides.append(f"""
    <section class="slide" data-title="#1.4 Use Case & Verdict MLP" data-notes="Alokasi waktu: 1 menit. Use case MLP di dunia nyata (tabular/CSV & classification head) dan alasan mengapa MLP tidak dipilih sebagai tulang punggung pemroses foto Frozen.">
      <div class="kicker">ARSITEKTUR #1 · USE CASE &amp; RELEVANSI PROYEK</div>
      <h2>Kapan <span class="hl-blue">MLP Dipakai</span> &amp; Kenapa Bukan untuk Foto Frozen?</h2>
      <div class="uc-grid" style="margin-top:4px; flex:1; min-height:0; align-items:stretch;">
        <div class="uc-card" style="border-top:5px solid #34A853; justify-content:space-between; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:5px;">
            <span class="pill green" style="width:fit-content;">✓ SANGAT COCOK</span>
            <div class="card-title" style="font-size:14px;">1. Data Tabel (Tabular / CSV)</div>
            <p class="card-text" style="font-size:11.8px;">Prediksi harga rumah, skor kredit, atau deteksi penipuan dari kolom fitur numerik bebas urutan.</p>
          </div>
          <div style="background:#F8F9FA; border:1px solid #E0E3E7; border-radius:9px; padding:8px; font-family:var(--font-code); font-size:9.8px; color:#3C4043;">
            <div style="font-weight:700; border-bottom:1px solid #DADCE0; padding-bottom:3px; margin-bottom:4px; color:#137333;">Luas | Kamar | Jarak &#8594; Harga</div>
            <div>72m² &nbsp;|&nbsp; 3 &nbsp;&nbsp;|&nbsp; 2km &#8594; 850jt</div>
            <div>90m² &nbsp;|&nbsp; 4 &nbsp;&nbsp;|&nbsp; 5km &#8594; 920jt</div>
          </div>
          <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; font-size:10.8px; padding:6px 9px;"><strong>Aturan:</strong> Kolom tabel = jagonya MLP!</div>
        </div>

        <div class="uc-card" style="border-top:5px solid #4285F4; justify-content:space-between; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:5px;">
            <span class="pill blue" style="width:fit-content;">✓ COCOK DI UJUNG</span>
            <div class="card-title" style="font-size:14px;">2. Classification Head CNN</div>
            <p class="card-text" style="font-size:11.8px;">Menjadi lapisan penutup (<code>Dense(64) &#8594; Dense(5)</code>) <strong>setelah</strong> gambar diringkas konvolusi menjadi vektor ciri kecil.</p>
          </div>
          <div style="background:#E8F0FE; border:1px solid #C6DAFC; border-radius:9px; padding:10px 8px; text-align:center; font-family:var(--font-code); font-size:10px; color:#174EA6; font-weight:700;">
            Foto &#8594; CNN / MobileNet &#8594; GAP &#8594; <span style="background:#1A73E8; color:#FFF; padding:2px 6px; border-radius:5px;">MLP Head (5)</span>
          </div>
          <div class="mini-box" style="background:#E8F0FE; border-color:#C6DAFC; font-size:10.8px; padding:6px 9px;"><strong>Aturan:</strong> Pakai sesudah ekstraksi ciri!</div>
        </div>

        <div class="uc-card" style="border-top:5px solid #EA4335; justify-content:space-between; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:5px;">
            <span class="pill red" style="width:fit-content;">✕ HINDARI SEBAGAI BACKBONE</span>
            <div class="card-title" style="font-size:14px;">3. Foto Kamera ({tot_imgs} Foto)</div>
            <p class="card-text" style="font-size:11.8px;">Posisi figurin berubah-ubah &amp; latar <code>ramai</code> ({n_ramai} foto) membuat bobot MLP raksasa mudah terkecoh.</p>
          </div>
          <div style="display:flex; align-items:center; gap:9px; background:#FCE8E6; border:1px solid #F6AEA9; border-radius:9px; padding:7px 9px;">
            <img src="assets/P03/thumb_elsa_ramai.jpg" alt="Elsa Ramai" style="width:42px; height:42px; border-radius:7px; object-fit:cover;"/>
            <div style="font-family:var(--font-code); font-size:9.8px; color:#C5221F; line-height:1.35;"><strong>{r_mlp['total_params']:,}</strong> param<br/>Rentan geser &amp; latar!</div>
          </div>
          <div class="mini-box" style="background:#FCE8E6; border-color:#F6AEA9; font-size:10.8px; padding:6px 9px;"><strong>Aturan:</strong> Ganti input Flatten ke Conv2D!</div>
        </div>
      </div>
      <div class="verdict-box avoid" style="margin-top:10px;">
        <div>
          <div style="font-family:var(--font-title); font-size:12.5px; font-weight:700; color:#C5221F;">VERDICT PROYEK FROZEN · MLP (GENERASI #1)</div>
          <div style="font-size:12px; color:#202124; margin-top:2px;">Hanya dijadikan <strong>pembanding awal (negatif kontrol)</strong> di Langkah 1 notebook &amp; sebagai <em>Head</em> akhir. Untuk membaca piksel 2D, kita berevolusi ke <strong>CNN Klasik!</strong></div>
        </div>
        <span class="pill red" style="font-size:11px; flex-shrink:0;">{r_mlp['total_params']/1e6:.2f}M Param · Gagal Spasial</span>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # ==================================================================
    # BAB 2 — ARSITEKTUR #2: CNN KLASIK (S10–S15, 10.5 menit)
    # ==================================================================
    slides.append(
        make_divider_slide(
            bg_class="bg-red",
            kicker="BAB 2 · ARSITEKTUR #2 (EVOLUSI SPASIAL)",
            title="CNN Klasik: Melihat dalam 2D",
            description="Menggantikan Flatten raksasa dengan Kernel 3×3 geser, Parameter Sharing, Stride, Padding, dan Pooling (generasi LeNet hingga VGG).",
            footer_label=FOOTER,
            data_title="Bab 2 — CNN Klasik (Conv2D + Pooling)",
            notes="Alokasi waktu: 1 menit. Masuk Bab 2 membedah Arsitektur #2: CNN Klasik.",
        )
    )

    # S11: #2.1 CNN Klasik In General
    slides.append(f"""
    <section class="slide" data-title="#2.1 CNN Klasik — Gambaran Umum" data-notes="Alokasi waktu: 1.5 menit. Jelaskan pipeline utuh CNN Klasik pada foto Elsa nyata: Conv2D -> ReLU -> MaxPool berulang menghasilkan Feature Map bertingkat.">
      <div class="kicker">ARSITEKTUR #2 · PENJELASAN IN GENERAL</div>
      <h2>CNN Klasik: <span class="hl-red">Ekstraksi Pola Bertingkat dari Foto 2D</span></h2>
      {_arch_badge_row("2. CNN KLASIK (STACKED CONV+POOL)", "blue", [
          ("dark", "Foto 224×224×3", "Tetap Bentuk 2D!"),
          ("red", "Conv2D 3×3 + ReLU", "Cari Tepi & Warna"),
          ("yellow", "MaxPooling 2×2", "Ringkas Ukuran ÷2"),
          ("blue", "Conv2D Dalam", "Bentuk & Bagian"),
          ("green", "GAP + Dense(5)", "Softmax 5 Kelas"),
      ])}
      <div class="card" style="margin-top:9px; padding:11px 14px; flex:1; min-height:0; display:flex; flex-direction:column; justify-content:space-between; gap:8px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong style="font-family:var(--font-title); font-size:12.8px;">Hasil Nyata Operasi Conv2D &amp; MaxPool pada Foto Elsa (<code>data/frozen_v1/</code>)</strong>
          <span class="pill blue" style="font-size:10px;">Total 3-Blok CNN: {r_cnn['total_params']:,} Param (~95× lebih hemat dari MLP!)</span>
        </div>
        <div style="flex:1; min-height:0; display:flex; align-items:center; justify-content:center;">
          <img src="assets/P03/02_cnn_conv_pool_elsa.png" alt="Conv2D dan MaxPool Elsa nyata" style="width:100%; height:100%; max-height:215px; object-fit:contain; border-radius:10px;"/>
        </div>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:7px; text-align:center;">
          <div class="mini-box" style="background:#F8F9FA; padding:5px 7px; font-size:10.6px;"><strong style="color:#1A73E8;">Layer Awal</strong><br/>Tepi &amp; warna dasar</div>
          <div class="mini-box" style="background:#F8F9FA; padding:5px 7px; font-size:10.6px;"><strong style="color:#C5221F;">Layer Tengah</strong><br/>Tekstur rambut &amp; gaun</div>
          <div class="mini-box" style="background:#F8F9FA; padding:5px 7px; font-size:10.6px;"><strong style="color:#B06000;">Layer Dalam</strong><br/>Bagian kepala &amp; tubuh</div>
          <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; padding:5px 7px; font-size:10.6px;"><strong style="color:#137333;">Head (GAP+Dense)</strong><br/>Skor 5 Karakter Frozen</div>
        </div>
        <div class="callout green" style="font-size:11.6px; padding:7px 11px;">
          <strong>Kunci Revolusioner:</strong> CNN tidak memasang kabel terpisah per koordinat piksel, melainkan menggeser <strong>filter kecil yang sama (<code>Kernel 3×3</code>)</strong> ke seluruh foto &#8594; melahirkan <em>Feature Map</em>!
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S12: #2.2 Fitur Khusus CNN Klasik
    slides.append(f"""
    <section class="slide" data-title="#2.2 CNN Klasik — Fitur Khusus" data-notes="Alokasi waktu: 2 menit. Bedah 4 fitur khusus CNN: Kernel & Parameter Sharing, Stride, Padding, dan Pooling + rumus sederhana ukuran Feature Map.">
      <div class="kicker">ARSITEKTUR #2 · FITUR KHUSUS (FONDASI CONVOLUTION)</div>
      <h2>4 Senjata Khusus CNN: <span class="hl-red">Kernel, Stride, Padding &amp; Pooling</span></h2>
      <div class="grid-2" style="flex:1; min-height:0; align-items:stretch;">
        <div class="card-tint blue" style="padding:11px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:6px;">
          <div>
            <div class="card-title" style="color:#1A73E8; font-size:13.8px;">1. Kernel 3×3 &amp; Parameter Sharing</div>
            <p class="card-text" style="font-size:11.6px; margin-top:3px;"><strong>Kernel/Filter</strong> adalah kotak bobot kecil (<code>3×3</code>) pencari pola tepi/warna. Satu filter <code>3×3×3</code> cuma punya <strong>27 bobot + 1 bias = 28 param</strong>, dipakai ulang menggeser seluruh foto!</p>
          </div>
          <svg viewBox="0 0 360 56" style="width:100%; height:56px; background:#FFFFFF; border-radius:8px; border:1px solid #C6DAFC;">
            <rect x="18" y="8" width="40" height="40" rx="4" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.5"/>
            <rect x="24" y="14" width="14" height="14" rx="2" fill="rgba(234,67,53,0.28)" stroke="#EA4335" stroke-width="1.5"/>
            <text x="68" y="32" font-family="Poppins" font-size="11" font-weight="700" fill="#5F6368">&#8594; geser sama ke semua posisi &#8594;</text>
            <rect x="292" y="11" width="34" height="34" rx="4" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.5"/>
            <text x="309" y="32" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#C5221F">3×3</text>
          </svg>
          <div class="formula-box" style="font-size:10.8px; padding:5px 10px;">1 Filter = <strong>28 param</strong> (bukan 150.528×64 di MLP!)</div>
        </div>

        <div class="card-tint red" style="padding:11px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:6px;">
          <div>
            <div class="card-title" style="color:#C5221F; font-size:13.8px;">2. Stride &amp; Padding (Atur Dimensi Peta)</div>
            <p class="card-text" style="font-size:11.6px; margin-top:3px;"><strong>Stride (S)</strong> = langkah geser (<code>S=1</code> rapat; <code>S=2</code> loncat 2 &#8594; ukuran ÷2). <strong>Padding (P)</strong> = bingkai nol <code>0</code> di tepi gambar agar ukuran tepi tetap terjaga.</p>
          </div>
          <svg viewBox="0 0 360 56" style="width:100%; height:56px; background:#FFFFFF; border-radius:8px; border:1px solid #F6AEA9;">
            <rect x="18" y="8" width="40" height="40" rx="4" fill="#F1F3F4" stroke="#9AA0A6" stroke-dasharray="3,2"/>
            <rect x="24" y="14" width="28" height="28" rx="3" fill="#E8F0FE" stroke="#4285F4"/>
            <text x="72" y="25" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#C5221F">Padding P=1 (tepi 0)</text>
            <text x="72" y="40" font-family="Roboto Mono" font-size="9" fill="#5F6368">Stride S=1: rapat | S=2: ÷2</text>
            <rect x="255" y="13" width="88" height="30" rx="6" fill="#FCE8E6"/>
            <text x="299" y="32" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#C5221F">16 &#8594; 14 / 8</text>
          </svg>
          <div class="formula-box" style="font-size:10.8px; padding:5px 10px;">Output = (W &minus; K + 2P) / S + 1 &nbsp;|&nbsp; (16&minus;3+0)/1+1 = <strong>14</strong></div>
        </div>

        <div class="card-tint yellow" style="padding:11px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:6px;">
          <div>
            <div class="card-title" style="color:#B06000; font-size:13.8px;">3. MaxPooling 2×2 (Ringkas &amp; Tahan Geser)</div>
            <p class="card-text" style="font-size:11.6px; margin-top:3px;">Di tiap kotak <code>2×2</code> pada <em>Feature Map</em>, ambil nilai <strong>terbesar (maksimum)</strong> saja &#8594; ukuran mengecil separuh &amp; geseran 1px tidak mengubah nilai puncak!</p>
          </div>
          <svg viewBox="0 0 360 56" style="width:100%; height:56px; background:#FFFFFF; border-radius:8px; border:1px solid #FDE293;">
            <rect x="24" y="10" width="36" height="36" rx="4" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.5"/>
            <text x="33" y="24" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#5F6368">1</text>
            <text x="51" y="24" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#C5221F">8</text>
            <text x="33" y="40" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#5F6368">2</text>
            <text x="51" y="40" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#5F6368">0</text>
            <text x="80" y="32" font-family="Poppins" font-size="10.5" font-weight="700" fill="#B06000">&#8594; ambil max &#8594;</text>
            <rect x="196" y="14" width="28" height="28" rx="5" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
            <text x="210" y="32" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#137333">8</text>
            <text x="240" y="32" font-family="Roboto" font-size="9.5" fill="#5F6368">Ukuran ÷ 2!</text>
          </svg>
          <div class="formula-box" style="font-size:10.8px; padding:5px 10px;"><code>14×14</code> &#8594; MaxPool <code>2×2</code> &#8594; <strong><code>7×7</code> (tahan geser 1px!)</strong></div>
        </div>

        <div class="card-tint green" style="padding:11px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:6px;">
          <div>
            <div class="card-title" style="color:#137333; font-size:13.8px;">4. Receptive Field (Pandangan Makin Luas)</div>
            <p class="card-text" style="font-size:11.6px; margin-top:3px;">Semakin dalam melewati <code>Conv2D + MaxPool</code>, 1 piksel di <em>Feature Map</em> lapisan atas merangkum area luas di foto asli — dari tepi kecil ke wajah/gaun Elsa utuh!</p>
          </div>
          <svg viewBox="0 0 360 56" style="width:100%; height:56px; background:#FFFFFF; border-radius:8px; border:1px solid #A8DAB5;">
            <rect x="20" y="18" width="20" height="20" rx="3" fill="#E8F0FE" stroke="#4285F4"/>
            <text x="48" y="31" font-family="Roboto Mono" font-size="8.5" fill="#1A73E8">Tepi 3×3</text>
            <text x="108" y="32" font-family="Poppins" font-size="11" fill="#5F6368">&#8594;</text>
            <rect x="128" y="12" width="32" height="32" rx="4" fill="#FEF7E0" stroke="#FBBC04"/>
            <text x="168" y="31" font-family="Roboto Mono" font-size="8.5" fill="#B06000">Gaun 7×7</text>
            <text x="228" y="32" font-family="Poppins" font-size="11" fill="#5F6368">&#8594;</text>
            <rect x="248" y="6" width="44" height="44" rx="5" fill="#E6F4EA" stroke="#34A853" stroke-width="1.6"/>
            <text x="300" y="31" font-family="Roboto Mono" font-size="8.5" font-weight="700" fill="#137333">Elsa Utuh</text>
          </svg>
          <div class="formula-box" style="font-size:10.8px; padding:5px 10px;">Makin dalam = cakupan area foto <strong>makin luas!</strong></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S13: #2.3 Simulasi Full CNN Klasik (Real Elsa 16x16 Canvas!)
    slides.append(f"""
    <section class="slide" id="sim-cnn-slide" data-title="#2.3 Simulasi Full Arsitektur CNN Klasik" data-notes="Alokasi waktu: 2.5 menit. Simulator #2: hitung konvolusi 2D nyata pada matriks 16x16 Elsa! Peserta mengubah Filter (Sobel X/Y/Tajam), Stride (1/2), & Padding (Valid/Same) untuk melihat Feature Map dan MaxPool 2x2 secara langsung.">
      <div class="kicker">ARSITEKTUR #2 · SIMULASI FULL CNN KLASIK (PIKSEL ELSA NYATA)</div>
      <h2>Simulasi CNN: <span class="hl-red">Geser Kernel 3×3</span> &#8594; <span class="hl-blue">Feature Map</span> &#8594; <span class="hl-green">MaxPool</span></h2>
      <div class="sim-bar pdf-keep-ui" id="sim-cnn-bar">
        <button type="button" class="btn-ui" data-cnn-f="sobel_v" onclick="setCnnState({{filter:'sobel_v'}})">Filter: Tepi Vertikal</button>
        <button type="button" class="btn-ui outline" data-cnn-f="sobel_h" onclick="setCnnState({{filter:'sobel_h'}})">Filter: Tepi Horizontal</button>
        <button type="button" class="btn-ui outline" data-cnn-f="sharp" onclick="setCnnState({{filter:'sharp'}})">Filter: Pertajam</button>
        <button type="button" class="btn-ui outline" id="cnn-btn-stride" onclick="toggleCnnStride()">Stride: 1</button>
        <button type="button" class="btn-ui outline" id="cnn-btn-pad" onclick="toggleCnnPad()">Padding: Valid (0)</button>
        <div class="kpi-row">
          <span class="kpi-chip" id="cnn-kpi-shape">Feature Map: 14×14 &#8594; Pool: 7×7</span>
        </div>
      </div>

      <div class="cnn-canvas-strip" style="margin-top:8px; flex:1; min-height:0;">
        <div class="cnn-can-card" style="justify-content:space-between; padding:10px 12px;">
          <strong style="font-family:var(--font-title); font-size:12.2px;">1. Input Asli Elsa (16×16)</strong>
          <canvas id="cnn-can-in" width="212" height="212"></canvas>
          <div style="width:100%; text-align:center;">
            <div style="font-family:var(--font-code); font-size:10.5px; color:#202124; font-weight:700;" id="cnn-lbl-in">Grid asli 16×16 (256 piksel)</div>
            <div style="font-size:10.2px; color:#5F6368; margin-top:2px;">Matriks skala 0.0–1.0 diekstrak dari <code>thumb_elsa.jpg</code></div>
          </div>
        </div>
        <div class="cnn-can-card" style="border-color:#4285F4; background:#F8FAFF; justify-content:space-between; padding:10px 12px;">
          <strong style="font-family:var(--font-title); font-size:12.2px; color:#1A73E8;">2. Feature Map (Conv2D + ReLU)</strong>
          <canvas id="cnn-can-fm" width="212" height="212"></canvas>
          <div style="width:100%; text-align:center;">
            <div style="font-family:var(--font-code); font-size:10.5px; color:#1A73E8; font-weight:700;" id="cnn-lbl-fm">14×14 (196 sel aktif)</div>
            <div style="font-size:10.2px; color:#5F6368; margin-top:2px;" id="cnn-kernel-txt">Kernel Sobel Vertikal <code>3×3</code> + ReLU (&gt;0 menyala biru)</div>
          </div>
        </div>
        <div class="cnn-can-card" style="border-color:#34A853; background:#F6FBF7; justify-content:space-between; padding:10px 12px;">
          <strong style="font-family:var(--font-title); font-size:12.2px; color:#137333;">3. MaxPool 2×2 &#8594; Head Softmax</strong>
          <canvas id="cnn-can-pool" width="212" height="212"></canvas>
          <div style="width:100%; text-align:center;">
            <div style="font-family:var(--font-code); font-size:10.5px; color:#137333; font-weight:700;" id="cnn-lbl-pool">7×7 &#8594; 49 ciri ke Softmax</div>
            <div style="font-size:10.2px; color:#5F6368; margin-top:2px;">Ambil nilai maksimum per kotak <code>2×2</code> (ringkas &amp; stabil)</div>
          </div>
        </div>
      </div>
      <div class="formula-box" id="cnn-sim-formula" style="margin-top:8px; font-size:11.5px;">
        <strong>Rumus Ukuran:</strong> (16 &minus; 3 + 2×0) / 1 + 1 = <strong>14×14</strong> &nbsp;|&nbsp; Hanya <strong>9 bobot kernel + 1 bias = 10 param</strong> (dibanding ratusan ribu kabel di MLP!)
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S14: #2.4 Use Case & Batas CNN Klasik
    slides.append(f"""
    <section class="slide" data-title="#2.4 Use Case & Batas CNN Klasik" data-notes="Alokasi waktu: 1.5 menit. Use case CNN Klasik (OCR, klasifikasi sederhana, inspeksi pabrik) dan 2 masalah saat CNN ditumpuk makin dalam (era VGG): Vanishing Gradient dan kepala Flatten raksasa.">
      <div class="kicker">ARSITEKTUR #2 · USE CASE &amp; MASALAH GENERASI BARU</div>
      <h2>Use Case CNN Klasik &amp; <span class="hl-red">Kenapa Masih Perlu Berevolusi?</span></h2>
      <div class="uc-grid" style="margin-top:4px; flex:1; min-height:0; align-items:stretch;">
        <div class="uc-card" style="border-top:5px solid #34A853; justify-content:space-between; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:5px;">
            <span class="pill green" style="width:fit-content;">✓ SANGAT COCOK</span>
            <div class="card-title" style="font-size:14px;">1. OCR &amp; Angka/Huruf (LeNet)</div>
            <p class="card-text" style="font-size:11.8px;">Membaca tulisan tangan kode pos, plat nomor kendaraan, dan gambar ikon berlatar bersih di perangkat ringan.</p>
          </div>
          <div style="background:#F8F9FA; border:1px solid #E0E3E7; border-radius:9px; padding:8px; display:flex; align-items:center; justify-content:center; gap:10px;">
            <div style="width:38px; height:38px; background:#202124; color:#FFF; font-family:var(--font-code); font-size:20px; font-weight:700; display:flex; align-items:center; justify-content:center; border-radius:7px;">7</div>
            <div style="font-family:var(--font-code); font-size:9.8px; color:#137333; line-height:1.35;"><strong>28×28 Polos</strong><br/>Akurasi &gt;99% cepat!</div>
          </div>
          <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; font-size:10.8px; padding:6px 9px;"><strong>Aturan:</strong> Objek tunggal &amp; latar bersih!</div>
        </div>

        <div class="uc-card" style="border-top:5px solid #4285F4; justify-content:space-between; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:5px;">
            <span class="pill blue" style="width:fit-content;">✓ SANGAT COCOK</span>
            <div class="card-title" style="font-size:14px;">2. Inspeksi Kualitas Pabrik</div>
            <p class="card-text" style="font-size:11.8px;">Mendeteksi goresan, retak, atau botol penyok di jalur konveyor dengan kamera &amp; lampu terkendali.</p>
          </div>
          <div style="background:#E8F0FE; border:1px solid #C6DAFC; border-radius:9px; padding:9px 8px; text-align:center; font-family:var(--font-code); font-size:10px; color:#174EA6; font-weight:700;">
            Kamera Tetap &#8594; Conv 3 Blok &#8594; <span style="background:#1A73E8; color:#FFF; padding:2px 6px; border-radius:5px;">LOLOS / CACAT</span>
          </div>
          <div class="mini-box" style="background:#E8F0FE; border-color:#C6DAFC; font-size:10.8px; padding:6px 9px;"><strong>Aturan:</strong> Sudut &amp; latar seragam!</div>
        </div>

        <div class="uc-card" style="border-top:5px solid #FBBC04; justify-content:space-between; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:5px;">
            <span class="pill yellow" style="width:fit-content;">⚠ MENTOK SAAT DALAM &amp; DATA MINI</span>
            <div class="card-title" style="font-size:14px;">3. Foto Ramai &amp; Dataset 143 Foto</div>
            <p class="card-text" style="font-size:11.8px;">Menumpuk &gt;16 layer CNN polos memicu <em>Vanishing Gradient</em>, sedangkan melatih 3 blok dari nol di ~100 foto train Frozen hanya mentok <code>val_acc 34.3%</code> (uji 48×48)!</p>
          </div>
          <div style="display:flex; align-items:center; gap:9px; background:#FEF7E0; border:1px solid #FDE293; border-radius:9px; padding:7px 9px;">
            <img src="assets/P03/thumb_elsa_ramai.jpg" alt="Elsa Ramai" style="width:42px; height:42px; border-radius:7px; object-fit:cover;"/>
            <div style="font-family:var(--font-code); font-size:9.8px; color:#B06000; line-height:1.35;"><strong>From Scratch = Baseline #1</strong><br/>Butuh Pretrained CNN!</div>
          </div>
          <div class="mini-box" style="background:#FEF7E0; border-color:#FDE293; font-size:10.8px; padding:6px 9px;"><strong>Peran Frozen:</strong> Jadi pembanding awal vs MobileNetV2!</div>
        </div>
      </div>
      <div class="verdict-box foundation" style="margin-top:10px;">
        <div>
          <div style="font-family:var(--font-title); font-size:12.5px; font-weight:700; color:#174EA6;">BASELINE #1 PROYEK FROZEN &amp; PEMICU RESNET (#3)</div>
          <div style="font-size:12px; color:#202124; margin-top:2px;">(1) CNN polos 3 blok hanya jadi <strong>Baseline awal (from scratch)</strong>. (2) Menumpuk CNN dalam terhalang <strong>Vanishing Gradient</strong> &amp; kepala <code>Flatten</code> boros — memicu lahirnya <strong>ResNet (#3) &#8594; MobileNetV2 (#4)</strong>!</div>
        </div>
        <span class="pill blue" style="font-size:11px; flex-shrink:0;">3-Blok CNN: {r_cnn['total_params']:,} Param</span>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S15: Q&A #1
    slides.append(
        make_qa_slide(
            qa_id="qa-p03-1",
            qa_num=1,
            kicker="CEK PEMAHAMAN · Q&A #1 (MLP VS CNN KLASIK)",
            title_html='Menghitung Dimensi <span class="hl-blue">Feature Map</span> &amp; Efisiensi CNN',
            question_html="Sebuah foto berukuran <code>28×28</code> diproses oleh layer <code>Conv2D</code> dengan <code>Kernel 3×3</code>, <code>Stride = 1</code>, dan <code>Padding = valid (0)</code>. Berapa ukuran <strong>Feature Map</strong> yang dihasilkan?",
            choices=[
                "A. 28×28 piksel (ukurannya tidak berubah)",
                "B. 26×26 piksel ((28 − 3 + 0) / 1 + 1)",
                "C. 14×14 piksel (langsung menyusut separuh)",
            ],
            answer_html="<strong>Jawaban: B (26×26 piksel).</strong><br/>Dengan rumus <code>(W − K + 2P) / S + 1 = (28 − 3 + 0) / 1 + 1 = 26</code>. Karena <em>Padding valid</em> tidak menambah bingkai nol di tepi, jendela <code>3×3</code> berkurang 2 langkah dari lebar awal. Opsi C baru terjadi jika setelahnya diberi <code>MaxPooling 2×2</code>.",
            vis_q_html='''<svg viewBox="0 0 260 190" style="width:100%; max-height:195px;">
              <rect x="20" y="20" width="110" height="110" rx="8" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
              <rect x="30" y="30" width="28" height="28" rx="4" fill="rgba(234,67,53,0.22)" stroke="#EA4335" stroke-width="2"/>
              <text x="75" y="92" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#1A73E8">28 × 28</text>
              <text x="44" y="48" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" font-weight="700" fill="#C5221F">3×3</text>
              <path d="M138 75 L164 75" stroke="#5F6368" stroke-width="2.5"/>
              <polygon points="162,69 172,75 162,81" fill="#5F6368"/>
              <rect x="176" y="34" width="68" height="82" rx="8" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2" stroke-dasharray="4,3"/>
              <text x="210" y="80" text-anchor="middle" font-family="Poppins" font-size="16" font-weight="800" fill="#B06000">? × ?</text>
              <text x="130" y="156" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" fill="#5F6368">Stride = 1 &nbsp;|&nbsp; Padding = 0 (Valid)</text>
              <text x="130" y="174" text-anchor="middle" font-family="Poppins" font-size="10" fill="#1A73E8">(W &minus; K + 2P) / S + 1 = ?</text>
            </svg>''',
            vis_a_html='''<svg viewBox="0 0 260 190" style="width:100%; max-height:195px;">
              <rect x="18" y="20" width="96" height="96" rx="8" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.8"/>
              <text x="66" y="72" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#1A73E8">28 × 28</text>
              <path d="M120 68 L142 68" stroke="#137333" stroke-width="2.4"/>
              <polygon points="140,62 150,68 140,74" fill="#137333"/>
              <rect x="154" y="26" width="88" height="84" rx="8" fill="#E6F4EA" stroke="#34A853" stroke-width="2.4"/>
              <text x="198" y="65" text-anchor="middle" font-family="Poppins" font-size="15" font-weight="800" fill="#137333">26 × 26</text>
              <text x="198" y="85" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#137333">Feature Map ✓</text>
              <rect x="18" y="132" width="224" height="44" rx="8" fill="#E6F4EA" stroke="#A8DAB5"/>
              <text x="130" y="151" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#137333">(28 &minus; 3 + 0) / 1 + 1 = 26</text>
              <text x="130" y="167" text-anchor="middle" font-family="Roboto" font-size="9.5" fill="#3C4043">Baru menjadi 13×13 jika diberi MaxPool 2×2</text>
            </svg>''',
            footer_label=FOOTER,
            notes="Alokasi waktu: 2 menit. Diskusi Q&A #1: minta peserta menghitung ukuran output konvolusi 28x28 dengan kernel 3x3 valid.",
            bar_color="blue",
            correct_choice="B",
            data_title="Q&A #1 — Hitung Dimensi Feature Map",
        )
    )

    # ==================================================================
    # BAB 3 — ARSITEKTUR #3: RESNET (S16–S21, 9.5 menit)
    # ==================================================================
    slides.append(
        make_divider_slide(
            bg_class="bg-yellow",
            kicker="BAB 3 · ARSITEKTUR #3 (TEROBOSAN JARINGAN DALAM)",
            title="ResNet: Residual Network",
            description="Menyelamatkan sinyal gradien dengan jalan pintas Skip Connection (F(x) + x), BatchNorm, dan Global Average Pooling.",
            footer_label=FOOTER,
            data_title="Bab 3 — ResNet (Residual Network)",
            notes="Alokasi waktu: 1 menit. Masuk Bab 3 membahas Arsitektur #3: ResNet.",
        )
    )

    # S17: #3.1 ResNet In General
    slides.append(f"""
    <section class="slide" data-title="#3.1 ResNet — Gambaran Umum" data-notes="Alokasi waktu: 1.5 menit. Penjelasan ResNet in general: masalah degradasi jaringan polos dalam vs jalan pintas Skip Connection dan grafik nyata Frozen.">
      <div class="kicker">ARSITEKTUR #3 · PENJELASAN IN GENERAL</div>
      <h2>ResNet: <span class="hl-yellow">Jalan Pintas Agar Jaringan Dalam Tetap Tajam</span></h2>
      {_arch_badge_row("3. RESNET (RESIDUAL BLOCKS + GAP)", "yellow", [
          ("dark", "Foto 224×224×3", "Masuk Blok Awal"),
          ("blue", "Conv + BN + ReLU", "Olahan Utama F(x)"),
          ("yellow", "Tambah +x (Skip)", "Jalur Pintas Utuh"),
          ("green", "Global Avg Pool", "7×7×2048 &#8594; 2048"),
          ("green", "Dense(5)", "Softmax Frozen"),
      ])}
      <div class="grid-2" style="flex:1; min-height:0; margin-top:10px; align-items:stretch;">
        <div class="card" style="display:flex; flex-direction:column; justify-content:flex-start; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
            <strong style="font-family:var(--font-title); font-size:12.5px;">Bukti Nyata Frozen (12 Conv Layer · Param Kembar: {tr['mini_resnet']['params']:,})</strong>
            <span class="pill yellow" style="font-size:10px;">UJI EKSPERIMEN</span>
          </div>
          <div style="background:#FFFFFF; border:1px solid #E8EAED; border-radius:10px; padding:6px;">
            <img src="assets/P03/03_resnet_skip_gap.png" alt="Plain Deep Net vs Mini-ResNet Frozen" style="width:100%; height:auto; max-height:210px; object-fit:contain; display:block; border-radius:6px;"/>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:auto;">
            <div class="mini-box" style="background:#F8F9FA; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.5px; font-weight:700; color:#5F6368;">GRAFIK KIRI · LOSS 12 EPOCH</div>
              <div style="font-size:11.3px; color:#202124; margin-top:2px;">Plain <code>{tr['plain_deep']['loss'][-1]}</code> &#8594; Mini-ResNet <strong style="color:#137333;">{tr['mini_resnet']['loss'][-1]}</strong></div>
            </div>
            <div class="mini-box" style="background:#E6F4EA; border-color:#CEEAD6; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.5px; font-weight:700; color:#137333;">GRAFIK KANAN · HEMAT KEPALA</div>
              <div style="font-size:11.3px; color:#202124; margin-top:2px;">Flatten <code>51.38M</code> &#8594; GAP <strong style="color:#137333;">10.245</strong></div>
            </div>
          </div>
        </div>
        <div class="card" style="display:flex; flex-direction:column; justify-content:flex-start; gap:10px;">
          <div class="card-title" style="color:#B06000;">Kenapa Jaringan Terlalu Dalam Malah Memburuk?</div>
          <ul class="clean" style="font-size:12.3px; line-height:1.48;">
            <li>Secara teori, 50 layer seharusnya &ge; 20 layer. Kenyataannya di CNN polos, semakin dalam tumpukan, error malah naik (<em><strong>Degradation Problem</strong></em>) karena sinyal error (<em>gradien</em>) melemah saat mundur.</li>
            <li>Pada uji nyata Frozen dengan jumlah bobot kembar (<code>{tr['mini_resnet']['params']:,}</code>): <strong>Mini-ResNet</strong> menekan loss hingga <code>{tr['mini_resnet']['loss'][-1]}</code> (vs <code>{tr['plain_deep']['loss'][-1]}</code>) dan meraih akurasi validasi <strong>2&times; lebih tinggi</strong> (<code>{tr['mini_resnet']['val_acc'][-1]}%</code> vs <code>{tr['plain_deep']['val_acc'][-1]}%</code>)!</li>
            <li><strong>Peran di Evolusi:</strong> Membuka pintu model sangat dalam (<code>ResNet50/101</code>) sekaligus menghapus borosnya <code>Flatten</code> lewat <em>Global Average Pooling</em> (GAP).</li>
          </ul>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:auto;">
            <div class="evo-prob">
              <div style="font-weight:700; color:#C5221F; margin-bottom:2px;">CNN Polos Dalam</div>
              <div>Sinyal gradien habis di tengah &amp; ekor Flatten 51.38M param.</div>
            </div>
            <div class="evo-sol">
              <div style="font-weight:700; color:#137333; margin-bottom:2px;">ResNet (+x &amp; GAP)</div>
              <div>Jalur tol <code>+ x</code> selamatkan gradien &amp; GAP hemat 99.9% ekor.</div>
            </div>
          </div>
          <div class="callout yellow" style="font-size:11.6px;">
            <strong>Analogi Jalan Tol:</strong> Jalur pintas (<em>Skip Connection</em>) adalah jalur tol bebas hambatan di samping jalan tikungan &mdash; informasi asli <code>x</code> selalu selamat sampai tujuan!
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S18: #3.2 Fitur Khusus ResNet
    slides.append(f"""
    <section class="slide" data-title="#3.2 ResNet — Fitur Khusus" data-notes="Alokasi waktu: 1.5 menit. 3 terobosan inti ResNet: Skip Connection F(x)+x, Batch Normalization penstabil angka, dan Global Average Pooling (GAP) pengganti Flatten.">
      <div class="kicker">ARSITEKTUR #3 · FITUR KHUSUS</div>
      <h2>3 Inovasi ResNet: <span class="hl-yellow">Skip Connection</span>, <span class="hl-blue">BatchNorm</span> &amp; <span class="hl-green">GAP</span></h2>
      <div class="uc-grid" style="margin-top:6px; flex:1; min-height:0;">
        <div class="card" style="border-top:5px solid #FBBC04; display:flex; flex-direction:column; gap:8px;">
          <span class="pill yellow" style="width:fit-content;">INOVASI #1 · INTI</span>
          <div class="card-title" style="font-size:14.2px;">Skip Connection (<code>y = F(x) + x</code>)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Alih-alih memaksa layer menghafal ulang seluruh gambar dari nol, layer konvolusi cukup belajar <strong>residu/perubahan kecil <code>F(x)</code></strong> yang ditambahkan ke input asli <code>x</code>.</p>
          <div style="background:#FFFDF6; border:1px solid #FDE293; border-radius:10px; padding:10px 8px; margin-top:4px;">
            <svg viewBox="0 0 260 92" width="100%" height="106" aria-label="Diagram Skip Connection">
              <defs>
                <marker id="arr-y" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#E37400"/></marker>
                <marker id="arr-d" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#5F6368"/></marker>
              </defs>
              <rect x="6" y="42" width="34" height="24" rx="6" fill="#202124"/>
              <text x="23" y="58" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#FFF">x</text>
              <path d="M40,54 L66,54" stroke="#5F6368" stroke-width="2" marker-end="url(#arr-d)"/>
              <rect x="70" y="38" width="108" height="32" rx="7" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.5"/>
              <text x="124" y="52" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#1A73E8">Conv + BN + ReLU</text>
              <text x="124" y="64" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="#5F6368">Belajar koreksi F(x)</text>
              <path d="M178,54 L200,54" stroke="#5F6368" stroke-width="2" marker-end="url(#arr-d)"/>
              <path d="M23,42 C23,12 214,12 214,39" fill="none" stroke="#FBBC04" stroke-width="3" marker-end="url(#arr-y)"/>
              <rect x="82" y="4" width="92" height="16" rx="8" fill="#FEF7E0" stroke="#F9AB00"/>
              <text x="128" y="15" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#B06000">Jalur Tol +x Utuh</text>
              <circle cx="214" cy="54" r="11" fill="#FEF7E0" stroke="#E37400" stroke-width="2"/>
              <text x="214" y="58" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#B06000">+</text>
              <path d="M225,54 L250,54" stroke="#34A853" stroke-width="2" marker-end="url(#arr-d)"/>
              <text x="241" y="46" text-anchor="middle" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#137333">y</text>
            </svg>
          </div>
          <div style="font-size:11.3px; color:#3C4043;"><strong>Efek Praktis:</strong> Gradien error dari layer akhir dapat meloncat mundur langsung lewat garis <code>+ x</code> tanpa mengecil jadi nol.</div>
          <div class="formula-box" style="margin-top:auto; font-size:11.5px;">Output Blok = F(x) + x<br/><span style="font-size:10px; color:#5F6368;">Saat Backprop, gradien mengalir langsung lewat +x!</span></div>
        </div>

        <div class="card" style="border-top:5px solid #4285F4; display:flex; flex-direction:column; gap:8px;">
          <span class="pill blue" style="width:fit-content;">INOVASI #2 · STABILISATOR</span>
          <div class="card-title" style="font-size:14.2px;">Batch Normalization (BN)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Menjaga skala angka aktivasi di setiap layer tidak terlalu besar atau mengecil ekstrem selama training. Efeknya: training jauh lebih cepat stabil dan tidak mudah macet.</p>
          <div style="background:#F8FAFF; border:1px solid #D2E3FC; border-radius:10px; padding:10px 8px; margin-top:4px;">
            <svg viewBox="0 0 260 92" width="100%" height="106" aria-label="Diagram Batch Normalization">
              <rect x="6" y="10" width="96" height="72" rx="7" fill="#FCE8E6" stroke="#F6AEA9"/>
              <text x="54" y="24" text-anchor="middle" font-family="Poppins" font-size="8.8" font-weight="700" fill="#C5221F">Sebelum BN (Liar)</text>
              <rect x="18" y="34" width="12" height="38" rx="2" fill="#EA4335"/>
              <rect x="38" y="64" width="12" height="8" rx="2" fill="#EA4335"/>
              <rect x="58" y="28" width="12" height="44" rx="2" fill="#EA4335"/>
              <rect x="78" y="60" width="12" height="12" rx="2" fill="#EA4335"/>
              <text x="54" y="80" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#C5221F">-420 .. +850</text>
              <text x="128" y="50" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#1A73E8">BN →</text>
              <rect x="152" y="10" width="102" height="72" rx="7" fill="#E8F0FE" stroke="#AECBFA"/>
              <text x="203" y="24" text-anchor="middle" font-family="Poppins" font-size="8.8" font-weight="700" fill="#1A73E8">Sesudah BN (Rapi)</text>
              <rect x="166" y="45" width="12" height="27" rx="2" fill="#4285F4"/>
              <rect x="185" y="42" width="12" height="30" rx="2" fill="#4285F4"/>
              <rect x="204" y="43" width="12" height="29" rx="2" fill="#4285F4"/>
              <rect x="223" y="46" width="12" height="26" rx="2" fill="#4285F4"/>
              <text x="203" y="80" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#1A73E8">mean≈0 · std≈1</text>
            </svg>
          </div>
          <div style="font-size:11.3px; color:#3C4043;"><strong>Aturan Penting Transfer Learning:</strong> Saat evaluasi atau <em>fine-tuning</em>, BN memakai statistik beku agar angka prediksi tidak goyang.</div>
          <div class="formula-box" style="margin-top:auto; font-size:11.5px;">Rata-rata &approx; 0, Sebaran &approx; 1<br/><span style="font-size:10px; color:#5F6368;">Penting di P07: base dipanggil training=False!</span></div>
        </div>

        <div class="card" style="border-top:5px solid #34A853; display:flex; flex-direction:column; gap:8px;">
          <span class="pill green" style="width:fit-content;">INOVASI #3 · PENGHEMAT HEAD</span>
          <div class="card-title" style="font-size:14.2px;">Global Average Pooling (GAP)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Mengganti <code>Flatten &#8594; Dense</code> yang boros: merata-ratakan tiap <em>Feature Map</em> <code>7×7</code> menjadi <strong>1 angka perwakilan per kanal</strong>.</p>
          <div style="background:#F4FBF6; border:1px solid #CEEAD6; border-radius:10px; padding:10px 8px; margin-top:4px;">
            <svg viewBox="0 0 272 92" width="100%" height="106" aria-label="Diagram Global Average Pooling">
              <rect x="6" y="14" width="54" height="54" rx="6" fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"/>
              <line x1="24" y1="14" x2="24" y2="68" stroke="#A8DAB5"/><line x1="42" y1="14" x2="42" y2="68" stroke="#A8DAB5"/>
              <line x1="6" y1="32" x2="60" y2="32" stroke="#A8DAB5"/><line x1="6" y1="50" x2="60" y2="50" stroke="#A8DAB5"/>
              <text x="33" y="81" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#137333">7×7×2048</text>
              <path d="M64,28 L104,20" stroke="#EA4335" stroke-width="1.6" stroke-dasharray="3,2"/>
              <rect x="108" y="8" width="158" height="28" rx="6" fill="#FCE8E6" stroke="#EA4335"/>
              <text x="187" y="20" text-anchor="middle" font-family="Poppins" font-size="8.3" font-weight="700" fill="#C5221F">Flatten (Cara Lama VGG)</text>
              <text x="187" y="31" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" fill="#C5221F">100.352 → 51.38M param!</text>
              <path d="M64,52 L104,60" stroke="#34A853" stroke-width="2"/>
              <rect x="108" y="46" width="158" height="32" rx="6" fill="#E6F4EA" stroke="#34A853" stroke-width="1.6"/>
              <text x="187" y="59" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#137333">GAP (Cara ResNet)</text>
              <text x="187" y="71" text-anchor="middle" font-family="Roboto Mono" font-size="8" font-weight="700" fill="#137333">2.048 angka → 10.245</text>
            </svg>
          </div>
          <div style="font-size:11.3px; color:#3C4043;"><strong>Kenapa Efektif:</strong> Tanpa lapisan <code>Dense(512)</code> raksasa, model jauh lebih ringan dan tidak mudah <em>overfitting</em> di dataset kecil.</div>
          <div class="formula-box" style="margin-top:auto; font-size:11.5px;">51.380.229 &#8594; <strong>10.245 param</strong><br/><span style="font-size:10px; color:#137333;">Pangkas &gt;99.9% bobot kepala!</span></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S19: #3.3 Simulasi Full ResNet
    slides.append(f"""
    <section class="slide" id="sim-resnet-slide" data-title="#3.3 Simulasi Full Arsitektur ResNet" data-notes="Alokasi waktu: 2 menit. Simulator #3: bandingkan kekuatan sinyal gradien Plain Deep Net vs ResNet (+Skip Connection) dari Layer 20 mundur ke Layer 1.">
      <div class="kicker">ARSITEKTUR #3 · SIMULASI FULL RESNET</div>
      <h2>Simulasi ResNet: <span class="hl-red">Plain Deep Net</span> vs <span class="hl-green">Skip Connection (+x)</span></h2>
      <div class="sim-bar pdf-keep-ui" id="sim-resnet-bar">
        <button type="button" class="btn-ui" data-res="plain" onclick="setResnetSim('plain')">1. Plain Deep Net (Tanpa Skip)</button>
        <button type="button" class="btn-ui outline" data-res="resnet" onclick="setResnetSim('resnet')">2. ResNet (+ Skip Connection &amp; GAP)</button>
        <div class="kpi-row">
          <span class="kpi-chip" id="res-kpi-grad">Sinyal di Layer 1: 7% (Macet)</span>
          <span class="kpi-chip" id="res-kpi-head">Head: Flatten 51.38M</span>
        </div>
      </div>

      <div class="grid-2" style="flex:1; min-height:0; margin-top:8px; align-items:stretch;">
        <div class="card" style="display:flex; flex-direction:column; justify-content:space-between; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-family:var(--font-title); font-size:12.5px;" id="res-bar-ttl">Kekuatan Sinyal Gradien Saat Backprop (L20 &#8594; L1)</strong>
            <span class="pill red" id="res-status-pill" style="font-size:10px;">Vanishing Gradient!</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:8px;" id="res-signal-bars"></div>
          <div style="background:#F8F9FA; border:1px solid #E8EAED; border-radius:10px; padding:7px 9px;">
            <div style="font-size:10px; font-weight:700; color:#5F6368; margin-bottom:4px;" id="res-arch-cap">Alur Sinyal &amp; Ekor Arsitektur Saat Ini:</div>
            <svg id="res-arch-svg" viewBox="0 0 430 92" width="100%" height="92" aria-label="Diagram Alur Arsitektur ResNet vs Plain Deep Net"></svg>
          </div>
          <div class="callout yellow" id="res-callout" style="font-size:11.5px;">
            Tanpa jalur pintas, sinyal belajar yang dikirim dari Loss di Layer 20 habis terserap di tengah jalan sebelum mencapai Layer 1!
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:10px;">
          <div class="card sync-card sync-on sync-red" id="res-stage-block" style="padding:13px 15px;">
            <div style="display:flex; justify-content:flex-start; align-items:center; gap:8px;">
              <strong style="font-family:var(--font-title); font-size:13px;">1. Blok Dalam (Layer 1 &#8594; Layer 20)</strong>
              <span class="pill red" id="res-blk-pill" style="font-size:10px;">TANPA +x</span>
            </div>
            <div style="font-size:12px; color:#3C4043; margin-top:5px; line-height:1.45;" id="res-block-desc">Setiap blok saat ini hanya menyalurkan jalur utama konvolusi <code>F(x)</code> tanpa penyambung <code>+ x</code>. Saat backprop, sinyal gradien menyusut hingga tinggal <strong>7%</strong> di Layer 1.</div>
          </div>
          <div class="card sync-card sync-on sync-red" id="res-stage-gap" style="padding:13px 15px;">
            <div style="display:flex; justify-content:flex-start; align-items:center; gap:8px;">
              <strong style="font-family:var(--font-title); font-size:13px;">2. Ekor Arsitektur (Flatten vs GAP)</strong>
              <span class="pill red" id="res-gap-pill" style="font-size:10px;">FLATTEN 51.38M</span>
            </div>
            <div style="font-size:12px; color:#3C4043; margin-top:5px; line-height:1.45;" id="res-gap-desc">Dengan cara lama (<code>Flatten &#8594; Dense(512)</code>), tensor <code>7×7×2048</code> diratakan menjadi <code>100.352</code> angka dan menghabiskan <code>51.380.229</code> parameter kepala!</div>
          </div>
          <div class="card card-tint blue" style="margin-top:auto; padding:12px 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <strong style="font-family:var(--font-title); font-size:12px; color:#1A73E8;">HASIL KERAS NYATA (ResNet50 · 224×224×3)</strong>
              <span class="pill blue" style="font-size:9.5px;">BENCHMARK ASLI</span>
            </div>
            <div style="font-family:var(--font-code); font-size:11px; color:#202124; line-height:1.5;">
              Total Bobot: <strong>{r_res['total_params']:,}</strong> ({r_res['est_size_mb']} MB) · <strong>{r_res['skip_add_layers']} blok Skip Add()</strong><br/>
              Kedalaman: <strong>{r_res['layers_backbone']} layer backbone</strong> · Latensi CPU: <strong>~{r_res['latency_ms_8imgs']:.0f} ms</strong> / 8 foto
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S20: #3.4 Use Case ResNet
    slides.append(f"""
    <section class="slide" data-title="#3.4 Use Case & Verdict ResNet" data-notes="Alokasi waktu: 1.5 menit. Use case ResNet50 di dunia nyata dan posisinya di proyek Frozen: akurat tapi terlalu berat untuk HP/Colab ringan.">
      <div class="kicker">ARSITEKTUR #3 · USE CASE &amp; RELEVANSI PROYEK</div>
      <h2>Use Case <span class="hl-yellow">ResNet</span> &amp; Kenapa Belum Jadi Pilihan Utama Kita</h2>
      <div class="uc-grid" style="margin-top:4px; flex:1; min-height:0;">
        <div class="uc-card" style="border-top:4px solid #34A853;">
          <span class="pill green" style="width:fit-content;">&#10003; SANGAT COCOK</span>
          <div class="card-title" style="font-size:14px;">1. Citra Medis &amp; Riset Server GPU</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Deteksi pneumonia pada X-Ray paru atau klasifikasi sel mikroskopis di server rumah sakit yang memiliki GPU khusus &amp; butuh akurasi tinggi tanpa batasan ukuran file 90 MB.</p>
          <ul class="clean" style="font-size:11.5px; line-height:1.45; margin-top:4px;">
            <li><strong>Contoh Kasus:</strong> Radiologi, patologi digital, satelit.</li>
            <li><strong>Skala Data:</strong> Ratusan ribu hingga jutaan citra berlabel.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.45;">
            <strong style="color:#137333;">Kenapa Andal di Server:</strong>
            <div>• 175 layer menangkap tekstur mikro halus.</div>
            <div>• Stabil dilatih dengan GPU berkapasitas besar.</div>
          </div>
          <div style="font-family:var(--font-code); font-size:10.5px; color:#137333; background:#E6F4EA; border-radius:7px; padding:5px 8px;">Syarat ideal: GPU Cloud / Server ≥ 8 GB VRAM</div>
        </div>

        <div class="uc-card" style="border-top:4px solid #4285F4;">
          <span class="pill blue" style="width:fit-content;">&#10003; BACKBONE STANDAR</span>
          <div class="card-title" style="font-size:14px;">2. Pembanding Akurasi (Benchmark)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Menjadi tolok ukur klasik di banyak jurnal ilmiah Computer Vision termasuk sebagai pembanding langsung <code>ResNet50 vs MobileNetV2</code> di silabus proyek kita.</p>
          <ul class="clean" style="font-size:11.5px; line-height:1.45; margin-top:4px;">
            <li><strong>Fokus Uji:</strong> Seberapa besar selisih akurasi vs model ringan.</li>
            <li><strong>Catatan Training:</strong> Selalu panggil base BN dengan <code>training=False</code>.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.45;">
            <strong style="color:#1A73E8;">Posisi di Proyek Frozen:</strong>
            <div>• Baseline pembanding akurasi di P06/P07.</div>
            <div>• Menguji apakah model berat benar-benar perlu.</div>
          </div>
          <div style="font-family:var(--font-code); font-size:10.5px; color:#1A73E8; background:#E8F0FE; border-radius:7px; padding:5px 8px;">Peran: Pembanding akurasi &amp; ukuran vs MobileNetV2</div>
        </div>

        <div class="uc-card" style="border-top:4px solid #EA4335;">
          <span class="pill red" style="width:fit-content;">&#9888; BERAT DI HP &amp; DATA KECIL</span>
          <div class="card-title" style="font-size:14px;">3. Aplikasi Mobile / Dataset Mini</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;"><code>ResNet50</code> memiliki <strong>{r_res['total_params']/1e6:.2f} juta parameter</strong> (~{r_res['est_size_mb']} MB, latensi ~{r_res['latency_ms_8imgs']:.0f} ms / 8 foto CPU) karena konvolusi <code>3×3</code> standar tetap mahal dihitung!</p>
          <ul class="clean" style="font-size:11.5px; line-height:1.45; margin-top:4px;">
            <li><strong>Kecepatan:</strong> Lebih lambat di CPU / perangkat seluler.</li>
            <li><strong>Kapasitas:</strong> Mudah menghafal (<em>overfitting</em>) jika dataset mini.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.45;">
            <strong style="color:#C5221F;">Kendala di Edge / HP:</strong>
            <div>• File bobot {r_res['est_size_mb']} MB lambat diunduh di app.</div>
            <div>• Terlalu besar untuk dataset {tot_imgs} foto Frozen.</div>
          </div>
          <div style="font-family:var(--font-code); font-size:10.5px; color:#C5221F; background:#FCE8E6; border-radius:7px; padding:5px 8px;">Solusi: Ganti konvolusi standar → Depthwise!</div>
        </div>
      </div>
      <div class="verdict-box bench" style="margin-top:10px;">
        <div>
          <div style="font-family:var(--font-title); font-size:12.5px; font-weight:700; color:#B06000;">VERDICT PROYEK FROZEN · RESNET50 (GENERASI #3)</div>
          <div style="font-size:12px; color:#202124; margin-top:2px;">Digunakan sebagai <strong>pembanding benchmark</strong>, bukan model produksi akhir. Untuk mendapatkan kecerdasan ResNet dalam bodi 10&times; lebih ringan, lahirlah <strong>MobileNetV2!</strong></div>
        </div>
        <span class="pill yellow" style="font-size:11px; flex-shrink:0;">{r_res['total_params']/1e6:.2f}M Param · {r_res['est_size_mb']} MB</span>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S21: Q&A #2
    slides.append(
        make_qa_slide(
            qa_id="qa-p03-2",
            qa_num=2,
            kicker="CEK PEMAHAMAN · Q&A #2 (RESNET)",
            title_html='Rahasia <span class="hl-yellow">Skip Connection</span> &amp; <span class="hl-green">GAP</span>',
            question_html="Apa dua terobosan pada <strong>ResNet</strong> yang membuatnya bisa memiliki 50+ layer sekaligus menghindari ledakan jutaan parameter di bagian akhir sebelum Softmax?",
            choices=[
                "A. Membuang fungsi ReLU dan memperbesar ukuran gambar ke 1024×1024",
                "B. Menambahkan jalur pintas Skip Connection (F(x) + x) dan memakai Global Average Pooling (GAP)",
                "C. Menghapus semua layer Conv2D dan kembali memakai Flatten → Dense",
            ],
            answer_html="<strong>Jawaban: B.</strong><br/><strong>Skip Connection (<code>F(x) + x</code>)</strong> menjaga sinyal gradien tetap mengalir lancar saat jaringan sangat dalam (mencegah <em>Vanishing Gradient</em>), sedangkan <strong>GAP</strong> merata-ratakan setiap <em>Feature Map</em> menjadi 1 angka per kanal — memangkas parameter kepala dari <code>51,38 juta</code> menjadi <code>10.245</code>!",
            vis_q_html="""<svg viewBox="0 0 320 296" style="width:100%; max-width:360px; height:auto;" aria-label="Ilustrasi Tantangan ResNet">
              <rect x="6" y="6" width="308" height="132" rx="12" fill="#FEF7E0" stroke="#F9AB00" stroke-width="1.5"/>
              <text x="160" y="29" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#B06000">Tantangan 1: 50+ Layer Dalam</text>
              <rect x="18" y="46" width="76" height="30" rx="7" fill="#34A853"/><text x="56" y="65" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#FFF">L50: 100%</text>
              <text x="108" y="66" text-anchor="middle" font-family="Poppins" font-size="14" fill="#B06000">&#8594;</text>
              <rect x="122" y="46" width="74" height="30" rx="7" fill="#FFFFFF" stroke="#DADCE0"/><text x="159" y="65" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#5F6368">L25: ???%</text>
              <text x="210" y="66" text-anchor="middle" font-family="Poppins" font-size="14" fill="#EA4335">&#8594;</text>
              <rect x="224" y="46" width="78" height="30" rx="7" fill="#FCE8E6" stroke="#EA4335"/><text x="263" y="65" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#C5221F">L1: Hilang?</text>
              <text x="160" y="102" text-anchor="middle" font-family="Roboto" font-size="11.2" fill="#3C4043">Bagaimana mengirim sinyal balik</text>
              <text x="160" y="118" text-anchor="middle" font-family="Roboto" font-size="11.2" fill="#3C4043">tanpa tergerus puluhan layer?</text>

              <rect x="6" y="156" width="308" height="132" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.5"/>
              <text x="160" y="179" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#1A73E8">Tantangan 2: Ekor Sebelum Softmax</text>
              <rect x="20" y="197" width="84" height="34" rx="7" fill="#FFFFFF" stroke="#4285F4"/><text x="62" y="218" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#1A73E8">7×7×2048</text>
              <text x="116" y="218" text-anchor="middle" font-family="Poppins" font-size="14" fill="#1A73E8">&#8594;</text>
              <rect x="128" y="197" width="78" height="34" rx="7" fill="#FCE8E6" stroke="#EA4335" stroke-dasharray="4,2"/><text x="167" y="218" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#C5221F">[ ??? ]</text>
              <text x="218" y="218" text-anchor="middle" font-family="Poppins" font-size="14" fill="#1A73E8">&#8594;</text>
              <rect x="230" y="197" width="68" height="34" rx="7" fill="#E6F4EA" stroke="#34A853"/><text x="264" y="218" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#137333">5 Kelas</text>
              <text x="160" y="254" text-anchor="middle" font-family="Roboto" font-size="11.2" fill="#3C4043">Pengganti Flatten agar bobot kepala</text>
              <text x="160" y="270" text-anchor="middle" font-family="Roboto" font-size="11.2" fill="#3C4043">tidak membengkak jadi 51,38 juta!</text>
            </svg>""",
            vis_a_html="""<svg viewBox="0 0 320 296" style="width:100%; max-width:360px; height:auto;" aria-label="Jawaban Skip Connection dan GAP">
              <rect x="6" y="6" width="308" height="132" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
              <text x="160" y="27" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">1. Skip Connection: y = F(x) + x</text>
              <path d="M54,74 C96,38 224,38 264,74" fill="none" stroke="#F9AB00" stroke-width="3.5"/>
              <rect x="88" y="38" width="144" height="20" rx="10" fill="#FEF7E0" stroke="#F9AB00"/><text x="160" y="51.5" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#B06000">Jalur Tol +x (Gradien 86%+)</text>
              <rect x="24" y="72" width="60" height="30" rx="6" fill="#202124"/><text x="54" y="91" text-anchor="middle" font-family="Roboto Mono" font-size="10" fill="#FFF">Input x</text>
              <rect x="114" y="72" width="92" height="30" rx="6" fill="#E8F0FE" stroke="#4285F4"/><text x="160" y="91" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#1A73E8">Blok F(x)</text>
              <circle cx="264" cy="87" r="15" fill="#FEF7E0" stroke="#E37400" stroke-width="2"/><text x="264" y="92" text-anchor="middle" font-family="Poppins" font-size="15" font-weight="700" fill="#B06000">+</text>
              <text x="160" y="125" text-anchor="middle" font-family="Roboto" font-size="11" font-weight="700" fill="#137333">Layer 1 tetap tajam menangkap tepi!</text>

              <rect x="6" y="156" width="308" height="132" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
              <text x="160" y="179" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">2. Global Average Pooling (GAP)</text>
              <rect x="20" y="196" width="82" height="36" rx="7" fill="#FFFFFF" stroke="#34A853"/><text x="61" y="218" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#137333">7×7×2048</text>
              <text x="114" y="218" text-anchor="middle" font-family="Poppins" font-size="14" fill="#137333">&#8594;</text>
              <rect x="126" y="196" width="86" height="36" rx="7" fill="#34A853"/><text x="169" y="213" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#FFF">GAP</text><text x="169" y="226" text-anchor="middle" font-family="Roboto Mono" font-size="8.8" fill="#E6F4EA">2.048 angka</text>
              <text x="224" y="218" text-anchor="middle" font-family="Poppins" font-size="14" fill="#137333">&#8594;</text>
              <rect x="236" y="196" width="64" height="36" rx="7" fill="#FFFFFF" stroke="#34A853"/><text x="268" y="218" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#137333">Dense(5)</text>
              <text x="160" y="256" text-anchor="middle" font-family="Roboto Mono" font-size="11.5" font-weight="700" fill="#137333">51.38M &#8594; 10.245 param</text>
              <text x="160" y="273" text-anchor="middle" font-family="Roboto" font-size="11" fill="#3C4043">Pangkas &gt;99.9% bobot ekor model!</text>
            </svg>""",
            footer_label=FOOTER,
            notes="Alokasi waktu: 2 menit. Q&A #2 menguji pemahaman fungsi Skip Connection + GAP pada ResNet.",
            bar_color="yellow",
            correct_choice="B",
            data_title="Q&A #2 — Rahasia ResNet & GAP",
        )
    )

    # ==================================================================
    # BAB 4 — MOBILENETV2 & EFFICIENTNET + KOMPARASI (S22–S33, 19.0 menit)
    # ==================================================================
    slides.append(
        make_divider_slide(
            bg_class="bg-green",
            kicker="BAB 4 · ARSITEKTUR #4 &amp; #5 (ERA EFISIEN MODERN)",
            title="MobileNetV2 &amp; EfficientNet",
            description="Bagaimana merancang jaringan cerdas yang muat di HP, cepat dilatih di Google Colab, dan menjadi kandidat utama proyek Disney Frozen.",
            footer_label=FOOTER,
            data_title="Bab 4 — MobileNetV2 & EfficientNet",
            notes="Alokasi waktu: 1 menit. Masuk Bab 4 membedah Arsitektur #4 (MobileNetV2) dan #5 (EfficientNet) plus perbandingan 5 arsitektur.",
        )
    )

    # S23: #4.1 MobileNetV2 In General
    slides.append(f"""
    <section class="slide" data-title="#4.1 MobileNetV2 — Gambaran Umum" data-notes="Alokasi waktu: 1.5 menit. Penjelasan MobileNetV2 in general: dirancang ringan untuk mobile & Colab dengan 2.26M param (10x lebih kecil dari ResNet50).">
      <div class="kicker">ARSITEKTUR #4 · PENJELASAN IN GENERAL (BINTANG PROYEK)</div>
      <h2>MobileNetV2: <span class="hl-green">Kecerdasan CNN dalam Bodi Super Ramping</span></h2>
      {_arch_badge_row("4. MOBILENETV2 (BACKBONE UTAMA PROYEK &#9733;)", "green", [
          ("dark", "Foto 224×224×3", "Skala [-1 s.d. 1]"),
          ("blue", "Conv Awal 3×3", "32 Channel Dasar"),
          ("green", "17× Inverted Residual", "Depthwise + Linear"),
          ("yellow", "GAP (1280 Fitur)", "Ringkas Vektor"),
          ("green", "Dropout + Dense(5)", "Softmax Frozen"),
      ])}
      <div class="grid-2" style="flex:1; min-height:0; margin-top:10px; align-items:stretch;">
        <div class="card" style="display:flex; flex-direction:column; justify-content:flex-start; gap:10px;">
          <div class="card-title" style="color:#137333;">Kenapa Dunia Butuh MobileNetV2?</div>
          <ul class="clean" style="font-size:12.3px; line-height:1.48;">
            <li><strong>ResNet50</strong> beratnya <strong>{r_res['est_size_mb']} MB</strong> ({r_res['total_params']/1e6:.2f}M param) &mdash; lambat di HP dan terlalu kompleks untuk dataset kita yang berjumlah <strong>{tot_imgs} foto</strong>.</li>
            <li><strong>MobileNetV2</strong> memangkas beban menjadi hanya <strong>{r_mob['total_params']:,} parameter</strong> (<strong>{r_mob['est_size_mb']} MB</strong>!) dengan latensi <strong>~{r_res['latency_ms_8imgs']/r_mob['latency_ms_8imgs']:.1f}&times; lebih cepat</strong> di CPU.</li>
            <li>Di Keras, backbone ImageNet MobileNetV2 sudah tersedia bawaan dan menerima input rentang nilai piksel <code>[-1, +1]</code> lewat <code>preprocess_input</code>.</li>
          </ul>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:auto;">
            <div class="evo-prob">
              <div style="font-weight:700; color:#C5221F; margin-bottom:2px;">ResNet50 (Generasi #3)</div>
              <div><code>{r_res['total_params']/1e6:.2f}M</code> param · <code>{r_res['est_size_mb']} MB</code> · berat di CPU/HP.</div>
            </div>
            <div class="evo-sol">
              <div style="font-weight:700; color:#137333; margin-bottom:2px;">MobileNetV2 (Generasi #4)</div>
              <div><code>{r_mob['total_params']/1e6:.2f}M</code> param · <code>{r_mob['est_size_mb']} MB</code> · 10&times; lebih ramping!</div>
            </div>
          </div>
          <div class="callout green" style="font-size:11.6px;">
            <strong>Analogi Koki Spesialis:</strong> Daripada semua koki mencampur semua bahan sekaligus (Conv biasa), tiap koki cukup memotong 1 bahan dulu (<em>Depthwise</em>), lalu digabung ringan (<em>Pointwise 1&times;1</em>).
          </div>
        </div>
        <div class="card" style="display:flex; flex-direction:column; justify-content:flex-start; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
            <strong style="font-family:var(--font-title); font-size:12.5px;">Bukti Hematnya Komputasi &amp; Ukuran Model</strong>
            <span class="pill green" style="font-size:10px;">DATA NYATA</span>
          </div>
          <div style="background:#FFFFFF; border:1px solid #E8EAED; border-radius:10px; padding:6px;">
            <img src="assets/P03/04_mobilenetv2_depthwise.png" alt="Depthwise Separable vs Conv2D Biasa" style="width:100%; height:auto; max-height:215px; object-fit:contain; display:block; border-radius:6px;"/>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:auto;">
            <div class="mini-box" style="background:#E6F4EA; border-color:#CEEAD6; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.5px; font-weight:700; color:#137333;">GRAFIK KIRI · OPERASI BLOK</div>
              <div style="font-size:11.3px; color:#202124; margin-top:2px;"><code>231.2M</code> &#8594; <strong style="color:#137333;">27.5M ops (Hemat 8.4&times;)</strong></div>
            </div>
            <div class="mini-box" style="background:#F8F9FA; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.5px; font-weight:700; color:#5F6368;">GRAFIK KANAN · UKURAN BOBOT</div>
              <div style="font-size:11.3px; color:#202124; margin-top:2px;">ResNet50 <code>90.0 MB</code> &#8594; MobV2 <strong style="color:#137333;">8.6 MB</strong></div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S24: #4.2 Fitur Khusus MobileNetV2
    slides.append(f"""
    <section class="slide" data-title="#4.2 MobileNetV2 — Fitur Khusus" data-notes="Alokasi waktu: 2 menit. Bedah 3 inovasi MobileNetV2 sesuai PLAN.md P7: Depthwise Separable Convolution (hemat 8.4x), Inverted Residual, dan Linear Bottleneck.">
      <div class="kicker">ARSITEKTUR #4 · FITUR KHUSUS (SANDLER DKK., CVPR 2018)</div>
      <h2>3 Rahasia Rampingnya <span class="hl-green">MobileNetV2</span></h2>
      <div class="uc-grid" style="margin-top:6px; flex:1; min-height:0;">
        <div class="card" style="border-top:5px solid #34A853; display:flex; flex-direction:column; gap:8px;">
          <span class="pill green" style="width:fit-content;">FITUR #1 · HEMAT 8.4×</span>
          <div class="card-title" style="font-size:14px;">Depthwise Separable Conv</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Memecah <code>Conv2D 3×3</code> biasa menjadi 2 langkah terpisah: (a) <strong>Depthwise <code>3×3</code></strong> (tiap kanal difilter sendiri), lalu (b) <strong>Pointwise <code>1×1</code></strong> untuk mengaduk hasilnya antarkanal.</p>
          <div style="background:#F4FBF6; border:1px solid #CEEAD6; border-radius:10px; padding:8px;">
            <svg viewBox="0 0 264 96" width="100%" height="100" aria-label="Diagram Depthwise Separable">
              <rect x="6" y="8" width="252" height="28" rx="6" fill="#FCE8E6" stroke="#EA4335"/>
              <text x="132" y="21" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#C5221F">Conv2D 3×3 Biasa (Gabung Sekaligus)</text>
              <text x="132" y="32" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#C5221F">231.211.008 perkalian / blok!</text>
              <text x="132" y="48" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#137333">&#8595; Dipecah Jadi 2 Tahap Super Ringan &#8595;</text>
              <rect x="6" y="54" width="116" height="36" rx="6" fill="#FEF7E0" stroke="#F9AB00" stroke-width="1.5"/>
              <text x="64" y="69" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#B06000">1. Depthwise 3×3</text>
              <text x="64" y="81" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" fill="#5F6368">1 filter / kanal</text>
              <text x="132" y="76" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#137333">&#8594;</text>
              <rect x="142" y="54" width="116" height="36" rx="6" fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"/>
              <text x="200" y="69" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#137333">2. Pointwise 1×1</text>
              <text x="200" y="81" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" fill="#137333">Total 27.5M ops!</text>
            </svg>
          </div>
          <div style="font-size:11.3px; color:#3C4043;"><strong>Hasil Nyata:</strong> Kualitas peta fitur hampir setara <code>Conv2D 3×3</code> penuh namun beban perkalian turun hampir <strong>9 kali lipat</strong>.</div>
          <div class="formula-box" style="margin-top:auto; font-size:11px;">231.2M ops &#8594; <strong>27.5M ops</strong> (8.4× lebih ringan!)</div>
        </div>

        <div class="card" style="border-top:5px solid #4285F4; display:flex; flex-direction:column; gap:8px;">
          <span class="pill blue" style="width:fit-content;">FITUR #2 · POLA TERBALIK</span>
          <div class="card-title" style="font-size:14px;">Inverted Residual (Sempit-Lebar-Sempit)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">ResNet menyempitkan kanal dulu sebelum conv. MobileNetV2 justru membaliknya: kanal input ramping (<code>32</code>) diperluas <strong><code>6×</code> (<code>192</code>)</strong> di dalam blok agar <em>Depthwise</em> kaya pola, lalu diperas kembali jadi <code>32</code>.</p>
          <div style="background:#F8FAFF; border:1px solid #D2E3FC; border-radius:10px; padding:8px;">
            <svg viewBox="0 0 264 96" width="100%" height="100" aria-label="Diagram Inverted Residual">
              <path d="M26,70 Q132,96 238,70" fill="none" stroke="#34A853" stroke-width="2.2" stroke-dasharray="4,3"/>
              <text x="132" y="92" text-anchor="middle" font-family="Poppins" font-size="8" font-weight="700" fill="#137333">Skip +x antar jalur sempit</text>
              <rect x="6" y="26" width="40" height="44" rx="5" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.5"/>
              <text x="26" y="45" text-anchor="middle" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#1A73E8">32</text>
              <text x="26" y="57" text-anchor="middle" font-family="Poppins" font-size="7.2" fill="#5F6368">ch</text>
              <text x="53" y="51" text-anchor="middle" font-family="Poppins" font-size="11" fill="#5F6368">&#8594;</text>
              <rect x="60" y="6" width="64" height="68" rx="6" fill="#E6F4EA" stroke="#34A853" stroke-width="1.6"/>
              <text x="92" y="34" text-anchor="middle" font-family="Poppins" font-size="8.2" font-weight="700" fill="#137333">Expand 6×</text>
              <text x="92" y="48" text-anchor="middle" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#137333">192 ch</text>
              <text x="131" y="51" text-anchor="middle" font-family="Poppins" font-size="11" fill="#5F6368">&#8594;</text>
              <rect x="138" y="6" width="66" height="68" rx="6" fill="#FEF7E0" stroke="#F9AB00" stroke-width="1.6"/>
              <text x="171" y="34" text-anchor="middle" font-family="Poppins" font-size="8.2" font-weight="700" fill="#B06000">DW 3×3</text>
              <text x="171" y="48" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" font-weight="700" fill="#B06000">192 ch</text>
              <text x="211" y="51" text-anchor="middle" font-family="Poppins" font-size="11" fill="#5F6368">&#8594;</text>
              <rect x="218" y="26" width="40" height="44" rx="5" fill="#E8F0FE" stroke="#1A73E8" stroke-width="1.5"/>
              <text x="238" y="45" text-anchor="middle" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#1A73E8">32</text>
              <text x="238" y="57" text-anchor="middle" font-family="Poppins" font-size="7.2" fill="#5F6368">ch</text>
            </svg>
          </div>
          <div style="font-size:11.3px; color:#3C4043;"><strong>Kenapa Unik:</strong> Jalur sempit menghemat RAM antar-blok, sementara ruang lebar <code>192</code> memberi keleluasaan memfilter pola Elsa &amp; Olaf.</div>
          <div class="formula-box" style="margin-top:auto; font-size:11px;">32 ch &#8594; Expand 192 ch &#8594; Project 32 ch (+Skip)</div>
        </div>

        <div class="card" style="border-top:5px solid #FBBC04; display:flex; flex-direction:column; gap:8px;">
          <span class="pill yellow" style="width:fit-content;">FITUR #3 · TANPA POTONG</span>
          <div class="card-title" style="font-size:14px;">Linear Bottleneck (Tanpa ReLU di Ujung)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Ketika data berdimensi <code>192</code> diperas kembali ke <code>32</code> kanal ramping, <code>ReLU</code> akan menghapus semua angka negatif dan membuang informasi berharga. Solusinya: lapisan terakhir blok <strong>tanpa ReLU (Linear)</strong>!</p>
          <div style="background:#FFFDF6; border:1px solid #FDE293; border-radius:10px; padding:8px;">
            <svg viewBox="0 0 264 96" width="100%" height="100" aria-label="Diagram Linear Bottleneck">
              <rect x="6" y="10" width="252" height="36" rx="7" fill="#FCE8E6" stroke="#EA4335"/>
              <text x="132" y="25" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#C5221F">Pakai ReLU di Jalur Sempit (32 ch)</text>
              <text x="132" y="38" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#C5221F">[-0.8, +0.9, -0.4] &#8594; [0, +0.9, 0] (Hilang!)</text>
              <rect x="6" y="54" width="252" height="36" rx="7" fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"/>
              <text x="132" y="69" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#137333">Linear Bottleneck (Tanpa ReLU!)</text>
              <text x="132" y="82" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#137333">[-0.8, +0.9, -0.4] &#8594; Utuh tersimpan ✓</text>
            </svg>
          </div>
          <div style="font-size:11.3px; color:#3C4043;"><strong>Efek di MobileNetV2:</strong> 17 blok <code>project_BN</code> di Keras sengaja langsung menuju penjumlahan <code>Add()</code> tanpa aktivasi ReLU pemotong.</div>
          <div class="formula-box" style="margin-top:auto; font-size:11px;">Layer 1×1 Project = Linear (no ReLU!)</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S25: #4.3 Simulasi Full MobileNetV2
    slides.append(f"""
    <section class="slide" id="sim-mob-slide" data-title="#4.3 Simulasi Full MobileNetV2" data-notes="Alokasi waktu: 2 menit. Simulator #4: bandingkan langsung biaya komputasi Conv Biasa vs Depthwise+Pointwise MobileNetV2 dan aliran Inverted Residual.">
      <div class="kicker">ARSITEKTUR #4 · SIMULASI FULL MOBILENETV2</div>
      <h2>Simulasi MobileNetV2: <span class="hl-red">Conv Biasa</span> vs <span class="hl-green">Inverted Residual Block</span></h2>
      <div class="sim-bar pdf-keep-ui" id="sim-mob-bar">
        <button type="button" class="btn-ui" data-mob="standard" onclick="setMobSim('standard')">1. Mode Conv2D Biasa (3×3)</button>
        <button type="button" class="btn-ui outline" data-mob="mobilenetv2" onclick="setMobSim('mobilenetv2')">2. Mode MobileNetV2 (Expand &#8594; DW &#8594; Linear Project)</button>
        <div class="kpi-row">
          <span class="kpi-chip" id="mob-kpi-ops">Perkalian: 231.2 Juta</span>
          <span class="kpi-chip" id="mob-kpi-save">Efisiensi: Baseline 1×</span>
        </div>
      </div>

      <div class="grid-2" style="flex:1; min-height:0; margin-top:8px; align-items:stretch;">
        <div class="canvas-box" style="justify-content:space-between; gap:8px;">
          <strong style="font-family:var(--font-title); font-size:12px;" id="mob-vis-ttl">Pipa Konvolusi Standar 56×56×64 &#8594; 128 Channel</strong>
          <svg id="mob-sim-svg" viewBox="0 0 440 215" style="width:100%; flex:1; max-height:225px;"></svg>
          <div class="formula-box" id="mob-sim-formula" style="width:100%; font-size:11px;">
            <code>56 × 56 × 3 × 3 × 64 × 128 = 231.211.008</code> kali perkalian!
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:8px;">
          <div class="card sync-card sync-on sync-red" id="mob-stage-1" style="padding:11px 14px;">
            <div style="display:flex; justify-content:flex-start; align-items:center; gap:8px;"><strong style="font-family:var(--font-title); font-size:12.5px;">Langkah 1 · Expand 1×1 (+ ReLU6)</strong><span class="pill red" id="mob-p1" style="font-size:9.5px;">GABUNG PENUH</span></div>
            <div style="font-size:11.6px; color:#3C4043; margin-top:4px; line-height:1.42;" id="mob-st1-desc">Pada mode standar tidak ada pemisahan &mdash; semua <code>64×128</code> kombinasi kanal langsung dikalikan sekaligus dengan filter 3×3!</div>
          </div>
          <div class="card sync-card sync-on sync-red" id="mob-stage-2" style="padding:11px 14px;">
            <div style="display:flex; justify-content:flex-start; align-items:center; gap:8px;"><strong style="font-family:var(--font-title); font-size:12.5px;">Langkah 2 · Depthwise 3×3 per Kanal</strong><span class="pill red" id="mob-p2" style="font-size:9.5px;">231.2M OPS</span></div>
            <div style="font-size:11.6px; color:#3C4043; margin-top:4px; line-height:1.42;" id="mob-st2-desc">Filter 3×3 mengulang pemindaian ruang sekaligus mengaduk antar-kanal dalam 1 langkah berat (<code>231.2 juta</code> perkalian per blok).</div>
          </div>
          <div class="card sync-card sync-on sync-red" id="mob-stage-3" style="padding:11px 14px;">
            <div style="display:flex; justify-content:flex-start; align-items:center; gap:8px;"><strong style="font-family:var(--font-title); font-size:12.5px;">Langkah 3 · Linear Project 1×1 + Skip</strong><span class="pill red" id="mob-p3" style="font-size:9.5px;">PAKAI RELU</span></div>
            <div style="font-size:11.6px; color:#3C4043; margin-top:4px; line-height:1.42;" id="mob-st3-desc">Output langsung dipotong ReLU dan ukuran model menjadi sangat berat bila dipakai berulang untuk perangkat seluler.</div>
          </div>
          <div class="card card-tint green" style="margin-top:auto; padding:10px 13px;">
            <div style="font-family:var(--font-title); font-size:11.5px; font-weight:700; color:#137333;">BENCHMARK NYATA MOBILENETV2 (KERAS · 224×224×3)</div>
            <div style="font-family:var(--font-code); font-size:10.8px; color:#202124; margin-top:3px;">
              Total: <strong>{r_mob['total_params']:,}</strong> param ({r_mob['est_size_mb']} MB) · <strong>{r_mob['depthwise_layers']} DepthwiseConv2D</strong> · Latensi <strong>{r_mob['latency_ms_8imgs']} ms</strong>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S26: #4.4 Use Case MobileNetV2
    slides.append(f"""
    <section class="slide" data-title="#4.4 Use Case & Pemilihan MobileNetV2" data-notes="Alokasi waktu: 1.5 menit. Jelaskan use case MobileNetV2 di dunia nyata dan alasan ilmiah mengapa ia terpilih sebagai backbone utama proyek Frozen.">
      <div class="kicker">ARSITEKTUR #4 · USE CASE &amp; RELEVANSI PROYEK</div>
      <h2>Use Case <span class="hl-green">MobileNetV2</span>: Kenapa Jadi Jagoan Proyek Frozen?</h2>
      <div class="uc-grid" style="margin-top:4px; flex:1; min-height:0;">
        <div class="uc-card" style="border-top:4px solid #34A853;">
          <span class="pill green" style="width:fit-content;">&#10003; MOBILE &amp; EDGE AI</span>
          <div class="card-title" style="font-size:14px;">1. Kamera HP Real-Time (TFLite)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Aplikasi identifikasi tanaman, kode QR pintar, atau klasifikasi mainan langsung di Android/iOS tanpa perlu mengirim foto ke server.</p>
          <ul class="clean" style="font-size:11.4px; line-height:1.45; margin-top:4px;">
            <li><strong>Contoh Nyata:</strong> Kamera Google Lens ringan, scanner struk, robotika mini.</li>
            <li><strong>Keunggulan Edge:</strong> Model <code>{r_mob['est_size_mb']} MB</code> muat di cache aplikasi.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.45;">
            <strong style="color:#137333;">Kenapa Bisa Jalan Offline:</strong>
            <div>• Beban operasi 8.4&times; lebih ringan dari Conv biasa.</div>
            <div>• Hemat baterai &amp; RAM saat prediksi live.</div>
          </div>
          <div style="font-family:var(--font-code); font-size:10.5px; color:#137333; background:#E6F4EA; border-radius:7px; padding:5px 8px;">Target: HP Android/iOS · Raspberry Pi · Web</div>
        </div>

        <div class="uc-card" style="border-top:4px solid #4285F4;">
          <span class="pill blue" style="width:fit-content;">&#10003; DATASET KECIL ({tot_imgs} FOTO)</span>
          <div class="card-title" style="font-size:14px;">2. Transfer Learning Data Terbatas</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Hanya <strong>{r_mob['backbone_params']/1e6:.2f}M param</strong> di backbone (<code>{r_mob['depthwise_layers']}</code> <em>DepthwiseConv2D</em>) + fitur ImageNet siap pakai &#8594; risiko <em>overfitting</em> jauh lebih rendah dibanding model 23M+ parameter!</p>
          <ul class="clean" style="font-size:11.4px; line-height:1.45; margin-top:4px;">
            <li><strong>Bekal ImageNet (P04):</strong> Sudah kenal tekstur kain, wajah, &amp; warna dasar.</li>
            <li><strong>Input Standar:</strong> Normalisasi <code>[-1, +1]</code> via <code>preprocess_input</code>.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.45;">
            <strong style="color:#1A73E8;">Cocok untuk {tot_imgs} Foto Frozen:</strong>
            <div>• Kepala klasifikasi hanya <code>6.405</code> param (<code>1.280→5</code>).</div>
            <div>• Tahan overfit pada ~85–100 foto train <code>polos/ramai</code>.</div>
          </div>
          <div style="font-family:var(--font-code); font-size:10.5px; color:#1A73E8; background:#E8F0FE; border-radius:7px; padding:5px 8px;">Kunci: Tetap 100% CNN + Generalisasi Tinggi!</div>
        </div>

        <div class="uc-card" style="border-top:4px solid #FBBC04;">
          <span class="pill yellow" style="width:fit-content;">&#10003; TRANSFER LEARNING 2 TAHAP</span>
          <div class="card-title" style="font-size:14px;">3. Setup Resmi &amp; Eksperimen Cepat</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Ringan (~{r_mob['est_size_mb']} MB, {r_mob['latency_ms_8imgs']:.1f} ms/8 foto CPU) serta siap <strong>Grad-CAM</strong> lewat peta akhir <code>7×7×1280</code>.</p>
          <ul class="clean" style="font-size:11.4px; line-height:1.45; margin-top:4px;">
            <li><strong>Tahap 1 (P04/P06):</strong> Base beku + latih head <code>6.405</code> param.</li>
            <li><strong>Tahap 2 (P07/P08):</strong> <em>Fine-tune</em> akhir dengan <code>training=False</code>.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.45;">
            <strong style="color:#B06000;">vs CNN Polos Dari Nol:</strong>
            <div>• CNN polos 3 blok di 48×48 mentok <code>val_acc 34.3%</code>.</div>
            <div>• CNN Klasik dijadikan Baseline #1, MobV2 model utama!</div>
          </div>
          <div style="font-family:var(--font-code); font-size:10.5px; color:#B06000; background:#FEF7E0; border-radius:7px; padding:5px 8px;">Status: Rekomendasi Utama P04–P08</div>
        </div>
      </div>
      <div class="verdict-box winner" style="margin-top:10px;">
        <div>
          <div style="font-family:var(--font-title); font-size:12.5px; font-weight:700; color:#137333;">VERDICT PROYEK FROZEN · PILIHAN UTAMA: MOBILENETV2 (PRETRAINED CNN) &#9733;</div>
          <div style="font-size:12px; color:#202124; margin-top:2px;"><strong>MobileNetV2</strong> adalah CNN modern paling optimal untuk {tot_imgs} foto Frozen: memakai strategi <strong>Transfer Learning 2 Tahap</strong> (<code>training=False</code>) &amp; siap diaudit Grad-CAM di <strong>P08</strong>!</div>
        </div>
        <span class="pill green" style="font-size:11px; flex-shrink:0;">{r_mob['total_params']/1e6:.2f}M Param · {r_mob['est_size_mb']} MB</span>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S27: #5.1 EfficientNet In General
    slides.append(f"""
    <section class="slide" data-title="#5.1 EfficientNet — Gambaran Umum" data-notes="Alokasi waktu: 1 menit. Penjelasan EfficientNet in general sebagai evolusi lanjutan dari blok MobileNetV2 (MBConv + Compound Scaling + SE Attention).">
      <div class="kicker">ARSITEKTUR #5 · PENJELASAN IN GENERAL (GENERASI TERBARU DI KELUARGA EFISIEN)</div>
      <h2>EfficientNet: <span style="color:#8E24AA;">Menskalakan Model Secara Seimbang</span></h2>
      {_arch_badge_row("5. EFFICIENTNET-B0 (MBCONV + SE ATTENTION)", "blue", [
          ("dark", "Foto 224×224×3", "Skala Terukur &phi;"),
          ("blue", "Blok MBConv1/6", "Warisan MobileNetV2"),
          ("yellow", "SE Attention", "Bobot Fokus Kanal"),
          ("green", "GAP (1280 Fitur)", "Vektor Karakter"),
          ("green", "Dense(5)", "Softmax Frozen"),
      ])}
      <div class="grid-2" style="flex:1; min-height:0; margin-top:10px; align-items:stretch;">
        <div class="card" style="display:flex; flex-direction:column; justify-content:flex-start; gap:10px;">
          <div class="card-title" style="color:#681DA8;">Dari MobileNetV2 ke EfficientNet (Tan &amp; Le, ICML 2019)</div>
          <ul class="clean" style="font-size:12.3px; line-height:1.48;">
            <li>Setelah blok MobileNetV2 berhasil, peneliti bertanya: <em>"Kalau saya ingin model sedikit lebih pintar lagi, apakah cukup menambah jumlah layer saja?"</em></li>
            <li>Jawabannya tidak! Jika hanya memperdalam layer (<em>Depth</em>) tanpa memperlebar kanal (<em>Width</em>) dan memperjelas piksel foto (<em>Resolution</em>), model cepat jenuh.</li>
            <li>EfficientNet menggabungkan blok <strong>MBConv</strong> (keturunan langsung <em>Inverted Residual</em> MobileNetV2) + <strong>Compound Scaling</strong> + perhatian kanal (<strong>SE Attention</strong>)!</li>
          </ul>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:auto;">
            <div class="mini-box" style="background:#F3E8FD; border-color:#D7AEFB; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.5px; font-weight:700; color:#681DA8;">KOMPOSISI B0 NYATA</div>
              <div style="font-size:11.3px; color:#202124; margin-top:2px;"><code>{r_eff['total_params']/1e6:.2f}M</code> param · <code>{r_eff['layers_backbone']}</code> layers</div>
            </div>
            <div class="mini-box" style="background:#FCE8E6; border-color:#F6AEA9; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.5px; font-weight:700; color:#C5221F;">GERBANG FOKUS</div>
              <div style="font-size:11.3px; color:#202124; margin-top:2px;"><code>{r_eff['se_multiply_layers']} blok</code> SE Attention Multiply</div>
            </div>
          </div>
          <div class="callout blue" style="font-size:11.6px;">
            <strong>Analogi Lensa Zoom Seimbang:</strong> Memperbesar kamera tak cukup hanya menambah kaca (<em>Depth</em>), tapi juga bukaan cahaya (<em>Width</em>) dan kejernihan sensor (<em>Resolution</em>) bersamaan!
          </div>
        </div>
        <div class="card" style="display:flex; flex-direction:column; justify-content:flex-start; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
            <strong style="font-family:var(--font-title); font-size:12.5px;">Efek SE Attention pada Foto Elsa Latar Ramai</strong>
            <span class="pill" style="background:#F3E8FD; color:#681DA8; font-size:10px;">VISUAL FOKUS</span>
          </div>
          <div style="background:#FFFFFF; border:1px solid #E8EAED; border-radius:10px; padding:6px;">
            <img src="assets/P03/05_efficientnet_compound_se.png" alt="Efek SE Attention pada Elsa latar ramai" style="width:100%; height:auto; max-height:215px; object-fit:contain; display:block; border-radius:6px;"/>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:auto;">
            <div class="evo-prob">
              <div style="font-weight:700; color:#C5221F; margin-bottom:2px;">Tanpa SE Attention</div>
              <div>Cangkir Chip &amp; latar di belakang Elsa ikut menyala terang (distraksi!).</div>
            </div>
            <div class="evo-sol">
              <div style="font-weight:700; color:#137333; margin-bottom:2px;">Dengan SE Attention</div>
              <div>Kanal gaun biru Elsa disorot fokus, sementara objek latar diredam otomatis.</div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S28: #5.2 Fitur Khusus EfficientNet
    slides.append(f"""
    <section class="slide" data-title="#5.2 EfficientNet — Fitur Khusus" data-notes="Alokasi waktu: 1.5 menit. 3 fitur khusus EfficientNet: Compound Scaling (Depth x Width x Resolution), blok MBConv (16 Depthwise), dan Squeeze-and-Excitation (SE) Attention (16 Multiply).">
      <div class="kicker">ARSITEKTUR #5 · FITUR KHUSUS</div>
      <h2>3 Fitur Khusus EfficientNet: <span style="color:#8E24AA;">Compound Scaling</span> &amp; <span class="hl-red">SE Attention</span></h2>
      <div class="uc-grid" style="margin-top:6px; flex:1; min-height:0;">
        <div class="card" style="border-top:5px solid #8E24AA; display:flex; flex-direction:column; gap:8px;">
          <span class="pill" style="background:#F3E8FD; color:#681DA8; width:fit-content;">FITUR #1 · ATURAN SKALA</span>
          <div class="card-title" style="font-size:14px;">Compound Scaling (&phi;)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Menambah <strong>Kedalaman (Depth)</strong>, <strong>Lebar Kanal (Width)</strong>, dan <strong>Resolusi Input</strong> secara bersamaan dengan rasio tetap (<code>B0 &rarr; B1 &rarr; B2 &rarr; B7</code>) &mdash; bukan asal memperdalam saja!</p>
          <div style="background:#FAF5FF; border:1px solid #E9D5FF; border-radius:10px; padding:8px;">
            <svg viewBox="0 0 268 96" width="100%" height="100" aria-label="Diagram Compound Scaling">
              <rect x="4" y="32" width="64" height="50" rx="6" fill="#FFFFFF" stroke="#8E24AA" stroke-width="1.5"/>
              <text x="36" y="52" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#681DA8">B0 (&phi;=0)</text>
              <text x="36" y="67" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#5F6368">224px · 1×</text>
              <text x="79" y="60" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#8E24AA">&#8594;</text>
              <rect x="92" y="14" width="170" height="72" rx="8" fill="#F3E8FD" stroke="#8E24AA" stroke-width="1.8"/>
              <text x="177" y="32" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#681DA8">B2..B7 (&phi; Naik Seimbang!)</text>
              <rect x="102" y="42" width="46" height="34" rx="5" fill="#FFF" stroke="#D7AEFB"/><text x="125" y="57" text-anchor="middle" font-family="Poppins" font-size="8" font-weight="700" fill="#681DA8">Depth</text><text x="125" y="69" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#5F6368">Lapis &uarr;</text>
              <rect x="154" y="42" width="46" height="34" rx="5" fill="#FFF" stroke="#D7AEFB"/><text x="177" y="57" text-anchor="middle" font-family="Poppins" font-size="8" font-weight="700" fill="#681DA8">Width</text><text x="177" y="69" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#5F6368">Kanal &uarr;</text>
              <rect x="206" y="42" width="48" height="34" rx="5" fill="#FFF" stroke="#D7AEFB"/><text x="230" y="57" text-anchor="middle" font-family="Poppins" font-size="8" font-weight="700" fill="#681DA8">Resolusi</text><text x="230" y="69" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#5F6368">Piksel &uarr;</text>
            </svg>
          </div>
          <div style="font-size:11.3px; color:#3C4043;"><strong>Rumus Sederhana:</strong> Untuk sumber daya komputer 2<sup>&phi;</sup> lebih besar, naikkan ketiga dimensi secara proporsional agar tidak pincang.</div>
          <div class="formula-box" style="margin-top:auto; font-size:11px;">Depth &alpha;<sup>&phi;</sup> · Width &beta;<sup>&phi;</sup> · Resolution &gamma;<sup>&phi;</sup></div>
        </div>

        <div class="card" style="border-top:5px solid #34A853; display:flex; flex-direction:column; gap:8px;">
          <span class="pill green" style="width:fit-content;">FITUR #2 · WARISAN #4</span>
          <div class="card-title" style="font-size:14px;">Blok MBConv ({r_eff['depthwise_layers']} Depthwise)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Memakai blok <em>Inverted Residual</em> MobileNetV2 (Expand &#8594; Depthwise &#8594; Project + Skip), dilengkapi aktivasi halus <strong>Swish/SiLU</strong> yang sedikit lebih mulus dibanding ReLU.</p>
          <div style="background:#F4FBF6; border:1px solid #CEEAD6; border-radius:10px; padding:8px;">
            <svg viewBox="0 0 264 96" width="100%" height="100" aria-label="Diagram Blok MBConv">
              <rect x="6" y="24" width="54" height="38" rx="6" fill="#E8F0FE" stroke="#4285F4"/><text x="33" y="42" text-anchor="middle" font-family="Poppins" font-size="8.2" font-weight="700" fill="#1A73E8">Expand</text><text x="33" y="54" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#5F6368">1×1 Swish</text>
              <text x="66" y="46" text-anchor="middle" font-family="Poppins" font-size="11" fill="#137333">&#8594;</text>
              <rect x="72" y="24" width="58" height="38" rx="6" fill="#FEF7E0" stroke="#F9AB00"/><text x="101" y="42" text-anchor="middle" font-family="Poppins" font-size="8.2" font-weight="700" fill="#B06000">DWConv</text><text x="101" y="54" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#5F6368">3×3 / 5×5</text>
              <text x="136" y="46" text-anchor="middle" font-family="Poppins" font-size="11" fill="#137333">&#8594;</text>
              <rect x="142" y="24" width="52" height="38" rx="6" fill="#FCE8E6" stroke="#EA4335"/><text x="168" y="42" text-anchor="middle" font-family="Poppins" font-size="8.2" font-weight="700" fill="#C5221F">SE Gate</text><text x="168" y="54" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#C5221F">Multiply()</text>
              <text x="200" y="46" text-anchor="middle" font-family="Poppins" font-size="11" fill="#137333">&#8594;</text>
              <rect x="206" y="24" width="52" height="38" rx="6" fill="#E6F4EA" stroke="#34A853"/><text x="232" y="42" text-anchor="middle" font-family="Poppins" font-size="8.2" font-weight="700" fill="#137333">Project</text><text x="232" y="54" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#137333">+ Skip</text>
              <rect x="44" y="72" width="176" height="18" rx="9" fill="#E6F4EA" stroke="#CEEAD6"/><text x="132" y="84" text-anchor="middle" font-family="Poppins" font-size="8" font-weight="700" fill="#137333">Gabungan Inverted Residual + Fokus SE!</text>
            </svg>
          </div>
          <div style="font-size:11.3px; color:#3C4043;"><strong>Catatan Penting:</strong> <code>EfficientNetB0</code> menerima piksel mentah <code>[0, 255]</code> karena layer rescaling-nya sudah built-in di dalam model Keras!</div>
          <div class="formula-box" style="margin-top:auto; font-size:11px;">Keras B0: {r_eff['layers_backbone']} layers · {r_eff['skip_add_layers']} Skip Add</div>
        </div>

        <div class="card" style="border-top:5px solid #EA4335; display:flex; flex-direction:column; gap:8px;">
          <span class="pill red" style="width:fit-content;">FITUR #3 · FOKUS OBJEK</span>
          <div class="card-title" style="font-size:14px;">Squeeze-and-Excitation (SE)</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Jaringan memberi skor kepentingan <code>0..1</code> di tiap kanal (<code>Multiply</code>): kanal gaun biru Elsa dikali besar (<code>0.95</code>), sementara kanal cangkir/dinding <code>ramai</code> diredam (<code>0.12</code>)!</p>
          <div style="background:#FFF8F7; border:1px solid #FAD2CF; border-radius:10px; padding:8px;">
            <svg viewBox="0 0 264 96" width="100%" height="100" aria-label="Diagram SE Attention">
              <rect x="6" y="10" width="252" height="24" rx="6" fill="#E8F0FE" stroke="#4285F4"/>
              <text x="20" y="25" font-family="Poppins" font-size="8.3" font-weight="700" fill="#1A73E8">Kanal Gaun Elsa</text>
              <text x="150" y="25" font-family="Roboto Mono" font-size="8.3" font-weight="700" fill="#137333">× 0.95 (Fokus Utama!)</text>
              <rect x="6" y="40" width="252" height="24" rx="6" fill="#FCE8E6" stroke="#EA4335"/>
              <text x="20" y="55" font-family="Poppins" font-size="8.3" font-weight="700" fill="#C5221F">Kanal Cangkir Latar</text>
              <text x="150" y="55" font-family="Roboto Mono" font-size="8.3" font-weight="700" fill="#C5221F">× 0.12 (Diredam!)</text>
              <rect x="34" y="72" width="196" height="18" rx="9" fill="#FCE8E6" stroke="#F6AEA9"/><text x="132" y="84" text-anchor="middle" font-family="Poppins" font-size="8" font-weight="700" fill="#C5221F">Squeeze (GAP) &#8594; Excite (Sigmoid 0..1)</text>
            </svg>
          </div>
          <div style="font-size:11.3px; color:#3C4043;"><strong>Efek Nyata:</strong> Sangat membantu ketika objek Frozen berukuran kecil di tengah latar ruangan <code>ramai</code>.</div>
          <div class="formula-box" style="margin-top:auto; font-size:11px;">Keras B0: {r_eff['se_multiply_layers']} layer SE Multiply()</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S29: #5.3 Simulasi Full EfficientNet
    slides.append(f"""
    <section class="slide" id="sim-eff-slide" data-title="#5.3 Simulasi Full Arsitektur EfficientNet" data-notes="Alokasi waktu: 2 menit. Simulator #5: ubah tingkat Compound Scaling (B0 vs B1 vs B2) dan toggle SE Attention OFF vs ON pada foto Elsa berlatar ramai.">
      <div class="kicker">ARSITEKTUR #5 · SIMULASI FULL EFFICIENTNET</div>
      <h2>Simulasi EfficientNet: <span style="color:#8E24AA;">Compound Scaling</span> &amp; <span class="hl-red">SE Channel Attention</span></h2>
      <div class="sim-bar pdf-keep-ui" id="sim-eff-bar">
        <button type="button" class="btn-ui" data-eff-s="b0" onclick="setEffState({{scale:'b0'}})">B0 (&phi;=0 · 224px)</button>
        <button type="button" class="btn-ui outline" data-eff-s="b1" onclick="setEffState({{scale:'b1'}})">B1 (&phi;=1 · 240px)</button>
        <button type="button" class="btn-ui outline" data-eff-s="b2" onclick="setEffState({{scale:'b2'}})">B2 (&phi;=2 · 260px)</button>
        <button type="button" class="btn-ui outline" id="eff-se-btn" onclick="toggleEffSe()">SE Attention: OFF</button>
        <div class="kpi-row">
          <span class="kpi-chip" id="eff-kpi-meta">{r_eff['total_params']/1e6:.2f}M Param · {r_eff['est_size_mb']} MB</span>
        </div>
      </div>

      <div class="grid-2" style="flex:1; min-height:0; margin-top:8px; align-items:stretch;">
        <div class="card" style="display:flex; flex-direction:column; justify-content:space-between; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-family:var(--font-title); font-size:12.2px;">Bobot Perhatian Tiap Kanal pada Foto <code>elsa_ramai.jpg</code></strong>
            <span class="pill" id="eff-se-pill" style="background:#F1F3F4; color:#5F6368; font-size:10px;">SE OFF (Bobot Rata)</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:8px;" id="eff-se-bars"></div>
          <div style="background:#F8F9FA; border:1px solid #E8EAED; border-radius:10px; padding:7px 9px;">
            <div style="font-size:10px; font-weight:700; color:#5F6368; margin-bottom:4px;" id="eff-svg-cap">Visual Skala &amp; Gerbang SE Gate Saat Ini:</div>
            <svg id="eff-arch-svg" viewBox="0 0 430 82" width="100%" height="82" aria-label="Diagram Simulasi EfficientNet Compound Scaling dan SE"></svg>
          </div>
          <div class="callout blue" id="eff-callout" style="font-size:11.5px;">
            Tanpa SE Attention, semua kanal (termasuk latar dinding dan cangkir di belakang Elsa) mendapat bobot setara.
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:8px;">
          <div class="card sync-card sync-on sync-blue" id="eff-stage-scale" style="padding:11px 14px;">
            <div style="display:flex; justify-content:flex-start; align-items:center; gap:8px;"><strong style="font-family:var(--font-title); font-size:12.5px;">1. Compound Scaling (&phi;)</strong><span class="pill blue" id="eff-p1" style="font-size:9.5px;">B0 · BASELINE</span></div>
            <div style="font-size:11.7px; color:#3C4043; margin-top:4px; line-height:1.42;" id="eff-scale-desc">Skala <code>B0</code>: resolusi <code>224×224</code>, depth <code>1.0×</code>, width <code>1.0×</code> &#8594; <code>{r_eff['total_params']/1e6:.2f}M</code> parameter pada Frozen 5-kelas.</div>
          </div>
          <div class="card sync-card sync-on sync-red" id="eff-stage-se" style="padding:11px 14px;">
            <div style="display:flex; justify-content:flex-start; align-items:center; gap:8px;"><strong style="font-family:var(--font-title); font-size:12.5px;">2. SE Gate (Squeeze &#8594; Excite)</strong><span class="pill red" id="eff-p2" style="font-size:9.5px;">SE OFF</span></div>
            <div style="font-size:11.7px; color:#3C4043; margin-top:4px; line-height:1.42;" id="eff-se-desc">Klik tombol <strong>SE Attention: ON</strong> di atas untuk melihat bobot kanal latar diredam otomatis agar fokus ke gaun biru Elsa!</div>
          </div>
          <div class="card card-tint blue" style="padding:10px 13px;">
            <div style="font-family:var(--font-title); font-size:11.2px; font-weight:700; color:#681DA8;">HASIL KERAS NYATA (EfficientNetB0 · 224×224×3)</div>
            <div style="font-family:var(--font-code); font-size:10.5px; color:#202124; margin-top:3px;">
              Total: <strong>{r_eff['total_params']:,}</strong> ({r_eff['est_size_mb']} MB) · <strong>{r_eff['layers_backbone']} layers</strong> · <strong>{r_eff['se_multiply_layers']} SE Gate</strong> · <strong>{r_eff['latency_ms_8imgs']} ms</strong>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:10px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:11px; padding:8px 10px; margin-top:auto;">
            <img src="assets/P03/thumb_elsa_ramai.jpg" alt="Elsa Ramai" style="width:48px; height:48px; object-fit:cover; border-radius:8px; border:1px solid #DADCE0;"/>
            <div style="font-size:11px; color:#3C4043; line-height:1.38;"><strong>Kenapa masih lebih lambat di CPU?</strong> Karena <code>{r_eff['layers_backbone']}</code> layer + <code>{r_eff['se_multiply_layers']}</code> gerbang SE mengeksekusi lebih banyak cabang per langkah dibanding MobileNetV2.</div>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S30: #5.4 Use Case EfficientNet
    slides.append(f"""
    <section class="slide" data-title="#5.4 Use Case & Verdict EfficientNet" data-notes="Alokasi waktu: 1.5 menit. Use case EfficientNet di server/cloud dan mengapa posisinya sebagai runner-up pembanding MobileNetV2 di proyek Frozen.">
      <div class="kicker">ARSITEKTUR #5 · USE CASE &amp; RELEVANSI PROYEK</div>
      <h2>Use Case <span style="color:#8E24AA;">EfficientNet</span> &amp; Perbandingannya vs MobileNetV2</h2>
      <div class="uc-grid" style="margin-top:4px; flex:1; min-height:0;">
        <div class="uc-card" style="border-top:4px solid #34A853;">
          <span class="pill green" style="width:fit-content;">&#10003; CLOUD API / SERVER GPU</span>
          <div class="card-title" style="font-size:14px;">1. Klasifikasi E-Commerce &amp; Produk</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Menilai foto produk toko online di server GPU: butuh akurasi tertinggi dengan ukuran model yang tetap jauh lebih ringkas daripada ResNet50.</p>
          <ul class="clean" style="font-size:11.4px; line-height:1.45; margin-top:4px;">
            <li><strong>Contoh Nyata:</strong> Katalog fashion, sensor mutu pabrik, aplikasi cloud.</li>
            <li><strong>Skala B0–B7:</strong> Mudah dinaikkan jika GPU tersedia lebih besar.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.45;">
            <strong style="color:#137333;">Keunggulan di Latar Ramai:</strong>
            <div>• Gerbang SE membantu abaikan objek pengganggu.</div>
            <div>• Lebih hemat bobot 5.8&times; daripada ResNet50.</div>
          </div>
          <div style="font-family:var(--font-code); font-size:10.5px; color:#137333; background:#E6F4EA; border-radius:7px; padding:5px 8px;">Ideal bila tersedia GPU untuk training &amp; API</div>
        </div>

        <div class="uc-card" style="border-top:4px solid #8E24AA;">
          <span class="pill" style="background:#F3E8FD; color:#681DA8; width:fit-content;">&#10003; PEMBANDING RESMI</span>
          <div class="card-title" style="font-size:14px;">2. Pembanding MobileNetV2 di Notebook</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Sesuai <code>PLAN.md</code>, <code>EfficientNetB0</code> (<strong>{r_eff['total_params']/1e6:.2f}M param</strong>, {r_eff['est_size_mb']} MB) diuji berdampingan melawan MobileNetV2 untuk membuktikan alasan ilmiah pemilihan model!</p>
          <ul class="clean" style="font-size:11.4px; line-height:1.45; margin-top:4px;">
            <li><strong>Perbandingan Adil:</strong> Sama-sama punya arsitektur dasar MBConv.</li>
            <li><strong>Uji Eksperimen:</strong> Membuktikan apakah ekstra 16 blok SE sepadan.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.45;">
            <strong style="color:#681DA8;">Posisi di Proyek Frozen:</strong>
            <div>• Kandidat kuat upgrade jika foto <code>ramai</code> sulit.</div>
            <div>• Baseline pembanding di P06/P07.</div>
          </div>
          <div style="font-family:var(--font-code); font-size:10.5px; color:#681DA8; background:#F3E8FD; border-radius:7px; padding:5px 8px;">Peran: Runner-Up &amp; Pesaing Utama MobileNetV2</div>
        </div>

        <div class="uc-card" style="border-top:4px solid #FBBC04;">
          <span class="pill yellow" style="width:fit-content;">&#9888; TRADE-OFF EKSEKUSI</span>
          <div class="card-title" style="font-size:14px;">3. Batas Kecepatan CPU &amp; Preprocessing</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Pada uji CPU lokal kita (8 foto), <code>EfficientNetB0</code> memakan <strong>{r_eff['latency_ms_8imgs']:.1f} ms</strong> vs <strong>{r_mob['latency_ms_8imgs']:.1f} ms</strong> di MobileNetV2 (~{r_eff['latency_ms_8imgs']/r_mob['latency_ms_8imgs']:.1f}&times; lebih lambat) akibat banyaknya operasi cabang SE &amp; aktivasi besar.</p>
          <ul class="clean" style="font-size:11.4px; line-height:1.45; margin-top:4px;">
            <li><strong>Total Layer:</strong> {r_eff['layers_backbone']} layer vs {r_mob['layers_backbone']} layer di MobileNetV2.</li>
            <li><strong>Input Unik:</strong> Bawaan <code>[0, 255]</code> (jangan salah double-scaling!).</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.45;">
            <strong style="color:#B06000;">Alasan Belum Jadi #1 Pemula:</strong>
            <div>• Ukuran file ~2&times; lebih besar &amp; CPU ~{r_eff['latency_ms_8imgs']/r_mob['latency_ms_8imgs']:.1f}&times; lebih lambat.</div>
            <div>• Lebih sensitif tuning saat dataset masih {tot_imgs} foto.</div>
          </div>
          <div style="font-family:var(--font-code); font-size:10.5px; color:#B06000; background:#FEF7E0; border-radius:7px; padding:5px 8px;">Kesimpulan: MobileNetV2 tetap paling praktis!</div>
        </div>
      </div>
      <div class="verdict-box runner" style="margin-top:10px;">
        <div>
          <div style="font-family:var(--font-title); font-size:12.5px; font-weight:700; color:#681DA8;">VERDICT PROYEK FROZEN · RUNNER-UP &amp; KANDIDAT UPGRADE (GENERASI #5)</div>
          <div style="font-size:12px; color:#202124; margin-top:2px;">Paling menjanjikan bila nanti ingin mengejar akurasi ekstra pada foto <code>ramai</code>, sementara <strong>MobileNetV2</strong> menang mutlak di kesederhanaan, kecepatan, dan kestabilan transfer learning untuk pemula!</div>
        </div>
        <span class="pill" style="background:#8E24AA; color:#FFF; font-size:11px; flex-shrink:0;">{r_eff['total_params']/1e6:.2f}M Param · {r_eff['se_multiply_layers']} SE</span>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S31: MATRIKS RANGKUMAN 5 ARSITEKTUR (+ VIT/YOLO CONTEXT)
    slides.append(f"""
    <section class="slide" data-title="Matriks Perbandingan 5 Arsitektur" data-notes="Alokasi waktu: 2 menit. Rangkuman angka nyata Keras 5 arsitektur pada input 224x224x3 Frozen, grafik trade-off, dan catatan posisi ViT/YOLO di era modern.">
      <div class="kicker">SINTESIS BAB 1–4 · DATA BENCHMARK NYATA KERAS (INPUT 224×224×3)</div>
      <h2>Perbandingan Lengkap 5 Arsitektur + <span class="hl-blue">Posisi Model Modern</span></h2>
      <div class="grid-2" style="grid-template-columns:1.18fr 0.82fr; flex:1; min-height:0; gap:12px; align-items:stretch;">
        <div style="display:flex; flex-direction:column; gap:8px; justify-content:flex-start;">
          <table class="cmp-table">
            <thead>
              <tr><th>Arsitektur</th><th>Parameter</th><th>Ukuran</th><th>Latensi (8 foto)</th><th>Peran di Frozen</th></tr>
            </thead>
            <tbody>
              <tr><td><strong>1. MLP (2 Hidden)</strong></td><td>{r_mlp['total_params']:,}</td><td>{r_mlp['est_size_mb']} MB</td><td>{r_mlp['latency_ms_8imgs']} ms</td><td>Kontrol Negatif (Buta Spasial)</td></tr>
              <tr><td><strong>2. CNN Klasik</strong></td><td>{r_cnn['total_params']:,}</td><td>{r_cnn['est_size_mb']} MB</td><td>{r_cnn['latency_ms_8imgs']} ms</td><td>Baseline Awal (From Scratch)</td></tr>
              <tr><td><strong>3. ResNet50</strong></td><td>{r_res['total_params']:,}</td><td>{r_res['est_size_mb']} MB</td><td>{r_res['latency_ms_8imgs']} ms</td><td>Pembanding Berat (16 Skip)</td></tr>
              <tr class="row-winner"><td><strong>4. MobileNetV2 &#9733;</strong></td><td>{r_mob['total_params']:,}</td><td>{r_mob['est_size_mb']} MB</td><td>{r_mob['latency_ms_8imgs']} ms</td><td><strong>Pretrained CNN Utama ★</strong></td></tr>
              <tr><td><strong>5. EfficientNetB0</strong></td><td>{r_eff['total_params']:,}</td><td>{r_eff['est_size_mb']} MB</td><td>{r_eff['latency_ms_8imgs']} ms</td><td>Runner-Up (16 SE Attention)</td></tr>
            </tbody>
          </table>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
            <div class="mini-box" style="background:#E6F4EA; border-color:#CEEAD6; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.5px; font-weight:700; color:#137333;">REKOMENDASI UTAMA · PRETRAINED CNN</div>
              <div style="font-size:11.1px; color:#202124; margin-top:2px;"><strong>MobileNetV2</strong> (<code>8.64 MB</code>): latih head <code>6.405</code> param di P04/P06 lalu <em>fine-tune</em> <code>training=False</code> (P07) &amp; Grad-CAM <code>7×7</code> (P08).</div>
            </div>
            <div class="mini-box" style="background:#F3E8FD; border-color:#D7AEFB; padding:8px 10px;">
              <div style="font-family:var(--font-code); font-size:9.5px; font-weight:700; color:#681DA8;">BASELINE &amp; RUNNER-UP PEMBANDING</div>
              <div style="font-size:11.1px; color:#202124; margin-top:2px;"><strong>CNN Klasik</strong> jadi Baseline #1 (uji 48×48: <code>val_acc 34.3%</code>); <strong>EfficientNetB0</strong> (~2.9&times; lebih lambat) pembanding uji <code>ramai</code>.</div>
            </div>
          </div>
          <div class="callout blue" style="font-size:11.3px; margin-top:auto;">
            <strong>Catatan Lanskap Modern (Di Luar 5 Arsitektur Inti):</strong> <strong>Vision Transformer (ViT)</strong> memecah gambar jadi token layaknya teks (hebat jika dilatih jutaan foto, tapi mudah <em>overfit</em> di {tot_imgs} foto tanpa pretraining raksasa), sedangkan <strong>YOLO</strong> khusus tugas <em>Object Detection</em> (kotak banyak objek sekaligus).
          </div>
        </div>
        <div class="card" style="padding:10px 12px; display:flex; flex-direction:column; justify-content:flex-start; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-family:var(--font-title); font-size:12px;">Grafik Trade-Off Benchmark Keras</strong>
            <span class="pill green" style="font-size:9.5px;">MEASURED</span>
          </div>
          <div style="background:#FFFFFF; border:1px solid #E8EAED; border-radius:9px; padding:6px;">
            <img src="assets/P03/06_5arch_comparison_chart.png" alt="Grafik Benchmark 5 Arsitektur" style="width:100%; height:auto; max-height:245px; object-fit:contain; display:block; border-radius:6px;"/>
          </div>
          <div class="mini-box" style="margin-top:auto; font-size:11px; line-height:1.4; background:#F8F9FA;">
            <strong style="color:#137333;">Kuadran Terbaik (Kiri-Bawah):</strong> Parameter ringkas + latensi cepat ditempati <strong>MobileNetV2</strong> sebagai kompromi paling sehat.
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S32: Q&A #3
    slides.append(
        make_qa_slide(
            qa_id="qa-p03-3",
            qa_num=3,
            kicker="CEK PEMAHAMAN · Q&A #3 (STUDI KASUS KEPUTUSAN)",
            title_html='Menjadi Konsultan: <span class="hl-green">Pilih Arsitektur Terbaik</span>',
            question_html=f"Untuk proyek klasifikasi 5 karakter Disney Frozen kita (dataset awal <code>{tot_imgs}</code> foto <code>polos vs ramai</code>, akan dijalankan di Google Colab &amp; bisa dipasang di HP), arsitektur mana yang paling seimbang dipilih?",
            choices=[
                f"A. MLP karena waktu inferensi per batch-nya paling cepat ({r_mlp['latency_ms_8imgs']} ms)",
                f"B. ResNet50 karena jumlah parameternya paling besar ({r_res['total_params']/1e6:.2f}M param)",
                f"C. MobileNetV2 karena ringan ({r_mob['total_params']/1e6:.2f}M param / {r_mob['est_size_mb']} MB), cepat, dan tahan overfit pada data kecil",
            ],
            answer_html=f"<strong>Jawaban: C (MobileNetV2 — Pretrained CNN).</strong><br/>MobileNetV2 <strong>tetap keluarga CNN</strong>, tetapi saat base dibekukan kita hanya melatih <code>6.405</code> parameter kepala (sangat aman untuk ~85–100 foto train) dibanding CNN polos dari nol atau <code>ResNet50</code> ({r_res['est_size_mb']} MB)!",
            vis_q_html=f"""<svg viewBox="0 0 320 296" style="width:100%; max-width:360px; height:auto;" aria-label="Syarat Proyek Frozen">
              <rect x="6" y="6" width="308" height="136" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.5"/>
              <text x="160" y="30" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#1A73E8">Kandidat Soal &amp; Batasan Proyek</text>
              <rect x="20" y="44" width="280" height="24" rx="6" fill="#FFF" stroke="#AECBFA"/><text x="160" y="60" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="600" fill="#202124">1. Dataset Mini: {tot_imgs} foto polos &amp; ramai</text>
              <rect x="20" y="75" width="280" height="24" rx="6" fill="#FFF" stroke="#AECBFA"/><text x="160" y="91" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="600" fill="#202124">2. Perangkat: Colab Gratis &amp; Aplikasi HP</text>
              <rect x="20" y="106" width="280" height="24" rx="6" fill="#FFF" stroke="#AECBFA"/><text x="160" y="122" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="600" fill="#202124">3. Syarat: Kenal pola 2D + Tahan Overfit</text>

              <rect x="6" y="158" width="308" height="130" rx="12" fill="#FEF7E0" stroke="#F9AB00" stroke-width="1.5"/>
              <text x="160" y="181" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#B06000">3 Pilihan Kandidat</text>
              <rect x="18" y="196" width="88" height="76" rx="8" fill="#FCE8E6" stroke="#EA4335"/><text x="62" y="216" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#C5221F">A. MLP</text><text x="62" y="234" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#C5221F">{r_mlp['latency_ms_8imgs']} ms</text><text x="62" y="250" text-anchor="middle" font-family="Roboto" font-size="9" fill="#5F6368">Buta 2D?</text>
              <rect x="116" y="196" width="88" height="76" rx="8" fill="#FFF" stroke="#F9AB00"/><text x="160" y="216" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#B06000">B. ResNet50</text><text x="160" y="234" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#B06000">{r_res['est_size_mb']} MB</text><text x="160" y="250" text-anchor="middle" font-family="Roboto" font-size="9" fill="#5F6368">Terlalu berat?</text>
              <rect x="214" y="196" width="88" height="76" rx="8" fill="#E6F4EA" stroke="#34A853"/><text x="258" y="216" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#137333">C. MobV2</text><text x="258" y="234" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#137333">{r_mob['est_size_mb']} MB</text><text x="258" y="250" text-anchor="middle" font-family="Roboto" font-size="9" fill="#137333">Seimbang?</text>
            </svg>""",
            vis_a_html=f"""<svg viewBox="0 0 320 296" style="width:100%; max-width:360px; height:auto;" aria-label="Jawaban MobileNetV2 Pilihan Terbaik">
              <rect x="6" y="6" width="308" height="148" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
              <text x="160" y="34" text-anchor="middle" font-family="Poppins" font-size="14" font-weight="700" fill="#137333">&#9733; MobileNetV2 Pilihan Optimal</text>
              <rect x="22" y="50" width="130" height="42" rx="8" fill="#FFF" stroke="#34A853"/><text x="87" y="69" text-anchor="middle" font-family="Roboto Mono" font-size="12" font-weight="700" fill="#137333">{r_mob['total_params']/1e6:.2f}M Param</text><text x="87" y="83" text-anchor="middle" font-family="Roboto" font-size="9.5" fill="#5F6368">10× lebih ramping</text>
              <rect x="168" y="50" width="130" height="42" rx="8" fill="#FFF" stroke="#34A853"/><text x="233" y="69" text-anchor="middle" font-family="Roboto Mono" font-size="12" font-weight="700" fill="#137333">{r_mob['est_size_mb']} MB</text><text x="233" y="83" text-anchor="middle" font-family="Roboto" font-size="9.5" fill="#5F6368">Muat di HP &amp; Colab</text>
              <rect x="22" y="102" width="276" height="36" rx="8" fill="#34A853"/><text x="160" y="124" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#FFF">Depthwise Separable + Inverted Residual</text>

              <rect x="6" y="170" width="308" height="118" rx="12" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.4"/>
              <text x="160" y="193" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#C5221F">Kenapa Opsi A &amp; B Kalah?</text>
              <text x="160" y="220" text-anchor="middle" font-family="Roboto" font-size="11" fill="#202124">• Opsi A (MLP): Flatten bikin buta posisi 2D</text>
              <text x="160" y="242" text-anchor="middle" font-family="Roboto" font-size="11" fill="#202124">• Opsi B (ResNet50): {r_res['est_size_mb']} MB terlalu berat</text>
              <text x="160" y="264" text-anchor="middle" font-family="Roboto" font-size="11" font-weight="700" fill="#137333">MobileNetV2 dipakai sebagai tulang punggung P04–P08!</text>
            </svg>""",
            footer_label=FOOTER,
            notes="Alokasi waktu: 2 menit. Diskusi Q&A #3: konsolidasikan alasan memilih MobileNetV2 sebelum masuk istirahat dan hands-on.",
            bar_color="green",
            correct_choice="C",
            data_title="Q&A #3 — Konsultan Pemilihan Arsitektur",
        )
    )

    # S33: TRANSISI KE PRAKTIK KODE
    slides.append(f"""
    <section class="slide" data-title="Transisi Menuju Hands-On" data-notes="Alokasi waktu: 1 menit. Jembatan dari teori Bab 1–4 ke praktik notebook P03_arsitektur_neural_network.ipynb.">
      <div class="kicker">JEMBATAN TEORI &#8594; PRAKTIK KODE</div>
      <h2>Siap Membuktikan <span class="hl-blue">Ke-5 Arsitektur</span> Langsung di Keras?</h2>
      <div class="card-tint green" style="padding:12px 16px; margin-bottom:10px;">
        <div class="card-title" style="color:#137333; font-size:14.5px;">Semua Angka di Slide Tadi Bisa Kamu Bangun &amp; Uji Sendiri!</div>
        <p class="card-text" style="font-size:12.6px; margin-top:3px;">Dalam notebook <code>{SESSION.notebook_student_path.name}</code> (mode <strong>Visual-First</strong>, offline-safe dengan <code>weights=None</code> agar ringan dan cepat), kamu akan membuktikan 3 hal utama:</p>
      </div>
      <div class="uc-grid" style="flex:1; min-height:0;">
        <div class="card" style="border-top:5px solid #EA4335; display:flex; flex-direction:column; gap:8px;">
          <span class="pill red" style="width:fit-content;">BUKTI #1 · LANGKAH 1–3</span>
          <div class="card-title" style="color:#C5221F; font-size:14.5px;">MLP vs Conv2D &amp; CNN Klasik</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Melihat langsung <strong>MLP 9.64M param</strong> dibanding <strong>CNN 101K param</strong> dan menyaksikan foto Elsa berubah menjadi <em>Feature Map</em> tepi!</p>
          <ul class="clean" style="font-size:11.5px; line-height:1.45; margin-top:4px;">
            <li><strong>Langkah 1:</strong> Rakit MLP &amp; grafik ledakan param.</li>
            <li><strong>Langkah 2:</strong> Filter Sobel <code>3×3</code> + <code>MaxPooling2D(2)</code>.</li>
            <li><strong>Langkah 3:</strong> Rangkai 3 blok CNN + GAP &amp; kurva training.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; background:#FCE8E6; border-color:#F6AEA9;">
            <strong style="color:#C5221F;">Target Output:</strong> <code>ho_step1..3.png</code> &amp; <code># TODO 1–3</code> lolos!
          </div>
        </div>

        <div class="card" style="border-top:5px solid #FBBC04; display:flex; flex-direction:column; gap:8px;">
          <span class="pill yellow" style="width:fit-content;">BUKTI #2 · LANGKAH 4–5</span>
          <div class="card-title" style="color:#B06000; font-size:14.5px;">ResNet, MobileNetV2 &amp; EffNet</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Menyambungkan <code>layers.Add()</code> pada <strong>Mini-ResNet</strong>, lalu mengintip isi <strong>17 DepthwiseConv2D</strong> di MobileNetV2 &amp; <strong>16 SE Multiply</strong> di EfficientNetB0.</p>
          <ul class="clean" style="font-size:11.5px; line-height:1.45; margin-top:4px;">
            <li><strong>Langkah 4:</strong> Functional API <code>Add()</code> + cek <code>ResNet50</code>.</li>
            <li><strong>Langkah 5:</strong> Audit layer <code>MobileNetV2</code> &amp; <code>EfficientNetB0</code>.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; background:#FEF7E0; border-color:#FDE293;">
            <strong style="color:#B06000;">Target Output:</strong> Bukti 16 Skip, 17 DW, 16 SE (<code># TODO 4–6</code>)!
          </div>
        </div>

        <div class="card" style="border-top:5px solid #34A853; display:flex; flex-direction:column; gap:8px;">
          <span class="pill green" style="width:fit-content;">BUKTI #3 · LANGKAH 6</span>
          <div class="card-title" style="color:#137333; font-size:14.5px;">Benchmark 5 Arsitektur Frozen</div>
          <p class="card-text" style="font-size:12px; line-height:1.45;">Mencetak grafik kuadran &amp; tabel <code>results/p03_5_architectures_benchmark.csv</code> langsung dari pengukuran TensorFlow!</p>
          <ul class="clean" style="font-size:11.5px; line-height:1.45; margin-top:4px;">
            <li><strong>Langkah 6:</strong> Ukur parameter, MB, &amp; latensi 8 foto Frozen.</li>
            <li><strong>Mini-Challenge:</strong> Pilih arsitektur optimal 3 studi kasus.</li>
          </ul>
          <div class="mini-box" style="margin-top:auto; font-size:11px; background:#E6F4EA; border-color:#CEEAD6;">
            <strong style="color:#137333;">Artefak Resmi:</strong> File CSV &amp; kuadran di folder <code>results/</code>!
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # ==================================================================
    # BAB 5 — ISTIRAHAT, HANDS-ON VISUAL-FIRST, EVALUASI & PENUTUP (S34–S52)
    # ==================================================================
    slides.append(
        make_divider_slide(
            bg_class="bg-blue",
            kicker="BAB 5 · ISTIRAHAT SEJENAK (5 MENIT)",
            title="Istirahat 5 Menit",
            description="Minum air, regangkan mata & tangan sejenak. Setelah jeda, kita buka notebook dan membuktikan ke-5 arsitektur secara langsung!",
            footer_label=FOOTER,
            data_title="Istirahat 5 Menit",
            notes="Alokasi waktu: 5 menit. Jeda 5 menit sambil menyiapkan Google Colab / Jupyter Notebook P03.",
        )
    )

    # S35: Cover Peta Hands-On
    slides.append(
        make_cover_roadmap_slide(
            bg_class="bg-green",
            kicker="BAB 5 · PRAKTIK KODE VISUAL-FIRST (40 MENIT)",
            title="Hands-On Notebook P03",
            description="6 langkah terpandu membangun, membedah layer, dan membenchmark 5 arsitektur langsung pada data Frozen.",
            chips=[
                ("1", "Tahap 1 · MLP", "Bangun MLP Keras &amp; ukur ledakan 9.64M param"),
                ("2", "Tahap 2 · Conv2D", "Filter Sobel + MaxPool 2×2 pada foto Elsa nyata"),
                ("3", "Tahap 3 · CNN Klasik", "3 Blok Conv + GAP vs MLP (kurva training nyata)"),
                ("4", "Tahap 4 · Mini-ResNet", "Functional API Add() + inspeksi ResNet50 (16 Skip)"),
                ("5", "Tahap 5 · Mobile &amp; Eff", "Inspeksi MobileNetV2 (17 DW) &amp; EfficientNetB0 (16 SE)"),
                ("6", "Tahap 6 · Benchmark", "Ekspor tabel &amp; kuadran 5 arsitektur ke results/"),
            ],
            footer_label=FOOTER,
            data_title="Hands-On — Peta 6 Langkah",
            notes="Alokasi waktu: 2 menit. Tunjukkan peta 6 langkah praktik notebook + fitur Alat Visualisasi Siap Pakai.",
            grid_3x2=True,
            env_strip=f"&#128211; {SESSION.notebook_student_path.name} &nbsp;·&nbsp; &#128193; data/frozen_v1/ ({tot_imgs} foto) &nbsp;·&nbsp; &#9889; Offline-Safe (weights=None)",
        )
    )

    # S36–S41: 6 Visual-First Hands-On Step Slides
    slides.append(
        make_handson_step_slide(
            step_num=1,
            step_labels=ho_steps,
            stage_badge="Tahap 1 · # TODO 1",
            title="Membangun MLP Keras &amp; Bukti 9.64M Parameter",
            kicker="HANDS-ON · LANGKAH 1 / 6 (6 MENIT)",
            notebook_name=SESSION.notebook_student_path.name,
            goal_html="Membuktikan bagaimana 2 Hidden Layer <code>Dense</code> langsung meledakkan parameter menjadi <code>9.636.101</code> pada foto <code>224×224×3</code>.",
            bullets_html="""
              <li><span class="ho-sub-tag red">1</span><span>Jalankan <strong>Setup 1–3</strong> &amp; sel <strong>Alat Visualisasi Siap Pakai</strong> (<em>0 coding!</em>).</span></li>
              <li><span class="ho-sub-tag red">2</span><span><strong># TODO 1:</strong> Lengkapi <code>Dense(64, activation="relu")</code> &amp; <code>Dense(32, activation="relu")</code> setelah <code>Flatten()</code>.</span></li>
              <li><span class="ho-sub-tag red">3</span><span>Panggil helper grafik untuk membandingkan <code>P02 1-Layer</code> vs <code>MLP P03</code>.</span></li>
            """,
            code_snippet="""# Tahap 1 (# TODO 1): Rakit MLP 224x224x3 dan cek jumlah parameternya
model_mlp = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation="relu"),   # TODO 1A
    tf.keras.layers.Dense(32, activation="relu"),   # TODO 1B
    tf.keras.layers.Dense(5, activation="softmax")
])
tampilkan_ledakan_mlp(model_mlp)""",
            callout_html="<strong>Klik Logis!</strong> Hanya dengan menambah 64 neuron tersembunyi, bobot melompat dari 752 ribu menjadi <strong>9,64 juta</strong>!",
            color="red",
            footer_label=FOOTER,
            notes="Alokasi waktu: 6 menit. Pandu peserta menjalankan Setup 1-3, Alat Visualisasi, lalu mengisi # TODO 1.",
            theory_ref="Slide 06–08 — MLP In General & Simulasi",
            output_img="assets/P03/ho_step1_mlp_explosion.png",
            output_caption="Output Notebook Step 1: Perbandingan nyata 1-Layer P02 (0.75M) vs MLP 2-Hidden (9.64M) vs CNN Klasik (0.10M).",
            checklist_html="✓ <code>model_mlp.count_params() == 9636101</code><br/>✓ Grafik batang Step 1 tampil &amp; tersimpan",
        )
    )

    slides.append(
        make_handson_step_slide(
            step_num=2,
            step_labels=ho_steps,
            stage_badge="Tahap 2 · # TODO 2",
            title="Operasi Konvolusi 2D (Sobel) &amp; MaxPooling Nyata",
            kicker="HANDS-ON · LANGKAH 2 / 6 (6 MENIT)",
            notebook_name=SESSION.notebook_student_path.name,
            goal_html="Mengaplikasikan filter konvolusi <code>3×3</code> dan <code>MaxPooling2D(2)</code> langsung ke foto Elsa agar melihat lahirnya <em>Feature Map</em>.",
            bullets_html="""
              <li><span class="ho-sub-tag">1</span><span><strong># TODO 2A:</strong> Gunakan <code>layers.Conv2D(1, 3, use_bias=False)</code> untuk memindai foto Elsa.</span></li>
              <li><span class="ho-sub-tag">2</span><span><strong># TODO 2B:</strong> Ringkas ukuran peta fitur menggunakan <code>layers.MaxPooling2D((2, 2))</code>.</span></li>
              <li><span class="ho-sub-tag">3</span><span>Amati perbedaan foto asli, peta tepi <code>30×30</code>, hasil pool <code>15×15</code>, &amp; peta warna biru gaun Elsa!</span></li>
            """,
            code_snippet="""# Tahap 2 (# TODO 2): Filter Konvolusi 3x3 + MaxPool 2x2 pada foto Elsa
conv_layer = tf.keras.layers.Conv2D(1, kernel_size=3, use_bias=False)  # TODO 2A
pool_layer = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))            # TODO 2B
tampilkan_conv_pool_elsa(elsa_32, conv_layer, pool_layer)""",
            callout_html="<strong>Bukti Nyata!</strong> Garis kontur rambut, wajah, dan tepi gaun Elsa menyala terang hanya dari satu matriks kernel <code>3×3</code>.",
            color="blue",
            footer_label=FOOTER,
            notes="Alokasi waktu: 6 menit. Pandu peserta mengisi # TODO 2 dan membaca output 4 panel foto Elsa.",
            theory_ref="Slide 11–13 — CNN Klasik & Simulasi Kernel 3×3",
            output_img="assets/P03/ho_step2_conv_pool_map.png",
            output_caption="Output Notebook Step 2: Foto Elsa → Feature Map Tepi (30×30) → MaxPool 2×2 (15×15) → Filter Biru.",
            checklist_html="✓ Ukuran Feature Map mengecil separuh pasca <code>MaxPooling2D(2)</code><br/>✓ Siluet Elsa tampak jelas pada Feature Map",
        )
    )

    slides.append(
        make_handson_step_slide(
            step_num=3,
            step_labels=ho_steps,
            stage_badge="Tahap 3 · # TODO 3",
            title="Merakit CNN Klasik &amp; Membandingkan vs MLP",
            kicker="HANDS-ON · LANGKAH 3 / 6 (6 MENIT)",
            notebook_name=SESSION.notebook_student_path.name,
            goal_html="Membangun model <strong>CNN Klasik (3 Blok)</strong> + <code>GlobalAveragePooling2D()</code> (hanya <code>101.829</code> param) dan membandingkan belajarnya vs MLP.",
            bullets_html="""
              <li><span class="ho-sub-tag">1</span><span><strong># TODO 3:</strong> Rangkai 3 blok <code>Conv2D(..., padding="same", activation="relu")</code> + <code>MaxPooling2D(2)</code> lalu tutup dengan <code>GlobalAveragePooling2D()</code>.</span></li>
              <li><span class="ho-sub-tag">2</span><span>Lihat bagaimana CNN punya <strong>~95× lebih sedikit param</strong> dari MLP di <code>224×224</code> namun akurasinya lebih progresif!</span></li>
            """,
            code_snippet="""# Tahap 3 (# TODO 3): CNN Klasik (3 Blok Conv+Pool + GAP -> 101.829 param!)
model_cnn = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),
    tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu"),
    tf.keras.layers.MaxPooling2D(2),                                  # TODO 3A
    tf.keras.layers.Conv2D(64, 3, padding="same", activation="relu"),
    tf.keras.layers.MaxPooling2D(2),
    tf.keras.layers.Conv2D(128, 3, padding="same", activation="relu"),
    tf.keras.layers.MaxPooling2D(2),
    tf.keras.layers.GlobalAveragePooling2D(),                         # TODO 3B
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(5, activation="softmax")
])""",
            callout_html="<strong>Kenapa GAP dipakai?</strong> Tanpa GAP (jika pakai Flatten), ekor CNN bisa melonjak kembali jutaan bobot seperti VGG!",
            color="blue",
            footer_label=FOOTER,
            notes="Alokasi waktu: 6 menit. Pandu # TODO 3 lalu bandingkan grafik progres belajar MLP vs CNN.",
            theory_ref="Slide 11–14 — CNN Klasik & Hematnya Parameter Sharing",
            output_img="assets/P03/ho_step3_cnn_vs_mlp.png",
            output_caption="Output Notebook Step 3: Pada data Frozen 48×48, CNN Klasik (23.909 param) naik melampaui 40%, sementara MLP (444.677 param) stagnan di 22.2%!",
            checklist_html="✓ <code>model_cnn.count_params() == 101829</code><br/>✓ Grafik training curve muncul",
        )
    )

    slides.append(
        make_handson_step_slide(
            step_num=4,
            step_labels=ho_steps,
            stage_badge="Tahap 4 · # TODO 4",
            title="Mini-ResNet Block (<code>Add()</code>) &amp; Inspeksi <code>ResNet50</code>",
            kicker="HANDS-ON · LANGKAH 4 / 6 (7 MENIT)",
            notebook_name=SESSION.notebook_student_path.name,
            goal_html="Membuat blok <em>Skip Connection</em> nyata memakai Keras Functional API serta membedah anatomi <code>ResNet50</code>.",
            bullets_html="""
              <li><span class="ho-sub-tag yellow">1</span><span><strong># TODO 4A:</strong> Sambungkan cabang utama <code>fx</code> dan jalur pintas <code>shortcut</code> via <code>tf.keras.layers.Add()([fx, shortcut])</code>.</span></li>
              <li><span class="ho-sub-tag yellow">2</span><span><strong># TODO 4B:</strong> Muat <code>ResNet50(include_top=False, weights=None)</code> lalu hitung blok <code>Add()</code> (<code>16</code>) &amp; ukur bobotnya (<code>23.60M</code>).</span></li>
            """,
            code_snippet="""# Tahap 4 (# TODO 4): Sambungkan Skip Connection F(x) + x dengan Functional API
shortcut = x
fx = tf.keras.layers.Conv2D(16, 3, padding="same", activation="relu")(x)
fx = tf.keras.layers.Conv2D(16, 3, padding="same")(fx)
out_skip = tf.keras.layers.Add()([fx, shortcut])    # TODO 4A (F(x) + x)
out_skip = tf.keras.layers.ReLU()(out_skip)

res_base = tf.keras.applications.ResNet50(          # TODO 4B (Offline-Safe)
    include_top=False, weights=None, input_shape=(224, 224, 3)
)""",
            callout_html="<strong>Pelajaran Functional API:</strong> <code>Sequential</code> hanya lurus satu jalur; untuk membuat cabang <code>+x</code> seperti ResNet, kita memakai <strong>Functional API</strong>!",
            color="yellow",
            footer_label=FOOTER,
            notes="Alokasi waktu: 7 menit. Pastikan peserta memahami mengapa Sequential tidak bisa bercabang dan bagaimana Add() bekerja.",
            theory_ref="Slide 17–20 — ResNet Skip Connection & GAP",
            output_img="assets/P03/ho_step4_mini_resnet.png",
            output_caption="Output Notebook Step 4: Mini-ResNet menekan loss lebih rendah (0.762) daripada Plain Deep Net (0.963) + GAP memangkas 51.38M -> 10.245 param.",
            checklist_html="✓ <code>len([l for l in res_base.layers if isinstance(l, tf.keras.layers.Add)]) == 16</code>",
        )
    )

    slides.append(
        make_handson_step_slide(
            step_num=5,
            step_labels=ho_steps,
            stage_badge="Tahap 5 · # TODO 5–6",
            title="Membedah <code>MobileNetV2</code> &amp; <code>EfficientNetB0</code>",
            kicker="HANDS-ON · LANGKAH 5 / 6 (8 MENIT)",
            notebook_name=SESSION.notebook_student_path.name,
            goal_html="Memuat kedua arsitektur efisien modern (<code>weights=None</code>) dan membuktikan keberadaan layer <code>DepthwiseConv2D</code> &amp; blok <em>SE Attention</em> (<code>Multiply</code>).",
            bullets_html="""
              <li><span class="ho-sub-tag green">1</span><span><strong># TODO 5:</strong> Muat <code>MobileNetV2(include_top=False, weights=None)</code> lalu hitung jumlah <code>DepthwiseConv2D</code> (<code>17</code> layer!).</span></li>
              <li><span class="ho-sub-tag green">2</span><span><strong># TODO 6:</strong> Muat <code>EfficientNetB0(include_top=False, weights=None)</code> lalu hitung layer <code>Multiply</code> gerbang <em>SE Attention</em> (<code>16</code> layer!).</span></li>
            """,
            code_snippet="""# Tahap 5 (# TODO 5 & 6): Muat MobileNetV2 & EfficientNetB0 lalu audit layernya
mob_base = tf.keras.applications.MobileNetV2(       # TODO 5
    include_top=False, weights=None, input_shape=(224, 224, 3))
eff_base = tf.keras.applications.EfficientNetB0(    # TODO 6
    include_top=False, weights=None, input_shape=(224, 224, 3))

n_dw = sum(isinstance(l, tf.keras.layers.DepthwiseConv2D) for l in mob_base.layers)  # 17
n_se = sum(isinstance(l, tf.keras.layers.Multiply) for l in eff_base.layers)         # 16""",
            callout_html="<strong>Terbukti di Kode!</strong> MobileNetV2 hanya <code>8.64 MB</code> (~10× lebih kecil dari ResNet50 <code>90.02 MB</code>)!",
            color="green",
            footer_label=FOOTER,
            notes="Alokasi waktu: 8 menit. Ajak peserta melihat nama-nama layer MobileNetV2 (expanded_conv_depthwise, project) serta SE Multiply di EfficientNetB0.",
            theory_ref="Slide 23–30 — MobileNetV2 & EfficientNet",
            output_img="assets/P03/ho_step5_mobilenet_effnet.png",
            output_caption="Output Notebook Step 5: Hemat 8.4× Depthwise Separable Conv & perbandingan estimasi ukuran ResNet50 (90.0 MB) vs EffNetB0 (15.5 MB) vs MobileNetV2 (8.6 MB).",
            checklist_html="✓ <code>n_dw == 17</code> pada MobileNetV2 &amp; <code>n_se == 16</code> pada EfficientNetB0",
        )
    )

    slides.append(
        make_handson_step_slide(
            step_num=6,
            step_labels=ho_steps,
            stage_badge="Tahap 6 · # TODO 7–8",
            title="Benchmark 5 Arsitektur &amp; Ekspor <code>results/</code>",
            kicker="HANDS-ON · LANGKAH 6 / 6 (7 MENIT)",
            notebook_name=SESSION.notebook_student_path.name,
            goal_html="Mengukur waktu inferensi batch 8 foto Frozen nyata untuk seluruh 5 arsitektur lalu mengekspor grafik kuadran &amp; tabel CSV.",
            bullets_html="""
              <li><span class="ho-sub-tag green">1</span><span><strong># TODO 7:</strong> Kumpulkan hasil <code>benchmark_model()</code> untuk ke-5 model ke DataFrame <code>df_bench</code>.</span></li>
              <li><span class="ho-sub-tag green">2</span><span><strong># TODO 8:</strong> Simpan tabel ke <code>results/p03_5_architectures_benchmark.csv</code> dan grafik kuadran ke PNG.</span></li>
            """,
            code_snippet="""# Tahap 6 (# TODO 7 & 8): Benchmark 5 Arsitektur -> Simpan CSV & Grafik Kuadran
df_bench = kumpulkan_benchmark_5_arsitektur(daftar_5_model, batch_frozen_8)  # TODO 7
out_csv = RESULTS_DIR / "p03_5_architectures_benchmark.csv"
df_bench.to_csv(out_csv, index=False)                                        # TODO 8
plot_kuadran_5_arsitektur(df_bench, RESULTS_DIR / "p03_5_architectures_benchmark.png")""",
            callout_html="<strong>Artefak Laporan Bab Metode!</strong> Tabel CSV + grafik kuadran ini bisa langsung dipakai sebagai bukti ilmiah saat mempertahankan pemilihan <strong>MobileNetV2</strong>!",
            color="green",
            footer_label=FOOTER,
            notes="Alokasi waktu: 7 menit. Pastikan peserta mengekspor kedua file ke results/ dan bisa membaca kuadran trade-off.",
            theory_ref="Slide 31 — Matriks Perbandingan 5 Arsitektur",
            output_img="assets/P03/ho_step6_benchmark_quadrant.png",
            output_caption="Output Notebook Step 6: Grafik Parameter & Kuadran Trade-off Parameter vs Waktu Inferensi dari 5 arsitektur Keras nyata.",
            checklist_html="✓ File <code>results/p03_5_architectures_benchmark.csv</code> &amp; <code>.png</code> terbentuk",
        )
    )

    # S42: MINI-CHALLENGE (6 menit, Q->A expansion in PDF)
    slides.append(f"""
    <section class="slide" data-title="Mini-Challenge — Konsultan Arsitektur" data-notes="Alokasi waktu: 6 menit. Mini-Challenge: peserta mencocokkan 3 skenario dunia nyata ke arsitektur tepat dan merangkum draf 3 kalimat alasan memilih MobileNetV2.">
      <div class="kicker">MINI-CHALLENGE · STUDIO KEPUTUSAN ARSITEKTUR (6 MENIT)</div>
      <h2>Mini-Challenge: <span class="hl-blue">Tentukan Arsitektur Terbaik</span> untuk 3 Kasus!</h2>
      <div class="qa-box" style="flex:1; min-height:0; justify-content:flex-start; gap:12px;">
        <div class="uc-grid" style="margin-top:0;">
          <div class="mini-box" style="border-top:4px solid #4285F4; display:flex; flex-direction:column; gap:5px; padding:11px 13px;">
            <span class="pill blue" style="width:fit-content; font-size:9.5px;">KASUS A · DATA TABEL</span>
            <strong style="color:#1A73E8; font-size:13px;">Prediksi Harga Rumah CSV</strong>
            <p style="font-size:11.6px; margin:0; line-height:1.42;">File CSV berisi 12 kolom angka (luas rumah, jumlah kamar, jarak stasiun, usia bangunan). Tidak ada data gambar 2D sama sekali.</p>
            <div style="font-family:var(--font-code); font-size:10px; color:#1A73E8; background:#E8F0FE; border-radius:6px; padding:4px 7px; margin-top:auto;">Ciri: Data 1D tanpa piksel tetangga</div>
          </div>
          <div class="mini-box" style="border-top:4px solid #FBBC04; display:flex; flex-direction:column; gap:5px; padding:11px 13px;">
            <span class="pill yellow" style="width:fit-content; font-size:9.5px;">KASUS B · SERVER GPU</span>
            <strong style="color:#B06000; font-size:13px;">Radiologi X-Ray Rumah Sakit</strong>
            <p style="font-size:11.6px; margin:0; line-height:1.42;">200.000 citra medis di server ber-GPU ganda; prioritas utama akurasi tekstur halus, ukuran model {r_res['est_size_mb']} MB bukan masalah.</p>
            <div style="font-family:var(--font-code); font-size:10px; color:#B06000; background:#FEF7E0; border-radius:6px; padding:4px 7px; margin-top:auto;">Ciri: Data masif + GPU server besar</div>
          </div>
          <div class="mini-box" style="border-top:4px solid #34A853; display:flex; flex-direction:column; gap:5px; padding:11px 13px;">
            <span class="pill green" style="width:fit-content; font-size:9.5px;">KASUS C · APLIKASI HP</span>
            <strong style="color:#137333; font-size:13px;">Kamera Offline Frozen</strong>
            <p style="font-size:11.6px; margin:0; line-height:1.42;">{tot_imgs} foto 5 karakter Frozen (polos &amp; ramai), akan dilatih di Colab gratis &amp; dipasang di HP agar cepat mendeteksi langsung.</p>
            <div style="font-family:var(--font-code); font-size:10px; color:#137333; background:#E6F4EA; border-radius:6px; padding:4px 7px; margin-top:auto;">Ciri: Data mini + hemat RAM &amp; waktu</div>
          </div>
        </div>
        <div class="mini-box" style="background:#F8F9FA; border:1.2px solid #DADCE0; padding:10px 14px; font-size:12px; color:#202124; line-height:1.48;">
          <strong>Tugas Diskusi (6 Menit):</strong><br/>
          (1) Cocokkan arsitektur untuk <strong>Kasus A, B, C</strong> dari daftar <code>[MLP, CNN Klasik, ResNet50, MobileNetV2, EfficientNetB0]</code>.<br/>
          (2) Susun 3 kalimat draf <em>"Alasan Ilmiah Memilih MobileNetV2"</em> menggunakan angka nyata dari <code>df_bench</code> (param <code>{r_mob['total_params']/1e6:.2f}M</code>, ukuran <code>{r_mob['est_size_mb']} MB</code>, &amp; latensi <code>{r_mob['latency_ms_8imgs']} ms</code>).
        </div>
        <button type="button" class="btn-ui" onclick="toggleQA('mc-p03-ans', this)">Klik untuk Lihat Jawaban &amp; Pembahasan</button>
        <div class="qa-answer" id="mc-p03-ans" style="font-size:12px; line-height:1.48;">
          <strong>Jawaban Tepat:</strong><br/>
          • <strong>Kasus A &#8594; MLP:</strong> Data tabular 1D tidak memiliki grid piksel spasial sehingga lapisan <em>Fully-Connected Dense</em> sudah tepat.<br/>
          • <strong>Kasus B &#8594; ResNet50 (atau EfficientNet seri menengah):</strong> Tersedia GPU besar &amp; ratusan ribu citra; <em>Skip Connection</em> menjaga akurasi layer dalam.<br/>
          • <strong>Kasus C &#8594; MobileNetV2 (Pretrained CNN):</strong> Hanya <code>{r_mob['total_params']/1e6:.2f}M param ({r_mob['est_size_mb']} MB)</code> — latih head <code>6.405</code> param dulu (P04/P06), lalu <em>fine-tune</em> akhir dengan <code>training=False</code> (P07) &amp; audit Grad-CAM (P08)!
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S43: KAMUS ISTILAH P03 (Filterable 2-Column)
    slides.append(
        make_glossary_slide(
            kicker="GLOSARIUM RINGKAS · ARSITEKTUR NEURAL NETWORK",
            title_html='Kamus Istilah <span class="hl-blue">P03 (18 Istilah Asli)</span>',
            groups=[
                {
                    "ch": "1",
                    "color": "b1",
                    "label": "MLP",
                    "heading": "BAB 1 · MLP (FULLY-CONNECTED)",
                    "col": "left",
                    "grow": False,
                    "items": [
                        ("MLP", "Multi-Layer Perceptron: jaringan dengan Hidden Layer penuh (Dense).", 6, "mlp multi layer perceptron dense"),
                        ("Hidden Layer", "Lapisan neuron tersembunyi di antara Input dan Output.", 6, "hidden layer tersembunyi"),
                        ("Fully-Connected", "Setiap neuron terhubung ke semua neuron lapisan sebelumnya.", 7, "fully connected dense"),
                        ("Spatial Blindness", "Hilangnya hubungan posisi piksel 2D akibat diratakan (Flatten).", 7, "spatial blindness flatten posisi"),
                    ],
                },
                {
                    "ch": "2",
                    "color": "b2",
                    "label": "CNN",
                    "heading": "BAB 2 · CNN KLASIK (CONVOLUTION)",
                    "col": "left",
                    "grow": True,
                    "items": [
                        ("Kernel / Filter", "Matriks angka kecil (misal 3×3) pencari pola tepi atau warna.", 12, "kernel filter 3x3"),
                        ("Parameter Sharing", "Satu filter sama dipakai bergeser ke seluruh area foto (hemat bobot).", 12, "parameter sharing"),
                        ("Stride & Padding", "Panjang langkah geser filter (Stride) & bingkai nol di tepi (Padding).", 12, "stride padding"),
                        ("MaxPooling", "Mengambil nilai maksimum per kotak 2×2 agar ringkas & tahan geser.", 12, "maxpooling pooling"),
                        ("Feature Map", "Peta respons 2D hasil saringan sebuah filter konvolusi.", 13, "feature map peta fitur"),
                    ],
                },
                {
                    "ch": "3",
                    "color": "b4",
                    "label": "ResNet",
                    "heading": "BAB 3 · RESNET (JARINGAN DALAM)",
                    "col": "right",
                    "grow": False,
                    "items": [
                        ("Vanishing Gradient", "Sinyal belajar mengecil/hilang saat melewati terlalu banyak layer.", 17, "vanishing gradient degradation"),
                        ("Skip Connection", "Jalur pintas (F(x) + x) agar gradien dan informasi awal tetap utuh.", 18, "skip shortcut connection"),
                        ("BatchNorm", "Penstabil sebaran nilai angka antar layer agar training mulus.", 18, "batchnorm batch normalization"),
                        ("Global Avg Pooling", "Merata-ratakan tiap peta fitur menjadi 1 angka (gantikan Flatten raksasa).", 18, "global average pooling gap"),
                    ],
                },
                {
                    "ch": "4",
                    "color": "b3",
                    "label": "MobileNet & EffNet",
                    "heading": "BAB 4 · MOBILENETV2 & EFFICIENTNET",
                    "col": "right",
                    "grow": True,
                    "items": [
                        ("Depthwise Conv", "Konvolusi 3×3 per kanal mandiri, diikuti Pointwise 1×1 pengaduk.", 24, "depthwise separable pointwise"),
                        ("Inverted Residual", "Pola sempit -> mengembang 6× -> sempit lagi di blok MobileNetV2.", 24, "inverted residual expand"),
                        ("Linear Bottleneck", "Lapisan proyeksi sempit tanpa ReLU agar info tidak terpotong.", 24, "linear bottleneck"),
                        ("Compound Scaling", "Menyeimbangkan Depth, Width, & Resolution bersamaan lewat skala phi.", 28, "compound scaling efficientnet"),
                        ("SE Attention", "Squeeze-and-Excitation: memberi bobot prioritas ke kanal fitur paling penting.", 28, "se squeeze excitation attention"),
                    ],
                },
            ],
            footer_label=FOOTER,
            notes="Alokasi waktu: 2 menit. Ulas singkat 18 istilah teknis asli P03 dengan filter Bab dan tombol lompat SXX.",
            data_title="Kamus Istilah P03",
        )
    )

    # S44–S48: KUIS EVALUASI 5 SOAL (2 menit x 5 = 10 menit)
    quiz_specs = [
        {
            "num": 1,
            "data_title": "Kuis 1/5 — Kelemahan MLP pada Gambar",
            "kicker": "EVALUASI CEPAT · KUIS 1 / 5 (BAB 1 · MLP)",
            "title_html": 'Mengapa <span class="hl-red">MLP</span> Kurang Ideal untuk Foto Frozen?',
            "question_html": "Saat foto Frozen <code>224×224×3</code> dimasukkan ke MLP dengan Hidden Layer <code>Dense(64)</code>, apa kelemahan utamanya dibanding CNN?",
            "choices": [
                "A. Tidak bisa memakai fungsi aktivasi ReLU maupun Softmax",
                "B. Flatten membuang posisi tetangga 2D & menghasilkan jutaan parameter (9.64M) yang rentan pergeseran",
                "C. MLP tidak bisa menghasilkan 5 kelas probabilitas di output",
            ],
            "correct": "B",
            "answer": "<strong>Jawaban: B.</strong><br/>MLP tetap mendukung ReLU &amp; Softmax, tetapi keharusan meratakan gambar (<code>Flatten</code>) membuat bobot meledak ke <code>9.64 juta</code> dan mengikat bobot pada posisi koordinat kaku.",
            "vis_q": """<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Ilustrasi Kuis 1 MLP">
              <rect x="8" y="8" width="304" height="126" rx="12" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.5"/>
              <text x="160" y="31" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#C5221F">Foto Frozen &#8594; MLP</text>
              <rect x="22" y="48" width="74" height="36" rx="7" fill="#FFF" stroke="#4285F4"/><text x="59" y="69" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#1A73E8">224×224×3</text>
              <text x="110" y="70" text-anchor="middle" font-family="Poppins" font-size="13" fill="#C5221F">&#8594;</text>
              <rect x="122" y="48" width="76" height="36" rx="7" fill="#FFF" stroke="#EA4335"/><text x="160" y="69" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#C5221F">Flatten 1D</text>
              <text x="212" y="70" text-anchor="middle" font-family="Poppins" font-size="13" fill="#C5221F">&#8594;</text>
              <rect x="224" y="48" width="74" height="36" rx="7" fill="#EA4335"/><text x="261" y="69" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#FFF">9.64M</text>
              <text x="160" y="112" text-anchor="middle" font-family="Roboto" font-size="11.2" font-weight="700" fill="#C5221F">Apa risiko utamanya bagi foto?</text>

              <rect x="8" y="152" width="304" height="126" rx="12" fill="#F8F9FA" stroke="#DADCE0" stroke-width="1.4"/>
              <text x="160" y="178" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#3C4043">Cek 3 Kemungkinan</text>
              <text x="160" y="205" text-anchor="middle" font-family="Roboto" font-size="11" fill="#5F6368">1. Aktivasi ReLU &amp; Softmax?</text>
              <text x="160" y="226" text-anchor="middle" font-family="Roboto" font-size="11" fill="#5F6368">2. Buta tetangga 2D + boros bobot?</text>
              <text x="160" y="247" text-anchor="middle" font-family="Roboto" font-size="11" fill="#5F6368">3. Output 5 probabilitas kelas?</text>
            </svg>""",
            "vis_a": """<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Jawaban Kuis 1 MLP">
              <rect x="8" y="8" width="304" height="134" rx="12" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.8"/>
              <text x="160" y="33" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#C5221F">Risiko Ganda MLP pada Foto</text>
              <rect x="22" y="48" width="130" height="44" rx="8" fill="#FFF" stroke="#EA4335"/><text x="87" y="67" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#C5221F">Buta Spasial 2D</text><text x="87" y="82" text-anchor="middle" font-family="Roboto" font-size="9.5" fill="#5F6368">Posisi geser = keliru!</text>
              <rect x="168" y="48" width="130" height="44" rx="8" fill="#FFF" stroke="#EA4335"/><text x="233" y="67" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#C5221F">9.64M Param</text><text x="233" y="82" text-anchor="middle" font-family="Roboto" font-size="9.5" fill="#5F6368">Boros &amp; rawan overfit</text>
              <text x="160" y="122" text-anchor="middle" font-family="Roboto" font-size="11" font-weight="700" fill="#C5221F">ReLU &amp; Softmax tetap ada, tapi input 2D rusak!</text>

              <rect x="8" y="158" width="304" height="120" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
              <text x="160" y="185" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">Bandingkan dengan CNN (Bab 2)</text>
              <text x="160" y="216" text-anchor="middle" font-family="Roboto Mono" font-size="11.5" font-weight="700" fill="#137333">MLP 9.64M vs CNN 0.10M (95× Hemat!)</text>
              <text x="160" y="248" text-anchor="middle" font-family="Roboto" font-size="11" fill="#3C4043">CNN memakai kernel geser 3×3 menjaga pola 2D.</text>
            </svg>""",
            "color": "red",
        },
        {
            "num": 2,
            "data_title": "Kuis 2/5 — Hitung Output CNN",
            "kicker": "EVALUASI CEPAT · KUIS 2 / 5 (BAB 2 · CNN KLASIK)",
            "title_html": 'Menghitung Ukuran <span class="hl-blue">Feature Map</span> &amp; <span class="hl-green">MaxPool</span>',
            "question_html": "Jika sebuah input berukuran <code>10×10</code> melewati <code>Conv2D(Kernel=3×3, Stride=1, Padding=valid)</code> lalu diteruskan ke <code>MaxPooling2D(2×2)</code>, berapakah ukuran akhirnya?",
            "choices": [
                "A. 8×8 setelah Conv &#8594; 4×4 setelah MaxPool",
                "B. 10×10 setelah Conv &#8594; 5×5 setelah MaxPool",
                "C. 7×7 setelah Conv &#8594; 3×3 setelah MaxPool",
            ],
            "correct": "A",
            "answer": "<strong>Jawaban: A (8×8 &#8594; 4×4).</strong><br/>Langkah Conv: <code>(10 − 3 + 0) / 1 + 1 = 8×8</code>. Lalu <code>MaxPooling 2×2</code> membagi dua dimensi: <code>8 / 2 = 4×4</code>.",
            "vis_q": """<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Ilustrasi Kuis 2 Hitung Output CNN">
              <rect x="8" y="8" width="304" height="148" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.5"/>
              <text x="160" y="32" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#1A73E8">Alur Dimensi Peta Fitur</text>
              <rect x="18" y="52" width="66" height="44" rx="8" fill="#FFF" stroke="#4285F4"/><text x="51" y="72" text-anchor="middle" font-family="Roboto Mono" font-size="12" font-weight="700" fill="#1A73E8">10×10</text><text x="51" y="87" text-anchor="middle" font-family="Roboto" font-size="9" fill="#5F6368">Input</text>
              <text x="97" y="78" text-anchor="middle" font-family="Poppins" font-size="13" fill="#1A73E8">&#8594;</text>
              <rect x="110" y="52" width="84" height="44" rx="8" fill="#FEF7E0" stroke="#F9AB00"/><text x="152" y="71" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#B06000">Conv 3×3</text><text x="152" y="86" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#5F6368">pad=valid, s=1</text>
              <text x="207" y="78" text-anchor="middle" font-family="Poppins" font-size="13" fill="#1A73E8">&#8594;</text>
              <rect x="220" y="52" width="82" height="44" rx="8" fill="#FCE8E6" stroke="#EA4335" stroke-dasharray="4,2"/><text x="261" y="72" text-anchor="middle" font-family="Roboto Mono" font-size="12" font-weight="700" fill="#C5221F">? × ?</text><text x="261" y="87" text-anchor="middle" font-family="Roboto" font-size="9" fill="#C5221F">lalu Pool 2×2</text>
              <text x="160" y="130" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#1A73E8">Rumus: (N − K + 2P) / S + 1</text>

              <rect x="8" y="172" width="304" height="106" rx="12" fill="#F8F9FA" stroke="#DADCE0" stroke-width="1.4"/>
              <text x="160" y="200" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#3C4043">Diketahui:</text>
              <text x="160" y="226" text-anchor="middle" font-family="Roboto Mono" font-size="11.5" fill="#202124">N = 10 · K = 3 · P = 0 · S = 1</text>
              <text x="160" y="252" text-anchor="middle" font-family="Roboto" font-size="11" fill="#5F6368">Setelah itu MaxPooling 2×2 membagi dua ukuran.</text>
            </svg>""",
            "vis_a": """<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Jawaban Kuis 2 Output CNN">
              <rect x="8" y="8" width="304" height="132" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.6"/>
              <text x="160" y="34" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#1A73E8">Langkah 1 · Conv2D (3×3, Valid)</text>
              <rect x="24" y="48" width="272" height="34" rx="8" fill="#FFF" stroke="#AECBFA"/><text x="160" y="69" text-anchor="middle" font-family="Roboto Mono" font-size="12" font-weight="700" fill="#1A73E8">(10 − 3 + 0) / 1 + 1 = 8 × 8</text>
              <text x="160" y="108" text-anchor="middle" font-family="Roboto" font-size="11" fill="#3C4043">Tanpa padding, 1 piksel tepi atas/bawah/kiri/kanan</text>
              <text x="160" y="124" text-anchor="middle" font-family="Roboto" font-size="11" fill="#3C4043">terpotong sehingga 10×10 menyusut menjadi 8×8.</text>

              <rect x="8" y="156" width="304" height="122" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
              <text x="160" y="182" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">Langkah 2 · MaxPooling2D (2×2)</text>
              <rect x="24" y="196" width="272" height="36" rx="8" fill="#34A853"/><text x="160" y="219" text-anchor="middle" font-family="Roboto Mono" font-size="13" font-weight="700" fill="#FFF">8×8 &#8594; 4 × 4 (Dibagi 2!) ✓</text>
              <text x="160" y="258" text-anchor="middle" font-family="Roboto" font-size="11" fill="#137333">Ringkas ukuran &amp; lebih tahan geser!</text>
            </svg>""",
            "color": "blue",
        },
        {
            "num": 3,
            "data_title": "Kuis 3/5 — Fungsi Skip Connection",
            "kicker": "EVALUASI CEPAT · KUIS 3 / 5 (BAB 3 · RESNET)",
            "title_html": 'Mengapa <span class="hl-yellow">ResNet</span> Menambahkan <code>+ x</code>?',
            "question_html": "Masalah utama apa yang berhasil dipecahkan oleh <strong>Skip Connection (<code>y = F(x) + x</code>)</strong> saat membangun arsitektur dalam puluhan layer?",
            "choices": [
                "A. Membuat ukuran file gambar JPEG otomatis terkompresi lebih kecil",
                "B. Mencegah Vanishing Gradient / Degradation sehingga layer awal tetap mendapat sinyal belajar kuat",
                "C. Menghilangkan kebutuhan akan fungsi Softmax di ujung model",
            ],
            "correct": "B",
            "answer": "<strong>Jawaban: B.</strong><br/>Jalur pintas <code>+x</code> memberi jalan tol bagi gradien saat <em>backpropagation</em> maupun informasi awal ke layer dalam, terbukti di Frozen di mana Mini-ResNet mencapai akurasi validasi 2× Plain Deep Net!",
            "vis_q": """<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Ilustrasi Kuis 3 ResNet">
              <rect x="8" y="8" width="304" height="134" rx="12" fill="#FEF7E0" stroke="#F9AB00" stroke-width="1.5"/>
              <text x="160" y="32" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#B06000">Masalah CNN Polos 20–50 Layer</text>
              <rect x="22" y="50" width="76" height="32" rx="7" fill="#34A853"/><text x="60" y="70" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#FFF">L20: 100%</text>
              <text x="112" y="70" text-anchor="middle" font-family="Poppins" font-size="13" fill="#B06000">&#8594;</text>
              <rect x="126" y="50" width="68" height="32" rx="7" fill="#FFF" stroke="#DADCE0"/><text x="160" y="70" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#5F6368">...</text>
              <text x="208" y="70" text-anchor="middle" font-family="Poppins" font-size="13" fill="#EA4335">&#8594;</text>
              <rect x="222" y="50" width="76" height="32" rx="7" fill="#FCE8E6" stroke="#EA4335"/><text x="260" y="70" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#C5221F">L1: 7%</text>
              <text x="160" y="114" text-anchor="middle" font-family="Roboto" font-size="11.2" font-weight="700" fill="#B06000">Apa obat yang diberikan ResNet?</text>

              <rect x="8" y="158" width="304" height="120" rx="12" fill="#F8F9FA" stroke="#DADCE0" stroke-width="1.4"/>
              <text x="160" y="185" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#3C4043">Klu Rumus Blok ResNet:</text>
              <rect x="60" y="200" width="200" height="38" rx="8" fill="#FFF" stroke="#F9AB00"/><text x="160" y="224" text-anchor="middle" font-family="Roboto Mono" font-size="14" font-weight="700" fill="#B06000">y = F(x) + x</text>
              <text x="160" y="262" text-anchor="middle" font-family="Roboto" font-size="10.5" fill="#5F6368">Perhatikan jalur tambahan + x di luar F(x).</text>
            </svg>""",
            "vis_a": """<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Jawaban Kuis 3 Skip Connection">
              <rect x="8" y="8" width="304" height="138" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
              <text x="160" y="30" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">Jalur Tol Skip Connection (+x)</text>
              <path d="M56,78 C96,42 224,42 264,78" fill="none" stroke="#F9AB00" stroke-width="3.8"/>
              <rect x="88" y="42" width="144" height="20" rx="10" fill="#FEF7E0" stroke="#F9AB00"/><text x="160" y="55.5" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#B06000">Gradien L1 Tetap Kuat 86%+</text>
              <rect x="26" y="76" width="58" height="30" rx="6" fill="#202124"/><text x="55" y="95" text-anchor="middle" font-family="Roboto Mono" font-size="10" fill="#FFF">Input x</text>
              <rect x="114" y="76" width="92" height="30" rx="6" fill="#E8F0FE" stroke="#4285F4"/><text x="160" y="95" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#1A73E8">Blok F(x)</text>
              <circle cx="264" cy="91" r="14" fill="#FEF7E0" stroke="#E37400" stroke-width="2"/><text x="264" y="96" text-anchor="middle" font-family="Poppins" font-size="14" font-weight="700" fill="#B06000">+</text>
              <text x="160" y="130" text-anchor="middle" font-family="Roboto" font-size="11" font-weight="700" fill="#137333">Anti Vanishing Gradient / Degradation!</text>

              <rect x="8" y="162" width="304" height="116" rx="12" fill="#FEF7E0" stroke="#F9AB00" stroke-width="1.4"/>
              <text x="160" y="190" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#B06000">Bukti Eksperimen Frozen (12 Layer)</text>
              <text x="160" y="218" text-anchor="middle" font-family="Roboto Mono" font-size="11.5" font-weight="700" fill="#137333">Val Acc: Mini-ResNet 2× Plain Deep!</text>
              <text x="160" y="246" text-anchor="middle" font-family="Roboto" font-size="10.8" fill="#3C4043">Parameter kembar (24.373), hasil belajar jauh tajam.</text>
            </svg>""",
            "color": "yellow",
        },
        {
            "num": 4,
            "data_title": "Kuis 4/5 — Rahasia MobileNetV2",
            "kicker": "EVALUASI CEPAT · KUIS 4 / 5 (BAB 4 · MOBILENETV2)",
            "title_html": 'Mengapa <span class="hl-green">MobileNetV2</span> Jauh Lebih Ringan?',
            "question_html": f"Tiga ciri arsitektur manakah yang membuat <strong>MobileNetV2</strong> hanya berbobot <code>{r_mob['total_params']/1e6:.2f}M</code> param (hemat ~8.4× hitungan dibanding konvolusi biasa)?",
            "choices": [
                "A. Membuang semua layer konvolusi dan menggantinya dengan Dense layer",
                "B. Depthwise Separable Convolution + Inverted Residual (Expand 6×) + Linear Bottleneck",
                "C. Menggunakan kernel raksasa 11×11 di seluruh lapisan model",
            ],
            "correct": "B",
            "answer": "<strong>Jawaban: B.</strong><br/>Memisahkan filter spasial per kanal (<em>Depthwise</em>) dan pengadukan kanal (<em>Pointwise 1×1</em>) memotong perkalian secara drastis, sementara <em>Linear Bottleneck</em> menjaga informasi di jalur sempit tanpa terpotong ReLU.",
            "vis_q": f"""<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Ilustrasi Kuis 4 MobileNetV2">
              <rect x="8" y="8" width="304" height="132" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"/>
              <text x="160" y="32" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">Duel Ukuran &amp; Biaya Komputasi</text>
              <rect x="22" y="50" width="124" height="44" rx="8" fill="#FEF7E0" stroke="#F9AB00"/><text x="84" y="69" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#B06000">ResNet50</text><text x="84" y="84" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#C5221F">{r_res['est_size_mb']} MB</text>
              <text x="160" y="76" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#5F6368">vs</text>
              <rect x="174" y="50" width="124" height="44" rx="8" fill="#34A853"/><text x="236" y="69" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#FFF">MobileNetV2</text><text x="236" y="84" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#E6F4EA">{r_mob['est_size_mb']} MB</text>
              <text x="160" y="120" text-anchor="middle" font-family="Roboto" font-size="11.2" font-weight="700" fill="#137333">Apa 3 rahasia di balik efisiensinya?</text>

              <rect x="8" y="156" width="304" height="122" rx="12" fill="#F8F9FA" stroke="#DADCE0" stroke-width="1.4"/>
              <text x="160" y="184" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#3C4043">Target Operasi 1 Blok</text>
              <text x="160" y="214" text-anchor="middle" font-family="Roboto Mono" font-size="12.5" font-weight="700" fill="#137333">231.2M ops &#8594; 27.5M ops (8.4×)</text>
              <text x="160" y="248" text-anchor="middle" font-family="Roboto" font-size="11" fill="#5F6368">Di Keras terdapat {r_mob['depthwise_layers']} layer DepthwiseConv2D!</text>
            </svg>""",
            "vis_a": """<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Jawaban Kuis 4 MobileNetV2">
              <rect x="8" y="8" width="304" height="270" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
              <text x="160" y="34" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#137333">3 Kunci Utama MobileNetV2 ✓</text>

              <rect x="20" y="50" width="280" height="58" rx="9" fill="#FFF" stroke="#34A853" stroke-width="1.4"/>
              <text x="160" y="72" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#137333">1. Depthwise Separable Conv</text>
              <text x="160" y="92" text-anchor="middle" font-family="Roboto" font-size="10.5" fill="#3C4043">Pisah filter 3×3 per kanal + aduk 1×1 (Hemat 8.4×)</text>

              <rect x="20" y="120" width="280" height="58" rx="9" fill="#FFF" stroke="#4285F4" stroke-width="1.4"/>
              <text x="160" y="142" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#1A73E8">2. Inverted Residual (Expand 6×)</text>
              <text x="160" y="162" text-anchor="middle" font-family="Roboto" font-size="10.5" fill="#3C4043">Sempit (32) → Lebar (192) → Sempit (32) + Skip</text>

              <rect x="20" y="190" width="280" height="58" rx="9" fill="#FFF" stroke="#F9AB00" stroke-width="1.4"/>
              <text x="160" y="212" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#B06000">3. Linear Bottleneck (No ReLU)</text>
              <text x="160" y="232" text-anchor="middle" font-family="Roboto" font-size="10.5" fill="#3C4043">Ujung blok sempit tanpa ReLU agar info tidak hilang</text>
            </svg>""",
            "color": "green",
        },
        {
            "num": 5,
            "data_title": "Kuis 5/5 — Compound Scaling & SE",
            "kicker": "EVALUASI CEPAT · KUIS 5 / 5 (BAB 4 · EFFICIENTNET)",
            "title_html": 'Konsep Inti <span style="color:#8E24AA;">EfficientNet</span> pada Latar Ramai',
            "question_html": "Apa peran <strong>Compound Scaling (&phi;)</strong> dan <strong>Squeeze-and-Excitation (SE)</strong> pada arsitektur EfficientNet?",
            "choices": [
                "A. Compound Scaling menyeimbangkan Depth, Width, &amp; Resolusi bersamaan; SE Attention memberi bobot ekstra pada kanal ciri penting",
                "B. Keduanya berfungsi untuk menghapus seluruh label kelas pada metadata.csv",
                "C. EfficientNet tidak memakai konvolusi sama sekali melainkan Self-Attention penuh seperti ViT",
            ],
            "correct": "A",
            "answer": "<strong>Jawaban: A.</strong><br/>EfficientNet masih berbasis blok konvolusi (<code>MBConv</code> turunan MobileNetV2), lalu ditingkatkan secara seimbang lewat <em>Compound Scaling</em> dan dipasangi <em>SE Attention</em> agar kanal ciri objek menonjol di atas latar ramai.",
            "vis_q": """<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Ilustrasi Kuis 5 EfficientNet">
              <rect x="8" y="8" width="304" height="128" rx="12" fill="#F3E8FD" stroke="#8E24AA" stroke-width="1.5"/>
              <text x="160" y="32" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#681DA8">1. Compound Scaling (B0 &#8594; B2..B7)</text>
              <rect x="24" y="48" width="84" height="44" rx="8" fill="#FFF" stroke="#D7AEFB"/><text x="66" y="74" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#681DA8">Depth?</text>
              <rect x="118" y="48" width="84" height="44" rx="8" fill="#FFF" stroke="#D7AEFB"/><text x="160" y="74" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#681DA8">Width?</text>
              <rect x="212" y="48" width="84" height="44" rx="8" fill="#FFF" stroke="#D7AEFB"/><text x="254" y="74" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#681DA8">Resolusi?</text>
              <text x="160" y="118" text-anchor="middle" font-family="Roboto" font-size="11" fill="#681DA8">Bagaimana ketiganya dinaikkan?</text>

              <rect x="8" y="152" width="304" height="126" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.5"/>
              <text x="160" y="178" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#1A73E8">2. SE Gate pada Latar Ramai</text>
              <text x="160" y="212" text-anchor="middle" font-family="Roboto" font-size="11.5" fill="#202124">Gaun Biru Elsa vs Cangkir Latar Belakang</text>
              <text x="160" y="246" text-anchor="middle" font-family="Roboto Mono" font-size="11.5" font-weight="700" fill="#1A73E8">Bobot Kanal = [ ? , ? ]</text>
            </svg>""",
            "vis_a": f"""<svg viewBox="0 0 320 290" style="width:100%; max-width:350px; height:auto;" aria-label="Jawaban Kuis 5 EfficientNet">
              <rect x="8" y="8" width="304" height="128" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
              <text x="160" y="33" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">1. Scale Seimbang (Compound φ) ✓</text>
              <rect x="26" y="48" width="268" height="36" rx="8" fill="#FFF" stroke="#34A853"/><text x="160" y="71" text-anchor="middle" font-family="Roboto Mono" font-size="11.5" font-weight="700" fill="#137333">Depth &amp; Width &amp; Resolusi Naik Bareng</text>
              <text x="160" y="114" text-anchor="middle" font-family="Roboto" font-size="11" fill="#3C4043">Bukan Self-Attention ViT, tetap berbasis MBConv!</text>

              <rect x="8" y="152" width="304" height="126" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
              <text x="160" y="177" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">2. SE Attention ({r_eff['se_multiply_layers']} Blok Multiply) ✓</text>
              <rect x="22" y="192" width="132" height="40" rx="8" fill="#34A853"/><text x="88" y="216" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#FFF">Gaun Elsa ×0.95</text>
              <rect x="166" y="192" width="132" height="40" rx="8" fill="#FCE8E6" stroke="#EA4335"/><text x="232" y="216" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#C5221F">Latar ×0.12</text>
              <text x="160" y="258" text-anchor="middle" font-family="Roboto" font-size="10.8" font-weight="700" fill="#137333">Kanal objek penting otomatis dikuatkan!</text>
            </svg>""",
            "color": "blue",
        },
    ]

    for q in quiz_specs:
        slides.append(
            make_qa_slide(
                qa_id=f"quiz-p03-{q['num']}",
                qa_num=q["num"],
                kicker=q["kicker"],
                title_html=q["title_html"],
                question_html=q["question_html"],
                choices=q["choices"],
                answer_html=q["answer"],
                vis_q_html=q["vis_q"],
                vis_a_html=q["vis_a"],
                footer_label=FOOTER,
                notes=f"Alokasi waktu: 2 menit. Kuis {q['num']}/5: ajak peserta menebak opsi A/B/C sebelum membuka jawaban.",
                bar_color=q["color"],
                correct_choice=q["correct"],
                data_title=q["data_title"],
                quiz_progress_idx=q["num"],
                quiz_total=5,
            )
        )

    # S49: 3 POIN UTAMA (WHITE GOOGLE I/O)
    slides.append(
        make_summary_3pillars_slide(
            session_id="P03",
            title_html='3 Poin Utama <span class="hl-blue">Arsitektur Neural Network</span>',
            kicker="RANGKUMAN SESI · P03",
            pillars=[
                {
                    "bar": "blue",
                    "badge": "EVOLUSI KAUSAL",
                    "title": "Lahir dari Cacat Nyata",
                    "bullets": [
                        "<strong>MLP</strong> buta spasi 2D &amp; boros (<code>9.64M</code>) &#8594; <strong>CNN</strong> bawa filter geser <code>3×3</code>.",
                        "CNN dalam macet &#8594; <strong>ResNet</strong> bawa <code>Skip +x</code> &amp; <code>GAP</code> &#8594; <strong>MobileNetV2</strong> &amp; <strong>EffNet</strong> bikin ringan!",
                    ],
                    "strip_html": "<span>MLP</span><span>&#8594;</span><span>CNN</span><span>&#8594;</span><span>ResNet</span><span>&#8594;</span><strong style='color:#137333;'>MobV2</strong>",
                    "foot_cls": "blue",
                    "foot_html": "Inti: Setiap blok ada alasannya, bukan sekadar hafalan!",
                },
                {
                    "bar": "yellow",
                    "badge": "ANATOMI 5 MODEL",
                    "title": "Senjata Khas Tiap Generasi",
                    "bullets": [
                        "<strong>CNN Klasik:</strong> Parameter Sharing, Stride, Padding, MaxPool.",
                        "<strong>MobileNetV2 &amp; EffNet:</strong> Depthwise Separable (hemat 8.4×), Inverted Residual, Linear Bottleneck, &amp; SE Attention.",
                    ],
                    "strip_html": "<span>Conv2D</span><span>+</span><span>Skip</span><span>+</span><strong style='color:#B06000;'>Depthwise + SE</strong>",
                    "foot_cls": "yellow",
                    "foot_html": "Teruji: Simulasi #1 s.d. #5 langsung pada foto Elsa!",
                },
                {
                    "bar": "green",
                    "badge": "PILIHAN PROYEK → P04",
                    "title": "MobileNetV2 = CNN Utama ★",
                    "bullets": [
                        "<strong>MobileNetV2 tetap 100% CNN!</strong> CNN Klasik (<code>101.8K</code>) dipakai sebagai <em>Baseline #1 from scratch</em>, lalu <strong>MobileNetV2</strong> (<code>8.64 MB</code>, <code>6.405</code> param head) jadi model inti.",
                        "Di <strong>P04–P08</strong>: aktifkan <em>Transfer Learning 2 Tahap</em> (<code>training=False</code>) &amp; audit Grad-CAM (<code>7×7</code>), dengan <strong>EffNetB0</strong> sebagai pembanding <code>ramai</code>.",
                    ],
                    "strip_html": "<span style='color:#1A73E8;'>Baseline CNN</span><span>&#8594;</span><strong style='color:#137333;'>MobV2 (2 Tahap)</strong>",
                    "foot_cls": "green",
                    "foot_html": "Artefak: results/p03_5_architectures_benchmark.csv &amp; .png",
                },
            ],
            banner_left_html='<strong style="color:#137333;">&#10003; P03 Tuntas!</strong> &nbsp;·&nbsp; Kamus 18 Istilah: <strong style="color:#1A73E8;">Slide 43</strong> &nbsp;·&nbsp; Referensi: <strong style="color:#B06000;">Slide 51–52</strong>',
            banner_quote="&ldquo;Arsitektur terbaik bukan yang terbesar, melainkan yang pas dengan ukuran data &amp; tugasnya.&rdquo;",
            footer_label=FOOTER,
            notes="Alokasi waktu: 2 menit. Rangkum 3 pilar utama sebelum menutup sesi P03.",
        )
    )

    # S50: CLOSING (WHITE GOOGLE I/O)
    slides.append(
        make_closing_slide(
            session_id="P03",
            status_badge="&#10003; 5 Arsitektur Terbedah",
            headline_html='<span style="color:#1A73E8;">Arsitektur Neural Network</span> berevolusi agar mesin melihat lebih cerdas, <span style="color:#EA4335;">tanpa membuang memori</span> — siap menuju <span style="color:#137333;">MobileNetV2</span>!',
            subtext_html='Terima kasih sudah mengikuti sesi <strong style="color:#202124;">P03 — Arsitektur Neural Network</strong>. Sampai jumpa di <strong style="color:#137333;">P04 — Arsitektur CNN &amp; Transfer Learning</strong>!',
            footer_label=FOOTER,
            notes="Alokasi waktu: 1 menit. Tutup sesi P03 dengan apresiasi dan pratinjau P04 (Transfer Learning pada MobileNetV2).",
        )
    )

    # S51–S52: 2 SLIDE REFERENSI MATERI (0 MENIT) — hanya tautan dari docs/PLAN.md (+ label [CEK LINK] bila belum diverifikasi)
    slides.append(
        make_references_slide(
            kicker="REFERENSI MATERI · BAGIAN 1 (MLP, CNN KLASIK &amp; RESNET)",
            title_html='Referensi Materi: <span class="hl-blue">Fondasi MLP, Konvolusi &amp; ResNet</span>',
            cards=[
                {
                    "num": 1,
                    "title": "3Blue1Brown — But what is a Neural Network?",
                    "url": "https://www.youtube.com/watch?v=aircAruvnKk",
                    "tag": "Video Inti",
                    "desc": "Visualisasi terbaik membangun intuisi MLP berlapis (Hidden Layer) dari piksel angka hingga prediksi.",
                    "ctx": "Bab 1 · MLP (S06–S08)",
                    "accent": "acc-blue",
                    "featured": True,
                },
                {
                    "num": 2,
                    "title": "Coursera (DeepLearning.AI) — Foundations of CNN Week 1",
                    "url": "https://www.coursera.org/learn/convolutional-neural-networks",
                    "tag": "Kursus",
                    "desc": "Penjelasan terstruktur operasi konvolusi, deteksi tepi, Stride, Padding, dan MaxPooling pada gambar.",
                    "ctx": "Bab 2 · CNN (S11–S14)",
                    "accent": "acc-red",
                },
                {
                    "num": 3,
                    "title": "CNN Explainer (Interactive Browser Tool) [CEK LINK]",
                    "url": "https://poloclub.github.io/cnn-explainer/",
                    "tag": "Interaktif",
                    "tag_cls": "code",
                    "desc": "Eksplorasi visual langsung cara kerja setiap kernel Conv2D, ReLU, MaxPooling hingga Softmax di browser.",
                    "ctx": "Bab 2 · Simulasi (S13)",
                    "accent": "acc-blue",
                },
                {
                    "num": 4,
                    "title": "Stanford CS231n — Convolutional Neural Networks Notes [CEK LINK]",
                    "url": "https://cs231n.github.io/convolutional-networks/",
                    "tag": "Catatan",
                    "tag_cls": "doc",
                    "desc": "Catatan kuliah mendalam mengenai anatomi arsitektur ConvNet, ukuran Feature Map, serta evolusi LeNet hingga ResNet.",
                    "ctx": "Bab 2–3 (S12–S18)",
                    "accent": "acc-green",
                },
                {
                    "num": 5,
                    "title": "Dumoulin &amp; Visin — A Guide to Convolution Arithmetic [CEK LINK]",
                    "url": "https://arxiv.org/abs/1603.07285",
                    "tag": "Referensi",
                    "tag_cls": "doc",
                    "desc": "Panduan visual matematis bagaimana Kernel, Stride, dan Padding mengubah dimensi Feature Map.",
                    "ctx": "Bab 2 · Rumus (S12, S15)",
                    "accent": "acc-yellow",
                    "num_cls": "yellow",
                },
                {
                    "num": 6,
                    "title": "He dkk. — Deep Residual Learning (Paper ResNet) [CEK LINK]",
                    "url": "https://arxiv.org/abs/1512.03385",
                    "tag": "Paper ResNet",
                    "tag_cls": "must",
                    "desc": "Paper asli yang memperkenalkan Skip Connection (F(x) + x) untuk memecahkan masalah degradasi jaringan dalam.",
                    "ctx": "Bab 3 · ResNet (S17–S20)",
                    "accent": "acc-yellow",
                    "num_cls": "yellow",
                },
            ],
            route_title="📚 Peta Bacaan Bagian 1 (Bab 1–3)",
            route_steps=[
                ("#1A73E8", "MLP (#1):", "Mantapkan intuisi Hidden Layer non-linear sebelum masuk Conv2D."),
                ("#C5221F", "CNN (#2, #3, #4, #5):", "Coba klik filter interaktif di CNN Explainer agar rumus Feature Map makin menempel."),
                ("#B06000", "ResNet (#4, #6):", "Lihat grafik error Plain Net vs ResNet sebagai bukti empiris Skip Connection."),
            ],
            footer_label=FOOTER,
            notes="Alokasi waktu: 0 menit. Referensi bacaan opsional Bagian 1 sesuai docs/PLAN.md.",
            data_title="Referensi Materi (1/2) — MLP, CNN & ResNet",
        )
    )

    slides.append(
        make_references_slide(
            kicker="REFERENSI MATERI · BAGIAN 2 (MOBILENETV2, EFFICIENTNET &amp; KERAS)",
            title_html='Referensi Materi: <span class="hl-green">MobileNetV2, EfficientNet &amp; Praktik Keras</span>',
            cards=[
                {
                    "num": 7,
                    "title": "Sandler dkk. — MobileNetV2: Inverted Residuals (CVPR)",
                    "url": "https://arxiv.org/abs/1801.04381",
                    "tag": "Paper Utama",
                    "tag_cls": "must",
                    "desc": "Paper resmi MobileNetV2 yang merancang Inverted Residual &amp; Linear Bottleneck untuk perangkat hemat daya.",
                    "ctx": "Bab 4 · MobileNetV2 (S23–S26)",
                    "accent": "acc-green",
                    "num_cls": "green",
                    "featured": True,
                },
                {
                    "num": 8,
                    "title": "Tutorial TensorFlow — Transfer Learning &amp; MobileNetV2 (ID)",
                    "url": "https://www.tensorflow.org/tutorials/images/transfer_learning?hl=id",
                    "tag": "Tutorial ID",
                    "tag_cls": "code",
                    "desc": "Panduan praktis berbahasa Indonesia memuat MobileNetV2 di Keras serta langkah berikutnya menuju P04.",
                    "ctx": "Jembatan P03 &#8594; P04",
                    "accent": "acc-green",
                    "num_cls": "green",
                },
                {
                    "num": 9,
                    "title": "Roboflow — How to Train MobileNetV2 on a Custom Dataset",
                    "url": "https://roboflow.com/blog/how-to-train-mobilenetv2-on-a-custom-dataset",
                    "tag": "Panduan Praktik",
                    "desc": "Alur nyata menyiapkan dataset foto kustom untuk MobileNetV2 hingga perbandingan efisiensi model.",
                    "ctx": "Proyek Frozen P03–P08",
                    "accent": "acc-blue",
                },
                {
                    "num": 10,
                    "title": "Keras Guides — Functional API &amp; Pretrained Applications [CEK LINK]",
                    "url": "https://keras.io/guides/",
                    "tag": "Dokumentasi",
                    "tag_cls": "doc",
                    "desc": "Rujukan resmi menulis model bercabang (Add Skip Connection pada Mini-ResNet) serta memuat ResNet50 / EfficientNetB0.",
                    "ctx": "Hands-On Langkah 4–5",
                    "accent": "acc-blue",
                },
                {
                    "num": 11,
                    "title": "Google Machine Learning Crash Course — Neural Nets [CEK LINK]",
                    "url": "https://developers.google.com/machine-learning/crash-course",
                    "tag": "Referensi",
                    "tag_cls": "doc",
                    "desc": "Penguatan konsep arsitektur jaringan saraf, regularisasi, dan komparasi kapasitas model untuk pemula.",
                    "ctx": "Bab 1 &amp; 4",
                    "accent": "acc-yellow",
                    "num_cls": "yellow",
                },
                {
                    "num": 12,
                    "title": "Yosinski dkk. — How Transferable are Features in DNN? [CEK LINK]",
                    "url": "https://arxiv.org/abs/1411.1792",
                    "tag": "Jembatan P04",
                    "tag_cls": "doc",
                    "desc": "Menjelaskan mengapa layer awal CNN (pendeteksi tepi &amp; warna) bersifat umum dan bisa diwariskan antar dataset!",
                    "ctx": "Persiapan P04",
                    "accent": "acc-red",
                    "num_cls": "red",
                },
            ],
            route_title="📚 Peta Bacaan Bagian 2 &amp; Persiapan P04",
            route_steps=[
                ("#137333", "MobileNetV2 (#7, #8):", "Pahami blok Inverted Residual sebagai bekal langsung sesi P04."),
                ("#1A73E8", "Keras Code (#10):", "Cek dokumentasi Keras Applications bila ingin mencoba varian B0..B7 atau ResNet."),
                ("#C5221F", "Jembatan P04 (#8, #12):", "Pelajari sekilas mengapa bobot tepi ImageNet membantu foto Disney Frozen kita!"),
            ],
            footer_label=FOOTER,
            notes="Alokasi waktu: 0 menit. Referensi bacaan opsional Bagian 2 untuk MobileNetV2, EfficientNet, dan persiapan Transfer Learning P04.",
            data_title="Referensi Materi (2/2) — MobileNetV2 & EfficientNet",
        )
    )

    return "\n".join(slides)


def build_extra_js(data: dict) -> str:
    elsa_16_json = json.dumps(data["elsa_16_gray"])
    r_mob = _bench_dict(data)["4. MobileNetV2"]
    r_eff = _bench_dict(data)["5. EfficientNetB0"]

    return f"""
    const P03_ELSA_16 = {elsa_16_json};

    // =========================================================================
    // SIMULATOR #1 (Slide 08): MLP Dense Flow & Tes Geser 2 Piksel
    // =========================================================================
    function setMlpSim(mode) {{
      document.querySelectorAll('#sim-mlp-bar .btn-ui').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.mlp !== mode);
      }});
      const svg = document.getElementById('mlp-sim-svg');
      const kParam = document.getElementById('mlp-kpi-param');
      const kPred = document.getElementById('mlp-kpi-pred');
      const ttl = document.getElementById('mlp-vis-ttl');
      const badge = document.getElementById('mlp-vis-badge');
      const callout = document.getElementById('mlp-sim-callout');
      const s1 = document.getElementById('mlp-stage-1');
      const s2 = document.getElementById('mlp-stage-2');
      const s3 = document.getElementById('mlp-stage-3');
      const d1 = document.getElementById('mlp-st1-desc');
      const d2 = document.getElementById('mlp-st2-desc');
      const d3 = document.getElementById('mlp-st3-desc');
      [s1, s2, s3].forEach((el) => el && el.classList.remove('sync-on', 'sync-blue', 'sync-red', 'sync-green'));
      if (!svg) return;

      const isShift = mode === '64_shift';
      const isH4 = mode === '4_norm';
      if (isShift) {{
        s1 && s1.classList.add('sync-on', 'sync-red');
        s3 && s3.classList.add('sync-on', 'sync-red');
      }} else {{
        s2 && s2.classList.add('sync-on', 'sync-blue');
      }}

      if (d1) d1.innerHTML = isShift
        ? 'Koordinat piksel Elsa bergeser +2px ke kanan; kabel indeks lama kini menerima <strong>warna latar polos</strong>!'
        : 'Foto <code>224×224×3</code> diratakan menjadi <code>150.528</code> input tetap berdasarkan nomor koordinat.';
      if (d2) d2.innerHTML = isH4
        ? '<strong>Hidden 4 neuron:</strong> butuh ~<code>602.137</code> bobot — lebih ringan tapi masih mudah kurang daya ingat.'
        : '<strong>Hidden 64 &#8594; 32 neuron:</strong> memakan total <code>9.636.101</code> bobot karena setiap neuron menyambung semua piksel.';
      if (d3) d3.innerHTML = isShift
        ? 'Skor keyakinan Elsa jatuh dari <code>82% &#8594; 29%</code> (kalah oleh Olaf <code>36%</code> &amp; Anna <code>35%</code>)!'
        : (isH4 ? 'Skor keyakinan Elsa baru <code>61%</code> dengan kapasitas hidden 4.' : 'Skor Elsa <code>82%</code> hanya selama posisi figurin tepat di tengah bingkai!');

      if (kParam) kParam.textContent = isH4 ? 'Param (224×224): ~602K' : 'Param: 9.636.101';
      if (kPred) kPred.textContent = isShift ? 'Elsa: 29% (Meleset!)' : (isH4 ? 'Elsa: 61%' : 'Elsa: 82%');
      if (ttl) ttl.textContent = isShift ? 'Posisi Foto Elsa Digeser 2 Piksel ke Kanan!' : 'Posisi Foto Elsa Normal → Terbaca di Kabel Tetap';
      if (badge) {{
        badge.textContent = isShift ? 'Posisi Bergeser!' : 'Posisi Tepat';
        badge.className = 'pill ' + (isShift ? 'red' : 'blue');
      }}
      if (callout) {{
        callout.innerHTML = isShift
          ? '<strong>Spatial Blindness Terbukti!</strong> Gaun biru berpindah ke indeks piksel tetangga; kabel bobot lama salah mengira latar sebagai objek!'
          : (isH4
              ? '<strong>Hidden 4:</strong> Kapasitas lebih hemat, tetapi setiap neuron tetap harus membaca seluruh 150.528 piksel.'
              : '<strong>Hidden 64:</strong> Mencapai <strong>9.636.101 parameter</strong> hanya dari 2 Hidden Dense, namun tetap terpaku pada koordinat tetap!');
      }}

      const shiftPx = isShift ? 18 : 0;
      const hiddenCount = isH4 ? 3 : 5;
      let lines = '';
      for (let i = 0; i < 4; i++) {{
        const iy = 42 + i * 44;
        for (let h = 0; h < hiddenCount; h++) {{
          const hy = hiddenCount === 3 ? 58 + h * 54 : 36 + h * 38;
          const stroke = isShift ? '#F6AEA9' : '#C6DAFC';
          lines += `<line x1="112" y1="${{iy}}" x2="225" y2="${{hy}}" stroke="${{stroke}}" stroke-width="1.3"/>`;
        }}
      }}
      for (let h = 0; h < hiddenCount; h++) {{
        const hy = hiddenCount === 3 ? 58 + h * 54 : 36 + h * 38;
        [68, 112, 156].forEach((oy, idx) => {{
          lines += `<line x1="255" y1="${{hy}}" x2="345" y2="${{oy}}" stroke="${{idx === 1 && !isShift ? '#34A853' : '#DADCE0'}}" stroke-width="1.4"/>`;
        }});
      }}
      let hNodes = '';
      for (let h = 0; h < hiddenCount; h++) {{
        const hy = hiddenCount === 3 ? 58 + h * 54 : 36 + h * 38;
        hNodes += `<circle cx="240" cy="${{hy}}" r="13" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/><text x="240" y="${{hy + 4}}" text-anchor="middle" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#1A73E8">H${{h + 1}}</text>`;
      }}
      svg.innerHTML = `
        <rect x="8" y="16" width="84" height="186" rx="10" fill="#F8F9FA" stroke="#DADCE0" stroke-width="1.4"/>
        <rect x="24" y="60" width="34" height="94" rx="7" fill="none" stroke="#9AA0A6" stroke-width="1.4" stroke-dasharray="3,2"/>
        <rect x="${{24 + shiftPx}}" y="60" width="34" height="94" rx="7" fill="${{isShift ? '#FCE8E6' : '#4285F4'}}" stroke="${{isShift ? '#EA4335' : '#1A73E8'}}" stroke-width="1.8" opacity="0.9"/>
        <text x="${{41 + shiftPx}}" y="110" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="${{isShift ? '#C5221F' : '#FFFFFF'}}">Elsa</text>
        <text x="50" y="34" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#202124">Input 2D</text>
        <text x="50" y="192" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="${{isShift ? '#C5221F' : '#1A73E8'}}">${{isShift ? 'Bergeser +2px!' : 'Slot Tetap ✓'}}</text>
        ${{lines}}
        <circle cx="112" cy="42" r="9" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.8"/>
        <circle cx="112" cy="86" r="9" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.8"/>
        <circle cx="112" cy="130" r="9" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.8"/>
        <circle cx="112" cy="174" r="9" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.8"/>
        ${{hNodes}}
        <rect x="345" y="54" width="76" height="28" rx="7" fill="#FFFFFF" stroke="#DADCE0"/><text x="383" y="72" text-anchor="middle" font-family="Poppins" font-size="9.5" fill="#5F6368">Anna ${{isShift ? '35%' : '8%'}}</text>
        <rect x="345" y="98" width="76" height="28" rx="7" fill="${{isShift ? '#FCE8E6' : '#E6F4EA'}}" stroke="${{isShift ? '#EA4335' : '#34A853'}}" stroke-width="2"/><text x="383" y="116" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="${{isShift ? '#C5221F' : '#137333'}}">Elsa ${{isShift ? '29%' : (isH4 ? '61%' : '82%')}}</text>
        <rect x="345" y="142" width="76" height="28" rx="7" fill="#FFFFFF" stroke="#DADCE0"/><text x="383" y="160" text-anchor="middle" font-family="Poppins" font-size="9.5" fill="#5F6368">Olaf ${{isShift ? '36%' : '10%'}}</text>
      `;
    }}

    // =========================================================================
    // SIMULATOR #2 (Slide 13): CNN Klasik (Real Elsa 16x16 + Kernel/Stride/Pad)
    // =========================================================================
    const cnnState = {{ filter: 'sobel_v', stride: 1, pad: 0 }};
    const CNN_KERNELS = {{
      sobel_v: [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
      sobel_h: [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
      sharp:   [[0, -1, 0], [-1, 5, -1], [0, -1, 0]],
    }};

    function drawMatrixCanvas(canvasId, mat, modeColor) {{
      const cv = document.getElementById(canvasId);
      if (!cv || !mat.length) return;
      const ctx = cv.getContext('2d');
      const h = mat.length, w = mat[0].length;
      const cw = cv.width, ch = cv.height;
      ctx.clearRect(0, 0, cw, ch);
      let maxV = 0.001;
      for (let r = 0; r < h; r++) for (let c = 0; c < w; c++) maxV = Math.max(maxV, mat[r][c]);
      const cellW = cw / w, cellH = ch / h;
      for (let r = 0; r < h; r++) {{
        for (let c = 0; c < w; c++) {{
          const norm = Math.max(0, Math.min(1, modeColor === 'gray' ? mat[r][c] : mat[r][c] / maxV));
          if (modeColor === 'gray') {{
            const v = Math.round(norm * 255);
            ctx.fillStyle = `rgb(${{v}},${{v}},${{v}})`;
          }} else if (modeColor === 'blue') {{
            const rC = Math.round(255 - norm * 220);
            const gC = Math.round(255 - norm * 145);
            const bC = Math.round(255 - norm * 10);
            ctx.fillStyle = `rgb(${{rC}},${{gC}},${{bC}})`;
          }} else {{
            const rC = Math.round(255 - norm * 205);
            const gC = Math.round(255 - norm * 85);
            const bC = Math.round(255 - norm * 185);
            ctx.fillStyle = `rgb(${{rC}},${{gC}},${{bC}})`;
          }}
          ctx.fillRect(Math.floor(c * cellW), Math.floor(r * cellH), Math.ceil(cellW), Math.ceil(cellH));
        }}
      }}
    }}

    function renderCnnSim() {{
      document.querySelectorAll('#sim-cnn-bar [data-cnn-f]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.cnnF !== cnnState.filter);
      }});
      const bStr = document.getElementById('cnn-btn-stride');
      const bPad = document.getElementById('cnn-btn-pad');
      if (bStr) {{ bStr.textContent = 'Stride: ' + cnnState.stride; bStr.classList.toggle('outline', cnnState.stride === 1); }}
      if (bPad) {{ bPad.textContent = cnnState.pad === 1 ? 'Padding: Same (1)' : 'Padding: Valid (0)'; bPad.classList.toggle('outline', cnnState.pad === 0); }}

      const pad = cnnState.pad, stride = cnnState.stride;
      const K = CNN_KERNELS[cnnState.filter];
      const H = 16, W = 16;
      const padded = Array.from({{ length: H + 2 * pad }}, (_, r) =>
        Array.from({{ length: W + 2 * pad }}, (_, c) => {{
          const sr = r - pad, sc = c - pad;
          return (sr >= 0 && sr < H && sc >= 0 && sc < W) ? P03_ELSA_16[sr][sc] : 0;
        }})
      );
      const outN = Math.floor((H - 3 + 2 * pad) / stride) + 1;
      const fmap = [];
      for (let r = 0; r < outN; r++) {{
        const row = [];
        for (let c = 0; c < outN; c++) {{
          let s = 0;
          for (let kr = 0; kr < 3; kr++) for (let kc = 0; kc < 3; kc++) s += padded[r * stride + kr][c * stride + kc] * K[kr][kc];
          row.push(Math.max(0, s));
        }}
        fmap.push(row);
      }}
      const poolN = Math.max(1, Math.floor(outN / 2));
      const pool = [];
      for (let r = 0; r < poolN; r++) {{
        const row = [];
        for (let c = 0; c < poolN; c++) {{
          const rr = r * 2, cc = c * 2;
          row.push(Math.max(
            fmap[rr][cc],
            fmap[rr][Math.min(cc + 1, outN - 1)],
            fmap[Math.min(rr + 1, outN - 1)][cc],
            fmap[Math.min(rr + 1, outN - 1)][Math.min(cc + 1, outN - 1)]
          ));
        }}
        pool.push(row);
      }}
      drawMatrixCanvas('cnn-can-in', P03_ELSA_16, 'gray');
      drawMatrixCanvas('cnn-can-fm', fmap, 'blue');
      drawMatrixCanvas('cnn-can-pool', pool, 'green');

      const kShape = document.getElementById('cnn-kpi-shape');
      const lFm = document.getElementById('cnn-lbl-fm');
      const lPool = document.getElementById('cnn-lbl-pool');
      const kTxt = document.getElementById('cnn-kernel-txt');
      const fBox = document.getElementById('cnn-sim-formula');
      const kNames = {{
        sobel_v: 'Kernel Sobel Vertikal <code>3×3</code> + ReLU (&gt;0 menyala biru)',
        sobel_h: 'Kernel Sobel Horizontal <code>3×3</code> + ReLU (&gt;0 menyala biru)',
        sharp:   'Kernel Pertajam <code>3×3</code> + ReLU (&gt;0 menyala biru)',
      }};
      if (kShape) kShape.textContent = `Feature Map: ${{outN}}×${{outN}} → Pool: ${{poolN}}×${{poolN}}`;
      if (lFm) lFm.textContent = `${{outN}}×${{outN}} (${{outN * outN}} sel aktif)`;
      if (lPool) lPool.textContent = `${{poolN}}×${{poolN}} → ${{poolN * poolN}} ciri ke Softmax`;
      if (kTxt) kTxt.innerHTML = kNames[cnnState.filter] || '';
      if (fBox) fBox.innerHTML = `<strong>Rumus Ukuran:</strong> (16 &minus; 3 + 2×${{pad}}) / ${{stride}} + 1 = <strong>${{outN}}×${{outN}}</strong> &rarr; setelah MaxPool 2×2 menjadi <strong>${{poolN}}×${{poolN}}</strong> (hanya 10 param per filter!)`;
    }}
    function setCnnState(patch) {{ Object.assign(cnnState, patch); renderCnnSim(); }}
    function toggleCnnStride() {{ cnnState.stride = cnnState.stride === 1 ? 2 : 1; renderCnnSim(); }}
    function toggleCnnPad() {{ cnnState.pad = cnnState.pad === 0 ? 1 : 0; renderCnnSim(); }}

    // =========================================================================
    // SIMULATOR #3 (Slide 19): ResNet Signal Flow & GAP
    // =========================================================================
    function setResnetSim(mode) {{
      document.querySelectorAll('#sim-resnet-bar .btn-ui').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.res !== mode);
      }});
      const isRes = mode === 'resnet';
      const bars = document.getElementById('res-signal-bars');
      const archSvg = document.getElementById('res-arch-svg');
      const archCap = document.getElementById('res-arch-cap');
      const kGrad = document.getElementById('res-kpi-grad');
      const kHead = document.getElementById('res-kpi-head');
      const pill = document.getElementById('res-status-pill');
      const callout = document.getElementById('res-callout');
      const bDesc = document.getElementById('res-block-desc');
      const gDesc = document.getElementById('res-gap-desc');
      const sBlk = document.getElementById('res-stage-block');
      const sGap = document.getElementById('res-stage-gap');
      const blkPill = document.getElementById('res-blk-pill');
      const gapPill = document.getElementById('res-gap-pill');
      if (sBlk) {{
        sBlk.classList.toggle('sync-on', true);
        sBlk.classList.toggle('sync-green', isRes);
        sBlk.classList.toggle('sync-red', !isRes);
      }}
      if (sGap) {{
        sGap.classList.toggle('sync-on', true);
        sGap.classList.toggle('sync-green', isRes);
        sGap.classList.toggle('sync-red', !isRes);
      }}
      if (blkPill) {{
        blkPill.textContent = isRes ? 'AKTIF (+x)' : 'TANPA +x';
        blkPill.className = 'pill ' + (isRes ? 'green' : 'red');
      }}
      if (gapPill) {{
        gapPill.textContent = isRes ? 'GAP 10.245' : 'FLATTEN 51.38M';
        gapPill.className = 'pill ' + (isRes ? 'green' : 'red');
      }}

      const vals = isRes ? [100, 96, 92, 89, 86] : [100, 58, 30, 14, 7];
      const names = ['Layer 20', 'Layer 15', 'Layer 10', 'Layer 5', 'Layer 1'];
      if (bars) {{
        bars.innerHTML = vals.map((v, i) => `
          <div class="signal-bar-row">
            <span style="font-family:var(--font-code); font-weight:700; color:#3C4043;">${{names[i]}}</span>
            <div class="signal-track"><div class="signal-fill" style="width:${{v}}%; background:${{isRes ? '#34A853' : (v < 25 ? '#EA4335' : '#FBBC04')}};"></div></div>
            <span style="font-family:var(--font-code); font-weight:700; color:${{isRes ? '#137333' : '#C5221F'}};">${{v}}%</span>
          </div>
        `).join('');
      }}
      if (archCap) archCap.textContent = isRes
        ? 'Alur ResNet (+x Skip Bridge + GAP Head):'
        : 'Alur Plain Deep Net (Seri Polos + Flatten Head):';
      if (archSvg) {{
        archSvg.innerHTML = isRes ? `
          <rect x="6" y="42" width="44" height="30" rx="6" fill="#202124"/><text x="28" y="61" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#FFF">Foto x</text>
          <path d="M50,57 L74,57" stroke="#34A853" stroke-width="2"/>
          <path d="M60,57 C60,12 200,12 200,45" fill="none" stroke="#F9AB00" stroke-width="3"/>
          <rect x="92" y="7" width="84" height="16" rx="8" fill="#FEF7E0" stroke="#F9AB00"/><text x="134" y="18" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#B06000">Jalur Tol +x</text>
          <rect x="74" y="40" width="108" height="34" rx="7" fill="#E8F0FE" stroke="#4285F4"/><text x="128" y="55" text-anchor="middle" font-family="Poppins" font-size="9" font-weight="700" fill="#1A73E8">Blok F(x) 175 L</text><text x="128" y="67" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#5F6368">16 Skip Add()</text>
          <circle cx="200" cy="57" r="11" fill="#FEF7E0" stroke="#E37400" stroke-width="2"/><text x="200" y="61" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#B06000">+</text>
          <path d="M211,57 L235,57" stroke="#34A853" stroke-width="2"/>
          <rect x="235" y="40" width="88" height="34" rx="7" fill="#E6F4EA" stroke="#34A853" stroke-width="1.6"/><text x="279" y="55" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#137333">GAP 1×1</text><text x="279" y="67" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#137333">2.048 angka</text>
          <path d="M323,57 L343,57" stroke="#34A853" stroke-width="2"/>
          <rect x="343" y="40" width="81" height="34" rx="7" fill="#34A853"/><text x="383" y="55" text-anchor="middle" font-family="Poppins" font-size="9" font-weight="700" fill="#FFF">Dense(5)</text><text x="383" y="67" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#E6F4EA">10.245 param</text>
        ` : `
          <rect x="6" y="42" width="44" height="30" rx="6" fill="#202124"/><text x="28" y="61" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#FFF">Foto x</text>
          <path d="M50,57 L72,57" stroke="#EA4335" stroke-width="2"/>
          <rect x="72" y="40" width="122" height="34" rx="7" fill="#FCE8E6" stroke="#EA4335"/><text x="133" y="55" text-anchor="middle" font-family="Poppins" font-size="9" font-weight="700" fill="#C5221F">Conv Seri Tanpa +x</text><text x="133" y="67" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#C5221F">Sinyal L1 tinggal 7%</text>
          <rect x="92" y="10" width="82" height="16" rx="8" fill="#FCE8E6" stroke="#F6AEA9"/><text x="133" y="21" text-anchor="middle" font-family="Poppins" font-size="8" font-weight="700" fill="#C5221F">Tanpa Jalur Tol</text>
          <path d="M194,57 L218,57" stroke="#EA4335" stroke-width="2"/>
          <rect x="218" y="40" width="106" height="34" rx="7" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.6"/><text x="271" y="55" text-anchor="middle" font-family="Poppins" font-size="9" font-weight="700" fill="#C5221F">Flatten→Dense(512)</text><text x="271" y="67" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#C5221F">100.352 angka</text>
          <path d="M324,57 L343,57" stroke="#EA4335" stroke-width="2"/>
          <rect x="343" y="40" width="81" height="34" rx="7" fill="#EA4335"/><text x="383" y="55" text-anchor="middle" font-family="Poppins" font-size="9" font-weight="700" fill="#FFF">Dense(5)</text><text x="383" y="67" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#FCE8E6">51.38M param</text>
        `;
      }}
      if (kGrad) kGrad.textContent = isRes ? 'Sinyal di Layer 1: 86% (Kuat!)' : 'Sinyal di Layer 1: 7% (Macet)';
      if (kHead) kHead.textContent = isRes ? 'Head: GAP 10.245' : 'Head: Flatten 51.38M';
      if (pill) {{
        pill.textContent = isRes ? 'Skip + GAP Aktif ✓' : 'Vanishing Gradient!';
        pill.className = 'pill ' + (isRes ? 'green' : 'red');
      }}
      if (callout) callout.innerHTML = isRes
        ? '<strong>ResNet Berhasil!</strong> Lewat jembatan <code>+ x</code>, gradien tidak habis di tengah jalan sehingga lapisan awal tetap belajar tepi gambar Frozen dengan tajam!'
        : 'Tanpa jalur pintas, sinyal belajar yang dikirim dari Loss di Layer 20 habis terserap di tengah jalan sebelum mencapai Layer 1!';
      if (bDesc) bDesc.innerHTML = isRes
        ? 'Mode aktif: <code>Output = F(x) + x</code>! Layer cukup belajar koreksi kecil sementara data awal mengalir utuh lewat jembatan sehingga gradien Layer 1 tetap <strong>86%</strong>.'
        : 'Setiap blok saat ini hanya menyalurkan jalur utama konvolusi <code>F(x)</code> tanpa penyambung <code>+ x</code>. Saat backprop, sinyal gradien menyusut hingga tinggal <strong>7%</strong> di Layer 1.';
      if (gDesc) gDesc.innerHTML = isRes
        ? 'Di ujung ResNet50 (tensor <code>7×7×2048</code>), <strong>GAP</strong> meringkas tiap peta fitur menjadi rata-rata tunggal (<code>2.048</code> angka) sehingga parameter head turun dari <code>51,38 juta</code> ke <code>10.245</code>!'
        : 'Dengan cara lama (<code>Flatten &#8594; Dense(512)</code>), tensor <code>7×7×2048</code> diratakan menjadi <code>100.352</code> angka dan menghabiskan <code>51.380.229</code> parameter kepala!';
    }}

    // =========================================================================
    // SIMULATOR #4 (Slide 25): MobileNetV2 Conv Biasa vs Inverted Residual
    // =========================================================================
    function setMobSim(mode) {{
      document.querySelectorAll('#sim-mob-bar .btn-ui').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.mob !== mode);
      }});
      const isMob = mode === 'mobilenetv2';
      const svg = document.getElementById('mob-sim-svg');
      const kOps = document.getElementById('mob-kpi-ops');
      const kSave = document.getElementById('mob-kpi-save');
      const ttl = document.getElementById('mob-vis-ttl');
      const fBox = document.getElementById('mob-sim-formula');
      const s1 = document.getElementById('mob-stage-1');
      const s2 = document.getElementById('mob-stage-2');
      const s3 = document.getElementById('mob-stage-3');
      const p1 = document.getElementById('mob-p1');
      const p2 = document.getElementById('mob-p2');
      const p3 = document.getElementById('mob-p3');
      const d1 = document.getElementById('mob-st1-desc');
      const d2 = document.getElementById('mob-st2-desc');
      const d3 = document.getElementById('mob-st3-desc');
      [s1, s2, s3].forEach((e) => {{
        if (!e) return;
        e.classList.toggle('sync-on', true);
        e.classList.toggle('sync-green', isMob);
        e.classList.toggle('sync-red', !isMob);
      }});
      if (p1) {{ p1.textContent = isMob ? 'EXPAND 6×' : 'GABUNG PENUH'; p1.className = 'pill ' + (isMob ? 'green' : 'red'); }}
      if (p2) {{ p2.textContent = isMob ? '27.5M OPS' : '231.2M OPS'; p2.className = 'pill ' + (isMob ? 'green' : 'red'); }}
      if (p3) {{ p3.textContent = isMob ? 'LINEAR + SKIP' : 'PAKAI RELU'; p3.className = 'pill ' + (isMob ? 'green' : 'red'); }}
      if (d1) d1.innerHTML = isMob
        ? 'Kanal ramping <code>32</code> diperluas dulu menjadi <code>192</code> kanal (<code>6×</code>) via konvolusi <code>1×1</code> + <code>ReLU6</code> agar kaya pola.'
        : 'Pada mode standar tidak ada pemisahan &mdash; semua <code>64×128</code> kombinasi kanal langsung dikalikan sekaligus dengan filter 3×3!';
      if (d2) d2.innerHTML = isMob
        ? 'Memindai ruang spasial foto Frozen secara mandiri tiap kanal (<code>192</code> filter) tanpa mengaduk antarkanal (hemat ~8.4&times; hitungan!).'
        : 'Filter 3×3 mengulang pemindaian ruang sekaligus mengaduk antar-kanal dalam 1 langkah berat (<code>231.2 juta</code> perkalian per blok).';
      if (d3) d3.innerHTML = isMob
        ? 'Memeras kembali ke <code>32</code> kanal <strong>tanpa ReLU (Linear)</strong> agar angka negatif tetap utuh, lalu menyambungkan <code>Skip +x</code>!'
        : 'Output langsung dipotong ReLU dan ukuran model menjadi sangat berat bila dipakai berulang untuk perangkat seluler.';
      if (!svg) return;

      if (kOps) kOps.textContent = isMob ? 'Perkalian: 27.5 Juta' : 'Perkalian: 231.2 Juta';
      if (kSave) kSave.textContent = isMob ? 'Hemat 8.4×!' : 'Efisiensi: Baseline 1×';
      if (ttl) ttl.textContent = isMob ? 'Blok Inverted Residual: 32 → Expand 192 → DW 3×3 → Linear 32 (+Skip)' : 'Pipa Konvolusi Standar 56×56×64 → 128 Channel';
      if (fBox) fBox.innerHTML = isMob
        ? '<strong>Depthwise + Pointwise:</strong> <code>(56×56×3×3×64) + (56×56×1×1×64×128) = 27.5M ops</code> (hemat <strong>8.4×</strong>!) · Backbone Frozen: {r_mob["total_params"]:,} param.'
        : '<code>56 × 56 × 3 × 3 × 64 × 128 = 231.211.008</code> kali perkalian pada 1 blok konvolusi standar!';

      if (!isMob) {{
        svg.innerHTML = `
          <rect x="18" y="56" width="92" height="104" rx="10" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
          <text x="64" y="103" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#1A73E8">Input</text>
          <text x="64" y="122" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" fill="#174EA6">56×56×64</text>
          <line x1="110" y1="108" x2="155" y2="108" stroke="#5F6368" stroke-width="2.5"/>
          <rect x="155" y="42" width="128" height="132" rx="12" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.5"/>
          <text x="219" y="96" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#C5221F">Conv2D 3×3</text>
          <text x="219" y="114" text-anchor="middle" font-family="Roboto" font-size="10" fill="#C5221F">Gabung Spasial + Kanal</text>
          <text x="219" y="136" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#C5221F">231.2M ops!</text>
          <line x1="283" y1="108" x2="324" y2="108" stroke="#5F6368" stroke-width="2.5"/>
          <rect x="324" y="46" width="98" height="124" rx="10" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
          <text x="373" y="103" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#B06000">Output</text>
          <text x="373" y="122" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" fill="#B06000">56×56×128</text>
        `;
      }} else {{
        svg.innerHTML = `
          <path d="M 52 146 Q 220 204 388 146" fill="none" stroke="#34A853" stroke-width="2.6" stroke-dasharray="5,4"/>
          <text x="220" y="198" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#137333">Skip Connection (+x langsung antar bottleneck sempit)</text>
          <rect x="14" y="76" width="72" height="66" rx="9" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
          <text x="50" y="106" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#1A73E8">32 ch</text>
          <text x="50" y="122" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="#174EA6">Sempit</text>
          <line x1="86" y1="109" x2="108" y2="109" stroke="#3C4043" stroke-width="2"/>
          <rect x="108" y="34" width="94" height="140" rx="10" fill="#E6F4EA" stroke="#34A853" stroke-width="2.2"/>
          <text x="155" y="92" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#137333">Expand 1×1</text>
          <text x="155" y="110" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#137333">192 ch (6×)</text>
          <text x="155" y="128" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="#5F6368">+ ReLU6</text>
          <line x1="202" y1="109" x2="222" y2="109" stroke="#3C4043" stroke-width="2"/>
          <rect x="222" y="34" width="96" height="140" rx="10" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2.2"/>
          <text x="270" y="92" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#B06000">DW 3×3</text>
          <text x="270" y="110" text-anchor="middle" font-family="Roboto" font-size="9.2" fill="#B06000">1 filter / kanal</text>
          <text x="270" y="128" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="#137333">Super ringan!</text>
          <line x1="318" y1="109" x2="340" y2="109" stroke="#3C4043" stroke-width="2"/>
          <rect x="340" y="76" width="88" height="66" rx="9" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2"/>
          <text x="384" y="104" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#1A73E8">Project 32</text>
          <text x="384" y="120" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#C5221F">Linear (no ReLU)</text>
        `;
      }}
    }}

    // =========================================================================
    // SIMULATOR #5 (Slide 29): EfficientNet Compound Scaling & SE Attention
    // =========================================================================
    const effState = {{ scale: 'b0', se: false }};
    const EFF_SCALES = {{
      b0: {{ res: 224, depth: '1.0×', width: '1.0×', meta: '{r_eff["total_params"]/1e6:.2f}M Param · {r_eff["est_size_mb"]} MB' }},
      b1: {{ res: 240, depth: '1.1×', width: '1.0×', meta: '~6.5M Param · 24.8 MB' }},
      b2: {{ res: 260, depth: '1.2×', width: '1.1×', meta: '~7.8M Param · 29.8 MB' }},
    }};

    function renderEffSim() {{
      document.querySelectorAll('#sim-eff-bar [data-eff-s]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.effS !== effState.scale);
      }});
      const btnSe = document.getElementById('eff-se-btn');
      const kMeta = document.getElementById('eff-kpi-meta');
      const sePill = document.getElementById('eff-se-pill');
      const bars = document.getElementById('eff-se-bars');
      const archSvg = document.getElementById('eff-arch-svg');
      const callout = document.getElementById('eff-callout');
      const scDesc = document.getElementById('eff-scale-desc');
      const seDesc = document.getElementById('eff-se-desc');
      const sSc = document.getElementById('eff-stage-scale');
      const sSe = document.getElementById('eff-stage-se');
      const p1 = document.getElementById('eff-p1');
      const p2 = document.getElementById('eff-p2');
      const sp = EFF_SCALES[effState.scale];
      if (btnSe) {{
        btnSe.textContent = effState.se ? 'SE Attention: ON ✓' : 'SE Attention: OFF';
        btnSe.classList.toggle('outline', !effState.se);
      }}
      if (sSc) {{
        sSc.classList.toggle('sync-on', true);
        sSc.classList.toggle('sync-green', effState.scale !== 'b0');
        sSc.classList.toggle('sync-blue', effState.scale === 'b0');
      }}
      if (sSe) {{
        sSe.classList.toggle('sync-on', true);
        sSe.classList.toggle('sync-green', effState.se);
        sSe.classList.toggle('sync-red', !effState.se);
      }}
      if (p1) {{
        p1.textContent = effState.scale.toUpperCase() + (effState.scale === 'b0' ? ' · BASELINE' : ' · SCALED');
        p1.className = 'pill ' + (effState.scale === 'b0' ? 'blue' : 'green');
      }}
      if (p2) {{
        p2.textContent = effState.se ? 'SE ON ✓' : 'SE OFF';
        p2.className = 'pill ' + (effState.se ? 'green' : 'red');
      }}

      if (kMeta) kMeta.textContent = sp.meta;
      if (scDesc) scDesc.innerHTML = `Skala <code>${{effState.scale.toUpperCase()}}</code>: resolusi <code>${{sp.res}}×${{sp.res}}</code>, depth <code>${{sp.depth}}</code>, width <code>${{sp.width}}</code> &#8594; <code>${{sp.meta}}</code>.`;
      if (sePill) {{
        sePill.textContent = effState.se ? 'SE ON (Fokus Karakter!)' : 'SE OFF (Bobot Rata)';
        sePill.style.background = effState.se ? '#E6F4EA' : '#F1F3F4';
        sePill.style.color = effState.se ? '#137333' : '#5F6368';
      }}
      const chs = effState.se
        ? [
            ['Gaun Biru Elsa', 95, '#1A73E8'],
            ['Siluet Tubuh & Mahkota', 88, '#34A853'],
            ['Cangkir Latar (Ramai)', 16, '#EA4335'],
            ['Dinding & Rak Belakang', 10, '#9AA0A6'],
          ]
        : [
            ['Gaun Biru Elsa', 55, '#4285F4'],
            ['Siluet Tubuh & Mahkota', 55, '#4285F4'],
            ['Cangkir Latar (Ramai)', 55, '#FBBC04'],
            ['Dinding & Rak Belakang', 55, '#9AA0A6'],
          ];
      if (bars) {{
        bars.innerHTML = chs.map(([nm, w, col]) => `
          <div style="display:flex; flex-direction:column; gap:3px;">
            <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:600;"><span>${{nm}}</span><span style="font-family:var(--font-code);">${{(w/100).toFixed(2)}}</span></div>
            <div class="signal-track"><div class="signal-fill" style="width:${{w}}%; background:${{col}};"></div></div>
          </div>
        `).join('');
      }}
      if (archSvg) {{
        const boxW = effState.scale === 'b0' ? 68 : (effState.scale === 'b1' ? 76 : 84);
        const seCol = effState.se ? '#34A853' : '#EA4335';
        const seBg = effState.se ? '#E6F4EA' : '#FCE8E6';
        archSvg.innerHTML = `
          <rect x="8" y="${{41 - (boxW-28)/2}}" width="${{boxW}}" height="${{boxW-28}}" rx="6" fill="#F3E8FD" stroke="#8E24AA" stroke-width="1.8"/>
          <text x="${{8 + boxW/2}}" y="38" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#681DA8">${{effState.scale.toUpperCase()}} Input</text>
          <text x="${{8 + boxW/2}}" y="51" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="#5F6368">${{sp.res}}×${{sp.res}}</text>
          <text x="${{boxW + 22}}" y="45" text-anchor="middle" font-family="Poppins" font-size="13" fill="#5F6368">&#8594;</text>
          <rect x="${{boxW + 34}}" y="18" width="114" height="46" rx="7" fill="#E8F0FE" stroke="#4285F4"/>
          <text x="${{boxW + 91}}" y="37" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#1A73E8">Blok MBConv</text>
          <text x="${{boxW + 91}}" y="51" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#174EA6">D:${{sp.depth}} · W:${{sp.width}}</text>
          <text x="${{boxW + 160}}" y="45" text-anchor="middle" font-family="Poppins" font-size="13" fill="${{seCol}}">&#8594;</text>
          <rect x="${{boxW + 172}}" y="14" width="154" height="54" rx="8" fill="${{seBg}}" stroke="${{seCol}}" stroke-width="1.8"/>
          <text x="${{boxW + 249}}" y="34" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="${{seCol}}">SE Gate ${{effState.se ? 'AKTIF' : 'OFF'}}</text>
          <text x="${{boxW + 249}}" y="49" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="${{seCol}}">${{effState.se ? 'Elsa ×0.95 | Latar ×0.16' : 'Semua bobot rata 0.55'}}</text>
        `;
      }}
      if (callout) callout.innerHTML = effState.se
        ? '<strong>SE Attention Aktif ({r_eff["se_multiply_layers"]} blok)!</strong> Jaringan meredam bobot kanal latar ramai ke <code>0.10–0.16</code> dan membesarkan ciri Elsa menjadi <code>0.88–0.95</code>.'
        : 'Tanpa SE Attention, semua kanal (termasuk latar dinding dan cangkir di belakang Elsa) mendapat bobot setara.';
      if (seDesc) seDesc.innerHTML = effState.se
        ? '<code>Output = Channel × Bobot_SE</code> sudah aktif &mdash; fitur gaun Elsa dikuatkan, latar ramai diredam!'
        : 'Klik tombol <strong>SE Attention: ON</strong> di atas untuk melihat bobot kanal latar diredam otomatis agar fokus ke gaun biru Elsa!';
    }}
    function setEffState(patch) {{ Object.assign(effState, patch); renderEffSim(); }}
    function toggleEffSe() {{ effState.se = !effState.se; renderEffSim(); }}

    // Initial render
    setMlpSim('64_norm');
    renderCnnSim();
    setResnetSim('plain');
    setMobSim('standard');
    renderEffSim();

    // =========================================================================
    // PDF / PPTX DETERMINISTIC STATE EXPANDER (2 states per simulator)
    // =========================================================================
    window.SLIDE_PDF_EXPANDERS = window.SLIDE_PDF_EXPANDERS || [];
    window.SLIDE_PDF_EXPANDERS.push(({{ cloneSlideWithCanvases }}) => {{
      const expandBar = (barId, states, applyFn, prefix) => {{
        const host = document.getElementById(barId);
        if (!host) return;
        const slide = host.closest('section.slide');
        if (!slide) return;
        const clones = states.map((st) => {{
          applyFn(st);
          return cloneSlideWithCanvases(slide, prefix + '-' + JSON.stringify(st));
        }});
        clones.forEach((c) => slide.parentNode.insertBefore(c, slide));
        slide.remove();
      }};

      expandBar('sim-mlp-bar', ['64_norm', '64_shift'], setMlpSim, 'mlp');
      expandBar('sim-cnn-bar', [
        {{ filter: 'sobel_v', stride: 1, pad: 0 }},
        {{ filter: 'sobel_v', stride: 2, pad: 1 }},
      ], setCnnState, 'cnn');
      expandBar('sim-resnet-bar', ['plain', 'resnet'], setResnetSim, 'res');
      expandBar('sim-mob-bar', ['standard', 'mobilenetv2'], setMobSim, 'mob');
      expandBar('sim-eff-bar', [
        {{ scale: 'b0', se: false }},
        {{ scale: 'b2', se: true }},
      ], setEffState, 'eff');
    }});
"""


def main() -> None:
    data_path = ASSETS_DIR / "p03_data.json"
    if not data_path.exists():
        raise FileNotFoundError(f"Jalankan build_assets.py dulu: {data_path} tidak ditemukan.")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    slides_html = build_slides_html(data)
    extra_js = build_extra_js(data)
    out_path, total = write_deck_html(
        SESSION,
        slides_html,
        extra_css=EXTRA_CSS,
        extra_js=extra_js,
    )
    print(f"✅ HTML interaktif P03 ({total} slide) berhasil dibuat: {out_path}")


if __name__ == "__main__":
    main()
