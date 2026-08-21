"""Assemble the completed eight-chapter body with reusable training and answers."""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools import build_all_main_body
from full.tools import build_chapter_01_training_answers_mathjax_component as chapter_one_answers
from full.tools import build_chapter_01_training_mathjax_component as chapter_one_training
from full.tools import build_chapter_02_training_mathjax_component as chapter_two_training
from full.tools import build_chapter_03_training_mathjax_component as chapter_three_training
from full.tools.render_mathjax_formula import MATHJAX


STYLE = build_all_main_body.STYLE + r"""
<style>
.training-section{break-before:page}
.exam-page{break-before:page;min-height:230mm}
.exam-page:first-child{break-before:auto}
.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt;break-after:avoid}
.writing-space{min-height:105mm}
.answer-section{break-before:page}
.answer-section h1{break-before:page}
.answer-section h1:first-child{break-before:auto}
.answer-step{break-inside:avoid;margin:8pt 0}
.answer-step strong{color:#315d7c}
</style>
"""


def _main_body(document: str) -> str:
    match = re.search(r"<main(?:\s[^>]*)?>(.*)</main>", document, flags=re.DOTALL)
    if match is None:
        raise ValueError("component is missing a main element")
    return match.group(1).strip()


def _component_main(writer: object, output: Path) -> str:
    return _main_body(writer(output).read_text(encoding="utf-8"))


def _training_fragments(directory: Path) -> list[str]:
    return [
        _component_main(chapter_one_training.write_html, directory / "chapter-01-training.html"),
        chapter_two_training.training_html(),
        _component_main(chapter_three_training.write_training_html, directory / "chapter-03-training.html"),
    ]


def _answer_fragments(directory: Path) -> list[str]:
    return [
        _component_main(chapter_one_answers.write_html, directory / "chapter-01-answers.html"),
        chapter_two_training.answers_html(),
        _component_main(chapter_three_training.write_answers_html, directory / "chapter-03-answers.html"),
    ]


def _document(body: str, training: str, answers: str) -> str:
    return (
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<script>window.MathJax={tex:{packages:{"[+]": ["ams"]}}};</script>'
        f'<script defer src="{MATHJAX}"></script>{STYLE}'
        f'<body><main>{body}<section class="training-section">{training}</section>'
        f'<section class="answer-section">{answers}</section></main></body></html>'
    )


def write_html(output: Path) -> Path:
    """Write the first full-book assembly using only verified chapter 1--3 training."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dsp-full-handout-") as temporary:
        directory = Path(temporary)
        body_path = build_all_main_body.write_html(directory / "main-body.html")
        body = _main_body(body_path.read_text(encoding="utf-8"))
        training = "\n".join(_training_fragments(directory))
        answers = "\n".join(_answer_fragments(directory))
    output.write_text(_document(body, training, answers), encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_html(ROOT / "full" / "outputs" / "dsp_full_handout.html"))
