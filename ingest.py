"""
Ingestion Script — يُشغَّل مرة واحدة لبناء الـ Vector DB

الاستخدام:
    python ingest.py
"""

from Src.Ingestion.Loader import load_documents
from Src.Ingestion.Chunker import chunk_documents
from Src.Retriver.Vector_Store import create_vector_store
from Src.Config.Settings import settings


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
