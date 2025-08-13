#!/bin/bash
# Patch .dispatch() calls to .post() for Boost.Asio compatibility

TARGET="src/Messenger/MessageInStream.cpp"

if [ ! -f "$TARGET" ]; then
  echo "Error: $TARGET not found!"
  exit 1
fi

cp "$TARGET" "${TARGET}.bak"
echo "Backup created at ${TARGET}.bak"

sed -i 's/strand_\.dispatch(/strand_.post(/g' "$TARGET"

echo "Patched .dispatch() to .post() in $TARGET"
