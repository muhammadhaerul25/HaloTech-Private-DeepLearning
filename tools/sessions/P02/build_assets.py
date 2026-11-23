"""Generate deterministic visual assets & real Frozen v1 data JSON for P02: Teori Neural Network (ANN).

Outputs saved to `materials/P02/assets/P02/`:
- Real Frozen v1 thumbnails (`thumb_anna.jpg`, `thumb_elsa.jpg`, `thumb_kristoff.jpg`,
  `thumb_olaf.jpg`, `thumb_sven.jpg`, `thumb_elsa_ramai.jpg`)
- `01_frozen_gallery_5classes.png` (Real 2x5 polos vs ramai Frozen figurine showcase)
- `02_linear_vs_nonlinear.png` (Why linear boundaries fail & why activation is needed)
- `03_activation_comparison.png` (ReLU vs Sigmoid vs Tanh curves with clean annotations)
- `04_cross_entropy_penalty.png` (Cross-Entropy Loss penalty curve vs predicted probability)
- `05_flatten_frozen_visual.png` (Real Elsa 2D photo -> 1D flattened strip + param count bar chart)
- `p02_data.json` (Real normalized RGB & dataset stats dynamically read from `data/frozen_v1/`)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageOps

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


def generate_thumbnails_and_stats() -> dict:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = FROZEN_DIR / "dataset_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    meta_df = pd.read_csv(FROZEN_DIR / "metadata.csv")

    char_samples = {}
    for kls in CLASSES:
        fp_polos = _pick_sample_image(kls, "polos", idx=1)
        with Image.open(fp_polos) as im:
            im_rgb = im.convert("RGB")
            sq = _center_crop_square(im_rgb, crop_frac=0.68)
            thumb = sq.resize((220, 220), Image.Resampling.LANCZOS)
            thumb.save(ASSETS_DIR / f"thumb_{kls}.jpg", quality=90)

            # Extract central figurine patch (middle 35%) normalized RGB [0..1] for realistic 1-neuron simulator
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

    # Also save ramai thumbnails for Elsa & Olaf to show contrast polos vs ramai
    for kls in ("elsa", "olaf", "anna"):
        fp_ramai = _pick_sample_image(kls, "ramai", idx=0)
        with Image.open(fp_ramai) as im:
            sq = _center_crop_square(im.convert("RGB"), crop_frac=0.88)
            sq.resize((220, 220), Image.Resampling.LANCZOS).save(ASSETS_DIR / f"thumb_{kls}_ramai.jpg", quality=90)

    p02_data = {
        "dataset_name": summary["dataset_name"],
        "total_images": int(len(meta_df)),
        "classes": CLASSES,
        "polos_count": int((meta_df["kondisi"] == "polos").sum()),
        "ramai_count": int((meta_df["kondisi"] == "ramai").sum()),
        "sessions_count": int(meta_df["sesi_foto"].nunique()),
        "char_samples": char_samples,
    }
    (ASSETS_DIR / "p02_data.json").write_text(json.dumps(p02_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return p02_data


def generate_charts() -> None:
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

    # 2. Linear vs Non-Linear Boundary Intuition (taller aspect ratio to fill slide card cleanly)
    rng = np.random.default_rng(SEED)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 4.9), dpi=190)

    ang1 = rng.uniform(0, 2 * np.pi, 35)
    r1 = rng.normal(0.55, 0.14, 35)
    ang2 = rng.uniform(0, 2 * np.pi, 45)
    r2 = rng.normal(1.65, 0.18, 45)
    for ax, title in [(ax1, "Tanpa Aktivasi (1 Garis Lurus Saja)"), (ax2, "Dengan Aktivasi Non-Linear (ReLU)")]:
        ax.scatter(r1 * np.cos(ang1), r1 * np.sin(ang1), c=COLORS["blue"], s=52, label="Elsa (Biru + Pirang)", edgecolors="#FFFFFF", linewidths=0.7)
        ax.scatter(r2 * np.cos(ang2), r2 * np.sin(ang2), c=COLORS["red"], s=52, label="Karakter / Latar Lain", edgecolors="#FFFFFF", linewidths=0.7)
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-2.4, 2.4)
        ax.set_aspect("equal")
        ax.grid(True, linestyle="--", alpha=0.28)
        ax.set_title(title, fontsize=12, fontweight="bold", color=COLORS["dark"], pad=9)
        ax.tick_params(labelsize=9.5, colors=COLORS["muted"])

    xs = np.linspace(-2.3, 2.3, 100)
    ax1.plot(xs, 0.45 * xs + 0.2, color=COLORS["dark"], linewidth=2.8, linestyle="--", label="Garis Lurus (Gagal Memisah)")
    ax1.legend(loc="lower center", fontsize=8.8, framealpha=0.95)

    theta = np.linspace(0, 2 * np.pi, 200)
    ax2.plot(1.1 * np.cos(theta), 1.1 * np.sin(theta), color=COLORS["green"], linewidth=3.0, label="Batas Melengkung (Berhasil!)")
    ax2.fill(1.1 * np.cos(theta), 1.1 * np.sin(theta), color="#E6F4EA", alpha=0.45)
    ax2.legend(loc="lower center", fontsize=8.8, framealpha=0.95)

    fig.tight_layout(pad=1.2)
    fig.savefig(ASSETS_DIR / "02_linear_vs_nonlinear.png", dpi=190, facecolor="#FFFFFF")
    plt.close(fig)

    # 3. Activation Functions Comparison (ReLU, Sigmoid, Tanh — taller & clearer labels)
    z = np.linspace(-5, 5, 300)
    relu = np.maximum(0, z)
    sigmoid = 1.0 / (1.0 + np.exp(-z))
    tanh = np.tanh(z)

    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.85), dpi=190)
    specs = [
        (axes[0], relu, "1. ReLU (Negatif -> 0)", COLORS["blue"], "Negatif -> 0 (Tidak Aktif)\nPositif -> Tetap Lurus", (-0.5, 5.2)),
        (axes[1], sigmoid, "2. Sigmoid (Persentase 0–100%)", COLORS["red"], "Menekan semua angka\nke rentang 0.0 s.d. 1.0", (-0.15, 1.15)),
        (axes[2], tanh, "3. Tanh (Skala -1 s.d. +1)", COLORS["green"], "Simetris di nol:\nNegatif tetap negatif", (-1.2, 1.2)),
    ]
    for ax, y, ttl, col, note, ylim in specs:
        ax.axhline(0, color="#DADCE0", linewidth=1.2)
        ax.axvline(0, color="#DADCE0", linewidth=1.2)
        ax.plot(z, y, color=col, linewidth=3.4)
        ax.set_title(ttl, fontsize=12, fontweight="bold", color=COLORS["dark"], pad=8)
        ax.set_xlabel("Skor Mentah (z)", fontsize=10, color=COLORS["muted"])
        ax.set_ylim(*ylim)
        ax.grid(True, linestyle=":", alpha=0.45)
        ax.text(0.05, 0.90, note, transform=ax.transAxes, fontsize=9.2, va="top",
                bbox=dict(boxstyle="round,pad=0.38", facecolor="#F8F9FA", edgecolor="#DADCE0"))
    axes[0].set_ylabel("Output Aktivasi", fontsize=10, color=COLORS["muted"])
    fig.tight_layout(pad=1.2)
    fig.savefig(ASSETS_DIR / "03_activation_comparison.png", dpi=190, facecolor="#FFFFFF")
    plt.close(fig)

    # 4. Cross-Entropy Loss Curve (-log(p)) — ZERO OVERLAP annotation coordinates
    p = np.linspace(0.02, 1.0, 250)
    ce = -np.log(p)
    fig, ax = plt.subplots(figsize=(6.8, 4.4), dpi=190)
    ax.plot(p, ce, color=COLORS["red"], linewidth=3.2)
    ax.fill_between(p, ce, alpha=0.10, color=COLORS["red"])
    pts = [
        (0.08, -np.log(0.08), "Salah Percaya Diri! (8%)\nHukuman berat: Loss = 2.53", COLORS["red"], (0.30, 3.10)),
        (0.50, -np.log(0.50), "Masih Ragu-ragu (50%)\nLoss sedang = 0.69", COLORS["yellow"], (0.36, 1.85)),
        (0.92, -np.log(0.92), "Yakin & Benar! (92%)\nLoss kecil = 0.08", COLORS["green"], (0.58, 0.78)),
    ]
    for px, py, txt, col, (tx, ty) in pts:
        ax.scatter([px], [py], color=col, s=85, zorder=5, edgecolors="#202124", linewidths=1.3)
        ax.annotate(
            txt,
            xy=(px, py),
            xytext=(tx, ty),
            fontsize=9.2,
            fontweight="bold",
            color=COLORS["dark"],
            bbox=dict(boxstyle="round,pad=0.38", facecolor="#FFFFFF", edgecolor=col, lw=1.7),
            arrowprops=dict(arrowstyle="->", color=col, lw=1.7, connectionstyle="arc3,rad=0.12"),
        )
    ax.set_title("Cross-Entropy Loss: Hukuman Seberapa Salah Tebakan AI", fontsize=11.8, fontweight="bold", color=COLORS["dark"], pad=9)
    ax.set_xlabel("Peluang yang Diberikan AI pada Kelas yang Benar (p)", fontsize=10, color=COLORS["dark"])
    ax.set_ylabel("Nilai Loss (Makin Kecil Makin Bagus)", fontsize=10, color=COLORS["dark"])
    ax.set_xlim(0, 1.06)
    ax.set_ylim(0, 4.15)
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(ASSETS_DIR / "04_cross_entropy_penalty.png", dpi=190, facecolor="#FFFFFF")
    plt.close(fig)

    # 5. Flatten Real Elsa Photo + Parameter Explosion Bar Chart (bigger fonts, clearer labels)
    fp_elsa = _pick_sample_image("elsa", "polos", idx=1)
    with Image.open(fp_elsa) as im:
        elsa_sq = _center_crop_square(im.convert("RGB"), crop_frac=0.68).resize((160, 160), Image.Resampling.LANCZOS)
        elsa_arr = np.array(elsa_sq)

    fig = plt.figure(figsize=(11.0, 4.2), dpi=190)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 0.95, 1.5], wspace=0.32)
    ax_img = fig.add_subplot(gs[0])
    ax_flat = fig.add_subplot(gs[1])
    ax_bar = fig.add_subplot(gs[2])

    ax_img.imshow(elsa_arr)
    for y_line in range(20, 160, 20):
        ax_img.axhline(y_line, color="#FBBC04", linewidth=1.3, linestyle="--", alpha=0.92)
    ax_img.set_title("1. Foto Elsa Utuh (2D)\nDipecah baris demi baris", fontsize=11.2, fontweight="bold", color=COLORS["dark"], pad=8)
    ax_img.axis("off")

    flat_vec = elsa_arr[::8, ::4, :].reshape(-1, 3)
    strip = np.tile(flat_vec[:, None, :], (1, 28, 1))
    ax_flat.imshow(strip, aspect="auto")
    ax_flat.set_title("2. Vektor 1D (Flatten)\nTetangga atas-bawah terputus!", fontsize=11.2, fontweight="bold", color=COLORS["red"], pad=8)
    ax_flat.set_xticks([])
    ax_flat.set_yticks([0, len(flat_vec) // 2, len(flat_vec) - 1])
    ax_flat.set_yticklabels(["Baris 1", "Tengah", "Akhir"], fontsize=9.8, fontweight="bold", color=COLORS["dark"])

    labels = ["MNIST\n28×28×1", "Frozen Kecil\n64×64×3", "Frozen Standar\n224×224×3"]
    params_m = [
        (28 * 28 * 1 * 128) / 1e6,
        (64 * 64 * 3 * 128) / 1e6,
        (224 * 224 * 3 * 128) / 1e6,
    ]
    bars = ax_bar.bar(labels, params_m, color=[COLORS["green"], COLORS["yellow"], COLORS["red"]], edgecolor="#202124", linewidth=1.1, width=0.52)
    for b, val in zip(bars, params_m):
        ax_bar.text(b.get_x() + b.get_width() / 2, val + 0.6, f"{val:.2f} Juta", ha="center", va="bottom", fontsize=10.5, fontweight="bold", color=COLORS["dark"])
    ax_bar.set_ylim(0, 23.5)
    ax_bar.set_ylabel("Jumlah Bobot Layer 1 (Juta)", fontsize=10, color=COLORS["dark"])
    ax_bar.set_title("3. Ledakan Bobot MLP (128 Neuron)", fontsize=11.2, fontweight="bold", color=COLORS["dark"], pad=8)
    ax_bar.tick_params(labelsize=9.5)
    ax_bar.grid(axis="y", linestyle="--", alpha=0.35)

    fig.subplots_adjust(left=0.03, right=0.98, top=0.84, bottom=0.14, wspace=0.32)
    fig.savefig(ASSETS_DIR / "05_flatten_frozen_visual.png", dpi=190, facecolor="#FFFFFF")
    plt.close(fig)


def main() -> None:
    data = generate_thumbnails_and_stats()
    generate_charts()
    print(f"✅ Aset visual & JSON P02 selesai dibuat di: {ASSETS_DIR}")
    print(f"   Dataset Frozen v1: {data['total_images']} foto ({data['polos_count']} polos, {data['ramai_count']} ramai)")


if __name__ == "__main__":
    main()
