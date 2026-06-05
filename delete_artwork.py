"""Remove artwork entries from index.html and delete image files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"


def remove_gallery_item(html: str, href: str) -> str:
    escaped = re.escape(href)
    pattern = rf"\s*<li[^>]*>\s*<a href=\"{escaped}\"[^>]*>.*?</a>\s*</li>"
    return re.sub(pattern, "", html, count=1, flags=re.DOTALL)


def deletion_paths(href: str, src: str | None) -> list[Path]:
    paths: list[Path] = []
    if href.startswith("images/"):
        paths.append(ROOT / href)
    if src and src.startswith("images/") and ROOT / src not in paths:
        paths.append(ROOT / src)
    return paths


def delete_files(paths: list[Path]) -> None:
    for path in paths:
        if path.exists():
            path.unlink()
            print(f"Deleted {path.relative_to(ROOT)}")
        else:
            print(f"Not found: {path.relative_to(ROOT)}")


def apply_deletions(deletions: list[dict[str, str]]) -> None:
    if not INDEX.exists():
        raise FileNotFoundError(f"Missing {INDEX}")

    html = INDEX.read_text(encoding="utf-8")
    all_paths: list[Path] = []

    for entry in deletions:
        href = entry.get("href", "")
        src = entry.get("src", "")
        if not href:
            continue
        html = remove_gallery_item(html, href)
        all_paths.extend(deletion_paths(href, src))

    INDEX.write_text(html, encoding="utf-8")
    print(f"Updated {INDEX.name}")

    for path in dict.fromkeys(all_paths):
        delete_files([path])


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python delete_artwork.py gallery-deletion.json")

    payload_path = Path(sys.argv[1])
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    deletions = payload.get("deletions", [])
    if not deletions:
        raise SystemExit("No deletions found in JSON file.")

    apply_deletions(deletions)


if __name__ == "__main__":
    main()
