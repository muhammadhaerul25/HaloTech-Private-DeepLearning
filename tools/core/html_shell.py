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
      width: 100vw;
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
    body.is-fullscreen, :fullscreen body {
      padding: 0;
      gap: 0;
      background: #0B0D11;
    }

    #progress-bar {
      position: fixed; top: 0; left: 0; height: 4px;
      background: linear-gradient(90deg, var(--blue), var(--red), var(--yellow), var(--green));
      width: 2%; transition: width 0.25s ease; z-index: 100;
    }
    body.is-fullscreen #progress-bar, :fullscreen #progress-bar { height: 3px; }

    #stage-scaler {
      width: 1152px;
      height: 648px;
      flex-shrink: 0;
      position: relative;
    }

    #stage-wrap {
      width: 1152px;
      height: 648px;
      position: relative;
      transform-origin: top left;
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 24px 70px rgba(0,0,0,0.45);
      background: var(--white);
      will-change: transform;
    }
    body.is-fullscreen #stage-wrap, :fullscreen #stage-wrap {
      border-radius: 0;
      box-shadow: none;
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
    h1 { font-size: 37px; }
    h2 { font-size: 26px; margin-bottom: 8px; }
    .subtitle { font-size: 14.8px; color: var(--muted); line-height: 1.48; margin-bottom: 12px; }
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

    .card-title { font-family: var(--font-title); font-size: 16.4px; font-weight: 700; color: var(--dark); }
    .card-body { font-size: 13.8px; line-height: 1.54; color: #3C4043; }
    .card-body ul { padding-left: 18px; display: flex; flex-direction: column; gap: 8px; }
    .card .callout { margin-top: auto; }

    .callout {
      background: var(--tint-blue); border-left: 4px solid var(--blue);
      border-radius: 0 11px 11px 0; padding: 10px 14px;
      font-size: 12.8px; line-height: 1.46; color: var(--dark);
    }
    .callout.red { background: var(--tint-red); border-left-color: var(--red); }
    .callout.yellow { background: var(--tint-yellow); border-left-color: var(--yellow); }
    .callout.green { background: var(--tint-green); border-left-color: var(--green); }

    .big-num { font-family: var(--font-title); font-size: 35px; font-weight: 700; line-height: 1.05; }

    pre.code {
      background: #1E2025; color: #E8EAED; font-family: var(--font-code);
      font-size: 11.4px; line-height: 1.48;
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
    .divider-center h1 { font-size: 48px; margin-top: 10px; }
    .divider-center p { font-size: 18px; margin-top: 14px; opacity: 0.93; line-height: 1.5; }

    /* Interactive Question -> Answer Reveal */
    .qa-box { display: flex; flex-direction: column; gap: 14px; flex: 1; justify-content: center; }
    .qa-question {
      background: var(--tint-blue); border: 1.5px solid #C6DAFC; border-radius: 16px;
      padding: 18px 22px; font-family: var(--font-title); font-size: 18px;
      font-weight: 600; color: var(--dark); line-height: 1.4;
    }
    .qa-choices { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    .qa-choice {
      background: var(--surface); border: 1.5px solid var(--border); border-radius: 12px;
      padding: 11px 14px; font-size: 14px; color: #3C4043; line-height: 1.4;
    }
    .qa-choice.clickable {
      cursor: pointer; display: flex; align-items: center; justify-content: space-between; gap: 10px;
      transition: background 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease, transform 0.12s ease;
      user-select: none;
    }
    .qa-choice.clickable:hover {
      border-color: var(--blue); background: #F4F8FF;
      box-shadow: 0 3px 10px rgba(66,133,244,0.12); transform: translateY(-1px);
    }
    .qa-choice.picked-correct {
      background: var(--tint-green) !important; border-color: var(--green) !important;
      color: #137333 !important; box-shadow: 0 3px 12px rgba(52,168,83,0.18) !important;
    }
    .qa-choice.picked-wrong {
      background: var(--tint-red) !important; border-color: var(--red) !important;
      color: #C5221F !important; box-shadow: 0 3px 10px rgba(234,67,53,0.15) !important;
    }
    .qa-choice-badge {
      display: none; flex-shrink: 0; font-family: var(--font-title); font-size: 11px; font-weight: 700;
      padding: 2px 9px; border-radius: 999px; white-space: nowrap;
    }
    .qa-choice.picked-correct .qa-choice-badge { display: inline-block; background: var(--green); color: #FFFFFF; }
    .qa-choice.picked-wrong .qa-choice-badge { display: inline-block; background: var(--red); color: #FFFFFF; }
    .qa-answer {
      display: none; background: var(--tint-green); border: 1.5px solid #A8DAB5;
      border-left: 6px solid var(--green); border-radius: 14px; padding: 16px 20px;
      font-size: 13.8px; line-height: 1.5; color: var(--dark);
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
    body.is-fullscreen #controls, :fullscreen #controls {
      position: fixed; bottom: 8px; left: 50%; right: auto; transform: translateX(-50%); z-index: 90;
      width: max-content; white-space: nowrap;
      background: rgba(32, 33, 36, 0.88);
      backdrop-filter: blur(10px);
      opacity: 0.08; transition: opacity 0.22s ease;
    }
    body.is-fullscreen #controls:hover, body.is-fullscreen #controls:focus-within,
    :fullscreen #controls:hover, :fullscreen #controls:focus-within { opacity: 1; }
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
      #stage-scaler { width: auto !important; height: auto !important; display: block !important; }
      #stage-wrap { width: 13.333in !important; height: auto !important; transform: none !important; box-shadow: none; border-radius: 0; overflow: visible; }
      .slide { position: relative !important; display: flex !important; width: 13.333in; height: 7.5in; page-break-after: always; break-after: page; animation: none !important; opacity: 1 !important; }
      .slide:last-child { page-break-after: auto; break-after: auto; }
      .qa-answer, .quiz-ans { display: block !important; animation: none !important; opacity: 1 !important; }
      .vis-q { display: none !important; }
      .vis-a { display: inline !important; }
      .btn-ui { display: none !important; }
      .gloss-search-wrap, .ho-copy-btn { display: none !important; }
    }

    /* P02 Standard Reusable Layout & Component Patterns (P03-P08 Ready) */
    .sim-bar { display: flex; flex-wrap: wrap; gap: 7px; align-items: center; }
    .sim-slider-row { display: grid; grid-template-columns: 120px 1fr 56px; gap: 8px; align-items: center; font-size: 12.2px; }
    .sim-slider-row input[type="range"] { width: 100%; accent-color: var(--blue-text); cursor: pointer; }
    .sim-val { font-family: var(--font-code); font-weight: 700; text-align: right; color: var(--dark); font-size: 12.2px; }
    .formula-box { background: var(--surface); border: 1.5px solid #C6DAFC; border-radius: 12px; padding: 8px 14px; font-family: var(--font-code); font-size: 12.8px; color: var(--dark); text-align: center; font-weight: 600; }
    .canvas-box { background: var(--white); border: 1px solid var(--border); border-radius: 14px; padding: 9px 11px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; gap: 6px; height: 100%; }
    .canvas-box canvas { width: 100%; height: auto; max-height: 100%; display: block; }
    .kpi-strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .kpi-mini { background: var(--surface); border: 1px solid var(--border); border-radius: 11px; padding: 7px 9px; text-align: center; }
    .kpi-mini .k-num { font-family: var(--font-title); font-size: 17.5px; font-weight: 700; color: var(--blue-text); line-height: 1.1; }
    .kpi-mini .k-lbl { font-size: 10.2px; color: var(--muted); margin-top: 2px; }
    .mini-box { background: #FFFFFF; border: 1px solid var(--border); border-radius: 11px; padding: 9px 12px; font-size: 12.4px; line-height: 1.44; color: #3C4043; }

    /* Synced Left Card + Active Badge Choreography */
    .sync-card { position: relative; transition: transform 0.18s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.18s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.16s ease, border-color 0.16s ease; will-change: transform, box-shadow, opacity; }
    .sync-card .card-top-bar { transition: height 0.24s ease; }
    .sync-card.sync-dim { opacity: 0.48; transform: translateY(0) scale(0.992); }
    .sync-card.sync-on { opacity: 1 !important; transform: translateY(-3.5px) scale(1.012); z-index: 4; }
    .sync-card.sync-on .card-top-bar { height: 5.5px; }
    .sync-card.sync-blue   { box-shadow: 0 0 0 2.5px rgba(66,133,244,0.72), 0 8px 18px rgba(66,133,244,0.22) !important; border-color: #4285F4 !important; }
    .sync-card.sync-yellow { box-shadow: 0 0 0 2.5px rgba(251,188,4,0.84), 0 8px 18px rgba(227,116,0,0.22) !important; border-color: #FBBC04 !important; }
    .sync-card.sync-green  { box-shadow: 0 0 0 2.5px rgba(52,168,83,0.72), 0 8px 18px rgba(52,168,83,0.22) !important; border-color: #34A853 !important; }
    .sync-card.sync-red    { box-shadow: 0 0 0 2.5px rgba(234,67,53,0.72), 0 8px 18px rgba(234,67,53,0.22) !important; border-color: #EA4335 !important; }
    .sync-card::after { content: '● AKTIF'; position: absolute; top: 6px; right: 7px; font-family: var(--font-title); font-size: 7.4px; font-weight: 800; letter-spacing: 0.04em; padding: 1.5px 5.5px; border-radius: 999px; opacity: 0; transform: scale(0.8); transition: opacity 0.14s ease, transform 0.14s ease; pointer-events: none; }
    .sync-card.sync-on::after { opacity: 1; transform: scale(1); }
    .sync-card.sync-no-badge::after { display: none; }
    .sync-card.sync-blue::after   { background: #4285F4; color: #FFFFFF; }
    .sync-card.sync-yellow::after { background: #FBBC04; color: #202124; }
    .sync-card.sync-green::after  { background: #34A853; color: #FFFFFF; }
    .sync-card.sync-red::after    { background: #EA4335; color: #FFFFFF; }
    .sync-bullet { transition: background 0.24s ease, box-shadow 0.24s ease, transform 0.24s ease, opacity 0.24s ease; border-radius: 7px; padding: 2.5px 6px; margin: 0 -6px; }
    .sync-bullet.sync-dim { opacity: 0.45; }
    .sync-bullet.sync-on  { background: #FFFFFF; opacity: 1; transform: translateX(3px); }

    /* Cover Roadmaps (bg-yellow Evaluasi / bg-blue Hands-On) */
    .cover-roadmap { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; }
    .cover-roadmap-3x2 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; max-width: 740px; margin-top: 20px; }
    .cover-chip { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-radius: 13px; border: 1.5px solid rgba(0,0,0,0.10); }
    .bg-yellow .cover-chip { background: rgba(255,255,255,0.62); border-color: rgba(32,33,36,0.16); color: #202124; }
    .bg-blue   .cover-chip { background: rgba(255,255,255,0.16); border-color: rgba(255,255,255,0.34); color: #FFFFFF; }
    .bg-green  .cover-chip { background: rgba(255,255,255,0.68); border-color: rgba(32,33,36,0.16); color: #202124; }
    .bg-red    .cover-chip { background: rgba(255,255,255,0.16); border-color: rgba(255,255,255,0.34); color: #FFFFFF; }
    .cover-chip-num { width: 26px; height: 26px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-family: var(--font-title); font-size: 12px; font-weight: 800; flex-shrink: 0; }
    .bg-yellow .cover-chip-num { background: #202124; color: #FBBC04; }
    .bg-blue   .cover-chip-num { background: #FFFFFF; color: #1A73E8; }
    .bg-green  .cover-chip-num { background: #202124; color: #34A853; }
    .bg-red    .cover-chip-num { background: #FFFFFF; color: #C5221F; }
    .cover-chip-ttl { font-family: var(--font-title); font-size: 12.2px; font-weight: 700; line-height: 1.2; }
    .cover-chip-sub { font-size: 10.6px; opacity: 0.86; line-height: 1.25; margin-top: 1px; }
    .cover-env-strip { margin-top: 14px; display: inline-flex; align-items: center; gap: 8px; padding: 6px 13px; border-radius: 999px; font-family: var(--font-code); font-size: 11px; font-weight: 600; background: rgba(32,33,36,0.22); color: #FFFFFF; border: 1px solid rgba(255,255,255,0.28); }

    /* Visual-First Hands-On + Stepper */
    .ho-layout { display: grid; grid-template-columns: 0.92fr 1.28fr; gap: 15px; flex: 1; min-height: 0; align-items: stretch; }
    .ho-head-row { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin-bottom: 8px; }
    .ho-stepper { display: flex; align-items: center; gap: 3.5px; background: #F8F9FA; border: 1px solid #E0E3E7; border-radius: 999px; padding: 3px 5.5px; flex-shrink: 0; }
    .ho-step-dot { font-family: var(--font-title); font-size: 9.3px; font-weight: 700; padding: 3px 7.5px; border-radius: 999px; color: #5F6368; white-space: nowrap; }
    .ho-step-dot.done { background: #E6F4EA; color: #137333; }
    .ho-step-dot.cur  { background: #1A73E8; color: #FFFFFF; box-shadow: 0 2px 6px rgba(26,115,232,0.28); }
    .ho-left-card { justify-content: flex-start !important; gap: 9px; padding: 13px 15px !important; }
    .ho-sub-list { list-style: none !important; padding-left: 0 !important; margin: 0 !important; display: flex; flex-direction: column; gap: 7px; }
    .ho-sub-list li { display: flex; align-items: flex-start; gap: 8px; font-size: 12.2px; line-height: 1.40; color: #3C4043; }
    .ho-sub-tag { font-family: var(--font-code); font-size: 9.8px; font-weight: 700; padding: 1.5px 6.5px; border-radius: 6px; background: #E8F0FE; color: #1A73E8; border: 1px solid #C6DAFC; flex-shrink: 0; margin-top: 1px; }
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
    .ho-check-box { background: #FFFFFF; border: 1.2px solid #DADCE0; border-radius: 10px; padding: 7.5px 10px; display: flex; flex-direction: column; gap: 3px; }
    .ho-check-ttl { font-family: var(--font-title); font-size: 9.6px; font-weight: 800; color: #137333; letter-spacing: 0.03em; }
    .ho-check-items { font-size: 11px; color: #3C4043; line-height: 1.38; }
    .tok-todo { color: #FDD663; font-weight: 700; font-style: normal; background: rgba(253,214,99,0.12); padding: 0 4px; border-radius: 4px; }
    .tok-cm  { color: #7F8794; font-style: italic; }
    .tok-kw  { color: #8AB4F8; font-weight: 600; }
    .tok-str { color: #81C995; }
    .tok-num { color: #FDD663; }
    .tok-fn  { color: #F28B82; }
    .ho-vis-card { flex: 1; min-height: 0; background: #FFFFFF; border: 1.5px solid #DADCE0; border-radius: 13px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 8px rgba(32,33,36,0.05); }
    .ho-vis-bar { background: #F8F9FA; border-bottom: 1px solid #E8EAED; padding: 5px 11px; display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-shrink: 0; }
    .ho-vis-body { flex: 1; min-height: 0; padding: 6px 8px; display: flex; align-items: center; justify-content: center; background: #FFFFFF; }
    .ho-vis-body img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; display: block; border-radius: 6px; }
    .ho-vis-cap { font-size: 10.4px; color: #5F6368; background: #FAFBFD; border-top: 1px solid #EEF0F3; padding: 4.5px 11px; flex-shrink: 0; line-height: 1.3; }

    /* Interactive 2-Column Grouped Dictionary */
    .gloss-head-row { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin-bottom: 10px; }
    .gloss-controls { display: flex; align-items: center; gap: 7px; flex-wrap: wrap; }
    .gloss-search-wrap { position: relative; display: flex; align-items: center; }
    .gloss-search { font-family: var(--font-body); font-size: 11px; color: #202124; background: #F8F9FA; border: 1.4px solid #DADCE0; border-radius: 999px; padding: 4px 11px 4px 26px; width: 158px; outline: none; transition: all 0.16s ease; }
    .gloss-search:focus { background: #FFFFFF; border-color: #4285F4; width: 185px; box-shadow: 0 0 0 3px rgba(66,133,244,0.14); }
    .gloss-search-ico { position: absolute; left: 9px; font-size: 10.5px; color: #5F6368; pointer-events: none; }
    .gloss-filter-bar { display: flex; gap: 5px; flex-wrap: wrap; }
    .gloss-fbtn { font-family: var(--font-title); font-size: 10.5px; font-weight: 700; padding: 4px 10px; border-radius: 999px; border: 1.4px solid #DADCE0; background: #FFFFFF; color: #5F6368; cursor: pointer; transition: all 0.14s ease; }
    .gloss-fbtn:hover { border-color: #4285F4; color: #1A73E8; }
    .gloss-fbtn.active { background: #202124; color: #FFFFFF; border-color: #202124; }
    .dict-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 13px; flex: 1; min-height: 0; align-items: stretch; }
    .dict-col { display: flex; flex-direction: column; gap: 9px; min-height: 0; }
    .dict-group { background: #FFFFFF; border: 1.4px solid #DADCE0; border-radius: 13px; overflow: hidden; display: flex; flex-direction: column; min-height: 0; }
    .dict-group.grow { flex: 1; }
    .dict-group-head { display: flex; align-items: center; justify-content: space-between; padding: 6px 12px; font-family: var(--font-title); font-size: 10.6px; font-weight: 800; letter-spacing: 0.02em; border-bottom: 1px solid #E8EAED; }
    .dict-group-head.b1 { background: #E8F0FE; color: #1A73E8; border-bottom-color: #D2E3FC; }
    .dict-group-head.b2 { background: #FCE8E6; color: #C5221F; border-bottom-color: #FAD2CF; }
    .dict-group-head.b3 { background: #E6F4EA; color: #137333; border-bottom-color: #CEEAD6; }
    .dict-group-head.b4 { background: #FEF7E0; color: #B06000; border-bottom-color: #FDE293; }
    .dict-group-cnt { font-size: 9.4px; font-weight: 700; padding: 1.5px 7px; border-radius: 999px; background: rgba(255,255,255,0.82); }
    .dict-list { display: flex; flex-direction: column; flex: 1; }
    .dict-row { display: grid; grid-template-columns: 146px 1fr auto; gap: 9px; align-items: center; padding: 4.5px 12px; border-bottom: 1px solid #EEF0F3; flex: 1; transition: background 0.14s ease, opacity 0.18s ease; }
    .dict-row:nth-child(even) { background: #FAFBFD; }
    .dict-row:last-child { border-bottom: none; }
    .dict-row:hover { background: #F1F6FE; }
    .dict-row.ch-dim { opacity: 0.20; }
    .dict-term { font-family: var(--font-title); font-size: 11px; font-weight: 700; line-height: 1.2; }
    .dict-term.b1 { color: #1A73E8; }
    .dict-term.b2 { color: #C5221F; }
    .dict-term.b3 { color: #137333; }
    .dict-term.b4 { color: #B06000; }
    .dict-def { font-size: 10.6px; line-height: 1.28; color: #3C4043; }
    .dict-slide-btn { font-family: var(--font-code); font-size: 9.4px; font-weight: 700; padding: 2.5px 7px; border-radius: 7px; border: 1px solid #DADCE0; background: #FFFFFF; color: #5F6368; cursor: pointer; white-space: nowrap; transition: all 0.14s ease; }
    .dict-slide-btn:hover { background: #1A73E8; border-color: #1A73E8; color: #FFFFFF; }

    /* Balanced Full-Height 2x3 Reference Cards + Self-Study Route Bar */
    .ref-grid-full { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-rows: repeat(3, minmax(0, 1fr)); gap: 9px; flex: 1; min-height: 0; margin-top: 2px; }
    .ref-card-rich { display: flex; flex-direction: column; justify-content: space-between; gap: 5px; padding: 9px 13px; border-radius: 12px; min-width: 0; overflow: hidden; background: #FFFFFF; border: 1px solid #DADCE0; border-left: 4px solid #4285F4; text-decoration: none; color: inherit; user-select: text; transition: border-color 0.16s ease, transform 0.16s ease, background 0.16s ease, box-shadow 0.16s ease; }
    .ref-card-rich.acc-blue { border-left-color: #4285F4; }
    .ref-card-rich.acc-green { border-left-color: #34A853; }
    .ref-card-rich.acc-yellow { border-left-color: #FBBC04; }
    .ref-card-rich.acc-red { border-left-color: #EA4335; }
    .ref-card-rich.featured { background: #FFFDF4; border-color: #F6C343; border-left: 4px solid #FBBC04; }
    .ref-card-rich:hover { border-color: #4285F4; background: #F4F8FF; transform: translateY(-1.5px); box-shadow: 0 5px 14px rgba(26,115,232,0.12); }
    .ref-card-top { display: flex; align-items: flex-start; gap: 9px; min-width: 0; }
    .ref-card-top .ref-num { width: 25px; height: 25px; font-size: 11.6px; margin-top: 0; }
    .ref-card-head { flex: 1; min-width: 0; display: flex; align-items: flex-start; justify-content: space-between; gap: 7px; }
    .ref-card-rich .ref-title { font-size: 12.6px; line-height: 1.24; }
    .ref-card-rich .ref-desc { font-size: 11.4px; line-height: 1.38; color: #3C4043; padding-left: 34px; }
    .ref-card-foot { display: flex; align-items: center; justify-content: space-between; gap: 8px; padding-top: 5px; padding-left: 34px; border-top: 1px dashed #E8EAED; min-width: 0; }
    .ref-card-rich .ref-url { font-size: 9.9px; font-weight: 600; color: #1A73E8; min-width: 0; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .ref-ctx-pill { font-family: var(--font-title); font-size: 9.2px; font-weight: 700; padding: 2px 7.5px; border-radius: 999px; background: #F1F3F4; color: #3C4043; white-space: nowrap; flex-shrink: 0; }
    .ref-route-bar { margin-top: 10px; background: #F8F9FA; border: 1.5px solid #E0E3E7; border-radius: 12px; padding: 8px 13px; display: flex; flex-direction: column; gap: 5px; flex-shrink: 0; }
    .ref-route-head { display: flex; justify-content: space-between; align-items: center; font-family: var(--font-title); font-size: 11.2px; font-weight: 700; color: #202124; }
    .ref-route-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 9px; }
    .ref-step-box { background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 9px; padding: 6.5px 10px; font-size: 10.8px; line-height: 1.34; color: #3C4043; }

    /* White Google I/O 3-Pillar Finale */
    .finale-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; flex: 1; min-height: 0; margin-top: 8px; }
    .finale-card { background: #FFFFFF; border: 1.5px solid #DADCE0; border-radius: 15px; padding: 14px 16px; color: #202124; display: flex; flex-direction: column; justify-content: space-between; gap: 8px; position: relative; overflow: hidden; box-shadow: 0 3px 12px rgba(32,33,36,0.05); }
    .finale-top { display: flex; align-items: center; justify-content: space-between; margin-top: 2px; }
    .finale-pts { margin: 0; padding-left: 15px; display: flex; flex-direction: column; gap: 9px; font-size: 12.2px; line-height: 1.44; color: #3C4043; }
    .finale-pts strong { color: #202124; }
    .finale-strip { background: #F8F9FA; border: 1.2px solid #E0E3E7; border-radius: 9px; padding: 7px 10px; display: flex; align-items: center; justify-content: space-between; gap: 4px; }
    .finale-pill { background: #F8F9FA; border: 1.2px solid #DADCE0; border-radius: 9px; padding: 7px 10px; font-size: 11px; color: #202124; line-height: 1.32; }
    .finale-pill.blue { background: #E8F0FE; border-color: #C6DAFC; color: #174EA6; }
    .finale-pill.green { background: #E6F4EA; border-color: #A8DAB5; color: #137333; }
    .finale-pill.yellow { background: #FEF7E0; border-color: #FDE293; color: #202124; }
    .finale-banner { margin-top: 10px; background: #F8F9FA; border: 1.4px solid #DADCE0; border-left: 5px solid #34A853; border-radius: 13px; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }
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
    const BASE_STAGE_W = 1152;
    const BASE_STAGE_H = 648;
    window.__STAGE_SCALE__ = 1;

    function fitStage() {{
      const scaler = document.getElementById('stage-scaler');
      const stage = document.getElementById('stage-wrap');
      if (!scaler || !stage) return;
      const isFull = Boolean(
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        (window.innerWidth >= screen.width - 2 && window.innerHeight >= screen.height - 2)
      );
      document.body.classList.toggle('is-fullscreen', isFull);
      const fBtn = document.getElementById('full-btn');
      if (fBtn) fBtn.textContent = isFull ? 'Exit Full (F)' : 'Fullscreen (F)';

      const availW = isFull ? window.innerWidth : Math.max(320, window.innerWidth - 32);
      const availH = isFull ? window.innerHeight : Math.max(200, window.innerHeight - 76);
      const scale = Math.min(availW / BASE_STAGE_W, availH / BASE_STAGE_H);
      window.__STAGE_SCALE__ = scale;

      scaler.style.width = Math.round(BASE_STAGE_W * scale) + 'px';
      scaler.style.height = Math.round(BASE_STAGE_H * scale) + 'px';
      stage.style.transform = `scale(${{scale.toFixed(5)}})`;
    }}

    function toggleFull() {{
      if (!document.fullscreenElement) {{
        const req = document.documentElement.requestFullscreen || document.documentElement.webkitRequestFullscreen;
        if (req) req.call(document.documentElement);
      }} else {{
        const ex = document.exitFullscreen || document.webkitExitFullscreen;
        if (ex) ex.call(document);
      }}
    }}
    window.addEventListener('resize', fitStage);
    document.addEventListener('fullscreenchange', () => {{
      fitStage();
      setTimeout(() => {{ fitStage(); window.dispatchEvent(new Event('resize')); }}, 60);
    }});
    document.addEventListener('webkitfullscreenchange', () => {{
      fitStage();
      setTimeout(() => {{ fitStage(); window.dispatchEvent(new Event('resize')); }}, 60);
    }});

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
    function pickQAChoice(choiceEl, qaId) {{
      if (!choiceEl) return;
      const isCorrect = choiceEl.dataset.correct === 'true';
      choiceEl.classList.remove('picked-correct', 'picked-wrong');
      choiceEl.classList.add(isCorrect ? 'picked-correct' : 'picked-wrong');
      const badge = choiceEl.querySelector('.qa-choice-badge');
      if (badge) badge.textContent = isCorrect ? '✓ Tepat!' : '✕ Belum tepat';
    }}
    function toggleQA(id, btn) {{
      const el = document.getElementById(id);
      if (!el) return;
      const shown = el.classList.toggle('shown');
      syncVisualReveal(id, shown);
      const box = el.closest('.qa-box');
      if (box) {{
        box.querySelectorAll('.qa-choice.clickable').forEach((ch) => {{
          const badge = ch.querySelector('.qa-choice-badge');
          if (shown) {{
            if (ch.dataset.correct === 'true') {{
              ch.classList.remove('picked-wrong');
              ch.classList.add('picked-correct');
              if (badge) badge.textContent = '✓ Tepat!';
            }}
          }} else {{
            ch.classList.remove('picked-correct', 'picked-wrong');
            if (badge) badge.textContent = '';
          }}
        }});
      }}
      if (btn) btn.textContent = shown ? 'Sembunyikan Jawaban' : 'Klik untuk Lihat Jawaban & Penjelasan';
    }}
    function toggleAns(id, btn) {{
      const el = document.getElementById(id);
      if (!el) return;
      const shown = el.classList.toggle('shown');
      syncVisualReveal(id, shown);
      if (btn) btn.textContent = shown ? 'Sembunyikan Jawaban' : 'Lihat Jawaban';
    }}
    function copyHandsOnCode(btn, codeId) {{
      const el = document.getElementById(codeId);
      if (!el) return;
      const text = el.innerText || el.textContent || '';
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(() => {{
          if (!btn) return;
          const orig = btn.textContent;
          btn.textContent = '✓ Tersalin';
          setTimeout(() => {{ btn.textContent = orig; }}, 1400);
        }}).catch(() => {{}});
      }}
    }}
    function filterDictRows(btnEl, chKey, rootId) {{
      const root = document.getElementById(rootId || 'dict-root');
      if (!root) return;
      root.querySelectorAll('.gloss-fbtn').forEach((b) => b.classList.toggle('active', b === btnEl));
      root.querySelectorAll('.dict-row').forEach((row) => {{
        const match = chKey === 'all' || row.dataset.ch === chKey;
        row.classList.toggle('ch-dim', !match);
      }});
    }}
    function searchDictRows(query, rootId) {{
      const root = document.getElementById(rootId || 'dict-root');
      if (!root) return;
      const q = (query || '').trim().toLowerCase();
      root.querySelectorAll('.dict-row').forEach((row) => {{
        const hay = (row.dataset.kw || row.textContent || '').toLowerCase();
        row.classList.toggle('ch-dim', Boolean(q) && !hay.includes(q));
      }});
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
      fitStage();
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
  <div id="stage-scaler">
  <div id="stage-wrap">
    <div id="session-timer" role="timer" aria-live="off" title="Timer sesi berjalan (tidak ter-reset saat pindah slide/refresh)">
      <span class="timer-dot"></span>
      <span id="session-timer-val">00:00</span>
      <button type="button" class="timer-end-mini" onclick="endSessionTimer()" title="Klik untuk mengakhiri timer">End</button>
    </div>

{numbered_slides}
  </div>
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
    <button id="full-btn" class="ctrl-btn" onclick="toggleFull()">Fullscreen (F)</button>
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


_STD_PY_TOKEN_RE = re.compile(
    r'(?P<todo>#\s*TODO[^\n]*)'
    r'|(?P<cm>#[^\n]*)'
    r'|(?P<str>"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27)'
    r'|(?P<kw>\b(?:def|return|for|in|if|else|assert|import|from|as|None|True|False)\b)'
    r'|(?P<fn>\b(?:print|len|np|pd|tf|plt|keras)\b)'
    r'|(?P<num>\b\d+(?:\.\d+)?\b)'
)


def highlight_python(snippet: str) -> str:
    """Syntax-highlight short Python snippets for dark-theme `.ho-pre` code cards."""
    out: list[str] = []
    pos = 0
    for m in _STD_PY_TOKEN_RE.finditer(snippet):
        if m.start() > pos:
            out.append(html_lib.escape(snippet[pos : m.start()]))
        kind = m.lastgroup or ""
        tok = html_lib.escape(m.group(0))
        out.append(f'<span class="tok-{kind}">{tok}</span>')
        pos = m.end()
    if pos < len(snippet):
        out.append(html_lib.escape(snippet[pos:]))
    return "".join(out)


def make_agenda_goals_slide(
    *,
    footer_label: str,
    notes: str,
    steps: list[tuple[str, str, str, str, str]],
    goals: list[tuple[str, str]],
    rhythm_callout: str,
    title_html: str = 'Peta Perjalanan &amp; <span class="hl-blue">Target Belajar</span>',
    data_title: str = "Agenda & Learning Goals (120 Menit)",
) -> str:
    """P02-style merged Slide 02: left `.step-list` roadmap + right 3 Learning Goals card."""
    step_html = []
    for num_lbl, color, title, badge, desc in steps:
        num_cls = f" {color}" if color != "blue" else ""
        step_html.append(
            f'<div class="step-item" style="padding:10px 13px; flex:1; align-items:center;">'
            f'<div class="step-num{num_cls}">{num_lbl}</div>'
            f'<div style="flex:1;"><div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">'
            f'<span class="step-title">{title}</span>'
            f'<span class="pill {color}" style="font-size:10px; padding:2px 8px; white-space:nowrap;">{badge}</span>'
            f'</div><div class="step-desc">{desc}</div></div></div>'
        )
    goal_borders = [("blue", "#C6DAFC"), ("green", "#A8DAB5"), ("red", "#F6AEA9")]
    goal_html = []
    for idx_g, (g_title, g_desc) in enumerate(goals):
        g_col, g_bd = goal_borders[idx_g % len(goal_borders)]
        goal_html.append(
            f'<div class="mini-box" style="background:var(--tint-{g_col}); border-color:{g_bd}; flex:1; display:flex; align-items:center; padding:10px 13px; font-size:12.6px; line-height:1.42;">'
            f'<div><strong>{idx_g + 1}. {g_title}:</strong> {g_desc}</div></div>'
        )
    return f"""
    <section class="slide" data-title="{html_lib.escape(data_title)}" data-notes="{html_lib.escape(notes)}">
      <div class="kicker">PETA 120 MENIT &amp; TARGET BELAJAR</div>
      <h2>{title_html}</h2>
      <div class="split-60-40" style="flex:1; min-height:0; align-items:stretch;">
        <div class="step-list" style="justify-content:space-between; gap:8px;">
          {"".join(step_html)}
        </div>
        <div class="card surface" style="justify-content:space-between; padding:15px 17px; gap:10px; height:100%;">
          <div class="card-top-bar bar-green"></div>
          <div>
            <span class="pill green">3 LEARNING GOALS</span>
            <div class="card-title" style="margin-top:6px;">Yang Akan Kamu Kuasai</div>
          </div>
          <div style="display:flex; flex-direction:column; gap:10px; flex:1; justify-content:space-between;">
            {"".join(goal_html)}
          </div>
          <div class="callout" style="padding:8px 11px; font-size:12px;">{rhythm_callout}</div>
        </div>
      </div>
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""


def make_cover_roadmap_slide(
    *,
    bg_class: str,
    kicker: str,
    title: str,
    description: str,
    chips: list[tuple[str, str, str]],
    footer_label: str,
    data_title: str,
    notes: str,
    grid_3x2: bool = False,
    env_strip: str = "",
) -> str:
    """Create Evaluasi / Hands-On divider cover with horizontal or 3x2 roadmap chips."""
    wrap_cls = "cover-roadmap-3x2" if grid_3x2 else "cover-roadmap"
    chips_html = "\n          ".join(
        f'<div class="cover-chip"><span class="cover-chip-num">{num}</span>'
        f'<div><div class="cover-chip-ttl">{ttl}</div><div class="cover-chip-sub">{sub}</div></div></div>'
        for num, ttl, sub in chips
    )
    env_html = f'<div class="cover-env-strip">{env_strip}</div>' if env_strip else ""
    return f"""
    <section class="slide {bg_class}" data-title="{html_lib.escape(data_title)}" data-notes="{html_lib.escape(notes)}">
      <div class="divider-center" style="position:relative; z-index:1;">
        <div class="kicker">{kicker}</div>
        <h1>{title}</h1>
        <p>{description}</p>
        <div class="{wrap_cls}">
          {chips_html}
        </div>
        {env_html}
      </div>
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""


def make_qa_slide(
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
    footer_label: str,
    notes: str,
    bar_color: str = "blue",
    correct_choice: str = "A",
    data_title: str = "",
    quiz_progress_idx: int = 0,
    quiz_total: int = 5,
) -> str:
    """P02-style clickable Q&A / Quiz slide with instant feedback, `.vis-q/.vis-a`, and optional quiz stepper."""
    choice_divs = []
    for idx_c, c in enumerate(choices):
        letter = chr(ord("A") + idx_c)
        is_ok = "true" if letter == correct_choice.upper() else "false"
        choice_divs.append(
            f'<div class="qa-choice clickable" data-qa="{qa_id}" data-correct="{is_ok}" '
            f'onclick="pickQAChoice(this, \'{qa_id}\')" role="button" tabindex="0">'
            f'<span>{c}</span><span class="qa-choice-badge"></span></div>'
        )
    if quiz_progress_idx > 0:
        dots = "".join(
            f'<span class="ho-step-dot {"done" if qi < quiz_progress_idx else ("cur" if qi == quiz_progress_idx else "")}">'
            f'{"✓ " if qi < quiz_progress_idx else ""}Soal {qi}</span>'
            for qi in range(1, quiz_total + 1)
        )
        head_html = (
            f'<div class="ho-head-row" style="margin-bottom:10px;">'
            f'<div><div class="kicker">{kicker}</div><h2 style="margin-bottom:0;">{title_html}</h2></div>'
            f'<div class="ho-stepper">{dots}</div></div>'
        )
    else:
        head_html = f'<div class="kicker">{kicker}</div>\n      <h2>{title_html}</h2>'
    slide_dt = data_title or f"Tanya-Jawab #{qa_num}"
    return f"""
    <section class="slide" data-title="{html_lib.escape(slide_dt)}" data-notes="{html_lib.escape(notes)}">
      {head_html}
      <div class="split-60-40" style="align-items:stretch;">
        <div class="qa-box" style="justify-content:center; gap:10px;">
          <div class="qa-question" style="font-size:15.2px;">{question_html}</div>
          <div style="display:flex; flex-direction:column; gap:7px;">
            {" ".join(choice_divs)}
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
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""


def make_handson_step_slide(
    *,
    step_num: int,
    step_labels: list[str],
    stage_badge: str,
    title: str,
    kicker: str,
    notebook_name: str,
    goal_html: str,
    bullets_html: str,
    code_snippet: str,
    callout_html: str,
    color: str,
    footer_label: str,
    notes: str,
    theory_ref: str = "",
    output_img: str = "",
    output_caption: str = "",
    checklist_html: str = "",
    session_badge: str = "NOTEBOOK",
) -> str:
    """P02 Visual-First Hands-On template: stepper + micro-tasks + highlighted snippet + real dataset visual."""
    stepper_html = "".join(
        f'<span class="ho-step-dot {"done" if i < step_num else ("cur" if i == step_num else "")}">'
        f'{"✓ " if i < step_num else ""}{lbl}</span>'
        for i, lbl in enumerate(step_labels, 1)
    )
    theory_html = f'<div class="ho-theory-chip"><span>🔗</span><span>{theory_ref}</span></div>' if theory_ref else ""
    check_html = (
        f'<div class="ho-check-box"><div class="ho-check-ttl">🎯 CEK BERHASIL</div>'
        f'<div class="ho-check-items">{checklist_html}</div></div>'
        if checklist_html
        else ""
    )
    vis_html = (
        f'<div class="ho-vis-card"><div class="ho-vis-bar">'
        f'<span style="font-family:var(--font-title); font-size:9.6px; font-weight:800; color:#137333; letter-spacing:0.03em;">● OUTPUT VISUAL NYATA (DATA FROZEN v1)</span>'
        f'<span style="font-family:var(--font-code); font-size:9.4px; color:#5F6368;">Hasil langsung di bawah sel</span></div>'
        f'<div class="ho-vis-body"><img src="{output_img}" alt="Visual Output {html_lib.escape(title)}" /></div>'
        f'<div class="ho-vis-cap">{output_caption}</div></div>'
        if output_img
        else ""
    )
    return f"""
    <section class="slide" data-title="Hands-On {stage_badge}: {title}" data-notes="{html_lib.escape(notes)}">
      <div class="ho-head-row">
        <div>
          <div class="kicker">{kicker}</div>
          <h2 style="margin-bottom:0;">{stage_badge}: <span class="hl-{color}">{title}</span></h2>
        </div>
        <div class="ho-stepper">{stepper_html}</div>
      </div>
      <div class="ho-layout">
        <div class="card surface ho-left-card">
          <div class="card-top-bar bar-{color}"></div>
          <div>
            <span class="pill {color}">{stage_badge.upper()} · {session_badge}</span>
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
                <span class="pill dark" style="font-size:10px; padding:1.5px 8px;">{notebook_name}</span>
              </div>
              <div style="display:flex; align-items:center; gap:7px;">
                <span style="font-family:var(--font-code); font-size:10px; color:#9AA0A6;">Shift+Enter</span>
                <button type="button" class="ho-copy-btn" onclick="copyHandsOnCode(this, 'ho-code-{step_num}')">Salin</button>
              </div>
            </div>
            <pre class="code ho-pre"><code id="ho-code-{step_num}">{highlight_python(code_snippet)}</code></pre>
          </div>
          {vis_html}
        </div>
      </div>
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""


def make_summary_3pillars_slide(
    *,
    session_id: str,
    title_html: str,
    kicker: str,
    pillars: list[dict],
    banner_left_html: str,
    banner_quote: str,
    footer_label: str,
    notes: str,
) -> str:
    """White Google I/O 3-pillar summary slide (`01`, `02`, `03` cards + green-accented footer banner)."""
    num_colors = {"blue": "#1A73E8", "green": "#137333", "red": "#E37400", "yellow": "#B06000"}
    cards_html = []
    for idx_p, p in enumerate(pillars, 1):
        bar = p.get("bar", "blue")
        pill_cls = p.get("pill_cls", bar)
        foot_cls = p.get("foot_cls", pill_cls)
        bullets = "".join(f"<li>{b}</li>" for b in p.get("bullets", []))
        strip = f'<div class="finale-strip">{p["strip_html"]}</div>' if p.get("strip_html") else ""
        cards_html.append(
            f'<div class="finale-card"><div class="card-top-bar bar-{bar}"></div>'
            f'<div class="finale-top"><div class="big-num" style="color:{num_colors.get(bar, "#1A73E8")}; font-size:32px;">{idx_p:02d}</div>'
            f'<span class="pill {pill_cls}" style="font-size:9.6px; padding:2px 8px;">{p["badge"]}</span></div>'
            f'<div class="card-title" style="color:#202124; font-size:15.5px;">{p["title"]}</div>'
            f'<ul class="finale-pts">{bullets}</ul>{strip}'
            f'<div class="finale-pill {foot_cls}">{p["foot_html"]}</div></div>'
        )
    return f"""
    <section class="slide" data-title="3 Poin Utama Hari Ini" data-notes="{html_lib.escape(notes)}" style="background: radial-gradient(circle at 88% 18%, rgba(66,133,244,0.06) 0%, rgba(52,168,83,0.04) 42%, #FFFFFF 100%);">
      <div class="kicker" style="position:relative; z-index:1;">{kicker}</div>
      <h2 style="position:relative; z-index:1;">{title_html}</h2>
      <div class="finale-grid" style="position:relative; z-index:1;">
        {"".join(cards_html)}
      </div>
      <div class="finale-banner" style="position:relative; z-index:1;">
        <div style="font-size:12.2px; color:#202124;">{banner_left_html}</div>
        <div style="font-size:11.6px; font-style:italic; color:#5F6368; white-space:nowrap;">{banner_quote}</div>
      </div>
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""


def make_closing_slide(
    *,
    session_id: str,
    status_badge: str,
    headline_html: str,
    subtext_html: str,
    footer_label: str,
    notes: str,
) -> str:
    """Crisp White Google I/O closing slide with balanced whitespace & 4-color gradient divider."""
    return f"""
    <section class="slide" data-title="Closing &amp; Key Quote" data-notes="{html_lib.escape(notes)}" style="background: radial-gradient(circle at 84% 24%, rgba(66,133,244,0.09) 0%, rgba(234,67,53,0.05) 36%, rgba(52,168,83,0.06) 68%, #FFFFFF 100%); justify-content: space-between;">
      <svg viewBox="0 0 960 540" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:0;">
        <circle cx="885" cy="84" r="24" fill="#E8F0FE" stroke="#4285F4" stroke-width="2" opacity="0.8"/>
        <rect x="64" y="408" width="22" height="22" rx="7" transform="rotate(18 75 419)" fill="#FCE8E6" stroke="#EA4335" stroke-width="2" opacity="0.78"/>
        <polygon points="884,412 899,438 869,438" fill="#E6F4EA" stroke="#34A853" stroke-width="2" opacity="0.82"/>
        <circle cx="96" cy="96" r="12" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2" opacity="0.85"/>
      </svg>
      <div style="position:relative; z-index:1; display:flex; align-items:center; justify-content:space-between;">
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="font-family:var(--font-title); font-size:12px; font-weight:700; letter-spacing:1.8px; color:#5F6368;">CLOSING · {session_id}</span>
          <span style="background:#E6F4EA; border:1px solid #A8DAB5; color:#137333; font-family:var(--font-title); font-size:10.5px; font-weight:700; padding:3px 10px; border-radius:999px;">{status_badge}</span>
        </div>
        <div style="display:flex; gap:7px; align-items:center;">
          <span style="width:10px; height:10px; border-radius:50%; background:#4285F4;"></span>
          <span style="width:10px; height:10px; border-radius:50%; background:#EA4335;"></span>
          <span style="width:10px; height:10px; border-radius:50%; background:#FBBC04;"></span>
          <span style="width:10px; height:10px; border-radius:50%; background:#34A853;"></span>
        </div>
      </div>
      <div style="position:relative; z-index:1; margin:auto 0; display:flex; flex-direction:column; align-items:center; text-align:center; gap:18px; padding:0 48px;">
        <h1 style="font-family:var(--font-title); font-size:clamp(25px,2.55vw,32px); font-weight:700; line-height:1.38; color:#202124; max-width:850px; margin:0; letter-spacing:-0.3px;">{headline_html}</h1>
        <div style="height:4px; width:240px; border-radius:999px; background:linear-gradient(90deg, #4285F4 0%, #EA4335 35%, #FBBC04 70%, #34A853 100%); margin:2px 0;"></div>
        <p style="font-size:15.5px; color:#5F6368; max-width:820px; line-height:1.5; margin:0;">{subtext_html}</p>
      </div>
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""


def make_glossary_slide(
    *,
    kicker: str,
    title_html: str,
    groups: list[dict],
    footer_label: str,
    notes: str,
    data_title: str = "Kamus Istilah",
    root_id: str = "dict-root",
) -> str:
    """Slide Kamus Istilah 2 kolom standar P02 dengan filter Bab, pencarian, dan lompat slide SXX."""
    def _rows_html(items: list[tuple[str, str, int, str]], ch_key: str, color_cls: str) -> str:
        out = []
        for term, defn, snum, kw in items:
            target_idx = max(0, int(snum) - 1)
            out.append(
                f'<div class="dict-row" data-ch="{html_lib.escape(ch_key)}" data-kw="{html_lib.escape(kw.lower())}">'
                f'<div class="dict-term {html_lib.escape(color_cls)}">{term}</div>'
                f'<div class="dict-def">{defn}</div>'
                f'<button type="button" class="dict-slide-btn" onclick="showSlide({target_idx})" title="Lompat ke Slide {snum:02d}">S{snum:02d} &#8599;</button>'
                f'</div>'
            )
        return "\n              ".join(out)

    total_terms = sum(len(g.get("items", [])) for g in groups)
    filter_btns = [
        f'<button type="button" class="gloss-fbtn active" data-ch="all" onclick="filterDictRows(this, \'all\', \'{root_id}\')">Semua ({total_terms})</button>'
    ]
    left_groups: list[str] = []
    right_groups: list[str] = []
    for g in groups:
        ch_key = str(g["ch"])
        color_cls = g.get("color", "b1")
        label = g["label"]
        heading = g["heading"]
        items = g.get("items", [])
        col = g.get("col", "left")
        grow_cls = " grow" if g.get("grow", True) else ""
        filter_btns.append(
            f'<button type="button" class="gloss-fbtn" data-ch="{html_lib.escape(ch_key)}" onclick="filterDictRows(this, \'{html_lib.escape(ch_key)}\', \'{root_id}\')">{html_lib.escape(label)} ({len(items)})</button>'
        )
        card = (
            f'<div class="dict-group{grow_cls}">\n'
            f'            <div class="dict-group-head {html_lib.escape(color_cls)}">\n'
            f'              <span>{heading}</span>\n'
            f'              <span class="dict-group-cnt">{len(items)} istilah</span>\n'
            f'            </div>\n'
            f'            <div class="dict-list">\n'
            f'              {_rows_html(items, ch_key, color_cls)}\n'
            f'            </div>\n'
            f'          </div>'
        )
        if col == "right":
            right_groups.append(card)
        else:
            left_groups.append(card)

    return f"""    <section class="slide" id="{html_lib.escape(root_id)}" data-title="{html_lib.escape(data_title)}" data-notes="{html_lib.escape(notes)}">
      <div class="gloss-head-row">
        <div>
          <div class="kicker">{kicker}</div>
          <h2 style="margin-bottom:0;">{title_html}</h2>
        </div>
        <div class="gloss-controls pdf-keep-ui">
          <div class="gloss-search-wrap">
            <span class="gloss-search-ico">&#128269;</span>
            <input type="text" class="gloss-search" placeholder="Cari istilah..." oninput="searchDictRows(this.value, '{html_lib.escape(root_id)}')" />
          </div>
          <div class="gloss-filter-bar">
            {''.join(filter_btns)}
          </div>
        </div>
      </div>
      <div class="dict-grid">
        <div class="dict-col">
          {''.join(left_groups)}
        </div>
        <div class="dict-col">
          {''.join(right_groups)}
        </div>
      </div>
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""


def make_references_slide(
    *,
    kicker: str,
    title_html: str,
    cards: list[dict],
    route_title: str,
    route_badge: str = "Opsional · Klik kartu untuk membuka",
    route_steps: list[tuple[str, str, str]] | None = None,
    footer_label: str,
    notes: str,
    data_title: str = "Referensi Materi",
) -> str:
    """Slide Referensi 2x3 balanced (.ref-grid-full) + route bar bawah standar P02 (0 menit)."""
    card_html: list[str] = []
    for c in cards:
        num = c["num"]
        title = c["title"]
        url = c["url"]
        tag = c["tag"]
        desc = c["desc"]
        ctx = c["ctx"]
        accent = c.get("accent", "acc-blue")
        num_cls = c.get("num_cls", "")
        tag_cls = c.get("tag_cls", "")
        featured_cls = " featured" if c.get("featured") else ""
        disp_url = c.get("display_url", url.replace("https://", "").replace("http://", "").rstrip("/") + " ↗")
        card_html.append(
            f'<a class="ref-card-rich {html_lib.escape(accent)}{featured_cls}" href="{html_lib.escape(url)}" target="_blank" rel="noopener">\n'
            f'          <div class="ref-card-top">\n'
            f'            <div class="ref-num {html_lib.escape(num_cls)}">{num}</div>\n'
            f'            <div class="ref-card-head"><span class="ref-title">{title}</span><span class="ref-tag {html_lib.escape(tag_cls)}">{tag}</span></div>\n'
            f'          </div>\n'
            f'          <div class="ref-desc">{desc}</div>\n'
            f'          <div class="ref-card-foot"><span class="ref-url">{disp_url}</span><span class="ref-ctx-pill">{ctx}</span></div>\n'
            f'        </a>'
        )

    steps_html = ""
    if route_steps:
        step_boxes = "".join(
            f'<div class="ref-step-box"><strong style="color:{html_lib.escape(color)};">{head}</strong> {body}</div>'
            for color, head, body in route_steps
        )
        steps_html = f"""
      <div class="ref-route-bar">
        <div class="ref-route-head">
          <span>{route_title}</span>
          <span class="pill blue" style="font-size:9.6px; padding:2px 8px;">{route_badge}</span>
        </div>
        <div class="ref-route-grid">
          {step_boxes}
        </div>
      </div>"""

    return f"""    <section class="slide" data-title="{html_lib.escape(data_title)}" data-notes="{html_lib.escape(notes)}">
      <div class="kicker">{kicker}</div>
      <h2>{title_html}</h2>
      <div class="ref-grid-full">
        {''.join(card_html)}
      </div>{steps_html}
      <div class="slide-footer"><span>{html_lib.escape(footer_label)}</span><span>__NUM__</span></div>
    </section>
"""

