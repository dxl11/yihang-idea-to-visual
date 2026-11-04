# Brand Kit

Long-term brand identity files for **Yihang Idea to Visual** (`yihang-idea-to-visual`).

## Layout

```text
brand-kit/
  README.md
  brand-profile.sample.json   # public sample (neutral)
  private/                    # gitignored — put real logos & private prefs here
```

## Rules

1. Missing brand name or logo must not block creation — use neutral design.
2. Never invent a fake brand name for the user.
3. Private logos and preference files belong in `private/` (ignored by git).
4. Validate profiles with `schemas/brand-profile.schema.json`.
5. Font paths must point to fonts already installed / licensed on the machine.

## Sample

See `brand-profile.sample.json` for a neutral starter profile.
