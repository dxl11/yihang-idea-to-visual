# Visual Reference Library

Inspiration library for Skill **`yihang-idea-to-visual`**.

Upload your own images. Do **not** scrape copyrighted web images into the public repository.

## Accepted formats

PNG, JPG, JPEG, WEBP (also GIF/BMP/TIFF for indexing). SVG demo sketches may live here for humans, but the indexer focuses on raster formats.

## Where to put files

| Directory | Suggested content |
|---|---|
| `editorial/` | Magazine / editorial layouts |
| `minimalism/` | Minimal compositions |
| `technology/` | Tech / AI aesthetics |
| `artistic/` | Artistic / hand-feel |
| `infographic/` | Charts / process diagrams |
| `photography/` | Photo narrative |
| `typography/` | Type-led posters |
| `miscellaneous/` | Everything else |
| `private/` | Private references (gitignored) |

## Build / update index

```bash
python ../scripts/build_reference_index.py --library . --output catalog.json
```

Incremental by default. Use `--full` to drop missing paths.

## Contact sheets

```bash
python ../scripts/create_contact_sheet.py --library . --output ../../../contact-sheets --category editorial
```

## Tags, source, license

Edit `catalog.json` entries (or ask the agent after visual analysis):

- `tags`: searchable keywords
- `source`: URL or “user upload”
- `author`: creator name
- `license`: `unknown` | `private` | `CC0` | `CC-BY-4.0` | `MIT` | custom
- `attribution`: required credit text

## Delete images

1. Delete the file from disk.
2. Re-run the indexer (`--full` to remove stale entries, or leave incremental `missing: true` markers).

## Private vs public

| Kind | Location | Git |
|---|---|---|
| Public / clearly licensed demos | category folders | may commit |
| Private inspiration | `private/` | ignored |
| Unknown license | local only | do not publish |

Unknown-license images: internal visual analysis only — never treat as redistributable assets in final public posts without rights clearance.

## Demo assets

Original abstract PNG samples in this repo are project-made layout/color sketches. They are **not** commercial templates and **not** third-party works.
