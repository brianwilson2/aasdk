import os
import re

# Folder to start from
root_dir = './'  # adjust if needed

# Patterns to replace
replacements = [
    (r'#include\s*<f1x/aasdk/Channel/IChannel.hpp>', ''),  # Remove IChannel include
    (r'#include\s*<f1x/aasdk/Channel/SendPromise.hpp>', ''),  # Remove SendPromise include
    (r'#include\s*<f1x/aasdk/Channel/ReceivePromise.hpp>', ''),  # Remove ReceivePromise include
]

# We'll add this one if any of the above are found
add_promise_include = '#include <f1x/aasdk/Channel/Promise.hpp>\n'

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(('.cpp', '.hpp', '.h')):
            file_path = os.path.join(subdir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if any old includes exist
            if any(re.search(pattern, content) for pattern, _ in replacements):
                # Remove old includes
                for pattern, replacement in replacements:
                    content = re.sub(pattern, replacement, content)

                # Add new include at top (after other includes)
                lines = content.splitlines()
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.startswith('#include'):
                        insert_pos = i + 1

                # Avoid duplicate insertion
                if add_promise_include.strip() not in content:
                    lines.insert(insert_pos, add_promise_include.strip())
                    content = '\n'.join(lines)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'Updated includes in: {file_path}')
