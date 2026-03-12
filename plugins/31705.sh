#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}-${PORT}.txt"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: SSL Anonymous Cipher Suites Supported (31705)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

CMD="nmap -p $PORT --script ssl-enum-ciphers $IP"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"
echo "Output:" >> "$OUTFILE"

timeout 120 bash -c "$CMD" >> "$OUTFILE" 2>&1

echo "" >> "$OUTFILE"
echo "Anonymous Cipher Suites:" >> "$OUTFILE"
