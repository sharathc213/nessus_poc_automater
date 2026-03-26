import json
import os

DATA_FILE = "assets_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def append_data(new_data):

    existing = load_data()

    structured = {}

    for d in existing + new_data:

        key = (d["vulnerability"], d["report"])

        if key not in structured:
            structured[key] = {
                "assets": set(),
                "severity": d.get("severity", "unknown")
            }

        structured[key]["assets"].add(d["asset"])

    final = []

    for (vuln, vlan), info in structured.items():
        for asset in info["assets"]:
            final.append({
                "report": vlan,
                "vulnerability": vuln,
                "asset": asset,
                "severity": info["severity"]
            })

    save_data(final)

    return final