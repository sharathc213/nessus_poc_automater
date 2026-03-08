import os
import argparse
import subprocess
from parser import parse_report

PLUGIN_DIR = "plugins"
OUTPUT_DIR = "output"


def get_plugins():
    plugins = []

    for f in os.listdir(PLUGIN_DIR):
        if f.endswith(".sh"):
            plugins.append(f.replace(".sh", ""))

    return plugins


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--report", required=True)

    args = parser.parse_args()

    # create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plugins = get_plugins()

    print("[+] Loaded plugins:", plugins)

    vulns = parse_report(args.report, plugins)

    for v in vulns:

        script = f"{PLUGIN_DIR}/{v['plugin_id']}.sh"

        if not os.path.exists(script):
            continue

        print(f"[+] {v['plugin_id']} -> {v['ip']}:{v['port']} ({v.get('service','')})")

        subprocess.run([
            "bash",
            script,
            v["ip"],
            v["port"],
            v["service"],
            v["plugin_name"].replace(" ", "_"),
            OUTPUT_DIR
        ])


if __name__ == "__main__":
    main()