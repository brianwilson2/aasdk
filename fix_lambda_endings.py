import os
import re
import shutil

# Folder to scan
ROOT_DIR = './'

# File extensions to scan
EXTENSIONS = ['.cpp', '.hpp', '.h', '.c']

# Regex to find lines ending lambda with '});' or '}) ;' possibly with whitespace/newlines before semicolon
# This looks for lines that have }) followed by optional whitespace and a semicolon
LAMBDA_END_PATTERN = re.compile(r'\}\)\s*;')

# Regex to find boost::asio::dispatch(boost::asio::bind_executor or sendStrand_.dispatch etc (basic check)
DISPATCH_PATTERN = re.compile(r'(boost::asio::dispatch\s*\(\s*boost::asio::bind_executor|\.dispatch\s*\()')

def fix_lambda_endings(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If the file doesn't contain any dispatch or bind_executor, skip early
    if not DISPATCH_PATTERN.search(content):
        return False

    # Find all occurrences of '});' or '}) ;' that are *not* already '})) ;' or '}))'
    # We want to replace '});' -> '}));' only if it's a lambda closing after adding an extra '('
    # So we avoid messing with normal '});'

    # We do a negative lookbehind for ')' to avoid '}))'
    fixed_content = re.sub(r'(?<!\))\}\)\s*;', '}));', content)

    if fixed_content != content:
        # Backup original
        backup_path = filepath + '.bak'
        shutil.copy2(filepath, backup_path)
        print(f'[Backup] Created backup: {backup_path}')
        # Write fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f'[Fixed] Updated lambda endings in: {filepath}')
        return True
    return False

def walk_and_fix(root_dir):
    fixed_files = 0
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                full_path = os.path.join(subdir, file)
                if fix_lambda_endings(full_path):
                    fixed_files += 1
    print(f'\nDone! Fixed {fixed_files} file(s).')

if __name__ == '__main__':
    print('Starting lambda endings fixer...')
    walk_and_fix(ROOT_DIR)
