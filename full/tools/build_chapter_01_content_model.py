from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = Path("full/source/chapter_01_content_model.json")


def _pages(start: int, end: int) -> list[int]:
    return list(range(start, end + 1))


UNIT_DEFINITIONS = [
    ("c1-opening", "chapter_opening", "第一章导览", 1, 1, "将原课件四节目录改排为本章开篇导览，保留四节名称和原始顺序。"),
    ("c1-01-origin", "textbook_section", "1.1 离散时间信号的由来", 2, 8, "保留时域采样、采样间隔、采样频率与音频采样率实例。"),
    ("c1-01-representations", "textbook_section", "1.1 离散时间信号的表示方法", 9, 15, "保留数列、函数、图形和单位抽样序列四种表示。"),
    ("c1-01-operations", "textbook_section", "1.1 离散时间信号的基本运算", 16, 30, "保留和、积、移位、反褶、累加、差分、尺度、能量和平均功率。"),
    ("c1-02-matlab-sequence", "excluded_source_scope", "1.1 MATLAB 下序列运算的实现（不纳入讲义）", 31, 44, "用户明确限定本讲义仅覆盖 DSP 基础知识；本单元及其 MATLAB 绘图、函数和音频实验内容全部不纳入讲义。"),
    ("c1-01-typical-sequences", "textbook_section", "1.1 几种常用的典型序列", 45, 57, "保留单位抽样、矩形、阶跃、实指数、正弦和复指数序列。"),
    ("c1-01-periodicity", "textbook_section", "1.1 离散时间序列的周期性", 58, 67, "保留周期定义、周期求解方法与正弦序列周期性。"),
    ("c1-02-linearity", "textbook_section", "1.2 离散时间系统的线性性质", 68, 76, "将原章节导览与线性系统判定例题连续排版。"),
    ("c1-02-time-invariance", "textbook_section", "1.2 离散时间系统的移不变性质", 77, 84, "保留移不变定义、移位比较法和相关例题。"),
    ("c1-02-convolution-basics", "textbook_section", "1.2 LSI 系统的时域求解：线性卷积（基础）", 85, 97, "保留 LSI、单位抽样响应、卷积和定义及计算步骤。"),
    ("c1-02-convolution-properties", "textbook_section", "1.2 LSI 系统的时域求解：卷积性质与应用", 98, 114, "保留卷积规则、相关、应用例题和图解。"),
    ("c1-02-causal-stable", "textbook_section", "1.2 离散时间系统的因果性及稳定性", 115, 123, "保留一般系统与 LSI 系统的因果性、稳定性判据和例题。"),
    ("c1-03-difference-equation", "textbook_section", "1.3 常系数线性差分方程", 124, 133, "保留通式、四种求解法、因果和非因果迭代解、结构及 MATLAB filter。"),
    ("c1-04-sampling-theorem-1", "textbook_section", "1.4 时域采样定理", 134, 149, "保留理想采样、频域周期延拓、无混叠和混叠、采样定理。"),
    ("c1-04-sampling-theorem-2", "textbook_section", "1.4 采样定理的工程应用与带通信号采样", 150, 159, "保留抗混叠滤波、音频实例和带通信号采样。"),
    ("c1-04-sampling-recovery", "textbook_section", "1.4 时域采样信号的恢复", 160, 167, "保留理想低通重构、内插函数和恢复过程图解。"),
    ("c1-04-analog-digital-chain", "textbook_section", "1.4 模拟信号的数字处理方法", 168, 176, "保留前置滤波、A/D、DSP、D/A、平滑滤波、零阶保持及处理链图解。"),
    ("c1-04-applications-and-close", "chapter_case", "1.4 采样认知案例与本章收束", 177, 185, "保留奈奎斯特、香农、车轮视觉混叠和透过现象看本质的课程收束内容。"),
]


DIRECT_REWRITE_UNIT_BY_PAGE = {
    20: "c1-01-operations",
    129: "c1-03-difference-equation",
    130: "c1-03-difference-equation",
    171: "c1-04-analog-digital-chain",
}
INCREMENTAL_GROUPS_BY_UNIT = {
    "c1-04-sampling-theorem-1": [[142, 143]],
    "c1-04-sampling-recovery": [[164, 165]],
}
COMPONENT_FILE_BY_UNIT = {
    "c1-01-representations": "full/source/chapter_01_representation_component.json",
    "c1-01-operations": "full/source/chapter_01_operations_component.json",
    "c1-01-typical-sequences": "full/source/chapter_01_typical_sequences_component.json",
    "c1-01-periodicity": "full/source/chapter_01_periodicity_component.json",
    "c1-02-linearity": "full/source/chapter_01_linearity_component.json",
    "c1-02-time-invariance": "full/source/chapter_01_time_invariance_component.json",
    "c1-02-convolution-basics": "full/source/chapter_01_convolution_basics_component.json",
    "c1-02-convolution-properties": "full/source/chapter_01_convolution_properties_component.json",
    "c1-02-causal-stable": "full/source/chapter_01_causal_stable_component.json",
}


def build_content_model(root: Path = ROOT, output_path: Path | None = None) -> dict:
    chapter = json.loads((root / "full/source/chapter_01.json").read_text(encoding="utf-8"))["chapter"]
    direct = json.loads((root / "full/source/chapter_01_direct_rewrites.json").read_text(encoding="utf-8"))
    direct_pages = {block["source_page"] for block in direct["blocks"]}

    if direct_pages != set(DIRECT_REWRITE_UNIT_BY_PAGE):
        raise ValueError("direct rewrite inventory is not aligned with the chapter one placement map")

    units = []
    for unit_id, unit_type, title, start, end, scope in UNIT_DEFINITIONS:
        source_pages = _pages(start, end)
        excluded = unit_id == "c1-02-matlab-sequence"
        units.append(
            {
                "id": unit_id,
                "unit_type": unit_type,
                "title": title,
                "source_pages": source_pages,
                "source_scope": scope,
                "direct_rewrite_source_pages": [page for page in source_pages if DIRECT_REWRITE_UNIT_BY_PAGE.get(page) == unit_id],
                "incremental_page_groups": INCREMENTAL_GROUPS_BY_UNIT.get(unit_id, []),
                "component_file": COMPONENT_FILE_BY_UNIT.get(unit_id),
                "source_text_status": "excluded_by_user_scope_2026-07-22" if excluded else "must_reconcile_with_original_courseware",
                "figure_status": "not_applicable_excluded_by_user_scope" if excluded else "must_visually_verify_or_redraw_before_final_layout",
            }
        )

    all_pages = [page for unit in units for page in unit["source_pages"]]
    if all_pages != list(range(chapter["start_page"], chapter["end_page"] + 1)):
        raise ValueError("chapter one source pages must be contiguous and unique")

    model = {
        "chapter": chapter,
        "source_file": "full/source/chapter_01.json",
        "direct_rewrite_component_file": "full/source/chapter_01_direct_rewrites.json",
        "generation_contract": {
            "source_order_locked": True,
            "all_source_pages_represented_once": True,
            "natural_reflow_required": True,
            "final_page_breaks_must_not_follow_source_page_breaks": True,
            "incremental_pages": "retain as separately represented source content unless final visual review proves full containment",
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
