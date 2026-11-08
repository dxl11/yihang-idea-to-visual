#!/usr/bin/env python3
"""Inspect a single source photo for Photo-to-Poster jobs.

Extracts technical metadata and a simple dominant-color sample.
Does not invent subject labels; optional notes come from the host agent.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. Install with: pip install Pillow") from exc


class PhotoInspectError(Exception):
    """Raised when photo inspection fails."""


DEFAULT_CANVAS = (1080, 1440)


def _utc_now() -> str:
    """Return UTC ISO-8601 timestamp.

    Returns:
        Timestamp string with Z suffix.
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def dominant_colors(image: Image.Image, max_colors: int = 5) -> List[str]:
    """Sample dominant RGB hex colors from an image.

    Args:
        image: Source PIL image.
        max_colors: Maximum colors to return.

    Returns:
        List of ``#RRGGBB`` strings.

    Raises:
        PhotoInspectError: If sampling fails.
    """
    try:
        small = image.convert("RGB").resize((64, 64))
        counts = Counter(small.getdata())
    except OSError as exc:
        raise PhotoInspectError(f"failed to sample colors: {exc}") from exc
    top = [rgb for rgb, _ in counts.most_common(max_colors)]
    return [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in top]


def fit_strategy(width: int, height: int, canvas: Tuple[int, int], ratio_top: float) -> str:
    """Recommend non-destructive placement strategy for the top band.

    Args:
        width: Source width.
        height: Source height.
        canvas: Target canvas size.
        ratio_top: Top band height ratio (0-1).

    Returns:
        Strategy label: ``cover-center``, ``contain-pad``, or ``unknown``.
    """
    if width <= 0 or height <= 0 or ratio_top <= 0:
        return "unknown"
    band_h = max(1, int(round(canvas[1] * ratio_top)))
    band_aspect = canvas[0] / band_h
    src_aspect = width / height
    if abs(src_aspect - band_aspect) < 0.08:
        return "cover-center"
    if src_aspect > band_aspect:
        return "cover-center"
    return "contain-pad"


def inspect_photo(
    path: Path,
    *,
    photo_id: str = "photo-001",
    ratio_top: float = 0.5,
    canvas: Tuple[int, int] = DEFAULT_CANVAS,
) -> Dict[str, Any]:
    """Inspect one photo and return a JSON-serializable report.

    Args:
        path: Source image path.
        photo_id: Logical id for this photo job.
        ratio_top: Intended top-band ratio for composition planning.
        canvas: Target poster canvas.

    Returns:
        Inspection dictionary.

    Raises:
        PhotoInspectError: On I/O or decode failure.
    """
    if not path.is_file():
        raise PhotoInspectError(f"file not found: {path}")
    try:
        with Image.open(path) as img:
            img.load()
            width, height = img.size
            fmt = (img.format or path.suffix.lstrip(".")).upper()
            mode = img.mode
            colors = dominant_colors(img)
    except OSError as exc:
        raise PhotoInspectError(f"cannot open image {path}: {exc}") from exc

    return {
        "photo_id": photo_id,
        "path": str(path),
        "filename": path.name,
        "width": width,
        "height": height,
        "aspect_ratio": round(width / height, 4) if height else None,
        "format": fmt,
        "mode": mode,
        "dominant_colors": colors,
        "canvas": {"width": canvas[0], "height": canvas[1], "aspect": "3:4"},
        "planned_ratio_top": ratio_top,
        "fit_strategy": fit_strategy(width, height, canvas, ratio_top),
        "rules": {
            "one_photo_one_poster": True,
            "forbid_collage": True,
            "top_uses_source_pixels": True,
        },
        "inspected_at": _utc_now(),
        "notes": "Subject/scene labels must come from host vision analysis; this script only reports technical facts.",
    }


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser.

    Returns:
        ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(description="Inspect one photo for Photo-to-Poster")
    parser.add_argument("--input", type=Path, required=True, help="Source photo path")
    parser.add_argument("--photo-id", default="photo-001")
    parser.add_argument("--ratio-top", type=float, default=0.5)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1440)
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry.

    Args:
        argv: Optional argv list.

    Returns:
        Exit code.
    """
    args = build_parser().parse_args(argv)
    try:
        report = inspect_photo(
            args.input,
            photo_id=args.photo_id,
            ratio_top=args.ratio_top,
            canvas=(args.width, args.height),
        )
    except PhotoInspectError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: cannot write report: {exc}", file=sys.stderr)
            return 1
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
