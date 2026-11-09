<p align="center">
  <img src="docs/assets/readme-banner.png" alt="Idea to Visual — 暗房中，想法显影为可发布图文" width="100%" />
</p>

<p align="center">
  <strong>Yihang Idea to Visual</strong><br/>
  <em>想法在暗房里显影 · 一次安装 · 一条创作链路</em>
</p>

<p align="center">
  <a href="README.en.md">English</a> · 简体中文 ·
  <a href="https://github.com/dxl11/yihang-idea-to-visual">GitHub</a> ·
  <a href="https://agentskills.io/specification">Agent Skills</a>
</p>

---

> **TIMER CARD — 现在安装（Cursor 项目级）**
>
> ```bash
> npx skills add dxl11/yihang-idea-to-visual --skill yihang-idea-to-visual -a cursor
> ```
>
> Node.js **22.20+** · 不要手动复制 `SKILL.md`

全局安装加 `-g`。非交互加 `-y`。详见下方第 4–5 节。

---

**Idea to Visual** 把一句原始想法，经 Thought Reviewer 深化，再分阶段完成润色、标题、封面、图文排版与审核，最终交付按发布顺序命名的封面 / 正文 PNG 与 ZIP。

这是符合 [Agent Skills](https://agentskills.io/specification) 标准的**单一 Skill**（`yihang-idea-to-visual`）——不是 Agent、不是多 Agent 团队、不是 MCP Server，也不是 Web 应用。Thought Reviewer 是 Skill 内部模块，不是独立 Skill。

| 暗房工位 | 创作阶段 | 你得到什么 |
|---|---|---|
| **EXPOSE** | Thought Reviewer | 观点被理解、审阅、可跳过 |
| **DEVELOP** | 文章润色 | 立场保留，表达变清楚 |
| **FIX** | 文章锁定 | 原文完整性保护，禁止擅自删改 |
| **WASH** | 标题 · 封面 · 图文 | 单一平台、同一画布尺寸 |
| **DRY** | 审核 · 交付 | `00-cover.png` … + `final-export.zip` |

核心理念：**你专注思考与表达；AI 负责审阅、编辑、设计、排版与打包。**

---

## 1. 项目名称和介绍

**Yihang Idea to Visual** 把个人表达的生产链路产品化。

仓库内 Skill 主文件：

```text
.agents/skills/yihang-idea-to-visual/SKILL.md
```

## 2. 项目核心定位

面向需要持续输出个人 IP 图文的创作者、研究者与经营者。每次创作只选择一个发布平台、使用同一画布尺寸，输出可直接上传社交媒体的图片组。

## 3. 核心功能

- Thought Reviewer：思想审阅、多轮对话、可跳过
- 七阶段门禁工作流（思想审阅 → 文章 → 标题 → 封面 → 图文 → 审核 → 交付）
- **Photo-to-Poster**：照片驱动艺术海报（一张照片一张独立 3:4 PNG；上半区原图像素合成）
- 锁定文章后的原文完整性保护（禁止擅自删改/总结）
- 平台配置与 Skill 指令分离
- 思想知识库（方法卡片检索）与视觉参考库
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
3. 默认先进入 Thought Reviewer；可要求跳过并直接润色。之后按阶段确认；需要时 Agent 会运行 Skill 内的 Python 脚本（需本机 Python 3.10+ 与 Pillow）。

辅助依赖（排版/校验脚本，可选但推荐）：

```bash
python -m pip install "Pillow>=10"
```

## 6. Thought Reviewer（思想审阅）

> **EXPOSE** — 润色之前，先让观点在安全灯下显影。

许多想法在润色前尚未想清楚。Thought Reviewer 先帮助理解真实观点，再从多视角审阅，而不是立刻改写成漂亮文章。

### 六种审阅视角（同一 Skill 内的分析镜头）

1. 哲学思考  
2. 逻辑分析  
3. 批判性思考  
4. 领域专家（按主题动态选择，不固定全开）  
5. 创新思考  
6. 普通读者  

### 八维审阅标准（定性，不要虚假精确打分）

观点清晰度、思想深度、逻辑严谨性、论据充分性、独特性、反方考验、现实价值、表达潜力。

可用标签：表现较强 / 值得加强 / 存在关键问题 / 值得深入探索 / 目前未发现突出问题。

### 思想对话机制

- 每次优先提出**一个**关键问题并等待作者判断  
- 根据新回答更新审阅，而不是重复首轮结论  
- 允许作者坚持原观点；不施压达成 AI 结论  
- 作者可随时结束审阅，或明确要求进入文章润色  

### 三种审阅模式

| 模式 | 说明 |
|---|---|
| 标准模式（默认） | 先肯定有价值观察，再指出问题与方向 |
| 深度批判模式 | 用户主动要求时，优先检验论证、证据、假设与反方 |
| 轻量模式 | 只保留核心观点、一个亮点、一个问题 |

用户明确表示不需要思想审阅时，可直接进入 STEP 01。

### 思想知识库

目录：`.agents/skills/yihang-idea-to-visual/assets/thought-library/`

- 精选方法卡片（哲学 / 逻辑 / 批判 / 商业 / 经济 / 科学 / 心理 / 创新 / 系统思维等）  
- 索引：`scripts/build_thought_index.py` → `catalog.json`  
- 私有专家资料放入 `private/`（gitignore），或放在本地项目目录  
- 优先抽取可执行方法，而不是上传整本书  
- 引用时区分原文与 AI 解释，记录作者 / 书名 / 章节 / 页码；不得伪造出处  
- **不要**把受版权保护的完整书籍提交到公开 GitHub 仓库  

说明详见 [thought-library/README.md](.agents/skills/yihang-idea-to-visual/assets/thought-library/README.md) 与 [thought-reviewer.md](.agents/skills/yihang-idea-to-visual/references/thought-reviewer.md)。

## 7. 完整创作工作流

0. **STEP 00 Thought Reviewer** — 理解观点、多视角审阅、可选多轮对话；可跳过。  
1. **STEP 01 思想整理与文章润色** — 保留作者立场与表达习惯，确认后锁定文章。  
2. **STEP 02 标题创作** — 基于锁定文章给出 5 个差异化标题方向。  
3. **STEP 03 封面设计** — 选定平台；最多 3 个视觉问题；**先检索并真实加载**内置视觉库（空库须明示无图参考），再出三个结构不同的封面；中文标题用 `render_pages.py` 合成。  
4. **STEP 04 图文设计** — 按语义分页；三套正文风格预览后批量生成；文字放不下就加页，不删文。  
5. **STEP 05 整体审核与局部修改** — 缩略图总览；单页/多页/全局修改；改文必须回到文章阶段。  
6. **STEP 06 质量检查与最终交付** — 校验通过后输出 `00-cover.png`、`01-page.png`… 与 `final-export.zip`。

未确认阶段不得跳过（Thought Reviewer 在用户明确要求时可跳过）；新对话应读取项目 `state.json` 续作。

## 8. 视觉参考库介绍

目录：`.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/`

这是 Skill 作者维护的**内置视觉灵感参考库**。当前阶段**尚未收录图片**，只预留分类目录与空 `catalog.json`（`total_assets: 0`）。

### 当前如何使用（空库）

- 封面 STEP 03 必须运行 `retrieve_cover_references.py` 检索并验真。  
- 空库 → **明示无图参考**，可仅用品牌规范与封面规则继续三方案设计。  
- 有匹配 → 将已验证绝对路径传入宿主图像工具原生参考输入（路径写进 Prompt ≠ 已加载）。  
- **不得**假装存在尚未上传的参考图。

### 以后如何添加素材

1. 将 PNG / JPG / JPEG / WEBP / SVG 放入对应分类目录（`editorial/`、`cover-design/`、`carousel-layout/`、`color-palettes/` 等）。  
2. 为每张图准备唯一编号，并记录来源、作者、授权。  
3. 运行：`python .agents/skills/yihang-idea-to-visual/scripts/build_reference_index.py --full`  
4. 由可读图的 Agent 补充排版 / 字体 / 色彩 / 构图分析。  
5. 交叉分类用 `tags`，不必复制同一文件到多个目录。  

私有或未知授权图片放入 `private/`（gitignore）；仅可内部分析，不得直接用于最终作品或公开再分发。

索引 / 检索 / 联系表：`build_reference_index.py` · `retrieve_cover_references.py` · `create_contact_sheet.py`  

详见 [visual-reference-library/README.md](.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/README.md)。

## 8.5 Photo-to-Poster（照片艺术海报）

上传一张或多张照片，按 12 种艺术风格 Recipe 逐张生成独立竖版海报（默认 **1080×1440 / 3:4**）。

硬规则：一张照片一张海报；禁止拼贴/九宫格/多图合并；上半区用原图像素，下半区才是艺术生成；多张照片即使同风格也要分别调用生成任务。

流程：分析照片 → 推荐 3 个风格 → 用户选择（整批同风格或单张覆盖）→ 逐张生成与合成 → 单张重生不影响其他 → ZIP 打包。

资源：`assets/photo-to-poster/` · 说明：[photo-to-poster.md](.agents/skills/yihang-idea-to-visual/references/photo-to-poster.md)  
脚本：`scripts/photo_to_poster/inspect_photo.py` · `compose_poster.py` · `validate_poster.py` · `export_posters.py`  
本地输出：`.idea-to-visual/photo-to-poster-output/`（不提交公开仓库）  
图像生成依赖宿主可用工具；不可用时须明确说明，不得虚构 API。

## 9. 个人品牌视觉系统

三层配置，互不混淆：

1. **长期品牌身份** — 稳定识别规范  
2. **个人视觉偏好** — 长期喜好；更新须用户明确同意  
3. **当前项目风格** — 单篇作品可变  

样本：[brand-profile.sample.json](.agents/skills/yihang-idea-to-visual/assets/brand-kit/brand-profile.sample.json)  
真实 Logo / 偏好放入 `assets/brand-kit/private/`（不提交）。无品牌名时使用中性设计，不要虚构品牌。

## 10. 使用示例

```text
用户：帮我用 Yihang Idea to Visual，把这段笔记做成小红书图文。
AI：进入 STEP 00 Thought Reviewer，先提炼观点并提出一个关键问题……
用户：先跳过审阅，直接润色。
AI：进入 STEP 01，整理文章 → 确认锁定 → 询问是否进入标题创作……
```

平台配置：[profiles.json](.agents/skills/yihang-idea-to-visual/assets/platform-profiles/profiles.json)  
脚本示例：

```bash
python .agents/skills/yihang-idea-to-visual/scripts/build_thought_index.py --help
python .agents/skills/yihang-idea-to-visual/scripts/build_reference_index.py --help
python .agents/skills/yihang-idea-to-visual/scripts/render_pages.py --list-templates
python .agents/skills/yihang-idea-to-visual/scripts/validate_project.py --help
python .agents/skills/yihang-idea-to-visual/scripts/package_export.py --help
```

## 11. 更新与卸载

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

## 12. 项目目录

```text
yihang-idea-to-visual/
├── README.md / README.en.md
├── docs/assets/readme-banner.png
├── LICENSE / ASSET-LICENSES.md / CONTRIBUTING.md / CHANGELOG.md
├── pyproject.toml / .gitignore
├── .github/workflows/validate.yml
├── .agents/skills/yihang-idea-to-visual/
│   ├── SKILL.md
│   ├── references/          # 含 thought-reviewer.md
│   ├── scripts/             # 含 build_thought_index.py
│   ├── schemas/
│   └── assets/
│       ├── thought-library/
│       └── visual-reference-library/
├── examples/
└── tests/
```

私人项目数据请放在 `.idea-to-visual/projects/`（已被 gitignore）。私人思想资料放在 `assets/thought-library/private/`。

## 13. 贡献指南

见 [CONTRIBUTING.md](CONTRIBUTING.md)。提交前请运行：

```bash
python -m pytest
```

欢迎改进文档、平台配置、脚本与测试；请保持 Skill 名称为 `yihang-idea-to-visual`，且不要提交私人内容。

## 14. 版权与隐私说明

- 代码与文档：MIT（见 [LICENSE](LICENSE)）  
- 图片 / 字体 / Logo：见 [ASSET-LICENSES.md](ASSET-LICENSES.md)  
- Banner：`docs/assets/readme-banner.png` 为本项目生成的暗房主题示意图，MIT  
- 不提交私人文章、私有参考图、私有思想笔记、私有品牌包、API Key / Token / 凭证  
- 不打包未授权第三方字体、图片或完整受版权保护书籍  
- 未知授权参考图仅可内部分析  
- 思想知识库引用必须可追溯；未经核实不得伪造出处  

### 当前版本限制

- 不内置云端图像生成 API  
- 平台尺寸为可配置默认值，需按需核验官方来源  
- 参考库视觉语义分析依赖宿主读图能力  
- 中文渲染效果依赖本机字体  
- Thought Reviewer 依赖宿主 Agent 的推理与可选检索能力；知识库不会自动“读完整书架”  

---

<p align="center">
  <a href="https://github.com/dxl11/yihang-idea-to-visual">github.com/dxl11/yihang-idea-to-visual</a>
</p>
