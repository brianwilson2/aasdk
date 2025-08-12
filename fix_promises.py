import os
import re
import shutil

root_dir = '/home/brian/aasdk/include/f1x/aasdk'
backup_dir = '/home/brian/aasdk/include_backup'

pattern = re.compile(r'\b(SendPromise|ReceivePromise)::Pointer')

def fix_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    changed = False
    new_lines = []
    for line in lines:
        if pattern.search(line) and 'messenger::' not in line:
            line = re.sub(r'\b(SendPromise|ReceivePromise)::Pointer', r'messenger.\1::Pointer', line)
            line = line.replace('messenger.', 'messenger::')  # fix dot to ::
            changed = True
        new_lines.append(line)

    if changed:
        # Backup file
        rel_path = os.path.relpath(filepath, root_dir)
        backup_path = os.path.join(backup_dir, rel_path)
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(filepath, backup_path)
        print(f'Backed up: {backup_path}')

        # Write fixed file
        with open(filepath, 'w') as f:
            f.writelines(new_lines)
        print(f'Fixed: {filepath}')

for subdir, _, files in os.walk(root_dir):
    for filename in files:
        if filename.endswith(('.hpp', '.cpp', '.h', '.cc')):
            fix_file(os.path.join(subdir, filename))
