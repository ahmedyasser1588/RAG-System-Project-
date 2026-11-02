import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# If running on Streamlit Cloud, inject st.secrets into os.environ if present
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        for key, value in st.secrets.items():
            if isinstance(value, str) and key not in os.environ:
                os.environ[key] = value
except Exception:
    pass


class Settings(BaseSettings):
    llm_api_key: str = ""
    llm_model_name: str = "llama-3.3-70b-versatile"

    LANGSMITH_TRACING: str = ""
    LANGSMITH_ENDPOINT: str = ""
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_AGENT_ID: str = ""
    LANGSMITH_AGENT_ENVIRONMENT: str = ""

    chunk_size: int = 100
    chunk_overlap: int = 10
    data_directory: Path = BASE_DIR / "Data"
    model_of_embedding: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_store_directory: Path = BASE_DIR / "Data" / "Vector_DB"
    collection_name: str = "Knowledge"
    top_k: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
