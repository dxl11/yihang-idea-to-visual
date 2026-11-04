#!/usr/bin/env python3
"""One-shot generator for seed Thought Library method cards."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / ".agents" / "skills" / "yihang-idea-to-visual" / "assets" / "thought-library"


def write_card(rel_path: str, meta: dict, body: str) -> None:
    """Write a method card with YAML-like frontmatter.

    Args:
        rel_path: Path relative to the thought library root.
        meta: Frontmatter fields.
        body: Markdown body.

    Returns:
        None
    """
    path = BASE / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for key, value in meta.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    lines.append(dedent(body).strip())
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", rel_path)


CARDS: list[tuple[str, dict, str]] = [
    (
        "philosophy/socratic-questioning.md",
        {
            "id": "TH-PHI-001",
            "title": "Socratic Questioning",
            "title_zh": "苏格拉底式提问",
            "category": "philosophy",
            "tags": ["questioning", "definitions", "clarification"],
            "best_for": ["unclear goals", "vague claims"],
            "license": "MIT",
            "source": "Classical method summary; curated card for yihang-idea-to-visual",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Socratic Questioning

        ## When to use
        When the author's claim sounds confident but key terms or aims remain fuzzy.

        ## Steps
        1. Ask what the author means by the central term.
        2. Ask what success would look like if the claim were true.
        3. Ask what would count as a counterexample.
        4. Ask whether a simpler restatement still preserves the point.

        ## Caveats
        Do not interrogate endlessly. One precise question often beats five vague ones.

        ## AI interpretation note
        This card paraphrases a classical pedagogical pattern; it is not a quotation from a specific edition.
        """,
    ),
    (
        "philosophy/conceptual-analysis.md",
        {
            "id": "TH-PHI-002",
            "title": "Conceptual Analysis",
            "title_zh": "概念分析",
            "category": "philosophy",
            "tags": ["concepts", "definitions", "ambiguity"],
            "best_for": ["loaded words", "category mistakes"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Conceptual Analysis

        ## When to use
        When a keyword carries multiple meanings.

        ## Steps
        1. List plausible meanings in context.
        2. Pick the meaning the author most likely intends.
        3. Check whether later conclusions switch meaning mid-argument.
        4. Offer a sharper working definition without forcing jargon.

        ## Caveats
        Do not replace the author's vocabulary unless clarity requires it.
        """,
    ),
    (
        "philosophy/first-principles.md",
        {
            "id": "TH-PHI-003",
            "title": "First Principles",
            "title_zh": "第一性原理",
            "category": "philosophy",
            "tags": ["fundamentals", "decomposition", "rebuild"],
            "best_for": ["inherited assumptions", "industry slogans"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # First Principles

        ## When to use
        When the idea rests on industry common sense that may be outdated or borrowed.

        ## Steps
        1. Strip slogans and analogies.
        2. List irreducible facts the author accepts.
        3. Rebuild the claim from those facts only.
        4. Mark which steps reintroduce convention or fashion.

        ## Caveats
        First principles is not a license to ignore empirical context.
        """,
    ),
    (
        "logic/deductive-reasoning.md",
        {
            "id": "TH-LOG-001",
            "title": "Deductive Reasoning",
            "title_zh": "演绎推理",
            "category": "logic",
            "tags": ["entailment", "validity", "argument"],
            "best_for": ["if-then chains", "policy conclusions"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Deductive Reasoning

        ## When to use
        When the author presents premises that supposedly force a conclusion.

        ## Steps
        1. Restate premises explicitly.
        2. Check whether the conclusion is entailed, not merely suggested.
        3. Flag missing premises required for validity.
        4. Separate validity (form) from soundness (truth of premises).

        ## Caveats
        A valid structure can still be empirically false.
        """,
    ),
    (
        "logic/inductive-reasoning.md",
        {
            "id": "TH-LOG-002",
            "title": "Inductive Reasoning",
            "title_zh": "归纳推理",
            "category": "logic",
            "tags": ["generalization", "samples", "evidence"],
            "best_for": ["anecdotes to rules", "trend claims"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Inductive Reasoning

        ## When to use
        When a general rule is inferred from limited cases.

        ## Steps
        1. Identify the sample and the claimed population.
        2. Ask how representative the cases are.
        3. Ask what contrary cases would reduce confidence.
        4. Soften overconfident wording when sample is thin.

        ## Caveats
        More anecdotes are not automatically stronger evidence.
        """,
    ),
    (
        "logic/falsificationism.md",
        {
            "id": "TH-LOG-003",
            "title": "Falsificationism",
            "title_zh": "证伪主义",
            "category": "logic",
            "tags": ["falsify", "testability", "science"],
            "best_for": ["unfalsifiable slogans", "strong predictions"],
            "license": "MIT",
            "source": "Curated method card; not a book excerpt",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Falsificationism

        ## When to use
        When a claim is so flexible that no observation could challenge it.

        ## Steps
        1. Ask what observation would count against the claim.
        2. If none exists, mark the claim as currently untestable rhetoric.
        3. Help the author state a riskier, clearer version.
        4. Prefer risky clarity over safe vagueness when the author wants depth.

        ## Caveats
        Not every valuable reflection must be a scientific hypothesis.
        """,
    ),
    (
        "critical-thinking/reverse-thinking.md",
        {
            "id": "TH-CRT-001",
            "title": "Reverse Thinking",
            "title_zh": "逆向思维",
            "category": "critical-thinking",
            "tags": ["inversion", "counter", "risk"],
            "best_for": ["strategy claims", "success recipes"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Reverse Thinking

        ## When to use
        When the author lists how to succeed; invert to how the idea fails.

        ## Steps
        1. State the claim in one sentence.
        2. Invert: what would make the opposite true?
        3. Collect failure modes that are realistic, not theatrical.
        4. Feed the strongest failure mode back into revision.

        ## Caveats
        Inversion is a probe, not automatic rejection.
        """,
    ),
    (
        "critical-thinking/counterexample-test.md",
        {
            "id": "TH-CRT-002",
            "title": "Counterexample Test",
            "title_zh": "反例检验",
            "category": "critical-thinking",
            "tags": ["counterexample", "boundary", "scope"],
            "best_for": ["universal claims", "always/never wording"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Counterexample Test

        ## When to use
        When wording implies universality.

        ## Steps
        1. Locate absolute language.
        2. Propose one credible counterexample.
        3. Ask whether the claim needs a scope limiter.
        4. Keep the core insight if it survives with narrower scope.

        ## Caveats
        A single exotic edge case may not deserve killing a useful rule of thumb.
        """,
    ),
    (
        "critical-thinking/cognitive-bias-check.md",
        {
            "id": "TH-CRT-003",
            "title": "Cognitive Bias Check",
            "title_zh": "认知偏差识别",
            "category": "critical-thinking",
            "tags": ["bias", "psychology", "judgment"],
            "best_for": ["overconfidence", "survivorship", "confirmation"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Cognitive Bias Check

        ## When to use
        When the argument may be shaped by common judgment traps.

        ## Steps
        1. Scan for confirmation-only evidence.
        2. Check survivorship (only winners mentioned).
        3. Check availability (vivid stories over base rates).
        4. Name the bias tentatively; invite the author to accept or reject the diagnosis.

        ## Caveats
        Bias labels can become a status move—use sparingly and specifically.
        """,
    ),
    (
        "critical-thinking/causal-analysis.md",
        {
            "id": "TH-CRT-004",
            "title": "Causal Analysis",
            "title_zh": "因果分析",
            "category": "critical-thinking",
            "tags": ["causation", "correlation", "mechanism"],
            "best_for": ["because claims", "growth narratives"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Causal Analysis

        ## When to use
        When A is said to cause B.

        ## Steps
        1. Separate correlation from mechanism.
        2. Ask about reverse causation and common causes.
        3. Ask whether the effect size is large enough to matter.
        4. Prefer mechanisms the author can actually defend.

        ## Caveats
        Absence of a full causal model does not make a practical heuristic worthless.
        """,
    ),
    (
        "critical-thinking/premise-check.md",
        {
            "id": "TH-CRT-005",
            "title": "Premise Check",
            "title_zh": "前提检验",
            "category": "critical-thinking",
            "tags": ["assumptions", "hidden premises"],
            "best_for": ["hidden defaults", "shared culture assumptions"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Premise Check

        ## When to use
        When the conclusion depends on unspoken defaults.

        ## Steps
        1. List premises the author never stated.
        2. Rate each as plausible / contested / fragile.
        3. Show how the conclusion changes if a fragile premise fails.
        4. Ask the author which premises they are willing to defend.

        ## Caveats
        Not every premise needs a treatise—flag only load-bearing ones.
        """,
    ),
    (
        "business/multiple-mental-models.md",
        {
            "id": "TH-BUS-001",
            "title": "Multiple Mental Models",
            "title_zh": "多元思维模型",
            "category": "business",
            "tags": ["models", "decision", "latticework"],
            "best_for": ["complex business judgments"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Multiple Mental Models

        ## When to use
        When one fashionable framework is doing all the work.

        ## Steps
        1. Name the dominant model the author is using.
        2. Add 1–2 alternative models from adjacent fields.
        3. Compare what each model highlights and hides.
        4. Keep tension visible rather than forcing premature synthesis.

        ## Caveats
        More models are not better if they are decorative.
        """,
    ),
    (
        "business/network-effects.md",
        {
            "id": "TH-BUS-002",
            "title": "Network Effects",
            "title_zh": "网络效应",
            "category": "business",
            "tags": ["platforms", "scale", "flywheel"],
            "best_for": ["platform claims", "viral growth"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Network Effects

        ## When to use
        When value supposedly rises with more users/participants.

        ## Steps
        1. Specify who connects to whom.
        2. Distinguish direct, indirect, and data network effects.
        3. Ask about cold-start and multi-homing.
        4. Check whether the author confuses virality with defensibility.

        ## Caveats
        Growth alone is not proof of network effects.
        """,
    ),
    (
        "business/moat-analysis.md",
        {
            "id": "TH-BUS-003",
            "title": "Moat Analysis",
            "title_zh": "护城河分析",
            "category": "business",
            "tags": ["moat", "advantage", "competition"],
            "best_for": ["durable advantage claims"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Moat Analysis

        ## When to use
        When the author claims a lasting competitive edge.

        ## Steps
        1. Name the alleged moat type.
        2. Ask how a well-funded rival would attack it.
        3. Ask what evidence shows the moat is widening vs eroding.
        4. Separate temporary lead from structural moat.

        ## Caveats
        Narrative moats are common; cash-flow evidence is rarer.
        """,
    ),
    (
        "economics/opportunity-cost.md",
        {
            "id": "TH-ECO-001",
            "title": "Opportunity Cost",
            "title_zh": "机会成本",
            "category": "economics",
            "tags": ["tradeoff", "scarce", "choice"],
            "best_for": ["priority claims", "time allocation"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Opportunity Cost

        ## When to use
        When recommending an action without naming what is given up.

        ## Steps
        1. Ask what alternative uses of time/money/attention are displaced.
        2. Compare the next-best option, not a fantasy zero-cost baseline.
        3. Make the trade-off explicit in the claim.
        4. Avoid pretending every good thing can be maximized jointly.

        ## Caveats
        Opportunity cost is a lens, not a demand for spreadsheet precision.
        """,
    ),
    (
        "economics/incentive-analysis.md",
        {
            "id": "TH-ECO-002",
            "title": "Incentive Analysis",
            "title_zh": "激励机制",
            "category": "economics",
            "tags": ["incentives", "behavior", "institutions"],
            "best_for": ["org design", "policy", "platform rules"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Incentive Analysis

        ## When to use
        When outcomes depend on how people are rewarded or punished.

        ## Steps
        1. Map actors and their payoffs.
        2. Ask what behavior the current rules actually encourage.
        3. Look for metric gaming.
        4. Suggest incentive-aligned revisions only if the author wants them.

        ## Caveats
        Do not assume everyone is a cynical optimizer.
        """,
    ),
    (
        "economics/comparative-advantage.md",
        {
            "id": "TH-ECO-003",
            "title": "Comparative Advantage",
            "title_zh": "比较优势",
            "category": "economics",
            "tags": ["specialization", "trade", "relative cost"],
            "best_for": ["who should do what", "outsourcing claims"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Comparative Advantage

        ## When to use
        When absolute skill is confused with relative opportunity.

        ## Steps
        1. Separate absolute advantage from comparative advantage.
        2. Ask about opportunity costs of self-doing vs trading.
        3. Apply carefully to personal IP choices.
        4. Avoid telling the author to outsource their voice.

        ## Caveats
        Personal meaning and brand authenticity may outweigh pure efficiency.
        """,
    ),
    (
        "systems-thinking/systems-thinking.md",
        {
            "id": "TH-SYS-001",
            "title": "Systems Thinking",
            "title_zh": "系统思维",
            "category": "systems-thinking",
            "tags": ["system", "interdependence", "structure"],
            "best_for": ["ecosystems", "org problems", "AI markets"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Systems Thinking

        ## When to use
        When local fixes keep failing because parts interact.

        ## Steps
        1. Name the elements and relationships.
        2. Find delays and unintended consequences.
        3. Prefer structure explanations over blame stories.
        4. Propose interventions that change relationships, not only symptoms.

        ## Caveats
        Drawing a complicated diagram is not the same as understanding.
        """,
    ),
    (
        "systems-thinking/feedback-loops.md",
        {
            "id": "TH-SYS-002",
            "title": "Feedback Loops",
            "title_zh": "反馈回路",
            "category": "systems-thinking",
            "tags": ["reinforcing", "balancing", "loop"],
            "best_for": ["flywheels", "runaways", "homeostasis"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Feedback Loops

        ## When to use
        When outcomes feed back into causes.

        ## Steps
        1. Identify reinforcing and balancing loops.
        2. Ask which loop currently dominates.
        3. Ask what would flip dominance.
        4. Relate to the author's claim about growth or control.

        ## Caveats
        Not every cycle is a meaningful loop—require a causal story.
        """,
    ),
    (
        "systems-thinking/complex-systems.md",
        {
            "id": "TH-SYS-003",
            "title": "Complex Systems",
            "title_zh": "复杂系统",
            "category": "systems-thinking",
            "tags": ["emergence", "nonlinearity", "adaptation"],
            "best_for": ["markets", "culture", "AI ecosystems"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Complex Systems

        ## When to use
        When linear plans collide with adaptive agents.

        ## Steps
        1. Check for emergence.
        2. Watch for path dependence and tipping points.
        3. Prefer probes and feedback over grand prediction.
        4. Soften claims that assume controllable linear causality.

        ## Caveats
        Complexity talk can become an excuse to avoid responsibility—keep actionable.
        """,
    ),
    (
        "systems-thinking/leverage-points.md",
        {
            "id": "TH-SYS-004",
            "title": "Leverage Points",
            "title_zh": "杠杆点",
            "category": "systems-thinking",
            "tags": ["intervention", "leverage", "change"],
            "best_for": ["where to intervene", "strategy focus"],
            "license": "MIT",
            "source": "Curated method card; not a book excerpt",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Leverage Points

        ## When to use
        When the author pushes on a low-leverage symptom.

        ## Steps
        1. List candidate intervention points.
        2. Rank by likely systemic effect, not by ease.
        3. Ask whether the author's effort matches leverage.
        4. Offer one higher-leverage question.

        ## Caveats
        High leverage often means harder politics and slower feedback.
        """,
    ),
    (
        "science/probabilistic-thinking.md",
        {
            "id": "TH-SCI-001",
            "title": "Probabilistic Thinking",
            "title_zh": "概率思维",
            "category": "science",
            "tags": ["probability", "uncertainty", "base-rate"],
            "best_for": ["forecasts", "risk claims"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Probabilistic Thinking

        ## When to use
        When certainty language hides uncertainty.

        ## Steps
        1. Replace always/never with ranges when appropriate.
        2. Bring in base rates before vivid stories.
        3. Update beliefs when new evidence arrives.
        4. Separate confidence from importance.

        ## Caveats
        Fake numeric probabilities are worse than honest qualitative uncertainty.
        """,
    ),
    (
        "creativity/lateral-thinking.md",
        {
            "id": "TH-CRE-001",
            "title": "Lateral Thinking",
            "title_zh": "横向思维",
            "category": "creativity",
            "tags": ["lateral", "reframe", "provocation"],
            "best_for": ["stuck frames", "cliché angles"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Lateral Thinking

        ## When to use
        When the idea is correct but tired.

        ## Steps
        1. State the habitual frame.
        2. Provoke an alternative entry point.
        3. Keep provocations that unlock insight; discard gimmicks.
        4. Return to a coherent claim the author still owns.

        ## Caveats
        Novelty without truthfulness is just noise.
        """,
    ),
    (
        "creativity/cross-disciplinary-links.md",
        {
            "id": "TH-CRE-002",
            "title": "Cross-disciplinary Links",
            "title_zh": "跨学科联系",
            "category": "creativity",
            "tags": ["interdisciplinary", "transfer", "bridge"],
            "best_for": ["AI+business", "tech+society"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Cross-disciplinary Links

        ## When to use
        When a second field could illuminate the claim.

        ## Steps
        1. Name the home field of the claim.
        2. Borrow one concept from a neighboring field.
        3. Test whether the analogy shares structure, not just vibe.
        4. Credit the source field without name-dropping.

        ## Caveats
        Decorative interdisciplinarity confuses readers.
        """,
    ),
    (
        "creativity/analogical-reasoning.md",
        {
            "id": "TH-CRE-003",
            "title": "Analogical Reasoning",
            "title_zh": "类比推理",
            "category": "creativity",
            "tags": ["analogy", "mapping", "metaphor"],
            "best_for": ["explanations", "insight transfer"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Analogical Reasoning

        ## When to use
        When an analogy is carrying the argument.

        ## Steps
        1. Map source to target relations explicitly.
        2. List mismatches that would break the analogy.
        3. Keep the analogy as illumination, not as proof.
        4. Ask for non-analogical evidence if stakes are high.

        ## Caveats
        A beautiful metaphor can smuggle a false conclusion.
        """,
    ),
    (
        "creativity/combinatorial-innovation.md",
        {
            "id": "TH-CRE-004",
            "title": "Combinatorial Innovation",
            "title_zh": "组合创新",
            "category": "creativity",
            "tags": ["combine", "remix", "innovation"],
            "best_for": ["product ideas", "content formats"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Combinatorial Innovation

        ## When to use
        When the author senses a new idea but cannot name it.

        ## Steps
        1. Break the domain into parts.
        2. Recombine two parts that rarely meet.
        3. Evaluate usefulness, not just surprise.
        4. Ask which combination the author actually wants to own.

        ## Caveats
        Combination without a point of view becomes collage.
        """,
    ),
    (
        "psychology/reader-empathy.md",
        {
            "id": "TH-PSY-001",
            "title": "Reader Empathy",
            "title_zh": "普通读者共情",
            "category": "psychology",
            "tags": ["audience", "clarity", "misread"],
            "best_for": ["public writing", "carousel copy"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Reader Empathy

        ## When to use
        Before turning a thought into publishable writing.

        ## Steps
        1. Ask why a non-specialist should care.
        2. Locate jargon that can be misunderstood.
        3. Check emotional tone vs intended seriousness.
        4. Protect accuracy—do not dumb down into falsehood.

        ## Caveats
        Audience clarity is not the same as chasing engagement hacks.
        """,
    ),
    (
        "miscellaneous/source-attribution.md",
        {
            "id": "TH-MIS-001",
            "title": "Source Attribution Discipline",
            "title_zh": "资料出处纪律",
            "category": "miscellaneous",
            "tags": ["citation", "copyright", "provenance"],
            "best_for": ["expert uploads", "quotations"],
            "license": "MIT",
            "source": "Curated method card",
            "author": "Yihang Idea to Visual Contributors",
        },
        """
        # Source Attribution Discipline

        ## When to use
        Whenever expert notes, books, or papers are referenced.

        ## Steps
        1. Record author, title, section/page if known.
        2. Separate verbatim quote from paraphrase.
        3. If unverified, say so; never invent page numbers.
        4. Keep copyrighted full texts out of the public repository.

        ## Caveats
        A large private library does not automatically improve review quality—curate methods first.
        """,
    ),
    (
        "miscellaneous/demo-expert-note-distribution-vs-insight.md",
        {
            "id": "TH-MIS-DEMO-001",
            "title": "Demo Note: Distribution vs Insight",
            "title_zh": "测试资料：分发与洞察",
            "category": "miscellaneous",
            "tags": ["demo", "citation-test", "ai", "distribution", "insight"],
            "best_for": ["knowledge-base citation tests"],
            "license": "MIT",
            "source": "Original demo note for yihang-idea-to-visual tests",
            "author": "Yihang Idea to Visual Contributors",
            "work_title": "Demo Thought Note: Distribution vs Insight",
            "section": "Core claim",
            "page": "1",
        },
        """
        # Demo Note: Distribution vs Insight

        > Original demo excerpt for citation tests. Not a third-party book.

        ## Core claim
        When generative tools compress production cost, attention markets tighten.
        Distribution skill matters more than before, but it is not identical to the
        ability to notice unmet needs. Distribution moves existing supply toward
        attention; insight discovers demand that supply has not yet articulated.

        ## Author note
        This paragraph is intentionally short so agents can cite author, title,
        section, and page without loading a full manuscript.
        """,
    ),
]


def main() -> None:
    """Generate all seed thought cards.

    Returns:
        None
    """
    BASE.mkdir(parents=True, exist_ok=True)
    for rel, meta, body in CARDS:
        write_card(rel, meta, body)
    print("total", len(CARDS))


if __name__ == "__main__":
    main()
