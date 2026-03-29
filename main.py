import argparse
import os

from modes import poc, assets,dirb
from parser import parse_report
from utils.common import *
from modes import assets
from modes.storage import append_data, load_data
from modes import export_m1, export_m2, export_m3
# ---------------------------
# HELPERS
# ---------------------------

def get_reports(path):

    if os.path.isfile(path):
        return [path]

    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.endswith(".html")
    ]


def get_plugins():

    if not os.path.exists("plugins"):
        return []

    return [
        f.replace(".sh", "")
        for f in os.listdir("plugins")
        if f.endswith(".sh")
    ]


# ---------------------------
# MAIN
# ---------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("mode", choices=["poc", "assets","dirb"])

    parser.add_argument("-r", "--report", required=True)

    parser.add_argument("-p", "--plugin", nargs="+")
    parser.add_argument("-s", "--severity", nargs="+",
                        choices=["critical", "high", "medium", "low", "none"])

    parser.add_argument(
        "--resume",
        action="store_true",
    )
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=2,
        help="Number of threads"
    )
    parser.add_argument(
        "-m", "--mode_type",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="1=default, 2=VLAN-IP, 3=VLAN-IP+Port"
    )
    args = parser.parse_args()

    reports = get_reports(args.report)

    if not reports:
        print("[-] No reports found")
        return

    # ---------------------------
    # POC MODE
    # ---------------------------
    if args.mode == "poc":

        plugins = get_plugins()
        print("[+] Loaded plugins:", plugins)

        for report in reports:
            poc.process(report, plugins, args)

    # ---------------------------
    # ASSETS MODE
    # ---------------------------
    elif args.mode == "assets":

        all_new_data = []

        for report in reports:
            print(f"[+] Processing: {report}")
            data = assets.process(report, args)
            all_new_data.extend(data)

        # ---------------------------
        # 🔥 RESUME SUPPORT
        # ---------------------------
        if args.resume:
            print("[+] Resume mode: appending to JSON")
            final_data = append_data(all_new_data)
        else:
            print("[+] Fresh run: overwriting JSON")
            from modes.storage import save_data
            save_data(all_new_data)
            final_data = all_new_data

        # ---------------------------
        # EXPORT FROM JSON
        # ---------------------------
        if args.mode_type == 1:
            export_m1.export_to_excel(final_data)

        elif args.mode_type == 2:
            export_m2.export_to_excel(final_data)

        elif args.mode_type == 3:
            export_m3.export_to_excel(final_data)
    elif args.mode == "dirb":

        for report in reports:
            dirb.process(report, args)


if __name__ == "__main__":
    main()