#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}-${PORT}.txt"

CMD="nmap -sV -Pn -p $PORT --script oracle-tns-version,oracle-sid-brute $IP"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: Oracle Database Unsupported Version Detection" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 180 bash -c "$CMD" >> "$OUTFILE" 2>&1