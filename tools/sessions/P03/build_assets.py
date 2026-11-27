"""Generate deterministic visual assets & real Frozen v1 benchmarks for P03: Arsitektur Neural Network.

Outputs saved to `materials/P03/assets/P03/`:
- Real Frozen v1 thumbnails (`thumb_anna.jpg`, `thumb_elsa.jpg`, `thumb_kristoff.jpg`,
  `thumb_olaf.jpg`, `thumb_sven.jpg`, `thumb_elsa_ramai.jpg`, `thumb_olaf_ramai.jpg`)
- `01_p02_handoff_limit.png`
- `02_cnn_conv_pool_elsa.png`
- `03_resnet_skip_gap.png`
- `04_mobilenetv2_depthwise.png`
- `05_efficientnet_compound_se.png`
- `06_5arch_comparison_chart.png`
- `ho_step1_mlp_explosion.png` .. `ho_step6_benchmark_quadrant.png`
- `p03_data.json` (Real dynamic Frozen stats, pixel matrices, Keras benchmarks & training traces)
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from core.registry import get_session  # noqa: E402

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

SESSION = get_session("P03")
FROZEN_DIR = ROOT_DIR / "data" / "frozen_v1"
ASSETS_DIR = SESSION.assets_dir

CLASSES = ["anna", "elsa", "kristoff", "olaf", "sven"]
COLORS = {
    "blue": "#4285F4",
    "blue_dark": "#1A73E8",
    "red": "#EA4335",
    "red_dark": "#C5221F",
    "yellow": "#FBBC04",
    "yellow_dark": "#B06000",
    "green": "#34A853",
    "green_dark": "#137333",
    "purple": "#8E24AA",
    "dark": "#202124",
    "muted": "#5F6368",
    "surface": "#F8F9FA",
    "border": "#DADCE0",
}


def _pick_sample_image(kelas: str, kondisi: str, idx: int = 0) -> Path:
    folder = FROZEN_DIR / kelas / kondisi
    files = sorted(folder.glob("*.jpg"))
    if not files:
        raise FileNotFoundError(f"Tidak ditemukan foto di {folder}")
    return files[min(idx, len(files) - 1)]


def _center_crop_square(im: Image.Image, crop_frac: float = 0.72) -> Image.Image:
    w, h = im.size
    side = int(min(w, h) * crop_frac)
    cx, cy = w // 2, int(h * 0.48)
    left = max(0, min(w - side, cx - side // 2))
    top = max(0, min(h - side, cy - side // 2))
    return im.crop((left, top, left + side, top + side))


def _apply_conv2d_valid(img2d: np.ndarray, kernel: np.ndarray, stride: int = 1, padding: int = 0) -> np.ndarray:
    if padding > 0:
        img2d = np.pad(img2d, ((padding, padding), (padding, padding)), mode="constant", constant_values=0.0)
    kh, kw = kernel.shape
    h, w = img2d.shape
    out_h = (h - kh) // stride + 1
    out_w = (w - kw) // stride + 1
    out = np.zeros((out_h, out_w), dtype=np.float32)
    for r in range(out_h):
        for c in range(out_w):
            patch = img2d[r * stride : r * stride + kh, c * stride : c * stride + kw]
            out[r, c] = float(np.sum(patch * kernel))
    return out


def _apply_maxpool_2x2(fmap: np.ndarray) -> np.ndarray:
    h, w = fmap.shape
    oh, ow = h // 2, w // 2
    out = np.zeros((oh, ow), dtype=np.float32)
    for r in range(oh):
        for c in range(ow):
            out[r, c] = float(np.max(fmap[r * 2 : r * 2 + 2, c * 2 : c * 2 + 2]))
    return out


def generate_thumbnails_and_dataset_stats() -> tuple[dict, Image.Image, Image.Image]:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    meta_path = FROZEN_DIR / "metadata.csv"
    df = pd.read_csv(meta_path)

    thumb_specs = [
        ("anna", "polos", "thumb_anna.jpg"),
        ("elsa", "polos", "thumb_elsa.jpg"),
        ("kristoff", "polos", "thumb_kristoff.jpg"),
        ("olaf", "polos", "thumb_olaf.jpg"),
        ("sven", "polos", "thumb_sven.jpg"),
        ("elsa", "ramai", "thumb_elsa_ramai.jpg"),
        ("olaf", "ramai", "thumb_olaf_ramai.jpg"),
    ]
    thumbs: dict[str, Image.Image] = {}
    for kelas, kondisi, fname in thumb_specs:
        raw = Image.open(_pick_sample_image(kelas, kondisi, idx=0)).convert("RGB")
        cropped = _center_crop_square(raw, crop_frac=0.72).resize((200, 200), Image.Resampling.LANCZOS)
        cropped.save(ASSETS_DIR / fname, quality=92)
        thumbs[fname] = cropped

    class_counts = {c: int((df["kelas"] == c).sum()) for c in CLASSES}
    cond_counts = {
        "polos": int((df["kondisi"] == "polos").sum()),
        "ramai": int((df["kondisi"] == "ramai").sum()),
    }

    elsa_polos = thumbs["thumb_elsa.jpg"]
    elsa_ramai = thumbs["thumb_elsa_ramai.jpg"]

    # Extract real 16x16 grayscale & RGB grids from Elsa polos for interactive Simulator #2
    elsa_16_gray = np.round(
        np.array(elsa_polos.convert("L").resize((16, 16), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0,
        3,
    )
    elsa_8_rgb = np.round(
        np.array(elsa_polos.resize((8, 8), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0,
        3,
    )

    stats = {
        "total_images": int(len(df)),
        "num_classes": len(CLASSES),
        "classes": CLASSES,
        "class_counts": class_counts,
        "condition_counts": cond_counts,
        "elsa_16_gray": elsa_16_gray.tolist(),
        "elsa_8_rgb": elsa_8_rgb.tolist(),
    }
    return stats, elsa_polos, elsa_ramai


def _build_5_architectures_and_benchmark() -> tuple[dict, pd.DataFrame, dict]:
    """Build real Keras models (offline-safe weights=None) for the 5 evolutionary architectures."""
    inp = tf.keras.Input(shape=(224, 224, 3), name="foto_frozen_224")

    # 0. P02 Reference 1-Layer Dense(5)
    p02_x = tf.keras.layers.Flatten()(inp)
    p02_out = tf.keras.layers.Dense(5, activation="softmax")(p02_x)
    m_p02 = tf.keras.Model(inp, p02_out, name="P02_1Layer_Dense")

    # 1. Architecture #1: MLP (Flatten -> Dense(64) -> Dense(32) -> Dense(5))
    mlp_x = tf.keras.layers.Flatten()(inp)
    mlp_x = tf.keras.layers.Dense(64, activation="relu")(mlp_x)
    mlp_x = tf.keras.layers.Dense(32, activation="relu")(mlp_x)
    mlp_out = tf.keras.layers.Dense(5, activation="softmax")(mlp_x)
    m_mlp = tf.keras.Model(inp, mlp_out, name="1_MLP_Dense")

    # 2. Architecture #2: CNN Klasik (3x Conv2D+MaxPool + GAP + Dense(5))
    c_x = tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu")(inp)
    c_x = tf.keras.layers.MaxPooling2D(2)(c_x)
    c_x = tf.keras.layers.Conv2D(64, 3, padding="same", activation="relu")(c_x)
    c_x = tf.keras.layers.MaxPooling2D(2)(c_x)
    c_x = tf.keras.layers.Conv2D(128, 3, padding="same", activation="relu")(c_x)
    c_x = tf.keras.layers.MaxPooling2D(2)(c_x)
    c_x = tf.keras.layers.GlobalAveragePooling2D()(c_x)
    c_x = tf.keras.layers.Dense(64, activation="relu")(c_x)
    c_out = tf.keras.layers.Dense(5, activation="softmax")(c_x)
    m_cnn = tf.keras.Model(inp, c_out, name="2_CNN_Klasik")

    # Also build VGG16-style reference (Flatten + Dense(512) head) just for comparison text if needed
    # 3. Architecture #3: ResNet50 + GAP + Dense(5)
    res_base = tf.keras.applications.ResNet50(include_top=False, weights=None, input_shape=(224, 224, 3))
    r_x = res_base(inp, training=False)
    r_x = tf.keras.layers.GlobalAveragePooling2D()(r_x)
    r_out = tf.keras.layers.Dense(5, activation="softmax")(r_x)
    m_res = tf.keras.Model(inp, r_out, name="3_ResNet50")

    # 4. Architecture #4: MobileNetV2 + GAP + Dropout + Dense(5)
    mob_base = tf.keras.applications.MobileNetV2(include_top=False, weights=None, input_shape=(224, 224, 3))
    mob_x = mob_base(inp, training=False)
    mob_x = tf.keras.layers.GlobalAveragePooling2D()(mob_x)
    mob_x = tf.keras.layers.Dropout(0.2)(mob_x)
    mob_out = tf.keras.layers.Dense(5, activation="softmax")(mob_x)
    m_mob = tf.keras.Model(inp, mob_out, name="4_MobileNetV2")

    # 5. Architecture #5: EfficientNetB0 + GAP + Dropout + Dense(5)
    eff_base = tf.keras.applications.EfficientNetB0(include_top=False, weights=None, input_shape=(224, 224, 3))
    eff_x = eff_base(inp, training=False)
    eff_x = tf.keras.layers.GlobalAveragePooling2D()(eff_x)
    eff_x = tf.keras.layers.Dropout(0.2)(eff_x)
    eff_out = tf.keras.layers.Dense(5, activation="softmax")(eff_x)
    m_eff = tf.keras.Model(inp, eff_out, name="5_EfficientNetB0")

    dummy_batch = np.random.default_rng(SEED).random((8, 224, 224, 3), dtype=np.float32)

    specs = [
        ("1. MLP (2 Hidden)", m_mlp, m_mlp),
        ("2. CNN Klasik", m_cnn, m_cnn),
        ("3. ResNet50", m_res, res_base),
        ("4. MobileNetV2", m_mob, mob_base),
        ("5. EfficientNetB0", m_eff, eff_base),
    ]

    rows = []
    for label, model_full, base_mod in specs:
        # Warmup
        _ = model_full(dummy_batch, training=False)
        timings = []
        for _ in range(5):
            t0 = time.perf_counter()
            _ = model_full(dummy_batch, training=False)
            timings.append((time.perf_counter() - t0) * 1000.0)
        med_ms = float(np.median(timings))
        total_p = int(model_full.count_params())
        base_p = int(base_mod.count_params())
        est_mb = round((total_p * 4) / (1024 * 1024), 2)
        depthwise_cnt = sum(1 for l in base_mod.layers if isinstance(l, tf.keras.layers.DepthwiseConv2D))
        add_cnt = sum(1 for l in base_mod.layers if isinstance(l, tf.keras.layers.Add))
        mul_cnt = sum(1 for l in base_mod.layers if isinstance(l, tf.keras.layers.Multiply))
        rows.append(
            {
                "architecture": label,
                "total_params": total_p,
                "backbone_params": base_p,
                "est_size_mb": est_mb,
                "latency_ms_8imgs": round(med_ms, 1),
                "layers_backbone": len(base_mod.layers),
                "depthwise_layers": depthwise_cnt,
                "skip_add_layers": add_cnt,
                "se_multiply_layers": mul_cnt,
            }
        )

    bench_df = pd.DataFrame(rows)
    p02_params = int(m_p02.count_params())

    # Small real training comparison on frozen_v1 (64x64) so curve & numbers are genuine!
    df_meta = pd.read_csv(FROZEN_DIR / "metadata.csv")
    imgs = []
    labels = []
    cls_to_idx = {c: i for i, c in enumerate(CLASSES)}
    for _, row in df_meta.iterrows():
        fpath = FROZEN_DIR / row["file"]
        im = _center_crop_square(Image.open(fpath).convert("RGB"), crop_frac=0.72).resize((48, 48), Image.Resampling.BILINEAR)
        imgs.append(np.asarray(im, dtype=np.float32) / 255.0)
        labels.append(cls_to_idx[row["kelas"]])
    X = np.stack(imgs, axis=0)
    y = np.array(labels, dtype=np.int32)

    rng = np.random.default_rng(SEED)
    idx_perm = rng.permutation(len(X))
    n_val = max(20, int(0.25 * len(X)))
    val_idx, tr_idx = idx_perm[:n_val], idx_perm[n_val:]
    X_tr, y_tr = X[tr_idx], y[tr_idx]
    X_val, y_val = X[val_idx], y[val_idx]

    def _fit_quick(model: tf.keras.Model, epochs: int = 24, lr: float = 2e-3) -> dict:
        model.compile(
            optimizer=tf.keras.optimizers.Adam(lr),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        h = model.fit(X_tr, y_tr, validation_data=(X_val, y_val), epochs=epochs, batch_size=16, verbose=0)
        return {
            "loss": [round(float(v), 3) for v in h.history["loss"]],
            "val_loss": [round(float(v), 3) for v in h.history["val_loss"]],
            "acc": [round(float(v) * 100, 1) for v in h.history["accuracy"]],
            "val_acc": [round(float(v) * 100, 1) for v in h.history["val_accuracy"]],
            "params": int(model.count_params()),
        }

    # 1) Small 48x48 MLP (Flatten + Dense)
    m_tr_mlp = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(48, 48, 3)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(5, activation="softmax"),
    ])
    hist_mlp = _fit_quick(m_tr_mlp, epochs=28, lr=1.5e-3)

    # Shift invariance test on fitted train patterns (8px horizontal shift)
    X_tr_shifted = np.roll(X_tr, shift=8, axis=2)
    _, acc_orig_mlp = m_tr_mlp.evaluate(X_tr, y_tr, verbose=0)
    _, acc_shift_mlp = m_tr_mlp.evaluate(X_tr_shifted, y_tr, verbose=0)

    # 2) Small 48x48 CNN Klasik
    m_tr_cnn = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(48, 48, 3)),
        tf.keras.layers.Conv2D(16, 3, padding="same", activation="relu"),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu"),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(64, 3, padding="same", activation="relu"),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(5, activation="softmax"),
    ])
    hist_cnn = _fit_quick(m_tr_cnn, epochs=28, lr=2.5e-3)
    _, acc_orig_cnn = m_tr_cnn.evaluate(X_tr, y_tr, verbose=0)
    _, acc_shift_cnn = m_tr_cnn.evaluate(X_tr_shifted, y_tr, verbose=0)

    # 3) Mini-ResNet vs Plain Deep Net (depth 12 conv layers on 48x48)
    def _build_deep(use_skip: bool) -> tf.keras.Model:
        di = tf.keras.Input(shape=(48, 48, 3))
        x = tf.keras.layers.Conv2D(16, 3, padding="same", activation="relu")(di)
        x = tf.keras.layers.MaxPooling2D(2)(x)
        for _ in range(5):
            shortcut = x
            y_b = tf.keras.layers.Conv2D(16, 3, padding="same")(x)
            y_b = tf.keras.layers.BatchNormalization()(y_b)
            y_b = tf.keras.layers.ReLU()(y_b)
            y_b = tf.keras.layers.Conv2D(16, 3, padding="same")(y_b)
            y_b = tf.keras.layers.BatchNormalization()(y_b)
            if use_skip:
                x = tf.keras.layers.Add()([y_b, shortcut])
                x = tf.keras.layers.ReLU()(x)
            else:
                x = tf.keras.layers.ReLU()(y_b)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        out = tf.keras.layers.Dense(5, activation="softmax")(x)
        return tf.keras.Model(di, out)

    tf.keras.utils.set_random_seed(SEED)
    hist_plain = _fit_quick(_build_deep(False), epochs=12, lr=1.5e-3)
    tf.keras.utils.set_random_seed(SEED)
    hist_resnet = _fit_quick(_build_deep(True), epochs=12, lr=1.5e-3)

    # Clear extra keras refs
    extra = {
        "p02_1layer_params": p02_params,
        "shift_test_64": {
            "mlp_val_acc": round(float(acc_orig_mlp) * 100, 1),
            "mlp_shift6px_acc": round(float(acc_shift_mlp) * 100, 1),
            "cnn_val_acc": round(float(acc_orig_cnn) * 100, 1),
            "cnn_shift6px_acc": round(float(acc_shift_cnn) * 100, 1),
        },
        "train_traces_64": {
            "mlp": hist_mlp,
            "cnn": hist_cnn,
            "plain_deep": hist_plain,
            "mini_resnet": hist_resnet,
        },
    }
    return extra, bench_df, {
        "elsa_thumb": None,
        "m_mlp": m_mlp,
        "m_cnn": m_cnn,
    }


def _plot_01_p02_handoff_limit(bench_df: pd.DataFrame, extra: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=140)
    p02_p = extra["p02_1layer_params"] / 1e6
    mlp_p = bench_df.loc[bench_df["architecture"] == "1. MLP (2 Hidden)", "total_params"].iloc[0] / 1e6
    cnn_p = bench_df.loc[bench_df["architecture"] == "2. CNN Klasik", "total_params"].iloc[0] / 1e6

    bars = axes[0].bar(
        ["P02 1-Layer\nDense(5)", "P03 #1 MLP\n(64->32->5)", "P03 #2 CNN\nKlasik (3 Blok)"],
        [p02_p, mlp_p, cnn_p],
        color=[COLORS["yellow"], COLORS["red"], COLORS["blue"]],
        edgecolor=COLORS["dark"],
        linewidth=0.8,
        width=0.52,
    )
    axes[0].set_title("Ledakan Parameter Input 224x224x3 (Juta Param)", fontsize=10.5, fontweight="bold", pad=10)
    axes[0].set_ylabel("Jumlah Parameter (Juta)", fontsize=9.5)
    axes[0].grid(axis="y", alpha=0.25, linestyle="--")
    for b, val in zip(bars, [p02_p, mlp_p, cnn_p]):
        axes[0].text(b.get_x() + b.get_width() / 2, val + 0.18, f"{val:.2f}M", ha="center", va="bottom", fontsize=9.5, fontweight="bold")
    axes[0].set_ylim(0, max(p02_p, mlp_p, cnn_p) * 1.18)

    st = extra["shift_test_64"]
    x = np.arange(2)
    w = 0.34
    b1 = axes[1].bar(x - w / 2, [st["mlp_val_acc"], st["mlp_shift6px_acc"]], width=w, label="MLP (Flatten)", color=COLORS["red"])
    b2 = axes[1].bar(x + w / 2, [st["cnn_val_acc"], st["cnn_shift6px_acc"]], width=w, label="CNN (Conv2D)", color=COLORS["green"])
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(["Foto Posisi Normal", "Digeser 8 Piksel ->"], fontsize=9.5)
    axes[1].set_ylim(0, 105)
    axes[1].set_ylabel("Akurasi Ketahanan (%)", fontsize=9.5)
    axes[1].set_title("Uji Pergeseran Foto Frozen (Crop 48x48, Data Nyata)", fontsize=10.2, fontweight="bold", pad=10)
    axes[1].legend(frameon=True, fontsize=8.5, loc="upper right")
    axes[1].grid(axis="y", alpha=0.25, linestyle="--")
    for bar_g in (b1, b2):
        for b in bar_g:
            axes[1].text(b.get_x() + b.get_width() / 2, b.get_height() + 1.8, f"{b.get_height():.1f}%", ha="center", fontsize=8.5, fontweight="bold")

    plt.tight_layout(pad=1.3)
    fig.savefig(ASSETS_DIR / "01_p02_handoff_limit.png", dpi=150)
    plt.close(fig)


def _plot_02_cnn_conv_pool(elsa_polos: Image.Image) -> None:
    arr_rgb = np.array(elsa_polos.resize((64, 64), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    arr_gray = np.array(elsa_polos.convert("L").resize((32, 32), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    blue_score = np.clip(arr_rgb[:, :, 2] - 0.5 * (arr_rgb[:, :, 0] + arr_rgb[:, :, 1]), 0.0, 1.0)
    fmap_edge = np.maximum(0.0, _apply_conv2d_valid(arr_gray, sobel_x, stride=1, padding=0))
    pooled_edge = _apply_maxpool_2x2(fmap_edge)

    fig, axes = plt.subplots(1, 4, figsize=(10.2, 3.0), dpi=145)
    axes[0].imshow(arr_rgb)
    axes[0].set_title("1. Foto Elsa (64x64)", fontsize=9.5, fontweight="bold")
    axes[1].imshow(fmap_edge, cmap="viridis")
    axes[1].set_title("2. Feature Map Tepi\n(Conv2D 3x3 -> 30x30)", fontsize=9.2, fontweight="bold")
    axes[2].imshow(pooled_edge, cmap="viridis")
    axes[2].set_title("3. MaxPool 2x2\n(Ringkas -> 15x15)", fontsize=9.2, fontweight="bold")
    axes[3].imshow(blue_score, cmap="Blues")
    axes[3].set_title("4. Filter Warna Gaun\n(Channel Biru Dominan)", fontsize=9.2, fontweight="bold")
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout(pad=1.0)
    fig.savefig(ASSETS_DIR / "02_cnn_conv_pool_elsa.png", dpi=150)
    fig.savefig(ASSETS_DIR / "ho_step2_conv_pool_map.png", dpi=150)
    plt.close(fig)


def _plot_03_resnet_skip_gap(extra: dict, bench_df: pd.DataFrame) -> None:
    tr = extra["train_traces_64"]
    epochs = list(range(1, len(tr["plain_deep"]["loss"]) + 1))

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=145)
    axes[0].plot(epochs, tr["plain_deep"]["loss"], "o--", color=COLORS["red"], linewidth=2, label="Plain Deep (12 Conv, Tanpa Skip)")
    axes[0].plot(epochs, tr["mini_resnet"]["loss"], "s-", color=COLORS["green"], linewidth=2.4, label="Mini-ResNet (+ Skip Connection)")
    axes[0].set_title("Training Loss Jaringan Dalam Frozen (Data Nyata)", fontsize=10, fontweight="bold", pad=8)
    axes[0].set_xlabel("Epoch", fontsize=9)
    axes[0].set_ylabel("Cross-Entropy Loss", fontsize=9)
    axes[0].legend(fontsize=8.2, loc="upper right")
    axes[0].grid(alpha=0.25, linestyle="--")

    # Flatten vs GAP head size for ResNet output (7x7x2048 feature tensor -> 5 classes)
    flatten_head = (7 * 7 * 2048 * 512 + 512 * 5) / 1e6
    gap_head = (2048 * 5 + 5) / 1e6
    b = axes[1].bar(["Flatten -> Dense(512)\n(Cara VGG Lama)", "Global Average Pooling\n(Cara ResNet / MobileNetV2)"], [flatten_head, gap_head], color=[COLORS["red"], COLORS["blue"]], width=0.48)
    axes[1].set_title("Hemat Bobot Kepala: Flatten vs GAP (Tensor 7x7x2048)", fontsize=9.8, fontweight="bold", pad=8)
    axes[1].set_ylabel("Juta Parameter Kepala", fontsize=9)
    axes[1].grid(axis="y", alpha=0.25, linestyle="--")
    for bar_i, val in zip(b, [flatten_head, gap_head]):
        lbl = f"{val:.2f}M" if val >= 0.1 else f"{int(val*1e6):,}"
        axes[1].text(bar_i.get_x() + bar_i.get_width() / 2, val + 1.2, lbl, ha="center", fontsize=9.5, fontweight="bold")
    axes[1].set_ylim(0, flatten_head * 1.18)

    plt.tight_layout(pad=1.2)
    fig.savefig(ASSETS_DIR / "03_resnet_skip_gap.png", dpi=150)
    fig.savefig(ASSETS_DIR / "ho_step4_mini_resnet.png", dpi=150)
    plt.close(fig)


def _plot_04_mobilenetv2_depthwise(bench_df: pd.DataFrame) -> None:
    # Exact arithmetic comparison for a standard block: 56x56x64 -> 56x56x128 with kernel 3x3
    H, W, Cin, Cout = 56, 56, 64, 128
    std_ops = H * W * 3 * 3 * Cin * Cout
    dw_ops = H * W * 3 * 3 * Cin
    pw_ops = H * W * 1 * 1 * Cin * Cout
    dws_ops = dw_ops + pw_ops
    ratio = std_ops / dws_ops

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.7), dpi=145)
    b = axes[0].bar(
        ["Conv2D Biasa\n(3x3 Semua Kanal)", "Depthwise + 1x1\n(MobileNetV2)"],
        [std_ops / 1e6, dws_ops / 1e6],
        color=[COLORS["red"], COLORS["green"]],
        width=0.5,
    )
    axes[0].set_title(f"Hitungan Perkalian 1 Blok (Hemat {ratio:.1f}x!)", fontsize=10.2, fontweight="bold", pad=8)
    axes[0].set_ylabel("Juta Perkalian (MFLOPs)", fontsize=9)
    axes[0].grid(axis="y", alpha=0.25, linestyle="--")
    for bi, val in zip(b, [std_ops / 1e6, dws_ops / 1e6]):
        axes[0].text(bi.get_x() + bi.get_width() / 2, val + 4, f"{val:.1f}M", ha="center", fontsize=9.5, fontweight="bold")
    axes[0].set_ylim(0, std_ops / 1e6 * 1.18)

    sub = bench_df[bench_df["architecture"].isin(["3. ResNet50", "4. MobileNetV2", "5. EfficientNetB0"])]
    cols = [COLORS["yellow"], COLORS["green"], COLORS["blue"]]
    b2 = axes[1].barh(sub["architecture"], sub["est_size_mb"], color=cols, height=0.52)
    axes[1].set_title("Estimasi Ukuran Bobot Model (MB, Float32 Nyata)", fontsize=10, fontweight="bold", pad=8)
    axes[1].set_xlabel("Ukuran Model (MB)", fontsize=9)
    axes[1].grid(axis="x", alpha=0.25, linestyle="--")
    for bi, val in zip(b2, sub["est_size_mb"]):
        axes[1].text(val + 1.5, bi.get_y() + bi.get_height() / 2, f"{val:.1f} MB", va="center", fontsize=9, fontweight="bold")
    axes[1].set_xlim(0, sub["est_size_mb"].max() * 1.24)

    plt.tight_layout(pad=1.2)
    fig.savefig(ASSETS_DIR / "04_mobilenetv2_depthwise.png", dpi=150)
    fig.savefig(ASSETS_DIR / "ho_step5_mobilenet_effnet.png", dpi=150)
    plt.close(fig)


def _plot_05_efficientnet_compound_se(elsa_ramai: Image.Image, bench_df: pd.DataFrame) -> None:
    arr = np.array(elsa_ramai.resize((80, 80), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    # Simulated channel maps: channel A = blue dress/frost tone, channel B = cluttered wall/wood tone
    ch_dress = np.clip(arr[:, :, 2] - 0.35 * (arr[:, :, 0] + arr[:, :, 1]), 0.0, 1.0)
    ch_wall = np.clip(0.6 * arr[:, :, 0] + 0.4 * arr[:, :, 1] - 0.5 * arr[:, :, 2], 0.0, 1.0)
    se_combined = np.clip(0.92 * ch_dress + 0.15 * ch_wall, 0.0, 1.0)

    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.2), dpi=145)
    axes[0].imshow(arr)
    axes[0].set_title("Foto Elsa (Latar Ramai)", fontsize=9.5, fontweight="bold")
    axes[1].imshow(0.5 * ch_dress + 0.5 * ch_wall, cmap="inferno")
    axes[1].set_title("Tanpa SE Attention\n(Latar ikut menyala)", fontsize=9.2, fontweight="bold")
    axes[2].imshow(se_combined, cmap="inferno")
    axes[2].set_title("Dengan SE Attention\n(Fokus ke Gaun Biru Elsa)", fontsize=9.2, fontweight="bold")
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout(pad=1.0)
    fig.savefig(ASSETS_DIR / "05_efficientnet_compound_se.png", dpi=150)
    plt.close(fig)


def _plot_06_benchmark_charts(bench_df: pd.DataFrame, extra: dict) -> None:
    # Chart 06 & ho_step6_benchmark_quadrant
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.0), dpi=150)
    colors = [COLORS["red"], COLORS["blue"], COLORS["yellow"], COLORS["green"], COLORS["purple"]]
    short_names = ["1. MLP", "2. CNN Klasik", "3. ResNet50", "4. MobileNetV2", "5. EfficientNetB0"]

    params_m = bench_df["total_params"] / 1e6
    bars = axes[0].barh(short_names[::-1], params_m[::-1], color=colors[::-1], height=0.56)
    axes[0].set_title("Jumlah Parameter 5 Arsitektur (Input 224x224x3)", fontsize=10, fontweight="bold", pad=8)
    axes[0].set_xlabel("Juta Parameter", fontsize=9)
    axes[0].grid(axis="x", alpha=0.25, linestyle="--")
    for b, val in zip(bars, params_m[::-1]):
        axes[0].text(val + 0.4, b.get_y() + b.get_height() / 2, f"{val:.2f}M", va="center", fontsize=8.8, fontweight="bold")
    axes[0].set_xlim(0, params_m.max() * 1.22)

    lat = bench_df["latency_ms_8imgs"]
    sizes = np.clip(bench_df["est_size_mb"] * 6.5, 45, 520)
    axes[1].scatter(params_m, lat, s=sizes, c=colors, alpha=0.85, edgecolors=COLORS["dark"], linewidth=1.2)
    offsets = [(8, 12), (8, 14), (-64, 16), (8, 12), (8, 10)]
    for i, nm in enumerate(short_names):
        dx, dy = offsets[i]
        axes[1].annotate(
            f"{nm}\n({lat.iloc[i]:.0f} ms)",
            (params_m.iloc[i], lat.iloc[i]),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=8.3,
            fontweight="bold",
            color=COLORS["dark"],
        )
    axes[1].set_title("Kompromi Parameter vs Waktu Inferensi (Batch 8 Foto)", fontsize=10, fontweight="bold", pad=8)
    axes[1].set_xlabel("Juta Parameter (M)", fontsize=9)
    axes[1].set_ylabel("Waktu Inferensi (ms)", fontsize=9)
    axes[1].grid(alpha=0.25, linestyle="--")
    axes[1].set_xlim(-1.8, params_m.max() * 1.18)
    axes[1].set_ylim(-60, lat.max() * 1.25)

    plt.tight_layout(pad=1.2)
    fig.savefig(ASSETS_DIR / "06_5arch_comparison_chart.png", dpi=150)
    fig.savefig(ASSETS_DIR / "ho_step6_benchmark_quadrant.png", dpi=150)
    plt.close(fig)

    # Also save ho_step1_mlp_explosion.png and ho_step3_cnn_vs_mlp.png
    fig1, ax1 = plt.subplots(figsize=(6.4, 3.6), dpi=145)
    p02_m = extra["p02_1layer_params"] / 1e6
    mlp_m = params_m.iloc[0]
    cnn_m = params_m.iloc[1]
    bs = ax1.bar(["1-Layer P02\n(Dense 5)", "MLP P03\n(Dense 64->32->5)", "CNN Klasik\n(3 Conv+GAP)"], [p02_m, mlp_m, cnn_m], color=[COLORS["yellow"], COLORS["red"], COLORS["blue"]], width=0.5)
    ax1.set_title("Eksperimen Step 1: Ledakan Parameter MLP pada Foto 224x224x3", fontsize=9.8, fontweight="bold")
    ax1.set_ylabel("Juta Parameter")
    ax1.grid(axis="y", alpha=0.25, linestyle="--")
    for bi, val in zip(bs, [p02_m, mlp_m, cnn_m]):
        ax1.text(bi.get_x() + bi.get_width() / 2, val + 0.15, f"{val:.2f}M", ha="center", fontweight="bold", fontsize=9)
    ax1.set_ylim(0, mlp_m * 1.18)
    plt.tight_layout()
    fig1.savefig(ASSETS_DIR / "ho_step1_mlp_explosion.png", dpi=150)
    plt.close(fig1)

    tr = extra["train_traces_64"]
    fig3, ax3 = plt.subplots(figsize=(6.5, 3.6), dpi=145)
    ep = list(range(1, len(tr["mlp"]["val_acc"]) + 1))
    ax3.plot(ep, tr["mlp"]["acc"], "o--", color=COLORS["red"], linewidth=2, label=f"MLP (Param 48x48: {tr['mlp']['params']:,})")
    ax3.plot(ep, tr["cnn"]["acc"], "s-", color=COLORS["blue"], linewidth=2.4, label=f"CNN Klasik (Param 48x48: {tr['cnn']['params']:,})")
    ax3.set_title("Eksperimen Step 3: Progres Belajar MLP vs CNN Klasik", fontsize=9.8, fontweight="bold")
    ax3.set_xlabel("Epoch")
    ax3.set_ylabel("Akurasi Training (%)")
    ax3.set_ylim(0, 105)
    ax3.legend(fontsize=8.3)
    ax3.grid(alpha=0.25, linestyle="--")
    plt.tight_layout()
    fig3.savefig(ASSETS_DIR / "ho_step3_cnn_vs_mlp.png", dpi=150)
    plt.close(fig3)


def main() -> None:
    stats, elsa_polos, elsa_ramai = generate_thumbnails_and_dataset_stats()
    extra, bench_df, _ = _build_5_architectures_and_benchmark()

    _plot_01_p02_handoff_limit(bench_df, extra)
    _plot_02_cnn_conv_pool(elsa_polos)
    _plot_03_resnet_skip_gap(extra, bench_df)
    _plot_04_mobilenetv2_depthwise(bench_df)
    _plot_05_efficientnet_compound_se(elsa_ramai, bench_df)
    _plot_06_benchmark_charts(bench_df, extra)

    payload = {
        **stats,
        "p02_1layer_params": extra["p02_1layer_params"],
        "shift_test_64": extra["shift_test_64"],
        "train_traces_64": extra["train_traces_64"],
        "benchmarks": bench_df.to_dict(orient="records"),
    }
    out_json = ASSETS_DIR / "p03_data.json"
    tmp_json = ASSETS_DIR / "_tmp_p03_data.json"
    tmp_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp_json.replace(out_json)
    print(f"✅ Aset & benchmark nyata P03 selesai dibuat di: {ASSETS_DIR}")


if __name__ == "__main__":
    main()
