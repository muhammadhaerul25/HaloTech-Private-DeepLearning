"""Generate deterministic visual assets & real Frozen v1 data JSON for P02: Teori Neural Network.

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
        "03_flatten_frozen_visual.png",
        "03a_one_pixel_one_neuron.png",
        "03b_flatten_to_input_layer.png",
        "03b_elsa_rgb_flatten_transform.png",
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

    # Real 4x4 Elsa pixel sample (tightly framed on Elsa's figurine) for Slide 21 Flatten animation
    fp_elsa_main = _pick_sample_image("elsa", "polos", idx=1)
    with Image.open(fp_elsa_main) as im_e:
        im_e_rgb = im_e.convert("RGB")
        ew_o, eh_o = im_e_rgb.size
        side_f = int(min(ew_o, eh_o) * 0.32)
        cx_f, cy_f = int(ew_o * 0.43), int(eh_o * 0.46)
        left_f = max(0, min(ew_o - side_f, cx_f - side_f // 2))
        top_f = max(0, min(eh_o - side_f, cy_f - side_f // 2))
        elsa_crop_4x4 = im_e_rgb.crop((left_f, top_f, left_f + side_f, top_f + side_f))
        elsa_220 = elsa_crop_4x4.resize((220, 220), Image.Resampling.LANCZOS)
        elsa_220.save(ASSETS_DIR / "thumb_elsa_flatten.jpg", quality=92)
        e4_full = np.array(elsa_220, dtype=np.float32)
        bg_med = np.median(e4_full[:30, :30].reshape(-1, 3), axis=0)
        blk_step = e4_full.shape[0] // 4
        flatten_4x4 = []
        for r in range(4):
            for c in range(4):
                blk = e4_full[r * blk_step : (r + 1) * blk_step, c * blk_step : (c + 1) * blk_step].reshape(-1, 3)
                dist = np.linalg.norm(blk - bg_med, axis=1)
                fg = blk[dist > 28.0]
                if len(fg) / len(blk) >= 0.12:
                    # True representative real pixel from Elsa figurine in this block (not washed out by wall average)
                    top_fg = fg[np.argsort(np.linalg.norm(fg - bg_med, axis=1))[len(fg) // 3 :]]
                    rgb_val = [int(v) for v in np.median(top_fg, axis=0)]
                else:
                    rgb_val = [int(v) for v in np.median(blk, axis=0)]
                gray_val = (0.299 * rgb_val[0] + 0.587 * rgb_val[1] + 0.114 * rgb_val[2]) / 255.0
                flatten_4x4.append(
                    {
                        "idx": r * 4 + c + 1,
                        "row": r,
                        "col": c,
                        "rgb": rgb_val,
                        "gray": round(float(gray_val), 2),
                    }
                )

    # Real 8x8 Elsa pixel grid (64 real pixels from thumb_elsa.jpg) for Slide 22 per-pixel animation & click inspector
    elsa_thumb_arr = np.array(elsa_thumb_img, dtype=np.float32)
    grid_n = 8
    step_g = elsa_thumb_arr.shape[0] / grid_n
    elsa_grid_8x8 = []
    dress_best_idx = 35
    dress_best_score = -999.0
    for r in range(grid_n):
        for c in range(grid_n):
            y0_g, y1_g = int(round(r * step_g)), int(round((r + 1) * step_g))
            x0_g, x1_g = int(round(c * step_g)), int(round((c + 1) * step_g))
            blk = elsa_thumb_arr[y0_g:y1_g, x0_g:x1_g, :].reshape(-1, 3)
            # Sample median RGB of each grid square for crisp true pixel representation
            med = np.median(blk, axis=0)
            rgb_i = [int(np.clip(round(float(v)), 0, 255)) for v in med]
            norm_f = [round(v / 255.0, 2) for v in rgb_i]
            gray_f = round((0.299 * rgb_i[0] + 0.587 * rgb_i[1] + 0.114 * rgb_i[2]) / 255.0, 2)
            idx_g = r * grid_n + c
            elsa_grid_8x8.append(
                {
                    "idx": idx_g + 1,
                    "r": r,
                    "c": c,
                    "rgb": rgb_i,
                    "norm": norm_f,
                    "gray": gray_f,
                }
            )
            # Identify the bluest pixel on Elsa's figurine dress (center region)
            if 2 <= r <= 5 and 2 <= c <= 5:
                blueness = rgb_i[2] - 0.5 * (rgb_i[0] + rgb_i[1])
                if blueness > dress_best_score:
                    dress_best_score = blueness
                    dress_best_idx = idx_g

    elsa_rgb_ends = {
        "first_rgb": elsa_grid_8x8[0]["norm"],
        "last_rgb": elsa_grid_8x8[-1]["norm"],
        "first_gray": [elsa_grid_8x8[0]["gray"], elsa_grid_8x8[1]["gray"], elsa_grid_8x8[2]["gray"]],
        "last_gray": [elsa_grid_8x8[-2]["gray"], elsa_grid_8x8[-1]["gray"]],
        "grid_n": grid_n,
        "dress_idx": int(dress_best_idx),
        "grid": elsa_grid_8x8,
    }

    # Real 5-class Frozen training math demo on FULL 224x224x3 = 150,528 real pixels
    # (100% consistent with Input Layer neuron count & full RGB triplets on Slide 22–25!)
    X_full_list = []
    sample6_x = []
    for kls in CLASSES:
        with Image.open(ASSETS_DIR / f"thumb_{kls}.jpg") as im_tm:
            im_224 = im_tm.convert("RGB").resize((224, 224), Image.Resampling.LANCZOS)
            flat_tm = np.array(im_224, dtype=np.float64).reshape(-1) / 255.0  # exact 150,528 pixels!
        X_full_list.append(flat_tm)
        sample6_x.append(
            [
                round(float(flat_tm[0]), 2),
                round(float(flat_tm[1]), 2),
                round(float(flat_tm[2]), 2),
                round(float(flat_tm[-3]), 2),
                round(float(flat_tm[-2]), 2),
                round(float(flat_tm[-1]), 2),
            ]
        )
    X_full = np.stack(X_full_list, axis=0)  # (5, 150528)
    n_pix_total = int(X_full.shape[1])       # 150,528
    sample_idx = [0, 1, 2, n_pix_total - 3, n_pix_total - 2, n_pix_total - 1]
    n_pix_mid = n_pix_total - len(sample_idx)  # 150,522

    rng_tm = np.random.default_rng(7)
    W0_full = rng_tm.normal(0.0, 0.0025, size=(n_pix_total, 5))
    b0_tm = np.round(rng_tm.uniform(-0.25, 0.25, size=(5,)), 2)

    W_full = np.zeros((n_pix_total, 5), dtype=np.float64)
    b_tm = np.zeros((5,), dtype=np.float64)
    Y_tm = np.eye(5)
    for _ in range(600):
        lg_tm = X_full @ W_full + b_tm
        lg_tm -= lg_tm.max(axis=1, keepdims=True)
        pr_tm = np.exp(lg_tm) / np.exp(lg_tm).sum(axis=1, keepdims=True)
        dZ_tm = (pr_tm - Y_tm) / 5.0
        W_full -= 0.00018 * (X_full.T @ dZ_tm + 45.0 * W_full)
        b_tm -= 3.5 * dZ_tm.sum(axis=0)
    b_tm = np.round(b_tm, 2)

    def _pack_weights(W_mat: np.ndarray) -> tuple[list[list[float]], list[list[float]]]:
        w_samp = [[round(float(W_mat[m, c]), 4) for c in range(5)] for m in sample_idx]
        mid_sums = []
        for i_ph in range(5):
            row_mids = []
            for c in range(5):
                tot_wx = float(X_full[i_ph] @ W_mat[:, c])
                samp_wx = sum(sample6_x[i_ph][k_s] * w_samp[k_s][c] for k_s in range(len(sample_idx)))
                row_mids.append(round(tot_wx - samp_wx, 2))
            mid_sums.append(row_mids)
        return w_samp, mid_sums

    W0_samp, mid0_sums = _pack_weights(W0_full)
    W_samp, mid_sums = _pack_weights(W_full)

    training_math_demo = {
        "n_input": n_pix_total,
        "n_mid": n_pix_mid,
        "sample_ids": ["x1", "x2", "x3", "x150.526", "x150.527", "x150.528"],
        "sample_names": ["Piksel 1 (R)", "Piksel 1 (G)", "Piksel 1 (B)", "Piksel akhir (R)", "Piksel akhir (G)", "Piksel akhir (B)"],
        "classes": [c.capitalize() for c in CLASSES],
        "thumbs": [f"assets/P02/thumb_{c}.jpg" for c in CLASSES],
        "X_sample": sample6_x,
        "W0_sample": W0_samp,
        "mid0": mid0_sums,
        "b0": [round(float(v), 2) for v in b0_tm],
        "W_sample": W_samp,
        "mid_trained": mid_sums,
        "b_trained": [round(float(v), 2) for v in b_tm],
    }

    # Real 1-Layer Full Neural Network (150,528 Input -> 5 Output Softmax = 752,645 params — ZERO Hidden Layer!)
    # for Ultimate Slide 29: tracks ALL 5 characters across ALL 8 Epochs so students can watch full training progress!
    Xc_1l = (X_full - 0.5).astype(np.float64)
    Y_1l = np.eye(5, dtype=np.float64)
    rng_1l = np.random.default_rng(7)
    W_1l = rng_1l.normal(0.0, 0.0028, size=(n_pix_total, 5)).astype(np.float64)
    b_1l = rng_1l.normal(0.0, 0.25, size=(5,)).astype(np.float64)
    lr_w_1l, lr_b_1l = 0.00026, 0.25

    full_nn_epochs = []
    for ep_i in range(1, 9):
        wx_e = Xc_1l @ W_1l
        z_e = wx_e + b_1l
        z_s = z_e - z_e.max(axis=1, keepdims=True)
        ex_e = np.exp(z_s)
        pr_e = ex_e / ex_e.sum(axis=1, keepdims=True)
        ep_rows = []
        for ph_i in range(5):
            probs_ph = [round(float(pr_e[ph_i, c]) * 100.0, 1) for c in range(5)]
            wx_ph = [round(float(wx_e[ph_i, c]), 2) for c in range(5)]
            b_ph = [round(float(b_1l[c]), 2) for c in range(5)]
            z_ph = [round(float(z_e[ph_i, c]), 2) for c in range(5)]
            p_true_f = max(float(pr_e[ph_i, ph_i]), 1e-6)
            loss_ph = round(float(-np.log(p_true_f)), 2)
            ep_rows.append(
                {
                    "wx": wx_ph,
                    "b": b_ph,
                    "z": z_ph,
                    "probs": probs_ph,
                    "pred": int(np.argmax(pr_e[ph_i])),
                    "loss": loss_ph,
                    "ok": bool(int(np.argmax(pr_e[ph_i])) == ph_i),
                }
            )
        avg_loss = round(float(np.mean([r["loss"] for r in ep_rows])), 2)
        acc_cnt = sum(1 for r in ep_rows if r["ok"])
        full_nn_epochs.append({"epoch": ep_i, "avg_loss": avg_loss, "acc": acc_cnt, "photos": ep_rows})

        # 1 full epoch of real gradient descent updates across all 5 Frozen photos (Anna -> Elsa -> Kristoff -> Olaf -> Sven)
        for ph_step in range(5):
            xi = Xc_1l[ph_step : ph_step + 1]
            yi = Y_1l[ph_step : ph_step + 1]
            zi = xi @ W_1l + b_1l
            zi -= zi.max(axis=1, keepdims=True)
            pi = np.exp(zi) / np.exp(zi).sum(axis=1, keepdims=True)
            dZ = pi - yi
            W_1l -= lr_w_1l * (xi.T @ dZ + 0.02 * W_1l)
            b_1l -= lr_b_1l * dZ[0]

    full_nn_demo = {
        "n_input": n_pix_total,
        "n_output": 5,
        "total_params": n_pix_total * 5 + 5,  # 752,645 (150,528 x 5 + 5 bias)
        "classes": [c.capitalize() for c in CLASSES],
        "thumbs": [f"assets/P02/thumb_{c}.jpg" for c in CLASSES],
        "X_sample": sample6_x,
        "epochs": full_nn_epochs,
    }

    p02_data = {
        "dataset_name": summary["dataset_name"],
        "total_images": int(len(meta_df)),
        "classes": CLASSES,
        "polos_count": int((meta_df["kondisi"] == "polos").sum()),
        "ramai_count": int((meta_df["kondisi"] == "ramai").sum()),
        "sessions_count": int(meta_df["sesi_foto"].nunique()),
        "char_samples": char_samples,
        "mini_forward_pass": mini_fp,
        "flatten_4x4": flatten_4x4,
        "elsa_rgb_ends": elsa_rgb_ends,
        "training_math_demo": training_math_demo,
        "full_nn_demo": full_nn_demo,
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

    # 3a. Prepare real Elsa arrays for Slide 22 1D Flatten strip (Slide 20 is now live interactive 60fps HTML/Canvas)
    fp_elsa = _pick_sample_image("elsa", "polos", idx=1)
    with Image.open(fp_elsa) as im:
        elsa_sq = _center_crop_square(im.convert("RGB"), crop_frac=0.58).resize((180, 180), Image.Resampling.LANCZOS)
        elsa_arr180 = np.array(elsa_sq)
        elsa_arr160 = np.array(elsa_sq.resize((160, 160), Image.Resampling.LANCZOS))

    # Real first & last normalized RGB pixel values from Elsa photo (no hardcoded dummy numbers!)
    p_first = elsa_arr180[0, 0].astype(np.float32) / 255.0
    p_last = elsa_arr180[-1, -1].astype(np.float32) / 255.0

    # 3b. Slide 22 Standalone 1D Flattened Color Strip from REAL Elsa RGB pixels (used inside enlarged interactive Slide 22)
    with Image.open(ASSETS_DIR / "thumb_elsa_flatten.jpg") as im_fl:
        fl_20 = np.array(im_fl.convert("RGB").resize((20, 20), Image.Resampling.BILINEAR))
    strip_1d = fl_20.reshape(-1, 1, 3)  # genuine (400, 1, 3) unrolled row-by-row
    strip_vis = np.repeat(strip_1d, 72, axis=1)
    Image.fromarray(strip_vis, mode="RGB").save(ASSETS_DIR / "03c_elsa_flatten_strip.png")

    # 4. Mini 2x2 Real Elsa Patch for Forward Pass Slide 30
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


def generate_handson_visuals(data: dict, elsa_thumb: Image.Image) -> dict:
    """Generate 6 crisp, real Matplotlib visual previews for Hands-On Slides 40-45 (Bab 3 Tahap 1-5)."""
    import os
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    from PIL import ImageOps
    import tensorflow as tf

    np.random.seed(SEED)
    tf.keras.utils.set_random_seed(SEED)

    # Load all Frozen photos deterministically (sorted by file, EXIF-safe, 64x64 RGB, 0.0-1.0)
    meta_df = pd.read_csv(FROZEN_DIR / "metadata.csv").sort_values("file").reset_index(drop=True)
    label_to_idx = {k: i for i, k in enumerate(CLASSES)}
    SMALL = 64
    X_all, y_all, cond_all = [], [], []
    sample_polos_idx, sample_ramai_idx = {}, {}
    for _, row in meta_df.iterrows():
        with Image.open(FROZEN_DIR / row["file"]) as im:
            im_ok = ImageOps.exif_transpose(im).convert("RGB").resize((SMALL, SMALL), Image.Resampling.LANCZOS)
            arr = np.array(im_ok, dtype=np.float32) / 255.0
        X_all.append(arr)
        y_all.append(label_to_idx[row["kelas"]])
        cond_all.append(row["kondisi"])
        if row["kondisi"] == "polos" and row["kelas"] not in sample_polos_idx:
            sample_polos_idx[row["kelas"]] = len(X_all) - 1
        if row["kondisi"] == "ramai" and row["kelas"] not in sample_ramai_idx:
            sample_ramai_idx[row["kelas"]] = len(X_all) - 1

    X_all = np.array(X_all, dtype=np.float32)
    y_all = np.array(y_all, dtype=np.int32)
    cond_all = np.array(cond_all)
    samp_indices = [sample_polos_idx[k] for k in CLASSES]
    ramai_indices = [sample_ramai_idx[k] for k in CLASSES]

    # Use real cropped Elsa thumb for super crisp 8x8 pixel & flatten visuals
    elsa_mini = np.array(elsa_thumb.resize((8, 8), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    pr, pc = 4, 2  # Directly on Elsa's blue dress!
    px_rgb = elsa_mini[pr, pc]
    wall_rgb = elsa_mini[0, 0]
    r_v, g_v, b_v = float(px_rgb[0]), float(px_rgb[1]), float(px_rgb[2])
    wr_v, wg_v, wb_v = float(wall_rgb[0]), float(wall_rgb[1]), float(wall_rgb[2])

    # ------------------------------------------------------------------
    # HO-1: Tahap 1 (1.1 & 1.2) — Foto Asli -> Grid 8x8 Angka -> Zoom 1 Piksel RGB
    # ------------------------------------------------------------------
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8.8, 3.1), dpi=180, gridspec_kw={"width_ratios": [1.0, 1.15, 1.18]})
    ax1.imshow(elsa_thumb)
    step_e = elsa_thumb.size[0] / 8.0
    ax1.add_patch(patches.Rectangle((pc * step_e, pr * step_e), step_e, step_e, lw=2.6, edgecolor=COLORS["red"], facecolor="none"))
    ax1.set_title(f"1. Foto Asli Elsa\n(kotak merah = [{pr}, {pc}] gaun)", fontsize=9.0, fontweight="bold", color=COLORS["dark"])
    ax1.axis("off")

    ax2.imshow(elsa_mini, interpolation="nearest")
    for rr in range(8):
        for cc in range(8):
            lum = 0.299 * elsa_mini[rr, cc, 0] + 0.587 * elsa_mini[rr, cc, 1] + 0.114 * elsa_mini[rr, cc, 2]
            txt_col = "#FFFFFF" if lum < 0.54 else "#202124"
            ax2.text(cc, rr, f"{lum:.1f}", ha="center", va="center", fontsize=6.5, fontweight="bold", color=txt_col)
    ax2.add_patch(patches.Rectangle((pc - 0.5, pr - 0.5), 1, 1, lw=2.6, edgecolor=COLORS["red"], facecolor="none"))
    ax2.set_xticks(range(8)); ax2.set_yticks(range(8))
    ax2.tick_params(labelsize=6.4, length=0)
    ax2.set_title("2. Grid 8×8 (Angka = kecerahan)\nTiap kotak berisi 3 angka R, G, B", fontsize=8.8, fontweight="bold", color=COLORS["blue_dark"])

    bars = ax3.bar(["R", "G", "B"], [r_v, g_v, b_v], color=[COLORS["red"], COLORS["green"], COLORS["blue"]], width=0.48, edgecolor="#202124", lw=0.8)
    for bar, val in zip(bars, [r_v, g_v, b_v]):
        ax3.text(bar.get_x() + bar.get_width() / 2, val + 0.035, f"{val:.2f}", ha="center", va="bottom", fontsize=8.8, fontweight="bold", color=COLORS["dark"])
    swatch = patches.FancyBboxPatch((0.05, 0.79), 0.24, 0.16, boxstyle="round,pad=0.02", transform=ax3.transAxes, facecolor=px_rgb, edgecolor="#202124", lw=1.4)
    ax3.add_patch(swatch)
    ax3.text(0.33, 0.87, f"Warna asli [{pr}, {pc}]\nRGB = [{r_v:.2f}, {g_v:.2f}, {b_v:.2f}]", transform=ax3.transAxes, ha="left", va="center", fontsize=6.9, fontweight="bold", color=COLORS["dark"])
    ax3.set_ylim(0, 1.15)
    ax3.set_ylabel("Nilai (0.0 – 1.0)", fontsize=8)
    ax3.set_title(f"3. Zoom Piksel [{pr}, {pc}]\nBiru (B) paling dominan!", fontsize=8.8, fontweight="bold", color="#137333")
    ax3.grid(axis="y", linestyle="--", alpha=0.35)
    ax3.spines["top"].set_visible(False); ax3.spines["right"].set_visible(False)

    fig.tight_layout(pad=0.9)
    fig.savefig(ASSETS_DIR / "ho_step1_pixel_grid.png", dpi=180, facecolor="#FFFFFF")
    plt.close(fig)

    # ------------------------------------------------------------------
    # HO-2: Tahap 2 (2.1 & 2.2) — Visual 2D -> Pita 1D Flatten (P1..P64 = x1..x192) + Skala Parameter
    # ------------------------------------------------------------------
    fig = plt.figure(figsize=(8.8, 3.25), dpi=180)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1.0], width_ratios=[1.0, 2.55], hspace=0.55, wspace=0.22)
    ax_2d = fig.add_subplot(gs[0, 0])
    ax_1d = fig.add_subplot(gs[0, 1])
    ax_sc = fig.add_subplot(gs[1, :])

    ax_2d.imshow(elsa_mini, interpolation="nearest")
    for rr in range(8):
        ax_2d.axhline(rr - 0.5, color="#FFFFFF", lw=0.7, alpha=0.85)
    ax_2d.set_yticks(range(8))
    ax_2d.set_yticklabels([f"B{i+1}" for i in range(8)], fontsize=6.2, fontweight="bold", color=COLORS["blue_dark"])
    ax_2d.set_xticks([])
    ax_2d.set_title("2D: 8×8 Piksel", fontsize=8.8, fontweight="bold", color=COLORS["dark"])

    strip_rgb = elsa_mini.reshape(1, 64, 3)
    ax_1d.imshow(strip_rgb, aspect="auto", interpolation="nearest")
    for b_idx in range(1, 8):
        ax_1d.axvline(b_idx * 8 - 0.5, color="#FFFFFF", lw=1.4)
    for b_idx in range(8):
        ax_1d.text(b_idx * 8 + 3.5, 0.0, f"B{b_idx+1}", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#FFFFFF",
                   bbox=dict(boxstyle="round,pad=0.14", facecolor="#202124", edgecolor="none", alpha=0.68))
    ax_1d.set_yticks([])
    ax_1d.set_xticks([0, 15, 31, 47, 63])
    ax_1d.set_xticklabels(["P1 (x1–3)", "P16", "P32", "P48", "P64 (x190–192)"], fontsize=6.9, fontweight="bold")
    ax_1d.set_title("Sesudah Flatten() → 64 Piksel Warna × 3 RGB = 192 Neuron Input", fontsize=8.6, fontweight="bold", color="#137333")

    labels_sc = ["Mini 8×8×3\n(192 neuron)", "Hands-On 64×64×3\n(12.288 neuron)", "Penuh 224×224×3\n(150.528 neuron)"]
    vals_sc = [192 * 5 + 5, 12288 * 5 + 5, 150528 * 5 + 5]
    cols_sc = [COLORS["green"], COLORS["blue"], COLORS["red"]]
    y_pos = np.arange(len(labels_sc))
    bh = ax_sc.barh(y_pos, vals_sc, color=cols_sc, height=0.58, edgecolor="#202124", lw=0.6)
    ax_sc.set_xscale("log")
    ax_sc.set_xlim(100, 28_000_000)
    ax_sc.set_yticks(y_pos); ax_sc.set_yticklabels(labels_sc, fontsize=7.6, fontweight="bold")
    ax_sc.invert_yaxis()
    for b_bar, vv in zip(bh, vals_sc):
        ax_sc.text(vv * 1.22, b_bar.get_y() + b_bar.get_height() / 2, f"{vv:,} param (W+b)".replace(",", "."), va="center", fontsize=8.1, fontweight="bold", color=COLORS["dark"])
    ax_sc.set_title("Perbandingan Total Parameter (Input × 5 Kelas + 5 Bias) — Skala Log", fontsize=8.6, fontweight="bold", color=COLORS["dark"])
    ax_sc.grid(axis="x", linestyle="--", alpha=0.3)
    ax_sc.spines["top"].set_visible(False); ax_sc.spines["right"].set_visible(False)

    fig.subplots_adjust(left=0.17, right=0.95, top=0.90, bottom=0.11)
    fig.savefig(ASSETS_DIR / "ho_step2_flatten_strip.png", dpi=180, facecolor="#FFFFFF")
    plt.close(fig)

    # ------------------------------------------------------------------
    # HO-3: Tahap 3 (3.1, 3.2, 3.3) — Zero-Sum Blue Detector (Gaun > 0 vs Dinding < 0!) + ReLU + Softmax & Loss!
    # ------------------------------------------------------------------
    w_r, w_g, w_b, b_val = -3.0, -2.0, 5.0, -0.05
    c_r, c_g, c_b = r_v * w_r, g_v * w_g, b_v * w_b
    z_neuron = c_r + c_g + c_b + b_val
    z_wall = (wr_v * w_r) + (wg_v * w_g) + (wb_v * w_b) + b_val

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8.8, 3.05), dpi=180)
    parts = [c_r, c_g, c_b, b_val, z_neuron]
    p_lbls = ["R·wR", "G·wG", "B·wB", "Bias", "z Gaun"]
    p_cols = [COLORS["red"] if v < 0 else COLORS["green"] for v in parts[:-1]] + [COLORS["blue"]]
    b1 = ax1.bar(p_lbls, parts, color=p_cols, width=0.56, edgecolor="#202124", lw=0.7)
    ax1.axhline(0, color="#202124", lw=0.9)
    for bar, v in zip(b1, parts):
        ax1.text(bar.get_x() + bar.get_width() / 2, v + (0.06 if v >= 0 else -0.07), f"{v:+.2f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=7.4, fontweight="bold")
    ax1.set_ylim(min(parts) - 0.65, max(parts) + 1.25)
    ax1.text(0.97, 0.96, f"Dinding [0,0] → z = {z_wall:+.2f}", transform=ax1.transAxes, ha="right", va="top",
             fontsize=6.9, fontweight="bold", color=COLORS["muted"],
             bbox=dict(boxstyle="round,pad=0.22", facecolor="#F8F9FA", edgecolor="#DADCE0"))
    ax1.set_title("3.1 Timbangan 1 Neuron\nz = r·wR + g·wG + b·wB + bias", fontsize=8.4, fontweight="bold", color=COLORS["dark"])
    ax1.tick_params(labelsize=7.2); ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    skor_ex = np.array([-1.2, -0.4, 0.0, 0.8, 2.1])
    relu_ex = np.maximum(0.0, skor_ex)
    xx = np.arange(len(skor_ex))
    ax2.bar(xx - 0.18, skor_ex, width=0.34, color="#DADCE0", edgecolor="#5F6368", label="Sebelum")
    ax2.bar(xx + 0.18, relu_ex, width=0.34, color=COLORS["green"], edgecolor="#137333", label="Sesudah ReLU")
    ax2.axhline(0, color="#202124", lw=0.9)
    ax2.set_xticks(xx); ax2.set_xticklabels([f"{v:+.1f}" for v in skor_ex], fontsize=7.4)
    ax2.set_ylim(-1.6, 2.6)
    ax2.set_title("3.2 ReLU: Minus → 0\nPositif tetap menyala", fontsize=8.4, fontweight="bold", color="#137333")
    ax2.legend(fontsize=6.9, loc="upper left", framealpha=0.9)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    z5 = np.array([0.4, 2.3, 0.1, -0.2, 0.2])
    ez = np.exp(z5 - np.max(z5))
    pr5_prob = ez / np.sum(ez)
    pr5 = pr5_prob * 100.0
    loss_elsa_demo = float(-np.log(pr5_prob[1]))
    c_names = [c.capitalize() for c in CLASSES]
    bar_cols = [COLORS["green"] if i == int(np.argmax(pr5)) else COLORS["blue"] for i in range(5)]
    b3 = ax3.barh(c_names, pr5, color=bar_cols, height=0.56, edgecolor="#202124", lw=0.6)
    ax3.invert_yaxis(); ax3.set_xlim(0, 102)
    for bar, v in zip(b3, pr5):
        ax3.text(v + 2, bar.get_y() + bar.get_height() / 2, f"{v:.1f}%", va="center", fontsize=7.6, fontweight="bold")
    ax3.text(0.97, 0.06, f"Loss (−ln P) = {loss_elsa_demo:.2f}", transform=ax3.transAxes, ha="right", va="bottom",
             fontsize=7.2, fontweight="bold", color="#137333",
             bbox=dict(boxstyle="round,pad=0.25", facecolor="#E6F4EA", edgecolor=COLORS["green"]))
    ax3.set_title("3.3 Softmax (100%) & Loss\nArgmax = ELSA ✓", fontsize=8.4, fontweight="bold", color=COLORS["blue_dark"])
    ax3.tick_params(labelsize=7.6); ax3.grid(axis="x", linestyle="--", alpha=0.3)
    ax3.spines["top"].set_visible(False); ax3.spines["right"].set_visible(False)

    fig.tight_layout(pad=0.9)
    fig.savefig(ASSETS_DIR / "ho_step3_neuron_relu_softmax.png", dpi=180, facecolor="#FFFFFF")
    plt.close(fig)

    # ------------------------------------------------------------------
    # Build & evaluate REAL 1-Layer Keras model (Epoch 0 Baby -> Epoch 20 Trained)
    # ------------------------------------------------------------------
    tf.keras.utils.set_random_seed(SEED)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(SMALL, SMALL, 3)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(len(CLASSES), activation="softmax"),
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    W_init = model.layers[-1].get_weights()[0].copy()
    loss_e0, acc_e0 = model.evaluate(X_all, y_all, verbose=0)
    probs_e0 = model.predict(X_all[samp_indices], verbose=0)

    # HO-4: Tahap 4 — Tebakan "Model Bayi" (Epoch 0, Bobot Acak!)
    fig, axes = plt.subplots(2, 5, figsize=(8.8, 3.1), dpi=180, gridspec_kw={"height_ratios": [1.25, 1.0], "hspace": 0.36, "wspace": 0.25})
    short_lbl = ["A", "E", "K", "O", "S"]
    for i, idx_s in enumerate(samp_indices):
        axes[0, i].imshow(X_all[idx_s])
        pred_i = int(np.argmax(probs_e0[i]))
        ok = pred_i == y_all[idx_s]
        t_col = "#137333" if ok else "#C5221F"
        for sp in axes[0, i].spines.values():
            sp.set_edgecolor(t_col); sp.set_linewidth(2.0)
        axes[0, i].set_xticks([]); axes[0, i].set_yticks([])
        axes[0, i].set_title(f"Asli: {CLASSES[i].capitalize()}\nTebak: {CLASSES[pred_i].capitalize()} {'✓' if ok else '✗'}", fontsize=7.5, fontweight="bold", color=t_col)
        b_col = [COLORS["green"] if j == y_all[idx_s] else "#BDC1C6" for j in range(5)]
        axes[1, i].bar(short_lbl, probs_e0[i] * 100.0, color=b_col, width=0.65)
        axes[1, i].axhline(20, color="#9AA0A6", lw=0.8, linestyle="--")
        axes[1, i].set_ylim(0, 100); axes[1, i].tick_params(labelsize=6.8)
        axes[1, i].spines["top"].set_visible(False); axes[1, i].spines["right"].set_visible(False)
        if i == 0:
            axes[1, i].set_ylabel("Prob %", fontsize=7.2)
    fig.suptitle(f"Epoch 0 (Model Bayi / Bobot Acak) · 61.445 Parameter · Loss = {loss_e0:.2f} · Akurasi = {acc_e0*100:.1f}%", fontsize=9.1, fontweight="bold", color="#C5221F", y=0.98)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.80, bottom=0.10)
    fig.savefig(ASSETS_DIR / "ho_step4_baby_model.png", dpi=180, facecolor="#FFFFFF")
    plt.close(fig)

    # Train 20 real epochs (monotonic curve E1 -> E20 & clear weight silhouettes!)
    n_ep = 20
    hist = model.fit(X_all, y_all, epochs=n_ep, batch_size=16, verbose=0)
    losses = [float(v) for v in hist.history["loss"]]
    accs = [float(v) * 100.0 for v in hist.history["accuracy"]]
    probs_e20 = model.predict(X_all[samp_indices], verbose=0)
    probs_ramai = model.predict(X_all[ramai_indices], verbose=0)
    _, acc_polos_all = model.evaluate(X_all[cond_all == "polos"], y_all[cond_all == "polos"], verbose=0)
    _, acc_ramai_all = model.evaluate(X_all[cond_all == "ramai"], y_all[cond_all == "ramai"], verbose=0)

    # HO-5: Tahap 5.1 & 5.2 — Kurva Training Loss & Accuracy (20 Epoch Nyata)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.05), dpi=180)
    ep = list(range(1, n_ep + 1))
    ax1.plot(ep, losses, marker="o", color=COLORS["red"], lw=2.2, markersize=4.5)
    ax1.fill_between(ep, losses, min(losses) * 0.85, color=COLORS["red"], alpha=0.10)
    ax1.annotate(f"E1: {losses[0]:.2f}", (1, losses[0]), textcoords="offset points", xytext=(9, -3), fontsize=8.0, fontweight="bold", color="#C5221F",
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="#FCE8E6", edgecolor=COLORS["red"], lw=0.8))
    ax1.annotate(f"E{n_ep}: {losses[-1]:.2f}", (n_ep, losses[-1]), textcoords="offset points", xytext=(-58, 16), fontsize=8.2, fontweight="bold", color="#137333",
                 bbox=dict(boxstyle="round,pad=0.22", facecolor="#E6F4EA", edgecolor=COLORS["green"], lw=0.9))
    ax1.set_title(f"Kurva Loss Turun Mulus (Epoch 1 → {n_ep})", fontsize=9.2, fontweight="bold", color=COLORS["dark"])
    ax1.set_xlabel("Epoch", fontsize=8); ax1.set_ylabel("Cross-Entropy Loss", fontsize=8)
    ax1.set_xticks([1, 5, 10, 15, 20]); ax1.grid(True, linestyle="--", alpha=0.35)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    ax2.plot(ep, accs, marker="s", color=COLORS["green"], lw=2.2, markersize=4.5)
    ax2.fill_between(ep, accs, 0, color=COLORS["green"], alpha=0.10)
    ax2.annotate(f"E1: {accs[0]:.1f}%", (1, accs[0]), textcoords="offset points", xytext=(9, -15), fontsize=8.0, fontweight="bold", color=COLORS["muted"],
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="#F8F9FA", edgecolor="#DADCE0", lw=0.8))
    ax2.annotate(f"E{n_ep}: {accs[-1]:.1f}%", (n_ep, accs[-1]), textcoords="offset points", xytext=(-64, 12), fontsize=8.2, fontweight="bold", color="#137333",
                 bbox=dict(boxstyle="round,pad=0.22", facecolor="#E6F4EA", edgecolor=COLORS["green"], lw=0.9))
    ax2.set_title(f"Kurva Akurasi Naik (Epoch 1 → {n_ep})", fontsize=9.2, fontweight="bold", color=COLORS["dark"])
    ax2.set_xlabel("Epoch", fontsize=8); ax2.set_ylabel("Akurasi (%)", fontsize=8)
    ax2.set_xticks([1, 5, 10, 15, 20]); ax2.set_ylim(0, min(105, max(85, max(accs) + 20)))
    ax2.grid(True, linestyle="--", alpha=0.35)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout(pad=1.0)
    fig.savefig(ASSETS_DIR / "ho_step5_loss_curve.png", dpi=180, facecolor="#FFFFFF")
    plt.close(fig)

    # HO-6: Tahap 5.3 & 5.4 — Tebakan Sesudah Belajar (Epoch 20) + Peta Perubahan Bobot ΔW (64x64)!
    W_delta = model.layers[-1].get_weights()[0] - W_init  # Pure learned pattern without init static!
    fig, axes = plt.subplots(2, 5, figsize=(8.8, 3.15), dpi=180, gridspec_kw={"height_ratios": [1.15, 1.05], "hspace": 0.42, "wspace": 0.22})
    for i, idx_s in enumerate(samp_indices):
        axes[0, i].imshow(X_all[idx_s])
        pred_i = int(np.argmax(probs_e20[i]))
        conf = probs_e20[i, pred_i] * 100.0
        ok = pred_i == y_all[idx_s]
        t_col = "#137333" if ok else "#C5221F"
        for sp in axes[0, i].spines.values():
            sp.set_edgecolor(t_col); sp.set_linewidth(2.0)
        axes[0, i].set_xticks([]); axes[0, i].set_yticks([])
        axes[0, i].set_title(f"{CLASSES[i].capitalize()} → {CLASSES[pred_i].capitalize()} ({conf:.0f}%) {'✓' if ok else '✗'}", fontsize=7.3, fontweight="bold", color=t_col)

        w_img = W_delta[:, i].reshape(SMALL, SMALL, 3)
        w_mag = np.mean(np.abs(w_img), axis=2)  # Where neuron focuses most strongly!
        w_hi = max(float(np.percentile(w_mag, 98)), 1e-6)
        axes[1, i].imshow(np.clip(w_mag / w_hi, 0.0, 1.0), cmap="inferno")
        axes[1, i].set_xticks([]); axes[1, i].set_yticks([])
        axes[1, i].set_title(f"Fokus Bobot ΔW: {CLASSES[i].capitalize()}", fontsize=7.2, fontweight="bold", color=COLORS["blue_dark"])

    fig.suptitle(f"Sesudah Belajar (Epoch {n_ep} · Loss {losses[-1]:.2f} · Akurasi {accs[-1]:.1f}%) & Peta Fokus Bobot ΔW", fontsize=8.9, fontweight="bold", color="#137333", y=0.98)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.82, bottom=0.04)
    fig.savefig(ASSETS_DIR / "ho_step6_predict_and_weights.png", dpi=180, facecolor="#FFFFFF")
    plt.close(fig)

    ho_metrics = {
        "elsa_px_pos": [pr, pc],
        "elsa_px_rgb": [round(r_v, 2), round(g_v, 2), round(b_v, 2)],
        "neuron_z": round(z_neuron, 2),
        "wall_z": round(z_wall, 2),
        "softmax_loss_demo": round(loss_elsa_demo, 2),
        "epochs": n_ep,
        "epoch0_loss": round(float(loss_e0), 2),
        "epoch0_acc_pct": round(float(acc_e0) * 100.0, 1),
        "epoch1_loss": round(losses[0], 2),
        "epoch1_acc_pct": round(accs[0], 1),
        "epoch_end_loss": round(losses[-1], 2),
        "epoch_end_acc_pct": round(accs[-1], 1),
        "all_polos_acc_pct": round(float(acc_polos_all) * 100.0, 1),
        "all_ramai_acc_pct": round(float(acc_ramai_all) * 100.0, 1),
        "sample_e0_correct": int(sum(int(np.argmax(probs_e0[i])) == y_all[samp_indices[i]] for i in range(5))),
        "sample_end_correct": int(sum(int(np.argmax(probs_e20[i])) == y_all[samp_indices[i]] for i in range(5))),
        "sample_ramai_correct": int(sum(int(np.argmax(probs_ramai[i])) == y_all[ramai_indices[i]] for i in range(5))),
    }
    data["handson_metrics"] = ho_metrics
    (ASSETS_DIR / "p02_data.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return ho_metrics


def main() -> None:
    data, elsa_thumb = generate_thumbnails_and_stats()
    generate_charts(data, elsa_thumb)
    ho_m = generate_handson_visuals(data, elsa_thumb)
    print(f"✅ Aset visual & JSON P02 (Teori Neural Network) selesai dibuat di: {ASSETS_DIR}")
    print(f"   Dataset Frozen v1: {data['total_images']} foto ({data['polos_count']} polos, {data['ramai_count']} ramai)")
    print(f"   Mini 4-pixel forward pass x={data['mini_forward_pass']['x']} -> probs={data['mini_forward_pass']['probs']}")
    print(f"   Hands-On real Keras 1-Layer: E0 loss={ho_m['epoch0_loss']} ({ho_m['epoch0_acc_pct']}%) -> E{ho_m['epochs']} loss={ho_m['epoch_end_loss']} ({ho_m['epoch_end_acc_pct']}%) | sample {ho_m['sample_e0_correct']}/5 -> {ho_m['sample_end_correct']}/5")


if __name__ == "__main__":
    main()
