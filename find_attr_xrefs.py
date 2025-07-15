#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scans AsciiDoc (*.adoc) files for cross-references (xrefs) where the link
contains a '{' character, which typically signifies an attribute.

Usage:
  - Run in the current directory:
    python find_attr_xrefs.py

  - Specify a directory:
    python find_attr_xrefs.py /path/to/your/docs

  - Recurse into subdirectories:
    python find_attr_xrefs.py -r /path/to/your/docs

Kudos: Google Gemini
"""

import argparse
import re
from pathlib import Path
import sys

def find_xrefs_with_attributes(directory: str, recurse: bool):
    """
    Finds and prints adoc files and the specific xrefs containing attributes.

    Args:
        directory (str): The path to the directory to search.
        recurse (bool): If True, search subdirectories recursively.
    """
    base_path = Path(directory)
    if not base_path.is_dir():
        print(f"Error: Directory not found at '{directory}'")
        sys.exit(1)

    # Use rglob for recursive search, glob otherwise.
    file_iterator = base_path.rglob('*.adoc') if recurse else base_path.glob('*.adoc')

    # Regex to find xrefs where the link part contains '{'.
    # Uses re.VERBOSE for readability.
    xref_pattern = re.compile(r"""
    ( # Start of capturing group for the whole match
        # --- Match Style 1: xref:link[text] ---
        xref:             # Literal "xref:"
        [^\[\n]*?         # Part of the link before '{' (non-greedy, no brackets/newlines)
        \{                # The required literal curly brace
        [^\[\n]* # Part of the link after '{' (no brackets/newlines)
        \[                # Literal opening square bracket for the text
        .*?               # The link text (non-greedy)
        \]                # Literal closing square bracket

        | # OR

        # --- Match Style 2: <<link,text>> ---
        <<                # Literal "<<"
        [^,>\n]*?         # Part of the link before '{' (non-greedy, no comma, >, or newline)
        \{                # The required literal curly brace
        [^,>\n]* # Part of the link after '{' (no comma, >, or newline)
        (?:               # Optional non-capturing group for the link text
            ,             # A literal comma separating link and text
            .*?           # The link text (non-greedy)
        )?                # Make the text part optional
        >>                # Literal ">>"
    )
    """, re.VERBOSE)

    found_any = False
    for file_path in file_iterator:
        try:
            content = file_path.read_text(encoding='utf-8')
            matches = xref_pattern.findall(content)

            if matches:
                if not found_any:
                    found_any = True
                
                print(f"\n## {file_path}")
                for match in matches:
                    print(f"  - {match.strip()}")

        except Exception as e:
            print(f"\n## {file_path}")
            print(f"  - Error reading file: {e}")

def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(
        description="Find AsciiDoc xrefs with attributes in the link.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help="Directory to search for *.adoc files (defaults to current directory)."
    )
    parser.add_argument(
        '-r', '--recurse',
        action='store_true',
        help="Recursively search subdirectories."
    )
    args = parser.parse_args()

    find_xrefs_with_attributes(args.directory, args.recurse)

if __name__ == "__main__":
    main()

