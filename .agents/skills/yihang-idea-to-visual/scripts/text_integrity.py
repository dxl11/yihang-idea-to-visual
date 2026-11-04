#!/usr/bin/env python3
"""Article text integrity helpers for yihang-idea-to-visual.

Normalization intentionally avoids aggressive punctuation rewriting so that
Chinese punctuation, Latin words, digits, and symbols survive round-trips.
"""

from __future__ import annotations

from typing import Iterable, List


def normalize_article_text(text: str) -> str:
    """Normalize article text for integrity comparison.

    Args:
        text: Raw article text, possibly with mixed newlines.

    Returns:
        Normalized string using LF newlines with trailing whitespace stripped
        per line, then a single trailing newline removed from the whole text.
        Empty lines are preserved as empty lines (structure retained).

    Raises:
        TypeError: If ``text`` is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    unified = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip(" \t") for line in unified.split("\n")]
    # Drop one trailing empty line caused by a final newline in files.
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def concatenate_fragments(fragments: Iterable[str]) -> str:
    """Concatenate page text fragments without inserting separators.

    Args:
        fragments: Ordered fragment strings from page-manifest body pages.

    Returns:
        Joined string (empty string if no fragments).

    Raises:
        TypeError: If any fragment is not a string.
    """
    parts: List[str] = []
    for fragment in fragments:
        if not isinstance(fragment, str):
            raise TypeError("each fragment must be a str")
        parts.append(fragment)
    return "".join(parts)


def verify_article_integrity(article_text: str, fragments: Iterable[str]) -> tuple[bool, str]:
    """Verify that concatenated fragments equal the locked article.

    Args:
        article_text: Locked final article text.
        fragments: Ordered body-page fragments covering the article.

    Returns:
        Tuple ``(ok, message)`` where ``ok`` is True on match.

    Raises:
        TypeError: If inputs have invalid types.
    """
    expected = normalize_article_text(article_text)
    actual = normalize_article_text(concatenate_fragments(fragments))
    if expected == actual:
        return True, "article integrity ok"
    # Provide a short diagnostic without dumping entire articles.
    exp_len = len(expected)
    act_len = len(actual)
    mismatch_at = next(
        (i for i, (a, b) in enumerate(zip(expected, actual)) if a != b),
        min(exp_len, act_len),
    )
    return (
        False,
        (
            f"article integrity mismatch: expected_len={exp_len} actual_len={act_len} "
            f"first_diff_at={mismatch_at}"
        ),
    )
