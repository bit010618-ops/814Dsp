"""Create bounded CZT technical-figure crops from the rendered course slides."""
from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp"
DESTINATION = ROOT / "full" / "assets" / "source-figures"


# (source render, output asset, left, top, right, bottom)
# The boxes retain each technical drawing but deliberately omit slide titles,
# institutional marks, footer/page numbers, and explanatory prose banners.
CROPS = (
    ("source-ch4-czt-0648.png", "ch04-czt-zplane-sampling.png", (160, 330, 950, 1230)),
    ("source-ch4-czt-0652.png", "ch04-czt-fft-convolution-flow.png", (350, 220, 2160, 890)),
)


def crop_all(destination: Path = DESTINATION) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for source_name, output_name, box in CROPS:
        source = SOURCE / source_name
        if not source.is_file():
            raise FileNotFoundError(source)
        output = destination / output_name
        with Image.open(source) as image:
            image.crop(box).convert("RGB").save(output, optimize=True)
        outputs.append(output)
    return outputs


if __name__ == "__main__":
    for path in crop_all():
        print(path)
