#!/usr/bin/env python3
"""Create labeled contact sheets from the visual reference library."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. Install with: pip install Pillow") from exc


class ContactSheetError(Exception):
    """Raised when contact sheet generation fails."""


def load_catalog(path: Path) -> Dict[str, Any]:
    """Load catalog JSON.

    Args:
        path: catalog.json path.

    Returns:
        Parsed catalog.

    Raises:
        ContactSheetError: On read/parse failure.
    """
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContactSheetError(f"cannot read catalog: {exc}") from exc


def filter_items(
    items: Sequence[Dict[str, Any]],
    *,
    category: Optional[str] = None,
    ids: Optional[Sequence[str]] = None,
) -> List[Dict[str, Any]]:
    """Filter catalog items.

    Args:
        items: Catalog items.
        category: Optional category name.
        ids: Optional explicit ids.

    Returns:
        Filtered item list.
    """
    result = []
    id_set = set(ids) if ids else None
    for item in items:
        if item.get("missing"):
            continue
        if category and item.get("category") != category:
            continue
        if id_set is not None and item.get("id") not in id_set:
            continue
        result.append(item)
    return result


def _load_thumb(path: Path, box: Tuple[int, int]) -> Image.Image:
    """Load and fit an image into a thumbnail box.

    Args:
        path: Image path.
        box: (width, height) thumbnail box.

    Returns:
        RGB thumbnail image.

    Raises:
        ContactSheetError: If image cannot be opened.
    """
    try:
        with Image.open(path) as img:
            thumb = img.convert("RGB")
            thumb.thumbnail(box, Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", box, (245, 245, 245))
            offset = ((box[0] - thumb.width) // 2, (box[1] - thumb.height) // 2)
            canvas.paste(thumb, offset)
            return canvas
    except OSError as exc:
        raise ContactSheetError(f"cannot open {path}: {exc}") from exc


def create_sheets(
    library: Path,
    items: Sequence[Dict[str, Any]],
    output_dir: Path,
    *,
    thumb_size: int = 240,
    columns: int = 4,
    max_per_sheet: int = 12,
    label_height: int = 36,
    padding: int = 16,
) -> List[Path]:
    """Render one or more contact sheet PNGs.

    Args:
        library: Library root (for resolving relative paths).
        items: Filtered catalog items.
        output_dir: Output directory for sheet PNGs.
        thumb_size: Thumbnail max edge.
        columns: Grid columns.
        max_per_sheet: Max images per sheet.
        label_height: Label band height under each thumb.
        padding: Outer/inner padding.

    Returns:
        List of written PNG paths.

    Raises:
        ContactSheetError: On render failure.
    """
    if not items:
        raise ContactSheetError("no items to render")
    output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    written: List[Path] = []
    sheets = [
        items[i : i + max_per_sheet]
        for i in range(0, len(items), max_per_sheet)
    ]
    cell_w = thumb_size
    cell_h = thumb_size + label_height
    for sheet_index, chunk in enumerate(sheets, start=1):
        rows = math.ceil(len(chunk) / columns)
        width = padding * 2 + columns * cell_w + (columns - 1) * padding
        height = padding * 2 + rows * cell_h + (rows - 1) * padding
        sheet = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(sheet)
        for idx, item in enumerate(chunk):
            r, c = divmod(idx, columns)
            x = padding + c * (cell_w + padding)
            y = padding + r * (cell_h + padding)
            img_path = library / str(item["path"])
            try:
                thumb = _load_thumb(img_path, (thumb_size, thumb_size))
            except ContactSheetError as exc:
                print(f"WARN: {exc}", file=sys.stderr)
                thumb = Image.new("RGB", (thumb_size, thumb_size), (220, 220, 220))
            sheet.paste(thumb, (x, y))
            label = f"{item.get('id', '?')}  {item.get('filename', '')}"
            draw.text((x + 4, y + thumb_size + 8), label[:48], fill=(30, 30, 30), font=font)
        out = output_dir / f"contact-sheet-{sheet_index:02d}.png"
        try:
            sheet.save(out, format="PNG")
        except OSError as exc:
            raise ContactSheetError(f"failed to save {out}: {exc}") from exc
        written.append(out)
    return written


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional argv for tests.

    Returns:
        Parsed namespace.
    """
    parser = argparse.ArgumentParser(
        description="Create contact sheets for yihang-idea-to-visual reference images."
    )
    default_lib = Path(__file__).resolve().parents[1] / "assets" / "visual-reference-library"
    parser.add_argument("--library", type=Path, default=default_lib)
    parser.add_argument("--catalog", type=Path, default=None)
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    parser.add_argument("--category", type=str, default=None)
    parser.add_argument("--ids", type=str, nargs="*", default=None)
    parser.add_argument("--max-per-sheet", type=int, default=12)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--thumb-size", type=int, default=240)
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry.

    Args:
        argv: Optional argv.

    Returns:
        Exit code.
    """
    args = parse_args(argv)
    catalog_path = args.catalog or (args.library / "catalog.json")
    try:
        catalog = load_catalog(catalog_path)
        items = filter_items(catalog.get("items", []), category=args.category, ids=args.ids)
        paths = create_sheets(
            args.library,
            items,
            args.output,
            thumb_size=args.thumb_size,
            columns=args.columns,
            max_per_sheet=args.max_per_sheet,
        )
    except ContactSheetError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
