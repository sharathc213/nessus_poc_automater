import re

plugin_regex = re.compile(r'(\d+)\s+\(\d+\)\s+-\s+([^<]+)')
ip_regex = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+\(tcp/(\d+)/(.*?)\)')

def parse_report(report, valid_plugins):

    results = []

    current_plugin = None
    plugin_name = None

    with open(report, "r", encoding="utf-8", errors="ignore") as f:

        for line in f:

            # detect plugin
            p = plugin_regex.search(line)
            if p:
                pid = p.group(1)

                if pid in valid_plugins:
                    current_plugin = pid
                    plugin_name = p.group(2).split("<")[0].strip()
                else:
                    current_plugin = None

                continue

            # detect ip:port/service
            if current_plugin:
                m = ip_regex.search(line)

                if m:
                    ip = m.group(1)
                    port = m.group(2)
                    service = m.group(3)

                    results.append({
                        "plugin_id": current_plugin,
                        "plugin_name": plugin_name,
                        "ip": ip,
                        "port": port,
                        "service": service
                    })

    return results