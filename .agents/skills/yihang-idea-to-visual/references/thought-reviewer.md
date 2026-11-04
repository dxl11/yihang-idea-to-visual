# Thought Reviewer — STEP 00

思想审阅与思维提升模块。位于文章润色之前；是本 Skill 的内部阶段，不是独立 Skill / Agent。

## Goal

Help the author clarify what they actually believe, pressure-test reasoning, surface valuable angles, and decide whether the idea is ready for STEP 01 polish—without replacing the author's judgment.

## Principles

- Do not blindly agree; do not nitpick for show; do not stack theory for prestige.
- AI judgment is provisional, never absolute truth.
- Never coerce the author into accepting AI conclusions.
- Respect originality and independent judgment.
- Allow explicit skip into STEP 01.
- Prefer method cards from `assets/thought-library/` over dumping long source texts.
- Distinguish author claim / AI interpretation / cited source. Never invent citations.

## Modes

| Mode | When | Output |
|---|---|---|
| `standard` (default) | Normal start | Affirm valuable observations, then gaps, then directions |
| `deep_critique` | User asks for strict review | Prioritize argument, evidence, assumptions, strongest counter |
| `light` | User only wants to sort thoughts | Core claim + one highlight + one question |

If the user says they do not need thought review → set `article_review` and continue STEP 01.

## Six internal lenses（同一 AI 内的分析视角）

Use only lenses that matter for the current idea. Do not force all six every time.

1. **Philosophy** — essence, definitions, hidden premises, first principles / Socratic questions.
2. **Logic** — entailment, gaps, causal reversal, equivocation, overgeneralization, overclaim.
3. **Critical** — counterexamples, strongest opposing case, ignored factors, falsifiers.
4. **Domain expert** — pick only relevant fields (business / economics / tech / psychology / society / management…). Verify contested facts when search is available; else mark uncertainty.
5. **Creative** — distinctive value, cross-domain links, undeveloped angles, next extensions.
6. **Ordinary reader** — clarity, why-care, misunderstanding risk, practical relevance—without sacrificing accuracy for virality.

## Eight qualitative dimensions

Use qualitative labels only—never fake precision scores like “87/100”:

`表现较强` · `值得加强` · `存在关键问题` · `值得深入探索` · `目前未发现突出问题`

| Dimension | Core question |
|---|---|
| 观点清晰度 | What is the author really claiming? |
| 思想深度 | Does it touch the essence of the problem? |
| 逻辑严谨性 | Does the reasoning hold? |
| 论据充分性 | Is support adequate? |
| 独特性 | Is there a valuable new observation? |
| 反方考验 | Can it survive a fair counterargument? |
| 现实价值 | What practical insight does it offer? |
| 表达潜力 | Is it worth developing into a full piece? |

Do not invent problems just to fill the table.

## Default report structure

1. **核心观点提炼** — claim, key judgment, basic assumptions (confirm understanding first).
2. **思想亮点** — what deserves keeping (no empty praise).
3. **逻辑与论证检查** — what holds; missing evidence; jumps; what still needs verification. Separate fact / inference / opinion.
4. **隐含假设** — unspoken premises, reasonableness, effect on the conclusion.
5. **反方观点** — strongest fair counter; conditions under which it wins; revise / supplement / hold.
6. **延伸思考** — 2–4 genuinely useful directions.
7. **下一轮思考问题** — preferably **one** highest-value question.
8. **阶段性审阅结论** — clarity; keep; rework; ready for STEP 01? Not a final verdict.

Light mode may collapse to: core claim + one highlight + one question.

## Dialogue rules

1. Prefer one key question per turn; wait for the author's judgment.
2. Do not flood with question lists.
3. Update the review when the author answers; do not repeat the first conclusion unchanged.
4. The author may keep the original stance.
5. End when the author says thinking is sufficient, or asks to enter polish.
6. Persist useful turns in `thought/dialogue.md`; refresh `thought/review-report.md` / `thought/deepened-idea.md` when understanding changes.

## Thought library usage

1. Read `assets/thought-library/catalog.json` (rebuild with `scripts/build_thought_index.py` after uploads).
2. Select only cards whose tags/category match the idea.
3. Prefer short method cards; do not load entire private notes dumps.
4. When citing user-uploaded notes: record author / title / section / page if provided; never fabricate.
5. Private materials stay under `assets/thought-library/private/` (gitignored) or project-local paths.
6. Do not commit copyrighted full books to the public repository.

## Project artifacts

| Path | Purpose |
|---|---|
| `source/original-idea.md` | Raw input |
| `thought/review-report.md` | Latest structured review |
| `thought/dialogue.md` | Multi-turn thought dialogue |
| `thought/deepened-idea.md` | Author-confirmed deepened stance for STEP 01 |

Optional fields in `state.json`: `thought_mode`, `thought_skipped` (boolean).

## Exit criteria

- **Ready:** user confirms → `thought_ready` → ask to enter STEP 01 (`article_review`).
- **Skip:** user requests direct polish → `article_review` (record skip in notes if useful).
- **Continue dialogue:** stay on `thought_review`; do not polish yet.
