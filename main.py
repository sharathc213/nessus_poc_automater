import os
import argparse
import subprocess
from parser import parse_report
import re
import html

PLUGIN_DIR = "plugins"
OUTPUT_DIR = "output"


def get_plugins():
    plugins = []

    for f in os.listdir(PLUGIN_DIR):
        if f.endswith(".sh"):
            plugins.append(f.replace(".sh", ""))

    return plugins


def clean_name(name):
    name = html.unescape(name)              # convert &lt; -> <
    name = re.sub(r'[<>:"/\\|?*]', '', name) # remove unsafe characters
    name = name.replace(" ", "_")
    return name


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--report", required=True)
    parser.add_argument("-p", "--plugin", help="Run only a specific plugin ID")

    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plugins = get_plugins()

    print("[+] Loaded plugins:", plugins)

    vulns = parse_report(args.report, plugins)

    for v in vulns:

        # filter plugin if user specified one
        if args.plugin and v["plugin_id"] != args.plugin:
            continue

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
            clean_name(v["plugin_name"]),
            OUTPUT_DIR
        ])


if __name__ == "__main__":
    main()