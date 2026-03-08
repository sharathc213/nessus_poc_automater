#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

TESTSSL="tools/testssl.sh/testssl.sh"

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}-${PORT}.txt"

CMD="$TESTSSL --headers $IP:$PORT"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: HSTS Missing From HTTPS Server (142960)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 120 bash -c "$CMD" >> "$OUTFILE" 2>&1