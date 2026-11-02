from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# BASE_DIR = مجلد المشروع الرئيسي (يعمل على أي جهاز تلقائياً)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    llm_api_key: str
    llm_model_name: str

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
