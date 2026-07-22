import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "full" / "tools"))

from build_chapter_01_content_model import build_content_model


def test_chapter_one_model_covers_each_original_page_once_in_original_order():
    model = build_content_model(ROOT)

    all_pages = [page for unit in model["units"] for page in unit["source_pages"]]
    assert all_pages == list(range(1, 186))
    assert model["chapter"]["title"] == "离散时间信号与系统"
    assert len(model["units"]) == 18


def test_chapter_one_model_anchors_verified_direct_rewrites_and_retained_incremental_pages():
    model = build_content_model(ROOT)
    by_id = {unit["id"]: unit for unit in model["units"]}

    assert by_id["c1-01-operations"]["direct_rewrite_source_pages"] == [20]
    assert by_id["c1-02-matlab-sequence"]["direct_rewrite_source_pages"] == []
    assert by_id["c1-02-matlab-sequence"]["source_text_status"] == "excluded_by_user_scope_2026-07-22"
    assert by_id["c1-03-difference-equation"]["direct_rewrite_source_pages"] == [129, 130]
    assert by_id["c1-04-analog-digital-chain"]["direct_rewrite_source_pages"] == [171]
    assert by_id["c1-opening"]["direct_rewrite_source_pages"] == []
    assert by_id["c1-01-representations"]["component_file"] == "full/source/chapter_01_representation_component.json"
    assert by_id["c1-01-operations"]["component_file"] == "full/source/chapter_01_operations_component.json"
    assert by_id["c1-01-typical-sequences"]["component_file"] == "full/source/chapter_01_typical_sequences_component.json"
    assert by_id["c1-01-periodicity"]["component_file"] == "full/source/chapter_01_periodicity_component.json"
    assert by_id["c1-02-linearity"]["component_file"] == "full/source/chapter_01_linearity_component.json"
    assert by_id["c1-02-time-invariance"]["component_file"] == "full/source/chapter_01_time_invariance_component.json"
    assert by_id["c1-02-convolution-basics"]["component_file"] == "full/source/chapter_01_convolution_basics_component.json"
    assert by_id["c1-04-sampling-theorem-1"]["incremental_page_groups"] == [[142, 143]]
    assert by_id["c1-04-sampling-recovery"]["incremental_page_groups"] == [[164, 165]]


def test_written_model_matches_builder_output(tmp_path):
    model = build_content_model(ROOT, output_path=tmp_path / "chapter_01_content_model.json")
    written = json.loads((tmp_path / "chapter_01_content_model.json").read_text(encoding="utf-8"))

    assert written == model
