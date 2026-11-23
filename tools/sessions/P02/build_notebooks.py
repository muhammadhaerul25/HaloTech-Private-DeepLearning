"""Generator notebook peserta & kunci jawaban untuk Hands-on P02:
Teori Neural Network (ANN) — Menggunakan Dataset Proyek Disney Frozen (`data/frozen_v1/`).

Mengikuti standar ultra awam-friendly (`docs/STANDAR_MATERI.md`):
- Sel kode pendek (5–15 baris), 1 sel = 1 aksi sederhana, komentar Bahasa Indonesia.
- Setup 3 tahap standar (Libraries + versi, Colab/Lokal + SEED=42, Config dinamis DATA_DIR & CLASS_NAMES).
- 8 latihan `# TODO` terfokus + `assert` + 8 sel `<details>` Hint & Jawaban (versi peserta).
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
# Hands-on P02: Teori Neural Network (ANN)

**Durasi Hands-on:** ±50 menit (6 langkah bertahap mengikuti Slide Bab 1–4)  
**Dataset Proyek Utama:** **Disney Frozen Figurine (`data/frozen_v1/`)** — 5 kelas (`anna, elsa, kristoff, olaf, sven`) + eksperimen cepat `Fashion-MNIST / MNIST` (`28×28`).  
**Gaya Kode:** Ramah pemula — setiap sel kode **pendek (5–15 baris)**, satu sel = satu tugas sederhana, dan setiap baris diberi komentar Bahasa Indonesia (`# ...`).

**Peta 6 Langkah Praktik Hari Ini:**
1. **Langkah 1 (Bab 1 · Slide 07–14):** Membuat **1 Neuron & *Forward Pass*** dari nol (NumPy) memakai warna rata-rata foto nyata **Elsa & Olaf**.
2. **Langkah 2 (Bab 2 · Slide 18–25):** Menghitung fungsi aktivasi (**ReLU, Sigmoid**) & **Softmax** secara manual lalu mencocokkannya dengan Keras.
3. **Langkah 3 (Bab 3 · Slide 28–37):** Membangun & melatih **MLP (Multi-Layer Perceptron)** pertama di Keras pada gambar `28×28`.
4. **Langkah 4 (Bab 3 · Slide 31–37):** Eksperimen mengubah **Learning Rate** & **Aktivasi (`ReLU` vs `Sigmoid`)** lalu membandingkan kurva *Loss*.
5. **Langkah 5 (Bab 4 · Slide 40–44):** Eksperimen **Flatten foto nyata Disney Frozen (`data/frozen_v1/`)** ke MLP — melihat ledakan parameter (jembatan ke **P03 CNN**).
6. **Langkah 6 (Slide 49 & 58–59):** Verifikasi **Mini-Challenge Softmax** & Daftar Referensi Belajar Mandiri.

> **Cara Menjalankan:** Tekan `Shift + Enter` berurutan dari atas ke bawah. Pada versi peserta, lengkapi bagian bertanda `# TODO`.
"""
        )
    )

    # =========================================================================
    # SETUP 3 TAHAP BAKU
    # =========================================================================
    cells.extend(
        setup_cells_standard(
            extra_imports="from PIL import Image               # Pillow: untuk membuka foto Disney Frozen",
            use_tensorflow=True,
            extra_config='MNIST_NPZ = Path("data/mnist/mnist.npz")',
        )
    )

    # =========================================================================
    # LANGKAH 0: MENGINTIP DATASET PROYEK DISNEY FROZEN (TRANSISI DARI P01)
    # =========================================================================
    cells.append(
        md(
            """
---
## Transisi dari P01 (3 menit): Mengintip Dataset Proyek Disney Frozen (Sesuai Slide 05)

Di P01 kita belajar bahwa komputer membaca foto sebagai matriks angka `0–255` (RGB) lalu menormalisasinya ke `0.0–1.0`.  
Sekarang mari muat tabel `metadata.csv` dari folder proyek nyata kita (`data/frozen_v1/`) secara **dinamis** (sehingga kode tetap berjalan meski jumlah foto bertambah nanti!).
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
print("Daftar kelas unik            :", sorted(df_meta["kelas"].unique().tolist()))
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
# Tampilkan 1 contoh foto polos dari tiap karakter Frozen
fig, axes = plt.subplots(1, 5, figsize=(12, 2.8))

for i, kls in enumerate(CLASS_NAMES):
    baris = df_meta[(df_meta["kelas"] == kls) & (df_meta["kondisi"] == "polos")].iloc[0]
    foto = Image.open(DATA_DIR / baris["file"]).convert("RGB")
    axes[i].imshow(foto)
    axes[i].set_title(kls.capitalize(), fontweight="bold")
    axes[i].axis("off")

plt.suptitle("5 Karakter Proyek Akhir: Disney Frozen Dataset", fontweight="bold")
plt.tight_layout()
plt.show()
"""
        )
    )

    # =========================================================================
    # LANGKAH 1: 1 NEURON & FORWARD PASS DARI NOL (NUMPY)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 1 (8 menit): Satu Neuron & *Forward Pass* dari Nol (Sesuai Slide 07–14)

Di dalam *Neural Network*, setiap **neuron** hanyalah kalkulator kecil:
$$z = (x_1 \\cdot w_1) + (x_2 \\cdot w_2) + (x_3 \\cdot w_3) + b$$
Mari kita ambil 3 angka input sederhana — rata-rata warna `[R, G, B]` skala `0.0–1.0` di bagian tengah foto **Elsa** dan **Olaf**!
"""
        )
    )

    cells.append(
        code(
            """
def ambil_rgb_tengah(kelas_nama: str) -> np.ndarray:
    # Ambil 1 foto polos lalu potong area tengah tempat figurine berada
    baris = df_meta[(df_meta["kelas"] == kelas_nama) & (df_meta["kondisi"] == "polos")].iloc[0]
    arr = np.array(Image.open(DATA_DIR / baris["file"]).convert("RGB"), dtype=np.float32) / 255.0
    h, w, _ = arr.shape
    patch = arr[int(h * 0.35):int(h * 0.65), int(w * 0.35):int(w * 0.65), :]
    return patch.mean(axis=(0, 1)).round(3)

x_elsa = ambil_rgb_tengah("elsa")
x_olaf = ambil_rgb_tengah("olaf")
print("Input RGB [R, G, B] Elsa :", x_elsa)
print("Input RGB [R, G, B] Olaf :", x_olaf)
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 1A (`# TODO 1A`): Menghitung Skor 1 Neuron (`z = x·w + b`)",
        instruction_md="Misalkan sebuah neuron 'Detektor Gaun Biru Elsa' memiliki bobot `w = np.array([-1.5, 0.5, 2.5])` dan bias `b = -0.3`. Hitung skor `z_elsa` menggunakan `float(np.dot(x_elsa, w) + b)`.",
        student_code="""
# Bobot (weight) & bias contoh untuk 1 neuron
w = np.array([-1.5, 0.5, 2.5], dtype=np.float32)
b = -0.3

# TODO 1A: Hitung skor z_elsa = float(np.dot(x_elsa, w) + b)
z_elsa = None  # TODO

assert z_elsa is not None and isinstance(z_elsa, float)
print(f"Skor mentah z_elsa = {z_elsa:.4f}")
print("✅ Cek Latihan 1A lolos!")
""",
        solution_code="""
# Bobot (weight) & bias contoh untuk 1 neuron
w = np.array([-1.5, 0.5, 2.5], dtype=np.float32)
b = -0.3

# Hitung perkalian titik (dot product) input * bobot + bias
z_elsa = float(np.dot(x_elsa, w) + b)

assert z_elsa is not None and isinstance(z_elsa, float)
print(f"Skor mentah z_elsa = {z_elsa:.4f}")
print("✅ Cek Latihan 1A lolos!")
""",
        hint_code="z_elsa = float(np.dot(x_elsa, w) + b)",
        hint_label="Latihan 1A",
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 1B (`# TODO 1B`): Menerapkan Fungsi Aktivasi `ReLU` & `Sigmoid`",
        instruction_md="Lengkapi fungsi `relu(z)` (`np.maximum(0.0, z)`) dan `sigmoid(z)` (`1.0 / (1.0 + np.exp(-z))`), lalu uji pada angka negatif dan positif.",
        student_code="""
def relu(z):
    # TODO 1B-1: Kembalikan np.maximum(0.0, z)
    return None  # TODO

def sigmoid(z):
    # TODO 1B-2: Kembalikan 1.0 / (1.0 + np.exp(-z))
    return None  # TODO

uji_z = np.array([-2.0, 0.0, 2.0])
out_relu = relu(uji_z)
out_sig = sigmoid(uji_z)

assert out_relu is not None and np.allclose(out_relu, [0.0, 0.0, 2.0])
assert out_sig is not None and np.isclose(out_sig[1], 0.5)
print("ReLU([-2, 0, 2])    :", out_relu)
print("Sigmoid([-2, 0, 2]) :", np.round(out_sig, 4))
print("✅ Cek Latihan 1B lolos!")
""",
        solution_code="""
def relu(z):
    # Ubah angka negatif menjadi 0, biarkan angka positif tetap apa adanya
    return np.maximum(0.0, z)

def sigmoid(z):
    # Tekan semua angka ke rentang probabilitas 0.0 sampai 1.0
    return 1.0 / (1.0 + np.exp(-z))

uji_z = np.array([-2.0, 0.0, 2.0])
out_relu = relu(uji_z)
out_sig = sigmoid(uji_z)

assert out_relu is not None and np.allclose(out_relu, [0.0, 0.0, 2.0])
assert out_sig is not None and np.isclose(out_sig[1], 0.5)
print("ReLU([-2, 0, 2])    :", out_relu)
print("Sigmoid([-2, 0, 2]) :", np.round(out_sig, 4))
print("✅ Cek Latihan 1B lolos!")
""",
        hint_code="return np.maximum(0.0, z)\n# dan untuk sigmoid:\nreturn 1.0 / (1.0 + np.exp(-z))",
        hint_label="Latihan 1B",
    )

    # =========================================================================
    # LANGKAH 2: SOFTMAX MANUAL VS KERAS
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 2 (6 menit): Menghitung `Softmax` Manual & Mencocokkan dengan Keras (Sesuai Slide 23–26)

Di ujung jaringan saraf (Output Layer), terdapat **5 neuron** untuk 5 karakter Frozen (`anna, elsa, kristoff, olaf, sven`).  
Skor mentahnya (*logits*) bisa positif maupun negatif — fungsi **Softmax** mengubahnya menjadi probabilitas yang selalu berjumlah **`1.0` (100%)**.
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 2A (`# TODO 2A`): Membuat Fungsi `softmax_manual(logits)`",
        instruction_md="Hitung eksponensial yang aman dari overflow: `exp_val = np.exp(logits - np.max(logits))`, lalu bagi dengan `np.sum(exp_val)`.",
        student_code="""
def softmax_manual(logits):
    # Kurangi nilai maksimum agar eksponensial stabil secara numerik
    shifted = logits - np.max(logits)
    # TODO 2A: Hitung exp_val = np.exp(shifted), lalu kembalikan exp_val / np.sum(exp_val)
    exp_val = None  # TODO
    return None     # TODO

logits_frozen = np.array([1.2, 2.8, -0.5, 0.3, -0.9], dtype=np.float32)
probs_manual = softmax_manual(logits_frozen)

assert probs_manual is not None and np.isclose(np.sum(probs_manual), 1.0)
for nama, p in zip(CLASS_NAMES, probs_manual):
    print(f"  {nama:<10}: {p * 100:5.2f}%")
print("✅ Cek Latihan 2A lolos!")
""",
        solution_code="""
def softmax_manual(logits):
    # Kurangi nilai maksimum agar eksponensial stabil secara numerik
    shifted = logits - np.max(logits)
    exp_val = np.exp(shifted)
    return exp_val / np.sum(exp_val)

logits_frozen = np.array([1.2, 2.8, -0.5, 0.3, -0.9], dtype=np.float32)
probs_manual = softmax_manual(logits_frozen)

assert probs_manual is not None and np.isclose(np.sum(probs_manual), 1.0)
for nama, p in zip(CLASS_NAMES, probs_manual):
    print(f"  {nama:<10}: {p * 100:5.2f}%")
print("✅ Cek Latihan 2A lolos!")
""",
        hint_code="exp_val = np.exp(shifted)\nreturn exp_val / np.sum(exp_val)",
        hint_label="Latihan 2A",
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 2B (`# TODO 2B`): Mencocokkan `softmax_manual` dengan `tf.nn.softmax`",
        instruction_md="Panggil `tf.nn.softmax(logits_frozen).numpy()` dan buktikan hasilnya identik dengan rumus manual kita!",
        student_code="""
# TODO 2B: Hitung probabilitas memakai tf.nn.softmax(logits_frozen).numpy()
probs_keras = None  # TODO

assert probs_keras is not None and np.allclose(probs_manual, probs_keras, atol=1e-6)
print("Selisih terbesar manual vs Keras:", float(np.max(np.abs(probs_manual - probs_keras))))
print("Karakter terprediksi             :", CLASS_NAMES[int(np.argmax(probs_keras))].upper())
print("✅ Cek Latihan 2B lolos!")
""",
        solution_code="""
# Hitung probabilitas dengan fungsi bawaan TensorFlow/Keras
probs_keras = tf.nn.softmax(logits_frozen).numpy()

assert probs_keras is not None and np.allclose(probs_manual, probs_keras, atol=1e-6)
print("Selisih terbesar manual vs Keras:", float(np.max(np.abs(probs_manual - probs_keras))))
print("Karakter terprediksi             :", CLASS_NAMES[int(np.argmax(probs_keras))].upper())
print("✅ Cek Latihan 2B lolos!")
""",
        hint_code="probs_keras = tf.nn.softmax(logits_frozen).numpy()",
        hint_label="Latihan 2B",
    )

    # =========================================================================
    # LANGKAH 3: MEMBANGUN & MELATIH MLP DI KERAS (FASHION-MNIST / MNIST 28x28)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 3 (12 menit): Melatih MLP Pertama di Keras pada Citra `28×28` (Sesuai Slide 28–37)

Sebelum menguji foto Frozen beresolusi besar, kita latih dulu jaringan **MLP (*Multi-Layer Perceptron*)** pada dataset gambar kecil `28×28` (`Fashion-MNIST`, atau otomatis menggunakan `data/mnist/mnist.npz` lokal jika komputer sedang offline).
"""
        )
    )

    cells.append(
        code(
            """
# Muat Fashion-MNIST (fallback otomatis ke data/mnist/mnist.npz lokal jika offline)
local_mnist = BASE_DIR / "data" / "mnist" / "mnist.npz"
if SMOKE_TEST and local_mnist.exists():
    with np.load(local_mnist) as d:
        (x_tr, y_tr), (x_va, y_va) = (d["x_train"], d["y_train"]), (d["x_test"], d["y_test"])
    DATASET_28 = "MNIST (lokal · mode cepat)"
else:
    try:
        (x_tr, y_tr), (x_va, y_va) = tf.keras.datasets.fashion_mnist.load_data()
        DATASET_28 = "Fashion-MNIST"
    except Exception:
        with np.load(local_mnist) as d:
            (x_tr, y_tr), (x_va, y_va) = (d["x_train"], d["y_train"]), (d["x_test"], d["y_test"])
        DATASET_28 = "MNIST (fallback lokal)"

# Ambil subset ringkas agar training selesai dalam hitungan detik di kelas
n_train = 1200 if SMOKE_TEST else 6000
n_val = 400 if SMOKE_TEST else 1500
x_tr, y_tr = x_tr[:n_train], y_tr[:n_train]
x_va, y_va = x_va[:n_val], y_va[:n_val]

print(f"Dataset 28x28 aktif : {DATASET_28}")
print("Shape x_train       :", x_tr.shape, "| dtype:", x_tr.dtype)
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 3A (`# TODO 3A`): Normalisasi Piksel `0–255` ke `0.0–1.0` (`float32`)",
        instruction_md="Ingat pelajaran P01! Ubah `x_tr` dan `x_va` ke `float32` lalu bagi `255.0` agar gradien stabil saat training.",
        student_code="""
# TODO 3A: Ubah ke float32 dan bagi 255.0
x_tr_norm = None  # TODO: x_tr.astype("float32") / 255.0
x_va_norm = None  # TODO: x_va.astype("float32") / 255.0

assert x_tr_norm is not None and x_tr_norm.dtype == np.float32
assert float(x_tr_norm.max()) <= 1.0 and float(x_tr_norm.min()) >= 0.0
print("Rentang baru:", float(x_tr_norm.min()), "s.d.", float(x_tr_norm.max()))
print("✅ Cek Latihan 3A lolos!")
""",
        solution_code="""
# Ubah ke float32 dan bagi 255.0 agar skala input 0.0 sampai 1.0
x_tr_norm = x_tr.astype("float32") / 255.0
x_va_norm = x_va.astype("float32") / 255.0

assert x_tr_norm is not None and x_tr_norm.dtype == np.float32
assert float(x_tr_norm.max()) <= 1.0 and float(x_tr_norm.min()) >= 0.0
print("Rentang baru:", float(x_tr_norm.min()), "s.d.", float(x_tr_norm.max()))
print("✅ Cek Latihan 3A lolos!")
""",
        hint_code='x_tr_norm = x_tr.astype("float32") / 255.0\nx_va_norm = x_va.astype("float32") / 255.0',
        hint_label="Latihan 3A",
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 3B (`# TODO 3B`): Menyusun Arsitektur MLP di Keras",
        instruction_md="Buat fungsi `buat_mlp(activation='relu', lr=0.001)` dengan susunan: `Input((28, 28))` → `Flatten()` → `Dense(64, activation=activation)` → `Dense(10, activation='softmax')`.",
        student_code="""
def buat_mlp(activation="relu", lr=0.001):
    # TODO 3B: Lengkapi daftar layer Sequential berikut
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(28, 28)),
        None,  # TODO: tf.keras.layers.Flatten()
        None,  # TODO: tf.keras.layers.Dense(64, activation=activation)
        None,  # TODO: tf.keras.layers.Dense(10, activation="softmax")
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model

mlp_base = buat_mlp(activation="relu", lr=0.001)
assert mlp_base.output_shape == (None, 10)
print("Total parameter MLP 28x28:", f"{mlp_base.count_params():,}")
print("✅ Cek Latihan 3B lolos!")
""",
        solution_code="""
def buat_mlp(activation="relu", lr=0.001):
    # Susun layer MLP: Flatten 28x28 -> Hidden Dense(64) -> Output Softmax(10)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(28, 28)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation=activation),
        tf.keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model

mlp_base = buat_mlp(activation="relu", lr=0.001)
assert mlp_base.output_shape == (None, 10)
print("Total parameter MLP 28x28:", f"{mlp_base.count_params():,}")
print("✅ Cek Latihan 3B lolos!")
""",
        hint_code='tf.keras.layers.Flatten(),\ntf.keras.layers.Dense(64, activation=activation),\ntf.keras.layers.Dense(10, activation="softmax"),',
        hint_label="Latihan 3B",
    )

    cells.append(
        md(
            """
Sekarang mari latih `mlp_base` dan amati *Train Loss* serta *Validation Loss* tiap *epoch*:
"""
        )
    )

    cells.append(
        code(
            """
# Latih MLP baseline (2 epoch saat SMOKE_TEST, 6 epoch saat kelas normal)
EPOCHS = 2 if SMOKE_TEST else 6
hist_base = mlp_base.fit(
    x_tr_norm, y_tr,
    validation_data=(x_va_norm, y_va),
    epochs=EPOCHS,
    batch_size=64,
    verbose=1,
)
print(f"Akurasi validasi akhir (ReLU, LR=0.001): {hist_base.history['val_accuracy'][-1]*100:.2f}%")
"""
        )
    )

    # =========================================================================
    # LANGKAH 4: EKSPERIMEN LEARNING RATE & AKTIVASI
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 4 (10 menit): Eksperimen *Learning Rate* & Aktivasi `ReLU` vs `Sigmoid` (Sesuai Slide 31–37)

Mari buktikan secara langsung apa efeknya jika **Learning Rate terlalu besar (`0.1`)** atau jika hidden layer memakai **`Sigmoid`** dibanding **`ReLU`**.
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 4 (`# TODO 4`): Melatih Pembanding `LR = 0.1` & Aktivasi `Sigmoid`",
        instruction_md="Panggil `buat_mlp(activation='relu', lr=0.1)` dan `buat_mlp(activation='sigmoid', lr=0.001)`, lalu latih keduanya selama `EPOCHS` epoch.",
        student_code="""
# TODO 4A: Buat model dengan learning rate terlalu besar (lr=0.1)
mlp_lr_besar = None  # TODO: buat_mlp(activation="relu", lr=0.1)
# TODO 4B: Buat model dengan aktivasi sigmoid (lr=0.001)
mlp_sigmoid = None   # TODO: buat_mlp(activation="sigmoid", lr=0.001)

assert mlp_lr_besar is not None and mlp_sigmoid is not None
hist_lr_besar = mlp_lr_besar.fit(x_tr_norm, y_tr, validation_data=(x_va_norm, y_va), epochs=EPOCHS, batch_size=64, verbose=0)
hist_sigmoid = mlp_sigmoid.fit(x_tr_norm, y_tr, validation_data=(x_va_norm, y_va), epochs=EPOCHS, batch_size=64, verbose=0)

print(f"Val Acc ReLU (LR=0.001)    : {hist_base.history['val_accuracy'][-1]*100:.2f}%")
print(f"Val Acc ReLU (LR=0.1)      : {hist_lr_besar.history['val_accuracy'][-1]*100:.2f}%")
print(f"Val Acc Sigmoid (LR=0.001) : {hist_sigmoid.history['val_accuracy'][-1]*100:.2f}%")
print("✅ Cek Latihan 4 lolos!")
""",
        solution_code="""
# Buat 2 model pembanding: LR terlalu besar (0.1) dan aktivasi Sigmoid
mlp_lr_besar = buat_mlp(activation="relu", lr=0.1)
mlp_sigmoid = buat_mlp(activation="sigmoid", lr=0.001)

assert mlp_lr_besar is not None and mlp_sigmoid is not None
hist_lr_besar = mlp_lr_besar.fit(x_tr_norm, y_tr, validation_data=(x_va_norm, y_va), epochs=EPOCHS, batch_size=64, verbose=0)
hist_sigmoid = mlp_sigmoid.fit(x_tr_norm, y_tr, validation_data=(x_va_norm, y_va), epochs=EPOCHS, batch_size=64, verbose=0)

print(f"Val Acc ReLU (LR=0.001)    : {hist_base.history['val_accuracy'][-1]*100:.2f}%")
print(f"Val Acc ReLU (LR=0.1)      : {hist_lr_besar.history['val_accuracy'][-1]*100:.2f}%")
print(f"Val Acc Sigmoid (LR=0.001) : {hist_sigmoid.history['val_accuracy'][-1]*100:.2f}%")
print("✅ Cek Latihan 4 lolos!")
""",
        hint_code='mlp_lr_besar = buat_mlp(activation="relu", lr=0.1)\nmlp_sigmoid = buat_mlp(activation="sigmoid", lr=0.001)',
        hint_label="Latihan 4",
    )

    cells.append(
        md(
            """
Mari gambar grafik perbandingan *Validation Loss* ketiga percobaan tersebut dan simpan ke `results/p02_lr_activation_compare.png`:
"""
        )
    )

    cells.append(
        code(
            """
# Plot perbandingan kurva Validation Loss
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.plot(hist_base.history["val_loss"], marker="o", color="#4285F4", label="ReLU · LR=0.001 (Ideal)")
ax.plot(hist_lr_besar.history["val_loss"], marker="s", color="#EA4335", label="ReLU · LR=0.1 (Terlalu Besar)")
ax.plot(hist_sigmoid.history["val_loss"], marker="^", color="#34A853", label="Sigmoid · LR=0.001")

ax.set_title("Perbandingan Kurva Validation Loss: Efek Learning Rate & Aktivasi")
ax.set_xlabel("Epoch")
ax.set_ylabel("Validation Loss (makin kecil makin baik)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()

plot_lr_path = RESULTS_DIR / "p02_lr_activation_compare.png"
fig.savefig(plot_lr_path, dpi=150)
plt.show()
print("Grafik disimpan ke:", plot_lr_path)
"""
        )
    )

    # =========================================================================
    # LANGKAH 5: EKSPERIMEN FLATTEN FOTO DISNEY FROZEN KE MLP (JEMBATAN KE CNN)
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 5 (10 menit): Eksperimen *Flatten* Foto Disney Frozen ke MLP (Sesuai Slide 40–44)

Sekarang mari uji langsung **foto nyata proyek Disney Frozen (`data/frozen_v1/`)**!  
Kita muat foto-foto Frozen ke ukuran kecil `64 × 64 × 3` (agar RAM aman) dan kita lihat:
1. Berapa **ledakan jumlah parameter** MLP pada ukuran `64×64×3` vs `224×224×3`?
2. Bagaimana hasil saat foto Frozen di-*flatten* lurus ke dalam MLP?
"""
        )
    )

    cells.append(
        code(
            """
# Muat foto Frozen ke ukuran kecil 64x64 RGB (skala 0.0-1.0)
FROZEN_SMALL = 64
label_to_idx = {nama: i for i, nama in enumerate(CLASS_NAMES)}

X_frozen, y_frozen = [], []
for _, row in df_meta.iterrows():
    im = Image.open(DATA_DIR / row["file"]).convert("RGB").resize((FROZEN_SMALL, FROZEN_SMALL))
    X_frozen.append(np.array(im, dtype=np.float32) / 255.0)
    y_frozen.append(label_to_idx[row["kelas"]])

X_frozen = np.array(X_frozen)
y_frozen = np.array(y_frozen)
print("Shape X_frozen :", X_frozen.shape, "| Jumlah kelas:", len(CLASS_NAMES))
print("Jika di-flatten (64x64x3) -> 1 baris sepanjang:", 64 * 64 * 3, "angka per foto!")
"""
        )
    )

    todo_block(
        cells,
        is_solution=is_solution,
        title="Latihan 5 (`# TODO 5`): Membangun MLP untuk Foto Frozen (`64×64×3`) & Cek Ledakan Parameter",
        instruction_md="Bangun model `mlp_frozen` dengan input `(64, 64, 3)` → `Flatten()` → `Dense(128, activation='relu')` → `Dense(len(CLASS_NAMES), activation='softmax')`, lalu bandingkan jumlah parameternya dengan input `224×224×3`!",
        student_code="""
# TODO 5: Susun MLP untuk foto Frozen 64x64x3 (5 kelas output)
mlp_frozen = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(FROZEN_SMALL, FROZEN_SMALL, 3)),
    None,  # TODO: tf.keras.layers.Flatten()
    None,  # TODO: tf.keras.layers.Dense(128, activation="relu")
    None,  # TODO: tf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax")
])
mlp_frozen.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

params_64 = mlp_frozen.count_params()
params_224_est = (224 * 224 * 3 * 128) + 128 + (128 * len(CLASS_NAMES)) + len(CLASS_NAMES)

assert params_64 > 1_000_000
print(f"Parameter MLP Frozen (64x64x3)   : {params_64:>12,}")
print(f"Parameter MLP Frozen (224x224x3) : {params_224_est:>12,}  <-- MELEDAK > 19 Juta!")
print("✅ Cek Latihan 5 lolos!")
""",
        solution_code="""
# Susun MLP untuk foto Frozen 64x64x3 (5 kelas output)
mlp_frozen = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(FROZEN_SMALL, FROZEN_SMALL, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax"),
])
mlp_frozen.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

params_64 = mlp_frozen.count_params()
params_224_est = (224 * 224 * 3 * 128) + 128 + (128 * len(CLASS_NAMES)) + len(CLASS_NAMES)

assert params_64 > 1_000_000
print(f"Parameter MLP Frozen (64x64x3)   : {params_64:>12,}")
print(f"Parameter MLP Frozen (224x224x3) : {params_224_est:>12,}  <-- MELEDAK > 19 Juta!")
print("✅ Cek Latihan 5 lolos!")
""",
        hint_code='tf.keras.layers.Flatten(),\ntf.keras.layers.Dense(128, activation="relu"),\ntf.keras.layers.Dense(len(CLASS_NAMES), activation="softmax"),',
        hint_label="Latihan 5",
    )

    cells.append(
        md(
            """
Mari jalankan uji singkat `mlp_frozen` pada foto Frozen (sekadar untuk melihat gejala **overfitting & hilangnya struktur 2D** — metodologi split resmi bebas leakage akan dipelajari di **P05**):
"""
        )
    )

    cells.append(
        code(
            """
# Uji cepat MLP pada foto Frozen (sekadar ilustrasi keterbatasan MLP pada gambar)
idx_acak = np.random.permutation(len(X_frozen))
batas = int(0.8 * len(X_frozen))
X_f_tr, y_f_tr = X_frozen[idx_acak[:batas]], y_frozen[idx_acak[:batas]]
X_f_va, y_f_va = X_frozen[idx_acak[batas:]], y_frozen[idx_acak[batas:]]

hist_f = mlp_frozen.fit(
    X_f_tr, y_f_tr,
    validation_data=(X_f_va, y_f_va),
    epochs=2 if SMOKE_TEST else 8,
    batch_size=16,
    verbose=1,
)

# Simpan ringkasan parameter ke CSV untuk bahan diskusi P03
df_params = pd.DataFrame([
    {"skenario": "MNIST (28x28x1 -> Dense 64)", "total_parameter": int(mlp_base.count_params())},
    {"skenario": "Frozen Kecil (64x64x3 -> Dense 128)", "total_parameter": int(params_64)},
    {"skenario": "Frozen Standar (224x224x3 -> Dense 128)", "total_parameter": int(params_224_est)},
])
params_csv = RESULTS_DIR / "p02_mlp_parameter_comparison.csv"
df_params.to_csv(params_csv, index=False)
assert params_csv.exists() and plot_lr_path.exists()
print("\\nTabel perbandingan parameter disimpan ke:", params_csv)
print(df_params.to_string(index=False))
"""
        )
    )

    # =========================================================================
    # LANGKAH 6: MINI-CHALLENGE & REFERENSI
    # =========================================================================
    cells.append(
        md(
            """
---
## Langkah 6 (4 menit): Mini-Challenge *Softmax* (Sesuai Slide 49)

Sebelum menjalankan sel di bawah ini, coba **tebak tanpa kalkulator**:
Jika skor mentah (*logits*) 3 karakter Frozen adalah **`Elsa = 2.0`, `Anna = 1.0`, `Olaf = 0.0`**:
1. Karakter mana yang mendapat probabilitas tertinggi?
2. Mengapa jumlah ketiga probabilitas **selalu tepat `1.0` (100%)**?
3. Apa yang terjadi jika semua skor ditambah `+10` menjadi `[12.0, 11.0, 10.0]`?

Jalankan sel berikut untuk mengecek tebakanmu!
"""
        )
    )

    cells.append(
        code(
            """
# Verifikasi Mini-Challenge Softmax (Slide 49)
skor_a = np.array([2.0, 1.0, 0.0])
skor_b = np.array([12.0, 11.0, 10.0])

prob_a = softmax_manual(skor_a)
prob_b = softmax_manual(skor_b)

for nama, pa, pb in zip(["Elsa", "Anna", "Olaf"], prob_a, prob_b):
    print(f"{nama:<6} | skor [2,1,0] -> {pa*100:5.2f}% | skor [12,11,10] -> {pb*100:5.2f}%")
print("Total probabilitas:", round(float(prob_a.sum()), 4), "(selalu 1.0 = 100%!)")
print("✅ Seluruh langkah Hands-on P02 selesai!")
"""
        )
    )

    cells.append(
        md(
            """
## Referensi Video & Sumber Belajar Mandiri (Selaras Slide 58–59)

### Tahap 1–3 · Neuron, Aktivasi `ReLU`, `Softmax` & `Loss` (Slide 58)
1. [3Blue1Brown — *But what is a Neural Network? (Ch. 1)*](https://www.youtube.com/watch?v=aircAruvnKk) *(Wajib — struktur layer, weight & bias)*
2. [StatQuest — *Neural Networks Pt. 1: Inside the Black Box*](https://www.youtube.com/watch?v=CqOfi41LfDw) *(penjelasan ramah pemula)*
3. [3Blue1Brown — *Versi Tulis Neural Networks*](https://3blue1brown.com/lessons/neural-networks)
4. [StatQuest — *Neural Networks Pt. 3: ReLU in Action!*](https://www.youtube.com/watch?v=68BZ5f7P94E) *(Wajib — bukti visual non-linearitas ReLU)*
5. [TensorFlow Playground (Sandbox Interaktif)](https://playground.tensorflow.org/) *(eksperimen langsung di browser)*
6. [StatQuest — *ArgMax and SoftMax*](https://www.youtube.com/watch?v=KpKog-L9veg) *(Wajib — probabilitas 0–100%)*
7. [StatQuest — *Cross-Entropy Loss*](https://www.youtube.com/watch?v=6ArSys5qHAU)
8. [3Blue1Brown — *Gradient Descent (Ch. 2)*](https://www.youtube.com/watch?v=IHZwWFHWa-w) *(Wajib)*

### Tahap 4–5 · Training, Keras & Persiapan P03 (Slide 59)
9. [StatQuest — *Gradient Descent, Step-by-Step*](https://www.youtube.com/watch?v=sDv4f4s2SB8)
10. [3Blue1Brown — *What is Backpropagation Really Doing? (Ch. 3)*](https://www.youtube.com/watch?v=Ilg3gGewQ5U) *(Wajib)*
11. [StatQuest — *Backpropagation Details Pt. 1*](https://www.youtube.com/watch?v=IN2XmBhILt4) *(opsional)*
12. [3Blue1Brown — *Backpropagation Calculus (Ch. 4)*](https://www.youtube.com/watch?v=tIeHLnjs5U8) *(opsional)*
13. [TensorFlow Official — *Classify Images (Fashion-MNIST)*](https://www.tensorflow.org/tutorials/keras/classification) *(Wajib — sejalan Langkah 3)*
14. [Keras Official — *The Sequential Model Guide*](https://keras.io/guides/sequential_model/)
15. [Stanford CS231n — *Lecture Notes (Neural Networks)*](https://cs231n.github.io/) *(opsional)*
16. [Coursera — *Neural Networks and Deep Learning (Course 1)*](https://www.coursera.org/learn/neural-networks-deep-learning) & [Preview P03: *CNN Week 1*](https://www.coursera.org/learn/convolutional-neural-networks)
"""
        )
    )

    return cells


def main() -> None:
    build_notebook_pair(SESSION, build_cells)


if __name__ == "__main__":
    main()
