"""Generate 59-slide ultra-beginner-friendly, step-by-step interactive HTML5 deck (SSOT) for P02.

Designed specifically for non-IT / complete beginners:
- Every concept follows: Everyday Analogy -> Concrete Frozen Example (Zero Math) ->
  Gentle Step-by-Step Number Example -> Technical Name -> Interactive Simulator -> Visual Q&A.
- Balanced, dense-yet-airy visual layout (zero dead whitespace, zero overlap, crisp dark-mode code).
- 6 interactive HTML5/Canvas simulators registered in `window.SLIDE_PDF_EXPANDERS`.
- Total speaker notes duration: exactly 120.0 minutes across 59 slides.
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
    .sim-slider-row { display: grid; grid-template-columns: 118px 1fr 56px; gap: 8px; align-items: center; font-size: 12.5px; }
    .sim-slider-row input[type="range"] { width: 100%; accent-color: var(--blue-text); cursor: pointer; }
    .sim-val { font-family: var(--font-code); font-weight: 700; text-align: right; color: var(--dark); font-size: 12.5px; }
    .frozen-chip { display: inline-flex; align-items: center; gap: 7px; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 4px 8px; font-size: 12px; font-weight: 600; color: var(--dark); }
    .frozen-chip img { width: 26px; height: 26px; border-radius: 6px; object-fit: cover; border: 1px solid var(--border); }
    .prob-row { display: grid; grid-template-columns: 88px 1fr 52px 58px; gap: 7px; align-items: center; font-size: 12.2px; }
    .prob-track { height: 18px; background: #ECEFF1; border-radius: 999px; overflow: hidden; border: 1px solid var(--border); }
    .prob-fill { height: 100%; border-radius: 999px; transition: width 0.16s ease; }
    .formula-box { background: var(--surface); border: 1.5px solid #C6DAFC; border-radius: 12px; padding: 9px 14px; font-family: var(--font-code); font-size: 13px; color: var(--dark); text-align: center; font-weight: 600; }
    .canvas-box { background: var(--white); border: 1px solid var(--border); border-radius: 14px; padding: 10px 12px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; gap: 8px; height: 100%; }
    .canvas-box canvas { width: 100%; height: auto; max-height: 100%; display: block; }
    .kpi-strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .kpi-mini { background: var(--surface); border: 1px solid var(--border); border-radius: 11px; padding: 8px 10px; text-align: center; }
    .kpi-mini .k-num { font-family: var(--font-title); font-size: 18px; font-weight: 700; color: var(--blue-text); line-height: 1.1; }
    .kpi-mini .k-lbl { font-size: 10.5px; color: var(--muted); margin-top: 2px; }
    .contrib-row { display: grid; grid-template-columns: 92px 1fr 52px; gap: 7px; align-items: center; font-size: 11.8px; font-family: var(--font-code); }
    .contrib-track { height: 14px; background: #F1F3F4; border-radius: 999px; position: relative; overflow: hidden; border: 1px solid #E0E3E7; }
    .contrib-mid { position: absolute; left: 50%; top: 0; bottom: 0; width: 1.5px; background: #9AA0A6; }
    .contrib-bar { position: absolute; top: 1px; bottom: 1px; border-radius: 999px; }
    .mini-box { background: #FFFFFF; border: 1px solid var(--border); border-radius: 11px; padding: 10px 12px; font-size: 12.6px; line-height: 1.45; color: #3C4043; }
    .ref-sub { font-size: 11.2px; color: var(--muted); background: var(--white); border: 1px dashed var(--border); border-radius: 9px; padding: 8px 11px; line-height: 1.45; }
    .marathon-bar { display: grid; grid-template-columns: auto repeat(5, 1fr); gap: 8px; align-items: center; background: var(--surface); border: 1px solid var(--border); border-radius: 13px; padding: 8px 12px; margin-top: 8px; }
    .marathon-step { display: flex; align-items: center; gap: 6px; background: var(--white); border: 1px solid var(--border); border-radius: 9px; padding: 5px 8px; font-size: 10.8px; font-weight: 600; color: var(--dark); text-decoration: none; }
    .marathon-dot { width: 18px; height: 18px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-family: var(--font-title); font-size: 10px; font-weight: 700; color: #FFF; flex-shrink: 0; }
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
) -> str:
    choices_html = "\n            ".join(f'<div class="qa-choice">{c}</div>' for c in choices)
    return f"""
    <section class="slide" data-title="Tanya-Jawab #{qa_num}" data-notes="{notes}">
      <div class="kicker">{kicker}</div>
      <h2>{title_html}</h2>
      <div class="split-60-40" style="align-items:stretch;">
        <div class="qa-box" style="justify-content:center; gap:12px;">
          <div class="qa-question" style="font-size:clamp(15px,1.4vw,18.5px);">{question_html}</div>
          <div style="display:flex; flex-direction:column; gap:8px;">
            {choices_html}
          </div>
          <button class="btn-ui" onclick="toggleQA('{qa_id}', this)">Klik untuk Lihat Jawaban &amp; Penjelasan</button>
          <div id="{qa_id}" class="qa-answer" style="padding:12px 16px; font-size:13.5px;">{answer_html}</div>
        </div>
        <div id="{qa_id}-vis" class="card surface" style="justify-content:center; align-items:center; text-align:center; gap:10px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="vis-q" style="width:100%;">{vis_q_html}</div>
          <div class="vis-a" style="width:100%;">{vis_a_html}</div>
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

    s: list[str] = []

    # =========================================================================
    # PEMBUKA & TRANSISI MULUS DARI P01 (SLIDE 01–05 · 5.5 menit)
    # =========================================================================
    s.append(
        f"""
    <!-- 01: COVER -->
    <section class="slide active" data-title="Cover — Teori Neural Network (ANN)" data-notes="Alokasi waktu: 1 menit. Selamat datang di P02! Di P01 kita sudah berhasil mengubah foto menjadi angka 0 sampai 1. Hari ini kita pelan-pelan membuka isi otak AI (Neural Network) memakai foto asli 5 karakter Disney Frozen!" style="background: radial-gradient(circle at 82% 46%, rgba(234,67,53,0.12) 0%, rgba(66,133,244,0.10) 35%, rgba(251,188,4,0.08) 60%, #FFFFFF 100%); justify-content: space-between;">
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

      <div style="position:relative; z-index:1; display:grid; grid-template-columns: 1.62fr 0.78fr; align-items:center; gap:18px; margin:auto 0;">
        <div>
          <h1 style="font-family:var(--font-title); font-size:clamp(28px,3.35vw,43px); font-weight:700; line-height:1.12; color:#202124; margin:0; letter-spacing:-0.6px;">
            P02 - Teori Neural<br />
            <span style="display:inline-block; padding-top:2px; background:linear-gradient(90deg, #EA4335 0%, #4285F4 55%, #34A853 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Network (ANN)</span>
          </h1>
          <div style="height:4px; width:100%; max-width:560px; border-radius:999px; margin:10px 0 12px; background:linear-gradient(90deg, #EA4335 0%, #FBBC04 35%, #34A853 70%, #4285F4 100%);"></div>
          <div style="font-size:clamp(15px,1.5vw,19.5px); font-weight:500; color:#5F6368; line-height:1.38;">
            Membongkar Isi &ldquo;Otak AI&rdquo; Langkah demi Langkah — dari Angka Piksel ke Tebakan Karakter Disney Frozen
          </div>
          <div style="margin-top:11px; display:inline-flex; align-items:center; gap:8px; background:#FFFFFF; border:1.5px solid #E0E3E7; border-radius:999px; padding:5px 14px 5px 7px; box-shadow:0 3px 10px rgba(234,67,53,0.08);">
            <span style="width:24px; height:24px; border-radius:50%; background:linear-gradient(135deg, #EA4335, #4285F4); color:#FFFFFF; font-family:var(--font-title); font-size:11px; font-weight:700; display:inline-flex; align-items:center; justify-content:center;">MH</span>
            <span style="font-size:13.5px; color:#5F6368;">Presented by <strong style="color:#202124; font-weight:700;">Muhammad Haerul</strong></span>
          </div>
        </div>

        <div style="display:flex; align-items:center; justify-content:center;">
          <svg viewBox="0 0 260 220" style="width:230px; height:195px;">
            <g stroke="#DADCE0" stroke-width="2">
              <line x1="42" y1="45" x2="130" y2="38"/><line x1="42" y1="45" x2="130" y2="110"/><line x1="42" y1="45" x2="130" y2="182"/>
              <line x1="42" y1="110" x2="130" y2="38"/><line x1="42" y1="110" x2="130" y2="110"/><line x1="42" y1="110" x2="130" y2="182"/>
              <line x1="42" y1="175" x2="130" y2="38"/><line x1="42" y1="175" x2="130" y2="110"/><line x1="42" y1="175" x2="130" y2="182"/>
              <line x1="130" y1="38" x2="218" y2="75"/><line x1="130" y1="38" x2="218" y2="145"/>
              <line x1="130" y1="110" x2="218" y2="75"/><line x1="130" y1="110" x2="218" y2="145"/>
              <line x1="130" y1="182" x2="218" y2="75"/><line x1="130" y1="182" x2="218" y2="145"/>
            </g>
            <circle cx="42" cy="45" r="16" fill="#4285F4" stroke="#FFF" stroke-width="3"/>
            <circle cx="42" cy="110" r="16" fill="#4285F4" stroke="#FFF" stroke-width="3"/>
            <circle cx="42" cy="175" r="16" fill="#4285F4" stroke="#FFF" stroke-width="3"/>
            <circle cx="130" cy="38" r="17" fill="#FBBC04" stroke="#FFF" stroke-width="3"/>
            <circle cx="130" cy="110" r="17" fill="#EA4335" stroke="#FFF" stroke-width="3"/>
            <circle cx="130" cy="182" r="17" fill="#FBBC04" stroke="#FFF" stroke-width="3"/>
            <circle cx="218" cy="75" r="18" fill="#34A853" stroke="#FFF" stroke-width="3"/>
            <circle cx="218" cy="145" r="18" fill="#34A853" stroke="#FFF" stroke-width="3"/>
            <text x="42" y="210" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#5F6368">Input</text>
            <text x="130" y="210" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#5F6368">Hidden</text>
            <text x="218" y="210" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#5F6368">Softmax</text>
          </svg>
        </div>
      </div>

      <div style="position:relative; z-index:1; display:flex; gap:6px; flex-wrap:wrap; align-items:center;">
        <span class="pill blue" style="font-size:10.5px; padding:4px 10px;">Neuron &amp; Layer</span>
        <span class="pill blue" style="font-size:10.5px; padding:4px 10px;">Weight &amp; Bias</span>
        <span class="pill red" style="font-size:10.5px; padding:4px 10px;">Aktivasi ReLU</span>
        <span class="pill green" style="font-size:10.5px; padding:4px 10px;">Softmax 5 Kelas</span>
        <span class="pill yellow" style="font-size:10.5px; padding:4px 10px;">Loss &amp; Backprop</span>
        <span class="pill solid-blue" style="font-size:10.5px; padding:4px 12px;">NumPy</span>
        <span class="pill" style="background:#EA4335; color:#FFFFFF; font-size:10.5px; padding:4px 12px;">Keras</span>
      </div>
    </section>

    <!-- 02: PETA PERJALANAN BELAJAR 5 BAB -->
    <section class="slide" data-title="Peta Perjalanan Belajar (5 Bab)" data-notes="Alokasi waktu: 1 menit. Ini alur belajar P02 yang disusun bertahap dengan bahasa sederhana hingga praktik kode: Bab 1 cara kerja Neuron & Layer, Bab 2 Fungsi Aktivasi (ReLU) dan Softmax, Bab 3 proses belajar (Loss, Gradient Descent, Backpropagation), Bab 4 batasan MLP pada foto Frozen, dan Bab 5 praktik.">
      <div class="kicker">PETA PERJALANAN BELAJAR</div>
      <h2>Memahami <span class="hl-red">Neural Network (ANN)</span> Pelan-Pelan (5 Bab)</h2>
      <p class="subtitle">Memakai istilah asli Deep Learning dengan <strong>penjelasan sederhana langkah demi langkah</strong> langsung pada foto 5 karakter Frozen kita.</p>
      <div class="step-list">
        <div class="step-item"><div class="step-num">01</div><div><div class="step-title">Bagaimana <em>Neuron</em> &amp; <em>Layer</em> Menilai Foto?</div><div class="step-desc">Dari cara mata mengenali ciri Elsa, diterjemahkan menjadi <code>Input × Weight + Bias</code> lalu disusun berlapis menjadi <em>Layer</em>.</div></div></div>
        <div class="step-item"><div class="step-num red">02</div><div><div class="step-title">Fungsi Aktivasi (<code>ReLU</code>) &amp; Probabilitas <code>Softmax</code></div><div class="step-desc">Kenapa neuron membutuhkan fungsi aktivasi non-linear dan bagaimana skor mentah diubah menjadi probabilitas <code>0–100%</code> untuk 5 karakter Frozen.</div></div></div>
        <div class="step-item"><div class="step-num green">03</div><div><div class="step-title">Bagaimana Model Belajar dari Kesalahan?</div><div class="step-desc">Dari bobot awal yang acak → mengukur kesalahan (<em>Loss</em>) → memperbarui bobot (<em>Gradient Descent, Learning Rate, Backpropagation</em>) → mengenali <em>Overfitting</em>.</div></div></div>
        <div class="step-item"><div class="step-num yellow">04</div><div><div class="step-title">Kenapa Foto Frozen Tidak Cukup Pakai MLP Biasa?</div><div class="step-desc">Dampak <em>Flatten</em> pada foto <strong>Elsa</strong> 2D &amp; ledakan 19,2 juta bobot — alasan logis menuju <strong>CNN (P03)</strong>!</div></div></div>
        <div class="step-item"><div class="step-num">05</div><div><div class="step-title">Praktik Santai di Notebook, Mini-Challenge &amp; Kuis</div><div class="step-desc">6 langkah kode pendek (5–15 baris/sel), menebak output Softmax tanpa kalkulator, kamus istilah, dan kuis 5 soal.</div></div></div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    s.append(
        make_agenda_slide(
            footer_label=FOOTER,
            notes="Alokasi waktu: 1 menit. Pembagian 120 menit persis seperti P01 agar ritme belajar nyaman dan ada jeda istirahat sebelum praktik kode.",
            blocks=[
                ("blue", "00–10 · Recap & Kenalan Frozen", "Menyambung angka piksel P01 dan mengenal 5 karakter proyek akhir Disney Frozen."),
                ("red", "10–40 · Teori Santai + 6 Simulator", "Belajar pelan lewat analogi sehari-hari & 6 simulator interaktif yang bisa langsung dicoba."),
                ("yellow", "40–45 · Istirahat Singkat", "Jeda 5 menit untuk minum air & meregangkan mata sebelum menyentuh kode."),
                ("green", "45–95 · Hands-On Notebook", "6 langkah kode super pendek: 1 neuron NumPy, Softmax, MLP Keras, & uji foto Frozen."),
                ("blue", "95–110 · Mini-Challenge", "Menebak peluang Softmax tanpa kalkulator & diskusi intuisi bersama."),
                ("red", "110–120 · Kuis & Penutup", "Kuis interaktif 5 soal, rangkuman 3 poin inti, dan preview P03 (CNN)."),
            ],
        )
    )

    s.append(
        f"""
    <!-- 04: TUJUAN BELAJAR (PADAT & KONKRET) -->
    <section class="slide" data-title="Apa yang Akan Kita Kuasai?" data-notes="Alokasi waktu: 1 menit. Tiga kemampuan konkret yang akan kamu kuasai setelah sesi ini — semuanya langsung bisa dicek di akhir kelas.">
      <div class="kicker">TUJUAN BELAJAR</div>
      <h2>3 Kemampuan Praktis yang <span class="hl-red">Langsung Bisa Kamu Lakukan</span></h2>
      <div class="grid-3">
        <div class="card" style="justify-content:space-between; padding:18px 20px;">
          <div class="card-top-bar bar-blue"></div>
          <div>
            <span class="pill blue">POIN 01 · NEURON &amp; LAYER</span>
            <div class="card-title" style="margin-top:8px;">Bisa Menghitung 1 Neuron dengan Tangan</div>
          </div>
          <div class="card-body" style="font-size:13.6px;">
            <ul>
              <li>Paham bahwa <strong>Neuron</strong> adalah unit hitung sederhana: <code>input × weight + bias</code>.</li>
              <li>Mengerti cara banyak neuron disusun berlapis dalam <em>Input, Hidden,</em> &amp; <em>Output Layer</em>.</li>
            </ul>
          </div>
          <div class="mini-box" style="background:var(--tint-blue); border-color:#C6DAFC; font-size:13px;"><strong>Contoh Target:</strong> Diberi <code>x=[1, 0.5]</code> &amp; bobotnya, kamu bisa menghitung skor <code>z</code> dalam 15 detik!</div>
          <div class="callout"><strong>Hasil:</strong> Neural Network terasa seperti hitungan sederhana, bukan sihir.</div>
        </div>
        <div class="card" style="justify-content:space-between; padding:18px 20px;">
          <div class="card-top-bar bar-red"></div>
          <div>
            <span class="pill red">POIN 02 · AKTIVASI &amp; SOFTMAX</span>
            <div class="card-title" style="margin-top:8px;">Paham Fungsi <code>ReLU</code> &amp; <code>Softmax</code></div>
          </div>
          <div class="card-body" style="font-size:13.6px;">
            <ul>
              <li>Tahu mengapa fungsi aktivasi <code>ReLU</code> dipakai di <em>hidden layer</em> agar model bisa membentuk pola non-linear.</li>
              <li>Tahu cara <code>Softmax</code> mengubah skor mentah menjadi probabilitas <strong>100%</strong> untuk 5 karakter Frozen.</li>
            </ul>
          </div>
          <div class="mini-box" style="background:var(--tint-red); border-color:#F6AEA9; font-size:13px;"><strong>Contoh Target:</strong> Paham kenapa output &ldquo;Elsa 85%, Anna 8%, ...&rdquo; jumlahnya selalu tepat <code>100%</code>!</div>
          <div class="callout red"><strong>Hasil:</strong> Bisa menjelaskan arti persentase prediksi model AI.</div>
        </div>
        <div class="card" style="justify-content:space-between; padding:18px 20px;">
          <div class="card-top-bar bar-green"></div>
          <div>
            <span class="pill green">POIN 03 · PROSES TRAINING</span>
            <div class="card-title" style="margin-top:8px;">Bisa Membaca Grafik Training AI</div>
          </div>
          <div class="card-body" style="font-size:13.6px;">
            <ul>
              <li>Paham alur <em>Loss → Gradient Descent → Backpropagation</em> dengan penjelasan sederhana.</li>
              <li>Bisa langsung mengenali grafik <strong>Overfitting</strong> &amp; paham mengapa foto butuh CNN.</li>
            </ul>
          </div>
          <div class="mini-box" style="background:var(--tint-green); border-color:#A8DAB5; font-size:13px;"><strong>Contoh Target:</strong> Melihat grafik <em>Train vs Val Loss</em>, kamu tahu apakah model belajar sehat atau menghafal!</div>
          <div class="callout green"><strong>Hasil:</strong> Siap melatih model pertama di Keras &amp; lanjut ke P03!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 05: RECAP P01 & PERKENALAN DATASET PROYEK NYATA FROZEN (DENGAN KPI STRIP!) -->
    <section class="slide" data-title="Recap P01 &amp; Dataset Proyek Nyata: Disney Frozen" data-notes="Alokasi waktu: 1.5 menit. Jembatan paling penting dari P01 ke P02! Ingatkan bahwa di P01 kita sudah ubah foto menjadi angka 0 sampai 1. Mulai hari ini, seluruh contoh memakai foto proyek asli kita: 5 karakter Disney Frozen.">
      <div class="kicker">TRANSISI P01 → P02 · DATASET PROYEK AKHIR</div>
      <h2>Dari Piksel P01 Menuju <span class="hl-blue">5 Karakter Disney Frozen</span></h2>
      <div class="split-60-40">
        <div style="display:flex; flex-direction:column; gap:9px; min-height:0;">
          <div class="img-box" style="flex:1; min-height:0; padding:7px;">
            <img src="assets/P02/01_frozen_gallery_5classes.png" alt="Galeri 5 Karakter Disney Frozen Polos vs Ramai" />
          </div>
          <div class="kpi-strip">
            <div class="kpi-mini"><div class="k-num">{total_imgs}</div><div class="k-lbl">Foto Asli (v1)</div></div>
            <div class="kpi-mini"><div class="k-num" style="color:#137333;">5 Kelas</div><div class="k-lbl">Anna s.d. Sven</div></div>
            <div class="kpi-mini"><div class="k-num" style="color:#EA4335;">{polos_n} / {ramai_n}</div><div class="k-lbl">Polos vs Ramai</div></div>
            <div class="kpi-mini"><div class="k-num" style="color:#B06000;">{sessions_n} Sesi</div><div class="k-lbl">Klaster Foto</div></div>
          </div>
        </div>
        <div class="card surface" style="gap:9px;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Menyambung Tepat dari Akhir P01</div>
          <div class="card-body" style="font-size:13.3px;">
            <ul>
              <li><strong>P01 (Sudah Selesai):</strong> Foto diubah jadi matriks angka <code>0.0–1.0</code>, ukurannya diseragamkan, &amp; dicek kebersihannya.</li>
              <li><strong>Kenapa Tidak Pakai <code>if-else</code>?</strong> Di P01 kita buktikan aturan manual langsung gagal kalau objek bergeser atau latarnya ramai!</li>
              <li><strong>Misi P02 Hari Ini:</strong> Membuka <strong>&ldquo;Kotak Hitam Otak AI&rdquo;</strong> — melihat bagaimana angka piksel foto <strong>Elsa</strong> diproses sampai keluar prediksi <strong>&ldquo;85% Elsa&rdquo;</strong>!</li>
            </ul>
          </div>
          <div class="callout"><strong>Catatan:</strong> Dataset <code>v1</code> berisi {total_imgs} foto dan bisa terus ditambah di versi berikutnya — semua kode kita membacanya secara otomatis!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    # =========================================================================
    # BAB 1: DARI CARA MANUSIA MENEBAK KE 1 NEURON & LAYER (SLIDE 06–16 · 11.5m)
    # =========================================================================
    s.append(
        make_divider_slide(
            bg_class="bg-blue",
            kicker="BAB 1 · ANATOMI NEURON & LAYER",
            title="Bagaimana <em>Neuron</em> &amp; <em>Layer</em> Menilai Foto?",
            description="Mulai dari cara manusia mengecek ciri foto tanpa rumus, lalu menerjemahkannya secara sederhana menjadi 1 Neuron hingga banyak Layer.",
            footer_label=FOOTER,
            data_title="Bab 1: Cara Neuron & Layer Menilai Foto",
            notes="Alokasi waktu: 0.5 menit. Masuk Bab 1! Kita mulai tanpa rumus sama sekali — dari cara kita sendiri mengenali karakter Frozen lalu langsung menghubungkannya ke konsep Neuron dan Layer.",
        )
    )

    s.append(
        f"""
    <!-- 07: STEP 1 (ZERO MATH) — BAGAIMANA MANUSIA MENEBAK ELSA? -->
    <section class="slide" data-title="Step 1: Bagaimana Kamu Sendiri Menebak Foto Elsa?" data-notes="Alokasi waktu: 1 menit. Mulai dari nol matematika! Tanya peserta: bagaimana otakmu langsung tahu foto ini Elsa? Pasti karena kamu mengumpulkan ciri visual (gaun biru, rambut pirang, tidak bertanduk) lalu menilai seberapa kuat tiap ciri.">
      <div class="kicker">BAB 1 · STEP 1 (NOL RUMUS!)</div>
      <h2>Bagaimana <span class="hl-blue">Kamu Sendiri</span> Tahu Foto Ini adalah Elsa?</h2>
      <div class="split-40-60">
        <div class="card tint-blue" style="align-items:center; justify-content:space-between; text-align:center;">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">CONTOH FOTO INPUT</span>
          <img src="assets/P02/thumb_elsa.jpg" alt="Foto Elsa" style="width:215px; height:215px; border-radius:14px; object-fit:cover; border:3px solid var(--blue); box-shadow:0 8px 20px rgba(66,133,244,0.2);" />
          <div class="mini-box" style="width:100%;">Otak manusia tidak menebak acak — kita otomatis mengecek <strong>ciri-ciri penting</strong> pada foto dan memberi bobot penilaian!</div>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Cara Otak Menilai Ciri Foto Elsa</div>
          <div class="step-list" style="gap:10px;">
            <div class="step-item" style="background:#FFF; padding:11px 14px;"><div class="step-num" style="background:#4285F4;">+3</div><div><div class="step-title">Apakah ada warna Biru Muda (gaun)?</div><div class="step-desc">Sangat khas Elsa → beri bobot positif besar <strong>+3</strong>.</div></div></div>
            <div class="step-item" style="background:#FFF; padding:11px 14px;"><div class="step-num green">+2</div><div><div class="step-title">Apakah ada rambut pirang / terang?</div><div class="step-desc">Mendukung ciri Elsa → beri bobot positif <strong>+2</strong>.</div></div></div>
            <div class="step-item" style="background:#FFF; padding:11px 14px;"><div class="step-num red">-5</div><div><div class="step-title">Apakah ada tanduk rusa besar?</div><div class="step-desc">Kalau ada, itu ciri Sven → beri bobot negatif besar <strong>-5</strong>.</div></div></div>
          </div>
          <div class="callout green"><strong>Intinya:</strong> Jika total skor ciri-cirinya <strong>melewati batas minimum</strong> → kita menyimpulkan <strong>&ldquo;Ini ELSA!&rdquo;</strong>. Cara kerja 1 <strong>Neuron</strong> di Neural Network persis seperti ini!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 08: STEP 2 — TERJEMAHAN KE ISTILAH NEURON AI -->
    <section class="slide" data-title="Step 2: Menghubungkan Cara Kerja Otak ke 1 Neuron AI" data-notes="Alokasi waktu: 1 menit. Sekarang kita pasangkan langsung istilah asli Deep Learning dengan penjelasan sederhananya: Ciri = Input (x), Tingkat Penting = Weight (w), Batas Ambang = Bias (b), Keputusan Akhir = Activation Function.">
      <div class="kicker">BAB 1 · STEP 2 (ISTILAH ASLI &amp; ARTI SEDERHANANYA)</div>
      <h2>Mengenal 4 Komponen Utama <span class="hl-blue">1 Neuron</span></h2>
      <div class="grid-2">
        <div class="card tint-blue" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">PENJELASAN SEDERHANA</span>
          <div class="step-list" style="gap:10px;">
            <div class="mini-box"><strong>1. Ciri pada Foto:</strong> &ldquo;Ada warna biru? Ada rambut pirang?&rdquo; (sinyal yang diterima dari foto).</div>
            <div class="mini-box"><strong>2. Seberapa Penting Tiap Ciri:</strong> Gaun biru penting (<code>+3</code>), tanduk rusa mengurangi skor (<code>-5</code>).</div>
            <div class="mini-box"><strong>3. Batas Ambang Minimal:</strong> Harus tembus minimal skor <code>3</code> agar dianggap cocok dengan Elsa.</div>
            <div class="mini-box"><strong>4. Aturan Keluaran:</strong> Teruskan sinyal jika skor positif/memenuhi syarat, atau ubah jadi <code>0</code> jika negatif.</div>
          </div>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <span class="pill red">ISTILAH RESMI DI NEURAL NETWORK</span>
          <div class="step-list" style="gap:10px;">
            <div class="mini-box" style="border-left:4px solid var(--blue);"><strong>1. Input (<code>x</code>):</strong> Angka masukan dari foto (mis. <code>1</code> = ada / terang, <code>0</code> = tidak ada / gelap).</div>
            <div class="mini-box" style="border-left:4px solid var(--red);"><strong>2. Weight / Bobot (<code>w</code>):</strong> Angka pengali yang menentukan seberapa besar pengaruh tiap input.</div>
            <div class="mini-box" style="border-left:4px solid var(--yellow);"><strong>3. Bias (<code>b</code>):</strong> Angka penambah untuk menggeser ambang batas aktifnya neuron (mis. <code>-3</code>).</div>
            <div class="mini-box" style="border-left:4px solid var(--green);"><strong>4. Activation Function:</strong> Fungsi di ujung neuron yang menentukan output akhir (mis. <code>ReLU</code>).</div>
          </div>
        </div>
      </div>
      <div class="callout" style="margin-top:10px;"><strong>Ingat Sederhananya:</strong> 1 <strong>Neuron</strong> bukanlah sesuatu yang rumit — ia hanyalah <strong>unit hitung kecil</strong> yang menghitung <code>input × weight + bias</code> lalu melewatkannya ke fungsi aktivasi.</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 09: STEP 3 — CONTOH HITUNG PELAN PAKAI ANGKA BULAT! -->
    <section class="slide" data-title="Step 3: Contoh Hitung Pelan Pakai Angka Bulat" data-notes="Alokasi waktu: 1 menit. Sebelum masuk desimal, hitung dulu pakai angka bulat super mudah! Bandingkan foto Elsa vs foto Sven melewati 1 neuron yang sama persis.">
      <div class="kicker">BAB 1 · STEP 3 (HITUNG PELAN ANGKA BULAT)</div>
      <h2>Simulasi Hitung Tangan: <span class="hl-blue">Foto Elsa</span> vs <span class="hl-red">Foto Sven</span></h2>
      <div class="grid-2">
        <div class="card tint-blue" style="justify-content:space-between; padding:16px 18px;">
          <div class="card-top-bar bar-blue"></div>
          <div style="display:flex; align-items:center; gap:12px;">
            <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:68px; height:68px; border-radius:10px; object-fit:cover; border:2px solid var(--blue);" />
            <div><span class="pill blue">KASUS A · FOTO ELSA</span><div class="card-title" style="margin-top:3px;">Input: Biru=1, Pirang=1, Tanduk=0</div></div>
          </div>
          <table class="io-table" style="font-size:13.8px;">
            <thead><tr><th>Ciri Input</th><th>Input (x)</th><th>Weight (w)</th><th>x × w</th></tr></thead>
            <tbody>
              <tr><td style="padding:10px 10px;">Gaun Biru</td><td style="padding:10px 10px;"><code>1</code></td><td style="padding:10px 10px;"><code>+3</code></td><td style="padding:10px 10px;"><strong>+3</strong></td></tr>
              <tr><td style="padding:10px 10px;">Rambut Pirang</td><td style="padding:10px 10px;"><code>1</code></td><td style="padding:10px 10px;"><code>+2</code></td><td style="padding:10px 10px;"><strong>+2</strong></td></tr>
              <tr><td style="padding:10px 10px;">Tanduk Rusa</td><td style="padding:10px 10px;"><code>0</code></td><td style="padding:10px 10px;"><code>-5</code></td><td style="padding:10px 10px;"><strong>0</strong></td></tr>
              <tr><td style="padding:10px 10px;"><strong>Bias (b)</strong></td><td colspan="2" style="padding:10px 10px;"><code>b = -3</code></td><td style="padding:10px 10px;"><strong>-3</strong></td></tr>
            </tbody>
          </table>
          <div class="callout green" style="font-size:13.4px;"><strong>Total Skor <code>z</code> = 3 + 2 + 0 − 3 = <code>+2</code> (&gt; 0) → Neuron AKTIF! &ldquo;Cocok Elsa&rdquo;</strong></div>
        </div>

        <div class="card tint-red" style="justify-content:space-between; padding:16px 18px;">
          <div class="card-top-bar bar-red"></div>
          <div style="display:flex; align-items:center; gap:12px;">
            <img src="assets/P02/thumb_sven.jpg" alt="Sven" style="width:68px; height:68px; border-radius:10px; object-fit:cover; border:2px solid var(--red);" />
            <div><span class="pill red">KASUS B · FOTO SVEN</span><div class="card-title" style="margin-top:3px;">Input: Biru=0, Pirang=0, Tanduk=1</div></div>
          </div>
          <table class="io-table" style="font-size:13.8px;">
            <thead><tr><th>Ciri Input</th><th>Input (x)</th><th>Weight (w)</th><th>x × w</th></tr></thead>
            <tbody>
              <tr><td style="padding:10px 10px;">Gaun Biru</td><td style="padding:10px 10px;"><code>0</code></td><td style="padding:10px 10px;"><code>+3</code></td><td style="padding:10px 10px;"><strong>0</strong></td></tr>
              <tr><td style="padding:10px 10px;">Rambut Pirang</td><td style="padding:10px 10px;"><code>0</code></td><td style="padding:10px 10px;"><code>+2</code></td><td style="padding:10px 10px;"><strong>0</strong></td></tr>
              <tr><td style="padding:10px 10px;">Tanduk Rusa</td><td style="padding:10px 10px;"><code>1</code></td><td style="padding:10px 10px;"><code>-5</code></td><td style="padding:10px 10px;"><strong>-5</strong></td></tr>
              <tr><td style="padding:10px 10px;"><strong>Bias (b)</strong></td><td colspan="2" style="padding:10px 10px;"><code>b = -3</code></td><td style="padding:10px 10px;"><strong>-3</strong></td></tr>
            </tbody>
          </table>
          <div class="callout red" style="font-size:13.4px;"><strong>Total Skor <code>z</code> = 0 + 0 − 5 − 3 = <code>-8</code> (≤ 0) → Neuron TIDAK AKTIF! &ldquo;Bukan Elsa&rdquo;</strong></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 10: STEP 4 — ANATOMI RESMI 1 NEURON (SVG + RUMUS) -->
    <section class="slide" data-title="Step 4: Diagram Resmi 1 Neuron (Input × Weight + Bias)" data-notes="Alokasi waktu: 1 menit. Sekarang setelah peserta lancar menghitung angka bulat di slide 9, tunjukkan diagram resmi 1 neuron — rumus z = x1*w1 + x2*w2 + x3*w3 + b sekarang terasa sangat familiar!">
      <div class="kicker">BAB 1 · STEP 4 (DIAGRAM RESMI 1 NEURON)</div>
      <h2>Anatomi Lengkap 1 Neuron: <span class="hl-blue"><code>Input × Weight + Bias</code></span></h2>
      <div class="split-60-40">
        <div class="card" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <svg viewBox="0 0 560 255" style="width:100%; height:auto;">
            <rect x="12" y="24" width="136" height="46" rx="11" fill="#FCE8E6" stroke="#EA4335" stroke-width="2"/>
            <text x="80" y="45" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#C5221F">x₁ : Merah (R)</text>
            <text x="80" y="61" text-anchor="middle" font-family="Roboto Mono" font-size="11" fill="#3C4043">nilai 0.0 – 1.0</text>

            <rect x="12" y="102" width="136" height="46" rx="11" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/>
            <text x="80" y="123" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#137333">x₂ : Hijau (G)</text>
            <text x="80" y="139" text-anchor="middle" font-family="Roboto Mono" font-size="11" fill="#3C4043">nilai 0.0 – 1.0</text>

            <rect x="12" y="180" width="136" height="46" rx="11" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
            <text x="80" y="201" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#1A73E8">x₃ : Biru (B)</text>
            <text x="80" y="217" text-anchor="middle" font-family="Roboto Mono" font-size="11" fill="#3C4043">nilai 0.0 – 1.0</text>

            <line x1="148" y1="47" x2="275" y2="125" stroke="#EA4335" stroke-width="2.5"/>
            <line x1="148" y1="125" x2="275" y2="125" stroke="#34A853" stroke-width="2.5"/>
            <line x1="148" y1="203" x2="275" y2="125" stroke="#4285F4" stroke-width="2.5"/>
            <rect x="184" y="62" width="44" height="20" rx="6" fill="#FFF" stroke="#EA4335"/><text x="206" y="76" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#C5221F">× w₁</text>
            <rect x="184" y="115" width="44" height="20" rx="6" fill="#FFF" stroke="#34A853"/><text x="206" y="129" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#137333">× w₂</text>
            <rect x="184" y="168" width="44" height="20" rx="6" fill="#FFF" stroke="#4285F4"/><text x="206" y="182" text-anchor="middle" font-family="Roboto Mono" font-size="11" font-weight="700" fill="#1A73E8">× w₃</text>

            <rect x="280" y="16" width="84" height="34" rx="9" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
            <text x="322" y="37" text-anchor="middle" font-family="Roboto Mono" font-size="12" font-weight="700" fill="#B06000">+ Bias (b)</text>
            <line x1="322" y1="50" x2="322" y2="82" stroke="#FBBC04" stroke-width="2.5"/>

            <circle cx="322" cy="125" r="43" fill="#202124" stroke="#4285F4" stroke-width="3"/>
            <text x="322" y="121" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#FFF">Σ + b</text>
            <text x="322" y="139" text-anchor="middle" font-family="Roboto Mono" font-size="11" fill="#FBBC04">skor z</text>

            <line x1="365" y1="125" x2="408" y2="125" stroke="#202124" stroke-width="2.5"/>
            <rect x="408" y="95" width="76" height="60" rx="12" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2"/>
            <text x="446" y="120" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#1A73E8">Aktivasi</text>
            <text x="446" y="137" text-anchor="middle" font-family="Roboto Mono" font-size="10.5" fill="#3C4043">f(z)</text>

            <line x1="484" y1="125" x2="508" y2="125" stroke="#34A853" stroke-width="2.5"/>
            <circle cx="530" cy="125" r="22" fill="#34A853"/>
            <text x="530" y="129" text-anchor="middle" font-family="Poppins" font-size="12" font-weight="700" fill="#FFF">Out</text>
          </svg>
          <div class="formula-box">z = (x₁ · w₁) + (x₂ · w₂) + (x₃ · w₃) + b &nbsp;→&nbsp; output = f(z)</div>
        </div>

        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <div class="card-title">Ringkasan 3 Kunci yang Wajib Diingat</div>
          <div class="card-body" style="font-size:13.4px;">
            <ul>
              <li><strong>Weight (<code>w</code>):</strong> Angka pengali yang menentukan seberapa penting tiap input. Positif = dukung, Negatif = kurangi, Nol = abaikan.</li>
              <li><strong>Bias (<code>b</code>):</strong> Angka penggeser ambang batas minimal agar neuron aktif.</li>
              <li><strong>Aktivasi (<code>f(z)</code>):</strong> Fungsi di ujung neuron yang mengubah skor <code>z</code> menjadi output akhir (dibahas tuntas di Bab 2).</li>
            </ul>
          </div>
          <div class="mini-box" style="background:#FFF;"><strong>Rahasia Deep Learning:</strong> Manusia <em>tidak</em> mengetik angka <code>w</code> dan <code>b</code> satu per satu — komputer yang <strong>mencarinya otomatis</strong> dari foto latihan!</div>
          <div class="callout yellow"><strong>Siap Mencoba?</strong> Di slide berikutnya kita geser langsung bobot <code>w</code> &amp; <code>b</code> pada foto asli Elsa, Anna, dan Olaf!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 11: STEP 5 — SIMULATOR #1 (KALKULATOR 1 NEURON + BAR KONTRIBUSI LIVE!) -->
    <section class="slide" data-title="Simulator #1: Kalkulator 1 Neuron (Foto Frozen Nyata)" data-notes="Alokasi waktu: 1.5 menit. Demo interaktif! Klik Elsa, Anna, atau Olaf, lalu geser slider bobot dan bias. Tunjukkan bahwa dengan bobot bawaan, Elsa menghasilkan z positif (AKTIF) sedangkan Anna menghasilkan z negatif (TIDAK AKTIF / ReLU = 0).">
      <div class="kicker">BAB 1 · STEP 5 · SIMULATOR INTERAKTIF #1</div>
      <h2>Coba Sendiri: <span class="hl-blue">Kalkulator 1 Neuron</span> pada Foto Frozen</h2>
      <div class="split-40-60">
        <div class="card surface" style="gap:9px; padding:14px 16px; justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div style="font-family:var(--font-title); font-size:13px; font-weight:700;">1. Pilih Foto Input Nyata (<code>data/frozen_v1/</code>)</div>
          <div id="n1-presets" class="sim-bar pdf-keep-ui">
            <button type="button" class="btn-ui" data-char="elsa" onclick="setN1Char('elsa')" style="padding:5px 11px; font-size:12px;">Elsa</button>
            <button type="button" class="btn-ui outline" data-char="anna" onclick="setN1Char('anna')" style="padding:5px 11px; font-size:12px;">Anna</button>
            <button type="button" class="btn-ui outline" data-char="olaf" onclick="setN1Char('olaf')" style="padding:5px 11px; font-size:12px;">Olaf</button>
          </div>
          <div style="display:flex; align-items:center; gap:11px; background:#FFF; border:1px solid var(--border); border-radius:11px; padding:8px 10px;">
            <img id="n1-img" src="assets/P02/thumb_elsa.jpg" alt="Sample Frozen" style="width:64px; height:64px; border-radius:9px; object-fit:cover; border:1px solid var(--border);" />
            <div style="font-size:12px; line-height:1.42;">
              <div id="n1-char-name" style="font-family:var(--font-title); font-weight:700; font-size:14px; color:var(--blue-text);">Elsa (Foto Asli)</div>
              <div id="n1-rgb-txt" style="font-family:var(--font-code); font-size:11.5px; color:#3C4043;">R=0.67 · G=0.66 · B=0.67</div>
              <div style="font-size:10.8px; color:var(--muted);">Rata-rata RGB area figurine (0.0–1.0)</div>
            </div>
          </div>
          <div style="font-family:var(--font-title); font-size:13px; font-weight:700;">2. Geser Weight (<code>w</code>) &amp; Bias (<code>b</code>)</div>
          <div class="sim-slider-row"><span>w₁ (Merah R)</span><input id="n1-w1" type="range" min="-3" max="3" step="0.1" value="-1.5" oninput="updateN1()"/><span id="n1-w1-v" class="sim-val">-1.5</span></div>
          <div class="sim-slider-row"><span>w₂ (Hijau G)</span><input id="n1-w2" type="range" min="-3" max="3" step="0.1" value="1.5" oninput="updateN1()"/><span id="n1-w2-v" class="sim-val">+1.5</span></div>
          <div class="sim-slider-row"><span>w₃ (Biru B)</span><input id="n1-w3" type="range" min="-3" max="3" step="0.1" value="2.5" oninput="updateN1()"/><span id="n1-w3-v" class="sim-val">+2.5</span></div>
          <div class="sim-slider-row"><span>Bias (b)</span><input id="n1-b" type="range" min="-2" max="2" step="0.1" value="-1.3" oninput="updateN1()"/><span id="n1-b-v" class="sim-val">-1.3</span></div>
        </div>

        <div class="card" style="gap:9px; justify-content:space-between; padding:14px 18px;">
          <div class="card-top-bar bar-green"></div>
          <div style="font-family:var(--font-title); font-size:14px; font-weight:700;">3. Bedah Sumbangan Tiap Input &amp; Skor Akhir</div>
          <div id="n1-eq" class="formula-box" style="font-size:11.8px; text-align:left; padding:7px 11px;">z = ...</div>
          <!-- Live contribution bars (fills center space cleanly with huge pedagogical value!) -->
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:11px; padding:9px 12px; display:flex; flex-direction:column; gap:6px;">
            <div style="font-size:11px; font-weight:700; color:var(--muted); display:flex; justify-content:space-between;"><span>Sumbangan Tiap Komponen ke Skor z</span><span>Kiri (−) | Kanan (+)</span></div>
            <div class="contrib-row"><span>x₁·w₁ (R)</span><div class="contrib-track"><div class="contrib-mid"></div><div id="n1-cb0" class="contrib-bar"></div></div><span id="n1-cv0" class="sim-val">0.00</span></div>
            <div class="contrib-row"><span>x₂·w₂ (G)</span><div class="contrib-track"><div class="contrib-mid"></div><div id="n1-cb1" class="contrib-bar"></div></div><span id="n1-cv1" class="sim-val">0.00</span></div>
            <div class="contrib-row"><span>x₃·w₃ (B)</span><div class="contrib-track"><div class="contrib-mid"></div><div id="n1-cb2" class="contrib-bar"></div></div><span id="n1-cv2" class="sim-val">0.00</span></div>
            <div class="contrib-row"><span>Bias (b)</span><div class="contrib-track"><div class="contrib-mid"></div><div id="n1-cb3" class="contrib-bar"></div></div><span id="n1-cv3" class="sim-val">0.00</span></div>
          </div>
          <div class="grid-3" style="flex:0 0 auto; gap:10px;">
            <div class="card tint-blue" style="padding:9px; gap:2px; align-items:center; text-align:center;">
              <span style="font-size:10.5px; font-weight:700; color:var(--blue-text);">SKOR MENTAH (z)</span>
              <div id="n1-z" class="big-num" style="font-size:25px; color:var(--dark);">+0.36</div>
            </div>
            <div class="card tint-green" style="padding:9px; gap:2px; align-items:center; text-align:center;">
              <span style="font-size:10.5px; font-weight:700; color:#137333;">OUTPUT ReLU</span>
              <div id="n1-relu" class="big-num" style="font-size:25px; color:#137333;">0.36</div>
            </div>
            <div class="card tint-yellow" style="padding:9px; gap:2px; align-items:center; text-align:center;">
              <span style="font-size:10.5px; font-weight:700; color:#B06000;">SIGMOID (0–100%)</span>
              <div id="n1-sig" class="big-num" style="font-size:25px; color:#B06000;">59%</div>
            </div>
          </div>
          <div id="n1-status" class="callout green" style="padding:8px 12px; font-size:12.8px;">Neuron AKTIF!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 12: STEP 6 — MENGAPA BUTUH BIAS? (DENGAN SVG VISUAL KONKRET — ZERO OVERLAP!) -->
    <section class="slide" data-title="Step 6: Mengapa Harus Ada Bias (b)?" data-notes="Alokasi waktu: 1 menit. Tunjukkan secara visual beda garis tanpa bias (terkunci di nol) vs dengan bias (bisa digeser sesuai ambang batas atau kecerahan dasar foto).">
      <div class="kicker">BAB 1 · STEP 6 · PERAN BIAS</div>
      <h2>Kenapa Harus Ditambah <span class="hl-yellow">Bias (<code>b</code>)</span>?</h2>
      <div class="grid-2">
        <div class="card tint-red" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <span class="pill red">TANPA BIAS (z = w · x)</span>
          <div class="card-title">Batas Terkunci di Titik Nol (Kaku!)</div>
          <svg viewBox="0 0 360 122" style="width:100%; height:auto; background:#FFF; border-radius:10px; border:1px solid #F6AEA9;">
            <line x1="28" y1="94" x2="340" y2="94" stroke="#9AA0A6" stroke-width="1.5"/>
            <line x1="56" y1="12" x2="56" y2="106" stroke="#9AA0A6" stroke-width="1.5"/>
            <line x1="56" y1="94" x2="310" y2="20" stroke="#EA4335" stroke-width="3"/>
            <circle cx="56" cy="94" r="6" fill="#EA4335"/>
            <text x="68" y="112" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#C5221F">Terkunci di (0, 0)!</text>
            <text x="242" y="80" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#C5221F">Hanya bisa diputar, tak bisa digeser</text>
          </svg>
          <div class="card-body" style="font-size:13.2px;">
            <ul>
              <li>Jika semua input <code>0</code>, hasilnya <strong>pasti selalu <code>0</code></strong>.</li>
              <li>Sulit menyesuaikan diri saat foto <strong>polos terang vs redup</strong> punya tingkat kecerahan dasar berbeda!</li>
            </ul>
          </div>
        </div>
        <div class="card tint-green" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">DENGAN BIAS (z = w · x + b)</span>
          <div class="card-title">Bebas Mengatur Ambang Batas Aktif!</div>
          <svg viewBox="0 0 360 122" style="width:100%; height:auto; background:#FFF; border-radius:10px; border:1px solid #A8DAB5;">
            <line x1="28" y1="94" x2="340" y2="94" stroke="#9AA0A6" stroke-width="1.5"/>
            <line x1="56" y1="12" x2="56" y2="106" stroke="#9AA0A6" stroke-width="1.5"/>
            <line x1="56" y1="94" x2="310" y2="20" stroke="#DADCE0" stroke-width="2" stroke-dasharray="5 4"/>
            <line x1="56" y1="54" x2="310" y2="14" stroke="#34A853" stroke-width="3"/>
            <circle cx="56" cy="54" r="6" fill="#34A853"/>
            <text x="68" y="34" font-family="Roboto Mono" font-size="10.5" font-weight="700" fill="#137333">Digeser sebesar +b!</text>
            <text x="234" y="84" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#137333">Ambang aktif jadi fleksibel</text>
          </svg>
          <div class="card-body" style="font-size:13.2px;">
            <ul>
              <li><strong>Bias negatif</strong> → neuron jadi lebih &ldquo;ketat&rdquo; (hanya aktif jika ciri Elsa sangat jelas).</li>
              <li><strong>Bias positif</strong> → neuron lebih mudah aktif. Persis seperti angka <code>c</code> pada <code>y = mx + c</code>!</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 13: STEP 7 — DARI 1 NEURON KE BANYAK LAYER (MLP) -->
    <section class="slide" data-title="Step 7: Dari 1 Neuron ke Banyak Layer (MLP)" data-notes="Alokasi waktu: 1 menit. Satu neuron hanya bisa mengecek 1 pola sederhana. Untuk mengenali 5 karakter Frozen yang kompleks, kita susun puluhan neuron berlapis: Input Layer -> Hidden Layer -> Output Layer.">
      <div class="kicker">BAB 1 · STEP 7 · DARI 1 NEURON KE BANYAK LAYER</div>
      <h2>Satu Neuron Tidak Cukup → Susun <span class="hl-blue">Multi-Layer Perceptron (MLP)</span></h2>
      <div class="split-60-40">
        <div class="card" style="justify-content:center; align-items:center;">
          <div class="card-top-bar bar-blue"></div>
          <svg viewBox="0 0 560 285" style="width:100%; height:auto;">
            <rect x="16" y="22" width="110" height="232" rx="14" fill="#E8F0FE" stroke="#C6DAFC" stroke-width="1.5"/>
            <rect x="168" y="22" width="116" height="232" rx="14" fill="#FEF7E0" stroke="#FDE293" stroke-width="1.5"/>
            <rect x="326" y="22" width="90" height="232" rx="14" fill="#FCE8E6" stroke="#F6AEA9" stroke-width="1.5"/>
            <rect x="454" y="22" width="94" height="232" rx="14" fill="#E6F4EA" stroke="#A8DAB5" stroke-width="1.5"/>
            <g stroke="#9AA0A6" stroke-width="1.1" opacity="0.6">
              <line x1="71" y1="68" x2="226" y2="62"/><line x1="71" y1="68" x2="226" y2="112"/><line x1="71" y1="68" x2="226" y2="162"/><line x1="71" y1="68" x2="226" y2="212"/>
              <line x1="71" y1="138" x2="226" y2="62"/><line x1="71" y1="138" x2="226" y2="112"/><line x1="71" y1="138" x2="226" y2="162"/><line x1="71" y1="138" x2="226" y2="212"/>
              <line x1="71" y1="208" x2="226" y2="62"/><line x1="71" y1="208" x2="226" y2="112"/><line x1="71" y1="208" x2="226" y2="162"/><line x1="71" y1="208" x2="226" y2="212"/>
              <line x1="226" y1="62" x2="371" y2="95"/><line x1="226" y1="62" x2="371" y2="180"/>
              <line x1="226" y1="112" x2="371" y2="95"/><line x1="226" y1="112" x2="371" y2="180"/>
              <line x1="226" y1="162" x2="371" y2="95"/><line x1="226" y1="162" x2="371" y2="180"/>
              <line x1="226" y1="212" x2="371" y2="95"/><line x1="226" y1="212" x2="371" y2="180"/>
              <line x1="371" y1="95" x2="501" y2="54"/><line x1="371" y1="95" x2="501" y2="96"/><line x1="371" y1="95" x2="501" y2="138"/><line x1="371" y1="95" x2="501" y2="180"/><line x1="371" y1="95" x2="501" y2="222"/>
              <line x1="371" y1="180" x2="501" y2="54"/><line x1="371" y1="180" x2="501" y2="96"/><line x1="371" y1="180" x2="501" y2="138"/><line x1="371" y1="180" x2="501" y2="180"/><line x1="371" y1="180" x2="501" y2="222"/>
            </g>
            <circle cx="71" cy="68" r="15" fill="#4285F4"/><text x="71" y="72" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#FFF">x₁</text>
            <circle cx="71" cy="138" r="15" fill="#4285F4"/><text x="71" y="142" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#FFF">x₂</text>
            <circle cx="71" cy="208" r="15" fill="#4285F4"/><text x="71" y="212" text-anchor="middle" font-family="Roboto Mono" font-size="10" font-weight="700" fill="#FFF">xₙ</text>
            <circle cx="226" cy="62" r="14" fill="#FBBC04"/><circle cx="226" cy="112" r="14" fill="#FBBC04"/>
            <circle cx="226" cy="162" r="14" fill="#FBBC04"/><circle cx="226" cy="212" r="14" fill="#FBBC04"/>
            <circle cx="371" cy="95" r="15" fill="#EA4335"/><circle cx="371" cy="180" r="15" fill="#EA4335"/>
            <circle cx="501" cy="54" r="13" fill="#34A853"/><text x="501" y="57" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#FFF">An</text>
            <circle cx="501" cy="96" r="13" fill="#34A853"/><text x="501" y="99" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#FFF">El</text>
            <circle cx="501" cy="138" r="13" fill="#34A853"/><text x="501" y="141" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#FFF">Kr</text>
            <circle cx="501" cy="180" r="13" fill="#34A853"/><text x="501" y="183" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#FFF">Ol</text>
            <circle cx="501" cy="222" r="13" fill="#34A853"/><text x="501" y="225" text-anchor="middle" font-family="Poppins" font-size="8.5" font-weight="700" fill="#FFF">Sv</text>
            <text x="71" y="274" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#1A73E8">Input Layer</text>
            <text x="226" y="274" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#B06000">Hidden 1 (Warna)</text>
            <text x="371" y="274" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#C5221F">Hidden 2</text>
            <text x="501" y="274" text-anchor="middle" font-family="Poppins" font-size="11" font-weight="700" fill="#137333">Output (5)</text>
          </svg>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Pembagian Tugas Setiap <em>Layer</em></div>
          <div class="card-body" style="font-size:13.3px;">
            <ul>
              <li><strong>Input Layer:</strong> Pintu masuk angka piksel foto (hanya meneruskan data).</li>
              <li><strong>Hidden Layer 1 &amp; 2 (<code>Dense</code>):</strong> Lapisan neuron di tengah jaringan! Sebagian neuron mendeteksi warna biru, sebagian mendeteksi warna putih salju, lalu lapisan berikutnya menggabungkannya.</li>
              <li><strong>Output Layer:</strong> <strong>5 neuron keluaran</strong> (masing-masing mewakili <code>Anna, Elsa, Kristoff, Olaf, Sven</code>).</li>
            </ul>
          </div>
          <div class="callout green">Inilah alasan disebut <strong><em>Deep</em> Learning</strong> — karena memiliki banyak <em>Hidden Layer</em> yang saling bertumpuk!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 14: STEP 8 — FORWARD PASS LENGKAP (ZERO WHITESPACE!) -->
    <section class="slide" data-title="Step 8: Forward Pass — Perjalanan Foto dari Kiri ke Kanan" data-notes="Alokasi waktu: 1.5 menit. Tunjukkan alur maju (Forward Pass) secara konkret: setiap kolom memperlihatkan foto/angka, dimensi data, dan peran layer-nya.">
      <div class="kicker">BAB 1 · STEP 8 · ALUR MAJU (FORWARD PASS)</div>
      <h2><em>Forward Pass</em>: Perjalanan 1 Foto Elsa Menjadi <span class="hl-green">Tebakan 87.8%</span></h2>
      <div class="grid-4" style="align-items:stretch;">
        <div class="card tint-blue" style="padding:13px; justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div><span class="pill blue">TAHAP 1</span><div class="card-title" style="font-size:15px; margin-top:4px;">Foto Masuk</div></div>
          <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:110px; height:110px; border-radius:11px; object-fit:cover; margin:0 auto; border:2px solid var(--blue);" />
          <div class="card-body" style="font-size:12.4px;">Angka piksel <code>0.0–1.0</code> hasil P01 masuk dari pintu kiri.</div>
          <div class="formula-box" style="font-size:11px; padding:5px;">Input: angka piksel</div>
        </div>
        <div class="card tint-yellow" style="padding:13px; justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <div><span class="pill yellow">TAHAP 2</span><div class="card-title" style="font-size:15px; margin-top:4px;">Tim Hidden + ReLU</div></div>
          <div class="mini-box" style="font-size:11.8px;">
            &bull; Neuron #1 (Biru): <strong>+2.4</strong><br/>
            &bull; Neuron #2 (Pirang): <strong>+1.8</strong><br/>
            &bull; Neuron #3 (Tanduk): <strong>0.0</strong> <em>(padam)</em><br/>
            &bull; ... hingga 64/128 neuron!
          </div>
          <div class="card-body" style="font-size:12.4px;">Tiap neuron menghitung <code>w·x + b</code> lalu disaring <code>ReLU</code>.</div>
          <div class="formula-box" style="font-size:11px; padding:5px;">Output: 128 angka ciri</div>
        </div>
        <div class="card tint-red" style="padding:13px; justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div><span class="pill red">TAHAP 3</span><div class="card-title" style="font-size:15px; margin-top:4px;">5 Skor Mentah</div></div>
          <pre class="code" style="font-size:11px; padding:9px;">Anna     : +0.8
Elsa     : +3.4
Kristoff : -0.6
Olaf     : +0.1
Sven     : -1.2</pre>
          <div class="card-body" style="font-size:12.4px;">Disebut <strong><em>logits</em></strong> (skor mentah, belum berbentuk persen).</div>
          <div class="formula-box" style="font-size:11px; padding:5px;">Output: 5 skor mentah</div>
        </div>
        <div class="card tint-green" style="padding:13px; justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div><span class="pill green">TAHAP 4</span><div class="card-title" style="font-size:15px; margin-top:4px;">Persentase Softmax</div></div>
          <pre class="code" style="font-size:11px; padding:9px; background:#133822;">Elsa     : 87.8% ★
Anna     :  6.5%
Olaf     :  3.2%
Kristoff :  1.6%
Sven     :  0.9%</pre>
          <div class="card-body" style="font-size:12.4px;">Total peluang tepat <strong>100%</strong> → AI memilih <strong>ELSA!</strong></div>
          <div class="formula-box" style="font-size:11px; padding:5px; border-color:#A8DAB5;">Prediksi Akhir: ELSA</div>
        </div>
      </div>
      <div class="callout" style="margin-top:10px;"><strong>Pengingat:</strong> Aliran maju dari Tahap 1 → 4 ini disebut <strong><em>Forward Pass</em></strong>. Nanti di Bab 3 kita lihat bagaimana AI belajar kalau tebakan Tahap 4 ini meleset!</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    s.append(
        _qa_slide(
            qa_id="qa1",
            qa_num=1,
            kicker="TANYA-JAWAB #1 · LATIHAN HITUNG TANGAN",
            title_html='Coba Hitung Sendiri: <span class="hl-blue">Berapa Skor <code>z</code> Neuron Ini?</span>',
            question_html="Sebuah neuron menerima 2 input <code>x = [0.8, 0.2]</code> dengan bobot <code>w = [2.0, -1.0]</code> dan bias <code>b = 0.5</code>. Berapakah nilai skor mentah <code>z</code>?",
            choices=[
                "<strong>A.</strong> <code>z = 1.4</code>",
                "<strong>B.</strong> <code>z = 1.9</code>",
                "<strong>C.</strong> <code>z = 2.3</code>",
            ],
            answer_html="<strong>Jawaban: B — Tepatnya <code>z = 1.9</code>!</strong><br/>Langkah: <code>(0.8 × 2.0) + (0.2 × -1.0) + 0.5 = 1.6 − 0.2 + 0.5 = 1.9</code>. Karena positif, jika masuk <code>ReLU</code> neuron langsung menyala!",
            vis_q_html='<span class="pill blue">PETUNJUK RUMUS</span><div class="formula-box" style="margin:12px 0; font-size:14px;">z = (x₁ · w₁) + (x₂ · w₂) + b</div><div class="mini-box">Hitung pelan-pelan:<br/>1) <code>0.8 × 2.0 = ?</code><br/>2) <code>0.2 × (-1.0) = ?</code><br/>3) Tambahkan <code>+ 0.5</code>!</div>',
            vis_a_html='<span class="pill green">RINCIAN HITUNGAN</span><div class="mini-box" style="text-align:left; font-family:var(--font-code); font-size:12.8px; margin-top:10px;">1) 0.8 × 2.0  = +1.6<br/>2) 0.2 × -1.0 = -0.2<br/>3) Bias b     = +0.5<br/>--------------------<br/><strong>Total skor z  = +1.9 ★</strong></div><div class="callout green" style="margin-top:8px;">Skor positif → Neuron AKTIF!</div>',
            notes="Alokasi waktu: 1 menit. Beri waktu 30 detik agar peserta menghitung 1 neuron dengan tangan memakai petunjuk di kartu kanan, lalu klik Reveal.",
        )
    )

    s.append(
        _qa_slide(
            qa_id="qa2",
            qa_num=2,
            kicker="TANYA-JAWAB #2 · KONSEP BIAS",
            title_html='Cek Pemahaman: <span class="hl-yellow">Apa Fungsi Bias (<code>b</code>)?</span>',
            question_html="Mengapa setiap neuron menambahkan angka <code>bias (b)</code> setelah menghitung <code>input × weight</code>?",
            choices=[
                "<strong>A.</strong> Agar jumlah file foto di folder bertambah banyak",
                "<strong>B.</strong> Untuk menggeser ambang nyala neuron agar tidak terkunci di titik nol <code>(0, 0)</code>",
                "<strong>C.</strong> Agar semua foto berubah menjadi hitam-putih",
            ],
            answer_html="<strong>Jawaban: B — Menggeser ambang nyala neuron!</strong><br/>Dengan <code>bias</code>, neuron bisa mengatur sendiri seberapa ketat/mudahnya ia menyala terhadap sebuah pola (persis seperti standar kelulusan).",
            vis_q_html='<span class="pill yellow">INGAT ANALOGI</span><div class="big-num" style="color:#B06000; margin:12px 0;">y = m·x + c</div><div class="mini-box">Di rumus garis sederhana, <code>w</code> mengatur kemiringan, sedangkan <strong><code>b</code></strong> berperan sebagai <code>c</code> yang menggeser posisi garis!</div>',
            vis_a_html='<span class="pill green">TEPAT SEKALI!</span><div class="big-num" style="color:#137333; margin:10px 0;">z = w·x + b</div><div class="mini-box"><strong>Bias negatif besar</strong> → neuron lebih ketat.<br/><strong>Bias positif</strong> → neuron lebih mudah aktif.<br/>Tanpa bias, input 0 selalu menghasilkan 0!</div>',
            notes="Alokasi waktu: 1 menit. Pastikan peserta benar-benar paham peran bias sebelum lanjut ke Bab 2 (Fungsi Aktivasi & Softmax).",
        )
    )

    # =========================================================================
    # BAB 2: FUNGSI AKTIVASI (ReLU) & SOFTMAX (SLIDE 17–26 · 11.5 menit)
    # =========================================================================
    s.append(
        make_divider_slide(
            bg_class="bg-red",
            kicker="BAB 2 · FUNGSI AKTIVASI & SOFTMAX",
            title="Fungsi Aktivasi (<code>ReLU</code>) &amp; Probabilitas <code>Softmax</code>",
            description="Mengenal 2 komponen wajib agar jaringan bisa memahami pola non-linear dan mengeluarkan prediksi dalam bentuk persentase 0–100%.",
            footer_label=FOOTER,
            data_title="Bab 2: Fungsi Aktivasi & Softmax",
            notes="Alokasi waktu: 0.5 menit. Masuk Bab 2! Kita pelajari dulu Fungsi Aktivasi ReLU secara sederhana, lalu bagaimana Softmax menghasilkan probabilitas 100%.",
        )
    )

    s.append(
        f"""
    <!-- 18: STEP 1 (ZERO MATH) — MENGENAL ReLU DENGAN SEDERHANA -->
    <section class="slide" data-title="Step 1: Mengenal Fungsi Aktivasi ReLU Secara Sederhana" data-notes="Alokasi waktu: 1 menit. Jelaskan ReLU pakai bahasa sehari-hari dulu sebelum menyebut istilah non-linearitas! Aturannya cuma 1 kalimat: kalau negatif ubah jadi 0, kalau positif biarkan tetap.">
      <div class="kicker">BAB 2 · STEP 1 (ATURAN PALING SEDERHANA DI DEEP LEARNING)</div>
      <h2>Mengenal <span class="hl-blue"><code>ReLU</code></span>: &ldquo;Ubah Negatif Jadi Nol!&rdquo;</h2>
      <div class="grid-2">
        <div class="card tint-blue" style="justify-content:space-between; padding:16px 18px;">
          <div class="card-top-bar bar-blue"></div>
          <div>
            <span class="pill blue">ATURAN 1 KALIMAT</span>
            <div class="card-title" style="margin-top:6px;">Jika Negatif → Ubah Jadi <code>0</code>. Jika Positif → Biarkan!</div>
          </div>
          <div class="formula-box" style="font-size:16px; padding:11px 14px;">ReLU(z) = max(0, z)</div>
          <table class="io-table" style="font-size:13.5px;">
            <thead><tr><th>Skor Masuk (z)</th><th>Output ReLU</th><th>Artinya di Neuron</th></tr></thead>
            <tbody>
              <tr><td style="padding:10px 10px;"><code>-8.0</code> (foto Sven di neuron Elsa)</td><td style="padding:10px 10px;"><strong><code>0.0</code></strong></td><td style="padding:10px 10px;">Tidak aktif / Tidak cocok</td></tr>
              <tr><td style="padding:10px 10px;"><code>-0.5</code></td><td style="padding:10px 10px;"><strong><code>0.0</code></strong></td><td style="padding:10px 10px;">Tidak aktif / Diabaikan</td></tr>
              <tr><td style="padding:10px 10px;"><code>+2.0</code> (foto Elsa di neuron Elsa)</td><td style="padding:10px 10px;"><strong><code>+2.0</code></strong></td><td style="padding:10px 10px;">Aktif! Teruskan sinyal kuat</td></tr>
            </tbody>
          </table>
        </div>
        <div class="card surface" style="justify-content:space-between; padding:16px 18px;">
          <div class="card-top-bar bar-red"></div>
          <div>
            <span class="pill red">KENAPA HARUS ADA &ldquo;PATAHAN&rdquo; DI NOL?</span>
            <div class="card-title" style="margin-top:6px;">Supaya Model Bisa Membuat Batas Melengkung!</div>
          </div>
          <div class="card-body" style="font-size:13.6px;">
            <ul>
              <li>Bayangkan <strong>tanpa fungsi aktivasi <code>ReLU</code></strong>: semua angka hanya dikali dan ditambah lurus saja.</li>
              <li>Kalau 10 lapisan hanya melakukan perkalian lurus, secara matematika hasilnya tetap <strong>1 garis lurus biasa</strong> — model tidak bisa mengenali bentuk rumit!</li>
              <li>Dengan patahan <code>0</code> dari <code>ReLU</code>, setiap neuron bisa <strong>membelokkan batas keputusan</strong> sehingga gabungan puluhan neuron mampu melingkari bentuk wajah, gaun, &amp; tanduk karakter Frozen!</li>
            </ul>
          </div>
          <div class="callout red"><strong>Sederhananya:</strong> Tanpa <code>ReLU</code>, model hanya bisa menarik 1 garis lurus; dengan <code>ReLU</code>, model bisa melipat batas mengikuti bentuk objek!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 19: STEP 2 — BUKTI VISUAL GARIS LURUS VS MELENGKUNG -->
    <section class="slide" data-title="Step 2: Bukti Visual Garis Lurus vs Melengkung" data-notes="Alokasi waktu: 1.5 menit. Tunjukkan gambar kiri (1 garis lurus gagal memisahkan titik biru di tengah) vs gambar kanan (dengan ReLU, batas bisa melengkung melingkari kelompok Elsa!).">
      <div class="kicker">BAB 2 · STEP 2 · BUKTI VISUAL NON-LINEARITAS</div>
      <h2>Lihat Bedanya: <span class="hl-red">1 Garis Lurus</span> vs <span class="hl-green">Batas Melengkung</span></h2>
      <div class="split-60-40">
        <div class="img-box" style="padding:8px;">
          <img src="assets/P02/02_linear_vs_nonlinear.png" alt="Batas Keputusan Linear vs Non-Linear" />
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Contoh Nyata di Foto Frozen Kita</div>
          <div class="card-body" style="font-size:13.4px;">
            <ul>
              <li><strong>Aturan Lurus (Gagal):</strong> <em>&ldquo;Pokoknya makin banyak warna biru = makin pasti Elsa!&rdquo;</em> — padahal di rak ramai ada latar biru lain atau cahaya kebiruan!</li>
              <li><strong>Aturan Non-Linear (Berhasil):</strong> <em>&ldquo;Warna biru <strong>DAN</strong> bentuk gaun di tengah <strong>TAPI BUKAN</strong> cangkir di samping!&rdquo;</em></li>
            </ul>
          </div>
          <div class="mini-box" style="background:var(--tint-green); border-color:#A8DAB5;"><strong>Intinya:</strong> <em>Fungsi Aktivasi Non-Linear</em> berarti fungsi yang membuat batas keputusan model <strong>bisa melengkung mengikuti pola nyata</strong>, tidak kaku seperti 1 garis lurus.</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 20: STEP 3 — 3 FUNGSI AKTIVASI POPULER (ReLU, Sigmoid, Tanh) -->
    <section class="slide" data-title="Step 3: Mengenal 3 Fungsi Aktivasi Populer" data-notes="Alokasi waktu: 1 menit. Tunjukkan 3 kurva paling terkenal di Deep Learning: ReLU, Sigmoid, dan Tanh. Ajak peserta fokus pada bentuk dan kegunaan masing-masing, tidak perlu menghafal rumus eksponensial.">
      <div class="kicker">BAB 2 · STEP 3 · TIGA FUNGSI AKTIVASI POPULER</div>
      <h2>Tiga Fungsi Aktivasi Populer: <span class="hl-blue">ReLU</span>, <span class="hl-red">Sigmoid</span>, dan <span class="hl-green">Tanh</span></h2>
      <div class="img-box" style="height:auto; flex:0 0 auto; padding:6px;">
        <img src="assets/P02/03_activation_comparison.png" alt="Perbandingan Kurva ReLU, Sigmoid, dan Tanh" style="max-height:245px;" />
      </div>
      <table class="io-table" style="margin-top:8px; font-size:12.8px;">
        <thead><tr><th>Nama Aktivasi</th><th>Sifat Sederhana</th><th>Rentang Output</th><th>Kapan Dipakai?</th></tr></thead>
        <tbody>
          <tr><td><strong>ReLU</strong> ★</td><td>Negatif → <code>0</code>, Positif → tetap</td><td><code>0</code> s.d. <code>+∞</code></td><td><strong>Default di semua Hidden Layer!</strong></td></tr>
          <tr><td><strong>Sigmoid</strong></td><td>Kurva huruf <code>S</code> (seperti persen)</td><td><code>0.0</code> s.d. <code>1.0</code></td><td>Output <strong>2 pilihan (Ya/Tidak)</strong>, mis. Polos vs Ramai.</td></tr>
          <tr><td><strong>Tanh</strong></td><td>Huruf <code>S</code> tapi simetris di nol</td><td><code>-1.0</code> s.d. <code>+1.0</code></td><td>Data bertanda minus/plus (sering di teks/sinyal).</td></tr>
        </tbody>
      </table>
      <div class="callout" style="margin-top:8px; padding:7px 12px; font-size:12.6px;"><strong>Tips Awam:</strong> Kamu tidak perlu menghafal rumus <code>e⁻ᶻ</code> — cukup ingat <strong><code>ReLU</code> untuk tengah jaringan</strong> dan <strong><code>Sigmoid/Softmax</code> untuk ujung output</strong>!</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 21: STEP 4 — SIMULATOR #2 (LABORATORIUM AKTIVASI) -->
    <section class="slide" data-title="Simulator #2: Laboratorium Fungsi Aktivasi" data-notes="Alokasi waktu: 1.5 menit. Demo interaktif! Klik tab ReLU, Sigmoid, Tanh dan geser slider z ke kiri (negatif) dan ke kanan (positif) agar peserta melihat langsung pergerakan titik pada kurva.">
      <div class="kicker">BAB 2 · STEP 4 · SIMULATOR INTERAKTIF #2</div>
      <h2>Laboratorium <span class="hl-red">Fungsi Aktivasi</span> (Geser Skor <code>z</code>)</h2>
      <div class="split-60-40">
        <div class="canvas-box">
          <div id="act-tabs" class="sim-bar pdf-keep-ui">
            <button type="button" class="btn-ui" data-act="relu" onclick="setActMode('relu')" style="padding:5px 12px; font-size:12px;">1. ReLU</button>
            <button type="button" class="btn-ui outline" data-act="sigmoid" onclick="setActMode('sigmoid')" style="padding:5px 12px; font-size:12px;">2. Sigmoid</button>
            <button type="button" class="btn-ui outline" data-act="tanh" onclick="setActMode('tanh')" style="padding:5px 12px; font-size:12px;">3. Tanh</button>
          </div>
          <canvas id="act-canvas" width="580" height="320"></canvas>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div>
            <div class="card-title" id="act-title">ReLU: max(0, z)</div>
            <div class="sim-slider-row" style="margin-top:10px;">
              <span>Input Skor (z)</span>
              <input id="act-z-sl" type="range" min="-5" max="5" step="0.1" value="1.5" oninput="updateActSim()"/>
              <span id="act-z-val" class="sim-val">+1.5</span>
            </div>
          </div>
          <div class="card tint-blue" style="padding:12px; align-items:center; text-align:center;">
            <span style="font-size:11px; font-weight:700; color:var(--blue-text);">OUTPUT AKTIVASI f(z)</span>
            <div id="act-out-val" class="big-num" style="font-size:34px; color:var(--dark);">1.500</div>
          </div>
          <div class="mini-box" id="act-tip" style="font-size:12.4px;"><strong>Coba Eksperimen:</strong> Geser <code>z</code> ke <code>-4.0</code> lalu ke <code>+4.0</code> dan bandingkan respons ReLU vs Sigmoid!</div>
          <div id="act-note" class="callout">ReLU aktif!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 22: STEP 5 — KENAPA RELU RAJA HIDDEN LAYER? -->
    <section class="slide" data-title="Step 5: Kenapa ReLU Dipakai di Hampir Semua AI Modern?" data-notes="Alokasi waktu: 1 menit. Jelaskan 3 alasan praktis mengapa ReLU menang telak dibanding Sigmoid di hidden layer — pakai bahasa super ringan tanpa jargon berat.">
      <div class="kicker">BAB 2 · STEP 5 · PILIHAN STANDAR INDUSTRI</div>
      <h2>3 Alasan <span class="hl-blue">ReLU</span> Menjadi Raja di <em>Hidden Layer</em></h2>
      <div class="grid-3">
        <div class="card tint-blue" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div><div class="big-num" style="color:var(--blue-text);">01</div><div class="card-title" style="margin-top:4px;">Super Cepat Dihitung</div></div>
          <div class="card-body" style="font-size:13.2px;">Tidak perlu menghitung rumus pangkat <code>e⁻ᶻ</code> yang berat. Komputer cukup cek 1 hal: <em>&ldquo;Lebih kecil dari 0? Jadikan 0!&rdquo;</em></div>
          <div class="mini-box"><strong>Dampak:</strong> Training di Google Colab jauh lebih cepat selesai!</div>
        </div>
        <div class="card tint-green" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div><div class="big-num" style="color:#137333;">02</div><div class="card-title" style="margin-top:4px;">Sinyal Belajar Tidak Macet</div></div>
          <div class="card-body" style="font-size:13.2px;">Pada <code>Sigmoid</code>, di ujung kiri/kanan kurvanya rata/mendatar → AI sulit merasa ada perubahan (<em>vanishing gradient</em>). <code>ReLU</code> tetap curam untuk semua <code>z &gt; 0</code>!</div>
          <div class="mini-box"><strong>Dampak:</strong> Jaringan dalam (puluhan layer) tetap lancar belajar!</div>
        </div>
        <div class="card tint-yellow" style="justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <div><div class="big-num" style="color:#B06000;">03</div><div class="card-title" style="margin-top:4px;">Neuron Fokus &amp; Hemat</div></div>
          <div class="card-body" style="font-size:13.2px;">Neuron yang tidak cocok otomatis bernilai <code>0</code> (istirahat), jadi hanya neuron detektor ciri yang relevan saja yang menyala!</div>
          <div class="mini-box"><strong>Dampak:</strong> Model <strong>MobileNetV2</strong> di P04–P08 juga memakai versi ReLU (<code>ReLU6</code>)!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 23: STEP 6 — MENGENAL SOFTMAX (PROBABILITAS 100%) -->
    <section class="slide" data-title="Step 6: Softmax — Mengubah Logits Menjadi Probabilitas 100%" data-notes="Alokasi waktu: 1 menit. Mulai dari masalah konkret: skor mentah (+3.2, +0.8, -0.6) susah dibaca sebagai persentase dan ada angka minusnya. Softmax mengubahnya menjadi probabilitas 0-100% yang totalnya tepat 100%.">
      <div class="kicker">BAB 2 · STEP 6 · OUTPUT MULTI-KELAS</div>
      <h2><em>Softmax</em>: Mengubah <em>Logits</em> Menjadi <span class="hl-green">Probabilitas 0–100%</span></h2>
      <div class="split-60-40">
        <div class="card" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">3 Langkah Sederhana Cara Kerja <em>Softmax</em></div>
          <div class="step-list" style="gap:8px;">
            <div class="step-item" style="padding:8px 12px;"><div class="step-num">1</div><div><div class="step-title">Ubah Semua Skor Jadi Positif (Eksponensial <code>eᶻ</code>)</div><div class="step-desc">Skor negatif seperti <code>-1.0</code> otomatis jadi positif kecil (<code>0.37</code>), sedangkan skor tertinggi (<code>+3.2</code>) menjadi besar (<code>24.5</code>).</div></div></div>
            <div class="step-item" style="padding:8px 12px;"><div class="step-num yellow">2</div><div><div class="step-title">Jumlahkan Seluruh Nilai Positif (<code>Σ eᶻ</code>)</div><div class="step-desc">Hitung total keseluruhan nilai <code>eᶻ</code> dari <code>Anna + Elsa + Kristoff + Olaf + Sven</code>.</div></div></div>
            <div class="step-item" style="padding:8px 12px;"><div class="step-num green">3</div><div><div class="step-title">Bagi Tiap Nilai dengan Totalnya (<code>× 100%</code>)</div><div class="step-desc">Setiap karakter mendapat probabilitas <strong>0%–100%</strong>, dan <strong>kelimanya selalu berjumlah tepat 100%!</strong></div></div></div>
          </div>
          <div class="formula-box" style="font-size:12.5px;">P(kelas i) = eᶻⁱ / (eᶻ¹ + eᶻ² + eᶻ³ + eᶻ⁴ + eᶻ⁵)</div>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Mengapa Totalnya Selalu 100%?</div>
          <div class="card-body" style="font-size:13.3px;">
            <ul>
              <li>Kelima karakter Frozen saling bersaing dalam satu total probabilitas penuh (<strong><code>1.0</code> = <code>100%</code></strong>).</li>
              <li>Kalau probabilitas <strong>Elsa</strong> naik jadi <strong>85%</strong>, maka probabilitas 4 karakter lainnya <strong>otomatis mengecil</strong> agar total tetap 100%.</li>
              <li>Tidak pernah ada probabilitas negatif (<code>-10%</code>) atau lebih dari 100%.</li>
            </ul>
          </div>
          <div class="callout green"><strong>Di Keras:</strong> Cukup tulis <code>Dense(5, activation="softmax")</code> di baris paling terakhir model!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 24: STEP 7 — SIMULATOR #3 (SIMULATOR SOFTMAX + KOLOM e^z LIVE!) -->
    <section class="slide" data-title="Simulator #3: Simulator Softmax 5 Karakter Frozen" data-notes="Alokasi waktu: 1.5 menit. Demo interaktif! Klik 3 preset (Yakin Elsa, Ragu Elsa vs Anna, Semua Skor Negatif). Tunjukkan kolom nilai e^z di kanan agar peserta melihat langsung bagaimana skor negatif pun jadi positif!">
      <div class="kicker">BAB 2 · STEP 7 · SIMULATOR INTERAKTIF #3</div>
      <h2>Simulator <span class="hl-green">Softmax</span> untuk 5 Karakter Disney Frozen</h2>
      <div class="sim-bar pdf-keep-ui" id="sm-presets" style="margin-bottom:8px;">
        <span style="font-size:12px; font-weight:700; color:var(--muted);">Preset Cepat:</span>
        <button type="button" class="btn-ui" data-smp="elsa" onclick="setSmPreset('elsa')" style="padding:5px 11px; font-size:11.5px;">1. Yakin Elsa</button>
        <button type="button" class="btn-ui outline" data-smp="ragu" onclick="setSmPreset('ragu')" style="padding:5px 11px; font-size:11.5px;">2. Ragu Elsa vs Anna</button>
        <button type="button" class="btn-ui outline" data-smp="neg" onclick="setSmPreset('neg')" style="padding:5px 11px; font-size:11.5px;">3. Semua Skor Negatif</button>
      </div>
      <div class="grid-2">
        <div class="card surface" style="padding:13px 16px; gap:8px; justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div style="font-family:var(--font-title); font-size:13.5px; font-weight:700;">1. Geser Skor Mentah (<em>Logits</em>)</div>
          <div class="sim-slider-row"><span class="frozen-chip"><img src="assets/P02/thumb_anna.jpg" alt="Anna"/>Anna</span><input id="sm-0" type="range" min="-4" max="5" step="0.2" value="0.8" oninput="updateSm()"/><span id="sm-v0" class="sim-val">+0.8</span></div>
          <div class="sim-slider-row"><span class="frozen-chip"><img src="assets/P02/thumb_elsa.jpg" alt="Elsa"/>Elsa</span><input id="sm-1" type="range" min="-4" max="5" step="0.2" value="3.2" oninput="updateSm()"/><span id="sm-v1" class="sim-val">+3.2</span></div>
          <div class="sim-slider-row"><span class="frozen-chip"><img src="assets/P02/thumb_kristoff.jpg" alt="Kristoff"/>Kristoff</span><input id="sm-2" type="range" min="-4" max="5" step="0.2" value="-0.6" oninput="updateSm()"/><span id="sm-v2" class="sim-val">-0.6</span></div>
          <div class="sim-slider-row"><span class="frozen-chip"><img src="assets/P02/thumb_olaf.jpg" alt="Olaf"/>Olaf</span><input id="sm-3" type="range" min="-4" max="5" step="0.2" value="0.2" oninput="updateSm()"/><span id="sm-v3" class="sim-val">+0.2</span></div>
          <div class="sim-slider-row"><span class="frozen-chip"><img src="assets/P02/thumb_sven.jpg" alt="Sven"/>Sven</span><input id="sm-4" type="range" min="-4" max="5" step="0.2" value="-1.0" oninput="updateSm()"/><span id="sm-v4" class="sim-val">-1.0</span></div>
        </div>
        <div class="card" style="padding:13px 16px; gap:8px; justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-family:var(--font-title); font-size:13.5px; font-weight:700;">2. Output Softmax (Probabilitas 0–100%)</span>
            <span id="sm-sum-pill" class="pill green" style="font-size:11px; padding:3px 9px;">Total = 100.0%</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:8px;">
            <div class="prob-row" style="font-size:10.5px; color:var(--muted); font-weight:700;"><span>Karakter</span><span>Porsi Peluang</span><span style="text-align:right;">eᶻ</span><span style="text-align:right;">Persen</span></div>
            <div class="prob-row"><strong>Anna</strong><div class="prob-track"><div id="sm-b0" class="prob-fill" style="background:#EA4335; width:8%;"></div></div><span id="sm-e0" class="sim-val" style="color:var(--muted); font-size:11px;">2.23</span><span id="sm-p0" class="sim-val">7.7%</span></div>
            <div class="prob-row"><strong>Elsa</strong><div class="prob-track"><div id="sm-b1" class="prob-fill" style="background:#4285F4; width:85%;"></div></div><span id="sm-e1" class="sim-val" style="color:var(--muted); font-size:11px;">24.5</span><span id="sm-p1" class="sim-val">84.9%</span></div>
            <div class="prob-row"><strong>Kristoff</strong><div class="prob-track"><div id="sm-b2" class="prob-fill" style="background:#5F6368; width:2%;"></div></div><span id="sm-e2" class="sim-val" style="color:var(--muted); font-size:11px;">0.55</span><span id="sm-p2" class="sim-val">1.9%</span></div>
            <div class="prob-row"><strong>Olaf</strong><div class="prob-track"><div id="sm-b3" class="prob-fill" style="background:#34A853; width:4%;"></div></div><span id="sm-e3" class="sim-val" style="color:var(--muted); font-size:11px;">1.22</span><span id="sm-p3" class="sim-val">4.2%</span></div>
            <div class="prob-row"><strong>Sven</strong><div class="prob-track"><div id="sm-b4" class="prob-fill" style="background:#FBBC04; width:1%;"></div></div><span id="sm-e4" class="sim-val" style="color:var(--muted); font-size:11px;">0.37</span><span id="sm-p4" class="sim-val">1.3%</span></div>
          </div>
          <div id="sm-winner" class="callout green" style="padding:8px 12px; font-size:12.6px;">Prediksi AI: ELSA!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 25: STEP 8 — SIGMOID VS SOFTMAX (DENGAN FOTO CONTOH NYATA!) -->
    <section class="slide" data-title="Step 8: Kapan Pakai Sigmoid vs Softmax?" data-notes="Alokasi waktu: 1 menit. Bedakan secara visual: kalau pilihannya cuma 2 (misal Polos vs Ramai) pakai 1 neuron Sigmoid; kalau 5 karakter Frozen pakai 5 neuron Softmax.">
      <div class="kicker">BAB 2 · STEP 8 · ATURAN EMAS OUTPUT LAYER</div>
      <h2>Kapan Pakai <span class="hl-red">Sigmoid</span> vs <span class="hl-green">Softmax</span>?</h2>
      <div class="grid-2">
        <div class="card tint-red" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div><span class="pill red">1 NEURON · SIGMOID</span><div class="card-title" style="margin-top:4px;">Tebakan 2 Pilihan (Ya / Tidak)</div></div>
          <div style="display:flex; gap:10px; align-items:center; justify-content:center;">
            <img src="assets/P02/thumb_elsa.jpg" alt="Polos" style="width:82px; height:82px; border-radius:10px; object-fit:cover; border:2px solid var(--blue);" />
            <span style="font-family:var(--font-title); font-weight:700; color:#C5221F;">VS</span>
            <img src="assets/P02/thumb_elsa_ramai.jpg" alt="Ramai" style="width:82px; height:82px; border-radius:10px; object-fit:cover; border:2px solid var(--red);" />
          </div>
          <div class="card-body" style="font-size:13.2px;">
            <ul>
              <li>Contoh: <em>&ldquo;Apakah latar foto ini Polos (0) atau Ramai (1)?&rdquo;</em></li>
              <li>Cukup <strong>1 neuron Sigmoid</strong> → keluar 1 angka <code>0.0–1.0</code>.</li>
            </ul>
          </div>
          <div class="formula-box" style="font-size:11.8px; border-color:#F6AEA9;">Dense(1, "sigmoid") + binary_crossentropy</div>
        </div>
        <div class="card tint-green" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div><span class="pill green">5 NEURON · SOFTMAX ★ PROJECT KITA</span><div class="card-title" style="margin-top:4px;">Tebakan 3+ Pilihan Saling Lepas</div></div>
          <div style="display:flex; gap:6px; justify-content:center;">
            <img src="assets/P02/thumb_anna.jpg" alt="Anna" style="width:54px; height:54px; border-radius:8px; object-fit:cover; border:1.5px solid var(--green);" />
            <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:54px; height:54px; border-radius:8px; object-fit:cover; border:1.5px solid var(--green);" />
            <img src="assets/P02/thumb_kristoff.jpg" alt="Kristoff" style="width:54px; height:54px; border-radius:8px; object-fit:cover; border:1.5px solid var(--green);" />
            <img src="assets/P02/thumb_olaf.jpg" alt="Olaf" style="width:54px; height:54px; border-radius:8px; object-fit:cover; border:1.5px solid var(--green);" />
            <img src="assets/P02/thumb_sven.jpg" alt="Sven" style="width:54px; height:54px; border-radius:8px; object-fit:cover; border:1.5px solid var(--green);" />
          </div>
          <div class="card-body" style="font-size:13.2px;">
            <ul>
              <li>Project kita: 1 foto = <strong>1 dari 5 karakter Frozen</strong>.</li>
              <li>Butuh <strong>5 neuron Softmax</strong> → 5 peluang berjumlah <code>100%</code>.</li>
            </ul>
          </div>
          <div class="formula-box" style="font-size:11.8px; border-color:#A8DAB5;">Dense(5, "softmax") + sparse_categorical_crossentropy</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    s.append(
        _qa_slide(
            qa_id="qa3",
            qa_num=3,
            kicker="TANYA-JAWAB #3 · SOFTMAX MULTI-KELAS",
            title_html='Cek Pemahaman: <span class="hl-green">Kenapa Softmax, Bukan ReLU, di Output Layer?</span>',
            question_html="Untuk menebak 5 karakter Disney Frozen, mengapa kita memakai <strong>Softmax</strong> di lapisan paling akhir dan bukan <code>ReLU</code>?",
            choices=[
                "<strong>A.</strong> Karena ReLU tidak bisa mengeluarkan angka positif",
                "<strong>B.</strong> Karena Softmax mengubah 5 skor mentah menjadi peluang <code>0–100%</code> yang totalnya tepat <code>100%</code>",
                "<strong>C.</strong> Karena Softmax otomatis memperbesar foto jadi 224×224",
            ],
            answer_html="<strong>Jawaban: B — Menghasilkan peluang 0–100% berjumlah 100%!</strong><br/><code>ReLU</code> bisa mengeluarkan angka tak terbatas (mis. <code>50</code> dan <code>120</code>) sehingga tidak terbaca sebagai peluang. <code>Softmax</code> mengubah 5 skor mentah menjadi probabilitas yang jumlahnya tepat 100%.",
            vis_q_html='<span class="pill red">BANDINGKAN OUTPUT</span><div class="mini-box" style="text-align:left; font-family:var(--font-code); font-size:12px; margin-top:10px;">ReLU    : [0.8, 3.2, 0.0, 0.2, 0.0]<br/>Total   : 4.2 (bukan persen!)<br/><br/>Softmax : [8%, 85%, 2%, 4%, 1%]<br/>Total   : ???</div>',
            vis_a_html='<span class="pill green">TOTAL PAS 100%!</span><div class="big-num" style="color:#137333; margin:10px 0;">100.0%</div><div class="mini-box">Setiap karakter mendapat porsi peluang jelas antara <code>0%</code> s.d. <code>100%</code> dan total kelimanya selalu tepat <code>1.0</code>!</div>',
            notes="Alokasi waktu: 1.5 menit. Minta peserta menebak dari kotak perbandingan kanan, lalu klik Reveal sebelum masuk Bab 3.",
        )
    )

    # =========================================================================
    # BAB 3: BAGAIMANA AI BELAJAR DARI KESALAHAN? (SLIDE 27–38 · 13.0 menit)
    # =========================================================================
    s.append(
        make_divider_slide(
            bg_class="bg-green",
            kicker="BAB 3 · PROSES TRAINING MODEL",
            title="Bagaimana Model Belajar dari Kesalahan?",
            description="Mengikuti perjalanan 1 foto Elsa dari bobot acak awal hingga model memperbaiki bobotnya sendiri lewat Loss, Gradient Descent, dan Backpropagation.",
            footer_label=FOOTER,
            data_title="Bab 3: Proses Training (Loss, Gradient Descent & Backprop)",
            notes="Alokasi waktu: 0.5 menit. Masuk Bab 3! Ini bagian inti Deep Learning — kita urai langkah demi langkah bagaimana bobot model berubah dari acak menjadi akurat.",
        )
    )

    s.append(
        f"""
    <!-- 28: STEP 1 — KONDISI AWAL: BOBOT MASIH ACAK -->
    <section class="slide" data-title="Step 1: Kondisi Awal — Bobot Masih Acak" data-notes="Alokasi waktu: 1 menit. Mulai dari kondisi nyata saat model baru dibuat: semua weight w dan bias b diisi angka acak, sehingga prediksinya masih keliru. Dari sinilah proses training dimulai.">
      <div class="kicker">BAB 3 · STEP 1 (TITIK MULAI PROSES TRAINING)</div>
      <h2>Saat Baru Dibuat, <span class="hl-red">Bobot Masih Acak</span> — Prediksi Awal Keliru</h2>
      <div class="grid-3">
        <div class="card tint-blue" style="justify-content:space-between; text-align:center;">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue" style="margin:0 auto;">1. FOTO MASUK</span>
          <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:128px; height:128px; border-radius:12px; object-fit:cover; margin:0 auto; border:3px solid var(--blue);" />
          <div class="mini-box"><strong>Label Asli (Ground Truth):</strong><br/><span style="color:var(--blue-text); font-weight:700; font-size:15px;">ELSA (100%)</span></div>
        </div>
        <div class="card tint-yellow" style="justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <span class="pill yellow">2. INISIALISASI BOBOT ACAK</span>
          <div class="card-title">Model Belum Pernah Dilatih</div>
          <pre class="code" style="font-size:11.5px;">w₁ = +0.12  (acak)
w₂ = -0.45  (acak)
w₃ = +0.03  (acak)
b  =  0.00</pre>
          <div class="card-body" style="font-size:12.8px;">Karena nilai <code>w</code> masih acak, model belum tahu bahwa warna biru muda adalah ciri khas Elsa.</div>
        </div>
        <div class="card tint-red" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <span class="pill red">3. PREDIKSI AWAL KELIRU</span>
          <div class="card-title">Output Awal Model</div>
          <pre class="code" style="font-size:11.5px; background:#3B1616;">Anna     : 45%  ✗
Olaf     : 30%  ✗
Sven     : 15%  ✗
Elsa     : 10%  ← (Padahal ini asli!)</pre>
          <div class="callout red" style="padding:7px 10px; font-size:12.4px;"><strong>Pertanyaan Kunci:</strong> Bagaimana cara mengukur seberapa besar kesalahannya lalu memperbaiki bobotnya?</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 29: STEP 2 — MENGUKUR KESALAHAN (CROSS-ENTROPY LOSS) -->
    <section class="slide" data-title="Step 2: Mengukur Kesalahan (Cross-Entropy Loss)" data-notes="Alokasi waktu: 1.5 menit. Langkah pertama agar model bisa belajar adalah mengukur seberapa besar kesalahannya menggunakan fungsi Loss (Cross-Entropy). Semakin kecil nilai Loss, semakin akurat prediksi model.">
      <div class="kicker">BAB 3 · STEP 2 · MENGUKUR BESAR KESALAHAN</div>
      <h2><em>Loss</em>: Angka Pengukur <span class="hl-red">Seberapa Besar Kesalahan</span> Prediksi</h2>
      <div class="split-60-40">
        <div class="img-box" style="padding:7px;">
          <img src="assets/P02/04_cross_entropy_penalty.png" alt="Kurva Cross-Entropy Loss" />
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title">Cara Membaca Nilai <em>Loss</em></div>
          <div class="card-body" style="font-size:13.2px;">
            <ul>
              <li><strong>Makin KECIL nilai <em>Loss</em> = makin AKURAT model!</strong> (Target ideal: mendekati <code>0.0</code>).</li>
              <li><strong>Yakin tapi Salah (Elsa cuma 8%):</strong> <code>Loss = 2.53</code> → nilai penalti sangat tinggi.</li>
              <li><strong>Masih Ragu (Elsa 50%):</strong> <code>Loss = 0.69</code> → masih perlu diperbaiki.</li>
              <li><strong>Yakin &amp; Benar (Elsa 92%):</strong> <code>Loss = 0.08</code> → nyaris tepat!</li>
            </ul>
          </div>
          <div class="callout red"><strong>Sederhananya:</strong> <em>Loss</em> adalah jarak kesalahan antara tebakan model dan label asli. Tujuan <em>training</em> adalah <strong>mengubah bobot agar <em>Loss</em> sekecil mungkin!</strong></div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 30: STEP 3 — GRADIENT DESCENT -->
    <section class="slide" data-title="Step 3: Gradient Descent — Menurunkan Loss Bertahap" data-notes="Alokasi waktu: 1 menit. Jelaskan Gradient Descent dengan sangat sederhana: Gradien menunjukkan arah kemiringan kurva Loss (naik atau turun), lalu model melangkah ke arah turun menuju nilai Loss terendah.">
      <div class="kicker">BAB 3 · STEP 3 · GRADIENT DESCENT (PENJELASAN SEDERHANA)</div>
      <h2><em>Gradient Descent</em>: Menurunkan <span class="hl-blue"><em>Loss</em> Bertahap</span> ke Titik Terendah</h2>
      <div class="grid-2">
        <div class="card tint-blue" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">INTUISI KURVA LOSS</span>
          <div class="card-title">Mencari Titik Terendah Kurva <em>Loss</em></div>
          <svg viewBox="0 0 380 132" style="width:100%; height:auto; background:#FFF; border-radius:10px; border:1px solid #C6DAFC;">
            <path d="M 28 14 Q 190 190 352 14" fill="none" stroke="#5F6368" stroke-width="2.5"/>
            <circle cx="88" cy="60" r="8.5" fill="#EA4335"/>
            <path d="M 100 68 Q 130 88 155 94" fill="none" stroke="#1A73E8" stroke-width="2.5" stroke-dasharray="4 3"/>
            <circle cx="190" cy="100" r="8" fill="#34A853"/>
            <text x="108" y="30" font-family="Poppins" font-size="10.5" font-weight="700" fill="#C5221F">Mulai (Loss tinggi)</text>
            <text x="190" y="122" text-anchor="middle" font-family="Poppins" font-size="10.5" font-weight="700" fill="#137333">Titik Minimum (Loss ≈ 0)</text>
          </svg>
          <div class="card-body" style="font-size:13px;">
            <ul>
              <li><strong>Seperti Menyetel Keran Air:</strong> Air terlalu panas? Putar sedikit ke dingin. Masih kurang pas? Putar pelan lagi hingga tepat.</li>
              <li><strong>Arah Kemiringan (Gradien):</strong> Model mengecek kemiringan kurva <em>Loss</em> lalu menggeser bobot ke arah <strong>menurun</strong>!</li>
            </ul>
          </div>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">CARA KOMPUTER MEMPERBARUI BOBOT</span>
          <div class="card-title">Hanya 1 Rumus Pembaruan Bobot</div>
          <div class="formula-box" style="font-size:13.5px;">w_baru = w_lama − (Learning Rate × Gradien)</div>
          <div class="card-body" style="font-size:13.2px;">
            <ul>
              <li><strong>Gradien:</strong> Penunjuk arah — apakah bobot <code>w</code> harus dinaikkan atau diturunkan agar <em>Loss</em> berkurang.</li>
              <li><strong>Tanda Minus (<code>−</code>):</strong> Melangkah ke arah <em>turun</em> (menurunkan <em>Loss</em>).</li>
              <li><strong>Learning Rate:</strong> Seberapa <strong>besar ukuran langkah</strong> tiap kali mengubah bobot.</li>
            </ul>
          </div>
          <div class="callout green">Di Keras, algoritma <em>optimizer</em> modern yang kita pakai untuk mengatur langkah ini bernama <strong><code>Adam</code></strong>!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 31: STEP 4 — LEARNING RATE DENGAN MINI-SVG DI TIAP KARTU -->
    <section class="slide" data-title="Step 4: Learning Rate — Jangan Kekecilan, Jangan Kebesaran!" data-notes="Alokasi waktu: 1 menit. Tunjukkan 3 skenario ukuran langkah (Learning Rate) lewat 3 gambar mini kurva Loss yang kontras agar peserta langsung paham efeknya secara visual.">
      <div class="kicker">BAB 3 · STEP 4 · UKURAN LANGKAH (LEARNING RATE)</div>
      <h2><em>Learning Rate</em>: <span class="hl-red">Seberapa Besar Perubahan Bobot?</span></h2>
      <div class="grid-3">
        <div class="card tint-yellow" style="justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <div><span class="pill yellow">KEKECILAN (0.00001)</span><div class="card-title" style="margin-top:4px;">Terlalu Lambat</div></div>
          <svg viewBox="0 0 240 88" style="width:100%; background:#FFF; border-radius:9px; border:1px solid #FDE293;">
            <path d="M 18 14 Q 120 140 222 14" fill="none" stroke="#9AA0A6" stroke-width="2"/>
            <circle cx="48" cy="40" r="4.5" fill="#E37400"/><circle cx="56" cy="46" r="4.5" fill="#E37400"/><circle cx="65" cy="52" r="4.5" fill="#E37400"/>
            <circle cx="120" cy="76" r="5" fill="#34A853"/>
          </svg>
          <div class="card-body" style="font-size:12.8px;">Loss turun sangat pelan — butuh ratusan putaran &amp; sering belum sampai dasar.</div>
        </div>
        <div class="card tint-green" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div><span class="pill green">PAS / IDEAL (0.001) ★</span><div class="card-title" style="margin-top:4px;">Turun Mulus ke Dasar</div></div>
          <svg viewBox="0 0 240 88" style="width:100%; background:#FFF; border-radius:9px; border:1px solid #A8DAB5;">
            <path d="M 18 14 Q 120 140 222 14" fill="none" stroke="#9AA0A6" stroke-width="2"/>
            <polyline points="48,40 76,60 100,72 118,76" fill="none" stroke="#1A73E8" stroke-width="2.2"/>
            <circle cx="48" cy="40" r="4.5" fill="#1A73E8"/><circle cx="76" cy="60" r="4.5" fill="#1A73E8"/><circle cx="118" cy="76" r="5.5" fill="#34A853"/>
          </svg>
          <div class="card-body" style="font-size:12.8px;">Langkah mantap di awal lalu makin halus saat mendekati titik terbaik!</div>
        </div>
        <div class="card tint-red" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div><span class="pill red">KEBESARAN (0.5 – 1.0)</span><div class="card-title" style="margin-top:4px;">Melompat Liar / Meledak!</div></div>
          <svg viewBox="0 0 240 88" style="width:100%; background:#FFF; border-radius:9px; border:1px solid #F6AEA9;">
            <path d="M 18 14 Q 120 140 222 14" fill="none" stroke="#9AA0A6" stroke-width="2"/>
            <polyline points="54,44 195,36 32,24 214,18" fill="none" stroke="#EA4335" stroke-width="2.2"/>
            <circle cx="54" cy="44" r="4.5" fill="#EA4335"/><circle cx="195" cy="36" r="4.5" fill="#EA4335"/><circle cx="214" cy="18" r="5.5" fill="#C5221F"/>
          </svg>
          <div class="card-body" style="font-size:12.8px;">Lompatan melewati dasar lembah ke dinding seberang — <strong>Loss malah naik / <code>NaN</code>!</strong></div>
        </div>
      </div>
      <div class="callout" style="margin-top:10px;"><strong>Patokan Aman:</strong> Mulai dengan <code>Adam(learning_rate=0.001)</code>; nanti saat <em>fine-tuning</em> MobileNetV2 di P07 kita kecilkan jadi <code>0.00001 (1e-5)</code>.</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 32: STEP 5 — SIMULATOR #4 (LEMBAH LOSS — SINKRON w = -2.8!) -->
    <section class="slide" data-title="Simulator #4: Lembah Loss &amp; Learning Rate Interaktif" data-notes="Alokasi waktu: 1.5 menit. Demo interaktif! Klik 3 preset Learning Rate (Kecil, Ideal, Besar) dan tunjukkan nomor langkah 0 sampai 8 di grafik lembah.">
      <div class="kicker">BAB 3 · STEP 5 · SIMULATOR INTERAKTIF #4</div>
      <h2>Simulasi <span class="hl-green">Gradient Descent</span>: Lihat Bola Menuruni Lembah</h2>
      <div class="split-60-40">
        <div class="canvas-box">
          <div id="gd-presets" class="sim-bar pdf-keep-ui">
            <button type="button" class="btn-ui outline" data-gd="small" onclick="setGdMode('small')" style="padding:5px 11px; font-size:11.5px;">1. LR Kecil (0.03)</button>
            <button type="button" class="btn-ui" data-gd="ideal" onclick="setGdMode('ideal')" style="padding:5px 11px; font-size:11.5px;">2. LR Ideal (0.20)</button>
            <button type="button" class="btn-ui outline" data-gd="large" onclick="setGdMode('large')" style="padding:5px 11px; font-size:11.5px;">3. LR Besar (1.06)</button>
          </div>
          <canvas id="gd-canvas" width="580" height="320"></canvas>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div>
            <div id="gd-title" class="card-title">LR Ideal (0.20) — Turun Mulus</div>
            <div class="card-body" style="font-size:13px; margin-top:6px;">
              Titik awal: <code>w = -2.8</code> (<code>Loss = 7.84</code>)<br/>Target dasar lembah: <code>w = 0.0</code> (<code>Loss = 0.00</code>).<br/>Simulasi menjalankan <strong>8 langkah</strong> pembaruan bobot.
            </div>
          </div>
          <div class="grid-2" style="flex:0 0 auto; gap:10px;">
            <div class="card tint-blue" style="padding:10px; align-items:center; text-align:center;">
              <span style="font-size:10.5px; font-weight:700; color:var(--blue-text);">POSISI AKHIR (w)</span>
              <div id="gd-end-w" class="big-num" style="font-size:24px;">-0.05</div>
            </div>
            <div class="card tint-green" style="padding:10px; align-items:center; text-align:center;">
              <span style="font-size:10.5px; font-weight:700; color:#137333;">LOSS AKHIR</span>
              <div id="gd-end-loss" class="big-num" style="font-size:24px;">0.002</div>
            </div>
          </div>
          <div id="gd-note" class="callout green">Berhasil turun mulus!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 33: STEP 6 — BACKPROPAGATION DENGAN DIAGRAM SVG 2 ARAH PENUH! -->
    <section class="slide" data-title="Step 6: Backpropagation — Menghitung Koreksi Mundur" data-notes="Alokasi waktu: 1.5 menit. Tunjukkan diagram 2 arah: panah biru maju (foto Olaf salah ditebak Elsa), lalu panah merah mundur (Backpropagation) menghitung seberapa besar kontribusi kesalahan tiap bobot w2 dan w1.">
      <div class="kicker">BAB 3 · STEP 6 · BACKPROPAGATION (TANPA KALKULUS!)</div>
      <h2><em>Backpropagation</em>: Menghitung <span class="hl-red">Koreksi Mundur</span> ke Setiap Bobot</h2>
      <div class="card" style="flex:1; justify-content:space-between; gap:10px;">
        <div class="card-top-bar bar-blue"></div>
        <!-- Full visual 2-way diagram (eliminates 45% bottom whitespace from v1!) -->
        <svg viewBox="0 0 920 190" style="width:100%; height:auto; background:#F8F9FA; border-radius:12px; border:1px solid #DADCE0;">
          <!-- Forward boxes -->
          <rect x="22" y="34" width="150" height="72" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
          <text x="97" y="64" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#1A73E8">1. Foto OLAF</text>
          <text x="97" y="84" text-anchor="middle" font-family="Roboto" font-size="11.5" fill="#3C4043">Masuk ke Input</text>

          <rect x="242" y="34" width="175" height="72" rx="12" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
          <text x="329" y="64" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#B06000">2. Bobot Hidden (w₁)</text>
          <text x="329" y="84" text-anchor="middle" font-family="Roboto" font-size="11.5" fill="#3C4043">Hitung pola ciri</text>

          <rect x="488" y="34" width="175" height="72" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/>
          <text x="575" y="64" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#137333">3. Bobot Output (w₂)</text>
          <text x="575" y="84" text-anchor="middle" font-family="Roboto" font-size="11.5" fill="#3C4043">Tebak: 70% Elsa ✗</text>

          <rect x="734" y="34" width="164" height="72" rx="12" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.5"/>
          <text x="816" y="64" text-anchor="middle" font-family="Poppins" font-size="13" font-weight="700" fill="#C5221F">4. LOSS TINGGI!</text>
          <text x="816" y="84" text-anchor="middle" font-family="Roboto" font-size="11.5" fill="#3C4043">Aslinya OLAF!</text>

          <!-- Blue forward arrows -->
          <line x1="172" y1="68" x2="236" y2="68" stroke="#1A73E8" stroke-width="3"/><polygon points="236,62 242,68 236,74" fill="#1A73E8"/>
          <line x1="417" y1="68" x2="482" y2="68" stroke="#1A73E8" stroke-width="3"/><polygon points="482,62 488,68 482,74" fill="#1A73E8"/>
          <line x1="663" y1="68" x2="728" y2="68" stroke="#1A73E8" stroke-width="3"/><polygon points="728,62 734,68 728,74" fill="#1A73E8"/>
          <text x="455" y="22" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#1A73E8">ALUR MAJU (FORWARD PASS) ─────────────────────────→</text>

          <!-- Red backward path -->
          <path d="M 816 106 L 816 148 L 329 148 L 329 112" fill="none" stroke="#EA4335" stroke-width="3" stroke-dasharray="6 4"/>
          <line x1="575" y1="148" x2="575" y2="112" stroke="#EA4335" stroke-width="3" stroke-dasharray="6 4"/>
          <polygon points="569,114 575,106 581,114" fill="#EA4335"/>
          <polygon points="323,114 329,106 335,114" fill="#EA4335"/>
          <rect x="372" y="135" width="386" height="26" rx="13" fill="#EA4335"/>
          <text x="565" y="152" text-anchor="middle" font-family="Poppins" font-size="11.5" font-weight="700" fill="#FFFFFF">← BACKPROPAGATION: Kirim Koreksi Mundur ke w₂ &amp; w₁</text>
        </svg>

        <div class="grid-2" style="flex:0 0 auto; gap:14px;">
          <div class="callout yellow" style="margin:0;">
            <strong>Penjelasan Sederhana:</strong> Dari nilai <em>Loss</em> di ujung kanan, sistem melacak <strong>mundur</strong> ke tiap layer: bobot mana yang paling besar menyebabkan tebakan keliru, bobot itulah yang paling besar dikoreksi!
          </div>
          <div class="callout green" style="margin:0;">
            <strong>Kabar Baik di Keras:</strong> Kamu <strong>tidak perlu menghitung turunan kalkulus</strong> secara manual — cukup panggil <code>model.fit()</code>, TensorFlow menghitung <em>Backpropagation</em> otomatis dalam milidetik!
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 34: STEP 7 — CERITA UTUH 1 PUTARAN BELAJAR + PROGRES EPOCH (FILLED CLEANLY) -->
    <section class="slide" data-title="Step 7: Cerita Utuh 4 Langkah Training AI" data-notes="Alokasi waktu: 1 menit. Rangkum 4 langkah siklus training plus tunjukkan progres nyata dari Epoch 1 (tebakan 12%) hingga Epoch 15 (93% Elsa) agar peserta melihat gambaran besarnya.">
      <div class="kicker">BAB 3 · STEP 7 · RINGKASAN SIKLUS TRAINING</div>
      <h2>4 Langkah yang Berulang Ratusan Kali di <span class="hl-green"><code>model.fit()</code></span></h2>
      <div class="grid-4" style="flex:0 0 auto; align-items:stretch;">
        <div class="card tint-blue" style="padding:15px;"><div class="card-top-bar bar-blue"></div><div class="big-num" style="color:var(--blue-text); font-size:28px;">01</div><div class="card-title" style="font-size:15.5px;">Forward Pass</div><div class="card-body" style="font-size:13px;">Foto masuk dari Input Layer → keluar probabilitas Softmax di Output Layer.</div></div>
        <div class="card tint-red" style="padding:15px;"><div class="card-top-bar bar-red"></div><div class="big-num" style="color:var(--red); font-size:28px;">02</div><div class="card-title" style="font-size:15.5px;">Hitung Loss</div><div class="card-body" style="font-size:13px;">Ukur seberapa besar kesalahan prediksi dibandingkan label asli Frozen.</div></div>
        <div class="card tint-yellow" style="padding:15px;"><div class="card-top-bar bar-yellow"></div><div class="big-num" style="color:#B06000; font-size:28px;">03</div><div class="card-title" style="font-size:15.5px;">Backpropagation</div><div class="card-body" style="font-size:13px;">Hitung mundur seberapa besar kontribusi tiap <code>weight</code> &amp; <code>bias</code> terhadap Loss.</div></div>
        <div class="card tint-green" style="padding:15px;"><div class="card-top-bar bar-green"></div><div class="big-num" style="color:#137333; font-size:28px;">04</div><div class="card-title" style="font-size:15.5px;">Update Bobot</div><div class="card-body" style="font-size:13px;"><code>Adam</code> menggeser bobot turun sebesar <em>Learning Rate</em> agar Loss mengecil.</div></div>
      </div>
      <div class="card surface" style="margin-top:14px; flex:1; justify-content:space-between; padding:16px 20px;">
        <div class="card-title" style="font-size:15.5px;">Progres Prediksi Foto Elsa Setelah Siklus 1–4 Diulang Terus-Menerus:</div>
        <div class="grid-3" style="flex:0 0 auto; gap:14px;">
          <div class="mini-box" style="border-left:4px solid var(--red); padding:12px 14px;">
            <strong>Putaran Awal (Epoch 1)</strong><br/>
            <span style="font-size:12.5px;">Prediksi Elsa: <code>12%</code> · Loss: <code>2.12</code></span>
            <div class="prob-track" style="height:10px; margin-top:7px;"><div class="prob-fill" style="width:12%; background:#EA4335;"></div></div>
          </div>
          <div class="mini-box" style="border-left:4px solid var(--yellow); padding:12px 14px;">
            <strong>Pertengahan (Epoch 5)</strong><br/>
            <span style="font-size:12.5px;">Prediksi Elsa: <code>68%</code> · Loss: <code>0.39</code></span>
            <div class="prob-track" style="height:10px; margin-top:7px;"><div class="prob-fill" style="width:68%; background:#FBBC04;"></div></div>
          </div>
          <div class="mini-box" style="border-left:4px solid var(--green); padding:12px 14px;">
            <strong>Terlatih (Epoch 15)</strong><br/>
            <span style="font-size:12.5px;">Prediksi Elsa: <code>93%</code> · Loss: <code>0.07</code></span>
            <div class="prob-track" style="height:10px; margin-top:7px;"><div class="prob-fill" style="width:93%; background:#34A853;"></div></div>
          </div>
        </div>
        <div class="callout green" style="padding:8px 14px; font-size:12.8px;"><strong>Kesimpulan:</strong> Seluruh proses <code>01 → 02 → 03 → 04</code> ini berjalan otomatis di belakang layar setiap kali kamu menjalankan 1 baris <code>model.fit(...)</code>!</div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 35: STEP 8 — BATCH SIZE & EPOCH DENGAN VISUAL BUKU SOAL -->
    <section class="slide" data-title="Step 8: Batch Size &amp; Epoch (Analogi Buku 143 Soal)" data-notes="Alokasi waktu: 1 menit. Pakai analogi super mudah: membaca buku latihan 143 foto Frozen dengan mencicil 16 foto per sesi (Batch) sampai tamat 1 buku penuh (Epoch).">
      <div class="kicker">BAB 3 · STEP 8 · ISTILAH WAJIB TRAINING</div>
      <h2>Apa Bedanya <span class="hl-blue">Batch Size</span> dan <span class="hl-red">Epoch</span>?</h2>
      <div class="grid-2">
        <div class="card tint-blue" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div><span class="pill blue">BATCH SIZE (mis. 16 foto)</span><div class="card-title" style="margin-top:4px;">Cicilan Paket Foto per Update</div></div>
          <div style="display:flex; gap:6px; justify-content:center; flex-wrap:wrap; background:#FFF; padding:10px; border-radius:10px; border:1px solid #C6DAFC;">
            <span class="pill blue" style="font-size:11px;">Paket 1 (16 foto)</span>
            <span class="pill blue" style="font-size:11px;">Paket 2 (16 foto)</span>
            <span class="pill blue" style="font-size:11px;">…</span>
            <span class="pill blue" style="font-size:11px;">Paket 9</span>
          </div>
          <div class="card-body" style="font-size:13.2px;">
            <ul>
              <li>Komputer tidak memuat ribuan foto sekaligus agar memori GPU tidak penuh — dipecah jadi paket kecil (<strong><em>Batch</em></strong>).</li>
              <li>Selesai 1 paket → hitung rata-rata Loss → update bobot 1 kali.</li>
            </ul>
          </div>
          <div class="callout"><strong>Contoh Frozen:</strong> <code>128</code> foto latih ÷ <code>batch_size=16</code> = <strong>8 kali update bobot</strong> dalam 1 putaran!</div>
        </div>
        <div class="card tint-red" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div><span class="pill red">EPOCH (mis. 10 putaran)</span><div class="card-title" style="margin-top:4px;">Berapa Kali Menamatkan 1 Buku?</div></div>
          <div style="display:flex; gap:8px; align-items:center; justify-content:center; background:#FFF; padding:10px; border-radius:10px; border:1px solid #F6AEA9; font-family:var(--font-code); font-size:12px; font-weight:700;">
            <span style="padding:5px 10px; background:#FCE8E6; border-radius:7px; color:#C5221F;">Epoch 1</span> →
            <span style="padding:5px 10px; background:#FEF7E0; border-radius:7px; color:#B06000;">Epoch 2</span> →
            <span>…</span> →
            <span style="padding:5px 10px; background:#E6F4EA; border-radius:7px; color:#137333;">Epoch 10</span>
          </div>
          <div class="card-body" style="font-size:13.2px;">
            <ul>
              <li><strong>1 Epoch</strong> = AI sudah melihat <strong>seluruh foto di Train Set tepat 1 kali penuh</strong>.</li>
              <li>Sama seperti membaca buku ujian: baca 1 kali belum paham → ulangi 10–20 kali.</li>
            </ul>
          </div>
          <div class="callout red"><strong>Peringatan:</strong> Mengulang terlalu banyak <em>epoch</em> tanpa rem bisa membuat AI &ldquo;menghafal&rdquo; foto latih (<strong>Overfitting</strong>)!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 36: STEP 9 — PENGENALAN OVERFITTING (POLOS VS RAMAI) -->
    <section class="slide" data-title="Step 9: Overfitting — Menghafal Kunci vs Paham Pola" data-notes="Alokasi waktu: 1 menit. Jelaskan Overfitting dengan analogi murid yang hafal soal latihan (Elsa Polos) tapi gugur saat ujian bertemu foto baru (Elsa Ramai di rak).">
      <div class="kicker">BAB 3 · STEP 9 · BAHAYA UTAMA DATASET KECIL</div>
      <h2>Mengenal <span class="hl-red">Overfitting</span>: Pintar di Latihan, Gugur di Ujian!</h2>
      <div class="grid-3">
        <div class="card tint-yellow" style="justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <div><span class="pill yellow">UNDERFITTING</span><div class="card-title" style="margin-top:4px;">Belum Cukup Belajar</div></div>
          <div class="card-body" style="font-size:13px;"><ul><li>Train Loss tinggi &amp; Val Loss tinggi.</li><li>Analogi: murid baru baca 1 halaman, latihan &amp; ujian sama-sama gagal.</li></ul></div>
          <div class="mini-box"><strong>Tanda:</strong> Kedua grafik tetap tinggi &amp; datar.</div>
        </div>
        <div class="card tint-green" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div><span class="pill green">GOOD FIT (IDEAL) ★</span><div class="card-title" style="margin-top:4px;">Paham Ciri Karakter</div></div>
          <div class="card-body" style="font-size:13px;"><ul><li>Train Loss turun &amp; Val Loss ikut turun rapat.</li><li>Model mengenali wajah &amp; kostum Frozen di latar baru!</li></ul></div>
          <div class="mini-box"><strong>Tanda:</strong> Garis biru &amp; merah turun bersama.</div>
        </div>
        <div class="card tint-red" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div><span class="pill red">OVERFITTING ⚠️</span><div class="card-title" style="margin-top:4px;">Menghafal Foto Latih</div></div>
          <div class="card-body" style="font-size:13px;"><ul><li>Train Loss mendekati 0, <strong>tetapi Val Loss malah NAIK!</strong></li><li>AI menghafal warna dinding/tangan, bukan karakter Frozen!</li></ul></div>
          <div class="mini-box"><strong>Tanda:</strong> Garis biru &amp; merah makin melebar!</div>
        </div>
      </div>
      <div class="callout red" style="margin-top:10px;"><strong>Kenapa Penting di Project Kita?</strong> Karena dataset Frozen <code>v1</code> masih kecil (<code>{total_imgs}</code> foto), memantau <strong>Train Loss vs Val Loss</strong> adalah wajib!</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 37: STEP 10 — SIMULATOR #5 (EVALUASI KURVA LOSS — PADAT DENGAN 3 KPI LIVE!) -->
    <section class="slide" data-title="Simulator #5: Membaca Kurva Loss (Train vs Val)" data-notes="Alokasi waktu: 1 menit. Demo interaktif! Klik Underfitting, Good Fit, dan Overfitting. Perhatikan 3 angka KPI live di kanan (Train Loss, Val Loss, Gap) agar peserta bisa membaca grafik training dengan cepat.">
      <div class="kicker">BAB 3 · STEP 10 · SIMULATOR INTERAKTIF #5</div>
      <h2>Membaca Kurva <em>Loss</em>: <span class="hl-blue">Underfitting, Good Fit, &amp; Overfitting</span></h2>
      <div class="split-60-40">
        <div class="canvas-box">
          <div id="ov-btns" class="sim-bar pdf-keep-ui">
            <button type="button" class="btn-ui outline" data-ov="under" onclick="setOvMode('under')" style="padding:5px 11px; font-size:11.5px;">1. Underfitting</button>
            <button type="button" class="btn-ui" data-ov="good" onclick="setOvMode('good')" style="padding:5px 11px; font-size:11.5px;">2. Good Fit (Ideal)</button>
            <button type="button" class="btn-ui outline" data-ov="over" onclick="setOvMode('over')" style="padding:5px 11px; font-size:11.5px;">3. Overfitting</button>
          </div>
          <canvas id="ov-canvas" width="580" height="320"></canvas>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div>
            <div id="ov-title" class="card-title">Good Fit (Ideal)</div>
            <div id="ov-desc" class="card-body" style="font-size:13px; margin-top:5px;">Deskripsi kondisi kurva.</div>
          </div>
          <div class="grid-3" style="flex:0 0 auto; gap:8px;">
            <div class="kpi-mini"><div id="ov-k-tr" class="k-num">0.19</div><div class="k-lbl">Train Loss</div></div>
            <div class="kpi-mini"><div id="ov-k-va" class="k-num" style="color:#EA4335;">0.28</div><div class="k-lbl">Val Loss</div></div>
            <div class="kpi-mini"><div id="ov-k-gap" class="k-num" style="color:#137333;">+0.09</div><div class="k-lbl">Selisih Gap</div></div>
          </div>
          <div id="ov-signs" class="mini-box" style="font-size:12.2px;">Ciri cepat terlihat di grafik.</div>
          <div id="ov-action" class="callout green" style="padding:8px 12px; font-size:12.5px;">Tindakan disarankan.</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    s.append(
        _qa_slide(
            qa_id="qa4",
            qa_num=4,
            kicker="TANYA-JAWAB #4 · LEARNING RATE",
            title_html='Cek Pemahaman: <span class="hl-red">Apa Efek Learning Rate Terlalu Besar?</span>',
            question_html="Saat melatih model di Keras, kamu memasang <code>learning_rate = 0.5</code> (terlalu besar). Apa yang paling mungkin terlihat pada grafik <em>Loss</em>?",
            choices=[
                "<strong>A.</strong> Loss turun mulus dan akurasi langsung 100%",
                "<strong>B.</strong> Bobot melompat melewati dasar lembah sehingga Loss naik-turun liar atau malah meningkat",
                "<strong>C.</strong> Jumlah foto di folder otomatis berkurang",
            ],
            answer_html="<strong>Jawaban: B — Loss naik-turun liar / gagal stabil!</strong><br/>Langkah terlalu lebar membuat bola terus terlempar ke dinding seberang lembah. Solusi cepat: kecilkan <code>learning_rate</code> (mis. <code>0.001</code>)!",
            vis_q_html='<span class="pill red">INGAT ANALOGI SHOWER</span><div class="mini-box" style="margin-top:10px;">Kalau kamu memutar keran shower terlalu brutal setiap kali kurang hangat, apa yang terjadi pada suhu air?</div>',
            vis_a_html='<span class="pill green">TEPAT!</span><div class="mini-box" style="margin-top:10px;">Air terus bolak-balik kepanasan–kedinginan! Sama seperti <em>Loss</em> yang memantul liar saat <code>LR</code> kebesaran.</div>',
            notes="Alokasi waktu: 1 menit. Tanyakan dulu ke peserta sebelum klik Reveal, lalu masuk ke Bab 4 (Jembatan menuju CNN!).",
        )
    )

    # =========================================================================
    # BAB 4: BATASAN MLP PADA FOTO FROZEN & JEMBATAN KE P03 (SLIDE 39–44 · 6.5m)
    # =========================================================================
    s.append(
        make_divider_slide(
            bg_class="bg-yellow",
            kicker="BAB 4 · JEMBATAN MENUJU P03 (CNN)",
            title="Kenapa Foto Frozen Tidak Cukup Pakai MLP Biasa?",
            description="Melihat langsung dampak Flatten pada foto Elsa 2D dan ledakan 19,2 juta bobot — alasan lahirnya CNN!",
            footer_label=FOOTER,
            data_title="Bab 4: Batasan MLP & Jembatan ke CNN",
            notes="Alokasi waktu: 0.5 menit. Bab 4 menjembatani mulus dari P02 (ANN/MLP) ke P03 (CNN) memakai foto nyata Elsa.",
        )
    )

    s.append(
        f"""
    <!-- 40: STEP 1 — MEMAHAMI FLATTEN PADA FOTO ELSA -->
    <section class="slide" data-title="Step 1: Apa Itu Flatten pada Foto 2D?" data-notes="Alokasi waktu: 1.5 menit. Jelaskan Flatten secara sederhana: layer Dense hanya bisa menerima 1 deretan angka (vektor 1D), jadi foto Elsa 2D harus dipecah per baris lalu disambung memanjang!">
      <div class="kicker">BAB 4 · STEP 1 · OPERASI FLATTEN PADA GAMBAR</div>
      <h2><em>Flatten</em>: Meratakan Foto 2D <span class="hl-blue">Elsa</span> Menjadi 1 Baris Angka</h2>
      <div class="img-box" style="height:auto; flex:1; padding:7px;">
        <img src="assets/P02/05_flatten_frozen_visual.png" alt="Visualisasi Flatten Foto Elsa dan Ledakan Parameter" />
      </div>
      <div class="callout red" style="margin-top:9px; font-size:13.2px;">
        <strong>Masalah Utama <em>Flatten</em>:</strong> Foto Elsa <code>224×224×3</code> diratakan baris demi baris menjadi <strong>1 vektor panjang <code>150.528</code> angka</strong>. Akibatnya, piksel kepala dan bahu yang tadinya bertetangga atas-bawah jadi terpisah jauh — <strong>struktur 2D gambar rusak!</strong>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 41: STEP 2 — SIMULATOR #6 (LEDAKAN PARAMETER MLP + RASIO 192x!) -->
    <section class="slide" data-title="Simulator #6: Kalkulator Ledakan Parameter MLP" data-notes="Alokasi waktu: 1.5 menit. Demo interaktif! Bandingkan MNIST 28x28 vs Frozen 64x64x3 vs Frozen standar 224x224x3 — bobot melonjak 192 kali lipat menjadi 19,27 juta bobot hanya di 1 layer!">
      <div class="kicker">BAB 4 · STEP 2 · SIMULATOR INTERAKTIF #6</div>
      <h2>Kalkulator <span class="hl-red">Ledakan Bobot</span> MLP pada Foto</h2>
      <div class="split-40-60">
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div>
            <div style="font-family:var(--font-title); font-size:13.5px; font-weight:700; margin-bottom:7px;">1. Pilih Ukuran Input Foto</div>
            <div id="fl-presets" class="sim-bar pdf-keep-ui">
              <button type="button" class="btn-ui outline" data-fl="mnist" onclick="setFlMode('mnist')" style="padding:5px 9px; font-size:11.5px;">MNIST 28×28</button>
              <button type="button" class="btn-ui outline" data-fl="f64" onclick="setFlMode('f64')" style="padding:5px 9px; font-size:11.5px;">Frozen 64×64×3</button>
              <button type="button" class="btn-ui" data-fl="f224" onclick="setFlMode('f224')" style="padding:5px 9px; font-size:11.5px;">Frozen 224×224×3</button>
            </div>
            <div class="sim-slider-row" style="margin-top:11px;">
              <span>Neuron Hidden</span>
              <input id="fl-units" type="range" min="32" max="256" step="32" value="128" oninput="updateFlSim()"/>
              <span id="fl-units-v" class="sim-val">128</span>
            </div>
          </div>
          <div class="card tint-red" style="padding:11px; gap:3px; text-align:center;">
            <div style="display:flex; justify-content:center; gap:6px; align-items:center;">
              <span style="font-size:10.5px; font-weight:700; color:#C5221F;">BOBOT LAYER 1</span>
              <span id="fl-ratio" class="pill red" style="font-size:10px; padding:2px 7px;">192× MNIST!</span>
            </div>
            <div id="fl-params" class="big-num" style="font-size:27px; color:#C5221F;">19.267.712</div>
            <span id="fl-input-len" style="font-family:var(--font-code); font-size:11px; color:#3C4043;">150.528 input × 128 neuron</span>
          </div>
          <div id="fl-note" class="callout red" style="padding:8px 11px; font-size:12.4px;">Bahaya overfitting!</div>
        </div>
        <div class="canvas-box">
          <canvas id="fl-canvas" width="560" height="330"></canvas>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 42: STEP 3 — DAMPAK NYATA DI FOTO POLOS VS RAMAI (FOTO LEBIH BESAR & RAPAT) -->
    <section class="slide" data-title="Step 3: Dua Alasan MLP Mudah Terkecoh di Foto Frozen" data-notes="Alokasi waktu: 1 menit. Tunjukkan perbandingan foto nyata Elsa Polos vs Elsa Ramai berdampingan: di foto ramai Elsa bergeser dan dikelilingi properti rak, sehingga MLP mudah menghafal latar.">
      <div class="kicker">BAB 4 · STEP 3 · BUKTI DI DATASET PROYEK KITA</div>
      <h2>Kenapa MLP Mudah Bingung di <span class="hl-red">Foto Polos vs Ramai</span>?</h2>
      <div class="grid-2">
        <div class="card surface" style="justify-content:space-between; padding:16px 18px;">
          <div class="card-top-bar bar-red"></div>
          <div style="display:flex; gap:14px; justify-content:center; align-items:center;">
            <div style="text-align:center;"><img src="assets/P02/thumb_elsa.jpg" alt="Elsa Polos" style="width:162px; height:162px; border-radius:12px; object-fit:cover; border:2.5px solid var(--blue);" /><div style="font-size:12px; font-weight:700; color:var(--blue-text); margin-top:5px;">Elsa · Polos (Tengah)</div></div>
            <div style="text-align:center;"><img src="assets/P02/thumb_elsa_ramai.jpg" alt="Elsa Ramai" style="width:162px; height:162px; border-radius:12px; object-fit:cover; border:2.5px solid var(--red);" /><div style="font-size:12px; font-weight:700; color:var(--red); margin-top:5px;">Elsa · Ramai (Geser + Rak)</div></div>
          </div>
          <div>
            <div class="card-title">1. Posisi Bergeser Sedikit → Semua Indeks Piksel Berubah!</div>
            <div class="card-body" style="font-size:13.2px; margin-top:5px;">MLP menghafal &ldquo;piksel nomor #50.120 harus biru&rdquo;. Begitu Elsa bergeser sedikit ke kiri di foto ramai, nomor piksel birunya berpindah semua sehingga model bingung!</div>
          </div>
        </div>
        <div class="card surface" style="justify-content:space-between; padding:16px 18px;">
          <div class="card-top-bar bar-yellow"></div>
          <div>
            <span class="pill red">TIDAK SEIMBANG!</span>
            <div class="big-num" style="color:#C5221F; margin-top:6px;">19.2 Juta vs {total_imgs} Foto</div>
          </div>
          <div>
            <div class="card-title">2. Terlalu Banyak Bobot = Menghafal Latar Belakang</div>
            <div class="card-body" style="font-size:13.2px; margin-top:5px;">
              <ul>
                <li>Jumlah bobot MLP jauh terlalu besar untuk {total_imgs} foto → model malah menghafal warna dinding atau properti rak (<strong>Overfitting</strong>).</li>
                <li><strong>Solusi di P03:</strong> Arsitektur yang membaca foto <strong>tetap dalam bentuk 2D utuh</strong> &amp; jauh lebih hemat bobot → <strong>CNN!</strong></li>
              </ul>
            </div>
          </div>
          <div class="callout yellow"><strong>Kabar Baiknya:</strong> Di P03 kita hanya mengganti bagian ekstraksi ciri depannya menjadi <strong>CNN</strong>!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    s.append(
        _qa_slide(
            qa_id="qa5",
            qa_num=5,
            kicker="TANYA-JAWAB #5 · JEMBATAN KE P03",
            title_html='Cek Pemahaman: <span class="hl-blue">Apa Masalah Utama MLP untuk Foto?</span>',
            question_html="Jika foto Frozen <code>224×224×3</code> langsung di-<em>flatten</em> masuk ke MLP biasa (<code>Dense</code>), dua masalah besar apa yang muncul?",
            choices=[
                "<strong>A.</strong> MLP tidak bisa memakai aktivasi ReLU dan Softmax",
                "<strong>B.</strong> Struktur 2D gambar rusak dan jumlah bobot meledak jutaan sehingga mudah <em>overfitting</em>",
                "<strong>C.</strong> Foto tidak bisa dibuka menggunakan Python",
            ],
            answer_html="<strong>Jawaban: B — Struktur 2D rusak &amp; jumlah bobot meledak!</strong><br/>Itulah alasan tepat mengapa di sesi <strong>P03</strong> kita mempelajari <strong>Convolutional Neural Network (CNN)</strong>!",
            vis_q_html='<span class="pill yellow">INGAT 2 FAKTA INI</span><div class="mini-box" style="margin-top:10px;">1) Foto 2D diratakan jadi 1 vektor panjang (<code>Flatten</code>)<br/>2) Layer 1 butuh <strong>19.267.712 bobot</strong> untuk <code>143</code> foto!</div>',
            vis_a_html='<span class="pill green">SIAP LANJUT KE CNN!</span><div class="mini-box" style="margin-top:10px;"><strong>CNN (P03)</strong> memindai gambar tetap dalam matriks <strong>2D utuh</strong> dengan filter kecil <code>3×3</code> yang dipakai ulang di seluruh foto!</div>',
            notes="Alokasi waktu: 1 menit. Pastikan peserta benar-benar merasakan alasan logis mengapa kita membutuhkan CNN di P03.",
        )
    )

    s.append(
        f"""
    <!-- 44: STEP 4 — GAMBAR BESAR PIPELINE (ILMU P02 TETAP DIPAKAI DI MODEL FINAL — VISUAL PIPELINE!) -->
    <section class="slide" data-title="Step 4: Ilmu P02 Tetap Dipakai di Model Final Kita!" data-notes="Alokasi waktu: 1 menit. Yakinkan peserta bahwa seluruh ilmu P02 hari ini (Dense, ReLU, Softmax, Loss, Adam) tetap dipakai sebagai classification head di ujung MobileNetV2!">
      <div class="kicker">BAB 4 · STEP 4 · GAMBAR BESAR PROJECT AKHIR</div>
      <h2>Materi Hari Ini Tetap Menjadi <span class="hl-green">Classification Head</span> Model Final!</h2>
      <div class="grid-3" style="flex:0 0 auto;">
        <div class="card tint-blue" style="padding:15px;">
          <div class="card-top-bar bar-blue"></div>
          <span class="pill blue">P01 · SELESAI ✓</span>
          <div class="card-title">1. Preprocessing Data</div>
          <div class="card-body" style="font-size:13px;">Foto mentah Frozen → EXIF, Audit, Resize <code>224×224</code>, Normalisasi <code>0.0–1.0</code>.</div>
        </div>
        <div class="card tint-yellow" style="padding:15px;">
          <div class="card-top-bar bar-yellow"></div>
          <span class="pill yellow">P03 &amp; P04 · BERIKUTNYA</span>
          <div class="card-title">2. Feature Extractor (CNN)</div>
          <div class="card-body" style="font-size:13px;">Filter 2D (<code>MobileNetV2</code>) mengekstrak bentuk gaun, wajah, &amp; tanduk secara utuh tanpa <em>Flatten</em> mentah!</div>
        </div>
        <div class="card tint-green" style="padding:15px;">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">P02 · HARI INI ★</span>
          <div class="card-title">3. Classification Head (ANN)</div>
          <div class="card-body" style="font-size:13px;">Di ujung CNN, kita <strong>tetap memakai materi P02</strong>: <code>Dense + Softmax(5)</code>, <code>Loss</code>, &amp; <code>Adam</code>!</div>
        </div>
      </div>
      <div class="card surface" style="margin-top:14px; flex:1; justify-content:space-between; padding:16px 20px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:12px 16px;">
          <div style="display:flex; align-items:center; gap:9px;">
            <img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:52px; height:52px; border-radius:9px; object-fit:cover; border:2px solid var(--blue);" />
            <div style="font-size:12px;"><strong>Input Foto (P01)</strong><br/><code>224×224×3</code></div>
          </div>
          <span style="font-size:20px; font-weight:700; color:var(--blue-text);">→</span>
          <div class="mini-box" style="background:var(--tint-yellow); border-color:#FDE293; text-align:center; padding:8px 14px;"><strong>CNN Backbone (P03–P04)</strong><br/><code>Conv2D / MobileNetV2</code></div>
          <span style="font-size:20px; font-weight:700; color:var(--green);">→</span>
          <div class="mini-box" style="background:var(--tint-green); border-color:#A8DAB5; text-align:center; padding:8px 14px;"><strong>ANN Head (P02)</strong><br/><code>Dense + Softmax(5)</code></div>
          <span style="font-size:20px; font-weight:700; color:#137333;">→</span>
          <div style="text-align:center; font-family:var(--font-code); font-size:12.5px; font-weight:700; color:#137333; background:#E6F4EA; padding:8px 12px; border-radius:10px;">ELSA<br/>94.2%</div>
        </div>
        <div class="callout" style="padding:8px 14px; font-size:13px;">Sekarang kamu sudah menguasai fondasi <strong>Data (P01)</strong> dan <strong>Classification Head ANN (P02)</strong> — saatnya istirahat 5 menit lalu praktik di notebook!</div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>
"""
    )

    # =========================================================================
    # BAB 5: ISTIRAHAT, PRAKTIK HANDS-ON, MINI-CHALLENGE, KAMUS, KUIS & REFERENSI (SLIDE 45–59 · 72.0m)
    # =========================================================================
    s.append(
        make_divider_slide(
            bg_class="bg-blue",
            kicker="BAB 5 · ISTIRAHAT 5 MENIT & PRAKTIK HANDS-ON",
            title="Saatnya Praktik Santai di Notebook!",
            description="Istirahat 5 menit dulu (minum air & regangkan mata), lalu kita coba langsung 1 neuron, Softmax, dan MLP pertama di Keras.",
            footer_label=FOOTER,
            data_title="Bab 5: Istirahat & Praktik Hands-On",
            notes="Alokasi waktu: 5 menit. Beri jeda istirahat penuh 5 menit sebelum membuka notebook P02_neural_network_ann.ipynb.",
        )
    )

    s.append(
        f"""
    <!-- 46: PETA 6 LANGKAH PRAKTIK HANDS-ON -->
    <section class="slide" data-title="6 Langkah Praktik Hands-On P02 (±50 Menit)" data-notes="Alokasi waktu: 44 menit. Pandu peserta mengerjakan P02_neural_network_ann.ipynb sel demi sel dari Setup 1-3 sampai Langkah 6. Setiap sel hanya 5-15 baris dan ada tombol Hint & Jawaban.">
      <div class="kicker">BAB 5 · PRAKTIK NOTEBOOK (<code>P02_neural_network_ann.ipynb</code>)</div>
      <h2>6 Langkah Praktik <span class="hl-blue">Ramah Pemula</span> (5–15 Baris / Sel)</h2>
      <div class="grid-3">
        <div class="card surface" style="padding:13px;"><div class="card-top-bar bar-blue"></div><span class="pill blue">LANGKAH 1 · 8m</span><div class="card-title" style="font-size:15px;">1 Neuron di NumPy</div><div class="card-body" style="font-size:12.8px;">Ambil warna RGB foto asli <strong>Elsa &amp; Olaf</strong>, hitung <code>z = x·w + b</code>, serta tulis fungsi <code>relu()</code> &amp; <code>sigmoid()</code>.</div></div>
        <div class="card surface" style="padding:13px;"><div class="card-top-bar bar-red"></div><span class="pill red">LANGKAH 2 · 6m</span><div class="card-title" style="font-size:15px;">Softmax Manual vs Keras</div><div class="card-body" style="font-size:12.8px;">Hitung <code>softmax_manual()</code> untuk 5 karakter Frozen lalu buktikan hasilnya persis sama dengan <code>tf.nn.softmax</code>.</div></div>
        <div class="card surface" style="padding:13px;"><div class="card-top-bar bar-green"></div><span class="pill green">LANGKAH 3 · 12m</span><div class="card-title" style="font-size:15px;">MLP Pertama di Keras</div><div class="card-body" style="font-size:12.8px;">Normalisasi gambar <code>28×28</code> (Fashion-MNIST / MNIST), susun <code>Flatten → Dense(64) → Softmax</code>, &amp; latih!</div></div>
        <div class="card surface" style="padding:13px;"><div class="card-top-bar bar-yellow"></div><span class="pill yellow">LANGKAH 4 · 10m</span><div class="card-title" style="font-size:15px;">Eksperimen LR &amp; Aktivasi</div><div class="card-body" style="font-size:12.8px;">Uji <code>LR = 0.001</code> vs <code>LR = 0.1</code> serta <code>ReLU</code> vs <code>Sigmoid</code>, lalu simpan grafik kurva <em>Val Loss</em>.</div></div>
        <div class="card surface" style="padding:13px;"><div class="card-top-bar bar-red"></div><span class="pill red">LANGKAH 5 · 10m</span><div class="card-title" style="font-size:15px;">Flatten Foto Frozen</div><div class="card-body" style="font-size:12.8px;">Muat <code>{total_imgs}</code> foto <code>data/frozen_v1/</code>, bangun MLP 5 kelas, &amp; lihat ledakan bobot <code>64×64</code> vs <code>224×224</code>!</div></div>
        <div class="card surface" style="padding:13px;"><div class="card-top-bar bar-blue"></div><span class="pill blue">LANGKAH 6 · 4m</span><div class="card-title" style="font-size:15px;">Cek Mini-Challenge</div><div class="card-body" style="font-size:12.8px;">Cocokkan tebakan Softmax manual <code>[2.0, 1.0, 0.0]</code> dan simpan tabel perbandingan ke <code>results/</code>.</div></div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 47: DI BALIK LAYAR KODE 1/2 (DENGAN CONTOH OUTPUT NYATA!) -->
    <section class="slide" data-title="Di Balik Layar: 1 Neuron &amp; Softmax di NumPy" data-notes="Alokasi waktu: 1 menit. Tinjau kembali kode pendek Langkah 1 dan Langkah 2 beserta contoh output nyatanya di notebook.">
      <div class="kicker">BAB 5 · BEDAH KODE RINGKAS (1/2)</div>
      <h2>Ternyata Neuron &amp; Softmax Cuma <span class="hl-blue">3 Baris Python!</span></h2>
      <div class="grid-2">
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">1 Neuron + ReLU (NumPy)</div>
          <pre class="code"><code># 1. Hitung skor z = input * weight + bias
z = float(np.dot(x_elsa, w) + b)

# 2. Fungsi aktivasi ReLU
output_relu = np.maximum(0.0, z)</code></pre>
          <div class="mini-box" style="font-family:var(--font-code); font-size:11.8px;"><strong>Output Notebook:</strong><br/>Input RGB Elsa: <code>[0.67, 0.66, 0.67]</code><br/>Skor <code>z = +0.70</code> → ReLU = <code>0.70</code> ✓</div>
          <div class="callout"><code>np.dot(x, w)</code> otomatis mengalikan tiap pasangan lalu menjumlahkannya!</div>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Softmax Stabil (NumPy vs Keras)</div>
          <pre class="code"><code>def softmax_manual(logits):
    shifted = logits - np.max(logits)
    exp_val = np.exp(shifted)
    return exp_val / np.sum(exp_val)

probs_keras = tf.nn.softmax(logits_frozen).numpy()</code></pre>
          <div class="mini-box" style="font-family:var(--font-code); font-size:11.8px;"><strong>Output Notebook:</strong><br/>Selisih manual vs Keras: <code>0.000000</code><br/>Prediksi teratas: <strong>ELSA</strong> ✓</div>
          <div class="callout green">Mengurangi <code>np.max(logits)</code> menjaga komputer tidak error angka terlalu besar!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 48: DI BALIK LAYAR KODE 2/2 (DENGAN OUTPUT PARAMETER!) -->
    <section class="slide" data-title="Di Balik Layar: Membangun MLP di Keras" data-notes="Alokasi waktu: 1 menit. Petakan 4 baris kode Sequential di Keras kembali ke teori Bab 1-3 agar peserta paham arti setiap argumen tanpa menghafal buta.">
      <div class="kicker">BAB 5 · BEDAH KODE RINGKAS (2/2)</div>
      <h2>Membangun MLP di <span class="hl-red">TensorFlow / Keras</span></h2>
      <div class="split-60-40">
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div class="card-title">Arsitektur &amp; Compile MLP 5 Kelas Frozen</div>
          <pre class="code"><code>model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(64, 64, 3)),
    tf.keras.layers.Flatten(),                      # 12.288 angka
    tf.keras.layers.Dense(128, activation="relu"),  # Hidden layer
    tf.keras.layers.Dense(5, activation="softmax"), # 5 karakter
])
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)</code></pre>
          <div class="mini-box" style="font-family:var(--font-code); font-size:11.8px;"><strong>Hasil <code>model.count_params()</code>:</strong> <code>64×64×3</code> = <strong>1.573.637</strong> bobot | <code>224×224×3</code> = <strong>19.268.485</strong> bobot!</div>
        </div>
        <div class="card surface" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Peta 1-ke-1 dengan Teori Hari Ini</div>
          <div class="card-body" style="font-size:13px;">
            <ul>
              <li><code>Flatten()</code> → Bab 4 (meratakan foto 2D jadi 1 vektor).</li>
              <li><code>Dense(128, "relu")</code> → Bab 1 &amp; 2 (128 neuron + aktivasi ReLU).</li>
              <li><code>Dense(5, "softmax")</code> → Bab 2 (probabilitas 100% untuk 5 karakter).</li>
              <li><code>sparse_categorical_crossentropy</code> → Bab 3 (fungsi Loss multi-kelas).</li>
              <li><code>Adam(0.001)</code> → Bab 3 (optimizer Gradient Descent).</li>
            </ul>
          </div>
          <div class="callout green">Di P03, kita cukup mengganti <code>Flatten()</code> di depan dengan <strong><code>Conv2D + MaxPooling2D</code></strong>!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 49: MINI-CHALLENGE SOFTMAX (DENGAN THUMBNAIL FROZEN!) -->
    <section class="slide" data-title="Mini-Challenge: Tebak Output Softmax Tanpa Kalkulator" data-notes="Alokasi waktu: 12 menit. Sesuai PLAN.md! Ajak peserta menebak urutan dan perkiraan persen Softmax dari skor [2.0, 1.0, 0.0] tanpa kalkulator dulu, diskusikan bersama, baru klik Kunci Diskusi.">
      <div class="kicker">BAB 5 · MINI-CHALLENGE (10–15 MENIT)</div>
      <h2>Tebak Output <span class="hl-green">Softmax</span> Tanpa Kalkulator!</h2>
      <div class="grid-2">
        <div class="card tint-blue" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div class="card-title">Skenario Tantangan</div>
          <div style="display:flex; justify-content:space-around; gap:8px;">
            <div style="text-align:center;"><img src="assets/P02/thumb_elsa.jpg" alt="Elsa" style="width:66px; height:66px; border-radius:10px; object-fit:cover; border:2px solid var(--blue);"/><div style="font-family:var(--font-code); font-size:12px; font-weight:700;">Elsa = 2.0</div></div>
            <div style="text-align:center;"><img src="assets/P02/thumb_anna.jpg" alt="Anna" style="width:66px; height:66px; border-radius:10px; object-fit:cover; border:2px solid var(--red);"/><div style="font-family:var(--font-code); font-size:12px; font-weight:700;">Anna = 1.0</div></div>
            <div style="text-align:center;"><img src="assets/P02/thumb_olaf.jpg" alt="Olaf" style="width:66px; height:66px; border-radius:10px; object-fit:cover; border:2px solid var(--green);"/><div style="font-family:var(--font-code); font-size:12px; font-weight:700;">Olaf = 0.0</div></div>
          </div>
          <div class="card-body" style="font-size:13.4px;">
            <ol style="padding-left:18px; display:flex; flex-direction:column; gap:6px;">
              <li>Tanpa kalkulator, siapa peluang terbesar? Di atas atau di bawah 50%?</li>
              <li>Kenapa jumlah peluang ketiganya <strong>selalu tepat <code>1.0</code> (100%)</strong>?</li>
              <li><strong>Bonus:</strong> Jika semua skor ditambah <code>+10</code> jadi <code>[12, 11, 10]</code>, apakah persentasenya berubah?</li>
            </ol>
          </div>
        </div>
        <div class="card surface" style="justify-content:center; gap:10px;">
          <div class="card-top-bar bar-green"></div>
          <div class="card-title">Pembahasan &amp; Kunci Diskusi</div>
          <div class="card-body" style="font-size:13.4px;">Diskusikan tebakanmu dulu, lalu buka kunci dan cocokkan dengan Langkah 6 Notebook!</div>
          <button class="btn-ui outline" onclick="toggleQA('mc-hint', this)">Klik untuk Lihat Kunci Diskusi</button>
          <div id="mc-hint" class="qa-answer" style="padding:12px 14px; font-size:13px;">
            <strong>1. Hasil Eksak:</strong> <code>e² ≈ 7.39</code>, <code>e¹ ≈ 2.72</code>, <code>e⁰ = 1.00</code> (total <code>11.11</code>) → <strong>Elsa = 66.5%</strong>, <strong>Anna = 24.5%</strong>, <strong>Olaf = 9.0%</strong>.<br/>
            <strong>2. Selalu 100%:</strong> Karena tiap <code>eᶻ</code> dibagi oleh jumlah seluruh <code>eᶻ</code>.<br/>
            <strong>3. Ditambah +10:</strong> <strong>TIDAK BERUBAH!</strong> Karena Softmax hanya melihat <em>selisih antar-skor</em> (<code>e¹⁰</code> saling mencoret)!
          </div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 50: KAMUS ISTILAH 1/2 (6 BARIS PADAT + CALLOUT!) -->
    <section class="slide" data-title="Kamus Istilah Santai (Bagian 1/2)" data-notes="Alokasi waktu: 1 menit. Ulas singkat 6 istilah utama Bab 1 dan Bab 2 dalam bahasa sehari-hari agar tidak terasa asing lagi.">
      <div class="kicker">BAB 5 · KAMUS ISTILAH (1/2)</div>
      <h2>Kamus Cepat <span class="hl-blue">Neural Network</span> — Bagian 1</h2>
      <table class="io-table" style="font-size:13.6px;">
        <thead><tr><th style="width:27%;">Istilah Asli</th><th>Penjelasan Sederhana</th></tr></thead>
        <tbody>
          <tr><td style="padding:10px 12px;"><strong>Neuron / Unit</strong></td><td style="padding:10px 12px;">Unit hitung kecil yang menjumlahkan <code>input × weight + bias</code> lalu melewatkannya ke fungsi aktivasi.</td></tr>
          <tr><td style="padding:10px 12px;"><strong>Weight (<code>w</code>) &amp; Bias (<code>b</code>)</strong></td><td style="padding:10px 12px;">Parameter yang dipelajari model: <em>weight</em> = besar pengaruh tiap input, <em>bias</em> = penggeser ambang aktif.</td></tr>
          <tr><td style="padding:10px 12px;"><strong>Dense / Hidden Layer</strong></td><td style="padding:10px 12px;">Lapisan berisi banyak neuron di tengah jaringan yang mengenali pola gabungan dari input.</td></tr>
          <tr><td style="padding:10px 12px;"><strong>Forward Pass</strong></td><td style="padding:10px 12px;">Alur perhitungan maju dari kiri (foto input) ke kanan (output prediksi).</td></tr>
          <tr><td style="padding:10px 12px;"><strong>Activation Function</strong></td><td style="padding:10px 12px;">Fungsi non-linear di ujung neuron agar model bisa membentuk batas keputusan melengkung.</td></tr>
          <tr><td style="padding:10px 12px;"><strong>ReLU &amp; Sigmoid</strong></td><td style="padding:10px 12px;"><code>ReLU</code> = ubah negatif jadi <code>0</code> (standar <em>hidden layer</em>); <code>Sigmoid</code> = ubah ke <code>0–100%</code> (output 2 kelas).</td></tr>
        </tbody>
      </table>
      <div class="callout" style="margin-top:10px; padding:8px 13px; font-size:12.8px;"><strong>Ringkasan Alur Bab 1–2:</strong> <em>Input × Weight + Bias → Aktivasi ReLU → Lanjut ke Layer Berikutnya!</em></div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 51: KAMUS ISTILAH 2/2 (6 BARIS PADAT + CALLOUT!) -->
    <section class="slide" data-title="Kamus Istilah Santai (Bagian 2/2)" data-notes="Alokasi waktu: 1 menit. Ulas singkat 6 istilah utama Bab 3 dan Bab 4 agar peserta mantap memakai istilahnya saat diskusi.">
      <div class="kicker">BAB 5 · KAMUS ISTILAH (2/2)</div>
      <h2>Kamus Cepat <span class="hl-red">Neural Network</span> — Bagian 2</h2>
      <table class="io-table" style="font-size:13.6px;">
        <thead><tr><th style="width:27%;">Istilah Asli</th><th>Penjelasan Sederhana</th></tr></thead>
        <tbody>
          <tr><td style="padding:10px 12px;"><strong>Logits &amp; Softmax</strong></td><td style="padding:10px 12px;"><em>Logits</em> = skor mentah sebelum persen; <em>Softmax</em> = pengubah logits menjadi probabilitas <code>0–100%</code> (total 100%).</td></tr>
          <tr><td style="padding:10px 12px;"><strong>Loss (Cross-Entropy)</strong></td><td style="padding:10px 12px;">Angka pengukur seberapa salah prediksi model — makin mendekati <code>0</code>, makin akurat modelnya.</td></tr>
          <tr><td style="padding:10px 12px;"><strong>Gradient Descent &amp; LR</strong></td><td style="padding:10px 12px;">Cara model menurunkan <em>Loss</em> secara bertahap dengan ukuran langkah sebesar <em>Learning Rate</em>.</td></tr>
          <tr><td style="padding:10px 12px;"><strong>Backpropagation</strong></td><td style="padding:10px 12px;">Perhitungan mundur dari output ke seluruh layer untuk tahu seberapa banyak tiap bobot perlu dikoreksi.</td></tr>
          <tr><td style="padding:10px 12px;"><strong>Batch &amp; Epoch</strong></td><td style="padding:10px 12px;"><em>Batch</em> = jumlah foto per 1 kali update bobot; <em>Epoch</em> = 1 putaran penuh membaca seluruh data latih.</td></tr>
          <tr><td style="padding:10px 12px;"><strong>Overfitting &amp; Flatten</strong></td><td style="padding:10px 12px;"><em>Overfitting</em> = hafal data latih tapi buruk di data baru; <em>Flatten</em> = meratakan matriks gambar 2D jadi 1 vektor.</td></tr>
        </tbody>
      </table>
      <div class="callout red" style="margin-top:10px; padding:8px 13px; font-size:12.8px;"><strong>Ringkasan Alur Bab 3–4:</strong> <em>Forward Pass → Hitung Loss → Backpropagation → Update Bobot (Adam)!</em></div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 52: KUIS INTERAKTIF SOAL 1 & 2 -->
    <section class="slide" data-title="Kuis Interaktif — Soal 1 &amp; 2" data-notes="Alokasi waktu: 1.5 menit. Kuis santai soal 1 dan 2 sesuai PLAN.md. Biarkan peserta menjawab lisan dulu sebelum klik Lihat Jawaban.">
      <div class="kicker">BAB 5 · KUIS INTERAKTIF (5 SOAL)</div>
      <h2>Uji Pemahaman — <span class="hl-blue">Soal 1 &amp; 2</span></h2>
      <div style="display:flex; flex-direction:column; gap:14px; flex:1; justify-content:center;">
        <div class="quiz-item">
          <div><strong>1. Apa fungsi <code>bias (b)</code> pada sebuah neuron?</strong></div>
          <button class="btn-ui outline" onclick="toggleAns('qz1', this)" style="padding:5px 12px; font-size:12px;">Lihat Jawaban</button>
          <div id="qz1" class="quiz-ans"><strong>Jawaban:</strong> Menggeser standar/ambang nyala neuron sehingga batas keputusan tidak terkunci di titik nol <code>(0, 0)</code>.</div>
        </div>
        <div class="quiz-item">
          <div><strong>2. Apa yang terjadi jika <code>learning rate</code> dipasang terlalu besar saat training?</strong></div>
          <button class="btn-ui outline" onclick="toggleAns('qz2', this)" style="padding:5px 12px; font-size:12px;">Lihat Jawaban</button>
          <div id="qz2" class="quiz-ans"><strong>Jawaban:</strong> Langkah pembaruan bobot melompat melewati dasar lembah sehingga Loss naik-turun liar, sulit konvergen, atau meledak (<code>NaN</code>).</div>
        </div>
      </div>
      <div class="callout" style="padding:8px 13px; font-size:12.5px;"><strong>Tips:</strong> Jawab dulu dengan bahasamu sendiri sebelum membuka tombol hijau di atas!</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 53: KUIS INTERAKTIF SOAL 3 & 4 -->
    <section class="slide" data-title="Kuis Interaktif — Soal 3 &amp; 4" data-notes="Alokasi waktu: 1.5 menit. Kuis soal 3 dan 4 mencakup alasan ReLU & Softmax serta mengenali Overfitting.">
      <div class="kicker">BAB 5 · KUIS INTERAKTIF (5 SOAL)</div>
      <h2>Uji Pemahaman — <span class="hl-red">Soal 3 &amp; 4</span></h2>
      <div style="display:flex; flex-direction:column; gap:14px; flex:1; justify-content:center;">
        <div class="quiz-item">
          <div><strong>3. Mengapa <code>ReLU</code> dipakai di <em>hidden layer</em>, sedangkan <code>Softmax</code> dipakai di <em>output layer</em> 5 karakter Frozen?</strong></div>
          <button class="btn-ui outline" onclick="toggleAns('qz3', this)" style="padding:5px 12px; font-size:12px;">Lihat Jawaban</button>
          <div id="qz3" class="quiz-ans"><strong>Jawaban:</strong> <code>ReLU</code> cepat, non-linear, dan menjaga sinyal tetap kuat di tengah jaringan; <code>Softmax</code> mengubah 5 skor mentah menjadi peluang <code>0–100%</code> yang jumlahnya tepat <code>100%</code>.</div>
        </div>
        <div class="quiz-item">
          <div><strong>4. Saat melihat grafik training, <em>Train Loss</em> terus turun ke <code>0.05</code>, tetapi <em>Validation Loss</em> justru berbalik naik. Apa yang sedang terjadi?</strong></div>
          <button class="btn-ui outline" onclick="toggleAns('qz4', this)" style="padding:5px 12px; font-size:12px;">Lihat Jawaban</button>
          <div id="qz4" class="quiz-ans"><strong>Jawaban:</strong> Model mengalami <strong>Overfitting</strong> — mulai menghafal foto latih/latar belakang dan gagal menggeneralisasi pada foto baru!</div>
        </div>
      </div>
      <div class="callout red" style="padding:8px 13px; font-size:12.5px;"><strong>Cek Cepat:</strong> Jika kamu bisa menjawab Soal 3 &amp; 4 dengan tepat, fondasi Bab 2 &amp; Bab 3 sudah mantap!</div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 54: KUIS INTERAKTIF SOAL 5 + SELF-CHECK KRITERIA BERHASIL (NO MORE EMPTY SLIDE!) -->
    <section class="slide" data-title="Kuis Interaktif — Soal 5 &amp; Self-Check P02" data-notes="Alokasi waktu: 1 menit. Soal terakhir memastikan jembatan ke P03 CNN paham, dilengkapi checklist 3 kriteria berhasil sesuai PLAN.md.">
      <div class="kicker">BAB 5 · KUIS SOAL 5 &amp; SELF-CHECK KELULUSAN P02</div>
      <h2>Soal Terakhir &amp; <span class="hl-green">Checklist Penguasaan P02</span></h2>
      <div class="split-60-40" style="align-items:stretch;">
        <div style="display:flex; flex-direction:column; gap:12px; justify-content:center;">
          <div class="quiz-item">
            <div><strong>5. Mengapa kita tidak cukup hanya memakai MLP (<code>Flatten → Dense</code>) untuk foto karakter Frozen ukuran <code>224×224×3</code>?</strong></div>
            <button class="btn-ui outline" onclick="toggleAns('qz5', this)" style="padding:5px 12px; font-size:12px;">Lihat Jawaban</button>
            <div id="qz5" class="quiz-ans"><strong>Jawaban:</strong> Karena (1) <code>Flatten</code> memutus tetangga 2D piksel sehingga model bingung saat objek bergeser/latar ramai, dan (2) jumlah bobot meledak (&gt;19 juta bobot di 1 layer) sehingga rawan <em>overfitting</em>. Solusinya: <strong>CNN (P03)</strong>!</div>
          </div>
        </div>
        <div class="card tint-green" style="justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <span class="pill green">KRITERIA BERHASIL P02</span>
          <div class="card-title" style="font-size:15.5px;">Sudah Bisa 3 Hal Ini?</div>
          <div class="card-body" style="font-size:13px;">
            <ul>
              <li>✅ Bisa menghitung 1 neuron (<code>w·x + b</code>) dengan tangan.</li>
              <li>✅ Bisa menjelaskan alasan <code>ReLU</code> di <em>hidden</em> &amp; <code>Softmax</code> di <em>output</em>.</li>
              <li>✅ Bisa membaca kurva <em>loss</em> turun/naik &amp; gejala <em>overfitting</em>.</li>
            </ul>
          </div>
          <div class="mini-box">Jika 3/3 tercetak di kepala, kamu <strong>100% siap</strong> masuk ke CNN di P03!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 55: 3 POIN UTAMA HARI INI (DARK — KONTRAST CODE RAPI!) -->
    <section class="slide dark" data-title="3 Poin Utama Hari Ini" data-notes="Alokasi waktu: 1 menit. Rangkum 3 pesan kunci P02 yang paling mudah diingat peserta sebelum pulang.">
      <div class="kicker">KEY TAKEAWAYS · P02</div>
      <h2 style="color:white;">3 Poin Utama <span style="color:var(--yellow);">Hari Ini</span></h2>
      <div class="grid-3" style="margin-top:8px;">
        <div class="card" style="background:#292A2D; border-color:#3C4043; justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div><div class="big-num" style="color:var(--blue);">01</div><div class="card-title" style="color:white; margin-top:4px;">Neuron, ReLU, &amp; Softmax</div></div>
          <div class="card-body" style="color:#BDC1C6; font-size:13.5px;">Setiap <em>Neuron</em> menghitung <code>input × weight + bias</code>, aktivasi <code>ReLU</code> memberi kemampuan non-linear, dan <code>Softmax</code> menghasilkan probabilitas 100% untuk 5 karakter Frozen.</div>
        </div>
        <div class="card" style="background:#292A2D; border-color:#3C4043; justify-content:space-between;">
          <div class="card-top-bar bar-green"></div>
          <div><div class="big-num" style="color:var(--green);">02</div><div class="card-title" style="color:white; margin-top:4px;">Training = Perbaiki Bobot</div></div>
          <div class="card-body" style="color:#BDC1C6; font-size:13.5px;"><em>Cross-Entropy Loss</em> mengukur kesalahan, <em>Backpropagation</em> menghitung koreksi mundur, dan <em>Gradient Descent</em> menggeser bobot sebesar <em>Learning Rate</em> — selalu pantau <em>Overfitting</em>!</div>
        </div>
        <div class="card" style="background:#292A2D; border-color:#3C4043; justify-content:space-between;">
          <div class="card-top-bar bar-red"></div>
          <div><div class="big-num" style="color:var(--red);">03</div><div class="card-title" style="color:white; margin-top:4px;">MLP → Jembatan ke CNN</div></div>
          <div class="card-body" style="color:#BDC1C6; font-size:13.5px;">Meratakan foto <code>224×224×3</code> (<code>Flatten</code>) merusak posisi 2D &amp; meledakkan &gt;19 juta bobot. Di <strong>P03</strong> kita pelajari arsitektur khusus gambar: <strong>CNN</strong>!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 56: TUGAS MANDIRI & PREVIEW P03 -->
    <section class="slide" data-title="Tugas Ringkas &amp; Preview P03 (CNN)" data-notes="Alokasi waktu: 1 menit. Sampaikan tugas ringan 1 halaman sesuai PLAN.md dan bocoran seru P03 tentang konvolusi pada foto Frozen.">
      <div class="kicker">OUTPUT SESI &amp; LANGKAH BERIKUTNYA</div>
      <h2>Tugas Ringkas &amp; <span class="hl-blue">Preview Sesi P03</span></h2>
      <div class="grid-2">
        <div class="card tint-yellow" style="justify-content:space-between;">
          <div class="card-top-bar bar-yellow"></div>
          <div><span class="pill yellow">TUGAS MANDIRI (1 HALAMAN)</span><div class="card-title" style="margin-top:4px;">Ceritakan dengan Bahasamu Sendiri</div></div>
          <div class="card-body" style="font-size:13.5px;">
            <ul>
              <li>Tulis ringkasan singkat (maks. 1 halaman atau sketsa panah) tentang <strong>&ldquo;Cara Kerja 1 Neuron sampai Softmax &amp; Proses Belajarnya&rdquo;</strong>.</li>
              <li>Sertakan 1 gambar grafik perbandingan <em>Learning Rate</em> hasil Langkah 4 Notebook P02.</li>
            </ul>
          </div>
          <div class="mini-box"><strong>Tujuan:</strong> Menguji bahwa kamu benar-benar paham dengan bahasa sendiri (bukan hafalan definisi)!</div>
        </div>
        <div class="card tint-blue" style="justify-content:space-between;">
          <div class="card-top-bar bar-blue"></div>
          <div><span class="pill blue">PREVIEW · P03 BERIKUTNYA</span><div class="card-title" style="margin-top:4px;">CNN Fundamentals &amp; Tugas Computer Vision</div></div>
          <div class="card-body" style="font-size:13.5px;">
            <ul>
              <li>Bagaimana <strong>Kernel Konvolusi 2D (<code>Conv2D</code>)</strong> membaca foto <strong>Elsa, Anna, Olaf</strong> secara utuh tanpa <em>Flatten</em> mentah!</li>
              <li>Memahami <em>Stride, Padding, Pooling, Feature Map,</em> dan <em>GAP</em>.</li>
              <li>Membedakan <em>Classification, Localization, Detection,</em> dan <em>Segmentation</em>.</li>
            </ul>
          </div>
          <div class="mini-box"><strong>Hasil di P03:</strong> Kita langsung melihat <em>Feature Map</em> nyata dari foto Frozen kita sendiri!</div>
        </div>
      </div>
      <div class="slide-footer"><span>{FOOTER}</span><span>__NUM__</span></div>
    </section>

    <!-- 57: CLOSING & KEY QUOTE -->
    <section class="slide" data-title="Closing &amp; Key Quote" data-notes="Alokasi waktu: 1 menit. Tutup sesi P02 dengan kutipan penutup dan apresiasi atas pencapaian peserta hari ini." style="background: repeating-linear-gradient(-35deg, rgba(234,67,53,0.025) 0px, rgba(234,67,53,0.025) 1px, transparent 1px, transparent 28px), #FFFFFF; justify-content: space-between;">
      <div style="display:flex; align-items:center; justify-content:space-between;">
        <span style="font-family:var(--font-title); font-size:12px; font-weight:700; letter-spacing:1.8px; color:#80868B;">CLOSING · P02</span>
        <div style="display:flex; gap:6px;">
          <span style="width:9px; height:9px; border-radius:50%; background:#4285F4;"></span>
          <span style="width:9px; height:9px; border-radius:50%; background:#EA4335;"></span>
          <span style="width:9px; height:9px; border-radius:50%; background:#FBBC04;"></span>
          <span style="width:9px; height:9px; border-radius:50%; background:#34A853;"></span>
        </div>
      </div>
      <div style="margin:auto 0; display:flex; flex-direction:column; align-items:center; text-align:center; gap:20px; padding:0 44px;">
        <div style="font-family:var(--font-title); font-size:46px; font-weight:700; line-height:0.6; color:#F6AEA9; user-select:none;">&rdquo;</div>
        <h1 style="font-family:var(--font-title); font-size:clamp(24px,2.5vw,33px); font-weight:700; line-height:1.38; color:#202124; max-width:860px; margin:0;">
          Di balik kecerdasan <span style="color:#EA4335;">Deep Learning</span> tidak ada sihir — hanya ribuan <strong>Neuron</strong> sederhana yang terus <span style="color:#1A73E8;">belajar memperbaiki bobot</span> dari kesalahannya.
        </h1>
      </div>
      <div class="slide-footer"><span>P02 - Teori Neural Network (ANN)</span><span>__NUM__</span></div>
    </section>

    <!-- 58: REFERENSI BELAJAR MANDIRI 1/2 (0 MENIT — SETARA P01: 3 KOLOM, 8 KARTU KLIK-LANGSUNG!) -->
    <section class="slide" data-title="Referensi Belajar (1/2): Neuron, ReLU, Softmax &amp; Loss" data-notes="Alokasi waktu: 0 menit. Slide referensi belajar mandiri Bagian 1/2 berisi 8 video YouTube & eksperimen interaktif berurutan untuk Bab 1 dan Bab 2 (3Blue1Brown, StatQuest, & TensorFlow Playground)." style="padding: 20px 44px 48px;">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
        <div class="kicker" style="margin-bottom:0;">REFERENSI BELAJAR MANDIRI (1/2) · BERURUTAN</div>
        <span class="pill blue" style="font-size:10.5px; padding:3px 10px;">Klik Kartu untuk Membuka Tautan ↗</span>
      </div>
      <h2 style="margin-top:4px; margin-bottom:3px;">Video &amp; Sumber Belajar: <span class="hl-blue">Neuron, ReLU, Softmax &amp; Loss</span></h2>
      <p class="subtitle" style="margin-bottom:10px; font-size:13.5px;">Ikuti urutan langkah <strong>1 → 8</strong> di bawah ini untuk memperdalam intuisi visual Bab 1–2 dengan penjelasan ramah pemula.</p>
      <div class="grid-3" style="gap:13px;">
        <div class="card" style="padding:14px 15px; gap:8px;">
          <div class="card-top-bar bar-blue"></div>
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <span class="pill blue" style="font-size:11px; padding:4px 10px;">TAHAP 1 · NEURON &amp; LAYER</span>
            <span style="font-size:11px; color:var(--muted); font-weight:600;">Bab 1</span>
          </div>
          <div class="ref-list">
            <a class="ref-item featured" href="https://www.youtube.com/watch?v=aircAruvnKk" target="_blank" rel="noopener">
              <div class="ref-num">1</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">3Blue1Brown — What is a Neural Network?</span><span class="ref-tag must">Wajib ↗</span></div>
                <div class="ref-desc">Visualisasi terbaik struktur <em>Input, Hidden, Output Layer</em>, bobot (<code>w</code>), dan bias (<code>b</code>).</div>
                <div class="ref-url">youtube.com/watch?v=aircAruvnKk</div>
              </div>
            </a>
            <a class="ref-item" href="https://www.youtube.com/watch?v=CqOfi41LfDw" target="_blank" rel="noopener">
              <div class="ref-num">2</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">StatQuest — Neural Networks Pt. 1</span><span class="ref-tag">YouTube ↗</span></div>
                <div class="ref-desc">Penjelasan super pelan dari nol tentang cara kerja 1 neuron &amp; <em>forward pass</em>.</div>
                <div class="ref-url">youtube.com/watch?v=CqOfi41LfDw</div>
              </div>
            </a>
            <a class="ref-item" href="https://3blue1brown.com/lessons/neural-networks" target="_blank" rel="noopener">
              <div class="ref-num">3</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">3Blue1Brown — Versi Tulis Interaktif</span><span class="ref-tag doc">Artikel ↗</span></div>
                <div class="ref-desc">Versi bacaan bergambar dari serial video Ch. 1–4 bagi yang suka membaca pelan.</div>
                <div class="ref-url">3blue1brown.com/lessons/neural-networks</div>
              </div>
            </a>
          </div>
          <div class="callout" style="font-size:11.2px; padding:7px 10px;"><strong>Fokus Slide:</strong> <em>Neuron, Weight, Bias &amp; Forward Pass</em>.</div>
        </div>

        <div class="card" style="padding:14px 15px; gap:8px;">
          <div class="card-top-bar bar-yellow"></div>
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <span class="pill yellow" style="font-size:11px; padding:4px 10px;">TAHAP 2 · AKTIVASI &amp; ReLU</span>
            <span style="font-size:11px; color:var(--muted); font-weight:600;">Bab 2</span>
          </div>
          <div class="ref-list">
            <a class="ref-item featured" href="https://www.youtube.com/watch?v=68BZ5f7P94E" target="_blank" rel="noopener">
              <div class="ref-num yellow">4</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">StatQuest — ReLU in Action! (Pt. 3)</span><span class="ref-tag must">Wajib ↗</span></div>
                <div class="ref-desc">Bukti visual cara <code>ReLU</code> melipat garis lurus agar jaringan mampu membentuk pola melengkung.</div>
                <div class="ref-url">youtube.com/watch?v=68BZ5f7P94E</div>
              </div>
            </a>
            <a class="ref-item featured" href="https://playground.tensorflow.org/" target="_blank" rel="noopener">
              <div class="ref-num yellow">5</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">TensorFlow Playground (Sandbox)</span><span class="ref-tag must">Interaktif ↗</span></div>
                <div class="ref-desc">Ubah jumlah neuron, ganti <code>ReLU / Sigmoid / Tanh</code>, dan geser <em>Learning Rate</em> di browser.</div>
                <div class="ref-url">playground.tensorflow.org</div>
              </div>
            </a>
            <div class="ref-sub">
              <strong>Misi 5 Menit di Playground:</strong><br/>
              &bull; Pilih pola data <em>Lingkaran</em> (mirip Slide 19)<br/>
              &bull; Bandingkan <em>Linear</em> (gagal!) vs <em>ReLU</em> (berhasil!)
            </div>
          </div>
          <div class="callout yellow" style="font-size:11.2px; padding:7px 10px;"><strong>Fokus Slide:</strong> <em>Non-Linearitas, ReLU, Sigmoid &amp; Tanh</em>.</div>
        </div>

        <div class="card" style="padding:14px 15px; gap:8px;">
          <div class="card-top-bar bar-green"></div>
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <span class="pill green" style="font-size:11px; padding:4px 10px;">TAHAP 3 · SOFTMAX &amp; LOSS</span>
            <span style="font-size:11px; color:var(--muted); font-weight:600;">Bab 2–3</span>
          </div>
          <div class="ref-list">
            <a class="ref-item featured" href="https://www.youtube.com/watch?v=KpKog-L9veg" target="_blank" rel="noopener">
              <div class="ref-num green">6</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">StatQuest — ArgMax and SoftMax</span><span class="ref-tag must">Wajib ↗</span></div>
                <div class="ref-desc">Cara <code>Softmax</code> mengubah skor mentah (<em>logits</em>) menjadi probabilitas <code>0–100%</code>.</div>
                <div class="ref-url">youtube.com/watch?v=KpKog-L9veg</div>
              </div>
            </a>
            <a class="ref-item" href="https://www.youtube.com/watch?v=6ArSys5qHAU" target="_blank" rel="noopener">
              <div class="ref-num green">7</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">StatQuest — Cross-Entropy Loss</span><span class="ref-tag">YouTube ↗</span></div>
                <div class="ref-desc">Mengapa <em>Cross-Entropy</em> memberi penalti besar pada prediksi yang salah percaya diri.</div>
                <div class="ref-url">youtube.com/watch?v=6ArSys5qHAU</div>
              </div>
            </a>
            <a class="ref-item featured" href="https://www.youtube.com/watch?v=IHZwWFHWa-w" target="_blank" rel="noopener">
              <div class="ref-num green">8</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">3Blue1Brown — Gradient Descent (Ch. 2)</span><span class="ref-tag must">Wajib ↗</span></div>
                <div class="ref-desc">Animasi visual bagaimana model menurunkan nilai <em>Loss</em> secara bertahap.</div>
                <div class="ref-url">youtube.com/watch?v=IHZwWFHWa-w</div>
              </div>
            </a>
          </div>
          <div class="callout green" style="font-size:11.2px; padding:7px 10px;"><strong>Fokus Slide:</strong> <em>Softmax 5 Kelas &amp; Cross-Entropy Loss</em>.</div>
        </div>
      </div>
      <div class="slide-footer"><span>P02 - Teori Neural Network (ANN)</span><span>__NUM__</span></div>
    </section>

    <!-- 59: REFERENSI BELAJAR MANDIRI 2/2 (0 MENIT — SETARA P01: 2 KOLOM, 8 KARTU KLIK-LANGSUNG + RUTE MARATON!) -->
    <section class="slide" data-title="Referensi Belajar (2/2): Backprop, Keras &amp; Persiapan P03" data-notes="Alokasi waktu: 0 menit. Slide referensi belajar mandiri Bagian 2/2 berisi 8 video & panduan resmi (langkah 9 sampai 16) untuk Gradient Descent, Backpropagation, Keras Sequential, CS231n, dan preview P03 CNN." style="padding: 20px 44px 48px;">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
        <div class="kicker" style="margin-bottom:0;">REFERENSI BELAJAR MANDIRI (2/2) · LANJUTAN &amp; PRAKTIK</div>
        <span class="pill red" style="font-size:10.5px; padding:3px 10px;">Training, Keras &amp; Jembatan P03</span>
      </div>
      <h2 style="margin-top:4px; margin-bottom:3px;">Video &amp; Sumber Belajar: <span class="hl-red">Backpropagation, Keras &amp; Persiapan P03</span></h2>
      <p class="subtitle" style="margin-bottom:10px; font-size:13.5px;">Urutan langkah <strong>9 → 16</strong> untuk menguasai proses training model di Keras dan bersiap masuk ke <strong>CNN (P03)</strong>.</p>
      <div class="grid-2" style="gap:15px; flex:1; min-height:0;">
        <div class="card" style="padding:14px 16px; gap:8px;">
          <div class="card-top-bar bar-red"></div>
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <span class="pill red" style="font-size:11px; padding:4px 10px;">TAHAP 4 · GRADIENT DESCENT &amp; BACKPROP</span>
            <span style="font-size:11px; color:var(--muted); font-weight:600;">Bab 3</span>
          </div>
          <div class="ref-list">
            <a class="ref-item" href="https://www.youtube.com/watch?v=sDv4f4s2SB8" target="_blank" rel="noopener">
              <div class="ref-num red">9</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">StatQuest — Gradient Descent, Step-by-Step</span><span class="ref-tag">YouTube ↗</span></div>
                <div class="ref-desc">Penjelasan pelan dan terstruktur tentang kemiringan kurva &amp; ukuran <em>Learning Rate</em>.</div>
                <div class="ref-url">youtube.com/watch?v=sDv4f4s2SB8</div>
              </div>
            </a>
            <a class="ref-item featured" href="https://www.youtube.com/watch?v=Ilg3gGewQ5U" target="_blank" rel="noopener">
              <div class="ref-num red">10</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">3Blue1Brown — Backpropagation Intuition (Ch. 3)</span><span class="ref-tag must">Wajib ↗</span></div>
                <div class="ref-desc">Intuisi visual bagaimana koreksi kesalahan dikirim mundur ke seluruh bobot jaringan.</div>
                <div class="ref-url">youtube.com/watch?v=Ilg3gGewQ5U</div>
              </div>
            </a>
            <a class="ref-item" href="https://www.youtube.com/watch?v=IN2XmBhILt4" target="_blank" rel="noopener">
              <div class="ref-num red">11</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">StatQuest — Backpropagation Details Pt. 1</span><span class="ref-tag">Opsional ↗</span></div>
                <div class="ref-desc">Contoh perhitungan pembaruan bobot langkah demi langkah bagi yang ingin detail angka.</div>
                <div class="ref-url">youtube.com/watch?v=IN2XmBhILt4</div>
              </div>
            </a>
            <a class="ref-item" href="https://www.youtube.com/watch?v=tIeHLnjs5U8" target="_blank" rel="noopener">
              <div class="ref-num red">12</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">3Blue1Brown — Backpropagation Calculus (Ch. 4)</span><span class="ref-tag">Opsional ↗</span></div>
                <div class="ref-desc">Pendamping matematis Ch. 3 (<em>chain rule</em>) — opsional untuk pendalaman kalkulus.</div>
                <div class="ref-url">youtube.com/watch?v=tIeHLnjs5U8</div>
              </div>
            </a>
          </div>
          <div class="callout red" style="font-size:11.2px; padding:7px 10px;"><strong>Fokus Slide:</strong> <em>Gradient Descent, Learning Rate &amp; Backpropagation</em>.</div>
        </div>

        <div class="card" style="padding:14px 16px; gap:8px;">
          <div class="card-top-bar bar-blue"></div>
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <span class="pill blue" style="font-size:11px; padding:4px 10px;">TAHAP 5 · KERAS, CATATAN &amp; PREVIEW P03</span>
            <span style="font-size:11px; color:var(--muted); font-weight:600;">Bab 4–5</span>
          </div>
          <div class="ref-list">
            <a class="ref-item featured" href="https://www.tensorflow.org/tutorials/keras/classification" target="_blank" rel="noopener">
              <div class="ref-num">13</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">TensorFlow — Classify Images (Fashion-MNIST)</span><span class="ref-tag must">Wajib ↗</span></div>
                <div class="ref-desc">Tutorial resmi <code>Flatten → Dense(relu) → Softmax</code> yang sejalan dengan Langkah 3 Notebook.</div>
                <div class="ref-url">tensorflow.org/tutorials/keras/classification</div>
              </div>
            </a>
            <a class="ref-item" href="https://keras.io/guides/sequential_model/" target="_blank" rel="noopener">
              <div class="ref-num">14</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">Keras Official — Sequential Model Guide</span><span class="ref-tag code">Kode ↗</span></div>
                <div class="ref-desc">Dokumentasi resmi menyusun <code>tf.keras.Sequential</code>, <code>compile()</code>, dan <code>fit()</code>.</div>
                <div class="ref-url">keras.io/guides/sequential_model</div>
              </div>
            </a>
            <a class="ref-item" href="https://cs231n.github.io/" target="_blank" rel="noopener">
              <div class="ref-num">15</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">Stanford CS231n — Lecture Notes (NN)</span><span class="ref-tag doc">Opsional ↗</span></div>
                <div class="ref-desc">Catatan kuliah visual standar emas tentang arsitektur NN, aktivasi, dan kurva loss.</div>
                <div class="ref-url">cs231n.github.io</div>
              </div>
            </a>
            <a class="ref-item" href="https://www.coursera.org/learn/neural-networks-deep-learning" target="_blank" rel="noopener">
              <div class="ref-num">16</div>
              <div class="ref-content">
                <div class="ref-head"><span class="ref-title">Coursera — Neural Networks &amp; Deep Learning</span><span class="ref-tag doc">Course ↗</span></div>
                <div class="ref-desc">Course 1 Andrew Ng (opsional); lanjutkan ke <em>CNN Week 1</em> sebagai preview sesi P03.</div>
                <div class="ref-url">coursera.org/learn/neural-networks-deep-learning</div>
              </div>
            </a>
          </div>
          <div class="callout" style="font-size:11.2px; padding:7px 10px;"><strong>Fokus Slide:</strong> <em>Praktik Keras, Flatten vs CNN &amp; Persiapan P03</em>.</div>
        </div>
      </div>
      <div class="marathon-bar">
        <span style="font-family:var(--font-title); font-size:11.5px; font-weight:700; color:var(--dark); white-space:nowrap;">Rute Maraton (±2 Jam):</span>
        <a class="marathon-step" href="https://www.youtube.com/watch?v=aircAruvnKk" target="_blank" rel="noopener"><span class="marathon-dot" style="background:var(--blue);">1</span><span>3B1B Neuron</span></a>
        <a class="marathon-step" href="https://www.youtube.com/watch?v=68BZ5f7P94E" target="_blank" rel="noopener"><span class="marathon-dot" style="background:var(--yellow); color:var(--dark);">2</span><span>StatQuest ReLU</span></a>
        <a class="marathon-step" href="https://www.youtube.com/watch?v=KpKog-L9veg" target="_blank" rel="noopener"><span class="marathon-dot" style="background:var(--green);">3</span><span>Softmax</span></a>
        <a class="marathon-step" href="https://www.youtube.com/watch?v=Ilg3gGewQ5U" target="_blank" rel="noopener"><span class="marathon-dot" style="background:var(--red);">4</span><span>Backprop</span></a>
        <a class="marathon-step" href="https://www.coursera.org/learn/convolutional-neural-networks" target="_blank" rel="noopener"><span class="marathon-dot" style="background:var(--dark);">5</span><span>Preview P03</span></a>
      </div>
      <div class="slide-footer"><span>P02 - Teori Neural Network (ANN)</span><span>__NUM__</span></div>
    </section>
"""
    )

    return "\n".join(s)


def build_extra_js(data: dict) -> str:
    cs_json = json.dumps(data["char_samples"], ensure_ascii=False)
    total_imgs = data["total_images"]
    return f"""
    // =========================================================================
    // SIMULATOR #1 (Slide 11): Kalkulator 1 Neuron + Bar Kontribusi Live
    // =========================================================================
    const FROZEN_CHAR_DATA = {cs_json};
    let n1Char = 'elsa';

    function setN1Char(kls) {{
      n1Char = kls;
      document.querySelectorAll('#n1-presets button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.char !== kls);
      }});
      const img = document.getElementById('n1-img');
      if (img) img.src = `assets/P02/thumb_${{kls}}.jpg`;
      const nameEl = document.getElementById('n1-char-name');
      if (nameEl) nameEl.textContent = kls.charAt(0).toUpperCase() + kls.slice(1) + ' (Foto Asli)';
      updateN1();
    }}

    function _renderContrib(barId, valId, v) {{
      const bar = document.getElementById(barId);
      const txt = document.getElementById(valId);
      if (txt) txt.textContent = (v >= 0 ? '+' : '') + v.toFixed(2);
      if (!bar) return;
      const pct = Math.min(50, (Math.abs(v) / 2.2) * 50);
      if (v >= 0) {{
        bar.style.left = '50%';
        bar.style.width = pct.toFixed(1) + '%';
        bar.style.background = '#34A853';
      }} else {{
        bar.style.left = (50 - pct).toFixed(1) + '%';
        bar.style.width = pct.toFixed(1) + '%';
        bar.style.background = '#EA4335';
      }}
    }}

    function updateN1() {{
      const info = FROZEN_CHAR_DATA[n1Char] || {{ rgb_norm: [0.5, 0.5, 0.5] }};
      const [r, g, bVal] = info.rgb_norm;
      const w1 = parseFloat(document.getElementById('n1-w1').value);
      const w2 = parseFloat(document.getElementById('n1-w2').value);
      const w3 = parseFloat(document.getElementById('n1-w3').value);
      const bias = parseFloat(document.getElementById('n1-b').value);

      const fmt = (v) => (v >= 0 ? '+' : '') + v.toFixed(1);
      document.getElementById('n1-w1-v').textContent = fmt(w1);
      document.getElementById('n1-w2-v').textContent = fmt(w2);
      document.getElementById('n1-w3-v').textContent = fmt(w3);
      document.getElementById('n1-b-v').textContent = fmt(bias);
      document.getElementById('n1-rgb-txt').textContent = `R=${{r.toFixed(2)}} · G=${{g.toFixed(2)}} · B=${{bVal.toFixed(2)}}`;

      const c0 = r * w1, c1 = g * w2, c2 = bVal * w3, c3 = bias;
      _renderContrib('n1-cb0', 'n1-cv0', c0);
      _renderContrib('n1-cb1', 'n1-cv1', c1);
      _renderContrib('n1-cb2', 'n1-cv2', c2);
      _renderContrib('n1-cb3', 'n1-cv3', c3);

      const z = c0 + c1 + c2 + c3;
      const relu = Math.max(0, z);
      const sig = 1 / (1 + Math.exp(-z));

      document.getElementById('n1-eq').textContent =
        `z = (${{r.toFixed(2)}}×${{fmt(w1)}}) + (${{g.toFixed(2)}}×${{fmt(w2)}}) + (${{bVal.toFixed(2)}}×${{fmt(w3)}}) + (${{fmt(bias)}}) = ${{z.toFixed(2)}}`;
      document.getElementById('n1-z').textContent = (z >= 0 ? '+' : '') + z.toFixed(2);
      document.getElementById('n1-relu').textContent = relu.toFixed(2);
      document.getElementById('n1-sig').textContent = Math.round(sig * 100) + '%';

      const st = document.getElementById('n1-status');
      if (z > 0.0) {{
        st.className = 'callout green';
        st.innerHTML = `<strong>Neuron AKTIF!</strong> Sumbangan positif mengalahkan negatif → <code>z = +${{z.toFixed(2)}}</code>, <code>ReLU = ${{relu.toFixed(2)}}</code>.`;
      }} else {{
        st.className = 'callout red';
        st.innerHTML = `<strong>Neuron TIDAK AKTIF (ReLU = 0.00)!</strong> Skor <code>z = ${{z.toFixed(2)}}</code> bernilai negatif/nol → output menjadi 0.`;
      }}
    }}
    updateN1();

    // =========================================================================
    // SIMULATOR #2 (Slide 21): Laboratorium Fungsi Aktivasi
    // =========================================================================
    let actMode = 'relu';

    function evalAct(mode, z) {{
      if (mode === 'relu') return Math.max(0, z);
      if (mode === 'sigmoid') return 1 / (1 + Math.exp(-z));
      return Math.tanh(z);
    }}

    function setActMode(m) {{
      actMode = m;
      document.querySelectorAll('#act-tabs button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.act !== m);
      }});
      updateActSim();
    }}

    function updateActSim() {{
      const sl = document.getElementById('act-z-sl');
      if (!sl) return;
      const zVal = parseFloat(sl.value);
      document.getElementById('act-z-val').textContent = (zVal >= 0 ? '+' : '') + zVal.toFixed(1);
      const yVal = evalAct(actMode, zVal);
      document.getElementById('act-out-val').textContent = yVal.toFixed(3);

      const meta = {{
        relu: {{
          title: 'ReLU: max(0, z)',
          color: '#4285F4', yMin: -0.6, yMax: 5.2,
          note: zVal <= 0
            ? '<strong>Zona Padam (z ≤ 0):</strong> Output tepat <code>0.000</code> — neuron istirahat untuk skor minus.'
            : `<strong>Zona Aktif (z &gt; 0):</strong> Output lurus mengikuti input (<code>${{yVal.toFixed(2)}}</code>) tanpa melambat!`,
        }},
        sigmoid: {{
          title: 'Sigmoid: Kurva S (0%–100%)',
          color: '#EA4335', yMin: -0.15, yMax: 1.15,
          note: `<strong>Rentang 0 s.d. 1:</strong> Terbaca seperti peluang 2 kelas (<code>${{(yVal*100).toFixed(1)}}%</code>). Di ujung kiri/kanan kurva sangat mendatar.`,
        }},
        tanh: {{
          title: 'Tanh: Skala -1 s.d. +1',
          color: '#34A853', yMin: -1.25, yMax: 1.25,
          note: zVal < 0
            ? `<strong>Simetris di Nol (Zona Negatif):</strong> Input negatif tetap negatif (<code>${{yVal.toFixed(3)}}</code>), mendekati <code>-1</code>.`
            : zVal > 0
              ? `<strong>Simetris di Nol (Zona Positif):</strong> Input positif tetap positif (<code>+${{yVal.toFixed(3)}}</code>), mendekati <code>+1</code>.`
              : '<strong>Tepat di Nol:</strong> Saat <code>z = 0</code>, output Tanh tepat <code>0.000</code> (simetris kiri-kanan).',
        }},
      }}[actMode];

      document.getElementById('act-title').textContent = meta.title;
      document.getElementById('act-note').innerHTML = meta.note;

      const canvas = document.getElementById('act-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, W, H);

      const padL = 50, padR = 18, padT = 16, padB = 36;
      const pw = W - padL - padR, ph = H - padT - padB;
      const toX = (z) => padL + ((z + 5) / 10) * pw;
      const toY = (y) => padT + ph - ((y - meta.yMin) / (meta.yMax - meta.yMin)) * ph;

      ctx.strokeStyle = '#ECEFF1'; ctx.lineWidth = 1;
      for (let gx = -4; gx <= 4; gx += 2) {{
        const px = toX(gx); ctx.beginPath(); ctx.moveTo(px, padT); ctx.lineTo(px, padT + ph); ctx.stroke();
      }}
      ctx.strokeStyle = '#9AA0A6'; ctx.lineWidth = 1.4;
      const y0 = toY(0), x0 = toX(0);
      ctx.beginPath(); ctx.moveTo(padL, y0); ctx.lineTo(padL + pw, y0); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x0, padT); ctx.lineTo(x0, padT + ph); ctx.stroke();
      ctx.strokeRect(padL, padT, pw, ph);

      ctx.strokeStyle = meta.color; ctx.lineWidth = 3.5;
      ctx.beginPath();
      for (let i = 0; i <= 200; i++) {{
        const zv = -5 + (i / 200) * 10;
        const px = toX(zv), py = toY(evalAct(actMode, zv));
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }}
      ctx.stroke();

      const ax = toX(zVal), ay = toY(yVal);
      ctx.save(); ctx.setLineDash([4, 4]); ctx.strokeStyle = '#5F6368'; ctx.lineWidth = 1.3;
      ctx.beginPath(); ctx.moveTo(ax, padT + ph); ctx.lineTo(ax, ay); ctx.lineTo(padL, ay); ctx.stroke();
      ctx.restore();
      ctx.fillStyle = meta.color; ctx.strokeStyle = '#202124'; ctx.lineWidth = 2.2;
      ctx.beginPath(); ctx.arc(ax, ay, 7, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

      ctx.fillStyle = '#5F6368'; ctx.font = '600 11.5px Roboto Mono, monospace'; ctx.textAlign = 'center';
      for (const xv of [-5, -2.5, 0, 2.5, 5]) ctx.fillText(String(xv), toX(xv), padT + ph + 16);
      ctx.fillStyle = '#202124'; ctx.font = '700 11.5px Roboto, sans-serif';
      ctx.fillText('Input Skor Mentah (z)', padL + pw / 2, H - 5);
    }}
    updateActSim();

    // =========================================================================
    // SIMULATOR #3 (Slide 24): Mesin Softmax 5 Karakter Frozen (+ kolom e^z)
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
      const rawExps = logits.map((v) => Math.exp(v));
      const sumE = rawExps.reduce((a, b) => a + b, 0);
      const probs = rawExps.map((e) => (e / sumE) * 100);

      let bestIdx = 0;
      probs.forEach((p, i) => {{
        if (p > probs[bestIdx]) bestIdx = i;
        document.getElementById('sm-v' + i).textContent = (logits[i] >= 0 ? '+' : '') + logits[i].toFixed(1);
        document.getElementById('sm-e' + i).textContent = rawExps[i] >= 10 ? rawExps[i].toFixed(1) : rawExps[i].toFixed(2);
        document.getElementById('sm-b' + i).style.width = p.toFixed(1) + '%';
        document.getElementById('sm-p' + i).textContent = p.toFixed(1) + '%';
      }});
      const tot = probs.reduce((a, b) => a + b, 0);
      document.getElementById('sm-sum-pill').textContent = `Total = ${{tot.toFixed(1)}}%`;
      document.getElementById('sm-winner').innerHTML =
        `<strong>Prediksi AI: ${{SM_NAMES[bestIdx].toUpperCase()}} (${{probs[bestIdx].toFixed(1)}}%)</strong> — Perhatikan kolom <code>eᶻ</code>: semua positif, sehingga total porsi selalu tepat <code>100.0%</code>!`;
    }}
    updateSm();

    // =========================================================================
    // SIMULATOR #4 (Slide 32): Lembah Loss & Learning Rate (Sinkron w = -2.8!)
    // =========================================================================
    let gdMode = 'ideal';
    const GD_CFGS = {{
      small: {{
        lr: 0.03, title: 'LR Terlalu Kecil (0.03) — Lambat', cls: 'callout yellow',
        note: '<strong>Terlalu Lambat:</strong> Setelah 8 langkah, bola baru bergerak sedikit dari <code>-2.8</code> dan masih jauh dari dasar!',
      }},
      ideal: {{
        lr: 0.20, title: 'LR Ideal (0.20) — Turun Mulus', cls: 'callout green',
        note: '<strong>Berhasil!</strong> Dengan <code>LR = 0.20</code>, bola meluncur cepat dan tepat berhenti di dasar lembah <em>Loss</em>.',
      }},
      large: {{
        lr: 1.06, title: 'LR Terlalu Besar (1.06) — Memantul Liar!', cls: 'callout red',
        note: '<strong>Bahaya Divergen!</strong> Langkah terlalu lebar membuat bola melompati dasar lembah dan memantul makin tinggi!',
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
      document.getElementById('gd-end-loss').textContent = last.loss.toFixed(3);
      const noteEl = document.getElementById('gd-note');
      noteEl.className = cfg.cls;
      noteEl.innerHTML = cfg.note;

      const padL = 48, padR = 16, padT = 18, padB = 36;
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
        ctx.beginPath(); ctx.arc(px, py, idx === pts.length - 1 ? 6.5 : 4.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        if (idx === 0 || idx === pts.length - 1) {{
          ctx.fillStyle = '#202124'; ctx.font = '700 10.5px Roboto Mono'; ctx.textAlign = 'center';
          const lblX = Math.max(padL + 44, Math.min(padL + pw - 44, px));
          const lblY = idx === pts.length - 1 && py < padT + 26 ? py + 20 : Math.max(padT + 14, py - 11);
          ctx.fillText(idx === 0 ? 'Mulai (t=0)' : 'Akhir (t=8)', lblX, lblY);
        }}
      }});

      ctx.fillStyle = '#202124'; ctx.font = '700 11.5px Roboto'; ctx.textAlign = 'center';
      ctx.fillText('Nilai Bobot (w) — Target Dasar Lembah di w = 0', padL + pw / 2, H - 6);
      ctx.save(); ctx.translate(15, padT + ph / 2); ctx.rotate(-Math.PI / 2);
      ctx.fillText('Nilai Loss', 0, 0); ctx.restore();
    }}
    renderGdCanvas();

    // =========================================================================
    // SIMULATOR #5 (Slide 37): Evaluasi Kurva Loss (+ 3 KPI Live & Ciri Cepat!)
    // =========================================================================
    let ovMode = 'good';
    const OV_DATA = {{
      under: {{
        title: 'Underfitting — Model Belum Belajar',
        desc: 'Baik <strong>Train Loss (biru)</strong> maupun <strong>Val Loss (merah)</strong> sama-sama tetap tinggi &amp; datar.',
        signs: '<strong>Ciri di Grafik:</strong> Kedua garis berada di atas (&gt;1.3) dan hampir tidak turun meski epoch bertambah.',
        cls: 'callout yellow',
        act: '<strong>Solusi:</strong> Tambah jumlah epoch, periksa Learning Rate, atau perbesar jumlah neuron.',
        tr: [1.62, 1.54, 1.49, 1.45, 1.42, 1.40, 1.39, 1.38, 1.38, 1.37],
        va: [1.65, 1.58, 1.53, 1.50, 1.48, 1.46, 1.46, 1.45, 1.45, 1.45],
      }},
      good: {{
        title: 'Good Fit (Ideal) — Sehat &amp; Generalisasi Baik',
        desc: 'Kurva <strong>Train Loss (biru)</strong> dan <strong>Val Loss (merah)</strong> turun mulus bersama dan jaraknya tetap rapat.',
        signs: '<strong>Ciri di Grafik:</strong> Kedua garis turun serempak mendekati <code>0.2–0.3</code> dengan celah tipis (<code>+0.09</code>).',
        cls: 'callout green',
        act: '<strong>Status:</strong> Model sehat &amp; benar-benar paham ciri karakter Frozen!',
        tr: [1.58, 1.15, 0.84, 0.62, 0.47, 0.36, 0.29, 0.24, 0.21, 0.19],
        va: [1.60, 1.19, 0.90, 0.69, 0.54, 0.43, 0.36, 0.32, 0.29, 0.28],
      }},
      over: {{
        title: 'Overfitting — Menghafal Foto Latih!',
        desc: 'Mulai Epoch 5, <strong>Train Loss (biru)</strong> mendekati 0, <strong>tetapi Val Loss (merah) justru berbalik NAIK!</strong>',
        signs: '<strong>Ciri di Grafik:</strong> Kedua garis berpisah tajam — selisih (gap) antara Train &amp; Val melonjak menjadi <code>+1.50</code>!',
        cls: 'callout red',
        act: '<strong>Solusi (P06–P07):</strong> Data Augmentation, Dropout, EarlyStopping, &amp; Transfer Learning!',
        tr: [1.55, 1.08, 0.72, 0.45, 0.26, 0.15, 0.09, 0.05, 0.03, 0.02],
        va: [1.58, 1.16, 0.88, 0.72, 0.70, 0.79, 0.95, 1.14, 1.32, 1.52],
      }},
    }};

    function setOvMode(m) {{
      ovMode = m;
      document.querySelectorAll('#ov-btns button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.ov !== m);
      }});
      renderOvCanvas();
    }}

    function renderOvCanvas() {{
      const d = OV_DATA[ovMode];
      document.getElementById('ov-title').innerHTML = d.title;
      document.getElementById('ov-desc').innerHTML = d.desc;
      document.getElementById('ov-signs').innerHTML = d.signs;
      const actEl = document.getElementById('ov-action');
      actEl.className = d.cls;
      actEl.innerHTML = d.act;

      const lastTr = d.tr[d.tr.length - 1], lastVa = d.va[d.va.length - 1];
      const gap = lastVa - lastTr;
      document.getElementById('ov-k-tr').textContent = lastTr.toFixed(2);
      document.getElementById('ov-k-va').textContent = lastVa.toFixed(2);
      const gapEl = document.getElementById('ov-k-gap');
      gapEl.textContent = '+' + gap.toFixed(2);
      gapEl.style.color = gap > 0.5 ? '#C5221F' : gap > 0.15 ? '#B06000' : '#137333';

      const canvas = document.getElementById('ov-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, W, H);

      const padL = 48, padR = 18, padT = 20, padB = 36;
      const pw = W - padL - padR, ph = H - padT - padB;
      const toX = (ep) => padL + (ep / 9) * pw;
      const toY = (v) => padT + ph - (Math.min(1.8, v) / 1.8) * ph;

      ctx.strokeStyle = '#ECEFF1'; ctx.lineWidth = 1;
      for (const yv of [0.4, 0.8, 1.2, 1.6]) {{
        const py = toY(yv);
        ctx.beginPath(); ctx.moveTo(padL, py); ctx.lineTo(padL + pw, py); ctx.stroke();
        ctx.fillStyle = '#5F6368'; ctx.font = '500 10.5px Roboto Mono'; ctx.textAlign = 'right';
        ctx.fillText(yv.toFixed(1), padL - 6, py + 3);
      }}
      ctx.strokeStyle = '#9AA0A6'; ctx.lineWidth = 1.2; ctx.strokeRect(padL, padT, pw, ph);

      const drawLine = (arr, col) => {{
        ctx.strokeStyle = col; ctx.lineWidth = 3.2;
        ctx.beginPath();
        arr.forEach((v, i) => {{ const px = toX(i), py = toY(v); if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }});
        ctx.stroke();
        arr.forEach((v, i) => {{ ctx.fillStyle = col; ctx.beginPath(); ctx.arc(toX(i), toY(v), 4, 0, Math.PI * 2); ctx.fill(); }});
      }};
      drawLine(d.tr, '#1A73E8');
      drawLine(d.va, '#EA4335');

      ctx.fillStyle = '#1A73E8'; ctx.fillRect(padL + 12, padT + 9, 16, 4);
      ctx.fillStyle = '#202124'; ctx.font = '700 11.5px Roboto'; ctx.textAlign = 'left';
      ctx.fillText('Train Loss (Latihan)', padL + 33, padT + 14);
      ctx.fillStyle = '#EA4335'; ctx.fillRect(padL + 165, padT + 9, 16, 4);
      ctx.fillStyle = '#202124'; ctx.fillText('Val Loss (Ujian)', padL + 186, padT + 14);

      ctx.fillStyle = '#202124'; ctx.font = '700 11.5px Roboto'; ctx.textAlign = 'center';
      ctx.fillText('Putaran Training (Epoch 1 s.d. 10)', padL + pw / 2, H - 6);
    }}
    renderOvCanvas();

    // =========================================================================
    // SIMULATOR #6 (Slide 41): Kalkulator Ledakan Parameter MLP (+ Rasio 192x!)
    // =========================================================================
    let flMode = 'f224';
    const FL_MODES = {{
      mnist: {{ label: 'MNIST (28×28×1)', inputs: 28 * 28 * 1, color: '#34A853' }},
      f64:   {{ label: 'Frozen Kecil (64×64×3)', inputs: 64 * 64 * 3, color: '#FBBC04' }},
      f224:  {{ label: 'Frozen Standar (224×224×3)', inputs: 224 * 224 * 3, color: '#EA4335' }},
    }};

    function setFlMode(m) {{
      flMode = m;
      document.querySelectorAll('#fl-presets button').forEach((b) => {{
        b.classList.toggle('outline', b.dataset.fl !== m);
      }});
      updateFlSim();
    }}

    function updateFlSim() {{
      const units = parseInt(document.getElementById('fl-units').value, 10) || 128;
      document.getElementById('fl-units-v').textContent = String(units);
      const cur = FL_MODES[flMode];
      const total = cur.inputs * units;
      const ratio = Math.round(cur.inputs / FL_MODES.mnist.inputs);

      document.getElementById('fl-params').textContent = total.toLocaleString('id-ID');
      document.getElementById('fl-input-len').textContent = `${{cur.inputs.toLocaleString('id-ID')}} input × ${{units}} neuron`;
      const ratioEl = document.getElementById('fl-ratio');
      if (ratioEl) ratioEl.textContent = ratio === 1 ? 'Baseline 1×' : `${{ratio}}× MNIST!`;

      const noteEl = document.getElementById('fl-note');
      if (flMode === 'mnist') {{
        noteEl.className = 'callout green';
        noteEl.innerHTML = `<strong>Masih Ringan!</strong> Gambar kecil <code>28×28×1</code> hanya butuh <strong>${{total.toLocaleString('id-ID')}}</strong> bobot di layer 1.`;
      }} else if (flMode === 'f64') {{
        noteEl.className = 'callout yellow';
        noteEl.innerHTML = `<strong>16× Lebih Besar!</strong> Foto kecil <code>64×64×3</code> sudah butuh <strong>${{(total/1e6).toFixed(2)}} juta bobot</strong> untuk <code>{total_imgs}</code> foto Frozen.`;
      }} else {{
        noteEl.className = 'callout red';
        noteEl.innerHTML = `<strong>192× Meledak!</strong> Baru <code>{total_imgs}</code> foto Frozen, tapi 1 layer MLP saja sudah butuh <strong>${{(total/1e6).toFixed(2)}} juta bobot</strong>!`;
      }}

      const canvas = document.getElementById('fl-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, W, H);

      const keys = ['mnist', 'f64', 'f224'];
      const valsM = keys.map((k) => (FL_MODES[k].inputs * units) / 1e6);
      const maxM = Math.max(...valsM) * 1.22;
      const padL = 58, padR = 20, padT = 32, padB = 48;
      const pw = W - padL - padR, ph = H - padT - padB;

      ctx.strokeStyle = '#DADCE0'; ctx.strokeRect(padL, padT, pw, ph);
      const barW = 98;
      keys.forEach((k, i) => {{
        const cx = padL + (pw / 3) * (i + 0.5);
        const bh = Math.max(8, (valsM[i] / maxM) * ph);
        const by = padT + ph - bh;
        ctx.fillStyle = FL_MODES[k].color;
        ctx.globalAlpha = k === flMode ? 1.0 : 0.35;
        ctx.fillRect(cx - barW / 2, by, barW, bh);
        ctx.globalAlpha = 1.0;
        ctx.strokeStyle = k === flMode ? '#202124' : '#9AA0A6';
        ctx.lineWidth = k === flMode ? 2.4 : 1;
        ctx.strokeRect(cx - barW / 2, by, barW, bh);

        ctx.fillStyle = '#202124'; ctx.font = '700 12.5px Roboto Mono'; ctx.textAlign = 'center';
        ctx.fillText(`${{valsM[i].toFixed(2)}} Jt`, cx, by - 9);
        ctx.font = '700 11.5px Roboto';
        ctx.fillText(k === 'mnist' ? '28×28×1' : k === 'f64' ? '64×64×3' : '224×224×3', cx, padT + ph + 19);
      }});
      ctx.fillStyle = '#202124'; ctx.font = '700 12.5px Poppins'; ctx.textAlign = 'center';
      ctx.fillText(`Perbandingan Jumlah Bobot Layer 1 (Dense ${{units}} Neuron)`, padL + pw / 2, 19);
    }}
    updateFlSim();

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

      expandHelper('n1-presets', ['elsa', 'anna', 'olaf'], setN1Char, 'n1');
      expandHelper('act-tabs', ['relu', 'sigmoid', 'tanh'], setActMode, 'act');
      expandHelper('sm-presets', ['elsa', 'ragu', 'neg'], setSmPreset, 'sm');
      expandHelper('gd-presets', ['small', 'ideal', 'large'], setGdMode, 'gd');
      expandHelper('ov-btns', ['under', 'good', 'over'], setOvMode, 'ov');
      expandHelper('fl-presets', ['mnist', 'f64', 'f224'], setFlMode, 'fl');
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
