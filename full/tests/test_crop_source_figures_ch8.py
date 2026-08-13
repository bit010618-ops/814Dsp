from pathlib import Path


def test_chapter_eight_technical_figure_crops_are_reproducible(tmp_path: Path):
    from full.tools import crop_source_figures_ch8 as cropper

    output_paths = cropper.crop_all(destination=tmp_path)

    assert [path.name for path in output_paths] == [
        "ch08-decimation-spectrum.png",
        "ch08-decimator-structure.png",
        "ch08-interpolator-structure.png",
        "ch08-rational-converter.png",
    ]
    for path in output_paths:
        assert path.is_file()
        assert path.stat().st_size > 10_000
