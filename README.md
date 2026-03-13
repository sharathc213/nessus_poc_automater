# Nessus POC Automation Tool

This tool parses **Nessus HTML reports** and can:

-   Run **Proof-of-Concept (PoC) scripts** for vulnerabilities
-   Extract **asset lists from reports**
-   Filter by **plugin ID**
-   Filter by **severity**
-   Process **multiple reports**
-   Resume interrupted PoC runs
-   Group assets **by vulnerability or IP**

------------------------------------------------------------------------

# Usage

The tool supports two modes:

poc\
assets

### Basic Syntax

python main.py `<mode>`{=html} -r `<report>`{=html}

Examples:

python main.py poc -r report.html\
python main.py assets -r report.html

------------------------------------------------------------------------

# Options

### -r , --report

Specify the Nessus report file or a directory containing reports.

Example:

python main.py poc -r report.html

or

python main.py poc -r reports/

------------------------------------------------------------------------

### -p , --plugin

Run only specific plugin IDs.

Supports **multiple plugins**.

python main.py poc -r report.html -p 57582

Multiple plugins:

python main.py poc -r report.html -p 57582 42873 78479

Works in both **poc** and **assets** mode.

------------------------------------------------------------------------

### -s , --severity

Filter findings by severity.

Available values:

critical\
high\
medium\
low\
none

Example:

python main.py assets -r report.html -s critical

Multiple severities:

python main.py assets -r report.html -s critical high

Example in PoC mode:

python main.py poc -r report.html -s high medium

------------------------------------------------------------------------

### --resume

Resume interrupted PoC execution.

python main.py poc -r report.html --resume

------------------------------------------------------------------------

### --ip-wise

Group assets by IP instead of vulnerability.

python main.py assets -r report.html --ip-wise

Example output:

10.1.1.122 57582 - SSL Self-Signed Certificate 42873 - SWEET32 Cipher

10.1.1.130 57582 - SSL Self-Signed Certificate

------------------------------------------------------------------------

# Examples

Run PoC for all vulnerabilities:

python main.py poc -r report.html

Extract assets from a report:

python main.py assets -r report.html

Run PoC for specific plugins:

python main.py poc -r report.html -p 57582 42873

Extract only critical findings:

python main.py assets -r report.html -s critical

Run PoC only for high severity vulnerabilities:

python main.py poc -r report.html -s high

Process multiple reports:

python main.py assets -r reports/

------------------------------------------------------------------------

# Output

PoC results are saved in:

output/

Asset list is saved in:

assets.txt

Resume logs are stored in:

logs/
