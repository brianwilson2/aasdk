import os
import shutil
import re

# Root folder of aasdk
root_dir = "."

# Patterns to update
patterns = {
    r"ReceivePromise::defer\(strand_\)": "ReceivePromise::defer(ioService_)",
    r"SendPromise::defer\(strand_\)": "SendPromise::defer(ioService_)",
}

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith((".cpp", ".hpp", ".ut.cpp")):
            file_path = os.path.join(subdir, file)
            
            # Read content
            with open(file_path, "r") as f:
                content = f.read()
            
            new_content = content
            for pat, repl in patterns.items():
                new_content = re.sub(pat, repl, new_content)
            
            # Only overwrite if changed
            if new_content != content:
                # Backup original
                shutil.copy(file_path, file_path + ".bak")
                with open(file_path, "w") as f:
                    f.write(new_content)
                print(f"Updated: {file_path}")
