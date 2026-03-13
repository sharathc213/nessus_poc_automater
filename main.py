import os
import argparse
import subprocess
from parser import parse_report
import re
import html
import hashlib

PLUGIN_DIR = "plugins"
OUTPUT_DIR = "output"
LOG_DIR = "logs"
ASSET_FILE = "assets.txt"


def get_plugins():
    plugins = []

    if not os.path.exists(PLUGIN_DIR):
        return plugins

    for f in os.listdir(PLUGIN_DIR):
        if f.endswith(".sh"):
            plugins.append(f.replace(".sh", ""))

    return plugins


def clean_name(name):
    name = html.unescape(name)
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.replace(" ", "_")
    return name


def get_resume_file(report):

    os.makedirs(LOG_DIR, exist_ok=True)

    report_hash = hashlib.md5(report.encode()).hexdigest()

    return os.path.join(LOG_DIR, f"resume_{report_hash}.log")


def load_completed(resume_file):

    completed = set()

    if os.path.exists(resume_file):
        with open(resume_file) as f:
            for line in f:
                completed.add(line.strip())

    return completed


def save_completed(resume_file, entry):

    with open(resume_file, "a") as f:
        f.write(entry + "\n")


def get_reports(path):

    if os.path.isfile(path):
        return [path]

    reports = []

    for f in os.listdir(path):
        if f.endswith(".html"):
            reports.append(os.path.join(path, f))

    return reports


# ---------------------------
# POC MODE
# ---------------------------

def process_report_poc(report, plugins, args):

    print(f"\n[+] Processing report: {report}")

    if args.plugin:
        vulns = parse_report(report, args.plugin)
    else:
        vulns = parse_report(report, plugins)

    resume_file = get_resume_file(report)

    completed = load_completed(resume_file) if args.resume else set()

    severity_filter = None
    if args.severity:
        severity_filter = [s.lower() for s in args.severity]

    for v in vulns:

        if args.plugin and v["plugin_id"] not in args.plugin:
            continue

        if severity_filter:
            if v.get("risk", "").lower() not in severity_filter:
                continue

        key = f"{v['plugin_id']}|{v['ip']}|{v['port']}"

        if key in completed:
            print(f"[SKIP] {key}")
            continue

        script = f"{PLUGIN_DIR}/{v['plugin_id']}.sh"

        if not os.path.exists(script):
            continue

        print(f"[+] {v['plugin_id']} -> {v['ip']}:{v['port']} ({v.get('service','')})")

        result = subprocess.run([
            "bash",
            script,
            v["ip"],
            v["port"],
            v.get("service", ""),
            clean_name(v["plugin_name"]),
            OUTPUT_DIR
        ])

        if result.returncode == 0:
            save_completed(resume_file, key)


# ---------------------------
# ASSETS MODE
# ---------------------------
def process_report_assets(report, args):

    print(f"[+] Processing report: {report}")

    vulns = parse_report(report, None)

    severity_filter = None
    if args.severity:
        severity_filter = [s.lower() for s in args.severity]

    plugin_group = {}
    ip_group = {}

    for v in vulns:

        if args.plugin and v["plugin_id"] not in args.plugin:
            continue

        if severity_filter:
            if v.get("risk", "").lower() not in severity_filter:
                continue
        else:
            if v.get("risk", "").lower() == "none":
                continue

        plugin_key = f"{v['plugin_id']} - {v['plugin_name']}"
        ip = v["ip"]

        if plugin_key not in plugin_group:
            plugin_group[plugin_key] = []

        entry = f"{ip} - {v.get('protocol','tcp')}/{v['port']}"

        if entry not in plugin_group[plugin_key]:
            plugin_group[plugin_key].append(entry)

        vuln_entry = f"{v['plugin_id']} - {v['plugin_name']}"

        if ip not in ip_group:
            ip_group[ip] = []

        if vuln_entry not in ip_group[ip]:
            ip_group[ip].append(vuln_entry)

    return ip_group if args.ip_wise else plugin_group
# MAIN
# ---------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "mode",
        choices=["poc", "assets"],
        help="Run mode: poc or assets"
    )

    parser.add_argument(
        "-r", "--report",
        required=True,
        help="Nessus report file or folder"
    )

    parser.add_argument(
        "-p", "--plugin",
        nargs="+",
        help="Run only specific plugin IDs (multiple allowed)"
    )
    parser.add_argument(
        "-s", "--severity",
        nargs="+",
        choices=["critical", "high", "medium", "low", "none"],
        help="Filter findings by severity"
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume previous run (poc mode only)"
    )
    parser.add_argument(
        "--ip-wise",
        action="store_true",
        help="Group assets by IP instead of vulnerability")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plugins = get_plugins()

    print("[+] Loaded plugins:", plugins)

    reports = get_reports(args.report)

    if not reports:
        print("[-] No HTML reports found")
        return

    # ---------------------------
    # POC MODE
    # ---------------------------

    if args.mode == "poc":

        for report in reports:
            process_report_poc(report, plugins, args)

    # ---------------------------
    # ASSETS MODE
    # ---------------------------

    if args.mode == "assets":

        with open(ASSET_FILE, "w") as outfile:

            for report in reports:

                grouped = process_report_assets(report, args)

                for key, values in grouped.items():

                    print(key)
                    outfile.write(key + "\n")

                    for v in values:
                                     # skip informational findings
                        
                        if isinstance(v, dict) and v.get("risk", "").lower() == "none":
                            print(v.get("risk"))
                            continue
                        print(v)
                        outfile.write(v + "\n")

                    print()
                    outfile.write("\n")

        print(f"\n[+] Asset list saved to {ASSET_FILE}")


if __name__ == "__main__":
    main()