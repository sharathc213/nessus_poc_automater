#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}-${PORT}.txt"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: SSL Anonymous Cipher Suites Supported (31705)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

# Detect protocol
PROTO="https"

if ! echo | timeout 3 openssl s_client -connect $IP:$PORT 2>/dev/null | grep -q "BEGIN CERTIFICATE"; then
    PROTO="http"
fi

echo "Protocol detected: $PROTO" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "openssl s_client -connect $IP:$PORT -cipher aNULL" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 20 openssl s_client -connect $IP:$PORT -cipher aNULL \
    >> "$OUTFILE" 2>&1

echo "" >> "$OUTFILE"
echo "Analysis:" >> "$OUTFILE"

if grep -qi "Cipher is" "$OUTFILE"; then
    echo "Anonymous cipher supported (Potential vulnerability)" >> "$OUTFILE"
else
    echo "Anonymous cipher NOT supported" >> "$OUTFILE"
fi