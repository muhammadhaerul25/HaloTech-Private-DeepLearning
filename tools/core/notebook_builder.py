"""Standard Beginner-Friendly Notebook Builder Helpers (P02–P08).

Enforces the P01 cell-by-cell standard:
- Short code cells (5–15 lines), one simple action per cell, Bahasa Indonesia comments.
- Mandatory 3-stage Setup (Libraries + Version, Colab/Local + SEED=42, Config & Paths).
- Student version: focused `# TODO` + `assert` paired with a `<details>` Hint & Jawaban cell.
- Solution version: all `# TODO` completed, no `<details>` hint cells, passes `SMOKE_TEST=1`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from .registry import SessionConfig

try:
    import nbformat as nbf
except ImportError:
    nbf = None


def _to_source_lines(text: str) -> list[str]:
    return text.strip().splitlines(keepends=True)


def md(text: str):
    if nbf is not None:
        return nbf.v4.new_markdown_cell(text.strip())
    return {
        "cell_type": "markdown",
        "id": f"md-{abs(hash(text)) % 10**8:08d}",
        "metadata": {},
        "source": _to_source_lines(text),
    }


def code(text: str):
    if nbf is not None:
        return nbf.v4.new_code_cell(text.strip())
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": f"code-{abs(hash(text)) % 10**8:08d}",
        "metadata": {},
        "outputs": [],
        "source": _to_source_lines(text),
    }


def todo_block(
    cells: list,
    *,
    is_solution: bool,
    title: str,
    instruction_md: str,
    student_code: str,
    solution_code: str,
    hint_code: str,
    hint_label: str | None = None,
) -> None:
    """Append a standardized `# TODO` exercise cell (+ `<details>` hint on student version)."""
    cells.append(md(f"### {title}\n{instruction_md.strip()}"))
    if is_solution:
        cells.append(code(solution_code))
    else:
        cells.append(code(student_code))
        label = hint_label or title
        cells.append(
            md(
                f"""
<details>
<summary><b>💡 Hint &amp; Jawaban {label}</b> (klik untuk membuka)</summary>

```python
{hint_code.strip()}
```
</details>
"""
            )
        )


def setup_cells_standard(
    *,
    extra_imports: str = "",
    use_tensorflow: bool = False,
    extra_config: str = "",
) -> list:
    """Return the mandatory 3-stage Setup cells (6 cells: 3 markdown + 3 code)."""
    cells = []

    tf_import = (
        "import tensorflow as tf             # TensorFlow/Keras: untuk membangun & melatih Neural Network\n"
        if use_tensorflow
        else ""
    )
    tf_ver = 'print("Versi TensorFlow :", tf.__version__)\n' if use_tensorflow else ""

    cells.append(
        md(
            """
## Setup 1/3: Memanggil Pustaka (*Libraries*) Python
Kita panggil alat-alat Python yang diperlukan dan mencetak versinya agar eksperimen dapat direproduksi (*reproducible*).
"""
        )
    )
    cells.append(
        code(
            f"""
import os                           # Untuk membaca pengaturan komputer / environment
import random                       # Untuk mengunci angka acak bawaan Python
from pathlib import Path            # Untuk mengatur alamat folder & file

import numpy as np                  # NumPy: untuk mengolah matriks/tabel angka
import pandas as pd                 # Pandas: untuk membuat tabel laporan
import matplotlib.pyplot as plt     # Matplotlib: untuk menampilkan gambar & grafik
{tf_import}{extra_imports.strip()}

print("✅ Semua library berhasil dimuat!")
print("Versi NumPy      :", np.__version__)
{tf_ver}""".rstrip()
        )
    )

    tf_seed = "tf.random.set_seed(SEED)\n" if use_tensorflow else ""
    cells.append(
        md(
            """
## Setup 2/3: Deteksi Google Colab & Mengunci `SEED = 42`
Notebook ini bisa berjalan di **Google Colab** maupun di **komputer lokal**. Kita kunci `SEED = 42` agar hasil acak selalu konsisten setiap kali dijalankan ulang.
"""
        )
    )
    cells.append(
        code(
            f"""
# Cek apakah notebook dijalankan di Google Colab atau lokal
try:
    import google.colab  # noqa: F401
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# Kunci angka acak (SEED = 42) untuk reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
{tf_seed}
print("Berjalan di Google Colab :", IN_COLAB)
print("SEED dikunci pada        :", SEED)
""".rstrip()
        )
    )

    cells.append(
        md(
            """
## Setup 3/3: Konfigurasi Proyek & Alamat Folder
Daftar kelas, ukuran gambar (`IMG_SIZE = 224`), dan folder data disimpan sebagai variabel konfigurasi di sini (tidak di-*hardcode*) agar nanti mudah diganti ke foto Disney buatan sendiri.
"""
        )
    )
    cells.append(
        code(
            f"""
# Konfigurasi utama proyek (dinamis — tetap aman jika jumlah foto dataset ditambah nanti)
IMG_SIZE = 224
SMOKE_TEST = os.environ.get("SMOKE_TEST", "0") == "1"
CLASS_NAMES = ["anna", "elsa", "kristoff", "olaf", "sven"]
{extra_config.strip()}

# Cari folder utama proyek yang memiliki folder "data/"
BASE_DIR = Path(".")
for folder in [Path("."), Path(".."), Path("../.."), Path("../../..")]:
    if (folder / "data").exists():
        BASE_DIR = folder
        break

# Gunakan dataset proyek utama Disney Frozen (otomatis fallback ke data/sample jika belum tersedia)
DATA_DIR = BASE_DIR / "data" / "frozen_v1"
if not DATA_DIR.exists():
    DATA_DIR = BASE_DIR / "data" / "sample"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print("Mode SMOKE_TEST  :", SMOKE_TEST)
print("Folder Dataset   :", DATA_DIR.resolve())
print("Folder Hasil     :", RESULTS_DIR.resolve())
""".rstrip()
        )
    )
    return cells


def write_notebook(path: Path, cells: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if nbf is not None:
        nb = nbf.v4.new_notebook()
        nb.metadata["kernelspec"] = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }
        nb.metadata["language_info"] = {"name": "python", "version": "3.11"}
        nb.cells = cells
        with open(path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
    else:
        nb_dict = {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python", "version": "3.11"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        path.write_text(json.dumps(nb_dict, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Written: {path} ({len(cells)} cells)")


def build_notebook_pair(session: SessionConfig, build_cells_fn: Callable[[bool], list]) -> dict:
    """Build both student and solution notebooks for `session`."""
    student_cells = build_cells_fn(False)
    solution_cells = build_cells_fn(True)
    write_notebook(session.notebook_student_path, student_cells)
    write_notebook(session.notebook_solution_path, solution_cells)
    return {
        "student_path": str(session.notebook_student_path),
        "student_cells": len(student_cells),
        "solution_path": str(session.notebook_solution_path),
        "solution_cells": len(solution_cells),
    }
