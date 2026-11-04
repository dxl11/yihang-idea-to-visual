#!/usr/bin/env python3
"""Package validated project PNGs into ordered files and a ZIP archive."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


class PackageError(Exception):
    """Raised when packaging fails."""


def load_json(path: Path) -> Any:
    """Load JSON file.

    Args:
        path: JSON path.

    Returns:
        Parsed object.

    Raises:
        PackageError: On failure.
    """
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PackageError(f"cannot read {path}: {exc}") from exc


def resolve_page_image(project_dir: Path, output_file: str) -> Path:
    """Resolve a page image path from manifest output_file.

    Args:
        project_dir: Project root.
        output_file: Relative or basename path from manifest.

    Returns:
        Existing image path.

    Raises:
        PackageError: If the file cannot be found.
    """
    candidates = [
        project_dir / output_file,
        project_dir / "output" / Path(output_file).name,
        project_dir / "output" / "pages" / Path(output_file).name,
        project_dir / "output" / "cover" / Path(output_file).name,
        project_dir / "export" / Path(output_file).name,
    ]
    for path in candidates:
        if path.is_file():
            return path
    raise PackageError(f"missing PNG for {output_file}; looked in {[str(c) for c in candidates]}")


def collect_ordered_pages(manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return pages sorted by index.

    Args:
        manifest: page-manifest dictionary.

    Returns:
        Sorted page dicts.

    Raises:
        PackageError: If pages missing.
    """
    pages: Sequence[Dict[str, Any]] = manifest.get("pages") or []
    if not pages:
        raise PackageError("page-manifest has no pages")
    return sorted(pages, key=lambda p: int(p.get("index", 0)))


def package_project(
    project_dir: Path,
    *,
    export_name: Optional[str] = None,
    require_cover: bool = True,
) -> Dict[str, Any]:
    """Copy ordered PNGs and build ZIP + manifest.

    Args:
        project_dir: Project directory.
        export_name: Folder/zip basename (defaults to project folder name).
        require_cover: Require a cover role page.

    Returns:
        Result dictionary with paths.

    Raises:
        PackageError: On missing files or ZIP failure.
    """
    manifest_path = project_dir / "pages" / "page-manifest.json"
    if not manifest_path.exists():
        raise PackageError("pages/page-manifest.json missing")
    manifest = load_json(manifest_path)
    pages = collect_ordered_pages(manifest)

    if require_cover and not any(p.get("role") == "cover" for p in pages):
        raise PackageError("cover page missing from manifest")

    name = export_name or project_dir.name
    export_dir = project_dir / "export"
    staging = export_dir / name
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)

    written: List[str] = []
    body_i = 1
    for page in pages:
        src = resolve_page_image(project_dir, str(page["output_file"]))
        role = page.get("role")
        if role == "cover":
            dest_name = "00-cover.png"
        else:
            dest_name = f"{body_i:02d}-page.png"
            body_i += 1
        dest = staging / dest_name
        try:
            shutil.copy2(src, dest)
        except OSError as exc:
            raise PackageError(f"copy failed {src} -> {dest}: {exc}") from exc
        written.append(dest_name)

    zip_path = export_dir / "final-export.zip"
    try:
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for filename in written:
                zf.write(staging / filename, arcname=f"{name}/{filename}")
    except OSError as exc:
        raise PackageError(f"zip create failed: {exc}") from exc

    # Integrity test: reopen and list
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            bad = zf.testzip()
            names = zf.namelist()
            if bad is not None:
                raise PackageError(f"zip corruption detected at {bad}")
    except zipfile.BadZipFile as exc:
        raise PackageError(f"zip is not readable: {exc}") from exc

    checklist = {
        "project": str(project_dir),
        "export_dir": str(staging),
        "zip": str(zip_path),
        "files": written,
        "zip_entries": names,
        "skill_id": "yihang-idea-to-visual",
    }
    checklist_path = export_dir / "export-manifest.json"
    try:
        checklist_path.write_text(
            json.dumps(checklist, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise PackageError(f"cannot write export manifest: {exc}") from exc

    return checklist


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional argv.

    Returns:
        Namespace.
    """
    parser = argparse.ArgumentParser(
        description="Package yihang-idea-to-visual PNGs into ordered export + ZIP."
    )
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--name", type=str, default=None, help="Export folder name")
    parser.add_argument(
        "--allow-missing-cover",
        action="store_true",
        help="Do not require a cover role page",
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
    try:
        result = package_project(
            args.project,
            export_name=args.name,
            require_cover=not args.allow_missing_cover,
        )
    except PackageError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
