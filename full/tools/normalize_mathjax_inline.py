"""Normalize legacy inline math fragments into complete MathJax units.

Newer chapter-body builders use this only as a compatibility safeguard for
content that was authored before the shared inline delimiter helper existed.
Formula display blocks are intentionally preserved verbatim.
"""
from __future__ import annotations

import re


_FORMULA_BLOCK = re.compile(r"(<div class=\"formula\">.*?</div>)", re.DOTALL)
_PARENTHESIZED_MATH = re.compile(
    r"(?<![\\A-Za-z0-9_])"
    r"\(((?:[^()<>\n]|\([^()<>\n]*\)){1,180})\)"
)
_FUNCTION_STYLE_MATH = re.compile(
    r"(?<![\\A-Za-z0-9_(])"
    r"([A-Za-z](?:_[A-Za-z0-9]+)?\([^()<>\n]*\))"
    r"(?![A-Za-z0-9_])"
)
_INLINE_MATH = re.compile(r"(\\\(.*?\\\))", re.DOTALL)


def _latexify_legacy_symbols(expression: str) -> str:
    """Translate old ASCII Greek names only after a fragment is known to be math."""
    return re.sub(r"(?<![A-Za-z\\])omega(?=[_\[]|\b)", r"\\omega", expression)


def _normalize_prose(fragment: str) -> str:
    """Wrap only compact ASCII mathematical fragments in MathJax delimiters."""
    protected: list[str] = []

    def protect_inline(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"@@INLINE_MATH_{len(protected) - 1}@@"

    fragment = _INLINE_MATH.sub(protect_inline, fragment)
    fragment = _PARENTHESIZED_MATH.sub(
        lambda match: rf"\({_latexify_legacy_symbols(match.group(1))}\)", fragment
    )
    parts = _INLINE_MATH.split(fragment)
    for index in range(0, len(parts), 2):
        parts[index] = _FUNCTION_STYLE_MATH.sub(
            lambda match: rf"\({_latexify_legacy_symbols(match.group(1))}\)", parts[index]
        )
    normalized = "".join(parts)
    for index, inline in enumerate(protected):
        normalized = normalized.replace(f"@@INLINE_MATH_{index}@@", inline)
    return normalized


def normalize_legacy_inline_math(content: str) -> str:
    """Return content whose compatible legacy inline formulas are MathJax math."""
    parts = _FORMULA_BLOCK.split(content)
    return "".join(
        part if part.startswith('<div class="formula">') else _normalize_prose(part)
        for part in parts
    )
