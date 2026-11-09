# Visual Reference Library

Directory: [assets/visual-reference-library/](../assets/visual-reference-library/)

## Purpose

Built-in inspiration library maintained by the skill author. Used for **analysis and trait combination** during cover and editorial design—not for copying final artwork.

The library may be **empty**. An empty `catalog.json` is valid and must not block the creative pipeline — but the agent must **disclose** that covers are generated without image references.

## STEP 03 cover retrieval (required)

Before inventing cover art:

1. Read `catalog.json`.
2. Run `scripts/retrieve_cover_references.py` (writes a cover-ref manifest).
3. Branch on `mode`:

| Mode | Required behavior |
|---|---|
| `empty` | Inform user; continue with brand + cover rules; `image_reference_used` stays false |
| `no_match` | Inform user; optional consent to continue without refs; never invent matches |
| `matched` | Open verified files; pass `absolute_path` into host image tool reference input; log REF-ids per cover direction |

**Forbidden:** path-only prompts, catalog-text-as-image, claiming refs without a real tool image-input call.

Editorial (STEP 04) still uses the empty-catalog skip for retrieval when `total_assets == 0`, and the same honesty rules when assets exist.

## Indexing

```bash
python scripts/build_reference_index.py \
  --library assets/visual-reference-library \
  --output assets/visual-reference-library/catalog.json
```

The script extracts technical metadata (path, size, aspect, hash, duplicates) and creates pending analysis fields. It keeps `assets` and `items` in sync and updates `total_assets`. It does **not** invent design-language understanding from filenames alone.

Optional analysis fields (fill when a pixel-capable agent reads the image):  
`style_notes`, `layout_notes`, `color_notes`, `typography_notes`, `composition_notes`, `visual_hierarchy`, `whitespace_notes`, `graphic_language`, `use_cases`, `tags`, `best_for`.

Visual analysis must be performed by an AI that can read image pixels. If the host cannot read images, state the limitation; do not fake analysis.

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

Prefer filter by `category`, `tags`, `best_for`, and existing notes. Do not traverse the entire library every time. Prefer `retrieve_cover_references.py` for STEP 03 so load failures are explicit.

## Combination

Support multi-reference synthesis when assets exist and are loaded, e.g.:

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
- Never create fake catalog rows or download unauthorized web images into the library.

User guide: [assets/visual-reference-library/README.md](../assets/visual-reference-library/README.md)
