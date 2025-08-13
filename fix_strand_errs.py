import os
import re
import shutil

ROOT_DIR = './'
EXTENSIONS = ['.cpp', '.hpp', '.h', '.c']

# Patterns to fix:
# Replace strand_.get_executor().context() -> strand_.get_io_context()
# You can tweak this if you want the opposite.

def fix_strand_usage(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Backup original file
    shutil.copy2(filepath, filepath + '.bak')

    # Replace pattern
    fixed_content = re.sub(r'strand_\.get_executor\(\)\.context\(\)', 'strand_.get_io_context()', content)

    if fixed_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f'[Fixed strand usage] {filepath}')

def walk_and_fix_strand(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                fix_strand_usage(os.path.join(subdir, file))

if __name__ == '__main__':
    walk_and_fix_strand(ROOT_DIR)
    print("Finished fixing strand usage.")
