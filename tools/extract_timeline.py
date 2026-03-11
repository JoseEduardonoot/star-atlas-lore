"""Extract all dated events from canon files and output as JSON."""
import re, os, json
from collections import defaultdict

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
events = []

for root, dirs, files in os.walk(canon_dir):
    for f in files:
        if not f.endswith(".md"):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, canon_dir).replace("\\", "/")
        try:
            with open(path, "r", encoding="utf-8") as fh:
                for line_num, line in enumerate(fh, 1):
                    if not re.search(r"~\d{4}", line):
                        continue
                    years = re.findall(r"~(\d{4})", line)
                    clean = line.strip()
                    # Remove leading list markers
                    clean = re.sub(r"^[-*]\s*", "", clean)
                    # Remove leading bold year like **~2523**:
                    clean = re.sub(r"^\*\*~\d{4}\*\*:\s*", "", clean)
                    # Skip headers
                    if clean.startswith("#"):
                        continue
                    # Skip table separator rows
                    if clean.startswith("|") and "---" in clean:
                        continue
                    # Skip too-short
                    if len(clean) < 10:
                        continue
                    for year in years:
                        events.append({
                            "year": int(year),
                            "text": clean[:300],
                            "source": rel,
                            "line": line_num,
                        })
        except Exception as e:
            print(f"Error reading {path}: {e}")

events.sort(key=lambda x: (x["year"], x["source"]))

out_path = os.path.join(canon_dir, "meta", "_timeline_raw.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(events, f, indent=2, ensure_ascii=False)

unique_sources = len(set(e["source"] for e in events))
unique_years = len(set(e["year"] for e in events))
print(f"Extracted {len(events)} events from {unique_sources} files")
print(f"Unique years: {unique_years}")
print(f"Saved to: {out_path}")
