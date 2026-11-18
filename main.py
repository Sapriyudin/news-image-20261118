#!/usr/bin/env python3
"""news-image-20261118 — "THE WORLD IN ONE DAY".

Entry for the make.fun bounty "Sum up 18 November's world news in one
image". The image is a front-page newspaper summing up the world news of
Wednesday 18 November 2026: the Crimea bridge cut in two, the Gulf drone
interceptions, Trump in Manila, Nvidia's record quarter, Britain's
settlement sanctions, the Canada-China trade deals, Cyclone Akvan, and
Dhoni's IPL retirement — with a world map of where it happened and a
"day in numbers" box.

The image is pre-rendered by gen.py (PIL, run locally at build time).
This file is stdlib-only: it just copies the pre-rendered entry.png to
the output directory the harness asks for.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "."))
    src = HERE / "entry.png"
    if not src.is_file():
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    data = src.read_bytes()
    if not data.startswith(PNG_MAGIC) or len(data) == 0:
        print("entry.png is not a valid PNG", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")
    print("wrote", out_dir / "entry.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
