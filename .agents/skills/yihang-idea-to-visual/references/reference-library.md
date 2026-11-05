# Visual Reference Library

Directory: [assets/visual-reference-library/](../assets/visual-reference-library/)

## Purpose

Built-in inspiration library maintained by the skill author. Used for **analysis and trait combination** during cover and editorial design—not for copying final artwork.

The library may be **empty**. An empty `catalog.json` is valid and must not block the creative pipeline.

## Empty-library rule

Before retrieving references in STEP 03 (cover) or STEP 04 (editorial):

1. Read `assets/visual-reference-library/catalog.json`.
2. If `total_assets == 0`, or both `assets` and `items` are empty → **skip library retrieval** and continue the normal three-direction cover / three-style editorial flow.
3. Never invent, hallucinate, or claim reference images that are not in the catalog.
4. When real assets are added later, the same flow can retrieve them without changing stage mechanics.

## Indexing

```bash
python scripts/build_reference_index.py \
  --library assets/visual-reference-library \
  --output assets/visual-reference-library/catalog.json
```

The script extracts technical metadata (path, size, aspect, hash, duplicates) and creates pending analysis fields. It keeps `assets` and `items` in sync and updates `total_assets`. It does **not** invent design-language understanding from filenames alone.

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

With zero assets the script exits successfully and prints that there is nothing to sheet.

## Retrieval

Prefer filter by `category`, `tags`, `best_for`, and existing notes. Do not traverse the entire library every time.

## Combination

Support multi-reference synthesis when assets exist, e.g.:

- A → structure
- B → color
- C → illustration language

Output must be an original design.

## Categories (framework)

`editorial` · `minimalism` · `technology` · `artistic` · `infographic` · `typography` · `cover-design` · `carousel-layout` · `photography` · `color-palettes`  
(+ `private/` for non-public local refs)

## Copyright

- Do not scrape copyrighted images into the public repo.
- Uploads ≠ redistribution rights.
- `license: unknown` / `private` → internal analysis only; never ship into final public posts or public redistributable packs.
- Keep private files under ignored `private/` folders.
- Never reproduce protected logos or distinctive protected artwork.

User guide: [assets/visual-reference-library/README.md](../assets/visual-reference-library/README.md)
