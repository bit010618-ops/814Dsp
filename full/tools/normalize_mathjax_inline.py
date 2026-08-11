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


def _normalize_prose(fragment: str) -> str:
    """Wrap only compact ASCII mathematical fragments in MathJax delimiters."""
    fragment = _PARENTHESIZED_MATH.sub(
        lambda match: rf"\({match.group(1)}\)", fragment
    )
    return _FUNCTION_STYLE_MATH.sub(
        lambda match: rf"\({match.group(1)}\)", fragment
    )


def normalize_legacy_inline_math(content: str) -> str:
    """Return content whose compatible legacy inline formulas are MathJax math."""
    parts = _FORMULA_BLOCK.split(content)
    return "".join(
        part if part.startswith('<div class="formula">') else _normalize_prose(part)
        for part in parts
    )
