# Quality and Export — STEP 06

## Required outputs

```text
00-cover.png
01-page.png
02-page.png
...
final-export.zip
```

## Pre-flight checklist

1. All expected PNGs exist
2. Each PNG opens successfully
3. Dimensions match selected platform
4. Aspect ratio consistent across set
5. No mojibake / tofu glyphs
6. No text overflow flags in page JSON / validator
7. Article integrity: concatenated `text_fragments` == locked article
8. Page numbers continuous
9. Brand tokens consistent with design profile
10. ZIP created and tested for extractability

## Commands

```bash
python scripts/validate_project.py --project ../../../../../.idea-to-visual/projects/<name>
python scripts/package_export.py --project ../../../../../.idea-to-visual/projects/<name> --name <name>
```

Prefer absolute project paths in practice.

## Integrity rule

Validation must compare **normalized continuous text**, not merely character counts. See `validate_project.py` for the exact normalization used (documented in `--help` / module docstring). If integrity fails, the project must not be marked `exported`.

## Failure policy

Any failed check → remain in `finalized` or `review`, report actionable errors, fix, re-validate. Never hand over a failing ZIP as a final deliverable.
