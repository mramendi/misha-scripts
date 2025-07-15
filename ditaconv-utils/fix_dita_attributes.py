import sys
import os
import re

def process_dita_files(guid, doc_id, root_dir='.'):
    """
    Recursively finds and replaces attribute references in .dita files.
    """
    # CORRECTED PATTERN: Searches for {attribute} (no '$')
    # and allows for hyphens in the attribute name.
    pattern = re.compile(r"""
        \{                  # Match the literal opening brace '{'
        (                   # Start a capturing group for the attribute name
            [a-zA-Z0-9_-]+  # Match letters, numbers, underscores, AND hyphens
        )                   # End the capturing group
        \}                  # Match the literal closing brace '}'
        """, re.VERBOSE)

    # The replacement function that formats the new string
    def replacer(match):
        attribute_name = match.group(1).lower()
        return f'<ph conref="{guid}.dita/{doc_id}#{attribute_name}"></ph>'

    print(f"🔍 Starting scan in '{os.path.abspath(root_dir)}'...")
    files_processed = 0
    total_replacements = 0

    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.dita'):
                files_processed += 1
                filepath = os.path.join(dirpath, filename)
                print(f"--- Processing: {filepath}")

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Perform replacement and count occurrences
                    new_content, num_replacements = pattern.subn(replacer, content)
                    total_replacements += num_replacements

                    if num_replacements > 0:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"✅ Replaced {num_replacements} instance(s).")
                    else:
                        print("No matching attributes found in this file.")

                except Exception as e:
                    print(f"❌ Error processing file {filepath}: {e}")

    print("\n✨ Script finished.")
    print(f"Processed {files_processed} files and made {total_replacements} total replacements.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: Incorrect number of arguments.")
        print("Usage: python process_dita.py <GUID> <id>")
        sys.exit(1)

    guid_arg = sys.argv[1]
    id_arg = sys.argv[2]

    process_dita_files(guid_arg, id_arg)
