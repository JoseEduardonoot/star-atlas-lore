"""Read verification report summary."""
import json
path = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon\meta\_verification_report.json"
with open(path, "r", encoding="utf-8") as f:
    d = json.load(f)
s = d["summary"]
print("=== FINAL VERIFICATION ===")
print(f"Events: {s['timeline_events']}")
print(f"Files scanned: {s['files_scanned']}")
print(f"Date references: {s['date_references']}")
print(f"Eras ordering errors: {len(d['eras_ordering_errors'])}")
print(f"Orphaned years: {len(d['orphaned_years'])}")
print(f"Duplicates: {len(d['duplicates'])}")
print(f"Chrono errors: {len(d['chrono_errors'])}")
print(f"Contradictions: {len(d['contradictions'])}")

if d["eras_ordering_errors"]:
    print("\nERAS ERRORS:")
    for e in d["eras_ordering_errors"]:
        print(f"  L{e['line']}: ~{e['year']} after ~{e['prev_year']}")

if d["duplicates"]:
    print("\nDUPLICATES:")
    for dd in d["duplicates"]:
        print(f"  ~{dd['year']} ({dd['overlap']}): L{dd['line_a']} vs L{dd['line_b']}")
