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
CURL_OPTS="-I"

# Detect HTTPS
if echo | timeout 3 openssl s_client -connect $IP:$PORT 2>/dev/null | grep -q "BEGIN CERTIFICATE"; then
    PROTO="https"
    CURL_OPTS="-k -I"
fi

CMD="curl $CURL_OPTS $PROTO://$IP:$PORT"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: Apache Tomcat Unsupported Version (299410)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 15 bash -c "$CMD" >> "$OUTFILE" 2>&1

echo "" >> "$OUTFILE"
echo "Possible Tomcat Indicators:" >> "$OUTFILE"

grep -Ei "tomcat|coyote" "$OUTFILE" >> "$OUTFILE"