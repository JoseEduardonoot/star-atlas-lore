"""Rewrite the undated events section with all user corrections applied."""
import os

canon_dir = r"c:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon"
path = os.path.join(canon_dir, "meta", "master_timeline.md")

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the Undated Events section
insert_idx = None
for i, line in enumerate(lines):
    if "Undated Events" in line and "Pending" in line:
        insert_idx = i
        break

if insert_idx is None:
    print("ERROR: Could not find Undated Events section")
    exit(1)

new_section = """\u0001f4cb Undated Events (Pending Placement)

> The following major events have no confirmed canon date. Each includes a proposed date
> and rationale. Status indicators: \u2705 = user-approved, \u274c = deferred, \u0001f4cb = pending review.

### Batch 1: Post-War Governments & Institutions

| # | Date | Event | Rationale | Status |
|---|:---:|---|---|:---:|
| 1 | **~2523** | Anfoil State formally constituted under Ponel.eldr | Created at the Accord | \u0001f4cb |
| 2 | **~2524** | Xyanyang Government formed as independent state | Broke from MUD ~2522, stabilized with Redam ~2524 | \u0001f4cb |
| 3 | **~2526** | Xianyang Enforcers created as military arm | Military formalization after independence | \u0001f4cb |
| 4 | **~2530** | Gate Garrison formally organized | Awakened Tufa stayed behind ~2525, grew over ~5yr | \u0001f4cb |
| 5 | **~2532** | Ustur Regency established in Pavo Passage | Ponel.eldr left Elder Order ~2532 | \u0001f4cb |
| 6 | **~2538** | Abyd Government first provisional state | Abyd-IX civil war ~2538 per eras doc | \u0001f4cb |

### Batch 2: Pavo Passage Organizations (Civil War Era ~2565\u20132586)

| # | Date | Event | Rationale | Status |
|---|:---:|---|---|:---:|
| 7 | **~2560** | TAPP (Toll Authority of Pavo Passage) operational | Infrastructure predates civil war; formalized as power grew | \u0001f4cb |
| 8 | **~2586** | Ruling Conclave established | Created immediately after Pavo civil war ends ~2586 | \u2705 |
| 9 | **~2587** | Meridian Trading Company (MTC) enters Pavo | MUD/Synod front; established after Conclave stabilized | \u0001f4cb |
| 10 | **~2588** | Vale Horizon Exchange (VHE) founded by Seraphine Vale | Counter-MTC balance; formed after MTC presence | \u0001f4cb |

### Batch 3: Specialist Organizations

| # | Date | Event | Rationale | Status |
|---|:---:|---|---|:---:|
| 11 | **~2525** | Nimrod Trackers DAC founded in Communion | Early Golden Era; monster hunters (NOT bounty hunters) | \u0001f4cb |
| 12 | **~2545** | Iris Academy formally opens at Zenith Door | Chior.eldr + Exfeheros per `zenith_door.md` | \u0001f4cb |
| 13 | **~2550** | Holpla Insurances Inc founded | Post-war commercial boom, COP Cradle HQ | \u0001f4cb |
| 14 | **~2575** | Winter Fist Path arrives in Pavo with Ustur Regency | Came together with the Ustur Regency presence | \u2705 |

### Batch 4: Ancient / Pre-War Organizations

| # | Date | Event | Rationale | Status |
|---|:---:|---|---|:---:|
| 15 | **Pre-~1461** | Living Factories already active (pre-Primitive Era) | Interacted with humanity when AI started on Earth; already ancient | \u2705 |
| 16 | **Ancient** | Hikibashi \u2014 always existed in Mierese culture | Not a founding event; cultural institution since Mierese origins | \u2705 |
| 17 | **Ancient** | Mierese Lore Keepers \u2014 always existed in Mierese culture | Not a founding event; cultural institution since Mierese origins | \u2705 |
| 18 | **Pre-~2512** | Order of Light established (before Convergence War) | User-confirmed: predates the war | \u2705 |
| 19 | **Pre-~2512** | Heralds of Vignus begin operations (before Convergence War) | User-confirmed: predates the war | \u2705 |
| 20 | **~2515** | Order of Seasons created (Convergence War era) | User-confirmed: during the Convergence War | \u2705 |
| 21 | **~2470** | Panemorfa group formed | A few decades before Denebula Utopia (~2495) | \u2705 |

### Deferred (Need Deep Dive First)

| # | Era Note | Faction | Reason |
|---|:---:|---|---|
| 22 | *Convergence War era* | Umbral Court | Deferred until deep dive \u2014 user noted they are from Convergence War era |
| 23 | *TBD* | The Real Truth Network | Deferred until deep dive |

"""

# Fix the emoji issue - write with proper unicode
new_section = new_section.replace("\u0001f4cb", "\U0001f4cb")

lines_before = lines[:insert_idx]
header = "## \U0001f4cb Undated Events (Pending Placement)\n\n"
remainder = new_section.split("\n", 1)[1]  # skip the first line (header already included)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines_before)
    f.write("## \U0001f4cb Undated Events (Pending Placement)\n\n")
    f.write(remainder)

print("Undated events section rewritten with all corrections")
