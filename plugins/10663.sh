#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}.txt"

CMD="nmap -sU -Pn -p 67 --script dhcp-discover $IP"

echo "Target: $IP" > "$OUTFILE"
echo "Plugin: DHCP Server Detection (10663)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 60 $CMD >> "$OUTFILE" 2>&1