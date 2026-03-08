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

CMD="$TESTSSL --poodle $IP:$PORT"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: SSLv3 Padding Oracle (POODLE) (78479)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 180 bash -c "$CMD" >> "$OUTFILE" 2>&1