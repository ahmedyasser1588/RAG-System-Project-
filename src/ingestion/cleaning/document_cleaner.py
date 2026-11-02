from langchain_core.documents import Document
from src.ingestion.cleaning.pipeline import clean_text


def clean_document(doc: Document) -> Document:
    cleaned_content = clean_text(doc.page_content)
    return Document(
        page_content=cleaned_content,
        metadata=doc.metadata.copy(),
    )


def clean_documents(docs: list[Document]) -> list[Document]:
    return [clean_document(doc) for doc in docs]
