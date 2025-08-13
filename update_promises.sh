#!/bin/bash
# Filename: update_promises.sh
# Usage: run from the root of the aasdk folder
# This script updates all Promise::defer calls to the new Boost.Asio style.

# Folders to scan
folders=("src/Channel" "src/Transport" "src/Messenger" "src/USB" "src/TCP")
# File types to scan
extensions=("cpp" "ut.cpp" "hpp" "h" "inl")

echo "Updating all Promise::defer calls to use strand_..."

# Scan main folders
for folder in "${folders[@]}"; do
    for ext in "${extensions[@]}"; do
        for file in "$folder"/*."$ext"; do
            [ -e "$file" ] || continue

            # Backup original
            cp "$file" "$file.bak"

            # Update ReceivePromise::defer(ioService_) and SendPromise::defer(ioService_)
            sed -i 's/::defer(ioService_)/::defer(strand_)/g' "$file"

            # Update ReceivePromise::defer(strand_.get_executor().context())
            sed -i 's/::defer(strand_\.get_executor()\.context())/::defer(strand_)/g' "$file"

            # Update SendPromise::defer(strand_.get_executor().context())
            sed -i 's/SendPromise::defer(strand_\.get_executor()\.context())/SendPromise::defer(strand_)/g' "$file"

            echo "Updated: $file (backup saved as $file.bak)"
        done
    done
done

# Specifically handle receiveStrand_ in src/Messenger
for file in src/Messenger/*.{cpp,ut.cpp,hpp}; do
    [ -e "$file" ] || continue

    cp "$file" "$file.bak"
    sed -i 's/ReceivePromise::defer(receiveStrand_\.get_executor()\.context())/ReceivePromise::defer(receiveStrand_)/g' "$file"
    echo "Updated receiveStrand_: $file (backup saved as $file.bak)"
done

echo "All done. Originals backed up with .bak extension."
