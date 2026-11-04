# Thinking Frameworks Index

Executable method index for Thought Reviewer. Prefer these short cards over large raw texts.

Full library: [assets/thought-library/](../assets/thought-library/)  
Rebuild catalog: `python scripts/build_thought_index.py --library assets/thought-library --output assets/thought-library/catalog.json`

## How to retrieve

1. Identify topic keywords from the author's idea.
2. Open `catalog.json` and filter by `category` / `tags` / `best_for`.
3. Load **2–6** matching method cards maximum.
4. Apply methods as lenses; do not paste whole cards into the user-facing report unless helpful.
5. If a private expert note is cited, quote only the needed fragment and keep source metadata.

## Seed methods (public)

### Philosophy & logic

| Card | Path | Use when |
|---|---|---|
| Socratic questioning | `philosophy/socratic-questioning.md` | Clarify definitions and hidden goals |
| Conceptual analysis | `philosophy/conceptual-analysis.md` | Ambiguous key terms |
| First principles | `philosophy/first-principles.md` | Rebuild from basics |
| Deductive reasoning | `logic/deductive-reasoning.md` | Check entailment |
| Inductive reasoning | `logic/inductive-reasoning.md` | Generalization from cases |
| Falsificationism | `logic/falsificationism.md` | Seek disconfirming tests |

### Critical thinking

| Card | Path | Use when |
|---|---|---|
| Reverse thinking | `critical-thinking/reverse-thinking.md` | Invert the claim |
| Counterexample test | `critical-thinking/counterexample-test.md` | Find breaking cases |
| Cognitive bias check | `critical-thinking/cognitive-bias-check.md` | Spot bias patterns |
| Causal analysis | `critical-thinking/causal-analysis.md` | Cause vs correlation |
| Premise check | `critical-thinking/premise-check.md` | Stress-test assumptions |

### Business & economics

| Card | Path | Use when |
|---|---|---|
| Multiple mental models | `business/multiple-mental-models.md` | Avoid single-lens decisions |
| Opportunity cost | `economics/opportunity-cost.md` | Trade-offs |
| Incentive analysis | `economics/incentive-analysis.md` | Behavior under incentives |
| Comparative advantage | `economics/comparative-advantage.md` | Specialization claims |
| Network effects | `business/network-effects.md` | Platform / scale dynamics |
| Moat analysis | `business/moat-analysis.md` | Durable advantage claims |

### Science & systems

| Card | Path | Use when |
|---|---|---|
| Systems thinking | `systems-thinking/systems-thinking.md` | Interacting parts |
| Feedback loops | `systems-thinking/feedback-loops.md` | Reinforcing / balancing loops |
| Complex systems | `systems-thinking/complex-systems.md` | Non-linear / emergent behavior |
| Leverage points | `systems-thinking/leverage-points.md` | Where intervention matters |
| Probabilistic thinking | `science/probabilistic-thinking.md` | Uncertainty & base rates |

### Creativity & psychology

| Card | Path | Use when |
|---|---|---|
| Lateral thinking | `creativity/lateral-thinking.md` | Escape habitual frames |
| Cross-disciplinary links | `creativity/cross-disciplinary-links.md` | Transfer insights |
| Analogical reasoning | `creativity/analogical-reasoning.md` | Structure mapping |
| Combinatorial innovation | `creativity/combinatorial-innovation.md` | Recombine parts |
| Reader empathy | `psychology/reader-empathy.md` | Ordinary-reader clarity |

## Uploading expert materials

1. Place private notes under `assets/thought-library/private/` (gitignored) or a project-local path.
2. Prefer extracting a **method card** (when_to_use / steps / caveats / source) instead of dumping full books.
3. Fill source metadata: author, title, section, page, license, attribution.
4. Re-run `build_thought_index.py`.
5. Never commit copyrighted full books to the public GitHub repository.
6. Distinguish source wording from AI paraphrase in any citation.

## Extension rule

New cards are welcome under the category folders or `miscellaneous/`. Keep each card short, actionable, and source-honest.
