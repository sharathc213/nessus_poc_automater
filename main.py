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


def get_plugins():
    plugins = []

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
    """
    Return list of report files.
    Accepts single file or directory
    """

    if os.path.isfile(path):
        return [path]

    reports = []

    for f in os.listdir(path):
        if f.endswith(".html"):
            reports.append(os.path.join(path, f))

    return reports


def process_report(report, plugins, args):

    print(f"\n[+] Processing report: {report}")

    vulns = parse_report(report, plugins)

    resume_file = get_resume_file(report)

    completed = load_completed(resume_file) if args.resume else set()

    for v in vulns:

        if args.plugin and v["plugin_id"] != args.plugin:
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
            v["service"],
            clean_name(v["plugin_name"]),
            OUTPUT_DIR
        ])

        if result.returncode == 0:
            save_completed(resume_file, key)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--report", required=True,
                        help="Nessus report file or folder")

    parser.add_argument("-p", "--plugin",
                        help="Run only a specific plugin ID")

    parser.add_argument("--resume", action="store_true",
                        help="Resume previous run")

    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plugins = get_plugins()

    print("[+] Loaded plugins:", plugins)

    reports = get_reports(args.report)

    if not reports:
        print("[-] No HTML reports found")
        return

    for report in reports:
        process_report(report, plugins, args)


if __name__ == "__main__":
    main()