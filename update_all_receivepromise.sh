#!/bin/bash
# update_all_receivepromise.sh
# Updates ReceivePromise::defer calls from .get_executor().context() to just strand_ in all likely affected files

# Folders to check
FOLDERS="./src/Channel ./src/Messenger ./src/Transport"

for folder in $FOLDERS; do
    FILES=$(grep -rl "ReceivePromise::defer(strand_\.get_executor().context()" "$folder")
    for f in $FILES; do
        echo "Updating $f"
        cp "$f" "$f.bak"
        sed -i 's/ReceivePromise::defer(strand_\.get_executor().context()/ReceivePromise::defer(strand_/g' "$f"
    done
done

echo "All done. Backups saved with .bak extension."
