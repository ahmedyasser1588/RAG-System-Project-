from langchain_groq import ChatGroq
from src.config.settings import settings


def get_llm(model_name: str | None = None):
    return ChatGroq(
        api_key=settings.llm_api_key,
        model=model_name or settings.llm_model_name,
    )
