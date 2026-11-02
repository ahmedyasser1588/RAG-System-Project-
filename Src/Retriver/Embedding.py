# pyrefly: ignore [missing-import]
from langchain_huggingface import HuggingFaceEmbeddings
from Src.Config.Settings import settings


def get_embedding() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.model_of_embedding)
