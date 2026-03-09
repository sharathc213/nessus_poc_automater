#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

DIR="$OUTDIR/$NAME"
TARGET_DIR="$DIR/${IP}-${PORT}"

mkdir -p "$TARGET_DIR"

OUTFILE="$TARGET_DIR/${IP}-${PORT}.txt"

echo "Target: $IP:$PORT" > "$OUTFILE"
echo "Plugin: Unsupported Windows OS (108797)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

# First try SMB OS discovery
CMD="nmap -p445 -Pn --script smb-os-discovery $IP"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

timeout 120 bash -c "$CMD" >> "$OUTFILE" 2>&1


# If SMB didn't return OS, try RDP
if ! grep -qi "Windows" "$OUTFILE"; then

    echo "" >> "$OUTFILE"
    echo "[!] SMB OS detection failed. Trying RDP detection." >> "$OUTFILE"
    echo "" >> "$OUTFILE"

    CMD="nmap -p3389 -Pn --script rdp-ntlm-info $IP"

    echo "Command:" >> "$OUTFILE"
    echo "$CMD" >> "$OUTFILE"
    echo "" >> "$OUTFILE"

    timeout 120 bash -c "$CMD" >> "$OUTFILE" 2>&1

fi