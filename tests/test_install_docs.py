"""Ensure bilingual install docs stay aligned with official Skills CLI commands."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_CN = ROOT / "README.md"
README_EN = ROOT / "README.en.md"
SKILL_MD = ROOT / ".agents" / "skills" / "yihang-idea-to-visual" / "SKILL.md"

REPO_URL = "https://github.com/dxl11/yihang-idea-to-visual"
OWNER_REPO = "dxl11/yihang-idea-to-visual"
SKILL_ID = "yihang-idea-to-visual"

REQUIRED_COMMANDS = [
    f"npx skills add {OWNER_REPO} --skill {SKILL_ID} -a cursor",
    f"npx skills add {OWNER_REPO} --skill {SKILL_ID} -a cursor -g",
    f"npx skills add {OWNER_REPO} --list",
    "npx skills list",
    "npx skills ls -a cursor",
    "npx skills check",
    f"npx skills update {SKILL_ID}",
    f"npx skills update {SKILL_ID} -g",
    f"npx skills remove {SKILL_ID} -a cursor",
    f"npx skills remove {SKILL_ID} -a cursor -g",
]

FORBIDDEN_PLACEHOLDERS = [
    "GITHUB_OWNER",
    "example/idea-to-visual",
    "your-fork-or-repo-url",
    "<your-",
]


def test_readme_pair_language_switch_links():
    cn = README_CN.read_text(encoding="utf-8")
    en = README_EN.read_text(encoding="utf-8")
    assert "[English](README.en.md)" in cn
    assert "[简体中文](README.md)" in en


def test_github_url_and_skill_id_consistent():
    for path in (README_CN, README_EN, ROOT / "pyproject.toml", ROOT / "CONTRIBUTING.md"):
        text = path.read_text(encoding="utf-8")
        assert REPO_URL in text, f"missing repo URL in {path}"
        assert SKILL_ID in text, f"missing skill id in {path}"
        for bad in FORBIDDEN_PLACEHOLDERS:
            assert bad not in text, f"placeholder {bad!r} found in {path}"


def test_required_install_commands_present_in_both_readmes():
    cn = README_CN.read_text(encoding="utf-8")
    en = README_EN.read_text(encoding="utf-8")
    for cmd in REQUIRED_COMMANDS:
        assert cmd in cn, f"missing in README.md: {cmd}"
        assert cmd in en, f"missing in README.en.md: {cmd}"


def test_node_requirement_documented():
    for path in (README_CN, README_EN):
        text = path.read_text(encoding="utf-8")
        assert "22.20" in text
        assert "node -v" in text
        assert "npm -v" in text


def test_skill_frontmatter_name():
    text = SKILL_MD.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert re.search(r"^name:\s*yihang-idea-to-visual\s*$", text, re.M)


def test_no_duplicate_cursor_skills_tree():
    assert not (ROOT / ".cursor" / "skills" / SKILL_ID).exists()


def test_section_order_markers_present():
    """Both READMEs follow the agreed top-level section sequence."""
    markers_cn = [
        "## 1. 项目名称和介绍",
        "## 2. 项目核心定位",
        "## 3. 核心功能",
        "## 4. 一键安装命令",
        "## 5. Cursor 项目级和全局安装",
        "## 6. 完整创作工作流",
        "## 7. 视觉参考库介绍",
        "## 8. 个人品牌视觉系统",
        "## 9. 使用示例",
        "## 10. 更新与卸载",
        "## 11. 项目目录",
        "## 12. 贡献指南",
        "## 13. 版权与隐私说明",
    ]
    markers_en = [
        "## 1. Project name and introduction",
        "## 2. Core positioning",
        "## 3. Core features",
        "## 4. One-command install",
        "## 5. Cursor project vs global install",
        "## 6. Full creative workflow",
        "## 7. Visual reference library",
        "## 8. Personal brand visual system",
        "## 9. Usage examples",
        "## 10. Update and uninstall",
        "## 11. Repository layout",
        "## 12. Contributing",
        "## 13. Copyright and privacy",
    ]
    cn = README_CN.read_text(encoding="utf-8")
    en = README_EN.read_text(encoding="utf-8")
    positions_cn = [cn.index(m) for m in markers_cn]
    positions_en = [en.index(m) for m in markers_en]
    assert positions_cn == sorted(positions_cn)
    assert positions_en == sorted(positions_en)
