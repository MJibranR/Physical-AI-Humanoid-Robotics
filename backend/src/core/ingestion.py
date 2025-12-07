import sys
import os
# Add backend/src to sys.path for direct execution to resolve relative imports
# This is a workaround for direct script execution and generally not recommended for modules.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from typing import List, Dict, Any

# Assuming these are available in the same core directory
from .embedding_model import EmbeddingModel
from .qdrant_client import QdrantStore

def read_markdown_files(docs_path: str) -> List[str]:
    """
    Reads all markdown files from the specified path and returns their content.
    """
    markdown_contents = []
    for root, _, files in os.walk(docs_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    markdown_contents.append(f.read())
    return markdown_contents

def simple_chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Splits text into chunks of a given size with optional overlap.
    A more sophisticated solution would use a proper text splitter library.
    """
    chunks = []
    words = text.split()
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap # Move window by chunk_size - overlap
        if i >= len(words) and overlap > 0: # Handle last chunk overlap for very short texts
            break
    return chunks

def ingest_book_content(docs_base_path: str, qdrant_host: str = "localhost", qdrant_port: int = 6333, qdrant_api_key: str = None):
    """
    Orchestrates reading, chunking, embedding, and uploading book content to Qdrant.
    """
    print(f"Starting ingestion process from {docs_base_path}...")
    
    # 1. Read markdown files
    all_raw_docs = []
    for root, _, files in os.walk(docs_base_path):
        for file_name in files:
            if file_name.endswith(".md") or file_name.endswith(".mdx"):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    all_raw_docs.append({"content": f.read(), "source": file_name})
    
    print(f"Read {len(all_raw_docs)} raw documents.")

    if not all_raw_docs:
        print("No documents found to ingest. Exiting ingestion.")
        return

    # 2. Chunk text
    all_chunks = []
    all_chunk_metadatas = []
    for doc in all_raw_docs:
        chunks = simple_chunk_text(doc["content"])
        for chunk in chunks:
            all_chunks.append(chunk)
            all_chunk_metadatas.append({"source_file": doc["source"]})
    
    print(f"Generated {len(all_chunks)} chunks.")

    # 3. Generate embeddings
    embedding_model = EmbeddingModel()
    embeddings = embedding_model.get_embeddings(all_chunks)
    print(f"Generated {len(embeddings)} embeddings.")

    # 4. Upload to Qdrant
    qdrant_store = QdrantStore(host=qdrant_host, port=qdrant_port, api_key=qdrant_api_key)
    qdrant_store.upsert_vectors(all_chunks, embeddings, all_chunk_metadatas)
    print("Ingestion process completed.")

if __name__ == "__main__":
    # Example usage
    docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "my-website", "docs"))
    
    # Ensure Qdrant is running or accessible
    qdrant_host = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    ingest_book_content(docs_path, qdrant_host=qdrant_host, qdrant_port=qdrant_port, qdrant_api_key=qdrant_api_key)
