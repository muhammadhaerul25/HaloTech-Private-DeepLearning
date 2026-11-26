"""Unified HTML-to-PDF, HTML-to-PPTX (2x Retina HD + Speaker Notes), and Presenter Script PDF Exporter.

Works generically for any session P01–P08:
- Interactive simulators register expansion hooks via `window.SLIDE_PDF_EXPANDERS`.
- Q&A (`.qa-answer`) and Quiz (`.quiz-ans`) slides automatically split into Question -> Answer pairs.
- PPTX slides are 100% visually identical to PDF pages (2240x1260 HD) with detailed Speaker Notes.
- Presenter Script PDF renders A4 portrait pages (1 base HTML slide = 1 page).
"""

from __future__ import annotations

import asyncio
import base64
import io
import json
import re
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

from .registry import SessionConfig

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_browser_bin() -> str:
    browser_bin = next((c for c in CHROME_CANDIDATES if Path(c).exists()), None)
    if browser_bin is None:
        raise RuntimeError("Tidak ditemukan Google Chrome atau Microsoft Edge untuk ekspor PDF/PPTX.")
    return browser_bin


def count_pdf_pages(pdf_path: Path) -> int:
    try:
        import pikepdf
        with pikepdf.open(pdf_path) as pdf:
            return len(pdf.pages)
    except ImportError:
        pass
    try:
        import pymupdf
        with pymupdf.open(pdf_path) as doc:
            return len(doc)
    except ImportError:
        pass
    raw_pdf = pdf_path.read_bytes()
    return len(re.findall(rb"/Type\s*/Page\b", raw_pdf))


GENERIC_EXPAND_JS = """
() => {
  // 0. Tag original 1..N slide numbers before expansion
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

  // 1. Run declarative session-registered expanders (standard contract for P02+)
  if (Array.isArray(window.SLIDE_PDF_EXPANDERS)) {
    for (const fn of window.SLIDE_PDF_EXPANDERS) {
      if (typeof fn === 'function') {
        try { fn({ cloneSlideWithCanvases }); } catch (e) { console.error(e); }
      }
    }
  }

  // 2. Backwards-compatible hooks for P01 legacy simulators (safe no-ops on other sessions)
  const ai1Tabs = document.getElementById('ai1-tabs');
  if (ai1Tabs && typeof setAi1Tab === 'function') {
    const s = ai1Tabs.closest('section.slide');
    if (s) {
      ['rule', 'ml', 'dl'].map((m) => { setAi1Tab(m); return cloneSlideWithCanvases(s, m); })
        .forEach((c) => s.parentNode.insertBefore(c, s));
      s.remove();
    }
  }
  const ai2Btns = document.getElementById('ai2-btns');
  if (ai2Btns && typeof setAi2Cond === 'function') {
    const s = ai2Btns.closest('section.slide');
    if (s) {
      ['center', 'shift', 'tilt', 'busy', 'mnist'].map((cond) => { setAi2Cond(cond); return cloneSlideWithCanvases(s, cond); })
        .forEach((c) => s.parentNode.insertBefore(c, s));
      s.remove();
    }
  }
  const ai3Good = document.getElementById('ai3-btn-good');
  if (ai3Good && typeof setAi3Mode === 'function') {
    const s = ai3Good.closest('section.slide');
    if (s) {
      ['good', 'bad'].map((m) => { setAi3Mode(m); return cloneSlideWithCanvases(s, m); })
        .forEach((c) => s.parentNode.insertBefore(c, s));
      s.remove();
    }
  }
  const histBtns = document.getElementById('hist-preset-btns');
  if (histBtns && typeof setHistOffset === 'function') {
    const s = histBtns.closest('section.slide');
    if (s) {
      [0, -90, 75].map((off) => {
        setHistOffset(off);
        const sl = document.getElementById('hist-offset-sl');
        if (sl) sl.setAttribute('value', String(off));
        return cloneSlideWithCanvases(s, 'hist-' + (off >= 0 ? 'p' + off : 'm' + Math.abs(off)));
      }).forEach((c) => s.parentNode.insertBefore(c, s));
      s.remove();
    }
  }
  const bcBtns = document.getElementById('bc-preset-btns');
  if (bcBtns && typeof setBcPreset === 'function') {
    const s = bcBtns.closest('section.slide');
    if (s) {
      [[0, 1.0, 'normal'], [0, 0.35, 'lowc'], [0, 1.60, 'highc'], [-65, 1.0, 'dark']].map(([bVal, cFac, key]) => {
        setBcPreset(bVal, cFac, key);
        const bSl = document.getElementById('bc-b-sl');
        const cSl = document.getElementById('bc-c-sl');
        if (bSl) bSl.setAttribute('value', String(bVal));
        if (cSl) cSl.setAttribute('value', String(Math.round(cFac * 100)));
        return cloneSlideWithCanvases(s, 'bc-' + key);
      }).forEach((c) => s.parentNode.insertBefore(c, s));
      s.remove();
    }
  }

  // 3. Expand Q&A and Quiz slides (Question page -> Answer page)
  const slides = Array.from(document.querySelectorAll('section.slide'));
  let expandedCount = 0;
  for (const slide of slides) {
    const answers = slide.querySelectorAll('.qa-answer, .quiz-ans');
    if (answers.length === 0) continue;

    answers.forEach((el) => el.classList.remove('shown'));
    const clone = cloneSlideWithCanvases(slide, 'ans');
    clone.classList.add('pdf-answer-slide');
    clone.querySelectorAll('.qa-answer, .quiz-ans').forEach((el) => el.classList.add('shown'));
    slide.parentNode.insertBefore(clone, slide.nextSibling);
    expandedCount += 1;
  }

  return {
    baseAfterSims: slides.length,
    expandedPairs: expandedCount,
    totalPdfSlides: document.querySelectorAll('section.slide').length,
  };
}
"""

PRINT_OVERRIDE_CSS = """
@media print {
  .qa-answer, .quiz-ans { display: none !important; }
  .qa-answer.shown, .quiz-ans.shown { display: block !important; animation: none !important; opacity: 1 !important; }
  section.slide:not(.pdf-answer-slide) .vis-q { display: inline !important; }
  section.slide:not(.pdf-answer-slide) .vis-a { display: none !important; }
  section.slide.pdf-answer-slide .vis-q { display: none !important; }
  section.slide.pdf-answer-slide .vis-a { display: inline !important; }
  /* Keep simulator state tabs visible in PDF when marked with .pdf-keep-ui or legacy IDs */
  .pdf-keep-ui .btn-ui,
  [id^="ai1-tabs"] .btn-ui,
  [id^="ai2-btns"] .btn-ui,
  [id^="ai3-btn-"],
  [id^="hist-preset-btns"] .btn-ui,
  [id^="bc-preset-btns"] .btn-ui {
    display: inline-flex !important;
  }
}
"""

PPTX_VIEWPORT_CSS = """
html, body {
  margin: 0 !important; padding: 0 !important;
  width: 1120px !important; height: 630px !important;
  overflow: hidden !important; background: #FFFFFF !important;
  -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;
}
#progress-bar, #controls, #notes-drawer, #grid-modal, #session-timer, #edge-modal, .sim-modal {
  display: none !important;
}
#stage-scaler {
  width: 1120px !important; height: 630px !important;
  margin: 0 !important; padding: 0 !important;
}
#stage-wrap {
  width: 1120px !important; height: 630px !important;
  transform: none !important;
  max-width: none !important; max-height: none !important;
  aspect-ratio: auto !important; border-radius: 0 !important;
  box-shadow: none !important; margin: 0 !important; overflow: hidden !important;
}
section.slide { border-radius: 0 !important; box-shadow: none !important; animation: none !important; transition: none !important; }
section.slide.active { opacity: 1 !important; }
.qa-answer, .quiz-ans { display: none !important; }
.qa-answer.shown, .quiz-ans.shown { display: block !important; animation: none !important; opacity: 1 !important; }
section.slide:not(.pdf-answer-slide) .vis-q { display: inline !important; }
section.slide:not(.pdf-answer-slide) .vis-a { display: none !important; }
section.slide.pdf-answer-slide .vis-q { display: none !important; }
section.slide.pdf-answer-slide .vis-a { display: inline !important; }
.qa-box > .btn-ui, .quiz-item > .btn-ui, .card > .btn-ui.outline[onclick*="toggleQA"] {
  display: none !important;
}
"""


def export_pdf(session: SessionConfig) -> dict:
    """Export 16:9 vector PDF from `session.html_path` with interactive expansion."""
    if not session.html_path.exists():
        raise FileNotFoundError(f"HTML tidak ditemukan: {session.html_path}")

    tmp_html = session.material_dir / f"_tmp_print_{session.id}.html"
    tmp_pdf = session.material_dir / f"_tmp_print_{session.id}.pdf"
    raw_html = session.html_path.read_text(encoding="utf-8")
    inject_block = (
        f"<style>{PRINT_OVERRIDE_CSS}</style>\n"
        f"<script>window.addEventListener('load', () => {{ setTimeout({GENERIC_EXPAND_JS}, 300); }});</script>\n"
        "</body>"
    )
    tmp_html.write_text(raw_html.replace("</body>", inject_block, 1), encoding="utf-8")
    browser_bin = find_browser_bin()

    try:
        cmd = [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=5000",
            f"--print-to-pdf={tmp_pdf.resolve()}",
            tmp_html.resolve().as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        session.pdf_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_pdf.replace(session.pdf_path)
    finally:
        tmp_html.unlink(missing_ok=True)
        tmp_pdf.unlink(missing_ok=True)

    pages = count_pdf_pages(session.pdf_path)
    size_mb = session.pdf_path.stat().st_size / (1024 * 1024)
    print(f"PDF berhasil dibuat: {session.pdf_path} ({pages} halaman | {size_mb:.2f} MB)")
    return {"path": str(session.pdf_path), "pages": pages, "size_mb": round(size_mb, 2)}


def export_pptx(session: SessionConfig, explanations: dict[int, list[str]] | None = None) -> dict:
    """Export 16:9 2x Retina HD PPTX directly from HTML via Chrome CDP + Speaker Notes."""
    from pptx import Presentation
    from pptx.util import Inches
    from tornado.websocket import websocket_connect

    explanations = explanations or {}
    if not session.html_path.exists():
        raise FileNotFoundError(f"HTML tidak ditemukan: {session.html_path}")

    tmp_html = session.material_dir / f"_tmp_pptx_{session.id}.html"
    raw_html = session.html_path.read_text(encoding="utf-8")
    base_slide_count = len(re.findall(r'<section class="slide\b', raw_html))
    inject_block = f"<style>{PPTX_VIEWPORT_CSS}</style>\n</body>"
    tmp_html.write_text(raw_html.replace("</body>", inject_block, 1), encoding="utf-8")

    browser_bin = find_browser_bin()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]

    user_data_dir = tempfile.mkdtemp(prefix=f"chr_pptx_{session.id.lower()}_")
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
            tmp_html.resolve().as_uri(),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
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
                await conn.write_message(json.dumps({"id": curr_id, "method": method, "params": params or {}}))
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
            await asyncio.sleep(0.6)
            await cdp_call(
                "Runtime.evaluate",
                {
                    "expression": "document.fonts ? document.fonts.ready.then(() => true) : Promise.resolve(true)",
                    "awaitPromise": True,
                },
            )
            exp_res = await cdp_call(
                "Runtime.evaluate",
                {"expression": f"({GENERIC_EXPAND_JS})()", "returnByValue": True},
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
                meta_res = await cdp_call("Runtime.evaluate", {"expression": activate_js, "returnByValue": True})
                meta = meta_res.get("result", {}).get("value", {})
                shot = await cdp_call(
                    "Page.captureScreenshot",
                    {"format": "png", "clip": {"x": 0, "y": 0, "width": 1120, "height": 630, "scale": 1}},
                )
                captured.append((meta, base64.b64decode(shot["data"])))

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
            bullets = explanations.get(orig_num, [])
            clean_bullets = [
                re.sub(r"\*\*([^*]+)\*\*", r"\1", re.sub(r"\*([^*]+)\*", r"\1", b))
                for b in bullets
            ]
            notes_lines = [
                f"Halaman Slide {idx:02d}/{len(slides_data)} (Acuan HTML Slide {orig_num:02d}/{base_slide_count}) — {title}",
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

        session.pptx_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_pptx = session.material_dir / f"_tmp_pptx_{session.id}.pptx"
        try:
            prs.save(tmp_pptx)
            tmp_pptx.replace(session.pptx_path)
        finally:
            tmp_pptx.unlink(missing_ok=True)
        size_mb = session.pptx_path.stat().st_size / (1024 * 1024)
        print(f"PPTX HD 100% Sinkron HTML/PDF berhasil dibuat: {session.pptx_path} ({len(slides_data)} slide | {size_mb:.2f} MB)")
        return {"path": str(session.pptx_path), "slides": len(slides_data), "size_mb": round(size_mb, 2)}
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
        tmp_html.unlink(missing_ok=True)
        shutil.rmtree(user_data_dir, ignore_errors=True)


def _md_inline_to_html(text: str) -> str:
    """Convert lightweight inline markdown (`**bold**`, `*italic*`, `` `code` ``) to HTML."""
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", out)
    return out


PRESENTER_OVERRIDE_CSS = """
@media print {
  @page { size: A4 portrait; margin: 11mm 12mm 11mm 12mm; }
  html, body {
    background: #FFFFFF !important; height: auto !important; overflow: visible !important;
    display: block !important; padding: 0 !important; margin: 0 !important; gap: 0 !important;
    -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;
  }
  #progress-bar, #controls, #notes-drawer, #grid-modal, #session-timer, #edge-modal, .sim-modal {
    display: none !important;
  }
  #stage-wrap {
    width: 100% !important; max-width: none !important; height: auto !important;
    aspect-ratio: auto !important; box-shadow: none !important; border-radius: 0 !important;
    background: transparent !important; overflow: visible !important; display: block !important;
  }
  .presenter-page {
    width: 100%; page-break-after: always; break-after: page;
    page-break-inside: avoid; break-inside: avoid;
    display: flex; flex-direction: column; gap: 7px; padding: 0; margin: 0;
  }
  .presenter-page:last-child { page-break-after: auto; break-after: auto; }
  .p-header {
    display: flex; align-items: center; justify-content: space-between;
    gap: 8px; border-bottom: 2px solid #1A73E8; padding-bottom: 4px;
  }
  .p-header-title {
    font-family: 'Poppins', sans-serif; font-size: 12.2pt; font-weight: 700;
    color: #202124; line-height: 1.22;
  }
  .p-header-title .p-slide-num {
    display: inline-block; background: #1A73E8; color: #FFFFFF;
    font-family: 'Roboto Mono', monospace; font-size: 9.5pt; font-weight: 700;
    padding: 2px 8px; border-radius: 5px; margin-right: 7px; vertical-align: middle;
  }
  .p-header-kicker {
    font-family: 'Roboto Mono', monospace; font-size: 7.8pt; font-weight: 700;
    color: #5F6368; background: #F1F3F4; padding: 2.5px 8px; border-radius: 999px; white-space: nowrap;
  }
  .p-slide-frame {
    width: 592px; height: 333px; margin: 0 auto;
    border: 1.5px solid #DADCE0; border-radius: 10px; overflow: hidden;
    position: relative; background: #FFFFFF; box-shadow: 0 2px 6px rgba(32,33,36,0.05); flex-shrink: 0;
  }
  .p-slide-frame > section.slide {
    position: absolute !important; top: 0 !important; left: 0 !important;
    width: 1120px !important; height: 630px !important;
    transform: scale(0.5285714) !important; transform-origin: top left !important;
    display: flex !important; opacity: 1 !important; animation: none !important;
    page-break-after: avoid !important; break-after: avoid !important;
    border-radius: 0 !important; box-shadow: none !important;
  }
  .p-slide-frame .btn-ui { display: inline-flex !important; }
  .p-slide-frame .qa-answer, .p-slide-frame .quiz-ans { display: block !important; opacity: 1 !important; animation: none !important; }
  .p-exp-box {
    background: #F8F9FA; border: 1px solid #DADCE0; border-left: 4.5px solid #1A73E8;
    border-radius: 0 9px 9px 0; padding: 9px 13px; display: flex; flex-direction: column; gap: 5px;
  }
  .p-exp-label {
    font-family: 'Poppins', sans-serif; font-size: 10pt; font-weight: 700;
    color: #1A73E8; letter-spacing: 0.2px; border-bottom: 1px solid #E8EAED; padding-bottom: 3px;
  }
  .p-exp-list { padding-left: 16px; display: flex; flex-direction: column; gap: 4px; margin: 0; }
  .p-exp-list li { font-family: 'Roboto', Arial, sans-serif; font-size: 8.95pt; line-height: 1.38; color: #202124; }
  .p-exp-list li.sub-point {
    list-style-type: none; margin-left: -6px; padding-left: 8px;
    border-left: 2px solid #C6DAFC; color: #3C4043;
  }
  .p-exp-list li code {
    font-family: 'Roboto Mono', monospace; font-size: 8.2pt;
    background: #FFFFFF; border: 1px solid #E8EAED; color: #C5221F; padding: 0.5px 4px; border-radius: 3px;
  }
}
"""


def export_presenter_script(session: SessionConfig, explanations: dict[int, list[str]]) -> dict:
    """Export A4 Portrait Presenter Script PDF (1 base HTML slide = 1 page)."""
    if not session.html_path.exists():
        raise FileNotFoundError(f"HTML tidak ditemukan: {session.html_path}")

    formatted = {
        str(k): [_md_inline_to_html(b) for b in v]
        for k, v in explanations.items()
    }
    explanations_json = json.dumps(formatted, ensure_ascii=False)
    default_kicker = f"SESSION {session.id}"

    transform_js = f"""
    const EXPLANATIONS = {explanations_json};
    window.addEventListener('load', () => {{
      setTimeout(() => {{
        const stage = document.getElementById('stage-wrap');
        const slides = Array.from(stage.querySelectorAll('section.slide'));
        slides.forEach((slide, idx) => {{
          const num = idx + 1;
          const title = slide.getAttribute('data-title') || ('Slide ' + num);
          const kickerEl = slide.querySelector('.kicker');
          const kicker = kickerEl ? kickerEl.textContent.trim() : '{default_kicker}';

          const page = document.createElement('div');
          page.className = 'presenter-page';

          const hdr = document.createElement('div');
          hdr.className = 'p-header';
          hdr.innerHTML = `
            <div class="p-header-title">
              <span class="p-slide-num">Slide ${{num}}</span>${{title}}
            </div>
            <span class="p-header-kicker">${{kicker}}</span>
          `;

          const frame = document.createElement('div');
          frame.className = 'p-slide-frame';

          const exp = document.createElement('div');
          exp.className = 'p-exp-box';
          const bullets = EXPLANATIONS[String(num)] || [];
          const liHtml = bullets.map((b) => {{
            const trimmed = b.trim();
            if (trimmed.startsWith('•') || trimmed.startsWith('–')) {{
              return `<li class="sub-point">${{trimmed}}</li>`;
            }}
            return `<li>${{trimmed}}</li>`;
          }}).join('');
          exp.innerHTML = `
            <div class="p-exp-label">Penjelasan Detail Materi — Slide ${{num}}:</div>
            <ul class="p-exp-list">${{liHtml}}</ul>
          `;

          slide.parentNode.insertBefore(page, slide);
          frame.appendChild(slide);
          page.appendChild(hdr);
          page.appendChild(frame);
          page.appendChild(exp);
        }});
      }}, 350);
    }});
    """

    tmp_html = session.material_dir / f"_tmp_presenter_script_{session.id}.html"
    tmp_pdf = session.material_dir / f"_tmp_presenter_script_{session.id}.pdf"
    raw_html = session.html_path.read_text(encoding="utf-8")
    inject_block = (
        f"<style>{PRESENTER_OVERRIDE_CSS}</style>\n"
        f"<script>{transform_js}</script>\n"
        "</body>"
    )
    tmp_html.write_text(raw_html.replace("</body>", inject_block, 1), encoding="utf-8")
    browser_bin = find_browser_bin()

    try:
        cmd = [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=4500",
            f"--print-to-pdf={tmp_pdf.resolve()}",
            tmp_html.resolve().as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        session.presenter_script_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_pdf.replace(session.presenter_script_path)
    finally:
        tmp_html.unlink(missing_ok=True)
        tmp_pdf.unlink(missing_ok=True)

    pages = count_pdf_pages(session.presenter_script_path)
    size_mb = session.presenter_script_path.stat().st_size / (1024 * 1024)
    print(f"PDF Presenter Script berhasil dibuat: {session.presenter_script_path} ({pages} halaman | {size_mb:.2f} MB)")
    return {"path": str(session.presenter_script_path), "pages": pages, "size_mb": round(size_mb, 2)}
