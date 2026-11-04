# Editorial Design — STEP 04

## Absolute content protection

After `article_locked`, body production **must not**:

- Modify sentences
- Delete content
- Summarize or compress
- Change viewpoints
- Add new claims

**May** only: re-paginate, adjust paragraph layout, line breaks, type size, and visual emphasis of existing words.

If copy does not fit → **add a page**. Never cut text to fit.

## Pagination

Do not fix page count (e.g. not always 7).

1. Parse natural paragraphs / sections
2. Keep semantic units together when readable
3. Avoid overcrowded pages
4. Avoid splitting a complete argument just to inflate page count
5. Cover is **not** counted as a body page

## Visual strategy by topic (examples)

| Topic | Typical visuals |
|---|---|
| AI / tech | Abstract tech forms, diagrams |
| Business | Editorial magazine layout, structure charts |
| Personal reflection | Type-led, artistic journal |
| Knowledge | Infographic, process diagrams |
| Story | Illustration / photo narrative |
| Data | Charts (data must come from the article) |

Not every page needs an image. Imagery serves the text.

## Three style previews

1. Pick a representative body page.
2. Render three distinct styles (font system, structure, palette, whitespace, text/image ratio, reading feel).
3. User selects one.
4. Cover style and body style may differ but must remain brand-coherent.

Built-in layout ids (clear structural differences):

- `editorial-minimal`
- `modern-technology`
- `artistic-journal`

JSON samples: [assets/templates/editorial-layouts/](../assets/templates/editorial-layouts/)

## Batch production

After style lock:

1. Write `design/editorial-profile.json` (fonts, colors, margins, grid, folio, signature).
2. Build `pages/page-manifest.json` with ordered pages and **contiguous text fragments** covering the full locked article.
3. Render each page with `scripts/render_pages.py`.
4. Set status `pages_generated` then move to review.

## Integrity mapping

Each body page records `text_fragments` in reading order. Concatenating all fragments (no extra spaces inserted by the checker beyond documented normalization rules in `validate_project.py`) must equal the locked article body. Whitespace/newline handling is defined by the validator — do not “fix” integrity by counting characters alone.
