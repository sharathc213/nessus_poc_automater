#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}-${PORT}.txt"

PROTO="http"

# detect HTTPS
if echo | timeout 3 openssl s_client -connect $IP:$PORT 2>/dev/null | grep -q "BEGIN CERTIFICATE"; then
    PROTO="https"
fi

URL="$PROTO://$IP:$PORT"

CMD="eyewitness --web -d $DIR --single $URL"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: Apache Tomcat Default Files (12085)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 300 $CMD >> "$OUTFILE" 2>&1