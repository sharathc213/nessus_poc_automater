import re

plugin_regex = re.compile(r'(\d+)\s+\(\d+\)\s+-\s+([^<]+)')
host_regex = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+\((tcp|udp)/(\d+)(?:/([^)]+))?\)')
risk_regex = re.compile(
    r'Risk Factor.*?</div>\s*<div[^>]*>\s*(None|Low|Medium|High|Critical)',
    re.IGNORECASE | re.DOTALL
)

def parse_report(report, valid_plugins=None):

    results = []

    with open(report, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()

    plugins = list(plugin_regex.finditer(data))

    for i, p in enumerate(plugins):

        pid = p.group(1)
        pname = p.group(2).strip()

        if valid_plugins is not None and pid not in valid_plugins:
            continue

        start = p.end()

        if i + 1 < len(plugins):
            end = plugins[i+1].start()
        else:
            end = len(data)

        section = data[start:end]

        hosts = host_regex.findall(section)
        risk_match = risk_regex.search(section)

        risk = "Unknown"
        if risk_match:
            risk = risk_match.group(1).strip()

        for ip, proto, port, service in hosts:
            results.append({
            "plugin_id": pid,
            "plugin_name": pname,
            "ip": ip,
            "port": port,
            "protocol": proto,
            "service": service,
            "risk": risk
        })
    return results