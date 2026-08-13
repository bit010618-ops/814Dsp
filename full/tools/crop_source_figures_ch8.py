"""Create clean, individually bounded chapter-eight technical figure crops."""
from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp" / "source-ch8"
DESTINATION = ROOT / "full" / "assets" / "source-figures"


# Each box is derived from its own slide. The bounds retain the complete
# technical diagram and intentionally omit only surrounding course-slide chrome.
CROPS = (
    ("page-1020.png", "ch08-decimation-spectrum.png", (46, 14, 1058, 608)),
    ("page-1024.png", "ch08-decimator-structure.png", (220, 120, 790, 202)),
    ("page-1033.png", "ch08-interpolator-structure.png", (196, 130, 906, 598)),
    ("page-1041.png", "ch08-rational-converter.png", (80, 350, 1025, 595)),
)


def crop_all(destination: Path = DESTINATION) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for source_name, output_name, box in CROPS:
        source = SOURCE / source_name
        output = destination / output_name
        if not source.is_file():
            raise FileNotFoundError(source)
        with Image.open(source) as image:
            image.crop(box).convert("RGB").save(output, optimize=True)
        outputs.append(output)
    return outputs


if __name__ == "__main__":
    for path in crop_all():
        print(path)
