"""Generate 57-slide beginner-friendly interactive HTML5 presentation slides/P01_image_processing_eda.html.

Designed for non-IT / non-technical learners:
- Clear flow from AI Fundamentals (what AI/ML/DL is, why we use AI here, how it works end-to-end) ->
  how humans see images -> how computers read & display images ->
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
  <title>P01 - Understanding Images, Image Processing &amp; EDA (57 Slides)</title>
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
          <span style="font-size:13.5px; font-weight:600; color:#5F6368;">Fase Fondasi &nbsp;·&nbsp; 120 Menit</span>
        </div>
      </div>

      <div style="position:relative; z-index:1; display:grid; grid-template-columns: 1.65fr 0.72fr; align-items:center; gap:18px; margin:auto 0;">
        <div>
          <h1 style="font-family:var(--font-title); font-size:clamp(28px,3.4vw,44px); font-weight:700; line-height:1.12; color:#202124; margin:0; letter-spacing:-0.6px;">
            P01 - Understanding Images,<br />
            <span style="display:inline-block; padding-top:2px; background:linear-gradient(90deg, #4285F4 0%, #8E24AA 55%, #EA4335 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Image Processing &amp; EDA</span>
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
    <section class="slide" data-title="Peta Perjalanan Belajar (5 Bab)" data-notes="Alokasi waktu: 1 menit. Ini alur belajar kita hari ini: mulai dari dasar cara komputer melihat gambar, peran AI & alasan belajar image processing, hingga praktik memeriksa kualitas foto.">
      <div class="kicker">PETA PERJALANAN BELAJAR</div>
      <h2>Dari Foto Biasa Menuju <span class="hl-blue">Data Siap AI</span></h2>
      <p class="subtitle">Disusun bertahap dengan analogi sehari-hari — tidak perlu latar belakang IT untuk memahaminya.</p>
      <div class="step-list">
        <div class="step-item"><div class="step-num">01</div><div><div class="step-title">Bagaimana Kita &amp; Komputer Melihat Gambar</div><div class="step-desc">Perbedaan cara mata manusia vs komputer membaca foto, pixel, nilai 0–255, dan RGB channels.</div></div></div>
        <div class="step-item"><div class="step-num red">02</div><div><div class="step-title">Peran AI &amp; Mengapa Perlu Image Processing?</div><div class="step-desc">Kenapa foto butuh AI, apa itu AI, bagaimana cara kerjanya, serta kenapa foto mentah wajib dirapikan dulu.</div></div></div>
        <div class="step-item"><div class="step-num yellow">03</div><div><div class="step-title">Exploratory Data Analysis (EDA)</div><div class="step-desc">Mengecek keseimbangan jumlah foto, grafik pencahayaan, serta membedakan latar polos vs ramai.</div></div></div>
        <div class="step-item"><div class="step-num green">04</div><div><div class="step-title">Tiga Jebakan Tersembunyi Kamera HP</div><div class="step-desc">Mendeteksi EXIF orientation yang terputar, duplicate images, dan corrupted files.</div></div></div>
        <div class="step-item"><div class="step-num">05</div><div><div class="step-title">Praktik Santai, Diskusi &amp; Kuis Interaktif</div><div class="step-desc">Melihat hasil nyata pada 120 foto sampel, diskusi tantangan latar polos vs ramai, kamus istilah, &amp; kuis.</div></div></div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>02 / 57</span></div>
    </section>

    <!-- 03: ALUR SESI 120 MENIT -->
    <section class="slide" data-title="Alur Sesi 120 Menit" data-notes="Alokasi waktu: 1 menit. Kita bagi waktu 120 menit agar santai, ada jeda istirahat, dan semua materi tuntas di kelas.">
      <div class="kicker">AGENDA · 120 MENIT</div>
      <h2>Alur Sesi <span class="hl-blue">Hari Ini</span></h2>
      <p class="subtitle">Belajar pelan-pelan, penuh ilustrasi visual, dan tanya-jawab interaktif yang tuntas di kelas.</p>
      <div class="grid-3">
        <div class="card tint-blue"><div class="card-top-bar bar-blue"></div><div class="card-title">00–10 · Pemanasan</div><div class="card-body">Menyegarkan ingatan tentang data angka dan membayangkan bagaimana komputer "melihat" sebuah foto.</div></div>
        <div class="card tint-red"><div class="card-top-bar bar-red"></div><div class="card-title">10–40 · Teori &amp; Ilustrasi</div><div class="card-body">Memahami pixel &amp; RGB, peran AI pada foto, alasan Image Processing, EDA dataset, serta 3 jebakan file foto.</div></div>
        <div class="card tint-yellow"><div class="card-top-bar bar-yellow"></div><div class="card-title">40–45 · Istirahat Singkat</div><div class="card-body">Jeda 5 menit untuk minum air dan meregangkan mata sebelum melihat contoh praktik.</div></div>
        <div class="card tint-green"><div class="card-top-bar bar-green"></div><div class="card-title">45–95 · Praktik Terpandu</div><div class="card-body">Menjalankan 6 langkah pemeriksaan foto secara bertahap pada koleksi foto sampel.</div></div>
        <div class="card tint-blue"><div class="card-top-bar bar-blue"></div><div class="card-title">95–110 · Diskusi Kasus</div><div class="card-body">Menebak tantangan nyata: lebih mudah mana bagi AI, foto berlatar polos atau foto berlatar ramai?</div></div>
        <div class="card tint-red"><div class="card-top-bar bar-red"></div><div class="card-title">110–120 · Kuis &amp; Penutup</div><div class="card-body">Kuis interaktif 5 soal dengan pembahasan langsung serta rangkuman poin terpenting hari ini.</div></div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>03 / 57</span></div>
    </section>

    <!-- 04: TUJUAN BELAJAR -->
    <section class="slide" data-title="Apa yang Akan Kita Kuasai?" data-notes="Alokasi waktu: 1 menit. Tiga kemampuan praktis yang akan kita bawa pulang setelah sesi selesai.">
      <div class="kicker">TUJUAN BELAJAR</div>
      <h2>Apa yang Akan Kita <span class="hl-blue">Kuasai</span>?</h2>
      <div class="grid-3">
        <div class="card"><div class="card-top-bar bar-blue"></div><span class="pill blue" style="margin-bottom:6px;">POIN 01</span><div class="card-title">Paham Bahasa Gambar Komputer</div><div class="card-body"><ul><li>Tahu bedanya cara mata kita vs komputer membaca foto.</li><li>Mengerti bahwa setiap foto sebenarnya adalah tabel berisi angka 0–255.</li><li>Mengerti konsep RGB channels (Red, Green, Blue).</li></ul></div><div class="callout"><strong>Hasil:</strong> Gambar digital tidak lagi terasa seperti <em>black box</em>.</div></div>
        <div class="card"><div class="card-top-bar bar-green"></div><span class="pill green" style="margin-bottom:6px;">POIN 02</span><div class="card-title">Paham Peran AI &amp; Image Processing</div><div class="card-body"><ul><li>Mengerti kenapa kita butuh AI dan bagaimana cara AI belajar dari foto.</li><li>Mengerti kenapa foto wajib dirapikan (resize proporsional &amp; normalisasi 0–1) sebelum masuk ke AI.</li></ul></div><div class="callout green"><strong>Hasil:</strong> Paham hubungan erat antara bahan foto yang rapi dan kecerdasan AI.</div></div>
        <div class="card"><div class="card-top-bar bar-red"></div><span class="pill red" style="margin-bottom:6px;">POIN 03</span><div class="card-title">Bisa Mengaudit Koleksi Foto</div><div class="card-body"><ul><li>Mampu mengecek apakah jumlah foto sudah seimbang.</li><li>Bisa membedakan foto gelap, terang, polos, dan ramai.</li><li>Tahu cara menyaring foto rusak dan kembar.</li></ul></div><div class="callout red"><strong>Hasil:</strong> Koleksi foto bersih, sehat, dan jujur untuk AI.</div></div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>04 / 57</span></div>
    </section>

    <!-- 05: PEMANTIK -->
    <section class="slide" data-title="Pemanasan: Dari Angka Biasa ke Foto" data-notes="Alokasi waktu: 1.5 menit. Sebelumnya kita mengenal data dalam bentuk tabel angka biasa. Sekarang, bayangkan kalau input yang masuk ke komputer adalah foto dari kamera HP.">
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

    <!-- 10: APA ITU PIKSEL -->
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
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>10 / 57</span></div>
    </section>

    <!-- 11: INTERACTIVE 8x8 GRID -->
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
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>11 / 57</span></div>
    </section>

    <!-- 12: TIGA LAMPU WARNA RGB -->
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
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>12 / 57</span></div>
    </section>

    <!-- 13: INTERACTIVE RGB MIXER -->
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
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>13 / 57</span></div>
    </section>

    <!-- 14: QA REVEAL #1 (SETELAH PAHAM PIXEL & 3 WARNA RGB) -->
    <section class="slide" data-title="Tanya-Jawab #1: Seberapa Banyak Angka dalam 1 Foto?" data-notes="Alokasi waktu: 1.5 menit. Nah, setelah peserta paham apa itu Pixel dan bahwa 1 Pixel punya 3 angka RGB, ajak mereka menebak berapa total angka dalam 1 foto 224x224!">
      <div class="kicker">TANYA &amp; JAWAB INTERAKTIF · #1</div>
      <h2>Coba Tebak: <span class="hl-blue">Berapa Banyak Angka</span> di 1 Foto?</h2>
      <div class="split-60-40">
        <div class="qa-box" style="margin:0; justify-content:center;">
          <div class="qa-question">
            Tadi kita sudah lihat bahwa <strong>1 kotak pixel</strong> memiliki <strong>3 angka warna (R, G, B)</strong>. Jika komputer membaca sebuah foto berukuran <strong>224 × 224 pixels</strong>, kira-kira berapa total angka yang dibaca komputer untuk 1 foto saja?
          </div>
          <div class="qa-choices">
            <div class="qa-choice"><strong>A.</strong> Sekitar 672 angka saja</div>
            <div class="qa-choice"><strong>B.</strong> Sekitar 50.176 angka</div>
            <div class="qa-choice"><strong>C.</strong> Lebih dari 150.000 angka!</div>
          </div>
          <button class="btn-ui" onclick="toggleQA('qa1', this)">Klik untuk Lihat Jawaban &amp; Penjelasan</button>
          <div id="qa1" class="qa-answer">
            <strong>Jawaban: C — Tepatnya 150.528 angka!</strong><br />
            Hitungan sederhananya: <code>224 baris × 224 kolom × 3 warna (RGB) = 150.528 angka</code>.<br />
            Bayangkan jika kita punya 1.000 foto, berarti komputer harus membaca lebih dari <strong>150 juta angka</strong>!
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
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>14 / 57</span></div>
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
    <section class="slide bg-red" data-title="Bab 2: Peran AI &amp; Mengapa Perlu Image Processing?" data-notes="Alokasi waktu: 0.5 menit. Di Bab 1 kita sudah tahu foto = lautan angka 0-255. Sekarang kita masuk ke Bab 2: bagaimana AI belajar dari angka tersebut, dan mengapa foto mentah wajib dirapikan dulu.">
      <div class="divider-center">
        <span class="pill dark">BAB 2 · PERAN AI &amp; IMAGE PROCESSING</span>
        <h1>Bagaimana AI Membaca Foto &amp; Mengapa Perlu Dirapikan?</h1>
        <p>Menjembatani lautan angka pixel dari Bab 1 menuju cara kerja AI, alasan kita memakai AI, dan pentingnya merapikan foto mentah.</p>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>18 / 57</span></div>
    </section>

    <!-- 19: AI FUNDAMENTAL 1/3 - APA ITU AI? (INTERACTIVE 3-LEVEL EXPLORER) -->
    <section class="slide" data-title="AI Fundamental (1/3): Apa Itu AI di Project Ini?" data-notes="Alokasi waktu: 1.5 menit. Klik 3 tombol di atas ilustrasi untuk menunjukkan perbedaan Program Biasa, Machine Learning, dan Deep Learning secara visual.">
      <div class="kicker">BAB 2 · AI FUNDAMENTAL 1/3 · SIMULATOR KONSEP</div>
      <h2>Dari Angka Pixel ke Makna: <span class="hl-blue">Apa Itu AI</span>?</h2>
      <p class="subtitle">Klik 3 tombol di bawah untuk melihat perbedaan cara kerja <strong>Program Biasa</strong>, <strong>Machine Learning</strong>, dan <strong>Deep Learning</strong>:</p>
      <div class="split-60-40">
        <div class="card surface" style="justify-content:space-between; gap:10px; padding:14px 18px;">
          <div id="ai1-tabs" style="display:flex; gap:6px; flex-wrap:wrap; justify-content:center;">
            <button type="button" class="btn-ui outline" data-tab="rule" onclick="setAi1Tab('rule')">1. Program Biasa</button>
            <button type="button" class="btn-ui outline" data-tab="ml" onclick="setAi1Tab('ml')">2. Machine Learning</button>
            <button type="button" class="btn-ui" data-tab="dl" onclick="setAi1Tab('dl')">3. Deep Learning (Project Kita)</button>
          </div>

          <!-- Visual Panel 1: Program Biasa -->
          <div id="ai1-panel-rule" style="display:none; flex-direction:column; gap:10px; flex:1; justify-content:center;">
            <svg viewBox="0 0 500 185" style="width:100%; max-height:185px;">
              <rect x="8" y="18" width="138" height="148" rx="14" fill="#FFFFFF" stroke="#DADCE0" stroke-width="2"/>
              <text x="77" y="42" text-anchor="middle" font-family="Poppins, sans-serif" font-size="11.5" font-weight="700" fill="#202124">Input: Manusia</text>
              <rect x="22" y="54" width="110" height="44" rx="8" fill="#FCE8E6" stroke="#EA4335"/>
              <text x="77" y="74" text-anchor="middle" font-size="10.5" font-weight="700" fill="#C5221F">Tulis Rumus Kaku</text>
              <text x="77" y="89" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="9.5" fill="#202124">if (x,y) == kuning</text>
              <rect x="22" y="108" width="110" height="44" rx="8" fill="#F8F9FA" stroke="#DADCE0"/>
              <text x="77" y="128" text-anchor="middle" font-size="10.5" font-weight="700" fill="#3C4043">+ Data Foto</text>
              <text x="77" y="143" text-anchor="middle" font-size="9.5" fill="#5F6368">150.528 angka</text>

              <path d="M154 92 L188 92" stroke="#5F6368" stroke-width="3"/><polygon points="186,86 198,92 186,98" fill="#5F6368"/>

              <rect x="204" y="34" width="136" height="116" rx="14" fill="#202124"/>
              <text x="272" y="68" text-anchor="middle" font-family="Poppins, sans-serif" font-size="12" font-weight="700" fill="#FBBC04">Komputer</text>
              <text x="272" y="90" text-anchor="middle" font-size="11" fill="#E8EAED">Hanya mengecek</text>
              <text x="272" y="107" text-anchor="middle" font-size="11" fill="#E8EAED">aturan manusia</text>
              <text x="272" y="126" text-anchor="middle" font-size="10" fill="#9AA0A6">(Tidak bisa belajar)</text>

              <path d="M348 92 L382 92" stroke="#5F6368" stroke-width="3"/><polygon points="380,86 392,92 380,98" fill="#5F6368"/>

              <rect x="398" y="34" width="94" height="116" rx="14" fill="#F1F3F4" stroke="#DADCE0" stroke-width="2"/>
              <text x="445" y="76" text-anchor="middle" font-family="Poppins, sans-serif" font-size="11.5" font-weight="700" fill="#202124">Output</text>
              <text x="445" y="98" text-anchor="middle" font-size="10.5" fill="#C5221F" font-weight="700">Kaku &amp; Mudah</text>
              <text x="445" y="114" text-anchor="middle" font-size="10.5" fill="#C5221F" font-weight="700">Gagal di Foto</text>
            </svg>
            <div class="callout red" style="margin:0;"><strong>Program Biasa:</strong> Manusia harus memikirkan semua rumusnya sendiri. Cocok untuk hitungan kasir/pajak, tapi gagal untuk foto nyata.</div>
          </div>

          <!-- Visual Panel 2: Machine Learning -->
          <div id="ai1-panel-ml" style="display:none; flex-direction:column; gap:10px; flex:1; justify-content:center;">
            <svg viewBox="0 0 500 185" style="width:100%; max-height:185px;">
              <rect x="8" y="14" width="154" height="156" rx="14" fill="#FFFFFF" stroke="#4285F4" stroke-width="2"/>
              <text x="85" y="36" text-anchor="middle" font-family="Poppins, sans-serif" font-size="11" font-weight="700" fill="#1A73E8">Input: Banyak Contoh</text>
              <!-- Mini photo cards -->
              <rect x="20" y="46" width="38" height="38" rx="6" fill="#E8F0FE" stroke="#4285F4"/><circle cx="39" cy="65" r="11" fill="#4285F4"/>
              <rect x="66" y="46" width="38" height="38" rx="6" fill="#FCE8E6" stroke="#EA4335"/><rect x="75" y="55" width="20" height="20" fill="#EA4335"/>
              <rect x="112" y="46" width="38" height="38" rx="6" fill="#FEF7E0" stroke="#FBBC04"/><polygon points="131,52 143,76 119,76" fill="#FBBC04"/>
              <rect x="20" y="96" width="130" height="58" rx="8" fill="#E6F4EA" stroke="#34A853"/>
              <text x="85" y="118" text-anchor="middle" font-size="10.5" font-weight="700" fill="#137333">+ Nama / Labelnya</text>
              <text x="85" y="136" text-anchor="middle" font-size="9.5" fill="#202124">"Lingkaran", "Persegi",</text>
              <text x="85" y="149" text-anchor="middle" font-size="9.5" fill="#202124">"Segitiga"</text>

              <path d="M168 92 L198 92" stroke="#4285F4" stroke-width="3"/><polygon points="196,86 208,92 196,98" fill="#4285F4"/>

              <rect x="214" y="26" width="136" height="132" rx="14" fill="#E8F0FE" stroke="#4285F4" stroke-width="2.5"/>
              <text x="282" y="56" text-anchor="middle" font-family="Poppins, sans-serif" font-size="12" font-weight="700" fill="#1A73E8">Machine Learning</text>
              <text x="282" y="78" text-anchor="middle" font-size="11" fill="#202124">Mencari pola sendiri</text>
              <text x="282" y="95" text-anchor="middle" font-size="11" fill="#202124">dari ratusan contoh</text>
              <rect x="232" y="112" width="100" height="28" rx="8" fill="#4285F4"/>
              <text x="282" y="130" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">Belajar Otomatis</text>

              <path d="M356 92 L386 92" stroke="#34A853" stroke-width="3"/><polygon points="384,86 396,92 384,98" fill="#34A853"/>

              <rect x="402" y="26" width="90" height="132" rx="14" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/>
              <text x="447" y="68" text-anchor="middle" font-family="Poppins, sans-serif" font-size="11.5" font-weight="700" fill="#137333">Hasil</text>
              <text x="447" y="92" text-anchor="middle" font-size="10.5" font-weight="700" fill="#202124">Model Pintar</text>
              <text x="447" y="110" text-anchor="middle" font-size="9.5" fill="#137333">Bisa menebak</text>
              <text x="447" y="124" text-anchor="middle" font-size="9.5" fill="#137333">data baru!</text>
            </svg>
            <div class="callout" style="margin:0;"><strong>Machine Learning:</strong> Kita tidak lagi menulis rumus, melainkan memberikan <strong>contoh data + label</strong> agar komputer menemukan polanya sendiri.</div>
          </div>

          <!-- Visual Panel 3: Deep Learning (Default visible) -->
          <div id="ai1-panel-dl" style="display:flex; flex-direction:column; gap:10px; flex:1; justify-content:center;">
            <svg viewBox="0 0 500 185" style="width:100%; max-height:185px;">
              <!-- Step 0: Input Photo -->
              <rect x="6" y="24" width="96" height="136" rx="12" fill="#FFFFFF" stroke="#DADCE0" stroke-width="2"/>
              <text x="54" y="44" text-anchor="middle" font-family="Poppins, sans-serif" font-size="10.5" font-weight="700" fill="#202124">Foto Input</text>
              <polygon points="54,58 63,78 85,78 67,91 74,112 54,99 34,112 41,91 23,78 45,78" fill="#FBBC04" stroke="#E37400" stroke-width="1.5"/>
              <text x="54" y="138" text-anchor="middle" font-size="9.5" fill="#5F6368">Ribuan Pixel</text>

              <path d="M106 92 L124 92" stroke="#4285F4" stroke-width="2.5"/><polygon points="122,87 130,92 122,97" fill="#4285F4"/>

              <!-- Layer 1: Edges -->
              <rect x="134" y="24" width="102" height="136" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
              <text x="185" y="44" text-anchor="middle" font-family="Poppins, sans-serif" font-size="10.5" font-weight="700" fill="#1A73E8">Lapisan 1</text>
              <rect x="150" y="54" width="70" height="60" rx="8" fill="#202124"/>
              <line x1="160" y1="102" x2="185" y2="62" stroke="#FFFFFF" stroke-width="2.5"/>
              <line x1="185" y1="62" x2="210" y2="102" stroke="#FFFFFF" stroke-width="2.5"/>
              <line x1="158" y1="84" x2="212" y2="84" stroke="#4285F4" stroke-width="2"/>
              <text x="185" y="132" text-anchor="middle" font-size="10" font-weight="700" fill="#1A73E8">Kenali Garis</text>
              <text x="185" y="146" text-anchor="middle" font-size="9" fill="#3C4043">&amp; Tepi (Edges)</text>

              <path d="M240 92 L258 92" stroke="#FBBC04" stroke-width="2.5"/><polygon points="256,87 264,92 256,97" fill="#E37400"/>

              <!-- Layer 2: Shapes & Parts -->
              <rect x="268" y="24" width="102" height="136" rx="12" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
              <text x="319" y="44" text-anchor="middle" font-family="Poppins, sans-serif" font-size="10.5" font-weight="700" fill="#B06000">Lapisan 2</text>
              <rect x="284" y="54" width="70" height="60" rx="8" fill="#FFFFFF" stroke="#FBBC04" stroke-width="1.5"/>
              <polygon points="319,60 328,80 309,80" fill="#FBBC04"/>
              <polygon points="295,85 315,78 308,98" fill="#EA4335"/>
              <polygon points="343,85 323,78 330,98" fill="#34A853"/>
              <text x="319" y="132" text-anchor="middle" font-size="10" font-weight="700" fill="#B06000">Kenali Sudut</text>
              <text x="319" y="146" text-anchor="middle" font-size="9" fill="#3C4043">&amp; Bagian Bentuk</text>

              <path d="M374 92 L392 92" stroke="#34A853" stroke-width="2.5"/><polygon points="390,87 398,92 390,97" fill="#34A853"/>

              <!-- Layer 3: Full Object -->
              <rect x="402" y="24" width="92" height="136" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="2.5"/>
              <text x="448" y="44" text-anchor="middle" font-family="Poppins, sans-serif" font-size="10.5" font-weight="700" fill="#137333">Lapisan 3</text>
              <circle cx="448" cy="84" r="24" fill="#34A853"/>
              <text x="448" y="89" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">98%</text>
              <text x="448" y="130" text-anchor="middle" font-size="10.5" font-weight="700" fill="#137333">"Bintang!"</text>
              <text x="448" y="146" text-anchor="middle" font-size="9" fill="#202124">Objek Utuh</text>
            </svg>
            <div class="callout green" style="margin:0;"><strong>Deep Learning (Mesin Project Kita):</strong> Meniru jaringan saraf otak manusia untuk mengenali gambar secara berlapis — dari <strong>garis tepi &rarr; bentuk bagian &rarr; objek utuh</strong>!</div>
          </div>
        </div>

        <div class="card">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">ANALOGI SEHARI-HARI</span>
          <div class="card-title">Seperti Mengajari Anak Kecil</div>
          <div class="card-body">
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:8px;">
              <div style="display:flex; align-items:center; gap:8px; background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:6px 8px;">
                <img src="assets/P01/sample_polos.jpg" alt="Contoh Foto 1" style="width:40px; height:40px; object-fit:cover; border-radius:6px;" />
                <div style="font-size:10.5px; line-height:1.25;"><strong>Contoh 1</strong><br /><span style="color:var(--muted);">"Ini Bintang"</span></div>
              </div>
              <div style="display:flex; align-items:center; gap:8px; background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:6px 8px;">
                <img src="assets/P01/sample_ramai.jpg" alt="Contoh Foto 2" style="width:40px; height:40px; object-fit:cover; border-radius:6px;" />
                <div style="font-size:10.5px; line-height:1.25;"><strong>Contoh 2</strong><br /><span style="color:var(--muted);">"Ini Heksagon"</span></div>
              </div>
            </div>
            <ul>
              <li>Saat mengajari anak kecil mengenali karakter Disney, kita <strong>tidak pernah memberinya rumus matematika</strong> ukuran telinga atau tabel RGB.</li>
              <li>Kita cukup <strong>menunjukkan banyak contoh foto</strong> sambil menyebutkan namanya.</li>
              <li>Dari contoh-contoh itulah ia mengenali cirinya sendiri!</li>
            </ul>
          </div>
          <div class="callout" style="margin-top:auto;"><strong>Kesimpulan:</strong> AI di project kita belajar langsung dari <strong>koleksi contoh foto</strong> yang kita siapkan.</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>19 / 57</span></div>
    </section>

    <!-- 20: AI FUNDAMENTAL 2/3 - KENAPA KITA MENGGUNAKAN AI DI SINI? (INTERACTIVE SIMULATOR) -->
    <section class="slide" data-title="AI Fundamental (2/3): Mengapa Kita Menggunakan AI?" data-notes="Alokasi waktu: 1.5 menit. Ajak peserta mengklik 4 kondisi foto di kiri untuk melihat langsung mengapa aturan manual (if-else) langsung gagal saat foto bergeser, miring, atau latarnya ramai, sedangkan AI tetap berhasil!">
      <div class="kicker">BAB 2 · AI FUNDAMENTAL 2/3 · SIMULATOR INTERAKTIF</div>
      <h2>Mengapa Mengenali Foto <span class="hl-red">Wajib Pakai AI</span>? (Uji Langsung!)</h2>
      <p class="subtitle">Coba klik 4 kondisi pemotretan di bawah untuk menguji <strong>Aturan Manual (<code>if-else</code>)</strong> vs <strong>Model AI</strong>:</p>
      <div class="split-60-40">
        <div class="card surface" style="align-items:center; justify-content:space-between; padding:12px 16px; gap:8px;">
          <div id="ai2-btns" style="display:flex; gap:6px; flex-wrap:wrap; justify-content:center;">
            <button type="button" class="btn-ui outline" data-cond="center" onclick="setAi2Cond('center')">1. Posisi Tengah</button>
            <button type="button" class="btn-ui" data-cond="shift" onclick="setAi2Cond('shift')">2. Geser ke Pojok</button>
            <button type="button" class="btn-ui outline" data-cond="tilt" onclick="setAi2Cond('tilt')">3. Miring &amp; Kecil</button>
            <button type="button" class="btn-ui outline" data-cond="busy" onclick="setAi2Cond('busy')">4. Latar Ramai</button>
          </div>

          <svg id="ai2-svg" viewBox="0 0 460 210" style="width:100%; max-height:205px; background:#FFFFFF; border:1.5px solid var(--border); border-radius:14px;">
            <!-- Busy background clutter (hidden unless cond == busy) -->
            <g id="ai2-bg-busy" style="display:none; opacity:0.85;">
              <rect x="0" y="0" width="460" height="210" fill="#3C4043"/>
              <circle cx="70" cy="50" r="28" fill="#EA4335" opacity="0.6"/>
              <rect x="330" y="25" width="75" height="55" rx="8" fill="#4285F4" opacity="0.55"/>
              <circle cx="230" cy="105" r="32" fill="#FBBC04" opacity="0.75"/>
              <polygon points="90,180 140,120 185,185" fill="#34A853" opacity="0.55"/>
              <rect x="290" y="130" width="90" height="60" rx="10" fill="#EA4335" opacity="0.5"/>
              <circle cx="395" cy="115" r="22" fill="#FEF7E0" opacity="0.6"/>
            </g>

            <!-- Grid lines to remind of pixels -->
            <g stroke="rgba(0,0,0,0.06)" stroke-width="1">
              <line x1="115" y1="0" x2="115" y2="210"/><line x1="230" y1="0" x2="230" y2="210"/><line x1="345" y1="0" x2="345" y2="210"/>
              <line x1="0" y1="70" x2="460" y2="70"/><line x1="0" y1="140" x2="460" y2="140"/>
            </g>

            <!-- Target Star Object + AI Pattern Box -->
            <g id="ai2-star-group" transform="translate(345, 138)">
              <rect x="-46" y="-46" width="92" height="92" rx="12" fill="rgba(52,168,83,0.12)" stroke="#34A853" stroke-width="2.5" stroke-dasharray="6 4"/>
              <polygon points="0,-36 10,-11 37,-11 15,5 23,32 0,16 -23,32 -15,5 -37,-11 -10,-11" fill="#FBBC04" stroke="#B06000" stroke-width="2"/>
              <rect x="-44" y="-64" width="88" height="18" rx="6" fill="#34A853"/>
              <text x="0" y="-51" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="9.5" font-weight="700" fill="#FFFFFF">AI: Pola Bintang</text>
            </g>

            <!-- Fixed Manual Rule Sensor at Center (230, 105) -->
            <g id="ai2-manual-sensor">
              <rect x="202" y="77" width="56" height="56" rx="8" fill="rgba(234,67,53,0.10)" stroke="#EA4335" stroke-width="2.5"/>
              <line x1="230" y1="70" x2="230" y2="140" stroke="#EA4335" stroke-width="1.5"/>
              <line x1="195" y1="105" x2="265" y2="105" stroke="#EA4335" stroke-width="1.5"/>
              <rect x="148" y="138" width="164" height="20" rx="6" fill="#202124"/>
              <text x="230" y="152" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="9.5" font-weight="600" fill="#FBBC04">Cek if-else: pixel[tengah]</text>
            </g>
          </svg>

          <div id="ai2-caption" style="font-size:12.5px; color:#3C4043; text-align:center; background:#FFFFFF; border:1px solid var(--border); border-radius:10px; padding:6px 12px; width:100%;">
            <strong>Kondisi 2 (Geser ke Pojok):</strong> Objek bintang bergeser ke kanan bawah. Titik tengah menjadi kosong (putih), sehingga aturan manual <code>if-else</code> langsung gagal!
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:12px; justify-content:space-between;">
          <div id="ai2-card-rule" class="card tint-red" style="flex:1; padding:14px 18px;">
            <div class="card-top-bar bar-red"></div>
            <span class="pill red">PROGRAM BIASA (ATURAN IF-ELSE)</span>
            <div id="ai2-rule-status" class="card-title" style="color:#C5221F;">❌ GAGAL MENEBak!</div>
            <div id="ai2-rule-desc" class="card-body" style="font-size:13.5px;">
              Aturan manual hanya mengecek koordinat <code>pixel[tengah]</code>. Karena bintang bergeser, titik tengah berisi warna putih (<code>255,255,255</code>) dan program mengira tidak ada bintang!
            </div>
          </div>

          <div id="ai2-card-ai" class="card tint-green" style="flex:1; padding:14px 18px;">
            <div class="card-top-bar bar-green"></div>
            <span class="pill green">MODEL AI (DEEP LEARNING)</span>
            <div id="ai2-ai-status" class="card-title" style="color:#137333;">✅ BERHASIL (Keyakinan: 98%)</div>
            <div id="ai2-ai-desc" class="card-body" style="font-size:13.5px;">
              AI tidak menghafal koordinat titik mati, melainkan memindai <strong>pola 5 sudut lancip &amp; warna kuning</strong> di seluruh area foto sehingga tetap akurat!
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>20 / 57</span></div>
    </section>

    <!-- 21: AI FUNDAMENTAL 3/3 - BAGAIMANA PENGGUNAANNYA & SIMULASI GARBAGE IN GARBAGE OUT -->
    <section class="slide" data-title="AI Fundamental (3/3): Bagaimana Penggunaan AI di Project Ini?" data-notes="Alokasi waktu: 1.5 menit. Klik tombol saklar di atas untuk membandingkan apa yang terjadi pada AI jika foto mentah langsung dimasukkan (Tanpa P01) vs jika foto dirapikan dulu dengan Image Processing & EDA (Pakai P01).">
      <div class="kicker">BAB 2 · AI FUNDAMENTAL 3/3 · SIMULASI ALUR PROJECT</div>
      <h2>Bagaimana <span class="hl-green">Cara Penggunaan AI</span> di Project Kita?</h2>
      <p class="subtitle">Uji 2 skenario di bawah untuk melihat mengapa <strong>Tahap 1 (Image Processing &amp; EDA)</strong> menjadi penentu utama:</p>
      <div style="display:flex; gap:8px; margin-bottom:10px; flex-wrap:wrap;">
        <button id="ai3-btn-good" type="button" class="btn-ui green" onclick="setAi3Mode('good')">✅ Skenario A: Foto Dirapikan Dulu (Pakai Image Processing &amp; EDA)</button>
        <button id="ai3-btn-bad" type="button" class="btn-ui outline" onclick="setAi3Mode('bad')">❌ Skenario B: Foto Mentah HP Langsung Masuk AI (Tanpa P01)</button>
      </div>

      <!-- 3-Stage Interactive Pipeline -->
      <div class="grid-3" style="flex:1; min-height:0;">
        <!-- Stage 1 -->
        <div id="ai3-st1" class="card tint-yellow" style="border-width:2px;">
          <div class="card-top-bar bar-yellow"></div>
          <span id="ai3-st1-pill" class="pill yellow">TAHAP 1 · FOKUS HARI INI (P01)</span>
          <div id="ai3-st1-title" class="card-title">1. Siapkan &amp; Rapikan Foto</div>
          <div style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:8px; display:flex; align-items:center; justify-content:center; height:128px; overflow:hidden;">
            <img id="ai3-st1-img" src="assets/P01/06_resize_aspect_ratio.png" alt="Ilustrasi Tahap 1" style="max-width:100%; max-height:100%; object-fit:contain;" />
          </div>
          <div id="ai3-st1-body" class="card-body" style="font-size:13px;">
            Foto di-resize proporsional <code>224×224</code> tanpa gepeng, skala angkanya disederhanakan ke <code>0–1</code>, posisinya tegak, dan bebas file rusak/kembar.
          </div>
        </div>

        <!-- Stage 2 -->
        <div id="ai3-st2" class="card tint-blue">
          <div class="card-top-bar bar-blue"></div>
          <span id="ai3-st2-pill" class="pill blue">TAHAP 2 · PROSES BELAJAR</span>
          <div id="ai3-st2-title" class="card-title">2. Latih Model AI (Training)</div>
          <div style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:8px; display:flex; align-items:center; justify-content:center; height:128px; overflow:hidden;">
            <img id="ai3-st2-img" src="assets/P01/03_synthetic_examples.png" alt="Ilustrasi Tahap 2" style="max-width:100%; max-height:100%; object-fit:contain;" />
          </div>
          <div id="ai3-st2-body" class="card-body" style="font-size:13px;">
            AI mempelajari pola bentuk &amp; warna dari ratusan contoh foto yang <strong>seragam dan seimbang</strong> (kondisi <strong>polos &amp; ramai</strong>).
          </div>
        </div>

        <!-- Stage 3 -->
        <div id="ai3-st3" class="card tint-green">
          <div class="card-top-bar bar-green"></div>
          <span id="ai3-st3-pill" class="pill green">TAHAP 3 · SIAP DIGUNAKAN</span>
          <div id="ai3-st3-title" class="card-title">3. Tebak Foto Baru (Prediction)</div>
          <div id="ai3-st3-box" style="background:#202124; color:#FFFFFF; border-radius:12px; padding:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; height:128px; gap:6px; text-align:center;">
            <div style="font-family:var(--font-code); font-size:11px; color:#81C995;">INPUT: Foto Baru dari HP</div>
            <div style="font-family:var(--font-title); font-size:20px; font-weight:700; color:#FBBC04;">Prediksi: Bintang ⭐</div>
            <div style="background:#34A853; color:#FFFFFF; font-size:11.5px; font-weight:700; padding:3px 12px; border-radius:999px;">Keyakinan AI: 98% (Akurat!)</div>
          </div>
          <div id="ai3-st3-body" class="card-body" style="font-size:13px;">
            Saat diberi foto baru, AI mampu menebak nama karakternya dengan <strong>akurat &amp; konsisten</strong>!
          </div>
        </div>
      </div>

      <div id="ai3-banner" class="callout green" style="margin-top:10px;">
        <strong>Analogi Dapur &amp; Koki Pintar:</strong> Sepintar apa pun kokinya (<strong>AI</strong>), masakannya hanya enak jika bahan bakunya (<strong>foto</strong>) dicuci bersih dan dipotong seragam terlebih dahulu. Mari lihat 3 masalah foto mentah di slide berikutnya!
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>21 / 57</span></div>
    </section>

    <!-- 22: MENGAPA IMAGE PROCESSING PENTING -->
    <section class="slide" data-title="Mengapa Foto Mentah Perlu Preprocessing?" data-notes="Alokasi waktu: 1.5 menit. Nah, setelah paham bahwa AI butuh bahan foto yang rapi, sekarang kita lihat 3 masalah utama pada foto mentah dari kamera HP yang harus kita bereskan.">
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
          <div class="card-body">Ada foto yang miring/terbalik dari kamera HP, terlalu gelap, berlatar ramai, atau filenya rusak. Semua ini wajib diaudit dulu!</div>
          <svg viewBox="0 0 220 75" style="width:100%; max-height:74px; margin-top:auto;">
            <rect x="16" y="16" width="52" height="42" rx="6" fill="#FFFFFF" stroke="#4285F4" stroke-width="2" transform="rotate(-8 42 37)"/>
            <text x="42" y="41" text-anchor="middle" font-size="9.5" font-weight="700" fill="#1A73E8">Miring</text>
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
          <div style="display:flex; flex-direction:column; gap:8px; margin-top:12px;">
            <div class="card surface" style="padding:10px 12px; gap:4px;">
              <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                <strong class="hl-green">Formula Skala 0–1</strong>
                <code style="font-size:12px;">x' = x / 255</code>
              </div>
              <div id="f-01" style="font-family:'Roboto Mono',monospace; font-size:12px; color:var(--muted);">128 / 255 = 0.502</div>
            </div>
            <div class="card surface" style="padding:10px 12px; gap:4px;">
              <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                <strong class="hl-blue">Formula Skala −1–1 (MobileNetV2)</strong>
                <code style="font-size:12px;">x' = (x / 127.5) − 1</code>
              </div>
              <div id="f-11" style="font-family:'Roboto Mono',monospace; font-size:12px; color:var(--muted);">(128 / 127.5) − 1 = 0.004</div>
            </div>
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
          <div style="background:#FFFFFF; border:1px solid #F4C7C3; border-radius:14px; padding:8px 12px; margin:6px 0; display:flex; flex-direction:column; align-items:center; gap:6px;">
            <img src="assets/P01/cat_dog_imbalance.jpg" alt="Ilustrasi Kucing 95 foto vs Anjing 5 foto" style="width:100%; max-height:112px; object-fit:contain; border-radius:8px;" />
            <div style="width:100%; display:flex; justify-content:space-around; font-size:12px; font-weight:700;">
              <span style="background:#FCE8E6; color:#C5221F; padding:2px 10px; border-radius:999px;">Kucing: 95 foto</span>
              <span style="background:#FEF7E0; color:#8A5700; padding:2px 10px; border-radius:999px;">Anjing: 5 foto</span>
            </div>
          </div>
          <svg viewBox="0 0 360 90" style="width:100%; max-height:82px; margin-top:auto;">
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
        <div class="img-box" style="flex-direction:column; gap:10px; padding:14px;">
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; width:100%;">
            <div style="display:flex; flex-direction:column; align-items:center; gap:4px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:10px; padding:6px;">
              <img src="assets/P01/sample_polos.jpg" alt="Contoh Gambar Kondisi Polos" style="height:82px; width:82px; object-fit:cover; border-radius:6px; border:1px solid #E0E0E0;" />
              <span style="font-size:11.5px; font-weight:700; color:#1A73E8;">Contoh Gambar Polos</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:4px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:10px; padding:6px;">
              <img src="assets/P01/sample_ramai.jpg" alt="Contoh Gambar Kondisi Ramai" style="height:82px; width:82px; object-fit:cover; border-radius:6px; border:1px solid #E0E0E0;" />
              <span style="font-size:11.5px; font-weight:700; color:#C5221F;">Contoh Gambar Ramai</span>
            </div>
          </div>
          <img src="assets/P01/07_histogram_brightness_contrast.png" alt="Histogram foto polos vs ramai" style="max-height:220px;" />
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
        <div class="img-box" style="flex-direction:column; gap:10px; padding:14px;">
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; width:100%;">
            <div style="display:flex; flex-direction:column; align-items:center; gap:4px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:10px; padding:6px;">
              <img src="assets/P01/sample_polos.jpg" alt="Contoh Foto Latar Polos" style="height:82px; width:82px; object-fit:cover; border-radius:6px; border:1px solid #E0E0E0;" />
              <span style="font-size:11.5px; font-weight:700; color:#1A73E8;">Contoh Latar Polos</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:4px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:10px; padding:6px;">
              <img src="assets/P01/sample_ramai.jpg" alt="Contoh Foto Latar Ramai" style="height:82px; width:82px; object-fit:cover; border-radius:6px; border:1px solid #E0E0E0;" />
              <span style="font-size:11.5px; font-weight:700; color:#C5221F;">Contoh Latar Ramai</span>
            </div>
          </div>
          <img src="assets/P01/07b_brightness_contrast_box.png" alt="Boxplot Brightness dan Contrast Polos vs Ramai" style="max-height:220px;" />
        </div>
        <div class="card" style="padding:18px 20px; gap:8px;">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">CONTOH DATA SAMPEL (119 FOTO VALID)</span>
          <div class="card-title" style="font-size:19px;">Temuan Nyata: Polos vs Ramai</div>
          <div class="card-body" style="font-size:14.5px; line-height:1.45;">
            <ul style="gap:6px;">
              <li><strong>Brightness (Rata-rata Intensitas):</strong><br />Polos: <strong>{polos['mean_brightness']:.2f}</strong> · Ramai: <strong>{ramai['mean_brightness']:.2f}</strong><br />Foto latar polos jauh lebih terang karena didominasi latar putih.</li>
              <li><strong>Contrast (Simpangan Baku):</strong><br />Polos: <strong>{polos['mean_contrast']:.2f}</strong> · Ramai: <strong>{ramai['mean_contrast']:.2f}</strong><br />Foto latar ramai lebih bervariasi gelap-terangnya.</li>
            </ul>
          </div>
          <div class="callout yellow" style="margin-top:auto; font-size:13.5px; padding:10px 12px;">Jika perbedaan ini terlalu ekstrem, AI bisa menebak hanya dari terangnya foto!</div>
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
          <div style="background:#F8F9FA; border:1px solid #DADCE0; border-radius:12px; padding:10px 12px; margin:6px 0; display:flex; flex-direction:column; gap:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:11.5px; font-weight:700; color:#1A73E8;">Animasi Kernel 3×3 Menggeser (Sliding Window)</span>
              <div style="display:flex; gap:6px; align-items:center;">
                <button id="edge-toggle" type="button" onclick="toggleEdgeAnim()" style="font-size:11px; padding:2px 8px; border-radius:999px; border:1px solid #DADCE0; background:#FFF; cursor:pointer; font-weight:600; color:#202124;">Pause</button>
                <button type="button" onclick="openEdgeModal()" style="font-size:11px; padding:2px 9px; border-radius:999px; border:1px solid #1A73E8; background:#E8F0FE; cursor:pointer; font-weight:700; color:#1A73E8;">⤢ Expand</button>
              </div>
            </div>
            <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
              <div style="display:flex; flex-direction:column; align-items:center; gap:3px;">
                <span style="font-size:10.5px; color:#5F6368; font-weight:600;">Gambar Input (5×5)</span>
                <div id="edge-in" style="position:relative; display:grid; grid-template-columns:repeat(5, 22px); grid-template-rows:repeat(5, 22px); gap:2px; background:#E8EAED; padding:2px; border-radius:6px;">
                  <div id="edge-win" style="position:absolute; width:72px; height:72px; border:2.5px solid #4285F4; background:rgba(66,133,244,0.16); border-radius:5px; pointer-events:none; transition:left 0.35s ease, top 0.35s ease; left:1px; top:1px;"></div>
                </div>
              </div>
              <div style="display:flex; flex-direction:column; align-items:center; gap:3px;">
                <span style="font-size:10.5px; color:#5F6368; font-weight:600;">Kernel 3×3</span>
                <div style="display:grid; grid-template-columns:repeat(3, 22px); gap:2px; background:#E8F0FE; padding:3px; border-radius:6px; border:1px solid #AECBFA; font-family:'Roboto Mono',monospace; font-size:9.5px; font-weight:700; text-align:center;">
                  <span style="background:#FFF; border-radius:3px; line-height:18px; color:#C5221F;">-1</span><span style="background:#FFF; border-radius:3px; line-height:18px; color:#5F6368;">0</span><span style="background:#FFF; border-radius:3px; line-height:18px; color:#137333;">+1</span>
                  <span style="background:#FFF; border-radius:3px; line-height:18px; color:#C5221F;">-2</span><span style="background:#FFF; border-radius:3px; line-height:18px; color:#5F6368;">0</span><span style="background:#FFF; border-radius:3px; line-height:18px; color:#137333;">+2</span>
                  <span style="background:#FFF; border-radius:3px; line-height:18px; color:#C5221F;">-1</span><span style="background:#FFF; border-radius:3px; line-height:18px; color:#5F6368;">0</span><span style="background:#FFF; border-radius:3px; line-height:18px; color:#137333;">+1</span>
                </div>
              </div>
              <div style="display:flex; flex-direction:column; align-items:center; gap:3px;">
                <span style="font-size:10.5px; color:#5F6368; font-weight:600;">Peta Edge (3×3)</span>
                <div id="edge-out" style="display:grid; grid-template-columns:repeat(3, 24px); grid-template-rows:repeat(3, 24px); gap:2px; background:#202124; padding:3px; border-radius:6px;"></div>
              </div>
            </div>
            <div id="edge-status" style="font-family:'Roboto Mono',monospace; font-size:11px; color:#202124; background:#FFF; border:1px solid #E8EAED; border-radius:6px; padding:4px 8px; text-align:center;">Posisi (0,0) → Selisih kiri-kanan = 920 → EDGE TERDETEKSI!</div>
          </div>
          <div class="callout" style="margin-top:auto;">Semakin banyak <em>edge</em> yang terdeteksi, semakin kompleks isi latar belakang foto tersebut.</div>
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
      <div style="flex:1; min-height:0; display:grid; grid-template-columns:190px 1fr; gap:12px;">
        <div class="card" style="padding:10px; gap:8px; justify-content:space-around; align-items:center;">
          <div style="display:flex; flex-direction:column; align-items:center; gap:4px; width:100%;">
            <span style="font-size:11.5px; font-weight:700; color:#1A73E8;">Foto Asli: Polos</span>
            <img src="assets/P01/orig_heksagon_polos.jpg" alt="Foto Asli Latar Polos" style="width:128px; height:128px; object-fit:cover; border-radius:8px; border:1px solid #DADCE0;" />
          </div>
          <div style="display:flex; flex-direction:column; align-items:center; gap:4px; width:100%;">
            <span style="font-size:11.5px; font-weight:700; color:#C5221F;">Foto Asli: Ramai</span>
            <img src="assets/P01/orig_heksagon_ramai.jpg" alt="Foto Asli Latar Ramai" style="width:128px; height:128px; object-fit:cover; border-radius:8px; border:1px solid #DADCE0;" />
          </div>
        </div>
        <div class="img-box" style="padding:10px;">
          <img src="assets/P01/08_canny_edge_density.png" alt="Deteksi tepi polos vs ramai" />
        </div>
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
        <div class="card surface" style="align-items:center; justify-content:center; padding:14px;">
          <svg id="qa4-vis" viewBox="0 0 320 278" style="width:100%; height:100%; max-height:370px;">
            <!-- Header Latihan -->
            <text x="160" y="13" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="9.5" font-weight="700" fill="#5F6368">SAAT AI BELAJAR (LATIHAN)</text>

            <!-- Kartu Kiri: Objek A (Bintang) di Meja Kayu Berantakan -->
            <rect x="8" y="20" width="144" height="106" rx="12" fill="#EFEBE9" stroke="#8D6E63" stroke-width="2"/>
            <!-- Tekstur meja & barang berantakan -->
            <line x1="16" y1="42" x2="144" y2="42" stroke="#D7CCC8" stroke-width="2"/>
            <line x1="16" y1="88" x2="144" y2="88" stroke="#D7CCC8" stroke-width="2"/>
            <rect x="18" y="28" width="22" height="28" rx="3" fill="#FFF" stroke="#BCAAA4" stroke-width="1.2" transform="rotate(-12 29 42)"/>
            <line x1="116" y1="30" x2="138" y2="52" stroke="#FBBC04" stroke-width="4" stroke-linecap="round"/>
            <circle cx="132" cy="76" r="8" fill="none" stroke="#A1887F" stroke-width="1.5"/>
            <!-- Objek A: Bintang Biru -->
            <polygon points="80,36 86,52 103,52 89,62 94,78 80,68 66,78 71,62 57,52 74,52" fill="#4285F4" stroke="#1A73E8" stroke-width="1.8"/>
            <text x="80" y="63" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">A</text>
            <rect x="16" y="102" width="128" height="18" rx="9" fill="#5D4037"/>
            <text x="80" y="114" text-anchor="middle" font-size="9.5" font-weight="700" fill="#FFFFFF">Objek A + Meja Berantakan</text>

            <!-- Kartu Kanan: Objek B (Kotak) di Tembok Putih Polos -->
            <rect x="168" y="20" width="144" height="106" rx="12" fill="#FFFFFF" stroke="#BDC1C6" stroke-width="2"/>
            <!-- Objek B: Kotak Hijau -->
            <rect x="218" y="38" width="44" height="44" rx="10" fill="#34A853" stroke="#137333" stroke-width="1.8"/>
            <text x="240" y="65" text-anchor="middle" font-size="13" font-weight="700" fill="#FFFFFF">B</text>
            <rect x="178" y="102" width="124" height="18" rx="9" fill="#5F6368"/>
            <text x="240" y="114" text-anchor="middle" font-size="9.5" font-weight="700" fill="#FFFFFF">Objek B + Tembok Putih</text>

            <!-- Panah ke Ujian -->
            <path d="M160 130 L160 142" stroke="#FBBC04" stroke-width="2.5" stroke-linecap="round"/>
            <rect x="34" y="143" width="252" height="28" rx="14" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
            <text x="160" y="161" text-anchor="middle" font-size="11" font-weight="700" fill="#202124">SAAT UJIAN: Objek A ditaruh di Tembok Putih!</text>

            <!-- Hasil Ujian: Tembok Putih berisi Objek A -->
            <g class="vis-q">
              <rect x="44" y="182" width="232" height="86" rx="14" fill="#FFFFFF" stroke="#4285F4" stroke-width="2.5" stroke-dasharray="6 4"/>
              <polygon points="94,196 99,210 114,210 102,219 107,233 94,224 81,233 86,219 74,210 89,210" fill="#4285F4" stroke="#1A73E8" stroke-width="1.5"/>
              <text x="94" y="220" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">A</text>
              <text x="94" y="252" text-anchor="middle" font-size="9" font-weight="700" fill="#5F6368">Latar Tembok Putih</text>
              <text x="198" y="218" text-anchor="middle" font-size="12" font-weight="700" fill="#1A73E8">Tebakan AI:</text>
              <text x="198" y="242" text-anchor="middle" font-size="20" font-weight="700" fill="#1A73E8">A atau B?</text>
            </g>
            <g class="vis-a">
              <rect x="44" y="182" width="232" height="86" rx="14" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.5"/>
              <rect x="54" y="192" width="76" height="66" rx="10" fill="#FFFFFF" stroke="#DADCE0" stroke-width="1.5"/>
              <polygon points="92,199 97,211 110,211 100,219 104,231 92,223 80,231 84,219 74,211 87,211" fill="#4285F4" stroke="#1A73E8" stroke-width="1.5"/>
              <text x="92" y="220" text-anchor="middle" font-size="9.5" font-weight="700" fill="#FFFFFF">A</text>
              <text x="92" y="248" text-anchor="middle" font-size="8.5" font-weight="700" fill="#5F6368">Tembok Putih</text>
              <text x="200" y="214" text-anchor="middle" font-size="12" font-weight="700" fill="#C5221F">AI Menebak: "B!"</text>
              <text x="200" y="234" text-anchor="middle" font-size="10" font-weight="600" fill="#202124">Salah! AI tertipu oleh</text>
              <text x="200" y="248" text-anchor="middle" font-size="10" font-weight="600" fill="#202124">latar tembok putihnya</text>
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
          <div style="display:flex; align-items:center; justify-content:space-around; gap:8px; background:#FFFFFF; border:1px solid #D2E3FC; border-radius:12px; padding:10px; margin:6px 0;">
            <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
              <img src="assets/P01/sample_polos.jpg" alt="Contoh Train Polos" style="width:74px; height:74px; object-fit:cover; border-radius:8px; border:2px solid #4285F4;" />
              <span style="font-size:11px; font-weight:700; color:#1A73E8;">Studio Polos</span>
            </div>
            <span style="font-size:20px; font-weight:700; color:#1A73E8;">&rarr;</span>
            <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
              <img src="assets/P01/sample_ramai.jpg" alt="Contoh Test Ramai" style="width:74px; height:74px; object-fit:cover; border-radius:8px; border:2px solid #EA4335;" />
              <span style="font-size:11px; font-weight:700; color:#C5221F;">Dunia Ramai (?)</span>
            </div>
          </div>
          <svg viewBox="0 0 360 76" style="width:100%; max-height:70px; margin-top:auto;">
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
          <div style="display:flex; align-items:center; justify-content:space-around; gap:6px; background:#FFFFFF; border:1px solid #CEEAD6; border-radius:12px; padding:10px; margin:6px 0;">
            <div style="display:flex; align-items:center; gap:6px;">
              <img src="assets/P01/sample_polos.jpg" alt="Polos" style="width:64px; height:64px; object-fit:cover; border-radius:8px; border:2px solid #34A853;" />
              <span style="font-size:16px; font-weight:700; color:#137333;">+</span>
              <img src="assets/P01/sample_ramai.jpg" alt="Ramai" style="width:64px; height:64px; object-fit:cover; border-radius:8px; border:2px solid #34A853;" />
            </div>
            <span style="font-size:20px; font-weight:700; color:#137333;">&rarr;</span>
            <div style="background:#E6F4EA; border:1.5px solid #34A853; border-radius:10px; padding:8px 10px; text-align:center;">
              <div style="font-size:12px; font-weight:700; color:#137333;">Fokus Bentuk</div>
              <div style="font-size:10.5px; color:#202124;">Bukan Latar!</div>
            </div>
          </div>
          <svg viewBox="0 0 360 76" style="width:100%; max-height:70px; margin-top:auto;">
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
            <div style="background:#F8F9FA; border:1px solid #DADCE0; border-radius:12px; padding:8px; margin-top:10px; display:flex; flex-direction:column; gap:6px;">
              <img src="assets/P01/edge_exceptions.jpg" alt="Ilustrasi baju motif garis di tembok polos vs latar bokeh" style="width:100%; max-height:132px; object-fit:contain; border-radius:8px;" />
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; text-align:center; font-size:11px; font-weight:700;">
                <span style="background:#FCE8E6; color:#C5221F; padding:3px 6px; border-radius:999px;">Motif Garis &rarr; High Edge</span>
                <span style="background:#E8F0FE; color:#1A73E8; padding:3px 6px; border-radius:999px;">Latar Bokeh &rarr; Low Edge</span>
              </div>
            </div>
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
          <svg viewBox="0 0 340 104" style="width:100%; max-height:104px; margin-top:auto;">
            <rect x="4" y="18" width="96" height="68" rx="10" fill="#FFFFFF" stroke="#4285F4" stroke-width="2"/>
            <text x="52" y="46" text-anchor="middle" font-size="11" font-weight="700" fill="#1A73E8">1. Statistik</text>
            <text x="52" y="64" text-anchor="middle" font-size="9.5" fill="#5F6368">Saring cepat</text>
            <path d="M104 52 L118 52" stroke="#5F6368" stroke-width="2.5"/><polygon points="116,47 125,52 116,57" fill="#5F6368"/>
            <rect x="126" y="18" width="96" height="68" rx="10" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
            <text x="174" y="46" text-anchor="middle" font-size="11" font-weight="700" fill="#8A5700">2. Cek Visual</text>
            <text x="174" y="64" text-anchor="middle" font-size="9.5" fill="#5F6368">Lihat sampel foto</text>
            <path d="M226 52 L240 52" stroke="#5F6368" stroke-width="2.5"/><polygon points="238,47 247,52 238,57" fill="#5F6368"/>
            <rect x="248" y="18" width="88" height="68" rx="10" fill="#34A853"/>
            <text x="292" y="46" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">3. Valid!</text>
            <text x="292" y="64" text-anchor="middle" font-size="9.5" fill="#E6F4EA">Data terjamin</text>
          </svg>
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
        <div class="img-box" style="display:grid; grid-template-columns:1fr 1fr; gap:14px; padding:16px; align-items:stretch;">
          <div style="display:flex; flex-direction:column; align-items:center; justify-content:space-between; gap:8px; background:#FCE8E6; border:2px solid #EA4335; border-radius:16px; padding:12px;">
            <span style="font-size:13px; font-weight:700; color:#C5221F; text-align:center; line-height:1.3;">Tanpa Koreksi EXIF<br />(Terputar 90°)</span>
            <div style="width:100%; max-width:200px; aspect-ratio:1/1; border-radius:12px; overflow:hidden; background:#FFFFFF; border:1px solid #F4C7C3; display:flex; align-items:center; justify-content:center;">
              <img src="assets/P01/exif_puppy.jpg" alt="Foto terputar 90 derajat tanpa koreksi EXIF" style="width:100%; height:100%; object-fit:cover; transform:rotate(-90deg);" />
            </div>
            <span style="font-size:11.5px; color:#C5221F; font-weight:600; text-align:center;">Program membaca piksel miring!</span>
          </div>
          <div style="display:flex; flex-direction:column; align-items:center; justify-content:space-between; gap:8px; background:#E6F4EA; border:2px solid #34A853; border-radius:16px; padding:12px;">
            <span style="font-size:13px; font-weight:700; color:#137333; text-align:center; line-height:1.3;">Dengan <code>exif_transpose()</code><br />(Tegak Benar)</span>
            <div style="width:100%; max-width:200px; aspect-ratio:1/1; border-radius:12px; overflow:hidden; background:#FFFFFF; border:1px solid #CEEAD6; display:flex; align-items:center; justify-content:center;">
              <img src="assets/P01/exif_puppy.jpg" alt="Foto tegak benar dengan exif_transpose" style="width:100%; height:100%; object-fit:cover;" />
            </div>
            <span style="font-size:11.5px; color:#137333; font-weight:600; text-align:center;">Orientasi tegak sesuai galeri HP</span>
          </div>
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
            <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; margin-top:10px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:12px; padding:10px;">
              <div style="display:flex; flex-direction:column; align-items:center; gap:4px; background:#E8F0FE; border:1.5px solid #4285F4; border-radius:10px; padding:6px 8px; flex:1;">
                <img src="assets/P01/exif_puppy.jpg" alt="foto1.jpg" style="width:64px; height:64px; object-fit:cover; border-radius:6px; border:1px solid #AECBFA;" />
                <span style="font-family:'Roboto Mono',monospace; font-size:10px; font-weight:700; color:#1A73E8;">foto1.jpg</span>
                <span style="font-size:9.5px; color:#5F6368;">Hash: 9f8a...</span>
              </div>
              <span style="font-size:16px; font-weight:700; color:#5F6368;">=</span>
              <div style="display:flex; flex-direction:column; align-items:center; gap:4px; background:#FCE8E6; border:1.5px solid #EA4335; border-radius:10px; padding:6px 8px; flex:1;">
                <img src="assets/P01/exif_puppy.jpg" alt="salinan_foto1.jpg" style="width:64px; height:64px; object-fit:cover; border-radius:6px; border:1px solid #F4C7C3;" />
                <span style="font-family:'Roboto Mono',monospace; font-size:10px; font-weight:700; color:#C5221F;">salinan_foto1.jpg</span>
                <span style="font-size:9.5px; color:#C5221F;">Hash: 9f8a... (Sama!)</span>
              </div>
              <span style="background:#EA4335; color:#FFFFFF; font-size:11px; font-weight:700; padding:6px 10px; border-radius:999px; white-space:nowrap;">Buang 1!</span>
            </div>
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
            <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; margin-top:10px; background:#FEF7E0; border:1.5px solid #FBBC04; border-radius:12px; padding:10px;">
              <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:6px; flex:1;">
                <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#FFF; border:1px solid #F9AB00; border-radius:8px; padding:4px;">
                  <img src="assets/P01/exif_puppy.jpg" alt="Burst 00:01.1" style="width:54px; height:54px; object-fit:cover; border-radius:5px; transform:rotate(-3deg);" />
                  <span style="font-family:'Roboto Mono',monospace; font-size:9.5px; font-weight:700; color:#202124;">00:01.1</span>
                </div>
                <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#FFF; border:1px solid #F9AB00; border-radius:8px; padding:4px;">
                  <img src="assets/P01/exif_puppy.jpg" alt="Burst 00:01.3" style="width:54px; height:54px; object-fit:cover; border-radius:5px;" />
                  <span style="font-family:'Roboto Mono',monospace; font-size:9.5px; font-weight:700; color:#202124;">00:01.3</span>
                </div>
                <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#FFF; border:1px solid #F9AB00; border-radius:8px; padding:4px;">
                  <img src="assets/P01/exif_puppy.jpg" alt="Burst 00:01.5" style="width:54px; height:54px; object-fit:cover; border-radius:5px; transform:rotate(3deg);" />
                  <span style="font-family:'Roboto Mono',monospace; font-size:9.5px; font-weight:700; color:#202124;">00:01.5</span>
                </div>
              </div>
              <span style="background:#202124; color:#FBBC04; font-family:'Roboto Mono',monospace; font-size:10.5px; font-weight:700; padding:7px 10px; border-radius:999px; white-space:nowrap;">1 id_sesi</span>
            </div>
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
          <div style="background:#FFFFFF; border:1px solid #F4C7C3; border-radius:12px; padding:10px; margin-top:auto; display:flex; flex-direction:column; gap:8px;">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:6px;">
              <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#E6F4EA; border:1.5px solid #34A853; border-radius:8px; padding:5px 7px;">
                <img src="assets/P01/exif_puppy.jpg" alt="foto_01" style="width:44px; height:44px; object-fit:cover; border-radius:4px;" />
                <span style="font-family:'Roboto Mono',monospace; font-size:9px; color:#137333; font-weight:700;">01.jpg ✓</span>
              </div>
              <span style="color:#5F6368; font-weight:700;">&rarr;</span>
              <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#E6F4EA; border:1.5px solid #34A853; border-radius:8px; padding:5px 7px;">
                <img src="assets/P01/exif_puppy.jpg" alt="foto_02" style="width:44px; height:44px; object-fit:cover; border-radius:4px;" />
                <span style="font-family:'Roboto Mono',monospace; font-size:9px; color:#137333; font-weight:700;">02.jpg ✓</span>
              </div>
              <span style="color:#EA4335; font-weight:700;">&rarr;</span>
              <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px; background:#FCE8E6; border:2px dashed #EA4335; border-radius:8px; padding:5px 8px;">
                <div style="width:44px; height:44px; display:flex; align-items:center; justify-content:center; background:#FFFFFF; border-radius:4px; color:#EA4335; font-size:22px; font-weight:700;">✕</div>
                <span style="font-family:'Roboto Mono',monospace; font-size:9px; color:#C5221F; font-weight:700;">03.jpg (0 KB)</span>
              </div>
              <span style="color:#EA4335; font-weight:700;">&rarr;</span>
              <div style="background:#EA4335; color:#FFFFFF; border-radius:10px; padding:10px 8px; text-align:center; font-size:11px; font-weight:700; line-height:1.25;">
                Program<br />Macet!
              </div>
            </div>
          </div>
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
          <svg viewBox="0 0 340 108" style="width:100%; max-height:108px; margin-top:auto;">
            <rect x="4" y="26" width="76" height="56" rx="10" fill="#F8F9FA" stroke="#DADCE0" stroke-width="1.5"/>
            <text x="42" y="50" text-anchor="middle" font-size="11.5" font-weight="700" fill="#202124">120 File</text>
            <text x="42" y="67" text-anchor="middle" font-size="9.5" fill="#5F6368">Dataset awal</text>

            <path d="M84 54 L104 54" stroke="#5F6368" stroke-width="2.5"/><polygon points="102,49 111,54 102,59" fill="#5F6368"/>

            <rect x="112" y="22" width="94" height="64" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
            <text x="159" y="50" text-anchor="middle" font-size="11" font-weight="700" fill="#1A73E8">Uji Buka</text>
            <text x="159" y="67" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="9.5" fill="#1A73E8">verify()</text>

            <path d="M210 42 L232 28" stroke="#34A853" stroke-width="2.5"/><polygon points="228,25 237,25 233,33" fill="#34A853"/>
            <path d="M210 66 L232 80" stroke="#EA4335" stroke-width="2.5"/><polygon points="233,75 237,83 228,83" fill="#EA4335"/>

            <rect x="238" y="8" width="98" height="38" rx="9" fill="#E6F4EA" stroke="#34A853" stroke-width="1.5"/>
            <text x="287" y="25" text-anchor="middle" font-size="10.5" font-weight="700" fill="#137333">119 Valid ✓</text>
            <text x="287" y="39" text-anchor="middle" font-size="9" fill="#137333">Lanjut ke AI</text>

            <rect x="238" y="62" width="98" height="38" rx="9" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.5"/>
            <text x="287" y="79" text-anchor="middle" font-size="10.5" font-weight="700" fill="#C5221F">1 Rusak ✕</text>
            <text x="287" y="93" text-anchor="middle" font-size="9" fill="#C5221F">Disisihkan</text>
          </svg>
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
      <div style="margin-top:14px; flex:1; min-height:0; display:grid; grid-template-columns:1.25fr 1fr; gap:14px;">
        <div class="card surface" style="justify-content:center; padding:16px 20px;">
          <div class="card-title" style="font-size:18px;">Daftar Temuan Khusus pada Sampel:</div>
          <div class="card-body" style="font-size:14.5px; line-height:1.45;">
            <ul style="gap:6px;">
              <li><strong>Corrupted file:</strong> <code>segitiga_ramai_12.jpg</code> — gagal uji buka, langsung dikecualikan agar tidak merusak hitungan rata-rata.</li>
              <li><strong>Duplicate images:</strong> <code>lingkaran_polos_01.jpg</code> &amp; <code>02.jpg</code> — memiliki <em>file hash</em> SHA-256 identik.</li>
              <li><strong>Foto EXIF orientation=6:</strong> <code>persegi_polos_01.jpg</code> &amp; <code>bintang_ramai_01.jpg</code> — otomatis diputar tegak saat dibuka.</li>
            </ul>
          </div>
        </div>
        <div class="card" style="padding:14px 16px; justify-content:center; gap:8px;">
          <div class="card-title" style="font-size:16px;">Cuplikan File Dataset Sampel</div>
          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;">
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:8px; padding:5px;">
              <img src="assets/P01/sample_lingkaran_01.jpg" alt="lingkaran_polos_01.jpg" style="width:52px; height:52px; object-fit:cover; border-radius:5px;" />
              <span style="font-family:'Roboto Mono',monospace; font-size:8.5px; color:#1A73E8; font-weight:700;">lingkaran (Dup)</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:8px; padding:5px;">
              <img src="assets/P01/sample_persegi_01.jpg" alt="persegi_polos_01.jpg" style="width:52px; height:52px; object-fit:cover; border-radius:5px;" />
              <span style="font-family:'Roboto Mono',monospace; font-size:8.5px; color:#8A5700; font-weight:700;">persegi (EXIF=6)</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:8px; padding:5px;">
              <img src="assets/P01/sample_bintang_01.jpg" alt="bintang_ramai_01.jpg" style="width:52px; height:52px; object-fit:cover; border-radius:5px;" />
              <span style="font-family:'Roboto Mono',monospace; font-size:8.5px; color:#8A5700; font-weight:700;">bintang (EXIF=6)</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#FCE8E6; border:1px dashed #EA4335; border-radius:8px; padding:5px;">
              <div style="width:52px; height:52px; display:flex; align-items:center; justify-content:center; background:#FFF; border-radius:5px; color:#EA4335; font-size:20px; font-weight:700;">✕</div>
              <span style="font-family:'Roboto Mono',monospace; font-size:8.5px; color:#C5221F; font-weight:700;">segitiga (Rusak)</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:8px; padding:5px;">
              <img src="assets/P01/orig_heksagon_polos.jpg" alt="heksagon_polos_01.jpg" style="width:52px; height:52px; object-fit:cover; border-radius:5px;" />
              <span style="font-family:'Roboto Mono',monospace; font-size:8.5px; color:#137333; font-weight:700;">heksagon (Valid)</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#F8F9FA; border:1px solid #DADCE0; border-radius:8px; padding:5px;">
              <img src="assets/P01/orig_heksagon_ramai.jpg" alt="heksagon_ramai_01.jpg" style="width:52px; height:52px; object-fit:cover; border-radius:5px;" />
              <span style="font-family:'Roboto Mono',monospace; font-size:8.5px; color:#137333; font-weight:700;">ramai (Valid)</span>
            </div>
          </div>
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
    <section class="slide" data-title="6 Langkah Praktik Terpandu (50 Menit)" data-notes="Alokasi waktu: 38.5 menit (selama sesi praktik). Keenam langkah ini sama persis dengan urutan sel di Notebook Hands-on P01, merangkum Bab 1 sampai Bab 4 secara berurutan.">
      <div class="kicker">HANDS-ON · 50 MENIT · SINKRON DENGAN NOTEBOOK</div>
      <h2>6 Langkah <span class="hl-blue">Praktik di Notebook</span> (Sesuai Bab 1–4)</h2>
      <div class="step-list">
        <div class="step-item"><div class="step-num">01</div><div><div class="step-title">Membaca Gambar &amp; Mengintip Matriks Pixel (Bab 1)</div><div class="step-desc">Membuka 1 foto sampel, melihat dimensi <code>(Tinggi, Lebar, 3)</code>, dan melakukan zoom-in <code>8×8</code> pixel untuk melihat angka <code>0–255</code>.</div></div></div>
        <div class="step-item"><div class="step-num red">02</div><div><div class="step-title">Memisahkan RGB Channels &amp; Mengubah ke Grayscale (Bab 1)</div><div class="step-desc">Memisahkan 3 lapisan warna (Red, Green, Blue) dan mengubahnya menjadi 1 channel <em>Grayscale</em>.</div></div></div>
        <div class="step-item"><div class="step-num yellow">03</div><div><div class="step-title">Image Processing: Resize Letterbox &amp; Normalization (Bab 2)</div><div class="step-desc">Menyeragamkan ukuran ke <code>224×224</code> tanpa gepeng (<em>letterbox padding</em>) dan mengubah skala <code>uint8 (0–255)</code> ke <code>float32 (0.0–1.0)</code>.</div></div></div>
        <div class="step-item"><div class="step-num green">04</div><div><div class="step-title">Mengatasi 3 Jebakan Kamera HP (Bab 4)</div><div class="step-desc">Memutar foto otomatis sesuai catatan <em>EXIF</em>, menyaring <em>corrupted file</em> dengan <code>verify()</code>, dan mendeteksi <em>duplicate</em> dengan <code>SHA-256</code>.</div></div></div>
        <div class="step-item"><div class="step-num">05</div><div><div class="step-title">EDA Kesehatan Dataset: Polos vs Ramai (Bab 3)</div><div class="step-desc">Menghitung keseimbangan jumlah foto (<em>class balance</em>), rata-rata <em>brightness</em>, <em>contrast</em>, <em>histogram</em>, serta <em>edge density</em> (Canny).</div></div></div>
        <div class="step-item"><div class="step-num red">06</div><div><div class="step-title">Menyimpan Ringkasan Audit Data &amp; Grafik</div><div class="step-desc">Menyimpan tabel hasil audit (CSV) dan grafik perbandingan kondisi <strong>polos vs ramai</strong> ke folder <code>results/</code>.</div></div></div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>47 / 57</span></div>
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
          <div style="background:#F8F9FA; border:1px solid #DADCE0; border-radius:12px; padding:10px; margin-top:auto; display:flex; align-items:center; justify-content:space-between; gap:8px;">
            <div style="display:flex; flex-direction:column; align-items:center; gap:3px; background:#E8F0FE; border:1.5px solid #4285F4; border-radius:8px; padding:6px 8px;">
              <span style="font-family:'Roboto Mono',monospace; font-size:10px; font-weight:700; color:#1A73E8;">1. verify()</span>
              <span style="font-size:9.5px; color:#137333; font-weight:700;">Utuh ✓ / Rusak ✕</span>
            </div>
            <span style="font-weight:700; color:#5F6368;">&rarr;</span>
            <div style="display:flex; align-items:center; gap:6px; background:#FFFFFF; border:1px solid #DADCE0; border-radius:8px; padding:5px 8px;">
              <img src="assets/P01/exif_puppy.jpg" alt="Miring" style="width:42px; height:42px; object-fit:cover; border-radius:5px; transform:rotate(-90deg); border:1px solid #EA4335;" />
              <span style="font-size:12px; font-weight:700; color:#34A853;">&rarr;</span>
              <img src="assets/P01/exif_puppy.jpg" alt="Tegak" style="width:42px; height:42px; object-fit:cover; border-radius:5px; border:1.5px solid #34A853;" />
            </div>
            <span style="background:#E6F4EA; color:#137333; font-size:10px; font-weight:700; padding:5px 8px; border-radius:8px; text-align:center;">2. Tegak<br />+ RGB</span>
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
          <div style="background:#F8F9FA; border:1px solid #DADCE0; border-radius:12px; padding:10px; margin-top:auto; display:flex; flex-direction:column; gap:6px;">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
              <div style="display:flex; align-items:center; gap:6px; background:#FFFFFF; border:1px solid #DADCE0; border-radius:8px; padding:4px 8px; flex:1;">
                <img src="assets/P01/exif_puppy.jpg" alt="foto_a.jpg" style="width:36px; height:36px; object-fit:cover; border-radius:4px;" />
                <span style="font-family:'Roboto Mono',monospace; font-size:10px; font-weight:700; color:#202124;">foto_a.jpg</span>
              </div>
              <span style="font-size:12px; font-weight:700; color:#5F6368;">&rarr;</span>
              <span style="font-family:'Roboto Mono',monospace; font-size:10px; font-weight:700; background:#FEF7E0; color:#8A5700; border:1px solid #FBBC04; padding:5px 8px; border-radius:8px;">SHA-256: a3f9c2...</span>
            </div>
            <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
              <div style="display:flex; align-items:center; gap:6px; background:#FFFFFF; border:1px solid #DADCE0; border-radius:8px; padding:4px 8px; flex:1;">
                <img src="assets/P01/exif_puppy.jpg" alt="copy_b.jpg" style="width:36px; height:36px; object-fit:cover; border-radius:4px;" />
                <span style="font-family:'Roboto Mono',monospace; font-size:10px; font-weight:700; color:#202124;">copy_b.jpg</span>
              </div>
              <span style="font-size:12px; font-weight:700; color:#5F6368;">&rarr;</span>
              <span style="font-family:'Roboto Mono',monospace; font-size:10px; font-weight:700; background:#FCE8E6; color:#C5221F; border:1px solid #EA4335; padding:5px 8px; border-radius:8px;">SHA-256: a3f9c2...</span>
            </div>
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
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:4px 0;">
            <div style="display:flex; align-items:center; gap:8px; background:#FFFFFF; border:1.5px solid #4285F4; border-radius:10px; padding:7px;">
              <img src="assets/P01/sample_polos.jpg" alt="Sampel Polos" style="width:52px; height:52px; object-fit:cover; border-radius:6px;" />
              <div style="font-size:10.5px; line-height:1.3;">
                <strong style="color:#1A73E8;">Polos</strong><br />
                <span style="color:#5F6368;">Terang &amp; bersih<br />Edge: 0.0121</span>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; background:#FFFFFF; border:1.5px solid #EA4335; border-radius:10px; padding:7px;">
              <img src="assets/P01/sample_ramai.jpg" alt="Sampel Ramai" style="width:52px; height:52px; object-fit:cover; border-radius:6px;" />
              <div style="font-size:10.5px; line-height:1.3;">
                <strong style="color:#C5221F;">Ramai</strong><br />
                <span style="color:#5F6368;">Penuh corak<br />Edge: 0.0853</span>
              </div>
            </div>
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
      <h2>5 Istilah Dasar <span class="hl-blue">Gambar &amp; AI</span></h2>
      <table class="io-table" style="margin-top:8px;">
        <thead><tr><th style="width:26%;">Istilah</th><th>Penjelasan Bahasa Sehari-hari</th></tr></thead>
        <tbody>
          <tr><td><strong>Pixel</strong></td><td>Elemen kotak terkecil penyusun gambar digital; setiap <em>pixel</em> berisi nilai intensitas <code>0–255</code>.</td></tr>
          <tr><td><strong>RGB &amp; Grayscale</strong></td><td><strong>RGB:</strong> 3 channel warna dasar (Red, Green, Blue). <strong>Grayscale:</strong> 1 channel yang hanya mengukur gelap-terang.</td></tr>
          <tr><td><strong>Deep Learning (AI)</strong></td><td>Cabang AI yang belajar mengenali pola gambar (garis tepi &rarr; bentuk &rarr; objek) langsung dari banyak contoh foto.</td></tr>
          <tr><td><strong>Resolution</strong></td><td>Jumlah total <em>pixel</em> lebar × tinggi yang membentuk sebuah foto (misal diseragamkan ke <code>224 × 224</code>).</td></tr>
          <tr><td><strong>Aspect Ratio</strong></td><td>Perbandingan lebar dan tinggi foto yang harus dijaga agar objek tidak gepeng/terdistorsi saat di-<em>resize</em>.</td></tr>
        </tbody>
      </table>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>51 / 57</span></div>
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
              <rect x="16" y="14" width="288" height="114" rx="14" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.5"/>
              <text x="160" y="38" text-anchor="middle" font-size="12.5" font-weight="700" fill="#C5221F">BAHAYA: DATA LEAKAGE!</text>
              <rect x="28" y="50" width="112" height="44" rx="10" fill="#FFFFFF" stroke="#EA4335" stroke-width="1.5"/>
              <text x="84" y="70" text-anchor="middle" font-size="11" font-weight="700" fill="#202124">Train Set</text>
              <text x="84" y="86" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="9.5" fill="#1A73E8">foto1.jpg</text>
              <text x="160" y="76" text-anchor="middle" font-size="16" font-weight="700" fill="#EA4335">=</text>
              <rect x="180" y="50" width="112" height="44" rx="10" fill="#FFFFFF" stroke="#EA4335" stroke-width="1.5"/>
              <text x="236" y="70" text-anchor="middle" font-size="11" font-weight="700" fill="#202124">Test Set</text>
              <text x="236" y="86" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="9.5" fill="#C5221F">foto1.jpg (Sama!)</text>
              <text x="160" y="116" text-anchor="middle" font-size="10" font-weight="700" fill="#C5221F">Soal ujian sama persis dengan latihan!</text>

              <rect x="16" y="142" width="288" height="106" rx="14" fill="#202124"/>
              <text x="160" y="166" text-anchor="middle" font-size="12" font-weight="700" fill="#FBBC04">Akibatnya: Inflated Accuracy</text>
              <rect x="30" y="180" width="120" height="52" rx="10" fill="#292A2D" stroke="#FBBC04" stroke-width="1.5"/>
              <text x="90" y="200" text-anchor="middle" font-size="10.5" font-weight="700" fill="#FFFFFF">Nilai Test Set</text>
              <text x="90" y="220" text-anchor="middle" font-size="12.5" font-weight="700" fill="#FBBC04">~100% (Palsu)</text>
              <rect x="170" y="180" width="120" height="52" rx="10" fill="#292A2D" stroke="#EA4335" stroke-width="1.5"/>
              <text x="230" y="200" text-anchor="middle" font-size="10.5" font-weight="700" fill="#FFFFFF">Foto Baru Asli</text>
              <text x="230" y="220" text-anchor="middle" font-size="12.5" font-weight="700" fill="#F28B82">Anjlok / Gagal!</text>
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
          <div class="card-body" style="color:#BDC1C6;">Mata kita melihat bentuk, sedangkan komputer hanya membaca matriks pixel berisi nilai <code>0–255</code> dan 3 <em>RGB channels</em>.</div>
        </div>
        <div class="card" style="background:#292A2D; border-color:#3C4043;">
          <div class="card-top-bar bar-green"></div>
          <div class="big-num" style="color:var(--green);">02</div>
          <div class="card-title" style="color:white;">AI Butuh Bahan yang Rapi</div>
          <div class="card-body" style="color:#BDC1C6;">AI belajar mengenali pola dari contoh foto. <em>Image Processing</em> memastikan ukuran foto seragam (<code>224×224</code>) tanpa gepeng dan skalanya stabil (<code>0–1</code>).</div>
        </div>
        <div class="card" style="background:#292A2D; border-color:#3C4043;">
          <div class="card-top-bar bar-red"></div>
          <div class="big-num" style="color:var(--red);">03</div>
          <div class="card-title" style="color:white;">Exploratory Data Analysis (EDA)</div>
          <div class="card-body" style="color:#BDC1C6;">Mengaudit keseimbangan kelas, pencahayaan, kondisi <strong>polos vs ramai</strong>, serta menyaring jebakan EXIF, <em>corrupted files</em>, dan <em>duplicates</em>.</div>
        </div>
      </div>
      <div class="slide-footer"><span>Memahami Gambar di Komputer &amp; Image Processing</span><span>56 / 57</span></div>
    </section>

    <!-- 54: PENUTUP -->
    <section class="slide" data-title="Closing &amp; Key Quote" data-notes="Alokasi waktu: 1 menit. Tutup sesi dengan kutipan penutup dan apresiasi atas antusiasme peserta hari ini." style="background: repeating-linear-gradient(-35deg, rgba(66,133,244,0.025) 0px, rgba(66,133,244,0.025) 1px, transparent 1px, transparent 28px), #FFFFFF; justify-content: space-between;">
      <div style="display:flex; align-items:center; justify-content:space-between;">
        <span style="font-family:var(--font-title); font-size:12px; font-weight:700; letter-spacing:1.8px; color:#80868B;">CLOSING</span>
        <div style="display:flex; gap:6px;">
          <span style="width:9px; height:9px; border-radius:50%; background:#4285F4;"></span>
          <span style="width:9px; height:9px; border-radius:50%; background:#EA4335;"></span>
          <span style="width:9px; height:9px; border-radius:50%; background:#FBBC04;"></span>
          <span style="width:9px; height:9px; border-radius:50%; background:#34A853;"></span>
        </div>
      </div>

      <div style="margin:auto 0; display:flex; flex-direction:column; align-items:center; text-align:center; gap:20px; padding:0 44px;">
        <div style="font-family:var(--font-title); font-size:46px; font-weight:700; line-height:0.6; color:#D2E3FC; user-select:none;">&rdquo;</div>
        <h1 style="font-family:var(--font-title); font-size:clamp(24px,2.55vw,33px); font-weight:700; line-height:1.38; color:#202124; max-width:860px; margin:0;">
          <span style="color:#EA4335;">Data yang bersih</span> melahirkan model yang cerdas, sedangkan <span style="color:#1A73E8;">Image Processing &amp; EDA</span> memastikan AI belajar dari pola yang benar.
        </h1>
      </div>

      <div class="slide-footer"><span>P01 - Understanding Images, Image Processing &amp; EDA</span><span>57 / 57</span></div>
    </section>

  </div>

  <div id="controls">
    <button class="ctrl-btn" onclick="prevSlide()">← Prev</button>
    <span id="counter" style="display:inline-flex; align-items:center; gap:5px;">
      <input id="page-jump" type="number" min="1" max="57" value="1" title="Ketik nomor slide (1-57) lalu tekan Enter" onchange="jumpToSlide(this.value)" onkeydown="if(event.key==='Enter'){{jumpToSlide(this.value); this.blur();}}" />
      <span>/ 57</span>
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
      <h3 style="font-family:var(--font-title);">Daftar Semua Slide (57 Slides)</h3>
      <button class="ctrl-btn" onclick="toggleGrid()">Tutup (Esc)</button>
    </div>
    <div id="grid-cards" class="grid-cards"></div>
  </div>

  <div id="edge-modal" style="display:none; position:fixed; inset:0; z-index:200; background:rgba(32,33,36,0.76); backdrop-filter:blur(4px); align-items:center; justify-content:center; padding:20px;" onclick="if(event.target===this) closeEdgeModal()">
    <div style="background:#FFFFFF; border-radius:20px; max-width:960px; width:100%; padding:22px 26px; box-shadow:0 20px 50px rgba(0,0,0,0.35); display:flex; flex-direction:column; gap:14px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="font-family:'Roboto Mono',monospace; font-size:11px; color:#1A73E8; font-weight:700; text-transform:uppercase;">Eksplorasi Pixel Range Lebih Luas</div>
          <h3 style="margin:2px 0 0; font-family:var(--font-title); font-size:20px; color:#202124;">Simulasi Kernel 3×3 Edge Detection</h3>
        </div>
        <button type="button" onclick="closeEdgeModal()" style="padding:6px 14px; border-radius:999px; border:1px solid #DADCE0; background:#F8F9FA; cursor:pointer; font-weight:700; color:#202124;">✕ Tutup</button>
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; justify-content:space-between; background:#F8F9FA; padding:10px 14px; border-radius:12px; border:1px solid #E8EAED;">
        <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
          <span style="font-size:12px; font-weight:700; color:#5F6368;">Ukuran Grid:</span>
          <button type="button" class="edge-sz-btn" data-sz="5" onclick="setEdgeModalSize(5)" style="font-size:12px; padding:4px 10px; border-radius:999px; border:1px solid #DADCE0; background:#FFF; cursor:pointer; font-weight:600;">5×5</button>
          <button type="button" class="edge-sz-btn" data-sz="8" onclick="setEdgeModalSize(8)" style="font-size:12px; padding:4px 10px; border-radius:999px; border:1px solid #DADCE0; background:#FFF; cursor:pointer; font-weight:600;">8×8</button>
          <button type="button" class="edge-sz-btn" data-sz="10" onclick="setEdgeModalSize(10)" style="font-size:12px; padding:4px 10px; border-radius:999px; border:1px solid #1A73E8; background:#E8F0FE; color:#1A73E8; cursor:pointer; font-weight:700;">10×10</button>
          <button type="button" class="edge-sz-btn" data-sz="12" onclick="setEdgeModalSize(12)" style="font-size:12px; padding:4px 10px; border-radius:999px; border:1px solid #DADCE0; background:#FFF; cursor:pointer; font-weight:600;">12×12</button>
        </div>
        <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
          <span style="font-size:12px; font-weight:700; color:#5F6368;">Pola:</span>
          <button type="button" class="edge-pat-btn" data-pat="vertical" onclick="setEdgeModalPreset('vertical')" style="font-size:12px; padding:4px 10px; border-radius:999px; border:1px solid #DADCE0; background:#FFF; cursor:pointer; font-weight:600;">Garis Tegak</button>
          <button type="button" class="edge-pat-btn" data-pat="box" onclick="setEdgeModalPreset('box')" style="font-size:12px; padding:4px 10px; border-radius:999px; border:1px solid #1A73E8; background:#E8F0FE; color:#1A73E8; cursor:pointer; font-weight:700;">Kotak</button>
          <button type="button" class="edge-pat-btn" data-pat="diag" onclick="setEdgeModalPreset('diag')" style="font-size:12px; padding:4px 10px; border-radius:999px; border:1px solid #DADCE0; background:#FFF; cursor:pointer; font-weight:600;">Diagonal</button>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
          <button id="edge-m-play" type="button" onclick="toggleEdgeModalPlay()" style="font-size:12px; padding:4px 12px; border-radius:999px; border:none; background:#1A73E8; color:#FFF; cursor:pointer; font-weight:700;">Pause</button>
          <button id="edge-m-spd" type="button" onclick="toggleEdgeModalSpeed()" style="font-size:12px; padding:4px 10px; border-radius:999px; border:1px solid #DADCE0; background:#FFF; cursor:pointer; font-weight:600;">Speed: 2×</button>
        </div>
      </div>
      <div style="display:flex; align-items:center; justify-content:space-around; gap:16px; flex-wrap:wrap;">
        <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
          <span id="edge-m-in-lbl" style="font-size:12.5px; font-weight:700; color:#202124;">Gambar Input (10×10) · <span style="color:#1A73E8; font-weight:500;">klik pixel untuk ubah</span></span>
          <div id="edge-m-in" style="position:relative; display:grid; gap:2px; background:#E8EAED; padding:3px; border-radius:8px; user-select:none;">
            <div id="edge-m-win" style="position:absolute; border:2.5px solid #4285F4; background:rgba(66,133,244,0.18); border-radius:5px; pointer-events:none; transition:left 0.14s ease, top 0.14s ease;"></div>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
          <span style="font-size:12.5px; font-weight:700; color:#202124;">Sobel Kernel (3×3)</span>
          <div style="display:grid; grid-template-columns:repeat(3, 30px); gap:3px; background:#E8F0FE; padding:5px; border-radius:8px; border:1px solid #AECBFA; font-family:'Roboto Mono',monospace; font-size:11px; font-weight:700; text-align:center;">
            <span style="background:#FFF; border-radius:4px; line-height:24px; color:#C5221F;">-1</span><span style="background:#FFF; border-radius:4px; line-height:24px; color:#5F6368;">0</span><span style="background:#FFF; border-radius:4px; line-height:24px; color:#137333;">+1</span>
            <span style="background:#FFF; border-radius:4px; line-height:24px; color:#C5221F;">-2</span><span style="background:#FFF; border-radius:4px; line-height:24px; color:#5F6368;">0</span><span style="background:#FFF; border-radius:4px; line-height:24px; color:#137333;">+2</span>
            <span style="background:#FFF; border-radius:4px; line-height:24px; color:#C5221F;">-1</span><span style="background:#FFF; border-radius:4px; line-height:24px; color:#5F6368;">0</span><span style="background:#FFF; border-radius:4px; line-height:24px; color:#137333;">+1</span>
          </div>
          <span style="font-size:11px; color:#5F6368; text-align:center;">Deteksi tepi<br />kiri–kanan &amp; atas–bawah</span>
        </div>
        <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
          <span id="edge-m-out-lbl" style="font-size:12.5px; font-weight:700; color:#202124;">Peta Edge Output (8×8)</span>
          <div id="edge-m-out" style="display:grid; gap:2px; background:#202124; padding:4px; border-radius:8px;"></div>
        </div>
      </div>
      <div id="edge-m-status" style="font-family:'Roboto Mono',monospace; font-size:12px; color:#202124; background:#F8F9FA; border:1px solid #E8EAED; border-radius:8px; padding:8px 12px; text-align:center;">Posisi (0,0)</div>
    </div>
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
      const s01 = (v / 255).toFixed(3);
      const s11 = (v / 127.5 - 1).toFixed(3);
      document.getElementById('n-u8').textContent = v;
      document.getElementById('n-01').textContent = s01;
      document.getElementById('n-11').textContent = s11;
      document.getElementById('f-01').textContent = `${{v}} / 255 = ${{s01}}`;
      document.getElementById('f-11').textContent = `(${{v}} / 127.5) − 1 = ${{s11}}`;
    }}

    // Animated 3x3 Edge Detection Kernel on Slide 31
    (function initEdgeAnim() {{
      const inEl = document.getElementById('edge-in');
      const outEl = document.getElementById('edge-out');
      const winEl = document.getElementById('edge-win');
      const statusEl = document.getElementById('edge-status');
      if (!inEl || !outEl || !winEl) return;

      const img = [
        [10, 10, 240, 240, 240],
        [10, 10, 240, 240, 240],
        [10, 10, 240, 240, 240],
        [10, 10, 240, 240, 240],
        [10, 10, 240, 240, 240]
      ];
      const kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]];

      for (let r = 0; r < 5; r++) {{
        for (let c = 0; c < 5; c++) {{
          const cell = document.createElement('div');
          const v = img[r][c];
          cell.textContent = v;
          cell.style.cssText = `width:22px;height:22px;display:flex;align-items:center;justify-content:center;font-family:'Roboto Mono',monospace;font-size:8.5px;font-weight:700;border-radius:3px;background:${{v < 100 ? '#3C4043' : '#FFFFFF'}};color:${{v < 100 ? '#E8EAED' : '#202124'}};`;
          inEl.appendChild(cell);
        }}
      }}

      const outCells = [];
      for (let r = 0; r < 3; r++) {{
        for (let c = 0; c < 3; c++) {{
          const cell = document.createElement('div');
          cell.style.cssText = 'width:24px;height:24px;border-radius:3px;background:#303134;border:1px solid #5F6368;transition:all 0.25s ease;display:flex;align-items:center;justify-content:center;font-family:"Roboto Mono",monospace;font-size:8px;font-weight:700;';
          outEl.appendChild(cell);
          outCells.push(cell);
        }}
      }}

      let step = 0;
      let playing = true;

      function renderStep() {{
        const r = Math.floor(step / 3);
        const c = step % 3;
        winEl.style.left = (1 + c * 24) + 'px';
        winEl.style.top = (1 + r * 24) + 'px';

        let sum = 0;
        for (let kr = 0; kr < 3; kr++) {{
          for (let kc = 0; kc < 3; kc++) {{
            sum += img[r + kr][c + kc] * kernel[kr][kc];
          }}
        }}
        const mag = Math.abs(sum);
        const isEdge = mag > 100;

        if (step === 0) {{
          outCells.forEach((oc) => {{
            oc.style.background = '#303134';
            oc.style.borderColor = '#5F6368';
            oc.textContent = '';
          }});
        }}
        const cur = outCells[step];
        cur.style.background = isEdge ? '#FFFFFF' : '#202124';
        cur.style.borderColor = '#4285F4';
        cur.style.color = isEdge ? '#202124' : '#9AA0A6';
        cur.textContent = isEdge ? '1' : '0';

        if (statusEl) {{
          statusEl.innerHTML = isEdge
            ? `Posisi (${{r}},${{c}}) &rarr; Skor=${{mag}} &rarr; <strong style="color:#137333;">EDGE TERDETEKSI (Putih)</strong>`
            : `Posisi (${{r}},${{c}}) &rarr; Skor=${{mag}} &rarr; <span style="color:#5F6368;">Area rata (Hitam)</span>`;
        }}
      }}

      renderStep();
      setInterval(() => {{
        if (!playing) return;
        step = (step + 1) % 9;
        renderStep();
      }}, 850);

      window.toggleEdgeAnim = function() {{
        playing = !playing;
        const btn = document.getElementById('edge-toggle');
        if (btn) btn.textContent = playing ? 'Pause' : 'Play';
      }};
    }})();

    // Expanded Edge Detection Modal (5x5 up to 12x12)
    (function initEdgeModal() {{
      let mSize = 10;
      let mPat = 'box';
      let mGrid = [];
      let mStep = 0;
      let mPlay = true;
      let mFast = true;
      let mTimer = null;
      let outCells = [];

      function buildPattern(N, pat) {{
        const g = [];
        for (let r = 0; r < N; r++) {{
          const row = [];
          for (let c = 0; c < N; c++) {{
            if (pat === 'vertical') {{
              row.push(c < Math.floor(N / 2) ? 10 : 240);
            }} else if (pat === 'diag') {{
              row.push(c >= r ? 240 : 10);
            }} else {{
              const pad = N <= 5 ? 1 : N <= 8 ? 2 : 3;
              const inside = r >= pad && r < N - pad && c >= pad && c < N - pad;
              row.push(inside ? 240 : 10);
            }}
          }}
          g.push(row);
        }}
        return g;
      }}

      function rebuildModalDOM() {{
        const inEl = document.getElementById('edge-m-in');
        const outEl = document.getElementById('edge-m-out');
        const winEl = document.getElementById('edge-m-win');
        if (!inEl || !outEl || !winEl) return;

        const cellPx = mSize <= 5 ? 42 : mSize <= 8 ? 32 : mSize <= 10 ? 27 : 23;
        const gap = 2;
        const stride = cellPx + gap;
        const outN = mSize - 2;

        document.getElementById('edge-m-in-lbl').innerHTML = `Gambar Input (${{mSize}}×${{mSize}}) · <span style="color:#1A73E8; font-weight:500;">klik pixel untuk ubah</span>`;
        document.getElementById('edge-m-out-lbl').textContent = `Peta Edge Output (${{outN}}×${{outN}})`;

        inEl.querySelectorAll('.em-cell').forEach((n) => n.remove());
        outEl.innerHTML = '';
        outCells = [];

        inEl.style.gridTemplateColumns = `repeat(${{mSize}}, ${{cellPx}}px)`;
        inEl.style.gridTemplateRows = `repeat(${{mSize}}, ${{cellPx}}px)`;
        winEl.style.width = (cellPx * 3 + gap * 2 + 4) + 'px';
        winEl.style.height = (cellPx * 3 + gap * 2 + 4) + 'px';

        for (let r = 0; r < mSize; r++) {{
          for (let c = 0; c < mSize; c++) {{
            const cell = document.createElement('div');
            cell.className = 'em-cell';
            const v = mGrid[r][c];
            cell.textContent = mSize <= 10 ? v : '';
            cell.title = `(${{r}},${{c}}) = ${{v}} (klik untuk ubah)`;
            cell.style.cssText = `width:${{cellPx}}px;height:${{cellPx}}px;display:flex;align-items:center;justify-content:center;font-family:'Roboto Mono',monospace;font-size:${{mSize <= 8 ? 10 : 8.5}}px;font-weight:700;border-radius:4px;cursor:pointer;background:${{v < 100 ? '#3C4043' : '#FFFFFF'}};color:${{v < 100 ? '#E8EAED' : '#202124'}};`;
            cell.onclick = () => {{
              mGrid[r][c] = mGrid[r][c] < 100 ? 240 : 10;
              rebuildModalDOM();
              renderModalStep();
            }};
            inEl.appendChild(cell);
          }}
        }}

        const outPx = Math.min(34, Math.floor((cellPx * mSize) / outN));
        outEl.style.gridTemplateColumns = `repeat(${{outN}}, ${{outPx}}px)`;
        outEl.style.gridTemplateRows = `repeat(${{outN}}, ${{outPx}}px)`;
        for (let r = 0; r < outN; r++) {{
          for (let c = 0; c < outN; c++) {{
            const oc = document.createElement('div');
            oc.style.cssText = `width:${{outPx}}px;height:${{outPx}}px;border-radius:4px;background:#303134;border:1px solid #5F6368;display:flex;align-items:center;justify-content:center;font-family:'Roboto Mono',monospace;font-size:${{outN <= 6 ? 10 : 8.5}}px;font-weight:700;transition:all 0.15s ease;`;
            outEl.appendChild(oc);
            outCells.push(oc);
          }}
        }}
        mStep = 0;
        renderModalStep();
      }}

      function renderModalStep() {{
        const winEl = document.getElementById('edge-m-win');
        const statusEl = document.getElementById('edge-m-status');
        if (!winEl || outCells.length === 0) return;

        const outN = mSize - 2;
        const cellPx = mSize <= 5 ? 42 : mSize <= 8 ? 32 : mSize <= 10 ? 27 : 23;
        const stride = cellPx + 2;
        const r = Math.floor(mStep / outN);
        const c = mStep % outN;

        winEl.style.left = (1 + c * stride) + 'px';
        winEl.style.top = (1 + r * stride) + 'px';

        const kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]];
        const ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]];
        let gx = 0, gy = 0;
        for (let kr = 0; kr < 3; kr++) {{
          for (let kc = 0; kc < 3; kc++) {{
            const val = mGrid[r + kr][c + kc];
            gx += val * kx[kr][kc];
            gy += val * ky[kr][kc];
          }}
        }}
        const mag = Math.round(Math.hypot(gx, gy));
        const isEdge = mag > 150;

        if (mStep === 0) {{
          outCells.forEach((oc) => {{
            oc.style.background = '#303134';
            oc.style.borderColor = '#5F6368';
            oc.textContent = '';
          }});
        }}
        const cur = outCells[mStep];
        cur.style.background = isEdge ? '#FFFFFF' : '#202124';
        cur.style.borderColor = '#4285F4';
        cur.style.color = isEdge ? '#202124' : '#9AA0A6';
        cur.textContent = isEdge ? '1' : '0';

        if (statusEl) {{
          statusEl.innerHTML = isEdge
            ? `Posisi (${{r}},${{c}}) &rarr; |Gx|=${{Math.abs(gx)}}, |Gy|=${{Math.abs(gy)}} &rarr; Skor=${{mag}} &rarr; <strong style="color:#137333;">EDGE TERDETEKSI (Putih)</strong>`
            : `Posisi (${{r}},${{c}}) &rarr; |Gx|=${{Math.abs(gx)}}, |Gy|=${{Math.abs(gy)}} &rarr; Skor=${{mag}} &rarr; <span style="color:#5F6368;">Area rata (Hitam)</span>`;
        }}
      }}

      function startTimer() {{
        if (mTimer) clearInterval(mTimer);
        mTimer = setInterval(() => {{
          const modal = document.getElementById('edge-modal');
          if (!modal || modal.style.display === 'none' || !mPlay) return;
          const total = (mSize - 2) * (mSize - 2);
          mStep = (mStep + 1) % total;
          renderModalStep();
        }}, mFast ? 220 : 650);
      }}

      window.openEdgeModal = function() {{
        const modal = document.getElementById('edge-modal');
        if (!modal) return;
        modal.style.display = 'flex';
        mGrid = buildPattern(mSize, mPat);
        rebuildModalDOM();
        startTimer();
      }};
      window.closeEdgeModal = function() {{
        const modal = document.getElementById('edge-modal');
        if (modal) modal.style.display = 'none';
        if (mTimer) {{ clearInterval(mTimer); mTimer = null; }}
      }};
      window.setEdgeModalSize = function(sz) {{
        mSize = sz;
        document.querySelectorAll('.edge-sz-btn').forEach((b) => {{
          const active = Number(b.dataset.sz) === sz;
          b.style.borderColor = active ? '#1A73E8' : '#DADCE0';
          b.style.background = active ? '#E8F0FE' : '#FFF';
          b.style.color = active ? '#1A73E8' : '#202124';
        }});
        mGrid = buildPattern(mSize, mPat);
        rebuildModalDOM();
      }};
      window.setEdgeModalPreset = function(pat) {{
        mPat = pat;
        document.querySelectorAll('.edge-pat-btn').forEach((b) => {{
          const active = b.dataset.pat === pat;
          b.style.borderColor = active ? '#1A73E8' : '#DADCE0';
          b.style.background = active ? '#E8F0FE' : '#FFF';
          b.style.color = active ? '#1A73E8' : '#202124';
        }});
        mGrid = buildPattern(mSize, mPat);
        rebuildModalDOM();
      }};
      window.toggleEdgeModalPlay = function() {{
        mPlay = !mPlay;
        document.getElementById('edge-m-play').textContent = mPlay ? 'Pause' : 'Play';
      }};
      window.toggleEdgeModalSpeed = function() {{
        mFast = !mFast;
        document.getElementById('edge-m-spd').textContent = mFast ? 'Speed: 2×' : 'Speed: 1×';
        startTimer();
      }};
    }})();

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

    // Slide 19: AI Fundamental 1/3 Interactive Tabs
    function setAi1Tab(tab) {{
      document.querySelectorAll('#ai1-tabs button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.tab !== tab);
      }});
      ['rule', 'ml', 'dl'].forEach((k) => {{
        const p = document.getElementById('ai1-panel-' + k);
        if (p) p.style.display = k === tab ? 'flex' : 'none';
      }});
    }}

    // Slide 20: AI Fundamental 2/3 Interactive Condition Simulator
    function setAi2Cond(cond) {{
      document.querySelectorAll('#ai2-btns button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.cond !== cond);
      }});
      const star = document.getElementById('ai2-star-group');
      const busyBg = document.getElementById('ai2-bg-busy');
      const cap = document.getElementById('ai2-caption');
      const rCard = document.getElementById('ai2-card-rule');
      const rStat = document.getElementById('ai2-rule-status');
      const rDesc = document.getElementById('ai2-rule-desc');
      const aStat = document.getElementById('ai2-ai-status');
      const aDesc = document.getElementById('ai2-ai-desc');
      if (!star) return;

      busyBg.style.display = cond === 'busy' ? 'block' : 'none';

      if (cond === 'center') {{
        star.setAttribute('transform', 'translate(230, 105) rotate(0) scale(1)');
        cap.innerHTML = '<strong>Kondisi 1 (Posisi Tengah Ideal):</strong> Objek bintang tepat berada di koordinat tengah dan latar belakang bersih.';
        rCard.className = 'card tint-yellow';
        rStat.style.color = '#B06000';
        rStat.textContent = '⚠️ Kebetulan Berhasil (Sangat Rapuh)';
        rDesc.innerHTML = 'Karena bintang kebetulan pas di <code>pixel[tengah]</code>, aturan <code>if-else</code> tampak berhasil. Tapi coba klik tombol kondisi lainnya!';
        aStat.textContent = '✅ BERHASIL (Keyakinan: 99%)';
        aDesc.innerHTML = 'AI mengenali <strong>pola bentuk 5 sudut bintang &amp; warna kuning</strong> secara utuh.';
      }} else if (cond === 'shift') {{
        star.setAttribute('transform', 'translate(345, 138) rotate(0) scale(1)');
        cap.innerHTML = '<strong>Kondisi 2 (Geser ke Pojok):</strong> Objek bintang bergeser ke kanan bawah. Titik tengah menjadi kosong (putih), sehingga aturan <code>if-else</code> langsung gagal!';
        rCard.className = 'card tint-red';
        rStat.style.color = '#C5221F';
        rStat.textContent = '❌ GAGAL MENEBAK!';
        rDesc.innerHTML = 'Aturan manual hanya mengecek koordinat <code>pixel[tengah]</code>. Karena bintang bergeser, titik tengah berisi warna putih (<code>255,255,255</code>) dan program mengira tidak ada bintang!';
        aStat.textContent = '✅ TETAP BERHASIL (Keyakinan: 98%)';
        aDesc.innerHTML = 'AI memindai <strong>pola bentuk &amp; warna</strong> di seluruh area foto sehingga tetap menemukan bintang walaupun posisinya bergeser!';
      }} else if (cond === 'tilt') {{
        star.setAttribute('transform', 'translate(135, 95) rotate(-28) scale(0.68)');
        cap.innerHTML = '<strong>Kondisi 3 (Miring &amp; Lebih Kecil):</strong> Foto diambil agak jauh dan miring 28°. Posisi dan ukuran pixel berubah drastis.';
        rCard.className = 'card tint-red';
        rStat.style.color = '#C5221F';
        rStat.textContent = '❌ GAGAL MENEBAK!';
        rDesc.innerHTML = 'Saat ukuran mengecil dan sudutnya miring, koordinat pixel tidak lagi cocok dengan rumus kaku buatan manusia.';
        aStat.textContent = '✅ TETAP BERHASIL (Keyakinan: 96%)';
        aDesc.innerHTML = 'AI mengenali <strong>proporsi sudut lancip bintang</strong> meskipun ukurannya lebih kecil dan posisinya miring!';
      }} else if (cond === 'busy') {{
        star.setAttribute('transform', 'translate(130, 110) rotate(12) scale(0.9)');
        cap.innerHTML = '<strong>Kondisi 4 (Latar Belakang Ramai):</strong> Banyak benda warna-warni di latar belakang yang mengecoh pembacaan pixel sederhana.';
        rCard.className = 'card tint-red';
        rStat.style.color = '#C5221F';
        rStat.textContent = '❌ GAGAL / TERKECOH LATAR!';
        rDesc.innerHTML = 'Titik tengah kebetulan terkena bercak warna kuning dari latar belakang ramai, sehingga program biasa salah mengira latar sebagai objek!';
        aStat.textContent = '✅ TETAP BERHASIL (Keyakinan: 94%)';
        aDesc.innerHTML = 'Karena dilatih dengan contoh foto <strong>polos &amp; ramai</strong>, AI mampu membedakan pola bentuk bintang dari gangguan latar belakang!';
      }}
    }}

    // Slide 21: AI Fundamental 3/3 Interactive Pipeline Simulator
    function setAi3Mode(mode) {{
      const bGood = document.getElementById('ai3-btn-good');
      const bBad = document.getElementById('ai3-btn-bad');
      const st1 = document.getElementById('ai3-st1');
      const st1Pill = document.getElementById('ai3-st1-pill');
      const st1Title = document.getElementById('ai3-st1-title');
      const st1Img = document.getElementById('ai3-st1-img');
      const st1Body = document.getElementById('ai3-st1-body');
      const st2Body = document.getElementById('ai3-st2-body');
      const st3 = document.getElementById('ai3-st3');
      const st3Pill = document.getElementById('ai3-st3-pill');
      const st3Box = document.getElementById('ai3-st3-box');
      const st3Body = document.getElementById('ai3-st3-body');
      const banner = document.getElementById('ai3-banner');
      if (!st1) return;

      if (mode === 'good') {{
        bGood.className = 'btn-ui green';
        bBad.className = 'btn-ui outline';
        bBad.style.background = '';
        bBad.style.color = '';
        bBad.style.borderColor = '';
        st1.className = 'card tint-yellow';
        st1Pill.className = 'pill yellow';
        st1Pill.textContent = 'TAHAP 1 · FOKUS HARI INI (P01)';
        st1Title.textContent = '1. Siapkan & Rapikan Foto';
        st1Img.src = 'assets/P01/06_resize_aspect_ratio.png';
        st1Body.innerHTML = 'Foto di-resize proporsional <code>224×224</code> tanpa gepeng, skala angkanya disederhanakan ke <code>0–1</code>, posisinya tegak, dan bebas file rusak/kembar.';
        st2Body.innerHTML = 'AI mempelajari pola bentuk &amp; warna dari ratusan contoh foto yang <strong>seragam, bersih, dan seimbang</strong> (polos &amp; ramai).';
        st3.className = 'card tint-green';
        st3Pill.className = 'pill green';
        st3Pill.textContent = 'TAHAP 3 · HASIL AKHIR';
        st3Box.innerHTML = '<div style="font-family:var(--font-code); font-size:11px; color:#81C995;">INPUT: Foto Baru dari HP</div><div style="font-family:var(--font-title); font-size:20px; font-weight:700; color:#FBBC04;">Prediksi: Bintang ⭐</div><div style="background:#34A853; color:#FFFFFF; font-size:11.5px; font-weight:700; padding:3px 12px; border-radius:999px;">Keyakinan AI: 98% (Akurat!)</div>';
        st3Body.innerHTML = 'Saat diberi foto baru, AI mampu menebak nama karakternya dengan <strong>akurat &amp; konsisten</strong>!';
        banner.className = 'callout green';
        banner.innerHTML = '<strong>Analogi Dapur &amp; Koki Pintar:</strong> Sepintar apa pun kokinya (<strong>AI</strong>), masakannya hanya enak jika bahan bakunya (<strong>foto</strong>) dicuci bersih dan dipotong seragam terlebih dahulu!';
      }} else {{
        bGood.className = 'btn-ui outline';
        bBad.className = 'btn-ui';
        bBad.style.background = '#EA4335';
        bBad.style.color = '#FFFFFF';
        bBad.style.borderColor = '#EA4335';
        st1.className = 'card tint-red';
        st1Pill.className = 'pill red';
        st1Pill.textContent = 'TAHAP 1 DILEWATI · BAHAN BERANTAKAN!';
        st1Title.textContent = '1. Foto Mentah Langsung Masuk';
        st1Img.src = 'assets/P01/09_exif_trap.png';
        st1Body.innerHTML = 'Foto masuk dalam kondisi <strong>miring 90° dari kamera HP</strong>, ukuran acak/gepeng, angka terlalu besar (<code>0–255</code>), serta ada file rusak &amp; duplikat!';
        st2Body.innerHTML = '<strong>Garbage In:</strong> AI kebingungan saat belajar karena bentuk objek gepeng/terbalik dan proses hitungannya tidak stabil.';
        st3.className = 'card tint-red';
        st3Pill.className = 'pill red';
        st3Pill.textContent = 'TAHAP 3 · GARBAGE OUT!';
        st3Box.innerHTML = '<div style="font-family:var(--font-code); font-size:11px; color:#F28B82;">INPUT: Foto Baru dari HP</div><div style="font-family:var(--font-title); font-size:19px; font-weight:700; color:#EA4335;">Salah Tebak / Error! ❌</div><div style="background:#EA4335; color:#FFFFFF; font-size:11.5px; font-weight:700; padding:3px 12px; border-radius:999px;">Akurasi Anjlok (Garbage Out)</div>';
        st3Body.innerHTML = 'Karena dilatih dengan data yang kotor dan tidak seragam, tebakan AI menjadi <strong>kacau di dunia nyata</strong>!';
        banner.className = 'callout red';
        banner.innerHTML = '<strong>Prinsip "Garbage In, Garbage Out":</strong> Tanpa <strong>Image Processing &amp; EDA (P01)</strong>, model AI secanggih apa pun akan gagal. Mari lihat 3 masalah foto mentah di slide berikutnya!';
      }}
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
    # Auto-number slide footers (02 / 57 .. 57 / 57) based on actual <section class="slide"> order
    parts = re.split(r'(<section class="slide\b[^>]*>[\s\S]*?</section>)', html)
    total_slides = sum(1 for p in parts if p.startswith('<section class="slide'))
    slide_idx = 0
    for i, part in enumerate(parts):
        if part.startswith('<section class="slide'):
            slide_idx += 1
            parts[i] = re.sub(
                r'(<div class="slide-footer"><span>[^<]+</span><span>)\d+\s*/\s*\d+(</span></div>)',
                rf'\g<1>{slide_idx:02d} / {total_slides}\2',
                part,
            )
    html = "".join(parts)

    OUT_HTML.write_text(html, encoding="utf-8")
    return str(OUT_HTML)


def verify_html(path_str: str) -> None:
    text = Path(path_str).read_text(encoding="utf-8")
    slide_count = len(re.findall(r'<section class="slide', text))
    assert slide_count == 57, f"Expected 57 slides, got {slide_count}"

    # Verify no P3/P4/P5/P7/P8/P04/P13 labels in visible slide sections
    body_part = text.split('<div id="stage-wrap">', 1)[1].split('<div id="controls">', 1)[0]
    p_codes = re.findall(r'\bP(?:0?[34578]|1[0-3])\b', body_part)
    # Exclude asset path 'assets/P01/'
    non_asset_codes = [
        m.group(0)
        for m in re.finditer(r'\bP(?:0?[34578]|1[0-3])\b', re.sub(r'assets/P01/', '', body_part))
    ]
    assert not non_asset_codes, f"Found unwanted session codes in slides: {non_asset_codes}"

    # Verify no datetime / calendar date / clock time strings in slides
    dt_matches = re.findall(
        r'\b(?:Minggu|Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember|202[4-9]|WIB|WITA|WIT)\b|13:00|15:00|19:30|21:30',
        body_part,
        flags=re.IGNORECASE,
    )
    assert not dt_matches, f"Found unwanted datetime strings in slides: {dt_matches}"

    # Verify every image referenced exists
    imgs = re.findall(r'src="(assets/P01/[^"]+)"', text)
    missing = [img for img in imgs if not (ROOT_DIR / "slides" / img).exists()]
    assert not missing, f"Missing image assets: {missing}"

    # Verify speaker notes time sum == 120.0 min
    notes = re.findall(r'data-notes="([^"]+)"', text)
    assert len(notes) == 57, f"Expected 57 speaker notes, got {len(notes)}"
    total_min = 0.0
    for n in notes:
        m = re.search(r'Alokasi waktu:\s*([0-9.]+)\s*menit', n)
        assert m, f"Missing time allocation in note: {n[:60]}"
        total_min += float(m.group(1))
    assert abs(total_min - 120.0) < 1e-6, f"Speaker notes sum to {total_min} min instead of 120.0"

    print(f"HTML interaktif {slide_count} slide berhasil dibuat: {path_str}")
    print(f"Verifikasi lolos: 57 slide, 0 kode P4/P5/P7/P8, {len(imgs)} gambar valid, total waktu notes = {total_min:.1f} menit.")


if __name__ == "__main__":
    out = build_html()
    verify_html(out)
