# Brand Identity System

## Three layers (never conflate)

### Layer 1 — Long-term brand identity

Stable recognition rules:

- Brand name (optional)
- Author signature
- Logo or wordmark
- Primary / secondary colors
- CJK and Latin font families
- Type hierarchy
- Page margins & grid
- Cover rules
- Body page rules
- Decorative / icon assets
- Usage do's and don'ts

Stored in brand-kit (public sample or user private path). Missing name/logo must **not** block creation — use neutral design without inventing a fake brand.

### Layer 2 — Personal visual preferences

Long-lived taste: preferred styles, colors, density, imagery types.  
Update **only** with explicit user consent after suggesting a change.

### Layer 3 — Project design profile

Per-work variation in `design/cover-profile.json` and `design/editorial-profile.json`.

## Preference update protocol

1. After a project, optionally analyze feedback.
2. Propose candidate long-term preference updates.
3. Apply only if the user clearly agrees.
4. Never promote a one-off request (e.g. temporary dark tech look) into Layer 1/2 automatically.

## Fonts & licensing

- Configure paths in brand / design profile.
- Prefer already-installed licensed fonts.
- Missing CJK font → fail clearly; no silent mojibake.
- Do not download commercial fonts into the repository.

## Schema

Validate with [schemas/brand-profile.schema.json](../schemas/brand-profile.schema.json).
