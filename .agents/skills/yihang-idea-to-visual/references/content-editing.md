# Content Editing — STEP 01

## Goal

Transform raw user input into a clear, publishable article while preserving the author's voice and intent.

## Input types

- Quick notes or sticky thoughts
- Unstructured long drafts
- Scattered opinions
- Work notes / meeting remnants
- Speech-to-text transcripts
- Multi-fragment thinking not yet coherent

## Process

1. **Understand intent** — What does the author actually want readers to take away?
2. **Identify theme** — One primary theme; secondary themes stay supporting.
3. **Map logic** — Cause→effect, problem→insight→action, narrative arc, or claim→evidence.
4. **Restructure** — Headings/sections only when they help reading; do not force a blog template.
5. **Polish language** — Clarity, rhythm, readability; keep characteristic phrasing.
6. **Iterate** — Always edit from the **current draft**, not from the original each time.

## Allowed edits

- Reordering for clearer logic
- Tightening redundant sentences
- Fixing grammar and punctuation
- Clarifying ambiguous pronouns or references
- Splitting oversized paragraphs

## Forbidden edits

- Inventing personal stories the author never told
- Adding statistics or citations without a user-provided source
- Reversing or softening the author's stance for virality
- Inserting trending buzzwords that change meaning
- Claiming expertise the author did not express

## Versioning

On each meaningful revision:

1. Save previous draft under `history/` (or append to `versions.json`).
2. Update `content/article-draft.md`.
3. Do **not** overwrite all history files.

When the user confirms satisfaction:

1. Write `content/final-article.md`.
2. Record version id + timestamp in `history/versions.json`.
3. Set status `article_locked`.
4. Ask whether to enter title creation. **Do not auto-advance.**

## Unlocking later

If the user later changes locked article text:

1. Create a new article version.
2. Explicitly warn that title, cover, and editorial pages may need re-confirmation.
3. Downgrade dependent locks in `state.json` as needed.
