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
echo "Plugin: Unsupported Web Server Detection (34460)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

# Try HTTPS first
CMD="curl -k -I https://$IP:$PORT"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"
echo "Output:" >> "$OUTFILE"

timeout 15 bash -c "$CMD" >> "$OUTFILE" 2>&1

# If HTTPS did not return server header, try HTTP
if ! grep -qi "server:" "$OUTFILE"; then

    CMD="curl -I http://$IP:$PORT"

    echo "" >> "$OUTFILE"
    echo "Command:" >> "$OUTFILE"
    echo "$CMD" >> "$OUTFILE"
    echo "" >> "$OUTFILE"
    echo "Output:" >> "$OUTFILE"

    timeout 15 bash -c "$CMD" >> "$OUTFILE" 2>&1
fi

echo "" >> "$OUTFILE"
echo "Extracted Server Header:" >> "$OUTFILE"

grep -i "server:" "$OUTFILE" >> "$OUTFILE"