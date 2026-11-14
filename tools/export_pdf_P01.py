"""Ekspor slides/P01_image_processing_eda.html menjadi PDF berkualitas tinggi
dengan slide Question & Answer Reveal dipisah menjadi 2 halaman berurutan:
- Halaman N: Pertanyaan (jawaban masih tersembunyi)
- Halaman N+1: Pertanyaan + Jawaban terbuka (muncul saat Next di PDF)

Setelah PDF selesai dibuat, otomatis disinkronkan ke folder Materials/.
"""

from __future__ import annotations

from pathlib import Path
from playwright.sync_api import sync_playwright
import fitz  # PyMuPDF

from sync_materials import main as sync_materials

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "slides" / "P01_image_processing_eda.html"
PDF_PATH = ROOT / "slides" / "P01_image_processing_eda.pdf"


EXPAND_QA_JS = """
() => {
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
}
"""


def export_pdf() -> None:
    if not HTML_PATH.exists():
        raise FileNotFoundError(f"HTML tidak ditemukan: {HTML_PATH}")

    file_url = HTML_PATH.resolve().as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=2)
        page.goto(file_url, wait_until="networkidle")
        page.evaluate("() => document.fonts.ready")
        page.evaluate(
            """() => Promise.all(
                Array.from(document.images).map(img =>
                    img.complete ? Promise.resolve() : new Promise(res => {
                        img.addEventListener('load', res, { once: true });
                        img.addEventListener('error', res, { once: true });
                    })
                )
            )"""
        )

        page.add_style_tag(content=PRINT_OVERRIDE_CSS)
        stats = page.evaluate(EXPAND_QA_JS)

        page.emulate_media(media="print")
        page.pdf(
            path=str(PDF_PATH),
            width="13.333in",
            height="7.5in",
            margin={"top": "0in", "right": "0in", "bottom": "0in", "left": "0in"},
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()

    doc = fitz.open(PDF_PATH)
    page_count = len(doc)
    doc.close()
    size_mb = PDF_PATH.stat().st_size / (1024 * 1024)

    print(
        f"PDF berhasil dibuat: {PDF_PATH}\n"
        f"  Slide asli: {stats['originalSlides']} | Q&A dipisah: {stats['expandedPairs']} pasang\n"
        f"  Total halaman PDF: {page_count} | Ukuran: {size_mb:.2f} MB"
    )

    sync_materials()


if __name__ == "__main__":
    export_pdf()

