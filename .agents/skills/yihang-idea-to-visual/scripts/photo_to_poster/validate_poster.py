#!/usr/bin/env python3
"""Validate Photo-to-Poster PNG outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. Install with: pip install Pillow") from exc


class ValidateError(Exception):
    """Raised when validation cannot run."""


def validate_one(
    path: Path,
    *,
    expect_width: int = 1080,
    expect_height: int = 1440,
) -> Dict[str, Any]:
    """Validate a single poster file.

    Args:
        path: PNG path.
        expect_width: Required width.
        expect_height: Required height.

    Returns:
        Result dictionary with ``ok`` bool and ``issues`` list.

    Raises:
        ValidateError: If the file cannot be opened at all for inspection.
    """
    issues: List[str] = []
    if not path.is_file():
        return {"path": str(path), "ok": False, "issues": ["file missing"]}
    try:
        with Image.open(path) as img:
            img.load()
            width, height = img.size
            fmt = img.format
            mode = img.mode
    except OSError as exc:
        raise ValidateError(f"cannot open {path}: {exc}") from exc

    if fmt != "PNG":
        issues.append(f"format is {fmt}, expected PNG")
    if (width, height) != (expect_width, expect_height):
        issues.append(f"size {width}x{height}, expected {expect_width}x{expect_height}")
    if abs((width / height) - (3 / 4)) > 0.01:
        issues.append(f"aspect {width/height:.4f} is not 3:4")
    if mode not in {"RGB", "RGBA"}:
        issues.append(f"unexpected mode {mode}")

    return {
        "path": str(path),
        "ok": not issues,
        "width": width,
        "height": height,
        "format": fmt,
        "mode": mode,
        "issues": issues,
    }


def validate_many(paths: Sequence[Path], **kwargs: Any) -> Dict[str, Any]:
    """Validate multiple posters.

    Args:
        paths: Poster paths.
        **kwargs: Forwarded to ``validate_one``.

    Returns:
        Aggregate report.

    Raises:
        ValidateError: Propagated from ``validate_one``.
    """
    results = [validate_one(p, **kwargs) for p in paths]
    return {
        "ok": all(r["ok"] for r in results),
        "count": len(results),
        "results": results,
    }


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser.

    Returns:
        ArgumentParser.
    """
    parser = argparse.ArgumentParser(description="Validate Photo-to-Poster PNG files")
    parser.add_argument("posters", nargs="+", type=Path, help="Poster PNG paths")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1440)
    parser.add_argument("--json-out", type=Path, default=None)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry.

    Args:
        argv: Optional argv.

    Returns:
        Exit code (0 if all ok).
    """
    args = build_parser().parse_args(argv)
    try:
        report = validate_many(args.posters, expect_width=args.width, expect_height=args.height)
    except ValidateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json_out:
        try:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: cannot write report: {exc}", file=sys.stderr)
            return 1
    print(text, end="")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
