#!/bin/bash

# Folders to search
folders=(
    "./src/Channel/AV"
    "./src/Channel/Input"
    "./src/Channel/Sensor"
    "./src/Channel/Bluetooth"
    "./src/Channel/Control"
    "./src/Messenger"
    "./src/Transport"
    "./src/USB"
    "./src/TCP"
)

# Loop through folders
for dir in "${folders[@]}"; do
    find "$dir" -type f -name "*.cpp" | while read -r file; do
        modified=false

        # Replace strand_.get_executor().context() with strand_
        if grep -q "strand_.*get_executor().context()" "$file"; then
            cp "$file" "$file.bak"
            sed -i 's/strand_.*get_executor().context()/strand_/' "$file"
            modified=true
        fi

        # Replace ioService_ with strand_ in ReceivePromise::defer()
        if grep -q "ReceivePromise::defer(ioService_)" "$file"; then
            [ "$modified" = false ] && cp "$file" "$file.bak"
            sed -i 's/ReceivePromise::defer(ioService_)/ReceivePromise::defer(strand_)/' "$file"
            modified=true
        fi

        [ "$modified" = true ] && echo "Updated: $file (backup: $file.bak)"
    done
done

echo "All done. Originals backed up with .bak extension."

