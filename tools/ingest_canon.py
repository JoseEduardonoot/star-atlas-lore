"""
Star Atlas Canon Ingestion Pipeline
Reads all .md files from the canon directory, chunks by section,
generates embeddings, and stores in Qdrant local storage.
"""

import os
import re
import sys
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# Configuration
CANON_DIR = Path(r"C:\Users\jose_\.openclaw\workspace\star-atlas-lore\canon")
QDRANT_PATH = Path(r"C:\Users\jose_\.openclaw\workspace\star-atlas-lore\.qdrant_data")
COLLECTION_NAME = "star_atlas_canon"
MODEL_NAME = "all-MiniLM-L6-v2"  # Fast, 384-dim, good for semantic search
CHUNK_MIN_LENGTH = 50  # Skip chunks shorter than this


def chunk_markdown(filepath: Path) -> list[dict]:
    """Split a markdown file into chunks by ## headers."""
    text = filepath.read_text(encoding="utf-8")
    
    # Get relative path for metadata
    rel_path = filepath.relative_to(CANON_DIR)
    
    # Split by ## headers (keep the header with its content)
    sections = re.split(r'(?=^## )', text, flags=re.MULTILINE)
    
    chunks = []
    for section in sections:
        section = section.strip()
        if len(section) < CHUNK_MIN_LENGTH:
            continue
        
        # Extract section title if present
        title_match = re.match(r'^##\s+(.+?)$', section, re.MULTILINE)
        section_title = title_match.group(1).strip() if title_match else "Overview"
        
        # Clean up markdown artifacts for better embeddings
        clean_text = re.sub(r'[#*`\-|]', ' ', section)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        chunks.append({
            "file": str(rel_path),
            "section": section_title,
            "text": clean_text,
            "raw": section,  # Keep original markdown
            "file_category": str(rel_path.parent),
        })
    
    return chunks


def ingest():
    """Main ingestion pipeline."""
    print(f"🔍 Scanning canon directory: {CANON_DIR}")
    
    # Collect all markdown files
    md_files = sorted(CANON_DIR.rglob("*.md"))
    print(f"📄 Found {len(md_files)} canon files")
    
    # Chunk all files
    all_chunks = []
    for f in md_files:
        chunks = chunk_markdown(f)
        all_chunks.extend(chunks)
        print(f"  ✅ {f.relative_to(CANON_DIR)}: {len(chunks)} chunks")
    
    print(f"\n📦 Total chunks: {len(all_chunks)}")
    
    # Load embedding model
    print(f"\n🧠 Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    
    # Generate embeddings
    print("⚡ Generating embeddings...")
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    vector_size = embeddings.shape[1]
    print(f"✅ Generated {len(embeddings)} embeddings (dim={vector_size})")
    
    # Initialize Qdrant
    QDRANT_PATH.mkdir(parents=True, exist_ok=True)
    client = QdrantClient(path=str(QDRANT_PATH))
    
    # Recreate collection
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
    
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )
    
    # Upload points
    points = [
        PointStruct(
            id=i,
            vector=embeddings[i].tolist(),
            payload={
                "file": all_chunks[i]["file"],
                "section": all_chunks[i]["section"],
                "text": all_chunks[i]["text"],
                "raw": all_chunks[i]["raw"],
                "category": all_chunks[i]["file_category"],
            },
        )
        for i in range(len(all_chunks))
    ]
    
    # Upload in batches
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)
    
    print(f"\n✅ Ingested {len(points)} chunks into Qdrant collection '{COLLECTION_NAME}'")
    print(f"📁 Storage: {QDRANT_PATH}")
    
    # Summary
    info = client.get_collection(COLLECTION_NAME)
    print(f"📊 Collection stats: {info.points_count} points")


if __name__ == "__main__":
    ingest()
