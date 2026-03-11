"""Assess the full scope of lore files for event extraction."""
import os, re

canon = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"

# Count all .md files by subdirectory
dirs = {}
all_files = []
for root, _, files in os.walk(canon):
    rel = os.path.relpath(root, canon)
    md_files = [f for f in files if f.endswith(".md")]
    if md_files:
        dirs[rel] = len(md_files)
        for f in md_files:
            all_files.append(os.path.join(root, f))

print("=== CANON FILE COUNT BY DIRECTORY ===")
total = 0
for d in sorted(dirs.keys()):
    print(f"  {d}: {dirs[d]} files")
    total += dirs[d]
print(f"  TOTAL: {total} files")

# Read the timeline and collect source file references
tl_path = os.path.join(canon, "meta", "master_timeline.md")
with open(tl_path, "r", encoding="utf-8") as f:
    tl = f.read()

# Extract all source file references from timeline
source_lines = re.findall(r"📁 `(.+?)`", tl)
sources = set(source_lines)
print(f"\n=== FILES REFERENCED IN TIMELINE ===")
print(f"  {len(sources)} unique source file paths referenced")

# Find canon files NOT referenced in timeline at all
unreferenced = []
for fpath in all_files:
    rel = os.path.relpath(fpath, canon).replace(os.sep, "/")
    if rel.startswith("meta/"):
        continue
    
    basename = os.path.basename(fpath)
    found = any(basename.replace(".md", "") in s for s in sources)
    if not found:
        # Count events (dates) in the file
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        date_count = len(re.findall(r"~\d{4}", content))
        size = len(content)
        unreferenced.append((rel, date_count, size))

print(f"\n=== FILES NOT REFERENCED IN TIMELINE ({len(unreferenced)}) ===")
for f, dc, sz in sorted(unreferenced):
    status = f"{dc} dates" if dc > 0 else "NO dates"
    print(f"  {f} [{status}, {sz//1024}KB]")

# Count files with dates but not in timeline
with_dates = [f for f in unreferenced if f[1] > 0]
without_dates = [f for f in unreferenced if f[1] == 0]
print(f"\n=== SUMMARY ===")
print(f"  Total canon files: {total}")
print(f"  Referenced in timeline: {total - len(unreferenced)}")
print(f"  NOT referenced (with dates): {len(with_dates)}")
print(f"  NOT referenced (no dates): {len(without_dates)}")
