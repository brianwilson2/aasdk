import os
import re

root_dir = '/home/brian/aasdk/src'  # adjust if needed

pattern = re.compile(r'promise_->(resolve|reject)\s*\((.*)\);')

results = []

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(('.cpp', '.cxx', '.cc', '.h', '.hpp')):
            path = os.path.join(subdir, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    match = pattern.search(line)
                    if match:
                        action = match.group(1)
                        arg = match.group(2).strip()
                        results.append((path, i, action, arg))

print(f"Found {len(results)} promise->resolve/reject calls:\n")

for path, line_no, action, arg in results:
    print(f"{path}:{line_no}: promise_->{action}({arg})")
