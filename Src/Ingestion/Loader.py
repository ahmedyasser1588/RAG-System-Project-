from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
)
from Src.Config.Settings import settings


def load_documents(path: str | None = None) -> list:
    """Load all supported documents (TXT, PDF, MD) from the data directory."""
    target = path if path is not None else str(settings.data_directory)
    docs = []

    txt_loader = DirectoryLoader(
        target,
        loader_cls=TextLoader,
        glob="**/*.txt",
        show_progress=True,
        loader_kwargs={"encoding": "utf-8"},
    )

    pdf_loader = DirectoryLoader(
        str(settings.data_directory),
        loader_cls=PyPDFLoader,
        glob="**/*.pdf",
        show_progress=True,
    )

    md_loader = DirectoryLoader(
        str(settings.data_directory),
        loader_cls=TextLoader,
        glob="**/*.md",
        show_progress=True,
    )

    docs.extend(txt_loader.load())
    docs.extend(pdf_loader.load())
    docs.extend(md_loader.load())

    return docs
