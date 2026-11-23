"""Unified 6-Gate Definition-of-Done Validator for HaloTech Private Deep Learning (P01–P08)."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from .exporter import count_pdf_pages
from .registry import ROOT_DIR, SessionConfig

DATETIME_PATTERN = re.compile(
    r"\b(?:Minggu|Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|"
    r"Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember|"
    r"202[4-9]|WIB|WITA|WIT)\b|13:00|15:00|19:30|21:30",
    flags=re.IGNORECASE,
)

# Forbidden old PLAN.md session codes (P9..P13 never exist in P01..P08 curriculum)
LEGACY_HIGH_CODE_PATTERN = re.compile(r"\bP(?:0?9|1[0-3])\b")


def load_presenter_explanations(session: SessionConfig) -> dict[int, list[str]]:
    """Load `SLIDE_EXPLANATIONS` dict for either legacy P01 or modular P02+ sessions."""
    candidates = [
        session.code_dir / "presenter_notes.py",
        ROOT_DIR / "tools" / f"build_presenter_script_{session.id}.py",
    ]
    for path in candidates:
        if path.exists():
            spec = importlib.util.spec_from_file_location(f"_notes_{session.id}", path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "SLIDE_EXPLANATIONS"):
                    return dict(mod.SLIDE_EXPLANATIONS)
    return {}


def validate_html(session: SessionConfig) -> dict:
    assert session.html_path.exists(), f"Missing HTML: {session.html_path}"
    text = session.html_path.read_text(encoding="utf-8")

    slide_count = len(re.findall(r'<section class="slide\b', text))
    assert slide_count >= 18, f"Slide HTML terlalu sedikit ({slide_count})"

    # Check page-jump max and counter match actual slide count
    m_max = re.search(r'id="page-jump"[^>]*max="(\d+)"', text)
    assert m_max, "Missing max attribute on #page-jump"
    assert int(m_max.group(1)) == slide_count, (
        f"#page-jump max={m_max.group(1)} tidak cocok dengan jumlah slide aktual ({slide_count})"
    )
    m_cnt = re.search(r'<span id="counter"[\s\S]*?<span>\s*/\s*(\d+)\s*</span>', text)
    assert m_cnt, "Missing / N counter span"
    assert int(m_cnt.group(1)) == slide_count, (
        f"Counter / {m_cnt.group(1)} tidak cocok dengan jumlah slide aktual ({slide_count})"
    )

    body_part = text.split('<div id="stage-wrap">', 1)[1].split('<div id="controls">', 1)[0]

    # Check no datetime tokens
    dt_matches = DATETIME_PATTERN.findall(body_part)
    assert not dt_matches, f"Ditemukan teks tanggal/jam (melanggar kebijakan timeless): {dt_matches[:10]}"

    # Check no legacy P09-P13 codes
    legacy_codes = LEGACY_HIGH_CODE_PATTERN.findall(body_part)
    assert not legacy_codes, f"Ditemukan kode sesi lama (P09–P13) di slide: {legacy_codes[:10]}"

    # Check referenced local assets exist
    imgs = re.findall(rf'src="(assets/{session.id}/[^"]+)"', text)
    missing_imgs = [img for img in imgs if not (session.material_dir / img).exists()]
    assert not missing_imgs, f"Aset gambar HTML tidak ditemukan: {missing_imgs}"

    # Check speaker notes presence and total duration == 120.0 minutes
    notes = re.findall(r'data-notes="([^"]+)"', text)
    assert len(notes) == slide_count, f"Jumlah data-notes ({len(notes)}) != jumlah slide ({slide_count})"
    total_min = 0.0
    for idx, note in enumerate(notes, 1):
        m = re.search(r"Alokasi waktu:\s*([0-9.]+)\s*menit", note)
        assert m, f"Slide {idx} tidak memiliki 'Alokasi waktu: X menit' pada data-notes"
        total_min += float(m.group(1))
    assert abs(total_min - session.duration_minutes) < 1e-6, (
        f"Total alokasi waktu speaker notes = {total_min:.2f} menit, wajib tepat {session.duration_minutes:.1f} menit"
    )

    return {
        "slide_count": slide_count,
        "local_assets_checked": len(imgs),
        "speaker_notes_total_min": round(total_min, 2),
        "timeless_ok": True,
    }


def validate_pdf_and_pptx(session: SessionConfig) -> dict:
    from pptx import Presentation

    assert session.pdf_path.exists(), f"Missing PDF: {session.pdf_path}"
    assert session.pptx_path.exists(), f"Missing PPTX: {session.pptx_path}"

    pdf_pages = count_pdf_pages(session.pdf_path)
    prs = Presentation(session.pptx_path)
    pptx_slides = len(prs.slides)

    w_in = round(prs.slide_width.inches, 3)
    h_in = round(prs.slide_height.inches, 3)
    assert abs((w_in / h_in) - (16 / 9)) < 0.01, f"PPTX bukan 16:9: {w_in}x{h_in}"
    assert pdf_pages == pptx_slides, (
        f"Jumlah halaman PDF ({pdf_pages}) != jumlah slide PPTX ({pptx_slides})"
    )

    missing_notes = []
    for i, slide in enumerate(prs.slides, 1):
        txt = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        if not txt:
            missing_notes.append(i)
            continue
        dt_hits = DATETIME_PATTERN.findall(txt)
        assert not dt_hits, f"PPTX Slide {i} speaker notes mengandung teks tanggal/jam: {dt_hits}"

    assert not missing_notes, f"PPTX slide tanpa speaker notes: {missing_notes}"

    return {
        "pdf_pages": pdf_pages,
        "pptx_slides": pptx_slides,
        "parity_ok": True,
        "pptx_notes_coverage": f"{pptx_slides}/{pptx_slides}",
    }


def validate_presenter_script(session: SessionConfig, html_slide_count: int) -> dict:
    assert session.presenter_script_path.exists(), f"Missing Presenter Script PDF: {session.presenter_script_path}"
    pages = count_pdf_pages(session.presenter_script_path)
    assert pages >= html_slide_count, (
        f"Halaman Presenter Script ({pages}) < jumlah slide HTML ({html_slide_count})"
    )
    explanations = load_presenter_explanations(session)
    missing_exp = [n for n in range(1, html_slide_count + 1) if n not in explanations or not explanations[n]]
    assert not missing_exp, f"SLIDE_EXPLANATIONS belum mencakup slide: {missing_exp}"
    return {
        "presenter_pdf_pages": pages,
        "explanations_covered": f"{html_slide_count}/{html_slide_count}",
    }


def validate_notebooks(session: SessionConfig, execute: bool = True) -> dict:
    import nbformat

    assert session.notebook_student_path.exists(), f"Missing Student Notebook: {session.notebook_student_path}"
    assert session.notebook_solution_path.exists(), f"Missing Solution Notebook: {session.notebook_solution_path}"

    nb_stu = nbformat.read(session.notebook_student_path, as_version=4)
    nb_sol = nbformat.read(session.notebook_solution_path, as_version=4)

    todo_code_indices = [
        i for i, c in enumerate(nb_stu.cells)
        if c.cell_type == "code" and "# TODO" in c.source
    ]
    hint_md_indices = [
        i for i, c in enumerate(nb_stu.cells)
        if c.cell_type == "markdown" and "<details>" in c.source and "Hint" in c.source
    ]
    assert len(todo_code_indices) > 0, "Notebook peserta harus memiliki minimal 1 sel latihan # TODO"
    assert len(todo_code_indices) == len(hint_md_indices), (
        f"Jumlah sel # TODO ({len(todo_code_indices)}) != jumlah sel <details> Hint ({len(hint_md_indices)})"
    )

    sol_todos = [i for i, c in enumerate(nb_sol.cells) if c.cell_type == "code" and "# TODO" in c.source]
    assert not sol_todos, f"Notebook solusi masih mengandung # TODO pada sel: {sol_todos}"

    sol_executed = False
    stu_prefix_ok = False
    first_todo_idx = todo_code_indices[0]

    if execute:
        env = os.environ.copy()
        env["SMOKE_TEST"] = "1"

        # 1. Execute full solution notebook in a temp copy so we don't dirty tracked files
        with tempfile.TemporaryDirectory(prefix=f"nb_val_{session.id.lower()}_") as tmp_dir:
            tmp_sol_out = Path(tmp_dir) / "sol_exec.ipynb"
            cmd = [
                sys.executable, "-m", "jupyter", "nbconvert",
                "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=300",
                "--output", str(tmp_sol_out),
                str(session.notebook_solution_path.resolve()),
            ]
            res = subprocess.run(cmd, cwd=str(ROOT_DIR), env=env, capture_output=True, text=True)
            assert res.returncode == 0, (
                f"Eksekusi Notebook Solusi GAGAL (SMOKE_TEST=1):\n{res.stderr[-1500:]}"
            )
            sol_executed = True

            # 2. Execute student notebook cells strictly BEFORE first # TODO cell
            # Place temp input in session.material_dir so relative BASE_DIR discovery matches real location
            prefix_nb = nbformat.v4.new_notebook(metadata=nb_stu.metadata)
            prefix_nb.cells = nb_stu.cells[:first_todo_idx]
            tmp_stu_in = session.material_dir / f"_tmp_val_stu_{session.id}.ipynb"
            tmp_stu_out = Path(tmp_dir) / "stu_prefix_exec.ipynb"
            nbformat.write(prefix_nb, tmp_stu_in)
            try:
                cmd_stu = [
                    sys.executable, "-m", "jupyter", "nbconvert",
                    "--to", "notebook", "--execute",
                    "--ExecutePreprocessor.timeout=180",
                    "--output", str(tmp_stu_out),
                    str(tmp_stu_in.resolve()),
                ]
                res_stu = subprocess.run(cmd_stu, cwd=str(ROOT_DIR), env=env, capture_output=True, text=True)
                assert res_stu.returncode == 0, (
                    f"Eksekusi sel awal Notebook Peserta (sebelum # TODO pertama) GAGAL:\n{res_stu.stderr[-1500:]}"
                )
                stu_prefix_ok = True
            finally:
                tmp_stu_in.unlink(missing_ok=True)

    return {
        "student_cells": len(nb_stu.cells),
        "solution_cells": len(nb_sol.cells),
        "todo_count": len(todo_code_indices),
        "hint_details_count": len(hint_md_indices),
        "solution_smoke_executed": sol_executed,
        "student_prefix_executed": stu_prefix_ok,
    }


def validate_portal_sync(session: SessionConfig) -> dict:
    sessions_json = json.loads((ROOT_DIR / "sessions.json").read_text(encoding="utf-8"))
    entry = next((s for s in sessions_json.get("sessions", []) if s.get("id") == session.id), None)
    assert entry is not None, f"{session.id} tidak ditemukan di sessions.json"

    status = entry.get("status")
    if status != "available":
        return {"portal_status": status, "registered": False}

    links = entry.get("links", {})
    for key in ("slidesHtml", "slidesPdf", "slidesPptx", "notebook", "solution"):
        rel = links.get(key)
        assert rel, f"sessions.json {session.id}.links.{key} kosong"
        assert (ROOT_DIR / rel).exists(), f"Target path sessions.json tidak ada: {rel}"

    vercel_cfg = json.loads((ROOT_DIR / "vercel.json").read_text(encoding="utf-8"))
    rewrites = {r["source"]: r["destination"] for r in vercel_cfg.get("rewrites", [])}
    expected_dest = "/" + session.rel_html
    assert rewrites.get(session.url_slug) == expected_dest, (
        f"vercel.json rewrite {session.url_slug} != {expected_dest}"
    )

    sw_text = (ROOT_DIR / "sw.js").read_text(encoding="utf-8")
    assert f"./{session.rel_html}" in sw_text, f"sw.js belum memasukkan ./{session.rel_html} ke PRECACHE_ASSETS"

    return {"portal_status": "available", "registered": True}


def validate_session(
    session: SessionConfig,
    *,
    execute_notebooks: bool = True,
    check_portal: bool = True,
) -> dict:
    """Run all 6 Definition-of-Done gates for `session`."""
    res_html = validate_html(session)
    res_pdf_pptx = validate_pdf_and_pptx(session)
    res_presenter = validate_presenter_script(session, res_html["slide_count"])
    res_nb = validate_notebooks(session, execute=execute_notebooks)
    res_portal = validate_portal_sync(session) if check_portal else {"skipped": True}
    return {
        "session": session.id,
        "html": res_html,
        "pdf_pptx": res_pdf_pptx,
        "presenter_script": res_presenter,
        "notebooks": res_nb,
        "portal_pwa": res_portal,
        "status": "PASSED",
    }
