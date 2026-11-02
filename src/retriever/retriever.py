from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever

try:
    from langchain.retrievers import EnsembleRetriever
except ImportError:
    try:
        from langchain.retrievers.ensemble import EnsembleRetriever
    except ImportError:
        from langchain_core.retrievers import BaseRetriever
        from langchain_core.callbacks import CallbackManagerForRetrieverRun
        from langchain_core.documents import Document

        class EnsembleRetriever(BaseRetriever):  # type: ignore
            retrievers: list
            weights: list[float]

            def _get_relevant_documents(
                self,
                query: str,
                *,
                run_manager: CallbackManagerForRetrieverRun | None = None,
            ) -> list[Document]:
                combined = []
                seen = set()
                for retriever in self.retrievers:
                    try:
                        docs = retriever.invoke(query)
                        for doc in docs:
                            if doc.page_content not in seen:
                                seen.add(doc.page_content)
                                combined.append(doc)
                    except Exception:
                        continue
                return combined

from src.config.settings import settings
from src.retriever.embedding import get_embedding
from src.ingestion.loader import load_documents
from src.ingestion.chunker import chunk_documents


def get_vector_store() -> Chroma:
    return Chroma(
        persist_directory=str(settings.vector_store_directory),
        collection_name=settings.collection_name,
        embedding_function=get_embedding(),
    )


def get_similarity_retriever(top_k: int | None = None):
    vector_db = get_vector_store()
    return vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k if top_k is not None else settings.top_k},
    )


def get_mmr_retriever(lambda_mult: float = 0.5):
    vector_db = get_vector_store()
    return vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": settings.top_k,
            "lambda_mult": lambda_mult,
        },
    )


def get_keyword_retriever():
    docs = load_documents()
    chunks = chunk_documents(docs)
    return BM25Retriever.from_documents(chunks)


def get_hybrid_retriever(alpha: float = 0.5):
    try:
        keyword_retriever = get_keyword_retriever()
        similarity_retriever = get_similarity_retriever()
        return EnsembleRetriever(
            retrievers=[keyword_retriever, similarity_retriever],
            weights=[1 - alpha, alpha],
        )
    except Exception:
        return get_similarity_retriever()


def get_retriever(retriever_type: str = "similarity"):
    retriever_type = retriever_type.strip().lower()

    if retriever_type == "similarity":
        return get_similarity_retriever()
    elif retriever_type == "hybrid":
        return get_hybrid_retriever()
    elif retriever_type == "mmr":
        return get_mmr_retriever()
    else:
        raise ValueError(
            "Unknown retriever type. Please choose from: [similarity, mmr, hybrid]"
        )
