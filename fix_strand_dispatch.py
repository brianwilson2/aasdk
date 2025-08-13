import re
from pathlib import Path
import shutil

# Backup directory
backup_dir = Path("backup_before_strand_fix")
backup_dir.mkdir(exist_ok=True)

# Directories to scan
root_dirs = ["src", "include"]

# Match e.g. receiveStrand_.dispatch( or sendStrand_.dispatch(
pattern = re.compile(r"(\w+Strand_)\.dispatch\s*\(")

for root in root_dirs:
    for path in Path(root).rglob("*.[ch]pp"):
        content = path.read_text()

        if pattern.search(content):
            # Backup original
            backup_path = backup_dir / path.name
            shutil.copy(path, backup_path)

            # Replace dispatch calls with modern syntax
            new_content = pattern.sub(
                r"boost::asio::dispatch(boost::asio::bind_executor(\1, ", content
            )

            # Fix the closing parentheses/semicolon
            new_content = re.sub(r"\}\s*\);", r"}));", new_content)

            # Write changes
            path.write_text(new_content)
            print(f"Updated: {path}")

print("✅ All *.cpp and *.hpp files updated. Backups in", backup_dir)
