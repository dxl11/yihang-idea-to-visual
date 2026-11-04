# Cover Design — STEP 03

## Prerequisites

- `article_locked`
- `title_locked`
- Platform selected (`platform_selected`)

## Pre-design questions

Ask **at most 3** questions that materially change visual direction. Skip anything already known. Use defaults for non-critical gaps (e.g., prefer light background if unspecified).

Good questions: mood (calm vs bold), imagery preference (abstract / photo / type-led), must-include brand mark.

## Analysis sequence

1. Article theme & emotional tone
2. Title hierarchy (primary line vs optional subtitle)
3. Brand kit + preference layer
4. Reference library retrieval (category/tags first; do not scan everything)
5. Compose **three original directions**

## Three previews

Each preview must differ in **structure**, not only palette. Vary at least two of: layout grid, typography scale, imagery type, density/whitespace philosophy.

Example style pool (choose dynamically):

- Magazine editorial
- Modern minimal
- Tech futurism
- Artistic journal
- Photo narrative
- Infographic
- Big-type poster
- Other original direction suited to the piece

## Rendering split

| Layer | Owner |
|---|---|
| Illustration, abstract BG, decorative art | Host image tool if available; else programmatic / SVG samples |
| Title, author, logo text, folio | `scripts/render_pages.py` only |

Never ask an image model to paint the full Chinese title as final typography.

## Lock

On approval: save cover profile + final cover preview path, set `cover_locked`, ask before STEP 04.

## Reference combination

May combine traits from multiple references (A layout + B color + C illustration language). Must produce an original composition — never clone one reference wholesale. Do not copy protected logos.
