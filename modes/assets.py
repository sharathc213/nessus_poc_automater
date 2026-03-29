import os
from parser import parse_report


def process(report, args):
    """
    Process a single Nessus HTML report and extract
    vulnerability → VLAN → asset mapping
    """

    vulns = parse_report(report, None)

    severity_filter = None
    if args.severity:
        severity_filter = [s.lower() for s in args.severity]

    report_name = os.path.basename(report).replace(".html", "")

    results = []

    for v in vulns:

        # ---------------------------
        # Severity Filtering
        # ---------------------------
        # If the user specified severities in the terminal, we filter by them.
        if severity_filter:
            if v.get("risk", "").lower() not in severity_filter:
                continue
        # 🔥 REMOVED THE HARDCODED SKIP FOR "NONE" HERE!
        # Now, if no severity is specified, it grabs everything, including "None".

        # ---------------------------
        # 🔥 Plugin Availability Check
        # ---------------------------
        plugin_id = v["plugin_id"]
        plugin_path = os.path.join("plugins", f"{plugin_id}.sh")

        status = "Plugin Available" if os.path.exists(plugin_path) else ""

        # ---------------------------
        # Build Structured Output
        # ---------------------------
        results.append({
            "report": report_name,  # VLAN
            "vulnerability": f"{plugin_id} - {v['plugin_name']}",
            "asset": f"{v['ip']} ({v.get('protocol','tcp')}/{v['port']})",
            "severity": v.get("risk", "unknown").lower(),
            "status": status,
            "plugin": plugin_id  # ✅ ADDED: This makes sure your export script can find the plugin ID!
        })

    return results