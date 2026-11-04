# Idea to Visual (Yihang Idea to Visual)

English | [简体中文](README.md)

**Skill id:** `yihang-idea-to-visual`  
**Product name:** Idea to Visual / Yihang Idea to Visual  
**GitHub repository name:** `idea-to-visual` (keep as-is unless you intentionally rename the remote)

Start from a raw idea. Through staged confirmations, organize thinking, polish the article, craft titles, design a cover, paginate editorial graphics, review visuals, and deliver ordered cover/body PNGs plus a ZIP package ready for social publishing.

This repository ships **one** [Agent Skill](https://agentskills.io/specification)—not an autonomous agent, multi-agent crew, MCP server, or web application.

---

## 1. Introduction

Yihang Idea to Visual productizes the personal-IP content pipeline: you focus on thinking and expression; the same skill handles editing, design, layout, and packaging. Project-level install path:

```text
.agents/skills/yihang-idea-to-visual/SKILL.md
```

Cursor discovers skills under `.agents/skills/` automatically. You can also invoke `/yihang-idea-to-visual` in Agent chat.

## 2. Product positioning

Built for creators, researchers, and operators who publish branded carousels. Each project selects **one** platform and **one** canvas size, then exports an upload-ready image set.

## 3. Feature highlights

- Six gated stages (article → title → cover → editorial → review → export)
- **Locked-article integrity protection** (no silent rewrite/summary/deletion)
- Platform profiles separated from skill instructions
- Visual reference indexing, contact sheets, multi-reference trait remixing
- Three brand layers: long-term identity / lasting preferences / per-project style
- Pillow-based precise typography (split from generative imagery)
- Resumable project state under `.idea-to-visual/projects/`
- Ordered ZIP delivery with automated validation

## 4. End-to-end workflow

1. **STEP 01 — Thought organization & polish** — Preserve stance and voice; lock on confirmation.  
2. **STEP 02 — Titles** — Offer five meaningfully different directions from the locked article.  
3. **STEP 03 — Cover** — Pick one platform; ask ≤3 decisive visual questions; show three structurally distinct cover previews.  
4. **STEP 04 — Editorial** — Semantic pagination; three body-style previews; batch render; add pages instead of cutting copy.  
5. **STEP 05 — Review** — Thumbnails; single/multi/global edits; copy changes require returning to STEP 01.  
6. **STEP 06 — QA & delivery** — Validate, then emit `00-cover.png`, `01-page.png`, … and `final-export.zip`.

Do not skip unconfirmed stages. New chats must resume from `state.json`.

## 5. Repository layout

```text
idea-to-visual/
├── README.md / README.en.md
├── LICENSE / ASSET-LICENSES.md / CONTRIBUTING.md / CHANGELOG.md
├── pyproject.toml / .gitignore
├── .github/workflows/validate.yml
├── .agents/skills/yihang-idea-to-visual/
│   ├── SKILL.md
│   ├── references/
│   ├── scripts/
│   ├── schemas/
│   └── assets/
├── examples/
└── tests/
```

Keep private project data in `.idea-to-visual/projects/` (gitignored).

## 6. Installation

```bash
git clone <your-fork-or-repo-url> idea-to-visual
cd idea-to-visual
python -m pip install -e ".[dev]"
```

Requires Python 3.10+ and Pillow. Dev/CI also use pytest and jsonschema.

## 7. Using in Cursor

1. Open this repository root in Cursor.  
2. Cursor discovers `.agents/skills/yihang-idea-to-visual/`.  
3. Describe your idea in Agent chat, or type `/yihang-idea-to-visual`.  
4. Confirm stage by stage; the agent runs helper scripts when needed.

Note: Cursor also loads `.cursor/skills/`. This project maintains **only** the `.agents/skills/` copy to avoid duplication.

For a user-global install, copy the skill folder to `~/.agents/skills/yihang-idea-to-visual/` or `~/.cursor/skills/yihang-idea-to-visual/`.

## 8. Other Agent Skills hosts

Any tool that follows [agentskills.io](https://agentskills.io/specification) generally needs:

1. The `yihang-idea-to-visual` folder on its skill discovery path  
2. Frontmatter `name` matching the directory name  
3. Python + Pillow for scripts  

If Claude Code / Codex scan `.claude/skills` or `.codex/skills`, copy the same folder there (keep a single source of truth).

## 9. Uploading visual references

Place images under:

`.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/<category>/`

Categories: `editorial`, `minimalism`, `technology`, `artistic`, `infographic`, `photography`, `typography`, `miscellaneous`. Private files go in `private/` (ignored).

See [assets/visual-reference-library/README.md](.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/README.md).

## 10. Indexing references

```bash
python .agents/skills/yihang-idea-to-visual/scripts/build_reference_index.py \
  --library .agents/skills/yihang-idea-to-visual/assets/visual-reference-library \
  --output .agents/skills/yihang-idea-to-visual/assets/visual-reference-library/catalog.json
```

The indexer extracts technical metadata and duplicates. Design-language analysis must be done by an AI that can read pixels—never fake it from filenames alone.

Contact sheets:

```bash
python .agents/skills/yihang-idea-to-visual/scripts/create_contact_sheet.py \
  --library .agents/skills/yihang-idea-to-visual/assets/visual-reference-library \
  --output contact-sheets \
  --category editorial
```

## 11. Personal brand kit

Starter sample:

[brand-profile.sample.json](.agents/skills/yihang-idea-to-visual/assets/brand-kit/brand-profile.sample.json)

Store real logos/preferences in `assets/brand-kit/private/` (gitignored). Missing brand names must not invent a fake identity—continue with neutral design.

Long-term preference updates require explicit user consent.

## 12. Platform configuration

Edit [profiles.json](.agents/skills/yihang-idea-to-visual/assets/platform-profiles/profiles.json). One platform per project. Size entries include `source` and `verified_at`. If unverifiable, do not present them as freshly confirmed official rules.

## 13. Image generation dependencies

This skill is **not** an image API. Use host image tools for illustration/backgrounds only when they truly exist; otherwise fall back to programmatic graphics + local references/templates and disclose the limit.

Never send a full Chinese article to an image model for final typography. Titles and body copy are rendered by `render_pages.py`.

## 14. CJK font configuration

Set `typography.cjk_font_path` in brand/design profiles to an installed, license-permitted font. Missing fonts must fail loudly—never emit mojibake silently.

Do not bundle commercial fonts in this repository.

## 15. Helper scripts

| Script | Purpose |
|---|---|
| `scripts/build_reference_index.py` | Reference catalog |
| `scripts/create_contact_sheet.py` | Contact sheets |
| `scripts/render_pages.py` | JSON → PNG layout |
| `scripts/validate_project.py` | Project QA incl. article integrity |
| `scripts/package_export.py` | Ordered naming + ZIP |

Every script supports `--help`.

## 16. Final PNG & ZIP delivery

```text
export/<project-name>/
  00-cover.png
  01-page.png
  02-page.png
  ...
final-export.zip
```

Run `validate_project.py` before calling a deliverable final. Failing checks must not be marked complete.

## 17. Copyright & privacy

- Code & docs: MIT ([LICENSE](LICENSE))  
- Images/fonts/logos: [ASSET-LICENSES.md](ASSET-LICENSES.md)  
- User articles, private references, and private brand kits stay out of GitHub by default  
- Unknown-license references: internal analysis only—not public redistribution

## 18. FAQ

**Q: Skill not discovered?**  
Open the repository root and confirm `.agents/skills/yihang-idea-to-visual/SKILL.md` exists.

**Q: Multi-size export in one run?**  
No. One platform, one canvas per project.

**Q: No image generator available?**  
Copy, titles, and structured typography PNGs still work; illustration layers degrade with an explicit capability note.

**Q: Is the old id `idea-to-visual` still valid?**  
Use Idea to Visual as the product name; the **skill id must be** `yihang-idea-to-visual`.

## 19. Current limitations

- No bundled cloud image API keys  
- Platform sizes are configurable defaults—verify against official sources when needed  
- Semantic reference analysis depends on host vision capability  
- CJK quality depends on local fonts

## 20. Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Before opening a PR:

```bash
python -m pytest
```

---

## Acceptance snapshot

- [x] Single skill: `yihang-idea-to-visual`
- [x] Standard `SKILL.md` + references
- [x] Five runnable scripts + tests
- [x] Bilingual README
- [x] LICENSE / ASSET-LICENSES / gitignore / CI
