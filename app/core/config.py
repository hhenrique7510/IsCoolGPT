from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    api_title: str = "IsCoolGPT API"
    api_version: str = "1.0.0"
    
    # LLM Provider Settings
    llm_provider: str = "mock"  # openai, huggingface, or mock (para testes sem API key)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    huggingface_api_key: Optional[str] = None
    huggingface_model: str = "microsoft/DialoGPT-medium"
    huggingface_api_url: Optional[str] = None
    
    # Application Settings
    max_tokens: int = 500
    temperature: float = 0.7
    
    # AWS Settings (for deployment)
    aws_region: str = "us-east-1"
    ecr_repository: Optional[str] = None
    ecs_cluster: Optional[str] = None
    ecs_service: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

