import re
import sys

def fix_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    fixed_lines = []
    pattern = re.compile(r'\}\)\)\s*;\)\s*;')  # matches '})) ;);' with optional spaces

    for line in lines:
        if pattern.search(line):
            fixed_line = pattern.sub('}));', line)
            print(f'Fixed in {filename}: {line.strip()} -> {fixed_line.strip()}')
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)

    with open(filename, 'w') as f:
        f.writelines(fixed_lines)

if __name__ == "__main__":
    for fname in sys.argv[1:]:
        fix_file(fname)
