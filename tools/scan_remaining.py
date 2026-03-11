"""Scan all remaining faction files and extract dated events."""
import os, re

canon = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
factions_dir = os.path.join(canon, "factions")

# Read the timeline to know what's already there
with open(os.path.join(canon, "meta", "master_timeline.md"), "r", encoding="utf-8") as f:
    tl = f.read()

# Files already processed in batch 1 or already extensively in timeline
skip = {
    # Batch 1
    "ashroot_grove.md", "balifa_grove.md", "crumon_dynasty.md", 
    "dark_photoli.md", "deepwell_grove.md", "exile_scavengers.md",
    # Already in timeline (Phase 1-2)
    "ecos.md", "house_akalma.md", "house_outro.md", "house_patrah.md", 
    "jorvik.md", "ka_dara.md", "church_of_the_dreamer_below.md", "bmah.md",
    "slavers_of_frenir.md", "pergamos_new_government.md", "frenir_new_government.md",
    "anfoil_state.md", "xyanyang_government.md", "xianyang_enforcers.md",
    "gate_garrison.md", "ustur_regency_pavo.md", "abyd_government.md",
    "iris_academy.md", "holpla_insurances.md", "nimrod_trackers.md",
    "mtc.md", "vhe.md", "tapp.md", "ruling_conclave.md", "panemorfa.md",
    "order_of_seasons.md", "living_factories.md", "barrot_entertainment_company.md",
    "fimbul_industries.md", "bluevael_mining_colonies.md", "coral_dwellers.md",
    "relic_barons.md", "ophek.md", "duskbloom_grove.md", "kamec_democracy.md",
}

remaining = []
for f in sorted(os.listdir(factions_dir)):
    if not f.endswith(".md") or f in skip:
        continue
    path = os.path.join(factions_dir, f)
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
    
    dates = sorted(set(int(d) for d in re.findall(r"~(\d{4})", content)))
    
    # Extract events with dates
    events = []
    lines_list = content.split("\n")
    for i, line in enumerate(lines_list):
        m = re.match(r"^- \*\*~(\d{4})\*\*:\s*(.+)", line.strip())
        hm = re.match(r"^### .+\(~(\d{4})", line.strip())
        if m:
            events.append((int(m.group(1)), m.group(2).strip()[:120]))
        elif hm:
            # Get rest of header text
            events.append((int(hm.group(1)), line.strip()[:120]))
    
    basename = f.replace(".md", "")
    in_tl = basename in tl
    
    print(f"{'[TL]' if in_tl else '[NEW]'} {f} dates={dates}")
    for yr, txt in events:
        print(f"  ~{yr}: {txt}")
    if not events and dates:
        print(f"  (dates found but not in event format)")
    if not dates:
        print(f"  (NO dates — needs context-based dating)")
    print()

    remaining.append(f)

print(f"\nTotal remaining: {len(remaining)} files")
