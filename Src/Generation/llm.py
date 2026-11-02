from langchain_groq import ChatGroq
from Src.Config.Settings import settings

def get_llm():
    return ChatGroq(
        api_key=settings.llm_api_key,
        model=settings.llm_model_name
    )