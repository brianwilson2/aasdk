#!/bin/bash

# Directory to scan
DIR="./src"

# Fix extra closing parens on lambdas
find "$DIR" -type f \( -name "*.cpp" -o -name "*.hpp" \) -exec sed -i 's/})) ;);/});/g' {} +

# Fix strand get_io_context to get_executor context
find "$DIR" -type f \( -name "*.cpp" -o -name "*.hpp" \) -exec sed -i 's/strand_\.get_io_context()/strand_.get_executor().context()/g' {} +

echo "Fixes applied. You might want to do a manual grep for '})) ;);' or 'get_io_context' just in case."
