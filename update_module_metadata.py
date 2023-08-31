import os
import os.path

# do not look for assemblies in these directories
non_assembly_dirs=["modules","snippets","images","_attributes"]

# the assemblies for each module
modules_assemblies={}

# find assemblies and scan them for includes
for root,dirs,files in os.walk("."):
    if any(nad in root for nad in non_assembly_dirs):
        continue
    for file in files:
        if file.lower().endswith(".adoc"):
            # determine assembly pathname for metadata inclusion
            assy=os.path.join(root,file)
            if assy.startswith("./"):
                assy=assy[2:]
            # scan for includes of modules
            for line in open(os.path.join(root,file)).readlines():
                if line.startswith("include::"):
                    module=line[len("include::"):]
                    module=module[:module.index("[")]
                    if module.startswith("_attributes/"): continue
                    if module.startswith("snippets/"): continue
                    if not module.startswith("modules/"):
                        print(f"Strange include in {os.path.join(root,file)}")
                        print(line)
                        continue
                    module=module[len("modules/"):]
                    if not module in modules_assemblies:
                        modules_assemblies[module]=set()
                    modules_assemblies[module].add(assy)

# apply the metadata to modules
module_list=os.listdir("modules")
for module_file in module_list:
    if module_file.lower().endswith(".adoc"):
        if not module_file in modules_assemblies:
            print(f"{module_file} not found in any assemblies, file unchanged")
            continue
        #read the original module as lines
        orig_lines=open(os.path.join("modules", module_file)).readlines()

        #prepare new module lines - metadata comes first
        module_lines=["// This module is included in the following assemblies:\n"]
        for assy in modules_assemblies[module_file]:
            module_lines.append(f"// * {assy}\n")
        module_lines.append("\n")

        # process possible comments at the start of original to remove old metadata
        # performance won't be great
        while orig_lines[0].startswith("//"):
            # copy this comment to the new module IF it is not inclusion metadata
            try:
                comment_content=orig_lines[0][2:].strip()
            except IndexError: comment_content=""
            if not (comment_content=="" or comment_content.startswith("*") or "assembl" in comment_content):
                module_lines.append(orig_lines[0])
            orig_lines=orig_lines[1:]

        # skip all empty lines after the comments at the start
        while orig_lines[0].strip()=="":
            orig_lines=orig_lines[1:]

        # the rest of the original goes into the new module
        module_lines.extend(orig_lines)
        with open(os.path.join("modules", module_file),"w") as outfile:
            outfile.writelines(module_lines)

        # remove the module from the dictionary
        del modules_assemblies[module_file]

# If any modules remain in the dictionary, something went wrong
if len(modules_assemblies)>0:
    print("Modules not found:")
    for module in modules_assemblies:
        print(module)
