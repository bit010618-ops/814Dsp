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
    ("src-0591-0591.png", "ch04-dit-fft-n8-flow.png", (45, 90, 1490, 650)),
    ("src-0622-0622.png", "ch04-dif-fft-n8-flow.png", (205, 220, 1325, 745)),
    ("src-0713-0713.png", "ch05-fir-direct-form.png", (330, 365, 1120, 600)),
)


COURSE_MARK_MASKS = {}


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
