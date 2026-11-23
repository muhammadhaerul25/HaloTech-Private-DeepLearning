"""Standard HTML5 Interactive Slide Shell & Reusable Component Helpers (P02–P08).

Extracts the proven Google I/O-inspired conference design system, keyboard navigation,
notes drawer, grid overview modal, persistent session timer, Q&A/Quiz reveal mechanics,
PWA registration, and print CSS from P01 into a single reusable module.
"""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

from .registry import SessionConfig

STANDARD_CSS = """
    :root {
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
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
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
    }

    #progress-bar {
      position: fixed; top: 0; left: 0; height: 4px;
      background: linear-gradient(90deg, var(--blue), var(--red), var(--yellow), var(--green));
      width: 2%; transition: width 0.25s ease; z-index: 100;
    }

    #stage-wrap {
      width: min(96vw, calc((100vh - 92px) * 16 / 9));
      height: min(calc(100vh - 92px), calc(96vw * 9 / 16));
      flex-shrink: 0;
      position: relative;
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 24px 70px rgba(0,0,0,0.45);
      background: var(--white);
    }

    .slide {
      position: absolute; inset: 0;
      padding: 34px 50px 46px;
      display: none; flex-direction: column;
      background: var(--white); overflow: hidden;
    }
    .slide.active { display: flex; animation: fadeSlide 0.22s ease; }
    @keyframes fadeSlide {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .slide.dark { background: var(--dark); color: var(--white); }
    .slide.bg-blue { background: var(--blue); color: var(--white); }
    .slide.bg-green { background: var(--green); color: var(--dark); }
    .slide.bg-yellow { background: var(--yellow); color: var(--dark); }
    .slide.bg-red { background: var(--red); color: var(--white); }

    .kicker {
      font-family: var(--font-title); font-size: 12.5px; font-weight: 700;
      letter-spacing: 0.08em; text-transform: uppercase;
      color: var(--blue-text); margin-bottom: 5px;
    }
    .slide.dark .kicker { color: var(--yellow); }
    .slide.bg-blue .kicker, .slide.bg-red .kicker { color: rgba(255,255,255,0.92); }
    .slide.bg-green .kicker, .slide.bg-yellow .kicker { color: var(--dark); }

    h1, h2 { font-family: var(--font-title); font-weight: 700; line-height: 1.18; letter-spacing: -0.015em; }
    h1 { font-size: clamp(28px, 3.2vw, 44px); }
    h2 { font-size: clamp(22px, 2.25vw, 31px); margin-bottom: 8px; }
    .subtitle { font-size: clamp(13.5px, 1.25vw, 17px); color: var(--muted); line-height: 1.48; margin-bottom: 12px; }
    .slide.dark .subtitle { color: #BDC1C6; }

    .hl-blue { color: var(--blue-text); }
    .hl-red { color: var(--red); }
    .hl-green { color: #1E8E3E; }
    .hl-yellow { color: #E37400; }

    .pill {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 5px 13px; border-radius: 999px;
      font-family: var(--font-title); font-size: 12px; font-weight: 600;
      width: fit-content;
    }
    .pill.blue { background: var(--tint-blue); color: var(--blue-text); }
    .pill.red { background: var(--tint-red); color: #C5221F; }
    .pill.yellow { background: var(--tint-yellow); color: #B06000; }
    .pill.green { background: var(--tint-green); color: #137333; }
    .pill.dark { background: #303134; color: var(--white); }
    .pill.solid-blue { background: var(--blue); color: var(--white); }

    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; flex: 1; min-height: 0; }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; flex: 1; min-height: 0; }
    .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; flex: 1; min-height: 0; }
    .split-60-40 { display: grid; grid-template-columns: 1.38fr 1fr; gap: 18px; flex: 1; min-height: 0; align-items: stretch; }
    .split-40-60 { display: grid; grid-template-columns: 1fr 1.38fr; gap: 18px; flex: 1; min-height: 0; align-items: stretch; }

    .card {
      background: var(--white); border: 1px solid var(--border);
      border-radius: 15px; padding: 18px 22px;
      display: flex; flex-direction: column; gap: 10px;
      box-shadow: 0 3px 10px rgba(32,33,36,0.05);
      position: relative; overflow: hidden;
    }
    .card.surface { background: var(--surface); }
    .card.tint-blue { background: var(--tint-blue); border-color: #C6DAFC; }
    .card.tint-red { background: var(--tint-red); border-color: #F6AEA9; }
    .card.tint-yellow { background: var(--tint-yellow); border-color: #FDE293; }
    .card.tint-green { background: var(--tint-green); border-color: #A8DAB5; }

    .card-top-bar { position: absolute; top: 0; left: 0; right: 0; height: 4px; }
    .bar-blue { background: var(--blue); }
    .bar-red { background: var(--red); }
    .bar-yellow { background: var(--yellow); }
    .bar-green { background: var(--green); }

    .card-title { font-family: var(--font-title); font-size: clamp(15.5px, 1.4vw, 19px); font-weight: 700; color: var(--dark); }
    .card-body { font-size: clamp(13.5px, 1.18vw, 15.8px); line-height: 1.55; color: #3C4043; }
    .card-body ul { padding-left: 18px; display: flex; flex-direction: column; gap: 8px; }
    .card .callout { margin-top: auto; }

    .callout {
      background: var(--tint-blue); border-left: 4px solid var(--blue);
      border-radius: 0 11px 11px 0; padding: 10px 14px;
      font-size: clamp(12.5px, 1.08vw, 14.5px); line-height: 1.46; color: var(--dark);
    }
    .callout.red { background: var(--tint-red); border-left-color: var(--red); }
    .callout.yellow { background: var(--tint-yellow); border-left-color: var(--yellow); }
    .callout.green { background: var(--tint-green); border-left-color: var(--green); }

    .big-num { font-family: var(--font-title); font-size: clamp(28px, 3vw, 42px); font-weight: 700; line-height: 1.05; }

    pre.code {
      background: #1E2025; color: #E8EAED; font-family: var(--font-code);
      font-size: clamp(11px, 0.96vw, 12.8px); line-height: 1.48;
      padding: 12px 15px; border-radius: 11px; overflow-x: auto; border: 1px solid #3C4043;
      white-space: pre-wrap; word-break: break-word;
    }
    code { font-family: var(--font-code); background: #F1F3F4; padding: 1px 5px; border-radius: 5px; font-size: 0.9em; color: #C5221F; }
    .slide.dark code { background: rgba(255,255,255,0.13); color: #FDE293; }
    .slide.bg-blue code, .slide.bg-red code { background: rgba(255,255,255,0.18); color: #FFFFFF; }
    .slide.bg-yellow code, .slide.bg-green code { background: rgba(32,33,36,0.12); color: #202124; }
    pre.code code { background: none; padding: 0; color: inherit; }

    .img-box {
      background: var(--white); border: 1px solid var(--border);
      border-radius: 14px; padding: 10px;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      overflow: hidden; height: 100%;
    }
    .img-box img { max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 8px; }

    .step-list { display: flex; flex-direction: column; gap: 9px; flex: 1; justify-content: center; }
    .step-item {
      display: grid; grid-template-columns: 44px 1fr; gap: 13px; align-items: center;
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 13px; padding: 10px 14px;
    }
    .step-num {
      width: 38px; height: 38px; border-radius: 10px;
      background: var(--blue); color: var(--white);
      font-family: var(--font-title); font-weight: 700; font-size: 16px;
      display: flex; align-items: center; justify-content: center;
    }
    .step-num.red { background: var(--red); }
    .step-num.yellow { background: var(--yellow); color: var(--dark); }
    .step-num.green { background: var(--green); }
    .step-title { font-family: var(--font-title); font-weight: 700; font-size: 14.5px; color: var(--dark); }
    .step-desc { font-size: 13px; color: var(--muted); margin-top: 2px; line-height: 1.4; }

    table.io-table { width: 100%; border-collapse: collapse; font-size: 14.5px; border-radius: 12px; overflow: hidden; border: 1px solid var(--border); }
    table.io-table th { background: var(--dark); color: var(--white); font-family: var(--font-title); text-align: left; padding: 12px 16px; }
    table.io-table td { padding: 12px 16px; border-top: 1px solid var(--border); color: #3C4043; line-height: 1.45; }
    table.io-table tr:nth-child(even) td { background: var(--surface); }
    table.io-table.spacious th, table.io-table.spacious td { padding: 11px 18px; font-size: 15px; line-height: 1.42; }

    .cluster-4 { position: absolute; right: 42px; top: 38px; display: grid; grid-template-columns: 36px 36px; gap: 10px; }
    .c-circle { width: 34px; height: 34px; border-radius: 50%; background: var(--blue); }
    .c-square { width: 34px; height: 34px; border-radius: 8px; background: var(--red); }
    .c-tri { width: 0; height: 0; border-left: 17px solid transparent; border-right: 17px solid transparent; border-bottom: 32px solid var(--yellow); }
    .c-pill { width: 38px; height: 22px; border-radius: 999px; background: var(--green); align-self: center; }

    .slide-footer {
      position: absolute; bottom: 12px; left: 50px; right: 50px;
      display: flex; justify-content: space-between; align-items: center;
      font-size: 11.5px; color: var(--muted);
      border-top: 1px solid rgba(218,220,224,0.6); padding-top: 6px;
    }
    .slide.dark .slide-footer { color: #9AA0A6; border-top-color: rgba(255,255,255,0.12); }
    .slide.bg-blue .slide-footer, .slide.bg-red .slide-footer { color: rgba(255,255,255,0.88); border-top-color: rgba(255,255,255,0.22); }
    .slide.bg-green .slide-footer, .slide.bg-yellow .slide-footer { color: rgba(32,33,36,0.82); border-top-color: rgba(32,33,36,0.18); }

    .divider-center { flex: 1; display: flex; flex-direction: column; justify-content: center; max-width: 820px; }
    .divider-center h1 { font-size: clamp(34px, 4.2vw, 54px); margin-top: 10px; }
    .divider-center p { font-size: clamp(15px, 1.55vw, 20px); margin-top: 14px; opacity: 0.93; line-height: 1.5; }

    /* Interactive Question -> Answer Reveal */
    .qa-box { display: flex; flex-direction: column; gap: 14px; flex: 1; justify-content: center; }
    .qa-question {
      background: var(--tint-blue); border: 1.5px solid #C6DAFC; border-radius: 16px;
      padding: 18px 22px; font-family: var(--font-title); font-size: clamp(16px, 1.55vw, 21px);
      font-weight: 600; color: var(--dark); line-height: 1.4;
    }
    .qa-choices { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    .qa-choice {
      background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
      padding: 12px 14px; font-size: 14px; color: #3C4043; line-height: 1.4;
    }
    .qa-answer {
      display: none; background: var(--tint-green); border: 1.5px solid #A8DAB5;
      border-left: 6px solid var(--green); border-radius: 14px; padding: 16px 20px;
      font-size: clamp(13.5px, 1.18vw, 15.5px); line-height: 1.5; color: var(--dark);
      animation: fadeSlide 0.2s ease;
    }
    .qa-answer.shown { display: block; }
    .vis-a { display: none; }

    .btn-ui {
      background: var(--blue-text); color: white; border: none; border-radius: 10px;
      padding: 8px 16px; font-family: var(--font-title); font-size: 13px; font-weight: 600;
      cursor: pointer; width: fit-content; transition: opacity 0.15s;
    }
    .btn-ui:hover { opacity: 0.9; }
    .btn-ui.outline { background: var(--white); color: var(--blue-text); border: 1.5px solid var(--blue-text); }
    .btn-ui.green { background: #1E8E3E; color: white; }

    .quiz-item { background: var(--surface); border: 1px solid var(--border); border-radius: 13px; padding: 14px 16px; display: flex; flex-direction: column; gap: 7px; }
    .quiz-ans { display: none; background: var(--tint-green); border-left: 4px solid var(--green); padding: 8px 12px; border-radius: 0 8px 8px 0; font-size: 13px; line-height: 1.45; }
    .quiz-ans.shown { display: block; }

    .ref-list { display: flex; flex-direction: column; gap: 8px; flex: 1; }
    .ref-item {
      display: grid; grid-template-columns: 28px 1fr; gap: 10px; align-items: start;
      padding: 9px 12px; border-radius: 12px;
      background: var(--surface); border: 1px solid var(--border);
      text-decoration: none; color: inherit; user-select: text;
      transition: border-color 0.16s ease, transform 0.16s ease, background 0.16s ease, box-shadow 0.16s ease;
    }
    .ref-item:hover {
      border-color: var(--blue); background: var(--tint-blue);
      transform: translateY(-1.5px); box-shadow: 0 4px 12px rgba(26,115,232,0.12);
    }
    .ref-item.featured { background: #FFFDF5; border: 1.5px solid var(--yellow); }
    .ref-item.featured:hover { background: var(--tint-yellow); border-color: #E37400; }
    .ref-num {
      width: 26px; height: 26px; border-radius: 8px; margin-top: 1px;
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-title); font-size: 12px; font-weight: 700;
      color: var(--white); background: var(--blue); flex-shrink: 0;
    }
    .ref-num.yellow { background: var(--yellow); color: var(--dark); }
    .ref-num.green { background: var(--green); }
    .ref-num.red { background: var(--red); }
    .ref-content { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
    .ref-head { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
    .ref-title { font-family: var(--font-title); font-size: 12.6px; font-weight: 700; color: var(--dark); line-height: 1.28; }
    .ref-tag {
      font-family: var(--font-code); font-size: 9.8px; font-weight: 700;
      padding: 2px 7px; border-radius: 999px; background: var(--tint-red); color: #C5221F;
      white-space: nowrap; flex-shrink: 0;
    }
    .ref-tag.doc { background: var(--tint-blue); color: var(--blue-text); }
    .ref-tag.code { background: var(--tint-green); color: #137333; }
    .ref-tag.must { background: var(--yellow); color: var(--dark); }
    .ref-desc { font-size: 11.4px; color: #3C4043; line-height: 1.38; }
    .ref-url { font-family: var(--font-code); font-size: 9.8px; color: var(--blue-text); opacity: 0.9; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    /* Controls bar */
    #controls {
      flex-shrink: 0; display: flex; align-items: center; gap: 10px; z-index: 20;
      background: #202124; color: #E8EAED; padding: 6px 14px; border-radius: 999px;
      border: 1px solid #3C4043; font-size: 12.5px;
    }
    #page-jump {
      width: 46px; background: #303134; color: #FFFFFF; border: 1px solid #5F6368;
      border-radius: 7px; padding: 2px 5px; text-align: center;
      font-family: var(--font-code); font-size: 12.5px; font-weight: 600;
    }
    #page-jump:focus { outline: none; border-color: var(--blue); }
    :fullscreen #controls {
      position: fixed; bottom: 10px; right: 16px; z-index: 90;
      opacity: 0.35; transition: opacity 0.2s ease;
    }
    :fullscreen #controls:hover { opacity: 1; }
    .ctrl-btn {
      background: #303134; color: #E8EAED; border: 1px solid #5F6368;
      border-radius: 999px; padding: 4px 12px; cursor: pointer; font-family: var(--font-title); font-size: 12px;
      transition: background 0.15s ease, border-color 0.15s ease;
    }
    .ctrl-btn:hover { background: var(--blue); border-color: var(--blue); color: white; }
    .ctrl-btn.timer-active { background: #C5221F; border-color: #EA4335; color: #FFFFFF; }
    .ctrl-btn.timer-active:hover { background: #A50E0E; border-color: #EA4335; }

    /* Persistent session timer inside #stage-wrap */
    #session-timer {
      position: absolute; top: 12px; right: 16px; z-index: 80;
      display: none; align-items: center; gap: 8px;
      background: rgba(32, 33, 36, 0.88); color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 999px; padding: 5px 10px 5px 12px;
      backdrop-filter: blur(8px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.24);
      font-family: var(--font-code); font-size: 13px; font-weight: 600;
      user-select: none;
    }
    #session-timer.active { display: inline-flex; }
    #session-timer.overtime { border-color: rgba(251, 188, 4, 0.7); background: rgba(60, 24, 24, 0.92); }
    .timer-dot {
      width: 8px; height: 8px; border-radius: 50%; background: #34A853;
      box-shadow: 0 0 0 3px rgba(52, 168, 83, 0.28);
      animation: timerPulse 1.6s ease-in-out infinite;
      flex-shrink: 0;
    }
    #session-timer.overtime .timer-dot { background: #FBBC04; box-shadow: 0 0 0 3px rgba(251, 188, 4, 0.3); }
    @keyframes timerPulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.55; transform: scale(0.85); }
    }
    .timer-end-mini {
      background: rgba(234, 67, 53, 0.9); color: #FFFFFF; border: none;
      border-radius: 999px; padding: 2px 8px; cursor: pointer;
      font-family: var(--font-title); font-size: 10.5px; font-weight: 700;
      transition: background 0.15s ease;
    }
    .timer-end-mini:hover { background: #C5221F; }

    #notes-drawer {
      position: fixed; right: 18px; bottom: 58px; width: min(440px, 90vw); max-height: 44vh;
      background: #202124; color: #E8EAED; border: 1px solid #3C4043; border-radius: 14px;
      padding: 16px; box-shadow: 0 18px 45px rgba(0,0,0,0.5); display: none;
      flex-direction: column; gap: 8px; overflow-y: auto; z-index: 95; font-size: 13px; line-height: 1.52; user-select: text;
    }
    #notes-drawer.open { display: flex; }
    #notes-drawer h4 { font-family: var(--font-title); color: var(--yellow); font-size: 14px; }

    #grid-modal { position: fixed; inset: 0; background: rgba(17,19,23,0.95); z-index: 120; display: none; padding: 26px; overflow-y: auto; }
    #grid-modal.open { display: block; }
    .grid-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; max-width: 1300px; margin: 16px auto; }
    .g-item { background: #292A2D; color: #E8EAED; border: 1px solid #3C4043; border-radius: 11px; padding: 12px; cursor: pointer; }
    .g-item:hover { border-color: var(--blue); background: #303134; }
    .g-num { font-family: var(--font-code); font-size: 11.5px; color: var(--yellow); }
    .g-ttl { font-family: var(--font-title); font-size: 13px; font-weight: 600; margin-top: 3px; }

    @media print {
      @page { size: 13.333in 7.5in; margin: 0; }
      body { background: white; height: auto; overflow: visible; display: block; padding: 0; gap: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      #progress-bar, #controls, #notes-drawer, #grid-modal, #session-timer { display: none !important; }
      #stage-wrap { width: 13.333in; height: auto; box-shadow: none; border-radius: 0; overflow: visible; }
      .slide { position: relative !important; display: flex !important; width: 13.333in; height: 7.5in; page-break-after: always; break-after: page; animation: none !important; opacity: 1 !important; }
      .slide:last-child { page-break-after: auto; break-after: auto; }
      .qa-answer, .quiz-ans { display: block !important; animation: none !important; opacity: 1 !important; }
      .vis-q { display: none !important; }
      .vis-a { display: inline !important; }
      .btn-ui { display: none !important; }
    }
"""


def _build_core_js(session_key: str) -> str:
    slide_idx_key = f"{session_key}_slide_idx"
    timer_key = f"{session_key}_session_timer_v1"
    return f"""
    window.SLIDE_PDF_EXPANDERS = window.SLIDE_PDF_EXPANDERS || [];

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
        try {{ localStorage.setItem('{slide_idx_key}', String(idx)); }} catch (e) {{}}
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

    // Build grid overview
    const gc = document.getElementById('grid-cards');
    if (gc) {{
      slides.forEach((s, i) => {{
        const d = document.createElement('div');
        d.className = 'g-item';
        d.innerHTML = `<div class="g-num">SLIDE ${{String(i + 1).padStart(2, '0')}}</div><div class="g-ttl">${{s.dataset.title || ''}}</div>`;
        d.onclick = () => {{ showSlide(i); toggleGrid(); }};
        gc.appendChild(d);
      }});
    }}

    function syncVisualReveal(id, shown) {{
      const vis = document.getElementById(id + '-vis');
      if (!vis) return;
      vis.querySelectorAll('.vis-q').forEach((n) => {{ n.style.display = shown ? 'none' : ''; }});
      vis.querySelectorAll('.vis-a').forEach((n) => {{ n.style.display = shown ? 'inline' : 'none'; }});
    }}
    function toggleQA(id, btn) {{
      const el = document.getElementById(id);
      if (!el) return;
      const shown = el.classList.toggle('shown');
      syncVisualReveal(id, shown);
      if (btn) btn.textContent = shown ? 'Sembunyikan Jawaban' : 'Klik untuk Lihat Jawaban & Penjelasan';
    }}
    function toggleAns(id, btn) {{
      const el = document.getElementById(id);
      if (!el) return;
      const shown = el.classList.toggle('shown');
      syncVisualReveal(id, shown);
      if (btn) btn.textContent = shown ? 'Sembunyikan Jawaban' : 'Lihat Jawaban';
    }}

    // Persistent Session Timer (namespaced per session)
    const TIMER_STORAGE_KEY = '{timer_key}';
    let sessionTimerInterval = null;
    let memoryTimerState = null;

    function formatTimerDuration(ms) {{
      const totalSec = Math.max(0, Math.floor(ms / 1000));
      const hrs = Math.floor(totalSec / 3600);
      const mins = Math.floor((totalSec % 3600) / 60);
      const secs = totalSec % 60;
      const pad = (n) => String(n).padStart(2, '0');
      return hrs > 0 ? `${{hrs}}:${{pad(mins)}}:${{pad(secs)}}` : `${{pad(mins)}}:${{pad(secs)}}`;
    }}
    function readTimerState() {{
      try {{
        const raw = localStorage.getItem(TIMER_STORAGE_KEY);
        if (raw) {{ memoryTimerState = JSON.parse(raw); return memoryTimerState; }}
      }} catch (e) {{}}
      return memoryTimerState;
    }}
    function writeTimerState(state) {{
      memoryTimerState = state;
      try {{
        if (state) localStorage.setItem(TIMER_STORAGE_KEY, JSON.stringify(state));
        else localStorage.removeItem(TIMER_STORAGE_KEY);
      }} catch (e) {{}}
    }}
    function renderSessionTimer() {{
      const badge = document.getElementById('session-timer');
      const valEl = document.getElementById('session-timer-val');
      const btn = document.getElementById('timer-btn');
      const st = readTimerState();
      if (st && st.running && typeof st.startEpoch === 'number') {{
        const elapsedMs = Math.max(0, Date.now() - st.startEpoch);
        if (valEl) valEl.textContent = formatTimerDuration(elapsedMs);
        if (badge) {{
          badge.classList.add('active');
          badge.classList.toggle('overtime', elapsedMs >= 120 * 60 * 1000);
        }}
        if (btn) {{ btn.textContent = '■ End Timer'; btn.classList.add('timer-active'); }}
      }} else {{
        if (badge) badge.classList.remove('active', 'overtime');
        if (valEl) valEl.textContent = '00:00';
        if (btn) {{ btn.textContent = '▶ Start Timer'; btn.classList.remove('timer-active'); }}
      }}
    }}
    function startSessionTimer() {{
      const cur = readTimerState();
      if (cur && cur.running && typeof cur.startEpoch === 'number') return;
      writeTimerState({{ running: true, startEpoch: Date.now() }});
      renderSessionTimer();
      if (!sessionTimerInterval) sessionTimerInterval = setInterval(renderSessionTimer, 1000);
    }}
    function endSessionTimer() {{
      writeTimerState({{ running: false, startEpoch: null }});
      if (sessionTimerInterval) {{ clearInterval(sessionTimerInterval); sessionTimerInterval = null; }}
      renderSessionTimer();
    }}
    function toggleSessionTimer() {{
      const st = readTimerState();
      if (st && st.running) endSessionTimer();
      else startSessionTimer();
    }}
    window.addEventListener('storage', (e) => {{
      if (e.key === TIMER_STORAGE_KEY) renderSessionTimer();
    }});
"""


def _build_init_js(session_key: str) -> str:
    slide_idx_key = f"{session_key}_slide_idx"
    return f"""
    (function initSlide() {{
      const st = readTimerState();
      if (st && st.running && typeof st.startEpoch === 'number') {{
        renderSessionTimer();
        sessionTimerInterval = setInterval(renderSessionTimer, 1000);
      }} else {{
        renderSessionTimer();
      }}
      if ('serviceWorker' in navigator && location.protocol !== 'file:') {{
        navigator.serviceWorker.register('../../sw.js', {{ scope: '../../' }}).catch(() => {{}});
      }}
      const m = window.location.hash.match(/^#slide-(\\d+)$/);
      if (m) {{ showSlide(parseInt(m[1], 10) - 1); return; }}
      try {{
        const saved = localStorage.getItem('{slide_idx_key}');
        if (saved !== null) {{ showSlide(parseInt(saved, 10)); return; }}
      }} catch (e) {{}}
      showSlide(0);
    }})();
"""


def auto_number_slides(slides_html: str) -> tuple[str, int]:
    """Auto-number slide footers (`02 / N .. N / N`) and ensure first slide has `.active`."""
    parts = re.split(r'(<section class="slide\b[^>]*>[\s\S]*?</section>)', slides_html)
    total = sum(1 for p in parts if p.startswith('<section class="slide'))
    idx = 0
    for i, part in enumerate(parts):
        if part.startswith('<section class="slide'):
            idx += 1
            if idx == 1 and 'active' not in part.split('>', 1)[0]:
                part = part.replace('<section class="slide', '<section class="slide active', 1)
            part = re.sub(
                r'(<div class="slide-footer"><span>[^<]+</span><span>)\s*(?:\d+\s*/\s*\d+|__NUM__)\s*(</span></div>)',
                rf'\g<1>{idx:02d} / {total}\2',
                part,
            )
            parts[i] = part
    return "".join(parts), total


def render_deck_html(
    session: SessionConfig,
    slides_html: str,
    *,
    extra_css: str = "",
    extra_modals_html: str = "",
    extra_js: str = "",
    icon_rel_path: str = "../P01/assets/P01/icon-192.png",
) -> tuple[str, int]:
    """Wrap session slide sections in the standardized HTML5 presentation shell."""
    numbered_slides, total_slides = auto_number_slides(slides_html)
    session_key = session.id.lower()
    page_title = f"{session.id} - {html_lib.escape(session.title)} ({total_slides} Slides)"
    core_js = _build_core_js(session_key)
    init_js = _build_init_js(session_key)

    full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#202124" />
  <link rel="manifest" href="../../manifest.webmanifest" />
  <link rel="apple-touch-icon" href="{icon_rel_path}" />
  <title>{page_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Roboto+Mono:wght@400;500;600&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet" />
  <style>
{STANDARD_CSS}
{extra_css}
  </style>
</head>
<body>
  <div id="progress-bar"></div>
  <div id="stage-wrap">
    <div id="session-timer" role="timer" aria-live="off" title="Timer sesi berjalan (tidak ter-reset saat pindah slide/refresh)">
      <span class="timer-dot"></span>
      <span id="session-timer-val">00:00</span>
      <button type="button" class="timer-end-mini" onclick="endSessionTimer()" title="Klik untuk mengakhiri timer">End</button>
    </div>

{numbered_slides}
  </div>

  <div id="controls">
    <button class="ctrl-btn" onclick="prevSlide()">← Prev</button>
    <span id="counter" style="display:inline-flex; align-items:center; gap:5px;">
      <input id="page-jump" type="number" min="1" max="{total_slides}" value="1" title="Ketik nomor slide (1-{total_slides}) lalu tekan Enter" onchange="jumpToSlide(this.value)" onkeydown="if(event.key==='Enter'){{jumpToSlide(this.value); this.blur();}}" />
      <span>/ {total_slides}</span>
    </span>
    <button class="ctrl-btn" onclick="nextSlide()">Next →</button>
    <button class="ctrl-btn" onclick="toggleNotes()">Notes (N)</button>
    <button class="ctrl-btn" onclick="toggleGrid()">Grid (G)</button>
    <button class="ctrl-btn" onclick="toggleFull()">Fullscreen (F)</button>
    <button id="timer-btn" class="ctrl-btn" onclick="toggleSessionTimer()">▶ Start Timer</button>
  </div>

  <div id="notes-drawer">
    <h4>Catatan Pengajar (Speaker Notes)</h4>
    <div id="notes-text"></div>
  </div>

  <div id="grid-modal">
    <div style="max-width:1300px; margin:0 auto; display:flex; justify-content:space-between; align-items:center; color:white;">
      <h3 style="font-family:var(--font-title);">Daftar Semua Slide ({total_slides} Slides)</h3>
      <button class="ctrl-btn" onclick="toggleGrid()">Tutup (Esc)</button>
    </div>
    <div id="grid-cards" class="grid-cards"></div>
  </div>

{extra_modals_html}

  <script>
{core_js}
{extra_js}
{init_js}
  </script>
</body>
</html>
"""
    return full_html, total_slides


def write_deck_html(
    session: SessionConfig,
    slides_html: str,
    **kwargs,
) -> tuple[Path, int]:
    """Render and write standardized deck HTML to `session.html_path`."""
    full_html, total_slides = render_deck_html(session, slides_html, **kwargs)
    session.html_path.parent.mkdir(parents=True, exist_ok=True)
    session.html_path.write_text(full_html, encoding="utf-8")
    return session.html_path, total_slides


# ---------------------------------------------------------------------------
# Reusable Slide Section Builders
# ---------------------------------------------------------------------------
def make_divider_slide(
    *,
    bg_class: str,
    kicker: str,
    title: str,
    description: str,
    footer_label: str,
    data_title: str,
    notes: str,
) -> str:
    return f"""
    <section class="slide {bg_class}" data-title="{html_lib.escape(data_title)}" data-notes="{html_lib.escape(notes)}">
      <div class="divider-center">
        <div class="kicker">{kicker}</div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""


def make_agenda_slide(
    *,
    footer_label: str,
    notes: str,
    blocks: list[tuple[str, str, str]],
) -> str:
    """Create standard 6-card 120-minute agenda slide.

    blocks: list of (tint_and_bar_color, title, description), e.g. ('blue', '00–10 · Pemanasan', '...')
    """
    cards = []
    for color, title, desc in blocks:
        cards.append(
            f'<div class="card tint-{color}"><div class="card-top-bar bar-{color}"></div>'
            f'<div class="card-title">{title}</div><div class="card-body">{desc}</div></div>'
        )
    cards_html = "\n        ".join(cards)
    return f"""
    <section class="slide" data-title="Alur Sesi 120 Menit" data-notes="{html_lib.escape(notes)}">
      <div class="kicker">AGENDA · 120 MENIT</div>
      <h2>Alur Sesi <span class="hl-blue">Hari Ini</span></h2>
      <p class="subtitle">Belajar pelan-pelan, penuh ilustrasi visual, dan tanya-jawab interaktif yang tuntas di kelas.</p>
      <div class="grid-3">
        {cards_html}
      </div>
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""
