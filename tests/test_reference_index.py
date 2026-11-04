"""Tests for build_reference_index and contact sheets."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "yihang-idea-to-visual"
SCRIPTS = SKILL / "scripts"
LIBRARY = SKILL / "assets" / "visual-reference-library"


def test_catalog_exists_and_has_items():
    catalog = json.loads((LIBRARY / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["skill_id"] == "yihang-idea-to-visual"
    assert len(catalog["items"]) >= 1
    for item in catalog["items"]:
        assert "sha256" in item
        assert "width" in item
        assert "height" in item
        assert item.get("license") in {"MIT", "unknown", "private", "CC0", "CC-BY-4.0"}


def test_incremental_index(tmp_path: Path):
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
    assert data["stats"]["total"] >= 1

    # Incremental second run should succeed
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


def test_contact_sheet(tmp_path: Path):
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
    sheets = list(out.glob("contact-sheet-*.png"))
    assert sheets
    from PIL import Image

    with Image.open(sheets[0]) as img:
        img.verify()
