import os
import re

# Root folder to scan
root_dir = 'src'

# Regex to match strand_.dispatch or strand_.post calls
pattern = re.compile(r'(\bstrand_)\.(dispatch|post)\s*\(')

def fix_line(line):
    # Replace strand_.dispatch(  => boost::asio::dispatch(boost::asio::bind_executor(strand_, 
    # Replace strand_.post(      => boost::asio::post(boost::asio::bind_executor(strand_, 
    def repl(match):
        method = match.group(2)
        return f'boost::asio::{method}(boost::asio::bind_executor(strand_, '

    return pattern.sub(repl, line)

def process_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    changed = False
    new_lines = []
    for line in lines:
        if pattern.search(line):
            new_line = fix_line(line)
            if new_line != line:
                print(f'Fixing line in {filepath}:')
                print(f'  Before: {line.strip()}')
                print(f'  After:  {new_line.strip()}')
                changed = True
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if changed:
        with open(filepath, 'w') as f:
            f.writelines(new_lines)

def main():
    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith(('.cpp', '.hpp', '.h', '.cc', '.cxx')):
                filepath = os.path.join(subdir, filename)
                process_file(filepath)

if __name__ == '__main__':
    main()
