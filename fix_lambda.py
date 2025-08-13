import os
import re

ROOT = './src'

pattern = re.compile(r'\}\)\s*;\);')

for root, _, files in os.walk(ROOT):
    for file in files:
        if file.endswith(('.cpp', '.hpp', '.h', '.c')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            if pattern.search(content):
                fixed = pattern.sub('}));', content)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(fixed)
                print(f'Fixed lambda endings in {path}')
