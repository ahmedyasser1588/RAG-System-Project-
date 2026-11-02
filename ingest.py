"""
Ingestion Script — builds and populates the ChromaDB vector store.

Usage:
    python ingest.py
"""

from src.ingestion.loader import load_documents
from src.ingestion.chunker import chunk_documents
from src.retriever.vector_store import create_vector_store
from src.config.settings import settings


def run_ingestion():
    print("📂 Loading documents...")
    docs = load_documents()
    print(f"   Loaded {len(docs)} documents.")

    print("✂️  Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"   Created {len(chunks)} chunks.")

    print("🗄️  Building Vector Store...")
    create_vector_store(chunks)
    print(f"   Vector Store saved to: {settings.vector_store_directory}")

    print("✅ Ingestion complete!")


if __name__ == "__main__":
    run_ingestion()
