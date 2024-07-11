#!/usr/bin/python3

# This script extracts YAML scripts from modules
# Plase it in the modules directory and run it
# It scans all *.adoc files for YAML sources moarked with [source,yaml]
# A file named extracted.yaml is output, containing all the snippets with the file names they are from
# Subdirectories ar NOT scanned

import os

def comment_out_callouts_ellipses(in_s):
    unprocessed = in_s
    processed_left = ""

    if unprocessed.strip().find("...") == 0:
        return("#"+unprocessed)

    while True:
        pos = unprocessed.find("<")
        if pos == -1:
            return (processed_left+unprocessed)

        processed_left += unprocessed[:pos]
        unprocessed = unprocessed[pos:]
        callout = True
        i = 1
        while (i<len(unprocessed)) and (unprocessed[i]!=">"):
            if not unprocessed[i].isdigit():
                callout = False
                break
            i+=1
        if callout:
            processed_left += "#"
        processed_left += unprocessed[:i+1]
        unprocessed = unprocessed[i+1:]






out = open("extracted.yaml","w")

for entry in os.scandir("."):
    if entry.is_dir():
        continue
    fname=entry.name
    if fname.find(".adoc")<0:
        continue
    file_lines=open(fname).readlines()

    while len(file_lines)>0:
        line = file_lines.pop(0)

        if line.replace(" ","").find("[source,yaml") >= 0:
            try:
                tearline = file_lines.pop(0)
                while (tearline.strip() != "----"):
                    tearline = file_lines.pop(0)

                out.write("# "+fname+"\n")
                scriptline = file_lines.pop(0)
                while (scriptline.strip() != "----"):

                    out.write(comment_out_callouts_ellipses(scriptline))
                    scriptline = file_lines.pop(0)
            except IndexError:
                print(f"WARNING: source block ended prematurely in {fname}")
            out.write("\n")
