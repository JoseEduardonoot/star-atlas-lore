"""
Export master timeline to CSV format.
Columns: Year, Era, Event, Source
"""
import os, re, csv

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
tl_path = os.path.join(canon_dir, "meta", "master_timeline.md")
csv_path = os.path.join(canon_dir, "meta", "master_timeline.csv")

with open(tl_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Define era boundaries
era_ranges = [
    (0, 2349, "Primitive Age"),
    (2350, 2399, "Foundation Era"),
    (2400, 2449, "Cataclysm Era"),
    (2450, 2511, "Expansion Era"),
    (2512, 2523, "Convergence War"),
    (2524, 2619, "Golden Era"),
    (2620, 9999, "Current Age"),
]

def get_era(year):
    for lo, hi, name in era_ranges:
        if lo <= year <= hi:
            return name
    return "Unknown"

events = []
current_source = ""

for i, line in enumerate(lines):
    # Match event lines
    m = re.match(r"^- \*\*~?(\d{4})\*\*:\s*(.+)", line)
    pm = re.match(r"^- \*\*Pre-~(\d{4})\*\*:\s*(.+)", line)
    
    if m or pm:
        if m:
            year = int(m.group(1))
            text = m.group(2).strip()
        else:
            year = int(pm.group(1))
            text = "Pre-" + pm.group(2).strip()
        
        # Clean markdown bold/links from text
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"`(.+?)`", r"\1", text)
        text = text.replace("\u2014", "-").replace("\u2019", "'")
        
        # Look for source on next line
        source = ""
        if i + 1 < len(lines):
            sm = re.search(r"`(.+?\.md)`", lines[i + 1])
            if sm:
                source = sm.group(1)
        
        era = get_era(year)
        events.append({
            "year": year,
            "era": era,
            "event": text,
            "source": source,
        })

# Write CSV
with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["year", "era", "event", "source"])
    writer.writeheader()
    for e in events:
        writer.writerow(e)

print(f"Exported {len(events)} events to {csv_path}")

# Also print era breakdown
era_counts = {}
for e in events:
    era_counts[e["era"]] = era_counts.get(e["era"], 0) + 1

print("\nEra breakdown:")
for era, count in sorted(era_counts.items(), key=lambda x: [r[0] for r in era_ranges if r[2] == x[0]][0] if any(r[2] == x[0] for r in era_ranges) else 0):
    print(f"  {era}: {count} events")
