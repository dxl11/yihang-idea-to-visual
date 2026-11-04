# Changelog

All notable changes to **Idea to Visual** / Skill `yihang-idea-to-visual` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] — 2026-11-04

### Changed
- Redesigned bilingual GitHub README under Darkroom Safelight Bay art direction: custom banner, timer-card install lead, station→workflow mapping; install commands unchanged.

### Added
- `docs/assets/readme-banner.png`, `PRODUCT.md`, `DESIGN.md`.

## [1.2.0] — 2026-11-04

### Added
- Thought Reviewer (STEP 00) inside the existing skill: six lenses, eight qualitative dimensions, dialogue rules, and three modes (`standard` / `deep_critique` / `light`).
- Progressive references: `thought-reviewer.md`, `thinking-frameworks.md`.
- Thought Library under `assets/thought-library/` with curated method cards, demo citation note, and `scripts/build_thought_index.py`.
- Project statuses `thought_review` / `thought_ready`, optional `thought_mode` / `thought_skipped`, and `thought/` artifacts in the project template.
- Acceptance fixtures and automated tests for Thought Reviewer wiring, indexing, skip path docs, and citation metadata.
- Bilingual README section documenting Thought Reviewer, dialogue, modes, private library maintenance, and copyright rules.

### Changed
- Workflow now starts with optional thought review before article polish; existing stages 01–06 remain intact.
- Skill metadata version bumped to 1.2.0.

## [1.1.0] — 2026-03-25

### Added
- Official one-command install docs via Vercel Skills CLI (`npx skills`).
- Bilingual install / update / uninstall / verify sections aligned with https://github.com/dxl11/yihang-idea-to-visual.
- CI checks for install command consistency, README bilingual presence, and private/sensitive path safeguards.

### Changed
- Canonical GitHub repository URL set to `https://github.com/dxl11/yihang-idea-to-visual`.
- README section order reorganized for distribution and onboarding.

## [1.0.0] — 2026-03-25

### Added
- Single Agent Skill `yihang-idea-to-visual` with six-stage creative workflow.
- Progressive-disclosure references for editing, titles, platforms, cover/editorial design, brand identity, review, and export.
- Helper scripts: reference index, contact sheet, page renderer, project validator, ZIP exporter.
- JSON Schemas for brand profile, project state, design profile, and page manifest.
- Visual reference library directory layout with catalog sample and original demo SVGs.
- Platform profiles for Xiaohongshu, WeChat, Douyin, Weibo, Instagram, LinkedIn, and custom sizes.
- Bilingual README (`README.md` / `README.en.md`), MIT LICENSE, ASSET-LICENSES, CONTRIBUTING.
- GitHub Actions validation workflow and automated tests for skill structure, text integrity, rendering, and export.

### Notes
- Image generation depends on tools available in the host agent environment; this skill does not ship an image API.
- Private user projects should live under `.idea-to-visual/projects/` and remain gitignored.
