#!/usr/bin/env python3
"""Print the package version (``__version__`` from the package __init__)."""
import pathlib
import re
import sys

INIT = pathlib.Path("src/PyReprism/__init__.py")


def main() -> int:
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']',
                      INIT.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        print("could not find __version__ in", INIT, file=sys.stderr)
        return 1
    print(match.group(1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
