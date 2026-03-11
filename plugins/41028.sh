#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

# Only run for SNMP
if [ "$SERVICE" != "snmp" ]; then
    exit 0
fi

DIR="$OUTDIR/$NAME"
TARGET_DIR="$DIR/${IP}-${PORT}"

mkdir -p "$TARGET_DIR"

OUTFILE="$TARGET_DIR/${IP}-${PORT}.txt"

CMD="nmap -sU -p $PORT --script snmp-info,snmp-sysdescr -oN - $IP"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: SNMP Agent Default Community Name (public) (41028)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 120 bash -c "$CMD" >> "$OUTFILE" 2>&1