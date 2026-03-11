"""
Batch 8-10: Extract and merge events from species, history, institutions, narratives.
"""
import os, re

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
tl_path = os.path.join(canon_dir, "meta", "master_timeline.md")

batch810_events = [
    # SPECIES: USTUR
    (2383, "**Armi.eldr** born \u2014 future faction leader who trains Chior and Ponel; leads Ustur during the Convergence War",
     "species/ustur.md"),
    (2391, "**Chior.eldr** and **Ponel.eldr** born \u2014 twin pupils of Armi.eldr who will shape post-war Ustur politics",
     "species/ustur.md"),
    (2551, "**Vzus Tenet** construction completed \u2014 a Titan-class Ustur warship stored at Doers Harbor; built using materials from across Galia",
     "species/ustur.md"),
    (2557, "**Eolus.tcher** formally establishes Garadar DAC as a recognized multi-species entity \u2014 the DAC becomes the MRZ's most successful cooperative community",
     "species/ustur.md"),
    
    # SPECIES: HUMAN
    (2480, "**Charon Gotti Jr.** born \u2014 heir to the MUD leadership; will lead MUD during the current era and Book I conflict",
     "species/human.md"),
    (2417, "**Pearce** born on Amora-IV \u2014 future MUD military leader and namesake of the Pearce Council",
     "species/human.md"),
    (2557, "**Pearce** retires from active command \u2014 the Pearce Council established in his honor to oversee MUD military policy",
     "species/human.md"),
    
    # SPECIES: PHOTOLI
    (2080, "**Om** (Photoli elder) fights a Dark Photoli in his youth \u2014 nearly killed; nursed by the Lumikir of Ka-dara, beginning the Photoli-Lumikir bond",
     "species/photoli.md"),
    (2569, "**Om** uplifts the Lumikir species \u2014 awakening their sapient potential; they begin building the Scriptorium into an interstellar knowledge institution",
     "species/photoli.md"),
    
    # INSTITUTIONS: COUNCIL OF PEACE
    (2527, "COP expands operations \u2014 establishes peacekeeping protocols and MRZ patrol routes to prevent another Convergence War",
     "institutions/council_of_peace.md"),
    (2617, "COP establishes the **Safe Zone** enforcement framework \u2014 formal boundaries and patrol routes for the Safe Zone perimeter",
     "institutions/council_of_peace.md"),
    
    # NARRATIVES: NEVER ALONE
    (2620, "The **Jorvik Fleet** starts harassing Safe Zone territories \u2014 testing COP defenses; a bold escalation beyond traditional piracy",
     "narratives/never_alone_campaign.md"),
    
    # SPECIES: SOGMIAN (additional)
    (1461, "Sogmian civilization first emerges \u2014 earliest recorded presence of the Sogmian species in documented galactic history",
     "species/sogmian.md"),
    
    # COSMOLOGY: THE CATACLYSM
    (2510, "The **Cataclysm** begins \u2014 Iris (the sentient planet) starts generating anomalous cosmic events that affect surrounding space",
     "geography/the_cataclysm.md"),
    (2522, "**Iris conceals itself** and the Cataclysm region \u2014 no one can enter or exit; the region becomes impenetrable",
     "geography/the_cataclysm.md"),
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

# ── Filter ────────────────────────────────────────────────────────────
new_events = []
for year, text, source in batch810_events:
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

print(f"Events to add: {len(new_events)} (filtered from {len(batch810_events)})")

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
