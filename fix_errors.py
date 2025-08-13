#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

# === ADD YOUR FIX RULES HERE ===
rules = [
    ("#include <f1x/aasdk/Channel/AV/IChannel.hpp>", '#include "IChannel.hpp"  // Fixed include path'),
    ("boost::asio::strand<boost::asio::io_context::executor_type>&", "boost::asio::io_service::strand&"),
    (".get_executor()", ".get_io_context()")]
# ==============================

BACKUP_DIR = "AIscriptbackups"

def backup_file(filepath):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"{timestamp}__{os.path.basename(filepath)}")
    shutil.copy2(filepath, backup_path)
    print(f"[BACKUP] {filepath} -> {backup_path}")

def process_file(filepath):
    if not os.path.isfile(filepath):
        print(f"[SKIP] File not found: {filepath}")
        return
    backup_file(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False
    for search, replace in rules:
        if search in content:
            content = content.replace(search, replace)
            print(f"[FIX] Replaced '{search}' with '{replace}' in {filepath}")
            changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(f"[NO CHANGE] {filepath}")

def fix_files(start_dir="."):
    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.endswith((".cpp", ".hpp", ".h")):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    fix_files()
