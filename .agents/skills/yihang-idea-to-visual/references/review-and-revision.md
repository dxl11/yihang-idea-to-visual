# Review and Revision — STEP 05

## Holistic preview

After all pages render:

1. Present ordered thumbnails (contact sheet recommended).
2. Allow opening any page at full size.
3. Collect revision requests with clear scope.

## Revision scopes

| Scope | Effect |
|---|---|
| Single page | Only the named page |
| Multi page | Only the listed pages |
| Global | Shared design tokens / all pages |

Always restatescope back to the user before regenerating.

## Locked text boundary

If a revision requires changing locked article wording:

1. Stop visual-only editing.
2. Explain that article text is locked.
3. Require returning to STEP 01, creating a new article version, then reconfirming dependent stages as needed.

## Versioning

- Keep prior PNG outputs under `history/` or versioned subfolders.
- Append entries to `history/versions.json`.
- Do not destroy previous confirmed exports until the user explicitly replaces them.

## Status

While revising, status is `review`. When the user accepts the set, move to `finalized` then run STEP 06 checks before `exported`.
