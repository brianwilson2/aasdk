#!/bin/bash
# fix_strand_executor.sh
# Replace strand_.get_executor() with strand_.executor() for Boost compatibility

FILE="src/Channel/ServiceChannel.cpp"
SEARCH="strand_.get_executor()"
REPLACE="strand_.executor()"

if grep -q "$SEARCH" "$FILE"; then
    echo "Patching $FILE: replacing '$SEARCH' with '$REPLACE'"
    sed -i "s/$SEARCH/$REPLACE/g" "$FILE"
    echo "Patch applied."
else
    echo "No occurrences of '$SEARCH' found in $FILE. Nothing to do."
fi
