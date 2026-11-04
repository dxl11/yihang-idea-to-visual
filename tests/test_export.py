"""Export and project validation tests."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import zipfile
from pathlib import Path

import pytest
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents" / "skills" / "yihang-idea-to-visual" / "scripts"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


validate = _load("validate_project", SCRIPTS / "validate_project.py")
package = _load("package_export", SCRIPTS / "package_export.py")
ti = _load("text_integrity", SCRIPTS / "text_integrity.py")


ARTICLE = """第一段：关于个人表达的长期主义。

第二段：把复杂想法拆成可读页面，而不是删减原意。符号：100%、A/B、#标签。

第三段短。
"""


def _font():
    for path in [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path("/System/Library/Fonts/PingFang.ttc"),
    ]:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), 28)
            except OSError:
                continue
    return ImageFont.load_default()


def _write_png(path: Path, size=(1080, 1440), label="page"):
    img = Image.new("RGB", size, (250, 248, 242))
    draw = ImageDraw.Draw(img)
    draw.text((80, 80), label, fill=(20, 20, 20), font=_font())
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def _build_project(tmp_path: Path) -> Path:
    project = tmp_path / "sample-project"
    (project / "content").mkdir(parents=True)
    (project / "pages").mkdir(parents=True)
    (project / "output" / "cover").mkdir(parents=True)
    (project / "output" / "pages").mkdir(parents=True)
    (project / "history").mkdir(parents=True)

    article = ti.normalize_article_text(ARTICLE)
    (project / "content" / "final-article.md").write_text(article + "\n", encoding="utf-8")
    # Split into two body fragments covering full article exactly
    mid = len(article) // 2
    frag1, frag2 = article[:mid], article[mid:]

    state = {
        "project_name": "sample-project",
        "skill_id": "yihang-idea-to-visual",
        "status": "finalized",
        "updated_at": "2026-03-25T00:00:00Z",
        "canvas": {"width": 1080, "height": 1440},
        "locks": {"article": True, "title": True, "cover": True, "editorial": True},
    }
    (project / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    cover = project / "output" / "cover" / "00-cover.png"
    p1 = project / "output" / "pages" / "01-page.png"
    p2 = project / "output" / "pages" / "02-page.png"
    _write_png(cover, label="cover")
    _write_png(p1, label="page1")
    _write_png(p2, label="page2")

    manifest = {
        "project_name": "sample-project",
        "article_version": "v1",
        "article_path": "content/final-article.md",
        "canvas": {"width": 1080, "height": 1440},
        "pages": [
            {
                "index": 0,
                "role": "cover",
                "output_file": "output/cover/00-cover.png",
                "text_fragments": [],
                "page_number": None,
                "overflow_flags": [],
            },
            {
                "index": 1,
                "role": "body",
                "output_file": "output/pages/01-page.png",
                "text_fragments": [frag1],
                "page_number": 1,
                "overflow_flags": [],
            },
            {
                "index": 2,
                "role": "body",
                "output_file": "output/pages/02-page.png",
                "text_fragments": [frag2],
                "page_number": 2,
                "overflow_flags": [],
            },
        ],
    }
    (project / "pages" / "page-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return project


def test_validate_ok(tmp_path: Path):
    project = _build_project(tmp_path)
    report = validate.validate_project(project)
    assert report["ok"], report["errors"]


def test_validate_detects_integrity_break(tmp_path: Path):
    project = _build_project(tmp_path)
    manifest = json.loads((project / "pages" / "page-manifest.json").read_text(encoding="utf-8"))
    manifest["pages"][1]["text_fragments"] = ["被篡改的片段"]
    (project / "pages" / "page-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report = validate.validate_project(project)
    assert not report["ok"]
    assert any("integrity" in e for e in report["errors"])


def test_package_zip_and_order(tmp_path: Path):
    project = _build_project(tmp_path)
    result = package.package_project(project, export_name="sample-project")
    assert Path(result["zip"]).is_file()
    assert result["files"][0] == "00-cover.png"
    assert result["files"][1] == "01-page.png"
    assert result["files"][2] == "02-page.png"
    with zipfile.ZipFile(result["zip"], "r") as zf:
        assert zf.testzip() is None
        names = zf.namelist()
        assert "sample-project/00-cover.png" in names
        # PNG opens
        with zf.open("sample-project/01-page.png") as handle:
            with Image.open(handle) as img:
                img.verify()


def test_package_errors_when_page_missing(tmp_path: Path):
    project = _build_project(tmp_path)
    missing = project / "output" / "pages" / "02-page.png"
    missing.unlink()
    with pytest.raises(package.PackageError, match="missing PNG"):
        package.package_project(project)


def test_wrong_skill_id_fails(tmp_path: Path):
    project = _build_project(tmp_path)
    state = json.loads((project / "state.json").read_text(encoding="utf-8"))
    state["skill_id"] = "idea-to-visual"
    (project / "state.json").write_text(json.dumps(state), encoding="utf-8")
    report = validate.validate_project(project)
    assert not report["ok"]
    assert any("yihang-idea-to-visual" in e for e in report["errors"])
