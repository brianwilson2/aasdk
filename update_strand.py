#!/usr/bin/env python3
import os
import re
import shutil

# Root folder to start searching from
root_dir = "./src"

# Regex patterns
strand_decl_pattern = re.compile(r"(boost::asio::strand<).*?(>)\s+strand_;")
defer_pattern = re.compile(r"defer\((ioService_)\)")

# Walk through files
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith((".cpp", ".h")):
            path = os.path.join(subdir, file)

            with open(path, "r") as f:
                content = f.read()

            new_content = content

            # Update strand<> declaration
            new_content = strand_decl_pattern.sub(
                r"boost::asio::strand<boost::asio::io_context::executor_type> strand_;",
                new_content
            )

            # Update defer(ioService_) → defer(strand_.get_executor().context())
            new_content = defer_pattern.sub(
                r"defer(strand_.get_executor().context())",
                new_content
            )

            if new_content != content:
                bak_path = path + ".bak"
                shutil.copy2(path, bak_path)
                with open(path, "w") as f:
                    f.write(new_content)
                print(f"Updated: {path} (backup saved as {bak_path})")
