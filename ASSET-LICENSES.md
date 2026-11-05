# Asset License Policy / 素材版权管理办法

This document governs images, fonts, logos, and other non-code assets used with **Yihang Idea to Visual** (`yihang-idea-to-visual`).

---

## 1. Scope

| Asset type | Default status | Redistributable in this repo? |
|---|---|---|
| Python scripts, schemas, docs | MIT (see `LICENSE`) | Yes |
| Original demo SVG samples created for this project | MIT | Yes |
| User-uploaded reference images | Private / user-owned | No (unless user grants explicit public license) |
| Third-party photos / magazine scans | Unknown until proven | No |
| Commercial fonts | Not bundled | No |
| Brand logos / marks | Trademark-protected | No |

---

## 2. Visual Reference Library

### Allowed local uses
- Internal visual analysis by the AI agent
- Style inspiration for original compositions
- Contact sheet generation for browsing

### Forbidden uses
- Copying a protected composition wholesale into a final deliverable
- Reproducing protected logos, characters, or distinctive artwork
- Publishing unknown-license images to a public GitHub repository
- Claiming user-uploaded private references as MIT-licensed project assets

### Required metadata fields
Every indexed reference should record:
- `source`
- `author`
- `license` (`unknown` | `private` | `CC0` | `CC-BY-4.0` | `MIT` | custom)
- `attribution`

Images with `license: unknown` or `license: private` must stay local (for example under a `private/` directory ignored by git).

---

## 3. Fonts

- Do **not** download or bundle commercial fonts into this repository.
- Prefer fonts already installed on the host system with a compatible license.
- Configure font paths in the brand kit / design profile.
- If a required CJK font is missing, scripts must fail with a clear error instead of rendering mojibake.

Suggested safe system fonts (availability varies by OS):
- Windows: `Microsoft YaHei`, `SimHei`, `Segoe UI`
- macOS: `PingFang SC`, `Hiragino Sans GB`, `Helvetica Neue`
- Linux: `Noto Sans CJK`, `Source Han Sans` (if installed by the user)

---

## 4. Generated Output

PNG covers, editorial pages, and ZIP packages created for a user project belong to the user, subject to:
- Rights in any third-party assets embedded in those pages
- Trademark restrictions on logos used
- Platform content policies for the chosen social network

---

## 5. Demo Assets in This Repository

The built-in visual reference library under
`.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/`
currently ships **empty** (directories + empty `catalog.json` only). Do not commit third-party scraped images there.

README banner `docs/assets/readme-banner.png` is an original darkroom-theme illustration generated for this project (MIT). Prompt provenance is embedded in the PNG and mirrored in `docs/assets/readme-banner.png.json`.

---

## 6. Thought Library

Path: `.agents/skills/yihang-idea-to-visual/assets/thought-library/`

| Material | Default status | Public repo? |
|---|---|---|
| Curated method cards in this repo | MIT | Yes |
| Original demo expert note | MIT | Yes |
| User private notes / excerpts | Private / user-owned | No (`private/`) |
| Copyrighted full books or scanned chapters | Not allowed | No |

Rules:
- Prefer short executable method cards over bulk uploads.
- Record `author` / `source` / `work_title` / `section` / `page` when citing.
- Never invent citations or page numbers.
- Do not commit copyrighted full books to the public repository.
- Private materials stay under `private/` (gitignored) or outside the repo.

---

## 7. Contribution Rule

Do not open a pull request that adds:
- Scraped web images
- Magazine scans without documented permission
- Packaged commercial fonts
- Private brand kits or private project articles
- Copyrighted full books or unauthorized long excerpts for the Thought Library

When contributing an image or thought card, include license, source, and attribution in `catalog.json` or the card frontmatter.
