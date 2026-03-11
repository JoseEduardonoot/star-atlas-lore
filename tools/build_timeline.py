"""
Build master_timeline.md with smart de-duplication:
1. Use eras_of_star_atlas.md as the curated backbone
2. Extract additional events from all other canon files
3. De-duplicate using keyword overlap scoring
4. Output a clean, readable timeline
"""
import re, os, json
from collections import defaultdict

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"

# ──────────────────────────────────────────────
# Step 1: Parse eras_of_star_atlas.md as backbone
# ──────────────────────────────────────────────

eras_path = os.path.join(canon_dir, "history", "eras_of_star_atlas.md")
with open(eras_path, "r", encoding="utf-8") as f:
    eras_lines = f.readlines()

backbone = []  # (year, clean_text, source)
for line in eras_lines:
    m = re.match(r"^- \*\*~(\d{4})\*\*:\s*(.+)", line.strip())
    if m:
        year = int(m.group(1))
        text = m.group(2).strip()
        # Clean up text
        text = re.sub(r"\*\*", "", text)  # remove bold markers
        text = text.rstrip(".")
        backbone.append((year, text, "history/eras_of_star_atlas.md"))

print(f"Backbone events from eras_of_star_atlas.md: {len(backbone)}")

# ──────────────────────────────────────────────
# Step 2: Extract all events from all other files
# ──────────────────────────────────────────────

skip_files = {
    "history/eras_of_star_atlas.md",      # already used as backbone
    "meta/master_timeline.md",             # output file
    "meta/_timeline_raw.json",             # temp file
    "meta/named_characters.md",            # character registry, not events
}

other_events = []
for root, dirs, files in os.walk(canon_dir):
    for f in files:
        if not f.endswith(".md"):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, canon_dir).replace("\\", "/")
        if rel in skip_files:
            continue
        try:
            with open(path, "r", encoding="utf-8") as fh:
                for line_num, line in enumerate(fh, 1):
                    # Only match lines that start with a date pattern (timeline entries)
                    stripped = line.strip()
                    # Match: - **~YYYY**: text  or  - ~YYYY: text
                    m = re.match(r"^[-*]\s*\*?\*?~(\d{4})\*?\*?:?\s*(.+)", stripped)
                    if not m:
                        continue
                    year = int(m.group(1))
                    text = m.group(2).strip()
                    # Skip cross-reference lines, table headers, open questions
                    if any(x in text.lower() for x in ["cross-ref", "canon/", "→", "⏸️", "q-", "~~"]):
                        continue
                    # Skip very short
                    if len(text) < 15:
                        continue
                    # Clean
                    text = re.sub(r"\*\*", "", text)  # remove bold
                    text = text.rstrip(".")
                    if len(text) > 200:
                        text = text[:197] + "..."
                    other_events.append((year, text, rel))
        except:
            pass

print(f"Other events from non-eras files: {len(other_events)}")

# ──────────────────────────────────────────────
# Step 3: Smart de-dedup — find events NOT in backbone
# ──────────────────────────────────────────────

def extract_keywords(text):
    """Extract meaningful keywords for comparison."""
    t = text.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    words = set(t.split())
    # Remove common stop words
    stops = {"the", "a", "an", "of", "in", "to", "and", "is", "are", "was",
             "were", "for", "on", "at", "by", "from", "with", "as", "this",
             "that", "their", "its", "has", "had", "be", "been", "they",
             "it", "he", "she", "his", "her", "which", "who", "whom",
             "after", "before", "during", "first", "new", "begin", "begins",
             "also", "but", "not", "or", "all", "most", "into", "over"}
    return words - stops

def overlap_score(kw1, kw2):
    """Score how much two keyword sets overlap."""
    if not kw1 or not kw2:
        return 0
    intersection = kw1 & kw2
    smaller = min(len(kw1), len(kw2))
    return len(intersection) / max(smaller, 1)

# Index backbone by year
backbone_by_year = defaultdict(list)
for year, text, src in backbone:
    kw = extract_keywords(text)
    backbone_by_year[year].append((text, kw, src))

# Find genuinely new events
new_events = []
seen_new = set()  # prevent dupes among new events too

for year, text, src in other_events:
    kw = extract_keywords(text)
    
    # Check against backbone events for this year
    is_dupe = False
    for bb_text, bb_kw, bb_src in backbone_by_year.get(year, []):
        score = overlap_score(kw, bb_kw)
        if score > 0.4:  # 40% keyword overlap = likely same event
            is_dupe = True
            break
    
    if is_dupe:
        continue
    
    # Check against already-accepted new events for this year
    key = f"{year}:{' '.join(sorted(list(kw)[:5]))}"
    for existing_key in list(seen_new):
        if existing_key.startswith(f"{year}:"):
            ex_kw = set(existing_key.split(":")[1].split())
            if overlap_score(kw, ex_kw) > 0.5:
                is_dupe = True
                break
    
    if is_dupe:
        continue
    
    seen_new.add(key)
    new_events.append((year, text, src))

print(f"New events (not in backbone): {len(new_events)}")

# ──────────────────────────────────────────────
# Step 4: Merge backbone + new events, sort, write
# ──────────────────────────────────────────────

all_events = []
for year, text, src in backbone:
    all_events.append({"year": year, "text": text, "source": src, "status": "backbone"})
for year, text, src in new_events:
    all_events.append({"year": year, "text": text, "source": src, "status": "supplemental"})

all_events.sort(key=lambda x: (x["year"], x["source"]))

ERAS = [
    ("Primitive Era", 0, 1826, "~0–~1826"),
    ("Foundation Era", 1826, 2305, "~1826–~2305"),
    ("Expansion Era", 2305, 2512, "~2305–~2512"),
    ("Convergence War", 2512, 2523, "~2512–~2523"),
    ("Golden Era", 2523, 2620, "~2523–~2620"),
    ("Current Age", 2620, 9999, "~2620–present"),
]

ERA_EMOJIS = {
    "Primitive Era": "🦴",
    "Foundation Era": "🏛️",
    "Expansion Era": "🚀",
    "Convergence War": "⚔️",
    "Golden Era": "✨",
    "Current Age": "🌐",
}

def get_era(year):
    for name, start, end, label in ERAS:
        if start <= year < end:
            return name
    return "Unknown"

# Group by era
by_era = defaultdict(list)
for ev in all_events:
    era = get_era(ev["year"])
    by_era[era].append(ev)

# Count stats
total = len(all_events)
backbone_count = sum(1 for e in all_events if e["status"] == "backbone")
supplemental_count = total - backbone_count

# Build markdown
lines = []
lines.append("# 📅 Canon Document: MASTER TIMELINE")
lines.append("")
lines.append("**Status**: 🟢 Canon (Compiled from all canon sources, Feb 2026)")
lines.append(f"**Total Events**: {total} ({backbone_count} from eras backbone + {supplemental_count} supplemental)")
lines.append(f"**Unique Years**: {len(set(e['year'] for e in all_events))}")
lines.append(f"**Range**: ~{min(e['year'] for e in all_events)} — ~{max(e['year'] for e in all_events)}")
lines.append("")
lines.append("> [!NOTE]")
lines.append("> This is the single source of truth for all dated lore events in Star Atlas canon.")
lines.append("> All dates use the `~YYYY` convention (approximate galactic standard years).")
lines.append("> Events are sourced from eras_of_star_atlas.md (backbone) and supplemented from all canon files.")
lines.append("")
lines.append("---")
lines.append("")

for era_name, era_start, era_end, era_label in ERAS:
    era_events = by_era.get(era_name, [])
    if not era_events:
        continue
    
    emoji = ERA_EMOJIS.get(era_name, "📌")
    lines.append(f"## {emoji} {era_name} ({era_label})")
    lines.append("")
    
    # Group by year
    events_by_year = defaultdict(list)
    for ev in era_events:
        events_by_year[ev["year"]].append(ev)
    
    for year in sorted(events_by_year.keys()):
        year_events = events_by_year[year]
        for ev in year_events:
            src_tag = f"`{ev['source']}`"
            lines.append(f"- **~{year}**: {ev['text']}")
            lines.append(f"  - 📁 {src_tag}")
    
    lines.append("")
    lines.append("---")
    lines.append("")

# Footer
lines.append("## 📋 Undated Events (Pending Placement)")
lines.append("")
lines.append("> Events with no confirmed date will be listed here during Phase 2.")
lines.append("> Each will include a proposed date and rationale for user approval.")
lines.append("")
lines.append("*(To be populated)*")
lines.append("")

out_path = os.path.join(canon_dir, "meta", "master_timeline.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nWritten: {out_path}")
print(f"Total events: {total}")
print(f"Total lines: {len(lines)}")
file_size = os.path.getsize(out_path)
print(f"File size: {file_size / 1024:.1f} KB")
