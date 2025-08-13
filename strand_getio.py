import os

ROOT_DIR = './'
OLD_CALL = 'strand_.get_io_service()'
NEW_CALL = 'strand_.get_executor().context()'

def replace_io_service():
    for subdir, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(('.cpp', '.hpp', '.h')):
                path = os.path.join(subdir, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if OLD_CALL in content:
                    new_content = content.replace(OLD_CALL, NEW_CALL)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Fixed {path}')

if __name__ == '__main__':
    replace_io_service()
