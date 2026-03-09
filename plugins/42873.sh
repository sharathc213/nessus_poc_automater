#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTSSL="$SCRIPT_DIR/../tools/testssl.sh/testssl.sh"

# Ensure testssl is executable
if [ ! -x "$TESTSSL" ]; then
    chmod +x "$TESTSSL"
fi

CMD="$TESTSSL --sweet32 $IP:$PORT"

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}-${PORT}.txt"

CMD="$TESTSSL --sweet32 $IP:$PORT"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: SSL Medium Strength Cipher Suites Supported (SWEET32) (42873)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 180 bash -c "$CMD" >> "$OUTFILE" 2>&1