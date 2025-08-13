#!/bin/bash
# fix_servicechannel_executor.sh
# Replace strand_.get_executor() with strand_ (passing strand_ itself)

FILE="src/Channel/ServiceChannel.cpp"
SEARCH="strand_.get_executor()"
REPLACE="strand_"

if grep -q "$SEARCH" "$FILE"; then
    echo "Patching $FILE: replacing '$SEARCH' with '$REPLACE'"
    sed -i "s/$SEARCH/$REPLACE/g" "$FILE"
    echo "Patch applied."
else
    echo "No occurrences of '$SEARCH' found in $FILE. Trying alternative patch..."

    # Try replacing strand_.executor() too
    SEARCH2="strand_.executor()"
    if grep -q "$SEARCH2" "$FILE"; then
        echo "Replacing '$SEARCH2' with '$REPLACE'"
        sed -i "s/$SEARCH2/$REPLACE/g" "$FILE"
        echo "Alternative patch applied."
    else
        echo "No matching patterns found. Nothing changed."
    fi
fi
