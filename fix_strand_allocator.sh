#!/bin/bash
# fix_strand_allocator.sh - Fixes Boost strand post() calls in IOContextWrapper.hpp for Boost 1.74+

FILE="include/f1x/aasdk/IO/IOContextWrapper.hpp"

if [ ! -f "$FILE" ]; then
  echo "Error: $FILE not found!"
  exit 1
fi

echo "Patching $FILE to fix Boost strand post() calls..."

# Use sed to find lines with 'strand_->post(' and add allocator argument if missing
# This assumes the call is on one line and looks like strand_->post(std::move(handler));
# It will add ", boost::asio::allocator<void>()" inside the parentheses.

sed -i -E '
  s/(strand_->post\(\s*std::move\(handler\)\s*\);)/strand_->post(std::move(handler), boost::asio::allocator<void>());/
' "$FILE"

echo "Patch applied. Please run cmake and make again from the build directory."
