# output doc for all YAML Pipelines tasks listed in arguments to one module named tasks.adoc

import yaml
import sys

def task_yaml_to_doc_file(fname,outfile):
    y = yaml.safe_load(open(fname,"r"))

    task_name = y["metadata"]["name"]
    outfile.write('[discrete]\n')
    outfile.write(f'[id="op-taskref-{task_name}_{{context}}"]\n')
    outfile.write(f"== {task_name}\n\n")

    task_desc = y["spec"]["description"].strip()
    task_pos = task_desc.lower().find("task")
    if task_pos >= 0:
        task_desc = task_desc[task_pos+5:]
    outfile.write(f"The `{task_name}` task {task_desc}\n\n")

    outfile.write(f".Supported parameters for the `{task_name}` task\n")
    outfile.write('[options="header"]\n')
    outfile.write('|===\n')
    outfile.write('| Parameter | Description | Type | Default value\n')

    for param in y["spec"]["params"]:

        # work out default
        dflt = ""
        if "default" in param and len(param["default"])>0:
            if param["type"].strip() == "array":
                nwln = ""
                for default_entry in param["default"]:
                    dflt += nwln+"`- "+default_entry+"`"
                    nwln = "\n"
            else:
                dflt = f'`{param["default"].strip()}`'

        outfile.write(f'|`{param["name"].strip()}` |{param["description"].strip()} |`{param["type"].strip()}` |{dflt} \n')

    outfile.write('|===\n\n')

    if "workspaces" in y["spec"]:
        if len(y["spec"]["workspaces"]) > 0:

            outfile.write(f".Supported workspaces for the `{task_name}` task\n")
            outfile.write('[options="header"]\n')
            outfile.write('|===\n')
            outfile.write('| Workspace | Description \n')

            for wsp in y["spec"]["workspaces"]:
                outfile.write(f'|`{wsp["name"].strip()}` |{wsp["description"].strip().replace("\n"," ").replace( "  "," ")} \n')

            outfile.write('|===\n\n')



def main():
    outfile = open("tasks.adoc","w")
    for fname in sys.argv[1:]:
        print (f"Processing {fname}")
        task_yaml_to_doc_file(fname,outfile)
    outfile.close()

if __name__ == "__main__":
    main()
