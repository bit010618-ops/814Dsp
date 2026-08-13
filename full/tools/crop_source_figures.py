"""Create clean technical-figure crops from the user-supplied course-slide renders.

The source slides are kept out of the handout as complete pages: their title bars,
school mark, and source-slide footer are not part of the handout figure itself.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp" / "source-figures-ch4ch5"
DESTINATION = ROOT / "full" / "assets" / "source-figures"


# (source image, destination image, left, top, right, bottom)
CROPS = (
    ("src-0591-0591.png", "ch04-dit-fft-n8-flow.png", (150, 100, 1360, 850)),
    ("src-0622-0622.png", "ch04-dif-fft-n8-flow.png", (205, 220, 1325, 745)),
    ("src-0673-0673.png", "ch05-direct-form-i.png", (120, 350, 1420, 825)),
    ("src-0692-0692.png", "ch05-cascade-form.png", (85, 260, 1450, 805)),
    ("src-0699-0699.png", "ch05-parallel-form.png", (0, 0, 1534, 830)),
    ("src-0713-0713.png", "ch05-fir-direct-form.png", (160, 350, 1260, 810)),
    ("src-0714-0714.png", "ch05-fir-cascade-form.png", (160, 300, 1260, 830)),
    ("src-0720-0720.png", "ch05-frequency-sampling-form.png", (160, 180, 1400, 830)),
    ("src-0731-0731.png", "ch05-fast-convolution-form.png", (115, 150, 1430, 745)),
)


COURSE_MARK_MASKS = {
    # This figure uses the full slide width for formulas and callouts.  Remove
    # only the isolated course mark, not the mathematical content beside it.
    "ch05-parallel-form.png": (1260, 0, 1534, 88),
}


def crop_all() -> list[Path]:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for source_name, output_name, box in CROPS:
        source = SOURCE / source_name
        output = DESTINATION / output_name
        if not source.is_file():
            raise FileNotFoundError(source)
        with Image.open(source) as image:
            cropped = image.crop(box).convert("RGB")
            mask = COURSE_MARK_MASKS.get(output_name)
            if mask:
                cropped.paste((255, 255, 255), mask)
            cropped.save(output, optimize=True)
        outputs.append(output)
    return outputs


if __name__ == "__main__":
    for path in crop_all():
        print(path)
