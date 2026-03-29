import subprocess
import os
from parser import parse_report
from concurrent.futures import ThreadPoolExecutor

OUTPUT_DIR = "output/dirb"
LOG_FILE = "logs/dirb_completed.txt"
# 🔥 Defind your wordlist here (Change this to your preferred path)
WORDLIST = "/usr/share/wordlists/dirb/common.txt" 


# ---------------------------
# HTTPS Detection
# ---------------------------
def is_https(ip, port):
    try:
        # Quick check for SSL/TLS
        cmd = f'echo | timeout 2 openssl s_client -connect {ip}:{port} 2>/dev/null'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return "BEGIN CERTIFICATE" in result.stdout
    except:
        return False


# ---------------------------
# Resume Handling
# ---------------------------
def load_completed():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE) as f:
        return set(line.strip() for line in f)


def save_completed(entry):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")


# ---------------------------
# THREAD WORKER
# ---------------------------
def scan_target(ip, port, completed):

    key = f"{ip}:{port}"

    # Check completed status first! Don't waste time on openssl checks.
    if key in completed:
        print(f"[SKIP] {key}")
        return

    https = is_https(ip, port)
    protocol = "https" if https else "http"

    url = f"{protocol}://{ip}:{port}/FUZZ"
    output_file = os.path.join(OUTPUT_DIR, f"{ip}-{port}.txt")

    print(f"[FFUF] Fuzzing {protocol}://{ip}:{port}")

    # 🔥 FFUF Command
    # -w: wordlist, -u: URL (with FUZZ keyword), -o: output file, -of: output format (md/csv/json)
    # Added -t 40 inside ffuf so each target fuzzes super fast.
    cmd = [
        "ffuf", 
        "-w", WORDLIST, 
        "-u", url, 
        "-o", output_file, 
        "-of", "md", 
        "-t", "40", 
        "-noninteractive"
    ]

    try:
        # We run it and wait for completion
        result = subprocess.run(cmd, check=True) 
        save_completed(key)

    except subprocess.CalledProcessError as e:
        # FFUF might exit with non-zero if no directories are found or network drops.
        # We still mark it complete to avoid endless rescanning loops on bad hosts.
        save_completed(key)
        print(f"[FFUF WARNING] {ip}:{port} finished with an error code but marked complete.")
    except Exception as e:
        print(f"[ERROR] {ip}:{port} -> {e}")


# ---------------------------
# MAIN PROCESS
# ---------------------------
def process(report, args):

    print(f"[+] Processing report: {report}")

    if args.plugin:
        plugin_ids = args.plugin
    else:
        plugin_ids = ["11219"]  # default HTTP plugin

    vulns = parse_report(report, plugin_ids)
    completed = load_completed() if args.resume else set()
    targets = set()

    for v in vulns:
        ip = v["ip"]
        port = str(v["port"])
        targets.add((ip, port))

    if not targets:
        print("[-] No web targets found")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ⚠️ Keep this thread pool low (around 2 or 3) because ffuf spins up 40 threads per host.
    max_threads = args.threads if hasattr(args, "threads") else 2
    print(f"[+] Running with {max_threads} parallel target scans")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for ip, port in targets:
            executor.submit(scan_target, ip, port, completed)