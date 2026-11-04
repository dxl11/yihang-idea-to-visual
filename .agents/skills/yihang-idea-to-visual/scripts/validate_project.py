#!/usr/bin/env python3
"""Validate an Idea to Visual project before final export.

Performs file existence, image dimension, page order, overflow flag, and
exact article text integrity checks (fragment concatenation, not mere counts).
"""

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

try:
    from text_integrity import normalize_article_text, verify_article_integrity
except ImportError:  # pragma: no cover
    from scripts.text_integrity import (  # type: ignore
        normalize_article_text,
        verify_article_integrity,
    )


class ValidationError(Exception):
    """Raised for unexpected validator failures."""


def load_json(path: Path) -> Any:
    """Load JSON with unified error wrapping.

    Args:
        path: JSON file path.

    Returns:
        Parsed object.

    Raises:
        ValidationError: On I/O or JSON errors.
    """
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read JSON {path}: {exc}") from exc


def read_text(path: Path) -> str:
    """Read UTF-8 text.

    Args:
        path: Text file path.

    Returns:
        File contents.

    Raises:
        ValidationError: On I/O errors.
    """
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValidationError(f"cannot read text {path}: {exc}") from exc


def check_image(path: Path, expected_size: Optional[tuple[int, int]] = None) -> List[str]:
    """Validate that an image opens and optionally matches size.

    Args:
        path: PNG path.
        expected_size: Optional (width, height).

    Returns:
        List of error strings (empty if ok).
    """
    errors: List[str] = []
    if not path.exists():
        return [f"missing image: {path}"]
    try:
        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            size = img.size
            if expected_size and size != expected_size:
                errors.append(
                    f"size mismatch {path.name}: got {size}, expected {expected_size}"
                )
    except OSError as exc:
        errors.append(f"unreadable image {path}: {exc}")
    return errors


def validate_project(project_dir: Path) -> Dict[str, Any]:
    """Run full project validation.

    Args:
        project_dir: Project root containing state.json / content / pages / output.

    Returns:
        Report dictionary with ``ok``, ``errors``, ``warnings``.

    Raises:
        ValidationError: If critical project files cannot be parsed.
    """
    errors: List[str] = []
    warnings: List[str] = []

    state_path = project_dir / "state.json"
    if not state_path.exists():
        errors.append("state.json missing")
        return {"ok": False, "errors": errors, "warnings": warnings}

    state = load_json(state_path)
    if state.get("skill_id") != "yihang-idea-to-visual":
        errors.append(
            f"skill_id must be yihang-idea-to-visual, got {state.get('skill_id')!r}"
        )

    article_path = project_dir / "content" / "final-article.md"
    if not article_path.exists():
        errors.append("content/final-article.md missing")
        article_text = ""
    else:
        article_text = read_text(article_path)

    manifest_path = project_dir / "pages" / "page-manifest.json"
    if not manifest_path.exists():
        errors.append("pages/page-manifest.json missing")
        return {"ok": False, "errors": errors, "warnings": warnings}

    manifest = load_json(manifest_path)
    pages: Sequence[Dict[str, Any]] = manifest.get("pages") or []
    if not pages:
        errors.append("page-manifest pages[] is empty")

    canvas = state.get("canvas") or manifest.get("canvas") or {}
    expected_size = None
    if canvas.get("width") and canvas.get("height"):
        expected_size = (int(canvas["width"]), int(canvas["height"]))

    # Order + continuity
    indices = [int(p.get("index", -1)) for p in pages]
    if indices != sorted(indices):
        errors.append("page indices are not sorted")
    if indices and indices != list(range(indices[0], indices[0] + len(indices))):
        errors.append(f"page indices not contiguous: {indices}")

    body_fragments: List[str] = []
    body_numbers: List[int] = []
    for page in pages:
        role = page.get("role")
        out_name = page.get("output_file")
        if not out_name:
            errors.append(f"page index={page.get('index')} missing output_file")
            continue
        out_path = project_dir / out_name
        if not out_path.is_file():
            # Also accept under output/
            alt = project_dir / "output" / Path(out_name).name
            out_path = alt if alt.is_file() else out_path
        errors.extend(check_image(out_path, expected_size))

        for flag in page.get("overflow_flags") or []:
            errors.append(f"overflow on page {page.get('index')}: {flag}")

        if role == "body":
            frags = page.get("text_fragments") or []
            if not isinstance(frags, list):
                errors.append(f"page {page.get('index')} text_fragments must be a list")
            else:
                body_fragments.extend(str(f) for f in frags)
            if page.get("page_number") is not None:
                body_numbers.append(int(page["page_number"]))

    if body_numbers and body_numbers != list(range(1, len(body_numbers) + 1)):
        errors.append(f"body page_number not continuous from 1: {body_numbers}")

    if article_text:
        ok, message = verify_article_integrity(article_text, body_fragments)
        if not ok:
            errors.append(message)
            # Extra hint: show normalized lengths only
            warnings.append(
                "integrity uses normalize_article_text (rstrip per line, strip trailing empty lines); "
                "fragments must concatenate to the locked article without summarization"
            )
        else:
            warnings.append(message)

    # Aspect consistency among existing images
    sizes = []
    for page in pages:
        out_name = page.get("output_file")
        if not out_name:
            continue
        out_path = project_dir / out_name
        if not out_path.is_file():
            alt = project_dir / "output" / Path(out_name).name
            out_path = alt if alt.is_file() else out_path
        if out_path.is_file():
            try:
                with Image.open(out_path) as img:
                    sizes.append(img.size)
            except OSError:
                continue
    if sizes and len(set(sizes)) > 1:
        errors.append(f"inconsistent image sizes across pages: {sorted(set(sizes))}")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "article_normalized_len": len(normalize_article_text(article_text)) if article_text else 0,
        "fragment_count": len(body_fragments),
        "page_count": len(pages),
    }


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional argv.

    Returns:
        Namespace.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Validate yihang-idea-to-visual project outputs. "
            "Article integrity compares concatenated page text_fragments to "
            "content/final-article.md after normalize_article_text()."
        )
    )
    parser.add_argument("--project", type=Path, required=True, help="Project directory")
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry.

    Args:
        argv: Optional argv.

    Returns:
        0 if ok, 1 if validation failed, 2 on unexpected error.
    """
    args = parse_args(argv)
    try:
        report = validate_project(args.project)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if report["ok"]:
            print("VALIDATION OK")
        else:
            print("VALIDATION FAILED")
            for err in report["errors"]:
                print(f" - {err}")
        for warn in report.get("warnings") or []:
            print(f"warning: {warn}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
