"""Generate web-optimized display images in images/display/."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
IMAGES = ROOT / "images"
DISPLAY = IMAGES / "display"
INDEX = ROOT / "index.html"
MAX_WIDTH = 800
JPEG_QUALITY = 82

SRC_PATTERN = re.compile(r'href="(images/[^"]+)"')


def referenced_images() -> list[Path]:
    text = INDEX.read_text(encoding="utf-8")
    paths = sorted({match.group(1) for match in SRC_PATTERN.finditer(text)})
    return [ROOT / path for path in paths]


def resize_dimensions(width: int, height: int) -> tuple[int, int]:
    if width <= MAX_WIDTH:
        return width, height
    new_width = MAX_WIDTH
    new_height = max(1, round(height * (MAX_WIDTH / width)))
    return new_width, new_height


def has_transparency(image: Image.Image) -> bool:
    if image.mode in ("RGBA", "LA"):
        alpha = image.getchannel("A")
        return alpha.getextrema()[0] < 255
    if image.mode == "P" and "transparency" in image.info:
        return True
    return False


def save_display_image(source: Path, destination: Path) -> tuple[int, int]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    suffix = source.suffix.lower()

    with Image.open(source) as image:
        image.load()
        width, height = resize_dimensions(*image.size)
        if (width, height) != image.size:
            image = image.resize((width, height), Image.Resampling.LANCZOS)

        if suffix in {".jpg", ".jpeg"}:
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(
                destination,
                format="JPEG",
                quality=JPEG_QUALITY,
                optimize=True,
                progressive=True,
            )
        elif suffix == ".png":
            if has_transparency(image) and image.mode != "RGBA":
                image = image.convert("RGBA")
            elif not has_transparency(image) and image.mode != "RGB":
                image = image.convert("RGB")
            image.save(destination, format="PNG", optimize=True)
        else:
            raise ValueError(f"Unsupported image type: {source.name}")

    return source.stat().st_size, destination.stat().st_size


def main() -> None:
    sources = referenced_images()
    missing: list[str] = []
    before_total = 0
    after_total = 0
    created = 0

    for source in sources:
        if not source.exists():
            missing.append(str(source.relative_to(ROOT)))
            continue

        destination = DISPLAY / source.relative_to(IMAGES)
        before, after = save_display_image(source, destination)
        before_total += before
        after_total += after
        created += 1

    print(f"Created {created} display images in {DISPLAY.relative_to(ROOT)}")
    print(f"Original total: {before_total / 1024 / 1024:.1f} MB")
    print(f"Display total:  {after_total / 1024 / 1024:.1f} MB")
    print(f"Saved:          {(before_total - after_total) / 1024 / 1024:.1f} MB")

    if missing:
        raise SystemExit(f"Missing source images: {', '.join(missing)}")


if __name__ == "__main__":
    main()
