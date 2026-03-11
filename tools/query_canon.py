"""
Star Atlas Canon Query Tool
Semantic search over canon lore stored in Qdrant.
Usage: python query_canon.py "What are the Sogmian noble houses?"
"""

import sys
import atexit
from pathlib import Path
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Configuration
QDRANT_PATH = Path(r"C:\Users\jose_\.openclaw\workspace\star-atlas-lore\.qdrant_data")
COLLECTION_NAME = "star_atlas_canon"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5

# Lazy globals
_client = None
_model = None


def _cleanup():
    global _client
    if _client is not None:
        try:
            _client.close()
        except Exception:
            pass
        _client = None


atexit.register(_cleanup)


def get_client():
    global _client
    if _client is None:
        _client = QdrantClient(path=str(QDRANT_PATH))
    return _client


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def query(question: str, top_k: int = TOP_K, show_raw: bool = False) -> list[dict]:
    """Query the canon vector store and return top-K results."""
    client = get_client()
    model = get_model()
    
    # Embed query
    query_vector = model.encode(question).tolist()
    
    # Search
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    ).points
    
    output = []
    for r in results:
        output.append({
            "score": r.score,
            "file": r.payload["file"],
            "section": r.payload["section"],
            "text": r.payload["raw"] if show_raw else r.payload["text"],
        })
    
    return output


def print_results(question: str, results: list[dict]):
    """Pretty-print query results."""
    print(f"\n🔍 Query: \"{question}\"")
    print("=" * 70)
    
    for i, r in enumerate(results, 1):
        score_bar = "█" * int(r["score"] * 20)
        print(f"\n📄 [{i}] {r['file']} → {r['section']}")
        print(f"   Score: {r['score']:.4f} {score_bar}")
        print(f"   ---")
        # Truncate long text for display
        text = r["text"]
        if len(text) > 500:
            text = text[:500] + "..."
        for line in text.split("\n"):
            print(f"   {line}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query_canon.py \"your question here\"")
        print("\nOptions:")
        print("  --raw     Show original markdown instead of clean text")
        print("  --top N   Return top N results (default: 5)")
        sys.exit(1)
    
    # Parse args
    args = sys.argv[1:]
    show_raw = "--raw" in args
    top_k = TOP_K
    
    if "--top" in args:
        idx = args.index("--top")
        top_k = int(args[idx + 1])
        args = [a for i, a in enumerate(args) if i != idx and i != idx + 1]
    
    args = [a for a in args if a != "--raw"]
    question = " ".join(args)
    
    results = query(question, top_k=top_k, show_raw=show_raw)
    print_results(question, results)
