#!/usr/bin/env python3
import os
import re
import shutil

# Set DRY_RUN=True to only preview changes
DRY_RUN = True

USB_SRC_DIR = './src/USB/'

# Pattern 1: lambda Promise errors
# Matches lambda in promise->then and replaces with correct capture
lambda_pattern = re.compile(
    r'(\.then\s*\(\s*)\[\s*this.*?\]\(.*?\)\s*mutable\s*{',
    re.DOTALL
)

lambda_replacement = r'\1[this, self = this->shared_from_this(), promise]('

# Pattern 2: hotplugRegisterCallback with extra args
hotplug_pattern = re.compile(
    r'(hotplugRegisterCallback\s*\([^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+),[^,]+\)',
    re.DOTALL
)

hotplug_replacement = r'\1)'

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content
    changed = False

    # Fix lambda Promises
    if lambda_pattern.search(new_content):
        new_content = lambda_pattern.sub(lambda_replacement, new_content)
        changed = True

    # Fix hotplugRegisterCallback
    if hotplug_pattern.search(new_content):
        new_content = hotplug_pattern.sub(hotplug_replacement, new_content)
        changed = True

    if changed:
        print(f"[{'DRY_RUN' if DRY_RUN else 'FIXED'}] {filepath}")
        if not DRY_RUN:
            # backup original
            bak_path = filepath + '.bak'
            shutil.copyfile(filepath, bak_path)
            with open(filepath, 'w') as f:
                f.write(new_content)

def main():
    for root, dirs, files in os.walk(USB_SRC_DIR):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.hpp'):
                path = os.path.join(root, file)
                process_file(path)

if __name__ == '__main__':
    main()
