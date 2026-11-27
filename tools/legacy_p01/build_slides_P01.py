"""Build materials/P01/P01_understanding_images_processing_eda.pptx from data/sample/ using slide_theme.py.

Generates real data visualizations in materials/P01/assets/P01/ and composes
29 Google I/O-inspired slides (including MNIST 28x28 case study, RGB sub-pixel
screen display, 3 AI Fundamental slides, & 2 Reference slides) synced with HTML
and Bahasa Indonesia speaker notes summing to 120 minutes.
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
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools" / "legacy_p01"))

import slide_theme as st

SAMPLE_DIR = ROOT_DIR / "data" / "sample"
ASSETS_DIR = ROOT_DIR / "materials" / "P01" / "assets" / "P01"
OUT_PPTX = ROOT_DIR / "materials" / "P01" / "P01_understanding_images_processing_eda.pptx"
STATS_JSON = ASSETS_DIR / "sample_stats.json"

SESSION_LABEL = "P01 · Understanding Images, Image Processing & EDA"


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

    polos_asset = ASSETS_DIR / "sample_polos.jpg"
    ramai_asset = ASSETS_DIR / "sample_ramai.jpg"
    if not polos_asset.exists():
        polos_asset = SAMPLE_DIR / "bintang" / "polos" / "bintang_polos_02.jpg"
    if not ramai_asset.exists():
        ramai_asset = SAMPLE_DIR / "bintang" / "ramai" / "bintang_ramai_01.jpg"
    g_polos_hist = np.array(ImageOps.exif_transpose(Image.open(polos_asset)).convert("L"))
    g_ramai_hist = np.array(ImageOps.exif_transpose(Image.open(ramai_asset)).convert("L"))

    polos_df = df[df["kondisi"] == "polos"]
    ramai_df = df[df["kondisi"] == "ramai"]

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
        "hist256_polos": np.bincount(g_polos_hist.ravel(), minlength=256).tolist(),
        "hist256_ramai": np.bincount(g_ramai_hist.ravel(), minlength=256).tolist(),
        "dist_polos_b": [round(float(x), 2) for x in polos_df["mean_intensity"].tolist()],
        "dist_polos_c": [round(float(x), 2) for x in polos_df["std_intensity"].tolist()],
        "dist_ramai_b": [round(float(x), 2) for x in ramai_df["mean_intensity"].tolist()],
        "dist_ramai_c": [round(float(x), 2) for x in ramai_df["std_intensity"].tolist()],
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

    # 7. Histogram & Brightness/Contrast Comparison (Synced with HTML Slide 33 & 34: Histogram + Boxplot 119 Valid Images)
    p7 = ASSETS_DIR / "07_histogram_brightness_contrast.png"
    polos_src = ASSETS_DIR / "sample_polos.jpg"
    ramai_src = ASSETS_DIR / "sample_ramai.jpg"
    if not polos_src.exists():
        polos_src = SAMPLE_DIR / "bintang" / "polos" / "bintang_polos_02.jpg"
    if not ramai_src.exists():
        ramai_src = SAMPLE_DIR / "bintang" / "ramai" / "bintang_ramai_01.jpg"
    with Image.open(polos_src) as im:
        g_polos = np.array(ImageOps.exif_transpose(im).convert("L"))
    with Image.open(ramai_src) as im:
        g_ramai = np.array(ImageOps.exif_transpose(im).convert("L"))

    fig, axes_h = plt.subplots(1, 3, figsize=(11.6, 3.95), dpi=200)
    ax1, ax2, ax3 = axes_h

    ax1.hist(g_polos.ravel(), bins=32, range=(0, 256), color="#4285F4", alpha=0.88, edgecolor="#FFFFFF")
    ax1.axvline(g_polos.mean(), color="#EA4335", linestyle="--", linewidth=2.2, label=f"Mean = {g_polos.mean():.1f}")
    ax1.set_title(f"Histogram Polos (65.536 px)\nMean={g_polos.mean():.1f} | Std={g_polos.std():.1f}", fontsize=12, fontweight="bold", color="#1A73E8")
    ax1.set_xlabel("Intensitas Piksel (0–255)", fontsize=11)
    ax1.set_ylabel("Jumlah Piksel", fontsize=11)
    ax1.legend(fontsize=10, loc="upper left")

    ax2.hist(g_ramai.ravel(), bins=32, range=(0, 256), color="#EA4335", alpha=0.86, edgecolor="#FFFFFF")
    ax2.axvline(g_ramai.mean(), color="#202124", linestyle="--", linewidth=2.2, label=f"Mean = {g_ramai.mean():.1f}")
    ax2.set_title(f"Histogram Ramai (65.536 px)\nMean={g_ramai.mean():.1f} | Std={g_ramai.std():.1f}", fontsize=12, fontweight="bold", color="#C5221F")
    ax2.set_xlabel("Intensitas Piksel (0–255)", fontsize=11)
    ax2.set_ylabel("Jumlah Piksel", fontsize=11)
    ax2.legend(fontsize=10, loc="upper left")

    bp_b_p = np.array(stats["dist_polos_b"])
    bp_b_r = np.array(stats["dist_ramai_b"])
    bp_c_p = np.array(stats["dist_polos_c"])
    bp_c_r = np.array(stats["dist_ramai_c"])
    bplot = ax3.boxplot(
        [bp_b_p, bp_b_r, bp_c_p, bp_c_r],
        tick_labels=["B:Polos", "B:Ramai", "C:Polos", "C:Ramai"],
        patch_artist=True,
        widths=0.52,
    )
    for b_idx, (fcol, ecol) in enumerate([("#E8F0FE", "#1A73E8"), ("#FCE8E6", "#EA4335"), ("#E8F0FE", "#1A73E8"), ("#FCE8E6", "#EA4335")]):
        bplot["boxes"][b_idx].set_facecolor(fcol)
        bplot["boxes"][b_idx].set_edgecolor(ecol)
    ax3.set_title(
        f"Boxplot 119 Foto Valid (B vs C)\nB: {bp_b_p.mean():.1f} vs {bp_b_r.mean():.1f} | C: {bp_c_p.mean():.1f} vs {bp_c_r.mean():.1f}",
        fontsize=11.5,
        fontweight="bold",
        color="#202124",
    )
    ax3.set_ylabel("Skala Nilai (0–255)", fontsize=11)
    ax3.grid(axis="y", alpha=0.3)

    fig.tight_layout(pad=1.2)
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
    puppy_fp = ASSETS_DIR / "exif_puppy.jpg"
    if puppy_fp.exists():
        with Image.open(puppy_fp) as im:
            fixed_im = im.convert("RGB")
            raw_arr = np.array(fixed_im.rotate(90, expand=True))
            fixed_arr = np.array(fixed_im)
    else:
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

    # 11. RGB Screen Display (Synced with HTML Slide 09: Tahap 1: Nyalakan 3 Lampu Pixel -> Tahap 2: Susun 3 Lapis RGB -> Tahap 3: Tampil Jadi Gambar Utuh)
    p11 = ASSETS_DIR / "11_rgb_screen_display.png"
    fig, ax = plt.subplots(figsize=(11.6, 3.85), dpi=200)
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 3.85)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    # Stage 1 Box (Left): Tahap 1: Nyalakan 3 Lampu Pixel (Zoom 1000x)
    ax.add_patch(patches.FancyBboxPatch((0.12, 0.2), 3.40, 3.45, boxstyle="round,pad=0.05,rounding_size=0.22", facecolor="#E8F0FE", edgecolor="#C6DAFC", linewidth=2))
    ax.text(1.82, 3.37, "Tahap 1: Nyalakan 3 Lampu Pixel", ha="center", va="center", fontsize=11.3, fontweight="bold", color="#1A73E8")
    ax.add_patch(patches.FancyBboxPatch((0.26, 0.92), 3.12, 2.18, boxstyle="round,pad=0.04,rounding_size=0.16", facecolor="#111317", edgecolor="#3C4043", linewidth=1.8))

    # Left inside Stage 1: 3 sub-pixel LED bars inside 1 pixel housing
    ax.add_patch(patches.FancyBboxPatch((0.38, 1.12), 1.66, 1.80, boxstyle="round,pad=0.03,rounding_size=0.12", facecolor="#181B22", edgecolor="#5F6368", linewidth=1.1, linestyle="--"))
    ax.text(1.21, 2.74, "1 KOTAK PIXEL LAYAR", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#9AA0A6", family="monospace")
    for xx, lbl, pct, col in [
        (0.66, "R 92%", 0.92, "#EA4335"),
        (1.21, "G 26%", 0.26, "#34A853"),
        (1.76, "B 21%", 0.21, "#4285F4"),
    ]:
        ax.add_patch(patches.FancyBboxPatch((xx - 0.19, 1.44), 0.38, 1.12, boxstyle="round,pad=0.02,rounding_size=0.08", facecolor="#23262D", edgecolor="#3C4043", linewidth=1.0))
        ax.add_patch(patches.FancyBboxPatch((xx - 0.15, 1.48), 0.30, 1.04 * pct, boxstyle="round,pad=0.0,rounding_size=0.06", facecolor=col, edgecolor="none"))
        ax.text(xx, 1.26, lbl, ha="center", va="center", fontsize=7.8, fontweight="bold", color=col, family="monospace")

    # Small arrow to merged color output on the right of Stage 1
    ax.annotate("", xy=(2.38, 2.02), xytext=(2.10, 2.02), arrowprops=dict(arrowstyle="-|>,head_width=0.20,head_length=0.16", lw=2.2, color="#FBBC04"))
    ax.add_patch(patches.FancyBboxPatch((2.42, 1.12), 0.84, 1.80, boxstyle="round,pad=0.03,rounding_size=0.12", facecolor="#181B22", edgecolor="#3C4043", linewidth=1.1))
    ax.text(2.84, 2.66, "1 TITIK\nWARNA", ha="center", va="center", fontsize=7.4, fontweight="bold", color="#BDC1C6")
    ax.add_patch(patches.FancyBboxPatch((2.57, 1.66), 0.54, 0.54, boxstyle="round,pad=0.02,rounding_size=0.10", facecolor="#EA4335", edgecolor="#FFFFFF", linewidth=1.5))
    ax.text(2.84, 1.34, "Titik\nMerah", ha="center", va="center", fontsize=8.2, fontweight="bold", color="#FBBC04")
    ax.text(1.82, 0.54, "3 lampu mikro R-G-B menyala jadi 1 titik warna", ha="center", va="center", fontsize=9.2, color="#3C4043")

    # Arrow 1
    ax.annotate("", xy=(4.00, 1.95), xytext=(3.56, 1.95), arrowprops=dict(arrowstyle="-|>,head_width=0.26,head_length=0.22", lw=2.8, color="#34A853"))
    ax.text(3.78, 2.24, "Tumpuk", ha="center", va="center", fontsize=9.0, fontweight="bold", color="#137333")

    # Stage 2 Box (Middle): Tahap 2: Susun 3 Lapis RGB (3D Stacked Layers)
    ax.add_patch(patches.FancyBboxPatch((4.04, 0.2), 3.48, 3.45, boxstyle="round,pad=0.05,rounding_size=0.22", facecolor="#FFFFFF", edgecolor="#DADCE0", linewidth=2))
    ax.text(5.78, 3.37, "Tahap 2: Susun 3 Lapis RGB", ha="center", va="center", fontsize=11.3, fontweight="bold", color="#202124")
    ax.add_patch(patches.FancyBboxPatch((4.20, 0.92), 3.16, 2.18, boxstyle="round,pad=0.04,rounding_size=0.16", facecolor="#111317", edgecolor="#3C4043", linewidth=1.8))

    layers_spec = [
        (1.06, "Lapis B (21%)", "53", "#4285F4", "#8AB4F8", 0.42),
        (1.68, "Lapis G (26%)", "67", "#34A853", "#81C995", 0.48),
        (2.30, "Lapis R (92%)", "234", "#EA4335", "#F28B82", 0.94),
    ]
    ax.plot([5.32, 5.32], [1.42, 1.80], color="#FBBC04", lw=1.6, linestyle="--")
    ax.plot([5.32, 5.32], [2.04, 2.42], color="#FBBC04", lw=1.6, linestyle="--")
    for y_base, badge_txt, val_str, col_hex, txt_hex, cell_alpha in layers_spec:
        plane_pts = [(4.62, y_base + 0.50), (6.12, y_base + 0.50), (5.84, y_base), (4.34, y_base)]
        ax.add_patch(patches.Polygon(plane_pts, facecolor=col_hex, alpha=0.22, edgecolor="none"))
        ax.add_patch(patches.Polygon(plane_pts, facecolor="none", edgecolor=col_hex, linewidth=1.5))
        ax.plot([5.12, 4.84], [y_base + 0.50, y_base], color=col_hex, alpha=0.35, lw=0.7)
        ax.plot([5.62, 5.34], [y_base + 0.50, y_base], color=col_hex, alpha=0.35, lw=0.7)
        ax.plot([4.48, 5.98], [y_base + 0.25, y_base + 0.25], color=col_hex, alpha=0.35, lw=0.7)
        cell_pts = [(5.14, y_base + 0.38), (5.62, y_base + 0.38), (5.50, y_base + 0.12), (5.02, y_base + 0.12)]
        ax.add_patch(patches.Polygon(cell_pts, facecolor="#16181D", edgecolor="none"))
        ax.add_patch(patches.Polygon(cell_pts, facecolor=col_hex, alpha=cell_alpha, edgecolor="#FFFFFF", linewidth=1.3))
        ax.text(5.32, y_base + 0.25, val_str, ha="center", va="center", fontsize=9.8, fontweight="bold", color="#FFFFFF", family="monospace")
        ax.text(6.70, y_base + 0.24, badge_txt, ha="center", va="center", fontsize=8.6, fontweight="bold", color=txt_hex, family="monospace")

    ax.text(5.78, 0.54, "3 angka berasal dari 3 lapis channel R-G-B", ha="center", va="center", fontsize=9.2, color="#3C4043")

    # Arrow 2
    ax.annotate("", xy=(8.02, 1.95), xytext=(7.55, 1.95), arrowprops=dict(arrowstyle="-|>,head_width=0.26,head_length=0.22", lw=2.8, color="#FBBC04"))
    ax.text(7.78, 2.24, "Tampil", ha="center", va="center", fontsize=9.0, fontweight="bold", color="#B06000")

    # Stage 3 Box (Right): Tahap 3: Tampil Jadi Gambar Utuh (with 1-pixel pointer & RGB readout)
    ax.add_patch(patches.FancyBboxPatch((8.06, 0.2), 3.42, 3.45, boxstyle="round,pad=0.05,rounding_size=0.22", facecolor="#FEF7E0", edgecolor="#FDE293", linewidth=2))
    ax.text(9.77, 3.37, "Tahap 3: Tampil Jadi Gambar Utuh", ha="center", va="center", fontsize=11.3, fontweight="bold", color="#B06000")
    ax.add_patch(patches.FancyBboxPatch((8.20, 0.92), 3.14, 2.18, boxstyle="round,pad=0.04,rounding_size=0.16", facecolor="#202124", edgecolor="#3C4043", linewidth=1.5))
    ax.text(9.77, 2.86, "Pixel(112, 88) · Apel Merah", ha="center", va="center", fontsize=9.0, family="monospace", color="#8AB4F8", fontweight="bold")

    # Mini gridded image on the left of Stage 3 pointing to 1 pixel
    img_x0, img_y0, img_s = 8.32, 1.16, 1.32
    ax.add_patch(patches.FancyBboxPatch((img_x0, img_y0), img_s, img_s, boxstyle="round,pad=0.0,rounding_size=0.08", facecolor="#5E97F6", edgecolor="#8AB4F8", linewidth=1.2))
    ax.add_patch(patches.Rectangle((img_x0, img_y0), img_s, 0.26, facecolor="#81C995", edgecolor="none"))
    ax.add_patch(patches.Circle((img_x0 + 0.62, img_y0 + 0.62), 0.34, facecolor="#EA4335", edgecolor="none"))
    ax.add_patch(patches.Ellipse((img_x0 + 0.78, img_y0 + 1.02), 0.24, 0.11, angle=20, facecolor="#34A853", edgecolor="none"))
    step_g = img_s / 6.0
    for gi in range(1, 6):
        ax.plot([img_x0 + gi * step_g, img_x0 + gi * step_g], [img_y0, img_y0 + img_s], color="#FFFFFF", alpha=0.30, lw=0.6)
        ax.plot([img_x0, img_x0 + img_s], [img_y0 + gi * step_g, img_y0 + gi * step_g], color="#FFFFFF", alpha=0.30, lw=0.6)
    px_x = img_x0 + 2 * step_g
    px_y = img_y0 + 2 * step_g
    ax.add_patch(patches.Rectangle((px_x, px_y), step_g, step_g, facecolor="none", edgecolor="#FBBC04", linewidth=2.0))
    ax.plot([px_x + step_g, 9.86], [px_y + step_g, 2.52], color="#FBBC04", lw=1.3, linestyle="--")
    ax.plot([px_x + step_g, 9.86], [px_y, 1.24], color="#FBBC04", lw=1.3, linestyle="--")

    # RGB bars box on the right of Stage 3
    ax.add_patch(patches.FancyBboxPatch((9.86, 1.18), 1.36, 1.38, boxstyle="round,pad=0.03,rounding_size=0.10", facecolor="#16181D", edgecolor="#FBBC04", linewidth=1.2))
    for yy, lbl, val, pct, col in [
        (2.26, "R", 234, 0.92, "#EA4335"),
        (1.86, "G", 67, 0.26, "#34A853"),
        (1.46, "B", 53, 0.21, "#4285F4"),
    ]:
        ax.text(9.94, yy, lbl, ha="left", va="center", fontsize=9.0, fontweight="bold", color=col, family="monospace")
        ax.add_patch(patches.FancyBboxPatch((10.14, yy - 0.06), 0.64, 0.12, boxstyle="round,pad=0.0,rounding_size=0.04", facecolor="#3C4043", edgecolor="none"))
        ax.add_patch(patches.FancyBboxPatch((10.14, yy - 0.06), 0.64 * pct, 0.12, boxstyle="round,pad=0.0,rounding_size=0.04", facecolor=col, edgecolor="none"))
        ax.text(11.16, yy, str(val), ha="right", va="center", fontsize=9.0, fontweight="bold", color="#FFFFFF", family="monospace")
    ax.text(9.77, 0.54, "Jutaan pixel menyatu jadi gambar utuh [R,G,B]", ha="center", va="center", fontsize=9.2, color="#3C4043")

    fig.tight_layout(pad=0.25)
    fig.savefig(p11, dpi=200, facecolor="#FFFFFF")
    plt.close(fig)
    paths["screen_display"] = p11

    # 12. Color Channels Overview 2x2 (1 Ch, 3 Ch, 4 Ch, 5+ Ch)
    p12 = ASSETS_DIR / "12_color_channels_overview.png"
    fig, axes = plt.subplots(2, 2, figsize=(9.4, 5.8))
    fig.patch.set_facecolor("#FFFFFF")
    panels = [
        ("1 CHANNEL · GRAYSCALE", "Hitam-Putih & Abu-Abu (MNIST, Rontgen)", "#F8F9FA", "#5F6368"),
        ("3 CHANNELS · RGB (FOKUS!)", "Foto Penuh Warna (+ HSV, LAB, YCbCr)", "#E8F0FE", "#1A73E8"),
        ("4 CHANNELS · RGBA & CMYK", "Transparan (PNG) & Cetak Printer", "#FEF7E0", "#8A5700"),
        ("5+ CHANNELS · MULTISPECTRAL", "Satelit, Drone (RGB + NIR + Thermal)", "#E6F4EA", "#137333"),
    ]
    for idx, (ax, (badge, sub, bg, accent)) in enumerate(zip(axes.flat, panels)):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6.2)
        ax.axis("off")
        ax.add_patch(patches.FancyBboxPatch((0.15, 0.15), 9.7, 5.9, boxstyle="round,pad=0.05,rounding_size=0.35", facecolor=bg, edgecolor=accent, linewidth=2 if idx == 1 else 1.4))
        ax.text(0.55, 5.45, badge, fontsize=11, fontweight="bold", color=accent, family="monospace")
        ax.text(0.55, 4.82, sub, fontsize=10.5, fontweight="bold", color="#202124")
        if idx == 0:
            ax.add_patch(patches.FancyBboxPatch((0.6, 0.7), 3.6, 3.6, boxstyle="round,pad=0.04,rounding_size=0.25", facecolor="#181A1F", edgecolor="#5F6368", linewidth=1.2))
            ax.plot([1.4, 3.3, 2.0], [3.5, 3.5, 1.4], color="#EAECEF", lw=6, solid_capstyle="round")
            ax.text(2.4, 0.36, "Contoh: Angka MNIST / X-Ray", ha="center", fontsize=8.8, color="#3C4043", fontweight="bold")
            ax.add_patch(patches.FancyBboxPatch((4.8, 1.4), 4.4, 2.3, boxstyle="round,pad=0.04,rounding_size=0.2", facecolor="#FFFFFF", edgecolor="#9AA0A6", linewidth=1.4))
            ax.text(7.0, 2.85, "[142]", ha="center", va="center", fontsize=14, fontweight="bold", family="monospace", color="#202124")
            ax.text(7.0, 1.95, "1 angka / pixel (0-255)", ha="center", va="center", fontsize=9.5, color="#5F6368")
        elif idx == 1:
            for j, (dx, dy, lbl, fcol, ecol) in enumerate([
                (0.7, 2.0, "R", "#FCE8E6", "#EA4335"),
                (1.5, 1.4, "G", "#E6F4EA", "#34A853"),
                (2.3, 0.8, "B", "#E8F0FE", "#4285F4"),
            ]):
                ax.add_patch(patches.FancyBboxPatch((dx, dy), 2.3, 2.0, boxstyle="round,pad=0.03,rounding_size=0.2", facecolor=fcol, edgecolor=ecol, linewidth=1.6))
                ax.text(dx + 0.4, dy + 1.5, lbl, fontsize=12, fontweight="bold", family="monospace", color=ecol)
            ax.annotate("", xy=(5.65, 2.4), xytext=(4.85, 2.4), arrowprops=dict(arrowstyle="-|>,head_width=0.22,head_length=0.2", lw=2.5, color="#1A73E8"))
            ax.add_patch(patches.FancyBboxPatch((5.85, 0.75), 3.4, 3.5, boxstyle="round,pad=0.03,rounding_size=0.25", facecolor="#FFFFFF", edgecolor="#4285F4", linewidth=1.4))
            ax.add_patch(patches.Rectangle((6.05, 0.9), 3.0, 0.9, facecolor="#34A853", edgecolor="none"))
            ax.add_patch(patches.Circle((7.55, 2.65), 0.85, facecolor="#EA4335", edgecolor="none"))
            ax.add_patch(patches.Ellipse((7.95, 3.55), 0.7, 0.35, angle=20, facecolor="#34A853", edgecolor="none"))
            ax.text(7.55, 0.36, "Foto Penuh Warna", ha="center", fontsize=8.8, color="#1A73E8", fontweight="bold")
        elif idx == 2:
            # Checkerboard RGBA
            cx0, cy0, cell = 0.65, 0.95, 0.55
            for r in range(6):
                for c in range(7):
                    col = "#E8EAED" if (r + c) % 2 == 0 else "#FFFFFF"
                    ax.add_patch(patches.Rectangle((cx0 + c * cell, cy0 + r * cell), cell, cell, facecolor=col, edgecolor="none"))
            ax.add_patch(patches.Rectangle((cx0, cy0), 7 * cell, 6 * cell, facecolor="none", edgecolor="#8A5700", linewidth=1.2))
            pts = []
            for ii in range(10):
                ang = np.pi / 2 + ii * np.pi / 5
                rr = 1.05 if ii % 2 == 0 else 0.46
                pts.append((cx0 + 3.5 * cell + rr * np.cos(ang), cy0 + 3.0 * cell + rr * np.sin(ang)))
            ax.add_patch(patches.Polygon(pts, facecolor="#FBBC04", edgecolor="#B06000", linewidth=1.5))
            ax.text(2.55, 0.40, "RGBA (PNG Transparan)", ha="center", fontsize=8.6, fontweight="bold", color="#8A5700")
            # CMYK printer ink circles
            ax.add_patch(patches.FancyBboxPatch((5.0, 0.95), 4.3, 3.3, boxstyle="round,pad=0.03,rounding_size=0.22", facecolor="#FFFFFF", edgecolor="#FDE293", linewidth=1.4))
            for cx, cy, lbl, col, tcol in [
                (6.2, 3.15, "C", "#00B8D4", "#FFFFFF"),
                (8.1, 3.15, "M", "#E91E63", "#FFFFFF"),
                (6.2, 1.80, "Y", "#FDD835", "#202124"),
                (8.1, 1.80, "K", "#202124", "#FFFFFF"),
            ]:
                ax.add_patch(patches.Circle((cx, cy), 0.56, facecolor=col, edgecolor="none"))
                ax.text(cx, cy, lbl, ha="center", va="center", fontsize=12, fontweight="bold", family="monospace", color=tcol)
            ax.text(7.15, 0.40, "CMYK (Tinta Cetak)", ha="center", fontsize=8.6, fontweight="bold", color="#8A5700")
        else:
            for k, (lbl, fcol, ecol, y0) in enumerate([
                ("Red", "#FCE8E6", "#EA4335", 3.55),
                ("Green", "#E6F4EA", "#34A853", 2.85),
                ("Blue", "#E8F0FE", "#4285F4", 2.15),
                ("NIR (Inframerah)", "#F3E8FD", "#9334E6", 1.45),
                ("Thermal (Suhu)", "#FEF7E0", "#E37400", 0.75),
            ]):
                ax.add_patch(patches.FancyBboxPatch((0.6 + k * 0.14, y0), 3.4, 0.55, boxstyle="round,pad=0.02,rounding_size=0.14", facecolor=fcol, edgecolor=ecol, linewidth=1.3))
                ax.text(2.3 + k * 0.14, y0 + 0.27, lbl, ha="center", va="center", fontsize=8.2, fontweight="bold", family="monospace", color=ecol)
            ax.add_patch(patches.FancyBboxPatch((5.15, 0.75), 4.2, 3.55, boxstyle="round,pad=0.03,rounding_size=0.25", facecolor="#1B3A4B", edgecolor="#34A853", linewidth=1.4))
            ax.add_patch(patches.Polygon([(5.2, 0.8), (9.3, 0.8), (9.3, 2.3), (7.5, 2.6), (5.2, 2.0)], facecolor="#34A853", alpha=0.85))
            ax.plot([5.2, 6.8, 8.2, 9.3], [2.9, 3.2, 2.7, 3.4], color="#8AB4F8", lw=3)
            ax.add_patch(patches.Circle((8.1, 3.55), 0.42, facecolor="#FBBC04", alpha=0.85))
            ax.add_patch(patches.Circle((8.1, 3.55), 0.20, facecolor="#EA4335", alpha=0.95))
            ax.text(7.25, 0.36, "Peta Vegetasi & Suhu", ha="center", fontsize=8.8, fontweight="bold", color="#137333")
    fig.tight_layout(pad=0.4)
    fig.savefig(p12, dpi=200, facecolor="#FFFFFF")
    plt.close(fig)
    paths["channels_overview"] = p12

    mnist_png = ASSETS_DIR / "mnist_grid_demo.png"
    if mnist_png.exists():
        paths["mnist"] = mnist_png

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
        "Deep Learning Track · Session P01 · 120 menit",
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
        "Fase Fondasi  ·  Mengubah Foto Mentah Menjadi Data Siap Latih\nFondasi sebelum masuk ke Neural Network & CNN",
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
Selamat datang di Sesi P01: Understanding Images, Image Processing, dan Exploratory Data Analysis (EDA). Hari ini kita masuk ke fase Fondasi untuk project klasifikasi karakter Disney kita nanti.

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
Format ini akan konsisten di seluruh pertemuan P01 sampai P08 agar ritme belajar terasa terstruktur.

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
        """Alokasi waktu: 2 menit

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
        """Alokasi waktu: 2 menit

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
        "Piksel, AI Fundamental, Preprocessing & EDA",
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
        """Alokasi waktu: 1 menit

Naskah ajar:
Ini adalah contoh grid 8 kali 8 piksel. Di sebelah kiri terlihat kotak-kotak gambar, dan di sebelah kanan adalah angka sebenarnya di balik setiap kotak.

Penjelasan konsep:
Setiap kotak disebut piksel (picture element). Pada gambar grayscale standar, angka 0 berarti hitam pekat dan 255 berarti putih terang.

Transisi:
Mari kita lihat langsung contoh dataset nyata paling legendaris yang dipakai di video 3Blue1Brown: MNIST!""",
    )

    # =======================================================================
    # SLIDE 07 — STUDI KASUS KLASIK: DATASET ASLI MNIST (28x28)
    # =======================================================================
    s_mnist = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s_mnist, "TEORI · STUDI KASUS KLASIK", "Dataset Asli MNIST (28×28 Grayscale)")
    if "mnist" in vis:
        s_mnist.shapes.add_picture(str(vis["mnist"]), Inches(0.75), Inches(1.58), width=Inches(11.83))
    st.add_card(
        s_mnist,
        st.MARGIN_X,
        Inches(5.35),
        st.CONTENT_WIDTH,
        Inches(1.35),
        body="Dataset MNIST (tulisan tangan 0–9, tersedia di data/mnist/) berukuran 28 × 28 × 1 = 784 angka grayscale. Bandingkan dengan foto RGB proyek kita (224 × 224 × 3 = 150.528 angka — 192× lebih besar!).",
        bg_color=st.SURFACE_BG,
        accent_color=st.BLUE,
        body_size=Pt(22),
    )
    st.add_footer(s_mnist, 7, SESSION_LABEL)
    st.set_speaker_notes(
        s_mnist,
        """Alokasi waktu: 2 menit

Naskah ajar:
Dataset MNIST ini adalah contoh paling original bagi pemula Deep Learning, dan sama persis dengan yang dibahas di video 3Blue1Brown. Perhatikan angka '7' asli di sebelah kanan: di tepian goresan pena terdapat gradasi angka abu-abu alami seperti 37, 91, hingga 254.

Penjelasan konsep:
Satu gambar MNIST berukuran 28×28×1 (784 angka). Foto berwarna proyek kita berukuran 224×224×3 (150.528 angka), namun prinsipnya sama persis: matriks angka!

Transisi:
Mengapa ada foto yang 1 channel (seperti MNIST) dan ada yang 3 channel berwarna? Mari kita bandingkan.""",
    )

    # =======================================================================
    # SLIDE 07 — PENGANTAR COLOR CHANNELS (1, 3, 4, 5+)
    # =======================================================================
    s7 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s7, "TEORI · COLOR CHANNELS", "Jenis Gambar: Color Channels (1, 3, 4, 5+)")
    s7.shapes.add_picture(str(vis["channels_overview"]), Inches(0.65), Inches(1.58), width=Inches(8.15))
    st.add_card(
        s7,
        Inches(8.98),
        Inches(1.58),
        Inches(3.70),
        Inches(2.45),
        title="Fokus Kita: 3 Ch (RGB)",
        body="Foto HP & model AI fokus ke RGB (3 angka/pixel). Selain RGB ada HSV, LAB, & YCbCr.",
        bg_color=st.TINT_BLUE,
        accent_color=st.BLUE,
        title_size=Pt(21),
        body_size=Pt(18),
        border_color=None,
    )
    st.add_callout_box(
        s7,
        Inches(8.98),
        Inches(4.22),
        Inches(3.70),
        Inches(2.25),
        "1 Ch (Grayscale) = MNIST & X-ray.\n4 Ch = PNG & cetak.\n5+ Ch = Citra satelit.",
        accent_color=st.GREEN,
        bg_color=st.TINT_GREEN,
        font_size=Pt(17),
        bold=True,
    )
    st.add_footer(s7, 7, SESSION_LABEL)
    st.set_speaker_notes(
        s7,
        """Alokasi waktu: 1 menit

Naskah ajar:
Berdasarkan color channel-nya, gambar dibagi menjadi: 1 channel (Grayscale, seperti MNIST atau foto rontgen), 3 channels (RGB yang paling umum untuk foto — selain palet warna 3-channel lain seperti HSV atau YCbCr), 4 channels (RGBA transparan PNG & CMYK untuk cetak), hingga 5+ channels (citra satelit multispectral/inframerah).

Penjelasan konsep:
Di antara semuanya, gambar foto sehari-hari dan model AI pengenalan objek paling banyak berfokus pada format 3 channels RGB agar informasi warna objek tidak hilang.

Transisi:
Mari kita bedah lebih dalam cara kerja 3 channel RGB tersebut.""",
    )

    # =======================================================================
    # SLIDE 08 — RGB CHANNELS
    # =======================================================================
    s8 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s8, "TEORI · RGB", "RGB: Tiga Channel, Tiga Informasi")
    s8.shapes.add_picture(str(vis["rgb_channels"]), Inches(0.75), Inches(1.75), width=Inches(11.83))
    st.add_card(
        s8,
        st.MARGIN_X,
        Inches(5.35),
        st.CONTENT_WIDTH,
        Inches(1.35),
        body="Setiap piksel RGB adalah kombinasi 3 angka: (Red, Green, Blue). Objek merah menyala terang di channel R, tapi gelap di G dan B.",
        bg_color=st.SURFACE_BG,
        accent_color=st.RED,
        body_size=Pt(24),
    )
    st.add_footer(s8, 8, SESSION_LABEL)
    st.set_speaker_notes(
        s8,
        """Alokasi waktu: 2 menit

Naskah ajar:
Perhatikan contoh data sampel persegi merah ini. Ketika kita pisah menjadi 3 channel terpisah, di channel Red (R) kotak perseginya terlihat putih terang (nilainya tinggi), sedangkan di channel Green (G) dan Blue (B) kotaknya gelap (nilainya rendah).

Penjelasan konsep:
Inilah cara CNN nanti membaca warna: setiap filter konvolusi melihat kombinasi nilai dari ketiga channel ini secara bersamaan.

Transisi:
Bagaimana komputer mengubah kembali angka RGB menjadi cahaya di layar HP? Mari kita lihat!""",
    )

    # =======================================================================
    # SLIDE 10 — CARA KOMPUTER MENAMPILKAN GAMBAR KE LAYAR (SYNCED HTML SLIDE 09)
    # =======================================================================
    s_disp = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(
        s_disp,
        "TEORI · LAYAR & SUB-PIXEL",
        "Cara Komputer Menampilkan Gambar ke Layar",
    )
    if "screen_display" in vis:
        s_disp.shapes.add_picture(str(vis["screen_display"]), st.MARGIN_X, Inches(1.58), width=st.CONTENT_WIDTH)
    st.add_callout_box(
        s_disp,
        st.MARGIN_X,
        Inches(5.65),
        st.CONTENT_WIDTH,
        Inches(1.05),
        "Intinya: Setiap 1 pixel di layar HP hanyalah 3 lampu mikro Red, Green, Blue yang kecerahannya diatur oleh angka 0–255.",
        accent_color=st.GREEN,
        bg_color=st.TINT_GREEN,
        font_size=Pt(20),
        bold=True,
    )
    st.add_footer(s_disp, 10, SESSION_LABEL)
    st.set_speaker_notes(
        s_disp,
        """Alokasi waktu: 2 menit

Naskah ajar:
Proses kebalikan dari membaca gambar: untuk menampilkan apel merah di layar HP, komputer membaca paket angka [234, 67, 53] dari memori, lalu menyalakan 3 lampu kecil sub-pixel (Red 92%, Green 26%, Blue 21%).

Penjelasan konsep:
Karena jutaan kotak lampu RGB ini tersusun sangat rapat, mata kita memadukan titik-titik cahaya tersebut dan langsung melihat foto apel utuh yang halus.

Transisi:
Sekarang setelah paham piksel, 3 channel RGB, dan cara layar menampilkannya, berapa total angka dalam satu foto standar 224×224?""",
    )

    # =======================================================================
    # SLIDE 11 — IMAGE SHAPE (Reordered after Pixel & RGB)
    # =======================================================================
    s9 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s9, "TEORI · DIMENSI ARRAY", "Setiap Foto Punya Shape")
    st.add_card(
        s9,
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
    st.add_card(
        s9,
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
        s9,
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
            s9,
            Inches(8.35),
            Inches(1.75) + i * Inches(1.62),
            Inches(4.23),
            Inches(1.42),
            title=desc,
            bg_color=st.SURFACE_BG,
            accent_color=col,
            title_size=Pt(24),
        )
    st.add_footer(s9, 9, SESSION_LABEL)
    st.set_speaker_notes(
        s9,
        """Alokasi waktu: 2 menit

Naskah ajar:
Setiap foto di NumPy direpresentasikan sebagai array 3 dimensi yang disebut shape. Untuk input standar MobileNetV2, ukurannya adalah 224 kali 224 kali 3, yang berarti ada 150.528 angka dalam satu foto saja!

Penjelasan konsep:
Urutan di Python/NumPy adalah (Height, Width, Channels): tinggi dulu (baris), baru lebar (kolom), lalu jumlah channel warna. Kita cukup memanggil `img.shape` untuk memeriksanya.

Transisi:
Bagaimana cara komputer mengenali karakter dari 150.528 angka ini? Mari kita pahami peran AI terlebih dahulu.""",
    )

    # =======================================================================
    # SLIDE 10 — AI FUNDAMENTAL (1/3): APA ITU AI, ML & DEEP LEARNING?
    # =======================================================================
    s10 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s10, "TEORI · AI FUNDAMENTAL (1/3)", "Apa Itu AI di Project Ini?")
    ai_cards = [
        (
            "1",
            "Program Biasa (Rule-Based)",
            "Manusia menulis aturan if-else manual. Mudah untuk rumus pasti, tapi mustahil untuk 150.528 piksel foto.",
            st.RED,
            st.TINT_RED,
        ),
        (
            "2",
            "Machine Learning (ML)",
            "Manusia memilihkan ciri/fitur foto secara manual (sudut, warna, ukuran), lalu mesin belajar dari tabel fitur itu.",
            st.BLUE,
            st.TINT_BLUE,
        ),
        (
            "3",
            "Deep Learning (CNN)",
            "Foto mentah langsung masuk tanpa pilih ciri manual! Lapisan saraf otomatis mencari tepi, bentuk, hingga objek utuh.",
            st.GREEN,
            st.TINT_GREEN,
        ),
    ]
    for idx, (num, ttl, desc, acc, tint) in enumerate(ai_cards):
        st.add_card(
            s10,
            st.MARGIN_X + idx * Inches(4.02),
            Inches(1.75),
            Inches(3.78),
            Inches(3.55),
            title=ttl,
            body=desc,
            bg_color=tint,
            accent_color=acc,
            badge_text=num,
            title_size=Pt(23),
            body_size=Pt(20),
            border_color=None,
        )
    st.add_callout_box(
        s10,
        st.MARGIN_X,
        Inches(5.50),
        st.CONTENT_WIDTH,
        Inches(1.22),
        "Hirarki: Artificial Intelligence (AI)  ⊃  Machine Learning (ML)  ⊃  Deep Learning (CNN — fokus project kita).",
        accent_color=st.BLUE,
        bg_color=st.TINT_BLUE,
        font_size=Pt(20),
        bold=True,
    )
    st.add_footer(s10, 10, SESSION_LABEL)
    st.set_speaker_notes(
        s10,
        """Alokasi waktu: 2 menit

Naskah ajar:
Sekarang kita sudah tahu bahwa satu foto hanyalah 150.528 angka piksel. Pertanyaannya: bagaimana komputer tahu itu foto Mickey atau Donald? Di sinilah bedanya Program Biasa dengan AI. Pada program biasa, programmer menulis aturan if-else. Pada Machine Learning dan khususnya Deep Learning (CNN), komputer belajar mencari pola sendiri dari contoh foto yang kita berikan.

Penjelasan konsep:
Deep Learning adalah cabang Machine Learning yang menggunakan jaringan saraf tiruan berlapis untuk mengenali pola visual bertingkat langsung dari piksel mentah.

Transisi:
Mengapa kita tidak bisa memakai aturan if-else biasa saja untuk mengenali foto? Mari kita buktikan di slide berikutnya.""",
    )

    # =======================================================================
    # SLIDE 11 — AI FUNDAMENTAL (2/3): MENGAPA WAJIB PAKAI AI?
    # =======================================================================
    s11 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s11, "TEORI · AI FUNDAMENTAL (2/3)", "Mengapa Mengenali Foto Wajib Pakai AI?")
    why_cards = [
        (
            "1",
            "Posisi & Sudut Berubah",
            "Objek digeser sedikit saja ke pojok atau miring 15°, koordinat angka pikselnya berubah total.",
            st.RED,
            st.TINT_RED,
        ),
        (
            "2",
            "Cahaya & Latar Ramai",
            "Foto di tempat redup atau berlatar ramai mengubah ratusan ribu nilai RGB sekaligus.",
            st.YELLOW,
            st.TINT_YELLOW,
        ),
        (
            "3",
            "Solusi Deep Learning",
            "Filter CNN memindai seluruh area gambar sehingga tetap mengenali bentuk objek di mana pun posisinya.",
            st.GREEN,
            st.TINT_GREEN,
        ),
    ]
    for idx, (num, ttl, desc, acc, tint) in enumerate(why_cards):
        st.add_card(
            s11,
            st.MARGIN_X + idx * Inches(4.02),
            Inches(1.75),
            Inches(3.78),
            Inches(3.55),
            title=ttl,
            body=desc,
            bg_color=tint,
            accent_color=acc,
            badge_text=num,
            title_size=Pt(23),
            body_size=Pt(20),
            border_color=None,
        )
    st.add_callout_box(
        s11,
        st.MARGIN_X,
        Inches(5.50),
        st.CONTENT_WIDTH,
        Inches(1.22),
        "Aturan if-else kaku pada koordinat piksel pasti gagal saat objek bergeser; AI belajar pola bentuk & tekstur yang fleksibel.",
        accent_color=st.RED,
        bg_color=st.TINT_RED,
        font_size=Pt(20),
        bold=True,
    )
    st.add_footer(s11, 11, SESSION_LABEL)
    st.set_speaker_notes(
        s11,
        """Alokasi waktu: 2 menit

Naskah ajar:
Bayangkan kita membuat aturan manual: 'Jika piksel tengah (112, 112) berwarna hitam, maka itu Mickey'. Begitu boneka Mickey digeser sedikit ke kanan, dipotret miring, atau berada di latar belakang yang ramai, aturan if-else tadi langsung gagal total!

Penjelasan konsep:
Di notebook nanti kita akan membuktikan lewat kode bagaimana menggeser gambar mengubah nilai piksel di koordinat tetap, dan mengapa kita membutuhkan AI yang memindai pola bentuk di seluruh gambar.

Transisi:
Lalu bagaimana alur kerja penggunaan AI di project kita dari awal sampai akhir, dan di mana posisi sesi P01 ini?""",
    )

    # =======================================================================
    # SLIDE 12 — AI FUNDAMENTAL (3/3): ALUR KERJA AI DI PROJECT KITA
    # =======================================================================
    s12 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s12, "TEORI · AI FUNDAMENTAL (3/3)", "Alur Kerja AI & Peran Krusial P01")
    workflow_cards = [
        (
            "1",
            "Tahap 1: Siapkan Foto (P01)",
            "Seragamkan ukuran, tegakkan posisi, dan saring file rusak agar bahan foto siap latih.",
            st.BLUE,
            st.TINT_BLUE,
        ),
        (
            "2",
            "Tahap 2: Latih Model AI",
            "Model AI mempelajari pola bentuk & warna dengan tenang dari koleksi foto bersih dan seimbang.",
            st.YELLOW,
            st.TINT_YELLOW,
        ),
        (
            "3",
            "Tahap 3: Tebak Foto Baru",
            "Saat diberi foto baru dari HP, AI mampu menebak karakternya dengan tepat & konsisten!",
            st.GREEN,
            st.TINT_GREEN,
        ),
    ]
    for idx, (num, ttl, desc, acc, tint) in enumerate(workflow_cards):
        st.add_card(
            s12,
            st.MARGIN_X + idx * Inches(4.02),
            Inches(1.75),
            Inches(3.78),
            Inches(3.55),
            title=ttl,
            body=desc,
            bg_color=tint,
            accent_color=acc,
            badge_text=num,
            title_size=Pt(23),
            body_size=Pt(20),
            border_color=None,
        )
    st.add_callout_box(
        s12,
        st.MARGIN_X,
        Inches(5.50),
        st.CONTENT_WIDTH,
        Inches(1.22),
        "Prinsip Garbage In, Garbage Out: AI secanggih apa pun akan gagal jika dilatih dengan foto mentah yang rusak, gepeng, atau bocor!",
        accent_color=st.GREEN,
        bg_color=st.TINT_GREEN,
        font_size=Pt(20),
        bold=True,
    )
    st.add_footer(s12, 12, SESSION_LABEL)
    st.set_speaker_notes(
        s12,
        """Alokasi waktu: 2 menit

Naskah ajar:
Menggunakan AI itu ibarat memasak di dapur profesional. Model AI (CNN) adalah kompor canggihnya, sedangkan foto adalah bahan makanannya. Sesi P01 hari ini adalah tahap menyiapkan dan memeriksa bahan: membersihkan data yang rusak, menyeragamkan ukuran, dan menormalisasi angka.

Penjelasan konsep:
Prinsip utamanya adalah Garbage In, Garbage Out. Jika data yang masuk berantakan, hasil prediksi AI juga pasti berantakan.

Transisi:
Sekarang kita tahu mengapa data harus disiapkan untuk AI. Mari kita bahas langkah teknis pertamanya: tipe data uint8 vs float32!""",
    )

    # =======================================================================
    # SLIDE 13 — DATA TYPES
    # =======================================================================
    s13 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s13, "TEORI · TIPE DATA", "Kenali Tipe Data Gambar")
    st.add_pill_tag(s13, "uint8  →  0–255", st.MARGIN_X, Inches(1.68), bg_color=st.TINT_BLUE, text_color=st.BLUE_TEXT, width=Inches(3.4), height=Inches(0.52), size=Pt(21))
    st.add_card(
        s13,
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
    st.add_pill_tag(s13, "float32  →  0.0–1.0", Inches(6.88), Inches(1.68), bg_color=st.TINT_GREEN, text_color=st.TEXT_DARK, width=Inches(3.8), height=Inches(0.52), size=Pt(21))
    st.add_card(
        s13,
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
        s13,
        st.MARGIN_X,
        Inches(5.60),
        st.CONTENT_WIDTH,
        Inches(1.12),
        bg_color=st.DARK_BG,
        border_color=None,
    )
    st.add_text_box(
        s13,
        st.MARGIN_X + Inches(0.28),
        Inches(5.76),
        st.CONTENT_WIDTH - Inches(0.56),
        Inches(0.85),
        "arr_float = arr_uint8.astype('float32') / 255.0   # konversi aman ke 0.0–1.0",
        font_name=st.FONT_CODE,
        size=Pt(20),
        color=st.TEXT_LIGHT,
    )
    st.add_footer(s13, 13, SESSION_LABEL)
    st.set_speaker_notes(
        s13,
        """Alokasi waktu: 1 menit

Naskah ajar:
Saat foto dibuka dari disk, tipenya adalah `uint8` (unsigned integer 8-bit) dengan rentang 0 sampai 255. Tapi sebelum masuk ke neural network, kita ubah menjadi `float32` karena perhitungan bobot dan gradien membutuhkan angka desimal.

Penjelasan konsep:
Jika kita membagi `uint8` langsung tanpa mengubah ke float atau membagi dengan 255.0, hasilnya bisa terpotong menjadi integer.

Transisi:
Selain tipe data, ukuran foto dari kamera HP juga berbeda-beda. Bagaimana cara menyamakan ukurannya?""",
    )

    # =======================================================================
    # SLIDE 14 — RESIZE & ASPECT RATIO
    # =======================================================================
    s14 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s14, "TEORI · UKURAN INPUT", "Resize Tanpa Merusak Proporsi")
    s14.shapes.add_picture(str(vis["resize"]), Inches(1.55), Inches(1.62), height=Inches(3.62))
    st.add_card(
        s14,
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
    st.add_footer(s14, 14, SESSION_LABEL)
    st.set_speaker_notes(
        s14,
        """Alokasi waktu: 2 menit

Naskah ajar:
Foto dari HP biasanya punya rasio 4:3 atau 16:9, sedangkan MobileNetV2 membutuhkan input bujur sangkar 224 kali 224. Jika langsung di-resize paksa, lingkaran menjadi lonjong! Solusinya adalah menjaga aspect ratio dengan padding (letterbox) atau center crop yang aman.

Penjelasan konsep:
Model CNN tidak bisa menerima ukuran gambar yang berubah-ubah dalam satu batch, jadi ukuran input wajib seragam.

Transisi:
Ukuran sudah seragam 224×224. Bagaimana dengan skala angkanya?""",
    )

    # =======================================================================
    # SLIDE 15 — NORMALIZATION
    # =======================================================================
    s15 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s15, "TEORI · PREPROCESSING (PREVIEW P7)", "Skala Angka Harus Konsisten")
    st.add_card(
        s15,
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
        s15,
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
    st.add_pill_tag(s15, "PREVIEW P7", st.MARGIN_X, Inches(5.05), bg_color=st.TINT_YELLOW, text_color=st.TEXT_DARK, width=Inches(1.85), height=Inches(0.5), size=Pt(18))
    st.add_card(
        s15,
        st.MARGIN_X + Inches(2.05),
        Inches(5.02),
        st.CONTENT_WIDTH - Inches(2.05),
        Inches(1.42),
        bg_color=st.DARK_BG,
        border_color=None,
    )
    st.add_text_box(
        s15,
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
    st.add_footer(s15, 15, SESSION_LABEL)
    st.set_speaker_notes(
        s15,
        """Alokasi waktu: 2 menit

Naskah ajar:
Angka 0–255 terlalu besar untuk pelatihan neural network yang stabil, jadi kita lakukan normalisasi. Ada dua skala yang sering dipakai: 0 sampai 1, atau −1 sampai 1. Khusus untuk MobileNetV2 yang akan kita pakai di P7 nanti, fungsi `preprocess_input` mengubah skala piksel menjadi kira-kira −1 sampai 1.

Penjelasan konsep:
Ini adalah preview untuk P7. Kita tidak perlu menghafal rumusnya, cukup panggil `preprocess_input` bawaan MobileNetV2 agar sesuai dengan bobot ImageNet-nya.

Transisi:
Ada satu aturan emas tentang preprocessing ini yang wajib diingat selamanya.""",
    )

    # =======================================================================
    # SLIDE 16 — KEYNOTE MOMENT
    # =======================================================================
    s16 = st.add_keynote_slide(
        prs,
        "ATURAN EMAS PREPROCESSING",
        "Preprocessing saat training =\npreprocessing saat prediksi.",
        "Salah skala antara training dan inferensi akan membuat akurasi model anjlok.",
        bg_color=st.DARK_BG,
        slide_number=16,
        session_label=SESSION_LABEL,
    )
    st.set_speaker_notes(
        s16,
        """Alokasi waktu: 1 menit

Naskah ajar:
Ingat satu kalimat ini: Preprocessing saat training harus sama persis dengan preprocessing saat prediksi! Jika saat training model menerima angka −1 sampai 1, lalu saat demo kita memberi angka 0 sampai 255, model akan kebingungan dan menebak acak.

Penjelasan konsep:
Ini adalah salah satu bug paling sering terjadi di dunia nyata saat deployment model computer vision.

Transisi:
Sekarang kita beralih dari menyiapkan satu foto ke memahami keseluruhan dataset foto melalui EDA.""",
    )

    # =======================================================================
    # SLIDE 17 — HISTOGRAM, BRIGHTNESS & CONTRAST (SYNCED HTML SLIDE 33 & 34)
    # =======================================================================
    s17 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s17, "TEORI · EDA ISSUE #2 (PENCAHAYAAN & KONTRAS)", "Issue #2 EDA: Histogram, Brightness & Contrast")
    s17.shapes.add_picture(str(vis["histogram"]), Inches(0.85), Inches(1.58), width=Inches(11.6))
    st.add_card(
        s17,
        st.MARGIN_X,
        Inches(5.45),
        st.CONTENT_WIDTH,
        Inches(1.25),
        body="Brightness (Mean: Polos 228.11 vs Ramai 127.21) mengukur terang keseluruhan foto (pixel + ΔB). Contrast (Std: Polos 45.21 vs Ramai 54.69) mengukur ketajaman jarak gelap-terang ((pixel − mean) × C).",
        bg_color=st.SURFACE_BG,
        accent_color=st.BLUE,
        body_size=Pt(20),
    )
    st.add_footer(s17, 17, SESSION_LABEL)
    st.set_speaker_notes(
        s17,
        """Alokasi waktu: 2 menit

Naskah ajar:
Histogram menunjukkan seberapa banyak piksel pada setiap tingkat kecerahan 0 sampai 255. Pada contoh data sampel kita: gambar polos punya puncak sempit di area terang (background seragam), sedangkan gambar ramai sebarannya jauh lebih melebar karena banyak objek dan warna latar.

Penjelasan konsep:
Dari histogram kita menghitung dua angka ringkas: Mean intensitas untuk brightness, dan Simpangan Baku (std) untuk kontras.

Transisi:
Selain histogram, apa saja yang perlu kita cek saat melakukan EDA dataset?""",
    )

    # =======================================================================
    # SLIDE 18 — EXPLORATORY DATA ANALYSIS (3-column table + imbalance callout)
    # =======================================================================
    s18 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s18, "TEORI · EDA DESKRIPTIF (ISSUE #1–#3)", "Kenali 3 Issue Utama Sebelum Modeling")
    st.add_styled_table(
        s18,
        st.MARGIN_X,
        Inches(1.58),
        st.CONTENT_WIDTH,
        Inches(3.8),
        headers=["Issue EDA", "Yang Dilihat", "Mengapa Penting"],
        rows=[
            ["Issue #1 · Imbalance", "Jumlah foto per kelas × kondisi", "Cegah model bias ke kelas terbanyak"],
            ["Issue #2 · Pencahayaan", "Histogram, Brightness & Contrast", "Cek foto terlalu gelap / silau"],
            ["Issue #3 · Latar Ramai", "Edge density & latar polos vs ramai", "Cegah AI menghafal latar belakang"],
            ["Cek Tambahan · Bab 4", "Resolusi, file rusak, EXIF & duplikat", "Pastikan input bersih & valid"],
        ],
        col_widths=[Inches(3.3), Inches(4.4), Inches(4.13)],
        header_color=st.BLUE,
        font_size=Pt(21),
        header_size=Pt(22),
    )
    st.add_callout_box(
        s18,
        st.MARGIN_X,
        Inches(5.58),
        st.CONTENT_WIDTH,
        Inches(1.18),
        "Class imbalance: jika 1 karakter punya 100 foto tapi karakter lain hanya 15 foto, model cenderung bias ke kelas mayoritas. EDA membantu menemukan ini sebelum melatih model (skenario S1 & S2).",
        accent_color=st.RED,
        bg_color=st.TINT_RED,
        font_size=Pt(19),
    )
    st.add_footer(s18, 18, SESSION_LABEL)
    st.set_speaker_notes(
        s18,
        """Alokasi waktu: 2 menit

Naskah ajar:
EDA itu ibarat memeriksa bahan masakan sebelum mulai memasak. Ada 4 hal utama yang kita periksa: distribusi jumlah foto (untuk mendeteksi class imbalance), resolusi gambar, karakteristik pencahayaan (brightness & contrast), dan kompleksitas latar belakang (edge density).

Penjelasan konsep:
Class imbalance terjadi jika satu karakter punya 100 foto sementara karakter lain hanya 15 foto; model bisa cenderung menebak kelas yang jumlahnya banyak.

Transisi:
Mari kita lihat lebih dekat ukuran keempat: bagaimana cara mengukur 'keramaian' background?""",
    )

    # =======================================================================
    # SLIDE 19 — EDGE DENSITY
    # =======================================================================
    s19 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s19, "TEORI · EDA ISSUE #3 (LATAR RAMAI)", "Issue #3 EDA: Seberapa Ramai Background-nya?")
    s19.shapes.add_picture(str(vis["edge_density"]), Inches(0.85), Inches(1.58), width=Inches(11.6))
    polos_ed = stats["by_condition"]["polos"]["mean_edge_density"]
    ramai_ed = stats["by_condition"]["ramai"]["mean_edge_density"]
    st.add_callout_box(
        s19,
        st.MARGIN_X,
        Inches(5.38),
        st.CONTENT_WIDTH,
        Inches(1.38),
        f"edge_density = jumlah_piksel_tepi / total_piksel (Canny). Contoh data sampel: polos = {polos_ed:.4f}, ramai = {ramai_ed:.4f}.\nCatatan: edge density & entropy adalah proxy kompleksitas visual background, bukan ukuran langsung kesulitan model.",
        accent_color=st.RED,
        bg_color=st.TINT_RED,
        font_size=Pt(19),
    )
    st.add_footer(s19, 19, SESSION_LABEL)
    st.set_speaker_notes(
        s19,
        f"""Alokasi waktu: 2 menit

Naskah ajar:
Kita memakai algoritma Canny Edge Detection untuk mencari garis-garis tepi pada gambar, lalu menghitung rasio piksel tepi terhadap total piksel. Pada 119 foto valid contoh data sampel kita, rata-rata edge density kondisi polos adalah {polos_ed:.4f}, sedangkan kondisi ramai jauh lebih tinggi yaitu {ramai_ed:.4f}.

Penjelasan konsep:
Penting dicatat: edge density hanyalah proxy (pendekatan) untuk kompleksitas visual background, bukan ukuran langsung seberapa sulit model akan belajar.

Transisi:
Terakhir di bagian teori, mari waspadai 3 jebakan klasik saat mengumpulkan dataset foto sendiri.""",
    )

    # =======================================================================
    # SLIDE 20 — THREE COMMON DATA TRAPS
    # =======================================================================
    s20 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s20, "TEORI · KUALITAS DATA", "Tiga Jebakan dalam Dataset")
    traps = [
        ("1", "Orientasi EXIF", "Foto HP sering tersimpan miring meski tampak tegak di galeri.", st.YELLOW, st.TINT_YELLOW),
        ("2", "Foto kembar / burst", "Foto identik atau nyaris sama bisa bocor ke train & test.", st.RED, st.TINT_RED),
        ("3", "Data leakage", "EDA bersifat deskriptif: jangan memilih data berdasarkan test set!", st.BLUE, st.TINT_BLUE),
    ]
    for idx, (num, ttl, desc, acc, tint) in enumerate(traps):
        st.add_card(
            s20,
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
    s20.shapes.add_picture(str(vis["exif"]), Inches(0.75), Inches(5.45), height=Inches(1.48))
    st.add_text_box(
        s20,
        Inches(3.9),
        Inches(5.65),
        Inches(8.6),
        Inches(1.1),
        f"Pada contoh data sampel (120 file): ditemukan {stats['exif_orientation_6_count']} foto EXIF=6, {stats['duplicate_file_count']} file duplikat identik, dan {stats['corrupted_count']} file rusak.",
        font_name=st.FONT_BODY,
        size=Pt(22),
        color=st.TEXT_DARK,
    )
    st.add_footer(s20, 20, SESSION_LABEL)
    st.set_speaker_notes(
        s20,
        """Alokasi waktu: 2 menit

Naskah ajar:
Ada tiga jebakan yang harus kita tangkap di notebook nanti. Pertama, tag EXIF Orientation=6 membuat foto terputar 90 derajat saat dibaca mentah (lihat contoh di kiri bawah). Kedua, foto kembar/burst yang dicek dengan hash. Ketiga, data leakage: ingat, EDA bersifat deskriptif saja; kita tidak boleh membuang atau memilih data berdasarkan hasil test set.

Penjelasan konsep:
Setelah ini kita istirahat 5 menit (menit 40–45) sebelum masuk ke sesi Hands-on notebook.

Transisi:
Sampai ketemu 5 menit lagi untuk praktik langsung di notebook!""",
    )

    # =======================================================================
    # SLIDE 21 — HANDS-ON SECTION DIVIDER (6 steps aligned with Notebook)
    # =======================================================================
    s21 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header_rich(
        s21,
        "BAGIAN 02 · ISTIRAHAT 5 MENIT + HANDS-ON 50 MENIT (MENIT 40–95)",
        [("HANDS-ON: ", st.GREEN), ("Praktik EDA Notebook", st.TEXT_DARK)],
        kicker_color=st.GREEN,
    )
    steps_detail = [
        ("01", "Baca foto & MNIST, intip matriks piksel", "Buka foto data/sample/ & data/mnist/, cek shape & patch 8×8.", st.BLUE),
        ("02", "Pisahkan channel RGB & grayscale", "Visualisasikan channel R, G, B serta matriks 2D grayscale.", st.RED),
        ("03", "Resize proporsional & normalisasi", "Letterbox 224×224, konversi float32 (0–1) & bukti eksperimen AI.", st.YELLOW),
        ("04", "Saring 3 jebakan kamera HP", "Koreksi EXIF, verifikasi Pillow (verify), dan hash SHA-256.", st.GREEN),
        ("05", "EDA dataset: Polos vs Ramai (119 foto)", "Hitung class balance, brightness (mean), kontras (std), & Canny.", st.BLUE),
        ("06", "Simpan ringkasan audit & grafik boxplot", "Bandingkan distribusi polos vs ramai & simpan ke folder results/.", st.RED),
    ]
    st.add_numbered_steps(s21, st.MARGIN_X, Inches(1.65), Inches(7.25), steps_detail, row_height=0.86)
    st.add_card(
        s21,
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
        s21,
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
    st.add_footer(s21, 21, SESSION_LABEL)
    st.set_speaker_notes(
        s21,
        """Alokasi waktu: 55 menit (5 menit istirahat + 50 menit hands-on notebook)

Naskah ajar:
Selamat datang kembali! Selama 50 menit ke depan kita akan mengerjakan notebook P01. Ada 6 langkah berurutan yang sama persis dengan struktur sel di notebook: mulai dari membaca array gambar & koreksi EXIF, memisahkan channel RGB, melakukan resize proporsional & normalisasi + bukti eksperimen AI, menginventaris file rusak dan duplikat dengan hash SHA-256, menghitung brightness/kontras/edge density, hingga membuat boxplot perbandingan polos vs ramai.

Penjelasan konsep:
Pandu peserta mengisi bagian `# TODO` secara bertahap dan memastikan semua sel `assert` berjalan dengan benar pada data sampel.

Transisi:
Setelah statistik dan boxplot selesai dibuat, mari kita masuk ke Mini-challenge!""",
    )

    # =======================================================================
    # SLIDE 22 — MINI-CHALLENGE DIVIDER
    # =======================================================================
    s22 = st.add_blank_slide(prs, st.YELLOW)
    st.add_text_box(
        s22,
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
        s22,
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
        s22,
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
    st.add_footer(s22, 22, SESSION_LABEL, on_dark=False, fg_color=st.TEXT_DARK)
    st.set_speaker_notes(
        s22,
        """Alokasi waktu: 15 menit

Naskah ajar:
Sekarang coba lihat kembali tabel statistik dan boxplot yang baru saja kita hasilkan. Hanya dari statistik (brightness, kontras, edge density), menurutmu kondisi mana yang lebih sulit bagi model nanti: polos atau ramai? Dan mengapa?

Instruksi interaksi:
Minta peserta menuliskan alasannya secara lisan atau di catatan sebagai hipotesis awal. Jangan langsung memberi jawaban final—hipotesis ini akan diuji nanti saat evaluasi model!

Transisi:
Mari kita rangkum istilah-istilah baru yang kita pelajari hari ini di Glosarium.""",
    )

    # =======================================================================
    # SLIDE 23 — GLOSSARY
    # =======================================================================
    s23 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s23, "REFERENSI CEPAT", "Glosarium Singkat")
    glossary_items = [
        ("Piksel & Channel", "Titik terkecil gambar & lapisan warna (R, G, B)."),
        ("Shape", "Dimensi array gambar: (tinggi, lebar, channel)."),
        ("Deep Learning (AI)", "Model berlapis yang belajar pola visual dari contoh data."),
        ("uint8 & float32", "Bilangan bulat 0–255 (file) vs desimal (komputasi AI)."),
        ("Normalisasi", "Mengubah rentang nilai piksel ke skala konsisten."),
        ("EDA", "Eksplorasi awal untuk mengenali pola & kualitas data."),
        ("Edge density", "Rasio piksel tepi terhadap total piksel gambar."),
        ("Class imbalance", "Ketimpangan jumlah foto antar kelas."),
        ("Data leakage", "Kebocoran informasi test set ke proses training/keputusan."),
    ]
    st.add_styled_table(
        s23,
        st.MARGIN_X,
        Inches(1.58),
        st.CONTENT_WIDTH,
        Inches(5.2),
        headers=["Istilah", "Definisi Singkat"],
        rows=[[k, v] for k, v in glossary_items],
        col_widths=[Inches(3.2), Inches(8.63)],
        header_color=st.BLUE,
        font_size=Pt(20),
        header_size=Pt(22),
    )
    st.add_footer(s23, 23, SESSION_LABEL)
    st.set_speaker_notes(
        s23,
        """Alokasi waktu: 2 menit

Naskah ajar:
Ini adalah istilah-istilah kunci dari sesi P01 sebagai pegangan cepat, mulai dari Piksel, Shape, Deep Learning (AI), hingga Edge Density dan Data Leakage. Pastikan tidak ada istilah yang masih terasa asing sebelum kita masuk ke quiz.

Penjelasan konsep:
Tanyakan apakah ada dari istilah ini yang masih perlu diulang contohnya secara singkat.

Transisi:
Sekarang saatnya menguji pemahaman dengan 5 soal quiz singkat!""",
    )

    # =======================================================================
    # SLIDE 24 — QUIZ (5 questions, no answers on slide)
    # =======================================================================
    s24 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s24, "EVALUASI SINGKAT", "Sudah Paham? Uji Dirimu!")
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
            s24,
            st.MARGIN_X,
            top_y,
            st.CONTENT_WIDTH,
            Inches(0.88),
            bg_color=tint,
            border_color=None,
            shadow=False,
        )
        st.add_pill_tag(s24, num, st.MARGIN_X + Inches(0.22), top_y + Inches(0.20), bg_color=acc, text_color=st.TEXT_DARK if acc in (st.YELLOW, st.GREEN) else st.TEXT_LIGHT, width=Inches(0.54), height=Inches(0.48), font_name=st.FONT_TITLE, size=Pt(20))
        st.add_text_box(
            s24,
            st.MARGIN_X + Inches(0.95),
            top_y + Inches(0.20),
            st.CONTENT_WIDTH - Inches(1.2),
            Inches(0.52),
            q_txt,
            font_name=st.FONT_BODY,
            size=Pt(24),
            color=st.TEXT_DARK,
        )
    st.add_footer(s24, 24, SESSION_LABEL)
    st.set_speaker_notes(
        s24,
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
Mari kita tutup sesi hari ini dengan rangkuman dan checklist kriteria berhasil.""",
    )

    # =======================================================================
    # SLIDE 25 — CLOSING & CHECKLIST (no homework, no next-session card)
    # =======================================================================
    s25 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s25, "RANGKUMAN & PENUTUP", "Key Takeaways & Kriteria Berhasil P01")
    takeaways = [
        ("1", "Gambar adalah representasi angka", st.BLUE, st.TINT_BLUE),
        ("2", "Preprocessing harus konsisten", st.GREEN, st.TINT_GREEN),
        ("3", "EDA memahami kualitas dataset", st.RED, st.TINT_RED),
    ]
    for idx, (num, ttl, acc, tint) in enumerate(takeaways):
        st.add_card(
            s25,
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
        s25,
        st.MARGIN_X,
        Inches(3.85),
        st.CONTENT_WIDTH,
        Inches(2.8),
        headers=["Kriteria Berhasil P01", "Target Capaian Hari Ini"],
        rows=[
            ["Pahami struktur & peran AI", "Bisa jelaskan shape (224, 224, 3), uint8 vs float32, & alasan pakai AI"],
            ["Statistik dataset lengkap", "Tabel kelas × kondisi serta perbandingan polos vs ramai terbaca"],
            ["Kebersihan data terjamin", "Berhasil mendeteksi file rusak, duplikat SHA-256, & orientasi EXIF"],
        ],
        col_widths=[Inches(4.3), Inches(7.53)],
        header_color=st.DARK_BG,
        font_size=Pt(21),
        header_size=Pt(22),
    )
    st.add_footer(s25, 25, SESSION_LABEL)
    st.set_speaker_notes(
        s25,
        """Alokasi waktu: 4 menit

Naskah ajar:
Tiga hal utama yang kita bawa pulang hari ini: gambar adalah matriks angka, preprocessing harus konsisten antara training dan prediksi untuk model AI, dan EDA membantu kita memahami kualitas data sebelum melatih model. Pastikan ketiga kriteria berhasil P01 sudah tercapai di akhir sesi ini tanpa perlu tugas rumah tambahan.

Penjelasan konsep:
Dengan fondasi gambar dan EDA yang kuat dari P01 ini, seluruh pipeline pemrosesan foto untuk model deep learning kita sudah siap.

Transisi:
Terima kasih sudah mengikuti Sesi P01 dengan antusias! Di dua slide setelah ini tersedia daftar video YouTube & sumber belajar mandiri berurutan untuk memperdalam materi.""",
    )

    # =======================================================================
    # SLIDE 26 — REFERENSI BELAJAR MANDIRI (1/2)
    # =======================================================================
    s26 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s26, "REFERENSI BELAJAR MANDIRI (1/2)", "Video YouTube: Piksel, AI & Image Processing")
    st.add_styled_table(
        s26,
        st.MARGIN_X,
        Inches(1.58),
        st.CONTENT_WIDTH,
        Inches(5.15),
        headers=["Tahap & Materi", "Rekomendasi Video YouTube", "Tautan"],
        rows=[
            ["1. Piksel & Array", "3Blue1Brown — Neural Networks Ch. 1 (00:00–05:30)", "youtube.com/watch?v=aircAruvnKk"],
            ["1. Array NumPy", "Keith Galli — Complete Python NumPy Tutorial", "youtube.com/watch?v=GB9ByFAIAH4"],
            ["2. AI vs ML vs DL", "IBM Technology — AI, ML, DL & GenAI Explained", "youtube.com/watch?v=qYNweeDHiyU"],
            ["2. Deep Learning", "Simplilearn — Deep Learning In 5 Minutes", "youtube.com/watch?v=6M5VXKLf4D4"],
            ["2. Pengantar AI", "Simplilearn — What is AI? (5 Minutes · Opsional)", "youtube.com/watch?v=ad79nYk2keg"],
            ["3. Pillow (PIL)", "Corey Schafer — Image Manipulation with Pillow", "youtube.com/watch?v=6Qs3w1uYujo"],
            ["3. OpenCV Full", "freeCodeCamp — OpenCV Course Full Tutorial", "youtube.com/watch?v=oXlwWbU8l2o"],
            ["3. OpenCV Praktis", "Murtaza's Workshop — Learn OpenCV in 3 Hours", "youtube.com/watch?v=WQeoO7MI0Bs"],
        ],
        col_widths=[Inches(2.5), Inches(5.33), Inches(4.0)],
        header_color=st.BLUE,
        font_size=Pt(16),
        header_size=Pt(18),
    )
    st.add_footer(s26, 26, SESSION_LABEL)
    st.set_speaker_notes(
        s26,
        """Alokasi waktu: 0 menit

Naskah ajar:
Slide referensi belajar mandiri bagian 1/2 (untuk dipelajari di luar jam sesi). Urutan video disesuaikan mulai dari pemahaman Piksel & NumPy, AI Fundamental, hingga praktik Pillow dan OpenCV.""",
    )

    # =======================================================================
    # SLIDE 27 — REFERENSI BELAJAR MANDIRI (2/2)
    # =======================================================================
    s27 = st.add_blank_slide(prs, st.LIGHT_BG)
    st.add_slide_header(s27, "REFERENSI BELAJAR MANDIRI (2/2)", "Video & Modul: EDA, Canny Edge & Anti-Leakage")
    st.add_styled_table(
        s27,
        st.MARGIN_X,
        Inches(1.58),
        st.CONTENT_WIDTH,
        Inches(4.35),
        headers=["Tahap & Materi", "Rekomendasi Video / Sumber Belajar", "Tautan"],
        rows=[
            ["4. Filter & Kernel", "Computerphile — How Blurs & Filters Work", "youtube.com/watch?v=C_zFhWdM4ic"],
            ["4. Gradien Sobel", "Computerphile — Finding the Edges (Sobel)", "youtube.com/watch?v=uihBwtPIBxM"],
            ["4. Canny Edge", "Computerphile — Canny Edge Detector (Wajib)", "youtube.com/watch?v=sRF9t8LqXW4"],
            ["4. Kode Citra", "DigitalSreeni — Python for Microscopists", "github.com/bnsreenu/python_for_microscopists"],
            ["5. CNN Week 1", "Coursera DeepLearning.AI — CNN Course", "coursera.org/learn/convolutional-neural-networks"],
            ["5. Anti-Leakage", "Kaggle Learn — Data Leakage (Interaktif)", "kaggle.com/code/alexisbcook/data-leakage"],
            ["5. Data Leakage", "IBM — What is Data Leakage in ML?", "ibm.com/topics/data-leakage"],
        ],
        col_widths=[Inches(2.5), Inches(5.13), Inches(4.2)],
        header_color=st.RED,
        font_size=Pt(16),
        header_size=Pt(18),
    )
    st.add_callout_box(
        s27,
        st.MARGIN_X,
        Inches(6.08),
        st.CONTENT_WIDTH,
        Inches(0.78),
        "Rute Maraton (±2,5–3 Jam): 3Blue1Brown → IBM Technology → Corey Schafer & freeCodeCamp OpenCV → Computerphile (Canny) → Kaggle Data Leakage.",
        accent_color=st.GREEN,
        bg_color=st.TINT_GREEN,
        font_size=Pt(16),
        bold=True,
    )
    st.add_footer(s27, 27, SESSION_LABEL)
    st.set_speaker_notes(
        s27,
        """Alokasi waktu: 0 menit

Naskah ajar:
Slide referensi belajar mandiri bagian 2/2: pendalaman deteksi tepi (Blur/Filter, Sobel, Canny) untuk memahami metrik edge density polos vs ramai, serta sumber belajar anti-data leakage dan class imbalance.""",
    )

    # Auto-sync sequential slide footer numbers & verify 120-min speaker notes sum
    import re as _re
    total_notes_min = 0
    for idx_s, sld in enumerate(prs.slides, start=1):
        for shp in sld.shapes:
            if shp.has_text_frame and shp.left == Inches(11.5) and shp.top == Inches(7.02):
                for p in shp.text_frame.paragraphs:
                    for r in p.runs:
                        r.text = f"{idx_s:02d}"
        if sld.has_notes_slide:
            m_min = _re.search(r"Alokasi waktu:\s*(\d+)\s*menit", sld.notes_slide.notes_text_frame.text)
            if m_min:
                total_notes_min += int(m_min.group(1))
    assert total_notes_min == 120, f"Expected 120 min notes in PPTX, got {total_notes_min}"

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT_PPTX)


def main() -> None:
    stats, df = analyze_sample_dataset()
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    STATS_JSON.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    vis = generate_visualizations(df, stats)
    html_main = ROOT_DIR / "materials" / "P01" / "P01_understanding_images_processing_eda.html"
    if html_main.exists():
        from export_pdf_P01 import export_pptx
        export_pptx()
    else:
        build_deck(stats, vis)
        print(f"PPTX berhasil dibuat: {OUT_PPTX}")
    print(f"Statistik sampel: valid={stats['valid_images']}, rusak={stats['corrupted_count']}, duplikat={stats['duplicate_file_count']}, exif6={stats['exif_orientation_6_count']}")


if __name__ == "__main__":
    main()
