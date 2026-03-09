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
echo "Plugin: VMware vCenter Server Out-of-bounds Write (183957)" >> "$OUTFILE"
echo "" >> "$OUTFILE"

# Try nmap detection
CMD="nmap -sVC -p $PORT --script http-title,ssl-cert $IP"

echo "Command:" >> "$OUTFILE"
echo "$CMD" >> "$OUTFILE"
echo "" >> "$OUTFILE"
echo "Output:" >> "$OUTFILE"

NMAP_OUTPUT=$(timeout 120 bash -c "$CMD" 2>&1)

echo "$NMAP_OUTPUT" >> "$OUTFILE"


# If VMware detected stop
if echo "$NMAP_OUTPUT" | grep -qi "vmware"; then
    echo "" >> "$OUTFILE"
    echo "[+] VMware service detected via Nmap." >> "$OUTFILE"

else

    echo "" >> "$OUTFILE"
    echo "[!] VMware version not detected via Nmap. Trying curl." >> "$OUTFILE"

    PROTO="https"

    if ! curl -k -I https://$IP:$PORT --max-time 5 2>/dev/null | grep -q "HTTP"; then
        PROTO="http"
    fi

    URL="$PROTO://$IP:$PORT"

    CMD="curl -k $URL"

    echo "" >> "$OUTFILE"
    echo "Command:" >> "$OUTFILE"
    echo "$CMD" >> "$OUTFILE"
    echo "" >> "$OUTFILE"

    timeout 30 bash -c "$CMD" >> "$OUTFILE" 2>&1


    # If still nothing useful take screenshot
    if ! grep -qi "vmware" "$OUTFILE"; then

        echo "" >> "$OUTFILE"
        echo "[!] Version still not detected. Taking screenshot." >> "$OUTFILE"

        EW_CMD="eyewitness --web -d $TARGET_DIR --single $URL --no-prompt"

        echo "" >> "$OUTFILE"
        echo "Command:" >> "$OUTFILE"
        echo "$EW_CMD" >> "$OUTFILE"
        echo "" >> "$OUTFILE"

        timeout 180 bash -c "$EW_CMD" >> "$OUTFILE" 2>&1

    fi

fi