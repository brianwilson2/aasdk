import os
import re

# Folder to scan — adjust as needed
root_dir = '.'

# Regex to find problematic lines ending with "}))" but missing a semicolon before closing
pattern = re.compile(r'(\}\))\s*(?!;)')  # matches '})' not followed by ;

fix_count = 0

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(('.cpp', '.hpp', '.h', '.cxx', '.cc')):
            path = os.path.join(subdir, file)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            file_changed = False
            for line in lines:
                # Fix lines where '}))' not followed by ';'
                if pattern.search(line):
                    new_line = re.sub(r'\}\)\s*(?!;)', '})) ;', line)
                    if new_line != line:
                        fix_count += 1
                        print(f"Fixed missing semicolon in {path.strip('./')} : {line.strip()}")
                        line = new_line
                        file_changed = True
                new_lines.append(line)

            if file_changed:
                with open(path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)

if fix_count == 0:
    print("No missing semicolons found.")
else:
    print(f"Total missing semicolons fixed: {fix_count}")

