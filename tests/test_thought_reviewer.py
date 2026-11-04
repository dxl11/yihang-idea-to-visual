"""Thought Reviewer module: wiring, library index, and acceptance fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "yihang-idea-to-visual"
SCRIPTS = SKILL / "scripts"
THOUGHT_LIB = SKILL / "assets" / "thought-library"
FIXTURES = ROOT / "tests" / "fixtures" / "thought-reviewer"
SKILL_MD = SKILL / "SKILL.md"


def test_thought_reviewer_reference_linked_in_skill():
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "references/thought-reviewer.md" in text
    assert "references/thinking-frameworks.md" in text
    assert "STEP 00" in text
    assert "Thought Reviewer" in text
    assert (SKILL / "references" / "thought-reviewer.md").is_file()
    assert (SKILL / "references" / "thinking-frameworks.md").is_file()


def test_thought_statuses_in_schema_and_template():
    schema = json.loads((SKILL / "schemas" / "project-state.schema.json").read_text(encoding="utf-8"))
    statuses = schema["properties"]["status"]["enum"]
    assert "thought_review" in statuses
    assert "thought_ready" in statuses
    assert statuses.index("thought_review") < statuses.index("article_review")

    state = json.loads(
        (SKILL / "assets" / "templates" / "project-template" / "state.json").read_text(
            encoding="utf-8"
        )
    )
    assert state["status"] == "thought_review"
    assert state.get("thought_mode") == "standard"
    assert "thought" in state.get("locks", {})


def test_thought_library_seed_cards_exist():
    required = [
        "philosophy/socratic-questioning.md",
        "logic/deductive-reasoning.md",
        "critical-thinking/counterexample-test.md",
        "business/moat-analysis.md",
        "economics/opportunity-cost.md",
        "systems-thinking/systems-thinking.md",
        "science/probabilistic-thinking.md",
        "creativity/lateral-thinking.md",
        "psychology/reader-empathy.md",
        "miscellaneous/demo-expert-note-distribution-vs-insight.md",
    ]
    for rel in required:
        assert (THOUGHT_LIB / rel).is_file(), rel


def test_thought_catalog_and_index_script(tmp_path: Path):
    catalog_path = THOUGHT_LIB / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    assert catalog["skill_id"] == "yihang-idea-to-visual"
    assert catalog["library"] == "thought-library"
    assert len(catalog["items"]) >= 20

    demo = next(item for item in catalog["items"] if item["id"] == "TH-MIS-DEMO-001")
    assert demo["author"]
    assert demo["work_title"] or "Demo" in demo["title"]
    assert demo.get("section")
    assert demo.get("page")
    assert demo["license"] in {"MIT", "unknown", "private", "CC0", "CC-BY-4.0"}

    out = tmp_path / "catalog.json"
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "build_thought_index.py"),
            "--library",
            str(THOUGHT_LIB),
            "--output",
            str(out),
            "--full",
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    rebuilt = json.loads(out.read_text(encoding="utf-8"))
    assert rebuilt["stats"]["total"] >= 20


def test_build_thought_index_help():
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "build_thought_index.py"), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert proc.returncode == 0
    assert "usage:" in (proc.stdout + proc.stderr).lower()


def test_acceptance_checklist_fixtures_present():
    checklist = json.loads((FIXTURES / "acceptance_checklist.json").read_text(encoding="utf-8"))
    assert checklist["module"] == "thought-reviewer"
    assert len(checklist["scenarios"]) >= 8

    for scenario in checklist["scenarios"]:
        fixture = scenario.get("fixture")
        fixtures = scenario.get("fixtures") or ([] if fixture is None else [fixture])
        for name in fixtures:
            assert (FIXTURES / name).is_file(), name
        assert scenario["must_cover"], scenario["id"]


def test_skill_documents_skip_and_dialogue_rules():
    skill = SKILL_MD.read_text(encoding="utf-8")
    reviewer = (SKILL / "references" / "thought-reviewer.md").read_text(encoding="utf-8")
    combined = skill + "\n" + reviewer
    assert "skip" in combined.lower() or "跳过" in combined
    assert "one key question" in combined.lower() or "一个" in combined
    assert "deep_critique" in combined or "深度批判" in combined
    assert "light" in combined.lower() or "轻量" in combined


def test_readmes_document_thought_reviewer():
    cn = (ROOT / "README.md").read_text(encoding="utf-8")
    en = (ROOT / "README.en.md").read_text(encoding="utf-8")
    assert "Thought Reviewer" in cn
    assert "Thought Reviewer" in en
    assert "思想知识库" in cn
    assert "Thought library" in en
    assert "build_thought_index.py" in cn
    assert "build_thought_index.py" in en


def test_t5_demo_source_traceable_without_fabricating_book():
    """Citation fixture must point at original demo note, not a copyrighted book."""
    demo = (
        THOUGHT_LIB / "miscellaneous" / "demo-expert-note-distribution-vs-insight.md"
    ).read_text(encoding="utf-8")
    assert "Original demo" in demo or "original demo" in demo.lower()
    assert "third-party book" in demo.lower() or "Not a third-party" in demo
    assert "page: 1" in demo.lower() or "page: 1" in demo


def test_content_editing_acknowledges_prior_thought_step():
    text = (SKILL / "references" / "content-editing.md").read_text(encoding="utf-8")
    assert "Thought Reviewer" in text or "STEP 00" in text
    assert "deepened-idea.md" in text
