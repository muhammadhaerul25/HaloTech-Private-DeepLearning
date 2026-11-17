"""Validate and render slides/P04_image_processing_eda.pptx and data/sample/.

Since LibreOffice is not installed in this environment, renders each slide
directly from the PPTX shapes, text, tables, and embedded images into PNGs
and a combined PDF under slides/assets/P04/rendered/.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
from pathlib import Path

import fitz  # PyMuPDF
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE

ROOT_DIR = Path(__file__).resolve().parent.parent
PPTX_PATH = ROOT_DIR / "materials" / "P01" / "P01_image_processing_eda.pptx"
SAMPLE_DIR = ROOT_DIR / "data" / "sample"
RENDER_DIR = ROOT_DIR / "materials" / "P01" / "assets" / "P01" / "rendered"

# Render at 1280x720 (16:9)
RENDER_W = 1280
RENDER_H = 720


def _emu_to_px(emu: int, slide_emu: int, target_px: int) -> int:
    return int(round((emu / slide_emu) * target_px))


def _rgb_tuple(rgb_color) -> tuple[int, int, int] | None:
    if rgb_color is None:
        return None
    return (rgb_color[0], rgb_color[1], rgb_color[2])


def _load_font(size_pt: float, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    px = max(int(round(size_pt * 1.25)), 10)
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, px)
    return ImageFont.load_default()


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    lines: list[str] = []
    for raw_line in text.split("\n"):
        if not raw_line:
            lines.append("")
            continue
        words = raw_line.split(" ")
        curr = ""
        for w in words:
            test = f"{curr} {w}".strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width or not curr:
                curr = test
            else:
                lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)
    return lines


def render_pptx_to_png_and_pdf(prs: Presentation) -> list[Path]:
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    sw = int(prs.slide_width)
    sh = int(prs.slide_height)
    png_paths: list[Path] = []

    for idx, slide in enumerate(prs.slides, start=1):
        bg_rgb = (255, 255, 255)
        try:
            if slide.background.fill.type is not None:
                bg_rgb = _rgb_tuple(slide.background.fill.fore_color.rgb) or (255, 255, 255)
        except Exception:
            pass

        canvas = Image.new("RGB", (RENDER_W, RENDER_H), bg_rgb)
        draw = ImageDraw.Draw(canvas)

        for shape in slide.shapes:
            x = _emu_to_px(shape.left, sw, RENDER_W)
            y = _emu_to_px(shape.top, sh, RENDER_H)
            w = _emu_to_px(shape.width, sw, RENDER_W)
            h = _emu_to_px(shape.height, sh, RENDER_H)

            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                im_bytes = shape.image.blob
                with Image.open(io.BytesIO(im_bytes)) as pim:
                    pim_rgb = pim.convert("RGB").resize((max(w, 1), max(h, 1)), Image.Resampling.BILINEAR)
                    canvas.paste(pim_rgb, (x, y))
                continue

            if shape.has_table:
                tbl = shape.table
                col_ws = [_emu_to_px(c.width, sw, RENDER_W) for c in tbl.columns]
                row_hs = [_emu_to_px(r.height, sh, RENDER_H) for r in tbl.rows]
                cy = y
                for r_i, row in enumerate(tbl.rows):
                    cx = x
                    rh = row_hs[r_i]
                    for c_i, cell in enumerate(row.cells):
                        cw = col_ws[c_i]
                        cell_bg = (248, 249, 250)
                        try:
                            if cell.fill.type is not None:
                                cell_bg = _rgb_tuple(cell.fill.fore_color.rgb) or cell_bg
                        except Exception:
                            pass
                        draw.rectangle([cx, cy, cx + cw, cy + rh], fill=cell_bg, outline=(218, 220, 224), width=1)
                        txt = cell.text_frame.text
                        font_size = 18
                        bold = False
                        txt_col = (32, 33, 36)
                        if cell.text_frame.paragraphs and cell.text_frame.paragraphs[0].runs:
                            r0 = cell.text_frame.paragraphs[0].runs[0]
                            if r0.font.size:
                                font_size = r0.font.size.pt
                            bold = bool(r0.font.bold)
                            if r0.font.color and r0.font.color.rgb:
                                txt_col = _rgb_tuple(r0.font.color.rgb) or txt_col
                        fnt = _load_font(font_size, bold=bold)
                        wrapped = _wrap_text(draw, txt, fnt, max(cw - 16, 20))
                        ty = cy + 8
                        for line in wrapped:
                            draw.text((cx + 8, ty), line, fill=txt_col, font=fnt)
                            ty += int(font_size * 1.35)
                        cx += cw
                    cy += rh
                continue

            # AutoShape / TextBox
            fill_col = None
            try:
                if shape.fill.type == 1:  # solid
                    fill_col = _rgb_tuple(shape.fill.fore_color.rgb)
            except Exception:
                pass
            if fill_col is not None:
                auto_type = None
                try:
                    auto_type = shape.auto_shape_type
                except Exception:
                    pass
                if auto_type == MSO_SHAPE.OVAL:
                    draw.ellipse([x, y, x + w, y + h], fill=fill_col)
                elif auto_type == MSO_SHAPE.ISOSCELES_TRIANGLE:
                    draw.polygon([(x + w // 2, y), (x, y + h), (x + w, y + h)], fill=fill_col)
                else:
                    draw.rounded_rectangle([x, y, x + w, y + h], radius=min(16, max(min(w, h) // 4, 4)), fill=fill_col)

            if shape.has_text_frame:
                tf = shape.text_frame
                ty = y + 6
                for p in tf.paragraphs:
                    txt = p.text
                    if not txt:
                        ty += 12
                        continue
                    font_size = 20
                    bold = False
                    txt_col = (32, 33, 36)
                    if p.runs:
                        r0 = p.runs[0]
                        if r0.font.size:
                            font_size = r0.font.size.pt
                        bold = bool(r0.font.bold)
                        if r0.font.color and r0.font.color.rgb:
                            txt_col = _rgb_tuple(r0.font.color.rgb) or txt_col
                    fnt = _load_font(font_size, bold=bold)
                    wrapped = _wrap_text(draw, txt, fnt, max(w - 14, 20))
                    for line in wrapped:
                        bbox = draw.textbbox((0, 0), line, font=fnt)
                        lw = bbox[2] - bbox[0]
                        lh = bbox[3] - bbox[1]
                        tx = x + 7
                        if p.alignment == 2:  # CENTER
                            tx = x + max((w - lw) // 2, 4)
                        elif p.alignment == 3:  # RIGHT
                            tx = x + max(w - lw - 7, 4)
                        if tf.vertical_anchor == 3 and len(tf.paragraphs) == 1 and len(wrapped) == 1:
                            ty = y + max((h - lh) // 2, 2)
                        draw.text((tx, ty), line, fill=txt_col, font=fnt)
                        ty += int(font_size * 1.38)

        out_png = RENDER_DIR / f"slide_{idx:02d}.png"
        canvas.save(out_png)
        png_paths.append(out_png)

    # Combine into PDF using PyMuPDF
    pdf_path = RENDER_DIR / "P01_preview.pdf"
    doc = fitz.open()
    for p in png_paths:
        img_doc = fitz.open(p)
        pdf_bytes = img_doc.convert_to_pdf()
        img_pdf = fitz.open("pdf", pdf_bytes)
        doc.insert_pdf(img_pdf)
    doc.save(pdf_path)
    doc.close()
    return png_paths


def validate_all() -> dict:
    assert PPTX_PATH.exists(), f"Missing PPTX: {PPTX_PATH}"
    prs = Presentation(PPTX_PATH)
    slide_count = len(prs.slides)
    assert slide_count == 22, f"Expected 22 slides, got {slide_count}"

    w_in = round(prs.slide_width.inches, 3)
    h_in = round(prs.slide_height.inches, 3)
    aspect_ratio = round(w_in / h_in, 4)
    assert abs(aspect_ratio - (16 / 9)) < 0.01, f"Not 16:9: {w_in}x{h_in}"

    total_minutes = 0
    notes_missing = []
    time_per_slide = []
    for i, slide in enumerate(prs.slides, start=1):
        if not slide.has_notes_slide or not slide.notes_slide.notes_text_frame.text.strip():
            notes_missing.append(i)
            continue
        notes_txt = slide.notes_slide.notes_text_frame.text
        m = re.search(r"Alokasi waktu:\s*(\d+)\s*menit", notes_txt)
        assert m, f"Slide {i} missing 'Alokasi waktu: X menit'"
        mins = int(m.group(1))
        total_minutes += mins
        time_per_slide.append((i, mins))

    assert not notes_missing, f"Slides missing notes: {notes_missing}"
    assert total_minutes == 120, f"Total minutes = {total_minutes}, expected 120"

    # Ensure no datetime / date / day / clock time strings appear in slides or speaker notes
    dt_pattern = re.compile(
        r"\b(?:Minggu|Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember|202[4-9]|WIB|WITA|WIT)\b|13:00|15:00|19:30|21:30",
        flags=re.IGNORECASE,
    )
    for i, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            if shape.has_text_frame:
                m_dt = dt_pattern.findall(shape.text_frame.text)
                assert not m_dt, f"Slide {i} text contains datetime token(s): {m_dt}"
        if slide.has_notes_slide:
            m_notes_dt = dt_pattern.findall(slide.notes_slide.notes_text_frame.text)
            assert not m_notes_dt, f"Slide {i} notes contain datetime token(s): {m_notes_dt}"

    # Dataset validation
    meta = pd.read_csv(SAMPLE_DIR / "metadata.csv")
    assert len(meta) == 120, f"Expected 120 rows in metadata.csv, got {len(meta)}"
    assert meta["kelas"].nunique() == 5
    assert meta["kondisi"].nunique() == 2
    assert (meta.groupby(["kelas", "kondisi"]).size() == 12).all()

    hashes = {}
    corrupted = 0
    exif6 = 0
    for rel in meta["file"]:
        fp = SAMPLE_DIR / rel
        assert fp.exists(), f"Missing sample file: {fp}"
        h = hashlib.sha256(fp.read_bytes()).hexdigest()
        hashes.setdefault(h, []).append(rel)
        try:
            with Image.open(fp) as im:
                im.verify()
        except Exception:
            corrupted += 1
            continue
        with Image.open(fp) as im:
            if im.getexif().get(274, 1) == 6:
                exif6 += 1

    dup_files = sum(len(v) for v in hashes.values() if len(v) > 1)
    assert dup_files == 2, f"Expected 2 duplicate files, got {dup_files}"
    assert corrupted == 1, f"Expected 1 corrupted file, got {corrupted}"
    assert exif6 == 2, f"Expected 2 EXIF=6 files, got {exif6}"

    pngs = render_pptx_to_png_and_pdf(prs)
    return {
        "slide_count": slide_count,
        "dimensions_in": f"{w_in}x{h_in}",
        "aspect_ratio_16_9": True,
        "notes_present_all_22": True,
        "total_minutes": total_minutes,
        "dataset_files": len(meta),
        "dataset_valid": len(meta) - corrupted,
        "dataset_corrupted": corrupted,
        "dataset_duplicates": dup_files,
        "dataset_exif6": exif6,
        "rendered_png_count": len(pngs),
        "rendered_pdf": str(RENDER_DIR / "P01_preview.pdf"),
    }


if __name__ == "__main__":
    res = validate_all()
    print(json.dumps(res, indent=2))

