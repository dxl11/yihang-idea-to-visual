"""Rendering tests for render_pages.py."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents" / "skills" / "yihang-idea-to-visual" / "scripts"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


render = _load("render_pages", SCRIPTS / "render_pages.py")


def _find_cjk_font() -> str | None:
    candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ]
    for path in candidates:
        if path.exists():
            return str(path)
    return None


CJK_FONT = _find_cjk_font()


def _base_design(template_id: str, width: int, height: int, text: str) -> dict:
    return {
        "template_id": template_id,
        "canvas": {"width": width, "height": height},
        "colors": {
            "background": "#FFFFFF",
            "text": "#111111",
            "primary": "#1F4B99",
            "secondary": "#999999",
        },
        "typography": {
            "cjk_font_path": CJK_FONT,
            "body_size": 32,
            "caption_size": 20,
            "line_spacing": 1.35,
        },
        "layout": {"margin": 80},
        "text_blocks": [
            {
                "text": text,
                "x": 80,
                "y": 160,
                "size": 32,
                "max_width": width - 160,
                "bottom_limit": height - 120,
            }
        ],
        "shapes": [],
        "images": [],
        "folio": {"text": "01", "x": width - 120, "y": height - 100},
    }


@pytest.mark.skipif(CJK_FONT is None, reason="No CJK font installed on host")
@pytest.mark.parametrize(
    "template_id",
    ["editorial-minimal", "modern-technology", "artistic-journal"],
)
@pytest.mark.parametrize(
    "size",
    [(1080, 1440), (1080, 1350), (1080, 1080)],
)
def test_templates_and_ratios(tmp_path: Path, template_id: str, size: tuple[int, int]):
    design = _base_design(template_id, size[0], size[1], "中文排版测试 ABC 123。")
    out = tmp_path / f"{template_id}-{size[0]}x{size[1]}.png"
    result = render.render_page(design, out)
    assert out.is_file()
    assert result["overflow_flags"] == []
    with Image.open(out) as img:
        assert img.size == size


def test_missing_font_raises(tmp_path: Path):
    with pytest.raises(render.RenderError):
        render.resolve_font(
            str(tmp_path / "missing.ttf"),
            24,
            fallbacks=[],
            use_system_fallbacks=False,
        )


@pytest.mark.skipif(CJK_FONT is None, reason="No CJK font installed on host")
def test_text_overflow_flag(tmp_path: Path):
    design = _base_design("editorial-minimal", 600, 400, "溢出测试" * 80)
    design["text_blocks"][0]["bottom_limit"] = 220
    out = tmp_path / "overflow.png"
    result = render.render_page(design, out)
    assert result["overflow_flags"], "expected overflow flags"


@pytest.mark.skipif(CJK_FONT is None, reason="No CJK font installed on host")
def test_missing_image_errors(tmp_path: Path):
    design = _base_design("modern-technology", 800, 1000, "图片缺失")
    design["images"] = [{"path": "nope.png", "box": [10, 10, 100, 100]}]
    with pytest.raises(render.RenderError, match="image missing"):
        render.render_page(design, tmp_path / "x.png", base_dir=tmp_path)


def test_list_templates_cli():
    import subprocess

    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "render_pages.py"), "--list-templates"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert proc.returncode == 0
    assert "editorial-minimal" in proc.stdout
    assert "modern-technology" in proc.stdout
    assert "artistic-journal" in proc.stdout
