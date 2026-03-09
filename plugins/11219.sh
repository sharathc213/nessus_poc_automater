#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

# run only for web services
if [ "$SERVICE" != "www" ]; then
    exit 0
fi

BASE_DIR="$OUTDIR/$NAME"
TARGET_DIR="$BASE_DIR/${IP}-${PORT}"

mkdir -p "$TARGET_DIR"

OUTFILE="$TARGET_DIR/${IP}-${PORT}.txt"

PROTO="http"

# Detect HTTPS
if echo | timeout 3 openssl s_client -connect $IP:$PORT 2>/dev/null | grep -q "BEGIN CERTIFICATE"; then
    PROTO="https"
fi

URL="$PROTO://$IP:$PORT"

CMD="eyewitness --web -d $TARGET_DIR --single $URL --no-prompt"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: Nessus SYN Scanner (11219)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 300 bash -c "$CMD" >> "$OUTFILE" 2>&1