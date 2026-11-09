#!/usr/bin/env python3
"""Retrieve and verify visual-library images for STEP 03 cover design.

Modes:
  - ``empty``: catalog has no assets → no image references (disclose to user).
  - ``matched``: one or more openable files match the query.
  - ``no_match``: catalog has assets but none match / none load → disclose.

Writing a path into a prompt is NOT enough. Callers must pass verified
``absolute_path`` values into the host image tool's native reference-image
input (e.g. Cursor GenerateImage ``reference_image_paths``). This script only
proves files exist and can be opened as images.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. Install with: pip install Pillow") from exc


class RetrieveError(Exception):
    """Raised when cover-reference retrieval cannot run."""


def _utc_now() -> str:
    """Return UTC ISO-8601 timestamp.

    Returns:
        Timestamp with Z suffix.
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_entries(catalog: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return asset entries from ``assets`` or legacy ``items``.

    Args:
        catalog: Catalog dictionary.

    Returns:
        List of asset dicts.

    Raises:
        RetrieveError: If neither field is a list.
    """
    if isinstance(catalog.get("assets"), list):
        return list(catalog["assets"])
    if isinstance(catalog.get("items"), list):
        return list(catalog["items"])
    raise RetrieveError("catalog missing assets/items array")


def load_catalog(path: Path) -> Dict[str, Any]:
    """Load catalog JSON.

    Args:
        path: Path to catalog.json.

    Returns:
        Parsed catalog.

    Raises:
        RetrieveError: On missing or invalid JSON.
    """
    if not path.is_file():
        raise RetrieveError(f"catalog not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RetrieveError(f"invalid catalog: {exc}") from exc


def tokenize_query(text: str) -> Set[str]:
    """Split a free-text query into lowercase tokens.

    Args:
        text: Query string (theme, tags, mood, etc.).

    Returns:
        Token set (length >= 2).
    """
    parts = re.split(r"[\s,;/|、，。；：:\-_\.]+", text.lower())
    return {p for p in parts if len(p) >= 2}


def entry_haystack(entry: Dict[str, Any]) -> str:
    """Build a searchable text blob from catalog metadata.

    Args:
        entry: Asset entry.

    Returns:
        Lowercased concatenated metadata string.
    """
    chunks: List[str] = [
        str(entry.get("id", "")),
        str(entry.get("filename", "")),
        str(entry.get("path", "")),
        str(entry.get("category", "")),
        str(entry.get("style_notes", "")),
        str(entry.get("layout_notes", "")),
        str(entry.get("color_notes", "")),
        str(entry.get("typography_notes", "")),
        str(entry.get("composition_notes", "")),
        str(entry.get("visual_hierarchy", "")),
        str(entry.get("whitespace_notes", "")),
        str(entry.get("graphic_language", "")),
        str(entry.get("notes", "")),
    ]
    for key in ("tags", "best_for", "use_cases"):
        val = entry.get(key) or []
        if isinstance(val, list):
            chunks.extend(str(v) for v in val)
        else:
            chunks.append(str(val))
    return " ".join(chunks).lower()


def score_entry(entry: Dict[str, Any], tokens: Set[str], categories: Set[str]) -> int:
    """Score how well an entry matches query tokens / categories.

    Args:
        entry: Asset entry.
        tokens: Query tokens.
        categories: Preferred category names.

    Returns:
        Integer score (higher is better).
    """
    if entry.get("missing") is True:
        return -1
    score = 0
    cat = str(entry.get("category", "")).lower()
    if categories and cat in categories:
        score += 8
    hay = entry_haystack(entry)
    for tok in tokens:
        if tok in hay:
            score += 2
        # Prefer tag exact-ish hits
        tags = [str(t).lower() for t in (entry.get("tags") or [])]
        if tok in tags:
            score += 3
    return score


def verify_image_load(path: Path) -> Dict[str, Any]:
    """Attempt to open an image file; return load report.

    Args:
        path: Absolute or relative image path.

    Returns:
        Dict with ``ok``, ``width``, ``height``, ``format``, ``error``.

    Raises:
        RetrieveError: Never — failures are returned in the report.
    """
    report: Dict[str, Any] = {
        "ok": False,
        "width": None,
        "height": None,
        "format": None,
        "error": None,
    }
    if not path.is_file():
        report["error"] = "file_not_found"
        return report
    try:
        with Image.open(path) as img:
            img.load()
            report["width"], report["height"] = img.size
            report["format"] = img.format or path.suffix.lstrip(".").upper()
            report["ok"] = True
    except OSError as exc:
        report["error"] = f"cannot_open: {exc}"
    return report


def retrieve_cover_references(
    *,
    library: Path,
    catalog_path: Path,
    query: str = "",
    categories: Optional[Sequence[str]] = None,
    limit: int = 3,
) -> Dict[str, Any]:
    """Retrieve and verify cover reference images.

    Args:
        library: visual-reference-library root.
        catalog_path: catalog.json path.
        query: Free-text theme / tags / mood.
        categories: Optional preferred categories.
        limit: Max matched assets to return.

    Returns:
        Result dictionary with ``mode``, ``references``, ``disclaimer``.

    Raises:
        RetrieveError: On catalog read failures.
    """
    if limit < 1:
        raise RetrieveError("limit must be >= 1")
    catalog = load_catalog(catalog_path)
    entries = normalize_entries(catalog)
    # Count only non-missing catalog rows as "present"
    present = [e for e in entries if e.get("missing") is not True]
    total = int(catalog.get("total_assets") or len(present))

    base: Dict[str, Any] = {
        "module": "cover-reference-retrieval",
        "skill_id": "yihang-idea-to-visual",
        "retrieved_at": _utc_now(),
        "query": query,
        "categories": list(categories or []),
        "catalog_path": str(catalog_path),
        "library_path": str(library),
        "catalog_total_assets": total,
        "references": [],
        "rejected": [],
        "image_reference_used": False,
        "host_tool_hint": {
            "cursor_generate_image": {
                "param": "reference_image_paths",
                "note": (
                    "Pass verified absolute_path list into GenerateImage. "
                    "Path-in-prompt alone is NOT image reference."
                ),
            }
        },
    }

    if total == 0 or not present:
        base["mode"] = "empty"
        base["disclaimer"] = (
            "Visual reference library is empty. Cover generation may continue "
            "with brand rules + cover-design prompts only — WITHOUT image references. "
            "Do not pretend reference images were loaded."
        )
        return base

    tokens = tokenize_query(query)
    cats = {c.lower() for c in (categories or []) if c}
    ranked: List[tuple[int, Dict[str, Any]]] = []
    for entry in present:
        sc = score_entry(entry, tokens, cats)
        if sc < 0:
            continue
        ranked.append((sc, entry))
    ranked.sort(key=lambda pair: (-pair[0], str(pair[1].get("id", ""))))

    # If query provided but all scores are 0, treat as no_match (no suitable hit).
    # If query empty, allow top assets by category preference / id order with score 0.
    if tokens or cats:
        ranked = [p for p in ranked if p[0] > 0]

    if not ranked:
        base["mode"] = "no_match"
        base["disclaimer"] = (
            "Catalog has assets, but none matched the query/categories "
            "(or matching files failed filters). Do not invent matches. "
            "With user consent, fall back to brand rules without claiming image refs."
        )
        return base

    refs: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []
    for sc, entry in ranked:
        if len(refs) >= limit:
            break
        rel = str(entry.get("path", "")).replace("\\", "/")
        if not rel:
            rejected.append(
                {
                    "id": entry.get("id"),
                    "reason": "missing_path_field",
                    "loaded": False,
                }
            )
            continue
        abs_path = (library / rel).resolve()
        load = verify_image_load(abs_path)
        payload = {
            "id": entry.get("id"),
            "relative_path": rel,
            "absolute_path": str(abs_path),
            "category": entry.get("category"),
            "tags": entry.get("tags") or [],
            "best_for": entry.get("best_for") or [],
            "score": sc,
            "license": entry.get("license"),
            "source": entry.get("source"),
            "author": entry.get("author"),
            "metadata": {
                "style_notes": entry.get("style_notes") or "",
                "layout_notes": entry.get("layout_notes") or "",
                "color_notes": entry.get("color_notes") or "",
                "typography_notes": entry.get("typography_notes") or "",
                "composition_notes": entry.get("composition_notes") or "",
                "visual_hierarchy": entry.get("visual_hierarchy") or "",
                "whitespace_notes": entry.get("whitespace_notes") or "",
                "graphic_language": entry.get("graphic_language") or "",
            },
            "load": load,
        }
        if load["ok"]:
            refs.append(payload)
        else:
            payload["loaded"] = False
            rejected.append(payload)

    base["rejected"] = rejected
    base["references"] = refs
    if not refs:
        base["mode"] = "no_match"
        base["disclaimer"] = (
            "Matching catalog rows existed but every candidate failed to load. "
            "Do not claim image references were used."
        )
        base["image_reference_used"] = False
        return base

    base["mode"] = "matched"
    base["image_reference_used"] = False  # set True only after host tool call
    base["disclaimer"] = (
        "Candidates verified openable. Agent MUST pass absolute_path into the "
        "host image tool reference input, then set image_reference_used=true "
        "in the project cover-ref manifest. Catalog text alone is not a reference."
    )
    base["agent_checklist"] = [
        "Read each absolute_path with a pixel-capable tool (or trust this load report).",
        "Analyze design language from pixels + metadata.",
        "Pass absolute paths to GenerateImage reference_image_paths (or equivalent).",
        "Record which REF-ids each cover direction used.",
        "Never claim refs if the tool call omitted reference images.",
    ]
    return base


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser.

    Returns:
        ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        description="Retrieve and verify visual refs for STEP 03 covers"
    )
    parser.add_argument(
        "--library",
        type=Path,
        required=True,
        help="assets/visual-reference-library root",
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=None,
        help="catalog.json (default: <library>/catalog.json)",
    )
    parser.add_argument("--query", default="", help="Theme / tags / mood keywords")
    parser.add_argument(
        "--category",
        action="append",
        default=[],
        help="Preferred category (repeatable)",
    )
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path (e.g. design/cover-ref-manifest.json)",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry.

    Args:
        argv: Optional argv.

    Returns:
        Exit code (0 even for empty/no_match — those are valid branches).
    """
    args = build_parser().parse_args(argv)
    catalog = args.catalog or (args.library / "catalog.json")
    try:
        result = retrieve_cover_references(
            library=args.library,
            catalog_path=catalog,
            query=args.query,
            categories=args.category,
            limit=args.limit,
        )
    except RetrieveError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: cannot write output: {exc}", file=sys.stderr)
            return 1
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
