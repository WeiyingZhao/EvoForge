"""
Core configuration for EvoForge backend.
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False
    PROJECT_NAME: str = "EvoForge"
    VERSION: str = "0.1.0"

    # Database
    DATABASE_URL: str = "sqlite:///./evoforge.db"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Ray Configuration
    RAY_ADDRESS: str = "auto"
    RAY_NUM_CPUS: int = 8
    RAY_NUM_GPUS: int = 0

    # LLM API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Evolution Settings
    MAX_GENERATIONS: int = 100
    POPULATION_SIZE: int = 50
    MUTATION_RATE: float = 0.3

    # Sandbox Settings
    SANDBOX_TIMEOUT: int = 30
    SANDBOX_MEMORY_LIMIT: str = "512m"
    SANDBOX_NETWORK_ENABLED: bool = False

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
