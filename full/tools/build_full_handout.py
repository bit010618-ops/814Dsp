"""Assemble the completed eight-chapter body with reusable training and answers."""
from __future__ import annotations

import html
import json
import re
import sys
import tempfile
from importlib import import_module
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAM_TRAINING_MANIFEST = ROOT / "full" / "source" / "exam_training_manifest.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools import build_all_main_body
from full.tools import build_appendices
from full.tools import build_chapter_01_training_answers_mathjax_component as chapter_one_answers
from full.tools import build_chapter_01_supplemental_mathjax_component as chapter_one_supplemental
from full.tools import build_chapter_01_training_mathjax_component as chapter_one_training
from full.tools import build_chapter_01_supplemental_training_batch_one_mathjax_component as chapter_one_batch_one
from full.tools import build_chapter_01_supplemental_training_batch_two_mathjax_component as chapter_one_batch_two
from full.tools import build_chapter_01_supplemental_training_batch_three_mathjax_component as chapter_one_batch_three
from full.tools import build_chapter_02_supplemental_training_mathjax_component as chapter_two_supplemental
from full.tools import build_chapter_02_training_mathjax_component as chapter_two_training
from full.tools import build_chapter_03_training_mathjax_component as chapter_three_training
from full.tools import build_chapter_03_supplemental_training_batch_one_mathjax_component as chapter_three_batch_one
from full.tools import build_chapter_03_supplemental_training_batch_two_mathjax_component as chapter_three_batch_two
from full.tools import build_chapter_03_supplemental_training_batch_three_mathjax_component as chapter_three_batch_three
from full.tools import build_chapter_03_supplemental_training_batch_four_mathjax_component as chapter_three_batch_four
from full.tools import build_chapter_03_supplemental_training_batch_five_mathjax_component as chapter_three_batch_five
from full.tools import build_chapter_03_supplemental_training_batch_six_mathjax_component as chapter_three_batch_six
from full.tools import build_chapter_03_supplemental_training_batch_seven_mathjax_component as chapter_three_batch_seven
from full.tools import build_chapter_03_supplemental_training_batch_eight_mathjax_component as chapter_three_batch_eight
from full.tools import build_chapter_03_supplemental_training_batch_nine_mathjax_component as chapter_three_batch_nine
from full.tools import build_chapter_03_supplemental_training_batch_ten_mathjax_component as chapter_three_batch_ten
from full.tools import build_chapter_03_supplemental_training_batch_eleven_mathjax_component as chapter_three_batch_eleven
from full.tools import build_chapter_03_supplemental_training_batch_twelve_mathjax_component as chapter_three_batch_twelve
from full.tools import build_chapter_03_supplemental_training_batch_thirteen_mathjax_component as chapter_three_batch_thirteen
from full.tools import build_chapter_04_training_mathjax_component as chapter_four_training
from full.tools import build_chapter_04_supplemental_training_batch_one_mathjax_component as chapter_four_batch_one
from full.tools import build_chapter_05_training_mathjax_component as chapter_five_training
from full.tools import build_chapter_06_training_mathjax_component as chapter_six_training
from full.tools import build_chapter_07_training_mathjax_component as chapter_seven_training
from full.tools import build_chapter_07_supplemental_training_mathjax_component as chapter_seven_supplemental
from full.tools import build_chapter_08_training_mathjax_component as chapter_eight_training
from full.tools.render_mathjax_formula import MATHJAX


_CHAPTER_TWO_BATCH_NAMES = (
    "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
    "eighteen", "nineteen", "twenty", "twenty_one", "twenty_two", "twenty_three",
    "twenty_four", "twenty_five",
)
CHAPTER_TWO_SUPPLEMENTAL_BATCHES = tuple(
    import_module(
        f"full.tools.build_chapter_02_supplemental_training_batch_{name}_mathjax_component"
    )
    for name in _CHAPTER_TWO_BATCH_NAMES
)


STYLE = build_all_main_body.STYLE + r"""
<style>
.training-section{break-before:page}
.exam-page{break-before:page;break-inside:avoid;page-break-inside:avoid;min-height:230mm}
.exam-page:first-child{break-before:auto}
.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt;break-after:avoid}
.writing-space{min-height:105mm}
.answer-section{break-before:page}
.answer-section h1{break-before:page}
.answer-section h1:first-child{break-before:auto}
.appendix{break-before:page}
.appendix h1{break-before:auto}
.appendix h2{break-before:auto;margin-top:16pt}
.appendix-e .table{border-collapse:collapse;width:100%;margin:8pt 0 14pt;font-size:9.5pt}
.appendix-e .table th,.appendix-e .table td{border:.45pt solid #b9c6cf;padding:5pt 6pt;text-align:left;vertical-align:top}
.appendix-e .table th{background:#f4f7f8;color:#315d7c;font-weight:600}
.appendix-e .table .page-ref{white-space:nowrap}
.answer-step{break-inside:avoid;margin:8pt 0}
.answer-step strong{color:#315d7c}
.fft-flow{break-inside:avoid;margin:12pt 0}
.fft-flow img{display:block;width:100%;height:auto;border:.5pt solid #d6dde2;background:#fff}
.fft-flow svg{display:block;width:100%;height:auto;border:.5pt solid #d6dde2;background:#fff}
.fft-flow figcaption{color:#52616b;text-align:center;margin-top:5pt;font-size:9.5pt}
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
        _component_main(
            chapter_one_supplemental.write_questions_html,
            directory / "chapter-01-supplemental-training.html",
        ),
        chapter_one_batch_one.training_html(),
        chapter_one_batch_two.training_html(),
        chapter_one_batch_three.training_html(),
        chapter_two_training.training_html(),
        chapter_two_supplemental.training_html(),
        *(component.training_html() for component in CHAPTER_TWO_SUPPLEMENTAL_BATCHES),
        _component_main(chapter_three_training.write_training_html, directory / "chapter-03-training.html"),
        _component_main(chapter_three_batch_one.write_training_html, directory / "chapter-03-batch-one-training.html"),
        _component_main(chapter_three_batch_two.write_training_html, directory / "chapter-03-batch-two-training.html"),
        _component_main(chapter_three_batch_three.write_training_html, directory / "chapter-03-batch-three-training.html"),
        _component_main(chapter_three_batch_four.write_training_html, directory / "chapter-03-batch-four-training.html"),
        _component_main(chapter_three_batch_five.write_training_html, directory / "chapter-03-batch-five-training.html"),
        _component_main(chapter_three_batch_six.write_training_html, directory / "chapter-03-batch-six-training.html"),
        _component_main(chapter_three_batch_seven.write_training_html, directory / "chapter-03-batch-seven-training.html"),
        _component_main(chapter_three_batch_eight.write_training_html, directory / "chapter-03-batch-eight-training.html"),
        _component_main(chapter_three_batch_nine.write_training_html, directory / "chapter-03-batch-nine-training.html"),
        _component_main(chapter_three_batch_ten.write_training_html, directory / "chapter-03-batch-ten-training.html"),
        _component_main(chapter_three_batch_eleven.write_training_html, directory / "chapter-03-batch-eleven-training.html"),
        _component_main(chapter_three_batch_twelve.write_training_html, directory / "chapter-03-batch-twelve-training.html"),
        _component_main(chapter_three_batch_thirteen.write_training_html, directory / "chapter-03-batch-thirteen-training.html"),
        _component_main(chapter_four_training.write_training_html, directory / "chapter-04-training.html"),
        _component_main(chapter_four_batch_one.write_training_html, directory / "chapter-04-batch-one-training.html"),
        _component_main(chapter_five_training.write_training_html, directory / "chapter-05-training.html"),
        _component_main(chapter_six_training.write_training_html, directory / "chapter-06-training.html"),
        _component_main(chapter_seven_training.write_training_html, directory / "chapter-07-training.html"),
        _component_main(
            chapter_seven_supplemental.write_training_html,
            directory / "chapter-07-supplemental-training.html",
        ),
        _component_main(chapter_eight_training.write_training_html, directory / "chapter-08-training.html"),
    ]


def _answer_fragments(directory: Path) -> list[str]:
    return [
        _component_main(chapter_one_answers.write_html, directory / "chapter-01-answers.html"),
        _component_main(
            chapter_one_supplemental.write_answers_html,
            directory / "chapter-01-supplemental-answers.html",
        ),
        chapter_one_batch_one.answers_html(),
        chapter_one_batch_two.answers_html(),
        chapter_one_batch_three.answers_html(),
        chapter_two_training.answers_html(),
        chapter_two_supplemental.answers_html(),
        *(component.answers_html() for component in CHAPTER_TWO_SUPPLEMENTAL_BATCHES),
        _component_main(chapter_three_training.write_answers_html, directory / "chapter-03-answers.html"),
        _component_main(chapter_three_batch_one.write_answers_html, directory / "chapter-03-batch-one-answers.html"),
        _component_main(chapter_three_batch_two.write_answers_html, directory / "chapter-03-batch-two-answers.html"),
        _component_main(chapter_three_batch_three.write_answers_html, directory / "chapter-03-batch-three-answers.html"),
        _component_main(chapter_three_batch_four.write_answers_html, directory / "chapter-03-batch-four-answers.html"),
        _component_main(chapter_three_batch_five.write_answers_html, directory / "chapter-03-batch-five-answers.html"),
        _component_main(chapter_three_batch_six.write_answers_html, directory / "chapter-03-batch-six-answers.html"),
        _component_main(chapter_three_batch_seven.write_answers_html, directory / "chapter-03-batch-seven-answers.html"),
        _component_main(chapter_three_batch_eight.write_answers_html, directory / "chapter-03-batch-eight-answers.html"),
        _component_main(chapter_three_batch_nine.write_answers_html, directory / "chapter-03-batch-nine-answers.html"),
        _component_main(chapter_three_batch_ten.write_answers_html, directory / "chapter-03-batch-ten-answers.html"),
        _component_main(chapter_three_batch_eleven.write_answers_html, directory / "chapter-03-batch-eleven-answers.html"),
        _component_main(chapter_three_batch_twelve.write_answers_html, directory / "chapter-03-batch-twelve-answers.html"),
        _component_main(chapter_three_batch_thirteen.write_answers_html, directory / "chapter-03-batch-thirteen-answers.html"),
        _component_main(chapter_four_training.write_answers_html, directory / "chapter-04-answers.html"),
        _component_main(chapter_four_batch_one.write_answers_html, directory / "chapter-04-batch-one-answers.html"),
        _component_main(chapter_five_training.write_answers_html, directory / "chapter-05-answers.html"),
        _component_main(chapter_six_training.write_answers_html, directory / "chapter-06-answers.html"),
        _component_main(chapter_seven_training.write_answers_html, directory / "chapter-07-answers.html"),
        _component_main(
            chapter_seven_supplemental.write_answers_html,
            directory / "chapter-07-supplemental-answers.html",
        ),
        _component_main(chapter_eight_training.write_answers_html, directory / "chapter-08-answers.html"),
    ]


def _normalize_answer_refs(fragment: str) -> str:
    """Defer every printed answer page number until final whole-book pagination."""
    return re.sub(r"详解见 P\.(?:\d+|____)", "详解见 P.____", fragment)


def _exam_navigation_html() -> str:
    """Render the audited question manifest as the paper-book lookup appendix."""
    manifest = json.loads(EXAM_TRAINING_MANIFEST.read_text(encoding="utf-8"))
    chapter_sections: list[str] = []
    for chapter in manifest["chapters"]:
        chapter_rows: list[str] = []
        for bucket, kind in (
            ("priority_questions", "重点精练"),
            ("supplemental_questions", "补充真题"),
        ):
            for question in chapter[bucket]:
                locator = html.escape(question["source_locator"])
                exam_id = html.escape(question["id"], quote=True)
                chapter_rows.append(
                    f'<tr data-exam-navigation="true" data-exam-id="{exam_id}">'
                    f'<td>{question["year"]} 年</td><td>{kind}</td><td>{locator}</td>'
                    '<td class="page-ref">详解见 P.待回填</td></tr>'
                )
        if not chapter_rows:
            continue
        number = chapter["chapter"]
        chapter_sections.append(
            f"<h2>第{number}章</h2>"
            "<table class=\"table\"><thead><tr>"
            "<th>年份</th><th>训练位置</th><th>题目</th><th>详解</th>"
            "</tr></thead><tbody>"
            f"{''.join(chapter_rows)}</tbody></table>"
        )
    if not chapter_sections:
        raise ValueError("exam training manifest contains no navigation entries")
    return (
        '<section class="appendix appendix-e"><h1>附录 E：华理 814 真题考点导航</h1>'
        "<p>按章节、年份和训练位置检索；全部页码将在全书最终分页后统一回填。</p>"
        f"{''.join(chapter_sections)}</section>"
    )


def _document(
    body: str, training: str, appendices: str, navigation: str, answers: str
) -> str:
    return (
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<script>window.MathJax={tex:{packages:{"[+]": ["ams"]}}};</script>'
        f'<script defer src="{MATHJAX}"></script>{STYLE}{build_appendices.STYLE}'
        f'<body><main>{body}<section class="training-section">{training}</section>{appendices}{navigation}'
        '<section class="answer-section"><div class="appendix-f">'
        "<h1>附录 F：华理 814 历年 DSP 真题整理详解</h1>"
        f"{answers}</div></section>{build_appendices.appendix_i_html()}</main></body></html>"
    )


def write_html(output: Path) -> Path:
    """Write the full-book assembly using every currently verified training component."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dsp-full-handout-") as temporary:
        directory = Path(temporary)
        body_path = build_all_main_body.write_html(directory / "main-body.html")
        body = _main_body(body_path.read_text(encoding="utf-8"))
        training = "\n".join(
            _normalize_answer_refs(fragment)
            for fragment in _training_fragments(directory)
        )
        answers = "\n".join(_answer_fragments(directory))
    output.write_text(
        _document(
            body,
            training,
            build_appendices.pre_answer_appendices_html(body),
            _exam_navigation_html(),
            answers,
        ),
        encoding="utf-8",
    )
    return output


if __name__ == "__main__":
    print(write_html(ROOT / "full" / "outputs" / "dsp_full_handout.html"))
