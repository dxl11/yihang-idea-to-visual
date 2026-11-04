# Idea to Visual（Yihang Idea to Visual）

[English](README.en.md) | 简体中文

**Skill 标识：** `yihang-idea-to-visual`  
**产品名称：** Idea to Visual / Yihang Idea to Visual  
**仓库名称：** `idea-to-visual`（GitHub 仓库名可保持不变）

从一句原始想法出发，通过多轮确认，完成思想整理、文章润色、标题创作、封面设计、图文排版、视觉审核，并交付按发布顺序命名的封面/正文 PNG 与 ZIP 压缩包。

这是一个符合 [Agent Skills](https://agentskills.io/specification) 标准的**单一 Skill**，不是 Agent、不是多 Agent 团队、不是 MCP Server，也不是 Web 应用。

---

## 1. 项目介绍

Yihang Idea to Visual 把个人表达的生产链路产品化：用户专注思考与表达，AI 在同一 Skill 内完成编辑、设计、排版与打包。项目级安装路径为：

```text
.agents/skills/yihang-idea-to-visual/SKILL.md
```

Cursor 会自动发现 `.agents/skills/` 下的 Skill；也可通过聊天中的 `/yihang-idea-to-visual` 手动调用。

## 2. 产品定位

面向需要持续输出个人 IP 图文内容的创作者、研究者与经营者。每次创作只选择一个发布平台、使用同一画布尺寸，输出可直接上传社交媒体的图片组。

## 3. 功能特点

- 六阶段门禁工作流（文章 → 标题 → 封面 → 图文 → 审核 → 交付）
- 锁定文章后的**原文完整性保护**（禁止擅自删改/总结）
- 平台配置与 Skill 指令分离（`assets/platform-profiles/profiles.json`）
- 视觉参考库索引、联系表、多图特征组合参考
- 三层品牌系统：长期身份 / 长期偏好 / 项目风格
- Pillow 精确中文排版（与图像生成分离）
- 项目状态可恢复（`.idea-to-visual/projects/`）
- ZIP 顺序交付与自动化校验

## 4. 完整工作流程

1. **STEP 01 思想整理与文章润色** — 保留作者立场与表达习惯，确认后锁定文章。  
2. **STEP 02 标题创作** — 基于锁定文章给出 5 个差异化标题方向。  
3. **STEP 03 封面设计** — 选择单一平台，提出至多 3 个关键视觉问题，输出 3 套结构差异明显的封面预览。  
4. **STEP 04 图文设计** — 按语义分页；三套正文风格预览后批量生成；文字放不下就加页，不删文。  
5. **STEP 05 整体审核与局部修改** — 缩略图总览；单页/多页/全局修改；改文必须回到文章阶段。  
6. **STEP 06 质量检查与最终交付** — 校验通过后输出 `00-cover.png`、`01-page.png`… 与 `final-export.zip`。

未确认阶段不得跳过；新对话应读取 `state.json` 续作。

## 5. 项目目录

```text
idea-to-visual/
├── README.md / README.en.md
├── LICENSE / ASSET-LICENSES.md / CONTRIBUTING.md / CHANGELOG.md
├── pyproject.toml / .gitignore
├── .github/workflows/validate.yml
├── .agents/skills/yihang-idea-to-visual/
│   ├── SKILL.md
│   ├── references/
│   ├── scripts/
│   ├── schemas/
│   └── assets/
├── examples/
└── tests/
```

私人项目数据请放在仓库根目录的 `.idea-to-visual/projects/`（已被 gitignore）。

## 6. 安装方法

```bash
git clone <your-fork-or-repo-url> idea-to-visual
cd idea-to-visual
python -m pip install -e ".[dev]"
```

依赖：Python 3.10+、Pillow。开发/CI 另需 pytest、jsonschema。

## 7. 在 Cursor 中使用

1. 用 Cursor 打开本仓库根目录。  
2. Cursor 自动从 `.agents/skills/yihang-idea-to-visual/` 发现 Skill。  
3. 在 Agent 对话中描述想法，或输入 `/yihang-idea-to-visual`。  
4. 按阶段确认；需要时 Agent 会执行 `scripts/` 下的辅助脚本。  

说明：Cursor 同时兼容 `.cursor/skills/`，本项目**只维护** `.agents/skills/` 一份，避免重复拷贝。

个人全局安装可将该 Skill 目录复制到 `~/.agents/skills/yihang-idea-to-visual/` 或 `~/.cursor/skills/yihang-idea-to-visual/`。

## 8. 其他 Agent Skills 工具

凡支持 [agentskills.io](https://agentskills.io/specification) 的工具，通常只需：

1. 将 `yihang-idea-to-visual` 目录放到其 Skill 发现路径；  
2. 保证 frontmatter 的 `name` 与目录名同为 `yihang-idea-to-visual`；  
3. 提供 Python + Pillow 以便运行脚本。

Claude Code / Codex 等若扫描 `.claude/skills` 或 `.codex/skills`，可复制同一目录过去（内容保持一份源，避免分叉）。

## 9. 视觉参考库上传

将图片放入：

`.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/<category>/`

分类：`editorial`、`minimalism`、`technology`、`artistic`、`infographic`、`photography`、`typography`、`miscellaneous`。私有图放入 `private/`（忽略提交）。

详见 [assets/visual-reference-library/README.md](.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/README.md)。

## 10. 参考图索引

```bash
python .agents/skills/yihang-idea-to-visual/scripts/build_reference_index.py \
  --library .agents/skills/yihang-idea-to-visual/assets/visual-reference-library \
  --output .agents/skills/yihang-idea-to-visual/assets/visual-reference-library/catalog.json
```

脚本提取尺寸、哈希、重复项；视觉风格分析需由能读图的 AI 完成，不可仅凭文件名假装理解。

联系表：

```bash
python .agents/skills/yihang-idea-to-visual/scripts/create_contact_sheet.py \
  --library .agents/skills/yihang-idea-to-visual/assets/visual-reference-library \
  --output contact-sheets \
  --category editorial
```

## 11. 个人品牌档案

参考样本：

[brand-profile.sample.json](.agents/skills/yihang-idea-to-visual/assets/brand-kit/brand-profile.sample.json)

真实 Logo / 偏好写入 `assets/brand-kit/private/`（gitignore）。无品牌名也不要虚构名称，使用中性设计继续创作。

长期偏好更新必须经用户明确同意。

## 12. 平台配置

编辑 [profiles.json](.agents/skills/yihang-idea-to-visual/assets/platform-profiles/profiles.json)。每次作品只选一个平台。尺寸字段含 `source` 与 `verified_at`；无法核验时不得冒充“最新官方规范”。

## 13. 图片生成工具依赖

Skill **不是**图像生成 API。插画/摄影/抽象背景仅在宿主环境真实提供图像工具时使用；否则降级为程序化图形 + 本地参考/模板，并明确告知能力边界。

**禁止**把完整中文正文交给图像模型“生成带字图片”。标题与正文由 `render_pages.py` 渲染。

## 14. 中文字体配置

在品牌或 design profile 中设置 `typography.cjk_font_path` 为系统已安装且授权允许的字体路径。缺失时脚本报错退出，不会默默输出乱码。

不要把商业字体打包进本仓库。

## 15. 辅助脚本

| 脚本 | 作用 |
|---|---|
| `scripts/build_reference_index.py` | 参考库索引 |
| `scripts/create_contact_sheet.py` | 联系表 |
| `scripts/render_pages.py` | JSON → PNG 排版 |
| `scripts/validate_project.py` | 项目校验（含原文完整性） |
| `scripts/package_export.py` | 顺序命名 + ZIP |

均支持 `--help`。

## 16. 最终 PNG 与 ZIP 交付

```text
export/<project-name>/
  00-cover.png
  01-page.png
  02-page.png
  ...
final-export.zip
```

交付前必须通过 `validate_project.py`。未通过校验不得标记为最终成品。

## 17. 版权与隐私

- 代码与文档：MIT（见 [LICENSE](LICENSE)）  
- 图片/字体/Logo：见 [ASSET-LICENSES.md](ASSET-LICENSES.md)  
- 用户文章、私有参考图、私有品牌包默认不进 GitHub  
- 未知授权参考图仅可内部分析，不可默认公开再分发

## 18. 常见问题

**Q: 为什么找不到 Skill？**  
确认打开的是仓库根目录，且存在 `.agents/skills/yihang-idea-to-visual/SKILL.md`。

**Q: 可以一次导出多种尺寸吗？**  
不可以。单次项目单一平台、单一画布。

**Q: 没有图像生成工具怎么办？**  
仍可完成文案、标题、结构化排版 PNG；插画层降级并说明限制。

**Q: 旧名称 `idea-to-visual` 还能用吗？**  
产品可称 Idea to Visual；**Skill 标识必须是** `yihang-idea-to-visual`。

## 19. 当前版本限制

- 不内置云端图像生成密钥/API  
- 平台尺寸为可配置默认值，需按需核验官方来源  
- 参考库视觉语义分析依赖宿主读图能力  
- 中文效果依赖本机字体

## 20. 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。提交前请运行：

```bash
python -m pytest
```

---

## 快速验收清单

- [x] 单一 Skill：`yihang-idea-to-visual`
- [x] 标准 `SKILL.md` + references
- [x] 五个可运行脚本 + 测试
- [x] 中英文 README
- [x] LICENSE / ASSET-LICENSES / gitignore / CI
