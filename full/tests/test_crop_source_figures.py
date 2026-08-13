from pathlib import Path

from PIL import Image


def test_source_figure_crops_exclude_complete_course_slide_shell(tmp_path: Path, monkeypatch):
    from full.tools import crop_source_figures as cropper

    monkeypatch.setattr(cropper, "DESTINATION", tmp_path)
    outputs = cropper.crop_all()

    assert len(outputs) == 2
    assert all(output.is_file() for output in outputs)
    # The original lecture slides are 1534 by 863, so every crop must discard
    # some surrounding course-slide chrome rather than replay a complete slide.
    assert all(Image.open(output).size != (1534, 863) for output in outputs)


def test_crops_exclude_slide_explanations_and_keep_only_technical_bodies():
    """Lecture annotations and slide furniture are not handout illustrations."""
    from full.tools import crop_source_figures as cropper

    boxes = {output: box for _, output, box in cropper.CROPS}

    # Remove the DIT slide's bottom calculation banner and the FIR slide's
    # explanatory bullet list; neither is part of the structural drawing.
    assert boxes["ch04-dit-fft-n8-flow.png"] == (75, 100, 1350, 645)
    assert boxes["ch04-dif-fft-n8-flow.png"] == (220, 240, 1310, 720)
