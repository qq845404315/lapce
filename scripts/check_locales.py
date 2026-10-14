#!/usr/bin/env python3
"""Deduplicate locale TOML keys, keeping the last definition."""
from pathlib import Path

for name in ["en-US.toml", "zh-CN.toml"]:
    path = Path("lapce-app/locales") / name
    seen = {}
    order = []
    comments = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("["):
            comments.append(line)
            continue
        if "=" in stripped:
            key = stripped.split("=", 1)[0].strip().strip('"')
            seen[key] = line
            if key not in order:
                order.append(key)
        else:
            comments.append(line)
    # Keep a simple header
    out = ["# UI strings for Lapce. Keys are stable identifiers.", ""]
    for key in order:
        out.append(seen[key])
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(name, "->", len(order), "unique keys")

# Check used keys
import re

root = Path("lapce-app/src")
used = set()
for p in root.rglob("*.rs"):
    t = p.read_text(encoding="utf-8", errors="ignore")
    used.update(re.findall(r'i18n::t(?:_or)?\("([^"]+)"', t))
zh = set()
for line in Path("lapce-app/locales/zh-CN.toml").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.startswith("#"):
        zh.add(line.split("=", 1)[0].strip().strip('"'))
missing = sorted(used - zh)
print("used", len(used), "zh", len(zh), "missing", len(missing))
for m in missing:
    print(" MISSING", m)
