from __future__ import annotations

import json
import re
from pathlib import Path

from pypdf import PdfReader


TOPICS = (
    (r"FFT|快速傅里叶|基[-－]?2", 4, "FFT"),
    (r"DFT|DFS|离散傅里叶|频谱分析|栅栏|重叠相加|重叠保留", 3, "DFT"),
    (r"抽取|内插|多采样率|采样频率变换|零值插入", 8, "多采样率"),
    (r"窗函数|等波纹|线性相位|FIR.*设计", 7, "FIR 设计"),
    (r"巴特沃斯|双线性|脉冲响应不变|IIR.*设计", 6, "IIR 设计"),
    (r"直接型|级联型|并联型|数字滤波器结构|FIR.*结构|IIR.*结构", 5, "滤波器结构"),
    (r"z\s*变换|z变换|零极点|收敛域|系统函数|频率响应|谐振器|陷波器|最小相位", 2, "z 变换与频域分析"),
    (r"离散.*系统|差分方程|循环卷积|线性卷积|时域采样", 1, "离散时间信号与系统"),
)


def classify_question(*, year: int, source_pages: list[int], text: str) -> dict:
    matches = [
        {"chapter": chapter, "topic": topic, "pattern": pattern}
        for pattern, chapter, topic in TOPICS
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    ]
    required_chapters = sorted({item["chapter"] for item in matches})
    if matches:
        placement_chapter = max(required_chapters)
        chapter = placement_chapter
        topic = matches[0]["topic"]
        confidence = 1.0
    else:
        chapter = None
        placement_chapter = None
        topic = None
        confidence = 0.0
    return {
        "year": year,
        "source_pages": source_pages,
        "chapter": chapter,
        "topic": topic,
        "required_chapters": required_chapters,
        "placement_chapter": placement_chapter,
        "confidence": confidence,
        "manual_review": confidence < 1.0,
        "matched_patterns": [item["pattern"] for item in matches],
    }


def build_exam_page_index(
    pages: list[dict], paper_starts: dict[int, int], end_page: int | None = None
) -> list[dict]:
    starts = sorted((page, year) for year, page in paper_starts.items())
    index = []
    for page in sorted(pages, key=lambda item: item["index"]):
        source_page = page["index"]
        if end_page is not None and source_page > end_page:
            continue
        matching_starts = [item for item in starts if item[0] <= source_page]
        if not matching_starts:
            continue
        _, year = matching_starts[-1]
        auto = classify_question(
            year=year,
            source_pages=[source_page],
            text=page.get("text", ""),
        )
        index.append(
            {
                "id": f"{year}-p{source_page}",
                "record_type": "source_page",
                "year": year,
                "source_page": source_page,
                "text": page.get("text", ""),
                "auto_classification": auto,
                "scope_status": "pending_manual_review",
            }
        )
    return index


def write_exam_page_index(
    pdf_path: Path,
    output_path: Path,
    paper_starts: dict[int, int],
    end_page: int | None = None,
) -> list[dict]:
    reader = PdfReader(str(pdf_path))
    pages = [
        {"index": index + 1, "text": page.extract_text() or ""}
        for index, page in enumerate(reader.pages)
    ]
    records = build_exam_page_index(pages, paper_starts, end_page=end_page)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return records
