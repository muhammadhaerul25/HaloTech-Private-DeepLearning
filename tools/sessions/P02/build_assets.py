"""Generate deterministic visual assets & real Frozen v1 data JSON for P02: Computer Vision 101.

Outputs saved to `materials/P02/assets/P02/`:
- Real Frozen v1 thumbnails (`thumb_anna.jpg`, `thumb_elsa.jpg`, `thumb_kristoff.jpg`,
  `thumb_olaf.jpg`, `thumb_sven.jpg`, `thumb_elsa_ramai.jpg`, `thumb_olaf_ramai.jpg`, `thumb_anna_ramai.jpg`)
- `01_frozen_gallery_5classes.png` (Real 2x5 polos vs ramai Frozen figurine showcase)
- `02_cv_tasks_4panel.png` (4 CV Tasks illustrated with code overlays on real Frozen photos)
- `03_flatten_frozen_visual.png` (Real Elsa 2D photo -> 1D flattened pixel strip + parameter counts)
- `04_mini_forward_pass_pixels.png` (Real 2x2 pixel patch from Elsa photo for Slide 33 forward pass)
- `05_loss_gradient_descent_overview.png` (Cross-Entropy Loss curve + Gradient Descent bowl intuition)
- `06_mlp_vs_cnn_preview.png` (MLP Flatten vs CNN 2D Filter teaser for Bab 4)
- `p02_data.json` (Real normalized RGB, dynamic dataset stats, and exact 4-pixel forward pass values)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from core.registry import get_session  # noqa: E402

SEED = 42
SESSION = get_session("P02")
FROZEN_DIR = ROOT_DIR / "data" / "frozen_v1"
ASSETS_DIR = SESSION.assets_dir

CLASSES = ["anna", "elsa", "kristoff", "olaf", "sven"]
COLORS = {
    "blue": "#4285F4",
    "blue_dark": "#1A73E8",
    "red": "#EA4335",
    "yellow": "#FBBC04",
    "green": "#34A853",
    "dark": "#202124",
    "muted": "#5F6368",
    "surface": "#F8F9FA",
}


def _pick_sample_image(kelas: str, kondisi: str, idx: int = 0) -> Path:
    folder = FROZEN_DIR / kelas / kondisi
    files = sorted(folder.glob("*.jpg"))
    if not files:
        raise FileNotFoundError(f"Tidak ditemukan foto di {folder}")
    return files[min(idx, len(files) - 1)]


def _center_crop_square(im: Image.Image, crop_frac: float = 0.72) -> Image.Image:
    """Crop a centered square focused on the figurine so tiny figures are clearly visible."""
    w, h = im.size
    side = int(min(w, h) * crop_frac)
    cx, cy = w // 2, int(h * 0.48)
    left = max(0, min(w - side, cx - side // 2))
    top = max(0, min(h - side, cy - side // 2))
    return im.crop((left, top, left + side, top + side))


def _compute_real_4pixel_forward_pass(elsa_thumb: Image.Image) -> dict:
    """Compute an exact, reproducible 4-pixel -> 2-hidden -> 2-output forward pass from real Elsa photo."""
    gray_2x2 = np.array(elsa_thumb.convert("L").resize((2, 2), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    x = np.round(gray_2x2.flatten(), 2)  # 4 real pixel values in [0, 1]

    # Simple human-readable weights & biases for pedagogical clarity
    W1 = np.array(
        [
            [0.8, -0.4],
            [0.6, 0.5],
            [-0.2, 0.9],
            [0.4, -0.3],
        ],
        dtype=np.float64,
    )
    b1 = np.array([-0.1, 0.1], dtype=np.float64)

    z1 = x.astype(np.float64) @ W1 + b1
    h1 = np.maximum(0.0, z1)  # ReLU

    W2 = np.array(
        [
            [1.5, -0.8],
            [-0.5, 1.2],
        ],
        dtype=np.float64,
    )
    b2 = np.array([0.2, -0.2], dtype=np.float64)
    logits = h1 @ W2 + b2
    shifted = logits - np.max(logits)
    exps = np.exp(shifted)
    probs = exps / np.sum(exps)

    return {
        "x": [round(float(v), 2) for v in x],
        "W1": W1.tolist(),
        "b1": b1.tolist(),
        "z1": [round(float(v), 3) for v in z1],
        "h1": [round(float(v), 3) for v in h1],
        "W2": W2.tolist(),
        "b2": b2.tolist(),
        "logits": [round(float(v), 3) for v in logits],
        "probs": [round(float(v), 4) for v in probs],
    }


def generate_thumbnails_and_stats() -> tuple[dict, Image.Image]:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    # Remove stale assets from previous P02 layout if present
    for old_name in (
        "02_linear_vs_nonlinear.png",
        "03_activation_comparison.png",
        "04_cross_entropy_penalty.png",
        "05_flatten_frozen_visual.png",
    ):
        (ASSETS_DIR / old_name).unlink(missing_ok=True)

    summary_path = FROZEN_DIR / "dataset_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    meta_df = pd.read_csv(FROZEN_DIR / "metadata.csv")

    char_samples = {}
    elsa_thumb_img = None
    for kls in CLASSES:
        fp_polos = _pick_sample_image(kls, "polos", idx=1)
        with Image.open(fp_polos) as im:
            im_rgb = im.convert("RGB")
            sq = _center_crop_square(im_rgb, crop_frac=0.68)
            thumb = sq.resize((220, 220), Image.Resampling.LANCZOS)
            thumb.save(ASSETS_DIR / f"thumb_{kls}.jpg", quality=90)
            if kls == "elsa":
                elsa_thumb_img = thumb.copy()

            arr = np.array(thumb, dtype=np.float32) / 255.0
            center = arr[65:155, 70:150, :]
            r_m, g_m, b_m = [round(float(center[:, :, c].mean()), 2) for c in range(3)]
            char_samples[kls] = {
                "file": fp_polos.name,
                "rgb_norm": [r_m, g_m, b_m],
                "count_total": int(summary["by_class"][kls]),
                "count_polos": int(summary["class_x_condition"][kls]["polos"]),
                "count_ramai": int(summary["class_x_condition"][kls]["ramai"]),
            }

    for kls in ("elsa", "olaf", "anna"):
        fp_ramai = _pick_sample_image(kls, "ramai", idx=0)
        with Image.open(fp_ramai) as im:
            sq = _center_crop_square(im.convert("RGB"), crop_frac=0.88)
            sq.resize((220, 220), Image.Resampling.LANCZOS).save(ASSETS_DIR / f"thumb_{kls}_ramai.jpg", quality=90)

    assert elsa_thumb_img is not None
    mini_fp = _compute_real_4pixel_forward_pass(elsa_thumb_img)

    # Real 3x3 Elsa pixel sample for the interactive Flatten motion animation (Slide 21)
    fp_elsa_main = _pick_sample_image("elsa", "polos", idx=1)
    with Image.open(fp_elsa_main) as im_e:
        elsa_crop_3x3 = _center_crop_square(im_e.convert("RGB"), crop_frac=0.58)
        e3_rgb = np.array(elsa_crop_3x3.resize((3, 3), Image.Resampling.BILINEAR))
        e3_gray = np.array(elsa_crop_3x3.convert("L").resize((3, 3), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    flatten_3x3 = [
        {
            "idx": r * 3 + c + 1,
            "row": r,
            "col": c,
            "rgb": [int(e3_rgb[r, c, 0]), int(e3_rgb[r, c, 1]), int(e3_rgb[r, c, 2])],
            "gray": round(float(e3_gray[r, c]), 2),
        }
        for r in range(3)
        for c in range(3)
    ]

    p02_data = {
        "dataset_name": summary["dataset_name"],
        "total_images": int(len(meta_df)),
        "classes": CLASSES,
        "polos_count": int((meta_df["kondisi"] == "polos").sum()),
        "ramai_count": int((meta_df["kondisi"] == "ramai").sum()),
        "sessions_count": int(meta_df["sesi_foto"].nunique()),
        "char_samples": char_samples,
        "mini_forward_pass": mini_fp,
        "flatten_3x3": flatten_3x3,
    }
    (ASSETS_DIR / "p02_data.json").write_text(json.dumps(p02_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return p02_data, elsa_thumb_img


def _extract_figurine_mask(arr_rgb: np.ndarray, y_max: int = 172, dist_thresh: float = 28.0) -> tuple[np.ndarray, tuple[int, int, int, int]]:
    """Extract a clean foreground silhouette mask & tight bbox for a figurine on a polos background."""
    h, w, _ = arr_rgb.shape
    lab = cv2.cvtColor(arr_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    # Estimate background LAB from top-left and top-right wall patches
    bg_samples = np.concatenate([lab[:35, :35].reshape(-1, 3), lab[:35, -35:].reshape(-1, 3)], axis=0)
    bg_med = np.median(bg_samples, axis=0)
    dist = np.linalg.norm(lab - bg_med, axis=-1)

    mask = np.zeros((h, w), dtype=np.uint8)
    mask[(dist > dist_thresh)] = 255
    # Restrict to central figurine area above fingers
    roi = np.zeros((h, w), dtype=np.uint8)
    roi[14:y_max, 36 : w - 36] = 255
    mask = cv2.bitwise_and(mask, roi)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # Keep largest connected component (the figurine itself)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    if num_labels > 1:
        best_lbl = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        mask = np.where(labels == best_lbl, 255, 0).astype(np.uint8)

    ys, xs = np.where(mask > 0)
    if len(xs) > 0:
        x0, x1 = int(xs.min()), int(xs.max())
        y0, y1 = int(ys.min()), int(ys.max())
        bbox = (max(0, x0 - 4), max(0, y0 - 4), (x1 - x0) + 8, (y1 - y0) + 8)
    else:
        bbox = (60, 30, 100, 140)
    return mask, bbox


def _overlay_mask(arr_rgb: np.ndarray, mask: np.ndarray, hex_color: str, alpha: float = 0.50) -> np.ndarray:
    """Blend a crisp translucent mask + white contour border onto an RGB image."""
    out = arr_rgb.astype(np.float32).copy()
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    col = np.array([r, g, b], dtype=np.float32)
    fg = mask > 0
    out[fg] = (1.0 - alpha) * out[fg] + alpha * col
    out_u8 = np.clip(out, 0, 255).astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(out_u8, contours, -1, (255, 255, 255), 2)
    return out_u8


def generate_charts(p02_data: dict, elsa_thumb: Image.Image) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"

    # 1. Real Frozen v1 2x5 Gallery (Polos vs Ramai)
    fig, axes = plt.subplots(2, 5, figsize=(11.2, 4.7), dpi=190)
    for col, kls in enumerate(CLASSES):
        for row, cond in enumerate(["polos", "ramai"]):
            fp = _pick_sample_image(kls, cond, idx=1 if cond == "polos" else 0)
            with Image.open(fp) as im:
                sq = _center_crop_square(im.convert("RGB"), crop_frac=0.72 if cond == "polos" else 0.90)
                axes[row, col].imshow(sq)
            axes[row, col].set_xticks([])
            axes[row, col].set_yticks([])
            for sp in axes[row, col].spines.values():
                sp.set_edgecolor("#DADCE0")
                sp.set_linewidth(1.4)
            if row == 0:
                axes[row, col].set_title(kls.capitalize(), fontsize=13, fontweight="bold", color=COLORS["dark"], pad=6)
            if col == 0:
                axes[row, col].set_ylabel(
                    cond.upper(),
                    fontsize=12.5,
                    fontweight="bold",
                    color=COLORS["blue_dark"] if cond == "polos" else COLORS["red"],
                    labelpad=8,
                )
    fig.suptitle("Dataset Proyek Nyata: 5 Karakter Disney Frozen (Polos vs Ramai)", fontsize=14.5, fontweight="bold", color=COLORS["dark"], y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(ASSETS_DIR / "01_frozen_gallery_5classes.png", dpi=190, facecolor="#FFFFFF")
    plt.close(fig)

    # 2. 4 CV Tasks Illustrated on Real Frozen Photo with REAL pixel-accurate silhouette mask
    elsa_arr = np.array(elsa_thumb)
    elsa_mask, (ex, ey, ew, eh) = _extract_figurine_mask(elsa_arr, y_max=170, dist_thresh=24.0)
    elsa_masked_img = _overlay_mask(elsa_arr, elsa_mask, COLORS["green"], alpha=0.52)

    fig, axes = plt.subplots(1, 4, figsize=(11.8, 3.95), dpi=190)
    titles = [
        ("1. Image Classification", COLORS["blue_dark"], "Output: 1 Label ('Elsa')\nuntuk seluruh foto"),
        ("2. Object Detection", COLORS["red"], "Output: Bounding Box + Label\n(apa & di mana)"),
        ("3. Semantic & Instance Segm.", COLORS["green"], "Output: Mask Presisi per Piksel\n(mengikuti lekuk objek)"),
        ("4. Object Tracking", "#B06000", "Output: ID #1 Antar-Frame\n(melacak gerak di video)"),
    ]
    for i, (ax, (ttl, col, sub)) in enumerate(zip(axes, titles)):
        ax.imshow(elsa_masked_img if i == 2 else elsa_arr)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_edgecolor(col)
            sp.set_linewidth(2.2)
        ax.set_title(ttl, fontsize=10.8, fontweight="bold", color=col, pad=6)
        ax.set_xlabel(sub, fontsize=8.8, color=COLORS["dark"], labelpad=6)

        if i == 0:
            ax.text(
                110, 24, "Label: ELSA", ha="center", va="center", fontsize=9.5, fontweight="bold",
                color="#FFFFFF", bbox=dict(boxstyle="round,pad=0.32", facecolor=COLORS["blue"], edgecolor="none")
            )
        elif i == 1:
            rect = patches.Rectangle((ex, ey), ew, eh, linewidth=2.6, edgecolor=COLORS["red"], facecolor="none")
            ax.add_patch(rect)
            ax.text(
                ex, max(16, ey - 5), "Elsa [bbox]", ha="left", va="bottom", fontsize=8.4, fontweight="bold",
                color="#FFFFFF", bbox=dict(boxstyle="square,pad=0.18", facecolor=COLORS["red"], edgecolor="none")
            )
        elif i == 2:
            ax.text(
                110, 198, "Mask #1: Elsa", ha="center", va="center", fontsize=8.5, fontweight="bold",
                color="#FFFFFF", bbox=dict(boxstyle="round,pad=0.25", facecolor=COLORS["green"], edgecolor="none")
            )
        elif i == 3:
            for (dx, dy, alp) in [(-24, 6, 0.35), (-12, 3, 0.62), (0, 0, 1.0)]:
                r = patches.Rectangle(
                    (max(4, ex + dx), max(4, ey + dy)), ew, eh,
                    linewidth=2.2, edgecolor=COLORS["yellow"], facecolor="none",
                    alpha=alp, linestyle="--" if alp < 1 else "-"
                )
                ax.add_patch(r)
            cx, cy = ex + ew * 0.5, ey + eh * 0.5
            ax.annotate("", xy=(cx + 4, cy), xytext=(cx - 26, cy + 7), arrowprops=dict(arrowstyle="->", color=COLORS["yellow"], lw=2.8))
            ax.text(
                ex, max(16, ey - 5), "ID #1 · Elsa", ha="left", va="bottom", fontsize=8.4, fontweight="bold",
                color=COLORS["dark"], bbox=dict(boxstyle="square,pad=0.2", facecolor=COLORS["yellow"], edgecolor="none")
            )

    fig.suptitle("4 Tugas Utama Computer Vision pada Foto yang Sama (Ilustrasi Konsep Buatan Kode)", fontsize=12.4, fontweight="bold", color=COLORS["dark"], y=0.97)
    fig.subplots_adjust(left=0.015, right=0.985, top=0.83, bottom=0.14, wspace=0.08)
    fig.savefig(ASSETS_DIR / "02_cv_tasks_4panel.png", dpi=190, facecolor="#FFFFFF", bbox_inches="tight", pad_inches=0.10)
    plt.close(fig)

    # 2b. Real Multi-Object Detection Illustration (Elsa + Olaf side-by-side with tight bounding boxes)
    olaf_thumb = Image.open(ASSETS_DIR / "thumb_olaf.jpg").convert("RGB")
    olaf_arr = np.array(olaf_thumb)
    olaf_mask, (ox, oy, ow, oh) = _extract_figurine_mask(olaf_arr, y_max=114, dist_thresh=18.0)

    # Create clean 2-figurine composite (220x440)
    comp_det = np.concatenate([elsa_arr, olaf_arr], axis=1)
    fig, ax = plt.subplots(figsize=(5.6, 3.15), dpi=190)
    ax.imshow(comp_det)
    r1 = patches.Rectangle((ex, ey), ew, eh, linewidth=2.8, edgecolor=COLORS["blue"], facecolor="none")
    ax.add_patch(r1)
    ax.text(ex, max(15, ey - 4), "Elsa (x₁,y₁,w₁,h₁)", ha="left", va="bottom", fontsize=8.5, fontweight="bold",
            color="#FFFFFF", bbox=dict(boxstyle="square,pad=0.2", facecolor=COLORS["blue"], edgecolor="none"))
    r2 = patches.Rectangle((220 + ox, oy), ow, oh, linewidth=2.8, edgecolor=COLORS["red"], facecolor="none")
    ax.add_patch(r2)
    ax.text(220 + ox, max(15, oy - 4), "Olaf (x₂,y₂,w₂,h₂)", ha="left", va="bottom", fontsize=8.5, fontweight="bold",
            color="#FFFFFF", bbox=dict(boxstyle="square,pad=0.2", facecolor=COLORS["red"], edgecolor="none"))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Ilustrasi Konsep: 2 Objek + 2 Bounding Box Sekaligus", fontsize=10.5, fontweight="bold", color=COLORS["dark"], pad=6)
    fig.tight_layout(pad=0.35)
    fig.savefig(ASSETS_DIR / "02b_object_detection_demo.png", dpi=190, facecolor="#FFFFFF", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)

    # 2c. Semantic vs Instance Segmentation on 2 Real Olafs side-by-side
    two_olaf = np.concatenate([olaf_arr, olaf_arr[:, ::-1, :]], axis=1)
    olaf_mask_flip = olaf_mask[:, ::-1]
    mask_both = np.concatenate([olaf_mask, olaf_mask_flip], axis=1)
    sem_img = _overlay_mask(two_olaf, mask_both, COLORS["blue"], alpha=0.52)

    inst_img = _overlay_mask(two_olaf, np.concatenate([olaf_mask, np.zeros_like(olaf_mask)], axis=1), COLORS["green"], alpha=0.52)
    inst_img = _overlay_mask(inst_img, np.concatenate([np.zeros_like(olaf_mask), olaf_mask_flip], axis=1), COLORS["red"], alpha=0.52)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.75), dpi=190)
    ax1.imshow(sem_img)
    ax1.set_title("Semantic Segmentation\n2 Olaf = 1 Warna Kelas ('Olaf')", fontsize=10.4, fontweight="bold", color=COLORS["blue_dark"], pad=6)
    ax1.text(220, 198, "Semua piksel = kelas 'Olaf'", ha="center", va="center", fontsize=8.5, fontweight="bold",
             color="#FFFFFF", bbox=dict(boxstyle="round,pad=0.25", facecolor=COLORS["blue"], edgecolor="none"))
    ax1.axis("off")

    ax2.imshow(inst_img)
    ax2.set_title("Instance Segmentation\nOlaf #1 & Olaf #2 Dipisah Jelas!", fontsize=10.4, fontweight="bold", color="#137333", pad=6)
    ax2.text(110, 198, "Olaf #1", ha="center", va="center", fontsize=8.5, fontweight="bold",
             color="#FFFFFF", bbox=dict(boxstyle="round,pad=0.25", facecolor=COLORS["green"], edgecolor="none"))
    ax2.text(330, 198, "Olaf #2", ha="center", va="center", fontsize=8.5, fontweight="bold",
             color="#FFFFFF", bbox=dict(boxstyle="round,pad=0.25", facecolor=COLORS["red"], edgecolor="none"))
    ax2.axis("off")

    fig.tight_layout(pad=0.5)
    fig.savefig(ASSETS_DIR / "02c_semantic_vs_instance_demo.png", dpi=190, facecolor="#FFFFFF", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)

    # 2d. Elsa Silhouette Mask Closeup (Slide 15 left card)
    fig, ax = plt.subplots(figsize=(5.4, 2.65), dpi=190)
    comp_seg = np.concatenate([elsa_arr, elsa_masked_img], axis=1)
    ax.imshow(comp_seg)
    ax.axvline(220, color="#FFFFFF", linewidth=2.5)
    ax.text(110, 22, "Foto Asli", ha="center", va="center", fontsize=9.2, fontweight="bold", color="#FFFFFF",
            bbox=dict(boxstyle="round,pad=0.25", facecolor=COLORS["dark"], edgecolor="none"))
    ax.text(330, 22, "Mask per Piksel", ha="center", va="center", fontsize=9.2, fontweight="bold", color="#FFFFFF",
            bbox=dict(boxstyle="round,pad=0.25", facecolor=COLORS["green"], edgecolor="none"))
    ax.axis("off")
    fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    fig.savefig(ASSETS_DIR / "02d_elsa_mask_closeup.png", dpi=190, facecolor="#FFFFFF", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)

    # 3a. Slide 20 Hero: Real Elsa Photo -> 8x8 Pixel Grid -> 1 Highlighted Pixel -> 1 Neuron Circle
    fp_elsa = _pick_sample_image("elsa", "polos", idx=1)
    with Image.open(fp_elsa) as im:
        elsa_sq = _center_crop_square(im.convert("RGB"), crop_frac=0.58).resize((180, 180), Image.Resampling.LANCZOS)
        elsa_arr180 = np.array(elsa_sq)
        elsa_arr160 = np.array(elsa_sq.resize((160, 160), Image.Resampling.LANCZOS))
        elsa_8x8 = np.array(elsa_sq.resize((8, 8), Image.Resampling.BILINEAR))
        elsa_8x8_gray = np.array(elsa_sq.convert("L").resize((8, 8), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
        elsa_3x3 = np.array(elsa_sq.resize((3, 3), Image.Resampling.BILINEAR))
        elsa_3x3_gray = np.array(elsa_sq.convert("L").resize((3, 3), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0

    # Pick a clearly visible pixel on Elsa's blue dress (row 5, col 4 in 8x8)
    hr, hc = 5, 3
    h_val = float(elsa_8x8_gray[hr, hc])
    h_rgb = tuple(int(c) for c in elsa_8x8[hr, hc])

    fig = plt.figure(figsize=(8.6, 4.1), dpi=200)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 48)
    ax.axis("off")

    # Step 1: Real Elsa photo (left)
    ax_p1 = fig.add_axes([0.03, 0.18, 0.24, 0.62])
    ax_p1.imshow(elsa_arr180)
    ax_p1.set_xticks([]); ax_p1.set_yticks([])
    for sp in ax_p1.spines.values():
        sp.set_edgecolor(COLORS["blue"]); sp.set_linewidth(2.4)
    ax_p1.set_title("1. Foto Asli Elsa", fontsize=10.5, fontweight="bold", color=COLORS["dark"], pad=7)

    # Arrow 1 -> 2
    ax.annotate("", xy=(33.5, 24.5), xytext=(28.2, 24.5), arrowprops=dict(arrowstyle="-|>,head_width=0.45,head_length=0.6", color=COLORS["muted"], lw=2.4))
    ax.text(30.8, 27.6, "Zoom\nPiksel", ha="center", va="bottom", fontsize=8.2, fontweight="bold", color=COLORS["muted"])

    # Step 2: 8x8 Visible Pixel Grid of Elsa (middle)
    ax_p2 = fig.add_axes([0.345, 0.18, 0.24, 0.62])
    ax_p2.imshow(elsa_8x8, interpolation="nearest")
    ax_p2.set_xticks(np.arange(-0.5, 8, 1), minor=True)
    ax_p2.set_yticks(np.arange(-0.5, 8, 1), minor=True)
    ax_p2.grid(which="minor", color="#FFFFFF", linestyle="-", linewidth=1.1, alpha=0.85)
    ax_p2.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    for sp in ax_p2.spines.values():
        sp.set_edgecolor(COLORS["dark"]); sp.set_linewidth(2.0)
    # Highlight 1 pixel on Elsa's dress
    ax_p2.add_patch(patches.Rectangle((hc - 0.5, hr - 0.5), 1, 1, linewidth=3.0, edgecolor=COLORS["red"], facecolor="none", zorder=5))
    ax_p2.set_title("2. Kotak-Kotak Piksel (8×8)", fontsize=10.5, fontweight="bold", color=COLORS["dark"], pad=7)

    # Step 3: Magnified Pixel -> 1 Bold Neuron Circle (right)
    # Zoom dashed guides from highlighted cell toward pixel card
    ax.annotate("", xy=(65.5, 25.0), xytext=(59.5, 25.0), arrowprops=dict(arrowstyle="-|>,head_width=0.45,head_length=0.6", color=COLORS["red"], lw=2.6))
    ax.text(62.5, 28.2, "Ambil\n1 Piksel", ha="center", va="bottom", fontsize=8.2, fontweight="bold", color=COLORS["red"])

    # Magnified Pixel Box
    pix_box = patches.FancyBboxPatch((66.5, 17.0), 11.5, 16.0, boxstyle="round,pad=0.6,rounding_size=1.8",
                                     facecolor=tuple(c / 255.0 for c in h_rgb), edgecolor=COLORS["red"], linewidth=2.6)
    ax.add_patch(pix_box)
    txt_on_pix = "#FFFFFF" if h_val < 0.58 else "#202124"
    ax.text(72.25, 26.8, f"{h_val:.2f}", ha="center", va="center", fontsize=14, fontweight="bold", color=txt_on_pix, family="DejaVu Sans Mono")
    ax.text(72.25, 21.0, "nilai 0–1", ha="center", va="center", fontsize=7.8, color=txt_on_pix)
    ax.text(72.25, 11.2, "1 Nilai Piksel", ha="center", va="center", fontsize=9.2, fontweight="bold", color=COLORS["red"])

    # Arrow Pixel -> Neuron
    ax.annotate("", xy=(83.8, 25.0), xytext=(79.0, 25.0), arrowprops=dict(arrowstyle="-|>,head_width=0.45,head_length=0.6", color=COLORS["blue_dark"], lw=2.8))

    # Glowing 1 Neuron Circle
    outer_ring = patches.Circle((90.8, 25.0), 7.6, facecolor="#E8F0FE", edgecolor="#C6DAFC", linewidth=2.0)
    inner_node = patches.Circle((90.8, 25.0), 6.2, facecolor=COLORS["blue"], edgecolor="#FFFFFF", linewidth=2.5)
    ax.add_patch(outer_ring)
    ax.add_patch(inner_node)
    ax.text(90.8, 28.0, "x₁", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#D2E3FC", family="DejaVu Sans Mono")
    ax.text(90.8, 23.6, f"{h_val:.2f}", ha="center", va="center", fontsize=13.5, fontweight="bold", color="#FFFFFF", family="DejaVu Sans Mono")
    ax.text(90.8, 11.2, "3. 1 Neuron", ha="center", va="center", fontsize=10.5, fontweight="bold", color=COLORS["blue_dark"])
    ax.text(90.8, 7.2, "(pemegang 1 angka)", ha="center", va="center", fontsize=8.4, color=COLORS["muted"])

    # Bottom caption strip
    ax.text(50, 2.5, "Setiap 1 kotak piksel pada foto Elsa diwakili oleh tepat 1 lingkaran Neuron yang memegang angkanya.",
            ha="center", va="center", fontsize=9.3, fontweight="bold", color=COLORS["dark"])

    fig.savefig(ASSETS_DIR / "03a_one_pixel_one_neuron.png", dpi=200, facecolor="#FFFFFF")
    plt.close(fig)

    # 3b. Slide 21 Hero: Real 3x3 Elsa Grid (Row 1, 2, 3) -> Flatten Top-to-Bottom -> 9 Stacked Neurons = INPUT LAYER
    fig = plt.figure(figsize=(11.4, 4.35), dpi=200)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 114)
    ax.set_ylim(0, 44)
    ax.axis("off")

    row_cols = [COLORS["blue"], COLORS["red"], COLORS["green"]]
    row_bg = ["#E8F0FE", "#FCE8E6", "#E6F4EA"]
    row_names = ["Baris 1", "Baris 2", "Baris 3"]

    # Panel 1: Real Elsa mini reference (far left)
    ax_ref = fig.add_axes([0.015, 0.24, 0.145, 0.52])
    ax_ref.imshow(elsa_arr180)
    ax_ref.set_xticks([]); ax_ref.set_yticks([])
    for sp in ax_ref.spines.values():
        sp.set_edgecolor("#DADCE0"); sp.set_linewidth(2.0)
    ax_ref.set_title("Foto Elsa", fontsize=10.5, fontweight="bold", color=COLORS["dark"], pad=6)

    ax.annotate("", xy=(24.8, 22.0), xytext=(19.0, 22.0), arrowprops=dict(arrowstyle="-|>,head_width=0.45,head_length=0.6", color=COLORS["muted"], lw=2.4))
    ax.text(21.9, 25.2, "Contoh\n3×3", ha="center", va="bottom", fontsize=8.2, fontweight="bold", color=COLORS["muted"])

    # Panel 2: Real 3x3 Colored Pixel Grid of Elsa with Row Color Coding
    ax.text(43.5, 40.4, "1. Gambar 2D (3×3 = 9 Piksel Nyata)", ha="center", va="center", fontsize=11.0, fontweight="bold", color=COLORS["dark"])
    gx0, gy0, cell = 32.5, 9.6, 7.2
    for r in range(3):
        # Row label pill on left
        ry_center = gy0 + (2 - r) * (cell + 1.0) + cell / 2
        pill = patches.FancyBboxPatch((25.8, ry_center - 1.85), 5.6, 3.7, boxstyle="round,pad=0.2,rounding_size=0.9",
                                      facecolor=row_bg[r], edgecolor=row_cols[r], linewidth=1.4)
        ax.add_patch(pill)
        ax.text(28.6, ry_center, row_names[r], ha="center", va="center", fontsize=7.6, fontweight="bold", color=row_cols[r])
        for c in range(3):
            cx = gx0 + c * (cell + 0.9)
            cy = gy0 + (2 - r) * (cell + 1.0)
            rgb = tuple(int(v) / 255.0 for v in elsa_3x3[r, c])
            gv = float(elsa_3x3_gray[r, c])
            idx = r * 3 + c + 1
            rect = patches.FancyBboxPatch((cx, cy), cell, cell, boxstyle="round,pad=0.05,rounding_size=1.0",
                                          facecolor=rgb, edgecolor=row_cols[r], linewidth=2.4)
            ax.add_patch(rect)
            tc = "#FFFFFF" if gv < 0.56 else "#202124"
            ax.text(cx + cell / 2, cy + cell * 0.66, f"x{idx}", ha="center", va="center", fontsize=8.0, fontweight="bold", color=tc, family="DejaVu Sans Mono")
            ax.text(cx + cell / 2, cy + cell * 0.30, f"{gv:.2f}", ha="center", va="center", fontsize=9.8, fontweight="bold", color=tc, family="DejaVu Sans Mono")
    ax.text(44.2, 4.8, "Bentuk 2D: tersusun dalam baris & kolom", ha="center", va="center", fontsize=8.8, color=COLORS["muted"])

    # Middle Flatten Stage: placed high and clean ABOVE all 3 curved arrows
    flat_badge = patches.FancyBboxPatch((59.8, 37.2), 16.8, 4.6, boxstyle="round,pad=0.3,rounding_size=1.4",
                                        facecolor="#FEF7E0", edgecolor=COLORS["yellow"], linewidth=2.0)
    ax.add_patch(flat_badge)
    ax.text(68.2, 39.5, "2. FLATTEN", ha="center", va="center", fontsize=10.2, fontweight="bold", color="#B06000")
    ax.text(68.2, 34.4, "Susun baris bertumpuk\ndari atas ke bawah", ha="center", va="center", fontsize=8.2, fontweight="bold", color=COLORS["dark"])

    # Right: Vertical Stacked 9 Neuron Circles = INPUT LAYER
    cap = patches.FancyBboxPatch((81.5, 2.0), 30.5, 39.8, boxstyle="round,pad=0.4,rounding_size=2.2",
                                 facecolor="#F8F9FA", edgecolor=COLORS["blue"], linewidth=2.6)
    ax.add_patch(cap)
    ax.text(96.75, 39.2, "3. INPUT LAYER", ha="center", va="center", fontsize=11.5, fontweight="bold", color=COLORS["blue_dark"])
    ax.text(96.75, 36.4, "(1 Kolom Vertikal = 9 Neuron)", ha="center", va="center", fontsize=8.2, color=COLORS["muted"])

    ys = np.linspace(32.2, 4.8, 9)
    for idx0, y_pos in enumerate(ys):
        r = idx0 // 3
        c = idx0 % 3
        gv = float(elsa_3x3_gray[r, c])
        circ = patches.Circle((89.0, y_pos), 1.52, facecolor=row_cols[r], edgecolor="#FFFFFF", linewidth=1.6, zorder=4)
        ax.add_patch(circ)
        ax.text(89.0, y_pos, f"{gv:.2f}", ha="center", va="center", fontsize=6.6, fontweight="bold", color="#FFFFFF", family="DejaVu Sans Mono", zorder=5)
        ax.text(91.9, y_pos, f"x{idx0 + 1}", ha="left", va="center", fontsize=8.2, fontweight="bold", color=row_cols[r], family="DejaVu Sans Mono")
        ax.text(96.2, y_pos, f"({row_names[r]}, Kol {c + 1})", ha="left", va="center", fontsize=7.6, color=COLORS["muted"])

    # Clean connectors from the 3 row centers on the grid to the 3 row groups on the Input Layer
    row_target_y = [ys[1], ys[4], ys[7]]
    for r in range(3):
        ry_src = gy0 + (2 - r) * (cell + 1.0) + cell / 2
        ax.annotate(
            "", xy=(80.8, row_target_y[r]), xytext=(57.0, ry_src),
            arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.55", color=row_cols[r], lw=2.4,
                            connectionstyle=f"arc3,rad={-0.06 if r == 0 else (0.10 if r == 2 else 0.0)}"),
        )

    fig.savefig(ASSETS_DIR / "03b_flatten_to_input_layer.png", dpi=200, facecolor="#FFFFFF")
    plt.close(fig)

    # 3c. Slide 23 Hero: Full-Scale Real Elsa (224x224x3) -> Actual Stacked Colored Neuron Circles Capsule -> Bar Chart
    fig = plt.figure(figsize=(11.4, 4.2), dpi=190)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.05, 1.45], wspace=0.28)
    ax_img = fig.add_subplot(gs[0])
    ax_flat = fig.add_subplot(gs[1])
    ax_bar = fig.add_subplot(gs[2])

    ax_img.imshow(elsa_arr160)
    for y_line in range(20, 160, 20):
        ax_img.axhline(y_line, color="#FBBC04", linewidth=1.3, linestyle="--", alpha=0.92)
    ax_img.set_title("1. Foto Elsa (224×224×3)\nDiiris baris demi baris", fontsize=10.8, fontweight="bold", color=COLORS["dark"], pad=8)
    ax_img.axis("off")

    # Panel 2: Actual Input Layer Capsule with Individual Neuron Circles (NOT window-blind stripes!)
    ax_flat.set_xlim(0, 10)
    ax_flat.set_ylim(0, 12)
    ax_flat.axis("off")
    ax_flat.set_title("2. Input Layer (Flatten 1D)\n150.528 neuron bertumpuk", fontsize=10.8, fontweight="bold", color=COLORS["blue_dark"], pad=8)
    capsule = patches.FancyBboxPatch((1.3, 0.4), 7.4, 11.1, boxstyle="round,pad=0.2,rounding_size=0.9",
                                     facecolor="#E8F0FE", edgecolor=COLORS["blue"], linewidth=2.2)
    ax_flat.add_patch(capsule)
    sample_nodes = [
        (10.1, "x₁", "0.76", "#EA4335", "Piksel 1 (R)"),
        (8.6, "x₂", "0.75", "#34A853", "Piksel 1 (G)"),
        (7.1, "x₃", "0.74", "#4285F4", "Piksel 1 (B)"),
        (2.8, "x₁₅₀₅₂₇", "0.42", "#34A853", "Piksel akhir (G)"),
        (1.3, "x₁₅₀₅₂₈", "0.39", "#4285F4", "Piksel akhir (B)"),
    ]
    for ny, nlbl, nval, ncol, ndesc in sample_nodes:
        c_node = patches.Circle((3.0, ny), 0.62, facecolor=ncol, edgecolor="#FFFFFF", linewidth=1.8, zorder=4)
        ax_flat.add_patch(c_node)
        ax_flat.text(3.0, ny, nval, ha="center", va="center", fontsize=7.2, fontweight="bold", color="#FFFFFF", family="DejaVu Sans Mono", zorder=5)
        ax_flat.text(4.0, ny + 0.16, nlbl, ha="left", va="center", fontsize=8.4, fontweight="bold", color=COLORS["dark"], family="DejaVu Sans Mono")
        ax_flat.text(4.0, ny - 0.28, ndesc, ha="left", va="center", fontsize=7.0, color=COLORS["muted"])
    # Vertical ellipsis dots in center
    for dy in [5.65, 4.95, 4.25]:
        ax_flat.add_patch(patches.Circle((3.0, dy), 0.13, facecolor=COLORS["blue_dark"], edgecolor="none"))
    ax_flat.text(4.0, 4.95, "150.523 neuron\nlainnya bertumpuk\nke bawah...", ha="left", va="center", fontsize=7.8, fontweight="bold", color=COLORS["blue_dark"])

    labels = ["MNIST\n(28×28×1)", "Frozen Kecil\n(64×64×3)", "Frozen Standar\n(224×224×3)"]
    neurons_k = [784 / 1000, 12288 / 1000, 150528 / 1000]
    val_txts = ["784", "12.288", "150.528"]
    bars = ax_bar.bar(labels, neurons_k, color=[COLORS["green"], COLORS["yellow"], COLORS["blue"]], edgecolor="#202124", linewidth=1.1, width=0.52)
    for b, val, vtxt in zip(bars, neurons_k, val_txts):
        ax_bar.text(b.get_x() + b.get_width() / 2, val + 4.0, f"{vtxt}\nneuron", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=COLORS["dark"])
    ax_bar.set_ylim(0, 185.0)
    ax_bar.set_ylabel("Jumlah Neuron Input (Ribu)", fontsize=10, color=COLORS["dark"])
    ax_bar.set_title("3. Jumlah Neuron Input Layer per Ukuran Foto", fontsize=10.8, fontweight="bold", color=COLORS["dark"], pad=8)
    ax_bar.tick_params(labelsize=9.2)
    ax_bar.grid(axis="y", linestyle="--", alpha=0.35)

    fig.subplots_adjust(left=0.03, right=0.98, top=0.84, bottom=0.14, wspace=0.26)
    fig.savefig(ASSETS_DIR / "03_flatten_frozen_visual.png", dpi=190, facecolor="#FFFFFF")
    plt.close(fig)

    # 4. Mini 2x2 Real Elsa Patch for Forward Pass Slide 33
    x_vals = p02_data["mini_forward_pass"]["x"]
    grid_2x2 = np.array(x_vals).reshape(2, 2)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.2, 3.0), dpi=190)
    ax1.imshow(elsa_thumb)
    ax1.set_title("Foto Elsa Asli", fontsize=11, fontweight="bold", color=COLORS["dark"])
    ax1.axis("off")

    ax2.imshow(grid_2x2, cmap="gray", vmin=0.0, vmax=1.0)
    ax2.set_title("Versi Mini 2×2 (4 Piksel)", fontsize=11, fontweight="bold", color=COLORS["blue_dark"])
    ax2.set_xticks([0, 1])
    ax2.set_yticks([0, 1])
    for r in range(2):
        for c in range(2):
            v = grid_2x2[r, c]
            idx_num = r * 2 + c + 1
            txt_col = "#FFFFFF" if v < 0.5 else "#202124"
            ax2.text(c, r, f"x{idx_num}\n{v:.2f}", ha="center", va="center", fontsize=12, fontweight="bold", color=txt_col)
    fig.tight_layout(pad=1.0)
    fig.savefig(ASSETS_DIR / "04_mini_forward_pass_pixels.png", dpi=190, facecolor="#FFFFFF")
    plt.close(fig)

    # 5. Loss + Gradient Descent 2-Panel Intuition
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 3.9), dpi=190)

    p = np.linspace(0.03, 1.0, 220)
    ce = -np.log(p)
    ax1.plot(p, ce, color=COLORS["red"], linewidth=3.2)
    ax1.fill_between(p, ce, alpha=0.10, color=COLORS["red"])
    for px, py, txt, col, (tx, ty) in [
        (0.10, -np.log(0.10), "Salah & Yakin (10%)\nLoss Besar = 2.30", COLORS["red"], (0.30, 2.75)),
        (0.90, -np.log(0.90), "Benar & Yakin (90%)\nLoss Kecil = 0.11", COLORS["green"], (0.50, 0.90)),
    ]:
        ax1.scatter([px], [py], color=col, s=75, zorder=5, edgecolors="#202124", linewidths=1.2)
        ax1.annotate(
            txt, xy=(px, py), xytext=(tx, ty), fontsize=8.8, fontweight="bold", color=COLORS["dark"],
            bbox=dict(boxstyle="round,pad=0.32", facecolor="#FFFFFF", edgecolor=col, lw=1.6),
            arrowprops=dict(arrowstyle="->", color=col, lw=1.6),
        )
    ax1.set_title("1. Loss: Seberapa Salah Tebakan AI", fontsize=11.5, fontweight="bold", color=COLORS["dark"], pad=8)
    ax1.set_xlabel("Probabilitas untuk Kelas yang Benar (p)", fontsize=9.5)
    ax1.set_ylabel("Nilai Loss (makin kecil makin baik)", fontsize=9.5)
    ax1.set_ylim(0, 3.7)
    ax1.grid(True, linestyle="--", alpha=0.35)

    w_grid = np.linspace(-3.2, 3.2, 200)
    ax2.plot(w_grid, w_grid ** 2, color=COLORS["dark"], linewidth=2.8)
    w_steps = [-2.6, -1.56, -0.94, -0.56, -0.34, -0.05]
    l_steps = [w ** 2 for w in w_steps]
    ax2.plot(w_steps, l_steps, color=COLORS["blue"], linewidth=2.2, marker="o", markersize=7, label="Langkah Gradient Descent")
    ax2.scatter([0], [0], color=COLORS["green"], s=110, zorder=6, edgecolors="#202124", linewidths=1.3, label="Dasar Lembah (Loss Minimum)")
    ax2.annotate(
        "Mulai (Bobot Acak)\nLoss Tinggi", xy=(-2.6, 6.76), xytext=(-2.95, 9.2),
        fontsize=8.6, fontweight="bold", color=COLORS["red"],
        bbox=dict(boxstyle="round,pad=0.28", facecolor="#FCE8E6", edgecolor=COLORS["red"]),
        arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.5),
    )
    ax2.annotate(
        "Turun bertahap\nke dasar lembah", xy=(-0.05, 0.05), xytext=(0.75, 2.3),
        fontsize=8.6, fontweight="bold", color="#137333",
        bbox=dict(boxstyle="round,pad=0.28", facecolor="#E6F4EA", edgecolor=COLORS["green"]),
        arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=1.5),
    )
    ax2.set_title("2. Gradient Descent: Turun Bukit Menuju Error Terkecil", fontsize=11.5, fontweight="bold", color=COLORS["dark"], pad=8)
    ax2.set_xlabel("Nilai Weight (w)", fontsize=9.5)
    ax2.set_ylabel("Nilai Loss", fontsize=9.5)
    ax2.set_ylim(-0.6, 11.4)
    ax2.grid(True, linestyle="--", alpha=0.35)
    ax2.legend(loc="upper right", fontsize=8.2, framealpha=0.95)

    fig.tight_layout(pad=1.3)
    fig.savefig(ASSETS_DIR / "05_loss_gradient_descent_overview.png", dpi=190, facecolor="#FFFFFF")
    plt.close(fig)

    # 6. MLP vs CNN Teaser Comparison (Bab 4)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 3.8), dpi=190)
    ax1.imshow(elsa_arr160)
    ax1.set_title("MLP: Gambar Dipotong & Diluruskan (1D)\n19,27 Juta Bobot · Peka Pergeseran", fontsize=10.8, fontweight="bold", color=COLORS["red"], pad=8)
    for y in range(16, 160, 16):
        ax1.axhline(y, color=COLORS["red"], linewidth=1.2, linestyle="--", alpha=0.85)
    ax1.axis("off")

    ax2.imshow(elsa_arr160)
    ax2.set_title("CNN: Filter Kecil (3×3) Menggeser di Gambar 2D Utuh\nHemat Bobot · Tahan Pergeseran Posisi", fontsize=10.8, fontweight="bold", color="#137333", pad=8)
    for (rx, ry, col, lbl) in [(48, 32, COLORS["blue"], "Filter Wajah"), (42, 86, COLORS["green"], "Filter Gaun"), (92, 58, COLORS["yellow"], "Filter Tepi")]:
        rect = patches.Rectangle((rx, ry), 36, 36, linewidth=2.6, edgecolor=col, facecolor=col, alpha=0.20)
        ax2.add_patch(rect)
        rect_b = patches.Rectangle((rx, ry), 36, 36, linewidth=2.6, edgecolor=col, facecolor="none")
        ax2.add_patch(rect_b)
        ax2.text(rx + 18, ry - 4, lbl, ha="center", va="bottom", fontsize=8.5, fontweight="bold",
                 color="#FFFFFF" if col != COLORS["yellow"] else COLORS["dark"],
                 bbox=dict(boxstyle="round,pad=0.2", facecolor=col, edgecolor="none"))
    ax2.axis("off")

    fig.tight_layout(pad=1.2)
    fig.savefig(ASSETS_DIR / "06_mlp_vs_cnn_preview.png", dpi=190, facecolor="#FFFFFF")
    plt.close(fig)


def main() -> None:
    data, elsa_thumb = generate_thumbnails_and_stats()
    generate_charts(data, elsa_thumb)
    print(f"✅ Aset visual & JSON P02 (Computer Vision 101) selesai dibuat di: {ASSETS_DIR}")
    print(f"   Dataset Frozen v1: {data['total_images']} foto ({data['polos_count']} polos, {data['ramai_count']} ramai)")
    print(f"   Mini 4-pixel forward pass x={data['mini_forward_pass']['x']} -> probs={data['mini_forward_pass']['probs']}")


if __name__ == "__main__":
    main()
