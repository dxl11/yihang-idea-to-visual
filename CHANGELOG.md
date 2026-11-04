# Changelog

All notable changes to **Idea to Visual** / Skill `yihang-idea-to-visual` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
