#!/bin/bash
# update_strand_full.sh
# Updates ReceivePromise::defer calls from .get_executor().context() to just strand_ for all service & AV channels

FILES=$(grep -rl "ReceivePromise::defer(strand_\.get_executor().context()" ./src/Channel)

for f in $FILES; do
    echo "Updating $f"
    cp "$f" "$f.bak"
    sed -i 's/ReceivePromise::defer(strand_\.get_executor().context()/ReceivePromise::defer(strand_/g' "$f"
done

echo "All done. Backups saved with .bak extension."
