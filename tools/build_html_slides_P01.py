"""Generate 54-slide beginner-friendly interactive HTML5 presentation slides/P01_image_processing_eda.html.

Designed for non-IT / non-technical learners:
- Clear flow from how humans see images -> how computers read & display images ->
  why image processing matters -> core concepts -> dataset health check (EDA) ->
  hidden camera traps -> hands-on & mini-challenge -> interactive quiz.
- No session numbering codes (no P4/P5/P7/P8 labels) in visible content or notes.
- Interactive Question -> Answer Reveal cards throughout the deck.
- Google I/O conference visual language (AGENTS.md) + reference deck layout patterns.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
STATS_PATH = ROOT_DIR / "slides" / "assets" / "P01" / "sample_stats.json"
OUT_HTML = ROOT_DIR / "slides" / "P01_image_processing_eda.html"


def build_html() -> str:
    stats = json.loads(STATS_PATH.read_text(encoding="utf-8"))
    polos = stats["by_condition"]["polos"]
    ramai = stats["by_condition"]["ramai"]

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#202124" />
  <link rel="manifest" href="../manifest.webmanifest" />
  <link rel="apple-touch-icon" href="assets/P01/icon-192.png" />
  <title>Memahami Gambar di Komputer &amp; Image Processing (54 Slides)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Roboto+Mono:wght@400;500;600&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --blue: #4285F4;
      --blue-text: #1A73E8;
      --red: #EA4335;
      --yellow: #FBBC04;
      --green: #34A853;
      --dark: #202124;
      --muted: #5F6368;
      --border: #DADCE0;
      --surface: #F8F9FA;
      --white: #FFFFFF;
      --tint-blue: #E8F0FE;
      --tint-red: #FCE8E6;
      --tint-yellow: #FEF7E0;
      --tint-green: #E6F4EA;
      --font-title: 'Poppins', Arial, sans-serif;
      --font-body: 'Roboto', Arial, sans-serif;
      --font-code: 'Roboto Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #111317;
      color: var(--dark);
      font-family: var(--font-body);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 10px 16px;
      gap: 10px;
      user-select: none;
    }}

    #progress-bar {{
      position: fixed; top: 0; left: 0; height: 4px;
      background: linear-gradient(90deg, var(--blue), var(--red), var(--yellow), var(--green));
      width: 2%; transition: width 0.25s ease; z-index: 100;
    }}

    #stage-wrap {{
      width: min(96vw, calc((100vh - 92px) * 16 / 9));
      height: min(calc(100vh - 92px), calc(96vw * 9 / 16));
      flex-shrink: 0;
      position: relative;
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 24px 70px rgba(0,0,0,0.45);
      background: var(--white);
    }}

    .slide {{
      position: absolute; inset: 0;
      padding: 34px 50px 46px;
      display: none; flex-direction: column;
      background: var(--white); overflow: hidden;
    }}
    .slide.active {{ display: flex; animation: fadeSlide 0.22s ease; }}
    @keyframes fadeSlide {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .slide.dark {{ background: var(--dark); color: var(--white); }}
    .slide.bg-blue {{ background: var(--blue); color: var(--white); }}
    .slide.bg-green {{ background: var(--green); color: var(--dark); }}
    .slide.bg-yellow {{ background: var(--yellow); color: var(--dark); }}
    .slide.bg-red {{ background: var(--red); color: var(--white); }}

    .kicker {{
      font-family: var(--font-title); font-size: 12.5px; font-weight: 700;
      letter-spacing: 0.08em; text-transform: uppercase;
      color: var(--blue-text); margin-bottom: 5px;
    }}
    .slide.dark .kicker {{ color: var(--yellow); }}
    .slide.bg-blue .kicker, .slide.bg-red .kicker {{ color: rgba(255,255,255,0.92); }}
    .slide.bg-green .kicker, .slide.bg-yellow .kicker {{ color: var(--dark); }}

    h1, h2 {{ font-family: var(--font-title); font-weight: 700; line-height: 1.18; letter-spacing: -0.015em; }}
    h1 {{ font-size: clamp(28px, 3.2vw, 44px); }}
    h2 {{ font-size: clamp(22px, 2.25vw, 31px); margin-bottom: 8px; }}
    .subtitle {{ font-size: clamp(13.5px, 1.25vw, 17px); color: var(--muted); line-height: 1.48; margin-bottom: 12px; }}
    .slide.dark .subtitle {{ color: #BDC1C6; }}

    .hl-blue {{ color: var(--blue-text); }}
    .hl-red {{ color: var(--red); }}
    .hl-green {{ color: #1E8E3E; }}
    .hl-yellow {{ color: #E37400; }}

    .pill {{
      display: inline-flex; align-items: center; gap: 6px;
      padding: 5px 13px; border-radius: 999px;
      font-family: var(--font-title); font-size: 12px; font-weight: 600;
      width: fit-content;
    }}
    .pill.blue {{ background: var(--tint-blue); color: var(--blue-text); }}
    .pill.red {{ background: var(--tint-red); color: #C5221F; }}
    .pill.yellow {{ background: var(--tint-yellow); color: #B06000; }}
    .pill.green {{ background: var(--tint-green); color: #137333; }}
    .pill.dark {{ background: #303134; color: var(--white); }}
    .pill.solid-blue {{ background: var(--blue); color: var(--white); }}

    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; flex: 1; min-height: 0; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; flex: 1; min-height: 0; }}
    .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; flex: 1; min-height: 0; }}
    .split-60-40 {{ display: grid; grid-template-columns: 1.38fr 1fr; gap: 18px; flex: 1; min-height: 0; align-items: stretch; }}
    .split-40-60 {{ display: grid; grid-template-columns: 1fr 1.38fr; gap: 18px; flex: 1; min-height: 0; align-items: stretch; }}

    .card {{
      background: var(--white); border: 1px solid var(--border);
      border-radius: 15px; padding: 18px 22px;
      display: flex; flex-direction: column; gap: 10px;
      box-shadow: 0 3px 10px rgba(32,33,36,0.05);
      position: relative; overflow: hidden;
    }}
    .card.surface {{ background: var(--surface); }}
    .card.tint-blue {{ background: var(--tint-blue); border-color: #C6DAFC; }}
    .card.tint-red {{ background: var(--tint-red); border-color: #F6AEA9; }}
    .card.tint-yellow {{ background: var(--tint-yellow); border-color: #FDE293; }}
    .card.tint-green {{ background: var(--tint-green); border-color: #A8DAB5; }}

    .card-top-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 4px; }}
    .bar-blue {{ background: var(--blue); }}
    .bar-red {{ background: var(--red); }}
    .bar-yellow {{ background: var(--yellow); }}
    .bar-green {{ background: var(--green); }}

    .card-title {{ font-family: var(--font-title); font-size: clamp(15.5px, 1.4vw, 19px); font-weight: 700; color: var(--dark); }}
    .card-body {{ font-size: clamp(13.5px, 1.18vw, 15.8px); line-height: 1.55; color: #3C4043; }}
    .card-body ul {{ padding-left: 18px; display: flex; flex-direction: column; gap: 8px; }}
    .card .callout {{ margin-top: auto; }}

    .callout {{
      background: var(--tint-blue); border-left: 4px solid var(--blue);
      border-radius: 0 11px 11px 0; padding: 10px 14px;
      font-size: clamp(12.5px, 1.08vw, 14.5px); line-height: 1.46; color: var(--dark);
    }}
    .callout.red {{ background: var(--tint-red); border-left-color: var(--red); }}
    .callout.yellow {{ background: var(--tint-yellow); border-left-color: var(--yellow); }}
    .callout.green {{ background: var(--tint-green); border-left-color: var(--green); }}

    .big-num {{ font-family: var(--font-title); font-size: clamp(28px, 3vw, 42px); font-weight: 700; line-height: 1.05; }}

    pre.code {{
      background: #1E2025; color: #E8EAED; font-family: var(--font-code);
      font-size: clamp(11px, 0.96vw, 12.8px); line-height: 1.48;
      padding: 12px 15px; border-radius: 11px; overflow-x: auto; border: 1px solid #3C4043;
      white-space: pre-wrap; word-break: break-word;
    }}
    code {{ font-family: var(--font-code); background: #F1F3F4; padding: 1px 5px; border-radius: 5px; font-size: 0.9em; color: #C5221F; }}
    pre.code code {{ background: none; padding: 0; color: inherit; }}

    .img-box {{
      background: var(--white); border: 1px solid var(--border);
      border-radius: 14px; padding: 10px;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      overflow: hidden; height: 100%;
    }}
    .img-box img {{ max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 8px; }}

    .step-list {{ display: flex; flex-direction: column; gap: 9px; flex: 1; justify-content: center; }}
    .step-item {{
      display: grid; grid-template-columns: 44px 1fr; gap: 13px; align-items: center;
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 13px; padding: 10px 14px;
    }}
    .step-num {{
      width: 38px; height: 38px; border-radius: 10px;
      background: var(--blue); color: var(--white);
      font-family: var(--font-title); font-weight: 700; font-size: 16px;
      display: flex; align-items: center; justify-content: center;
    }}
    .step-num.red {{ background: var(--red); }}
    .step-num.yellow {{ background: var(--yellow); color: var(--dark); }}
    .step-num.green {{ background: var(--green); }}
    .step-title {{ font-family: var(--font-title); font-weight: 700; font-size: 14.5px; color: var(--dark); }}
    .step-desc {{ font-size: 13px; color: var(--muted); margin-top: 2px; line-height: 1.4; }}

    table.io-table {{ width: 100%; border-collapse: collapse; font-size: 14.5px; border-radius: 12px; overflow: hidden; border: 1px solid var(--border); }}
    table.io-table th {{ background: var(--dark); color: var(--white); font-family: var(--font-title); text-align: left; padding: 12px 16px; }}
    table.io-table td {{ padding: 12px 16px; border-top: 1px solid var(--border); color: #3C4043; line-height: 1.45; }}
    table.io-table tr:nth-child(even) td {{ background: var(--surface); }}

    .cluster-4 {{ position: absolute; right: 42px; top: 38px; display: grid; grid-template-columns: 36px 36px; gap: 10px; }}
    .c-circle {{ width: 34px; height: 34px; border-radius: 50%; background: var(--blue); }}
    .c-square {{ width: 34px; height: 34px; border-radius: 8px; background: var(--red); }}
    .c-tri {{ width: 0; height: 0; border-left: 17px solid transparent; border-right: 17px solid transparent; border-bottom: 32px solid var(--yellow); }}
    .c-pill {{ width: 38px; height: 22px; border-radius: 999px; background: var(--green); align-self: center; }}

    .slide-footer {{
      position: absolute; bottom: 12px; left: 50px; right: 50px;
      display: flex; justify-content: space-between; align-items: center;
      font-size: 11.5px; color: var(--muted);
      border-top: 1px solid rgba(218,220,224,0.6); padding-top: 6px;
    }}
    .slide.dark .slide-footer {{ color: #9AA0A6; border-top-color: rgba(255,255,255,0.12); }}
    .slide.bg-blue .slide-footer, .slide.bg-red .slide-footer {{ color: rgba(255,255,255,0.88); border-top-color: rgba(255,255,255,0.22); }}
    .slide.bg-green .slide-footer, .slide.bg-yellow .slide-footer {{ color: rgba(32,33,36,0.82); border-top-color: rgba(32,33,36,0.18); }}

    .divider-center {{ flex: 1; display: flex; flex-direction: column; justify-content: center; max-width: 820px; }}
    .divider-center h1 {{ font-size: clamp(34px, 4.2vw, 54px); margin-top: 10px; }}
    .divider-center p {{ font-size: clamp(15px, 1.55vw, 20px); margin-top: 14px; opacity: 0.93; line-height: 1.5; }}

    /* Interactive Question -> Answer Reveal */
    .qa-box {{
      display: flex; flex-direction: column; gap: 14px; flex: 1; justify-content: center;
    }}
    .qa-question {{
      background: var(--tint-blue); border: 1.5px solid #C6DAFC; border-radius: 16px;
      padding: 18px 22px; font-family: var(--font-title); font-size: clamp(16px, 1.55vw, 21px);
      font-weight: 600; color: var(--dark); line-height: 1.4;
    }}
    .qa-choices {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
    .qa-choice {{
      background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
      padding: 12px 14px; font-size: 14px; color: #3C4043; line-height: 1.4;
    }}
    .qa-answer {{
      display: none; background: var(--tint-green); border: 1.5px solid #A8DAB5;
      border-left: 6px solid var(--green); border-radius: 14px; padding: 16px 20px;
      font-size: clamp(13.5px, 1.18vw, 15.5px); line-height: 1.5; color: var(--dark);
      animation: fadeSlide 0.2s ease;
    }}
    .qa-answer.shown {{ display: block; }}
    .vis-a {{ display: none; }}

    /* Interactive widgets */
    .pixel-grid-8 {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 4px; width: 100%; max-width: 320px; aspect-ratio: 1; }}
    .px-cell {{
      border-radius: 5px; display: flex; align-items: center; justify-content: center;
      font-family: var(--font-code); font-size: 11px; font-weight: 600; cursor: pointer;
      border: 1px solid rgba(0,0,0,0.08); transition: transform 0.12s;
    }}
    .px-cell:hover {{ transform: scale(1.08); z-index: 2; }}

    .btn-ui {{
      background: var(--blue-text); color: white; border: none; border-radius: 10px;
      padding: 8px 16px; font-family: var(--font-title); font-size: 13px; font-weight: 600;
      cursor: pointer; width: fit-content; transition: opacity 0.15s;
    }}
    .btn-ui:hover {{ opacity: 0.9; }}
    .btn-ui.outline {{ background: var(--white); color: var(--blue-text); border: 1.5px solid var(--blue-text); }}
    .btn-ui.green {{ background: #1E8E3E; color: white; }}

    .quiz-item {{ background: var(--surface); border: 1px solid var(--border); border-radius: 13px; padding: 14px 16px; display: flex; flex-direction: column; gap: 7px; }}
    .quiz-ans {{ display: none; background: var(--tint-green); border-left: 4px solid var(--green); padding: 8px 12px; border-radius: 0 8px 8px 0; font-size: 13px; line-height: 1.45; }}
    .quiz-ans.shown {{ display: block; }}

    /* Controls bar */
    #controls {{
      flex-shrink: 0; display: flex; align-items: center; gap: 10px; z-index: 20;
      background: #202124; color: #E8EAED; padding: 6px 14px; border-radius: 999px;
      border: 1px solid #3C4043; font-size: 12.5px;
    }}
    #page-jump {{
      width: 46px; background: #303134; color: #FFFFFF; border: 1px solid #5F6368;
      border-radius: 7px; padding: 2px 5px; text-align: center;
      font-family: var(--font-code); font-size: 12.5px; font-weight: 600;
    }}
    #page-jump:focus {{ outline: none; border-color: var(--blue); }}
    :fullscreen #controls {{
      position: fixed; bottom: 10px; right: 16px; z-index: 90;
      opacity: 0.35; transition: opacity 0.2s ease;
    }}
    :fullscreen #controls:hover {{ opacity: 1; }}
    .ctrl-btn {{
      background: #303134; color: #E8EAED; border: 1px solid #5F6368;
      border-radius: 999px; padding: 4px 12px; cursor: pointer; font-family: var(--font-title); font-size: 12px;
    }}
    .ctrl-btn:hover {{ background: var(--blue); border-color: var(--blue); color: white; }}

    #notes-drawer {{
      position: fixed; right: 18px; bottom: 58px; width: min(440px, 90vw); max-height: 44vh;
      background: #202124; color: #E8EAED; border: 1px solid #3C4043; border-radius: 14px;
      padding: 16px; box-shadow: 0 18px 45px rgba(0,0,0,0.5); display: none;
      flex-direction: column; gap: 8px; overflow-y: auto; z-index: 95; font-size: 13px; line-height: 1.52; user-select: text;
    }}
    #notes-drawer.open {{ display: flex; }}
    #notes-drawer h4 {{ font-family: var(--font-title); color: var(--yellow); font-size: 14px; }}

    #grid-modal {{ position: fixed; inset: 0; background: rgba(17,19,23,0.95); z-index: 120; display: none; padding: 26px; overflow-y: auto; }}
    #grid-modal.open {{ display: block; }}
    .grid-cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; max-width: 1300px; margin: 16px auto; }}
    .g-item {{ background: #292A2D; color: #E8EAED; border: 1px solid #3C4043; border-radius: 11px; padding: 12px; cursor: pointer; }}
    .g-item:hover {{ border-color: var(--blue); background: #303134; }}
    .g-num {{ font-family: var(--font-code); font-size: 11.5px; color: var(--yellow); }}
    .g-ttl {{ font-family: var(--font-title); font-size: 13px; font-weight: 600; margin-top: 3px; }}

    @media print {{
      @page {{ size: 13.333in 7.5in; margin: 0; }}
      body {{ background: white; height: auto; overflow: visible; display: block; padding: 0; gap: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
      #progress-bar, #controls, #notes-drawer, #grid-modal {{ display: none !important; }}
      #stage-wrap {{ width: 13.333in; height: auto; box-shadow: none; border-radius: 0; overflow: visible; }}
      .slide {{ position: relative !important; display: flex !important; width: 13.333in; height: 7.5in; page-break-after: always; break-after: page; animation: none !important; opacity: 1 !important; }}
      .slide:last-child {{ page-break-after: auto; break-after: auto; }}
      .qa-answer, .quiz-ans {{ display: block !important; animation: none !important; opacity: 1 !important; }}
      .vis-q {{ display: none !important; }}
      .vis-a {{ display: inline !important; }}
      .btn-ui {{ display: none !important; }}
    }}
  </style>
</head>
<body>
  <div id="progress-bar"></div>
  <div id="stage-wrap">

    <!-- 01: COVER -->
    <section class="slide active" data-title="Cover — Memahami Gambar &amp; Image Processing" data-notes="Alokasi waktu: 1 menit. Selamat datang! Hari ini kita belajar dari paling dasar: bagaimana mata kita dan komputer melihat gambar, mengapa foto perlu dirapikan (Image Processing), dan bagaimana memeriksa kesehatan koleksi foto kita." style="background: radial-gradient(circle at 82% 46%, rgba(251,188,4,0.14) 0%, rgba(66,133,244,0.10) 32%, rgba(234,67,53,0.05) 56%, #FFFFFF 100%); justify-content: space-between;">
      <!-- Playful floating geometric accents -->
      <svg viewBox="0 0 960 540" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:0;">
        <circle cx="885" cy="72" r="24" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2" opacity="0.85"/>
        <rect x="640" y="54" width="22" height="22" rx="7" transform="rotate(18 651 65)" fill="#E8F0FE" stroke="#4285F4" stroke-width="2" opacity="0.8"/>
        <polygon points="560,415 574,439 546,439" fill="#E6F4EA" stroke="#34A853" stroke-width="2" opacity="0.8"/>
        <circle cx="912" cy="402" r="14" fill="#FCE8E6" stroke="#EA4335" stroke-width="2" opacity="0.8"/>
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
          <span style="font-size:13.5px; font-weight:600; color:#5F6368;">120 Menit &nbsp;·&nbsp; Minggu, 15 November 2026</span>
        </div>
      </div>

      <div style="position:relative; z-index:1; display:grid; grid-template-columns: 1.65fr 0.72fr; align-items:center; gap:18px; margin:auto 0;">
        <div>
          <h1 style="font-family:var(--font-title); font-size:clamp(28px,3.5vw,46px); font-weight:700; line-height:1.12; color:#202124; margin:0; letter-spacing:-0.6px;">
            Understanding Digital Images<br />
            <span style="display:inline-block; padding-top:2px; background:linear-gradient(90deg, #4285F4 0%, #8E24AA 55%, #EA4335 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">&amp; Image Processing</span>
          </h1>
          <div style="height:4px; width:100%; max-width:580px; border-radius:999px; margin:10px 0 12px; background:linear-gradient(90deg, #4285F4 0%, #EA4335 35%, #FBBC04 70%, #34A853 100%);"></div>
          <div style="font-size:clamp(15px,1.55vw,20px); font-weight:500; color:#5F6368; line-height:1.35;">
            Mengubah Foto Mentah Menjadi Data Siap Latih untuk AI
          </div>
          <div style="margin-top:10px; display:inline-flex; align-items:center; gap:8px; background:#FFFFFF; border:1.5px solid #E0E3E7; border-radius:999px; padding:5px 14px 5px 7px; box-shadow:0 3px 10px rgba(66,133,244,0.08);">
            <span style="width:24px; height:24px; border-radius:50%; background:linear-gradient(135deg, #4285F4, #34A853); color:#FFFFFF; font-family:var(--font-title); font-size:11px; font-weight:700; display:inline-flex; align-items:center; justify-content:center;">MH</span>
            <span style="font-size:13.5px; color:#5F6368;">Presented by <strong style="color:#202124; font-weight:700;">Muhammad Haerul</strong></span>
          </div>
        </div>

        <div style="display:flex; align-items:center; justify-content:center;">
          <svg viewBox="0 0 260 260" style="width:200px; height:200px;">
            <defs>
              <filter id="coverGlow" x="-30%" y="-30%" width="160%" height="160%">
                <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#4285F4" flood-opacity="0.20"/>
              </filter>
            </defs>
            <!-- Playful colorful orbital rings -->
            <circle cx="130" cy="130" r="106" fill="none" stroke="#4285F4" stroke-width="2" stroke-dasharray="115 70 45 75" opacity="0.48"/>
            <circle cx="130" cy="130" r="84" fill="none" stroke="#EA4335" stroke-width="2" stroke-dasharray="80 55 70 50" stroke-dashoffset="35" opacity="0.45"/>
            <circle cx="130" cy="130" r="64" fill="none" stroke="#34A853" stroke-width="2" stroke-dasharray="60 45 50 45" stroke-dashoffset="15" opacity="0.52"/>
            <!-- Orbiting playful shapes -->
            <circle cx="234" cy="116" r="9" fill="#FBBC04" stroke="#FFFFFF" stroke-width="2"/>
            <rect x="44" y="64" width="16" height="16" rx="5" fill="#4285F4" stroke="#FFFFFF" stroke-width="2"/>
            <circle cx="192" cy="210" r="8" fill="#34A853" stroke="#FFFFFF" stroke-width="2"/>
            <circle cx="48" cy="182" r="7" fill="#EA4335" stroke="#FFFFFF" stroke-width="2"/>
            <!-- Center playful 3x3 pixel grid card -->
            <rect x="86" y="86" width="88" height="88" rx="24" fill="#FFFFFF" filter="url(#coverGlow)" stroke="#E8EAED" stroke-width="1.5"/>
            <rect x="103" y="103" width="15" height="15" rx="4" fill="#EA4335"/>
            <rect x="122" y="103" width="15" height="15" rx="4" fill="#FBBC04"/>
            <rect x="141" y="103" width="15" height="15" rx="4" fill="#34A853"/>
            <rect x="103" y="122" width="15" height="15" rx="4" fill="#4285F4"/>
            <rect x="122" y="122" width="15" height="15" rx="4" fill="#8E24AA"/>
            <rect x="141" y="122" width="15" height="15" rx="4" fill="#4285F4"/>
            <rect x="103" y="141" width="15" height="15" rx="4" fill="#34A853"/>
            <rect x="122" y="141" width="15" height="15" rx="4" fill="#FBBC04"/>
            <rect x="141" y="141" width="15" height="15" rx="4" fill="#EA4335"/>
          </svg>
        </div>
      </div>

      <div style="position:relative; z-index:1; display:flex; gap:6px; flex-wrap:wrap; align-items:center; padding-bottom:2px;">
        <span class="pill red" style="font-size:10.5px; padding:4px 10px;">Mata vs Komputer</span>
        <span class="pill green" style="font-size:10.5px; padding:4px 10px;">Pixel &amp; RGB</span>
        <span class="pill blue" style="font-size:10.5px; padding:4px 10px;">Aspect Ratio</span>
        <span class="pill blue" style="font-size:10.5px; padding:4px 10px;">Normalization</span>
        <span class="pill yellow" style="font-size:10.5px; padding:4px 10px;">EDA</span>
        <span class="pill" style="background:#F3E8FD; color:#7627BB; font-size:10.5px; padding:4px 10px;">Edge Density</span>
        <span class="pill" style="background:#F3E8FD; color:#7627BB; font-size:10.5px; padding:4px 10px;">EXIF &amp; Hash</span>
        <span class="pill solid-blue" style="font-size:10.5px; padding:4px 12px;">Python</span>
        <span class="pill" style="background:#EA4335; color:#FFFFFF; font-size:10.5px; padding:4px 12px;">OpenCV</span>
        <span class="pill" style="background:#34A853; color:#FFFFFF; font-size:10.5px; padding:4px 12px;">NumPy</span>
      </div>
    </section>

    <!-- 02: PETA MATERI -->
    <section class="slide" data-title="Peta Perjalanan Belajar (5 Bab)" data-notes="Alokasi waktu: 1 menit. Ini alur belajar kita hari ini: mulai dari dasar cara komputer melihat gambar, alasan belajar image processing, hingga praktik memeriksa kualitas foto.">
      <div class="kicker">PETA PERJALANAN BELAJAR</div>
      <h2>Dari Foto Biasa Menuju <span class="hl-blue">Data Siap AI</span></h2>
      <p class="subtitle">Disusun bertahap dengan analogi sehari-hari — tidak perlu latar belakang IT untuk memahaminya.</p>
      <div class="step-list">
        <div class="step-item"><div class="step-num">01</div><div><div class="step-title">Bagaimana Kita &amp; Komputer Melihat Gambar</div><div class="step-desc">Perbedaan cara mata manusia vs komputer membaca foto, pixel, nilai 0–255, dan RGB channels.</div></div></div>
        <div class="step-item"><div class="step-num red">02</div><div><div class="step-title">Mengapa Kita Perlu Image Processing?</div><div class="step-desc">Menyamakan resolution, menjaga aspect ratio agar tidak distorted, dan melakukan normalization.</div></div></div>
        <div class="step-item"><div class="step-num yellow">03</div><div><div class="step-title">Exploratory Data Analysis (EDA)</div><div class="step-desc">Mengecek keseimbangan jumlah foto, grafik pencahayaan, serta membedakan latar polos vs ramai.</div></div></div>
        <div class="step-item"><div class="step-num green">04</div><div><div class="step-title">Tiga Jebakan Tersembunyi Kamera HP</div><div class="step-desc">Mendeteksi EXIF orientation yang terputar, duplicate images, dan corrupted files.</div></div></div>
        <div class="step-item"><div class="step-num">05</div><div><div class="step-title">Praktik Santai, Diskusi &amp; Kuis Interaktif</div><div class="step-desc">Melihat hasil nyata pada 120 foto sampel, diskusi tantangan latar polos vs ramai, kamus istilah, &amp; kuis.</div></div></div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>02 / 54</span></div>
    </section>

    <!-- 03: ALUR SESI 120 MENIT -->
    <section class="slide" data-title="Alur Sesi 120 Menit" data-notes="Alokasi waktu: 1 menit. Kita bagi waktu 120 menit agar santai, ada jeda istirahat, dan semua materi tuntas di kelas.">
      <div class="kicker">AGENDA · 120 MENIT</div>
      <h2>Alur Sesi <span class="hl-blue">Hari Ini</span></h2>
      <p class="subtitle">Belajar pelan-pelan, penuh ilustrasi visual, dan tanya-jawab interaktif yang tuntas di kelas.</p>
      <div class="grid-3">
        <div class="card tint-blue"><div class="card-top-bar bar-blue"></div><div class="card-title">00–10 · Pemanasan</div><div class="card-body">Menyegarkan ingatan tentang data angka dan membayangkan bagaimana komputer "melihat" sebuah foto.</div></div>
        <div class="card tint-red"><div class="card-top-bar bar-red"></div><div class="card-title">10–40 · Teori &amp; Ilustrasi</div><div class="card-body">Memahami pixel, RGB channels, alasan Image Processing, EDA dataset, serta 3 jebakan file foto.</div></div>
        <div class="card tint-yellow"><div class="card-top-bar bar-yellow"></div><div class="card-title">40–45 · Istirahat Singkat</div><div class="card-body">Jeda 5 menit untuk minum air dan meregangkan mata sebelum melihat contoh praktik.</div></div>
        <div class="card tint-green"><div class="card-top-bar bar-green"></div><div class="card-title">45–95 · Praktik Terpandu</div><div class="card-body">Menjalankan 6 langkah pemeriksaan foto secara bertahap pada koleksi foto sampel.</div></div>
        <div class="card tint-blue"><div class="card-top-bar bar-blue"></div><div class="card-title">95–110 · Diskusi Kasus</div><div class="card-body">Menebak tantangan nyata: lebih mudah mana bagi AI, foto berlatar polos atau foto berlatar ramai?</div></div>
        <div class="card tint-red"><div class="card-top-bar bar-red"></div><div class="card-title">110–120 · Kuis &amp; Penutup</div><div class="card-body">Kuis interaktif 5 soal dengan pembahasan langsung serta rangkuman poin terpenting hari ini.</div></div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>03 / 54</span></div>
    </section>

    <!-- 04: TUJUAN BELAJAR -->
    <section class="slide" data-title="Apa yang Akan Kita Kuasai?" data-notes="Alokasi waktu: 1 menit. Tiga kemampuan praktis yang akan kita bawa pulang setelah sesi selesai.">
      <div class="kicker">TUJUAN BELAJAR</div>
      <h2>Apa yang Akan Kita <span class="hl-blue">Kuasai</span>?</h2>
      <div class="grid-3">
        <div class="card"><div class="card-top-bar bar-blue"></div><span class="pill blue" style="margin-bottom:6px;">POIN 01</span><div class="card-title">Paham Bahasa Gambar Komputer</div><div class="card-body"><ul><li>Tahu bedanya cara mata kita vs komputer membaca foto.</li><li>Mengerti bahwa setiap foto sebenarnya adalah tabel berisi angka 0–255.</li><li>Mengerti konsep RGB channels (Red, Green, Blue).</li></ul></div><div class="callout"><strong>Hasil:</strong> Gambar digital tidak lagi terasa seperti <em>black box</em>.</div></div>
        <div class="card"><div class="card-top-bar bar-green"></div><span class="pill green" style="margin-bottom:6px;">POIN 02</span><div class="card-title">Tahu Kenapa Foto Harus Dirapikan</div><div class="card-body"><ul><li>Mengerti bahaya <em>distorted aspect ratio</em> saat melakukan resize.</li><li>Paham alasan menyamakan skala angka (0–1).</li><li>Tahu cara mencegah foto terbalik dari kamera HP.</li></ul></div><div class="callout green"><strong>Hasil:</strong> Paham fungsi utama Image Processing sebelum AI dilatih.</div></div>
        <div class="card"><div class="card-top-bar bar-red"></div><span class="pill red" style="margin-bottom:6px;">POIN 03</span><div class="card-title">Bisa Mengaudit Koleksi Foto</div><div class="card-body"><ul><li>Mampu mengecek apakah jumlah foto sudah seimbang.</li><li>Bisa membedakan foto gelap, terang, polos, dan ramai.</li><li>Tahu cara menyaring foto rusak dan kembar.</li></ul></div><div class="callout red"><strong>Hasil:</strong> Koleksi foto bersih, sehat, dan jujur untuk AI.</div></div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>04 / 54</span></div>
    </section>

    <!-- 05: PEMANTIK -->
    <section class="slide" data-title="Pemanasan: Dari Angka Biasa ke Foto" data-notes="Alokasi waktu: 2 menit. Sebelumnya kita mengenal data dalam bentuk tabel angka biasa. Sekarang, bayangkan kalau input yang masuk ke komputer adalah foto dari kamera HP.">
      <div class="kicker">PEMANASAN</div>
      <h2>Dari Data Tabel Biasa ke <span class="hl-blue">Sebuah Foto</span></h2>
      <div class="grid-2">
        <div class="card surface">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Data yang Mudah Dibayangkan</div>
          <div class="card-body">
            <ul>
              <li>Misalnya data tinggi badan, umur, atau harga rumah.</li>
              <li>Bentuknya sudah jelas: berupa <strong>baris dan kolom angka</strong> di Excel.</li>
              <li>Komputer langsung bisa menghitung rata-rata atau mencari polanya.</li>
            </ul>
          </div>
          <svg viewBox="0 0 360 88" style="width:100%; max-height:86px; margin-top:auto;">
            <rect x="8" y="8" width="344" height="72" rx="10" fill="#FFFFFF" stroke="#DADCE0"/>
            <line x1="8" y1="32" x2="352" y2="32" stroke="#DADCE0"/><line x1="120" y1="8" x2="120" y2="80" stroke="#DADCE0"/><line x1="235" y1="8" x2="235" y2="80" stroke="#DADCE0"/>
            <text x="64" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="#1A73E8">Nama</text>
            <text x="177" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="#1A73E8">Umur</text>
            <text x="293" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="#1A73E8">Tinggi</text>
            <text x="64" y="51" text-anchor="middle" font-size="11" fill="#3C4043">Budi</text><text x="177" y="51" text-anchor="middle" font-size="11" fill="#3C4043">25</text><text x="293" y="51" text-anchor="middle" font-size="11" fill="#3C4043">170 cm</text>
            <text x="64" y="71" text-anchor="middle" font-size="11" fill="#3C4043">Siti</text><text x="177" y="71" text-anchor="middle" font-size="11" fill="#3C4043">22</text><text x="293" y="71" text-anchor="middle" font-size="11" fill="#3C4043">160 cm</text>
          </svg>
          <div class="callout"><strong>Tapi bagaimana dengan foto?</strong> Foto tidak terlihat seperti tabel Excel!</div>
        </div>
        <div class="card">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Tantangan Besar Saat Membaca Foto</div>
          <div class="card-body">
            <ul>
              <li>Saat kita memotret dengan HP, yang tersimpan di memori ternyata <strong>bukan gambar utuh</strong>.</li>
              <li>Komputer tidak punya mata dan tidak punya imajinasi seperti manusia.</li>
              <li>Jadi, bagaimana caranya komputer bisa mengenali bentuk bintang, wajah, atau benda lain?</li>
            </ul>
          </div>
          <svg viewBox="0 0 360 88" style="width:100%; max-height:86px; margin-top:auto;">
            <rect x="14" y="10" width="84" height="68" rx="10" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
            <circle cx="56" cy="38" r="16" fill="#FBBC04"/><path d="M26 68 L48 48 L66 60 L82 44 L94 68 Z" fill="#34A853"/>
            <path d="M112 44 L152 44" stroke="#EA4335" stroke-width="3" stroke-linecap="round"/><polygon points="150,38 164,44 150,50" fill="#EA4335"/>
            <text x="138" y="34" text-anchor="middle" font-size="10" font-weight="700" fill="#C5221F">?</text>
            <rect x="172" y="10" width="174" height="68" rx="10" fill="#202124"/>
            <text x="259" y="34" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="11" fill="#FBBC04">[251, 188, 4, ...]</text>
            <text x="259" y="54" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="11" fill="#A8DAB5">[52, 168, 83, ...]</text>
            <text x="259" y="70" text-anchor="middle" font-size="10" fill="#9AA0A6">Ribuan angka di memori</text>
          </svg>
          <div class="callout green">Jawabannya ada di 3 ilustrasi pertama pada Bab 1 berikut ini!</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>05 / 54</span></div>
    </section>

    <!-- 06: DIVIDER BAB 1 -->
    <section class="slide bg-blue" data-title="Bab 1: Cara Kita &amp; Komputer Melihat Gambar" data-notes="Alokasi waktu: 0.5 menit. Kita masuk ke Bab 1: membedah perbedaan cara mata manusia dan komputer melihat gambar.">
      <div class="divider-center">
        <span class="pill dark">BAB 1 · DASAR PENGENALAN GAMBAR</span>
        <h1>Bagaimana Kita &amp; Komputer Melihat Gambar?</h1>
        <p>Mengintip perbedaan besar antara mata manusia yang langsung mengenali bentuk, dan komputer yang hanya membaca lautan angka.</p>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>06 / 54</span></div>
    </section>

    <!-- 07: ILUSTRASI 1 - CARA MANUSIA MELIHAT GAMBAR (REALISTIS) -->
    <section class="slide" data-title="Ilustrasi: Cara Manusia Melihat Gambar" data-notes="Alokasi waktu: 1.5 menit. Perhatikan alur realistis ini: cahaya memantul dari objek nyata (apel), masuk ke lensa dan retina mata, dikirim sebagai sinyal saraf ke otak, dan otak langsung mengenali 'Ini Apel Merah!'.">
      <div class="kicker">BAB 1 · ILUSTRASI 1</div>
      <h2>Cara <span class="hl-blue">Mata Manusia</span> Melihat Gambar</h2>
      <p class="subtitle">Otak kita sangat hebat: begitu cahaya masuk ke mata, kita langsung mengenali bentuk, warna, dan maknanya.</p>
      <div class="card surface" style="flex:1; padding:12px 16px; justify-content:space-between; align-items:center;">
        <img src="assets/P01/human_vision_realistic.jpg" alt="Ilustrasi realistis mata manusia dan otak melihat objek" style="max-height:305px; max-width:100%; object-fit:contain; border-radius:12px;" />
        <div class="grid-3" style="width:100%; flex:0 0 auto; gap:12px;">
          <div class="callout" style="margin:0; text-align:center;"><strong>1. Objek Nyata:</strong> Cahaya memantul dari apel merah.</div>
          <div class="callout yellow" style="margin:0; text-align:center;"><strong>2. Mata Menangkap:</strong> Lensa memfokuskan cahaya ke retina.</div>
          <div class="callout green" style="margin:0; text-align:center;"><strong>3. Otak Mengenali:</strong> Sinyal saraf langsung paham <em>"Ini Apel!"</em></div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>07 / 54</span></div>
    </section>

    <!-- 08: ILUSTRASI 2 INTERAKTIF - CARA KOMPUTER MEMBACA GAMBAR -->
    <section class="slide" data-title="Simulator: Cara Komputer Membaca Gambar" data-notes="Alokasi waktu: 2 menit. Fitur interaktif! Ajak peserta mengganti mode dari Mata Manusia -> Grid Pixel -> Angka Komputer, memilih objek (Apel/Bintang/Rumah), dan mengklik pixel untuk melihat angka RGB aslinya.">
      <div class="kicker">BAB 1 · SIMULATOR INTERAKTIF</div>
      <h2>Cara <span class="hl-red">Komputer Membaca</span> Gambar (Coba Langsung!)</h2>
      <div class="split-60-40">
        <div class="card surface" style="align-items:center; justify-content:center; gap:10px; padding:14px;">
          <div id="comp-presets" style="display:flex; gap:6px; flex-wrap:wrap; justify-content:center;">
            <button class="btn-ui" data-preset="apple" onclick="setCompPreset('apple')">Apel Merah</button>
            <button class="btn-ui outline" data-preset="star" onclick="setCompPreset('star')">Bintang</button>
            <button class="btn-ui outline" data-preset="house" onclick="setCompPreset('house')">Rumah</button>
          </div>
          <canvas id="comp-canvas" width="288" height="288" style="border-radius:12px; border:2px solid var(--border); background:#FFF; cursor:crosshair; max-height:255px; aspect-ratio:1;"></canvas>
          <div id="comp-modes" style="display:flex; gap:6px; flex-wrap:wrap; justify-content:center;">
            <button class="btn-ui outline" data-mode="human" onclick="setCompMode('human')">1. Mata Manusia</button>
            <button class="btn-ui outline" data-mode="grid" onclick="setCompMode('grid')">2. Grid Pixel</button>
            <button class="btn-ui green" data-mode="numbers" onclick="setCompMode('numbers')">3. Angka Komputer</button>
          </div>
        </div>
        <div class="card">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title">Inspektur Pixel Real-Time</div>
          <div class="card-body">
            <div style="margin-bottom:8px;">
              <label style="font-weight:700; font-size:13px;">Ukuran Grid: <span id="comp-res-lbl">8 × 8</span> pixels</label>
              <input id="comp-res" type="range" min="0" max="7" value="1" step="1" style="width:100%;" oninput="updateCompRes()" />
            </div>
            <div style="display:flex; align-items:center; gap:12px; background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:10px 12px; margin-bottom:10px;">
              <div id="comp-swatch" style="width:48px; height:48px; border-radius:10px; background:#EA4335; border:2px solid #FFF; box-shadow:0 2px 6px rgba(0,0,0,0.15); flex-shrink:0;"></div>
              <div id="comp-px-readout" style="font-family:var(--font-code); font-size:12.5px; line-height:1.45;">Klik atau arahkan kursor ke kotak gambar untuk melihat angka RGB-nya!</div>
            </div>
            <ul>
              <li><strong>Mode 1:</strong> Bentuk utuh seperti yang kita lihat.</li>
              <li><strong>Mode 2:</strong> Dipecah menjadi kotak-kotak <em>pixel</em>.</li>
              <li><strong>Mode 3:</strong> Komputer hanya melihat angka <code>0–255</code>!</li>
            </ul>
          </div>
          <div class="callout red">Komputer <strong>sama sekali tidak melihat apel atau bintang</strong> — di memorinya, foto hanyalah <em>pixel matrix</em> (array angka)!</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>08 / 54</span></div>
    </section>

    <!-- 09: ILUSTRASI 3 - CARA KOMPUTER MENAMPILKAN GAMBAR -->
    <section class="slide" data-title="Ilustrasi: Cara Komputer Menampilkan Gambar" data-notes="Alokasi waktu: 1.5 menit. Lalu bagaimana kita bisa melihat foto di layar HP? Komputer membaca pixel matrix tadi, lalu menyalakan 3 lampu kecil Merah-Hijau-Biru di tiap titik layar.">
      <div class="kicker">BAB 1 · ILUSTRASI 3</div>
      <h2>Cara <span class="hl-green">Komputer Menampilkan</span> Gambar ke Layar</h2>
      <p class="subtitle">Proses kebalikannya: angka diubah kembali menjadi cahaya lampu warna di layar HP atau laptop kita.</p>
      <div class="card surface" style="flex:1; justify-content:center; align-items:center; padding:18px;">
        <svg viewBox="0 0 920 300" style="width:100%; height:100%; max-height:290px;">
          <!-- Step 1: Angka -->
          <rect x="20" y="35" width="225" height="225" rx="18" fill="#E8F0FE" stroke="#C6DAFC" stroke-width="2"/>
          <text x="132" y="65" text-anchor="middle" font-family="Poppins, sans-serif" font-size="15" font-weight="700" fill="#1A73E8">1. File Berisi Angka</text>
          <rect x="42" y="92" width="180" height="114" rx="10" fill="#202124"/>
          <text x="132" y="125" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="13" fill="#EA4335">Merah : 251</text>
          <text x="132" y="152" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="13" fill="#34A853">Hijau : 188</text>
          <text x="132" y="179" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="13" fill="#4285F4">Biru  :   4</text>
          <text x="132" y="240" text-anchor="middle" font-family="Roboto, sans-serif" font-size="13" fill="#3C4043">Data angka dari memori</text>

          <!-- Arrow 1 -->
          <path d="M260 148 L320 148" stroke="#34A853" stroke-width="4" stroke-linecap="round"/>
          <polygon points="318,139 336,148 318,157" fill="#34A853"/>
          <text x="298" y="132" text-anchor="middle" font-family="Roboto, sans-serif" font-size="12" font-weight="700" fill="#137333">Dikirim</text>

          <!-- Step 2: Lampu Layar -->
          <rect x="345" y="35" width="235" height="225" rx="18" fill="#FFFFFF" stroke="#DADCE0" stroke-width="2"/>
          <text x="462" y="65" text-anchor="middle" font-family="Poppins, sans-serif" font-size="15" font-weight="700" fill="#202124">2. Sub-pixel RGB di Layar</text>
          <rect x="380" y="92" width="165" height="114" rx="12" fill="#202124"/>
          <rect x="396" y="108" width="38" height="82" rx="6" fill="#EA4335" opacity="0.95"/>
          <rect x="443" y="108" width="38" height="82" rx="6" fill="#34A853" opacity="0.78"/>
          <rect x="490" y="108" width="38" height="82" rx="6" fill="#4285F4" opacity="0.15"/>
          <text x="415" y="154" text-anchor="middle" font-family="Poppins, sans-serif" font-size="14" font-weight="700" fill="#FFF">R</text>
          <text x="462" y="154" text-anchor="middle" font-family="Poppins, sans-serif" font-size="14" font-weight="700" fill="#FFF">G</text>
          <text x="509" y="154" text-anchor="middle" font-family="Poppins, sans-serif" font-size="14" font-weight="700" fill="#FFF">B</text>
          <text x="462" y="240" text-anchor="middle" font-family="Roboto, sans-serif" font-size="13" fill="#5F6368">3 sub-pixel menyala sesuai angka</text>

          <!-- Arrow 2 -->
          <path d="M595 148 L655 148" stroke="#FBBC04" stroke-width="4" stroke-linecap="round"/>
          <polygon points="653,139 671,148 653,157" fill="#FBBC04"/>
          <text x="633" y="132" text-anchor="middle" font-family="Roboto, sans-serif" font-size="12" font-weight="700" fill="#B06000">Dilihat</text>

          <!-- Step 3: Mata Melihat -->
          <rect x="680" y="35" width="220" height="225" rx="18" fill="#FEF7E0" stroke="#FDE293" stroke-width="2"/>
          <text x="790" y="65" text-anchor="middle" font-family="Poppins, sans-serif" font-size="15" font-weight="700" fill="#B06000">3. Jadi Gambar Lagi!</text>
          <rect x="725" y="96" width="130" height="106" rx="14" fill="#FBBC04" stroke="#E37400" stroke-width="2"/>
          <text x="790" y="154" text-anchor="middle" font-family="Poppins, sans-serif" font-size="14" font-weight="700" fill="#202124">Kuning Cerah</text>
          <text x="790" y="240" text-anchor="middle" font-family="Roboto, sans-serif" font-size="13" fill="#3C4043">Mata menggabungkan cahayanya</text>
        </svg>
      </div>
      <div class="callout green" style="margin-top:10px;">Layar HP menggabungkan jutaan titik sub-pixel <strong>Red, Green, Blue</strong> yang sangat rapat sehingga mata kita melihatnya sebagai gambar utuh.</div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>09 / 54</span></div>
    </section>

    <!-- 10: QA REVEAL #1 -->
    <section class="slide" data-title="Tanya-Jawab #1: Seberapa Banyak Angka dalam 1 Foto?" data-notes="Alokasi waktu: 1.5 menit. Ajak peserta menebak dulu sebelum menekan tombol Lihat Jawaban.">
      <div class="kicker">TANYA &amp; JAWAB INTERAKTIF · #1</div>
      <h2>Coba Tebak: <span class="hl-blue">Berapa Banyak Angka</span> di 1 Foto?</h2>
      <div class="split-60-40">
        <div class="qa-box" style="margin:0; justify-content:center;">
          <div class="qa-question">
            Jika komputer membaca sebuah foto warna kecil berukuran <strong>224 × 224 pixels</strong>, dan setiap kotak punya <strong>3 angka</strong> (Merah, Hijau, Biru), kira-kira berapa total angka yang dibaca komputer untuk 1 foto saja?
          </div>
          <div class="qa-choices">
            <div class="qa-choice"><strong>A.</strong> Sekitar 672 angka saja</div>
            <div class="qa-choice"><strong>B.</strong> Sekitar 50.176 angka</div>
            <div class="qa-choice"><strong>C.</strong> Lebih dari 150.000 angka!</div>
          </div>
          <button class="btn-ui" onclick="toggleQA('qa1', this)">Klik untuk Lihat Jawaban &amp; Penjelasan</button>
          <div id="qa1" class="qa-answer">
            <strong>Jawaban: C — Tepatnya 150.528 angka!</strong><br />
            Hitungan sederhananya: <code>224 baris × 224 kolom × 3 warna = 150.528 angka</code>.<br />
            Bayangkan jika kita punya 1.000 foto, berarti komputer harus membaca lebih dari <strong>150 juta angka</strong>! Itulah alasan mengapa data foto harus rapi dan ukurannya seragam agar komputer tidak kewalahan.
          </div>
        </div>
        <div class="card surface" style="align-items:center; justify-content:center; padding:16px;">
          <svg id="qa1-vis" viewBox="0 0 320 260" style="width:100%; height:100%; max-height:360px;">
            <rect x="24" y="42" width="118" height="118" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.5"/>
            <rect x="44" y="58" width="118" height="118" rx="12" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.5" opacity="0.92"/>
            <rect x="64" y="74" width="118" height="118" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="2.5" opacity="0.92"/>
            <rect x="84" y="90" width="118" height="118" rx="12" fill="#FFFFFF" stroke="#202124" stroke-width="2.5"/>
            <text x="143" y="138" text-anchor="middle" font-size="18" font-weight="700" fill="#202124">224 × 224</text>
            <text x="143" y="160" text-anchor="middle" font-size="13" font-weight="600" fill="#5F6368">pixels</text>
            <text x="143" y="184" text-anchor="middle" font-size="12" font-weight="700" fill="#1A73E8">× 3 RGB Channels</text>
            <rect x="224" y="64" width="76" height="34" rx="10" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.5"/>
            <text x="262" y="86" text-anchor="middle" font-size="13" font-weight="700" fill="#C5221F">R (0–255)</text>
            <rect x="224" y="108" width="76" height="34" rx="10" fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"/>
            <text x="262" y="130" text-anchor="middle" font-size="13" font-weight="700" fill="#137333">G (0–255)</text>
            <rect x="224" y="152" width="76" height="34" rx="10" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.5"/>
            <text x="262" y="174" text-anchor="middle" font-size="13" font-weight="700" fill="#1A73E8">B (0–255)</text>
            <g class="vis-q">
              <rect x="50" y="220" width="220" height="30" rx="15" fill="#202124"/>
              <text x="160" y="240" text-anchor="middle" font-size="13" font-weight="700" fill="#FBBC04">Total Angka = 224 × 224 × 3 = ?</text>
            </g>
            <g class="vis-a">
              <rect x="34" y="220" width="252" height="30" rx="15" fill="#34A853"/>
              <text x="160" y="240" text-anchor="middle" font-size="13" font-weight="700" fill="#FFFFFF">Total = 150.528 Angka / Foto!</text>
            </g>
          </svg>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>10 / 54</span></div>
    </section>

    <!-- 11: APA ITU PIKSEL -->
    <section class="slide" data-title="Mengenal Piksel: Kertas Berpetak Digital" data-notes="Alokasi waktu: 1 menit. Gunakan analogi kertas berpetak atau mosaik keramik. Setiap kotak kecil disebut piksel.">
      <div class="kicker">BAB 1 · KONSEP PIXEL</div>
      <h2>Apa Itu <span class="hl-blue">Pixel</span>?</h2>
      <div class="split-60-40">
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">PIXEL (PICTURE ELEMENT)</span>
          <div class="card-title">Kotak Terkecil Penyusun Gambar</div>
          <div class="card-body">
            <ul>
              <li>Bayangkan sebuah lukisan mosaik dari keramik kecil-kecil, atau buku gambar berpetak.</li>
              <li>Setiap <strong>satu kotak tunggal</strong> hanya boleh diisi <strong>satu warna polos</strong>.</li>
              <li>Kotak kecil itulah yang disebut <strong>Pixel</strong>.</li>
              <li>Jika kita perbesar (zoom in) sebuah foto sampai mentok, kotak-kotak ini akan terlihat jelas!</li>
            </ul>
          </div>
          <div class="callout">Semakin banyak kotaknya, foto terlihat makin <strong>halus dan tajam</strong>.</div>
        </div>
        <div class="img-box">
          <img src="assets/P01/01_opening_character.png" alt="Contoh gambar geometris sintetis" />
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>11 / 54</span></div>
    </section>

    <!-- 12: INTERACTIVE 8x8 GRID -->
    <section class="slide" data-title="Eksperimen: Lihat Seperti Komputer (Grid 8×8)" data-notes="Alokasi waktu: 2 menit. Ajak peserta mencoba tombol 'Lihat Sebagai Angka Komputer' dan mengklik kotak untuk merasakan angka 0 (gelap) sampai 255 (putih terang).">
      <div class="kicker">BAB 1 · EKSPERIMEN INTERAKTIF</div>
      <h2>Coba Lihat <span class="hl-blue">Seperti Komputer</span> (8×8 Pixel Grid)</h2>
      <div class="split-40-60">
        <div class="card surface" style="align-items:center; justify-content:center; gap:12px;">
          <div id="grid8" class="pixel-grid-8"></div>
          <div style="display:flex; gap:8px; flex-wrap:wrap; justify-content:center;">
            <button class="btn-ui" onclick="toggleGridNumbers()">Tukar: Warna ↔ Angka</button>
            <button class="btn-ui outline" onclick="resetGrid8()">Reset</button>
          </div>
          <div id="px-info" style="font-family:var(--font-code); font-size:12.5px; color:var(--dark); text-align:center;">Klik kotak mana saja untuk mengintip angkanya!</div>
        </div>
        <div class="card">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Cara Membaca Nilai Brightness</div>
          <div class="card-body">
            <ul>
              <li><strong>Angka 0 = Hitam Pekat</strong> (intensitas terendah / gelap total).</li>
              <li><strong>Angka 255 = Putih Terang</strong> (intensitas maksimal / terang penuh).</li>
              <li><strong>Angka 100–180 = Grayscale</strong> (remang-remang di antara gelap dan terang).</li>
            </ul>
          </div>
          <div class="callout green">Di sebelah kiri, bentuk persegi terlihat jelas oleh mata kita. Namun saat angka ditampilkan, komputer hanya melihat angka <strong>35</strong> (gelap) di tengah lautan angka <strong>245</strong> (terang).</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>12 / 54</span></div>
    </section>

    <!-- 13: TIGA LAMPU WARNA RGB -->
    <section class="slide" data-title="Model Warna RGB: Tiga Sumber Cahaya" data-notes="Alokasi waktu: 1 menit. Jelaskan RGB tanpa rumus: tiga warna cahaya dasar Merah, Hijau, Biru yang digabungkan di titik yang sama.">
      <div class="kicker">BAB 1 · KONSEP WARNA RGB</div>
      <h2>Model Warna <span class="hl-red">R</span><span class="hl-green">G</span><span class="hl-blue">B</span>: Tiga Sumber Cahaya</h2>
      <p class="subtitle">Setiap titik layar menyalakan tiga warna cahaya dasar dalam intensitas 0–255 untuk membentuk jutaan warna.</p>
      <div class="grid-3">
        <div class="card tint-red">
          <div class="card-top-bar bar-red"></div>
          <div class="big-num hl-red">R</div>
          <div class="card-title">Red (Merah)</div>
          <div class="card-body">Mengatur intensitas channel <strong>Red</strong> dinyalakan pada pixel tersebut (0 = mati, 255 = penuh).</div>
        </div>
        <div class="card tint-green">
          <div class="card-top-bar bar-green"></div>
          <div class="big-num hl-green">G</div>
          <div class="card-title">Green (Hijau)</div>
          <div class="card-body">Mengatur intensitas channel <strong>Green</strong> dinyalakan pada titik yang sama (0 = mati, 255 = penuh).</div>
        </div>
        <div class="card tint-blue">
          <div class="card-top-bar bar-blue"></div>
          <div class="big-num hl-blue">B</div>
          <div class="card-title">Blue (Biru)</div>
          <div class="card-body">Mengatur intensitas channel <strong>Blue</strong> dinyalakan. Gabungan ketiganya menghasilkan 16 juta+ warna!</div>
        </div>
      </div>
      <div class="card surface" style="flex-direction:row; align-items:center; gap:18px; padding:10px 18px; margin-top:10px; flex:0 0 auto;">
        <svg viewBox="0 0 180 110" style="width:155px; height:95px; flex-shrink:0;">
          <rect x="0" y="0" width="180" height="110" rx="12" fill="#202124"/>
          <g style="mix-blend-mode:screen;">
            <circle cx="72" cy="44" r="30" fill="#FF0000"/>
            <circle cx="108" cy="44" r="30" fill="#00FF00"/>
            <circle cx="90" cy="74" r="30" fill="#0000FF"/>
          </g>
          <text x="90" y="57" text-anchor="middle" font-size="9.5" font-weight="700" fill="#202124">Putih</text>
          <text x="90" y="34" text-anchor="middle" font-size="8.5" font-weight="700" fill="#202124">Kuning</text>
        </svg>
        <div class="card-body" style="margin:0;">
          <strong>Percampuran Cahaya (Additive):</strong> Jika <strong>Red = 255</strong>, <strong>Green = 255</strong>, dan <strong>Blue = 0</strong>, cahaya merah + hijau bergabung menjadi <strong>Kuning</strong>. Jika ketiganya <code>255</code>, hasilnya <strong>Putih</strong>!
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>13 / 54</span></div>
    </section>

    <!-- 14: INTERACTIVE RGB MIXER -->
    <section class="slide" data-title="Eksperimen: Campur 3 Lampu Warna" data-notes="Alokasi waktu: 2 menit. Geser ketiga slider Merah, Hijau, Biru untuk melihat bagaimana angka berubah menjadi warna di layar.">
      <div class="kicker">BAB 1 · EKSPERIMEN INTERAKTIF</div>
      <h2>Coba Sendiri: <span class="hl-blue">3 Angka Jadi 1 Warna</span></h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Atur Intensitas RGB Channels (0–255)</div>
          <div style="display:flex; flex-direction:column; gap:14px; margin-top:8px;">
            <div>
              <label style="font-weight:700; color:#C5221F;">Merah (R): <span id="r-val">66</span></label>
              <input id="r-sl" type="range" min="0" max="255" value="66" style="width:100%;" oninput="updateRGB()" />
            </div>
            <div>
              <label style="font-weight:700; color:#137333;">Hijau (G): <span id="g-val">133</span></label>
              <input id="g-sl" type="range" min="0" max="255" value="133" style="width:100%;" oninput="updateRGB()" />
            </div>
            <div>
              <label style="font-weight:700; color:#1A73E8;">Biru (B): <span id="b-val">244</span></label>
              <input id="b-sl" type="range" min="0" max="255" value="244" style="width:100%;" oninput="updateRGB()" />
            </div>
          </div>
          <div class="callout" style="margin-top:auto;">Coba matikan semua ke <strong>0</strong> (jadi Hitam) atau naikkan semua ke <strong>255</strong> (jadi Putih)!</div>
        </div>
        <div class="card surface" style="align-items:center; justify-content:center; gap:14px;">
          <div id="rgb-swatch" style="width:190px; height:190px; border-radius:26px; background:rgb(66,133,244); box-shadow:0 12px 28px rgba(0,0,0,0.16); border:4px solid #FFF;"></div>
          <div id="rgb-code" style="font-family:var(--font-code); font-size:17px; font-weight:700;">Warna: (66, 133, 244)</div>
          <div style="display:flex; gap:8px; flex-wrap:wrap; justify-content:center;">
            <button class="btn-ui outline" onclick="setRGB(251,188,4)">Kuning</button>
            <button class="btn-ui outline" onclick="setRGB(234,67,53)">Merah</button>
            <button class="btn-ui outline" onclick="setRGB(0,0,0)">Hitam</button>
            <button class="btn-ui outline" onclick="setRGB(255,255,255)">Putih</button>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>14 / 54</span></div>
    </section>

    <!-- 15: ABU-ABU VS WARNA -->
    <section class="slide" data-title="Foto Abu-abu (Grayscale) vs Foto Warna (RGB)" data-notes="Alokasi waktu: 1 menit. Jelaskan kapan kita pakai abu-abu (1 lapis angka) dan kapan kita wajib pakai warna (3 lapis angka).">
      <div class="kicker">BAB 1 · GRAYSCALE VS RGB</div>
      <h2><span class="hl-blue">Grayscale</span> (1 Channel) vs <span class="hl-red">RGB</span> (3 Channels)</h2>
      <div class="split-60-40">
        <div class="img-box">
          <img src="assets/P01/04_grayscale_vs_rgb.png" alt="Perbandingan RGB dan Grayscale" />
        </div>
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Beda Jumlah Channel Warna</div>
          <div class="card-body">
            <ul>
              <li><strong>Grayscale (Abu-abu):</strong> Hanya punya <strong>1 channel</strong> (mengukur terang-gelap saja). Cocok saat kita cuma ingin mengukur <em>brightness</em> atau mendeteksi <em>edges</em> (tepi objek).</li>
              <li><strong>RGB (Warna):</strong> Punya <strong>3 channels</strong> (Red, Green, Blue). Wajib dipakai saat mengenali karakter, buah, rambu, atau benda yang warnanya jadi ciri khas!</li>
            </ul>
          </div>
          <div class="callout yellow"><strong>Tips:</strong> Untuk melatih AI pengenalan objek nyata, gunakan format <strong>RGB</strong> agar informasi warnanya tidak hilang.</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>15 / 54</span></div>
    </section>

    <!-- 16: PEMISAHAN 3 RGB CHANNELS -->
    <section class="slide" data-title="Mengintip 3 RGB Channels dalam 1 Foto" data-notes="Alokasi waktu: 1 menit. Tunjukkan gambar nyata pemisahan R, G, B channel: area yang berwarna merah menyala paling terang di channel R.">
      <div class="kicker">BAB 1 · RGB CHANNELS</div>
      <h2>Mengintip <span class="hl-blue">3 RGB Channels</span> dalam 1 Foto</h2>
      <div class="img-box" style="flex:1; padding:12px;">
        <img src="assets/P01/05_rgb_channels.png" alt="Pemisahan channel R G B" />
      </div>
      <div class="callout" style="margin-top:10px;">
        <strong>Cara membacanya:</strong> Area yang berwarna terang pada <em>Channel R (Red)</em> berarti memiliki intensitas <em>Red</em> yang tinggi. Tiga <em>channel</em> inilah yang digabung menjadi satu foto penuh warna.
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>16 / 54</span></div>
    </section>

    <!-- 17: QA REVEAL #2 -->
    <section class="slide" data-title="Tanya-Jawab #2: Kapan Warna Jadi Penentu?" data-notes="Alokasi waktu: 1.5 menit. Tanya peserta mengapa foto warna jauh lebih membantu AI dibanding hitam-putih.">
      <div class="kicker">TANYA &amp; JAWAB INTERAKTIF · #2</div>
      <h2>Coba Pikirkan: <span class="hl-green">Pentingkah Warna</span> Bagi AI?</h2>
      <div class="split-60-40">
        <div class="qa-box" style="margin:0; justify-content:center;">
          <div class="qa-question">
            Bayangkan kita melatih AI untuk membedakan <strong>Jeruk Matang</strong> vs <strong>Jeruk Mentah</strong>, atau dua karakter kartun yang bentuk tubuhnya mirip tapi bajunya beda warna. Apa yang terjadi jika fotonya kita ubah menjadi <em>grayscale</em> semua?
          </div>
          <div class="qa-choices">
            <div class="qa-choice"><strong>A.</strong> Tidak masalah, AI tetap mudah membedakannya.</div>
            <div class="qa-choice"><strong>B.</strong> AI akan kebingungan karena petunjuk warnanya hilang!</div>
            <div class="qa-choice"><strong>C.</strong> AI justru bekerja lebih lambat.</div>
          </div>
          <button class="btn-ui" onclick="toggleQA('qa2', this)">Klik untuk Lihat Jawaban &amp; Penjelasan</button>
          <div id="qa2" class="qa-answer">
            <strong>Jawaban: B — AI akan kebingungan karena petunjuk warnanya hilang!</strong><br />
            Di foto <em>grayscale</em>, warna oranye cerah dan hijau muda bisa memiliki intensitas abu-abu yang hampir sama. Karena itu, untuk mengenali benda atau karakter sehari-hari, kita menjaga foto tetap dalam format <strong>warna (RGB)</strong>.
          </div>
        </div>
        <div class="card surface" style="align-items:center; justify-content:center; padding:16px;">
          <svg id="qa2-vis" viewBox="0 0 320 265" style="width:100%; height:100%; max-height:360px;">
            <rect x="10" y="10" width="300" height="114" rx="14" fill="#FFFFFF" stroke="#E0E3E7" stroke-width="2"/>
            <text x="160" y="30" text-anchor="middle" font-size="12" font-weight="700" fill="#137333">FORMAT RGB (BERWARNA)</text>
            <circle cx="88" cy="72" r="28" fill="#FB8C00"/>
            <ellipse cx="96" cy="43" rx="10" ry="5" fill="#34A853" transform="rotate(-20 96 43)"/>
            <text x="88" y="114" text-anchor="middle" font-size="11" font-weight="700" fill="#202124">Matang (255, 140, 0)</text>
            <circle cx="232" cy="72" r="28" fill="#5BB974"/>
            <ellipse cx="240" cy="43" rx="10" ry="5" fill="#1E8E3E" transform="rotate(-20 240 43)"/>
            <text x="232" y="114" text-anchor="middle" font-size="11" font-weight="700" fill="#202124">Mentah (91, 185, 116)</text>
            <text x="160" y="77" text-anchor="middle" font-size="14" font-weight="700" fill="#34A853">≠ Jelas</text>

            <g class="vis-q">
              <rect x="10" y="140" width="300" height="114" rx="14" fill="#FFFFFF" stroke="#BDC1C6" stroke-width="2" stroke-dasharray="6 4"/>
              <text x="160" y="164" text-anchor="middle" font-size="12" font-weight="700" fill="#5F6368">JIKA DIUBAH KE GRAYSCALE...</text>
              <circle cx="160" cy="202" r="26" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
              <text x="160" y="210" text-anchor="middle" font-size="22" font-weight="700" fill="#1A73E8">?</text>
              <text x="160" y="244" text-anchor="middle" font-size="11" font-weight="600" fill="#5F6368">Klik tombol di kiri untuk melihat hasil grayscale</text>
            </g>
            <g class="vis-a">
              <rect x="10" y="140" width="300" height="114" rx="14" fill="#FFFFFF" stroke="#EA4335" stroke-width="2"/>
              <text x="160" y="160" text-anchor="middle" font-size="12" font-weight="700" fill="#C5221F">DIUBAH KE GRAYSCALE</text>
              <circle cx="88" cy="202" r="28" fill="#9A9A9A"/>
              <ellipse cx="96" cy="173" rx="10" ry="5" fill="#757575" transform="rotate(-20 96 173)"/>
              <text x="88" y="244" text-anchor="middle" font-size="11" font-weight="700" fill="#5F6368">Gray ≈ 154</text>
              <circle cx="232" cy="202" r="28" fill="#959595"/>
              <ellipse cx="240" cy="173" rx="10" ry="5" fill="#6E6E6E" transform="rotate(-20 240 173)"/>
              <text x="232" y="244" text-anchor="middle" font-size="11" font-weight="700" fill="#5F6368">Gray ≈ 149</text>
              <text x="160" y="207" text-anchor="middle" font-size="16" font-weight="700" fill="#EA4335">≈ Mirip!</text>
            </g>
          </svg>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>17 / 54</span></div>
    </section>

    <!-- 18: DIVIDER BAB 2 -->
    <section class="slide bg-red" data-title="Bab 2: Mengapa Kita Perlu Image Processing?" data-notes="Alokasi waktu: 0.5 menit. Sekarang kita sudah tahu foto = angka. Lalu kenapa tidak langsung kita masukkan saja ke AI? Ini jawabannya!">
      <div class="divider-center">
        <span class="pill dark">BAB 2 · KENAPA IMAGE PROCESSING PENTING</span>
        <h1>Mengapa Kita Perlu Belajar Image Processing?</h1>
        <p>Foto mentah dari kamera HP penuh ketidakteraturan. Tanpa dirapikan terlebih dahulu, AI akan kesulitan belajar dan mudah salah menebak.</p>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>18 / 54</span></div>
    </section>

    <!-- 19: MENGAPA IMAGE PROCESSING PENTING -->
    <section class="slide" data-title="Mengapa Foto Mentah Perlu Preprocessing?" data-notes="Alokasi waktu: 1.5 menit. Jelaskan langsung alasan praktisnya tanpa analogi yang dipaksakan: kamera HP memotret untuk mata manusia, bukan untuk mesin.">
      <div class="kicker">BAB 2 · ALASAN UTAMA</div>
      <h2>Mengapa Foto Mentah Perlu <span class="hl-blue">Preprocessing</span>?</h2>
      <p class="subtitle">Kamera HP menghasilkan foto untuk dilihat mata manusia, bukan untuk dihitung mesin. Agar AI belajar akurat, inputnya harus seragam.</p>
      <div class="grid-3">
        <div class="card tint-red">
          <div class="card-top-bar bar-red"></div>
          <span class="pill red">MASALAH FOTO MENTAH</span>
          <div class="card-title">1. Resolution Acak</div>
          <div class="card-body">Foto dari kamera HP berbeda-beda ukurannya (ada yang kotak, ada yang panjang). AI hanya bisa menerima ukuran yang <strong>sama persis</strong>.</div>
          <svg viewBox="0 0 220 75" style="width:100%; max-height:74px; margin-top:auto;">
            <rect x="10" y="16" width="54" height="42" rx="6" fill="#FFFFFF" stroke="#EA4335" stroke-width="2"/>
            <rect x="78" y="8" width="42" height="58" rx="6" fill="#FFFFFF" stroke="#EA4335" stroke-width="2"/>
            <rect x="134" y="22" width="74" height="32" rx="6" fill="#FFFFFF" stroke="#EA4335" stroke-width="2"/>
            <text x="37" y="41" text-anchor="middle" font-size="9.5" fill="#C5221F">4:3</text>
            <text x="99" y="41" text-anchor="middle" font-size="9.5" fill="#C5221F">9:16</text>
            <text x="171" y="42" text-anchor="middle" font-size="9.5" fill="#C5221F">16:9</text>
          </svg>
        </div>
        <div class="card tint-yellow">
          <div class="card-top-bar bar-yellow"></div>
          <span class="pill yellow">MASALAH FOTO MENTAH</span>
          <div class="card-title">2. Skala Angka Terlalu Besar</div>
          <div class="card-body">Angka <code>0–255</code> terlalu lebar bagi perhitungan AI. Perlu <em>Normalization</em> ke skala kecil (<code>0–1</code>) agar AI belajar dengan stabil.</div>
          <svg viewBox="0 0 220 75" style="width:100%; max-height:74px; margin-top:auto;">
            <rect x="10" y="18" width="84" height="36" rx="8" fill="#FFFFFF" stroke="#FBBC04" stroke-width="2"/>
            <text x="52" y="40" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="11.5" font-weight="700" fill="#B06000">0 – 255</text>
            <path d="M100 36 L122 36" stroke="#B06000" stroke-width="2.5"/><polygon points="120,31 129,36 120,41" fill="#B06000"/>
            <rect x="132" y="18" width="78" height="36" rx="8" fill="#34A853"/>
            <text x="171" y="40" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="11.5" font-weight="700" fill="#FFF">0 – 1</text>
          </svg>
        </div>
        <div class="card tint-blue">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">MASALAH FOTO MENTAH</span>
          <div class="card-title">3. Kejutan Tersembunyi</div>
          <div class="card-body">Ada foto yang miring (<em>EXIF</em>), terlalu gelap, berlatar ramai, atau <em>corrupted file</em>. Semua ini harus diaudit dan dibersihkan dulu!</div>
          <svg viewBox="0 0 220 75" style="width:100%; max-height:74px; margin-top:auto;">
            <rect x="16" y="16" width="52" height="42" rx="6" fill="#FFFFFF" stroke="#4285F4" stroke-width="2" transform="rotate(-8 42 37)"/>
            <text x="42" y="41" text-anchor="middle" font-size="9.5" font-weight="700" fill="#1A73E8">EXIF</text>
            <rect x="84" y="16" width="52" height="42" rx="6" fill="#202124"/>
            <text x="110" y="41" text-anchor="middle" font-size="9.5" font-weight="700" fill="#FBBC04">Gelap</text>
            <rect x="152" y="16" width="52" height="42" rx="6" fill="#FFFFFF" stroke="#EA4335" stroke-width="2"/>
            <path d="M168 28 L188 46 M188 28 L168 46" stroke="#EA4335" stroke-width="2.5"/>
          </svg>
        </div>
      </div>
      <div class="callout green" style="margin-top:12px;">
        <strong>Intinya:</strong> <em>Image Processing</em> melakukan <em>resize</em>, menyetarakan skala angka, dan standar kualitas foto sebelum masuk ke tahap pelatihan AI.
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>19 / 54</span></div>
    </section>

    <!-- 20: ALASAN 1 - UKURAN & ASPECT RATIO -->
    <section class="slide" data-title="Alasan 1: Resize &amp; Uniform Resolution" data-notes="Alokasi waktu: 1 menit. Jelaskan kenapa foto dari kamera HP harus diseragamkan ukurannya (misal 224x224) sebelum masuk ke AI.">
      <div class="kicker">BAB 2 · UNIFORM RESOLUTION</div>
      <h2>Resize &amp; Uniform <span class="hl-blue">Resolution</span></h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Mengapa Ukurannya Harus Sama?</div>
          <div class="card-body">
            <ul>
              <li>Foto jepretan HP modern biasanya sangat besar (ribuan pixel lebar dan tingginya).</li>
              <li>Foto kiriman WhatsApp ukurannya lebih kecil karena sudah dikompresi.</li>
              <li>Model AI bekerja seperti pintu gerbang dengan cetakan pas — semua foto yang masuk harus punya <strong>lebar dan tinggi yang sama</strong> (contoh populer: <code>224 × 224</code> kotak).</li>
            </ul>
          </div>
          <div class="callout">Selain adil, ukuran <code>224 × 224</code> cukup ringan sehingga komputer bisa melatih ratusan foto dengan cepat!</div>
        </div>
        <div class="card surface">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title">Masalah Aspect Ratio yang Berbeda</div>
          <div class="card-body">
            <ul>
              <li>Dataset kita berisi foto dengan rasio beragam, sedangkan input model AI berbentuk <strong>persegi sama sisi</strong>.</li>
              <li>Kalau ada foto yang lebar memanjang (landscape) atau tinggi memanjang (portrait), bagaimana cara memasukkannya ke bingkai persegi?</li>
              <li>Hati-hati: jika dipaksa di-<em>stretch</em> begitu saja, bentuk objek menjadi <strong>distorted</strong>!</li>
            </ul>
          </div>
          <svg viewBox="0 0 360 70" style="width:100%; max-height:68px; margin-top:auto;">
            <rect x="8" y="14" width="58" height="40" rx="6" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
            <rect x="76" y="10" width="38" height="48" rx="6" fill="#FCE8E6" stroke="#EA4335" stroke-width="2"/>
            <path d="M126 34 L196 34" stroke="#34A853" stroke-width="3" stroke-linecap="round"/><polygon points="194,28 206,34 194,40" fill="#34A853"/>
            <text x="164" y="25" text-anchor="middle" font-size="10" font-weight="700" fill="#137333">Resize</text>
            <rect x="216" y="8" width="52" height="52" rx="8" fill="#34A853"/>
            <text x="242" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="#FFF">224²</text>
            <rect x="278" y="8" width="52" height="52" rx="8" fill="#34A853"/>
            <text x="304" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="#FFF">224²</text>
          </svg>
          <div class="callout yellow">Di slide berikutnya kita lihat dampak <em>distorted aspect ratio</em> secara langsung!</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>20 / 54</span></div>
    </section>

    <!-- 21: BAHAYA GAMBAR GEPENG (ASPECT RATIO) -->
    <section class="slide" data-title="Bahaya Memaksa Foto Menjadi Gepeng" data-notes="Alokasi waktu: 1.5 menit. Tunjukkan gambar nyata: lingkaran sempurna menjadi lonjong/elips jika ditarik paksa tanpa menjaga proporsi.">
      <div class="kicker">BAB 2 · MENJAGA PROPORSI</div>
      <h2>Jangan Sampai Foto <span class="hl-red">Menjadi Distorted!</span></h2>
      <div class="img-box" style="flex:1; padding:12px;">
        <img src="assets/P01/06_resize_aspect_ratio.png" alt="Perbandingan aspect ratio benar vs gepeng" />
      </div>
      <div class="grid-2" style="flex:0 0 auto; margin-top:10px;">
        <div class="callout red"><strong>Cara Salah (Tarik Paksa):</strong> Lingkaran berubah menjadi lonjong. AI bisa salah mengira itu benda lain!</div>
        <div class="callout green"><strong>Cara Benar (Tambah Tepi / Potong Rapi):</strong> Menambah ruang kosong di sisi atau memotong tepi agar bentuk aslinya tetap utuh.</div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>21 / 54</span></div>
    </section>

    <!-- 22: ALASAN 2 - MENYAMAKAN SKALA ANGKA (NORMALISASI) -->
    <section class="slide" data-title="Alasan 2: Menyetarakan Skala Angka (Normalisasi)" data-notes="Alokasi waktu: 1 menit. Jelaskan normalisasi dengan analogi satuan berat (gram ke kilogram) agar orang non-IT langsung paham.">
      <div class="kicker">BAB 2 · NORMALIZATION</div>
      <h2>Menyetarakan Skala Angka (<span class="hl-green">Normalization</span>)</h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Mengapa Angka 0–255 Perlu Diperkecil?</div>
          <div class="card-body">
            <ul>
              <li>Komputer menyimpan <em>brightness</em> dalam angka <strong>0 sampai 255</strong>.</li>
              <li>Saat AI berhitung, angka ratusan (misal 250) terlalu besar dan membuat proses belajarnya tidak stabil.</li>
              <li>Maka seluruh angka kita bagi dengan 255, sehingga skalanya berubah menjadi <strong>0.0 sampai 1.0</strong>.</li>
            </ul>
          </div>
          <div class="callout green">Tujuannya sederhana: menjaga agar perhitungan di dalam model AI tetap stabil, cepat, dan tidak melonjak karena angka ratusan.</div>
        </div>
        <div class="card surface">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Dua Skala yang Sering Dipakai AI</div>
          <div class="card-body">
            <ul>
              <li><strong>Skala 0 sampai 1:</strong> Paling mudah dipahami (0 = gelap total, 0.5 = setengah terang, 1.0 = terang penuh).</li>
              <li><strong>Skala −1 sampai +1:</strong> Dipakai oleh beberapa model AI modern populer (seperti MobileNetV2) agar titik tengahnya tepat berada di angka <code>0</code>.</li>
            </ul>
            <svg viewBox="0 0 360 112" style="width:100%; height:105px; margin-top:10px;">
              <rect x="0" y="0" width="360" height="112" rx="12" fill="#FFFFFF" stroke="#E0E3E7" stroke-width="1.5"/>
              <text x="16" y="25" font-size="11" font-weight="700" fill="#5F6368">Asli (uint8)</text>
              <line x1="110" y1="21" x2="340" y2="21" stroke="#BDC1C6" stroke-width="4" stroke-linecap="round"/>
              <circle cx="110" cy="21" r="5" fill="#202124"/><text x="110" y="38" text-anchor="middle" font-size="10" font-weight="700" fill="#202124">0</text>
              <circle cx="225" cy="21" r="5" fill="#4285F4"/><text x="225" y="38" text-anchor="middle" font-size="10" font-weight="700" fill="#1A73E8">128</text>
              <circle cx="340" cy="21" r="5" fill="#202124"/><text x="340" y="38" text-anchor="middle" font-size="10" font-weight="700" fill="#202124">255</text>

              <text x="16" y="64" font-size="11" font-weight="700" fill="#137333">÷ 255 (0–1)</text>
              <line x1="110" y1="60" x2="340" y2="60" stroke="#A8DAB5" stroke-width="4" stroke-linecap="round"/>
              <circle cx="110" cy="60" r="5" fill="#34A853"/><text x="110" y="77" text-anchor="middle" font-size="10" font-weight="700" fill="#137333">0.0</text>
              <circle cx="225" cy="60" r="5" fill="#34A853"/><text x="225" y="77" text-anchor="middle" font-size="10" font-weight="700" fill="#137333">0.5</text>
              <circle cx="340" cy="60" r="5" fill="#34A853"/><text x="340" y="77" text-anchor="middle" font-size="10" font-weight="700" fill="#137333">1.0</text>

              <text x="16" y="99" font-size="11" font-weight="700" fill="#1A73E8">MobileNetV2</text>
              <line x1="110" y1="95" x2="340" y2="95" stroke="#AECBFA" stroke-width="4" stroke-linecap="round"/>
              <circle cx="110" cy="95" r="5" fill="#4285F4"/><text x="110" y="109" text-anchor="middle" font-size="9.5" font-weight="700" fill="#1A73E8">-1.0</text>
              <circle cx="225" cy="95" r="5" fill="#4285F4"/><text x="225" y="109" text-anchor="middle" font-size="9.5" font-weight="700" fill="#1A73E8">0.0</text>
              <circle cx="340" cy="95" r="5" fill="#4285F4"/><text x="340" y="109" text-anchor="middle" font-size="9.5" font-weight="700" fill="#1A73E8">+1.0</text>
            </svg>
          </div>
          <div class="callout">Anda tidak perlu menghafal rumusnya — sistem AI modern sudah menyediakan tombol otomatis untuk ini!</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>22 / 54</span></div>
    </section>

    <!-- 23: INTERACTIVE NORMALIZATION CALCULATOR -->
    <section class="slide" data-title="Eksperimen: Kalkulator Penyetara Skala" data-notes="Alokasi waktu: 1.5 menit. Ajak peserta menggeser slider brightness untuk melihat bagaimana angka asli 0-255 berubah menjadi skala 0-1 dan -1 sampai +1.">
      <div class="kicker">BAB 2 · EKSPERIMEN INTERAKTIF</div>
      <h2>Coba Sendiri: <span class="hl-blue">Normalization Calculator</span></h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Geser Nilai Intensitas Pixel (0–255)</div>
          <input id="norm-sl" type="range" min="0" max="255" value="128" style="width:100%; margin:12px 0;" oninput="updateNorm()" />
          <div class="grid-3" style="flex:0 0 auto; gap:10px;">
            <div class="card surface" style="padding:12px; align-items:center;"><div style="font-size:12px; color:var(--muted);">Angka Asli</div><div id="n-u8" class="big-num" style="font-size:26px;">128</div></div>
            <div class="card surface" style="padding:12px; align-items:center;"><div style="font-size:12px; color:var(--muted);">Skala 0–1</div><div id="n-01" class="big-num hl-green" style="font-size:26px;">0.502</div></div>
            <div class="card surface" style="padding:12px; align-items:center;"><div style="font-size:12px; color:var(--muted);">Skala −1–1</div><div id="n-11" class="big-num hl-blue" style="font-size:26px;">0.004</div></div>
          </div>
          <div class="callout" style="margin-top:auto;">Perhatikan: saat angka asli di tengah (<code>128</code>), skala 0–1 menjadi sekitar <code>0.5</code> dan skala −1–1 mendekati <code>0</code>!</div>
        </div>
        <div class="card">
          <div class="card-top-bar bar-yellow"></div>
          <span class="pill yellow">CATATAN PRAKTIS</span>
          <div class="card-title">Di Balik Layar Sistem AI</div>
          <div class="card-body">Saat memakai model AI siap pakai nantinya, kita tidak perlu menghitung manual satu per satu. Cukup panggil satu fungsi bawaan:</div>
          <pre class="code"><code>from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
foto_siap = preprocess_input(foto_asli)</code></pre>
          <div class="callout yellow">Yang terpenting: <strong>aturan skala harus sama persis</strong> antara saat AI belajar dan saat AI diuji!</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>23 / 54</span></div>
    </section>

    <!-- 24: ANGKA BULAT VS DESIMAL -->
    <section class="slide" data-title="Mengapa Perlu Angka Desimal?" data-notes="Alokasi waktu: 1 menit. Jelaskan uint8 vs float32 secara sederhana: kamera menyimpan angka bulat agar hemat kuota/memori, sedangkan AI menghitung dengan angka desimal agar akurat.">
      <div class="kicker">BAB 2 · DATA TYPE</div>
      <h2><span class="hl-blue">uint8</span> (Integer) vs <span class="hl-green">float32</span> (Floating-Point)</h2>
      <div class="grid-2">
        <div class="card surface">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">SAAT DISIMPAN DI HP (UINT8)</span>
          <div class="card-title">Integer: 0, 1, 2, ..., 255</div>
          <div class="card-body">
            <ul>
              <li>Kamera HP memakai <em>integer</em> tanpa koma agar ukuran file foto <strong>kecil dan hemat memori</strong>.</li>
              <li>Istilah komputernya adalah <code>uint8</code>.</li>
              <li><strong>Kekurangannya:</strong> Tidak bisa menyimpan angka <em>decimal</em> seperti <code>0.5</code>!</li>
            </ul>
            <svg viewBox="0 0 320 62" style="width:100%; height:60px; margin-top:8px;">
              <rect x="0" y="0" width="320" height="62" rx="10" fill="#FFFFFF" stroke="#E0E3E7"/>
              <polyline points="20,48 75,48 75,34 140,34 140,20 215,20 215,10 300,10" fill="none" stroke="#4285F4" stroke-width="3"/>
              <text x="160" y="57" text-anchor="middle" font-size="10.5" font-weight="700" fill="#1A73E8">Tangga Kasar: hanya lompat 0, 1, 2, ..., 255</text>
            </svg>
          </div>
          <div class="callout">Contoh nilai pixel: <code>[0, 128, 255]</code> (hanya <em>integer</em>).</div>
        </div>
        <div class="card">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">SAAT DIHITUNG OLEH AI (FLOAT32)</span>
          <div class="card-title">Floating-Point: 0.000, 0.502, 1.000</div>
          <div class="card-body">
            <ul>
              <li>Untuk menyetarakan skala ke <code>0–1</code>, angka harus bisa memakai koma (desimal).</li>
              <li>Istilah komputernya adalah <code>float32</code>.</li>
              <li><strong>Aturannya:</strong> Ubah dulu ke mode <em>floating-point</em> sebelum dibagi 255 agar nilai decimalnya tidak hilang terpotong menjadi nol!</li>
            </ul>
            <svg viewBox="0 0 320 62" style="width:100%; height:60px; margin-top:8px;">
              <rect x="0" y="0" width="320" height="62" rx="10" fill="#F8F9FA" stroke="#E0E3E7"/>
              <line x1="20" y1="48" x2="300" y2="10" stroke="#34A853" stroke-width="3" stroke-linecap="round"/>
              <text x="160" y="57" text-anchor="middle" font-size="10.5" font-weight="700" fill="#137333">Garis Halus: bisa nilai 0.000, 0.502, 1.000</text>
            </svg>
          </div>
          <div class="callout green">Contoh setelah dibagi 255: <code>[0.000, 0.502, 1.000]</code> (halus &amp; presisi).</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>24 / 54</span></div>
    </section>

    <!-- 25: QA REVEAL #3 -->
    <section class="slide" data-title="Tanya-Jawab #3: Dampak Aspect Ratio Terdistorsi" data-notes="Alokasi waktu: 1.5 menit. Pertanyaan refleksi penutup Bab 2 sebelum masuk ke EDA.">
      <div class="kicker">TANYA &amp; JAWAB INTERAKTIF · #3</div>
      <h2>Coba Tebak: <span class="hl-red">Apa Jadinya</span> Jika Aspect Ratio Terdistorsi?</h2>
      <div class="split-60-40">
        <div class="qa-box" style="margin:0; justify-content:center;">
          <div class="qa-question">
            Kita punya foto bola basket yang bulat sempurna dalam bingkai memanjang (persegi panjang). Jika kita langsung memaksa menyusutkannya menjadi kotak persegi <code>224 × 224</code> tanpa menjaga proporsi, apa yang terjadi?
          </div>
          <div class="qa-choices">
            <div class="qa-choice"><strong>A.</strong> Bola tetap bulat sempurna.</div>
            <div class="qa-choice"><strong>B.</strong> Bola berubah lonjong seperti bola rugbi/telur!</div>
            <div class="qa-choice"><strong>C.</strong> Warnanya berubah menjadi <em>grayscale</em>.</div>
          </div>
          <button class="btn-ui" onclick="toggleQA('qa3', this)">Klik untuk Lihat Jawaban &amp; Penjelasan</button>
          <div id="qa3" class="qa-answer">
            <strong>Jawaban: B — Bola berubah lonjong seperti bola rugbi atau telur!</strong><br />
            Akibatnya, AI mempelajari bentuk yang salah. Jika suatu saat melihat foto bola basket asli yang bulat, AI bisa ragu atau salah menebak. Karena itu, menjaga proporsi asli foto sangat penting dalam Image Processing!
          </div>
        </div>
        <div class="card surface" style="align-items:center; justify-content:center; padding:16px;">
          <svg id="qa3-vis" viewBox="0 0 320 265" style="width:100%; height:100%; max-height:360px;">
            <text x="160" y="20" text-anchor="middle" font-size="12" font-weight="700" fill="#137333">FOTO ASLI (16:9 PERSEGI PANJANG)</text>
            <rect x="40" y="28" width="240" height="86" rx="12" fill="#FFFFFF" stroke="#34A853" stroke-width="2.5"/>
            <circle cx="160" cy="71" r="32" fill="#FB8C00" stroke="#202124" stroke-width="2"/>
            <path d="M 128 71 H 192 M 160 39 V 103" stroke="#202124" stroke-width="1.8" fill="none"/>

            <path d="M 160 120 V 142" stroke="#EA4335" stroke-width="3" stroke-linecap="round"/>
            <polygon points="154,138 166,138 160,147" fill="#EA4335"/>
            <text x="232" y="137" text-anchor="middle" font-size="11" font-weight="700" fill="#EA4335">Dipaksa jadi 224×224</text>

            <g class="vis-q">
              <rect x="104" y="152" width="112" height="104" rx="12" fill="#FFFFFF" stroke="#4285F4" stroke-width="2.5" stroke-dasharray="6 4"/>
              <text x="160" y="214" text-anchor="middle" font-size="36" font-weight="700" fill="#1A73E8">?</text>
            </g>
            <g class="vis-a">
              <rect x="104" y="152" width="112" height="104" rx="12" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.5"/>
              <ellipse cx="160" cy="204" rx="22" ry="38" fill="#FB8C00" stroke="#202124" stroke-width="2"/>
              <path d="M 138 204 H 182 M 160 166 V 242" stroke="#202124" stroke-width="1.8" fill="none"/>
              <rect x="224" y="188" width="84" height="28" rx="14" fill="#EA4335"/>
              <text x="266" y="206" text-anchor="middle" font-size="11.5" font-weight="700" fill="#FFFFFF">Distorted!</text>
            </g>
          </svg>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>25 / 54</span></div>
    </section>

    <!-- 26: DIVIDER BAB 3 -->
    <section class="slide bg-green" data-title="Bab 3: Exploratory Data Analysis (EDA)" data-notes="Alokasi waktu: 0.5 menit. Sekarang kita masuk ke Bab 3: melakukan Exploratory Data Analysis (EDA) pada dataset foto sebelum dipakai melatih AI.">
      <div class="divider-center">
        <span class="pill dark">BAB 3 · EXPLORATORY DATA ANALYSIS (EDA)</span>
        <h1>Exploratory Data Analysis (EDA)</h1>
        <p>Mengenal isi, distribusi, dan kualitas dataset foto sebelum melakukan <em>training</em> model AI.</p>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>26 / 54</span></div>
    </section>

    <!-- 27: APA ITU EDA -->
    <section class="slide" data-title="Apa Itu Exploratory Data Analysis (EDA)?" data-notes="Alokasi waktu: 1.5 menit. Jelaskan Exploratory Data Analysis (EDA) sebagai langkah memeriksa kondisi dataset sebelum training model.">
      <div class="kicker">BAB 3 · MENGAPA PERLU EDA</div>
      <h2>Kualitas Model Bergantung pada <span class="hl-green">Kualitas Data</span></h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Apa Itu EDA (Exploratory Data Analysis)?</div>
          <div class="card-body">
            <ul>
              <li>Proses <strong>mengaudit kondisi dataset foto</strong> secara menyeluruh sebelum diberikan ke model AI.</li>
              <li>Tujuannya memahami distribusi jumlah foto, pencahayaan, dan potensi masalah sejak awal.</li>
              <li>Di tahap ini kita <strong>hanya mengamati dan mencatat fakta</strong> — belum melatih model sama sekali.</li>
            </ul>
          </div>
          <div class="callout green">Prinsip utama Machine Learning: <strong>Garbage In, Garbage Out</strong> — data yang berantakan akan menghasilkan prediksi yang buruk.</div>
        </div>
        <div class="card surface">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">4 Pertanyaan Wajib Saat Cek Foto</div>
          <div class="card-body">
            <ul>
              <li><strong>1. Adilkah jumlahnya?</strong> Jangan sampai satu jenis punya 100 foto, jenis lain cuma 5 foto.</li>
              <li><strong>2. Bagaimana cahayanya?</strong> Apakah terlalu gelap, terlalu silau, atau pas?</li>
              <li><strong>3. Seberapa ramai latarnya?</strong> Apakah polos rapi atau penuh benda lain?</li>
              <li><strong>4. Ada foto bermasalah?</strong> Apakah ada <em>corrupted file</em>, <em>duplicate</em>, atau terbalik (<em>EXIF</em>)?</li>
            </ul>
          </div>
          <svg viewBox="0 0 360 72" style="width:100%; max-height:70px; margin-top:auto;">
            <rect x="8" y="14" width="96" height="44" rx="8" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.8"/>
            <text x="56" y="40" text-anchor="middle" font-size="11" font-weight="700" fill="#C5221F">Data Berantakan</text>
            <path d="M112 36 L142 36" stroke="#EA4335" stroke-width="2.5"/><polygon points="140,31 150,36 140,41" fill="#EA4335"/>
            <rect x="154" y="14" width="60" height="44" rx="8" fill="#202124"/>
            <text x="184" y="40" text-anchor="middle" font-size="11" font-weight="700" fill="#FBBC04">AI</text>
            <path d="M222 36 L252 36" stroke="#EA4335" stroke-width="2.5"/><polygon points="250,31 260,36 250,41" fill="#EA4335"/>
            <rect x="264" y="14" width="88" height="44" rx="8" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.8"/>
            <text x="308" y="40" text-anchor="middle" font-size="11" font-weight="700" fill="#C5221F">Tebakan Ngawur</text>
          </svg>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>27 / 54</span></div>
    </section>

    <!-- 28: CLASS IMBALANCE -->
    <section class="slide" data-title="Masalah #1: Jumlah Foto Tidak Seimbang" data-notes="Alokasi waktu: 1 menit. Analogi belajar ujian: jika 90% latihan soal A, saat bingung murid akan selalu menebak A.">
      <div class="kicker">BAB 3 · KESEIMBANGAN DATA</div>
      <h2>Waspada Jika Jumlah Foto <span class="hl-red">Tidak Seimbang</span></h2>
      <div class="grid-2">
        <div class="card tint-red">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title">Analogi Latihan Soal Ujian</div>
          <div class="card-body">
            <ul>
              <li>Bayangkan Anda berlatih 95 soal tentang <strong>Kucing</strong>, dan hanya 5 soal tentang <strong>Anjing</strong>.</li>
              <li>Saat ujian muncul foto yang agak kabur, Anda pasti cenderung menebak "Kucing" karena lebih sering melihatnya!</li>
              <li>Hal yang persis sama terjadi pada AI jika jumlah fotonya timpang (istilahnya: <em>Class Imbalance</em>).</li>
            </ul>
          </div>
          <svg viewBox="0 0 360 90" style="width:100%; max-height:88px; margin-top:auto;">
            <text x="4" y="24" font-family="Roboto, sans-serif" font-size="12" font-weight="700" fill="#C5221F">Kucing (95)</text>
            <rect x="95" y="10" width="245" height="18" rx="6" fill="#EA4335"/>
            <text x="4" y="64" font-family="Roboto, sans-serif" font-size="12" font-weight="700" fill="#5F6368">Anjing (5)</text>
            <rect x="95" y="50" width="18" height="18" rx="6" fill="#FBBC04"/>
            <text x="122" y="64" font-family="Roboto, sans-serif" font-size="11.5" fill="#C5221F">AI cenderung menebak Kucing terus!</text>
          </svg>
        </div>
        <div class="card">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Kondisi pada Data Sampel Kita</div>
          <div class="card-body">
            <ul>
              <li>Dalam dataset sampel latihan kita, terdapat <strong>5 jenis bentuk</strong> × <strong>2 kondisi latar (polos &amp; ramai)</strong>.</li>
              <li>Setiap kelompok disiapkan <strong>12 foto</strong> (total 120 file), sehingga sangat seimbang!</li>
              <li>Satu-satunya selisih kecil muncul karena ada 1 file yang sengaja dibuat rusak untuk latihan deteksi.</li>
            </ul>
          </div>
          <svg viewBox="0 0 360 72" style="width:100%; max-height:70px;">
            <rect x="6" y="14" width="62" height="22" rx="6" fill="#4285F4"/><text x="37" y="29" text-anchor="middle" font-size="11" font-weight="700" fill="#FFF">12</text>
            <rect x="76" y="14" width="62" height="22" rx="6" fill="#34A853"/><text x="107" y="29" text-anchor="middle" font-size="11" font-weight="700" fill="#FFF">12</text>
            <rect x="146" y="14" width="62" height="22" rx="6" fill="#FBBC04"/><text x="177" y="29" text-anchor="middle" font-size="11" font-weight="700" fill="#202124">12</text>
            <rect x="216" y="14" width="62" height="22" rx="6" fill="#EA4335"/><text x="247" y="29" text-anchor="middle" font-size="11" font-weight="700" fill="#FFF">12</text>
            <rect x="286" y="14" width="62" height="22" rx="6" fill="#4285F4"/><text x="317" y="29" text-anchor="middle" font-size="11" font-weight="700" fill="#FFF">12</text>
            <text x="180" y="56" text-anchor="middle" font-family="Roboto, sans-serif" font-size="11.5" fill="#137333">5 kelas seimbang (per kondisi)</text>
          </svg>
          <div class="callout green">Selalu hitung jumlah foto di tiap folder kategori sebelum mulai melatih AI.</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>28 / 54</span></div>
    </section>

    <!-- 29: HISTOGRAM -->
    <section class="slide" data-title="Melihat Sebaran Cahaya dengan Grafik Histogram" data-notes="Alokasi waktu: 1.5 menit. Jelaskan histogram secara sederhana sebagai grafik penghitung seberapa banyak piksel gelap vs piksel terang.">
      <div class="kicker">BAB 3 · CEK PENCAHAYAAN</div>
      <h2>Grafik <span class="hl-blue">Histogram</span>: Cek Foto Terlalu Gelap / Silau</h2>
      <div class="split-60-40">
        <div class="img-box">
          <img src="assets/P01/07_histogram_brightness_contrast.png" alt="Histogram foto polos vs ramai" />
        </div>
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Cara Mudah Membaca Grafik Ini</div>
          <div class="card-body">
            <ul>
              <li><strong>Sisi Kiri (dekat 0):</strong> Banyak titik gelap / bayangan.</li>
              <li><strong>Tengah (100–160):</strong> Warna dan cahaya seimbang.</li>
              <li><strong>Sisi Kanan (dekat 255):</strong> Banyak area putih / sangat terang.</li>
            </ul>
          </div>
          <div class="callout"><strong>Contoh data sampel:</strong> Foto latar polos punya puncak tinggi di kanan (latar putih bersih), sedangkan foto latar ramai menyebar rata di tengah karena penuh warna!</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>29 / 54</span></div>
    </section>

    <!-- 30: BRIGHTNESS & CONTRAST -->
    <section class="slide" data-title="Mengukur Terang (Brightness) &amp; Kontras" data-notes="Alokasi waktu: 1.5 menit. Jelaskan hasil pengukuran nyata pada 119 foto sampel valid.">
      <div class="kicker">BAB 3 · BRIGHTNESS &amp; CONTRAST</div>
      <h2>Mengukur <span class="hl-blue">Brightness</span> &amp; <span class="hl-red">Contrast</span> Koleksi Foto</h2>
      <div class="split-60-40">
        <div class="img-box">
          <img src="assets/P01/07b_brightness_contrast_box.png" alt="Boxplot Brightness dan Contrast Polos vs Ramai" />
        </div>
        <div class="card">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">CONTOH DATA SAMPEL (119 FOTO VALID)</span>
          <div class="card-title">Temuan Nyata: Polos vs Ramai</div>
          <div class="card-body">
            <ul>
              <li><strong>Brightness (Rata-rata Intensitas):</strong><br />Polos: <strong>{polos['mean_brightness']:.2f}</strong> · Ramai: <strong>{ramai['mean_brightness']:.2f}</strong><br />Foto latar polos jauh lebih terang karena didominasi latar putih.</li>
              <li><strong>Contrast (Simpangan Baku):</strong><br />Polos: <strong>{polos['mean_contrast']:.2f}</strong> · Ramai: <strong>{ramai['mean_contrast']:.2f}</strong><br />Foto latar ramai lebih bervariasi gelap-terangnya.</li>
            </ul>
          </div>
          <div class="callout yellow">Jika perbedaan ini terlalu ekstrem, AI bisa menebak hanya dari terangnya foto!</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>30 / 54</span></div>
    </section>

    <!-- 31: DETEKSI TEPI (MENJIPLAK GARIS) -->
    <section class="slide" data-title="Mengukur Background Complexity: Edge Detection" data-notes="Alokasi waktu: 1 menit. Jelaskan Canny Edge Detection secara sederhana: komputer mendeteksi garis batas (edge) objek di dalam foto untuk mengukur seberapa ramai latar belakangnya.">
      <div class="kicker">BAB 3 · EDGE DETECTION &amp; EDGE DENSITY</div>
      <h2>Mengukur Background Complexity: <span class="hl-red">Edge Detection</span></h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Bagaimana Edge Detection Bekerja?</div>
          <div class="card-body">
            <ul>
              <li>Algoritma mencari titik di mana <strong>perubahan warna atau <em>brightness</em> terjadi secara tajam</strong> (misalnya batas antara objek dan latar).</li>
              <li>Titik-titik perubahan tajam itu digambar sebagai <em>edge</em> putih di atas latar hitam (contoh populer: metode <em>Canny</em>).</li>
            </ul>
          </div>
          <div class="callout">Semakin banyak <em>edge</em> yang terdeteksi, semakin kompleks isi latar belakang foto tersebut.</div>
        </div>
        <div class="card surface">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title">Menghitung Edge Density</div>
          <div class="card-body">
            <ul>
              <li>Kita cukup menghitung: <strong>berapa persen pixel yang menjadi <em>edge</em></strong> dibanding seluruh foto.</li>
              <li><strong>Latar Polos:</strong> Hanya ada garis luar objek utama → persentase garis sangat kecil.</li>
              <li><strong>Latar Ramai:</strong> Penuh garis dari benda-benda di belakangnya → persentase garis melonjak tinggi!</li>
            </ul>
          </div>
          <svg viewBox="0 0 360 95" style="width:100%; max-height:92px; margin-top:auto;">
            <rect x="8" y="8" width="155" height="78" rx="10" fill="#202124"/>
            <polygon points="85,20 112,68 58,68" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
            <text x="85" y="81" text-anchor="middle" font-size="10.5" fill="#A8DAB5">Polos: Sedikit Garis</text>
            <rect x="195" y="8" width="155" height="78" rx="10" fill="#202124"/>
            <polygon points="272,20 299,68 245,68" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
            <circle cx="222" cy="30" r="10" fill="none" stroke="#EA4335" stroke-width="1.8"/>
            <rect x="308" y="22" width="24" height="24" fill="none" stroke="#FBBC04" stroke-width="1.8"/>
            <line x1="205" y1="62" x2="242" y2="48" stroke="#4285F4" stroke-width="1.8"/>
            <line x1="305" y1="65" x2="340" y2="52" stroke="#34A853" stroke-width="1.8"/>
            <text x="272" y="81" text-anchor="middle" font-size="10.5" fill="#F6AEA9">Ramai: Penuh Coretan Garis</text>
          </svg>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>31 / 54</span></div>
    </section>

    <!-- 32: HASIL NYATA CANNY POLOS VS RAMAI -->
    <section class="slide" data-title="Bukti Nyata: Latar Polos vs Latar Ramai" data-notes="Alokasi waktu: 1.5 menit. Tunjukkan hasil nyata pada 119 foto valid: latar ramai punya <em>edge density</em> sekitar 7 kali lipat lebih tinggi!">
      <div class="kicker">BAB 3 · HASIL DATA SAMPEL</div>
      <h2>Bukti Nyata: <span class="hl-blue">Latar Polos</span> vs <span class="hl-red">Latar Ramai</span></h2>
      <div class="img-box" style="flex:1; padding:10px;">
        <img src="assets/P01/08_canny_edge_density.png" alt="Deteksi tepi polos vs ramai" />
      </div>
      <div class="callout red" style="margin-top:10px;">
        <strong>Contoh data sampel (119 valid images):</strong> Rata-rata <em>edge density</em> latar polos hanya <code>{polos['mean_edge_density']:.4f}</code>, sedangkan latar ramai melonjak menjadi <code>{ramai['mean_edge_density']:.4f}</code> (<strong>~7× lebih padat!</strong>).
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>32 / 54</span></div>
    </section>

    <!-- 33: QA REVEAL #4 -->
    <section class="slide" data-title="Tanya-Jawab #4: Bahaya Latar Belakang Ramai" data-notes="Alokasi waktu: 1.5 menit. Ajak peserta menebak kenapa foto berlatar ramai sering mengecoh AI pemula.">
      <div class="kicker">TANYA &amp; JAWAB INTERAKTIF · #4</div>
      <h2>Coba Pikirkan: <span class="hl-red">Kenapa Latar Ramai</span> Mengecoh AI?</h2>
      <div class="split-60-40">
        <div class="qa-box" style="margin:0; justify-content:center;">
          <div class="qa-question">
            Misalkan semua foto <strong>Objek A</strong> diambil di atas meja kayu berantakan, sedangkan semua foto <strong>Objek B</strong> diambil di depan tembok putih polos. Apa risiko terbesar saat AI belajar dari foto ini?
          </div>
          <div class="qa-choices">
            <div class="qa-choice"><strong>A.</strong> AI belajar mengenali bentuk Objek A dan B dengan sempurna.</div>
            <div class="qa-choice"><strong>B.</strong> AI "curang": ia menghafal meja kayu = A, tembok putih = B!</div>
            <div class="qa-choice"><strong>C.</strong> Foto menjadi tidak bisa disimpan.</div>
          </div>
          <button class="btn-ui" onclick="toggleQA('qa4', this)">Klik untuk Lihat Jawaban &amp; Penjelasan</button>
          <div id="qa4" class="qa-answer">
            <strong>Jawaban: B — AI bisa "curang" menghafal latar belakangnya!</strong><br />
            Komputer selalu mencari jalan pintas termudah. Jika objek A ditaruh di depan tembok putih saat diuji nanti, AI bisa salah menebaknya sebagai Objek B! Itulah mengapa memisahkan evaluasi foto <strong>polos vs ramai</strong> sangat penting untuk menguji kepintaran AI yang sesungguhnya.
          </div>
        </div>
        <div class="card surface" style="align-items:center; justify-content:center; padding:16px;">
          <svg id="qa4-vis" viewBox="0 0 320 265" style="width:100%; height:100%; max-height:360px;">
            <rect x="12" y="14" width="138" height="106" rx="12" fill="#D7CCC8" stroke="#795548" stroke-width="2"/>
            <line x1="20" y1="36" x2="142" y2="36" stroke="#A1887F" stroke-width="2"/>
            <line x1="20" y1="70" x2="142" y2="70" stroke="#A1887F" stroke-width="2"/>
            <circle cx="81" cy="64" r="22" fill="#4285F4"/>
            <text x="81" y="69" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">A</text>
            <text x="81" y="108" text-anchor="middle" font-size="10.5" font-weight="700" fill="#4E342E">Latar Meja Kayu</text>

            <rect x="170" y="14" width="138" height="106" rx="12" fill="#FFFFFF" stroke="#BDC1C6" stroke-width="2"/>
            <rect x="217" y="42" width="44" height="44" rx="8" fill="#34A853"/>
            <text x="239" y="69" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">B</text>
            <text x="239" y="108" text-anchor="middle" font-size="10.5" font-weight="700" fill="#5F6368">Latar Tembok Putih</text>

            <rect x="46" y="138" width="228" height="36" rx="18" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
            <text x="160" y="161" text-anchor="middle" font-size="11.5" font-weight="700" fill="#202124">Saat Ujian: Objek A di Tembok Putih</text>

            <g class="vis-q">
              <rect x="76" y="188" width="168" height="66" rx="12" fill="#FFFFFF" stroke="#4285F4" stroke-width="2.5" stroke-dasharray="6 4"/>
              <circle cx="132" cy="221" r="18" fill="#4285F4"/>
              <text x="132" y="226" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">A</text>
              <text x="196" y="227" text-anchor="middle" font-size="18" font-weight="700" fill="#1A73E8">→ ?</text>
            </g>
            <g class="vis-a">
              <rect x="76" y="188" width="168" height="66" rx="12" fill="#FFFFFF" stroke="#EA4335" stroke-width="2.5"/>
              <circle cx="132" cy="221" r="18" fill="#4285F4"/>
              <text x="132" y="226" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">A</text>
              <text x="196" y="226" text-anchor="middle" font-size="16" font-weight="700" fill="#EA4335">→ B ?!</text>
            </g>
          </svg>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>33 / 54</span></div>
    </section>

    <!-- 34: DUA SKENARIO PENGUJIAN -->
    <section class="slide" data-title="Menguji Kejujuran AI: Skenario Polos vs Ramai" data-notes="Alokasi waktu: 1 menit. Jelaskan secara non-teknis mengapa kita mencatat kondisi latar (polos vs ramai) sejak awal.">
      <div class="kicker">BAB 3 · STRATEGI UJI</div>
      <h2>Mengapa Kita Memisahkan Catatan <span class="hl-blue">Polos</span> vs <span class="hl-red">Ramai</span>?</h2>
      <div class="grid-2">
        <div class="card tint-blue">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">UJI KONDISI BERSIH</span>
          <div class="card-title">Belajar dari Latar Polos → Diuji di Latar Ramai</div>
          <div class="card-body">Jika AI hanya berlatih di studio yang bersih, apakah ia masih sanggup mengenali objek yang sama di jalanan atau ruangan ramai? Di sinilah ketangguhannya diuji!</div>
          <svg viewBox="0 0 360 76" style="width:100%; max-height:74px; margin-top:auto;">
            <rect x="10" y="14" width="128" height="48" rx="10" fill="#FFFFFF" stroke="#4285F4" stroke-width="2"/>
            <text x="74" y="42" text-anchor="middle" font-size="11.5" font-weight="700" fill="#1A73E8">Train: Polos</text>
            <path d="M148 38 L208 38" stroke="#1A73E8" stroke-width="3"/><polygon points="206,32 218,38 206,44" fill="#1A73E8"/>
            <rect x="224" y="14" width="126" height="48" rx="10" fill="#FCE8E6" stroke="#EA4335" stroke-width="2"/>
            <text x="287" y="42" text-anchor="middle" font-size="11.5" font-weight="700" fill="#C5221F">Test: Ramai (?)</text>
          </svg>
        </div>
        <div class="card tint-green">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">UJI KONDISI CAMPURAN</span>
          <div class="card-title">Belajar dari Foto Campuran (Polos + Ramai)</div>
          <div class="card-body">Dengan memberi variasi latar belakang sejak awal, AI dipaksa fokus pada <strong>bentuk objeknya</strong>, bukan menghafal tembok atau mejanya.</div>
          <svg viewBox="0 0 360 76" style="width:100%; max-height:74px; margin-top:auto;">
            <rect x="10" y="14" width="140" height="48" rx="10" fill="#FFFFFF" stroke="#34A853" stroke-width="2"/>
            <text x="80" y="42" text-anchor="middle" font-size="11.5" font-weight="700" fill="#137333">Train: Polos + Ramai</text>
            <path d="M160 38 L210 38" stroke="#137333" stroke-width="3"/><polygon points="208,32 220,38 208,44" fill="#137333"/>
            <rect x="226" y="14" width="124" height="48" rx="10" fill="#34A853"/>
            <text x="288" y="42" text-anchor="middle" font-size="11.5" font-weight="700" fill="#FFFFFF">AI Lebih Tangguh!</text>
          </svg>
        </div>
      </div>
      <div class="callout" style="margin-top:12px;">Catat kondisi latar (<code>polos</code> / <code>ramai</code>) di daftar foto Anda sejak tahap pemeriksaan awal ini!</div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>34 / 54</span></div>
    </section>

    <!-- 35: PETUNJUK BUKAN VONIS -->
    <section class="slide" data-title="Angka Statistik Itu Petunjuk, Bukan Vonis" data-notes="Alokasi waktu: 1 menit. Ingatkan bahwa angka deteksi tepi hanyalah alat bantu cepat, mata manusia tetap perlu melihat sampel fotonya.">
      <div class="kicker">BAB 3 · CATATAN BIJAK</div>
      <h2>Angka Kerumitan Itu <span class="hl-yellow">Petunjuk</span>, Bukan Vonis</h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title">Contoh Pengecualian</div>
          <div class="card-body">
            <ul>
              <li>Objek yang memakai baju bermotif garis-garis atau kotak-kotak akan menghasilkan banyak <em>edge</em>, walaupun difoto di depan tembok polos!</li>
              <li>Sebaliknya, latar belakang yang buram (efek <em>bokeh</em> kamera HP) punya sedikit <em>edge</em> meski sebenarnya berada di tempat ramai.</li>
            </ul>
            <svg viewBox="0 0 340 100" style="width:100%; height:96px; margin-top:10px;">
              <rect x="4" y="4" width="156" height="92" rx="10" fill="#F8F9FA" stroke="#EA4335" stroke-width="1.5"/>
              <rect x="52" y="14" width="60" height="50" rx="8" fill="#FFFFFF" stroke="#202124" stroke-width="1.5"/>
              <line x1="56" y1="24" x2="108" y2="24" stroke="#202124" stroke-width="2"/>
              <line x1="56" y1="34" x2="108" y2="34" stroke="#202124" stroke-width="2"/>
              <line x1="56" y1="44" x2="108" y2="44" stroke="#202124" stroke-width="2"/>
              <line x1="56" y1="54" x2="108" y2="54" stroke="#202124" stroke-width="2"/>
              <text x="82" y="84" text-anchor="middle" font-size="10" font-weight="700" fill="#C5221F">Motif Garis → High Edge</text>

              <rect x="180" y="4" width="156" height="92" rx="10" fill="#F8F9FA" stroke="#4285F4" stroke-width="1.5"/>
              <circle cx="218" cy="36" r="14" fill="#AECBFA" opacity="0.5"/>
              <circle cx="294" cy="40" r="16" fill="#FDE293" opacity="0.5"/>
              <circle cx="258" cy="39" r="18" fill="#34A853"/>
              <text x="258" y="84" text-anchor="middle" font-size="10" font-weight="700" fill="#1A73E8">Latar Bokeh → Low Edge</text>
            </svg>
          </div>
        </div>
        <div class="card surface">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Kebiasaan Baik Pemeriksa Data</div>
          <div class="card-body">
            <ul>
              <li>Gunakan angka statistik untuk menyaring ribuan foto dengan cepat.</li>
              <li>Tetap luangkan waktu melihat langsung beberapa contoh foto dengan mata kepala sendiri untuk memastikan kondisi sebenarnya.</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>35 / 54</span></div>
    </section>

    <!-- 36: DIVIDER BAB 4 -->
    <section class="slide bg-yellow" data-title="Bab 4: Tiga Jebakan Tersembunyi Kamera HP" data-notes="Alokasi waktu: 0.5 menit. Sekarang kita bahas tiga masalah diam-diam yang paling sering menjebak pemula saat mengumpulkan foto dari HP.">
      <div class="divider-center">
        <span class="pill dark">BAB 4 · KUALITAS &amp; KEBERSIHAN DATA</span>
        <h1>Tiga Jebakan Tersembunyi pada Foto HP</h1>
        <p>Foto yang tampak baik-baik saja di galeri HP ternyata bisa terbaca terbalik, kembar menipu, atau membuat program macet mendadak.</p>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>36 / 54</span></div>
    </section>

    <!-- 37: JEBAKAN 1 - EXIF ORIENTATION -->
    <section class="slide" data-title="Jebakan #1: Foto Terlihat Tegak di HP, Tapi Miring di Komputer" data-notes="Alokasi waktu: 1.5 menit. Tunjukkan gambar nyata jebakan EXIF: HP hanya menempelkan catatan rotasi (EXIF) tanpa memutar piksel aslinya.">
      <div class="kicker">BAB 4 · JEBAKAN #1</div>
      <h2>Terlihat Tegak di HP, <span class="hl-red">Tapi Terputar di Program!</span></h2>
      <div class="split-60-40">
        <div class="img-box">
          <img src="assets/P01/09_exif_trap.png" alt="Jebakan EXIF Orientation" />
        </div>
        <div class="card">
          <div class="card-top-bar bar-red"></div>
          <span class="pill red">EXIF ORIENTATION</span>
          <div class="card-title">Mengapa Bisa Terbalik?</div>
          <div class="card-body">
            <ul>
              <li>Saat memotret sambil memiringkan HP, kamera sering menyimpan pixel dalam orientasi asli sensor, lalu menempelkan <strong>catatan kecil (EXIF)</strong>: <em>"Tolong putar 90° saat dibuka"</em>.</li>
              <li>Galeri HP membaca catatan itu, tapi program pembaca angka sering <strong>mengabaikannya</strong>!</li>
            </ul>
          </div>
          <div class="callout green"><strong>Solusi mudah:</strong> Jalankan perintah putar otomatis (<code>exif_transpose</code>) tepat saat foto pertama kali dibuka!</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>37 / 54</span></div>
    </section>

    <!-- 38: JEBAKAN 2 - FOTO KEMBAR & BURST -->
    <section class="slide" data-title="Jebakan #2: Duplicate Images &amp; Burst Photos" data-notes="Alokasi waktu: 1.5 menit. Jelaskan bahaya foto duplikat dan foto jepretan beruntun (burst) yang hampir sama persis.">
      <div class="kicker">BAB 4 · JEBAKAN #2</div>
      <h2><span class="hl-blue">Duplicate Images</span> &amp; <span class="hl-yellow">Burst Photos</span></h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">1. Duplicate Images (Kembar Identik)</div>
          <div class="card-body">
            <ul>
              <li>Sering terjadi tanpa sengaja saat kita menyalin foto dua kali dengan nama file berbeda (misal <code>foto1.jpg</code> dan <code>salinan_foto1.jpg</code>).</li>
              <li>Komputer mendeteksinya otomatis dengan membuat <strong><em>file hash</em> (SHA-256)</strong>.</li>
            </ul>
            <svg viewBox="0 0 320 66" style="width:100%; height:64px; margin-top:8px;">
              <rect x="4" y="6" width="96" height="54" rx="8" fill="#E8F0FE" stroke="#4285F4"/>
              <text x="52" y="28" text-anchor="middle" font-size="10" font-weight="700" fill="#1A73E8">foto1.jpg</text>
              <text x="52" y="46" text-anchor="middle" font-size="9" fill="#5F6368">Hash: 9f8a...</text>
              <rect x="116" y="6" width="104" height="54" rx="8" fill="#FCE8E6" stroke="#EA4335"/>
              <text x="168" y="28" text-anchor="middle" font-size="10" font-weight="700" fill="#C5221F">salinan_foto1.jpg</text>
              <text x="168" y="46" text-anchor="middle" font-size="9" fill="#C5221F">Hash: 9f8a... (Sama!)</text>
              <rect x="232" y="16" width="82" height="34" rx="17" fill="#EA4335"/>
              <text x="273" y="37" text-anchor="middle" font-size="10.5" font-weight="700" fill="#FFFFFF">Buang 1!</text>
            </svg>
          </div>
          <div class="callout">Jika dua file punya <em>hash</em> yang persis sama, sisakan satu dan buang duplikatnya!</div>
        </div>
        <div class="card">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title">2. Burst Photos dalam 1 Sesi</div>
          <div class="card-body">
            <ul>
              <li>Saat memotret beruntun (<em>burst mode</em>), sudut dan cahayanya 99% sama.</li>
              <li>Jika foto ke-1 masuk <strong>Train Set</strong> dan foto ke-2 masuk <strong>Test Set</strong>, skor evaluasi AI akan mengalami <strong>inflated accuracy</strong>!</li>
            </ul>
            <svg viewBox="0 0 320 66" style="width:100%; height:64px; margin-top:8px;">
              <rect x="4" y="6" width="212" height="54" rx="8" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.5"/>
              <rect x="14" y="14" width="56" height="38" rx="6" fill="#FFFFFF" stroke="#F9AB00"/>
              <text x="42" y="37" text-anchor="middle" font-size="9.5" font-weight="700" fill="#202124">00:01.1</text>
              <rect x="82" y="14" width="56" height="38" rx="6" fill="#FFFFFF" stroke="#F9AB00"/>
              <text x="110" y="37" text-anchor="middle" font-size="9.5" font-weight="700" fill="#202124">00:01.3</text>
              <rect x="150" y="14" width="56" height="38" rx="6" fill="#FFFFFF" stroke="#F9AB00"/>
              <text x="178" y="37" text-anchor="middle" font-size="9.5" font-weight="700" fill="#202124">00:01.5</text>
              <rect x="226" y="16" width="88" height="34" rx="17" fill="#202124"/>
              <text x="270" y="37" text-anchor="middle" font-size="10" font-weight="700" fill="#FBBC04">1 id_sesi</text>
            </svg>
          </div>
          <div class="callout yellow">Beri kode <code>id_sesi</code> agar foto dari sesi yang sama tidak terpecah antara <em>train</em> dan <em>test</em>.</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>38 / 54</span></div>
    </section>

    <!-- 39: JEBAKAN 3 - FILE RUSAK -->
    <section class="slide" data-title="Jebakan #3: Corrupted Files" data-notes="Alokasi waktu: 1 menit. Satu file rusak bisa membuat proses latihan AI yang sudah berjalan berjam-jam tiba-tiba crash.">
      <div class="kicker">BAB 4 · JEBAKAN #3</div>
      <h2>Satu <span class="hl-red">Corrupted File</span> Bisa Menghentikan Semua Proses</h2>
      <div class="grid-2">
        <div class="card tint-red">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title">Dari Mana Asalnya Corrupted File?</div>
          <div class="card-body">
            <ul>
              <li>Proses unduh atau kirim file yang terputus di tengah jalan.</li>
              <li>File kosong (0 KB) atau dokumen lain yang keliru diberi akhiran <code>.jpg</code>.</li>
              <li>Efeknya: saat AI melatih ratusan foto, program tiba-tiba berhenti error tepat ketika menyentuh <em>corrupted file</em> tersebut!</li>
            </ul>
          </div>
          <svg viewBox="0 0 360 76" style="width:100%; max-height:74px; margin-top:auto;">
            <rect x="12" y="14" width="60" height="48" rx="8" fill="#FFFFFF" stroke="#EA4335" stroke-width="2"/>
            <path d="M28 28 L56 48 M56 28 L28 48" stroke="#EA4335" stroke-width="3.5" stroke-linecap="round"/>
            <path d="M84 38 L135 38" stroke="#EA4335" stroke-width="3" stroke-dasharray="5,4"/>
            <rect x="145" y="17" width="195" height="42" rx="10" fill="#EA4335"/>
            <text x="242" y="43" text-anchor="middle" font-family="Poppins, sans-serif" font-size="12.5" font-weight="700" fill="#FFFFFF">Proses Latih AI Macet!</text>
          </svg>
        </div>
        <div class="card">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Pencegahan Sangat Mudah</div>
          <div class="card-body">
            <ul>
              <li>Sebelum mulai, perintahkan komputer untuk <strong>menguji buka semua file satu per satu</strong>.</li>
              <li>Catat nama file yang gagal dibuka, lalu sisihkan dari perhitungan statistik maupun daftar latih AI.</li>
            </ul>
          </div>
          <div class="callout green">Di data sampel kita, ada 1 file sengaja dibuat rusak agar kita terbiasa menyaringnya sejak awal.</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>39 / 54</span></div>
    </section>

    <!-- 40: HASIL AUDIT 120 FILE SAMPEL -->
    <section class="slide" data-title="Hasil EDA: 120 File Sampel" data-notes="Alokasi waktu: 1.5 menit. Tunjukkan angka nyata hasil EDA pada 120 file di data sampel kita.">
      <div class="kicker">BAB 4 · HASIL EDA NYATA</div>
      <h2>Hasil EDA <span class="hl-blue">120 File Sampel</span> Kita</h2>
      <p class="subtitle">Contoh data sampel: hasil pemeriksaan otomatis sebelum masuk tahap berikutnya.</p>
      <div class="grid-4" style="flex:0 0 auto;">
        <div class="card tint-blue"><div class="big-num hl-blue">{stats['total_metadata_rows']}</div><div class="card-title">Total File</div><div class="card-body">5 jenis × 2 latar × 12 foto.</div></div>
        <div class="card tint-green"><div class="big-num hl-green">{stats['valid_images']}</div><div class="card-title">Valid Images</div><div class="card-body">Siap dihitung &amp; dianalisis.</div></div>
        <div class="card tint-red"><div class="big-num hl-red">{stats['corrupted_count']}</div><div class="card-title">Corrupted File</div><div class="card-body">Disisihkan otomatis.</div></div>
        <div class="card tint-yellow"><div class="big-num hl-yellow">{stats['duplicate_file_count'] + stats['exif_orientation_6_count']}</div><div class="card-title">Perlu Perhatian</div><div class="card-body">{stats['duplicate_file_count']} duplicate + {stats['exif_orientation_6_count']} EXIF orientation=6.</div></div>
      </div>
      <div class="card surface" style="margin-top:14px; flex:1; justify-content:center;">
        <div class="card-title">Daftar Temuan Khusus pada Sampel:</div>
        <div class="card-body">
          <ul>
            <li><strong>Corrupted file:</strong> <code>segitiga_ramai_12.jpg</code> — gagal uji buka, langsung dikecualikan agar tidak merusak hitungan rata-rata.</li>
            <li><strong>Duplicate images:</strong> <code>lingkaran_polos_01.jpg</code> dan <code>lingkaran_polos_02.jpg</code> — memiliki <em>file hash</em> SHA-256 identik.</li>
            <li><strong>Foto EXIF orientation=6:</strong> <code>persegi_polos_01.jpg</code> dan <code>bintang_ramai_01.jpg</code> — otomatis diputar tegak saat dibuka.</li>
          </ul>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>40 / 54</span></div>
    </section>

    <!-- 41: QA REVEAL #5 -->
    <section class="slide" data-title="Tanya-Jawab #5: Bahaya Data Leakage" data-notes="Alokasi waktu: 1.5 menit. Pertanyaan terakhir sebelum masuk ke praktik: apa bahayanya jika foto kembar bocor ke bahan ujian AI?">
      <div class="kicker">TANYA &amp; JAWAB INTERAKTIF · #5</div>
      <h2>Coba Pikirkan: Bahaya <span class="hl-red">Data Leakage</span></h2>
      <div class="split-60-40">
        <div class="qa-box" style="margin:0; justify-content:center;">
          <div class="qa-question">
            Kita punya 2 <em>duplicate images</em>. Satu ditaruh di <strong>Train Set</strong>, dan satu lagi ditaruh di <strong>Test Set</strong>. Mengapa hal ini sangat berbahaya?
          </div>
          <div class="qa-choices">
            <div class="qa-choice"><strong>A.</strong> Komputer akan hang karena gambarnya sama.</div>
            <div class="qa-choice"><strong>B.</strong> Nilai ujian AI terlihat 100% pintar, padahal ia cuma menghafal!</div>
            <div class="qa-choice"><strong>C.</strong> Tidak berpengaruh apa-apa pada hasil AI.</div>
          </div>
          <button class="btn-ui" onclick="toggleQA('qa5', this)">Klik untuk Lihat Jawaban &amp; Penjelasan</button>
          <div id="qa5" class="qa-answer">
            <strong>Jawaban: B — Nilai ujian AI terlihat pintar palsu karena bocor!</strong><br />
            Ibarat siswa yang sudah diberi kunci soal ujian yang persis sama sebelumnya. Saat diuji di dunia nyata dengan foto baru yang belum pernah ia lihat, performanya langsung anjlok. Dalam dunia AI, kebocoran ini disebut <strong>Data Leakage</strong>.
          </div>
        </div>
        <div class="card surface" style="align-items:center; justify-content:center; padding:16px;">
          <svg id="qa5-vis" viewBox="0 0 320 265" style="width:100%; height:100%; max-height:360px;">
            <rect x="12" y="18" width="130" height="140" rx="14" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.5"/>
            <text x="77" y="42" text-anchor="middle" font-size="13" font-weight="700" fill="#1A73E8">TRAIN SET</text>
            <rect x="37" y="56" width="80" height="80" rx="10" fill="#FFFFFF" stroke="#4285F4" stroke-width="2"/>
            <circle cx="77" cy="88" r="18" fill="#FBBC04"/>
            <text x="77" y="126" text-anchor="middle" font-size="10.5" font-weight="700" fill="#202124">Hash: a94f...</text>

            <rect x="178" y="18" width="130" height="140" rx="14" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.5"/>
            <text x="243" y="42" text-anchor="middle" font-size="13" font-weight="700" fill="#C5221F">TEST SET</text>
            <rect x="203" y="56" width="80" height="80" rx="10" fill="#FFFFFF" stroke="#EA4335" stroke-width="2"/>
            <circle cx="243" cy="88" r="18" fill="#FBBC04"/>
            <text x="243" y="126" text-anchor="middle" font-size="10.5" font-weight="700" fill="#202124">Hash: a94f...</text>

            <g class="vis-q">
              <circle cx="160" cy="91" r="16" fill="#202124"/>
              <text x="160" y="96" text-anchor="middle" font-size="15" font-weight="700" fill="#FBBC04">?</text>
              <rect x="24" y="182" width="272" height="62" rx="14" fill="#FFFFFF" stroke="#BDC1C6" stroke-width="2" stroke-dasharray="6 4"/>
              <text x="160" y="218" text-anchor="middle" font-size="12.5" font-weight="700" fill="#5F6368">Apa dampaknya saat model diuji?</text>
            </g>
            <g class="vis-a">
              <path d="M 122 96 H 198" stroke="#EA4335" stroke-width="3" stroke-dasharray="6 4"/>
              <rect x="124" y="80" width="72" height="22" rx="11" fill="#EA4335"/>
              <text x="160" y="95" text-anchor="middle" font-size="10.5" font-weight="700" fill="#FFFFFF">LEAK!</text>
              <rect x="24" y="182" width="272" height="62" rx="14" fill="#202124"/>
              <text x="160" y="207" text-anchor="middle" font-size="13" font-weight="700" fill="#FBBC04">Akurasi Uji: 100% (Palsu)</text>
              <text x="160" y="229" text-anchor="middle" font-size="12" font-weight="600" fill="#E8EAED">Foto Baru Dunia Nyata: Gagal!</text>
            </g>
          </svg>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>41 / 54</span></div>
    </section>

    <!-- 42: ATURAN EMAS KEBERSIHAN DATA -->
    <section class="slide" data-title="4 Aturan Emas Sebelum Melatih AI" data-notes="Alokasi waktu: 1 menit. Rangkuman 4 aturan praktis agar eksperimen AI jujur dan bersih.">
      <div class="kicker">BAB 4 · ATURAN EMAS</div>
      <h2>4 Aturan Emas <span class="hl-green">Menjaga Kejujuran Data</span></h2>
      <div class="grid-2">
        <div class="card"><div class="card-top-bar bar-blue"></div><div class="card-title">1. Hapus Duplicate Sebelum Split</div><div class="card-body">Pastikan tidak ada <em>duplicate images</em> sebelum membagi dataset menjadi <strong>Train Set</strong> dan <strong>Test Set</strong>.</div></div>
        <div class="card"><div class="card-top-bar bar-red"></div><div class="card-title">2. Jaga Group Sesi Foto</div><div class="card-body"><em>Burst photos</em> dari momen yang sama harus masuk ke satu kelompok yang sama (jangan terpecah antara <em>train</em> dan <em>test</em>).</div></div>
        <div class="card"><div class="card-top-bar bar-yellow"></div><div class="card-title">3. Test Set Disimpan Rapat</div><div class="card-body">Jangan mengintip atau menyetel aturan berdasarkan <em>Test Set</em>; biarkan ia menjadi ujian terakhir yang murni.</div></div>
        <div class="card"><div class="card-top-bar bar-green"></div><div class="card-title">4. Catat Semua Pembersihan</div><div class="card-body">Simpan daftar <em>corrupted files</em> dan <em>duplicates</em> yang dibuang agar audit data tetap transparan.</div></div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>42 / 54</span></div>
    </section>

    <!-- 43: DIVIDER BAB 5 -->
    <section class="slide bg-blue" data-title="Bab 5: Praktik, Diskusi &amp; Kuis Interaktif" data-notes="Alokasi waktu: 5 menit. Sekarang kita masuk ke sesi praktik terpandu, diskusi kasus, kamus santai, dan kuis interaktif.">
      <div class="divider-center">
        <span class="pill dark">BAB 5 · PRAKTIK &amp; UJI PEMAHAMAN</span>
        <h1>Saatnya Praktik, Diskusi &amp; Uji Pemahaman</h1>
        <p>Melihat alur 6 langkah pemeriksaan foto, mendiskusikan tantangan polos vs ramai, dan menguji pemahaman lewat kuis.</p>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>43 / 54</span></div>
    </section>

    <!-- 44: 6 LANGKAH PRAKTIK (50 MENIT) -->
    <section class="slide" data-title="6 Langkah Praktik Terpandu (50 Menit)" data-notes="Alokasi waktu: 42.5 menit (selama sesi praktik). Jelaskan urutan 6 langkah dari awal hingga menyimpan laporan kesehatan data.">
      <div class="kicker">HANDS-ON · 50 MENIT</div>
      <h2>6 Langkah <span class="hl-blue">Memeriksa Koleksi Foto</span></h2>
      <div class="step-list">
        <div class="step-item"><div class="step-num">01</div><div><div class="step-title">Siapkan Folder &amp; Uji Buka 1 Foto</div><div class="step-desc">Pastikan foto terbaca sebagai warna RGB, ukurannya terlihat, dan posisi tegaknya sudah sesuai catatan EXIF.</div></div></div>
        <div class="step-item"><div class="step-num red">02</div><div><div class="step-title">Saring Corrupted File &amp; Hitung Keseimbangan</div><div class="step-desc">Periksa semua file di folder, sisihkan file yang gagal dibuka, dan cek apakah jumlah foto tiap jenis seimbang.</div></div></div>
        <div class="step-item"><div class="step-num yellow">03</div><div><div class="step-title">Deteksi Duplicate Images</div><div class="step-desc">Hitung <em>file hash</em> (SHA-256) untuk tiap <em>valid image</em> dan tandai jika ada <em>duplicates</em>.</div></div></div>
        <div class="step-item"><div class="step-num green">04</div><div><div class="step-title">Ukur Brightness, Contrast &amp; Edge Density</div><div class="step-desc">Hitung rata-rata <em>brightness</em>, <em>contrast</em>, dan <em>edge density</em> pada setiap <em>valid image</em>.</div></div></div>
        <div class="step-item"><div class="step-num">05</div><div><div class="step-title">Bandingkan Kondisi Polos vs Ramai</div><div class="step-desc">Buat grafik perbandingan agar terlihat jelas perbedaan <em>brightness</em> dan <em>background complexity</em>-nya.</div></div></div>
        <div class="step-item"><div class="step-num red">06</div><div><div class="step-title">Simpan Ringkasan Audit Data</div><div class="step-desc">Simpan tabel hasil pemeriksaan dan gambar grafik ke folder hasil agar bisa dijadikan pegangan langkah selanjutnya.</div></div></div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>44 / 54</span></div>
    </section>

    <!-- 45: INTIP DI BALIK LAYAR - EXIF & RUSAK -->
    <section class="slide" data-title="Di Balik Layar: Cek Rusak &amp; Putar EXIF" data-notes="Alokasi waktu: 1 menit. Tunjukkan cuplikan kode ringkas dengan penjelasan bahasa awam: komputer hanya memanggil dua fungsi bantu.">
      <div class="kicker">PRAKTIK · DI BALIK LAYAR</div>
      <h2>Cara Komputer <span class="hl-blue">Mengecek Corrupted File &amp; EXIF</span></h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Logika Sederhananya</div>
          <div class="card-body">
            <ul>
              <li>Kita tidak perlu menulis rumus rumit dari nol.</li>
              <li>Pustaka gambar Python (<code>Pillow</code>) sudah punya tombol khusus untuk memeriksa apakah file utuh dan untuk memutar foto sesuai catatan EXIF.</li>
              <li>Jika file gagal diperiksa, komputer langsung menandainya sebagai <em>rusak</em> lalu lanjut ke file berikutnya tanpa macet!</li>
            </ul>
          </div>
        </div>
        <div class="card surface">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Cuplikan Perintahnya</div>
          <pre class="code"><code>from PIL import Image, ImageOps

# 1. Uji apakah file foto sehat
with Image.open(lokasi_foto) as img:
    img.verify()

# 2. Buka lagi, putar tegak (EXIF), ubah ke RGB
with Image.open(lokasi_foto) as img:
    img = ImageOps.exif_transpose(img).convert("RGB")</code></pre>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>45 / 54</span></div>
    </section>

    <!-- 46: INTIP DI BALIK LAYAR - SIDIK JARI FOTO -->
    <section class="slide" data-title="Di Balik Layar: Mendeteksi Duplicate Images" data-notes="Alokasi waktu: 1 menit. Jelaskan konsep sidik jari file (hash) dengan bahasa sehari-hari.">
      <div class="kicker">PRAKTIK · DI BALIK LAYAR</div>
      <h2>Cara Komputer <span class="hl-yellow">Mendeteksi Duplicate Images</span></h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title">File Hash (SHA-256)</div>
          <div class="card-body">
            <ul>
              <li>Bagaimana komputer tahu dua file berbeda nama ternyata isinya kembar identik?</li>
              <li>Komputer meringkas isi file menjadi kode unik pendek (disebut <strong>Hash</strong>), sebagai identitas unik isi file.</li>
              <li>Jika kodenya sama persis, berarti fotonya 100% kembar walaupun nama file-nya diganti!</li>
            </ul>
          </div>
        </div>
        <div class="card surface">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Cuplikan Perintahnya</div>
          <pre class="code"><code>import hashlib

def get_file_hash(lokasi_foto):
    isi = open(lokasi_foto, "rb").read()
    return hashlib.sha256(isi).hexdigest()

# Dua duplicate images pasti menghasilkan hash yang sama!</code></pre>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>46 / 54</span></div>
    </section>

    <!-- 47: MINI-CHALLENGE -->
    <section class="slide" data-title="Mini-Challenge: Diskusi Detektif Data (15 Menit)" data-notes="Alokasi waktu: 10 menit. Ajak peserta berdiskusi santai menjawab 3 pertanyaan studi kasus berdasarkan angka nyata data sampel.">
      <div class="kicker">MINI-CHALLENGE · 15 MENIT</div>
      <h2>Diskusi Kasus: <span class="hl-red">Polos</span> vs <span class="hl-blue">Ramai</span></h2>
      <div class="grid-2">
        <div class="card surface">
          <div class="card-top-bar bar-red"></div>
          <span class="pill red">FAKTA DATA SAMPEL (119 FOTO)</span>
          <div class="card-title">Ringkasan Statistik Sampel</div>
          <div class="card-body">
            <ul>
              <li><strong>Foto Polos:</strong> Brightness <code>{polos['mean_brightness']:.2f}</code>, edge density <code>{polos['mean_edge_density']:.4f}</code>.</li>
              <li><strong>Foto Ramai:</strong> Brightness <code>{ramai['mean_brightness']:.2f}</code>, edge density <code>{ramai['mean_edge_density']:.4f}</code> (~7× lebih padat!).</li>
            </ul>
          </div>
          <div class="callout yellow">Angka sudah di tangan. Sekarang saatnya berpendapat!</div>
        </div>
        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">3 Pertanyaan Diskusi Bersama</div>
          <div class="card-body">
            <ul>
              <li><strong>1.</strong> Menurutmu, kondisi mana yang akan lebih sulit ditebak oleh AI nantinya: <strong>Polos</strong> atau <strong>Ramai</strong>? Mengapa?</li>
              <li><strong>2.</strong> Jika AI hanya kita latih dengan foto <strong>Polos</strong>, kira-kira apa yang terjadi saat ia melihat foto <strong>Ramai</strong>?</li>
              <li><strong>3.</strong> Apa saranmu agar AI bisa pintar di kedua kondisi sekaligus?</li>
            </ul>
          </div>
          <button class="btn-ui outline" onclick="toggleQA('mc-hint', this)" style="margin-top:8px;">Klik untuk Lihat Poin Petunjuk Diskusi</button>
          <div id="mc-hint" class="qa-answer" style="padding:12px 14px; font-size:13.5px;">
            <strong>Petunjuk:</strong> Latar <strong>ramai</strong> lebih menantang (~7× lebih banyak <em>edge</em>). Jika AI hanya dilatih foto <strong>polos</strong>, ia mudah terkecoh oleh latar belakang baru. Solusinya: campur foto polos + ramai di <em>Train Set</em>!
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>47 / 54</span></div>
    </section>

    <!-- 48: GLOSARIUM SANTAI 1 -->
    <section class="slide" data-title="Kamus Istilah Santai (Bagian 1)" data-notes="Alokasi waktu: 1 menit. Rangkuman 5 istilah dasar yang sering muncul agar peserta tetap akrab saat mendengarnya lagi.">
      <div class="kicker">GLOSARIUM · 1/2</div>
      <h2>5 Istilah Dasar yang <span class="hl-blue">Sudah Kita Pahami</span></h2>
      <table class="io-table" style="margin-top:8px;">
        <thead><tr><th style="width:26%;">Istilah</th><th>Penjelasan Bahasa Sehari-hari</th></tr></thead>
        <tbody>
          <tr><td><strong>Pixel</strong></td><td>Elemen terkecil penyusun gambar digital; setiap <em>pixel</em> hanya berisi satu warna polos.</td></tr>
          <tr><td><strong>RGB Channels</strong></td><td>Tiga channel warna dasar (Red, Green, Blue) yang dicampur untuk membentuk jutaan warna di layar.</td></tr>
          <tr><td><strong>Grayscale</strong></td><td>Citra 1 channel yang hanya mengukur 1 <em>channel</em> (mengukur gelap-terang saja).</td></tr>
          <tr><td><strong>Resolution</strong></td><td>Jumlah total <em>pixel</em> lebar × tinggi yang membentuk sebuah foto (misal <code>224 × 224</code>).</td></tr>
          <tr><td><strong>Aspect Ratio</strong></td><td>Perbandingan lebar dan tinggi foto agar bentuk objeknya tetap proporsional dan tidak mengalami distorsi (<em>stretched/squashed</em>).</td></tr>
        </tbody>
      </table>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>48 / 54</span></div>
    </section>

    <!-- 49: GLOSARIUM SANTAI 2 -->
    <section class="slide" data-title="Kamus Istilah Santai (Bagian 2)" data-notes="Alokasi waktu: 1 menit. Rangkuman 5 istilah terkait Image Processing dan pemeriksaan kesehatan foto.">
      <div class="kicker">GLOSARIUM · 2/2</div>
      <h2>5 Istilah <span class="hl-green">Image Processing &amp; EDA</span></h2>
      <table class="io-table" style="margin-top:8px;">
        <thead><tr><th style="width:26%;">Istilah</th><th>Penjelasan Bahasa Sehari-hari</th></tr></thead>
        <tbody>
          <tr><td><strong>Normalization</strong></td><td>Menyetarakan skala nilai <em>pixel</em> dari <code>0–255</code> menjadi angka kecil (<code>0–1</code> atau <code>−1–1</code>) agar AI lebih mudah menghitung.</td></tr>
          <tr><td><strong>EDA</strong></td><td><em>Exploratory Data Analysis</em> — proses memeriksa kualitas, distribusi, dan kebersihan dataset foto sebelum <em>training</em> model AI.</td></tr>
          <tr><td><strong>Histogram</strong></td><td>Grafik sebaran intensitas <em>pixel</em> untuk melihat apakah foto terlalu gelap, pas, atau terlalu silau.</td></tr>
          <tr><td><strong>Edge Density</strong></td><td>Rasio jumlah pixel <em>edge</em> terhadap total pixel; makin tinggi nilainya, makin ramai isi foto tersebut.</td></tr>
          <tr><td><strong>EXIF &amp; Hash</strong></td><td><strong>EXIF:</strong> metadata orientasi rotasi dari kamera. <strong>Hash:</strong> kode unik (SHA-256) dari isi file untuk mendeteksi <em>duplicate</em>.</td></tr>
        </tbody>
      </table>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>49 / 54</span></div>
    </section>

    <!-- 50: QUIZ 1 & 2 -->
    <section class="slide" data-title="Kuis Interaktif — Soal 1 &amp; 2" data-notes="Alokasi waktu: 1.5 menit. Minta peserta menjawab soal 1 dan 2 dulu, lalu klik tombol untuk melihat jawabannya.">
      <div class="kicker">KUIS INTERAKTIF · BAGIAN 1/3</div>
      <h2>Uji Pemahaman: <span class="hl-blue">Soal 1 &amp; 2</span></h2>
      <div class="grid-2">
        <div class="quiz-item">
          <span class="pill blue">SOAL 1 · CARA KOMPUTER MELIHAT</span>
          <div class="card-title">Apa yang sebenarnya dilihat komputer saat membaca sebuah foto?</div>
          <div class="card-body">A. Bentuk benda secara langsung seperti mata manusia.<br />B. Matriks pixel berisi nilai intensitas 0–255.<br />C. Rekaman suara kamera.</div>
          <button class="btn-ui" onclick="toggleAns('q1', this)">Lihat Jawaban</button>
          <div id="q1" class="quiz-ans"><strong>Jawaban: B.</strong> Komputer tidak punya mata; ia hanya membaca deretan nilai <em>brightness</em> (0–255) di setiap pixel.</div>
        </div>
        <div class="quiz-item">
          <span class="pill green">SOAL 2 · WARNA RGB</span>
          <div class="card-title">Jika nilai RGB = (255, 255, 255), warna apa yang tampil di layar?</div>
          <div class="card-body">A. Hitam pekat<br />B. Grayscale gelap<br />C. Putih terang</div>
          <button class="btn-ui" onclick="toggleAns('q2', this)">Lihat Jawaban</button>
          <div id="q2" class="quiz-ans"><strong>Jawaban: C.</strong> Ketika ketiga channel RGB berada di nilai maksimal (255) bersama-sama, hasilnya adalah cahaya putih terang.</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>50 / 54</span></div>
    </section>

    <!-- 51: QUIZ 3 & 4 -->
    <section class="slide" data-title="Kuis Interaktif — Soal 3 &amp; 4" data-notes="Alokasi waktu: 1.5 menit. Lanjutkan dengan soal 3 dan 4 tentang Image Processing dan EDA.">
      <div class="kicker">KUIS INTERAKTIF · BAGIAN 2/3</div>
      <h2>Uji Pemahaman: <span class="hl-green">Soal 3 &amp; 4</span></h2>
      <div class="grid-2">
        <div class="quiz-item">
          <span class="pill yellow">SOAL 3 · IMAGE PROCESSING</span>
          <div class="card-title">Mengapa kita perlu mengecilkan foto secara proporsional &amp; menyamakan skalanya ke 0–1?</div>
          <div class="card-body">A. Agar aspect ratio tidak terdistorsi dan training AI lebih stabil.<br />B. Agar foto berubah menjadi grayscale.<br />C. Agar ukuran file menjadi lebih berat.</div>
          <button class="btn-ui" onclick="toggleAns('q3', this)">Lihat Jawaban</button>
          <div id="q3" class="quiz-ans"><strong>Jawaban: A.</strong> Menjaga proporsi mencegah distorsi bentuk, dan normalization ke 0–1 membantu AI belajar dengan tenang dan stabil.</div>
        </div>
        <div class="quiz-item">
          <span class="pill red">SOAL 4 · JEBAKAN KAMERA HP</span>
          <div class="card-title">Mengapa foto tegak di HP kadang tampak miring / tertidur (<em>rotated</em>) saat dibaca oleh program komputer?</div>
          <div class="card-body">A. Karena ukuran fotonya terlalu kecil.<br />B. Karena komputer mengabaikan metadata EXIF orientation dari kamera HP.<br />C. Karena fotonya berlatar belakang polos.</div>
          <button class="btn-ui" onclick="toggleAns('q4', this)">Lihat Jawaban</button>
          <div id="q4" class="quiz-ans"><strong>Jawaban: B.</strong> Kamera HP sering hanya menulis metadata EXIF tanpa memutar matriks pixel aslinya, sehingga perlu diputar otomatis saat dibuka.</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>51 / 54</span></div>
    </section>

    <!-- 52: QUIZ 5 -->
    <section class="slide" data-title="Kuis Interaktif — Soal 5" data-notes="Alokasi waktu: 1 menit. Soal terakhir untuk menguji pemahaman tentang kebersihan data dan kebocoran data.">
      <div class="kicker">KUIS INTERAKTIF · BAGIAN 3/3</div>
      <h2>Uji Pemahaman: <span class="hl-red">Soal 5 (Penentu!)</span></h2>
      <div class="split-60-40">
        <div class="qa-box" style="margin:0; justify-content:center;">
          <div class="quiz-item">
            <span class="pill red">SOAL 5 · KEJUJURAN DATA</span>
            <div class="card-title">Apa bahayanya jika foto <em>duplicate</em> dibiarkan masuk ke <em>Train Set</em> dan <em>Test Set</em> sekaligus?</div>
            <div class="card-body">A. AI akan menolak membuka gambar tersebut.<br />B. Nilai ujian AI mengalami <em>inflated accuracy</em> akibat <em>data leakage</em>.<br />C. Gambar akan otomatis terhapus oleh komputer.</div>
            <button class="btn-ui" onclick="toggleAns('q5', this)">Lihat Jawaban</button>
            <div id="q5" class="quiz-ans"><strong>Jawaban: B.</strong> Duplicate images menyebabkan <em>data leakage</em>: akurasi evaluasi tampak tinggi, padahal gagal saat bertemu foto baru di dunia nyata!</div>
          </div>
          <div class="callout green">Jika Anda bisa menjawab 4–5 soal dengan benar, Anda sudah menguasai seluruh fondasi materi hari ini!</div>
        </div>
        <div class="card surface" style="align-items:center; justify-content:center; padding:16px;">
          <svg id="q5-vis" viewBox="0 0 320 265" style="width:100%; height:100%; max-height:360px;">
            <g class="vis-q">
              <rect x="20" y="20" width="280" height="222" rx="14" fill="#FFFFFF" stroke="#4285F4" stroke-width="2" stroke-dasharray="6 4"/>
              <circle cx="160" cy="112" r="34" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.5"/>
              <text x="160" y="123" text-anchor="middle" font-size="30" font-weight="700" fill="#1A73E8">?</text>
              <text x="160" y="176" text-anchor="middle" font-size="13" font-weight="700" fill="#202124">Duplicate di Train &amp; Test</text>
              <text x="160" y="198" text-anchor="middle" font-size="11.5" font-weight="600" fill="#5F6368">Klik "Lihat Jawaban" untuk melihat kesimpulan</text>
            </g>
            <g class="vis-a">
              <rect x="20" y="20" width="280" height="96" rx="14" fill="#E6F4EA" stroke="#34A853" stroke-width="2.5"/>
              <text x="160" y="48" text-anchor="middle" font-size="13" font-weight="700" fill="#137333">DATA BERSIH (TANPA LEAKAGE)</text>
              <rect x="42" y="64" width="102" height="36" rx="10" fill="#FFFFFF" stroke="#34A853" stroke-width="1.5"/>
              <text x="93" y="87" text-anchor="middle" font-size="12" font-weight="700" fill="#202124">Train: Unik</text>
              <rect x="176" y="64" width="102" height="36" rx="10" fill="#FFFFFF" stroke="#34A853" stroke-width="1.5"/>
              <text x="227" y="87" text-anchor="middle" font-size="12" font-weight="700" fill="#202124">Test: Baru</text>
              <text x="160" y="87" text-anchor="middle" font-size="14" font-weight="700" fill="#34A853">≠</text>

              <rect x="20" y="138" width="280" height="104" rx="14" fill="#202124"/>
              <circle cx="72" cy="190" r="28" fill="#FBBC04"/>
              <text x="72" y="196" text-anchor="middle" font-size="18" font-weight="700" fill="#202124">5/5</text>
              <text x="192" y="178" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">Checkpoint Fondasi</text>
              <text x="192" y="202" text-anchor="middle" font-size="12" font-weight="600" fill="#81C995">Pixel · RGB · Aspect Ratio</text>
              <text x="192" y="220" text-anchor="middle" font-size="12" font-weight="600" fill="#8AB4F8">EDA · Hash · Data Integrity</text>
            </g>
          </svg>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>52 / 54</span></div>
    </section>

    <!-- 53: KEYNOTE TAKEAWAYS -->
    <section class="slide dark" data-title="3 Poin Utama Hari Ini" data-notes="Alokasi waktu: 1 menit. Tegaskan kembali tiga pesan inti yang paling mudah diingat.">
      <div class="cluster-4"><div class="c-circle"></div><div class="c-square"></div><div class="c-tri"></div><div class="c-pill"></div></div>
      <div class="kicker">RINGKASAN UTAMA</div>
      <h2 style="color:white;">3 Hal Terpenting yang <span style="color:var(--yellow);">Kita Bawa Pulang</span></h2>
      <div class="grid-3" style="margin-top:14px;">
        <div class="card" style="background:#292A2D; border-color:#3C4043;">
          <div class="card-top-bar bar-blue"></div>
          <div class="big-num" style="color:var(--blue);">01</div>
          <div class="card-title" style="color:white;">Image = Pixel Matrix</div>
          <div class="card-body" style="color:#BDC1C6;">Mata kita melihat bentuk, sedangkan komputer hanya membaca matriks pixel berisi nilai 0–255 dan 3 RGB channels.</div>
        </div>
        <div class="card" style="background:#292A2D; border-color:#3C4043;">
          <div class="card-top-bar bar-green"></div>
          <div class="big-num" style="color:var(--green);">02</div>
          <div class="card-title" style="color:white;">Merapikan Bahan Mentah</div>
          <div class="card-body" style="color:#BDC1C6;">Image Processing memastikan resolution seragam tanpa distorsi dan nilai pixel ternormalisasi (0–1) agar AI belajar dengan stabil.</div>
        </div>
        <div class="card" style="background:#292A2D; border-color:#3C4043;">
          <div class="card-top-bar bar-red"></div>
          <div class="big-num" style="color:var(--red);">03</div>
          <div class="card-title" style="color:white;">Exploratory Data Analysis (EDA)</div>
          <div class="card-body" style="color:#BDC1C6;">Memeriksa cahaya, <em>background complexity</em> (polos vs ramai), EXIF orientation=6, <em>corrupted files</em>, dan <em>duplicate images</em> menjaga agar AI belajar secara jujur.</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>53 / 54</span></div>
    </section>

    <!-- 54: PENUTUP -->
    <section class="slide bg-blue" data-title="Penutup &amp; Langkah Berikutnya" data-notes="Alokasi waktu: 1 menit. Tutup sesi dengan apresiasi dan beri gambaran singkat topik berikutnya tentang bagaimana AI mulai belajar dari pola gambar.">
      <div class="divider-center">
        <span class="pill dark">SELESAI · TERIMA KASIH</span>
        <h1>Terima Kasih &amp; Sampai Jumpa!</h1>
        <p>Hari ini kita sudah memahami cara komputer membaca gambar, alasan melakukan <em>Image Processing</em>, dan cara mengaudit kualitas koleksi foto kita.<br /><br /><strong>Langkah Berikutnya:</strong> Setelah dataset foto kita bersih, terstandar, dan lolos audit kualitas, pada pertemuan mendatang kita akan mulai mempelajari bagaimana model AI mengekstrak pola visual dari angka-angka <em>pixel</em> tersebut.</p>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>54 / 54</span></div>
    </section>

  </div>

  <div id="controls">
    <button class="ctrl-btn" onclick="prevSlide()">← Prev</button>
    <span id="counter" style="display:inline-flex; align-items:center; gap:5px;">
      <input id="page-jump" type="number" min="1" max="54" value="1" title="Ketik nomor slide (1-54) lalu tekan Enter" onchange="jumpToSlide(this.value)" onkeydown="if(event.key==='Enter'){{jumpToSlide(this.value); this.blur();}}" />
      <span>/ 54</span>
    </span>
    <button class="ctrl-btn" onclick="nextSlide()">Next →</button>
    <button class="ctrl-btn" onclick="toggleNotes()">Notes (N)</button>
    <button class="ctrl-btn" onclick="toggleGrid()">Grid (G)</button>
    <button class="ctrl-btn" onclick="toggleFull()">Fullscreen (F)</button>
  </div>

  <div id="notes-drawer">
    <h4>Catatan Pengajar (Speaker Notes)</h4>
    <div id="notes-text"></div>
  </div>

  <div id="grid-modal">
    <div style="max-width:1300px; margin:0 auto; display:flex; justify-content:space-between; align-items:center; color:white;">
      <h3 style="font-family:var(--font-title);">Daftar Semua Slide (54 Slides)</h3>
      <button class="ctrl-btn" onclick="toggleGrid()">Tutup (Esc)</button>
    </div>
    <div id="grid-cards" class="grid-cards"></div>
  </div>

  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    let idx = 0;

    function showSlide(n, syncHash = true) {{
      idx = Math.max(0, Math.min(slides.length - 1, n));
      slides.forEach((s, i) => s.classList.toggle('active', i === idx));
      const pj = document.getElementById('page-jump');
      if (pj) pj.value = String(idx + 1);
      document.getElementById('progress-bar').style.width = ((idx + 1) / slides.length * 100) + '%';
      document.getElementById('notes-text').textContent = slides[idx].dataset.notes || 'Tidak ada catatan.';
      if (syncHash) {{
        try {{ history.replaceState(null, '', '#slide-' + (idx + 1)); }} catch (e) {{}}
        try {{ localStorage.setItem('p01_slide_idx', String(idx)); }} catch (e) {{}}
      }}
    }}
    function jumpToSlide(val) {{
      const num = parseInt(val, 10);
      if (!isNaN(num)) showSlide(num - 1);
    }}
    function nextSlide() {{ showSlide(idx + 1); }}
    function prevSlide() {{ showSlide(idx - 1); }}
    function toggleNotes() {{ document.getElementById('notes-drawer').classList.toggle('open'); }}
    function toggleGrid() {{ document.getElementById('grid-modal').classList.toggle('open'); }}
    function toggleFull() {{
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }}

    document.addEventListener('keydown', (e) => {{
      if (document.activeElement && document.activeElement.tagName === 'INPUT') return;
      if (e.key === 'ArrowRight' || e.key === ' ') {{ e.preventDefault(); nextSlide(); }}
      else if (e.key === 'ArrowLeft') {{ e.preventDefault(); prevSlide(); }}
      else if (e.key === 'n' || e.key === 'N') toggleNotes();
      else if (e.key === 'g' || e.key === 'G') toggleGrid();
      else if (e.key === 'f' || e.key === 'F') toggleFull();
      else if (e.key === 'j' || e.key === 'J') {{ e.preventDefault(); const pj = document.getElementById('page-jump'); if (pj) {{ pj.focus(); pj.select(); }} }}
      else if (e.key === 'Escape') document.getElementById('grid-modal').classList.remove('open');
    }});

    window.addEventListener('hashchange', () => {{
      const m = window.location.hash.match(/^#slide-(\\d+)$/);
      if (m) showSlide(parseInt(m[1], 10) - 1, false);
    }});

    // Interactive Computer Vision Simulator (Slide 08)
    let compPreset = 'apple';
    let compMode = 'numbers';
    let compGrid = 8;
    const compSizes = [4, 8, 12, 16, 24, 32, 48, 64];
    let compSamples = [];

    function drawObjectToOffscreen(preset, size) {{
      const off = document.createElement('canvas');
      off.width = size; off.height = size;
      const octx = off.getContext('2d');
      octx.fillStyle = '#F8F9FA';
      octx.fillRect(0, 0, size, size);
      const s = size / 100;
      octx.save();
      octx.scale(s, s);
      if (preset === 'apple') {{
        octx.fillStyle = '#EA4335';
        octx.beginPath(); octx.arc(50, 56, 28, 0, Math.PI * 2); octx.fill();
        octx.fillStyle = '#795548';
        octx.fillRect(47, 16, 6, 14);
        octx.fillStyle = '#34A853';
        octx.beginPath(); octx.ellipse(61, 22, 11, 6, -0.4, 0, Math.PI * 2); octx.fill();
      }} else if (preset === 'star') {{
        octx.fillStyle = '#FBBC04';
        octx.beginPath();
        for (let i = 0; i < 10; i++) {{
          const ang = -Math.PI / 2 + i * Math.PI / 5;
          const rad = i % 2 === 0 ? 36 : 16;
          const px = 50 + Math.cos(ang) * rad;
          const py = 52 + Math.sin(ang) * rad;
          if (i === 0) octx.moveTo(px, py); else octx.lineTo(px, py);
        }}
        octx.closePath(); octx.fill();
      }} else {{
        octx.fillStyle = '#4285F4';
        octx.beginPath(); octx.moveTo(50, 14); octx.lineTo(84, 46); octx.lineTo(16, 46); octx.closePath(); octx.fill();
        octx.fillStyle = '#FBBC04';
        octx.fillRect(24, 46, 52, 38);
        octx.fillStyle = '#795548';
        octx.fillRect(43, 60, 14, 24);
      }}
      octx.restore();
      return octx.getImageData(0, 0, size, size).data;
    }}

    function renderCompCanvas() {{
      const canvas = document.getElementById('comp-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width;
      ctx.clearRect(0, 0, W, W);

      if (compMode === 'human') {{
        const hi = drawObjectToOffscreen(compPreset, W);
        const imgData = ctx.createImageData(W, W);
        imgData.data.set(hi);
        ctx.putImageData(imgData, 0, 0);
        compSamples = hi;
        return;
      }}

      const N = compGrid;
      const data = drawObjectToOffscreen(compPreset, N);
      compSamples = data;
      const cell = W / N;
      for (let r = 0; r < N; r++) {{
        for (let c = 0; c < N; c++) {{
          const i = (r * N + c) * 4;
          const R = data[i], G = data[i+1], B = data[i+2];
          ctx.fillStyle = `rgb(${{R}},${{G}},${{B}})`;
          ctx.fillRect(c * cell, r * cell, cell, cell);
          ctx.strokeStyle = N >= 48 ? 'rgba(32,33,36,0.08)' : 'rgba(32,33,36,0.18)';
          ctx.lineWidth = 1;
          ctx.strokeRect(c * cell, r * cell, cell, cell);
          if (compMode === 'numbers' && N <= 16) {{
            const gray = Math.round(0.299 * R + 0.587 * G + 0.114 * B);
            ctx.fillStyle = gray < 140 ? '#FFFFFF' : '#202124';
            ctx.font = `600 ${{N <= 8 ? 11 : N <= 12 ? 8.5 : 7}}px Roboto Mono, monospace`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(String(gray), c * cell + cell / 2, r * cell + cell / 2);
          }}
        }}
      }}
      if (compMode === 'numbers' && N > 16) {{
        ctx.fillStyle = 'rgba(32,33,36,0.78)';
        ctx.beginPath();
        ctx.roundRect(22, W - 30, W - 44, 22, 11);
        ctx.fill();
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '600 10.5px Roboto, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Grid rapat — hover/klik pixel untuk lihat angka', W / 2, W - 19);
      }}
    }}

    function setCompPreset(p) {{
      compPreset = p;
      document.querySelectorAll('#comp-presets button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.preset !== p);
      }});
      renderCompCanvas();
    }}
    function setCompMode(m) {{
      compMode = m;
      document.querySelectorAll('#comp-modes button').forEach((b) => {{
        const active = b.dataset.mode === m;
        b.classList.toggle('outline', !active);
        if (b.dataset.mode === 'numbers') b.classList.toggle('green', active);
      }});
      renderCompCanvas();
    }}
    function updateCompRes() {{
      const v = Number(document.getElementById('comp-res').value);
      compGrid = compSizes[v];
      document.getElementById('comp-res-lbl').textContent = `${{compGrid}} × ${{compGrid}}`;
      renderCompCanvas();
    }}

    const compCanvasEl = document.getElementById('comp-canvas');
    if (compCanvasEl) {{
      const inspect = (e) => {{
        const rect = compCanvasEl.getBoundingClientRect();
        const x = Math.floor((e.clientX - rect.left) / rect.width * (compMode === 'human' ? compCanvasEl.width : compGrid));
        const y = Math.floor((e.clientY - rect.top) / rect.height * (compMode === 'human' ? compCanvasEl.height : compGrid));
        const stride = compMode === 'human' ? compCanvasEl.width : compGrid;
        if (x < 0 || y < 0 || x >= stride || y >= stride) return;
        const i = (y * stride + x) * 4;
        const R = compSamples[i], G = compSamples[i+1], B = compSamples[i+2];
        const gray = Math.round(0.299 * R + 0.587 * G + 0.114 * B);
        document.getElementById('comp-swatch').style.background = `rgb(${{R}},${{G}},${{B}})`;
        document.getElementById('comp-px-readout').innerHTML = `Posisi (${{y+1}}, ${{x+1}})<br/>RGB: <strong>(${{R}}, ${{G}}, ${{B}})</strong> · Gray: <strong>${{gray}}</strong>`;
      }};
      compCanvasEl.addEventListener('mousemove', inspect);
      compCanvasEl.addEventListener('click', inspect);
      renderCompCanvas();
    }}

    // Build grid overview
    const gc = document.getElementById('grid-cards');
    slides.forEach((s, i) => {{
      const d = document.createElement('div');
      d.className = 'g-item';
      d.innerHTML = `<div class="g-num">SLIDE ${{String(i+1).padStart(2,'0')}}</div><div class="g-ttl">${{s.dataset.title || ''}}</div>`;
      d.onclick = () => {{ showSlide(i); toggleGrid(); }};
      gc.appendChild(d);
    }});

    // Interactive 8x8 pixel grid
    const base8 = [
      [245,245,245,245,245,245,245,245],
      [245,245,245,245,245,245,245,245],
      [245,245, 35, 35, 35, 35,245,245],
      [245,245, 35,180,180, 35,245,245],
      [245,245, 35,180,180, 35,245,245],
      [245,245, 35, 35, 35, 35,245,245],
      [245,245,245,245,245,245,245,245],
      [245,245,245,245,245,245,245,245],
    ];
    let showNums = false;
    function renderGrid8() {{
      const el = document.getElementById('grid8');
      el.innerHTML = '';
      for (let r = 0; r < 8; r++) {{
        for (let c = 0; c < 8; c++) {{
          const v = base8[r][c];
          const cell = document.createElement('div');
          cell.className = 'px-cell';
          cell.style.background = `rgb(${{v}},${{v}},${{v}})`;
          cell.style.color = v < 128 ? '#FFFFFF' : '#202124';
          cell.textContent = showNums ? v : '';
          cell.onclick = () => {{
            document.getElementById('px-info').textContent = `Kotak baris ${{r+1}}, kolom ${{c+1}} → Angka = ${{v}} (${{v < 80 ? 'Gelap' : v > 200 ? 'Putih Terang' : 'Abu-abu'}})`;
          }};
          el.appendChild(cell);
        }}
      }}
    }}
    function toggleGridNumbers() {{ showNums = !showNums; renderGrid8(); }}
    function resetGrid8() {{ showNums = false; renderGrid8(); document.getElementById('px-info').textContent = 'Klik kotak mana saja untuk mengintip angkanya!'; }}
    renderGrid8();

    // Interactive RGB mixer
    function updateRGB() {{
      const r = document.getElementById('r-sl').value;
      const g = document.getElementById('g-sl').value;
      const b = document.getElementById('b-sl').value;
      document.getElementById('r-val').textContent = r;
      document.getElementById('g-val').textContent = g;
      document.getElementById('b-val').textContent = b;
      document.getElementById('rgb-swatch').style.background = `rgb(${{r}},${{g}},${{b}})`;
      document.getElementById('rgb-code').textContent = `Warna: (${{r}}, ${{g}}, ${{b}})`;
    }}
    function setRGB(r, g, b) {{
      document.getElementById('r-sl').value = r;
      document.getElementById('g-sl').value = g;
      document.getElementById('b-sl').value = b;
      updateRGB();
    }}

    // Interactive normalization calculator
    function updateNorm() {{
      const v = Number(document.getElementById('norm-sl').value);
      document.getElementById('n-u8').textContent = v;
      document.getElementById('n-01').textContent = (v / 255).toFixed(3);
      document.getElementById('n-11').textContent = (v / 127.5 - 1).toFixed(3);
    }}

    // Interactive Question -> Answer Reveal & Quiz toggles
    function syncVisualReveal(id, shown) {{
      const vis = document.getElementById(id + '-vis');
      if (!vis) return;
      vis.querySelectorAll('.vis-q').forEach((n) => {{ n.style.display = shown ? 'none' : ''; }});
      vis.querySelectorAll('.vis-a').forEach((n) => {{ n.style.display = shown ? 'inline' : 'none'; }});
    }}
    function toggleQA(id, btn) {{
      const el = document.getElementById(id);
      const shown = el.classList.toggle('shown');
      syncVisualReveal(id, shown);
      if (btn) btn.textContent = shown ? 'Sembunyikan Jawaban' : 'Klik untuk Lihat Jawaban & Penjelasan';
    }}
    function toggleAns(id, btn) {{
      const el = document.getElementById(id);
      const shown = el.classList.toggle('shown');
      syncVisualReveal(id, shown);
      if (btn) btn.textContent = shown ? 'Sembunyikan Jawaban' : 'Lihat Jawaban';
    }}

    (function initSlide() {{
      if ('serviceWorker' in navigator && location.protocol !== 'file:') {{
        navigator.serviceWorker.register('../sw.js', {{ scope: '../' }}).catch(() => {{}});
      }}
      const m = window.location.hash.match(/^#slide-(\\d+)$/);
      if (m) {{
        showSlide(parseInt(m[1], 10) - 1);
        return;
      }}
      try {{
        const saved = localStorage.getItem('p01_slide_idx');
        if (saved !== null) {{
          showSlide(parseInt(saved, 10));
          return;
        }}
      }} catch (e) {{}}
      showSlide(0);
    }})();
  </script>
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    return str(OUT_HTML)


def verify_html(path_str: str) -> None:
    text = Path(path_str).read_text(encoding="utf-8")
    slide_count = len(re.findall(r'<section class="slide', text))
    assert slide_count == 54, f"Expected 54 slides, got {slide_count}"

    # Verify no P3/P4/P5/P7/P8/P04/P13 labels in visible slide sections
    body_part = text.split('<div id="stage-wrap">', 1)[1].split('<div id="controls">', 1)[0]
    p_codes = re.findall(r'\bP(?:0?[34578]|1[0-3])\b', body_part)
    # Exclude asset path 'assets/P01/'
    non_asset_codes = [
        m.group(0)
        for m in re.finditer(r'\bP(?:0?[34578]|1[0-3])\b', re.sub(r'assets/P01/', '', body_part))
    ]
    assert not non_asset_codes, f"Found unwanted session codes in slides: {non_asset_codes}"

    # Verify every image referenced exists
    imgs = re.findall(r'src="(assets/P01/[^"]+)"', text)
    missing = [img for img in imgs if not (ROOT_DIR / "slides" / img).exists()]
    assert not missing, f"Missing image assets: {missing}"

    # Verify speaker notes time sum == 120.0 min
    notes = re.findall(r'data-notes="([^"]+)"', text)
    assert len(notes) == 54, f"Expected 54 speaker notes, got {len(notes)}"
    total_min = 0.0
    for n in notes:
        m = re.search(r'Alokasi waktu:\s*([0-9.]+)\s*menit', n)
        assert m, f"Missing time allocation in note: {n[:60]}"
        total_min += float(m.group(1))
    assert abs(total_min - 120.0) < 1e-6, f"Speaker notes sum to {total_min} min instead of 120.0"

    print(f"HTML interaktif {slide_count} slide berhasil dibuat: {path_str}")
    print(f"Verifikasi lolos: 54 slide, 0 kode P4/P5/P7/P8, {len(imgs)} gambar valid, total waktu notes = {total_min:.1f} menit.")


if __name__ == "__main__":
    out = build_html()
    verify_html(out)
