# Yihang Idea to Visual

[English](README.en.md) | 简体中文

**Skill 名称：** `yihang-idea-to-visual`  
**显示名称：** Yihang Idea to Visual  
**产品定位：** Idea to Visual — AI 个人 IP 图文创作 Skill  
**GitHub：** [https://github.com/dxl11/yihang-idea-to-visual](https://github.com/dxl11/yihang-idea-to-visual)

从一句原始想法出发，通过分阶段确认，完成思想整理、文章润色、标题创作、封面设计、图文排版、视觉审核，并交付按发布顺序命名的封面/正文 PNG 与 ZIP。

这是符合 [Agent Skills](https://agentskills.io/specification) 标准的**单一 Skill**，不是 Agent、不是多 Agent 团队、不是 MCP Server，也不是 Web 应用。

---

## 1. 项目名称和介绍

**Yihang Idea to Visual** 把个人表达的生产链路产品化：用户专注思考与表达，AI 在同一 Skill 内完成编辑、设计、排版与打包。

仓库内 Skill 主文件：

```text
.agents/skills/yihang-idea-to-visual/SKILL.md
```

## 2. 项目核心定位

面向需要持续输出个人 IP 图文的创作者、研究者与经营者。每次创作只选择一个发布平台、使用同一画布尺寸，输出可直接上传社交媒体的图片组。

核心理念：让用户专注于思考和表达，让 AI 负责编辑、设计、排版和制作。

## 3. 核心功能

- 六阶段门禁工作流（文章 → 标题 → 封面 → 图文 → 审核 → 交付）
- 锁定文章后的原文完整性保护（禁止擅自删改/总结）
- 平台配置与 Skill 指令分离
- 视觉参考库索引、联系表、多图特征组合参考
- 三层品牌系统：长期身份 / 长期偏好 / 项目风格
- Pillow 精确中文排版（与图像生成分离）
- 项目状态可恢复（`.idea-to-visual/projects/`，本地私有）
- ZIP 顺序交付与自动化校验

## 4. 一键安装命令

使用 [Vercel Skills CLI](https://github.com/vercel-labs/skills)（`npx skills`）。**不要**手动下载或复制 `SKILL.md`。

### 环境要求

- Node.js **22.20** 或更高版本
- npm
- npx
- Cursor

环境检查：

```bash
node -v
npm -v
```

### Cursor 项目级安装（推荐协作）

```bash
npx skills add dxl11/yihang-idea-to-visual --skill yihang-idea-to-visual -a cursor
```

安装到当前项目，仅供当前项目使用，适合项目协作。

### Cursor 全局安装

```bash
npx skills add dxl11/yihang-idea-to-visual --skill yihang-idea-to-visual -a cursor -g
```

安装到用户全局目录，可在多个项目中使用。

### 查看仓库中的可安装 Skill

```bash
npx skills add dxl11/yihang-idea-to-visual --list
```

### 非交互安装（CI / 脚本）

```bash
npx skills add dxl11/yihang-idea-to-visual --skill yihang-idea-to-visual -a cursor -y
```

本地源码发现（开发者）：

```bash
npx skills add . --list
```

## 5. Cursor 项目级和全局安装

| 范围 | 命令 | 典型路径 |
|---|---|---|
| 项目级 | 不加 `-g` | 当前项目 `.agents/skills/yihang-idea-to-visual/` |
| 全局 | 加 `-g` | `~/.cursor/skills/yihang-idea-to-visual/` |

安装后会一并带上 `references/`、`scripts/`、`schemas/`、`assets/`（含视觉参考库与品牌样本）。相对路径引用在安装后仍然有效。

**不会**为 Cursor 再复制一套到 `.cursor/skills/`（项目级安装目标就是 Cursor 使用的 `.agents/skills/`）。

### 查看已安装的 Skills

```bash
npx skills list
```

查看 Cursor 对应的 Skill：

```bash
npx skills ls -a cursor
```

### 如何验证安装

1. 确认存在：`.agents/skills/yihang-idea-to-visual/SKILL.md`（项目级）或全局 Cursor skills 目录中的同名文件夹。  
2. Frontmatter 中 `name` 为 `yihang-idea-to-visual`。  
3. `references/`、`scripts/`、`schemas/`、`assets/` 齐全。  
4. 在 Cursor Agent 对话中输入 `/yihang-idea-to-visual`，或描述「把想法做成图文轮播」。

### 安装成功后如何使用

1. 用 Cursor 打开已安装该 Skill 的项目。  
2. 在 Agent 中调用 `/yihang-idea-to-visual` 或直接描述创作需求。  
3. 按六阶段逐步确认；需要时 Agent 会运行 Skill 内的 Python 脚本（需本机 Python 3.10+ 与 Pillow）。

辅助依赖（排版/校验脚本，可选但推荐）：

```bash
python -m pip install "Pillow>=10" 
```

## 6. 完整创作工作流

1. **STEP 01 思想整理与文章润色** — 保留作者立场与表达习惯，确认后锁定文章。  
2. **STEP 02 标题创作** — 基于锁定文章给出 5 个差异化标题方向。  
3. **STEP 03 封面设计** — 选择单一平台；至多 3 个关键视觉问题；3 套结构差异封面预览。  
4. **STEP 04 图文设计** — 按语义分页；三套正文风格预览后批量生成；文字放不下就加页，不删文。  
5. **STEP 05 整体审核与局部修改** — 缩略图总览；单页/多页/全局修改；改文必须回到文章阶段。  
6. **STEP 06 质量检查与最终交付** — 校验通过后输出 `00-cover.png`、`01-page.png`… 与 `final-export.zip`。

未确认阶段不得跳过；新对话应读取项目 `state.json` 续作。

## 7. 视觉参考库介绍

目录：`.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/`

- 支持 PNG / JPG / JPEG / WEBP 等常见格式  
- 按分类目录存放；私有图放入 `private/`（gitignore）  
- 索引：`scripts/build_reference_index.py`  
- 联系表：`scripts/create_contact_sheet.py`  
- 未知授权图片仅可内部视觉分析，不得默认公开再分发  

详见 [visual-reference-library/README.md](.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/README.md)。

## 8. 个人品牌视觉系统

三层配置，互不混淆：

1. **长期品牌身份** — 稳定识别规范  
2. **个人视觉偏好** — 长期喜好；更新须用户明确同意  
3. **当前项目风格** — 单篇作品可变  

样本：[brand-profile.sample.json](.agents/skills/yihang-idea-to-visual/assets/brand-kit/brand-profile.sample.json)  
真实 Logo / 偏好放入 `assets/brand-kit/private/`（不提交）。无品牌名时使用中性设计，不要虚构品牌。

## 9. 使用示例

```text
用户：帮我用 Yihang Idea to Visual，把这段笔记做成小红书图文。
AI：进入 STEP 01，整理文章 → 确认锁定 → 询问是否进入标题创作……
```

平台配置：[profiles.json](.agents/skills/yihang-idea-to-visual/assets/platform-profiles/profiles.json)  
脚本示例：

```bash
python .agents/skills/yihang-idea-to-visual/scripts/build_reference_index.py --help
python .agents/skills/yihang-idea-to-visual/scripts/render_pages.py --list-templates
python .agents/skills/yihang-idea-to-visual/scripts/validate_project.py --help
python .agents/skills/yihang-idea-to-visual/scripts/package_export.py --help
```

## 10. 更新与卸载

### 检查更新

```bash
npx skills check
```

### 更新项目级 Skill

```bash
npx skills update yihang-idea-to-visual
```

### 更新全局 Skill

```bash
npx skills update yihang-idea-to-visual -g
```

### 卸载项目级 Skill

```bash
npx skills remove yihang-idea-to-visual -a cursor
```

### 卸载全局 Skill

```bash
npx skills remove yihang-idea-to-visual -a cursor -g
```

> 以上命令使用 Skills CLI 当前正式参数。若官方 CLI 变更，以 [commands.md](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) 为准。

### 安装常见问题

**Q: `npx skills` 报 Node 版本过低？**  
请升级到 Node.js 22.20+。

**Q: Cursor 里找不到 Skill？**  
确认安装目标为 `-a cursor`，并重启 Cursor / 重新打开项目；项目级路径应为 `.agents/skills/yihang-idea-to-visual/SKILL.md`。

**Q: 需要手动复制文件吗？**  
不需要。一律使用 `npx skills add ...`。

**Q: 会不会装出两套重复 Skill？**  
项目级 Cursor 安装到 `.agents/skills/`；本仓库源码也位于该路径。请勿再手工复制到 `.cursor/skills/`。

**Q: 排版脚本乱码？**  
配置本机已授权的中文字体路径；缺失字体会明确报错，不会静默输出乱码。

## 11. 项目目录

```text
yihang-idea-to-visual/
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

私人项目数据请放在 `.idea-to-visual/projects/`（已被 gitignore）。

## 12. 贡献指南

见 [CONTRIBUTING.md](CONTRIBUTING.md)。提交前请运行：

```bash
python -m pytest
```

欢迎改进文档、平台配置、脚本与测试；请保持 Skill 名称为 `yihang-idea-to-visual`，且不要提交私人内容。

## 13. 版权与隐私说明

- 代码与文档：MIT（见 [LICENSE](LICENSE)）  
- 图片 / 字体 / Logo：见 [ASSET-LICENSES.md](ASSET-LICENSES.md)  
- 不提交私人文章、私有参考图、私有品牌包、API Key / Token / 凭证  
- 不打包未授权第三方字体与图片  
- 未知授权参考图仅可内部分析  

### 当前版本限制

- 不内置云端图像生成 API  
- 平台尺寸为可配置默认值，需按需核验官方来源  
- 参考库视觉语义分析依赖宿主读图能力  
- 中文渲染效果依赖本机字体  

---

仓库地址：[https://github.com/dxl11/yihang-idea-to-visual](https://github.com/dxl11/yihang-idea-to-visual)
