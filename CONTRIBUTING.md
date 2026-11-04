# Contributing to Idea to Visual

Thank you for contributing to **Yihang Idea to Visual** (Skill id: `yihang-idea-to-visual`).

## Ground rules

1. This repository publishes **one Skill**, not multiple skills, not an agent team, not a web app.
2. Keep `SKILL.md` under 500 lines; put deep detail in `references/`.
3. Skill folder name and frontmatter `name` must remain `yihang-idea-to-visual`.
4. Do not commit private articles, private brand kits, or unknown-license images.
5. Do not bundle commercial fonts.
6. Prefer fixes that keep scripts CLI-friendly (`--help` required).

## Development setup

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

On Windows PowerShell the same commands work.

## What to change where

| Change | Location |
|---|---|
| Workflow / stage gates | `.agents/skills/yihang-idea-to-visual/SKILL.md` |
| Deep design rules | `references/*.md` |
| Platform sizes | `assets/platform-profiles/profiles.json` |
| Schemas | `schemas/*.schema.json` |
| Scripts | `scripts/*.py` |
| Docs | `README.md` and `README.en.md` (keep both in sync) |

## Pull request checklist

- [ ] Tests pass (`python -m pytest`)
- [ ] Scripts still expose `--help`
- [ ] No private user content
- [ ] Asset licenses documented if media was added
- [ ] Chinese and English README sections stay aligned
- [ ] Skill name remains `yihang-idea-to-visual`

## Code style

- Python 3.10+ type hints where helpful
- Explicit timeouts and error messages for I/O
- Javadoc-style docstrings for public functions (Args / Returns / Raises)
- Delete unused files and dead code in the same PR

## Reporting issues

Include:
- OS and Python version
- Exact command
- Expected vs actual result
- Whether a CJK font is installed
