import sys
import os
import os.path

if len(sys.argv)!=3:
    python("List files in a tree that match a change list.\nCompares ONLY FILE NAMES, in case directories change, so false positives are possible")
    print("Usage: files_in_change-list.py <directory> <change-list-file")

change_list_file=sys.argv[2]
change_list=open(change_list_file).read()

dir_path=sys.argv[1]
print(dir_path)

for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file in change_list:
            print(os.path.join(root,file))
