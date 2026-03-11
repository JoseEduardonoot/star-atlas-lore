"""Remove new duplicates introduced by batch merges."""
import re, json

path = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon\meta\master_timeline.md"
report_path = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon\meta\_verification_report.json"

# Read duplicates from report
with open(report_path, "r", encoding="utf-8") as f:
    report = json.load(f)

dupes = report["duplicates"]
print(f"Duplicates to resolve: {len(dupes)}")

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines_to_remove = set()

for d in dupes:
    la = d["line_a"] - 1  # 0-indexed
    lb = d["line_b"] - 1
    
    # Keep the longer/more detailed version
    text_a = lines[la].strip() if la < len(lines) else ""
    text_b = lines[lb].strip() if lb < len(lines) else ""
    
    # Remove the shorter one
    if len(text_a) >= len(text_b):
        remove = lb
    else:
        remove = la
    
    lines_to_remove.add(remove)
    # Also remove source line if it follows
    if remove + 1 < len(lines) and "\U0001f4c1" in lines[remove + 1]:
        lines_to_remove.add(remove + 1)
    
    print(f"  ~{d['year']}: removing L{remove+1} (keeping L{la+1 if remove == lb else lb+1})")

new_lines = [lines[i] for i in range(len(lines)) if i not in lines_to_remove]

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

evts = sum(1 for l in new_lines if re.match(r"^- \*\*[~P]", l))
print(f"\nRemoved {len(lines) - len(new_lines)} lines")
print(f"Total events now: {evts}")
