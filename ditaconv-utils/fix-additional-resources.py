# move additional resources from assembly to modules
# run ONLy on an assembly file

# PROOF OF CONCEPT/PROTOTYPE

# (no code was AI generated)

import sys
import os.path

(basepath,drop)=os.path.split(sys.argv[1])

with open(sys.argv[1]) as f:
    lines = f.readlines()

out_lines = []

while True:
    # Find ``.Additional resources`
    # if it is not found, put the rest of lines into out_lines and we're done
    n=0
    while n<len(lines):
        if lines[n].strip()==".Additional resources":
            break
        n+=1
    if n==len(lines):
        out_lines.extend(lines)
        break

    # lines[n] is .Additional resources

    # go up the list to find the include
    m=n-1
    while (m>=0) and (lines[m].strip().find("include::")!=0):
        m-=1
    if m<0:
        # include not found - warn, end processing gracefully; this should never happen
        print("ERROR: no include before .Additional resources in file",sys.argv[1])
        out_lines.extend(lines)
        break
    include_line=lines[m].strip() # we will use this to get the module file name

    # lines[m]
    # now everything up to the include, and the include itself too, gets into out_lines
    out_lines.extend(lines[:m+1])

    # find where the additional resources block ends
    q=m+1
    while q<len(lines):
        # we're looking for the next include OR heading
        if (lines[q].find("include::") == 0) or (lines[q].find("=") == 0):
            # we found it but now want to backtrack through any comments or [] definitions
            while (lines[q-1].find("//") == 0) or (lines[q-1].strip().find("[") == 0):
                q-=1
            # now q is the index of the first line NOT going into additional resources
            break
        q+=1

    # if the break in the previous loop did not trigger, now q==len(lines) which works too

    # if q<n there is no additional resources and this should never happen
    if q<n:
        print("ERROR: Additional resources block failed to calculate in file",sys.argv[1])
        out_lines.extend(lines[m+1:])
        break

    additional_resources=lines[m+1:q]
    lines=lines[q:]

    # now we add the additional_resources to the included file in question

    # this find will always succeed as include_line is searched for with ::
    filename_start=include_line.find("::")+2

    # if this find fails, warn - should never happen
    filename_end=include_line.find("[")
    if filename_end <= 0:
        print("ERROR: no [ found in module include line in file",sys.argv[1])
        print("line:",include_line)
        filename_end=len(include_line)

    module_filename=include_line[filename_start:filename_end]

    try:
        with open(os.path.join(basepath,module_filename),"a") as append_file:
            append_file.write("\n")
            append_file.writelines(additional_resources)
    except Exception as e:
        print("When writing to",module_filename,"exception occurred:",e)

# write assembly

try:
    with open(sys.argv[1],"w") as append_file:
        append_file.writelines(out_lines)
except Exception as e:
    print("When writing to",sys.argv[1],"exception occurred:",e)
