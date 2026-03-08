#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}-${PORT}.txt"

CMD="nmap -sV -Pn --script ssl-enum-ciphers -p $PORT $IP"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: $NAME" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 120 $CMD >> "$OUTFILE" 2>&1