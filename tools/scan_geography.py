"""Scan all geography files for events not yet in timeline."""
import os, re

canon = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"

# Read timeline
with open(os.path.join(canon, "meta", "master_timeline.md"), "r", encoding="utf-8") as f:
    tl = f.read()

# Geography files already extensively in timeline
skip = {
    "old_grove.md", "hanging_gardens.md", "pavo_passage.md", "frenir.md",
    "barrot_gateway.md", "bluvael.md", "harkend.md", "glowhaven.md",
    "ilidae.md", "yuldun_waste.md", "abyd_ix.md", "everstorm.md",
}

geo_dirs = [
    os.path.join(canon, "geography", "sectors"),
    os.path.join(canon, "geography", "worlds"),
    os.path.join(canon, "geography"),
]

for gdir in geo_dirs:
    if not os.path.isdir(gdir):
        continue
    for f in sorted(os.listdir(gdir)):
        if not f.endswith(".md") or f in skip:
            continue
        path = os.path.join(gdir, f)
        if os.path.isdir(path):
            continue
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        
        # Extract events
        events = []
        for line in content.split("\n"):
            stripped = line.strip()
            m = re.match(r"^- \*\*~(\d{4})\*\*:\s*(.+)", stripped)
            hm = re.match(r"^##+ .+\(~(\d{4})", stripped)
            if m:
                events.append((int(m.group(1)), m.group(2).strip()[:120]))
            elif hm:
                events.append((int(hm.group(1)), stripped[:120]))
        
        basename = f.replace(".md", "")
        rel = os.path.relpath(path, canon).replace(os.sep, "/")
        in_tl = basename in tl
        dates = sorted(set(int(d) for d in re.findall(r"~(\d{4})", content)))
        
        if events or dates:
            marker = "[TL]" if in_tl else "[NEW]"
            print(f"{marker} {rel} dates={dates}")
            for yr, txt in events:
                print(f"  ~{yr}: {txt}")
            print()
