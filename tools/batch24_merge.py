"""
Batch 2-4: Extract and merge events from ALL remaining faction files (E-Z).
This covers ~27 files with ~40+ new events.
"""
import os, re

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
tl_path = os.path.join(canon_dir, "meta", "master_timeline.md")

# ── New events to insert ──────────────────────────────────────────────
# Distilled from reading all remaining faction files
batch24_events = [
    # FIMBUL BYOS (Builders of Your Own Ship)
    (2623, "**Fimbul BYOS** operations disrupted during COP MRZ Incursion \u2014 BYOS workshops in Pergamos raided for association with Pergamos shadow economy",
     "factions/fimbul_byos.md"),
    
    # FIMBUL ECOS (Fimbul ECOS division)
    (2623, "**Fimbul ECOS** division resources redirected during COP MRZ Incursion \u2014 ECOS-Fimbul joint programs face scrutiny",
     "factions/fimbul_ecos.md"),
    
    # GALIA MEDICAL UNION
    (2525, "COP charters the **Galia Medical Union** (GMU) \u2014 a permanent cross-faction medical corps to handle the casualties of the Convergence War",
     "factions/galia_medical_union.md"),
    (2530, "GMU fully operational \u2014 medical fleet deployed across Safe Zone; trauma surgery and rehabilitation infrastructure built",
     "factions/galia_medical_union.md"),
    (2617, "GMU launches **SDU technology** (Survey Data Units) \u2014 a tiered classification system for cataloguing biological data across sectors",
     "factions/galia_medical_union.md"),
    
    # GARADAR DAC
    (2512, "Ustur deserters under **Eolus.tcher** settle in an abandoned MRZ sector during the Convergence War \u2014 founding Garadar settlement",
     "factions/garadar_dac.md"),
    (2521, "**Zagah** (Sogmian exile) arrives at Garadar and begins organizing multi-species governance",
     "factions/garadar_dac.md"),
    (2557, "Garadar sector renamed **Eol-Garadar** \u2014 combining Eolus.tcher (Ustur founder) and Garadar (settlement name)",
     "factions/garadar_dac.md"),
    
    # GRAFT RESEARCH
    (2600, "**Graft Research** founded \u2014 a secretive biotech faction experimenting with biological augmentation and grafting technology",
     "factions/graft_research.md"),
    
    # IZARIANS
    (1965, "The original **Izar civilization collapses** in an unknown catastrophe \u2014 leaving ruins that become the foundation of Izarian culture",
     "factions/izarians.md"),
    
    # LUMIRO GROVE
    (2493, "**Lumiro Grove** established as ECOS's diplomatic and espionage grove \u2014 the faction's \"Voice\" on the High Circle",
     "factions/lumiro_grove.md"),
    
    # MALKABAETS
    (2545, "**Malkabaets** order founded \u2014 a mystical priesthood dedicated to interpreting the Cosmic Current; Sogmian-led with multi-species membership",
     "factions/malkabaets.md"),
    (2580, "First **Photoli** joins the Malkabaets \u2014 triggering an internal crisis; the order must reconcile Sogmian tradition with alien spirituality",
     "factions/malkabaets.md"),
    (2587, "**Jefos** (Prince of House Akalma) born in HRZ \u2014 Cosmic Current storm rages at his birth; Malkabaets declare it a prophetic sign",
     "factions/malkabaets.md"),
    
    # MERCHANT PRINCES OF DENEBULA
    (2471, "Merchant Prince **Ayevat** discovers **Denebula Sector** and begins building the foundation of the merchant prince system",
     "factions/merchant_princes_of_denebula.md"),
    (2511, "Merchant Prince **Gel** (Photoli co-founder of Denebula) dies under **mysterious circumstances**",
     "factions/merchant_princes_of_denebula.md"),
    
    # MYCENAS GOVERNMENT
    (2440, "The **Horror** begins at Mycenas \u2014 an external threat (later revealed as Tufa-related) terrorizes the sector for decades",
     "factions/mycenas_government.md"),
    
    # PERGAMOS SHADOW BANKS
    (2542, "**Pergamos** formally begins alliances with major MRZ factions \u2014 becoming the commercial backbone of the MRZ through its Shadow Banks",
     "factions/pergamos_shadow_banks.md"),
    (2550, "Pergamos **Shadow Contracts** extend to every MRZ sector \u2014 Shadow Banks control logistics, credit, and enforcement",
     "factions/pergamos_shadow_banks.md"),
    
    # SCRIPTORIUM OF THE LUMIKIR
    (2112, "**Scriptorium of the Lumikir** founded at Ka-dara \u2014 a knowledge-preserving institution built by the Lumikir species",
     "factions/scriptorium_of_the_lumikir.md"),
    (2535, "Scriptorium establishes the **Whisper Conclave** \u2014 an intelligence-gathering branch that trades in secrets and classified data",
     "factions/scriptorium_of_the_lumikir.md"),
    (2585, "Scriptorium **reorganized across entire homeworld** as data volume exceeds all previous projections",
     "factions/scriptorium_of_the_lumikir.md"),
    
    # SONS OF PATRAH
    (2624, "**Sons of Patrah** faction emerges \u2014 Sogmian militants loyal to House Patrah, active during the COP intervention era",
     "factions/sons_of_patrah.md"),
    
    # SORKOF PIRATES
    (2580, "**Sorkof Pirates** split from Jorvik \u2014 rejecting the codified Creed; become an independent pirate faction operating outside Jorvik law",
     "factions/sorkof_pirates.md"),
    
    # SWAMP LORDS
    (2530, "**Swamp Lords** settle in the marshlands of Dream Reach \u2014 reclusive warlords who build fortress-habitats in hostile terrain",
     "factions/swamp_lords.md"),
    
    # THE COLLECTIVE ANARCHY
    (2570, "**The Collective Anarchy** emerges \u2014 a decentralized anarchist network in the MRZ advocating for total independence from COP authority",
     "factions/the_collective_anarchy.md"),
    
    # THE POSITIVE UNION
    (2590, "**The Positive Union** founded \u2014 a political movement promoting cross-faction cooperation and COP reform through diplomacy rather than war",
     "factions/the_positive_union.md"),
    
    # THORNVEIL GROVE
    (2493, "**Thornveil Grove** established as ECOS's pharmaceutical and bioengineering grove \u2014 the \"Alchemist\" on the High Circle",
     "factions/thornveil_grove.md"),
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
new_events = []
for year, text, source in batch24_events:
    basename = source.replace("factions/", "").replace(".md", "")
    year_str = f"~{year}"
    
    already = False
    for line in lines:
        if year_str in line and basename.replace("_", " ") in line.lower():
            already = True
            break
        # Also check for key terms from the event text
        first_bold = re.search(r"\*\*(.+?)\*\*", text)
        if first_bold and year_str in line and first_bold.group(1).lower() in line.lower():
            already = True
            break
    
    if not already:
        new_events.append((year, text, source))

print(f"Events to add: {len(new_events)} (filtered from {len(batch24_events)})")

# ── Insert events in chronological order ──────────────────────────────
def find_insert_point(year, lines, max_idx):
    best = None
    for i in range(max_idx):
        m = re.match(r"^- \*\*~?(\d{4})\*\*:", lines[i])
        pm = re.match(r"^- \*\*Pre-~(\d{4})\*\*:", lines[i])
        if m:
            ly = int(m.group(1))
            if ly <= year:
                if i + 1 < len(lines) and lines[i+1].strip().startswith("- " + "\U0001f4c1"):
                    best = i + 2
                elif i + 1 < len(lines) and lines[i+1].strip().startswith("  - " + "\U0001f4c1"):
                    best = i + 2
                else:
                    best = i + 1
        elif pm:
            ly = int(pm.group(1))
            if ly <= year:
                if i + 1 < len(lines) and ("\U0001f4c1" in lines[i+1]):
                    best = i + 2
                else:
                    best = i + 1
    return best

new_events.sort(key=lambda x: x[0])
inserted = 0
for year, text, source in new_events:
    idx = find_insert_point(year, lines, undated_idx + inserted)
    if idx is None:
        print(f"  WARNING: No insertion point for ~{year}: {text[:50]}")
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

evts = sum(1 for l in lines if re.match(r"^- \*\*[~P]", l))
print(f"\nTotal events now: {evts}")
print(f"Total lines: {len(lines)}")
