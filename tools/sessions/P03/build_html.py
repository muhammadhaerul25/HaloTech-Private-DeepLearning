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

    /* Slide 12: Continuous 60fps CSS Loop Animations for CNN Mechanics */
    @keyframes kSlideLoop {
      0%, 20%   { transform: translate(0px, 0px); }
      25%, 45%  { transform: translate(22px, 0px); }
      50%, 70%  { transform: translate(0px, 22px); }
      75%, 95%  { transform: translate(22px, 22px); }
      100%      { transform: translate(0px, 0px); }
    }
    @keyframes kCellGlow1 { 0%, 20% { opacity: 1; } 25%, 95% { opacity: 0.28; } 100% { opacity: 1; } }
    @keyframes kCellGlow2 { 0%, 20% { opacity: 0.28; } 25%, 45% { opacity: 1; } 50%, 100% { opacity: 0.28; } }
    @keyframes kCellGlow3 { 0%, 45% { opacity: 0.28; } 50%, 70% { opacity: 1; } 75%, 100% { opacity: 0.28; } }
    @keyframes kCellGlow4 { 0%, 70% { opacity: 0.28; } 75%, 95% { opacity: 1; } 100% { opacity: 0.28; } }
    @keyframes s1StepLoop {
      0%, 20%   { transform: translateX(0px); }
      25%, 45%  { transform: translateX(13px); }
      50%, 70%  { transform: translateX(26px); }
      75%, 95%  { transform: translateX(39px); }
      100%      { transform: translateX(0px); }
    }
    @keyframes s2JumpLoop {
      0%, 28%   { transform: translateX(0px); }
      35%, 63%  { transform: translateX(26px); }
      70%, 95%  { transform: translateX(52px); }
      100%      { transform: translateX(0px); }
    }
    @keyframes padPulseLoop { 0%, 100% { opacity: 0.45; } 50% { opacity: 1; } }
    @keyframes rfBox1 { 0%, 30% { opacity: 1; transform: scale(1.04); } 36%, 100% { opacity: 0.45; transform: scale(1); } }
    @keyframes rfBox2 { 0%, 32% { opacity: 0.45; transform: scale(1); } 36%, 64% { opacity: 1; transform: scale(1.04); } 70%, 100% { opacity: 0.45; transform: scale(1); } }
    @keyframes rfBox3 { 0%, 66% { opacity: 0.45; transform: scale(1); } 70%, 96% { opacity: 1; transform: scale(1.04); } 100% { opacity: 0.45; transform: scale(1); } }
    .s12c-kern { animation: kSlideLoop 4.2s ease-in-out infinite; }
    @keyframes elsaScanLoop {
      0%, 20%   { transform: translate(6px, 8px); }
      25%, 45%  { transform: translate(34px, 12px); }
      50%, 70%  { transform: translate(12px, 38px); }
      75%, 95%  { transform: translate(36px, 40px); }
      100%      { transform: translate(6px, 8px); }
    }
    @keyframes pxTransferFly {
      0%   { transform: translateX(0px) scale(0.75); opacity: 0; }
      20%  { opacity: 1; transform: translateX(8px) scale(1.1); }
      80%  { opacity: 1; transform: translateX(46px) scale(1.1); }
      100% { transform: translateX(54px) scale(0.75); opacity: 0; }
    }
    .s12c-elsa-scan { animation: elsaScanLoop 4.2s ease-in-out infinite; }
    .s12c-px-fly { animation: pxTransferFly 1.05s linear infinite; }
    .s12c-fm1 { animation: kCellGlow1 4.2s ease-in-out infinite; }
    .s12c-fm2 { animation: kCellGlow2 4.2s ease-in-out infinite; }
    .s12c-fm3 { animation: kCellGlow3 4.2s ease-in-out infinite; }
    .s12c-fm4 { animation: kCellGlow4 4.2s ease-in-out infinite; }
    .s12c-s1 { animation: s1StepLoop 3.6s ease-in-out infinite; }
    .s12c-s2 { animation: s2JumpLoop 3.6s ease-in-out infinite; }
    .s12c-pad { animation: padPulseLoop 2.2s ease-in-out infinite; }
    .s12c-rf1 { animation: rfBox1 3.9s ease-in-out infinite; transform-origin: center; }
    .s12c-rf2 { animation: rfBox2 3.9s ease-in-out infinite; transform-origin: center; }
    .s12c-rf3 { animation: rfBox3 3.9s ease-in-out infinite; transform-origin: center; }

    .sim-ctrl-sep { width: 1.5px; height: 22px; background: #DADCE0; margin: 0 2px; flex-shrink: 0; }
    .btn-ui.play-btn { background: #1E8E3E; color: #FFFFFF; border-color: #1E8E3E; }
    .btn-ui.play-btn.playing { background: #C5221F; border-color: #C5221F; color: #FFFFFF; }
    .signal-bar-row { padding: 3px 6px; border-radius: 8px; border: 1.5px solid transparent; transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease; }
    .signal-bar-row.bar-active { background: #FFF8E1; border-color: #FBBC04; transform: translateX(3px); }
    @media print {
      .ambient-pulse, .s12c-kern, .s12c-elsa-scan, .s12c-px-fly, .s12c-s1, .s12c-s2, .s12c-pad,
      .s12c-fm1, .s12c-fm2, .s12c-fm3, .s12c-fm4,
      .s12c-rf1, .s12c-rf2, .s12c-rf3 {
        animation: none !important; opacity: 1 !important; transform: none !important;
      }
      .s12c-elsa-scan { transform: translate(22px, 22px) !important; }
      .s12c-px-fly { display: none !important; }
      .sync-card.sync-dim { opacity: 1 !important; transform: none !important; }
      .sim-ctrl-sep { display: none !important; }
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
    # S03: PEMANASAN — TITIK MENTOK MODEL 1-LAYER P02 (SEDERHANA & VISUAL)
    # ------------------------------------------------------------------
    slides.append(f"""
    <section class="slide" data-title="Pemanasan — Kenapa Model P02 Belum Cukup" data-notes="Alokasi waktu: 2 menit. Recap P02 dengan bahasa sederhana: model 1-layer P02 meluruskan piksel jadi 1 baris sehingga rentan saat figurin bergeser posisi, boros kabel jika diperdalam, dan mudah tertipu latar ramai.">
      <div class="kicker">PEMANASAN · MENYAMBUNG P02 KE P03</div>
      <h2>Kenapa Model 1-Layer P02 <span class="hl-red">Belum Cukup</span> untuk Foto Frozen?</h2>
      <div class="split-60-40" style="grid-template-columns:1.05fr 0.95fr; flex:1; min-height:0; align-items:stretch;">
        <div style="display:flex; flex-direction:column; gap:10px; min-height:0;">
          <div class="card" style="flex:1; padding:13px 15px; display:flex; flex-direction:column; justify-content:space-between; gap:10px; min-height:0;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="font-family:var(--font-title); font-size:13px; color:#202124;">2 Tantangan Nyata di Foto Proyek Kita</strong>
              <span class="pill blue" style="font-size:9.8px; padding:2px 9px;">Dataset Asli Frozen</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; flex:1; min-height:0;">
              <div style="background:#FFF8F7; border:1.5px solid #F6AEA9; border-radius:12px; padding:9px; display:flex; flex-direction:column; gap:8px; min-height:0;">
                <div style="position:relative; flex:1; min-height:155px; background:#FFFFFF; border-radius:9px; border:1px solid #FAD2CF; overflow:hidden; display:flex; align-items:center; justify-content:center;">
                  <img src="assets/P03/thumb_elsa.jpg" alt="Elsa Bergeser" style="height:100%; width:84%; object-fit:cover; transform:translateX(14px); border-left:2.5px dashed #EA4335;"/>
                  <span style="position:absolute; top:6px; left:6px; background:#EA4335; color:#FFF; font-family:var(--font-title); font-size:9px; font-weight:700; padding:2px 7px; border-radius:999px;">Geser Sedikit &#8594;</span>
                </div>
                <div style="font-size:11.6px; color:#3C4043; line-height:1.38; flex-shrink:0;">
                  <strong style="color:#C5221F;">A. Posisi Elsa Bergeser:</strong><br/>Model P02 menghafal letak piksel kaku — geser sedikit saja, ia mengira objek lain!
                </div>
              </div>
              <div style="background:#FFFDF5; border:1.5px solid #FDE293; border-radius:12px; padding:9px; display:flex; flex-direction:column; gap:8px; min-height:0;">
                <div style="position:relative; flex:1; min-height:155px; background:#FFFFFF; border-radius:9px; border:1px solid #FDE293; overflow:hidden;">
                  <img src="assets/P03/thumb_elsa_ramai.jpg" alt="Elsa Latar Ramai" style="width:100%; height:100%; object-fit:cover; display:block;"/>
                  <span style="position:absolute; top:6px; left:6px; background:#FBBC04; color:#202124; font-family:var(--font-title); font-size:9px; font-weight:700; padding:2px 7px; border-radius:999px;">Banyak Benda Lain</span>
                </div>
                <div style="font-size:11.6px; color:#3C4043; line-height:1.38; flex-shrink:0;">
                  <strong style="color:#B06000;">B. Latar Belakang Ramai:</strong><br/>Ada rak &amp; warna benda lain di belakang Elsa. Model 1 lapis mudah terkecoh latar!
                </div>
              </div>
            </div>
            <div style="background:#F8F9FA; border:1px solid #E0E3E7; border-radius:9px; padding:7px 11px; font-size:11.6px; color:#3C4043; text-align:center;">
              <strong style="color:#202124;">Intinya:</strong> Model polos P02 hanya bisa menebak <em>warna di kotak yang sama</em>, belum paham <strong>bentuk objek</strong>.
            </div>
          </div>

          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;">
            <div class="mini-box" style="text-align:center; padding:8px 6px;"><div style="font-family:var(--font-title); font-size:15px; font-weight:800; color:#1A73E8;">{tot_imgs} Foto</div><div style="font-size:10px; color:#5F6368;">{n_polos} Polos · {n_ramai} Ramai</div></div>
            <div class="mini-box" style="text-align:center; padding:8px 6px;"><div style="font-family:var(--font-title); font-size:15px; font-weight:800; color:#B06000;">{p02_p:,} Kabel</div><div style="font-size:10px; color:#5F6368;">Berat Model 1-Layer P02</div></div>
            <div class="mini-box" style="text-align:center; padding:8px 6px;"><div style="font-family:var(--font-title); font-size:15px; font-weight:800; color:#137333;">5 Karakter</div><div style="font-size:10px; color:#5F6368;">Anna s.d. Sven</div></div>
          </div>
        </div>

        <div class="card surface" style="justify-content:space-between; padding:15px 17px; gap:10px; height:100%;">
          <div class="card-top-bar bar-red"></div>
          <div style="font-family:var(--font-title); font-size:14px; font-weight:700; color:#202124;">3 Batas Model P02 (Dengan Bahasa Sederhana)</div>
          <div style="display:flex; flex-direction:column; gap:9px; flex:1; justify-content:space-between;">
            <div class="card-tint red" style="padding:11px 13px; flex:1; display:flex; flex-direction:column; justify-content:center;">
              <div class="card-title" style="color:#C5221F; font-size:13px;">1. Foto Diluruskan Jadi 1 Baris Panjang</div>
              <p class="card-text" style="font-size:12px; margin-top:3px; line-height:1.42;">Semua piksel foto diratakan berjejer (<code>Flatten</code>), sehingga mata &amp; gaun Elsa yang berdekatan malah terpisah jauh.</p>
            </div>
            <div class="card-tint yellow" style="padding:11px 13px; flex:1; display:flex; flex-direction:column; justify-content:center;">
              <div class="card-title" style="color:#B06000; font-size:13px;">2. Menambah Lapisan Bikin Kabel Membengkak</div>
              <p class="card-text" style="font-size:12px; margin-top:3px; line-height:1.42;">Baru 1 lapis saja butuh <code>{p02_p:,}</code> kabel bobot. Kalau ditambah 2 lapis biasa, jumlahnya melonjak jadi <strong>~9,6 Juta kabel</strong>!</p>
            </div>
            <div class="card-tint blue" style="padding:11px 13px; flex:1; display:flex; flex-direction:column; justify-content:center;">
              <div class="card-title" style="color:#1A73E8; font-size:13px;">3. Mudah Menghafal Warna Latar Belakang</div>
              <p class="card-text" style="font-size:12px; margin-top:3px; line-height:1.42;">Dengan ratusan ribu kabel &amp; 1 lapis saja, model mudah mencari jalan pintas menghafal warna latar ketimbang bentuk karakter.</p>
            </div>
          </div>
          <div class="callout" style="padding:9px 12px; font-size:12px; line-height:1.42;">
            <strong>Pertanyaan Hari Ini:</strong> Bagaimana merancang <em>arsitektur</em> AI yang paham bentuk 2D, tidak boros kabel, dan tahan latar ramai?
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

    # S06: #1.1 MLP In General (Interactive Input / Hidden / Output Anatomy)
    slides.append(f"""
    <section class="slide" id="s06-mlp-slide" data-title="#1.1 MLP — Gambaran Umum" data-notes="Alokasi waktu: 1.5 menit. Penjelasan interaktif anatomi MLP: bedakan jelas Input Layer (kuning), Hidden Layer 1 &amp; 2 ciri khas MLP (biru), dan Output Layer 5 kelas Frozen (hijau) dengan toggle 0/1/2 Hidden &amp; Play aliran sinyal.">
      <div class="kicker">ARSITEKTUR #1 · ANATOMI &amp; SIMULASI DASAR MLP</div>
      <h2>MLP: Membedah <span style="color:#B06000;">Input Layer</span>, <span class="hl-blue">Hidden Layer</span> &amp; <span class="hl-green">Output Layer</span></h2>
      <div class="sim-bar pdf-keep-ui" id="s06-mlp-bar" style="margin-bottom:2px;">
        <button type="button" class="btn-ui outline" data-s06m="0" onclick="setS06Mlp(0)">0 Hidden (P02)</button>
        <button type="button" class="btn-ui outline" data-s06m="1" onclick="setS06Mlp(1)">1 Hidden (64)</button>
        <button type="button" class="btn-ui" data-s06m="2" onclick="setS06Mlp(2)">2 Hidden (MLP 64&#8594;32)</button>
        <span class="sim-ctrl-sep"></span>
        <button type="button" class="btn-ui play-btn" id="s06-play-btn" onclick="playS06Mlp()">&#9654; Play Neuron</button>
        <button type="button" class="btn-ui outline" onclick="stepS06Neuron()">&#9197; +1 Neuron</button>
        <button type="button" class="btn-ui outline" onclick="resetS06Mlp()">&#8634; Reset</button>
        <div class="kpi-row">
          <span class="kpi-chip" id="s06-kpi-param">Param: {r_mlp['total_params']:,}</span>
          <span class="kpi-chip" id="s06-kpi-badge" style="background:#E8F0FE; color:#1A73E8; border-color:#C6DAFC;">MLP Penuh (2 Hidden)</span>
        </div>
      </div>

      <div class="grid-2" style="grid-template-columns:0.86fr 1.14fr; flex:1; min-height:0; margin-top:6px; align-items:stretch; gap:12px;">
        <div class="card surface" style="display:flex; flex-direction:column; justify-content:space-between; gap:8px; padding:13px 15px;">
          <div class="card-top-bar bar-blue"></div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-family:var(--font-title); font-size:13.2px; color:#202124;">3 Bagian Penting Arsitektur MLP</strong>
            <span class="pill blue" style="font-size:9.2px; padding:2px 8px;">Klik Layer untuk Cek</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:8px; flex:1; justify-content:space-between;">
            <div class="card sync-card" id="s06-card-in" onclick="focusS06Step(1)" style="cursor:pointer; background:#FFFDF5; border-color:#FDE293; padding:10px 12px; flex:1; display:flex; flex-direction:column; justify-content:center;">
              <div style="display:flex; align-items:center; gap:7px;">
                <span class="pill yellow" style="font-size:9px; padding:1.5px 7px;">1. INPUT LAYER</span>
                <strong style="font-family:var(--font-title); font-size:12.2px; color:#B06000;">150.528 Angka Piksel</strong>
              </div>
              <p class="card-text" style="font-size:11.4px; margin-top:4px; line-height:1.38;">Foto <code>224×224×3</code> diratakan (<code>Flatten</code>) menjadi deretan angka masukan; belum ada proses menebak.</p>
            </div>

            <div class="card sync-card" id="s06-card-hid" onclick="focusS06Step(2)" style="cursor:pointer; background:#F4F8FF; border-color:#C6DAFC; padding:10px 12px; flex:1; display:flex; flex-direction:column; justify-content:center;">
              <div style="display:flex; align-items:center; gap:7px;">
                <span class="pill blue" style="font-size:9px; padding:1.5px 7px;">2. HIDDEN LAYER (INTI MLP)</span>
                <strong style="font-family:var(--font-title); font-size:12.2px; color:#1A73E8;" id="s06-hid-ttl">2 Lapis (64 &#8594; 32 Neuron)</strong>
              </div>
              <p class="card-text" style="font-size:11.4px; margin-top:4px; line-height:1.38;" id="s06-hid-desc">Lapisan tersembunyi di tengah yang merangkai ciri dasar (<em>biru gaun + putih salju</em>) sebelum mengambil keputusan.</p>
            </div>

            <div class="card sync-card" id="s06-card-out" onclick="focusS06Step(3)" style="cursor:pointer; background:#F5FBF7; border-color:#A8DAB5; padding:10px 12px; flex:1; display:flex; flex-direction:column; justify-content:center;">
              <div style="display:flex; align-items:center; gap:7px;">
                <span class="pill green" style="font-size:9px; padding:1.5px 7px;">3. OUTPUT LAYER</span>
                <strong style="font-family:var(--font-title); font-size:12.2px; color:#137333;">5 Kelas Frozen (Softmax)</strong>
              </div>
              <p class="card-text" style="font-size:11.4px; margin-top:4px; line-height:1.38;">Menghasilkan peluang akhir 5 karakter: <strong>Anna, Elsa, Kristoff, Olaf, Sven</strong> (total = 100%).</p>
            </div>
          </div>
          <div class="callout blue" id="s06-mlp-callout" style="font-size:11.3px; padding:8px 11px; line-height:1.38;">
            <strong>Kunci Pola Corong:</strong> Jumlah neuron mengecil bertahap (<code>150.528 ≫ 64 &gt; 32 &gt; 5</code>) untuk menyaring jutaan piksel menjadi 5 keputusan karakter Frozen.
          </div>
        </div>

        <div class="card" id="s06-diag-wrap" style="position:relative; display:flex; flex-direction:column; justify-content:space-between; align-items:center; gap:6px; padding:12px 14px;">
          <canvas id="s06-motion-canvas" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:15;"></canvas>
          <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
            <span style="font-family:var(--font-title); font-size:12.6px; font-weight:700; color:#202124;" id="s06-diag-ttl">Peta Layer MLP: Input &#8594; Hidden (64 &#8594; 32) &#8594; Output</span>
            <span class="pill blue" style="font-size:9.2px; padding:2px 8px;" id="s06-diag-pill">Klik Neuron / ▶ Play</span>
          </div>
          <svg id="s06-mlp-svg" viewBox="0 0 470 262" style="width:100%; flex:1; max-height:296px;"></svg>
          <div id="s06-neuron-narr" style="width:100%; background:#FFF8E1; border:1px solid #FDE293; border-radius:8px; padding:4.5px 10px; font-size:10.4px; color:#202124; line-height:1.35;">
            <strong>Klik neuron mana saja</strong> (atau tekan <strong>&#9654; Play Neuron</strong>) untuk melihat sinyal mengalir rinci neuron demi neuron!
          </div>
          <div class="formula-box" id="s06-mlp-formula" style="width:100%; font-size:10.4px; padding:6px 10px;">
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
        <div class="card" style="border-top:5px solid #34A853; display:flex; flex-direction:column; justify-content:space-between; gap:8px; padding:12px 14px;">
          <span class="pill green" style="width:fit-content;">FITUR KHUSUS UTAMA</span>
          <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; flex:1; display:grid; grid-template-columns:1fr 118px; gap:10px; align-items:center; padding:9px 11px;">
            <div>
              <strong style="color:#137333; font-size:12.2px;">1. Representasi Hidden Bertingkat</strong>
              <div style="font-size:11.2px; margin-top:3px; color:#202124; line-height:1.38;">Kombinasi 2+ <em>Hidden Layer</em> + <code>ReLU</code> mampu membentuk batas pemisah berliku (<em>non-linear</em>): <code>h&#8322; = ReLU(W&#8322;·h&#8321; + b&#8322;)</code>.</div>
            </div>
            <svg viewBox="0 0 116 74" style="width:100%; height:72px; background:#FFFFFF; border:1px solid #A8DAB5; border-radius:8px;">
              <line x1="12" y1="62" x2="104" y2="12" stroke="#DADCE0" stroke-width="1.2" stroke-dasharray="3,2"/>
              <path d="M 10 56 Q 38 14, 62 38 T 106 18" fill="none" stroke="#137333" stroke-width="2.2"/>
              <circle cx="26" cy="24" r="4.2" fill="#4285F4"/><circle cx="44" cy="18" r="4.2" fill="#4285F4"/>
              <circle cx="34" cy="36" r="4.2" fill="#4285F4"/><circle cx="76" cy="18" r="4.2" fill="#4285F4"/>
              <polygon points="82,38 77,47 87,47" fill="#EA4335"/><polygon points="62,48 57,57 67,57" fill="#EA4335"/>
              <polygon points="94,48 89,57 99,57" fill="#EA4335"/><polygon points="36,52 31,61 41,61" fill="#EA4335"/>
              <text x="58" y="70" text-anchor="middle" font-family="Poppins" font-size="7.2" font-weight="700" fill="#137333">Batas Berliku ReLU</text>
            </svg>
          </div>
          <div class="mini-box" style="background:#E8F0FE; border-color:#C6DAFC; flex:1; display:grid; grid-template-columns:1fr 118px; gap:10px; align-items:center; padding:9px 11px;">
            <div>
              <strong style="color:#1A73E8; font-size:12.2px;">2. Koneksi Semua-ke-Semua (<em>All-to-All</em>)</strong>
              <div style="font-size:11.2px; margin-top:3px; color:#202124; line-height:1.38;">Setiap fitur masukan bebas berinteraksi langsung tanpa asumsi urutan ruang — sangat ideal untuk tabel angka CSV.</div>
            </div>
            <svg viewBox="0 0 116 74" style="width:100%; height:72px; background:#FFFFFF; border:1px solid #C6DAFC; border-radius:8px;">
              <line x1="34" y1="16" x2="72" y2="18" stroke="#90B4F8" stroke-width="1"/><line x1="34" y1="16" x2="72" y2="36" stroke="#90B4F8" stroke-width="1"/><line x1="34" y1="16" x2="72" y2="54" stroke="#90B4F8" stroke-width="1"/>
              <line x1="34" y1="36" x2="72" y2="18" stroke="#90B4F8" stroke-width="1"/><line x1="34" y1="36" x2="72" y2="36" stroke="#1A73E8" stroke-width="1.4"/><line x1="34" y1="36" x2="72" y2="54" stroke="#90B4F8" stroke-width="1"/>
              <line x1="34" y1="54" x2="72" y2="18" stroke="#90B4F8" stroke-width="1"/><line x1="34" y1="54" x2="72" y2="36" stroke="#90B4F8" stroke-width="1"/><line x1="34" y1="54" x2="72" y2="54" stroke="#90B4F8" stroke-width="1"/>
              <line x1="72" y1="18" x2="98" y2="36" stroke="#34A853" stroke-width="1.2"/><line x1="72" y1="36" x2="98" y2="36" stroke="#34A853" stroke-width="1.4"/><line x1="72" y1="54" x2="98" y2="36" stroke="#34A853" stroke-width="1.2"/>
              <rect x="6" y="10" width="28" height="12" rx="4" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1"/><text x="20" y="18.5" text-anchor="middle" font-family="Roboto Mono" font-size="6.4" font-weight="700" fill="#B06000">Luas</text>
              <rect x="6" y="30" width="28" height="12" rx="4" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1"/><text x="20" y="38.5" text-anchor="middle" font-family="Roboto Mono" font-size="6.2" font-weight="700" fill="#B06000">Kamar</text>
              <rect x="6" y="48" width="28" height="12" rx="4" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1"/><text x="20" y="56.5" text-anchor="middle" font-family="Roboto Mono" font-size="6.2" font-weight="700" fill="#B06000">Jarak</text>
              <circle cx="72" cy="18" r="5.5" fill="#E8F0FE" stroke="#1A73E8" stroke-width="1.3"/>
              <circle cx="72" cy="36" r="5.5" fill="#1A73E8"/>
              <circle cx="72" cy="54" r="5.5" fill="#E8F0FE" stroke="#1A73E8" stroke-width="1.3"/>
              <circle cx="100" cy="36" r="7" fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"/><text x="100" y="38.5" text-anchor="middle" font-family="Poppins" font-size="6.2" font-weight="700" fill="#137333">Rp</text>
              <text x="58" y="69" text-anchor="middle" font-family="Poppins" font-size="7" font-weight="700" fill="#1A73E8">Semua-ke-Semua</text>
            </svg>
          </div>
          <div class="mini-box" style="flex:1; display:grid; grid-template-columns:1fr 118px; gap:10px; align-items:center; padding:9px 11px;">
            <div>
              <strong style="color:#202124; font-size:12.2px;">3. Menjadi &ldquo;Kepala&rdquo; di Ekor Modern</strong>
              <div style="font-size:11.2px; margin-top:3px; color:#5F6368; line-height:1.38;">Lapisan akhir <code>Dense + Softmax</code> di CNN, ResNet, maupun MobileNetV2 pada hakikatnya adalah blok MLP mini!</div>
            </div>
            <svg viewBox="0 0 116 74" style="width:100%; height:72px; background:#FFFFFF; border:1px solid #DADCE0; border-radius:8px;">
              <rect x="6" y="18" width="40" height="28" rx="6" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.3"/>
              <text x="26" y="30" text-anchor="middle" font-family="Poppins" font-size="6.8" font-weight="700" fill="#1A73E8">CNN /</text>
              <text x="26" y="39" text-anchor="middle" font-family="Poppins" font-size="6.4" font-weight="700" fill="#1A73E8">MobileNet</text>
              <line x1="46" y1="32" x2="53" y2="32" stroke="#5F6368" stroke-width="1.5"/>
              <polygon points="56,32 51,29 51,35" fill="#5F6368"/>
              <rect x="57" y="16" width="33" height="32" rx="6" fill="#E6F4EA" stroke="#34A853" stroke-width="1.6"/>
              <text x="73.5" y="29" text-anchor="middle" font-family="Poppins" font-size="6.8" font-weight="700" fill="#137333">MLP</text>
              <text x="73.5" y="38.5" text-anchor="middle" font-family="Poppins" font-size="6.2" font-weight="700" fill="#137333">Head</text>
              <line x1="90" y1="32" x2="94" y2="32" stroke="#34A853" stroke-width="1.5"/>
              <polygon points="97,32 93,29.5 93,34.5" fill="#34A853"/>
              <circle cx="104" cy="32" r="7" fill="#34A853"/><text x="104" y="34.5" text-anchor="middle" font-family="Poppins" font-size="6" font-weight="700" fill="#FFF">5</text>
              <text x="58" y="64" text-anchor="middle" font-family="Poppins" font-size="7" font-weight="700" fill="#5F6368">Ekstrak &#8594; Kepala MLP</text>
            </svg>
          </div>
        </div>

        <div class="card" style="border-top:5px solid #EA4335; display:flex; flex-direction:column; justify-content:space-between; gap:8px; padding:12px 14px;">
          <span class="pill red" style="width:fit-content;">CACAT FATAL SAAT MEMBACA FOTO</span>
          <div class="mini-box" style="background:#FCE8E6; border-color:#F6AEA9; flex:1; display:grid; grid-template-columns:1fr 126px; gap:10px; align-items:center; padding:10px 12px;">
            <div>
              <strong style="color:#C5221F; font-size:12.4px;">1. Ledakan Parameter: {r_mlp['total_params']:,} Param!</strong>
              <div style="font-size:11.4px; margin-top:4px; color:#202124; line-height:1.4;">Hanya dengan <code>64</code> hidden neuron pada <code>224×224×3</code>: layer ke-1 sendiri memakan <code>150.528 × 64 + 64 = 9.633.856</code> bobot!</div>
            </div>
            <svg viewBox="0 0 124 88" style="width:100%; height:86px; background:#FFFFFF; border:1px solid #F6AEA9; border-radius:8px;">
              <rect x="18" y="14" width="32" height="54" rx="4" fill="#EA4335"/>
              <text x="34" y="11" text-anchor="middle" font-family="Roboto Mono" font-size="7.4" font-weight="700" fill="#C5221F">9.64M</text>
              <text x="34" y="79" text-anchor="middle" font-family="Poppins" font-size="7.2" font-weight="700" fill="#C5221F">MLP</text>
              <rect x="74" y="62" width="32" height="6" rx="2" fill="#34A853"/>
              <text x="90" y="57" text-anchor="middle" font-family="Roboto Mono" font-size="7.4" font-weight="700" fill="#137333">0.10M</text>
              <text x="90" y="79" text-anchor="middle" font-family="Poppins" font-size="7.2" font-weight="700" fill="#137333">CNN</text>
              <rect x="64" y="22" width="52" height="16" rx="8" fill="#E6F4EA" stroke="#A8DAB5" stroke-width="1"/>
              <text x="90" y="32.5" text-anchor="middle" font-family="Poppins" font-size="7" font-weight="700" fill="#137333">~95× hemat</text>
            </svg>
          </div>
          <div class="mini-box" style="background:#FEF7E0; border-color:#FDE293; flex:1; display:grid; grid-template-columns:1fr 140px; gap:10px; align-items:center; padding:10px 12px;">
            <div>
              <strong style="color:#B06000; font-size:12.4px;">2. Spatial Blindness (Lupa Tetangga 2D)</strong>
              <div style="font-size:11.4px; margin-top:4px; color:#202124; line-height:1.4;">Jika karakter Elsa bergeser 2–8 piksel ke kanan atau kiri, seluruh piksel berpindah indeks — bobot terlatih kehilangan jejak!</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #FDE293; border-radius:8px; padding:6px; display:flex; flex-direction:column; gap:4px; align-items:center;">
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:5px; width:100%;">
                <div style="text-align:center;">
                  <div style="position:relative; width:56px; height:52px; margin:0 auto; border-radius:6px; overflow:hidden; border:1.5px solid #34A853; background:#F8F9FA;">
                    <img src="assets/P03/thumb_elsa.jpg" alt="Elsa Normal" style="width:100%; height:100%; object-fit:cover;"/>
                    <div style="position:absolute; inset:8px 14px; border:1.5px dashed #137333; border-radius:3px;"></div>
                  </div>
                  <div style="font-family:var(--font-code); font-size:7.6px; font-weight:700; color:#137333; margin-top:2px;">Slot Tepat ✓</div>
                </div>
                <div style="text-align:center;">
                  <div style="position:relative; width:56px; height:52px; margin:0 auto; border-radius:6px; overflow:hidden; border:1.5px solid #EA4335; background:#FCE8E6;">
                    <img src="assets/P03/thumb_elsa.jpg" alt="Elsa Geser" style="width:100%; height:100%; object-fit:cover; transform:translateX(9px);"/>
                    <div style="position:absolute; inset:8px 14px; border:1.5px dashed #C5221F; border-radius:3px;"></div>
                  </div>
                  <div style="font-family:var(--font-code); font-size:7.6px; font-weight:700; color:#C5221F; margin-top:2px;">Geser ✕ Bingung</div>
                </div>
              </div>
              <span style="font-family:var(--font-title); font-size:7.5px; font-weight:700; color:#B06000;">Kotak slot tetap, figur bergeser</span>
            </div>
          </div>
          <div class="callout red" style="font-size:11.4px; padding:9px 12px;">
            <strong>Akibat Nyata di Proyek Frozen:</strong> Pada foto <code>48×48</code>, MLP butuh <code>444.677</code> param tapi akurasi belajarnya macet di <code>{tr['mlp']['acc'][-1]}%</code> (validasi <code>{sh['mlp_val_acc']}%</code>) &#8594; butuh <strong>CNN</strong>!
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S08: #1.3 Simulasi Full MLP (P02-Grade Panorama: Real Photo Shift + Dual Sliders + 60fps Signal Canvas)
    slides.append(f"""
    <section class="slide" id="sim-mlp-slide" data-title="#1.3 Simulasi Full Arsitektur MLP" data-notes="Alokasi waktu: 2 menit. Simulator #1 (standar P02): pilih foto Anna/Elsa/Olaf, geser jumlah neuron Hidden (4..128), geser posisi foto 0..4px secara langsung di grid koordinat tetap, dan jalankan Play 60fps.">
      <div class="kicker">ARSITEKTUR #1 · SIMULASI FULL MLP (DATA FROZEN NYATA)</div>
      <h2>Simulasi MLP: <span class="hl-blue">Ledakan Bobot Hidden Layer</span> &amp; <span class="hl-red">Tes Geser Piksel</span></h2>

      <div class="sim-bar pdf-keep-ui" id="sim-mlp-bar" style="margin-bottom:5px; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:11px; padding:4px 8px; gap:5px; flex-wrap:nowrap;">
        <div style="display:flex; align-items:center; gap:4px; flex-shrink:0;">
          <button type="button" class="btn-ui play-btn" id="mlp-play-btn" onclick="playMlpSim()" style="padding:3.5px 8.5px; font-size:9.8px;">&#9654; Play</button>
          <button type="button" class="btn-ui outline" onclick="stepMlpSim()" style="padding:3.5px 7px; font-size:9.6px; color:#137333; border-color:#A8DAB5;">&#9197; +1 Tahap</button>
          <button type="button" class="btn-ui outline" onclick="resetMlpSim()" style="padding:3.5px 6.5px; font-size:9.6px; color:#5F6368; border-color:#DADCE0;">&#8634; Reset</button>
        </div>
        <div id="mlp-char-bar" style="display:flex; align-items:center; gap:3.5px; flex-shrink:0;">
          <button type="button" class="btn-ui outline" data-mchar="0" onclick="selectMlpChar(0)" style="padding:2px 7px 2px 3px; font-size:9.6px; border-radius:999px; display:inline-flex; align-items:center; gap:4px;"><img src="assets/P03/thumb_anna.jpg" alt="Anna" style="width:16px; height:16px; border-radius:50%; object-fit:cover;"/>Anna</button>
          <button type="button" class="btn-ui" data-mchar="1" onclick="selectMlpChar(1)" style="padding:2px 7px 2px 3px; font-size:9.6px; border-radius:999px; display:inline-flex; align-items:center; gap:4px;"><img src="assets/P03/thumb_elsa.jpg" alt="Elsa" style="width:16px; height:16px; border-radius:50%; object-fit:cover;"/>Elsa</button>
          <button type="button" class="btn-ui outline" data-mchar="2" onclick="selectMlpChar(2)" style="padding:2px 7px 2px 3px; font-size:9.6px; border-radius:999px; display:inline-flex; align-items:center; gap:4px;"><img src="assets/P03/thumb_olaf.jpg" alt="Olaf" style="width:16px; height:16px; border-radius:50%; object-fit:cover;"/>Olaf</button>
        </div>
        <div style="display:flex; align-items:center; gap:7px; flex-shrink:0;">
          <div style="display:flex; align-items:center; gap:4px; background:#FFFFFF; border:1px solid #DADCE0; border-radius:999px; padding:2px 7px;">
            <strong style="font-family:var(--font-title); font-size:9.2px; color:#1A73E8;">Hidden:</strong>
            <input id="mlp-hid-slider" type="range" min="4" max="128" step="4" value="64" oninput="onMlpSlider()" style="width:52px; accent-color:#1A73E8; cursor:pointer; margin:0;"/>
            <span id="mlp-hid-val" style="font-family:var(--font-code); font-size:9.2px; font-weight:700; color:#1A73E8; min-width:22px; text-align:right;">64</span>
          </div>
          <div style="display:flex; align-items:center; gap:4px; background:#FFFFFF; border:1px solid #DADCE0; border-radius:999px; padding:2px 7px;">
            <strong style="font-family:var(--font-title); font-size:9.2px; color:#C5221F;">Geser:</strong>
            <input id="mlp-shift-slider" type="range" min="0" max="16" step="4" value="0" oninput="onMlpSlider()" style="width:48px; accent-color:#EA4335; cursor:pointer; margin:0;"/>
            <span id="mlp-shift-val" style="font-family:var(--font-code); font-size:9.2px; font-weight:700; color:#C5221F; min-width:30px; text-align:right;">0px</span>
          </div>
          <span class="pill blue" id="mlp-vis-badge" style="font-size:9.6px; padding:2.5px 9px; white-space:nowrap;">Siap · 82%</span>
        </div>
      </div>

      <div id="mlp-hero-wrap" style="position:relative; flex:1; min-height:0; display:flex; flex-direction:column; justify-content:space-between; background:#FFFFFF; border:1.5px solid #C6DAFC; border-radius:15px; padding:7px 10px; margin-bottom:6px; box-shadow:0 4px 14px rgba(66,133,244,0.06);">
        <canvas id="mlp-motion-canvas" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:20;"></canvas>

        <div style="flex:1; min-height:0; display:grid; grid-template-columns:202px 14px 1fr; gap:4px; align-items:stretch;">
          <!-- LEFT: REAL FROZEN PHOTO INSIDE FIXED COORDINATE SLOT FRAME + LIVE FLATTEN STRIP -->
          <div style="background:#F8F9FA; border:1px solid #E0E3E7; border-radius:11px; padding:6px 8px; display:flex; flex-direction:column; justify-content:space-between; gap:4px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-family:var(--font-title); font-size:9.8px; font-weight:700; color:#202124;" id="mlp-photo-lbl">Foto Elsa (224×224)</span>
              <span class="pill blue" id="mlp-slot-pill" style="font-size:8.4px; padding:1.5px 6px;">Slot 100%</span>
            </div>
            <div style="position:relative; flex:1; min-height:94px; background:#D7D2CA; border-radius:9px; border:1.8px solid #4285F4; overflow:hidden;" id="mlp-photo-box">
              <img id="mlp-photo-img" src="assets/P03/thumb_elsa.jpg" alt="Frozen Input" style="width:100%; height:100%; object-fit:cover; display:block; transform:scale(1.18) translateX(0px); transition:transform 0.22s ease;"/>
              <!-- Fixed memorized coordinate grid slots overlay -->
              <div style="position:absolute; inset:14% 25%; border:2px dashed #FBBC04; border-radius:6px; box-shadow:inset 0 0 0 1px rgba(0,0,0,0.22); pointer-events:none;"></div>
              <span id="mlp-slot-tag" style="position:absolute; bottom:4px; left:4px; right:4px; text-align:center; background:rgba(32,33,36,0.78); color:#FFF; font-family:var(--font-code); font-size:7.8px; padding:1.5px 4px; border-radius:4px;">Slot Terlatih Pas ✓</span>
            </div>
            <div id="mlp-flat-strip" style="background:#FFF; border:1px solid #E0E3E7; border-radius:6px; padding:3px 5px; display:flex; flex-direction:column; gap:2px;">
              <div style="display:flex; justify-content:space-between; font-family:var(--font-code); font-size:7.2px; color:#5F6368; font-weight:700;">
                <span>Slot Flatten Tetap:</span><span id="mlp-flat-note" style="color:#137333;">Piksel Pas</span>
              </div>
              <div id="mlp-flat-cells" style="display:grid; grid-template-columns:repeat(5,1fr); gap:2px;"></div>
            </div>
            <div style="display:flex; gap:4px; align-items:center; justify-content:space-between;" class="pdf-keep-ui">
              <button type="button" class="btn-ui outline" onclick="nudgeMlpShift(-4)" style="flex:0.85; padding:2.5px 5px; font-size:8.6px; white-space:nowrap;">&#8592; 4px</button>
              <button type="button" class="btn-ui outline" onclick="nudgeMlpShift(4)" style="flex:1.15; padding:2.5px 5px; font-size:8.6px; white-space:nowrap; color:#C5221F; border-color:#F6AEA9;">Geser +4px &#8594;</button>
            </div>
          </div>

          <!-- ARROW: Photo -> Network -->
          <div style="display:flex; align-items:center; justify-content:center;">
            <svg viewBox="0 0 18 18" style="width:14px; height:14px;">
              <line x1="1" y1="9" x2="10" y2="9" stroke="#4285F4" stroke-width="2.5" stroke-linecap="round"/>
              <polygon points="8,4 17,9 8,14" fill="#4285F4"/>
            </svg>
          </div>

          <!-- CENTER-RIGHT: WIDE NETWORK PANORAMA + LIVE SOFTMAX BARS -->
          <div style="display:flex; align-items:center; justify-content:center; min-height:0;">
            <svg id="mlp-sim-svg" viewBox="0 0 760 236" style="width:100%; height:100%; max-height:276px; display:block;"></svg>
          </div>
        </div>

        <!-- BOTTOM LIVE MATH & DIAGNOSTIC BAR -->
        <div style="display:grid; grid-template-columns:1.18fr 1fr; gap:8px; margin-top:5px;">
          <div style="background:#FEF7E0; border:1px solid #FDE293; border-radius:8px; padding:5.5px 10px; font-family:var(--font-code); font-size:9.6px; color:#202124; line-height:1.35;" id="mlp-math-eq">
            Bobot = (150.528×64+64) + (64×32+32) + (32×5+5) = <strong>9.636.101 param</strong>
          </div>
          <div style="background:#E6F4EA; border:1px solid #A8DAB5; border-radius:8px; padding:5.5px 10px; font-size:10.3px; color:#202124; line-height:1.35;" id="mlp-sim-callout">
            <strong>Posisi Normal:</strong> Piksel jatuh tepat di slot terlatih &rarr; Elsa unggul <strong>82%</strong>!
          </div>
        </div>
      </div>

      <!-- 4 CLICKABLE SYNCHRONIZED STAGE CARDS -->
      <div style="display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:8px; flex:0 0 auto;">
        <div class="card surface sync-card" id="mlp-stage-1" onclick="jumpMlpStep(1)" style="cursor:pointer; padding:6px 10px; gap:2px;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title" style="font-size:11px; color:#B06000;">1. Foto 2D &#8594; Flatten</div>
          <div style="font-size:9.8px; color:#3C4043; line-height:1.3;" id="mlp-st1-desc"><code>224×224×3</code> diratakan jadi <code>150.528</code> slot koordinat tetap.</div>
        </div>
        <div class="card surface sync-card" id="mlp-stage-2" onclick="jumpMlpStep(2)" style="cursor:pointer; padding:6px 10px; gap:2px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title" style="font-size:11px; color:#1A73E8;" id="mlp-st2-ttl">2. Hidden Dense (64 &#8594; 32)</div>
          <div style="font-size:9.8px; color:#3C4043; line-height:1.3;" id="mlp-st2-desc">Setiap neuron terhubung ke semua piksel &#8594; bobot meledak!</div>
        </div>
        <div class="card surface sync-card" id="mlp-stage-3" onclick="jumpMlpStep(3)" style="cursor:pointer; padding:6px 10px; gap:2px;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title" style="font-size:11px; color:#137333;">3. Softmax &amp; Argmax (5)</div>
          <div style="font-size:9.8px; color:#3C4043; line-height:1.3;" id="mlp-st3-desc">Mengubah skor akhir ke peluang 0–100% tiap karakter.</div>
        </div>
        <div class="card surface sync-card" id="mlp-stage-4" onclick="jumpMlpStep(4)" style="cursor:pointer; padding:6px 10px; gap:2px;">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title" style="font-size:11px; color:#C5221F;">4. Cacat: Buta Geser</div>
          <div style="font-size:9.8px; color:#3C4043; line-height:1.3;" id="mlp-st4-desc">Klik untuk geser +8px: kabel tetap menembak latar polos!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S09: #1.4 Use Case MLP (Visual Illustrations on all 3 Cards)
    slides.append(f"""
    <section class="slide" data-title="#1.4 Use Case & Verdict MLP" data-notes="Alokasi waktu: 1 menit. Use case MLP di dunia nyata (tabular/CSV & classification head) dengan ilustrasi visual di tiap kartu dan alasan mengapa MLP tidak dipilih sebagai tulang punggung pemroses foto Frozen.">
      <div class="kicker">ARSITEKTUR #1 · USE CASE &amp; RELEVANSI PROYEK</div>
      <h2>Kapan <span class="hl-blue">MLP Dipakai</span> &amp; Kenapa Bukan untuk Foto Frozen?</h2>
      <div class="uc-grid" style="margin-top:4px; flex:1; min-height:0; align-items:stretch;">
        <div class="uc-card" style="border-top:5px solid #34A853; justify-content:space-between; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:5px;">
            <span class="pill green" style="width:fit-content;">✓ SANGAT COCOK</span>
            <div class="card-title" style="font-size:14px;">1. Data Tabel (Tabular / CSV)</div>
            <p class="card-text" style="font-size:11.6px;">Prediksi harga rumah, skor kredit, atau deteksi penipuan dari kolom fitur numerik bebas urutan.</p>
          </div>
          <div style="flex:1; min-height:142px; background:#F8FBF9; border:1.4px solid #CEEAD6; border-radius:11px; padding:7px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <svg viewBox="0 0 260 128" style="width:100%; height:100%; max-height:138px;" aria-label="Ilustrasi MLP pada Data Tabel CSV">
              <rect x="6" y="14" width="102" height="98" rx="8" fill="#FFFFFF" stroke="#34A853" stroke-width="1.5"/>
              <rect x="6" y="14" width="102" height="22" rx="8" fill="#34A853"/>
              <text x="57" y="29" text-anchor="middle" font-family="Poppins" font-size="9" font-weight="700" fill="#FFF">TABEL CSV (1D)</text>
              <rect x="13" y="42" width="88" height="18" rx="4" fill="#E6F4EA"/><text x="57" y="54" text-anchor="middle" font-family="Roboto Mono" font-size="8.2" font-weight="700" fill="#137333">Luas: 72 m²</text>
              <rect x="13" y="64" width="88" height="18" rx="4" fill="#FEF7E0"/><text x="57" y="76" text-anchor="middle" font-family="Roboto Mono" font-size="8.2" font-weight="700" fill="#B06000">Kamar: 3</text>
              <rect x="13" y="86" width="88" height="18" rx="4" fill="#E8F0FE"/><text x="57" y="98" text-anchor="middle" font-family="Roboto Mono" font-size="8.2" font-weight="700" fill="#1A73E8">Jarak: 2 km</text>
              <g stroke="#94A3B8" stroke-width="1.2">
                <line x1="108" y1="51" x2="146" y2="42"/><line x1="108" y1="51" x2="146" y2="84"/>
                <line x1="108" y1="73" x2="146" y2="42"/><line x1="108" y1="73" x2="146" y2="84"/>
                <line x1="108" y1="95" x2="146" y2="42"/><line x1="108" y1="95" x2="146" y2="84"/>
                <line x1="164" y1="42" x2="196" y2="63"/><line x1="164" y1="84" x2="196" y2="63"/>
              </g>
              <circle cx="155" cy="42" r="10" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.8"/><text x="155" y="45" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" font-weight="700" fill="#1A73E8">H1</text>
              <circle cx="155" cy="84" r="10" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.8"/><text x="155" y="87" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" font-weight="700" fill="#1A73E8">H2</text>
              <rect x="196" y="44" width="58" height="38" rx="8" fill="#34A853"/>
              <text x="225" y="60" text-anchor="middle" font-family="Poppins" font-size="8" font-weight="700" fill="#E6F4EA">Harga</text>
              <text x="225" y="73" text-anchor="middle" font-family="Roboto Mono" font-size="8.8" font-weight="700" fill="#FFF">850 jt</text>
            </svg>
          </div>
          <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; font-size:10.8px; padding:6px 9px;"><strong>Aturan:</strong> Kolom tabel = jagonya MLP!</div>
        </div>

        <div class="uc-card" style="border-top:5px solid #4285F4; justify-content:space-between; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:5px;">
            <span class="pill blue" style="width:fit-content;">✓ COCOK DI UJUNG</span>
            <div class="card-title" style="font-size:14px;">2. Classification Head CNN</div>
            <p class="card-text" style="font-size:11.6px;">Menjadi lapisan penutup (<code>Dense(64) &#8594; Dense(5)</code>) <strong>setelah</strong> gambar diringkas konvolusi menjadi vektor ciri kecil.</p>
          </div>
          <div style="flex:1; min-height:142px; background:#F4F8FF; border:1.4px solid #C6DAFC; border-radius:11px; padding:8px; display:flex; flex-direction:column; justify-content:center; gap:7px;">
            <div style="display:grid; grid-template-columns:54px 1fr; gap:8px; align-items:center;">
              <div style="position:relative; height:64px; border-radius:8px; overflow:hidden; border:2px solid #4285F4;">
                <img src="assets/P03/thumb_elsa.jpg" alt="Elsa Input" style="width:100%; height:100%; object-fit:cover; display:block;"/>
              </div>
              <svg viewBox="0 0 185 88" style="width:100%; height:88px;" aria-label="Ilustrasi MLP sebagai Classification Head di Ujung CNN">
                <rect x="2" y="16" width="52" height="56" rx="7" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.6"/>
                <text x="28" y="40" text-anchor="middle" font-family="Poppins" font-size="8.2" font-weight="700" fill="#1A73E8">CNN /</text>
                <text x="28" y="52" text-anchor="middle" font-family="Poppins" font-size="8.2" font-weight="700" fill="#1A73E8">MobV2</text>
                <path d="M54,44 L68,44" stroke="#5F6368" stroke-width="1.8"/>
                <rect x="68" y="22" width="44" height="44" rx="7" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.6"/>
                <text x="90" y="42" text-anchor="middle" font-family="Poppins" font-size="8.2" font-weight="700" fill="#B06000">GAP</text>
                <text x="90" y="54" text-anchor="middle" font-family="Roboto Mono" font-size="7.2" fill="#B06000">Ringkas</text>
                <path d="M112,44 L126,44" stroke="#1A73E8" stroke-width="1.8"/>
                <rect x="126" y="14" width="56" height="60" rx="8" fill="#1A73E8"/>
                <text x="154" y="37" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#FFF">MLP Head</text>
                <text x="154" y="51" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" fill="#D2E3FC">Dense(5)</text>
                <text x="154" y="64" text-anchor="middle" font-family="Poppins" font-size="7.5" font-weight="700" fill="#E6F4EA">→ Elsa ✓</text>
              </svg>
            </div>
            <div style="background:#FFFFFF; border:1px solid #C6DAFC; border-radius:7px; padding:4px 8px; font-family:var(--font-code); font-size:9.2px; color:#174EA6; text-align:center;">
              Hanya baca vektor ringkas, bukan 150.528 piksel!
            </div>
          </div>
          <div class="mini-box" style="background:#E8F0FE; border-color:#C6DAFC; font-size:10.8px; padding:6px 9px;"><strong>Aturan:</strong> Pakai sesudah ekstraksi ciri!</div>
        </div>

        <div class="uc-card" style="border-top:5px solid #EA4335; justify-content:space-between; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:5px;">
            <span class="pill red" style="width:fit-content;">✕ HINDARI SEBAGAI BACKBONE</span>
            <div class="card-title" style="font-size:14px;">3. Foto Kamera ({tot_imgs} Foto)</div>
            <p class="card-text" style="font-size:11.6px;">Posisi figurin berubah-ubah &amp; latar <code>ramai</code> ({n_ramai} foto) membuat bobot MLP raksasa mudah terkecoh.</p>
          </div>
          <div style="flex:1; min-height:142px; background:#FFF6F5; border:1.4px solid #F6AEA9; border-radius:11px; padding:8px; display:flex; flex-direction:column; justify-content:center; gap:6px;">
            <div style="display:grid; grid-template-columns:86px 1fr; gap:8px; align-items:center;">
              <div style="position:relative; height:86px; border-radius:9px; overflow:hidden; border:2px solid #EA4335;">
                <img src="assets/P03/thumb_elsa_ramai.jpg" alt="Elsa Ramai" style="width:100%; height:100%; object-fit:cover; display:block;"/>
                <div style="position:absolute; inset:0; background:repeating-linear-gradient(90deg, rgba(234,67,53,0.18) 0 1px, transparent 1px 17px), repeating-linear-gradient(0deg, rgba(234,67,53,0.18) 0 1px, transparent 1px 17px); pointer-events:none;"></div>
                <span style="position:absolute; bottom:3px; left:3px; background:#EA4335; color:#FFF; font-family:var(--font-title); font-size:7.5px; font-weight:700; padding:1px 5px; border-radius:4px;">Latar Ramai</span>
              </div>
              <div style="display:flex; flex-direction:column; gap:4px; font-size:10.3px; color:#C5221F; line-height:1.34;">
                <div><strong>• {r_mlp['total_params']:,} kabel</strong> menembak tiap piksel termasuk cangkir &amp; dinding!</div>
                <div><strong>• Geser posisi dikit</strong> &#8594; semua bobot langsung salah sasaran.</div>
              </div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #F6AEA9; border-radius:7px; padding:4px 8px; font-family:var(--font-code); font-size:9.2px; color:#C5221F; text-align:center;">
              ✕ Rentan overfit pada {tot_imgs} foto Frozen!
            </div>
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

    # S11: #2.1 CNN Klasik In General (Clear 4-Step Flow + Synchronized Interactive Pipeline)
    slides.append(f"""
    <section class="slide" id="s11-cnn-slide" data-title="#2.1 CNN Klasik — Gambaran Umum" data-notes="Alokasi waktu: 1.5 menit. Jelaskan alur bertingkat CNN Klasik secara jelas: Foto 2D utuh -> Conv2D 3x3 geser (Feature Map) -> MaxPooling 2x2 (tahan geser) -> Conv Dalam + GAP Softmax (101.829 param).">
      <div class="kicker">ARSITEKTUR #2 · ALUR UTUH &amp; PENJELASAN IN GENERAL</div>
      <h2>CNN Klasik: <span class="hl-red">Ekstraksi Pola Bertingkat</span> dari Foto 2D (Bukan 1D!)</h2>

      <div class="sim-bar pdf-keep-ui" id="s11-cnn-bar" style="margin-bottom:6px; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:11px; padding:4px 9px; gap:6px;">
        <div style="display:flex; align-items:center; gap:5px;">
          <button type="button" class="btn-ui play-btn" id="s11-play-btn" onclick="playS11Cnn()" style="padding:3.5px 9px; font-size:9.8px;">&#9654; Play 4 Tahap</button>
          <button type="button" class="btn-ui outline" onclick="stepS11Cnn()" style="padding:3.5px 7.5px; font-size:9.6px; color:#137333; border-color:#A8DAB5;">&#9197; +1 Tahap</button>
          <button type="button" class="btn-ui outline" onclick="resetS11Cnn()" style="padding:3.5px 7px; font-size:9.6px; color:#5F6368; border-color:#DADCE0;">&#8634; Reset</button>
        </div>
        <span class="pill blue" id="s11-status-pill" style="font-size:9.8px; padding:2.5px 10px;">Total 3-Blok CNN: {r_cnn['total_params']:,} Param (~95× lebih hemat dari MLP!)</span>
      </div>

      <div class="grid-2" style="grid-template-columns:1.12fr 0.88fr; flex:1; min-height:0; gap:12px; align-items:stretch;">
        <!-- LEFT: CRYSTAL CLEAR 4-STAGE VISUAL PIPELINE ON REAL ELSA -->
        <div class="card" style="padding:12px 14px; display:flex; flex-direction:column; justify-content:space-between; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-family:var(--font-title); font-size:12.6px; color:#202124;">Perjalanan Nyata Foto Elsa di Dalam CNN</strong>
            <span class="pill green" style="font-size:9.2px; padding:2px 8px;">Klik kartu untuk sorot tahap</span>
          </div>

          <div style="display:grid; grid-template-columns:1fr 16px 1fr; grid-template-rows:1fr 16px 1fr; gap:4px; flex:1; min-height:0; align-items:center;">
            <!-- Stage 1 Visual -->
            <div class="card sync-card" id="s11-vis-1" onclick="jumpS11Cnn(1)" style="cursor:pointer; height:100%; background:#FFFDF5; border-color:#FDE293; padding:8px; display:flex; align-items:center; gap:9px;">
              <div style="position:relative; width:72px; height:72px; flex-shrink:0; border-radius:8px; overflow:hidden; border:2px solid #FBBC04;">
                <img src="assets/P03/thumb_elsa.jpg" alt="Elsa 2D" style="width:100%; height:100%; object-fit:cover; display:block;"/>
                <div style="position:absolute; top:16px; left:22px; width:20px; height:20px; border:2.2px solid #EA4335; background:rgba(234,67,53,0.22); border-radius:3px;"></div>
              </div>
              <div style="min-width:0;">
                <span class="pill yellow" style="font-size:8.5px; padding:1px 6px;">TAHAP 1</span>
                <div style="font-family:var(--font-title); font-size:11.6px; font-weight:700; color:#B06000; margin-top:3px;">Input Foto 2D Utuh</div>
                <div style="font-size:10.2px; color:#3C4043; line-height:1.32; margin-top:2px;">Ukuran <code>224×224×3</code> tidak diluruskan. Kotak merah <code>3×3</code> siap memindai.</div>
              </div>
            </div>

            <div style="text-align:center; font-weight:800; color:#1A73E8; font-size:14px;">&#8594;</div>

            <!-- Stage 2 Visual -->
            <div class="card sync-card" id="s11-vis-2" onclick="jumpS11Cnn(2)" style="cursor:pointer; height:100%; background:#F4F8FF; border-color:#C6DAFC; padding:8px; display:flex; align-items:center; gap:9px;">
              <canvas id="s11-can-fm" width="72" height="72" style="width:72px; height:72px; flex-shrink:0; border-radius:8px; border:2px solid #4285F4; image-rendering:pixelated;"></canvas>
              <div style="min-width:0;">
                <span class="pill blue" style="font-size:8.5px; padding:1px 6px;">TAHAP 2</span>
                <div style="font-family:var(--font-title); font-size:11.6px; font-weight:700; color:#1A73E8; margin-top:3px;">Conv2D 3×3 + ReLU</div>
                <div style="font-size:10.2px; color:#3C4043; line-height:1.32; margin-top:2px;">Lahir <strong>Feature Map</strong>: tepi rambut &amp; gaun menyala biru terang!</div>
              </div>
            </div>

            <div style="grid-column:3; text-align:center; font-weight:800; color:#34A853; font-size:14px;">&#8595;</div>
            <div style="grid-column:1; grid-row:2;"></div>
            <div style="grid-column:2; grid-row:2;"></div>

            <!-- Stage 4 Visual (Bottom-Left: Hierarchical Output) -->
            <div class="card sync-card" id="s11-vis-4" onclick="jumpS11Cnn(4)" style="cursor:pointer; grid-column:1; grid-row:3; height:100%; background:#FFF7F6; border-color:#F6AEA9; padding:8px; display:flex; align-items:center; gap:9px;">
              <div style="width:72px; height:72px; flex-shrink:0; border-radius:8px; background:#FFFFFF; border:2px solid #EA4335; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:4px; gap:3px;">
                <span style="font-family:var(--font-code); font-size:7.6px; font-weight:700; color:#C5221F;">GAP → Softmax</span>
                <div style="width:100%; background:#E6F4EA; border-radius:4px; padding:2px 4px; font-family:var(--font-title); font-size:8.6px; font-weight:700; color:#137333; text-align:center;">Elsa ✓</div>
                <span style="font-family:var(--font-code); font-size:7.2px; color:#5F6368;">101.829 p</span>
              </div>
              <div style="min-width:0;">
                <span class="pill red" style="font-size:8.5px; padding:1px 6px;">TAHAP 4</span>
                <div style="font-family:var(--font-title); font-size:11.6px; font-weight:700; color:#C5221F; margin-top:3px;">Conv Dalam &#8594; Head</div>
                <div style="font-size:10.2px; color:#3C4043; line-height:1.32; margin-top:2px;">Gabung pola kepala &amp; gaun &#8594; diringkas <code>GAP</code> ke 5 kelas Frozen.</div>
              </div>
            </div>

            <div style="grid-column:2; grid-row:3; text-align:center; font-weight:800; color:#137333; font-size:14px;">&#8592;</div>

            <!-- Stage 3 Visual (Bottom-Right: MaxPool 2x2) -->
            <div class="card sync-card" id="s11-vis-3" onclick="jumpS11Cnn(3)" style="cursor:pointer; grid-column:3; grid-row:3; height:100%; background:#F5FBF7; border-color:#A8DAB5; padding:8px; display:flex; align-items:center; gap:9px;">
              <canvas id="s11-can-pool" width="72" height="72" style="width:72px; height:72px; flex-shrink:0; border-radius:8px; border:2px solid #34A853; image-rendering:pixelated;"></canvas>
              <div style="min-width:0;">
                <span class="pill green" style="font-size:8.5px; padding:1px 6px;">TAHAP 3</span>
                <div style="font-family:var(--font-title); font-size:11.6px; font-weight:700; color:#137333; margin-top:3px;">MaxPooling 2×2</div>
                <div style="font-size:10.2px; color:#3C4043; line-height:1.32; margin-top:2px;">Meringkas peta ÷2 sambil menyimpan ciri terkuat &amp; tahan geser.</div>
              </div>
            </div>
          </div>

          <div class="callout green" id="s11-callout" style="font-size:11px; padding:6px 10px; line-height:1.38;">
            <strong>Alur Sederhana (1 &#8594; 2 &#8594; 3 &#8594; 4):</strong> Foto 2D dipindai 1 filter geser (<em>Feature Map</em>), diringkas (<em>MaxPool</em>), lalu diulang 3 lapis sebelum <code>GAP → Softmax</code>.
          </div>
        </div>

        <!-- RIGHT: 4 SYNCHRONIZED EXPLANATIONS + MLP VS CNN SUMMARY -->
        <div class="card surface" style="padding:12px 14px; display:flex; flex-direction:column; justify-content:space-between; gap:7px;">
          <div class="card-top-bar bar-blue"></div>
          <div style="font-family:var(--font-title); font-size:13px; font-weight:700; color:#202124;">Kenapa Alur CNN Mengalahkan MLP?</div>
          <div style="display:flex; flex-direction:column; gap:6.5px; flex:1; justify-content:space-between;">
            <div class="card sync-card" id="s11-card-1" onclick="jumpS11Cnn(1)" style="cursor:pointer; padding:7.5px 10px; flex:1; justify-content:center;">
              <div style="font-family:var(--font-title); font-size:11.4px; font-weight:700; color:#B06000;">1. Tetap 2D (Bentuk Tetangga Aman)</div>
              <div style="font-size:10.5px; color:#3C4043; line-height:1.34; margin-top:2px;">Piksel wajah, mahkota, dan gaun Elsa tetap berdekatan — tidak dirusak oleh <code>Flatten</code> di awal.</div>
            </div>
            <div class="card sync-card" id="s11-card-2" onclick="jumpS11Cnn(2)" style="cursor:pointer; padding:7.5px 10px; flex:1; justify-content:center;">
              <div style="font-family:var(--font-title); font-size:11.4px; font-weight:700; color:#1A73E8;">2. Filter Geser Sama (Parameter Sharing)</div>
              <div style="font-size:10.5px; color:#3C4043; line-height:1.34; margin-top:2px;">1 filter <code>3×3</code> cuma butuh <strong>10 bobot</strong>, lalu digeser ke seluruh foto untuk mengenali tepi di mana pun posisinya.</div>
            </div>
            <div class="card sync-card" id="s11-card-3" onclick="jumpS11Cnn(3)" style="cursor:pointer; padding:7.5px 10px; flex:1; justify-content:center;">
              <div style="font-family:var(--font-title); font-size:11.4px; font-weight:700; color:#137333;">3. Pooling Ringkas &amp; Tahan Pergeseran</div>
              <div style="font-size:10.5px; color:#3C4043; line-height:1.34; margin-top:2px;"><code>MaxPool 2×2</code> mengambil nilai terkuat per kotak sehingga posisi bergeser sedikit tetap terbaca sama.</div>
            </div>
            <div class="card sync-card" id="s11-card-4" onclick="jumpS11Cnn(4)" style="cursor:pointer; padding:7.5px 10px; flex:1; justify-content:center;">
              <div style="font-family:var(--font-title); font-size:11.4px; font-weight:700; color:#C5221F;">4. Hierarki Ciri (Tepi &#8594; Objek Utuh)</div>
              <div style="font-size:10.5px; color:#3C4043; line-height:1.34; margin-top:2px;">Blok awal cari garis &#8594; blok tengah cari tekstur kain &#8594; blok dalam kenali figurin &#8594; hanya <strong>101.829 param</strong>!</div>
            </div>
          </div>
          <div class="mini-box" style="background:#E8F0FE; border-color:#C6DAFC; padding:6px 10px; font-size:10.6px; color:#174EA6; text-align:center;">
            <strong>Perbandingan Nyata:</strong> MLP <code>{r_mlp['total_params']:,}</code> param &#8594; CNN 3-Blok <strong><code>{r_cnn['total_params']:,}</code> param</strong> (~95× lebih ringan!)
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
""")

    # S12: #2.2 Fitur Khusus CNN Klasik (Real Frozen Photos + 3x3 Sliding Window + Pixel Transfer Animation)
    slides.append(f"""
    <section class="slide" data-title="#2.2 CNN Klasik — Fitur Khusus" data-notes="Alokasi waktu: 2 menit. Bedah 4 fitur khusus CNN memakai foto asli dataset Frozen dengan animasi sliding window 3x3, perpindahan piksel ke Feature Map, Stride &amp; Padding, MaxPooling 2x2, dan Receptive Field.">
      <div class="kicker">ARSITEKTUR #2 · FITUR KHUSUS (ANIMASI SLIDING WINDOW FROZEN)</div>
      <h2>4 Senjata Khusus CNN: <span class="hl-red">Kernel, Stride, Padding &amp; Pooling</span></h2>
      <div class="grid-2" style="flex:1; min-height:0; align-items:stretch;">
        <!-- CARD 1: KERNEL 3x3 SLIDING WINDOW ON ELSA PHOTO + PIXEL TRANSFER -->
        <div class="card-tint blue" style="padding:10px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:6px;">
          <div>
            <div class="card-title" style="color:#1A73E8; font-size:13.8px;">1. Kernel 3×3 Sliding Window &amp; Parameter Sharing</div>
            <p class="card-text" style="font-size:11.3px; margin-top:2px;">Satu <strong>Kernel <code>3×3×3</code></strong> (cuma <strong>28 param</strong>!) menggeser melintasi seluruh foto Frozen, mengalikan 9 piksel ke 1 sel output.</p>
          </div>
          <div style="background:#FFFFFF; border:1px solid #C6DAFC; border-radius:10px; padding:7px 10px; display:flex; align-items:center; justify-content:space-between; gap:8px; height:88px;">
            <div style="position:relative; width:72px; height:72px; flex-shrink:0; border-radius:7px; overflow:hidden; border:1.8px solid #4285F4;">
              <img src="assets/P03/thumb_elsa.jpg" alt="Elsa Kernel 3x3" style="width:100%; height:100%; object-fit:cover; display:block;"/>
              <div style="position:absolute; inset:0; background:repeating-linear-gradient(90deg, rgba(255,255,255,0.22) 0 1px, transparent 1px 12px), repeating-linear-gradient(0deg, rgba(255,255,255,0.22) 0 1px, transparent 1px 12px);"></div>
              <div class="s12c-elsa-scan" style="position:absolute; top:0; left:0; width:26px; height:26px; border:2.2px solid #FBBC04; background:rgba(234,67,53,0.34); border-radius:3px; display:flex; align-items:center; justify-content:center;">
                <span style="font-family:var(--font-code); font-size:7px; font-weight:800; color:#FFF;">3×3</span>
              </div>
            </div>
            <div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:3px; min-width:0;">
              <span style="font-family:var(--font-code); font-size:8.4px; font-weight:700; color:#C5221F; background:#FCE8E6; padding:1.5px 7px; border-radius:999px;">9 Piksel × Kernel 3×3</span>
              <div style="position:relative; width:74px; height:14px; display:flex; align-items:center;">
                <div style="width:100%; height:2px; background:#C6DAFC;"></div>
                <span class="s12c-px-fly" style="position:absolute; left:0; width:10px; height:10px; border-radius:50%; background:#EA4335; border:1.5px solid #FFF; box-shadow:0 0 6px #EA4335;"></span>
                <span style="position:absolute; right:-2px; font-size:11px; color:#1A73E8; font-weight:800;">&#9654;</span>
              </div>
              <span style="font-family:var(--font-code); font-size:7.8px; color:#5F6368;">transfer nilai piksel</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px; flex-shrink:0;">
              <div style="width:58px; height:58px; border-radius:7px; border:1.8px solid #1A73E8; background:#F4F8FF; padding:5px; display:grid; grid-template-columns:1fr 1fr; gap:4px;">
                <div class="s12c-fm1" style="background:#4285F4; border-radius:3px;"></div>
                <div class="s12c-fm2" style="background:#1A73E8; border-radius:3px;"></div>
                <div class="s12c-fm3" style="background:#4285F4; border-radius:3px;"></div>
                <div class="s12c-fm4" style="background:#1A73E8; border-radius:3px;"></div>
              </div>
              <span style="font-family:var(--font-code); font-size:7.6px; font-weight:700; color:#1A73E8;">Feature Map</span>
            </div>
          </div>
          <div class="formula-box" style="font-size:10.5px; padding:5px 10px;">1 Filter = <strong>28 param</strong> (geser ke seluruh foto, bukan 150.528×64 kabel!)</div>
        </div>

        <!-- CARD 2: STRIDE & PADDING ON ANNA PHOTO -->
        <div class="card-tint red" style="padding:10px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:6px;">
          <div>
            <div class="card-title" style="color:#C5221F; font-size:13.8px;">2. Stride &amp; Padding (Atur Langkah &amp; Tepi)</div>
            <p class="card-text" style="font-size:11.3px; margin-top:2px;"><strong>Stride (S)</strong> = lompatan jendela geser (<code>S=1</code> rapat; <code>S=2</code> loncat 2 &#8594; ukuran ÷2). <strong>Padding (P)</strong> = bingkai <code>0</code> agar pinggiran foto tetap terpindai.</p>
          </div>
          <div style="background:#FFFFFF; border:1px solid #F6AEA9; border-radius:10px; padding:7px 10px; display:flex; align-items:center; justify-content:space-between; gap:10px; height:88px;">
            <div class="s12c-pad" style="padding:5px; border-radius:8px; background:#E8F0FE; border:1.8px dashed #4285F4; flex-shrink:0;">
              <div style="position:relative; width:58px; height:58px; border-radius:5px; overflow:hidden; border:1.2px solid #5F6368;">
                <img src="assets/P03/thumb_anna.jpg" alt="Anna Padding" style="width:100%; height:100%; object-fit:cover; display:block;"/>
                <span style="position:absolute; bottom:2px; left:2px; right:2px; text-align:center; background:rgba(26,115,232,0.86); color:#FFF; font-family:var(--font-code); font-size:7px; font-weight:700; border-radius:3px;">Pad P=1</span>
              </div>
            </div>
            <div style="flex:1; display:flex; flex-direction:column; justify-content:center; gap:7px; min-width:0;">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-family:var(--font-code); font-size:8.4px; font-weight:700; color:#1A73E8; width:62px;">S=1 Rapat</span>
                <div style="position:relative; flex:1; height:16px; border-radius:4px; background:#F1F3F4; border:1px solid #DADCE0; overflow:hidden;">
                  <div class="s12c-s1" style="position:absolute; top:2px; left:2px; width:18px; height:10px; border-radius:2px; background:#4285F4;"></div>
                </div>
                <span style="font-family:var(--font-code); font-size:8.4px; font-weight:700; color:#1A73E8;">14×14</span>
              </div>
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-family:var(--font-code); font-size:8.4px; font-weight:700; color:#C5221F; width:62px;">S=2 Loncat</span>
                <div style="position:relative; flex:1; height:16px; border-radius:4px; background:#F1F3F4; border:1px solid #DADCE0; overflow:hidden;">
                  <div class="s12c-s2" style="position:absolute; top:2px; left:2px; width:18px; height:10px; border-radius:2px; background:#EA4335;"></div>
                </div>
                <span style="font-family:var(--font-code); font-size:8.4px; font-weight:700; color:#C5221F;">8×8</span>
              </div>
            </div>
          </div>
          <div class="formula-box" style="font-size:10.5px; padding:5px 10px;">Output = (W &minus; K + 2P) / S + 1 &nbsp;|&nbsp; (16&minus;3+0)/1+1 = <strong>14</strong></div>
        </div>

        <!-- CARD 3: MAXPOOLING 2x2 ON OLAF PHOTO + MAX PIXEL TRANSFER -->
        <div class="card-tint yellow" style="padding:10px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:6px;">
          <div>
            <div class="card-title" style="color:#B06000; font-size:13.8px;">3. MaxPooling 2×2 (Ringkas &amp; Tahan Geser)</div>
            <p class="card-text" style="font-size:11.3px; margin-top:2px;">Dari tiap kotak <code>2×2</code> di peta fitur Frozen, ambil hanya <strong>1 piksel terkuat</strong> &#8594; ukuran susut ÷2 dan tahan geser <code>1px</code>!</p>
          </div>
          <div style="background:#FFFFFF; border:1px solid #FDE293; border-radius:10px; padding:7px 10px; display:flex; align-items:center; justify-content:space-between; gap:8px; height:88px;">
            <div style="position:relative; width:72px; height:72px; flex-shrink:0; border-radius:7px; overflow:hidden; border:1.8px solid #F9AB00;">
              <img src="assets/P03/thumb_olaf.jpg" alt="Olaf MaxPool" style="width:100%; height:100%; object-fit:cover; filter:contrast(1.15) saturate(0.35); display:block;"/>
              <div style="position:absolute; inset:0; background:repeating-linear-gradient(90deg, rgba(251,188,4,0.35) 0 1px, transparent 1px 36px), repeating-linear-gradient(0deg, rgba(251,188,4,0.35) 0 1px, transparent 1px 36px);"></div>
              <div class="s12c-kern" style="position:absolute; top:2px; left:2px; width:32px; height:32px; border:2.2px solid #EA4335; background:rgba(251,188,4,0.32); border-radius:4px; display:flex; align-items:center; justify-content:center;">
                <span style="font-family:var(--font-code); font-size:7.5px; font-weight:800; color:#202124; background:rgba(255,255,255,0.82); padding:0 3px; border-radius:2px;">2×2</span>
              </div>
            </div>
            <div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:3px; min-width:0;">
              <span style="font-family:var(--font-code); font-size:8.4px; font-weight:700; color:#B06000; background:#FEF7E0; padding:1.5px 7px; border-radius:999px;">Ambil Maksimum!</span>
              <div style="position:relative; width:74px; height:14px; display:flex; align-items:center;">
                <div style="width:100%; height:2px; background:#FDE293;"></div>
                <span class="s12c-px-fly" style="position:absolute; left:0; width:10px; height:10px; border-radius:50%; background:#34A853; border:1.5px solid #FFF; box-shadow:0 0 6px #34A853;"></span>
                <span style="position:absolute; right:-2px; font-size:11px; color:#137333; font-weight:800;">&#9654;</span>
              </div>
              <span style="font-family:var(--font-code); font-size:7.8px; color:#5F6368;">buang 75% piksel lemah</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px; flex-shrink:0;">
              <div style="width:54px; height:54px; border-radius:7px; border:1.8px solid #34A853; background:#E6F4EA; padding:4px; display:grid; grid-template-columns:1fr 1fr; gap:3px; font-family:var(--font-code); font-size:9px; font-weight:700; text-align:center;">
                <div class="s12c-fm1" style="background:#FFF; border:1px solid #FBBC04; border-radius:3px; color:#C5221F; line-height:20px;">8</div>
                <div class="s12c-fm2" style="background:#FFF; border:1px solid #4285F4; border-radius:3px; color:#1A73E8; line-height:20px;">4</div>
                <div class="s12c-fm3" style="background:#FFF; border:1px solid #34A853; border-radius:3px; color:#137333; line-height:20px;">7</div>
                <div class="s12c-fm4" style="background:#FFF; border:1px solid #F9AB00; border-radius:3px; color:#B06000; line-height:20px;">6</div>
              </div>
              <span style="font-family:var(--font-code); font-size:7.6px; font-weight:700; color:#137333;">MaxPool ÷2</span>
            </div>
          </div>
          <div class="formula-box" style="font-size:10.5px; padding:5px 10px;"><code>14×14</code> &#8594; MaxPool <code>2×2</code> &#8594; <strong><code>7×7</code> (tahan geser 1px!)</strong></div>
        </div>

        <!-- CARD 4: RECEPTIVE FIELD ZOOM ON FROZEN PHOTO -->
        <div class="card-tint green" style="padding:10px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:6px;">
          <div>
            <div class="card-title" style="color:#137333; font-size:13.8px;">4. Receptive Field (Pandangan Makin Luas)</div>
            <p class="card-text" style="font-size:11.3px; margin-top:2px;">Makin dalam melewati <code>Conv2D + MaxPool</code>, 1 piksel atas merangkum area foto Frozen makin luas — dari tepi kecil ke karakter utuh!</p>
          </div>
          <div style="background:#FFFFFF; border:1px solid #A8DAB5; border-radius:10px; padding:7px 10px; display:flex; align-items:center; justify-content:space-between; gap:6px; height:88px;">
            <div class="s12c-rf1" style="display:flex; align-items:center; gap:5px;">
              <div style="position:relative; width:56px; height:56px; border-radius:7px; overflow:hidden; border:1.8px solid #4285F4;">
                <img src="assets/P03/thumb_elsa.jpg" alt="RF 3x3" style="width:100%; height:100%; object-fit:cover; opacity:0.42; display:block;"/>
                <div style="position:absolute; top:16px; left:22px; width:16px; height:16px; border:2px solid #1A73E8; background:rgba(66,133,244,0.28); border-radius:2px;"></div>
              </div>
              <span style="font-family:var(--font-code); font-size:8px; font-weight:700; color:#1A73E8;">1. Tepi<br/>3×3</span>
            </div>
            <span style="font-weight:800; color:#5F6368; font-size:12px;">&#8594;</span>
            <div class="s12c-rf2" style="display:flex; align-items:center; gap:5px;">
              <div style="position:relative; width:56px; height:56px; border-radius:7px; overflow:hidden; border:1.8px solid #FBBC04;">
                <img src="assets/P03/thumb_elsa.jpg" alt="RF 7x7" style="width:100%; height:100%; object-fit:cover; opacity:0.65; display:block;"/>
                <div style="position:absolute; top:10px; left:14px; width:30px; height:32px; border:2px solid #B06000; background:rgba(251,188,4,0.22); border-radius:3px;"></div>
              </div>
              <span style="font-family:var(--font-code); font-size:8px; font-weight:700; color:#B06000;">2. Gaun<br/>7×7</span>
            </div>
            <span style="font-weight:800; color:#5F6368; font-size:12px;">&#8594;</span>
            <div class="s12c-rf3" style="display:flex; align-items:center; gap:5px;">
              <div style="position:relative; width:60px; height:60px; border-radius:8px; overflow:hidden; border:2.2px solid #34A853;">
                <img src="assets/P03/thumb_elsa.jpg" alt="RF Utuh" style="width:100%; height:100%; object-fit:cover; display:block;"/>
              </div>
              <span style="font-family:var(--font-code); font-size:8.2px; font-weight:700; color:#137333;">3. Elsa<br/>Utuh ✓</span>
            </div>
          </div>
          <div class="formula-box" style="font-size:10.5px; padding:5px 10px;">Makin dalam = cakupan area foto <strong>makin luas!</strong></div>
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
        <button type="button" class="btn-ui" data-cnn-f="sobel_v" onclick="setCnnState({{filter:'sobel_v'}})">Tepi Vertikal</button>
        <button type="button" class="btn-ui outline" data-cnn-f="sobel_h" onclick="setCnnState({{filter:'sobel_h'}})">Tepi Horiz.</button>
        <button type="button" class="btn-ui outline" data-cnn-f="sharp" onclick="setCnnState({{filter:'sharp'}})">Pertajam</button>
        <button type="button" class="btn-ui outline" id="cnn-btn-stride" onclick="toggleCnnStride()">Stride: 1</button>
        <button type="button" class="btn-ui outline" id="cnn-btn-pad" onclick="toggleCnnPad()">Padding: Valid (0)</button>
        <span class="sim-ctrl-sep"></span>
        <button type="button" class="btn-ui play-btn" id="cnn-play-btn" onclick="playCnnSim()">&#9654; Play 3×3</button>
        <button type="button" class="btn-ui outline" onclick="stepCnnSim()">&#9197; +1 Kotak</button>
        <button type="button" class="btn-ui outline" onclick="resetCnnSim()">&#8634; Reset</button>
        <div class="kpi-row">
          <span class="kpi-chip" id="cnn-kpi-shape">FM: 14×14 &#8594; Pool: 7×7</span>
        </div>
      </div>

      <div class="cnn-canvas-strip" style="margin-top:8px; flex:1; min-height:0;">
        <div class="cnn-can-card" style="justify-content:space-between; padding:10px 12px;">
          <strong style="font-family:var(--font-title); font-size:12.2px;">1. Input Asli Elsa (<span id="cnn-in-dim">16×16</span>)</strong>
          <canvas id="cnn-can-in" width="212" height="212" style="cursor:crosshair;" title="Klik piksel mana saja untuk menggeser jendela 3×3"></canvas>
          <div style="width:100%; text-align:center;">
            <div style="font-family:var(--font-code); font-size:10.3px; color:#202124; font-weight:700;" id="cnn-lbl-in">Jendela geser 3×3 aktif (kotak kuning)</div>
            <div style="font-size:10px; color:#5F6368; margin-top:2px;">Klik piksel di kanvas untuk geser kotak <code>3×3</code> manual!</div>
          </div>
        </div>
        <div class="cnn-can-card" style="border-color:#4285F4; background:#F8FAFF; justify-content:space-between; padding:10px 12px;">
          <strong style="font-family:var(--font-title); font-size:12.2px; color:#1A73E8;">2. Feature Map (Conv2D + ReLU)</strong>
          <canvas id="cnn-can-fm" width="212" height="212" style="cursor:crosshair;" title="Klik sel untuk melihat area 3×3 asalnya"></canvas>
          <div style="width:100%; text-align:center;">
            <div style="font-family:var(--font-code); font-size:10.3px; color:#1A73E8; font-weight:700;" id="cnn-lbl-fm">14×14 (196 sel aktif)</div>
            <div style="font-size:10px; color:#5F6368; margin-top:2px;" id="cnn-kernel-txt">Kernel Sobel Vertikal <code>3×3</code> + ReLU (&gt;0 menyala biru)</div>
          </div>
        </div>
        <div class="cnn-can-card" style="border-color:#34A853; background:#F6FBF7; justify-content:space-between; padding:10px 12px;">
          <strong style="font-family:var(--font-title); font-size:12.2px; color:#137333;">3. MaxPool 2×2 &#8594; Head Softmax</strong>
          <canvas id="cnn-can-pool" width="212" height="212"></canvas>
          <div style="width:100%; text-align:center;">
            <div style="font-family:var(--font-code); font-size:10.3px; color:#137333; font-weight:700;" id="cnn-lbl-pool">7×7 &#8594; 49 ciri ke Softmax</div>
            <div style="font-size:10px; color:#5F6368; margin-top:2px;">Ambil nilai maksimum per kotak <code>2×2</code> (ringkas &amp; stabil)</div>
          </div>
        </div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1.15fr; gap:8px; margin-top:7px;">
        <div class="formula-box" id="cnn-sim-size" style="font-size:10.8px; text-align:left; padding:6px 10px;">
          <strong>Rumus Ukuran:</strong> (16 &minus; 3 + 2×0) / 1 + 1 = <strong>14×14</strong> &rarr; Pool <strong>7×7</strong> (hanya 10 param!)
        </div>
        <div class="formula-box" id="cnn-sim-formula" style="font-size:10.8px; text-align:left; padding:6px 10px; background:#FFF8E1; border-color:#FDE293;">
          <strong>Jendela 3×3 (baris 6, kol 8):</strong> Σ(Piksel×Kernel) &#8594; ReLU = <strong>1.44</strong> &#8594; Pool (3,4)
        </div>
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
        <button type="button" class="btn-ui" data-res="plain" onclick="setResnetSim('plain')">1. Plain Deep Net</button>
        <button type="button" class="btn-ui outline" data-res="resnet" onclick="setResnetSim('resnet')">2. ResNet (+Skip &amp; GAP)</button>
        <span class="sim-ctrl-sep"></span>
        <button type="button" class="btn-ui play-btn" id="res-play-btn" onclick="playResSim()">&#9654; Play Backprop</button>
        <button type="button" class="btn-ui outline" onclick="stepResSim()">&#9197; +1 Blok</button>
        <button type="button" class="btn-ui outline" onclick="resetResSim()">&#8634; Reset</button>
        <div class="kpi-row">
          <span class="kpi-chip" id="res-kpi-grad">Sinyal L1: 7% (Macet)</span>
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
        <button type="button" class="btn-ui" data-mob="standard" onclick="setMobSim('standard')">1. Conv2D Biasa</button>
        <button type="button" class="btn-ui outline" data-mob="mobilenetv2" onclick="setMobSim('mobilenetv2')">2. MobileNetV2 (Expand→DW→Proj)</button>
        <span class="sim-ctrl-sep"></span>
        <button type="button" class="btn-ui play-btn" id="mob-play-btn" onclick="playMobSim()">&#9654; Play Aliran Blok</button>
        <button type="button" class="btn-ui outline" onclick="stepMobSim()">&#9197; +1 Langkah</button>
        <button type="button" class="btn-ui outline" onclick="resetMobSim()">&#8634; Reset</button>
        <div class="kpi-row">
          <span class="kpi-chip" id="mob-kpi-ops">Perkalian: 231.2 Juta</span>
          <span class="kpi-chip" id="mob-kpi-save">Efisiensi: 1×</span>
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
        <button type="button" class="btn-ui" data-eff-s="b0" onclick="setEffState({{scale:'b0'}})">B0 (&phi;=0 · 224)</button>
        <button type="button" class="btn-ui outline" data-eff-s="b1" onclick="setEffState({{scale:'b1'}})">B1 (&phi;=1 · 240)</button>
        <button type="button" class="btn-ui outline" data-eff-s="b2" onclick="setEffState({{scale:'b2'}})">B2 (&phi;=2 · 260)</button>
        <button type="button" class="btn-ui outline" id="eff-se-btn" onclick="toggleEffSe()">SE: OFF</button>
        <span class="sim-ctrl-sep"></span>
        <button type="button" class="btn-ui play-btn" id="eff-play-btn" onclick="playEffSim()">&#9654; Play SE Gate</button>
        <button type="button" class="btn-ui outline" onclick="stepEffSim()">&#9197; +1 Tahap</button>
        <button type="button" class="btn-ui outline" onclick="resetEffSim()">&#8634; Reset</button>
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
    bmap = _bench_dict(data)
    p02_p = data["p02_1layer_params"]
    r_mlp = bmap["1. MLP (2 Hidden)"]
    r_mob = bmap["4. MobileNetV2"]
    r_eff = bmap["5. EfficientNetB0"]

    return f"""
    const P03_ELSA_16 = {elsa_16_json};

    // =========================================================================
    // SIMULATOR #1 (Slide 8): P02-Style Full Interactive MLP Panorama
    // (Real Frozen Photos + Hidden/Shift Sliders + 60fps Packet Overlay + Softmax)
    // =========================================================================
    const MLP_CHARS = [
      {{ name: 'Anna', src: 'assets/P03/thumb_anna.jpg', targetIdx: 0, baseProbs: [80, 9, 5, 4, 2] }},
      {{ name: 'Elsa', src: 'assets/P03/thumb_elsa.jpg', targetIdx: 1, baseProbs: [7, 82, 4, 5, 2] }},
      {{ name: 'Olaf', src: 'assets/P03/thumb_olaf.jpg', targetIdx: 3, baseProbs: [5, 8, 3, 81, 3] }},
    ];
    const MLP_CLASS_NAMES = ['Anna', 'Elsa', 'Kristoff', 'Olaf', 'Sven'];
    const mlpState = {{ charIdx: 1, hidden: 64, shift: 0, step: 0, raf: null, timer: null, phaseT: 0 }};

    function _stopMlpTimer() {{
      if (mlpState.timer) {{ clearInterval(mlpState.timer); mlpState.timer = null; }}
      if (mlpState.raf) {{ cancelAnimationFrame(mlpState.raf); mlpState.raf = null; }}
      const cv = document.getElementById('mlp-motion-canvas');
      if (cv) {{ const ctx = cv.getContext('2d'); if (ctx) ctx.clearRect(0, 0, cv.width, cv.height); }}
      const pb = document.getElementById('mlp-play-btn');
      if (pb) {{ pb.innerHTML = '&#9654; Play'; pb.classList.remove('playing'); }}
    }}

    function _calcMlpProbs() {{
      const ch = MLP_CHARS[mlpState.charIdx];
      const hFactor = Math.min(1.06, Math.max(0.76, 0.72 + (mlpState.hidden / 64) * 0.28));
      const shiftSteps = mlpState.shift / 4; // 0->0, 4px->1, 8px->2 (flips!), 12px->3, 16px->4
      const shiftPenalty = Math.min(0.84, shiftSteps * 0.34);
      const raw = ch.baseProbs.map((p, idx) => {{
        if (idx === ch.targetIdx) return Math.max(12, Math.round(p * hFactor * (1 - shiftPenalty)));
        const boostShare = idx === (ch.targetIdx + 2) % 5 ? 0.56 : (idx === (ch.targetIdx + 4) % 5 ? 0.26 : 0.09);
        return Math.round(p + (shiftPenalty * ch.baseProbs[ch.targetIdx]) * boostShare);
      }});
      const sum = raw.reduce((a, b) => a + b, 0) || 100;
      const norm = raw.map((v) => Math.round((v / sum) * 100));
      const diff = 100 - norm.reduce((a, b) => a + b, 0);
      norm[ch.targetIdx] = Math.max(1, norm[ch.targetIdx] + diff);
      return norm;
    }}

    function _mlpLayoutCoords() {{
      const H = mlpState.hidden;
      const inYs = [44, 70, 96, 122, 174, 200];
      const h1Nodes = H <= 16 ? 3 : (H <= 64 ? 4 : 5);
      const h1Span = h1Nodes === 3 ? [84, 120, 156] : (h1Nodes === 4 ? [62, 96, 130, 180] : [54, 86, 118, 150, 186]);
      const h2Ys = [82, 120, 158];
      const outYs = [80, 100, 120, 140, 160];
      return {{ inX: 58, inYs, h1X: 218, h1Ys: h1Span, h1Nodes, h2X: 344, h2Ys, outX: 468, outYs }};
    }}

    function _drawMlpMotionTick() {{
      const cv = document.getElementById('mlp-motion-canvas');
      const wrap = document.getElementById('mlp-hero-wrap');
      const svg = document.getElementById('mlp-sim-svg');
      const pbox = document.getElementById('mlp-photo-box');
      if (!cv || !wrap || !svg) return;
      const w = wrap.clientWidth, h = wrap.clientHeight;
      if (cv.width !== w || cv.height !== h) {{ cv.width = w; cv.height = h; }}
      const ctx = cv.getContext('2d');
      ctx.clearRect(0, 0, w, h);
      if (!mlpState.timer) return;

      const wrapRect = wrap.getBoundingClientRect();
      const svgRect = svg.getBoundingClientRect();
      const s = Math.min(svgRect.width / 760, svgRect.height / 236);
      const ox = (svgRect.left - wrapRect.left) + (svgRect.width - 760 * s) / 2;
      const oy = (svgRect.top - wrapRect.top) + (svgRect.height - 236 * s) / 2;
      const toCanvas = (sx, sy) => [ox + sx * s, oy + sy * s];

      const probs = _calcMlpProbs();
      const argmax = probs.indexOf(Math.max(...probs));
      const g = _mlpLayoutCoords();
      const isShift = mlpState.shift >= 8;
      mlpState.phaseT = (mlpState.phaseT + 0.032) % 1;
      const t = mlpState.phaseT;
      const col = isShift || mlpState.step === 4 ? '#EA4335' : (mlpState.step === 3 ? '#34A853' : (mlpState.step <= 1 ? '#F9AB00' : '#1A73E8'));

      const pts = [];
      if (mlpState.step <= 1 && pbox) {{
        const pb = pbox.getBoundingClientRect();
        const startX = pb.right - wrapRect.left + 4;
        const startY = pb.top - wrapRect.top + pb.height / 2;
        g.inYs.forEach((iy, idx) => {{
          const p = (t + idx * 0.14) % 1;
          const [tx, ty] = toCanvas(g.inX - 11, iy);
          pts.push([startX + (tx - startX) * p, startY + (ty - startY) * p, '#F9AB00']);
        }});
      }} else if (mlpState.step === 2) {{
        g.inYs.forEach((iy, ii) => {{
          const hy = g.h1Ys[ii % g.h1Ys.length];
          const p = (t + ii * 0.13) % 1;
          const [x1, y1] = toCanvas(g.inX, iy);
          const [x2, y2] = toCanvas(g.h1X, hy);
          pts.push([x1 + (x2 - x1) * p, y1 + (y2 - y1) * p, '#4285F4']);
        }});
        g.h1Ys.forEach((hy, hi) => {{
          const ky = g.h2Ys[hi % g.h2Ys.length];
          const p = (t + 0.4 + hi * 0.16) % 1;
          const [x1, y1] = toCanvas(g.h1X, hy);
          const [x2, y2] = toCanvas(g.h2X, ky);
          pts.push([x1 + (x2 - x1) * p, y1 + (y2 - y1) * p, '#1A73E8']);
        }});
      }} else if (mlpState.step === 3) {{
        g.h2Ys.forEach((ky, ki) => {{
          const p = (t + ki * 0.22) % 1;
          const [x1, y1] = toCanvas(g.h2X, ky);
          const [x2, y2] = toCanvas(g.outX, g.outYs[argmax]);
          pts.push([x1 + (x2 - x1) * p, y1 + (y2 - y1) * p, '#34A853']);
        }});
      }} else {{
        // Step 4 (Spatial Blindness): corrupted pixel signal flows Input[1..3] -> H1 -> H2 -> wrong argmax
        [1, 2, 3].forEach((ii, k) => {{
          const p = (t + k * 0.18) % 1;
          const hy = g.h1Ys[k % g.h1Ys.length];
          const ky = g.h2Ys[k % g.h2Ys.length];
          if (p < 0.36) {{
            const lp = p / 0.36;
            const [x1, y1] = toCanvas(g.inX, g.inYs[ii]);
            const [x2, y2] = toCanvas(g.h1X, hy);
            pts.push([x1 + (x2 - x1) * lp, y1 + (y2 - y1) * lp, '#EA4335']);
          }} else if (p < 0.70) {{
            const lp = (p - 0.36) / 0.34;
            const [x1, y1] = toCanvas(g.h1X, hy);
            const [x2, y2] = toCanvas(g.h2X, ky);
            pts.push([x1 + (x2 - x1) * lp, y1 + (y2 - y1) * lp, '#EA4335']);
          }} else {{
            const lp = (p - 0.70) / 0.30;
            const [x1, y1] = toCanvas(g.h2X, ky);
            const [x2, y2] = toCanvas(g.outX, g.outYs[argmax]);
            pts.push([x1 + (x2 - x1) * lp, y1 + (y2 - y1) * lp, '#C5221F']);
          }}
        }});
      }}

      pts.forEach(([px, py, cOv]) => {{
        ctx.beginPath();
        ctx.arc(px, py, 4.8, 0, Math.PI * 2);
        ctx.fillStyle = cOv || col;
        ctx.fill();
        ctx.lineWidth = 1.8;
        ctx.strokeStyle = '#FFFFFF';
        ctx.stroke();
      }});
      mlpState.raf = requestAnimationFrame(_drawMlpMotionTick);
    }}

    function _renderMlpSim() {{
      const ch = MLP_CHARS[mlpState.charIdx];
      const H = mlpState.hidden;
      const sh = mlpState.shift;
      const step = mlpState.step;
      const isShift = sh >= 8;
      const totalParams = (150528 * H + H) + (H * 32 + 32) + (32 * 5 + 5);
      const probs = _calcMlpProbs();
      const maxProb = Math.max(...probs);
      const argmax = probs.indexOf(maxProb);
      const isOk = argmax === ch.targetIdx;

      document.querySelectorAll('#mlp-char-bar [data-mchar]').forEach((b) => {{
        b.classList.toggle('outline', Number(b.dataset.mchar) !== mlpState.charIdx);
      }});
      const slHid = document.getElementById('mlp-hid-slider');
      const slSh = document.getElementById('mlp-shift-slider');
      if (slHid) slHid.value = String(H);
      if (slSh) slSh.value = String(sh);
      const vHid = document.getElementById('mlp-hid-val');
      const vSh = document.getElementById('mlp-shift-val');
      if (vHid) vHid.textContent = String(H);
      if (vSh) vSh.textContent = sh === 0 ? '0px' : `+${{sh}}px`;

      const badge = document.getElementById('mlp-vis-badge');
      if (badge) {{
        badge.textContent = isOk ? `${{ch.name}} · ${{probs[ch.targetIdx]}}% ✓` : `Meleset → ${{MLP_CLASS_NAMES[argmax]}} (${{probs[argmax]}}%)!`;
        badge.className = 'pill ' + (isOk ? (sh > 0 ? 'yellow' : 'green') : 'red');
      }}

      const pLbl = document.getElementById('mlp-photo-lbl');
      const pImg = document.getElementById('mlp-photo-img');
      const sPill = document.getElementById('mlp-slot-pill');
      const sTag = document.getElementById('mlp-slot-tag');
      if (pLbl) pLbl.textContent = `Foto ${{ch.name}} (224×224)`;
      if (pImg) {{
        pImg.src = ch.src;
        pImg.style.transform = `scale(1.18) translateX(${{sh * 0.85}}px)`;
      }}
      const matchPct = Math.max(12, 100 - (sh / 4) * 22);
      if (sPill) {{
        sPill.textContent = `Slot ${{matchPct}}%`;
        sPill.className = 'pill ' + (sh === 0 ? 'green' : (sh === 4 ? 'yellow' : 'red'));
      }}
      if (sTag) {{
        sTag.textContent = sh === 0 ? 'Slot Terlatih Pas ✓' : `Bergeser +${{sh}}px · Kena Latar!`;
        sTag.style.background = isShift ? 'rgba(197,34,31,0.88)' : 'rgba(32,33,36,0.78)';
      }}

      // Update live 1D Flatten fixed-slot pixel strip
      const fCells = document.getElementById('mlp-flat-cells');
      const fNote = document.getElementById('mlp-flat-note');
      if (fCells) {{
        const shiftSlots = Math.min(3, Math.round(sh / 4));
        const charCol = mlpState.charIdx === 0 ? '#5C7CFA' : (mlpState.charIdx === 1 ? '#4DABF7' : '#F1F3F5');
        const bgCol = '#DDD6CC';
        const basePattern = [0, 1, 1, 1, 0];
        const shiftedPattern = basePattern.map((_, i) => (i - shiftSlots >= 0 ? basePattern[i - shiftSlots] : 0));
        fCells.innerHTML = shiftedPattern.map((isObj, i) => {{
          const changed = isObj !== basePattern[i];
          return `<div style="height:14px; border-radius:3px; background:${{isObj ? charCol : bgCol}}; border:1px solid ${{changed ? '#EA4335' : '#CBD5E1'}}; display:flex; align-items:center; justify-content:center; font-family:var(--font-code); font-size:6.8px; font-weight:700; color:${{changed ? '#C5221F' : '#3C4043'}};">x${{2480 + i}}</div>`;
        }}).join('');
      }}
      if (fNote) {{
        fNote.textContent = sh === 0 ? 'Piksel Pas' : `Isi x₂₄₈₁.. geser!`;
        fNote.style.color = sh === 0 ? '#137333' : '#C5221F';
      }}

      const st2Ttl = document.getElementById('mlp-st2-ttl');
      if (st2Ttl) st2Ttl.textContent = `2. Hidden Dense (${{H}} → 32)`;
      const eq = document.getElementById('mlp-math-eq');
      if (eq) eq.innerHTML = `Bobot = <code>(150.528×${{H}}+${{H}}) + (${{H}}×32+32) + (32×5+5)</code> = <strong style="color:#C5221F;">${{totalParams.toLocaleString('id-ID')}} param</strong>`;

      const callout = document.getElementById('mlp-sim-callout');
      if (callout) {{
        callout.style.background = isOk ? '#E6F4EA' : '#FCE8E6';
        callout.style.borderColor = isOk ? '#A8DAB5' : '#F6AEA9';
        callout.innerHTML = isShift
          ? `<strong>Spatial Blindness Terbukti!</strong> Geser <code>+${{sh}}px</code> mendorong piksel figur keluar dari slot lama &rarr; <strong>${{ch.name}} jatuh ke ${{probs[ch.targetIdx]}}%</strong> (kalah dari <strong>${{MLP_CLASS_NAMES[argmax]}} ${{probs[argmax]}}%</strong>)!`
          : `<strong>Posisi Normal (${{H}} Hidden):</strong> Total <strong>${{totalParams.toLocaleString('id-ID')}} param</strong>; ${{ch.name}} menebak tepat <strong>${{probs[ch.targetIdx]}}%</strong> selama foto diam di slot tengah!`;
      }}

      const cards = [
        [document.getElementById('mlp-stage-1'), 1, 'sync-yellow'],
        [document.getElementById('mlp-stage-2'), 2, 'sync-blue'],
        [document.getElementById('mlp-stage-3'), 3, isOk ? 'sync-green' : 'sync-red'],
        [document.getElementById('mlp-stage-4'), 4, 'sync-red'],
      ];
      cards.forEach(([el, num, cls]) => {{
        if (!el) return;
        el.classList.remove('sync-on', 'sync-dim', 'sync-yellow', 'sync-blue', 'sync-green', 'sync-red');
        if (step === 0) {{
          if ((isShift && num === 4) || (!isShift && num === 2)) el.classList.add('sync-on', cls);
        }} else if (step === num) {{
          el.classList.add('sync-on', cls);
        }} else {{
          el.classList.add('sync-dim');
        }}
      }});

      const svg = document.getElementById('mlp-sim-svg');
      if (!svg) return;
      const g = _mlpLayoutCoords();
      const inLbls = ['x₁', 'x₂', 'x₃', 'x₄', 'xₙ₋₁', 'xₙ'];
      const inValsNorm = ['0.81', '0.24', '0.19', '0.26', '0.78', '0.75'];
      const inValsShft = ['0.81', '0.80', '0.79', '0.81', '0.77', '0.75'];

      const opIn = step === 0 || step === 1 || step === 4 ? 1 : 0.3;
      const opH = step === 0 || step === 2 || step === 4 ? 1 : 0.3;
      const opOut = step === 0 || step === 3 || step === 4 ? 1 : 0.3;

      let wires = '';
      g.inYs.forEach((iy, iIdx) => g.h1Ys.forEach((hy) => {{
        const mis = isShift && (iIdx >= 1 && iIdx <= 3);
        wires += `<line x1="${{g.inX}}" y1="${{iy}}" x2="${{g.h1X}}" y2="${{hy}}" stroke="${{mis ? '#F28B82' : (step === 2 ? '#4285F4' : '#CFD8DC')}}" stroke-width="${{mis || step === 2 ? 1.45 : 0.95}}" opacity="${{opH}}"/>`;
      }}));
      g.h1Ys.forEach((y1) => g.h2Ys.forEach((y2) => {{
        wires += `<line x1="${{g.h1X}}" y1="${{y1}}" x2="${{g.h2X}}" y2="${{y2}}" stroke="${{isShift ? '#F28B82' : (step === 2 ? '#1A73E8' : '#CFD8DC')}}" stroke-width="${{step === 2 || isShift ? 1.5 : 0.95}}" opacity="${{opH}}"/>`;
      }}));
      g.h2Ys.forEach((hy) => g.outYs.forEach((oy, oIdx) => {{
        const isPred = oIdx === argmax;
        wires += `<line x1="${{g.h2X}}" y1="${{hy}}" x2="${{g.outX}}" y2="${{oy}}" stroke="${{isPred ? (isOk ? '#34A853' : '#EA4335') : '#E0E3E7'}}" stroke-width="${{isPred ? 1.85 : 0.95}}" opacity="${{opOut}}"/>`;
      }}));

      const funnelBg = `<polygon points="38,32 218,48 344,68 480,66 480,174 344,172 218,196 38,212" fill="rgba(241,245,249,0.55)" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="4,3"/>`;

      const inSvg = `<rect x="38" y="31" width="40" height="181" rx="12" fill="rgba(254,247,224,0.65)" stroke="#FBBC04" stroke-width="1.2" stroke-dasharray="4,3"/>` +
        g.inYs.map((iy, idx) => {{
          const bad = isShift && (idx >= 1 && idx <= 3);
          const vTxt = isShift ? inValsShft[idx] : inValsNorm[idx];
          return `<circle cx="${{g.inX}}" cy="${{iy}}" r="10.2" fill="${{bad ? '#FCE8E6' : '#FEF7E0'}}" stroke="${{bad ? '#EA4335' : '#FBBC04'}}" stroke-width="${{step === 1 || bad ? 2.2 : 1.7}}"/><text x="${{g.inX}}" y="${{iy + 3.2}}" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" font-weight="700" fill="${{bad ? '#C5221F' : '#B06000'}}">${{inLbls[idx]}}</text>${{idx >= 1 && idx <= 3 ? `<text x="${{g.inX - 24}}" y="${{iy + 3}}" text-anchor="end" font-family="Roboto Mono" font-size="6.8" font-weight="700" fill="${{bad ? '#C5221F' : '#5F6368'}}">${{vTxt}}</text>` : ''}}`;
        }}).join('') + `<circle cx="${{g.inX}}" cy="141" r="1.8" fill="#B06000"/><circle cx="${{g.inX}}" cy="148" r="1.8" fill="#B06000"/><circle cx="${{g.inX}}" cy="155" r="1.8" fill="#B06000"/>`;

      const h1Svg = g.h1Ys.map((hy, idx) => `<circle cx="${{g.h1X}}" cy="${{hy}}" r="11" fill="#E8F0FE" stroke="#4285F4" stroke-width="${{step === 2 ? 2.3 : 1.7}}"/><text x="${{g.h1X}}" y="${{hy + 3.2}}" text-anchor="middle" font-family="Roboto Mono" font-size="7.6" font-weight="700" fill="#1A73E8">${{idx === g.h1Nodes - 1 ? 'h' + H : 'h' + (idx + 1)}}</text>`).join('') +
        (g.h1Nodes === 4 ? `<circle cx="${{g.h1X}}" cy="148" r="1.7" fill="#4285F4"/><circle cx="${{g.h1X}}" cy="155" r="1.7" fill="#4285F4"/><circle cx="${{g.h1X}}" cy="162" r="1.7" fill="#4285F4"/>` : '');
      const h2Svg = g.h2Ys.map((hy, idx) => `<circle cx="${{g.h2X}}" cy="${{hy}}" r="11" fill="#D2E3FC" stroke="#1A73E8" stroke-width="${{step === 2 ? 2.3 : 1.7}}"/><text x="${{g.h2X}}" y="${{hy + 3.2}}" text-anchor="middle" font-family="Roboto Mono" font-size="7.6" font-weight="700" fill="#174EA6">${{idx === 2 ? 'k₃₂' : 'k' + (idx + 1)}}</text>`).join('');

      const outSvg = `<rect x="452" y="65" width="296" height="110" rx="11" fill="rgba(230,244,234,0.35)" stroke="#A8DAB5" stroke-width="1.1" stroke-dasharray="4,3"/>` +
        g.outYs.map((oy, idx) => {{
          const p = probs[idx];
          const isWin = idx === argmax;
          const barCol = isWin ? (isOk ? '#34A853' : '#EA4335') : (idx === ch.targetIdx ? '#FBBC04' : '#9AA0A6');
          const pillBg = isWin ? (isOk ? '#E6F4EA' : '#FCE8E6') : '#FFFFFF';
          return `
            <circle cx="${{g.outX}}" cy="${{oy}}" r="8.2" fill="${{pillBg}}" stroke="${{barCol}}" stroke-width="${{isWin ? 2 : 1.3}}"/>
            <text x="${{g.outX}}" y="${{oy + 2.8}}" text-anchor="middle" font-family="Roboto Mono" font-size="7" font-weight="700" fill="#202124">y${{idx + 1}}</text>
            <text x="483" y="${{oy + 3}}" font-family="Poppins" font-size="8.6" font-weight="${{isWin ? 700 : 500}}" fill="${{isWin ? (isOk ? '#137333' : '#C5221F') : '#3C4043'}}">${{MLP_CLASS_NAMES[idx]}}</text>
            <rect x="538" y="${{oy - 5}}" width="164" height="10.5" rx="5.2" fill="#F1F3F4" stroke="#E0E3E7"/>
            <rect x="538" y="${{oy - 5}}" width="${{Math.max(4, (p / 100) * 164)}}" height="10.5" rx="5.2" fill="${{barCol}}"/>
            <text x="710" y="${{oy + 3}}" font-family="Roboto Mono" font-size="8.4" font-weight="700" fill="${{isWin ? (isOk ? '#137333' : '#C5221F') : '#5F6368'}}">${{p}}%</text>
          `;
        }}).join('');

      svg.innerHTML = `
        <rect x="8" y="4" width="100" height="19" rx="9.5" fill="#FEF7E0" stroke="#FBBC04"/><text x="58" y="16.5" text-anchor="middle" font-family="Poppins" font-size="8.4" font-weight="700" fill="#B06000">INPUT LAYER</text>
        <rect x="180" y="4" width="204" height="19" rx="9.5" fill="#E8F0FE" stroke="#4285F4"/><text x="282" y="16.5" text-anchor="middle" font-family="Poppins" font-size="8.4" font-weight="700" fill="#1A73E8">HIDDEN LAYERS (${{H}} → 32)</text>
        <rect x="516" y="4" width="166" height="19" rx="9.5" fill="#E6F4EA" stroke="#34A853"/><text x="599" y="16.5" text-anchor="middle" font-family="Poppins" font-size="8.4" font-weight="700" fill="#137333">OUTPUT · SOFTMAX 5 KELAS</text>
        <rect x="94" y="27" width="82" height="15" rx="7" fill="#FCE8E6" stroke="#F6AEA9" stroke-width="0.9"/><text x="135" y="37" text-anchor="middle" font-family="Roboto Mono" font-size="7.4" font-weight="700" fill="#C5221F">${{(150528 * H / 1e6).toFixed(2)}}M bobot</text>
        ${{funnelBg}}
        <rect x="182" y="44" width="198" height="154" rx="12" fill="rgba(232,240,254,0.28)" stroke="${{step === 2 ? '#1A73E8' : '#8AB4F8'}}" stroke-width="${{step === 2 ? 2.1 : 1.2}}" stroke-dasharray="5,3"/>
        ${{wires}}
        <g opacity="${{opIn}}">${{inSvg}}</g>
        <g opacity="${{opH}}">${{h1Svg}}${{h2Svg}}</g>
        <g opacity="${{opOut}}">${{outSvg}}</g>
        <text x="58" y="226" text-anchor="middle" font-family="Poppins" font-size="8.6" font-weight="700" fill="#B06000">150.528 Piksel 1D</text>
        <text x="282" y="226" text-anchor="middle" font-family="Poppins" font-size="8.6" font-weight="700" fill="#1A73E8">Corong: 150.528 ≫ ${{H}} → 32 → 5</text>
        <text x="599" y="226" text-anchor="middle" font-family="Poppins" font-size="8.6" font-weight="700" fill="${{isOk ? '#137333' : '#C5221F'}}">Prediksi: ${{MLP_CLASS_NAMES[argmax]}} (${{probs[argmax]}}%)</text>
      `;
    }}

    function setMlpSim(cfg) {{
      _stopMlpTimer();
      if (typeof cfg === 'string') {{
        mlpState.charIdx = 1; mlpState.hidden = cfg === '4_norm' ? 4 : 64;
        mlpState.shift = cfg === '64_shift' ? 8 : 0; mlpState.step = 0;
      }} else if (cfg && typeof cfg === 'object') {{
        Object.assign(mlpState, cfg);
      }}
      _renderMlpSim();
    }}
    function selectMlpChar(idx) {{ _stopMlpTimer(); mlpState.charIdx = idx; _renderMlpSim(); }}
    function onMlpSlider() {{
      _stopMlpTimer();
      const shEl = document.getElementById('mlp-hid-slider');
      const ssEl = document.getElementById('mlp-shift-slider');
      if (shEl) mlpState.hidden = parseInt(shEl.value, 10) || 64;
      if (ssEl) mlpState.shift = parseInt(ssEl.value, 10) || 0;
      mlpState.step = mlpState.shift >= 8 ? 4 : 0;
      _renderMlpSim();
    }}
    function nudgeMlpShift(delta) {{
      _stopMlpTimer();
      mlpState.shift = Math.max(0, Math.min(16, mlpState.shift + delta));
      mlpState.step = mlpState.shift >= 8 ? 4 : 0;
      _renderMlpSim();
    }}
    function jumpMlpStep(num) {{
      _stopMlpTimer();
      if (num === 4) {{ mlpState.shift = mlpState.shift >= 8 ? 0 : 8; mlpState.step = mlpState.shift >= 8 ? 4 : 0; }}
      else {{ mlpState.step = mlpState.step === num ? 0 : num; }}
      _renderMlpSim();
    }}
    function stepMlpSim() {{
      _stopMlpTimer();
      if (mlpState.step < 3) {{ mlpState.step += 1; }}
      else if (mlpState.shift < 8) {{ mlpState.shift = 8; mlpState.step = 4; }}
      else {{ mlpState.shift = 0; mlpState.step = 1; }}
      _renderMlpSim();
    }}
    function playMlpSim() {{
      if (mlpState.timer) {{ _stopMlpTimer(); _renderMlpSim(); return; }}
      const pb = document.getElementById('mlp-play-btn');
      if (pb) {{ pb.innerHTML = '&#9632; Stop'; pb.classList.add('playing'); }}
      mlpState.shift = 0; mlpState.step = 1; mlpState.phaseT = 0;
      _renderMlpSim();
      mlpState.raf = requestAnimationFrame(_drawMlpMotionTick);
      mlpState.timer = setInterval(() => {{
        if (mlpState.step < 3 && mlpState.shift === 0) {{ mlpState.step += 1; _renderMlpSim(); }}
        else if (mlpState.shift === 0) {{ mlpState.shift = 8; mlpState.step = 4; _renderMlpSim(); }}
        else {{ _stopMlpTimer(); mlpState.step = 0; _renderMlpSim(); }}
      }}, 1400);
    }}
    function resetMlpSim() {{ _stopMlpTimer(); mlpState.charIdx = 1; mlpState.hidden = 64; mlpState.shift = 0; mlpState.step = 0; _renderMlpSim(); }}

    // =========================================================================
    // SIMULATOR #2 (Slide 13): CNN Klasik (Real Elsa 16x16 + Sliding Kernel 3x3)
    // =========================================================================
    const cnnState = {{ filter: 'sobel_v', stride: 1, pad: 0, scanIdx: 92, timer: null }};
    const CNN_KERNELS = {{
      sobel_v: [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
      sobel_h: [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
      sharp:   [[0, -1, 0], [-1, 5, -1], [0, -1, 0]],
    }};
    function _stopCnnTimer() {{
      if (cnnState.timer) {{ clearInterval(cnnState.timer); cnnState.timer = null; }}
      const pb = document.getElementById('cnn-play-btn');
      if (pb) {{ pb.innerHTML = '&#9654; Play 3×3'; pb.classList.remove('playing'); }}
    }}

    function drawMatrixCanvas(canvasId, mat, modeColor, boxSpec) {{
      const cv = document.getElementById(canvasId);
      if (!cv || !mat.length) return;
      const ctx = cv.getContext('2d');
      const h = mat.length, w = mat[0].length;
      const cw = cv.width, ch = cv.height;
      ctx.clearRect(0, 0, cw, ch);
      let maxV = 0.001;
      for (let r = 0; r < h; r++) for (let c = 0; c < w; c++) maxV = Math.max(maxV, mat[r][c]);
      const cellW = cw / w, cellH = ch / h;
      const padFrame = boxSpec && boxSpec.padFrame ? boxSpec.padFrame : 0;
      const dimAfter = boxSpec && typeof boxSpec.dimAfter === 'number' ? boxSpec.dimAfter : -1;
      for (let r = 0; r < h; r++) {{
        for (let c = 0; c < w; c++) {{
          const isPadCell = padFrame > 0 && (r < padFrame || c < padFrame || r >= h - padFrame || c >= w - padFrame);
          const idx = r * w + c;
          const dimmed = dimAfter >= 0 && idx > dimAfter;
          if (isPadCell) {{
            ctx.fillStyle = '#E8F0FE';
          }} else {{
            const norm = Math.max(0, Math.min(1, modeColor === 'gray' ? mat[r][c] : mat[r][c] / maxV));
            if (modeColor === 'gray') {{
              const v = Math.round(norm * 255);
              ctx.fillStyle = `rgb(${{v}},${{v}},${{v}})`;
            }} else if (modeColor === 'blue') {{
              const mult = dimmed ? 0.28 : 1.0;
              ctx.fillStyle = `rgb(${{Math.round(255 - norm * 220 * mult)}},${{Math.round(255 - norm * 145 * mult)}},${{Math.round(255 - norm * 10 * mult)}})`;
            }} else {{
              ctx.fillStyle = `rgb(${{Math.round(255 - norm * 205)}},${{Math.round(255 - norm * 85)}},${{Math.round(255 - norm * 185)}})`;
            }}
          }}
          ctx.fillRect(Math.floor(c * cellW), Math.floor(r * cellH), Math.ceil(cellW), Math.ceil(cellH));
        }}
      }}
      if (padFrame > 0) {{
        ctx.save();
        ctx.strokeStyle = '#4285F4';
        ctx.setLineDash([4, 3]);
        ctx.lineWidth = 1.6;
        ctx.strokeRect(padFrame * cellW, padFrame * cellH, (w - 2 * padFrame) * cellW, (h - 2 * padFrame) * cellH);
        ctx.restore();
      }}
      if (boxSpec && typeof boxSpec.r0 === 'number') {{
        const {{ r0, c0, rows, cols, stroke, fill }} = boxSpec;
        const x = Math.max(0, c0 * cellW);
        const y = Math.max(0, r0 * cellH);
        const bw = Math.min(cw - x, cols * cellW);
        const bh = Math.min(ch - y, rows * cellH);
        if (fill) {{ ctx.fillStyle = fill; ctx.fillRect(x, y, bw, bh); }}
        ctx.strokeStyle = stroke;
        ctx.lineWidth = 3;
        ctx.strokeRect(x + 1.5, y + 1.5, Math.max(2, bw - 3), Math.max(2, bh - 3));
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

      const totCells = outN * outN;
      if (cnnState.scanIdx < 0) cnnState.scanIdx = Math.floor(outN * 0.42) * outN + Math.floor(outN * 0.55);
      const idx = cnnState.scanIdx % totCells;
      const fr = Math.floor(idx / outN);
      const fc = idx % outN;
      const inR = fr * stride;
      const inC = fc * stride;
      const pr = Math.min(poolN - 1, Math.floor(fr / 2));
      const pc = Math.min(poolN - 1, Math.floor(fc / 2));

      const inBox = {{ r0: inR, c0: inC, rows: 3, cols: 3, stroke: '#FBBC04', fill: 'rgba(251,188,4,0.25)', padFrame: pad }};
      const fmBox = {{ r0: fr, c0: fc, rows: 1, cols: 1, stroke: '#EA4335', fill: 'rgba(234,67,53,0.26)', dimAfter: cnnState.timer ? idx : -1 }};
      const plBox = {{ r0: pr, c0: pc, rows: 1, cols: 1, stroke: '#1A73E8', fill: 'rgba(26,115,232,0.22)' }};

      drawMatrixCanvas('cnn-can-in', padded, 'gray', inBox);
      drawMatrixCanvas('cnn-can-fm', fmap, 'blue', fmBox);
      drawMatrixCanvas('cnn-can-pool', pool, 'green', plBox);

      const inDim = document.getElementById('cnn-in-dim');
      const lIn = document.getElementById('cnn-lbl-in');
      const kShape = document.getElementById('cnn-kpi-shape');
      const lFm = document.getElementById('cnn-lbl-fm');
      const lPool = document.getElementById('cnn-lbl-pool');
      const kTxt = document.getElementById('cnn-kernel-txt');
      const sBox = document.getElementById('cnn-sim-size');
      const fBox = document.getElementById('cnn-sim-formula');
      const kNames = {{
        sobel_v: 'Kernel Sobel Vertikal <code>3×3</code> + ReLU (&gt;0 menyala biru)',
        sobel_h: 'Kernel Sobel Horizontal <code>3×3</code> + ReLU (&gt;0 menyala biru)',
        sharp:   'Kernel Pertajam <code>3×3</code> + ReLU (&gt;0 menyala biru)',
      }};
      if (inDim) inDim.textContent = pad ? '16×16 + Pad 1 = 18×18' : '16×16';
      if (lIn) lIn.textContent = `Jendela 3×3 di (${{inR}}, ${{inC}}) · Stride ${{stride}}`;
      if (kShape) kShape.textContent = `FM: ${{outN}}×${{outN}} → Pool: ${{poolN}}×${{poolN}}`;
      if (lFm) lFm.textContent = `${{outN}}×${{outN}} (${{outN * outN}} langkah geser)`;
      if (lPool) lPool.textContent = `${{poolN}}×${{poolN}} → ${{poolN * poolN}} ciri ke Softmax`;
      if (kTxt) kTxt.innerHTML = kNames[cnnState.filter] || '';
      if (sBox) sBox.innerHTML = `<strong>Rumus Ukuran:</strong> (16 &minus; 3 + 2×${{pad}}) / ${{stride}} + 1 = <strong>${{outN}}×${{outN}}</strong> &rarr; Pool <strong>${{poolN}}×${{poolN}}</strong> (10 param)`;
      if (fBox) fBox.innerHTML = `<strong>Jendela 3×3 &#8594; Sel (${{fr}},${{fc}}):</strong> Geser <code>(${{inR}},${{inC}})</code> &#8594; ReLU = <strong><code>${{fmap[fr][fc].toFixed(2)}}</code></strong> &#8594; Pool (${{pr}},${{pc}})`;
    }}
    function _initCnnCanvasClicks() {{
      const cvIn = document.getElementById('cnn-can-in');
      const cvFm = document.getElementById('cnn-can-fm');
      if (cvIn && !cvIn.dataset.bound) {{
        cvIn.dataset.bound = '1';
        cvIn.addEventListener('click', (e) => {{
          _stopCnnTimer();
          const rect = cvIn.getBoundingClientRect();
          const pad = cnnState.pad, stride = cnnState.stride;
          const nP = 16 + 2 * pad;
          const outN = Math.floor((16 - 3 + 2 * pad) / stride) + 1;
          const c = Math.floor(((e.clientX - rect.left) / rect.width) * nP);
          const r = Math.floor(((e.clientY - rect.top) / rect.height) * nP);
          const fr = Math.max(0, Math.min(outN - 1, Math.round((r - 1) / stride)));
          const fc = Math.max(0, Math.min(outN - 1, Math.round((c - 1) / stride)));
          cnnState.scanIdx = fr * outN + fc;
          renderCnnSim();
        }});
      }}
      if (cvFm && !cvFm.dataset.bound) {{
        cvFm.dataset.bound = '1';
        cvFm.addEventListener('click', (e) => {{
          _stopCnnTimer();
          const rect = cvFm.getBoundingClientRect();
          const outN = Math.floor((16 - 3 + 2 * cnnState.pad) / cnnState.stride) + 1;
          const fc = Math.max(0, Math.min(outN - 1, Math.floor(((e.clientX - rect.left) / rect.width) * outN)));
          const fr = Math.max(0, Math.min(outN - 1, Math.floor(((e.clientY - rect.top) / rect.height) * outN)));
          cnnState.scanIdx = fr * outN + fc;
          renderCnnSim();
        }});
      }}
    }}
    function setCnnState(patch) {{ _stopCnnTimer(); Object.assign(cnnState, patch); renderCnnSim(); }}
    function toggleCnnStride() {{ _stopCnnTimer(); cnnState.stride = cnnState.stride === 1 ? 2 : 1; renderCnnSim(); }}
    function toggleCnnPad() {{ _stopCnnTimer(); cnnState.pad = cnnState.pad === 0 ? 1 : 0; renderCnnSim(); }}
    function stepCnnSim() {{
      _stopCnnTimer();
      const outN = Math.floor((16 - 3 + 2 * cnnState.pad) / cnnState.stride) + 1;
      cnnState.scanIdx = (cnnState.scanIdx + 1) % (outN * outN);
      renderCnnSim();
    }}
    function playCnnSim() {{
      if (cnnState.timer) {{ _stopCnnTimer(); renderCnnSim(); return; }}
      const pb = document.getElementById('cnn-play-btn');
      if (pb) {{ pb.innerHTML = '&#9632; Stop'; pb.classList.add('playing'); }}
      const outN = Math.floor((16 - 3 + 2 * cnnState.pad) / cnnState.stride) + 1;
      cnnState.scanIdx = Math.floor(outN * 0.25) * outN;
      renderCnnSim();
      cnnState.timer = setInterval(() => {{
        const curOut = Math.floor((16 - 3 + 2 * cnnState.pad) / cnnState.stride) + 1;
        cnnState.scanIdx = (cnnState.scanIdx + 1) % (curOut * curOut);
        renderCnnSim();
      }}, 140);
    }}
    function resetCnnSim() {{ _stopCnnTimer(); cnnState.filter = 'sobel_v'; cnnState.stride = 1; cnnState.pad = 0; cnnState.scanIdx = 92; renderCnnSim(); }}

    // =========================================================================
    // SIMULATOR #3 (Slide 19): ResNet Signal Flow & GAP (Play Backprop L20->L1)
    // =========================================================================
    const resState = {{ mode: 'plain', step: -1, timer: null }};
    function _stopResTimer() {{
      if (resState.timer) {{ clearInterval(resState.timer); resState.timer = null; }}
      const pb = document.getElementById('res-play-btn');
      if (pb) {{ pb.innerHTML = '&#9654; Play Backprop'; pb.classList.remove('playing'); }}
    }}
    function _renderResnetSim() {{
      const mode = resState.mode;
      const step = resState.step;
      document.querySelectorAll('#sim-resnet-bar [data-res]').forEach((b) => {{
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
      const tone = isRes ? 'sync-green' : 'sync-red';
      if (sBlk) {{
        sBlk.classList.remove('sync-on', 'sync-dim', 'sync-green', 'sync-red');
        if (step < 0 || step <= 3) sBlk.classList.add('sync-on', tone);
        else sBlk.classList.add('sync-dim');
      }}
      if (sGap) {{
        sGap.classList.remove('sync-on', 'sync-dim', 'sync-green', 'sync-red');
        if (step < 0 || step === 4) sGap.classList.add('sync-on', tone);
        else sGap.classList.add('sync-dim');
      }}
      if (blkPill) {{ blkPill.textContent = isRes ? 'AKTIF (+x)' : 'TANPA +x'; blkPill.className = 'pill ' + (isRes ? 'green' : 'red'); }}
      if (gapPill) {{ gapPill.textContent = isRes ? 'GAP 10.245' : 'FLATTEN 51.38M'; gapPill.className = 'pill ' + (isRes ? 'green' : 'red'); }}

      const vals = isRes ? [100, 96, 92, 89, 86] : [100, 58, 30, 14, 7];
      const names = ['Layer 20', 'Layer 15', 'Layer 10', 'Layer 5', 'Layer 1'];
      if (bars) {{
        bars.innerHTML = vals.map((v, i) => `
          <div class="signal-bar-row ${{step === i ? 'bar-active' : ''}}">
            <span style="font-family:var(--font-code); font-weight:700; color:#3C4043;">${{names[i]}}</span>
            <div class="signal-track"><div class="signal-fill" style="width:${{step >= 0 && i > step ? 0 : v}}%; background:${{isRes ? '#34A853' : (v < 25 ? '#EA4335' : '#FBBC04')}};"></div></div>
            <span style="font-family:var(--font-code); font-weight:700; color:${{isRes ? '#137333' : '#C5221F'}};">${{step >= 0 && i > step ? '…' : v + '%'}}</span>
          </div>
        `).join('');
      }}
      if (archCap) archCap.textContent = isRes
        ? 'Alur ResNet (+x Skip Bridge + GAP Head):'
        : 'Alur Plain Deep Net (Seri Polos + Flatten Head):';
      const pulseX = step >= 0 ? [365, 280, 195, 130, 62][step] : -99;
      if (archSvg) {{
        const pulseDot = step >= 0
          ? `<circle cx="${{pulseX}}" cy="${{isRes && step === 2 ? 16 : 57}}" r="7.5" fill="#FBBC04" stroke="#202124" stroke-width="2"/>`
          : '';
        archSvg.innerHTML = (isRes ? `
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
        `) + pulseDot;
      }}
      if (kGrad) kGrad.textContent = isRes ? 'Sinyal L1: 86% (Kuat!)' : 'Sinyal L1: 7% (Macet)';
      if (kHead) kHead.textContent = isRes ? 'Head: GAP 10.245' : 'Head: Flatten 51.38M';
      if (pill) {{
        pill.textContent = step >= 0 ? `Backprop: ${{names[step]}} (${{vals[step]}}%)` : (isRes ? 'Skip + GAP Aktif ✓' : 'Vanishing Gradient!');
        pill.className = 'pill ' + (isRes ? 'green' : 'red');
      }}
      if (callout) callout.innerHTML = step >= 0
        ? `<strong>Backprop di ${{names[step]}}:</strong> Sinyal gradien tersisa <strong>${{vals[step]}}%</strong> ${{isRes ? '(terbantu jalan pintas +x!)' : '(melemah setiap melewati tumpukan layer!)'}}.`
        : (isRes
            ? '<strong>ResNet Berhasil!</strong> Lewat jembatan <code>+ x</code>, gradien tidak habis di tengah jalan sehingga lapisan awal tetap belajar tepi gambar Frozen dengan tajam!'
            : 'Tanpa jalur pintas, sinyal belajar yang dikirim dari Loss di Layer 20 habis terserap di tengah jalan sebelum mencapai Layer 1!');
      if (bDesc) bDesc.innerHTML = isRes
        ? 'Mode aktif: <code>Output = F(x) + x</code>! Layer cukup belajar koreksi kecil sementara data awal mengalir utuh lewat jembatan sehingga gradien Layer 1 tetap <strong>86%</strong>.'
        : 'Setiap blok saat ini hanya menyalurkan jalur utama konvolusi <code>F(x)</code> tanpa penyambung <code>+ x</code>. Saat backprop, sinyal gradien menyusut hingga tinggal <strong>7%</strong> di Layer 1.';
      if (gDesc) gDesc.innerHTML = isRes
        ? 'Di ujung ResNet50 (tensor <code>7×7×2048</code>), <strong>GAP</strong> meringkas tiap peta fitur menjadi rata-rata tunggal (<code>2.048</code> angka) sehingga parameter head turun dari <code>51,38 juta</code> ke <code>10.245</code>!'
        : 'Dengan cara lama (<code>Flatten &#8594; Dense(512)</code>), tensor <code>7×7×2048</code> diratakan menjadi <code>100.352</code> angka dan menghabiskan <code>51.380.229</code> parameter kepala!';
    }}
    function setResnetSim(mode) {{ _stopResTimer(); resState.mode = mode; resState.step = -1; _renderResnetSim(); }}
    function stepResSim() {{
      _stopResTimer();
      if (resState.step < 4) resState.step += 1;
      else {{ resState.mode = resState.mode === 'plain' ? 'resnet' : 'plain'; resState.step = 0; }}
      _renderResnetSim();
    }}
    function playResSim() {{
      if (resState.timer) {{ _stopResTimer(); return; }}
      const pb = document.getElementById('res-play-btn');
      if (pb) {{ pb.innerHTML = '&#9632; Stop'; pb.classList.add('playing'); }}
      if (resState.step < 0 || resState.step >= 4) resState.step = 0;
      _renderResnetSim();
      resState.timer = setInterval(() => {{
        if (resState.step < 4) {{ resState.step += 1; _renderResnetSim(); }}
        else if (resState.mode !== 'resnet') {{ resState.mode = 'resnet'; resState.step = 0; _renderResnetSim(); }}
        else {{ _stopResTimer(); resState.step = -1; _renderResnetSim(); }}
      }}, 950);
    }}
    function resetResSim() {{ _stopResTimer(); resState.mode = 'plain'; resState.step = -1; _renderResnetSim(); }}

    // =========================================================================
    // SIMULATOR #4 (Slide 25): MobileNetV2 Conv Biasa vs Inverted Residual (Play)
    // =========================================================================
    const mobState = {{ mode: 'standard', step: 0, timer: null }};
    function _stopMobTimer() {{
      if (mobState.timer) {{ clearInterval(mobState.timer); mobState.timer = null; }}
      const pb = document.getElementById('mob-play-btn');
      if (pb) {{ pb.innerHTML = '&#9654; Play Aliran Blok'; pb.classList.remove('playing'); }}
    }}
    function _renderMobSim() {{
      const mode = mobState.mode;
      const step = mobState.step;
      document.querySelectorAll('#sim-mob-bar [data-mob]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.mob !== mode);
      }});
      const isMob = mode === 'mobilenetv2';
      const svg = document.getElementById('mob-sim-svg');
      const kOps = document.getElementById('mob-kpi-ops');
      const kSave = document.getElementById('mob-kpi-save');
      const ttl = document.getElementById('mob-vis-ttl');
      const fBox = document.getElementById('mob-sim-formula');
      const stages = [
        document.getElementById('mob-stage-1'),
        document.getElementById('mob-stage-2'),
        document.getElementById('mob-stage-3'),
      ];
      const p1 = document.getElementById('mob-p1');
      const p2 = document.getElementById('mob-p2');
      const p3 = document.getElementById('mob-p3');
      const d1 = document.getElementById('mob-st1-desc');
      const d2 = document.getElementById('mob-st2-desc');
      const d3 = document.getElementById('mob-st3-desc');
      stages.forEach((e, idx) => {{
        if (!e) return;
        e.classList.remove('sync-on', 'sync-dim', 'sync-green', 'sync-red', 'sync-yellow', 'sync-blue');
        if (step === 0) e.classList.add('sync-on', isMob ? 'sync-green' : 'sync-red');
        else if (idx + 1 === step) e.classList.add('sync-on', step === 2 && isMob ? 'sync-yellow' : (isMob ? 'sync-green' : 'sync-red'));
        else e.classList.add('sync-dim');
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
      if (kSave) kSave.textContent = isMob ? 'Hemat 8.4×!' : 'Efisiensi: 1×';
      const stepTag = step > 0 ? ` [Langkah ${{step}}/3]` : '';
      if (ttl) ttl.textContent = (isMob ? 'Blok Inverted Residual: 32 → Expand 192 → DW 3×3 → Linear 32 (+Skip)' : 'Pipa Konvolusi Standar 56×56×64 → 128 Channel') + stepTag;
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
        const o1 = step === 0 || step === 1 ? 1 : 0.32;
        const o2 = step === 0 || step === 2 ? 1 : 0.32;
        const o3 = step === 0 || step === 3 ? 1 : 0.32;
        svg.innerHTML = `
          <g opacity="${{o3}}">
            <path d="M 52 146 Q 220 204 388 146" fill="none" stroke="#34A853" stroke-width="${{step === 3 ? 3.4 : 2.6}}" stroke-dasharray="5,4"/>
            <text x="220" y="198" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#137333">Skip Connection (+x langsung antar bottleneck sempit)</text>
          </g>
          <rect x="14" y="76" width="72" height="66" rx="9" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
          <text x="50" y="106" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#1A73E8">32 ch</text>
          <text x="50" y="122" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="#174EA6">Sempit</text>
          <line x1="86" y1="109" x2="108" y2="109" stroke="#3C4043" stroke-width="2"/>
          <g opacity="${{o1}}">
            <rect x="108" y="34" width="94" height="140" rx="10" fill="#E6F4EA" stroke="#34A853" stroke-width="${{step === 1 ? 3.5 : 2.2}}"/>
            <text x="155" y="92" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#137333">Expand 1×1</text>
            <text x="155" y="110" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#137333">192 ch (6×)</text>
            <text x="155" y="128" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="#5F6368">+ ReLU6</text>
          </g>
          <line x1="202" y1="109" x2="222" y2="109" stroke="#3C4043" stroke-width="2"/>
          <g opacity="${{o2}}">
            <rect x="222" y="34" width="96" height="140" rx="10" fill="#FEF7E0" stroke="#FBBC04" stroke-width="${{step === 2 ? 3.5 : 2.2}}"/>
            <text x="270" y="92" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#B06000">DW 3×3</text>
            <text x="270" y="110" text-anchor="middle" font-family="Roboto" font-size="9.2" fill="#B06000">1 filter / kanal</text>
            <text x="270" y="128" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="#137333">Super ringan!</text>
          </g>
          <line x1="318" y1="109" x2="340" y2="109" stroke="#3C4043" stroke-width="2"/>
          <g opacity="${{o3}}">
            <rect x="340" y="76" width="88" height="66" rx="9" fill="#E8F0FE" stroke="#1A73E8" stroke-width="${{step === 3 ? 3.5 : 2}}"/>
            <text x="384" y="104" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#1A73E8">Project 32</text>
            <text x="384" y="120" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#C5221F">Linear (no ReLU)</text>
          </g>
        `;
      }}
    }}
    function setMobSim(mode) {{ _stopMobTimer(); mobState.mode = mode; mobState.step = 0; _renderMobSim(); }}
    function stepMobSim() {{
      _stopMobTimer();
      mobState.mode = 'mobilenetv2';
      mobState.step = mobState.step < 3 ? mobState.step + 1 : 0;
      _renderMobSim();
    }}
    function playMobSim() {{
      if (mobState.timer) {{ _stopMobTimer(); return; }}
      const pb = document.getElementById('mob-play-btn');
      if (pb) {{ pb.innerHTML = '&#9632; Stop'; pb.classList.add('playing'); }}
      mobState.mode = 'mobilenetv2';
      mobState.step = 1;
      _renderMobSim();
      mobState.timer = setInterval(() => {{
        if (mobState.step < 3) {{ mobState.step += 1; _renderMobSim(); }}
        else {{ _stopMobTimer(); mobState.step = 0; _renderMobSim(); }}
      }}, 1150);
    }}
    function resetMobSim() {{ _stopMobTimer(); mobState.mode = 'standard'; mobState.step = 0; _renderMobSim(); }}

    // =========================================================================
    // SIMULATOR #5 (Slide 29): EfficientNet Compound Scaling & SE Attention
    // =========================================================================
    const effState = {{ scale: 'b0', se: false, step: 0, timer: null }};
    const EFF_SCALES = {{
      b0: {{ res: 224, depth: '1.0×', width: '1.0×', meta: '{r_eff["total_params"]/1e6:.2f}M Param · {r_eff["est_size_mb"]} MB' }},
      b1: {{ res: 240, depth: '1.1×', width: '1.0×', meta: '~6.5M Param · 24.8 MB' }},
      b2: {{ res: 260, depth: '1.2×', width: '1.1×', meta: '~7.8M Param · 29.8 MB' }},
    }};
    function _stopEffTimer() {{
      if (effState.timer) {{ clearInterval(effState.timer); effState.timer = null; }}
      const pb = document.getElementById('eff-play-btn');
      if (pb) {{ pb.innerHTML = '&#9654; Play SE Gate'; pb.classList.remove('playing'); }}
    }}

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
        btnSe.textContent = effState.se ? 'SE: ON ✓' : 'SE: OFF';
        btnSe.classList.toggle('outline', !effState.se);
      }}
      if (sSc) {{
        sSc.classList.remove('sync-on', 'sync-dim', 'sync-green', 'sync-blue');
        if (effState.step === 0 || effState.step === 1) sSc.classList.add('sync-on', effState.scale !== 'b0' ? 'sync-green' : 'sync-blue');
        else sSc.classList.add('sync-dim');
      }}
      if (sSe) {{
        sSe.classList.remove('sync-on', 'sync-dim', 'sync-green', 'sync-red', 'sync-yellow');
        if (effState.step === 0 || effState.step >= 2) sSe.classList.add('sync-on', effState.se ? 'sync-green' : (effState.step === 2 ? 'sync-yellow' : 'sync-red'));
        else sSe.classList.add('sync-dim');
      }}
      if (p1) {{ p1.textContent = effState.scale.toUpperCase() + (effState.scale === 'b0' ? ' · BASELINE' : ' · SCALED'); p1.className = 'pill ' + (effState.scale === 'b0' ? 'blue' : 'green'); }}
      if (p2) {{ p2.textContent = effState.se ? 'SE ON ✓' : (effState.step === 2 ? 'SQUEEZE...' : 'SE OFF'); p2.className = 'pill ' + (effState.se ? 'green' : (effState.step === 2 ? 'yellow' : 'red')); }}

      if (kMeta) kMeta.textContent = sp.meta;
      if (scDesc) scDesc.innerHTML = `Skala <code>${{effState.scale.toUpperCase()}}</code>: resolusi <code>${{sp.res}}×${{sp.res}}</code>, depth <code>${{sp.depth}}</code>, width <code>${{sp.width}}</code> &#8594; <code>${{sp.meta}}</code>.`;
      if (sePill) {{
        sePill.textContent = effState.se ? 'SE ON (Fokus Karakter!)' : (effState.step === 2 ? 'Tahap Squeeze (GAP)' : 'SE OFF (Bobot Rata)');
        sePill.style.background = effState.se ? '#E6F4EA' : (effState.step === 2 ? '#FEF7E0' : '#F1F3F4');
        sePill.style.color = effState.se ? '#137333' : (effState.step === 2 ? '#B06000' : '#5F6368');
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
          <rect x="8" y="${{41 - (boxW-28)/2}}" width="${{boxW}}" height="${{boxW-28}}" rx="6" fill="#F3E8FD" stroke="#8E24AA" stroke-width="${{effState.step === 1 ? 2.8 : 1.8}}"/>
          <text x="${{8 + boxW/2}}" y="38" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#681DA8">${{effState.scale.toUpperCase()}} Input</text>
          <text x="${{8 + boxW/2}}" y="51" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" fill="#5F6368">${{sp.res}}×${{sp.res}}</text>
          <text x="${{boxW + 22}}" y="45" text-anchor="middle" font-family="Poppins" font-size="13" fill="#5F6368">&#8594;</text>
          <rect x="${{boxW + 34}}" y="18" width="114" height="46" rx="7" fill="#E8F0FE" stroke="#4285F4"/>
          <text x="${{boxW + 91}}" y="37" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#1A73E8">Blok MBConv</text>
          <text x="${{boxW + 91}}" y="51" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#174EA6">D:${{sp.depth}} · W:${{sp.width}}</text>
          <text x="${{boxW + 160}}" y="45" text-anchor="middle" font-family="Poppins" font-size="13" fill="${{seCol}}">&#8594;</text>
          <rect x="${{boxW + 172}}" y="14" width="154" height="54" rx="8" fill="${{seBg}}" stroke="${{seCol}}" stroke-width="${{effState.step >= 2 ? 2.8 : 1.8}}"/>
          <text x="${{boxW + 249}}" y="34" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="${{seCol}}">SE Gate ${{effState.se ? 'AKTIF' : 'OFF'}}</text>
          <text x="${{boxW + 249}}" y="49" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="${{seCol}}">${{effState.se ? 'Elsa ×0.95 | Latar ×0.16' : 'Semua bobot rata 0.55'}}</text>
        `;
      }}
      if (callout) callout.innerHTML = effState.se
        ? '<strong>SE Attention Aktif ({r_eff["se_multiply_layers"]} blok)!</strong> Jaringan meredam bobot kanal latar ramai ke <code>0.10–0.16</code> dan membesarkan ciri Elsa menjadi <code>0.88–0.95</code>.'
        : (effState.step === 2 ? '<strong>Tahap Squeeze (GAP):</strong> Meringkas tiap peta kanal menjadi 1 skor ringkasan sebelum diberi bobot penting.' : 'Tanpa SE Attention, semua kanal (termasuk latar dinding dan cangkir di belakang Elsa) mendapat bobot setara.');
      if (seDesc) seDesc.innerHTML = effState.se
        ? '<code>Output = Channel × Bobot_SE</code> sudah aktif &mdash; fitur gaun Elsa dikuatkan, latar ramai diredam!'
        : 'Klik <strong>SE: ON</strong> atau <strong>&#9654; Play SE Gate</strong> untuk melihat kanal latar diredam otomatis agar fokus ke gaun biru Elsa!';
    }}
    function setEffState(patch) {{ _stopEffTimer(); effState.step = 0; Object.assign(effState, patch); renderEffSim(); }}
    function toggleEffSe() {{ _stopEffTimer(); effState.step = 0; effState.se = !effState.se; renderEffSim(); }}
    function stepEffSim() {{
      _stopEffTimer();
      effState.step = (effState.step % 3) + 1;
      if (effState.step === 1) {{ effState.scale = 'b1'; effState.se = false; }}
      else if (effState.step === 2) {{ effState.se = false; }}
      else if (effState.step === 3) {{ effState.se = true; }}
      renderEffSim();
    }}
    function playEffSim() {{
      if (effState.timer) {{ _stopEffTimer(); return; }}
      const pb = document.getElementById('eff-play-btn');
      if (pb) {{ pb.innerHTML = '&#9632; Stop'; pb.classList.add('playing'); }}
      effState.step = 1; effState.scale = 'b1'; effState.se = false;
      renderEffSim();
      effState.timer = setInterval(() => {{
        if (effState.step === 1) {{ effState.step = 2; effState.se = false; renderEffSim(); }}
        else if (effState.step === 2) {{ effState.step = 3; effState.se = true; renderEffSim(); }}
        else {{ _stopEffTimer(); effState.step = 0; renderEffSim(); }}
      }}, 1150);
    }}
    function resetEffSim() {{ _stopEffTimer(); effState.scale = 'b0'; effState.se = false; effState.step = 0; renderEffSim(); }}

    function _stopAllP03Timers() {{ _stopS06Timer(); _stopS11Timer(); _stopMlpTimer(); _stopCnnTimer(); _stopResTimer(); _stopMobTimer(); _stopEffTimer(); }}

    // =========================================================================
    // SLIDE 11 (#2.1 CNN Klasik 4-Step Interactive Pipeline Explorer)
    // =========================================================================
    const s11State = {{ step: 0, timer: null }};
    function _stopS11Timer() {{
      if (s11State.timer) {{ clearInterval(s11State.timer); s11State.timer = null; }}
      const pb = document.getElementById('s11-play-btn');
      if (pb) {{ pb.innerHTML = '&#9654; Play 4 Tahap'; pb.classList.remove('playing'); }}
    }}
    function _renderS11Canvases() {{
      if (typeof drawMatrixCanvas !== 'function' || typeof P03_ELSA_16 === 'undefined') return;
      const K = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]];
      const fm = [];
      for (let r = 0; r < 14; r++) {{
        const row = [];
        for (let c = 0; c < 14; c++) {{
          let s = 0;
          for (let kr = 0; kr < 3; kr++) for (let kc = 0; kc < 3; kc++) s += P03_ELSA_16[r + kr][c + kc] * K[kr][kc];
          row.push(Math.max(0, s));
        }}
        fm.push(row);
      }}
      const pl = [];
      for (let r = 0; r < 7; r++) {{
        const row = [];
        for (let c = 0; c < 7; c++) row.push(Math.max(fm[r * 2][c * 2], fm[r * 2][c * 2 + 1], fm[r * 2 + 1][c * 2], fm[r * 2 + 1][c * 2 + 1]));
        pl.push(row);
      }}
      drawMatrixCanvas('s11-can-fm', fm, 'blue');
      drawMatrixCanvas('s11-can-pool', pl, 'green');
    }}
    function _renderS11Cnn() {{
      const st = s11State.step;
      const tones = ['', 'sync-yellow', 'sync-blue', 'sync-green', 'sync-red'];
      for (let i = 1; i <= 4; i++) {{
        const vEl = document.getElementById('s11-vis-' + i);
        const cEl = document.getElementById('s11-card-' + i);
        [vEl, cEl].forEach((el) => {{
          if (!el) return;
          el.classList.remove('sync-on', 'sync-dim', 'sync-yellow', 'sync-blue', 'sync-green', 'sync-red');
          if (st === 0) {{
            if (i === 2) el.classList.add('sync-on', 'sync-blue');
          }} else if (st === i) {{
            el.classList.add('sync-on', tones[i]);
          }} else {{
            el.classList.add('sync-dim');
          }}
        }});
      }}
      const co = document.getElementById('s11-callout');
      const msgs = [
        '<strong>Alur Sederhana (1 → 2 → 3 → 4):</strong> Foto 2D dipindai 1 filter geser (<em>Feature Map</em>), diringkas (<em>MaxPool</em>), lalu diulang 3 lapis sebelum <code>GAP → Softmax</code>.',
        '<strong>Tahap 1/4 (Input 2D):</strong> Foto masuk utuh <code>224×224×3</code> — struktur ruang wajah, mahkota, &amp; gaun Elsa tetap terjaga.',
        '<strong>Tahap 2/4 (Conv2D 3×3):</strong> Satu filter kecil menggeser di atas foto menyalakan garis tepi &amp; warna menjadi <strong>Feature Map</strong>.',
        '<strong>Tahap 3/4 (MaxPool 2×2):</strong> Ukuran peta diringkas separuh sambil mempertahankan fitur paling kuat sehingga tahan pergeseran.',
        '<strong>Tahap 4/4 (Hierarki → Head):</strong> Blok dalam menyusun bagian tubuh utuh, diringkas <code>GAP</code> &rarr; hanya <strong>101.829 param</strong>!',
      ];
      if (co) co.innerHTML = msgs[st] || msgs[0];
    }}
    function jumpS11Cnn(n) {{ _stopS11Timer(); s11State.step = s11State.step === n ? 0 : n; _renderS11Cnn(); }}
    function stepS11Cnn() {{ _stopS11Timer(); s11State.step = (s11State.step % 4) + 1; _renderS11Cnn(); }}
    function resetS11Cnn() {{ _stopS11Timer(); s11State.step = 0; _renderS11Cnn(); }}
    function playS11Cnn() {{
      if (s11State.timer) {{ _stopS11Timer(); return; }}
      const pb = document.getElementById('s11-play-btn');
      if (pb) {{ pb.innerHTML = '&#9632; Stop'; pb.classList.add('playing'); }}
      s11State.step = 1;
      _renderS11Cnn();
      s11State.timer = setInterval(() => {{
        if (s11State.step < 4) {{ s11State.step += 1; _renderS11Cnn(); }}
        else {{ _stopS11Timer(); s11State.step = 0; _renderS11Cnn(); }}
      }}, 1150);
    }}

    // =========================================================================
    // SIMULATOR SLIDE 6 (#1.1 MLP Neuron-by-Neuron Animated Flow Engine)
    // =========================================================================
    const s06State = {{ hiddenCount: 2, step: 0, focusType: null, focusIdx: 0, seqPos: -1, timer: null, raf: null, pulseT: 0 }};
    function _s06TraceList(hc) {{
      const seq = [
        {{ type: 'in', idx: 0 }}, {{ type: 'in', idx: 1 }}, {{ type: 'in', idx: 2 }}, {{ type: 'in', idx: 5 }},
      ];
      if (hc >= 1) seq.push({{ type: 'h1', idx: 0 }}, {{ type: 'h1', idx: 1 }}, {{ type: 'h1', idx: 2 }}, {{ type: 'h1', idx: 3 }});
      if (hc >= 2) seq.push({{ type: 'h2', idx: 0 }}, {{ type: 'h2', idx: 1 }}, {{ type: 'h2', idx: 2 }});
      seq.push({{ type: 'out', idx: 1 }});
      return seq;
    }}
    function _stopS06Timer() {{
      if (s06State.timer) {{ clearInterval(s06State.timer); s06State.timer = null; }}
      if (s06State.raf) {{ cancelAnimationFrame(s06State.raf); s06State.raf = null; }}
      const cv = document.getElementById('s06-motion-canvas');
      if (cv) {{ const ctx = cv.getContext('2d'); if (ctx) ctx.clearRect(0, 0, cv.width, cv.height); }}
      const pb = document.getElementById('s06-play-btn');
      if (pb) {{ pb.innerHTML = '&#9654; Play Neuron'; pb.classList.remove('playing'); }}
    }}
    function _s06LayerCoords(hc) {{
      const inYs = [46, 70, 94, 118, 182, 206];
      const h1Ys = [62, 90, 118, 186];
      const h2Ys = [86, 126, 166];
      const outYs = [90, 108, 126, 144, 162];
      if (hc === 0) return {{ inX: 66, inYs, outX: 408, outLeftX: 369, outYs, h1X: 0, h1Ys: [], h2X: 0, h2Ys: [] }};
      if (hc === 1) return {{ inX: 66, inYs, h1X: 235, h1Ys, h2X: 0, h2Ys: [], outX: 408, outLeftX: 369, outYs }};
      return {{ inX: 66, inYs, h1X: 184, h1Ys, h2X: 288, h2Ys, outX: 408, outLeftX: 369, outYs }};
    }}
    function _drawS06MotionTick() {{
      const cv = document.getElementById('s06-motion-canvas');
      const wrap = document.getElementById('s06-diag-wrap');
      const svg = document.getElementById('s06-mlp-svg');
      if (!cv || !wrap || !svg) return;
      const w = wrap.clientWidth, h = wrap.clientHeight;
      if (cv.width !== w || cv.height !== h) {{ cv.width = w; cv.height = h; }}
      const ctx = cv.getContext('2d');
      ctx.clearRect(0, 0, w, h);
      if (!s06State.timer || !s06State.focusType) return;

      const wrapR = wrap.getBoundingClientRect();
      const svgR = svg.getBoundingClientRect();
      const sx = svgR.width / 470, sy = svgR.height / 262;
      const ox = svgR.left - wrapR.left, oy = svgR.top - wrapR.top;
      s06State.pulseT = (s06State.pulseT + 0.036) % 1;
      const t = s06State.pulseT;
      const c = _s06LayerCoords(s06State.hiddenCount);
      const ft = s06State.focusType, fi = s06State.focusIdx;
      const paths = [];
      let dotCol = '#1A73E8';

      if (ft === 'in') {{
        dotCol = '#F9AB00';
        const nx = c.h1Ys.length ? c.h1X : c.outLeftX;
        const nYs = c.h1Ys.length ? c.h1Ys : c.outYs;
        nYs.forEach((ny, k) => paths.push([c.inX, c.inYs[fi], nx, ny, (t + k * 0.12) % 1]));
      }} else if (ft === 'h1') {{
        dotCol = '#1A73E8';
        c.inYs.forEach((iy, k) => paths.push([c.inX, iy, c.h1X, c.h1Ys[fi], (t * 0.8 + k * 0.11) % 1, '#FBBC04']));
        const nx = c.h2Ys.length ? c.h2X : c.outLeftX;
        const nYs = c.h2Ys.length ? c.h2Ys : c.outYs;
        nYs.forEach((ny, k) => paths.push([c.h1X, c.h1Ys[fi], nx, ny, (t + k * 0.14) % 1, '#1A73E8']));
      }} else if (ft === 'h2') {{
        dotCol = '#174EA6';
        c.h1Ys.forEach((hy, k) => paths.push([c.h1X, hy, c.h2X, c.h2Ys[fi], (t * 0.8 + k * 0.15) % 1, '#4285F4']));
        c.outYs.forEach((oy, k) => paths.push([c.h2X, c.h2Ys[fi], c.outLeftX, oy, (t + k * 0.12) % 1, '#34A853']));
      }} else if (ft === 'out') {{
        dotCol = '#34A853';
        const px = c.h2Ys.length ? c.h2X : (c.h1Ys.length ? c.h1X : c.inX);
        const pYs = c.h2Ys.length ? c.h2Ys : (c.h1Ys.length ? c.h1Ys : c.inYs);
        pYs.forEach((py, k) => paths.push([px, py, c.outLeftX, c.outYs[fi], (t + k * 0.15) % 1, '#34A853']));
      }}
      paths.forEach(([x1, y1, x2, y2, p, colOv]) => {{
        const px = ox + (x1 + (x2 - x1) * p) * sx;
        const py = oy + (y1 + (y2 - y1) * p) * sy;
        ctx.beginPath();
        ctx.arc(px, py, 4.6, 0, Math.PI * 2);
        ctx.fillStyle = colOv || dotCol;
        ctx.fill();
        ctx.lineWidth = 1.6;
        ctx.strokeStyle = '#FFFFFF';
        ctx.stroke();
      }});
      s06State.raf = requestAnimationFrame(_drawS06MotionTick);
    }}
    function _renderS06Mlp() {{
      const hc = s06State.hiddenCount;
      const ft = s06State.focusType;
      const fi = s06State.focusIdx;
      const st = ft === 'in' ? 1 : ((ft === 'h1' || ft === 'h2') ? 2 : (ft === 'out' ? 3 : s06State.step));

      document.querySelectorAll('#s06-mlp-bar [data-s06m]').forEach((b) => {{
        b.classList.toggle('outline', Number(b.dataset.s06m) !== hc);
      }});
      const cIn = document.getElementById('s06-card-in');
      const cHid = document.getElementById('s06-card-hid');
      const cOut = document.getElementById('s06-card-out');
      [[cIn, 1, 'sync-yellow'], [cHid, 2, 'sync-blue'], [cOut, 3, 'sync-green']].forEach(([el, num, cls]) => {{
        if (!el) return;
        el.classList.remove('sync-on', 'sync-dim', 'sync-yellow', 'sync-blue', 'sync-green');
        if (st === 0) {{
          if (hc > 0 && num === 2) el.classList.add('sync-on', 'sync-blue');
        }} else if (st === num) {{
          el.classList.add('sync-on', cls);
        }} else {{
          el.classList.add('sync-dim');
        }}
      }});

      const kParam = document.getElementById('s06-kpi-param');
      const kBadge = document.getElementById('s06-kpi-badge');
      const hidTtl = document.getElementById('s06-hid-ttl');
      const hidDesc = document.getElementById('s06-hid-desc');
      const callout = document.getElementById('s06-mlp-callout');
      const diagTtl = document.getElementById('s06-diag-ttl');
      const diagPill = document.getElementById('s06-diag-pill');
      const narr = document.getElementById('s06-neuron-narr');
      const formula = document.getElementById('s06-mlp-formula');
      const svg = document.getElementById('s06-mlp-svg');

      if (hc === 0) {{
        if (kParam) kParam.textContent = 'Param: {p02_p:,}';
        if (kBadge) {{ kBadge.textContent = 'Model P02 (0 Hidden)'; kBadge.style.background = '#FEF7E0'; kBadge.style.color = '#B06000'; kBadge.style.borderColor = '#FDE293'; }}
        if (hidTtl) hidTtl.textContent = '0 Hidden Layer (Langsung ke Output)';
        if (hidDesc) hidDesc.innerHTML = 'Mode P02 <strong>tanpa Hidden Layer</strong>: piksel langsung dikalikan bobot ke 5 kelas tanpa perangkum tengah.';
        if (callout) callout.innerHTML = '<strong>Perbandingan P02:</strong> Tanpa <em>Hidden Layer</em>, model hanya punya 1 tahap perkalian langsung (<code>{p02_p:,}</code> param).';
        if (diagTtl) diagTtl.textContent = 'Model P02: Input Layer → Output Layer (0 Hidden)';
        if (formula) formula.innerHTML = '<code>150.528 × 5 + 5</code> = <strong>{p02_p:,} Param</strong> (Model 1-Layer P02)';
      }} else if (hc === 1) {{
        if (kParam) kParam.textContent = 'Param: 9.634.181';
        if (kBadge) {{ kBadge.textContent = 'MLP Dasar (1 Hidden)'; kBadge.style.background = '#E8F0FE'; kBadge.style.color = '#1A73E8'; kBadge.style.borderColor = '#C6DAFC'; }}
        if (hidTtl) hidTtl.textContent = '1 Lapis (64 Neuron + ReLU)';
        if (hidDesc) hidDesc.innerHTML = 'Tersisip <strong>1 Hidden Layer (64)</strong> untuk merangkum kombinasi piksel sebelum menuju Output Layer 5 kelas.';
        if (callout) callout.innerHTML = '<strong>MLP Minimal (1 Hidden):</strong> Begitu ada minimal 1 <em>Hidden Layer</em>, jaringan sudah disebut <strong>MLP</strong>!';
        if (diagTtl) diagTtl.textContent = 'Peta Layer MLP: Input → 1 Hidden (64) → Output';
        if (formula) formula.innerHTML = '<code>(150.528×64+64) + (64×5+5)</code> = <strong>9.634.181 Param</strong>';
      }} else {{
        if (kParam) kParam.textContent = 'Param: {r_mlp["total_params"]:,}';
        if (kBadge) {{ kBadge.textContent = 'MLP Penuh (2 Hidden)'; kBadge.style.background = '#E8F0FE'; kBadge.style.color = '#1A73E8'; kBadge.style.borderColor = '#C6DAFC'; }}
        if (hidTtl) hidTtl.textContent = '2 Lapis (64 → 32 Neuron)';
        if (hidDesc) hidDesc.innerHTML = 'Lapisan tersembunyi di tengah yang merangkai ciri dasar (<em>biru gaun + putih salju</em>) sebelum mengambil keputusan.';
        if (callout) callout.innerHTML = '<strong>Kunci MLP:</strong> Semua neuron tersambung penuh (<code>Dense</code>) melewati <strong>Hidden Layer</strong> sehingga mampu mengenali kombinasi ciri bertingkat.';
        if (diagTtl) diagTtl.textContent = 'Peta Layer MLP: Input → Hidden (64 → 32) → Output';
        if (formula) formula.innerHTML = '<code>(150.528×64+64) + (64×32+32) + (32×5+5)</code> = <strong>{r_mlp["total_params"]:,} Param</strong>';
      }}

      const inLbls = ['x₁', 'x₂', 'x₃', 'x₄', 'xₙ₋₁', 'xₙ'];
      const inVals = ['0.85', '0.62', '0.79', '0.44', '0.51', '0.31'];
      const h1Lbls = ['h₁', 'h₂', 'h₃', 'h₆₄'];
      const h1Vals = ['0.91', '0.74', '0.58', '0.43'];
      const h2Lbls = ['k₁', 'k₂', 'k₃₂'];
      const h2Vals = ['0.88', '0.69', '0.52'];
      const outNames = ['Anna', 'Elsa', 'Kristoff', 'Olaf', 'Sven'];
      const outPcts = ['7%', '82%', '4%', '5%', '2%'];

      if (narr) {{
        if (ft === 'in') narr.innerHTML = `<strong style="color:#B06000;">Neuron Input ${{inLbls[fi]}} (piksel=${{inVals[fi]}}):</strong> Mengirim nilai ke <strong>SEMUA neuron</strong> di depannya lewat kabel bobot (<code>×w</code>)!`;
        else if (ft === 'h1') narr.innerHTML = `<strong style="color:#1A73E8;">Neuron Hidden 1 ${{h1Lbls[fi]}} (ReLU=${{h1Vals[fi]}}):</strong> Menjumlah sinyal masuk dari <em>seluruh 150.528 Input</em>, lalu mengirim ke semua neuron berikutnya.`;
        else if (ft === 'h2') narr.innerHTML = `<strong style="color:#174EA6;">Neuron Hidden 2 ${{h2Lbls[fi]}} (ReLU=${{h2Vals[fi]}}):</strong> Menyaring pola H1 menjadi 32 ringkasan sebelum menyalurkan ke 5 kelas Output.`;
        else if (ft === 'out') narr.innerHTML = `<strong style="color:#137333;">Output ${{outNames[fi]}} (${{outPcts[fi]}}):</strong> Menerima akumulasi dari semua neuron sebelumnya &#8594; Softmax tertinggi memilih <strong>${{outNames[fi]}}</strong>!`;
        else narr.innerHTML = '<strong>Pola Corong:</strong> Input terbanyak (<code>150.528</code>) mengerucut lewat Hidden (<code>64 → 32</code>) ke Output (<code>5</code>). Klik neuron / <strong>&#9654; Play Neuron</strong>!';
      }}
      if (diagPill) {{
        diagPill.textContent = ft === 'in' ? `Fokus: ${{inLbls[fi]}}` : (ft === 'h1' ? `Fokus: ${{h1Lbls[fi]}}` : (ft === 'h2' ? `Fokus: ${{h2Lbls[fi]}}` : (ft === 'out' ? `Output: ${{outNames[fi]}}` : 'Pola Corong: 150.528 ≫ 64 > 32 > 5')));
      }}
      if (!svg) return;

      const c = _s06LayerCoords(hc);
      const hasFocus = !!ft;
      const lineStyle = (isInHit, isOutHit, hitCol) => {{
        if (!hasFocus) return {{ stroke: '#CBD5E1', w: 1.0, op: 0.78 }};
        if (isOutHit) return {{ stroke: hitCol, w: 2.25, op: 1 }};
        if (isInHit) return {{ stroke: '#F9AB00', w: 1.85, op: 0.95 }};
        return {{ stroke: '#E2E8F0', w: 0.85, op: 0.2 }};
      }};

      let wires = '';
      if (hc === 0) {{
        c.inYs.forEach((iy, ii) => c.outYs.forEach((oy, oi) => {{
          const s = lineStyle(ft === 'out' && oi === fi, ft === 'in' && ii === fi, '#F9AB00');
          wires += `<line x1="${{c.inX}}" y1="${{iy}}" x2="${{c.outLeftX}}" y2="${{oy}}" stroke="${{s.stroke}}" stroke-width="${{s.w}}" opacity="${{s.op}}"/>`;
        }}));
      }} else if (hc === 1) {{
        c.inYs.forEach((iy, ii) => c.h1Ys.forEach((hy, hi) => {{
          const s = lineStyle(ft === 'h1' && hi === fi, ft === 'in' && ii === fi, '#F9AB00');
          wires += `<line x1="${{c.inX}}" y1="${{iy}}" x2="${{c.h1X}}" y2="${{hy}}" stroke="${{s.stroke}}" stroke-width="${{s.w}}" opacity="${{s.op}}"/>`;
        }}));
        c.h1Ys.forEach((hy, hi) => c.outYs.forEach((oy, oi) => {{
          const s = lineStyle(ft === 'out' && oi === fi, ft === 'h1' && hi === fi, '#1A73E8');
          wires += `<line x1="${{c.h1X}}" y1="${{hy}}" x2="${{c.outLeftX}}" y2="${{oy}}" stroke="${{s.stroke}}" stroke-width="${{s.w}}" opacity="${{s.op}}"/>`;
        }}));
      }} else {{
        c.inYs.forEach((iy, ii) => c.h1Ys.forEach((hy, hi) => {{
          const s = lineStyle(ft === 'h1' && hi === fi, ft === 'in' && ii === fi, '#F9AB00');
          wires += `<line x1="${{c.inX}}" y1="${{iy}}" x2="${{c.h1X}}" y2="${{hy}}" stroke="${{s.stroke}}" stroke-width="${{s.w}}" opacity="${{s.op}}"/>`;
        }}));
        c.h1Ys.forEach((y1, i1) => c.h2Ys.forEach((y2, i2) => {{
          const s = lineStyle(ft === 'h2' && i2 === fi, ft === 'h1' && i1 === fi, '#1A73E8');
          wires += `<line x1="${{c.h1X}}" y1="${{y1}}" x2="${{c.h2X}}" y2="${{y2}}" stroke="${{s.stroke}}" stroke-width="${{s.w}}" opacity="${{s.op}}"/>`;
        }}));
        c.h2Ys.forEach((hy, hi) => c.outYs.forEach((oy, oi) => {{
          const s = lineStyle(ft === 'out' && oi === fi, ft === 'h2' && hi === fi, '#34A853');
          wires += `<line x1="${{c.h2X}}" y1="${{hy}}" x2="${{c.outLeftX}}" y2="${{oy}}" stroke="${{s.stroke}}" stroke-width="${{s.w}}" opacity="${{s.op}}"/>`;
        }}));
      }}

      const funnelPts = hc === 0
        ? '46,32 452,77 452,175 46,220'
        : (hc === 1 ? '46,32 235,48 452,77 452,175 235,204 46,220' : '46,32 184,48 288,72 452,77 452,175 288,180 184,204 46,220');
      const funnelBg = `
        <defs>
          <linearGradient id="s06FunnelGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#FEF7E0" stop-opacity="0.38"/>
            <stop offset="50%" stop-color="#E8F0FE" stop-opacity="0.34"/>
            <stop offset="100%" stop-color="#E6F4EA" stop-opacity="0.38"/>
          </linearGradient>
        </defs>
        <polygon points="${{funnelPts}}" fill="url(#s06FunnelGrad)" stroke="#CBD5E1" stroke-width="1.1" stroke-dasharray="4,3"/>
      `;

      const h1Dots = [145, 152, 159].map((dy) => `<circle cx="${{c.h1X}}" cy="${{dy}}" r="2" fill="#4285F4"/>`).join('');
      const inDots = [143, 150, 157].map((dy) => `<circle cx="${{c.inX}}" cy="${{dy}}" r="2" fill="#B06000"/>`).join('');

      let hidSvg = '';
      if (hc === 0) {{
        hidSvg = `
          <rect x="135" y="46" width="198" height="160" rx="12" fill="#FFFDF5" stroke="#FBBC04" stroke-width="1.4" stroke-dasharray="5,4"/>
          <text x="234" y="118" text-anchor="middle" font-family="Poppins" font-size="10.8" font-weight="700" fill="#B06000">TIDAK ADA HIDDEN LAYER</text>
          <text x="234" y="136" text-anchor="middle" font-family="Roboto" font-size="9.2" fill="#5F6368">Model 1-Layer P02 langsung Input &#8594; Output</text>
        `;
      }} else if (hc === 1) {{
        const nodes = c.h1Ys.map((hy, idx) => {{
          const act = ft === 'h1' && fi === idx;
          return `<g style="cursor:pointer;" onclick="selectS06Neuron('h1', ${{idx}})">
            ${{act ? `<circle cx="${{c.h1X}}" cy="${{hy}}" r="15.5" fill="none" stroke="#1A73E8" stroke-width="2" opacity="0.55"/>` : ''}}
            <circle cx="${{c.h1X}}" cy="${{hy}}" r="${{act ? 12.2 : 10.8}}" fill="${{act ? '#1A73E8' : '#E8F0FE'}}" stroke="#4285F4" stroke-width="${{act ? 2.4 : 1.9}}"/>
            <text x="${{c.h1X}}" y="${{hy + 3.4}}" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" font-weight="700" fill="${{act ? '#FFF' : '#1A73E8'}}">${{h1Lbls[idx]}}</text>
            ${{act ? `<rect x="${{c.h1X - 15}}" y="${{hy - 23}}" width="30" height="11.5" rx="4" fill="#1A73E8"/><text x="${{c.h1X}}" y="${{hy - 14.5}}" text-anchor="middle" font-family="Roboto Mono" font-size="6.8" font-weight="700" fill="#FFF">${{h1Vals[idx]}}</text>` : ''}}
          </g>`;
        }}).join('');
        hidSvg = `<rect x="160" y="42" width="150" height="168" rx="12" fill="rgba(232,240,254,0.34)" stroke="${{(ft==='h1') ? '#1A73E8' : '#8AB4F8'}}" stroke-width="${{(ft==='h1') ? 2.2 : 1.3}}" stroke-dasharray="5,3"/>${{nodes}}${{h1Dots}}`;
      }} else {{
        const n1 = c.h1Ys.map((hy, idx) => {{
          const act = ft === 'h1' && fi === idx;
          return `<g style="cursor:pointer;" onclick="selectS06Neuron('h1', ${{idx}})">
            ${{act ? `<circle cx="${{c.h1X}}" cy="${{hy}}" r="15.2" fill="none" stroke="#1A73E8" stroke-width="2" opacity="0.55"/>` : ''}}
            <circle cx="${{c.h1X}}" cy="${{hy}}" r="${{act ? 12 : 10.6}}" fill="${{act ? '#1A73E8' : '#E8F0FE'}}" stroke="#4285F4" stroke-width="${{act ? 2.3 : 1.8}}"/>
            <text x="${{c.h1X}}" y="${{hy + 3.4}}" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" font-weight="700" fill="${{act ? '#FFF' : '#1A73E8'}}">${{h1Lbls[idx]}}</text>
            ${{act ? `<rect x="${{c.h1X - 15}}" y="${{hy - 22.5}}" width="30" height="11.5" rx="4" fill="#1A73E8"/><text x="${{c.h1X}}" y="${{hy - 14.2}}" text-anchor="middle" font-family="Roboto Mono" font-size="6.8" font-weight="700" fill="#FFF">${{h1Vals[idx]}}</text>` : ''}}
          </g>`;
        }}).join('');
        const n2 = c.h2Ys.map((hy, idx) => {{
          const act = ft === 'h2' && fi === idx;
          return `<g style="cursor:pointer;" onclick="selectS06Neuron('h2', ${{idx}})">
            ${{act ? `<circle cx="${{c.h2X}}" cy="${{hy}}" r="15.2" fill="none" stroke="#174EA6" stroke-width="2" opacity="0.55"/>` : ''}}
            <circle cx="${{c.h2X}}" cy="${{hy}}" r="${{act ? 12 : 10.6}}" fill="${{act ? '#174EA6' : '#D2E3FC'}}" stroke="#1A73E8" stroke-width="${{act ? 2.3 : 1.8}}"/>
            <text x="${{c.h2X}}" y="${{hy + 3.4}}" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" font-weight="700" fill="${{act ? '#FFF' : '#174EA6'}}">${{h2Lbls[idx]}}</text>
            ${{act ? `<rect x="${{c.h2X - 15}}" y="${{hy - 22.5}}" width="30" height="11.5" rx="4" fill="#174EA6"/><text x="${{c.h2X}}" y="${{hy - 14.2}}" text-anchor="middle" font-family="Roboto Mono" font-size="6.8" font-weight="700" fill="#FFF">${{h2Vals[idx]}}</text>` : ''}}
          </g>`;
        }}).join('');
        hidSvg = `
          <rect x="144" y="42" width="184" height="168" rx="12" fill="rgba(232,240,254,0.28)" stroke="${{(ft==='h1'||ft==='h2') ? '#1A73E8' : '#8AB4F8'}}" stroke-width="${{(ft==='h1'||ft==='h2') ? 2.1 : 1.3}}" stroke-dasharray="5,3"/>
          ${{n1}}${{h1Dots}}${{n2}}
          <text x="184" y="222" text-anchor="middle" font-family="Roboto Mono" font-size="8.2" font-weight="700" fill="#1A73E8">H1: 64 ReLU</text>
          <text x="288" y="222" text-anchor="middle" font-family="Roboto Mono" font-size="8.2" font-weight="700" fill="#174EA6">H2: 32 ReLU</text>
        `;
      }}

      const inNodes = c.inYs.map((iy, idx) => {{
        const act = ft === 'in' && fi === idx;
        return `<g style="cursor:pointer;" onclick="selectS06Neuron('in', ${{idx}})">
          ${{act ? `<circle cx="${{c.inX}}" cy="${{iy}}" r="14" fill="none" stroke="#F9AB00" stroke-width="1.9" opacity="0.6"/>` : ''}}
          <circle cx="${{c.inX}}" cy="${{iy}}" r="${{act ? 11.2 : 9.6}}" fill="${{act ? '#F9AB00' : '#FEF7E0'}}" stroke="#FBBC04" stroke-width="${{act ? 2.3 : 1.8}}"/>
          <text x="${{c.inX}}" y="${{iy + 3.2}}" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" font-weight="700" fill="${{act ? '#FFF' : '#B06000'}}">${{inLbls[idx]}}</text>
          ${{act ? `<rect x="${{c.inX - 38}}" y="${{iy - 6.5}}" width="24" height="12.5" rx="4" fill="#B06000"/><text x="${{c.inX - 26}}" y="${{iy + 2}}" text-anchor="middle" font-family="Roboto Mono" font-size="6.8" font-weight="700" fill="#FFF">${{inVals[idx]}}</text>` : ''}}
        </g>`;
      }}).join('');
      const outNodes = c.outYs.map((oy, idx) => {{
        const act = (ft === 'out' && fi === idx) || (st === 3 && idx === 1 && !ft);
        return `<g style="cursor:pointer;" onclick="selectS06Neuron('out', ${{idx}})">
          <rect x="369" y="${{oy - 7.5}}" width="78" height="15" rx="7.5" fill="${{act ? '#34A853' : '#E6F4EA'}}" stroke="#34A853" stroke-width="${{act ? 2.1 : 1.4}}"/>
          <text x="408" y="${{oy + 2.9}}" text-anchor="middle" font-family="Poppins" font-size="${{act ? 8.1 : 8.4}}" font-weight="700" fill="${{act ? '#FFFFFF' : '#137333'}}">${{act ? outNames[idx] + ' ' + outPcts[idx] : outNames[idx]}}</text>
        </g>`;
      }}).join('');
      const funnelTag = hc === 0
        ? '150.528 &#8811; 5 (Langsung tanpa Hidden Layer)'
        : (hc === 1 ? 'Pola Corong: 150.528 &#8811; 64 &gt; 5' : 'Pola Corong Mengecil: 150.528 &#8811; 64 &gt; 32 &gt; 5');

      svg.innerHTML = `
        <rect x="20" y="5" width="92" height="19" rx="9.5" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.3"/>
        <text x="66" y="17.5" text-anchor="middle" font-family="Poppins" font-size="8.6" font-weight="700" fill="#B06000">INPUT LAYER</text>
        <rect x="160" y="5" width="152" height="19" rx="9.5" fill="${{hc === 0 ? '#F1F3F4' : '#E8F0FE'}}" stroke="${{hc === 0 ? '#DADCE0' : '#4285F4'}}" stroke-width="1.3"/>
        <text x="236" y="17.5" text-anchor="middle" font-family="Poppins" font-size="8.6" font-weight="700" fill="${{hc === 0 ? '#5F6368' : '#1A73E8'}}">${{hc === 0 ? '0 HIDDEN LAYER' : 'HIDDEN LAYERS (MLP)'}}</text>
        <rect x="358" y="5" width="100" height="19" rx="9.5" fill="#E6F4EA" stroke="#34A853" stroke-width="1.3"/>
        <text x="408" y="17.5" text-anchor="middle" font-family="Poppins" font-size="8.6" font-weight="700" fill="#137333">OUTPUT LAYER</text>
        ${{funnelBg}}
        <rect x="46" y="32" width="40" height="188" rx="13" fill="rgba(254,247,224,0.55)" stroke="#FBBC04" stroke-width="1.2" stroke-dasharray="4,3"/>
        <rect x="363" y="77" width="89" height="98" rx="12" fill="rgba(230,244,234,0.45)" stroke="#A8DAB5" stroke-width="1.2" stroke-dasharray="4,3"/>
        ${{wires}}
        ${{hidSvg}}
        ${{inNodes}}${{inDots}}
        ${{outNodes}}
        <text x="66" y="238" text-anchor="middle" font-family="Poppins" font-size="8.8" font-weight="700" fill="#B06000">150.528 Piksel</text>
        <text x="236" y="238" text-anchor="middle" font-family="Poppins" font-size="8.8" font-weight="700" fill="${{hc === 0 ? '#5F6368' : '#1A73E8'}}">${{hc === 0 ? 'Langsung ke Output' : (hc === 1 ? '1 Hidden Layer (64)' : '2 Hidden Layer (64 → 32)')}}</text>
        <text x="408" y="238" text-anchor="middle" font-family="Poppins" font-size="8.8" font-weight="700" fill="#137333">5 Kelas Softmax</text>
        <text x="236" y="254" text-anchor="middle" font-family="Roboto Mono" font-size="8.3" font-weight="700" fill="#5F6368">${{funnelTag}}</text>
      `;
    }}
    function setS06Mlp(hc) {{ _stopS06Timer(); s06State.hiddenCount = hc; s06State.step = 0; s06State.focusType = null; s06State.seqPos = -1; _renderS06Mlp(); }}
    function focusS06Step(num) {{
      _stopS06Timer();
      s06State.focusType = num === 1 ? 'in' : (num === 2 && s06State.hiddenCount > 0 ? 'h1' : (num === 3 ? 'out' : null));
      s06State.focusIdx = num === 3 ? 1 : 0;
      _renderS06Mlp();
    }}
    function selectS06Neuron(type, idx) {{
      _stopS06Timer();
      if (s06State.focusType === type && s06State.focusIdx === idx) {{ s06State.focusType = null; }}
      else {{ s06State.focusType = type; s06State.focusIdx = idx; }}
      _renderS06Mlp();
    }}
    function stepS06Neuron() {{
      _stopS06Timer();
      const seq = _s06TraceList(s06State.hiddenCount);
      s06State.seqPos = (s06State.seqPos + 1) % seq.length;
      const cur = seq[s06State.seqPos];
      s06State.focusType = cur.type;
      s06State.focusIdx = cur.idx;
      _renderS06Mlp();
    }}
    function playS06Mlp() {{
      if (s06State.timer) {{ _stopS06Timer(); _renderS06Mlp(); return; }}
      const pb = document.getElementById('s06-play-btn');
      if (pb) {{ pb.innerHTML = '&#9632; Stop'; pb.classList.add('playing'); }}
      const seq = _s06TraceList(s06State.hiddenCount);
      s06State.seqPos = 0;
      s06State.focusType = seq[0].type;
      s06State.focusIdx = seq[0].idx;
      s06State.pulseT = 0;
      _renderS06Mlp();
      s06State.raf = requestAnimationFrame(_drawS06MotionTick);
      s06State.timer = setInterval(() => {{
        const sList = _s06TraceList(s06State.hiddenCount);
        if (s06State.seqPos + 1 < sList.length) {{
          s06State.seqPos += 1;
          s06State.focusType = sList[s06State.seqPos].type;
          s06State.focusIdx = sList[s06State.seqPos].idx;
          _renderS06Mlp();
        }} else {{
          _stopS06Timer();
          s06State.focusType = null;
          s06State.seqPos = -1;
          _renderS06Mlp();
        }}
      }}, 850);
    }}
    function resetS06Mlp() {{ _stopS06Timer(); s06State.hiddenCount = 2; s06State.step = 0; s06State.focusType = null; s06State.seqPos = -1; _renderS06Mlp(); }}

    // Initial render
    _renderS06Mlp();
    _renderS11Canvases();
    _renderS11Cnn();
    setMlpSim('64_norm');
    _initCnnCanvasClicks();
    renderCnnSim();
    setResnetSim('plain');
    setMobSim('standard');
    renderEffSim();

    // =========================================================================
    // PDF / PPTX DETERMINISTIC STATE EXPANDER (2 states per simulator)
    // =========================================================================
    window.SLIDE_PDF_EXPANDERS = window.SLIDE_PDF_EXPANDERS || [];
    window.SLIDE_PDF_EXPANDERS.push(({{ cloneSlideWithCanvases }}) => {{
      _stopAllP03Timers();
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

      expandBar('sim-mlp-bar', [
        {{ charIdx: 1, hidden: 64, shift: 0, step: 0 }},
        {{ charIdx: 1, hidden: 64, shift: 8, step: 4 }},
      ], setMlpSim, 'mlp');
      expandBar('sim-cnn-bar', [
        {{ filter: 'sobel_v', stride: 1, pad: 0, scanIdx: 92 }},
        {{ filter: 'sobel_v', stride: 2, pad: 1, scanIdx: 27 }},
      ], setCnnState, 'cnn');
      expandBar('sim-resnet-bar', ['plain', 'resnet'], setResnetSim, 'res');
      expandBar('sim-mob-bar', ['standard', 'mobilenetv2'], setMobSim, 'mob');
      expandBar('sim-eff-bar', [
        {{ scale: 'b0', se: false, step: 0 }},
        {{ scale: 'b2', se: true, step: 0 }},
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
