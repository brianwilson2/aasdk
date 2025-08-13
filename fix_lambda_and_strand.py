import os
import re
import shutil

ROOT_DIR = '.'  # Change if needed
EXTENSIONS = ['.cpp', '.hpp', '.h', '.c']

# Patterns to fix
LAMBDA_ENDING_PATTERN = re.compile(r'\}\)\s*;\s*\)')
STRAND_GET_IO_SERVICE_PATTERN = re.compile(r'strand_\.get_io_service\s*\(\s*\)')

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fixed_content = content

    # Fix lambda endings: replace patterns like })) ;); with }));
    # We replace all occurrences of '})) ;);' or similar with '}));'
    fixed_content = re.sub(r'\}\)\s*;\s*\)', '}));', fixed_content)

    # Fix strand_.get_io_service() to strand_.get_executor().context()
    fixed_content = STRAND_GET_IO_SERVICE_PATTERN.sub('strand_.get_executor().context()', fixed_content)

    if fixed_content != content:
        backup_path = filepath + '.bak'
        shutil.copy2(filepath, backup_path)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f'[Fixed] {filepath} (backup saved as {backup_path})')
        return True
    return False

def walk_and_fix(root_dir):
    fixed_files = 0
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                full_path = os.path.join(subdir, file)
                try:
                    if fix_file(full_path):
                        fixed_files += 1
                except Exception as e:
                    print(f'[Error] Failed to fix {full_path}: {e}')
    print(f'\nDone! Fixed {fixed_files} file(s).')

if __name__ == '__main__':
    print('Starting fixes for lambda endings and strand_.get_io_service()...')
    walk_and_fix(ROOT_DIR)
