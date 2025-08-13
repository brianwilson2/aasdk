import os

# Search terms based on your working copy variable names
search_terms = [
    "boost::asio::io_context& ioService",
    "boost::asio::strand<boost::asio::io_context::executor_type>& strand"
]

# Use the current folder as base_dir
base_dir = os.getcwd()

# Path to the .txt file containing upstream changed file list
changed_files_txt = os.path.join(base_dir, "promise_usage.txt")  # make sure your .txt file is here

# Read the list of changed files from the text file
with open(changed_files_txt, "r") as f:
    changed_files = {line.strip() for line in f if line.strip()}

# Search working copy for matching terms
matching_files = set()

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith((".hpp", ".cpp")):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as src:
                    content = src.read()
                    if any(term in content for term in search_terms):
                        matching_files.add(os.path.relpath(file_path, base_dir))
            except Exception as e:
                print(f"Could not read {file_path}: {e}")

# Compare and output results
print("Files in BOTH working copy and upstream changes:")
for f in sorted(matching_files & changed_files):
    print(f)

print("\nFiles ONLY in working copy search results:")
for f in sorted(matching_files - changed_files):
    print(f)

print("\nFiles ONLY in upstream changed file list:")
for f in sorted(changed_files - matching_files):
    print(f)
