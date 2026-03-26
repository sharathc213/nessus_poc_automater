import os
import re
import html
import hashlib


def clean_name(name):
    name = html.unescape(name)
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name.replace(" ", "_")


def get_resume_file(report):
    os.makedirs("logs", exist_ok=True)
    report_hash = hashlib.md5(report.encode()).hexdigest()
    return os.path.join("logs", f"resume_{report_hash}.log")


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