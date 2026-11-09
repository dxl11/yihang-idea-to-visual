"""STEP 03 cover reference retrieval: empty / match / load-fail honesty."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "yihang-idea-to-visual"
SCRIPTS = SKILL / "scripts"
LIBRARY = SKILL / "assets" / "visual-reference-library"
RETRIEVE = SCRIPTS / "retrieve_cover_references.py"


def _run_retrieve(*, library: Path, catalog: Path, query: str = "", categories: list[str] | None = None) -> dict:
    cmd = [
        sys.executable,
        str(RETRIEVE),
        "--library",
        str(library),
        "--catalog",
        str(catalog),
        "--query",
        query,
        "--limit",
        "3",
    ]
    for cat in categories or []:
        cmd.extend(["--category", cat])
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60, check=False)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_empty_library_mode():
    result = _run_retrieve(library=LIBRARY, catalog=LIBRARY / "catalog.json", query="editorial calm")
    assert result["mode"] == "empty"
    assert result["references"] == []
    assert result["image_reference_used"] is False
    assert "empty" in result["disclaimer"].lower() or "without" in result["disclaimer"].lower()


def test_matched_asset_loads_and_is_traceable(tmp_path: Path):
    lib = tmp_path / "lib"
    (lib / "cover-design").mkdir(parents=True)
    img_path = lib / "cover-design" / "sample-editorial.png"
    Image.new("RGB", (400, 600), (240, 236, 228)).save(img_path)

    catalog = {
        "version": "1.0",
        "skill_id": "yihang-idea-to-visual",
        "total_assets": 1,
        "categories": ["cover-design"],
        "assets": [
            {
                "id": "REF-0001",
                "path": "cover-design/sample-editorial.png",
                "filename": "sample-editorial.png",
                "category": "cover-design",
                "tags": ["editorial", "calm", "big-type"],
                "best_for": ["cover"],
                "license": "test",
                "style_notes": "quiet editorial poster",
            }
        ],
        "items": [],
    }
    catalog["items"] = catalog["assets"]
    cat_path = lib / "catalog.json"
    cat_path.write_text(json.dumps(catalog), encoding="utf-8")

    result = _run_retrieve(
        library=lib,
        catalog=cat_path,
        query="editorial calm cover",
        categories=["cover-design"],
    )
    assert result["mode"] == "matched"
    assert len(result["references"]) == 1
    ref = result["references"][0]
    assert ref["id"] == "REF-0001"
    assert ref["load"]["ok"] is True
    assert Path(ref["absolute_path"]).is_file()
    assert result["image_reference_used"] is False  # until host tool call


def test_missing_file_not_treated_as_loaded(tmp_path: Path):
    lib = tmp_path / "lib"
    lib.mkdir()
    catalog = {
        "total_assets": 1,
        "assets": [
            {
                "id": "REF-404",
                "path": "cover-design/does-not-exist.png",
                "category": "cover-design",
                "tags": ["editorial"],
            }
        ],
        "items": [],
    }
    catalog["items"] = catalog["assets"]
    cat_path = lib / "catalog.json"
    cat_path.write_text(json.dumps(catalog), encoding="utf-8")

    result = _run_retrieve(library=lib, catalog=cat_path, query="editorial")
    assert result["mode"] == "no_match"
    assert result["references"] == []
    assert any(r.get("id") == "REF-404" for r in result["rejected"])
    assert result["image_reference_used"] is False


def test_corrupt_image_rejected(tmp_path: Path):
    lib = tmp_path / "lib"
    (lib / "typography").mkdir(parents=True)
    bad = lib / "typography" / "broken.png"
    bad.write_bytes(b"not-an-image")
    catalog = {
        "total_assets": 1,
        "assets": [
            {
                "id": "REF-BAD",
                "path": "typography/broken.png",
                "category": "typography",
                "tags": ["type"],
            }
        ],
        "items": [],
    }
    catalog["items"] = catalog["assets"]
    cat_path = lib / "catalog.json"
    cat_path.write_text(json.dumps(catalog), encoding="utf-8")

    result = _run_retrieve(library=lib, catalog=cat_path, query="type typography")
    assert result["mode"] == "no_match"
    assert result["references"] == []
    assert result["rejected"]
    assert result["rejected"][0]["load"]["ok"] is False


def test_no_match_when_query_misses(tmp_path: Path):
    lib = tmp_path / "lib"
    (lib / "technology").mkdir(parents=True)
    img = lib / "technology" / "neon.png"
    Image.new("RGB", (200, 200), (10, 20, 40)).save(img)
    catalog = {
        "total_assets": 1,
        "assets": [
            {
                "id": "REF-TECH",
                "path": "technology/neon.png",
                "category": "technology",
                "tags": ["neon", "tech"],
            }
        ],
        "items": [],
    }
    catalog["items"] = catalog["assets"]
    cat_path = lib / "catalog.json"
    cat_path.write_text(json.dumps(catalog), encoding="utf-8")

    result = _run_retrieve(library=lib, catalog=cat_path, query="watercolor botanical soft")
    assert result["mode"] == "no_match"
    assert result["references"] == []


def test_cover_docs_require_real_image_load():
    cover = (SKILL / "references" / "cover-design.md").read_text(encoding="utf-8")
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    prompt = (SKILL / "assets" / "templates" / "cover-prompts" / "cover-generation.md").read_text(
        encoding="utf-8"
    )
    blob = cover + skill + prompt
    assert "retrieve_cover_references.py" in blob
    assert "reference_image_paths" in blob or "native reference" in blob.lower()
    assert "Path-in-prompt" in blob or "path-in-prompt" in blob.lower() or "Path-in-prompt" in cover
    assert "STEP03-A" in cover and "STEP03-C" in cover
    assert "structurally" in blob.lower() or "结构" in cover


def test_three_directions_rule_still_present():
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "3 structurally distinct" in skill or "three" in skill.lower()
    assert "render_pages.py" in skill


def test_platform_profiles_still_valid():
    profiles = json.loads(
        (SKILL / "assets" / "platform-profiles" / "profiles.json").read_text(encoding="utf-8")
    )
    xhs = next(p for p in profiles["profiles"] if p["id"] == "xiaohongshu")
    assert xhs["width"] == 1080 and xhs["height"] == 1440
