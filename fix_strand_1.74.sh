#!/bin/bash
# fix_strand_1.74.sh - Patch Messenger.cpp for Boost 1.74 strand constructor

FILE="src/Messenger/Messenger.cpp"

if [ ! -f "$FILE" ]; then
  echo "Error: $FILE not found. Run this from the aasdk root folder."
  exit 1
fi

echo "Patching $FILE for Boost 1.74 strand constructor..."

# Backup first
cp "$FILE" "${FILE}.bak"

# Replace strand_ constructor args with make_strand(ioService)
sed -i -E 's/(receiveStrand_|sendStrand_)\(ioService\)/\1(boost::asio::make_strand(ioService))/' "$FILE"

echo "Patch applied. Backup saved as ${FILE}.bak"
