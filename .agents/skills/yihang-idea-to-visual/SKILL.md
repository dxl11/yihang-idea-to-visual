---
name: yihang-idea-to-visual
description: >-
  Turns a raw idea into a branded social-media image carousel (cover + body PNGs + ZIP).
  Guides thought organization, article editing, title creation, cover design, editorial
  pagination, visual review, and export while protecting locked article text. Use when
  the user mentions Idea to Visual, yihang-idea-to-visual, personal IP graphics, 图文创作,
  封面设计, 小红书轮播, carousel PNG export, or wants to turn notes into publishable visuals.
license: MIT
compatibility: Requires Python 3.10+ with Pillow for local PNG rendering; optional host image-generation tools when available.
metadata:
  author: yihang
  version: "1.0.0"
  product: Idea to Visual
  product_alias: Yihang Idea to Visual
---

# Yihang Idea to Visual

Single Agent Skill. Not an agent team, MCP server, or web app.

**Product name:** Idea to Visual (Yihang Idea to Visual)  
**Skill id / folder:** `yihang-idea-to-visual`

Core promise: the user focuses on thinking and expression; this skill handles editing, design, layout, and packaging.

## When to use

- User provides raw notes, drafts, voice transcripts, or scattered opinions and wants publishable carousel graphics.
- User asks for cover + multi-page editorial PNGs for one social platform.
- User wants personal-brand visual consistency across a post.

## Hard constraints

1. One skill owns the full workflow end-to-end.
2. Never invent author experiences, fake data, or reverse the author's stance.
3. After article lock, never rewrite, summarize, compress, delete, or invent body text. Layout-only changes are allowed.
4. One platform and one canvas size per project. Do not auto-export multi-size packs.
5. Do not auto-advance stages. Ask after each lock.
6. Do not pretend image APIs exist. Use host tools if present; otherwise use programmatic/template rendering and state the limit.
7. Never send full Chinese article text to an image model for typography. Render text with `scripts/render_pages.py` (Pillow).
8. Private project data lives under `.idea-to-visual/projects/` (gitignored). Never write private content into public skill asset folders.
9. Unknown-license reference images: internal analysis only, never treat as redistributable.

## Progressive references

Load only what the current stage needs:

| Stage need | Read |
|---|---|
| Article editing | [references/content-editing.md](references/content-editing.md) |
| Titles | [references/title-generation.md](references/title-generation.md) |
| Platform / size | [references/platform-profiles.md](references/platform-profiles.md) |
| Cover design | [references/cover-design.md](references/cover-design.md) |
| Body editorial design | [references/editorial-design.md](references/editorial-design.md) |
| Brand layers | [references/brand-identity.md](references/brand-identity.md) |
| Visual library | [references/reference-library.md](references/reference-library.md) |
| Review / revisions | [references/review-and-revision.md](references/review-and-revision.md) |
| QA / ZIP export | [references/quality-and-export.md](references/quality-and-export.md) |

Schemas: [schemas/](schemas/) · Scripts: [scripts/](scripts/) · Assets: [assets/](assets/)

## Project persistence

Create/continue projects under:

```text
.idea-to-visual/projects/<project-name>/
  state.json
  source/original-idea.md
  content/article-draft.md | final-article.md | title.md
  design/platform.json | cover-profile.json | editorial-profile.json | brand-snapshot.json
  previews/cover/ | editorial/
  pages/page-manifest.json
  output/cover/ | pages/
  export/final-export.zip
  history/versions.json
```

Copy structure from [assets/templates/project-template/](assets/templates/project-template/) when starting.

### Stage status values

Use exactly one primary status in `state.json`:

`article_review` → `article_locked` → `title_review` → `title_locked` → `platform_selected` → `cover_preview` → `cover_locked` → `editorial_preview` → `editorial_locked` → `pages_generated` → `review` → `finalized` → `exported`

Rules:
- User confirmation required before status advances.
- Do not skip unconfirmed stages.
- New chats must read `state.json` and resume.
- Article edits create a new version; warn that title/cover/editorial may need re-confirmation.
- Page revisions keep history; do not wipe prior outputs.

## Workflow overview

```text
STEP 01 Article → STEP 02 Title → STEP 03 Cover → STEP 04 Editorial → STEP 05 Review → STEP 06 Export
```

### STEP 01 — Thought organization & article polish

1. Read the raw idea; identify theme, claims, and structure.
2. Edit for clarity while preserving the author's voice.
3. Iterate on user feedback from the **current** draft (do not restart from scratch each turn).
4. On confirmation: write `content/final-article.md`, append history, set `article_locked`, ask to enter STEP 02.

Forbidden: fabricated stories/data, stance reversal, engagement-driven distortion.

Details: [references/content-editing.md](references/content-editing.md)

### STEP 02 — Title creation

1. Use **only** the locked article as source.
2. Offer **5 distinctly different** titles (viewpoint / reflective / question / viral / suspense — adapt labels to content).
3. Do not produce near-duplicate paraphrases.
4. On confirmation: save `content/title.md`, lock, ask to enter cover design.

Details: [references/title-generation.md](references/title-generation.md)

### STEP 03 — Cover design

1. Select **one** platform; load [assets/platform-profiles/profiles.json](assets/platform-profiles/profiles.json). Prefer live verification of sizes when network is available; never claim unverified sizes are official.
2. Ask at most **3** visual questions that change direction; skip known facts; use defaults for non-critical gaps.
3. Analyze theme + brand kit + reference library.
4. Propose **3 visually distinct** cover directions (not just recolors). Styles must be content-driven (editorial, minimal, tech, artistic journal, photo narrative, infographic, big-type, etc.).
5. Produce three full cover previews; iterate; lock cover; ask before STEP 04.

Image generation: use host image tools for illustration/background only when available. Always composite final title/author text via `scripts/render_pages.py`.

Details: [references/cover-design.md](references/cover-design.md), [references/reference-library.md](references/reference-library.md), [references/brand-identity.md](references/brand-identity.md)

### STEP 04 — Editorial design (content protection max priority)

Locked article text is immutable except layout.

Allowed: re-pagination, paragraph layout, line breaks, type size, visual emphasis of existing words.  
Forbidden: sentence edits, deletion, summarization, compression, stance change, new claims.  
If text does not fit → **add pages**, never cut copy.

Process:
1. Paginate by semantic units (no fixed page count).
2. Choose visual strategy from topic (tech / business / reflection / knowledge / story / data). Not every page needs imagery.
3. Preview **three** distinct editorial styles on a representative page; user picks one.
4. Build Design Profile (fonts, colors, margins, grid, folio, signature). Cover and body styles may differ but must stay brand-coherent.
5. Generate full set via page JSON + `scripts/render_pages.py`. Record contiguous text fragments in `page-manifest.json` for integrity checks.

Templates: `editorial-minimal`, `modern-technology`, `artistic-journal` (see [assets/templates/editorial-layouts/](assets/templates/editorial-layouts/)).

Details: [references/editorial-design.md](references/editorial-design.md)

### STEP 05 — Holistic review & local edits

1. Build a contact sheet / thumbnails of all pages (`scripts/create_contact_sheet.py` when helpful).
2. Support single-page, multi-page, or global visual edits with matching blast radius.
3. If a request would change locked article wording → stop, warn, and require returning to STEP 01 for a new article version.
4. Version every revision under `history/`.

Details: [references/review-and-revision.md](references/review-and-revision.md)

### STEP 06 — QA & delivery

Run:

```bash
python scripts/validate_project.py --project <path>
python scripts/package_export.py --project <path>
```

Deliver:

```text
<project-name>/
  00-cover.png
  01-page.png
  02-page.png
  ...
  final-export.zip
```

Checks must cover existence, openability, size/aspect, mojibake, overflow, **exact article integrity** (concatenated page fragments == locked article), folio continuity, brand coherence, ZIP test. Failures cannot be marked final.

Details: [references/quality-and-export.md](references/quality-and-export.md)

## Helper scripts

Run from skill root `.agents/skills/yihang-idea-to-visual/` (or pass absolute paths).

| Script | Purpose |
|---|---|
| `scripts/build_reference_index.py` | Scan library → incremental `catalog.json` |
| `scripts/create_contact_sheet.py` | Thumbnail contact sheets with IDs |
| `scripts/render_pages.py` | JSON layout → PNG (text + shapes + images) |
| `scripts/validate_project.py` | Integrity / size / mapping QA |
| `scripts/package_export.py` | Ordered PNGs + ZIP + manifest |

Each script supports `--help`.

## Brand layers (do not conflate)

1. **Long-term brand identity** — stable kit in brand-kit (or user private path).
2. **Personal visual preferences** — lasting taste; update only with explicit user consent after a project.
3. **Project design profile** — per-work variation.

Missing brand name/logo must not block creation; use neutral untitled design.

Details: [references/brand-identity.md](references/brand-identity.md)

## Fonts

- Use installed, redistributable-allowed fonts via configured paths.
- Missing CJK font → clear error; never silently emit garbled glyphs.
- Do not download/bundle commercial fonts into the repo.

## Capability boundary

| Capability | Behavior |
|---|---|
| Text editing / titles / planning | Always available |
| Precise Chinese typography | `render_pages.py` + system fonts |
| Illustration / photo generation | Only if host agent exposes a real image tool |
| No image tool | Programmatic backgrounds + demo/reference assets; disclose limit |
| Network size verification | Prefer official sources when online; otherwise label sizes as configured defaults |

## Resume checklist

On every turn after the first:
1. Locate project path / `state.json`.
2. Confirm locked artifacts still exist.
3. Continue from the current status only.
4. Refuse stage skips without user confirmation.
