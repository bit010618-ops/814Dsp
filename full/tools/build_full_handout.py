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
from full.tools.normalize_mathjax_inline import normalize_legacy_inline_math
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
.chapter-exam-section{break-before:page}
.exam-page{break-before:page;break-inside:avoid;page-break-inside:avoid;min-height:230mm}
.exam-page:first-child{break-before:auto}
.chapter-exam-first{break-before:auto;page-break-before:auto}
.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt;break-after:avoid}
.writing-space{min-height:0}
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
.formula-lead{break-after:avoid;color:#52616b;font-size:10.5pt;margin:9pt 0 3pt}
.answer-page-ref{color:inherit;text-decoration:none;white-space:nowrap}
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


_CHAPTER_FRAGMENT_COUNTS = (5, 26, 14, 2, 1, 1, 2, 1)
_CHINESE_CHAPTERS = ("第一", "第二", "第三", "第四", "第五", "第六", "第七", "第八")


def _group_by_chapter(fragments: list[str]) -> list[list[str]]:
    """Split the verified flat component order into its eight chapter buckets."""
    if len(fragments) != sum(_CHAPTER_FRAGMENT_COUNTS):
        raise ValueError("chapter fragment count no longer matches the audited assembly")
    groups: list[list[str]] = []
    cursor = 0
    for count in _CHAPTER_FRAGMENT_COUNTS:
        groups.append(fragments[cursor : cursor + count])
        cursor += count
    return groups


def _remove_training_banner(fragment: str) -> str:
    """Use one reader-facing chapter title instead of batch-specific H1 banners."""
    return re.sub(r"<h1(?:\s[^>]*)?>.*?</h1>", "", fragment, count=1, flags=re.DOTALL)


def _remove_answer_banner(fragment: str) -> str:
    """Avoid repeating component-local answer banners under the final answer heading."""
    return re.sub(
        r"<h1(?:\s[^>]*)?>\s*真题整理详解[^<]*</h1>",
        "",
        fragment,
        flags=re.DOTALL,
    )


_FORMULA_OR_HEADING = re.compile(
    r"<h[1-4](?:\s[^>]*)?>(?P<heading>.*?)</h[1-4]>|"
    r'(?P<formula><div class="formula(?:\s[^"]*)?">(?P<formula_body>.*?)</div>)',
    flags=re.DOTALL,
)


def _formula_lead(formula: str, heading: str) -> str:
    """Describe a display formula in Chinese when nearby prose does not name it."""
    title = re.sub(r"<[^>]+>", "", heading)
    title = html.unescape(title).strip()
    latex = re.sub(r"<[^>]+>", "", formula)
    label = build_all_main_body._formula_name(latex, title or "本节")
    return f"{label}："


def _has_formula_context(rendered: str) -> bool:
    paragraph = re.search(r"<p(?:\s[^>]*)?>(.*?)</p>\s*$", rendered, flags=re.DOTALL)
    if paragraph is None:
        return False
    text = re.sub(r"<[^>]+>", "", paragraph.group(1))
    return bool(re.search(r"(?:为|如下|满足|得到|写成|可表示为|条件是|关系是)[：:]?\s*$", text))


def _has_explicit_formula_name(rendered: str) -> bool:
    """A chapter formula table already supplies its own reader-facing name."""
    return bool(
        re.search(r'<p class="formula-name">.*?</p>\s*$', rendered, flags=re.DOTALL)
    )


def _with_formula_leads(fragment: str) -> str:
    """Keep formulas readable by naming their purpose before the formula box."""
    output: list[str] = []
    cursor = 0
    heading = ""
    for match in _FORMULA_OR_HEADING.finditer(fragment):
        between = fragment[cursor:match.start()]
        output.append(between)
        if match.group("heading") is not None:
            heading = match.group("heading")
            output.append(match.group(0))
        else:
            # Only the immediately preceding paragraph can introduce this formula;
            # rebuilding the complete 600-page fragment here would be quadratic.
            rendered = "".join(output[-6:])
            if not _has_explicit_formula_name(between) and not _has_formula_context(rendered):
                output.append(
                    f'<p class="formula-lead">{html.escape(_formula_lead(match.group("formula"), heading))}</p>'
                )
            output.append(match.group("formula"))
        cursor = match.end()
    output.append(fragment[cursor:])
    return "".join(output)


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


def _anchor_answer_headings(
    fragment: str, start_index: int
) -> tuple[str, list[tuple[str, str]]]:
    """Give one answer fragment stable targets and return their years."""
    index = start_index
    records: list[tuple[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        nonlocal index
        index += 1
        answer_id = f"answer-{index:03d}"
        attributes = match.group("attributes")
        title = re.sub(r"<[^>]+>", "", match.group("title"))
        year_match = re.search(r"(20\d{2})\s*年真题", html.unescape(title))
        if year_match is None:
            raise ValueError(f"answer heading has no year: {title}")
        records.append((year_match.group(1), answer_id))
        return (
            f'<h2{attributes} id="{answer_id}" data-answer-id="{answer_id}">'
            f'{match.group("title")}</h2>'
        )

    anchored = re.sub(
        r"<h2(?P<attributes>[^>]*)>(?P<title>.*?)</h2>",
        replace,
        fragment,
        flags=re.DOTALL,
    )
    return anchored, records


def _training_years(fragment: str) -> list[str]:
    """Read the printed year immediately preceding each training page reference."""
    years: list[str] = []
    for match in re.finditer(r"详解见 P\.____", fragment):
        context = re.sub(r"<[^>]+>", " ", fragment[max(0, match.start() - 500) : match.start()])
        candidates = re.findall(r"(20\d{2})\s*年真题", context)
        if not candidates:
            raise ValueError("training page reference has no preceding exam year")
        years.append(candidates[-1])
    return years


def _link_training_references(fragment: str, answer_records: list[tuple[str, str]]) -> str:
    """Attach every printed page-reference placeholder to its same-component answer."""
    by_year: dict[str, list[str]] = {}
    for year, answer_id in answer_records:
        by_year.setdefault(year, []).append(answer_id)
    years = _training_years(fragment)
    consumed: dict[str, int] = {}

    def replace(match: re.Match[str]) -> str:
        year = years.pop(0)
        targets = by_year.get(year, [])
        if not targets:
            raise ValueError(f"training year {year} has no detailed-answer target")
        occurrence = consumed.get(year, 0)
        answer_id = targets[0] if len(targets) == 1 else targets[occurrence]
        if len(targets) > 1 and occurrence >= len(targets):
            raise ValueError(f"training year {year} has more references than answer headings")
        consumed[year] = occurrence + 1
        return (
            f'<a class="answer-page-ref" href="#{answer_id}" '
            f'data-answer-ref="{answer_id}">详解见 P.____</a>'
        )

    linked = re.sub(r"详解见 P\.____", replace, fragment)
    if years:
        raise ValueError("not every training reference was linked")
    return linked


def _document(body: str, appendices: str, navigation: str, answers: str) -> str:
    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<script>window.MathJax={tex:{packages:{"[+]": ["ams"]}}};</script>'
        f'<script defer src="{MATHJAX}"></script>{STYLE}<style>{build_appendices.STYLE}</style></head>'
        f'<body><main>{body}{appendices}{navigation}'
        '<section class="answer-section"><div class="appendix-f">'
        "<h1>附录 F：真题整理详解</h1>"
        f"{answers}</div></section>{build_appendices.appendix_i_html()}</main></body></html>"
    )


def write_html(output: Path) -> Path:
    """Write the full-book assembly using every currently verified training component."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dsp-full-handout-") as temporary:
        directory = Path(temporary)
        chapter_bodies = [_with_formula_leads(body) for body in build_all_main_body._chapters()]
        training_fragments = _group_by_chapter(
            [_normalize_answer_refs(fragment) for fragment in _training_fragments(directory)]
        )
        answer_fragments = _answer_fragments(directory)
        anchored_answers: list[str] = []
        answer_records_by_fragment: list[list[tuple[str, str]]] = []
        answer_index = 0
        for fragment in answer_fragments:
            anchored, records = _anchor_answer_headings(_with_formula_leads(fragment), answer_index)
            anchored_answers.append(anchored)
            answer_records_by_fragment.append(records)
            answer_index += len(records)
        answer_records_by_chapter = _group_by_chapter(answer_records_by_fragment)
        chapter_blocks: list[str] = []
        for index, (chapter_body, question_group, record_group) in enumerate(
            zip(chapter_bodies, training_fragments, answer_records_by_chapter), start=1
        ):
            training = "\n".join(
                normalize_legacy_inline_math(
                    _remove_training_banner(_link_training_references(fragment, records))
                )
                for fragment, records in zip(question_group, record_group)
            )
            title = _CHINESE_CHAPTERS[index - 1]
            first_exam_page = '<section class="exam-page">'
            if first_exam_page not in training:
                raise ValueError(f"第 {index} 章真题整理缺少题面页")
            training = training.replace(
                first_exam_page,
                f'<section class="exam-page chapter-exam-first"><h1>{title}章真题整理</h1>',
                1,
            )
            chapter_blocks.append(
                f'<section class="chapter-start">{chapter_body}'
                f'<section class="chapter-exam-section">{training}</section>'
                "</section>"
            )
        body = "\n".join(chapter_blocks)
        answers = "\n".join(
            normalize_legacy_inline_math(_remove_answer_banner(fragment))
            for fragment in anchored_answers
        )
    output.write_text(
        _document(
            body,
            _with_formula_leads(build_appendices.pre_answer_appendices_html(body)),
            _exam_navigation_html(),
            answers,
        ),
        encoding="utf-8",
    )
    return output


if __name__ == "__main__":
    print(write_html(ROOT / "full" / "outputs" / "dsp_full_handout.html"))
