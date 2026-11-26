"""Generate 59-slide interactive HTML5 deck (SSOT) for P02: Teori Neural Network.

Structure (exact 120.0 minutes across 59 slides):
- Pembuka (01–06 · 6.0m): Cover, Peta 5 Bab, Alur 120 Menit, Tujuan 3 Kartu, Recap P01, Pemanasan Q&A
- Bab 1 (07–11 · 6.0m): AI vs ML vs DL (+ 2 simulators + 1 Q&A)
- Bab 2 (12–19 · 10.0m): 4 Task Computer Vision: Classification, Detection, Instance Segmentation, Object Tracking (+ 2 simulators + 1 Q&A)
- Bab 3 (20–40 · 27.0m): Neural Network dari terkecil -> terbesar: Neuron -> Input/Output Layer -> Koneksi -> Hidden Layer -> Forward Pass 4 piksel nyata -> Loss/Gradient Descent/Backprop intuitif (+ 7 simulators + 2 Q&A)
- Bab 4 (41–45 · 6.0m): Arsitektur CV (Teaser): MLP -> CNN -> ResNet -> MobileNetV2 (+ 1 simulator + 1 Q&A)
- Istirahat (46 · 5.0m): Pembatas Bab 5 + Jeda 5 menit
- Bab 5 (47–59 · 60.0m): 6 Langkah Hands-On (45m), Mini-Challenge (5m), Kamus Istilah (2m), Kuis 5 Soal (4m), 3 Poin Utama Dark (2m), Closing (2m), 2 Slide Referensi (0m)
"""

from __future__ import annotations

import html as html_lib
import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from core.html_shell import make_agenda_slide, make_divider_slide, write_deck_html  # noqa: E402
from core.registry import get_session  # noqa: E402

SESSION = get_session("P02")
ASSETS_DIR = SESSION.assets_dir
FOOTER = SESSION.short_title

# Toggle sementara untuk menyembunyikan Slide 28–40 lama (Bab 3C–3E: Koneksi 1-ke-5,
# Hidden Layer, Forward Pass 4px, Loss/GD/Backprop, Q&A #4–#5) tanpa menghapus kodenya.
# Ubah ke False kapan saja untuk memunculkan kembali seluruh 59 slide.
HIDE_SLIDES_28_40 = True
# Bab 4 (Arsitektur Neural Network untuk CV) dipindahkan ke P03; tetap disimpan
# utuh di kode agar mudah diadaptasi saat membangun P03.
HIDE_BAB4_ARCH = True

EXTRA_CSS = """
    .sim-bar { display: flex; flex-wrap: wrap; gap: 7px; align-items: center; }
    .sim-slider-row { display: grid; grid-template-columns: 120px 1fr 56px; gap: 8px; align-items: center; font-size: 12.2px; }
    .sim-slider-row input[type="range"] { width: 100%; accent-color: var(--blue-text); cursor: pointer; }
    .sim-val { font-family: var(--font-code); font-weight: 700; text-align: right; color: var(--dark); font-size: 12.2px; }
    .prob-row { display: grid; grid-template-columns: 84px 1fr 50px 56px; gap: 7px; align-items: center; font-size: 12px; }
    .prob-track { height: 17px; background: #ECEFF1; border-radius: 999px; overflow: hidden; border: 1px solid var(--border); }
    .prob-fill { height: 100%; border-radius: 999px; transition: width 0.16s ease; }
    .formula-box { background: var(--surface); border: 1.5px solid #C6DAFC; border-radius: 12px; padding: 8px 14px; font-family: var(--font-code); font-size: 12.8px; color: var(--dark); text-align: center; font-weight: 600; }
    .canvas-box { background: var(--white); border: 1px solid var(--border); border-radius: 14px; padding: 9px 11px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; gap: 6px; height: 100%; }
    .canvas-box canvas { width: 100%; height: auto; max-height: 100%; display: block; }
    .kpi-strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .kpi-mini { background: var(--surface); border: 1px solid var(--border); border-radius: 11px; padding: 7px 9px; text-align: center; }
    .kpi-mini .k-num { font-family: var(--font-title); font-size: 17.5px; font-weight: 700; color: var(--blue-text); line-height: 1.1; }
    .kpi-mini .k-lbl { font-size: 10.2px; color: var(--muted); margin-top: 2px; }
    .mini-box { background: #FFFFFF; border: 1px solid var(--border); border-radius: 11px; padding: 9px 12px; font-size: 12.4px; line-height: 1.44; color: #3C4043; }
    .contrib-row { display: grid; grid-template-columns: 88px 1fr 50px; gap: 7px; align-items: center; font-size: 11.5px; font-family: var(--font-code); }
    .contrib-track { height: 13px; background: #F1F3F4; border-radius: 999px; position: relative; overflow: hidden; border: 1px solid #E0E3E7; }
    .contrib-mid { position: absolute; left: 50%; top: 0; bottom: 0; width: 1.5px; background: #9AA0A6; }
    .contrib-bar { position: absolute; top: 1px; bottom: 1px; border-radius: 999px; }
    .match-row { display: grid; grid-template-columns: 1.35fr 1fr; gap: 10px; align-items: center; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 9px 12px; }
    .match-btns { display: flex; flex-wrap: wrap; gap: 5px; }
    .match-btns .btn-ui { padding: 5px 9px; font-size: 11px; border-radius: 8px; }
    .glossary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 9px; flex: 1; }
    .gloss-card { background: var(--surface); border: 1px solid var(--border); border-radius: 11px; padding: 8px 11px; display: flex; flex-direction: column; gap: 3px; }
    .gloss-term { font-family: var(--font-title); font-size: 12.3px; font-weight: 700; color: var(--blue-text); }
    .gloss-def { font-size: 11.1px; line-height: 1.36; color: #3C4043; }
    .quiz-grid-compact { display: grid; grid-template-columns: 1fr 1fr; gap: 11px; flex: 1; align-content: center; }
    .quiz-item.compact { padding: 11px 14px; gap: 6px; }
    .quiz-item.compact .q-txt { font-size: 13px; font-weight: 600; color: var(--dark); line-height: 1.35; }
    .quiz-item.compact .btn-ui { padding: 5px 11px; font-size: 11.2px; }
    .quiz-item.compact .quiz-ans { font-size: 12px; padding: 7px 10px; line-height: 1.38; }
    .arch-card-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
    .arch-pill-card { border: 1.5px solid var(--border); border-radius: 12px; padding: 10px 12px; background: var(--surface); cursor: pointer; transition: all 0.15s; text-align: left; }
    .arch-pill-card.active { background: var(--tint-blue); border-color: var(--blue); box-shadow: 0 4px 12px rgba(66,133,244,0.16); }
    .ho-layout { display: grid; grid-template-columns: 1.05fr 1.15fr; gap: 16px; flex: 1; min-height: 0; align-items: stretch; }
    /* Slide 22 3-stage process animation styling (zero layout-shift / 60fps smooth) */
    .in-stage-card { transition: opacity 0.32s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.32s cubic-bezier(0.22, 1, 0.36, 1); will-change: opacity, box-shadow; }
    .in-stage-card.dim { opacity: 0.42; }
    .in-stage-card.glow-blue { box-shadow: 0 0 0 2.5px rgba(66,133,244,0.36), 0 8px 20px rgba(66,133,244,0.14) !important; opacity: 1; }
    .in-stage-card.glow-yellow { box-shadow: 0 0 0 2.5px rgba(251,188,4,0.48), 0 8px 20px rgba(227,116,0,0.14) !important; opacity: 1; }
    .in-stage-card.glow-green { box-shadow: 0 0 0 2.5px rgba(52,168,83,0.36), 0 8px 20px rgba(52,168,83,0.14) !important; opacity: 1; }
    .in-scan-bar { position: absolute; left: 0; right: 0; height: 10px; top: 0; opacity: 0; pointer-events: none; z-index: 5; background: linear-gradient(to bottom, rgba(251,188,4,0.0), rgba(251,188,4,0.92), rgba(66,133,244,0.85), rgba(251,188,4,0.0)); }
    .in-arrow-box { position: relative; transition: opacity 0.28s ease; }
    .in-arrow-box.dim { opacity: 0.34; }
    .in-arrow-box.active { opacity: 1; }
    .in-arrow-dot { position: absolute; top: 50%; left: 2px; width: 9px; height: 9px; border-radius: 50%; transform: translateY(-50%); opacity: 0; pointer-events: none; }
    .in-node-row { transition: opacity 0.34s cubic-bezier(0.22, 1, 0.36, 1), background 0.18s ease; border-radius: 8px; cursor: pointer; will-change: opacity; }
    .in-node-row:hover { background: #F1F6FE; }
    .in-node-row.traced { background: #E8F0FE; box-shadow: inset 0 0 0 1.5px #4285F4; }
    .in-node-row.hidden-step { opacity: 0; }
    .in-clickable { cursor: pointer; transition: box-shadow 0.2s ease; }
    .in-clickable:hover { box-shadow: 0 0 0 3px rgba(66,133,244,0.28), 0 6px 16px rgba(66,133,244,0.20) !important; }
    /* Slide 23 Input -> Output Layer 60fps interactive motion styling (zero layout-shift) */
    .io-card { transition: box-shadow 0.28s ease, opacity 0.28s ease; }
    .io-card.active-card { box-shadow: 0 0 0 2.5px rgba(66,133,244,0.42), 0 6px 16px rgba(66,133,244,0.14); }
    .io-card.active-green { box-shadow: 0 0 0 2.5px rgba(52,168,83,0.46), 0 6px 16px rgba(52,168,83,0.16); }
    .io-stage { transition: opacity 0.28s ease, box-shadow 0.28s ease; }
    .io-stage.dim { opacity: 0.36; }
    .io-stage.glow-blue { box-shadow: 0 0 0 2.5px rgba(66,133,244,0.38), 0 6px 16px rgba(66,133,244,0.14) !important; opacity: 1; }
    .io-stage.glow-green { box-shadow: 0 0 0 2.5px rgba(52,168,83,0.44), 0 6px 16px rgba(52,168,83,0.16) !important; opacity: 1; }
    .io-in-node, .io-out-node { cursor: pointer; transition: opacity 0.26s ease; }
    .io-in-node:hover circle, .io-out-node:hover rect:first-child { filter: brightness(0.95); }
    .io-node-dim { opacity: 0.16; }
    .io-wires-group { transition: opacity 0.28s ease; }
    /* Slide 20: 1 Pixel -> 1 Neuron 60fps interactive widget */
    .n1-cell { width: 100%; height: 100%; cursor: pointer; position: relative; transition: opacity 0.22s ease; box-sizing: border-box; }
    .n1-cell:hover { outline: 2px solid #FBBC04; z-index: 3; }
    .n1-cell.selected { outline: 2.6px solid #EA4335; outline-offset: -1px; z-index: 4; box-shadow: 0 0 0 1px #FFFFFF; }
    .n1-stage-dim { opacity: 0.24; transition: opacity 0.28s ease; }
    .n1-stage-on  { opacity: 1; transition: opacity 0.28s ease; }
    /* Slide 24: Mathematical Training Simulation (5 Frozen photos -> Weights+Bias -> Activation -> Output) */
    .tm-ds-item { display: flex; align-items: center; gap: 7px; padding: 4.5px 7px; border-radius: 9px; border: 1.5px solid #E0E3E7; background: #FFFFFF; cursor: pointer; transition: border-color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease; }
    .tm-ds-item:hover { border-color: #4285F4; background: #F8FAFF; }
    .tm-ds-item.active { border-color: #1A73E8; background: #E8F0FE; box-shadow: 0 2px 8px rgba(26,115,232,0.16); }
    .tm-math-card { border-radius: 9px; padding: 5.5px 9px; transition: box-shadow 0.28s ease, opacity 0.28s ease; }
    .tm-math-card.glow-yellow { box-shadow: 0 0 0 2.5px rgba(251,188,4,0.60), 0 4px 12px rgba(227,116,0,0.16); opacity: 1; }
    .tm-math-card.glow-green  { box-shadow: 0 0 0 2.5px rgba(52,168,83,0.55), 0 4px 12px rgba(52,168,83,0.16); opacity: 1; }
    .tm-math-card.dim { opacity: 0.42; }
    /* Slide 25 (Weight & Bias) & Slide 26 (Activation Function) interactive dataset chips & sliders */
    .ds-chip-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; }
    .ds-chip { display: flex; flex-direction: column; align-items: center; gap: 2px; padding: 4px 4px; border-radius: 9px; border: 1.5px solid #E0E3E7; background: #FFFFFF; cursor: pointer; transition: border-color 0.16s ease, background 0.16s ease, box-shadow 0.16s ease; text-align: center; }
    .ds-chip:hover { border-color: #4285F4; background: #F8FAFF; }
    .ds-chip.active { border-color: #1A73E8; background: #E8F0FE; box-shadow: 0 2px 8px rgba(26,115,232,0.16); }
    .ds-chip img { width: 26px; height: 26px; border-radius: 6px; object-fit: cover; border: 1.8px solid #DADCE0; }
    .ds-chip .c-name { font-family: var(--font-title); font-size: 9.2px; font-weight: 700; color: #202124; line-height: 1.1; }
    .ds-chip .c-score { font-family: var(--font-code); font-size: 8.6px; font-weight: 700; padding: 1px 5px; border-radius: 999px; line-height: 1.2; }
    .wb-srow { display: grid; grid-template-columns: 112px 1fr 48px; gap: 6px; align-items: center; font-size: 10.6px; }
    .wb-srow input[type="range"] { width: 100%; margin: 0; accent-color: #1A73E8; cursor: pointer; }
    .wb-srow.bias-row input[type="range"] { accent-color: #E37400; }
    /* Unified Synchronized Explanation-Card Choreography across ALL animated slides (S20-S28) */
    @keyframes syncCardPulse {
      0%, 100% { filter: brightness(1.00); }
      50%      { filter: brightness(1.03); }
    }
    .sync-card {
      position: relative;
      transition: transform 0.18s cubic-bezier(0.22, 1, 0.36, 1),
                  box-shadow 0.18s cubic-bezier(0.22, 1, 0.36, 1),
                  opacity 0.16s ease,
                  border-color 0.16s ease;
      will-change: transform, box-shadow, opacity;
    }
    @media print {
      .sync-card, .sync-card::after, .sync-bullet { transition: none !important; animation: none !important; }
    }
    .sync-card .card-top-bar { transition: height 0.24s ease; }
    .sync-card.sync-dim { opacity: 0.48; transform: translateY(0) scale(0.992); }
    .sync-card.sync-on {
      opacity: 1 !important;
      transform: translateY(-3.5px) scale(1.012);
      z-index: 4;
      animation: syncCardPulse 1.5s ease-in-out infinite;
    }
    .sync-card.sync-on .card-top-bar { height: 5.5px; }
    .sync-card.sync-blue   { box-shadow: 0 0 0 2.5px rgba(66,133,244,0.72), 0 8px 18px rgba(66,133,244,0.22) !important; border-color: #4285F4 !important; }
    .sync-card.sync-yellow { box-shadow: 0 0 0 2.5px rgba(251,188,4,0.84), 0 8px 18px rgba(227,116,0,0.22) !important; border-color: #FBBC04 !important; }
    .sync-card.sync-green  { box-shadow: 0 0 0 2.5px rgba(52,168,83,0.72), 0 8px 18px rgba(52,168,83,0.22) !important; border-color: #34A853 !important; }
    .sync-card.sync-red    { box-shadow: 0 0 0 2.5px rgba(234,67,53,0.72), 0 8px 18px rgba(234,67,53,0.22) !important; border-color: #EA4335 !important; }
    .sync-card::after {
      content: '● AKTIF';
      position: absolute;
      top: 6px;
      right: 7px;
      font-family: var(--font-title);
      font-size: 7.4px;
      font-weight: 800;
      letter-spacing: 0.04em;
      padding: 1.5px 5.5px;
      border-radius: 999px;
      opacity: 0;
      transform: scale(0.8);
      transition: opacity 0.14s ease, transform 0.14s ease;
      pointer-events: none;
    }
    .sync-card.sync-on::after { opacity: 1; transform: scale(1); }
    .sync-card.sync-no-badge::after { display: none; }
    .sync-card.sync-blue::after   { background: #4285F4; color: #FFFFFF; }
    .sync-card.sync-yellow::after { background: #FBBC04; color: #202124; }
    .sync-card.sync-green::after  { background: #34A853; color: #FFFFFF; }
    .sync-card.sync-red::after    { background: #EA4335; color: #FFFFFF; }
    .sync-card.sync-on .card-title { padding-right: 44px; }
    .sync-bullet {
      transition: background 0.24s ease, box-shadow 0.24s ease, transform 0.24s ease, opacity 0.24s ease;
      border-radius: 7px;
      padding: 2.5px 6px;
      margin: 0 -6px;
    }
    .sync-bullet.sync-dim { opacity: 0.45; }
    .sync-bullet.sync-on  { background: #FFFFFF; opacity: 1; transform: translateX(3px); }
    .sync-bullet.sync-blue.sync-on   { box-shadow: 0 0 0 1.8px rgba(66,133,244,0.62), 0 3px 8px rgba(66,133,244,0.16); }
    .sync-bullet.sync-green.sync-on  { box-shadow: 0 0 0 1.8px rgba(52,168,83,0.62), 0 3px 8px rgba(52,168,83,0.16); }
    .sync-bullet.sync-red.sync-on    { box-shadow: 0 0 0 1.8px rgba(234,67,53,0.62), 0 3px 8px rgba(234,67,53,0.16); }
    .sync-bullet.sync-yellow.sync-on { box-shadow: 0 0 0 1.8px rgba(251,188,4,0.75), 0 3px 8px rgba(227,116,0,0.16); }
    /* Ultimate Slide 29: Full End-to-End Neural Network Controls */
    .fnn-char-btn { display: inline-flex; align-items: center; gap: 4px; padding: 2.5px 7px 2.5px 3px; border-radius: 999px; border: 1.5px solid #DADCE0; background: #FFFFFF; font-family: var(--font-title); font-size: 9.6px; font-weight: 700; color: #3C4043; cursor: pointer; transition: all 0.16s ease; }
    .fnn-char-btn:hover { border-color: #4285F4; background: #F8FAFF; }
    .fnn-char-btn.active { border-color: #1A73E8; background: #E8F0FE; color: #1A73E8; box-shadow: 0 2px 6px rgba(26,115,232,0.18); }
    .fnn-char-btn img { width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1.5px solid #DADCE0; }
    .fnn-char-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; flex-shrink: 0; border: 1px solid rgba(0,0,0,0.12); }
    .fnn-stage-card { cursor: pointer; }

    /* Slides 30 & 35 Cover Roadmaps (high-contrast on bg-yellow & bg-blue) */
    .cover-roadmap { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; }
    .cover-roadmap-3x2 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; max-width: 740px; margin-top: 20px; }
    .cover-chip { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-radius: 13px; border: 1.5px solid rgba(0,0,0,0.10); }
    .bg-yellow .cover-chip { background: rgba(255,255,255,0.62); border-color: rgba(32,33,36,0.16); color: #202124; }
    .bg-blue   .cover-chip { background: rgba(255,255,255,0.16); border-color: rgba(255,255,255,0.34); color: #FFFFFF; }
    .cover-chip-num { width: 26px; height: 26px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-family: var(--font-title); font-size: 12px; font-weight: 800; flex-shrink: 0; }
    .bg-yellow .cover-chip-num { background: #202124; color: #FBBC04; }
    .bg-blue   .cover-chip-num { background: #FFFFFF; color: #1A73E8; }
    .cover-chip-ttl { font-family: var(--font-title); font-size: 12.2px; font-weight: 700; line-height: 1.2; }
    .cover-chip-sub { font-size: 10.6px; opacity: 0.86; line-height: 1.25; margin-top: 1px; }
    .cover-env-strip { margin-top: 14px; display: inline-flex; align-items: center; gap: 8px; padding: 6px 13px; border-radius: 999px; font-family: var(--font-code); font-size: 11px; font-weight: 600; background: rgba(32,33,36,0.22); color: #FFFFFF; border: 1px solid rgba(255,255,255,0.28); }

    /* Slide 31 Interactive Quiz Cards & Scoreboard */
    .qz-head-row { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin-bottom: 6px; }
    .qz-toolbar { display: flex; align-items: center; gap: 7px; flex-shrink: 0; }
    .qz-score-pill { font-family: var(--font-title); font-size: 11.4px; font-weight: 700; background: #E8F0FE; color: #1A73E8; border: 1.5px solid #C6DAFC; border-radius: 999px; padding: 4px 12px; }
    .qz-opts { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 1px; }
    .qz-opt { font-family: var(--font-body); font-size: 10.7px; font-weight: 500; padding: 3.5px 9px; border-radius: 8px; border: 1.3px solid #DADCE0; background: #FFFFFF; color: #3C4043; cursor: pointer; transition: all 0.14s ease; }
    .qz-opt:hover { border-color: #4285F4; background: #F4F8FF; }
    .qz-opt.ok  { background: #E6F4EA !important; border-color: #34A853 !important; color: #137333 !important; font-weight: 700 !important; }
    .qz-opt.bad { background: #FCE8E6 !important; border-color: #EA4335 !important; color: #C5221F !important; }
    .qz-foot { display: flex; align-items: center; gap: 7px; flex-wrap: wrap; }
    .qz-item-tight { padding: 7.5px 11px !important; gap: 4.5px !important; justify-content: space-between; }
    .qz-item-tight .q-txt { font-size: 12.1px !important; line-height: 1.32 !important; }
    .qz-item-tight .quiz-ans { font-size: 10.6px !important; padding: 4.5px 8px !important; line-height: 1.28 !important; margin-top: 1px; }
    .qz-mini-btn { font-family: var(--font-title); font-size: 10.1px; font-weight: 600; color: #1A73E8; background: transparent; border: none; padding: 2px 4px; cursor: pointer; text-decoration: underline; }
    section.slide.pdf-answer-slide .qz-opt[data-correct="true"] { background: #E6F4EA !important; border-color: #34A853 !important; color: #137333 !important; font-weight: 700 !important; }
    @media print { .qz-ctrl-hide { display: none !important; } }

    /* Slide 32 Interactive 2-Column Grouped Dictionary List */
    .gloss-head-row { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin-bottom: 10px; }
    .gloss-controls { display: flex; align-items: center; gap: 7px; flex-wrap: wrap; }
    .gloss-search-wrap { position: relative; display: flex; align-items: center; }
    .gloss-search {
      font-family: var(--font-body); font-size: 11px; color: #202124;
      background: #F8F9FA; border: 1.4px solid #DADCE0; border-radius: 999px;
      padding: 4px 11px 4px 26px; width: 158px; outline: none; transition: all 0.16s ease;
    }
    .gloss-search:focus { background: #FFFFFF; border-color: #4285F4; width: 185px; box-shadow: 0 0 0 3px rgba(66,133,244,0.14); }
    .gloss-search-ico { position: absolute; left: 9px; font-size: 10.5px; color: #5F6368; pointer-events: none; }
    .gloss-filter-bar { display: flex; gap: 5px; flex-wrap: wrap; }
    .gloss-fbtn { font-family: var(--font-title); font-size: 10.5px; font-weight: 700; padding: 4px 10px; border-radius: 999px; border: 1.4px solid #DADCE0; background: #FFFFFF; color: #5F6368; cursor: pointer; transition: all 0.14s ease; }
    .gloss-fbtn:hover { border-color: #4285F4; color: #1A73E8; }
    .gloss-fbtn.active { background: #202124; color: #FFFFFF; border-color: #202124; }
    .dict-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; flex: 1; min-height: 0; align-items: stretch; }
    .dict-col { display: flex; flex-direction: column; gap: 11px; min-height: 0; }
    .dict-group { background: #FFFFFF; border: 1.4px solid #DADCE0; border-radius: 13px; overflow: hidden; display: flex; flex-direction: column; min-height: 0; }
    .dict-group.grow { flex: 1; }
    .dict-group-head { display: flex; align-items: center; justify-content: space-between; padding: 7px 13px; font-family: var(--font-title); font-size: 11px; font-weight: 800; letter-spacing: 0.02em; border-bottom: 1px solid #E8EAED; }
    .dict-group-head.b1 { background: #E8F0FE; color: #1A73E8; border-bottom-color: #D2E3FC; }
    .dict-group-head.b2 { background: #FCE8E6; color: #C5221F; border-bottom-color: #FAD2CF; }
    .dict-group-head.b3 { background: #E6F4EA; color: #137333; border-bottom-color: #CEEAD6; }
    .dict-group-cnt { font-size: 9.6px; font-weight: 700; padding: 1.5px 7px; border-radius: 999px; background: rgba(255,255,255,0.82); }
    .dict-list { display: flex; flex-direction: column; flex: 1; }
    .dict-row {
      display: grid; grid-template-columns: 144px 1fr auto; gap: 10px; align-items: center;
      padding: 5.5px 12px; border-bottom: 1px solid #EEF0F3; flex: 1;
      transition: background 0.14s ease, opacity 0.18s ease;
    }
    .dict-row:nth-child(even) { background: #FAFBFD; }
    .dict-row:last-child { border-bottom: none; }
    .dict-row:hover { background: #F1F6FE; }
    .dict-row.ch-dim { opacity: 0.20; }
    .dict-term { font-family: var(--font-title); font-size: 11.4px; font-weight: 700; line-height: 1.22; }
    .dict-term.b1 { color: #1A73E8; }
    .dict-term.b2 { color: #C5221F; }
    .dict-term.b3 { color: #137333; }
    .dict-def { font-size: 10.9px; line-height: 1.32; color: #3C4043; }
    .dict-slide-btn {
      font-family: var(--font-code); font-size: 9.4px; font-weight: 700;
      padding: 2.5px 7px; border-radius: 7px; border: 1px solid #DADCE0;
      background: #FFFFFF; color: #5F6368; cursor: pointer; white-space: nowrap;
      transition: all 0.14s ease;
    }
    .dict-slide-btn:hover { background: #1A73E8; border-color: #1A73E8; color: #FFFFFF; }
    @media print { .gloss-search-wrap { display: none !important; } }

    /* Slides 33 & 34 Balanced Full-Height Reference Cards & Guide Strip */
    .ref-grid-full {
      display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-rows: repeat(3, minmax(0, 1fr));
      gap: 9px; flex: 1; min-height: 0; margin-top: 2px;
    }
    .ref-card-rich {
      display: flex; flex-direction: column; justify-content: space-between; gap: 5px;
      padding: 9px 13px; border-radius: 12px; min-width: 0; overflow: hidden;
      background: #FFFFFF; border: 1px solid #DADCE0; border-left: 4px solid #4285F4;
      text-decoration: none; color: inherit; user-select: text;
      transition: border-color 0.16s ease, transform 0.16s ease, background 0.16s ease, box-shadow 0.16s ease;
    }
    .ref-card-rich.acc-blue   { border-left-color: #4285F4; }
    .ref-card-rich.acc-green  { border-left-color: #34A853; }
    .ref-card-rich.acc-yellow { border-left-color: #FBBC04; }
    .ref-card-rich.acc-red    { border-left-color: #EA4335; }
    .ref-card-rich.featured   { background: #FFFDF4; border-color: #F6C343; border-left: 4px solid #FBBC04; }
    .ref-card-rich:hover {
      border-color: #4285F4; background: #F4F8FF;
      transform: translateY(-1.5px); box-shadow: 0 5px 14px rgba(26,115,232,0.12);
    }
    .ref-card-rich.featured:hover { background: #FEF7E0; border-color: #E37400; }
    .ref-card-top { display: flex; align-items: flex-start; gap: 9px; min-width: 0; }
    .ref-card-top .ref-num { width: 25px; height: 25px; font-size: 11.6px; margin-top: 0; }
    .ref-card-head { flex: 1; min-width: 0; display: flex; align-items: flex-start; justify-content: space-between; gap: 7px; }
    .ref-card-rich .ref-title { font-size: 12.6px; line-height: 1.24; }
    .ref-card-rich .ref-desc { font-size: 11.4px; line-height: 1.38; color: #3C4043; padding-left: 34px; }
    .ref-card-foot {
      display: flex; align-items: center; justify-content: space-between; gap: 8px;
      padding-top: 5px; padding-left: 34px; border-top: 1px dashed #E8EAED; min-width: 0;
    }
    .ref-card-rich .ref-url { font-size: 9.9px; font-weight: 600; color: #1A73E8; min-width: 0; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .ref-ctx-pill {
      font-family: var(--font-title); font-size: 9.2px; font-weight: 700;
      padding: 2px 7.5px; border-radius: 999px; background: #F1F3F4; color: #3C4043;
      white-space: nowrap; flex-shrink: 0;
    }
    .ref-route-bar { margin-top: 10px; background: #F8F9FA; border: 1.5px solid #E0E3E7; border-radius: 12px; padding: 8px 13px; display: flex; flex-direction: column; gap: 5px; flex-shrink: 0; }
    .ref-route-head { display: flex; justify-content: space-between; align-items: center; font-family: var(--font-title); font-size: 11.2px; font-weight: 700; color: #202124; }
    .ref-route-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 9px; }
    .ref-step-box { background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 9px; padding: 6.5px 10px; font-size: 10.8px; line-height: 1.34; color: #3C4043; }

    /* Slides 36-41 Visual-First Hands-On Stepper, Compact Code & Real Visual Output */
    .ho-layout { display: grid; grid-template-columns: 0.92fr 1.28fr; gap: 15px; flex: 1; min-height: 0; align-items: stretch; }
    .ho-head-row { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin-bottom: 8px; }
    .ho-stepper { display: flex; align-items: center; gap: 3.5px; background: #F8F9FA; border: 1px solid #E0E3E7; border-radius: 999px; padding: 3px 5.5px; flex-shrink: 0; }
    .ho-step-dot { font-family: var(--font-title); font-size: 9.3px; font-weight: 700; padding: 3px 7.5px; border-radius: 999px; color: #5F6368; white-space: nowrap; }
    .ho-step-dot.done { background: #E6F4EA; color: #137333; }
    .ho-step-dot.cur  { background: #1A73E8; color: #FFFFFF; box-shadow: 0 2px 6px rgba(26,115,232,0.28); }
    .ho-left-card { justify-content: flex-start !important; gap: 9px; padding: 13px 15px !important; }
    .ho-sub-list { list-style: none !important; padding-left: 0 !important; margin: 0 !important; display: flex; flex-direction: column; gap: 7px; }
    .ho-sub-list li { display: flex; align-items: flex-start; gap: 8px; font-size: 12.2px; line-height: 1.40; color: #3C4043; }
    .ho-sub-tag {
      font-family: var(--font-code); font-size: 9.8px; font-weight: 700;
      padding: 1.5px 6.5px; border-radius: 6px; background: #E8F0FE; color: #1A73E8;
      border: 1px solid #C6DAFC; flex-shrink: 0; margin-top: 1px;
    }
    .ho-sub-tag.green  { background: #E6F4EA; color: #137333; border-color: #A8DAB5; }
    .ho-sub-tag.red    { background: #FCE8E6; color: #C5221F; border-color: #F6AEA9; }
    .ho-sub-tag.yellow { background: #FEF7E0; color: #B06000; border-color: #FDE293; }
    .ho-theory-chip { display: inline-flex; align-items: center; gap: 6px; background: #F1F3F4; border: 1px solid #DADCE0; border-radius: 8px; padding: 4.5px 9px; font-size: 11px; color: #3C4043; width: fit-content; }
    .ho-right-col { display: flex; flex-direction: column; gap: 10px; min-height: 0; }
    .ho-code-card { background: #181A1F; border: 1px solid #3C4043; border-radius: 13px; padding: 9px 13px !important; gap: 6px; justify-content: flex-start !important; flex: 0 0 auto; }
    .ho-win-bar { display: flex; align-items: center; justify-content: space-between; gap: 8px; padding-bottom: 5px; border-bottom: 1px solid #2D3036; }
    .ho-dots { display: inline-flex; gap: 5px; align-items: center; margin-right: 6px; }
    .ho-dots span { width: 8.5px; height: 8.5px; border-radius: 50%; display: inline-block; }
    .ho-copy-btn { font-family: var(--font-title); font-size: 9.8px; font-weight: 600; padding: 2.5px 8.5px; border-radius: 7px; border: 1px solid #4A4E57; background: #262930; color: #E8EAED; cursor: pointer; }
    .ho-copy-btn:hover { background: #353942; }
    .ho-pre { margin: 0 !important; flex: 0 0 auto !important; border: none !important; background: transparent !important; padding: 2px 1px !important; font-size: 11px !important; line-height: 1.42 !important; color: #E8EAED; }
    .tok-todo { color: #FDD663; font-weight: 700; font-style: normal; background: rgba(253,214,99,0.12); padding: 0 4px; border-radius: 4px; }
    .tok-cm  { color: #7F8794; font-style: italic; }
    .ho-check-box { background: #FFFFFF; border: 1.2px solid #DADCE0; border-radius: 10px; padding: 7.5px 10px; display: flex; flex-direction: column; gap: 3px; }
    .ho-check-ttl { font-family: var(--font-title); font-size: 9.6px; font-weight: 800; color: #137333; letter-spacing: 0.03em; }
    .ho-check-items { font-size: 11px; color: #3C4043; line-height: 1.38; }
    .tok-kw  { color: #8AB4F8; font-weight: 600; }
    .tok-str { color: #81C995; }
    .tok-num { color: #FDD663; }
    .tok-fn  { color: #F28B82; }
    .ho-vis-card {
      flex: 1; min-height: 0; background: #FFFFFF; border: 1.5px solid #DADCE0; border-radius: 13px;
      display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 8px rgba(32,33,36,0.05);
    }
    .ho-vis-bar {
      background: #F8F9FA; border-bottom: 1px solid #E8EAED; padding: 5px 11px;
      display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-shrink: 0;
    }
    .ho-vis-body {
      flex: 1; min-height: 0; padding: 6px 8px; display: flex; align-items: center; justify-content: center; background: #FFFFFF;
    }
    .ho-vis-body img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; display: block; border-radius: 6px; }
    .ho-vis-cap {
      font-size: 10.4px; color: #5F6368; background: #FAFBFD; border-top: 1px solid #EEF0F3;
      padding: 4.5px 11px; flex-shrink: 0; line-height: 1.3;
    }
    .ho-term { margin-top: auto; background: #0F1115; border: 1px solid #2E323A; border-radius: 10px; overflow: hidden; }
    .ho-term-bar { background: #1E2128; padding: 4px 10px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #2E323A; }
    .ho-term-pre { margin: 0; padding: 8px 11px; font-family: var(--font-code); font-size: 10.9px; line-height: 1.42; color: #A8DAB5; white-space: pre-wrap; }

    /* Slide 42 Dark Finale */
    .finale-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; flex: 1; min-height: 0; margin-top: 8px; }
    .finale-card { background: #292A2D; border: 1px solid #3C4043; border-radius: 15px; padding: 15px 17px; color: #FFFFFF; display: flex; flex-direction: column; justify-content: flex-start; gap: 9px; position: relative; overflow: hidden; }
    .finale-top { display: flex; align-items: center; justify-content: space-between; margin-top: 4px; }
    .finale-pill { margin-top: auto; background: rgba(255,255,255,0.06); border: 1px solid #45474A; border-radius: 9px; padding: 7px 10px; font-size: 11.2px; color: #E8EAED; line-height: 1.35; }
    .finale-banner { margin-top: 11px; background: #292A2D; border: 1px solid #3C4043; border-left: 5px solid #34A853; border-radius: 13px; padding: 11px 16px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }
"""


def _qa_slide(
    *,
    qa_id: str,
    qa_num: int,
    kicker: str,
    title_html: str,
    question_html: str,
    choices: list[str],
    answer_html: str,
    vis_q_html: str,
    vis_a_html: str,
    notes: str,
    bar_color: str = "blue",
    correct_choice: str | None = None,
    data_title: str = "",
    quiz_progress_idx: int = 0,
) -> str:
    if correct_choice is None:
        m_ans = re.search(r"Jawaban:\s*([A-Z])\b", answer_html)
        assert m_ans, f"Tidak menemukan huruf jawaban pada {qa_id}: {answer_html[:60]}"
        correct_choice = m_ans.group(1).upper()
    choice_divs = []
    for idx_c, c in enumerate(choices):
        letter = chr(ord("A") + idx_c)
        is_ok = "true" if letter == correct_choice.upper() else "false"
        choice_divs.append(
            f'<div class="qa-choice clickable" data-qa="{qa_id}" data-correct="{is_ok}" '
            f'onclick="pickQAChoice(this, \'{qa_id}\')" role="button" tabindex="0">'
            f'<span>{c}</span><span class="qa-choice-badge"></span></div>'
        )
    choices_html = "\n            ".join(choice_divs)
    slide_dt = data_title or f"Tanya-Jawab #{qa_num}"
    if quiz_progress_idx > 0:
        dots = []
        for qi in range(1, 6):
            cls = "done" if qi < quiz_progress_idx else ("cur" if qi == quiz_progress_idx else "")
            mk = "✓ " if qi < quiz_progress_idx else ""
            dots.append(f'<span class="ho-step-dot {cls}">{mk}Soal {qi}</span>')
        head_html = f"""<div class="ho-head-row" style="margin-bottom:10px;">
        <div>
          <div class="kicker">{kicker}</div>
          <h2 style="margin-bottom:0;">{title_html}</h2>
        </div>
        <div class="ho-stepper">{"".join(dots)}</div>
      </div>"""
    else:
        head_html = f"""<div class="kicker">{kicker}</div>
      <h2>{title_html}</h2>"""
    return f"""
    <section class="slide" data-title="{slide_dt}" data-notes="{notes}">
      {head_html}
      <div class="split-60-40" style="align-items:stretch;">
        <div class="qa-box" style="justify-content:center; gap:10px;">
          <div class="qa-question" style="font-size:15.2px;">{question_html}</div>
          <div style="display:flex; flex-direction:column; gap:7px;">
            {choices_html}
          </div>
          <button class="btn-ui" onclick="toggleQA('{qa_id}', this)">Klik untuk Lihat Jawaban &amp; Penjelasan</button>
          <div id="{qa_id}" class="qa-answer" style="padding:10px 14px; font-size:12.4px; line-height:1.45;">{answer_html}</div>
        </div>
        <div id="{qa_id}-vis" class="card surface" style="justify-content:center; align-items:center; text-align:center; gap:8px; padding:14px 16px;">
          <div class="card-top-bar bar-{bar_color}"></div>
          <div class="vis-q" style="width:100%;">{vis_q_html}</div>
          <div class="vis-a" style="width:100%;">{vis_a_html}</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""


_PY_TOKEN_RE = re.compile(
    r'(?P<todo>#\s*TODO[^\n]*)'
    r'|(?P<cm>#[^\n]*)'
    r'|(?P<str>"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27)'
    r'|(?P<kw>\b(?:def|return|for|in|if|else|assert|import|from|as|None|True|False)\b)'
    r'|(?P<fn>\b(?:print|len|np|pd|tf|plt|tampilkan_piksel_grid|tampilkan_zoom_piksel|tampilkan_visual_flatten|tampilkan_skala_parameter|tampilkan_timbangan_neuron|tampilkan_relu|tampilkan_softmax_frozen|tampilkan_tebakan_model|tampilkan_kurva_training|tampilkan_peta_bobot)\b)'
    r'|(?P<num>\b\d+(?:\.\d+)?\b)'
)


def _highlight_py(snippet: str) -> str:
    """Syntax-highlight short Python snippets into clean dark-theme spans (zero tag nesting issues)."""
    out: list[str] = []
    pos = 0
    for m in _PY_TOKEN_RE.finditer(snippet):
        if m.start() > pos:
            out.append(html_lib.escape(snippet[pos : m.start()]))
        kind = m.lastgroup or ""
        tok = html_lib.escape(m.group(0))
        out.append(f'<span class="tok-{kind}">{tok}</span>')
        pos = m.end()
    if pos < len(snippet):
        out.append(html_lib.escape(snippet[pos:]))
    return "".join(out)


def _handson_step_slide(
    *,
    step_num: int,
    stage_badge: str,
    title: str,
    kicker: str,
    goal_html: str,
    bullets_html: str,
    code_snippet: str,
    callout_html: str,
    color: str,
    notes: str,
    theory_ref: str = "",
    output_img: str = "",
    output_caption: str = "",
    checklist_html: str = "",
) -> str:
    step_labels = ["1. Piksel", "2. Flatten", "3. Neuron", "4. Model", "5. Fit", "6. Tebak"]
    stepper_items = []
    for idx_s, lbl_s in enumerate(step_labels, 1):
        cls_s = "done" if idx_s < step_num else ("cur" if idx_s == step_num else "")
        mark_s = "✓ " if idx_s < step_num else ""
        stepper_items.append(f'<span class="ho-step-dot {cls_s}">{mark_s}{lbl_s}</span>')
    stepper_html = "\n          ".join(stepper_items)

    theory_html = (
        f'<div class="ho-theory-chip"><span>🔗</span><span><strong>Bab 3:</strong> {theory_ref}</span></div>'
        if theory_ref
        else ""
    )
    check_html = (
        f'<div class="ho-check-box"><div class="ho-check-ttl">🎯 CEK BERHASIL</div><div class="ho-check-items">{checklist_html}</div></div>'
        if checklist_html
        else ""
    )
    hl_code = _highlight_py(code_snippet)
    vis_html = (
        f"""
          <div class="ho-vis-card">
            <div class="ho-vis-bar">
              <span style="font-family:var(--font-title); font-size:9.6px; font-weight:800; color:#137333; letter-spacing:0.03em;">● OUTPUT VISUAL NYATA (DATA FROZEN v1)</span>
              <span style="font-family:var(--font-code); font-size:9.4px; color:#5F6368;">Hasil langsung di bawah sel</span>
            </div>
            <div class="ho-vis-body">
              <img src="{output_img}" alt="Visual Output {html_lib.escape(title)}" />
            </div>
            <div class="ho-vis-cap">{output_caption}</div>
          </div>"""
        if output_img
        else ""
    )
    return f"""
    <section class="slide" data-title="Hands-On {stage_badge}: {title}" data-notes="{notes}">
      <div class="ho-head-row">
        <div>
          <div class="kicker">{kicker}</div>
          <h2 style="margin-bottom:0;">{stage_badge}: <span class="hl-{color}">{title}</span></h2>
        </div>
        <div class="ho-stepper">
          {stepper_html}
        </div>
      </div>
      <div class="ho-layout">
        <div class="card surface ho-left-card">
          <div class="card-top-bar bar-{color}"></div>
          <div>
            <span class="pill {color}">{stage_badge.upper()} · NOTEBOOK P02</span>
            <div class="card-title" style="margin-top:6px; font-size:15px;">{goal_html}</div>
          </div>
          <ul class="ho-sub-list">{bullets_html}</ul>
          {theory_html}
          {check_html}
          <div class="callout {color if color != 'blue' else ''}" style="margin-top:auto; padding:7.5px 10.5px; font-size:11.3px;">{callout_html}</div>
        </div>
        <div class="ho-right-col">
          <div class="card ho-code-card">
            <div class="ho-win-bar">
              <div style="display:flex; align-items:center;">
                <span class="ho-dots"><span style="background:#EA4335;"></span><span style="background:#FBBC04;"></span><span style="background:#34A853;"></span></span>
                <span class="pill dark" style="font-size:10px; padding:1.5px 8px;">p02_teori_neural_network.ipynb</span>
              </div>
              <div style="display:flex; align-items:center; gap:7px;">
                <span style="font-family:var(--font-code); font-size:10px; color:#9AA0A6;">3–6 baris · Shift+Enter</span>
                <button type="button" class="ho-copy-btn" onclick="copyHandsOnCode(this, 'ho-code-{step_num}')">Salin</button>
              </div>
            </div>
            <pre class="code ho-pre"><code id="ho-code-{step_num}">{hl_code}</code></pre>
          </div>
          {vis_html}
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""


def build_slides_html(data: dict) -> str:
    total_imgs = data["total_images"]
    ho_m = data.get("handson_metrics", {})
    e0_loss = ho_m.get("epoch0_loss", 1.71)
    e0_acc = ho_m.get("epoch0_acc_pct", 24.5)
    e1_loss = ho_m.get("epoch1_loss", 2.41)
    e_end = ho_m.get("epochs", 20)
    e_end_loss = ho_m.get("epoch_end_loss", 1.04)
    e_end_acc = ho_m.get("epoch_end_acc_pct", 65.7)
    s_e0 = ho_m.get("sample_e0_correct", 2)
    s_end = ho_m.get("sample_end_correct", 4)
    ho_z_gaun = ho_m.get("neuron_z", 0.33)
    ho_z_wall = ho_m.get("wall_z", -0.23)
    ho_loss_sm = ho_m.get("softmax_loss_demo", 0.38)
    polos_n = data["polos_count"]
    ramai_n = data["ramai_count"]
    sessions_n = data["sessions_count"]
    fp = data["mini_forward_pass"]
    x0, x1, x2, x3 = fp["x"]
    h0, h1 = fp["h1"]
    l0, l1 = fp["logits"]
    p0, p1 = fp["probs"]
    er0, eg0, eb0 = data["elsa_rgb_ends"]["first_rgb"]
    er_end, eg_end, eb_end = data["elsa_rgb_ends"]["last_rgb"]

    s: list[str] = []

    # =========================================================================
    # PEMBUKA (SLIDE 01–06 · 6.0 MENIT)
    # =========================================================================
    s.append(
        f"""
    <!-- 01: COVER -->
    <section class="slide active" data-title="Cover — Teori Neural Network" data-notes="Alokasi waktu: 1 menit. Selamat datang di P02 Teori Neural Network! Kita mulai dari peta AI, ML, dan DL beserta 4 tugas Computer Vision, lalu membedah cara kerja Neural Network dari 1 piksel sampai Backpropagation secara menyeluruh." style="background: radial-gradient(circle at 82% 46%, rgba(234,67,53,0.12) 0%, rgba(66,133,244,0.10) 35%, rgba(251,188,4,0.08) 60%, #FFFFFF 100%); justify-content: space-between;">
      <svg viewBox="0 0 960 540" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:0;">
        <circle cx="885" cy="72" r="24" fill="#FCE8E6" stroke="#EA4335" stroke-width="2" opacity="0.85"/>
        <rect x="640" y="54" width="22" height="22" rx="7" transform="rotate(18 651 65)" fill="#E8F0FE" stroke="#4285F4" stroke-width="2" opacity="0.8"/>
        <polygon points="560,415 574,439 546,439" fill="#E6F4EA" stroke="#34A853" stroke-width="2" opacity="0.8"/>
        <circle cx="912" cy="402" r="14" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2" opacity="0.85"/>
      </svg>

      <div style="position:relative; z-index:1;">
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
      </div>

      <div style="position:relative; z-index:1; display:grid; grid-template-columns: 1.24fr 1fr; align-items:center; gap:24px; margin:auto 0;">
        <div>
          <h1 style="font-family:var(--font-title); font-size:42px; font-weight:700; line-height:1.1; color:#202124; margin:0; letter-spacing:-0.6px;">
            P02 — Teori<br />
            <span style="display:inline-block; padding-top:2px; background:linear-gradient(90deg, #EA4335 0%, #4285F4 55%, #34A853 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Neural Network</span>
          </h1>
          <div style="height:4px; width:100%; max-width:520px; border-radius:999px; margin:10px 0 12px; background:linear-gradient(90deg, #4285F4 0%, #EA4335 35%, #FBBC04 70%, #34A853 100%);"></div>
          <div style="font-size:15.8px; font-weight:500; color:#5F6368; line-height:1.45;">
            Memahami <strong>AI · ML · DL</strong> &amp; 4 Tugas <em>Computer Vision</em>,<br />
            hingga Cara Kerja <strong>Neural Network</strong> dari 1 Piksel sampai <em>Backpropagation</em>
          </div>
          <div style="margin-top:14px; display:inline-flex; align-items:center; gap:8px; background:#FFFFFF; border:1.5px solid #E0E3E7; border-radius:999px; padding:5px 14px 5px 7px; box-shadow:0 3px 10px rgba(234,67,53,0.08);">
            <span style="width:24px; height:24px; border-radius:50%; background:linear-gradient(135deg, #EA4335, #4285F4); color:#FFFFFF; font-family:var(--font-title); font-size:11px; font-weight:700; display:inline-flex; align-items:center; justify-content:center;">MH</span>
            <span style="font-size:13.5px; color:#5F6368;">Presented by <strong style="color:#202124; font-weight:700;">Muhammad Haerul</strong></span>
          </div>
        </div>

        <div style="background:rgba(255,255,255,0.94); border:1.5px solid #E0E3E7; border-radius:18px; padding:13px 14px; box-shadow:0 12px 30px rgba(32,33,36,0.08); display:flex; flex-direction:column; gap:10px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-family:var(--font-title); font-size:10.5px; font-weight:700; letter-spacing:0.06em; color:#5F6368;">DATASET PROYEK · 5 KARAKTER FROZEN</span>
            <span style="font-family:var(--font-code); font-size:10px; font-weight:700; color:#1A73E8; background:#E8F0FE; padding:2px 7px; border-radius:999px;">Foto Asli</span>
          </div>

          <!-- 1+4 Bento Collage of all 5 Frozen Characters -->
          <div style="display:grid; grid-template-columns:1.12fr 1fr 1fr; grid-template-rows:108px 108px; gap:7px;">
            <div style="grid-row:span 2; position:relative; border-radius:11px; overflow:hidden; border:2.5px solid #4285F4; box-shadow:0 3px 10px rgba(66,133,244,0.16);">
              <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:100%; height:100%; object-fit:cover; object-position:center 35%; display:block;"/>
              <div style="position:absolute; inset:7px; border:1.5px dashed rgba(255,255,255,0.75); border-radius:7px; pointer-events:none;"></div>
              <span style="position:absolute; left:6px; bottom:6px; background:#4285F4; color:#FFFFFF; font-family:var(--font-title); font-size:10px; font-weight:700; padding:2px 8px; border-radius:6px;">Elsa</span>
            </div>
            <div style="position:relative; border-radius:10px; overflow:hidden; border:2px solid #EA4335;">
              <img src="assets/P02/thumb_anna.jpg" alt="Anna" style="width:100%; height:100%; object-fit:cover; object-position:center 15%; display:block;"/>
              <span style="position:absolute; left:5px; bottom:5px; background:rgba(234,67,53,0.92); color:#FFFFFF; font-family:var(--font-title); font-size:9.2px; font-weight:700; padding:1px 6px; border-radius:5px;">Anna</span>
            </div>
            <div style="position:relative; border-radius:10px; overflow:hidden; border:2px solid #FBBC04;">
              <img src="assets/P02/thumb_kristoff.jpg" alt="Kristoff" style="width:100%; height:100%; object-fit:cover; object-position:center 15%; display:block;"/>
              <span style="position:absolute; left:5px; bottom:5px; background:#FBBC04; color:#202124; font-family:var(--font-title); font-size:9.2px; font-weight:700; padding:1px 6px; border-radius:5px;">Kristoff</span>
            </div>
            <div style="position:relative; border-radius:10px; overflow:hidden; border:2px solid #34A853;">
              <img src="assets/P02/thumb_olaf.jpg" alt="Olaf" style="width:100%; height:100%; object-fit:cover; object-position:center 18%; display:block;"/>
              <span style="position:absolute; left:5px; bottom:5px; background:rgba(52,168,83,0.94); color:#FFFFFF; font-family:var(--font-title); font-size:9.2px; font-weight:700; padding:1px 6px; border-radius:5px;">Olaf</span>
            </div>
            <div style="position:relative; border-radius:10px; overflow:hidden; border:2px solid #1A73E8;">
              <img src="assets/P02/thumb_sven.jpg" alt="Sven" style="width:100%; height:100%; object-fit:cover; object-position:center 18%; display:block;"/>
              <span style="position:absolute; left:5px; bottom:5px; background:rgba(26,115,232,0.94); color:#FFFFFF; font-family:var(--font-title); font-size:9.2px; font-weight:700; padding:1px 6px; border-radius:5px;">Sven</span>
            </div>
          </div>

          <!-- Compact Pipeline Strip: Piksel -> Neural Network -> 5 Kelas -->
          <div style="background:#F8F9FA; border:1px solid #E0E3E7; border-radius:12px; padding:7px 10px; display:flex; align-items:center; justify-content:space-between; gap:8px;">
            <div style="text-align:center;">
              <div style="font-family:var(--font-title); font-size:10.5px; font-weight:700; color:#1A73E8;">Input Piksel</div>
              <div style="font-family:var(--font-code); font-size:9.5px; color:#5F6368;">224×224×3</div>
            </div>
            <span style="font-weight:700; color:#5F6368; font-size:13px;">→</span>
            <svg viewBox="0 0 124 58" style="width:116px; height:52px; flex-shrink:0;">
              <g stroke="#CFD4DA" stroke-width="1.15" opacity="0.85">
                <line x1="18" y1="9" x2="106" y2="9"/><line x1="18" y1="9" x2="106" y2="19"/><line x1="18" y1="9" x2="106" y2="29"/><line x1="18" y1="9" x2="106" y2="39"/><line x1="18" y1="9" x2="106" y2="49"/>
                <line x1="18" y1="19" x2="106" y2="9"/><line x1="18" y1="19" x2="106" y2="19"/><line x1="18" y1="19" x2="106" y2="29"/><line x1="18" y1="19" x2="106" y2="39"/><line x1="18" y1="19" x2="106" y2="49"/>
                <line x1="18" y1="29" x2="106" y2="9"/><line x1="18" y1="29" x2="106" y2="19"/><line x1="18" y1="29" x2="106" y2="29"/><line x1="18" y1="29" x2="106" y2="39"/><line x1="18" y1="29" x2="106" y2="49"/>
                <line x1="18" y1="39" x2="106" y2="9"/><line x1="18" y1="39" x2="106" y2="19"/><line x1="18" y1="39" x2="106" y2="29"/><line x1="18" y1="39" x2="106" y2="39"/><line x1="18" y1="39" x2="106" y2="49"/>
                <line x1="18" y1="49" x2="106" y2="9"/><line x1="18" y1="49" x2="106" y2="19"/><line x1="18" y1="49" x2="106" y2="29"/><line x1="18" y1="49" x2="106" y2="39"/><line x1="18" y1="49" x2="106" y2="49"/>
              </g>
              <g stroke="#4285F4" stroke-width="1.6" opacity="0.72">
                <line x1="18" y1="19" x2="106" y2="19"/><line x1="18" y1="29" x2="106" y2="19"/><line x1="18" y1="39" x2="106" y2="19"/>
              </g>
              <rect x="46" y="20" width="32" height="18" rx="6" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.3"/>
              <text x="62" y="32" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="800" fill="#B06000">W + b</text>
              <circle cx="18" cy="9" r="4.3" fill="#EA4335" stroke="#FFF" stroke-width="1.2"/>
              <circle cx="18" cy="19" r="4.3" fill="#34A853" stroke="#FFF" stroke-width="1.2"/>
              <circle cx="18" cy="29" r="4.3" fill="#4285F4" stroke="#FFF" stroke-width="1.2"/>
              <circle cx="18" cy="39" r="4.3" fill="#4285F4" stroke="#FFF" stroke-width="1.2"/>
              <circle cx="18" cy="49" r="4.3" fill="#4285F4" stroke="#FFF" stroke-width="1.2"/>
              <circle cx="106" cy="9" r="4.2" fill="#4285F4" stroke="#FFF" stroke-width="1.2"/>
              <circle cx="106" cy="19" r="5.0" fill="#34A853" stroke="#FFF" stroke-width="1.3"/>
              <circle cx="106" cy="29" r="4.2" fill="#FBBC04" stroke="#FFF" stroke-width="1.2"/>
              <circle cx="106" cy="39" r="4.2" fill="#EA4335" stroke="#FFF" stroke-width="1.2"/>
              <circle cx="106" cy="49" r="4.2" fill="#5F6368" stroke="#FFF" stroke-width="1.2"/>
            </svg>
            <span style="font-weight:700; color:#5F6368; font-size:13px;">→</span>
            <div style="text-align:center;">
              <div style="font-family:var(--font-title); font-size:10.5px; font-weight:700; color:#137333;">5 Kelas</div>
              <div style="font-family:var(--font-code); font-size:9.5px; color:#5F6368;">Neural Network</div>
            </div>
          </div>
        </div>
      </div>

      <div style="position:relative; z-index:1; display:flex; gap:6px; flex-wrap:wrap; align-items:center;">
        <span class="pill blue" style="font-size:10.5px; padding:4px 10px;">AI vs ML vs DL</span>
        <span class="pill red" style="font-size:10.5px; padding:4px 10px;">4 CV Tasks</span>
        <span class="pill green" style="font-size:10.5px; padding:4px 10px;">Neuron → Layer → Network</span>
        <span class="pill yellow" style="font-size:10.5px; padding:4px 10px;">{"Backpropagation" if HIDE_BAB4_ARCH else "Arsitektur CV"}</span>
        <span class="pill solid-blue" style="font-size:10.5px; padding:4px 12px;">NumPy</span>
        <span class="pill" style="background:#EA4335; color:#FFFFFF; font-size:10.5px; padding:4px 12px;">Keras</span>
      </div>
    </section>

    <!-- 02: AGENDA & LEARNING GOALS (GABUNGAN PETA + ALUR 120M + TUJUAN) -->
    <section class="slide" data-title="Agenda &amp; Learning Goals (120 Menit)" data-notes="Alokasi waktu: 2 menit. Satu slide ringkas yang menyatukan agenda 3 bab teori (Bab 1: 9m, Bab 2: 9.5m, Bab 3: 29.5m), kuis 5 soal, kamus 14 istilah &amp; Referensi Materi (7.5m), serta sesi hands-on 5 tahap mikro-task &amp; penutup (58.5m) beserta 3 target belajar utama.">
      <div class="kicker">SESSION OVERVIEW · 120 MENIT</div>
      <h2>Agenda &amp; <span class="hl-blue">Learning Goals</span></h2>
      <div class="split-60-40" style="flex:1; min-height:0; align-items:stretch;">
        <div class="step-list" style="display:flex; flex-direction:column; justify-content:space-between; gap:8px; height:100%;">
          <div class="step-item" style="padding:10px 13px; flex:1; align-items:center;">
            <div class="step-num">01</div>
            <div style="flex:1;">
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">Bab 1: AI vs Machine Learning vs Deep Learning</span>
                <span class="pill blue" style="font-size:10px; padding:2px 8px; white-space:nowrap;">~9 menit</span>
              </div>
              <div class="step-desc">Bukan AI vs AI Klasik vs AI Modern, paradigma belajar ML, dan beda spesifik ML vs DL.</div>
            </div>
          </div>
          <div class="step-item" style="padding:10px 13px; flex:1; align-items:center;">
            <div class="step-num red">02</div>
            <div style="flex:1;">
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">Bab 2: 4 Tugas Utama Computer Vision</span>
                <span class="pill red" style="font-size:10px; padding:2px 8px; white-space:nowrap;">~9,5 menit</span>
              </div>
              <div class="step-desc"><em>Classification, Object Detection, Semantic &amp; Instance Segmentation,</em> &amp; <em>Object Tracking</em>.</div>
            </div>
          </div>
          <div class="step-item" style="padding:10px 13px; flex:1; align-items:center;">
            <div class="step-num green">03</div>
            <div style="flex:1;">
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">Bab 3: Bedah Total Neural Network (Tahap 1–5)</span>
                <span class="pill green" style="font-size:10px; padding:2px 8px; white-space:nowrap;">{"~29,5 menit" if HIDE_BAB4_ARCH else ("~22 menit" if HIDE_SLIDES_28_40 else "~27 menit")}</span>
              </div>
              <div class="step-desc">1 Piksel → <em>Flatten</em> → <em>Dense</em> &amp; Parameter → <em>Weight/Bias</em>, Aktivasi → <em>Backprop</em>, <em>LR/Adam</em>, <em>Batch</em> &amp; <em>Overfitting</em> → Full NN.</div>
            </div>
          </div>
          <div class="step-item" style="padding:10px 13px; flex:1; align-items:center;">
            <div class="step-num yellow">Q</div>
            <div style="flex:1;">
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">Kuis 5 Soal, Kamus Istilah &amp; Referensi Materi</span>
                <span class="pill yellow" style="font-size:10px; padding:2px 8px; white-space:nowrap;">~7,5 menit</span>
              </div>
              <div class="step-desc">5 slide kuis berilustrasi Bab 1–3, kamus <strong>14 istilah kunci</strong>, dan Referensi Materi Bab 1–3.</div>
            </div>
          </div>
          <div class="step-item" style="padding:10px 13px; flex:1; align-items:center;">
            <div class="step-num">HO</div>
            <div style="flex:1;">
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">Hands-On Notebook &amp; Rangkuman Penutup</span>
                <span class="pill dark" style="font-size:10px; padding:2px 8px; white-space:nowrap;">~58,5 menit</span>
              </div>
              <div class="step-desc">5 tahap mikro-task visual-first NumPy &amp; Keras pada foto Frozen (55,5m) → 3 Poin Utama (3m).</div>
            </div>
          </div>
        </div>

        <div class="card surface" style="justify-content:space-between; padding:15px 17px; gap:10px; height:100%;">
          <div class="card-top-bar bar-green"></div>
          <div>
            <span class="pill green">3 LEARNING GOALS</span>
            <div class="card-title" style="margin-top:6px;">Yang Akan Kamu Kuasai</div>
          </div>
          <div style="display:flex; flex-direction:column; gap:10px; flex:1; justify-content:space-between;">
            <div class="mini-box" style="background:var(--tint-blue); border-color:#C6DAFC; flex:1; display:flex; align-items:center; padding:10px 13px; font-size:12.6px; line-height:1.42;">
              <div><strong>1. Peta AI &amp; Task CV:</strong> Tepat membedakan AI/ML/DL dan memilih <em>Image Classification</em> untuk proyek Frozen.</div>
            </div>
            <div class="mini-box" style="background:var(--tint-green); border-color:#A8DAB5; flex:1; display:flex; align-items:center; padding:10px 13px; font-size:12.6px; line-height:1.42;">
              <div><strong>2. Bedah Neural Network:</strong> Paham alur 1 Piksel → <em>Flatten</em> &amp; <em>Dense</em> → <em>Weight &amp; Bias</em> → <em>Softmax</em> → <em>Backprop</em>, <em>Adam</em> &amp; <em>Overfitting</em>.</div>
            </div>
            <div class="mini-box" style="background:var(--tint-red); border-color:#F6AEA9; flex:1; display:flex; align-items:center; padding:10px 13px; font-size:12.6px; line-height:1.42;">
              <div><strong>3. Bukti di Kode Nyata:</strong> Membangun Neural Network 1-Layer di NumPy &amp; Keras lalu mencocokkan <code>model.summary()</code> dengan hitungan tangan — siap menuju P03!</div>
            </div>
          </div>
          <div class="callout" style="padding:8px 11px; font-size:12px;"><strong>Ritme 120 Menit:</strong> 61,5m pembuka, Bab 1–3, kuis &amp; kamus → <strong>58,5m</strong> hands-on praktik &amp; rangkuman penutup.</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 03: PEMANASAN RECAP P01 -->
    <section class="slide" data-title="Pemanasan: Recap P01 — Foto = Matriks Angka" data-notes="Alokasi waktu: 2 menit. Kita menyambung langsung dari akhir P01: komputer tidak melihat boneka Elsa seperti mata kita, melainkan melihat matriks angka piksel RGB berskala 0 sampai 1 dari dataset proyek Frozen kita — tunjuk contoh 1 piksel gaun biru Elsa [0.52, 0.53, 0.60] sebagai jembatan ke Bab 3 dan Hands-On.">
      <div class="kicker">PEMANASAN · RECAP P01</div>
      <h2>Menyambung P01: Foto Frozen di Mata Komputer = <span class="hl-blue">Matriks Angka</span></h2>
      <div class="split-60-40" style="flex:1; min-height:0; align-items:stretch;">
        <div style="display:flex; flex-direction:column; gap:9px; min-height:0;">
          <div class="img-box" style="flex:1; min-height:0; padding:8px; display:flex; align-items:center; justify-content:center; background:#FFFFFF;">
            <img src="assets/P02/01_frozen_gallery_5classes.png" alt="Galeri 5 Karakter Disney Frozen Polos vs Ramai" style="width:100%; height:100%; object-fit:contain;" />
          </div>
          <div class="kpi-strip">
            <div class="kpi-mini"><div class="k-num">{total_imgs}</div><div class="k-lbl">Foto Asli (v1)</div></div>
            <div class="kpi-mini"><div class="k-num" style="color:#137333;">5 Kelas</div><div class="k-lbl">Anna s.d. Sven</div></div>
            <div class="kpi-mini"><div class="k-num" style="color:#EA4335;">{polos_n} / {ramai_n}</div><div class="k-lbl">Polos vs Ramai</div></div>
            <div class="kpi-mini"><div class="k-num" style="color:#B06000;">{sessions_n} Sesi</div><div class="k-lbl">Sesi Foto</div></div>
          </div>
        </div>
        <div class="card surface" style="gap:10px; justify-content:space-between; padding:15px 17px;">
          <div class="card-top-bar bar-blue"></div>
          <div>
            <div class="card-title" style="margin-bottom:6px;">Modal dari P01 yang Kita Bawa Hari Ini</div>
            <div class="card-body" style="font-size:12.8px; line-height:1.45;">
              <ul style="gap:6px;">
                <li>Setiap foto warna adalah array 3D berukuran <code>(Tinggi, Lebar, 3)</code> — misalnya setelah di-<em>resize</em> menjadi <code>(224, 224, 3)</code>.</li>
                <li>Angka piksel asli <code>0–255</code> dinormalisasi menjadi <code>0.0–1.0</code> (<code>float32</code>) agar perhitungan komputer stabil.</li>
                <li>Dataset proyek kita berisi <strong>5 karakter Disney Frozen</strong> dalam 2 kondisi latar: <strong>Polos</strong> dan <strong>Ramai</strong>.</li>
              </ul>
            </div>
          </div>

          <!-- Visual Bridge Card: P01 -> P02 (Real Elsa Dress Pixel [4,2] RGB -> 150.528 numbers!) -->
          <div style="background:#FFFFFF; border:1.5px solid #C6DAFC; border-radius:12px; padding:10px 12px; display:flex; flex-direction:column; gap:7px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-family:var(--font-title); font-size:10.5px; font-weight:800; color:#1A73E8;">JEMBATAN P01 → P02 · 1 PIKSEL GAUN ELSA</span>
              <span style="font-family:var(--font-code); font-size:9.5px; font-weight:700; color:#5F6368;">Skala 0.0–1.0</span>
            </div>
            <div style="display:grid; grid-template-columns:56px 1fr; gap:10px; align-items:center;">
              <div style="width:56px; height:56px; border-radius:10px; background:rgb(133,135,153); border:2px solid #4285F4; display:flex; align-items:flex-end; justify-content:center; padding-bottom:3px; box-shadow:0 3px 8px rgba(66,133,244,0.18);">
                <span style="font-family:var(--font-code); font-size:8px; font-weight:800; color:#FFFFFF; background:rgba(32,33,36,0.55); border-radius:4px; padding:1px 4px;">[4, 2]</span>
              </div>
              <div style="display:flex; flex-direction:column; gap:4px; font-family:var(--font-code); font-size:10px;">
                <div style="display:flex; align-items:center; gap:6px;"><span style="width:22px; font-weight:800; color:#EA4335;">R:</span><div style="flex:1; height:8px; background:#FCE8E6; border-radius:4px; overflow:hidden;"><div style="width:52%; height:100%; background:#EA4335;"></div></div><strong style="width:44px; text-align:right; white-space:nowrap;">0.52</strong></div>
                <div style="display:flex; align-items:center; gap:6px;"><span style="width:22px; font-weight:800; color:#137333;">G:</span><div style="flex:1; height:8px; background:#E6F4EA; border-radius:4px; overflow:hidden;"><div style="width:53%; height:100%; background:#34A853;"></div></div><strong style="width:44px; text-align:right; white-space:nowrap;">0.53</strong></div>
                <div style="display:flex; align-items:center; gap:6px;"><span style="width:22px; font-weight:800; color:#1A73E8;">B:</span><div style="flex:1; height:8px; background:#E8F0FE; border-radius:4px; overflow:hidden;"><div style="width:60%; height:100%; background:#4285F4;"></div></div><strong style="width:44px; text-align:right; color:#1A73E8; white-space:nowrap;">0.60 ★</strong></div>
              </div>
            </div>
            <div style="font-size:10.6px; color:#5F6368; background:#F8F9FA; border-radius:7px; padding:4.5px 8px; text-align:center;">
              1 foto <code>224×224×3</code> = <strong style="color:#1A73E8;">150.528 angka</strong> seperti ini masuk ke Neural Network!
            </div>
          </div>

          <div class="callout" style="padding:9px 12px; font-size:12.4px;"><strong>Pertanyaan besar hari ini:</strong> Setelah foto jadi <code>150.528</code> angka <code>0.0–1.0</code>, bagaimana komputer bisa menebak isinya?</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    # 06: PEMANASAN Q&A REVEAL #1
    s.append(
        _qa_slide(
            qa_id="qa-warmup",
            qa_num=1,
            kicker="PEMANASAN · TANYA-JAWAB #1",
            title_html='Bagaimana Komputer Tahu <span class="hl-red">Ini Foto Elsa?</span>',
            question_html="Komputer hanya melihat ribuan angka piksel <code>0.0–1.0</code>. Menurutmu, cara mana yang paling mungkin berhasil membedakan Elsa di latar polos maupun latar rak yang ramai?",
            choices=[
                "<strong>A.</strong> Menulis aturan manual: <code>if warna_biru &gt; 30%: return 'Elsa'</code>",
                "<strong>B.</strong> Memberi komputer banyak contoh foto berlabel, lalu membiarkannya belajar pola angka sendiri lewat <em>Neural Network</em>",
                "<strong>C.</strong> Membandingkan ukuran file JPEG (KB) masing-masing foto",
            ],
            answer_html="<strong>Jawaban: B!</strong> Aturan manual (A) langsung gagal jika latar ramai punya benda biru atau pencahayaan redup. Dengan <strong>Deep Learning (Neural Network)</strong>, komputer mempelajari pola angka langsung dari contoh foto berlabel.",
            vis_q_html='''<div style="display:flex; flex-direction:column; gap:12px; width:100%; align-items:center;">
              <span class="pill red" style="font-size:10px; padding:3px 10px;">TANTANGAN NYATA DATASET FROZEN</span>
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; width:100%;">
                <div style="background:#FFFFFF; border:1.5px solid #C6DAFC; border-radius:12px; padding:7px; text-align:center;">
                  <img src="assets/P02/thumb_elsa.jpg" alt="Elsa latar polos" style="width:100%; height:172px; object-fit:cover; border-radius:9px; display:block;"/>
                  <div style="margin-top:6px; font-family:var(--font-title); font-size:11px; font-weight:700; color:#1A73E8;">Kondisi 1 · Latar Polos</div>
                </div>
                <div style="background:#FFFFFF; border:1.5px solid #F6AEA9; border-radius:12px; padding:7px; text-align:center;">
                  <img src="assets/P02/thumb_elsa_ramai.jpg" alt="Elsa latar ramai" style="width:100%; height:172px; object-fit:cover; border-radius:9px; display:block;"/>
                  <div style="margin-top:6px; font-family:var(--font-title); font-size:11px; font-weight:700; color:#C5221F;">Kondisi 2 · Latar Rak Ramai</div>
                </div>
              </div>
              <div style="font-size:12px; color:#5F6368; line-height:1.4; text-align:center; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:10px; padding:8px 11px; width:100%;">
                Keduanya adalah <strong>Elsa</strong> — perhatikan ada banyak objek &amp; warna lain di latar belakang foto kanan!
              </div>
            </div>''',
            vis_a_html='''<div style="display:flex; flex-direction:column; gap:10px; width:100%; align-items:center;">
              <span class="pill green" style="font-size:10px; padding:3px 10px;">KENAPA NEURAL NETWORK MENANG?</span>
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; width:100%;">
                <div style="background:#FFFFFF; border:2px solid #34A853; border-radius:12px; padding:6px; text-align:center;">
                  <img src="assets/P02/thumb_elsa.jpg" alt="Elsa latar polos" style="width:100%; height:148px; object-fit:cover; border-radius:8px; display:block;"/>
                  <div style="margin-top:5px; font-family:var(--font-title); font-size:10.5px; font-weight:700; color:#137333;">Polos ✓</div>
                </div>
                <div style="background:#FFFFFF; border:2px solid #34A853; border-radius:12px; padding:6px; text-align:center;">
                  <img src="assets/P02/thumb_elsa_ramai.jpg" alt="Elsa latar ramai" style="width:100%; height:148px; object-fit:cover; border-radius:8px; display:block;"/>
                  <div style="margin-top:5px; font-family:var(--font-title); font-size:10.5px; font-weight:700; color:#137333;">Ramai ✓ (ada kuda biru!)</div>
                </div>
              </div>
              <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; width:100%; text-align:left; font-size:12px; line-height:1.42; padding:9px 12px;">
                <strong>Belajar dari Contoh:</strong> Aturan manual (A) tertipu kuda biru di belakang Elsa. <em>Neural Network</em> mempelajari kombinasi pola wajah, rambut, dan gaun secara otomatis dari data berlabel!
              </div>
            </div>''',
            notes="Alokasi waktu: 1 menit. Minta peserta menebak dulu sebelum tombol jawaban dibuka. Ini menjadi pintu masuk sempurna ke Bab 1 (AI vs ML vs DL).",
            bar_color="red",
        )
    )

    # =========================================================================
    # BAB 1: AI VS ML VS DL (SLIDE 07–11 · 6.0 MENIT)
    # =========================================================================
    s.append(
        make_divider_slide(
            bg_class="bg-blue",
            kicker="BAB 01 · GAMBARAN BESAR",
            title="AI vs Machine Learning vs Deep Learning",
            description="Tiga istilah yang sering dicampuradukkan — padahal membentuk hierarki subset: Deep Learning adalah bagian dari Machine Learning, dan Machine Learning adalah bagian dari AI.",
            footer_label=FOOTER,
            data_title="Bab 1 — AI vs ML vs DL",
            notes="Alokasi waktu: 0.5 menit. Masuk Bab 1: meluruskan tiga istilah paling sering terdengar (AI, ML, DL) supaya peserta punya peta besar sebelum masuk ke Computer Vision.",
        )
    )

    s.append(
        f"""
    <!-- 08: ARTIFICIAL INTELLIGENCE (AI) -->
    <section class="slide" data-title="Bab 1: Apa Itu Artificial Intelligence (AI)?" data-notes="Alokasi waktu: 1.5 menit. Definisi akurat AI: bidang ilmu komputer yang membangun sistem mampu mengamati input/lingkungan, menalar atau mengambil keputusan, dan bertindak untuk mencapai tujuan. Bandingkan 3 kartu secara jernih: Bukan AI (automasi statis), AI Klasik (pencarian & penalaran non-ML), dan AI Modern (belajar dari data).">
      <div class="kicker">BAB 01 · ARTIFICIAL INTELLIGENCE (AI)</div>
      <h2><span class="hl-blue">Artificial Intelligence (AI)</span>: Sistem yang Mampu Mengambil Keputusan Cerdas</h2>
      <p class="subtitle"><strong>Definisi AI:</strong> Cabang ilmu komputer untuk membangun sistem yang mampu <strong>mengamati lingkungan</strong>, <strong>menalar / memutuskan</strong>, dan <strong>bertindak</strong> guna mencapai suatu tujuan — baik lewat pencarian logika maupun belajar dari data.</p>
      <div class="grid-3" style="margin-bottom:9px;">
        <div class="card tint-red" style="justify-content:space-between; gap:7px; padding:13px 15px;">
          <div class="card-top-bar bar-red"></div>
          <div>
            <span class="pill red">BUKAN AI · AUTOMASI STATIS</span>
            <div class="card-title" style="font-size:15px; margin-top:5px;">Menjalankan Langkah Tetap</div>
          </div>
          <div style="background:#FFFFFF; border:1px solid #F6AEA9; border-radius:10px; padding:6px 8px; display:flex; align-items:center; justify-content:center;">
            <svg viewBox="0 0 260 88" style="width:100%; height:84px; display:block;">
              <!-- Calculator -->
              <rect x="10" y="10" width="66" height="68" rx="8" fill="#FCE8E6" stroke="#EA4335" stroke-width="2"/>
              <rect x="18" y="18" width="50" height="16" rx="3" fill="#FFFFFF" stroke="#EA4335" stroke-width="1.2"/>
              <text x="62" y="30" text-anchor="end" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#202124">12+8=20</text>
              <rect x="18" y="40" width="13" height="11" rx="2" fill="#EA4335"/><text x="24.5" y="48.5" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#FFF">1</text>
              <rect x="36" y="40" width="13" height="11" rx="2" fill="#EA4335"/><text x="42.5" y="48.5" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#FFF">2</text>
              <rect x="54" y="40" width="13" height="11" rx="2" fill="#EA4335"/><text x="60.5" y="48.5" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#FFF">3</text>
              <rect x="18" y="56" width="49" height="13" rx="2" fill="#202124"/><text x="42.5" y="65.5" text-anchor="middle" font-family="Roboto Mono" font-size="7.5" fill="#FFF">FIXED RULE</text>
              <!-- Rigid flow -->
              <line x1="84" y1="44" x2="112" y2="44" stroke="#EA4335" stroke-width="2.2"/><polygon points="110,40 118,44 110,48" fill="#EA4335"/>
              <rect x="120" y="24" width="64" height="40" rx="8" fill="#F8F9FA" stroke="#DADCE0" stroke-width="1.8"/>
              <text x="152" y="41" text-anchor="middle" font-family="Poppins" font-size="9" font-weight="700" fill="#5F6368">Menu IVR</text>
              <text x="152" y="54" text-anchor="middle" font-family="Roboto Mono" font-size="8" fill="#C5221F">Tekan 1/2/3</text>
              <line x1="186" y1="44" x2="210" y2="44" stroke="#EA4335" stroke-width="2.2"/><polygon points="208,40 216,44 208,48" fill="#EA4335"/>
              <rect x="218" y="28" width="34" height="32" rx="6" fill="#202124"/>
              <text x="235" y="47" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" font-weight="700" fill="#FFF">OUT</text>
            </svg>
          </div>
          <div class="card-body" style="font-size:12.4px;">
            <ul>
              <li>Hanya mengikuti instruksi baku yang kaku — tidak mencari strategi dan tidak belajar.</li>
              <li><strong>Contoh:</strong> Kalkulator, rumus Excel (<code>SUM</code>), <em>vending machine</em>, menu tombol <code>1–2–3</code>.</li>
            </ul>
          </div>
          <div class="mini-box" style="font-size:11.4px;"><strong>Ciri:</strong> Input sama selalu lewat jalur statis yang ditulis persis oleh programmer.</div>
        </div>

        <div class="card tint-blue" style="justify-content:space-between; gap:7px; padding:13px 15px;">
          <div class="card-top-bar bar-blue"></div>
          <div>
            <span class="pill blue">AI KLASIK · PENALARAN &amp; PENCARIAN</span>
            <div class="card-title" style="font-size:15px; margin-top:5px;">Cerdas Tanpa Belajar dari Data</div>
          </div>
          <div style="background:#FFFFFF; border:1px solid #C6DAFC; border-radius:10px; padding:6px 8px; display:flex; align-items:center; justify-content:center;">
            <svg viewBox="0 0 260 88" style="width:100%; height:84px; display:block;">
              <!-- Left: Search Tree (Minimax Chess) -->
              <text x="64" y="13" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#1A73E8">Search Tree (Catur)</text>
              <line x1="64" y1="26" x2="32" y2="50" stroke="#DADCE0" stroke-width="1.8"/>
              <line x1="64" y1="26" x2="96" y2="50" stroke="#4285F4" stroke-width="2.6"/>
              <line x1="32" y1="50" x2="18" y2="74" stroke="#DADCE0" stroke-width="1.5"/>
              <line x1="32" y1="50" x2="46" y2="74" stroke="#DADCE0" stroke-width="1.5"/>
              <line x1="96" y1="50" x2="82" y2="74" stroke="#DADCE0" stroke-width="1.5"/>
              <line x1="96" y1="50" x2="110" y2="74" stroke="#4285F4" stroke-width="2.6"/>
              <circle cx="64" cy="26" r="7" fill="#4285F4"/>
              <circle cx="32" cy="50" r="6" fill="#BDC1C6"/>
              <circle cx="96" cy="50" r="7" fill="#4285F4"/>
              <circle cx="18" cy="74" r="5" fill="#BDC1C6"/>
              <circle cx="46" cy="74" r="5" fill="#BDC1C6"/>
              <circle cx="82" cy="74" r="5" fill="#BDC1C6"/>
              <circle cx="110" cy="74" r="7" fill="#34A853"/>
              <!-- Divider -->
              <line x1="132" y1="12" x2="132" y2="78" stroke="#E0E3E7" stroke-width="1.2" stroke-dasharray="3,3"/>
              <!-- Right: A* Map Route -->
              <text x="196" y="13" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#1A73E8">Rute Peta (A*)</text>
              <rect x="148" y="22" width="98" height="56" rx="6" fill="#F8F9FA" stroke="#DADCE0" stroke-width="1.4"/>
              <path d="M158 66 L184 66 L184 42 L214 42 L236 32" fill="none" stroke="#4285F4" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="158" cy="66" r="5" fill="#EA4335"/>
              <circle cx="236" cy="32" r="5.5" fill="#34A853"/>
              <text x="158" y="76" text-anchor="middle" font-family="Roboto Mono" font-size="7" fill="#C5221F">A</text>
              <text x="236" y="25" text-anchor="middle" font-family="Roboto Mono" font-size="7" fill="#137333">B</text>
            </svg>
          </div>
          <div class="card-body" style="font-size:12.4px;">
            <ul>
              <li>Memecahkan masalah lewat <strong><em>search</em></strong>, <strong><em>planning</em></strong>, &amp; logika formal.</li>
              <li><strong>Contoh:</strong> <strong>AI Catur (<em>Deep Blue / Minimax</em>)</strong>, <strong>Navigasi Rute (<em>A*</em>)</strong>, &amp; <strong>Expert System</strong>.</li>
            </ul>
          </div>
          <div class="mini-box" style="font-size:11.4px;"><strong>Ciri:</strong> Strategi dirancang lewat algoritma logika, bukan dilatih dari jutaan data.</div>
        </div>

        <div class="card tint-green" style="justify-content:space-between; gap:7px; padding:13px 15px;">
          <div class="card-top-bar bar-green"></div>
          <div>
            <span class="pill green">AI MODERN · BELAJAR DARI DATA</span>
            <div class="card-title" style="font-size:15px; margin-top:5px;">Machine Learning &amp; Deep Learning</div>
          </div>
          <div style="background:#FFFFFF; border:1px solid #A8DAB5; border-radius:10px; padding:6px 8px; display:flex; align-items:center; justify-content:space-around; gap:6px; height:98px;">
            <div style="display:flex; flex-direction:column; gap:3px; align-items:center;">
              <div style="display:flex; gap:3px;">
                <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:32px; height:32px; border-radius:6px; object-fit:cover; border:1.5px solid #4285F4;"/>
                <img src="assets/P02/thumb_anna.jpg" alt="Anna" style="width:32px; height:32px; border-radius:6px; object-fit:cover; border:1.5px solid #EA4335;"/>
              </div>
              <span style="font-family:var(--font-code); font-size:8.5px; color:#5F6368;">Data Foto</span>
            </div>
            <svg viewBox="0 0 92 70" style="width:86px; height:66px; flex-shrink:0;">
              <g stroke="#A8DAB5" stroke-width="1.4">
                <line x1="12" y1="16" x2="46" y2="14"/><line x1="12" y1="16" x2="46" y2="35"/><line x1="12" y1="16" x2="46" y2="56"/>
                <line x1="12" y1="54" x2="46" y2="14"/><line x1="12" y1="54" x2="46" y2="35"/><line x1="12" y1="54" x2="46" y2="56"/>
                <line x1="46" y1="14" x2="80" y2="35"/><line x1="46" y1="35" x2="80" y2="35"/><line x1="46" y1="56" x2="80" y2="35"/>
              </g>
              <circle cx="12" cy="16" r="6" fill="#4285F4"/><circle cx="12" cy="54" r="6" fill="#4285F4"/>
              <circle cx="46" cy="14" r="6.5" fill="#FBBC04"/><circle cx="46" cy="35" r="6.5" fill="#EA4335"/><circle cx="46" cy="56" r="6.5" fill="#FBBC04"/>
              <circle cx="80" cy="35" r="7.5" fill="#34A853"/>
            </svg>
            <div style="background:#E6F4EA; border:1.5px solid #34A853; border-radius:8px; padding:4px 7px; text-align:center;">
              <div style="font-family:var(--font-title); font-size:10.5px; font-weight:700; color:#137333;">Elsa!</div>
              <div style="font-family:var(--font-code); font-size:8px; color:#5F6368;">Belajar Pola</div>
            </div>
          </div>
          <div class="card-body" style="font-size:12.4px;">
            <ul>
              <li>Menemukan pola rumit otomatis dari contoh data (foto, suara, teks).</li>
              <li><strong>Contoh:</strong> <strong>Face Unlock</strong>, rekomendasi YouTube/Netflix, ChatGPT/Gemini, &amp; <strong>proyek Frozen kita!</strong></li>
            </ul>
          </div>
          <div class="mini-box" style="font-size:11.4px;"><strong>Ciri:</strong> Performa meningkat saat diberi contoh data makin beragam &amp; berkualitas.</div>
        </div>
      </div>
      <div class="callout"><strong>Ringkasnya:</strong> Tidak semua program komputer adalah AI, dan tidak semua AI memakai Machine Learning — tetapi untuk memahami <strong>foto/gambar</strong>, kita memerlukan <strong>AI Modern (ML &amp; DL)</strong>.</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 09: MACHINE LEARNING + SIMULATOR #1 -->
    <section class="slide" data-title="Bab 1: Machine Learning &amp; Simulator Aturan vs Belajar" data-notes="Alokasi waktu: 2 menit. Di Machine Learning, manusia tidak menulis aturan manual; kita memberi contoh data dan kunci jawaban (Supervised Learning), lalu algoritma ML menghasilkan Model yang siap dipakai memprediksi foto baru.">
      <div class="kicker">BAB 01 · MACHINE LEARNING</div>
      <h2><span class="hl-red">Machine Learning (ML)</span>: Belajar dari Contoh</h2>
      <div class="sim-bar pdf-keep-ui" id="ml-tabs" style="margin-bottom:10px;">
        <button class="btn-ui" data-ml="rule" onclick="setMlTab('rule')">1. Pemrograman Tradisional (Aturan Manual)</button>
        <button class="btn-ui outline" data-ml="ml" onclick="setMlTab('ml')">2. Machine Learning (Training → Prediksi)</button>
      </div>
      <div class="split-60-40" style="flex:1; min-height:0; align-items:stretch;">
        <div class="card surface" style="justify-content:space-between; align-items:center; gap:10px; padding:13px 15px;">
          <div class="card-top-bar bar-red"></div>
          <div style="display:flex; align-items:center; gap:10px; width:100%; background:#FFFFFF; border:1px solid #DADCE0; border-radius:11px; padding:7px 10px;">
            <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:40px; height:40px; border-radius:8px; object-fit:cover; border:2px solid #4285F4;"/>
            <img src="assets/P02/thumb_olaf.jpg" alt="Olaf" style="width:40px; height:40px; border-radius:8px; object-fit:cover; border:2px solid #34A853;"/>
            <img src="assets/P02/thumb_anna.jpg" alt="Anna" style="width:40px; height:40px; border-radius:8px; object-fit:cover; border:2px solid #EA4335;"/>
            <div style="font-size:11.6px; color:#3C4043; line-height:1.35;"><strong>Data Nyata Proyek ({total_imgs} Foto):</strong><br/>Bandingkan alur program aturan manual vs alur belajar Machine Learning!</div>
          </div>
          <div id="ml-diagram" style="width:100%; flex:1; display:flex; align-items:center; justify-content:center;"></div>
        </div>
        <div class="card" style="justify-content:space-between; gap:10px; padding:15px 17px;">
          <div class="card-top-bar bar-blue" id="ml-bar"></div>
          <div>
            <span class="pill blue" id="ml-badge">ATURAN MANUAL</span>
            <div class="card-title" id="ml-title" style="margin-top:6px; font-size:16px;">Manusia Menulis Semua Aturan</div>
          </div>
          <div class="card-body" id="ml-desc" style="font-size:12.8px; line-height:1.45;"></div>
          <div id="ml-extra"></div>
          <div class="callout" id="ml-callout" style="padding:8px 11px; font-size:12px;"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 10: DEEP LEARNING + SIMULATOR #2 (HIERARKI AI ⊃ ML ⊃ DL) -->
    <section class="slide" data-title="Bab 1: Deep Learning &amp; Peta AI ⊃ ML ⊃ DL" data-notes="Alokasi waktu: 1.5 menit. Deep Learning adalah cabang khusus Machine Learning yang memakai Neural Network berlapis banyak sehingga bisa mempelajari fitur langsung dari piksel mentah. Gunakan 3 tab sebagai recap cepat peta AI ⊃ ML ⊃ DL.">
      <div class="kicker">BAB 01 · DEEP LEARNING</div>
      <h2><span class="hl-green">Deep Learning (DL)</span> di Dalam Peta AI ⊃ ML ⊃ DL</h2>
      <div class="sim-bar pdf-keep-ui" id="vnn-tabs" style="margin-bottom:10px;">
        <button class="btn-ui outline" data-vnn="ai" onclick="setVnnMode('ai')">1. Recap: AI</button>
        <button class="btn-ui outline" data-vnn="ml" onclick="setVnnMode('ml')">2. Recap: ML</button>
        <button class="btn-ui" data-vnn="dl" onclick="setVnnMode('dl')">3. Deep Learning (DL) ← Proyek Kita</button>
      </div>
      <div class="split-40-60" style="flex:1; min-height:0; align-items:stretch;">
        <div class="canvas-box" style="justify-content:space-between; padding:12px 14px; gap:6px;">
          <svg id="vnn-svg" viewBox="0 0 360 320" style="width:100%; flex:1; max-height:340px;">
            <circle id="vnn-c-ai" cx="180" cy="160" r="148" fill="#E8F0FE" stroke="#4285F4" stroke-width="3" style="cursor:pointer;" onclick="setVnnMode('ai')"/>
            <text x="180" y="52" text-anchor="middle" font-family="Poppins" font-size="11.8" font-weight="700" fill="#1A73E8" style="pointer-events:none;">Artificial Intelligence (AI)</text>
            <circle id="vnn-c-ml" cx="180" cy="186" r="106" fill="#FCE8E6" stroke="#EA4335" stroke-width="3" style="cursor:pointer;" onclick="setVnnMode('ml')"/>
            <text x="180" y="122" text-anchor="middle" font-family="Poppins" font-size="10.8" font-weight="700" fill="#C5221F" style="pointer-events:none;">Machine Learning (ML)</text>
            <circle id="vnn-c-dl" cx="180" cy="214" r="62" fill="#E6F4EA" stroke="#34A853" stroke-width="4.5" style="cursor:pointer;" onclick="setVnnMode('dl')"/>
            <text x="180" y="207" text-anchor="middle" font-family="Poppins" font-size="12.2" font-weight="700" fill="#137333" style="pointer-events:none;">Deep Learning</text>
            <text x="180" y="225" text-anchor="middle" font-family="Roboto Mono" font-size="9.8" font-weight="700" fill="#137333" style="pointer-events:none;">(Neural Network)</text>
          </svg>
          <div style="font-size:10.5px; color:#5F6368; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:999px; padding:3px 12px; text-align:center;">
            <strong>Interaktif:</strong> Klik langsung lingkaran <code>AI</code>, <code>ML</code>, atau <code>DL</code> di atas!
          </div>
        </div>
        <div class="card surface" style="justify-content:space-between; gap:8px; padding:14px 16px;">
          <div class="card-top-bar bar-green" id="vnn-bar"></div>
          <div>
            <span class="pill green" id="vnn-pill">DEEP LEARNING (DL)</span>
            <div class="card-title" id="vnn-title" style="margin-top:5px;">ML dengan Neural Network Berlapis Banyak</div>
          </div>
          <div id="vnn-illus" style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:11px; padding:7px 10px;"></div>
          <div class="card-body" id="vnn-body" style="font-size:12.6px;"></div>
          <div class="mini-box" id="vnn-frozen" style="font-size:11.8px; padding:8px 11px;"></div>
          <div class="mini-box" id="vnn-extra" style="font-size:11.5px; padding:8px 11px; background:#F8F9FA; border-color:#DADCE0;"></div>
          <div class="callout green" id="vnn-callout" style="font-size:12px; padding:8px 11px;"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 11: PERBEDAAN SPESIFIK ML VS DL (FITUR MANUAL VS OTOMATIS) -->
    <section class="slide" data-title="Bab 1: Perbedaan Spesifik Machine Learning vs Deep Learning" data-notes="Alokasi waktu: 2 menit. Inilah perbedaan paling krusial antara ML klasik dan DL: ML memakai algoritma matematika/statistik yang butuh fitur jelas (untuk gambar harus diekstrak manual oleh manusia), sedangkan DL memakai Neural Network berlapis sehingga AI mempelajari fiturnya sendiri langsung dari piksel mentah!">
      <div class="kicker">BAB 01 · PERBEDAAN KUNCI</div>
      <h2>Perbedaan Spesifik: <span class="hl-red">Machine Learning</span> vs <span class="hl-green">Deep Learning</span></h2>
      <div class="card surface" style="padding:10px 12px; margin-bottom:10px; flex:0 0 auto; gap:8px;">
        <!-- Row 1: ML Klasik with real Elsa photo -->
        <div style="display:grid; grid-template-columns:102px 22px 1.25fr 22px 1.05fr 22px 90px; align-items:center; gap:6px; background:#FCE8E6; border:1.5px solid #F6AEA9; border-radius:11px; padding:7px 10px;">
          <div style="display:flex; align-items:center; gap:6px; background:#FFFFFF; border:1.5px solid #4285F4; border-radius:8px; padding:4px 6px;">
            <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:34px; height:34px; border-radius:6px; object-fit:cover;"/>
            <span style="font-family:var(--font-title); font-size:10px; font-weight:700; color:#1A73E8; line-height:1.15;">Foto<br/>Elsa</span>
          </div>
          <div style="text-align:center; font-size:18px; font-weight:700; color:#C5221F;">→</div>
          <div style="background:#FFFFFF; border:2px solid #EA4335; border-radius:9px; padding:6px 9px;">
            <div style="font-family:var(--font-title); font-size:11px; font-weight:700; color:#C5221F;">1. Ekstraksi Fitur Manual (oleh Manusia)</div>
            <div style="font-family:var(--font-code); font-size:9.6px; color:#5F6368; margin-top:2px;">[R=0.67, G=0.66, B=0.67, Edge=0.04, Rasio=0.75]</div>
          </div>
          <div style="text-align:center; font-size:18px; font-weight:700; color:#C5221F;">→</div>
          <div style="background:#FFFFFF; border:2px solid #FBBC04; border-radius:9px; padding:6px 9px;">
            <div style="font-family:var(--font-title); font-size:11px; font-weight:700; color:#B06000;">2. Algoritma Statistik (ML)</div>
            <div style="font-family:var(--font-code); font-size:9.6px; color:#5F6368; margin-top:2px;">Random Forest · SVM · Regression</div>
          </div>
          <div style="text-align:center; font-size:18px; font-weight:700; color:#C5221F;">→</div>
          <div style="background:#202124; color:#FFFFFF; border-radius:8px; padding:8px 6px; text-align:center; font-family:var(--font-title); font-size:11px; font-weight:700;">Prediksi<br/><span style="color:#FBBC04; font-size:10px;">Elsa</span></div>
        </div>
        <!-- Row 2: Deep Learning with real Elsa photo + Neural Network visual -->
        <div style="display:grid; grid-template-columns:102px 22px 1fr 22px 90px; align-items:center; gap:6px; background:#E6F4EA; border:1.5px solid #A8DAB5; border-radius:11px; padding:7px 10px;">
          <div style="display:flex; align-items:center; gap:6px; background:#FFFFFF; border:1.5px solid #4285F4; border-radius:8px; padding:4px 6px;">
            <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:34px; height:34px; border-radius:6px; object-fit:cover;"/>
            <span style="font-family:var(--font-title); font-size:10px; font-weight:700; color:#1A73E8; line-height:1.15;">Piksel<br/>Mentah</span>
          </div>
          <div style="text-align:center; font-size:18px; font-weight:700; color:#137333;">→</div>
          <div style="background:#34A853; border-radius:9px; padding:6px 12px; display:flex; align-items:center; justify-content:space-between; gap:10px;">
            <div>
              <div style="font-family:var(--font-title); font-size:11.6px; font-weight:700; color:#FFFFFF;">Deep Learning: Neural Network Berlapis Banyak (Feature Learning + Klasifikasi)</div>
              <div style="font-size:10.3px; color:#E6F4EA; margin-top:2px;">AI mempelajari sendiri fitur penting langsung dari piksel mentah: tepi → bentuk → karakter!</div>
            </div>
            <svg viewBox="0 0 84 44" style="width:76px; height:40px; flex-shrink:0;">
              <g stroke="rgba(255,255,255,0.55)" stroke-width="1.2">
                <line x1="12" y1="10" x2="42" y2="8"/><line x1="12" y1="10" x2="42" y2="22"/><line x1="12" y1="10" x2="42" y2="36"/>
                <line x1="12" y1="34" x2="42" y2="8"/><line x1="12" y1="34" x2="42" y2="22"/><line x1="12" y1="34" x2="42" y2="36"/>
                <line x1="42" y1="8" x2="72" y2="22"/><line x1="42" y1="22" x2="72" y2="22"/><line x1="42" y1="36" x2="72" y2="22"/>
              </g>
              <circle cx="12" cy="10" r="4.5" fill="#FFFFFF"/><circle cx="12" cy="34" r="4.5" fill="#FFFFFF"/>
              <circle cx="42" cy="8" r="4.5" fill="#FBBC04"/><circle cx="42" cy="22" r="4.5" fill="#FBBC04"/><circle cx="42" cy="36" r="4.5" fill="#FBBC04"/>
              <circle cx="72" cy="22" r="5.5" fill="#FFFFFF"/>
            </svg>
          </div>
          <div style="text-align:center; font-size:18px; font-weight:700; color:#137333;">→</div>
          <div style="background:#202124; color:#FFFFFF; border-radius:8px; padding:8px 6px; text-align:center; font-family:var(--font-title); font-size:11px; font-weight:700;">Prediksi<br/><span style="color:#34A853; font-size:10px;">Elsa</span></div>
        </div>
      </div>
      <table class="io-table" style="font-size:12.4px;">
        <thead>
          <tr><th style="width:20%;">Aspek</th><th style="width:40%;">Machine Learning (ML Klasik)</th><th style="width:40%;">Deep Learning (DL)</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Algoritma Inti</strong></td>
            <td>Algoritma matematika &amp; statistik klasik (<em>Linear/Logistic Regression, Decision Tree, Random Forest, SVM</em>).</td>
            <td>Arsitektur <strong>Neural Network</strong> berlapis banyak (<em>MLP, CNN, Transformer</em>).</td>
          </tr>
          <tr>
            <td><strong>Fitur / Ciri Data</strong></td>
            <td>Fitur harus <strong>jelas &amp; terstruktur</strong>; pada gambar, manusia harus <strong>mengekstrak fitur secara manual</strong>.</td>
            <td><strong>Dipelajari otomatis oleh AI</strong> langsung dari data mentah (piksel) tanpa ekstraksi fitur manual.</td>
          </tr>
          <tr>
            <td><strong>Cocok untuk Data</strong></td>
            <td>Data <strong>tabular</strong> (tabel kolom jelas: umur, gaji, luas rumah, transaksi).</td>
            <td>Data <strong>tidak terstruktur</strong> (foto, video, suara, teks) — termasuk <strong>foto Frozen kita!</strong></td>
          </tr>
          <tr>
            <td><strong>Data &amp; Komputasi</strong></td>
            <td>Cukup data kecil–menengah; cepat dijalankan di CPU biasa.</td>
            <td>Umumnya butuh data lebih banyak &amp; GPU (atau dibantu <em>Transfer Learning</em> di P04).</td>
          </tr>
        </tbody>
      </table>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    # 11: Q&A REVEAL #2 (BAB 1)
    s.append(
        _qa_slide(
            qa_id="qa-bab1",
            qa_num=2,
            kicker="BAB 01 · TANYA-JAWAB #2",
            title_html='Di Mana Letak <span class="hl-blue">Proyek Frozen</span> di Peta Ini?',
            question_html="Proyek kita melatih model <strong>Neural Network berlapis banyak</strong> langsung pada foto piksel 5 karakter Frozen tanpa menulis aturan ciri warna secara manual. Termasuk kategori mana?",
            choices=[
                "<strong>A.</strong> AI klasik berbasis pencarian / Expert System (bukan ML, bukan DL)",
                "<strong>B.</strong> Machine Learning klasik (fitur warna/bentuk harus diekstrak manual oleh manusia)",
                "<strong>C.</strong> Deep Learning — sekaligus bagian dari Machine Learning dan Artificial Intelligence",
            ],
            answer_html="<strong>Jawaban: C!</strong> Dalam hierarki subset (<code>AI ⊃ ML ⊃ DL</code>), model Deep Learning otomatis juga termasuk Machine Learning dan AI. Keunggulan utamanya: fitur gambar dipelajari otomatis dari piksel mentah!",
            vis_q_html='''<div style="display:flex; flex-direction:column; gap:12px; width:100%; align-items:center;">
              <span class="pill blue" style="font-size:10px; padding:3px 10px;">CEK PEMAHAMAN BAB 1 · PETA AI ⊃ ML ⊃ DL</span>
              <div style="display:flex; gap:6px; justify-content:center; width:100%;">
                <img src="assets/P02/thumb_anna.jpg" style="width:58px; height:58px; border-radius:10px; object-fit:cover; border:2px solid #EA4335;"/>
                <img src="assets/P02/thumb_elsa.jpg" style="width:58px; height:58px; border-radius:10px; object-fit:cover; border:2px solid #4285F4;"/>
                <img src="assets/P02/thumb_kristoff.jpg" style="width:58px; height:58px; border-radius:10px; object-fit:cover; border:2px solid #FBBC04;"/>
                <img src="assets/P02/thumb_olaf.jpg" style="width:58px; height:58px; border-radius:10px; object-fit:cover; border:2px solid #34A853;"/>
                <img src="assets/P02/thumb_sven.jpg" style="width:58px; height:58px; border-radius:10px; object-fit:cover; border:2px solid #1A73E8;"/>
              </div>
              <svg viewBox="0 0 260 156" style="width:255px; height:152px; display:block;">
                <circle cx="130" cy="78" r="72" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.4"/>
                <text x="130" y="27" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="800" fill="#1A73E8">AI</text>
                <circle cx="130" cy="90" r="50" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.4"/>
                <text x="130" y="59" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="800" fill="#C5221F">ML</text>
                <circle cx="130" cy="103" r="28" fill="#E6F4EA" stroke="#34A853" stroke-width="2.6"/>
                <text x="130" y="108" text-anchor="middle" font-family="Poppins" font-size="15" font-weight="800" fill="#137333">?</text>
              </svg>
              <div style="font-size:12px; color:#5F6368; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:10px; padding:8px 12px; width:100%; text-align:center; line-height:1.4;">
                Piksel mentah 5 karakter Frozen → <strong>Neural Network</strong> → di lapis mana posisinya?
              </div>
            </div>''',
            vis_a_html='''<div style="display:flex; flex-direction:column; gap:11px; width:100%; align-items:center;">
              <span class="pill green" style="font-size:10px; padding:3px 10px;">TEPAT! DL ⊂ ML ⊂ AI ✓</span>
              <svg viewBox="0 0 260 164" style="width:260px; height:164px; display:block;">
                <circle cx="130" cy="82" r="76" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.4" opacity="0.82"/>
                <text x="130" y="28" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="800" fill="#1A73E8">AI</text>
                <circle cx="130" cy="95" r="53" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.4" opacity="0.88"/>
                <text x="130" y="61" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="800" fill="#C5221F">ML</text>
                <circle cx="130" cy="110" r="31" fill="#34A853" stroke="#FFFFFF" stroke-width="3"/>
                <text x="130" y="114" text-anchor="middle" font-family="Poppins" font-size="13.5" font-weight="800" fill="#FFFFFF">DL ★</text>
              </svg>
              <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; width:100%; text-align:left; font-size:12px; line-height:1.42; padding:9px 12px;">
                <strong>Posisi Tepat (DL ⊂ ML ⊂ AI):</strong> Karena Deep Learning berada di dalam ML &amp; AI, proyek Frozen kita sekaligus bagian dari <strong>ML</strong> dan <strong>AI</strong> — belajar fitur otomatis langsung dari piksel mentah!
              </div>
            </div>''',
            notes="Alokasi waktu: 1.5 menit. Pastikan peserta paham hierarki subset AI ⊃ ML ⊃ DL sebelum berpindah ke Bab 2 (Task Computer Vision).",
            bar_color="blue",
        )
    )

    # =========================================================================
    # BAB 2: TASK COMPUTER VISION (SLIDE 12–19 · 10.0 MENIT)
    # =========================================================================
    s.append(
        make_divider_slide(
            bg_class="bg-red",
            kicker="BAB 02 · TASK COMPUTER VISION",
            title="Task Computer Vision",
            description="Computer Vision membuat komputer 'melihat' foto dan video — tetapi bentuk output-nya berbeda-beda tergantung jenis tugasnya.",
            footer_label=FOOTER,
            data_title="Bab 2 — Task Computer Vision",
            notes="Alokasi waktu: 0.5 menit. Masuk Bab 2: mengenalkan 4 tugas utama Computer Vision memakai foto Frozen milik peserta sendiri sebagai satu contoh utuh.",
        )
    )

    s.append(
        f"""
    <!-- 12: 4 TASK PADA SATU FOTO (PETA VISUAL UTUH) -->
    <section class="slide" data-title="Bab 2: 4 Task CV pada Satu Foto" data-notes="Alokasi waktu: 1.5 menit. Tunjukkan keempat panel secara berdampingan pada foto asli Elsa agar peserta langsung menangkap beda bentuk output tiap task. Tegaskan bahwa kotak, mask, dan panah adalah ilustrasi buatan kode, bukan hasil model sungguhan.">
      <div class="kicker">BAB 02 · PERBANDINGAN TASK COMPUTER VISION</div>
      <h2>4 Task Computer Vision pada <span class="hl-red">Foto yang Sama</span></h2>
      <div class="img-box" style="height:auto; flex:1; min-height:0; padding:8px 10px; margin-bottom:10px;">
        <img src="assets/P02/02_cv_tasks_4panel.png" alt="4 Task Computer Vision pada foto Elsa (Ilustrasi Konsep Buatan Kode)" style="width:100%; height:100%; max-height:335px; object-fit:contain;"/>
      </div>
      <div class="grid-4" style="gap:10px; flex:0 0 auto;">
        <div class="card tint-blue" style="padding:10px 12px; gap:4px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title" style="font-size:13px; color:#1A73E8;">1. Classification</div>
          <div style="font-size:11.6px; color:#3C4043; line-height:1.38;"><strong>Pertanyaan:</strong> &ldquo;Foto ini apa?&rdquo;<br/><strong>Output:</strong> 1 label kelas (proyek kita!).</div>
        </div>
        <div class="card tint-red" style="padding:10px 12px; gap:4px;">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title" style="font-size:13px; color:#C5221F;">2. Object Detection</div>
          <div style="font-size:11.6px; color:#3C4043; line-height:1.38;"><strong>Pertanyaan:</strong> &ldquo;Apa &amp; di mana?&rdquo;<br/><strong>Output:</strong> <em>Bounding box</em> + label.</div>
        </div>
        <div class="card tint-green" style="padding:10px 12px; gap:4px;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title" style="font-size:12.6px; color:#137333;">3. Semantic &amp; Instance Segm.</div>
          <div style="font-size:11.6px; color:#3C4043; line-height:1.38;"><strong>Pertanyaan:</strong> &ldquo;Piksel mana persisnya?&rdquo;<br/><strong>Output:</strong> <em>Mask</em> presisi per piksel.</div>
        </div>
        <div class="card tint-yellow" style="padding:10px 12px; gap:4px;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title" style="font-size:13px; color:#B06000;">4. Object Tracking</div>
          <div style="font-size:11.6px; color:#3C4043; line-height:1.38;"><strong>Pertanyaan:</strong> &ldquo;Ke mana bergeraknya?&rdquo;<br/><strong>Output:</strong> <em>Bbox</em> + ID antar-frame video.</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 13: IMAGE CLASSIFICATION -->
    <section class="slide" data-title="Bab 2: Image Classification" data-notes="Alokasi waktu: 1 menit. Image Classification adalah tugas paling dasar dan merupakan tugas proyek akhir kita: 1 foto masuk, keluar 1 label kelas beserta persentase keyakinannya.">
      <div class="kicker">BAB 02 · IMAGE CLASSIFICATION</div>
      <h2><span class="hl-blue">Image Classification</span>: Memberi Label pada Seluruh Foto</h2>
      <div class="split-40-60">
        <div class="card tint-blue" style="align-items:center; justify-content:center; gap:16px; text-align:center; padding:18px 18px;">
          <div class="card-top-bar bar-blue"></div>
          <img src="assets/P02/thumb_elsa.jpg" alt="Contoh Elsa" style="width:186px; height:186px; object-fit:cover; border-radius:14px; border:3px solid #4285F4; box-shadow:0 4px 14px rgba(66,133,244,0.16);"/>
          <div style="font-family:var(--font-title); font-weight:700; font-size:15px; color:#1A73E8;">Output: Label &ldquo;Elsa&rdquo; + Probabilitas</div>
          <div style="width:100%; background:#FFFFFF; border:1px solid #C6DAFC; border-radius:11px; padding:10px 12px; display:flex; flex-direction:column; gap:5px; text-align:left;">
            <div style="font-size:10px; color:#5F6368; font-weight:700; margin-bottom:2px;">ILUSTRASI OUTPUT PROBABILITAS (5 KELAS):</div>
            <div style="display:grid; grid-template-columns:56px 1fr 34px; gap:6px; align-items:center; font-size:11px;"><strong>Elsa</strong><div style="height:11px; background:#E8F0FE; border-radius:999px; overflow:hidden;"><div style="width:88%; height:100%; background:#34A853;"></div></div><span style="font-family:var(--font-code); text-align:right; color:#137333; font-weight:700;">88%</span></div>
            <div style="display:grid; grid-template-columns:56px 1fr 34px; gap:6px; align-items:center; font-size:11px;"><span>Anna</span><div style="height:11px; background:#E8F0FE; border-radius:999px; overflow:hidden;"><div style="width:7%; height:100%; background:#4285F4;"></div></div><span style="font-family:var(--font-code); text-align:right;">7%</span></div>
            <div style="display:grid; grid-template-columns:56px 1fr 34px; gap:6px; align-items:center; font-size:11px;"><span>Lainnya</span><div style="height:11px; background:#E8F0FE; border-radius:999px; overflow:hidden;"><div style="width:5%; height:100%; background:#9AA0A6;"></div></div><span style="font-family:var(--font-code); text-align:right;">5%</span></div>
          </div>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Cara Kerja &amp; Karakteristik</div>
          <div class="card-body">
            <ul>
              <li><strong>Input:</strong> 1 gambar utuh (misalnya foto figurine <code>224×224×3</code>).</li>
              <li><strong>Output:</strong> Daftar probabilitas untuk setiap kelas yang mungkin (di proyek kita: <code>Anna, Elsa, Kristoff, Olaf, Sven</code>).</li>
              <li><strong>Batasan:</strong> Model <em>tidak</em> menggambar kotak lokasi objek — ia mengasumsikan ada 1 objek utama di foto tersebut.</li>
              <li><strong>Contoh sehari-hari:</strong> Klasifikasi jenis penyakit daun, pilah jenis sampah, dan <strong>proyek klasifikasi 5 karakter Frozen kita!</strong></li>
            </ul>
          </div>
          <div class="callout"><strong>Jembatan ke Bab 3:</strong> Karena hanya menebak 1 dari 5 kelas, <em>Output Layer</em>-nya cukup <strong>5 neuron</strong>!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 14: OBJECT DETECTION -->
    <section class="slide" data-title="Bab 2: Object Detection" data-notes="Alokasi waktu: 1 menit. Jika dalam satu foto ada banyak objek sekaligus dan kita ingin tahu lokasinya masing-masing, kita naik level ke Object Detection.">
      <div class="kicker">BAB 02 · OBJECT DETECTION</div>
      <h2><span class="hl-red">Object Detection</span>: Apa Objeknya &amp; Di Mana Letaknya?</h2>
      <div class="split-40-60">
        <div class="card tint-red" style="align-items:center; justify-content:center; gap:14px; text-align:center; padding:16px 16px;">
          <div class="card-top-bar bar-red"></div>
          <div class="img-box" style="width:100%; height:auto; flex:0 0 auto; padding:8px; border-color:#F6AEA9;">
            <img src="assets/P02/02b_object_detection_demo.png" alt="Ilustrasi Object Detection dengan foto asli Elsa dan Olaf" style="width:100%; height:auto;"/>
          </div>
          <div class="mini-box" style="width:100%; font-size:11.6px; border-color:#F6AEA9; text-align:left;">
            <strong>Format Output per Objek:</strong> 4 angka koordinat kotak <code>(x, y, w, h)</code> + 1 label kelas (contoh: <code>Elsa</code> &amp; <code>Olaf</code> sekaligus).
          </div>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title">Beda Utama dengan Image Classification</div>
          <div class="card-body">
            <ul>
              <li><strong>Bisa banyak objek sekaligus:</strong> Dalam 1 foto yang berisi Elsa, Anna, dan Olaf bersamaan, semua dideteksi satu per satu.</li>
              <li><strong>Output ganda:</strong> Untuk setiap objek, model mengeluarkan <strong>4 angka koordinat kotak</strong> (<em>bounding box</em>: posisi &amp; ukuran) <strong>+ 1 label kelas</strong>.</li>
              <li><strong>Contoh populer:</strong> Kamera pendeteksi wajah di HP, sistem kamera mobil otonom (pejalan kaki, rambu, kendaraan), kasir otomatis penghitung barang.</li>
            </ul>
          </div>
          <div class="callout red"><strong>Catatan arsitektur:</strong> Karena harus memprediksi banyak kotak + label, output layer-nya jauh lebih kompleks daripada 5 neuron biasa.</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 15: SEMANTIC AND INSTANCE SEGMENTATION -->
    <section class="slide" data-title="Bab 2: Semantic and Instance Segmentation" data-notes="Alokasi waktu: 1.5 menit. Semantic dan Instance Segmentation melabeli piksel demi piksel secara presisi mengikuti lekuk bentuk objek. Jelaskan bedanya: Semantic memberi satu warna untuk semua objek sekelas, sedangkan Instance memisahkan setiap individu objek meski kelasnya sama.">
      <div class="kicker">BAB 02 · IMAGE SEGMENTATION</div>
      <h2><span class="hl-green">Semantic and Instance Segmentation</span>: Bentuk per Piksel</h2>
      <div class="grid-2">
        <div class="card surface" style="justify-content:space-between; gap:10px; padding:15px 18px;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Bukan Kotak — Melainkan <em>Mask</em> Presisi</div>
          <div class="card-body" style="font-size:12.8px;">
            <ul>
              <li><em>Bounding box</em> masih ikut membawa latar belakang di sudutnya; <strong>Segmentation</strong> melabeli <strong>setiap piksel</strong> sesuai bentuk asli objek.</li>
              <li><strong>Contoh:</strong> Efek <em>blur background</em> Zoom/Meet, potong stiker di HP, pemetaan tumor di citra medis (MRI/CT-Scan).</li>
            </ul>
          </div>
          <div class="img-box" style="width:100%; height:auto; flex:0 0 auto; padding:6px; border-color:#A8DAB5;">
            <img src="assets/P02/02d_elsa_mask_closeup.png" alt="Perbandingan foto asli Elsa dan mask presisi per piksel" style="width:100%; max-height:190px; object-fit:contain;"/>
          </div>
          <div class="callout green" style="font-size:12.2px; margin-top:0;"><strong>Output:</strong> Peta <em>mask</em> per piksel seukuran gambar untuk tiap kelas atau tiap objek.</div>
        </div>
        <div class="card tint-green" style="justify-content:space-between; gap:10px; padding:15px 18px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Perbandingan: Semantic vs Instance</div>
          <div class="img-box" style="width:100%; height:auto; flex:1; min-height:0; padding:8px; border-color:#A8DAB5;">
            <img src="assets/P02/02c_semantic_vs_instance_demo.png" alt="Perbandingan Semantic Segmentation vs Instance Segmentation pada 2 foto Olaf" style="width:100%; height:auto; max-height:100%; object-fit:contain;"/>
          </div>
          <div class="mini-box" style="font-size:12.2px;"><strong>Ringkasnya:</strong> <em>Semantic</em> menggabungkan semua objek sekelas dalam 1 warna; <strong>Instance</strong> memisahkan tiap individu (<code>Olaf #1</code> vs <code>Olaf #2</code>).</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 16: OBJECT TRACKING -->
    <section class="slide" data-title="Bab 2: Object Tracking" data-notes="Alokasi waktu: 1 menit. Object Tracking bekerja pada video: menggabungkan Object Detection di tiap frame lalu menghubungkannya dengan ID yang konsisten dari waktu ke waktu. Proyek kita adalah foto statis sehingga ini sebagai wawasan lengkap.">
      <div class="kicker">BAB 02 · OBJECT TRACKING</div>
      <h2><span class="hl-yellow">Object Tracking</span>: Mengikuti Objek Antar-Frame Video</h2>
      <div class="split-60-40">
        <div class="card surface" style="justify-content:space-between; padding:14px 16px;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title">Detection + ID Tracking Antar-Frame (<code>t = 1 → 2 → 3</code>)</div>
          <div style="display:grid; grid-template-columns:1fr 22px 1fr 22px 1fr; align-items:center; gap:6px; flex:1;">
            <!-- Frame t=1 -->
            <div style="background:#FFFFFF; border:2px solid #DADCE0; border-radius:11px; padding:7px; height:196px; position:relative;">
              <div style="font-family:var(--font-code); font-size:10px; font-weight:700; color:#5F6368; text-align:center;">Frame t = 1</div>
              <div style="position:absolute; left:10px; top:34px; width:74px; border:2.5px solid #FBBC04; border-radius:7px; overflow:hidden; background:#FEF7E0;">
                <div style="background:#FBBC04; color:#202124; font-family:var(--font-code); font-size:8.3px; font-weight:700; padding:2px 4px; text-align:center;">ID #1 · Elsa</div>
                <img src="assets/P02/thumb_elsa.jpg" style="width:100%; height:54px; object-fit:cover; display:block;"/>
              </div>
              <div style="position:absolute; right:10px; bottom:10px; width:68px; border:2px solid #4285F4; border-radius:7px; overflow:hidden; background:#E8F0FE;">
                <div style="background:#4285F4; color:#FFF; font-family:var(--font-code); font-size:8px; font-weight:700; padding:2px 3px; text-align:center;">ID #2 · Olaf</div>
                <img src="assets/P02/thumb_olaf.jpg" style="width:100%; height:44px; object-fit:cover; display:block;"/>
              </div>
            </div>
            <div style="text-align:center; font-size:18px; font-weight:700; color:#1A73E8;">→</div>
            <!-- Frame t=2 -->
            <div style="background:#FFFFFF; border:2px solid #DADCE0; border-radius:11px; padding:7px; height:196px; position:relative;">
              <div style="font-family:var(--font-code); font-size:10px; font-weight:700; color:#5F6368; text-align:center;">Frame t = 2</div>
              <div style="position:absolute; left:46px; top:30px; width:74px; border:2.5px solid #FBBC04; border-radius:7px; overflow:hidden; background:#FEF7E0;">
                <div style="background:#FBBC04; color:#202124; font-family:var(--font-code); font-size:8.3px; font-weight:700; padding:2px 4px; text-align:center;">ID #1 · Elsa</div>
                <img src="assets/P02/thumb_elsa.jpg" style="width:100%; height:54px; object-fit:cover; display:block;"/>
              </div>
              <div style="position:absolute; right:10px; bottom:10px; width:68px; border:2px solid #4285F4; border-radius:7px; overflow:hidden; background:#E8F0FE;">
                <div style="background:#4285F4; color:#FFF; font-family:var(--font-code); font-size:8px; font-weight:700; padding:2px 3px; text-align:center;">ID #2 · Olaf</div>
                <img src="assets/P02/thumb_olaf.jpg" style="width:100%; height:44px; object-fit:cover; display:block;"/>
              </div>
            </div>
            <div style="text-align:center; font-size:18px; font-weight:700; color:#1A73E8;">→</div>
            <!-- Frame t=3 -->
            <div style="background:#FFFFFF; border:2px solid #DADCE0; border-radius:11px; padding:7px; height:196px; position:relative;">
              <div style="font-family:var(--font-code); font-size:10px; font-weight:700; color:#5F6368; text-align:center;">Frame t = 3</div>
              <div style="position:absolute; right:10px; top:26px; width:74px; border:2.5px solid #FBBC04; border-radius:7px; overflow:hidden; background:#FEF7E0;">
                <div style="background:#FBBC04; color:#202124; font-family:var(--font-code); font-size:8.3px; font-weight:700; padding:2px 4px; text-align:center;">ID #1 · Elsa</div>
                <img src="assets/P02/thumb_elsa.jpg" style="width:100%; height:54px; object-fit:cover; display:block;"/>
              </div>
              <div style="position:absolute; right:10px; bottom:10px; width:68px; border:2px solid #4285F4; border-radius:7px; overflow:hidden; background:#E8F0FE;">
                <div style="background:#4285F4; color:#FFF; font-family:var(--font-code); font-size:8px; font-weight:700; padding:2px 3px; text-align:center;">ID #2 · Olaf</div>
                <img src="assets/P02/thumb_olaf.jpg" style="width:100%; height:44px; object-fit:cover; display:block;"/>
              </div>
            </div>
          </div>
          <div style="font-size:11.6px; color:#1A73E8; font-weight:700; text-align:center;">Ilustrasi konsep: <code>ID #1</code> (Elsa) bergerak ke kanan &amp; <code>ID #2</code> (Olaf) tetap dikenali dengan ID yang sama!</div>
        </div>
        <div class="card" style="justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title">Kapan Dipakai?</div>
          <div class="card-body" style="font-size:13.4px;">
            <ul>
              <li><strong>Menghitung lalu lintas:</strong> Memastikan mobil yang lewat tidak dihitung dua kali pada frame berikutnya.</li>
              <li><strong>Analisis olahraga:</strong> Melacak lintasan bola dan pergerakan tiap pemain.</li>
              <li><strong>Kamera otomatis:</strong> Mengikuti pembicara yang berjalan di panggung.</li>
            </ul>
          </div>
          <div class="callout yellow"><strong>Wawasan:</strong> Proyek Frozen kita memakai <strong>foto tunggal</strong> (bukan video), jadi kita fokus ke <em>Image Classification</em>.</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 17: LATIHAN INTERAKTIF — COCOKKAN KASUS NYATA -->
    <section class="slide" data-title="Bab 2: Latihan Cocokkan Kasus dengan Task CV" data-notes="Alokasi waktu: 1.5 menit. Minta peserta menebak task yang paling cocok untuk keempat kasus nyata berikut, lalu klik tombolnya satu per satu untuk melihat umpan balik langsung.">
      <div class="kicker">BAB 02 · LATIHAN INTERAKTIF</div>
      <h2>Cocokkan <span class="hl-blue">Kasus Nyata</span> dengan Task CV yang Tepat</h2>
      <p class="subtitle">Klik jawaban yang paling sesuai untuk tiap kasus di bawah ini:</p>
      <div id="match-list" style="display:flex; flex-direction:column; gap:9px; flex:1; justify-content:center;">
        <div class="match-row" id="m-row-0">
          <div><strong>1. Aplikasi menebak jenis penyakit daun</strong> dari 1 foto daun utuh.<div id="m-fb-0" style="font-size:11.5px; color:#5F6368; margin-top:2px;">Pilih salah satu task di sebelah kanan →</div></div>
          <div class="match-btns pdf-keep-ui">
            <button class="btn-ui outline" data-mc="cls" onclick="checkMatch(0,'cls',this)">Classification</button>
            <button class="btn-ui outline" data-mc="det" onclick="checkMatch(0,'det',this)">Detection</button>
            <button class="btn-ui outline" data-mc="seg" onclick="checkMatch(0,'seg',this)">Segmentation</button>
            <button class="btn-ui outline" data-mc="trk" onclick="checkMatch(0,'trk',this)">Tracking</button>
          </div>
        </div>
        <div class="match-row" id="m-row-1">
          <div><strong>2. Kamera kasir otomatis</strong> menghitung banyak barang berbeda di atas nampan.<div id="m-fb-1" style="font-size:11.5px; color:#5F6368; margin-top:2px;">Pilih salah satu task di sebelah kanan →</div></div>
          <div class="match-btns pdf-keep-ui">
            <button class="btn-ui outline" data-mc="cls" onclick="checkMatch(1,'cls',this)">Classification</button>
            <button class="btn-ui outline" data-mc="det" onclick="checkMatch(1,'det',this)">Detection</button>
            <button class="btn-ui outline" data-mc="seg" onclick="checkMatch(1,'seg',this)">Segmentation</button>
            <button class="btn-ui outline" data-mc="trk" onclick="checkMatch(1,'trk',this)">Tracking</button>
          </div>
        </div>
        <div class="match-row" id="m-row-2">
          <div><strong>3. Fitur hapus latar belakang rapi</strong> tepat mengikuti lekuk rambut di foto profil.<div id="m-fb-2" style="font-size:11.5px; color:#5F6368; margin-top:2px;">Pilih salah satu task di sebelah kanan →</div></div>
          <div class="match-btns pdf-keep-ui">
            <button class="btn-ui outline" data-mc="cls" onclick="checkMatch(2,'cls',this)">Classification</button>
            <button class="btn-ui outline" data-mc="det" onclick="checkMatch(2,'det',this)">Detection</button>
            <button class="btn-ui outline" data-mc="seg" onclick="checkMatch(2,'seg',this)">Segmentation</button>
            <button class="btn-ui outline" data-mc="trk" onclick="checkMatch(2,'trk',this)">Tracking</button>
          </div>
        </div>
        <div class="match-row" id="m-row-3">
          <div><strong>4. CCTV jalan tol</strong> mengukur kecepatan &amp; lintasan setiap mobil di rekaman video.<div id="m-fb-3" style="font-size:11.5px; color:#5F6368; margin-top:2px;">Pilih salah satu task di sebelah kanan →</div></div>
          <div class="match-btns pdf-keep-ui">
            <button class="btn-ui outline" data-mc="cls" onclick="checkMatch(3,'cls',this)">Classification</button>
            <button class="btn-ui outline" data-mc="det" onclick="checkMatch(3,'det',this)">Detection</button>
            <button class="btn-ui outline" data-mc="seg" onclick="checkMatch(3,'seg',this)">Segmentation</button>
            <button class="btn-ui outline" data-mc="trk" onclick="checkMatch(3,'trk',this)">Tracking</button>
          </div>
        </div>
      </div>
      <div class="callout" style="margin-top:6px;"><strong>Pola cepat mengingat:</strong> 1 label foto = <em>Classification</em> · Kotak banyak objek = <em>Detection</em> · Mask per piksel = <em>Segmentation</em> · Video + ID = <em>Tracking</em>.</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    # 18: Q&A REVEAL #3 (BAB 2)
    s.append(
        _qa_slide(
            qa_id="qa-bab2",
            qa_num=3,
            kicker="BAB 02 · TANYA-JAWAB #3",
            title_html='Task Mana untuk <span class="hl-red">Proyek Frozen</span> &amp; Kenapa?',
            question_html="Setiap foto di folder <code>data/frozen_v1/</code> berisi 1 figurine utama dari 5 karakter (Anna, Elsa, Kristoff, Olaf, Sven) dan tujuannya menebak nama karakternya. Task CV mana yang paling tepat?",
            choices=[
                "<strong>A.</strong> Image Classification (multi-kelas: 5 kelas)",
                "<strong>B.</strong> Semantic / Instance Segmentation karena latar belakang ada yang ramai",
                "<strong>C.</strong> Object Tracking karena ada 7 sesi foto berbeda",
            ],
            answer_html="<strong>Jawaban: A (Image Classification multi-kelas)!</strong> Kita hanya perlu 1 label karakter per foto (bukan menggambar mask piksel maupun melacak gerak video). Masalah latar ramai tetap bisa ditangani oleh model klasifikasi Deep Learning yang dilatih dengan foto kondisi polos dan ramai.",
            vis_q_html='<div style="display:flex; gap:8px; justify-content:center;"><img src="assets/P02/thumb_anna.jpg" style="width:82px; height:82px; border-radius:10px; object-fit:cover;"/><img src="assets/P02/thumb_elsa.jpg" style="width:82px; height:82px; border-radius:10px; object-fit:cover;"/><img src="assets/P02/thumb_olaf.jpg" style="width:82px; height:82px; border-radius:10px; object-fit:cover;"/></div><div style="margin-top:10px; font-size:13px; color:#5F6368;">1 foto figurine → 1 nama karakter. Tugas CV yang mana?</div>',
            vis_a_html='<div class="big-num hl-blue" style="font-size:24px;">Image Classification</div><div class="mini-box" style="margin-top:8px; background:#E8F0FE; border-color:#C6DAFC;"><strong>Multi-Class (5 Kelas):</strong> Input 1 foto <code>(224,224,3)</code> → Output 5 probabilitas berjumlah <code>100%</code>. Sekarang kita bongkar jaringan saraf yang melakukannya di Bab 3!</div>',
            notes="Alokasi waktu: 1.5 menit. Tegaskan kesimpulan Bab 2 sebelum masuk ke jantung sesi hari ini yaitu Bab 3 (Neural Network dari bagian terkecil sampai terbesar).",
            bar_color="red",
        )
    )

    # =========================================================================
    # BAB 3: NEURAL NETWORK — TERKECIL -> TERBESAR (SLIDE 20–40 · 27.0 MENIT)
    # =========================================================================
    s.append(
        make_divider_slide(
            bg_class="bg-green",
            kicker="BAB 03 · NEURAL NETWORK (5 TAHAP)" if HIDE_SLIDES_28_40 else "BAB 03 · NEURAL NETWORK",
            title="Bedah Total: Neural Network",
            description=(
                "Tahap 1 (1 Neuron) → Tahap 2 (Flatten & RGB) → Tahap 3 (Layer & Dense) → Tahap 4 (Weight, Aktivasi, Argmax) → Tahap 5 (Backprop, LR/Adam, Batch & Overfitting) → Full NN."
                if HIDE_SLIDES_28_40
                else "Kita rakit dari bagian paling kecil (1 Neuron) → Input Layer → Output Layer → hubungan tiap neuron → Hidden Layer → hitungan Forward Pass → cara belajar."
            ),
            footer_label=FOOTER,
            data_title="Bab 3 — Bedah Neural Network",
            notes=f"Alokasi waktu: 0.5 menit. Bab 3 adalah bagian inti ({'23.0' if HIDE_SLIDES_28_40 else '27'} menit). Kita susun pelan-pelan dari 1 neuron tunggal, lalu kumpulan neuron menjadi layer, sampai simulasi perhitungan, siklus belajar, dan simulasi penuh end-to-end.",
        )
    )

    # 21: NEURON BIOLOGIS -> BUATAN
    s.append(
        f"""
    <!-- 20: DIMULAI DARI 1 NEURON (1 UNIT PEMEGANG 1 ANGKA PIKSEL) -->
    <section class="slide" data-title="Bab 3A: Dimulai dari 1 Neuron — 1 Unit Pemegang 1 Angka" data-notes="Alokasi waktu: 1.5 menit. Mulai dari bagian paling kecil dan paling konkret: 1 Neuron adalah 1 unit penyusun Neural Network yang memegang 1 nilai angka. Tunjuk gambar kanan: foto asli Elsa diperbesar jadi kotak piksel 8×8, lalu 1 kotak piksel (pada gaun Elsa) masuk menjadi tepat 1 lingkaran Neuron.">
      <div class="kicker">BAB 03 · TAHAP 1 · 1 NEURON</div>
      <h2>Dimulai dari <span class="hl-green">1 Neuron</span>: 1 Unit Pemegang 1 Angka</h2>
      <div class="split-40-60" style="grid-template-columns:0.82fr 1.48fr;">
        <div class="card surface" style="justify-content:space-between; gap:10px; padding:16px 18px;">
          <div class="card-top-bar bar-green"></div>
          <div style="display:flex; flex-direction:column; gap:10px;">
            <div class="card-title">Apa Itu 1 Neuron?</div>
            <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; font-size:12.6px; line-height:1.48;">
              <strong>Definisi:</strong> <strong>Neuron</strong> (<em>Node</em>) adalah <strong>unit terkecil</strong> penyusun <em>Neural Network</em> yang memegang <strong>1 nilai angka</strong> (terinspirasi sel saraf otak).
            </div>
            <div class="card-body" style="font-size:12.8px; line-height:1.5;">
              <ul style="gap:7px;">
                <li id="n1-bul-1" class="sync-bullet"><strong>Pada gambar:</strong> Foto terdiri dari banyak piksel bernilai <code style="white-space:nowrap;">0.0–1.0</code>. Setiap <strong>1 nilai piksel</strong> diwakili oleh tepat <strong>1 Neuron</strong>!</li>
                <li id="n1-bul-2" class="sync-bullet"><strong>Catatan akurat:</strong> Di lapisan paling depan, neuron hanya <em>memegang nilai piksel</em>. Di lapisan berikutnya, neuron akan <em>menghitung</em> angkanya dari neuron-neuron sebelumnya.</li>
              </ul>
            </div>
            <div class="mini-box" style="background:#FFFFFF; border-color:#DADCE0; padding:8px 10px; font-size:11.4px;">
              <div style="font-weight:700; color:#202124; margin-bottom:5px;">Contoh Nilai Angka dalam 1 Neuron Piksel:</div>
              <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:6px; text-align:center; font-family:var(--font-code); font-size:10.5px;">
                <div style="background:#202124; color:#FFFFFF; border-radius:7px; padding:4px 3px;"><strong>0.00</strong><div style="font-family:var(--font-body); font-size:9.3px; opacity:0.85;">Hitam gelap</div></div>
                <div style="background:#535E96; color:#FFFFFF; border-radius:7px; padding:4px 3px;"><strong>0.42</strong><div style="font-family:var(--font-body); font-size:9.3px; opacity:0.95;">Gaun Elsa</div></div>
                <div style="background:#F8F9FA; color:#202124; border:1px solid #DADCE0; border-radius:7px; padding:4px 3px;"><strong>1.00</strong><div style="font-family:var(--font-body); font-size:9.3px; color:#5F6368;">Putih terang</div></div>
              </div>
            </div>
          </div>
          <div class="callout green" style="font-size:12px;"><strong>Lanjut ke Tahap 2.1:</strong> Karena 1 foto punya banyak piksel, mari kita susun semua neuron piksel tersebut ke bawah (<em>Flatten</em>)!</div>
        </div>
        <div class="card" style="justify-content:space-between; gap:8px; padding:12px 14px;">
          <div class="card-top-bar bar-blue"></div>

          <!-- Compact Control Bar -->
          <div class="sim-bar pdf-keep-ui" style="justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:10px; padding:4px 8px; gap:6px;">
            <div style="display:flex; align-items:center; gap:5px;">
              <button class="btn-ui" id="n1-btn-play" onclick="playN1Anim()" style="padding:3.5px 9px; font-size:10.4px; background:#34A853; border-color:#34A853;">▶ Play</button>
              <button class="btn-ui outline" id="n1-btn-next" onclick="nextN1Sample()" style="padding:3.5px 8px; font-size:10.4px; color:#1A73E8; border-color:#C6DAFC;">⏭ Piksel Lain</button>
              <button class="btn-ui outline" id="n1-btn-reset" onclick="resetN1Anim()" style="padding:3.5px 8px; font-size:10.4px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
            </div>
            <span style="font-size:10.2px; color:#5F6368; font-weight:600;">Klik kotak mana saja di grid <code>8×8</code>!</span>
          </div>

          <!-- Interactive 4-Stage Horizontal Visual + 60fps Motion Canvas (LARGE 1:1 Photo & 8x8 Grid, labels aligned on TOP!) -->
          <div id="n1-stage-wrap" style="position:relative; flex:1; min-height:0; display:grid; grid-template-columns:174px 32px 174px 38px 88px 20px 104px; align-items:center; justify-content:space-between; padding:4px 4px;">
            <canvas id="n1-motion-canvas" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:20;"></canvas>

            <!-- 1. Foto Asli Elsa (176x176 — 1:1 with 8x8 Grid!) -->
            <div id="n1-st1" class="n1-stage-on" style="display:flex; flex-direction:column; align-items:center; gap:9px;">
              <div style="font-family:var(--font-title); font-size:12.2px; font-weight:700; color:#202124; text-align:center; height:18px; line-height:18px; white-space:nowrap;">1. Foto Asli Elsa</div>
              <div style="height:178px; display:flex; align-items:center; justify-content:center;">
                <div id="n1-photo-box" style="position:relative; width:172px; height:172px; border-radius:11px; overflow:hidden; border:2.6px solid #4285F4; box-shadow:0 4px 14px rgba(66,133,244,0.16);">
                  <img src="assets/P02/thumb_elsa.jpg" alt="Foto Asli Elsa" style="width:100%; height:100%; object-fit:cover; display:block;"/>
                </div>
              </div>
              <div style="font-size:10.2px; color:#5F6368; height:16px; line-height:16px;">&nbsp;</div>
            </div>

            <!-- Arrow 1: Zoom Piksel -->
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px;">
              <span style="font-family:var(--font-title); font-size:9.0px; font-weight:700; color:#5F6368; text-align:center; line-height:1.15;">Zoom<br/>Piksel</span>
              <svg viewBox="0 0 34 18" style="width:32px; height:16px;">
                <line x1="2" y1="9" x2="23" y2="9" stroke="#5F6368" stroke-width="2.8" stroke-linecap="round"/>
                <polygon points="21,4 32,9 21,14" fill="#5F6368"/>
              </svg>
            </div>

            <!-- 2. Kotak-Kotak Piksel (176x176 Interactive 8x8 Grid — 1:1 with Photo!) -->
            <div id="n1-st2" class="n1-stage-on" style="display:flex; flex-direction:column; align-items:center; gap:9px;">
              <div style="font-family:var(--font-title); font-size:12.2px; font-weight:700; color:#202124; text-align:center; height:18px; line-height:18px; white-space:nowrap;">2. Kotak Piksel (8×8)</div>
              <div style="height:178px; display:flex; align-items:center; justify-content:center;">
                <div id="n1-grid" style="width:172px; height:172px; display:grid; grid-template-columns:repeat(8,1fr); grid-template-rows:repeat(8,1fr); gap:1px; background:#FFFFFF; border:2.4px solid #202124; border-radius:7px; overflow:hidden; box-shadow:0 4px 14px rgba(32,33,36,0.14);"></div>
              </div>
              <div id="n1-coord-lbl" style="font-family:var(--font-code); font-size:10.4px; font-weight:700; color:#C5221F; height:16px; line-height:16px;">Baris 5, Kol 3</div>
            </div>

            <!-- Arrow 2: Ambil 1 Piksel -->
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px;">
              <span style="font-family:var(--font-title); font-size:9.0px; font-weight:700; color:#EA4335; text-align:center; line-height:1.15;">Ambil<br/>1 Piksel</span>
              <svg viewBox="0 0 36 18" style="width:34px; height:16px;">
                <line x1="2" y1="9" x2="25" y2="9" stroke="#EA4335" stroke-width="2.8" stroke-linecap="round"/>
                <polygon points="23,4 34,9 23,14" fill="#EA4335"/>
              </svg>
            </div>

            <!-- 3. Nilai Piksel Card -->
            <div id="n1-st3" class="n1-stage-on" style="display:flex; flex-direction:column; align-items:center; gap:9px;">
              <div style="font-family:var(--font-title); font-size:12.2px; font-weight:700; color:#EA4335; text-align:center; height:18px; line-height:18px; white-space:nowrap;">3. Nilai Piksel</div>
              <div style="height:178px; display:flex; align-items:center; justify-content:center;">
                <div id="n1-pix-card" style="width:86px; height:114px; border-radius:15px; background:#6C708F; border:2.8px solid #EA4335; color:#FFFFFF; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px; box-shadow:0 5px 14px rgba(234,67,53,0.20);">
                  <div id="n1-pix-val" style="font-family:var(--font-code); font-size:23px; font-weight:700; line-height:1;">0.45</div>
                  <div style="font-size:10.5px; opacity:0.92;">nilai 0–1</div>
                </div>
              </div>
              <div style="font-size:10.2px; color:#5F6368; height:16px; line-height:16px;">&nbsp;</div>
            </div>

            <!-- Arrow 3: Pixel -> Neuron -->
            <div style="display:flex; align-items:center; justify-content:center;">
              <svg viewBox="0 0 24 18" style="width:22px; height:16px;">
                <line x1="1" y1="9" x2="14" y2="9" stroke="#1A73E8" stroke-width="2.8" stroke-linecap="round"/>
                <polygon points="12,4 23,9 12,14" fill="#1A73E8"/>
              </svg>
            </div>

            <!-- 4. Neuron Glowing Circle -->
            <div id="n1-st4" class="n1-stage-on" style="display:flex; flex-direction:column; align-items:center; gap:9px;">
              <div style="font-family:var(--font-title); font-size:12.2px; font-weight:700; color:#1A73E8; text-align:center; height:18px; line-height:18px; white-space:nowrap;">4. Neuron</div>
              <div style="height:178px; display:flex; align-items:center; justify-content:center;">
                <div id="n1-neuron-ring" style="width:102px; height:102px; border-radius:50%; background:#E8F0FE; border:2.4px solid #C6DAFC; display:flex; align-items:center; justify-content:center; box-shadow:0 5px 16px rgba(66,133,244,0.20);">
                  <div id="n1-neuron-core" style="width:82px; height:82px; border-radius:50%; background:#4285F4; border:2.8px solid #FFFFFF; color:#FFFFFF; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px;">
                    <div id="n1-neuron-idx" style="font-family:var(--font-code); font-size:11.5px; font-weight:700; color:#D2E3FC; line-height:1;">x₁</div>
                    <div id="n1-neuron-val" style="font-family:var(--font-code); font-size:21px; font-weight:700; line-height:1.05;">0.45</div>
                  </div>
                </div>
              </div>
              <div style="font-size:10.0px; color:#5F6368; text-align:center; height:16px; line-height:16px; white-space:nowrap;">(pemegang 1 angka)</div>
            </div>
          </div>

          <div id="n1-caption" class="sync-card sync-no-badge" style="font-size:11.4px; font-weight:700; color:#202124; text-align:center; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:9px; padding:6px 10px;">
            Setiap 1 kotak piksel pada foto Elsa diwakili oleh tepat 1 lingkaran Neuron yang memegang angkanya.
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 21: ANIMASI INTERAKTIF FLATTEN (KIRI->KANAN, ATAS->BAWAH -> INPUT LAYER) -->
    <section class="slide" data-title="Bab 3A: Animasi Flatten — Piksel Disusun ke Bawah Menjadi Input Layer" data-notes="Alokasi waktu: 1.5 menit. Klik tombol 'Play' (atau '+1 Piksel' pelan-pelan) agar peserta melihat langsung tiap piksel foto Elsa (4×4 = 16 piksel) dipindai dari kiri ke kanan, atas ke bawah, lalu terbang dan bertumpuk vertikal menjadi 1 kolom Input Layer berisi 16 neuron!">
      <div class="kicker">BAB 03 · TAHAP 2.1 · FLATTEN → INPUT LAYER</div>
      <h2>Neuron Disusun ke Bawah (<span class="hl-blue">Flatten</span>) = <span class="hl-green">Input Layer</span></h2>
      <div class="sim-bar pdf-keep-ui" id="flatten-ctrl" style="margin-bottom:6px; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:11px; padding:4px 9px; gap:6px;">
        <div style="display:flex; flex-wrap:wrap; gap:5px; align-items:center;">
          <button class="btn-ui" id="flt-btn-play" onclick="playFlattenAnim()" style="padding:4px 10px; font-size:10.6px; background:#34A853; border-color:#34A853;">▶ Play</button>
          <button class="btn-ui outline" id="flt-btn-step" onclick="stepFlattenAnim()" style="padding:4px 9px; font-size:10.6px; color:#137333; border-color:#A8DAB5;">⏭ +1 Piksel</button>
          <button class="btn-ui outline" id="flt-btn-reset" onclick="resetFlattenAnim()" style="padding:4px 9px; font-size:10.6px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
          <span style="width:1px; height:16px; background:#DADCE0; margin:0 2px;"></span>
          <button class="btn-ui outline" id="flt-btn-done" onclick="completeFlattenAnim()" style="padding:4px 9px; font-size:10.4px;">✓ Semua (16/16)</button>
        </div>
        <span class="pill green" id="flatten-status" style="font-size:10.4px;">Input Layer: 16 / 16 neuron (Selesai!)</span>
      </div>
      <div id="flt-stage-wrap" style="position:relative; flex:1; min-height:0; display:grid; grid-template-columns:222px 40px 1fr; gap:6px; align-items:stretch; background:#FFFFFF; border:1.5px solid #C6DAFC; border-radius:14px; padding:8px 12px; margin-bottom:7px;">
        <canvas id="flt-split-canvas" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:20;"></canvas>
        <!-- Left column: EXACT 1:1 size & vertical alignment with the 4x4 grid inside #flatten-canvas! -->
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
          <div style="display:flex; flex-direction:column; align-items:center; width:218px; height:324px; padding-top:14px; box-sizing:border-box;">
            <div style="font-family:var(--font-title); font-size:12.2px; font-weight:700; color:#202124; line-height:16px; height:16px; margin-bottom:14px;">Foto Elsa (Crop)</div>
            <div id="flt-photo-box" style="position:relative; width:218px; height:218px; border-radius:11px; overflow:hidden; border:2.5px solid #4285F4; box-shadow:0 4px 12px rgba(66,133,244,0.14); flex-shrink:0;">
              <img id="flt-elsa-img" src="assets/P02/thumb_elsa_flatten.jpg" alt="Foto Asli Elsa (Crop Figur)" style="width:100%; height:100%; object-fit:cover; display:block;"/>
              <!-- Subtle 4x4 grid lines matching the 16 pixel blocks -->
              <div style="position:absolute; inset:0; background-image:linear-gradient(to right, rgba(255,255,255,0.55) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.55) 1px, transparent 1px); background-size:25% 25%; pointer-events:none;"></div>
            </div>
            <div style="font-size:9.8px; color:#5F6368; line-height:1.3; margin-top:11px;">Dibagi <code>4×4</code> (16 piksel nyata) agar warna asli &amp; urutan pindai jelas.</div>
          </div>
        </div>
        <!-- Connecting arrow centered vertically with the 224x224 Photo & 4x4 Grid -->
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px; padding-bottom:18px;">
          <span style="font-family:var(--font-title); font-size:9.6px; font-weight:700; color:#1A73E8; text-align:center; line-height:1.15;">Bagi<br/>4×4</span>
          <svg viewBox="0 0 40 22" style="width:38px; height:20px;">
            <line x1="2" y1="11" x2="29" y2="11" stroke="#4285F4" stroke-width="3.2" stroke-linecap="round"/>
            <polygon points="27,4 39,11 27,18" fill="#4285F4"/>
          </svg>
        </div>
        <div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; min-height:0;">
          <canvas id="flatten-canvas" width="800" height="340" style="width:100%; height:100%; max-height:336px; object-fit:contain; display:block;"></canvas>
        </div>
      </div>
      <div class="grid-3" style="flex:0 0 auto; gap:10px;">
        <div id="flt-card-1" class="card tint-blue sync-card" style="padding:8px 11px; gap:2px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title" style="font-size:12.4px; color:#1A73E8;">1. Pindai Kiri → Kanan, Atas → Bawah</div>
          <div style="font-size:11.1px; color:#3C4043; line-height:1.36;">Baris 1 (<code>x₁..x₄</code>), Baris 2 (<code>x₅..x₈</code>), Baris 3 (<code>x₉..x₁₂</code>), lalu Baris 4 (<code>x₁₃..x₁₆</code>).</div>
        </div>
        <div id="flt-card-2" class="card tint-yellow sync-card" style="padding:8px 11px; gap:2px;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title" style="font-size:12.4px; color:#B06000;">2. Ubah &amp; Susun Bertumpuk (<em>Flatten</em>)</div>
          <div style="font-size:11.1px; color:#3C4043; line-height:1.36;">Setiap kotak piksel menjadi <strong>1 neuron</strong> lalu ditumpuk rapi vertikal dari atas ke bawah.</div>
        </div>
        <div id="flt-card-3" class="card tint-green sync-card" style="padding:8px 11px; gap:2px;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title" style="font-size:12.4px; color:#137333;">3. Terbentuk <em>Input Layer</em></div>
          <div style="font-size:11.1px; color:#3C4043; line-height:1.36;">Kumpulan neuron dalam 1 kolom vertikal disebut <strong>Layer</strong> — lapisan pertama ini adalah <strong>Input Layer</strong>!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 22: INPUT LAYER SKALA FOTO BERWARNA (RGB) + SIMULATOR #3 (FULL-WIDTH 3-STAGE TRANSFORM) -->
    <section class="slide" data-title="Bab 3A: Berapa Jumlah Neuron di Input Layer Foto Berwarna?" data-notes="Alokasi waktu: 2 menit. Lanjutkan dari contoh mini 4×4 (16 neuron) ke foto Frozen berwarna RGB secara penuh: tunjukkan dimensi Tinggi (H) × Lebar (W) × Channel (C) di foto original Elsa, kurung kurawal total neuron di hasil Flatten 1D, lalu angka piksel 0.0–1.0 di Input Layer. Coba klik ketiga preset Frozen.">
      <div class="kicker">BAB 03 · TAHAP 2.2 · SKALA INPUT LAYER (H×W×C)</div>
      <h2><span class="hl-blue">Input Layer</span>: <span class="hl-red">Tinggi × Lebar × Channel</span></h2>

      <!-- Compact Single-Row Control Bar (Per-Pixel Animation + Frozen Presets + Live Sliders) -->
      <div class="sim-bar pdf-keep-ui" id="in-presets" style="margin-bottom:8px; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:12px; padding:5px 10px; gap:6px;">
        <div style="display:flex; flex-wrap:wrap; gap:5px; align-items:center;">
          <button class="btn-ui" id="in-btn-play" onclick="playInProcess()" style="padding:4px 9px; font-size:10.6px; background:#34A853; border-color:#34A853;">▶ Play</button>
          <button class="btn-ui outline" id="in-btn-step" onclick="stepInProcess()" style="padding:4px 8px; font-size:10.6px; color:#137333; border-color:#A8DAB5;">⏭ +1 Piksel</button>
          <button class="btn-ui outline" id="in-btn-reset" onclick="resetInProcessZero()" style="padding:4px 8px; font-size:10.6px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
          <span style="width:1px; height:18px; background:#DADCE0; margin:0 2px;"></span>
          <button class="btn-ui outline" data-in="64_1" onclick="setInSize(64,64,1,this)" style="padding:4px 7px; font-size:10.2px;">64×64×1 (Gray)</button>
          <button class="btn-ui outline" data-in="64_3" onclick="setInSize(64,64,3,this)" style="padding:4px 7px; font-size:10.2px;">64×64×3 (RGB)</button>
          <button class="btn-ui" data-in="224_3" onclick="setInSize(224,224,3,this)" style="padding:4px 7px; font-size:10.2px;">224×224×3 (RGB)</button>
        </div>
        <div style="display:flex; align-items:center; gap:9px; font-size:10.8px; color:#3C4043;">
          <label style="display:inline-flex; align-items:center; gap:4px; font-weight:600;">
            <span>H=W</span>
            <input id="in-hw" type="range" min="16" max="256" step="8" value="224" oninput="updateInCalc()" style="width:68px; accent-color:#4285F4;"/>
            <span class="sim-val" id="in-hw-v" style="min-width:46px; font-size:10.2px;">224×224</span>
          </label>
          <label style="display:inline-flex; align-items:center; gap:4px; font-weight:600;">
            <span>Ch</span>
            <input id="in-ch" type="range" min="1" max="3" step="2" value="3" oninput="updateInCalc()" style="width:36px; accent-color:#34A853;"/>
            <span class="sim-val" id="in-ch-v" style="min-width:46px; font-size:10.2px;">3 (RGB)</span>
          </label>
        </div>
      </div>

      <!-- ENLARGED FULL-WIDTH 3-STAGE TRANSFORMATION DIAGRAM WITH PHYSICAL MOTION OVERLAY -->
      <div id="in-hero-wrap" style="position:relative; flex:1; min-height:0; display:grid; grid-template-columns:1.12fr 48px 1.15fr 48px 1.18fr; gap:6px; align-items:stretch; background:#FFFFFF; border:1.5px solid #C6DAFC; border-radius:16px; padding:12px 14px; box-shadow:0 4px 14px rgba(66,133,244,0.06);">
        <canvas id="in-motion-canvas" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:25;"></canvas>

        <!-- STAGE 1: ORIGINAL ELSA WITH HEIGHT (H), WIDTH (W), AND CHANNEL (C) ANNOTATIONS -->
        <div id="in-stage-1" class="in-stage-card" style="display:flex; flex-direction:column; align-items:center; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:12px; padding:10px 10px 9px;">
          <div style="font-family:var(--font-title); font-size:12.8px; font-weight:700; color:#202124;">1. Foto Original Elsa</div>

          <!-- Dimensioned Image Container -->
          <div style="display:flex; flex-direction:column; align-items:center; gap:4px; margin:2px 0;">
            <!-- Top Width (W) Arrow -->
            <div style="display:flex; align-items:center; gap:5px; padding-left:34px;">
              <span style="display:inline-block; width:36px; height:2px; background:#1A73E8;"></span>
              <span id="in-w-dim" style="font-family:var(--font-code); font-size:10.5px; font-weight:700; color:#1A73E8; background:#E8F0FE; border:1px solid #C6DAFC; border-radius:6px; padding:1px 7px;">Lebar (W) = 224</span>
              <span style="display:inline-block; width:36px; height:2px; background:#1A73E8;"></span>
            </div>

            <div style="display:flex; align-items:center; gap:6px;">
              <!-- Left Height (H) Vertical Dimension -->
              <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; width:28px; height:174px; position:relative;">
                <div style="position:absolute; top:2px; bottom:2px; left:50%; width:2px; background:#EA4335; transform:translateX(-50%);"></div>
                <div style="position:absolute; top:0; left:50%; width:8px; height:2px; background:#EA4335; transform:translateX(-50%);"></div>
                <div style="position:absolute; bottom:0; left:50%; width:8px; height:2px; background:#EA4335; transform:translateX(-50%);"></div>
                <span id="in-h-dim" style="position:relative; z-index:2; writing-mode:vertical-rl; transform:rotate(180deg); font-family:var(--font-code); font-size:10.2px; font-weight:700; color:#C5221F; background:#FCE8E6; border:1px solid #F6AEA9; border-radius:6px; padding:6px 2px;">Tinggi (H) = 224</span>
              </div>

              <!-- Real Elsa Photo with 3-Channel Depth Stack (R, G, B) + Clickable Slice Trigger -->
              <div style="position:relative; width:174px; height:174px; margin-right:16px; margin-bottom:10px;">
                <!-- Back Channel Layer B (Blue) -->
                <div id="in-ch-layer-b" style="position:absolute; top:12px; left:14px; width:166px; height:166px; border-radius:10px; background:#E8F0FE; border:2px solid #4285F4; z-index:1;"></div>
                <!-- Middle Channel Layer G (Green) -->
                <div id="in-ch-layer-g" style="position:absolute; top:6px; left:7px; width:166px; height:166px; border-radius:10px; background:#E6F4EA; border:2px solid #34A853; z-index:2;"></div>
                <!-- Front Image Layer (R / Original Elsa) with clickable 8x8 Pixel Grid -->
                <div id="in-img-frame" class="in-clickable" onclick="triggerPixelClick(event)" title="Klik kotak piksel mana saja di Foto Elsa untuk menerbangkannya ke Flatten & Input Layer!" style="position:relative; z-index:3; width:166px; height:166px; border-radius:10px; overflow:hidden; border:2.5px solid #EA4335; box-shadow:0 4px 10px rgba(32,33,36,0.12);">
                  <img id="in-elsa-img" src="assets/P02/thumb_elsa.jpg" alt="Foto Original Elsa" style="width:100%; height:100%; object-fit:cover; display:block; transition:filter 0.2s;"/>
                  <!-- Subtle 8x8 pixel grid overlay showing individual square pixels -->
                  <div style="position:absolute; inset:0; background-image:linear-gradient(to right, rgba(255,255,255,0.48) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.48) 1px, transparent 1px); background-size:12.5% 12.5%; pointer-events:none;"></div>
                  <!-- Animated scanner beam -->
                  <div id="in-scan-bar" class="in-scan-bar"></div>
                </div>
                <!-- 3-Channel Depth Callout Tag at bottom-right -->
                <div id="in-ch-tag" style="position:absolute; right:-14px; bottom:-12px; z-index:4; background:#202124; color:#FFFFFF; font-family:var(--font-code); font-size:9.5px; font-weight:700; padding:2px 7px; border-radius:6px; box-shadow:0 2px 6px rgba(0,0,0,0.2);">C = 3 (R·G·B)</div>
              </div>
            </div>
          </div>

          <!-- Bottom Dimension Summary Pill -->
          <div id="in-shape-pill" style="font-family:var(--font-code); font-size:11.2px; font-weight:700; color:#1A73E8; background:#E8F0FE; border:1px solid #C6DAFC; border-radius:8px; padding:4px 10px; width:100%; text-align:center;">
            Shape: (224, 224, 3) · RGB
          </div>
        </div>

        <!-- ARROW 1 -> 2 -->
        <div id="in-arrow-1" class="in-arrow-box" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px;">
          <span style="font-family:var(--font-title); font-size:10.5px; font-weight:700; color:#1A73E8;">Flatten</span>
          <div style="position:relative; width:44px; height:22px;">
            <svg viewBox="0 0 46 22" style="width:44px; height:22px; display:block;">
              <line x1="2" y1="11" x2="34" y2="11" stroke="#1A73E8" stroke-width="3.2" stroke-linecap="round"/>
              <polygon points="32,4 44,11 32,18" fill="#1A73E8"/>
            </svg>
            <div id="in-dot-1" class="in-arrow-dot" style="background:#FBBC04; box-shadow:0 0 8px #FBBC04;"></div>
          </div>
          <span style="font-size:9.2px; color:#5F6368; text-align:center; line-height:1.2;">piksel demi<br/>piksel</span>
        </div>

        <!-- STAGE 2: FLATTENED 1D STRIP + BIG CURLY BRACE WITH TOTAL NEURON MULTIPLICATION -->
        <div id="in-stage-2" class="in-stage-card" style="display:flex; flex-direction:column; align-items:center; justify-content:space-between; background:#FEF7E0; border:1.5px solid #FDE293; border-radius:12px; padding:10px 10px 9px;">
          <div style="font-family:var(--font-title); font-size:12.8px; font-weight:700; color:#B06000;">2. Hasil Flatten (1D)</div>

          <div style="display:flex; align-items:center; justify-content:center; gap:6px; width:100%; flex:1; padding:2px 0;">
            <!-- Real Elsa 1D Flattened Strip (Clickable to split pixels into Input Layer!) -->
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px;">
              <span style="font-family:var(--font-code); font-size:8.8px; font-weight:700; color:#5F6368;">Baris 1</span>
              <div id="in-strip-wrap" class="in-clickable" onclick="triggerPixelSplitClick()" title="Klik pita 1D untuk memecah piksel ke lingkaran angka Input Layer!" style="width:48px; height:216px; border-radius:8px; overflow:hidden; border:2.5px solid #E37400; box-shadow:0 3px 8px rgba(227,116,0,0.16); background:#FFF8E1; position:relative;">
                <img id="in-strip-img" src="assets/P02/03c_elsa_flatten_strip.png" alt="Pita piksel 1D hasil Flatten foto Elsa" style="width:100%; height:100%; object-fit:fill; display:block; transition:filter 0.2s;"/>
              </div>
              <span style="font-family:var(--font-code); font-size:8.8px; font-weight:700; color:#5F6368;">Baris akhir</span>
            </div>

            <!-- Big Crisp SVG Curly Brace -->
            <svg viewBox="0 0 34 230" style="width:30px; height:220px; flex-shrink:0;">
              <path id="in-brace-path" d="M 4 6 C 17 6, 17 18, 17 34 L 17 92 C 17 107, 22 115, 31 115 C 22 115, 17 123, 17 138 L 17 196 C 17 212, 17 224, 4 224"
                    fill="none" stroke="#B06000" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="280" stroke-dashoffset="0"/>
            </svg>

            <!-- Multiplication & Giant Total Neuron Callout right beside the brace tip -->
            <div style="display:flex; flex-direction:column; align-items:flex-start; justify-content:center; gap:6px; min-width:142px;">
              <span style="font-family:var(--font-title); font-size:10px; font-weight:700; color:#B06000; letter-spacing:0.04em;">HASIL PERKALIAN</span>
              <div id="in-brace-eq" style="font-family:var(--font-code); font-size:13px; font-weight:700; color:#202124; background:#FFFFFF; border:1px solid #FDE293; border-radius:8px; padding:4px 9px;">224 × 224 × 3</div>
              <div style="font-family:var(--font-title); font-size:10px; font-weight:700; color:#5F6368; margin-top:2px;">TOTAL NEURON:</div>
              <div id="in-total" class="big-num hl-blue" style="font-size:35px; line-height:1.05; letter-spacing:-0.02em;">150.528</div>
              <div id="in-brace-sub" style="font-size:10.5px; color:#5F6368; line-height:1.3;">neuron piksel bertumpuk<br/>(<strong>3× lipat</strong> dari Grayscale)</div>
            </div>
          </div>

          <div id="in-formula" style="font-family:var(--font-code); font-size:10.2px; font-weight:700; color:#B06000; background:#FFFFFF; border:1px solid #FDE293; border-radius:8px; padding:4px 8px; width:100%; text-align:center;">
            224 (H) × 224 (W) × 3 (RGB) = 150.528
          </div>
        </div>

        <!-- ARROW 2 -> 3 -->
        <div id="in-arrow-2" class="in-arrow-box" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px;">
          <span style="font-family:var(--font-title); font-size:10.5px; font-weight:700; color:#137333;">Angka</span>
          <div style="position:relative; width:44px; height:22px;">
            <svg viewBox="0 0 46 22" style="width:44px; height:22px; display:block;">
              <line x1="2" y1="11" x2="34" y2="11" stroke="#34A853" stroke-width="3.2" stroke-linecap="round"/>
              <polygon points="32,4 44,11 32,18" fill="#34A853"/>
            </svg>
            <div id="in-dot-2" class="in-arrow-dot" style="background:#34A853; box-shadow:0 0 8px #34A853;"></div>
          </div>
          <span style="font-size:9.2px; color:#5F6368; text-align:center; line-height:1.2;">skala<br/>0.0–1.0</span>
        </div>

        <!-- STAGE 3: INPUT LAYER CAPSULE WITH ACTUAL NUMBERED NEURONS -->
        <div id="in-stage-3" class="in-stage-card" style="display:flex; flex-direction:column; align-items:center; justify-content:space-between; background:#E8F0FE; border:2px solid #4285F4; border-radius:14px; padding:10px 12px 9px;">
          <div style="text-align:center;">
            <div style="font-family:var(--font-title); font-size:13px; font-weight:700; color:#1A73E8;">3. Input Layer (Angka)</div>
            <div id="in-layer-sub" style="font-family:var(--font-code); font-size:10px; color:#5F6368;">1 Kolom Vertikal · 150.528 Neuron</div>
          </div>

          <!-- Dynamic Vertical Neuron Stack (click any row to trace origin!) -->
          <div id="in-layer-nodes" style="display:flex; flex-direction:column; justify-content:space-between; gap:3px; width:100%; flex:1; margin:5px 0; background:#FFFFFF; border:1px solid #C6DAFC; border-radius:11px; padding:6px 9px;"></div>

          <div style="font-size:10.3px; color:#1A73E8; font-weight:700; text-align:center;">
            Klik piksel di Foto Elsa atau neuron di atas!
          </div>
        </div>
      </div>

      <div id="in-live-callout" class="callout sync-card sync-no-badge" style="margin-top:7px; flex:0 0 auto; font-size:11.8px; padding:7px 12px;">
        <strong>Aturan cepat:</strong> Pada foto berwarna (<code>RGB = 3</code>), tiap <strong>1 kotak piksel</strong> pecah menjadi <strong>3 neuron</strong> (<code>R, G, B</code>). Klik <strong>▶ Play</strong>, <strong>⏭ +1 Piksel</strong>, atau klik kotak piksel mana saja pada Foto Elsa!
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 23: INPUT & OUTPUT LAYER (INTERACTIVE 60FPS PIXEL-BY-PIXEL & NEURON-BY-NEURON MOTION) -->
    <section class="slide" data-title="Bab 3B: Input Layer &amp; Output Layer" data-notes="Alokasi waktu: 1.5 menit. Hubungkan Input Layer (150.528 neuron piksel) langsung ke Output Layer di ujung jaringan dengan animasi interaktif pixel-by-pixel, neuron-by-neuron, dan koneksi neuron-by-neuron. Klik Play, +1 Langkah, atau klik langsung piksel foto / neuron input / neuron output untuk mendemonstrasikan bagaimana 1 neuron input terhubung ke seluruh 5 neuron output.">
      <div class="kicker">BAB 03 · TAHAP 3.1 · INPUT &amp; OUTPUT LAYER</div>
      <h2><span class="hl-blue">Input Layer</span> &amp; <span class="hl-green">Output Layer</span></h2>

      <!-- Compact Single-Row Interactive Control Bar -->
      <div class="sim-bar pdf-keep-ui" style="margin-bottom:6px; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:11px; padding:4px 9px; gap:6px;">
        <div style="display:flex; align-items:center; gap:5px; flex-shrink:0;">
          <button class="btn-ui" id="io-btn-play" onclick="playIoMotion()" style="padding:3.5px 9px; font-size:10.4px; background:#34A853; border-color:#34A853;">▶ Play</button>
          <button class="btn-ui outline" id="io-btn-step" onclick="stepIoMotion()" style="padding:3.5px 8px; font-size:10.4px; color:#137333; border-color:#A8DAB5;">⏭ +1 Langkah</button>
          <button class="btn-ui outline" id="io-btn-reset" onclick="resetIoMotionZero()" style="padding:3.5px 8px; font-size:10.4px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
        </div>
        <div id="io-live-status" style="font-size:10.5px; color:#3C4043; font-weight:500; text-align:right; flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
          <strong style="color:#1A73E8;">Interaktif:</strong> Klik <strong>▶ Play</strong>, <strong>⏭ +1 Langkah</strong>, atau klik langsung <strong>piksel foto / neuron Input / neuron Output</strong>!
        </div>
      </div>

      <!-- HERO 4-STAGE PIPELINE WITH 60FPS PIXEL/NEURON/CONNECTION MOTION CANVAS -->
      <div id="io-hero-wrap" style="position:relative; flex:1; min-height:0; display:grid; grid-template-columns:144px 36px 1fr 38px 162px; gap:5px; align-items:stretch; background:#FFFFFF; border:1.5px solid #C6DAFC; border-radius:15px; padding:6px 10px; margin-bottom:6px; box-shadow:0 4px 14px rgba(66,133,244,0.06);">
        <canvas id="io-motion-canvas" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:25;"></canvas>

        <!-- 1. FOTO ORIGINAL (CLICKABLE 8x8 PIXEL GRID!) -->
        <div id="io-stage-1" class="io-stage" style="display:flex; flex-direction:column; align-items:center; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:12px; padding:7px 7px;">
          <div style="font-family:var(--font-title); font-size:11.2px; font-weight:700; color:#202124;">1. Foto Original</div>
          <div id="io-img-frame" class="in-clickable" onclick="triggerIoPixelClick(event)" title="Klik kotak piksel mana saja untuk melacak alurnya hingga Output Layer!" style="position:relative; width:102px; height:102px; border-radius:10px; overflow:hidden; border:2.5px solid #4285F4; box-shadow:0 3px 10px rgba(66,133,244,0.16);">
            <img src="assets/P02/thumb_elsa.jpg" alt="Foto Original Elsa" style="width:100%; height:100%; object-fit:cover; display:block;"/>
            <div style="position:absolute; inset:0; background-image:linear-gradient(to right, rgba(255,255,255,0.45) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.45) 1px, transparent 1px); background-size:12.5% 12.5%; pointer-events:none;"></div>
          </div>
          <div style="font-family:var(--font-code); font-size:9.4px; font-weight:700; color:#1A73E8; background:#E8F0FE; border:1px solid #C6DAFC; border-radius:7px; padding:1.5px 7px;">224×224×3</div>
        </div>

        <!-- ARROW: Foto -> Input Layer -->
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px;">
          <span style="font-family:var(--font-title); font-size:9.2px; font-weight:700; color:#1A73E8;">Flatten</span>
          <svg viewBox="0 0 38 20" style="width:34px; height:18px;">
            <line x1="2" y1="10" x2="27" y2="10" stroke="#4285F4" stroke-width="3" stroke-linecap="round"/>
            <polygon points="25,4 36,10 25,16" fill="#4285F4"/>
          </svg>
        </div>

        <!-- 2 & 3. UNIFIED SVG: TALL DENSE INPUT LAYER (150.528) -> FUNNEL CONNECTIONS -> COMPACT OUTPUT LAYER (5) -->
        <div style="display:flex; align-items:center; justify-content:center; min-height:0;">
          <svg id="io-svg" viewBox="0 0 544 278" style="width:100%; height:100%; max-height:242px; display:block;">
            <!-- Input Layer Capsule (TALLEST & DENSE — visibly packed with many neurons!) -->
            <rect id="io-in-cap" x="4" y="2" width="176" height="274" rx="14" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.2"/>
            <text x="92" y="20" text-anchor="middle" font-family="Poppins, Arial" font-size="12" font-weight="700" fill="#1A73E8">2. Input Layer</text>
            <text x="92" y="33" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="9.2" font-weight="700" fill="#1A73E8">150.528 neuron piksel</text>

            <!-- Output Layer Capsule (VISIBLY SHORTER & COMPACT — only 5 classes!) -->
            <rect id="io-out-cap" x="308" y="42" width="232" height="196" rx="14" fill="#E6F4EA" stroke="#34A853" stroke-width="2.2"/>
            <text x="424" y="61" text-anchor="middle" font-family="Poppins, Arial" font-size="12" font-weight="700" fill="#137333">3. Output Layer</text>
            <text x="424" y="74" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="9.2" fill="#5F6368">1 layer · 5 neuron = 5 kelas</text>

            <!-- Base Funnel Connection Lines (dimmed cleanly during live animated wire propagation) -->
            <g id="io-wires-bg" class="io-wires-group" stroke="#CFD4DA" stroke-width="1.15" opacity="0.88">
              <line x1="180" y1="50"  x2="318" y2="96"/><line x1="180" y1="50"  x2="318" y2="156"/><line x1="180" y1="50"  x2="318" y2="186"/><line x1="180" y1="50"  x2="318" y2="216"/>
              <line x1="180" y1="73"  x2="318" y2="96"/><line x1="180" y1="73"  x2="318" y2="156"/><line x1="180" y1="73"  x2="318" y2="186"/><line x1="180" y1="73"  x2="318" y2="216"/>
              <line x1="180" y1="96"  x2="318" y2="96"/><line x1="180" y1="96"  x2="318" y2="156"/><line x1="180" y1="96"  x2="318" y2="186"/><line x1="180" y1="96"  x2="318" y2="216"/>
              <line x1="180" y1="119" x2="318" y2="96"/><line x1="180" y1="119" x2="318" y2="156"/><line x1="180" y1="119" x2="318" y2="186"/><line x1="180" y1="119" x2="318" y2="216"/>
              <line x1="180" y1="142" x2="318" y2="96"/><line x1="180" y1="142" x2="318" y2="156"/><line x1="180" y1="142" x2="318" y2="186"/><line x1="180" y1="142" x2="318" y2="216"/>
              <line x1="180" y1="165" x2="318" y2="96"/><line x1="180" y1="165" x2="318" y2="156"/><line x1="180" y1="165" x2="318" y2="186"/><line x1="180" y1="165" x2="318" y2="216"/>
              <line x1="180" y1="214" x2="318" y2="96"/><line x1="180" y1="214" x2="318" y2="156"/><line x1="180" y1="214" x2="318" y2="186"/><line x1="180" y1="214" x2="318" y2="216"/>
              <line x1="180" y1="237" x2="318" y2="96"/><line x1="180" y1="237" x2="318" y2="156"/><line x1="180" y1="237" x2="318" y2="186"/><line x1="180" y1="237" x2="318" y2="216"/>
              <line x1="180" y1="260" x2="318" y2="96"/><line x1="180" y1="260" x2="318" y2="156"/><line x1="180" y1="260" x2="318" y2="186"/><line x1="180" y1="260" x2="318" y2="216"/>
            </g>
            <!-- Highlighted green funnel lines converging into Elsa (y2) -->
            <g id="io-wires-hi" class="io-wires-group" stroke="#34A853" stroke-width="1.85" opacity="0.82">
              <line x1="180" y1="50"  x2="318" y2="126"/>
              <line x1="180" y1="73"  x2="318" y2="126"/>
              <line x1="180" y1="96"  x2="318" y2="126"/>
              <line x1="180" y1="119" x2="318" y2="126"/>
              <line x1="180" y1="142" x2="318" y2="126"/>
              <line x1="180" y1="165" x2="318" y2="126"/>
              <line x1="180" y1="214" x2="318" y2="126"/>
              <line x1="180" y1="237" x2="318" y2="126"/>
              <line x1="180" y1="260" x2="318" y2="126"/>
            </g>
            <!-- Middle label pill -->
            <rect x="186" y="7" width="116" height="30" rx="8" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.5"/>
            <text x="244" y="19.5" text-anchor="middle" font-family="Poppins, Arial" font-size="9.2" font-weight="700" fill="#B06000">Kalkulasi</text>
            <text x="244" y="31" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="700" fill="#B06000">probabilitas kelas</text>

            <!-- 9 Densely Stacked Interactive Input Layer Neuron Circles (click any neuron to fire its 5 wires!) -->
            <g id="io-in-0" class="io-in-node" onclick="inspectIoInput(0)"><title>Klik x₁ untuk melihat 5 koneksi ke Output Layer!</title>
              <rect x="12" y="39" width="160" height="22" rx="7" fill="transparent"/>
              <circle id="io-in-c-0" cx="28" cy="50"  r="10" fill="#EA4335" stroke="#FFF" stroke-width="1.5"/><text x="28" y="53"  text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="#FFF">{er0:.2f}</text>
              <text x="44" y="53"  font-family="Roboto Mono, monospace" font-size="9.2" font-weight="700" fill="#202124">x₁</text><text x="64" y="53"  font-family="Roboto, Arial" font-size="8.4" fill="#5F6368">Piksel 1 (R)</text>
            </g>
            <g id="io-in-1" class="io-in-node" onclick="inspectIoInput(1)"><title>Klik x₂ untuk melihat 5 koneksi ke Output Layer!</title>
              <rect x="12" y="62" width="160" height="22" rx="7" fill="transparent"/>
              <circle id="io-in-c-1" cx="28" cy="73"  r="10" fill="#34A853" stroke="#FFF" stroke-width="1.5"/><text x="28" y="76"  text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="#FFF">{eg0:.2f}</text>
              <text x="44" y="76"  font-family="Roboto Mono, monospace" font-size="9.2" font-weight="700" fill="#202124">x₂</text><text x="64" y="76"  font-family="Roboto, Arial" font-size="8.4" fill="#5F6368">Piksel 1 (G)</text>
            </g>
            <g id="io-in-2" class="io-in-node" onclick="inspectIoInput(2)"><title>Klik x₃ untuk melihat 5 koneksi ke Output Layer!</title>
              <rect x="12" y="85" width="160" height="22" rx="7" fill="transparent"/>
              <circle id="io-in-c-2" cx="28" cy="96"  r="10" fill="#4285F4" stroke="#FFF" stroke-width="1.5"/><text x="28" y="99"  text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="#FFF">{eb0:.2f}</text>
              <text x="44" y="99"  font-family="Roboto Mono, monospace" font-size="9.2" font-weight="700" fill="#202124">x₃</text><text x="64" y="99"  font-family="Roboto, Arial" font-size="8.4" fill="#5F6368">Piksel 1 (B)</text>
            </g>
            <g id="io-in-3" class="io-in-node" onclick="inspectIoInput(3)"><title>Klik x₄ untuk melihat 5 koneksi ke Output Layer!</title>
              <rect x="12" y="108" width="160" height="22" rx="7" fill="transparent"/>
              <circle id="io-in-c-3" cx="28" cy="119" r="10" fill="#EA4335" stroke="#FFF" stroke-width="1.5"/><text x="28" y="122" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="#FFF">{er0:.2f}</text>
              <text x="44" y="122" font-family="Roboto Mono, monospace" font-size="9.2" font-weight="700" fill="#202124">x₄</text><text x="64" y="122" font-family="Roboto, Arial" font-size="8.4" fill="#5F6368">Piksel 2 (R)</text>
            </g>
            <g id="io-in-4" class="io-in-node" onclick="inspectIoInput(4)"><title>Klik x₅ untuk melihat 5 koneksi ke Output Layer!</title>
              <rect x="12" y="131" width="160" height="22" rx="7" fill="transparent"/>
              <circle id="io-in-c-4" cx="28" cy="142" r="10" fill="#34A853" stroke="#FFF" stroke-width="1.5"/><text x="28" y="145" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="#FFF">{eg0:.2f}</text>
              <text x="44" y="145" font-family="Roboto Mono, monospace" font-size="9.2" font-weight="700" fill="#202124">x₅</text><text x="64" y="145" font-family="Roboto, Arial" font-size="8.4" fill="#5F6368">Piksel 2 (G)</text>
            </g>
            <g id="io-in-5" class="io-in-node" onclick="inspectIoInput(5)"><title>Klik x₆ untuk melihat 5 koneksi ke Output Layer!</title>
              <rect x="12" y="154" width="160" height="22" rx="7" fill="transparent"/>
              <circle id="io-in-c-5" cx="28" cy="165" r="10" fill="#4285F4" stroke="#FFF" stroke-width="1.5"/><text x="28" y="168" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="#FFF">{eb0:.2f}</text>
              <text x="44" y="168" font-family="Roboto Mono, monospace" font-size="9.2" font-weight="700" fill="#202124">x₆</text><text x="64" y="168" font-family="Roboto, Arial" font-size="8.4" fill="#5F6368">Piksel 2 (B)</text>
            </g>

            <!-- Ellipsis band for 150.519 more neurons -->
            <g id="io-in-ell" style="transition:opacity 0.28s ease;">
              <circle cx="28" cy="182" r="1.9" fill="#1A73E8"/><circle cx="28" cy="189" r="1.9" fill="#1A73E8"/><circle cx="28" cy="196" r="1.9" fill="#1A73E8"/>
              <rect id="io-in-ell-box" x="42" y="179" width="130" height="20" rx="6" fill="#FFFFFF" stroke="#C6DAFC" stroke-width="1"/>
              <text x="107" y="192" text-anchor="middle" font-family="Poppins, Arial" font-size="8.4" font-weight="700" fill="#1A73E8">+150.519 neuron lainnya</text>
            </g>

            <g id="io-in-6" class="io-in-node" onclick="inspectIoInput(6)"><title>Klik x150.526 untuk melihat 5 koneksi ke Output Layer!</title>
              <rect x="12" y="203" width="160" height="22" rx="7" fill="transparent"/>
              <circle id="io-in-c-6" cx="28" cy="214" r="10" fill="#EA4335" stroke="#FFF" stroke-width="1.5"/><text x="28" y="217" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="#FFF">{er_end:.2f}</text>
              <text x="44" y="217" font-family="Roboto Mono, monospace" font-size="8.6" font-weight="700" fill="#202124">x150.526</text><text x="103" y="217" font-family="Roboto, Arial" font-size="8.2" fill="#5F6368">akhir (R)</text>
            </g>
            <g id="io-in-7" class="io-in-node" onclick="inspectIoInput(7)"><title>Klik x150.527 untuk melihat 5 koneksi ke Output Layer!</title>
              <rect x="12" y="226" width="160" height="22" rx="7" fill="transparent"/>
              <circle id="io-in-c-7" cx="28" cy="237" r="10" fill="#34A853" stroke="#FFF" stroke-width="1.5"/><text x="28" y="240" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="#FFF">{eg_end:.2f}</text>
              <text x="44" y="240" font-family="Roboto Mono, monospace" font-size="8.6" font-weight="700" fill="#202124">x150.527</text><text x="103" y="240" font-family="Roboto, Arial" font-size="8.2" fill="#5F6368">akhir (G)</text>
            </g>
            <g id="io-in-8" class="io-in-node" onclick="inspectIoInput(8)"><title>Klik x150.528 untuk melihat 5 koneksi ke Output Layer!</title>
              <rect x="12" y="249" width="160" height="22" rx="7" fill="transparent"/>
              <circle id="io-in-c-8" cx="28" cy="260" r="10" fill="#4285F4" stroke="#FFF" stroke-width="1.5"/><text x="28" y="263" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="#FFF">{eb_end:.2f}</text>
              <text x="44" y="263" font-family="Roboto Mono, monospace" font-size="8.6" font-weight="700" fill="#202124">x150.528</text><text x="103" y="263" font-family="Roboto, Arial" font-size="8.2" fill="#5F6368">akhir (B)</text>
            </g>

            <!-- Output Layer: Compact 5 Interactive Neuron Rows (click any class to see all incoming wires!) -->
            <g id="io-out-0" class="io-out-node" onclick="inspectIoOutput(0)"><title>Klik Anna (y₁) untuk melihat seluruh sinyal masuk!</title>
              <rect id="io-out-bg-0" x="318" y="83" width="212" height="26" rx="8" fill="#FFFFFF" stroke="#DADCE0" stroke-width="1.2"/>
              <circle id="io-out-c-0" cx="334" cy="96" r="9.5" fill="#4285F4"/><text x="334" y="99" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.4" font-weight="700" fill="#FFF">y₁</text>
              <text x="350" y="99.5" font-family="Poppins, Arial" font-size="10.2" font-weight="700" fill="#202124">Anna</text>
              <rect x="414" y="91.5" width="72" height="9" rx="4.5" fill="#F1F3F4"/><rect id="io-bar-0" x="414" y="91.5" width="6" height="9" rx="4.5" fill="#4285F4"/>
              <text id="io-pct-0" x="522" y="99.5" text-anchor="end" font-family="Roboto Mono, monospace" font-size="9.5" font-weight="700" fill="#5F6368">4%</text>
            </g>

            <g id="io-out-1" class="io-out-node" onclick="inspectIoOutput(1)"><title>Klik Elsa (y₂) untuk melihat seluruh sinyal masuk!</title>
              <rect id="io-out-bg-1" x="318" y="113" width="212" height="26" rx="8" fill="#D4F0DC" stroke="#34A853" stroke-width="2"/>
              <circle id="io-out-c-1" cx="334" cy="126" r="9.5" fill="#34A853"/><text x="334" y="129" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.4" font-weight="700" fill="#FFF">y₂</text>
              <text x="350" y="129.5" font-family="Poppins, Arial" font-size="10.5" font-weight="700" fill="#137333">Elsa ★</text>
              <rect x="414" y="121.5" width="72" height="9" rx="4.5" fill="#FFFFFF"/><rect id="io-bar-1" x="414" y="121.5" width="64" height="9" rx="4.5" fill="#34A853"/>
              <text id="io-pct-1" x="522" y="129.5" text-anchor="end" font-family="Roboto Mono, monospace" font-size="9.8" font-weight="700" fill="#137333">89%</text>
            </g>

            <g id="io-out-2" class="io-out-node" onclick="inspectIoOutput(2)"><title>Klik Kristoff (y₃) untuk melihat seluruh sinyal masuk!</title>
              <rect id="io-out-bg-2" x="318" y="143" width="212" height="26" rx="8" fill="#FFFFFF" stroke="#DADCE0" stroke-width="1.2"/>
              <circle id="io-out-c-2" cx="334" cy="156" r="9.5" fill="#FBBC04"/><text x="334" y="159" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.4" font-weight="700" fill="#202124">y₃</text>
              <text x="350" y="159.5" font-family="Poppins, Arial" font-size="10.2" font-weight="700" fill="#202124">Kristoff</text>
              <rect x="414" y="151.5" width="72" height="9" rx="4.5" fill="#F1F3F4"/><rect id="io-bar-2" x="414" y="151.5" width="4" height="9" rx="4.5" fill="#FBBC04"/>
              <text id="io-pct-2" x="522" y="159.5" text-anchor="end" font-family="Roboto Mono, monospace" font-size="9.5" font-weight="700" fill="#5F6368">2%</text>
            </g>

            <g id="io-out-3" class="io-out-node" onclick="inspectIoOutput(3)"><title>Klik Olaf (y₄) untuk melihat seluruh sinyal masuk!</title>
              <rect id="io-out-bg-3" x="318" y="173" width="212" height="26" rx="8" fill="#FFFFFF" stroke="#DADCE0" stroke-width="1.2"/>
              <circle id="io-out-c-3" cx="334" cy="186" r="9.5" fill="#EA4335"/><text x="334" y="189" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.4" font-weight="700" fill="#FFF">y₄</text>
              <text x="350" y="189.5" font-family="Poppins, Arial" font-size="10.2" font-weight="700" fill="#202124">Olaf</text>
              <rect x="414" y="181.5" width="72" height="9" rx="4.5" fill="#F1F3F4"/><rect id="io-bar-3" x="414" y="181.5" width="5" height="9" rx="4.5" fill="#EA4335"/>
              <text id="io-pct-3" x="522" y="189.5" text-anchor="end" font-family="Roboto Mono, monospace" font-size="9.5" font-weight="700" fill="#5F6368">3%</text>
            </g>

            <g id="io-out-4" class="io-out-node" onclick="inspectIoOutput(4)"><title>Klik Sven (y₅) untuk melihat seluruh sinyal masuk!</title>
              <rect id="io-out-bg-4" x="318" y="203" width="212" height="26" rx="8" fill="#FFFFFF" stroke="#DADCE0" stroke-width="1.2"/>
              <circle id="io-out-c-4" cx="334" cy="216" r="9.5" fill="#5F6368"/><text x="334" y="219" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.4" font-weight="700" fill="#FFF">y₅</text>
              <text x="350" y="219.5" font-family="Poppins, Arial" font-size="10.2" font-weight="700" fill="#202124">Sven</text>
              <rect x="414" y="211.5" width="72" height="9" rx="4.5" fill="#F1F3F4"/><rect id="io-bar-4" x="414" y="211.5" width="4" height="9" rx="4.5" fill="#5F6368"/>
              <text id="io-pct-4" x="522" y="219.5" text-anchor="end" font-family="Roboto Mono, monospace" font-size="9.5" font-weight="700" fill="#5F6368">2%</text>
            </g>
          </svg>
        </div>

        <!-- ARROW: Output Layer -> Hasil Klasifikasi -->
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px;">
          <span style="font-family:var(--font-title); font-size:9px; font-weight:700; color:#137333; text-align:center; line-height:1.12;">Pilih<br/>tertinggi</span>
          <svg viewBox="0 0 38 20" style="width:34px; height:18px;">
            <line x1="2" y1="10" x2="27" y2="10" stroke="#34A853" stroke-width="3" stroke-linecap="round"/>
            <polygon points="25,4 36,10 25,16" fill="#34A853"/>
          </svg>
        </div>

        <!-- 4. HASIL KLASIFIKASI -->
        <div id="io-stage-4" class="io-stage" style="display:flex; flex-direction:column; align-items:center; justify-content:space-between; background:#E6F4EA; border:2px solid #34A853; border-radius:12px; padding:8px 9px; text-align:center;">
          <div style="font-family:var(--font-title); font-size:11.4px; font-weight:700; color:#137333;">4. Hasil Klasifikasi</div>
          <div id="io-result-card" style="display:flex; flex-direction:column; align-items:center; gap:5px; background:#FFFFFF; border:1px solid #A8DAB5; border-radius:10px; padding:9px 10px; width:100%; transition:opacity 0.3s ease;">
            <span style="font-family:var(--font-title); font-size:8.6px; font-weight:700; letter-spacing:0.06em; color:#137333; background:#E6F4EA; padding:2px 8px; border-radius:999px;">PREDIKSI AKHIR</span>
            <div id="io-result-name" style="font-family:var(--font-title); font-size:26px; font-weight:800; color:#137333; line-height:1.05;">ELSA</div>
            <span id="io-result-pct" style="font-family:var(--font-code); font-size:11px; font-weight:700; color:#FFFFFF; background:#34A853; padding:2.5px 10px; border-radius:999px;">89% Yakin</span>
          </div>
          <div style="font-size:9.2px; color:#5F6368; line-height:1.22;">Angka peluang = ilustrasi konsep</div>
        </div>
      </div>

      <!-- 4 NUMBERED EXPLANATION CARDS MATCHING STAGES 1 -> 2 -> 3 -> 4 ABOVE -->
      <div class="grid-4" style="flex:0 0 auto; gap:7px;">
        <div id="io-card-1" class="card surface io-card sync-card" style="padding:6px 9px; gap:2px;">
          <div class="card-top-bar" style="background:#5F6368;"></div>
          <div class="card-title" style="font-size:11.4px; color:#202124;">1. Foto Original</div>
          <div style="font-size:10.3px; color:#3C4043; line-height:1.32;">Foto asli Frozen (<code>224×224×3</code>) dipindai piksel demi piksel sebagai <strong>data mentah</strong> awal.</div>
        </div>
        <div id="io-card-2" class="card tint-blue io-card sync-card" style="padding:6px 9px; gap:2px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title" style="font-size:11.4px; color:#1A73E8;">2. Input Layer</div>
          <div style="font-size:10.3px; color:#3C4043; line-height:1.32;">Semua nilai piksel di-<em>flatten</em> jadi <strong>150.528 neuron</strong> — selalu jauh lebih banyak daripada <em>Output Layer</em>.</div>
        </div>
        <div id="io-card-3" class="card tint-green io-card sync-card" style="padding:6px 9px; gap:2px;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title" style="font-size:11.4px; color:#137333;">3. Output Layer</div>
          <div style="font-size:10.3px; color:#3C4043; line-height:1.32;">Selalu <strong>1 layer</strong>, jumlah <strong>neuron = jumlah kelas</strong> (5 neuron); tiap neuron input terhubung ke semua 5 output.</div>
        </div>
        <div id="io-card-4" class="card tint-yellow io-card sync-card" style="padding:6px 9px; gap:2px;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title" style="font-size:11.4px; color:#B06000;">4. Hasil Klasifikasi</div>
          <div style="font-size:10.3px; color:#3C4043; line-height:1.32;">Skor 5 neuron diubah jadi persentase (<code>Softmax</code>), lalu <strong>peluang tertinggi</strong> (<strong>Elsa 89%</strong>) dipilih!</div>
        </div>
      </div>

      <!-- KEY RULE CALLOUT (SCIENTIFICALLY PRECISE SUMMARY) -->
      <div class="callout" style="margin-top:6px; flex:0 0 auto; padding:5.5px 11px; font-size:11px; line-height:1.35;">
        <strong>Aturan Kunci (Neural Network · Klasifikasi Multi-Kelas):</strong> <strong>Ukuran piksel × channel</strong> (<code>H×W×C</code>) menentukan jumlah neuron di <strong>Input Layer</strong> &nbsp;·&nbsp; <strong>Jumlah kelas gambar</strong> menentukan jumlah neuron di <strong>Output Layer</strong> <span style="color:#5F6368;">(catatan: klasifikasi biner 2 kelas cukup 1 neuron Sigmoid).</span>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 24 (NEW): DENSE (FULLY CONNECTED) & CARA MENGHITUNG PARAMETER (W + b) — INTERACTIVE SIMULATOR -->
    <section class="slide" data-title="Bab 3B: Dense (Fully Connected) &amp; Parameter (W + b)" data-notes="Alokasi waktu: 1.5 menit. Simulator interaktif Lapisan Dense (Fully Connected) &amp; Rumus Parameter: klik Play atau +1 Langkah untuk melihat 1 neuron input (x1 -> x2 -> x3 -> semua) menyambungkan kabel bobot W ke seluruh 5 neuron output lalu ditambah 5 Bias (+b1..+b5). Peserta juga bisa mengklik langsung neuron x1..xn atau y1..y5, serta mengganti skala Mini 8x8 (965), Hands-On 64x64 (61.445), dan Penuh 224x224 (752.645).">
      <div class="kicker">BAB 03 · TAHAP 3.2 · DENSE LAYER &amp; PARAMETER</div>
      <h2>Lapisan <span class="hl-blue">Dense</span> (<em>Fully Connected</em>) &amp; Menghitung <span class="hl-red">Parameter</span></h2>

      <div style="display:grid; grid-template-columns:0.86fr 1.34fr; gap:12px; flex:1; min-height:0; align-items:stretch;">
        <!-- LEFT COLUMN: 3 SYNC-CARDS (choreographed live with simulator!) -->
        <div style="display:flex; flex-direction:column; justify-content:space-between; gap:8px; min-height:0;">
          <div id="dense-sc-1" class="card tint-blue sync-card" style="padding:10px 13px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-blue"></div>
            <div class="card-title" style="font-size:12.6px; color:#1A73E8;">1. Apa Itu Lapisan <code>Dense</code>?</div>
            <div style="font-size:11.1px; color:#3C4043; line-height:1.38;">
              Disebut juga <strong>Fully Connected Layer</strong>: <strong>setiap</strong> neuron di <em>Input Layer</em> dihubungkan dengan kabel bobot (<code>W</code>) ke <strong>semua</strong> 5 neuron di <em>Output Layer</em>. Di Keras cukup ditulis: <code>Dense(5, activation="softmax")</code>!
            </div>
          </div>

          <div id="dense-sc-2" class="card tint-yellow sync-card" style="padding:10px 13px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-yellow"></div>
            <div class="card-title" style="font-size:12.6px; color:#B06000;">2. Rumus Menghitung <em>Parameter</em></div>
            <div class="formula-box" style="padding:5px 9px; font-size:11px; margin:2px 0; background:#FFFFFF; border-color:#FDE293; color:#202124;">
              Total Parameter = (Input × Output) + Bias
            </div>
            <div style="font-size:11px; color:#3C4043; line-height:1.36;">
              Setiap <strong>1 kabel</strong> menyimpan <code>1 Weight (W)</code> dan setiap <strong>1 neuron output</strong> menyimpan <code>1 Bias (b)</code> — itulah angka yang nanti dipelajari komputer!
            </div>
          </div>

          <div id="dense-sc-3" class="card tint-green sync-card" style="padding:10px 13px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-green"></div>
            <div class="card-title" style="font-size:12.6px; color:#137333;">3. Kenapa Wajib Paham Angka Ini?</div>
            <div style="font-size:11px; color:#3C4043; line-height:1.36;">
              Saat Hands-On nanti, tabel <code>model.summary()</code> Keras akan memunculkan tepat <strong><code>61.445</code> parameter</strong> — sekarang kamu tahu 100% asal angkanya, bukan sulap!
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN: INTERACTIVE DENSE & PARAMETER SIMULATOR -->
        <div class="card" style="padding:9px 12px; gap:7px; justify-content:space-between; border:1.5px solid #C6DAFC; box-shadow:0 4px 14px rgba(66,133,244,0.06);">
          <!-- Control Toolbar (Play / +1 Langkah / Reset + 3 Scale Presets) -->
          <div style="display:flex; align-items:center; justify-content:space-between; gap:6px; flex-wrap:wrap;">
            <div id="dense-ctrl" class="sim-bar pdf-keep-ui" style="gap:5px;">
              <button type="button" id="dense-btn-play" class="btn-ui green" onclick="toggleDensePlay()" style="padding:3.5px 10px; font-size:10px;">▶ Play</button>
              <button type="button" class="btn-ui outline" onclick="stepDenseSim()" style="padding:3.5px 9px; font-size:10px;">⏭ +1 Langkah</button>
              <button type="button" class="btn-ui outline" onclick="resetDenseSim()" style="padding:3.5px 8px; font-size:10px;">↺ Reset</button>
            </div>
            <div id="dense-scale-tabs" class="pdf-keep-ui" style="display:flex; gap:4px;">
              <button type="button" class="btn-ui outline" data-ds="8" onclick="setDenseScale(8)" style="padding:3px 8px; font-size:9.6px;">Mini 8×8</button>
              <button type="button" class="btn-ui outline" data-ds="64" onclick="setDenseScale(64)" style="padding:3px 8px; font-size:9.6px;">Hands-On 64×64</button>
              <button type="button" class="btn-ui" data-ds="224" onclick="setDenseScale(224)" style="padding:3px 8px; font-size:9.6px;">Penuh 224×224</button>
            </div>
          </div>

          <!-- Interactive Stage SVG (fills container cleanly, clickable x1..xn & y1..y5!) -->
          <div style="flex:1; min-height:0; display:flex; flex-direction:column; justify-content:space-between; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:11px; padding:6px 8px; gap:4px;">
            <div style="display:flex; align-items:center; justify-content:space-between; font-size:9.5px; color:#5F6368; padding:0 2px;">
              <span id="dense-step-badge" style="font-family:var(--font-title); font-weight:700; color:#1A73E8; background:#E8F0FE; border-radius:999px; padding:1.5px 8px;">Tahap 5/5 · Penuh (W + b)</span>
              <span><strong>Interaktif:</strong> Klik <strong>▶ Play</strong>, <strong>⏭ +1 Langkah</strong>, atau klik langsung neuron <code>x₁..xₙ</code> / <code>y₁..y₅</code>!</span>
            </div>
            <svg id="dense-svg" viewBox="0 0 620 232" style="width:100%; flex:1; min-height:0; display:block;"></svg>
            <!-- Mini Keras model.summary() Live Readout Bar -->
            <div id="dense-keras-bar" style="display:flex; align-items:center; justify-content:space-between; gap:8px; background:#202124; color:#FFFFFF; border-radius:8px; padding:4.5px 10px; font-family:var(--font-code); font-size:9.6px;">
              <span style="color:#8AB4F8; font-weight:700;">Keras: Dense(5, activation="softmax")</span>
              <span id="dense-keras-eq" style="color:#FDD663; font-weight:700;">(150.528 × 5) + 5 = 752.645 Param #</span>
            </div>
          </div>

          <!-- 3 Clickable Scale Comparison Cards -->
          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;">
            <div id="dense-card-8" onclick="setDenseScale(8)" style="cursor:pointer; background:#F8F9FA; border:1.5px solid #DADCE0; border-radius:10px; padding:5.5px 8px; text-align:center;">
              <div style="font-family:var(--font-title); font-size:9.8px; font-weight:800; color:#137333;">Mini 8×8×3</div>
              <div style="font-family:var(--font-code); font-size:12px; font-weight:800; color:#202124;">965 param</div>
              <div style="font-size:9px; color:#5F6368;">192×5 + 5 (Tahap 2.1)</div>
            </div>
            <div id="dense-card-64" onclick="setDenseScale(64)" style="cursor:pointer; background:#F8F9FA; border:1.5px solid #DADCE0; border-radius:10px; padding:5.5px 8px; text-align:center;">
              <div style="font-family:var(--font-title); font-size:9.8px; font-weight:800; color:#1A73E8;">Hands-On 64×64×3</div>
              <div style="font-family:var(--font-code); font-size:12px; font-weight:800; color:#202124;">61.445 param</div>
              <div style="font-size:9px; color:#5F6368;">12.288×5 + 5 (Keras)</div>
            </div>
            <div id="dense-card-224" onclick="setDenseScale(224)" style="cursor:pointer; background:#FCE8E6; border:2px solid #EA4335; border-radius:10px; padding:5.5px 8px; text-align:center;">
              <div style="font-family:var(--font-title); font-size:9.8px; font-weight:800; color:#C5221F;">Penuh 224×224×3</div>
              <div style="font-family:var(--font-code); font-size:12px; font-weight:800; color:#202124;">752.645 param</div>
              <div style="font-size:9px; color:#5F6368;">150.528×5 + 5 (Slide 32)</div>
            </div>
          </div>

          <div id="dense-callout" class="callout" style="padding:5px 10px; font-size:10.4px; line-height:1.32;">
            <strong>Skala Penuh 224×224×3:</strong> <code>150.528 × 5 Weight + 5 Bias = 752.645 parameter</code> yang disetel otomatis saat training!
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 25: SIMULASI TRAINING (MATEMATIKA NYATA 5 FOTO FROZEN -> WEIGHTS+BIAS -> ACTIVATION -> OUTPUT) -->
    <section class="slide" data-title="Bab 3B: Simulasi Training — Bagaimana Neural Network Mengenali Gambar?" data-notes="Alokasi waktu: {"3.5" if HIDE_BAB4_ARCH else ("3" if HIDE_SLIDES_28_40 else "2")} menit. Jawab pertanyaan inti setelah Slide 24 (Dense &amp; Parameter): bagaimana Neural Network tahu secara matematis bahwa foto ini adalah Elsa? Tunjukkan 5 foto nyata berlabel (Anna, Elsa, Kristoff, Olaf, Sven) di kiri. Klik Sebelum Training (weight acak -> tebakan salah ~20%), lalu klik Play agar peserta melihat tiap gambar masuk ke Input Layer utuh 150.528 neuron piksel (224×224×3, tampil x1..x3, elipsis +150.522 piksel lain, x150.526..x150.528), dikalikan Weight (w) + Bias (b), diubah oleh Softmax (e^z / Σe^z), lalu Target vs Prediksi (Error) mendorong update Weight & Bias sehingga setiap foto mengaktifkan neuron kelasnya masing-masing di Output Layer!">
      <div class="kicker">BAB 03 · TAHAP 4 · SIMULASI TRAINING (ALUR UTUH)</div>
      <h2><span class="hl-green">Simulasi Training</span>: Bagaimana Neural Network Mengenali <span class="hl-blue">Gambar</span>?</h2>

      <!-- Compact Control Bar -->
      <div class="sim-bar pdf-keep-ui" id="tm-ctrl" style="margin-bottom:6px; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:11px; padding:4px 9px; gap:6px;">
        <div style="display:flex; align-items:center; gap:5px;">
          <button class="btn-ui" id="tm-btn-train" onclick="playTmSim()" style="padding:3.5px 9px; font-size:10.3px; background:#34A853; border-color:#34A853;">▶ Play</button>
          <button class="btn-ui outline" id="tm-btn-step" onclick="stepTmPhase()" style="padding:3.5px 8px; font-size:10.2px; color:#137333; border-color:#A8DAB5;">⏭ +1 Tahap Hitung</button>
          <button class="btn-ui outline" id="tm-btn-reset" onclick="resetTmSim()" style="padding:3.5px 8px; font-size:10.2px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
          <span style="width:1px; height:16px; background:#DADCE0; margin:0 2px;"></span>
          <button class="btn-ui outline" data-tm="before" onclick="setTmMode('before')" style="padding:3.5px 8px; font-size:10.1px;">Sebelum Training (Acak)</button>
          <button class="btn-ui outline" data-tm="after" onclick="setTmMode('after')" style="padding:3.5px 8px; font-size:10.1px;">Sesudah Training (Terlatih)</button>
        </div>
        <span class="pill blue" id="tm-status-pill" style="font-size:10.0px; padding:3px 10px;">Siap · Pilih Foto / ▶ Play</span>
      </div>

      <!-- HERO INTERACTIVE STAGE: 5 LABELED FROZEN PHOTOS -> INPUT x WEIGHT + BIAS -> ACTIVATION (SOFTMAX) -> OUTPUT -->
      <div id="tm-stage-wrap" style="position:relative; flex:1; min-height:0; display:grid; grid-template-columns:190px 20px 1fr; gap:5px; align-items:stretch; background:#FFFFFF; border:1.5px solid #C6DAFC; border-radius:15px; padding:7px 10px; margin-bottom:6px; box-shadow:0 4px 14px rgba(66,133,244,0.06);">
        <canvas id="tm-motion-canvas" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:25;"></canvas>

        <!-- LEFT: LABELED DATASET (5 REAL FROZEN PHOTOS) -->
        <div style="display:flex; flex-direction:column; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:11px; padding:6px 7px;">
          <div style="text-align:center; margin-bottom:2px;">
            <div style="font-family:var(--font-title); font-size:10.8px; font-weight:700; color:#202124;">1. Dataset Berlabel (5 Kelas)</div>
            <div style="font-size:8.8px; color:#5F6368;">Klik foto untuk lihat hitungannya!</div>
          </div>
          <div id="tm-dataset-list" style="display:flex; flex-direction:column; gap:4px; flex:1; justify-content:space-between;"></div>
        </div>

        <!-- ARROW: Dataset -> Input Layer -->
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
          <svg viewBox="0 0 20 18" style="width:18px; height:16px;">
            <line x1="1" y1="9" x2="11" y2="9" stroke="#4285F4" stroke-width="2.6" stroke-linecap="round"/>
            <polygon points="9,4 19,9 9,14" fill="#4285F4"/>
          </svg>
        </div>

        <!-- RIGHT: FULL-WIDTH INTERACTIVE MATH NETWORK SVG + 2-STAGE LIVE CALCULATION (WEIGHT+BIAS -> ACTIVATION FUNCTION) -->
        <div style="display:flex; flex-direction:column; justify-content:space-between; gap:5px; min-height:0;">
          <div style="flex:1; min-height:0; display:flex; align-items:center; justify-content:center;">
            <svg id="tm-svg" viewBox="0 0 820 248" style="width:100%; height:100%; max-height:248px; display:block;"></svg>
          </div>
          <!-- 2-STAGE TRANSPARENT MATHEMATICAL PROCESS: (A) WEIGHT + BIAS -> (B) ACTIVATION FUNCTION (SOFTMAX) -->
          <div style="display:grid; grid-template-columns:1.36fr 16px 1.04fr; gap:5px; align-items:stretch;">
            <div id="tm-math-wb" class="tm-math-card" style="background:#FEF7E0; border:1.5px solid #FDE293; display:flex; flex-direction:column; justify-content:center; gap:2px;">
              <div style="font-family:var(--font-title); font-size:9.6px; font-weight:700; color:#B06000;">Tahap 4.1 · Weight + Bias &nbsp;<code>z = Σ(x·w) + b</code></div>
              <div id="tm-math-wb-eq" style="font-family:var(--font-code); font-size:9.2px; color:#202124; line-height:1.32;"></div>
            </div>
            <div style="display:flex; align-items:center; justify-content:center; font-size:15px; font-weight:800; color:#137333;">→</div>
            <div id="tm-math-act" class="tm-math-card" style="background:#E6F4EA; border:1.5px solid #A8DAB5; display:flex; flex-direction:column; justify-content:center; gap:2px;">
              <div style="font-family:var(--font-title); font-size:9.6px; font-weight:700; color:#137333;">Tahap 4.2 · Activation (<code>Softmax</code>)</div>
              <div id="tm-math-act-eq" style="font-family:var(--font-code); font-size:9.2px; color:#202124; line-height:1.32;"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 3 COMPACT STEP EXPLANATION CARDS (synced live with animation phases!) -->
      <div class="grid-3" style="flex:0 0 auto; gap:8px;">
        <div id="tm-card-1" class="card surface sync-card" style="padding:5.5px 9px; gap:2px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title" style="font-size:11.4px; color:#1A73E8;">1. Data Berlabel Masuk</div>
          <div style="font-size:10.1px; color:#3C4043; line-height:1.3;">Foto dari 5 kelas + <strong>Label</strong> masuk ke <em>Input Layer</em> membawa nilai piksel nyatanya.</div>
        </div>
        <div id="tm-card-2" class="card tint-yellow sync-card" style="padding:5.5px 9px; gap:2px;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title" style="font-size:11.4px; color:#B06000;">2. Weight + Bias → Skor <code>z</code> <span style="font-weight:600; opacity:0.85;">(4.1)</span></div>
          <div style="font-size:10.1px; color:#3C4043; line-height:1.3;">Input dikali <strong>Weight (<code>w</code>)</strong> lalu ditambah <strong>Bias (<code>b</code>)</strong> menghasilkan skor mentah <code>z</code> tiap kelas.</div>
        </div>
        <div id="tm-card-3" class="card tint-green sync-card" style="padding:5.5px 9px; gap:2px;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title" style="font-size:11.4px; color:#137333;">3. Activation → Output Akhir <span style="font-weight:600; opacity:0.85;">(4.2–4.3)</span></div>
          <div style="font-size:10.1px; color:#3C4043; line-height:1.3;"><strong>Softmax</strong> mengubah <code>z</code> jadi probabilitas <code>0–100%</code>; <em>training</em> menguatkan <code>w</code> &amp; <code>b</code> ke kelas benar!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 25: WEIGHT & BIAS — APA ITU, KENAPA PERLU, CARA KERJA, & SIMULASI DATASET FROZEN -->
    <section class="slide" data-title="Bab 3B: Weight &amp; Bias — Menimbang Fitur Gambar" data-notes="Alokasi waktu: {"2.5" if HIDE_BAB4_ARCH else ("2.5" if HIDE_SLIDES_28_40 else "2")} menit. Bedah khusus komponen pertama dari Slide 25: Weight (w) dan Bias (b). Jelaskan secara runtut dari kiri: (1) Apa itu Weight (bobot kepentingan tiap fitur piksel) dan Bias (ambang awal penggeser); (2) Kenapa keduanya wajib ada; (3) Cara kerjanya z = Σ(x·w) + b. Lalu demokan simulator kanan pada 5 foto nyata Frozen: klik 1. Bobot Ideal Elsa -> 2. Tanpa Bias (b=0) untuk membuktikan semua 5 karakter ikut aktif positif tanpa ambang -> 3. Weight Biru Dibalik untuk membuktikan weight mengendalikan ciri apa yang dicari neuron!">
      <div class="kicker">BAB 03 · TAHAP 4.1 · WEIGHT &amp; BIAS</div>
      <h2><span class="hl-blue">Weight</span> &amp; <span class="hl-yellow">Bias</span>: Bagaimana Neural Network Menimbang Fitur Gambar</h2>

      <div style="display:grid; grid-template-columns:0.88fr 1.32fr; gap:12px; flex:1; min-height:0; align-items:stretch;">
        <!-- LEFT COLUMN: APA ITU, KENAPA PERLU, CARA KERJA -->
        <div style="display:flex; flex-direction:column; justify-content:space-between; gap:8px; min-height:0;">
          <div id="wb-card-1" class="card tint-blue sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-blue"></div>
            <div class="card-title" style="font-size:12.6px; color:#1A73E8;">1. Apa Itu Weight (<code>w</code>) &amp; Bias (<code>b</code>)?</div>
            <div style="font-size:11.1px; color:#3C4043; line-height:1.38;">
              <div style="margin-bottom:3px;"><strong>Weight (<code>w</code>):</strong> angka <strong>bobot pengali</strong> di tiap kabel fitur — <code>w &gt; 0</code> mendukung kelas, <code>w &lt; 0</code> menekan, <code>w ≈ 0</code> mengabaikan.</div>
              <div><strong>Bias (<code>b</code>):</strong> angka <strong>penggeser ambang awal</strong> (<em>offset</em>) — mengatur seberapa mudah atau ketat neuron kelas menyala.</div>
            </div>
          </div>

          <div id="wb-card-2" class="card tint-yellow sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-yellow"></div>
            <div class="card-title" style="font-size:12.6px; color:#B06000;">2. Kenapa Keduanya Diperlukan?</div>
            <div style="font-size:11.1px; color:#3C4043; line-height:1.38;">
              <div style="margin-bottom:3px;"><strong>Tanpa Weight:</strong> semua piksel dianggap sama pentingnya — model gagal membedakan biru gaun Elsa dari latar polos.</div>
              <div><strong>Tanpa Bias:</strong> skor terkunci di <code>0</code> saat input <code>0</code> — tidak punya garis ambang sehingga kelas lain mudah ikut aktif!</div>
            </div>
          </div>

          <div id="wb-card-3" class="card tint-green sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-green"></div>
            <div class="card-title" style="font-size:12.6px; color:#137333;">3. Bagaimana Cara Kerjanya?</div>
            <div class="formula-box" style="padding:4px 8px; font-size:10.3px; margin:2px 0; background:#FFFFFF; border-color:#A8DAB5;">z = (x₁·w₁ + x₂·w₂ + ... + x₁₅₀.₅₂₈·w₁₅₀.₅₂₈) + b</div>
            <div style="font-size:10.9px; color:#3C4043; line-height:1.36;">Saat <em>training</em>, tiap karakter punya kombinasi <code>w</code> &amp; <code>b</code> sendiri agar skor <code>z</code> foto target jadi <strong>positif paling tinggi</strong> dibanding 4 karakter lainnya.</div>
          </div>
        </div>

        <!-- RIGHT COLUMN: SEAMLESS ZOOM-IN OF SLIDE 24 TAHAP A (WEIGHT + BIAS -> z) PER CHARACTER -->
        <div class="card" style="padding:8px 11px; gap:5.5px; justify-content:space-between; border:1.5px solid #C6DAFC; box-shadow:0 4px 14px rgba(66,133,244,0.06);">
          <!-- CONTINUITY MINI-MAP: EXPLICITLY SHOWS WHERE THIS HAPPENS IN SLIDE 24! -->
          <div style="display:flex; align-items:center; justify-content:space-between; gap:4px; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:8px; padding:3.5px 8px; font-size:9.1px; color:#5F6368;">
            <strong style="color:#202124; white-space:nowrap;">📍 Posisi di Tahap 4:</strong>
            <div style="display:flex; align-items:center; gap:3.5px; flex-wrap:nowrap;">
              <span style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:5px; padding:1px 5px;">Input 150.528</span>
              <span>→</span>
              <span style="background:#FEF7E0; border:1.5px solid #FBBC04; color:#B06000; font-weight:700; border-radius:5px; padding:1px 6px;">🔍 Tahap 4.1: Weight + Bias → z</span>
              <span>→</span>
              <span style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:5px; padding:1px 5px;">Tahap 4.2: Activation</span>
            </div>
          </div>

          <!-- Interactive Control Bar + Experiment Presets (100% synced with Slide 24 numbers!) -->
          <div class="sim-bar pdf-keep-ui" id="wb-presets" style="gap:4px; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:4px;">
              <button class="btn-ui" id="wb-btn-tour" onclick="playWbTour()" style="padding:3px 8px; font-size:9.6px; background:#34A853; border-color:#34A853;">▶ Play</button>
              <button class="btn-ui outline" id="wb-btn-next" onclick="nextWbChar()" style="padding:3px 7px; font-size:9.5px; color:#137333; border-color:#A8DAB5;">⏭ Berikutnya</button>
              <button class="btn-ui outline" onclick="setWbPreset('elsa_opt')" style="padding:3px 7.5px; font-size:9.5px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
            </div>
            <div style="display:flex; align-items:center; gap:4px;">
              <button class="btn-ui outline" data-wb="no_bias" onclick="setWbPreset('no_bias')" style="padding:3px 7.5px; font-size:9.5px;">Coba Bias = 0</button>
              <button class="btn-ui outline" data-wb="wrong_w" onclick="setWbPreset('wrong_w')" style="padding:3px 7.5px; font-size:9.5px;">Coba Balik Weight</button>
            </div>
          </div>

          <!-- 5 Clickable Real Frozen Character Chips (exact same photos & z scores as Slide 24!) -->
          <div id="wb-ds-chips" class="ds-chip-row"></div>

          <!-- LIVE ZOOM-IN NEURON DIAGRAM SVG: SHOWS EXACT CABLES FROM SLIDE 24 ENTERING 1 OUTPUT NEURON! -->
          <div style="flex:1; min-height:0; display:flex; align-items:center; justify-content:center; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:10px; padding:4px 6px;">
            <svg id="wb-zoom-svg" viewBox="0 0 600 218" style="width:100%; height:100%; max-height:218px; display:block;"></svg>
          </div>

          <!-- 2 FOCUSED LIVE EXPERIMENT SLIDERS (Hero 150.523-Pixel Weight Scale + Bias) -->
          <div style="display:grid; grid-template-columns:1.12fr 0.88fr; gap:8px; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:9px; padding:5px 9px;">
            <div class="wb-srow" style="grid-template-columns:132px 1fr 46px; font-size:9.5px;">
              <strong id="wb-hero-lbl" style="color:#137333;">Weight 150.522 Piksel</strong>
              <input id="wb-hero-w" type="range" min="-1.5" max="1.5" step="0.05" value="1.0" oninput="onWbSliderInput()"/>
              <span class="sim-val" id="wb-hero-vw" style="font-size:9.6px; color:#137333;">+1.00×</span>
            </div>
            <div class="wb-srow bias-row" style="grid-template-columns:72px 1fr 44px; font-size:9.5px; border-left:1px solid #DADCE0; padding-left:8px;">
              <strong id="wb-bias-lbl" style="color:#B06000;">b₂ · Bias</strong>
              <input id="wb-b" type="range" min="-4.0" max="4.0" step="0.01" value="-1.04" oninput="onWbSliderInput()"/>
              <span class="sim-val" id="wb-vb" style="font-size:9.6px; color:#B06000;">-1.04</span>
            </div>
          </div>

          <!-- Live Explanation Tying Back to Slide 24 -->
          <div class="callout green" id="wb-insight" style="padding:4.5px 9px; font-size:10.1px; line-height:1.32;"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 26: ACTIVATION FUNCTION — APA ITU, KENAPA PERLU, CARA KERJA, & SIMULASI DATASET FROZEN -->
    <section class="slide" data-title="Bab 3B: Activation Function — Non-Linearity &amp; Probabilitas" data-notes="Alokasi waktu: {"3" if HIDE_BAB4_ARCH else ("2.5" if HIDE_SLIDES_28_40 else "2")} menit. Bedah khusus komponen kedua dari Slide 25: Activation Function. Jelaskan kiri ke kanan: (1) Apa itu (fungsi penyaring/pengubah skor mentah z); (2) Kenapa wajib ada (tanpa non-linearity, 100 layer tetap cuma 1 garis lurus yang gagal mengenali bentuk kompleks; sekaligus mengubah skor bebas menjadi rentang bermakna); (3) fungsi utama: ReLU di lapisan fitur, Sigmoid/Tanh untuk biner/terpusat-0, Softmax untuk multi-kelas. Lalu demokan simulator kanan pada 5 foto nyata Frozen across ReLU, Sigmoid, dan Softmax!">
      <div class="kicker">BAB 03 · TAHAP 4.2 · ACTIVATION FUNCTION</div>
      <h2><span class="hl-red">Activation Function</span>: Dari Skor Mentah Menjadi Aktivasi &amp; Peluang</h2>

      <div style="display:grid; grid-template-columns:0.88fr 1.32fr; gap:12px; flex:1; min-height:0; align-items:stretch;">
        <!-- LEFT COLUMN: APA ITU, KENAPA PERLU, CARA KERJA -->
        <div style="display:flex; flex-direction:column; justify-content:space-between; gap:8px; min-height:0;">
          <div id="act-card-1" class="card tint-red sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-red"></div>
            <div class="card-title" style="font-size:12.6px; color:#C5221F;">1. Apa Itu Activation Function?</div>
            <div style="font-size:11.1px; color:#3C4043; line-height:1.38;">Fungsi matematika di ujung neuron yang mengubah <strong>skor mentah <code>z</code></strong> (bisa minus atau plus bebas) menjadi <strong>sinyal keluaran aktif</strong> yang berguna bagi lapisan berikutnya atau prediksi akhir.</div>
          </div>

          <div id="act-card-2" class="card tint-blue sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-blue"></div>
            <div class="card-title" style="font-size:12.6px; color:#1A73E8;">2. Kenapa Wajib Ada?</div>
            <div style="font-size:11.1px; color:#3C4043; line-height:1.38;">
              <div style="margin-bottom:3px;"><strong>Memecah garis lurus (<em>Non-Linearity</em>):</strong> Tanpa aktivasi, menumpuk banyak lapisan neuron tetap setara 1 garis lurus — mustahil mengenali lekuk wajah, rambut, atau gaun!</div>
              <div><strong>Menstandarkan output:</strong> Mengubah skor bebas (mis. <code>-0.90, +2.13</code>) menjadi rentang jelas (<code>≥ 0</code> atau <code>0–100%</code>).</div>
            </div>
          </div>

          <div id="act-card-3" class="card tint-green sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-green"></div>
            <div class="card-title" style="font-size:12.6px; color:#137333;">3. Fungsi Aktivasi Utama</div>
            <div style="font-size:10.6px; color:#3C4043; line-height:1.34; display:flex; flex-direction:column; gap:2.5px;">
              <div id="act-b-relu" class="sync-bullet">• <strong><code>ReLU</code></strong> <em>(Lapisan Fitur)</em>: <code>max(0, z)</code> → negatif jadi <code>0</code>, positif lolos.</div>
              <div id="act-b-sigmoid" class="sync-bullet">• <strong><code>Sigmoid</code></strong> <em>(Output 2 Kelas)</em>: memeras <code>z</code> ke <code>0–100%</code> (<em>sepupunya</em> <code>Tanh</code>: <code>−1 s/d +1</code>).</div>
              <div id="act-b-softmax" class="sync-bullet">• <strong><code>Softmax</code></strong> <em>(Output Multi-Kelas)</em>: 5 skor kelas → total tepat <code>100%</code>!</div>
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN: SEAMLESS ZOOM-IN OF SLIDE 24 TAHAP B (ACTIVATION FUNCTION) PER CHARACTER -->
        <div class="card" style="padding:8px 11px; gap:5.5px; justify-content:space-between; border:1.5px solid #A8DAB5; box-shadow:0 4px 14px rgba(52,168,83,0.06);">
          <!-- CONTINUITY MINI-MAP: EXPLICITLY SHOWS WHERE THIS HAPPENS IN SLIDE 24! -->
          <div style="display:flex; align-items:center; justify-content:space-between; gap:4px; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:8px; padding:3.5px 8px; font-size:9.1px; color:#5F6368;">
            <strong style="color:#202124; white-space:nowrap;">📍 Posisi di Tahap 4:</strong>
            <div style="display:flex; align-items:center; gap:3.5px; flex-wrap:nowrap;">
              <span style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:5px; padding:1px 5px;">Tahap 4.1: Weight + Bias → z</span>
              <span>→</span>
              <span style="background:#E6F4EA; border:1.5px solid #34A853; color:#137333; font-weight:700; border-radius:5px; padding:1px 6px;">🔍 Tahap 4.2: Activation Function</span>
              <span>→</span>
              <span style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:5px; padding:1px 5px;">Tahap 4.3: Output Akhir</span>
            </div>
          </div>

          <!-- Interactive Auto-Tour + 3 Activation Function Tabs (registered in PDF/PPTX expanders!) -->
          <div class="sim-bar pdf-keep-ui" id="act-tabs" style="gap:4px; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:4px;">
              <button class="btn-ui" id="act-btn-tour" onclick="playActTour()" style="padding:3px 8px; font-size:9.6px; background:#34A853; border-color:#34A853;">▶ Play</button>
              <button class="btn-ui outline" id="act-btn-next" onclick="nextActChar()" style="padding:3px 7px; font-size:9.5px; color:#137333; border-color:#A8DAB5;">⏭ Berikutnya</button>
              <button class="btn-ui outline" onclick="resetActZ()" style="padding:3px 7px; font-size:9.5px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
            </div>
            <div style="display:flex; align-items:center; gap:4px;">
              <button class="btn-ui" data-act="relu" onclick="setActTab('relu')" style="padding:3px 7.5px; font-size:9.5px;">1. ReLU</button>
              <button class="btn-ui outline" data-act="sigmoid" onclick="setActTab('sigmoid')" style="padding:3px 7.5px; font-size:9.5px;">2. Sigmoid</button>
              <button class="btn-ui outline" data-act="softmax" onclick="setActTab('softmax')" style="padding:3px 7.5px; font-size:9.5px;">3. Softmax</button>
            </div>
          </div>

          <!-- 5 Clickable Real Frozen Character Chips (exact Slide 24/25 z -> Output!) -->
          <div id="act-ds-chips" class="ds-chip-row"></div>

          <!-- LIVE ZOOM-IN ACTIVATION MACHINE SVG: TAHAP A (z) -> ACTIVATION MACHINE (ReLU/Sigmoid/Softmax) -> OUTPUT! -->
          <div style="flex:1; min-height:0; display:flex; align-items:center; justify-content:center; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:10px; padding:4px 6px;">
            <svg id="act-zoom-svg" viewBox="0 0 600 218" style="width:100%; height:100%; max-height:218px; display:block;"></svg>
          </div>

          <!-- Compact Interactive Slider to Test Target Score z Live Across ALL 3 Activation Functions! -->
          <div style="display:flex; align-items:center; gap:8px; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:9px; padding:4.5px 9px;">
            <strong id="act-z-lbl" style="color:#B06000; font-size:9.6px; white-space:nowrap;">Geser z₂ (Elsa):</strong>
            <input id="act-z-slider" type="range" min="-4.0" max="4.0" step="0.1" value="2.1" oninput="onActSlider()" style="flex:1; accent-color:#34A853; cursor:pointer; margin:0;"/>
            <span class="sim-val" id="act-z-readout" style="font-size:9.7px; color:#137333; min-width:96px;">z=+2.13 → 2.13</span>
          </div>

          <!-- Bottom Concrete Dataset Takeaway -->
          <div class="callout green" id="act-callout" style="padding:4.5px 9px; font-size:10.1px; line-height:1.32;"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 27: OUTPUT AKHIR — ZOOM-IN TAHAP C (ARGMAX, CONFIDENCE, & EVALUASI ERROR) -->
    <section class="slide" data-title="Bab 3B: Output Akhir — Keputusan Argmax, Confidence &amp; Evaluasi" data-notes="Alokasi waktu: {"2.5" if HIDE_BAB4_ARCH else ("2.5" if HIDE_SLIDES_28_40 else "1.5")} menit. Melengkapi trilogi Zoom-In dari Slide 25 (Tahap 4.1 Slide 26 -> Tahap 4.2 Slide 27 -> Output Akhir Slide 28). Tunjukkan bagaimana 5 probabilitas Softmax diubah menjadi 1 keputusan lewat Argmax, bedakan Confidence Yakin vs Ragu memakai ambang 60%, lalu klik Acak (Belum Latih) agar peserta melihat tebakan salah menghasilkan Error/Loss besar sebagai bahan belajar Training!">
      <div class="kicker">BAB 03 · TAHAP 4.3 · OUTPUT AKHIR &amp; ERROR</div>
      <h2><span class="hl-green">Output Akhir</span>: Keputusan <span class="hl-blue">Argmax</span>, <em>Confidence</em> &amp; Cek <em>Error</em></h2>

      <div style="display:grid; grid-template-columns:0.88fr 1.32fr; gap:12px; flex:1; min-height:0; align-items:stretch;">
        <!-- LEFT COLUMN: APA ITU, KENAPA PERLU, CARA KERJA -->
        <div style="display:flex; flex-direction:column; justify-content:space-between; gap:8px; min-height:0;">
          <div id="out-card-1" class="card tint-green sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-green"></div>
            <div class="card-title" style="font-size:12.6px; color:#137333;">1. Apa Itu Output Akhir (<code>Argmax</code>)?</div>
            <div style="font-size:11.1px; color:#3C4043; line-height:1.38;">Setelah <strong>Softmax</strong> (Tahap 4.2) mengeluarkan 5 peluang, fungsi <strong><code>Argmax</code></strong> memilih <strong>1 kelas dengan peluang tertinggi</strong> sebagai prediksi akhir model.</div>
          </div>

          <div id="out-card-2" class="card tint-blue sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-blue"></div>
            <div class="card-title" style="font-size:12.6px; color:#1A73E8;">2. Kenapa Cek <em>Confidence</em>?</div>
            <div style="font-size:11.1px; color:#3C4043; line-height:1.38;">
              <div style="margin-bottom:3px;"><strong>Yakin vs Ragu:</strong> Menang dengan <code>77.7%</code> (Elsa) jauh lebih aman daripada menang tipis <code>41.9%</code>!</div>
              <div>Di aplikasi nyata, kita pasang <strong>Ambang Yakin (<em>Threshold</em>)</strong> — jika di bawah ambang, sistem memberi tanda <em>perlu cek manusia</em>.</div>
            </div>
          </div>

          <div id="out-card-3" class="card tint-red sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-red"></div>
            <div class="card-title" style="font-size:12.6px; color:#C5221F;">3. Evaluasi ke <em>Error / Loss</em></div>
            <div class="formula-box" style="padding:4px 8px; font-size:10.8px; margin:2px 0; background:#FFFFFF; border-color:#F6AEA9;">Error = 100% − P(Kelas Asli)  |  Loss = −ln(P)</div>
            <div style="font-size:10.9px; color:#3C4043; line-height:1.36;">Saat <em>training</em>, selisih antara prediksi dan <strong>Label Asli (100%)</strong> dikirim balik untuk memperbaiki <code>Weight</code> &amp; <code>Bias</code>!</div>
          </div>
        </div>

        <!-- RIGHT COLUMN: SEAMLESS ZOOM-IN OF SLIDE 24 TAHAP C (OUTPUT AKHIR -> ARGMAX -> EVALUASI) -->
        <div class="card" style="padding:8px 11px; gap:5.5px; justify-content:space-between; border:1.5px solid #A8DAB5; box-shadow:0 4px 14px rgba(52,168,83,0.06);">
          <!-- CONTINUITY MINI-MAP: COMPLETING THE SLIDE 24 -> 25 -> 26 -> 27 TRILOGY! -->
          <div style="display:flex; align-items:center; justify-content:space-between; gap:4px; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:8px; padding:3.5px 8px; font-size:9.1px; color:#5F6368;">
            <strong style="color:#202124; white-space:nowrap;">📍 Posisi di Tahap 4:</strong>
            <div style="display:flex; align-items:center; gap:3.5px; flex-wrap:nowrap;">
              <span style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:5px; padding:1px 5px;">Tahap 4.1</span>
              <span>→</span>
              <span style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:5px; padding:1px 5px;">Tahap 4.2</span>
              <span>→</span>
              <span style="background:#E6F4EA; border:1.5px solid #34A853; color:#137333; font-weight:700; border-radius:5px; padding:1px 6px;">🔍 Tahap 4.3: Output Akhir &amp; Error</span>
              <span>→</span>
              <span style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:5px; padding:1px 5px;">Tahap 5</span>
            </div>
          </div>

          <!-- Consistent Control Bar (Play/Stop, Berikutnya, Reset + 3 Evaluation Modes) -->
          <div class="sim-bar pdf-keep-ui" id="out-presets" style="gap:4px; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:4px;">
              <button class="btn-ui" id="out-btn-tour" onclick="playOutTour()" style="padding:3px 8px; font-size:9.6px; background:#34A853; border-color:#34A853;">▶ Play</button>
              <button class="btn-ui outline" id="out-btn-next" onclick="nextOutChar()" style="padding:3px 7px; font-size:9.5px; color:#137333; border-color:#A8DAB5;">⏭ Berikutnya</button>
              <button class="btn-ui outline" onclick="resetOutSim()" style="padding:3px 7px; font-size:9.5px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
            </div>
            <div style="display:flex; align-items:center; gap:4px;">
              <button class="btn-ui" data-out="trained" onclick="setOutMode('trained')" style="padding:3px 7.5px; font-size:9.5px;">1. Terlatih</button>
              <button class="btn-ui outline" data-out="ragu" onclick="setOutMode('ragu')" style="padding:3px 7.5px; font-size:9.5px;">2. Ragu (Tipis)</button>
              <button class="btn-ui outline" data-out="untrained" onclick="setOutMode('untrained')" style="padding:3px 7.5px; font-size:9.5px;">3. Acak (Belum Latih)</button>
            </div>
          </div>

          <!-- 5 Clickable Real Frozen Character Chips (exact Slide 24/25/26 probs -> Decision!) -->
          <div id="out-ds-chips" class="ds-chip-row"></div>

          <!-- LIVE ZOOM-IN OUTPUT DECISION SVG: PROBABILITAS SLIDE 26 -> ARGMAX & CONFIDENCE -> EVALUASI LABEL ASLI! -->
          <div style="flex:1; min-height:0; display:flex; align-items:center; justify-content:center; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:10px; padding:4px 6px;">
            <svg id="out-zoom-svg" viewBox="0 0 600 218" style="width:100%; height:100%; max-height:218px; display:block;"></svg>
          </div>

          <!-- Interactive Confidence Threshold Slider + Reset -->
          <div style="display:flex; align-items:center; gap:8px; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:9px; padding:4.5px 9px;">
            <strong style="color:#1A73E8; font-size:9.6px; white-space:nowrap;">Ambang Yakin (<em>Threshold</em>):</strong>
            <input id="out-thresh-slider" type="range" min="40" max="90" step="5" value="60" oninput="onOutThreshInput()" style="flex:1; accent-color:#1A73E8; cursor:pointer; margin:0;"/>
            <span class="sim-val" id="out-thresh-readout" style="font-size:9.7px; color:#1A73E8; min-width:54px;">≥ 60%</span>
          </div>

          <!-- Bottom Concrete Evaluation Takeaway -->
          <div class="callout green" id="out-callout" style="padding:4.5px 9px; font-size:10.1px; line-height:1.32;"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    if HIDE_SLIDES_28_40:
        s.append(
            f"""
    <!-- 28: SIKLUS BELAJAR UTUH (FORWARD PASS -> LOSS -> BACKPROP & GRADIENT DESCENT -> EPOCH) -->
    <section class="slide" data-title="Bab 3C: Siklus Belajar Utuh — Forward Pass, Loss, Backprop, Gradient Descent &amp; Epoch" data-notes="Alokasi waktu: 2 menit. Menyambung langsung dari nilai Error dan Loss pada Slide 28 (foto Olaf belum latih: P=11.3%, Loss=2.18). Tunjukkan 4 tahap belajar berulang yang bekerja otomatis saat memanggil model.fit() di Keras: (1) Forward Pass (aliran maju Slide 25-28), (2) Hitung Loss (ukur kesalahan), (3) Backpropagation & Gradient Descent (lacak mundur bobot penyebab salah lalu geser sebesar Learning Rate), dan (4) Ulangi tiap Epoch hingga Loss turun dari 2.18 menjadi 0.23 dan Olaf dikenali 79.2%!">
      <div class="kicker">BAB 03 · TAHAP 5.1 · SIKLUS BELAJAR UTUH (EPOCH)</div>
      <h2><span class="hl-green">Siklus Belajar Utuh</span>: Dari <span class="hl-red">Loss</span> ke Koreksi Bobot (<span class="hl-blue">Epoch</span>)</h2>

      <div style="display:grid; grid-template-columns:0.86fr 1.34fr; gap:12px; flex:1; min-height:0; align-items:stretch;">
        <!-- LEFT COLUMN: 3 KARTU KONSEP INTI MENYAMBUNG SLIDE 27 -> HANDS-ON -->
        <div style="display:flex; flex-direction:column; justify-content:space-between; gap:8px; min-height:0;">
          <div id="tr-card-1" class="card tint-blue sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-blue"></div>
            <div class="card-title" style="font-size:12.4px; color:#1A73E8;">1. Forward Pass &amp; Loss</div>
            <div style="font-size:11.0px; color:#3C4043; line-height:1.38;"><strong>Forward Pass</strong> adalah aliran hitung maju (Tahap 4.1–4.3): <code>Foto → W+b → Softmax → Prediksi</code>. Lalu <strong>Loss</strong> mengukur seberapa jauh tebakan dari label asli.</div>
          </div>

          <div id="tr-card-2" class="card tint-yellow sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-yellow"></div>
            <div class="card-title" style="font-size:12.4px; color:#B06000;">2. Backpropagation &amp; Gradient Descent</div>
            <div style="font-size:11.0px; color:#3C4043; line-height:1.38;">
              <div style="margin-bottom:3px;"><strong>Backpropagation:</strong> melacak mundur dari ujung <em>Loss</em> ke kabel <code>w</code> &amp; <code>b</code> penyebab kesalahan.</div>
              <div><strong>Gradient Descent:</strong> menggeser bobot sedikit demi sedikit (sebesar <em>Learning Rate</em>) ke arah yang menurunkan <em>Loss</em>.</div>
            </div>
          </div>

          <div id="tr-card-3" class="card tint-green sync-card" style="padding:9px 12px; gap:4px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-green"></div>
            <div class="card-title" style="font-size:12.4px; color:#137333;">3. Ulangi Tiap Epoch (<code>model.fit()</code>)</div>
            <div style="font-size:11.0px; color:#3C4043; line-height:1.38;">1 putaran penuh membaca seluruh foto Frozen = <strong>1 Epoch</strong>. Saat diulang beberapa <em>epoch</em> di Keras, <strong>Loss turun</strong> otomatis tanpa hitung kalkulus manual!</div>
          </div>
        </div>

        <!-- RIGHT COLUMN: INTERACTIVE 4-STAGE TRAINING CYCLE CONNECTED TO SLIDE 27 OLAF NUMBERS! -->
        <div class="card" style="padding:8px 11px; gap:5.5px; justify-content:space-between; border:1.5px solid #A8DAB5; box-shadow:0 4px 14px rgba(52,168,83,0.06);">
          <!-- CONTINUITY STRIP FROM SLIDE 27 -->
          <div style="display:flex; align-items:center; justify-content:space-between; gap:4px; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:8px; padding:3.5px 8px; font-size:9.1px; color:#5F6368;">
            <strong style="color:#202124; white-space:nowrap;">📍 Sambungan Tahap 4.3:</strong>
            <div style="display:flex; align-items:center; gap:3.5px; flex-wrap:nowrap;">
              <span style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:5px; padding:1px 5px;">Tahap 4.3: Output &amp; Error</span>
              <span>→</span>
              <span style="background:#E6F4EA; border:1.5px solid #34A853; color:#137333; font-weight:700; border-radius:5px; padding:1px 6px;">🔍 Tahap 5: Siklus Belajar → Loss Turun</span>
            </div>
          </div>

          <!-- UNIFORM CONTROL BAR (Play/Stop, +1 Tahap, Reset + 4 Cycle Tabs) -->
          <div class="sim-bar pdf-keep-ui" id="tr-cycle-tabs" style="gap:4px; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:4px;">
              <button class="btn-ui" id="tr-btn-play" onclick="playTrCycle()" style="padding:3px 8px; font-size:9.6px; background:#34A853; border-color:#34A853;">▶ Play</button>
              <button class="btn-ui outline" id="tr-btn-step" onclick="stepTrCycle()" style="padding:3px 7px; font-size:9.5px; color:#137333; border-color:#A8DAB5;">⏭ +1 Tahap</button>
              <button class="btn-ui outline" onclick="resetTrCycle()" style="padding:3px 7px; font-size:9.5px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
            </div>
            <div style="display:flex; align-items:center; gap:3.5px;">
              <button class="btn-ui" data-trst="1" onclick="setTrStage(1)" style="padding:3px 6.5px; font-size:9.2px;">1. Forward</button>
              <button class="btn-ui outline" data-trst="2" onclick="setTrStage(2)" style="padding:3px 6.5px; font-size:9.2px;">2. Loss</button>
              <button class="btn-ui outline" data-trst="3" onclick="setTrStage(3)" style="padding:3px 6.5px; font-size:9.2px;">3. Backprop+GD</button>
              <button class="btn-ui outline" data-trst="4" onclick="setTrStage(4)" style="padding:3px 6.5px; font-size:9.2px;">4. Epoch</button>
            </div>
          </div>

          <!-- LIVE INTERACTIVE TRAINING CYCLE SVG (CONCRETE OLAF CASE: LOSS 2.18 -> 0.23, P 11.3% -> 79.2%!) -->
          <div style="flex:1; min-height:0; display:flex; align-items:center; justify-content:center; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:10px; padding:6px 8px;">
            <svg id="tr-cycle-svg" viewBox="0 0 600 316" style="width:100%; height:100%; display:block;"></svg>
          </div>

          <!-- BOTTOM LIVE TAKEAWAY CALLOUT -->
          <div class="callout green" id="tr-cycle-callout" style="padding:5px 9px; font-size:10.1px; line-height:1.34;"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 30 (NEW): WEIGHT INITIALIZATION, LEARNING RATE & OPTIMIZER (SGD vs ADAM) — FULL INTERACTIVE SIMULATOR -->
    <section class="slide" data-title="Bab 3C: Weight Initialization, Learning Rate &amp; Optimizer (SGD vs Adam)" data-notes="Alokasi waktu: 2 menit. Simulator interaktif penuh Tahap 5.2: (1) Klik Acak Bobot atau klik titik mana saja pada kurva parabola untuk menunjukkan Weight Initialization (Epoch 0), (2) klik Play / +1 Langkah atau geser slider Learning Rate (0.02–1.08) + preset Kecil/Ideal/Besar untuk menyaksikan bola meluncur mulus vs memantul liar saat LR > 1.0, dan (3) aktifkan mode Duel SGD vs Adam untuk membuktikan keunggulan adaptif optimizer Adam yang dipakai di Keras Hands-On.">
      <div class="kicker">BAB 03 · TAHAP 5.2 · WEIGHT INIT, LEARNING RATE &amp; OPTIMIZER</div>
      <h2><span class="hl-blue">Learning Rate</span> &amp; <span class="hl-green">Optimizer</span>: Mengatur Langkah Turun Bukit</h2>

      <div style="display:grid; grid-template-columns:0.86fr 1.34fr; gap:12px; flex:1; min-height:0; align-items:stretch;">
        <!-- LEFT COLUMN: 3 SYNC-CARDS (choreographed live with simulator!) -->
        <div style="display:flex; flex-direction:column; justify-content:space-between; gap:8px; min-height:0;">
          <div id="gd-sc-1" class="card tint-yellow sync-card" style="padding:9px 12px; gap:3.5px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-yellow"></div>
            <div class="card-title" style="font-size:12.4px; color:#B06000;">1. <em>Weight Initialization</em> (Bobot Acak)</div>
            <div style="font-size:10.9px; color:#3C4043; line-height:1.38;">
              Sebelum belajar (<strong>Epoch 0</strong>), seluruh bobot <code>W</code> diisi angka acak kecil. Akibatnya model mulai di lereng bukit <em>Loss</em> yang tinggi (<em>&ldquo;Model Bayi&rdquo;</em> yang tebakannya masih ngawur!).
            </div>
          </div>

          <div id="gd-sc-2" class="card tint-blue sync-card" style="padding:9px 12px; gap:3.5px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-blue"></div>
            <div class="card-title" style="font-size:12.4px; color:#1A73E8;">2. <em>Learning Rate</em> (Besar Langkah)</div>
            <div style="font-size:10.9px; color:#3C4043; line-height:1.38;">
              Mengatur seberapa jauh <code>W &amp; b</code> digeser tiap koreksi: <strong>terlalu kecil</strong> = sangat lambat; <strong>pas</strong> = mulus ke dasar lembah; <strong>terlalu besar</strong> = melompat liar &amp; <em>Loss</em> meledak!
            </div>
          </div>

          <div id="gd-sc-3" class="card tint-green sync-card" style="padding:9px 12px; gap:3.5px; flex:1; justify-content:center;">
            <div class="card-top-bar bar-green"></div>
            <div class="card-title" style="font-size:12.4px; color:#137333;">3. <em>Optimizer</em>: <code>SGD</code> vs <code>Adam</code></div>
            <div style="font-size:10.8px; color:#3C4043; line-height:1.36;">
              Mesin otomatis pengeksekusi <em>Gradient Descent</em>:<br/>
              • <strong><code>SGD</code>:</strong> langkah konstan, sederhana tapi mudah lambat/liar.<br/>
              • <strong><code>Adam</code> ★:</strong> menyesuaikan langkah adaptif tiap bobot — pilihan standar di Hands-On Keras kita!
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN: FULL 60FPS INTERACTIVE LR & OPTIMIZER SIMULATOR -->
        <div class="card" style="padding:8.5px 11.5px; gap:6px; justify-content:space-between; border:1.5px solid #C6DAFC; box-shadow:0 4px 14px rgba(66,133,244,0.06);">
          <!-- Row 1: Animation Controls + Optimizer Mode Switcher -->
          <div style="display:flex; align-items:center; justify-content:space-between; gap:5px; flex-wrap:wrap;">
            <div class="sim-bar pdf-keep-ui" style="gap:4.5px;">
              <button type="button" id="gd-btn-play" class="btn-ui green" onclick="toggleGdPlay()" style="padding:3.2px 9.5px; font-size:9.8px;">▶ Play</button>
              <button type="button" class="btn-ui outline" onclick="stepGdSim()" style="padding:3.2px 8.5px; font-size:9.8px;">⏭ +1 Langkah</button>
              <button type="button" class="btn-ui outline" onclick="randomizeGdStart()" style="padding:3.2px 8.5px; font-size:9.8px;" title="Acak posisi awal Weight Initialization (t=0)">🎲 Acak Bobot</button>
              <button type="button" class="btn-ui outline" onclick="resetGdSim()" style="padding:3.2px 7.5px; font-size:9.8px;">↺ Reset</button>
            </div>
            <div id="gd-opt-tabs" class="pdf-keep-ui" style="display:flex; gap:3.5px; align-items:center;">
              <button type="button" class="btn-ui" data-opt="sgd" onclick="setGdOptimizer('sgd')" style="padding:3px 8px; font-size:9.5px;">SGD</button>
              <button type="button" class="btn-ui outline" data-opt="adam" onclick="setGdOptimizer('adam')" style="padding:3px 8px; font-size:9.5px;">Adam ★</button>
              <button type="button" class="btn-ui outline" data-opt="duel" onclick="setGdOptimizer('duel')" style="padding:3px 8px; font-size:9.5px;">Duel SGD vs Adam</button>
            </div>
          </div>

          <!-- Row 2: Learning Rate Presets + Live Slider -->
          <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:9px; padding:4px 9px;">
            <div class="sim-bar pdf-keep-ui" id="gd-presets" style="gap:4px;">
              <button type="button" class="btn-ui outline" data-gd="small" onclick="setGdMode('small')" style="padding:2.5px 7.5px; font-size:9.4px;">1. LR Kecil</button>
              <button type="button" class="btn-ui" data-gd="ideal" onclick="setGdMode('ideal')" style="padding:2.5px 7.5px; font-size:9.4px;">2. LR Ideal</button>
              <button type="button" class="btn-ui outline" data-gd="large" onclick="setGdMode('large')" style="padding:2.5px 7.5px; font-size:9.4px;">3. LR Besar</button>
            </div>
            <div style="display:flex; align-items:center; gap:7px; flex:1; min-width:170px; justify-content:flex-end;">
              <span style="font-family:var(--font-title); font-size:9.6px; font-weight:700; color:#5F6368; white-space:nowrap;">Geser LR:</span>
              <input id="gd-lr-slider" type="range" min="0.02" max="1.08" step="0.01" value="0.20" oninput="setGdLrSlider(this.value)" style="width:128px; accent-color:#4285F4; cursor:pointer;" />
              <span id="gd-lr-val" style="font-family:var(--font-code); font-size:10.4px; font-weight:800; color:#1A73E8; background:#E8F0FE; border-radius:6px; padding:1.5px 6px; min-width:42px; text-align:center;">0.20</span>
            </div>
          </div>

          <!-- Interactive Canvas Stage (60fps ball rolling + click parabola to set Weight Init!) -->
          <div style="flex:1; min-height:0; display:flex; flex-direction:column; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:10px; padding:5px 7px; gap:2px;">
            <div style="display:flex; align-items:center; justify-content:space-between; font-size:9.4px; color:#5F6368;">
              <span id="gd-title" style="font-family:var(--font-title); font-weight:800; color:#202124;">LR Ideal (0.20) — Mulus ke Dasar Lembah</span>
              <span><strong>Tip:</strong> Klik kurva parabola untuk atur titik awal <code>w₀</code>!</span>
            </div>
            <canvas id="gd-canvas" width="620" height="305" onclick="clickGdCanvas(event)" style="width:100%; flex:1; min-height:0; object-fit:contain; display:block; cursor:crosshair;"></canvas>
          </div>

          <!-- Compact Live Telemetry Bar -->
          <div style="display:grid; grid-template-columns:0.85fr 1.05fr 1.1fr; gap:7px;">
            <div style="background:#F8F9FA; border:1px solid #E0E3E7; border-radius:8px; padding:4.5px 9px; display:flex; justify-content:space-between; align-items:center; font-size:10.5px;">
              <span style="color:#5F6368;">Langkah:</span>
              <strong id="gd-step-txt" style="font-family:var(--font-code); color:#1A73E8;">t = 10 / 10</strong>
            </div>
            <div style="background:#F8F9FA; border:1px solid #E0E3E7; border-radius:8px; padding:4.5px 9px; display:flex; justify-content:space-between; align-items:center; font-size:10.5px;">
              <span id="gd-w-lbl" style="color:#5F6368;">Weight (w):</span>
              <strong id="gd-end-w" style="font-family:var(--font-code); color:#202124;">-0.02</strong>
            </div>
            <div style="background:#F8F9FA; border:1px solid #E0E3E7; border-radius:8px; padding:4.5px 9px; display:flex; justify-content:space-between; align-items:center; font-size:10.5px;">
              <span id="gd-loss-lbl" style="color:#5F6368;">Nilai Loss:</span>
              <strong id="gd-end-loss" style="font-family:var(--font-code); color:#137333;">0.000</strong>
            </div>
          </div>

          <div id="gd-note" class="callout green" style="padding:5px 10px; font-size:10.4px; line-height:1.32;"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 31 (NEW): BATCH SIZE vs STEP vs EPOCH & PENGENALAN OVERFITTING — DUAL INTERACTIVE SIMULATORS -->
    <section class="slide" data-title="Bab 3C: Batch Size vs Epoch &amp; Pengenalan Overfitting" data-notes="Alokasi waktu: 2 menit. Dua simulator interaktif berdampingan: (Kiri) Simulator Batch Size vs Step vs Epoch pada 143 foto Frozen — klik Play, +1 Batch, atau ubah Batch Size (8 / 16 / 32 / 143) untuk melihat jumlah Step per Epoch &amp; total update bobot berubah langsung; (Kanan) Simulator Underfitting -> Good Fit -> Overfitting — klik Play atau geser slider Epoch (1–50) untuk menyaksikan kurva pola &amp; kurva Train vs Val Loss memisahkan zona Underfitting, Good Fit, dan Overfitting.">
      <div class="kicker">BAB 03 · TAHAP 5.3 · BATCH SIZE, EPOCH &amp; OVERFITTING</div>
      <h2><span class="hl-blue">Batch Size vs Epoch</span> &amp; Jebakan <span class="hl-red">Overfitting</span></h2>

      <div style="display:grid; grid-template-columns:1.0fr 1.08fr; gap:13px; flex:1; min-height:0; align-items:stretch;">
        <!-- LEFT PANEL: INTERACTIVE BATCH SIZE / STEP / EPOCH SIMULATOR -->
        <div class="card surface" style="padding:10px 12px; gap:6.5px; justify-content:space-between; border:1.5px solid #C6DAFC;">
          <div class="card-top-bar bar-blue"></div>
          <div style="display:flex; align-items:center; justify-content:space-between; gap:6px;">
            <div>
              <span class="pill blue" style="font-size:9px; padding:1.5px 7px;">SIMULATOR 1 · CARA MEMBACA DATA</span>
              <div class="card-title" style="margin-top:3px; font-size:13.4px;">Kenapa di Keras Ada <code id="bs-title-code">batch_size=16</code>?</div>
            </div>
            <div id="bs-size-tabs" class="pdf-keep-ui" style="display:flex; gap:3px; flex-wrap:wrap; justify-content:flex-end;">
              <button type="button" class="btn-ui outline" data-bs="8" onclick="setBatchSizeSim(8)" style="padding:2.5px 6.5px; font-size:9.2px;">8</button>
              <button type="button" class="btn-ui" data-bs="16" onclick="setBatchSizeSim(16)" style="padding:2.5px 6.5px; font-size:9.2px;">16 ★</button>
              <button type="button" class="btn-ui outline" data-bs="32" onclick="setBatchSizeSim(32)" style="padding:2.5px 6.5px; font-size:9.2px;">32</button>
              <button type="button" class="btn-ui outline" data-bs="143" onclick="setBatchSizeSim(143)" style="padding:2.5px 6.5px; font-size:9.2px;">143</button>
            </div>
          </div>

          <!-- Animation controls for Batch Simulator -->
          <div style="display:flex; align-items:center; justify-content:space-between; gap:6px; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:8px; padding:4px 8px;">
            <div id="bs-ctrl" class="sim-bar pdf-keep-ui" style="gap:4px;">
              <button type="button" id="bs-btn-play" class="btn-ui green" onclick="toggleBsPlay()" style="padding:2.8px 8.5px; font-size:9.4px;">▶ Play 1 Epoch</button>
              <button type="button" class="btn-ui outline" onclick="stepBsSim()" style="padding:2.8px 7.5px; font-size:9.4px;">⏭ +1 Batch</button>
              <button type="button" class="btn-ui outline" onclick="resetBsSim()" style="padding:2.8px 7px; font-size:9.4px;">↺</button>
            </div>
            <span id="bs-status-pill" style="font-family:var(--font-code); font-size:9.4px; font-weight:800; color:#137333; background:#E6F4EA; border-radius:999px; padding:2px 8px;">Epoch 1 ✓ (9/9 Step)</span>
          </div>

          <!-- Interactive 3-Stage Visual Pipeline: Tumpukan Foto -> Mesin NN + RAM -> Update Bobot W & b -->
          <div style="background:#FFFFFF; border:1px solid #E0E3E7; border-radius:10px; padding:7px 8px; display:flex; flex-direction:column; gap:5.5px; flex:1; justify-content:space-between;">
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:9.4px; color:#5F6368;">
              <span>Alur 1 Epoch (<strong style="color:#202124;">{total_imgs} foto Frozen</strong>):</span>
              <strong id="bs-photo-prog" style="font-family:var(--font-code); color:#1A73E8;">48 / 143 foto</strong>
            </div>

            <!-- 3-Stage Animated Visual SVG -->
            <svg id="bs-svg" viewBox="0 0 470 154" style="width:100%; flex:1; min-height:0; display:block;"></svg>

            <!-- Compact Clickable Batch Strip (click any batch to inspect that step!) -->
            <div style="display:flex; flex-direction:column; gap:3px;">
              <div style="display:flex; justify-content:space-between; font-size:8.6px; color:#5F6368;">
                <span>Klik paket batch di bawah (atau tekan <strong>▶ Play</strong>):</span>
                <span id="bs-strip-legend">Hijau = selesai · Kuning = diproses di NN</span>
              </div>
              <div id="bs-grid" style="display:flex; flex-wrap:wrap; gap:3.5px; align-items:center;"></div>
            </div>

            <!-- Live Summary Equation Bar -->
            <div id="bs-eq-bar" style="background:#F8F9FA; border:1px solid #E0E3E7; border-radius:8px; padding:4.5px 8px; display:flex; justify-content:space-between; align-items:center; font-family:var(--font-code); font-size:9.3px;">
              <span style="color:#3C4043;">⌈143 / 16⌉ = <strong style="color:#1A73E8;">9 Step/Epoch</strong></span>
              <span style="color:#137333; font-weight:800;">20 Epoch = 180× update W,b</span>
            </div>
          </div>

          <div style="display:flex; flex-direction:column; gap:3.5px; font-size:10.5px; color:#3C4043; line-height:1.34;">
            <div>• <strong><code>Batch Size</code>:</strong> Paket foto sekali proses agar RAM aman &amp; bobot cepat dikoreksi.</div>
            <div>• <strong><code>Step / Iteration</code>:</strong> 1× siklus <code>Forward → Loss → Backprop</code> untuk 1 batch.</div>
            <div>• <strong><code>Epoch</code>:</strong> 1 putaran penuh melewati seluruh {total_imgs} foto Frozen!</div>
          </div>

          <div id="bs-callout" class="callout" style="padding:5.5px 9px; font-size:10.2px; line-height:1.3;">
            <strong>Analogi Kartu Soal:</strong> Daripada menunggu 143 soal selesai baru cek jawaban, model mengoreksi diri tiap <strong>16 soal (1 Batch)</strong>!
          </div>
        </div>

        <!-- RIGHT PANEL: INTERACTIVE UNDERFITTING vs GOOD FIT vs OVERFITTING SIMULATOR -->
        <div class="card surface" style="padding:10px 12px; gap:6.5px; justify-content:space-between; border:1.5px solid #F6AEA9;">
          <div class="card-top-bar bar-red"></div>
          <div style="display:flex; align-items:center; justify-content:space-between; gap:6px;">
            <div style="min-width:0;">
              <span class="pill red" style="font-size:9px; padding:1.5px 7px;">SIMULATOR 2 · KUALITAS BELAJAR</span>
              <div class="card-title" style="margin-top:3px; font-size:13.2px; white-space:nowrap;">Hafal Kunci vs Paham Pola!</div>
            </div>
            <div id="fit-tabs" class="pdf-keep-ui" style="display:flex; gap:3px; flex-wrap:nowrap; flex-shrink:0;">
              <button type="button" class="btn-ui outline" data-fit="under" onclick="setFitScenario('under')" style="padding:2.5px 6px; font-size:8.8px; white-space:nowrap;">Underfit</button>
              <button type="button" class="btn-ui" data-fit="good" onclick="setFitScenario('good')" style="padding:2.5px 6px; font-size:8.8px; white-space:nowrap;">Good Fit ✓</button>
              <button type="button" class="btn-ui outline" data-fit="over" onclick="setFitScenario('over')" style="padding:2.5px 6px; font-size:8.8px; white-space:nowrap;">Overfit</button>
              <button type="button" class="btn-ui outline" data-fit="all" onclick="setFitScenario('all')" style="padding:2.5px 6px; font-size:8.8px; white-space:nowrap;" title="Alur nyambung Underfit → Good Fit → Overfit (Epoch 1–50)">Semua</button>
            </div>
          </div>

          <!-- Play + Reset + Epoch Slider Control -->
          <div style="display:flex; align-items:center; justify-content:space-between; gap:6px; background:#FFFFFF; border:1px solid #E0E3E7; border-radius:8px; padding:4px 8px;">
            <div style="display:flex; align-items:center; gap:4px;">
              <button type="button" id="fit-btn-play" class="btn-ui green" onclick="toggleFitPlay()" style="padding:2.8px 8.5px; font-size:9.3px; white-space:nowrap;">▶ Play Good Fit</button>
              <button type="button" class="btn-ui outline" onclick="resetFitSim()" style="padding:2.8px 6.5px; font-size:9.3px;" title="Ulang dari Epoch 1">↺</button>
            </div>
            <div style="display:flex; align-items:center; gap:5px; flex:1; justify-content:flex-end;">
              <span style="font-family:var(--font-title); font-size:9.3px; font-weight:700; color:#5F6368;">Epoch:</span>
              <input id="fit-ep-slider" type="range" min="1" max="30" step="1" value="30" oninput="setFitEpoch(this.value)" style="width:105px; accent-color:#34A853; cursor:pointer;" />
              <span id="fit-ep-val" style="font-family:var(--font-code); font-size:9.8px; font-weight:800; color:#137333; background:#E6F4EA; border-radius:6px; padding:1.5px 6px; min-width:44px; text-align:center;">30/30</span>
            </div>
          </div>

          <!-- Interactive Dual Canvas (Left: Pattern Fit · Right: Train vs Val Loss) -->
          <div style="background:#FFFFFF; border:1px solid #E0E3E7; border-radius:10px; padding:5px 7px; flex:1; min-height:0; display:flex; flex-direction:column; gap:3px;">
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:9.3px; color:#5F6368;">
              <span id="fit-zone-title" style="font-family:var(--font-title); font-weight:800; color:#137333;">2. Good Fit / Generalization ✓ (Target Ideal!)</span>
              <span>● Latih (Train) &nbsp; ★ Foto Baru (Val)</span>
            </div>
            <canvas id="fit-canvas" width="520" height="268" style="width:100%; flex:1; min-height:0; object-fit:contain; display:block;"></canvas>
          </div>

          <!-- Live Train vs Val Accuracy Comparison Strip -->
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:7px;">
            <div style="background:#FFFFFF; border:1px solid #E0E3E7; border-radius:8px; padding:4.5px 9px; display:flex; justify-content:space-between; align-items:center; font-size:10.3px;">
              <span style="color:#5F6368;">Akurasi Latih (Train):</span>
              <strong id="fit-acc-tr" style="font-family:var(--font-code); color:#1A73E8;">88%</strong>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E0E3E7; border-radius:8px; padding:4.5px 9px; display:flex; justify-content:space-between; align-items:center; font-size:10.3px;">
              <span style="color:#5F6368;">Akurasi Foto Baru (Val):</span>
              <strong id="fit-acc-val" style="font-family:var(--font-code); color:#137333;">85% ✓</strong>
            </div>
          </div>

          <div id="fit-callout" class="callout green" style="padding:5.5px 9px; font-size:10.2px; line-height:1.3;">
            <strong>Good Fit (Generalization):</strong> Model menangkap ciri asli karakter Frozen — akurat di foto latihan <strong>DAN</strong> foto baru! (Di <strong>P05</strong> kita pisah <code>train/val/test</code> agar <em>Overfitting</em> langsung terdeteksi!)
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 32: ULTIMATE BAB 3 — SIMULASI FULL NEURAL NETWORK END-TO-END (TAHAP 1 -> 2 -> 3 -> 4 -> 5!) -->
    <section class="slide" data-title="Bab 3 · Simulasi Full Neural Network (End-to-End Tahap 1–5)" data-notes="Alokasi waktu: {"3.5" if HIDE_BAB4_ARCH else "3"} menit. Slide puncak (Ultimate) Bab 3 yang menyatukan seluruh 5 tahap dari Slide 20–31 dalam 1 model Neural Network nyata 1-layer (150.528 Input -> 5 Output Softmax = 752.645 parameter, tanpa konsep yang belum diajarkan!) yang dilatih langsung 8 epoch melewati kelima foto figurin Frozen. Demokan: klik tombol biru Full 8 Epoch agar peserta menyaksikan model melatih Anna, Elsa, Kristoff, Olaf, dan Sven secara bergantian dari Epoch 1 (0/5 benar, Mean Loss 1.70) hingga Epoch 8 (5/5 benar yakin, Mean Loss 0.21) lengkap dengan gelombang merah Backpropagation dan kurva Loss yang turun secara real-time! Atau klik 1 Foto / geser slider Epoch 1–8 / klik kartu tahap bawah untuk membedah 1 karakter pelan-pelan. Lalu lanjut ke Kuis 5 Soal Berilustrasi di Slide 34–38.">
      <div class="kicker">BAB 03 · SIMULASI FULL NEURAL NETWORK (END-TO-END · TAHAP 1–5)</div>
      <h2>Simulasi <span class="hl-blue">Full Neural Network</span>: Dari Piksel ke <span class="hl-red">Backprop</span> (<span class="hl-green">Tahap 1–5</span>)</h2>

      <!-- UNIFIED CONTROL BAR: Full 8 Epoch (All 5 Chars!), 1 Foto, +1 Tahap, Reset | 5 Frozen Photos w/ Live Status Dots | Epoch 1..8 -->
      <div class="sim-bar pdf-keep-ui" id="fnn-ctrl" style="margin-bottom:6px; justify-content:space-between; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:11px; padding:4px 8px; gap:5px; flex-wrap:nowrap;">
        <div style="display:flex; align-items:center; gap:4px; flex-shrink:0;">
          <button class="btn-ui" id="fnn-btn-full" onclick="playFnnFull()" style="padding:3.5px 8.5px; font-size:9.8px; background:#1A73E8; border-color:#1A73E8;" title="Jalankan training penuh 8 Epoch melewati semua 5 karakter bergantian!">▶ Full 8 Epoch</button>
          <button class="btn-ui" id="fnn-btn-play" onclick="playFnnSim()" style="padding:3.5px 8px; font-size:9.8px; background:#34A853; border-color:#34A853;" title="Jalankan 5 tahap pelan untuk 1 karakter yang dipilih">▶ 1 Foto</button>
          <button class="btn-ui outline" id="fnn-btn-step" onclick="stepFnnStage()" style="padding:3.5px 7px; font-size:9.6px; color:#137333; border-color:#A8DAB5;">⏭ +1 Tahap</button>
          <button class="btn-ui outline" id="fnn-btn-reset" onclick="resetFnnSim()" style="padding:3.5px 6.5px; font-size:9.6px; color:#5F6368; border-color:#DADCE0;">↺ Reset</button>
        </div>
        <div id="fnn-char-bar" style="display:flex; align-items:center; gap:3.5px; flex-shrink:0;"></div>
        <div style="display:flex; align-items:center; gap:5px; background:#FFFFFF; border:1px solid #DADCE0; border-radius:999px; padding:2.5px 8px; flex-shrink:0;">
          <strong style="font-family:var(--font-title); font-size:9.4px; color:#1A73E8; white-space:nowrap;">Epoch:</strong>
          <input id="fnn-ep-slider" type="range" min="1" max="8" step="1" value="8" oninput="onFnnEpochSlide()" style="width:62px; accent-color:#1A73E8; cursor:pointer; margin:0;"/>
          <span id="fnn-ep-pill" style="font-family:var(--font-code); font-size:9.3px; font-weight:700; color:#137333; min-width:96px; text-align:right;">E8/8 · 5/5 · 0.21</span>
        </div>
      </div>

      <!-- HERO FULL-WIDTH END-TO-END ARCHITECTURE + 60FPS FORWARD & BACKPROP MOTION OVERLAY -->
      <div id="fnn-stage-wrap" style="position:relative; flex:1; min-height:0; display:flex; flex-direction:column; justify-content:space-between; background:#FFFFFF; border:1.5px solid #C6DAFC; border-radius:15px; padding:6px 10px 6px; margin-bottom:6px; box-shadow:0 4px 16px rgba(66,133,244,0.07);">
        <canvas id="fnn-motion-canvas" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:25;"></canvas>

        <!-- Main Interactive 5-Column Panorama SVG (viewBox 1050 x 284) -->
        <div style="flex:1; min-height:0; display:flex; align-items:center; justify-content:center;">
          <svg id="fnn-svg" viewBox="0 0 1050 284" style="width:100%; height:100%; max-height:284px; display:block;"></svg>
        </div>

        <!-- Live Narration Strip Connecting Active Stage -> Real Numbers -->
        <div id="fnn-narration" style="font-size:10.2px; color:#202124; background:#F8F9FA; border:1px solid #E0E3E7; border-radius:8px; padding:4px 10px; line-height:1.32; display:flex; align-items:center; justify-content:space-between; gap:10px;">
          <span id="fnn-narr-txt"></span>
          <span id="fnn-narr-meta" style="font-family:var(--font-code); font-size:9.3px; font-weight:700; color:#5F6368; white-space:nowrap;">Total Param (W+b): 752.645</span>
        </div>
      </div>

      <!-- 5 CLICKABLE SYNCHRONIZED STAGE CARDS (TAHAP 1 -> TAHAP 2 -> TAHAP 3 -> TAHAP 4 -> TAHAP 5!) -->
      <div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:7px; flex:0 0 auto;">
        <div id="fnn-card-1" class="card surface sync-card fnn-stage-card" onclick="jumpFnnStage(1)" style="padding:5.5px 8px; gap:1.5px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title" style="font-size:10.7px; color:#1A73E8;">1. Piksel Foto</div>
          <div style="font-size:9.6px; color:#3C4043; line-height:1.28;">Foto <code>224×224×3</code> dibaca jadi angka piksel <code>0.0–1.0</code>.</div>
        </div>
        <div id="fnn-card-2" class="card tint-blue sync-card fnn-stage-card" onclick="jumpFnnStage(2)" style="padding:5.5px 8px; gap:1.5px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title" style="font-size:10.7px; color:#1A73E8;">2. Flatten (Input)</div>
          <div style="font-size:9.6px; color:#3C4043; line-height:1.28;">Disusun ke bawah jadi <strong>150.528 neuron</strong> <em>Input Layer</em>.</div>
        </div>
        <div id="fnn-card-3" class="card tint-yellow sync-card fnn-stage-card" onclick="jumpFnnStage(3)" style="padding:5.5px 8px; gap:1.5px;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title" style="font-size:10.7px; color:#B06000;">3. Weight + Bias</div>
          <div style="font-size:9.6px; color:#3C4043; line-height:1.28;">Hitung <code>z = Σ(x·w) + b</code> untuk <strong>5 skor mentah</strong> kelas.</div>
        </div>
        <div id="fnn-card-4" class="card tint-green sync-card fnn-stage-card" onclick="jumpFnnStage(4)" style="padding:5.5px 8px; gap:1.5px;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title" style="font-size:10.7px; color:#137333;">4. Softmax &amp; Argmax</div>
          <div style="font-size:9.6px; color:#3C4043; line-height:1.28;"><strong>Softmax</strong> ubah skor jadi probabilitas (<code>100%</code>) → <strong>Argmax</strong>.</div>
        </div>
        <div id="fnn-card-5" class="card tint-red sync-card fnn-stage-card" onclick="jumpFnnStage(5)" style="padding:5.5px 8px; gap:1.5px;">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title" style="font-size:10.7px; color:#C5221F;">5. Loss &amp; Backprop</div>
          <div style="font-size:9.6px; color:#3C4043; line-height:1.28;"><strong>Loss</strong> koreksi balik <code>W, b</code> melewati <strong>5 foto × 8 Epoch</strong>!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
        )

    if not HIDE_SLIDES_28_40:
        s.append(
            f"""
    <!-- 28: SATU NEURON INPUT KE SEMUA NEURON OUTPUT + SIMULATOR #6 -->
    <section class="slide" data-title="Bab 3C: Koneksi 1 Neuron Input ke 5 Neuron Output" data-notes="Alokasi waktu: 1.5 menit. Ini visual inti permintaan desain kita: telusuri tepat 1 neuron dari Input Layer ke seluruh 5 neuron Output Layer. Klik tombol neuron input x1, x2, x3, atau x4 untuk menyorot 5 garis weight miliknya!">
      <div class="kicker">BAB 03 · FULLY CONNECTED LAYER</div>
      <h2>Telusuri <span class="hl-red">1 Neuron Input</span> → 5 Neuron Output</h2>
      <div class="sim-bar pdf-keep-ui" id="trace-btns" style="margin-bottom:8px;">
        <button class="btn-ui" data-tr="0" onclick="setTraceNeuron(0)">Sorot Neuron x₁ (Piksel #1)</button>
        <button class="btn-ui outline" data-tr="1" onclick="setTraceNeuron(1)">Sorot Neuron x₂ (Piksel #2)</button>
        <button class="btn-ui outline" data-tr="2" onclick="setTraceNeuron(2)">Sorot Neuron x₃ (Piksel #3)</button>
        <button class="btn-ui outline" data-tr="3" onclick="setTraceNeuron(3)">Sorot Neuron x₄ (Piksel #4)</button>
      </div>
      <div class="split-60-40">
        <div class="canvas-box" style="justify-content:center;">
          <svg id="trace-svg" viewBox="0 0 480 285" style="width:100%; height:340px;"></svg>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div>
            <span class="pill red" id="trace-pill">NEURON x₁ AKTIF</span>
            <div class="card-title" style="margin-top:8px;">Setiap Garis = 1 Angka <em>Weight</em></div>
          </div>
          <div class="card-body" style="font-size:13.2px;" id="trace-desc">
            <ul>
              <li><strong>1 neuron input</strong> mengirim nilainya ke <strong>semua 5 neuron output</strong> secara serentak.</li>
              <li>Artinya, <strong>1 neuron input saja</strong> langsung membutuhkan <strong>5 buah weight</strong> (masing-masing untuk Anna, Elsa, Kristoff, Olaf, dan Sven).</li>
              <li>Pola sambungan penuh seperti ini disebut <strong>Fully Connected / Dense Layer</strong>.</li>
            </ul>
          </div>
          <div class="callout red" id="trace-callout"><strong>Bayangkan:</strong> Jika 1 neuron input punya 5 garis weight, bagaimana jika input layer kita punya <strong>150.528 neuron</strong>?</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 29: HITUNG WEIGHT TANPA HIDDEN LAYER -->
    <section class="slide" data-title="Bab 3C: Hitung Parameter Tanpa Hidden Layer" data-notes="Alokasi waktu: 1 menit. Mari hitung persis dengan matematika dasar: 150.528 neuron input disambung langsung ke 5 neuron output menghasilkan 752.640 weight + 5 bias = 752.645 parameter.">
      <div class="kicker">BAB 03 · HITUNG PARAMETER</div>
      <h2>Berapa Banyak Weight jika <span class="hl-blue">Input Langsung ke Output?</span></h2>
      <div class="grid-2">
        <div class="card tint-blue" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Rumus Hitung Parameter 1 Dense Layer</div>
          <div class="formula-box" style="font-size:14px;">Total Parameter = (Neuron Input × Neuron Output) + Bias</div>
          <div class="card-body" style="font-size:14px;">
            <ul>
              <li>Jumlah neuron <strong>Input Layer</strong> (foto <code>224×224×3</code>): <strong>150.528</strong></li>
              <li>Jumlah neuron <strong>Output Layer</strong> (5 karakter): <strong>5</strong></li>
              <li>Jumlah <strong>Weight</strong>: <code>150.528 × 5 = 752.640</code> garis koneksi</li>
              <li>Jumlah <strong>Bias</strong>: <code>5</code> (1 bias untuk tiap neuron output)</li>
            </ul>
          </div>
          <div class="kpi-mini" style="background:#FFFFFF; border-color:#4285F4;">
            <div class="k-num" style="font-size:26px;">752.645 Parameter</div>
            <div class="k-lbl">Baru 1 lapisan langsung — belum pakai Hidden Layer!</div>
          </div>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title">Masalah Jaringan Tanpa Hidden Layer</div>
          <div class="card-body" style="font-size:13.8px;">
            <ul>
              <li>Tanpa <strong>Hidden Layer</strong>, setiap kelas hanya dihitung lewat 1 penjumlahan lurus dari piksel (<em>linear classifier</em>).</li>
              <li>Ia seperti hanya membuat 1 &ldquo;template rata-rata&rdquo; per karakter — tidak bisa memahami bentuk mata, rambut, atau pose yang bervariasi.</li>
              <li>Untuk mengenali pola visual yang kompleks (terutama di latar ramai), kita perlu menambahkan lapisan perantara: <strong>Hidden Layer</strong>!</li>
            </ul>
          </div>
          <div class="callout red"><strong>Selanjutnya:</strong> Mari masukkan <strong>Hidden Layer</strong> di tengah dan lihat cara kerjanya!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 30: MENGAPA PERLU HIDDEN LAYER -->
    <section class="slide" data-title="Bab 3D: Mengapa Perlu Hidden Layer?" data-notes="Alokasi waktu: 1 menit. Hidden Layer bertugas memecah masalah sulit menjadi tahapan pola sederhana: dari piksel mentah -> garis & warna -> bagian bentuk -> keputusan karakter utuh.">
      <div class="kicker">BAB 03 · HIDDEN LAYER</div>
      <h2>Mengapa Butuh <span class="hl-green">Hidden Layer</span> di Tengah?</h2>
      <p class="subtitle">Menebak karakter langsung dari piksel itu terlalu berat. <strong>Hidden Layer</strong> belajar mengenali pola secara bertahap dari sederhana ke kompleks.</p>
      <div class="grid-4" style="align-items:stretch;">
        <div class="card tint-blue" style="justify-content:flex-start; gap:12px;">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">TAHAP 1</span>
          <div class="card-title">Input Layer</div>
          <div class="card-body" style="font-size:13.4px;">Menerima angka piksel mentah <code>0.0–1.0</code> dari foto Frozen. Belum tahu bentuk apa pun.</div>
          <div class="mini-box" style="margin-top:auto;"><strong>Contoh:</strong> 150.528 angka intensitas R, G, B.</div>
        </div>
        <div class="card tint-yellow" style="justify-content:flex-start; gap:12px;">
          <div class="card-top-bar bar-yellow"></div>
          <span class="pill yellow">TAHAP 2</span>
          <div class="card-title">Hidden Layer 1</div>
          <div class="card-body" style="font-size:13.4px;">Menggabungkan piksel menjadi pola dasar: <strong>kontras terang-gelap, warna dominan, tepi garis</strong>.</div>
          <div class="mini-box" style="margin-top:auto;"><strong>Contoh:</strong> Tepian gaun biru &amp; area putih salju.</div>
        </div>
        <div class="card tint-red" style="justify-content:flex-start; gap:12px;">
          <div class="card-top-bar bar-red"></div>
          <span class="pill red">TAHAP 3</span>
          <div class="card-title">Hidden Layer 2</div>
          <div class="card-body" style="font-size:13.4px;">Menggabungkan pola dasar menjadi <strong>ciri bagian objek</strong>: bentuk rambut, warna gaun, siluet tubuh.</div>
          <div class="mini-box" style="margin-top:auto;"><strong>Contoh:</strong> Kombinasi rambut pirang + gaun biru.</div>
        </div>
        <div class="card tint-green" style="justify-content:flex-start; gap:12px;">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">TAHAP 4</span>
          <div class="card-title">Output Layer</div>
          <div class="card-body" style="font-size:13.4px;">Menggabungkan semua ciri menjadi keputusan akhir 5 probabilitas <code>Softmax</code>.</div>
          <div class="mini-box" style="margin-top:auto;"><strong>Contoh:</strong> Prediksi akhir 5 karakter Frozen!</div>
        </div>
      </div>
      <div class="callout green" style="margin-top:10px;"><strong>Asal kata &ldquo;Deep Learning&rdquo;:</strong> Semakin banyak <strong>Hidden Layer</strong> yang ditumpuk (<em>deep</em> = dalam), semakin tinggi kemampuan jaringan menyusun pola bertingkat!</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 31: DIAGRAM NETWORK UTUH -->
    <section class="slide" data-title="Bab 3D: Diagram Neural Network Utuh (MLP)" data-notes="Alokasi waktu: 1 menit. Inilah arsitektur utuh Multi-Layer Perceptron (MLP): Input Layer -> Hidden Layer (+ ReLU) -> Output Layer (+ Softmax). Tunjukkan alur informasi dari kiri ke kanan.">
      <div class="kicker">BAB 03 · ARSITEKTUR MLP</div>
      <h2>Arsitektur Utuh <span class="hl-blue">Multi-Layer Perceptron (MLP)</span></h2>
      <div class="card surface" style="flex:1; align-items:center; justify-content:center; padding:12px;">
        <svg viewBox="0 0 820 324" style="width:100%; max-height:366px;">
          <!-- Tapered Funnel Layer Boxes: Tallest Input (150.528) -> Medium Hidden (128) -> Compact Output (5) -->
          <rect x="20" y="6" width="174" height="312" rx="16" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.2"/>
          <text x="107" y="26" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#1A73E8">Input Layer</text>
          <text x="107" y="40" text-anchor="middle" font-family="Roboto Mono" font-size="9.8" font-weight="700" fill="#1A73E8">150.528 neuron piksel</text>

          <rect x="285" y="34" width="204" height="256" rx="16" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2.2"/>
          <text x="387" y="55" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#B06000">Hidden Layer (+ ReLU)</text>
          <text x="387" y="70" text-anchor="middle" font-family="Roboto Mono" font-size="9.8" fill="#5F6368">mis. 128 neuron pengolah pola</text>

          <rect x="580" y="68" width="220" height="190" rx="16" fill="#E6F4EA" stroke="#34A853" stroke-width="2.2"/>
          <text x="690" y="89" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">Output Layer (+ Softmax)</text>
          <text x="690" y="103" text-anchor="middle" font-family="Roboto Mono" font-size="9.8" fill="#5F6368">5 neuron kelas Frozen</text>

          <!-- Funnel Connections: Input (9 visible nodes) -> Hidden (6 visible nodes) -> Output (5 nodes) -->
          <g stroke="#9AA0A6" stroke-width="1.05" opacity="0.52">
            <!-- Input -> Hidden -->
            <line x1="122" y1="62"  x2="372" y2="96"/><line x1="122" y1="62"  x2="372" y2="128"/><line x1="122" y1="62"  x2="372" y2="160"/><line x1="122" y1="62"  x2="372" y2="192"/><line x1="122" y1="62"  x2="372" y2="252"/>
            <line x1="122" y1="90"  x2="372" y2="96"/><line x1="122" y1="90"  x2="372" y2="128"/><line x1="122" y1="90"  x2="372" y2="160"/><line x1="122" y1="90"  x2="372" y2="192"/><line x1="122" y1="90"  x2="372" y2="252"/>
            <line x1="122" y1="118" x2="372" y2="96"/><line x1="122" y1="118" x2="372" y2="128"/><line x1="122" y1="118" x2="372" y2="160"/><line x1="122" y1="118" x2="372" y2="192"/><line x1="122" y1="118" x2="372" y2="252"/>
            <line x1="122" y1="146" x2="372" y2="96"/><line x1="122" y1="146" x2="372" y2="128"/><line x1="122" y1="146" x2="372" y2="160"/><line x1="122" y1="146" x2="372" y2="192"/><line x1="122" y1="146" x2="372" y2="252"/>
            <line x1="122" y1="174" x2="372" y2="96"/><line x1="122" y1="174" x2="372" y2="128"/><line x1="122" y1="174" x2="372" y2="160"/><line x1="122" y1="174" x2="372" y2="192"/><line x1="122" y1="174" x2="372" y2="252"/>
            <line x1="122" y1="202" x2="372" y2="96"/><line x1="122" y1="202" x2="372" y2="128"/><line x1="122" y1="202" x2="372" y2="160"/><line x1="122" y1="202" x2="372" y2="192"/><line x1="122" y1="202" x2="372" y2="252"/>
            <line x1="122" y1="256" x2="372" y2="96"/><line x1="122" y1="256" x2="372" y2="128"/><line x1="122" y1="256" x2="372" y2="160"/><line x1="122" y1="256" x2="372" y2="192"/><line x1="122" y1="256" x2="372" y2="252"/>
            <line x1="122" y1="284" x2="372" y2="96"/><line x1="122" y1="284" x2="372" y2="128"/><line x1="122" y1="284" x2="372" y2="160"/><line x1="122" y1="284" x2="372" y2="192"/><line x1="122" y1="284" x2="372" y2="252"/>
            <!-- Hidden -> Output -->
            <line x1="402" y1="96"  x2="622" y2="124"/><line x1="402" y1="96"  x2="622" y2="152"/><line x1="402" y1="96"  x2="622" y2="180"/><line x1="402" y1="96"  x2="622" y2="208"/><line x1="402" y1="96"  x2="622" y2="236"/>
            <line x1="402" y1="128" x2="622" y2="124"/><line x1="402" y1="128" x2="622" y2="152"/><line x1="402" y1="128" x2="622" y2="180"/><line x1="402" y1="128" x2="622" y2="208"/><line x1="402" y1="128" x2="622" y2="236"/>
            <line x1="402" y1="160" x2="622" y2="124"/><line x1="402" y1="160" x2="622" y2="152"/><line x1="402" y1="160" x2="622" y2="180"/><line x1="402" y1="160" x2="622" y2="208"/><line x1="402" y1="160" x2="622" y2="236"/>
            <line x1="402" y1="192" x2="622" y2="124"/><line x1="402" y1="192" x2="622" y2="152"/><line x1="402" y1="192" x2="622" y2="180"/><line x1="402" y1="192" x2="622" y2="208"/><line x1="402" y1="192" x2="622" y2="236"/>
            <line x1="402" y1="252" x2="622" y2="124"/><line x1="402" y1="252" x2="622" y2="152"/><line x1="402" y1="252" x2="622" y2="180"/><line x1="402" y1="252" x2="622" y2="208"/><line x1="402" y1="252" x2="622" y2="236"/>
          </g>

          <!-- Input nodes (8 densely stacked circles + 150.520 ellipsis) -->
          <circle cx="107" cy="62"  r="11.5" fill="#4285F4" stroke="#FFF" stroke-width="2"/><text x="107" y="65.5"  text-anchor="middle" font-family="Roboto Mono" font-size="8.8" font-weight="700" fill="#FFF">x₁</text>
          <circle cx="107" cy="90"  r="11.5" fill="#4285F4" stroke="#FFF" stroke-width="2"/><text x="107" y="93.5"  text-anchor="middle" font-family="Roboto Mono" font-size="8.8" font-weight="700" fill="#FFF">x₂</text>
          <circle cx="107" cy="118" r="11.5" fill="#4285F4" stroke="#FFF" stroke-width="2"/><text x="107" y="121.5" text-anchor="middle" font-family="Roboto Mono" font-size="8.8" font-weight="700" fill="#FFF">x₃</text>
          <circle cx="107" cy="146" r="11.5" fill="#4285F4" stroke="#FFF" stroke-width="2"/><text x="107" y="149.5" text-anchor="middle" font-family="Roboto Mono" font-size="8.8" font-weight="700" fill="#FFF">x₄</text>
          <circle cx="107" cy="174" r="11.5" fill="#4285F4" stroke="#FFF" stroke-width="2"/><text x="107" y="177.5" text-anchor="middle" font-family="Roboto Mono" font-size="8.8" font-weight="700" fill="#FFF">x₅</text>
          <circle cx="107" cy="202" r="11.5" fill="#4285F4" stroke="#FFF" stroke-width="2"/><text x="107" y="205.5" text-anchor="middle" font-family="Roboto Mono" font-size="8.8" font-weight="700" fill="#FFF">x₆</text>
          <circle cx="107" cy="222" r="2.2" fill="#1A73E8"/><circle cx="107" cy="230" r="2.2" fill="#1A73E8"/><circle cx="107" cy="238" r="2.2" fill="#1A73E8"/>
          <text x="144" y="233" text-anchor="middle" font-family="Roboto Mono" font-size="8" font-weight="700" fill="#1A73E8">+150.520</text>
          <circle cx="107" cy="256" r="11.5" fill="#4285F4" stroke="#FFF" stroke-width="2"/><text x="107" y="259.5" text-anchor="middle" font-family="Roboto Mono" font-size="7.8" font-weight="700" fill="#FFF">xₙ₋₁</text>
          <circle cx="107" cy="284" r="11.5" fill="#4285F4" stroke="#FFF" stroke-width="2"/><text x="107" y="287.5" text-anchor="middle" font-family="Roboto Mono" font-size="8.8" font-weight="700" fill="#FFF">xₙ</text>
          <text x="107" y="310" text-anchor="middle" font-family="Roboto" font-size="9.5" font-weight="700" fill="#1A73E8">Piksel 0.0–1.0 (Sangat Banyak!)</text>

          <!-- Hidden nodes (5 visible circles + ellipsis -> medium) -->
          <circle cx="387" cy="96"  r="13" fill="#FBBC04" stroke="#FFF" stroke-width="2.2"/><text x="387" y="99.5"  text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#202124">h₁</text>
          <circle cx="387" cy="128" r="13" fill="#EA4335" stroke="#FFF" stroke-width="2.2"/><text x="387" y="131.5" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#FFF">h₂</text>
          <circle cx="387" cy="160" r="13" fill="#FBBC04" stroke="#FFF" stroke-width="2.2"/><text x="387" y="163.5" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#202124">h₃</text>
          <circle cx="387" cy="192" r="13" fill="#EA4335" stroke="#FFF" stroke-width="2.2"/><text x="387" y="195.5" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#FFF">h₄</text>
          <circle cx="387" cy="215" r="2.2" fill="#B06000"/><circle cx="387" cy="223" r="2.2" fill="#B06000"/><circle cx="387" cy="231" r="2.2" fill="#B06000"/>
          <circle cx="387" cy="252" r="13" fill="#FBBC04" stroke="#FFF" stroke-width="2.2"/><text x="387" y="255.5" text-anchor="middle" font-family="Roboto Mono" font-size="9" font-weight="700" fill="#202124">h₁₂₈</text>
          <text x="387" y="282" text-anchor="middle" font-family="Roboto" font-size="10" font-weight="700" fill="#B06000">W₁·x + b₁ → ReLU</text>

          <!-- Output nodes (compact 5 nodes centered vertically) -->
          <circle cx="635" cy="124" r="10.5" fill="#34A853" stroke="#FFF" stroke-width="2"/><text x="656" y="128" font-family="Poppins" font-size="11" font-weight="700" fill="#202124">Anna</text>
          <circle cx="635" cy="152" r="10.5" fill="#34A853" stroke="#FFF" stroke-width="2"/><text x="656" y="156" font-family="Poppins" font-size="11.2" font-weight="700" fill="#137333">Elsa ★</text>
          <circle cx="635" cy="180" r="10.5" fill="#34A853" stroke="#FFF" stroke-width="2"/><text x="656" y="184" font-family="Poppins" font-size="11" font-weight="700" fill="#202124">Kristoff</text>
          <circle cx="635" cy="208" r="10.5" fill="#34A853" stroke="#FFF" stroke-width="2"/><text x="656" y="212" font-family="Poppins" font-size="11" font-weight="700" fill="#202124">Olaf</text>
          <circle cx="635" cy="236" r="10.5" fill="#34A853" stroke="#FFF" stroke-width="2"/><text x="656" y="240" font-family="Poppins" font-size="11" font-weight="700" fill="#202124">Sven</text>

          <!-- Labels on weights -->
          <rect x="208" y="278" width="62" height="22" rx="6" fill="#FFFFFF" stroke="#DADCE0"/>
          <text x="239" y="293" text-anchor="middle" font-family="Roboto Mono" font-size="10.8" font-weight="700" fill="#EA4335">W₁, b₁</text>
          <rect x="504" y="258" width="62" height="22" rx="6" fill="#FFFFFF" stroke="#DADCE0"/>
          <text x="535" y="273" text-anchor="middle" font-family="Roboto Mono" font-size="10.8" font-weight="700" fill="#137333">W₂, b₂</text>
        </svg>
      </div>
      <div class="callout" style="margin-top:8px;"><strong>Alur dari kiri ke kanan:</strong> Setiap data mengalir maju melewati perkalian bobot + bias + fungsi aktivasi. Proses maju ini disebut <strong>Forward Pass</strong>.</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 32: HITUNG PARAMETER DENGAN HIDDEN LAYER + SIMULATOR #7 -->
    <section class="slide" data-title="Bab 3D: Simulator Hitung Parameter dengan Hidden Layer" data-notes="Alokasi waktu: 1.5 menit. Momen 'aha' penting! Geser jumlah neuron di Hidden Layer dan perhatikan bagaimana total parameter pada foto 224×224×3 langsung melonjak ke 19.268.357 (sekitar 19,3 juta) saat hidden=128.">
      <div class="kicker">BAB 03 · KALKULATOR PARAMETER</div>
      <h2>Hitung Parameter dengan <span class="hl-red">Hidden Layer</span></h2>
      <div class="split-40-60">
        <div class="card surface" style="justify-content:space-between; gap:10px;">
          <div class="card-top-bar bar-red"></div>
          <div style="display:flex; flex-direction:column; gap:10px;">
            <div class="card-title">Atur Ukuran Input &amp; Hidden Layer</div>
            <div class="sim-bar pdf-keep-ui" id="hid-img-btns">
              <button class="btn-ui outline" data-hdim="64" onclick="setHidImg(64,this)" style="padding:5px 10px; font-size:11.5px;">Foto 64×64×3</button>
              <button class="btn-ui" data-hdim="224" onclick="setHidImg(224,this)" style="padding:5px 10px; font-size:11.5px;">Foto 224×224×3</button>
            </div>
            <div class="sim-slider-row"><span>Neuron Hidden</span><input id="hid-units" type="range" min="16" max="256" step="16" value="128" oninput="updateHidCalc()"/><span class="sim-val" id="hid-units-v">128</span></div>
            <div class="mini-box" id="hid-breakdown" style="font-family:var(--font-code); font-size:11.6px; line-height:1.58;"></div>
            <div class="mini-box" style="font-size:11.5px; background:#FFFFFF;">
              <strong>Bandingkan:</strong> Tanpa Hidden = <code>752.645</code> parameter. Tambah 1 Hidden Layer <code>128</code> neuron → melonjak <strong>~25× lipat</strong>!
            </div>
          </div>
          <div class="callout red" id="hid-warn"></div>
        </div>
        <div class="card tint-red" style="justify-content:center; align-items:center; text-align:center; gap:12px;">
          <div class="card-top-bar bar-red"></div>
          <div style="font-family:var(--font-title); font-size:13px; font-weight:700; color:#C5221F;">TOTAL PARAMETER (WEIGHT + BIAS)</div>
          <div class="big-num hl-red" id="hid-total" style="font-size:44px;">19.268.357</div>
          <div class="kpi-strip" style="grid-template-columns:1fr 1fr; width:100%;">
            <div class="kpi-mini" style="background:#FFFFFF;"><div class="k-num" id="hid-l1">19.267.712</div><div class="k-lbl">Layer 1 (Input → Hidden)</div></div>
            <div class="kpi-mini" style="background:#FFFFFF;"><div class="k-num" id="hid-l2" style="color:#137333;">645</div><div class="k-lbl">Layer 2 (Hidden → 5 Kelas)</div></div>
          </div>
          <div class="mini-box" style="width:100%; text-align:left;">
            <strong>Perhatikan:</strong> Lebih dari <strong>99,99%</strong> parameter menumpuk di sambungan pertama (Input → Hidden)! Ini alasan utama kenapa nanti di Bab 4 &amp; P03 kita pindah ke <strong>CNN</strong>.
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 31: FORWARD PASS MINI 4 PIKSEL NYATA + SIMULATOR #7 -->
    <section class="slide" data-title="Bab 3D: Forward Pass Langkah demi Langkah (4 Piksel Nyata)" data-notes="Alokasi waktu: 2.5 menit. Agar matematika terasa nyata dan transparan, kita jalankan Forward Pass lengkap pada 4 piksel asli foto Elsa yang di-resize ke 2x2. Klik langkah 1 sampai 4 untuk melihat angka nyata hasil eksekusi NumPy.">
      <div class="kicker">BAB 03 · FORWARD PASS</div>
      <h2><span class="hl-blue">Forward Pass</span> Langkah demi Langkah (4 Piksel Nyata Elsa)</h2>
      <div class="sim-bar pdf-keep-ui" id="fp-steps" style="margin-bottom:8px;">
        <button class="btn-ui" data-fp="1" onclick="setFpStep(1)">1. Input 4 Piksel</button>
        <button class="btn-ui outline" data-fp="2" onclick="setFpStep(2)">2. Hidden Layer + ReLU</button>
        <button class="btn-ui outline" data-fp="3" onclick="setFpStep(3)">3. Output Layer (Logits)</button>
        <button class="btn-ui outline" data-fp="4" onclick="setFpStep(4)">4. Softmax → Probabilitas</button>
      </div>
      <div class="split-40-60">
        <div class="img-box" style="height:auto; padding:12px; justify-content:center; gap:14px;">
          <img src="assets/P02/04_mini_forward_pass_pixels.png" alt="Foto Elsa asli diperkecil menjadi 2x2 (4 piksel nyata)" style="width:100%; max-height:265px; object-fit:contain;"/>
          <div class="formula-box" style="width:100%; font-size:11.6px;">x = [{x0:.2f}, {x1:.2f}, {x2:.2f}, {x3:.2f}] (nyata dari foto Elsa)</div>
        </div>
        <div class="card surface" style="justify-content:space-between; gap:10px;">
          <div class="card-top-bar bar-blue" id="fp-bar"></div>
          <div style="display:flex; flex-direction:column; gap:10px;">
            <div>
              <span class="pill blue" id="fp-pill">LANGKAH 1 / 4</span>
              <div class="card-title" id="fp-title" style="margin-top:6px;"></div>
            </div>
            <pre class="code" id="fp-math" style="margin:0; font-size:12px;"></pre>
            <div id="fp-visual"></div>
          </div>
          <div class="callout" id="fp-note"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
        )

        # 34: Q&A REVEAL #4 (FORWARD PASS)
        s.append(
            _qa_slide(
                qa_id="qa-fp",
                qa_num=4,
                kicker="BAB 03 · TANYA-JAWAB #4",
                title_html='Cek Cepat: <span class="hl-blue">Forward Pass &amp; Jumlah Parameter</span>',
                question_html="Sebuah jaringan mini punya <strong>4 neuron input</strong>, <strong>2 neuron hidden</strong>, dan <strong>2 neuron output</strong> (seperti contoh Elsa tadi). Berapa total parameter (weight + bias) pada <em>Layer 1</em> (Input → Hidden)?",
                choices=[
                    "<strong>A.</strong> 6 parameter (4 + 2)",
                    "<strong>B.</strong> 8 parameter (4 × 2, tanpa bias)",
                    "<strong>C.</strong> 10 parameter (4 × 2 weight + 2 bias)",
                ],
                answer_html="<strong>Jawaban: C (10 parameter)!</strong> Setiap 4 neuron input terhubung ke 2 neuron hidden = <code>4 × 2 = 8</code> weight, ditambah <code>2</code> bias (1 untuk setiap neuron hidden) → total <strong>10 parameter</strong>!",
                vis_q_html='<div class="formula-box" style="font-size:15px;">4 Input → 2 Hidden</div><div style="margin-top:10px; font-size:13px; color:#5F6368;">Ingat rumus: <code>(Input × Hidden) + Bias</code>. Jangan lupakan bias!</div>',
                vis_a_html='<div class="big-num hl-green">10 Parameter</div><div class="mini-box" style="margin-top:8px; background:#E6F4EA; border-color:#A8DAB5;"><strong>Rincian:</strong> <code>(4 × 2) + 2 = 10</code> di Layer 1, dan <code>(2 × 2) + 2 = 6</code> di Layer 2 → total jaringan mini = <strong>16 parameter</strong>.</div>',
                notes="Alokasi waktu: 1 menit. Minta peserta menghitung lisan 4×2+2 sebelum membuka jawaban. Setelah paham Forward Pass, kita masuk ke pertanyaan paling menarik: bagaimana bobot-bobot itu belajar?",
                bar_color="green",
            )
        )

        # 35: LOSS FUNCTION (INTUITIF)
        s.append(
            f"""
    <!-- 35: LOSS — SEBERAPA SALAH TEBAKAN -->
    <section class="slide" data-title="Bab 3E: Loss — Mengukur Seberapa Salah Tebakan AI" data-notes="Alokasi waktu: 1.5 menit. Saat model baru dibuat, semua weight masih acak sehingga tebakannya salah. Loss Function (seperti Cross-Entropy) memberi skor hukuman: makin salah dan makin yakin, makin besar nilai Loss-nya.">
      <div class="kicker">BAB 03 · LOSS FUNCTION</div>
      <h2><span class="hl-red">Loss Function</span>: Mengukur Seberapa Salah Tebakan AI</h2>
      <div class="img-box" style="height:auto; flex:1; min-height:0; padding:6px;">
        <img src="assets/P02/05_loss_gradient_descent_overview.png" alt="Grafik Cross-Entropy Loss dan intuisi Gradient Descent" style="width:100%; height:100%; max-height:340px; object-fit:contain;"/>
      </div>
      <div class="grid-2" style="flex:0 0 auto; margin-top:8px;">
        <div class="callout red"><strong>Panel Kiri (Loss):</strong> Jika foto asli Elsa hanya diberi peluang <code>10%</code>, hukumannya berat (<code>Loss = 2.30</code>). Jika diberi <code>90%</code>, <code>Loss = 0.11</code> (kecil = bagus!).</div>
        <div class="callout"><strong>Panel Kanan (Gradient Descent):</strong> Tujuan proses belajar adalah menggeser nilai <em>weight</em> turun menyusuri kurva sampai ke <strong>dasar lembah Loss terkecil</strong>.</div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 36: GRADIENT DESCENT + SIMULATOR #9 -->
    <section class="slide" data-title="Bab 3E: Gradient Descent &amp; Simulator Learning Rate" data-notes="Alokasi waktu: 1.5 menit. Gradient Descent ibarat menuruni bukit berkabut dengan melangkah ke arah paling miring ke bawah. Besar langkahnya disebut Learning Rate. Klik 3 preset (Kecil, Ideal, Besar) untuk melihat dampaknya.">
      <div class="kicker">BAB 03 · GRADIENT DESCENT</div>
      <h2><span class="hl-blue">Gradient Descent</span>: Turun Bukit &amp; Peran <em>Learning Rate</em></h2>
      <div class="sim-bar pdf-keep-ui" id="gd-presets" style="margin-bottom:8px;">
        <button class="btn-ui outline" data-gd="small" onclick="setGdMode('small')">1. Learning Rate Kecil (0.03)</button>
        <button class="btn-ui" data-gd="ideal" onclick="setGdMode('ideal')">2. Learning Rate Ideal (0.20)</button>
        <button class="btn-ui outline" data-gd="large" onclick="setGdMode('large')">3. Learning Rate Besar (1.06)</button>
      </div>
      <div class="split-60-40">
        <div class="canvas-box" style="justify-content:center;">
          <canvas id="gd-canvas" width="560" height="310"></canvas>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div>
            <div class="card-title" id="gd-title">LR Ideal — Turun Mulus</div>
            <div class="formula-box" style="margin-top:8px; font-size:12px;">w_baru = w_lama − (Learning Rate × Kemiringan)</div>
          </div>
          <div class="kpi-strip" style="grid-template-columns:1fr 1fr;">
            <div class="kpi-mini"><div class="k-num" id="gd-end-w">-0.05</div><div class="k-lbl">Posisi w (Langkah 8)</div></div>
            <div class="kpi-mini"><div class="k-num" id="gd-end-loss" style="color:#137333;">0.002</div><div class="k-lbl">Nilai Loss Akhir</div></div>
          </div>
          <div id="gd-note" class="callout green"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 35: BACKPROPAGATION SEKILAS -->
    <section class="slide" data-title="Bab 3E: Backpropagation Sekilas (Tanpa Turunan Rumit)" data-notes="Alokasi waktu: 1.5 menit. Pertanyaan wajar: kalau ada jutaan weight di banyak layer, bagaimana tahu weight mana yang harus dinaikkan atau diturunkan? Itulah tugas Backpropagation — dan kabar baiknya dihitung otomatis oleh TensorFlow/Keras!">
      <div class="kicker">BAB 03 · BACKPROPAGATION</div>
      <h2><span class="hl-red">Backpropagation</span>: Menghitung Arah Koreksi Secara Otomatis</h2>
      <div class="card surface" style="flex:1; justify-content:space-between; gap:12px; padding:16px 20px;">
        <div class="card-top-bar bar-red"></div>
        <svg viewBox="0 0 780 185" style="width:100%; max-height:195px;">
          <rect x="20" y="54" width="120" height="72" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.2"/>
          <text x="80" y="86" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#1A73E8">Input Foto</text>
          <text x="80" y="105" text-anchor="middle" font-family="Roboto" font-size="11" fill="#5F6368">(Elsa)</text>

          <rect x="205" y="54" width="140" height="72" rx="12" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2.2"/>
          <text x="275" y="86" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#B06000">Hidden Layer</text>
          <text x="275" y="105" text-anchor="middle" font-family="Roboto Mono" font-size="11" fill="#5F6368">Weight W₁, b₁</text>

          <rect x="410" y="54" width="145" height="72" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="2.2"/>
          <text x="482" y="86" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#137333">Output Layer</text>
          <text x="482" y="105" text-anchor="middle" font-family="Roboto Mono" font-size="11" fill="#5F6368">Weight W₂, b₂</text>

          <rect x="620" y="54" width="140" height="72" rx="12" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.2"/>
          <text x="690" y="86" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#C5221F">Nilai Loss</text>
          <text x="690" y="105" text-anchor="middle" font-family="Roboto" font-size="11" fill="#C5221F">Tebakan vs Asli</text>

          <!-- Forward arrows (top, blue) -->
          <path d="M140 72 L202 72" stroke="#1A73E8" stroke-width="3"/><polygon points="200,66 210,72 200,78" fill="#1A73E8"/>
          <path d="M345 72 L407 72" stroke="#1A73E8" stroke-width="3"/><polygon points="405,66 415,72 405,78" fill="#1A73E8"/>
          <path d="M555 72 L617 72" stroke="#1A73E8" stroke-width="3"/><polygon points="615,66 625,72 615,78" fill="#1A73E8"/>
          <text x="390" y="34" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#1A73E8">1. FORWARD PASS (Maju): Foto masuk → keluar prediksi → hitung Loss</text>

          <!-- Backward arrows (bottom, red dashed) -->
          <path d="M620 112 L558 112" stroke="#EA4335" stroke-width="3" stroke-dasharray="6,4"/><polygon points="560,106 550,112 560,118" fill="#EA4335"/>
          <path d="M410 112 L348 112" stroke="#EA4335" stroke-width="3" stroke-dasharray="6,4"/><polygon points="350,106 340,112 350,118" fill="#EA4335"/>
          <path d="M205 112 L143 112" stroke="#EA4335" stroke-width="3" stroke-dasharray="6,4"/><polygon points="145,106 135,112 145,118" fill="#EA4335"/>
          <text x="390" y="162" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#C5221F">2. BACKPROPAGATION (Mundur): Bagikan umpan balik koreksi ke W₂ lalu W₁</text>
        </svg>
        <div class="grid-3" style="flex:0 0 auto; gap:12px;">
          <div class="mini-box" style="background:#FFFFFF; border-color:#F6AEA9;">
            <strong style="color:#C5221F;">1. Ukur Kesalahan di Ujung</strong><br/>
            Bandingkan tebakan dengan label asli → dapatkan angka <em>Loss</em>.
          </div>
          <div class="mini-box" style="background:#FFFFFF; border-color:#FDE293;">
            <strong style="color:#B06000;">2. Lacak Mundur (Backprop)</strong><br/>
            Hitung kontribusi salah tiap bobot dari belakang (<code>W₂</code>) ke depan (<code>W₁</code>).
          </div>
          <div class="mini-box" style="background:#FFFFFF; border-color:#C6DAFC;">
            <strong style="color:#1A73E8;">3. Geser Bobot (Gradient Descent)</strong><br/>
            Setiap bobot digeser sedikit ke arah yang menurunkan <em>Loss</em>.
          </div>
        </div>
        <div class="callout green"><strong>Kabar baik untuk pemula:</strong> Kamu <em>tidak</em> perlu menghitung turunan kalkulus secara manual. Ketika memanggil <code>model.fit()</code> di Keras, TensorFlow menghitung <strong>Backpropagation</strong> &amp; memperbarui seluruh bobot secara otomatis!</div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 38: SATU SIKLUS TRAINING (EPOCH) -->
    <section class="slide" data-title="Bab 3E: Satu Siklus Training &amp; Epoch" data-notes="Alokasi waktu: 1 menit. Gabungkan keempat langkah belajar menjadi 1 siklus utuh yang terus berulang setiap Epoch sampai nilai Loss turun dan stabil.">
      <div class="kicker">BAB 03 · SIKLUS TRAINING &amp; EPOCH</div>
      <h2>Satu Siklus Training: <span class="hl-green">Tebak → Ukur → Koreksi → Ulangi</span></h2>
      <div class="grid-4" style="flex:0 0 auto; margin-bottom:12px;">
        <div class="card tint-blue" style="padding:14px;">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">01 · TEBAK</span>
          <div class="card-title" style="font-size:15px;">Forward Pass</div>
          <div class="card-body" style="font-size:12.5px;">Foto masuk → hitung tiap layer → keluar probabilitas Softmax.</div>
        </div>
        <div class="card tint-red" style="padding:14px;">
          <div class="card-top-bar bar-red"></div>
          <span class="pill red">02 · UKUR</span>
          <div class="card-title" style="font-size:15px;">Hitung Loss</div>
          <div class="card-body" style="font-size:12.5px;">Bandingkan probabilitas tebakan dengan label asli foto.</div>
        </div>
        <div class="card tint-yellow" style="padding:14px;">
          <div class="card-top-bar bar-yellow"></div>
          <span class="pill yellow">03 · KOREKSI</span>
          <div class="card-title" style="font-size:15px;">Backprop + GD</div>
          <div class="card-body" style="font-size:12.5px;">Hitung arah salah &amp; geser seluruh weight sedikit demi sedikit.</div>
        </div>
        <div class="card tint-green" style="padding:14px;">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">04 · ULANGI</span>
          <div class="card-title" style="font-size:15px;">Epoch</div>
          <div class="card-body" style="font-size:12.5px;">1 putaran penuh membaca seluruh data latih = <strong>1 Epoch</strong>.</div>
        </div>
      </div>
      <div class="card surface" style="flex:1; justify-content:center; gap:12px;">
        <div class="card-top-bar bar-green"></div>
        <div class="card-title">Apa yang Diharapkan Saat <code>model.fit(epochs=...)</code> Berjalan?</div>
        <div class="card-body">
          <ul>
            <li><strong>Epoch awal:</strong> Bobot masih acak → <em>Loss</em> tinggi, tebakan sering salah.</li>
            <li><strong>Epoch berjalan:</strong> Setiap paket foto (<em>batch</em>) mengoreksi bobot → <em>Loss</em> perlahan <strong>turun</strong>.</li>
            <li><strong>Detail lanjutan di P03:</strong> Kita akan membedah kurva <em>Train vs Validation Loss</em>, <em>Overfitting</em>, dan perbandingan <em>Learning Rate</em> lebih dalam di P03.</li>
          </ul>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 39: RANGKUMAN BAB 3 (PETA TERKECIL -> TERBESAR) -->
    <section class="slide" data-title="Bab 3: Rangkuman Peta Terkecil → Terbesar" data-notes="Alokasi waktu: 1 menit. Kunci seluruh Bab 3 dalam satu tangga hierarki: dari 1 piksel dan 1 neuron, naik ke layer, menjadi Neural Network utuh, lalu dilatih lewat siklus training.">
      <div class="kicker">BAB 03 · RANGKUMAN</div>
      <h2>Peta Utuh: Dari <span class="hl-blue">Bagian Terkecil</span> ke <span class="hl-green">Neural Network</span></h2>
      <div class="step-list">
        <div class="step-item"><div class="step-num">1</div><div><div class="step-title">Piksel &amp; 1 Neuron (Unit Terkecil)</div><div class="step-desc">1 neuron menghitung <code>(input × weight) + bias</code> lalu melewati aktivasi <code>ReLU</code>.</div></div></div>
        <div class="step-item"><div class="step-num blue">2</div><div><div class="step-title">Input Layer &amp; Output Layer</div><div class="step-desc">Neuron <strong>Input Layer</strong> = <code>Tinggi × Lebar × Channel</code> (mis. <code>150.528</code>); Neuron <strong>Output Layer</strong> = jumlah kelas (<code>5</code> + <code>Softmax</code>).</div></div></div>
        <div class="step-item"><div class="step-num yellow">3</div><div><div class="step-title">Hidden Layer (Pengolah Pola Bertahap)</div><div class="step-desc">Lapisan tengah yang menghubungkan input ke output agar jaringan bisa belajar pola non-linear yang kompleks.</div></div></div>
        <div class="step-item"><div class="step-num red">4</div><div><div class="step-title">Forward Pass (Menghitung Tebakan)</div><div class="step-desc">Aliran angka maju dari foto → Input → Hidden → Output → probabilitas 5 karakter.</div></div></div>
        <div class="step-item"><div class="step-num green">5</div><div><div class="step-title">Training Loop (Belajar Otomatis)</div><div class="step-desc">Hitung <strong>Loss</strong> → <strong>Backpropagation</strong> → update bobot dengan <strong>Gradient Descent</strong> berulang selama beberapa <strong>Epoch</strong>.</div></div></div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
        )

        # 40: Q&A REVEAL #5 (BAB 3)
        s.append(
            _qa_slide(
                qa_id="qa-bab3",
                qa_num=5,
                kicker="BAB 03 · TANYA-JAWAB #5",
                title_html='Cek Pemahaman Bab 3: <span class="hl-green">Bagaimana Model Belajar?</span>',
                question_html="Saat melatih Neural Network di Keras, kita melihat nilai <strong>Loss</strong> perlahan turun dari <code>1.65</code> menjadi <code>0.35</code> seiring bertambahnya <strong>Epoch</strong>. Apa artinya?",
                choices=[
                    "<strong>A.</strong> Model makin bingung karena angkanya makin kecil",
                    "<strong>B.</strong> Bobot (<em>weight</em> &amp; <em>bias</em>) berhasil dikoreksi oleh Gradient Descent sehingga tebakan model pada data latih makin mendekati label asli",
                    "<strong>C.</strong> Jumlah neuron di Input Layer berkurang otomatis tiap epoch",
                ],
                answer_html="<strong>Jawaban: B!</strong> Nilai <strong>Loss</strong> mengukur besar kesalahan — makin kecil Loss, makin dekat prediksi model ke jawaban benar. Jumlah neuron tidak berubah; yang berubah setiap langkah training adalah nilai angka <em>weight</em> dan <em>bias</em>.",
                vis_q_html='<div class="big-num hl-red">1.65 → 0.35</div><div style="margin-top:8px; font-size:13.5px; color:#5F6368;">Nilai Loss turun seiring Epoch berjalan — kabar baik atau kabar buruk?</div>',
                vis_a_html='<div class="big-num hl-green">Kabar Baik!</div><div class="mini-box" style="margin-top:8px; background:#E6F4EA; border-color:#A8DAB5;"><strong>Loss Menurun = Belajar!</strong> Artinya optimizer (Gradient Descent / Adam) berhasil menuntun bobot turun menuju dasar lembah error.</div>',
                notes="Alokasi waktu: 1 menit. Menutup Bab 3 dengan mengecek pemahaman arah nilai Loss. Setelah ini kita masuk ke Bab 4 (Teaser Arsitektur CV).",
                bar_color="green",
            )
        )

    if not HIDE_BAB4_ARCH:
        # =========================================================================
        # BAB 4: ARSITEKTUR NEURAL NETWORK UNTUK COMPUTER VISION (SLIDE 41–45 · 6.0M)
        # =========================================================================
        s.append(
            make_divider_slide(
                bg_class="bg-yellow",
                kicker="BAB 04 · TEASER ARSITEKTUR MODERN",
                title="Arsitektur Neural Network untuk Computer Vision",
                description="Mengapa MLP biasa kewalahan menangani foto, dan bagaimana keluarga CNN berevolusi dari LeNet sampai MobileNetV2.",
                footer_label=FOOTER,
                data_title="Bab 4 — Arsitektur CV (Teaser)",
                notes="Alokasi waktu: 0.5 menit. Bab 4 bersifat teaser konseptual agar peserta tahu peta arsitektur CV tanpa harus paham rumus konvolusi dulu (detail konvolusi di P03, detail arsitektur & transfer learning di P04).",
            )
        )

        # 42: MENGAPA MLP TIDAK CUKUP
        s.append(
            f"""
        <!-- 42: MENGAPA MLP TIDAK CUKUP UNTUK GAMBAR -->
        <section class="slide" data-title="Bab 4: Mengapa MLP Tidak Cukup untuk Gambar?" data-notes="Alokasi waktu: {"2.5" if HIDE_SLIDES_28_40 else "1.5"} menit. Tunjukkan dua alasan kuat dari hasil Bab 3 tadi: (1) ledakan 19,27 juta parameter di 1 layer saja, dan (2) Flatten merusak tetangga piksel 2D sehingga sangat peka jika objek bergeser sedikit.">
          <div class="kicker">BAB 04 · BATASAN MLP PADA FOTO</div>
          <h2>Mengapa <span class="hl-red">MLP Biasa</span> Tidak Cukup untuk Gambar?</h2>
          <div class="img-box" style="height:auto; flex:1; min-height:0; padding:7px;">
            <img src="assets/P02/06_mlp_vs_cnn_preview.png" alt="Perbandingan MLP Flatten 1D vs CNN Filter 2D pada foto Elsa" style="width:100%; height:100%; max-height:345px; object-fit:contain;"/>
          </div>
          <div class="grid-2" style="flex:0 0 auto; margin-top:8px;">
            <div class="callout red"><strong>Masalah 1 — Boros Parameter:</strong> Foto <code>224×224×3</code> → <code>Dense(128)</code> langsung butuh <strong>19,27 juta parameter</strong> padahal dataset v1 kita baru {total_imgs} foto!</div>
            <div class="callout green"><strong>Masalah 2 — Peka Posisi:</strong> <em>Flatten</em> memutus tetangga atas-bawah. <strong>CNN</strong> (P03) memakai filter kecil <code>3×3</code> yang bergeser di gambar 2D utuh!</div>
          </div>
          <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
        </section>

        <!-- 43: PETA ARSITEKTUR + SIMULATOR #10 -->
        <section class="slide" data-title="Bab 4: Peta Evolusi Arsitektur CV (Simulator)" data-notes="Alokasi waktu: {"2.5" if HIDE_SLIDES_28_40 else "2"} menit. Klik keempat kartu secara berurutan (MLP -> CNN -> ResNet -> MobileNet) untuk menjelaskan ide inti tiap generasi secara konseptual tanpa detail internal yang berat. Detailnya akan dipelajari di P03 dan P04.">
          <div class="kicker">BAB 04 · EVOLUSI ARSITEKTUR</div>
          <h2>Evolusi Arsitektur CV: <span class="hl-blue">MLP → CNN → ResNet → MobileNet</span></h2>
          <div class="sim-bar pdf-keep-ui" id="arch-tabs" style="margin-bottom:10px;">
            <button class="btn-ui outline" data-arch="mlp" onclick="setArchTab('mlp')">1. MLP (Fully Connected)</button>
            <button class="btn-ui outline" data-arch="cnn" onclick="setArchTab('cnn')">2. CNN (LeNet / VGG)</button>
            <button class="btn-ui outline" data-arch="resnet" onclick="setArchTab('resnet')">3. ResNet (Skip Connection)</button>
            <button class="btn-ui" data-arch="mobilenet" onclick="setArchTab('mobilenet')">4. MobileNetV2 ★ Proyek Kita</button>
          </div>
          <div class="split-60-40">
            <div class="card surface" style="justify-content:space-between;">
              <div class="card-top-bar bar-green" id="arch-bar"></div>
              <div>
                <span class="pill green" id="arch-pill">MOBILENETV2 · RINGAN &amp; CEPAT</span>
                <div class="card-title" id="arch-title" style="margin-top:8px;">Dirancang Ringan untuk HP &amp; Dataset Kecil</div>
              </div>
              <div class="card-body" id="arch-body" style="font-size:13.6px;"></div>
              <div class="callout green" id="arch-callout"></div>
            </div>
            <div class="card" style="justify-content:space-between;">
              <div class="card-top-bar bar-blue"></div>
              <div class="card-title">Ringkasan Perbandingan Cepat</div>
              <table class="io-table" style="font-size:12px;">
                <thead><tr><th>Keluarga</th><th>Ide Inti</th><th>Status di Kelas</th></tr></thead>
                <tbody>
                  <tr><td><strong>MLP</strong></td><td>Semua piksel disambung penuh</td><td>Praktik hari ini (P02)</td></tr>
                  <tr><td><strong>CNN Dasar</strong></td><td>Filter 2D geser + hemat bobot</td><td>Bedah tuntas di P03</td></tr>
                  <tr><td><strong>ResNet</strong></td><td><em>Skip Connection</em> agar bisa sangat dalam</td><td>Dibahas di P04</td></tr>
                  <tr style="background:var(--tint-green);"><td><strong>MobileNetV2</strong></td><td>Konvolusi ringan + <em>Transfer Learning</em></td><td><strong>Model Proyek P04–P08!</strong></td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
        </section>

        <!-- 44: ARSITEKTUR PER TASK & PILIHAN PROYEK -->
        <section class="slide" data-title="Bab 4: Arsitektur per Task CV &amp; Pilihan MobileNetV2" data-notes="Alokasi waktu: {"1.5" if HIDE_SLIDES_28_40 else "1"} menit. Hubungkan Bab 2 (4 Task CV) dengan Bab 4 (Arsitektur): tiap task punya keluarga arsitektur populer, tetapi semuanya sering memakai CNN backbone yang mirip! Untuk proyek kita dipilih MobileNetV2.">
          <div class="kicker">BAB 04 · MENGHUBUNGKAN TASK &amp; ARSITEKTUR</div>
          <h2>Arsitektur Populer per Task &amp; <span class="hl-green">Pilihan Proyek Kita</span></h2>
          <div class="grid-3" style="margin-bottom:10px;">
            <div class="card tint-blue">
              <div class="card-top-bar bar-blue"></div>
              <span class="pill blue">CLASSIFICATION</span>
              <div class="card-title">ResNet · MobileNetV2 · EfficientNet</div>
              <div class="card-body" style="font-size:13px;">Fokus mengekstrak fitur gambar lalu mengakhiri jaringan dengan <code>Dense + Softmax</code> untuk menebak label kelas.</div>
            </div>
            <div class="card tint-red">
              <div class="card-top-bar bar-red"></div>
              <span class="pill red">OBJECT DETECTION</span>
              <div class="card-title">YOLO · SSD · Faster R-CNN</div>
              <div class="card-body" style="font-size:13px;">Memakai <em>CNN backbone</em> untuk mengekstrak fitur, lalu menambahkan <em>detection head</em> untuk memprediksi <em>bounding box</em>.</div>
            </div>
            <div class="card tint-green">
              <div class="card-top-bar bar-green"></div>
              <span class="pill green">SEGMENTATION</span>
              <div class="card-title">U-Net · Mask R-CNN</div>
              <div class="card-body" style="font-size:13px;">Mengekstrak fitur lalu membesarkannya kembali agar bisa memberi label piksel demi piksel (<em>mask</em>).</div>
            </div>
          </div>
          <div class="callout green"><strong>Mengapa proyek Frozen kita memilih MobileNetV2?</strong> (1) Ringan &amp; cepat dilatih di Google Colab gratis, (2) sudah punya bobot terlatih dari jutaan gambar ImageNet (<em>Transfer Learning</em> di P04), dan (3) cocok untuk dataset berukuran kecil–menengah.</div>
          <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
        </section>
    """
        )

        # 45: Q&A REVEAL #6 (atau #4 saat Slide 28–40 disembunyikan) (BAB 4)
        s.append(
            _qa_slide(
                qa_id="qa-bab4",
                qa_num=4 if HIDE_SLIDES_28_40 else 6,
                kicker="BAB 04 · TANYA-JAWAB #4" if HIDE_SLIDES_28_40 else "BAB 04 · TANYA-JAWAB #6",
                title_html='Jembatan ke P03: <span class="hl-yellow">Kenapa Kita Pindah dari MLP ke CNN?</span>',
                question_html="Di Hands-On sebentar lagi kita akan mencoba membangun <strong>MLP kecil</strong> di Keras. Mengapa untuk model akhir proyek Frozen kita tidak memakai MLP saja, melainkan berpindah ke <strong>CNN (MobileNetV2)</strong>?",
                choices=[
                    "<strong>A.</strong> Karena MLP tidak bisa memakai fungsi aktivasi ReLU atau Softmax",
                    "<strong>B.</strong> Karena MLP merusak struktur 2D lewat Flatten dan meledakkan jumlah parameter hingga jutaan",
                    "<strong>C.</strong> Karena Keras tidak mendukung MLP untuk gambar berwarna RGB",
                ],
                answer_html="<strong>Jawaban: B!</strong> MLP tetap memakai ReLU dan Softmax (bahkan bagian ujung CNN juga memakai <code>Dense + Softmax</code>!). Namun untuk membaca piksel gambar, <strong>CNN</strong> jauh lebih unggul karena menjaga bentuk 2D dan sangat hemat parameter.",
                vis_q_html='<div class="big-num hl-red">19,27 Juta</div><div style="margin-top:8px; font-size:13px; color:#5F6368;">Parameter 1 layer MLP pada foto 224×224×3 — apa solusi utamanya?</div>',
                vis_a_html='<div class="big-num hl-green">CNN (P03)!</div><div class="mini-box" style="margin-top:8px; background:#E6F4EA; border-color:#A8DAB5;"><strong>P02 → P03:</strong> Hari ini kita praktik MLP kecil agar paham fondasi layer &amp; parameter. Pertemuan berikutnya kita bedah konvolusi CNN!</div>',
                notes="Alokasi waktu: 1 menit. Menutup seluruh sesi teori Bab 1–4. Setelah ini peserta istirahat 5 menit sebelum masuk ke Hands-On Notebook.",
                bar_color="yellow",
            )
        )


    # =========================================================================
    # POST-BAB 3: COVER KUIS/KAMUS/REF -> KUIS -> KAMUS -> REFERENSI -> COVER HANDS-ON -> HANDS-ON 1-6 -> 3 POIN UTAMA
    # (Saat HIDE_BAB4_ARCH=True: 100% selaras model 1-Layer Bab 1-3, ZERO istilah Hidden Layer/MLP)
    # =========================================================================
    _eval_cover_slide = f"""
    <!-- COVER EVALUASI & SUMBER BELAJAR -->
    <section class="slide bg-yellow" data-title="Cover — Kuis, Kamus &amp; Referensi" data-notes="Alokasi waktu: 0.5 menit. Cover pembuka sesi evaluasi singkat setelah Bab 3: kita mulai dari Kuis 5 Soal interaktif, lanjut Kamus 14 Istilah Kunci, dan daftar Referensi Materi Bab 1–3.">
      <svg viewBox="0 0 960 540" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:0;">
        <circle cx="855" cy="110" r="78" fill="none" stroke="rgba(32,33,36,0.10)" stroke-width="18"/>
        <circle cx="855" cy="110" r="42" fill="rgba(255,255,255,0.22)"/>
        <rect x="700" y="340" width="96" height="96" rx="22" transform="rotate(14 748 388)" fill="rgba(32,33,36,0.07)"/>
        <rect x="822" y="310" width="54" height="54" rx="14" transform="rotate(-12 849 337)" fill="rgba(255,255,255,0.26)"/>
      </svg>
      <div class="divider-center" style="position:relative; z-index:1;">
        <div class="kicker">EVALUASI &amp; SUMBER BELAJAR</div>
        <h1>Kuis, Kamus Istilah &amp; Referensi Materi</h1>
        <p>Uji cepat pemahaman Bab 1–3 lewat 5 soal interaktif, rangkum 14 istilah kunci Teori Neural Network, dan simpan tautan belajar mandiri.</p>
        <div class="cover-roadmap">
          <div class="cover-chip">
            <span class="cover-chip-num">1</span>
            <div>
              <div class="cover-chip-ttl">Kuis Interaktif 5 Soal</div>
              <div class="cover-chip-sub">Cek langsung skor (5 menit)</div>
            </div>
          </div>
          <div class="cover-chip">
            <span class="cover-chip-num">2</span>
            <div>
              <div class="cover-chip-ttl">Kamus 14 Istilah Kunci</div>
              <div class="cover-chip-sub">Peta ringkas Bab 1–3 (2 menit)</div>
            </div>
          </div>
          <div class="cover-chip">
            <span class="cover-chip-num">3</span>
            <div>
              <div class="cover-chip-ttl">12 Referensi Materi</div>
              <div class="cover-chip-sub">Rujukan lengkap Bab 1, 2 &amp; 3</div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""

    _break_slide = (
        f"""
    <!-- COVER HANDS-ON (VISUAL-FIRST · MIKRO-TASK TAHAP 1-5) -->
    <section class="slide bg-blue" data-title="Cover — Hands-On Praktik Neural Network" data-notes="Alokasi waktu: 1 menit. Cover pembuka sesi praktik Hands-On Visual-First. Ajak peserta membuka materials/P02/p02_teori_neural_network.ipynb di Google Colab atau Jupyter lokal. Jelaskan bahwa kode grafik sudah dirapikan ke Alat Visualisasi sehingga setiap tugas cuma 3–6 baris dan langsung memunculkan gambar nyata!">
      <svg viewBox="0 0 960 540" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:0;">
        <circle cx="848" cy="116" r="82" fill="none" stroke="rgba(255,255,255,0.14)" stroke-width="18"/>
        <circle cx="848" cy="116" r="44" fill="rgba(255,255,255,0.10)"/>
        <rect x="740" y="348" width="110" height="70" rx="16" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.20)" stroke-width="2"/>
        <circle cx="760" cy="364" r="4" fill="rgba(255,255,255,0.5)"/>
        <circle cx="774" cy="364" r="4" fill="rgba(255,255,255,0.5)"/>
        <circle cx="788" cy="364" r="4" fill="rgba(255,255,255,0.5)"/>
      </svg>
      <div class="divider-center" style="position:relative; z-index:1;">
        <div class="kicker">SESI PRAKTIK VISUAL-FIRST · NOTEBOOK P02</div>
        <h1>Hands-On: Praktik Neural Network</h1>
        <p>Ikuti perjalanan 1 foto asli Elsa melewati <strong>Tahap 1 → Tahap 5 Bab 3</strong>! Setiap tugas dipecah super kecil (<strong>3–6 baris kode</strong>) dan langsung menampilkan <strong>output visual nyata</strong>.</p>
        <div class="cover-roadmap-3x2">
          <div class="cover-chip"><span class="cover-chip-num">1</span><div><div class="cover-chip-ttl">1. Piksel Foto</div><div class="cover-chip-sub">1.1 Grid 8×8 · 1.2 RGB</div></div></div>
          <div class="cover-chip"><span class="cover-chip-num">2</span><div><div class="cover-chip-ttl">2. Flatten (Input)</div><div class="cover-chip-sub">2.1 Pita 1D · 2.2 Skala</div></div></div>
          <div class="cover-chip"><span class="cover-chip-num">3</span><div><div class="cover-chip-ttl">Tahap 3 · Neuron</div><div class="cover-chip-sub">3.1 z · 3.2 ReLU · 3.3 Softmax</div></div></div>
          <div class="cover-chip"><span class="cover-chip-num">4</span><div><div class="cover-chip-ttl">Tahap 4 · Model</div><div class="cover-chip-sub">4.1–4.3 Model Bayi E0</div></div></div>
          <div class="cover-chip"><span class="cover-chip-num">5</span><div><div class="cover-chip-ttl">Tahap 5 · Training</div><div class="cover-chip-sub">5.1 Fit · 5.2 Kurva Loss</div></div></div>
          <div class="cover-chip"><span class="cover-chip-num">6</span><div><div class="cover-chip-ttl">Tahap 5.3–5.4</div><div class="cover-chip-sub">Before/After &amp; Bobot ΔW</div></div></div>
        </div>
        <div class="cover-env-strip">📓 p02_teori_neural_network.ipynb &nbsp;·&nbsp; 📁 data/frozen_v1/ ({total_imgs} foto) &nbsp;·&nbsp; 🎨 1 Sel = 1 Visual Nyata</div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
        if HIDE_BAB4_ARCH
        else make_divider_slide(
            bg_class="bg-blue",
            kicker="BAB 05 · ISTIRAHAT &amp; HANDS-ON",
            title="Istirahat 5 Menit",
            description="Minum air, regangkan mata & tangan sejenak. Setelah jeda, kita buka notebook p02_teori_neural_network.ipynb dan praktik 6 langkah santai pada foto Frozen!",
            footer_label=FOOTER,
            data_title="Istirahat 5 Menit & Masuk Bab 5",
            notes="Alokasi waktu: 5 menit. Siapkan browser Google Colab atau Jupyter lokal untuk membuka materials/P02/p02_teori_neural_network.ipynb.",
        )
    )

    _handson_slides = [
        _handson_step_slide(
            step_num=1,
            stage_badge="Tahap 1",
            title="Foto Menjadi Kotak Piksel &amp; Angka RGB",
            kicker="HANDS-ON · TAHAP 0 &amp; 1 (9 MENIT)" if HIDE_BAB4_ARCH else "BAB 05 · HANDS-ON",
            goal_html="Melihat sendiri 1 foto Elsa berubah menjadi grid <code>8×8</code> angka <code>0.0–1.0</code>",
            bullets_html=f"""
              <li><span class="ho-sub-tag">0.1–0.3</span><span>Tekan <code>Shift+Enter</code> pada Setup, Alat Visualisasi, &amp; galeri {total_imgs} foto Frozen <em>(0 coding!)</em>.</span></li>
              <li><span class="ho-sub-tag">1.1</span><span><strong># TODO 1 (1 baris):</strong> Normalisasi <code>foto_mini = arr_8x8 / 255.0</code> → muncul grid <code>8×8</code> kotak warna + angka!</span></li>
              <li><span class="ho-sub-tag">1.2</span><span><strong># TODO 2 (1 baris):</strong> Ambil 1 piksel gaun Elsa <code>foto_mini[4, 2]</code> → lihat batang <strong>Blue (B)</strong> paling tinggi!</span></li>
            """,
            code_snippet="""# Tahap 1.1 & 1.2: Normalisasi 8x8 lalu intip 1 piksel gaun Elsa
foto_mini = arr_8x8 / 255.0            # TODO 1 (0-255 -> 0.0-1.0)
tampilkan_piksel_grid(foto_elsa, foto_mini, pr=4, pc=2)

piksel_gaun = foto_mini[4, 2]          # TODO 2 (ambil [R, G, B])
tampilkan_zoom_piksel(foto_mini, 4, 2, piksel_gaun)""",
            output_img="assets/P02/ho_step1_pixel_grid.png",
            output_caption="Foto asli Elsa → Grid 8×8 kotak angka 0.0–1.0 → Zoom piksel gaun [4, 2] dengan kanal Biru (B) paling dominan!",
            theory_ref="Slide 20 — Dimulai dari 1 Piksel → 1 Neuron",
            checklist_html="✓ <code>foto_mini</code> bershape <code>(8, 8, 3)</code> &amp; nilai <code>0.0–1.0</code><br/>✓ Batang <strong>Blue (B = 0.60)</strong> tertinggi pada piksel gaun <code>[4, 2]</code>",
            callout_html="<strong>Tangible!</strong> Angka di kotak grid = kecerahan rata-rata; aslinya tiap kotak punya 3 angka <code>[R, G, B]</code>.",
            color="blue",
            notes=f"Alokasi waktu: {'9' if HIDE_BAB4_ARCH else '7'} menit. Jalankan Tahap 0 (Setup + Alat Visualisasi + Galeri Frozen), lalu pandu # TODO 1 (dibagi 255.0) dan # TODO 2 (ambil piksel gaun biru [4, 2]) hingga 3 gambar visual muncul!",
        ),
        _handson_step_slide(
            step_num=2,
            stage_badge="Tahap 2",
            title="Flatten Foto 2D Menjadi Pita 1D",
            kicker="HANDS-ON · TAHAP 2.1 &amp; 2.2 (9 MENIT)" if HIDE_BAB4_ARCH else "BAB 05 · HANDS-ON",
            goal_html="Meluruskan kotak <code>8×8</code> menjadi 1 pita warna 1D &amp; menghitung skala <code>752.645</code>",
            bullets_html="""
              <li><span class="ho-sub-tag green">2.1</span><span><strong># TODO 3 (1 baris):</strong> Panggil <code>vektor_elsa = foto_mini.flatten()</code> → lihat baris <code>B1..B8</code> berjejer jadi <strong>1 pita warna lurus</strong>!</span></li>
              <li><span class="ho-sub-tag green">2.2</span><span><strong># TODO 4 (2 baris):</strong> Hitung <code>neuron_224 = 224 * 224 * 3</code> (<code>150.528</code>) dan <code>param_224 = neuron_224 * 5 + 5</code> (<code>752.645</code>).</span></li>
              <li><span class="ho-sub-tag green">Visual</span><span>Bandingkan langsung grafik tangga parameter: <code>8×8</code> (<code>965</code>) → <code>64×64</code> (<code>61.445</code>) → <code>224×224</code> (<code>752.645</code>)!</span></li>
            """,
            code_snippet="""# Tahap 2.1: Luruskan kotak 2D menjadi 1 pita warna 1D
vektor_elsa = foto_mini.flatten()       # TODO 3: (8,8,3) -> (192,)
tampilkan_visual_flatten(foto_mini, vektor_elsa)

# Tahap 2.2: Hitung skala foto penuh 224x224x3 (persis Slide 24 & 32!)
neuron_224 = IMG_SIZE * IMG_SIZE * 3    # TODO 4A -> 150.528
param_224 = neuron_224 * 5 + 5          # TODO 4B -> 752.645""",
            output_img="assets/P02/ho_step2_flatten_strip.png",
            output_caption="Atas: 8×8 (B1–B8) diluruskan jadi 64 piksel warna (P1 x1–3 .. P64 x190–192 = 192 neuron RGB). Bawah: skala parameter.",
            theory_ref="Slide 21–22 — Animasi Flatten & 150.528 Neuron Input",
            checklist_html="✓ <code>len(vektor_elsa) == 192</code> (64 piksel × 3 RGB)<br/>✓ Skala penuh: <code>150.528</code> neuron → <code>752.645</code> param (persis Slide 24 &amp; 32!)",
            callout_html="<strong>Momen Klik!</strong> Biru gaun Elsa di baris <code>B4–B5</code> tampak nyata pindah menjadi garis vertikal di tengah pita 1D!",
            color="green",
            notes=f"Alokasi waktu: {'9' if HIDE_BAB4_ARCH else '7'} menit. Pandu peserta mengerjakan # TODO 3 (.flatten()) dan sorot gambar pita warna 1D (biru gaun di B4-B5, tangan di B7-B8), lalu lanjut # TODO 4 menghitung 150.528 neuron -> 752.645 parameter.",
        ),
        _handson_step_slide(
            step_num=3,
            stage_badge="Tahap 3",
            title="Weight, Bias, ReLU &amp; Softmax",
            kicker="HANDS-ON · TAHAP 3.1, 3.2 &amp; 3.3 (9 MENIT)" if HIDE_BAB4_ARCH else "BAB 05 · HANDS-ON",
            goal_html="Membuktikan 1 neuron hanyalah kali-tambah biasa, <code>ReLU</code>, &amp; <code>Softmax 100%</code>",
            bullets_html="""
              <li><span class="ho-sub-tag red">3.1</span><span><strong># TODO 5 (1 baris):</strong> Hitung <code>z = r*w_r + g*w_g + b*w_b + bias</code> pada piksel gaun Elsa <em>(tanpa <code>np.dot</code> rumit!)</em>.</span></li>
              <li><span class="ho-sub-tag red">3.2</span><span><strong># TODO 6 (1 baris):</strong> Terapkan <code>np.maximum(0.0, skor_contoh)</code> → batang minus langsung rata jadi <code>0</code>!</span></li>
              <li><span class="ho-sub-tag red">3.3</span><span><strong>Eksperimen Bebas:</strong> Ubah 1 angka (mis. <code>skor_olaf = 3.0</code>) &amp; lihat foto pemenang <code>Argmax</code> berpindah live!</span></li>
            """,
            code_snippet="""# Tahap 3.1: Hitung 1 neuron (kali-tambah biasa!)
z = (r * w_r) + (g * w_g) + (b * w_b) + bias   # TODO 5
tampilkan_timbangan_neuron(r, g, b, w_r, w_g, w_b, bias, z)

# Tahap 3.2 & 3.3: ReLU + eksperimen bebas Softmax 5 karakter
hasil_relu = np.maximum(0.0, skor_contoh)       # TODO 6
tampilkan_softmax_frozen([0.4, 2.3, 0.1, -0.2, 0.2], df_meta, DATA_DIR)""",
            output_img="assets/P02/ho_step3_neuron_relu_softmax.png",
            output_caption=f"Kiri: z Gaun ({ho_z_gaun:+.2f}) vs Dinding ({ho_z_wall:+.2f}). Tengah: ReLU (negatif → 0). Kanan: Softmax 100% + Loss ({ho_loss_sm:.2f})!",
            theory_ref="Slide 26–28 — Weight+Bias, ReLU, Softmax & Loss",
            checklist_html="✓ Gaun biru menyala (<code>z &gt; 0</code>) sementara dinding redup (<code>z &lt; 0</code>)<br/>✓ Ubah <code>skor_olaf = 3.0</code> → lihat <code>Argmax</code> pindah &amp; <code>Loss</code> melonjak!",
            callout_html="<strong>Bebas Panik Sintaks:</strong> Tanpa <code>np.dot</code> rumit — peserta langsung melihat kaitan bobot, <code>ReLU</code>, <code>Softmax</code>, &amp; <code>Loss</code>!",
            color="red",
            notes=f"Alokasi waktu: {'9' if HIDE_BAB4_ARCH else '8'} menit. Pandu # TODO 5 (kali-tambah sederhana), # TODO 6 (ReLU), lalu ajak peserta bermain di Tahap 3.3 mengganti angka skor_olaf atau skor_anna untuk melihat Softmax & foto Argmax berubah seketika!",
        ),
        _handson_step_slide(
            step_num=4,
            stage_badge="Tahap 4",
            title="Rakit Model 1-Layer &amp; Uji Model Bayi",
            kicker="HANDS-ON · TAHAP 4.1, 4.2 &amp; 4.3 (9,5 MENIT)" if HIDE_BAB4_ARCH else "BAB 05 · HANDS-ON",
            goal_html="Menyusun 2 layer Keras (<code>61.445</code> param) &amp; melihat tebakan acak <strong>Epoch 0</strong>",
            bullets_html=f"""
              <li><span class="ho-sub-tag yellow">4.1</span><span>Jalankan sel pemuat {total_imgs} foto Frozen ukuran <code>64×64×3</code> (<code>Shift+Enter</code>, siap dalam 1 detik).</span></li>
              <li><span class="ho-sub-tag yellow">4.2</span><span><strong># TODO 7 (2 baris):</strong> Lengkapi <code>Flatten()</code> &amp; <code>Dense(5, activation="softmax")</code> → cocokkan <code>61.445</code> di <code>summary()</code>!</span></li>
              <li><span class="ho-sub-tag yellow">4.3</span><span><strong>Tes "Model Bayi" (Epoch 0):</strong> Lihat sendiri bar probabilitas ~20% rata semua (<code>Loss {e0_loss:.2f}</code>, tebak acak {s_e0}/5)!</span></li>
            """,
            code_snippet="""# Tahap 4.2: Rakit Neural Network 1-Layer persis diagram Slide 24 & 32
model_nn = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(64, 64, 3)),
    tf.keras.layers.Flatten(),                        # TODO 7A
    tf.keras.layers.Dense(5, activation="softmax"),   # TODO 7B
])
# Tahap 4.3: Uji tebakan SEBELUM belajar (Epoch 0 — bobot acak!)
tampilkan_tebakan_model(model_nn, X_5foto, y_5foto)""",
            output_img="assets/P02/ho_step4_baby_model.png",
            output_caption=f"Epoch 0 (Bobot Acak): Model belum belajar — bar probabilitas ~20% merata, akurasi awal {e0_acc:.1f}% ({s_e0}/5 benar).",
            theory_ref="Slide 24 & 32 — Dense(5, Softmax) & Weight Init (S30)",
            checklist_html="✓ <code>model_nn.summary()</code> tampil tepat <strong>61.445</strong> parameter<br/>✓ Grafik Epoch 0 menunjukkan bar ~20% rata (tebak acak)",
            callout_html="<strong>Kenapa perlu Training?</strong> Melihat &ldquo;Model Bayi&rdquo; menebak acak di Epoch 0 bikin peserta langsung paham fungsi <code>model.fit()</code>!",
            color="yellow",
            notes=f"Alokasi waktu: {'9.5' if HIDE_BAB4_ARCH else '7.5'} menit. Pandu # TODO 7 (Flatten + Dense(5, softmax)) dan cocokkan angka 61.445 di model.summary(), lalu jalankan Tahap 4.3 agar peserta melihat tebakan acak Model Bayi (Epoch 0, Loss {e0_loss:.2f}).",
        ),
        _handson_step_slide(
            step_num=5,
            stage_badge="Tahap 5",
            title="Latih Model (model.fit) &amp; Kurva Loss",
            kicker="HANDS-ON · TAHAP 5.1 &amp; 5.2 (9,5 MENIT)" if HIDE_BAB4_ARCH else "BAB 05 · HANDS-ON",
            goal_html="Menjalankan siklus <strong>Backprop + Gradient Descent</strong> &amp; melihat <em>Loss</em> turun",
            bullets_html=f"""
              <li><span class="ho-sub-tag">5.1</span><span><strong># TODO 8 (1 baris):</strong> Panggil <code>model_nn.fit(X_frozen, y_frozen, epochs=EPOCHS, batch_size=16)</code> ({e_end} epoch di kelas, 2 saat smoke test).</span></li>
              <li><span class="ho-sub-tag">5.2</span><span>Jalankan <code>tampilkan_kurva_training(history)</code> → simpan grafik otomatis ke <code>results/p02_nn_loss_curve.png</code>!</span></li>
              <li><span class="ho-sub-tag">Hasil</span><span>Amati nyata: <strong>Loss turun</strong> <code>{e1_loss:.2f} → {e_end_loss:.2f}</code> &amp; <strong>Akurasi naik</strong> <code>{e0_acc:.1f}% → {e_end_acc:.1f}%</code>!</span></li>
            """,
            code_snippet="""# Tahap 5.1: Jalankan siklus Backprop & Gradient Descent otomatis!
EPOCHS = 2 if SMOKE_TEST else 20
history = model_nn.fit(                               # TODO 8
    X_frozen, y_frozen, epochs=EPOCHS, batch_size=16, verbose=1
)
# Tahap 5.2: Plot kurva Loss turun & Akurasi naik
tampilkan_kurva_training(history, simpan_ke=RESULTS_DIR / "p02_nn_loss_curve.png")""",
            output_img="assets/P02/ho_step5_loss_curve.png",
            output_caption=f"Hasil nyata 1-Layer NN pada {total_imgs} foto Frozen: Loss turun mulus ({e1_loss:.2f} → {e_end_loss:.2f}) & Akurasi naik ke {e_end_acc:.1f}%.",
            theory_ref="Slide 29–31 — Backprop, Adam, Batch Size & Epoch",
            checklist_html="✓ Kurva merah <strong>Loss</strong> turun mulus dari Epoch 1 → 20<br/>✓ File <code>results/p02_nn_loss_curve.png</code> tersimpan otomatis",
            callout_html="<strong>Ingat metodologi:</strong> Pembagian data <em>train/val/test</em> resmi bebas <em>leakage</em> (Group Split) akan dipelajari tuntas di <strong>P05</strong>.",
            color="blue",
            notes=f"Alokasi waktu: {'9.5' if HIDE_BAB4_ARCH else '7.5'} menit. Pandu # TODO 8 menjalankan model_nn.fit() selama 20 epoch (~2 detik) dan plot kurva Loss turun ({e1_loss:.2f} -> {e_end_loss:.2f}) serta Akurasi naik ke {e_end_acc:.1f}%!",
        ),
        _handson_step_slide(
            step_num=6,
            stage_badge="Tahap 5.3–5.4",
            title="Uji Tebak &amp; Peta Bobot ΔW",
            kicker="HANDS-ON · TAHAP 5.3, 5.4 &amp; BONUS (8,5 MENIT)" if HIDE_BAB4_ARCH else "BAB 05 · HANDS-ON",
            goal_html="Menguji model menebak 5 foto Frozen &amp; mengintip isi otak bobot <code>ΔW</code>",
            bullets_html=f"""
              <li><span class="ho-sub-tag green">5.3</span><span><strong>Before vs After:</strong> Bandingkan tebakan Epoch 0 ({s_e0}/5) vs Epoch {e_end} (<strong>{s_end}/5 benar ✓</strong>) pada 5 karakter Frozen!</span></li>
              <li><span class="ho-sub-tag green">5.4</span><span><strong>Intip Peta Bobot <code>ΔW</code>:</strong> Lihat area piksel terang yang paling diingat neuron Anna, Elsa, Kristoff, Olaf, &amp; Sven!</span></li>
              <li><span class="ho-sub-tag green">Bonus</span><span><em>(Opsional)</em> Ubah 1 angka <code>LEARNING_RATE_COBA = 0.01</code> lalu lihat efek langkah kebesaran pada kurva <em>Loss</em>!</span></li>
            """,
            code_snippet="""# Tahap 5.3: Uji kembali model pada 5 foto Frozen (Sesudah Belajar!)
tampilkan_tebakan_model(model_nn, X_5foto, y_5foto, judul="SESUDAH BELAJAR")

# Tahap 5.4 (Bonus Aha!): Intip area piksel yg diingat bobot ΔW
tampilkan_peta_bobot(model_nn, W_awal, X_5foto)""",
            output_img="assets/P02/ho_step6_predict_and_weights.png",
            output_caption=f"Atas: {s_end}/5 karakter tepat sesudah belajar! Bawah: peta ΔW menunjukkan area fokus tiap neuron (jembatan ke CNN P03).",
            theory_ref="Slide 31 (Overfitting) → P03 (CNN) & P05 (Split)",
            checklist_html=f"✓ Tebakan naik dari <strong>{s_e0}/5 → {s_end}/5</strong> &amp; siluet muncul di peta <code>ΔW</code><br/>✓ Cek jujur <code>polos vs ramai</code> mengungkap risiko <em>shortcut learning</em>!",
            callout_html="<strong>Momen Aha!</strong> Model 1-layer cenderung menghafal posisi piksel &amp; latar — inilah alasan kita butuh <strong>CNN (P03)</strong> &amp; <strong>Group Split (P05)</strong>!",
            color="green",
            notes=f"Alokasi waktu: {'8.5' if HIDE_BAB4_ARCH else '7'} menit. Jalankan Tahap 5.3 (Before vs After {s_e0}/5 -> {s_end}/5 benar) dan Tahap 5.4 (heatmap Fokus Bobot ΔW). Tunjuk langsung area kuning menyala di tengah heatmap sebagai jembatan alami menuju P03 (CNN)!",
        ),
    ]

    _challenge_html = ""  # Removed from active P02 deck; preserved in git history if ever needed

    # Slide 32: 2-Column Grouped Dictionary List (Bab 1-2 Left | Bab 3 Right, clickable slide jump + search + filter)
    _dict_b1 = [
        ("AI / ML / DL", "Hierarki subset: AI (bidang luas) ⊃ ML (belajar dari data) ⊃ DL (memakai Neural Network berlapis).", 8, "ai ml dl artificial intelligence machine learning deep learning hierarki"),
        ("Supervised Learning", "Model belajar dari pasangan <code>Data + Label</code>; DL otomatis menemukan pola fitur dari piksel mentah.", 7, "supervised learning fitur data label"),
    ]
    _dict_b2 = [
        ("Image Classification", "Memberi 1 label kategori dan probabilitas pada keseluruhan foto (tugas utama proyek Frozen kita).", 13, "image classification klasifikasi foto label"),
        ("Object Detection", "Mencari banyak objek sekaligus dalam 1 foto beserta kotak koordinat <em>bounding box</em> + label.", 14, "object detection bounding box deteksi"),
        ("Segmentation", "Memetakan bentuk per piksel (<em>mask</em>): <em>Semantic</em> per kelas, <em>Instance</em> memisahkan tiap individu objek.", 15, "semantic instance segmentation mask piksel"),
        ("Object Tracking", "Mendeteksi dan mempertahankan nomor ID objek yang konsisten antar-frame di dalam video.", 16, "object tracking video id frame"),
    ]
    _dict_b3 = [
        ("Input Layer &amp; Flatten", "<code>Flatten</code> meluruskan foto <code>H×W×C</code> menjadi 1 kolom vektor piksel penerima input (<code>150.528</code> neuron).", 21, "input layer flatten piksel vektor 150528"),
        ("Dense &amp; Parameter", "Lapisan <em>Fully Connected</em>: semua input tersambung ke semua output; <code>Parameter = (In×Out) + Bias</code>.", 24, "dense fully connected parameter weight bias 61445 752645"),
        ("Neuron, Weight &amp; Bias", "Unit hitung inti: tiap input dikali bobot (<code>W</code>) lalu ditambah ambang (<code>b</code>): <code>z = Σ(x·w) + b</code>.", 26, "neuron weight bias bobot ambang"),
        ("ReLU, Sigmoid/Tanh &amp; Softmax", "Aktivasi non-linear: <code>ReLU</code> (negatif→<code>0</code>), <code>Sigmoid/Tanh</code>, &amp; <code>Softmax</code> (peluang total <code>100%</code>).", 27, "relu sigmoid tanh softmax aktivasi probabilitas"),
        ("Argmax &amp; Loss Function", "<code>Argmax</code> pilih peluang tertinggi; <code>Loss (−ln P)</code> mengukur seberapa salah tebakan dari label asli.", 28, "forward pass argmax loss function error cross entropy"),
        ("Backprop &amp; Gradient Descent", "<code>Backpropagation</code> melacak sumber salah; <code>Gradient Descent</code> menggeser <code>W, b</code> menuruni bukit <em>Loss</em>.", 29, "backpropagation gradient descent training"),
        ("LR, Init &amp; Optimizer (Adam)", "<em>Weight Init</em> = mulai bobot acak; <em>Learning Rate</em> = besar langkah; <code>Adam</code> = optimizer adaptif.", 30, "learning rate weight initialization optimizer adam sgd"),
        ("Batch Size, Epoch &amp; Overfitting", "<code>Batch</code> = paket foto per update (<code>Step</code>); <code>Epoch</code> = 1 putaran penuh; <em>Overfitting</em> = hafal latar/latihan.", 31, "batch size step iteration epoch overfitting underfitting generalization"),
    ]
    def _render_dict_rows(items, ch, cls):
        return "\n            ".join(
            f'<div class="dict-row" data-ch="{ch}" data-search="{kw}">'
            f'<div class="dict-term {cls}">{term}</div>'
            f'<div class="dict-def">{defn}</div>'
            f'<button type="button" class="dict-slide-btn" onclick="jumpToSlide({snum})" title="Lompat ke Slide {snum:02d}">S{snum:02d} ↗</button>'
            f'</div>'
            for term, defn, snum, kw in items
        )
    _glossary_html = f"""
    <!-- KAMUS ISTILAH (2-COLUMN GROUPED DICTIONARY LIST + FILTER + SEARCH + SLIDE JUMP) -->
    <section class="slide" data-title="Kamus Istilah Santai P02" data-notes="Alokasi waktu: 2 menit. Ulas singkat 14 istilah asli Bab 1–3 dalam format kamus 2 kolom. Gunakan tombol filter Bab, kotak cari istilah, atau klik kode slide (S08–S29) jika peserta ingin langsung menengok ulang visualnya.">
      <div class="gloss-head-row">
        <div>
          <div class="kicker">GLOSARIUM RINGKAS · TEORI NEURAL NETWORK</div>
          <h2 style="margin-bottom:0;">Kamus Istilah <span class="hl-blue">Teori Neural Network</span></h2>
        </div>
        <div class="gloss-controls pdf-keep-ui">
          <div class="gloss-search-wrap">
            <span class="gloss-search-ico">🔍</span>
            <input type="text" id="gloss-search-inp" class="gloss-search" placeholder="Cari istilah..." oninput="searchGlossary(this.value)" />
          </div>
          <div class="gloss-filter-bar">
            <button type="button" class="gloss-fbtn active" data-ch="all" onclick="filterGlossary('all', this)">Semua (14)</button>
            <button type="button" class="gloss-fbtn" data-ch="1" onclick="filterGlossary('1', this)">Bab 1 (2)</button>
            <button type="button" class="gloss-fbtn" data-ch="2" onclick="filterGlossary('2', this)">Bab 2 (4)</button>
            <button type="button" class="gloss-fbtn" data-ch="3" onclick="filterGlossary('3', this)">Bab 3 (8)</button>
          </div>
        </div>
      </div>
      <div class="dict-grid">
        <div class="dict-col">
          <div class="dict-group">
            <div class="dict-group-head b1">
              <span>BAB 1 · AI, MACHINE LEARNING &amp; DEEP LEARNING</span>
              <span class="dict-group-cnt">2 istilah</span>
            </div>
            <div class="dict-list">
              {_render_dict_rows(_dict_b1, "1", "b1")}
            </div>
          </div>
          <div class="dict-group grow">
            <div class="dict-group-head b2">
              <span>BAB 2 · 4 TUGAS COMPUTER VISION</span>
              <span class="dict-group-cnt">4 istilah</span>
            </div>
            <div class="dict-list">
              {_render_dict_rows(_dict_b2, "2", "b2")}
            </div>
          </div>
        </div>
        <div class="dict-col">
          <div class="dict-group grow">
            <div class="dict-group-head b3">
              <span>BAB 3 · ALUR MESIN NEURAL NETWORK</span>
              <span class="dict-group-cnt">8 istilah</span>
            </div>
            <div class="dict-list">
              {_render_dict_rows(_dict_b3, "3", "b3")}
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""

    # Slides 31-35: 5 Dedicated 1-by-1 Interactive Quiz Slides (clickable A/B/C + custom question/answer visual illustrations + thorough explanations!)
    _quiz_slides = [
        _qa_slide(
            qa_id="quiz-p02-1",
            qa_num=1,
            quiz_progress_idx=1,
            data_title="Kuis 1/5 — Peta AI, ML & Deep Learning",
            kicker="EVALUASI CEPAT · KUIS 1 / 5 (BAB 1)",
            title_html='Hubungan <span class="hl-blue">AI, Machine Learning &amp; Deep Learning</span>',
            question_html="Di Bab 1 kita melihat hubungan ketiga istilah besar kecerdasan buatan. Urutan mana yang <strong>paling tepat</strong> dari bidang paling luas ke paling khusus?",
            choices=[
                "<strong>A.</strong> Machine Learning (ML) ⊃ Artificial Intelligence (AI) ⊃ Deep Learning (DL)",
                "<strong>B.</strong> Artificial Intelligence (AI) ⊃ Machine Learning (ML) ⊃ Deep Learning (DL)",
                "<strong>C.</strong> Deep Learning (DL) ⊃ Machine Learning (ML) ⊃ Artificial Intelligence (AI)",
            ],
            answer_html=(
                "<strong>Jawaban: B — AI ⊃ ML ⊃ DL!</strong><br/>"
                "• <strong>Mengapa tepat:</strong> <strong>AI</strong> adalah payung terbesar (semua mesin cerdas), <strong>ML</strong> adalah bagian AI yang belajar pola dari data, dan <strong>DL</strong> adalah cabang khusus ML yang memakai <strong>Neural Network</strong> untuk mengekstrak fitur otomatis dari piksel.<br/>"
                "• <strong>Kenapa A &amp; C keliru:</strong> AI bukan bagian kecil dari ML/DL — sistem aturan klasik (<em>if-else</em>) tetap termasuk AI walau bukan ML maupun DL."
            ),
            vis_q_html="""
              <svg viewBox="0 0 360 235" style="width:100%; max-width:350px; margin:0 auto; display:block;">
                <ellipse cx="180" cy="118" rx="164" ry="108" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.5" stroke-dasharray="6 4"/>
                <ellipse cx="180" cy="138" rx="116" ry="76" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.5" stroke-dasharray="6 4"/>
                <ellipse cx="180" cy="160" rx="66" ry="42" fill="#E6F4EA" stroke="#34A853" stroke-width="2.5"/>
                <text x="180" y="42" text-anchor="middle" font-family="Poppins" font-size="13.5" font-weight="800" fill="#1A73E8">Lingkaran Luar = ?</text>
                <text x="180" y="92" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="800" fill="#C5221F">Tengah = ?</text>
                <text x="180" y="166" text-anchor="middle" font-family="Poppins" font-size="15" font-weight="800" fill="#137333">Inti = ?</text>
              </svg>
              <div style="font-size:12px; color:#5F6368; margin-top:4px;">Klik opsi <strong>A / B / C</strong> di kiri dulu, lalu buka jawabannya!</div>
            """,
            vis_a_html="""
              <svg viewBox="0 0 360 235" style="width:100%; max-width:350px; margin:0 auto; display:block;">
                <ellipse cx="180" cy="118" rx="166" ry="110" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.6"/>
                <text x="180" y="36" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="800" fill="#1A73E8">AI (Artificial Intelligence)</text>
                <text x="180" y="51" text-anchor="middle" font-family="Roboto" font-size="9.5" fill="#3C4043">Payung besar: aturan klasik hingga robot</text>
                <ellipse cx="180" cy="142" rx="124" ry="78" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.6"/>
                <text x="180" y="88" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="800" fill="#C5221F">ML (Machine Learning)</text>
                <text x="180" y="102" text-anchor="middle" font-family="Roboto" font-size="9.3" fill="#3C4043">Belajar pola langsung dari data</text>
                <ellipse cx="180" cy="166" rx="78" ry="46" fill="#E6F4EA" stroke="#34A853" stroke-width="2.8"/>
                <text x="180" y="156" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="800" fill="#137333">Deep Learning</text>
                <text x="180" y="171" text-anchor="middle" font-family="Roboto" font-size="9.2" fill="#137333">Neural Network</text>
                <text x="180" y="185" text-anchor="middle" font-family="Roboto" font-size="9.2" font-weight="700" fill="#137333">★ Proyek Frozen</text>
              </svg>
              <div style="display:flex; justify-content:center; gap:7px; margin-top:6px; align-items:center;">
                <img src="assets/P02/thumb_anna.jpg" style="width:32px; height:32px; border-radius:8px; object-fit:cover; border:2px solid #34A853;"/>
                <img src="assets/P02/thumb_elsa.jpg" style="width:32px; height:32px; border-radius:8px; object-fit:cover; border:2px solid #34A853;"/>
                <img src="assets/P02/thumb_olaf.jpg" style="width:32px; height:32px; border-radius:8px; object-fit:cover; border:2px solid #34A853;"/>
                <span style="font-size:11px; font-weight:700; color:#137333;">Klasifikasi piksel Frozen = DL ⊂ ML ⊂ AI</span>
              </div>
            """,
            notes="Alokasi waktu: 1 menit. Kuis 1/5 (Bab 1): minta peserta mengklik pilihan A/B/C terlebih dahulu sebelum membuka diagram Venn AI ⊃ ML ⊃ DL beserta penjelasannya.",
            bar_color="blue",
            correct_choice="B",
        ),
        _qa_slide(
            qa_id="quiz-p02-2",
            qa_num=2,
            quiz_progress_idx=2,
            data_title="Kuis 2/5 — Image Classification vs Object Detection",
            kicker="EVALUASI CEPAT · KUIS 2 / 5 (BAB 2)",
            title_html='Beda <span class="hl-red">Image Classification</span> &amp; <span class="hl-blue">Object Detection</span>',
            question_html="Apa perbedaan utama antara <strong>Image Classification</strong> (tugas proyek Frozen kita) dengan <strong>Object Detection</strong>?",
            choices=[
                "<strong>A.</strong> Object Detection hanya memberi 1 label kategori untuk seluruh foto tanpa posisi",
                "<strong>B.</strong> Image Classification memberi 1 label untuk seluruh foto; Object Detection mencari banyak objek sekaligus beserta kotak koordinat (<em>bounding box</em>)",
                "<strong>C.</strong> Keduanya menghasilkan keluaran yang sama persis, hanya berbeda bahasa pemrograman",
            ],
            answer_html=(
                "<strong>Jawaban: B!</strong><br/>"
                "• <strong>Image Classification:</strong> Menjawab <em>&ldquo;Ini foto siapa?&rdquo;</em> → keluaran <strong>1 label kelas + probabilitas</strong> untuk keseluruhan foto (persis proyek 5 karakter Frozen kita).<br/>"
                "• <strong>Object Detection:</strong> Menjawab <em>&ldquo;Ada apa saja &amp; di mana posisinya?&rdquo;</em> → keluaran banyak <strong>kotak <code>(x, y, w, h)</code> + label</strong> tiap objek.<br/>"
                "• <strong>Kenapa A &amp; C keliru:</strong> Opsi A justru terbalik definisinya, sedangkan keluaran keduanya berbeda struktur."
            ),
            vis_q_html="""
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; width:100%;">
                <div style="background:#FFFFFF; border:1.5px dashed #4285F4; border-radius:11px; padding:8px;">
                  <img src="assets/P02/thumb_elsa.jpg" style="width:100%; height:132px; object-fit:cover; border-radius:8px;"/>
                  <div style="font-family:var(--font-title); font-size:11px; font-weight:700; color:#1A73E8; margin-top:6px;">Kasus 1: Foto tunggal</div>
                  <div style="font-size:10.5px; color:#5F6368;">Keluaran: ?</div>
                </div>
                <div style="background:#FFFFFF; border:1.5px dashed #EA4335; border-radius:11px; padding:8px;">
                  <img src="assets/P02/thumb_olaf_ramai.jpg" style="width:100%; height:132px; object-fit:cover; border-radius:8px;"/>
                  <div style="font-family:var(--font-title); font-size:11px; font-weight:700; color:#C5221F; margin-top:6px;">Kasus 2: Banyak benda</div>
                  <div style="font-size:10.5px; color:#5F6368;">Keluaran: ?</div>
                </div>
              </div>
              <div style="font-size:11.6px; color:#5F6368; margin-top:8px;">Bandingkan keluaran kedua tugas Computer Vision ini!</div>
            """,
            vis_a_html="""
              <div style="display:flex; flex-direction:column; gap:9px; width:100%;">
                <div style="display:grid; grid-template-columns:1fr 1.35fr; gap:9px; align-items:stretch;">
                  <div style="background:#E8F0FE; border:1.5px solid #4285F4; border-radius:11px; padding:7px; display:flex; flex-direction:column; justify-content:space-between;">
                    <img src="assets/P02/thumb_elsa.jpg" style="width:100%; height:118px; object-fit:cover; border-radius:7px;"/>
                    <div style="margin-top:5px;">
                      <div style="font-family:var(--font-title); font-size:10.2px; font-weight:800; color:#1A73E8;">IMAGE CLASSIFICATION</div>
                      <div style="font-size:10px; color:#202124; background:#FFFFFF; border-radius:6px; padding:2px 6px; margin-top:3px; font-weight:700;">1 Label: ELSA (94%)</div>
                    </div>
                  </div>
                  <div style="background:#FCE8E6; border:1.5px solid #EA4335; border-radius:11px; padding:7px; display:flex; flex-direction:column; justify-content:space-between;">
                    <img src="assets/P02/02b_object_detection_demo.png" style="width:100%; height:118px; object-fit:cover; border-radius:7px;"/>
                    <div style="margin-top:5px;">
                      <div style="font-family:var(--font-title); font-size:10.2px; font-weight:800; color:#C5221F;">OBJECT DETECTION</div>
                      <div style="font-size:10px; color:#202124; background:#FFFFFF; border-radius:6px; padding:2px 6px; margin-top:3px; font-weight:700;">Banyak Kotak + Label</div>
                    </div>
                  </div>
                </div>
                <div style="background:#E6F4EA; border:1px solid #A8DAB5; border-radius:8px; padding:6px 10px; font-size:11px; color:#137333; font-weight:600;">
                  ✓ Proyek Frozen kita = <strong>Image Classification (5 Kelas)</strong>
                </div>
              </div>
            """,
            notes="Alokasi waktu: 1 menit. Kuis 2/5 (Bab 2): klik opsi lalu tunjukkan ilustrasi nyata berdampingan antara Classification (1 label Elsa) dan Object Detection (banyak bounding box).",
            bar_color="red",
            correct_choice="B",
        ),
        _qa_slide(
            qa_id="quiz-p02-3",
            qa_num=3,
            quiz_progress_idx=3,
            data_title="Kuis 3/5 — Menghitung Jumlah Neuron Input Layer",
            kicker="EVALUASI CEPAT · KUIS 3 / 5 (BAB 3 · TAHAP 2)",
            title_html='Menghitung <span class="hl-green">Neuron di Input Layer</span>',
            question_html="Jika sebuah foto berwarna RGB berukuran <strong><code>100 × 100 × 3</code></strong> diluruskan (<em>Flatten</em>) masuk ke Neural Network, berapa jumlah neuron di <strong>Input Layer</strong>?",
            choices=[
                "<strong>A.</strong> 10.000 neuron (hanya mengalikan tinggi × lebar = 100 × 100)",
                "<strong>B.</strong> 30.000 neuron (mengalikan tinggi × lebar × 3 channel RGB = 100 × 100 × 3)",
                "<strong>C.</strong> 100.000 neuron (karena tiap piksel dikali 10 secara otomatis)",
            ],
            answer_html=(
                "<strong>Jawaban: B — 30.000 neuron!</strong><br/>"
                "• <strong>Rumus pasti:</strong> <code>Tinggi × Lebar × Channel = 100 × 100 × 3 = 30.000</code> neuron penerima angka piksel.<br/>"
                "• <strong>Kenapa A keliru:</strong> <code>10.000</code> hanya cukup untuk gambar hitam-putih (<em>Grayscale</em>, 1 channel) — foto berwarna wajib menyimpan <strong>3 lapisan (R, G, B)</strong>.<br/>"
                "• <strong>Kaitan proyek Frozen:</strong> Untuk ukuran penuh <code>224×224×3</code>, jumlahnya <code>150.528</code> neuron!"
            ),
            vis_q_html="""
              <svg viewBox="0 0 330 225" style="width:100%; max-width:320px; margin:0 auto; display:block;">
                <rect x="40" y="34" width="110" height="110" rx="10" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.4"/>
                <rect x="26" y="48" width="110" height="110" rx="10" fill="#E6F4EA" stroke="#34A853" stroke-width="2.4"/>
                <rect x="12" y="62" width="110" height="110" rx="10" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.4"/>
                <text x="67" y="114" text-anchor="middle" font-family="Poppins" font-size="14" font-weight="800" fill="#C5221F">100 × 100</text>
                <text x="67" y="132" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#202124">× 3 (R, G, B)</text>
                <path d="M162 110 L212 110" stroke="#5F6368" stroke-width="3" marker-end="url(#arrq3)"/>
                <defs><marker id="arrq3" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#5F6368"/></marker></defs>
                <text x="187" y="98" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#1A73E8">Flatten</text>
                <rect x="224" y="24" width="88" height="172" rx="14" fill="#F8F9FA" stroke="#DADCE0" stroke-width="2.2" stroke-dasharray="5 4"/>
                <text x="268" y="108" text-anchor="middle" font-family="Poppins" font-size="22" font-weight="800" fill="#137333">?</text>
                <text x="268" y="128" text-anchor="middle" font-family="Roboto" font-size="10.5" font-weight="700" fill="#5F6368">Neuron Input</text>
              </svg>
              <div style="font-size:11.6px; color:#5F6368;">Ingat: foto RGB punya 3 lapis warna — jangan lupa dikali 3!</div>
            """,
            vis_a_html="""
              <div style="display:flex; flex-direction:column; gap:8px; width:100%;">
                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:6px;">
                  <div style="background:#FCE8E6; border:1.5px solid #EA4335; border-radius:9px; padding:7px 5px;">
                    <div style="font-family:var(--font-title); font-size:10.5px; font-weight:800; color:#C5221F;">Channel R</div>
                    <div style="font-family:var(--font-code); font-size:12.5px; font-weight:800; color:#202124;">10.000</div>
                  </div>
                  <div style="background:#E6F4EA; border:1.5px solid #34A853; border-radius:9px; padding:7px 5px;">
                    <div style="font-family:var(--font-title); font-size:10.5px; font-weight:800; color:#137333;">Channel G</div>
                    <div style="font-family:var(--font-code); font-size:12.5px; font-weight:800; color:#202124;">10.000</div>
                  </div>
                  <div style="background:#E8F0FE; border:1.5px solid #4285F4; border-radius:9px; padding:7px 5px;">
                    <div style="font-family:var(--font-title); font-size:10.5px; font-weight:800; color:#1A73E8;">Channel B</div>
                    <div style="font-family:var(--font-code); font-size:12.5px; font-weight:800; color:#202124;">10.000</div>
                  </div>
                </div>
                <div style="background:#E6F4EA; border:2px solid #34A853; border-radius:11px; padding:8px 10px;">
                  <div style="font-family:var(--font-code); font-size:11.5px; color:#137333; font-weight:700;">100 × 100 × 3 =</div>
                  <div style="font-family:var(--font-title); font-size:24px; font-weight:800; color:#137333; line-height:1.15;">30.000 Neuron Input ✓</div>
                </div>
                <img src="assets/P02/ho_step1_pixel_grid.png" style="width:100%; max-height:105px; object-fit:contain; border-radius:8px; border:1px solid #E0E3E7; background:#FFF; padding:3px;"/>
                <div style="font-size:10.4px; color:#5F6368;">Skala proyek Frozen (<code>224×224×3</code>) → <strong>150.528 neuron</strong>!</div>
              </div>
            """,
            notes="Alokasi waktu: 1 menit. Kuis 3/5 (Bab 3 Tahap 2): tekankan kenapa RGB harus dikali 3 (10.000 R + 10.000 G + 10.000 B = 30.000 neuron input).",
            bar_color="green",
            correct_choice="B",
        ),
        _qa_slide(
            qa_id="quiz-p02-4",
            qa_num=4,
            quiz_progress_idx=4,
            data_title="Kuis 4/5 — Peran Softmax di Output Layer",
            kicker="EVALUASI CEPAT · KUIS 4 / 5 (BAB 3 · TAHAP 4)",
            title_html='Mengapa Output Layer Memakai <span class="hl-yellow">Softmax</span>?',
            question_html="Di <strong>Output Layer</strong> klasifikasi <strong>5 karakter Frozen</strong> (<em>Anna, Elsa, Kristoff, Olaf, Sven</em>), mengapa kita memasang fungsi aktivasi <strong><code>Softmax</code></strong>?",
            choices=[
                "<strong>A.</strong> Mengubah 5 skor mentah (<code>z</code>) menjadi probabilitas <code>0–100%</code> yang jumlah totalnya tepat <code>100%</code>",
                "<strong>B.</strong> Mengubah semua skor positif menjadi angka negatif agar komputasi lebih ringan",
                "<strong>C.</strong> Menghapus latar belakang foto secara otomatis sebelum gambar dibaca neuron",
            ],
            answer_html=(
                "<strong>Jawaban: A!</strong><br/>"
                "• <strong>Mengapa tepat:</strong> Skor mentah <code>z = Σ(x·w) + b</code> bisa bernilai bebas (minus atau besar tak terbatas). <strong>Softmax</strong> (<code>e^z / Σe^z</code>) menormalkan kelima skor menjadi <strong>persentase keyakinan (0–100%) yang selalu berjumlah 100%</strong> sehingga mudah dibandingkan &amp; dipilih lewat <code>Argmax</code>.<br/>"
                "• <strong>Kenapa B &amp; C keliru:</strong> Softmax justru menghasilkan nilai positif <code>(0, 1)</code>, dan tidak pernah mengedit piksel latar foto."
            ),
            vis_q_html="""
              <svg viewBox="0 0 330 220" style="width:100%; max-width:320px; margin:0 auto; display:block;">
                <rect x="8" y="18" width="96" height="184" rx="11" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
                <text x="56" y="38" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="800" fill="#B06000">5 Skor Mentah z</text>
                <text x="56" y="68" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#202124">Anna: +0.4</text>
                <text x="56" y="96" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#137333">Elsa: +2.3</text>
                <text x="56" y="124" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#202124">Kris: +0.1</text>
                <text x="56" y="152" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#C5221F">Olaf: -0.2</text>
                <text x="56" y="180" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#202124">Sven: +0.2</text>
                <path d="M108 110 L134 110" stroke="#5F6368" stroke-width="2.4"/>
                <rect x="136" y="76" width="84" height="68" rx="12" fill="#202124"/>
                <text x="178" y="106" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="800" fill="#FBBC04">Softmax</text>
                <text x="178" y="124" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" fill="#E8EAED">Fungsi?</text>
                <path d="M222 110 L248 110" stroke="#5F6368" stroke-width="2.4"/>
                <rect x="250" y="54" width="72" height="112" rx="11" fill="#F8F9FA" stroke="#DADCE0" stroke-width="2" stroke-dasharray="5 4"/>
                <text x="286" y="116" text-anchor="middle" font-family="Poppins" font-size="22" font-weight="800" fill="#1A73E8">???</text>
              </svg>
              <div style="font-size:11.6px; color:#5F6368;">Apa yang dihasilkan Softmax dari 5 skor mentah <code>z</code> di atas?</div>
            """,
            vis_a_html="""
              <div style="display:flex; flex-direction:column; gap:6px; width:100%; text-align:left;">
                <div style="font-family:var(--font-title); font-size:11px; font-weight:800; color:#1A73E8; text-align:center;">Skor z → Softmax (e^z / Σe^z) → Probabilitas 100%</div>
                <div style="display:flex; align-items:center; gap:7px;">
                  <img src="assets/P02/thumb_anna.jpg" style="width:24px; height:24px; border-radius:50%; object-fit:cover;"/>
                  <span style="width:52px; font-size:11px; font-weight:700;">Anna</span>
                  <div style="flex:1; height:12px; background:#F1F3F4; border-radius:999px; overflow:hidden;"><div style="width:10.2%; height:100%; background:#4285F4;"></div></div>
                  <span style="width:38px; font-family:var(--font-code); font-size:10.5px; text-align:right;">10.2%</span>
                </div>
                <div style="display:flex; align-items:center; gap:7px; background:#E6F4EA; padding:4px 6px; border-radius:9px; border:1.5px solid #34A853;">
                  <img src="assets/P02/thumb_elsa.jpg" style="width:26px; height:26px; border-radius:50%; object-fit:cover; border:2px solid #34A853;"/>
                  <span style="width:52px; font-size:11.5px; font-weight:800; color:#137333;">Elsa ★</span>
                  <div style="flex:1; height:13px; background:#FFFFFF; border-radius:999px; overflow:hidden;"><div style="width:68.3%; height:100%; background:#34A853;"></div></div>
                  <span style="width:38px; font-family:var(--font-code); font-size:11px; font-weight:800; color:#137333; text-align:right;">68.3%</span>
                </div>
                <div style="display:flex; align-items:center; gap:7px;">
                  <img src="assets/P02/thumb_kristoff.jpg" style="width:24px; height:24px; border-radius:50%; object-fit:cover;"/>
                  <span style="width:52px; font-size:11px; font-weight:700;">Kristoff</span>
                  <div style="flex:1; height:12px; background:#F1F3F4; border-radius:999px; overflow:hidden;"><div style="width:7.6%; height:100%; background:#4285F4;"></div></div>
                  <span style="width:38px; font-family:var(--font-code); font-size:10.5px; text-align:right;">7.6%</span>
                </div>
                <div style="display:flex; align-items:center; gap:7px;">
                  <img src="assets/P02/thumb_olaf.jpg" style="width:24px; height:24px; border-radius:50%; object-fit:cover;"/>
                  <span style="width:52px; font-size:11px; font-weight:700;">Olaf</span>
                  <div style="flex:1; height:12px; background:#F1F3F4; border-radius:999px; overflow:hidden;"><div style="width:5.6%; height:100%; background:#4285F4;"></div></div>
                  <span style="width:38px; font-family:var(--font-code); font-size:10.5px; text-align:right;">5.6%</span>
                </div>
                <div style="display:flex; align-items:center; gap:7px;">
                  <img src="assets/P02/thumb_sven.jpg" style="width:24px; height:24px; border-radius:50%; object-fit:cover;"/>
                  <span style="width:52px; font-size:11px; font-weight:700;">Sven</span>
                  <div style="flex:1; height:12px; background:#F1F3F4; border-radius:999px; overflow:hidden;"><div style="width:8.4%; height:100%; background:#4285F4;"></div></div>
                  <span style="width:38px; font-family:var(--font-code); font-size:10.5px; text-align:right;">8.4%</span>
                </div>
                <div style="margin-top:4px; background:#E8F0FE; border:1px solid #C6DAFC; border-radius:8px; padding:6px 9px; text-align:center; font-size:11px; font-weight:700; color:#1A73E8;">
                  Total = 100.0% · Argmax memilih <strong>ELSA (68.3%) ✓</strong>
                </div>
              </div>
            """,
            notes="Alokasi waktu: 1 menit. Kuis 4/5 (Bab 3 Tahap 4): tunjukkan visual konversi skor mentah z (termasuk Olaf -0.2) menjadi 5 bar probabilitas positif yang jumlahnya tepat 100%.",
            bar_color="yellow",
            correct_choice="A",
        ),
        _qa_slide(
            qa_id="quiz-p02-5",
            qa_num=5,
            quiz_progress_idx=5,
            data_title="Kuis 5/5 — Backpropagation & Gradient Descent",
            kicker="EVALUASI CEPAT · KUIS 5 / 5 (BAB 3 · TAHAP 5)",
            title_html='Proses Koreksi Bobot: <span class="hl-blue">Backprop &amp; Gradient Descent</span>',
            question_html="Saat simulasi training Epoch 1 → Epoch 8 di Slide 32, <em>Mean Loss</em> turun dari <strong><code>1.70 → 0.21</code></strong>. Pasangan proses apa yang mengoreksi bobot <strong><code>W &amp; b</code></strong> agar tebakan makin akurat?",
            choices=[
                "<strong>A.</strong> Flatten + Argmax (meluruskan piksel lalu memilih skor tertinggi)",
                "<strong>B.</strong> Backpropagation + Gradient Descent (melacak sumber error mundur lalu menggeser <code>W &amp; b</code> menuruni bukit <em>Loss</em>)",
                "<strong>C.</strong> Resize + Normalisasi (mengecilkan dimensi foto dan membagi piksel dengan 255)",
            ],
            answer_html=(
                "<strong>Jawaban: B — Backpropagation + Gradient Descent!</strong><br/>"
                "• <strong>Backpropagation:</strong> Berjalan mundur dari nilai <em>Loss</em> untuk menghitung seberapa besar andil tiap bobot <code>W</code> dan bias <code>b</code> terhadap kesalahan.<br/>"
                "• <strong>Gradient Descent:</strong> Menggeser nilai <code>W &amp; b</code> sedikit demi sedikit sebesar <em>Learning Rate</em> menuju dasar lembah <em>Loss</em>.<br/>"
                "• <strong>Kenapa A &amp; C keliru:</strong> <em>Resize, Normalisasi, Flatten,</em> dan <em>Argmax</em> hanya memproses data di jalur maju — tidak pernah memperbarui bobot!"
            ),
            vis_q_html="""
              <svg viewBox="0 0 330 215" style="width:100%; max-width:320px; margin:0 auto; display:block;">
                <rect x="14" y="14" width="302" height="140" rx="12" fill="#FFFFFF" stroke="#E0E3E7" stroke-width="1.8"/>
                <text x="165" y="34" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="800" fill="#202124">Kurva Mean Loss Turun (E1 → E8)</text>
                <polyline points="42,58 78,76 114,96 150,112 186,123 222,131 258,137 290,141" fill="none" stroke="#EA4335" stroke-width="3.2" stroke-linecap="round"/>
                <circle cx="42" cy="58" r="5" fill="#EA4335"/>
                <text x="52" y="54" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#C5221F">E1: 1.70</text>
                <circle cx="290" cy="141" r="5.5" fill="#34A853"/>
                <text x="234" y="128" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#137333">E8: 0.21 ✓</text>
                <rect x="28" y="166" width="274" height="36" rx="10" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.6" stroke-dasharray="5 3"/>
                <text x="165" y="188" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="800" fill="#C5221F">↺ Proses apa yang mengoreksi W &amp; b?</text>
              </svg>
              <div style="font-size:11.6px; color:#5F6368;">Kuis terakhir sebelum Kamus Istilah &amp; Hands-On!</div>
            """,
            vis_a_html="""
              <div style="display:flex; flex-direction:column; gap:8px; width:100%;">
                <img src="assets/P02/05_loss_gradient_descent_overview.png" style="width:100%; max-height:152px; object-fit:contain; border-radius:9px; border:1px solid #E0E3E7; background:#FFF; padding:3px;"/>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:7px; text-align:left;">
                  <div style="background:#FCE8E6; border:1.4px solid #EA4335; border-radius:9px; padding:7px 9px;">
                    <div style="font-family:var(--font-title); font-size:10.4px; font-weight:800; color:#C5221F;">1. Backpropagation</div>
                    <div style="font-size:10px; color:#3C4043; line-height:1.3; margin-top:2px;">Lacak mundur bobot <code>W, b</code> mana yang memicu <em>Loss</em>.</div>
                  </div>
                  <div style="background:#E8F0FE; border:1.4px solid #4285F4; border-radius:9px; padding:7px 9px;">
                    <div style="font-family:var(--font-title); font-size:10.4px; font-weight:800; color:#1A73E8;">2. Gradient Descent</div>
                    <div style="font-size:10px; color:#3C4043; line-height:1.3; margin-top:2px;">Geser <code>W, b</code> menuruni bukit <em>Loss</em> tiap <em>Epoch</em>!</div>
                  </div>
                </div>
                <div style="background:#E6F4EA; border:1px solid #A8DAB5; border-radius:8px; padding:5px 9px; font-size:10.8px; color:#137333; font-weight:700;">
                  🎉 5/5 Kuis Tuntas — lanjut Kamus Istilah &amp; Hands-On!
                </div>
              </div>
            """,
            notes="Alokasi waktu: 1 menit. Kuis 5/5 (Bab 3 Tahap 5): tutup rangkaian 5 kuis dengan ilustrasi kurva Loss + Gradient Descent menuruni bukit sebelum masuk ke Kamus Istilah.",
            bar_color="blue",
            correct_choice="B",
        ),
    ]
    _quiz_html = "\n".join(_quiz_slides)

    # Slide 42: Grand Finale Dark Slide (zero premature Hidden/MLP leakage + balanced top alignment + finale strip)
    _summary_html = f"""
    <!-- 3 POIN UTAMA (DARK FINALE) -->
    <section class="slide dark" data-title="3 Poin Utama Hari Ini" data-notes="Alokasi waktu: 3 menit. Rangkum seluruh sesi Teori Neural Network menjadi 3 pilar utama agar mudah diingat setelah kelas selesai sekaligus beri preview singkat menuju P03 (Arsitektur Neural Network &amp; Konvolusi CNN).">
      <div class="kicker">RANGKUMAN INTI · TEORI NEURAL NETWORK</div>
      <h2>3 Poin Utama yang <span style="color:var(--yellow);">Wajib Dibawa Pulang</span></h2>
      <div class="finale-grid">
        <div class="finale-card">
          <div class="card-top-bar bar-blue"></div>
          <div class="finale-top">
            <div class="big-num" style="color:var(--blue); font-size:34px;">01</div>
            <span class="pill blue" style="font-size:9.8px; padding:2px 8px;">BAB 1 &amp; BAB 2</span>
          </div>
          <div class="card-title" style="color:#FFF; font-size:16px;">Peta Besar AI &amp; CV Jelas</div>
          <div class="card-body" style="color:#BDC1C6; font-size:13px;">Proyek klasifikasi 5 karakter Frozen berada di ranah <strong>Deep Learning</strong> (<code>AI ⊃ ML ⊃ DL</code>) dengan jenis tugas <strong>Multi-Class Image Classification</strong>.</div>
          <div class="finale-pill">🎯 <strong>Output:</strong> 1 label kelas + probabilitas 5 karakter (<code>100%</code>)</div>
        </div>
        <div class="finale-card">
          <div class="card-top-bar bar-green"></div>
          <div class="finale-top">
            <div class="big-num" style="color:var(--green); font-size:34px;">02</div>
            <span class="pill green" style="font-size:9.8px; padding:2px 8px;">BAB 3 · 5 TAHAP</span>
          </div>
          <div class="card-title" style="color:#FFF; font-size:16px;">Neural Network = 5 Tahap Runtut</div>
          <div class="card-body" style="color:#BDC1C6; font-size:13px;">Dimulai dari <strong>1 Piksel → 1 Neuron</strong>, diluruskan lewat <strong>Flatten</strong> menjadi <em>Input Layer</em>, dihitung <code>W·x + b → Softmax</code>, lalu belajar via <strong>Backpropagation &amp; Gradient Descent</strong>.</div>
          <div class="finale-pill">🔄 <strong>Siklus Belajar:</strong> Mean Loss turun <code>1.70 → 0.21</code> dalam 8 <em>Epoch</em></div>
        </div>
        <div class="finale-card">
          <div class="card-top-bar bar-red"></div>
          <div class="finale-top">
            <div class="big-num" style="color:var(--yellow); font-size:34px;">03</div>
            <span class="pill yellow" style="font-size:9.8px; padding:2px 8px;">HANDS-ON → P03</span>
          </div>
          <div class="card-title" style="color:#FFF; font-size:16px;">Terbukti di Kode → Siap ke P03!</div>
          <div class="card-body" style="color:#BDC1C6; font-size:13px;">Kamu baru saja membangun <strong>Neural Network 1-Layer</strong> nyata (<code>61.445</code> / <code>752.645</code> param) di Keras! Di <strong>P03</strong>, kita pelajari arsitektur berlapis &amp; <strong>CNN</strong> yang jauh lebih akurat membaca foto 2D.</div>
          <div class="finale-pill">🚀 <strong>Berikutnya:</strong> P03 — Arsitektur Neural Network &amp; CNN</div>
        </div>
      </div>
      <div class="finale-banner">
        <div style="font-size:12.6px; color:#E8EAED;">
          <strong style="color:#81C995;">✓ Fondasi Teori Neural Network (P02) Tuntas!</strong> &nbsp;·&nbsp; Referensi materi Bab 1–3: <strong style="color:#FDD663;">Slide 40–41</strong> &nbsp;·&nbsp; Simpan grafik Loss dari notebook sebagai catatan.
        </div>
        <div style="font-size:12px; font-style:italic; color:#9AA0A6; white-space:nowrap;">&ldquo;Memahami 1 neuron dengan jernih adalah kunci memahami jaringan jutaan parameter.&rdquo;</div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""

    _refs_html = f"""
    <!-- REFERENSI MATERI (1/2) — BAB 1 & BAB 2 (0 MENIT) -->
    <section class="slide" data-title="Referensi Materi (1/2) — Bab 1 &amp; Bab 2" data-notes="Alokasi waktu: 0 menit. Referensi materi bagian 1 khusus untuk Bab 1 (AI/ML/DL) dan Bab 2 (4 Tugas Computer Vision) sesuai docs/PLAN.md; sumber belum diverifikasi ulang diberi label [CEK LINK].">
      <div class="kicker">REFERENSI MATERI · BAGIAN 1 (BAB 1 &amp; BAB 2)</div>
      <h2>Referensi Materi: <span class="hl-blue">AI/ML/DL &amp; Tugas Computer Vision</span></h2>
      <div class="ref-grid-full">
        <a class="ref-card-rich featured" href="https://developers.google.com/machine-learning/crash-course" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num">1</div>
            <div class="ref-card-head"><span class="ref-title">Google Machine Learning Crash Course [CEK LINK]</span><span class="ref-tag must">Bab 1 · Inti</span></div>
          </div>
          <div class="ref-desc">Pengantar terstruktur ramah pemula tentang konsep AI, Machine Learning, fitur data, dan cara model belajar dari pasangan <code>Data + Label</code>.</div>
          <div class="ref-card-foot"><span class="ref-url">developers.google.com/machine-learning/crash-course ↗</span><span class="ref-ctx-pill">Bab 1 · AI, ML &amp; Fitur</span></div>
        </a>
        <a class="ref-card-rich acc-red" href="https://www.coursera.org/learn/convolutional-neural-networks" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num red">4</div>
            <div class="ref-card-head"><span class="ref-title">Coursera (DeepLearning.AI) — Computer Vision Week 1</span><span class="ref-tag">Bab 2 · Video</span></div>
          </div>
          <div class="ref-desc">Pengantar visual tugas Computer Vision pada foto nyata: membedakan <em>Image Classification</em>, deteksi objek, hingga cara komputer melihat tepi gambar.</div>
          <div class="ref-card-foot"><span class="ref-url">coursera.org/learn/convolutional-neural-networks ↗</span><span class="ref-ctx-pill">Bab 2 · 4 Tugas CV (S12–S16)</span></div>
        </a>
        <a class="ref-card-rich acc-blue" href="https://www.coursera.org/specializations/deep-learning" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num">2</div>
            <div class="ref-card-head"><span class="ref-title">Coursera — Deep Learning Specialization Course 1 [CEK LINK]</span><span class="ref-tag doc">Kursus</span></div>
          </div>
          <div class="ref-desc">Fondasi Neural Networks &amp; Deep Learning dari nol: mengapa pendekatan aturan manual kalah fleksibel dibanding belajar fitur otomatis.</div>
          <div class="ref-card-foot"><span class="ref-url">coursera.org/specializations/deep-learning ↗</span><span class="ref-ctx-pill">Bab 1 · ML vs DL (S07–S09)</span></div>
        </a>
        <a class="ref-card-rich acc-red" href="https://cs231n.github.io/classification/" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num red">5</div>
            <div class="ref-card-head"><span class="ref-title">Stanford CS231n — Image Classification Notes [CEK LINK]</span><span class="ref-tag doc">Catatan</span></div>
          </div>
          <div class="ref-desc">Catatan kuliah visual yang membedah tantangan nyata <em>Image Classification</em> (latar ramai, pencahayaan, sudut kamera) dari piksel ke skor kelas.</div>
          <div class="ref-card-foot"><span class="ref-url">cs231n.github.io/classification/ ↗</span><span class="ref-ctx-pill">Bab 2 · Classification (S13)</span></div>
        </a>
        <a class="ref-card-rich acc-yellow" href="https://www.youtube.com/@statquest" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num yellow">3</div>
            <div class="ref-card-head"><span class="ref-title">StatQuest — Machine Learning &amp; Neural Networks [CEK LINK]</span><span class="ref-tag">Video</span></div>
          </div>
          <div class="ref-desc">Penjelasan visual super jelas langkah demi langkah tentang <em>Supervised Learning</em>, klasifikasi multi-kelas, dan intuisi dasar Neural Network.</div>
          <div class="ref-card-foot"><span class="ref-url">youtube.com/@statquest ↗</span><span class="ref-ctx-pill">Bab 1 &amp; Bab 3 · Intuitif</span></div>
        </a>
        <a class="ref-card-rich acc-green" href="https://pillow.readthedocs.io/" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num green">6</div>
            <div class="ref-card-head"><span class="ref-title">Dokumentasi Pillow (PIL) — Pengolahan Foto &amp; Piksel [CEK LINK]</span><span class="ref-tag code">Dokumentasi</span></div>
          </div>
          <div class="ref-desc">Rujukan resmi membuka foto, mengubah ukuran (<em>resize</em>), membaca kanal <code>RGB</code>, dan mengubah gambar ke array NumPy untuk input Neural Network.</div>
          <div class="ref-card-foot"><span class="ref-url">pillow.readthedocs.io ↗</span><span class="ref-ctx-pill">Recap &amp; Hands-On Tahap 1</span></div>
        </a>
      </div>
      <div class="ref-route-bar">
        <div class="ref-route-head">
          <span>📚 Peta Referensi Materi Bab 1 &amp; Bab 2 (Sesuai Silabus P02)</span>
          <span class="pill blue" style="font-size:9.6px; padding:2px 8px;">Opsional · Klik kartu untuk membuka</span>
        </div>
        <div class="ref-route-grid">
          <div class="ref-step-box"><strong style="color:#1A73E8;">Bab 1 (#1, #2, #3):</strong> Memperkuat peta <code>AI ⊃ ML ⊃ DL</code>, cara kerja <em>Supervised Learning</em>, &amp; beda ML vs DL.</div>
          <div class="ref-step-box"><strong style="color:#C5221F;">Bab 2 (#4, #5):</strong> Memperdalam 4 tugas Computer Vision &amp; tantangan foto polos vs ramai pada <em>Image Classification</em>.</div>
          <div class="ref-step-box"><strong style="color:#137333;">Hands-On (#6):</strong> Panduan cepat membuka, <em>resize</em>, &amp; membaca nilai piksel RGB foto Frozen di Python.</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- REFERENSI MATERI (2/2) — BAB 3 & HANDS-ON (0 MENIT) -->
    <section class="slide" data-title="Referensi Materi (2/2) — Bab 3 Neural Network" data-notes="Alokasi waktu: 0 menit. Referensi materi bagian 2 khusus untuk Bab 3 (Neuron, Flatten, Weight+Bias, ReLU, Softmax, Loss, Backpropagation, Gradient Descent & Keras Sequential) sesuai docs/PLAN.md.">
      <div class="kicker">REFERENSI MATERI · BAGIAN 2 (BAB 3 · NEURAL NETWORK)</div>
      <h2>Referensi Materi: <span class="hl-green">Teori Neural Network &amp; Praktik Keras</span></h2>
      <div class="ref-grid-full">
        <a class="ref-card-rich featured" href="https://www.youtube.com/watch?v=aircAruvnKk" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num">7</div>
            <div class="ref-card-head"><span class="ref-title">3Blue1Brown — But what is a Neural Network?</span><span class="ref-tag must">Wajib</span></div>
          </div>
          <div class="ref-desc">Visual paling jernih untuk melihat langsung bagaimana piksel gambar masuk ke <em>Input Layer</em>, dikali bobot (<em>weight</em>), ditambah <em>bias</em>, hingga prediksi!</div>
          <div class="ref-card-foot"><span class="ref-url">youtube.com/watch?v=aircAruvnKk ↗</span><span class="ref-ctx-pill">Bab 3 · Tahap 1–4 (S20–S28)</span></div>
        </a>
        <a class="ref-card-rich acc-yellow" href="https://playground.tensorflow.org/" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num yellow">10</div>
            <div class="ref-card-head"><span class="ref-title">TensorFlow Playground [CEK LINK]</span><span class="ref-tag code">Sandbox</span></div>
          </div>
          <div class="ref-desc">Eksperimen interaktif langsung di browser tanpa coding: ubah bobot, fungsi aktivasi (<code>ReLU</code>), dan <em>Learning Rate</em> sambil melihat efeknya live!</div>
          <div class="ref-card-foot"><span class="ref-url">playground.tensorflow.org ↗</span><span class="ref-ctx-pill">Bab 3 · Eksperimen W, b &amp; LR</span></div>
        </a>
        <a class="ref-card-rich acc-blue" href="https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num">8</div>
            <div class="ref-card-head"><span class="ref-title">3Blue1Brown — Playlist Neural Networks (Bab 1–4)</span><span class="ref-tag">Video</span></div>
          </div>
          <div class="ref-desc">Seri lengkap 4 episode: membedah <em>Loss Function</em>, cara kerja <em>Gradient Descent</em> menuruni lembah error, hingga intuisi <em>Backpropagation</em>.</div>
          <div class="ref-card-foot"><span class="ref-url">youtube.com/playlist?list=PLZHQObOWTQDNU6R1_... ↗</span><span class="ref-ctx-pill">Bab 3 · Tahap 5 (S29–S32)</span></div>
        </a>
        <a class="ref-card-rich acc-green" href="https://keras.io/guides/sequential_model/" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num green">11</div>
            <div class="ref-card-head"><span class="ref-title">Keras Official — The Sequential Model Guide [CEK LINK]</span><span class="ref-tag code">Dokumentasi</span></div>
          </div>
          <div class="ref-desc">Panduan resmi menyusun layer <code>Sequential</code>, <code>Flatten</code>, dan <code>Dense(..., activation="softmax")</code> di Keras 3 beserta cara membaca <code>summary()</code>.</div>
          <div class="ref-card-foot"><span class="ref-url">keras.io/guides/sequential_model/ ↗</span><span class="ref-ctx-pill">Hands-On Tahap 4–5 (S46–S48)</span></div>
        </a>
        <a class="ref-card-rich acc-green" href="https://3blue1brown.com/lessons/neural-networks" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num green">9</div>
            <div class="ref-card-head"><span class="ref-title">3Blue1Brown — Versi Tulis Neural Networks</span><span class="ref-tag doc">Artikel</span></div>
          </div>
          <div class="ref-desc">Ringkasan interaktif berbentuk bacaan bergambar — cocok jika ingin mengulang konsep <em>Forward Pass</em>, <em>Weight</em>, &amp; <em>Loss</em> pelan-pelan tanpa video.</div>
          <div class="ref-card-foot"><span class="ref-url">3blue1brown.com/lessons/neural-networks ↗</span><span class="ref-ctx-pill">Bab 3 · Bacaan Santai</span></div>
        </a>
        <a class="ref-card-rich acc-blue" href="https://arxiv.org/abs/1412.6980" target="_blank" rel="noopener">
          <div class="ref-card-top">
            <div class="ref-num">12</div>
            <div class="ref-card-head"><span class="ref-title">Kingma &amp; Ba — Adam Optimizer (arXiv 1412.6980) [CEK LINK]</span><span class="ref-tag doc">Paper</span></div>
          </div>
          <div class="ref-desc">Paper asli optimizer <strong>Adam</strong> (pengembangan adaptif dari <em>Gradient Descent</em>) yang kita pakai langsung saat <code>compile()</code> di Hands-On Tahap 4!</div>
          <div class="ref-card-foot"><span class="ref-url">arxiv.org/abs/1412.6980 ↗</span><span class="ref-ctx-pill">Bab 3 &amp; Hands-On · Optimizer</span></div>
        </a>
      </div>
      <div class="ref-route-bar" style="background:#E6F4EA; border-color:#A8DAB5;">
        <div class="ref-route-head">
          <span style="color:#137333;">🧭 Rute Belajar Mandiri Rekomendasi Bab 3 (Sesudah Kelas · ±45 Menit)</span>
          <span class="pill green" style="font-size:9.6px; padding:2px 8px;">Opsional · 100% Selaras Bab 3 &amp; Hands-On</span>
        </div>
        <div class="ref-route-grid">
          <div class="ref-step-box"><strong style="color:#1A73E8;">1. Tonton #7 (±19 menit):</strong> Visualisasi 3Blue1Brown paling jernih memperkuat bayangan piksel → neuron → Softmax.</div>
          <div class="ref-step-box"><strong style="color:#B06000;">2. Coba #10 (±10 menit):</strong> Mainkan slider bobot, <code>ReLU</code>, &amp; <em>Learning Rate</em> di browser tanpa menulis kode sama sekali.</div>
          <div class="ref-step-box"><strong style="color:#137333;">3. Baca #11 (±15 menit):</strong> Referensi cepat untuk sintaks <code>Sequential([Flatten(), Dense(...)])</code> di Hands-On!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    if HIDE_BAB4_ARCH:
        # Urutan final 42 slide: Bab 1-3 -> Cover Kuis/Kamus/Ref -> Kuis -> Kamus -> Referensi -> Cover Hands-On -> Hands-On 1-6 -> 3 Poin Utama
        s.append(_eval_cover_slide)
        s.append(_quiz_html)
        s.append(_glossary_html)
        s.append(_refs_html)
        s.append(_break_slide)
        s.extend(_handson_slides)
        s.append(_summary_html)
    else:
        s.append(_break_slide)
        s.extend(_handson_slides)
        s.append(_challenge_html)
        s.append(_glossary_html)
        s.append(_quiz_html)
        s.append(_summary_html)
        s.append(_closing_html)
        s.append(_refs_html)

    return "\n".join(s)


def build_extra_js(data: dict) -> str:
    cs_json = json.dumps(data["char_samples"], ensure_ascii=False)
    fp_json = json.dumps(data["mini_forward_pass"], ensure_ascii=False)
    flt_json = json.dumps(data["flatten_4x4"], ensure_ascii=False)
    ends_json = json.dumps(data["elsa_rgb_ends"], ensure_ascii=False)
    tm_json = json.dumps(data["training_math_demo"], ensure_ascii=False)
    fnn_json = json.dumps(data["full_nn_demo"], ensure_ascii=False)
    total_imgs = data["total_images"]
    return f"""
    const FROZEN_CHAR_DATA = {cs_json};
    const MINI_FP = {fp_json};
    const FLATTEN_PIXELS = {flt_json};
    const ELSA_ENDS = {ends_json};
    const TRAINING_MATH = {tm_json};
    const FULL_NN_DATA = {fnn_json};

    // =========================================================================
    // SIMULATOR #1 (Slide 09): Aturan Manual vs Machine Learning
    // =========================================================================
    function setMlTab(mode) {{
      document.querySelectorAll('#ml-tabs button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.ml !== mode);
      }});
      const diag = document.getElementById('ml-diagram');
      const badge = document.getElementById('ml-badge');
      const title = document.getElementById('ml-title');
      const desc = document.getElementById('ml-desc');
      const extra = document.getElementById('ml-extra');
      const bar = document.getElementById('ml-bar');
      const call = document.getElementById('ml-callout');
      if (!diag) return;

      if (mode === 'rule') {{
        diag.innerHTML = `
          <svg viewBox="0 0 490 270" style="width:100%; height:100%; max-height:310px; display:block;">
            <rect x="8" y="16" width="474" height="175" rx="14" fill="#FFFFFF" stroke="#F6AEA9" stroke-width="1.6"/>
            <text x="24" y="38" font-family="Poppins" font-size="11.5" font-weight="700" fill="#C5221F">ALUR PEMROGRAMAN TRADISIONAL (ATURAN MANUAL)</text>
            <rect x="24" y="56" width="132" height="54" rx="10" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
            <text x="90" y="80" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#1A73E8">Data (Foto)</text>
            <text x="90" y="98" text-anchor="middle" font-family="Roboto" font-size="10.5" fill="#5F6368">Piksel RGB</text>
            <rect x="24" y="122" width="132" height="54" rx="10" fill="#FCE8E6" stroke="#EA4335" stroke-width="2"/>
            <text x="90" y="145" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#C5221F">Aturan Manual</text>
            <text x="90" y="163" text-anchor="middle" font-family="Roboto Mono" font-size="10" fill="#C5221F">if biru &gt; 0.6...</text>
            <line x1="156" y1="83" x2="212" y2="108" stroke="#5F6368" stroke-width="2.4"/>
            <line x1="156" y1="149" x2="212" y2="124" stroke="#5F6368" stroke-width="2.4"/>
            <rect x="214" y="84" width="112" height="64" rx="12" fill="#202124"/>
            <text x="270" y="121" text-anchor="middle" font-family="Poppins" font-size="12.5" font-weight="700" fill="#FFFFFF">Komputer</text>
            <line x1="326" y1="116" x2="366" y2="116" stroke="#5F6368" stroke-width="2.6"/>
            <polygon points="364,110 374,116 364,122" fill="#5F6368"/>
            <rect x="376" y="84" width="92" height="64" rx="10" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
            <text x="422" y="113" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#B06000">Jawaban</text>
            <text x="422" y="131" text-anchor="middle" font-family="Roboto" font-size="10.5" fill="#5F6368">Elsa / Olaf</text>
            <rect x="8" y="204" width="474" height="54" rx="12" fill="#FCE8E6" stroke="#F6AEA9" stroke-width="1.4"/>
            <text x="245" y="227" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#C5221F">Masalah pada Foto Dunia Nyata:</text>
            <text x="245" y="246" text-anchor="middle" font-family="Roboto" font-size="11" fill="#3C4043">Begitu cahaya redup atau latar rak ramai, aturan warna manual langsung gagal!</text>
          </svg>`;
        if (bar) bar.className = 'card-top-bar bar-red';
        badge.className = 'pill red'; badge.textContent = 'PEMROGRAMAN TRADISIONAL';
        title.textContent = 'Manusia Menulis Semua Aturan';
        desc.innerHTML = '<ul><li>Programmer harus memikirkan sendiri setiap syarat aturan (mis. <code>if-else</code>).</li><li>Cocok untuk aturan pasti (kalkulator, pajak), tetapi <strong>mustahil</strong> untuk membedakan ribuan variasi foto figurine!</li></ul>';
        if (extra) extra.innerHTML = '<div style="background:#FCE8E6; border:1px solid #F6AEA9; border-radius:11px; padding:9px 11px; display:flex; flex-direction:column; gap:5px; font-size:11.6px; color:#3C4043;"><div style="font-family:var(--font-title); font-size:11px; font-weight:800; color:#C5221F;">3 Penyebab Aturan Manual Gagal di Foto:</div><div>• <strong>Cahaya berubah:</strong> angka RGB biru gaun Elsa ikut turun di foto redup.</div><div>• <strong>Sudut &amp; jarak:</strong> figurin miring atau lebih kecil mengubah semua koordinat piksel.</div><div>• <strong>Latar rak ramai:</strong> benda biru di belakang ikut memicu aturan <code>if biru</code>!</div></div>';
        call.className = 'callout red';
        call.innerHTML = '<strong>Solusinya?</strong> Klik Tab <strong>2. Machine Learning</strong> agar komputer belajar pola sendiri dari contoh!';
      }} else {{
        diag.innerHTML = `
          <svg viewBox="0 0 490 270" style="width:100%; height:100%; max-height:310px; display:block;">
            <!-- Stage 1: Training -->
            <rect x="8" y="8" width="474" height="148" rx="14" fill="#FFFFFF" stroke="#A8DAB5" stroke-width="1.8"/>
            <text x="24" y="28" font-family="Poppins" font-size="11" font-weight="700" fill="#137333">TAHAP 1 · TRAINING (BELAJAR DARI CONTOH + KUNCI JAWABAN)</text>
            <rect x="24" y="40" width="132" height="46" rx="9" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.8"/>
            <text x="90" y="60" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#1A73E8">Data ({total_imgs} Foto)</text>
            <text x="90" y="76" text-anchor="middle" font-family="Roboto" font-size="10" fill="#5F6368">Contoh latihan</text>
            <rect x="24" y="96" width="132" height="46" rx="9" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>
            <text x="90" y="116" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#137333">Label Jawaban</text>
            <text x="90" y="132" text-anchor="middle" font-family="Roboto Mono" font-size="9.8" fill="#137333">Anna..Sven</text>
            <line x1="156" y1="63" x2="210" y2="85" stroke="#34A853" stroke-width="2.4"/>
            <line x1="156" y1="119" x2="210" y2="99" stroke="#34A853" stroke-width="2.4"/>
            <rect x="212" y="62" width="114" height="60" rx="12" fill="#1A73E8"/>
            <text x="269" y="89" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#FFFFFF">Algoritma</text>
            <text x="269" y="107" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#FFFFFF">ML</text>
            <line x1="326" y1="92" x2="366" y2="92" stroke="#34A853" stroke-width="2.6"/>
            <polygon points="364,86 374,92 364,98" fill="#34A853"/>
            <rect x="376" y="62" width="92" height="60" rx="10" fill="#E6F4EA" stroke="#34A853" stroke-width="2.4"/>
            <text x="422" y="89" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#137333">Model</text>
            <text x="422" y="106" text-anchor="middle" font-family="Roboto" font-size="10" fill="#137333">(Pola Terlatih)</text>

            <!-- Stage 2: Inference / Prediction -->
            <rect x="8" y="168" width="474" height="94" rx="14" fill="#E8F0FE" stroke="#C6DAFC" stroke-width="1.6"/>
            <text x="24" y="188" font-family="Poppins" font-size="11" font-weight="700" fill="#1A73E8">TAHAP 2 · PREDIKSI (INFERENCE PADA FOTO BARU)</text>
            <rect x="24" y="200" width="132" height="48" rx="9" fill="#FFFFFF" stroke="#4285F4" stroke-width="1.8"/>
            <text x="90" y="221" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#1A73E8">Foto Baru</text>
            <text x="90" y="237" text-anchor="middle" font-family="Roboto" font-size="9.8" fill="#5F6368">Belum pernah dilihat</text>
            <line x1="156" y1="224" x2="210" y2="224" stroke="#1A73E8" stroke-width="2.4"/><polygon points="208,218 218,224 208,230" fill="#1A73E8"/>
            <rect x="220" y="200" width="106" height="48" rx="9" fill="#34A853"/>
            <text x="273" y="229" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#FFFFFF">Model</text>
            <line x1="326" y1="224" x2="366" y2="224" stroke="#1A73E8" stroke-width="2.4"/><polygon points="364,218 374,224 364,230" fill="#1A73E8"/>
            <rect x="376" y="200" width="92" height="48" rx="9" fill="#202124"/>
            <text x="422" y="221" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#FFFFFF">Prediksi</text>
            <text x="422" y="238" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#34A853">"Elsa!"</text>
          </svg>`;
        if (bar) bar.className = 'card-top-bar bar-green';
        badge.className = 'pill green'; badge.textContent = 'MACHINE LEARNING (SUPERVISED)';
        title.textContent = 'Belajar Pola dari Contoh & Kunci Jawaban';
        desc.innerHTML = '<ul><li>Kita memberi data latihan beserta kunci jawabannya (<em>label</em>), lalu algoritma ML menghasilkan <strong>Model</strong> untuk menebak <strong>foto baru</strong>!</li></ul>';
        if (extra) extra.innerHTML = '<div style="background:#F8F9FA; border:1.2px solid #DADCE0; border-radius:11px; padding:9px 11px; display:flex; flex-direction:column; gap:5.5px; font-size:11.3px; color:#3C4043;"><div style="font-family:var(--font-title); font-size:10.8px; font-weight:800; color:#202124;">3 Paradigma Belajar Machine Learning:</div><div style="background:#E6F4EA; border:1px solid #A8DAB5; border-radius:7px; padding:4.5px 8px;"><strong style="color:#137333;">1. Supervised Learning ★ (Proyek Frozen):</strong> belajar dari <code>Foto + Label</code>.</div><div>• <strong>2. Unsupervised Learning:</strong> tanpa label — mengelompokkan pola mirip (<em>clustering</em>).</div><div>• <strong>3. Reinforcement Learning:</strong> belajar lewat <em>trial &amp; error</em> + skor hadiah (<em>reward</em>).</div></div>';
        call.className = 'callout green';
        call.innerHTML = '<strong>Hasil:</strong> Makin beragam contoh fotonya (polos &amp; ramai), makin tangguh pola yang dipelajari model.';
      }}
    }}
    setMlTab('rule');

    // =========================================================================
    // SIMULATOR #2 (Slide 10): Lingkaran Bersarang AI ⊃ ML ⊃ DL
    // =========================================================================
    const VNN_CFG = {{
      ai: {{
        pill: 'RECAP · ARTIFICIAL INTELLIGENCE (AI)', pillCls: 'pill blue', barCls: 'card-top-bar bar-blue', callCls: 'callout',
        title: 'Bidang Utama (Broad Field): Mengamati, Menalar & Bertindak',
        illus: '<div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:6px;"><span class="pill blue" style="font-size:10.5px; padding:3px 9px;">AI Catur (Minimax)</span><span class="pill blue" style="font-size:10.5px; padding:3px 9px;">Navigasi Rute (A*)</span><span class="pill blue" style="font-size:10.5px; padding:3px 9px;">Expert System</span><span class="pill green" style="font-size:10.5px; padding:3px 9px;">ML &amp; DL</span></div>',
        body: '<ul><li>Lingkaran terluar yang mencakup seluruh pendekatan AI — mulai dari <strong>AI Klasik</strong> (pencarian &amp; logika) hingga <strong>AI Modern</strong> (ML &amp; DL).</li></ul>',
        frozen: '<strong>Posisi di Peta:</strong> Semua sistem ML &amp; DL berada di dalam lingkaran AI (tetapi bukan automasi statis seperti kalkulator).',
        extra: '<strong>Ingat Pembeda Slide 06:</strong> Kalkulator &amp; Excel = <em>Bukan AI</em> (statis); AI Klasik = pencarian logika (<code>A*</code>, catur); AI Modern = belajar dari data.',
        call: '<strong>Klik lingkaran ML / DL</strong> untuk masuk lebih dalam ke cabang belajar dari data!',
      }},
      ml: {{
        pill: 'RECAP · MACHINE LEARNING (ML)', pillCls: 'pill red', barCls: 'card-top-bar bar-red', callCls: 'callout red',
        title: 'Cabang AI yang Belajar Pola dari Data',
        illus: '<div style="display:flex; align-items:center; justify-content:center; gap:7px; font-family:var(--font-code); font-size:10.5px;"><span style="background:#FCE8E6; color:#C5221F; padding:3px 8px; border-radius:6px; font-weight:700;">Fitur Manual</span><span>→</span><span style="background:#FEF7E0; color:#B06000; padding:3px 8px; border-radius:6px; font-weight:700;">Algoritma Statistik</span><span>→</span><span style="background:#202124; color:#FFF; padding:3px 8px; border-radius:6px; font-weight:700;">Model</span></div>',
        body: '<ul><li>Belajar pola dari contoh data menggunakan algoritma statistik (<em>Decision Tree, Random Forest, SVM</em>).</li></ul>',
        frozen: '<strong>Batasan pada foto:</strong> Manusia masih perlu mengekstrak fitur manual dulu (kita bedah tajam perbedaannya di slide berikutnya!).',
        extra: '<strong>Kapan ML Klasik Dipilih?</strong> Sangat unggul &amp; cepat untuk data <strong>tabel terstruktur</strong> (Excel/CSV: harga rumah, skor kredit, transaksi).',
        call: '<strong>Klik lingkaran DL</strong> untuk melihat solusi khusus bagi foto &amp; video!',
      }},
      dl: {{
        pill: 'DEEP LEARNING (DL)', pillCls: 'pill green', barCls: 'card-top-bar bar-green', callCls: 'callout green',
        title: 'Cabang ML dengan Neural Network Berlapis Banyak',
        illus: '<div style="display:flex; align-items:center; justify-content:center; gap:9px;"><img src="assets/P02/thumb_elsa.jpg" style="width:36px; height:36px; border-radius:7px; object-fit:cover; border:1.5px solid #4285F4;"/><span style="font-weight:700; color:#137333;">→</span><span style="background:#34A853; color:#FFF; padding:4px 10px; border-radius:7px; font-family:var(--font-title); font-size:11px; font-weight:700;">Neural Network (Belajar Fitur Otomatis)</span><span style="font-weight:700; color:#137333;">→</span><span style="background:#E6F4EA; border:1.5px solid #34A853; color:#137333; padding:3px 8px; border-radius:7px; font-family:var(--font-title); font-size:11px; font-weight:700;">Elsa!</span></div>',
        body: '<ul><li>Memakai <strong>Neural Network</strong> bertingkat yang otomatis mempelajari ciri langsung dari piksel mentah (tepi → bentuk → objek).</li><li>Sangat unggul untuk data tidak terstruktur: <strong>foto, video, suara, dan teks</strong>.</li></ul>',
        frozen: '<strong>Contoh di Proyek Frozen:</strong> Memasukkan foto <code>(224,224,3)</code> langsung ke <strong>Neural Network berlapis banyak</strong> untuk menebak Anna, Elsa, Kristoff, Olaf, atau Sven!',
        extra: '<strong>Kenapa Disebut &ldquo;Deep&rdquo;?</strong> Karena menumpuk lapisan fitur bertingkat (<em>piksel → tepi → bentuk → karakter</em>). Di <strong>P02</strong> kita bedah dulu fondasi 1 lapisan hingga tuntas sebelum banyak lapisan (CNN) di <strong>P03–P04</strong>!',
        call: '<strong>Posisi proyek kita:</strong> Kita bekerja tepat di jantung <strong>Deep Learning untuk Computer Vision</strong>.',
      }},
    }};

    function setVnnMode(m) {{
      const c = VNN_CFG[m];
      if (!c) return;
      document.querySelectorAll('#vnn-tabs button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.vnn !== m);
      }});
      document.getElementById('vnn-c-ai').setAttribute('opacity', m === 'ai' ? '1' : '0.45');
      document.getElementById('vnn-c-ml').setAttribute('opacity', m === 'ml' ? '1' : '0.55');
      document.getElementById('vnn-c-dl').setAttribute('opacity', m === 'dl' ? '1' : '0.6');
      document.getElementById('vnn-c-ai').setAttribute('stroke-width', m === 'ai' ? '5' : '2.5');
      document.getElementById('vnn-c-ml').setAttribute('stroke-width', m === 'ml' ? '5' : '2.5');
      document.getElementById('vnn-c-dl').setAttribute('stroke-width', m === 'dl' ? '5' : '2.5');
      document.getElementById('vnn-pill').className = c.pillCls;
      document.getElementById('vnn-pill').textContent = c.pill;
      document.getElementById('vnn-bar').className = c.barCls;
      document.getElementById('vnn-title').textContent = c.title;
      const illusEl = document.getElementById('vnn-illus');
      if (illusEl) illusEl.innerHTML = c.illus || '';
      document.getElementById('vnn-body').innerHTML = c.body;
      document.getElementById('vnn-frozen').innerHTML = c.frozen;
      const exEl = document.getElementById('vnn-extra'); if (exEl) exEl.innerHTML = c.extra || '';
      const callEl = document.getElementById('vnn-callout');
      callEl.className = c.callCls;
      callEl.innerHTML = c.call;
    }}
    setVnnMode('dl');

    // =========================================================================
    // SIMULATOR #3 (Slide 17): Cocokkan Kasus Nyata dengan Task CV
    // =========================================================================
    const MATCH_ANS = {{
      0: {{ ok: 'cls', msg: '✅ Benar! 1 foto daun utuh → 1 label penyakit = Image Classification.' }},
      1: {{ ok: 'det', msg: '✅ Benar! Banyak barang berbeda + lokasinya di nampan = Object Detection.' }},
      2: {{ ok: 'seg', msg: '✅ Benar! Memisahkan lekuk rambut per piksel dari latar = Semantic / Instance Segmentation.' }},
      3: {{ ok: 'trk', msg: '✅ Benar! Mengikuti ID tiap mobil antar-frame video = Object Tracking.' }},
    }};
    function setMatchPdfState(mode) {{
      [0, 1, 2, 3].forEach((i) => {{
        const row = document.getElementById('m-row-' + i);
        const fb = document.getElementById('m-fb-' + i);
        if (!row || !fb) return;
        row.querySelectorAll('button').forEach((b) => {{ b.className = 'btn-ui outline'; b.style.background = ''; }});
        if (mode === 'ans') {{
          const ok = MATCH_ANS[i].ok;
          const okBtn = row.querySelector(`button[data-mc="${{ok}}"]`);
          if (okBtn) okBtn.className = 'btn-ui green';
          fb.style.color = '#137333';
          fb.style.fontWeight = '700';
          fb.textContent = MATCH_ANS[i].msg;
        }} else {{
          fb.style.color = '#5F6368';
          fb.style.fontWeight = '400';
          fb.textContent = 'Pilih salah satu task di sebelah kanan →';
        }}
      }});
    }}
    function checkMatch(rowIdx, choice, btn) {{
      const row = document.getElementById('m-row-' + rowIdx);
      const fb = document.getElementById('m-fb-' + rowIdx);
      if (!row || !fb) return;
      row.querySelectorAll('button').forEach((b) => {{ b.className = 'btn-ui outline'; }});
      const ans = MATCH_ANS[rowIdx];
      if (choice === ans.ok) {{
        btn.className = 'btn-ui green';
        fb.style.color = '#137333';
        fb.style.fontWeight = '700';
        fb.textContent = ans.msg;
      }} else {{
        btn.className = 'btn-ui';
        btn.style.background = '#EA4335';
        fb.style.color = '#C5221F';
        fb.style.fontWeight = '600';
        fb.textContent = 'Belum tepat — coba lihat lagi apakah outputnya 1 label, banyak kotak, mask piksel, atau video!';
      }}
    }}

    // =========================================================================
    // SHARED HELPER: Synchronized Explanation-Card Glow & Lift across S20–S28
    // =========================================================================
    function _syncCards(ids, activeIdx, colors) {{
      ids.forEach((id, idx) => {{
        const el = document.getElementById(id);
        if (!el) return;
        el.classList.remove('sync-on', 'sync-dim', 'sync-blue', 'sync-yellow', 'sync-green', 'sync-red');
        if (activeIdx < 0) return;
        if (idx === activeIdx) {{
          el.classList.add('sync-on', 'sync-' + (colors[idx] || 'blue'));
        }} else {{
          el.classList.add('sync-dim');
        }}
      }});
    }}

    // =========================================================================
    // ANIMASI INTERAKTIF 1 PIKSEL -> 1 NEURON (Slide 20): 60fps Zoom -> Pick -> Morph
    // =========================================================================
    const N1_GRID_N = (ELSA_ENDS && ELSA_ENDS.grid_n) ? ELSA_ENDS.grid_n : 8;
    const N1_GRID = (ELSA_ENDS && ELSA_ENDS.grid) ? ELSA_ENDS.grid : [];
    const N1_DRESS_IDX = (ELSA_ENDS && typeof ELSA_ENDS.dress_idx === 'number') ? ELSA_ENDS.dress_idx : 35;
    const N1_SAMPLE_CYCLE = [N1_DRESS_IDX, 0, 19, 51]; // Gaun Biru Elsa -> Dinding (1,1) -> Rambut -> Tangan
    let n1SamplePos = 0;
    let n1SelectedIdx = N1_DRESS_IDX;
    let n1Raf = null;
    let n1Prog = 1.0;        // 0..1 (1.0 = idle/complete)
    let n1StartProg = 0.0;
    let n1Playing = false;
    let n1LastTs = 0;
    let n1Cache = null;

    function _n1GetPx(idx) {{
      if (N1_GRID.length > 0) return N1_GRID[Math.max(0, Math.min(N1_GRID.length - 1, idx))];
      return {{ idx: 1, r: 4, c: 2, rgb: [108, 112, 143], norm: [0.42, 0.44, 0.56], gray: 0.45 }};
    }}

    function _n1SetPlayBtn(playing) {{
      const b = document.getElementById('n1-btn-play');
      if (!b) return;
      b.textContent = playing ? '■ Stop' : '▶ Play';
      b.style.background = playing ? '#EA4335' : '#34A853';
      b.style.borderColor = playing ? '#EA4335' : '#34A853';
    }}

    function _stopN1Anim() {{
      if (n1Raf !== null) {{ cancelAnimationFrame(n1Raf); n1Raf = null; }}
      n1Playing = false;
      _n1SetPlayBtn(false);
    }}

    function _n1ClearOverlay() {{
      const c = document.getElementById('n1-motion-canvas');
      if (!c) return;
      const ctx = c.getContext('2d');
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, c.width, c.height);
    }}

    function _n1BuildGrid() {{
      const host = document.getElementById('n1-grid');
      if (!host || host.children.length > 0) return;
      host.innerHTML = N1_GRID.map((px, i) => {{
        const bg = `rgb(${{px.rgb[0]}},${{px.rgb[1]}},${{px.rgb[2]}})`;
        return `<div class="n1-cell${{i === n1SelectedIdx ? ' selected' : ''}}" data-n1="${{i}}" onclick="pickN1Pixel(${{i}})" title="Baris ${{px.r + 1}}, Kol ${{px.c + 1}} · nilai ${{px.gray.toFixed(2)}}" style="background:${{bg}};"></div>`;
      }}).join('');
    }}

    function _n1ApplyPixelValues(idx, showCard, showNeuron) {{
      const px = _n1GetPx(idx);
      const cells = document.querySelectorAll('#n1-grid .n1-cell');
      cells.forEach((c, i) => c.classList.toggle('selected', i === idx));

      const coord = document.getElementById('n1-coord-lbl');
      if (coord) coord.textContent = `Baris ${{px.r + 1}}, Kol ${{px.c + 1}}`;

      const pCard = document.getElementById('n1-pix-card');
      const pVal = document.getElementById('n1-pix-val');
      if (pCard) {{
        pCard.style.background = `rgb(${{px.rgb[0]}},${{px.rgb[1]}},${{px.rgb[2]}})`;
        pCard.style.color = px.gray < 0.58 ? '#FFFFFF' : '#202124';
      }}
      if (pVal) pVal.textContent = px.gray.toFixed(2);

      const nIdx = document.getElementById('n1-neuron-idx');
      const nVal = document.getElementById('n1-neuron-val');
      if (nIdx) nIdx.textContent = idx === N1_DRESS_IDX ? 'x₁' : `x${{px.idx}}`;
      if (nVal) nVal.textContent = px.gray.toFixed(2);

      const st2 = document.getElementById('n1-st2');
      const st3 = document.getElementById('n1-st3');
      const st4 = document.getElementById('n1-st4');
      if (st2) st2.className = n1Prog >= 0.14 ? 'n1-stage-on' : 'n1-stage-dim';
      if (st3) st3.className = showCard ? 'n1-stage-on' : 'n1-stage-dim';
      if (st4) st4.className = showNeuron ? 'n1-stage-on' : 'n1-stage-dim';
    }}

    function _n1CacheLayout() {{
      const wrap = document.getElementById('n1-stage-wrap');
      const canvas = document.getElementById('n1-motion-canvas');
      const photo = document.getElementById('n1-photo-box');
      const grid = document.getElementById('n1-grid');
      const pixCard = document.getElementById('n1-pix-card');
      const neuron = document.getElementById('n1-neuron-core');
      if (!wrap || !canvas || !photo || !grid || !pixCard || !neuron) return null;

      const W = wrap.clientWidth, H = wrap.clientHeight;
      if (W < 10 || H < 10) return null;
      const dpr = Math.min(3, (window.devicePixelRatio || 1) * Math.max(1, window.__STAGE_SCALE__ || 1));
      const cw = Math.round(W * dpr), ch = Math.round(H * dpr);
      if (canvas.width !== cw || canvas.height !== ch) {{ canvas.width = cw; canvas.height = ch; }}

      const hR = wrap.getBoundingClientRect();
      const sx = W / (hR.width || 1), sy = H / (hR.height || 1);
      const rel = (el) => {{
        const r = el.getBoundingClientRect();
        return {{ x: (r.left - hR.left) * sx, y: (r.top - hR.top) * sy, w: r.width * sx, h: r.height * sy }};
      }};
      n1Cache = {{
        canvas, ctx: canvas.getContext('2d'), W, H, dpr,
        rPhoto: rel(photo), rGrid: rel(grid), rPix: rel(pixCard), rNeuron: rel(neuron),
      }};
      return n1Cache;
    }}
    window.addEventListener('resize', () => {{ n1Cache = null; }});

    function _n1DrawOverlay() {{
      const L = n1Cache || _n1CacheLayout();
      if (!L) return;
      const {{ ctx, W, H, dpr, rPhoto, rGrid, rPix, rNeuron }} = L;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      const px = _n1GetPx(n1SelectedIdx);
      const pxCol = `rgb(${{px.rgb[0]}},${{px.rgb[1]}},${{px.rgb[2]}})`;
      const txtCol = px.gray < 0.58 ? '#FFFFFF' : '#202124';
      const clamp01 = (v) => (v < 0 ? 0 : (v > 1 ? 1 : v));
      const easeIO = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
      const easeOut = (t) => 1 - Math.pow(1 - t, 3);
      const qPt = (x0, y0, cx, cy, x1, y1, u) => {{
        const inv = 1 - u;
        return {{ x: inv * inv * x0 + 2 * inv * u * cx + u * u * x1, y: inv * inv * y0 + 2 * inv * u * cy + u * u * y1 }};
      }};

      const cwG = rGrid.w / N1_GRID_N, chG = rGrid.h / N1_GRID_N;
      const cwP = rPhoto.w / N1_GRID_N, chP = rPhoto.h / N1_GRID_N;
      const cellX = rGrid.x + (px.c + 0.5) * cwG;
      const cellY = rGrid.y + (px.r + 0.5) * chG;
      const pixCx = rPix.x + rPix.w / 2, pixCy = rPix.y + rPix.h / 2;
      const neuCx = rNeuron.x + rNeuron.w / 2, neuCy = rNeuron.y + rNeuron.h / 2;

      // Always outline matching pixel on Original Photo during animation!
      ctx.save();
      ctx.strokeStyle = '#FBBC04';
      ctx.fillStyle = 'rgba(251, 188, 4, 0.25)';
      ctx.lineWidth = 2.2;
      ctx.fillRect(rPhoto.x + px.c * cwP, rPhoto.y + px.r * chP, cwP, chP);
      ctx.strokeRect(rPhoto.x + px.c * cwP, rPhoto.y + px.r * chP, cwP, chP);
      ctx.restore();

      // PHASE 1 (0.00 -> 0.30): Zoom Rays expanding Foto -> 8x8 Grid!
      if (n1Prog < 0.34) {{
        const t1 = easeOut(clamp01(n1Prog / 0.28));
        const fade = n1Prog > 0.26 ? clamp01((0.34 - n1Prog) / 0.08) : 1.0;
        ctx.save();
        ctx.globalAlpha = 0.22 * fade;
        ctx.fillStyle = '#4285F4';
        ctx.beginPath();
        ctx.moveTo(rPhoto.x + rPhoto.w, rPhoto.y);
        ctx.lineTo(rPhoto.x + rPhoto.w + (rGrid.x - (rPhoto.x + rPhoto.w)) * t1, rPhoto.y + (rGrid.y - rPhoto.y) * t1);
        ctx.lineTo(rPhoto.x + rPhoto.w + (rGrid.x - (rPhoto.x + rPhoto.w)) * t1, rPhoto.y + rPhoto.h + (rGrid.y + rGrid.h - (rPhoto.y + rPhoto.h)) * t1);
        ctx.lineTo(rPhoto.x + rPhoto.w, rPhoto.y + rPhoto.h);
        ctx.closePath();
        ctx.fill();

        ctx.globalAlpha = 0.72 * fade;
        ctx.setLineDash([5, 4]);
        ctx.strokeStyle = '#4285F4';
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(rPhoto.x + rPhoto.w, rPhoto.y); ctx.lineTo(rGrid.x, rGrid.y);
        ctx.moveTo(rPhoto.x + rPhoto.w, rPhoto.y + rPhoto.h); ctx.lineTo(rGrid.x, rGrid.y + rGrid.h);
        ctx.stroke();
        ctx.restore();
      }}

      // PHASE 2 (0.28 -> 0.68): Selected 8x8 Pixel lifts off -> expands into 1 Nilai Piksel Card!
      if (n1Prog >= 0.28 && n1Prog < 0.70) {{
        const raw2 = clamp01((n1Prog - 0.28) / 0.36);
        const e2 = easeIO(raw2);
        const ctrlX = (cellX + pixCx) * 0.5;
        const ctrlY = Math.min(cellY, pixCy) - 42;

        // Dashed red guide arc
        ctx.save();
        ctx.setLineDash([5, 4]);
        ctx.strokeStyle = 'rgba(234, 67, 53, 0.80)';
        ctx.lineWidth = 2.1;
        ctx.beginPath(); ctx.moveTo(cellX, cellY); ctx.quadraticCurveTo(ctrlX, ctrlY, pixCx, pixCy); ctx.stroke();
        ctx.restore();

        if (n1Prog < 0.66) {{
          // Comet trail behind flying pixel square
          for (let g = 5; g >= 1; g--) {{
            const gp = qPt(cellX, cellY, ctrlX, ctrlY, pixCx, pixCy, Math.max(0, e2 - g * 0.05));
            const s = 18 + 20 * e2 - g * 2.5;
            ctx.save();
            ctx.globalAlpha = 0.26 * (1 - g / 6);
            _fltRoundRect(ctx, gp.x - s / 2, gp.y - s / 2, s, s, 6);
            ctx.fillStyle = pxCol; ctx.fill();
            ctx.restore();
          }}

          const pt = qPt(cellX, cellY, ctrlX, ctrlY, pixCx, pixCy, e2);
          const w = cwG + (54 - cwG) * e2;
          const h = chG + (66 - chG) * e2;
          ctx.save();
          _fltRoundRect(ctx, pt.x - w / 2 - 4, pt.y - h / 2 - 4, w + 8, h + 8, 12);
          ctx.fillStyle = 'rgba(234, 67, 53, 0.20)'; ctx.fill();
          _fltRoundRect(ctx, pt.x - w / 2, pt.y - h / 2, w, h, 4 + 8 * e2);
          ctx.fillStyle = pxCol; ctx.fill();
          ctx.strokeStyle = '#EA4335'; ctx.lineWidth = 2.4; ctx.stroke();
          if (e2 > 0.35) {{
            ctx.fillStyle = txtCol;
            ctx.font = '700 13px Roboto Mono, monospace';
            ctx.textAlign = 'center';
            ctx.fillText(px.gray.toFixed(2), pt.x, pt.y + 4);
          }}
          ctx.restore();
        }}

        // Red landing ripple on 1 Nilai Piksel card
        if (n1Prog >= 0.58) {{
          const rt = easeOut(clamp01((n1Prog - 0.58) / 0.12));
          ctx.save();
          ctx.beginPath();
          ctx.arc(pixCx, pixCy, 28 + 26 * rt, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(234, 67, 53, ${{(0.75 * (1 - rt)).toFixed(3)}})`;
          ctx.lineWidth = 2.6; ctx.stroke();
          ctx.restore();
        }}
      }}

      // PHASE 3 (0.64 -> 1.00): 1 Nilai Piksel morphs smoothly from square -> glowing blue Neuron circle!
      if (n1Prog >= 0.64) {{
        const raw3 = clamp01((n1Prog - 0.64) / 0.28);
        const e3 = easeIO(raw3);
        const ctrlX = (pixCx + neuCx) * 0.5;
        const ctrlY = Math.min(pixCy, neuCy) - 34;

        ctx.save();
        ctx.setLineDash([5, 4]);
        ctx.strokeStyle = 'rgba(26, 115, 232, 0.78)';
        ctx.lineWidth = 2.1;
        ctx.beginPath(); ctx.moveTo(pixCx, pixCy); ctx.quadraticCurveTo(ctrlX, ctrlY, neuCx, neuCy); ctx.stroke();
        ctx.restore();

        if (n1Prog < 0.94) {{
          for (let g = 5; g >= 1; g--) {{
            const gp = qPt(pixCx, pixCy, ctrlX, ctrlY, neuCx, neuCy, Math.max(0, e3 - g * 0.055));
            ctx.save();
            ctx.beginPath();
            ctx.arc(gp.x, gp.y, Math.max(4, 22 - g * 2.8), 0, Math.PI * 2);
            ctx.fillStyle = `rgba(66, 133, 244, ${{(0.26 * (1 - g / 6)).toFixed(3)}})`;
            ctx.fill();
            ctx.restore();
          }}

          const pt = qPt(pixCx, pixCy, ctrlX, ctrlY, neuCx, neuCy, e3);
          const sz = 50 + 18 * e3;
          const rad = 10 + (sz / 2 - 10) * e3;
          // Smooth color blend from real pixel RGB -> Google Blue #4285F4 (66, 133, 244)
          const rC = Math.round(px.rgb[0] + (66 - px.rgb[0]) * e3);
          const gC = Math.round(px.rgb[1] + (133 - px.rgb[1]) * e3);
          const bC = Math.round(px.rgb[2] + (244 - px.rgb[2]) * e3);
          ctx.save();
          _fltRoundRect(ctx, pt.x - sz / 2 - 4, pt.y - sz / 2 - 4, sz + 8, sz + 8, rad + 4);
          ctx.fillStyle = 'rgba(66, 133, 244, 0.22)'; ctx.fill();
          _fltRoundRect(ctx, pt.x - sz / 2, pt.y - sz / 2, sz, sz, rad);
          ctx.fillStyle = `rgb(${{rC}},${{gC}},${{bC}})`; ctx.fill();
          ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 2.4; ctx.stroke();
          ctx.fillStyle = '#FFFFFF';
          ctx.font = '700 14px Roboto Mono, monospace';
          ctx.textAlign = 'center';
          ctx.fillText(px.gray.toFixed(2), pt.x, pt.y + 5);
          ctx.restore();
        }}

        // Blue confirmation ripple on 3. 1 Neuron!
        if (n1Prog >= 0.86) {{
          const rt = easeOut(clamp01((n1Prog - 0.86) / 0.14));
          ctx.save();
          ctx.beginPath();
          ctx.arc(neuCx, neuCy, 36 + 24 * rt, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(66, 133, 244, ${{(0.85 * (1 - rt)).toFixed(3)}})`;
          ctx.lineWidth = 3.0; ctx.stroke();
          ctx.restore();
        }}
      }}
    }}

    function _tickN1(ts) {{
      if (!n1LastTs) n1LastTs = ts;
      const dt = Math.min(0.033, Math.max(0.001, (ts - n1LastTs) / 1000));
      n1LastTs = ts;
      n1Prog += dt * 0.44;
      if (n1Prog >= 1.0) {{
        n1Prog = 1.0;
        n1Playing = false;
        n1Raf = null;
        _n1SetPlayBtn(false);
        _n1ApplyPixelValues(n1SelectedIdx, true, true);
        _syncCards(['n1-bul-1', 'n1-bul-2'], -1, ['blue', 'green']);
        _syncCards(['n1-caption'], -1, ['green']);
        _n1ClearOverlay();
        return;
      }}
      _n1ApplyPixelValues(n1SelectedIdx, n1Prog >= 0.60, n1Prog >= 0.90);
      const n1PhaseIdx = n1Prog < 0.64 ? 0 : 1;
      _syncCards(['n1-bul-1', 'n1-bul-2'], n1PhaseIdx, ['blue', 'green']);
      _syncCards(['n1-caption'], 0, [n1PhaseIdx === 0 ? 'blue' : 'green']);
      _n1DrawOverlay();
      n1Raf = requestAnimationFrame(_tickN1);
    }}

    function playN1Anim() {{
      if (n1Playing && n1Raf !== null) {{
        _stopN1Anim();
        n1Prog = 1.0;
        _n1ApplyPixelValues(n1SelectedIdx, true, true);
        _n1ClearOverlay();
        return;
      }}
      _stopN1Anim();
      _n1BuildGrid();
      n1Cache = _n1CacheLayout();
      n1Prog = 0.0;
      n1Playing = true;
      n1LastTs = 0;
      _n1SetPlayBtn(true);
      const px = _n1GetPx(n1SelectedIdx);
      const cap = document.getElementById('n1-caption');
      if (cap) cap.innerHTML = `<strong>1 Piksel → 1 Neuron:</strong> Foto di-<em>zoom</em> jadi <code>8×8</code> → ambil <strong>Baris ${{px.r + 1}}, Kol ${{px.c + 1}}</strong> (<code>${{px.gray.toFixed(2)}}</code>) → masuk ke <strong>1 Neuron</strong>!`;
      _n1ApplyPixelValues(n1SelectedIdx, false, false);
      _n1DrawOverlay();
      n1Raf = requestAnimationFrame(_tickN1);
    }}

    function pickN1Pixel(idx) {{
      _stopN1Anim();
      _n1BuildGrid();
      n1SelectedIdx = idx;
      n1Cache = _n1CacheLayout();
      n1Prog = 0.28; // jump straight into Pick -> Morph!
      n1Playing = true;
      n1LastTs = 0;
      _n1SetPlayBtn(true);
      const px = _n1GetPx(idx);
      const cap = document.getElementById('n1-caption');
      if (cap) cap.innerHTML = `<strong>Piksel Dipilih (Baris ${{px.r + 1}}, Kol ${{px.c + 1}}):</strong> Nilai <code>${{px.gray.toFixed(2)}}</code> terangkat dari grid <code>8×8</code> → berubah menjadi <strong>Neuron ${{idx === N1_DRESS_IDX ? 'x₁' : 'x' + px.idx}}</strong>!`;
      _n1ApplyPixelValues(idx, false, false);
      _n1DrawOverlay();
      n1Raf = requestAnimationFrame(_tickN1);
    }}

    function nextN1Sample() {{
      n1SamplePos = (n1SamplePos + 1) % N1_SAMPLE_CYCLE.length;
      pickN1Pixel(N1_SAMPLE_CYCLE[n1SamplePos]);
    }}

    function resetN1Anim() {{
      _stopN1Anim();
      _n1BuildGrid();
      n1SelectedIdx = N1_DRESS_IDX;
      n1SamplePos = 0;
      n1Prog = 1.0;
      const cap = document.getElementById('n1-caption');
      if (cap) cap.textContent = 'Setiap 1 kotak piksel pada foto Elsa diwakili oleh tepat 1 lingkaran Neuron yang memegang angkanya.';
      _syncCards(['n1-bul-1', 'n1-bul-2'], -1, ['blue', 'green']);
      _syncCards(['n1-caption'], -1, ['green']);
      _n1ApplyPixelValues(n1SelectedIdx, true, true);
      _n1ClearOverlay();
    }}
    _n1BuildGrid();
    _n1ApplyPixelValues(n1SelectedIdx, true, true);

    // =========================================================================
    // ANIMASI INTERAKTIF FLATTEN (Slide 21): 4x4 Real Elsa -> Input Layer
    // =========================================================================
    const FLT_N = 4;
    const FLT_TOTAL = FLT_N * FLT_N; // 16 piksel nyata
    const FLT_ROW_COL = ['#4285F4', '#EA4335', '#E37400', '#34A853'];
    const FLT_ROW_BG  = ['#E8F0FE', '#FCE8E6', '#FEF7E0', '#E6F4EA'];
    const FLT_ROW_LBL = ['Brs 1', 'Brs 2', 'Brs 3', 'Brs 4'];
    let fltExtracted = FLT_TOTAL; // number of cropped photo tiles landed in 4x4 grid (0..16)
    let fltPlaced = FLT_TOTAL;    // number of pixels landed in Input Layer (0..16)
    let fltPhase = 'idle';        // 'idle' | 'split' | 'flatten'
    let fltSplitProg = 1.0;       // 0..1 progress of Phase 1 (Photo -> 4x4 grid split)
    let fltFlyIdx = -1;           // index (0..15) currently in flight (4x4 -> Input Layer)
    let fltFlyT = 0;              // 0..1 progress of current flying pixel in Phase 2
    let fltAutoPlay = false;
    let fltRafId = null;
    let fltLastTs = 0;
    let fltSplitCache = null;

    function _fltRoundRect(ctx, x, y, w, h, r) {{
      const rad = Math.min(r, w / 2, h / 2);
      ctx.beginPath();
      ctx.moveTo(x + rad, y);
      ctx.arcTo(x + w, y, x + w, y + h, rad);
      ctx.arcTo(x + w, y + h, x, y + h, rad);
      ctx.arcTo(x, y + h, x, y, rad);
      ctx.arcTo(x, y, x + w, y, rad);
      ctx.closePath();
    }}

    function _fltSplitCellWindow(idx) {{
      const tStart = idx * 0.056;
      const tEnd = tStart + 0.16;
      return {{ tStart, tEnd }};
    }}

    function _fltCacheSplitLayout() {{
      const wrap = document.getElementById('flt-stage-wrap');
      const ov = document.getElementById('flt-split-canvas');
      const photo = document.getElementById('flt-photo-box');
      const cvs = document.getElementById('flatten-canvas');
      if (!wrap || !ov || !photo || !cvs) return null;
      const wRect = wrap.getBoundingClientRect();
      const cw = wrap.clientWidth || wRect.width || 1000;
      const ch = wrap.clientHeight || wRect.height || 360;
      if (!wRect.width || !wRect.height) return null;
      const sx = wRect.width / cw;
      const sy = wRect.height / ch;
      const toLocal = (el) => {{
        const r = el.getBoundingClientRect();
        return {{
          x: (r.left - wRect.left) / sx,
          y: (r.top - wRect.top) / sy,
          w: r.width / sx,
          h: r.height / sy,
        }};
      }};
      const rPhoto = toLocal(photo);
      const rCvsBox = toLocal(cvs);
      // Compute actual rendered rectangle of 800x340 canvas inside rCvsBox (object-fit: contain)
      const natW = cvs.width || 800, natH = cvs.height || 340;
      const fitScale = Math.min(rCvsBox.w / natW, rCvsBox.h / natH);
      const drawW = natW * fitScale;
      const drawH = natH * fitScale;
      const ox = rCvsBox.x + (rCvsBox.w - drawW) / 2;
      const oy = rCvsBox.y + (rCvsBox.h - drawH) / 2;

      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      ov.width = Math.round(cw * dpr);
      ov.height = Math.round(ch * dpr);
      const ctx = ov.getContext('2d');

      return {{ ctx, dpr, cw, ch, rPhoto, ox, oy, fitScale }};
    }}

    function _fltClearSplitOverlay() {{
      const ov = document.getElementById('flt-split-canvas');
      if (!ov) return;
      const ctx = ov.getContext('2d');
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, ov.width, ov.height);
    }}

    function _fltDrawSplitOverlay() {{
      if (fltPhase !== 'split') {{
        _fltClearSplitOverlay();
        return;
      }}
      const L = fltSplitCache || (fltSplitCache = _fltCacheSplitLayout());
      if (!L) return;
      const {{ ctx, dpr, cw, ch, rPhoto, ox, oy, fitScale }} = L;
      const img = document.getElementById('flt-elsa-img');
      const imgReady = img && img.complete && img.naturalWidth > 0;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, cw, ch);

      const gx0 = 58, gy0 = 44, cell = 54, gap = 6;
      const srcCellW = rPhoto.w / FLT_N;
      const srcCellH = rPhoto.h / FLT_N;
      const dstCellW = cell * fitScale;
      const dstCellH = cell * fitScale;
      const smooth = (a, b, v) => {{
        const u = Math.max(0, Math.min(1, (v - a) / (b - a)));
        return u * u * (3 - 2 * u);
      }};

      // Subtle tint over already-lifted cells on Foto Elsa so the slice-off is unmistakable
      FLATTEN_PIXELS.forEach((px, idx) => {{
        const {{ tStart, tEnd }} = _fltSplitCellWindow(idx);
        const sx0 = rPhoto.x + px.col * srcCellW;
        const sy0 = rPhoto.y + px.row * srcCellH;
        if (fltSplitProg >= tStart && fltSplitProg < tEnd) {{
          ctx.save();
          ctx.strokeStyle = '#FBBC04';
          ctx.lineWidth = 2.4;
          ctx.strokeRect(sx0 + 1, sy0 + 1, srcCellW - 2, srcCellH - 2);
          ctx.restore();
        }}
      }});

      // Draw each flying cropped piece of Foto Elsa -> morphing into colored numeric 4x4 cell!
      FLATTEN_PIXELS.forEach((px, idx) => {{
        const {{ tStart, tEnd }} = _fltSplitCellWindow(idx);
        if (fltSplitProg < tStart || fltSplitProg >= tEnd) return;
        const rawT = (fltSplitProg - tStart) / (tEnd - tStart);
        const e = rawT < 0.5 ? 2 * rawT * rawT : 1 - Math.pow(-2 * rawT + 2, 2) / 2;
        const inv = 1 - e;

        const srcCx = rPhoto.x + (px.col + 0.5) * srcCellW;
        const srcCy = rPhoto.y + (px.row + 0.5) * srcCellH;
        const dstCx = ox + (gx0 + px.col * (cell + gap) + cell / 2) * fitScale;
        const dstCy = oy + (gy0 + px.row * (cell + gap) + cell / 2) * fitScale;

        const ctrlX = (srcCx + dstCx) / 2;
        const ctrlY = Math.min(srcCy, dstCy) - (22 + px.row * 4);
        const cx = inv * inv * srcCx + 2 * inv * e * ctrlX + e * e * dstCx;
        const cy = inv * inv * srcCy + 2 * inv * e * ctrlY + e * e * dstCy;

        const pop = 1 + 0.14 * Math.sin(Math.PI * rawT);
        const w = (srcCellW + (dstCellW - srcCellW) * e) * pop;
        const h = (srcCellH + (dstCellH - srcCellH) * e) * pop;
        const rad = (3 + 5 * e) * fitScale;
        const x = cx - w / 2;
        const y = cy - h / 2;

        // Faint curved guide trail behind flying slice
        ctx.save();
        ctx.strokeStyle = FLT_ROW_COL[px.row];
        ctx.globalAlpha = 0.34;
        ctx.lineWidth = 1.6;
        ctx.setLineDash([4, 3]);
        ctx.beginPath();
        ctx.moveTo(srcCx, srcCy);
        ctx.quadraticCurveTo(ctrlX, ctrlY, cx, cy);
        ctx.stroke();
        ctx.restore();

        // Card container with crisp shadow
        ctx.save();
        ctx.shadowColor = 'rgba(26, 115, 232, 0.28)';
        ctx.shadowBlur = 10;
        _fltRoundRect(ctx, x, y, w, h, rad);
        ctx.fillStyle = `rgb(${{px.rgb[0]}},${{px.rgb[1]}},${{px.rgb[2]}})`;
        ctx.fill();
        ctx.restore();

        // Crossfade real Elsa photo crop (1 -> 0) into colored pixel tile + number (0 -> 1)
        const photoAlpha = 1 - smooth(0.45, 0.94, rawT);
        if (imgReady && photoAlpha > 0.02) {{
          ctx.save();
          _fltRoundRect(ctx, x, y, w, h, rad);
          ctx.clip();
          ctx.globalAlpha = photoAlpha;
          const natSliceW = img.naturalWidth / FLT_N;
          const natSliceH = img.naturalHeight / FLT_N;
          ctx.drawImage(
            img,
            px.col * natSliceW, px.row * natSliceH, natSliceW, natSliceH,
            x, y, w, h
          );
          ctx.restore();
        }}

        const numAlpha = smooth(0.38, 0.90, rawT);
        if (numAlpha > 0.02) {{
          ctx.save();
          ctx.globalAlpha = numAlpha;
          const tc = px.gray < 0.58 ? '#FFFFFF' : '#202124';
          ctx.fillStyle = tc;
          ctx.textAlign = 'center';
          ctx.font = `700 ${{(9.5 * fitScale).toFixed(1)}}px Roboto Mono, monospace`;
          ctx.fillText(`x${{px.idx}}`, cx, y + h * 0.39);
          ctx.font = `700 ${{(12 * fitScale).toFixed(1)}}px Roboto Mono, monospace`;
          ctx.fillText(px.gray.toFixed(2), cx, y + h * 0.72);
          ctx.restore();
        }}

        // Crisp row-colored border
        ctx.save();
        _fltRoundRect(ctx, x, y, w, h, rad);
        ctx.strokeStyle = rawT < 0.55 ? '#FBBC04' : FLT_ROW_COL[px.row];
        ctx.lineWidth = 2.3;
        ctx.stroke();
        ctx.restore();
      }});
    }}

    function drawFlattenFrame() {{
      const canvas = document.getElementById('flatten-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, W, H);

      const gx0 = 58, gy0 = 44, cell = 54, gap = 6;
      const gridW = FLT_N * cell + (FLT_N - 1) * gap;
      const gridH = FLT_N * cell + (FLT_N - 1) * gap;
      const slotX = 538, slotY0 = 56, slotGap = 17.5, slotR = 7.4;

      const cellCenter = (r, c) => ({{
        x: gx0 + c * (cell + gap) + cell / 2,
        y: gy0 + r * (cell + gap) + cell / 2,
      }});
      const slotCenter = (idx) => ({{
        x: slotX,
        y: slotY0 + idx * slotGap,
      }});

      // Title: 2D Grid
      ctx.fillStyle = '#202124';
      ctx.font = '700 13px Poppins, Arial';
      ctx.textAlign = 'center';
      ctx.fillText('Gambar 2D (4×4 = 16 Piksel)', gx0 + gridW / 2, 24);

      // Row badges on left of grid
      for (let r = 0; r < FLT_N; r++) {{
        const cy = gy0 + r * (cell + gap) + cell / 2;
        _fltRoundRect(ctx, 6, cy - 12, 44, 24, 7);
        ctx.fillStyle = FLT_ROW_BG[r]; ctx.fill();
        ctx.strokeStyle = FLT_ROW_COL[r]; ctx.lineWidth = 1.6; ctx.stroke();
        ctx.fillStyle = FLT_ROW_COL[r];
        ctx.font = '700 10px Poppins, Arial';
        ctx.textAlign = 'center';
        ctx.fillText(FLT_ROW_LBL[r], 28, cy + 3.5);
      }}

      // Draw 4x4 real Elsa pixel cells (or dashed waiting placeholders before photo split lands!)
      FLATTEN_PIXELS.forEach((px, idx) => {{
        const x = gx0 + px.col * (cell + gap);
        const y = gy0 + px.row * (cell + gap);
        const isExtracted = idx < fltExtracted;
        const isLanded = idx < fltPlaced;
        const isFlying = fltPhase === 'flatten' && idx === fltFlyIdx;

        if (!isExtracted) {{
          const {{ tStart, tEnd }} = _fltSplitCellWindow(idx);
          const incoming = fltPhase === 'split' && fltSplitProg >= tStart && fltSplitProg < tEnd;
          ctx.save();
          ctx.setLineDash([4, 3]);
          _fltRoundRect(ctx, x, y, cell, cell, 8);
          ctx.fillStyle = incoming ? '#FEF7E0' : '#F8F9FA';
          ctx.fill();
          ctx.strokeStyle = incoming ? '#FBBC04' : '#DADCE0';
          ctx.lineWidth = incoming ? 2.2 : 1.4;
          ctx.stroke();
          ctx.restore();
          ctx.fillStyle = incoming ? '#B06000' : '#9AA0A6';
          ctx.textAlign = 'center';
          ctx.font = '700 9.5px Roboto Mono, monospace';
          ctx.fillText(`x${{px.idx}}`, x + cell / 2, y + 31);
          return;
        }}

        _fltRoundRect(ctx, x, y, cell, cell, 8);
        ctx.fillStyle = `rgb(${{px.rgb[0]}},${{px.rgb[1]}},${{px.rgb[2]}})`;
        ctx.fill();

        ctx.strokeStyle = isFlying ? '#FBBC04' : FLT_ROW_COL[px.row];
        ctx.lineWidth = isFlying ? 4.0 : 2.3;
        ctx.stroke();

        if (isFlying) {{
          ctx.save();
          _fltRoundRect(ctx, x - 3, y - 3, cell + 6, cell + 6, 10);
          ctx.strokeStyle = 'rgba(251,188,4,0.72)';
          ctx.lineWidth = 3;
          ctx.stroke();
          ctx.restore();
        }}

        const tc = px.gray < 0.58 ? '#FFFFFF' : '#202124';
        ctx.fillStyle = tc;
        ctx.textAlign = 'center';
        ctx.font = '700 9.5px Roboto Mono, monospace';
        ctx.fillText(`x${{px.idx}}`, x + cell / 2, y + 20);
        ctx.font = '700 12px Roboto Mono, monospace';
        ctx.fillText(px.gray.toFixed(2), x + cell / 2, y + 38);

        if (isLanded) {{
          ctx.beginPath();
          ctx.arc(x + cell - 9, y + 9, 6.0, 0, Math.PI * 2);
          ctx.fillStyle = FLT_ROW_COL[px.row];
          ctx.fill();
          ctx.fillStyle = '#FFFFFF';
          ctx.font = '700 8px Arial';
          ctx.fillText('✓', x + cell - 9, y + 11.8);
        }}
      }});

      // Bottom scan direction hint under grid
      ctx.fillStyle = '#5F6368';
      ctx.font = '600 10.5px Roboto, Arial';
      ctx.textAlign = 'center';
      ctx.fillText('Urutan pindai: kiri → kanan, lalu turun baris', gx0 + gridW / 2, gy0 + gridH + 22);

      // Center Flatten Badge
      _fltRoundRect(ctx, 344, 6, 108, 28, 9);
      ctx.fillStyle = '#FEF7E0'; ctx.fill();
      ctx.strokeStyle = '#FBBC04'; ctx.lineWidth = 2; ctx.stroke();
      ctx.fillStyle = '#B06000';
      ctx.font = '700 12px Poppins, Arial';
      ctx.textAlign = 'center';
      ctx.fillText('FLATTEN', 398, 24);

      ctx.fillStyle = '#5F6368';
      ctx.font = '600 10px Roboto, Arial';
      ctx.fillText('Susun ke bawah', 398, 48);

      // Right: Input Layer vertical capsule
      _fltRoundRect(ctx, 510, 6, 282, 326, 16);
      ctx.fillStyle = '#F8F9FA'; ctx.fill();
      ctx.strokeStyle = '#4285F4'; ctx.lineWidth = 2.6; ctx.stroke();

      ctx.fillStyle = '#1A73E8';
      ctx.font = '700 13px Poppins, Arial';
      ctx.textAlign = 'center';
      ctx.fillText('INPUT LAYER', 651, 24);
      ctx.fillStyle = '#5F6368';
      ctx.font = '600 9.8px Roboto Mono, monospace';
      ctx.fillText(`(1 Kolom Vertikal · ${{fltPlaced}} / ${{FLT_TOTAL}} Neuron)`, 651, 39);

      // Draw 16 vertical neuron slots
      FLATTEN_PIXELS.forEach((px, idx) => {{
        const pos = slotCenter(idx);
        const isLanded = idx < fltPlaced;
        const isTarget = fltPhase === 'flatten' && idx === fltFlyIdx;

        if (isLanded) {{
          ctx.beginPath();
          ctx.arc(pos.x, pos.y, slotR, 0, Math.PI * 2);
          ctx.fillStyle = FLT_ROW_COL[px.row];
          ctx.fill();
          ctx.strokeStyle = '#FFFFFF';
          ctx.lineWidth = 1.6;
          ctx.stroke();

          ctx.fillStyle = '#FFFFFF';
          ctx.font = '700 7.6px Roboto Mono, monospace';
          ctx.textAlign = 'center';
          ctx.fillText(String(px.idx), pos.x, pos.y + 2.7);

          ctx.fillStyle = FLT_ROW_COL[px.row];
          ctx.font = '700 10px Roboto Mono, monospace';
          ctx.textAlign = 'left';
          ctx.fillText(`x${{px.idx}}`, pos.x + 14, pos.y + 3.2);

          ctx.fillStyle = '#202124';
          ctx.font = '700 10px Roboto Mono, monospace';
          ctx.fillText(`= ${{px.gray.toFixed(2)}}`, pos.x + 42, pos.y + 3.2);

          ctx.fillStyle = '#5F6368';
          ctx.font = '400 9.4px Roboto, Arial';
          ctx.fillText(`(Baris ${{px.row + 1}}, Kol ${{px.col + 1}})`, pos.x + 96, pos.y + 3.2);
        }} else {{
          ctx.save();
          ctx.setLineDash([2.5, 2.5]);
          ctx.beginPath();
          ctx.arc(pos.x, pos.y, slotR, 0, Math.PI * 2);
          ctx.fillStyle = isTarget ? '#FEF7E0' : '#FFFFFF';
          ctx.fill();
          ctx.strokeStyle = isTarget ? '#FBBC04' : '#CFD4DA';
          ctx.lineWidth = isTarget ? 2.0 : 1.3;
          ctx.stroke();
          ctx.restore();

          ctx.fillStyle = isTarget ? '#B06000' : '#9AA0A6';
          ctx.font = '600 9.5px Roboto Mono, monospace';
          ctx.textAlign = 'left';
          ctx.fillText(`x${{px.idx}} (menunggu...)`, pos.x + 14, pos.y + 3.2);
        }}
      }});

      // If idle & completed (16/16), show clean 4-row directional guide arrows
      if (fltPhase === 'idle' && fltFlyIdx === -1 && fltPlaced === FLT_TOTAL) {{
        [0, 1, 2, 3].forEach((r) => {{
          const sy = gy0 + r * (cell + gap) + cell / 2;
          const ey = slotY0 + (r * FLT_N + 1.5) * slotGap;
          const curveBias = r === 0 ? -14 : r === 1 ? -5 : r === 2 ? 5 : 16;
          ctx.save();
          ctx.strokeStyle = FLT_ROW_COL[r];
          ctx.lineWidth = 2.2;
          ctx.beginPath();
          ctx.moveTo(gx0 + gridW + 8, sy);
          ctx.quadraticCurveTo(398, (sy + ey) / 2 + curveBias, 502, ey);
          ctx.stroke();
          ctx.fillStyle = FLT_ROW_COL[r];
          ctx.beginPath();
          ctx.moveTo(506, ey);
          ctx.lineTo(496, ey - 5.2);
          ctx.lineTo(496, ey + 5.2);
          ctx.closePath();
          ctx.fill();
          ctx.restore();
        }});
      }}

      // Phase 2: Flying pixel -> morphing into Neuron circle along Bezier curve!
      if (fltPhase === 'flatten' && fltFlyIdx >= 0 && fltFlyIdx < FLATTEN_PIXELS.length) {{
        const px = FLATTEN_PIXELS[fltFlyIdx];
        const src = cellCenter(px.row, px.col);
        const dst = slotCenter(fltFlyIdx);
        const ctrlX = (src.x + dst.x) / 2;
        const ctrlY = Math.min(src.y, dst.y) - 42;
        const t = Math.max(0, Math.min(1, fltFlyT));
        const e = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
        const inv = 1 - e;
        const fx = inv * inv * src.x + 2 * inv * e * ctrlX + e * e * dst.x;
        const fy = inv * inv * src.y + 2 * inv * e * ctrlY + e * e * dst.y;

        ctx.save();
        ctx.setLineDash([6, 4]);
        ctx.strokeStyle = FLT_ROW_COL[px.row];
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(src.x, src.y);
        ctx.quadraticCurveTo(ctrlX, ctrlY, dst.x, dst.y);
        ctx.stroke();
        ctx.restore();

        const sz = 42 - 14 * e;
        const rad = 8 + (sz / 2 - 8) * e;
        ctx.save();
        ctx.shadowColor = 'rgba(251, 188, 4, 0.55)';
        ctx.shadowBlur = 14;
        _fltRoundRect(ctx, fx - sz / 2, fy - sz / 2, sz, sz, rad);
        ctx.fillStyle = FLT_ROW_COL[px.row];
        ctx.fill();
        ctx.strokeStyle = '#FBBC04';
        ctx.lineWidth = 2.8;
        ctx.stroke();
        ctx.restore();

        ctx.fillStyle = '#FFFFFF';
        ctx.textAlign = 'center';
        ctx.font = '700 8.8px Roboto Mono, monospace';
        ctx.fillText(`x${{px.idx}}`, fx, fy - 1);
        ctx.font = '700 8.8px Roboto Mono, monospace';
        ctx.fillText(px.gray.toFixed(2), fx, fy + 9.5);
      }}

      // Render Phase 1 photo-to-4x4 split overlay if active
      _fltDrawSplitOverlay();

      // Sync 3 bottom explanation cards live with the animation phase!
      let fltCardIdx = -1;
      if (fltPhase === 'split') {{
        fltCardIdx = 0; // Card 1: Pindai Kiri -> Kanan, Atas -> Bawah
      }} else if (fltPhase === 'flatten' && fltFlyIdx >= 0) {{
        fltCardIdx = fltFlyT < 0.72 ? 1 : 2; // Card 2 while flying/morphing -> Card 3 on landing!
      }}
      _syncCards(['flt-card-1', 'flt-card-2', 'flt-card-3'], fltCardIdx, ['blue', 'yellow', 'green']);

      // Update status pill
      const st = document.getElementById('flatten-status');
      if (st) {{
        if (fltPhase === 'split') {{
          st.className = 'pill yellow';
          st.textContent = `Tahap 1/2: Memotong Foto Elsa → Grid 4×4 (${{fltExtracted}} / ${{FLT_TOTAL}})`;
        }} else if (fltPhase === 'flatten' && fltFlyIdx >= 0) {{
          const px = FLATTEN_PIXELS[fltFlyIdx];
          st.className = 'pill yellow';
          st.textContent = `Tahap 2/2: Memindahkan x${{px.idx}} (Baris ${{px.row + 1}}, Kol ${{px.col + 1}}) → Slot #${{px.idx}}`;
        }} else if (fltExtracted === 0) {{
          st.className = 'pill blue';
          st.textContent = 'Siap! Klik "▶ Play" atau "+1 Piksel"';
        }} else if (fltPlaced === 0) {{
          st.className = 'pill blue';
          st.textContent = 'Grid 4×4 siap! Klik "+1 Piksel" untuk susun ke Input Layer';
        }} else if (fltPlaced < FLT_TOTAL) {{
          st.className = 'pill blue';
          st.textContent = `Input Layer: ${{fltPlaced}} / ${{FLT_TOTAL}} neuron tersusun`;
        }} else {{
          st.className = 'pill green';
          st.textContent = `Input Layer: ${{FLT_TOTAL}} / ${{FLT_TOTAL}} neuron (Selesai!)`;
        }}
      }}
    }}

    function _fltSetPlayBtn(playing) {{
      const b = document.getElementById('flt-btn-play');
      if (!b) return;
      b.textContent = playing ? '■ Stop' : '▶ Play';
      b.style.background = playing ? '#EA4335' : '#34A853';
      b.style.borderColor = playing ? '#EA4335' : '#34A853';
    }}

    function _stopFltRaf() {{
      if (fltRafId !== null) {{ cancelAnimationFrame(fltRafId); fltRafId = null; }}
      fltAutoPlay = false;
      fltPhase = 'idle';
      _fltSetPlayBtn(false);
      _fltClearSplitOverlay();
    }}

    function _tickFltAnim(ts) {{
      if (!fltLastTs) fltLastTs = ts;
      const dt = Math.min(0.05, (ts - fltLastTs) / 1000);
      fltLastTs = ts;

      if (fltPhase === 'split') {{
        fltSplitProg = Math.min(1.0, fltSplitProg + dt * 0.48); // ~1.78s silky 16-piece cascade!
        let landed = 0;
        for (let i = 0; i < FLT_TOTAL; i++) {{
          if (fltSplitProg >= _fltSplitCellWindow(i).tEnd) landed += 1;
        }}
        fltExtracted = landed;
        if (fltSplitProg >= 1.0) {{
          fltExtracted = FLT_TOTAL;
          _fltClearSplitOverlay();
          if (fltAutoPlay) {{
            // Seamlessly transition into Phase 2: Flatten 4x4 -> Input Layer!
            fltPhase = 'flatten';
            fltPlaced = 0;
            fltFlyIdx = 0;
            fltFlyT = 0;
            drawFlattenFrame();
            fltRafId = requestAnimationFrame(_tickFltAnim);
            return;
          }} else {{
            fltPhase = 'idle';
            fltRafId = null;
            drawFlattenFrame();
            return;
          }}
        }}
        drawFlattenFrame();
        fltRafId = requestAnimationFrame(_tickFltAnim);
        return;
      }}

      // Phase 2: Flatten 4x4 -> Input Layer
      const speed = fltAutoPlay ? 2.55 : 2.9;
      fltFlyT += dt * speed;
      if (fltFlyT >= 1.0) {{
        fltPlaced = fltFlyIdx + 1;
        fltFlyT = 0;
        if (fltAutoPlay && fltPlaced < FLT_TOTAL) {{
          fltFlyIdx = fltPlaced;
        }} else {{
          fltFlyIdx = -1;
          fltPhase = 'idle';
          fltAutoPlay = false;
          fltRafId = null;
          _fltSetPlayBtn(false);
          drawFlattenFrame();
          return;
        }}
      }}
      drawFlattenFrame();
      fltRafId = requestAnimationFrame(_tickFltAnim);
    }}

    function playFlattenAnim() {{
      if (fltAutoPlay) {{
        _stopFltRaf();
        fltFlyIdx = -1;
        fltFlyT = 0;
        drawFlattenFrame();
        return;
      }}
      _stopFltRaf();
      fltSplitCache = _fltCacheSplitLayout();
      fltExtracted = 0;
      fltPlaced = 0;
      fltSplitProg = 0.0;
      fltFlyIdx = -1;
      fltFlyT = 0;
      fltPhase = 'split';
      fltAutoPlay = true;
      fltLastTs = 0;
      _fltSetPlayBtn(true);
      drawFlattenFrame();
      fltRafId = requestAnimationFrame(_tickFltAnim);
    }}

    function stepFlattenAnim() {{
      if (fltAutoPlay) _stopFltRaf();
      if (fltPhase === 'split') {{
        // Finish split immediately if mid-split
        _stopFltRaf();
        fltExtracted = FLT_TOTAL;
        fltSplitProg = 1.0;
        drawFlattenFrame();
        return;
      }}
      if (fltExtracted < FLT_TOTAL) {{
        // Step 1: Animate Foto Elsa -> 4x4 grid first, then stop ready for +1 Piksel!
        _stopFltRaf();
        fltSplitCache = _fltCacheSplitLayout();
        fltExtracted = 0;
        fltPlaced = 0;
        fltSplitProg = 0.0;
        fltPhase = 'split';
        fltAutoPlay = false;
        fltLastTs = 0;
        drawFlattenFrame();
        fltRafId = requestAnimationFrame(_tickFltAnim);
        return;
      }}
      if (fltFlyIdx >= 0) {{
        fltPlaced = fltFlyIdx + 1;
        fltFlyIdx = -1;
      }}
      if (fltPlaced >= FLT_TOTAL) {{
        fltPlaced = 0;
      }}
      fltPhase = 'flatten';
      fltFlyIdx = fltPlaced;
      fltFlyT = 0;
      fltAutoPlay = false;
      fltLastTs = 0;
      if (fltRafId !== null) cancelAnimationFrame(fltRafId);
      fltRafId = requestAnimationFrame(_tickFltAnim);
    }}

    function resetFlattenAnim() {{
      _stopFltRaf();
      fltExtracted = 0;
      fltPlaced = 0;
      fltSplitProg = 0.0;
      fltFlyIdx = -1;
      fltFlyT = 0;
      drawFlattenFrame();
    }}

    function completeFlattenAnim() {{
      _stopFltRaf();
      fltExtracted = FLT_TOTAL;
      fltPlaced = FLT_TOTAL;
      fltSplitProg = 1.0;
      fltFlyIdx = -1;
      fltFlyT = 0;
      drawFlattenFrame();
    }}

    function setFlattenPdfState(mode) {{
      _stopFltRaf();
      if (mode === 'mid') {{
        fltExtracted = FLT_TOTAL;
        fltPhase = 'flatten';
        fltPlaced = 9;
        fltFlyIdx = 9;   // x10 (Row 3, Col 2 — Elsa's blue dress!) frozen gracefully mid-flight!
        fltFlyT = 0.54;
      }} else {{
        fltExtracted = FLT_TOTAL;
        fltPhase = 'idle';
        fltPlaced = FLT_TOTAL;
        fltFlyIdx = -1;
        fltFlyT = 0;
      }}
      drawFlattenFrame();
    }}
    completeFlattenAnim();

    // =========================================================================
    // SIMULATOR #3 (Slide 22): Silky 60fps Per-Pixel Motion Engine (Zero Reflow!)
    // Architecture for butter-smooth playback:
    //   1. Layout coordinates cached ONCE per run/resize (0 getBoundingClientRect in RAF!)
    //   2. Dirty-checked DOM updates (0 innerHTML thrashing in RAF!)
    //   3. Pure vector glow halos & tapered motion trails (0 expensive shadowBlur!)
    //   4. Smooth anticipation -> Bezier glide -> landing ripple -> smooth RGB split -> settle glow
    // =========================================================================
    const IN_GRID_N = (ELSA_ENDS && ELSA_ENDS.grid_n) ? ELSA_ENDS.grid_n : 8;
    const IN_GRID = (ELSA_ENDS && ELSA_ENDS.grid) ? ELSA_ENDS.grid : [];
    const IN_DRESS_IDX = (ELSA_ENDS && typeof ELSA_ENDS.dress_idx === 'number') ? ELSA_ENDS.dress_idx : 35;
    const IN_TOTAL_STEPS = 6;
    const IN_STREAM_IDXS = [
      3, 4, 5, 6, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29,
      31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61
    ];
    let inAnimRaf = null;
    let inCompletedSteps = IN_TOTAL_STEPS; // 0..6
    let inActiveStep = 0;                  // 1..6, 99 (custom pixel click), or 0 (idle)
    let inStepProg = 0;                    // 0..1 progress of active animation step
    let inVisualFrac = 1.0;                // smoothly interpolated 1D strip reveal (0..1)
    let inAutoMode = false;
    let inLastTs = 0;
    let inTracedRow = -1;                  // interactive clicked neuron trace
    let inCustomPixel = null;              // clicked pixel object from IN_GRID
    let inLayoutCache = null;              // cached DOM geometry (0 reflows during animation!)
    let inLastStageKey = '';
    let inLastCalloutKey = '';
    let inLastTotText = '';
    let inLastClipPct = -1;

    const IN_DEFAULT_CALLOUT = '<strong>Aturan cepat:</strong> Pada foto berwarna (<code>RGB = 3</code>), tiap <strong>1 kotak piksel</strong> pecah menjadi <strong>3 neuron</strong> (<code>R, G, B</code>). Klik <strong>▶ Play</strong>, <strong>⏭ +1 Piksel</strong>, atau klik kotak piksel mana saja pada Foto Elsa!';

    function _inSetPlayBtn(isPlaying) {{
      const btn = document.getElementById('in-btn-play');
      if (!btn) return;
      btn.textContent = isPlaying ? '■ Stop' : '▶ Play';
      btn.style.background = isPlaying ? '#EA4335' : '#34A853';
      btn.style.borderColor = isPlaying ? '#EA4335' : '#34A853';
    }}

    function _stopInAnim() {{
      if (inAnimRaf !== null) {{
        cancelAnimationFrame(inAnimRaf);
        inAnimRaf = null;
      }}
      inAutoMode = false;
      _inSetPlayBtn(false);
    }}

    function _inRelRect(el, host, hRect, sx, sy) {{
      const r = el.getBoundingClientRect();
      return {{
        x: (r.left - hRect.left) * sx,
        y: (r.top - hRect.top) * sy,
        w: r.width * sx,
        h: r.height * sy,
      }};
    }}

    function _inCacheLayout() {{
      const wrap = document.getElementById('in-hero-wrap');
      const canvas = document.getElementById('in-motion-canvas');
      const imgFrame = document.getElementById('in-img-frame');
      const stripWrap = document.getElementById('in-strip-wrap');
      if (!wrap || !canvas || !imgFrame || !stripWrap) return null;
      const W = wrap.clientWidth, H = wrap.clientHeight;
      if (W < 10 || H < 10) return null;

      const dpr = Math.min(3, (window.devicePixelRatio || 1) * Math.max(1, window.__STAGE_SCALE__ || 1));
      const cwPx = Math.round(W * dpr), chPx = Math.round(H * dpr);
      if (canvas.width !== cwPx || canvas.height !== chPx) {{
        canvas.width = cwPx;
        canvas.height = chPx;
      }}

      const hRect = wrap.getBoundingClientRect();
      const sx = W / (hRect.width || 1);
      const sy = H / (hRect.height || 1);
      const rImg = _inRelRect(imgFrame, wrap, hRect, sx, sy);
      const rStrip = _inRelRect(stripWrap, wrap, hRect, sx, sy);
      const arrow2 = document.getElementById('in-arrow-2');
      const rArr2 = arrow2 ? _inRelRect(arrow2, wrap, hRect, sx, sy) : {{ x: rStrip.x + 220, y: rStrip.y + rStrip.h * 0.5, w: 44, h: 40 }};

      const circleEls = Array.from(document.querySelectorAll('#in-layer-nodes .in-node-circle'));
      const nodeRows = Array.from(document.querySelectorAll('#in-layer-nodes .in-node-row'));
      const circles = circleEls.map((el) => {{
        const rr = _inRelRect(el, wrap, hRect, sx, sy);
        return {{ x: rr.x + rr.w / 2, y: rr.y + rr.h / 2 }};
      }});
      const ellEl = nodeRows[3] || circleEls[2];
      const rEll = ellEl ? _inRelRect(ellEl, wrap, hRect, sx, sy) : {{ x: rArr2.x + 70, y: rStrip.y + rStrip.h * 0.55, w: 32, h: 24 }};
      const midPt = {{ x: rEll.x + 18, y: rEll.y + rEll.h / 2 }};

      inLayoutCache = {{
        canvas, ctx: canvas.getContext('2d'), W, H, dpr,
        rImg, rStrip, rArr2, circles, midPt,
        cellW: rImg.w / IN_GRID_N,
        cellH: rImg.h / IN_GRID_N,
      }};
      return inLayoutCache;
    }}

    window.addEventListener('resize', () => {{ inLayoutCache = null; }});

    function _inClearOverlay() {{
      const canvas = document.getElementById('in-motion-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }}

    function _inSetCallout(key, html) {{
      if (key === inLastCalloutKey) return;
      inLastCalloutKey = key;
      const el = document.getElementById('in-live-callout');
      if (el) el.innerHTML = html;
    }}

    function _inGetCfg() {{
      const hw = parseInt(document.getElementById('in-hw').value, 10) || 224;
      const ch = parseInt(document.getElementById('in-ch').value, 10) || 3;
      return {{ hw, ch, tot: hw * hw * ch, isRgb: ch === 3 }};
    }}

    function _inGetPixel(idx) {{
      if (IN_GRID.length > 0) {{
        const safe = Math.max(0, Math.min(IN_GRID.length - 1, idx));
        return IN_GRID[safe];
      }}
      return {{ idx: 1, r: 0, c: 0, rgb: [204, 204, 199], norm: [0.80, 0.80, 0.78], gray: 0.80 }};
    }}

    function _inPixelCss(px, isRgb) {{
      if (isRgb) return `rgb(${{px.rgb[0]}}, ${{px.rgb[1]}}, ${{px.rgb[2]}})`;
      const g = Math.round(px.gray * 255);
      return `rgb(${{g}}, ${{g}}, ${{g}})`;
    }}

    function _inHexRgba(hex, a) {{
      const n = parseInt(hex.slice(1), 16);
      return `rgba(${{(n >> 16) & 255}}, ${{(n >> 8) & 255}}, ${{n & 255}}, ${{a.toFixed(3)}})`;
    }}

    function _inStepPixelMeta(step) {{
      if (step === 1) return {{ px: _inGetPixel(0), label: 'P1 (1,1)', yFrac: 0.035, destMode: 'top1' }};
      if (step === 2) return {{ px: _inGetPixel(1), label: 'P2 (1,2)', yFrac: 0.075, destMode: 'top2' }};
      if (step === 3) return {{ px: _inGetPixel(2), label: 'P3 (1,3)', yFrac: 0.115, destMode: 'top3' }};
      if (step === 4) {{
        const p = _inGetPixel(IN_DRESS_IDX);
        return {{ px: p, label: 'Gaun Elsa', yFrac: (p.idx - 0.5) / 64, destMode: 'mid' }};
      }}
      if (step === 6) return {{ px: _inGetPixel(63), label: 'Piksel Akhir', yFrac: 0.965, destMode: 'end' }};
      if (step === 99 && inCustomPixel) {{
        const p = inCustomPixel;
        return {{
          px: p,
          label: `(${{p.r + 1}},${{p.c + 1}})`,
          yFrac: Math.max(0.035, Math.min(0.965, (p.idx - 0.5) / 64)),
          destMode: p.idx === 1 ? 'top1' : (p.idx === 64 ? 'end' : 'mid'),
        }};
      }}
      return null;
    }}

    function _inTargetStripFrac() {{
      if (inActiveStep === 99) return 1.0;
      const baseMap = [0, 0.055, 0.095, 0.135, 0.19, 0.955, 1.0];
      let frac = baseMap[Math.max(0, Math.min(IN_TOTAL_STEPS, inCompletedSteps))];
      if (inActiveStep >= 1 && inActiveStep <= 4 && inStepProg >= 0.48) {{
        frac = Math.max(frac, baseMap[inActiveStep]);
      }} else if (inActiveStep === 5) {{
        const s = Math.max(0, Math.min(1, inStepProg));
        const eased = 0.5 - 0.5 * Math.cos(Math.PI * s);
        frac = Math.max(frac, 0.14 + 0.815 * eased);
      }} else if (inActiveStep === 6 && inStepProg >= 0.48) {{
        frac = 1.0;
      }}
      return Math.max(0, Math.min(1, frac));
    }}

    function _inSyncDomToState(instant) {{
      const {{ tot, isRgb, hw }} = _inGetCfg();
      const targetFrac = _inTargetStripFrac();
      if (instant) {{
        inVisualFrac = targetFrac;
      }} else {{
        inVisualFrac += (targetFrac - inVisualFrac) * 0.22;
        if (Math.abs(targetFrac - inVisualFrac) < 0.002) inVisualFrac = targetFrac;
      }}

      // 1. Stage glow classes (dirty-checked — zero DOM writes unless phase changed!)
      const isSingle = (inActiveStep >= 1 && inActiveStep <= 6 && inActiveStep !== 5) || inActiveStep === 99;
      const phaseCode = inActiveStep === 5
        ? 'stream'
        : isSingle
          ? (inStepProg < 0.48 ? 'p1' : 'p2')
          : (inCompletedSteps === 0 ? 'zero' : 'idle');
      const stageKey = `${{phaseCode}}_${{inCompletedSteps === 0 ? 0 : 1}}`;
      if (stageKey !== inLastStageKey) {{
        inLastStageKey = stageKey;
        const s1 = document.getElementById('in-stage-1');
        const s2 = document.getElementById('in-stage-2');
        const s3 = document.getElementById('in-stage-3');
        const a1 = document.getElementById('in-arrow-1');
        const a2 = document.getElementById('in-arrow-2');
        if (phaseCode === 'stream') {{
          if (s1) s1.className = 'in-stage-card glow-blue';
          if (s2) s2.className = 'in-stage-card glow-yellow';
          if (s3) s3.className = 'in-stage-card glow-blue';
          if (a1) a1.className = 'in-arrow-box active';
          if (a2) a2.className = 'in-arrow-box active';
        }} else if (phaseCode === 'p1') {{
          if (s1) s1.className = 'in-stage-card glow-blue';
          if (s2) s2.className = 'in-stage-card glow-yellow';
          if (s3) s3.className = 'in-stage-card ' + (inCompletedSteps === 0 && inActiveStep !== 99 ? 'dim' : '');
          if (a1) a1.className = 'in-arrow-box active';
          if (a2) a2.className = 'in-arrow-box';
        }} else if (phaseCode === 'p2') {{
          if (s1) s1.className = 'in-stage-card';
          if (s2) s2.className = 'in-stage-card glow-yellow';
          if (s3) s3.className = 'in-stage-card glow-blue';
          if (a1) a1.className = 'in-arrow-box';
          if (a2) a2.className = 'in-arrow-box active';
        }} else {{
          if (s1) s1.className = 'in-stage-card';
          if (s2) s2.className = 'in-stage-card ' + (inCompletedSteps === 0 ? 'dim' : '');
          if (s3) s3.className = 'in-stage-card ' + (inCompletedSteps === 0 ? 'dim' : '');
          if (a1) a1.className = 'in-arrow-box';
          if (a2) a2.className = 'in-arrow-box';
        }}
        const inCallCol = phaseCode === 'p1' ? 'blue' : (phaseCode === 'stream' ? 'yellow' : (phaseCode === 'p2' ? 'green' : ''));
        _syncCards(['in-live-callout'], inCallCol ? 0 : -1, [inCallCol || 'blue']);
      }}

      // 2. Smooth 1D strip reveal & curly brace (only write when changed)
      const clipPct = Math.round((1 - inVisualFrac) * 1000) / 10;
      if (clipPct !== inLastClipPct) {{
        inLastClipPct = clipPct;
        const strip = document.getElementById('in-strip-img');
        if (strip) strip.style.clipPath = `inset(0 0 ${{clipPct.toFixed(1)}}% 0)`;
        const brace = document.getElementById('in-brace-path');
        if (brace) brace.style.strokeDashoffset = (280 * (1 - inVisualFrac)).toFixed(1);
      }}

      // 3. Smooth live counter (only write when formatted text changes)
      let dispTot = Math.round(tot * inVisualFrac);
      if (inActiveStep !== 99 && inCompletedSteps === 0 && inActiveStep === 0) {{
        dispTot = 0;
      }} else if (inActiveStep !== 99 && inActiveStep < 5 && inCompletedSteps < 5) {{
        const pxDone = Math.max(inCompletedSteps, inStepProg >= 0.48 ? inActiveStep : inActiveStep - 1);
        dispTot = Math.min(tot, Math.max(0, pxDone) * (isRgb ? 3 : 1));
      }}
      const totText = dispTot.toLocaleString('id-ID');
      if (totText !== inLastTotText) {{
        inLastTotText = totText;
        const totEl = document.getElementById('in-total');
        if (totEl) totEl.textContent = totText;
      }}

      // 4. Reveal neuron rows right as each orb lands (t >= 0.86) for crisp impact timing!
      const landed = inStepProg >= 0.86;
      const rows = document.querySelectorAll('#in-layer-nodes .in-node-row');
      rows.forEach((row, idx) => {{
        let visible = true;
        if (inActiveStep !== 99) {{
          if (isRgb) {{
            if (idx <= 2) visible = inCompletedSteps >= 1 || (inActiveStep === 1 && landed);
            else if (idx === 3) visible = inCompletedSteps >= 2 || (inActiveStep >= 2 && (inActiveStep > 2 || landed));
            else visible = inCompletedSteps >= 6 || (inActiveStep === 6 && landed);
          }} else {{
            if (idx === 0) visible = inCompletedSteps >= 1 || (inActiveStep === 1 && landed);
            else if (idx === 1) visible = inCompletedSteps >= 2 || (inActiveStep === 2 && landed);
            else if (idx === 2) visible = inCompletedSteps >= 3 || (inActiveStep === 3 && landed);
            else if (idx === 3) visible = inCompletedSteps >= 4 || (inActiveStep >= 4 && (inActiveStep > 4 || landed));
            else visible = inCompletedSteps >= 6 || (inActiveStep === 6 && landed);
          }}
        }}
        row.classList.toggle('hidden-step', !visible);
        row.classList.toggle('traced', idx === inTracedRow);
      }});

      // 5. Dirty-checked callout caption (updates ONCE per phase transition, never 60x/sec!)
      if (inActiveStep === 99 && inCustomPixel) {{
        const p = inCustomPixel;
        _inSetCallout(
          `c99_${{p.idx}}_${{isRgb}}`,
          isRgb
            ? `<strong>Piksel Dipilih (Baris ${{p.r + 1}}, Kol ${{p.c + 1}}):</strong> 1 kotak piksel warna asli meluncur ke <strong>Pita Flatten (1D)</strong> → pecah jadi <strong>3 neuron angka</strong>: Red <code>${{p.norm[0].toFixed(2)}}</code>, Green <code>${{p.norm[1].toFixed(2)}}</code>, Blue <code>${{p.norm[2].toFixed(2)}}</code>!`
            : `<strong>Piksel Dipilih (Baris ${{p.r + 1}}, Kol ${{p.c + 1}}):</strong> Pada mode <code>Grayscale</code>, 1 kotak piksel terbang ke Pita 1D → menjadi <strong>1 neuron tunggal</strong> bernilai <code>${{p.gray.toFixed(2)}}</code>!`
        );
      }} else if (inActiveStep >= 1 && inActiveStep <= 3) {{
        const p = _inGetPixel(inActiveStep - 1);
        const sub = inStepProg < 0.48 ? 1 : 2;
        const txt = sub === 1
          ? 'terangkat dari Foto Elsa → meluncur ke Pita 1D'
          : (isRgb ? `pecah jadi 3 bola angka (R=${{p.norm[0].toFixed(2)}}, G=${{p.norm[1].toFixed(2)}}, B=${{p.norm[2].toFixed(2)}}) → masuk Input Layer` : `masuk sebagai 1 bola angka (${{p.gray.toFixed(2)}}) → mendarat di x${{inActiveStep}}`);
        _inSetCallout(`s${{inActiveStep}}_${{sub}}_${{isRgb}}`, `<strong>Piksel #${{inActiveStep}} / 6 (Baris 1, Kol ${{inActiveStep}}):</strong> Kotak piksel #${{inActiveStep}} ${{txt}}!`);
      }} else if (inActiveStep === 4) {{
        const p = _inGetPixel(IN_DRESS_IDX);
        _inSetCallout(
          `s4_${{isRgb}}`,
          isRgb
            ? `<strong>Piksel #4 / 6 (Gaun Biru Elsa · Baris ${{p.r + 1}}, Kol ${{p.c + 1}}):</strong> Kotak piksel biru nyata melayang ke tengah Pita 1D lalu pecah jadi <code>R=${{p.norm[0].toFixed(2)}}</code>, <code>G=${{p.norm[1].toFixed(2)}}</code>, <code>B=${{p.norm[2].toFixed(2)}}</code>!`
            : `<strong>Piksel #4 / 6 (Gaun Elsa · Baris ${{p.r + 1}}, Kol ${{p.c + 1}}):</strong> Kotak piksel gaun Elsa melayang ke tengah Pita 1D lalu menjadi 1 angka <code>${{p.gray.toFixed(2)}}</code>!`
        );
      }} else if (inActiveStep === 5) {{
        _inSetCallout(`s5_${{tot}}`, `<strong>Langkah 5 / 6 (Aliran Per-Piksel):</strong> Seluruh <strong>${{(hw * hw).toLocaleString('id-ID')}} piksel</strong> dipindai halus satu per satu (kiri → kanan, atas → bawah) mengisi Pita 1D hingga <strong>${{tot.toLocaleString('id-ID')}} neuron</strong>!`);
      }} else if (inActiveStep === 6) {{
        const p = _inGetPixel(63);
        _inSetCallout(`s6_${{tot}}_${{isRgb}}`, `<strong>Piksel #6 / 6 (Piksel Terakhir · Pojok Kanan Bawah):</strong> Piksel terakhir terbang ke dasar Pita 1D lalu mendarat di neuron akhir (<code>x${{tot.toLocaleString('id-ID')}}</code> = <code>${{(isRgb ? p.norm[2] : p.gray).toFixed(2)}}</code>)!`);
      }} else if (inTracedRow < 0 && inCompletedSteps === IN_TOTAL_STEPS) {{
        _inSetCallout('default', IN_DEFAULT_CALLOUT);
      }} else if (inCompletedSteps === 0) {{
        _inSetCallout('zero', '<strong>Siap dimulai!</strong> Klik <strong>▶ Play</strong>, <strong>⏭ +1 Piksel</strong>, atau klik langsung kotak piksel mana saja pada <strong>Foto Elsa</strong> di kiri!');
      }}
    }}

    function _inDrawMotionOverlay() {{
      const L = inLayoutCache || _inCacheLayout();
      if (!L) return;
      const {{ ctx, W, H, dpr, rImg, rStrip, rArr2, circles, midPt, cellW, cellH }} = L;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      const {{ isRgb }} = _inGetCfg();
      const clamp01 = (v) => (v < 0 ? 0 : (v > 1 ? 1 : v));
      const easeIO = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
      const easeOut = (t) => 1 - Math.pow(1 - t, 3);
      const qPt = (x0, y0, cx, cy, x1, y1, u) => {{
        const inv = 1 - u;
        return {{
          x: inv * inv * x0 + 2 * inv * u * cx + u * u * x1,
          y: inv * inv * y0 + 2 * inv * u * cy + u * u * y1,
        }};
      }};

      // Helper: draw ultra-fast vector glow pixel square (zero shadowBlur lag!)
      const drawPixelSquare = (cx, cy, sz, fillCol, alpha, tag) => {{
        ctx.save();
        ctx.globalAlpha = alpha;
        // Soft vector outer halo
        _fltRoundRect(ctx, cx - sz / 2 - 4, cy - sz / 2 - 4, sz + 8, sz + 8, 8);
        ctx.fillStyle = 'rgba(251, 188, 4, 0.24)';
        ctx.fill();
        // Crisp pixel square
        _fltRoundRect(ctx, cx - sz / 2, cy - sz / 2, sz, sz, 5);
        ctx.fillStyle = fillCol;
        ctx.fill();
        ctx.strokeStyle = '#FBBC04';
        ctx.lineWidth = 2.4;
        ctx.stroke();
        if (tag && alpha > 0.45) {{
          const tw = Math.max(44, tag.length * 6.2 + 12);
          _fltRoundRect(ctx, cx - tw / 2, cy - sz / 2 - 20, tw, 16, 5);
          ctx.fillStyle = 'rgba(32, 33, 36, 0.92)';
          ctx.fill();
          ctx.fillStyle = '#FFFFFF';
          ctx.font = '700 9px Roboto Mono, monospace';
          ctx.textAlign = 'center';
          ctx.fillText(tag, cx, cy - sz / 2 - 9);
        }}
        ctx.restore();
      }};

      // Helper: draw expanding ripple ring (smooth landing / impact feedback)
      const drawRipple = (cx, cy, r0, r1, t, hexCol) => {{
        if (t <= 0 || t >= 1) return;
        const e = easeOut(t);
        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, r0 + (r1 - r0) * e, 0, Math.PI * 2);
        ctx.strokeStyle = _inHexRgba(hexCol, (1 - e) * 0.78);
        ctx.lineWidth = 2.8 * (1 - e * 0.55);
        ctx.stroke();
        ctx.restore();
      }};

      // CASE A: Silky Single-Pixel 2-Phase Flight (Steps 1, 2, 3, 4, 6, or 99 Custom Click)
      const meta = _inStepPixelMeta(inActiveStep);
      if (meta) {{
        const px = meta.px;
        const pxCol = _inPixelCss(px, isRgb);
        const srcX = rImg.x + (px.c + 0.5) * cellW;
        const srcY = rImg.y + (px.r + 0.5) * cellH;
        const dstX = rStrip.x + rStrip.w / 2;
        const dstY = rStrip.y + meta.yFrac * rStrip.h;
        const ctrl1X = (srcX + dstX) * 0.5;
        const ctrl1Y = Math.min(srcY, dstY) - 44;

        // Smooth anticipation pulse on source pixel square (0.00 -> 0.12)
        const liftT = clamp01(inStepProg / 0.10);
        const srcGlowAlpha = inStepProg < 0.52 ? (0.28 * liftT) : Math.max(0.08, 0.28 * (1 - (inStepProg - 0.52) / 0.48));
        ctx.save();
        ctx.fillStyle = `rgba(251, 188, 4, ${{srcGlowAlpha.toFixed(3)}})`;
        ctx.strokeStyle = `rgba(251, 188, 4, ${{(0.45 + 0.55 * liftT).toFixed(3)}})`;
        ctx.lineWidth = 2.6;
        ctx.fillRect(rImg.x + px.c * cellW, rImg.y + px.r * cellH, cellW, cellH);
        ctx.strokeRect(rImg.x + px.c * cellW, rImg.y + px.r * cellH, cellW, cellH);
        ctx.restore();

        // Phase 1 trajectory guide (fades gracefully once pixel lands)
        const arc1Alpha = inStepProg < 0.52 ? 0.85 : Math.max(0.18, 0.85 * (1 - (inStepProg - 0.52) / 0.35));
        ctx.save();
        ctx.setLineDash([6, 4]);
        ctx.strokeStyle = `rgba(26, 115, 232, ${{arc1Alpha.toFixed(3)}})`;
        ctx.lineWidth = 2.1;
        ctx.beginPath();
        ctx.moveTo(srcX, srcY);
        ctx.quadraticCurveTo(ctrl1X, ctrl1Y, dstX, dstY);
        ctx.stroke();
        ctx.restore();

        // Sub-phase 1 (0.00 -> 0.48): Anticipation + Gliding Square Pixel + Tapered Comet Trail!
        if (inStepProg < 0.54) {{
          const raw1 = clamp01((inStepProg - 0.04) / 0.44);
          const e1 = easeIO(raw1);
          const pt = qPt(srcX, srcY, ctrl1X, ctrl1Y, dstX, dstY, e1);

          // 6 fading comet trail ghosts behind the flying pixel
          for (let g = 6; g >= 1; g--) {{
            const gu = Math.max(0, e1 - g * 0.045);
            if (gu <= 0) continue;
            const gp = qPt(srcX, srcY, ctrl1X, ctrl1Y, dstX, dstY, gu);
            const gSz = 22 - g * 2.1;
            ctx.save();
            ctx.globalAlpha = (0.34 * (1 - g / 7)) * (inStepProg < 0.48 ? 1 : (0.54 - inStepProg) / 0.06);
            _fltRoundRect(ctx, gp.x - gSz / 2, gp.y - gSz / 2, gSz, gSz, 4);
            ctx.fillStyle = pxCol;
            ctx.fill();
            ctx.restore();
          }}

          // Smooth scale curve: pops gently on lift-off, settles smoothly into strip slot
          const popScale = inStepProg < 0.08
            ? 0.86 + 0.24 * easeOut(inStepProg / 0.08)
            : (inStepProg > 0.46 ? Math.max(0.55, 1.0 - ((inStepProg - 0.46) / 0.08) * 0.45) : 1.04);
          const fadeOut = inStepProg > 0.48 ? clamp01((0.54 - inStepProg) / 0.06) : 1.0;
          drawPixelSquare(pt.x, pt.y, 22 * popScale, pxCol, fadeOut, inStepProg < 0.47 ? meta.label : null);
        }}

        // Highlight landed pixel slot & soft amber landing ripple (t = 0.46 -> 0.66)
        if (inStepProg >= 0.45) {{
          const slotAlpha = clamp01((inStepProg - 0.45) / 0.08);
          ctx.save();
          ctx.globalAlpha = slotAlpha;
          ctx.fillStyle = pxCol;
          ctx.strokeStyle = '#E37400';
          ctx.lineWidth = 2.0;
          ctx.fillRect(rStrip.x + 2, dstY - 5, rStrip.w - 4, 10);
          ctx.strokeRect(rStrip.x + 2, dstY - 5, rStrip.w - 4, 10);
          ctx.restore();
          drawRipple(dstX, dstY, 8, 30, (inStepProg - 0.46) / 0.20, '#FBBC04');
        }}

        // Sub-phase 2 (0.48 -> 1.00): Smooth Split from 1D Strip -> RGB/Gray Orb(s) -> Settle Ripple!
        if (inStepProg >= 0.48) {{
          const raw2 = clamp01((inStepProg - 0.48) / 0.40); // arrives cleanly at t = 0.88!
          const e2 = easeIO(raw2);
          const ptOf = (idx) => circles[idx] || midPt;

          let orbs = [];
          if (isRgb) {{
            if (meta.destMode === 'top1') {{
              orbs = [
                {{ dst: ptOf(0), col: '#EA4335', txt: px.norm[0].toFixed(2) }},
                {{ dst: ptOf(1), col: '#34A853', txt: px.norm[1].toFixed(2) }},
                {{ dst: ptOf(2), col: '#4285F4', txt: px.norm[2].toFixed(2) }},
              ];
            }} else if (meta.destMode === 'end') {{
              orbs = [
                {{ dst: ptOf(3), col: '#EA4335', txt: px.norm[0].toFixed(2) }},
                {{ dst: ptOf(4), col: '#34A853', txt: px.norm[1].toFixed(2) }},
                {{ dst: ptOf(5), col: '#4285F4', txt: px.norm[2].toFixed(2) }},
              ];
            }} else {{
              orbs = [
                {{ dst: {{ x: midPt.x, y: midPt.y - 18 }}, col: '#EA4335', txt: px.norm[0].toFixed(2) }},
                {{ dst: {{ x: midPt.x, y: midPt.y }},      col: '#34A853', txt: px.norm[1].toFixed(2) }},
                {{ dst: {{ x: midPt.x, y: midPt.y + 18 }}, col: '#4285F4', txt: px.norm[2].toFixed(2) }},
              ];
            }}
          }} else {{
            const grayDst = meta.destMode === 'top1' ? ptOf(0)
              : meta.destMode === 'top2' ? ptOf(1)
              : meta.destMode === 'top3' ? ptOf(2)
              : meta.destMode === 'end' ? ptOf(4) : midPt;
            orbs = [{{ dst: grayDst, col: meta.destMode === 'end' ? '#5F6368' : '#4285F4', txt: px.gray.toFixed(2) }}];
          }}

          orbs.forEach((ob, k) => {{
            const ctrlX = (dstX + ob.dst.x) * 0.5;
            const ctrlY = (dstY + ob.dst.y) * 0.5 + (k - (orbs.length - 1) / 2) * 32 - 22;

            // Smooth dashed path fading in gently
            const pathAlpha = Math.min(0.85, clamp01(raw2 / 0.18) * 0.85) * (inStepProg > 0.90 ? clamp01((1.0 - inStepProg) / 0.10) : 1);
            ctx.save();
            ctx.setLineDash([5, 4]);
            ctx.strokeStyle = _inHexRgba(ob.col, pathAlpha);
            ctx.lineWidth = 2.0;
            ctx.beginPath();
            ctx.moveTo(dstX, dstY);
            ctx.quadraticCurveTo(ctrlX, ctrlY, ob.dst.x, ob.dst.y);
            ctx.stroke();
            ctx.restore();

            if (inStepProg < 0.92) {{
              // Tapered orb trail
              for (let g = 5; g >= 1; g--) {{
                const gu = Math.max(0, e2 - g * 0.045);
                if (gu <= 0) continue;
                const gp = qPt(dstX, dstY, ctrlX, ctrlY, ob.dst.x, ob.dst.y, gu);
                ctx.save();
                ctx.beginPath();
                ctx.arc(gp.x, gp.y, 13 - g * 1.7, 0, Math.PI * 2);
                ctx.fillStyle = _inHexRgba(ob.col, 0.28 * (1 - g / 6));
                ctx.fill();
                ctx.restore();
              }}

              // Smooth grow-in radius (5px -> 15.5px) so orbs emerge smoothly from the pixel!
              const op = qPt(dstX, dstY, ctrlX, ctrlY, ob.dst.x, ob.dst.y, e2);
              const rad = 5.5 + 10.0 * easeOut(clamp01(raw2 / 0.22));
              const orbAlpha = inStepProg > 0.88 ? clamp01((0.92 - inStepProg) / 0.04) : 1.0;

              ctx.save();
              ctx.globalAlpha = orbAlpha;
              // Soft outer glow halo
              ctx.beginPath();
              ctx.arc(op.x, op.y, rad + 4.5, 0, Math.PI * 2);
              ctx.fillStyle = _inHexRgba(ob.col, 0.22);
              ctx.fill();
              // Solid crisp orb
              ctx.beginPath();
              ctx.arc(op.x, op.y, rad, 0, Math.PI * 2);
              ctx.fillStyle = ob.col;
              ctx.fill();
              ctx.strokeStyle = '#FFFFFF';
              ctx.lineWidth = 2.2;
              ctx.stroke();

              if (rad >= 11) {{
                ctx.fillStyle = '#FFFFFF';
                ctx.font = '700 8.8px Roboto Mono, monospace';
                ctx.textAlign = 'center';
                ctx.fillText(ob.txt, op.x, op.y + 3);
              }}
              ctx.restore();
            }}

            // Smooth landing confirmation ripple on the Input Layer neuron (t = 0.85 -> 1.00)
            if (inStepProg >= 0.85) {{
              drawRipple(ob.dst.x, ob.dst.y, 15, 29, (inStepProg - 0.85) / 0.15, ob.col);
            }}
          }});
        }}
        return;
      }}

      // CASE B: Step 5 — Silky Continuous Per-Pixel River (32 staggered pixels + smooth gliding scanner!)
      if (inActiveStep === 5) {{
        const nP = IN_STREAM_IDXS.length;
        // Smoothly gliding scanner cursor sweeping across Elsa's 8x8 photo
        const scanFloat = clamp01(inStepProg / 0.80) * (nP - 1);
        const s0 = Math.floor(scanFloat), s1 = Math.min(nP - 1, s0 + 1);
        const sf = scanFloat - s0;
        const pxA = _inGetPixel(IN_STREAM_IDXS[s0]);
        const pxB = _inGetPixel(IN_STREAM_IDXS[s1]);
        const curColF = pxA.r === pxB.r ? (pxA.c + (pxB.c - pxA.c) * sf) : pxB.c;
        const curRowF = pxA.r === pxB.r ? pxA.r : pxB.r;
        ctx.save();
        ctx.fillStyle = 'rgba(251, 188, 4, 0.26)';
        ctx.strokeStyle = '#FBBC04';
        ctx.lineWidth = 2.5;
        ctx.fillRect(rImg.x + curColF * cellW, rImg.y + curRowF * cellH, cellW, cellH);
        ctx.strokeRect(rImg.x + curColF * cellW, rImg.y + curRowF * cellH, cellW, cellH);
        ctx.restore();

        // Smooth river of individual square pixels flying from Foto -> 1D Strip
        IN_STREAM_IDXS.forEach((pIdx, k) => {{
          const startT = (k / nP) * 0.72;
          const dur = 0.28;
          const local = (inStepProg - startT) / dur;
          if (local <= 0 || local >= 1) return;

          const px = _inGetPixel(pIdx);
          const pxCol = _inPixelCss(px, isRgb);
          const srcX = rImg.x + (px.c + 0.5) * cellW;
          const srcY = rImg.y + (px.r + 0.5) * cellH;
          const dstX = rStrip.x + rStrip.w / 2;
          const dstY = rStrip.y + ((pIdx + 0.5) / 64) * rStrip.h;

          if (local < 0.62) {{
            const u = easeIO(local / 0.62);
            const ctrlX = (srcX + dstX) * 0.5;
            const ctrlY = Math.min(srcY, dstY) - 34;
            const pt = qPt(srcX, srcY, ctrlX, ctrlY, dstX, dstY, u);
            const alpha = local < 0.08 ? local / 0.08 : (local > 0.54 ? (0.62 - local) / 0.08 : 1.0);

            // Subtle trailing ghost
            const gp = qPt(srcX, srcY, ctrlX, ctrlY, dstX, dstY, Math.max(0, u - 0.08));
            ctx.save();
            ctx.globalAlpha = alpha * 0.30;
            _fltRoundRect(ctx, gp.x - 6.5, gp.y - 6.5, 13, 13, 3);
            ctx.fillStyle = pxCol;
            ctx.fill();

            ctx.globalAlpha = alpha;
            _fltRoundRect(ctx, pt.x - 8, pt.y - 8, 16, 16, 4);
            ctx.fillStyle = pxCol;
            ctx.fill();
            ctx.strokeStyle = '#FBBC04';
            ctx.lineWidth = 1.6;
            ctx.stroke();
            ctx.restore();
          }} else {{
            // Clean RGB/Gray droplets flowing right across Arrow 2 -> Input Layer (no overlap over TOTAL NEURON!)
            const u = easeIO((local - 0.62) / 0.38);
            const cols = isRgb ? ['#EA4335', '#34A853', '#4285F4'] : ['#4285F4'];
            const startX = rArr2.x - 6;
            const startY = rArr2.y + rArr2.h * 0.5;
            cols.forEach((cHex, ci) => {{
              const tx = midPt.x;
              const ty = midPt.y + (ci - (cols.length - 1) / 2) * 14;
              const cx = (startX + tx) * 0.5;
              const cy = (startY + ty) * 0.5 - 10;
              const op = qPt(startX, startY, cx, cy, tx, ty, u);
              const a = u < 0.15 ? u / 0.15 : (u > 0.85 ? (1 - u) / 0.15 : 1.0);
              ctx.save();
              ctx.globalAlpha = a;
              ctx.beginPath();
              ctx.arc(op.x, op.y, 4.8, 0, Math.PI * 2);
              ctx.fillStyle = cHex;
              ctx.fill();
              ctx.strokeStyle = '#FFFFFF';
              ctx.lineWidth = 1.2;
              ctx.stroke();
              ctx.restore();
            }});
          }}
        }});
        return;
      }}

      // CASE C: Interactive Reverse Trace when user clicks any neuron circle in Input Layer!
      if (inTracedRow >= 0 && inTracedRow !== 3) {{
        const cMap = {{ 0: 0, 1: 1, 2: 2, 4: 3, 5: 4, 6: 5 }};
        const cIdx = cMap[inTracedRow];
        const dstC = circles[cIdx];
        if (!dstC) return;
        const pxMap = isRgb ? [0, 0, 0, 0, 63, 63, 63] : [0, 1, 2, 0, 62, 63];
        const px = _inGetPixel(pxMap[inTracedRow]);
        const col = isRgb
          ? ((inTracedRow === 0 || inTracedRow === 4) ? '#EA4335' : (inTracedRow === 1 || inTracedRow === 5) ? '#34A853' : '#4285F4')
          : '#1A73E8';

        const p1x = rImg.x + (px.c + 0.5) * cellW;
        const p1y = rImg.y + (px.r + 0.5) * cellH;
        const p2x = rStrip.x + rStrip.w / 2;
        const p2y = rStrip.y + Math.max(0.05, Math.min(0.95, (px.idx - 0.5) / 64)) * rStrip.h;

        ctx.save();
        ctx.fillStyle = 'rgba(251, 188, 4, 0.30)';
        ctx.strokeStyle = col;
        ctx.lineWidth = 2.8;
        ctx.fillRect(rImg.x + px.c * cellW, rImg.y + px.r * cellH, cellW, cellH);
        ctx.strokeRect(rImg.x + px.c * cellW, rImg.y + px.r * cellH, cellW, cellH);

        ctx.beginPath(); ctx.arc(p2x, p2y, 6, 0, Math.PI * 2);
        ctx.fillStyle = col; ctx.fill(); ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 2; ctx.stroke();

        ctx.strokeStyle = col;
        ctx.lineWidth = 2.6;
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.moveTo(p1x, p1y);
        ctx.quadraticCurveTo((p1x + p2x) / 2, Math.min(p1y, p2y) - 26, p2x, p2y);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(p2x, p2y);
        ctx.quadraticCurveTo((p2x + dstC.x) / 2, Math.min(p2y, dstC.y) - 20, dstC.x - 16, dstC.y);
        ctx.stroke();
        ctx.restore();
      }}
    }}

    function _tickInMotion(ts) {{
      if (!inLastTs) inLastTs = ts;
      const dt = Math.min(0.033, Math.max(0.001, (ts - inLastTs) / 1000));
      inLastTs = ts;
      // Smooth, unhurried pace: ~1.55s per single pixel (2 phases + settle), ~2.3s for Step 5 stream
      const speed = inActiveStep === 5 ? 0.44 : (inActiveStep === 99 ? 0.62 : (inAutoMode ? 0.66 : 0.62));
      inStepProg += dt * speed;
      if (inStepProg >= 1.0) {{
        if (inActiveStep === 99) {{
          inActiveStep = 0;
          inStepProg = 0;
          inAnimRaf = null;
          _inSyncDomToState(true);
          _inClearOverlay();
          return;
        }}
        inCompletedSteps = Math.max(inCompletedSteps, inActiveStep);
        inStepProg = 0;
        if (inAutoMode && inActiveStep < IN_TOTAL_STEPS) {{
          inActiveStep += 1;
        }} else {{
          inActiveStep = 0;
          inAutoMode = false;
          inAnimRaf = null;
          _inSetPlayBtn(false);
          _inSyncDomToState(true);
          _inClearOverlay();
          return;
        }}
      }}
      _inSyncDomToState(false);
      _inDrawMotionOverlay();
      inAnimRaf = requestAnimationFrame(_tickInMotion);
    }}

    function _resetInVisualFull() {{
      _stopInAnim();
      inLayoutCache = null;
      inLastStageKey = '';
      inLastCalloutKey = '';
      inLastTotText = '';
      inLastClipPct = -1;
      inCompletedSteps = IN_TOTAL_STEPS;
      inActiveStep = 0;
      inStepProg = 0;
      inTracedRow = -1;
      inCustomPixel = null;
      _inSyncDomToState(true);
      _inClearOverlay();
    }}

    function resetInProcessZero() {{
      _stopInAnim();
      inLayoutCache = null;
      inLastStageKey = '';
      inLastCalloutKey = '';
      inLastTotText = '';
      inLastClipPct = -1;
      inCompletedSteps = 0;
      inActiveStep = 0;
      inStepProg = 0;
      inTracedRow = -1;
      inCustomPixel = null;
      _inSyncDomToState(true);
      _inClearOverlay();
    }}

    function playInProcess() {{
      if (inAutoMode && inAnimRaf !== null) {{
        _stopInAnim();
        inActiveStep = 0;
        _inSyncDomToState(true);
        _inClearOverlay();
        return;
      }}
      _stopInAnim();
      inLayoutCache = _inCacheLayout();
      inLastStageKey = '';
      inLastCalloutKey = '';
      inTracedRow = -1;
      inCustomPixel = null;
      inCompletedSteps = 0;
      inActiveStep = 1;
      inStepProg = 0;
      inVisualFrac = 0;
      inAutoMode = true;
      inLastTs = 0;
      _inSetPlayBtn(true);
      _inSyncDomToState(true);
      _inDrawMotionOverlay();
      inAnimRaf = requestAnimationFrame(_tickInMotion);
    }}

    function stepInProcess() {{
      if (inAutoMode) _stopInAnim();
      inLayoutCache = _inCacheLayout();
      inLastStageKey = '';
      inLastCalloutKey = '';
      inTracedRow = -1;
      inCustomPixel = null;
      if (inActiveStep > 0 && inActiveStep <= IN_TOTAL_STEPS) {{
        inCompletedSteps = Math.max(inCompletedSteps, inActiveStep);
        inActiveStep = 0;
      }}
      if (inCompletedSteps >= IN_TOTAL_STEPS) {{
        inCompletedSteps = 0;
        inVisualFrac = 0;
      }}
      inActiveStep = inCompletedSteps + 1;
      inStepProg = 0;
      inAutoMode = false;
      inLastTs = 0;
      if (inAnimRaf !== null) cancelAnimationFrame(inAnimRaf);
      _inSyncDomToState(false);
      _inDrawMotionOverlay();
      inAnimRaf = requestAnimationFrame(_tickInMotion);
    }}

    function triggerPixelClick(ev) {{
      _stopInAnim();
      inLayoutCache = _inCacheLayout();
      inLastStageKey = '';
      inLastCalloutKey = '';
      inTracedRow = -1;
      const imgFrame = document.getElementById('in-img-frame');
      let idx = IN_DRESS_IDX;
      if (imgFrame && ev && typeof ev.clientX === 'number') {{
        const rect = imgFrame.getBoundingClientRect();
        const rx = Math.max(0, Math.min(0.999, (ev.clientX - rect.left) / (rect.width || 1)));
        const ry = Math.max(0, Math.min(0.999, (ev.clientY - rect.top) / (rect.height || 1)));
        const col = Math.floor(rx * IN_GRID_N);
        const row = Math.floor(ry * IN_GRID_N);
        idx = row * IN_GRID_N + col;
      }}
      inCompletedSteps = IN_TOTAL_STEPS;
      inCustomPixel = _inGetPixel(idx);
      inActiveStep = 99;
      inStepProg = 0;
      inAutoMode = false;
      inLastTs = 0;
      _inSyncDomToState(true);
      _inDrawMotionOverlay();
      inAnimRaf = requestAnimationFrame(_tickInMotion);
    }}

    function triggerPixelSplitClick() {{
      _stopInAnim();
      inLayoutCache = _inCacheLayout();
      inLastStageKey = '';
      inLastCalloutKey = '';
      inTracedRow = -1;
      inCompletedSteps = IN_TOTAL_STEPS;
      inCustomPixel = _inGetPixel(IN_DRESS_IDX);
      inActiveStep = 99;
      inStepProg = 0.48;
      inAutoMode = false;
      inLastTs = 0;
      _inSyncDomToState(true);
      _inDrawMotionOverlay();
      inAnimRaf = requestAnimationFrame(_tickInMotion);
    }}

    function traceInputNeuron(rowIdx) {{
      if (rowIdx === 3) return;
      _stopInAnim();
      inLayoutCache = _inCacheLayout();
      inLastStageKey = '';
      inLastCalloutKey = '';
      inCustomPixel = null;
      inCompletedSteps = IN_TOTAL_STEPS;
      inActiveStep = 0;
      inTracedRow = inTracedRow === rowIdx ? -1 : rowIdx;
      _inSyncDomToState(true);
      _inDrawMotionOverlay();
      if (inTracedRow >= 0) {{
        const {{ isRgb, tot }} = _inGetCfg();
        const names = isRgb
          ? ['x₁ (Piksel 1 · Red)', 'x₂ (Piksel 1 · Green)', 'x₃ (Piksel 1 · Blue)', '', `x${{(tot-2).toLocaleString('id-ID')}} (Piksel akhir · Red)`, `x${{(tot-1).toLocaleString('id-ID')}} (Piksel akhir · Green)`, `x${{tot.toLocaleString('id-ID')}} (Piksel akhir · Blue)`]
          : ['x₁ (Piksel 1 · Gray)', 'x₂ (Piksel 2 · Gray)', 'x₃ (Piksel 3 · Gray)', '', `x${{(tot-1).toLocaleString('id-ID')}} (Piksel akhir-1)`, `x${{tot.toLocaleString('id-ID')}} (Piksel akhir)`];
        _inSetCallout(
          `trace_${{inTracedRow}}_${{isRgb}}`,
          `<strong>Jejak Asal Neuron:</strong> <code>${{names[inTracedRow]}}</code> berasal langsung dari kotak piksel yang disorot pada <strong>Foto Elsa</strong> → masuk ke <strong>Pita 1D</strong> → menjadi angka di <strong>Input Layer</strong>! (Klik lagi untuk menutup jejak.)`
        );
      }}
    }}

    function setInSize(h, w, c, btn) {{
      _stopInAnim();
      document.getElementById('in-hw').value = String(h);
      document.getElementById('in-ch').value = String(c);
      document.querySelectorAll('#in-presets button[data-in]').forEach((b) => b.classList.add('outline'));
      if (btn) btn.classList.remove('outline');
      updateInCalc();
    }}
    function setInPdfPreset(key) {{
      const [hw, ch] = key.split('_').map((v) => parseInt(v, 10));
      const btn = document.querySelector(`#in-presets button[data-in="${{key}}"]`);
      setInSize(hw, hw, ch, btn);
    }}
    function updateInCalc() {{
      _stopInAnim();
      const hw = parseInt(document.getElementById('in-hw').value, 10) || 224;
      const ch = parseInt(document.getElementById('in-ch').value, 10) || 3;
      const tot = hw * hw * ch;
      const totStr = tot.toLocaleString('id-ID');
      const isRgb = ch === 3;

      document.getElementById('in-hw-v').textContent = `${{hw}}×${{hw}}`;
      document.getElementById('in-ch-v').textContent = isRgb ? '3 (RGB)' : '1 (Gray)';

      // Stage 1: Dimensions H, W, Channel depth layers, grayscale filter
      const wDim = document.getElementById('in-w-dim');
      const hDim = document.getElementById('in-h-dim');
      const chTag = document.getElementById('in-ch-tag');
      const shapePill = document.getElementById('in-shape-pill');
      const layerG = document.getElementById('in-ch-layer-g');
      const layerB = document.getElementById('in-ch-layer-b');
      const imgFrame = document.getElementById('in-img-frame');
      const elsaImg = document.getElementById('in-elsa-img');
      const stripImg = document.getElementById('in-strip-img');

      if (wDim) wDim.textContent = `Lebar (W) = ${{hw}}`;
      if (hDim) hDim.textContent = `Tinggi (H) = ${{hw}}`;
      if (chTag) chTag.textContent = isRgb ? 'C = 3 (R·G·B)' : 'C = 1 (Gray)';
      if (shapePill) shapePill.textContent = `Shape: (${{hw}}, ${{hw}}, ${{ch}}) · ${{isRgb ? 'RGB' : 'Grayscale'}}`;
      if (layerG) layerG.style.display = isRgb ? 'block' : 'none';
      if (layerB) layerB.style.display = isRgb ? 'block' : 'none';
      if (imgFrame) imgFrame.style.borderColor = isRgb ? '#EA4335' : '#5F6368';
      if (elsaImg) elsaImg.style.filter = isRgb ? 'none' : 'grayscale(100%)';
      if (stripImg) stripImg.style.filter = isRgb ? 'none' : 'grayscale(100%)';

      // Stage 2: Curly brace multiplication & big total
      const brEq = document.getElementById('in-brace-eq');
      const brSub = document.getElementById('in-brace-sub');
      if (brEq) brEq.textContent = `${{hw}} × ${{hw}} × ${{ch}}`;
      if (brSub) {{
        brSub.innerHTML = isRgb
          ? 'neuron piksel bertumpuk<br/>(<strong>3× lipat</strong> dari Grayscale)'
          : 'neuron piksel bertumpuk<br/>(1 channel hitam-putih)';
      }}
      document.getElementById('in-total').textContent = totStr;
      document.getElementById('in-formula').textContent = `${{hw}} (H) × ${{hw}} (W) × ${{ch}} (${{isRgb ? 'RGB' : 'Gray'}}) = ${{totStr}}`;

      // Stage 3: Input Layer numbered neuron circles with REAL Elsa pixel values
      const lSub = document.getElementById('in-layer-sub');
      if (lSub) lSub.textContent = `1 Kolom Vertikal · ${{totStr}} Neuron`;

      const nodesHost = document.getElementById('in-layer-nodes');
      if (nodesHost) {{
        const middleCount = Math.max(0, tot - (isRgb ? 6 : 5)).toLocaleString('id-ID');
        const nPrev2 = (tot - 2).toLocaleString('id-ID');
        const nPrev = (tot - 1).toLocaleString('id-ID');
        const nLast = totStr;
        const rows = isRgb
          ? [
              {{ col: '#EA4335', val: ELSA_ENDS.first_rgb[0].toFixed(2), idx: 'x₁', desc: 'Piksel 1 (Red)' }},
              {{ col: '#34A853', val: ELSA_ENDS.first_rgb[1].toFixed(2), idx: 'x₂', desc: 'Piksel 1 (Green)' }},
              {{ col: '#4285F4', val: ELSA_ENDS.first_rgb[2].toFixed(2), idx: 'x₃', desc: 'Piksel 1 (Blue)' }},
              {{ ellipsis: true, text: `${{middleCount}} neuron lainnya...` }},
              {{ col: '#EA4335', val: ELSA_ENDS.last_rgb[0].toFixed(2), idx: `x${{nPrev2}}`, desc: 'Piksel akhir (Red)' }},
              {{ col: '#34A853', val: ELSA_ENDS.last_rgb[1].toFixed(2), idx: `x${{nPrev}}`, desc: 'Piksel akhir (Green)' }},
              {{ col: '#4285F4', val: ELSA_ENDS.last_rgb[2].toFixed(2), idx: `x${{nLast}}`, desc: 'Piksel akhir (Blue)' }},
            ]
          : [
              {{ col: '#4285F4', val: ELSA_ENDS.first_gray[0].toFixed(2), idx: 'x₁', desc: 'Piksel 1 (Gray)' }},
              {{ col: '#4285F4', val: ELSA_ENDS.first_gray[1].toFixed(2), idx: 'x₂', desc: 'Piksel 2 (Gray)' }},
              {{ col: '#4285F4', val: ELSA_ENDS.first_gray[2].toFixed(2), idx: 'x₃', desc: 'Piksel 3 (Gray)' }},
              {{ ellipsis: true, text: `${{middleCount}} neuron lainnya...` }},
              {{ col: '#5F6368', val: ELSA_ENDS.last_gray[0].toFixed(2), idx: `x${{nPrev}}`, desc: 'Piksel akhir-1' }},
              {{ col: '#5F6368', val: ELSA_ENDS.last_gray[1].toFixed(2), idx: `x${{nLast}}`, desc: 'Piksel akhir' }},
            ];
        const cSz = isRgb ? 27 : 31;
        nodesHost.innerHTML = rows.map((r, rIdx) => {{
          if (r.ellipsis) {{
            return `<div class="in-node-row" style="display:flex; align-items:center; gap:9px; padding:1px 4px; cursor:default;">
              <div style="width:${{cSz}}px; display:flex; flex-direction:column; align-items:center; gap:2.5px;">
                <span style="width:3.5px; height:3.5px; border-radius:50%; background:#1A73E8;"></span>
                <span style="width:3.5px; height:3.5px; border-radius:50%; background:#1A73E8;"></span>
                <span style="width:3.5px; height:3.5px; border-radius:50%; background:#1A73E8;"></span>
              </div>
              <span style="font-family:var(--font-title); font-size:10.2px; font-weight:700; color:#1A73E8;">${{r.text}}</span>
            </div>`;
          }}
          return `<div class="in-node-row" onclick="traceInputNeuron(${{rIdx}})" title="Klik untuk melihat jejak asal piksel ini!" style="display:flex; align-items:center; gap:8px; padding:1px 4px;">
            <div class="in-node-circle" style="width:${{cSz}}px; height:${{cSz}}px; border-radius:50%; background:${{r.col}}; color:#FFFFFF; font-family:var(--font-code); font-size:${{isRgb ? '8.8' : '9.4'}}px; font-weight:700; display:flex; align-items:center; justify-content:center; flex-shrink:0; box-shadow:0 2px 5px rgba(0,0,0,0.12);">${{r.val}}</div>
            <div style="display:flex; flex-direction:column; line-height:1.15; min-width:0;">
              <span style="font-family:var(--font-code); font-size:10.5px; font-weight:700; color:#202124;">${{r.idx}}</span>
              <span style="font-size:9.2px; color:#5F6368;">${{r.desc}}</span>
            </div>
          </div>`;
        }}).join('');
      }}
      _resetInVisualFull();
    }}
    updateInCalc();

    // =========================================================================
    // SIMULATOR #3B (Slide 23): Silky 60fps Pixel -> Neuron -> Wire -> Output Motion
    // 7 Ultra-Detailed Steps + Direct Click on Photo Pixel / Input Neuron / Output Class:
    //   Step 1: Piksel 1 (1,1) -> Flatten -> pecah 3 neuron x1(R), x2(G), x3(B)
    //   Step 2: Piksel 2 (1,2) -> Flatten -> pecah 3 neuron x4(R), x5(G), x6(B)
    //   Step 3: Aliran piksel nyata + Piksel Akhir (8,8) -> +150.519 & x150.526..x150.528
    //   Step 4: Koneksi Neuron-by-Neuron: x1 mengirim sinyal satu per satu ke y1..y5 (5 kabel!)
    //   Step 5: Koneksi Neuron-by-Neuron: x2 -> x3 -> x4 -> x5 -> x6 menembakkan sinyal ke Output Layer
    //   Step 6: Gelombang penuh +150.519 & x150.526..x150.528 -> skor Softmax penuh (Elsa 89%)
    //   Step 7: Pilih tertinggi -> y2 (Elsa 89%) meluncur ke 4. Hasil Klasifikasi!
    //   Custom 101: Klik kotak piksel mana saja di Foto Original -> Input -> Output Elsa!
    //   Custom 102: Klik 1 neuron Input (x1..x150.528) -> nyalakan 5 kabel keluar ke y1..y5!
    //   Custom 103: Klik 1 neuron Output (y1..y5) -> nyalakan semua kabel masuk dari Input!
    // =========================================================================
    const IO_TOTAL_STEPS = 7;
    const IO_IN_LABELS = ['x₁ (R)', 'x₂ (G)', 'x₃ (B)', 'x₄ (R)', 'x₅ (G)', 'x₆ (B)', 'x150.526 (R)', 'x150.527 (G)', 'x150.528 (B)'];
    const IO_IN_SHORT  = ['1', '2', '3', '4', '5', '6', 'n-2', 'n-1', 'n'];
    const IO_IN_COLS   = ['#EA4335', '#34A853', '#4285F4', '#EA4335', '#34A853', '#4285F4', '#EA4335', '#34A853', '#4285F4'];
    const IO_OUT_NAMES = ['Anna', 'Elsa', 'Kristoff', 'Olaf', 'Sven'];
    const IO_OUT_COLS  = ['#4285F4', '#34A853', '#FBBC04', '#EA4335', '#5F6368'];
    const IO_FINAL_PCT = [4, 89, 2, 3, 2];
    const IO_STREAM_PX = [2, 5, 9, 13, 18, 21, 25, 28, 31, 35, 38, 42, 45, 49, 53, 57, 60];
    const IO_DEFAULT_STATUS = '<strong style="color:#1A73E8;">Interaktif:</strong> Klik <strong>▶ Play</strong>, <strong>⏭ +1 Langkah</strong>, atau klik langsung <strong>piksel foto / neuron Input / neuron Output</strong>!';

    let ioAnimRaf = null;
    let ioCompletedSteps = IO_TOTAL_STEPS; // 0..7
    let ioActiveStep = 0;                  // 1..7, 101 (pixel click), 102 (input click), 103 (output click), or 0 (idle)
    let ioStepProg = 0;                    // 0..1
    let ioAutoMode = false;
    let ioLastTs = 0;
    let ioLayoutCache = null;
    let ioCustomPixel = null;
    let ioInspectInIdx = -1;
    let ioInspectOutIdx = -1;
    let ioVisualPct = [4, 89, 2, 3, 2];
    let ioLastStatusKey = '';
    let ioLastDomKey = '';
    let ioLastPctSig = '';

    function _ioSetPlayBtn(isPlaying) {{
      const btn = document.getElementById('io-btn-play');
      if (!btn) return;
      btn.textContent = isPlaying ? '■ Stop' : '▶ Play';
      btn.style.background = isPlaying ? '#EA4335' : '#34A853';
      btn.style.borderColor = isPlaying ? '#EA4335' : '#34A853';
    }}

    function _stopIoAnim() {{
      if (ioAnimRaf !== null) {{
        cancelAnimationFrame(ioAnimRaf);
        ioAnimRaf = null;
      }}
      ioAutoMode = false;
      _ioSetPlayBtn(false);
    }}

    function _ioCacheLayout() {{
      const wrap = document.getElementById('io-hero-wrap');
      const canvas = document.getElementById('io-motion-canvas');
      const imgFrame = document.getElementById('io-img-frame');
      const inCap = document.getElementById('io-in-cap');
      const outCap = document.getElementById('io-out-cap');
      const resCard = document.getElementById('io-result-card');
      if (!wrap || !canvas || !imgFrame || !inCap || !outCap || !resCard) return null;

      const W = wrap.clientWidth, H = wrap.clientHeight;
      if (W < 10 || H < 10) return null;
      const dpr = Math.min(3, (window.devicePixelRatio || 1) * Math.max(1, window.__STAGE_SCALE__ || 1));
      const cwPx = Math.round(W * dpr), chPx = Math.round(H * dpr);
      if (canvas.width !== cwPx || canvas.height !== chPx) {{
        canvas.width = cwPx;
        canvas.height = chPx;
      }}

      const hRect = wrap.getBoundingClientRect();
      const sx = W / (hRect.width || 1);
      const sy = H / (hRect.height || 1);
      const rel = (el) => {{
        const r = el.getBoundingClientRect();
        return {{
          x: (r.left - hRect.left) * sx,
          y: (r.top - hRect.top) * sy,
          w: r.width * sx,
          h: r.height * sy,
        }};
      }};

      const rImg = rel(imgFrame);
      const rInCap = rel(inCap);
      const rOutCap = rel(outCap);
      const rRes = rel(resCard);
      const inExitX = rInCap.x + rInCap.w;

      const inNodes = [];
      for (let i = 0; i < 9; i++) {{
        const cEl = document.getElementById(`io-in-c-${{i}}`);
        if (cEl) {{
          const rc = rel(cEl);
          inNodes.push({{ cx: rc.x + rc.w / 2, cy: rc.y + rc.h / 2, wireX: inExitX }});
        }}
      }}
      const ellBox = document.getElementById('io-in-ell-box');
      const rEll = ellBox ? rel(ellBox) : {{ x: rInCap.x + 40, y: rInCap.y + rInCap.h * 0.68, w: 120, h: 20 }};
      const ellPt = {{ cx: rEll.x + rEll.w / 2, cy: rEll.y + rEll.h / 2, wireX: inExitX }};

      const outNodes = [];
      for (let j = 0; j < 5; j++) {{
        const cEl = document.getElementById(`io-out-c-${{j}}`);
        const bgEl = document.getElementById(`io-out-bg-${{j}}`);
        if (cEl && bgEl) {{
          const rc = rel(cEl);
          const rb = rel(bgEl);
          outNodes.push({{ cx: rc.x + rc.w / 2, cy: rc.y + rc.h / 2, wireX: rb.x, rightX: rb.x + rb.w }});
        }}
      }}

      ioLayoutCache = {{
        canvas, ctx: canvas.getContext('2d'), W, H, dpr,
        rImg, rInCap, rOutCap, rRes, inNodes, ellPt, outNodes,
        cellW: rImg.w / IN_GRID_N,
        cellH: rImg.h / IN_GRID_N,
      }};
      return ioLayoutCache;
    }}

    window.addEventListener('resize', () => {{ ioLayoutCache = null; }});

    function _ioClearOverlay() {{
      const canvas = document.getElementById('io-motion-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }}

    function _ioSetStatus(key, html) {{
      if (key === ioLastStatusKey) return;
      ioLastStatusKey = key;
      const el = document.getElementById('io-live-status');
      if (el) el.innerHTML = html;
    }}

    function _ioTargetPcts() {{
      if (ioActiveStep >= 100) return IO_FINAL_PCT.slice();
      if (ioCompletedSteps >= 6) return IO_FINAL_PCT.slice();
      if (ioActiveStep === 6) {{
        const t = Math.max(0, Math.min(1, ioStepProg));
        const s = 0.5 - 0.5 * Math.cos(Math.PI * t);
        return [
          12 + (4 - 12) * s,
          56 + (89 - 56) * s,
          10 + (2 - 10) * s,
          12 + (3 - 12) * s,
          10 + (2 - 10) * s,
        ];
      }}
      if (ioCompletedSteps === 5) return [12, 56, 10, 12, 10];
      if (ioActiveStep === 5) {{
        const t = Math.max(0, Math.min(1, ioStepProg));
        return [
          18 + (12 - 18) * t,
          26 + (56 - 26) * t,
          19 + (10 - 19) * t,
          19 + (12 - 19) * t,
          18 + (10 - 18) * t,
        ];
      }}
      if (ioCompletedSteps === 4) return [18, 26, 19, 19, 18];
      if (ioActiveStep === 4) {{
        const t = Math.max(0, Math.min(1, ioStepProg));
        return [18 * t, 26 * t, 19 * t, 19 * t, 18 * t];
      }}
      return [0, 0, 0, 0, 0];
    }}

    function _ioSyncDom(instant) {{
      // 1. Interpolate output probability bars smoothly (dirty-checked!)
      const tgt = _ioTargetPcts();
      for (let j = 0; j < 5; j++) {{
        if (instant) ioVisualPct[j] = tgt[j];
        else {{
          ioVisualPct[j] += (tgt[j] - ioVisualPct[j]) * 0.18;
          if (Math.abs(tgt[j] - ioVisualPct[j]) < 0.25) ioVisualPct[j] = tgt[j];
        }}
      }}
      const pctSig = ioVisualPct.map((v) => Math.round(v)).join('_');
      if (pctSig !== ioLastPctSig) {{
        ioLastPctSig = pctSig;
        for (let j = 0; j < 5; j++) {{
          const p = Math.round(ioVisualPct[j]);
          const bar = document.getElementById(`io-bar-${{j}}`);
          const txt = document.getElementById(`io-pct-${{j}}`);
          if (bar) bar.setAttribute('width', String(p <= 0 ? 0 : Math.max(3, Math.round((p / 100) * 72))));
          if (txt) txt.textContent = `${{p}}%`;
        }}
      }}

      // 2. Dirty-check node visibility, wire dimming, winner highlight, & bottom cards
      const isCustom = ioActiveStep >= 100;
      const inVis = [
        isCustom || ioCompletedSteps >= 1 || (ioActiveStep === 1 && ioStepProg >= 0.56),
        isCustom || ioCompletedSteps >= 1 || (ioActiveStep === 1 && ioStepProg >= 0.72),
        isCustom || ioCompletedSteps >= 1 || (ioActiveStep === 1 && ioStepProg >= 0.86),
        isCustom || ioCompletedSteps >= 2 || (ioActiveStep === 2 && ioStepProg >= 0.56),
        isCustom || ioCompletedSteps >= 2 || (ioActiveStep === 2 && ioStepProg >= 0.72),
        isCustom || ioCompletedSteps >= 2 || (ioActiveStep === 2 && ioStepProg >= 0.86),
        isCustom || ioCompletedSteps >= 3 || (ioActiveStep === 3 && ioStepProg >= 0.78),
        isCustom || ioCompletedSteps >= 3 || (ioActiveStep === 3 && ioStepProg >= 0.86),
        isCustom || ioCompletedSteps >= 3 || (ioActiveStep === 3 && ioStepProg >= 0.92),
      ];
      const ellVis = isCustom || ioCompletedSteps >= 3 || (ioActiveStep === 3 && ioStepProg >= 0.30);
      const wiresLive = (ioActiveStep >= 4 && ioActiveStep <= 6) || ioActiveStep === 101 || ioActiveStep === 102 || ioActiveStep === 103;
      const wiresDone = ioActiveStep === 0 && ioCompletedSteps >= 6;
      const winVis = isCustom || ioCompletedSteps >= 7 || (ioActiveStep === 7 && ioStepProg >= 0.78);
      const elsaHi = isCustom || ioCompletedSteps >= 6 || (ioActiveStep === 6 && ioStepProg >= 0.72) || ioActiveStep === 7;
      const activeStage = ioActiveStep >= 1 && ioActiveStep <= 3 ? (ioStepProg < 0.44 ? 1 : 2)
        : (ioActiveStep >= 4 && ioActiveStep <= 6 ? 3 : (ioActiveStep === 7 ? 4 : (ioActiveStep === 101 ? 1 : (ioActiveStep === 102 ? 2 : (ioActiveStep === 103 ? 3 : 0)))));

      const domKey = `${{inVis.map((b) => (b ? 1 : 0)).join('')}}_${{ellVis ? 1 : 0}}_${{wiresLive ? 1 : (wiresDone ? 2 : 0)}}_${{winVis ? 1 : 0}}_${{elsaHi ? 1 : 0}}_${{activeStage}}`;
      if (domKey !== ioLastDomKey) {{
        ioLastDomKey = domKey;
        for (let i = 0; i < 9; i++) {{
          const g = document.getElementById(`io-in-${{i}}`);
          if (g) g.classList.toggle('io-node-dim', !inVis[i]);
        }}
        const ell = document.getElementById('io-in-ell');
        if (ell) ell.style.opacity = ellVis ? '1' : '0.14';

        const wb = document.getElementById('io-wires-bg');
        const wh = document.getElementById('io-wires-hi');
        if (wb) wb.style.opacity = wiresLive ? '0.12' : (wiresDone ? '0.88' : '0.14');
        if (wh) wh.style.opacity = wiresLive ? '0.10' : (wiresDone ? '0.82' : '0.10');

        // Elsa winner row highlight
        const eBg = document.getElementById('io-out-bg-1');
        if (eBg) {{
          eBg.setAttribute('fill', elsaHi ? '#D4F0DC' : '#FFFFFF');
          eBg.setAttribute('stroke', elsaHi ? '#34A853' : '#DADCE0');
          eBg.setAttribute('stroke-width', elsaHi ? '2' : '1.2');
        }}

        // Stage 1 & Stage 4 glow/dim
        const st1 = document.getElementById('io-stage-1');
        const st4 = document.getElementById('io-stage-4');
        const rc = document.getElementById('io-result-card');
        if (st1) st1.className = 'io-stage ' + (activeStage === 1 ? 'glow-blue' : '');
        if (st4) st4.className = 'io-stage ' + (activeStage === 4 ? 'glow-green' : (!winVis ? 'dim' : ''));
        if (rc) rc.style.opacity = winVis ? '1' : '0.18';

        // Sync highlight & lift on matching 4 bottom numbered cards!
        _syncCards(
          ['io-card-1', 'io-card-2', 'io-card-3', 'io-card-4'],
          activeStage >= 1 && activeStage <= 4 ? activeStage - 1 : -1,
          ['blue', 'blue', 'green', 'yellow']
        );
      }}

      // 3. Live narration status bar (dirty-checked!)
      if (ioActiveStep === 1) {{
        _ioSetStatus('io_s1', '<strong style="color:#1A73E8;">Langkah 1/7 (Piksel 1 → Neuron):</strong> Piksel pojok <code>(1,1)</code> terbang lalu pecah menjadi 3 neuron pertama: <code>x₁ (R)</code>, <code>x₂ (G)</code>, <code>x₃ (B)</code>!');
      }} else if (ioActiveStep === 2) {{
        _ioSetStatus('io_s2', '<strong style="color:#1A73E8;">Langkah 2/7 (Piksel 2 → Neuron):</strong> Piksel sebelahnya <code>(1,2)</code> meluncur masuk menjadi <code>x₄ (R)</code>, <code>x₅ (G)</code>, <code>x₆ (B)</code>!');
      }} else if (ioActiveStep === 3) {{
        _ioSetStatus('io_s3', '<strong style="color:#1A73E8;">Langkah 3/7 (Penuh 150.528 Neuron):</strong> Seluruh piksel Elsa mengalir mengisi <code>+150.519 neuron</code> hingga piksel terakhir <code>x150.526..x150.528</code>!');
      }} else if (ioActiveStep === 4) {{
        const wIdx = Math.min(5, Math.floor(ioStepProg * 5) + 1);
        _ioSetStatus(`io_s4_${{wIdx}}`, `<strong style="color:#E37400;">Langkah 4/7 (Koneksi Neuron-by-Neuron):</strong> 1 neuron <code>x₁</code> mengirim sinyal satu per satu ke seluruh 5 output (<code>y₁..y${{wIdx}}</code>)!`);
      }} else if (ioActiveStep === 5) {{
        const nIdx = Math.min(6, Math.floor(ioStepProg * 5) + 2);
        _ioSetStatus(`io_s5_${{nIdx}}`, `<strong style="color:#137333;">Langkah 5/7 (Neuron demi Neuron):</strong> Kini giliran neuron <code>x${{nIdx}}</code> menembakkan 5 koneksi ke Output Layer — skor <strong>Elsa</strong> mulai unggul!`);
      }} else if (ioActiveStep === 6) {{
        _ioSetStatus('io_s6', '<strong style="color:#137333;">Langkah 6/7 (Gelombang Penuh → Softmax):</strong> Seluruh 150.528 neuron menggabungkan bobotnya ke 5 kelas → <strong>Elsa 89%</strong>, Anna 4%, Olaf 3%, Kristoff 2%, Sven 2%!');
      }} else if (ioActiveStep === 7) {{
        _ioSetStatus('io_s7', '<strong style="color:#137333;">Langkah 7/7 (Keputusan Akhir):</strong> Peluang tertinggi <strong>y₂ · Elsa (89%)</strong> terpilih sebagai hasil klasifikasi akhir!');
      }} else if (ioActiveStep === 101 && ioCustomPixel) {{
        const p = ioCustomPixel;
        _ioSetStatus(`io_c101_${{p.idx}}`, `<strong style="color:#1A73E8;">Lacak Piksel (${{p.r + 1}},${{p.c + 1}}):</strong> RGB (<code>${{p.norm[0].toFixed(2)}}, ${{p.norm[1].toFixed(2)}}, ${{p.norm[2].toFixed(2)}}</code>) → masuk Input Layer → menyumbang sinyal ke <strong>Output Layer</strong>!`);
      }} else if (ioActiveStep === 102 && ioInspectInIdx >= 0) {{
        _ioSetStatus(`io_c102_${{ioInspectInIdx}}`, `<strong style="color:#E37400;">Koneksi 1 Neuron Input:</strong> <code>${{IO_IN_LABELS[ioInspectInIdx]}}</code> terhubung ke <strong>semua 5 neuron Output</strong> (masing-masing dikali <em>weight</em> berbeda)!`);
      }} else if (ioActiveStep === 103 && ioInspectOutIdx >= 0) {{
        _ioSetStatus(`io_c103_${{ioInspectOutIdx}}`, `<strong style="color:#137333;">Sinyal Masuk ke y${{ioInspectOutIdx + 1}} (${{IO_OUT_NAMES[ioInspectOutIdx]}}):</strong> Neuron output ini mengumpulkan sinyal dari <strong>seluruh 150.528 neuron Input</strong>!`);
      }} else if (ioCompletedSteps === 0) {{
        _ioSetStatus('io_zero', '<strong>Siap!</strong> Klik <strong>▶ Play</strong> atau <strong>⏭ +1 Langkah</strong> untuk melihat alur dari piksel pertama sampai hasil klasifikasi.');
      }} else {{
        _ioSetStatus('io_default', IO_DEFAULT_STATUS);
      }}
    }}

    function _ioDrawOverlay() {{
      const L = ioLayoutCache || _ioCacheLayout();
      if (!L) return;
      const {{ ctx, W, H, dpr, rImg, rRes, inNodes, ellPt, outNodes, cellW, cellH }} = L;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      const clamp01 = (v) => (v < 0 ? 0 : (v > 1 ? 1 : v));
      const easeIO = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
      const easeOut = (t) => 1 - Math.pow(1 - t, 3);
      const qPt = (x0, y0, cx, cy, x1, y1, u) => {{
        const inv = 1 - u;
        return {{ x: inv * inv * x0 + 2 * inv * u * cx + u * u * x1, y: inv * inv * y0 + 2 * inv * u * cy + u * u * y1 }};
      }};

      const drawRipple = (cx, cy, r0, r1, t, hexCol) => {{
        if (t <= 0 || t >= 1) return;
        const e = easeOut(t);
        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, r0 + (r1 - r0) * e, 0, Math.PI * 2);
        ctx.strokeStyle = _inHexRgba(hexCol, (1 - e) * 0.80);
        ctx.lineWidth = 2.6 * (1 - e * 0.55);
        ctx.stroke();
        ctx.restore();
      }};

      // Helper: draw one animated wire from Input neuron -> Output neuron with traveling glowing pulse!
      const drawWirePulse = (x0, y0, x1, y1, prog, hexCol, lineW, orbR, badgeTxt) => {{
        if (prog <= 0) return;
        const tDraw = clamp01(prog / 0.35);
        const tPulse = clamp01((prog - 0.12) / 0.76);
        const eDraw = easeOut(tDraw);
        const ePulse = easeIO(tPulse);
        const ex = x0 + (x1 - x0) * eDraw;
        const ey = y0 + (y1 - y0) * eDraw;

        // Soft glowing wire
        ctx.save();
        ctx.strokeStyle = _inHexRgba(hexCol, 0.24);
        ctx.lineWidth = lineW + 3.2;
        ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(ex, ey); ctx.stroke();

        ctx.strokeStyle = _inHexRgba(hexCol, 0.92);
        ctx.lineWidth = lineW;
        ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(ex, ey); ctx.stroke();

        // Traveling comet orb along the wire
        if (prog >= 0.12 && prog <= 0.92) {{
          const px = x0 + (x1 - x0) * ePulse;
          const py = y0 + (y1 - y0) * ePulse;
          // 3 tiny trailing dots
          for (let g = 3; g >= 1; g--) {{
            const gu = Math.max(0, ePulse - g * 0.055);
            ctx.beginPath();
            ctx.arc(x0 + (x1 - x0) * gu, y0 + (y1 - y0) * gu, Math.max(1.8, orbR - g * 1.1), 0, Math.PI * 2);
            ctx.fillStyle = _inHexRgba(hexCol, 0.32 * (1 - g / 4));
            ctx.fill();
          }}
          ctx.beginPath(); ctx.arc(px, py, orbR + 3.5, 0, Math.PI * 2);
          ctx.fillStyle = _inHexRgba(hexCol, 0.25); ctx.fill();
          ctx.beginPath(); ctx.arc(px, py, orbR, 0, Math.PI * 2);
          ctx.fillStyle = hexCol; ctx.fill();
          ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 1.6; ctx.stroke();

          if (badgeTxt) {{
            const tw = Math.max(30, badgeTxt.length * 5.6 + 8);
            _fltRoundRect(ctx, px - tw / 2, py - orbR - 16, tw, 13.5, 4);
            ctx.fillStyle = 'rgba(32, 33, 36, 0.90)'; ctx.fill();
            ctx.fillStyle = '#FFFFFF';
            ctx.font = '700 8px Roboto Mono, monospace';
            ctx.textAlign = 'center';
            ctx.fillText(badgeTxt, px, py - orbR - 6.5);
          }}
        }}
        if (prog >= 0.84) {{
          drawRipple(x1, y1, 8, 22, (prog - 0.84) / 0.16, hexCol);
        }}
        ctx.restore();
      }};

      // Helper: draw 1 square pixel lifting from Foto Original -> splitting sequentially into 3 RGB input neurons!
      const drawPixelTo3Neurons = (px, targetIdxs, prog, tag) => {{
        const pxCol = _inPixelCss(px, true);
        const sx = rImg.x + (px.c + 0.5) * cellW;
        const sy = rImg.y + (px.r + 0.5) * cellH;
        const midY = inNodes[targetIdxs[1]] ? inNodes[targetIdxs[1]].cy : (rImg.y + rImg.h * 0.4);
        const splitX = inNodes[0] ? (inNodes[0].cx - 32) : (rImg.x + rImg.w + 34);

        // Highlight source pixel on photo
        ctx.save();
        ctx.fillStyle = 'rgba(251, 188, 4, 0.30)';
        ctx.strokeStyle = '#FBBC04';
        ctx.lineWidth = 2.4;
        ctx.fillRect(rImg.x + px.c * cellW, rImg.y + px.r * cellH, cellW, cellH);
        ctx.strokeRect(rImg.x + px.c * cellW, rImg.y + px.r * cellH, cellW, cellH);
        ctx.restore();

        // Phase A (0.00 -> 0.44): Square pixel glides from Foto Original -> Split Point right beside Input Layer
        const ctrlX = (sx + splitX) * 0.5;
        const ctrlY = Math.min(sy, midY) - 34;
        ctx.save();
        ctx.setLineDash([5, 4]);
        ctx.strokeStyle = `rgba(26, 115, 232, ${{(prog < 0.48 ? 0.85 : 0.25).toFixed(2)}})`;
        ctx.lineWidth = 2.0;
        ctx.beginPath(); ctx.moveTo(sx, sy); ctx.quadraticCurveTo(ctrlX, ctrlY, splitX, midY); ctx.stroke();
        ctx.restore();

        if (prog < 0.50) {{
          const u = easeIO(clamp01(prog / 0.44));
          const pt = qPt(sx, sy, ctrlX, ctrlY, splitX, midY, u);
          for (let g = 5; g >= 1; g--) {{
            const gp = qPt(sx, sy, ctrlX, ctrlY, splitX, midY, Math.max(0, u - g * 0.05));
            const s = 17 - g * 1.8;
            ctx.save();
            ctx.globalAlpha = 0.30 * (1 - g / 6);
            _fltRoundRect(ctx, gp.x - s / 2, gp.y - s / 2, s, s, 3);
            ctx.fillStyle = pxCol; ctx.fill();
            ctx.restore();
          }}
          const a = prog > 0.44 ? clamp01((0.50 - prog) / 0.06) : 1.0;
          ctx.save();
          ctx.globalAlpha = a;
          _fltRoundRect(ctx, pt.x - 10, pt.y - 10, 20, 20, 4);
          ctx.fillStyle = pxCol; ctx.fill();
          ctx.strokeStyle = '#FBBC04'; ctx.lineWidth = 2.2; ctx.stroke();
          if (tag && prog < 0.43) {{
            const tw = Math.max(38, tag.length * 6 + 10);
            _fltRoundRect(ctx, pt.x - tw / 2, pt.y - 28, tw, 14.5, 4);
            ctx.fillStyle = 'rgba(32,33,36,0.9)'; ctx.fill();
            ctx.fillStyle = '#FFFFFF'; ctx.font = '700 8.5px Roboto Mono, monospace'; ctx.textAlign = 'center';
            ctx.fillText(tag, pt.x, pt.y - 18);
          }}
          ctx.restore();
        }}

        // Phase B (0.42 -> 1.00): Smoothly splits into R, G, B orbs landing NEURON-BY-NEURON!
        if (prog >= 0.42) {{
          const rgbCols = ['#EA4335', '#34A853', '#4285F4'];
          targetIdxs.forEach((nIdx, k) => {{
            const dst = inNodes[nIdx];
            if (!dst) return;
            const st = 0.42 + k * 0.12;
            const local = clamp01((prog - st) / 0.34);
            if (local <= 0) return;
            const u = easeIO(local);
            const cx = (splitX + dst.cx) * 0.5;
            const cy = (midY + dst.cy) * 0.5 + (k - 1) * 14;
            const op = qPt(splitX, midY, cx, cy, dst.cx, dst.cy, u);

            ctx.save();
            ctx.setLineDash([4, 3]);
            ctx.strokeStyle = _inHexRgba(rgbCols[k], 0.78);
            ctx.lineWidth = 1.8;
            ctx.beginPath(); ctx.moveTo(splitX, midY); ctx.quadraticCurveTo(cx, cy, dst.cx, dst.cy); ctx.stroke();

            if (local < 0.96) {{
              const rad = 4.5 + 6.5 * easeOut(clamp01(local / 0.25));
              ctx.beginPath(); ctx.arc(op.x, op.y, rad + 3.5, 0, Math.PI * 2);
              ctx.fillStyle = _inHexRgba(rgbCols[k], 0.24); ctx.fill();
              ctx.beginPath(); ctx.arc(op.x, op.y, rad, 0, Math.PI * 2);
              ctx.fillStyle = rgbCols[k]; ctx.fill();
              ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 1.6; ctx.stroke();
            }}
            if (local >= 0.82) {{
              drawRipple(dst.cx, dst.cy, 10, 22, (local - 0.82) / 0.18, rgbCols[k]);
            }}
            ctx.restore();
          }});
        }}
      }};

      // STEP 1: Piksel 1 (1,1) -> x1, x2, x3
      if (ioActiveStep === 1) {{
        drawPixelTo3Neurons(_inGetPixel(0), [0, 1, 2], ioStepProg, 'P1 (1,1)');
        return;
      }}

      // STEP 2: Piksel 2 (1,2) -> x4, x5, x6
      if (ioActiveStep === 2) {{
        drawPixelTo3Neurons(_inGetPixel(1), [3, 4, 5], ioStepProg, 'P2 (1,2)');
        return;
      }}

      // STEP 3: Pixel river into +150.519 + Final Pixel (8,8) -> x150.526..x150.528
      if (ioActiveStep === 3) {{
        const nS = IO_STREAM_PX.length;
        IO_STREAM_PX.forEach((pIdx, k) => {{
          const startT = (k / nS) * 0.45;
          const local = (ioStepProg - startT) / 0.28;
          if (local <= 0 || local >= 1) return;
          const px = _inGetPixel(pIdx);
          const sx = rImg.x + (px.c + 0.5) * cellW;
          const sy = rImg.y + (px.r + 0.5) * cellH;
          const u = easeIO(local);
          const ctrlX = (sx + ellPt.cx) * 0.5;
          const ctrlY = Math.min(sy, ellPt.cy) - 24;
          const pt = qPt(sx, sy, ctrlX, ctrlY, ellPt.cx - 32, ellPt.cy, u);
          const a = local < 0.12 ? local / 0.12 : (local > 0.85 ? (1 - local) / 0.15 : 1.0);
          ctx.save();
          ctx.globalAlpha = a;
          ctx.strokeStyle = 'rgba(251,188,4,0.7)'; ctx.lineWidth = 1.6;
          ctx.strokeRect(rImg.x + px.c * cellW, rImg.y + px.r * cellH, cellW, cellH);
          _fltRoundRect(ctx, pt.x - 6.5, pt.y - 6.5, 13, 13, 3);
          ctx.fillStyle = _inPixelCss(px, true); ctx.fill();
          ctx.strokeStyle = '#FBBC04'; ctx.lineWidth = 1.5; ctx.stroke();
          ctx.restore();
        }});
        if (ioStepProg >= 0.45) {{
          drawPixelTo3Neurons(_inGetPixel(63), [6, 7, 8], clamp01((ioStepProg - 0.45) / 0.55), 'Akhir');
        }}
        return;
      }}

      // STEP 4: Signature Neuron-by-Neuron Wire Demo — x1 connects ONE BY ONE to y1..y5!
      if (ioActiveStep === 4 && inNodes[0]) {{
        const src = inNodes[0];
        // Glowing halo on x1
        ctx.save();
        ctx.beginPath(); ctx.arc(src.cx, src.cy, 15, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(234, 67, 53, 0.24)'; ctx.fill();
        ctx.strokeStyle = '#EA4335'; ctx.lineWidth = 2.4; ctx.stroke();
        ctx.restore();

        outNodes.forEach((dst, j) => {{
          const startT = j * 0.14;
          const local = clamp01((ioStepProg - startT) / 0.42);
          if (local <= 0) return;
          const col = j === 1 ? '#34A853' : IO_OUT_COLS[j];
          drawWirePulse(src.wireX, src.cy, dst.wireX, dst.cy, local, col, j === 1 ? 2.6 : 1.9, j === 1 ? 6.2 : 5.0, `w₁,${{j + 1}}`);
        }});
        return;
      }}

      // STEP 5: Sequential Neuron-by-Neuron Wave down x2 -> x3 -> x4 -> x5 -> x6!
      if (ioActiveStep === 5) {{
        for (let k = 0; k < 5; k++) {{
          const nIdx = k + 1; // x2..x6
          const src = inNodes[nIdx];
          if (!src) continue;
          const startT = k * 0.15;
          const local = clamp01((ioStepProg - startT) / 0.36);
          if (local <= 0) continue;

          // Highlight active input neuron as its wave fires
          if (local < 0.78) {{
            ctx.save();
            ctx.beginPath(); ctx.arc(src.cx, src.cy, 14, 0, Math.PI * 2);
            ctx.fillStyle = _inHexRgba(IO_IN_COLS[nIdx], 0.28); ctx.fill();
            ctx.strokeStyle = IO_IN_COLS[nIdx]; ctx.lineWidth = 2.2; ctx.stroke();
            ctx.restore();
          }}
          outNodes.forEach((dst, j) => {{
            const isElsa = j === 1;
            drawWirePulse(src.wireX, src.cy, dst.wireX, dst.cy, local, isElsa ? '#34A853' : '#9AA0A6', isElsa ? 2.4 : 1.3, isElsa ? 5.6 : 3.6, null);
          }});
        }}
        return;
      }}

      // STEP 6: Full Converging Funnel Wave (+150.519 & x150.526..x150.528 -> Output Layer Softmax!)
      if (ioActiveStep === 6) {{
        const sources = [
          {{ wireX: ellPt.wireX, cy: ellPt.cy, cx: ellPt.cx, col: '#1A73E8' }},
          ...inNodes.slice(6, 9).map((n, k) => ({{ wireX: n.wireX, cy: n.cy, cx: n.cx, col: IO_IN_COLS[6 + k] }})),
        ];
        sources.forEach((src, k) => {{
          const startT = k * 0.14;
          const local = clamp01((ioStepProg - startT) / 0.56);
          if (local <= 0) return;
          if (k > 0 && local < 0.85) {{
            ctx.save();
            ctx.beginPath(); ctx.arc(src.cx, src.cy, 13.5, 0, Math.PI * 2);
            ctx.fillStyle = _inHexRgba(src.col, 0.26); ctx.fill();
            ctx.strokeStyle = src.col; ctx.lineWidth = 2.0; ctx.stroke();
            ctx.restore();
          }}
          outNodes.forEach((dst, j) => {{
            const isElsa = j === 1;
            drawWirePulse(src.wireX, src.cy, dst.wireX, dst.cy, local, isElsa ? '#34A853' : '#B0BEC5', isElsa ? 2.5 : 1.25, isElsa ? 5.8 : 3.4, null);
          }});
        }});
        return;
      }}

      // STEP 7: Winner y2 (Elsa 89%) -> 4. Hasil Klasifikasi!
      if (ioActiveStep === 7 && outNodes[1]) {{
        const elsaOut = outNodes[1];
        const sx = elsaOut.rightX - 6;
        const sy = elsaOut.cy;
        const dx = rRes.x + rRes.w / 2;
        const dy = rRes.y + rRes.h / 2;
        const ctrlX = (sx + dx) * 0.5;
        const ctrlY = Math.min(sy, dy) - 24;

        drawRipple(elsaOut.cx, elsaOut.cy, 11, 26, clamp01(ioStepProg / 0.35), '#34A853');

        const u = easeIO(clamp01((ioStepProg - 0.08) / 0.68));
        ctx.save();
        ctx.setLineDash([6, 4]);
        ctx.strokeStyle = '#34A853'; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(sx, sy); ctx.quadraticCurveTo(ctrlX, ctrlY, dx, dy); ctx.stroke();

        if (ioStepProg >= 0.08 && ioStepProg <= 0.82) {{
          const pt = qPt(sx, sy, ctrlX, ctrlY, dx, dy, u);
          for (let g = 5; g >= 1; g--) {{
            const gp = qPt(sx, sy, ctrlX, ctrlY, dx, dy, Math.max(0, u - g * 0.05));
            ctx.beginPath(); ctx.arc(gp.x, gp.y, 13 - g * 1.8, 0, Math.PI * 2);
            ctx.fillStyle = _inHexRgba('#34A853', 0.28 * (1 - g / 6)); ctx.fill();
          }}
          ctx.beginPath(); ctx.arc(pt.x, pt.y, 19, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(52, 168, 83, 0.24)'; ctx.fill();
          ctx.beginPath(); ctx.arc(pt.x, pt.y, 15, 0, Math.PI * 2);
          ctx.fillStyle = '#34A853'; ctx.fill();
          ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 2.4; ctx.stroke();
          ctx.fillStyle = '#FFFFFF'; ctx.font = '700 9px Roboto Mono, monospace'; ctx.textAlign = 'center';
          ctx.fillText('89%', pt.x, pt.y + 3);
        }}
        if (ioStepProg >= 0.72) {{
          drawRipple(dx, dy, 24, 62, clamp01((ioStepProg - 0.72) / 0.28), '#34A853');
        }}
        ctx.restore();
        return;
      }}

      // CUSTOM 101: User clicked ANY square pixel on Foto Original -> Input -> Output Elsa!
      if (ioActiveStep === 101 && ioCustomPixel && outNodes[1]) {{
        const p = ioCustomPixel;
        const targetTri = p.idx <= 1 ? [0, 1, 2] : (p.idx === 2 ? [3, 4, 5] : (p.idx >= 63 ? [6, 7, 8] : [3, 4, 5]));
        if (ioStepProg < 0.56) {{
          drawPixelTo3Neurons(p, targetTri, clamp01(ioStepProg / 0.56), `(${{p.r + 1}},${{p.c + 1}})`);
        }} else {{
          // Keep source pixel highlighted while 3 RGB wires fire into Output Layer!
          ctx.save();
          ctx.fillStyle = 'rgba(251,188,4,0.28)'; ctx.strokeStyle = '#FBBC04'; ctx.lineWidth = 2.2;
          ctx.fillRect(rImg.x + p.c * cellW, rImg.y + p.r * cellH, cellW, cellH);
          ctx.strokeRect(rImg.x + p.c * cellW, rImg.y + p.r * cellH, cellW, cellH);
          ctx.restore();

          const local2 = clamp01((ioStepProg - 0.54) / 0.46);
          const rgbCols = ['#EA4335', '#34A853', '#4285F4'];
          targetTri.forEach((nIdx, k) => {{
            const src = inNodes[nIdx];
            if (!src) return;
            outNodes.forEach((dst, j) => {{
              const isElsa = j === 1;
              drawWirePulse(src.wireX, src.cy, dst.wireX, dst.cy, local2, isElsa ? rgbCols[k] : '#B0BEC5', isElsa ? 2.4 : 1.1, isElsa ? 5.2 : 2.8, null);
            }});
          }});
        }}
        return;
      }}

      // CUSTOM 102: User clicked ANY Input Neuron -> sequentially fires its 5 outgoing wires to y1..y5!
      if (ioActiveStep === 102 && ioInspectInIdx >= 0 && inNodes[ioInspectInIdx]) {{
        const src = inNodes[ioInspectInIdx];
        const sCol = IO_IN_COLS[ioInspectInIdx];
        ctx.save();
        ctx.beginPath(); ctx.arc(src.cx, src.cy, 15, 0, Math.PI * 2);
        ctx.fillStyle = _inHexRgba(sCol, 0.26); ctx.fill();
        ctx.strokeStyle = sCol; ctx.lineWidth = 2.5; ctx.stroke();
        ctx.restore();

        outNodes.forEach((dst, j) => {{
          const local = clamp01((ioStepProg - j * 0.12) / 0.48);
          if (local <= 0) return;
          drawWirePulse(src.wireX, src.cy, dst.wireX, dst.cy, local, j === 1 ? '#34A853' : IO_OUT_COLS[j], j === 1 ? 2.6 : 1.9, j === 1 ? 6.0 : 4.8, `w${{IO_IN_SHORT[ioInspectInIdx]}},${{j + 1}}`);
        }});
        return;
      }}

      // CUSTOM 103: User clicked ANY Output Class -> fires ALL incoming wires from Input Layer into y_j!
      if (ioActiveStep === 103 && ioInspectOutIdx >= 0 && outNodes[ioInspectOutIdx]) {{
        const dst = outNodes[ioInspectOutIdx];
        const oCol = IO_OUT_COLS[ioInspectOutIdx];
        ctx.save();
        ctx.beginPath(); ctx.arc(dst.cx, dst.cy, 15, 0, Math.PI * 2);
        ctx.fillStyle = _inHexRgba(oCol, 0.24); ctx.fill();
        ctx.strokeStyle = oCol; ctx.lineWidth = 2.4; ctx.stroke();
        ctx.restore();

        inNodes.forEach((src, i) => {{
          const local = clamp01((ioStepProg - i * 0.055) / 0.48);
          if (local <= 0) return;
          drawWirePulse(src.wireX, src.cy, dst.wireX, dst.cy, local, oCol, 2.0, 4.6, null);
        }});
      }}
    }}

    function _tickIoMotion(ts) {{
      if (!ioLastTs) ioLastTs = ts;
      const dt = Math.min(0.033, Math.max(0.001, (ts - ioLastTs) / 1000));
      ioLastTs = ts;
      const speeds = {{ 1: 0.62, 2: 0.65, 3: 0.46, 4: 0.48, 5: 0.45, 6: 0.56, 7: 0.68, 101: 0.52, 102: 0.55, 103: 0.58 }};
      ioStepProg += dt * (speeds[ioActiveStep] || 0.58);

      if (ioStepProg >= 1.0) {{
        if (ioActiveStep >= 100) {{
          ioActiveStep = 0;
          ioStepProg = 0;
          ioAnimRaf = null;
          _ioSyncDom(true);
          _ioClearOverlay();
          return;
        }}
        ioCompletedSteps = Math.max(ioCompletedSteps, ioActiveStep);
        ioStepProg = 0;
        if (ioAutoMode && ioActiveStep < IO_TOTAL_STEPS) {{
          ioActiveStep += 1;
        }} else {{
          ioActiveStep = 0;
          ioAutoMode = false;
          ioAnimRaf = null;
          _ioSetPlayBtn(false);
          _ioSyncDom(true);
          _ioClearOverlay();
          return;
        }}
      }}
      _ioSyncDom(false);
      _ioDrawOverlay();
      ioAnimRaf = requestAnimationFrame(_tickIoMotion);
    }}

    function resetIoMotionZero() {{
      _stopIoAnim();
      ioLayoutCache = null;
      ioLastStatusKey = '';
      ioLastDomKey = '';
      ioLastPctSig = '';
      ioCompletedSteps = 0;
      ioActiveStep = 0;
      ioStepProg = 0;
      ioCustomPixel = null;
      ioInspectInIdx = -1;
      ioInspectOutIdx = -1;
      ioVisualPct = [0, 0, 0, 0, 0];
      _ioSyncDom(true);
      _ioClearOverlay();
    }}

    function playIoMotion() {{
      if (ioAutoMode && ioAnimRaf !== null) {{
        _stopIoAnim();
        ioActiveStep = 0;
        ioCompletedSteps = IO_TOTAL_STEPS;
        _ioSyncDom(true);
        _ioClearOverlay();
        return;
      }}
      _stopIoAnim();
      ioLayoutCache = _ioCacheLayout();
      ioLastStatusKey = '';
      ioLastDomKey = '';
      ioLastPctSig = '';
      ioCompletedSteps = 0;
      ioActiveStep = 1;
      ioStepProg = 0;
      ioVisualPct = [0, 0, 0, 0, 0];
      ioAutoMode = true;
      ioLastTs = 0;
      _ioSetPlayBtn(true);
      _ioSyncDom(true);
      _ioDrawOverlay();
      ioAnimRaf = requestAnimationFrame(_tickIoMotion);
    }}

    function stepIoMotion() {{
      if (ioAutoMode) _stopIoAnim();
      ioLayoutCache = _ioCacheLayout();
      ioLastStatusKey = '';
      ioLastDomKey = '';
      if (ioActiveStep >= 1 && ioActiveStep <= IO_TOTAL_STEPS) {{
        ioCompletedSteps = Math.max(ioCompletedSteps, ioActiveStep);
        ioActiveStep = 0;
      }}
      if (ioCompletedSteps >= IO_TOTAL_STEPS) {{
        ioCompletedSteps = 0;
        ioVisualPct = [0, 0, 0, 0, 0];
      }}
      ioActiveStep = ioCompletedSteps + 1;
      ioStepProg = 0;
      ioAutoMode = false;
      ioLastTs = 0;
      if (ioAnimRaf !== null) cancelAnimationFrame(ioAnimRaf);
      _ioSyncDom(false);
      _ioDrawOverlay();
      ioAnimRaf = requestAnimationFrame(_tickIoMotion);
    }}

    function triggerIoPixelClick(ev) {{
      _stopIoAnim();
      ioLayoutCache = _ioCacheLayout();
      ioLastStatusKey = '';
      ioLastDomKey = '';
      const imgFrame = document.getElementById('io-img-frame');
      let idx = IN_DRESS_IDX;
      if (imgFrame && ev && typeof ev.clientX === 'number') {{
        const rect = imgFrame.getBoundingClientRect();
        const rx = Math.max(0, Math.min(0.999, (ev.clientX - rect.left) / (rect.width || 1)));
        const ry = Math.max(0, Math.min(0.999, (ev.clientY - rect.top) / (rect.height || 1)));
        idx = Math.floor(ry * IN_GRID_N) * IN_GRID_N + Math.floor(rx * IN_GRID_N);
      }}
      ioCompletedSteps = IO_TOTAL_STEPS;
      ioCustomPixel = _inGetPixel(idx);
      ioActiveStep = 101;
      ioStepProg = 0;
      ioAutoMode = false;
      ioLastTs = 0;
      _ioSyncDom(true);
      _ioDrawOverlay();
      ioAnimRaf = requestAnimationFrame(_tickIoMotion);
    }}

    function inspectIoInput(inIdx) {{
      _stopIoAnim();
      ioLayoutCache = _ioCacheLayout();
      ioLastStatusKey = '';
      ioLastDomKey = '';
      ioCompletedSteps = IO_TOTAL_STEPS;
      ioInspectInIdx = inIdx;
      ioInspectOutIdx = -1;
      ioActiveStep = 102;
      ioStepProg = 0;
      ioAutoMode = false;
      ioLastTs = 0;
      _ioSyncDom(true);
      _ioDrawOverlay();
      ioAnimRaf = requestAnimationFrame(_tickIoMotion);
    }}

    function inspectIoOutput(outIdx) {{
      _stopIoAnim();
      ioLayoutCache = _ioCacheLayout();
      ioLastStatusKey = '';
      ioLastDomKey = '';
      ioCompletedSteps = IO_TOTAL_STEPS;
      ioInspectOutIdx = outIdx;
      ioInspectInIdx = -1;
      ioActiveStep = 103;
      ioStepProg = 0;
      ioAutoMode = false;
      ioLastTs = 0;
      _ioSyncDom(true);
      _ioDrawOverlay();
      ioAnimRaf = requestAnimationFrame(_tickIoMotion);
    }}

    // =========================================================================
    // SIMULATOR #4 (Slide 24): Slow-Motion Mathematical Training & Calculation
    // Uses REAL 150.528-pixel (224x224x3) Softmax Regression matching Slide 22 & 23:
    //   x1, x2, x3 (Piksel 1 R/G/B) + [Ellipsis +150.523 piksel lain] + x150.527, x150.528 + Bias
    //   Phase 1 (0.00-0.22): Foto -> Input Layer (150.528 neuron + node +1 Bias)
    //   Phase 2 (0.22-0.56): Weight + Bias -> z = Σ(x·w) + b (lights up Box A!)
    //   Phase 3 (0.56-0.80): Activation Function (Unshifted Softmax e^z / Σe^z) -> P% (Box B!)
    //   Phase 4 (0.80-1.00): Target vs Prediksi -> Error -> Weight & Bias update!
    // =========================================================================
    const TM_VIS_COLS = ['#EA4335', '#34A853', '#4285F4', '#1A73E8', '#EA4335', '#34A853', '#4285F4'];
    const TM_OUT_COLS = ['#4285F4', '#34A853', '#FBBC04', '#EA4335', '#5F6368'];
    const TM_N_VIS = 7; // 3 top pixels (x1..x3) + 1 ellipsis bundle (+150.522) + 3 bottom pixels (x150.526..x150.528)
    let tmPhotoIdx = -1;       // default: -1 (no image picked yet — clean initial / reset state!)
    let tmTrainAlpha = 1.0;    // 0.0 = Sebelum Training (Acak), 1.0 = Sesudah Training (Terlatih)
    let tmPreUpdatePct = null; // Pre-update probability for Target vs Prediksi -> Error readout in Phase 4
    let tmRaf = null;
    let tmMode = 'idle';       // 'idle', 'train' (5 slow passes), 'pulse' (1 slow photo)
    let tmStepIdx = 0;         // 0..4 during slow 5-photo training tour
    let tmStepProg = 1.0;      // 0..1 (1.0 = complete)
    let tmManualPhase = 0;     // 0..4 when using "+1 Tahap Hitung"
    let tmLastRenderedPh = -1;
    let tmLastTs = 0;
    let tmCache = null;

    function _tmSetTrainBtn(running) {{
      const b = document.getElementById('tm-btn-train');
      if (!b) return;
      b.textContent = running ? '■ Stop' : '▶ Play';
      b.style.background = running ? '#EA4335' : '#34A853';
      b.style.borderColor = running ? '#EA4335' : '#34A853';
    }}

    function _stopTmAnim() {{
      if (tmRaf !== null) {{ cancelAnimationFrame(tmRaf); tmRaf = null; }}
      tmMode = 'idle';
      tmPreUpdatePct = null;
      _tmSetTrainBtn(false);
    }}

    function _tmClearCanvas() {{
      const c = document.getElementById('tm-motion-canvas');
      if (!c) return;
      const ctx = c.getContext('2d');
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, c.width, c.height);
    }}

    function _tmEval(photoIdx, alpha) {{
      const x = TRAINING_MATH.X_sample[photoIdx]; // 5 sample corner pixel values (x1,x2,x3,x150527,x150528)
      const round4 = (v) => Math.round(v * 10000) / 10000;
      const round2 = (v) => Math.round(v * 100) / 100;
      const W_samp = TRAINING_MATH.W0_sample.map((row, m) =>
        row.map((v, c) => round4(v + (TRAINING_MATH.W_sample[m][c] - v) * alpha))
      );
      const mid = TRAINING_MATH.mid0[photoIdx].map((v, c) =>
        round2(v + (TRAINING_MATH.mid_trained[photoIdx][c] - v) * alpha)
      );
      const b = TRAINING_MATH.b0.map((v, c) =>
        round2(v + (TRAINING_MATH.b_trained[c] - v) * alpha)
      );
      const sumSamp = [0, 0, 0, 0, 0];
      const z = [0, 0, 0, 0, 0];
      for (let c = 0; c < 5; c++) {{
        let ss = 0;
        for (let m = 0; m < x.length; m++) ss += x[m] * W_samp[m][c];
        sumSamp[c] = ss;
        z[c] = ss + mid[c] + b[c];
      }}
      // Exact unshifted Softmax: e^z / Σe^z (100% calculator-verifiable!)
      const ex = z.map((v) => Math.exp(v));
      const sumEx = ex.reduce((a, c) => a + c, 0);
      const probs = ex.map((v) => (v / sumEx) * 100);
      let predIdx = 0;
      for (let c = 1; c < 5; c++) if (probs[c] > probs[predIdx]) predIdx = c;
      return {{ x, W_samp, mid, b, sumSamp, z, ex, sumEx, probs, predIdx }};
    }}

    function _tmBuildDatasetList() {{
      const host = document.getElementById('tm-dataset-list');
      if (!host || host.children.length > 0) return;
      host.innerHTML = TRAINING_MATH.classes.map((cls, idx) => `
        <div id="tm-ds-${{idx}}" class="tm-ds-item${{idx === tmPhotoIdx ? ' active' : ''}}" onclick="selectTmPhoto(${{idx}})" title="Klik untuk melihat perhitungan 150.528 neuron piksel untuk ${{cls}}!">
          <img src="${{TRAINING_MATH.thumbs[idx]}}" alt="${{cls}}" style="width:28px; height:28px; border-radius:7px; object-fit:cover; border:2px solid ${{TM_OUT_COLS[idx]}}; flex-shrink:0;"/>
          <div style="display:flex; flex-direction:column; line-height:1.15; min-width:0; flex:1;">
            <span style="font-family:var(--font-title); font-size:10px; font-weight:700; color:#202124;">Gambar ${{idx + 1}} · ${{cls}}</span>
            <span style="font-family:var(--font-code); font-size:8.4px; color:#5F6368;">Label: <strong>y${{idx + 1}} = 1</strong></span>
          </div>
          <span style="width:8px; height:8px; border-radius:50%; background:${{TM_OUT_COLS[idx]}}; flex-shrink:0;"></span>
        </div>
      `).join('');
    }}

    function _tmRenderNetwork(activePhase) {{
      _tmBuildDatasetList();
      const ph = typeof activePhase === 'number' ? activePhase : 4; // 1=Input, 2=Weight+Bias, 3=Activation, 4=Complete
      for (let i = 0; i < 5; i++) {{
        const row = document.getElementById(`tm-ds-${{i}}`);
        if (row) row.classList.toggle('active', i === tmPhotoIdx);
      }}

      const hasPhoto = tmPhotoIdx >= 0 && tmPhotoIdx < 5;
      const evalRes = hasPhoto ? _tmEval(tmPhotoIdx, tmTrainAlpha) : null;
      const x = evalRes ? evalRes.x : null;
      const W_samp = evalRes ? evalRes.W_samp : null;
      const mid = evalRes ? evalRes.mid : null;
      const b = evalRes ? evalRes.b : null;
      const sumSamp = evalRes ? evalRes.sumSamp : null;
      const z = evalRes ? evalRes.z : null;
      const ex = evalRes ? evalRes.ex : null;
      const sumEx = evalRes ? evalRes.sumEx : 0;
      const probs = evalRes ? evalRes.probs : null;
      const predIdx = evalRes ? evalRes.predIdx : -1;
      const svg = document.getElementById('tm-svg');
      if (!svg) return;

      const sIds = TRAINING_MATH.sample_ids;
      const sNames = TRAINING_MATH.sample_names;
      const cNames = TRAINING_MATH.classes;
      const cls = hasPhoto ? cNames[tmPhotoIdx] : '';
      const isCorrect = hasPhoto && predIdx === tmPhotoIdx;

      // True funnel geometry (viewBox="0 0 820 248"): REAL 150.528-neuron Input Layer (3 RGB top + ellipsis + 3 RGB bottom)!
      const inY = [47, 68.5, 90, 117, 144, 165.5, 187]; // index 3 = +150.522 ellipsis bundle pill
      const biasY = 223;
      const outY = [74, 105, 136, 167, 198];
      const xInRight = 218;
      const xOutLeft = 524;
      const visToSamp = [0, 1, 2, null, 3, 4, 5];

      let html = '';
      // 1) Input Layer Capsule (REAL 150.528 neurons — 100% consistent with Slide 22 & 23!)
      html += `<rect x="4" y="4" width="214" height="240" rx="13" fill="#E8F0FE" stroke="#4285F4" stroke-width="${{hasPhoto && ph === 1 ? '3' : '2'}}"/>`;
      html += `<text x="111" y="19" text-anchor="middle" font-family="Poppins, Arial" font-size="10.4" font-weight="700" fill="#1A73E8">2. Input Layer (150.528 Neuron)</text>`;
      html += `<text x="111" y="31" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.1" fill="#5F6368">224×224×3 piksel nyata (awal, ..., akhir)</text>`;

      // 2) Output Layer Capsule (VISIBLY SHORTER & CENTERED — true funnel taper!)
      html += `<rect x="516" y="24" width="300" height="200" rx="13" fill="#E6F4EA" stroke="#34A853" stroke-width="${{hasPhoto && ph >= 3 ? '3' : '2'}}"/>`;
      html += `<text x="666" y="41" text-anchor="middle" font-family="Poppins, Arial" font-size="11" font-weight="700" fill="#137333">3. Output Layer (5 Kelas)</text>`;
      html += `<text x="666" y="53" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.8" fill="#5F6368">Activation Function: Softmax</text>`;

      // 3) Top Center Stage Pill + Inline Green/Red/Grey Weight Color Legend
      const isTrainPh4 = hasPhoto && tmMode === 'train' && ph === 4;
      const wPillCol = !hasPhoto ? '#E8F0FE' : (isTrainPh4 ? '#FCE8E6' : (ph === 2 ? '#FEF7E0' : (ph === 3 ? '#E6F4EA' : (tmTrainAlpha < 0.15 ? '#FCE8E6' : '#E6F4EA'))));
      const wPillStr = !hasPhoto ? '#4285F4' : (isTrainPh4 ? '#EA4335' : (ph === 2 ? '#FBBC04' : (ph === 3 ? '#34A853' : (tmTrainAlpha < 0.15 ? '#EA4335' : '#34A853'))));
      const wPillTxt = !hasPhoto ? '#1A73E8' : (isTrainPh4 ? '#C5221F' : (ph === 2 ? '#B06000' : (ph === 3 ? '#137333' : (tmTrainAlpha < 0.15 ? '#C5221F' : '#137333'))));
      const wPillLbl = !hasPhoto
        ? 'Pilih 1 Foto di Kiri / Klik ▶ Play'
        : ph === 1
          ? 'Tahap 1: Baca 150.528 Input Piksel'
          : ph === 2
            ? 'Tahap 2: Hitung Weight + Bias'
            : ph === 3
              ? 'Tahap 3: Activation (Softmax)'
              : isTrainPh4
                ? `Tahap 4: Error → Update w & b (${{Math.round(tmTrainAlpha * 100)}}%)`
                : (tmTrainAlpha < 0.15 ? 'Weight + Bias: Acak (Epoch 0)' : 'Weight + Bias: Terlatih (150.528 w)');
      html += `<rect x="242" y="4" width="254" height="20" rx="8" fill="${{wPillCol}}" stroke="${{wPillStr}}" stroke-width="1.6"/>`;
      html += `<text x="369" y="17.3" text-anchor="middle" font-family="Poppins, Arial" font-size="8.4" font-weight="700" fill="${{wPillTxt}}">${{wPillLbl}}</text>`;
      html += `<circle cx="242" cy="32.5" r="3.3" fill="#34A853"/>`;
      html += `<text x="249" y="35.3" font-family="Roboto, Arial" font-size="7.6" font-weight="700" fill="#137333">Hijau: w &gt; 0 (dukung)</text>`;
      html += `<circle cx="358" cy="32.5" r="3.3" fill="#EA4335"/>`;
      html += `<text x="365" y="35.3" font-family="Roboto, Arial" font-size="7.6" font-weight="700" fill="#C5221F">Merah: w &lt; 0 (tekan)</text>`;
      html += `<circle cx="468" cy="32.5" r="3.1" fill="#9AA0A6"/>`;
      html += `<text x="475" y="35.3" font-family="Roboto, Arial" font-size="7.3" font-weight="700" fill="#5F6368">w≈0</text>`;

      // 4) Background wires (all 6 visual rows to non-target outputs)
      for (let i = 0; i < TM_N_VIS; i++) {{
        for (let j = 0; j < 5; j++) {{
          if (hasPhoto && j === tmPhotoIdx) continue;
          const isMidRow = i === 3;
          const lw = isMidRow ? 1.55 : 0.95;
          html += `<line x1="${{xInRight}}" y1="${{inY[i]}}" x2="${{xOutLeft}}" y2="${{outY[j]}}" stroke="#D0D5DC" stroke-width="${{lw}}" opacity="${{!hasPhoto ? '0.62' : (ph === 1 ? '0.24' : '0.50')}}"/>`;
        }}
      }}

      // 5 & 6) Highlighted Weight wires + Hero 150.523-Pixel Bundle Wire + Bias wire ONLY when a photo is selected!
      const bVal = hasPhoto ? b[tmPhotoIdx] : 0;
      const midVal = hasPhoto ? mid[tmPhotoIdx] : 0;
      if (hasPhoto) {{
        const yTgt = outY[tmPhotoIdx];
        const tPosSample = {{ 0: 0.16, 1: 0.34, 2: 0.16, 4: 0.16, 5: 0.35, 6: 0.16 }};
        for (let i = 0; i < TM_N_VIS; i++) {{
          if (i === 3) continue;
          const m = visToSamp[i];
          const wv = W_samp[m][tmPhotoIdx];
          const isNearZero = Math.abs(wv) < 0.00005;
          const col = isNearZero ? '#9AA0A6' : (wv >= 0 ? '#34A853' : '#EA4335');
          const lw = isNearZero ? 1.2 : 1.7;
          const dash = isNearZero ? ' stroke-dasharray="3,2"' : '';
          const y0 = inY[i];
          html += `<line x1="${{xInRight}}" y1="${{y0}}" x2="${{xOutLeft}}" y2="${{yTgt}}" stroke="${{col}}" stroke-width="${{lw}}"${{dash}} opacity="${{ph >= 2 ? '0.88' : '0.28'}}"/>`;
          const tPos = tPosSample[i];
          const bx = xInRight + (xOutLeft - xInRight) * tPos;
          const by = y0 + (yTgt - y0) * tPos;
          const wKey = m < 3 ? 'w' + (m + 1) : (m === 3 ? 'wₙ₋₂' : (m === 4 ? 'wₙ₋₁' : 'wₙ'));
          const wLbl = isNearZero ? `${{wKey}}:≈0` : `${{wKey}}:${{(wv >= 0 ? '+' : '') + wv.toFixed(3)}}`;
          const pw = isNearZero ? (m >= 3 && m < 5 ? 48 : 42) : (m >= 3 && m < 5 ? 64 : 58);
          const pFill = isNearZero ? '#F1F3F4' : (wv >= 0 ? '#E6F4EA' : '#FCE8E6');
          const pTxt = isNearZero ? '#5F6368' : (wv >= 0 ? '#137333' : '#C5221F');
          html += `<rect x="${{(bx - pw / 2).toFixed(1)}}" y="${{(by - 7.0).toFixed(1)}}" width="${{pw}}" height="14" rx="4.2" fill="${{pFill}}" stroke="${{col}}" stroke-width="1.0" opacity="${{ph >= 2 ? '0.96' : '0.32'}}"/>`;
          html += `<text x="${{bx.toFixed(1)}}" y="${{(by + 2.5).toFixed(1)}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.1" font-weight="700" fill="${{pTxt}}" opacity="${{ph >= 2 ? '1' : '0.35'}}">${{wLbl}}</text>`;
        }}

        // HERO +150.523-pixel bundle wire right through the center!
        const mCol = midVal >= 0 ? '#34A853' : '#EA4335';
        const mLw = Math.min(5.0, 2.2 + Math.abs(midVal) * 0.85);
        html += `<line x1="${{xInRight}}" y1="${{inY[3]}}" x2="${{xOutLeft}}" y2="${{yTgt}}" stroke="${{mCol}}" stroke-width="${{mLw.toFixed(2)}}" opacity="${{ph >= 2 ? '0.96' : '0.30'}}"/>`;
        const mT = 0.43;
        const mBx = xInRight + (xOutLeft - xInRight) * mT;
        const mBy = inY[3] + (yTgt - inY[3]) * mT;
        const mStr = (midVal >= 0 ? '+' : '') + midVal.toFixed(2);
        html += `<rect x="${{(mBx - 64).toFixed(1)}}" y="${{(mBy - 9.5).toFixed(1)}}" width="128" height="19" rx="6" fill="${{midVal >= 0 ? '#E6F4EA' : '#FCE8E6'}}" stroke="${{mCol}}" stroke-width="1.7" opacity="${{ph >= 2 ? '1' : '0.35'}}"/>`;
        html += `<text x="${{mBx.toFixed(1)}}" y="${{(mBy + 3.0).toFixed(1)}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.8" font-weight="800" fill="${{midVal >= 0 ? '#137333' : '#C5221F'}}" opacity="${{ph >= 2 ? '1' : '0.35'}}">Σ 150.522 piksel: ${{mStr}}</text>`;

        // Dedicated Bias dashed wire
        const bSign = (bVal >= 0 ? '+' : '') + bVal.toFixed(2);
        const bT = 0.80;
        const bBx = xInRight + (xOutLeft - xInRight) * bT;
        const bBy = biasY + (yTgt - biasY) * bT;
        html += `<line x1="${{xInRight}}" y1="${{biasY}}" x2="${{xOutLeft}}" y2="${{yTgt}}" stroke="#E37400" stroke-width="2.1" stroke-dasharray="5,3" opacity="${{ph >= 2 ? '0.95' : '0.30'}}"/>`;
        html += `<rect x="${{(bBx - 33).toFixed(1)}}" y="${{(bBy - 8.5).toFixed(1)}}" width="66" height="17" rx="5.5" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.5" opacity="${{ph >= 2 ? '1' : '0.35'}}"/>`;
        html += `<text x="${{bBx.toFixed(1)}}" y="${{(bBy + 2.9).toFixed(1)}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.8" font-weight="700" fill="#B06000" opacity="${{ph >= 2 ? '1' : '0.35'}}">b${{tmPhotoIdx + 1}}:${{bSign}}</text>`;
      }} else {{
        for (let j = 0; j < 5; j++) {{
          html += `<line x1="${{xInRight}}" y1="${{biasY}}" x2="${{xOutLeft}}" y2="${{outY[j]}}" stroke="#F5C76B" stroke-width="1.1" stroke-dasharray="4,3" opacity="0.55"/>`;
        }}
      }}

      // 7) Input Layer REAL 150.528 Neurons (x1..x3 RGB + Ellipsis +150.522 + x150.526..x150.528 RGB + Bias)
      for (let i = 0; i < TM_N_VIS; i++) {{
        if (i === 3) {{
          html += `<rect id="tm-in-c-3" x="14" y="${{inY[3] - 11.5}}" width="194" height="23" rx="7.5" fill="#FFFFFF" stroke="#4285F4" stroke-width="1.5" stroke-dasharray="4,2" opacity="${{hasPhoto ? '1' : '0.82'}}"/>`;
          html += `<text x="111" y="${{inY[3] - 1.2}}" text-anchor="middle" font-family="Poppins, Arial" font-size="8.0" font-weight="700" fill="#1A73E8">⋮ +150.522 neuron piksel</text>`;
          html += `<text x="111" y="${{inY[3] + 8.0}}" text-anchor="middle" font-family="Roboto, Arial" font-size="6.7" fill="#5F6368">(memuat seluruh area figurin)</text>`;
        }} else {{
          const m = visToSamp[i];
          const isEnd = m >= 3;
          html += `<circle id="tm-in-c-${{i}}" cx="25" cy="${{inY[i]}}" r="8.8" fill="${{TM_VIS_COLS[i]}}" stroke="#FFFFFF" stroke-width="1.5" opacity="${{hasPhoto ? '1' : '0.58'}}"/>`;
          html += `<text x="25" y="${{inY[i] + 2.7}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.7" font-weight="700" fill="#FFFFFF">${{hasPhoto ? x[m].toFixed(2) : '—'}}</text>`;
          html += `<text x="39" y="${{inY[i] + 2.8}}" font-family="Roboto Mono, monospace" font-size="${{isEnd ? '7.5' : '8.4'}}" font-weight="700" fill="#202124">${{sIds[m]}}</text>`;
          html += `<text x="${{isEnd ? 89 : 60}}" y="${{inY[i] + 2.8}}" font-family="Roboto, Arial" font-size="8.0" fill="#3C4043">${{sNames[m]}}</text>`;
        }}
      }}
      html += `<line x1="15" y1="204" x2="206" y2="204" stroke="#B6CCF8" stroke-width="1" stroke-dasharray="3,3"/>`;
      html += `<circle id="tm-bias-c" cx="25" cy="${{biasY}}" r="9.4" fill="#FBBC04" stroke="#FFFFFF" stroke-width="1.6" opacity="${{hasPhoto ? '1' : '0.72'}}"/>`;
      html += `<text x="26" y="${{biasY + 3.0}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.0" font-weight="800" fill="#202124">+1</text>`;
      html += `<text x="41" y="${{biasY + 3.1}}" font-family="Poppins, Arial" font-size="8.7" font-weight="700" fill="#B06000">Bias (b)</text>`;
      html += `<text x="92" y="${{biasY + 3.0}}" font-family="Roboto, Arial" font-size="7.9" fill="#5F6368">Ambang kelas</text>`;

      // 8) Output Layer 5 Class Rows
      for (let j = 0; j < 5; j++) {{
        const isTarget = hasPhoto && j === tmPhotoIdx;
        const isWinner = hasPhoto && j === predIdx;
        const fillBg = hasPhoto && ph >= 3 && isTarget ? (isWinner ? '#D4F0DC' : '#FEF7E0') : (hasPhoto && ph === 2 && isTarget ? '#FEF7E0' : '#FFFFFF');
        const strokeBg = hasPhoto && ph >= 3 && isTarget ? (isWinner ? '#34A853' : '#FBBC04') : (hasPhoto && ph === 2 && isTarget ? '#FBBC04' : '#DADCE0');
        const sw = isTarget && ph >= 2 ? '2' : '1.1';
        const pct = hasPhoto && ph >= 3 ? probs[j] : 0;
        const barW = hasPhoto && ph >= 3 ? Math.max(2, Math.round((pct / 100) * 76)) : 0;
        const zStr = hasPhoto && ph >= 2 ? ((z[j] >= 0 ? '+' : '') + z[j].toFixed(2)) : '—';
        const pctStr = hasPhoto && ph >= 3 ? `${{pct.toFixed(1)}}%` : '—';

        html += `<rect id="tm-out-bg-${{j}}" x="524" y="${{outY[j] - 12.5}}" width="282" height="25" rx="7.5" fill="${{fillBg}}" stroke="${{strokeBg}}" stroke-width="${{sw}}"/>`;
        html += `<circle id="tm-out-c-${{j}}" cx="540" cy="${{outY[j]}}" r="8.8" fill="${{TM_OUT_COLS[j]}}" opacity="${{hasPhoto ? '1' : '0.68'}}"/>`;
        html += `<text x="540" y="${{outY[j] + 2.8}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.9" font-weight="700" fill="${{j === 2 ? '#202124' : '#FFFFFF'}}">y${{j + 1}}</text>`;
        html += `<text x="555" y="${{outY[j] + 3.2}}" font-family="Poppins, Arial" font-size="9.5" font-weight="700" fill="${{hasPhoto && ph >= 3 && isTarget && isWinner ? '#137333' : '#202124'}}">${{cNames[j]}}${{isTarget ? ' ★' : ''}}</text>`;
        html += `<text x="662" y="${{outY[j] + 2.9}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.0" font-weight="${{hasPhoto && ph === 2 && isTarget ? '700' : '500'}}" fill="${{hasPhoto && ph === 2 && isTarget ? '#B06000' : '#5F6368'}}">z=${{zStr}}</text>`;
        html += `<rect x="670" y="${{outY[j] - 4.2}}" width="76" height="8.4" rx="4.2" fill="${{isTarget ? '#FFFFFF' : '#F1F3F4'}}"/>`;
        html += `<rect x="670" y="${{outY[j] - 4.2}}" width="${{barW}}" height="8.4" rx="4.2" fill="${{TM_OUT_COLS[j]}}"/>`;
        html += `<text x="798" y="${{outY[j] + 3.2}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="9.1" font-weight="700" fill="${{hasPhoto && ph >= 3 && isTarget && isWinner ? '#137333' : '#3C4043'}}">${{pctStr}}</text>`;
      }}
      svg.innerHTML = html;

      // 9) 2-Box Transparent Live Math Strip (100% Calculator-Exact across ALL 150.528 pixels!)
      const wbBox = document.getElementById('tm-math-wb');
      const wbEq = document.getElementById('tm-math-wb-eq');
      const actBox = document.getElementById('tm-math-act');
      const actEq = document.getElementById('tm-math-act-eq');

      if (wbBox && wbEq) {{
        wbBox.className = 'tm-math-card ' + (!hasPhoto || ph < 2 ? 'dim' : (ph === 2 ? 'glow-yellow' : ''));
        if (!hasPhoto) {{
          wbEq.innerHTML = `<span style="color:#5F6368;">Klik 1 foto di <strong>Dataset Berlabel</strong> atau <strong>▶ Play</strong> untuk memulai perhitungan!</span>`;
        }} else if (ph < 2) {{
          wbEq.innerHTML = `<span style="color:#5F6368;">Menunggu 150.528 nilai piksel (x₁..x₁₅₀.₅₂₈) masuk ke kabel Weight &amp; Bias...</span>`;
        }} else {{
          const ss = sumSamp[tmPhotoIdx];
          const sumWx = ss + midVal;
          const ssTxt = (ss >= 0 ? '+' : '') + ss.toFixed(2);
          const midTxt = (midVal >= 0 ? '+' : '') + midVal.toFixed(2);
          const sumTxt = (sumWx >= 0 ? '+' : '') + sumWx.toFixed(2);
          const bTxt = (bVal >= 0 ? '+ ' : '− ') + Math.abs(bVal).toFixed(2);
          const zTxt = (z[tmPhotoIdx] >= 0 ? '+' : '') + z[tmPhotoIdx].toFixed(2);
          wbEq.innerHTML = `<div style="font-size:8.2px; white-space:nowrap;">6 kanal sudut (<code>${{ssTxt}}</code>) + [Σ 150.522 piksel = <code>${{midTxt}}</code>] = <strong>${{sumTxt}}</strong></div>`
            + `<div>Tambah Bias (<code>b${{tmPhotoIdx + 1}} = ${{bTxt}}</code>) → <strong style="color:#B06000;">Skor Mentah z${{tmPhotoIdx + 1}} = ${{zTxt}}</strong></div>`;
        }}
      }}

      if (actBox && actEq) {{
        actBox.className = 'tm-math-card ' + (!hasPhoto || ph < 3 ? 'dim' : (ph === 3 || (tmMode === 'train' && ph === 4) ? 'glow-green' : ''));
        if (!hasPhoto) {{
          actEq.innerHTML = `<span style="color:#5F6368;">Probabilitas <code>Softmax</code> akan dihitung setelah foto dipilih.</span>`;
        }} else if (ph < 3) {{
          actEq.innerHTML = `<span style="color:#5F6368;">Menunggu skor mentah z₁..z₅ dari tahap Weight + Bias...</span>`;
        }} else if (tmMode === 'train' && ph === 4 && tmPreUpdatePct !== null) {{
          const errGap = Math.max(0, 100 - tmPreUpdatePct);
          actEq.innerHTML = `<div>Target <strong>${{cls}} 100%</strong> vs Prediksi <strong>${{tmPreUpdatePct.toFixed(1)}}%</strong> → <span style="color:#C5221F; font-weight:700;">Error ${{errGap.toFixed(1)}}%</span></div>`
            + `<div>Update <code>w &amp; b</code> → <strong>y${{tmPhotoIdx + 1}} (${{cls}}) naik jadi ${{probs[tmPhotoIdx].toFixed(1)}}%</strong> ✅</div>`;
        }} else {{
          const zTxt = (z[tmPhotoIdx] >= 0 ? '+' : '') + z[tmPhotoIdx].toFixed(2);
          const numE = ex[tmPhotoIdx].toFixed(2);
          const denE = sumEx.toFixed(2);
          const verdict = isCorrect
            ? `<span style="color:#137333; font-weight:700;">✅ Aktif Tertinggi!</span>`
            : `<span style="color:#C5221F; font-weight:700;">❌ Kalah (${{cNames[predIdx]}} ${{probs[predIdx].toFixed(1)}}%)</span>`;
          actEq.innerHTML = `<div><code>e^(${{zTxt}}) / Σe^z</code> = <code>${{numE}} / ${{denE}}</code></div>`
            + `<div>Hasil <strong>y${{tmPhotoIdx + 1}} (${{cls}}) = ${{probs[tmPhotoIdx].toFixed(1)}}%</strong> ${{verdict}}</div>`;
        }}
      }}

      // 9b) Sync 3 bottom step cards with active phase during Play / +1 Tahap / photo pulse!
      const tmIsStepping = hasPhoto && (tmMode !== 'idle' || (tmManualPhase >= 1 && tmManualPhase <= 3));
      const tmCardIdx = !tmIsStepping ? -1 : (ph === 1 ? 0 : (ph === 2 ? 1 : 2));
      _syncCards(['tm-card-1', 'tm-card-2', 'tm-card-3'], tmCardIdx, ['blue', 'yellow', 'green']);

      // 10) Status Pill & Preset Buttons
      const pill = document.getElementById('tm-status-pill');
      if (pill && tmMode === 'idle') {{
        if (!hasPhoto) {{
          pill.className = 'pill blue';
          pill.textContent = 'Siap · Pilih Foto / ▶ Play';
        }} else if (tmTrainAlpha < 0.1) {{
          pill.className = 'pill red';
          pill.textContent = 'Epoch 0 · Weight Acak (Salah Tebak)';
        }} else {{
          pill.className = 'pill green';
          pill.textContent = 'Terlatih · 5/5 Kelas Tepat!';
        }}
      }}
      document.querySelectorAll('#tm-ctrl button[data-tm]').forEach((btn) => {{
        const isBef = btn.dataset.tm === 'before';
        const active = hasPhoto && ((isBef && tmTrainAlpha < 0.1) || (!isBef && tmTrainAlpha > 0.9));
        btn.classList.toggle('outline', !active);
      }});
    }}

    function _tmCacheLayout() {{
      const wrap = document.getElementById('tm-stage-wrap');
      const canvas = document.getElementById('tm-motion-canvas');
      if (!wrap || !canvas) return null;
      const W = wrap.clientWidth, H = wrap.clientHeight;
      if (W < 10 || H < 10) return null;
      const dpr = Math.min(3, (window.devicePixelRatio || 1) * Math.max(1, window.__STAGE_SCALE__ || 1));
      const cw = Math.round(W * dpr), ch = Math.round(H * dpr);
      if (canvas.width !== cw || canvas.height !== ch) {{ canvas.width = cw; canvas.height = ch; }}

      const hR = wrap.getBoundingClientRect();
      const sx = W / (hR.width || 1), sy = H / (hR.height || 1);
      const ptOf = (id) => {{
        const el = document.getElementById(id);
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return {{ x: (r.left - hR.left + r.width / 2) * sx, y: (r.top - hR.top + r.height / 2) * sy, rightX: (r.right - hR.left) * sx, leftX: (r.left - hR.left) * sx }};
      }};
      tmCache = {{
        canvas, ctx: canvas.getContext('2d'), W, H, dpr,
        ds: [0, 1, 2, 3, 4].map((i) => ptOf(`tm-ds-${{i}}`)),
        ins: Array.from({{ length: TM_N_VIS }}, (_, i) => ptOf(`tm-in-c-${{i}}`)),
        bias: ptOf('tm-bias-c'),
        outs: [0, 1, 2, 3, 4].map((j) => ptOf(`tm-out-c-${{j}}`)),
      }};
      return tmCache;
    }}
    window.addEventListener('resize', () => {{ tmCache = null; }});

    function _tmDrawOverlay() {{
      const L = tmCache || _tmCacheLayout();
      if (!L) return;
      const {{ ctx, W, H, dpr, ds, ins, bias, outs }} = L;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      const srcDs = ds[tmPhotoIdx];
      const tgtOut = outs[tmPhotoIdx];
      if (!srcDs || !tgtOut) return;
      const clamp01 = (v) => (v < 0 ? 0 : (v > 1 ? 1 : v));
      const easeIO = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
      const easeOut = (t) => 1 - Math.pow(1 - t, 3);

      // Phase 1 (0.00 -> 0.22): Slow glide from dataset photo -> Input Layer (150.528 neurons)
      if (tmStepProg < 0.24) {{
        const u = easeIO(clamp01(tmStepProg / 0.20));
        ins.forEach((inP, i) => {{
          if (!inP) return;
          const tx = i === 3 ? inP.leftX + 14 : inP.x;
          const ox = srcDs.rightX + (tx - srcDs.rightX) * u;
          const oy = srcDs.y + (inP.y - srcDs.y) * u;
          for (let g = 3; g >= 1; g--) {{
            const gu = Math.max(0, u - g * 0.06);
            ctx.beginPath();
            ctx.arc(srcDs.rightX + (tx - srcDs.rightX) * gu, srcDs.y + (inP.y - srcDs.y) * gu, 4.5 - g * 0.8, 0, Math.PI * 2);
            ctx.fillStyle = _inHexRgba(TM_VIS_COLS[i], 0.25 * (1 - g / 4)); ctx.fill();
          }}
          ctx.save();
          ctx.beginPath(); ctx.arc(ox, oy, 8.5, 0, Math.PI * 2);
          ctx.fillStyle = _inHexRgba(TM_VIS_COLS[i], 0.25); ctx.fill();
          ctx.beginPath(); ctx.arc(ox, oy, 5.4, 0, Math.PI * 2);
          ctx.fillStyle = TM_VIS_COLS[i]; ctx.fill();
          ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 1.6; ctx.stroke();
          ctx.restore();
        }});
      }}

      // Phase 2 (0.22 -> 0.56): Slow travel across 150.528 Weight wires + Bias wire -> Target Neuron!
      if (tmStepProg >= 0.22 && tmStepProg < 0.58) {{
        const u = easeIO(clamp01((tmStepProg - 0.22) / 0.30));
        const sources = bias ? ins.concat([bias]) : ins;
        sources.forEach((inP, idx) => {{
          if (!inP) return;
          const isMidOrb = idx === 3;
          const isBiasOrb = bias && idx === sources.length - 1;
          const sx = isMidOrb ? inP.rightX : inP.x + 14, sy = inP.y;
          const dx = tgtOut.x - 12, dy = tgtOut.y;
          const ox = sx + (dx - sx) * u;
          const oy = sy + (dy - sy) * u;
          const orbCol = isBiasOrb ? '#FBBC04' : (isMidOrb ? '#34A853' : '#E37400');
          const rad = isMidOrb ? 7.2 : 5.4;
          for (let g = 4; g >= 1; g--) {{
            const gu = Math.max(0, u - g * 0.05);
            ctx.beginPath();
            ctx.arc(sx + (dx - sx) * gu, sy + (dy - sy) * gu, rad - g * 0.85, 0, Math.PI * 2);
            ctx.fillStyle = _inHexRgba(orbCol, 0.28 * (1 - g / 5)); ctx.fill();
          }}
          ctx.save();
          ctx.beginPath(); ctx.arc(ox, oy, rad + 3.8, 0, Math.PI * 2);
          ctx.fillStyle = _inHexRgba(orbCol, 0.26); ctx.fill();
          ctx.beginPath(); ctx.arc(ox, oy, rad, 0, Math.PI * 2);
          ctx.fillStyle = orbCol; ctx.fill();
          ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 1.8; ctx.stroke();
          ctx.restore();
        }});
      }}

      // Phase 3 (0.56 -> 0.80): Activation Function (Softmax) pulse expanding on Output neuron!
      if (tmStepProg >= 0.56 && tmStepProg < 0.82) {{
        const rt = easeOut(clamp01((tmStepProg - 0.56) / 0.24));
        ctx.save();
        ctx.beginPath();
        ctx.arc(tgtOut.x, tgtOut.y, 10 + 22 * rt, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(52, 168, 83, ${{(0.88 * (1 - rt)).toFixed(3)}})`;
        ctx.lineWidth = 3.2; ctx.stroke();
        ctx.restore();
      }}

      // Phase 4 (0.80 -> 1.00): Error -> Weight & Bias update confirmation ring!
      if (tmStepProg >= 0.80) {{
        const rt = easeOut(clamp01((tmStepProg - 0.80) / 0.20));
        ctx.save();
        ctx.beginPath();
        ctx.arc(tgtOut.x, tgtOut.y, 12 + 18 * rt, 0, Math.PI * 2);
        ctx.strokeStyle = _inHexRgba(TM_OUT_COLS[tmPhotoIdx], 0.85 * (1 - rt));
        ctx.lineWidth = 2.8; ctx.stroke();
        ctx.restore();
      }}
    }}

    function _tmPhaseFromProg(p) {{
      if (p < 0.22) return 1;
      if (p < 0.56) return 2;
      if (p < 0.80) return 3;
      return 4;
    }}

    function _tickTm(ts) {{
      if (!tmLastTs) tmLastTs = ts;
      const dt = Math.min(0.033, Math.max(0.001, (ts - tmLastTs) / 1000));
      tmLastTs = ts;
      const speed = tmMode === 'train' ? 0.14 : 0.17;
      tmStepProg += dt * speed;
      const ph = _tmPhaseFromProg(tmStepProg);

      if (tmMode === 'train') {{
        const totalPhotos = 5;
        const startA = Math.pow(tmStepIdx / totalPhotos, 0.80);
        const endA   = Math.pow((tmStepIdx + 1) / totalPhotos, 0.80);
        const needWeightUpdate = tmStepProg >= 0.80;
        if (needWeightUpdate) {{
          if (tmPreUpdatePct === null) {{
            tmPreUpdatePct = _tmEval(tmPhotoIdx, startA).probs[tmPhotoIdx];
          }}
          const uUpd = Math.min(1, (tmStepProg - 0.80) / 0.20);
          tmTrainAlpha = startA + (endA - startA) * uUpd;
        }} else {{
          tmPreUpdatePct = null;
          tmTrainAlpha = startA;
        }}

        const clsName = TRAINING_MATH.classes[tmPhotoIdx];
        const pill = document.getElementById('tm-status-pill');
        if (pill) {{
          if (ph === 4 && tmPreUpdatePct !== null) {{
            pill.className = 'pill red';
            pill.textContent = `Target ${{clsName}} 100% vs ${{tmPreUpdatePct.toFixed(1)}}% → Error! Kuatkan w & b ke y${{tmPhotoIdx + 1}}!`;
          }} else {{
            const phLabel = ph === 1 ? '1. Baca 150.528 Input' : (ph === 2 ? '2. Weight + Bias → z' : '3. Softmax → %');
            pill.className = ph === 2 ? 'pill yellow' : (ph === 3 ? 'pill green' : 'pill blue');
            pill.textContent = `Foto ${{tmPhotoIdx + 1}}/5 (${{clsName}}) · ${{phLabel}}`;
          }}
        }}
        if (tmStepProg >= 1.0) {{
          tmStepProg = 0;
          tmStepIdx += 1;
          tmLastRenderedPh = -1;
          tmPreUpdatePct = null;
          if (tmStepIdx >= totalPhotos) {{
            tmPhotoIdx = 1; // Finish cleanly on Elsa!
            tmTrainAlpha = 1.0;
            _stopTmAnim();
            _tmRenderNetwork(4);
            _tmClearCanvas();
            return;
          }}
          tmPhotoIdx = tmStepIdx;
          tmTrainAlpha = Math.pow(tmStepIdx / totalPhotos, 0.80);
        }}
        if (ph !== tmLastRenderedPh || needWeightUpdate) {{
          tmLastRenderedPh = ph;
          _tmRenderNetwork(ph);
        }}
        _tmDrawOverlay();
        tmRaf = requestAnimationFrame(_tickTm);
        return;
      }}

      const clsName = TRAINING_MATH.classes[tmPhotoIdx];
      const phLabel = ph === 1 ? '1. Baca 150.528 Input' : (ph === 2 ? '2. Weight + Bias → z' : (ph === 3 ? '3. Softmax → %' : '4. Hasil Akhir!'));
      const pill = document.getElementById('tm-status-pill');
      if (pill) {{
        pill.className = ph === 2 ? 'pill yellow' : (ph >= 3 ? 'pill green' : 'pill blue');
        pill.textContent = `Uji ${{clsName}} · ${{phLabel}}`;
      }}
      if (tmStepProg >= 1.0) {{
        _stopTmAnim();
        _tmRenderNetwork(4);
        _tmClearCanvas();
        return;
      }}
      if (ph !== tmLastRenderedPh) {{
        tmLastRenderedPh = ph;
        _tmRenderNetwork(ph);
      }}
      _tmDrawOverlay();
      tmRaf = requestAnimationFrame(_tickTm);
    }}

    function playTmSim() {{
      if (tmMode === 'train' && tmRaf !== null) {{
        _stopTmAnim();
        tmTrainAlpha = 1.0;
        tmPhotoIdx = 1;
        tmLastRenderedPh = -1;
        _tmRenderNetwork(4);
        _tmClearCanvas();
        return;
      }}
      _stopTmAnim();
      tmMode = 'train';
      tmStepIdx = 0;
      tmStepProg = 0;
      tmPhotoIdx = 0;
      tmTrainAlpha = 0.0;
      tmPreUpdatePct = null;
      tmLastRenderedPh = 1;
      tmLastTs = 0;
      _tmSetTrainBtn(true);
      _tmRenderNetwork(1);
      tmCache = _tmCacheLayout();
      _tmDrawOverlay();
      tmRaf = requestAnimationFrame(_tickTm);
    }}

    function resetTmSim() {{
      _stopTmAnim();
      tmPhotoIdx = -1;
      tmTrainAlpha = 1.0;
      tmManualPhase = 0;
      tmLastRenderedPh = -1;
      _tmRenderNetwork(0);
      _tmClearCanvas();
    }}

    function stepTmPhase() {{
      _stopTmAnim();
      if (tmPhotoIdx < 0) {{
        tmPhotoIdx = 1; // Default to Elsa when stepping from unselected state
        tmManualPhase = 0;
      }}
      tmManualPhase = tmManualPhase >= 4 ? 1 : tmManualPhase + 1;
      tmLastRenderedPh = tmManualPhase;
      const clsName = TRAINING_MATH.classes[tmPhotoIdx];
      const labels = ['', 'Tahap 1/4: Input Layer (150.528 Neuron + Bias)', 'Tahap 2/4: Hitung Weight + Bias → z', 'Tahap 3/4: Activation Function (Softmax)', 'Tahap 4/4: Hasil Akhir di Output Layer'];
      const pill = document.getElementById('tm-status-pill');
      if (pill) {{
        pill.className = tmManualPhase === 2 ? 'pill yellow' : (tmManualPhase >= 3 ? 'pill green' : 'pill blue');
        pill.textContent = `${{clsName}} · ${{labels[tmManualPhase]}}`;
      }}
      _tmRenderNetwork(tmManualPhase);
      tmCache = _tmCacheLayout();
      tmStepProg = tmManualPhase === 1 ? 0.12 : (tmManualPhase === 2 ? 0.38 : (tmManualPhase === 3 ? 0.68 : 0.90));
      _tmDrawOverlay();
    }}

    function setTmMode(mode) {{
      _stopTmAnim();
      if (tmPhotoIdx < 0) tmPhotoIdx = 1; // Pick Elsa so Before/After contrast is immediately visible
      tmManualPhase = 4;
      tmLastRenderedPh = 4;
      tmTrainAlpha = mode === 'before' ? 0.0 : 1.0;
      _tmRenderNetwork(4);
      _tmClearCanvas();
    }}

    function setTmPdfState(mode) {{
      tmPhotoIdx = 1; // Elsa
      setTmMode(mode);
    }}

    function selectTmPhoto(idx) {{
      _stopTmAnim();
      tmPhotoIdx = idx;
      tmManualPhase = 4;
      tmLastRenderedPh = 1;
      tmMode = 'pulse';
      tmStepProg = 0;
      tmLastTs = 0;
      _tmRenderNetwork(1);
      tmCache = _tmCacheLayout();
      _tmDrawOverlay();
      tmRaf = requestAnimationFrame(_tickTm);
    }}
    tmPhotoIdx = 1; setTmMode('after');

    // =========================================================================
    // SIMULATOR #5 (Slide 25): SEAMLESS ZOOM-IN OF SLIDE 24 TAHAP 4.1 (WEIGHT + BIAS)
    // Uses 100% IDENTICAL 150.528-pixel weights, mid sums, & bias from Slide 24!
    // =========================================================================
    const WB_CHAR_NOTES = [
      '<strong>Zoom-In Tahap 4.1 (Anna · y₁):</strong> <code>150.522 piksel</code> objek menyumbang <code>+2.89</code> (pojok latar <code>w≈0</code>), dikurangi <code>Bias (−0.51)</code> → <strong>z₁ = +2.38</strong> → Softmax <strong>83.0% ✅</strong>!',
      '<strong>Zoom-In Tahap 4.1 (Elsa · y₂):</strong> <code>150.522 piksel</code> objek gaun biru menyumbang <code>+3.17</code> (pojok latar <code>w≈0</code>), lalu <code>Bias (−1.04)</code> menyeimbangkan jadi <strong>z₂ = +2.13</strong> → Softmax <strong>77.7% ✅</strong>!',
      '<strong>Zoom-In Tahap 4.1 (Kristoff · y₃):</strong> <code>150.522 piksel</code> objek menyumbang <code>+2.20</code> + <code>Bias (−0.16)</code> → <strong>z₃ = +2.04</strong> → Softmax <strong>75.4% ✅</strong>!',
      '<strong>Zoom-In Tahap 4.1 (Olaf · y₄):</strong> <code>150.522 piksel</code> objek menyumbang <code>+1.38</code>, diangkat oleh <code>Bias (+0.81)</code> → <strong>z₄ = +2.19</strong> → Softmax <strong>79.2% ✅</strong>!',
      '<strong>Zoom-In Tahap 4.1 (Sven · y₅):</strong> <code>150.522 piksel</code> objek menyumbang <code>+1.10</code>, dibantu <code>Bias (+0.90)</code> → <strong>z₅ = +2.00</strong> → Softmax <strong>74.9% ✅</strong>!',
    ];
    let wbCharIdx = 1; // default Elsa (matches Slide 24!)
    let wbPresetKey = 'elsa_opt';
    let wbTourTimer = null;
    let wbGlideRaf = null;

    function _wbSetTourBtn(running) {{
      const btn = document.getElementById('wb-btn-tour');
      if (!btn) return;
      btn.textContent = running ? '■ Stop' : '▶ Play';
      btn.style.background = running ? '#EA4335' : '#34A853';
      btn.style.borderColor = running ? '#EA4335' : '#34A853';
    }}

    function _stopWbAnim() {{
      if (wbTourTimer !== null) {{ clearInterval(wbTourTimer); wbTourTimer = null; }}
      if (wbGlideRaf !== null) {{ cancelAnimationFrame(wbGlideRaf); wbGlideRaf = null; }}
      _wbSetTourBtn(false);
    }}

    function _wbOrigParams(charIdx) {{
      return {{
        wScale: 1.0,
        b: TRAINING_MATH.b_trained[charIdx],
      }};
    }}

    function _wbPresetParams(charIdx, key) {{
      const o = _wbOrigParams(charIdx);
      if (key === 'no_bias') return {{ wScale: 1.0, b: 0.0 }};
      if (key === 'wrong_w') return {{ wScale: -1.0, b: o.b }};
      return {{ wScale: 1.0, b: o.b }};
    }}

    function _wbGlideTo(targetScale, targetB, presetKey) {{
      if (wbGlideRaf !== null) {{ cancelAnimationFrame(wbGlideRaf); wbGlideRaf = null; }}
      const wEl = document.getElementById('wb-hero-w');
      const bEl = document.getElementById('wb-b');
      if (!wEl || !bEl) return;
      const startW = parseFloat(wEl.value);
      const startB = parseFloat(bEl.value);
      const t0 = performance.now();
      const dur = 480;
      const step = (now) => {{
        const u = Math.min(1, (now - t0) / dur);
        const e = u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
        wEl.value = (startW + (targetScale - startW) * e).toFixed(2);
        bEl.value = (startB + (targetB - startB) * e).toFixed(2);
        updateWb(presetKey);
        if (u < 1) wbGlideRaf = requestAnimationFrame(step);
        else wbGlideRaf = null;
      }};
      wbGlideRaf = requestAnimationFrame(step);
    }}

    function _wbApplyInstant(charIdx, key) {{
      wbCharIdx = charIdx;
      wbPresetKey = key;
      const p = _wbPresetParams(charIdx, key);
      const wEl = document.getElementById('wb-hero-w');
      const bEl = document.getElementById('wb-b');
      if (wEl) wEl.value = p.wScale.toFixed(2);
      if (bEl) bEl.value = p.b.toFixed(2);
      document.querySelectorAll('#wb-presets button[data-wb]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.wb !== key);
      }});
      updateWb(key);
    }}

    function setWbPreset(key) {{
      _stopWbAnim();
      wbPresetKey = key;
      document.querySelectorAll('#wb-presets button[data-wb]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.wb !== key);
      }});
      const p = _wbPresetParams(wbCharIdx, key);
      _wbGlideTo(p.wScale, p.b, key);
    }}

    function setWbPdfState(key) {{
      _stopWbAnim();
      _wbApplyInstant(1, key);
    }}

    function selectWbChar(idx, animate) {{
      wbCharIdx = idx;
      wbPresetKey = 'elsa_opt';
      document.querySelectorAll('#wb-presets button[data-wb]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.wb !== 'elsa_opt');
      }});
      const p = _wbPresetParams(idx, 'elsa_opt');
      if (animate) _wbGlideTo(p.wScale, p.b, 'elsa_opt');
      else _wbApplyInstant(idx, 'elsa_opt');
    }}

    function onWbChipClick(idx) {{
      _stopWbAnim();
      selectWbChar(idx, true);
    }}

    function nextWbChar() {{
      _stopWbAnim();
      selectWbChar((wbCharIdx + 1) % 5, true);
    }}

    function playWbTour() {{
      if (wbTourTimer !== null) {{
        _stopWbAnim();
        return;
      }}
      _stopWbAnim();
      _wbSetTourBtn(true);
      let idx = 0;
      selectWbChar(idx, true);
      wbTourTimer = setInterval(() => {{
        idx += 1;
        if (idx >= 5) {{
          _stopWbAnim();
          selectWbChar(1, true);
          return;
        }}
        selectWbChar(idx, true);
      }}, 3800);
    }}

    function onWbSliderInput() {{
      _stopWbAnim();
      updateWb('');
    }}

    function updateWb(presetTag) {{
      const k = wbCharIdx;
      const clsName = TRAINING_MATH.classes[k];
      const sIds = TRAINING_MATH.sample_ids;
      const x = TRAINING_MATH.X_sample[k];
      const wScale = parseFloat(document.getElementById('wb-hero-w').value);
      const curB = parseFloat(document.getElementById('wb-b').value);

      const evBase = _tmEval(k, 1.0);
      const origMid = evBase.mid[k];
      const origSamp = evBase.sumSamp[k];
      const scaledMid = origMid * wScale;
      const sumWx = origSamp + scaledMid;
      const zCur = sumWx + curB;

      const zAll = evBase.z.slice();
      zAll[k] = zCur;
      const exAll = zAll.map((v) => Math.exp(v));
      const sumExAll = exAll.reduce((a, c) => a + c, 0);
      const probCur = (exAll[k] / sumExAll) * 100;
      let winIdx = 0;
      for (let j = 1; j < 5; j++) if (zAll[j] > zAll[winIdx]) winIdx = j;
      const isWinner = winIdx === k;

      const fmt2 = (v) => (v >= 0 ? '+' : '') + v.toFixed(2);
      const fmtScale = (v) => (v >= 0 ? '+' : '') + v.toFixed(2) + '×';

      // Update slider labels & readouts
      const hl = document.getElementById('wb-hero-lbl');
      if (hl) hl.textContent = 'Weight 150.522 Piksel';
      const hv = document.getElementById('wb-hero-vw');
      if (hv) {{
        hv.textContent = fmtScale(wScale);
        hv.style.color = wScale >= 0 ? '#137333' : '#C5221F';
      }}
      const bl = document.getElementById('wb-bias-lbl');
      if (bl) bl.textContent = `b${{k + 1}} · Bias`;
      const bv = document.getElementById('wb-vb');
      if (bv) bv.textContent = fmt2(curB);

      // 1. Render 5 clickable Frozen character chips showing exact Slide 24 z & %!
      const chipsHost = document.getElementById('wb-ds-chips');
      if (chipsHost) {{
        chipsHost.innerHTML = TRAINING_MATH.classes.map((cls, idx) => {{
          const isAct = idx === k;
          const evC = _tmEval(idx, 1.0);
          const zDisp = isAct ? zCur : evC.z[idx];
          const pDisp = isAct ? probCur : evC.probs[idx];
          const ok = isAct ? isWinner : true;
          const bg = ok ? '#E6F4EA' : '#FCE8E6';
          const col = ok ? '#137333' : '#C5221F';
          return `<div class="ds-chip${{isAct ? ' active' : ''}}" onclick="onWbChipClick(${{idx}})" title="Klik untuk Zoom-In kabel 150.528 Weight &amp; Bias milik ${{cls}}!">
            <img src="${{TRAINING_MATH.thumbs[idx]}}" alt="${{cls}}" style="border-color:${{TM_OUT_COLS[idx]}};"/>
            <span class="c-name">${{cls}}${{isAct ? ' ★' : ''}}</span>
            <span class="c-score" style="background:${{bg}}; color:${{col}};">z=${{fmt2(zDisp)}} · ${{pDisp.toFixed(0)}}%</span>
          </div>`;
        }}).join('');
      }}

      // 2. Render LIVE ZOOM-IN NEURON DIAGRAM SVG (REAL 150.528 pixel inputs: 3 RGB top + ellipsis + 3 RGB bottom!)
      const svg = document.getElementById('wb-zoom-svg');
      if (svg) {{
        const inY = [32, 51, 70, 96, 122, 141, 160];
        const visToSamp = [0, 1, 2, null, 3, 4, 5];
        const shortNames = ['Piksel 1 (R)', 'Piksel 1 (G)', 'Piksel 1 (B)', 'Akhir (R)', 'Akhir (G)', 'Akhir (B)'];
        const biasY = 196;
        const nCy = 104;
        const xLeft = 158;
        const xNeuronLeft = 408;

        let h = '';
        // Left: Input Layer capsule (150.528 neurons!)
        h += `<rect x="3" y="4" width="155" height="210" rx="11" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.8"/>`;
        h += `<text x="80.5" y="16.5" text-anchor="middle" font-family="Poppins, Arial" font-size="8.0" font-weight="700" fill="#1A73E8">Input ${{clsName}} (150.528)</text>`;
        for (let i = 0; i < 7; i++) {{
          if (i === 3) {{
            h += `<rect x="10" y="${{inY[3] - 11.0}}" width="141" height="22" rx="6.5" fill="#FFFFFF" stroke="#FBBC04" stroke-width="2.0"/>`;
            h += `<text x="80.5" y="${{inY[3] - 1.0}}" text-anchor="middle" font-family="Poppins, Arial" font-size="7.4" font-weight="800" fill="#1A73E8">⋮ +150.522 piksel</text>`;
            h += `<text x="80.5" y="${{inY[3] + 7.6}}" text-anchor="middle" font-family="Roboto, Arial" font-size="6.2" fill="#5F6368">Area objek utama (aktif)</text>`;
          }} else {{
            const m = visToSamp[i];
            const isEnd = m >= 3;
            h += `<circle cx="19" cy="${{inY[i]}}" r="7.5" fill="${{TM_VIS_COLS[i]}}" stroke="#FFFFFF" stroke-width="1.4"/>`;
            h += `<text x="19" y="${{inY[i] + 2.4}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="5.9" font-weight="700" fill="#FFFFFF">${{x[m].toFixed(2)}}</text>`;
            h += `<text x="31" y="${{inY[i] + 2.5}}" font-family="Roboto Mono, monospace" font-size="${{isEnd ? '6.7' : '7.5'}}" font-weight="700" fill="#202124">${{sIds[m]}}</text>`;
            h += `<text x="${{isEnd ? 78 : 49}}" y="${{inY[i] + 2.5}}" font-family="Roboto, Arial" font-size="7.0" fill="#5F6368">${{shortNames[m]}}</text>`;
          }}
        }}
        h += `<line x1="11" y1="178" x2="150" y2="178" stroke="#B6CCF8" stroke-width="1" stroke-dasharray="3,2"/>`;
        h += `<circle cx="19" cy="${{biasY}}" r="8.2" fill="#FBBC04" stroke="#FFFFFF" stroke-width="1.5"/>`;
        h += `<text x="19" y="${{biasY + 2.6}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.0" font-weight="800" fill="#202124">+1</text>`;
        h += `<text x="32" y="${{biasY + 2.6}}" font-family="Poppins, Arial" font-size="7.9" font-weight="700" fill="#B06000">Bias (b${{k + 1}})</text>`;

        // Center: 6 corner RGB wires (w ≈ 0 ignored!) + HERO 150.522-pixel thick cable + Dashed Amber Bias Wire!
        for (let i = 0; i < 7; i++) {{
          if (i === 3) continue;
          h += `<line x1="${{xLeft}}" y1="${{inY[i]}}" x2="${{xNeuronLeft}}" y2="${{nCy}}" stroke="#BDC1C6" stroke-width="1.15" stroke-dasharray="3,2" opacity="0.82"/>`;
        }}
        const topBx = xLeft + (xNeuronLeft - xLeft) * 0.44;
        const topBy = inY[1] + (nCy - inY[1]) * 0.44 - 12;
        h += `<rect x="${{(topBx - 54).toFixed(1)}}" y="${{(topBy - 7.5).toFixed(1)}}" width="108" height="15" rx="4.5" fill="#F1F3F4" stroke="#BDC1C6" stroke-width="1"/>`;
        h += `<text x="${{topBx.toFixed(1)}}" y="${{(topBy + 2.6).toFixed(1)}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.9" font-weight="700" fill="#5F6368">Piksel sudut: w≈0 (abaikan)</text>`;

        const botBx = xLeft + (xNeuronLeft - xLeft) * 0.42;
        const botBy = inY[5] + (nCy - inY[5]) * 0.42 + 12;
        h += `<rect x="${{(botBx - 46).toFixed(1)}}" y="${{(botBy - 7.5).toFixed(1)}}" width="92" height="15" rx="4.5" fill="#F1F3F4" stroke="#BDC1C6" stroke-width="1"/>`;
        h += `<text x="${{botBx.toFixed(1)}}" y="${{(botBy + 2.6).toFixed(1)}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.9" font-weight="700" fill="#5F6368">Piksel akhir: w≈0</text>`;

        // HERO 150.522-PIXEL WEIGHT BUNDLE WIRE (controlled live by Slider 1!)
        const mCol = scaledMid >= 0 ? '#34A853' : '#EA4335';
        const mLw = Math.min(5.4, 2.4 + Math.abs(scaledMid) * 0.85);
        h += `<line x1="${{xLeft}}" y1="${{inY[3]}}" x2="${{xNeuronLeft}}" y2="${{nCy}}" stroke="${{mCol}}" stroke-width="${{mLw.toFixed(2)}}" opacity="0.96"/>`;
        const hBx = xLeft + (xNeuronLeft - xLeft) * 0.50;
        const hBy = (inY[3] + nCy) / 2;
        h += `<rect x="${{(hBx - 78).toFixed(1)}}" y="${{(hBy - 12).toFixed(1)}}" width="156" height="24" rx="6.5" fill="${{scaledMid >= 0 ? '#E6F4EA' : '#FCE8E6'}}" stroke="#FBBC04" stroke-width="2.1"/>`;
        h += `<text x="${{hBx.toFixed(1)}}" y="${{(hBy - 1.0).toFixed(1)}}" text-anchor="middle" font-family="Poppins, Arial" font-size="7.1" font-weight="700" fill="#3C4043">Σ 150.522 piksel × (${{fmtScale(wScale)}})</text>`;
        h += `<text x="${{hBx.toFixed(1)}}" y="${{(hBy + 8.6).toFixed(1)}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="800" fill="${{scaledMid >= 0 ? '#137333' : '#C5221F'}}">= ${{fmt2(scaledMid)}}</text>`;

        // Bias dashed wire + amber pill
        const bBx = xLeft + (xNeuronLeft - xLeft) * 0.52;
        const bBy = biasY + (nCy + 14 - biasY) * 0.52 + 12;
        h += `<line x1="${{xLeft}}" y1="${{biasY}}" x2="${{xNeuronLeft}}" y2="${{nCy + 14}}" stroke="#E37400" stroke-width="2.2" stroke-dasharray="5,3"/>`;
        h += `<rect x="${{(bBx - 44).toFixed(1)}}" y="${{(bBy - 8.2).toFixed(1)}}" width="88" height="16.4" rx="5.5" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.6"/>`;
        h += `<text x="${{bBx.toFixed(1)}}" y="${{(bBy + 2.8).toFixed(1)}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.5" font-weight="700" fill="#B06000">Bias b${{k + 1}} = ${{fmt2(curB)}}</text>`;

        // Right: ZOOMED-IN OUTPUT NEURON BOX
        const boxFill = isWinner ? '#FEF7E0' : '#FCE8E6';
        const boxStr = isWinner ? '#FBBC04' : '#EA4335';
        h += `<rect x="${{xNeuronLeft}}" y="12" width="188" height="194" rx="13" fill="${{boxFill}}" stroke="${{boxStr}}" stroke-width="2.2"/>`;
        h += `<circle cx="${{xNeuronLeft + 22}}" cy="31" r="10.5" fill="${{TM_OUT_COLS[k]}}"/>`;
        h += `<text x="${{xNeuronLeft + 22}}" y="34.2" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.4" font-weight="700" fill="${{k === 2 ? '#202124' : '#FFFFFF'}}">y${{k + 1}}</text>`;
        h += `<text x="${{xNeuronLeft + 38}}" y="30" font-family="Poppins, Arial" font-size="10.2" font-weight="700" fill="#202124">Neuron ${{clsName}}</text>`;
        h += `<text x="${{xNeuronLeft + 38}}" y="41" font-family="Roboto, Arial" font-size="7.8" fill="#5F6368">Di dalam 1 neuron output</text>`;

        // Inner Step A1: Sum of 150.528 weighted inputs + Bias
        h += `<rect x="${{xNeuronLeft + 10}}" y="50" width="168" height="84" rx="9" fill="#FFFFFF" stroke="#FDE293" stroke-width="1.4"/>`;
        h += `<text x="${{xNeuronLeft + 94}}" y="65" text-anchor="middle" font-family="Poppins, Arial" font-size="8.4" font-weight="700" fill="#B06000">TAHAP 4.1 · PENJUMLAHAN (Σ)</text>`;
        h += `<text x="${{xNeuronLeft + 94}}" y="80" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.3" fill="#3C4043">Σ(x·w) = ${{fmt2(sumWx)}}</text>`;
        h += `<text x="${{xNeuronLeft + 94}}" y="94" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.3" fill="#B06000">Bias b${{k + 1}} = ${{fmt2(curB)}}</text>`;
        h += `<line x1="${{xNeuronLeft + 26}}" y1="101" x2="${{xNeuronLeft + 162}}" y2="101" stroke="#E0E3E7" stroke-width="1.2"/>`;
        h += `<text x="${{xNeuronLeft + 94}}" y="122" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="14.5" font-weight="800" fill="${{zCur >= 0 ? '#137333' : '#C5221F'}}">z${{k + 1}} = ${{fmt2(zCur)}}</text>`;

        // Down arrow into Faded Preview of Tahap 4.2 (Slide 26: Softmax)
        h += `<line x1="${{xNeuronLeft + 94}}" y1="135" x2="${{xNeuronLeft + 94}}" y2="149" stroke="#34A853" stroke-width="2" stroke-dasharray="3,2"/>`;
        h += `<polygon points="${{xNeuronLeft + 89}},147 ${{xNeuronLeft + 99}},147 ${{xNeuronLeft + 94}},154" fill="#34A853"/>`;
        h += `<rect x="${{xNeuronLeft + 10}}" y="155" width="168" height="42" rx="9" fill="${{isWinner ? '#E6F4EA' : '#FCE8E6'}}" stroke="${{isWinner ? '#A8DAB5' : '#F6AEA9'}}" stroke-width="1.3"/>`;
        h += `<text x="${{xNeuronLeft + 94}}" y="169" text-anchor="middle" font-family="Poppins, Arial" font-size="7.8" font-weight="700" fill="#5F6368">LANJUT KE TAHAP 4.2</text>`;
        h += `<text x="${{xNeuronLeft + 94}}" y="186" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="10.2" font-weight="700" fill="${{isWinner ? '#137333' : '#C5221F'}}">Softmax → ${{probCur.toFixed(1)}}% ${{isWinner ? '✅' : '❌'}}</text>`;

        svg.innerHTML = h;
      }}

      // 2b. Sync 3 left explanation cards with active experiment / Play tour!
      const wbCardIdx = presetTag === 'wrong_w'
        ? 0
        : (presetTag === 'no_bias'
          ? 1
          : (wbTourTimer !== null ? 2 : (presetTag === '' ? (Math.abs(wScale - 1.0) > 0.01 ? 0 : 1) : -1)));
      _syncCards(['wb-card-1', 'wb-card-2', 'wb-card-3'], wbCardIdx, ['blue', 'yellow', 'green']);

      // 3. Live Insight Callout
      const ins = document.getElementById('wb-insight');
      if (ins) {{
        if (presetTag === 'elsa_opt') {{
          ins.className = 'callout green';
          ins.innerHTML = WB_CHAR_NOTES[k];
        }} else if (presetTag === 'no_bias') {{
          ins.className = 'callout yellow';
          ins.innerHTML = `<strong>Efek Bias = 0 pada ${{clsName}}:</strong> Tanpa penggeser <code>b${{k + 1}} (${{fmt2(evBase.b[k])}})</code>, skor bergeser dari <code>${{fmt2(evBase.z[k])}}</code> ke <strong>z${{k + 1}} = ${{fmt2(zCur)}}</strong> (Softmax <strong>${{probCur.toFixed(1)}}%</strong>) — coba klik Olaf/Sven untuk lihat peluangnya anjlok tanpa Bias!`;
        }} else if (presetTag === 'wrong_w') {{
          ins.className = 'callout red';
          ins.innerHTML = `<strong>Efek Balik Weight 150.522 Piksel:</strong> Kabel utama berbalik merah (<code>${{fmtScale(wScale)}}</code>) sehingga sumbangan piksel jadi <code>${{fmt2(scaledMid)}}</code>, skor <strong>z${{k + 1}} jatuh ke ${{fmt2(zCur)}}</strong>, dan peluang ${{clsName}} anjlok jadi <strong>${{probCur.toFixed(1)}}% ❌</strong>!`;
        }} else {{
          wbPresetKey = '';
          document.querySelectorAll('#wb-presets button[data-wb]').forEach((btn) => btn.classList.add('outline'));
          ins.className = isWinner ? 'callout green' : 'callout red';
          ins.innerHTML = `<strong>Eksperimen ${{clsName}}:</strong> Skala <code>Weight=${{fmtScale(wScale)}}</code> &amp; <code>b${{k + 1}}=${{fmt2(curB)}}</code> menghasilkan <strong>z${{k + 1}} = ${{fmt2(zCur)}}</strong> → Softmax <strong>${{probCur.toFixed(1)}}%</strong> (${{isWinner ? 'masih menang ✅' : `kalah dari ${{TRAINING_MATH.classes[winIdx]}} ❌`}}).`;
        }}
      }}
    }}
    _wbApplyInstant(1, 'elsa_opt');

    // =========================================================================
    // SIMULATOR #6 (Slide 26): SEAMLESS ZOOM-IN OF SLIDE 24 TAHAP B (ACTIVATION FUNCTION)
    // Takes the EXACT scores z1..z5 from Slide 24 & Slide 25 and feeds them visibly through
    // ReLU / Sigmoid / Softmax inside a Zoom-In Pipeline SVG (Tahap A z -> Mesin Aktivasi -> Output)!
    // =========================================================================
    let actTab = 'relu';
    let actPhotoIdx = 1; // default Elsa (exact match with Slide 24 & 25!)
    let actManualZ = null; // null = exact Slide 24/25 z; number = live slider override on target neuron z_k
    let actTourTimer = null;

    function _actSetTourBtn(running) {{
      const btn = document.getElementById('act-btn-tour');
      if (!btn) return;
      btn.textContent = running ? '■ Stop' : '▶ Play';
      btn.style.background = running ? '#EA4335' : '#34A853';
      btn.style.borderColor = running ? '#EA4335' : '#34A853';
    }}

    function _stopActTour() {{
      if (actTourTimer !== null) {{ clearInterval(actTourTimer); actTourTimer = null; }}
      _actSetTourBtn(false);
    }}

    function setActTab(tab) {{
      _stopActTour();
      actTab = tab;
      actManualZ = null;
      document.querySelectorAll('#act-tabs button[data-act]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.act !== tab);
      }});
      renderActSim();
    }}

    function setActPdfState(tab) {{
      _stopActTour();
      actPhotoIdx = 1; // Elsa for clean PDF/PPTX export
      setActTab(tab);
    }}

    function selectActPhoto(idx) {{
      _stopActTour();
      actPhotoIdx = idx;
      actManualZ = null;
      renderActSim();
    }}

    function nextActChar() {{
      _stopActTour();
      actPhotoIdx = (actPhotoIdx + 1) % 5;
      actManualZ = null;
      renderActSim();
    }}

    function playActTour() {{
      if (actTourTimer !== null) {{
        _stopActTour();
        return;
      }}
      _stopActTour();
      _actSetTourBtn(true);
      let idx = 0;
      actPhotoIdx = idx;
      actManualZ = null;
      renderActSim();
      actTourTimer = setInterval(() => {{
        idx += 1;
        if (idx >= 5) {{
          _stopActTour();
          actPhotoIdx = 1;
          actManualZ = null;
          renderActSim();
          return;
        }}
        actPhotoIdx = idx;
        actManualZ = null;
        renderActSim();
      }}, 3400);
    }}

    function onActSlider() {{
      _stopActTour();
      const sl = document.getElementById('act-z-slider');
      if (!sl) return;
      actManualZ = parseFloat(sl.value);
      renderActSim();
    }}

    function resetActZ() {{
      _stopActTour();
      actManualZ = null;
      renderActSim();
    }}

    function renderActSim() {{
      const fmt2 = (v) => (v >= 0 ? '+' : '') + v.toFixed(2);
      const cNames = TRAINING_MATH.classes;
      const k = actPhotoIdx;
      const clsName = cNames[k];

      // Get exact Slide 24/25 raw scores z1..z5 for the selected Frozen photo!
      const evBase = _tmEval(k, 1.0);
      const zArr = evBase.z.slice();
      const origZk = evBase.z[k];
      const curZk = actManualZ !== null ? actManualZ : origZk;
      zArr[k] = curZk;

      // Sync slider value & label
      const sl = document.getElementById('act-z-slider');
      if (sl) sl.value = Math.max(-4, Math.min(4, curZk)).toFixed(1);
      const zLbl = document.getElementById('act-z-lbl');
      if (zLbl) zLbl.textContent = `Geser z${{k + 1}} (${{clsName}}):`;

      // Compute outputs for current photo across all 3 functions
      const reluArr = zArr.map((v) => Math.max(0, v));
      const sigK = (1 / (1 + Math.exp(-curZk))) * 100;
      const exArr = zArr.map((v) => Math.exp(v));
      const sumEx = exArr.reduce((a, c) => a + c, 0);
      const smArr = exArr.map((v) => (v / sumEx) * 100);
      let smWin = 0;
      for (let j = 1; j < 5; j++) if (smArr[j] > smArr[smWin]) smWin = j;

      // Update slider readout
      const rEl = document.getElementById('act-z-readout');
      if (rEl) {{
        if (actTab === 'relu') {{
          rEl.textContent = `z=${{fmt2(curZk)}} → ${{reluArr[k].toFixed(2)}}`;
          rEl.style.color = reluArr[k] > 0 ? '#137333' : '#C5221F';
        }} else if (actTab === 'sigmoid') {{
          rEl.textContent = `z=${{fmt2(curZk)}} → ${{sigK.toFixed(1)}}%`;
          rEl.style.color = sigK >= 50 ? '#137333' : '#C5221F';
        }} else {{
          rEl.textContent = `z=${{fmt2(curZk)}} → ${{smArr[k].toFixed(1)}}%`;
          rEl.style.color = smWin === k ? '#137333' : '#C5221F';
        }}
      }}

      // 0. Sync 3 left explanation cards + highlight active function bullet (ReLU / Sigmoid / Softmax)!
      const actBulIdx = actTab === 'relu' ? 0 : (actTab === 'sigmoid' ? 1 : 2);
      _syncCards(['act-b-relu', 'act-b-sigmoid', 'act-b-softmax'], actBulIdx, ['red', 'blue', 'green']);
      const actCardIdx = actManualZ !== null ? 1 : (actTourTimer !== null ? 2 : -1);
      _syncCards(['act-card-1', 'act-card-2', 'act-card-3'], actCardIdx, ['red', 'blue', 'green']);

      // 1. Update 5 Frozen Character Chips (exact Slide 24/25 z -> current Activation output!)
      const chipHost = document.getElementById('act-ds-chips');
      if (chipHost) {{
        chipHost.innerHTML = cNames.map((cls, idx) => {{
          const isAct = idx === k;
          const evC = _tmEval(idx, 1.0);
          const zk = isAct ? curZk : evC.z[idx];
          let txt = '', bg = '#E6F4EA', col = '#137333';
          if (actTab === 'relu') {{
            const rv = Math.max(0, zk);
            txt = `ReLU=${{rv.toFixed(2)}}`;
            bg = rv > 0 ? '#E6F4EA' : '#FCE8E6';
            col = rv > 0 ? '#137333' : '#C5221F';
          }} else if (actTab === 'sigmoid') {{
            const sv = (1 / (1 + Math.exp(-zk))) * 100;
            txt = `σ=${{sv.toFixed(0)}}%`;
            bg = sv >= 50 ? '#E6F4EA' : '#FCE8E6';
            col = sv >= 50 ? '#137333' : '#C5221F';
          }} else {{
            const pv = isAct ? smArr[idx] : evC.probs[idx];
            const ok = isAct ? (smWin === idx) : true;
            txt = `${{pv.toFixed(1)}}%`;
            bg = ok ? '#E6F4EA' : '#FCE8E6';
            col = ok ? '#137333' : '#C5221F';
          }}
          return `<div class="ds-chip${{isAct ? ' active' : ''}}" onclick="selectActPhoto(${{idx}})" title="Klik untuk melihat Tahap B (Activation) pada Foto ${{cls}}!">
            <img src="${{TRAINING_MATH.thumbs[idx]}}" alt="${{cls}}" style="border-color:${{TM_OUT_COLS[idx]}};"/>
            <span class="c-name">${{cls}}${{isAct ? ' ★' : ''}}</span>
            <span class="c-score" style="background:${{bg}}; color:${{col}};">${{txt}}</span>
          </div>`;
        }}).join('');
      }}

      // 2. Render LIVE ZOOM-IN ACTIVATION PIPELINE SVG (Tahap A z -> Mesin Activation -> Output Akhir!)
      const svg = document.getElementById('act-zoom-svg');
      if (svg) {{
        let h = '';
        const rowY = [54, 86, 118, 150, 182];

        // --- TAB 1: ReLU (Hidden Layer) ---
        if (actTab === 'relu') {{
          // Left box: 5 Raw Scores z from Slide 25 (Tahap A)
          h += `<rect x="3" y="6" width="144" height="206" rx="11" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.8"/>`;
          h += `<text x="75" y="21" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="700" fill="#B06000">Hasil Tahap 4.1</text>`;
          h += `<text x="75" y="32" text-anchor="middle" font-family="Roboto, Arial" font-size="7.4" fill="#5F6368">Skor mentah z Foto ${{clsName}}</text>`;
          for (let j = 0; j < 5; j++) {{
            const isT = j === k;
            const zv = zArr[j];
            h += `<rect x="10" y="${{rowY[j] - 11}}" width="130" height="22" rx="6" fill="#FFFFFF" stroke="${{isT ? '#FBBC04' : '#E0E3E7'}}" stroke-width="${{isT ? '1.8' : '1'}}"/>`;
            h += `<circle cx="22" cy="${{rowY[j]}}" r="7.2" fill="${{TM_OUT_COLS[j]}}"/>`;
            h += `<text x="22" y="${{rowY[j] + 2.5}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="${{j === 2 ? '#202124' : '#FFFFFF'}}">z${{j + 1}}</text>`;
            h += `<text x="34" y="${{rowY[j] + 2.8}}" font-family="Poppins, Arial" font-size="8.0" font-weight="${{isT ? '700' : '600'}}" fill="#202124">${{cNames[j]}}</text>`;
            h += `<text x="134" y="${{rowY[j] + 2.8}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="700" fill="${{zv > 0 ? '#137333' : '#C5221F'}}">${{fmt2(zv)}}</text>`;
          }}

          // Arrows Left -> Center Machine & Center Machine -> Right Output
          h += `<line x1="147" y1="109" x2="167" y2="109" stroke="#FBBC04" stroke-width="2.6"/><polygon points="165,104 174,109 165,114" fill="#FBBC04"/>`;
          h += `<line x1="414" y1="109" x2="434" y2="109" stroke="#34A853" stroke-width="2.6"/><polygon points="432,104 441,109 432,114" fill="#34A853"/>`;

          // Center box: Live ReLU Curve Machine!
          h += `<rect x="174" y="6" width="240" height="206" rx="12" fill="#FCE8E6" stroke="#EA4335" stroke-width="2"/>`;
          h += `<text x="294" y="22" text-anchor="middle" font-family="Poppins, Arial" font-size="9.4" font-weight="700" fill="#C5221F">TAHAP 4.2 · MESIN ReLU</text>`;
          h += `<text x="294" y="34" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.8" fill="#5F6368">f(z) = max(0, z)  (Lapisan Fitur)</text>`;
          // Embedded crisp mini SVG coordinate plot (x=186..402, y=44..186)
          const gx0 = 188, gx1 = 400, gy0 = 46, gy1 = 182;
          const xTo = (v) => gx0 + ((Math.max(-4.2, Math.min(4.2, v)) + 4.2) / 8.4) * (gx1 - gx0);
          const yTo = (v) => gy1 - ((Math.max(-0.3, Math.min(4.3, v)) + 0.3) / 4.6) * (gy1 - gy0);
          h += `<rect x="${{gx0}}" y="${{gy0}}" width="${{gx1 - gx0}}" height="${{gy1 - gy0}}" rx="7" fill="#FFFFFF" stroke="#F6AEA9" stroke-width="1.2"/>`;
          h += `<line x1="${{xTo(0).toFixed(1)}}" y1="${{gy0}}" x2="${{xTo(0).toFixed(1)}}" y2="${{gy1}}" stroke="#BDBDBD" stroke-width="1.1" stroke-dasharray="3,2"/>`;
          h += `<line x1="${{gx0 + 4}}" y1="${{yTo(0).toFixed(1)}}" x2="${{xTo(0).toFixed(1)}}" y2="${{yTo(0).toFixed(1)}}" stroke="#EA4335" stroke-width="3" stroke-linecap="round"/>`;
          h += `<line x1="${{xTo(0).toFixed(1)}}" y1="${{yTo(0).toFixed(1)}}" x2="${{gx1 - 4}}" y2="${{yTo(4.0).toFixed(1)}}" stroke="#34A853" stroke-width="3" stroke-linecap="round"/>`;
          h += `<text x="${{gx0 + 6}}" y="${{(yTo(0) - 7).toFixed(1)}}" font-family="Roboto, Arial" font-size="7.6" font-weight="700" fill="#C5221F">z ≤ 0 → Mati (0)</text>`;
          h += `<text x="${{(xTo(0) + 6).toFixed(1)}}" y="${{gy0 + 13}}" font-family="Roboto, Arial" font-size="7.6" font-weight="700" fill="#137333">z &gt; 0 → Lolos Aktif</text>`;
          // Plot all 5 real z dots on the ReLU curve!
          for (let j = 0; j < 5; j++) {{
            const px = xTo(zArr[j]), py = yTo(reluArr[j]);
            const isT = j === k;
            if (isT) h += `<circle cx="${{px.toFixed(1)}}" cy="${{py.toFixed(1)}}" r="9.5" fill="rgba(251,188,4,0.38)"/>`;
            h += `<circle cx="${{px.toFixed(1)}}" cy="${{py.toFixed(1)}}" r="${{isT ? '5.4' : '4.0'}}" fill="${{TM_OUT_COLS[j]}}" stroke="${{isT ? '#202124' : '#FFFFFF'}}" stroke-width="1.5"/>`;
            if (isT) {{
              const rLblX = Math.max(gx0 + 24, Math.min(gx1 - 24, px));
              const rLblY = py < gy0 + 28 ? py + 18 : py - 11;
              h += `<text x="${{rLblX.toFixed(1)}}" y="${{rLblY.toFixed(1)}}" text-anchor="middle" font-family="Poppins, Arial" font-size="8.0" font-weight="700" fill="#202124">${{clsName}}</text>`;
            }}
          }}
          h += `<text x="294" y="199" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.4" fill="#5F6368">Skor mentah z  (-4 ... 0 ... +4)</text>`;

          // Right box: 5 ReLU Outputs (Negative cut to 0.00, Positive pass through!)
          h += `<rect x="441" y="6" width="156" height="206" rx="11" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>`;
          h += `<text x="519" y="21" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="700" fill="#137333">Output Setelah ReLU</text>`;
          h += `<text x="519" y="32" text-anchor="middle" font-family="Roboto, Arial" font-size="7.4" fill="#5F6368">Sinyal ke layer berikutnya</text>`;
          for (let j = 0; j < 5; j++) {{
            const rv = reluArr[j];
            const alive = rv > 0;
            const isT = j === k;
            h += `<rect x="448" y="${{rowY[j] - 11}}" width="142" height="22" rx="6" fill="${{alive ? '#FFFFFF' : '#F8F9FA'}}" stroke="${{isT ? (alive ? '#34A853' : '#EA4335') : '#DADCE0'}}" stroke-width="${{isT ? '1.8' : '1'}}"/>`;
            h += `<text x="456" y="${{rowY[j] + 2.8}}" font-family="Poppins, Arial" font-size="8.0" font-weight="${{isT ? '700' : '600'}}" fill="${{alive ? '#202124' : '#9AA0A6'}}">${{cNames[j]}}</text>`;
            h += `<text x="584" y="${{rowY[j] + 2.8}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.0" font-weight="700" fill="${{alive ? '#137333' : '#C5221F'}}">${{rv.toFixed(2)}} ${{alive ? '✅' : '✕'}}</text>`;
          }}
        }}

        // --- TAB 2: Sigmoid (Output 2 Kelas) ---
        else if (actTab === 'sigmoid') {{
          // Left box: Single Neuron Raw Score z_k from Slide 25
          h += `<rect x="3" y="24" width="144" height="170" rx="11" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.8"/>`;
          h += `<text x="75" y="42" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="700" fill="#B06000">Hasil Tahap 4.1</text>`;
          h += `<text x="75" y="54" text-anchor="middle" font-family="Roboto, Arial" font-size="7.5" fill="#5F6368">1 Neuron Biner (${{clsName}})</text>`;
          h += `<rect x="15" y="72" width="120" height="68" rx="9" fill="#FFFFFF" stroke="#FDE293" stroke-width="1.5"/>`;
          h += `<text x="75" y="90" text-anchor="middle" font-family="Poppins, Arial" font-size="8.4" font-weight="700" fill="#202124">Skor Mentah z${{k + 1}}</text>`;
          h += `<text x="75" y="118" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="16" font-weight="800" fill="${{curZk >= 0 ? '#137333' : '#C5221F'}}">${{fmt2(curZk)}}</text>`;
          h += `<text x="75" y="160" text-anchor="middle" font-family="Roboto, Arial" font-size="7.6" fill="#5F6368">Bisa minus / plus bebas,</text>`;
          h += `<text x="75" y="172" text-anchor="middle" font-family="Roboto, Arial" font-size="7.6" fill="#5F6368">belum berbentuk %!</text>`;

          h += `<line x1="147" y1="109" x2="167" y2="109" stroke="#FBBC04" stroke-width="2.6"/><polygon points="165,104 174,109 165,114" fill="#FBBC04"/>`;
          h += `<line x1="414" y1="109" x2="434" y2="109" stroke="#1A73E8" stroke-width="2.6"/><polygon points="432,104 441,109 432,114" fill="#1A73E8"/>`;

          // Center box: Live Sigmoid S-Curve Machine!
          h += `<rect x="174" y="6" width="240" height="206" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>`;
          h += `<text x="294" y="22" text-anchor="middle" font-family="Poppins, Arial" font-size="9.4" font-weight="700" fill="#1A73E8">TAHAP 4.2 · MESIN Sigmoid</text>`;
          h += `<text x="294" y="34" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.8" fill="#5F6368">σ(z) = 1 / (1 + e⁻ᶻ)  (Output 2 Kelas)</text>`;
          const gx0 = 188, gx1 = 400, gy0 = 46, gy1 = 182;
          const xTo = (v) => gx0 + ((Math.max(-4.2, Math.min(4.2, v)) + 4.2) / 8.4) * (gx1 - gx0);
          const yTo = (v) => gy1 - ((Math.max(-0.06, Math.min(1.06, v)) + 0.06) / 1.12) * (gy1 - gy0);
          h += `<rect x="${{gx0}}" y="${{gy0}}" width="${{gx1 - gx0}}" height="${{gy1 - gy0}}" rx="7" fill="#FFFFFF" stroke="#C6DAFC" stroke-width="1.2"/>`;
          h += `<line x1="${{xTo(0).toFixed(1)}}" y1="${{gy0}}" x2="${{xTo(0).toFixed(1)}}" y2="${{gy1}}" stroke="#BDBDBD" stroke-width="1.1" stroke-dasharray="3,2"/>`;
          h += `<line x1="${{gx0}}" y1="${{yTo(0.5).toFixed(1)}}" x2="${{gx1}}" y2="${{yTo(0.5).toFixed(1)}}" stroke="#BDBDBD" stroke-width="1.1" stroke-dasharray="3,2"/>`;
          let pts = [];
          for (let s = 0; s <= 64; s++) {{
            const xv = -4.1 + (s / 64) * 8.2;
            const yv = 1 / (1 + Math.exp(-xv));
            pts.push(`${{xTo(xv).toFixed(1)}},${{yTo(yv).toFixed(1)}}`);
          }}
          h += `<polyline points="${{pts.join(' ')}}" fill="none" stroke="#1A73E8" stroke-width="3" stroke-linecap="round"/>`;
          h += `<text x="${{gx0 + 6}}" y="${{(yTo(0.5) - 4).toFixed(1)}}" font-family="Roboto Mono, monospace" font-size="7.4" font-weight="700" fill="#5F6368">Ambang 50%</text>`;
          const px = xTo(curZk), py = yTo(sigK / 100);
          const sigLblX = Math.max(gx0 + 24, Math.min(gx1 - 24, px));
          const sigLblY = py < gy0 + 28 ? py + 19 : py - 12;
          h += `<circle cx="${{px.toFixed(1)}}" cy="${{py.toFixed(1)}}" r="10.5" fill="rgba(251,188,4,0.38)"/>`;
          h += `<circle cx="${{px.toFixed(1)}}" cy="${{py.toFixed(1)}}" r="5.6" fill="#FBBC04" stroke="#202124" stroke-width="1.8"/>`;
          h += `<text x="${{sigLblX.toFixed(1)}}" y="${{sigLblY.toFixed(1)}}" text-anchor="middle" font-family="Poppins, Arial" font-size="8.0" font-weight="700" fill="#202124">${{sigK.toFixed(1)}}%</text>`;
          h += `<text x="294" y="199" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.4" fill="#5F6368">Diperas mulus ke rentang 0% – 100%</text>`;

          // Right box: Binary 2-Class Output
          const isYes = sigK >= 50;
          h += `<rect x="441" y="24" width="156" height="170" rx="11" fill="${{isYes ? '#E6F4EA' : '#FCE8E6'}}" stroke="${{isYes ? '#34A853' : '#EA4335'}}" stroke-width="1.8"/>`;
          h += `<text x="519" y="42" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="700" fill="${{isYes ? '#137333' : '#C5221F'}}">Output Biner (2 Kelas)</text>`;
          h += `<rect x="451" y="56" width="136" height="58" rx="8" fill="#FFFFFF" stroke="${{isYes ? '#34A853' : '#DADCE0'}}" stroke-width="1.6"/>`;
          h += `<text x="519" y="72" text-anchor="middle" font-family="Poppins, Arial" font-size="8.4" font-weight="700" fill="#202124">Ya, ${{clsName}}</text>`;
          h += `<text x="519" y="94" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="14.5" font-weight="800" fill="${{isYes ? '#137333' : '#5F6368'}}">${{sigK.toFixed(1)}}%</text>`;
          h += `<rect x="462" y="101" width="114" height="6.5" rx="3.2" fill="#ECEFF1"/>`;
          h += `<rect x="462" y="101" width="${{Math.max(2, Math.round((sigK / 100) * 114))}}" height="6.5" rx="3.2" fill="${{isYes ? '#34A853' : '#9AA0A6'}}"/>`;

          const notPct = 100 - sigK;
          h += `<rect x="451" y="122" width="136" height="44" rx="8" fill="#FFFFFF" stroke="${{!isYes ? '#EA4335' : '#DADCE0'}}" stroke-width="1.4"/>`;
          h += `<text x="519" y="138" text-anchor="middle" font-family="Poppins, Arial" font-size="8.0" font-weight="700" fill="#5F6368">Bukan ${{clsName}}</text>`;
          h += `<text x="519" y="155" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="10.5" font-weight="700" fill="${{!isYes ? '#C5221F' : '#5F6368'}}">${{notPct.toFixed(1)}}%</text>`;
          h += `<text x="519" y="182" text-anchor="middle" font-family="Poppins, Arial" font-size="8.0" font-weight="700" fill="${{isYes ? '#137333' : '#C5221F'}}">${{isYes ? `✅ Prediksi: ${{clsName}}` : `❌ Bukan ${{clsName}}`}}</text>`;
        }}

        // --- TAB 3: Softmax (Output 5 Kelas — 100% IDENTICAL TO SLIDE 24!) ---
        else {{
          // Left box: 5 Raw Scores z1..z5 from Slide 24/25
          h += `<rect x="3" y="6" width="144" height="206" rx="11" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.8"/>`;
          h += `<text x="75" y="21" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="700" fill="#B06000">Hasil Tahap 4.1</text>`;
          h += `<text x="75" y="32" text-anchor="middle" font-family="Roboto, Arial" font-size="7.4" fill="#5F6368">5 Skor Mentah Foto ${{clsName}}</text>`;
          for (let j = 0; j < 5; j++) {{
            const isT = j === k;
            const zv = zArr[j];
            h += `<rect x="10" y="${{rowY[j] - 11}}" width="130" height="22" rx="6" fill="#FFFFFF" stroke="${{isT ? '#FBBC04' : '#E0E3E7'}}" stroke-width="${{isT ? '1.8' : '1'}}"/>`;
            h += `<circle cx="22" cy="${{rowY[j]}}" r="7.2" fill="${{TM_OUT_COLS[j]}}"/>`;
            h += `<text x="22" y="${{rowY[j] + 2.5}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" font-weight="700" fill="${{j === 2 ? '#202124' : '#FFFFFF'}}">z${{j + 1}}</text>`;
            h += `<text x="34" y="${{rowY[j] + 2.8}}" font-family="Poppins, Arial" font-size="8.0" font-weight="${{isT ? '700' : '600'}}" fill="#202124">${{cNames[j]}}</text>`;
            h += `<text x="134" y="${{rowY[j] + 2.8}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="700" fill="${{zv > 0 ? '#137333' : '#C5221F'}}">${{fmt2(zv)}}</text>`;
          }}

          h += `<line x1="147" y1="109" x2="167" y2="109" stroke="#FBBC04" stroke-width="2.6"/><polygon points="165,104 174,109 165,114" fill="#FBBC04"/>`;
          h += `<line x1="376" y1="109" x2="396" y2="109" stroke="#34A853" stroke-width="2.6"/><polygon points="394,104 403,109 394,114" fill="#34A853"/>`;

          // Center box: Exact e^z / Σe^z Machine (100% matching Slide 24 Kotak B!)
          h += `<rect x="174" y="6" width="202" height="206" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/>`;
          h += `<text x="275" y="21" text-anchor="middle" font-family="Poppins, Arial" font-size="9.2" font-weight="700" fill="#137333">TAHAP 4.2 · MESIN Softmax</text>`;
          h += `<text x="275" y="33" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.6" fill="#5F6368">e^z (semua positif) ÷ Σe^z</text>`;
          for (let j = 0; j < 5; j++) {{
            const isT = j === k;
            h += `<rect x="184" y="${{rowY[j] - 10.5}}" width="182" height="21" rx="5.5" fill="#FFFFFF" stroke="${{isT ? '#34A853' : '#C8E6C9'}}" stroke-width="${{isT ? '1.6' : '1'}}"/>`;
            h += `<text x="192" y="${{rowY[j] + 2.8}}" font-family="Roboto Mono, monospace" font-size="7.5" fill="#5F6368">e^(${{fmt2(zArr[j])}})</text>`;
            h += `<text x="358" y="${{rowY[j] + 2.8}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.0" font-weight="700" fill="${{isT ? '#137333' : '#202124'}}">= ${{exArr[j].toFixed(2)}}</text>`;
          }}
          h += `<rect x="194" y="195" width="162" height="14" rx="4.5" fill="#137333"/>`;
          h += `<text x="275" y="204.8" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.5" font-weight="700" fill="#FFFFFF">Total Σe^z = ${{sumEx.toFixed(2)}}</text>`;

          // Right box: Final 5-Class Probabilities (Total = 100.0%)
          h += `<rect x="403" y="6" width="194" height="206" rx="11" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>`;
          h += `<text x="500" y="21" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="700" fill="#137333">Output Akhir (Total 100%)</text>`;
          h += `<text x="500" y="32" text-anchor="middle" font-family="Roboto, Arial" font-size="7.4" fill="#5F6368">Persis Output Layer Tahap 4</text>`;
          for (let j = 0; j < 5; j++) {{
            const pct = smArr[j];
            const isWin = j === smWin;
            h += `<rect x="410" y="${{rowY[j] - 11}}" width="180" height="22" rx="6" fill="${{isWin ? '#D4F0DC' : '#FFFFFF'}}" stroke="${{isWin ? '#34A853' : '#DADCE0'}}" stroke-width="${{isWin ? '1.8' : '1'}}"/>`;
            h += `<text x="418" y="${{rowY[j] + 2.8}}" font-family="Poppins, Arial" font-size="8.0" font-weight="700" fill="${{isWin ? '#137333' : '#202124'}}">${{cNames[j]}}${{isWin ? ' ★' : ''}}</text>`;
            h += `<rect x="478" y="${{rowY[j] - 3.8}}" width="68" height="7.6" rx="3.8" fill="${{isWin ? '#FFFFFF' : '#F1F3F4'}}"/>`;
            h += `<rect x="478" y="${{rowY[j] - 3.8}}" width="${{Math.max(2, Math.round((pct / 100) * 68))}}" height="7.6" rx="3.8" fill="${{TM_OUT_COLS[j]}}"/>`;
            h += `<text x="584" y="${{rowY[j] + 2.8}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="700" fill="${{isWin ? '#137333' : '#3C4043'}}">${{pct.toFixed(1)}}%</text>`;
          }}
        }}

        svg.innerHTML = h;
      }}

      // 3. Bottom Concrete Dataset Takeaway tying back to Slide 24 & Slide 25!
      const cl = document.getElementById('act-callout');
      if (cl) {{
        if (actTab === 'relu') {{
          const negCnt = zArr.filter((v) => v <= 0).length;
          cl.className = reluArr[k] > 0 ? 'callout green' : 'callout red';
          cl.innerHTML = `<strong>Zoom-In Tahap 4.2 (ReLU pada Foto ${{clsName}}):</strong> Dari 5 skor mentah Tahap 4.1, <strong>${{negCnt}} skor negatif dipotong jadi <code>0.00</code></strong> dan <strong>${{clsName}} (<code>z=${{fmt2(curZk)}}</code> → <code>${{reluArr[k].toFixed(2)}}</code>)</strong> ${{reluArr[k] > 0 ? 'lolos aktif ke layer berikutnya!' : 'ikut mati karena negatif!'}}`;
        }} else if (actTab === 'sigmoid') {{
          cl.className = sigK >= 50 ? 'callout green' : 'callout red';
          cl.innerHTML = `<strong>Zoom-In Tahap 4.2 (Sigmoid pada Foto ${{clsName}}):</strong> Skor mentah Tahap 4.1 (<code>z${{k + 1}}=${{fmt2(curZk)}}</code>) diperas kurva-S menjadi <strong>${{sigK.toFixed(1)}}%</strong> (${{sigK >= 50 ? `di atas 50% → <strong>Ya, ${{clsName}} ✅</strong>` : `di bawah 50% → <strong>Bukan ${{clsName}} ❌</strong>`}}).`;
        }} else {{
          cl.className = smWin === k ? 'callout green' : 'callout red';
          cl.innerHTML = `<strong>Zoom-In Tahap 4.2 (Softmax pada Foto ${{clsName}}):</strong> Persis Tahap 4! <code>e^(${{fmt2(curZk)}}) / ${{sumEx.toFixed(2)}}</code> = <strong>${{smArr[k].toFixed(1)}}% ${{clsName}}</strong> (${{smWin === k ? 'menang tertinggi ✅' : `kalah dari ${{cNames[smWin]}} ❌`}}), total 5 kelas selalu <code>100.0%</code>!`;
        }}
      }}
    }}
    setActTab('relu');

    // =========================================================================
    // SIMULATOR #7 (Slide 27): SEAMLESS ZOOM-IN OF SLIDE 24 TAHAP C (OUTPUT AKHIR)
    // Connects 100% identical probabilities from Slide 24 & 26 -> Argmax + Confidence
    // + Evaluation vs Ground-Truth Label (Error & Cross-Entropy Loss)!
    // =========================================================================
    let outMode = 'trained'; // 'trained' | 'ragu' | 'untrained'
    let outPhotoIdx = 1;     // default Elsa (matches Slide 24, 25, & 26!)
    let outThresh = 60;      // confidence threshold (%)
    let outTourTimer = null;

    function _outSetTourBtn(running) {{
      const btn = document.getElementById('out-btn-tour');
      if (!btn) return;
      btn.textContent = running ? '■ Stop' : '▶ Play';
      btn.style.background = running ? '#EA4335' : '#34A853';
      btn.style.borderColor = running ? '#EA4335' : '#34A853';
    }}

    function _stopOutTour() {{
      if (outTourTimer !== null) {{ clearInterval(outTourTimer); outTourTimer = null; }}
      _outSetTourBtn(false);
    }}

    function _outComputeProbs(photoIdx, mode) {{
      const ev = _tmEval(photoIdx, mode === 'untrained' ? 0.0 : 1.0);
      const temp = mode === 'ragu' ? 2.5 : 1.0;
      const zArr = ev.z.map((v) => v / temp);
      const ex = zArr.map((v) => Math.exp(v));
      const sumEx = ex.reduce((a, c) => a + c, 0);
      const probs = ex.map((e) => (e / sumEx) * 100);
      let winIdx = 0;
      for (let c = 1; c < 5; c++) if (probs[c] > probs[winIdx]) winIdx = c;
      const pTrue = probs[photoIdx];
      const errPct = 100 - pTrue;
      const ceLoss = -Math.log(Math.max(pTrue / 100, 1e-6));
      return {{ probs, winIdx, winPct: probs[winIdx], pTrue, errPct, ceLoss, isCorrect: winIdx === photoIdx }};
    }}

    function setOutMode(mode) {{
      _stopOutTour();
      outMode = mode;
      document.querySelectorAll('#out-presets button[data-out]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.out !== mode);
      }});
      renderOutSim();
    }}

    function setOutPdfState(mode) {{
      _stopOutTour();
      outMode = mode;
      outThresh = 60;
      outPhotoIdx = mode === 'untrained' ? 3 : 1; // Olaf salah tebak di Acak; Elsa di Terlatih & Ragu!
      const sl = document.getElementById('out-thresh-slider');
      if (sl) {{ sl.value = '60'; sl.setAttribute('value', '60'); }}
      document.querySelectorAll('#out-presets button[data-out]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.out !== mode);
      }});
      renderOutSim();
    }}

    function onOutChipClick(idx) {{
      _stopOutTour();
      outPhotoIdx = idx;
      renderOutSim();
    }}

    function nextOutChar() {{
      _stopOutTour();
      outPhotoIdx = (outPhotoIdx + 1) % 5;
      renderOutSim();
    }}

    function playOutTour() {{
      if (outTourTimer !== null) {{
        _stopOutTour();
        return;
      }}
      _stopOutTour();
      _outSetTourBtn(true);
      let idx = 0;
      outPhotoIdx = idx;
      renderOutSim();
      outTourTimer = setInterval(() => {{
        idx += 1;
        if (idx >= 5) {{
          _stopOutTour();
          outPhotoIdx = 1;
          renderOutSim();
          return;
        }}
        outPhotoIdx = idx;
        renderOutSim();
      }}, 3200);
    }}

    function onOutThreshInput() {{
      _stopOutTour();
      const sl = document.getElementById('out-thresh-slider');
      if (!sl) return;
      outThresh = parseInt(sl.value, 10) || 60;
      renderOutSim();
    }}

    function resetOutSim() {{
      _stopOutTour();
      outMode = 'trained';
      outPhotoIdx = 1;
      outThresh = 60;
      const sl = document.getElementById('out-thresh-slider');
      if (sl) {{ sl.value = '60'; sl.setAttribute('value', '60'); }}
      document.querySelectorAll('#out-presets button[data-out]').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.out !== 'trained');
      }});
      renderOutSim();
    }}

    function renderOutSim() {{
      const k = outPhotoIdx;
      const cNames = TRAINING_MATH.classes;
      const thumbs = TRAINING_MATH.thumbs;
      const clsName = cNames[k];
      const cur = _outComputeProbs(k, outMode);
      const isConfident = cur.winPct >= outThresh;
      const statusKind = !cur.isCorrect ? 'wrong' : (isConfident ? 'ok' : 'doubt');

      const trReadout = document.getElementById('out-thresh-readout');
      if (trReadout) trReadout.textContent = `≥ ${{outThresh}}%`;

      // 0. Sync 3 left explanation cards with active evaluation mode / Play tour!
      const outCardIdx = outMode === 'untrained'
        ? 2
        : (outMode === 'ragu' || outThresh !== 60
          ? 1
          : (outTourTimer !== null ? 0 : -1));
      _syncCards(['out-card-1', 'out-card-2', 'out-card-3'], outCardIdx, ['green', 'blue', 'red']);

      // 1. Render 5 clickable Frozen character chips showing real decision badge!
      const chipsEl = document.getElementById('out-ds-chips');
      if (chipsEl) {{
        chipsEl.innerHTML = cNames.map((nm, idx) => {{
          const r = _outComputeProbs(idx, outMode);
          const kind = !r.isCorrect ? 'wrong' : (r.winPct >= outThresh ? 'ok' : 'doubt');
          const bg = kind === 'ok' ? '#E6F4EA' : (kind === 'doubt' ? '#FEF7E0' : '#FCE8E6');
          const fg = kind === 'ok' ? '#137333' : (kind === 'doubt' ? '#B06000' : '#C5221F');
          const ico = kind === 'ok' ? '✅' : (kind === 'doubt' ? '⚠' : '❌');
          const isAct = idx === k;
          return `<div class="ds-chip${{isAct ? ' active' : ''}}" onclick="onOutChipClick(${{idx}})" title="Klik untuk cek Output Akhir Foto ${{nm}}">
            <img src="${{thumbs[idx]}}" alt="${{nm}}" style="border-color:${{TM_OUT_COLS[idx]}};"/>
            <div class="c-name">${{nm}}${{isAct ? ' ★' : ''}}</div>
            <div class="c-score" style="background:${{bg}}; color:${{fg}};">${{ico}} ${{r.winPct.toFixed(0)}}%</div>
          </div>`;
        }}).join('');
      }}

      // 2. Render 3-Column Zoom-In Output Decision & Evaluation SVG (viewBox 600x218)
      const svg = document.getElementById('out-zoom-svg');
      if (svg) {{
        let h = '';
        const rowY = [54, 86, 118, 150, 182];
        const statusStroke = statusKind === 'ok' ? '#34A853' : (statusKind === 'doubt' ? '#FBBC04' : '#EA4335');
        const statusFill = statusKind === 'ok' ? '#E6F4EA' : (statusKind === 'doubt' ? '#FEF7E0' : '#FCE8E6');
        const statusText = statusKind === 'ok' ? '#137333' : (statusKind === 'doubt' ? '#B06000' : '#C5221F');

        // LEFT BOX: 5 Softmax Probabilities from Slide 26 (Tahap B)
        h += `<rect x="3" y="6" width="166" height="206" rx="11" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>`;
        h += `<text x="86" y="21" text-anchor="middle" font-family="Poppins, Arial" font-size="8.4" font-weight="700" fill="#137333">Hasil Tahap 4.2</text>`;
        h += `<text x="86" y="32" text-anchor="middle" font-family="Roboto, Arial" font-size="7.3" fill="#5F6368">5 Probabilitas Softmax (100%)</text>`;
        for (let j = 0; j < 5; j++) {{
          const pct = cur.probs[j];
          const isWin = j === cur.winIdx;
          h += `<rect x="10" y="${{rowY[j] - 11}}" width="152" height="22" rx="6" fill="${{isWin ? '#D4F0DC' : '#FFFFFF'}}" stroke="${{isWin ? '#34A853' : '#DADCE0'}}" stroke-width="${{isWin ? '1.8' : '1'}}"/>`;
          h += `<text x="17" y="${{rowY[j] + 2.8}}" font-family="Poppins, Arial" font-size="7.8" font-weight="${{isWin ? '700' : '600'}}" fill="${{isWin ? '#137333' : '#202124'}}">${{cNames[j]}}${{isWin ? ' ★' : ''}}</text>`;
          h += `<rect x="74" y="${{rowY[j] - 3.5}}" width="46" height="7" rx="3.5" fill="${{isWin ? '#FFFFFF' : '#F1F3F4'}}"/>`;
          h += `<rect x="74" y="${{rowY[j] - 3.5}}" width="${{Math.max(2, Math.round((pct / 100) * 46))}}" height="7" rx="3.5" fill="${{TM_OUT_COLS[j]}}"/>`;
          h += `<text x="157" y="${{rowY[j] + 2.8}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="7.9" font-weight="700" fill="${{isWin ? '#137333' : '#3C4043'}}">${{pct.toFixed(1)}}%</text>`;
        }}

        // Arrows Left -> Center & Center -> Right
        h += `<line x1="169" y1="109" x2="188" y2="109" stroke="#34A853" stroke-width="2.6"/><polygon points="186,104 195,109 186,114" fill="#34A853"/>`;
        h += `<line x1="399" y1="109" x2="418" y2="109" stroke="${{statusStroke}}" stroke-width="2.6"/><polygon points="416,104 425,109 416,114" fill="${{statusStroke}}"/>`;

        // CENTER BOX: TAHAP C — ARGMAX & CONFIDENCE METER
        h += `<rect x="195" y="6" width="204" height="206" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>`;
        h += `<text x="297" y="21" text-anchor="middle" font-family="Poppins, Arial" font-size="9.0" font-weight="700" fill="#1A73E8">TAHAP 4.3 · Argmax &amp; Confidence</text>`;
        h += `<text x="297" y="33" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.4" fill="#5F6368">Pilih peluang tertinggi (max)</text>`;

        // Winning Prediction Card inside Center Box
        h += `<rect x="206" y="42" width="182" height="58" rx="9" fill="#FFFFFF" stroke="${{TM_OUT_COLS[cur.winIdx]}}" stroke-width="1.8"/>`;
        h += `<text x="297" y="57" text-anchor="middle" font-family="Roboto, Arial" font-size="7.6" font-weight="700" fill="#5F6368">PREDIKSI MODEL (Argmax)</text>`;
        h += `<text x="297" y="77" text-anchor="middle" font-family="Poppins, Arial" font-size="14.5" font-weight="800" fill="#202124">${{cNames[cur.winIdx].toUpperCase()}}</text>`;
        h += `<text x="297" y="92" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.6" font-weight="700" fill="${{statusText}}">Confidence = ${{cur.winPct.toFixed(1)}}%</text>`;

        // Live Confidence vs Threshold Gauge Bar (x=212..382, width=170)
        const bx = 212, bw = 170, by = 122;
        const fillW = Math.max(3, Math.round((cur.winPct / 100) * bw));
        const thX = bx + Math.round((outThresh / 100) * bw);
        h += `<text x="${{bx}}" y="114" font-family="Poppins, Arial" font-size="7.6" font-weight="700" fill="#202124">Cek vs Ambang Yakin</text>`;
        h += `<text x="${{bx + bw}}" y="114" text-anchor="end" font-family="Roboto Mono, monospace" font-size="7.6" font-weight="700" fill="#1A73E8">Ambang ${{outThresh}}%</text>`;
        h += `<rect x="${{bx}}" y="${{by}}" width="${{bw}}" height="14" rx="7" fill="#FFFFFF" stroke="#C6DAFC" stroke-width="1.2"/>`;
        h += `<rect x="${{bx}}" y="${{by}}" width="${{fillW}}" height="14" rx="7" fill="${{statusStroke}}"/>`;
        // Vertical dashed threshold marker
        h += `<line x1="${{thX}}" y1="${{by - 5}}" x2="${{thX}}" y2="${{by + 19}}" stroke="#202124" stroke-width="1.8" stroke-dasharray="3,2"/>`;
        h += `<text x="${{bx}}" y="${{by + 27}}" font-family="Roboto Mono, monospace" font-size="7.0" fill="#5F6368">0%</text>`;
        h += `<text x="${{bx + bw / 2}}" y="${{by + 27}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.0" fill="#5F6368">50%</text>`;
        h += `<text x="${{bx + bw}}" y="${{by + 27}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="7.0" fill="#5F6368">100%</text>`;

        // Decision Badge at bottom of Center Box
        const decTitle = !cur.isCorrect
          ? '❌ PREDIKSI SALAH!'
          : (isConfident ? '✅ YAKIN · DITERIMA' : '⚠ RAGU · CEK MANUAL');
        const decSub = !cur.isCorrect
          ? `Tebak ${{cNames[cur.winIdx]}}, padahal ${{clsName}}`
          : (isConfident ? `${{cur.winPct.toFixed(1)}}% ≥ ambang ${{outThresh}}%` : `${{cur.winPct.toFixed(1)}}% &lt; ambang ${{outThresh}}%`);
        h += `<rect x="206" y="160" width="182" height="42" rx="8" fill="${{statusFill}}" stroke="${{statusStroke}}" stroke-width="1.6"/>`;
        h += `<text x="297" y="177" text-anchor="middle" font-family="Poppins, Arial" font-size="8.8" font-weight="800" fill="${{statusText}}">${{decTitle}}</text>`;
        h += `<text x="297" y="192" text-anchor="middle" font-family="Roboto, Arial" font-size="7.6" font-weight="600" fill="#3C4043">${{decSub}}</text>`;

        // RIGHT BOX: EVALUASI VS LABEL ASLI (ERROR & LOSS -> BRIDGE TO TRAINING!)
        h += `<rect x="425" y="6" width="172" height="206" rx="11" fill="${{statusFill}}" stroke="${{statusStroke}}" stroke-width="1.8"/>`;
        h += `<text x="511" y="21" text-anchor="middle" font-family="Poppins, Arial" font-size="8.5" font-weight="700" fill="${{statusText}}">Evaluasi vs Label Asli</text>`;
        h += `<text x="511" y="32" text-anchor="middle" font-family="Roboto, Arial" font-size="7.3" fill="#5F6368">Target 100% − Prediksi</text>`;

        // Ground Truth Card
        h += `<rect x="434" y="42" width="154" height="42" rx="8" fill="#FFFFFF" stroke="#DADCE0" stroke-width="1.2"/>`;
        h += `<text x="511" y="56" text-anchor="middle" font-family="Roboto, Arial" font-size="7.4" fill="#5F6368">Label Asli Foto</text>`;
        h += `<text x="511" y="74" text-anchor="middle" font-family="Poppins, Arial" font-size="11.2" font-weight="800" fill="#202124">${{clsName}} (Target 100%)</text>`;

        // Error & Loss Readout Card
        h += `<rect x="434" y="92" width="154" height="62" rx="8" fill="#FFFFFF" stroke="${{statusStroke}}" stroke-width="1.5"/>`;
        h += `<text x="444" y="109" font-family="Roboto, Arial" font-size="7.6" fill="#5F6368">P(${{clsName}}):</text>`;
        h += `<text x="578" y="109" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="700" fill="#202124">${{cur.pTrue.toFixed(1)}}%</text>`;
        h += `<text x="444" y="127" font-family="Roboto, Arial" font-size="7.6" font-weight="700" fill="${{statusText}}">Error (100−P):</text>`;
        h += `<text x="578" y="127" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.6" font-weight="800" fill="${{statusText}}">${{cur.errPct.toFixed(1)}}%</text>`;
        h += `<text x="444" y="145" font-family="Roboto, Arial" font-size="7.6" fill="#5F6368">Loss (−ln P):</text>`;
        h += `<text x="578" y="145" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.4" font-weight="700" fill="${{statusText}}">${{cur.ceLoss.toFixed(2)}}</text>`;

        // Feedback Loop Footer Pill
        const fbTxt = !cur.isCorrect
          ? '↩ Error Besar → Koreksi Weight!'
          : (isConfident ? '✅ Loss Kecil → Bobot Sudah Baik' : '↩ Loss Sedang → Perlu Latih Lagi');
        h += `<rect x="434" y="164" width="154" height="36" rx="8" fill="${{statusStroke}}"/>`;
        h += `<text x="511" y="185" text-anchor="middle" font-family="Poppins, Arial" font-size="7.6" font-weight="700" fill="${{statusKind === 'doubt' ? '#202124' : '#FFFFFF'}}">${{fbTxt}}</text>`;

        svg.innerHTML = h;
      }}

      // 3. Bottom Concrete Takeaway
      const cl = document.getElementById('out-callout');
      if (cl) {{
        if (!cur.isCorrect) {{
          cl.className = 'callout red';
          cl.innerHTML = `<strong>Zoom-In Tahap 4.3 (Foto ${{clsName}} · Acak):</strong> <code>Argmax</code> salah memilih <strong>${{cNames[cur.winIdx]}} (${{cur.winPct.toFixed(1)}}%)</strong>, sedangkan peluang ${{clsName}} hanya <code>${{cur.pTrue.toFixed(1)}}%</code> → <strong>Error ${{cur.errPct.toFixed(1)}}% (Loss ${{cur.ceLoss.toFixed(2)}})</strong> dikirim balik untuk memperbaiki bobot!`;
        }} else if (!isConfident) {{
          cl.className = 'callout yellow';
          cl.innerHTML = `<strong>Zoom-In Tahap 4.3 (Foto ${{clsName}} · Ragu):</strong> <code>Argmax</code> memang memilih <strong>${{clsName}} (${{cur.winPct.toFixed(1)}}%)</strong>, tetapi masih di bawah ambang <code>${{outThresh}}%</code> (<code>Error ${{cur.errPct.toFixed(1)}}%</code>) → perlu verifikasi manual atau tambahan <em>training</em>!`;
        }} else {{
          cl.className = 'callout green';
          cl.innerHTML = `<strong>Zoom-In Tahap 4.3 (Foto ${{clsName}} · Terlatih):</strong> Persis Tahap 4 &amp; 4.2! <code>Argmax</code> memilih <strong>${{clsName}} (${{cur.winPct.toFixed(1)}}%)</strong> ≥ ambang <code>${{outThresh}}%</code> → <strong>Prediksi Benar &amp; Yakin ✅</strong> (<code>Loss = ${{cur.ceLoss.toFixed(2)}}</code>)!`;
        }}
      }}
    }}
    renderOutSim();

    // =========================================================================
    // SIMULATOR #7B (Slide 28): SIKLUS BELAJAR UTUH (FORWARD -> LOSS -> BACKPROP+GD -> EPOCH)
    // Seamless continuation of Slide 27 Untrained Olaf (P=11.3%, Loss=2.18) -> Trained Olaf (P=79.2%, Loss=0.23)!
    // =========================================================================
    let trStage = 1; // 1: Forward Pass, 2: Hitung Loss, 3: Backprop+GD, 4: Epoch Loop
    let trTimer = null;

    function _trSetPlayBtn(running) {{
      const btn = document.getElementById('tr-btn-play');
      if (!btn) return;
      btn.textContent = running ? '■ Stop' : '▶ Play';
      btn.style.background = running ? '#EA4335' : '#34A853';
      btn.style.borderColor = running ? '#EA4335' : '#34A853';
    }}

    function _stopTrCycle() {{
      if (trTimer !== null) {{ clearInterval(trTimer); trTimer = null; }}
      _trSetPlayBtn(false);
    }}

    function setTrStage(st) {{
      _stopTrCycle();
      trStage = st;
      renderTrCycle();
    }}

    function setTrPdfState(st) {{
      _stopTrCycle();
      trStage = parseInt(st, 10) || 1;
      renderTrCycle();
    }}

    function stepTrCycle() {{
      _stopTrCycle();
      trStage = (trStage % 4) + 1;
      renderTrCycle();
    }}

    function resetTrCycle() {{
      _stopTrCycle();
      trStage = 1;
      renderTrCycle();
    }}

    function playTrCycle() {{
      if (trTimer !== null) {{
        _stopTrCycle();
        return;
      }}
      _stopTrCycle();
      _trSetPlayBtn(true);
      trStage = 1;
      renderTrCycle();
      trTimer = setInterval(() => {{
        if (trStage >= 4) {{
          _stopTrCycle();
          return;
        }}
        trStage += 1;
        renderTrCycle();
      }}, 2600);
    }}

    function renderTrCycle() {{
      const svg = document.getElementById('tr-cycle-svg');
      if (!svg) return;
      document.querySelectorAll('#tr-cycle-tabs button[data-trst]').forEach((b) => {{
        b.classList.toggle('outline', parseInt(b.dataset.trst, 10) !== trStage);
      }});

      const st = trStage;
      const trCardIdx = st <= 2 ? 0 : (st === 3 ? 1 : 2);
      _syncCards(['tr-card-1', 'tr-card-2', 'tr-card-3'], trCardIdx, ['blue', 'yellow', 'green']);
      const box = (id, x, y, w, h, fill, stroke, numCol, title, l1, l2, active) => {{
        const sw = active ? '2.6' : '1.4';
        const op = active ? '1' : '0.62';
        let g = `<g opacity="${{op}}">`;
        if (active) g += `<rect x="${{x - 3}}" y="${{y - 3}}" width="${{w + 6}}" height="${{h + 6}}" rx="13" fill="none" stroke="${{stroke}}" stroke-width="1.5" stroke-dasharray="4,3"/>`;
        g += `<rect x="${{x}}" y="${{y}}" width="${{w}}" height="${{h}}" rx="11" fill="${{fill}}" stroke="${{stroke}}" stroke-width="${{sw}}"/>`;
        g += `<circle cx="${{x + 17}}" cy="${{y + 17}}" r="9.5" fill="${{stroke}}"/>`;
        g += `<text x="${{x + 17}}" y="${{y + 20.5}}" text-anchor="middle" font-family="Poppins, Arial" font-size="9.5" font-weight="800" fill="${{numCol}}">${{id}}</text>`;
        g += `<text x="${{x + 32}}" y="${{y + 20.5}}" font-family="Poppins, Arial" font-size="9.6" font-weight="800" fill="#202124">${{title}}</text>`;
        g += `<text x="${{x + 12}}" y="${{y + 40}}" font-family="Roboto, Arial" font-size="8.2" fill="#3C4043">${{l1}}</text>`;
        g += `<text x="${{x + 12}}" y="${{y + 54}}" font-family="Roboto Mono, monospace" font-size="8.1" font-weight="700" fill="#202124">${{l2}}</text>`;
        g += `</g>`;
        return g;
      }};

      let h = '';
      // 4 Cycle Nodes in a crisp, full-height 2x2 clockwise loop! (viewBox 600x316)
      h += box('1', 10, 10, 254, 72, '#E8F0FE', '#4285F4', '#FFFFFF', 'FORWARD PASS (Maju)',
        'Foto Olaf → Weight+Bias → Softmax', 'Epoch 1: P(Olaf) = 11.3% (Tebak Kristoff)', st === 1);
      h += box('2', 336, 10, 254, 72, '#FCE8E6', '#EA4335', '#FFFFFF', 'HITUNG LOSS (Ukur Salah)',
        'Bandingkan prediksi vs Label Asli (100%)', 'Error = 88.7%  |  Loss = 2.18 (Tinggi!)', st === 2);
      h += box('3', 336, 114, 254, 72, '#FEF7E0', '#FBBC04', '#202124', 'BACKPROP + GRADIENT DESCENT',
        'Lacak mundur &amp; geser w, b sebesar LR', 'w_baru = w_lama − LR × gradien', st === 3);
      h += box('4', 10, 114, 254, 72, '#E6F4EA', '#34A853', '#FFFFFF', 'ULANGI TIAP EPOCH',
        'Baca ulang seluruh foto Frozen (Ep 1→8)', 'Loss 2.18 → 0.23  |  P(Olaf) → 79.2% ✅', st === 4);

      // Clockwise Connecting Arrows between the 4 nodes
      const a12 = st === 1 || st === 2 ? '#4285F4' : '#BDC1C6';
      h += `<line x1="266" y1="46" x2="326" y2="46" stroke="${{a12}}" stroke-width="2.8"/><polygon points="324,40.5 334,46 324,51.5" fill="${{a12}}"/>`;
      const a23 = st === 2 || st === 3 ? '#EA4335' : '#BDC1C6';
      h += `<line x1="463" y1="84" x2="463" y2="104" stroke="${{a23}}" stroke-width="2.8"/><polygon points="457.5,102 463,112 468.5,102" fill="${{a23}}"/>`;
      const a34 = st === 3 || st === 4 ? '#FBBC04' : '#BDC1C6';
      h += `<line x1="334" y1="150" x2="274" y2="150" stroke="${{a34}}" stroke-width="2.8"/><polygon points="276,144.5 266,150 276,155.5" fill="${{a34}}"/>`;
      const a41 = st === 4 ? '#34A853' : '#BDC1C6';
      h += `<line x1="137" y1="112" x2="137" y2="92" stroke="${{a41}}" stroke-width="2.8" stroke-dasharray="4,2"/><polygon points="131.5,94 137,84 142.5,94" fill="${{a41}}"/>`;
      h += `<text x="148" y="102" font-family="Poppins, Arial" font-size="8.0" font-weight="700" fill="${{st === 4 ? '#137333' : '#5F6368'}}">Ulangi Epoch berikutnya!</text>`;

      // Richer Full-Width Bottom Panel: Real Loss Curve Drop (2.18 -> 0.23) across Epoch 1..8!
      h += `<rect x="10" y="200" width="580" height="106" rx="11" fill="#F8F9FA" stroke="#DADCE0" stroke-width="1.4"/>`;
      h += `<text x="24" y="220" font-family="Poppins, Arial" font-size="9.2" font-weight="700" fill="#202124">Dampak Siklus Belajar (Foto Olaf · Tahap 4.3):</text>`;
      h += `<text x="24" y="241" font-family="Roboto, Arial" font-size="8.5" fill="#C5221F">● Epoch 1 (Acak): Loss = 2.18 · P(Olaf) = 11.3% ❌</text>`;
      h += `<text x="24" y="261" font-family="Roboto, Arial" font-size="8.5" fill="#1A73E8">● Epoch 4 (Belajar): Loss = 0.85 · Mulai tepat</text>`;
      h += `<text x="24" y="281" font-family="Roboto, Arial" font-size="8.5" font-weight="700" fill="#137333">● Epoch 8 (Terlatih): Loss = 0.23 · P(Olaf) = 79.2% ✅</text>`;
      h += `<text x="24" y="297" font-family="Roboto, Arial" font-size="7.6" fill="#5F6368">Di Keras, cukup 1 baris: model.fit(epochs=8)</text>`;

      // Crisp Loss-vs-Epoch Chart on right half (x=318..578, y=210..294)
      const lossPts = [2.18, 1.72, 1.24, 0.85, 0.58, 0.41, 0.30, 0.23];
      const gx0 = 336, gx1 = 568, gy0 = 216, gy1 = 278;
      const showN = st === 1 || st === 2 ? 1 : (st === 3 ? 4 : 8);
      h += `<rect x="312" y="208" width="268" height="90" rx="8" fill="#FFFFFF" stroke="#E0E3E7" stroke-width="1.1"/>`;
      // Subtle horizontal guide lines
      for (const gl of [2.0, 1.2, 0.4]) {{
        const gy = gy1 - ((gl - 0.1) / 2.25) * (gy1 - gy0);
        h += `<line x1="${{gx0 - 4}}" y1="${{gy.toFixed(1)}}" x2="${{gx1 + 4}}" y2="${{gy.toFixed(1)}}" stroke="#F1F3F4" stroke-width="1"/>`;
        h += `<text x="${{gx0 - 7}}" y="${{(gy + 2.5).toFixed(1)}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="6.4" fill="#9AA0A6">${{gl.toFixed(1)}}</text>`;
      }}
      let poly = [];
      for (let i = 0; i < showN; i++) {{
        const px = gx0 + (i / 7) * (gx1 - gx0);
        const py = gy1 - ((lossPts[i] - 0.1) / 2.25) * (gy1 - gy0);
        poly.push(`${{px.toFixed(1)}},${{py.toFixed(1)}}`);
      }}
      if (poly.length > 1) {{
        h += `<polyline points="${{poly.join(' ')}}" fill="none" stroke="#34A853" stroke-width="2.6" stroke-linecap="round"/>`;
      }}
      for (let i = 0; i < showN; i++) {{
        const px = gx0 + (i / 7) * (gx1 - gx0);
        const py = gy1 - ((lossPts[i] - 0.1) / 2.25) * (gy1 - gy0);
        const isLast = i === showN - 1;
        const col = i === 0 ? '#EA4335' : (isLast && st === 4 ? '#34A853' : '#4285F4');
        h += `<circle cx="${{px.toFixed(1)}}" cy="${{py.toFixed(1)}}" r="${{isLast ? '4.8' : '3.2'}}" fill="${{col}}" stroke="#FFFFFF" stroke-width="1.3"/>`;
        if (i === 0 || isLast) {{
          const lblY = i === 0 ? py + 13 : (py > gy1 - 15 ? py - 9 : py + 13);
          h += `<text x="${{px.toFixed(1)}}" y="${{lblY.toFixed(1)}}" text-anchor="${{i === 0 ? 'start' : 'end'}}" font-family="Roboto Mono, monospace" font-size="7.6" font-weight="700" fill="${{col}}">${{lossPts[i].toFixed(2)}}</text>`;
        }}
      }}
      for (let e = 1; e <= 8; e++) {{
        const ex = gx0 + ((e - 1) / 7) * (gx1 - gx0);
        h += `<text x="${{ex.toFixed(1)}}" y="292" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.8" fill="#5F6368">E${{e}}</text>`;
      }}

      svg.innerHTML = h;

      const cl = document.getElementById('tr-cycle-callout');
      if (cl) {{
        if (st === 1) {{
          cl.className = 'callout';
          cl.innerHTML = '<strong>Langkah 1/4 · Forward Pass:</strong> Foto Olaf melewati alur Tahap 4.1–4.3. Karena bobot masih acak (Epoch 1), peluang Olaf baru <code>11.3%</code> dan model salah menebak Kristoff!';
        }} else if (st === 2) {{
          cl.className = 'callout red';
          cl.innerHTML = '<strong>Langkah 2/4 · Hitung Loss:</strong> Bandingkan tebakan <code>11.3%</code> dengan target <code>100%</code> → dihasilkan <strong>Loss = <code>2.18</code></strong> (skor kesalahan besar, persis Tahap 4.3)!';
        }} else if (st === 3) {{
          cl.className = 'callout yellow';
          cl.innerHTML = '<strong>Langkah 3/4 · Backpropagation &amp; Gradient Descent:</strong> Sistem melacak mundur kabel <code>w</code> &amp; <code>b</code> penyebab salah, lalu menggesernya sebesar <em>Learning Rate</em> agar <strong>Loss turun</strong>!';
        }} else {{
          cl.className = 'callout green';
          cl.innerHTML = '<strong>Langkah 4/4 · Epoch (<code>model.fit()</code>):</strong> Siklus 1→2→3 diulang tiap <strong>Epoch</strong>. Di Epoch 8, <strong>Loss turun <code>2.18 → 0.23</code></strong> dan prediksi Olaf naik ke <strong><code>79.2% ✅</code></strong> — siap praktik di Hands-On!';
        }}
      }}
    }}
    renderTrCycle();

    // =========================================================================
    // ULTIMATE SLIDE 29: SIMULASI FULL NEURAL NETWORK END-TO-END (TAHAP 1 -> 5!)
    // Model 1-Layer nyata (150.528 Input -> 5 Output Softmax = 752.645 param, ZERO Hidden Layer!)
    // + Mode "Full 8 Epoch" menjalankan semua 5 karakter bergantian dari E1 -> E8!
    // =========================================================================
    let fnnPhotoIdx = 3;      // Default: Olaf
    let fnnEpochIdx = 7;      // Default: Epoch 8 (index 7) — trained 5/5!
    let fnnStage = 0;         // 0 = overview, 1..5 = active stage highlight
    let fnnMode = 'idle';     // 'idle' | 'single' | 'full'
    let fnnFullPhase = 0;     // In 'full' mode: 0 = forward wave (T1..T4), 1 = red Backprop (T5)
    let fnnFullDone = false;  // Banner after finishing Full 8-Epoch tour
    let fnnProg = 0;
    let fnnRaf = null;
    let fnnLastTs = 0;
    let fnnCache = null;
    const fnnPlayEpochs = [0, 2, 4, 7]; // Key epochs for slow single-photo tour (E1 -> E3 -> E5 -> E8)
    let fnnPlayEpPos = 0;

    function _fnnSetBtns() {{
      const bFull = document.getElementById('fnn-btn-full');
      const bPlay = document.getElementById('fnn-btn-play');
      if (bFull) {{
        const isFull = fnnMode === 'full';
        bFull.textContent = isFull ? '■ Stop Full' : '▶ Full 8 Epoch';
        bFull.style.background = isFull ? '#EA4335' : '#1A73E8';
        bFull.style.borderColor = isFull ? '#EA4335' : '#1A73E8';
      }}
      if (bPlay) {{
        const isSingle = fnnMode === 'single';
        bPlay.textContent = isSingle ? '■ Stop' : '▶ 1 Foto';
        bPlay.style.background = isSingle ? '#EA4335' : '#34A853';
        bPlay.style.borderColor = isSingle ? '#EA4335' : '#34A853';
      }}
    }}

    function _fnnClearCanvas() {{
      const c = document.getElementById('fnn-motion-canvas');
      if (!c) return;
      const ctx = c.getContext('2d');
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, c.width, c.height);
    }}

    function _stopFnnAnim() {{
      if (fnnRaf !== null) {{ cancelAnimationFrame(fnnRaf); fnnRaf = null; }}
      fnnMode = 'idle';
      _fnnSetBtns();
    }}

    function _fnnBuildCharBar() {{
      const host = document.getElementById('fnn-char-bar');
      if (!host) return;
      const epObj = FULL_NN_DATA.epochs[fnnEpochIdx];
      if (host.children.length === 0) {{
        host.innerHTML = FULL_NN_DATA.classes.map((cls, idx) => `
          <button id="fnn-ch-${{idx}}" class="fnn-char-btn${{idx === fnnPhotoIdx ? ' active' : ''}}" onclick="selectFnnChar(${{idx}})" title="Uji foto nyata ${{cls}} di Full Neural Network!">
            <img src="${{FULL_NN_DATA.thumbs[idx]}}" alt="${{cls}}" style="border-color:${{TM_OUT_COLS[idx]}};"/>
            <span>${{cls}}</span>
            <span id="fnn-ch-dot-${{idx}}" class="fnn-char-dot"></span>
          </button>
        `).join('');
      }}
      for (let i = 0; i < 5; i++) {{
        const btn = document.getElementById(`fnn-ch-${{i}}`);
        if (btn) btn.classList.toggle('active', i === fnnPhotoIdx);
        const dot = document.getElementById(`fnn-ch-dot-${{i}}`);
        if (dot) {{
          const row = epObj.photos[i];
          const pT = row.probs[i];
          dot.style.background = !row.ok ? '#EA4335' : (pT >= 60 ? '#34A853' : '#FBBC04');
          dot.title = `${{FULL_NN_DATA.classes[i]}}: ${{pT.toFixed(1)}}% (${{row.ok ? (pT >= 60 ? 'Yakin' : 'Benar/Ragu') : 'Salah'}})`;
        }}
      }}
    }}

    function _fnnRenderSvg() {{
      _fnnBuildCharBar();
      const svg = document.getElementById('fnn-svg');
      if (!svg) return;

      const epObj = FULL_NN_DATA.epochs[fnnEpochIdx];
      const ph = epObj.photos[fnnPhotoIdx];
      const epNum = epObj.epoch;
      const clsName = FULL_NN_DATA.classes[fnnPhotoIdx];
      const cNames = FULL_NN_DATA.classes;
      const xSamp = FULL_NN_DATA.X_sample[fnnPhotoIdx];
      const isCorrect = ph.ok;
      const winPct = ph.probs[ph.pred];
      const isConf = isCorrect && winPct >= 60;
      const st = fnnStage; // 0 = overview, 1..5 = active stage highlight
      const isBackprop = st === 5;
      const isFullRunning = fnnMode === 'full';

      // Sync Epoch slider & top pill (shows Epoch, Acc/5, Mean Loss!)
      const sl = document.getElementById('fnn-ep-slider');
      if (sl) sl.value = String(epNum);
      const pill = document.getElementById('fnn-ep-pill');
      if (pill) {{
        pill.textContent = `E${{epNum}}/8 · ${{epObj.acc}}/5 · ${{epObj.avg_loss.toFixed(2)}}`;
        pill.style.color = epObj.acc < 3 ? '#C5221F' : (epObj.acc === 5 && epObj.avg_loss < 0.36 ? '#137333' : '#B06000');
      }}

      // Sync 5 bottom stage cards (.sync-card choreography!)
      _syncCards(
        ['fnn-card-1', 'fnn-card-2', 'fnn-card-3', 'fnn-card-4', 'fnn-card-5'],
        st >= 1 && st <= 5 ? st - 1 : -1,
        ['blue', 'blue', 'yellow', 'green', 'red']
      );

      // Layout geometry (viewBox="0 0 1050 284")
      const inY = [66, 92, 118, 150, 182, 208, 234]; // 3 top RGB + ellipsis + 3 bottom RGB
      const inCols = ['#EA4335', '#34A853', '#4285F4', '#1A73E8', '#EA4335', '#34A853', '#4285F4'];
      const inIds = ['x1', 'x2', 'x3', '', 'x150.526', 'x150.527', 'x150.528'];
      const inSubs = ['(R)', '(G)', '(B)', '', '(R)', '(G)', '(B)'];
      const inMap = [0, 1, 2, null, 3, 4, 5];

      const rowY = [82, 112, 142, 172, 202]; // Shared crisp alignment for Col 3 (z1..z5) & Col 4 (y1..y5)

      const colStroke = (colStage, baseCol) => (st === colStage ? baseCol : (st === 0 ? baseCol : '#DADCE0'));
      const colSw = (colStage) => (st === colStage ? '2.8' : '1.7');
      const colOp = (colStage) => (st === 0 || st === colStage || (colStage === 2 && st === 1) ? '1' : '0.78');

      let h = '';
      // Top Backpropagation return arc (Col 5 -> W, b at x=347) — lights up vivid RED during Tahap 5!
      const bpArcCol = isBackprop ? '#EA4335' : '#E0E3E7';
      const bpArcSw = isBackprop ? '2.8' : '1.4';
      const bpArcOp = isBackprop ? '1' : '0.72';
      h += `<path id="fnn-bp-arc" d="M 946 22 C 946 4, 347 4, 347 22" fill="none" stroke="${{bpArcCol}}" stroke-width="${{bpArcSw}}" stroke-dasharray="6,4" opacity="${{bpArcOp}}"/>`;
      h += `<polygon points="342,20 352,20 347,29" fill="${{bpArcCol}}" opacity="${{bpArcOp}}"/>`;
      h += `<rect x="498" y="1" width="292" height="16" rx="8" fill="${{isBackprop ? '#FCE8E6' : '#F8F9FA'}}" stroke="${{isBackprop ? '#EA4335' : '#DADCE0'}}" stroke-width="1.3"/>`;
      h += `<text x="644" y="11.8" text-anchor="middle" font-family="Poppins, Arial" font-size="7.7" font-weight="800" fill="${{isBackprop ? '#C5221F' : '#5F6368'}}">↩ BACKPROPAGATION + GRADIENT DESCENT (Koreksi W &amp; b)</text>`;

      // =========================================================================
      // COL 1: TAHAP 1 · FOTO & PIKSEL (x=4..128, y=28..278)
      // =========================================================================
      h += `<g opacity="${{colOp(1)}}">`;
      h += `<rect id="fnn-col-1" x="4" y="28" width="124" height="250" rx="13" fill="#F8F9FA" stroke="${{colStroke(1, '#4285F4')}}" stroke-width="${{colSw(1)}}"/>`;
      h += `<rect x="18" y="36" width="96" height="16" rx="8" fill="#E8F0FE"/><text x="66" y="47" text-anchor="middle" font-family="Poppins, Arial" font-size="7.6" font-weight="800" fill="#1A73E8">LANGKAH 1 · PIKSEL</text>`;
      h += `<text x="66" y="65" text-anchor="middle" font-family="Poppins, Arial" font-size="9.6" font-weight="700" fill="#202124">Foto ${{clsName}}</text>`;
      h += `<defs><clipPath id="fnn-ph-clip"><rect x="20" y="74" width="92" height="92" rx="10"/></clipPath></defs>`;
      h += `<image id="fnn-photo-el" href="${{FULL_NN_DATA.thumbs[fnnPhotoIdx]}}" x="20" y="74" width="92" height="92" preserveAspectRatio="xMidYMid slice" clip-path="url(#fnn-ph-clip)"/>`;
      for (let g = 1; g < 4; g++) {{
        h += `<line x1="${{20 + g * 23}}" y1="74" x2="${{20 + g * 23}}" y2="166" stroke="rgba(255,255,255,0.45)" stroke-width="0.9"/>`;
        h += `<line x1="20" y1="${{74 + g * 23}}" x2="112" y2="${{74 + g * 23}}" stroke="rgba(255,255,255,0.45)" stroke-width="0.9"/>`;
      }}
      h += `<rect x="20" y="74" width="92" height="92" rx="10" fill="none" stroke="${{TM_OUT_COLS[fnnPhotoIdx]}}" stroke-width="2.4"/>`;
      if (isFullRunning) {{
        h += `<rect x="24" y="78" width="84" height="14" rx="5" fill="rgba(26,115,232,0.92)"/>`;
        h += `<text x="66" y="87.8" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.1" font-weight="800" fill="#FFFFFF">E${{epNum}}/8 · Foto ${{fnnPhotoIdx + 1}}/5</text>`;
      }}
      h += `<rect x="22" y="176" width="88" height="18" rx="6" fill="#E8F0FE" stroke="#C6DAFC" stroke-width="1"/><text x="66" y="188" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="700" fill="#1A73E8">224 × 224 × 3</text>`;
      h += `<text x="66" y="210" text-anchor="middle" font-family="Roboto, Arial" font-size="7.8" fill="#5F6368">Nilai piksel 0.0 – 1.0</text>`;
      h += `<rect x="14" y="222" width="104" height="44" rx="8" fill="#FFFFFF" stroke="#DADCE0" stroke-width="1.2"/>`;
      h += `<text x="66" y="237" text-anchor="middle" font-family="Roboto, Arial" font-size="7.4" fill="#5F6368">Label Asli (Ground Truth)</text>`;
      h += `<text x="66" y="254" text-anchor="middle" font-family="Poppins, Arial" font-size="9.6" font-weight="800" fill="#202124">${{clsName}} (y${{fnnPhotoIdx + 1}}=1)</text>`;
      h += `</g>`;

      // Arrow Col 1 -> Col 2 (Flatten)
      const a12Col = st === 1 || st === 2 ? '#4285F4' : '#9AA0A6';
      h += `<text x="141" y="140" text-anchor="middle" font-family="Poppins, Arial" font-size="7.4" font-weight="700" fill="${{a12Col}}">Flatten</text>`;
      h += `<line x1="129" y1="150" x2="147" y2="150" stroke="${{a12Col}}" stroke-width="2.4"/><polygon points="145,145.5 153,150 145,154.5" fill="${{a12Col}}"/>`;

      // =========================================================================
      // COL 2: TAHAP 2 · INPUT LAYER (150.528 NEURON) (x=154..312, y=28..278)
      // =========================================================================
      h += `<g opacity="${{colOp(2)}}">`;
      h += `<rect id="fnn-col-2" x="154" y="28" width="158" height="250" rx="13" fill="#E8F0FE" stroke="${{colStroke(2, '#4285F4')}}" stroke-width="${{colSw(2)}}"/>`;
      h += `<rect x="179" y="36" width="108" height="16" rx="8" fill="#FFFFFF" stroke="#C6DAFC" stroke-width="1"/><text x="233" y="47" text-anchor="middle" font-family="Poppins, Arial" font-size="7.5" font-weight="800" fill="#1A73E8">LANGKAH 2 · INPUT LAYER</text>`;
      for (let i = 0; i < 7; i++) {{
        if (i === 3) {{
          h += `<rect id="fnn-in-3" x="163" y="${{inY[3] - 11.5}}" width="140" height="23" rx="7" fill="#FFFFFF" stroke="#4285F4" stroke-width="1.3" stroke-dasharray="4,2"/>`;
          h += `<text x="233" y="${{inY[3] - 1.2}}" text-anchor="middle" font-family="Poppins, Arial" font-size="7.5" font-weight="700" fill="#1A73E8">⋮ +150.522 neuron</text>`;
          h += `<text x="233" y="${{inY[3] + 7.8}}" text-anchor="middle" font-family="Roboto, Arial" font-size="6.4" fill="#5F6368">Total 150.528 piksel</text>`;
        }} else {{
          const m = inMap[i];
          const isEnd = m >= 3;
          h += `<circle id="fnn-in-${{i}}" cx="174" cy="${{inY[i]}}" r="9.4" fill="${{inCols[i]}}" stroke="#FFFFFF" stroke-width="1.5"/>`;
          h += `<text x="174" y="${{inY[i] + 2.8}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.7" font-weight="700" fill="#FFFFFF">${{xSamp[m].toFixed(2)}}</text>`;
          h += `<text x="188" y="${{inY[i] + 3.0}}" font-family="Roboto Mono, monospace" font-size="${{isEnd ? '7.5' : '8.4'}}" font-weight="700" fill="#202124">${{inIds[i]}}</text>`;
          h += `<text x="${{isEnd ? 240 : 210}}" y="${{inY[i] + 3.0}}" font-family="Roboto, Arial" font-size="7.6" fill="#5F6368">${{inSubs[i]}}</text>`;
        }}
      }}
      h += `<rect x="168" y="252" width="130" height="18" rx="6" fill="#FFFFFF" stroke="#C6DAFC" stroke-width="1"/>`;
      h += `<text x="233" y="264" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.6" font-weight="700" fill="#1A73E8">150.528 Neuron (RGB)</text>`;
      h += `</g>`;

      // =========================================================================
      // WIRES W, b (Input Layer 150.528 -> Weight + Bias 5 Skor, x=312..382)
      // =========================================================================
      const wBaseCol = isBackprop ? '#EA4335' : (st === 3 ? '#FBBC04' : '#CBD5E1');
      const wOp = isBackprop ? '0.82' : (st === 3 ? '0.90' : '0.58');
      for (let i = 0; i < 7; i++) {{
        for (let j = 0; j < 5; j++) {{
          const isTgt = j === fnnPhotoIdx;
          const lw = (i === 3 && isTgt) ? (isBackprop ? 2.6 : 2.3) : (isTgt ? 1.15 : 0.85);
          const strokeC = isBackprop && isTgt
            ? '#EA4335'
            : ((i === 3 && isTgt && !isBackprop) ? (ph.z[j] >= 0 ? '#34A853' : '#EA4335') : wBaseCol);
          h += `<line x1="312" y1="${{inY[i]}}" x2="382" y2="${{rowY[j]}}" stroke="${{strokeC}}" stroke-width="${{lw}}" opacity="${{wOp}}"/>`;
        }}
      }}
      // W, b Parameter Pill (752.645 param — 100% consistent with Bab 3 & TODO 2!)
      h += `<rect x="315" y="30" width="64" height="30" rx="7" fill="${{isBackprop ? '#FCE8E6' : '#FEF7E0'}}" stroke="${{isBackprop ? '#EA4335' : '#FBBC04'}}" stroke-width="1.5"/>`;
      h += `<text x="347" y="42.5" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.0" font-weight="800" fill="${{isBackprop ? '#C5221F' : '#B06000'}}">${{isBackprop ? '← ΔW, b' : 'W, b'}}</text>`;
      h += `<text x="347" y="54" text-anchor="middle" font-family="Roboto, Arial" font-size="6.8" font-weight="700" fill="#5F6368">752.645 param</text>`;

      // =========================================================================
      // COL 3: TAHAP 3 · WEIGHT + BIAS (z = Σ(x·w) + b, 5 SKOR MENTAH — TANPA HIDDEN!)
      // (x=382..578, y=28..278)
      // =========================================================================
      h += `<g opacity="${{colOp(3)}}">`;
      h += `<rect id="fnn-col-3" x="382" y="28" width="196" height="250" rx="13" fill="#FEF7E0" stroke="${{colStroke(3, '#FBBC04')}}" stroke-width="${{colSw(3)}}"/>`;
      h += `<rect x="404" y="36" width="152" height="16" rx="8" fill="#FFFFFF" stroke="#FDE293" stroke-width="1"/><text x="480" y="47" text-anchor="middle" font-family="Poppins, Arial" font-size="7.4" font-weight="800" fill="#B06000">LANGKAH 3 · WEIGHT + BIAS</text>`;
      h += `<text x="480" y="63" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.3" fill="#5F6368">z = Σ(x·w) + b  (5 Skor Mentah)</text>`;

      let maxZIdx = 0;
      for (let j = 1; j < 5; j++) {{ if (ph.z[j] > ph.z[maxZIdx]) maxZIdx = j; }}

      for (let j = 0; j < 5; j++) {{
        const zv = ph.z[j];
        const wxv = ph.wx[j];
        const bv = ph.b[j];
        const isTgt = j === fnnPhotoIdx;
        const isTop = j === maxZIdx;
        const rFill = isTop ? (isTgt ? '#E6F4EA' : '#FCE8E6') : '#FFFFFF';
        const rStr = isTgt ? (isTop ? '#34A853' : '#FBBC04') : (isTop ? '#EA4335' : '#E0E3E7');
        const fmtS = (v) => (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(2);
        h += `<rect x="390" y="${{rowY[j] - 12}}" width="180" height="24" rx="7" fill="${{rFill}}" stroke="${{rStr}}" stroke-width="${{isTgt || isTop ? '1.7' : '1.0'}}"/>`;
        h += `<circle id="fnn-z-${{j}}" cx="403" cy="${{rowY[j]}}" r="8.2" fill="${{TM_OUT_COLS[j]}}"/>`;
        h += `<text x="403" y="${{rowY[j] + 2.8}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.1" font-weight="700" fill="${{j === 2 ? '#202124' : '#FFFFFF'}}">z${{j + 1}}</text>`;
        h += `<text x="415" y="${{rowY[j] + 2.9}}" font-family="Roboto Mono, monospace" font-size="6.8" fill="#5F6368">${{fmtS(wxv)}} ${{bv >= 0 ? '+' : '−'}}${{Math.abs(bv).toFixed(2)}}</text>`;
        h += `<text x="564" y="${{rowY[j] + 3.0}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.0" font-weight="800" fill="${{zv >= 0 ? '#137333' : '#C5221F'}}">=${{fmtS(zv)}}${{isTgt ? '★' : ''}}</text>`;
      }}
      h += `<rect x="390" y="232" width="180" height="36" rx="8" fill="#FFFFFF" stroke="#FDE293" stroke-width="1.3"/>`;
      h += `<text x="480" y="247" text-anchor="middle" font-family="Poppins, Arial" font-size="8.1" font-weight="800" fill="#B06000">Skor Tertinggi: z${{maxZIdx + 1}} = ${{(ph.z[maxZIdx] >= 0 ? '+' : '') + ph.z[maxZIdx].toFixed(2)}}</text>`;
      h += `<text x="480" y="260" text-anchor="middle" font-family="Roboto, Arial" font-size="7.0" fill="#5F6368">(${{cNames[maxZIdx]}}) → diteruskan ke Softmax</text>`;
      h += `</g>`;

      // Arrow Col 3 -> Col 4 (Softmax)
      const a34Col = st === 3 || st === 4 ? '#34A853' : '#9AA0A6';
      h += `<text x="593" y="139" text-anchor="middle" font-family="Poppins, Arial" font-size="7.0" font-weight="800" fill="${{a34Col}}">Softmax</text>`;
      h += `<line x1="579" y1="150" x2="601" y2="150" stroke="${{a34Col}}" stroke-width="2.4"/><polygon points="599,145.5 607,150 599,154.5" fill="${{a34Col}}"/>`;

      // =========================================================================
      // COL 4: TAHAP 4 · OUTPUT LAYER (5 KELAS + SOFTMAX + ARGMAX) (x=608..820)
      // =========================================================================
      h += `<g opacity="${{colOp(4)}}">`;
      h += `<rect id="fnn-col-4" x="608" y="28" width="212" height="250" rx="13" fill="#E6F4EA" stroke="${{colStroke(4, '#34A853')}}" stroke-width="${{colSw(4)}}"/>`;
      h += `<rect x="640" y="36" width="148" height="16" rx="8" fill="#FFFFFF" stroke="#A8DAB5" stroke-width="1"/><text x="714" y="47" text-anchor="middle" font-family="Poppins, Arial" font-size="7.4" font-weight="800" fill="#137333">LANGKAH 4 · OUTPUT (SOFTMAX)</text>`;
      h += `<text x="714" y="63" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.3" fill="#5F6368">e^z / Σe^z (100%) → Argmax</text>`;

      for (let j = 0; j < 5; j++) {{
        const pct = ph.probs[j];
        const isWin = j === ph.pred;
        const isTgt = j === fnnPhotoIdx;
        const rowFill = isWin ? (isCorrect ? '#D4F0DC' : '#FCE8E6') : '#FFFFFF';
        const rowStr = isWin ? (isCorrect ? '#34A853' : '#EA4335') : (isTgt ? '#FBBC04' : '#DADCE0');
        const barW = Math.max(2, Math.round((pct / 100) * 64));
        h += `<rect x="616" y="${{rowY[j] - 12}}" width="196" height="24" rx="7" fill="${{rowFill}}" stroke="${{rowStr}}" stroke-width="${{isWin || isTgt ? '1.8' : '1'}}"/>`;
        h += `<circle id="fnn-out-${{j}}" cx="629" cy="${{rowY[j]}}" r="8.2" fill="${{TM_OUT_COLS[j]}}"/>`;
        h += `<text x="629" y="${{rowY[j] + 2.8}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.3" font-weight="700" fill="${{j === 2 ? '#202124' : '#FFFFFF'}}">y${{j + 1}}</text>`;
        h += `<text x="642" y="${{rowY[j] + 3.0}}" font-family="Poppins, Arial" font-size="8.4" font-weight="700" fill="#202124">${{cNames[j]}}${{isTgt ? ' ★' : ''}}</text>`;
        h += `<rect x="706" y="${{rowY[j] - 3.8}}" width="64" height="7.6" rx="3.8" fill="${{isWin ? '#FFFFFF' : '#F1F3F4'}}"/>`;
        h += `<rect x="706" y="${{rowY[j] - 3.8}}" width="${{barW}}" height="7.6" rx="3.8" fill="${{TM_OUT_COLS[j]}}"/>`;
        h += `<text x="807" y="${{rowY[j] + 3.0}}" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="800" fill="${{isWin ? (isCorrect ? '#137333' : '#C5221F') : '#3C4043'}}">${{pct.toFixed(1)}}%</text>`;
      }}
      // Argmax Verdict Box
      const vBg = !isCorrect ? '#FCE8E6' : (isConf ? '#137333' : '#FEF7E0');
      const vStr = !isCorrect ? '#EA4335' : (isConf ? '#137333' : '#FBBC04');
      const vTxtCol = !isCorrect ? '#C5221F' : (isConf ? '#FFFFFF' : '#B06000');
      const vLbl = !isCorrect
        ? `❌ Argmax: ${{cNames[ph.pred]}} (${{winPct.toFixed(1)}}%)`
        : (isConf ? `✅ YAKIN: ${{clsName.toUpperCase()}} (${{winPct.toFixed(1)}}%)` : `⚠ RAGU: ${{clsName}} (${{winPct.toFixed(1)}}%)`);
      h += `<rect x="616" y="232" width="196" height="36" rx="8" fill="${{vBg}}" stroke="${{vStr}}" stroke-width="1.6"/>`;
      h += `<text x="714" y="247" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="800" fill="${{vTxtCol}}">${{vLbl}}</text>`;
      h += `<text x="714" y="260" text-anchor="middle" font-family="Roboto, Arial" font-size="7.1" font-weight="600" fill="${{isConf ? '#E6F4EA' : '#5F6368'}}">${{!isCorrect ? `Padahal asli: ${{clsName}} (${{ph.probs[fnnPhotoIdx].toFixed(1)}}%)` : (isConf ? 'Lolos ambang yakin ≥ 60%!' : 'Benar, tapi masih di bawah 60%')}}</text>`;
      h += `</g>`;

      // Arrow Col 4 -> Col 5 (Loss)
      const a45Col = st === 4 || st === 5 ? '#EA4335' : '#9AA0A6';
      h += `<line x1="821" y1="150" x2="837" y2="150" stroke="${{a45Col}}" stroke-width="2.4"/><polygon points="835,145.5 843,150 835,154.5" fill="${{a45Col}}"/>`;

      // =========================================================================
      // COL 5: TAHAP 5 · LOSS -> BACKPROP + GD -> FULL 8-EPOCH PROGRESS (x=844..1046)
      // =========================================================================
      const c5Fill = !isCorrect ? '#FCE8E6' : (isConf ? '#E6F4EA' : '#FEF7E0');
      const c5Base = !isCorrect ? '#EA4335' : (isConf ? '#34A853' : '#FBBC04');
      h += `<g opacity="${{colOp(5)}}">`;
      h += `<rect id="fnn-col-5" x="844" y="28" width="202" height="250" rx="13" fill="${{c5Fill}}" stroke="${{colStroke(5, isBackprop ? '#EA4335' : c5Base)}}" stroke-width="${{colSw(5)}}"/>`;
      h += `<rect x="872" y="36" width="146" height="16" rx="8" fill="#FFFFFF" stroke="${{isBackprop ? '#EA4335' : '#DADCE0'}}" stroke-width="1"/><text x="945" y="47" text-anchor="middle" font-family="Poppins, Arial" font-size="7.4" font-weight="800" fill="${{isBackprop ? '#C5221F' : '#202124'}}">LANGKAH 5 · LOSS &amp; EPOCH</text>`;

      // Live Loss & Error Box (compact height 54px so 5-char scoreboard fits cleanly below!)
      const errPct = Math.max(0, 100 - ph.probs[fnnPhotoIdx]);
      h += `<rect x="854" y="56" width="182" height="54" rx="9" fill="#FFFFFF" stroke="${{c5Base}}" stroke-width="1.5"/>`;
      h += `<text x="863" y="70" font-family="Roboto, Arial" font-size="7.4" fill="#5F6368">P(${{clsName}}) / Error:</text>`;
      h += `<text x="1028" y="70" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.0" font-weight="800" fill="${{!isCorrect ? '#C5221F' : (isConf ? '#137333' : '#B06000')}}">${{ph.probs[fnnPhotoIdx].toFixed(1)}}% / ${{errPct.toFixed(1)}}%</text>`;
      h += `<text x="863" y="86" font-family="Roboto, Arial" font-size="7.4" font-weight="700" fill="#202124">Loss ${{clsName}}:</text>`;
      h += `<text x="1028" y="86" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.6" font-weight="800" fill="${{!isCorrect ? '#C5221F' : (isConf ? '#137333' : '#B06000')}}">${{ph.loss.toFixed(2)}}</text>`;
      h += `<text x="863" y="102" font-family="Roboto, Arial" font-size="7.3" font-weight="700" fill="#1A73E8">Mean Loss (5 Foto):</text>`;
      h += `<text x="1028" y="102" text-anchor="end" font-family="Roboto Mono, monospace" font-size="8.6" font-weight="800" fill="#1A73E8">${{epObj.avg_loss.toFixed(2)}}</text>`;

      // Live Mean-Loss-vs-Epoch Sparkline (ALL 5 characters across E1 -> E8!)
      h += `<rect x="854" y="116" width="182" height="90" rx="9" fill="#FFFFFF" stroke="#DADCE0" stroke-width="1.2"/>`;
      h += `<text x="945" y="129" text-anchor="middle" font-family="Poppins, Arial" font-size="7.3" font-weight="700" fill="#202124">Kurva Mean Loss 5 Foto (E1 → E8)</text>`;
      const lx0 = 874, lx1 = 1022, ly0 = 138, ly1 = 188;
      const meanLosses = FULL_NN_DATA.epochs.map((e) => e.avg_loss);
      const maxL = Math.max(1.9, Math.ceil(meanLosses[0] * 10) / 10 + 0.15);
      for (const frac of [0.25, 0.6, 0.95]) {{
        const gy = ly1 - frac * (ly1 - ly0);
        h += `<line x1="${{lx0}}" y1="${{gy.toFixed(1)}}" x2="${{lx1}}" y2="${{gy.toFixed(1)}}" stroke="#F1F3F4" stroke-width="1"/>`;
      }}
      let ptsAll = [];
      let ptsCur = [];
      for (let e = 0; e < 8; e++) {{
        const px = lx0 + (e / 7) * (lx1 - lx0);
        const py = ly1 - (Math.min(maxL, meanLosses[e]) / maxL) * (ly1 - ly0);
        ptsAll.push(`${{px.toFixed(1)}},${{py.toFixed(1)}}`);
        if (e <= fnnEpochIdx) ptsCur.push({{ x: px, y: py, v: meanLosses[e], e }});
      }}
      h += `<polyline points="${{ptsAll.join(' ')}}" fill="none" stroke="#E0E3E7" stroke-width="1.6" stroke-dasharray="3,2"/>`;
      if (ptsCur.length > 1) {{
        h += `<polyline points="${{ptsCur.map((pt) => `${{pt.x.toFixed(1)}},${{pt.y.toFixed(1)}}`).join(' ')}}" fill="none" stroke="#34A853" stroke-width="2.6" stroke-linecap="round"/>`;
      }}
      ptsCur.forEach((pt, idxP) => {{
        const isNow = idxP === ptsCur.length - 1;
        const dc = idxP === 0 ? '#EA4335' : (isNow && epObj.acc === 5 && epObj.avg_loss < 0.36 ? '#34A853' : '#4285F4');
        h += `<circle cx="${{pt.x.toFixed(1)}}" cy="${{pt.y.toFixed(1)}}" r="${{isNow ? '4.5' : '2.6'}}" fill="${{dc}}" stroke="#FFFFFF" stroke-width="1.2"/>`;
        if (isNow) {{
          const lxTxt = idxP === 0 ? pt.x + 2 : (idxP === 7 ? pt.x - 1 : pt.x + 6);
          const lyTxt = pt.y < ly0 + 13 ? pt.y + 12 : pt.y - 7;
          const anch = idxP === 7 ? 'end' : 'start';
          h += `<text x="${{lxTxt.toFixed(1)}}" y="${{lyTxt.toFixed(1)}}" text-anchor="${{anch}}" font-family="Roboto Mono, monospace" font-size="7.4" font-weight="800" fill="${{dc}}">${{pt.v.toFixed(2)}}</text>`;
        }}
      }});
      for (let e = 1; e <= 8; e++) {{
        const ex = lx0 + ((e - 1) / 7) * (lx1 - lx0);
        h += `<text x="${{ex.toFixed(1)}}" y="200" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="6.3" font-weight="${{e === epNum ? '800' : '500'}}" fill="${{e === epNum ? '#1A73E8' : '#70757A'}}">E${{e}}</text>`;
      }}

      // 5-Character Live Scoreboard Row (A E K O S) — lights up green one by one across Epochs!
      const initials = ['A', 'E', 'K', 'O', 'S'];
      for (let c = 0; c < 5; c++) {{
        const bx = 854 + c * 37;
        const rC = epObj.photos[c];
        const pC = rC.probs[c];
        const isActiveCh = c === fnnPhotoIdx;
        const cBg = !rC.ok ? '#FCE8E6' : (pC >= 60 ? '#E6F4EA' : '#FEF7E0');
        const cTxt = !rC.ok ? '#C5221F' : (pC >= 60 ? '#137333' : '#B06000');
        const cStr = isActiveCh ? '#1A73E8' : (!rC.ok ? '#F6AEA9' : (pC >= 60 ? '#A8DAB5' : '#FDE293'));
        const sym = !rC.ok ? '✕' : '✓';
        h += `<rect x="${{bx}}" y="212" width="33" height="20" rx="6" fill="${{cBg}}" stroke="${{cStr}}" stroke-width="${{isActiveCh ? '2.0' : '1.1'}}"/>`;
        h += `<text x="${{bx + 16.5}}" y="225" text-anchor="middle" font-family="Poppins, Arial" font-size="7.6" font-weight="800" fill="${{cTxt}}">${{initials[c]}} ${{sym}}</text>`;
      }}

      // Bottom Epoch Progress Pill
      const fbFill = isBackprop ? '#EA4335' : (epNum === 8 && epObj.acc === 5 ? '#34A853' : '#1A73E8');
      const fbTxt = isBackprop
        ? `↩ Backprop E${{epNum}} · Update W & b!`
        : (isFullRunning
            ? `Epoch ${{epNum}}/8 · Foto ${{fnnPhotoIdx + 1}}/5 (${{clsName}})`
            : (epNum === 8 ? `✅ Epoch 8 · 5/5 Kelas Tepat!` : `Epoch ${{epNum}}/8 · Akurasi ${{epObj.acc}}/5`));
      h += `<rect x="854" y="238" width="182" height="32" rx="8" fill="${{fbFill}}"/>`;
      h += `<text x="945" y="257.5" text-anchor="middle" font-family="Poppins, Arial" font-size="7.8" font-weight="800" fill="#FFFFFF">${{fbTxt}}</text>`;
      h += `</g>`;

      svg.innerHTML = h;

      // Live bottom narration line
      const nEl = document.getElementById('fnn-narr-txt');
      if (nEl) {{
        const fullPrefix = isFullRunning
          ? `<span style="background:#1A73E8; color:#FFF; font-family:var(--font-code); font-size:8.6px; font-weight:700; padding:1px 6px; border-radius:999px; margin-right:5px;">Full E${{epNum}}/8 · Foto ${{fnnPhotoIdx + 1}}/5</span>`
          : '';
        if (fnnFullDone) {{
          nEl.innerHTML = `<strong style="color:#137333;">✅ Simulasi Full 8 Epoch Selesai!</strong> Setelah melewati 5 karakter × 8 Epoch (40 langkah), akurasi naik <strong>0/5 → 5/5 (Yakin ≥ 74%)</strong> &amp; Mean Loss turun <code>1.70 → 0.21</code>!`;
        }} else if (st === 1) {{
          nEl.innerHTML = `${{fullPrefix}}<strong style="color:#1A73E8;">Tahap 1/5 (Foto → Piksel):</strong> Foto nyata <strong>${{clsName}}</strong> (<code>224×224×3</code>) dibaca komputer sebagai matriks angka piksel <code>0.0–1.0</code> dengan label asli <code>y${{fnnPhotoIdx + 1}} = 1</code>.`;
        }} else if (st === 2) {{
          nEl.innerHTML = `${{fullPrefix}}<strong style="color:#1A73E8;">Tahap 2/5 (Flatten → Input Layer):</strong> Seluruh piksel RGB diluruskan menjadi <strong>150.528 neuron Input Layer</strong> (<code>x₁..x₃</code> s.d. <code>x₁₅₀.₅₂₆..x₁₅₀.₅₂₈</code>).`;
        }} else if (st === 3) {{
          nEl.innerHTML = `${{fullPrefix}}<strong style="color:#B06000;">Tahap 3/5 (Weight + Bias):</strong> 150.528 input dikali bobot <code>W</code> + <code>b</code> (<strong>752.645 param</strong>) menghasilkan 5 skor mentah <code>z₁..z₅</code> — skor <strong>${{clsName}}</strong> = <code>${{(ph.z[fnnPhotoIdx] >= 0 ? '+' : '') + ph.z[fnnPhotoIdx].toFixed(2)}}</code>.`;
        }} else if (st === 4) {{
          nEl.innerHTML = `${{fullPrefix}}<strong style="color:#137333;">Tahap 4/5 (Output Softmax + Argmax):</strong> 5 skor mentah diubah <strong>Softmax</strong> menjadi probabilitas total <code>100%</code> → <strong>${{clsName}} ${{ph.probs[fnnPhotoIdx].toFixed(1)}}%</strong> (Argmax: <strong>${{cNames[ph.pred]}} ${{winPct.toFixed(1)}}%</strong> ${{isCorrect ? '✅' : '❌'}}).`;
        }} else if (st === 5) {{
          nEl.innerHTML = `${{fullPrefix}}<strong style="color:#C5221F;">Tahap 5/5 (Loss → Backprop + GD):</strong> <strong>Loss = <code>${{ph.loss.toFixed(2)}}</code></strong> mengirim sinyal koreksi mundur (panah merah) untuk menggeser <code>W &amp; b</code> agar Epoch berikutnya makin akurat!`;
        }} else {{
          nEl.innerHTML = `<strong style="color:#137333;">Siap Simulasi (Epoch ${{epNum}}/8):</strong> Klik <strong style="color:#1A73E8;">▶ Full 8 Epoch</strong> untuk melihat training utuh <strong>5 karakter bergantian (E1→E8)</strong>, atau klik <strong>▶ 1 Foto</strong> / geser slider Epoch!`;
        }}
      }}
    }}

    function _fnnCacheLayout() {{
      const wrap = document.getElementById('fnn-stage-wrap');
      const canvas = document.getElementById('fnn-motion-canvas');
      const svg = document.getElementById('fnn-svg');
      if (!wrap || !canvas || !svg) return null;
      const W = wrap.clientWidth, H = wrap.clientHeight;
      if (W < 10 || H < 10) return null;
      const dpr = Math.min(3, (window.devicePixelRatio || 1) * Math.max(1, window.__STAGE_SCALE__ || 1));
      const cw = Math.round(W * dpr), ch = Math.round(H * dpr);
      if (canvas.width !== cw || canvas.height !== ch) {{ canvas.width = cw; canvas.height = ch; }}
      const hR = wrap.getBoundingClientRect();
      const sR = svg.getBoundingClientRect();
      const sx = W / (hR.width || 1), sy = H / (hR.height || 1);
      const fit = Math.min(sR.width / 1050, sR.height / 284);
      const offX = (sR.left - hR.left + (sR.width - 1050 * fit) / 2) * sx;
      const offY = (sR.top - hR.top + (sR.height - 284 * fit) / 2) * sy;
      const toPt = (vx, vy) => ({{ x: offX + vx * fit * sx, y: offY + vy * fit * sy }});
      fnnCache = {{ canvas, ctx: canvas.getContext('2d'), W, H, dpr, toPt }};
      return fnnCache;
    }}
    window.addEventListener('resize', () => {{ fnnCache = null; }});

    function _fnnDrawOverlay() {{
      const L = fnnCache || _fnnCacheLayout();
      if (!L || fnnStage === 0) {{ _fnnClearCanvas(); return; }}
      const {{ ctx, W, H, dpr, toPt }} = L;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      const t = Math.max(0, Math.min(1, fnnProg));
      const easeIO = (u) => (u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2);
      const e = easeIO(t);
      const rowY = [82, 112, 142, 172, 202];
      const ty = rowY[fnnPhotoIdx];

      const drawOrb = (vx, vy, r, col) => {{
        const pt = toPt(vx, vy);
        ctx.save();
        ctx.beginPath(); ctx.arc(pt.x, pt.y, r + 4, 0, Math.PI * 2);
        ctx.fillStyle = _inHexRgba(col, 0.28); ctx.fill();
        ctx.beginPath(); ctx.arc(pt.x, pt.y, r, 0, Math.PI * 2);
        ctx.fillStyle = col; ctx.fill();
        ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 1.6; ctx.stroke();
        ctx.restore();
      }};

      if (fnnStage === 1) {{
        const p0 = toPt(20, 74 + 86 * e);
        const p1 = toPt(112, 74 + 86 * e + 8);
        ctx.save();
        ctx.fillStyle = 'rgba(251, 188, 4, 0.45)';
        ctx.fillRect(p0.x, p0.y, p1.x - p0.x, Math.max(4, p1.y - p0.y));
        ctx.restore();
        drawOrb(66 + 46 * e, 120, 5.2, '#4285F4');
      }} else if (fnnStage === 2) {{
        const ys = [66, 92, 118, 150, 182, 208, 234];
        const cols = ['#EA4335', '#34A853', '#4285F4', '#1A73E8', '#EA4335', '#34A853', '#4285F4'];
        ys.forEach((yy, idx) => {{
          drawOrb(114 + (174 - 114) * e, 120 + (yy - 120) * e, idx === 3 ? 6.2 : 4.5, cols[idx]);
        }});
      }} else if (fnnStage === 3) {{
        // Orbs flying across W, b wires (x=312 -> x=403)
        const srcYs = [66, 118, 150, 182, 234];
        srcYs.forEach((sy, i) => {{
          drawOrb(312 + (403 - 312) * e, sy + (rowY[i] - sy) * e, i === 2 ? 5.6 : 4.6, '#FBBC04');
        }});
      }} else if (fnnStage === 4) {{
        // Orbs flying across Softmax (x=578 -> x=629)
        rowY.forEach((ry, i) => {{
          drawOrb(578 + (629 - 578) * e, ry, i === fnnPhotoIdx ? 5.8 : 4.2, '#34A853');
        }});
      }} else if (fnnStage === 5) {{
        // BRIGHT RED BACKPROPAGATION PULSES traveling RIGHT -> LEFT along top arc & W, b wires!
        const bx = 946 - (946 - 347) * e;
        const by = 10 - Math.sin(Math.PI * e) * 4;
        drawOrb(bx, by, 6.8, '#EA4335');
        const inYs = [66, 118, 150, 182, 234];
        inYs.forEach((iy) => {{
          drawOrb(382 - (382 - 312) * e, ty + (iy - ty) * e, 5.0, '#EA4335');
        }});
      }}
    }}

    function _tickFnn(ts) {{
      if (!fnnLastTs) fnnLastTs = ts;
      const dt = Math.min(0.033, Math.max(0.001, (ts - fnnLastTs) / 1000));
      fnnLastTs = ts;

      // Identical comfortable 5-stage pace (Tahap 1 -> 2 -> 3 -> 4 -> 5) for BOTH '1 Foto' & 'Full 8 Epoch'!
      const speed = fnnStage === 5 ? 0.55 : 0.72;
      fnnProg += dt * speed;
      if (fnnProg >= 1.0) {{
        fnnProg = 0;
        if (fnnStage < 5) {{
          fnnStage += 1;
          _fnnRenderSvg();
        }} else if (fnnMode === 'full') {{
          // Finished Tahap 5 (Backprop): move smoothly to next character -> next Epoch!
          if (fnnPhotoIdx < 4) {{
            fnnPhotoIdx += 1;
            fnnStage = 1;
            _fnnRenderSvg();
          }} else if (fnnEpochIdx < 7) {{
            fnnPhotoIdx = 0;
            fnnEpochIdx += 1;
            fnnStage = 1;
            _fnnRenderSvg();
          }} else {{
            fnnFullDone = true;
            fnnStage = 0;
            _stopFnnAnim();
            _fnnRenderSvg();
            _fnnClearCanvas();
            return;
          }}
        }} else {{
          // Single-photo mode: advance across key Epochs (E1 -> E3 -> E5 -> E8)
          fnnPlayEpPos += 1;
          if (fnnPlayEpPos >= fnnPlayEpochs.length) {{
            fnnEpochIdx = 7;
            fnnStage = 0;
            _stopFnnAnim();
            _fnnRenderSvg();
            _fnnClearCanvas();
            return;
          }}
          fnnEpochIdx = fnnPlayEpochs[fnnPlayEpPos];
          fnnStage = 1;
          _fnnRenderSvg();
        }}
      }}
      _fnnDrawOverlay();
      fnnRaf = requestAnimationFrame(_tickFnn);
    }}

    function playFnnFull() {{
      if (fnnMode === 'full' && fnnRaf !== null) {{
        _stopFnnAnim();
        _fnnRenderSvg();
        _fnnClearCanvas();
        return;
      }}
      _stopFnnAnim();
      fnnFullDone = false;
      fnnMode = 'full';
      fnnEpochIdx = 0;    // Start from Epoch 1 (0/5 correct, Mean Loss 1.70)
      fnnPhotoIdx = 0;    // Start from Anna -> Elsa -> Kristoff -> Olaf -> Sven!
      fnnFullPhase = 0;
      fnnStage = 1;
      fnnProg = 0;
      fnnLastTs = 0;
      _fnnSetBtns();
      _fnnRenderSvg();
      fnnCache = _fnnCacheLayout();
      _fnnDrawOverlay();
      fnnRaf = requestAnimationFrame(_tickFnn);
    }}

    function playFnnSim() {{
      if (fnnMode === 'single' && fnnRaf !== null) {{
        _stopFnnAnim();
        _fnnRenderSvg();
        _fnnClearCanvas();
        return;
      }}
      _stopFnnAnim();
      fnnFullDone = false;
      fnnMode = 'single';
      fnnPlayEpPos = 0;
      fnnEpochIdx = fnnPlayEpochs[0];
      fnnStage = 1;
      fnnProg = 0;
      fnnLastTs = 0;
      _fnnSetBtns();
      _fnnRenderSvg();
      fnnCache = _fnnCacheLayout();
      _fnnDrawOverlay();
      fnnRaf = requestAnimationFrame(_tickFnn);
    }}

    function stepFnnStage() {{
      _stopFnnAnim();
      fnnFullDone = false;
      if (fnnStage === 0) {{
        fnnStage = 1;
      }} else if (fnnStage < 5) {{
        fnnStage += 1;
      }} else {{
        fnnEpochIdx = (fnnEpochIdx + 1) % 8;
        fnnStage = 1;
      }}
      fnnProg = 0.52;
      _fnnRenderSvg();
      fnnCache = _fnnCacheLayout();
      _fnnDrawOverlay();
    }}

    function jumpFnnStage(st) {{
      _stopFnnAnim();
      fnnFullDone = false;
      fnnStage = fnnStage === st ? 0 : st;
      fnnProg = 0.52;
      _fnnRenderSvg();
      fnnCache = _fnnCacheLayout();
      if (fnnStage > 0) _fnnDrawOverlay();
      else _fnnClearCanvas();
    }}

    function selectFnnChar(idx) {{
      _stopFnnAnim();
      fnnFullDone = false;
      fnnPhotoIdx = idx;
      _fnnRenderSvg();
      fnnCache = _fnnCacheLayout();
      if (fnnStage > 0) _fnnDrawOverlay();
      else _fnnClearCanvas();
    }}

    function onFnnEpochSlide() {{
      _stopFnnAnim();
      fnnFullDone = false;
      const sl = document.getElementById('fnn-ep-slider');
      if (!sl) return;
      fnnEpochIdx = Math.max(0, Math.min(7, (parseInt(sl.value, 10) || 1) - 1));
      _fnnRenderSvg();
      if (fnnStage > 0) _fnnDrawOverlay();
    }}

    function resetFnnSim() {{
      _stopFnnAnim();
      fnnFullDone = false;
      fnnPhotoIdx = 0;
      fnnEpochIdx = 0; // Epoch 1 (Anna, 0/5) ready to press Full 8 Epoch!
      fnnStage = 0;
      fnnProg = 0;
      _fnnRenderSvg();
      _fnnClearCanvas();
    }}

    function setFnnPdfState(mode) {{
      _stopFnnAnim();
      fnnFullDone = false;
      fnnPhotoIdx = 3; // Olaf
      if (mode === 'ep1_bp') {{
        fnnEpochIdx = 0; // Epoch 1 (0/5, Mean Loss 1.70 + Red Backprop active!)
        fnnStage = 5;
        fnnProg = 0.52;
      }} else {{
        fnnEpochIdx = 7; // Epoch 8 (5/5 Yakin, Mean Loss 0.21!)
        fnnStage = 4;
        fnnProg = 0.52;
      }}
      _fnnRenderSvg();
      _fnnClearCanvas();
    }}
    _fnnRenderSvg();

    // =========================================================================
    // SIMULATOR #5 (Slide 25): Telusuri 1 Neuron Input -> 5 Neuron Output
    // =========================================================================
    function setTraceNeuron(activeIdx) {{
      document.querySelectorAll('#trace-btns button').forEach((b) => {{
        b.classList.toggle('outline', parseInt(b.dataset.tr, 10) !== activeIdx);
      }});
      const svg = document.getElementById('trace-svg');
      if (!svg) return;
      // Tall dense Input Layer (8 visible nodes + ellipsis = 150.528) vs compact centered Output Layer (5 nodes)
      const inY = [46, 76, 106, 136, 166, 196, 240, 268];
      const inLbls = ['x₁', 'x₂', 'x₃', 'x₄', 'x₅', 'x₆', 'xₙ₋₁', 'xₙ'];
      const outY = [78, 114, 150, 186, 222];
      const outNames = ['Anna', 'Elsa', 'Kristoff', 'Olaf', 'Sven'];
      let html = '';

      // Subtle layer capsules emphasizing funnel (tall Input vs compact Output)
      html += `<rect x="20" y="24" width="104" height="258" rx="14" fill="#E8F0FE" stroke="#C6DAFC" stroke-width="1.6"/>`;
      html += `<rect x="332" y="54" width="136" height="192" rx="14" fill="#E6F4EA" stroke="#A8DAB5" stroke-width="1.6"/>`;

      // Background dim lines from all non-active input neurons
      for (let i = 0; i < inY.length; i++) {{
        if (i === activeIdx) continue;
        for (let j = 0; j < 5; j++) {{
          html += `<line x1="86" y1="${{inY[i]}}" x2="346" y2="${{outY[j]}}" stroke="#E0E3E7" stroke-width="1.05"/>`;
        }}
      }}
      // Highlighted 5 lines from active input neuron
      for (let j = 0; j < 5; j++) {{
        html += `<line x1="86" y1="${{inY[activeIdx]}}" x2="346" y2="${{outY[j]}}" stroke="#EA4335" stroke-width="2.6"/>`;
        const mx = 225, my = inY[activeIdx] * 0.44 + outY[j] * 0.56;
        html += `<rect x="${{mx - 22}}" y="${{my - 8.5}}" width="44" height="16.5" rx="5" fill="#FCE8E6" stroke="#EA4335" stroke-width="1"/>`;
        html += `<text x="${{mx}}" y="${{my + 3}}" text-anchor="middle" font-family="Roboto Mono" font-size="9.2" font-weight="700" fill="#C5221F">w${{activeIdx + 1}},${{j + 1}}</text>`;
      }}
      // Input nodes (8 visible circles + vertical ellipsis = visibly huge!)
      for (let i = 0; i < inY.length; i++) {{
        const act = i === activeIdx;
        const r = act ? 15.5 : 12.2;
        html += `<circle cx="72" cy="${{inY[i]}}" r="${{r}}" fill="${{act ? '#EA4335' : '#4285F4'}}" stroke="#FFF" stroke-width="${{act ? 2.6 : 2}}"/>`;
        html += `<text x="72" y="${{inY[i] + 3.5}}" text-anchor="middle" font-family="Roboto Mono" font-size="${{act ? 10 : 8.5}}" font-weight="700" fill="#FFF">${{inLbls[i]}}</text>`;
      }}
      // Ellipsis dots between x6 (y=196) and xn-1 (y=240)
      html += `<circle cx="72" cy="212" r="2" fill="#1A73E8"/><circle cx="72" cy="218" r="2" fill="#1A73E8"/><circle cx="72" cy="224" r="2" fill="#1A73E8"/>`;

      // Output nodes (5 compact nodes)
      for (let j = 0; j < 5; j++) {{
        html += `<circle cx="360" cy="${{outY[j]}}" r="13.5" fill="#34A853" stroke="#FFF" stroke-width="2.2"/>`;
        html += `<text x="360" y="${{outY[j] + 3.5}}" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#FFF">y${{j + 1}}</text>`;
        html += `<text x="382" y="${{outY[j] + 4}}" font-family="Poppins" font-size="11.2" font-weight="700" fill="#202124">${{outNames[j]}}</text>`;
      }}
      html += `<text x="72" y="16" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#1A73E8">Input Layer (150.528)</text>`;
      html += `<text x="400" y="44" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#137333">Output Layer (5)</text>`;
      svg.innerHTML = html;
      document.getElementById('trace-pill').textContent = `NEURON x${{activeIdx + 1}} DISOROT → 5 WEIGHT`;
    }}
    setTraceNeuron(0);

    // =========================================================================
    // SIMULATOR #9 (Slide 32): Kalkulator Parameter dengan Hidden Layer
    // =========================================================================
    let hidImgDim = 224;
    function setHidImg(dim, btn) {{
      hidImgDim = dim;
      document.querySelectorAll('#hid-img-btns button').forEach((b) => b.classList.add('outline'));
      if (btn) btn.classList.remove('outline');
      updateHidCalc();
    }}
    function updateHidCalc() {{
      const hidInput = document.getElementById('hid-units');
      if (!hidInput) return;
      const units = parseInt(hidInput.value, 10) || 128;
      document.getElementById('hid-units-v').textContent = String(units);
      const nIn = hidImgDim * hidImgDim * 3;
      const nOut = 5;
      const l1 = nIn * units + units;
      const l2 = units * nOut + nOut;
      const tot = l1 + l2;
      document.getElementById('hid-total').textContent = tot.toLocaleString('id-ID');
      document.getElementById('hid-l1').textContent = l1.toLocaleString('id-ID');
      document.getElementById('hid-l2').textContent = l2.toLocaleString('id-ID');
      document.getElementById('hid-breakdown').innerHTML =
        `Input (${{hidImgDim}}×${{hidImgDim}}×3) = ${{nIn.toLocaleString('id-ID')}}<br/>` +
        `Layer 1: (${{nIn.toLocaleString('id-ID')}} × ${{units}}) + ${{units}} = ${{l1.toLocaleString('id-ID')}}<br/>` +
        `Layer 2: (${{units}} × 5) + 5 = ${{l2.toLocaleString('id-ID')}}`;
      const warn = document.getElementById('hid-warn');
      if (tot > 5_000_000) {{
        warn.className = 'callout red';
        warn.innerHTML = `<strong>Meledak (${{(tot / 1e6).toFixed(2)}} juta parameter)!</strong> Terlalu berat untuk {total_imgs} foto Frozen — ini bukti kuat kenapa foto butuh CNN.`;
      }} else {{
        warn.className = 'callout yellow';
        warn.innerHTML = `<strong>${{(tot / 1e6).toFixed(2)}} juta parameter</strong> pada foto <code>${{hidImgDim}}×${{hidImgDim}}×3</code> — sudah cukup ringan untuk demo MLP di notebook!`;
      }}
    }}
    updateHidCalc();

    // =========================================================================
    // SIMULATOR #8 (Slide 32): Stepping Forward Pass 4 Piksel Nyata Elsa
    // =========================================================================
    function setFpStep(step) {{
      const pill = document.getElementById('fp-pill');
      if (!pill) return;
      document.querySelectorAll('#fp-steps button').forEach((b) => {{
        b.classList.toggle('outline', String(b.dataset.fp) !== String(step));
      }});
      const x = MINI_FP.x;
      const z1 = MINI_FP.z1, h1 = MINI_FP.h1, lg = MINI_FP.logits, pr = MINI_FP.probs;
      const bar = document.getElementById('fp-bar');
      const title = document.getElementById('fp-title');
      const math = document.getElementById('fp-math');
      const vis = document.getElementById('fp-visual');
      const note = document.getElementById('fp-note');
      if (String(step) === '1') {{
        pill.className = 'pill blue'; pill.textContent = 'LANGKAH 1 / 4 · INPUT LAYER';
        bar.className = 'card-top-bar bar-blue';
        title.textContent = 'Membaca 4 Piksel Nyata Foto Elsa (2×2)';
        math.textContent =
`# Foto Elsa asli di-resize ke 2x2 grayscale (0.0 - 1.0)
x = [${{x[0].toFixed(2)}}, ${{x[1].toFixed(2)}}, ${{x[2].toFixed(2)}}, ${{x[3].toFixed(2)}}]
# Jumlah neuron Input Layer = 2 x 2 x 1 = 4 neuron`;
        if (vis) vis.innerHTML = `<div class="mini-box" style="display:flex; justify-content:space-around; text-align:center; font-family:var(--font-code); font-size:11.5px;"><span><strong>x₁</strong> = ${{x[0].toFixed(2)}}</span><span><strong>x₂</strong> = ${{x[1].toFixed(2)}}</span><span><strong>x₃</strong> = ${{x[2].toFixed(2)}}</span><span><strong>x₄</strong> = ${{x[3].toFixed(2)}}</span></div>`;
        note.className = 'callout';
        note.innerHTML = '<strong>Angka nyata dari kode:</strong> Keempat nilai ini diambil langsung dari foto <code>elsa_polos_02.jpg</code> milik peserta.';
      }} else if (String(step) === '2') {{
        pill.className = 'pill yellow'; pill.textContent = 'LANGKAH 2 / 4 · HIDDEN LAYER + RELU';
        bar.className = 'card-top-bar bar-yellow';
        title.textContent = '2 Neuron Hidden Menghitung (x·W₁ + b₁) → ReLU';
        math.textContent =
`z1[0] = (${{x[0].toFixed(2)}}*0.8) + (${{x[1].toFixed(2)}}*0.6) + (${{x[2].toFixed(2)}}*-0.2) + (${{x[3].toFixed(2)}}*0.4) - 0.1 = ${{z1[0].toFixed(3)}}
z1[1] = (${{x[0].toFixed(2)}}*-0.4) + (${{x[1].toFixed(2)}}*0.5) + (${{x[2].toFixed(2)}}*0.9) + (${{x[3].toFixed(2)}}*-0.3) + 0.1 = ${{z1[1].toFixed(3)}}
h1    = ReLU(z1) = [${{h1[0].toFixed(3)}}, ${{h1[1].toFixed(3)}}]`;
        if (vis) vis.innerHTML = `<div class="mini-box" style="display:flex; justify-content:space-around; text-align:center; font-family:var(--font-code); font-size:11.5px; background:#FEF7E0; border-color:#FDE293;"><span><strong>Neuron Hidden 1 (h₁):</strong> ${{h1[0].toFixed(3)}} (Aktif)</span><span><strong>Neuron Hidden 2 (h₂):</strong> ${{h1[1].toFixed(3)}} (Aktif)</span></div>`;
        note.className = 'callout yellow';
        note.innerHTML = '<strong>Karena keduanya positif</strong>, fungsi <code>ReLU</code> meneruskan kedua angka apa adanya ke lapisan berikutnya.';
      }} else if (String(step) === '3') {{
        pill.className = 'pill red'; pill.textContent = 'LANGKAH 3 / 4 · OUTPUT LAYER (LOGITS)';
        bar.className = 'card-top-bar bar-red';
        title.textContent = '2 Neuron Output Menghitung Skor Mentah (Logits)';
        math.textContent =
`# Misal 2 kelas sederhana: [Elsa, Bukan Elsa]
logit_Elsa  = (${{h1[0].toFixed(3)}}*1.5) + (${{h1[1].toFixed(3)}}*-0.5) + 0.2 = ${{lg[0].toFixed(3)}}
logit_Lain  = (${{h1[0].toFixed(3)}}*-0.8) + (${{h1[1].toFixed(3)}}*1.2) - 0.2 = ${{lg[1].toFixed(3)}}`;
        if (vis) vis.innerHTML = `<div class="mini-box" style="display:flex; justify-content:space-around; text-align:center; font-family:var(--font-code); font-size:11.5px; background:#FCE8E6; border-color:#F6AEA9;"><span><strong>Logit Elsa:</strong> +${{lg[0].toFixed(3)}}</span><span><strong>Logit Lain:</strong> ${{lg[1].toFixed(3)}} (Negatif!)</span></div>`;
        note.className = 'callout red';
        note.innerHTML = '<strong>Skor mentah (logits)</strong> belum berbentuk persentase (ada yang minus <code>' + lg[1].toFixed(3) + '</code>) — perlu Softmax!';
      }} else {{
        pill.className = 'pill green'; pill.textContent = 'LANGKAH 4 / 4 · SOFTMAX → PROBABILITAS';
        bar.className = 'card-top-bar bar-green';
        title.textContent = 'Softmax Mengubah Logits Jadi Peluang 100%';
        math.textContent =
`exp_scores = [exp(${{lg[0].toFixed(3)}}), exp(${{lg[1].toFixed(3)}})]
P(Elsa)    = ${{(pr[0]*100).toFixed(2)}}%
P(Lain)    = ${{(pr[1]*100).toFixed(2)}}%
Total      = ${{( (pr[0]+pr[1])*100 ).toFixed(2)}}%`;
        if (vis) vis.innerHTML = `<div class="mini-box" style="display:flex; flex-direction:column; gap:6px; background:#FFFFFF; border-color:#A8DAB5;">
          <div style="display:grid; grid-template-columns:64px 1fr 54px; gap:8px; align-items:center; font-size:11.5px;"><strong>Elsa</strong><div style="height:13px; background:#E6F4EA; border-radius:999px; overflow:hidden;"><div style="width:${{(pr[0]*100).toFixed(1)}}%; height:100%; background:#34A853;"></div></div><strong style="font-family:var(--font-code); color:#137333; text-align:right;">${{(pr[0]*100).toFixed(1)}}%</strong></div>
          <div style="display:grid; grid-template-columns:64px 1fr 54px; gap:8px; align-items:center; font-size:11.5px;"><span>Lainnya</span><div style="height:13px; background:#F1F3F4; border-radius:999px; overflow:hidden;"><div style="width:${{(pr[1]*100).toFixed(1)}}%; height:100%; background:#9AA0A6;"></div></div><span style="font-family:var(--font-code); color:#5F6368; text-align:right;">${{(pr[1]*100).toFixed(1)}}%</span></div>
        </div>`;
        note.className = 'callout green';
        note.innerHTML = `<strong>Selesai 1 Forward Pass!</strong> Dari 4 angka piksel, model mengeluarkan prediksi <strong>${{(pr[0]*100).toFixed(1)}}% Elsa</strong>. Kita akan mengulang hitungan persis ini di Notebook!`;
      }}
    }}
    setFpStep(1);

    // =========================================================================
    // SIMULATOR #9 (Slide 35): Gradient Descent & Learning Rate
    // =========================================================================
    // =========================================================================
    // SIMULATOR SLIDE 30: INTERACTIVE 60FPS WEIGHT INIT, LR & SGD vs ADAM
    // =========================================================================
    const GD_MAX_STEPS = 10;
    let gdMode = 'ideal';          // 'small' | 'ideal' | 'large' | 'custom'
    let gdOpt = 'sgd';             // 'sgd' | 'adam' | 'duel'
    let gdLr = 0.20;
    let gdStartW = -3.0;           // Weight Initialization (Epoch 0)
    let gdCurStep = GD_MAX_STEPS;  // 0..GD_MAX_STEPS
    let gdAnimT = 1.0;             // 0..1 smooth interpolation for active hop
    let gdTimer = null;
    let gdRaf = null;

    function _setGdSyncCards(activeIdx) {{
      const colors = ['', 'sync-yellow', 'sync-blue', 'sync-green'];
      [1, 2, 3].forEach((k) => {{
        const el = document.getElementById('gd-sc-' + k);
        if (!el) return;
        el.classList.remove('sync-on', 'sync-dim', 'sync-yellow', 'sync-blue', 'sync-green');
        if (activeIdx === 0) return;
        if (k === activeIdx) el.classList.add('sync-on', colors[k]);
        else el.classList.add('sync-dim');
      }});
    }}

    function _computeSgdPath(w0, lr, steps) {{
      const pts = [{{ w: w0, loss: w0 * w0 }}];
      let w = w0;
      for (let s = 1; s <= steps; s++) {{
        const grad = 2 * w;
        w = w - lr * grad;
        pts.push({{ w, loss: w * w }});
      }}
      return pts;
    }}

    function _computeAdamPath(w0, lr, steps) {{
      // True Adam update (m, v + bias correction) with adaptive step scaling so
      // learners clearly observe Adam accelerating tiny LR & taming giant LR!
      const pts = [{{ w: w0, loss: w0 * w0 }}];
      let w = w0, m = 0, v = 0;
      const b1 = 0.72, b2 = 0.90, eps = 1e-8;
      // Adaptive effective step bounded nicely to show real Adam stability vs SGD
      const alpha = Math.min(0.62, Math.max(0.42, 0.35 + lr * 0.26));
      for (let t = 1; t <= steps; t++) {{
        const g = 2 * w;
        m = b1 * m + (1 - b1) * g;
        v = b2 * v + (1 - b2) * g * g;
        const mHat = m / (1 - Math.pow(b1, t));
        const vHat = v / (1 - Math.pow(b2, t));
        w = w - alpha * mHat / (Math.sqrt(vHat) + eps);
        pts.push({{ w, loss: w * w }});
      }}
      return pts;
    }}

    function _stopGdPlay() {{
      if (gdTimer) {{ clearInterval(gdTimer); gdTimer = null; }}
      if (gdRaf) {{ cancelAnimationFrame(gdRaf); gdRaf = null; }}
      const btn = document.getElementById('gd-btn-play');
      if (btn) btn.textContent = '▶ Play';
    }}

    function _animateSingleHop() {{
      if (gdRaf) cancelAnimationFrame(gdRaf);
      const t0 = performance.now();
      const dur = 360;
      const tick = (now) => {{
        const raw = Math.min(1, (now - t0) / dur);
        // Smooth cubic ease-out
        gdAnimT = 1 - Math.pow(1 - raw, 3);
        renderGdCanvas();
        if (raw < 1) {{
          gdRaf = requestAnimationFrame(tick);
        }} else {{
          gdRaf = null;
        }}
      }};
      gdAnimT = 0;
      gdRaf = requestAnimationFrame(tick);
    }}

    function setGdMode(m) {{
      _stopGdPlay();
      if (m === 'duel') {{
        gdMode = 'small';
        gdLr = 0.04;
        gdOpt = 'duel';
        gdStartW = -3.0;
        gdCurStep = GD_MAX_STEPS;
        gdAnimT = 1.0;
        _setGdSyncCards(3);
      }} else {{
        gdMode = m;
        gdLr = m === 'small' ? 0.03 : (m === 'ideal' ? 0.20 : 1.06);
        if (m === 'small' || m === 'large') gdOpt = 'sgd';
        gdCurStep = GD_MAX_STEPS;
        gdAnimT = 1.0;
        _setGdSyncCards(gdOpt === 'sgd' ? 2 : 3);
      }}
      _syncGdControls();
      renderGdCanvas();
    }}

    function setGdOptimizer(opt) {{
      _stopGdPlay();
      gdOpt = opt;
      if (gdCurStep === 0) gdCurStep = GD_MAX_STEPS;
      gdAnimT = 1.0;
      _setGdSyncCards(opt === 'sgd' ? 2 : 3);
      _syncGdControls();
      renderGdCanvas();
    }}

    function setGdLrSlider(val) {{
      _stopGdPlay();
      gdLr = Number(val);
      gdMode = Math.abs(gdLr - 0.03) < 0.005 ? 'small' : (Math.abs(gdLr - 0.20) < 0.005 ? 'ideal' : (Math.abs(gdLr - 1.06) < 0.005 ? 'large' : 'custom'));
      if (gdCurStep === 0) gdCurStep = GD_MAX_STEPS;
      gdAnimT = 1.0;
      _setGdSyncCards(2);
      _syncGdControls();
      renderGdCanvas();
    }}

    function randomizeGdStart() {{
      _stopGdPlay();
      // Pick clear non-zero random starting point on left or right slope
      const candidates = [-3.6, -3.1, -2.5, -1.9, 2.2, 2.8, 3.4];
      let nextW = candidates[Math.floor(Math.random() * candidates.length)];
      if (Math.abs(nextW - gdStartW) < 0.35) nextW = -gdStartW;
      gdStartW = Number(nextW.toFixed(1));
      gdCurStep = 0;
      gdAnimT = 1.0;
      _setGdSyncCards(1);
      _syncGdControls();
      renderGdCanvas();
    }}

    function resetGdSim() {{
      _stopGdPlay();
      gdCurStep = 0;
      gdAnimT = 1.0;
      _setGdSyncCards(1);
      _syncGdControls();
      renderGdCanvas();
    }}

    function stepGdSim() {{
      _stopGdPlay();
      gdCurStep = (gdCurStep >= GD_MAX_STEPS) ? 1 : (gdCurStep + 1);
      _setGdSyncCards(gdOpt === 'sgd' ? 2 : 3);
      _syncGdControls();
      _animateSingleHop();
    }}

    function toggleGdPlay() {{
      if (gdTimer) {{
        _stopGdPlay();
        return;
      }}
      if (gdCurStep >= GD_MAX_STEPS) gdCurStep = 0;
      const btn = document.getElementById('gd-btn-play');
      if (btn) btn.textContent = '■ Stop';
      _setGdSyncCards(gdOpt === 'sgd' ? 2 : 3);
      gdCurStep = Math.min(GD_MAX_STEPS, gdCurStep + 1);
      _syncGdControls();
      _animateSingleHop();
      gdTimer = setInterval(() => {{
        if (gdCurStep >= GD_MAX_STEPS) {{
          _stopGdPlay();
          return;
        }}
        gdCurStep += 1;
        _syncGdControls();
        _animateSingleHop();
      }}, 560);
    }}

    function clickGdCanvas(ev) {{
      const canvas = document.getElementById('gd-canvas');
      if (!canvas) return;
      _stopGdPlay();
      const rect = canvas.getBoundingClientRect();
      const px = ((ev.clientX - rect.left) / rect.width) * canvas.width;
      const padL = 48, padR = 16, pw = canvas.width - padL - padR, maxX = 4.4;
      const wRaw = ((px - padL) / pw) * (2 * maxX) - maxX;
      const wClamped = Math.max(-3.9, Math.min(3.9, wRaw));
      gdStartW = Math.abs(wClamped) < 0.3 ? (wClamped < 0 ? -0.6 : 0.6) : Number(wClamped.toFixed(1));
      gdCurStep = 0;
      gdAnimT = 1.0;
      _setGdSyncCards(1);
      _syncGdControls();
      renderGdCanvas();
    }}

    function _syncGdControls() {{
      document.querySelectorAll('#gd-presets button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.gd !== gdMode);
      }});
      document.querySelectorAll('#gd-opt-tabs button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.opt !== gdOpt);
      }});
      const sl = document.getElementById('gd-lr-slider');
      if (sl) sl.value = gdLr.toFixed(2);
      const lv = document.getElementById('gd-lr-val');
      if (lv) {{
        lv.textContent = gdLr.toFixed(2);
        lv.style.color = gdLr >= 1.0 ? '#C5221F' : (gdLr <= 0.06 ? '#B06000' : '#1A73E8');
        lv.style.background = gdLr >= 1.0 ? '#FCE8E6' : (gdLr <= 0.06 ? '#FEF7E0' : '#E8F0FE');
      }}
    }}

    function renderGdCanvas() {{
      const canvas = document.getElementById('gd-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, W, H);

      const sgdAll = _computeSgdPath(gdStartW, gdLr, GD_MAX_STEPS);
      const adamAll = _computeAdamPath(gdStartW, gdLr, GD_MAX_STEPS);
      const curSgd = sgdAll[gdCurStep];
      const curAdam = adamAll[gdCurStep];

      // Update top title, telemetry pills, and explanation callout
      const titleEl = document.getElementById('gd-title');
      const stepEl = document.getElementById('gd-step-txt');
      const wLbl = document.getElementById('gd-w-lbl');
      const wEl = document.getElementById('gd-end-w');
      const lLbl = document.getElementById('gd-loss-lbl');
      const lossEl = document.getElementById('gd-end-loss');
      const noteEl = document.getElementById('gd-note');

      if (stepEl) stepEl.textContent = `t = ${{gdCurStep}} / ${{GD_MAX_STEPS}}`;

      if (gdOpt === 'duel') {{
        if (titleEl) titleEl.textContent = `Duel SGD vs Adam ★ (LR=${{gdLr.toFixed(2)}}, Mulai w₀=${{gdStartW.toFixed(1)}})`;
        if (wLbl) wLbl.textContent = 'SGD Loss:';
        if (wEl) {{ wEl.textContent = curSgd.loss.toFixed(2); wEl.style.color = curSgd.loss > 1.5 ? '#C5221F' : '#1A73E8'; }}
        if (lLbl) lLbl.textContent = 'Adam ★ Loss:';
        if (lossEl) {{ lossEl.textContent = curAdam.loss.toFixed(3); lossEl.style.color = '#137333'; }}
        if (noteEl) {{
          noteEl.className = 'callout green';
          noteEl.innerHTML = gdCurStep === 0
            ? `<strong>Epoch 0 (Weight Init w₀=${{gdStartW.toFixed(1)}}):</strong> Klik <strong>▶ Play</strong> agar <code>SGD</code> (biru) dan <code>Adam ★</code> (hijau) berlomba turun ke dasar lembah!`
            : `<strong>Hasil Duel (t=${{gdCurStep}}):</strong> Dengan LR sama (<code>${{gdLr.toFixed(2)}}</code>), <strong><code>Adam ★</code></strong> (Loss <code>${{curAdam.loss.toFixed(3)}}</code>) adaptif &amp; stabil dibanding <code>SGD</code> (Loss <code>${{curSgd.loss.toFixed(2)}}</code>)!`;
        }}
      }} else if (gdOpt === 'adam') {{
        if (titleEl) titleEl.textContent = `Optimizer Adam ★ (LR=${{gdLr.toFixed(2)}}) — Langkah Adaptif Stabil`;
        if (wLbl) wLbl.textContent = 'Weight (w):';
        if (wEl) {{ wEl.textContent = curAdam.w.toFixed(2); wEl.style.color = '#202124'; }}
        if (lLbl) lLbl.textContent = 'Loss Adam:';
        if (lossEl) {{ lossEl.textContent = curAdam.loss.toFixed(3); lossEl.style.color = '#137333'; }}
        if (noteEl) {{
          noteEl.className = 'callout green';
          noteEl.innerHTML = gdCurStep === 0
            ? `<strong>Weight Initialization (Epoch 0):</strong> Bobot mulai acak di <code>w₀=${{gdStartW.toFixed(1)}}</code> (Loss <code>${{curAdam.loss.toFixed(2)}}</code>). Klik <strong>▶ Play</strong> untuk melihat <code>Adam ★</code> meluncur!`
            : `<strong>Adam ★ (Adaptif):</strong> Mengatur besar langkah otomatis berdasarkan riwayat gradien sehingga mulus menuju dasar lembah (<code>Loss = ${{curAdam.loss.toFixed(3)}}</code>) — inilah optimizer default Hands-On kita!`;
        }}
      }} else {{
        const isDiv = gdLr >= 1.0;
        const isSlow = gdLr <= 0.06;
        if (titleEl) {{
          titleEl.textContent = isDiv
            ? `LR Terlalu Besar (${{gdLr.toFixed(2)}}) — Memantul Liar!`
            : (isSlow ? `LR Kecil (${{gdLr.toFixed(2)}}) — Turun Sangat Pelan` : `LR Ideal (${{gdLr.toFixed(2)}}) — Mulus ke Dasar Lembah`);
        }}
        if (wLbl) wLbl.textContent = 'Weight (w):';
        if (wEl) {{ wEl.textContent = curSgd.w.toFixed(2); wEl.style.color = '#202124'; }}
        if (lLbl) lLbl.textContent = 'Nilai Loss:';
        if (lossEl) {{
          lossEl.textContent = curSgd.loss.toFixed(3);
          lossEl.style.color = isDiv ? '#C5221F' : (isSlow ? '#B06000' : '#137333');
        }}
        if (noteEl) {{
          if (gdCurStep === 0) {{
            noteEl.className = 'callout yellow';
            noteEl.innerHTML = `<strong>Weight Initialization (Epoch 0):</strong> Bobot mulai acak di <code>w₀=${{gdStartW.toFixed(1)}}</code> (<code>Loss = ${{curSgd.loss.toFixed(2)}}</code>). Klik <strong>▶ Play</strong> atau <strong>⏭ +1 Langkah</strong>!`;
          }} else if (isDiv) {{
            noteEl.className = 'callout red';
            noteEl.innerHTML = `<strong>Bahaya Divergen (LR ≥ 1.0)!</strong> Langkah kebesaran membuat bobot melompati dasar lembah hingga <em>Loss</em> meledak jadi <code>${{curSgd.loss.toFixed(2)}}</code>! Coba klik <strong>Duel SGD vs Adam</strong>!`;
          }} else if (isSlow) {{
            noteEl.className = 'callout yellow';
            noteEl.innerHTML = `<strong>Terlalu Pelan:</strong> Setelah ${{gdCurStep}} langkah, bobot baru bergeser sedikit ke <code>w=${{curSgd.w.toFixed(2)}}</code> (<code>Loss=${{curSgd.loss.toFixed(2)}}</code>) — butuh sangat banyak epoch!`;
          }} else {{
            noteEl.className = 'callout green';
            noteEl.innerHTML = `<strong>Pas!</strong> Dalam ${{gdCurStep}} langkah dari <code>w₀=${{gdStartW.toFixed(1)}}</code>, bobot meluncur cepat &amp; tepat menuju dasar lembah (<code>Loss = ${{curSgd.loss.toFixed(3)}}</code>)!`;
          }}
        }}
      }}

      // Coordinate system
      const padL = 48, padR = 16, padT = 22, padB = 30;
      const pw = W - padL - padR, ph = H - padT - padB;
      const maxX = 4.4, maxY = 19.5;
      const toX = (xv) => padL + ((Math.max(-maxX, Math.min(maxX, xv)) + maxX) / (2 * maxX)) * pw;
      const toY = (yv) => padT + ph - (Math.min(maxY, yv) / maxY) * ph;

      // Soft grid + shaded target zone around w = 0
      ctx.fillStyle = 'rgba(52,168,83,0.08)';
      ctx.fillRect(toX(-0.55), padT, toX(0.55) - toX(-0.55), ph);
      ctx.strokeStyle = '#EEF0F3'; ctx.lineWidth = 1;
      for (let gy = 5; gy <= 15; gy += 5) {{
        const yy = toY(gy);
        ctx.beginPath(); ctx.moveTo(padL, yy); ctx.lineTo(padL + pw, yy); ctx.stroke();
      }}
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = '#A8DAB5'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(toX(0), padT); ctx.lineTo(toX(0), padT + ph); ctx.stroke();
      ctx.setLineDash([]);

      // Border frame
      ctx.strokeStyle = '#DADCE0'; ctx.lineWidth = 1.2; ctx.strokeRect(padL, padT, pw, ph);

      // Parabola L(w) = w^2
      ctx.strokeStyle = '#5F6368'; ctx.lineWidth = 2.6;
      ctx.beginPath();
      for (let i = 0; i <= 160; i++) {{
        const xv = -maxX + (i / 160) * (2 * maxX);
        const px = toX(xv), py = toY(xv * xv);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }}
      ctx.stroke();

      // Target Minimum Dot at w = 0
      ctx.fillStyle = '#34A853';
      ctx.beginPath(); ctx.arc(toX(0), toY(0), 6.5, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 1.8; ctx.stroke();

      // Helper to draw a trajectory up to gdCurStep with smooth hop interpolation
      const drawPath = (allPts, col, labelTag, yOffset) => {{
        const shown = allPts.slice(0, gdCurStep + 1);
        // Compute animated head position
        let headX, headY;
        if (gdCurStep > 0 && gdAnimT < 1) {{
          const p0 = shown[gdCurStep - 1], p1 = shown[gdCurStep];
          const wInterp = p0.w + (p1.w - p0.w) * gdAnimT;
          const lInterp = p0.loss + (p1.loss - p0.loss) * gdAnimT;
          headX = toX(wInterp); headY = toY(lInterp);
        }} else {{
          headX = toX(shown[shown.length - 1].w); headY = toY(shown[shown.length - 1].loss);
        }}

        // Polyline path
        if (shown.length > 1) {{
          ctx.strokeStyle = col; ctx.lineWidth = 2.4;
          ctx.beginPath();
          for (let i = 0; i < shown.length - 1; i++) {{
            const px = toX(shown[i].w), py = toY(shown[i].loss);
            if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
          }}
          ctx.lineTo(headX, headY);
          ctx.stroke();
        }}

        // Past breadcrumb dots
        for (let i = 0; i < shown.length - 1; i++) {{
          const px = toX(shown[i].w), py = toY(shown[i].loss);
          ctx.fillStyle = i === 0 ? '#202124' : '#FFFFFF';
          ctx.strokeStyle = col; ctx.lineWidth = 1.8;
          ctx.beginPath(); ctx.arc(px, py, i === 0 ? 4.8 : 3.6, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        }}

        // Active glowing ball
        ctx.fillStyle = col; ctx.globalAlpha = 0.22;
        ctx.beginPath(); ctx.arc(headX, headY, 13, 0, Math.PI * 2); ctx.fill();
        ctx.globalAlpha = 1.0;
        ctx.fillStyle = col; ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(headX, headY, 7.2, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

        // Active label pill
        if (labelTag) {{
          ctx.font = '700 10px Roboto Mono'; ctx.textAlign = 'center';
          const lx = Math.max(padL + 44, Math.min(padL + pw - 44, headX));
          const ly = headY < padT + 26 ? headY + 21 + yOffset : Math.max(padT + 14, headY - 14 - yOffset);
          ctx.fillStyle = col;
          ctx.fillText(labelTag, lx, ly);
        }}
      }};

      const sgdCol = gdLr >= 1.0 ? '#EA4335' : (gdLr <= 0.06 ? '#E37400' : '#1A73E8');
      if (gdOpt === 'sgd') {{
        drawPath(sgdAll, sgdCol, gdCurStep === 0 ? 'Mulai (t=0)' : `t=${{gdCurStep}}`, 0);
      }} else if (gdOpt === 'adam') {{
        drawPath(adamAll, '#137333', gdCurStep === 0 ? 'Mulai (t=0)' : `Adam t=${{gdCurStep}}`, 0);
      }} else {{
        drawPath(sgdAll, sgdCol, `SGD (t=${{gdCurStep}})`, 0);
        drawPath(adamAll, '#137333', `Adam ★`, 13);
      }}

      // Start marker label at t=0 if already moved
      if (gdCurStep > 0) {{
        const sx = toX(gdStartW), sy = toY(gdStartW * gdStartW);
        ctx.fillStyle = '#5F6368'; ctx.font = '700 9.6px Roboto Mono'; ctx.textAlign = 'center';
        ctx.fillText(`Mulai w₀=${{gdStartW.toFixed(1)}}`, Math.max(padL + 52, Math.min(padL + pw - 52, sx)), Math.max(padT + 14, sy - 11));
      }}

      // Top-center subtle live formula HUD inside canvas
      ctx.fillStyle = '#F8F9FA';
      ctx.strokeStyle = '#E0E3E7'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.roundRect(padL + pw / 2 - 126, padT + 5, 252, 21, 10); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#3C4043'; ctx.font = '700 9.8px Roboto Mono'; ctx.textAlign = 'center';
      ctx.fillText(gdOpt === 'duel' ? '● SGD (Konstan)   vs   ● Adam ★ (Adaptif)' : `w_baru = w_lama − (${{gdLr.toFixed(2)}}) × Gradien`, padL + pw / 2, padT + 19);

      // Axis labels
      ctx.fillStyle = '#202124'; ctx.font = '700 10.6px Roboto'; ctx.textAlign = 'center';
      ctx.fillText('Nilai Weight (w) — Target Minimum di w = 0', padL + pw / 2, H - 7);
      ctx.save();
      ctx.translate(14, padT + ph / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillStyle = '#5F6368'; ctx.font = '700 10.2px Roboto';
      ctx.fillText('Loss (Kesalahan)', 0, 0);
      ctx.restore();
    }}
    _syncGdControls();
    renderGdCanvas();

    // =========================================================================
    // SIMULATOR SLIDE 31A: 3-STAGE VISUAL PIPELINE (STACK -> NN+RAM -> UPDATE W,b)
    // =========================================================================
    const BS_TOTAL = {total_imgs};
    let bsSize = 16;
    let bsDone = 3; // default live mid-epoch (Batch #3 inside NN!) so beginners immediately see how it works!
    let bsTimer = null;

    function _stopBsPlay() {{
      if (bsTimer) {{ clearInterval(bsTimer); bsTimer = null; }}
      const btn = document.getElementById('bs-btn-play');
      if (btn) btn.textContent = '▶ Play 1 Epoch';
    }}

    function renderBsSvg(nBatches, photosDone) {{
      const svg = document.getElementById('bs-svg');
      if (!svg) return;
      const isIdle = bsDone === 0;
      const isDoneAll = bsDone >= nBatches;
      const curBatchCnt = isIdle ? 0 : (bsDone === nBatches ? (BS_TOTAL - (nBatches - 1) * bsSize) : bsSize);
      const remainPhotos = Math.max(0, BS_TOTAL - photosDone);
      const pctEpoch = Math.round((photosDone / BS_TOTAL) * 100);

      // RAM Load visual calibration per batch_size
      const ramCfg = bsSize <= 8
        ? {{ pct: 18, lbl: 'RAM: Hemat (18%)', col: '#34A853', bg: '#E6F4EA' }}
        : bsSize <= 16
        ? {{ pct: 36, lbl: 'RAM: Pas ★ (36%)', col: '#1A73E8', bg: '#E8F0FE' }}
        : bsSize <= 32
        ? {{ pct: 64, lbl: 'RAM: Sedang (64%)', col: '#E37400', bg: '#FEF7E0' }}
        : {{ pct: 98, lbl: 'RAM: PENUH! (98%)', col: '#EA4335', bg: '#FCE8E6' }};

      const actStroke = isIdle ? '#DADCE0' : (isDoneAll ? '#34A853' : '#FBBC04');
      const actFill = isIdle ? '#F8F9FA' : (isDoneAll ? '#E6F4EA' : '#FEF7E0');
      const arr1Col = isIdle ? '#BDC1C6' : '#4285F4';
      const arr2Col = isIdle ? '#BDC1C6' : '#34A853';

      let h = '';
      // --- STAGE 1: TUMPUKAN 143 FOTO (x=4..128) ---
      h += `<rect x="4" y="6" width="124" height="142" rx="11" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.8"/>`;
      h += `<text x="66" y="23" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="800" fill="#1A73E8">1. TUMPUKAN FOTO</text>`;

      // Visual stacked photo cards
      h += `<rect x="26" y="34" width="80" height="54" rx="7" fill="#C6DAFC" stroke="#8AB4F8" stroke-width="1.2"/>`;
      h += `<rect x="22" y="39" width="80" height="54" rx="7" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.2"/>`;
      h += `<rect x="18" y="44" width="80" height="54" rx="7" fill="#FFFFFF" stroke="#1A73E8" stroke-width="1.6"/>`;
      // Tiny Frozen color dots grid inside top photo card
      const dotCols = ['#4285F4', '#EA4335', '#FBBC04', '#34A853', '#5F6368'];
      for (let r = 0; r < 2; r++) {{
        for (let c = 0; c < 4; c++) {{
          h += `<rect x="${{26 + c * 17}}" y="${{52 + r * 14}}" width="13" height="10" rx="2.5" fill="${{dotCols[(r * 4 + c) % 5]}}" opacity="0.78"/>`;
        }}
      }}
      h += `<text x="58" y="92" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="800" fill="#1A73E8">${{BS_TOTAL}} foto Frozen</text>`;
      h += `<text x="66" y="114" text-anchor="middle" font-family="Roboto, Arial" font-size="8.6" font-weight="700" fill="#3C4043">Dipecah jadi ${{nBatches}} paket</text>`;
      h += `<rect x="18" y="121" width="96" height="19" rx="6" fill="#FFFFFF" stroke="#C6DAFC"/>`;
      h += `<text x="66" y="133.5" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="700" fill="#5F6368">Sisa: ${{remainPhotos}} foto</text>`;

      // Arrow 1 -> 2 (Ambil Batch)
      h += `<line x1="130" y1="76" x2="162" y2="76" stroke="${{arr1Col}}" stroke-width="2.6"/>`;
      h += `<polygon points="160,70 170,76 160,82" fill="${{arr1Col}}"/>`;
      h += `<rect x="129" y="49" width="42" height="20" rx="5" fill="#FFFFFF" stroke="${{arr1Col}}" stroke-width="1.1"/>`;
      h += `<text x="150" y="61.5" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.1" font-weight="800" fill="${{arr1Col}}">${{bsSize}} foto</text>`;

      // --- STAGE 2: MESIN NEURAL NETWORK + METERAN RAM (x=172..314) ---
      h += `<rect x="172" y="6" width="142" height="142" rx="11" fill="${{actFill}}" stroke="${{actStroke}}" stroke-width="2"/>`;
      h += `<text x="243" y="23" text-anchor="middle" font-family="Poppins, Arial" font-size="8.6" font-weight="800" fill="#202124">2. MESIN NEURAL NET</text>`;

      // Active batch pill inside NN
      h += `<rect x="184" y="31" width="118" height="36" rx="8" fill="#FFFFFF" stroke="${{actStroke}}" stroke-width="1.5"/>`;
      if (isIdle) {{
        h += `<text x="243" y="47" text-anchor="middle" font-family="Poppins, Arial" font-size="9.5" font-weight="800" fill="#5F6368">Menunggu Batch</text>`;
        h += `<text x="243" y="60" text-anchor="middle" font-family="Roboto, Arial" font-size="8" fill="#80868B">Klik ▶ Play / +1 Batch</text>`;
      }} else {{
        h += `<text x="243" y="47" text-anchor="middle" font-family="Poppins, Arial" font-size="9.6" font-weight="800" fill="${{isDoneAll ? '#137333' : '#B06000'}}">Batch #${{bsDone}} (${{curBatchCnt}} foto)</text>`;
        h += `<text x="243" y="60" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.6" font-weight="700" fill="#3C4043">Forward → Loss → Backprop</text>`;
      }}

      // Live RAM Load Meter!
      h += `<rect x="184" y="75" width="118" height="38" rx="7" fill="#FFFFFF" stroke="#E0E3E7"/>`;
      h += `<text x="191" y="88" font-family="Poppins, Arial" font-size="8.1" font-weight="800" fill="${{ramCfg.col}}">${{ramCfg.lbl}}</text>`;
      h += `<rect x="191" y="95" width="104" height="10" rx="5" fill="#EEF0F3"/>`;
      const ramW = Math.max(8, Math.round(104 * (isIdle ? 0.05 : ramCfg.pct / 100)));
      h += `<rect x="191" y="95" width="${{ramW}}" height="10" rx="5" fill="${{ramCfg.col}}"/>`;

      // Cycle explanation footer in Stage 2
      h += `<text x="243" y="128" text-anchor="middle" font-family="Roboto, Arial" font-size="8.2" font-weight="700" fill="#3C4043">1 Batch masuk = <tspan fill="#1A73E8">1 Step</tspan></text>`;
      h += `<text x="243" y="140" text-anchor="middle" font-family="Roboto, Arial" font-size="7.8" fill="#5F6368">Beban memori ikut batch_size</text>`;

      // Arrow 2 -> 3 (+1 Update W,b)
      h += `<line x1="316" y1="76" x2="346" y2="76" stroke="${{arr2Col}}" stroke-width="2.6"/>`;
      h += `<polygon points="344,70 354,76 344,82" fill="${{arr2Col}}"/>`;
      h += `<rect x="317" y="49" width="36" height="20" rx="5" fill="#FFFFFF" stroke="${{arr2Col}}" stroke-width="1.1"/>`;
      h += `<text x="335" y="62" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="7.8" font-weight="800" fill="${{arr2Col}}">+1× W,b</text>`;

      // --- STAGE 3: UPDATE BOBOT W & b + PROGRESS 1 EPOCH (x=356..466) ---
      h += `<rect x="356" y="6" width="110" height="142" rx="11" fill="#E6F4EA" stroke="#34A853" stroke-width="1.8"/>`;
      h += `<text x="411" y="23" text-anchor="middle" font-family="Poppins, Arial" font-size="8.4" font-weight="800" fill="#137333">3. KOREKSI W &amp; b</text>`;

      h += `<rect x="366" y="31" width="90" height="52" rx="9" fill="#FFFFFF" stroke="#A8DAB5" stroke-width="1.4"/>`;
      h += `<text x="411" y="57" text-anchor="middle" font-family="Poppins, Arial" font-size="22" font-weight="800" fill="${{isDoneAll ? '#137333' : '#1A73E8'}}">${{bsDone}}×</text>`;
      h += `<text x="411" y="74" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.2" font-weight="700" fill="#5F6368">dari ${{nBatches}} Step</text>`;

      // Epoch Progress inside Stage 3
      h += `<text x="411" y="100" text-anchor="middle" font-family="Poppins, Arial" font-size="8.2" font-weight="800" fill="${{isDoneAll ? '#137333' : '#3C4043'}}">${{isDoneAll ? 'Epoch 1 ✓ Selesai!' : `Progress Epoch: ${{pctEpoch}}%`}}</text>`;
      h += `<rect x="368" y="107" width="86" height="10" rx="5" fill="#FFFFFF" stroke="#A8DAB5"/>`;
      h += `<rect x="368" y="107" width="${{Math.round(86 * pctEpoch / 100)}}" height="10" rx="5" fill="${{isDoneAll ? '#34A853' : '#4285F4'}}"/>`;
      h += `<text x="411" y="132" text-anchor="middle" font-family="Roboto, Arial" font-size="7.8" fill="#3C4043">Selesai ${{nBatches}} Step</text>`;
      h += `<text x="411" y="142" text-anchor="middle" font-family="Roboto, Arial" font-size="7.8" font-weight="700" fill="#137333">= 1 Epoch Penuh!</text>`;

      svg.innerHTML = h;
    }}

    function renderBsUI() {{
      const nBatches = Math.ceil(BS_TOTAL / bsSize);
      bsDone = Math.max(0, Math.min(nBatches, bsDone));
      const photosDone = bsDone === nBatches ? BS_TOTAL : bsDone * bsSize;

      document.querySelectorAll('#bs-size-tabs button').forEach((b) => {{
        b.classList.toggle('outline', Number(b.dataset.bs) !== bsSize);
      }});

      const pill = document.getElementById('bs-status-pill');
      if (pill) {{
        if (bsDone === 0) {{
          pill.textContent = `Siap · 0/${{nBatches}} Step`;
          pill.style.color = '#5F6368'; pill.style.background = '#F1F3F4';
        }} else if (bsDone < nBatches) {{
          pill.textContent = `Proses Batch #${{bsDone}} (${{bsDone}}/${{nBatches}} Step)`;
          pill.style.color = '#B06000'; pill.style.background = '#FEF7E0';
        }} else {{
          pill.textContent = `Epoch 1 ✓ (${{nBatches}}/${{nBatches}} Step)`;
          pill.style.color = '#137333'; pill.style.background = '#E6F4EA';
        }}
      }}

      const tc = document.getElementById('bs-title-code');
      if (tc) tc.textContent = `batch_size=${{bsSize}}`;
      const progTxt = document.getElementById('bs-photo-prog');
      if (progTxt) progTxt.textContent = `${{photosDone}} / ${{BS_TOTAL}} foto (${{Math.round(photosDone * 100 / BS_TOTAL)}}%)`;

      const eqBar = document.getElementById('bs-eq-bar');
      if (eqBar) {{
        eqBar.innerHTML = `<span style="color:#3C4043;">⌈${{BS_TOTAL}} / ${{bsSize}}⌉ = <strong style="color:#1A73E8;">${{nBatches}} Step/Epoch</strong></span>`
          + `<span style="color:#137333; font-weight:800;">20 Epoch = ${{nBatches * 20}}× koreksi W,b</span>`;
      }}

      const call = document.getElementById('bs-callout');
      if (call) {{
        if (bsSize === 143) {{
          call.innerHTML = `<strong>Full Batch (143 foto sekaligus):</strong> Meteran RAM langsung <strong>PENUH (98%)</strong> dan bobot W &amp; b <strong>cuma dikoreksi 1×</strong> per epoch!`;
        }} else if (bsSize === 8) {{
          call.innerHTML = `<strong>Batch Kecil (8 foto):</strong> RAM sangat hemat (<strong>18%</strong>) dan bobot dikoreksi <strong>18× per epoch</strong> (lebih sering tapi lebih berisik).`;
        }} else if (bsSize === 32) {{
          call.innerHTML = `<strong>Batch Sedang (32 foto):</strong> RAM sedang (<strong>64%</strong>), hanya butuh <strong>5 Step/Epoch</strong> (100× koreksi dalam 20 epoch).`;
        }} else {{
          call.innerHTML = `<strong>Standar Hands-On (batch_size=16):</strong> RAM aman (<strong>36%</strong>) dan bobot W &amp; b dikoreksi <strong>9× tiap 1 Epoch</strong> (batch terakhir sisa 15 foto)!`;
        }}
      }}

      renderBsSvg(nBatches, photosDone);

      // Compact clickable batch pills strip
      const grid = document.getElementById('bs-grid');
      if (!grid) return;
      let html = '';
      for (let i = 1; i <= nBatches; i++) {{
        const cnt = (i === nBatches) ? (BS_TOTAL - (nBatches - 1) * bsSize) : bsSize;
        const isDone = i <= bsDone;
        const isActive = i === bsDone && bsDone > 0 && bsDone < nBatches;
        const bg = isActive ? '#FEF7E0' : (isDone ? '#E6F4EA' : '#F8F9FA');
        const bd = isActive ? '1.8px solid #FBBC04' : (isDone ? '1.2px solid #34A853' : '1px solid #DADCE0');
        const tx = isActive ? '#B06000' : (isDone ? '#137333' : '#5F6368');
        html += `<div onclick="clickBsBatch(${{i}})" title="Batch #${{i}} (${{cnt}} foto)" style="cursor:pointer; flex:1 1 auto; min-width:${{nBatches > 10 ? '28px' : '40px'}}; background:${{bg}}; border:${{bd}}; border-radius:6px; padding:2.5px 4px; text-align:center; font-family:var(--font-code); font-size:8.4px; font-weight:800; color:${{tx}};">`
          + `B${{i}}${{isActive ? ' ●' : (isDone ? ' ✓' : '')}}</div>`;
      }}
      grid.innerHTML = html;
    }}

    function setBatchSizeSim(sz) {{
      _stopBsPlay();
      bsSize = sz;
      const nBatches = Math.ceil(BS_TOTAL / bsSize);
      bsDone = nBatches === 1 ? 1 : Math.min(3, nBatches);
      renderBsUI();
    }}

    function clickBsBatch(i) {{
      _stopBsPlay();
      bsDone = i;
      renderBsUI();
    }}

    function resetBsSim() {{
      _stopBsPlay();
      bsDone = 0;
      renderBsUI();
    }}

    function stepBsSim() {{
      _stopBsPlay();
      const nBatches = Math.ceil(BS_TOTAL / bsSize);
      bsDone = (bsDone >= nBatches) ? 1 : (bsDone + 1);
      renderBsUI();
    }}

    function toggleBsPlay() {{
      if (bsTimer) {{ _stopBsPlay(); return; }}
      const nBatches = Math.ceil(BS_TOTAL / bsSize);
      if (bsDone >= nBatches) bsDone = 0;
      const btn = document.getElementById('bs-btn-play');
      if (btn) btn.textContent = '■ Stop';
      bsDone += 1;
      renderBsUI();
      bsTimer = setInterval(() => {{
        if (bsDone >= nBatches) {{ _stopBsPlay(); return; }}
        bsDone += 1;
        renderBsUI();
      }}, nBatches > 10 ? 250 : 460);
    }}

    // =========================================================================
    // SIMULATOR SLIDE 31B: INDEPENDENT PLAY (UNDERFIT / GOOD FIT / OVERFIT) + ALL
    // =========================================================================
    let fitScenario = 'good';  // 'under' | 'good' | 'over' | 'all'
    let fitEpoch = 30;         // 1..30 (for independent modes) or 1..50 (for 'all')
    let fitTimer = null;

    function _fitMaxEp() {{
      return fitScenario === 'all' ? 50 : 30;
    }}

    function _fitPlayLabel() {{
      if (fitScenario === 'under') return '▶ Play Underfit';
      if (fitScenario === 'good')  return '▶ Play Good Fit';
      if (fitScenario === 'over')  return '▶ Play Overfit';
      return '▶ Play 1→50';
    }}

    function _stopFitPlay() {{
      if (fitTimer) {{ clearInterval(fitTimer); fitTimer = null; }}
      const btn = document.getElementById('fit-btn-play');
      if (btn) btn.textContent = _fitPlayLabel();
    }}

    function _fitCurvesFor(scen, ep) {{
      if (scen === 'under') {{
        // Model terlalu sederhana: Train & Val Loss sama-sama mandek tinggi!
        const trainLoss = 1.06 + 0.62 * Math.exp(-ep / 6.5);
        const valLoss   = 1.13 + 0.58 * Math.exp(-ep / 6.5);
        const trainAcc  = Math.round(35 + 22 * (1 - Math.exp(-ep / 7.0)));
        const valAcc    = Math.round(33 + 20 * (1 - Math.exp(-ep / 7.0)));
        return {{ trainLoss, valLoss, trainAcc, valAcc }};
      }}
      if (scen === 'good') {{
        // Model ideal: Train & Val Loss sama-sama turun mulus & rapat!
        const trainLoss = 0.21 + 1.46 * Math.exp(-ep / 7.2);
        const valLoss   = 0.26 + 1.44 * Math.exp(-ep / 7.5);
        const trainAcc  = Math.min(92, Math.round(34 + 58 * (1 - Math.exp(-ep / 7.5))));
        const valAcc    = Math.min(89, Math.round(32 + 57 * (1 - Math.exp(-ep / 7.8))));
        return {{ trainLoss, valLoss, trainAcc, valAcc }};
      }}
      if (scen === 'over') {{
        // Model terlalu hafal: Train Loss jatuh dekat 0, Val Loss balik naik tajam (bentuk U)!
        const trainLoss = 0.04 + 1.62 * Math.exp(-ep / 6.2);
        const valBase   = 0.32 + 1.38 * Math.exp(-ep / 5.6);
        const overBump  = ep > 11 ? 0.0034 * Math.pow(ep - 11, 1.92) : 0;
        const valLoss   = Math.min(1.80, valBase + overBump);
        const trainAcc  = Math.min(99, Math.round(36 + 63 * (1 - Math.exp(-ep / 6.5))));
        let valAcc      = Math.round(34 + 50 * (1 - Math.exp(-ep / 5.5)));
        if (ep > 11) valAcc = Math.max(54, valAcc - Math.round((ep - 11) * 1.55));
        return {{ trainLoss, valLoss, trainAcc, valAcc }};
      }}
      // 'all': Alur nyambung 1..50 (Underfit -> Good Fit -> Overfit)
      const trainLoss = 1.65 * Math.exp(-ep / 9.5) + 0.04;
      const valBase   = 1.68 * Math.exp(-ep / 10.2) + 0.24;
      const overBump  = ep > 20 ? 0.00145 * Math.pow(ep - 20, 1.92) : 0;
      const valLoss   = Math.min(1.85, valBase + overBump);
      const trainAcc  = Math.min(99, Math.round(34 + 65 * (1 - Math.exp(-ep / 10.5))));
      let valAcc      = Math.round(32 + 57 * (1 - Math.exp(-ep / 9.5)));
      if (ep > 22) valAcc = Math.max(54, valAcc - Math.round((ep - 22) * 1.15));
      return {{ trainLoss, valLoss, trainAcc, valAcc }};
    }}

    function _activeFitZone() {{
      if (fitScenario !== 'all') return fitScenario;
      if (fitEpoch <= 8) return 'under';
      if (fitEpoch <= 25) return 'good';
      return 'over';
    }}

    function renderFitCanvas() {{
      const canvas = document.getElementById('fit-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, W, H);

      const maxEp = _fitMaxEp();
      fitEpoch = Math.max(1, Math.min(maxEp, fitEpoch));
      const zone = _activeFitZone();
      const stats = _fitCurvesFor(fitScenario, fitEpoch);

      // Update tabs, play label, slider & badges
      document.querySelectorAll('#fit-tabs button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.fit !== fitScenario);
      }});
      const btn = document.getElementById('fit-btn-play');
      if (btn && !fitTimer) btn.textContent = _fitPlayLabel();

      const sl = document.getElementById('fit-ep-slider');
      if (sl) {{
        sl.max = String(maxEp);
        sl.value = String(fitEpoch);
        sl.style.accentColor = zone === 'good' ? '#34A853' : (zone === 'under' ? '#EA4335' : '#E37400');
      }}
      const ev = document.getElementById('fit-ep-val');
      if (ev) {{
        ev.textContent = `${{fitEpoch}}/${{maxEp}}`;
        ev.style.color = zone === 'good' ? '#137333' : (zone === 'under' ? '#C5221F' : '#B06000');
        ev.style.background = zone === 'good' ? '#E6F4EA' : (zone === 'under' ? '#FCE8E6' : '#FEF7E0');
      }}

      const zt = document.getElementById('fit-zone-title');
      if (zt) {{
        if (fitScenario === 'under') {{
          zt.textContent = `Mode Underfitting (Epoch ${{fitEpoch}}/30) — Model Terlalu Sederhana`;
          zt.style.color = '#C5221F';
        }} else if (fitScenario === 'good') {{
          zt.textContent = `Mode Good Fit ✓ (Epoch ${{fitEpoch}}/30) — Belajar Seimbang!`;
          zt.style.color = '#137333';
        }} else if (fitScenario === 'over') {{
          zt.textContent = `Mode Overfitting ⚠️ (Epoch ${{fitEpoch}}/30) — Menghafal Data Latih!`;
          zt.style.color = '#B06000';
        }} else {{
          if (zone === 'under') {{ zt.textContent = `Alur Nyambung · Zona Underfit (Epoch ${{fitEpoch}}/50)`; zt.style.color = '#C5221F'; }}
          else if (zone === 'good') {{ zt.textContent = `Alur Nyambung · Zona Good Fit ✓ (Epoch ${{fitEpoch}}/50)`; zt.style.color = '#137333'; }}
          else {{ zt.textContent = `Alur Nyambung · Zona Overfit ⚠️ (Epoch ${{fitEpoch}}/50)`; zt.style.color = '#B06000'; }}
        }}
      }}

      const accTr = document.getElementById('fit-acc-tr');
      const accVal = document.getElementById('fit-acc-val');
      if (accTr) accTr.textContent = `${{stats.trainAcc}}%`;
      if (accVal) {{
        const valGood = (zone === 'good') || (fitScenario === 'over' && fitEpoch <= 11);
        accVal.textContent = valGood ? `${{stats.valAcc}}% ✓` : `${{stats.valAcc}}% ⚠️`;
        accVal.style.color = valGood ? '#137333' : '#C5221F';
      }}

      const call = document.getElementById('fit-callout');
      if (call) {{
        if (fitScenario === 'under' || (fitScenario === 'all' && zone === 'under')) {{
          call.className = 'callout red';
          call.innerHTML = fitScenario === 'under'
            ? `<strong>Underfitting (Mandiri · Epoch ${{fitEpoch}}/30):</strong> Model terlalu sederhana — meski dilatih 30 epoch, garis tetap kaku &amp; <strong>Train (${{stats.trainAcc}}%) maupun Val (${{stats.valAcc}}%) sama-sama rendah</strong>!`
            : `<strong>Zona Underfitting (Epoch ${{fitEpoch}}):</strong> Model baru mulai belajar sehingga garis pola masih datar — salah di latihan (${{stats.trainAcc}}%) maupun foto baru (${{stats.valAcc}}%)!`;
        }} else if (fitScenario === 'good' || (fitScenario === 'all' && zone === 'good')) {{
          call.className = 'callout green';
          call.innerHTML = `<strong>Good Fit / Generalization ✓:</strong> Train Loss &amp; Val Loss <strong>turun bersama &amp; tetap rapat</strong> — akurat di latihan (<code>${{stats.trainAcc}}%</code>) <strong>DAN</strong> foto baru (<code>${{stats.valAcc}}%</code>)! Di <strong>P05</strong> kita pisah <code>train/val/test</code>.`;
        }} else {{
          call.className = 'callout yellow';
          call.innerHTML = `<strong>Overfitting (Hafal Latar!):</strong> Train Loss jatuh ke <code>${{stats.trainLoss.toFixed(2)}}</code> (<code>${{stats.trainAcc}}%</code>), tapi <strong>Val Loss berbalik naik ke <code>${{stats.valLoss.toFixed(2)}}</code> &amp; foto baru anjlok (<code>${{stats.valAcc}}%</code>)</strong>! Solusi: <em>Group Split</em> (P05) &amp; <em>CNN</em> (P03).`;
        }}
      }}

      // --- LEFT SUB-CHART: PATTERN FIT ---
      const lx0 = 14, ly0 = 22, lw = 224, lh = 220;
      ctx.fillStyle = '#FAFBFC'; ctx.strokeStyle = '#E0E3E7'; ctx.lineWidth = 1.1;
      ctx.beginPath(); ctx.roundRect(lx0, ly0, lw, lh, 8); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#3C4043'; ctx.font = '700 10px Poppins, Arial'; ctx.textAlign = 'center';
      ctx.fillText('Pola yang Dipelajari Model', lx0 + lw / 2, 13);

      const trPts = [
        [0.10, 0.25], [0.22, 0.50], [0.34, 0.62], [0.46, 0.78],
        [0.58, 0.66], [0.70, 0.56], [0.82, 0.34], [0.91, 0.28],
      ];
      const valPts = [[0.28, 0.58], [0.52, 0.72], [0.76, 0.44]];
      const toLX = (u) => lx0 + 12 + u * (lw - 24);
      const toLY = (v) => ly0 + lh - 14 - v * (lh - 28);

      // Compute morphed pattern curve independently per scenario!
      let alphaGood = 0, alphaOver = 0, tiltUnder = 0;
      if (fitScenario === 'under') {{
        // Stays linear! Only tilts slightly from horizontal to best-fit straight line
        tiltUnder = Math.min(1, fitEpoch / 12);
        alphaGood = 0.08 * Math.min(1, fitEpoch / 25);
        alphaOver = 0;
      }} else if (fitScenario === 'good') {{
        // Smoothly bends from straight line -> clean parabola (NEVER zig-zags!)
        alphaGood = Math.min(1, Math.max(0, (fitEpoch - 1) / 14));
        alphaOver = 0;
      }} else if (fitScenario === 'over') {{
        // Bends quickly by Epoch 10, then zig-zags aggressively from Epoch 11 -> 30!
        alphaGood = Math.min(1, Math.max(0, (fitEpoch - 1) / 9));
        alphaOver = Math.min(1.15, Math.max(0, (fitEpoch - 10) / 16));
      }} else {{
        alphaGood = Math.min(1, Math.max(0, (fitEpoch - 2) / 14));
        alphaOver = Math.min(1, Math.max(0, (fitEpoch - 22) / 22));
      }}

      const curveCol = zone === 'good' ? '#34A853' : (zone === 'under' ? '#EA4335' : '#E37400');
      ctx.strokeStyle = curveCol; ctx.lineWidth = 2.6;
      ctx.beginPath();
      for (let i = 0; i <= 100; i++) {{
        const u = i / 100;
        const yUnder = 0.47 + (0.04 + 0.06 * tiltUnder) * (u - 0.5);
        const yGood = 0.74 - 2.35 * Math.pow(u - 0.49, 2);
        const wiggle = 0.16 * Math.sin((u - 0.08) * Math.PI * 6.5) * Math.sin(u * Math.PI);
        const yMix = yUnder * (1 - alphaGood) + yGood * alphaGood + alphaOver * wiggle;
        const px = toLX(u), py = toLY(Math.max(0.05, Math.min(0.95, yMix)));
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }}
      ctx.stroke();

      trPts.forEach(([u, v]) => {{
        ctx.fillStyle = '#4285F4'; ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.arc(toLX(u), toLY(v), 4.2, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      }});
      valPts.forEach(([u, v]) => {{
        const cx = toLX(u), cy = toLY(v), r = 5.2;
        ctx.fillStyle = '#137333'; ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(cx, cy - r); ctx.lineTo(cx + r, cy); ctx.lineTo(cx, cy + r); ctx.lineTo(cx - r, cy);
        ctx.closePath(); ctx.fill(); ctx.stroke();
      }});

      ctx.fillStyle = '#5F6368'; ctx.font = '600 8.8px Roboto, Arial'; ctx.textAlign = 'center';
      ctx.fillText(
        zone === 'under' ? 'Garis tetap kaku (tidak bisa melengkung)'
          : (zone === 'good' ? 'Kurva halus cocok di ● & ★!' : (alphaOver < 0.15 ? 'Mulai melengkung, siap menghafal...' : 'Zig-zag hafal ● tapi meleset di ★!')),
        lx0 + lw / 2, H - 7
      );

      // --- RIGHT SUB-CHART: TRAIN vs VAL LOSS ---
      const rx0 = 268, ry0 = 22, rw = 238, rh = 220;
      ctx.fillStyle = '#FAFBFC'; ctx.strokeStyle = '#E0E3E7'; ctx.lineWidth = 1.1;
      ctx.beginPath(); ctx.roundRect(rx0, ry0, rw, rh, 8); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#3C4043'; ctx.font = '700 10px Poppins, Arial'; ctx.textAlign = 'center';
      ctx.fillText('Kurva Train Loss vs Val Loss', rx0 + rw / 2, 13);

      const toRX = (ep) => rx0 + 16 + ((ep - 1) / (maxEp - 1)) * (rw - 26);
      const toRY = (ls) => ry0 + rh - 14 - (Math.min(1.9, ls) / 1.9) * (rh - 26);

      // Subtle background tint tailored to scenario!
      if (fitScenario === 'under') {{
        ctx.fillStyle = 'rgba(234,67,53,0.06)';
        ctx.fillRect(rx0 + 2, ry0 + 2, rw - 4, toRY(0.95) - ry0);
      }} else if (fitScenario === 'good') {{
        ctx.fillStyle = 'rgba(52,168,83,0.08)';
        ctx.fillRect(toRX(12), ry0 + 2, toRX(30) - toRX(12), rh - 4);
      }} else if (fitScenario === 'over') {{
        ctx.fillStyle = 'rgba(52,168,83,0.07)';
        ctx.fillRect(toRX(7), ry0 + 2, toRX(13) - toRX(7), rh - 4);
        ctx.fillStyle = 'rgba(234,67,53,0.09)';
        ctx.fillRect(toRX(13), ry0 + 2, toRX(30) - toRX(13), rh - 4);
      }} else {{
        ctx.fillStyle = 'rgba(52,168,83,0.10)';
        ctx.fillRect(toRX(12), ry0 + 2, toRX(25) - toRX(12), rh - 4);
        ctx.fillStyle = 'rgba(234,67,53,0.08)';
        ctx.fillRect(toRX(25), ry0 + 2, toRX(50) - toRX(25), rh - 4);
      }}

      // Faint full preview curves
      ['trainLoss', 'valLoss'].forEach((key, ki) => {{
        ctx.strokeStyle = ki === 0 ? 'rgba(66,133,244,0.20)' : 'rgba(234,67,53,0.20)';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        for (let e = 1; e <= maxEp; e++) {{
          const px = toRX(e), py = toRY(_fitCurvesFor(fitScenario, e)[key]);
          if (e === 1) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }}
        ctx.stroke();
      }});

      // Active solid curves up to fitEpoch
      ['trainLoss', 'valLoss'].forEach((key, ki) => {{
        ctx.strokeStyle = ki === 0 ? '#1A73E8' : '#EA4335';
        ctx.lineWidth = 2.6;
        ctx.beginPath();
        for (let e = 1; e <= fitEpoch; e++) {{
          const px = toRX(e), py = toRY(_fitCurvesFor(fitScenario, e)[key]);
          if (e === 1) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }}
        ctx.stroke();
      }});

      // Vertical Epoch cursor + active dots
      const cx = toRX(fitEpoch);
      ctx.setLineDash([3, 3]); ctx.strokeStyle = '#5F6368'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(cx, ry0 + 4); ctx.lineTo(cx, ry0 + rh - 4); ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = '#1A73E8'; ctx.beginPath(); ctx.arc(cx, toRY(stats.trainLoss), 4.6, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#EA4335'; ctx.beginPath(); ctx.arc(cx, toRY(stats.valLoss), 4.6, 0, Math.PI * 2); ctx.fill();

      // Crisp non-overlapping legend pill at top-right (or bottom-left when Val is high on right!)
      const legY = (fitScenario === 'over' && fitEpoch > 20) ? (ry0 + rh - 38) : (ry0 + 6);
      const legX = (fitScenario === 'over' && fitEpoch > 20) ? (rx0 + 8) : (rx0 + rw - 88);
      ctx.fillStyle = 'rgba(255,255,255,0.94)'; ctx.strokeStyle = '#E0E3E7'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.roundRect(legX, legY, 82, 30, 6); ctx.fill(); ctx.stroke();
      ctx.font = '700 8.8px Roboto Mono'; ctx.textAlign = 'left';
      ctx.fillStyle = '#1A73E8'; ctx.fillText(`Train:${{stats.trainLoss.toFixed(2)}}`, legX + 6, legY + 12);
      ctx.fillStyle = '#EA4335'; ctx.fillText(`Val:  ${{stats.valLoss.toFixed(2)}}`, legX + 6, legY + 24);

      ctx.fillStyle = '#5F6368'; ctx.font = '600 8.8px Roboto, Arial'; ctx.textAlign = 'center';
      ctx.fillText(`Epoch 1 ──────────→ Epoch ${{maxEp}}`, rx0 + rw / 2, H - 7);
    }}

    function setFitScenario(scen) {{
      _stopFitPlay();
      fitScenario = scen;
      fitEpoch = scen === 'all' ? 18 : 30;
      renderFitCanvas();
    }}

    function setFitEpoch(v) {{
      _stopFitPlay();
      fitEpoch = Math.max(1, Math.min(_fitMaxEp(), Number(v)));
      renderFitCanvas();
    }}

    function resetFitSim() {{
      _stopFitPlay();
      fitEpoch = 1;
      renderFitCanvas();
    }}

    function toggleFitPlay() {{
      if (fitTimer) {{ _stopFitPlay(); return; }}
      const maxEp = _fitMaxEp();
      if (fitEpoch >= maxEp) fitEpoch = 1;
      const btn = document.getElementById('fit-btn-play');
      if (btn) btn.textContent = '■ Stop';
      renderFitCanvas();
      fitTimer = setInterval(() => {{
        if (fitEpoch >= maxEp) {{ _stopFitPlay(); return; }}
        fitEpoch += 1;
        renderFitCanvas();
      }}, fitScenario === 'all' ? 95 : 125);
    }}

    function setFitPdfState(st) {{
      _stopBsPlay(); _stopFitPlay();
      if (st === 'under') {{
        bsSize = 16; bsDone = 3; fitScenario = 'under'; fitEpoch = 30;
      }} else if (st === 'good') {{
        bsSize = 16; bsDone = Math.ceil(BS_TOTAL / 16); fitScenario = 'good'; fitEpoch = 30;
      }} else {{
        bsSize = 143; bsDone = 1; fitScenario = 'over'; fitEpoch = 30;
      }}
      renderBsUI();
      renderFitCanvas();
    }}

    renderBsUI();
    renderFitCanvas();

    // =========================================================================
    // SIMULATOR #12 (Slide 43): Peta Evolusi Arsitektur CV
    // =========================================================================
    const ARCH_CFG = {{
      mlp: {{
        pill: '1. MLP · FULLY CONNECTED', pillCls: 'pill red', barCls: 'card-top-bar bar-red', callCls: 'callout red',
        title: 'Semua Piksel Diluruskan & Disambung Penuh',
        body: '<ul><li>Cocok untuk data tabel (angka umur, harga, skor), tetapi kewalahan untuk foto beresolusi besar.</li><li>Foto <code>224×224×3</code> menghasilkan <strong>19,27 juta parameter</strong> hanya di 1 hidden layer 128 neuron!</li></ul>',
        call: '<strong>Peran di kelas:</strong> Pondasi konsep yang kita bangun langsung di Notebook P02 hari ini.',
      }},
      cnn: {{
        pill: '2. CNN (LENET / VGG) · FILTER 2D', pillCls: 'pill blue', barCls: 'card-top-bar bar-blue', callCls: 'callout',
        title: 'Membaca Gambar 2D dengan Filter Geser (Konvolusi)',
        body: '<ul><li>Alih-alih meluruskan foto, <strong>CNN</strong> menggeser filter kecil (mis. <code>3×3</code>) di seluruh gambar 2D.</li><li>Sangat hemat bobot (<em>parameter sharing</em>) dan tetap mengenali Elsa walau posisinya bergeser!</li></ul>',
        call: '<strong>Peran di kelas:</strong> Kita bedah total cara kerja kernel, stride, padding, dan pooling di <strong>P03</strong>!',
      }},
      resnet: {{
        pill: '3. RESNET · SKIP CONNECTION', pillCls: 'pill yellow', barCls: 'card-top-bar bar-yellow', callCls: 'callout yellow',
        title: 'Menambahkan Skip Connection agar Jaringan Bisa Sangat Dalam',
        body: '<ul><li>Dulu, menumpuk terlalu banyak layer CNN (mis. 50+ layer) justru membuat sinyal belajar melemah.</li><li><strong>ResNet</strong> menambahkan <em>residual / skip connection</em> sehingga jaringan 50–152 layer bisa dilatih dengan stabil.</li></ul>',
        call: '<strong>Peran di kelas:</strong> Kita bahas evolusi lengkap &amp; perbandingannya di <strong>P04</strong>.',
      }},
      mobilenet: {{
        pill: '4. MOBILENETV2 · RINGAN & CEPAT ★', pillCls: 'pill green', barCls: 'card-top-bar bar-green', callCls: 'callout green',
        title: 'Arsitektur Efisien untuk Perangkat Mobile & Dataset Kecil',
        body: '<ul><li>Memakai teknik konvolusi hemat komputasi sehingga jumlah parameter &amp; ukuran filenya jauh lebih kecil daripada ResNet50.</li><li>Tersedia bobot siap pakai (<em>pretrained ImageNet</em>) di Keras untuk <strong>Transfer Learning</strong>.</li></ul>',
        call: '<strong>Pilihan proyek kita:</strong> <em>Backbone</em> utama klasifikasi 5 karakter Disney Frozen pada <strong>P04–P08</strong>!',
      }},
    }};
    function setArchTab(k) {{
      if (!document.getElementById('arch-bar')) return;
      const c = ARCH_CFG[k];
      if (!c) return;
      document.querySelectorAll('#arch-tabs button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.arch !== k);
      }});
      document.getElementById('arch-pill').className = c.pillCls;
      document.getElementById('arch-pill').textContent = c.pill;
      document.getElementById('arch-bar').className = c.barCls;
      document.getElementById('arch-title').textContent = c.title;
      document.getElementById('arch-body').innerHTML = c.body;
      const cl = document.getElementById('arch-callout');
      cl.className = c.callCls;
      cl.innerHTML = c.call;
    }}
    setArchTab('mobilenet');

    // =========================================================================
    // INTERACTIVE HANDLERS: SLIDE 31 (KUIS), SLIDE 32 (KAMUS), SLIDE 36-41 (COPY)
    // =========================================================================
    const _qzScoreMap = {{}};
    function _updateQuizScore() {{
      const pts = Object.values(_qzScoreMap).filter(Boolean).length;
      const attempted = Object.keys(_qzScoreMap).length;
      const pill = document.getElementById('qz-score-pill');
      if (pill) {{
        pill.textContent = `Skor: ${{pts}} / 5`;
        pill.style.background = pts === 5 ? '#E6F4EA' : '#E8F0FE';
        pill.style.color = pts === 5 ? '#137333' : '#1A73E8';
        pill.style.borderColor = pts === 5 ? '#A8DAB5' : '#C6DAFC';
      }}
      const badge = document.getElementById('qz-done-badge');
      if (badge) {{
        if (pts === 5) {{
          badge.textContent = '🎉 5 / 5 Sempurna! Siap lanjut ke Hands-On!';
          badge.style.background = '#34A853'; badge.style.color = '#FFFFFF';
        }} else if (attempted > 0) {{
          badge.textContent = `Terjawab benar: ${{pts}} dari 5 soal — klik sisa opsi untuk cek!`;
          badge.style.background = '#FFFFFF'; badge.style.color = '#137333';
        }} else {{
          badge.textContent = 'Klik opsi A/B/C di tiap kartu untuk uji cepat!';
          badge.style.background = '#FFFFFF'; badge.style.color = '#137333';
        }}
      }}
    }}
    function pickMiniQuiz(btn, qid) {{
      if (!btn) return;
      const isOk = btn.dataset.correct === 'true';
      document.querySelectorAll(`.qz-opt[data-q="${{qid}}"]`).forEach((b) => {{
        b.classList.remove('ok', 'bad');
      }});
      btn.classList.add(isOk ? 'ok' : 'bad');
      _qzScoreMap[qid] = isOk;
      _updateQuizScore();
    }}
    function revealAllQuiz(show) {{
      ['q1', 'q2', 'q3', 'q4', 'q5'].forEach((qid) => {{
        const ans = document.getElementById(qid);
        if (ans) ans.classList.toggle('shown', !!show);
        const btn = ans ? ans.parentElement.querySelector('.qz-mini-btn') : null;
        if (btn) btn.textContent = show ? 'Sembunyikan Penjelasan' : 'Lihat Penjelasan';
        if (show) {{
          document.querySelectorAll(`.qz-opt[data-q="${{qid}}"][data-correct="true"]`).forEach((b) => b.classList.add('ok'));
          _qzScoreMap[qid] = true;
        }}
      }});
      _updateQuizScore();
    }}
    function resetMiniQuiz() {{
      Object.keys(_qzScoreMap).forEach((k) => delete _qzScoreMap[k]);
      document.querySelectorAll('.qz-opt').forEach((b) => b.classList.remove('ok', 'bad'));
      ['q1', 'q2', 'q3', 'q4', 'q5'].forEach((qid) => {{
        const ans = document.getElementById(qid);
        if (ans) ans.classList.remove('shown');
        const btn = ans ? ans.parentElement.querySelector('.qz-mini-btn') : null;
        if (btn) btn.textContent = 'Lihat Penjelasan';
      }});
      _updateQuizScore();
    }}

    // =========================================================================
    // SIMULATOR SLIDE 24: INTERACTIVE DENSE (FULLY CONNECTED) & PARAMETER CALC
    // =========================================================================
    const DENSE_SCALES = {{
      8:   {{ dim: 8,   nIn: 192,     inStr: '192',     dimTxt: '(8×8×3)',     wStr: '960',     totStr: '965',     label: 'Mini 8×8×3',      ctx: 'Tahap 2.1 Hands-On' }},
      64:  {{ dim: 64,  nIn: 12288,   inStr: '12.288',  dimTxt: '(64×64×3)',   wStr: '61.440',  totStr: '61.445',  label: 'Hands-On 64×64×3', ctx: 'model.summary() Keras' }},
      224: {{ dim: 224, nIn: 150528,  inStr: '150.528', dimTxt: '(224×224×3)', wStr: '752.640', totStr: '752.645', label: 'Penuh 224×224×3', ctx: 'Simulasi Penuh Slide 32' }},
    }};
    const DENSE_INPUTS = [
      {{ id: 0, lbl: 'x₁', sub: 'Piksel 1 (R)', col: '#EA4335', y: 54 }},
      {{ id: 1, lbl: 'x₂', sub: 'Piksel 1 (G)', col: '#34A853', y: 92 }},
      {{ id: 2, lbl: 'x₃', sub: 'Piksel 1 (B)', col: '#4285F4', y: 130 }},
      {{ id: 3, lbl: 'xₙ', sub: 'Piksel akhir', col: '#1A73E8', y: 192 }},
    ];
    const DENSE_OUTPUTS = [
      {{ id: 0, lbl: 'y₁ Anna',     b: '+b₁', col: '#4285F4', y: 48 }},
      {{ id: 1, lbl: 'y₂ Elsa',     b: '+b₂', col: '#34A853', y: 86 }},
      {{ id: 2, lbl: 'y₃ Kristoff', b: '+b₃', col: '#E37400', y: 124 }},
      {{ id: 3, lbl: 'y₄ Olaf',     b: '+b₄', col: '#EA4335', y: 162 }},
      {{ id: 4, lbl: 'y₅ Sven',     b: '+b₅', col: '#5F6368', y: 200 }},
    ];
    let _denseScale = 224;
    let _denseStep = 5;        // 0=idle, 1=x1(5W), 2=x1..x2(10W), 3=x1..x3(15W), 4=all W, 5=all W + 5 Bias!
    let _denseSelIn = -1;      // direct click on input neuron 0..3
    let _denseSelOut = -1;     // direct click on output neuron 0..4
    let _denseTimer = null;
    let _denseRaf = null;
    let _densePulseT = 0;

    function _setDenseSyncCards(activeIdx) {{
      const colors = ['', 'sync-blue', 'sync-yellow', 'sync-green'];
      [1, 2, 3].forEach((k) => {{
        const el = document.getElementById('dense-sc-' + k);
        if (!el) return;
        el.classList.remove('sync-on', 'sync-dim', 'sync-blue', 'sync-yellow', 'sync-green');
        if (activeIdx === 0) return;
        if (k === activeIdx) {{
          el.classList.add('sync-on', colors[k]);
        }} else {{
          el.classList.add('sync-dim');
        }}
      }});
    }}

    function _cubicPt(x0, y0, cx1, cy1, cx2, cy2, x1, y1, t) {{
      const u = 1 - t;
      const tt = t * t, uu = u * u, uuu = uu * u, ttt = tt * t;
      return {{
        x: uuu * x0 + 3 * uu * t * cx1 + 3 * u * tt * cx2 + ttt * x1,
        y: uuu * y0 + 3 * uu * t * cy1 + 3 * u * tt * cy2 + ttt * y1,
      }};
    }}

    function renderDenseSvg(pulsePhase = 0.55) {{
      const svg = document.getElementById('dense-svg');
      if (!svg) return;
      const cfg = DENSE_SCALES[_denseScale];
      const inX = 166, outX = 434;

      // Determine active input / output indices & center pill text
      const activeInputs = new Set();
      const activeOutputs = new Set();
      let highlightBias = false;
      let wireMode = 'all'; // 'none' | 'in' | 'out' | 'all'

      if (_denseSelIn >= 0) {{
        activeInputs.add(_denseSelIn);
        [0, 1, 2, 3, 4].forEach((o) => activeOutputs.add(o));
        wireMode = 'in';
      }} else if (_denseSelOut >= 0) {{
        [0, 1, 2, 3].forEach((i) => activeInputs.add(i));
        activeOutputs.add(_denseSelOut);
        highlightBias = true;
        wireMode = 'out';
      }} else if (_denseStep === 0) {{
        wireMode = 'none';
      }} else if (_denseStep === 1) {{
        activeInputs.add(0);
        [0, 1, 2, 3, 4].forEach((o) => activeOutputs.add(o));
        wireMode = 'in';
      }} else if (_denseStep === 2) {{
        activeInputs.add(0); activeInputs.add(1);
        [0, 1, 2, 3, 4].forEach((o) => activeOutputs.add(o));
        wireMode = 'in';
      }} else if (_denseStep === 3) {{
        activeInputs.add(0); activeInputs.add(1); activeInputs.add(2);
        [0, 1, 2, 3, 4].forEach((o) => activeOutputs.add(o));
        wireMode = 'in';
      }} else if (_denseStep === 4) {{
        [0, 1, 2, 3].forEach((i) => activeInputs.add(i));
        [0, 1, 2, 3, 4].forEach((o) => activeOutputs.add(o));
        wireMode = 'all';
      }} else {{
        [0, 1, 2, 3].forEach((i) => activeInputs.add(i));
        [0, 1, 2, 3, 4].forEach((o) => activeOutputs.add(o));
        highlightBias = true;
        wireMode = 'all';
      }}

      let h = '';
      // 1. Left Input Layer Container
      h += `<rect x="6" y="8" width="160" height="216" rx="13" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>`;
      h += `<text x="86" y="27" text-anchor="middle" font-family="Poppins, Arial" font-size="10.5" font-weight="800" fill="#1A73E8">INPUT LAYER</text>`;

      // Input Neurons (clickable!)
      DENSE_INPUTS.forEach((inp, idx) => {{
        const isAct = activeInputs.has(idx);
        const isNewest = (_denseSelIn === idx) || (_denseSelIn < 0 && _denseSelOut < 0 && _denseStep === idx + 1);
        const bg = isNewest ? '#FFFFFF' : (isAct ? '#F8FBFF' : 'rgba(255,255,255,0.72)');
        const stroke = isNewest ? inp.col : (isAct ? '#8AB4F8' : '#D2E3FC');
        const sw = isNewest ? 2.2 : 1.2;
        h += `<g style="cursor:pointer;" onclick="clickDenseInput(${{idx}})">`;
        h += `<rect x="16" y="${{inp.y - 14}}" width="140" height="28" rx="9" fill="${{bg}}" stroke="${{stroke}}" stroke-width="${{sw}}"/>`;
        h += `<circle cx="34" cy="${{inp.y}}" r="10.5" fill="${{inp.col}}" opacity="${{isAct || wireMode === 'none' ? 1 : 0.45}}"/>`;
        h += `<text x="34" y="${{inp.y + 3.5}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.6" font-weight="700" fill="#FFFFFF">${{inp.lbl}}</text>`;
        h += `<text x="51" y="${{inp.y - 1}}" font-family="Roboto, Arial" font-size="8.6" font-weight="700" fill="#202124">${{inp.sub}}</text>`;
        h += `<text x="51" y="${{inp.y + 9.5}}" font-family="Roboto Mono, monospace" font-size="7.6" fill="#5F6368">${{isAct ? '5 kabel W →' : 'klik untuk uji'}}</text>`;
        h += `</g>`;
      }});

      // Ellipsis pill showing remaining input neurons
      const remStr = (cfg.nIn - 4).toLocaleString('id-ID');
      h += `<rect x="28" y="151" width="116" height="19" rx="9" fill="#FFFFFF" stroke="#C6DAFC" stroke-width="1"/>`;
      h += `<text x="86" y="164" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.4" font-weight="700" fill="#1A73E8">⋮ +${{remStr}} neuron</text>`;
      h += `<text x="86" y="218" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.8" font-weight="800" fill="#1A73E8">Total: ${{cfg.inStr}} ${{cfg.dimTxt}}</text>`;

      // 2. Fully Connected Cables (background inactive wires first, then active glowing wires + dots!)
      const activeCables = [];
      DENSE_INPUTS.forEach((inp, iIdx) => {{
        DENSE_OUTPUTS.forEach((outp, oIdx) => {{
          const on = activeInputs.has(iIdx) && activeOutputs.has(oIdx);
          const d = `M ${{inX}} ${{inp.y}} C ${{inX + 86}} ${{inp.y}}, ${{outX - 86}} ${{outp.y}}, ${{outX}} ${{outp.y}}`;
          if (!on) {{
            h += `<path d="${{d}}" fill="none" stroke="#CFD4DA" stroke-width="1.1" opacity="0.5"/>`;
          }} else {{
            const isHero = (_denseSelIn === iIdx) || (_denseSelOut === oIdx) || (_denseSelIn < 0 && _denseSelOut < 0 && _denseStep >= 1 && _denseStep <= 3 && iIdx === _denseStep - 1);
            const col = _denseSelOut >= 0 ? outp.col : (isHero ? inp.col : '#4285F4');
            activeCables.push({{ inp, outp, d, col, isHero }});
          }}
        }});
      }});

      activeCables.forEach((cb, k) => {{
        h += `<path d="${{cb.d}}" fill="none" stroke="${{cb.col}}" stroke-width="${{cb.isHero ? 2.4 : 1.55}}" opacity="${{cb.isHero ? 0.95 : 0.62}}"/>`;
        // Traveling pulse dot along active hero or full cables
        if (cb.isHero || _denseStep >= 4) {{
          const t = (pulsePhase + (k % 5) * 0.14) % 1.0;
          const pt = _cubicPt(inX, cb.inp.y, inX + 86, cb.inp.y, outX - 86, cb.outp.y, outX, cb.outp.y, t);
          h += `<circle cx="${{pt.x.toFixed(1)}}" cy="${{pt.y.toFixed(1)}}" r="${{cb.isHero ? 3.8 : 2.6}}" fill="${{cb.col}}" stroke="#FFFFFF" stroke-width="1"/>`;
        }}
      }});

      // 3. Center Counter Badge (KABEL DENSE W)
      let boxTitle = 'KABEL DENSE (W)';
      let boxMain = `${{cfg.wStr}} W`;
      let boxSub = '+ 5 Bias (1 per output)';
      let boxBg = '#FEF7E0', boxStroke = '#FBBC04', boxTxt = '#B06000';

      if (_denseSelIn >= 0) {{
        boxTitle = `1 NEURON (${{DENSE_INPUTS[_denseSelIn].lbl}})`;
        boxMain = '5 Kabel W';
        boxSub = 'tersambung ke SEMUA 5 output';
        boxBg = '#E8F0FE'; boxStroke = '#4285F4'; boxTxt = '#1A73E8';
      }} else if (_denseSelOut >= 0) {{
        const oname = DENSE_OUTPUTS[_denseSelOut].lbl;
        const perOut = (cfg.nIn + 1).toLocaleString('id-ID');
        boxTitle = `KHUSUS ${{oname.toUpperCase()}}`;
        boxMain = `${{cfg.inStr}} W + 1 b`;
        boxSub = `= ${{perOut}} param utk 1 kelas`;
        boxBg = '#E6F4EA'; boxStroke = '#34A853'; boxTxt = '#137333';
      }} else if (_denseStep === 0) {{
        boxTitle = 'SIAP SIMULASI';
        boxMain = '0 Kabel Aktif';
        boxSub = 'Klik ▶ Play atau klik neuron!';
        boxBg = '#F8F9FA'; boxStroke = '#DADCE0'; boxTxt = '#5F6368';
      }} else if (_denseStep >= 1 && _denseStep <= 3) {{
        boxTitle = `${{_denseStep}} NEURON × 5 OUTPUT`;
        boxMain = `${{_denseStep * 5}} Kabel W`;
        boxSub = `tiap +1 input menambah +5 W`;
        boxBg = '#E8F0FE'; boxStroke = '#4285F4'; boxTxt = '#1A73E8';
      }} else if (_denseStep === 4) {{
        boxTitle = `${{cfg.inStr}} × 5 OUTPUT`;
        boxMain = `${{cfg.wStr}} W`;
        boxSub = 'seluruh kabel bobot tersambung!';
        boxBg = '#FEF7E0'; boxStroke = '#FBBC04'; boxTxt = '#B06000';
      }} else {{
        boxTitle = 'TOTAL PARAMETER (W + b)';
        boxMain = `${{cfg.totStr}} Param`;
        boxSub = `${{cfg.wStr}} W  +  5 Bias`;
        boxBg = '#E6F4EA'; boxStroke = '#34A853'; boxTxt = '#137333';
      }}

      h += `<rect x="218" y="80" width="164" height="72" rx="13" fill="${{boxBg}}" stroke="${{boxStroke}}" stroke-width="2.2"/>`;
      h += `<text x="300" y="99" text-anchor="middle" font-family="Poppins, Arial" font-size="9.2" font-weight="800" fill="${{boxTxt}}">${{boxTitle}}</text>`;
      h += `<text x="300" y="121" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="14" font-weight="800" fill="#202124">${{boxMain}}</text>`;
      h += `<text x="300" y="139" text-anchor="middle" font-family="Roboto, Arial" font-size="8.8" font-weight="600" fill="#5F6368">${{boxSub}}</text>`;

      // 4. Right Output Layer Container (Dense(5))
      h += `<rect x="434" y="8" width="180" height="216" rx="13" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/>`;
      h += `<text x="524" y="27" text-anchor="middle" font-family="Poppins, Arial" font-size="10.2" font-weight="800" fill="#137333">OUTPUT · Dense(5)</text>`;

      DENSE_OUTPUTS.forEach((outp, oIdx) => {{
        const isOutAct = activeOutputs.has(oIdx);
        const isBiasOn = highlightBias && (_denseSelOut < 0 || _denseSelOut === oIdx);
        const isClicked = _denseSelOut === oIdx;
        const cardStroke = isClicked ? outp.col : (isOutAct ? '#34A853' : '#A8DAB5');
        const cardSw = isClicked ? 2.4 : (isOutAct ? 1.5 : 1.0);
        h += `<g style="cursor:pointer;" onclick="clickDenseOutput(${{oIdx}})">`;
        h += `<rect x="446" y="${{outp.y - 14}}" width="156" height="28" rx="8" fill="#FFFFFF" stroke="${{cardStroke}}" stroke-width="${{cardSw}}"/>`;
        h += `<circle cx="461" cy="${{outp.y}}" r="6.5" fill="${{outp.col}}" opacity="${{isOutAct || wireMode === 'none' ? 1 : 0.4}}"/>`;
        h += `<text x="473" y="${{outp.y + 3.5}}" font-family="Poppins, Arial" font-size="9.8" font-weight="700" fill="#202124">${{outp.lbl}}</text>`;
        // Bias pill badge
        const bBg = isBiasOn ? '#FEF7E0' : '#F8F9FA';
        const bSt = isBiasOn ? '#FBBC04' : '#E0E3E7';
        const bTx = isBiasOn ? '#B06000' : '#80868B';
        h += `<rect x="556" y="${{outp.y - 9.5}}" width="39" height="19" rx="6" fill="${{bBg}}" stroke="${{bSt}}" stroke-width="${{isBiasOn ? 1.8 : 1}}"/>`;
        h += `<text x="575.5" y="${{outp.y + 3.2}}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="8.6" font-weight="800" fill="${{bTx}}">${{outp.b}}</text>`;
        h += `</g>`;
      }});

      svg.innerHTML = h;
    }}

    function updateDenseUI() {{
      const cfg = DENSE_SCALES[_denseScale];
      // Update top scale tabs & bottom scale cards
      document.querySelectorAll('#dense-scale-tabs button').forEach((b) => {{
        b.classList.toggle('outline', Number(b.dataset.ds) !== _denseScale);
      }});
      [8, 64, 224].forEach((k) => {{
        const c = document.getElementById('dense-card-' + k);
        if (!c) return;
        const on = k === _denseScale;
        const bc = k === 8 ? '#34A853' : (k === 64 ? '#4285F4' : '#EA4335');
        const bg = k === 8 ? '#E6F4EA' : (k === 64 ? '#E8F0FE' : '#FCE8E6');
        c.style.border = on ? `2px solid ${{bc}}` : '1.5px solid #DADCE0';
        c.style.background = on ? bg : '#F8F9FA';
      }});

      const badge = document.getElementById('dense-step-badge');
      const eq = document.getElementById('dense-keras-eq');
      const call = document.getElementById('dense-callout');

      if (_denseSelIn >= 0) {{
        const inp = DENSE_INPUTS[_denseSelIn];
        if (badge) badge.textContent = `Inspeksi Input ${{inp.lbl}} → 5 Output`;
        if (eq) eq.textContent = `1 input (${{inp.lbl}}) × 5 output = 5 kabel Weight (W)`;
        if (call) call.innerHTML = `<strong>Fully Connected!</strong> Neuron <code>${{inp.lbl}}</code> (${{inp.sub}}) mengirim <strong>5 kabel bobot</strong> sekaligus ke Anna, Elsa, Kristoff, Olaf, &amp; Sven!`;
        _setDenseSyncCards(1);
      }} else if (_denseSelOut >= 0) {{
        const outp = DENSE_OUTPUTS[_denseSelOut];
        const tot1 = (cfg.nIn + 1).toLocaleString('id-ID');
        if (badge) badge.textContent = `Inspeksi Output ${{outp.lbl}}`;
        if (eq) eq.textContent = `${{cfg.inStr}} kabel W + 1 Bias (${{outp.b}}) = ${{tot1}} Param`;
        if (call) call.innerHTML = `<strong>Khusus Neuron ${{outp.lbl}}:</strong> Menerima kabel dari <strong>semua ${{cfg.inStr}} piksel input</strong> ditambah <strong>1 Bias (${{outp.b}})</strong> = <code>${{tot1}}</code> parameter!`;
        _setDenseSyncCards(2);
      }} else if (_denseStep === 0) {{
        if (badge) badge.textContent = `Tahap 0/5 · Siap Simulasi`;
        if (eq) eq.textContent = `(${{cfg.inStr}} × 5) + 5 = ${{cfg.totStr}} Param #`;
        if (call) call.innerHTML = `<strong>Klik ▶ Play atau ⏭ +1 Langkah</strong> untuk melihat kabel <code>Dense</code> dirakit neuron demi neuron hingga terbentuk <code>${{cfg.totStr}}</code> parameter!`;
        _setDenseSyncCards(0);
      }} else if (_denseStep >= 1 && _denseStep <= 3) {{
        const inp = DENSE_INPUTS[_denseStep - 1];
        if (badge) badge.textContent = `Tahap ${{_denseStep}}/5 · Sambung ${{inp.lbl}} → 5 Output`;
        if (eq) eq.textContent = `${{_denseStep}} neuron × 5 output = ${{_denseStep * 5}} kabel W (pola n × 5)`;
        if (call) call.innerHTML = `<strong>Tahap ${{_denseStep}} (Fully Connected):</strong> Neuron <code>${{inp.lbl}}</code> menyambungkan <strong>5 kabel baru</strong> ke seluruh 5 kelas Frozen → total sementara <code>${{_denseStep * 5}} W</code>!`;
        _setDenseSyncCards(1);
      }} else if (_denseStep === 4) {{
        if (badge) badge.textContent = `Tahap 4/5 · Semua Kabel Weight (W)`;
        if (eq) eq.textContent = `${{cfg.inStr}} × 5 = ${{cfg.wStr}} Weight (belum + Bias)`;
        if (call) call.innerHTML = `<strong>Tahap 4 (Seluruh Kabel W):</strong> Karena semua <code>${{cfg.inStr}}</code> neuron input tersambung ke 5 output, terbentuk tepat <code>${{cfg.wStr}}</code> bobot <code>W</code>!`;
        _setDenseSyncCards(2);
      }} else {{
        if (badge) badge.textContent = `Tahap 5/5 · Lengkap (+ 5 Bias = ${{cfg.totStr}})`;
        if (eq) eq.textContent = `(${{cfg.inStr}} × 5) + 5 = ${{cfg.totStr}} Param #`;
        if (call) call.innerHTML = `<strong>${{cfg.label}}:</strong> <code>${{cfg.wStr}} Weight + 5 Bias = ${{cfg.totStr}} parameter</code> — cocok 100% dengan <strong>${{cfg.ctx}}</strong>!`;
        _setDenseSyncCards(3);
      }}

      renderDenseSvg(_densePulseT || 0.55);
    }}

    function _stopDensePlay() {{
      if (_denseTimer) {{ clearInterval(_denseTimer); _denseTimer = null; }}
      if (_denseRaf) {{ cancelAnimationFrame(_denseRaf); _denseRaf = null; }}
      const btn = document.getElementById('dense-btn-play');
      if (btn) btn.textContent = '▶ Play';
    }}

    function _startDensePulseLoop() {{
      if (_denseRaf) cancelAnimationFrame(_denseRaf);
      let lastTs = performance.now();
      const tick = (now) => {{
        const dt = Math.min(0.05, (now - lastTs) / 1000);
        lastTs = now;
        _densePulseT = (_densePulseT + dt * 0.72) % 1.0;
        renderDenseSvg(_densePulseT);
        if (_denseTimer) {{
          _denseRaf = requestAnimationFrame(tick);
        }} else {{
          _denseRaf = null;
        }}
      }};
      _denseRaf = requestAnimationFrame(tick);
    }}

    function toggleDensePlay() {{
      if (_denseTimer) {{
        _stopDensePlay();
        return;
      }}
      _denseSelIn = -1; _denseSelOut = -1;
      if (_denseStep >= 5) _denseStep = 0;
      const btn = document.getElementById('dense-btn-play');
      if (btn) btn.textContent = '■ Stop';
      _denseStep = Math.max(1, _denseStep + 1);
      updateDenseUI();
      _denseTimer = setInterval(() => {{
        if (_denseStep >= 5) {{
          _stopDensePlay();
          return;
        }}
        _denseStep += 1;
        updateDenseUI();
      }}, 1500);
      _startDensePulseLoop();
    }}

    function stepDenseSim() {{
      _stopDensePlay();
      _denseSelIn = -1; _denseSelOut = -1;
      _denseStep = (_denseStep >= 5) ? 1 : (_denseStep + 1);
      _densePulseT = 0.52;
      updateDenseUI();
    }}

    function resetDenseSim() {{
      _stopDensePlay();
      _denseSelIn = -1; _denseSelOut = -1;
      _denseStep = 0;
      _densePulseT = 0.52;
      updateDenseUI();
    }}

    function clickDenseInput(idx) {{
      _stopDensePlay();
      _denseSelOut = -1;
      _denseSelIn = (_denseSelIn === idx) ? -1 : idx;
      _densePulseT = 0.55;
      updateDenseUI();
    }}

    function clickDenseOutput(idx) {{
      _stopDensePlay();
      _denseSelIn = -1;
      _denseSelOut = (_denseSelOut === idx) ? -1 : idx;
      _densePulseT = 0.55;
      updateDenseUI();
    }}

    function setDenseScale(dim) {{
      if (!DENSE_SCALES[dim]) return;
      _denseScale = dim;
      if (_denseStep === 0 && _denseSelIn < 0 && _denseSelOut < 0) _denseStep = 5;
      updateDenseUI();
    }}

    function setDensePdfState(st) {{
      _stopDensePlay();
      _denseSelIn = -1; _denseSelOut = -1; _densePulseT = 0.52;
      if (st === 'x1') {{
        _denseScale = 224; _denseStep = 1;
      }} else {{
        _denseScale = 64; _denseStep = 5;
      }}
      updateDenseUI();
    }}
    updateDenseUI();

        let _glossCh = 'all';
    let _glossQuery = '';
    function _applyGlossaryFilter() {{
      const q = (_glossQuery || '').trim().toLowerCase();
      document.querySelectorAll('.dict-row').forEach((row) => {{
        const chOk = _glossCh === 'all' || row.dataset.ch === _glossCh;
        const txt = ((row.dataset.search || '') + ' ' + (row.textContent || '')).toLowerCase();
        const qOk = !q || txt.includes(q);
        row.classList.toggle('ch-dim', !(chOk && qOk));
      }});
    }}
    function filterGlossary(ch, btn) {{
      _glossCh = ch;
      document.querySelectorAll('.gloss-fbtn').forEach((b) => {{
        b.classList.toggle('active', b.dataset.ch === ch);
      }});
      _applyGlossaryFilter();
    }}
    function searchGlossary(val) {{
      _glossQuery = val || '';
      _applyGlossaryFilter();
    }}

    function copyHandsOnCode(btn, codeId) {{
      const el = document.getElementById(codeId);
      if (!el) return;
      const raw = el.innerText || el.textContent || '';
      const done = () => {{
        const orig = btn.textContent;
        btn.textContent = '✓ Tersalin';
        btn.style.borderColor = '#34A853';
        btn.style.color = '#81C995';
        setTimeout(() => {{
          btn.textContent = orig;
          btn.style.borderColor = '#4A4E57';
          btn.style.color = '#E8EAED';
        }}, 1400);
      }};
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(raw).then(done).catch(() => done());
      }} else {{
        const ta = document.createElement('textarea');
        ta.value = raw; document.body.appendChild(ta); ta.select();
        try {{ document.execCommand('copy'); }} catch (e) {{}}
        ta.remove(); done();
      }}
    }}

    // =========================================================================
    // DECLARATIVE PDF/PPTX EXPANDERS (Standard Contract for tools/core/exporter.py)
    // =========================================================================
    window.SLIDE_PDF_EXPANDERS.push(({{ cloneSlideWithCanvases }}) => {{
      const expandHelper = (hostId, states, applyFn, prefix) => {{
        const host = document.getElementById(hostId);
        if (!host) return;
        const slide = host.closest('section.slide');
        if (!slide) return;
        const clones = states.map((st) => {{
          applyFn(st);
          return cloneSlideWithCanvases(slide, prefix + '-' + st);
        }});
        clones.forEach((c) => slide.parentNode.insertBefore(c, slide));
        slide.remove();
      }};

      expandHelper('ml-tabs', ['rule', 'ml'], setMlTab, 'ml');
      expandHelper('vnn-tabs', ['ai', 'ml', 'dl'], setVnnMode, 'vnn');
      expandHelper('match-list', ['q', 'ans'], setMatchPdfState, 'match');
      expandHelper('flatten-ctrl', ['mid', 'done'], setFlattenPdfState, 'flt');
      expandHelper('in-presets', ['64_1', '224_3'], setInPdfPreset, 'in');
      expandHelper('dense-ctrl', ['x1', 'full64'], setDensePdfState, 'dense');
      expandHelper('tm-ctrl', ['before', 'after'], setTmPdfState, 'tm');
      expandHelper('wb-presets', ['elsa_opt', 'no_bias', 'wrong_w'], setWbPdfState, 'wb');
      expandHelper('act-tabs', ['relu', 'sigmoid', 'softmax'], setActPdfState, 'act');
      expandHelper('out-presets', ['trained', 'ragu', 'untrained'], setOutPdfState, 'out');
      expandHelper('tr-cycle-tabs', ['2', '4'], setTrPdfState, 'tr');
      expandHelper('fnn-ctrl', ['ep1_bp', 'ep8_done'], setFnnPdfState, 'fnn');
      expandHelper('fp-steps', ['1', '2', '3', '4'], setFpStep, 'fp');
      expandHelper('gd-presets', ['small', 'ideal', 'large', 'duel'], setGdMode, 'gd');
      expandHelper('fit-tabs', ['under', 'good', 'over'], setFitPdfState, 'fit');
      expandHelper('arch-tabs', ['mlp', 'cnn', 'resnet', 'mobilenet'], setArchTab, 'arch');
    }});
"""


def main() -> None:
    data_path = ASSETS_DIR / "p02_data.json"
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
    print(f"✅ HTML interaktif {SESSION.id} ({total} slide) berhasil dibuat: {out_path}")


if __name__ == "__main__":
    main()
