# Thought Library

Executable thinking methods and curated notes for the **Thought Reviewer** module inside Skill `yihang-idea-to-visual`.

This is **not** a dump of copyrighted books. Prefer short method cards that an agent can retrieve selectively.

## Directory layout

| Directory | Suggested content |
|---|---|
| `philosophy/` | Definitions, first principles, Socratic patterns |
| `logic/` | Deduction, induction, falsification |
| `critical-thinking/` | Counterexamples, biases, premise checks |
| `business/` | Moats, network effects, mental models |
| `economics/` | Incentives, opportunity cost, comparative advantage |
| `science/` | Probability and empirical caution |
| `psychology/` | Reader empathy and judgment patterns |
| `creativity/` | Lateral / cross-disciplinary / combinatorial methods |
| `systems-thinking/` | Systems, loops, leverage |
| `miscellaneous/` | Cross-cutting cards and original demo notes |
| `private/` | Private expert notes (gitignored) |

## Card format

Use markdown with optional frontmatter:

```markdown
---
id: TH-XXX-000
title: Method Name
title_zh: 中文名
category: logic
tags:
  - tag-a
best_for:
  - situation
license: MIT
source: Curated method card
author: Your Name
work_title: Optional book/article title
section: Optional chapter
page: Optional page
---

# Method Name

## When to use
...

## Steps
1. ...

## Caveats
...
```

## Build / update index

```bash
python ../scripts/build_thought_index.py --library . --output catalog.json --full
```

Incremental by default. Use `--full` to drop missing paths. Use `--include-private` only on a private machine when you want private notes indexed locally.

## Uploading expert materials

1. Extract actionable methods first; do not assume bulk uploads improve review quality.
2. Keep private / copyrighted full texts under `private/` or outside the public repo.
3. Fill author / title / section / page when citing.
4. Distinguish source wording from AI paraphrase.
5. Never invent citations.
6. Re-run the indexer after adding files.

## Private vs public

| Kind | Location | Git |
|---|---|---|
| Public curated method cards | category folders | may commit |
| Original demo notes | `miscellaneous/` | may commit |
| Private expert notes | `private/` | ignored |
| Copyrighted full books | nowhere in public repo | do not publish |

## Demo assets

The demo expert note in `miscellaneous/` is an original short excerpt for citation tests. It is not a third-party book chapter.
