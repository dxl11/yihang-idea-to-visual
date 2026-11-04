# Visual Reference Library

Directory: [assets/visual-reference-library/](../assets/visual-reference-library/)

## Purpose

Users continuously upload inspiration images (magazine covers, carousels, infographics, type specimens, palettes, illustration, photography, posters). The skill uses them for **analysis and combination**, not for copying.

## Indexing

```bash
python scripts/build_reference_index.py \
  --library assets/visual-reference-library \
  --output assets/visual-reference-library/catalog.json
```

The script extracts technical metadata (path, size, aspect, hash, duplicates) and creates pending analysis fields. It does **not** invent design-language understanding from filenames alone.

Visual analysis (style / layout / color / typography / composition notes) must be performed by an AI that can read image pixels. If the host cannot read images, state the limitation; do not fake analysis.

## Contact sheets

```bash
python scripts/create_contact_sheet.py \
  --library assets/visual-reference-library \
  --catalog assets/visual-reference-library/catalog.json \
  --output contact-sheets \
  --category editorial \
  --max-per-sheet 12
```

## Retrieval

Prefer filter by `category`, `tags`, `best_for`, and existing notes. Do not traverse the entire library every time.

## Combination

Support multi-reference synthesis, e.g.:

- A → structure
- B → color
- C → illustration language

Output must be an original design.

## Copyright

- Do not scrape copyrighted images into the public repo.
- User uploads ≠ redistribution rights.
- `license: unknown` / `private` → internal analysis only.
- Keep private files under ignored `private/` folders.
- Never reproduce protected logos or distinctive protected artwork.

User guide: [assets/visual-reference-library/README.md](../assets/visual-reference-library/README.md)
