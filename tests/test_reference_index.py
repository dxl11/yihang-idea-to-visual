"""Tests for build_reference_index and contact sheets (empty library framework)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "yihang-idea-to-visual"
SCRIPTS = SKILL / "scripts"
LIBRARY = SKILL / "assets" / "visual-reference-library"

REQUIRED_CATEGORIES = [
    "editorial",
    "minimalism",
    "technology",
    "artistic",
    "infographic",
    "typography",
    "cover-design",
    "carousel-layout",
    "photography",
    "color-palettes",
]


def test_catalog_is_empty_framework():
    catalog = json.loads((LIBRARY / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["skill_id"] == "yihang-idea-to-visual"
    assert catalog["total_assets"] == 0
    assert catalog.get("assets") == []
    assert catalog.get("items") == []
    for name in REQUIRED_CATEGORIES:
        assert name in catalog["categories"]
        assert (LIBRARY / name / ".gitkeep").is_file()


def test_no_shipped_raster_demos():
    rasters = list(LIBRARY.rglob("*.png")) + list(LIBRARY.rglob("*.jpg")) + list(
        LIBRARY.rglob("*.jpeg")
    ) + list(LIBRARY.rglob("*.webp"))
    assert rasters == [], f"unexpected raster assets: {rasters}"


def test_incremental_index_on_empty_library(tmp_path: Path):
    out = tmp_path / "catalog.json"
    cmd = [
        sys.executable,
        str(SCRIPTS / "build_reference_index.py"),
        "--library",
        str(LIBRARY),
        "--output",
        str(out),
        "--full",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)
    assert proc.returncode == 0, proc.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["stats"]["total"] == 0
    assert data["total_assets"] == 0
    assert data["assets"] == []
    assert data["items"] == []

    proc2 = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "build_reference_index.py"),
            "--library",
            str(LIBRARY),
            "--output",
            str(out),
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc2.returncode == 0, proc2.stderr


def test_contact_sheet_empty_catalog_exits_clean(tmp_path: Path):
    out = tmp_path / "sheets"
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "create_contact_sheet.py"),
            "--library",
            str(LIBRARY),
            "--catalog",
            str(LIBRARY / "catalog.json"),
            "--output",
            str(out),
            "--max-per-sheet",
            "4",
            "--columns",
            "2",
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "No reference assets" in (proc.stdout + proc.stderr)
    assert list(out.glob("contact-sheet-*.png")) == []


def test_skill_documents_empty_library_skip():
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    ref = (SKILL / "references" / "reference-library.md").read_text(encoding="utf-8")
    combined = skill + "\n" + ref
    assert "total_assets" in combined or "skip" in combined.lower()
    assert "visual-reference-library" in skill
