from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from Src.Ingestion.chunking.Structure import extract_sections


class StructureAwareChunker:
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_document(self, document: Document) -> list[Document]:
        """Split a single document into chunks respecting Markdown structure."""
        sections = extract_sections(document.page_content)
        chunks: list[Document] = []

        document_title = document.metadata.get("document_title")
        if not document_title and sections:
            first_section = sections[0]
            if first_section.level == 1:
                document_title = first_section.title

        for section_index, section in enumerate(sections):
            metadata = {
                **document.metadata,
                "document_title": document_title,
                "section": section.title,
                "section_level": section.level,
                "section_index": section_index,
                "section_parent": section.parent,
            }

            section_doc = Document(
                page_content=section.content,
                metadata=metadata,
            )

            # Section fits in one chunk
            if len(section.content) <= self.chunk_size:
                chunks.append(section_doc)
                continue

            # Section is too large — split further
            section_chunks = self.splitter.split_documents([section_doc])
            chunks.extend(section_chunks)

        return chunks

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """Split a list of documents into chunks respecting Markdown structure."""
        all_chunks: list[Document] = []
        for document in documents:
            document_chunks = self.split_document(document)
            all_chunks.extend(document_chunks)
        return all_chunks
