#!/usr/bin/env python3
"""Print the CHANGELOG.md section for a given version.

Usage: ``python .github/scripts/changelog_notes.py 0.2.0``

Extracts the body under ``## [0.2.0] ...`` up to the next ``## [`` heading.
Falls back to a generic line if the version has no changelog section.
"""
import pathlib
import re
import sys

CHANGELOG = pathlib.Path("CHANGELOG.md")


def notes_for(version: str, text: str) -> str:
    pattern = re.compile(
        r"^##\s*\[" + re.escape(version) + r"\][^\n]*\n(.*?)(?=^##\s*\[|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if match:
        body = match.group(1).strip()
        if body:
            return body
    return f"Release {version}."


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: changelog_notes.py <version>", file=sys.stderr)
        return 2
    version = sys.argv[1]
    text = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
    print(notes_for(version, text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
