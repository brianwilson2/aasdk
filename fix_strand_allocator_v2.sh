#!/bin/bash
# fix_strand_allocator_v2.sh - Correct allocator argument for Boost 1.74

FILE="include/f1x/aasdk/IO/IOContextWrapper.hpp"

if [ ! -f "$FILE" ]; then
  echo "Error: $FILE not found!"
  exit 1
fi

echo "Patching $FILE to fix Boost strand post() allocator argument for Boost 1.74..."

sed -i -E '
  s/strand_executor::allocator<void>/allocator<void>/g
' "$FILE"

echo "Patch applied. Now run cmake and make again from the build directory."

