"""Scan species, history, institutions, narratives for events not in timeline."""
import os, re

canon = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
with open(os.path.join(canon, "meta", "master_timeline.md"), "r", encoding="utf-8") as f:
    tl = f.read()

dirs_to_scan = [
    ("species", os.path.join(canon, "species")),
    ("history", os.path.join(canon, "history")),
    ("institutions", os.path.join(canon, "institutions")),
    ("narratives", os.path.join(canon, "narratives")),
    ("cosmology", os.path.join(canon, "cosmology")),
]

for label, dpath in dirs_to_scan:
    if not os.path.isdir(dpath):
        continue
    for f in sorted(os.listdir(dpath)):
        if not f.endswith(".md"):
            continue
        path = os.path.join(dpath, f)
        if os.path.isdir(path):
            continue
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        
        events = []
        for line in content.split("\n"):
            s = line.strip()
            m = re.match(r"^- \*\*~(\d{4})\*\*:\s*(.+)", s)
            if m:
                events.append((int(m.group(1)), m.group(2).strip()[:120]))
        
        basename = f.replace(".md", "")
        in_tl = basename in tl
        dates = sorted(set(int(d) for d in re.findall(r"~(\d{4})", content)))
        
        if events or dates:
            marker = "[TL]" if in_tl else "[NEW]"
            print(f"{marker} {label}/{f} dates={dates}")
            for yr, txt in events:
                # Check if this specific event is already in timeline
                in_event = "~" + str(yr) in tl and any(w in tl for w in txt.split("**")[1:2] if w)
                flag = " [EXISTING]" if in_event else ""
                print(f"  ~{yr}: {txt}{flag}")
            print()
