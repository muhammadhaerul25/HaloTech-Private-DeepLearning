"""Official session metadata registry for HaloTech Private Deep Learning (P01–P08)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
MATERIALS_DIR = ROOT_DIR / "materials"
TOOLS_DIR = ROOT_DIR / "tools"
SESSIONS_CODE_DIR = TOOLS_DIR / "sessions"
DATA_DIR = ROOT_DIR / "data"
RESULTS_DIR = ROOT_DIR / "results"


@dataclass(frozen=True)
class SessionConfig:
    id: str                  # e.g. "P01"
    num: int                 # e.g. 1
    url_slug: str            # e.g. "/p1"
    file_slug: str           # e.g. "understanding_images_processing_eda"
    title: str               # Display title
    short_title: str         # Footer / browser tab short title
    phase: str               # "Fondasi" | "Eksperimen" | "Analisis & Pelaporan"
    color: str               # Accent hex color
    tint: str                # Card tint hex color
    plan_ref: str            # Reference to docs/PLAN.md section
    duration_minutes: float = 120.0
    is_legacy_p01: bool = False
    folder_name: str = ""    # Optional custom materials folder name (defaults to id, e.g. "P02")
    code_folder_name: str = ""  # Optional custom tools/sessions folder name (defaults to folder_name or id)
    file_stem: str = ""      # Optional custom file stem (defaults to "{id}_{file_slug}")

    @property
    def dir_name(self) -> str:
        return self.folder_name or self.id

    @property
    def code_dir_name(self) -> str:
        return self.code_folder_name or self.dir_name

    @property
    def stem(self) -> str:
        return self.file_stem or f"{self.id}_{self.file_slug}"

    @property
    def material_dir(self) -> Path:
        return MATERIALS_DIR / self.dir_name

    @property
    def assets_dir(self) -> Path:
        return self.material_dir / "assets" / self.id

    @property
    def solutions_dir(self) -> Path:
        return self.material_dir / "solutions"

    @property
    def code_dir(self) -> Path:
        return SESSIONS_CODE_DIR / self.code_dir_name

    @property
    def html_path(self) -> Path:
        return self.material_dir / f"{self.stem}.html"

    @property
    def pdf_path(self) -> Path:
        return self.material_dir / f"{self.stem}.pdf"

    @property
    def pptx_path(self) -> Path:
        return self.material_dir / f"{self.stem}.pptx"

    @property
    def presenter_script_path(self) -> Path:
        if self.file_stem:
            return self.material_dir / f"{self.stem}_presenter_script.pdf"
        return self.material_dir / f"{self.id}_presenter_script.pdf"

    @property
    def notebook_student_path(self) -> Path:
        return self.material_dir / f"{self.stem}.ipynb"

    @property
    def notebook_solution_path(self) -> Path:
        return self.solutions_dir / f"{self.stem}.ipynb"

    @property
    def rel_html(self) -> str:
        return f"materials/{self.dir_name}/{self.stem}.html"

    @property
    def rel_pdf(self) -> str:
        return f"materials/{self.dir_name}/{self.stem}.pdf"

    @property
    def rel_pptx(self) -> str:
        return f"materials/{self.dir_name}/{self.stem}.pptx"

    @property
    def rel_notebook(self) -> str:
        return f"materials/{self.dir_name}/{self.stem}.ipynb"

    @property
    def rel_solution(self) -> str:
        return f"materials/{self.dir_name}/solutions/{self.stem}.ipynb"


SESSIONS: dict[str, SessionConfig] = {
    "P01": SessionConfig(
        id="P01",
        num=1,
        url_slug="/p1",
        file_slug="understanding_images_processing_eda",
        title="Understanding Images, Image Processing & EDA",
        short_title="Memahami Gambar di Komputer & Image Processing",
        phase="Fondasi",
        color="#4285F4",
        tint="#E8F0FE",
        plan_ref="P4",
        is_legacy_p01=True,
    ),
    "P02": SessionConfig(
        id="P02",
        num=2,
        url_slug="/p2",
        file_slug="teori_neural_network",
        title="Teori Neural Network",
        short_title="Teori Neural Network — AI/ML/DL, CV Tasks & Backprop",
        phase="Fondasi",
        color="#EA4335",
        tint="#FCE8E6",
        plan_ref="P5-P6 (Redesign)",
        folder_name="P02",
        code_folder_name="p02_teori_neural_network",
        file_stem="p02_teori_neural_network",
    ),
    "P03": SessionConfig(
        id="P03",
        num=3,
        url_slug="/p3",
        file_slug="arsitektur_neural_network",
        title="Arsitektur Neural Network",
        short_title="Arsitektur Neural Network — MLP, CNN, ResNet, MobileNetV2 & EfficientNet",
        phase="Fondasi",
        color="#FBBC04",
        tint="#FEF7E0",
        plan_ref="P5-P7 (Evolusi 5 Arsitektur)",
    ),
    "P04": SessionConfig(
        id="P04",
        num=4,
        url_slug="/p4",
        file_slug="cnn_architectures_transfer_learning",
        title="Arsitektur CNN & Transfer Learning",
        short_title="Arsitektur CNN & Transfer Learning (MobileNetV2)",
        phase="Fondasi",
        color="#34A853",
        tint="#E6F4EA",
        plan_ref="P7",
    ),
    "P05": SessionConfig(
        id="P05",
        num=5,
        url_slug="/p5",
        file_slug="data_methodology_splitting",
        title="Metodologi Data: Collection, Splitting & Desain Eksperimen",
        short_title="Metodologi Data, Splitting & Anti-Leakage",
        phase="Eksperimen",
        color="#4285F4",
        tint="#E8F0FE",
        plan_ref="P8",
    ),
    "P06": SessionConfig(
        id="P06",
        num=6,
        url_slug="/p6",
        file_slug="data_pipeline_augmentation_baseline",
        title="Data Pipeline, Augmentation & Model Baseline",
        short_title="Data Pipeline, Augmentation & Model Baseline",
        phase="Eksperimen",
        color="#EA4335",
        tint="#FCE8E6",
        plan_ref="P9",
    ),
    "P07": SessionConfig(
        id="P07",
        num=7,
        url_slug="/p7",
        file_slug="training_finetuning",
        title="Training Lengkap & Fine-tuning",
        short_title="Training Lengkap & Fine-tuning MobileNetV2",
        phase="Eksperimen",
        color="#FBBC04",
        tint="#FEF7E0",
        plan_ref="P10",
    ),
    "P08": SessionConfig(
        id="P08",
        num=8,
        url_slug="/p8",
        file_slug="evaluation_error_analysis_gradcam",
        title="Evaluasi Metrics, Analisis Error & Grad-CAM",
        short_title="Evaluasi Metrics, Analisis Error & Grad-CAM",
        phase="Analisis & Pelaporan",
        color="#34A853",
        tint="#E6F4EA",
        plan_ref="P11-P12",
    ),
}


def get_session(session_id: str) -> SessionConfig:
    """Resolve session ID such as 'P02', 'p2', or '2' to a SessionConfig."""
    key = session_id.strip().upper()
    if key.isdigit():
        key = f"P{int(key):02d}"
    elif key.startswith("P") and key[1:].isdigit():
        key = f"P{int(key[1:]):02d}"
    if key not in SESSIONS:
        valid = ", ".join(sorted(SESSIONS.keys()))
        raise KeyError(f"Sesi tidak dikenal: '{session_id}'. Pilihan valid: {valid}")
    return SESSIONS[key]
