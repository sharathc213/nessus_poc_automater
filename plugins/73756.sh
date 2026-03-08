#!/bin/bash

IP=$1
PORT=$2
SERVICE=$3
NAME=$4
OUTDIR=$5

DIR="$OUTDIR/$NAME"
mkdir -p "$DIR"

OUTFILE="$DIR/${IP}-${PORT}.txt"

echo "[+] Checking MSSQL Version on $IP:$PORT" > "$OUTFILE"

timeout 60 nmap -Pn -p $PORT -sV \
--script ms-sql-info \
$IP >> "$OUTFILE" 2>&1