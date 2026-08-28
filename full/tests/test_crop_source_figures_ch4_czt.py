from pathlib import Path

from PIL import Image


def test_chapter_four_czt_technical_crops_are_reproducible(tmp_path: Path):
    from full.tools import crop_source_figures_ch4_czt as cropper

    output_paths = cropper.crop_all(destination=tmp_path)

    assert [path.name for path in output_paths] == [
        "ch04-czt-zplane-sampling.png",
        "ch04-czt-fft-convolution-flow.png",
    ]
    assert all(path.is_file() for path in output_paths)
    assert all(Image.open(path).width < 2560 for path in output_paths)
    assert all(Image.open(path).height < 1440 for path in output_paths)


def test_chapter_four_czt_crops_exclude_slide_chrome_and_explanatory_banners():
    from full.tools import crop_source_figures_ch4_czt as cropper

    boxes = {output: box for _, output, box in cropper.CROPS}

    assert boxes["ch04-czt-zplane-sampling.png"] == (160, 330, 950, 1230)
    assert boxes["ch04-czt-fft-convolution-flow.png"] == (350, 220, 2160, 890)
