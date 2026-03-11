"""
Batch 5-7: Extract and merge events from ALL geography files (sectors + worlds).
"""
import os, re

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
tl_path = os.path.join(canon_dir, "meta", "master_timeline.md")

batch57_events = [
    # CORAL NEBULA
    (2348, "A new fertile sector discovered in ONI space (MRZ-18) \u2014 first explorers find **bioluminescent corals** that respond to sentient presence",
     "geography/sectors/coral_nebula.md"),
    (2399, "The **Rule of 1000** established at Coral Nebula \u2014 settlements exceeding 1000 citizens trigger dangerous flora expansion",
     "geography/sectors/coral_nebula.md"),
    (2433, "The Rule of 1000 broken at Coral Nebula \u2014 settlers flock to the crescent market; corals spread uncontrollably outward",
     "geography/sectors/coral_nebula.md"),
    (2598, "Scientific expeditions arrive at Coral Nebula to study the flora\u2019s behavior and intelligence potential",
     "geography/sectors/coral_nebula.md"),
    
    # DENEBULA UTOPIA
    (2495, "Denebula Sector colonized under Merchant Prince **Ayevat** \u2014 the \"Kingdom of Finance\" begins",
     "geography/sectors/denebula_utopia.md"),
    (2526, "Denebula merchant prince **Gelah** expands trade routes to Safe Zone \u2014 caste system solidifies",
     "geography/sectors/denebula_utopia.md"),
    
    # IZAR (Fallen Civilization)
    (1965, "The **Izar Catastrophe** \u2014 the advanced Izar civilization collapses; only ruins remain across Izar-248 and adjacent sectors",
     "geography/sectors/izar_fallen_civilization.md"),
    
    # IZAR SURVIVORS
    (2005, "Discovery of **Paclets** (underground agriculture organisms) by Izar survivors \u2014 enables long-term subterranean habitation",
     "geography/sectors/izar_survivors.md"),
    (2240, "Izar survivors complete centuries of adaptation \u2014 biology and psychology permanently changed by underground life",
     "geography/sectors/izar_survivors.md"),
    
    # MYCENAS
    (2546, "Virel (Mycenas leader) **destroys/expels all alien invaders** from Mycenas system \u2014 sector becomes isolationist fortress",
     "geography/sectors/mycenas.md"),
    (2553, "Virel constructs system-wide **defensive barrier** around Mycenas \u2014 upgraded planetary shield network",
     "geography/sectors/mycenas.md"),
    
    # OPHEK OASIS
    (2545, "Ophek Revel renames the sector **\"Ophek Oasis\"** \u2014 transforming it into the galaxy's premier pleasure district",
     "geography/sectors/ophek_oasis.md"),
    (2602, "Ophek Oasis becomes the **biggest entertainment sector** in the galaxy \u2014 its reputation draws visitors from all factions",
     "geography/sectors/ophek_oasis.md"),
    
    # SUMMER SEA
    (2557, "The **Relic Barons** install a massive space observatory in Summer Sea \u2014 mapping HRZ border regions",
     "geography/sectors/summer_sea.md"),
    
    # VEGA FALL
    (2450, "**Vega Fall** sector first settled by multi-species pioneers \u2014 becomes a rare example of sustained cross-faction cooperation",
     "geography/sectors/vega_fall.md"),
    
    # AKALMA EXILE
    (2510, "House Akalma expelled from ONI space after being falsely linked to Empress Paizul's assassination \u2014 **Akalma Exile** (MRZ-12) becomes a ghost sector",
     "geography/sectors/akalma_exile.md"),
    
    # KA-DARA
    (1940, "**Ingbus** (Ka-dara ruler) begins researching resurrection \u2014 initially preserving moral principles, but gradually descending into dark experimentation",
     "geography/sectors/ka_dara.md"),
    (2101, "Ingbus begins using **non-intelligent species** in resurrection research at Ka-dara \u2014 moral boundaries start to erode",
     "geography/sectors/ka_dara.md"),
    (2370, "Ingbus begins **kidnapping explorers** who venture into Ka-dara \u2014 using sentient subjects for experiments",
     "geography/sectors/ka_dara.md"),
    
    # NIGHT WINDOW
    (2555, "**Night Window** sector discovered \u2014 a permanently dark region used for covert operations and smuggling routes",
     "geography/sectors/night_window.md"),
    
    # XIANYANG
    (2543, "**Xianyang** institutes mandatory public army service \u2014 every citizen participates in the Rite of Passage military training",
     "geography/sectors/xianyang.md"),
    
    # EVERNAT
    (2100, "An alien traveler transports **TED** (the creature that becomes the Great Evernat) to the sector \u2014 origin of the living ecosystem",
     "geography/sectors/evernat.md"),
    
    # ETIRA (world)
    (2135, "Discovery of **Etira** \u2014 a mysterious world in the Yuldun sector; later becomes the resting place of the Dreamer Below",
     "geography/worlds/etira.md"),
]

# ── Read existing timeline ────────────────────────────────────────────
with open(tl_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

undated_idx = None
for i, line in enumerate(lines):
    if "Undated Events" in line or "Deferred" in line:
        undated_idx = i
        break
if undated_idx is None:
    undated_idx = len(lines) - 1

# ── Filter already-existing ───────────────────────────────────────────
new_events = []
for year, text, source in batch57_events:
    year_str = f"~{year}"
    first_bold = re.search(r"\*\*(.+?)\*\*", text)
    key = first_bold.group(1).lower() if first_bold else ""
    
    already = False
    for line in lines:
        if year_str in line:
            if key and key in line.lower():
                already = True
                break
    
    if not already:
        new_events.append((year, text, source))

print(f"Events to add: {len(new_events)} (filtered from {len(batch57_events)})")

# ── Insert ────────────────────────────────────────────────────────────
def find_insert_point(year, lines, max_idx):
    best = None
    for i in range(max_idx):
        m = re.match(r"^- \*\*~?(\d{4})\*\*:", lines[i])
        pm = re.match(r"^- \*\*Pre-~(\d{4})\*\*:", lines[i])
        if m:
            ly = int(m.group(1))
            if ly <= year:
                if i + 1 < len(lines) and "\U0001f4c1" in lines[i+1]:
                    best = i + 2
                else:
                    best = i + 1
        elif pm:
            ly = int(pm.group(1))
            if ly <= year:
                if i + 1 < len(lines) and "\U0001f4c1" in lines[i+1]:
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

with open(tl_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

evts = sum(1 for l in lines if re.match(r"^- \*\*[~P]", l))
print(f"\nTotal events now: {evts}")
