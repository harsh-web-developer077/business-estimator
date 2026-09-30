from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API
    api_title: str = "Business Estimator API"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    environment: str = "development"
    secret_key: str = "your-secret-key"

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost/business_estimator_db"
    db_pool_size: int = 20
    db_max_overflow: int = 10

    # AI / Claude
    claude_api_key: str = ""
    claude_model: str = "claude-3-5-sonnet-20241022"

    # CORS
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost"]

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
