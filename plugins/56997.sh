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
echo "Plugin: VMware ESX / ESXi Unsupported Version Detection (56997)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

# Run nmap version detection
NMAP_CMD="nmap -sVC -p $PORT $IP"

echo "Command:" >> "$OUTFILE"
echo "$NMAP_CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"

echo "Output:" >> "$OUTFILE"

NMAP_OUTPUT=$(timeout 60 $NMAP_CMD 2>&1)

echo "$NMAP_OUTPUT" >> "$OUTFILE"

# Check if VMware ESXi version detected
if echo "$NMAP_OUTPUT" | grep -qi "VMware"; then

    echo "" >> "$OUTFILE"
    echo "[+] VMware service detected through nmap." >> "$OUTFILE"

else

    echo "" >> "$OUTFILE"
    echo "[!] Version not detected via nmap. Taking screenshot with EyeWitness." >> "$OUTFILE"

    PROTO="https"

    # fallback http if https fails
    if ! curl -k -I https://$IP:$PORT --max-time 5 2>/dev/null | grep -q "HTTP"; then
        PROTO="http"
    fi

    URL="$PROTO://$IP:$PORT"

    EW_CMD="eyewitness --web -d $TARGET_DIR --single $URL --no-prompt"

    echo "" >> "$OUTFILE"
    echo "Command:" >> "$OUTFILE"
    echo "$EW_CMD" >> "$OUTFILE"
    echo "" >> "$OUTFILE"

    timeout 180 bash -c "$EW_CMD" >> "$OUTFILE" 2>&1

fi