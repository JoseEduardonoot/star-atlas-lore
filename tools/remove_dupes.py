"""Remove 7 duplicate event pairs from master timeline, keeping the more detailed version."""
import re

path = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon\meta\master_timeline.md"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Duplicates identified by the verification script:
# 1. ~2459: "Production halts across most settlements" vs "Production halts in most settlements" (100% overlap)
# 2. ~2471: Merchant Prince Ayevat long vs short version
# 3. ~2523: The Accord full vs "Council of Peace created; Star Atlas blockchain established"
# 4. ~2533: Frenir collapses long vs short version
# 5. ~2567: Pavo civil war ends vs Ruling Conclave established (merged events)
# 6. ~2620: "Beginning of the Current Age" vs with "— the playable timeline"
# 7. ~2624: COP Frenir liberation long vs short

# Strategy: remove the shorter/less detailed version for each pair
# We'll identify lines to remove by their content

lines_to_remove = set()

for i, line in enumerate(lines):
    text = line.strip()
    
    # Dupe 1: remove shorter ~2459 version
    if "~2459" in text and "Production halts in most settlements" in text:
        lines_to_remove.add(i)
        # Also remove its source line
        if i+1 < len(lines) and lines[i+1].strip().startswith("- "):
            lines_to_remove.add(i+1)
    
    # Dupe 2: remove shorter ~2471 Ayevat version
    if "~2471" in text and "Merchant Prince Ayevat discovers Denebula Sector and founds" in text:
        lines_to_remove.add(i)
        if i+1 < len(lines) and lines[i+1].strip().startswith("- "):
            lines_to_remove.add(i+1)
    
    # Dupe 3: remove shorter ~2523 COP/Star Atlas version
    if "~2523" in text and "Council of Peace created; Star Atlas blockchain established" in text:
        lines_to_remove.add(i)
        if i+1 < len(lines) and lines[i+1].strip().startswith("- "):
            lines_to_remove.add(i+1)
    
    # Dupe 4: remove shorter ~2533 Frenir version (by checking which is shorter)
    if "~2533" in text and "The Frenir government collapses entirely and slavers formally" in text:
        lines_to_remove.add(i)
        if i+1 < len(lines) and lines[i+1].strip().startswith("- "):
            lines_to_remove.add(i+1)
    
    # Dupe 5: remove "Ruling Conclave established in Pavo Passage" (merged entry from Phase 2)
    if "~2567" in text and "Ruling Conclave established in Pavo Passage" in text and "new" in lines[i+1] if i+1 < len(lines) else False:
        lines_to_remove.add(i)
        if i+1 < len(lines) and lines[i+1].strip().startswith("- "):
            lines_to_remove.add(i+1)
    
    # Dupe 6: remove shorter ~2620 version 
    if "~2620" in text and text == "- **~2620**: Beginning of the Current Age":
        lines_to_remove.add(i)
        if i+1 < len(lines) and lines[i+1].strip().startswith("- "):
            lines_to_remove.add(i+1)
    
    # Dupe 7: remove shorter ~2624 COP liberates Frenir
    if "~2624" in text and text.endswith("COP forces liberate Frenir"):
        lines_to_remove.add(i)
        if i+1 < len(lines) and lines[i+1].strip().startswith("- "):
            lines_to_remove.add(i+1)

# Filter out removed lines
new_lines = [lines[i] for i in range(len(lines)) if i not in lines_to_remove]

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

removed = len(lines) - len(new_lines)
print(f"Removed {removed} duplicate lines")
print(f"Lines: {len(lines)} -> {len(new_lines)}")

# Count final events
evts = sum(1 for l in new_lines if re.match(r"^- \*\*[~P]", l))
print(f"Total events now: {evts}")
