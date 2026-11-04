#!/usr/bin/env python3
"""Build or incrementally update the Thought Library catalog.

Scans markdown method cards and notes, extracts frontmatter metadata, and
writes/merges catalog.json. Does not invent citations or rewrite card bodies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MARKDOWN_EXTENSIONS = {".md", ".markdown"}
SKIP_DIR_NAMES = {"private"}
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


class ThoughtIndexError(Exception):
    """Raised when thought library indexing fails."""


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
        ThoughtIndexError: If the file cannot be read.
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
        raise ThoughtIndexError(f"failed to hash {path}: {exc}") from exc
    return digest.hexdigest()


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Parse simple YAML-like frontmatter from a markdown file.

    Args:
        text: Full file text.

    Returns:
        Tuple of (metadata dict, body markdown).
    """
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    meta: Dict[str, Any] = {}
    current_list_key: Optional[str] = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if current_list_key and line.lstrip().startswith("- "):
            meta.setdefault(current_list_key, []).append(line.lstrip()[2:].strip())
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            current_list_key = key
            meta[key] = []
            continue
        meta[key] = value
    body = text[match.end() :]
    return meta, body


def load_catalog(path: Path) -> Dict[str, Any]:
    """Load an existing catalog or return an empty structure.

    Args:
        path: catalog.json path.

    Returns:
        Catalog dictionary.

    Raises:
        ThoughtIndexError: If JSON is invalid.
    """
    if not path.exists():
        return {
            "version": "1.0",
            "skill_id": "yihang-idea-to-visual",
            "library": "thought-library",
            "updated_at": None,
            "items": [],
            "stats": {"total": 0},
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ThoughtIndexError(f"invalid catalog JSON at {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ThoughtIndexError("catalog root must be an object")
    data.setdefault("items", [])
    data.setdefault("version", "1.0")
    data.setdefault("skill_id", "yihang-idea-to-visual")
    data.setdefault("library", "thought-library")
    return data


def iter_markdown_files(library: Path, include_private: bool) -> List[Path]:
    """Collect markdown files under the library.

    Args:
        library: Thought library root.
        include_private: Whether to include the private/ folder.

    Returns:
        Sorted list of markdown paths.
    """
    files: List[Path] = []
    for path in library.rglob("*"):
        if not path.is_file():
            continue
        if path.name.lower() in {"readme.md", "catalog.json"}:
            continue
        if path.suffix.lower() not in MARKDOWN_EXTENSIONS:
            continue
        rel_parts = path.relative_to(library).parts
        if not include_private and rel_parts and rel_parts[0] in SKIP_DIR_NAMES:
            continue
        files.append(path)
    return sorted(files)


def next_id(existing_ids: set[str], prefix: str = "TH") -> str:
    """Allocate the next numeric thought id.

    Args:
        existing_ids: Already used ids.
        prefix: Id prefix.

    Returns:
        New id string.
    """
    max_n = 0
    pattern = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
    for item_id in existing_ids:
        match = pattern.match(item_id)
        if match:
            max_n = max(max_n, int(match.group(1)))
    return f"{prefix}-{max_n + 1:04d}"


def build_item(path: Path, library: Path, existing: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Build a catalog item for one markdown card.

    Args:
        path: Markdown file path.
        library: Library root.
        existing: Previous catalog item for the same relative path, if any.

    Returns:
        Catalog item dictionary.

    Raises:
        ThoughtIndexError: On read failure.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ThoughtIndexError(f"failed to read {path}: {exc}") from exc
    meta, body = parse_frontmatter(text)
    rel = path.relative_to(library).as_posix()
    category = meta.get("category") or (path.parent.name if path.parent != library else "miscellaneous")
    item_id = str(meta.get("id") or (existing or {}).get("id") or "")
    summary = ""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith(">"):
            summary = stripped
            break
    tags = meta.get("tags") if isinstance(meta.get("tags"), list) else []
    best_for = meta.get("best_for") if isinstance(meta.get("best_for"), list) else []
    return {
        "id": item_id,
        "filename": path.name,
        "path": rel,
        "title": meta.get("title") or path.stem.replace("-", " ").title(),
        "title_zh": meta.get("title_zh") or "",
        "category": category,
        "tags": tags,
        "best_for": best_for,
        "summary": summary[:240],
        "source": meta.get("source") or "user upload",
        "author": meta.get("author") or "",
        "work_title": meta.get("work_title") or "",
        "section": meta.get("section") or "",
        "page": meta.get("page") or "",
        "license": meta.get("license") or "unknown",
        "attribution": meta.get("attribution") or "",
        "sha256": file_sha256(path),
        "updated_at": _utc_now(),
        "missing": False,
    }


def merge_catalog(
    library: Path,
    output: Path,
    full: bool,
    include_private: bool,
) -> Dict[str, Any]:
    """Scan library and write catalog.json.

    Args:
        library: Thought library directory.
        output: Destination catalog path.
        full: If True, drop missing paths; else mark missing.
        include_private: Include private/ materials.

    Returns:
        Updated catalog dictionary.

    Raises:
        ThoughtIndexError: On I/O or parsing failures.
    """
    if not library.is_dir():
        raise ThoughtIndexError(f"library not found: {library}")

    catalog = load_catalog(output)
    by_path = {
        item["path"]: item
        for item in catalog.get("items", [])
        if isinstance(item, dict) and "path" in item
    }
    used_ids = {str(item.get("id")) for item in by_path.values() if item.get("id")}
    seen_paths: set[str] = set()
    items: List[Dict[str, Any]] = []

    try:
        files = iter_markdown_files(library, include_private=include_private)
    except OSError as exc:
        raise ThoughtIndexError(f"failed to scan library: {exc}") from exc

    for path in files:
        rel = path.relative_to(library).as_posix()
        seen_paths.add(rel)
        previous = by_path.get(rel)
        item = build_item(path, library, previous)
        if not item["id"]:
            item["id"] = next_id(used_ids)
        used_ids.add(str(item["id"]))
        items.append(item)

    if not full:
        for rel, old in by_path.items():
            if rel not in seen_paths:
                stale = dict(old)
                stale["missing"] = True
                stale["updated_at"] = _utc_now()
                items.append(stale)

    items.sort(key=lambda row: str(row.get("id") or row.get("path") or ""))
    catalog["items"] = items
    catalog["updated_at"] = _utc_now()
    catalog["stats"] = {
        "total": len([i for i in items if not i.get("missing")]),
        "missing": len([i for i in items if i.get("missing")]),
        "categories": sorted({str(i.get("category")) for i in items if not i.get("missing")}),
    }

    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise ThoughtIndexError(f"failed to write catalog: {exc}") from exc
    return catalog


def build_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser.

    Returns:
        Configured ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        description="Build or update Thought Library catalog.json"
    )
    parser.add_argument(
        "--library",
        type=Path,
        default=Path("assets/thought-library"),
        help="Thought library root directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="catalog.json path (default: <library>/catalog.json)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Drop entries whose files no longer exist",
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include markdown files under private/",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point.

    Args:
        argv: Optional argument list for tests.

    Returns:
        Process exit code.

    Raises:
        SystemExit: Indirectly via return codes for caller scripts.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    library = args.library.resolve()
    output = (args.output or (args.library / "catalog.json")).resolve()
    try:
        catalog = merge_catalog(
            library=library,
            output=output,
            full=bool(args.full),
            include_private=bool(args.include_private),
        )
    except ThoughtIndexError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(
        f"thought catalog updated: {output} "
        f"(total={catalog['stats']['total']}, missing={catalog['stats']['missing']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
