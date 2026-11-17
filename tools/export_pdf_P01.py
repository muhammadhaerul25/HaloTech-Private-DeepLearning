"""Ekspor slides/P01_image_processing_eda.html menjadi PDF berkualitas tinggi
dengan slide Question & Answer Reveal dipisah menjadi 2 halaman berurutan:
- Halaman N: Pertanyaan (jawaban masih tersembunyi)
- Halaman N+1: Pertanyaan + Jawaban terbuka (muncul saat Next di PDF)

Setelah PDF selesai dibuat, otomatis disinkronkan ke folder Materials/.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
import pikepdf

from sync_materials import main as sync_materials

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "slides" / "P01_image_processing_eda.html"
PDF_PATH = ROOT / "slides" / "P01_image_processing_eda.pdf"
TMP_HTML_PATH = ROOT / "slides" / "_tmp_print_P01.html"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


EXPAND_QA_JS = """
() => {
  // 1. Expand Slide 19 (AI Fundamental 1/3: 3 tabs -> rule, ml, dl)
  const ai1Tabs = document.getElementById('ai1-tabs');
  if (ai1Tabs && typeof setAi1Tab === 'function') {
    const slide19 = ai1Tabs.closest('section.slide');
    if (slide19) {
      const modes = ['rule', 'ml', 'dl'];
      const clones = modes.map((m) => {
        setAi1Tab(m);
        const c = slide19.cloneNode(true);
        c.querySelectorAll('[id]').forEach((el) => { el.id = el.id + '-pdf-' + m; });
        return c;
      });
      clones.forEach((c) => slide19.parentNode.insertBefore(c, slide19));
      slide19.remove();
    }
  }

  // 2. Expand Slide 20 (AI Fundamental 2/3: 4 conditions -> center, shift, tilt, busy)
  const ai2Btns = document.getElementById('ai2-btns');
  if (ai2Btns && typeof setAi2Cond === 'function') {
    const slide20 = ai2Btns.closest('section.slide');
    if (slide20) {
      const conds = ['center', 'shift', 'tilt', 'busy'];
      const clones = conds.map((cond) => {
        setAi2Cond(cond);
        const c = slide20.cloneNode(true);
        c.querySelectorAll('[id]').forEach((el) => { el.id = el.id + '-pdf-' + cond; });
        return c;
      });
      clones.forEach((c) => slide20.parentNode.insertBefore(c, slide20));
      slide20.remove();
    }
  }

  // 3. Expand Slide 21 (AI Fundamental 3/3: 2 scenarios -> good, bad)
  const ai3Good = document.getElementById('ai3-btn-good');
  if (ai3Good && typeof setAi3Mode === 'function') {
    const slide21 = ai3Good.closest('section.slide');
    if (slide21) {
      const modes = ['good', 'bad'];
      const clones = modes.map((m) => {
        setAi3Mode(m);
        const c = slide21.cloneNode(true);
        c.querySelectorAll('[id]').forEach((el) => { el.id = el.id + '-pdf-' + m; });
        return c;
      });
      clones.forEach((c) => slide21.parentNode.insertBefore(c, slide21));
      slide21.remove();
    }
  }

  // 4. Expand Q&A and Quiz slides (Question page -> Answer page)
  const slides = Array.from(document.querySelectorAll('section.slide'));
  let expandedCount = 0;

  for (const slide of slides) {
    const answers = slide.querySelectorAll('.qa-answer, .quiz-ans');
    if (answers.length === 0) continue;

    // Pastikan slide pertanyaan (halaman pertama) dalam keadaan tertutup
    answers.forEach((el) => el.classList.remove('shown'));

    // Buat slide kloningan tepat setelahnya untuk halaman jawaban terbuka
    const clone = slide.cloneNode(true);
    clone.classList.add('pdf-answer-slide');
    clone.querySelectorAll('.qa-answer, .quiz-ans').forEach((el) => {
      el.classList.add('shown');
    });

    // Pastikan tidak ada duplikasi id pada elemen yang dikloning
    clone.querySelectorAll('[id]').forEach((el) => {
      el.id = el.id + '-pdf-ans';
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

  /* Tampilkan indikator tab/skenario aktif pada Slide AI Fundamental 19-21 di PDF */
  [id^="ai1-tabs"] .btn-ui,
  [id^="ai2-btns"] .btn-ui,
  [id^="ai3-btn-"] {
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
        f"<script>window.addEventListener('DOMContentLoaded', {EXPAND_QA_JS});</script>\n"
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

    pdf = pikepdf.open(PDF_PATH)
    page_count = len(pdf.pages)
    pdf.close()
    size_mb = PDF_PATH.stat().st_size / (1024 * 1024)

    print(
        f"PDF berhasil dibuat: {PDF_PATH}\n"
        f"  Total halaman PDF: {page_count} | Ukuran: {size_mb:.2f} MB"
    )

    sync_materials()


if __name__ == "__main__":
    export_pdf()

