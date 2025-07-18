#!/usr.bin/python3

# This script edits files with the provided names (any number) to comment out (//) any lines starting with include::
# It also outputs a warning if a file has any text after any includes
# (not blank, not commented out with //)

import sys
import os

# Slices sys.argv to get file names. If empty, it reads from standard input.
files = sys.argv[1:]
if not files:
    print("Error: Please supply one or more file names.", file=sys.stderr)
    print("This command overwrites the files in place!", file=sys.stderr)
    sys.exit(1)

for filename in files:
    if not os.path.isfile(filename):
        print(f"{filename} does not exist or is not a regular file")
        continue
    backupname=filename+".backup"
    while os.path.exists(backupname):
        backupname+=".1"
    try:
        os.rename(filename,backupname)
    except Exception as e:
        print(f"Exception while renaming {filename} to {backupname}: {e}")
        continue
    try:
        with open(backupname) as f:
            lines=f.readlines()
    except Exception as e:
        print(f"Exception while reading {backupname}: {e}")
        continue

    try:
        seen_include = False
        warning_printed = False
        with open(filename,"w") as f:
            for line in lines:
                if line.startswith("include::"):
                    line = "//"+line
                    seen_include = True
                elif seen_include and line.strip()!="" and not line.startswith("//") and not line.startswith("ifdef::") and not line.startswith("ifndef::") and not warning_printed:
                    print(f"WARNING: {filename} has possible texts after includes, check if you need to split it")
                f.write(line)
    except Exception as e:
        print(f"Exception while writing {filename}, original content saved as {backupname}: {e}")
        continue
    try:
        os.remove(backupname)
    except Exception as e:
        print(f"Exception removing {backupname}, processing is not affected")
        print(e)
        continue
