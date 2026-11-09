# Cover Design — STEP 03

## Prerequisites

- `article_locked`
- `title_locked`
- Platform selected (`platform_selected`)
- Do **not** modify locked article or title

## Pre-design questions

Ask **at most 3** questions that materially change visual direction. Skip anything already known. Use defaults for non-critical gaps (e.g., prefer light background if unspecified).

Good questions: mood (calm vs bold), imagery preference (abstract / photo / type-led), must-include brand mark.

---

## Mandatory pipeline (asset-driven)

Cover work **must** follow STEP03-A → G. Freeform image generation without attempting library retrieval is forbidden.

### STEP03-A — Analyze cover needs

From locked article + title (+ brand kit + platform):

- Core theme and claim
- Emotional tone / expression
- Suitable visual metaphors
- Subjects or key elements to emphasize
- Platform canvas size
- Brand visual rules (if present; else neutral)

### STEP03-B — Retrieve built-in visual library

1. Read [assets/visual-reference-library/catalog.json](../assets/visual-reference-library/catalog.json).
2. Run:

```bash
python scripts/retrieve_cover_references.py \
  --library assets/visual-reference-library \
  --query "<theme tags mood>" \
  --category cover-design \
  --category typography \
  --limit 3 \
  --output <project>/design/cover-ref-manifest.json
```

Prefer theme / tags / `best_for` / composition metadata — not filenames alone.

### STEP03-C — Actually load reference images

**Critical.** After retrieval:

| Not enough | Required |
|---|---|
| Path written only in a text prompt | Host tool receives real image bytes / native ref input |
| Reading catalog descriptions only | Open verified files (script load report + pixel-capable read) |
| Imagining the image from notes | Pass `absolute_path` into image tool refs |

Host capability (Cursor): `GenerateImage` supports `reference_image_paths`. When mode is `matched`, pass the verified absolute paths there for illustration / background layers.

If the host image tool **cannot** accept reference images: record the limitation in the project notes / manifest; do **not** claim asset-driven generation succeeded.

Set `image_reference_used: true` in the cover-ref manifest **only** after a real tool call that included those paths.

### STEP03-D — Analyze design language of loaded refs

From pixels + metadata, extract: composition, subject placement/scale, color relations, type layout, hierarchy, whitespace, graphic language, style / use-case. Borrow methods — do not clone.

### STEP03-E — Compose generation brief

Combine: article theme/claim, locked title, platform size, brand rules, **loaded** refs + extracted language, [cover-generation.md](../assets/templates/cover-prompts/cover-generation.md), and the direction-specific idea.

Prompt rules must state: use the passed reference images; re-compose for this article; no mechanical clone; no palette-only “variants”; keep Chinese title typography on `scripts/render_pages.py`.

### STEP03-F — Three structurally distinct covers

- Differ in structure (grid / type scale / imagery role / density), not only palette.
- Each direction records which `REF-*` (if any) was used and what was borrowed.
- Show full previews; wait for user choice.

### STEP03-G — Choose / iterate / lock

Keep confirmation gates. Iterate on request. Lock only on approval → `cover_locked` → ask before STEP 04.

---

## Empty / no-match branches

| Mode | Behavior |
|---|---|
| `empty` | Tell user: no built-in reference images. Continue with brand + cover rules **without** image refs. Never fake refs. |
| `no_match` | Tell user: catalog has assets but none suitable / loadable. With consent, use brand/rules only; never invent matches. |
| `matched` | Load + pass refs into host image tool; document REF-ids per direction. |

## Rendering split

| Layer | Owner |
|---|---|
| Illustration, abstract BG, decorative art | Host image tool **with** `reference_image_paths` when matched; else programmatic / disclose no-ref |
| Title, author, logo text, folio | `scripts/render_pages.py` only |

Never ask an image model to paint the final Chinese title as typography.

## Lock

On approval: save cover profile + final cover preview path + cover-ref manifest (with truthful `image_reference_used`), set `cover_locked`, ask before STEP 04.

## Reference combination

When multiple refs load: A structure + B color + C illustration language is allowed. Output must be original. Do not copy protected logos. Unknown-license / private refs → internal analysis only; do not ship into public redistributable packs.
