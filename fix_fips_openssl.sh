#!/bin/bash
# fix_fips_openssl.sh - Patch FIPS_mode_set call for OpenSSL 3.0+

FILE="src/Transport/SSLWrapper.cpp"
BACKUP="${FILE}.bak"

if [ ! -f "$FILE" ]; then
  echo "Error: $FILE not found! Run this from the aasdk root folder."
  exit 1
fi

cp "$FILE" "$BACKUP"
echo "Backup saved to $BACKUP"

sed -i '/FIPS_mode_set(0);/c\
#if OPENSSL_VERSION_NUMBER < 0x30000000L\n    FIPS_mode_set(0);\n#endif' "$FILE"

echo "Patched $FILE to fix FIPS_mode_set for OpenSSL 3.0+"
