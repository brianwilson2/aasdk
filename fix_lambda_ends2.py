import os
import re
import shutil

ROOT_DIR = './'
EXTENSIONS = ['.cpp', '.hpp', '.h', '.c']

# Fix common lambda ending mistakes:
# Replace '})) ;);' or '})) ;' with '}))' or '});' correctly.

def fix_lambda_endings(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Backup original file
    shutil.copy2(filepath, filepath + '.bak')

    # Fix patterns:
    # 1) '})) ;);' -> '}));'
    content = re.sub(r'\}\}\)\s*;\s*\);', '}));', content)
    # 2) '})) ;' -> '}));'
    content = re.sub(r'\}\}\)\s*;', '}));', content)
    # 3) fix lonely '}); ;' -> '});'
    content = re.sub(r'\}\)\s*;\s*;', '});', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def walk_and_fix(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                fix_lambda_endings(os.path.join(subdir, file))

if __name__ == '__main__':
    walk_and_fix(ROOT_DIR)
    print("Lambda endings fixed, backups saved with .bak extension.")
