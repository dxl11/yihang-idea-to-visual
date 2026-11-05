#!/usr/bin/env python3
"""Build or incrementally update the visual reference library catalog.

Scans image files, extracts technical metadata, detects duplicates by hash,
and writes/merges catalog.json. Does not invent visual design analysis.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install with: pip install Pillow"
    ) from exc

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}


class IndexError_(Exception):
    """Raised when reference indexing fails."""


def _utc_now() -> str:
    """Return current UTC timestamp in ISO-8601 form.

    Returns:
        ISO-8601 timestamp string with Z suffix.
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def file_sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute SHA-256 hash of a file.

    Args:
        path: File path.
        chunk_size: Read chunk size in bytes.

    Returns:
        Hex digest string.

    Raises:
        OSError: If the file cannot be read.
        IndexError_: On unexpected I/O failure wrapped for callers.
    """
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(chunk_size)
                if not chunk:
                    break
                digest.update(chunk)
    except OSError as exc:
        raise IndexError_(f"failed to hash {path}: {exc}") from exc
    return digest.hexdigest()


def aspect_ratio_label(width: int, height: int) -> str:
    """Return a simplified aspect ratio label.

    Args:
        width: Image width in pixels.
        height: Image height in pixels.

    Returns:
        Ratio label such as ``4:5`` or ``1:1``.
    """
    if width <= 0 or height <= 0:
        return "unknown"
    g = math.gcd(width, height)
    return f"{width // g}:{height // g}"


DEFAULT_CATEGORIES = [
    "editorial",
    "minimalism",
    "technology",
    "artistic",
    "infographic",
    "typography",
    "cover-design",
    "carousel-layout",
    "photography",
    "color-palettes",
]


def empty_catalog() -> Dict[str, Any]:
    """Return an empty visual reference catalog skeleton.

    Returns:
        Catalog dictionary with zero assets.
    """
    return {
        "version": "1.0",
        "skill_id": "yihang-idea-to-visual",
        "description": "Yihang Idea to Visual built-in visual reference library",
        "total_assets": 0,
        "categories": list(DEFAULT_CATEGORIES),
        "assets": [],
        "items": [],
        "updated_at": None,
        "stats": {"total": 0, "pending_analysis": 0, "duplicates": 0},
    }


def normalize_catalog_entries(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return the asset list from either ``assets`` or legacy ``items``.

    Args:
        data: Catalog dictionary.

    Returns:
        List of asset/item dictionaries.

    Raises:
        IndexError_: If neither field is a list.
    """
    if isinstance(data.get("assets"), list):
        return list(data["assets"])
    if isinstance(data.get("items"), list):
        return list(data["items"])
    raise IndexError_("catalog missing assets/items array")


def load_catalog(path: Path) -> Dict[str, Any]:
    """Load an existing catalog or return an empty structure.

    Args:
        path: catalog.json path.

    Returns:
        Catalog dictionary.

    Raises:
        IndexError_: If JSON is invalid.
    """
    if not path.exists():
        return empty_catalog()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IndexError_(f"invalid catalog at {path}: {exc}") from exc
    entries = normalize_catalog_entries(data)
    data["items"] = entries
    data["assets"] = entries
    data.setdefault("skill_id", "yihang-idea-to-visual")
    data.setdefault(
        "description",
        "Yihang Idea to Visual built-in visual reference library",
    )
    data.setdefault("categories", list(DEFAULT_CATEGORIES))
    data["total_assets"] = len(entries)
    return data


def next_ref_id(items: List[Dict[str, Any]]) -> str:
    """Allocate the next REF-#### identifier.

    Args:
        items: Existing catalog items.

    Returns:
        New identifier string.
    """
    max_n = 0
    for item in items:
        raw = str(item.get("id", ""))
        if raw.startswith("REF-"):
            try:
                max_n = max(max_n, int(raw.split("-", 1)[1]))
            except ValueError:
                continue
    return f"REF-{max_n + 1:04d}"


def probe_image(path: Path) -> Tuple[int, int, str]:
    """Read image dimensions and format.

    Args:
        path: Image file path.

    Returns:
        Tuple of width, height, format name.

    Raises:
        IndexError_: If the image cannot be opened.
    """
    try:
        with Image.open(path) as img:
            width, height = img.size
            fmt = (img.format or path.suffix.lstrip(".")).upper()
            return width, height, fmt
    except OSError as exc:
        raise IndexError_(f"cannot open image {path}: {exc}") from exc


def scan_library(library: Path) -> List[Path]:
    """Collect image files under the library root.

    Args:
        library: Visual reference library directory.

    Returns:
        Sorted list of image paths.
    """
    files: List[Path] = []
    for path in library.rglob("*"):
        if not path.is_file():
            continue
        if path.name.lower() in {"catalog.json", "readme.md"}:
            continue
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            files.append(path)
    return sorted(files)


def build_or_update(
    library: Path,
    output: Path,
    *,
    incremental: bool = True,
) -> Dict[str, Any]:
    """Build or incrementally update the catalog.

    Args:
        library: Library root directory.
        output: Output catalog path.
        incremental: When True, merge with existing entries by relative path.

    Returns:
        Updated catalog dictionary.

    Raises:
        IndexError_: On I/O or validation failures.
        FileNotFoundError: If library does not exist.
    """
    if not library.is_dir():
        raise FileNotFoundError(f"library not found: {library}")

    catalog = (
        load_catalog(output)
        if incremental and output.exists()
        else empty_catalog()
    )
    by_path: Dict[str, Dict[str, Any]] = {
        str(item.get("path")): item for item in catalog["items"] if item.get("path")
    }
    hash_to_ids: Dict[str, List[str]] = {}
    for item in catalog["items"]:
        h = item.get("sha256")
        if h:
            hash_to_ids.setdefault(h, []).append(item["id"])

    files = scan_library(library)
    seen_paths = set()

    for file_path in files:
        rel = file_path.relative_to(library).as_posix()
        seen_paths.add(rel)
        category = rel.split("/", 1)[0] if "/" in rel else "miscellaneous"
        try:
            width, height, fmt = probe_image(file_path)
            digest = file_sha256(file_path)
        except IndexError_ as exc:
            print(f"WARN: {exc}", file=sys.stderr)
            continue

        existing = by_path.get(rel)
        if existing and existing.get("sha256") == digest and incremental:
            existing["width"] = width
            existing["height"] = height
            existing["aspect_ratio"] = aspect_ratio_label(width, height)
            existing["format"] = fmt
            continue

        item = existing or {
            "id": next_ref_id(list(by_path.values()) + catalog["items"]),
            "filename": file_path.name,
            "path": rel,
            "tags": [],
            "style_notes": "",
            "layout_notes": "",
            "color_notes": "",
            "typography_notes": "",
            "composition_notes": "",
            "best_for": [],
            "source": "",
            "author": "",
            "license": "unknown",
            "attribution": "",
            "notes": "",
            "analysis_status": "pending",
        }
        # Ensure unique id when brand-new
        if not existing:
            # Recompute id against current items to avoid collisions
            item["id"] = next_ref_id(list(by_path.values()))
            item["filename"] = file_path.name
            item["path"] = rel

        item.update(
            {
                "width": width,
                "height": height,
                "aspect_ratio": aspect_ratio_label(width, height),
                "format": fmt,
                "category": category,
                "sha256": digest,
                "updated_at": _utc_now(),
            }
        )
        if not item.get("analysis_status"):
            item["analysis_status"] = "pending"
        by_path[rel] = item
        hash_to_ids.setdefault(digest, [])
        if item["id"] not in hash_to_ids[digest]:
            hash_to_ids[digest].append(item["id"])

    # Drop missing files on full rebuild; keep on incremental with flag
    items: List[Dict[str, Any]] = []
    for rel, item in sorted(by_path.items(), key=lambda kv: kv[1].get("id", "")):
        if rel not in seen_paths:
            if incremental:
                item["missing"] = True
                items.append(item)
            continue
        item.pop("missing", None)
        dup_ids = [i for i in hash_to_ids.get(item.get("sha256", ""), []) if i != item["id"]]
        item["duplicate_of"] = dup_ids
        items.append(item)

    catalog["items"] = items
    catalog["assets"] = items
    catalog["total_assets"] = len(items)
    catalog["updated_at"] = _utc_now()
    catalog["skill_id"] = "yihang-idea-to-visual"
    catalog.setdefault(
        "description",
        "Yihang Idea to Visual built-in visual reference library",
    )
    catalog.setdefault("categories", list(DEFAULT_CATEGORIES))
    catalog["stats"] = {
        "total": len(items),
        "pending_analysis": sum(1 for i in items if i.get("analysis_status") == "pending"),
        "duplicates": sum(1 for i in items if i.get("duplicate_of")),
    }
    return catalog


def write_catalog(catalog: Dict[str, Any], output: Path) -> None:
    """Write catalog JSON atomically.

    Args:
        catalog: Catalog dictionary.
        output: Destination path.

    Raises:
        IndexError_: If writing fails.
    """
    entries = normalize_catalog_entries(catalog)
    catalog["items"] = entries
    catalog["assets"] = entries
    catalog["total_assets"] = len(entries)
    catalog.setdefault("categories", list(DEFAULT_CATEGORIES))
    catalog.setdefault(
        "description",
        "Yihang Idea to Visual built-in visual reference library",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    try:
        tmp.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(output)
    except OSError as exc:
        raise IndexError_(f"failed to write catalog: {exc}") from exc


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional argument list for testing.

    Returns:
        Parsed namespace.
    """
    parser = argparse.ArgumentParser(
        description="Build or update visual reference library catalog.json for yihang-idea-to-visual."
    )
    parser.add_argument(
        "--library",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "visual-reference-library",
        help="Path to visual-reference-library root",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output catalog path (default: <library>/catalog.json)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full rebuild (drop missing paths instead of marking them)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point.

    Args:
        argv: Optional argument list.

    Returns:
        Process exit code (0 success, 1 failure).
    """
    args = parse_args(argv)
    output = args.output or (args.library / "catalog.json")
    try:
        catalog = build_or_update(args.library, output, incremental=not args.full)
        write_catalog(catalog, output)
    except (IndexError_, FileNotFoundError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {output} ({catalog['stats']['total']} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
