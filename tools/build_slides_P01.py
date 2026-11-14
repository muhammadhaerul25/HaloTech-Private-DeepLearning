"""Build slides/P04_image_processing_eda.pptx from data/sample/ using slide_theme.py.

Generates real data visualizations in slides/assets/P04/ and composes
exactly 22 Google I/O-inspired slides with Bahasa Indonesia speaker notes
whose time allocations sum to 120 minutes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

import slide_theme as st

SAMPLE_DIR = ROOT_DIR / "data" / "sample"
ASSETS_DIR = ROOT_DIR / "slides" / "assets" / "P04"
OUT_PPTX = ROOT_DIR / "slides" / "P04_image_processing_eda.pptx"
STATS_JSON = ASSETS_DIR / "sample_stats.json"

SESSION_LABEL = "P04 · Image Processing & EDA Foto Sendiri"


# ---------------------------------------------------------------------------
# 1. Dataset Analysis (Real Execution on data/sample/)
# ---------------------------------------------------------------------------
def analyze_sample_dataset() -> dict:
    """Inspect all 120 files in data/sample/, exclude corrupted, compute stats."""
    meta = pd.read_csv(SAMPLE_DIR / "metadata.csv")
    records = []
    corrupted_files = []
    exif_rotated_files = []
    hash_map: dict[str, list[str]] = {}

    for _, row in meta.iterrows():
        rel_path = row["file"]
        fpath = SAMPLE_DIR / rel_path
        raw_bytes = fpath.read_bytes()
        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        hash_map.setdefault(sha256, []).append(rel_path)

        # Verify integrity
        try:
            with Image.open(fpath) as im:
                im.verify()
        except Exception as exc:
            corrupted_files.append({"file": rel_path, "error": str(exc)})
            continue

        # Load with EXIF check
        with Image.open(fpath) as im:
            exif = im.getexif()
            orientation = exif.get(274, 1) if exif else 1
            if orientation == 6:
                exif_rotated_files.append(rel_path)
            im_fixed = ImageOps.exif_transpose(im).convert("RGB")
            arr = np.array(im_fixed)

        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = float(np.count_nonzero(edges)) / float(edges.size)

        records.append(
            {
                "file": rel_path,
                "kelas": row["kelas"],
                "kondisi": row["kondisi"],
                "width": int(arr.shape[1]),
                "height": int(arr.shape[0]),
                "mean_intensity": float(gray.mean()),
                "std_intensity": float(gray.std()),
                "edge_density": edge_density,
                "orientation": int(orientation),
            }
        )

    df = pd.DataFrame(records)
    duplicate_groups = [paths for paths in hash_map.values() if len(paths) > 1]

    by_cond = {}
    for cond, grp in df.groupby("kondisi"):
        by_cond[cond] = {
            "count": int(len(grp)),
            "mean_brightness": round(float(grp["mean_intensity"].mean()), 2),
            "mean_contrast": round(float(grp["std_intensity"].mean()), 2),
            "mean_edge_density": round(float(grp["edge_density"].mean()), 4),
            "min_edge_density": round(float(grp["edge_density"].min()), 4),
            "max_edge_density": round(float(grp["edge_density"].max()), 4),
        }

    stats = {
        "total_metadata_rows": int(len(meta)),
        "valid_images": int(len(df)),
        "corrupted_count": int(len(corrupted_files)),
        "corrupted_files": corrupted_files,
        "duplicate_groups": duplicate_groups,
        "duplicate_file_count": int(sum(len(g) for g in duplicate_groups)),
        "exif_orientation_6_count": int(len(exif_rotated_files)),
        "exif_orientation_6_files": exif_rotated_files,
        "classes": sorted(df["kelas"].unique().tolist()),
        "conditions": sorted(df["kondisi"].unique().tolist()),
        "by_condition": by_cond,
    }
    return stats, df


# ---------------------------------------------------------------------------
# 2. Visualization Generators (Matplotlib + OpenCV)
# ---------------------------------------------------------------------------
def _style_ax(ax, title: str = ""):
    if title:
        ax.set_title(title, fontsize=15, fontweight="bold", color="#202124", pad=10)
    ax.tick_params(colors="#5F6368", labelsize=12)


def generate_visualizations(df: pd.DataFrame, stats: dict) -> dict[str, Path]:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.family"] = "DejaVu Sans"
    paths: dict[str, Path] = {}

    # 1. Opening generic geometric character + numerical matrix hint
    p1 = ASSETS_DIR / "01_opening_character.png"
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 4.4), dpi=200)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_facecolor("#F8F9FA")
    # Friendly geometric robot mascot (NOT Disney/Mickey)
    ax1.add_patch(patches.FancyBboxPatch((2.6, 2.2), 4.8, 4.6, boxstyle="round,pad=0.3,rounding_size=0.8", facecolor="#4285F4", edgecolor="#202124", linewidth=2.5))
    ax1.add_patch(patches.Circle((3.9, 5.1), 0.65, facecolor="#FFFFFF", edgecolor="#202124", linewidth=2))
    ax1.add_patch(patches.Circle((6.1, 5.1), 0.65, facecolor="#FFFFFF", edgecolor="#202124", linewidth=2))
    ax1.add_patch(patches.Circle((3.9, 5.1), 0.28, facecolor="#202124"))
    ax1.add_patch(patches.Circle((6.1, 5.1), 0.28, facecolor="#202124"))
    ax1.add_patch(patches.FancyBboxPatch((3.7, 3.1), 2.6, 0.7, boxstyle="round,pad=0.1,rounding_size=0.3", facecolor="#FBBC04", edgecolor="#202124", linewidth=2))
    ax1.add_patch(patches.Rectangle((4.85, 7.1), 0.3, 1.0, facecolor="#202124"))
    ax1.add_patch(patches.Circle((5.0, 8.35), 0.42, facecolor="#EA4335", edgecolor="#202124", linewidth=2))
    ax1.set_title("Mata Manusia: Objek Lucu", fontsize=15, fontweight="bold", color="#202124")

    # Right: stylized pixel matrix
    sample_patch = np.array([
        [245, 245, 66, 66, 66, 66, 245, 245],
        [245, 66, 66, 255, 255, 66, 66, 245],
        [66, 66, 255, 32, 32, 255, 66, 66],
        [66, 66, 66, 66, 66, 66, 66, 66],
        [66, 251, 251, 251, 251, 251, 251, 66],
        [66, 66, 66, 66, 66, 66, 66, 66],
        [245, 66, 66, 66, 66, 66, 66, 245],
        [245, 245, 66, 66, 66, 66, 245, 245],
    ])
    ax2.imshow(sample_patch, cmap="Blues_r", vmin=0, vmax=255)
    for r in range(8):
        for c in range(8):
            val = sample_patch[r, c]
            txt_col = "#FFFFFF" if val < 130 else "#202124"
            ax2.text(c, r, str(val), ha="center", va="center", color=txt_col, fontsize=10, fontweight="bold")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_title("Komputer: Matriks Angka", fontsize=15, fontweight="bold", color="#202124")
    fig.tight_layout(pad=1.5)
    fig.savefig(p1, dpi=200, facecolor="#FFFFFF")
    plt.close(fig)
    paths["opening"] = p1

    # 2. Actual 8x8 Pixel Grid from sample image
    p2 = ASSETS_DIR / "02_pixel_grid_8x8.png"
    sample_img_path = SAMPLE_DIR / "lingkaran" / "polos" / "lingkaran_polos_01.jpg"
    with Image.open(sample_img_path) as im:
        small_8x8 = np.array(im.convert("L").resize((8, 8), Image.Resampling.BILINEAR))
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 4.4), dpi=200)
    ax_l.imshow(small_8x8, cmap="gray", vmin=0, vmax=255)
    ax_l.set_title("Tampilan Visual 8 × 8 Piksel\n(Contoh data sampel)", fontsize=14, fontweight="bold", color="#202124")
    ax_l.set_xticks(range(8))
    ax_l.set_yticks(range(8))
    ax_l.tick_params(labelsize=11)

    ax_r.imshow(small_8x8, cmap="gray", vmin=0, vmax=255)
    for r in range(8):
        for c in range(8):
            v = int(small_8x8[r, c])
            tcol = "#FFFFFF" if v < 140 else "#202124"
            ax_r.text(c, r, str(v), ha="center", va="center", color=tcol, fontsize=11, fontweight="bold")
    ax_r.set_title("Nilai Angka Asli (uint8: 0–255)", fontsize=14, fontweight="bold", color="#202124")
    ax_r.set_xticks(range(8))
    ax_r.set_yticks(range(8))
    ax_r.tick_params(labelsize=11)
    fig.tight_layout(pad=1.4)
    fig.savefig(p2, dpi=200, facecolor="#FFFFFF")
    plt.close(fig)
    paths["pixel_grid"] = p2

    # 3. Synthetic Examples (polos vs ramai)
    p3 = ASSETS_DIR / "03_synthetic_examples.png"
    classes_show = ["lingkaran", "persegi", "segitiga", "bintang", "heksagon"]
    fig, axes = plt.subplots(2, 5, figsize=(11, 4.6), dpi=180)
    for col_i, kls in enumerate(classes_show):
        for row_i, cond in enumerate(["polos", "ramai"]):
            fp = SAMPLE_DIR / kls / cond / f"{kls}_{cond}_03.jpg"
            with Image.open(fp) as im:
                arr = np.array(ImageOps.exif_transpose(im).convert("RGB"))
            axes[row_i, col_i].imshow(arr)
            axes[row_i, col_i].set_xticks([])
            axes[row_i, col_i].set_yticks([])
            if row_i == 0:
                axes[row_i, col_i].set_title(kls.capitalize(), fontsize=13, fontweight="bold", color="#202124")
            if col_i == 0:
                axes[row_i, col_i].set_ylabel(cond.upper(), fontsize=13, fontweight="bold", color="#1A73E8" if cond == "polos" else "#EA4335")
    fig.suptitle("Contoh Data Sampel Sintetis: Polos vs Ramai (256 × 256)", fontsize=15, fontweight="bold", color="#202124")
    fig.tight_layout()
    fig.savefig(p3, dpi=180, facecolor="#FFFFFF")
    plt.close(fig)
    paths["synthetic_examples"] = p3

    # 4. Grayscale vs RGB
    p4 = ASSETS_DIR / "04_grayscale_vs_rgb.png"
    fp_rgb = SAMPLE_DIR / "bintang" / "polos" / "bintang_polos_03.jpg"
    with Image.open(fp_rgb) as im:
        rgb_arr = np.array(im.convert("RGB"))
        gray_arr = np.array(im.convert("L"))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 4.2), dpi=200)
    ax1.imshow(gray_arr, cmap="gray", vmin=0, vmax=255)
    ax1.set_title(f"Grayscale\nShape: {gray_arr.shape}", fontsize=15, fontweight="bold", color="#202124")
    ax1.axis("off")
    ax2.imshow(rgb_arr)
    ax2.set_title(f"RGB (Berwarna)\nShape: {rgb_arr.shape}", fontsize=15, fontweight="bold", color="#1A73E8")
    ax2.axis("off")
    fig.tight_layout(pad=1.5)
    fig.savefig(p4, dpi=200, facecolor="#FFFFFF")
    plt.close(fig)
    paths["grayscale_vs_rgb"] = p4

    # 5. RGB Channels (Original + R + G + B)
    p5 = ASSETS_DIR / "05_rgb_channels.png"
    fp_ch = SAMPLE_DIR / "persegi" / "polos" / "persegi_polos_03.jpg"
    with Image.open(fp_ch) as im:
        ch_arr = np.array(im.convert("RGB"))
    fig, axes = plt.subplots(1, 4, figsize=(11.5, 3.3), dpi=200)
    axes[0].imshow(ch_arr)
    axes[0].set_title("Asli (RGB)", fontsize=14, fontweight="bold", color="#202124")
    titles_ch = [("Channel R (Merah)", 0, "#EA4335"), ("Channel G (Hijau)", 1, "#34A853"), ("Channel B (Biru)", 2, "#1A73E8")]
    for idx, (ttl, ch_idx, col_hex) in enumerate(titles_ch, start=1):
        axes[idx].imshow(ch_arr[:, :, ch_idx], cmap="gray", vmin=0, vmax=255)
        axes[idx].set_title(ttl, fontsize=14, fontweight="bold", color=col_hex)
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout(pad=1.2)
    fig.savefig(p5, dpi=200, facecolor="#FFFFFF")
    plt.close(fig)
    paths["rgb_channels"] = p5

    # 6. Correct vs Distorted Aspect Ratio Resize
    p6 = ASSETS_DIR / "06_resize_aspect_ratio.png"
    # Create a 320x180 (16:9) crop/canvas containing our 256x256 lingkaran to show aspect distortion clearly
    with Image.open(SAMPLE_DIR / "lingkaran" / "polos" / "lingkaran_polos_03.jpg") as im:
        sq = im.convert("RGB").resize((180, 180), Image.Resampling.BILINEAR)
    wide_canvas = Image.new("RGB", (340, 180), (240, 244, 249))
    wide_canvas.paste(sq, (80, 0))
    distorted = wide_canvas.resize((224, 224), Image.Resampling.BILINEAR)
    # Letterbox preserve aspect ratio
    ratio = min(224 / wide_canvas.width, 224 / wide_canvas.height)
    new_w, new_h = int(wide_canvas.width * ratio), int(wide_canvas.height * ratio)
    resized_keep = wide_canvas.resize((new_w, new_h), Image.Resampling.BILINEAR)
    letterbox = Image.new("RGB", (224, 224), (240, 244, 249))
    letterbox.paste(resized_keep, ((224 - new_w) // 2, (224 - new_h) // 2))

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10.8, 3.85), dpi=200)
    ax1.imshow(wide_canvas)
    ax1.set_title("Asli (340 × 180)\nLingkaran Sempurna", fontsize=13, fontweight="bold", color="#202124", pad=10)
    ax2.imshow(distorted)
    ax2.set_title("Salah: Stretch Langsung\n(224 × 224 → Lonjong!)", fontsize=13, fontweight="bold", color="#EA4335", pad=10)
    ax3.imshow(letterbox)
    ax3.set_title("Benar: Jaga Proporsi\n(Letterbox 224 × 224)", fontsize=13, fontweight="bold", color="#34A853", pad=10)
    for ax in (ax1, ax2, ax3):
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout(pad=1.6)
    fig.savefig(p6, dpi=200, facecolor="#FFFFFF", bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)
    paths["resize"] = p6

    # 7. Histogram & Brightness/Contrast Comparison
    p7 = ASSETS_DIR / "07_histogram_brightness_contrast.png"
    with Image.open(SAMPLE_DIR / "segitiga" / "polos" / "segitiga_polos_03.jpg") as im:
        g_polos = np.array(im.convert("L"))
    with Image.open(SAMPLE_DIR / "segitiga" / "ramai" / "segitiga_ramai_03.jpg") as im:
        g_ramai = np.array(im.convert("L"))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.1), dpi=200)
    ax1.hist(g_polos.ravel(), bins=32, range=(0, 255), color="#4285F4", alpha=0.85, edgecolor="#FFFFFF")
    ax1.axvline(g_polos.mean(), color="#EA4335", linestyle="--", linewidth=2.2, label=f"Mean = {g_polos.mean():.1f}")
    ax1.set_title(f"Kondisi Polos (Contoh data sampel)\nMean={g_polos.mean():.1f} | Std={g_polos.std():.1f}", fontsize=13, fontweight="bold", color="#202124")
    ax1.set_xlabel("Intensitas Piksel (0–255)", fontsize=12)
    ax1.set_ylabel("Jumlah Piksel", fontsize=12)
    ax1.legend(fontsize=11)

    ax2.hist(g_ramai.ravel(), bins=32, range=(0, 255), color="#EA4335", alpha=0.85, edgecolor="#FFFFFF")
    ax2.axvline(g_ramai.mean(), color="#202124", linestyle="--", linewidth=2.2, label=f"Mean = {g_ramai.mean():.1f}")
    ax2.set_title(f"Kondisi Ramai (Contoh data sampel)\nMean={g_ramai.mean():.1f} | Std={g_ramai.std():.1f}", fontsize=13, fontweight="bold", color="#202124")
    ax2.set_xlabel("Intensitas Piksel (0–255)", fontsize=12)
    ax2.set_ylabel("Jumlah Piksel", fontsize=12)
    ax2.legend(fontsize=11)
    fig.tight_layout(pad=1.4)
    fig.savefig(p7, dpi=200, facecolor="#FFFFFF")
    plt.close(fig)
    paths["histogram"] = p7

    # 8. Canny Edge Density Comparison (real images + aggregate boxplot/bar)
    p8 = ASSETS_DIR / "08_canny_edge_density.png"
    with Image.open(SAMPLE_DIR / "heksagon" / "polos" / "heksagon_polos_03.jpg") as im:
        img_p = np.array(im.convert("RGB"))
    with Image.open(SAMPLE_DIR / "heksagon" / "ramai" / "heksagon_ramai_03.jpg") as im:
        img_r = np.array(im.convert("RGB"))

    edge_p = cv2.Canny(cv2.cvtColor(img_p, cv2.COLOR_RGB2GRAY), 100, 200)
    edge_r = cv2.Canny(cv2.cvtColor(img_r, cv2.COLOR_RGB2GRAY), 100, 200)
    ed_p = float(np.count_nonzero(edge_p)) / edge_p.size
    ed_r = float(np.count_nonzero(edge_r)) / edge_r.size

    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.8), dpi=200)
    axes[0].imshow(edge_p, cmap="gray")
    axes[0].set_title(f"Canny: Polos\nEdge density = {ed_p:.4f}", fontsize=13, fontweight="bold", color="#1A73E8")
    axes[0].set_xticks([])
    axes[0].set_yticks([])

    axes[1].imshow(edge_r, cmap="gray")
    axes[1].set_title(f"Canny: Ramai\nEdge density = {ed_r:.4f}", fontsize=13, fontweight="bold", color="#EA4335")
    axes[1].set_xticks([])
    axes[1].set_yticks([])

    polos_vals = df[df["kondisi"] == "polos"]["edge_density"].values
    ramai_vals = df[df["kondisi"] == "ramai"]["edge_density"].values
    bp = axes[2].boxplot([polos_vals, ramai_vals], tick_labels=["Polos", "Ramai"], patch_artist=True, widths=0.5)
    bp["boxes"][0].set_facecolor("#E8F0FE")
    bp["boxes"][0].set_edgecolor("#1A73E8")
    bp["boxes"][1].set_facecolor("#FCE8E6")
    bp["boxes"][1].set_edgecolor("#EA4335")
    axes[2].set_title(
        f"Rata-rata 119 Foto Valid\nPolos: {stats['by_condition']['polos']['mean_edge_density']:.4f} | Ramai: {stats['by_condition']['ramai']['mean_edge_density']:.4f}",
        fontsize=12,
        fontweight="bold",
        color="#202124",
    )
    axes[2].set_ylabel("Edge Density", fontsize=12)
    axes[2].tick_params(labelsize=12)
    fig.tight_layout(pad=1.2)
    fig.savefig(p8, dpi=200, facecolor="#FFFFFF", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    paths["edge_density"] = p8

    # 9. EXIF Orientation=6 Trap Demo
    p9 = ASSETS_DIR / "09_exif_trap.png"
    exif_fp = SAMPLE_DIR / "persegi" / "polos" / "persegi_polos_01.jpg"
    with Image.open(exif_fp) as im:
        raw_arr = np.array(im.convert("RGB"))
        fixed_arr = np.array(ImageOps.exif_transpose(im).convert("RGB"))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 3.3), dpi=180)
    ax1.imshow(raw_arr)
    ax1.set_title("Tanpa Koreksi EXIF\n(Terputar 90°)", fontsize=12, fontweight="bold", color="#EA4335")
    ax1.axis("off")
    ax2.imshow(fixed_arr)
    ax2.set_title("Dengan exif_transpose()\n(Tegak Benar)", fontsize=12, fontweight="bold", color="#34A853")
    ax2.axis("off")
    fig.tight_layout(pad=1.0)
    fig.savefig(p9, dpi=180, facecolor="#FFFFFF")
    plt.close(fig)
    paths["exif"] = p9

    return paths


# ---------------------------------------------------------------------------
# 3. Build 22 Slides
# ---------------------------------------------------------------------------
def build_deck(stats: dict, vis: dict[str, Path]) -> None:
    prs = st.create_presentation()

    # =======================================================================
    # SLIDE 01 — COVER
    # =======================================================================
    s1 = st.add_blank_slide(prs, st.DARK_BG)
    st.add_four_shape_cluster(s1, left=Inches(9.4), top=Inches(1.1), scale=1.05, on_dark=True)
    st.add_session_cover_badge(
        s1,
        "Deep Learning Track · Session P04 · 120 menit",
        left=st.MARGIN_X,
        top=Inches(1.35),
        bg_color=st.BLUE,
        text_color=st.TEXT_LIGHT,
    )
    st.add_text_box(
        s1,
        st.MARGIN_X,
        Inches(2.25),
        Inches(8.5),
        Inches(2.0),
        "Image Processing &\nEDA Foto Sendiri",
        font_name=st.FONT_TITLE,
        size=st.SIZE_COVER_TITLE,
        color=st.TEXT_LIGHT,
        bold=True,
        line_spacing=1.15,
    )
    st.add_text_box(
        s1,
        st.MARGIN_X,
        Inches(4.55),
        Inches(8.5),
        Inches(0.9),
        "Minggu, 15 November 2026  ·  13:00–15:00 WIB\nFondasi sebelum masuk ke Neural Network & CNN",
        font_name=st.FONT_BODY,
        size=st.SIZE_BODY,
        color=RGBColor(0xBD, 0xC1, 0xC6),
        line_spacing=1.35,
    )
    st.add_footer(s1, 1, SESSION_LABEL, on_dark=True)
    st.set_speaker_notes(
        s1,
        """Alokasi waktu: 2 menit

Naskah ajar:
Selamat siang! Selamat datang di Sesi P04: Image Processing dan Exploratory Data Analysis (EDA) Foto Sendiri. Hari ini kita masuk ke fase Fondasi untuk project klasifikasi karakter Disney kita nanti.

Penjelasan konsep:
Sebelum model deep learning bisa mengenali gambar, kita harus paham dulu bagaimana komputer melihat sebuah foto dan bagaimana cara memeriksa kualitas dataset foto kita sendiri.

Transisi:
Mari kita lihat susunan acara kita selama 120 menit ke depan di slide berikutnya.""",
    )

    # =======================================================================
    # SLIDE 02 — SESSION SCHEDULE
    # =======================================================================
    s2 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s2, "AGENDA · 120 MENIT", "Alur Sesi Hari Ini")
    schedule_blocks = [
        ("00–10", "Recap", "Pertanyaan pemantik", st.BLUE, st.TINT_BLUE),
        ("10–40", "Teori", "Konsep gambar & EDA", st.RED, st.TINT_RED),
        ("40–45", "Istirahat", "Jeda singkat 5 menit", st.YELLOW, st.TINT_YELLOW),
        ("45–95", "Hands-on", "Praktik notebook 50 menit", st.GREEN, st.TINT_GREEN),
        ("95–110", "Mini-challenge", "Analisis & hipotesis awal", st.BLUE, st.TINT_BLUE),
        ("110–120", "Quiz & penutup", "5 soal evaluasi + rangkuman", st.RED, st.TINT_RED),
    ]
    for idx, (waktu, judul, ket, acc, tint) in enumerate(schedule_blocks):
        col = idx % 3
        row = idx // 3
        left = st.MARGIN_X + col * Inches(4.02)
        top = Inches(1.75) + row * Inches(2.45)
        st.add_card(
            s2,
            left,
            top,
            Inches(3.78),
            Inches(2.15),
            title=f"{waktu}  ·  {judul}",
            body=ket,
            bg_color=tint,
            accent_color=acc,
            title_size=Pt(24),
            body_size=Pt(22),
            border_color=None,
        )
    st.add_footer(s2, 2, SESSION_LABEL)
    st.set_speaker_notes(
        s2,
        """Alokasi waktu: 2 menit

Naskah ajar:
Sesi 120 menit kita dibagi menjadi 6 blok. Kita mulai dengan 10 menit recap dan pemantik, lalu 30 menit teori inti, istirahat 5 menit, kemudian 50 menit hands-on notebook, 15 menit mini-challenge, dan ditutup 10 menit quiz serta rangkuman.

Penjelasan konsep:
Format ini akan konsisten di seluruh pertemuan P4 sampai P13 agar ritme belajar terasa terstruktur.

Transisi:
Sekarang mari kita cek 3 hal utama yang akan kita kuasai hari ini.""",
    )

    # =======================================================================
    # SLIDE 03 — LEARNING OBJECTIVES (Reference style: rich cards + callout)
    # =======================================================================
    s3 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header_rich(
        s3,
        "TUJUAN BELAJAR",
        [("Apa yang Akan Kita ", st.TEXT_DARK), ("Kuasai", st.BLUE_TEXT), ("?", st.TEXT_DARK)],
    )
    objectives = [
        (
            "1",
            "Gambar adalah angka",
            "Memahami foto sebagai matriks piksel 3D (tinggi × lebar × channel warna).",
            "Bekal membaca array RGB & grayscale.",
            st.BLUE,
            st.TINT_BLUE,
        ),
        (
            "2",
            "Menyiapkan data",
            "Resize proporsional ke 224×224, normalisasi skala, dan koreksi orientasi EXIF.",
            "Input seragam agar siap masuk CNN.",
            st.GREEN,
            st.TINT_GREEN,
        ),
        (
            "3",
            "Mengenali dataset",
            "Menghitung statistik brightness, kontras, & edge density pada polos vs ramai.",
            "Deteksi file rusak, duplikat & imbalance.",
            st.RED,
            st.TINT_RED,
        ),
    ]
    for idx, (num, ttl, desc, callout, acc, tint) in enumerate(objectives):
        cx = st.MARGIN_X + idx * Inches(4.02)
        st.add_card(
            s3,
            cx,
            Inches(1.75),
            Inches(3.78),
            Inches(4.95),
            title=ttl,
            body=desc,
            bg_color=st.LIGHT_BG,
            accent_color=acc,
            badge_text=num,
            title_size=Pt(24),
            body_size=Pt(21),
            border_color=st.BORDER_GRAY,
        )
        st.add_callout_box(
            s3,
            cx + Inches(0.22),
            Inches(5.35),
            Inches(3.34),
            Inches(1.10),
            callout,
            accent_color=acc,
            bg_color=tint,
            font_size=Pt(18),
            bold=True,
        )
    st.add_footer(s3, 3, SESSION_LABEL)
    st.set_speaker_notes(
        s3,
        """Alokasi waktu: 3 menit

Naskah ajar:
Ada tiga target utama hari ini. Pertama, kita membongkar cara komputer membaca gambar sebagai tabel angka. Kedua, kita belajar menyiapkan foto agar siap masuk ke model neural network nanti. Ketiga, kita melakukan Exploratory Data Analysis atau EDA untuk mengenali karakter foto polos vs ramai.

Penjelasan konsep:
Banyak pemula langsung melompat ke training model, padahal 70% masalah akurasi sering berasal dari data yang belum dicek orientasi, ukuran, atau duplikatnya.

Transisi:
Untuk memulai, mari kita jawab satu pertanyaan mendasar.""",
    )

    # =======================================================================
    # SLIDE 04 — OPENING QUESTION
    # =======================================================================
    s4 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header_rich(
        s4,
        "PERTANYAAN PEMANTIK",
        [("Bagaimana komputer ", st.TEXT_DARK), ("'melihat'", st.BLUE_TEXT), (" Mickey?", st.TEXT_DARK)],
    )
    s4.shapes.add_picture(str(vis["opening"]), Inches(0.75), Inches(1.68), width=Inches(7.7))
    st.add_card(
        s4,
        Inches(8.65),
        Inches(1.68),
        Inches(3.93),
        Inches(4.95),
        title="Bukan Objek!",
        body="• Mata manusia melihat bentuk, telinga, dan warna.\n• Komputer hanya membaca matriks angka 0–255.",
        bg_color=st.LIGHT_BG,
        accent_color=st.BLUE,
        title_size=Pt(25),
        body_size=Pt(21),
        border_color=st.BORDER_GRAY,
    )
    st.add_callout_box(
        s4,
        Inches(8.88),
        Inches(5.15),
        Inches(3.48),
        Inches(1.22),
        "Model CNN belajar mengenali pola dari angka-angka piksel ini.",
        accent_color=st.BLUE,
        bg_color=st.TINT_BLUE,
        font_size=Pt(18),
        bold=True,
    )
    st.add_footer(s4, 4, SESSION_LABEL)
    st.set_speaker_notes(
        s4,
        """Alokasi waktu: 3 menit

Naskah ajar:
Coba bayangkan saat kita memotret karakter Mickey. Mata kita langsung mengenali bentuk kepala dan ekspresinya. Tapi bagi komputer, tidak ada konsep 'Mickey' atau 'lucu'. Yang diterima komputer hanyalah sekumpulan angka di dalam memori.

Penjelasan konsep:
Di sebelah kiri adalah ilustrasi karakter geometris generik seperti yang dilihat manusia, dan di kanan adalah representasi matriks angka yang sebenarnya dibaca komputer.

Transisi:
Mari kita masuk ke blok TEORI untuk membedah angka-angka tersebut.""",
    )

    # =======================================================================
    # SLIDE 05 — SECTION DIVIDER: TEORI
    # =======================================================================
    s5 = st.add_section_divider(
        prs,
        "BAGIAN 01 · MENIT 10–40",
        "TEORI",
        "Piksel, Shape, Channel, Preprocessing & EDA",
        bg_color=st.BLUE,
        slide_number=5,
        session_label=SESSION_LABEL,
    )
    st.set_speaker_notes(
        s5,
        """Alokasi waktu: 1 menit

Naskah ajar:
Sekarang kita masuk ke sesi Teori selama 30 menit. Fokus kita adalah memahami konsep inti secara visual sebelum menyentuh kode di notebook.

Penjelasan konsep:
Semua istilah teknis tetap kita pakai dalam bahasa Inggris seperti pixel, channel, shape, dan normalization agar terbiasa dengan dokumentasi TensorFlow/Keras.

Transisi:
Kita mulai dari unit terkecil sebuah gambar: piksel.""",
    )

    # =======================================================================
    # SLIDE 06 — PIXELS (8x8 grid)
    # =======================================================================
    s6 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header_rich(
        s6,
        "TEORI · KONSEP 01",
        [("Foto Itu Sebenarnya ", st.TEXT_DARK), ("Tabel Angka", st.BLUE_TEXT)],
    )
    s6.shapes.add_picture(str(vis["pixel_grid"]), Inches(0.75), Inches(1.65), width=Inches(8.1))
    st.add_card(
        s6,
        Inches(9.05),
        Inches(1.65),
        Inches(3.53),
        Inches(3.35),
        title="Piksel (Pixel)",
        body="• 0 = Hitam pekat\n• 255 = Putih terang\n• 1–254 = Gradasi abu-abu",
        bg_color=st.SURFACE_BG,
        accent_color=st.BLUE,
        title_size=Pt(25),
        body_size=Pt(22),
    )
    st.add_card(
        s6,
        Inches(9.05),
        Inches(5.2),
        Inches(3.53),
        Inches(1.45),
        bg_color=st.DARK_BG,
        border_color=None,
    )
    st.add_text_box(
        s6,
        Inches(9.25),
        Inches(5.42),
        Inches(3.15),
        Inches(1.05),
        "arr = np.array(img)\nprint(arr[0, 0])  # 246",
        font_name=st.FONT_CODE,
        size=Pt(18),
        color=st.TEXT_LIGHT,
        line_spacing=1.3,
    )
    st.add_footer(s6, 6, SESSION_LABEL)
    st.set_speaker_notes(
        s6,
        """Alokasi waktu: 3 menit

Naskah ajar:
Ini adalah contoh nyata dari data sampel kita yang diperkecil menjadi grid 8 kali 8 piksel. Di sebelah kiri terlihat kotak-kotak gambar, dan di sebelah kanan adalah angka sebenarnya di balik setiap kotak.

Penjelasan konsep:
Setiap kotak disebut piksel (picture element). Pada gambar grayscale standar, angka 0 berarti hitam pekat dan 255 berarti putih terang. Referensi video 3Blue1Brown menunjukkan konsep grid piksel ini dengan sangat jelas.

Transisi:
Kalau satu foto ukurannya bukan 8×8, melainkan ukuran standar model CNN, berapa total angkanya?""",
    )

    # =======================================================================
    # SLIDE 07 — IMAGE SHAPE
    # =======================================================================
    s7 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s7, "TEORI · DIMENSI ARRAY", "Setiap Foto Punya Shape")
    st.add_card(
        s7,
        st.MARGIN_X,
        Inches(1.75),
        Inches(7.3),
        Inches(2.3),
        title="224 × 224 × 3 = 150.528 angka",
        body="Height (tinggi) × Width (lebar) × Channels (warna)",
        bg_color=st.TINT_BLUE,
        accent_color=st.BLUE,
        title_size=Pt(32),
        body_size=Pt(24),
        border_color=None,
    )
    # Code snippet card (Roboto Mono)
    st.add_card(
        s7,
        st.MARGIN_X,
        Inches(4.35),
        Inches(7.3),
        Inches(2.0),
        title="Cek di Python (NumPy)",
        bg_color=st.DARK_BG,
        title_color=st.YELLOW,
        title_size=Pt(22),
        border_color=None,
    )
    st.add_text_box(
        s7,
        st.MARGIN_X + Inches(0.28),
        Inches(5.32),
        Inches(6.74),
        Inches(0.8),
        "print(img.shape)  # (224, 224, 3)",
        font_name=st.FONT_CODE,
        size=Pt(23),
        color=st.TEXT_LIGHT,
    )
    dims = [
        ("H", "Height = 224 baris", st.RED),
        ("W", "Width = 224 kolom", st.GREEN),
        ("C", "Channels = 3 (RGB)", st.BLUE),
    ]
    for i, (ltr, desc, col) in enumerate(dims):
        st.add_card(
            s7,
            Inches(8.35),
            Inches(1.75) + i * Inches(1.62),
            Inches(4.23),
            Inches(1.42),
            title=desc,
            bg_color=st.SURFACE_BG,
            accent_color=col,
            title_size=Pt(24),
        )
    st.add_footer(s7, 7, SESSION_LABEL)
    st.set_speaker_notes(
        s7,
        """Alokasi waktu: 2 menit

Naskah ajar:
Setiap foto di NumPy direpresentasikan sebagai array 3 dimensi yang disebut shape. Untuk input standar MobileNetV2, ukurannya adalah 224 kali 224 kali 3, yang berarti ada 150.528 angka dalam satu foto saja!

Penjelasan konsep:
Urutan di Python/NumPy adalah (Height, Width, Channels): tinggi dulu (baris), baru lebar (kolom), lalu jumlah channel warna. Kita cukup memanggil `img.shape` untuk memeriksanya.

Transisi:
Mengapa ada yang 1 channel dan ada yang 3 channel? Mari kita bandingkan.""",
    )

    # =======================================================================
    # SLIDE 08 — GRAYSCALE VS RGB
    # =======================================================================
    s8 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s8, "TEORI · CHANNEL", "Satu Channel atau Tiga Channel?")
    s8.shapes.add_picture(str(vis["grayscale_vs_rgb"]), Inches(0.75), Inches(1.65), width=Inches(7.75))
    st.add_card(
        s8,
        Inches(8.75),
        Inches(1.65),
        Inches(3.83),
        Inches(1.65),
        title="Grayscale: (H, W)",
        body="1 lapis angka terang-gelap.",
        bg_color=st.SURFACE_BG,
        accent_color=st.TEXT_MUTED,
        title_size=Pt(22),
        body_size=Pt(20),
    )
    st.add_card(
        s8,
        Inches(8.75),
        Inches(3.48),
        Inches(3.83),
        Inches(1.75),
        title="RGB: (H, W, 3)",
        body="3 lapis: Merah, Hijau, Biru.",
        bg_color=st.TINT_BLUE,
        accent_color=st.BLUE,
        title_size=Pt(22),
        body_size=Pt(20),
        border_color=None,
    )
    st.add_callout_box(
        s8,
        Inches(8.75),
        Inches(5.42),
        Inches(3.83),
        Inches(1.20),
        "Selalu pakai .convert('RGB') agar foto karakter Disney tetap punya warna!",
        accent_color=st.GREEN,
        bg_color=st.TINT_GREEN,
        font_size=Pt(18),
        bold=True,
    )
    st.add_footer(s8, 8, SESSION_LABEL)
    st.set_speaker_notes(
        s8,
        """Alokasi waktu: 2 menit

Naskah ajar:
Foto grayscale hanya punya satu lapisan angka sehingga shape-nya dua dimensi: (H, W). Sementara foto berwarna RGB punya tiga lapisan yang ditumpuk: (H, W, 3).

Penjelasan konsep:
Untuk membedakan karakter Disney seperti Mickey, Minnie, Donald, atau Stitch, informasi warna sangat penting! Karena itu kita selalu memastikan foto dimuat dalam format RGB 3 channel.

Transisi:
Mari kita lihat isi masing-masing dari 3 channel RGB tersebut.""",
    )

    # =======================================================================
    # SLIDE 09 — RGB CHANNELS
    # =======================================================================
    s9 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s9, "TEORI · RGB", "RGB: Tiga Channel, Tiga Informasi")
    s9.shapes.add_picture(str(vis["rgb_channels"]), Inches(0.75), Inches(1.75), width=Inches(11.83))
    st.add_card(
        s9,
        st.MARGIN_X,
        Inches(5.35),
        st.CONTENT_WIDTH,
        Inches(1.35),
        body="Setiap piksel RGB adalah kombinasi 3 angka: (Red, Green, Blue). Objek merah menyala terang di channel R, tapi gelap di G dan B.",
        bg_color=st.SURFACE_BG,
        accent_color=st.RED,
        body_size=Pt(24),
    )
    st.add_footer(s9, 9, SESSION_LABEL)
    st.set_speaker_notes(
        s9,
        """Alokasi waktu: 3 menit

Naskah ajar:
Perhatikan contoh data sampel persegi merah ini. Ketika kita pisah menjadi 3 channel terpisah, di channel Red (R) kotak perseginya terlihat putih terang (nilainya tinggi), sedangkan di channel Green (G) dan Blue (B) kotaknya gelap (nilainya rendah).

Penjelasan konsep:
Inilah cara CNN nanti membaca warna: setiap filter konvolusi melihat kombinasi nilai dari ketiga channel ini secara bersamaan.

Transisi:
Angka-angka 0–255 ini disimpan dalam tipe data tertentu. Apa bedanya uint8 dan float32?""",
    )

    # =======================================================================
    # SLIDE 10 — DATA TYPES
    # =======================================================================
    s10 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s10, "TEORI · TIPE DATA", "Kenali Tipe Data Gambar")
    st.add_pill_tag(s10, "uint8  →  0–255", st.MARGIN_X, Inches(1.68), bg_color=st.TINT_BLUE, text_color=st.BLUE_TEXT, width=Inches(3.4), height=Inches(0.52), size=Pt(21))
    st.add_card(
        s10,
        st.MARGIN_X,
        Inches(2.35),
        Inches(5.7),
        Inches(3.05),
        title="Integer 8-bit (Penyimpanan)",
        body="• Hemat memori (1 byte/nilai)\n• Format standar file JPG/PNG\n• Tidak menyimpan desimal",
        bg_color=st.SURFACE_BG,
        accent_color=st.BLUE,
        title_size=Pt(24),
        body_size=Pt(22),
    )
    st.add_pill_tag(s10, "float32  →  0.0–1.0", Inches(6.88), Inches(1.68), bg_color=st.TINT_GREEN, text_color=st.TEXT_DARK, width=Inches(3.8), height=Inches(0.52), size=Pt(21))
    st.add_card(
        s10,
        Inches(6.88),
        Inches(2.35),
        Inches(5.7),
        Inches(3.05),
        title="Floating Point (Komputasi)",
        body="• Wajib untuk operasi Neural Network\n• Mendukung gradien & bobot desimal\n• Dipakai setelah normalisasi",
        bg_color=st.TINT_GREEN,
        accent_color=st.GREEN,
        title_size=Pt(24),
        body_size=Pt(22),
        border_color=None,
    )
    st.add_card(
        s10,
        st.MARGIN_X,
        Inches(5.60),
        st.CONTENT_WIDTH,
        Inches(1.12),
        bg_color=st.DARK_BG,
        border_color=None,
    )
    st.add_text_box(
        s10,
        st.MARGIN_X + Inches(0.28),
        Inches(5.76),
        st.CONTENT_WIDTH - Inches(0.56),
        Inches(0.85),
        "arr_float = arr_uint8.astype('float32') / 255.0   # konversi aman ke 0.0–1.0",
        font_name=st.FONT_CODE,
        size=Pt(20),
        color=st.TEXT_LIGHT,
    )
    st.add_footer(s10, 10, SESSION_LABEL)
    st.set_speaker_notes(
        s10,
        """Alokasi waktu: 2 menit

Naskah ajar:
Saat foto dibuka dari disk, tipenya adalah `uint8` (unsigned integer 8-bit) dengan rentang 0 sampai 255. Tapi sebelum masuk ke neural network, kita ubah menjadi `float32` karena perhitungan bobot dan gradien membutuhkan angka desimal.

Penjelasan konsep:
Jika kita membagi `uint8` langsung tanpa mengubah ke float atau membagi dengan 255.0, hasilnya bisa terpotong menjadi integer.

Transisi:
Selain tipe data, ukuran foto dari kamera HP juga berbeda-beda. Bagaimana cara menyamakan ukurannya?""",
    )

    # =======================================================================
    # SLIDE 11 — RESIZE & ASPECT RATIO
    # =======================================================================
    s11 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s11, "TEORI · UKURAN INPUT", "Resize Tanpa Merusak Proporsi")
    s11.shapes.add_picture(str(vis["resize"]), Inches(1.55), Inches(1.62), height=Inches(3.62))
    st.add_card(
        s11,
        st.MARGIN_X,
        Inches(5.45),
        st.CONTENT_WIDTH,
        Inches(1.3),
        body="MobileNetV2 butuh input seragam 224 × 224. Menarik paksa foto persegi panjang membuat bentuk karakter gepeng (distorsi).",
        bg_color=st.TINT_YELLOW,
        accent_color=st.YELLOW,
        body_size=Pt(24),
        border_color=None,
    )
    st.add_footer(s11, 11, SESSION_LABEL)
    st.set_speaker_notes(
        s11,
        """Alokasi waktu: 3 menit

Naskah ajar:
Foto dari HP biasanya punya rasio 4:3 atau 16:9, sedangkan MobileNetV2 membutuhkan input bujur sangkar 224 kali 224. Jika langsung di-resize paksa, lingkaran menjadi lonjong! Solusinya adalah menjaga aspect ratio dengan padding (letterbox) atau center crop yang aman.

Penjelasan konsep:
Model CNN tidak bisa menerima ukuran gambar yang berubah-ubah dalam satu batch, jadi ukuran input wajib seragam.

Transisi:
Ukuran sudah seragam 224×224. Bagaimana dengan skala angkanya?""",
    )

    # =======================================================================
    # SLIDE 12 — NORMALIZATION
    # =======================================================================
    s12 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s12, "TEORI · PREPROCESSING (PREVIEW P7)", "Skala Angka Harus Konsisten")
    st.add_card(
        s12,
        st.MARGIN_X,
        Inches(1.68),
        Inches(5.7),
        Inches(3.1),
        title="0–255  →  0–1",
        body="Bagi dengan 255.0\nContoh: [0, 128, 255] → [0.0, 0.50, 1.0]",
        bg_color=st.SURFACE_BG,
        accent_color=st.BLUE,
        title_size=Pt(28),
        body_size=Pt(23),
    )
    st.add_card(
        s12,
        Inches(6.88),
        Inches(1.68),
        Inches(5.7),
        Inches(3.1),
        title="0–255  →  −1–1",
        body="MobileNetV2: (x / 127.5) − 1.0\nContoh: [0, 128, 255] → [−1.0, 0.004, 1.0]",
        bg_color=st.TINT_BLUE,
        accent_color=st.BLUE,
        title_size=Pt(28),
        body_size=Pt(23),
        border_color=None,
    )
    st.add_pill_tag(s12, "PREVIEW P7", st.MARGIN_X, Inches(5.05), bg_color=st.TINT_YELLOW, text_color=st.TEXT_DARK, width=Inches(1.85), height=Inches(0.5), size=Pt(18))
    st.add_card(
        s12,
        st.MARGIN_X + Inches(2.05),
        Inches(5.02),
        st.CONTENT_WIDTH - Inches(2.05),
        Inches(1.42),
        bg_color=st.DARK_BG,
        border_color=None,
    )
    st.add_text_box(
        s12,
        st.MARGIN_X + Inches(2.3),
        Inches(5.2),
        st.CONTENT_WIDTH - Inches(2.5),
        Inches(1.1),
        "from tensorflow.keras.applications.mobilenet_v2 import preprocess_input\nx_norm = preprocess_input(x_uint8)  # skala sekitar -1 s.d. 1",
        font_name=st.FONT_CODE,
        size=Pt(19),
        color=st.TEXT_LIGHT,
        line_spacing=1.25,
    )
    st.add_footer(s12, 12, SESSION_LABEL)
    st.set_speaker_notes(
        s12,
        """Alokasi waktu: 3 menit

Naskah ajar:
Angka 0–255 terlalu besar untuk pelatihan neural network yang stabil, jadi kita lakukan normalisasi. Ada dua skala yang sering dipakai: 0 sampai 1, atau −1 sampai 1. Khusus untuk MobileNetV2 yang akan kita pakai di P7 nanti, fungsi `preprocess_input` mengubah skala piksel menjadi kira-kira −1 sampai 1.

Penjelasan konsep:
Ini adalah preview untuk P7. Kita tidak perlu menghafal rumusnya, cukup panggil `preprocess_input` bawaan MobileNetV2 agar sesuai dengan bobot ImageNet-nya.

Transisi:
Ada satu aturan emas tentang preprocessing ini yang wajib diingat selamanya.""",
    )

    # =======================================================================
    # SLIDE 13 — KEYNOTE MOMENT
    # =======================================================================
    s13 = st.add_keynote_slide(
        prs,
        "ATURAN EMAS PREPROCESSING",
        "Preprocessing saat training =\npreprocessing saat prediksi.",
        "Salah skala antara training dan inferensi akan membuat akurasi model anjlok.",
        bg_color=st.DARK_BG,
        slide_number=13,
        session_label=SESSION_LABEL,
    )
    st.set_speaker_notes(
        s13,
        """Alokasi waktu: 1 menit

Naskah ajar:
Ingat satu kalimat ini: Preprocessing saat training harus sama persis dengan preprocessing saat prediksi! Jika saat training model menerima angka −1 sampai 1, lalu saat demo kita memberi angka 0 sampai 255, model akan kebingungan dan menebak acak.

Penjelasan konsep:
Ini adalah salah satu bug paling sering terjadi di dunia nyata saat deployment model computer vision.

Transisi:
Sekarang kita beralih dari menyiapkan satu foto ke memahami keseluruhan dataset foto melalui EDA.""",
    )

    # =======================================================================
    # SLIDE 14 — HISTOGRAM
    # =======================================================================
    s14 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s14, "TEORI · STATISTIK CITRA", "Histogram: Membaca Karakter Foto")
    s14.shapes.add_picture(str(vis["histogram"]), Inches(2.1), Inches(1.60), height=Inches(3.65))
    st.add_card(
        s14,
        st.MARGIN_X,
        Inches(5.45),
        st.CONTENT_WIDTH,
        Inches(1.25),
        body="Mean (rata-rata) mengukur brightness (terang/gelap). Standar deviasi (std) mengukur contrast (sebaran gelap-terang).",
        bg_color=st.SURFACE_BG,
        accent_color=st.BLUE,
        body_size=Pt(24),
    )
    st.add_footer(s14, 14, SESSION_LABEL)
    st.set_speaker_notes(
        s14,
        """Alokasi waktu: 3 menit

Naskah ajar:
Histogram menunjukkan seberapa banyak piksel pada setiap tingkat kecerahan 0 sampai 255. Pada contoh data sampel kita: gambar polos punya puncak sempit di area terang (background seragam), sedangkan gambar ramai sebarannya jauh lebih melebar karena banyak objek dan warna latar.

Penjelasan konsep:
Dari histogram kita menghitung dua angka ringkas: Mean intensitas untuk brightness, dan Simpangan Baku (std) untuk kontras.

Transisi:
Selain histogram, apa saja yang perlu kita cek saat melakukan EDA dataset?""",
    )

    # =======================================================================
    # SLIDE 15 — EXPLORATORY DATA ANALYSIS (3-column table + imbalance callout)
    # =======================================================================
    s15 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s15, "TEORI · EDA DESKRIPTIF", "Kenali Data Sebelum Modeling")
    st.add_styled_table(
        s15,
        st.MARGIN_X,
        Inches(1.58),
        st.CONTENT_WIDTH,
        Inches(3.8),
        headers=["Ukuran", "Yang Dilihat", "Mengapa Penting"],
        rows=[
            ["Distribusi", "Jumlah per kelas × kondisi", "Deteksi class imbalance"],
            ["Resolusi & ukuran", "Dimensi (W×H) & MB file", "Konsistensi input model"],
            ["Brightness & contrast", "Rata-rata & simpangan baku", "Karakteristik pencahayaan"],
            ["Edge density & entropy", "Rasio tepi & keragaman piksel", "Kompleksitas background"],
        ],
        col_widths=[Inches(3.3), Inches(4.4), Inches(4.13)],
        header_color=st.BLUE,
        font_size=Pt(21),
        header_size=Pt(22),
    )
    st.add_callout_box(
        s15,
        st.MARGIN_X,
        Inches(5.58),
        st.CONTENT_WIDTH,
        Inches(1.18),
        "Class imbalance: jika 1 karakter punya 100 foto tapi karakter lain hanya 15 foto, model cenderung bias ke kelas mayoritas. EDA membantu menemukan ini sebelum melatih model (skenario S1 & S2).",
        accent_color=st.RED,
        bg_color=st.TINT_RED,
        font_size=Pt(19),
    )
    st.add_footer(s15, 15, SESSION_LABEL)
    st.set_speaker_notes(
        s15,
        """Alokasi waktu: 3 menit

Naskah ajar:
EDA itu ibarat memeriksa bahan masakan sebelum mulai memasak. Ada 4 hal utama yang kita periksa: distribusi jumlah foto (untuk mendeteksi class imbalance), resolusi gambar, karakteristik pencahayaan (brightness & contrast), dan kompleksitas latar belakang (edge density).

Penjelasan konsep:
Class imbalance terjadi jika satu karakter punya 100 foto sementara karakter lain hanya 15 foto; model bisa cenderung menebak kelas yang jumlahnya banyak.

Transisi:
Mari kita lihat lebih dekat ukuran keempat: bagaimana cara mengukur 'keramaian' background?""",
    )

    # =======================================================================
    # SLIDE 16 — EDGE DENSITY
    # =======================================================================
    s16 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s16, "TEORI · KOMPLEKSITAS VISUAL", "Seberapa Ramai Background-nya?")
    s16.shapes.add_picture(str(vis["edge_density"]), Inches(0.85), Inches(1.58), width=Inches(11.6))
    polos_ed = stats["by_condition"]["polos"]["mean_edge_density"]
    ramai_ed = stats["by_condition"]["ramai"]["mean_edge_density"]
    st.add_callout_box(
        s16,
        st.MARGIN_X,
        Inches(5.38),
        st.CONTENT_WIDTH,
        Inches(1.38),
        f"edge_density = jumlah_piksel_tepi / total_piksel (Canny). Contoh data sampel: polos = {polos_ed:.4f}, ramai = {ramai_ed:.4f}.\nCatatan: edge density & entropy adalah proxy kompleksitas visual background, bukan ukuran langsung kesulitan model.",
        accent_color=st.RED,
        bg_color=st.TINT_RED,
        font_size=Pt(19),
    )
    st.add_footer(s16, 16, SESSION_LABEL)
    st.set_speaker_notes(
        s16,
        f"""Alokasi waktu: 2 menit

Naskah ajar:
Kita memakai algoritma Canny Edge Detection untuk mencari garis-garis tepi pada gambar, lalu menghitung rasio piksel tepi terhadap total piksel. Pada 119 foto valid contoh data sampel kita, rata-rata edge density kondisi polos adalah {polos_ed:.4f}, sedangkan kondisi ramai jauh lebih tinggi yaitu {ramai_ed:.4f}.

Penjelasan konsep:
Penting dicatat: edge density hanyalah proxy (pendekatan) untuk kompleksitas visual background, bukan ukuran langsung seberapa sulit model akan belajar.

Transisi:
Terakhir di bagian teori, mari waspadai 3 jebakan klasik saat mengumpulkan dataset foto sendiri.""",
    )

    # =======================================================================
    # SLIDE 17 — THREE COMMON DATA TRAPS
    # =======================================================================
    s17 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s17, "TEORI · KUALITAS DATA", "Tiga Jebakan dalam Dataset")
    traps = [
        ("1", "Orientasi EXIF", "Foto HP sering tersimpan miring meski tampak tegak di galeri.", st.YELLOW, st.TINT_YELLOW),
        ("2", "Foto kembar / burst", "Foto identik atau nyaris sama bisa bocor ke train & test.", st.RED, st.TINT_RED),
        ("3", "Data leakage", "EDA bersifat deskriptif: jangan memilih data berdasarkan test set!", st.BLUE, st.TINT_BLUE),
    ]
    for idx, (num, ttl, desc, acc, tint) in enumerate(traps):
        st.add_card(
            s17,
            st.MARGIN_X + idx * Inches(4.02),
            Inches(1.75),
            Inches(3.78),
            Inches(3.55),
            title=ttl,
            body=desc,
            bg_color=tint,
            accent_color=acc,
            badge_text=num,
            title_size=Pt(25),
            body_size=Pt(22),
            border_color=None,
        )
    s17.shapes.add_picture(str(vis["exif"]), Inches(0.75), Inches(5.45), height=Inches(1.48))
    st.add_text_box(
        s17,
        Inches(3.9),
        Inches(5.65),
        Inches(8.6),
        Inches(1.1),
        f"Pada contoh data sampel (120 file): ditemukan {stats['exif_orientation_6_count']} foto EXIF=6, {stats['duplicate_file_count']} file duplikat identik, dan {stats['corrupted_count']} file rusak.",
        font_name=st.FONT_BODY,
        size=Pt(22),
        color=st.TEXT_DARK,
    )
    st.add_footer(s17, 17, SESSION_LABEL)
    st.set_speaker_notes(
        s17,
        """Alokasi waktu: 2 menit

Naskah ajar:
Ada tiga jebakan yang harus kita tangkap di notebook nanti. Pertama, tag EXIF Orientation=6 membuat foto terputar 90 derajat saat dibaca mentah (lihat contoh di kiri bawah). Kedua, foto kembar/burst yang dicek dengan hash. Ketiga, data leakage: ingat, EDA bersifat deskriptif saja; kita tidak boleh membuang atau memilih data berdasarkan hasil test set.

Penjelasan konsep:
Setelah ini kita istirahat 5 menit (menit 40–45) sebelum masuk ke sesi Hands-on notebook.

Transisi:
Sampai ketemu 5 menit lagi untuk praktik langsung di notebook!""",
    )

    # =======================================================================
    # SLIDE 18 — HANDS-ON SECTION DIVIDER (6 steps from PLAN.md P4)
    # =======================================================================
    s18 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header_rich(
        s18,
        "BAGIAN 02 · ISTIRAHAT 5 MENIT + HANDS-ON 50 MENIT (MENIT 40–95)",
        [("HANDS-ON: ", st.GREEN), ("Praktik EDA Notebook", st.TEXT_DARK)],
        kicker_color=st.GREEN,
    )
    steps_detail = [
        ("01", "Load foto & baca nilai arraynya", "Buka gambar ke RGB & periksa shape serta tipe data uint8.", st.BLUE),
        ("02", "Koreksi orientasi EXIF", "Gunakan ImageOps.exif_transpose() agar foto HP tegak.", st.RED),
        ("03", "Inventaris dataset", "Hitung jumlah foto per kelas × kondisi, resolusi, dan ukuran file.", st.YELLOW),
        ("04", "Deteksi file rusak & duplikat", "Verifikasi Pillow dan bandingkan hash SHA-256 tiap file.", st.GREEN),
        ("05", "Hitung statistik citra", "Brightness (mean), kontras (std), dan edge density (Canny).", st.BLUE),
        ("06", "Visualisasi boxplot polos vs ramai", "Bandingkan sebaran kedua kondisi secara visual.", st.RED),
    ]
    st.add_numbered_steps(s18, st.MARGIN_X, Inches(1.65), Inches(7.25), steps_detail, row_height=0.86)
    st.add_card(
        s18,
        Inches(8.35),
        Inches(1.65),
        Inches(4.23),
        Inches(3.6),
        title="Target Output Hands-on",
        body="• Tabel statistik kelas × kondisi\n• Daftar file rusak & duplikat\n• Grafik boxplot polos vs ramai",
        bg_color=st.TINT_GREEN,
        accent_color=st.GREEN,
        title_size=Pt(24),
        body_size=Pt(21),
        border_color=None,
    )
    st.add_callout_box(
        s18,
        Inches(8.35),
        Inches(5.45),
        Inches(4.23),
        Inches(1.25),
        "Jeda istirahat 5 menit sebelum mulai mengetik di Google Colab / lokal.",
        accent_color=st.YELLOW,
        bg_color=st.TINT_YELLOW,
        font_size=Pt(18),
        bold=True,
    )
    st.add_footer(s18, 18, SESSION_LABEL)
    st.set_speaker_notes(
        s18,
        """Alokasi waktu: 55 menit (5 menit istirahat + 50 menit hands-on notebook)

Naskah ajar:
Selamat datang kembali! Selama 50 menit ke depan kita akan mengerjakan notebook P04. Ada 6 langkah utama sesuai rencana belajar: mulai dari membaca array gambar, memperbaiki orientasi EXIF, menginventaris jumlah foto per kelas dan kondisi, mendeteksi file rusak dan duplikat dengan hash, menghitung brightness/kontras/edge density, hingga membuat boxplot perbandingan polos vs ramai.

Penjelasan konsep:
Pandu peserta mengisi bagian `# TODO` secara bertahap dan memastikan semua sel `assert` berjalan dengan benar pada data sampel.

Transisi:
Setelah statistik dan boxplot selesai dibuat, mari kita masuk ke Mini-challenge!""",
    )

    # =======================================================================
    # SLIDE 19 — MINI-CHALLENGE DIVIDER
    # =======================================================================
    s19 = st.add_blank_slide(prs, st.YELLOW)
    st.add_text_box(
        s19,
        st.MARGIN_X,
        Inches(1.35),
        st.CONTENT_WIDTH,
        Inches(0.45),
        "BAGIAN 03 · DISKUSI 15 MENIT (MENIT 95–110)",
        font_name=st.FONT_TITLE,
        size=st.SIZE_KICKER,
        color=st.TEXT_DARK,
        bold=True,
    )
    st.add_text_box(
        s19,
        st.MARGIN_X,
        Inches(1.85),
        st.CONTENT_WIDTH,
        Inches(1.1),
        "MINI-CHALLENGE",
        font_name=st.FONT_TITLE,
        size=st.SIZE_DIVIDER_TITLE,
        color=st.TEXT_DARK,
        bold=True,
    )
    st.add_card(
        s19,
        st.MARGIN_X,
        Inches(3.2),
        st.CONTENT_WIDTH,
        Inches(2.5),
        title="Hanya dari statistik, kondisi mana yang lebih sulit bagi model dan mengapa?",
        body="Catat sebagai hipotesis awal.",
        bg_color=st.LIGHT_BG,
        accent_color=st.RED,
        title_size=Pt(30),
        body_size=Pt(26),
        border_color=None,
    )
    st.add_footer(s19, 19, SESSION_LABEL, on_dark=False, fg_color=st.TEXT_DARK)
    st.set_speaker_notes(
        s19,
        """Alokasi waktu: 15 menit

Naskah ajar:
Sekarang coba lihat kembali tabel statistik dan boxplot yang baru saja kita hasilkan. Hanya dari statistik (brightness, kontras, edge density), menurutmu kondisi mana yang lebih sulit bagi model nanti: polos atau ramai? Dan mengapa?

Instruksi interaksi:
Minta peserta menuliskan alasannya secara lisan atau di catatan sebagai hipotesis awal. Jangan langsung memberi jawaban final—hipotesis ini akan diuji nanti di P11 saat evaluasi model!

Transisi:
Mari kita rangkum istilah-istilah baru yang kita pelajari hari ini di Glosarium.""",
    )

    # =======================================================================
    # SLIDE 20 — GLOSSARY
    # =======================================================================
    s20 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s20, "REFERENSI CEPAT", "Glosarium Singkat")
    glossary_items = [
        ("Piksel", "Unit titik terkecil penyusun gambar digital."),
        ("Channel", "Lapisan warna pada gambar (mis. R, G, B)."),
        ("Shape", "Dimensi array gambar: (tinggi, lebar, channel)."),
        ("uint8", "Tipe data bilangan bulat 0–255 untuk file gambar."),
        ("float32", "Tipe data desimal untuk komputasi neural network."),
        ("Normalisasi", "Mengubah rentang nilai piksel ke skala konsisten."),
        ("EDA", "Eksplorasi awal untuk mengenali pola & kualitas data."),
        ("Edge density", "Rasio piksel tepi terhadap total piksel gambar."),
        ("Class imbalance", "Ketimpangan jumlah foto antar kelas."),
    ]
    st.add_styled_table(
        s20,
        st.MARGIN_X,
        Inches(1.58),
        st.CONTENT_WIDTH,
        Inches(5.2),
        headers=["Istilah", "Definisi Singkat"],
        rows=[[k, v] for k, v in glossary_items],
        col_widths=[Inches(3.1), Inches(8.73)],
        header_color=st.BLUE,
        font_size=Pt(20),
        header_size=Pt(22),
    )
    st.add_footer(s20, 20, SESSION_LABEL)
    st.set_speaker_notes(
        s20,
        """Alokasi waktu: 2 menit

Naskah ajar:
Ini adalah 9 istilah kunci dari sesi P04 sebagai pegangan cepat. Pastikan tidak ada istilah yang masih terasa asing sebelum kita masuk ke quiz.

Penjelasan konsep:
Tanyakan apakah ada dari 9 istilah ini yang masih perlu diulang contohnya secara singkat.

Transisi:
Sekarang saatnya menguji pemahaman dengan 5 soal quiz singkat!""",
    )

    # =======================================================================
    # SLIDE 21 — QUIZ (5 questions, no answers on slide)
    # =======================================================================
    s21 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s21, "EVALUASI SINGKAT", "Sudah Paham? Uji Dirimu!")
    questions = [
        ("1", "Apa perbedaan uint8 dan float32?", st.BLUE, st.TINT_BLUE),
        ("2", "Apa shape foto RGB berukuran 224 × 224?", st.RED, st.TINT_RED),
        ("3", "Mengapa orientasi EXIF perlu diperiksa?", st.YELLOW, st.TINT_YELLOW),
        ("4", "Apa yang diukur oleh edge density?", st.GREEN, st.TINT_GREEN),
        ("5", "Mengapa test set tidak digunakan untuk memilih keputusan EDA?", st.BLUE, st.TINT_BLUE),
    ]
    for idx, (num, q_txt, acc, tint) in enumerate(questions):
        top_y = Inches(1.58) + idx * Inches(1.04)
        st.add_card(
            s21,
            st.MARGIN_X,
            top_y,
            st.CONTENT_WIDTH,
            Inches(0.88),
            bg_color=tint,
            border_color=None,
            shadow=False,
        )
        st.add_pill_tag(s21, num, st.MARGIN_X + Inches(0.22), top_y + Inches(0.20), bg_color=acc, text_color=st.TEXT_DARK if acc in (st.YELLOW, st.GREEN) else st.TEXT_LIGHT, width=Inches(0.54), height=Inches(0.48), font_name=st.FONT_TITLE, size=Pt(20))
        st.add_text_box(
            s21,
            st.MARGIN_X + Inches(0.95),
            top_y + Inches(0.20),
            st.CONTENT_WIDTH - Inches(1.2),
            Inches(0.52),
            q_txt,
            font_name=st.FONT_BODY,
            size=Pt(24),
            color=st.TEXT_DARK,
        )
    st.add_footer(s21, 21, SESSION_LABEL)
    st.set_speaker_notes(
        s21,
        """Alokasi waktu: 5 menit

Naskah ajar:
Ayo kita jawab 5 pertanyaan ini bersama-sama tanpa melihat catatan!

Kunci jawaban & penjelasan:
1. `uint8` adalah bilangan bulat 0–255 (hemat memori untuk penyimpanan file gambar), sedangkan `float32` adalah bilangan desimal yang dibutuhkan untuk normalisasi dan perhitungan gradien neural network.
2. `(224, 224, 3)` — tinggi 224, lebar 224, dan 3 channel warna RGB.
3. Karena foto HP sering menyimpan posisi putaran di metadata EXIF (mis. tag Orientation=6) sehingga saat dibaca mentah gambarnya tampak miring atau terbalik.
4. Edge density mengukur rasio jumlah piksel tepi (dari deteksi tepi seperti Canny) terhadap total piksel sebagai pendekatan/proxy kompleksitas visual background.
5. Karena akan menyebabkan data leakage; EDA harus deskriptif dan keputusan modeling tidak boleh mengintip test set.

Transisi:
Mari kita tutup sesi hari ini dengan rangkuman dan preview sesi berikutnya.""",
    )

    # =======================================================================
    # SLIDE 22 — CLOSING & NEXT SESSION (no homework)
    # =======================================================================
    s22 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s22, "RANGKUMAN & PENUTUP", "Takeaways & Next Step")
    takeaways = [
        ("1", "Gambar adalah representasi angka", st.BLUE, st.TINT_BLUE),
        ("2", "Preprocessing harus konsisten", st.GREEN, st.TINT_GREEN),
        ("3", "EDA memahami kualitas dataset", st.RED, st.TINT_RED),
    ]
    for idx, (num, ttl, acc, tint) in enumerate(takeaways):
        st.add_card(
            s22,
            st.MARGIN_X + idx * Inches(4.02),
            Inches(1.62),
            Inches(3.78),
            Inches(1.95),
            title=ttl,
            bg_color=tint,
            accent_color=acc,
            badge_text=num,
            title_size=Pt(22),
            border_color=None,
        )
    st.add_styled_table(
        s22,
        st.MARGIN_X,
        Inches(3.85),
        Inches(6.9),
        Inches(2.8),
        headers=["Kriteria Berhasil P04", "Target"],
        rows=[
            ["Pahami shape input", "Bisa jelaskan (224, 224, 3)"],
            ["Statistik dataset", "Tabel polos vs ramai terbaca"],
            ["Kebersihan data", "Bebas file rusak & duplikat"],
        ],
        col_widths=[Inches(3.2), Inches(3.7)],
        header_color=st.DARK_BG,
        font_size=Pt(22),
        header_size=Pt(22),
    )
    st.add_card(
        s22,
        Inches(8.05),
        Inches(3.85),
        Inches(4.53),
        Inches(2.8),
        title="Sesi Berikutnya",
        body="P5 — Teori Neural Network\nRabu, 18 November 2026\n19:30–21:30 WIB",
        bg_color=st.TINT_YELLOW,
        accent_color=st.YELLOW,
        title_size=Pt(26),
        body_size=Pt(23),
        border_color=None,
    )
    st.add_footer(s22, 22, SESSION_LABEL)
    st.set_speaker_notes(
        s22,
        """Alokasi waktu: 3 menit

Naskah ajar:
Tiga hal utama yang kita bawa pulang hari ini: gambar adalah angka, preprocessing harus konsisten antara training dan prediksi, dan EDA membantu kita memahami kualitas data sebelum melatih model. Pastikan ketiga kriteria berhasil P04 sudah tercapai di akhir sesi ini tanpa perlu tugas rumah tambahan.

Penjelasan konsep:
Di pertemuan berikutnya (P5, Rabu 18 November 2026), kita akan masuk ke Teori Neural Network: bagaimana angka-angka piksel tadi diproses oleh neuron, fungsi aktivasi, dan softmax.

Transisi:
Terima kasih sudah mengikuti Sesi P04 dengan antusias. Sampai jumpa hari Rabu!""",
    )

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT_PPTX)


def main() -> None:
    stats, df = analyze_sample_dataset()
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    STATS_JSON.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    vis = generate_visualizations(df, stats)
    build_deck(stats, vis)
    print(f"PPTX berhasil dibuat: {OUT_PPTX}")
    print(f"Statistik sampel: valid={stats['valid_images']}, rusak={stats['corrupted_count']}, duplikat={stats['duplicate_file_count']}, exif6={stats['exif_orientation_6_count']}")


if __name__ == "__main__":
    main()
