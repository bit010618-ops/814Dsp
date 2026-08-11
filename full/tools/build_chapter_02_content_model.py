"""Build the page-allocation audit model for chapter two's main body.

This model is deliberately an audit inventory, not a completion claim.  It
locks source order and assigns every source page to the body unit that must be
reconciled before the chapter can be accepted.  Training and answer modules
are intentionally absent.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = Path("full/source/chapter_02_content_model.json")


def _pages(start: int, end: int) -> list[int]:
    return list(range(start, end + 1))


UNIT_DEFINITIONS = [
    ("c2-opening", "chapter_opening", "第二章导览", 186, 186, "保留本章六节目录及原有先后顺序。"),
    ("c2-01-z-definition-roc", "textbook_section", "2.1 z 变换的定义与收敛域", 187, 201, "保留 z 变换由来、定义、典型序列与收敛域。"),
    ("c2-01-inverse-properties", "textbook_section", "2.1 z 反变换与 z 变换性质", 202, 222, "保留三种反变换方法、方法比较及 z 变换性质。"),
    ("c2-02-dtft", "textbook_section", "2.2 离散时间信号傅里叶变换", 223, 239, "保留正反变换、周期性、共轭对称性质及例题。"),
    ("c2-03-system-function", "textbook_section", "2.3 系统函数及其与系统性质的关系", 240, 253, "保留系统函数、收敛域与因果性、稳定性的关系。"),
    ("c2-04-frequency-response", "textbook_section", "2.4 系统频率响应的意义", 254, 282, "保留单位圆取值、幅频响应、相频响应和固定频率输入下的输出。"),
    ("c2-05-geometry-response", "textbook_section", "2.5 几何法画频率响应", 283, 303, "保留单位圆上的距离与相角关系及作图步骤。"),
    ("c2-06-special-filters-a", "textbook_section", "2.6 特殊滤波器：一阶滤波器", 304, 320, "保留简单一阶低通、高通、带通和带阻滤波器。"),
    ("c2-06-special-filters-b", "textbook_section", "2.6 特殊滤波器：谐振器与 DTMF", 321, 348, "保留数字谐振器、双音多频信号和陷波滤波器。"),
    ("c2-06-special-filters-c", "textbook_section", "2.6 特殊滤波器：全通、最小相位与应用", 349, 387, "保留全通滤波器、最小相位滤波器和工程滤波方法；课件叙事性结语待最终正文核对时按知识信息决定保留方式。"),
]

COMPONENT_FILE_BY_UNIT = {
    "c2-01-z-definition-roc": "full/tools/build_chapter_02_foundations_mathjax_component.py",
    "c2-01-inverse-properties": "full/tools/build_chapter_02_inverse_properties_mathjax_component.py",
    "c2-02-dtft": "full/tools/build_chapter_02_dtft_mathjax_component.py",
    "c2-03-system-function": "full/tools/build_chapter_02_system_frequency_mathjax_component.py",
    "c2-04-frequency-response": "full/tools/build_chapter_02_system_frequency_mathjax_component.py",
    "c2-05-geometry-response": "full/tools/build_chapter_02_system_frequency_mathjax_component.py",
    "c2-06-special-filters-a": "full/tools/build_chapter_02_special_filters_mathjax_component.py",
    "c2-06-special-filters-b": "full/tools/build_chapter_02_special_filters_mathjax_component.py",
    "c2-06-special-filters-c": "full/tools/build_chapter_02_special_filters_mathjax_component.py",
}


def build_content_model(root: Path = ROOT, output_path: Path | None = None) -> dict:
    chapter = json.loads((root / "full/source/chapter_02.json").read_text(encoding="utf-8"))["chapter"]
    units = []
    for unit_id, unit_type, title, start, end, scope in UNIT_DEFINITIONS:
        units.append(
            {
                "id": unit_id,
                "unit_type": unit_type,
                "title": title,
                "source_pages": _pages(start, end),
                "source_scope": scope,
                "component_file": COMPONENT_FILE_BY_UNIT.get(unit_id),
                "source_text_status": "pending_reconciliation_with_original_courseware",
                "figure_status": "pending_visual_reconciliation_or_clean_source_reuse",
            }
        )

    all_pages = [page for unit in units for page in unit["source_pages"]]
    expected_pages = list(range(chapter["start_page"], chapter["end_page"] + 1))
    if all_pages != expected_pages:
        raise ValueError("chapter two source pages must be contiguous and allocated exactly once")

    model = {
        "chapter": chapter,
        "source_file": "full/source/chapter_02.json",
        "generation_contract": {
            "source_order_locked": True,
            "source_page_allocation_complete": True,
            "content_reconciliation_complete": False,
            "natural_reflow_required": True,
            "final_page_breaks_must_not_follow_source_page_breaks": True,
            "training_and_answers_frozen_until_all_chapter_bodies_are_complete": True,
            "incremental_pages": "retain only when they add readable technical information; otherwise merge into the complete readable state",
        },
        "units": units,
    }
    target = output_path or root / OUTPUT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return model


if __name__ == "__main__":
    print((ROOT / OUTPUT_PATH).resolve())
    build_content_model()
