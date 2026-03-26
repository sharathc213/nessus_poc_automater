import subprocess
import os
from parser import parse_report
from concurrent.futures import ThreadPoolExecutor

OUTPUT_DIR = "output/dirb"
LOG_FILE = "logs/dirb_completed.txt"


# ---------------------------
# HTTPS Detection
# ---------------------------
def is_https(ip, port):
    try:
        cmd = f'echo | timeout 3 openssl s_client -connect {ip}:{port} 2>/dev/null'
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

    if key in completed:
        print(f"[SKIP] {key}")
        return

    https = is_https(ip, port)
    protocol = "https" if https else "http"

    url = f"{protocol}://{ip}:{port}"
    output_file = os.path.join(OUTPUT_DIR, f"{ip}-{port}.txt")

    print(f"[DIRB] {url}")

    cmd = ["dirb", url, "-o", output_file]

    try:
        result = subprocess.run(cmd)

        if result.returncode == 0:
            save_completed(key)

    except Exception as e:
        print(f"[ERROR] {url} -> {e}")


# ---------------------------
# MAIN PROCESS
# ---------------------------
def process(report, args):

    print(f"[+] Processing report: {report}")

    # ---------------------------
    # Plugin Selection
    # ---------------------------
    if args.plugin:
        plugin_ids = args.plugin
    else:
        plugin_ids = ["11219"]  # 🔥 default HTTP plugin

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

    # ---------------------------
    # THREAD CONTROL
    # ---------------------------
    max_threads = args.threads if hasattr(args, "threads") else 5

    print(f"[+] Running with {max_threads} threads")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for ip, port in targets:
            executor.submit(scan_target, ip, port, completed)