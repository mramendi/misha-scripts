#!/usr.bin/python3

# This script edits files with the provided names (any number) to comment out (//) any lines starting with include::
# Kudos: Google Gemini

import sys
import fileinput

# Slices sys.argv to get file names. If empty, it reads from standard input.
files = sys.argv[1:]
if not files:
    print("Error: Please supply one or more file names.", file=sys.stderr)
    print("This command overwrites the files in place!", file=sys.stderr)
    sys.exit(1)

# fileinput loops over every line in every file provided.
# inplace=True redirects stdout (print) back into the original file.
try:
    for line in fileinput.input(files, inplace=True):
        # Use the more readable startswith() method.
        if line.startswith("include::"):
            # The 'line' variable includes a newline character, so end=''
            # prevents print() from adding a second one.
            print("//" + line, end='')
        else:
            print(line, end='')
except FileNotFoundError as e:
    print(f"Error: {e}", file=sys.stderr)
