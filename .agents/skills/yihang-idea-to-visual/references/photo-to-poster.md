# Photo-to-Poster — 照片艺术海报生成

Internal module of Skill `yihang-idea-to-visual`. Not a separate skill or agent.

Assets: [assets/photo-to-poster/](../assets/photo-to-poster/)  
Catalog: [prompt-catalog.json](../assets/photo-to-poster/prompt-catalog.json)

## When to use

User uploads one or more personal photos and wants artistic 3:4 posters driven by those photos as reference—not carousel article pages.

## Hard rules (non-negotiable)

1. One input photo → one independent poster.
2. Batch uploads: process **sequentially**, separate jobs.
3. Never collage / grid / multi-photo mashup as the final deliverable.
4. Never put multiple source photos into one image-generation request.
5. Canvas default **1080×1440 (3:4)**.
6. Top band = **real source pixels** via `compose_poster.py`.
7. Bottom band = generated art from **that same photo only**.
8. No stretch/distort of the subject; use cover-center or contain-pad.
9. No gibberish text from the image model; captions via Pillow if needed.
10. Same style for a batch is allowed, but still **one generation job per photo**.

## Workflow

1. Accept photo(s). Copy into project `source/` (local only).
2. Run `inspect_photo.py` per photo (technical facts). Host vision adds subject/scene notes.
3. Recommend **three** styles from the 12 recipes (reasons + prompt ids). User may reshuffle.
4. User picks style: apply-all **or** per-photo override.
5. For each photo independently:
   - Load `base-prompt.md` + selected recipe.
   - If host image tool exists: generate art panel using **only this photo** as reference (prefer bottom-focused / full art then crop).
   - If no image tool: state the limitation; do not fake generation.
   - `compose_poster.py --photo … --art … --ratio-top <from catalog>`.
   - `validate_poster.py` on the PNG.
6. Show each poster separately. Allow single-photo regenerate without touching others.
7. `export_posters.py` → `manifest.json` + `final-export.zip`.

Minimize interrogation; reuse prior style choice when obvious.

## Style catalog (12)

| ID | Name | Top/Bottom |
|---|---|---|
| 01-minimal-abstract | 极简几何抽象 | 50/50 |
| 02-linocut-travel | 油毡版画旅行手记 | 45/55 |
| 03-raster-distortion | 光栅线场实验 | 50/50 |
| 04-swiss-editorial | 瑞士国际主义编辑 | 50/50 |
| 05-cyanotype-blueprint | 蓝晒艺术蓝图 | 50/50 |
| 06-risograph-print | 复古孔版印刷 | 45/55 |
| 07-topographic-lines | 地形等高线 | 50/50 |
| 08-paper-cut-relief | 纸雕浮雕 | 45/55 |
| 09-naturalist-specimen | 自然博物志 | 45/55 |
| 10-technical-line-art | 技术线描 | 50/50 |
| 11-ink-wash | 东方水墨 | 50/50 |
| 12-photogravure | 复古铜版摄影 | 50/50 |

## Layering model

| Layer | Owner |
|---|---|
| A Photo analysis | Host vision |
| B Art generation | Host image tool (optional; disclose if missing) |
| C Composition | `scripts/photo_to_poster/compose_poster.py` |
| D Typography | Pillow / SVG post-process |
| E QA / ZIP | `validate_poster.py` + `export_posters.py` |

If the generator returns a full-frame art image, crop/extract the bottom band for composition, but the **top band must still be the original photo pixels**.

## Output layout

```text
.idea-to-visual/photo-to-poster-output/<project>/
  source/
  generated-panels/
  posters/photo-001-poster.png …
  manifest.json
  final-export.zip
```

Private; do not commit user photos or posters to public GitHub.

## Relationship to carousel workflow

Photo-to-Poster is an **alternate module**. It does not replace Thought Reviewer → article → cover → editorial carousel. Do not mix locked-article carousel pages into poster jobs unless the user explicitly asks for a separate project.
