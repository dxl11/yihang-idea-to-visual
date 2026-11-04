"""Article content protection / integrity tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents" / "skills" / "yihang-idea-to-visual" / "scripts"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ti = _load_module("text_integrity", SCRIPTS / "text_integrity.py")


SAMPLE_ARTICLE = """AI 时代的个人 IP，不是靠“更会说”，而是靠“更会沉淀”。

我在 2024 年记录了 120+ 条想法；真正发出来的不到 10%。问题不在灵感，而在生产链路：从想法 → 成文 → 标题 → 封面 → 排版，每一步都在消耗意志力。

数字也会说话：把 3 个核心观点拆成 5–8 页图文，阅读完成率通常高于长文链接（这是经验判断，不是伪造实验）。

英文混排也要保真：Personal Branding = 长期一致性 × 可传播表达。

特殊符号保留：【观点】、#标签、100%、A/B、email@example.com、——以及《书名》。

最后一段较短。
"""


def test_normalize_preserves_cjk_punct_and_symbols():
    normalized = ti.normalize_article_text(SAMPLE_ARTICLE)
    assert "【观点】" in normalized
    assert "100%" in normalized
    assert "Personal Branding" in normalized
    assert "email@example.com" in normalized
    assert "——" in normalized


def test_fragments_round_trip_exact():
    article = ti.normalize_article_text(SAMPLE_ARTICLE)
    # Split into uneven semantic-ish chunks without altering characters.
    cuts = [0, 40, 120, 200, 280, len(article)]
    fragments = [article[cuts[i] : cuts[i + 1]] for i in range(len(cuts) - 1)]
    assert any("\n" in f for f in fragments)
    ok, msg = ti.verify_article_integrity(article, fragments)
    assert ok, msg


def test_detects_deleted_sentence():
    article = ti.normalize_article_text(SAMPLE_ARTICLE)
    fragments = [article[:80], article[100:]]  # dropped middle
    ok, msg = ti.verify_article_integrity(article, fragments)
    assert not ok
    assert "mismatch" in msg


def test_detects_summarization_replacement():
    article = ti.normalize_article_text(SAMPLE_ARTICLE)
    fake = ["这是总结后的短文，不是原文。"]
    ok, _ = ti.verify_article_integrity(article, fake)
    assert not ok


def test_count_equality_is_insufficient():
    """Same length but different content must fail."""
    a = "甲乙丙丁戊己庚辛"
    b = "一二三四五六七八"
    assert len(a) == len(b)
    ok, _ = ti.verify_article_integrity(a, [b])
    assert not ok
