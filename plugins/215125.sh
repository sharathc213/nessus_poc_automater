#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}.txt"

CMD="snmpwalk -v2c -c public $IP | grep -i version"

echo "Target: $IP" > "$OUTFILE"
echo "Plugin: 215125 Cisco IOS XE Software SNMP DoS" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

timeout 60 bash -c "$CMD" >> "$OUTFILE" 2>&1