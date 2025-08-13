import os
import re

SRC_DIR = './src'  # adjust if needed

promise_make_shared_pattern = re.compile(
    r'std::make_shared<(\w+::\w*Promise)>\(\s*\)'
)

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    matches = list(promise_make_shared_pattern.finditer(content))
    if not matches:
        return 0

    new_content = content
    for m in reversed(matches):
        promise_type = m.group(1)
        start, end = m.span()
        replacement = f'{promise_type}::defer(strand_)'
        new_content = new_content[:start] + replacement + new_content[end:]

    with open(filepath, 'w') as f:
        f.write(new_content)
    return len(matches)

def main():
    total_fixes = 0
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(('.cpp', '.hpp')):
                path = os.path.join(root, file)
                fixes = fix_file(path)
                if fixes:
                    print(f'Fixed {fixes} in {path}')
                    total_fixes += fixes

    if total_fixes == 0:
        print('No std::make_shared<...Promise>() calls found.')

if __name__ == '__main__':
    main()
