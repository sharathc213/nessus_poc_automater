# import os
# import subprocess
# from parser import parse_report
# from utils.common import clean_name, get_resume_file, load_completed, save_completed


# def process(report, plugins, args):

#     print(f"\n[+] Processing report: {report}")

#     vulns = parse_report(report, plugins if not args.plugin else args.plugin)

#     resume_file = get_resume_file(report)
#     completed = load_completed(resume_file) if args.resume else set()

#     severity_filter = [s.lower() for s in args.severity] if args.severity else None

#     for v in vulns:

#         if args.plugin and v["plugin_id"] not in args.plugin:
#             continue

#         if severity_filter and v.get("risk", "").lower() not in severity_filter:
#             continue

#         key = f"{v['plugin_id']}|{v['ip']}|{v['port']}"

#         if key in completed:
#             print(f"[SKIP] {key}")
#             continue

#         script = f"plugins/{v['plugin_id']}.sh"

#         if not os.path.exists(script):
#             continue

#         print(f"[+] {v['plugin_id']} -> {v['ip']}:{v['port']}")

#         result = subprocess.run([
#             "bash",
#             script,
#             v["ip"],
#             v["port"],
#             v.get("service", ""),
#             clean_name(v["plugin_name"]),
#             "output"
#         ])

#         if result.returncode == 0:
#             save_completed(resume_file, key)

import os
import subprocess
from parser import parse_report
from utils.common import clean_name, get_resume_file, load_completed, save_completed
from concurrent.futures import ThreadPoolExecutor
import threading

# 🔥 Lock for safe file writing
lock = threading.Lock()


# ---------------------------
# THREAD WORKER
# ---------------------------
def run_plugin(v, args, completed, resume_file):

    key = f"{v['plugin_id']}|{v['ip']}|{v['port']}"

    if key in completed:
        print(f"[SKIP] {key}")
        return

    script = f"plugins/{v['plugin_id']}.sh"

    if not os.path.exists(script):
        return

    print(f"[+] {v['plugin_id']} -> {v['ip']}:{v['port']}")

    try:
        result = subprocess.run([
            "bash",
            script,
            v["ip"],
            v["port"],
            v.get("service", ""),
            clean_name(v["plugin_name"]),
            "output"
        ])

        if result.returncode == 0:
            # 🔒 thread-safe write
            with lock:
                save_completed(resume_file, key)

    except Exception as e:
        print(f"[ERROR] {key} -> {e}")


# ---------------------------
# MAIN PROCESS
# ---------------------------
def process(report, plugins, args):

    print(f"\n[+] Processing report: {report}")

    vulns = parse_report(report, plugins if not args.plugin else args.plugin)

    resume_file = get_resume_file(report)
    completed = load_completed(resume_file) if args.resume else set()

    severity_filter = [s.lower() for s in args.severity] if args.severity else None

    # ---------------------------
    # FILTER VULNS FIRST
    # ---------------------------
    filtered = []

    for v in vulns:

        if args.plugin and v["plugin_id"] not in args.plugin:
            continue

        if severity_filter and v.get("risk", "").lower() not in severity_filter:
            continue

        filtered.append(v)

    if not filtered:
        print("[-] No matching vulnerabilities")
        return

    # ---------------------------
    # THREAD CONTROL
    # ---------------------------
    max_threads = args.threads if hasattr(args, "threads") else 5

    print(f"[+] Running with {max_threads} threads")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for v in filtered:
            executor.submit(run_plugin, v, args, completed, resume_file)