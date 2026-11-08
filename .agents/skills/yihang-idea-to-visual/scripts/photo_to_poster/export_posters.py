#!/usr/bin/env python3
"""Package Photo-to-Poster outputs into a ZIP with manifest.

Never merges multiple posters into one image. Each PNG stays independent.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


class ExportError(Exception):
    """Raised when export packaging fails."""


def _utc_now() -> str:
    """Return UTC ISO timestamp.

    Returns:
        ISO-8601 string with Z.
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_manifest(
    project_name: str,
    posters: Sequence[Path],
    *,
    style_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build export manifest.

    Args:
        project_name: Project folder name.
        posters: Ordered poster paths.
        style_id: Optional default style id.
        extra: Optional extra fields.

    Returns:
        Manifest dictionary.
    """
    entries = []
    for idx, path in enumerate(posters, start=1):
        entries.append(
            {
                "index": idx,
                "filename": path.name,
                "path": str(path),
                "independent": True,
            }
        )
    manifest: Dict[str, Any] = {
        "module": "photo-to-poster",
        "skill_id": "yihang-idea-to-visual",
        "project_name": project_name,
        "created_at": _utc_now(),
        "canvas": {"width": 1080, "height": 1440, "aspect": "3:4"},
        "rules": {
            "one_photo_one_poster": True,
            "forbid_collage": True,
            "posters_not_merged": True,
        },
        "default_style_id": style_id,
        "posters": entries,
        "count": len(entries),
    }
    if extra:
        manifest["extra"] = extra
    return manifest


def export_zip(
    posters_dir: Path,
    zip_path: Path,
    *,
    project_name: str,
    style_id: Optional[str] = None,
    pattern: str = "*.png",
) -> Path:
    """Write manifest.json and final-export.zip for a project.

    Args:
        posters_dir: Directory containing independent poster PNGs.
        zip_path: Destination ZIP path.
        project_name: Project name for manifest.
        style_id: Optional style id.
        pattern: Glob for poster files.

    Returns:
        ZIP path.

    Raises:
        ExportError: On missing files or I/O errors.
    """
    if not posters_dir.is_dir():
        raise ExportError(f"posters dir not found: {posters_dir}")
    posters = sorted(posters_dir.glob(pattern))
    if not posters:
        raise ExportError(f"no posters matching {pattern} in {posters_dir}")

    manifest = build_manifest(project_name, posters, style_id=style_id)
    manifest_path = posters_dir.parent / "manifest.json"
    try:
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise ExportError(f"cannot write manifest: {exc}") from exc

    try:
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(manifest_path, arcname="manifest.json")
            for poster in posters:
                zf.write(poster, arcname=poster.name)
            # Quick integrity: reopen later by caller via validate
    except OSError as exc:
        raise ExportError(f"cannot write zip: {exc}") from exc

    # Verify zip opens
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            bad = zf.testzip()
            if bad is not None:
                raise ExportError(f"zip integrity failed on member: {bad}")
    except zipfile.BadZipFile as exc:
        raise ExportError(f"invalid zip: {exc}") from exc

    return zip_path


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser.

    Returns:
        ArgumentParser.
    """
    parser = argparse.ArgumentParser(description="Export Photo-to-Poster ZIP + manifest")
    parser.add_argument("--posters-dir", type=Path, required=True)
    parser.add_argument("--zip", type=Path, required=True, help="Output ZIP path")
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--style-id", default=None)
    parser.add_argument("--pattern", default="*.png")
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
        path = export_zip(
            args.posters_dir,
            args.zip,
            project_name=args.project_name,
            style_id=args.style_id,
            pattern=args.pattern,
        )
    except ExportError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"zip": str(path), "ok": True}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
