from pathlib import Path

from PIL import Image


def test_source_figure_crops_exclude_complete_course_slide_shell(tmp_path: Path, monkeypatch):
    from full.tools import crop_source_figures as cropper

    monkeypatch.setattr(cropper, "DESTINATION", tmp_path)
    outputs = cropper.crop_all()

    assert len(outputs) == 9
    assert all(output.is_file() for output in outputs)
    # The original lecture slides are 1534 by 863, so every crop must discard
    # some surrounding course-slide chrome rather than replay a complete slide.
    assert all(Image.open(output).size != (1534, 863) for output in outputs)


def test_structure_crops_keep_the_full_parallel_and_cascade_diagrams(tmp_path: Path, monkeypatch):
    """Removing slide chrome must not trim formulas or the bottom structure paths."""
    from full.tools import crop_source_figures as cropper

    monkeypatch.setattr(cropper, "DESTINATION", tmp_path)
    outputs = {path.name: path for path in cropper.crop_all()}

    # The original technical drawings reach almost to the slide's lower blue
    # footer.  A smaller crop cuts the H_2(z) formula or the final FIR branch.
    assert Image.open(outputs["ch05-parallel-form.png"]).height >= 820
    assert Image.open(outputs["ch05-fir-cascade-form.png"]).height >= 530


def test_crops_start_before_the_parallel_and_frequency_sampling_text(tmp_path: Path, monkeypatch):
    """Figure-body prose must never be left half-visible at the crop edge."""
    from full.tools import crop_source_figures as cropper

    monkeypatch.setattr(cropper, "DESTINATION", tmp_path)
    outputs = {path.name: path for path in cropper.crop_all()}

    assert Image.open(outputs["ch05-parallel-form.png"]).height >= 820
    assert Image.open(outputs["ch05-frequency-sampling-form.png"]).height >= 650


def test_parallel_crop_keeps_the_full_width_but_masks_the_course_mark(tmp_path: Path, monkeypatch):
    from full.tools import crop_source_figures as cropper

    monkeypatch.setattr(cropper, "DESTINATION", tmp_path)
    outputs = {path.name: path for path in cropper.crop_all()}

    with Image.open(outputs["ch05-parallel-form.png"]) as image:
        assert image.size == (1534, 830)
        assert all(channel >= 245 for channel in image.getpixel((1400, 40))[:3])


def test_fir_cascade_crop_starts_at_the_complete_formula_not_a_partial_sentence():
    from full.tools import crop_source_figures as cropper

    boxes = {output: box for _, output, box in cropper.CROPS}
    assert boxes["ch05-fir-cascade-form.png"][1] >= 300
