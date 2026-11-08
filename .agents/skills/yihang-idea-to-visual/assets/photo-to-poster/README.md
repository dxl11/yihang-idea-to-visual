# Photo-to-Poster（照片艺术海报生成）

内置于 Skill `yihang-idea-to-visual` 的照片驱动艺术海报模块。

用户上传照片 → AI 分析 → 推荐风格 → 调用 Prompt Recipe → **逐张**生成艺术区 → Pillow 合成原图上半区 → 输出独立 3:4 PNG。

## Hard rules

1. **一张输入照片 = 一张独立海报。**  
2. 多张照片分别处理；禁止拼贴 / 九宫格 / 多图合集成品。  
3. 禁止把多张照片放进同一个图像生成请求。  
4. 画布默认 **1080×1440（3:4）**。  
5. **上半区使用原始照片实际像素**（`compose_poster.py`），不得用模型重绘冒充原貌。  
6. 下半区才是艺术生成重点。  
7. 不得拉伸扭曲主体；用 cover-center 或 contain-pad。  
8. 文案乱码禁止；标题用 Pillow 后处理。

## Layout

```text
photo-to-poster/
  README.md
  prompt-catalog.json
  prompts/
    base-prompt.md
    01-minimal-abstract.md … 12-photogravure.md
```

## Scripts

Run from skill root:

```bash
python scripts/photo_to_poster/inspect_photo.py --input <photo> --photo-id photo-001
python scripts/photo_to_poster/compose_poster.py --photo <photo> --art <art.png> --output posters/photo-001-poster.png --ratio-top 0.5
python scripts/photo_to_poster/validate_poster.py posters/*.png
python scripts/photo_to_poster/export_posters.py --posters-dir posters --zip final-export.zip --project-name demo
```

Image **generation** depends on host tools. These scripts do not invent APIs.

## Local output (gitignored)

```text
.idea-to-visual/photo-to-poster-output/<project-name>/
  source/
  generated-panels/
  posters/
  manifest.json
  final-export.zip
```

Do not commit user photos or finished posters to the public GitHub repo.

## Catalog

See `prompt-catalog.json` for style ids, ratios, recommended photo types, and prompt paths.
