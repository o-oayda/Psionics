#!/usr/bin/env python3
"""Copy generated Markdown powers to the local compendium directory."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SOURCE_DIR = Path("md_powers")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy generated Markdown powers to the compendium directory."
    )
    parser.add_argument(
        "--target",
        required=True,
        help=(
            "Destination directory for Markdown files (e.g. ~/Documents/Sandtray/compendium/powers)."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    target_dir = Path(args.target).expanduser().resolve()

    if not SOURCE_DIR.exists():
        print(f"Source directory '{SOURCE_DIR}' not found; skipping copy.")
        return

    markdown_files = sorted(SOURCE_DIR.glob("*.md"))
    if not markdown_files:
        print(f"No Markdown files found in '{SOURCE_DIR}'.")
        return

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"Unable to create target directory '{target_dir}': {exc}", file=sys.stderr)
        return

    copied = 0
    for src_path in markdown_files:
        dest_path = target_dir / src_path.name
        try:
            shutil.copy2(src_path, dest_path)
            copied += 1
        except OSError as exc:
            print(f"Failed to copy '{src_path}' to '{dest_path}': {exc}", file=sys.stderr)

    if copied:
        print(f"Copied {copied} Markdown file(s) to '{target_dir}'.")
    else:
        print("No files were copied. See errors above for details.")


if __name__ == "__main__":
    main()
