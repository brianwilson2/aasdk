#!/bin/bash

FILE="include/f1x/aasdk/IO/IOContextWrapper.hpp"

if [ ! -f "$FILE" ]; then
  echo "File not found: $FILE"
  exit 1
fi

# Backup the original file just in case
cp "$FILE" "${FILE}.bak"

# Use sed to replace the single-argument post call with the two-argument one including allocator
sed -i 's/strand_->post(std::move(handler));/strand_->post(std::move(handler), boost::asio::strand_executor::allocator<void>());/' "$FILE"

echo "Patch applied to $FILE (backup at ${FILE}.bak)"
