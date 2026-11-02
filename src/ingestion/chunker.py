from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config.settings import settings


def chunk_documents(docs: list) -> list:
    """Split documents into chunks using RecursiveCharacterTextSplitter."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(docs)
    return chunks
