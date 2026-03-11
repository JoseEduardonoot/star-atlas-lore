"""Find all faction files with no dates and extract key info for date proposals."""
import re, os

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
faction_dir = os.path.join(canon_dir, "factions")

results = []
for f in sorted(os.listdir(faction_dir)):
    if not f.endswith(".md"):
        continue
    path = os.path.join(faction_dir, f)
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
    
    dates = re.findall(r"~\d{4}", content)
    if dates:
        continue  # skip files that already have dates
    
    # Get name
    name_match = re.search(r"^#.*?:\s*(.+)", content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else f
    
    # Get zone
    zone_match = re.search(r"\*\*Zone\*\*:\s*(.+)", content)
    zone = zone_match.group(1).strip() if zone_match else "Unknown"
    
    # Get type
    type_match = re.search(r"\*\*Type\*\*:\s*(.+)", content)
    ftype = type_match.group(1).strip() if type_match else "Unknown"
    
    # Get leader
    leader_match = re.search(r"\*\*Leader\*\*:\s*(.+)", content)
    leader = leader_match.group(1).strip() if leader_match else "Unknown"
    
    # File size
    size = len(content)
    
    results.append({
        "file": f,
        "name": name,
        "zone": zone,
        "type": ftype,
        "leader": leader,
        "size": size,
    })

print(f"Factions with NO dates: {len(results)}\n")
for r in results:
    print(f"  {r['file']}")
    print(f"    Name: {r['name']}")
    print(f"    Zone: {r['zone']}")
    print(f"    Type: {r['type']}")
    print(f"    Size: {r['size']} bytes")
    print()
