# Visual Reference Library（内置视觉灵感参考库）

这是 Skill 作者维护的 **Yihang Idea to Visual** 内置视觉灵感库，供封面设计与图文设计阶段作参考分析与特征组合，**不是**可直接粘贴进最终作品的素材包。

## 当前状态

**素材库为空。** 本仓库只预留分类目录与空索引，尚未收录任何图片。

`catalog.json` 中 `total_assets` / `assets` / `items` 均为 0。空库时封面流程必须**明示无图参考**，可按品牌与封面规则继续三方案设计，不得假装已加载参考图。

## 目录分类

| 目录 | 用途 |
|---|---|
| `editorial/` | 杂志 / 编辑排版灵感 |
| `minimalism/` | 极简构图 |
| `technology/` | 科技 / AI 视觉语言 |
| `artistic/` | 艺术 / 手感 / 插画气质 |
| `infographic/` | 信息图 / 流程示意 |
| `typography/` | 大字报 / 字体主导海报 |
| `cover-design/` | 封面结构参考 |
| `carousel-layout/` | 轮播分页 / 多页节奏 |
| `photography/` | 摄影叙事 |
| `color-palettes/` | 配色板 / 色票参考 |
| `private/` | 私有参考（gitignore，不公开发布） |

交叉分类时优先用 `tags` 标注，不必把同一文件复制到多个目录。

## 如何放入图片（未来）

1. 将真实图片放入对应分类目录。  
2. 支持格式：`PNG` / `JPG` / `JPEG` / `WEBP` / `SVG`（索引脚本以光栅图为主；SVG 可人工存放）。  
3. 为每张素材准备唯一编号（建议 `REF-0001` 起，由索引脚本自动分配亦可）。  
4. 必须记录：`source`（来源）、`author`（作者）、`license`（授权）、`attribution`（署名要求）。  
5. 运行索引更新 `catalog.json`。  
6. 由具备读图能力的宿主 Agent 填写排版 / 字体 / 色彩 / 构图分析字段。

## 更新 catalog.json

在 Skill 根目录执行：

```bash
python scripts/build_reference_index.py --library assets/visual-reference-library --output assets/visual-reference-library/catalog.json --full
```

说明：

- 脚本会扫描分类目录中的图片，写入技术元数据（路径、尺寸、哈希、重复检测）。  
- `assets` 与 `items` 保持同步（兼容旧字段）；`total_assets` 与 `stats.total` 反映真实数量。  
- **不会**根据文件名虚构视觉风格分析。  
- 空目录扫描结果仍为 0 条记录。

可选联系表（有素材后）：

```bash
python scripts/create_contact_sheet.py --library assets/visual-reference-library --output contact-sheets --category editorial
```

无素材时联系表脚本会正常退出并提示为空，不生成假图。

## 如何分析图片

当宿主能读取像素时，为每条记录补充：

| 字段 | 内容 |
|---|---|
| `style_notes` | 风格气质 |
| `layout_notes` | 版式 / 网格 |
| `color_notes` | 色彩关系 |
| `typography_notes` | 字体层级与字重 |
| `composition_notes` | 构图与视觉重心 |
| `tags` / `best_for` | 检索标签与适用场景 |
| `analysis_status` | `pending` → 分析完成后改为实际状态 |

不能读图时：明确说明限制，保持 `analysis_status: pending`，**不要编造分析**。

## 封面 / 图文阶段如何调用

封面（STEP 03）必须走素材驱动流程：

```bash
python scripts/retrieve_cover_references.py \
  --library assets/visual-reference-library \
  --query "<主题 标签 气质>" \
  --limit 3 \
  --output <project>/design/cover-ref-manifest.json
```

1. 打开本目录的 `catalog.json`，并运行上述检索脚本。  
2. 若模式为 `empty` → **明确告知无内置参考图**，可仅用品牌规范与封面规则继续；不得假装已加载图片。  
3. 若模式为 `no_match` → 告知无合适匹配；经用户知情后可无图参考继续，不得虚构匹配。  
4. 若模式为 `matched` → 必须用宿主图像工具的**原生图片参考输入**传入已验证的 `absolute_path`（例如 Cursor `GenerateImage.reference_image_paths`）。只把路径写进 Prompt ≠ 已加载。  
5. 可多图组合参考（A 结构 + B 色彩 + C 插画语言），输出必须是原创设计；每个封面方案记录所用 `REF-*`。  
6. **不得**把受版权保护的构图、Logo、角色原样搬进最终交付。  

图文（STEP 04）在空库时可跳过检索；有素材时同样禁止路径伪装。

## 版权与分发

- 未知授权（`license: unknown`）或私有（`private`）图片：**仅可内部视觉分析**，不得用于最终公开作品，也不得当作公开可再分发素材。  
- 不要把未获授权的第三方图提交到公开 GitHub。  
- 私有文件放 `private/`（已被 gitignore）。  
- 详见仓库根目录 [ASSET-LICENSES.md](../../../../../ASSET-LICENSES.md)。

## 预留能力（当前不实现填充）

数据结构与脚本已兼容未来扩展，**现在不必开发**：

- 图片自动分类  
- 批量视觉分析  
- 丰富标签体系  
- 联系表浏览  
- 多图特征组合参考  
- 按文章主题检索灵感  

有真实素材后再逐步启用即可。
