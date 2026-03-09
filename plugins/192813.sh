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
echo "Plugin: Microsoft Windows Server 2012 SEoL (192813)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

# Try SMB OS detection first
CMD="nmap -p445 --script smb-os-discovery $IP"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"
echo "Output:" >> "$OUTFILE"

timeout 120 bash -c "$CMD" >> "$OUTFILE" 2>&1


# If Windows version not detected try RDP
if ! grep -qi "Windows Server 2012" "$OUTFILE"; then

    echo "" >> "$OUTFILE"
    echo "[!] SMB detection did not confirm Server 2012. Trying RDP detection." >> "$OUTFILE"
    echo "" >> "$OUTFILE"

    CMD="nmap -p3389 --script rdp-ntlm-info $IP"

    echo "Command:" >> "$OUTFILE"
    echo "$CMD" >> "$OUTFILE"
    echo "" >> "$OUTFILE"

    timeout 120 bash -c "$CMD" >> "$OUTFILE" 2>&1

fi