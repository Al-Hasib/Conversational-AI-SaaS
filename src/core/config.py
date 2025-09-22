import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Conversational AI SaaS"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "conversational_ai_saas"
    
    # CORS settings
    ALLOWED_HOSTS: List[str] = ["*"]  # Configure properly in production
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()