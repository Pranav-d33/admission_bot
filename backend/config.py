"""
Application Configuration Management
Centralized configuration settings using Pydantic for validation
"""
from pydantic_settings import BaseSettings
from pydantic import MongoDsn

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """
    Centralized application settings with type validation
    """
    # MongoDB Configuration
    MONGO_URI: MongoDsn = os.getenv(
        'MONGO_URI', 
        'mongodb://localhost:27017/rajasthan_tech_education' #cloud pe chala 
        
    )
    
    # Application Settings
    APP_NAME: str = "Rajasthan Tech Education Chatbot"
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # API Configuration
    API_PREFIX: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'development_secret_key')
    
    class Config:
        """Pydantic configuration for environment variable parsing"""
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()