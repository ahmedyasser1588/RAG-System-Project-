# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma
from src.retriever.embedding import get_embedding
from src.config.settings import settings


def create_vector_store(chunks: list) -> Chroma:
    """Create and persist a ChromaDB vector store from document chunks."""
    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding(),
        persist_directory=str(settings.vector_store_directory),
        collection_name=settings.collection_name,
    )
