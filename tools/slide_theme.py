"""Shared Google I/O-inspired conference slide theme for P04–P13.

Provides consistent colors, typography, layout constants, and reusable
python-pptx components without using any official Google logos or assets.
"""

from __future__ import annotations

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls
from pptx.util import Inches, Pt


# ---------------------------------------------------------------------------
# Design Constants (AGENTS.md — Google I/O-inspired conference theme)
# ---------------------------------------------------------------------------
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

MARGIN_X = Inches(0.75)
MARGIN_TOP = Inches(0.55)
CONTENT_WIDTH = SLIDE_WIDTH - 2 * MARGIN_X

# Color Palette
BLUE = RGBColor(0x42, 0x85, 0xF4)       # #4285F4
BLUE_TEXT = RGBColor(0x1A, 0x73, 0xE8)  # #1A73E8 (accent text on white)
RED = RGBColor(0xEA, 0x43, 0x35)        # #EA4335
YELLOW = RGBColor(0xFB, 0xBC, 0x04)     # #FBBC04
GREEN = RGBColor(0x34, 0xA8, 0x53)      # #34A853

DARK_BG = RGBColor(0x20, 0x21, 0x24)    # #202124
DARK_BG_ALT = RGBColor(0x0B, 0x12, 0x20)# #0B1220
LIGHT_BG = RGBColor(0xFF, 0xFF, 0xFF)   # #FFFFFF
SURFACE_BG = RGBColor(0xF8, 0xF9, 0xFA) # #F8F9FA

TINT_BLUE = RGBColor(0xE8, 0xF0, 0xFE)  # #E8F0FE
TINT_RED = RGBColor(0xFC, 0xE8, 0xE6)   # #FCE8E6
TINT_YELLOW = RGBColor(0xFE, 0xF7, 0xE0)# #FEF7E0
TINT_GREEN = RGBColor(0xE6, 0xF4, 0xEA) # #E6F4EA

TEXT_DARK = RGBColor(0x20, 0x21, 0x24)  # #202124
TEXT_LIGHT = RGBColor(0xFF, 0xFF, 0xFF) # #FFFFFF
TEXT_MUTED = RGBColor(0x5F, 0x63, 0x68) # #5F6368
BORDER_GRAY = RGBColor(0xDA, 0xDC, 0xE0)# #DADCE0

# Typography
FONT_TITLE = "Poppins"
FONT_BODY = "Roboto"
FONT_CODE = "Roboto Mono"
FONT_FALLBACK = "Arial"

SIZE_COVER_TITLE = Pt(44)
SIZE_DIVIDER_TITLE = Pt(54)
SIZE_KEYNOTE = Pt(42)
SIZE_TITLE = Pt(36)
SIZE_CARD_TITLE = Pt(24)
SIZE_BODY = Pt(24)
SIZE_SUPPORTING = Pt(20)
SIZE_KICKER = Pt(15)
SIZE_BADGE = Pt(16)
SIZE_PILL = Pt(18)
SIZE_FOOTER = Pt(14)


def create_presentation() -> Presentation:
    """Create a 16:9 widescreen Presentation."""
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    return prs


def add_blank_slide(prs: Presentation, bg_color: RGBColor = LIGHT_BG):
    """Add a blank slide with a solid background color."""
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = bg_color
    return slide


def set_shape_no_line(shape) -> None:
    """Remove outline from a shape."""
    shape.line.fill.background()


def set_shape_border(shape, color: RGBColor, width_pt: float = 1.0) -> None:
    """Set a subtle solid border on a shape."""
    shape.line.color.rgb = color
    shape.line.width = Pt(width_pt)


def add_subtle_shadow(shape) -> None:
    """Add a soft drop shadow via OOXML effectLst."""
    spPr = shape._element.spPr
    effectLst = parse_xml(
        f'<a:effectLst {nsdecls("a")}>'
        '  <a:outerShdw blurRad="101600" dist="38100" dir="5400000" algn="ctr">'
        '    <a:srgbClr val="000000"><a:alpha val="12000"/></a:srgbClr>'
        '  </a:outerShdw>'
        '</a:effectLst>'
    )
    spPr.append(effectLst)


def _format_run(
    run,
    text: str,
    font_name: str = FONT_BODY,
    size: Pt = SIZE_BODY,
    color: RGBColor = TEXT_DARK,
    bold: bool = False,
    italic: bool = False,
) -> None:
    run.text = text
    run.font.name = font_name
    run.font.size = size
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic


def add_text_box(
    slide,
    left,
    top,
    width,
    height,
    text: str,
    font_name: str = FONT_BODY,
    size: Pt = SIZE_BODY,
    color: RGBColor = TEXT_DARK,
    bold: bool = False,
    italic: bool = False,
    align: PP_ALIGN = PP_ALIGN.LEFT,
    valign: MSO_ANCHOR = MSO_ANCHOR.TOP,
    line_spacing: float = 1.15,
):
    """Add a clean text box with word wrap and proper margins."""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)

    lines = text.split("\n")
    for idx, line in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        run = p.add_run()
        _format_run(run, line, font_name, size, color, bold, italic)
    return tb


# ---------------------------------------------------------------------------
# 1. Session Cover Badge
# ---------------------------------------------------------------------------
def add_session_cover_badge(
    slide,
    text: str,
    left=MARGIN_X,
    top=Inches(1.15),
    bg_color: RGBColor = BLUE,
    text_color: RGBColor = TEXT_LIGHT,
):
    """Add a pill-shaped session badge for the cover slide."""
    width = Inches(min(max(len(text) * 0.145 + 0.7, 3.6), 8.5))
    height = Inches(0.54)
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    badge.adjustments[0] = 0.5
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    set_shape_no_line(badge)

    tf = badge.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    _format_run(run, text, FONT_TITLE, SIZE_BADGE, text_color, bold=True)
    return badge


# ---------------------------------------------------------------------------
# 2. Reusable Content Cards
# ---------------------------------------------------------------------------
def add_card(
    slide,
    left,
    top,
    width,
    height,
    title: str = "",
    body: str = "",
    bg_color: RGBColor = SURFACE_BG,
    accent_color: RGBColor | None = None,
    title_color: RGBColor = TEXT_DARK,
    body_color: RGBColor = TEXT_DARK,
    title_size: Pt = SIZE_CARD_TITLE,
    body_size: Pt = SIZE_BODY,
    border_color: RGBColor | None = BORDER_GRAY,
    shadow: bool = True,
    badge_text: str | None = None,
):
    """Add a rounded-corner content card with optional top accent bar or number badge."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.adjustments[0] = 0.08
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color is not None:
        set_shape_border(card, border_color, 1.0)
    else:
        set_shape_no_line(card)
    if shadow:
        add_subtle_shadow(card)

    pad_x = Inches(0.28)
    curr_y = top + Inches(0.26)

    if accent_color is not None:
        bar = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left + pad_x,
            top + Inches(0.18),
            Inches(0.65),
            Inches(0.10),
        )
        bar.adjustments[0] = 0.5
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_color
        set_shape_no_line(bar)
        curr_y = top + Inches(0.38)

    if badge_text is not None:
        pill_color = accent_color if accent_color is not None else BLUE
        pill_fg = TEXT_DARK if pill_color in (YELLOW, GREEN) else TEXT_LIGHT
        pill = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            left + pad_x,
            curr_y,
            Inches(0.52),
            Inches(0.52),
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = pill_color
        set_shape_no_line(pill)
        ptf = pill.text_frame
        ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
        pp = ptf.paragraphs[0]
        pp.alignment = PP_ALIGN.CENTER
        _format_run(pp.add_run(), badge_text, FONT_TITLE, Pt(22), pill_fg, bold=True)
        curr_y += Inches(0.64)

    if title:
        title_h = Inches(0.82)
        add_text_box(
            slide,
            left + pad_x,
            curr_y,
            width - 2 * pad_x,
            title_h,
            title,
            font_name=FONT_TITLE,
            size=title_size,
            color=title_color,
            bold=True,
            line_spacing=1.1,
        )
        curr_y += Inches(0.72) if len(title) < 28 else Inches(0.95)

    if body:
        rem_h = max(height - (curr_y - top) - Inches(0.2), Inches(0.5))
        add_text_box(
            slide,
            left + pad_x,
            curr_y,
            width - 2 * pad_x,
            rem_h,
            body,
            font_name=FONT_BODY,
            size=body_size,
            color=body_color,
            bold=False,
            line_spacing=1.2,
        )
    return card


# ---------------------------------------------------------------------------
# 3. Pill-shaped Terminology Tags
# ---------------------------------------------------------------------------
def add_pill_tag(
    slide,
    text: str,
    left,
    top,
    bg_color: RGBColor = TINT_BLUE,
    text_color: RGBColor = BLUE_TEXT,
    width=None,
    height=Inches(0.46),
    font_name: str = FONT_CODE,
    size: Pt = SIZE_PILL,
):
    """Add a pill-shaped tag for technical terms or labels."""
    w = width if width is not None else Inches(max(len(text) * 0.145 + 0.55, 1.5))
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, height)
    pill.adjustments[0] = 0.5
    pill.fill.solid()
    pill.fill.fore_color.rgb = bg_color
    set_shape_no_line(pill)

    tf = pill.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _format_run(p.add_run(), text, font_name, size, text_color, bold=True)
    return pill


# ---------------------------------------------------------------------------
# 4. Four-Shape Geometric Cluster
# ---------------------------------------------------------------------------
def add_four_shape_cluster(
    slide,
    left=Inches(9.6),
    top=Inches(1.1),
    scale: float = 1.0,
    on_dark: bool = False,
):
    """Add a Google-I/O-inspired cluster of 4 geometric shapes (circle, rounded square, triangle, pill)."""
    s = scale
    # 1. Blue Circle
    c = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        left + Inches(0.2 * s),
        top + Inches(0.1 * s),
        Inches(1.35 * s),
        Inches(1.35 * s),
    )
    c.fill.solid()
    c.fill.fore_color.rgb = BLUE
    set_shape_no_line(c)

    # 2. Red Rounded Square
    sq = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left + Inches(1.75 * s),
        top + Inches(0.35 * s),
        Inches(1.2 * s),
        Inches(1.2 * s),
    )
    sq.adjustments[0] = 0.25
    sq.fill.solid()
    sq.fill.fore_color.rgb = RED
    set_shape_no_line(sq)

    # 3. Yellow Triangle
    tri = slide.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE,
        left + Inches(0.35 * s),
        top + Inches(1.7 * s),
        Inches(1.3 * s),
        Inches(1.15 * s),
    )
    tri.fill.solid()
    tri.fill.fore_color.rgb = YELLOW
    set_shape_no_line(tri)

    # 4. Green Pill
    pill = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left + Inches(1.65 * s),
        top + Inches(1.85 * s),
        Inches(1.55 * s),
        Inches(0.68 * s),
    )
    pill.adjustments[0] = 0.5
    pill.fill.solid()
    pill.fill.fore_color.rgb = GREEN
    set_shape_no_line(pill)


# ---------------------------------------------------------------------------
# 5. Full-Color Section Divider
# ---------------------------------------------------------------------------
def add_section_divider(
    prs: Presentation,
    kicker: str,
    title: str,
    subtitle: str = "",
    bg_color: RGBColor = BLUE,
    slide_number: int | None = None,
    session_label: str = "P04 · Image Processing & EDA",
):
    """Create a full-color section divider slide."""
    slide = add_blank_slide(prs, bg_color)
    is_light_bg = bg_color in (YELLOW, GREEN)
    fg = TEXT_DARK if is_light_bg else TEXT_LIGHT

    # Decorative subtle geometric shapes on right (solid tonal tint, avoids footer)
    tonal_map = {
        BLUE: RGBColor(0x5C, 0x9B, 0xF6),
        RED: RGBColor(0xEF, 0x69, 0x5E),
        GREEN: RGBColor(0x57, 0xBB, 0x71),
        YELLOW: RGBColor(0xFC, 0xCA, 0x3A),
    }
    deco_col = tonal_map.get(bg_color, SURFACE_BG)

    deco1 = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(10.3), Inches(0.4), Inches(2.5), Inches(2.5)
    )
    deco1.fill.solid()
    deco1.fill.fore_color.rgb = deco_col
    set_shape_no_line(deco1)

    deco2 = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.6), Inches(3.6), Inches(2.2), Inches(2.2)
    )
    deco2.adjustments[0] = 0.25
    deco2.fill.solid()
    deco2.fill.fore_color.rgb = deco_col
    set_shape_no_line(deco2)

    add_text_box(
        slide,
        MARGIN_X,
        Inches(2.1),
        Inches(9.5),
        Inches(0.45),
        kicker.upper(),
        font_name=FONT_TITLE,
        size=SIZE_KICKER,
        color=fg,
        bold=True,
    )
    add_text_box(
        slide,
        MARGIN_X,
        Inches(2.6),
        Inches(10.0),
        Inches(1.5),
        title,
        font_name=FONT_TITLE,
        size=SIZE_DIVIDER_TITLE,
        color=fg,
        bold=True,
    )
    if subtitle:
        add_text_box(
            slide,
            MARGIN_X,
            Inches(4.1),
            Inches(9.5),
            Inches(1.8),
            subtitle,
            font_name=FONT_BODY,
            size=SIZE_BODY,
            color=fg,
            bold=False,
        )

    if slide_number is not None:
        add_footer(slide, slide_number, session_label, on_dark=not is_light_bg)
    return slide


def _set_fill_alpha(shape, alpha_val: int) -> None:
    """Set fill alpha (0..100000) on a solidFill shape."""
    solidFill = shape.fill._xPr.solidFill
    if solidFill is not None:
        srgb = solidFill.srgbClr
        if srgb is not None:
            alpha = parse_xml(f'<a:alpha {nsdecls("a")} val="{alpha_val}"/>')
            srgb.append(alpha)


# ---------------------------------------------------------------------------
# 6. Keynote-Style Slide
# ---------------------------------------------------------------------------
def add_keynote_slide(
    prs: Presentation,
    kicker: str,
    statement: str,
    subtext: str = "",
    bg_color: RGBColor = DARK_BG,
    slide_number: int | None = None,
    session_label: str = "P04 · Image Processing & EDA",
):
    """Create a high-impact keynote moment slide with one dominant statement."""
    slide = add_blank_slide(prs, bg_color)
    is_dark = bg_color in (DARK_BG, DARK_BG_ALT, BLUE, RED)
    fg = TEXT_LIGHT if is_dark else TEXT_DARK
    accent = YELLOW if is_dark else BLUE_TEXT

    # Accent bar
    bar = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN_X, Inches(2.05), Inches(1.1), Inches(0.12)
    )
    bar.adjustments[0] = 0.5
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    set_shape_no_line(bar)

    add_text_box(
        slide,
        MARGIN_X,
        Inches(2.3),
        CONTENT_WIDTH,
        Inches(0.45),
        kicker.upper(),
        font_name=FONT_TITLE,
        size=SIZE_KICKER,
        color=accent,
        bold=True,
    )
    add_text_box(
        slide,
        MARGIN_X,
        Inches(2.85),
        Inches(11.4),
        Inches(2.2),
        statement,
        font_name=FONT_TITLE,
        size=SIZE_KEYNOTE,
        color=fg,
        bold=True,
        line_spacing=1.18,
    )
    if subtext:
        add_text_box(
            slide,
            MARGIN_X,
            Inches(5.2),
            Inches(10.5),
            Inches(0.9),
            subtext,
            font_name=FONT_BODY,
            size=SIZE_BODY,
            color=RGBColor(0xBD, 0xC1, 0xC6) if is_dark else TEXT_MUTED,
        )

    add_four_shape_cluster(slide, left=Inches(10.4), top=Inches(0.6), scale=0.65, on_dark=is_dark)

    if slide_number is not None:
        add_footer(slide, slide_number, session_label, on_dark=is_dark)
    return slide


# ---------------------------------------------------------------------------
# 7. Styled Tables
# ---------------------------------------------------------------------------
def add_styled_table(
    slide,
    left,
    top,
    width,
    height,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list | None = None,
    header_color: RGBColor = BLUE,
    font_size: Pt = Pt(20),
    header_size: Pt = Pt(22),
):
    """Add a clean styled table with Google I/O palette."""
    n_rows = len(rows) + 1
    n_cols = len(headers)
    table_shape = slide.shapes.add_table(n_rows, n_cols, left, top, width, height)
    table = table_shape.table

    if col_widths is not None:
        for idx, cw in enumerate(col_widths):
            table.columns[idx].width = cw

    header_fg = TEXT_DARK if header_color in (YELLOW, GREEN) else TEXT_LIGHT

    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_color
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.14)
        tf.margin_right = Inches(0.14)
        tf.margin_top = Inches(0.08)
        tf.margin_bottom = Inches(0.08)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        _format_run(p.add_run(), h_text, FONT_TITLE, header_size, header_fg, bold=True)

    for r_idx, row in enumerate(rows, start=1):
        row_bg = LIGHT_BG if r_idx % 2 == 1 else SURFACE_BG
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.14)
            tf.margin_right = Inches(0.14)
            tf.margin_top = Inches(0.07)
            tf.margin_bottom = Inches(0.07)
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            _format_run(
                p.add_run(),
                val,
                FONT_BODY,
                font_size,
                TEXT_DARK,
                bold=(c_idx == 0),
            )
    return table_shape


# ---------------------------------------------------------------------------
# 8. Consistent Header & Footer
# ---------------------------------------------------------------------------
def add_slide_header(
    slide,
    kicker: str,
    title: str,
    kicker_color: RGBColor = BLUE_TEXT,
    title_size: Pt = SIZE_TITLE,
) -> None:
    """Add standard kicker + title header to a light content slide."""
    add_text_box(
        slide,
        MARGIN_X,
        Inches(0.38),
        CONTENT_WIDTH,
        Inches(0.35),
        kicker.upper(),
        font_name=FONT_TITLE,
        size=SIZE_KICKER,
        color=kicker_color,
        bold=True,
    )
    add_text_box(
        slide,
        MARGIN_X,
        Inches(0.72),
        CONTENT_WIDTH,
        Inches(0.72),
        title,
        font_name=FONT_TITLE,
        size=title_size,
        color=TEXT_DARK,
        bold=True,
    )


def add_slide_header_rich(
    slide,
    kicker: str,
    segments: list[tuple[str, RGBColor]],
    kicker_color: RGBColor = BLUE_TEXT,
    title_size: Pt = SIZE_TITLE,
) -> None:
    """Add standard kicker + multi-colored title header to a light content slide."""
    add_text_box(
        slide,
        MARGIN_X,
        Inches(0.38),
        CONTENT_WIDTH,
        Inches(0.35),
        kicker.upper(),
        font_name=FONT_TITLE,
        size=SIZE_KICKER,
        color=kicker_color,
        bold=True,
    )
    add_rich_title(
        slide,
        MARGIN_X,
        Inches(0.72),
        CONTENT_WIDTH,
        Inches(0.72),
        segments,
        font_name=FONT_TITLE,
        size=title_size,
    )


def add_footer(
    slide,
    slide_number: int,
    session_label: str = "P04 · Image Processing & EDA",
    on_dark: bool = False,
    fg_color: RGBColor | None = None,
) -> None:
    """Add consistent footer with session label and slide number."""
    if fg_color is not None:
        fg = fg_color
    else:
        fg = RGBColor(0xBD, 0xC1, 0xC6) if on_dark else TEXT_MUTED
    add_text_box(
        slide,
        MARGIN_X,
        Inches(7.02),
        Inches(8.0),
        Inches(0.32),
        session_label,
        font_name=FONT_BODY,
        size=SIZE_FOOTER,
        color=fg,
    )
    add_text_box(
        slide,
        Inches(11.5),
        Inches(7.02),
        Inches(1.08),
        Inches(0.32),
        f"{slide_number:02d}",
        font_name=FONT_TITLE,
        size=SIZE_FOOTER,
        color=fg,
        bold=True,
        align=PP_ALIGN.RIGHT,
    )


# ---------------------------------------------------------------------------
# Speaker Notes Helper (OOXML-verified via notes_slide)
# ---------------------------------------------------------------------------
def add_rich_title(
    slide,
    left,
    top,
    width,
    height,
    segments: list[tuple[str, RGBColor]],
    font_name: str = FONT_TITLE,
    size: Pt = SIZE_TITLE,
    align: PP_ALIGN = PP_ALIGN.LEFT,
    line_spacing: float = 1.15,
):
    """Add a title with multiple colored segments (inspired by reference decks)."""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    for text_part, color in segments:
        run = p.add_run()
        _format_run(run, text_part, font_name, size, color, bold=True)
    return tb


def add_callout_box(
    slide,
    left,
    top,
    width,
    height,
    text: str,
    accent_color: RGBColor = BLUE,
    bg_color: RGBColor = TINT_BLUE,
    text_color: RGBColor = TEXT_DARK,
    font_size: Pt = Pt(20),
    bold: bool = False,
):
    """Add a tinted callout box with a crisp left vertical accent bar (reference style)."""
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.adjustments[0] = 0.08
    box.fill.solid()
    box.fill.fore_color.rgb = bg_color
    set_shape_no_line(box)

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top + Inches(0.06), Inches(0.08), height - Inches(0.12)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent_color
    set_shape_no_line(bar)

    add_text_box(
        slide,
        left + Inches(0.20),
        top + Inches(0.08),
        width - Inches(0.30),
        height - Inches(0.16),
        text,
        font_name=FONT_BODY,
        size=font_size,
        color=text_color,
        bold=bold,
        valign=MSO_ANCHOR.MIDDLE,
        line_spacing=1.18,
    )
    return box


def add_numbered_steps(
    slide,
    left,
    top,
    width,
    steps: list[tuple[str, str, str, RGBColor]],
    row_height: float = 0.85,
):
    """Add a vertical numbered step list (01..NN) with colored badges and 1-line subtitles."""
    for idx, (num, title, subtitle, color) in enumerate(steps):
        y = top + Inches(idx * row_height)
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, y + Inches(0.04), Inches(0.46), Inches(0.42)
        )
        badge.adjustments[0] = 0.28
        badge.fill.solid()
        badge.fill.fore_color.rgb = color
        set_shape_no_line(badge)
        fg = TEXT_DARK if color in (YELLOW, GREEN) else TEXT_LIGHT
        tf = badge.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        _format_run(p.add_run(), num, FONT_TITLE, Pt(15), fg, bold=True)

        add_text_box(
            slide,
            left + Inches(0.58),
            y,
            width - Inches(0.58),
            Inches(0.34),
            title,
            font_name=FONT_TITLE,
            size=Pt(19),
            color=TEXT_DARK,
            bold=True,
        )
        if subtitle:
            add_text_box(
                slide,
                left + Inches(0.58),
                y + Inches(0.31),
                width - Inches(0.58),
                Inches(0.44),
                subtitle,
                font_name=FONT_BODY,
                size=Pt(17),
                color=TEXT_MUTED,
            )


def set_speaker_notes(slide, notes_text: str) -> None:
    """Embed speaker notes into the slide's notes_slide so PowerPoint & readers see them."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text.strip()
