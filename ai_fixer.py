import re
import os

def apply_rules_to_file(filepath, rules):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # Skip binary or non-utf8 files
        return

    original_content = content
    for rule in rules:
        if "file_pattern" in rule and not re.match(rule["file_pattern"], filepath):
            continue
        if "search" in rule and "replace" in rule:
            new_content, count = re.subn(rule["search"], rule["replace"], content)
            if count > 0:
                print(f"Replaced {count} occurrence(s) in {filepath} using rule: {rule.get('description', '')}")
                content = new_content
        elif "condition_missing" in rule and "insert_after" in rule and "insert_text" in rule:
            # Check if all condition_missing headers are missing
            if all(header not in content for header in rule["condition_missing"]):
                # Insert after the insert_after line
                pattern = re.escape(rule["insert_after"])
                new_content, count = re.subn(f"({pattern})", r"\1\n" + rule["insert_text"], content)
                if count > 0:
                    print(f"Inserted text in {filepath} after {rule['insert_after']}")
                    content = new_content

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

def main():
    import json
    with open("my_rules.json") as f:
        rules = json.load(f)

    for root, dirs, files in os.walk("."):
        for file in files:
            filepath = os.path.join(root, file)
            apply_rules_to_file(filepath, rules)

if __name__ == "__main__":
    main()
