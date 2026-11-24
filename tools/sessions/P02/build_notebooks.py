"""Generator notebook peserta & kunci jawaban untuk Hands-on P02:
Computer Vision 101 — Menggunakan Dataset Proyek Disney Frozen (`data/frozen_v1/`).

Standar ultra awam-friendly (`docs/STANDAR_MATERI.md`):
- Sel kode pendek (5–15 baris), 1 sel = 1 aksi sederhana, komentar Bahasa Indonesia.
- Setup 3 tahap standar (Libraries + versi, Colab/Lokal + SEED=42, Config dinamis DATA_DIR & CLASS_NAMES).
- 8 latihan `# TODO` terfokus + `assert` + 8 sel `<details>` Hint & Jawaban (versi peserta).
- Versi solusi lolos 100% dieksekusi dengan `SMOKE_TEST=1`.
- MLP hanya sebagai demo konsep (tidak mengklaim akurasi tinggi — jembatan ke CNN di P03).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from core.notebook_builder import (  # noqa: E402
    build_notebook_pair,
    code,
    md,
    setup_cells_standard,
    todo_block,
)
from core.registry import get_session  # noqa: E402

SESSION = get_session("P02")


def build_cells(is_solution: bool) -> list:
    cells = []

    # =========================================================================
    # JUDUL + PETA HANDS-ON
    # =========================================================================
    cells.append(
        md(
            """
# Hands-on P02: Computer Vision 101

**Durasi Hands-on:** ±38 menit + 5 menit Mini-Challenge (6 langkah selaras Slide 47–53)  
**Dataset Proyek Utama:** **Disney Frozen Figurine (`data/frozen_v1/`)** — 5 kelas (`anna, elsa, kristoff, olaf, sven`), dibaca secara **dinamis** dari `DATA_DIR` dan `metadata.csv`.  
**Gaya Kode:** Ramah pemula — setiap sel pendek (5–15 baris), 1 sel = 1 tugas, lengkap dengan komentar Bahasa Indonesia (`# ...`).

**Peta 6 Langkah Praktik Hari Ini:**
1. **Langkah 1 (Slide 03 & 47):** Setup 3 tahap & membaca data Frozen secara dinamis dari `metadata.csv`.
2. **Langkah 2 (Slide 21–22 & 48):** *Flatten* foto Frozen & menghitung jumlah neuron **Input Layer** (`H × W × C`).
3. **Langkah 3 (Slide 25–27, 33 & 49):** *Forward Pass* manual (1 neuron *Weight & Bias*, `ReLU`, `Softmax`, dan contoh mini 4 piksel nyata Elsa) di **NumPy**.
4. **Langkah 4 (Slide 31 & 50):** Membangun **MLP kecil** dengan `tf.keras.Sequential` untuk foto Frozen `64×64×3`.
5. **Langkah 5 (Slide 35–38 & 51):** Melatih MLP sebentar & memplot penurunan kurva **Loss** *(demo konsep — jembatan menuju CNN di P03)*.
6. **Langkah 6 (Slide 29, 32 & 52):** Mengecek `model.summary()` & mencocokkannya dengan hitungan tangan, lalu **Mini-Challenge (Slide 53)** membandingkan `32` vs `64` vs `128` neuron hidden.

> **Cara Menjalankan:** Tekan `Shift + Enter` berurutan dari atas ke bawah. Pada versi peserta, lengkapi bagian bertanda `# TODO`.
"""
        )
    )

    # =========================================================================
    # SETUP 3 TAHAP BAKU (LANGKAH 1 BAGIAN A — SLIDE 46)
    # =========================================================================
    cells.extend(
        setup_cells_standard(
            extra_imports="from PIL import Image               # Pillow: untuk membuka dan me-resize foto Frozen",
            use_tensorflow=True,
        )
    )

    # =========================================================================
    # LANGKAH 1: MEMBACA DATA FROZEN SECARA DINAMIS (SLIDE 03 & 46)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 1 (6 menit): Membaca Dataset Frozen Dinamis (Sesuai Slide 03 & 47)

Kita tidak pernah meng-hardcode jumlah foto karena dataset bisa terus bertambah di versi berikutnya.  
Mari baca tabel `metadata.csv` langsung dari `DATA_DIR` dan cek distribusi tiap karakter (`polos` vs `ramai`).
"""
        )
    )

    cells.append(
        code(
            """
# Baca metadata dataset Frozen secara dinamis
meta_path = DATA_DIR / "metadata.csv"
df_meta = pd.read_csv(meta_path)

print("Total foto tersedia saat ini :", len(df_meta))
print("Daftar kelas di metadata     :", sorted(df_meta["kelas"].unique().tolist()))
print("\\nTabel jumlah foto per Kelas x Kondisi:")
print(pd.crosstab(df_meta["kelas"], df_meta["kondisi"], margins=True))
"""
        )
    )

    cells.append(
        md(
            """
Mari tampilkan 1 contoh foto nyata untuk masing-masing dari 5 karakter Frozen (`anna`, `elsa`, `kristoff`, `olaf`, `sven`):
"""
        )
    )

    cells.append(
        code(
            """
# Tampilkan 1 foto polos untuk tiap karakter Frozen
fig, axes = plt.subplots(1, len(CLASS_NAMES), figsize=(12, 2.8))

for i, kls in enumerate(CLASS_NAMES):
    baris = df_meta[(df_meta["kelas"] == kls) & (df_meta["kondisi"] == "polos")].iloc[0]
    foto = Image.open(DATA_DIR / baris["file"]).convert("RGB")
    axes[i].imshow(foto)
    axes[i].set_title(kls.capitalize(), fontweight="bold")
    axes[i].axis("off")

plt.suptitle("5 Karakter Proyek Akhir: Image Classification (Multi-Kelas)", fontweight="bold")
plt.tight_layout()
plt.show()
"""
        )
    )

    # =========================================================================
    # LANGKAH 2: FLATTEN & HITUNG NEURON INPUT LAYER (SLIDE 23–24 & 47)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 2 (6 menit): *Flatten* Foto & Hitung Neuron *Input Layer* (Sesuai Slide 21–22 & 48)

Ingat aturan penting di **Slide 22**:
- Hanya ada **1 Input Layer**, tetapi jumlah **neuron** di dalamnya sama dengan banyaknya nilai piksel dari **1 gambar** setelah *resize*: `Tinggi × Lebar × Channel`.
- Agar bisa masuk ke *Input Layer* MLP, gambar 3D `(H, W, 3)` diluruskan menjadi 1 vektor panjang lewat operasi **Flatten**.
"""
        )
    )

    cells.append(
        code(
            """
# Ambil 1 foto asli Elsa, resize ke 64x64 dan 224x224, lalu normalisasi ke 0.0-1.0
baris_elsa = df_meta[(df_meta["kelas"] == "elsa") & (df_meta["kondisi"] == "polos")].iloc[0]
foto_elsa = Image.open(DATA_DIR / baris_elsa["file"]).convert("RGB")

arr_64 = np.array(foto_elsa.resize((64, 64)), dtype=np.float32) / 255.0
arr_224 = np.array(foto_elsa.resize((IMG_SIZE, IMG_SIZE)), dtype=np.float32) / 255.0

print("Shape foto 64x64   :", arr_64.shape, "| min/max:", round(float(arr_64.min()), 2), "/", round(float(arr_64.max()), 2))
print("Shape foto 224x224 :", arr_224.shape)
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 1 (`# TODO 1`): *Flatten* Foto `64×64×3` Menjadi Vektor Input Layer",
        instruction_md="Gunakan `.flatten()` pada `arr_64` untuk mengubah array 3D `(64, 64, 3)` menjadi 1 deretan neuron input, lalu cek panjangnya (`len(vektor_64)`).",
        student_code="""
# TODO 1: Luruskan arr_64 menjadi vektor 1D dengan .flatten()
vektor_64 = None  # TODO: arr_64.flatten()

assert vektor_64 is not None and vektor_64.ndim == 1
assert len(vektor_64) == 64 * 64 * 3
print("Shape setelah flatten :", vektor_64.shape)
print("Jumlah neuron input   :", f"{len(vektor_64):,}")
print("✅ Cek Latihan 1 lolos!")
""",
        solution_code="""
# Luruskan array 3D (64, 64, 3) menjadi vektor 1D sepanjang 12.288
vektor_64 = arr_64.flatten()

assert vektor_64 is not None and vektor_64.ndim == 1
assert len(vektor_64) == 64 * 64 * 3
print("Shape setelah flatten :", vektor_64.shape)
print("Jumlah neuron input   :", f"{len(vektor_64):,}")
print("✅ Cek Latihan 1 lolos!")
""",
        hint_code="vektor_64 = arr_64.flatten()",
        hint_label="Latihan 1",
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 2 (`# TODO 2`): Hitung Neuron Input `224×224×3` & Weight Tanpa Hidden Layer",
        instruction_md="Hitung `neuron_input_224 = IMG_SIZE * IMG_SIZE * 3` dan `param_tanpa_hidden = neuron_input_224 * len(CLASS_NAMES) + len(CLASS_NAMES)` (sesuai Slide 29).",
        student_code="""
# TODO 2A: Hitung jumlah neuron input untuk foto 224x224x3
neuron_input_224 = None  # TODO: IMG_SIZE * IMG_SIZE * 3

# TODO 2B: Hitung total parameter (weight + bias) jika langsung ke 5 neuron output
param_tanpa_hidden = None  # TODO: neuron_input_224 * len(CLASS_NAMES) + len(CLASS_NAMES)

assert neuron_input_224 == 150_528
assert param_tanpa_hidden == 752_645
print("Neuron Input (224x224x3) :", f"{neuron_input_224:,}")
print("Param langsung -> 5 kelas:", f"{param_tanpa_hidden:,}")
print("✅ Cek Latihan 2 lolos!")
""",
        solution_code="""
# Hitung jumlah neuron input (H * W * C) dan parameter langsung ke output layer
neuron_input_224 = IMG_SIZE * IMG_SIZE * 3
param_tanpa_hidden = neuron_input_224 * len(CLASS_NAMES) + len(CLASS_NAMES)

assert neuron_input_224 == 150_528
assert param_tanpa_hidden == 752_645
print("Neuron Input (224x224x3) :", f"{neuron_input_224:,}")
print("Param langsung -> 5 kelas:", f"{param_tanpa_hidden:,}")
print("✅ Cek Latihan 2 lolos!")
""",
        hint_code="neuron_input_224 = IMG_SIZE * IMG_SIZE * 3\nparam_tanpa_hidden = neuron_input_224 * len(CLASS_NAMES) + len(CLASS_NAMES)",
        hint_label="Latihan 2",
    )

    # =========================================================================
    # LANGKAH 3: FORWARD PASS MANUAL DENGAN NUMPY (SLIDE 21, 26, 32 & 48)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 3 (6 menit): *Forward Pass* Manual dengan NumPy (Sesuai Slide 25–27, 33 & 49)

Sekarang mari buktikan sendiri bahwa matematika di dalam *Neural Network* hanyalah perkalian bobot, penjumlahan bias, `ReLU`, dan `Softmax`!
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 3 (`# TODO 3`): Menghitung 1 Neuron & Aktivasi `ReLU`",
        instruction_md="Lengkapi perhitungan `z = float(np.dot(x_rgb, w) + b)` dan fungsi `relu(v)` yang mengembalikan `np.maximum(0.0, v)`.",
        student_code="""
# Contoh input 3 angka [R, G, B] dan bobot 1 neuron
x_rgb = np.array([0.67, 0.66, 0.67], dtype=np.float32)
w = np.array([-1.5, 1.5, 2.5], dtype=np.float32)
b = -1.3

# TODO 3A: Hitung skor z = float(np.dot(x_rgb, w) + b)
z = None  # TODO

def relu(v):
    # TODO 3B: Kembalikan np.maximum(0.0, v)
    return None  # TODO

out_relu = relu(z) if z is not None else None
assert z is not None and np.isclose(z, 0.36, atol=1e-2)
assert out_relu is not None and np.isclose(out_relu, z, atol=1e-6)
assert relu(-2.5) == 0.0
print(f"Skor z = {z:.4f} -> ReLU(z) = {out_relu:.4f}")
print("✅ Cek Latihan 3 lolos!")
""",
        solution_code="""
# Contoh input 3 angka [R, G, B] dan bobot 1 neuron
x_rgb = np.array([0.67, 0.66, 0.67], dtype=np.float32)
w = np.array([-1.5, 1.5, 2.5], dtype=np.float32)
b = -1.3

# Hitung perkalian titik input * bobot + bias
z = float(np.dot(x_rgb, w) + b)

def relu(v):
    # Ubah angka negatif menjadi 0, biarkan angka positif tetap apa adanya
    return np.maximum(0.0, v)

out_relu = relu(z)
assert z is not None and np.isclose(z, 0.36, atol=1e-2)
assert out_relu is not None and np.isclose(out_relu, z, atol=1e-6)
assert relu(-2.5) == 0.0
print(f"Skor z = {z:.4f} -> ReLU(z) = {out_relu:.4f}")
print("✅ Cek Latihan 3 lolos!")
""",
        hint_code="z = float(np.dot(x_rgb, w) + b)\n# dan di dalam relu(v):\nreturn np.maximum(0.0, v)",
        hint_label="Latihan 3",
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 4 (`# TODO 4`): Fungsi `softmax_manual` & Verifikasi 4-Piksel Forward Pass (Slide 33)",
        instruction_md="Lengkapi `softmax_manual(logits)` memakai `exp_val = np.exp(shifted)` lalu `exp_val / np.sum(exp_val)`. Setelah itu kita jalankan persis contoh 4 piksel foto Elsa di Slide 33!",
        student_code="""
def softmax_manual(logits):
    shifted = logits - np.max(logits)
    # TODO 4: Hitung exp_val dan bagi dengan jumlah totalnya
    exp_val = None  # TODO: np.exp(shifted)
    return None     # TODO: exp_val / np.sum(exp_val)

# Jalankan contoh mini 4 piksel nyata Elsa (Slide 32): 4 Input -> 2 Hidden -> 2 Output
x_4px = np.array([0.76, 0.74, 0.65, 0.65], dtype=np.float64)
W1 = np.array([[0.8, -0.4], [0.6, 0.5], [-0.2, 0.9], [0.4, -0.3]])
b1 = np.array([-0.1, 0.1])
W2 = np.array([[1.5, -0.8], [-0.5, 1.2]])
b2 = np.array([0.2, -0.2])

h1 = relu(x_4px @ W1 + b1)
logits_mini = h1 @ W2 + b2
probs_mini = softmax_manual(logits_mini)

assert probs_mini is not None and np.isclose(np.sum(probs_mini), 1.0)
print("Hidden h1 (ReLU) :", np.round(h1, 3))
print("Output logits    :", np.round(logits_mini, 3))
print(f"Probabilitas     : Elsa = {probs_mini[0]*100:.2f}%, Lain = {probs_mini[1]*100:.2f}%")
print("✅ Cek Latihan 4 lolos!")
""",
        solution_code="""
def softmax_manual(logits):
    shifted = logits - np.max(logits)
    exp_val = np.exp(shifted)
    return exp_val / np.sum(exp_val)

# Jalankan contoh mini 4 piksel nyata Elsa (Slide 32): 4 Input -> 2 Hidden -> 2 Output
x_4px = np.array([0.76, 0.74, 0.65, 0.65], dtype=np.float64)
W1 = np.array([[0.8, -0.4], [0.6, 0.5], [-0.2, 0.9], [0.4, -0.3]])
b1 = np.array([-0.1, 0.1])
W2 = np.array([[1.5, -0.8], [-0.5, 1.2]])
b2 = np.array([0.2, -0.2])

h1 = relu(x_4px @ W1 + b1)
logits_mini = h1 @ W2 + b2
probs_mini = softmax_manual(logits_mini)

assert probs_mini is not None and np.isclose(np.sum(probs_mini), 1.0)
print("Hidden h1 (ReLU) :", np.round(h1, 3))
print("Output logits    :", np.round(logits_mini, 3))
print(f"Probabilitas     : Elsa = {probs_mini[0]*100:.2f}%, Lain = {probs_mini[1]*100:.2f}%")
print("✅ Cek Latihan 4 lolos!")
""",
        hint_code="exp_val = np.exp(shifted)\nreturn exp_val / np.sum(exp_val)",
        hint_label="Latihan 4",
    )

    # =========================================================================
    # LANGKAH 4: BANGUN MLP KECIL DENGAN KERAS (SLIDE 30 & 49)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 4 (6 menit): Membangun MLP Kecil di Keras pada Foto Frozen (Sesuai Slide 31 & 50)

Mari muat seluruh foto Frozen dari `DATA_DIR` ke ukuran ringkas `64×64×3` (agar RAM tetap ringan di kelas), lalu bangun **MLP kecil** memakai `tf.keras.Sequential`.

> **Catatan Jujur:** MLP di sini hanya untuk **demo konsep** struktur layer, parameter, dan penurunan Loss — *bukan* model akhir proyek. Di **P03** kita pindah ke **CNN** yang jauh lebih cocok untuk gambar!
"""
        )
    )

    cells.append(
        code(
            """
# Muat foto Frozen ke ukuran 64x64 RGB (skala 0.0-1.0) secara dinamis
SMALL_SIZE = 64
label_to_idx = {nama: i for i, nama in enumerate(CLASS_NAMES)}

X_frozen, y_frozen = [], []
for _, row in df_meta.iterrows():
    im = Image.open(DATA_DIR / row["file"]).convert("RGB").resize((SMALL_SIZE, SMALL_SIZE))
    X_frozen.append(np.array(im, dtype=np.float32) / 255.0)
    y_frozen.append(label_to_idx[row["kelas"]])

X_frozen = np.array(X_frozen)
y_frozen = np.array(y_frozen)
print("Shape X_frozen :", X_frozen.shape, "| Jumlah label:", len(y_frozen))
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 5 (`# TODO 5`): Menyusun Model MLP Kecil (`buat_mlp_frozen`)",
        instruction_md="Lengkapi fungsi `buat_mlp_frozen(hidden_units=64)` dengan urutan layer: `Input((SMALL_SIZE, SMALL_SIZE, 3))` → `Flatten()` → `Dense(hidden_units, activation='relu')` → `Dense(len(CLASS_NAMES), activation='softmax')`.",
        student_code="""
def buat_mlp_frozen(hidden_units=64, lr=0.001):
    # TODO 5: Lengkapi daftar layer MLP berikut
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(SMALL_SIZE, SMALL_SIZE, 3)),
        None,  # TODO: tf.keras.layers.Flatten()
        None,  # TODO: tf.keras.layers.Dense(hidden_units, activation="relu")
        None,  # TODO: tf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax")
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model

mlp_kecil = buat_mlp_frozen(hidden_units=64)
assert mlp_kecil.output_shape == (None, len(CLASS_NAMES))
print("✅ Model MLP kecil berhasil dibangun! Output shape:", mlp_kecil.output_shape)
""",
        solution_code="""
def buat_mlp_frozen(hidden_units=64, lr=0.001):
    # Susun layer MLP: Input 64x64x3 -> Flatten -> Hidden ReLU -> Output Softmax (5 kelas)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(SMALL_SIZE, SMALL_SIZE, 3)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(hidden_units, activation="relu"),
        tf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax"),
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model

mlp_kecil = buat_mlp_frozen(hidden_units=64)
assert mlp_kecil.output_shape == (None, len(CLASS_NAMES))
print("✅ Model MLP kecil berhasil dibangun! Output shape:", mlp_kecil.output_shape)
""",
        hint_code='tf.keras.layers.Flatten(),\ntf.keras.layers.Dense(hidden_units, activation="relu"),\ntf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax"),',
        hint_label="Latihan 5",
    )

    # =========================================================================
    # LANGKAH 5: LATIH MLP SEBENTAR & PLOT LOSS (SLIDE 34–37 & 50)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 5 (7 menit): Latih MLP Sebentar & Plot Kurva *Loss* (Sesuai Slide 35–38 & 51)

Sekarang kita panggil `mlp_kecil.fit(...)` untuk melihat langsung siklus **Forward Pass → Loss → Backpropagation → Gradient Descent** bekerja otomatis di Keras!  
*(Catatan metodologi: pembagian resmi `train/val/test` bebas data leakage dengan Group Split akan kita pelajari tuntas di **P05**.)*
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 6 (`# TODO 6`): Menjalankan `mlp_kecil.fit(...)`",
        instruction_md="Latih `mlp_kecil` memakai `X_frozen` dan `y_frozen` selama `EPOCHS` (`2` saat `SMOKE_TEST`, `8` saat kelas normal) dengan `batch_size=16`.",
        student_code="""
EPOCHS = 2 if SMOKE_TEST else 8

# TODO 6: Panggil mlp_kecil.fit(X_frozen, y_frozen, epochs=EPOCHS, batch_size=16, verbose=1)
history = None  # TODO

assert history is not None and "loss" in history.history
print(f"Loss Epoch 1     : {history.history['loss'][0]:.4f}")
print(f"Loss Epoch akhir : {history.history['loss'][-1]:.4f}")
print("✅ Cek Latihan 6 lolos!")
""",
        solution_code="""
EPOCHS = 2 if SMOKE_TEST else 8

# Jalankan training singkat untuk mengamati penurunan nilai Loss (demo konsep)
history = mlp_kecil.fit(
    X_frozen, y_frozen,
    epochs=EPOCHS,
    batch_size=16,
    verbose=1,
)

assert history is not None and "loss" in history.history
print(f"Loss Epoch 1     : {history.history['loss'][0]:.4f}")
print(f"Loss Epoch akhir : {history.history['loss'][-1]:.4f}")
print("✅ Cek Latihan 6 lolos!")
""",
        hint_code="history = mlp_kecil.fit(X_frozen, y_frozen, epochs=EPOCHS, batch_size=16, verbose=1)",
        hint_label="Latihan 6",
    )

    cells.append(
        md(
            """
Mari gambar grafik *Training Loss* per *Epoch* dan simpan ke folder `results/`:
"""
        )
    )

    cells.append(
        code(
            """
# Plot kurva Training Loss MLP kecil pada foto Frozen (demo konsep)
fig, ax = plt.subplots(figsize=(7.0, 3.6))
epoch_x = range(1, len(history.history["loss"]) + 1)
ax.plot(epoch_x, history.history["loss"], marker="o", color="#4285F4", linewidth=2.5, label="Training Loss")
ax.set_title("Kurva Training Loss — Demo MLP Kecil pada Foto Frozen (64×64×3)")
ax.set_xlabel("Epoch")
ax.set_ylabel("Cross-Entropy Loss (makin kecil makin baik)")
ax.set_xticks(list(epoch_x))
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend()
plt.tight_layout()

loss_plot_path = RESULTS_DIR / "p02_mlp_loss_curve.png"
fig.savefig(loss_plot_path, dpi=150)
plt.show()
assert loss_plot_path.exists()
print("Grafik disimpan ke:", loss_plot_path)
"""
        )
    )

    # =========================================================================
    # LANGKAH 6: CEK model.summary() VS HITUNGAN TANGAN (SLIDE 28, 31 & 51)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 6 (7 menit): Cocokkan `model.summary()` dengan Hitungan Tangan (Sesuai Slide 29, 32 & 52)

Mari cetak tabel `mlp_kecil.summary()` lalu buktikan bahwa angka di kolom `Param #` cocok **100%** dengan rumus `(Input × Output) + Bias` dari Bab 3!
"""
        )
    )

    cells.append(
        code(
            """
# Tampilkan ringkasan arsitektur & jumlah parameter dari Keras
mlp_kecil.summary()
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 7 (`# TODO 7`): Membuktikan Hitungan Tangan == `mlp_kecil.count_params()`",
        instruction_md="Hitung `param_l1 = (n_input * 64) + 64` dan `param_l2 = (64 * n_kelas) + n_kelas`, lalu jumlahkan ke `total_manual` dan pastikan sama persis dengan `mlp_kecil.count_params()`!",
        student_code="""
n_input = SMALL_SIZE * SMALL_SIZE * 3   # 12.288 neuron input
n_hidden = 64
n_kelas = len(CLASS_NAMES)              # 5 neuron output

# TODO 7A: Hitung parameter Layer 1 (Input -> Hidden)
param_l1 = None  # TODO: (n_input * n_hidden) + n_hidden
# TODO 7B: Hitung parameter Layer 2 (Hidden -> Output)
param_l2 = None  # TODO: (n_hidden * n_kelas) + n_kelas

total_manual = (param_l1 + param_l2) if (param_l1 and param_l2) else None
total_keras = mlp_kecil.count_params()

assert total_manual == total_keras, f"Belum cocok: manual={total_manual}, keras={total_keras}"
print(f"Layer 1 (Input -> Hidden)  : {param_l1:>10,}")
print(f"Layer 2 (Hidden -> Output) : {param_l2:>10,}")
print(f"Total Hitungan Tangan      : {total_manual:>10,}")
print(f"Total Keras count_params() : {total_keras:>10,}  <-- COCOK 100%!")
print("✅ Cek Latihan 7 lolos!")
""",
        solution_code="""
n_input = SMALL_SIZE * SMALL_SIZE * 3   # 12.288 neuron input
n_hidden = 64
n_kelas = len(CLASS_NAMES)              # 5 neuron output

# Hitung jumlah parameter Layer 1 dan Layer 2 sesuai rumus (Input * Output) + Bias
param_l1 = (n_input * n_hidden) + n_hidden
param_l2 = (n_hidden * n_kelas) + n_kelas

total_manual = param_l1 + param_l2
total_keras = mlp_kecil.count_params()

assert total_manual == total_keras, f"Belum cocok: manual={total_manual}, keras={total_keras}"
print(f"Layer 1 (Input -> Hidden)  : {param_l1:>10,}")
print(f"Layer 2 (Hidden -> Output) : {param_l2:>10,}")
print(f"Total Hitungan Tangan      : {total_manual:>10,}")
print(f"Total Keras count_params() : {total_keras:>10,}  <-- COCOK 100%!")
print("✅ Cek Latihan 7 lolos!")
""",
        hint_code="param_l1 = (n_input * n_hidden) + n_hidden\nparam_l2 = (n_hidden * n_kelas) + n_kelas",
        hint_label="Latihan 7",
    )

    # =========================================================================
    # MINI-CHALLENGE (SLIDE 52)
    # =========================================================================
    cells.append(
        md(
            """
---
## Mini-Challenge (5 menit): Ubah Jumlah Neuron *Hidden Layer* (`32` vs `64` vs `128`) (Sesuai Slide 53)

Sebelum menjalankan sel berikut, **tebak dulu**:
1. Jika jumlah neuron hidden dinaikkan `2×` (dari `64` menjadi `128`), kira-kira berapa kali lipat total parameternya naik?
2. Berapa total parameter jika resolusi dinaikkan ke standar `224×224×3` dengan `128` neuron hidden?

Lengkapi `# TODO 8` lalu amati tabel hasilnya!
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 8 (`# TODO 8`): Eksperimen Ukuran Hidden Layer `32`, `64`, & `128`",
        instruction_md="Di dalam loop `daftar_hidden = [32, 64, 128]`, panggil `buat_mlp_frozen(hidden_units=u)` lalu latih selama `EPOCHS` dan catat jumlah parameter serta loss akhirnya.",
        student_code="""
daftar_hidden = [32, 64, 128]
hasil_eksperimen = []

for u in daftar_hidden:
    # TODO 8: Bangun model memakai buat_mlp_frozen(hidden_units=u)
    m_uji = None  # TODO
    assert m_uji is not None
    h_uji = m_uji.fit(X_frozen, y_frozen, epochs=EPOCHS, batch_size=16, verbose=0)
    hasil_eksperimen.append({
        "hidden_units": u,
        "total_parameter": int(m_uji.count_params()),
        "loss_akhir": round(float(h_uji.history["loss"][-1]), 4),
    })

df_exp = pd.DataFrame(hasil_eksperimen)
exp_csv = RESULTS_DIR / "p02_hidden_experiment.csv"
df_exp.to_csv(exp_csv, index=False)

assert len(df_exp) == 3 and exp_csv.exists()
param_224_128 = (224 * 224 * 3 * 128 + 128) + (128 * len(CLASS_NAMES) + len(CLASS_NAMES))
print(df_exp.to_string(index=False))
print(f"\\nSebagai perbandingan — MLP 224x224x3 (Hidden 128): {param_224_128:,} parameter (~19,27 juta!)")
print("✅ Seluruh Hands-on & Mini-Challenge P02 selesai!")
""",
        solution_code="""
daftar_hidden = [32, 64, 128]
hasil_eksperimen = []

for u in daftar_hidden:
    # Bangun dan latih singkat MLP dengan jumlah neuron hidden berbeda
    m_uji = buat_mlp_frozen(hidden_units=u)
    assert m_uji is not None
    h_uji = m_uji.fit(X_frozen, y_frozen, epochs=EPOCHS, batch_size=16, verbose=0)
    hasil_eksperimen.append({
        "hidden_units": u,
        "total_parameter": int(m_uji.count_params()),
        "loss_akhir": round(float(h_uji.history["loss"][-1]), 4),
    })

df_exp = pd.DataFrame(hasil_eksperimen)
exp_csv = RESULTS_DIR / "p02_hidden_experiment.csv"
df_exp.to_csv(exp_csv, index=False)

assert len(df_exp) == 3 and exp_csv.exists()
param_224_128 = (224 * 224 * 3 * 128 + 128) + (128 * len(CLASS_NAMES) + len(CLASS_NAMES))
print(df_exp.to_string(index=False))
print(f"\\nSebagai perbandingan — MLP 224x224x3 (Hidden 128): {param_224_128:,} parameter (~19,27 juta!)")
print("✅ Seluruh Hands-on & Mini-Challenge P02 selesai!")
""",
        hint_code="m_uji = buat_mlp_frozen(hidden_units=u)",
        hint_label="Latihan 8",
    )

    # =========================================================================
    # REFERENSI MANDIRI (SELARAS SLIDE 57–58 & docs/PLAN.md)
    # =========================================================================
    cells.append(
        md(
            """
## Referensi Belajar Mandiri (Selaras Slide 58–59)

1. [3Blue1Brown — *But what is a Neural Network?*](https://www.youtube.com/watch?v=aircAruvnKk) *(Wajib)*
2. [3Blue1Brown — *Playlist Neural Networks (Bab 1–4)*](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
3. [3Blue1Brown — *Versi Tulis Neural Networks*](https://3blue1brown.com/lessons/neural-networks)
4. [TensorFlow Playground](https://playground.tensorflow.org/) `[CEK LINK]`
5. [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) `[CEK LINK]`
6. [Keras Official — *The Sequential Model Guide*](https://keras.io/guides/sequential_model/) `[CEK LINK]`
7. [Coursera (DeepLearning.AI) — *Convolutional Neural Networks (Preview P03)*](https://www.coursera.org/learn/convolutional-neural-networks)
8. [CNN Explainer (Visual Interaktif)](https://poloclub.github.io/cnn-explainer/) `[CEK LINK]`
9. [Stanford CS231n — *Lecture Notes*](https://cs231n.github.io/) `[CEK LINK]`
10. [He dkk. — *Deep Residual Learning (ResNet)*](https://arxiv.org/abs/1512.03385) `[CEK LINK]`
11. [Sandler dkk. — *MobileNetV2: Inverted Residuals and Linear Bottlenecks*](https://arxiv.org/abs/1801.04381)
12. [TensorFlow — *Transfer Learning & Fine-Tuning (Versi Indonesia)*](https://www.tensorflow.org/tutorials/images/transfer_learning?hl=id)
"""
        )
    )

    return cells


def main() -> None:
    build_notebook_pair(SESSION, build_cells)


if __name__ == "__main__":
    main()
