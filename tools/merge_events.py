"""
Merge all approved undated events into the main timeline.
Adjustments:
- TAPP: ~2568 (after Ruling Conclave ~2567)
- Iris Academy: ~2525 (early Golden Era per user)
"""
import os, re

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
path = os.path.join(canon_dir, "meta", "master_timeline.md")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Define all approved events to insert into the main timeline
# Format: (year, text, source)
new_events = [
    # Ancient / Pre-era
    # Living Factories - add note in Primitive Era section
    
    # Convergence War era
    (2515, "Order of Seasons created \u2014 an assassin cult secretly revering the Iris aspect Dusk (Convergence War era)", "factions/order_of_seasons.md"),
    
    # Expansion Era
    (2470, "Panemorfa group formed \u2014 covert faction operating decades before the Denebula Utopia takes shape (~2495)", "factions/panemorfa.md"),
    
    # Golden Era - Early
    (2523, "Anfoil State formally constituted under Ponel.eldr \u2014 Meritocratic Technate established post-Accord", "factions/anfoil_state.md"),
    (2524, "Xyanyang Government formed as independent state after MRZ breakaway (~2522)", "factions/xyanyang_government.md"),
    (2525, "Iris Academy founded by Chior.eldr, Professor Exfeheros, and leading academics at Zenith Door \u2014 neutral organization devoted to peace and galactic research", "factions/iris_academy.md"),
    (2525, "Nimrod Trackers DAC founded in Communion sector \u2014 monster hunters specializing in exotic fauna", "factions/nimrod_trackers.md"),
    (2526, "Xianyang Enforcers created as military arm of Xyanyang Government", "factions/xianyang_enforcers.md"),
    (2530, "Gate Garrison formally organized \u2014 multi-species bounty-hunter organization led by an Awakened Tufa, operating from the HRZ", "factions/gate_garrison.md"),
    (2532, "Ustur Regency established in Pavo Passage; Winter Fist Path (Ustur martial sect) arrives with the Regency", "factions/ustur_regency_pavo.md"),
    (2538, "Abyd-IX first provisional government formed during civil war", "factions/abyd_government.md"),
    (2550, "Holpla Insurances Inc founded \u2014 galactic insurance corporation based at COP Cradle", "factions/holpla_insurances.md"),
    
    # Golden Era - Pavo sequence
    (2567, "Ruling Conclave established in Pavo Passage \u2014 fa\u00e7ade democracy created immediately after civil war ends", "factions/ruling_conclave.md"),
    (2568, "TAPP (Toll Authority of Pavo Passage) formalized under Conclave governance \u2014 toll infrastructure becomes the sector's power machine", "factions/tapp.md"),
    (2568, "Meridian Trading Company (MTC) enters Pavo Passage \u2014 MUD/Synod front for soft capture", "factions/mtc.md"),
    (2569, "Vale Horizon Exchange (VHE) founded by Seraphine Vale \u2014 counter-MTC balance, the people's corridor", "factions/vhe.md"),
]

# Parse the existing timeline into lines
lines = content.split("\n")

# Find the end of the Current Age section (before the Undated Events header)
undated_idx = None
for i, line in enumerate(lines):
    if "Undated Events" in line and "Pending" in line:
        undated_idx = i
        break

# We need to insert events into the correct era sections
# Build insertion map: find era section boundaries
era_sections = {}
current_era = None
for i, line in enumerate(lines):
    if line.startswith("## ") and any(era in line for era in ["Primitive", "Foundation", "Expansion", "Convergence", "Golden", "Current"]):
        current_era = line.strip()
        era_sections[current_era] = {"start": i, "end": None}
    elif line.startswith("## ") and current_era:
        era_sections[current_era]["end"] = i
        current_era = None
    elif line.startswith("---") and current_era and i > era_sections[current_era]["start"] + 2:
        era_sections[current_era]["end"] = i

# For simplicity, insert new events right before the undated section
# by adding them to the correct era sections
# But actually it's easier to just insert them as new lines before the --- that ends each era

# Let's take a simpler approach: insert all new events before the Undated Events section
# as a "Newly Added Events" block, then we can re-sort later

# Actually, the cleanest approach: insert into the right positions
# Find the last event line before undated section for each era year range

def get_insertion_point(year, lines, undated_idx):
    """Find where to insert an event with the given year."""
    # Look for the last line with a year <= our year, before undated section
    best_idx = None
    for i in range(undated_idx):
        m = re.match(r"^- \*\*~(\d{4})\*\*:", lines[i])
        if m:
            line_year = int(m.group(1))
            if line_year <= year:
                # Check if next line is a source line
                if i + 1 < len(lines) and lines[i+1].strip().startswith("- \U0001f4c1"):
                    best_idx = i + 2  # after the source line
                else:
                    best_idx = i + 1
    return best_idx

# Sort new events by year
new_events.sort(key=lambda x: x[0])

# Insert events one by one, adjusting indices
inserted = 0
for year, text, source in new_events:
    idx = get_insertion_point(year, lines, undated_idx + inserted)
    if idx is None:
        print(f"WARNING: Could not find insertion point for ~{year}: {text[:50]}")
        continue
    
    new_lines = [
        f"- **~{year}**: {text}",
        f"  - \U0001f4c1 `{source}` \u2705 *new*",
    ]
    lines = lines[:idx] + new_lines + lines[idx:]
    inserted += len(new_lines)
    print(f"Inserted ~{year} at line {idx}: {text[:60]}...")

# Also add Living Factories note in Primitive Era (before first event)
# Find Primitive Era section
for i, line in enumerate(lines):
    if "Primitive Era" in line and line.startswith("##"):
        # Insert after the blank line following the header
        insert_at = i + 2
        lf_lines = [
            "- **Pre-~1461**: The Living Factories \u2014 an ancient mechanical life form \u2014 are already active, predating all known Galia species. They later interact with humanity when AI begins on Earth",
            "  - \U0001f4c1 `factions/living_factories.md` \u2705 *new*",
        ]
        lines = lines[:insert_at] + lf_lines + lines[insert_at:]
        inserted += len(lf_lines)
        print(f"Inserted Living Factories at line {insert_at}")
        break

# Write back
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nTotal new events inserted: {len(new_events) + 1}")
print(f"Total lines now: {len(lines)}")

# Update the header stats
total_events = 0
for line in lines:
    if re.match(r"^- \*\*[~P]", line):
        total_events += 1

print(f"Approximate total events: {total_events}")
