"""Append undated events proposal section to master_timeline.md."""
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

new_section = """## \U0001f4cb Undated Events (Pending Placement)

> The following major events have no confirmed canon date. Each includes a proposed date
> and rationale. Events marked \U0001f4cb need user approval before becoming canon.

### Batch 1: Post-War Governments & Institutions (~2523\u20132540)

| # | Proposed Date | Event | Rationale | Source |
|---|:---:|---|---|---|
| 1 | **~2523** | Anfoil State formally constituted under Ponel.eldr | Created at the Accord \u2014 Ponel left Elder Order post-war | `anfoil_state.md` |
| 2 | **~2524** | Xyanyang Government formed as independent state | Broke from MUD ~2522, stabilized alongside Redam | `xyanyang_government.md` |
| 3 | **~2526** | Xianyang Enforcers created as military arm of Xyanyang | Military formalization after independence | `xianyang_enforcers.md` |
| 4 | **~2530** | Gate Garrison formally organized | Awakened Tufa stayed behind ~2525, organization grew over ~5 years | `gate_garrison.md` |
| 5 | **~2532** | Ustur Regency established in Pavo Passage | Ponel.eldr left Elder Order ~2532, created Meritocratic Technate | `ustur_regency_pavo.md` |
| 6 | **~2538** | Abyd Government first provisional state | Abyd civil war ~2538 per eras doc | `abyd_government.md` |

### Batch 2: Specialized Organizations (~2540\u20132580)

| # | Proposed Date | Event | Rationale | Source |
|---|:---:|---|---|---|
| 7 | **~2545** | Iris Academy formally opens at Zenith Door | Chior.eldr + Exfeheros per canon geography doc | `iris_academy.md` |
| 8 | **~2550** | Holpla Insurances Inc founded | Post-war commercial boom, COP infrastructure stabilizing | `holpla_insurances.md` |
| 9 | **~2555** | MTC (Merchant Transport Consortium) established | Post-Starpath era commerce expansion | `mtc.md` |
| 10 | **~2560** | VHE (Vale Horizon Exchange) founded | Trade stabilization mid-Golden Era | `vhe.md` |
| 11 | **~2565** | TAPP (Theater Alliance of Pavo Passage) formed | Pavo civil war ~2565, TAPP likely formed during/after conflict | `tapp.md` |
| 12 | **~2570** | Nimrod Trackers established | Mid-Golden Era bounty hunter guild | `nimrod_trackers.md` |
| 13 | **~2570** | Living Factories begin operations | Industrial expansion mid-Golden Era | `living_factories.md` |

### Batch 3: Religious, Cultural & Covert Organizations

| # | Proposed Date | Event | Rationale | Source |
|---|:---:|---|---|---|
| 14 | **~2540** | Hikibashi order formalized | Ancient Mierese tradition, formalized as organization post-war | `hikibashi.md` |
| 15 | **~2555** | Mierese Lore Keepers organized | Cultural preservation during Scriptorium reorganization era | `mierese_lore_keepers.md` |
| 16 | **~2560** | Order of Light established | Religious organization, mid-Golden Era | `order_of_light.md` |
| 17 | **~2570** | Heralds of Vignus begin operations | Itinerant oracles, likely emerged mid-Golden Era | `heralds_of_vignus.md` |
| 18 | **~2575** | Winter Fist Path sect formed in Pavo Passage | Ustur martial sect, after Ustur regency established | `winter_fist_path.md` |

### Batch 4: Criminal & Shadow Organizations

| # | Proposed Date | Event | Rationale | Source |
|---|:---:|---|---|---|
| 19 | **~2555** | The Real Truth Network begins broadcasting | Counter-establishment media, mid-Golden Era | `the_real_truth_network.md` |
| 20 | **~2565** | Umbral Court established | Shadow organization, emerged during Pavo civil war era | `umbral_court.md` |
| 21 | **~2580** | Panemorfa group formed | Late Golden Era covert faction | `panemorfa.md` |

### Batch 5: Already-Dated (Need Placement Only)

| # | Existing Date | Event | Notes | Source |
|---|:---:|---|---|---|
| 22 | **~2521** | Order of Seasons contracted by Pavo royals | Already in `pavo_passage.md` ~2521 | `order_of_seasons.md` |
| 23 | **~2586** | Ruling Conclave formally established | Already in eras: Pavo civil war ends ~2586 | `ruling_conclave.md` |
| 24 | **~2524** | Redam Government (Five Leaders) | Already in timeline ~2524 | `redam_government.md` |

"""

lines = lines[:insert_idx] + [new_section]
with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Undated events section written successfully")
print(f"Total lines now: {len(lines)}")
