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

PROTO="http"
CURL_OPTS="-I"

# Detect HTTPS using openssl
if echo | timeout 3 openssl s_client -connect $IP:$PORT 2>/dev/null | grep -q "BEGIN CERTIFICATE"; then
    PROTO="https"
    CURL_OPTS="-k -I"
fi

CMD="curl $CURL_OPTS $PROTO://$IP:$PORT"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"
echo "Output:" >> "$OUTFILE"

timeout 15 bash -c "$CMD" >> "$OUTFILE" 2>&1

echo "" >> "$OUTFILE"
echo "Extracted Server Header:" >> "$OUTFILE"

SERVER_HEADER=$(grep -i "server:" "$OUTFILE")

echo "$SERVER_HEADER" >> "$OUTFILE"