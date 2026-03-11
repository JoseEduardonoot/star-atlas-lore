"""
Phase 3: Cross-check every canon file against master timeline.

Reports:
1. DATE CONTRADICTIONS — same event described with different dates in different files
2. ORPHANED DATES — dates in source files NOT in the master timeline
3. CHRONOLOGICAL ERRORS — events out of order within a file
4. DUPLICATE EVENTS — near-identical text at the same year in the timeline
"""
import os, re, json
from collections import defaultdict

CANON_DIR = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
TIMELINE_PATH = os.path.join(CANON_DIR, "meta", "master_timeline.md")

# ── Step 1: Parse the master timeline ────────────────────────────────────
def parse_timeline():
    """Extract all dated events from the master timeline."""
    with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    events = []
    current_year = None
    for i, line in enumerate(lines):
        m = re.match(r"^- \*\*~?(\d{4})\*\*:\s*(.+)", line)
        pm = re.match(r"^- \*\*Pre-~(\d{4})\*\*:\s*(.+)", line)
        if m:
            year = int(m.group(1))
            text = m.group(2).strip()
            events.append({"year": year, "text": text, "line": i+1})
        elif pm:
            year = int(pm.group(1))
            text = pm.group(2).strip()
            events.append({"year": year, "text": text, "line": i+1, "pre": True})

    return events

# ── Step 2: Scan all canon files for dates ───────────────────────────────
def scan_all_files():
    """Walk every .md file in every canon subdirectory and extract dates."""
    file_dates = {}
    for root, dirs, files in os.walk(CANON_DIR):
        # Skip meta directory (contains the timeline itself and raw data)
        rel = os.path.relpath(root, CANON_DIR)
        if rel.startswith("meta"):
            continue

        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            rel_path = os.path.relpath(fpath, CANON_DIR)

            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            dates_in_file = []
            for i, line in enumerate(lines):
                # Find all ~YYYY patterns
                for m in re.finditer(r"~(\d{4})", line):
                    year = int(m.group(1))
                    # Get context: the full line, cleaned
                    ctx = line.strip()
                    # Skip table headers, metadata, cross-reference lines
                    if ctx.startswith("|---") or ctx.startswith("**Source**") or ctx.startswith("**Status**"):
                        continue
                    dates_in_file.append({
                        "year": year,
                        "line": i+1,
                        "context": ctx[:200],
                    })

            if dates_in_file:
                file_dates[rel_path] = dates_in_file

    return file_dates

# ── Step 3: Find contradictions ──────────────────────────────────────────
def find_contradictions(file_dates):
    """Find cases where the same event has different dates in different files."""
    contradictions = []

    # Build an index: keyword-set -> [(file, year, context)]
    keyword_index = defaultdict(list)
    for fpath, dates in file_dates.items():
        for d in dates:
            # Extract meaningful keywords
            words = set(re.findall(r"[A-Z][a-z]+(?:[A-Z][a-z]+)*|\b[A-Z]{2,}\b", d["context"]))
            # Filter to named entities only
            named = {w for w in words if len(w) > 3}
            if named:
                key = frozenset(list(named)[:5])  # cap at 5 keywords
                keyword_index[key].append({
                    "file": fpath,
                    "year": d["year"],
                    "context": d["context"],
                })

    # Check for same keywords with different years across files
    for key, entries in keyword_index.items():
        years = set(e["year"] for e in entries)
        files = set(e["file"] for e in entries)
        if len(years) > 1 and len(files) > 1:
            # Potential contradiction
            contradictions.append({
                "keywords": sorted(key),
                "entries": entries,
            })

    return contradictions

# ── Step 4: Find orphaned dates ──────────────────────────────────────────
def find_orphaned_dates(timeline_events, file_dates):
    """Find dates in source files that don't appear in the master timeline."""
    # Build set of (year, keyword-snippet) from timeline
    timeline_years = set(e["year"] for e in timeline_events)

    orphaned = []
    for fpath, dates in file_dates.items():
        for d in dates:
            # Check if this date's year exists in timeline at all
            if d["year"] not in timeline_years:
                orphaned.append({
                    "file": fpath,
                    "year": d["year"],
                    "context": d["context"],
                    "line": d["line"],
                    "type": "YEAR_MISSING"
                })

    return orphaned

# ── Step 5: Find chronological errors within files ───────────────────────
def find_chrono_errors(file_dates):
    """Find files where dates appear out of chronological order in lists."""
    errors = []
    for fpath, dates in file_dates.items():
        # Only check files with multiple dates
        if len(dates) < 2:
            continue

        # Check if dates in bullet lists are chronological
        list_dates = [d for d in dates if d["context"].startswith("- **~")]
        if len(list_dates) < 2:
            continue

        for i in range(len(list_dates) - 1):
            if list_dates[i]["year"] > list_dates[i+1]["year"]:
                errors.append({
                    "file": fpath,
                    "earlier_line": list_dates[i+1]["line"],
                    "earlier_year": list_dates[i+1]["year"],
                    "later_line": list_dates[i]["line"],
                    "later_year": list_dates[i]["year"],
                })

    return errors

# ── Step 6: Find duplicate timeline entries ──────────────────────────────
def find_duplicates(timeline_events):
    """Find near-duplicate events at the same year in the timeline."""
    dupes = []
    year_groups = defaultdict(list)
    for e in timeline_events:
        year_groups[e["year"]].append(e)

    for year, events in sorted(year_groups.items()):
        if len(events) < 2:
            continue

        for i in range(len(events)):
            for j in range(i+1, len(events)):
                a = events[i]["text"].lower()
                b = events[j]["text"].lower()
                # Check word overlap
                wa = set(re.findall(r"\w{4,}", a))
                wb = set(re.findall(r"\w{4,}", b))
                if wa and wb:
                    overlap = len(wa & wb) / min(len(wa), len(wb))
                    if overlap > 0.5:
                        dupes.append({
                            "year": year,
                            "line_a": events[i]["line"],
                            "text_a": events[i]["text"][:100],
                            "line_b": events[j]["line"],
                            "text_b": events[j]["text"][:100],
                            "overlap": round(overlap, 2),
                        })

    return dupes

# ── Step 7: Check eras_of_star_atlas date ordering ──────────────────────
def check_eras_ordering():
    """Verify dates in eras backbone are in chronological order."""
    eras_path = os.path.join(CANON_DIR, "history", "eras_of_star_atlas.md")
    with open(eras_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    errors = []
    prev_year = 0
    for i, line in enumerate(lines):
        m = re.match(r"^- \*\*~(\d{4})\*\*:", line)
        if m:
            year = int(m.group(1))
            if year < prev_year:
                errors.append({
                    "line": i+1,
                    "year": year,
                    "prev_year": prev_year,
                    "text": line.strip()[:100],
                })
            prev_year = year

    return errors

# ── Run all checks ───────────────────────────────────────────────────────
print("=" * 70)
print("PHASE 3: MASTER TIMELINE CROSS-CHECK VERIFICATION")
print("=" * 70)

print("\n[1/7] Parsing master timeline...")
timeline = parse_timeline()
print(f"  → {len(timeline)} events found")

print("\n[2/7] Scanning all canon files...")
file_dates = scan_all_files()
total_files = len(file_dates)
total_dates = sum(len(d) for d in file_dates.values())
print(f"  → {total_files} files with dates, {total_dates} total date references")

print("\n[3/7] Checking eras_of_star_atlas.md ordering...")
eras_errors = check_eras_ordering()
if eras_errors:
    print(f"  ⚠️ {len(eras_errors)} CHRONOLOGICAL ERRORS in eras backbone:")
    for e in eras_errors:
        print(f"    Line {e['line']}: ~{e['year']} appears after ~{e['prev_year']}")
        print(f"      {e['text']}")
else:
    print("  ✅ All dates in chronological order")

print("\n[4/7] Finding orphaned dates (in files but NOT in timeline)...")
orphaned = find_orphaned_dates(timeline, file_dates)
if orphaned:
    year_missing = [o for o in orphaned if o["type"] == "YEAR_MISSING"]
    print(f"  ⚠️ {len(year_missing)} dates in files with years NOT in timeline:")
    # Group by year for cleaner output
    by_year = defaultdict(list)
    for o in year_missing:
        by_year[o["year"]].append(o)
    for year in sorted(by_year.keys()):
        items = by_year[year]
        print(f"    ~{year}: ({len(items)} refs)")
        for item in items[:3]:
            print(f"      {item['file']}:{item['line']} — {item['context'][:80]}")
        if len(items) > 3:
            print(f"      ... and {len(items)-3} more")
else:
    print("  ✅ All file dates have corresponding timeline years")

print("\n[5/7] Finding near-duplicate events in timeline...")
dupes = find_duplicates(timeline)
if dupes:
    print(f"  ⚠️ {len(dupes)} potential duplicate pairs:")
    for d in dupes[:20]:
        print(f"    ~{d['year']} (overlap {d['overlap']}):")
        print(f"      L{d['line_a']}: {d['text_a'][:80]}...")
        print(f"      L{d['line_b']}: {d['text_b'][:80]}...")
else:
    print("  ✅ No significant duplicates")

print("\n[6/7] Finding chronological errors within individual files...")
chrono = find_chrono_errors(file_dates)
if chrono:
    print(f"  ⚠️ {len(chrono)} files with out-of-order dates:")
    for c in chrono[:15]:
        print(f"    {c['file']}: ~{c['later_year']} (L{c['later_line']}) before ~{c['earlier_year']} (L{c['earlier_line']})")
else:
    print("  ✅ All files have chronological date ordering")

print("\n[7/7] Checking for contradiction patterns across files...")
contradictions = find_contradictions(file_dates)
# Filter to real contradictions (not just different events at the same entity)
real_contradictions = [c for c in contradictions if len(c["entries"]) <= 5]
if real_contradictions:
    print(f"  ⚠️ {len(real_contradictions)} potential contradictions:")
    for c in real_contradictions[:15]:
        print(f"    Keywords: {', '.join(c['keywords'][:5])}")
        for e in c["entries"][:4]:
            print(f"      ~{e['year']} in {e['file']}: {e['context'][:60]}...")
else:
    print("  ✅ No clear contradictions found")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"  Timeline events:        {len(timeline)}")
print(f"  Canon files scanned:    {total_files}")
print(f"  Total date references:  {total_dates}")
print(f"  Eras ordering errors:   {len(eras_errors)}")
print(f"  Orphaned year refs:     {len([o for o in orphaned if o['type']=='YEAR_MISSING'])}")
print(f"  Duplicate pairs:        {len(dupes)}")
print(f"  Chrono errors in files: {len(chrono)}")
print(f"  Cross-file conflicts:   {len(real_contradictions)}")
print("=" * 70)

# Save detailed report
report_path = os.path.join(CANON_DIR, "meta", "_verification_report.json")
report = {
    "summary": {
        "timeline_events": len(timeline),
        "files_scanned": total_files,
        "date_references": total_dates,
    },
    "eras_ordering_errors": eras_errors,
    "orphaned_years": [{"year": o["year"], "file": o["file"], "line": o["line"], "context": o["context"][:100]} for o in orphaned if o["type"] == "YEAR_MISSING"],
    "duplicates": dupes,
    "chrono_errors": chrono,
    "contradictions": [{"keywords": c["keywords"][:5], "entries": [{"year": e["year"], "file": e["file"], "context": e["context"][:100]} for e in c["entries"][:5]]} for c in real_contradictions[:20]],
}
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)
print(f"\nDetailed report saved to: {report_path}")
