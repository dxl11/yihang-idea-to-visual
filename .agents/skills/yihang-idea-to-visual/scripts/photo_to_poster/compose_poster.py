#!/usr/bin/env python3
"""Compose a Photo-to-Poster PNG from source photo + generated art panel.

Top band uses the original photo as real pixels (no model redraw).
Bottom band uses a generated art image. Never merges multiple source photos.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. Install with: pip install Pillow") from exc


class ComposeError(Exception):
    """Raised when poster composition fails."""


DEFAULT_SIZE = (1080, 1440)


def load_rgb(path: Path) -> Image.Image:
    """Load an image as RGB.

    Args:
        path: Image path.

    Returns:
        RGB image.

    Raises:
        ComposeError: If the file cannot be opened.
    """
    try:
        with Image.open(path) as img:
            return img.convert("RGB")
    except OSError as exc:
        raise ComposeError(f"cannot open {path}: {exc}") from exc


def place_photo_in_band(
    photo: Image.Image,
    band_size: Tuple[int, int],
    *,
    mode: str = "cover-center",
    pad_color: Tuple[int, int, int] = (245, 241, 234),
    mild_grade: bool = True,
) -> Image.Image:
    """Place a source photo into a band without stretching the subject.

    Args:
        photo: Source RGB image.
        band_size: (width, height) of the top band.
        mode: ``cover-center`` (crop) or ``contain-pad`` (letterbox).
        pad_color: Background for contain mode.
        mild_grade: Apply a very mild contrast tweak only.

    Returns:
        Band-sized RGB image.

    Raises:
        ComposeError: On invalid sizes.
    """
    bw, bh = band_size
    if bw <= 0 or bh <= 0:
        raise ComposeError("invalid band size")
    src = photo
    if mild_grade:
        src = ImageEnhance.Contrast(src).enhance(1.03)
        src = ImageEnhance.Color(src).enhance(1.02)

    sw, sh = src.size
    if mode == "contain-pad":
        scale = min(bw / sw, bh / sh)
        nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
        resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (bw, bh), pad_color)
        canvas.paste(resized, ((bw - nw) // 2, (bh - nh) // 2))
        return canvas

    # cover-center: scale to cover, then center-crop (no stretch)
    scale = max(bw / sw, bh / sh)
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - bw) // 2)
    top = max(0, (nh - bh) // 2)
    return resized.crop((left, top, left + bw, top + bh))


def place_art_in_band(art: Image.Image, band_size: Tuple[int, int]) -> Image.Image:
    """Fit generated art into the bottom band with cover-center crop.

    Args:
        art: Generated art RGB image.
        band_size: (width, height).

    Returns:
        Band-sized RGB image.

    Raises:
        ComposeError: On invalid sizes.
    """
    return place_photo_in_band(art, band_size, mode="cover-center", mild_grade=False)


def optional_caption(
    image: Image.Image,
    text: str,
    *,
    y_ratio: float = 0.92,
) -> Image.Image:
    """Draw a short caption with Pillow (never model gibberish).

    Args:
        image: Poster image.
        text: Caption text.
        y_ratio: Vertical position ratio.

    Returns:
        Image with caption (copy).
    """
    if not text.strip():
        return image
    out = image.copy()
    draw = ImageDraw.Draw(out)
    try:
        font = ImageFont.load_default()
    except OSError:
        font = None
    x = int(out.width * 0.08)
    y = int(out.height * y_ratio)
    draw.text((x, y), text[:80], fill=(40, 40, 40), font=font)
    return out


def compose_poster(
    photo_path: Path,
    art_path: Path,
    output_path: Path,
    *,
    ratio_top: float = 0.5,
    canvas: Tuple[int, int] = DEFAULT_SIZE,
    fit_mode: str = "cover-center",
    caption: str = "",
) -> Path:
    """Compose one independent poster from one photo + one art panel.

    Args:
        photo_path: Original user photo (top band pixels).
        art_path: Generated art for the bottom band.
        output_path: Destination PNG path.
        ratio_top: Top band height ratio.
        canvas: Final canvas size (default 1080x1440).
        fit_mode: Photo placement mode.
        caption: Optional post-process caption.

    Returns:
        Written output path.

    Raises:
        ComposeError: On validation or I/O failures.
    """
    if not 0.2 <= ratio_top <= 0.8:
        raise ComposeError("ratio_top must be between 0.2 and 0.8")
    width, height = canvas
    top_h = int(round(height * ratio_top))
    bottom_h = height - top_h
    if top_h < 1 or bottom_h < 1:
        raise ComposeError("degenerate band heights")

    photo = load_rgb(photo_path)
    art = load_rgb(art_path)
    top = place_photo_in_band(photo, (width, top_h), mode=fit_mode)
    bottom = place_art_in_band(art, (width, bottom_h))

    poster = Image.new("RGB", (width, height), (255, 255, 255))
    poster.paste(top, (0, 0))
    poster.paste(bottom, (0, top_h))
    if caption:
        poster = optional_caption(poster, caption)

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        poster.save(output_path, format="PNG", optimize=True)
    except OSError as exc:
        raise ComposeError(f"failed to save {output_path}: {exc}") from exc
    return output_path


def build_parser() -> argparse.ArgumentParser:
    """Create CLI parser.

    Returns:
        ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        description="Compose one Photo-to-Poster PNG (one photo -> one poster)"
    )
    parser.add_argument("--photo", type=Path, required=True, help="Original photo")
    parser.add_argument("--art", type=Path, required=True, help="Generated art panel/image")
    parser.add_argument("--output", type=Path, required=True, help="Output PNG path")
    parser.add_argument("--ratio-top", type=float, default=0.5)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1440)
    parser.add_argument(
        "--fit",
        choices=["cover-center", "contain-pad"],
        default="cover-center",
    )
    parser.add_argument("--caption", default="", help="Optional Pillow caption")
    parser.add_argument(
        "--manifest-out",
        type=Path,
        default=None,
        help="Optional JSON sidecar describing the composition",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry.

    Args:
        argv: Optional argv.

    Returns:
        Exit code.
    """
    args = build_parser().parse_args(argv)
    try:
        out = compose_poster(
            args.photo,
            args.art,
            args.output,
            ratio_top=args.ratio_top,
            canvas=(args.width, args.height),
            fit_mode=args.fit,
            caption=args.caption,
        )
    except ComposeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    meta = {
        "output": str(out),
        "photo": str(args.photo),
        "art": str(args.art),
        "ratio_top": args.ratio_top,
        "ratio_bottom": round(1.0 - args.ratio_top, 4),
        "canvas": {"width": args.width, "height": args.height, "aspect": "3:4"},
        "fit": args.fit,
        "one_photo_one_poster": True,
    }
    if args.manifest_out:
        try:
            args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
            args.manifest_out.write_text(
                json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"ERROR: cannot write manifest: {exc}", file=sys.stderr)
            return 1
    print(json.dumps(meta, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
