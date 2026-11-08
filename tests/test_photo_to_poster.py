"""Photo-to-Poster module: prompts, catalog, compose/validate/export."""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "yihang-idea-to-visual"
PTP = SKILL / "assets" / "photo-to-poster"
SCRIPTS = SKILL / "scripts" / "photo_to_poster"

STYLE_FILES = [
    "01-minimal-abstract.md",
    "02-linocut-travel.md",
    "03-raster-distortion.md",
    "04-swiss-editorial.md",
    "05-cyanotype-blueprint.md",
    "06-risograph-print.md",
    "07-topographic-lines.md",
    "08-paper-cut-relief.md",
    "09-naturalist-specimen.md",
    "10-technical-line-art.md",
    "11-ink-wash.md",
    "12-photogravure.md",
]


def _make_photo(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    img = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(img)
    draw.rectangle((size[0] // 4, size[1] // 4, size[0] * 3 // 4, size[1] * 3 // 4), fill=(255, 255, 255))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")


def test_prompt_catalog_and_recipes_complete():
    catalog = json.loads((PTP / "prompt-catalog.json").read_text(encoding="utf-8"))
    assert catalog["module"] == "photo-to-poster"
    assert catalog["canvas"]["width"] == 1080
    assert catalog["canvas"]["height"] == 1440
    assert catalog["rules"]["one_photo_one_poster"] is True
    assert (PTP / "prompts" / "base-prompt.md").is_file()
    assert len(catalog["styles"]) == 12
    for style in catalog["styles"]:
        rel = style["prompt_path"]
        path = PTP / rel
        assert path.is_file(), rel
        text = path.read_text(encoding="utf-8")
        assert "详细生成 Prompt" in text or "```text" in text
        assert abs(style["ratio_top"] + style["ratio_bottom"] - 1.0) < 1e-6
    for name in STYLE_FILES:
        assert (PTP / "prompts" / name).is_file()


def test_skill_wires_photo_to_poster():
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "Photo-to-Poster" in skill
    assert "references/photo-to-poster.md" in skill
    assert "one photo" in skill.lower() or "一张" in skill or "one_photo" in skill
    assert (SKILL / "references" / "photo-to-poster.md").is_file()


def test_inspect_compose_validate_export_independent_posters(tmp_path: Path):
    photo_a = tmp_path / "a.png"
    photo_b = tmp_path / "b.png"
    art_a = tmp_path / "art-a.png"
    art_b = tmp_path / "art-b.png"
    _make_photo(photo_a, (900, 1200), (180, 90, 60))
    _make_photo(photo_b, (1600, 900), (40, 80, 140))
    _make_photo(art_a, (1080, 720), (240, 230, 210))
    _make_photo(art_b, (1080, 720), (30, 60, 90))

    # inspect A
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "inspect_photo.py"),
            "--input",
            str(photo_a),
            "--photo-id",
            "photo-001",
            "--output",
            str(tmp_path / "inspect-a.json"),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    inspect = json.loads((tmp_path / "inspect-a.json").read_text(encoding="utf-8"))
    assert inspect["width"] == 900
    assert inspect["rules"]["one_photo_one_poster"] is True

    posters_dir = tmp_path / "posters"
    out_a = posters_dir / "photo-001-poster.png"
    out_b = posters_dir / "photo-002-poster.png"

    for photo, art, out, ratio in [
        (photo_a, art_a, out_a, "0.5"),
        (photo_b, art_b, out_b, "0.45"),
    ]:
        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "compose_poster.py"),
                "--photo",
                str(photo),
                "--art",
                str(art),
                "--output",
                str(out),
                "--ratio-top",
                ratio,
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr
        assert out.is_file()

    # two independent files, not one collage
    assert out_a.is_file() and out_b.is_file()
    with Image.open(out_a) as img:
        assert img.size == (1080, 1440)
    with Image.open(out_b) as img:
        assert img.size == (1080, 1440)

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate_poster.py"),
            str(out_a),
            str(out_b),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    report = json.loads(proc.stdout)
    assert report["ok"] is True
    assert report["count"] == 2

    zip_path = tmp_path / "final-export.zip"
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "export_posters.py"),
            "--posters-dir",
            str(posters_dir),
            "--zip",
            str(zip_path),
            "--project-name",
            "batch-demo",
            "--style-id",
            "01-minimal-abstract",
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert zip_path.is_file()
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = set(zf.namelist())
        assert "manifest.json" in names
        assert "photo-001-poster.png" in names
        assert "photo-002-poster.png" in names
        assert zf.testzip() is None

    # regenerating A must not delete B
    art_a2 = tmp_path / "art-a2.png"
    _make_photo(art_a2, (1080, 720), (200, 200, 180))
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "compose_poster.py"),
            "--photo",
            str(photo_a),
            "--art",
            str(art_a2),
            "--output",
            str(out_a),
            "--ratio-top",
            "0.5",
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert out_b.is_file()


def test_readmes_mention_photo_to_poster():
    cn = (ROOT / "README.md").read_text(encoding="utf-8")
    en = (ROOT / "README.en.md").read_text(encoding="utf-8")
    assert "Photo-to-Poster" in cn
    assert "Photo-to-Poster" in en
    assert "1080" in cn and "1440" in cn
