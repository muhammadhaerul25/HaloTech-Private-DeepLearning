"""Generate 59-slide interactive HTML5 deck (SSOT) for P02: Computer Vision 101.

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

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from core.html_shell import make_agenda_slide, make_divider_slide, write_deck_html  # noqa: E402
from core.registry import get_session  # noqa: E402

SESSION = get_session("P02")
ASSETS_DIR = SESSION.assets_dir
FOOTER = SESSION.short_title

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
) -> str:
    choices_html = "\n            ".join(f'<div class="qa-choice">{c}</div>' for c in choices)
    return f"""
    <section class="slide" data-title="Tanya-Jawab #{qa_num}" data-notes="{notes}">
      <div class="kicker">{kicker}</div>
      <h2>{title_html}</h2>
      <div class="split-60-40" style="align-items:stretch;">
        <div class="qa-box" style="justify-content:center; gap:11px;">
          <div class="qa-question" style="font-size:clamp(14.5px,1.35vw,18px);">{question_html}</div>
          <div style="display:flex; flex-direction:column; gap:7px;">
            {choices_html}
          </div>
          <button class="btn-ui" onclick="toggleQA('{qa_id}', this)">Klik untuk Lihat Jawaban &amp; Penjelasan</button>
          <div id="{qa_id}" class="qa-answer" style="padding:11px 15px; font-size:13.2px;">{answer_html}</div>
        </div>
        <div id="{qa_id}-vis" class="card surface" style="justify-content:center; align-items:center; text-align:center; gap:10px;">
          <div class="card-top-bar bar-{bar_color}"></div>
          <div class="vis-q" style="width:100%;">{vis_q_html}</div>
          <div class="vis-a" style="width:100%;">{vis_a_html}</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""


def _handson_step_slide(
    *,
    step_num: int,
    title: str,
    kicker: str,
    goal_html: str,
    bullets_html: str,
    code_snippet: str,
    callout_html: str,
    color: str,
    notes: str,
) -> str:
    return f"""
    <section class="slide" data-title="Hands-On Langkah {step_num}: {title}" data-notes="{notes}">
      <div class="kicker">{kicker}</div>
      <h2>Langkah {step_num}: <span class="hl-{color}">{title}</span></h2>
      <div class="ho-layout">
        <div class="card surface" style="justify-content:space-between; padding:16px 18px;">
          <div class="card-top-bar bar-{color}"></div>
          <div>
            <span class="pill {color}">LANGKAH {step_num} / 6 · NOTEBOOK P02</span>
            <div class="card-title" style="margin-top:8px;">{goal_html}</div>
          </div>
          <div class="card-body" style="font-size:13.3px;">
            <ul>{bullets_html}</ul>
          </div>
          <div class="callout {color if color != 'blue' else ''}">{callout_html}</div>
        </div>
        <div class="card" style="background:#181A1F; border-color:#3C4043; padding:14px 16px; justify-content:space-between;">
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <span class="pill dark" style="font-size:11px;">P02_computer_vision_101.ipynb</span>
            <span style="font-family:var(--font-code); font-size:11px; color:#9AA0A6;">Python · NumPy / Keras</span>
          </div>
          <pre class="code" style="margin:0; flex:1; border:none; background:#181A1F; padding:10px 2px; font-size:12px;"><code>{code_snippet}</code></pre>
          <div style="font-size:11.5px; color:#BDC1C6; border-top:1px solid #303134; padding-top:8px;">
            Jalankan sel satu per satu (<code>Shift + Enter</code>) dan cocokkan hasilnya dengan teori Bab 1–4.
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""


def build_slides_html(data: dict) -> str:
    total_imgs = data["total_images"]
    polos_n = data["polos_count"]
    ramai_n = data["ramai_count"]
    sessions_n = data["sessions_count"]
    fp = data["mini_forward_pass"]
    x0, x1, x2, x3 = fp["x"]
    h0, h1 = fp["h1"]
    l0, l1 = fp["logits"]
    p0, p1 = fp["probs"]

    s: list[str] = []

    # =========================================================================
    # PEMBUKA (SLIDE 01–06 · 6.0 MENIT)
    # =========================================================================
    s.append(
        f"""
    <!-- 01: COVER -->
    <section class="slide active" data-title="Cover — Computer Vision 101" data-notes="Alokasi waktu: 1 menit. Selamat datang di P02 Computer Vision 101! Dari peta besar AI, ML, dan DL, lalu 4 jenis tugas Computer Vision, sampai membedah Neural Network dari satu neuron hingga arsitektur visi komputer modern." style="background: radial-gradient(circle at 82% 46%, rgba(234,67,53,0.12) 0%, rgba(66,133,244,0.10) 35%, rgba(251,188,4,0.08) 60%, #FFFFFF 100%); justify-content: space-between;">
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
          <h1 style="font-family:var(--font-title); font-size:clamp(30px,3.6vw,46px); font-weight:700; line-height:1.1; color:#202124; margin:0; letter-spacing:-0.6px;">
            P02 — Computer<br />
            <span style="display:inline-block; padding-top:2px; background:linear-gradient(90deg, #EA4335 0%, #4285F4 55%, #34A853 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Vision 101</span>
          </h1>
          <div style="height:4px; width:100%; max-width:520px; border-radius:999px; margin:10px 0 12px; background:linear-gradient(90deg, #4285F4 0%, #EA4335 35%, #FBBC04 70%, #34A853 100%);"></div>
          <div style="font-size:clamp(14.5px,1.4vw,18.5px); font-weight:500; color:#5F6368; line-height:1.42;">
            Dari Peta Besar <strong>AI · ML · DL</strong> &amp; Tugas Computer Vision,<br />
            hingga Bedah <strong>Neural Network</strong> dari 1 Neuron sampai Arsitektur Modern
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
            <svg viewBox="0 0 120 56" style="width:112px; height:50px; flex-shrink:0;">
              <g stroke="#CFD4DA" stroke-width="1.4">
                <line x1="16" y1="12" x2="60" y2="16"/><line x1="16" y1="12" x2="60" y2="40"/>
                <line x1="16" y1="28" x2="60" y2="16"/><line x1="16" y1="28" x2="60" y2="40"/>
                <line x1="16" y1="44" x2="60" y2="16"/><line x1="16" y1="44" x2="60" y2="40"/>
                <line x1="60" y1="16" x2="104" y2="10"/><line x1="60" y1="16" x2="104" y2="28"/><line x1="60" y1="16" x2="104" y2="46"/>
                <line x1="60" y1="40" x2="104" y2="10"/><line x1="60" y1="40" x2="104" y2="28"/><line x1="60" y1="40" x2="104" y2="46"/>
              </g>
              <circle cx="16" cy="12" r="5.5" fill="#4285F4" stroke="#FFF" stroke-width="1.5"/>
              <circle cx="16" cy="28" r="5.5" fill="#4285F4" stroke="#FFF" stroke-width="1.5"/>
              <circle cx="16" cy="44" r="5.5" fill="#4285F4" stroke="#FFF" stroke-width="1.5"/>
              <circle cx="60" cy="16" r="6.5" fill="#FBBC04" stroke="#FFF" stroke-width="1.5"/>
              <circle cx="60" cy="40" r="6.5" fill="#EA4335" stroke="#FFF" stroke-width="1.5"/>
              <circle cx="104" cy="10" r="5" fill="#34A853" stroke="#FFF" stroke-width="1.5"/>
              <circle cx="104" cy="28" r="6" fill="#34A853" stroke="#FFF" stroke-width="1.5"/>
              <circle cx="104" cy="46" r="5" fill="#34A853" stroke="#FFF" stroke-width="1.5"/>
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
        <span class="pill yellow" style="font-size:10.5px; padding:4px 10px;">Arsitektur CV</span>
        <span class="pill solid-blue" style="font-size:10.5px; padding:4px 12px;">NumPy</span>
        <span class="pill" style="background:#EA4335; color:#FFFFFF; font-size:10.5px; padding:4px 12px;">Keras</span>
      </div>
    </section>

    <!-- 02: AGENDA & LEARNING GOALS (GABUNGAN PETA + ALUR 120M + TUJUAN) -->
    <section class="slide" data-title="Agenda &amp; Learning Goals (120 Menit)" data-notes="Alokasi waktu: 2 menit. Satu slide ringkas yang menyatukan agenda 5 bab, pembagian durasi 120 menit, dan 3 target belajar utama agar peserta langsung paham arah sesi tanpa pengulangan.">
      <div class="kicker">SESSION OVERVIEW · 120 MENIT</div>
      <h2>Agenda &amp; <span class="hl-blue">Learning Goals</span></h2>
      <div class="split-60-40" style="align-items:stretch;">
        <div class="step-list" style="gap:7px;">
          <div class="step-item" style="padding:8px 12px;">
            <div class="step-num">01</div>
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">AI vs Machine Learning vs Deep Learning</span>
                <span class="pill blue" style="font-size:10px; padding:2px 8px;">~9 menit</span>
              </div>
              <div class="step-desc">Bukan AI vs AI Klasik vs AI Modern, paradigma belajar ML, dan beda spesifik ML vs DL.</div>
            </div>
          </div>
          <div class="step-item" style="padding:8px 12px;">
            <div class="step-num red">02</div>
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">4 Task Utama Computer Vision</span>
                <span class="pill red" style="font-size:10px; padding:2px 8px;">~10 menit</span>
              </div>
              <div class="step-desc"><em>Classification, Object Detection, Semantic &amp; Instance Segmentation,</em> &amp; <em>Object Tracking</em>.</div>
            </div>
          </div>
          <div class="step-item" style="padding:8px 12px;">
            <div class="step-num green">03</div>
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">Neural Network: Terkecil → Terbesar</span>
                <span class="pill green" style="font-size:10px; padding:2px 8px;">~27 menit</span>
              </div>
              <div class="step-desc">1 Neuron → Input/Output/Hidden Layer → Forward Pass → intuisi <em>Loss &amp; Gradient Descent</em>.</div>
            </div>
          </div>
          <div class="step-item" style="padding:8px 12px;">
            <div class="step-num yellow">04</div>
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">Arsitektur Neural Network untuk CV</span>
                <span class="pill yellow" style="font-size:10px; padding:2px 8px;">~6 menit</span>
              </div>
              <div class="step-desc">Batasan MLP pada foto &amp; peta arsitektur visi komputer modern menuju P03–P04.</div>
            </div>
          </div>
          <div class="step-item" style="padding:8px 12px;">
            <div class="step-num">05</div>
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                <span class="step-title">Istirahat, Hands-On Notebook &amp; Kuis</span>
                <span class="pill dark" style="font-size:10px; padding:2px 8px;">5m + 57m</span>
              </div>
              <div class="step-desc">Istirahat 5m → 6 langkah praktik (42m) → Mini-Challenge (5m) → Kamus &amp; Kuis 5 soal (10m).</div>
            </div>
          </div>
        </div>

        <div class="card surface" style="justify-content:space-between; padding:15px 17px;">
          <div class="card-top-bar bar-green"></div>
          <div>
            <span class="pill green">3 LEARNING GOALS</span>
            <div class="card-title" style="margin-top:6px;">Yang Akan Kamu Kuasai</div>
          </div>
          <div style="display:flex; flex-direction:column; gap:8px;">
            <div class="mini-box" style="background:var(--tint-blue); border-color:#C6DAFC;">
              <strong>1. Peta AI &amp; Task CV:</strong> Tepat membedakan AI/ML/DL dan memilih <em>Image Classification</em> untuk proyek Frozen.
            </div>
            <div class="mini-box" style="background:var(--tint-green); border-color:#A8DAB5;">
              <strong>2. Bedah Neural Network:</strong> Paham alur 1 Neuron → Layer → Forward Pass dan bisa mencocokkan parameter dengan <code>model.summary()</code>.
            </div>
            <div class="mini-box" style="background:var(--tint-red); border-color:#F6AEA9;">
              <strong>3. Alasan Pindah ke CNN:</strong> Melihat langsung ledakan <strong>19,27 juta bobot</strong> pada MLP sebagai jembatan logis ke P03!
            </div>
          </div>
          <div class="callout"><strong>Ritme 120 Menit:</strong> ~58m pembuka &amp; teori interaktif → <strong>5m istirahat</strong> → 57m praktik, challenge &amp; kuis.</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 03: PEMANASAN RECAP P01 -->
    <section class="slide" data-title="Pemanasan: Recap P01 — Foto = Matriks Angka" data-notes="Alokasi waktu: 2 menit. Kita menyambung langsung dari akhir P01: komputer tidak melihat boneka Elsa seperti mata kita, melainkan melihat matriks angka piksel RGB berskala 0 sampai 1 dari dataset proyek Frozen kita.">
      <div class="kicker">PEMANASAN · RECAP P01</div>
      <h2>Menyambung P01: Foto Frozen di Mata Komputer = <span class="hl-blue">Matriks Angka</span></h2>
      <div class="split-60-40">
        <div style="display:flex; flex-direction:column; gap:8px; min-height:0;">
          <div class="img-box" style="flex:1; min-height:0; padding:6px;">
            <img src="assets/P02/01_frozen_gallery_5classes.png" alt="Galeri 5 Karakter Disney Frozen Polos vs Ramai" />
          </div>
          <div class="kpi-strip">
            <div class="kpi-mini"><div class="k-num">{total_imgs}</div><div class="k-lbl">Foto Asli (v1)</div></div>
            <div class="kpi-mini"><div class="k-num" style="color:#137333;">5 Kelas</div><div class="k-lbl">Anna s.d. Sven</div></div>
            <div class="kpi-mini"><div class="k-num" style="color:#EA4335;">{polos_n} / {ramai_n}</div><div class="k-lbl">Polos vs Ramai</div></div>
            <div class="kpi-mini"><div class="k-num" style="color:#B06000;">{sessions_n} Sesi</div><div class="k-lbl">Sesi Foto</div></div>
          </div>
        </div>
        <div class="card surface" style="gap:9px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Modal dari P01 yang Kita Bawa Hari Ini</div>
          <div class="card-body" style="font-size:13.3px;">
            <ul>
              <li>Setiap foto warna adalah array 3D berukuran <code>(Tinggi, Lebar, 3)</code> — misalnya setelah di-<em>resize</em> menjadi <code>(224, 224, 3)</code>.</li>
              <li>Angka piksel asli <code>0–255</code> dinormalisasi menjadi <code>0.0–1.0</code> (<code>float32</code>) agar perhitungan komputer stabil.</li>
              <li>Dataset proyek kita berisi <strong>5 karakter Disney Frozen</strong> dalam 2 kondisi latar: <strong>Polos</strong> dan <strong>Ramai</strong>.</li>
            </ul>
          </div>
          <div class="callout"><strong>Pertanyaan besar hari ini:</strong> Setelah foto jadi angka <code>0.0–1.0</code>, bagaimana komputer bisa menebak isinya?</div>
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
            vis_q_html='<img src="assets/P02/thumb_elsa_ramai.jpg" alt="Elsa latar ramai" style="width:185px; height:185px; object-fit:cover; border-radius:14px; border:2px solid #DADCE0;"/><div style="margin-top:8px; font-size:13px; color:#5F6368;">Foto Elsa di latar rak ramai — aturan warna sederhana mudah tertipu!</div>',
            vis_a_html='<img src="assets/P02/thumb_elsa_ramai.jpg" alt="Elsa latar ramai" style="width:155px; height:155px; object-fit:cover; border-radius:14px; border:3px solid #34A853;"/><div class="mini-box" style="margin-top:8px; background:#E6F4EA; border-color:#A8DAB5;"><strong>Belajar dari Contoh:</strong> Model mempelajari kombinasi pola wajah, rambut, dan gaun secara otomatis dari data latih.</div>',
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
      <div class="kicker">BAB 01 · SIMULATOR #1 · PARADIGMA BELAJAR</div>
      <h2><span class="hl-red">Machine Learning (ML)</span>: Belajar dari Contoh</h2>
      <div class="sim-bar pdf-keep-ui" id="ml-tabs" style="margin-bottom:10px;">
        <button class="btn-ui" data-ml="rule" onclick="setMlTab('rule')">1. Pemrograman Tradisional (Aturan Manual)</button>
        <button class="btn-ui outline" data-ml="ml" onclick="setMlTab('ml')">2. Machine Learning (Training → Prediksi)</button>
      </div>
      <div class="split-60-40">
        <div class="card surface" style="justify-content:center; align-items:center; gap:12px; padding:14px 16px;">
          <div class="card-top-bar bar-red"></div>
          <div style="display:flex; align-items:center; gap:10px; width:100%; background:#FFFFFF; border:1px solid #DADCE0; border-radius:11px; padding:7px 10px;">
            <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:40px; height:40px; border-radius:8px; object-fit:cover; border:2px solid #4285F4;"/>
            <img src="assets/P02/thumb_olaf.jpg" alt="Olaf" style="width:40px; height:40px; border-radius:8px; object-fit:cover; border:2px solid #34A853;"/>
            <img src="assets/P02/thumb_anna.jpg" alt="Anna" style="width:40px; height:40px; border-radius:8px; object-fit:cover; border:2px solid #EA4335;"/>
            <div style="font-size:11.6px; color:#3C4043; line-height:1.35;"><strong>Data Nyata Proyek ({total_imgs} Foto):</strong><br/>Bandingkan alur program aturan manual vs alur belajar Machine Learning!</div>
          </div>
          <div id="ml-diagram" style="width:100%; flex:1; display:flex; align-items:center;"></div>
        </div>
        <div class="card" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div>
            <span class="pill blue" id="ml-badge">ATURAN MANUAL</span>
            <div class="card-title" id="ml-title" style="margin-top:8px;">Manusia Menulis Semua Aturan</div>
          </div>
          <div class="card-body" id="ml-desc" style="font-size:13.5px;"></div>
          <div class="callout" id="ml-callout"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 10: DEEP LEARNING + SIMULATOR #2 (HIERARKI AI ⊃ ML ⊃ DL) -->
    <section class="slide" data-title="Bab 1: Deep Learning &amp; Peta AI ⊃ ML ⊃ DL" data-notes="Alokasi waktu: 1.5 menit. Deep Learning adalah cabang khusus Machine Learning yang memakai Neural Network berlapis banyak sehingga bisa mempelajari fitur langsung dari piksel mentah. Gunakan 3 tab sebagai recap cepat peta AI ⊃ ML ⊃ DL.">
      <div class="kicker">BAB 01 · SIMULATOR #2 · HIERARKI AI ⊃ ML ⊃ DL</div>
      <h2><span class="hl-green">Deep Learning (DL)</span> di Dalam Peta AI ⊃ ML ⊃ DL</h2>
      <div class="sim-bar pdf-keep-ui" id="vnn-tabs" style="margin-bottom:10px;">
        <button class="btn-ui outline" data-vnn="ai" onclick="setVnnMode('ai')">1. Recap: AI</button>
        <button class="btn-ui outline" data-vnn="ml" onclick="setVnnMode('ml')">2. Recap: ML</button>
        <button class="btn-ui" data-vnn="dl" onclick="setVnnMode('dl')">3. Deep Learning (DL) ← Proyek Kita</button>
      </div>
      <div class="split-40-60">
        <div class="canvas-box" style="justify-content:center;">
          <svg id="vnn-svg" viewBox="0 0 360 320" style="width:100%; max-height:310px;">
            <circle id="vnn-c-ai" cx="180" cy="160" r="148" fill="#E8F0FE" stroke="#4285F4" stroke-width="3" style="cursor:pointer;" onclick="setVnnMode('ai')"/>
            <text x="180" y="52" text-anchor="middle" font-family="Poppins" font-size="11.8" font-weight="700" fill="#1A73E8" style="pointer-events:none;">Artificial Intelligence (AI)</text>
            <circle id="vnn-c-ml" cx="180" cy="186" r="106" fill="#FCE8E6" stroke="#EA4335" stroke-width="3" style="cursor:pointer;" onclick="setVnnMode('ml')"/>
            <text x="180" y="122" text-anchor="middle" font-family="Poppins" font-size="10.8" font-weight="700" fill="#C5221F" style="pointer-events:none;">Machine Learning (ML)</text>
            <circle id="vnn-c-dl" cx="180" cy="214" r="62" fill="#E6F4EA" stroke="#34A853" stroke-width="3.5" style="cursor:pointer;" onclick="setVnnMode('dl')"/>
            <text x="180" y="207" text-anchor="middle" font-family="Poppins" font-size="12.2" font-weight="700" fill="#137333" style="pointer-events:none;">Deep Learning</text>
            <text x="180" y="225" text-anchor="middle" font-family="Roboto Mono" font-size="9.8" font-weight="700" fill="#137333" style="pointer-events:none;">(Neural Network)</text>
          </svg>
        </div>
        <div class="card surface" style="justify-content:space-between; gap:8px;">
          <div class="card-top-bar bar-green" id="vnn-bar"></div>
          <div>
            <span class="pill green" id="vnn-pill">DEEP LEARNING (DL)</span>
            <div class="card-title" id="vnn-title" style="margin-top:6px;">ML dengan Neural Network Berlapis Banyak</div>
          </div>
          <div id="vnn-illus" style="background:#FFFFFF; border:1px solid #DADCE0; border-radius:11px; padding:7px 10px;"></div>
          <div class="card-body" id="vnn-body" style="font-size:13px;"></div>
          <div class="mini-box" id="vnn-frozen" style="font-size:12px;"></div>
          <div class="callout green" id="vnn-callout" style="font-size:12.5px;"></div>
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
            vis_q_html='<div style="display:flex; gap:7px; justify-content:center; margin-bottom:10px;"><img src="assets/P02/thumb_anna.jpg" style="width:62px; height:62px; border-radius:10px; object-fit:cover; border:2px solid #EA4335;"/><img src="assets/P02/thumb_elsa.jpg" style="width:62px; height:62px; border-radius:10px; object-fit:cover; border:2px solid #4285F4;"/><img src="assets/P02/thumb_olaf.jpg" style="width:62px; height:62px; border-radius:10px; object-fit:cover; border:2px solid #34A853;"/></div><svg viewBox="0 0 220 120" style="width:205px; height:112px; display:block; margin:0 auto;"><circle cx="110" cy="60" r="54" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/><text x="110" y="23" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#1A73E8">AI</text><circle cx="110" cy="68" r="37" fill="#FCE8E6" stroke="#EA4335" stroke-width="2"/><text x="110" y="45" text-anchor="middle" font-family="Poppins" font-size="9.5" font-weight="700" fill="#C5221F">ML</text><circle cx="110" cy="77" r="21" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/><text x="110" y="81" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#137333">?</text></svg><div style="margin-top:6px; font-size:12.5px; color:#5F6368;">Foto Frozen masuk langsung ke Neural Network — di lapis mana posisinya?</div>',
            vis_a_html='<svg viewBox="0 0 220 130" style="width:210px; height:122px; display:block; margin:0 auto;"><circle cx="110" cy="65" r="58" fill="#E8F0FE" stroke="#4285F4" stroke-width="2" opacity="0.7"/><text x="110" y="24" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#1A73E8">AI</text><circle cx="110" cy="74" r="40" fill="#FCE8E6" stroke="#EA4335" stroke-width="2" opacity="0.8"/><text x="110" y="49" text-anchor="middle" font-family="Poppins" font-size="10" font-weight="700" fill="#C5221F">ML</text><circle cx="110" cy="84" r="24" fill="#34A853" stroke="#FFFFFF" stroke-width="2.5"/><text x="110" y="88" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#FFFFFF">DL ★</text></svg><div class="mini-box" style="margin-top:8px; background:#E6F4EA; border-color:#A8DAB5;"><strong>Tepat (DL ⊂ ML ⊂ AI)!</strong> Deep Learning langsung belajar fitur dari piksel mentah foto Frozen.</div>',
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
            kicker="BAB 02 · MENGENAL TUGAS VISI KOMPUTER",
            title="4 Task Utama Computer Vision",
            description="Computer Vision membuat komputer 'melihat' foto dan video — tetapi bentuk output-nya berbeda-beda tergantung jenis tugasnya.",
            footer_label=FOOTER,
            data_title="Bab 2 — 4 Task Computer Vision",
            notes="Alokasi waktu: 0.5 menit. Masuk Bab 2: mengenalkan 4 tugas utama Computer Vision memakai foto Frozen milik peserta sendiri sebagai satu contoh utuh.",
        )
    )

    s.append(
        f"""
    <!-- 12: 4 TASK PADA SATU FOTO (PETA VISUAL UTUH) -->
    <section class="slide" data-title="Bab 2: 4 Task CV pada Satu Foto" data-notes="Alokasi waktu: 2 menit. Tunjukkan keempat panel secara berdampingan pada foto asli Elsa agar peserta langsung menangkap beda bentuk output tiap task. Tegaskan bahwa kotak, mask, dan panah adalah ilustrasi buatan kode, bukan hasil model sungguhan.">
      <div class="kicker">BAB 02 · PETA PERBANDINGAN OUTPUT</div>
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
      <div class="kicker">BAB 02 · TASK 1 / 4</div>
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
      <div class="kicker">BAB 02 · TASK 2 / 4</div>
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
      <div class="kicker">BAB 02 · TASK 3 / 4</div>
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
      <div class="kicker">BAB 02 · TASK 4 / 4 · VIDEO</div>
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
            kicker="BAB 03 · INTI SESI (TERKECIL → TERBESAR)",
            title="Bedah Total: Neural Network",
            description="Kita rakit dari bagian paling kecil (1 Neuron) → Input Layer → Output Layer → hubungan tiap neuron → Hidden Layer → hitungan Forward Pass → cara belajar.",
            footer_label=FOOTER,
            data_title="Bab 3 — Bedah Neural Network",
            notes="Alokasi waktu: 0.5 menit. Bab 3 adalah bagian inti (27 menit). Kita susun pelan-pelan dari 1 neuron tunggal, lalu kumpulan neuron menjadi layer, sampai jaringan utuh dan cara belajarnya.",
        )
    )

    # 21: NEURON BIOLOGIS -> BUATAN
    s.append(
        f"""
    <!-- 20: DIMULAI DARI 1 NEURON (1 UNIT PEMEGANG 1 ANGKA PIKSEL) -->
    <section class="slide" data-title="Bab 3A: Dimulai dari 1 Neuron — 1 Unit Pemegang 1 Angka" data-notes="Alokasi waktu: 1.5 menit. Mulai dari bagian paling kecil dan paling konkret: 1 Neuron adalah 1 unit penyusun Neural Network yang memegang 1 nilai angka. Tunjuk gambar kanan: foto asli Elsa diperbesar jadi kotak piksel 8×8, lalu 1 kotak piksel (pada gaun Elsa) masuk menjadi tepat 1 lingkaran Neuron.">
      <div class="kicker">BAB 03A · LANGKAH 1 · BAGIAN PALING KECIL</div>
      <h2>Dimulai dari <span class="hl-green">1 Neuron</span>: 1 Unit Pemegang 1 Angka</h2>
      <div class="split-40-60" style="grid-template-columns:0.88fr 1.42fr;">
        <div class="card surface" style="justify-content:space-between; gap:10px; padding:16px 18px;">
          <div class="card-top-bar bar-green"></div>
          <div style="display:flex; flex-direction:column; gap:10px;">
            <div class="card-title">Apa Itu 1 Neuron?</div>
            <div class="mini-box" style="background:#E6F4EA; border-color:#A8DAB5; font-size:12.6px; line-height:1.48;">
              <strong>Definisi:</strong> <strong>Neuron</strong> (<em>Node</em>) adalah <strong>unit terkecil</strong> penyusun <em>Neural Network</em> yang memegang <strong>1 nilai angka</strong> (terinspirasi sel saraf otak).
            </div>
            <div class="card-body" style="font-size:12.8px; line-height:1.5;">
              <ul style="gap:7px;">
                <li><strong>Pada gambar:</strong> Foto terdiri dari banyak piksel bernilai <code>0.0–1.0</code>. Setiap <strong>1 nilai piksel</strong> diwakili oleh tepat <strong>1 Neuron</strong>!</li>
                <li><strong>Catatan akurat:</strong> Di lapisan paling depan, neuron hanya <em>memegang nilai piksel</em>. Di lapisan berikutnya, neuron akan <em>menghitung</em> angkanya dari neuron-neuron sebelumnya.</li>
              </ul>
            </div>
          </div>
          <div class="callout green" style="font-size:12px;"><strong>Langkah berikutnya:</strong> Karena 1 foto punya banyak piksel, mari kita susun semua neuron piksel tersebut ke bawah!</div>
        </div>
        <div class="card" style="align-items:center; justify-content:center; padding:14px 16px;">
          <div class="card-top-bar bar-blue"></div>
          <img src="assets/P02/03a_one_pixel_one_neuron.png" alt="Ilustrasi 1 piksel nyata foto Elsa diwakili oleh 1 Neuron" style="width:100%; height:auto; max-height:100%; object-fit:contain; border-radius:8px;"/>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 21: ANIMASI INTERAKTIF FLATTEN (KIRI->KANAN, ATAS->BAWAH -> INPUT LAYER) -->
    <section class="slide" data-title="Bab 3A: Animasi Flatten — Piksel Disusun ke Bawah Menjadi Input Layer" data-notes="Alokasi waktu: 1.5 menit. Klik tombol 'Putar Animasi' (atau '+1 Piksel' pelan-pelan) agar peserta melihat langsung tiap piksel foto Elsa dipindai dari kiri ke kanan, atas ke bawah, lalu terbang dan bertumpuk vertikal menjadi 1 kolom Input Layer berisi 9 neuron!">
      <div class="kicker">BAB 03A · LANGKAH 2 · ANIMASI INTERAKTIF FLATTEN</div>
      <h2>Neuron Disusun ke Bawah (<span class="hl-blue">Flatten</span>) = <span class="hl-green">Input Layer</span></h2>
      <div class="sim-bar pdf-keep-ui" id="flatten-ctrl" style="margin-bottom:7px; justify-content:space-between;">
        <div style="display:flex; flex-wrap:wrap; gap:6px; align-items:center;">
          <button class="btn-ui" id="flt-btn-play" onclick="playFlattenAnim()" style="padding:5px 12px; font-size:11.5px;">▶ Putar Animasi</button>
          <button class="btn-ui outline" id="flt-btn-step" onclick="stepFlattenAnim()" style="padding:5px 11px; font-size:11.5px;">⏭ +1 Piksel</button>
          <button class="btn-ui outline" id="flt-btn-reset" onclick="resetFlattenAnim()" style="padding:5px 11px; font-size:11.5px;">↺ Reset</button>
          <button class="btn-ui outline" id="flt-btn-done" onclick="completeFlattenAnim()" style="padding:5px 11px; font-size:11.5px;">✓ Semua (9/9)</button>
        </div>
        <span class="pill blue" id="flatten-status" style="font-size:11px;">Input Layer: 9 / 9 neuron (Selesai!)</span>
      </div>
      <div style="flex:1; min-height:0; display:grid; grid-template-columns:156px 1fr; gap:12px; align-items:center; background:#FFFFFF; border:1.5px solid #C6DAFC; border-radius:14px; padding:10px 14px; margin-bottom:8px;">
        <div style="display:flex; flex-direction:column; align-items:center; text-align:center; gap:6px; border-right:1px solid #E8EAED; padding-right:12px;">
          <img src="assets/P02/thumb_elsa.jpg" alt="Foto Asli Elsa" style="width:128px; height:128px; object-fit:cover; border-radius:11px; border:2.5px solid #4285F4; box-shadow:0 4px 12px rgba(66,133,244,0.14);"/>
          <div style="font-family:var(--font-title); font-size:12px; font-weight:700; color:#202124;">Foto Asli Elsa</div>
          <div style="font-size:10.3px; color:#5F6368; line-height:1.35;">Contoh mini <code>3×3</code> (9 piksel nyata) agar urutan pemindaian terlihat jelas.</div>
        </div>
        <div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; min-height:0;">
          <canvas id="flatten-canvas" width="760" height="314" style="width:100%; height:100%; max-height:314px; object-fit:contain; display:block;"></canvas>
        </div>
      </div>
      <div class="grid-3" style="flex:0 0 auto; gap:10px;">
        <div class="card tint-blue" style="padding:9px 12px; gap:3px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title" style="font-size:12.6px; color:#1A73E8;">1. Pindai Kiri → Kanan, Atas → Bawah</div>
          <div style="font-size:11.3px; color:#3C4043; line-height:1.38;">Mulai Baris 1 (<code>x₁, x₂, x₃</code>), lanjut Baris 2 (<code>x₄, x₅, x₆</code>), lalu Baris 3 (<code>x₇, x₈, x₉</code>).</div>
        </div>
        <div class="card tint-yellow" style="padding:9px 12px; gap:3px;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title" style="font-size:12.6px; color:#B06000;">2. Ubah &amp; Susun Bertumpuk (<em>Flatten</em>)</div>
          <div style="font-size:11.3px; color:#3C4043; line-height:1.38;">Setiap kotak piksel menjadi <strong>1 neuron</strong> lalu ditumpuk rapi vertikal dari atas ke bawah.</div>
        </div>
        <div class="card tint-green" style="padding:9px 12px; gap:3px;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title" style="font-size:12.6px; color:#137333;">3. Terbentuk <em>Input Layer</em></div>
          <div style="font-size:11.3px; color:#3C4043; line-height:1.38;">Kumpulan neuron dalam 1 kolom vertikal disebut <strong>Layer</strong> — lapisan pertama ini adalah <strong>Input Layer</strong>!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 22: INPUT LAYER SKALA FOTO BERWARNA (RGB) + SIMULATOR #3 -->
    <section class="slide" data-title="Bab 3A: Berapa Jumlah Neuron di Input Layer Foto Berwarna?" data-notes="Alokasi waktu: 2 menit. Lanjutkan dari contoh mini 3×3 (9 neuron) ke foto berwarna RGB: tiap 1 titik piksel warna punya 3 nilai (R, G, B), sehingga butuh 3 neuron input. Total neuron bertumpuk di Input Layer = Tinggi × Lebar × Channel. Coba klik 3 preset pada simulator.">
      <div class="kicker">BAB 03A · SIMULATOR #3 · MENGHITUNG NEURON INPUT LAYER</div>
      <h2><span class="hl-blue">Input Layer</span> Foto Berwarna: <code>Tinggi × Lebar × Channel</code></h2>
      <div class="split-40-60">
        <div class="card surface" style="justify-content:space-between; gap:10px; padding:16px 18px;">
          <div class="card-top-bar bar-blue"></div>
          <div style="display:flex; flex-direction:column; gap:10px;">
            <div class="card-title">Dari Hitam-Putih ke Foto Berwarna (RGB)</div>
            <div class="card-body" style="font-size:12.8px; line-height:1.48;">
              <ul style="gap:6px;">
                <li>Pada foto hitam-putih (1 channel), <code>1</code> piksel = <strong>1 neuron</strong>.</li>
                <li>Pada <strong>foto berwarna (RGB = 3 channel)</strong>, tiap <code>1</code> titik piksel punya 3 angka (<code>R, G, B</code>) → butuh <strong>3 neuron</strong>!</li>
                <li>Jadi jumlah neuron bertumpuk di <strong>Input Layer</strong> = <code>Tinggi × Lebar × Channel</code>.</li>
              </ul>
            </div>
            <div class="mini-box" style="background:#FFFFFF; display:flex; flex-direction:column; gap:9px; padding:11px 12px;">
              <div style="font-family:var(--font-title); font-size:11px; font-weight:700; color:#1A73E8;">COBA PRESET UKURAN FOTO:</div>
              <div class="sim-bar pdf-keep-ui" id="in-presets">
                <button class="btn-ui outline" data-in="28,28,1" onclick="setInSize(28,28,1,this)" style="padding:5px 9px; font-size:11px;">MNIST 28×28×1</button>
                <button class="btn-ui outline" data-in="64,64,3" onclick="setInSize(64,64,3,this)" style="padding:5px 9px; font-size:11px;">Frozen 64×64×3</button>
                <button class="btn-ui" data-in="224,224,3" onclick="setInSize(224,224,3,this)" style="padding:5px 9px; font-size:11px;">Frozen 224×224×3</button>
              </div>
              <div class="sim-slider-row"><span>Ukuran (H=W)</span><input id="in-hw" type="range" min="16" max="256" step="8" value="224" oninput="updateInCalc()"/><span class="sim-val" id="in-hw-v">224×224</span></div>
              <div class="sim-slider-row"><span>Channel (C)</span><input id="in-ch" type="range" min="1" max="3" step="2" value="3" oninput="updateInCalc()"/><span class="sim-val" id="in-ch-v">3 (RGB)</span></div>
            </div>
          </div>
          <div class="callout" style="font-size:11.8px;"><strong>Catatan:</strong> Dihitung dari ukuran <strong>1 foto</strong> setelah <em>resize</em> — bukan jumlah total file foto di folder dataset!</div>
        </div>
        <div class="card tint-blue" style="justify-content:space-between; text-align:center; padding:16px 18px; gap:10px;">
          <div class="card-top-bar bar-blue"></div>
          <!-- Visual 3-Channel RGB -> Stacked Column of Neurons -->
          <div style="background:#FFFFFF; border:1px solid #C6DAFC; border-radius:12px; padding:10px 12px;">
            <div style="font-family:var(--font-title); font-size:10px; font-weight:700; color:#5F6368; letter-spacing:0.05em; margin-bottom:6px;">3 CHANNEL WARNA (R, G, B) → DITUMPUK DALAM 1 INPUT LAYER</div>
            <svg viewBox="0 0 430 96" style="width:100%; height:92px; display:block;">
              <!-- 3 stacked RGB planes -->
              <rect x="14" y="10" width="64" height="50" rx="7" fill="#FCE8E6" stroke="#EA4335" stroke-width="2"/>
              <text x="46" y="32" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#C5221F">Red (R)</text>
              <text x="46" y="48" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#C5221F">H × W</text>

              <rect x="86" y="18" width="64" height="50" rx="7" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/>
              <text x="118" y="40" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#137333">Green (G)</text>
              <text x="118" y="56" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#137333">H × W</text>

              <rect x="158" y="26" width="64" height="50" rx="7" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
              <text x="190" y="48" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#1A73E8">Blue (B)</text>
              <text x="190" y="64" text-anchor="middle" font-family="Roboto Mono" font-size="9" fill="#1A73E8">H × W</text>

              <text x="118" y="90" text-anchor="middle" font-family="Roboto" font-size="9.5" fill="#5F6368">1 foto berwarna = 3 lapis matriks</text>

              <!-- Arrow -->
              <line x1="232" y1="46" x2="274" y2="46" stroke="#1A73E8" stroke-width="2.8"/>
              <polygon points="274,40 285,46 274,52" fill="#1A73E8"/>
              <text x="256" y="36" text-anchor="middle" font-family="Poppins" font-size="9.2" font-weight="700" fill="#1A73E8">Flatten</text>

              <!-- Stacked Input Layer neurons preview -->
              <rect x="294" y="6" width="124" height="84" rx="11" fill="#F8F9FA" stroke="#4285F4" stroke-width="2"/>
              <circle cx="314" cy="24" r="9" fill="#EA4335"/><text x="314" y="27" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" font-weight="700" fill="#FFF">R</text>
              <text x="330" y="27" font-family="Roboto Mono" font-size="9.2" fill="#202124">x₁ (Piksel R)</text>
              <circle cx="314" cy="48" r="9" fill="#34A853"/><text x="314" y="51" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" font-weight="700" fill="#FFF">G</text>
              <text x="330" y="51" font-family="Roboto Mono" font-size="9.2" fill="#202124">x₂ (Piksel G)</text>
              <circle cx="314" cy="72" r="9" fill="#4285F4"/><text x="314" y="75" text-anchor="middle" font-family="Roboto Mono" font-size="8.5" font-weight="700" fill="#FFF">B</text>
              <text x="330" y="75" font-family="Roboto Mono" font-size="9.2" fill="#202124">x₃ ... xₙ</text>
            </svg>
          </div>
          <div>
            <div style="font-size:12.2px; font-weight:700; color:#1A73E8; font-family:var(--font-title); margin-bottom:2px;">TOTAL NEURON BERTUMPUK DI INPUT LAYER (1 FOTO)</div>
            <div class="big-num hl-blue" id="in-total" style="font-size:clamp(36px,4.2vw,54px);">150.528</div>
          </div>
          <div class="formula-box" id="in-formula">224 (tinggi) × 224 (lebar) × 3 (R, G, B) = 150.528 neuron</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 23: SKALA NYATA FLATTEN FOTO ELSA -->
    <section class="slide" data-title="Bab 3A: Skala Nyata — Foto Elsa Di-Flatten Jadi 150.528 Neuron" data-notes="Alokasi waktu: 1 menit. Ini wujud skala nyata dari proses Flatten pada Slide 21–22 untuk foto asli Elsa ukuran 224×224×3: seluruh baris piksel diluruskan ke bawah menjadi satu kolom Input Layer sepanjang 150.528 neuron.">
      <div class="kicker">BAB 03A · LANGKAH 3 · SKALA NYATA FOTO FROZEN</div>
      <h2>Skala Nyata: Foto Elsa Di-<span class="hl-blue">Flatten</span> Jadi 150.528 Neuron</h2>
      <div class="img-box" style="height:auto; flex:1; min-height:0; padding:8px;">
        <img src="assets/P02/03_flatten_frozen_visual.png" alt="Foto Elsa 2D di-flatten jadi kolom neuron Input Layer 1D dan perbandingan jumlah neuron" style="width:100%; height:100%; max-height:365px; object-fit:contain;"/>
      </div>
      <div class="callout" style="margin-top:8px; flex:0 0 auto;"><strong>Inti visual:</strong> Setiap lingkaran di kolom <code>Input Layer</code> (<code>x₁, x₂, ..., x₁₅₀₅₂₈</code>) adalah <strong>1 neuron</strong> yang memegang tepat 1 angka warna (R/G/B) dari foto Elsa!</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 26: OUTPUT LAYER = JUMLAH KELAS -->
    <section class="slide" data-title="Bab 3B: Output Layer = Jumlah Kelas" data-notes="Alokasi waktu: 1 menit. Di ujung jaringan terdapat Output Layer. Khusus untuk Image Classification multi-kelas, jumlah neuron di Output Layer sama persis dengan jumlah kelas dataset kita (5 karakter Frozen).">
      <div class="kicker">BAB 03B · OUTPUT LAYER</div>
      <h2><span class="hl-green">Output Layer</span>: 1 Neuron untuk Setiap Kelas</h2>
      <div class="split-60-40">
        <div class="card surface" style="justify-content:center;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title" style="margin-bottom:6px;">5 Neuron Output untuk 5 Karakter Frozen</div>
          <div style="display:flex; flex-direction:column; gap:7px;">
            <div class="mini-box" style="display:flex; justify-content:space-between; align-items:center;"><span><strong>Neuron Output 1</strong> · <code>Anna</code></span><span class="pill blue">Skor Anna → %</span></div>
            <div class="mini-box" style="display:flex; justify-content:space-between; align-items:center; background:var(--tint-green); border-color:#A8DAB5;"><span><strong>Neuron Output 2</strong> · <code>Elsa</code></span><span class="pill green">Skor Elsa → %</span></div>
            <div class="mini-box" style="display:flex; justify-content:space-between; align-items:center;"><span><strong>Neuron Output 3</strong> · <code>Kristoff</code></span><span class="pill blue">Skor Kristoff → %</span></div>
            <div class="mini-box" style="display:flex; justify-content:space-between; align-items:center;"><span><strong>Neuron Output 4</strong> · <code>Olaf</code></span><span class="pill blue">Skor Olaf → %</span></div>
            <div class="mini-box" style="display:flex; justify-content:space-between; align-items:center;"><span><strong>Neuron Output 5</strong> · <code>Sven</code></span><span class="pill blue">Skor Sven → %</span></div>
          </div>
        </div>
        <div class="card" style="justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title">Penting: Kapan Output = Jumlah Kelas?</div>
          <div class="card-body" style="font-size:13.4px;">
            <ul>
              <li>Aturan <strong>1 neuron = 1 kelas</strong> berlaku untuk <strong>Image Classification multi-kelas</strong> (di proyek Frozen kita: tepat <strong>5 neuron output</strong>).</li>
              <li>Jika nanti dataset ditambah karakter ke-6 (misalnya <em>Hans</em>), kita cukup mengubah output layer menjadi <strong>6 neuron</strong>.</li>
              <li><strong>Jembatan Bab 2:</strong> Pada <em>Object Detection</em> dan <em>Segmentation</em>, bentuk output layer-nya berbeda (koordinat kotak atau peta piksel 2D).</li>
            </ul>
          </div>
          <div class="callout yellow"><strong>Pertanyaan berikutnya:</strong> Bagaimana 5 skor mentah (<em>logits</em>) diubah menjadi persentase 0–100%?</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 27: SOFTMAX + SIMULATOR #5 -->
    <section class="slide" data-title="Bab 3B: Softmax Mengubah Skor Jadi Probabilitas" data-notes="Alokasi waktu: 2 menit. Output mentah dari 5 neuron (logits) bisa positif maupun negatif. Fungsi Softmax mengubahnya menjadi probabilitas 0–100% yang jumlah totalnya selalu tepat 100%. Coba ketiga preset di simulator.">
      <div class="kicker">BAB 03B · SIMULATOR #4 · SOFTMAX OUTPUT LAYER</div>
      <h2><span class="hl-green">Softmax</span>: Mengubah 5 Skor Mentah Menjadi Probabilitas 100%</h2>
      <div class="sim-bar pdf-keep-ui" id="sm-presets" style="margin-bottom:8px;">
        <button class="btn-ui" data-smp="elsa" onclick="setSmPreset('elsa')">1. Yakin Elsa</button>
        <button class="btn-ui outline" data-smp="ragu" onclick="setSmPreset('ragu')">2. Ragu Elsa vs Anna</button>
        <button class="btn-ui outline" data-smp="neg" onclick="setSmPreset('neg')">3. Semua Skor Negatif</button>
      </div>
      <div class="split-40-60">
        <div class="card surface" style="gap:7px; padding:13px 15px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title" style="font-size:14.5px;">Geser Skor Mentah (<em>Logits</em>)</div>
          <div class="sim-slider-row"><span>Anna</span><input id="sm-0" type="range" min="-4" max="5" step="0.2" value="0.8" oninput="updateSm()"/><span class="sim-val" id="sm-v0">+0.8</span></div>
          <div class="sim-slider-row"><span>Elsa</span><input id="sm-1" type="range" min="-4" max="5" step="0.2" value="3.2" oninput="updateSm()"/><span class="sim-val" id="sm-v1">+3.2</span></div>
          <div class="sim-slider-row"><span>Kristoff</span><input id="sm-2" type="range" min="-4" max="5" step="0.2" value="-0.6" oninput="updateSm()"/><span class="sim-val" id="sm-v2">-0.6</span></div>
          <div class="sim-slider-row"><span>Olaf</span><input id="sm-3" type="range" min="-4" max="5" step="0.2" value="0.2" oninput="updateSm()"/><span class="sim-val" id="sm-v3">+0.2</span></div>
          <div class="sim-slider-row"><span>Sven</span><input id="sm-4" type="range" min="-4" max="5" step="0.2" value="-1.0" oninput="updateSm()"/><span class="sim-val" id="sm-v4">-1.0</span></div>
          <div class="mini-box" style="font-size:11.6px;"><strong>Cara kerja ringkas:</strong> Tiap skor dipangkatkan (<code>eᶻ</code>) agar semua positif, lalu dibagi jumlah totalnya.</div>
        </div>
        <div class="card" style="gap:8px; padding:13px 15px; justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="card-title" style="font-size:14.5px;">Hasil Probabilitas Softmax</span>
            <span class="pill green" id="sm-sum-pill">Total = 100.0%</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:7px;">
            <div class="prob-row"><strong>Anna</strong><div class="prob-track"><div id="sm-b0" class="prob-fill" style="background:#4285F4;"></div></div><span id="sm-e0" style="font-family:var(--font-code); color:#5F6368; text-align:right;">2.2</span><strong id="sm-p0" style="text-align:right;">0%</strong></div>
            <div class="prob-row"><strong>Elsa</strong><div class="prob-track"><div id="sm-b1" class="prob-fill" style="background:#34A853;"></div></div><span id="sm-e1" style="font-family:var(--font-code); color:#5F6368; text-align:right;">24.5</span><strong id="sm-p1" style="text-align:right;">0%</strong></div>
            <div class="prob-row"><strong>Kristoff</strong><div class="prob-track"><div id="sm-b2" class="prob-fill" style="background:#FBBC04;"></div></div><span id="sm-e2" style="font-family:var(--font-code); color:#5F6368; text-align:right;">0.5</span><strong id="sm-p2" style="text-align:right;">0%</strong></div>
            <div class="prob-row"><strong>Olaf</strong><div class="prob-track"><div id="sm-b3" class="prob-fill" style="background:#EA4335;"></div></div><span id="sm-e3" style="font-family:var(--font-code); color:#5F6368; text-align:right;">1.2</span><strong id="sm-p3" style="text-align:right;">0%</strong></div>
            <div class="prob-row"><strong>Sven</strong><div class="prob-track"><div id="sm-b4" class="prob-fill" style="background:#5F6368;"></div></div><span id="sm-e4" style="font-family:var(--font-code); color:#5F6368; text-align:right;">0.4</span><strong id="sm-p4" style="text-align:right;">0%</strong></div>
          </div>
          <div class="callout green" id="sm-winner"></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 28: SATU NEURON INPUT KE SEMUA NEURON OUTPUT + SIMULATOR #6 -->
    <section class="slide" data-title="Bab 3C: Koneksi 1 Neuron Input ke 5 Neuron Output" data-notes="Alokasi waktu: 1.5 menit. Ini visual inti permintaan desain kita: telusuri tepat 1 neuron dari Input Layer ke seluruh 5 neuron Output Layer. Klik tombol neuron input x1, x2, x3, atau x4 untuk menyorot 5 garis weight miliknya!">
      <div class="kicker">BAB 03C · SIMULATOR #5 · MEMBEDAH KONEKSI (FULLY CONNECTED)</div>
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
      <div class="kicker">BAB 03C · HITUNGAN LANGSUNG (TANPA HIDDEN LAYER)</div>
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
      <div class="kicker">BAB 03D · HIDDEN LAYER</div>
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
      <div class="kicker">BAB 03D · GAMBAR UTUH NEURAL NETWORK</div>
      <h2>Arsitektur Utuh <span class="hl-blue">Multi-Layer Perceptron (MLP)</span></h2>
      <div class="card surface" style="flex:1; align-items:center; justify-content:center; padding:12px;">
        <svg viewBox="0 0 820 310" style="width:100%; max-height:360px;">
          <!-- Layer boxes -->
          <rect x="20" y="18" width="165" height="270" rx="16" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
          <text x="102" y="42" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#1A73E8">Input Layer</text>
          <text x="102" y="59" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" fill="#5F6368">150.528 neuron piksel</text>

          <rect x="275" y="18" width="210" height="270" rx="16" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
          <text x="380" y="42" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#B06000">Hidden Layer (+ ReLU)</text>
          <text x="380" y="59" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" fill="#5F6368">mis. 128 neuron pengolah pola</text>

          <rect x="575" y="18" width="225" height="270" rx="16" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/>
          <text x="687" y="42" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#137333">Output Layer (+ Softmax)</text>
          <text x="687" y="59" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" fill="#5F6368">5 neuron kelas Frozen</text>

          <!-- Connections -->
          <g stroke="#9AA0A6" stroke-width="1.3" opacity="0.65">
            <line x1="120" y1="95" x2="362" y2="95"/><line x1="120" y1="95" x2="362" y2="155"/><line x1="120" y1="95" x2="362" y2="215"/>
            <line x1="120" y1="155" x2="362" y2="95"/><line x1="120" y1="155" x2="362" y2="155"/><line x1="120" y1="155" x2="362" y2="215"/>
            <line x1="120" y1="215" x2="362" y2="95"/><line x1="120" y1="215" x2="362" y2="155"/><line x1="120" y1="215" x2="362" y2="215"/>
            <line x1="398" y1="95" x2="620" y2="90"/><line x1="398" y1="95" x2="620" y2="132"/><line x1="398" y1="95" x2="620" y2="174"/><line x1="398" y1="95" x2="620" y2="216"/><line x1="398" y1="95" x2="620" y2="258"/>
            <line x1="398" y1="155" x2="620" y2="90"/><line x1="398" y1="155" x2="620" y2="132"/><line x1="398" y1="155" x2="620" y2="174"/><line x1="398" y1="155" x2="620" y2="216"/><line x1="398" y1="155" x2="620" y2="258"/>
            <line x1="398" y1="215" x2="620" y2="90"/><line x1="398" y1="215" x2="620" y2="132"/><line x1="398" y1="215" x2="620" y2="174"/><line x1="398" y1="215" x2="620" y2="216"/><line x1="398" y1="215" x2="620" y2="258"/>
          </g>

          <!-- Input nodes -->
          <circle cx="102" cy="95" r="18" fill="#4285F4" stroke="#FFF" stroke-width="3"/><text x="102" y="99" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#FFF">x₁</text>
          <circle cx="102" cy="155" r="18" fill="#4285F4" stroke="#FFF" stroke-width="3"/><text x="102" y="159" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#FFF">x₂</text>
          <circle cx="102" cy="215" r="18" fill="#4285F4" stroke="#FFF" stroke-width="3"/><text x="102" y="219" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#FFF">xₙ</text>
          <text x="102" y="264" text-anchor="middle" font-family="Roboto" font-size="11" fill="#1A73E8">Piksel 0.0–1.0</text>

          <!-- Hidden nodes -->
          <circle cx="380" cy="95" r="19" fill="#FBBC04" stroke="#FFF" stroke-width="3"/><text x="380" y="99" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#202124">h₁</text>
          <circle cx="380" cy="155" r="19" fill="#EA4335" stroke="#FFF" stroke-width="3"/><text x="380" y="159" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#FFF">h₂</text>
          <circle cx="380" cy="215" r="19" fill="#FBBC04" stroke="#FFF" stroke-width="3"/><text x="380" y="219" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#202124">hₘ</text>
          <text x="380" y="264" text-anchor="middle" font-family="Roboto" font-size="11" fill="#B06000">W₁·x + b₁ → ReLU</text>

          <!-- Output nodes -->
          <circle cx="635" cy="90" r="13" fill="#34A853" stroke="#FFF" stroke-width="2.5"/><text x="660" y="94" font-family="Poppins" font-size="11.5" font-weight="700" fill="#202124">Anna</text>
          <circle cx="635" cy="132" r="13" fill="#34A853" stroke="#FFF" stroke-width="2.5"/><text x="660" y="136" font-family="Poppins" font-size="11.5" font-weight="700" fill="#137333">Elsa ★</text>
          <circle cx="635" cy="174" r="13" fill="#34A853" stroke="#FFF" stroke-width="2.5"/><text x="660" y="178" font-family="Poppins" font-size="11.5" font-weight="700" fill="#202124">Kristoff</text>
          <circle cx="635" cy="216" r="13" fill="#34A853" stroke="#FFF" stroke-width="2.5"/><text x="660" y="220" font-family="Poppins" font-size="11.5" font-weight="700" fill="#202124">Olaf</text>
          <circle cx="635" cy="258" r="13" fill="#34A853" stroke="#FFF" stroke-width="2.5"/><text x="660" y="262" font-family="Poppins" font-size="11.5" font-weight="700" fill="#202124">Sven</text>

          <!-- Labels on weights -->
          <rect x="200" y="246" width="60" height="22" rx="6" fill="#FFFFFF" stroke="#DADCE0"/>
          <text x="230" y="261" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#EA4335">W₁, b₁</text>
          <rect x="498" y="246" width="60" height="22" rx="6" fill="#FFFFFF" stroke="#DADCE0"/>
          <text x="528" y="261" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#137333">W₂, b₂</text>
        </svg>
      </div>
      <div class="callout" style="margin-top:8px;"><strong>Alur dari kiri ke kanan:</strong> Setiap data mengalir maju melewati perkalian bobot + bias + fungsi aktivasi. Proses maju ini disebut <strong>Forward Pass</strong>.</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 32: HITUNG PARAMETER DENGAN HIDDEN LAYER + SIMULATOR #7 -->
    <section class="slide" data-title="Bab 3D: Simulator Hitung Parameter dengan Hidden Layer" data-notes="Alokasi waktu: 1.5 menit. Momen 'aha' penting! Geser jumlah neuron di Hidden Layer dan perhatikan bagaimana total parameter pada foto 224×224×3 langsung melonjak ke 19.268.357 (sekitar 19,3 juta) saat hidden=128.">
      <div class="kicker">BAB 03D · SIMULATOR #6 · KALKULATOR PARAMETER MLP</div>
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
          <div class="big-num hl-red" id="hid-total" style="font-size:clamp(34px,4vw,52px);">19.268.357</div>
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
      <div class="kicker">BAB 03D · SIMULATOR #7 · MATEMATIKA RINGAN &amp; AKURAT</div>
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
            kicker="BAB 03D · TANYA-JAWAB #4",
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
      <div class="kicker">BAB 03E · BAGAIMANA NETWORK BELAJAR (1/4)</div>
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
    <section class="slide" data-title="Bab 3E: Gradient Descent &amp; Simulator Learning Rate" data-notes="Alokasi waktu: 2 menit. Gradient Descent ibarat menuruni bukit berkabut dengan melangkah ke arah paling miring ke bawah. Besar langkahnya disebut Learning Rate. Klik 3 preset (Kecil, Ideal, Besar) untuk melihat dampaknya.">
      <div class="kicker">BAB 03E · SIMULATOR #8 · GRADIENT DESCENT</div>
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
      <div class="kicker">BAB 03E · BAGAIMANA NETWORK BELAJAR (3/4)</div>
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
      <div class="kicker">BAB 03E · BAGAIMANA NETWORK BELAJAR (4/4)</div>
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
      <div class="kicker">BAB 03 · RANGKUMAN HIERARKI</div>
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
    <section class="slide" data-title="Bab 4: Mengapa MLP Tidak Cukup untuk Gambar?" data-notes="Alokasi waktu: 1.5 menit. Tunjukkan dua alasan kuat dari hasil Bab 3 tadi: (1) ledakan 19,27 juta parameter di 1 layer saja, dan (2) Flatten merusak tetangga piksel 2D sehingga sangat peka jika objek bergeser sedikit.">
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
    <section class="slide" data-title="Bab 4: Peta Evolusi Arsitektur CV (Simulator)" data-notes="Alokasi waktu: 2 menit. Klik keempat kartu secara berurutan (MLP -> CNN -> ResNet -> MobileNet) untuk menjelaskan ide inti tiap generasi secara konseptual tanpa detail internal yang berat. Detailnya akan dipelajari di P03 dan P04.">
      <div class="kicker">BAB 04 · SIMULATOR #9 · PETA EVOLUSI ARSITEKTUR</div>
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
    <section class="slide" data-title="Bab 4: Arsitektur per Task CV &amp; Pilihan MobileNetV2" data-notes="Alokasi waktu: 1 menit. Hubungkan Bab 2 (4 Task CV) dengan Bab 4 (Arsitektur): tiap task punya keluarga arsitektur populer, tetapi semuanya sering memakai CNN backbone yang mirip! Untuk proyek kita dipilih MobileNetV2.">
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

    # 45: Q&A REVEAL #6 (BAB 4)
    s.append(
        _qa_slide(
            qa_id="qa-bab4",
            qa_num=6,
            kicker="BAB 04 · TANYA-JAWAB #6",
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
    # ISTIRAHAT (SLIDE 46 · 5.0 MENIT)
    # =========================================================================
    s.append(
        make_divider_slide(
            bg_class="bg-blue",
            kicker="BAB 05 · ISTIRAHAT 5 MENIT → HANDS-ON NOTEBOOK",
            title="Istirahat 5 Menit",
            description="Minum air, regangkan mata & tangan sejenak. Setelah jeda, kita buka notebook P02_computer_vision_101.ipynb dan praktik 6 langkah santai pada foto Frozen!",
            footer_label=FOOTER,
            data_title="Istirahat 5 Menit & Masuk Bab 5",
            notes="Alokasi waktu: 5 menit. Berikan jeda istirahat penuh 5 menit. Siapkan browser Google Colab atau Jupyter lokal untuk membuka materials/P02/P02_computer_vision_101.ipynb.",
        )
    )

    # =========================================================================
    # BAB 5: 6 LANGKAH HANDS-ON (SLIDE 47–52 · 45.0 MENIT)
    # =========================================================================
    s.append(
        _handson_step_slide(
            step_num=1,
            title="Setup 3 Tahap & Baca Data Frozen Dinamis",
            kicker="BAB 05 · HANDS-ON (7 MENIT)",
            goal_html="Menyiapkan library, kunci <code>SEED = 42</code>, dan membaca <code>metadata.csv</code>",
            bullets_html="""
              <li>Jalankan <strong>Setup 1/3, 2/3, 3/3</strong> untuk memuat NumPy, Pandas, Matplotlib, TensorFlow, serta mendeteksi folder <code>DATA_DIR</code> otomatis.</li>
              <li>Baca tabel <code>metadata.csv</code> secara <strong>dinamis</strong> (tanpa meng-hardcode jumlah foto).</li>
              <li>Tampilkan 5 contoh foto nyata karakter Frozen (<code>anna, elsa, kristoff, olaf, sven</code>).</li>
            """,
            code_snippet="""# Setup 3/3 + baca metadata dinamis (Langkah 1)
df_meta = pd.read_csv(DATA_DIR / "metadata.csv")
print("Total foto tersedia :", len(df_meta))
print(pd.crosstab(df_meta["kelas"], df_meta["kondisi"]))""",
            callout_html="<strong>Target Langkah 1:</strong> Semua setup hijau tanpa error dan galeri 5 karakter Frozen muncul di layar.",
            color="blue",
            notes="Alokasi waktu: 7 menit. Pandu peserta menjalankan Setup 1/3 sampai 3/3 dan membaca metadata.csv secara dinamis. Pastikan Colab/lokal menemukan folder data/frozen_v1/.",
        )
    )

    s.append(
        _handson_step_slide(
            step_num=2,
            title="Flatten Foto & Hitung Neuron Input Layer",
            kicker="BAB 05 · HANDS-ON (7 MENIT)",
            goal_html="Mengubah foto 2D/3D menjadi vektor 1D dan menghitung neuron input",
            bullets_html="""
              <li>Buka 1 foto asli Elsa, ubah ukurannya ke <code>(64, 64, 3)</code> dan <code>(224, 224, 3)</code>, lalu normalisasi ke <code>0.0–1.0</code>.</li>
              <li>Lakukan <code>.flatten()</code> di NumPy dan buktikan panjang vektornya tepat sama dengan <code>H × W × C</code>.</li>
              <li>Kerjakan <strong># TODO 1</strong> &amp; <strong># TODO 2</strong> untuk mengecek jumlah neuron input dan estimasi weight tanpa hidden layer.</li>
            """,
            code_snippet="""# Ubah foto jadi array normalisasi lalu flatten
arr_64 = np.array(img_64, dtype=np.float32) / 255.0
vektor_input = arr_64.flatten()
print("Shape 3D      :", arr_64.shape)
print("Neuron Input  :", len(vektor_input))  # 12.288""",
            callout_html="<strong>Target Langkah 2:</strong> Melihat langsung hubungan antara <code>shape (H, W, C)</code> dengan jumlah neuron di <em>Input Layer</em>.",
            color="green",
            notes="Alokasi waktu: 7 menit. Pandu peserta menyelesaikan TODO 1 & TODO 2 tentang flatten dan hitungan neuron input layer. Cocokkan angkanya dengan Slide 23–24.",
        )
    )

    s.append(
        _handson_step_slide(
            step_num=3,
            title="Forward Pass Manual dengan NumPy",
            kicker="BAB 05 · HANDS-ON (7 MENIT)",
            goal_html="Menulis sendiri hitungan 1 neuron, <code>ReLU</code>, <code>Softmax</code>, dan 4-piksel Forward Pass",
            bullets_html="""
              <li>Kerjakan <strong># TODO 3</strong>: hitung <code>z = np.dot(x, w) + b</code> dan fungsi <code>relu(z)</code>.</li>
              <li>Kerjakan <strong># TODO 4</strong>: buat <code>softmax_manual(logits)</code> dan buktikan jumlah probabilitasnya selalu <code>1.0</code>.</li>
              <li>Jalankan ulang contoh <strong>4 piksel nyata Elsa</strong> (Slide 32) di NumPy dan cocokkan hasilnya!</li>
            """,
            code_snippet="""# Forward Pass 2 layer di NumPy (Langkah 3)
z1 = x_4px @ W1 + b1
h1 = np.maximum(0.0, z1)        # ReLU di Hidden
logits = h1 @ W2 + b2           # Skor Output
probs = softmax_manual(logits)  # Probabilitas 100%""",
            callout_html="<strong>Target Langkah 3:</strong> Semua <code>assert</code> lolos dan peserta melihat bahwa Forward Pass hanyalah perkalian matriks + aktivasi.",
            color="red",
            notes="Alokasi waktu: 7 menit. Minta peserta melengkapi TODO 3 & TODO 4. Jika mentok >2 menit, boleh mengintip tombol dropdown Hint di bawah sel.",
        )
    )

    s.append(
        _handson_step_slide(
            step_num=4,
            title="Bangun MLP Kecil dengan Keras",
            kicker="BAB 05 · HANDS-ON (7 MENIT)",
            goal_html="Menyusun arsitektur <code>Input → Flatten → Dense(ReLU) → Dense(Softmax)</code>",
            bullets_html="""
              <li>Muat foto Frozen ke ukuran ringkas <code>64×64×3</code> (agar RAM aman &amp; cepat dilatih di kelas).</li>
              <li>Kerjakan <strong># TODO 5</strong>: susun model <code>tf.keras.Sequential</code> dengan <code>Dense(64, activation="relu")</code> dan <code>Dense(len(CLASS_NAMES), activation="softmax")</code>.</li>
              <li><em>Compile</em> model memakai <code>Adam(learning_rate=0.001)</code> dan <code>sparse_categorical_crossentropy</code>.</li>
            """,
            code_snippet="""# Bangun MLP kecil di Keras (Langkah 4)
mlp = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(64, 64, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax"),
])""",
            callout_html="<strong>Catatan jujur:</strong> MLP ini hanya untuk <strong>demo konsep</strong> (bukan model final) — jembatan menuju CNN di P03!",
            color="yellow",
            notes="Alokasi waktu: 7 menit. Jelaskan kaitan tiap baris Sequential dengan diagram Bab 3 (Input -> Flatten -> Hidden ReLU -> Output Softmax).",
        )
    )

    s.append(
        _handson_step_slide(
            step_num=5,
            title="Latih MLP Sebentar & Plot Kurva Loss",
            kicker="BAB 05 · HANDS-ON (7 MENIT)",
            goal_html="Menjalankan <code>model.fit()</code> dan mengamati penurunan nilai <em>Loss</em>",
            bullets_html="""
              <li>Kerjakan <strong># TODO 6</strong>: latih model beberapa epoch pada foto Frozen (<code>2</code> epoch saat <code>SMOKE_TEST=1</code>, <code>8</code> epoch di kelas).</li>
              <li>Plot grafik <strong>Training Loss</strong> tiap epoch dan simpan ke <code>results/p02_mlp_loss_curve.png</code>.</li>
              <li>Diskusikan secara jujur mengapa MLP sederhana cepat kewalahan pada foto berlatar ramai.</li>
            """,
            code_snippet="""# Latih singkat & plot kurva Loss (Langkah 5)
history = mlp.fit(
    X_frozen, y_frozen,
    epochs=2 if SMOKE_TEST else 8,
    batch_size=16, verbose=1,
)
plt.plot(history.history["loss"], marker="o")""",
            callout_html="<strong>Ingat metodologi:</strong> Pembagian data <em>train/val/test</em> resmi bebas <em>leakage</em> (Group Split) akan kita pelajari tuntas di <strong>P05</strong>.",
            color="blue",
            notes="Alokasi waktu: 7 menit. Jalankan training demo singkat dan tunjukkan grafik Loss yang turun. Jangan mengklaim akurasi tinggi — fokus pada konsep Loss turun dan keterbatasan MLP.",
        )
    )

    s.append(
        _handson_step_slide(
            step_num=6,
            title="Cek model.summary() vs Hitungan Tangan",
            kicker="BAB 05 · HANDS-ON (7 MENIT)",
            goal_html="Membuktikan rumus <code>(Input × Output) + Bias</code> cocok 100% dengan Keras",
            bullets_html="""
              <li>Panggil <code>mlp.summary()</code> dan baca kolom <code>Param #</code> di setiap layer.</li>
              <li>Kerjakan <strong># TODO 7</strong>: hitung manual <code>param_l1 = (12288 * 64) + 64</code> dan <code>param_l2 = (64 * 5) + 5</code>, lalu buktikan cocok dengan <code>mlp.count_params()</code>!</li>
              <li>Bandingkan juga dengan estimasi jika input dibesarkan ke <code>224×224×3</code> (<strong>19,27 juta</strong> parameter!).</li>
            """,
            code_snippet="""# Cocokkan hitungan tangan vs Keras (Langkah 6)
mlp.summary()
hitung_manual = (64*64*3 * 64 + 64) + (64 * 5 + 5)
print("Hitungan manual :", f"{hitung_manual:,}")
print("Keras count     :", f"{mlp.count_params():,}")
assert hitung_manual == mlp.count_params()""",
            callout_html="<strong>Momen Aha:</strong> Angka di <code>model.summary()</code> bukan angka misterius — kamu sekarang tahu persis asal setiap parameternya!",
            color="green",
            notes="Alokasi waktu: 7 menit. Pastikan peserta melihat assert hitung_manual == mlp.count_params() lolos. Ini mengunci seluruh pemahaman Bab 3 dan Bab 4.",
        )
    )

    # =========================================================================
    # MINI-CHALLENGE (SLIDE 53 · 5.0 MENIT)
    # =========================================================================
    s.append(
        f"""
    <!-- 53: MINI-CHALLENGE -->
    <section class="slide" data-title="Mini-Challenge: Ubah Jumlah Neuron Hidden Layer" data-notes="Alokasi waktu: 5 menit. Ajak peserta menebak dulu sebelum menjalankan sel Mini-Challenge di notebook: apa dampak mengubah hidden neuron dari 32 ke 64 lalu 128 terhadap jumlah parameter dan kurva Loss?">
      <div class="kicker">BAB 05 · MINI-CHALLENGE (5 MENIT)</div>
      <h2>Mini-Challenge: <span class="hl-red">32 vs 64 vs 128 Neuron Hidden</span></h2>
      <div class="split-60-40">
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title">Tebak Dulu Sebelum Menjalankan Sel Terakhir!</div>
          <div class="card-body">
            <ul>
              <li>Di notebook bagian Mini-Challenge, kita membuat 3 MLP untuk foto Frozen <code>64×64×3</code> dengan ukuran <strong>Hidden Layer</strong> berbeda: <code>32</code>, <code>64</code>, dan <code>128</code> neuron.</li>
              <li><strong>Pertanyaan 1:</strong> Jika neuron hidden naik <code>2×</code> (dari <code>64</code> ke <code>128</code>), kira-kira berapa kali lipat jumlah parameternya naik?</li>
              <li><strong>Pertanyaan 2:</strong> Apakah jumlah parameter yang jauh lebih besar otomatis membuat model lebih bagus di foto baru?</li>
            </ul>
          </div>
          <div class="callout red"><strong>Kerjakan di Notebook:</strong> Lengkapi <code># TODO 8</code> di bagian Mini-Challenge dan simpan tabel perbandingannya ke <code>results/p02_hidden_experiment.csv</code>!</div>
        </div>
        <div class="card tint-yellow" style="justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title">Patokan Prediksi Cepat (64×64×3)</div>
          <table class="io-table" style="font-size:12.5px;">
            <thead><tr><th>Hidden</th><th>Total Parameter</th><th>Rasio</th></tr></thead>
            <tbody>
              <tr><td><strong>32 neuron</strong></td><td><code>393.413</code></td><td><code>0.5×</code></td></tr>
              <tr><td><strong>64 neuron</strong></td><td><code>786.821</code></td><td><code>1.0×</code></td></tr>
              <tr><td><strong>128 neuron</strong></td><td><code>1.573.637</code></td><td><code>2.0×</code></td></tr>
            </tbody>
          </table>
          <div class="mini-box"><strong>Poin diskusi:</strong> Menambah neuron memperbesar kapasitas, tetapi pada dataset kecil juga meningkatkan risiko menghafal data latih (<em>overfitting</em>) &amp; membuat training lebih berat!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 54: KAMUS ISTILAH -->
    <section class="slide" data-title="Kamus Istilah Santai P02" data-notes="Alokasi waktu: 2 menit. Ulas singkat 12 istilah asli yang kita pakai sepanjang sesi dengan penjelasan sederhana dalam bahasa sehari-hari.">
      <div class="kicker">BAB 05 · GLOSARIUM RINGKAS</div>
      <h2>Kamus Istilah <span class="hl-blue">Computer Vision 101</span></h2>
      <div class="glossary-grid">
        <div class="gloss-card"><div class="gloss-term">AI / ML / DL</div><div class="gloss-def">Hierarki subset: AI (bidang luas) ⊃ ML (belajar dari data) ⊃ DL (memakai Neural Network berlapis).</div></div>
        <div class="gloss-card"><div class="gloss-term">Image Classification</div><div class="gloss-def">Memberi 1 label kategori (dan probabilitas) pada keseluruhan foto.</div></div>
        <div class="gloss-card"><div class="gloss-term">Object Detection</div><div class="gloss-def">Mencari banyak objek dalam 1 foto dengan kotak <em>bounding box</em> + label.</div></div>
        <div class="gloss-card"><div class="gloss-term">Semantic &amp; Instance Segmentation</div><div class="gloss-def">Memetakan bentuk per piksel (<em>mask</em>): <em>Semantic</em> per kelas, <em>Instance</em> memisahkan tiap individu objek.</div></div>
        <div class="gloss-card"><div class="gloss-term">Object Tracking</div><div class="gloss-def">Mendeteksi dan mempertahankan ID objek yang sama antar-frame pada video.</div></div>
        <div class="gloss-card"><div class="gloss-term">Neuron, Weight &amp; Bias</div><div class="gloss-def">Unit hitung terkecil: input dikali bobot (<em>weight</em>) ditambah ambang (<em>bias</em>).</div></div>
        <div class="gloss-card"><div class="gloss-term">Input / Hidden / Output Layer</div><div class="gloss-def">Layer penerima piksel (<code>H×W×C</code>), layer pengolah pola di tengah, dan layer prediksi kelas.</div></div>
        <div class="gloss-card"><div class="gloss-term">ReLU &amp; Softmax</div><div class="gloss-def"><code>ReLU</code>: negatif jadi 0 di hidden layer. <code>Softmax</code>: skor jadi probabilitas total 100%.</div></div>
        <div class="gloss-card"><div class="gloss-term">Forward Pass</div><div class="gloss-def">Aliran perhitungan maju dari piksel foto hingga keluar probabilitas prediksi.</div></div>
        <div class="gloss-card"><div class="gloss-term">Loss Function</div><div class="gloss-def">Skor hukuman seberapa jauh tebakan model dari label asli (makin kecil makin baik).</div></div>
        <div class="gloss-card"><div class="gloss-term">Gradient Descent &amp; Backprop</div><div class="gloss-def">Cara model mencari arah salah dan menggeser bobot turun menuju Loss terkecil.</div></div>
        <div class="gloss-card"><div class="gloss-term">MLP vs CNN</div><div class="gloss-def">MLP meluruskan foto (boros bobot); CNN memakai filter 2D yang hemat dan tahan geser.</div></div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 55: KUIS INTERAKTIF 5 SOAL -->
    <section class="slide" data-title="Kuis Interaktif 5 Soal" data-notes="Alokasi waktu: 4 menit. Minta peserta menjawab kelima soal secara lisan terlebih dahulu sebelum membuka tombol jawaban satu per satu.">
      <div class="kicker">BAB 05 · EVALUASI CEPAT (5 SOAL)</div>
      <h2>Kuis Interaktif <span class="hl-red">5 Soal</span></h2>
      <div class="quiz-grid-compact">
        <div class="quiz-item compact">
          <div class="q-txt">1. Apa hubungan antara AI, Machine Learning (ML), dan Deep Learning (DL)?</div>
          <button class="btn-ui outline" onclick="toggleAns('q1', this)">Lihat Jawaban</button>
          <div id="q1" class="quiz-ans"><strong>Jawab:</strong> Hierarki subset <code>AI ⊃ ML ⊃ DL</code>. DL adalah bagian dari ML yang memakai Neural Network berlapis banyak.</div>
        </div>
        <div class="quiz-item compact">
          <div class="q-txt">2. Apa beda utama <em>Image Classification</em> dan <em>Object Detection</em>?</div>
          <button class="btn-ui outline" onclick="toggleAns('q2', this)">Lihat Jawaban</button>
          <div id="q2" class="quiz-ans"><strong>Jawab:</strong> Classification memberi 1 label untuk seluruh foto; Detection mencari banyak objek sekaligus beserta kotak lokasinya.</div>
        </div>
        <div class="quiz-item compact">
          <div class="q-txt">3. Jika foto berukuran <code>100×100×3</code>, berapa jumlah neuron di <em>Input Layer</em>?</div>
          <button class="btn-ui outline" onclick="toggleAns('q3', this)">Lihat Jawaban</button>
          <div id="q3" class="quiz-ans"><strong>Jawab:</strong> <code>100 × 100 × 3 = 30.000</code> neuron input (1 neuron per nilai piksel pada 1 gambar).</div>
        </div>
        <div class="quiz-item compact">
          <div class="q-txt">4. Mengapa di <em>Output Layer</em> klasifikasi 5 karakter Frozen kita memakai <code>Softmax</code>?</div>
          <button class="btn-ui outline" onclick="toggleAns('q4', this)">Lihat Jawaban</button>
          <div id="q4" class="quiz-ans"><strong>Jawab:</strong> Agar 5 skor mentah (<em>logits</em>) diubah menjadi probabilitas <code>0–100%</code> yang jumlah totalnya selalu tepat <code>100%</code>.</div>
        </div>
        <div class="quiz-item compact">
          <div class="q-txt">5. Mengapa MLP biasa tidak ideal untuk foto <code>224×224×3</code> sehingga kita butuh CNN?</div>
          <button class="btn-ui outline" onclick="toggleAns('q5', this)">Lihat Jawaban</button>
          <div id="q5" class="quiz-ans"><strong>Jawab:</strong> Karena <em>Flatten</em> merusak struktur spasial 2D dan jumlah bobotnya langsung meledak hingga jutaan (&gt;19 juta untuk 128 hidden).</div>
        </div>
        <div class="card tint-green" style="padding:10px 13px; justify-content:center; gap:5px;">
          <div class="card-title" style="font-size:13.5px; color:#137333;">Target Penguasaan P02</div>
          <div style="font-size:11.6px; line-height:1.4; color:#202124;">
            ✓ Bisa membedakan AI/ML/DL &amp; 4 Task CV<br/>
            ✓ Bisa menghitung neuron &amp; parameter MLP<br/>
            ✓ Paham alur Forward Pass &amp; Loss → Gradient Descent<br/>
            ✓ Tahu alasan pindah ke <strong>CNN</strong> di P03!
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 56: 3 POIN UTAMA (DARK) -->
    <section class="slide dark" data-title="3 Poin Utama Hari Ini" data-notes="Alokasi waktu: 2 menit. Rangkum seluruh sesi Computer Vision 101 menjadi 3 pilar utama agar mudah diingat setelah kelas selesai.">
      <div class="kicker">RANGKUMAN INTI · COMPUTER VISION 101</div>
      <h2>3 Poin Utama yang <span style="color:var(--yellow);">Wajib Dibawa Pulang</span></h2>
      <div class="grid-3" style="margin-top:12px;">
        <div class="card" style="background:#292A2D; border-color:#3C4043; color:#FFF; justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div class="big-num" style="color:var(--blue);">01</div>
          <div class="card-title" style="color:#FFF;">Peta Besar CV Itu Jelas</div>
          <div class="card-body" style="color:#BDC1C6;">Proyek klasifikasi 5 karakter Frozen berada di dalam <strong>Deep Learning</strong> (<code>AI ⊃ ML ⊃ DL</code>) dengan jenis tugas <strong>Multi-Class Image Classification</strong>.</div>
        </div>
        <div class="card" style="background:#292A2D; border-color:#3C4043; color:#FFF; justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div class="big-num" style="color:var(--green);">02</div>
          <div class="card-title" style="color:#FFF;">Neural Network = Susunan Sederhana</div>
          <div class="card-body" style="color:#BDC1C6;">Dimulai dari <strong>1 Neuron</strong> (<code>x·w + b → ReLU</code>), disusun menjadi <strong>Input, Hidden, &amp; Output Layer (<code>Softmax</code>)</strong>, lalu belajar menurunkan <strong>Loss</strong> lewat <strong>Gradient Descent</strong>.</div>
        </div>
        <div class="card" style="background:#292A2D; border-color:#3C4043; color:#FFF; justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div class="big-num" style="color:var(--yellow);">03</div>
          <div class="card-title" style="color:#FFF;">Batasan MLP → Pintu Menuju CNN</div>
          <div class="card-body" style="color:#BDC1C6;">Foto <code>224×224×3</code> meledakkan MLP ke <strong>19,27 juta parameter</strong>. Di <strong>P03</strong> kita bedah <strong>CNN</strong> yang membaca gambar 2D secara efisien!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 57: CLOSING & PREVIEW P03 -->
    <section class="slide" data-title="Closing &amp; Preview P03" data-notes="Alokasi waktu: 2 menit. Beri apresiasi kepada peserta, sampaikan tugas ringan merangkum alur neuron sampai jaringan dengan bahasa sendiri, dan berikan preview seru menuju P03 (Training Neural Network & Konvolusi CNN)." style="background: radial-gradient(circle at 80% 35%, rgba(52,168,83,0.12) 0%, rgba(66,133,244,0.09) 45%, #FFFFFF 100%);">
      <div class="kicker">PENUTUP · SAMPAI JUMPA DI P03</div>
      <h2>Luar Biasa! Pondasi <span class="hl-green">Computer Vision 101</span> Selesai</h2>
      <div class="grid-2" style="margin-top:8px;">
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Tugas Ringan Mandiri (Opsional)</div>
          <div class="card-body">
            <ul>
              <li>Tulis ringkasan singkat (maks. 1 halaman) dengan <strong>bahasamu sendiri</strong>: perjalanan 1 foto Frozen dari piksel → <em>Input Layer</em> → <em>Hidden Layer</em> → <code>Softmax</code>.</li>
              <li>Simpan grafik Loss &amp; tabel eksperimen <code>32 / 64 / 128</code> neuron dari notebook sebagai catatan belajar.</li>
            </ul>
          </div>
          <div class="callout"><strong>Slide 57–58</strong> berisi daftar referensi video &amp; bacaan mandiri yang bisa diklik kapan saja.</div>
        </div>
        <div class="card tint-green" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">PREVIEW PERTEMUAN BERIKUTNYA</span>
          <div class="card-title">P03 — Training Neural Network &amp; Konvolusi (CNN)</div>
          <div class="card-body">
            <ul>
              <li>Memperdalam proses training (kurva <em>Train vs Validation Loss</em>, <em>Overfitting</em>, <em>Learning Rate</em>).</li>
              <li>Membongkar <strong>Konvolusi (CNN)</strong>: kernel/filter 2D, stride, padding, pooling, dan melihat langsung <em>Feature Map</em> dari foto Disney Frozen milikmu!</li>
            </ul>
          </div>
          <div class="mini-box" style="font-style:italic; text-align:center;">&ldquo;Memahami 1 neuron dengan jernih adalah kunci memahami jaringan jutaan parameter.&rdquo;</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 58: REFERENSI BELAJAR MANDIRI (1/2) — 0 MENIT -->
    <section class="slide" data-title="Referensi Belajar Mandiri (1/2)" data-notes="Alokasi waktu: 0 menit. Referensi belajar mandiri bagian 1 (sumber sesuai docs/PLAN.md; sumber belum diverifikasi ulang diberi label [CEK LINK]).">
      <div class="kicker">REFERENSI MANDIRI (1/2) · TIDAK MASUK DURASI KELAS</div>
      <h2>Sumber Belajar: <span class="hl-blue">Neural Network &amp; Visualisasi Dasar</span></h2>
      <div class="grid-2" style="gap:12px;">
        <div class="ref-list">
          <a class="ref-item featured" href="https://www.youtube.com/watch?v=aircAruvnKk" target="_blank" rel="noopener">
            <div class="ref-num">1</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">3Blue1Brown — But what is a Neural Network?</span><span class="ref-tag must">Wajib</span></div>
              <div class="ref-desc">Visual paling jernih tentang piksel gambar masuk ke neuron, layer, weight, dan bias.</div>
              <div class="ref-url">youtube.com/watch?v=aircAruvnKk</div>
            </div>
          </a>
          <a class="ref-item" href="https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi" target="_blank" rel="noopener">
            <div class="ref-num">2</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">3Blue1Brown — Playlist Neural Networks (Bab 1–4)</span><span class="ref-tag">Video</span></div>
              <div class="ref-desc">Seri lengkap: struktur layer, Gradient Descent, hingga intuisi Backpropagation.</div>
              <div class="ref-url">youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi</div>
            </div>
          </a>
          <a class="ref-item" href="https://3blue1brown.com/lessons/neural-networks" target="_blank" rel="noopener">
            <div class="ref-num green">3</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">3Blue1Brown — Versi Tulis Neural Networks</span><span class="ref-tag doc">Artikel</span></div>
              <div class="ref-desc">Ringkasan interaktif berbentuk bacaan jika ingin mengulang pelan-pelan tanpa video.</div>
              <div class="ref-url">3blue1brown.com/lessons/neural-networks</div>
            </div>
          </a>
        </div>
        <div class="ref-list">
          <a class="ref-item" href="https://playground.tensorflow.org/" target="_blank" rel="noopener">
            <div class="ref-num yellow">4</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">TensorFlow Playground [CEK LINK]</span><span class="ref-tag code">Sandbox</span></div>
              <div class="ref-desc">Eksperimen langsung di browser: tambah/kurangi hidden layer, neuron, &amp; learning rate.</div>
              <div class="ref-url">playground.tensorflow.org</div>
            </div>
          </a>
          <a class="ref-item" href="https://developers.google.com/machine-learning/crash-course" target="_blank" rel="noopener">
            <div class="ref-num red">5</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">Google Machine Learning Crash Course [CEK LINK]</span><span class="ref-tag doc">Kursus</span></div>
              <div class="ref-desc">Pengantar konsep ML, Loss, Gradient Descent, dan Neural Network ramah pemula.</div>
              <div class="ref-url">developers.google.com/machine-learning/crash-course</div>
            </div>
          </a>
          <a class="ref-item" href="https://keras.io/guides/sequential_model/" target="_blank" rel="noopener">
            <div class="ref-num green">6</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">Keras Official — The Sequential Model Guide [CEK LINK]</span><span class="ref-tag code">Dokumentasi</span></div>
              <div class="ref-desc">Panduan resmi menyusun layer <code>Sequential</code>, <code>Flatten</code>, dan <code>Dense</code> di Keras 3.</div>
              <div class="ref-url">keras.io/guides/sequential_model/</div>
            </div>
          </a>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 59: REFERENSI BELAJAR MANDIRI (2/2) — 0 MENIT -->
    <section class="slide" data-title="Referensi Belajar Mandiri (2/2)" data-notes="Alokasi waktu: 0 menit. Referensi belajar mandiri bagian 2 untuk persiapan CNN (P03) dan Arsitektur MobileNetV2 (P04), seluruhnya merujuk docs/PLAN.md.">
      <div class="kicker">REFERENSI MANDIRI (2/2) · PERSIAPAN P03 &amp; P04</div>
      <h2>Sumber Belajar: <span class="hl-green">Computer Vision, CNN &amp; MobileNetV2</span></h2>
      <div class="grid-2" style="gap:12px;">
        <div class="ref-list">
          <a class="ref-item featured" href="https://www.coursera.org/learn/convolutional-neural-networks" target="_blank" rel="noopener">
            <div class="ref-num">7</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">Coursera (DeepLearning.AI) — Convolutional Neural Networks</span><span class="ref-tag must">Preview P03</span></div>
              <div class="ref-desc">Week 1 membahas dasar konvolusi 2D dan fondasi tugas Computer Vision.</div>
              <div class="ref-url">coursera.org/learn/convolutional-neural-networks</div>
            </div>
          </a>
          <a class="ref-item" href="https://poloclub.github.io/cnn-explainer/" target="_blank" rel="noopener">
            <div class="ref-num yellow">8</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">CNN Explainer (Visual Interaktif) [CEK LINK]</span><span class="ref-tag code">Interaktif</span></div>
              <div class="ref-desc">Melihat alur gambar nyata masuk ke filter CNN hingga Softmax secara langsung.</div>
              <div class="ref-url">poloclub.github.io/cnn-explainer/</div>
            </div>
          </a>
          <a class="ref-item" href="https://cs231n.github.io/" target="_blank" rel="noopener">
            <div class="ref-num red">9</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">Stanford CS231n — Lecture Notes [CEK LINK]</span><span class="ref-tag doc">Opsional</span></div>
              <div class="ref-desc">Catatan mendalam mengenai Neural Networks dan Convolutional Networks untuk CV.</div>
              <div class="ref-url">cs231n.github.io</div>
            </div>
          </a>
        </div>
        <div class="ref-list">
          <a class="ref-item" href="https://arxiv.org/abs/1512.03385" target="_blank" rel="noopener">
            <div class="ref-num">10</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">He dkk. — Deep Residual Learning (ResNet) [CEK LINK]</span><span class="ref-tag doc">Paper</span></div>
              <div class="ref-desc">Paper asli ide <em>skip connection</em> yang memungkinkan jaringan CNN sangat dalam.</div>
              <div class="ref-url">arxiv.org/abs/1512.03385</div>
            </div>
          </a>
          <a class="ref-item" href="https://arxiv.org/abs/1801.04381" target="_blank" rel="noopener">
            <div class="ref-num green">11</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">Sandler dkk. — MobileNetV2 (CVPR 2018)</span><span class="ref-tag doc">Paper Proyek</span></div>
              <div class="ref-desc">Paper resmi arsitektur ringan <strong>MobileNetV2</strong> yang menjadi model utama proyek kita.</div>
              <div class="ref-url">arxiv.org/abs/1801.04381</div>
            </div>
          </a>
          <a class="ref-item" href="https://www.tensorflow.org/tutorials/images/transfer_learning?hl=id" target="_blank" rel="noopener">
            <div class="ref-num green">12</div>
            <div class="ref-content">
              <div class="ref-head"><span class="ref-title">TensorFlow — Transfer Learning &amp; Fine-Tuning (ID)</span><span class="ref-tag code">Preview P04</span></div>
              <div class="ref-desc">Tutorial resmi berbahasa Indonesia memakai MobileNetV2 pada dataset foto kustom.</div>
              <div class="ref-url">tensorflow.org/tutorials/images/transfer_learning?hl=id</div>
            </div>
          </a>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    return "\n".join(s)


def build_extra_js(data: dict) -> str:
    cs_json = json.dumps(data["char_samples"], ensure_ascii=False)
    fp_json = json.dumps(data["mini_forward_pass"], ensure_ascii=False)
    flt_json = json.dumps(data["flatten_3x3"], ensure_ascii=False)
    total_imgs = data["total_images"]
    return f"""
    const FROZEN_CHAR_DATA = {cs_json};
    const MINI_FP = {fp_json};
    const FLATTEN_PIXELS = {flt_json};

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
      const call = document.getElementById('ml-callout');
      if (!diag) return;

      if (mode === 'rule') {{
        diag.innerHTML = `
          <svg viewBox="0 0 490 270" style="width:100%; height:265px; display:block;">
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
        badge.className = 'pill red'; badge.textContent = 'PEMROGRAMAN TRADISIONAL';
        title.textContent = 'Manusia Menulis Semua Aturan';
        desc.innerHTML = '<ul><li>Programmer harus memikirkan sendiri setiap syarat aturan (mis. <code>if-else</code>).</li><li>Cocok untuk aturan pasti (kalkulator, pajak), tetapi <strong>mustahil</strong> untuk membedakan ribuan variasi foto figurine!</li></ul>';
        call.className = 'callout red';
        call.innerHTML = '<strong>Batasnya:</strong> Setiap kali cahaya, sudut, atau latar foto berubah, aturan manual langsung patah.';
      }} else {{
        diag.innerHTML = `
          <svg viewBox="0 0 490 270" style="width:100%; height:265px; display:block;">
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
        badge.className = 'pill green'; badge.textContent = 'MACHINE LEARNING (SUPERVISED)';
        title.textContent = 'Belajar Pola dari Contoh & Kunci Jawaban';
        desc.innerHTML = '<ul><li><strong>Supervised Learning:</strong> kita memberi data latihan beserta kunci jawabannya (<em>label</em>) ke algoritma matematika &amp; statistik.</li><li>Hasil training berupa <strong>Model</strong> yang langsung bisa dipakai menebak <strong>foto baru</strong> yang belum pernah dilihat!</li></ul>';
        call.className = 'callout green';
        call.innerHTML = '<strong>Hasil:</strong> Makin beragam contoh fotonya (polos &amp; ramai), makin tangguh pola yang dipelajari model.';
      }}
    }}
    setMlTab('ml');

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
        call: '<strong>Klik Tab 2 &amp; 3</strong> untuk masuk lebih dalam ke cabang ML dan Deep Learning!',
      }},
      ml: {{
        pill: 'RECAP · MACHINE LEARNING (ML)', pillCls: 'pill red', barCls: 'card-top-bar bar-red', callCls: 'callout red',
        title: 'Cabang AI yang Belajar Pola dari Data',
        illus: '<div style="display:flex; align-items:center; justify-content:center; gap:7px; font-family:var(--font-code); font-size:10.5px;"><span style="background:#FCE8E6; color:#C5221F; padding:3px 8px; border-radius:6px; font-weight:700;">Fitur Manual</span><span>→</span><span style="background:#FEF7E0; color:#B06000; padding:3px 8px; border-radius:6px; font-weight:700;">Algoritma Statistik</span><span>→</span><span style="background:#202124; color:#FFF; padding:3px 8px; border-radius:6px; font-weight:700;">Model</span></div>',
        body: '<ul><li>Belajar pola dari contoh data menggunakan algoritma statistik (<em>Decision Tree, Random Forest, SVM</em>).</li></ul>',
        frozen: '<strong>Batasan pada foto:</strong> Manusia masih perlu mengekstrak fitur manual dulu (kita bedah tajam perbedaannya di slide berikutnya!).',
        call: '<strong>Klik Tab 3 (Deep Learning)</strong> untuk melihat solusi khusus bagi foto &amp; video.',
      }},
      dl: {{
        pill: 'DEEP LEARNING (DL)', pillCls: 'pill green', barCls: 'card-top-bar bar-green', callCls: 'callout green',
        title: 'Cabang ML dengan Neural Network Berlapis Banyak',
        illus: '<div style="display:flex; align-items:center; justify-content:center; gap:9px;"><img src="assets/P02/thumb_elsa.jpg" style="width:36px; height:36px; border-radius:7px; object-fit:cover; border:1.5px solid #4285F4;"/><span style="font-weight:700; color:#137333;">→</span><span style="background:#34A853; color:#FFF; padding:4px 10px; border-radius:7px; font-family:var(--font-title); font-size:11px; font-weight:700;">Neural Network (Belajar Fitur Otomatis)</span><span style="font-weight:700; color:#137333;">→</span><span style="background:#E6F4EA; border:1.5px solid #34A853; color:#137333; padding:3px 8px; border-radius:7px; font-family:var(--font-title); font-size:11px; font-weight:700;">Elsa!</span></div>',
        body: '<ul><li>Memakai <strong>Neural Network</strong> bertingkat yang otomatis mempelajari ciri langsung dari piksel mentah (tepi → bentuk → objek).</li><li>Sangat unggul untuk data tidak terstruktur: <strong>foto, video, suara, dan teks</strong>.</li></ul>',
        frozen: '<strong>Contoh di Proyek Frozen:</strong> Memasukkan foto <code>(224,224,3)</code> langsung ke <strong>Neural Network berlapis banyak</strong> untuk menebak Anna, Elsa, Kristoff, Olaf, atau Sven!',
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
      document.getElementById('vnn-pill').className = c.pillCls;
      document.getElementById('vnn-pill').textContent = c.pill;
      document.getElementById('vnn-bar').className = c.barCls;
      document.getElementById('vnn-title').textContent = c.title;
      const illusEl = document.getElementById('vnn-illus');
      if (illusEl) illusEl.innerHTML = c.illus || '';
      document.getElementById('vnn-body').innerHTML = c.body;
      document.getElementById('vnn-frozen').innerHTML = c.frozen;
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
    // ANIMASI INTERAKTIF FLATTEN (Slide 21): 3x3 Real Elsa -> Input Layer
    // =========================================================================
    const FLT_ROW_COL = ['#4285F4', '#EA4335', '#34A853'];
    const FLT_ROW_BG  = ['#E8F0FE', '#FCE8E6', '#E6F4EA'];
    const FLT_ROW_LBL = ['Brs 1', 'Brs 2', 'Brs 3'];
    let fltPlaced = 9;        // number of pixels already landed in Input Layer (0..9)
    let fltFlyIdx = -1;       // index (0..8) currently in flight, or -1 if idle
    let fltFlyT = 0;          // 0..1 progress of current flying pixel
    let fltAutoPlay = false;
    let fltRafId = null;
    let fltLastTs = 0;

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

    function drawFlattenFrame() {{
      const canvas = document.getElementById('flatten-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, W, H);

      const gx0 = 64, gy0 = 48, cell = 66, gap = 8;
      const slotX = 528, slotY0 = 64, slotGap = 28.5, slotR = 12.2;

      const cellCenter = (r, c) => ({{
        x: gx0 + c * (cell + gap) + cell / 2,
        y: gy0 + r * (cell + gap) + cell / 2,
      }});
      const slotCenter = (idx) => ({{
        x: slotX,
        y: slotY0 + idx * slotGap,
      }});

      // Title 1: 2D Grid
      ctx.fillStyle = '#202124';
      ctx.font = '700 13.5px Poppins, Arial';
      ctx.textAlign = 'center';
      ctx.fillText('1. Gambar 2D (3×3 = 9 Piksel Nyata)', gx0 + (3 * cell + 2 * gap) / 2, 26);

      // Row badges on left of grid
      for (let r = 0; r < 3; r++) {{
        const cy = gy0 + r * (cell + gap) + cell / 2;
        _fltRoundRect(ctx, 8, cy - 13, 48, 26, 7);
        ctx.fillStyle = FLT_ROW_BG[r]; ctx.fill();
        ctx.strokeStyle = FLT_ROW_COL[r]; ctx.lineWidth = 1.6; ctx.stroke();
        ctx.fillStyle = FLT_ROW_COL[r];
        ctx.font = '700 10.5px Poppins, Arial';
        ctx.textAlign = 'center';
        ctx.fillText(FLT_ROW_LBL[r], 32, cy + 4);
      }}

      // Draw 3x3 real Elsa pixel cells
      FLATTEN_PIXELS.forEach((px, idx) => {{
        const x = gx0 + px.col * (cell + gap);
        const y = gy0 + px.row * (cell + gap);
        const isLanded = idx < fltPlaced;
        const isFlying = idx === fltFlyIdx;

        _fltRoundRect(ctx, x, y, cell, cell, 9);
        ctx.fillStyle = `rgb(${{px.rgb[0]}},${{px.rgb[1]}},${{px.rgb[2]}})`;
        ctx.fill();

        if (isLanded) {{
          ctx.fillStyle = 'rgba(255,255,255,0.42)';
          ctx.fill();
        }}
        ctx.strokeStyle = isFlying ? '#FBBC04' : FLT_ROW_COL[px.row];
        ctx.lineWidth = isFlying ? 4.2 : 2.5;
        ctx.stroke();

        // Glow ring when scanning/flying
        if (isFlying) {{
          ctx.save();
          _fltRoundRect(ctx, x - 3, y - 3, cell + 6, cell + 6, 11);
          ctx.strokeStyle = 'rgba(251,188,4,0.65)';
          ctx.lineWidth = 3;
          ctx.stroke();
          ctx.restore();
        }}

        const tc = px.gray < 0.56 && !isLanded ? '#FFFFFF' : '#202124';
        ctx.fillStyle = tc;
        ctx.textAlign = 'center';
        ctx.font = '700 10.5px Roboto Mono, monospace';
        ctx.fillText(`x${{px.idx}}`, x + cell / 2, y + 26);
        ctx.font = '700 13.5px Roboto Mono, monospace';
        ctx.fillText(px.gray.toFixed(2), x + cell / 2, y + 46);

        if (isLanded) {{
          ctx.beginPath();
          ctx.arc(x + cell - 11, y + 11, 7.5, 0, Math.PI * 2);
          ctx.fillStyle = FLT_ROW_COL[px.row];
          ctx.fill();
          ctx.fillStyle = '#FFFFFF';
          ctx.font = '700 9px Arial';
          ctx.fillText('✓', x + cell - 11, y + 14);
        }}
      }});

      // Bottom scan direction hint under grid
      ctx.fillStyle = '#5F6368';
      ctx.font = '600 10.5px Roboto, Arial';
      ctx.textAlign = 'center';
      ctx.fillText('Urutan pindai: kiri → kanan, lalu turun baris', gx0 + (3 * cell + 2 * gap) / 2, gy0 + 3 * cell + 2 * gap + 22);

      // Center Flatten Badge (high above curves)
      _fltRoundRect(ctx, 316, 12, 134, 34, 9);
      ctx.fillStyle = '#FEF7E0'; ctx.fill();
      ctx.strokeStyle = '#FBBC04'; ctx.lineWidth = 2; ctx.stroke();
      ctx.fillStyle = '#B06000';
      ctx.font = '700 12px Poppins, Arial';
      ctx.textAlign = 'center';
      ctx.fillText('2. FLATTEN', 383, 33);

      ctx.fillStyle = '#5F6368';
      ctx.font = '600 10px Roboto, Arial';
      ctx.fillText('Susun ke bawah', 383, 60);

      // Right: Input Layer vertical capsule
      _fltRoundRect(ctx, 476, 10, 274, 296, 16);
      ctx.fillStyle = '#F8F9FA'; ctx.fill();
      ctx.strokeStyle = '#4285F4'; ctx.lineWidth = 2.6; ctx.stroke();

      ctx.fillStyle = '#1A73E8';
      ctx.font = '700 13.5px Poppins, Arial';
      ctx.textAlign = 'center';
      ctx.fillText('3. INPUT LAYER', 613, 30);
      ctx.fillStyle = '#5F6368';
      ctx.font = '600 10px Roboto Mono, monospace';
      ctx.fillText(`(1 Kolom Vertikal · ${{fltPlaced}} / 9 Neuron)`, 613, 45);

      // Draw 9 vertical neuron slots
      FLATTEN_PIXELS.forEach((px, idx) => {{
        const pos = slotCenter(idx);
        const isLanded = idx < fltPlaced;
        const isTarget = idx === fltFlyIdx;

        if (isLanded) {{
          ctx.beginPath();
          ctx.arc(pos.x, pos.y, slotR, 0, Math.PI * 2);
          ctx.fillStyle = FLT_ROW_COL[px.row];
          ctx.fill();
          ctx.strokeStyle = '#FFFFFF';
          ctx.lineWidth = 2;
          ctx.stroke();

          ctx.fillStyle = '#FFFFFF';
          ctx.font = '700 8.8px Roboto Mono, monospace';
          ctx.textAlign = 'center';
          ctx.fillText(px.gray.toFixed(2), pos.x, pos.y + 3.2);

          ctx.fillStyle = FLT_ROW_COL[px.row];
          ctx.font = '700 11px Roboto Mono, monospace';
          ctx.textAlign = 'left';
          ctx.fillText(`x${{px.idx}}`, pos.x + 19, pos.y + 3.5);

          ctx.fillStyle = '#5F6368';
          ctx.font = '400 10px Roboto, Arial';
          ctx.fillText(`(Baris ${{px.row + 1}}, Kol ${{px.col + 1}})`, pos.x + 42, pos.y + 3.5);
        }} else {{
          ctx.save();
          ctx.setLineDash([3, 3]);
          ctx.beginPath();
          ctx.arc(pos.x, pos.y, slotR, 0, Math.PI * 2);
          ctx.fillStyle = isTarget ? '#FEF7E0' : '#FFFFFF';
          ctx.fill();
          ctx.strokeStyle = isTarget ? '#FBBC04' : '#CFD4DA';
          ctx.lineWidth = isTarget ? 2.2 : 1.5;
          ctx.stroke();
          ctx.restore();

          ctx.fillStyle = isTarget ? '#B06000' : '#9AA0A6';
          ctx.font = '600 10px Roboto Mono, monospace';
          ctx.textAlign = 'left';
          ctx.fillText(`x${{px.idx}} (menunggu...)`, pos.x + 19, pos.y + 3.5);
        }}
      }});

      // If idle & completed (9/9), show clean 3-row directional guide arrows
      if (fltFlyIdx === -1 && fltPlaced === 9) {{
        [0, 1, 2].forEach((r) => {{
          const sy = gy0 + r * (cell + gap) + cell / 2;
          const ey = slotCenter(r * 3 + 1).y;
          ctx.save();
          ctx.strokeStyle = FLT_ROW_COL[r];
          ctx.lineWidth = 2.4;
          ctx.beginPath();
          ctx.moveTo(gx0 + 3 * cell + 2 * gap + 8, sy);
          ctx.quadraticCurveTo(385, (sy + ey) / 2 + (r === 0 ? -16 : r === 2 ? 16 : 0), 468, ey);
          ctx.stroke();
          // arrowhead
          ctx.fillStyle = FLT_ROW_COL[r];
          ctx.beginPath();
          ctx.moveTo(471, ey);
          ctx.lineTo(461, ey - 5.5);
          ctx.lineTo(461, ey + 5.5);
          ctx.closePath();
          ctx.fill();
          ctx.restore();
        }});
      }}

      // Flying pixel -> morphing into Neuron circle along Bezier curve!
      if (fltFlyIdx >= 0 && fltFlyIdx < FLATTEN_PIXELS.length) {{
        const px = FLATTEN_PIXELS[fltFlyIdx];
        const src = cellCenter(px.row, px.col);
        const dst = slotCenter(fltFlyIdx);
        const ctrlX = (src.x + dst.x) / 2;
        const ctrlY = Math.min(src.y, dst.y) - 46;
        const t = Math.max(0, Math.min(1, fltFlyT));
        const e = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
        const inv = 1 - e;
        const fx = inv * inv * src.x + 2 * inv * e * ctrlX + e * e * dst.x;
        const fy = inv * inv * src.y + 2 * inv * e * ctrlY + e * e * dst.y;

        // Dashed Bezier flight trajectory
        ctx.save();
        ctx.setLineDash([6, 4]);
        ctx.strokeStyle = FLT_ROW_COL[px.row];
        ctx.lineWidth = 2.6;
        ctx.beginPath();
        ctx.moveTo(src.x, src.y);
        ctx.quadraticCurveTo(ctrlX, ctrlY, dst.x, dst.y);
        ctx.stroke();
        ctx.restore();

        // Morphing token: starts as square pixel (44px, rx=8), morphs into glowing circle (32px, rx=16)
        const sz = 46 - 16 * e;
        const rad = 8 + (sz / 2 - 8) * e;
        ctx.save();
        ctx.shadowColor = 'rgba(251, 188, 4, 0.55)';
        ctx.shadowBlur = 14;
        _fltRoundRect(ctx, fx - sz / 2, fy - sz / 2, sz, sz, rad);
        ctx.fillStyle = FLT_ROW_COL[px.row];
        ctx.fill();
        ctx.strokeStyle = '#FBBC04';
        ctx.lineWidth = 3;
        ctx.stroke();
        ctx.restore();

        ctx.fillStyle = '#FFFFFF';
        ctx.textAlign = 'center';
        ctx.font = '700 9.5px Roboto Mono, monospace';
        ctx.fillText(`x${{px.idx}}`, fx, fy - 1);
        ctx.font = '700 9.5px Roboto Mono, monospace';
        ctx.fillText(px.gray.toFixed(2), fx, fy + 10);
      }}

      // Update status pill
      const st = document.getElementById('flatten-status');
      if (st) {{
        if (fltFlyIdx >= 0) {{
          const px = FLATTEN_PIXELS[fltFlyIdx];
          st.className = 'pill yellow';
          st.textContent = `Memindahkan x${{px.idx}} (Baris ${{px.row + 1}}, Kol ${{px.col + 1}}) → Slot #${{px.idx}}`;
        }} else if (fltPlaced === 0) {{
          st.className = 'pill blue';
          st.textContent = 'Siap! Klik "Putar Animasi" atau "+1 Piksel"';
        }} else if (fltPlaced < 9) {{
          st.className = 'pill blue';
          st.textContent = `Input Layer: ${{fltPlaced}} / 9 neuron tersusun`;
        }} else {{
          st.className = 'pill green';
          st.textContent = 'Input Layer: 9 / 9 neuron (Selesai!)';
        }}
      }}
    }}

    function _stopFltRaf() {{
      if (fltRafId !== null) {{ cancelAnimationFrame(fltRafId); fltRafId = null; }}
      fltAutoPlay = false;
    }}

    function _tickFltAnim(ts) {{
      if (!fltLastTs) fltLastTs = ts;
      const dt = Math.min(0.05, (ts - fltLastTs) / 1000);
      fltLastTs = ts;
      const speed = fltAutoPlay ? 1.85 : 2.6;
      fltFlyT += dt * speed;
      if (fltFlyT >= 1.0) {{
        fltPlaced = fltFlyIdx + 1;
        fltFlyT = 0;
        if (fltAutoPlay && fltPlaced < 9) {{
          fltFlyIdx = fltPlaced;
        }} else {{
          fltFlyIdx = -1;
          fltAutoPlay = false;
          fltRafId = null;
          drawFlattenFrame();
          return;
        }}
      }}
      drawFlattenFrame();
      fltRafId = requestAnimationFrame(_tickFltAnim);
    }}

    function playFlattenAnim() {{
      _stopFltRaf();
      fltPlaced = 0;
      fltFlyIdx = 0;
      fltFlyT = 0;
      fltAutoPlay = true;
      fltLastTs = 0;
      drawFlattenFrame();
      fltRafId = requestAnimationFrame(_tickFltAnim);
    }}

    function stepFlattenAnim() {{
      if (fltAutoPlay) _stopFltRaf();
      if (fltFlyIdx >= 0) {{
        // snap current flying pixel immediately first
        fltPlaced = fltFlyIdx + 1;
        fltFlyIdx = -1;
      }}
      if (fltPlaced >= 9) {{
        fltPlaced = 0;
      }}
      fltFlyIdx = fltPlaced;
      fltFlyT = 0;
      fltAutoPlay = false;
      fltLastTs = 0;
      if (fltRafId !== null) cancelAnimationFrame(fltRafId);
      fltRafId = requestAnimationFrame(_tickFltAnim);
    }}

    function resetFlattenAnim() {{
      _stopFltRaf();
      fltPlaced = 0;
      fltFlyIdx = -1;
      fltFlyT = 0;
      drawFlattenFrame();
    }}

    function completeFlattenAnim() {{
      _stopFltRaf();
      fltPlaced = 9;
      fltFlyIdx = -1;
      fltFlyT = 0;
      drawFlattenFrame();
    }}

    function setFlattenPdfState(mode) {{
      _stopFltRaf();
      if (mode === 'mid') {{
        fltPlaced = 4;
        fltFlyIdx = 4;   // x5 (Row 2, Col 2) frozen gracefully mid-flight!
        fltFlyT = 0.54;
      }} else {{
        fltPlaced = 9;
        fltFlyIdx = -1;
        fltFlyT = 0;
      }}
      drawFlattenFrame();
    }}
    completeFlattenAnim();

    // =========================================================================
    // SIMULATOR #3 (Slide 22): Kalkulator Jumlah Neuron Input Layer
    // =========================================================================
    function setInSize(h, w, c, btn) {{
      document.getElementById('in-hw').value = String(h);
      document.getElementById('in-ch').value = String(c);
      document.querySelectorAll('#in-presets button').forEach((b) => b.classList.add('outline'));
      if (btn) btn.classList.remove('outline');
      updateInCalc();
    }}
    function updateInCalc() {{
      const hw = parseInt(document.getElementById('in-hw').value, 10) || 224;
      const ch = parseInt(document.getElementById('in-ch').value, 10) || 3;
      const tot = hw * hw * ch;
      document.getElementById('in-hw-v').textContent = `${{hw}}×${{hw}}`;
      document.getElementById('in-ch-v').textContent = ch === 1 ? '1 (Gray)' : '3 (RGB)';
      document.getElementById('in-total').textContent = tot.toLocaleString('id-ID');
      document.getElementById('in-formula').textContent = `${{hw}} (tinggi) × ${{hw}} (lebar) × ${{ch}} (${{ch === 1 ? 'Grayscale' : 'R, G, B'}}) = ${{tot.toLocaleString('id-ID')}} neuron`;
    }}
    updateInCalc();

    // =========================================================================
    // SIMULATOR #7 (Slide 27): Softmax 5 Karakter Frozen
    // =========================================================================
    const SM_NAMES = ['Anna', 'Elsa', 'Kristoff', 'Olaf', 'Sven'];
    const SM_PRESETS = {{
      elsa: [0.8, 3.2, -0.6, 0.2, -1.0],
      ragu: [2.2, 2.4, -0.8, -0.4, -1.2],
      neg: [-2.4, -0.8, -3.0, -2.6, -3.4],
    }};
    function setSmPreset(key) {{
      const vals = SM_PRESETS[key];
      if (!vals) return;
      vals.forEach((v, i) => {{
        const el = document.getElementById('sm-' + i);
        if (el) {{ el.value = String(v); el.setAttribute('value', String(v)); }}
      }});
      document.querySelectorAll('#sm-presets button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.smp !== key);
      }});
      updateSm();
    }}
    function updateSm() {{
      const logits = [0, 1, 2, 3, 4].map((i) => parseFloat(document.getElementById('sm-' + i).value));
      const exps = logits.map((v) => Math.exp(v));
      const sumE = exps.reduce((a, b) => a + b, 0);
      const probs = exps.map((e) => (e / sumE) * 100);
      let best = 0;
      probs.forEach((p, i) => {{
        if (p > probs[best]) best = i;
        document.getElementById('sm-v' + i).textContent = (logits[i] >= 0 ? '+' : '') + logits[i].toFixed(1);
        document.getElementById('sm-e' + i).textContent = exps[i] >= 10 ? exps[i].toFixed(1) : exps[i].toFixed(2);
        document.getElementById('sm-b' + i).style.width = p.toFixed(1) + '%';
        document.getElementById('sm-p' + i).textContent = p.toFixed(1) + '%';
      }});
      document.getElementById('sm-sum-pill').textContent = `Total = ${{probs.reduce((a, b) => a + b, 0).toFixed(1)}}%`;
      document.getElementById('sm-winner').innerHTML =
        `<strong>Prediksi: ${{SM_NAMES[best].toUpperCase()}} (${{probs[best].toFixed(1)}}%)</strong> — Semua nilai <code>eᶻ</code> selalu positif sehingga total peluang selalu tepat <code>100.0%</code>.`;
    }}
    updateSm();

    // =========================================================================
    // SIMULATOR #8 (Slide 28): Telusuri 1 Neuron Input -> 5 Neuron Output
    // =========================================================================
    function setTraceNeuron(activeIdx) {{
      document.querySelectorAll('#trace-btns button').forEach((b) => {{
        b.classList.toggle('outline', parseInt(b.dataset.tr, 10) !== activeIdx);
      }});
      const svg = document.getElementById('trace-svg');
      if (!svg) return;
      const inY = [52, 114, 176, 238];
      const outY = [38, 92, 146, 200, 254];
      const outNames = ['Anna', 'Elsa', 'Kristoff', 'Olaf', 'Sven'];
      let html = '';
      // Background dim lines
      for (let i = 0; i < 4; i++) {{
        if (i === activeIdx) continue;
        for (let j = 0; j < 5; j++) {{
          html += `<line x1="92" y1="${{inY[i]}}" x2="345" y2="${{outY[j]}}" stroke="#E0E3E7" stroke-width="1.2"/>`;
        }}
      }}
      // Highlighted 5 lines from active input neuron
      for (let j = 0; j < 5; j++) {{
        html += `<line x1="92" y1="${{inY[activeIdx]}}" x2="345" y2="${{outY[j]}}" stroke="#EA4335" stroke-width="2.8"/>`;
        const mx = 225, my = inY[activeIdx] * 0.45 + outY[j] * 0.55;
        html += `<rect x="${{mx - 22}}" y="${{my - 9}}" width="44" height="17" rx="5" fill="#FCE8E6" stroke="#EA4335" stroke-width="1"/>`;
        html += `<text x="${{mx}}" y="${{my + 3}}" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" font-weight="700" fill="#C5221F">w${{activeIdx + 1}},${{j + 1}}</text>`;
      }}
      // Input nodes
      for (let i = 0; i < 4; i++) {{
        const act = i === activeIdx;
        html += `<circle cx="72" cy="${{inY[i]}}" r="${{act ? 21 : 17}}" fill="${{act ? '#EA4335' : '#4285F4'}}" stroke="#FFF" stroke-width="3"/>`;
        html += `<text x="72" y="${{inY[i] + 4}}" text-anchor="middle" font-family="Roboto Mono" font-size="11.5" font-weight="700" fill="#FFF">x${{i + 1}}</text>`;
      }}
      // Output nodes
      for (let j = 0; j < 5; j++) {{
        html += `<circle cx="362" cy="${{outY[j]}}" r="16" fill="#34A853" stroke="#FFF" stroke-width="2.5"/>`;
        html += `<text x="362" y="${{outY[j] + 4}}" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#FFF">y${{j + 1}}</text>`;
        html += `<text x="386" y="${{outY[j] + 4}}" font-family="Poppins" font-size="12" font-weight="700" fill="#202124">${{outNames[j]}}</text>`;
      }}
      html += `<text x="72" y="18" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#1A73E8">Input Layer</text>`;
      html += `<text x="385" y="18" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#137333">Output Layer (5 Kelas)</text>`;
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
      const units = parseInt(document.getElementById('hid-units').value, 10) || 128;
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
      document.querySelectorAll('#fp-steps button').forEach((b) => {{
        b.classList.toggle('outline', String(b.dataset.fp) !== String(step));
      }});
      const x = MINI_FP.x;
      const z1 = MINI_FP.z1, h1 = MINI_FP.h1, lg = MINI_FP.logits, pr = MINI_FP.probs;
      const pill = document.getElementById('fp-pill');
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
    let gdMode = 'ideal';
    const GD_CFGS = {{
      small: {{
        lr: 0.03, title: 'LR Kecil (0.03) — Turun Sangat Pelan', cls: 'callout yellow', lossColor: '#B06000',
        note: '<strong>Terlalu Pelan:</strong> Setelah 8 langkah dari <code>w=-2.8</code>, posisi masih jauh dari dasar lembah (butuh banyak epoch).',
      }},
      ideal: {{
        lr: 0.20, title: 'LR Ideal (0.20) — Mulus ke Dasar Lembah', cls: 'callout green', lossColor: '#137333',
        note: '<strong>Pas!</strong> Dalam 8 langkah, bobot meluncur cepat &amp; tepat menuju dasar lembah (<code>Loss ≈ 0.002</code>).',
      }},
      large: {{
        lr: 1.06, title: 'LR Terlalu Besar (1.06) — Memantul Liar!', cls: 'callout red', lossColor: '#C5221F',
        note: '<strong>Bahaya Divergen!</strong> Langkah kebesaran membuat bobot melompati dasar lembah hingga <em>Loss</em> malah makin meledak.',
      }},
    }};
    function setGdMode(m) {{
      gdMode = m;
      document.querySelectorAll('#gd-presets button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.gd !== m);
      }});
      renderGdCanvas();
    }}
    function renderGdCanvas() {{
      const cfg = GD_CFGS[gdMode];
      const canvas = document.getElementById('gd-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, W, H);

      const pts = [];
      let w = -2.8;
      for (let step = 0; step <= 8; step++) {{
        pts.push({{ w, loss: w * w }});
        w = w - cfg.lr * (2 * w);
      }}
      const last = pts[pts.length - 1];
      document.getElementById('gd-title').textContent = cfg.title;
      document.getElementById('gd-end-w').textContent = last.w.toFixed(2);
      const lossEl = document.getElementById('gd-end-loss');
      lossEl.textContent = last.loss.toFixed(3);
      lossEl.style.color = cfg.lossColor;
      const noteEl = document.getElementById('gd-note');
      noteEl.className = cfg.cls;
      noteEl.innerHTML = cfg.note;

      const padL = 48, padR = 16, padT = 18, padB = 34;
      const pw = W - padL - padR, ph = H - padT - padB;
      const maxX = 4.4, maxY = 19.5;
      const toX = (xv) => padL + ((Math.max(-maxX, Math.min(maxX, xv)) + maxX) / (2 * maxX)) * pw;
      const toY = (yv) => padT + ph - (Math.min(maxY, yv) / maxY) * ph;

      ctx.strokeStyle = '#DADCE0'; ctx.lineWidth = 1.2; ctx.strokeRect(padL, padT, pw, ph);
      ctx.strokeStyle = '#5F6368'; ctx.lineWidth = 2.8;
      ctx.beginPath();
      for (let i = 0; i <= 160; i++) {{
        const xv = -maxX + (i / 160) * (2 * maxX);
        const px = toX(xv), py = toY(xv * xv);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }}
      ctx.stroke();

      ctx.fillStyle = '#34A853';
      ctx.beginPath(); ctx.arc(toX(0), toY(0), 6.5, 0, Math.PI * 2); ctx.fill();

      const pCol = gdMode === 'ideal' ? '#1A73E8' : gdMode === 'small' ? '#E37400' : '#EA4335';
      ctx.strokeStyle = pCol; ctx.lineWidth = 2.4;
      ctx.beginPath();
      pts.forEach((p, idx) => {{ const px = toX(p.w), py = toY(p.loss); if (idx === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }});
      ctx.stroke();

      pts.forEach((p, idx) => {{
        const px = toX(p.w), py = toY(p.loss);
        ctx.fillStyle = idx === 0 ? '#202124' : idx === pts.length - 1 ? pCol : '#FFFFFF';
        ctx.strokeStyle = pCol; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(px, py, idx === pts.length - 1 ? 6.5 : 4.2, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        if (idx === 0 || idx === pts.length - 1) {{
          ctx.fillStyle = '#202124'; ctx.font = '700 10.5px Roboto Mono'; ctx.textAlign = 'center';
          const lblX = idx === 0
            ? Math.max(padL + 46, px - 36)
            : Math.max(padL + 46, Math.min(padL + pw - 46, px));
          const lblY = idx === pts.length - 1 && py < padT + 26 ? py + 22 : Math.max(padT + 14, py - 12);
          ctx.fillText(idx === 0 ? 'Mulai (t=0)' : 'Akhir (t=8)', lblX, lblY);
        }}
      }});
      ctx.fillStyle = '#202124'; ctx.font = '700 11px Roboto'; ctx.textAlign = 'center';
      ctx.fillText('Nilai Weight (w) — Target Minimum di w = 0', padL + pw / 2, H - 6);
    }}
    renderGdCanvas();

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
      expandHelper('sm-presets', ['elsa', 'ragu', 'neg'], setSmPreset, 'sm');
      expandHelper('fp-steps', ['1', '2', '3', '4'], setFpStep, 'fp');
      expandHelper('gd-presets', ['small', 'ideal', 'large'], setGdMode, 'gd');
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
