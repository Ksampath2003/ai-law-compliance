from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ai_law_compliance"

    # LLM
    ANTHROPIC_API_KEY: str

    # Vector Store
    USE_LOCAL_VECTOR_DB: bool = True
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-east-1-aws"
    PINECONE_INDEX: str = "ai-laws"
    CHROMA_DB_PATH: str = "./chroma_db"

    # Security
    SECRET_KEY: str = "dev-secret"
    ADMIN_API_KEY: str = "dev-admin-key"
    API_KEY_HEADER: str = "X-API-Key"

    # App
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
