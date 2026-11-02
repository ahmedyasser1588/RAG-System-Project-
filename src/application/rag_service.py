from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable

from src.generation.llm import get_llm
from src.generation.prompt import get_rag_prompt
from src.retriever.retriever import (
    get_similarity_retriever,
    get_mmr_retriever,
    get_hybrid_retriever,
)


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


class RAGService:
    def __init__(self, model_name: str | None = None):
        self.prompt = get_rag_prompt()
        self.llm = get_llm(model_name=model_name)

    def get_retrieved(self, question: str, retriever_type: str) -> list:
        retriever = get_retriever(retriever_type=retriever_type)
        return retriever.invoke(question)

    def generate(self, question: str, documents: list) -> str:
        prompt_value = self.prompt.invoke({
            "context": documents,
            "question": question,
        })
        response = self.llm.invoke(prompt_value)
        return StrOutputParser().invoke(response)

    @traceable
    def ask(self, question: str, retriever_type: str = "similarity") -> dict:
        documents = self.get_retrieved(question, retriever_type)

        answer = self.generate(
            question=question,
            documents=documents,
        )

        sources = [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
            }
            for doc in documents
        ]

        return {
            "answer": answer,
            "sources": sources,
        }
