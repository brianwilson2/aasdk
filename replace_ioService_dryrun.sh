#!/bin/bash

# Find all relevant cpp files
FILES=$(grep -rlE 'ReceivePromise::defer\((ioService_|strand_)\)' ./src)

for FILE in $FILES; do
    # Backup the file first
    cp "$FILE" "${FILE}.bak"

    # Replace ioService_ or strand_ with strand_.get_executor().context()
    sed -i -E 's/ReceivePromise::defer\((ioService_|strand_)\)/ReceivePromise::defer(strand_.get_executor().context())/g' "$FILE"

    echo "Updated: $FILE"
done

echo "All done. Originals backed up with .bak extension."
