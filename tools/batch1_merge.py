"""
Batch 1: Extract and merge events from Factions A-D into master timeline.
Files: ashroot_grove, balifa_grove, crumon_dynasty, dark_photoli, deepwell_grove, exile_scavengers
"""
import os, re

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
tl_path = os.path.join(canon_dir, "meta", "master_timeline.md")

# ── New events to insert ──────────────────────────────────────────────
# (year, text, source_file)
# Each event distilled from reading the full files

batch1_events = [
    # ASHROOT GROVE
    (2440, "Ashroot Grove founded \u2014 a penitent ECOS order establishes a watch-station on the Old Grove perimeter; Arch Druidess Venya takes the surname \"Sorrow\"",
     "factions/ashroot_grove.md"),
    
    # BALIFA GROVE / ECOS
    (2493, "ECOS ratifies the **Grove Doctrine** \u2014 codifying \"nature above politics\" and authorizing the ECOS Fleet to intervene in ecological crises by force",
     "factions/balifa_grove.md"),
    
    # CRUMON DYNASTY
    (2550, "Crumon Dynasty builds the **Spire Foundries** on Crushspire \u2014 monument-factories modeled after the Ustur Elder Spire on Ioki",
     "factions/crumon_dynasty.md"),
    (2560, "Crumon Dynasty hires the **Order of Seasons** to crush political opposition in Pavo Passage \u2014 the Order fulfills the contract",
     "factions/crumon_dynasty.md"),
    (2563, "**\"The Night\"** \u2014 the Order of Seasons kills the entire Crumon royal family for non-payment; Queen Cathris disappears; only baby Ike Pavo survives (absent from sector)",
     "factions/crumon_dynasty.md"),
    
    # DARK PHOTOLI
    (2624, "Dark Photoli experiments **released in Everstorm sector** \u2014 bioengineered creatures terrorize the region; local government hires captains to deal with the threat",
     "factions/dark_photoli.md"),
    (2624, "**Bah** (Dark Photoli) arrives at Etira after the Never Alone incident, butchers the Dreamer's corpse, and retrieves a mysterious **silver gem** artifact",
     "factions/dark_photoli.md"),
    
    # DEEPWELL GROVE
    (2501, "ECOS Fleet intervenes at **Ilidae** under Grove Doctrine to protect the Termiks from exploitation \u2014 Deepwell Grove's origin",
     "factions/deepwell_grove.md"),
    (2569, "ECOS and Iris Academy co-found **The Nursery** at Ilidae \u2014 a sustainable city designed around Termik welfare; Deepwell Grove formalized",
     "factions/deepwell_grove.md"),
    
    # EXILE SCAVENGERS
    (2530, "First scav-crews form in the aftermath of the Convergence War \u2014 desperate MRZ drifters begin stripping abandoned warships and stations",
     "factions/exile_scavengers.md"),
    (2550, "Exile Scavengers professionalize \u2014 the **Flotsam Exchange** (orbital bazaar in MRZ-12 orbit) develops as a stable market",
     "factions/exile_scavengers.md"),
    (2571, "Scav-crew discovers the **Whisper Engine** in Akalma Deep \u2014 a Sogmian Cosmic Current-reactive artifact; sold to Malkabaets for 40,000 ATLAS",
     "factions/exile_scavengers.md"),
    (2589, "Ghost Sevra Cull recovers the **Sogmian Memory Core** from Akalma Deep \u2014 contains House Akalma court records; sold to the Scriptorium's Whisper Conclave",
     "factions/exile_scavengers.md"),
    (2603, "Fennek's Bonepickers find the **Void Anchor** in a Current Cavity \u2014 an impossibly dense artifact of unknown origin; sold for est. 80,000+ ATLAS",
     "factions/exile_scavengers.md"),
    (2614, "Clatter.lrnr recovers the **Cradle Corridor Map** from a Ghost Station \u2014 Ustur navigational data of HRZ border sectors; sold to Relic Barons (Whisperkin)",
     "factions/exile_scavengers.md"),
]

# ── Read existing timeline ────────────────────────────────────────────
with open(tl_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the undated/deferred section
undated_idx = None
for i, line in enumerate(lines):
    if "Undated Events" in line or "Deferred" in line:
        undated_idx = i
        break

if undated_idx is None:
    undated_idx = len(lines) - 1

# ── Check for already-existing events ─────────────────────────────────
existing_text = "".join(lines)
new_events = []
for year, text, source in batch1_events:
    # Check if source file is already referenced at this year
    key_phrase = source.replace("factions/", "").replace(".md", "")
    year_str = f"~{year}"
    
    # Simple check: is there already a line with this year + something from this source?
    already = False
    for line in lines:
        if year_str in line and key_phrase.replace("_", " ") in line.lower():
            already = True
            break
    
    if not already:
        new_events.append((year, text, source))

print(f"Events to add: {len(new_events)} (filtered from {len(batch1_events)})")

# ── Insert events in chronological order ──────────────────────────────
def find_insert_point(year, lines, max_idx):
    """Find the correct insertion point for this year."""
    best = None
    for i in range(max_idx):
        m = re.match(r"^- \*\*~(\d{4})\*\*:", lines[i])
        pm = re.match(r"^- \*\*Pre-~(\d{4})\*\*:", lines[i])
        if m:
            ly = int(m.group(1))
            if ly <= year:
                # Skip source line
                if i + 1 < len(lines) and lines[i+1].strip().startswith("- \U0001f4c1"):
                    best = i + 2
                else:
                    best = i + 1
        elif pm:
            ly = int(pm.group(1))
            if ly <= year:
                if i + 1 < len(lines) and lines[i+1].strip().startswith("- \U0001f4c1"):
                    best = i + 2
                else:
                    best = i + 1
    return best

new_events.sort(key=lambda x: x[0])
inserted = 0
for year, text, source in new_events:
    idx = find_insert_point(year, lines, undated_idx + inserted)
    if idx is None:
        print(f"  WARNING: No insertion point for ~{year}")
        continue
    
    new_lines = [
        f"- **~{year}**: {text}\r\n",
        f"  - \U0001f4c1 `{source}` \u2705 *new*\r\n",
    ]
    lines = lines[:idx] + new_lines + lines[idx:]
    inserted += 2
    print(f"  + ~{year}: {text[:70]}...")

# ── Write back ────────────────────────────────────────────────────────
with open(tl_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

# Count events
evts = sum(1 for l in lines if re.match(r"^- \*\*[~P]", l))
print(f"\nTotal events now: {evts}")
print(f"Total lines: {len(lines)}")
