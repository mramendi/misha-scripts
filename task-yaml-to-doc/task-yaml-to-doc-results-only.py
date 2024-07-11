# output doc for all YAML Pipelines tasks listed in arguments to one module named tasks.adoc

import yaml
import sys

def task_yaml_to_doc_file(fname,outfile):
    y = yaml.safe_load(open(fname,"r"))

    task_name = y["metadata"]["name"]
    outfile.write('[discrete]\n')
    outfile.write(f'[id="op-taskref-{task_name}_{{context}}"]\n')
    outfile.write(f"== {task_name}\n\n")




    if "results" in y["spec"]:
        if len(y["spec"]["results"]) > 0:

            outfile.write(f".Results that the `{task_name}` task returns\n")
            outfile.write('[options="header"]\n')
            outfile.write('|===\n')
            outfile.write('| Result | Type | Description \n')

            for rslt in y["spec"]["results"]:
                outfile.write(f'|`{rslt["name"].strip()}` |`{rslt["type"].strip()}` |{rslt["description"].strip().replace("\n"," ").replace( "  "," ")} \n')

            outfile.write('|===\n\n')



def main():
    outfile = open("tasks-results.adoc","w")
    for fname in sys.argv[1:]:
        print (f"Processing {fname}")
        task_yaml_to_doc_file(fname,outfile)
    outfile.close()

if __name__ == "__main__":
    main()
