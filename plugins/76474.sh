#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}.txt"

CMD="snmpbulkwalk -v2c -c public $IP 1.3.6.1.2.1.1"

echo "Target: $IP" > "$OUTFILE"
echo "Plugin: SNMP 'GETBULK' Reflection DDoS (76474)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 60 $CMD >> "$OUTFILE" 2>&1