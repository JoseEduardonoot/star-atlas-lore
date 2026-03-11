import sys
sys.path.insert(0, r"C:\Users\jose_\.openclaw\workspace\star-atlas-lore")
from tools.query_canon import query

results = query(
    "Mycenas sector Virel the Serene history timeline meritocratic government barrier shield pirate",
    top_k=10,
    show_raw=True
)

with open(r"C:\Users\jose_\.openclaw\workspace\star-atlas-lore\mycenas_qdrant.txt", "w", encoding="utf-8") as f:
    for i, r in enumerate(results, 1):
        score = r["score"]
        file_name = r["file"]
        section = r["section"]
        f.write(f"=== Result {i} | Score: {score:.4f} | {file_name} > {section} ===\n")
        f.write(r["text"] + "\n\n")

print(f"Done - {len(results)} results written")
