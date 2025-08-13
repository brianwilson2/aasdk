import os
import shutil
import re

DRY_RUN = False
ROOT_DIR = "./src/USB"

REPLACEMENTS = [
    # USBEndpoint fixes (add user_data + timeout)
    ("bulkTransfer fillBulkTransfer",
     re.compile(r"fillBulkTransfer\([\s\S]+?transferHandler\)\);", re.MULTILINE),
     "fillBulkTransfer(\n                transfer,\n                handle_,\n                endpointAddress_,\n                buffer.data,\n                buffer.size,\n                reinterpret_cast<libusb_transfer_cb_fn>(&USBEndpoint::transferHandler),\n                this,\n                0);"),
    ("interruptTransfer fillInterruptTransfer",
     re.compile(r"fillInterruptTransfer\([\s\S]+?transferHandler\)\);", re.MULTILINE),
     "fillInterruptTransfer(\n                transfer,\n                handle_,\n                endpointAddress_,\n                buffer.data,\n                buffer.size,\n                reinterpret_cast<libusb_transfer_cb_fn>(&USBEndpoint::transferHandler),\n                this,\n                0);"),
    ("controlTransfer fillControlTransfer",
     re.compile(r"fillBulkTransfer\([\s\S]+?this,\n\s*0\);", re.MULTILINE),
     "fillControlTransfer(\n                transfer,\n                handle_,\n                buffer.data,\n                reinterpret_cast<libusb_transfer_cb_fn>(&USBEndpoint::transferHandler),\n                this,\n                0);"),

    # USBHub hotplug callback fix (cast flag)
    ("USBHub hotplugRegisterCallback",
     re.compile(r"LIBUSB_HOTPLUG_NO_FLAGS,"),
     "static_cast<libusb_hotplug_flag>(LIBUSB_HOTPLUG_NO_FLAGS),"),
]

modified_files = []

# Lambda Promise fix patterns
LAMBDA_PROMISE_PATTERN = re.compile(
    r"(\[\s*this[^\]]*\]\([^\)]*\)\s*mutable\s*\{)([\s\S]*?)(promise_->resolve\([^\)]*\);)([\s\S]*?)\}",
    re.MULTILINE
)

for dirpath, _, filenames in os.walk(ROOT_DIR):
    for fname in filenames:
        if not fname.endswith(".cpp") and not fname.endswith(".hpp"):
            continue
        full_path = os.path.join(dirpath, fname)
        with open(full_path, "r") as f:
            content = f.read()

        new_content = content
        changes_made = False

        # First handle static replacements
        for desc, pattern, new in REPLACEMENTS:
            if isinstance(pattern, str):
                if pattern in new_content:
                    new_content = new_content.replace(pattern, new)
                    changes_made = True
                    print(f"[DRY_RUN] Would update {fname}: {desc}" if DRY_RUN else f"Updating {fname}: {desc}")
            else:
                if pattern.search(new_content):
                    new_content = pattern.sub(new, new_content)
                    changes_made = True
                    print(f"[DRY_RUN] Would update {fname}: {desc}" if DRY_RUN else f"Updating {fname}: {desc}")

        # Auto-fix Promise lambda types
        def fix_lambda(match):
            start, body, resolve_call, rest = match.groups()
            if "endpoint" in resolve_call and "unsigned int" in content:
                new_resolve = "promise_->resolve(endpoint->getHandle() ? 1 : 0);"
            elif "bytesTransferred" in resolve_call and "IUSBEndpoint::Pointer" in content:
                new_resolve = "promise_->resolve(usbEndpoint);"
            else:
                return match.group(0)  # leave unchanged
            return f"{start}\n{body}{new_resolve}{rest}}}"

        new_content, num_subs = LAMBDA_PROMISE_PATTERN.subn(fix_lambda, new_content)
        if num_subs > 0:
            changes_made = True
            print(f"[DRY_RUN] Would fix {num_subs} lambda Promise(s) in {fname}" if DRY_RUN else f"Fixed {num_subs} lambda Promise(s) in {fname}")

        if changes_made and not DRY_RUN:
            # Backup first
            shutil.copy2(full_path, full_path + ".bak")
            with open(full_path, "w") as f:
                f.write(new_content)
            modified_files.append(full_path)

if DRY_RUN:
    print("\nDRY RUN complete. No files were modified.")
else:
    print("\nModified files:")
    for f in modified_files:
        print(f" - {f}")
