#!/usr/bin/env python3
"""Render page design JSON documents to PNG for yihang-idea-to-visual.

Separates typography/layout (this script) from generative imagery (host tools).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. Install with: pip install Pillow") from exc


class RenderError(Exception):
    """Raised when page rendering fails."""


# Built-in structural templates (not mere recolors).
TEMPLATES: Dict[str, Dict[str, Any]] = {
    "editorial-minimal": {
        "margin_ratio": 0.10,
        "title_y_ratio": 0.12,
        "body_y_ratio": 0.28,
        "accent": "top-rule",
        "image_slot": "none",
    },
    "modern-technology": {
        "margin_ratio": 0.08,
        "title_y_ratio": 0.10,
        "body_y_ratio": 0.42,
        "accent": "side-bar",
        "image_slot": "top",
    },
    "artistic-journal": {
        "margin_ratio": 0.12,
        "title_y_ratio": 0.18,
        "body_y_ratio": 0.34,
        "accent": "corner-mark",
        "image_slot": "bottom",
    },
}


def parse_color(value: str) -> Tuple[int, int, int]:
    """Parse ``#RRGGBB`` or ``rgb(r,g,b)`` into an RGB tuple.

    Args:
        value: Color string.

    Returns:
        (r, g, b) tuple.

    Raises:
        RenderError: If the color format is invalid.
    """
    raw = value.strip()
    if raw.startswith("#") and len(raw) == 7:
        try:
            return int(raw[1:3], 16), int(raw[3:5], 16), int(raw[5:7], 16)
        except ValueError as exc:
            raise RenderError(f"invalid hex color: {value}") from exc
    if raw.startswith("rgb(") and raw.endswith(")"):
        parts = raw[4:-1].split(",")
        if len(parts) != 3:
            raise RenderError(f"invalid rgb color: {value}")
        try:
            return tuple(int(p.strip()) for p in parts)  # type: ignore[return-value]
        except ValueError as exc:
            raise RenderError(f"invalid rgb color: {value}") from exc
    raise RenderError(f"unsupported color: {value}")


def resolve_font(
    font_path: Optional[str],
    size: int,
    fallbacks: Sequence[str] | None = None,
    *,
    use_system_fallbacks: bool = True,
) -> ImageFont.ImageFont:
    """Load a TrueType font with fallbacks.

    Args:
        font_path: Preferred font file path.
        size: Font size in pixels.
        fallbacks: Additional font paths to try.
        use_system_fallbacks: When True, also try common OS CJK font locations.

    Returns:
        Loaded font.

    Raises:
        RenderError: If no usable font is found (especially critical for CJK).
    """
    candidates: List[str] = []
    if font_path:
        candidates.append(font_path)
    if fallbacks:
        candidates.extend(fallbacks)
    # Common system locations (best-effort; never silently invent glyphs).
    if use_system_fallbacks:
        candidates.extend(
            [
                r"C:\Windows\Fonts\msyh.ttc",
                r"C:\Windows\Fonts\simhei.ttf",
                r"C:\Windows\Fonts\simsun.ttc",
                "/System/Library/Fonts/PingFang.ttc",
                "/Library/Fonts/Arial Unicode.ttf",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            ]
        )
    errors: List[str] = []
    for candidate in candidates:
        path = Path(candidate)
        if not path.exists():
            continue
        try:
            return ImageFont.truetype(str(path), size=size)
        except OSError as exc:
            errors.append(f"{path}: {exc}")
            continue
    raise RenderError(
        "CJK/text font missing. Configure typography.cjk_font_path to a licensed "
        f"installed font. Tried {len(candidates)} candidates. Details: {errors[:3]}"
    )


def wrap_text(
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
    draw: ImageDraw.ImageDraw,
) -> List[str]:
    """Wrap text to fit max width (character-aware for CJK).

    Args:
        text: Source text (may include newlines).
        font: Font used for measurement.
        max_width: Maximum line width in pixels.
        draw: ImageDraw used for textbbox.

    Returns:
        List of wrapped lines.
    """
    lines: List[str] = []
    for paragraph in text.split("\n"):
        if paragraph == "":
            lines.append("")
            continue
        current = ""
        for ch in paragraph:
            trial = current + ch
            bbox = draw.textbbox((0, 0), trial, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = ch
        lines.append(current)
    return lines


def check_overflow(lines: Sequence[str], line_height: int, top: int, bottom_limit: int) -> List[str]:
    """Detect vertical text overflow.

    Args:
        lines: Wrapped lines.
        line_height: Pixel line height.
        top: Top y of first line.
        bottom_limit: Maximum allowed bottom y.

    Returns:
        List of overflow flag strings (empty if none).
    """
    flags: List[str] = []
    bottom = top + len(lines) * line_height
    if bottom > bottom_limit:
        flags.append(f"text_overflow: bottom={bottom} limit={bottom_limit}")
    return flags


def apply_template_chrome(
    draw: ImageDraw.ImageDraw,
    canvas: Tuple[int, int],
    template_id: str,
    primary: Tuple[int, int, int],
    margin: int,
) -> None:
    """Draw structural accents that differentiate templates.

    Args:
        draw: Draw context.
        canvas: (width, height).
        template_id: Template key.
        primary: Primary RGB color.
        margin: Margin in pixels.
    """
    width, height = canvas
    spec = TEMPLATES.get(template_id, TEMPLATES["editorial-minimal"])
    accent = spec["accent"]
    if accent == "top-rule":
        draw.rectangle([margin, margin, width - margin, margin + 4], fill=primary)
    elif accent == "side-bar":
        draw.rectangle([0, 0, int(width * 0.035), height], fill=primary)
        draw.rectangle(
            [margin, int(height * 0.08), width - margin, int(height * 0.08) + 2],
            fill=primary,
        )
    elif accent == "corner-mark":
        mark = int(min(width, height) * 0.06)
        draw.polygon(
            [(width - margin, margin), (width - margin - mark, margin), (width - margin, margin + mark)],
            fill=primary,
        )


def render_page(design: Dict[str, Any], output: Path, *, base_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Render a single page design JSON to PNG.

    Args:
        design: Page design dictionary.
        output: Output PNG path.
        base_dir: Base directory for resolving relative asset paths.

    Returns:
        Result dict with ``output`` and ``overflow_flags``.

    Raises:
        RenderError: On validation or render failure.
    """
    try:
        width = int(design["canvas"]["width"])
        height = int(design["canvas"]["height"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RenderError("design.canvas.width/height required") from exc
    if width <= 0 or height <= 0:
        raise RenderError("canvas dimensions must be positive")

    colors = design.get("colors", {})
    background = parse_color(colors.get("background", "#FFFFFF"))
    text_color = parse_color(colors.get("text", "#111111"))
    primary = parse_color(colors.get("primary", "#1F4B99"))

    image = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(image)

    template_id = design.get("template_id", "editorial-minimal")
    margin = int(design.get("layout", {}).get("margin", int(min(width, height) * 0.1)))
    apply_template_chrome(draw, (width, height), template_id, primary, margin)

    # Background / embedded images
    base = base_dir or Path.cwd()
    for asset in design.get("images", []) or []:
        rel = asset.get("path")
        if not rel:
            continue
        path = Path(rel)
        if not path.is_absolute():
            path = base / path
        if not path.exists():
            raise RenderError(f"image missing: {path}")
        try:
            with Image.open(path) as src:
                placed = src.convert("RGBA")
                box = asset.get("box", [margin, margin, width - 2 * margin, int(height * 0.28)])
                x, y, w, h = [int(v) for v in box]
                placed = placed.resize((w, h), Image.Resampling.LANCZOS)
                image.paste(placed, (x, y), placed if placed.mode == "RGBA" else None)
        except OSError as exc:
            raise RenderError(f"failed to load image {path}: {exc}") from exc

    for shape in design.get("shapes", []) or []:
        kind = shape.get("type")
        fill = parse_color(shape.get("fill", colors.get("secondary", "#CCCCCC")))
        box = [int(v) for v in shape.get("box", [0, 0, 10, 10])]
        if kind == "rect":
            draw.rectangle(box, fill=fill)
        elif kind == "ellipse":
            draw.ellipse(box, fill=fill)

    typo = design.get("typography", {})
    fallbacks = typo.get("fallback_font_paths") or []
    overflow_flags: List[str] = []

    for block in design.get("text_blocks", []) or []:
        content = block.get("text", "")
        size = int(block.get("size", typo.get("body_size", 36)))
        font = resolve_font(
            block.get("font_path") or typo.get("cjk_font_path"),
            size,
            fallbacks,
        )
        x = int(block.get("x", margin))
        y = int(block.get("y", margin))
        max_width = int(block.get("max_width", width - margin - x))
        line_spacing = float(block.get("line_spacing", typo.get("line_spacing", 1.35)))
        color = parse_color(block.get("color", colors.get("text", "#111111")))
        lines = wrap_text(content, font, max_width, draw)
        ascent, descent = font.getmetrics()
        line_height = int((ascent + descent) * line_spacing)
        bottom_limit = int(block.get("bottom_limit", height - margin))
        overflow_flags.extend(check_overflow(lines, line_height, y, bottom_limit))
        cy = y
        for line in lines:
            draw.text((x, cy), line, font=font, fill=color)
            cy += line_height

    # Page number / signature
    folio = design.get("folio")
    if folio:
        folio_font = resolve_font(typo.get("cjk_font_path"), int(typo.get("caption_size", 22)), fallbacks)
        label = str(folio.get("text", ""))
        bbox = draw.textbbox((0, 0), label, font=folio_font)
        fx = int(folio.get("x", width - margin - (bbox[2] - bbox[0])))
        fy = int(folio.get("y", height - margin - (bbox[3] - bbox[1])))
        draw.text((fx, fy), label, font=folio_font, fill=text_color)

    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        image.save(output, format="PNG")
    except OSError as exc:
        raise RenderError(f"failed to save PNG: {exc}") from exc

    return {"output": str(output), "overflow_flags": overflow_flags, "template_id": template_id}


def load_design(path: Path) -> Dict[str, Any]:
    """Load design JSON from disk.

    Args:
        path: Design JSON path.

    Returns:
        Design dictionary.

    Raises:
        RenderError: On read/parse errors.
    """
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RenderError(f"invalid design JSON: {exc}") from exc


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional argv.

    Returns:
        Namespace.
    """
    parser = argparse.ArgumentParser(
        description="Render yihang-idea-to-visual page design JSON to PNG."
    )
    parser.add_argument("--design", type=Path, default=None, help="Page design JSON")
    parser.add_argument("--output", type=Path, default=None, help="Output PNG path")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=None,
        help="Base directory for relative image paths",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="Print built-in template ids and exit",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry.

    Args:
        argv: Optional argv.

    Returns:
        Exit code.
    """
    args = parse_args(argv)
    if args.list_templates:
        for key in TEMPLATES:
            print(key)
        return 0
    if args.design is None or args.output is None:
        print("ERROR: --design and --output are required unless --list-templates", file=sys.stderr)
        return 1
    try:
        design = load_design(args.design)
        result = render_page(design, args.output, base_dir=args.base_dir or args.design.parent)
    except RenderError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    if result["overflow_flags"]:
        print("OVERFLOW:", "; ".join(result["overflow_flags"]), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
