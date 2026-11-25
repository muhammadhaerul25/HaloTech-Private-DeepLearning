"""Generator notebook peserta & kunci jawaban untuk Hands-on P02:
Teori Neural Network — Menggunakan Dataset Proyek Disney Frozen (`data/frozen_v1/`).

100% selaras Bab 1–3 (Slide 01–42) — TANPA konsep Hidden Layer / MLP yang belum diajarkan:
- Sel kode pendek (5–15 baris), 1 sel = 1 aksi sederhana, komentar Bahasa Indonesia.
- Setup 3 tahap standar (Libraries + versi, Colab/Lokal + SEED=42, Config dinamis DATA_DIR & CLASS_NAMES).
- 8 latihan `# TODO` terfokus + `assert` + 8 sel `<details>` Hint & Jawaban (versi peserta).
- Model Neural Network 1-Layer nyata (`Input -> Flatten -> Dense(5, softmax)`) persis Slide 29.
- Versi solusi lolos 100% dieksekusi dengan `SMOKE_TEST=1`.
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
# Hands-on P02: Teori Neural Network

**Durasi Hands-on:** ±58 menit (6 langkah selaras Slide 36–41 + Eksperimen Opsional)  
**Dataset Proyek Utama:** **Disney Frozen Figurine (`data/frozen_v1/`)** — 5 kelas (`anna, elsa, kristoff, olaf, sven`), dibaca secara **dinamis** dari `DATA_DIR` dan `metadata.csv`.  
**Gaya Kode:** Ramah pemula — setiap sel pendek (5–15 baris), 1 sel = 1 tugas, lengkap dengan komentar Bahasa Indonesia (`# ...`).

**Peta 6 Langkah Praktik Hari Ini (100% Selaras Bab 1–3):**
1. **Langkah 1 (Slide 03 & 36):** Setup 3 tahap & membaca data Frozen secara dinamis dari `metadata.csv`.
2. **Langkah 2 (Slide 21–22 & 37):** *Flatten* foto Frozen & menghitung neuron **Input Layer** (`H × W × C`) serta parameter 1-layer (`752.645`).
3. **Langkah 3 (Slide 25–29 & 38):** *Forward Pass* manual di **NumPy** (1 neuron *Weight & Bias*, `ReLU`, `Softmax`, `Argmax`, & *Cross-Entropy Loss*).
4. **Langkah 4 (Slide 29 & 39):** Membangun **Neural Network 1-Layer** (`Input → Flatten → Dense(5, softmax)`) dengan `tf.keras.Sequential`.
5. **Langkah 5 (Slide 28–29 & 40):** Melatih model (`model.fit()`) & memplot kurva penurunan **Loss** per *Epoch*.
6. **Langkah 6 (Slide 29 & 41):** Mencocokkan `model.summary()` dengan hitungan tangan `(Input × Output) + Bias`, plus eksperimen opsional **Learning Rate**.

> **Cara Menjalankan:** Tekan `Shift + Enter` berurutan dari atas ke bawah. Pada versi peserta, lengkapi bagian bertanda `# TODO`.
"""
        )
    )

    # =========================================================================
    # SETUP 3 TAHAP BAKU (LANGKAH 1 BAGIAN A — SLIDE 36)
    # =========================================================================
    cells.extend(
        setup_cells_standard(
            extra_imports="from PIL import Image               # Pillow: untuk membuka dan me-resize foto Frozen",
            use_tensorflow=True,
        )
    )

    # =========================================================================
    # LANGKAH 1: MEMBACA DATA FROZEN SECARA DINAMIS (SLIDE 03 & 36)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 1 (9,5 menit): Membaca Dataset Frozen Dinamis (Sesuai Slide 03 & 36)

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
    # LANGKAH 2: FLATTEN & HITUNG NEURON INPUT LAYER (SLIDE 21–22 & 37)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 2 (9,5 menit): *Flatten* Foto & Hitung Neuron *Input Layer* (Sesuai Slide 21–22 & 37)

Ingat aturan penting di **Slide 22–23**:
- Jumlah **neuron** di *Input Layer* sama dengan banyaknya nilai piksel dari **1 gambar** setelah *resize*: `Tinggi × Lebar × Channel`.
- Agar bisa masuk ke *Input Layer*, gambar 3D `(H, W, 3)` diluruskan menjadi 1 vektor panjang lewat operasi **Flatten**.
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
        title="Latihan 2 (`# TODO 2`): Hitung Neuron Input `224×224×3` & Total Parameter `W + b`",
        instruction_md="Hitung `neuron_input_224 = IMG_SIZE * IMG_SIZE * 3` dan `param_1layer_224 = neuron_input_224 * len(CLASS_NAMES) + len(CLASS_NAMES)` — cocokkan dengan angka **`752.645`** di Slide 29!",
        student_code="""
# TODO 2A: Hitung jumlah neuron input untuk foto 224x224x3
neuron_input_224 = None  # TODO: IMG_SIZE * IMG_SIZE * 3

# TODO 2B: Hitung total parameter (weight + bias) menuju 5 neuron output
param_1layer_224 = None  # TODO: neuron_input_224 * len(CLASS_NAMES) + len(CLASS_NAMES)

assert neuron_input_224 == 150_528
assert param_1layer_224 == 752_645
print("Neuron Input (224x224x3) :", f"{neuron_input_224:,}")
print("Total Param (W + b)      :", f"{param_1layer_224:,}")
print("✅ Cek Latihan 2 lolos!")
""",
        solution_code="""
# Hitung jumlah neuron input (H * W * C) dan total parameter (Input * Output + Bias)
neuron_input_224 = IMG_SIZE * IMG_SIZE * 3
param_1layer_224 = neuron_input_224 * len(CLASS_NAMES) + len(CLASS_NAMES)

assert neuron_input_224 == 150_528
assert param_1layer_224 == 752_645
print("Neuron Input (224x224x3) :", f"{neuron_input_224:,}")
print("Total Param (W + b)      :", f"{param_1layer_224:,}")
print("✅ Cek Latihan 2 lolos!")
""",
        hint_code="neuron_input_224 = IMG_SIZE * IMG_SIZE * 3\nparam_1layer_224 = neuron_input_224 * len(CLASS_NAMES) + len(CLASS_NAMES)",
        hint_label="Latihan 2",
    )

    # =========================================================================
    # LANGKAH 3: FORWARD PASS MANUAL DENGAN NUMPY (SLIDE 25–29 & 38)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 3 (10 menit): *Forward Pass* Manual dengan NumPy (Sesuai Slide 25–29 & 38)

Sekarang mari buktikan sendiri bahwa matematika di dalam *Neural Network* hanyalah perkalian bobot + bias (`z = Σ(x·w) + b`), fungsi aktivasi (`ReLU` / `Softmax`), `Argmax`, dan `Loss (-ln P)`!
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 3 (`# TODO 3`): Menghitung 1 Neuron (`W·x + b`) & Aktivasi `ReLU`",
        instruction_md="Lengkapi perhitungan `z = float(np.dot(x_rgb, w) + b)` dan fungsi `relu(v)` yang mengembalikan `np.maximum(0.0, v)` (sesuai Slide 25–26).",
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
        title="Latihan 4 (`# TODO 4`): `softmax_manual`, `Argmax` & *Cross-Entropy Loss*",
        instruction_md="Lengkapi `softmax_manual(logits)` memakai `exp_val = np.exp(shifted)` lalu `exp_val / np.sum(exp_val)`. Setelah itu kita jalankan Forward Pass 1-Layer lengkap (`W·x + b → Softmax → Argmax → Loss`) pada 4 piksel nyata Elsa!",
        student_code="""
def softmax_manual(logits):
    shifted = logits - np.max(logits)
    # TODO 4: Hitung exp_val dan bagi dengan jumlah totalnya
    exp_val = None  # TODO: np.exp(shifted)
    return None     # TODO: exp_val / np.sum(exp_val)

# Forward Pass 1-Layer nyata pada 4 piksel Elsa -> 5 kelas Frozen (persis alur Slide 25-29!)
x_4px = np.array([0.76, 0.74, 0.65, 0.65], dtype=np.float64)
W_demo = np.array([
    [-0.4,  1.2, -0.3, -0.5, -0.2],
    [-0.3,  1.1, -0.2, -0.4, -0.3],
    [-0.2,  0.9, -0.4, -0.3, -0.1],
    [-0.3,  0.8, -0.2, -0.2, -0.3],
])
b_demo = np.array([-0.1, -0.5, 0.1, 0.0, -0.1])

z_skor = x_4px @ W_demo + b_demo
probs = softmax_manual(z_skor)

assert probs is not None and np.isclose(np.sum(probs), 1.0)
pred_idx = int(np.argmax(probs))
loss_elsa = float(-np.log(probs[1]))  # Target Elsa = index 1
print("Skor mentah z    :", np.round(z_skor, 2))
print("Probabilitas (%) :", np.round(probs * 100, 1))
print(f"Argmax Prediksi  : {CLASS_NAMES[pred_idx].upper()} ({probs[pred_idx]*100:.1f}%) | Loss = {loss_elsa:.2f}")
print("✅ Cek Latihan 4 lolos!")
""",
        solution_code="""
def softmax_manual(logits):
    shifted = logits - np.max(logits)
    exp_val = np.exp(shifted)
    return exp_val / np.sum(exp_val)

# Forward Pass 1-Layer nyata pada 4 piksel Elsa -> 5 kelas Frozen (persis alur Slide 25-29!)
x_4px = np.array([0.76, 0.74, 0.65, 0.65], dtype=np.float64)
W_demo = np.array([
    [-0.4,  1.2, -0.3, -0.5, -0.2],
    [-0.3,  1.1, -0.2, -0.4, -0.3],
    [-0.2,  0.9, -0.4, -0.3, -0.1],
    [-0.3,  0.8, -0.2, -0.2, -0.3],
])
b_demo = np.array([-0.1, -0.5, 0.1, 0.0, -0.1])

z_skor = x_4px @ W_demo + b_demo
probs = softmax_manual(z_skor)

assert probs is not None and np.isclose(np.sum(probs), 1.0)
pred_idx = int(np.argmax(probs))
loss_elsa = float(-np.log(probs[1]))  # Target Elsa = index 1
print("Skor mentah z    :", np.round(z_skor, 2))
print("Probabilitas (%) :", np.round(probs * 100, 1))
print(f"Argmax Prediksi  : {CLASS_NAMES[pred_idx].upper()} ({probs[pred_idx]*100:.1f}%) | Loss = {loss_elsa:.2f}")
print("✅ Cek Latihan 4 lolos!")
""",
        hint_code="exp_val = np.exp(shifted)\nreturn exp_val / np.sum(exp_val)",
        hint_label="Latihan 4",
    )

    # =========================================================================
    # LANGKAH 4: BANGUN NEURAL NETWORK 1-LAYER DI KERAS (SLIDE 29 & 39)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 4 (10 menit): Membangun Neural Network Pertamamu di Keras (Sesuai Slide 29 & 39)

Mari muat seluruh foto Frozen dari `DATA_DIR` ke ukuran ringkas `64×64×3` (agar RAM tetap ringan di kelas), lalu bangun **Neural Network 1-Layer** persis seperti diagram Slide 29: `Input → Flatten → Dense(5, activation="softmax")`!

> **Catatan Jujur:** Model 1-layer ini adalah langkah awal agar kamu paham penuh alur piksel → bobot → Softmax → Loss. Di **P03** kita akan naik ke arsitektur berlapis & **CNN** yang jauh lebih kuat mengenali pola 2D foto!
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
        title="Latihan 5 (`# TODO 5`): Menyusun Neural Network 1-Layer (`buat_nn_frozen`)",
        instruction_md="Lengkapi fungsi `buat_nn_frozen(lr=0.001)` dengan urutan persis Slide 29: `Input((SMALL_SIZE, SMALL_SIZE, 3))` → `Flatten()` → `Dense(len(CLASS_NAMES), activation='softmax')`.",
        student_code="""
def buat_nn_frozen(lr=0.001):
    # TODO 5: Lengkapi layer Flatten dan Output Dense(5, softmax)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(SMALL_SIZE, SMALL_SIZE, 3)),
        None,  # TODO: tf.keras.layers.Flatten()
        None,  # TODO: tf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax")
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model

model_nn = buat_nn_frozen(lr=0.001)
assert model_nn.output_shape == (None, len(CLASS_NAMES))
print("✅ Neural Network 1-Layer berhasil dibangun! Output shape:", model_nn.output_shape)
""",
        solution_code="""
def buat_nn_frozen(lr=0.001):
    # Susun Neural Network 1-Layer persis Slide 29: Input -> Flatten -> Output Softmax (5 kelas)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(SMALL_SIZE, SMALL_SIZE, 3)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax"),
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model

model_nn = buat_nn_frozen(lr=0.001)
assert model_nn.output_shape == (None, len(CLASS_NAMES))
print("✅ Neural Network 1-Layer berhasil dibangun! Output shape:", model_nn.output_shape)
""",
        hint_code='tf.keras.layers.Flatten(),\ntf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax"),',
        hint_label="Latihan 5",
    )

    # =========================================================================
    # LANGKAH 5: LATIH MODEL & PLOT KURVA LOSS (SLIDE 28–29 & 40)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 5 (10 menit): Latih Model (`model.fit()`) & Plot Kurva *Loss* (Sesuai Slide 28–29 & 40)

Sekarang kita panggil `model_nn.fit(...)` untuk melihat langsung siklus **Forward Pass → Loss → Backpropagation → Gradient Descent** bekerja otomatis di Keras!  
*(Catatan metodologi: pembagian resmi `train/val/test` bebas data leakage dengan Group Split akan kita pelajari tuntas di **P05**.)*
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 6 (`# TODO 6`): Menjalankan `model_nn.fit(...)`",
        instruction_md="Latih `model_nn` memakai `X_frozen` dan `y_frozen` selama `EPOCHS` (`2` saat `SMOKE_TEST`, `8` saat kelas normal) dengan `batch_size=16`.",
        student_code="""
EPOCHS = 2 if SMOKE_TEST else 8

# TODO 6: Panggil model_nn.fit(X_frozen, y_frozen, epochs=EPOCHS, batch_size=16, verbose=1)
history = None  # TODO

assert history is not None and "loss" in history.history
print(f"Loss Epoch 1     : {history.history['loss'][0]:.4f}")
print(f"Loss Epoch akhir : {history.history['loss'][-1]:.4f}")
print("✅ Cek Latihan 6 lolos!")
""",
        solution_code="""
EPOCHS = 2 if SMOKE_TEST else 8

# Jalankan training singkat untuk mengamati penurunan nilai Loss (demo konsep Bab 3)
history = model_nn.fit(
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
        hint_code="history = model_nn.fit(X_frozen, y_frozen, epochs=EPOCHS, batch_size=16, verbose=1)",
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
# Plot kurva Training Loss Neural Network 1-Layer pada foto Frozen (demo konsep)
fig, ax = plt.subplots(figsize=(7.0, 3.6))
epoch_x = range(1, len(history.history["loss"]) + 1)
ax.plot(epoch_x, history.history["loss"], marker="o", color="#4285F4", linewidth=2.5, label="Training Loss")
ax.set_title("Kurva Training Loss — Neural Network 1-Layer pada Foto Frozen (64×64×3)")
ax.set_xlabel("Epoch")
ax.set_ylabel("Cross-Entropy Loss (makin kecil makin baik)")
ax.set_xticks(list(epoch_x))
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend()
plt.tight_layout()

loss_plot_path = RESULTS_DIR / "p02_nn_loss_curve.png"
fig.savefig(loss_plot_path, dpi=150)
plt.show()
assert loss_plot_path.exists()
print("Grafik disimpan ke:", loss_plot_path)
"""
        )
    )

    # =========================================================================
    # LANGKAH 6: CEK model.summary() VS HITUNGAN TANGAN (SLIDE 29 & 41)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 6 (9 menit): Cocokkan `model.summary()` dengan Hitungan Tangan (Sesuai Slide 29 & 41)

Mari cetak tabel `model_nn.summary()` lalu buktikan bahwa angka di kolom `Param #` cocok **100%** dengan rumus `(Input × Output) + Bias` dari Bab 3!
"""
        )
    )

    cells.append(
        code(
            """
# Tampilkan ringkasan arsitektur & jumlah parameter dari Keras
model_nn.summary()
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 7 (`# TODO 7`): Membuktikan Hitungan Tangan == `model_nn.count_params()`",
        instruction_md="Hitung `n_weight = n_input * n_kelas` dan `n_bias = n_kelas`, lalu jumlahkan ke `total_manual` dan pastikan sama persis dengan `model_nn.count_params()` (`61.445`)!",
        student_code="""
n_input = SMALL_SIZE * SMALL_SIZE * 3   # 12.288 neuron input
n_kelas = len(CLASS_NAMES)              # 5 neuron output

# TODO 7A: Hitung jumlah Weight (Input * Output)
n_weight = None  # TODO: n_input * n_kelas
# TODO 7B: Hitung jumlah Bias (= jumlah neuron output)
n_bias = None    # TODO: n_kelas

total_manual = (n_weight + n_bias) if (n_weight is not None and n_bias is not None) else None
total_keras = model_nn.count_params()

assert total_manual == total_keras, f"Belum cocok: manual={total_manual}, keras={total_keras}"
print(f"Jumlah Weight (12.288 x 5) : {n_weight:>10,}")
print(f"Jumlah Bias (5 kelas)      : {n_bias:>10,}")
print(f"Total Hitungan Tangan      : {total_manual:>10,}")
print(f"Total Keras count_params() : {total_keras:>10,}  <-- COCOK 100%!")
print("✅ Cek Latihan 7 lolos!")
""",
        solution_code="""
n_input = SMALL_SIZE * SMALL_SIZE * 3   # 12.288 neuron input
n_kelas = len(CLASS_NAMES)              # 5 neuron output

# Hitung jumlah Weight & Bias sesuai rumus (Input * Output) + Bias
n_weight = n_input * n_kelas
n_bias = n_kelas

total_manual = n_weight + n_bias
total_keras = model_nn.count_params()

assert total_manual == total_keras, f"Belum cocok: manual={total_manual}, keras={total_keras}"
print(f"Jumlah Weight (12.288 x 5) : {n_weight:>10,}")
print(f"Jumlah Bias (5 kelas)      : {n_bias:>10,}")
print(f"Total Hitungan Tangan      : {total_manual:>10,}")
print(f"Total Keras count_params() : {total_keras:>10,}  <-- COCOK 100%!")
print("✅ Cek Latihan 7 lolos!")
""",
        hint_code="n_weight = n_input * n_kelas\nn_bias = n_kelas",
        hint_label="Latihan 7",
    )

    # =========================================================================
    # EKSPERIMEN TAMBAHAN (OPSIONAL): PENGARUH LEARNING RATE
    # =========================================================================
    cells.append(
        md(
            """
---
## Eksperimen Tambahan (Opsional): Pengaruh *Learning Rate* (`0.0001` vs `0.001` vs `0.01`)

Ingat **Tahap 5 (Backpropagation & Gradient Descent)** di Bab 3: **Learning Rate** mengatur seberapa besar langkah koreksi bobot `W & b` tiap langkah!  
Lengkapi `# TODO 8` untuk membandingkan 3 nilai *Learning Rate* berbeda pada dataset Frozen kita!
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 8 (`# TODO 8` · Opsional): Eksperimen 3 Nilai *Learning Rate*",
        instruction_md="Di dalam loop `daftar_lr = [0.0001, 0.001, 0.01]`, panggil `buat_nn_frozen(lr=lr_val)` lalu latih selama `EPOCHS` dan catat *Loss* awal vs *Loss* akhirnya.",
        student_code="""
daftar_lr = [0.0001, 0.001, 0.01]
hasil_eksperimen = []

for lr_val in daftar_lr:
    # TODO 8: Bangun model memakai buat_nn_frozen(lr=lr_val)
    m_uji = None  # TODO
    assert m_uji is not None
    h_uji = m_uji.fit(X_frozen, y_frozen, epochs=EPOCHS, batch_size=16, verbose=0)
    hasil_eksperimen.append({
        "learning_rate": lr_val,
        "loss_awal": round(float(h_uji.history["loss"][0]), 4),
        "loss_akhir": round(float(h_uji.history["loss"][-1]), 4),
        "total_parameter": int(m_uji.count_params()),
    })

df_exp = pd.DataFrame(hasil_eksperimen)
exp_csv = RESULTS_DIR / "p02_lr_experiment.csv"
df_exp.to_csv(exp_csv, index=False)

assert len(df_exp) == 3 and exp_csv.exists()
param_224 = (IMG_SIZE * IMG_SIZE * 3 * len(CLASS_NAMES)) + len(CLASS_NAMES)
print(df_exp.to_string(index=False))
print(f"\\nSebagai perbandingan — 1-Layer 224x224x3: {param_224:,} parameter (persis Slide 29!)")
print("✅ Seluruh Hands-on P02 selesai!")
""",
        solution_code="""
daftar_lr = [0.0001, 0.001, 0.01]
hasil_eksperimen = []

for lr_val in daftar_lr:
    # Bangun dan latih singkat Neural Network 1-Layer dengan Learning Rate berbeda
    m_uji = buat_nn_frozen(lr=lr_val)
    assert m_uji is not None
    h_uji = m_uji.fit(X_frozen, y_frozen, epochs=EPOCHS, batch_size=16, verbose=0)
    hasil_eksperimen.append({
        "learning_rate": lr_val,
        "loss_awal": round(float(h_uji.history["loss"][0]), 4),
        "loss_akhir": round(float(h_uji.history["loss"][-1]), 4),
        "total_parameter": int(m_uji.count_params()),
    })

df_exp = pd.DataFrame(hasil_eksperimen)
exp_csv = RESULTS_DIR / "p02_lr_experiment.csv"
df_exp.to_csv(exp_csv, index=False)

assert len(df_exp) == 3 and exp_csv.exists()
param_224 = (IMG_SIZE * IMG_SIZE * 3 * len(CLASS_NAMES)) + len(CLASS_NAMES)
print(df_exp.to_string(index=False))
print(f"\\nSebagai perbandingan — 1-Layer 224x224x3: {param_224:,} parameter (persis Slide 29!)")
print("✅ Seluruh Hands-on P02 selesai!")
""",
        hint_code="m_uji = buat_nn_frozen(lr=lr_val)",
        hint_label="Latihan 8",
    )

    # =========================================================================
    # REFERENSI MANDIRI (SELARAS SLIDE 33–34 & docs/PLAN.md)
    # =========================================================================
    cells.append(
        md(
            """
## Referensi Belajar Mandiri (Selaras Slide 33–34)

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
