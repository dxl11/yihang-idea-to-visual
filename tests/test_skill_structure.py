"""Validate yihang-idea-to-visual skill structure and Agent Skills conventions."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents" / "skills" / "yihang-idea-to-visual"
SKILL_MD = SKILL_DIR / "SKILL.md"
SKILL_ID = "yihang-idea-to-visual"

REFERENCE_FILES = [
    "thought-reviewer.md",
    "thinking-frameworks.md",
    "photo-to-poster.md",
    "content-editing.md",
    "title-generation.md",
    "platform-profiles.md",
    "cover-design.md",
    "editorial-design.md",
    "brand-identity.md",
    "reference-library.md",
    "review-and-revision.md",
    "quality-and-export.md",
]

SCRIPTS = [
    "build_thought_index.py",
    "build_reference_index.py",
    "create_contact_sheet.py",
    "render_pages.py",
    "validate_project.py",
    "package_export.py",
]

PHOTO_TO_POSTER_SCRIPTS = [
    "photo_to_poster/inspect_photo.py",
    "photo_to_poster/compose_poster.py",
    "photo_to_poster/validate_poster.py",
    "photo_to_poster/export_posters.py",
]

SCHEMAS = [
    "brand-profile.schema.json",
    "project-state.schema.json",
    "design-profile.schema.json",
    "page-manifest.schema.json",
]


def _parse_frontmatter(text: str) -> dict:
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    end = text.find("\n---\n", 4)
    assert end != -1, "frontmatter closing --- missing"
    block = text[4:end]
    data: dict = {}
    current_key = None
    folded: list[str] = []
    for line in block.splitlines():
        if current_key and (line.startswith("  ") or line.startswith("\t")):
            folded.append(line.strip())
            continue
        if current_key and folded:
            data[current_key] = " ".join(folded).strip()
            folded = []
            current_key = None
        if not line.strip():
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val in {">-", ">"}:
            current_key = key
            folded = []
            continue
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        data[key] = val
    if current_key and folded:
        data[current_key] = " ".join(folded).strip()
    return data


def test_skill_directory_name_matches_id():
    assert SKILL_DIR.name == SKILL_ID
    assert SKILL_MD.is_file()


def test_frontmatter_name_and_description():
    text = SKILL_MD.read_text(encoding="utf-8")
    meta = _parse_frontmatter(text)
    assert meta.get("name") == SKILL_ID
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["name"])
    assert len(meta["name"]) <= 64
    desc = meta.get("description", "")
    assert desc, "description required"
    assert len(desc) <= 1024
    assert "yihang-idea-to-visual" in desc or "Idea to Visual" in desc


def test_skill_md_under_500_lines():
    lines = SKILL_MD.read_text(encoding="utf-8").splitlines()
    assert len(lines) < 500, f"SKILL.md has {len(lines)} lines"


def test_references_exist_and_linked():
    text = SKILL_MD.read_text(encoding="utf-8")
    for name in REFERENCE_FILES:
        path = SKILL_DIR / "references" / name
        assert path.is_file(), f"missing reference {name}"
        assert f"references/{name}" in text.replace("\\", "/"), f"SKILL.md should link {name}"


def test_scripts_and_schemas_exist():
    for name in SCRIPTS:
        assert (SKILL_DIR / "scripts" / name).is_file()
    for name in PHOTO_TO_POSTER_SCRIPTS:
        assert (SKILL_DIR / "scripts" / name).is_file()
    for name in SCHEMAS:
        path = SKILL_DIR / "schemas" / name
        assert path.is_file()
        json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("script", PHOTO_TO_POSTER_SCRIPTS)
def test_photo_to_poster_script_help(script):
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, str(SKILL_DIR / "scripts" / script), "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )
    assert proc.returncode == 0
    combined = f"{proc.stdout or ''}{proc.stderr or ''}".lower()
    assert "usage:" in combined


def test_no_duplicate_cursor_skills_copy():
    cursor_copy = ROOT / ".cursor" / "skills" / SKILL_ID
    assert not cursor_copy.exists(), "Do not duplicate skill under .cursor/skills"


def test_old_skill_id_not_used_as_folder():
    old = ROOT / ".agents" / "skills" / "idea-to-visual"
    assert not old.exists()


def test_readme_pair_exists():
    assert (ROOT / "README.md").is_file()
    assert (ROOT / "README.en.md").is_file()


@pytest.mark.parametrize("script", SCRIPTS)
def test_script_help(script):
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, str(SKILL_DIR / "scripts" / script), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert proc.returncode == 0
    assert "usage:" in proc.stdout.lower() or "usage:" in proc.stderr.lower()
