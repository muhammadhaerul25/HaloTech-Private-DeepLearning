"""Ekspor materials/P01/P01_understanding_images_processing_eda.html menjadi PDF berkualitas tinggi
dengan slide interaktif AI Fundamental & Question/Answer Reveal dipisah menjadi
halaman-halaman berurutan.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import sys
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools" / "legacy_p01"))
HTML_PATH = ROOT / "materials" / "P01" / "P01_understanding_images_processing_eda.html"
PDF_PATH = ROOT / "materials" / "P01" / "P01_understanding_images_processing_eda.pdf"
PPTX_PATH = ROOT / "materials" / "P01" / "P01_understanding_images_processing_eda.pptx"
TMP_HTML_PATH = ROOT / "materials" / "P01" / "_tmp_print_P01.html"
TMP_PPTX_HTML_PATH = ROOT / "materials" / "P01" / "_tmp_pptx_P01.html"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


EXPAND_QA_JS = """
() => {
  // Tag original 1..59 slide numbers before expansion
  Array.from(document.querySelectorAll('section.slide')).forEach((s, i) => {
    s.setAttribute('data-orig-num', String(i + 1));
  });

  function cloneSlideWithCanvases(slide, suffix) {
    const c = slide.cloneNode(true);
    const origCanvases = slide.querySelectorAll('canvas');
    const clonedCanvases = c.querySelectorAll('canvas');
    origCanvases.forEach((oc, idx) => {
      const cc = clonedCanvases[idx];
      if (cc && oc.width > 0 && oc.height > 0) {
        cc.width = oc.width;
        cc.height = oc.height;
        cc.getContext('2d').drawImage(oc, 0, 0);
      }
    });
    c.querySelectorAll('[id]').forEach((el) => { el.id = el.id + '-pdf-' + suffix; });
    return c;
  }

  // 1. Expand Slide 20 (AI Fundamental 1/3: 3 tabs -> rule, ml, dl)
  const ai1Tabs = document.getElementById('ai1-tabs');
  if (ai1Tabs && typeof setAi1Tab === 'function') {
    const slide19 = ai1Tabs.closest('section.slide');
    if (slide19) {
      const modes = ['rule', 'ml', 'dl'];
      const clones = modes.map((m) => {
        setAi1Tab(m);
        return cloneSlideWithCanvases(slide19, m);
      });
      clones.forEach((c) => slide19.parentNode.insertBefore(c, slide19));
      slide19.remove();
    }
  }

  // 2. Expand Slide 21 (AI Fundamental 2/3: 5 conditions -> center, shift, tilt, busy, mnist)
  const ai2Btns = document.getElementById('ai2-btns');
  if (ai2Btns && typeof setAi2Cond === 'function') {
    const slide20 = ai2Btns.closest('section.slide');
    if (slide20) {
      const conds = ['center', 'shift', 'tilt', 'busy', 'mnist'];
      const clones = conds.map((cond) => {
        setAi2Cond(cond);
        return cloneSlideWithCanvases(slide20, cond);
      });
      clones.forEach((c) => slide20.parentNode.insertBefore(c, slide20));
      slide20.remove();
    }
  }

  // 3. Expand Slide 22 (AI Fundamental 3/3: 2 scenarios -> good, bad)
  const ai3Good = document.getElementById('ai3-btn-good');
  if (ai3Good && typeof setAi3Mode === 'function') {
    const slide21 = ai3Good.closest('section.slide');
    if (slide21) {
      const modes = ['good', 'bad'];
      const clones = modes.map((m) => {
        setAi3Mode(m);
        return cloneSlideWithCanvases(slide21, m);
      });
      clones.forEach((c) => slide21.parentNode.insertBefore(c, slide21));
      slide21.remove();
    }
  }

  // 4. Expand Slide 33 (Histogram Gelap / Silau: 3 states -> Normal 0, Gelap -90, Silau +75)
  const histBtns = document.getElementById('hist-preset-btns');
  if (histBtns && typeof setHistOffset === 'function') {
    const slide33 = histBtns.closest('section.slide');
    if (slide33) {
      const offsets = [0, -90, 75];
      const clones = offsets.map((off) => {
        setHistOffset(off);
        const sl = document.getElementById('hist-offset-sl');
        if (sl) sl.setAttribute('value', String(off));
        return cloneSlideWithCanvases(slide33, 'hist-' + (off >= 0 ? 'p' + off : 'm' + Math.abs(off)));
      });
      clones.forEach((c) => slide33.parentNode.insertBefore(c, slide33));
      slide33.remove();
    }
  }

  // 5. Expand Slide 34 (Brightness & Contrast Boxplot: 4 presets -> normal, lowc, highc, dark)
  const bcBtns = document.getElementById('bc-preset-btns');
  if (bcBtns && typeof setBcPreset === 'function') {
    const slide34 = bcBtns.closest('section.slide');
    if (slide34) {
      const presets = [
        [0, 1.0, 'normal'],
        [0, 0.35, 'lowc'],
        [0, 1.60, 'highc'],
        [-65, 1.0, 'dark'],
      ];
      const clones = presets.map(([bVal, cFac, key]) => {
        setBcPreset(bVal, cFac, key);
        const bSl = document.getElementById('bc-b-sl');
        const cSl = document.getElementById('bc-c-sl');
        if (bSl) bSl.setAttribute('value', String(bVal));
        if (cSl) cSl.setAttribute('value', String(Math.round(cFac * 100)));
        return cloneSlideWithCanvases(slide34, 'bc-' + key);
      });
      clones.forEach((c) => slide34.parentNode.insertBefore(c, slide34));
      slide34.remove();
    }
  }

  // 6. Expand Q&A and Quiz slides (Question page -> Answer page)
  const slides = Array.from(document.querySelectorAll('section.slide'));
  let expandedCount = 0;

  for (const slide of slides) {
    const answers = slide.querySelectorAll('.qa-answer, .quiz-ans');
    if (answers.length === 0) continue;

    // Pastikan slide pertanyaan (halaman pertama) dalam keadaan tertutup
    answers.forEach((el) => el.classList.remove('shown'));

    // Buat slide kloningan tepat setelahnya untuk halaman jawaban terbuka
    const clone = cloneSlideWithCanvases(slide, 'ans');
    clone.classList.add('pdf-answer-slide');
    clone.querySelectorAll('.qa-answer, .quiz-ans').forEach((el) => {
      el.classList.add('shown');
    });

    slide.parentNode.insertBefore(clone, slide.nextSibling);
    expandedCount += 1;
  }

  return {
    originalSlides: slides.length,
    expandedPairs: expandedCount,
    totalPdfSlides: document.querySelectorAll('section.slide').length,
  };
}
"""

PRINT_OVERRIDE_CSS = """
@media print {
  /* Jangan paksa jawaban tampil di semua slide; ikuti class .shown */
  .qa-answer, .quiz-ans {
    display: none !important;
  }
  .qa-answer.shown, .quiz-ans.shown {
    display: block !important;
    animation: none !important;
    opacity: 1 !important;
  }

  /* Slide pertanyaan: tampilkan .vis-q, sembunyikan .vis-a */
  section.slide:not(.pdf-answer-slide) .vis-q {
    display: inline !important;
  }
  section.slide:not(.pdf-answer-slide) .vis-a {
    display: none !important;
  }

  /* Slide jawaban: sembunyikan .vis-q, tampilkan .vis-a */
  section.slide.pdf-answer-slide .vis-q {
    display: none !important;
  }
  section.slide.pdf-answer-slide .vis-a {
    display: inline !important;
  }

  /* Tampilkan indikator tab/skenario aktif pada Slide AI Fundamental & Simulator EDA di PDF */
  [id^="ai1-tabs"] .btn-ui,
  [id^="ai2-btns"] .btn-ui,
  [id^="ai3-btn-"],
  [id^="hist-preset-btns"] .btn-ui,
  [id^="bc-preset-btns"] .btn-ui {
    display: inline-flex !important;
  }
}
"""


def export_pdf() -> None:
    if not HTML_PATH.exists():
        raise FileNotFoundError(f"HTML tidak ditemukan: {HTML_PATH}")

    raw_html = HTML_PATH.read_text(encoding="utf-8")
    inject_block = (
        f"<style>{PRINT_OVERRIDE_CSS}</style>\n"
        f"<script>window.addEventListener('load', () => {{ setTimeout({EXPAND_QA_JS}, 300); }});</script>\n"
        "</body>"
    )
    print_html = raw_html.replace("</body>", inject_block, 1)
    TMP_HTML_PATH.write_text(print_html, encoding="utf-8")

    browser_bin = next((c for c in CHROME_CANDIDATES if Path(c).exists()), None)
    if browser_bin is None:
        TMP_HTML_PATH.unlink(missing_ok=True)
        raise RuntimeError("Tidak ditemukan Chrome atau Edge untuk ekspor PDF.")

    try:
        file_url = TMP_HTML_PATH.resolve().as_uri()
        cmd = [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=5000",
            f"--print-to-pdf={PDF_PATH.resolve()}",
            file_url,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finally:
        TMP_HTML_PATH.unlink(missing_ok=True)

    try:
        import pikepdf
        with pikepdf.open(PDF_PATH) as pdf:
            page_count = len(pdf.pages)
    except ImportError:
        try:
            import fitz
            with fitz.open(PDF_PATH) as doc:
                page_count = len(doc)
        except ImportError:
            raw_pdf = PDF_PATH.read_bytes()
            page_count = len(re.findall(rb"/Type\s*/Page\b", raw_pdf))
    size_mb = PDF_PATH.stat().st_size / (1024 * 1024)

    print(
        f"PDF berhasil dibuat: {PDF_PATH}\n"
        f"  Total halaman PDF: {page_count} | Ukuran: {size_mb:.2f} MB"
    )


PPTX_VIEWPORT_CSS = """
html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 1120px !important;
  height: 630px !important;
  overflow: hidden !important;
  background: #FFFFFF !important;
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}
#progress-bar, #controls, #notes-drawer, #grid-modal, #session-timer, #edge-modal {
  display: none !important;
}
#stage-wrap {
  width: 1120px !important;
  height: 630px !important;
  max-width: none !important;
  max-height: none !important;
  aspect-ratio: auto !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  margin: 0 !important;
  overflow: hidden !important;
}
section.slide {
  border-radius: 0 !important;
  box-shadow: none !important;
}
.qa-answer, .quiz-ans {
  display: none !important;
}
.qa-answer.shown, .quiz-ans.shown {
  display: block !important;
  animation: none !important;
  opacity: 1 !important;
}
section.slide:not(.pdf-answer-slide) .vis-q {
  display: inline !important;
}
section.slide:not(.pdf-answer-slide) .vis-a {
  display: none !important;
}
section.slide.pdf-answer-slide .vis-q {
  display: none !important;
}
section.slide.pdf-answer-slide .vis-a {
  display: inline !important;
}
.qa-box > .btn-ui, .quiz-item > .btn-ui, .card > .btn-ui.outline[onclick*="mc-hint"] {
  display: none !important;
}
"""


def export_pptx() -> None:
    """Ekspor materials/P01/P01_understanding_images_processing_eda.pptx langsung dari HTML
    agar 100% identik secara visual dan urutan halaman dengan HTML & PDF (80 slide 16:9 HD
    lengkap dengan speaker notes detail di setiap slide).
    """
    import asyncio
    import base64
    import io
    import json
    import socket
    import tempfile
    import time
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches
    from tornado.websocket import websocket_connect

    try:
        from build_presenter_script_P01 import SLIDE_EXPLANATIONS
    except ImportError:
        SLIDE_EXPLANATIONS = {}

    if not HTML_PATH.exists():
        raise FileNotFoundError(f"HTML tidak ditemukan: {HTML_PATH}")

    raw_html = HTML_PATH.read_text(encoding="utf-8")
    inject_block = f"<style>{PPTX_VIEWPORT_CSS}</style>\n</body>"
    TMP_PPTX_HTML_PATH.write_text(raw_html.replace("</body>", inject_block, 1), encoding="utf-8")

    browser_bin = next((c for c in CHROME_CANDIDATES if Path(c).exists()), None)
    if browser_bin is None:
        TMP_PPTX_HTML_PATH.unlink(missing_ok=True)
        raise RuntimeError("Tidak ditemukan Chrome atau Edge untuk ekspor PPTX.")

    # Pick a free TCP port for Chrome DevTools Protocol
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]

    user_data_dir = tempfile.mkdtemp(prefix="chr_pptx_p01_")
    file_url = TMP_PPTX_HTML_PATH.resolve().as_uri()
    proc = subprocess.Popen(
        [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--allow-file-access-from-files",
            f"--user-data-dir={user_data_dir}",
            f"--remote-debugging-port={port}",
            "--window-size=1120,630",
            file_url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        # Wait for DevTools HTTP endpoint
        ws_url = None
        for _ in range(40):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1.0) as resp:
                    tabs = json.loads(resp.read().decode("utf-8"))
                    for t in tabs:
                        if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                            ws_url = t["webSocketDebuggerUrl"]
                            break
                if ws_url:
                    break
            except Exception:
                pass
            time.sleep(0.15)

        if not ws_url:
            raise RuntimeError("Gagal terhubung ke Chrome DevTools Protocol untuk ekspor PPTX.")

        async def _capture_all_slides():
            conn = await websocket_connect(ws_url, max_message_size=50 * 1024 * 1024)
            msg_id = 0

            async def cdp_call(method: str, params: dict | None = None) -> dict:
                nonlocal msg_id
                msg_id += 1
                curr_id = msg_id
                payload = {"id": curr_id, "method": method, "params": params or {}}
                await conn.write_message(json.dumps(payload))
                while True:
                    raw_msg = await conn.read_message()
                    if raw_msg is None:
                        raise RuntimeError("Koneksi CDP terputus.")
                    data = json.loads(raw_msg)
                    if data.get("id") == curr_id:
                        if "error" in data:
                            raise RuntimeError(f"CDP Error ({method}): {data['error']}")
                        return data.get("result", {})

            await cdp_call("Page.enable")
            await cdp_call("Runtime.enable")
            await cdp_call(
                "Emulation.setDeviceMetricsOverride",
                {"width": 1120, "height": 630, "deviceScaleFactor": 2, "mobile": False},
            )

            # Wait for document.readyState === 'complete', fonts, and base64 thumbnails
            await asyncio.sleep(0.6)
            await cdp_call(
                "Runtime.evaluate",
                {
                    "expression": "document.fonts ? document.fonts.ready.then(() => true) : Promise.resolve(true)",
                    "awaitPromise": True,
                },
            )

            # Run EXPAND_QA_JS to expand tabs, presets, and Q&A pairs identically to PDF
            exp_res = await cdp_call(
                "Runtime.evaluate",
                {"expression": f"({EXPAND_QA_JS})()", "returnByValue": True},
            )
            info = exp_res.get("result", {}).get("value", {})
            total_slides = int(info.get("totalPdfSlides", 0))

            captured = []
            for idx in range(total_slides):
                activate_js = f"""
                (() => {{
                  const all = Array.from(document.querySelectorAll('section.slide'));
                  all.forEach((s, i) => s.classList.toggle('active', i === {idx}));
                  const cur = all[{idx}];
                  return {{
                    title: cur ? (cur.getAttribute('data-title') || '') : '',
                    notes: cur ? (cur.getAttribute('data-notes') || '') : '',
                    origNum: cur ? parseInt(cur.getAttribute('data-orig-num') || '0', 10) : 0,
                    isAns: cur ? cur.classList.contains('pdf-answer-slide') : false
                  }};
                }})()
                """
                meta_res = await cdp_call(
                    "Runtime.evaluate",
                    {"expression": activate_js, "returnByValue": True},
                )
                meta = meta_res.get("result", {}).get("value", {})
                shot = await cdp_call(
                    "Page.captureScreenshot",
                    {
                        "format": "png",
                        "clip": {"x": 0, "y": 0, "width": 1120, "height": 630, "scale": 1},
                    },
                )
                png_bytes = base64.b64decode(shot["data"])
                captured.append((meta, png_bytes))

            conn.close()
            return captured

        slides_data = asyncio.run(_capture_all_slides())

        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        blank_layout = prs.slide_layouts[6]

        for idx, (meta, png_bytes) in enumerate(slides_data, 1):
            sld = prs.slides.add_slide(blank_layout)
            sld.shapes.add_picture(
                io.BytesIO(png_bytes),
                Inches(0),
                Inches(0),
                width=Inches(13.333),
                height=Inches(7.5),
            )

            orig_num = int(meta.get("origNum", 0))
            title = meta.get("title", f"Slide {idx}")
            base_notes = meta.get("notes", "")
            bullets = SLIDE_EXPLANATIONS.get(orig_num, [])
            clean_bullets = [
                re.sub(r"\*\*([^*]+)\*\*", r"\1", re.sub(r"\*([^*]+)\*", r"\1", b))
                for b in bullets
            ]
            notes_lines = [
                f"Halaman Slide {idx:02d}/{len(slides_data)} (Acuan HTML Slide {orig_num:02d}/59) — {title}",
                "",
            ]
            if base_notes:
                notes_lines.append(f"Catatan Waktu & Instruktur: {base_notes}")
                notes_lines.append("")
            if clean_bullets:
                notes_lines.append("Penjelasan Detail Materi:")
                for b in clean_bullets:
                    notes_lines.append(f"• {b}" if not b.startswith(("•", "–")) else f"  {b}")

            sld.notes_slide.notes_text_frame.text = "\n".join(notes_lines)

        PPTX_PATH.parent.mkdir(parents=True, exist_ok=True)
        prs.save(PPTX_PATH)
        size_mb = PPTX_PATH.stat().st_size / (1024 * 1024)
        print(
            f"PPTX 100% Sinkron HTML/PDF berhasil dibuat: {PPTX_PATH}\n"
            f"  Total Slide PPTX: {len(slides_data)} | Ukuran: {size_mb:.2f} MB"
        )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
        TMP_PPTX_HTML_PATH.unlink(missing_ok=True)
        import shutil
        shutil.rmtree(user_data_dir, ignore_errors=True)


if __name__ == "__main__":
    export_pdf()
    export_pptx()

