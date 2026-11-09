# Cover generation brief (STEP 03)

Combine with locked article/title, platform size, brand rules, and **actually loaded** visual-library references.

## Hard requirements

1. Use the reference images that were passed into the host image tool (native image reference input). Paths-in-text alone are invalid.
2. Borrow design language (composition, hierarchy, color relations, whitespace, graphic language) — re-compose for **this** article. Do not clone.
3. Do not create “three schemes” that only recolor the same layout.
4. Match the selected platform canvas (e.g. 1080×1440 for Xiaohongshu default).
5. Final Chinese title / author / folio must be composited via `scripts/render_pages.py` — never rely on the image model for accurate CJK typography.
6. Do not alter locked article or title wording.
7. If no reference images were loaded (`empty` / `no_match` / tool lacks ref support), state that clearly in the project cover-ref manifest and proceed with brand + these rules only.

## Brief skeleton

```text
Article theme / claim: …
Locked title: …
Platform / size: …
Brand constraints: …
Reference REF-ids + absolute paths actually passed to the image tool: …
Borrowed from refs (composition / color / type / hierarchy / whitespace / graphics): …
Direction concept (must differ structurally from the other two): …
Avoid: collage of multiple unrelated photos, gibberish text, cloned logos, palette-only variants
```

## Per-direction log (required)

For each of A / B / C record:

- `ref_ids`: list (may be empty only in empty/no_match/no-ref-tool branches)
- `borrowed`: short note of design language used
- `structure_diff`: what makes this direction structurally distinct
- `image_reference_used`: true only if host tool call included those images
